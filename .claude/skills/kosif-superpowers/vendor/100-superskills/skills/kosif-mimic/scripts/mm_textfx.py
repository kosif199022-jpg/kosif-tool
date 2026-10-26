"""Text events of the remake: typeset each line in the matched font at the measured size and place,
then replay the measured entrance/exit curves frame by frame (alpha, offset, scale, blur, word-by-word)."""
from __future__ import annotations

from pathlib import Path

import numpy as np

import mm_img
import mm_render_text as RT
from mm_common import ASSETS, log

FALLBACK_FONTS = ["Amiri-Bold.ttf", "NotoNaskhArabic-700.ttf", "Cairo-700.ttf"]


def _interp(curve, u):
    if not curve:
        return None
    x = np.linspace(0, 1, len(curve))
    return float(np.interp(np.clip(u, 0, 1), x, curve))


def consensus_style(events: list[dict]) -> dict:
    """Style shared by the video: shadows/outlines measured on the clearest backgrounds."""
    shadows = [e["style"]["shadow"] for e in events if (e.get("style") or {}).get("shadow")
               and e["style"]["shadow"].get("fit", 0) >= 0.6]
    out = {}
    if shadows:
        out["shadow"] = {k: float(np.median([s[k] for s in shadows])) for k in ("dx_px", "dy_px", "blur_px", "opacity")}
        out["shadow"]["color"] = "#000000"
    outlines = [e["style"]["outline"] for e in events if (e.get("style") or {}).get("outline")]
    if len(outlines) >= max(1, len(events) // 2):
        out["outline"] = outlines[0]
    return out


class EventLayer:
    def __init__(self, ev: dict, W: int, H: int, analysis_w: int, engine: str = "auto",
                 consensus: dict | None = None, font_dirs: list[Path] | None = None):
        self.ev = ev
        self.id = ev["id"]
        self.W, self.H = W, H
        self.t = ev["time"]
        self.ok = False
        font = (ev.get("font") or {}).get("chosen")
        if not font or not Path(font).exists():
            for name in FALLBACK_FONTS:
                p = ASSETS / "fonts" / name
                if p.exists():
                    font = str(p)
                    break
        self.font = font
        style = dict(ev.get("style") or {})
        cons = consensus or {}
        sh = style.get("shadow")
        if (not sh or sh.get("fit", 0) < 0.6) and cons.get("shadow"):
            style["shadow"] = cons["shadow"]
        if not style.get("outline") and cons.get("outline"):
            style["outline"] = cons["outline"]
        self.style = style
        lines = [ln for ln in ev.get("lines", []) if (ln.get("text") or ln.get("ocr") or "").strip()]
        if not lines:
            log(f"text event {self.id}: no text — skipped (fill spec.texts[{self.id - 1}].lines[].text)")
            return
        placed = []
        for ln in lines:
            text = (ln.get("text") or ln.get("ocr")).strip()
            size, L = RT.fit_size(text, font, max(6.0, float(ln["ink_h"])), engine)
            alpha, words = L.alpha, L.words
            sx = 1.0
            if ln.get("ink_w") and L.ink_w > 0:
                sx = float(np.clip(ln["ink_w"] / L.ink_w, 0.9, 1.1))
                if abs(sx - 1) > 0.004:
                    nw = max(1, int(round(alpha.shape[1] * sx)))
                    alpha = mm_img.resize(alpha, (nw, alpha.shape[0]), "linear")
                    words = [mm_img.resize(w_, (nw, w_.shape[0]), "linear") for w_ in words]
            ink = RT._ink_bbox(alpha)
            icx, icy = (ink[0] + ink[2]) / 2, (ink[1] + ink[3]) / 2
            x0, y0, x1, y1 = ln["bbox"]
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            placed.append({"alpha": alpha, "words": words, "ox": cx - icx, "oy": cy - icy, "size": size, "sx": sx})
            ln["render"] = {"font": Path(font).name, "size_px": size, "x_scale": round(sx, 4)}
        gx0 = min(int(np.floor(p["ox"])) for p in placed)
        gy0 = min(int(np.floor(p["oy"])) for p in placed)
        gx1 = max(int(np.ceil(p["ox"])) + p["alpha"].shape[1] for p in placed)
        gy1 = max(int(np.ceil(p["oy"])) + p["alpha"].shape[0] for p in placed)
        A = np.zeros((gy1 - gy0 + 1, gx1 - gx0 + 1), np.float32)
        word_maps = []
        for p in placed:
            xi, yi = int(round(p["ox"])) - gx0, int(round(p["oy"])) - gy0
            h, w = p["alpha"].shape
            A[yi:yi + h, xi:xi + w] = np.maximum(A[yi:yi + h, xi:xi + w], p["alpha"])
            for wa in p["words"]:
                Wm = np.zeros_like(A)
                Wm[yi:yi + h, xi:xi + w] = wa
                word_maps.append(Wm)
        self.A = A
        self.words = word_maps
        self.gx0, self.gy0 = gx0, gy0
        ink = RT._ink_bbox(A)
        self.center = (gx0 + (ink[0] + ink[2]) / 2, gy0 + (ink[1] + ink[3]) / 2)
        self.base, (self.m, _) = RT.compose(A, self.style)
        self.word_onsets = self._map_words(ev.get("anim_in", {}).get("word_onsets"), "on")
        self.word_offsets = self._map_words(ev.get("anim_out", {}).get("word_offsets"), "off")
        self.sigma_table = self._blur_table(analysis_w)
        self.ok = True

    # -- word mapping: rendered words ↔ words detected on the reference (by position)
    def _map_words(self, det, key):
        if not det or not self.words:
            return None
        boxes = []
        for Wm in self.words:
            ys, xs = np.nonzero(Wm > 0.3)
            if len(xs) == 0:
                boxes.append(None)
                continue
            boxes.append((self.gx0 + xs.mean(), self.gy0 + ys.mean()))
        out = []
        for i, c in enumerate(boxes):
            if c is None:
                out.append(None)
                continue
            best, bd = None, 1e18
            for d in det:
                b = d.get("box")
                if not b:
                    continue
                inside = b[0] - 2 <= c[0] <= b[2] + 2 and b[1] - 6 <= c[1] <= b[3] + 6
                dist = (0 if inside else 1e6) + (c[0] - (b[0] + b[2]) / 2) ** 2 + (c[1] - (b[1] + b[3]) / 2) ** 2
                if dist < bd:
                    best, bd = d, dist
            out.append(best)
        # words without a match: interpolate by reading order
        if all(o is None for o in out):
            dd = det
            out = [dd[min(len(dd) - 1, int(round(i * (len(dd) - 1) / max(1, len(out) - 1))))] for i in range(len(out))]
        else:
            last = None
            for i in range(len(out)):
                if out[i] is None:
                    out[i] = last
                else:
                    last = out[i]
            first = next(o for o in out if o is not None)
            out = [o if o is not None else first for o in out]
        return out

    def _blur_table(self, analysis_w):
        """sharpness ratio (as the analyser measures it) → blur sigma at output resolution."""
        f = analysis_w / float(self.W)
        a = mm_img.resize(self.A, (max(8, int(self.A.shape[1] * f)), max(8, int(self.A.shape[0] * f))), "area")
        base = float(mm_img.sobel_mag(a * 255).mean()) + 1e-6
        tab = []
        for s in (0, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 11, 15, 20):
            b = mm_img.gaussian_blur(a * 255, s) if s > 0 else a * 255
            tab.append((float(mm_img.sobel_mag(b).mean()) / base, s / f))
        return tab

    def _sigma_for(self, ratio):
        tab = self.sigma_table
        ratio = float(np.clip(ratio, tab[-1][0], 1.0))
        for (r0, s0), (r1, s1) in zip(tab, tab[1:]):
            if r1 <= ratio <= r0:
                t = (ratio - r0) / (r1 - r0) if r1 != r0 else 0
                return s0 + t * (s1 - s0)
        return 0.0

    # -- per frame
    def state(self, n: int):
        t = self.t
        if not self.ok or n < t["in_start"] or n >= t["out_end"]:
            return None
        st = {"alpha": 1.0, "dx": 0.0, "dy": 0.0, "scale": 1.0, "sigma": 0.0, "words": None}
        if n < t["full_in"]:
            an = self.ev["anim_in"]
            u = (n - t["in_start"]) / max(1, t["full_in"] - t["in_start"])
            self._apply_curves(st, an, u, n, entrance=True)
        elif n >= t["full_out"]:
            an = self.ev["anim_out"]
            u = (n - (t["full_out"] - 1)) / max(1, t["out_end"] - t["full_out"] + 1)
            self._apply_curves(st, an, u, n, entrance=False)
        return st

    def _apply_curves(self, st, an, u, n, entrance):
        kind = an.get("type", "fade")
        c = an.get("curves") or {}
        if kind == "cut":
            return
        if kind == "words":
            src = self.word_onsets if entrance else self.word_offsets
            if src:
                ws = []
                for d in src:
                    if d is None:
                        ws.append(1.0)
                    elif entrance:
                        # linear ramp through the measured 50 % frame, slope from the 50 %→90 % frames
                        mid = d.get("mid", d["on"])
                        span = max(0.5, d.get("full", mid + 2) - mid + 0.5)
                        ws.append(float(np.clip(0.5 + (n - mid) * 0.5 / span, 0, 1)))
                    else:
                        ws.append(float(np.clip(1 - (n - d["off"] + 2) / 3.0, 0, 1)))
                st["words"] = ws
                return
        a = _interp(c.get("alpha"), u)
        st["alpha"] = 1.0 if a is None else float(np.clip(a, 0, 1))
        if kind not in ("fade", "words"):
            st["dx"] = _interp(c.get("dx"), u) or 0.0
            st["dy"] = _interp(c.get("dy"), u) or 0.0
            s = _interp(c.get("scale"), u)
            st["scale"] = 1.0 if s is None or s <= 0 else s
        if kind == "blur":
            sh = _interp(c.get("sharp"), u)
            if sh is not None:
                ratio = sh / max(0.05, st["alpha"])
                st["sigma"] = self._sigma_for(min(1.0, ratio))

    def draw(self, frame: np.ndarray, n: int) -> np.ndarray:
        st = self.state(n)
        if st is None:
            return frame
        if st["words"] is not None:
            A = np.zeros_like(self.A)
            for w_, Wm in zip(st["words"], self.words):
                if w_ > 0:
                    A = np.maximum(A, Wm * w_)
            layer, _ = RT.compose(A, self.style)
        else:
            layer = self.base
        x = self.gx0 - self.m
        y = self.gy0 - self.m
        if st["sigma"] > 0.3:
            pad = int(3 * st["sigma"]) + 2
            layer = np.pad(layer, ((pad, pad), (pad, pad), (0, 0)))
            layer = mm_img.gaussian_blur(layer, st["sigma"])
            x -= pad
            y -= pad
        s = st["scale"]
        if abs(s - 1) > 0.002:
            h, w = layer.shape[:2]
            nw, nh = max(1, int(round(w * s))), max(1, int(round(h * s)))
            layer = mm_img.resize(layer, (nw, nh), "linear" if s > 1 else "area")
            cx, cy = self.center
            x = cx + (x - cx) * s
            y = cy + (y - cy) * s
        x += st["dx"]
        y += st["dy"]
        return RT.composite(frame, layer, x, y, st["alpha"])
