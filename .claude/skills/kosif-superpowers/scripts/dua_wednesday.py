#!/usr/bin/env python3
"""«دعاء يوم الأربعاء» — the Wednesday-morning dua reel engine (9:16 motion graphics over licensed footage).

One project.json drives a deterministic frame-by-frame compositor: one dua phrase = one shot, cut just before the
voice onset with a different transition each time; per-word kinetic Arabic text timed to the voice with a gold
karaoke highlight; a mihrab arch with a crescent drawn on behind a gold Ruqaa title; golden dust, god rays,
bloom, warm grade, vignette and grain. The voice track is stream-copied untouched.

Workflow (full guide: dua-wednesday/WORKFLOW.md):
    python3 scripts/dua_wednesday.py doctor
    python3 scripts/dua_wednesday.py fetch <tiktok-or-video-url> --job JOB         # source.mp4 + voice.m4a
    python3 scripts/dua_wednesday.py caption-times JOB/source.mp4                  # on-screen caption onsets
    python3 scripts/dua_wednesday.py asr --job JOB [--model medium]                # words.json + lines.draft.json
    python3 scripts/dua_wednesday.py init --job JOB                                # project.json from the example
    python3 scripts/dua_wednesday.py prep --job JOB a.mp4 b.mp4:556 ...            # clips → JOB/v/NN.mp4 (9:16)
    python3 scripts/dua_wednesday.py sprites --job JOB                             # text sprites (Chromium)
    python3 scripts/dua_wednesday.py stills --job JOB --t 2,5.4,20                 # review frames
    python3 scripts/dua_wednesday.py render --job JOB [--workers 4]                # out/master.mp4 + out/tiktok.mp4
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
PKG = SKILL / "dua-wednesday"
W, H = 1080, 1920
TITLE_CY, DATE_CY, DIV_Y, DUA_CY, SUB_CY = 300, 462, 520, 990, 1345
TRANSITIONS = ["light_leak", "whip", "ink_reveal", "zoom_through", "iris_gold",
               "film_burn", "spin_zoom", "bokeh_blur", "slide_up"]
TDUR_DEFAULT = {"light_leak": 0.6, "whip": 0.45, "ink_reveal": 0.7, "zoom_through": 0.5, "iris_gold": 0.65,
                "film_burn": 0.7, "spin_zoom": 0.55, "bokeh_blur": 0.7, "slide_up": 0.5}
KB_DEFAULT = [(1.00, 1.10, 0, -40), (1.12, 1.02, 30, 0), (1.02, 1.12, -20, 0), (1.10, 1.02, 0, 40),
              (1.02, 1.10, 0, -20), (1.06, 1.14, 0, 30), (1.12, 1.03, -25, 0), (1.02, 1.12, 0, -30),
              (1.10, 1.02, 20, 0), (1.00, 1.12, 0, 30)]


def fonts():
    return {
        "ArefRuqaa": str(SKILL / "proofs/_shared/fonts/ArefRuqaa-Bold.ttf"),
        "Gulzar": str(PKG / "fonts/Gulzar-Regular.ttf"),
        "Rakkas": str(PKG / "fonts/Rakkas-Regular.ttf"),
        "ElMessiri": str(PKG / "fonts/ElMessiri[wght].ttf"),
    }


# ====================================================================== project
def load_project(job: Path) -> dict:
    p = json.loads((job / "project.json").read_text(encoding="utf-8"))
    p["fps"] = int(p.get("fps", 30))
    lines = [[(w, float(t)) for w, t in line] for line in p["lines"]]
    p["lines"] = lines
    p["duration"] = float(p.get("duration") or lines[-1][-1][1] + 1.2)
    lead = float(p.get("cut_lead", 0.24))
    p["cuts"] = [0.0] + [line[0][1] - lead for line in lines[1:]]
    n_cuts = len(lines) - 1
    tr = p.get("transitions") or []
    p["transitions"] = [(tr[i] if i < len(tr) else TRANSITIONS[i % len(TRANSITIONS)]) for i in range(n_cuts)]
    td = p.get("tdur") or []
    p["tdur"] = [float(td[i]) if i < len(td) else TDUR_DEFAULT.get(p["transitions"][i], 0.6) for i in range(n_cuts)]
    shots = p.get("shots") or []
    if not shots:
        raise SystemExit("project.json needs shots (one licensed clip per dua line; run prep)")
    p["shots"] = [dict(shots[i % len(shots)]) for i in range(len(lines))]
    for i, s in enumerate(p["shots"]):
        s.setdefault("offset", 0.5)
        s["kb"] = tuple(s.get("kb") or KB_DEFAULT[i % len(KB_DEFAULT)])
        s["clip"] = str((job / s["clip"]).resolve())
    p["audio"] = str((job / p.get("audio", "voice.m4a")).resolve())
    p.setdefault("title", "الأربعاء")
    p.setdefault("subtitle", "صباح الخير والسعادة")
    p.setdefault("date_line", "")
    for c in range(n_cuts):            # a transition must fit inside both neighbouring shots
        lo = p["cuts"][c + 1] - p["cuts"][c]
        hi = (p["cuts"][c + 2] if c + 2 < len(p["cuts"]) else p["duration"]) - p["cuts"][c + 1]
        p["tdur"][c] = min(p["tdur"][c], 0.8 * min(lo, hi))
    return p


def sprite_spec(p):
    items = [
        {"id": "title", "text": p["title"], "font": "ArefRuqaa", "size": 200, "cx": 540, "cy": TITLE_CY, "maxW": 1000, "style": "gold", "words": False, "lh": 1.5},
        {"id": "date", "text": p["date_line"] or " ", "font": "ElMessiri", "size": 44, "weight": 600, "cx": 540, "cy": DATE_CY, "maxW": 1000, "style": "cream", "words": False},
        {"id": "sub", "text": p["subtitle"] or " ", "font": "Rakkas", "size": 92, "cx": 540, "cy": SUB_CY, "maxW": 1000, "style": "gold", "words": False},
    ]
    for i, line in enumerate(p["lines"]):
        text = " ".join(w for w, _ in line)
        for st in ("white", "gold"):
            items.append({"id": f"L{i}{st[0]}", "text": text, "font": "Gulzar", "size": int(p.get("dua_size", 128)), "cx": 540,
                          "cy": DUA_CY, "maxW": 960, "style": st, "words": True, "lh": 1.75})
    return {"fonts": fonts(), "items": items}


# ====================================================================== engine
class Engine:
    """All maths for one project; heavy imports live here so --help works without numpy/OpenCV."""

    def __init__(self, job: Path, p: dict):
        import cv2
        import numpy as np
        self.cv2, self.np = cv2, np
        self.job, self.p = job, p
        self.FPS, self.DUR = p["fps"], p["duration"]
        self.N = int(round(self.DUR * self.FPS))
        self.LINES, self.CUTS, self.TRANS, self.TDUR, self.SHOTS = p["lines"], p["cuts"], p["transitions"], p["tdur"], p["shots"]
        rng = np.random.default_rng(int(p.get("seed", 1448)))
        self.YY, self.XX = np.mgrid[0:H, 0:W].astype(np.float32)
        R = np.sqrt((self.XX - W / 2) ** 2 + (self.YY - H / 2) ** 2)
        self.VIGNETTE = (1 - 0.5 * np.clip((R / (0.62 * math.hypot(W, H)) - 0.35) / 0.65, 0, 1) ** 1.6)[..., None]
        YY = self.YY
        self.SCRIM = (1 - 0.42 * np.exp(-((YY - DUA_CY) / 210) ** 2) - 0.30 * np.exp(-((YY - 380) / 230) ** 2)
                      - 0.22 * np.exp(-((YY - SUB_CY) / 120) ** 2))[..., None]
        self.NOISE_A, self.NOISE_B = self.smooth_noise(90, 1), self.smooth_noise(140, 2)
        self.INK = np.clip(0.55 * self.NOISE_A + 0.45 * (YY / H), 0, 1)
        self.GRAIN = [np.random.default_rng(100 + k).standard_normal((H // 2, W // 2)).astype(np.float32) for k in range(6)]
        self.GOLD = np.array([80, 190, 245], np.float32) / 255     # BGR
        self.WARM = np.array([60, 140, 255], np.float32) / 255
        self.BOKEH, self.RAYS, self.CLIPS, self.GAIN = None, {}, {}, {}
        n = 110
        self.P = dict(x=rng.uniform(0, W, n), y=rng.uniform(0, H, n), v=rng.uniform(18, 70, n), a=rng.uniform(8, 35, n),
                      f=rng.uniform(.2, .9, n), s=rng.uniform(1.2, 4.2, n), ph=rng.uniform(0, 6.28, n), tw=rng.uniform(1.5, 4.0, n))
        self.KERNELS = {round(s, 1): self.dot_kernel(s) for s in np.arange(1.0, 4.6, 0.1)}
        self.LUT = self.make_lut()
        self.energy = self.audio_energy()
        self.S = self.load_sprites()

    # ---------------------------------------------------------------- helpers
    @staticmethod
    def clamp01(x): return min(max(x, 0.0), 1.0)
    def eoc(self, x): x = self.clamp01(x); return 1 - (1 - x) ** 3
    def eio(self, x): x = self.clamp01(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
    def eob(self, x, s=1.6): x = self.clamp01(x) - 1; return 1 + (s + 1) * x ** 3 + s * x ** 2
    def smooth(self, a, b, x): x = self.clamp01((x - a) / (b - a)); return x * x * (3 - 2 * x)

    def blur(self, img, sigma, down=4):
        cv2 = self.cv2
        if sigma < 0.6:
            return img
        if down > 1 and sigma > 3:
            h, w = img.shape[:2]
            s = cv2.resize(img, (w // down, h // down), interpolation=cv2.INTER_AREA)
            return cv2.resize(cv2.GaussianBlur(s, (0, 0), sigma / down), (w, h), interpolation=cv2.INTER_LINEAR)
        return cv2.GaussianBlur(img, (0, 0), sigma)

    def smooth_noise(self, scale, seed):
        np, cv2 = self.np, self.cv2
        small = np.random.default_rng(seed).random((H // scale + 2, W // scale + 2)).astype(np.float32)
        n = cv2.GaussianBlur(cv2.resize(small, (W, H), interpolation=cv2.INTER_CUBIC), (0, 0), scale / 3)
        return (n - n.min()) / (n.max() - n.min())

    def warp(self, img, scale=1.0, angle=0.0, dx=0.0, dy=0.0):
        cv2 = self.cv2
        M = cv2.getRotationMatrix2D((W / 2, H / 2), angle, scale)
        M[0, 2] += dx; M[1, 2] += dy
        return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    def dot_kernel(self, s):
        g = self.cv2.getGaussianKernel(int(s * 4) * 2 + 1, s)
        return (g @ g.T / (g @ g.T).max()).astype(self.np.float32)

    def make_lut(self):
        np = self.np
        x = np.arange(256, dtype=np.float32) / 255
        def sc(v): return v + 0.18 * (v - 0.5) * (1 - abs(2 * v - 1))
        return np.stack([sc(np.clip(0.035 + 0.9 * x ** 1.06, 0, 1)), sc(np.clip(0.03 + 0.96 * x, 0, 1)),
                         sc(np.clip(0.04 + x ** 0.94, 0, 1))], -1)

    def grade(self, img):
        u8 = (self.np.clip(img, 0, 1) * 255).astype(self.np.uint8)
        out = self.np.empty_like(img)
        for c in range(3):
            out[..., c] = self.LUT[u8[..., c], c]
        return out

    def audio_energy(self):
        np = self.np
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", self.p["audio"], "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                             capture_output=True).stdout
        hop = 48000 // self.FPS
        a = np.frombuffer(raw, np.float32)
        a = np.pad(a, (0, max(0, self.N * hop - len(a))))      # audio can be a few ms short of the timeline
        e = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2) + 1e-9) for i in range(self.N)])
        e = np.convolve(e, np.ones(3) / 3, mode="same")
        lo, hi = np.percentile(e, 10), np.percentile(e, 98)
        return np.clip((e - lo) / max(hi - lo, 1e-9), 0, 1)

    # ---------------------------------------------------------------- layers
    def leak(self, p):
        np = self.np
        cx, cy = W * (1.2 - 1.4 * p), H * (0.25 + 0.3 * p)
        d = ((self.XX - cx) / (W * 0.55)) ** 2 + ((self.YY - cy) / (H * 0.45)) ** 2
        return np.exp(-d)[..., None] * np.array([0.25, 0.55, 1.0], np.float32)

    def rays(self, t):
        np, cv2 = self.np, self.cv2
        k = round(t * 6) / 6
        if k not in self.RAYS:
            if len(self.RAYS) > 4:
                self.RAYS.clear()
            ox, oy = W * 0.92, -H * 0.08
            ang = np.arctan2(self.YY - oy, self.XX - ox)
            dist = np.sqrt((self.XX - ox) ** 2 + (self.YY - oy) ** 2)
            streak = 0.5 + 0.5 * np.sin(ang * 38 + k * 0.35) * np.sin(ang * 17 - k * 0.21)
            lay = (np.clip(streak, 0, 1) ** 3 * np.exp(-dist / (H * 0.55)))[..., None] * np.array([0.55, 0.8, 1.0], np.float32)
            self.RAYS[k] = cv2.resize(cv2.resize(lay, (W // 4, H // 4)), (W, H))
        return self.RAYS[k]

    def bokeh(self):
        np, cv2 = self.np, self.cv2
        if self.BOKEH is None:
            r = np.random.default_rng(7)
            lay = np.zeros((H, W, 3), np.float32)
            for _ in range(26):
                c = np.array([r.uniform(.4, .7), r.uniform(.7, .9), 1.0], np.float32) * r.uniform(.25, .6)
                cv2.circle(lay, (int(r.uniform(0, W)), int(r.uniform(0, H))), int(r.uniform(30, 110)), c.tolist(), -1, cv2.LINE_AA)
            self.BOKEH = self.blur(lay, 6, down=2)
        return self.BOKEH

    def particles(self, frame, t, energy):
        np, P = self.np, self.P
        col = np.array([0.55, 0.85, 1.0], np.float32)
        for i in range(len(P["x"])):
            y = (P["y"][i] - P["v"][i] * t) % (H + 40) - 20
            x = P["x"][i] + P["a"][i] * math.sin(P["f"][i] * t + P["ph"][i])
            a = (0.35 + 0.65 * (0.5 + 0.5 * math.sin(P["tw"][i] * t + P["ph"][i]))) * (0.45 + 0.9 * energy)
            k = self.KERNELS[round(min(max(P["s"][i], 1.0), 4.5), 1)]
            r = k.shape[0] // 2
            xi, yi = int(x), int(y)
            x0, y0, x1, y1 = max(xi - r, 0), max(yi - r, 0), min(xi + r + 1, W), min(yi + r + 1, H)
            if x0 < x1 and y0 < y1:
                frame[y0:y1, x0:x1] += k[y0 - (yi - r):y1 - (yi - r), x0 - (xi - r):x1 - (xi - r)][..., None] * a * col

    # ---------------------------------------------------------------- footage
    def clip_frame(self, path, idx):
        np = self.np
        c = self.CLIPS.get(path)
        if c is None or idx != c["next"]:
            if c:
                c["proc"].kill()
            proc = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{idx / self.FPS:.4f}", "-i", path,
                                     "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
            c = self.CLIPS[path] = {"proc": proc, "next": idx}
        buf = c["proc"].stdout.read(W * H * 3)
        if len(buf) < W * H * 3:                      # loop short clips
            c["proc"].kill(); del self.CLIPS[path]
            return self.clip_frame(path, 0) if idx else np.zeros((H, W, 3), np.uint8)
        c["next"] = idx + 1
        return np.frombuffer(buf, np.uint8).reshape(H, W, 3)

    def shot_bounds(self, i):
        a = self.CUTS[i] - (self.TDUR[i - 1] / 2 if i > 0 else 0)
        b = (self.CUTS[i + 1] + self.TDUR[i] / 2) if i + 1 < len(self.CUTS) else self.DUR
        return a, b

    def shot_frame(self, i, t):
        np = self.np
        s = self.SHOTS[i]
        z0, z1, dx, dy = s["kb"]
        a, b = self.shot_bounds(i)
        u = self.clamp01((t - a) / (b - a))
        f = self.clip_frame(s["clip"], int(round((s["offset"] + t - a) * self.FPS))).astype(np.float32) / 255
        key = (s["clip"], i)
        if key not in self.GAIN:             # per-shot auto exposure toward a calm, warm mid level
            self.GAIN[key] = float(np.clip(float(s.get("gain", 0)) or 0.36 / max(float(f.mean()), 1e-3), 0.6, 1.15))
        e = self.eio(u) * 0.6 + u * 0.4
        return self.warp(f * self.GAIN[key], z0 + (z1 - z0) * e, 0, dx * e, dy * e)

    # ---------------------------------------------------------------- transitions
    def transition(self, kind, A, B, p):
        np, cv2 = self.np, self.cv2
        s = math.sin(math.pi * p)
        if kind == "light_leak":
            m = self.smooth(0.3, 0.7, p)
            return 1 - (1 - (A * (1 - m) + B * m)) * (1 - np.clip(self.leak(p) * 1.25 * s, 0, 1))
        if kind == "whip":
            off = int(self.eio(p) * W)
            out = np.concatenate([A, B], axis=1)[:, off:off + W]
            k = int(140 * s) | 1
            return cv2.blur(out, (k, 1)) if k > 1 else out
        if kind == "ink_reveal":
            th = p * 1.25 - 0.1
            m = np.clip((th - self.INK) / 0.06, 0, 1)[..., None]
            edge = np.exp(-((self.INK - th) / 0.018) ** 2)[..., None] * s
            return A * (1 - m) + B * m + edge * self.GOLD * 1.4
        if kind == "zoom_through":
            src, q = (A, (p / 0.5) ** 2) if p < 0.5 else (B, (1 - (p - 0.5) / 0.5) ** 2)
            return sum(self.warp(src, 1 + q * (0.5 + 0.12 * j)) for j in range(4)) / 4 + s ** 6 * 0.9
        if kind == "iris_gold":
            r = self.eio(p) * math.hypot(W, H) / 2 * 1.05
            d = np.sqrt((self.XX - W / 2) ** 2 + (self.YY - H * 0.52) ** 2)
            m = np.clip((r - d) / 18, 0, 1)[..., None]
            ring = np.exp(-((d - r) / 9) ** 2)[..., None] * s
            return A * (1 - m) + B * m + ring * self.GOLD * 1.6
        if kind == "film_burn":
            burn = np.clip((p * 1.8 - self.NOISE_B) * 2.2, 0, 1)[..., None]
            heat = burn * np.array([0.12, 0.42, 0.95], np.float32) + burn ** 4 * 0.35
            m = self.smooth(0.45, 0.75, p)
            return 1 - (1 - (A * (1 - m) + B * m)) * (1 - np.clip(heat * s ** 1.5 * 1.05, 0, 1))
        if kind == "spin_zoom":
            e = self.eio(p)
            out = self.warp(A, 1 + e * 0.7, -e * 28) if p < 0.5 else self.warp(B, 1 + (1 - e) * 0.7, (1 - e) * 28)
            return self.blur(out, 14 * s)
        if kind == "bokeh_blur":
            m = self.smooth(0.25, 0.75, p)
            out = self.blur(A, 18 * self.smooth(0, 0.6, p)) * (1 - m) + self.blur(B, 18 * (1 - self.smooth(0.4, 1, p))) * m
            return 1 - (1 - out) * (1 - self.bokeh() * s)
        if kind == "slide_up":
            off = int(self.eio(p) * H)
            out = np.concatenate([A, B], axis=0)[off:off + H]
            k = int(120 * s) | 1
            return cv2.blur(out, (1, k)) if k > 1 else out
        return B if p > .5 else A

    def background(self, t):
        C, T = self.CUTS, self.TDUR
        i = max(k for k in range(len(C)) if C[k] - (T[k - 1] / 2 if k else 0) <= t)
        if i > 0 and t < C[i] + T[i - 1] / 2:
            p = (t - (C[i] - T[i - 1] / 2)) / T[i - 1]
            return self.transition(self.TRANS[i - 1], self.shot_frame(i - 1, t), self.shot_frame(i, t), self.clamp01(p))
        return self.shot_frame(i, t)

    # ---------------------------------------------------------------- text
    def load_sprites(self):
        np, cv2 = self.np, self.cv2
        d = self.job / "sprites"
        man = json.loads((d / "manifest.json").read_text())
        out = {}
        for k, recs in man.items():
            lst = []
            for r in recs:
                im = cv2.imread(str(d / r["file"]), cv2.IMREAD_UNCHANGED).astype(np.float32) / 255
                a = im[..., 3:4]
                lst.append(dict(rgb=im[..., :3], a=a, x=r["x"], y=r["y"], w=r["w"], h=r["h"],
                                shadow=np.clip(cv2.GaussianBlur(cv2.dilate(a, np.ones((5, 5))), (0, 0), 9)[..., None] * 1.6, 0, 1),
                                glow=cv2.GaussianBlur(a, (0, 0), 16)[..., None]))
            out[k] = lst
        return out

    def place(self, frame, sp, alpha, rgb=None, a=None, scale=1.0, dy=0.0, sigma=0.0, shadow_k=0.75, glow_k=0.0, glow_col=None, mask=None):
        np, cv2 = self.np, self.cv2
        if alpha <= 0.003:
            return
        rgb = sp["rgb"] if rgb is None else rgb
        a = sp["a"] if a is None else a
        shadow, glow = sp["shadow"], sp["glow"]
        h, w = a.shape[:2]
        if scale != 1.0 or dy or sigma > 0.5:
            M = cv2.getRotationMatrix2D((w / 2, h / 2), 0, scale); M[1, 2] += dy
            st = cv2.warpAffine(np.concatenate([rgb, a, shadow, glow], -1), M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            if sigma > 0.5:
                st = cv2.GaussianBlur(st, (0, 0), sigma)
            rgb, a, shadow, glow = st[..., :3], st[..., 3:4], st[..., 4:5], st[..., 5:6]
        if mask is not None:
            a, shadow, glow = a * mask, shadow * mask, glow * mask
        x, y = sp["x"], sp["y"]
        x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
        sl = (slice(y0 - y, y1 - y), slice(x0 - x, x1 - x))
        roi = frame[y0:y1, x0:x1]
        roi *= 1 - np.clip(shadow[sl] * shadow_k * alpha, 0, 0.92)
        if glow_k:
            roi += glow[sl] * (self.GOLD if glow_col is None else glow_col) * glow_k * alpha
        aa = a[sl] * alpha
        roi[:] = roi * (1 - aa) + rgb[sl] * aa

    def glint(self, sp, u, width=0.12):
        np = self.np
        h, w = sp["a"].shape[:2]
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        d = (xx + (yy - h / 2) * 0.45) - (1.3 - 1.6 * u) * w
        return np.exp(-(d / (width * w)) ** 2)[..., None]

    def draw_mihrab(self, frame, t):
        """Mihrab (pointed mosque arch) framing the title, drawn on from its feet to the apex, crowned by a crescent."""
        np, cv2 = self.np, self.cv2
        prog = self.smooth(0.1, 1.6, t)
        if prog <= 0:
            return
        LW, LH, X0, Y0 = 800, 520, 140, 20
        lay = np.zeros((LH, LW, 3), np.float32)
        col = (self.GOLD * 0.95).tolist()
        cx = LW / 2

        def arch(half, spring, apex, foot):
            pts = [(cx - half, foot), (cx - half, spring)]
            p0, p1, p2, p3 = (cx - half, spring), (cx - half, spring - (spring - apex) * 0.62), (cx - half * 0.32, apex + 26), (cx, apex)
            for k in range(1, 41):
                u = k / 40
                pts.append(tuple((1-u)**3*a + 3*(1-u)**2*u*b + 3*(1-u)*u**2*c + u**3*d for a, b, c, d in zip(p0, p1, p2, p3)))
            return pts

        def draw_side(pts, p, mirror):
            L = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
            tot, acc = sum(L), 0.0
            for (a, b), d in zip(zip(pts, pts[1:]), L):
                if acc >= p * tot:
                    break
                f = min(1.0, (p * tot - acc) / d)
                e = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
                if mirror:
                    a, e = (2 * cx - a[0], a[1]), (2 * cx - e[0], e[1])
                cv2.line(lay, (int(a[0] * 4), int(a[1] * 4)), (int(e[0] * 4), int(e[1] * 4)), col, 2, cv2.LINE_AA, 2)
                acc += d

        for half, apex, k in ((370, 96, 0.0), (352, 118, 0.12)):
            pts = arch(half, 300, apex, LH - 20)
            pp = self.clamp01(prog * 1.25 - k)
            draw_side(pts, pp, False); draw_side(pts, pp, True)
        c = self.eob((t - 1.0) / 0.8, 1.3)
        if c > 0:
            R = 34
            cy = 52 + 30 * (1 - min(c, 1.0)) + 2.5 * math.sin(t * 1.3)
            m = np.zeros((LH, LW), np.float32)
            cv2.circle(m, (int(cx * 4), int(cy * 4)), int(R * 4), 1.0, -1, cv2.LINE_AA, 2)
            cv2.circle(m, (int((cx + 15) * 4), int((cy - 9) * 4)), int(R * 0.86 * 4), 0.0, -1, cv2.LINE_AA, 2)
            m = m[..., None] * self.clamp01(c)
            shade = np.clip(1.15 - (self.YY[:LH, :LW, None] - (cy - R)) / (2 * R) * 0.5, 0.6, 1.2)
            lay = lay * (1 - m) + m * self.GOLD * 1.25 * shade
        lay = lay + self.blur(lay, 7, down=1) * 1.4
        frame[Y0:Y0 + LH, X0:X0 + LW] += lay * 0.85 * (1 - 0.2 * self.smooth(2.0, 4.0, t))

    def draw_divider(self, frame, t):
        np, cv2 = self.np, self.cv2
        p = self.eoc((t - 0.7) / 0.9)
        if p <= 0:
            return
        half = int(250 * p)
        lay = np.zeros((40, W, 3), np.float32)
        col = (self.GOLD * 0.95).tolist()
        cv2.line(lay, (540 - half, 20), (540 - 22, 20), col, 2, cv2.LINE_AA)
        cv2.line(lay, (540 + 22, 20), (540 + half, 20), col, 2, cv2.LINE_AA)
        d = int(12 * self.eob((t - 0.7) / 0.5))
        if d > 0:
            cv2.fillConvexPoly(lay, np.array([(540, 20 - d), (540 + d, 20), (540, 20 + d), (540 - d, 20)]), col, cv2.LINE_AA)
        for sx in (-1, 1):
            cv2.circle(lay, (540 + sx * (half + 8), 20), 3, col, -1, cv2.LINE_AA)
        frame[DIV_Y - 20:DIV_Y + 20] += (lay + self.blur(lay, 4, down=1)) * 0.9

    def draw_text(self, frame, t):
        np, S = self.np, self.S
        ti = S["title"][0]
        rev = self.eio((t - 0.05) / 1.1)
        if rev > 0:             # right→left calligraphic wipe with a glinting nib, then a periodic glint
            w = ti["a"].shape[1]
            xx = np.arange(w, dtype=np.float32)[None, :, None]
            edge = (1 - rev) * (w + 80) - 40
            nib = np.exp(-((xx - edge) / 18) ** 2) * (1 - self.smooth(0.85, 1, rev))
            self.place(frame, ti, 1.0, rgb=ti["rgb"] + nib * 0.9, scale=1.08 - 0.08 * self.eoc(rev), sigma=4 * (1 - rev),
                       glow_k=0.55, mask=np.clip((xx - edge) / 50, 0, 1))
            cyc = (t - 2.0) % 6.0
            if t > 2.0 and cyc < 1.2:
                frame[ti["y"]:ti["y"] + ti["h"], ti["x"]:ti["x"] + ti["w"]] += self.glint(ti, cyc / 1.2) * ti["a"] * 0.75
        d = S["date"][0]
        u = self.eoc((t - 0.55) / 0.7)
        self.place(frame, d, u, dy=24 * (1 - u), sigma=3 * (1 - u), shadow_k=0.85)
        self.draw_divider(frame, t)
        s = S["sub"][0]
        u = self.eoc((t - 1.1) / 0.8)
        self.place(frame, s, u, scale=1.15 - 0.15 * u, sigma=5 * (1 - u), glow_k=0.35)
        cyc = (t - 4.5) % 6.0
        if t > 4.5 and cyc < 1.0:
            frame[s["y"]:s["y"] + s["h"], s["x"]:s["x"] + s["w"]] += self.glint(s, cyc) * s["a"] * 0.7
        L, nL = self.LINES, len(self.LINES)
        for i, line in enumerate(L):
            last = i + 1 == nL
            end = self.DUR + 1 if last else self.CUTS[i + 1] - 0.05
            if t < line[0][1] - 0.2 or t > end:
                continue
            for k, (word, tk) in enumerate(line):
                a = (t - (tk - 0.08)) / 0.45
                if a <= 0:
                    continue
                nxt = line[k + 1][1] if k + 1 < len(line) else (self.DUR if last else end - 0.4)
                gold = 1.0 if t < nxt else 1 - self.smooth(0, 0.35, t - nxt)
                ex = 0.0 if last else self.clamp01((t - (end - 0.38 + 0.035 * k)) / 0.3)
                wsp, gsp = S[f"L{i}w"][k], S[f"L{i}g"][k]
                self.place(frame, wsp, self.eoc(a) * (1 - ex),
                           rgb=wsp["rgb"] * (1 - gold) + gsp["rgb"] * gold, a=wsp["a"] * (1 - gold) + gsp["a"] * gold,
                           scale=1.22 - 0.22 * self.eob(a, 1.4), dy=42 * (1 - self.eoc(a)) - 34 * self.eio(ex),
                           sigma=9 * (1 - self.eoc(a)) + 7 * ex, shadow_k=1.0,
                           glow_k=gold * (0.35 + 0.5 * math.exp(-max(t - tk, 0) * 3.0)), glow_col=self.WARM)

    # ---------------------------------------------------------------- frame
    def frame(self, n):
        np, cv2 = self.np, self.cv2
        t = n / self.FPS
        f = self.grade(self.background(t)) * self.SCRIM * self.VIGNETTE
        small = cv2.resize(f, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
        f += cv2.resize(cv2.GaussianBlur(np.clip(small - 0.62, 0, 1) * 1.8, (0, 0), 10), (W, H)) * 0.55      # bloom
        rk = 0.22 + 0.25 * (1 - self.smooth(0, 3.0, t)) + 0.08 * self.energy[n]
        f = 1 - (1 - f) * (1 - np.clip(self.rays(t) * rk, 0, 1))                                              # god rays
        self.draw_mihrab(f, t)
        self.particles(f, t, self.energy[n])
        self.draw_text(f, t)
        f += cv2.resize(self.GRAIN[n % 6], (W, H), interpolation=cv2.INTER_NEAREST)[..., None] * 0.022
        f *= self.smooth(0, 0.3, t) * (1 - self.smooth(self.DUR - 0.45, self.DUR, t))
        if t > self.DUR - 0.7:
            q = self.smooth(self.DUR - 0.7, self.DUR, t)
            f += self.leak(q) * 0.6 * math.sin(math.pi * q)
        return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)


# ====================================================================== commands
def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def cmd_doctor(a):
    rows = [("ffmpeg", bool(shutil.which("ffmpeg"))), ("ffprobe", bool(shutil.which("ffprobe"))), ("node", bool(shutil.which("node")))]
    for mod in ("numpy", "cv2", "faster_whisper", "yt_dlp"):
        try:
            __import__(mod); rows.append((mod, True))
        except ImportError:
            rows.append((mod, False))
    pw = subprocess.run(["node", "-e", "require(process.argv[1])", "/opt/node-tools/node_modules/playwright"],
                        capture_output=True).returncode == 0 if shutil.which("node") else False
    rows.append(("playwright (node)", pw))
    rows += [(f"font {k}", Path(v).exists()) for k, v in fonts().items()]
    for k, ok in rows:
        print(f"[{'ok' if ok else '--'}] {k}")
    print("pip install opencv-python-headless numpy   # engine;  pip install faster-whisper yt-dlp   # asr / fetch")


def cmd_fetch(a):
    job = Path(a.job); job.mkdir(parents=True, exist_ok=True)
    src = job / "source.mp4"
    ok = False
    try:
        run([sys.executable, "-m", "yt_dlp", "-q", "-f", "mp4/best", "-o", str(src), a.url]); ok = src.exists()
    except Exception:
        ok = False
    if not ok and "tiktok" in a.url:           # yt-dlp's TikTok extractor breaks often; public no-watermark endpoint
        import urllib.parse, urllib.request
        api = "https://www.tikwm.com/api/?hd=1&url=" + urllib.parse.quote(a.url, safe="")
        d = json.loads(urllib.request.urlopen(api, timeout=30).read())["data"]
        (job / "info.json").write_text(json.dumps({k: d.get(k) for k in ("id", "title", "duration", "author", "music_info")},
                                                  ensure_ascii=False, indent=1), encoding="utf-8")
        for key in ("hdplay", "play"):
            try:
                urllib.request.urlretrieve(d[key], src); ok = True; break
            except Exception:
                continue
    if not ok:
        raise SystemExit("could not download the video; save it yourself as JOB/source.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vn", "-c:a", "copy", str(job / "voice.m4a")])
    print(f"source → {src}\nvoice  → {job / 'voice.m4a'} (stream copy, untouched)")


def cmd_caption_times(a):
    """On-screen caption onsets of a reference reel: white-text coverage change in a horizontal band."""
    import numpy as np
    y0, y1 = (float(v) for v in a.band.split(":"))
    probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height",
                                       "-of", "json", a.video], capture_output=True, text=True).stdout)["streams"][0]
    w, h = probe["width"], probe["height"]
    by0, bh = int(h * y0), int(h * (y1 - y0))
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vf", f"fps=10,crop={w}:{bh}:0:{by0},scale=480:60,format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, 60, 480)
    m = frames > 235
    cov = m.mean(axis=(1, 2))
    onsets, on = [], False
    for i in range(1, len(cov)):
        if not on and cov[i] > 0.02 and cov[i - 1] <= 0.02:
            onsets.append(round(i / 10, 2)); on = True
        elif on and cov[i] <= 0.012:
            on = False
    print(json.dumps({"caption_onsets_s": onsets}, ensure_ascii=False))


def cmd_asr(a):
    import numpy as np
    from faster_whisper import WhisperModel
    job = Path(a.job)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(job / "voice.m4a"), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True).stdout
    audio = np.frombuffer(raw, np.float32)
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    words = []
    # transcribe in ~10 s windows: long windows make whisper skip or smear the first phrases of a dua
    step = 16000 * 10
    for s0 in range(0, len(audio), step):
        segs, _ = model.transcribe(audio[s0:s0 + step + 16000 // 2], language="ar", word_timestamps=True, beam_size=5)
        for sg in segs:
            for w in sg.words:
                t = s0 / 16000 + w.start
                if words and t < words[-1]["s"] + 0.05:
                    continue
                words.append({"w": w.word.strip(), "s": round(t, 2), "e": round(s0 / 16000 + w.end, 2), "p": round(w.probability, 2)})
    # energy onsets refine each phrase start (the cut is placed just before the voice rises)
    hop = 160
    e = np.array([np.sqrt(np.mean(audio[i:i + hop] ** 2) + 1e-9) for i in range(0, len(audio) - hop, hop)])
    db = 20 * np.log10(e)
    lines, cur = [], []
    for i, w in enumerate(words):
        gap = w["s"] - words[i - 1]["e"] if i else 0
        if cur and (gap > a.gap or len(cur) >= a.max_words):
            lines.append(cur); cur = []
        cur.append(w)
    if cur:
        lines.append(cur)
    draft = []
    for ln in lines:
        s = ln[0]["s"]
        k0, k1 = int(max(s - 0.4, 0) * 100), int((s + 0.8) * 100)
        rise = next((k for k in range(k0, min(k1, len(db))) if db[k] > a.rise_db), None)
        first = round(rise / 100, 2) if rise is not None else s
        row = [[ln[0]["w"], first]] + [[w["w"], max(w["s"], first + 0.15 * (j + 1))] for j, w in enumerate(ln[1:])]
        draft.append(row)
    (job / "words.json").write_text(json.dumps(words, ensure_ascii=False, indent=1), encoding="utf-8")
    (job / "lines.draft.json").write_text(json.dumps(draft, ensure_ascii=False, indent=1), encoding="utf-8")
    for row in draft:
        print(f"{row[0][1]:6.2f}  " + " ".join(w for w, _ in row))
    print("→ fix spelling / split, then paste into project.json \"lines\" (words.json keeps the raw timings)")


def cmd_init(a):
    job = Path(a.job); job.mkdir(parents=True, exist_ok=True)
    dst = job / "project.json"
    if dst.exists() and not a.force:
        raise SystemExit(f"{dst} exists (use --force)")
    shutil.copy(PKG / "project.example.json", dst)
    print(f"→ {dst}  (edit title, date_line, subtitle, lines, shots)")


def cmd_prep(a):
    """Licensed clips → 1080×1920 30 fps mezzanine. SRC[:X] where X is the crop's left edge in source pixels."""
    job = Path(a.job); (job / "v").mkdir(parents=True, exist_ok=True)
    for i, spec in enumerate(a.clips):
        src, x = spec, ""
        if ":" in spec and spec.rsplit(":", 1)[1].isdigit():
            src, x = spec.rsplit(":", 1)
        xexpr = x if x else "(iw-ow)/2"
        out = job / "v" / f"{i:02d}.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-i", src, "-t", str(a.seconds), "-an", "-vf",
             f"crop='min(iw,ih*9/16)':ih:{xexpr}:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.7:5:5:0,fps=30",
             "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-g", "15", str(out)])
        print(f"{src} → {out}")


