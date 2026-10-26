"""Overlay-text analysis of the reference.

1. bootstrap the text colour/polarity from persistent thin high-contrast strokes
2. per-frame masks (colour + top-hat + edge + 3-frame temporal stability + line grouping)
3. events = groups of stable plateaus (growing plateaus = word/typewriter reveals)
4. animation tracks around each event (visibility, displacement, scale, sharpness, per-word onsets)
   → entrance/exit kind + normalised curves that the builder replays
5. style at full resolution (fill, outline, shadow, glow, box, lines, alignment) + crops + OCR draft
"""
from __future__ import annotations

import os
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path

import numpy as np

import mm_color
import mm_img
from mm_common import ASSETS, f2t, log, rnd
from mm_video import FrameReader, fit_short_side, grab_frames_at

TEXT_SHORT = 540
CURVE_N = 21


def _odd(x):
    x = int(round(x))
    return x if x % 2 else x + 1


# ----------------------------------------------------------------------------- colour bootstrap

def bootstrap_color(frames: list[np.ndarray], k: int):
    h, w = frames[0].shape[:2]
    pers = {"light": np.zeros((h, w), np.float32), "dark": np.zeros((h, w), np.float32)}
    cands = {"light": [], "dark": []}
    for fr in frames:
        g = mm_img.to_gray(fr)
        edge = mm_img.dilate(mm_img.sobel_mag(g) > 60, 2)
        for pol in ("light", "dark"):
            th = mm_img.tophat(g, k, dark=(pol == "dark"))
            m = (th > 30) & edge
            n, lab, st = mm_img.label(m)
            big = np.zeros(n, bool)
            big[1:] = st[1:, 4] > 0.015 * h * w
            m &= ~big[lab]
            pers[pol] += m
            cands[pol].append(m)
    best = None
    for pol in ("light", "dark"):
        P = pers[pol]
        thr = max(3.0, 0.08 * len(frames))
        sel = P >= thr
        if sel.sum() < 40:
            continue
        cols = []
        wts = []
        for fr, m in zip(frames, cands[pol]):
            mm = m & sel
            if mm.any():
                cols.append(fr[mm])
                wts.append(P[mm])
        if not cols:
            continue
        cols = np.concatenate(cols).astype(np.float32)
        wts = np.concatenate(wts)
        if len(cols) > 40000:
            idx = np.random.default_rng(1).choice(len(cols), 40000, replace=False)
            cols, wts = cols[idx], wts[idx]
        lab = mm_color.rgb_to_lab(cols / 255.0)
        # weighted k-means (k=4)
        rng = np.random.default_rng(2)
        kk = min(4, len(lab))
        cent = lab[rng.choice(len(lab), kk, replace=False)]
        for _ in range(15):
            a = ((lab[:, None] - cent[None]) ** 2).sum(-1).argmin(1)
            for j in range(kk):
                s = a == j
                if s.any():
                    cent[j] = (lab[s] * wts[s, None]).sum(0) / wts[s].sum()
        a = ((lab[:, None] - cent[None]) ** 2).sum(-1).argmin(1)
        for j in range(kk):
            s = a == j
            if s.sum() < 20:
                continue
            spread = float(np.sqrt(((lab[s] - cent[j]) ** 2).sum(-1)).mean())
            weight = float(wts[s].sum())
            score = weight / (1.0 + spread / 6.0)
            rgb = np.median(cols[s], 0)
            cand = (score, pol, rgb, spread, weight)
            if best is None or cand[0] > best[0]:
                best = cand
    if best is None:
        return np.array([250, 250, 250], np.float32), "light", 0.0, 12.0
    total = sum(p.sum() for p in pers.values()) + 1
    return best[2].astype(np.float32), best[1], float(min(1.0, best[4] / total * 2)), best[3]


# ----------------------------------------------------------------------------- masks

class MaskMaker:
    def __init__(self, color, polarity, k, spread, size):
        self.color = np.asarray(color, np.float32)
        self.pol = polarity
        self.k = k
        self.col_thr = float(np.clip(spread * 2.2 + 30, 34, 75))
        self.w, self.h = size

    def candidate(self, fr: np.ndarray) -> np.ndarray:
        g = mm_img.to_gray(fr)
        th = mm_img.tophat(g, self.k, dark=(self.pol == "dark"))
        d = np.sqrt(((fr.astype(np.float32) - self.color) ** 2).sum(-1))
        edge = mm_img.dilate(mm_img.sobel_mag(g) > 45, 2)
        c = (((th > 20) & (d < self.col_thr)) | ((d < self.col_thr * 0.55) & (th > 8))) & edge
        n, lab, st = mm_img.label(c)
        if n > 1:
            keep = np.ones(n, bool)
            keep[0] = False
            keep[1:] = (st[1:, 4] >= 3) & (st[1:, 4] <= 0.015 * self.w * self.h)
            c = keep[lab]
        return c

    def group(self, m: np.ndarray) -> np.ndarray:
        """Keep pixels that belong to text-line-like groups."""
        if not m.any():
            return m
        kw = max(5, int(0.035 * self.w))
        G = mm_img.dilate(m, kw=kw, kh=max(3, int(0.006 * self.h)))
        n, lab, st = mm_img.label(G)
        keep = np.zeros(n, bool)
        for i in range(1, n):
            x, y, w, h, area = st[i]
            if h < 0.008 * self.h or h > 0.25 * self.h:
                continue
            sub = m[y:y + h, x:x + w] & (lab[y:y + h, x:x + w] == i)
            cnt = int(sub.sum())
            dens = cnt / max(1, w * h)
            if cnt < 25 or dens < 0.03 or dens > 0.8:
                continue
            if w < 0.6 * h:  # tall thin things are rarely captions
                continue
            keep[i] = True
        return m & keep[lab]


def _iou(a, b):
    inter = np.logical_and(a, b).sum()
    uni = np.logical_or(a, b).sum()
    return inter / uni if uni else 0.0


