"""Reference analysis → spec.json

  probe + audio copy → pass A (per-frame features) → text layer (mm_text) → shot boundaries →
  transition kind + progress curve by re-synthesis (mm_transitions) → per-shot look/motion/keyframes →
  global look (vignette, grain, letterbox, fades) → sheets for review.
"""
from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

import numpy as np

import mm_color
import mm_img
import mm_transitions as TR
from mm_common import Timer, ensure_dir, f2t, fps_str, log, probe, rnd, save_json, tc, work_paths
from mm_video import FrameReader, extract_audio, fit_short_side, grab_frames_at

SMALL_SHORT = 96      # shot/transition analysis resolution (short side)
MID_SHORT = 360       # sharpness / motion resolution


# ----------------------------------------------------------------------------- pass A

def pass_a(ref, fps: Fraction, W: int, H: int) -> dict:
    aw, ah = fit_short_side(W, H, MID_SHORT)
    sw, sh = fit_short_side(W, H, SMALL_SHORT)
    small, lum, lstd, sat, sharp, hist, motion = [], [], [], [], [], [], []
    acc = np.zeros((sh, sw), np.float64)
    noise = []
    prev = None
    prev_pts = None
    have_cv2 = mm_img.HAVE_CV2
    reader = FrameReader(ref, size=(aw, ah), fps=fps)
    n = 0
    for fr in reader:
        g = mm_img.to_gray(fr)
        sm = mm_img.resize(fr, (sw, sh), "area")
        small.append(sm)
        gs = sm.astype(np.float32).mean(-1)
        acc += gs
        lum.append(g.mean() / 255.0)
        lstd.append(g.std() / 255.0)
        mx = sm.max(-1).astype(np.float32)
        mn = sm.min(-1).astype(np.float32)
        sat.append(float(((mx - mn) / np.maximum(mx, 1)).mean()))
        lap = mm_img.laplacian_abs(g)
        sharp.append(float(np.median(mm_img.block_reduce_mean(lap, 8, 8))))
        q = (sm // 64).reshape(-1, 3).astype(np.int32)
        hh = np.bincount(q[:, 0] * 16 + q[:, 1] * 4 + q[:, 2], minlength=64).astype(np.float32)
        hist.append(hh / hh.sum())
        if n % 6 == 0:  # grain estimate: high-pass residual in flat areas
            hp = g - mm_img.gaussian_blur(g, 1.2)
            flat = mm_img.sobel_mag(mm_img.gaussian_blur(g, 2.0)) < 6.0
            if flat.mean() > 0.05:
                noise.append(float(1.4826 * np.median(np.abs(hp[flat]))))
        # global motion (similarity) prev → current
        m = (1.0, 0.0, 0.0, 0.0, 0.0)
        if have_cv2 and prev is not None:
            m = _similarity(prev, g)
        motion.append(m)
        prev = g
        n += 1
    reader.close()
    if n == 0:
        raise RuntimeError("could not decode any frame from the reference")
    return {"n": n, "small": np.stack(small), "lum": np.array(lum, np.float32), "lstd": np.array(lstd, np.float32),
            "sat": np.array(sat, np.float32), "sharp": np.array(sharp, np.float32), "hist": np.stack(hist),
            "motion": np.array(motion, np.float32), "mean_small": (acc / n).astype(np.float32),
            "noise": float(np.median(noise)) if noise else 0.0, "aw": aw, "ah": ah, "sw": sw, "sh": sh}


def _similarity(prev_g: np.ndarray, g: np.ndarray):
    """(scale, rot_deg, dx, dy, inlier_ratio) from prev to current using LK + RANSAC (OpenCV)."""
    cv2 = mm_img.cv2
    p8 = np.clip(prev_g, 0, 255).astype(np.uint8)
    c8 = np.clip(g, 0, 255).astype(np.uint8)
    pts = cv2.goodFeaturesToTrack(p8, maxCorners=200, qualityLevel=0.01, minDistance=8, blockSize=7)
    if pts is None or len(pts) < 12:
        return (1.0, 0.0, 0.0, 0.0, 0.0)
    nxt, st, _ = cv2.calcOpticalFlowPyrLK(p8, c8, pts, None, winSize=(21, 21), maxLevel=3)
    ok = st.reshape(-1) == 1
    if ok.sum() < 10:
        return (1.0, 0.0, 0.0, 0.0, 0.0)
    M, inl = cv2.estimateAffinePartial2D(pts[ok], nxt[ok], method=cv2.RANSAC, ransacReprojThreshold=1.5)
    if M is None:
        return (1.0, 0.0, 0.0, 0.0, 0.0)
    s = math.hypot(M[0, 0], M[1, 0])
    r = math.degrees(math.atan2(M[1, 0], M[0, 0]))
    h, w = g.shape
    # translation of the frame centre
    cx, cy = w / 2, h / 2
    dx = M[0, 0] * cx + M[0, 1] * cy + M[0, 2] - cx
    dy = M[1, 0] * cx + M[1, 1] * cy + M[1, 2] - cy
    return (float(s), float(r), float(dx), float(dy), float(inl.mean()) if inl is not None else 0.0)


# ----------------------------------------------------------------------------- distances

def _gray_small(feats):
    if "gsmall" not in feats:
        feats["gsmall"] = feats["small"].astype(np.float32).mean(-1)
    return feats["gsmall"]


def pair_dist(feats, i: np.ndarray, j: np.ndarray, tmask=None, block: int = 6, how: str = "median") -> np.ndarray:
    """Distance (0..255) between frames i[k] and j[k] over blocks of mean |ΔY|, text excluded.

    how='median' is robust (spikes only when most of the frame changes: cuts), how='mean' also sees
    partial changes (the first/last frames of a wipe or a slide)."""
    import warnings
    G = _gray_small(feats)
    i = np.clip(np.asarray(i), 0, len(G) - 1)
    j = np.clip(np.asarray(j), 0, len(G) - 1)
    out = np.zeros(len(i), np.float32)
    warnings.filterwarnings("ignore", message="Mean of empty slice")
    warnings.filterwarnings("ignore", message="All-NaN slice")
    for k0 in range(0, len(i), 512):
        ii, jj = i[k0:k0 + 512], j[k0:k0 + 512]
        d = np.abs(G[ii] - G[jj])
        if tmask is not None:
            valid = ~(tmask[ii] | tmask[jj])
            d = np.where(valid, d, np.nan)
        n, h, w = d.shape
        gh, gw = h // block, w // block
        d = d[:, : gh * block, : gw * block].reshape(n, gh, block, gw, block)
        with np.errstate(all="ignore"):
            bm = np.nanmean(d, axis=(2, 4)).reshape(n, -1)
            res = np.nanmedian(bm, axis=1) if how == "median" else np.nanmean(bm, axis=1)
        out[k0:k0 + 512] = np.nan_to_num(res, nan=0.0)
    return out


def hist_dist(feats, i, j):
    Hh = feats["hist"]
    return 0.5 * np.abs(Hh[np.clip(i, 0, len(Hh) - 1)] - Hh[np.clip(j, 0, len(Hh) - 1)]).sum(-1)


# ----------------------------------------------------------------------------- boundaries

def detect_boundaries(feats, tmask=None, L: int = 8, sensitivity: float = 1.0) -> list[dict]:
    N = feats["n"]
    idx = np.arange(N)
    D1 = np.zeros(N, np.float32)
    D1[1:] = pair_dist(feats, idx[1:], idx[:-1], tmask)
    D1m = np.zeros(N, np.float32)
    D1m[1:] = pair_dist(feats, idx[1:], idx[:-1], tmask, how="mean")
    feats["D1m"] = D1m
    H1 = np.zeros(N, np.float32)
    H1[1:] = hist_dist(feats, idx[1:], idx[:-1])
    DL = pair_dist(feats, idx - L, idx + L, tmask)
    HL = hist_dist(feats, idx - L, idx + L)
    feats["D1"], feats["DL"], feats["H1"], feats["HL"] = D1, DL, H1, HL
    cands = []
    # hard cuts: isolated spikes of the consecutive-frame distance
    for t in range(1, N):
        lo, hi = max(1, t - 10), min(N, t + 11)
        neigh = np.concatenate([D1[lo:max(lo, t - 1)], D1[min(hi, t + 2):hi]])
        local = float(np.median(neigh)) if len(neigh) else 0.0
        side = max(D1[t - 1] if t - 1 >= 1 else 0.0, D1[t + 1] if t + 1 < N else 0.0)
        if D1[t] > max(5.0, (3.0 * local + 2.0)) / sensitivity and D1[t] > 1.7 * side and (H1[t] > 0.06 or D1[t] > 20):
            cands.append({"c": t, "kind": "cut-spike", "score": float(D1[t])})
    # gradual: peaks of the lag-L distance that are not explained by a nearby cut
    med = float(np.median(DL))
    mad = float(np.median(np.abs(DL - med))) + 1e-3
    thr = max(5.0, med + 4.0 * mad) / sensitivity
    cut_at = [c["c"] for c in cands]
    for t in range(L, N - L):
        if DL[t] < thr or DL[t] < DL[t - 1] or DL[t] < DL[t + 1]:
            continue
        win = DL[max(0, t - L): t + L + 1]
        if DL[t] < win.max():
            continue
        if any(abs(t - c) <= L for c in cut_at):
            continue
        cands.append({"c": t, "kind": "gradual-peak", "score": float(DL[t])})
    cands.sort(key=lambda d: d["c"])
    # merge near-duplicates
    merged = []
    for c in cands:
        if merged and c["c"] - merged[-1]["c"] <= max(3, L // 2):
            if c["score"] > merged[-1]["score"]:
                merged[-1] = c
            continue
        merged.append(c)
    out = []
    for c in merged:
        b = refine_extent(feats, c, tmask, L)
        if b is not None:
            out.append(b)
    # drop overlaps (keep the stronger one)
    out.sort(key=lambda d: d["a"])
    final = []
    for b in out:
        if final and b["a"] <= final[-1]["b"] + 1:
            if b["strength"] > final[-1]["strength"]:
                final[-1] = b
            continue
        final.append(b)
    return final


def refine_extent(feats, cand, tmask, L):
    """Initial extent from the frame-to-frame change (mean over blocks, so partial wipes count),
    relative to the motion level inside the neighbouring shots."""
    N = feats["n"]
    D = feats["D1m"]
    c = cand["c"]
    ring = np.concatenate([D[max(1, c - 40):max(1, c - 14)], D[min(N, c + 14):min(N, c + 40)]])
    base = float(np.median(ring)) if len(ring) else float(np.median(D))
    spread = float(np.median(np.abs(ring - base))) if len(ring) else 1.0
    thr = max(base + 3.0 * spread + 0.6, base * 1.35, 1.0)
    span = 3 * L if cand["kind"] != "cut-spike" else 14
    best = None
    for d in range(0, L + 1):
        for t in (c - d, c + d):
            if 1 <= t < N and D[t] > thr:
                best = t
                break
        if best is not None:
            break
    if best is None:
        r0, r1 = (c, c) if cand["kind"] == "cut-spike" else (c - L // 2, c + L // 2)
    else:
        r0 = r1 = best
        while r0 - 1 >= 1 and D[r0 - 1] > thr and best - r0 < span:
            r0 -= 1
        while r1 + 1 < N and D[r1 + 1] > thr and r1 - best < span:
            r1 += 1
    a, b = r0, r1 - 1  # mixed frames [a, b]; pure A = a-1, pure B = b+1
    if cand["kind"] == "cut-spike" and b >= a:
        # zoom/blur/spin/whip transitions switch abruptly in the middle and one half can be faint
        # (dark footage): test the symmetric window; the fit trims whatever is really pure A/B
        k = max(c - a, b + 1 - c)
        a, b = max(1, c - k), min(N - 2, c + k - 1)
    # dips to black/white: grow to the whole monotone ramp of the mean luminance around the extreme
    lum = feats["lum"]
    lo, hi = max(1, a - 2 * L), min(N - 2, max(a, b) + 2 * L)
    k = lo + int(np.argmin(lum[lo:hi + 1]))
    if lum[k] < 0.06 and (a - L <= k <= b + L):
        a, b = min(a, k), max(b, k)
        while a - 1 >= 1 and lum[a - 1] > lum[a] + 0.002 and k - a < 4 * L:
            a -= 1
        while b + 1 < N - 1 and lum[b + 1] > lum[b] + 0.002 and b - k < 4 * L:
            b += 1
    k = lo + int(np.argmax(lum[lo:hi + 1]))
    if lum[k] > 0.9 and (a - L <= k <= b + L):
        a, b = min(a, k), max(b, k)
        while a - 1 >= 1 and lum[a - 1] < lum[a] - 0.002 and k - a < 4 * L:
            a -= 1
        while b + 1 < N - 1 and lum[b + 1] < lum[b] - 0.002 and b - k < 4 * L:
            b += 1
    a = max(1, a)
    b = min(N - 2, b)
    pa, pb = a - 1, b + 1
    if pb <= pa:
        return None
    g = pb - pa
    dAB = float(pair_dist(feats, np.array([pa]), np.array([pb]), tmask)[0])
    mA = float(pair_dist(feats, np.array([max(0, pa - g)]), np.array([pa]), tmask)[0])
    mB = float(pair_dist(feats, np.array([pb]), np.array([min(N - 1, pb + g)]), tmask)[0])
    hAB = float(hist_dist(feats, np.array([pa]), np.array([pb]))[0])
    real = dAB > 1.5 * max(mA, mB) + 1.5 or hAB > 0.25
    if not real:
        return None
    return {"a": int(a), "b": int(b), "pa": int(pa), "pb": int(pb), "strength": dAB / (max(mA, mB) + 1.0),
            "dAB": dAB, "hAB": hAB, "src": cand["kind"]}


# ----------------------------------------------------------------------------- classification

TIER1 = ["fade", "fadeblack", "fadewhite", "dipblack", "dipwhite", "flash", "blurcross", "zoomblur", "zoomin",
         "wipeleft", "wiperight", "wipeup", "wipedown", "slideleft", "slideright", "slideup", "slidedown",
         "smoothleft", "smoothright", "smoothup", "smoothdown", "coverleft", "coverright", "coverup", "coverdown",
         "revealleft", "revealright", "revealup", "revealdown", "circleopen", "circleclose", "dissolve",
         "whipleft", "whipright", "whipup", "whipdown", "fadefast", "fadeslow", "hblur", "fadegrays"]
TIER2 = [k for k in TR.ALL if k not in TIER1]


def _monotone_path(err: np.ndarray):
    """err[q, t] → minimal-cost non-decreasing q index path (DP). Returns (cost per frame, path)."""
    Q, T = err.shape
    cost = err[:, 0].copy()
    back = np.zeros((Q, T), np.int32)
    for t in range(1, T):
        best_prev = np.minimum.accumulate(cost)
        arg_prev = np.zeros(Q, np.int32)
        cur = 0
        for q in range(Q):
            if cost[q] <= cost[cur]:
                cur = q
            arg_prev[q] = cur
        back[:, t] = arg_prev
        cost = best_prev + err[:, t]
    q = int(np.argmin(cost))
    total = float(cost[q])
    path = [q]
    for t in range(T - 1, 0, -1):
        q = int(back[q, t])
        path.append(q)
    return total / T, path[::-1]


QS = np.array([0.01, 0.025, 0.05, 0.08, 0.12, 0.16, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7,
               0.75, 0.8, 0.84, 0.88, 0.92, 0.95, 0.975, 0.99])  # progress grid, dense near the ends
Q_LO, Q_HI = 0.015, 0.985


BLURRY = {"blurcross", "zoomblur", "zoomblurout", "whipleft", "whipright", "whipup", "whipdown", "spin", "hblur"}


class _Fitter:
    """Scores 'frames a..b are transition KIND from frame a-1 to frame b+1' by re-synthesis."""

    def __init__(self, feats, tmask):
        self.S = feats["small"]
        self.sharp = feats["sharp"]
        self.tmask = tmask
        self.cache = {}

    def blur_penalty(self, a, b, kind):
        """Kinds that blur the picture must show a sharpness dip on the reference."""
        if kind not in BLURRY:
            return 0.0
        ref = min(self.sharp[a - 1], self.sharp[min(len(self.sharp) - 1, b + 1)])
        dip = float(self.sharp[a:b + 1].min()) / max(1e-3, ref)
        return 0.05 if dip > 0.85 else (0.02 if dip > 0.7 else 0.0)

    def fit(self, a, b, kind, params):
        key = (a, b, kind, tuple(sorted(params.items())))
        if key in self.cache:
            return self.cache[key]
        S = self.S
        pa, pb = a - 1, b + 1
        A = S[pa].astype(np.float32)
        B = S[pb].astype(np.float32)
        F = S[a:b + 1].astype(np.float32)
        D = b - a + 1
        valid = np.ones(A.shape[:2], bool)
        if self.tmask is not None:
            valid = ~self.tmask[pa:pb + 1].any(0)
            if valid.mean() < 0.3:
                valid = np.ones(A.shape[:2], bool)
        vw = valid[..., None].astype(np.float32)
        nval = float(vw.sum() * 3)
        norm = float((np.abs(A - B) * vw).sum() / nval) + 4.0
        Ts = np.stack([TR.render(kind, A, B, 1.0 - q, **params) for q in QS])
        flatT = (Ts * vw[None]).reshape(len(QS), -1)
        flatF = (F * vw[None]).reshape(D, -1)
        err = np.stack([np.abs(flatT - flatF[t][None]).sum(1) / nval for t in range(D)], 1)
        # structure term: gradients keep blur-type kinds from 'winning' just by smoothing the mismatch
        gw = valid.astype(np.float32)
        nv = float(gw.sum()) + 1.0
        GT = np.stack([mm_img.sobel_mag(t.mean(-1)) for t in Ts]).reshape(len(QS), -1) * gw.reshape(1, -1)
        GF = np.stack([mm_img.sobel_mag(f.mean(-1)) for f in F]).reshape(D, -1) * gw.reshape(1, -1)
        gerr = np.stack([np.abs(GT - GF[t][None]).sum(1) / nv for t in range(D)], 1)
        err = err + 0.35 * gerr
        per, path = _monotone_path(err)
        res = (per / norm + TR.COMPLEXITY.get(kind, 0.0), [float(QS[p]) for p in path], per)
        self.cache[key] = res
        return res


def classify(feats, bnd: dict, tmask=None, deep: bool = True, fitter: _Fitter | None = None) -> dict:
    a, b = bnd["a"], bnd["b"]
    N = feats["n"]
    D = b - a + 1
    if D <= 0:
        return {"type": "cut", "ts": int(bnd["pb"]), "te": int(bnd["pb"]), "frames": 0, "confidence": 0.95,
                "progress": [], "alternatives": [], "params": {}}
    fitter = fitter or _Fitter(feats, tmask)
    results = []
    for kind in ["cut"] + TIER1:
        for params in TR.PARAM_GRID.get(kind, [TR.default_params(kind)]):
            s, path, per = fitter.fit(a, b, kind, params)
            results.append((s, kind, params, path, per))
    results.sort(key=lambda r: r[0])
    if deep and results[0][0] > 0.22:
        for kind in TIER2:
            for params in TR.PARAM_GRID.get(kind, [TR.default_params(kind)]):
                s, path, per = fitter.fit(a, b, kind, params)
                results.append((s, kind, params, path, per))
        results.sort(key=lambda r: r[0])
    best = results[0]
    kind, params = best[1], best[2]
    if kind == "cut":
        sw = a + next((i for i, q in enumerate(best[3]) if q >= 0.5), D)
        return {"type": "cut", "ts": int(sw), "te": int(sw), "frames": 0, "confidence": 0.8, "progress": [],
                "alternatives": [[r[1], round(r[0], 4)] for r in results[1:6]], "params": {},
                "fit_error": round(best[0], 4)}
    # grow the extent while the neighbouring frames are still explained as part of this transition
    sc = best[0]
    for _ in range(10):
        if a - 2 < 0:
            break
        s2, p2, _ = fitter.fit(a - 1, b, kind, params)
        if p2[0] > 0.06 and s2 <= sc * 1.12 + 0.004:
            a, sc, best = a - 1, s2, (s2, kind, params, p2, None)
        else:
            break
    for _ in range(10):
        if b + 2 >= N:
            break
        s2, p2, _ = fitter.fit(a, b + 1, kind, params)
        if p2[-1] < 0.94 and s2 <= sc * 1.12 + 0.004:
            b, sc, best = b + 1, s2, (s2, kind, params, p2, None)
        else:
            break
    # shrink ends that the path says are pure A / pure B
    path = list(best[3])
    while len(path) > 1 and path[0] <= Q_LO and a < b:
        a += 1
        path.pop(0)
    while len(path) > 1 and path[-1] >= Q_HI and b > a:
        b -= 1
        path.pop()
    D = b - a + 1
    fam = _family(kind)
    second = next((r for r in results[1:] if _family(r[1]) != fam), None)
    margin = (second[0] - results[0][0]) if second else 0.5
    conf = float(np.clip(0.5 + margin * 3.0 - sc, 0.05, 0.99))
    return {"type": kind, "params": params, "ts": int(a), "te": int(b + 1), "frames": int(D),
            "progress": [round(p, 3) for p in path], "fit_error": round(sc, 4), "confidence": round(conf, 2),
            "alternatives": [[r[1], round(r[0], 4)] for r in results[1:6]]}


def _family(kind):
    for f in ("wipe", "slide", "smooth", "cover", "reveal", "whip", "circle", "diag", "fade", "dip", "zoom"):
        if kind.startswith(f):
            return f
    return kind


# ----------------------------------------------------------------------------- per-shot measures

def shot_measures(feats, s0: int, s1: int, b0: int, b1: int, tmask=None) -> dict:
    """Look + motion over the shot body [b0, b1)."""
    S = feats["small"]
    idx = np.linspace(b0, max(b0, b1 - 1), num=min(8, max(1, b1 - b0))).round().astype(int)
    stats = []
    for i in idx:
        m = None if tmask is None else ~tmask[i]
        stats.append(mm_color.lab_stats(S[i], m))
    look = mm_color.merge_stats(stats)
    # centre-weighted stats (r < 0.6): used for colour transfer when a vignette is re-applied on top
    h, w = S.shape[1:3]
    yy, xx = np.mgrid[0:h, 0:w]
    rr = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) / math.sqrt(2)
    centre = rr < 0.6
    stats_c = []
    for i in idx:
        m = centre if tmask is None else (centre & ~tmask[i])
        stats_c.append(mm_color.lab_stats(S[i], m))
    look_c = mm_color.merge_stats(stats_c)
    mid = S[(b0 + b1) // 2]
    pal = mm_color.palette(mid, k=5, mask=None if tmask is None else ~tmask[(b0 + b1) // 2])
    mo = feats["motion"][b0 + 1:b1] if b1 - b0 > 2 else feats["motion"][b0:b0 + 1]
    W = feats["aw"]
    if len(mo):
        zoom_ps = float(np.prod(mo[:, 0]) ** (1.0 / max(1, len(mo))))
        dx = float(np.median(mo[:, 2]))
        dy = float(np.median(mo[:, 3]))
        mag = float(np.median(np.hypot(mo[:, 2], mo[:, 3]))) / W
        steady = float(np.std(mo[:, 0]))
    else:
        zoom_ps, dx, dy, mag, steady = 1.0, 0.0, 0.0, 0.0, 0.0
    fps_like = 1.0
    sharp = float(np.median(feats["sharp"][b0:max(b0 + 1, b1)]))
    lum = float(np.mean(feats["lum"][b0:max(b0 + 1, b1)]))
    sat = float(np.mean(feats["sat"][b0:max(b0 + 1, b1)]))
    D1 = feats.get("D1")
    pace = float(np.median(D1[b0 + 1:b1])) if D1 is not None and b1 - b0 > 2 else 0.0
    return {"lab": look, "lab_center": look_c, "palette": pal, "lum": rnd(lum), "sat": rnd(sat), "sharp": rnd(sharp, 2),
            "motion": {"zoom_per_frame": rnd(zoom_ps, 5), "zoom_per_s": None, "pan_x_per_frame": rnd(dx / W, 5),
                       "pan_y_per_frame": rnd(dy / W, 5), "speed": rnd(mag, 5), "pace": rnd(pace, 3),
                       "zoom_jitter": rnd(steady, 5)}}


def global_look(feats, shots, tmask=None) -> dict:
    meanY = feats["mean_small"]
    h, w = meanY.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) / math.sqrt(2)
    center = meanY[r < 0.25].mean()
    corner = meanY[r > 0.85].mean()
    ratio = float(corner / max(center, 1e-3))
    # per-frame vignette consistency: corner/centre ratio in each sampled frame
    G = _gray_small(feats)
    sel = np.linspace(0, len(G) - 1, num=min(60, len(G))).round().astype(int)
    ratios = np.array([G[i][r > 0.85].mean() / max(G[i][r < 0.25].mean(), 1e-3) for i in sel])
    consistent = float(np.mean(ratios < 0.92))
    vig = 0.0
    if ratio < 0.9 and consistent > 0.7:
        # model: L(r) = 1 - v * r^2.2 → v from the corner ring (mean r≈0.9)
        vig = float(np.clip((1 - ratio) / (0.9 ** 2.2), 0, 0.9))
    # letterbox: rows (top/bottom) that stay near-black in the mean image AND in the max
    S = feats["small"]
    mx = S[sel].max(axis=(0, 3)).astype(np.float32)  # h × w
    rowmax = mx.max(1)
    top = 0
    while top < h // 3 and rowmax[top] < 18:
        top += 1
    bot = 0
    while bot < h // 3 and rowmax[h - 1 - bot] < 18:
        bot += 1
    lum = feats["lum"]
    N = feats["n"]
    fade_in = 0
    if lum[0] < 0.04:
        while fade_in < min(N - 1, 90) and lum[fade_in] < 0.6 * lum[min(N - 1, fade_in + 30)]:
            fade_in += 1
    fade_out = 0
    if lum[-1] < 0.04:
        while fade_out < min(N - 1, 90) and lum[N - 1 - fade_out] < 0.6 * lum[max(0, N - 1 - fade_out - 30)]:
            fade_out += 1
    return {"vignette": {"strength": rnd(vig, 3), "corner_ratio": rnd(ratio, 3), "consistency": rnd(consistent, 2)},
            "grain": {"sigma": rnd(feats["noise"], 2)},
            "letterbox": {"top": rnd(top / h, 3), "bottom": rnd(bot / h, 3)},
            "fade_in_frames": int(fade_in), "fade_out_frames": int(fade_out)}


# ----------------------------------------------------------------------------- main entry

def analyze(ref: str, work: str, text_color: str | None = None, sensitivity: float = 1.0,
            skip_text: bool = False, deep: bool = True) -> dict:
    import mm_text
    P = work_paths(work)
    for k in ("frames", "sheets", "text", "audio", "cache"):
        ensure_dir(P[k])
    info = probe(ref)
    fps, W, H = info["fps"], info["w"], info["h"]
    log(f"reference: {W}x{H} @ {float(fps):.3f} fps, {info['duration']:.2f}s, audio={info.get('has_audio')}")
    with Timer("audio"):
        audio = extract_audio(ref, P["audio"])
    with Timer("pass A (shots/look features)"):
        feats = pass_a(ref, fps, W, H)
    N = feats["n"]
    text = {"events": [], "small_masks": None}
    if not skip_text:
        with Timer("text layer"):
            text = mm_text.analyze_text(ref, fps, W, H, N, P, feats, text_color=text_color)
    tmask = text.get("small_masks")
    with Timer("boundaries"):
        bnds = detect_boundaries(feats, tmask, sensitivity=sensitivity)
    trans = []
    with Timer("transitions (re-synthesis)"):
        fitter = _Fitter(feats, tmask)
        for bd in bnds:
            tr = classify(feats, bd, tmask, deep=deep, fitter=fitter)
            tr["evidence"] = {"src": bd["src"], "strength": rnd(bd["strength"], 2), "dAB": rnd(bd["dAB"], 2)}
            if trans and tr["ts"] < trans[-1]["te"]:  # keep transitions disjoint
                if tr["frames"] == 0 or tr["te"] <= trans[-1]["te"]:
                    continue
                tr["ts"] = trans[-1]["te"]
                tr["frames"] = tr["te"] - tr["ts"]
            trans.append(tr)
    # shots from transitions
    shots = []
    starts = [0] + [t["ts"] for t in trans]
    ends = [t["te"] for t in trans] + [N]
    for i in range(len(trans) + 1):
        s0 = starts[i]
        s1 = ends[i]
        b0 = trans[i - 1]["te"] if i > 0 else 0
        b1 = trans[i]["ts"] if i < len(trans) else N
        shots.append({"id": i + 1, "start": int(s0), "end": int(s1), "body": [int(b0), int(b1)]})
    for i, t in enumerate(trans):
        t["id"] = i + 1
        t["between"] = [i + 1, i + 2]
        t["ts_s"], t["te_s"] = rnd(f2t(t["ts"], fps)), rnd(f2t(t["te"], fps))
        t["type_ar"] = TR.AR.get(t["type"], t["type"])
    with Timer("shot measures + keyframes"):
        key_idx = []
        for s in shots:
            b0, b1 = s["body"]
            if b1 <= b0:
                b0, b1 = s["start"], max(s["start"] + 1, s["end"])
            s.update(shot_measures(feats, s["start"], s["end"], b0, b1, tmask))
            mo = s["motion"]
            mo["zoom_per_s"] = rnd(mo["zoom_per_frame"] ** float(fps), 4)
            s["start_s"], s["end_s"] = rnd(f2t(s["start"], fps)), rnd(f2t(s["end"], fps))
            s["dur_s"] = rnd(f2t(s["end"] - s["start"], fps))
            s["kenburns"] = _kenburns_guess(mo, float(fps))
            ks = [b0, (b0 + b1 - 1) // 2, max(b0, b1 - 1)]
            s["key_frames"] = ks
            key_idx += ks
        frames = grab_frames_at(ref, key_idx, fps)
        clean_masks = mm_text.masks_at(text, key_idx, W, H) if not skip_text else {}
        for s in shots:
            names = []
            for tag, i in zip(("first", "mid", "last"), s["key_frames"]):
                fr = frames.get(i)
                if fr is None:
                    continue
                p = P["frames"] / f"shot{s['id']:02d}_{tag}.jpg"
                mm_img.save_jpg(p, fr, 92)
                m = clean_masks.get(i)
                if m is not None and m.any():
                    clean = mm_img.inpaint(fr, mm_img.dilate(m, max(2, W // 180)), radius=max(3, W // 120))
                else:
                    clean = fr
                pc = P["frames"] / f"shot{s['id']:02d}_{tag}_clean.jpg"
                mm_img.save_jpg(pc, clean, 92)
                names.append({"tag": tag, "frame": int(i), "t": rnd(f2t(i, fps)), "image": str(p.relative_to(P["root"])),
                              "clean": str(pc.relative_to(P["root"]))})
            s["keyframes"] = names
            s["describe"] = ""
            s["queries"] = []
            s["replacement"] = None
    look = global_look(feats, shots, tmask)
    spec = {
        "version": 1,
        "skill": "kosif-mimic",
        "reference": {"path": str(Path(ref).resolve()), "w": W, "h": H, "fps": fps_str(fps), "frames": N,
                      "duration": rnd(N / float(fps), 4), "audio": audio},
        "shots": shots,
        "transitions": trans,
        "texts": text["events"],
        "text_style_global": text.get("global"),
        "look": look,
        "review": {"texts_confirmed": False, "fonts_confirmed": False, "shots_described": False},
        "notes": [],
    }
    save_json(P["spec"], spec)
    np.savez_compressed(P["cache"] / "feats.npz", small=feats["small"], lum=feats["lum"], sharp=feats["sharp"],
                        D1=feats["D1"], DL=feats["DL"], motion=feats["motion"])
    if tmask is not None:
        np.savez_compressed(P["cache"] / "text_small.npz", m=np.packbits(tmask, axis=-1), shape=np.array(tmask.shape))
    import mm_sheets
    with Timer("sheets"):
        mm_sheets.all_sheets(spec, P, feats)
    write_summary(spec, P)
    return spec


def _kenburns_guess(mo, fps):
    z = mo["zoom_per_frame"]
    if z is None:
        return None
    zps = z ** fps
    # a steady, centred zoom of ≥ 1%/s with little pan is most likely an editor's Ken Burns move
    if abs(zps - 1) >= 0.01 and abs(mo["pan_x_per_frame"]) < 0.002 and abs(mo["pan_y_per_frame"]) < 0.002 and (mo["zoom_jitter"] or 0) < 0.004:
        return {"zoom_per_s": rnd(zps, 4), "apply": True, "why": "steady centred zoom measured on the reference"}
    return None


def write_summary(spec: dict, P: dict):
    fps = Fraction(spec["reference"]["fps"])
    L = []
    r = spec["reference"]
    L.append(f"# تحليل الفيديو المرجعي\n")
    L.append(f"- الأبعاد: {r['w']}×{r['h']} — {float(fps):.3f} fps — {r['frames']} فريم ({tc(r['duration'])})")
    au = r.get("audio") or {}
    L.append(f"- الصوت: {'موجود (' + str(au.get('codec')) + ') ومحفوظ نسخة أصلية بدون تعديل' if au.get('has_audio') else 'لا يوجد'}")
    L.append(f"- عدد اللقطات: {len(spec['shots'])} — عدد الانتقالات: {len(spec['transitions'])} — عدد الكتابات: {len(spec['texts'])}\n")
    L.append("## اللقطات")
    for s in spec["shots"]:
        pal = ", ".join(p["name"] for p in s.get("palette", [])[:3])
        L.append(f"- لقطة {s['id']}: {tc(s['start_s'])} → {tc(s['end_s'])} ({s['dur_s']:.2f}ث) — ألوان: {pal} — حركة: {s['motion']['speed']}")
    L.append("\n## الانتقالات")
    for t in spec["transitions"]:
        L.append(f"- {t['id']}: بين لقطة {t['between'][0]} و {t['between'][1]} — {t['type_ar']} (`{t['type']}`) — "
                 f"{t['frames']} فريم عند {tc(t['ts_s'])} — ثقة {t['confidence']}")
    L.append("\n## الكتابة")
    for e in spec["texts"]:
        L.append(f"- كتابة {e['id']}: {tc(e['time']['in_start_s'])} → {tc(e['time']['out_end_s'])} — دخول: {e['anim_in']['type']} — "
                 f"خروج: {e['anim_out']['type']} — سطور: {len(e['lines'])} — OCR: {' / '.join(l.get('ocr', '') for l in e['lines'])}")
    lk = spec["look"]
    L.append(f"\n## الإحساس اللوني\n- فينييت: {lk['vignette']['strength']} — حبيبات: {lk['grain']['sigma']} — "
             f"أشرطة سوداء: {lk['letterbox']}")
    (P["root"] / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