def cmd_sprites(a):
    job = Path(a.job)
    p = load_project(job)
    spec = job / "sprite_spec.json"
    spec.write_text(json.dumps(sprite_spec(p), ensure_ascii=False), encoding="utf-8")
    run(["node", str(PKG / "sprites.cjs"), str(spec), str(job / "sprites")])


def cmd_stills(a):
    import cv2
    job = Path(a.job)
    eng = Engine(job, load_project(job))
    (job / "stills").mkdir(exist_ok=True)
    for t in (float(x) for x in a.t.split(",")):
        out = job / "stills" / f"t{t:05.2f}.jpg"
        cv2.imwrite(str(out), eng.frame(min(int(round(t * eng.FPS)), eng.N - 1)), [cv2.IMWRITE_JPEG_QUALITY, 88])
        print(out)


def cmd_render_chunk(a):
    job = Path(a.job)
    eng = Engine(job, load_project(job))
    s, e = (int(x) for x in a.range.split(":"))
    proc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(eng.FPS),
                             "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", a.out], stdin=subprocess.PIPE)
    for n in range(s, min(e, eng.N)):
        proc.stdin.write(eng.frame(n).tobytes())
    proc.stdin.close(); proc.wait()


def cmd_render(a):
    import os
    job = Path(a.job)
    p = load_project(job)
    n = int(round(p["duration"] * p["fps"]))
    out = job / "out"; out.mkdir(exist_ok=True)
    k = max(1, a.workers)
    bounds = [round(n * i / k) for i in range(k + 1)]
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1")
    procs, parts = [], []
    for i in range(k):
        part = out / f"part_{i}.mp4"; parts.append(part)
        procs.append(subprocess.Popen([sys.executable, __file__, "_chunk", "--job", str(job), "--range", f"{bounds[i]}:{bounds[i + 1]}",
                                       "--out", str(part)], env=env, stderr=subprocess.DEVNULL))
    if any(pr.wait() for pr in procs):
        raise SystemExit("a render chunk failed (run stills to debug)")
    lst = out / "parts.txt"
    lst.write_text("".join(f"file '{x.name}'\n" for x in parts))
    master, tiktok = out / "master.mp4", out / "tiktok.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", p["audio"], "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", str(master)])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(master), "-map", "0", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
         "-maxrate", "14M", "-bufsize", "28M", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(tiktok)])
    for x in parts + [lst]:
        x.unlink()
    def apkt(f):
        return subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-map", "0:a", "-c", "copy", "-f", "data", "-"], capture_output=True).stdout
    same = apkt(p["audio"]) == apkt(tiktok)
    frames = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames",
                             "-of", "csv=p=0", str(master)], capture_output=True, text=True).stdout.strip()
    rep = {"master": str(master), "tiktok": str(tiktok), "frames": int(frames or 0), "expected_frames": n, "fps": p["fps"],
           "duration_s": p["duration"], "transitions": p["transitions"], "audio_untouched": same}
    (out / "report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(rep, ensure_ascii=False))
    if not same or rep["frames"] != n:
        raise SystemExit("verification failed (see out/report.json)")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor", help="what this machine can run")
    s = sub.add_parser("fetch", help="download a video (yt-dlp; TikTok fallback) and copy its audio to JOB/voice.m4a")
    s.add_argument("url"); s.add_argument("--job", required=True)
    s = sub.add_parser("caption-times", help="on-screen caption onsets of a reference reel")
    s.add_argument("video"); s.add_argument("--band", default="0.44:0.56", help="caption band as fractions of height")
    s = sub.add_parser("asr", help="faster-whisper word timings → words.json + lines.draft.json")
    s.add_argument("--job", required=True); s.add_argument("--model", default="medium")
    s.add_argument("--gap", type=float, default=0.45); s.add_argument("--max-words", type=int, default=5)
    s.add_argument("--rise-db", type=float, default=-20.0)
    s = sub.add_parser("init", help="copy the Wednesday example project.json into JOB")
    s.add_argument("--job", required=True); s.add_argument("--force", action="store_true")
    s = sub.add_parser("prep", help="licensed clips → JOB/v/NN.mp4 (1080×1920, 30 fps, sharpened)")
    s.add_argument("--job", required=True); s.add_argument("clips", nargs="+", help="SRC or SRC:X (crop left edge in px)")
    s.add_argument("--seconds", type=float, default=7.0)
    s = sub.add_parser("sprites", help="render text sprites in Chromium"); s.add_argument("--job", required=True)
    s = sub.add_parser("stills", help="render review frames to JOB/stills"); s.add_argument("--job", required=True)
    s.add_argument("--t", required=True, help="comma-separated seconds")
    s = sub.add_parser("render", help="parallel render + concat + untouched audio + TikTok copy + checks")
    s.add_argument("--job", required=True); s.add_argument("--workers", type=int, default=4)
    s = sub.add_parser("_chunk"); s.add_argument("--job"); s.add_argument("--range"); s.add_argument("--out")
    a = ap.parse_args(argv)
    {"doctor": cmd_doctor, "fetch": cmd_fetch, "caption-times": cmd_caption_times, "asr": cmd_asr, "init": cmd_init,
     "prep": cmd_prep, "sprites": cmd_sprites, "stills": cmd_stills, "render": cmd_render, "_chunk": cmd_render_chunk}[a.cmd](a)


if __name__ == "__main__":
    main()