def _half(m):
    h, w = m.shape
    return m[: h // 2 * 2, : w // 2 * 2].reshape(h // 2, 2, w // 2, 2).any(axis=(1, 3))


# ----------------------------------------------------------------------------- main

def analyze_text(ref, fps: Fraction, W: int, H: int, N: int, P: dict, feats: dict, text_color: str | None = None) -> dict:
    tw, th = fit_short_side(W, H, TEXT_SHORT)
    k = _odd(max(15, th * 0.022))
    sample = np.linspace(0, N - 1, num=min(72, N)).round().astype(int)
    sframes = grab_frames_at(ref, list(sample), fps, size=(tw, th))
    if text_color:
        color = np.array(mm_color.rgb_of(text_color), np.float32)
        pol = "light" if color.mean() > 110 else "dark"
        conf, spread = 1.0, 8.0
    else:
        color, pol, conf, spread = bootstrap_color([sframes[i] for i in sample], k)
    log(f"text colour ≈ {mm_color.hex_of(color)} ({pol}, confidence {conf:.2f})")
    mk = MaskMaker(color, pol, k, spread, (tw, th))

    # pass 1: candidates with a 3-frame temporal AND
    halves = []
    reader = FrameReader(ref, size=(tw, th), fps=fps)
    buf = []
    for fr in reader:
        buf.append(mk.candidate(fr))
        if len(buf) == 3:
            m = buf[1] & mm_img.dilate(buf[0], 1) & mm_img.dilate(buf[2], 1)
            halves.append(_half(mk.group(m)))
            buf.pop(0)
        elif len(buf) == 2 and not halves:
            halves.append(_half(mk.group(buf[0] & mm_img.dilate(buf[1], 1))))
    reader.close()
    if buf:
        halves.append(_half(mk.group(buf[-1] & mm_img.dilate(buf[-2], 1) if len(buf) > 1 else buf[-1])))
    while len(halves) < N:
        halves.append(np.zeros_like(halves[0]))
    M = np.stack(halves[:N])
    events = segment_events(M, fps)
    log(f"text events: {len(events)}")

    # core frames (analysis res) → templates
    core_idx = [e["core_frame"] for e in events]
    cores = grab_frames_at(ref, core_idx, fps, size=(tw, th)) if core_idx else {}
    tmpl = []
    for e in events:
        tmpl.append(make_template(cores[e["core_frame"]], e, M, mk, tw, th))
    # pass 2: tracks
    windows = []
    for e, T in zip(events, tmpl):
        a0 = max(0, e["first"] - int(1.5 * float(fps)))
        a1 = min(N - 1, max(e["core_start"] + int(0.8 * float(fps)), e["first"] + 3))
        b0 = max(0, min(e["core_end"] - int(0.8 * float(fps)), e["last"] - 3))
        b1 = min(N - 1, e["last"] + int(1.5 * float(fps)))
        if b0 <= a1:  # short event: one continuous window
            b0 = a1 + 1
        windows.append((a0, a1, b0, b1))
    tracks = [dict() for _ in events]
    if events:
        need = np.zeros(N, bool)
        for (a0, a1, b0, b1) in windows:
            need[a0:a1 + 1] = True
            need[b0:b1 + 1] = True
        reader = FrameReader(ref, size=(tw, th), fps=fps)
        for n, fr in enumerate(reader):
            if not need[n]:
                continue
            g = mm_img.to_gray(fr)
            for ei, ((a0, a1, b0, b1), T) in enumerate(zip(windows, tmpl)):
                if a0 <= n <= a1 or b0 <= n <= b1:
                    tracks[ei][n] = measure(g, T)
        reader.close()
    out_events = []
    for i, (e, T, tr) in enumerate(zip(events, tmpl, tracks)):
        ev = finish_event(i + 1, e, T, tr, windows[i], fps, tw, th, W, H)
        out_events.append(ev)
    # style at full res + crops + OCR
    full = grab_frames_at(ref, [e["core_frame"] for e in events], fps) if events else {}
    for ev, e, T in zip(out_events, events, tmpl):
        style_and_crops(ev, full[e["core_frame"]], T, tw, th, W, H, P, color)
    # small masks for the shot analysis (exclude text pixels from distances)
    sw, sh = feats["sw"], feats["sh"]
    small = np.zeros((N, sh, sw), bool)
    for n in range(N):
        if M[n].any():
            small[n] = mm_img.resize(M[n].astype(np.uint8) * 255, (sw, sh), "area") > 0
    small = np.stack([mm_img.dilate(s, 1) if s.any() else s for s in small])
    glob = global_style(out_events, color, pol)
    return {"events": out_events, "small_masks": small, "half_masks": M, "global": glob,
            "analysis_size": [tw, th]}


def segment_events(M: np.ndarray, fps) -> list[dict]:
    N = len(M)
    area = M.reshape(N, -1).sum(1)
    amin = max(25, int(0.00025 * M.shape[1] * M.shape[2]))
    present = area >= amin
    runs = []
    cur = None
    for t in range(N):
        if not present[t]:
            if cur:
                runs.append(cur)
            cur = None
            continue
        if cur is None:
            cur = [t, t]
            continue
        a, b = mm_img.dilate(M[t], 1), mm_img.dilate(M[t - 1], 1)
        ratio = area[t] / max(1, area[t - 1])
        if _iou(a, b) >= 0.6 and 0.93 <= ratio <= 1.07:
            cur[1] = t
        else:
            runs.append(cur)
            cur = [t, t]
    if cur:
        runs.append(cur)
    plats = []
    for s, e in runs:
        if e - s + 1 < 3:
            continue
        rep = M[s:e + 1].mean(0) > 0.5
        if rep.sum() < amin:
            continue
        plats.append({"s": s, "e": e, "mask": rep, "area": int(rep.sum())})
    events = []
    for p in plats:
        if events:
            last = events[-1]["plats"][-1]
            gap = p["s"] - last["e"]
            dl, dp = mm_img.dilate(last["mask"], 2), mm_img.dilate(p["mask"], 2)
            c_lp = np.logical_and(last["mask"], dp).sum() / max(1, last["area"])
            c_pl = np.logical_and(p["mask"], dl).sum() / max(1, p["area"])
            same = c_lp > 0.9 and c_pl > 0.9 and gap < 0.6 * float(fps)
            grow = c_lp > 0.85 and p["area"] > 1.05 * last["area"] and gap < 1.0 * float(fps)
            shrink = c_pl > 0.85 and last["area"] > 1.05 * p["area"] and gap < 1.0 * float(fps)
            if same or grow or shrink:
                events[-1]["plats"].append(p)
                continue
        events.append({"plats": [p]})
    out = []
    for ev in events:
        ps = ev["plats"]
        ci = int(np.argmax([q["area"] * (1 + 0.02 * (q["e"] - q["s"])) for q in ps]))
        core = ps[ci]
        union = np.zeros_like(core["mask"])
        for q in ps:
            union |= q["mask"]
        out.append({"plats": ps, "core_i": ci, "core_start": core["s"], "core_end": core["e"],
                    "core_frame": (core["s"] + core["e"]) // 2, "first": ps[0]["s"], "last": ps[-1]["e"],
                    "core_mask_half": core["mask"], "union_half": union,
                    "steps": [{"frame": q["s"], "area": q["area"]} for q in ps[:ci]],
                    "exit_steps": [{"frame": q["s"], "area": q["area"]} for q in ps[ci + 1:]]})
    return out


def make_template(fr: np.ndarray, e: dict, M, mk: MaskMaker, tw, th) -> dict:
    up = mm_img.resize(e["core_mask_half"].astype(np.uint8) * 255, (tw, th), "nearest") > 0
    region = mm_img.dilate(up, 3)
    C = mk.candidate(fr) & region
    if C.sum() < 20:
        C = up
    ys, xs = np.nonzero(C)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    lh = _line_height(C[y0:y1, x0:x1])
    mg = int(max(10, 0.8 * lh))
    zx0, zy0 = max(0, x0 - mg), max(0, y0 - mg)
    zx1, zy1 = min(tw, x1 + mg), min(th, y1 + mg)
    g = mm_img.to_gray(fr)
    r_in = max(5, int(round(0.12 * lh)))     # outside typical outline/shadow
    r_out = r_in + max(4, int(round(0.1 * lh)))
    ring = mm_img.dilate(C, r_out) & ~mm_img.dilate(C, r_in)
    Ce = mm_img.erode(C, 1)
    if Ce.sum() < 0.25 * C.sum():
        Ce = C
    F = float(np.median(g[Ce]))                # fill luminance of the settled text
    Rc = float(np.median(g[ring])) if ring.any() else float(g.mean())
    # 'energy' zone: the text dilated enough to hold a blurred version of it, with its own far ring
    Z = mm_img.dilate(C, max(6, int(round(0.55 * lh))))
    ring_far = mm_img.dilate(C, max(9, int(round(0.8 * lh)))) & ~mm_img.dilate(C, max(7, int(round(0.62 * lh))))
    zyx = np.nonzero(Z)
    fyx = np.nonzero(ring_far)
    Rf = float(np.median(g[ring_far])) if ring_far.any() else Rc
    E0 = float(np.sum(g[Z] - Rf))
    sob = mm_img.sobel_mag(g)
    edge_px = mm_img.dilate(C, 1) & ~mm_img.erode(C, 1)
    sharp_c = float(sob[edge_px].mean()) / max(8.0, abs(F - Rc))
    sm = int(max(lh * 2.0, 0.08 * th))
    S = (max(0, zx0 - sm), max(0, zy0 - sm), min(tw, zx1 + sm), min(th, zy1 + sm))
    E = sob[zy0:zy1, zx0:zx1].astype(np.float32)
    words = word_columns(C, x0, x1, y0, y1, lh)
    cx, cy = (zx0 + zx1) / 2.0, (zy0 + zy1) / 2.0
    cyx = np.nonzero(Ce)
    ryx = np.nonzero(ring)
    eyx = np.nonzero(edge_px)
    wpix = []
    for wd in words:
        sel = (cyx[1] >= wd["x0"]) & (cyx[1] < wd["x1"]) & (cyx[0] >= wd["y0"]) & (cyx[0] < wd["y1"])
        wpix.append(sel)
    return {"C": C, "ring": ring, "F": F, "Rc": Rc, "zone": (zx0, zy0, zx1, zy1), "search": S, "E": E,
            "sharp": max(1e-3, sharp_c), "bbox": (x0, y0, x1, y1), "lh": lh, "words": words, "center": (cx, cy),
            "cpix": (cyx[0].astype(np.float32), cyx[1].astype(np.float32)),
            "rpix": (ryx[0].astype(np.float32), ryx[1].astype(np.float32)),
            "epix": (eyx[0].astype(np.float32), eyx[1].astype(np.float32)), "wsel": wpix, "pol": mk.pol,
            "zpix": (zyx[0].astype(np.float32), zyx[1].astype(np.float32)), "E0": E0 if abs(E0) > 1 else 1.0,
            "fpix": (fyx[0].astype(np.float32), fyx[1].astype(np.float32))}


def _line_height(sub: np.ndarray) -> float:
    """Typical ink height of one text line (dots and harakat merged into their line)."""
    lines = split_lines(sub)
    if not lines:
        return float(sub.shape[0])
    return float(np.median([b - a for a, b in lines]))


def split_lines(mask: np.ndarray, min_gap_ratio: float = 0.35) -> list[tuple[int, int]]:
    """Row ranges of text lines in a mask (merging gaps from dots/diacritics)."""
    prof = mask.sum(1)
    on = prof > max(1, 0.01 * prof.max())
    segs = []
    s = None
    for i, v in enumerate(on):
        if v and s is None:
            s = i
        if not v and s is not None:
            segs.append([s, i])
            s = None
    if s is not None:
        segs.append([s, len(on)])
    if not segs:
        return []
    # merge small segments (dots, harakat) into neighbours
    hts = sorted(b - a for a, b in segs)
    big = hts[-1]
    changed = True
    while changed and len(segs) > 1:
        changed = False
        for i in range(len(segs)):
            a, b = segs[i]
            if b - a < 0.45 * big:
                # merge with the nearer neighbour
                dprev = a - segs[i - 1][1] if i > 0 else 1e9
                dnext = segs[i + 1][0] - b if i + 1 < len(segs) else 1e9
                j = i - 1 if dprev <= dnext else i + 1
                lo, hi = min(segs[i][0], segs[j][0]), max(segs[i][1], segs[j][1])
                segs[min(i, j)] = [lo, hi]
                del segs[max(i, j)]
                changed = True
                break
    # merge lines separated by very small gaps
    out = [segs[0]]
    for a, b in segs[1:]:
        if a - out[-1][1] < min_gap_ratio * 0.2 * (b - a):
            out[-1][1] = b
        else:
            out.append([a, b])
    return [tuple(x) for x in out]


def word_columns(C, x0, x1, y0, y1, lh) -> list[dict]:
    """Word spans per line (RTL reading order: right→left, top line first)."""
    sub = C[y0:y1, x0:x1]
    words = []
    for (ra, rb) in split_lines(sub):
        line = sub[ra:rb]
        col = line.sum(0) > 0
        gap_min = max(3, int(0.22 * (rb - ra)))
        spans = []
        s = None
        gap = 0
        for i, v in enumerate(col):
            if v:
                if s is None:
                    s = i
                gap = 0
                e = i
            else:
                if s is not None:
                    gap += 1
                    if gap >= gap_min:
                        spans.append((s, e + 1))
                        s = None
                        gap = 0
        if s is not None:
            spans.append((s, e + 1))
        for (a, b) in sorted(spans, key=lambda ab: -ab[0]):  # right → left
            words.append({"x0": x0 + a, "x1": x0 + b, "y0": y0 + ra, "y1": y0 + rb})
    return words


SCALES = (0.5, 0.6, 0.7, 0.8, 0.88, 0.94, 1.0, 1.06, 1.12, 1.2, 1.32, 1.5)


def _sample(img, ys, xs, T, dx, dy, s):
    cx, cy = T["center"]
    X = np.rint(cx + s * (xs - cx) + dx).astype(np.int64)
    Y = np.rint(cy + s * (ys - cy) + dy).astype(np.int64)
    ok = (X >= 0) & (X < img.shape[1]) & (Y >= 0) & (Y < img.shape[0])
    out = np.full(len(xs), np.nan, np.float32)
    out[ok] = img[Y[ok], X[ok]]
    return out


def _alpha_at(g, sob, T, dx, dy, s):
    """Alpha of the text layer at a pose: per-pixel (L-R)/(F-R) with R the ring background."""
    ring = _sample(g, *T["rpix"], T, dx, dy, s)
    R = float(np.nanmedian(ring)) if np.isfinite(ring).any() else float(g.mean())
    den = T["F"] - R
    if abs(den) < 12:
        return None, None, None, R, None
    vals = (_sample(g, *T["cpix"], T, dx, dy, s) - R) / den
    alpha = float(np.clip(np.nanmedian(vals), -0.5, 1.5))
    words = []
    for sel in T["wsel"]:
        v = vals[sel]
        words.append(float(np.clip(np.nanmedian(v), -0.5, 1.5)) if np.isfinite(v).any() else alpha)
    edge = _sample(sob, *T["epix"], T, dx, dy, s)
    sharp = float(np.nanmean(edge)) / abs(den) / T["sharp"] if np.isfinite(edge).any() else 0.0
    zv = _sample(g, *T["zpix"], T, dx, dy, s)
    fr_ = _sample(g, *T["fpix"], T, dx, dy, s)
    Rf = float(np.nanmedian(fr_)) if np.isfinite(fr_).any() else R
    # integrated light over the zone (blur-invariant); finish_event turns it into a relative alpha
    # by differencing against text-free and settled frames on the same background
    energy = float(np.nansum(zv - Rf)) / abs(T["E0"])
    return alpha, words, sharp, R, energy


def _match_pose(sob, T):
    if not mm_img.HAVE_CV2:
        return 0.0, 0.0, 0.0, 1.0
    cv2 = mm_img.cv2
    sx0, sy0, sx1, sy1 = T["search"]
    area = sob[sy0:sy1, sx0:sx1].astype(np.float32)
    zx0, zy0, zx1, zy1 = T["zone"]
    E = T["E"]
    res = []
    for s in SCALES:
        tw_, th_ = int(round(E.shape[1] * s)), int(round(E.shape[0] * s))
        if tw_ < 8 or th_ < 8 or tw_ >= area.shape[1] or th_ >= area.shape[0]:
            continue
        Es = cv2.resize(E, (tw_, th_), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_LINEAR)
        r = cv2.matchTemplate(area, Es, cv2.TM_CCOEFF_NORMED)
        _, mv, _, ml = cv2.minMaxLoc(r)
        cx = sx0 + ml[0] + tw_ / 2 - (zx0 + zx1) / 2
        cy = sy0 + ml[1] + th_ / 2 - (zy0 + zy1) / 2
        res.append((float(mv), float(cx), float(cy), s))
    if not res:
        return 0.0, 0.0, 0.0, 1.0
    res.sort(key=lambda r: -r[0])
    mv, cx, cy, s = res[0]
    # parabolic refinement of the scale from the neighbours in the grid
    i = SCALES.index(s)
    nb = {r[3]: r[0] for r in res}
    if 0 < i < len(SCALES) - 1 and SCALES[i - 1] in nb and SCALES[i + 1] in nb:
        y0, y1, y2 = nb[SCALES[i - 1]], mv, nb[SCALES[i + 1]]
        den = (y0 - 2 * y1 + y2)
        if abs(den) > 1e-6:
            off = 0.5 * (y0 - y2) / den
            off = max(-0.5, min(0.5, off))
            step = (SCALES[i + 1] - SCALES[i - 1]) / 2
            s = s + off * step
    return mv, cx, cy, s


def measure(g: np.ndarray, T: dict) -> dict:
    sob = mm_img.sobel_mag(g)
    a, w, sh, R, en = _alpha_at(g, sob, T, 0.0, 0.0, 1.0)
    rest_ok = a is not None and a >= 0.9 and sh is not None and sh >= 0.75
    res = {"vis": a if a is not None else 0.0, "words": w if w is not None else [0.0] * len(T["words"]),
           "sharp": sh if sh is not None else 0.0, "dx": 0.0, "dy": 0.0, "scale": 1.0, "match": 1.0 if rest_ok else 0.0,
           "bg": R, "valid": a is not None, "energy": en if en is not None else 0.0}
    if rest_ok:
        return res
    mv, dx, dy, s = _match_pose(sob, T)
    res["match"] = mv
    moved = abs(dx) > 1.0 or abs(dy) > 1.0 or abs(s - 1) > 0.015
    if mv >= 0.5 and moved:
        a2, w2, sh2, _, en2 = _alpha_at(g, sob, T, dx, dy, s)
        if a2 is not None:
            res.update(vis=a2, words=w2, sharp=sh2, dx=dx, dy=dy, scale=s, energy=en2)
    return res


def _resample(values, n=CURVE_N):
    if len(values) == 0:
        return [1.0] * n
    if len(values) == 1:
        return [float(values[0])] * n
    x = np.linspace(0, 1, len(values))
    return [rnd(v, 3) for v in np.interp(np.linspace(0, 1, n), x, values)]


def _settled(m):
    if m is None or not m.get("valid", True):
        return False
    words_ok = (not m["words"]) or min(m["words"]) >= 0.85
    # sharpness is only loosely bounded: a shadow reads stronger on bright backgrounds than on dark ones
    return (m["vis"] >= 0.95 and abs(m["dx"]) <= 0.75 and abs(m["dy"]) <= 0.75 and abs(m["scale"] - 1) <= 0.02
            and m["sharp"] >= 0.6 and words_ok)


def _visible(m):
    if m is None:
        return False
    if m.get("valid", True) and m["vis"] > 0.12:
        return True
    moved = abs(m["dx"]) > 1 or abs(m["dy"]) > 1 or abs(m["scale"] - 1) > 0.015
    return m["match"] >= 0.5 and moved and m["vis"] > 0.03


def _ramp_zero(frames: list[int], vals: list[float], rising: bool, min_r2: float = 0.0) -> float | None:
    """Fit the 15–85 % part of the ramp that touches the settled end and extrapolate it to 0
    (sub-frame start of an entrance / end of an exit)."""
    seq = list(zip(frames, vals))
    if not rising:
        seq = seq[::-1]  # walk from the hidden end towards the settled end in both cases
    # keep only the contiguous ramp: from the last 'empty' sample (<0.08) before the settled end
    last_empty = -1
    for i, (_, v) in enumerate(seq):
        if v < 0.08:
            last_empty = i
    seq = seq[last_empty + 1:] if last_empty + 1 < len(seq) else seq
    pts = [(f, v) for f, v in seq if 0.15 <= v <= 0.85]
    if len(pts) < 3:
        return None
    x = np.array([p[0] for p in pts], np.float64)
    y = np.array([p[1] for p in pts], np.float64)
    a, b = np.polyfit(x, y, 1)
    if (rising and a <= 0.01) or ((not rising) and a >= -0.01):
        return None
    if min_r2 > 0:
        pred = a * x + b
        ss = float(((y - y.mean()) ** 2).sum()) + 1e-9
        if 1 - float(((y - pred) ** 2).sum()) / ss < min_r2:
            return None
    return float(-b / a)


def _rel_energy(tr, empty_frames, full_frames):
    """Map raw zone energy to 0..1 using the text-free stretch (lowest energies next to the event)
    and the settled frames. Returns None when the text adds too little energy to be measured
    reliably against the background's own variation (low contrast)."""
    e0 = np.array([tr[k]["energy"] for k in empty_frames if k in tr])
    e1 = [tr[k]["energy"] for k in full_frames if k in tr]
    if len(e0) < 4 or not e1:
        return None
    q = np.sort(e0)[: max(4, len(e0) // 3)]
    lo, hi = float(np.median(q)), float(np.median(e1))
    noise = float(np.std(q)) + 0.01
    if hi - lo < 0.05 or (hi - lo) / noise < 6.0:
        return None
    return lambda m: float(np.clip((m["energy"] - lo) / (hi - lo), -0.2, 1.3))


def finish_event(eid, e, T, tr, win, fps, tw, th, W, H) -> dict:
    a0, a1, b0, b1 = win
    sc = W / tw
    fps_f = float(fps)

    def S(n):
        return _settled(tr[n]) if n in tr else (a1 < n < b0)  # frames between windows: assumed settled

    # full_in: first frame of 3 consecutive settled frames
    full_in = None
    for n in range(a0, b1 + 1):
        if S(n) and S(n + 1) and S(n + 2):
            full_in = n
            break
    if full_in is None:
        full_in = e["core_start"]
    # full_out (exclusive): after the last frame of 3 consecutive settled frames
    full_out = None
    for n in range(b1, full_in, -1):
        if S(n) and S(n - 1) and S(n - 2):
            full_out = n + 1
            break
    if full_out is None or full_out <= full_in:
        full_out = e["core_end"] + 1
    n = full_in - 1
    while n >= a0 and n in tr and _visible(tr[n]):
        n -= 1
    in_start = n + 1
    n = full_out
    while n <= b1 and n in tr and _visible(tr[n]):
        n += 1
    out_end = n
    # sub-frame refinement from the alpha ramp (handles faint first/last frames of a fade)
    fr_in = [k for k in range(max(a0, in_start - 3), full_in) if k in tr]
    z = _ramp_zero(fr_in, [tr[k]["vis"] for k in fr_in], rising=True)
    if z is not None and in_start - 4 <= z <= full_in:
        in_start = int(np.clip(int(np.floor(z + 0.5)), a0, full_in))
    fr_out = [k for k in range(full_out, min(b1, out_end + 3) + 1) if k in tr]
    z = _ramp_zero(fr_out, [tr[k]["vis"] for k in fr_out], rising=False)
    if z is not None and full_out <= z <= out_end + 4:
        out_end = int(np.clip(int(np.floor(z + 0.5)), full_out + 1, b1 + 1))
    # curves include both ends: entrance [in_start … full_in], exit [full_out-1 … out_end]
    anim_in = classify_anim([tr.get(k) for k in range(in_start, full_in + 1)], T, e, "in", in_start, sc)
    anim_out = classify_anim([tr.get(k) for k in range(full_out - 1, out_end + 1)][::-1], T, e, "out", full_out, sc)
    # a blurred text spreads its light, so its median alpha lags: time blur ramps on integrated energy
    if anim_in["type"] == "blur":
        rel = _rel_energy(tr, list(range(max(a0, in_start - 25), in_start)), list(range(full_in, full_in + 3)))
        if rel:
            fr = [k for k in range(a0, full_in + 1) if k in tr]
            z = _ramp_zero(fr, [rel(tr[k]) for k in fr], rising=True, min_r2=0.93)
            if z is not None and a0 <= z < full_in:
                in_start = int(np.floor(z + 0.5))
                anim_in = classify_anim([tr.get(k) for k in range(in_start, full_in + 1)], T, e, "in", in_start, sc, rel)
                anim_in["type"] = "blur"
    if anim_out["type"] == "blur":
        rel = _rel_energy(tr, list(range(out_end, min(b1, out_end + 25) + 1)), list(range(full_out - 3, full_out)))
        if rel:
            fr = [k for k in range(full_out - 1, b1 + 1) if k in tr]
            z = _ramp_zero(fr, [rel(tr[k]) for k in fr], rising=False, min_r2=0.93)
            if z is not None and full_out < z <= b1 + 1:
                out_end = int(np.floor(z + 0.5))
                anim_out = classify_anim([tr.get(k) for k in range(full_out - 1, out_end + 1)][::-1], T, e, "out",
                                         full_out, sc, rel)
                anim_out["type"] = "blur"
    if anim_in["type"] == "words":
        anim_in["word_onsets"] = _word_onsets(tr, T, in_start, full_in, e, sc)
    if anim_out["type"] == "words":
        anim_out["word_offsets"] = _word_offsets(tr, T, full_out, out_end, sc)
    x0, y0, x1, y1 = T["bbox"]
    ev = {"id": eid,
          "time": {"in_start": int(in_start), "full_in": int(full_in), "full_out": int(full_out), "out_end": int(out_end),
                   "in_start_s": rnd(in_start / fps_f), "full_in_s": rnd(full_in / fps_f),
                   "full_out_s": rnd(full_out / fps_f), "out_end_s": rnd(out_end / fps_f)},
          "bbox": [rnd(x0 * sc, 1), rnd(y0 * sc, 1), rnd(x1 * sc, 1), rnd(y1 * sc, 1)],
          "anim_in": anim_in, "anim_out": anim_out,
          "words_detected": len(T["words"]),
          "lines": [], "style": {}, "font": {"candidates": [], "chosen": None}}
    return ev


def classify_anim(ms: list, T: dict, e: dict, direction: str, t0: int, sc: float, rel=None) -> dict:
    """ms is ordered from the HIDDEN end to the VISIBLE end for both directions.

    Returns the kind plus curves in forward time (entrance: hidden→visible, exit: visible→hidden),
    each resampled to CURVE_N points: alpha (0..1), dx/dy (source px, offset from the final place),
    scale (1 = final size) and sharp (edge energy relative to the settled text)."""
    ms = [m for m in ms if m is not None]
    n = len(ms)
    if n <= 2:  # only the two settled/hidden end points: an instant appearance
        return {"type": "cut", "frames": 0, "curves": {}, "detail": {}}
    vis = np.array([np.clip(m["vis"], 0, 1.2) for m in ms])
    dx = np.array([m["dx"] for m in ms])
    dy = np.array([m["dy"] for m in ms])
    scl = np.array([m["scale"] for m in ms])
    sh = np.array([np.clip(m["sharp"], 0, 1.5) for m in ms])
    match = np.array([m["match"] for m in ms])
    lh = T["lh"]
    good = match >= 0.5
    half = slice(0, max(1, (n + 1) // 2))  # the hidden half
    detail = {}
    gh = good[half]
    mvmax = max(np.abs(dy[half][gh]).max(initial=0), np.abs(dx[half][gh]).max(initial=0)) if gh.any() else 0.0
    moved = mvmax > max(2.5, 0.1 * lh)
    smax = np.abs(scl[half][gh] - 1).max(initial=0) if gh.any() else 0.0
    scaled = smax >= 0.06
    sequential = False
    if T["words"] and len(T["words"]) >= 2:
        wv = np.clip(np.array([m["words"] for m in ms]), 0, 1)
        mean = wv.mean(1)
        mid = (mean > 0.1) & (mean < 0.9)
        disp = float(wv[mid].std(1).max()) if mid.any() else 0.0
        detail["word_dispersion"] = round(disp, 3)
        sequential = disp > 0.3
    vs = vis[half]
    ratio = sh[half] / np.maximum(vs, 0.05)
    sel = vs > 0.25
    blur_ratio = float(np.median(ratio[sel])) if sel.any() else 1.0
    detail.update(move_px=round(float(mvmax * sc), 1), scale_dev=round(float(smax), 3), sharp_over_alpha=round(blur_ratio, 2))
    sign = -1.0 if direction == "in" else 1.0  # motion = displacement change in forward time
    if sequential:
        kind = "words"
    elif moved:
        cand = np.where(good[half], np.abs(dy[half]) + np.abs(dx[half]), -1)
        i = int(np.argmax(cand))
        mx, my = sign * dx[i], sign * dy[i]
        if abs(my) >= abs(mx):
            kind = "slide_up" if my < 0 else "slide_down"
        else:
            kind = "slide_left" if mx < 0 else "slide_right"
    elif scaled:
        s_h = float(scl[half][gh][0])
        grows = (s_h < 1) if direction == "in" else (s_h > 1)
        overshoot = direction == "in" and s_h < 1 and (scl[good] > 1.03).any()
        kind = "pop" if overshoot else ("zoom_in" if grows else "zoom_out")
    elif blur_ratio < 0.6:
        kind = "blur"
    else:
        kind = "fade"
    fwd = slice(None) if direction == "in" else slice(None, None, -1)
    g_f = good[fwd]
    alpha_src = vis
    if kind == "blur" and rel is not None:
        alpha_src = np.array([np.clip(rel(m), 0, 1.0) for m in ms])
    curves = {"alpha": _resample(np.clip(alpha_src[fwd], 0, 1)),
              "dx": _resample(np.where(g_f, dx[fwd], 0.0) * sc),
              "dy": _resample(np.where(g_f, dy[fwd], 0.0) * sc),
              "scale": _resample(np.where(g_f, scl[fwd], 1.0)),
              "sharp": _resample(sh[fwd])}
    if kind in ("fade", "words"):
        curves["dx"] = [0.0] * CURVE_N
        curves["dy"] = [0.0] * CURVE_N
        curves["scale"] = [1.0] * CURVE_N
    if kind != "blur":
        curves["sharp"] = [1.0] * CURVE_N
    return {"type": kind, "frames": int(n - 2), "curves": curves, "detail": detail}


def _wbox(wd, sc):
    return [rnd(wd["x0"] * sc, 1), rnd(wd["y0"] * sc, 1), rnd(wd["x1"] * sc, 1), rnd(wd["y1"] * sc, 1)]


def _word_onsets(tr, T, a, b, e, sc=1.0):
    """Per detected word (reading order): first frame above 10 %, 50 % and 90 % alpha."""
    out = []
    for j in range(len(T["words"])):
        on = mid = full = None
        for n in range(a, b + 3):
            m = tr.get(n)
            if m is None or j >= len(m["words"]):
                continue
            v = m["words"][j]
            if on is None and v > 0.1:
                on = n
            if mid is None and v > 0.5:
                mid = n
            if v > 0.9:
                full = n
                break
        on = a if on is None else on
        mid = on if mid is None else mid
        full = max(mid, b) if full is None else full
        out.append({"word": j, "on": int(on), "mid": int(mid), "full": int(full), "box": _wbox(T["words"][j], sc)})
    return out


def _word_offsets(tr, T, a, b, sc=1.0):
    out = []
    for j in range(len(T["words"])):
        off = b
        for n in range(a, b + 1):
            m = tr.get(n)
            if m is not None and j < len(m["words"]) and m["words"][j] < 0.5:
                off = n
                break
        out.append({"word": j, "off": int(off), "box": _wbox(T["words"][j], sc)})
    return out


# ----------------------------------------------------------------------------- style + crops

def style_and_crops(ev: dict, fr_full: np.ndarray, T: dict, tw, th, W, H, P: dict, color):
    sc = W / tw
    zx0, zy0, zx1, zy1 = [int(round(v * sc)) for v in T["zone"]]
    zx1, zy1 = min(W, zx1), min(H, zy1)
    crop = fr_full[zy0:zy1, zx0:zx1].astype(np.float32)
    up = mm_img.resize(T["C"].astype(np.uint8) * 255, (W, H), "nearest")[zy0:zy1, zx0:zx1] > 0
    near = mm_img.dilate(up, max(2, int(sc * 1.5)))
    d = np.sqrt(((crop - np.asarray(color, np.float32)) ** 2).sum(-1))
    dv = d[near]
    thr = _otsu(dv) if dv.size > 50 else 60.0
    thr = float(np.clip(thr, 25, 110))
    mask = (d < thr) & near
    core = mm_img.erode(mask, 1) if mm_img.erode(mask, 1).sum() > 30 else mask
    fill = np.median(crop[core], 0) if core.any() else np.asarray(color)
    g = mm_img.to_gray(crop)
    bg_mask = ~mm_img.dilate(mask, max(3, int(sc * 3)))
    bg = float(np.median(g[bg_mask])) if bg_mask.any() else float(g.mean())
    # lines
    lines = []
    ys, xs = np.nonzero(mask)
    for (ra, rb) in split_lines(mask):
        rows = mask[ra:rb]
        cols = np.nonzero(rows.any(0))[0]
        if len(cols) == 0:
            continue
        lines.append({"bbox": [zx0 + int(cols.min()), zy0 + ra, zx0 + int(cols.max()) + 1, zy0 + rb],
                      "ink_h": int(rb - ra), "ink_w": int(cols.max() - cols.min() + 1), "text": "", "ocr": ""})
    # alignment
    align = "center"
    if len(lines) >= 2:
        cx = [(l["bbox"][0] + l["bbox"][2]) / 2 for l in lines]
        rx = [l["bbox"][2] for l in lines]
        lx = [l["bbox"][0] for l in lines]
        spread = {"center": np.std(cx), "right": np.std(rx), "left": np.std(lx)}
        align = min(spread, key=spread.get)
    elif lines:
        cxl = (lines[0]["bbox"][0] + lines[0]["bbox"][2]) / 2
        align = "center" if abs(cxl - W / 2) < 0.06 * W else ("right" if cxl > W / 2 else "left")
    ev["lines"] = lines
    ev["style"] = {"fill": mm_color.hex_of(fill), "align": align, "bg_luma": rnd(bg, 1)}
    ev["style"].update(_effects(crop, mask, g, bg, sc))
    # background-invariant glyph mask (alpha ≥ 50 % against the local background) for font matching:
    # a plain colour threshold makes strokes look bolder on light backgrounds and thinner on dark ones
    base = mm_img.inpaint(np.clip(crop, 0, 255).astype(np.uint8), mm_img.dilate(mask, max(4, int(7 * sc))), radius=5)
    bgL = mm_img.gaussian_blur(mm_img.to_gray(base), 2 * sc)
    Ff = float(np.median(g[core])) if core.any() else 255.0
    den = Ff - bgL
    with np.errstate(all="ignore"):
        alpha = np.where(np.abs(den) > 10, (g - bgL) / den, 0.0)
    mask50 = (alpha >= 0.5) & near
    if mask50.sum() < 0.5 * mask.sum():
        mask50 = mask
    # crops for review / OCR / font matching
    tdir = P["text"]
    tdir.mkdir(parents=True, exist_ok=True)
    zp = tdir / f"ev{ev['id']:02d}_zone.png"
    mm_img.save_png(zp, crop)
    mp = tdir / f"ev{ev['id']:02d}_mask.png"
    mm_img.save_png(mp, (~mask).astype(np.uint8) * 255)
    ev["crops"] = {"zone": str(zp.relative_to(P["root"])), "mask": str(mp.relative_to(P["root"])), "lines": [],
                   "zone_origin": [zx0, zy0]}
    for li, l in enumerate(lines, 1):
        x0, y0, x1, y1 = l["bbox"]
        pad = max(4, int(0.25 * l["ink_h"]))
        own = np.zeros_like(mask50)
        own[y0 - zy0:y1 - zy0, :] = mask50[y0 - zy0:y1 - zy0, :]   # only this line's rows
        sub = own[max(0, y0 - zy0 - pad):y1 - zy0 + pad, max(0, x0 - zx0 - pad):x1 - zx0 + pad]
        lp = tdir / f"ev{ev['id']:02d}_l{li}.png"
        mm_img.save_png(lp, (~sub).astype(np.uint8) * 255)
        ev["crops"]["lines"].append(str(lp.relative_to(P["root"])))
        l["ocr"] = ocr_line(lp)
    # full-res mask of the event (for previews / inpainting)
    np.savez_compressed(P["cache"] / f"ev{ev['id']:02d}_mask.npz", m=np.packbits(mask, axis=-1),
                        shape=np.array(mask.shape), origin=np.array([zx0, zy0]))


def _otsu(v: np.ndarray) -> float:
    v = v[np.isfinite(v)]
    hist, edges = np.histogram(v, bins=128)
    p = hist.astype(np.float64) / max(1, hist.sum())
    w0 = np.cumsum(p)
    mu = np.cumsum(p * edges[:-1])
    mt = mu[-1]
    with np.errstate(all="ignore"):
        s = (mt * w0 - mu) ** 2 / (w0 * (1 - w0))
    i = int(np.nanargmax(s))
    return float(edges[i + 1])


def _effects(crop, mask, g, bg, sc) -> dict:
    """Outline, shadow, glow and box estimates around the text mask (full-res zone)."""
    out = {"outline": None, "shadow": None, "glow": None, "box": None}
    if mask.sum() < 30:
        return out
    fillL = float(np.median(g[mask]))
    light = fillL > bg
    r1 = mm_img.dilate(mask, max(1, int(round(sc)))) & ~mask
    r2 = mm_img.dilate(mask, max(4, int(round(4 * sc)))) & ~mm_img.dilate(mask, max(2, int(round(2.5 * sc))))
    L1 = float(np.median(g[r1])) if r1.any() else bg
    L2 = float(np.median(g[r2])) if r2.any() else bg
    # outline: a tight ring clearly darker (light text) / lighter (dark text) than the wider ring
    if (light and L1 < L2 - 28) or ((not light) and L1 > L2 + 28):
        width = 1
        for rr in range(2, int(8 * sc) + 1):
            ring = mm_img.dilate(mask, rr) & ~mm_img.dilate(mask, rr - 1)
            if ring.any() and abs(float(np.median(g[ring])) - L1) < 18:
                width = rr
            else:
                break
        oc = np.median(crop[r1], 0)
        out["outline"] = {"color": mm_color.hex_of(oc), "width_px": int(width)}
    # shadow: correlation of the 'darker than local background' map with the shifted text mask
    base = mm_img.inpaint(np.clip(crop, 0, 255).astype(np.uint8), mm_img.dilate(mask, max(4, int(7 * sc))), radius=5)
    bgL = mm_img.gaussian_blur(mm_img.to_gray(base), 3 * sc)
    dark = np.clip(bgL - g, 0, None) * (~mask)
    bright = np.clip(g - bgL, 0, None) * (~mask)
    mf = mask.astype(np.float32)
    best = (0.0, 0, 0)
    R = int(max(3, 10 * sc))
    for dy in range(-R, R + 1, max(1, int(sc))):
        for dx in range(-R, R + 1, max(1, int(sc))):
            if dx == 0 and dy == 0:
                continue
            sh = np.roll(np.roll(mf, dy, 0), dx, 1)
            v = float((dark * sh).sum() / max(1.0, sh.sum()))
            if v > best[0]:
                best = (v, dx, dy)
    if best[0] > 3.0 and light:
        v, dx, dy = best
        out_px = ~mm_img.dilate(mask, 1)
        Y = dark[out_px]
        base_res = float((Y * Y).mean()) + 1e-6
        fit = None
        step = max(1, int(round(sc)))
        for ddx in (dx - step, dx, dx + step):
            for ddy in (dy - step, dy, dy + step):
                sh = np.roll(np.roll(mf, ddy, 0), ddx, 1)
                for sg in (0.0, 1.0, 2.0, 3.0, 4.5, 6.0, 8.0):
                    mb = mm_img.gaussian_blur(sh, sg * sc) if sg > 0 else sh
                    X = (bgL * mb)[out_px]
                    xx = float((X * X).sum())
                    if xx <= 0:
                        continue
                    op = float((X * Y).sum() / xx)
                    res = float(((Y - op * X) ** 2).mean())
                    if fit is None or res < fit[0]:
                        fit = (res, ddx, ddy, sg, op)
        if fit is not None and fit[0] < 0.8 * base_res and fit[4] > 0.03:
            res, ddx, ddy, sg, op = fit
            out["shadow"] = {"dx_px": int(ddx), "dy_px": int(ddy), "blur_px": rnd(sg * sc, 1),
                             "opacity": rnd(min(1.0, op), 2), "color": "#000000",
                             "fit": rnd(1 - res / base_res, 2)}
    # glow: bright halo around light text that is not part of the fill
    halo = mm_img.dilate(mask, max(3, int(4 * sc))) & ~mm_img.dilate(mask, max(1, int(sc)))
    if light and halo.any() and float(np.median(bright[halo])) > 12:
        out["glow"] = {"radius_px": int(6 * sc), "strength": rnd(float(np.median(bright[halo])) / 255, 2),
                       "color": mm_color.hex_of(np.median(crop[halo], 0))}
    # box: unusually flat background right around the text
    ring_bg = mm_img.dilate(mask, max(6, int(8 * sc))) & ~mm_img.dilate(mask, max(3, int(3 * sc)))
    if ring_bg.sum() > 100:
        cstd = float(crop[ring_bg].std(0).mean())
        if cstd < 4.0:
            out["box"] = {"color": mm_color.hex_of(np.median(crop[ring_bg], 0)), "opacity": 0.85, "note": "flat background behind text"}
    return out


def ocr_line(path: Path) -> str:
    exe = shutil.which("tesseract")
    if not exe:
        return ""
    tess = ASSETS / "tessdata"
    if not (tess / "ara.traineddata").exists():
        return ""
    try:
        from PIL import Image
        im = Image.open(path).convert("L")
        hgt = im.height
        if hgt < 90:
            f = 90 / max(1, hgt)
            im = im.resize((int(im.width * f), int(im.height * f)), Image.LANCZOS)
        pad = Image.new("L", (im.width + 40, im.height + 40), 255)
        pad.paste(im, (20, 20))
        tmp = path.with_name(path.stem + "_ocr.png")
        pad.save(tmp)
        env = dict(os.environ)
        r = subprocess.run([exe, str(tmp), "stdout", "-l", "ara", "--psm", "7", "--tessdata-dir", str(tess)],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60, env=env)
        tmp.unlink(missing_ok=True)
        return r.stdout.decode("utf-8", "replace").strip()
    except Exception:
        return ""


def global_style(events, color, pol) -> dict:
    fills = [e["style"].get("fill") for e in events if e.get("style")]
    return {"detected_color": mm_color.hex_of(color), "polarity": pol, "fills": fills}


def masks_at(text: dict, frame_idx: list[int], W: int, H: int) -> dict:
    """Full-res approximate text masks (from the half-res analysis) for given frames."""
    M = text.get("half_masks")
    out = {}
    if M is None:
        return out
    for i in frame_idx:
        if 0 <= i < len(M) and M[i].any():
            out[i] = mm_img.resize(M[i].astype(np.uint8) * 255, (W, H), "nearest") > 0
    return out
