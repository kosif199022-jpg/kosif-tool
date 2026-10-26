"""KOSIF Mimic (المحاكاة) — rebuild a reference reel shot for shot with new footage: the same cut times to the frame,
the same transitions, the same words in the same place and lettering, the same sound — only the pictures change.
The method is references/mimic.md; the usual source of new footage is Pinterest through `kmotion fetch`.

    python scripts/kmotion.py mimic study REF.mp4 --out DIR
        → DIR/mimic.json   measured: frame-exact boundaries (hard cut / dissolve / dip to black / dip to white / slide),
                           shots with clip lengths for rebuilding, look per shot (colour mean/std, contrast, saturation,
                           motion), text zones + text-change times, fades, audio loudness; and the fields Claude fills:
                           shots[].query (Pinterest searches), texts[] (words, times, style), text_style
          DIR/audio.wav    the reference sound, lossless (the new film is cut on it)
          DIR/shots/       first/mid/last full-resolution frame of every shot;  DIR/search/  mid frames with the text
                           painted out (for describing and for visual search);  DIR/text/  crops of the text zones
          DIR/shots.jpg    every shot with its time and transition;  DIR/strip.jpg  a frame every 0.5 s (text changes)
    python scripts/kmotion.py mimic layer DIR [--erase x0,y0,x1,y1 …]
        the fixed design (title, date, badges, icons — whatever stays over every shot) lifted as layer/overlay.png
        (RGBA); boxes erased = the creator's watermark/handle/logo, which are never copied; study runs it once
    python scripts/kmotion.py mimic fonts DIR [--shot N]
        draws texts[N].text (or the first text) in every Arabic font on this PC, scores each against the reference crop
        (shape overlap) → DIR/fonts.jpg + ranking in mimic.json (text_style.font_candidates)
    python scripts/kmotion.py mimic match DIR --pool FOLDER [--set 3=clip.mp4@2.5 …] [--strength 0.7]
        for every shot, the pool clip + in-point closest in look and motion (one clip per shot while the pool allows),
        with a colour transfer towards the reference → DIR/match.json + DIR/match.jpg (reference | choice)
    python scripts/kmotion.py mimic build DIR --out FILM.mp4 [--no-color] [--no-text]
        timeline spec with the reference's clip lengths, transitions, texts and sound → FILM + compare
    python scripts/kmotion.py mimic compare REF FILM [--out DIR]
        side-by-side sheet + boundary/duration/audio deltas → compare.json + compare.jpg (the mimic gate)
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import analyze as A  # noqa: E402

FF = shutil.which("ffmpeg") or "ffmpeg"
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv", ".m4v", ".avi"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}
XFADE = {"dissolve": "fade", "fadeblack": "fadeblack", "fadewhite": "fadewhite", "slideleft": "slideleft",
         "slideright": "slideright", "slideup": "slideup", "slidedown": "slidedown", "wipe": "wipeleft", "unknown": "fade"}


# ───────────────────────── frames ─────────────────────────
def frames(video: Path, width: int, fps: float) -> np.ndarray:
    """RGB frames (N, h, w, 3) at a constant `fps` (the reference's own rate for frame-exact work)."""
    info = A.probe(video)
    h = max(2, int(round(info["height"] * width / info["width"] / 2) * 2))
    r = subprocess.run([FF, "-v", "error", "-i", str(video), "-vf", f"fps={fps},scale={width}:{h}:flags=area",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True)
    n = len(r.stdout) // (width * h * 3)
    return np.frombuffer(r.stdout[: n * width * h * 3], np.uint8).reshape(n, h, width, 3)


def still(video: Path, t: float, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([FF, "-y", "-v", "error", "-ss", f"{max(0.0, t):.4f}", "-i", str(video), "-frames:v", "1", "-q:v", "2", str(out)], check=True)
    return out


def imread(p: Path):
    """cv2.imread that works with Arabic (non-ASCII) paths on Windows."""
    import cv2
    try:
        return cv2.imdecode(np.fromfile(str(p), np.uint8), cv2.IMREAD_UNCHANGED if str(p).lower().endswith(".png") else cv2.IMREAD_COLOR)
    except (OSError, ValueError):
        return None


def imwrite(p: Path, im) -> None:
    import cv2
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    ok, buf = cv2.imencode(Path(p).suffix or ".png", im)
    if not ok:
        raise IOError(f"cannot encode {p}")
    buf.tofile(str(p))


def _gray(f: np.ndarray) -> np.ndarray:
    return f[..., 0] * 0.299 + f[..., 1] * 0.587 + f[..., 2] * 0.114


# ───────────────────────── boundaries (frame-exact) ─────────────────────────
def _dips(lum: np.ndarray, fps: float) -> tuple[list[dict], dict]:
    """Dips to black / white between shots — a near-black (near-white) moment with brightness ramps on both sides —
    found on the brightness curve before anything else (a dip often hides a hard cut at its darkest frame).
    Dips touching the first or last frame are the film's fade in / fade out."""
    n = len(lum)
    out, fades = [], {"in": 0.0, "out": 0.0}
    w, gap = int(1.5 * fps), max(2, int(0.4 * fps))
    i = 0
    while i < n:
        dark, light = lum[i] < 16, lum[i] > 238
        lo, hi = max(0, i - int(0.5 * fps)), min(n, i + int(0.5 * fps) + 1)
        if not (dark and lum[i] <= lum[lo:hi].min() + 1e-6) and not (light and lum[i] >= lum[lo:hi].max() - 1e-6):
            i += 1
            continue
        before = float(np.median(lum[max(0, i - w):max(1, i - gap)])) if i > gap else None
        after = float(np.median(lum[min(n - 1, i + gap):min(n, i + w)])) if i + gap < n else None
        sides = [v for v in (before, after) if v is not None]
        if not sides or (dark and max(sides) < 30) or (light and min(sides) > 200):
            i += 1
            continue
        flat = (lambda j: lum[j] < 16) if dark else (lambda j: lum[j] > 238)
        away = (lambda a, b: lum[a] > lum[b] + 0.3) if dark else (lambda a, b: lum[a] < lum[b] - 0.3)
        s = e = i
        while s - 1 >= 0 and flat(s - 1):
            s -= 1
        while e + 1 < n and flat(e + 1):
            e += 1
        def back(j, level):                                             # the side's own level is reached
            return level is not None and ((lum[j] >= 0.92 * level) if dark else (lum[j] <= level + 0.08 * (255 - level)))
        while s - 1 >= 0 and away(s - 1, s) and i - s < w and not back(s, before):
            s -= 1
        while e + 1 < n and away(e + 1, e) and e - i < w and not back(e, after):
            e += 1
        if s == 0 and dark:
            fades["in"] = round(e / fps, 3)
        elif e == n - 1 and dark:
            fades["out"] = round((n - 1 - s) / fps, 3)
        else:
            out.append({"frame": s, "end_frame": e, "start": round(s / fps, 4), "dur": round((e - s) / fps, 4),
                        "type": "fadeblack" if dark else "fadewhite", "conf": 0.9})
        i = e + 1
    return out, fades


def _blend(g: np.ndarray, a: int, b: int, js) -> tuple[np.ndarray, np.ndarray]:
    """For frames js, the mix ratio between frame a (0) and frame b (1) and how far each frame is from that mix."""
    Af, Bf = g[a].astype(np.float64), g[b].astype(np.float64)
    diff = Bf - Af; den = float((diff ** 2).sum()) + 1e-9; rms = math.sqrt(den / diff.size) + 1e-9
    al, res = [], []
    for j in js:
        F = g[j].astype(np.float64)
        x = float(((F - Af) * diff).sum() / den)
        al.append(x); res.append(math.sqrt(float(((F - Af - x * diff) ** 2).mean())) / rms)
    return np.array(al), np.array(res)


def boundaries(fr: np.ndarray, fps: float, ignore: np.ndarray | None = None) -> dict:
    """Shot boundaries to the frame: dips to black/white, hard cuts, dissolves (every frame a measured blend of the
    shot before and after), slides. Frame i shows [i/fps, (i+1)/fps). Gradual changes that are none of these go to
    `suspects` (camera moves look like that too) for a human look, never silently into the edit.
    `ignore` (bool, frame-sized): pixels left out — the text zone, so words fading in are not read as a dissolve."""
    n = len(fr)
    if ignore is not None and n and ignore.any():
        fr = fr.copy(); fr[:, ignore] = 0
    g = np.stack([_gray(f.astype(np.float32)) for f in fr]) if n else np.zeros((0, 1, 1))
    lum = g.reshape(n, -1).mean(1) if n else np.zeros(0)
    H = np.stack([A._hist(f) for f in fr]) if n else np.zeros((0, 512))
    d1 = np.zeros(n); h1 = np.zeros(n)
    if n > 1:
        d1[1:] = np.abs(g[1:] - g[:-1]).reshape(n - 1, -1).mean(1)
        h1[1:] = np.abs(H[1:] - H[:-1]).sum(1)
    out, fades = _dips(lum, fps)
    blocked = np.zeros(n, bool)
    for b in out:
        blocked[b["frame"]:b["end_frame"] + 1] = True
    if fades["in"]:
        blocked[:int(round(fades["in"] * fps)) + 1] = True
    if fades["out"]:
        blocked[n - 1 - int(round(fades["out"] * fps)):] = True
    flashes, suspects = [], []
    # hard cuts: one frame carries the whole change
    for i in range(1, n):
        if blocked[i]:
            continue
        lo, hi = max(1, i - 15), min(n, i + 16)
        nb = np.concatenate([d1[lo:i], d1[i + 1:hi]]); hb = np.concatenate([h1[lo:i], h1[i + 1:hi]])
        base, hbase = (float(np.median(nb)) if len(nb) else 0.0), (float(np.median(hb)) if len(hb) else 0.0)
        if d1[i] >= max(10.0, 4 * base + 4) and h1[i] >= max(0.35, 3 * hbase + 0.1) and d1[i] >= d1[max(1, i - 1):i + 2].max():
            if 0 < i < n - 1 and np.abs(H[i + 1] - H[i - 1]).sum() < 0.25:     # back to the same picture: a flash
                flashes.append({"t": round(i / fps, 4), "frame": i, "kind": "flash-white" if lum[i] > lum[i - 1] else "flash-dark"})
                continue
            out.append({"frame": i, "end_frame": i, "start": round(i / fps, 4), "dur": 0.0, "type": "cut", "conf": 0.95})
            blocked[i] = True
    # gradual changes: the picture k frames before and after differs, and no single frame carries it
    k = max(2, int(round(0.2 * fps)))
    D = np.zeros(n)
    for i in range(k, n - k):
        D[i] = np.abs(H[i - k] - H[i + k]).sum()
    W = int(round(1.2 * fps))
    for i in range(k, n - k):
        if D[i] < 0.5 or D[i] < D[max(0, i - k):i + k + 1].max() or blocked[max(0, i - k):i + k + 1].any():
            continue
        ok = lambda j: 0 <= j < n and not blocked[j]                    # noqa: E731
        a, b = i - k, i + k
        if not (ok(a) and ok(b)) or np.abs(H[a] - H[b]).sum() < 0.45:
            continue
        for _ in range(int(2 * fps)):                                   # grow while the blend carries on past a / b
            grew = False
            if ok(a - 1) and _blend(g, a, b, [a - 1])[0][0] < -0.06:
                a -= 1; grew = True
            if ok(b + 1) and _blend(g, a, b, [b + 1])[0][0] > 1.06:
                b += 1; grew = True
            if not grew:
                break
        al, _ = _blend(g, a, b, range(a, b + 1))
        s, e = a + 1, b - 1                                             # trim frames that are already pure A / pure B
        while s < e and al[s - a] < 0.04:
            s += 1
        while e > s and al[e - a] > 0.96:
            e -= 1
        a, b = s - 1, e + 1
        kind, conf = "unknown", 0.3
        if b - a >= 2 and np.abs(H[a] - H[b]).sum() >= 0.45:
            al2, res2 = _blend(g, a, b, range(a + 1, b))
            if len(al2) and float(np.median(res2)) < 0.35 and np.all(np.diff(al2) > -0.15) and al2[0] < 0.5 < al2[-1]:
                ga, gb = g[a] - g[a].mean(), g[b] - g[b].mean()
                same = float((ga * gb).sum() / (np.linalg.norm(ga) * np.linalg.norm(gb) + 1e-9))
                if same > 0.75:                                         # the same picture getting brighter/darker
                    suspects.append({"t": round(a / fps, 3), "dur": round((b - a) / fps, 3), "change": round(float(D[i]), 2),
                                     "why": f"exposure fade inside one shot (same picture, structure r={same:.2f}) — not a cut"})
                    blocked[a:b + 1] = True
                    continue
                kind, conf = "dissolve", round(max(0.5, 1 - float(np.median(res2))), 2)
        if kind == "unknown":
            a, b = i - k, i + k
            dx = float(np.median([A.shift(g[j - 1], g[j])[0] for j in range(a + 1, b + 1)]))
            dy = float(np.median([A.shift(g[j - 1], g[j])[1] for j in range(a + 1, b + 1)]))
            if max(abs(dx), abs(dy)) > 3.0 and np.abs(H[a] - H[b]).sum() >= 0.8:
                kind = ("slideleft" if dx < 0 else "slideright") if abs(dx) >= abs(dy) else ("slideup" if dy < 0 else "slidedown")
                conf = 0.5
        if kind == "unknown":
            suspects.append({"t": round(i / fps, 3), "change": round(float(D[i]), 2), "why": "gradual change that is not a blend: camera move or a wipe — look at the frames"})
            continue
        out.append({"frame": a, "end_frame": b, "start": round(a / fps, 4), "dur": round((b - a) / fps, 4), "type": kind, "conf": conf})
        blocked[a:b + 1] = True
    out.sort(key=lambda d: d["start"])
    return {"boundaries": out, "flashes": flashes, "suspects": suspects, "fades": fades, "lum": lum, "d1": d1}


def shots_from(bounds: list[dict], duration: float) -> list[dict]:
    """Shots between boundaries; `clip` is the length a rebuilt clip needs (it is on screen through both transitions)."""
    edges = [{"start": 0.0, "dur": 0.0, "type": "start"}] + bounds + [{"start": duration, "dur": 0.0, "type": "end"}]
    shots = []
    for i in range(len(edges) - 1):
        p, q = edges[i], edges[i + 1]
        own0, own1 = p["start"] + p["dur"], q["start"]
        shots.append({"i": i + 1, "start": round(p["start"], 4), "end": round(q["start"] + q["dur"], 4),
                      "own": [round(own0, 4), round(own1, 4)], "clip": round(q["start"] + q["dur"] - p["start"], 4),
                      "in": {"type": p["type"], "dur": p["dur"]} if p["type"] != "start" else None,
                      "out": {"type": q["type"], "dur": q["dur"]} if q["type"] != "end" else None})
    return shots


# ───────────────────────── text zones ─────────────────────────
def text_mask(f: np.ndarray) -> np.ndarray:
    """Pixels that look like overlay lettering: bright and pale (white text) or warm and bright (gold text), on a
    strong local edge."""
    import cv2
    hsv = cv2.cvtColor(f, cv2.COLOR_RGB2HSV)
    gray = cv2.cvtColor(f, cv2.COLOR_RGB2GRAY)
    edge = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 60
    edge = cv2.dilate(edge.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    white = (hsv[..., 2] > 190) & (hsv[..., 1] < 70)
    gold = (hsv[..., 0] >= 12) & (hsv[..., 0] <= 35) & (hsv[..., 1] > 80) & (hsv[..., 2] > 150)
    near_dark = cv2.erode(hsv[..., 2], np.ones((5, 5), np.uint8)) < 110      # an outline or shadow within 2 px
    return (white | gold) & edge & near_dark


def zone_of(P: np.ndarray, W: int, H: int) -> dict | None:
    """The text block from a persistence map (fraction of frames each pixel looked like text)."""
    import cv2
    z = (P > 0.55).astype(np.uint8)
    if z.sum() < 0.0008 * W * H:
        return None
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (max(3, int(W * 0.05)), max(3, int(H * 0.012))))
    zz = cv2.dilate(z, k)
    n, lab, st, _ = cv2.connectedComponentsWithStats(zz)
    boxes = [st[j] for j in range(1, n) if st[j][4] > 0.002 * W * H and st[j][3] < 0.6 * H]
    if not boxes:
        return None
    x0 = min(b[0] for b in boxes); y0 = min(b[1] for b in boxes)
    x1 = max(b[0] + b[2] for b in boxes); y1 = max(b[1] + b[3] for b in boxes)
    inside = z[y0:y1, x0:x1].sum() / max(1, z.sum())
    return {"bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "conf": round(float(inside), 2)}


def ignore_mask(masks: np.ndarray, shape: tuple[int, int], share: float = 0.08) -> np.ndarray | None:
    """Pixels that carry lettering in at least `share` of the film, grown a little, at the boundary resolution."""
    import cv2
    if not len(masks):
        return None
    z = (masks.mean(0) >= share).astype(np.uint8)
    if not z.any():
        return None
    Hm, Wm = z.shape
    z = cv2.dilate(z, cv2.getStructuringElement(cv2.MORPH_RECT, (max(3, Wm // 25), max(3, Hm // 60))))
    return cv2.resize(z, (shape[1], shape[0]), interpolation=cv2.INTER_NEAREST) > 0


# ───────────────────────── the fixed overlay layer ─────────────────────────
def template_mask(masks: np.ndarray, med: np.ndarray, share: float = 0.7) -> np.ndarray:
    """Lettering present in ≥ `share` of the non-dark frames: the film's fixed design (title, date, badges, icons)."""
    if not len(masks):
        return np.zeros(med.shape[1:3], bool)
    bright = np.array([_gray(f.astype(np.float32)).mean() > 40 for f in med])
    sub = masks[bright] if bright.any() else masks
    return sub.mean(0) >= share


def layer(dir_: Path, erase: list | None = None, snap: list | None = None) -> dict:
    """Lift the fixed overlay out of the reference as an RGBA PNG: a pixel that keeps its colour over every shot's
    different background belongs to the layer; how much it still varies gives its transparency (soft shadows/edges).
    `erase` = boxes [x0, y0, x1, y1] (fractions) removed from the layer — the creator's watermark, handle and logo
    are never copied into the new film."""
    import cv2
    rep = json.loads((dir_ / "mimic.json").read_text(encoding="utf-8"))
    ims = [imread(p) for p in sorted((dir_ / "shots").glob("shot_*_m.jpg"))]   # mid frames: shot edges are still dimmed by dips
    ims = [im for im in ims if im is not None and _gray(im.astype(np.float32)).mean() > 40]
    if len(ims) < 5:
        raise SystemExit("need at least 5 bright frames from different shots to lift the layer")
    st = np.stack(ims).astype(np.float32)                              # N, H, W, 3 (BGR)
    Hh, Ww = st.shape[1:3]
    med = np.median(st, 0)
    spread = np.median(np.abs(st - med), 0).mean(2)                    # robust per-pixel variation over the shots
    # the layer holds its colour to compression noise (≈ 0–8) while backgrounds swing by tens of levels
    core = (spread < 10).astype(np.uint8)
    core = cv2.morphologyEx(core, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    n, lab, stt, _ = cv2.connectedComponentsWithStats(core, connectivity=8)
    keep = np.zeros(n, bool); keep[1:] = stt[1:, 4] >= max(40, int(Hh * Ww * 0.00006))
    core = keep[lab].astype(np.uint8)
    region = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
    alpha = np.clip((18 - spread) / 12, 0, 1) * region
    # near an element, accept more variation (glints, shimmer, soft glow) to close its gaps — never far from one
    near = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (max(7, Ww // 40),) * 2)) > 0
    # thin coloured lines pick up the background through compression in a few shots: count in how many shots the
    # pixel keeps its colour (within 22 levels of the median) instead of how far it swings on average
    cons = (np.abs(st - med).mean(3) < 22).mean(0)
    loose = np.maximum(np.clip((30 - spread) / 14, 0, 1), np.clip((cons - 0.55) / 0.25, 0, 1)) * near
    loose_core = (loose > 0.5).astype(np.uint8)
    n2, lab2, st2, _ = cv2.connectedComponentsWithStats(loose_core, connectivity=8)
    ok2 = np.zeros(n2, bool); ok2[1:] = st2[1:, 4] >= max(40, int(Hh * Ww * 0.00006))
    alpha = np.maximum(alpha, loose * cv2.dilate(ok2[lab2].astype(np.uint8), np.ones((3, 3), np.uint8)))
    # the layer's own palette (gold, green, white…): a pixel near the layer whose median colour is one of those
    # colours and that keeps it in ≥ 45 % of the shots belongs to it too (thin ornaments, digits on a dimmed disc)
    sure = med[alpha > 0.8]
    pal = None
    if len(sure) > 50:
        from scipy.cluster.vq import kmeans2
        pal, _ = kmeans2(sure[:: max(1, len(sure) // 20000)].astype(np.float64), min(6, len(sure) // 10), seed=3, minit="++")
        wide = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (max(9, Ww // 15),) * 2)) > 0
        ys, xs = np.nonzero(wide)
        sub = st[:, ys, xs]                                             # N, P, 3: every shot votes per pixel
        hit = np.min(np.linalg.norm(sub[:, :, None, :] - pal[None, None], axis=3), axis=2) < 30
        vote = hit.mean(0)
        colour = np.array([np.median(sub[hit[:, j], j], 0) if hit[:, j].any() else med[ys[j], xs[j]] for j in range(len(ys))])
        keyed = np.zeros((Hh, Ww), np.float32); keyed[ys, xs] = np.clip((vote - 0.5) / 0.2, 0, 1)
        newer = (keyed > 0.5) & (alpha < 0.5)
        med[ys, xs] = np.where(newer[ys, xs, None], colour, med[ys, xs])
        alpha = np.maximum(alpha, cv2.morphologyEx(keyed.astype(np.float32), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)))
    # elements that move a little (a bobbing medallion) are not fixed pixels: take them from ONE shot, keyed by the
    # layer palette inside the box — `snap` = [{"box": [x0, y0, x1, y1], "shot": N}]
    snaps = snap if snap is not None else rep.get("layer", {}).get("snap", [])
    for sp_ in snaps or []:
        x0, y0, x1, y1 = sp_["box"]
        X0, Y0, X1, Y1 = int(x0 * Ww), int(y0 * Hh), int(math.ceil(x1 * Ww)), int(math.ceil(y1 * Hh))
        fim = imread(dir_ / "shots" / f"shot_{int(sp_['shot']):02d}_m.jpg").astype(np.float32)[Y0:Y1, X0:X1]
        if len(sure) > 50:
            dd = np.min(np.linalg.norm(fim[..., None, :] - pal[None, None], axis=3), axis=2)
            hue = np.clip((34 - dd) / 14, 0, 1)
            if sp_.get("hsv"):                                          # a hue range, e.g. gold [18, 40, 80, 140]
                h0, h1, s0, v0 = sp_["hsv"]
                hsv = cv2.cvtColor(fim.astype(np.uint8), cv2.COLOR_BGR2HSV)
                hue = ((hsv[..., 0] >= h0) & (hsv[..., 0] <= h1) & (hsv[..., 1] > s0) & (hsv[..., 2] > v0)).astype(np.float32)
                ring = cv2.dilate(hue, np.ones((3, 3), np.uint8)) > 0       # its dark outline, right next to it
                hue = np.maximum(hue, (ring & (hsv[..., 2] < 90)).astype(np.float32))
            hue = cv2.morphologyEx(hue.astype(np.float32), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
            alpha[Y0:Y1, X0:X1] = hue
            med[Y0:Y1, X0:X1] = fim
    # specks: faint or tiny islands (smoke and highlights that several backgrounds share) are not design
    lab_n, lab3, st3, _ = cv2.connectedComponentsWithStats((alpha > 0.15).astype(np.uint8), connectivity=8)
    peak = np.zeros(lab_n); np.maximum.at(peak, lab3.ravel(), alpha.ravel())
    strong = np.zeros(lab_n); np.add.at(strong, lab3.ravel(), (alpha > 0.8).ravel())
    keep3 = (peak > 0.85) & (strong >= max(30, int(Hh * Ww * 0.00004))); keep3[0] = False
    alpha = alpha * keep3[lab3]
    alpha = cv2.GaussianBlur(alpha, (3, 3), 0)
    for x0, y0, x1, y1 in erase or rep.get("layer", {}).get("erase", []) or []:
        alpha[int(y0 * Hh):int(math.ceil(y1 * Hh)), int(x0 * Ww):int(math.ceil(x1 * Ww))] = 0
    rgba = np.dstack([np.clip(med, 0, 255).astype(np.uint8), (alpha * 255).astype(np.uint8)])
    imwrite(dir_ / "layer" / "overlay.png", rgba)
    grey = np.full_like(med, 96); chk = ((np.indices((Hh, Ww)).sum(0) // 24) % 2)[..., None] * 60 + 70
    prev = [(med * alpha[..., None] + b * (1 - alpha[..., None])).astype(np.uint8) for b in (grey, np.repeat(chk, 3, 2).astype(np.float32))]
    imwrite(dir_ / "layer" / "overlay_preview.jpg", np.hstack(prev))
    rep.setdefault("layer", {})
    rep["layer"].update({"file": "layer/overlay.png", "use": rep["layer"].get("use", True), "erase": erase or rep["layer"].get("erase", []),
                         "snap": snaps or [],
                         "frames": len(ims), "coverage": round(float((alpha > 0.5).mean()), 4)})
    (dir_ / "mimic.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    return rep["layer"]


# ───────────────────────── look ─────────────────────────
def look(fr: np.ndarray, d1: np.ndarray | None = None, zone: list | None = None) -> dict:
    """Colour mean/std per channel, contrast, saturation, motion and the colour histogram — text zone left out."""
    if not len(fr):
        return {}
    h, w = fr.shape[1:3]
    m = np.ones((h, w), bool)
    if zone:
        x0, y0, x1, y1 = zone
        m[int(y0 * h):int(math.ceil(y1 * h)), int(x0 * w):int(math.ceil(x1 * w))] = False
        if m.sum() < 0.2 * h * w:
            m[:] = True
    px = fr[:, m].reshape(-1, 3).astype(np.float32)
    mx, mn = px.max(1), px.min(1)
    sat = float(np.mean((mx - mn) / (mx + 1e-6)))
    hist = np.mean([A._hist(f[m].reshape(-1, 1, 3)) for f in fr], axis=0)
    return {"mean": [round(float(v), 2) for v in px.mean(0)], "std": [round(float(v), 2) for v in px.std(0)],
            "contrast": round(float(_gray(px).std()), 2), "sat": round(sat, 4),
            "motion": round(float(np.median(d1)) if d1 is not None and len(d1) else 0.0, 3),
            "hist": [round(float(v), 5) for v in hist]}


def loudness(audio: Path) -> float | None:
    r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", str(audio), "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r'"input_i"\s*:\s*"(-?[\d.]+|-inf)"', r.stderr)
    return float(m.group(1)) if m and m.group(1) != "-inf" else None


# ───────────────────────── sheets ─────────────────────────
def _font(size: int):
    from PIL import ImageFont
    for p in (r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def sheet(cells: list[tuple[list, str]], out: Path, cols: int, cell_w: int = 220) -> Path:
    """Grid of image groups with a caption under each group; a group is one or more PIL images side by side."""
    from PIL import Image, ImageDraw
    if not cells:
        return out
    gw = max(len(c[0]) for c in cells) * cell_w
    hs = [max(int(im.height * cell_w / im.width) for im in c[0]) for c in cells]
    ch = max(hs) + 26
    rows = math.ceil(len(cells) / cols)
    canvas = Image.new("RGB", (cols * (gw + 8) + 8, rows * (ch + 8) + 8), (18, 18, 22))
    dr = ImageDraw.Draw(canvas); f = _font(14)
    for k, (ims, cap) in enumerate(cells):
        x0, y0 = 8 + (k % cols) * (gw + 8), 8 + (k // cols) * (ch + 8)
        for j, im in enumerate(ims):
            t = im.convert("RGB").resize((cell_w, int(im.height * cell_w / im.width)))
            canvas.paste(t, (x0 + j * cell_w, y0))
        dr.text((x0 + 2, y0 + ch - 22), cap, fill=(235, 235, 235), font=f)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, quality=88)
    return out


# ───────────────────────── study ─────────────────────────
def study(ref: Path, out: Path) -> dict:
    import cv2
    from PIL import Image
    out.mkdir(parents=True, exist_ok=True)
    info = A.probe(ref)
    fps = info["fps"] or 30.0
    fr = frames(ref, 96, fps)
    duration = round(len(fr) / fps, 4) if len(fr) else info["duration"]
    # text first (medium frames at 4 fps): its zone is left out while looking for shot boundaries
    tfps = 4.0
    med = frames(ref, 270, tfps)
    Hm, Wm = med.shape[1:3]
    masks = np.stack([text_mask(f) for f in med]) if len(med) else np.zeros((0, Hm, Wm), bool)
    ignore = ignore_mask(masks, fr.shape[1:3])
    bd = boundaries(fr, fps, ignore)
    shots = shots_from(bd["boundaries"], duration)
    import cv2
    tmask = template_mask(masks, med)
    imwrite(out / "layer" / "template_mask.png", (tmask * 255).astype(np.uint8))
    not_tmpl = ~(cv2.dilate(tmask.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0)
    for s in shots:
        a, b = int(s["own"][0] * tfps), max(int(s["own"][0] * tfps) + 1, int(s["own"][1] * tfps))
        sub = masks[a:b]
        s["text_zone"] = zone_of(sub.mean(0) * not_tmpl, Wm, Hm) if len(sub) else None
        fa, fb = int(round(s["own"][0] * fps)), max(int(round(s["own"][0] * fps)) + 1, int(round(s["own"][1] * fps)))
        s["look"] = look(fr[fa:fb], bd["d1"][fa + 1:fb], (s["text_zone"] or {}).get("bbox"))
        s["query"] = []; s["notes"] = ""
    # where the words change (inside the union of text zones)
    zones = [s["text_zone"]["bbox"] for s in shots if s.get("text_zone")]
    events = []
    if zones and len(masks):
        x0, y0 = min(z[0] for z in zones), min(z[1] for z in zones)
        x1, y1 = max(z[2] for z in zones), max(z[3] for z in zones)
        sub = masks[:, int(y0 * Hm):int(math.ceil(y1 * Hm)), int(x0 * Wm):int(math.ceil(x1 * Wm))]
        prev = None
        for j, m in enumerate(sub):
            cur = m.sum() > 0.01 * m.size
            if prev is not None:
                pm = sub[j - 1]
                inter, union = (m & pm).sum(), (m | pm).sum()
                iou = inter / union if union else 1.0
                if cur != prev or (cur and iou < 0.45):
                    t = round(j / tfps, 2)
                    if not events or t - events[-1]["t"] > 0.3:
                        events.append({"t": t, "kind": "appear" if cur and not prev else "disappear" if prev and not cur else "change"})
            prev = cur
    # audio
    audio = None
    if info["audio"]:
        wav = out / "audio.wav"
        subprocess.run([FF, "-y", "-v", "error", "-i", str(ref), "-vn", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(wav)], check=True)
        ext = {"aac": "m4a", "mp3": "mp3", "opus": "opus", "vorbis": "ogg"}.get(info["audio"]["codec"], "mka")
        subprocess.run([FF, "-y", "-v", "error", "-i", str(ref), "-vn", "-c:a", "copy", str(out / f"audio.orig.{ext}")])
        audio = {"file": "audio.wav", "original": f"audio.orig.{ext}", **info["audio"], "lufs": loudness(wav)}
    # stills: first / mid / last of every shot, a text-free search frame, the text crop
    cells = []
    for s in shots:
        t0, t1 = s["own"]; tm = (t0 + t1) / 2
        n = s["i"]
        for tag, t in (("a", t0 + 0.5 / fps), ("m", tm), ("b", max(t0, t1 - 1.5 / fps))):
            still(ref, t, out / "shots" / f"shot_{n:02d}_{tag}.jpg")
        im = imread(out / "shots" / f"shot_{n:02d}_m.jpg")
        if s.get("text_zone") and im is not None:
            x0, y0, x1, y1 = s["text_zone"]["bbox"]; hh, ww = im.shape[:2]
            px0, py0, px1, py1 = int(x0 * ww), int(y0 * hh), int(math.ceil(x1 * ww)), int(math.ceil(y1 * hh))
            pad = int(0.02 * ww)
            crop = im[max(0, py0 - pad):py1 + pad, max(0, px0 - pad):px1 + pad]
            (out / "text").mkdir(exist_ok=True)
            imwrite(out / "text" / f"shot_{n:02d}.png", crop)
            mfull = cv2.resize(text_mask(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)).astype(np.uint8), (ww, hh))
            box = np.zeros_like(mfull); box[max(0, py0 - pad):py1 + pad, max(0, px0 - pad):px1 + pad] = 1
            clean = cv2.inpaint(im, cv2.dilate(mfull * box, np.ones((7, 7), np.uint8)), 7, cv2.INPAINT_TELEA)
            px = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)[(mfull * box) > 0]
            if len(px):
                s["text_zone"]["color"] = "#%02x%02x%02x" % tuple(int(v) for v in np.median(px, 0))
        else:
            clean = im
        if clean is not None:
            (out / "search").mkdir(exist_ok=True)
            imwrite(out / "search" / f"shot_{n:02d}.jpg", clean)
        lab = f"#{n} {t0:.2f}-{t1:.2f}s  in:{(s['in'] or {}).get('type', 'start')}" + (f" {s['in']['dur']:.2f}s" if s.get("in") and s["in"]["dur"] else "")
        cells.append(([Image.open(out / "shots" / f"shot_{n:02d}_m.jpg")], lab))
    sheet(cells, out / "shots.jpg", cols=min(6, max(1, len(cells))))
    strip = [(([Image.fromarray(med[j])]), f"{j / tfps:.1f}s") for j in range(0, len(med), 2)]
    sheet(strip, out / "strip.jpg", cols=10, cell_w=150)
    rep = {
        "kind": "kosif-mimic", "version": 1, "ref": str(ref.resolve()), "info": info, "fps": fps, "duration": duration,
        "audio": audio, "fades": bd["fades"], "flashes": bd["flashes"], "suspects": bd["suspects"],
        "boundaries": [{k: v for k, v in b.items() if k != "end_frame"} for b in bd["boundaries"]], "shots": shots,
        "text_events": events,
        "text_style": {"font": None, "size": None, "color": None, "stroke": None, "stroke_color": "#000000",
                       "shadow": True, "box": None, "anim": "fade", "fade": 0.35, "line_height": 1.3, "align": "center"},
        "texts": [],
        "todo": ["read shots.jpg, strip.jpg and text/*.png; write every on-screen text into texts[] with start/end "
                 "(text_events are measured hints) and x/y as the CENTRE of the block in fractions of the frame",
                 "set text_style (colour, stroke, shadow, box, anim) from the crops; run `mimic fonts` and pick the font",
                 "look at layer/overlay_preview.jpg: the fixed design lifted from the film; erase the creator's watermark/"
                 "handle/logo with `mimic layer DIR --erase x0,y0,x1,y1` (never copy them); layer.use=false to retype instead",
                 "describe each search/shot_XX.jpg into shots[].query: 2–4 Pinterest searches (English + Arabic)",
                 "fetch candidates into one pool folder, then `mimic match` and `mimic build`"],
    }
    rep["layer"] = {"template_share": round(float(tmask.mean()), 4)}
    (out / "mimic.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    if tmask.mean() > 0.002:
        try:
            rep["layer"] = layer(out)
        except SystemExit as e:
            rep["layer"]["error"] = str(e)
            (out / "mimic.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    return rep


# ───────────────────────── fonts ─────────────────────────
def arabic_fonts() -> list[Path]:
    dirs = [Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts",
            Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "Fonts",
            Path("/usr/share/fonts"), Path.home() / ".fonts", HERE / "kit" / "fonts"]
    seen, out = set(), []
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        TTFont = None
    for d in dirs:
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*")):
            if p.suffix.lower() not in (".ttf", ".otf") or p.name.lower() in seen:
                continue
            seen.add(p.name.lower())
            try:
                cm = TTFont(str(p), lazy=True, fontNumber=0).getBestCmap() if TTFont else {0x627: 1, 0x644: 1}
            except Exception:
                continue
            # Pillow here has no RAQM: the shaper uses presentation forms, so a font without them draws '?'
            if cm and all(c in cm for c in (0x627, 0x644, 0x647, 0x639, 0xFEDF, 0xFE8E, 0xFEEB)):
                out.append(p)
    return out


def _render_mask(text: str, font_path: Path, size: int = 120):
    from PIL import Image, ImageDraw, ImageFont
    import timeline as T
    f = ImageFont.truetype(str(font_path), size)
    lines = [T._shape(ln) for ln in text.split("\n")]
    probe = ImageDraw.Draw(Image.new("L", (8, 8)))
    w = int(max(probe.textlength(ln, font=f) for ln in lines) + size)
    h = int(size * 1.6 * len(lines) + size)
    im = Image.new("L", (w, h), 0); dr = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        dr.text((w / 2, size * 0.5 + i * size * 1.6), ln, font=f, fill=255, anchor="ma")
    a = np.array(im) > 127
    ys, xs = np.nonzero(a)
    return (a[ys.min():ys.max() + 1, xs.min():xs.max() + 1], im) if len(ys) else (None, im)


def fonts(dir_: Path, shot: int | None = None, top: int = 12) -> dict:
    import cv2
    from PIL import Image
    rep = json.loads((dir_ / "mimic.json").read_text(encoding="utf-8"))
    texts = rep.get("texts") or []
    if not texts:
        raise SystemExit("mimic.json has no texts yet: write texts[] first (read text/*.png), then run fonts")
    t = texts[shot] if shot is not None else texts[0]
    # the reference crop: the shot that shows this text
    tm = (t["start"] + t["end"]) / 2
    s = next((s for s in rep["shots"] if s["own"][0] <= tm <= s["own"][1]), rep["shots"][0])
    crop_p = dir_ / "text" / f"shot_{s['i']:02d}.png"
    ref_im = imread(crop_p) if crop_p.exists() else None
    if "y" in t:                                                        # the band of this text in the shot's mid frame
        full = imread(dir_ / "shots" / f"shot_{s['i']:02d}_m.jpg")
        hh = full.shape[0]
        sz = float(t.get("size") or rep["text_style"].get("size") or 0.06)
        sz = sz if sz < 1 else sz / hh
        half = sz * hh * (0.9 + 0.65 * t["text"].count(chr(10)))
        y0, y1 = max(0, int(t["y"] * hh - half)), min(hh, int(t["y"] * hh + half))
        ref_im = full[y0:y1]
        crop_p = dir_ / "text" / f"band_{s['i']:02d}.png"; imwrite(crop_p, ref_im)
    if ref_im is None:
        raise SystemExit(f"no text crop for shot {s['i']} (text zone not detected) — pick the font by eye from shots/")
    m = text_mask(cv2.cvtColor(ref_im, cv2.COLOR_BGR2RGB))
    ys, xs = np.nonzero(m)
    if not len(ys):
        raise SystemExit("the crop has no lettering pixels")
    refm = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(np.uint8)
    refd = cv2.dilate(refm, np.ones((3, 3), np.uint8)) > 0
    scored = []
    for p in arabic_fonts():
        try:
            cm, _ = _render_mask(t["text"], p)
        except Exception:
            continue
        if cm is None:
            continue
        r = cv2.resize(cm.astype(np.uint8), (refm.shape[1], refm.shape[0]), interpolation=cv2.INTER_AREA) > 0
        rd = cv2.dilate(r.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
        prec = (r & refd).sum() / max(1, r.sum()); rec = (refm.astype(bool) & rd).sum() / max(1, refm.sum())
        aspect = 1 - min(1.0, abs(math.log((cm.shape[1] / cm.shape[0]) / (refm.shape[1] / refm.shape[0]))))
        score = 2 * prec * rec / max(1e-6, prec + rec) * (0.7 + 0.3 * aspect)
        scored.append({"font": str(p), "name": p.stem, "score": round(float(score), 4)})
    scored.sort(key=lambda d: -d["score"])
    cells = [([Image.open(crop_p)], f"REFERENCE (shot {s['i']})")]
    for c in scored[:top]:
        _, im = _render_mask(t["text"], Path(c["font"]))
        cells.append(([im.convert("RGB")], f"{c['name']}  {c['score']:.3f}"))
    sheet(cells, dir_ / "fonts.jpg", cols=3, cell_w=420)
    rep["text_style"]["font_candidates"] = scored[:top]
    (dir_ / "mimic.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"sheet": str(dir_ / "fonts.jpg"), "top": scored[:top]}


# ───────────────────────── match ─────────────────────────
def _features(fr: np.ndarray) -> dict:
    g = np.stack([_gray(f.astype(np.float32)) for f in fr])
    d1 = np.zeros(len(fr)); d1[1:] = np.abs(g[1:] - g[:-1]).reshape(len(fr) - 1, -1).mean(1) if len(fr) > 1 else 0
    px = fr.reshape(len(fr), -1, 3).astype(np.float32)
    mx, mn = px.max(2), px.min(2)
    H = np.stack([A._hist(f) for f in fr])
    h1 = np.zeros(len(fr)); h1[1:] = np.abs(H[1:] - H[:-1]).sum(1) if len(fr) > 1 else 0
    lum = g.reshape(len(fr), -1).mean(1)
    # the source's own edits: a jump in picture AND colour between neighbouring samples, or a near-black / white frame —
    # a window that holds one would show an extra cut or dip in the new film that the reference does not have
    cut = (d1 > 22) & (h1 > 0.55)                                      # cut[j]: the picture changes between j-1 and j
    dark = (lum < 18) | (lum > 245)                                    # dark[j]: sample j itself is near black / white
    return {"hist": H, "mean": px.mean(1), "std": px.std(1), "contrast": _gray(px).std(1),
            "sat": ((mx - mn) / (mx + 1e-6)).mean(1), "d1": d1, "cut": cut, "dark": dark, "brk": cut | dark}


def source_edits(p: Path, info: dict, n: int, mfps: float) -> np.ndarray:
    """Sample indices (at mfps) touched by a cut, dissolve or dip inside a source clip — found with the same
    frame-exact detector as the reference, so look-alike shots joined by a cut are caught too."""
    out = np.zeros(n, bool)
    fps = info.get("fps") or 30.0
    try:
        bd = boundaries(frames(p, 96, fps), fps)
    except Exception:
        return out
    for b in bd["boundaries"]:
        a = max(0, int(math.ceil(b["start"] * mfps - 1e-6)))
        e = min(n - 1, int(math.ceil((b["start"] + b["dur"]) * mfps - 1e-6)))
        out[a:e + 1] = True
    return out


def _cost(ref: dict, F: dict, a: int, b: int, mfps: float, rfps: float) -> float:
    h = np.abs(F["hist"][a:b].mean(0) - np.array(ref["hist"])).sum() / 2
    mean = np.linalg.norm(F["mean"][a:b].mean(0) - np.array(ref["mean"])) / 441.7
    con = abs(float(F["contrast"][a:b].mean()) - ref["contrast"]) / 64
    sat = abs(float(F["sat"][a:b].mean()) - ref["sat"])
    mot = abs(float(np.median(F["d1"][a + 1:b])) * (rfps / mfps) / 3 - ref["motion"] / 3) if b - a > 2 else 0.3   # per-frame motion at the ref rate
    edits = 2.0 if F["cut"][a + 1:b].any() or F["dark"][a:b].any() else 0.0   # never put the source's own cuts on screen
    return 0.40 * h + 0.25 * mean + 0.10 * min(1, con) + 0.10 * sat + 0.15 * min(1, mot) + edits


def colour_transfer(ref_look: dict, mean: np.ndarray, std: np.ndarray, strength: float) -> dict:
    out = {}
    for j, ch in enumerate("rgb"):
        mu_r, sd_r, mu_c, sd_c = ref_look["mean"][j], ref_look["std"][j], float(mean[j]), float(std[j])
        gain = float(np.clip(1 + strength * (sd_r / max(sd_c, 1.0) - 1), 0.6, 1.6))
        off = float(np.clip(mu_c * (1 - gain) + strength * (mu_r - mu_c), -120, 120))
        out[ch] = [round(gain, 4), round(off, 2)]
    return out


def match(dir_: Path, pool: Path, sets: list[str] | None = None, strength: float = 0.7) -> dict:
    from PIL import Image
    from scipy.optimize import linear_sum_assignment
    rep = json.loads((dir_ / "mimic.json").read_text(encoding="utf-8"))
    rfps, portrait = rep["fps"], rep["info"]["height"] > rep["info"]["width"]
    files = sorted(p for p in pool.rglob("*") if p.suffix.lower() in VIDEO_EXT | IMAGE_EXT and ".orig." not in p.name)
    edit_copies = {p.name.replace(".edit", "") for p in files if ".edit." in p.name}
    files = [p for p in files if ".edit." in p.name or p.name not in edit_copies]     # prefer fetch's edit-safe copy
    if not files:
        raise SystemExit(f"no videos or images in {pool}")
    mfps = 6.0                                                         # fine enough to see a source cut
    cands = []
    for p in files:
        try:
            if p.suffix.lower() in IMAGE_EXT:
                src = Image.open(p).convert("RGB")
                fr = np.stack([np.array(src.resize((96, max(2, int(96 * src.height / src.width)))))] * 4)
                info = {"width": src.width, "height": src.height, "duration": 0.0}
                kind = "image"
            else:
                info = A.probe(p); fr = frames(p, 96, mfps); kind = "video"
        except Exception as e:  # unreadable file: skip, but say so
            print(f"skip {p.name}: {e}", file=sys.stderr)
            continue
        if len(fr) < 1:
            continue
        F = _features(fr)
        if kind == "video":                                            # the source's own edits, at its full frame rate
            F["cut"] = F["cut"] | source_edits(p, info, len(fr), mfps)
        cands.append({"file": p, "kind": kind, "info": info, "F": F, "n": len(fr)})
    # the whole pool on one sheet (mid frame, name, length) — what the eye chooses from for --set
    pcells = []
    for c in cands:
        tmp = dir_ / "pool" / f"{c['file'].stem[:40]}.jpg"
        try:
            if c["kind"] == "video":
                still(c["file"], c["info"]["duration"] / 2, tmp); im = Image.open(tmp)
            else:
                im = Image.open(c["file"])
            pcells.append(([im], f"{c['file'].stem[:18]}  {c['info'].get('duration', 0):.1f}s"))
        except Exception:
            continue
    sheet(pcells, dir_ / "pool.jpg", cols=8, cell_w=150)
    shots = rep["shots"]
    forced = {}
    for s in sets or []:
        k, v = s.split("=", 1)
        f, _, t = v.partition("@")
        forced[int(k)] = (Path(f), float(t) if t.strip() else None)        # no time: the best clean window in that clip
    reps = max(1, math.ceil(len(shots) / max(1, len(cands))))
    cols, cost = [], np.full((len(shots), len(cands) * reps), 9.0)
    best_win = {}
    for ci, c in enumerate(cands):
        for r in range(reps):
            cols.append((ci, r))
    for si, s in enumerate(shots):
        need = s["clip"]
        for ci, c in enumerate(cands):
            if c["kind"] == "image":
                wins = [(0, c["n"])]; speed = 1.0
            else:
                L = c["info"]["duration"]
                speed = 1.0 if L >= need else max(0.5, L / need)
                span = max(2, int(round(need * speed * mfps)))
                wins = [(a, min(c["n"], a + span)) for a in range(0, max(1, c["n"] - span + 1), max(1, int(mfps / 2)))]
                if L < need * 0.5:
                    continue
            ranked = sorted((_cost(s["look"], c["F"], a, b, mfps, rfps), a, b) for a, b in wins)
            k, a, b = ranked[0]
            shape = 0.05 if (c["info"]["height"] > c["info"]["width"]) != portrait else 0.0
            small = 0.05 if min(c["info"]["width"], c["info"]["height"]) < 540 else 0.0
            best_win[(si, ci)] = (k + shape + small, a, b, speed)
            for r in range(reps):
                cost[si, ci * reps + r] = k + shape + small + 0.12 * r
    rows, colsel = linear_sum_assignment(cost)
    picks = []
    for si, cj in zip(rows, colsel):
        s = shots[si]
        if s["i"] in forced:
            f, t0 = forced[s["i"]]
            img = f.suffix.lower() in IMAGE_EXT
            if img:
                sub = np.stack([np.array(Image.open(f).convert("RGB").resize((96, 170)))] * 2); L = 0.0
            else:
                finfo = A.probe(f); sub = frames(f, 96, mfps); L = finfo["duration"]
            F = _features(sub)
            if not img:
                F["cut"] = F["cut"] | source_edits(f, finfo, len(sub), mfps)
            speed = 1.0 if img or L >= s["clip"] else max(0.5, L / s["clip"])
            span = max(2, int(round(s["clip"] * speed * mfps)))
            if t0 is None and not img:
                wins = [(a0, min(len(sub), a0 + span)) for a0 in range(0, max(1, len(sub) - span + 1))]
                k_, a, b = min((_cost(s["look"], F, a0, b0, mfps, rfps), a0, b0) for a0, b0 in wins)
                t0 = a / mfps
            else:
                t0 = t0 or 0.0; a = int(t0 * mfps); b = min(len(sub), a + span); k_ = _cost(s["look"], F, a, b, mfps, rfps)
            picks.append({"shot": s["i"], "file": str(f.resolve()), "kind": "image" if img else "video",
                          "in": round(t0, 3), "speed": round(speed, 4), "cost": round(float(k_), 4), "forced": True,
                          "match": colour_transfer(s["look"], F["mean"][a:b].mean(0), F["std"][a:b].mean(0), strength)})
            continue
        ci, _ = cols[cj]
        c = cands[ci]
        k, a, b, speed = best_win[(si, ci)]
        picks.append({"shot": s["i"], "file": str(c["file"].resolve()), "kind": c["kind"], "in": round(a / mfps, 3),
                      "speed": round(speed, 4), "cost": round(float(k), 4), "forced": False,
                      "match": colour_transfer(s["look"], c["F"]["mean"][a:b].mean(0), c["F"]["std"][a:b].mean(0), strength)})
    picks.sort(key=lambda d: d["shot"])
    cells = []
    for pk in picks:
        s = shots[pk["shot"] - 1]
        refp = dir_ / "search" / f"shot_{pk['shot']:02d}.jpg"
        tmp = dir_ / "match" / f"shot_{pk['shot']:02d}.jpg"
        if pk["kind"] == "video":
            still(Path(pk["file"]), pk["in"] + s["clip"] * pk["speed"] / 2, tmp)
            cim = Image.open(tmp)
        else:
            cim = Image.open(pk["file"])
        cells.append(([Image.open(refp) if refp.exists() else cim, cim],
                      f"#{pk['shot']} {s['clip']:.2f}s  {Path(pk['file']).stem[:22]}  cost {pk['cost']}"))
    sheet(cells, dir_ / "match.jpg", cols=3, cell_w=200)
    bad = [pk["shot"] for pk in picks if pk["cost"] is not None and pk["cost"] >= 2.0]
    if bad:
        print(f"warning: shots {bad} got a window holding the source's own cut or a black frame — the pool has no clean "
              f"clip long enough; fetch more footage for them or --set N=file@seconds", file=sys.stderr)
    res = {"pool": str(pool.resolve()), "strength": strength, "picks": picks, "unclean_shots": bad}
    (dir_ / "match.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    return res


# ───────────────────────── build ─────────────────────────
def build(dir_: Path, out: Path, colour: bool = True, text: bool = True, workers: int = 0) -> dict:
    import timeline as T
    rep = json.loads((dir_ / "mimic.json").read_text(encoding="utf-8"))
    mt = json.loads((dir_ / "match.json").read_text(encoding="utf-8"))
    picks = {p["shot"]: p for p in mt["picks"]}
    if text and not rep.get("texts"):
        raise SystemExit("mimic.json has no texts: write texts[] from text/*.png and strip.jpg first (or pass --no-text)")
    w, h = rep["info"]["width"], rep["info"]["height"]
    short = min(w, h)
    k = 1080 / short if short < 1080 else 1.0                       # quality-first: shortest side ≥ 1080, same aspect
    W, H = int(round(w * k / 2) * 2), int(round(h * k / 2) * 2)
    fps = int(round(rep["fps"]))
    clips = []
    for s in rep["shots"]:
        p = picks.get(s["i"])
        if not p:
            raise SystemExit(f"shot {s['i']} has no clip in match.json")
        c = {"fit": "cover"}
        if p["kind"] == "image":
            c.update({"image": p["file"], "dur": s["clip"], "zoom": {"from": 1.0, "to": 1.06}})
        else:
            # the window must end inside the source: a clip cut short shifts every later boundary
            L = A.probe(Path(p["file"]))["duration"]
            need = s["clip"] * p["speed"]
            t_in = max(0.0, min(p["in"], L - need - 0.04))
            if L - t_in < need - 1e-3:
                raise SystemExit(f"shot {s['i']}: {Path(p['file']).name} is {L:.2f}s, the shot needs {need:.2f}s — pick a longer clip")
            c.update({"src": p["file"], "in": round(t_in, 4), "out": round(t_in + need, 4), "speed": p["speed"], "mute": True})
        if colour and p.get("match"):
            c["match"] = p["match"]
        if s.get("out") and s["out"]["type"] != "cut":
            c["transition"] = {"type": XFADE.get(s["out"]["type"], "fade"), "dur": max(0.05, s["out"]["dur"])}
        clips.append(c)
    st = rep.get("text_style") or {}
    overlays = []
    dips = [b for b in rep["boundaries"] if b["type"] in ("fadeblack", "fadewhite")]
    lay = rep.get("layer") or {}
    if lay.get("use") and lay.get("file") and (dir_ / lay["file"]).exists():
        # the fixed design goes dark with the picture: one segment between dips, fading over half of each dip
        cuts = [0.0] + [b["start"] + b["dur"] / 2 for b in dips] + [rep["duration"]]
        half = [lay.get("fade_in", rep["fades"].get("in", 0.0))] + [b["dur"] / 2 for b in dips] + [rep["fades"].get("out", 0.0)]
        for j in range(len(cuts) - 1):
            overlays.append({"type": "image", "src": str((dir_ / lay["file"]).resolve()), "start": round(cuts[j], 4),
                             "end": round(cuts[j + 1], 4), "width": W, "x": 0, "y": 0, "anim": "none",
                             "fade_in": half[j], "fade_out": half[j + 1]})
    common = None
    if text and st.get("fit_width") and st.get("font"):               # one size for all texts: the longest line fits
        base = float(st.get("size") or 0.08); base = int(round(base * H)) if base < 1 else int(round(base * k))
        common = T.fit_size([t["text"] for t in rep.get("texts") or []], st["font"], base, float(st["fit_width"]) * W)
    for t in rep.get("texts") or [] if text else []:
        o = {"type": "text", **{k2: v for k2, v in st.items() if v is not None and k2 not in ("font_candidates", "fit_width")}, **t}
        if common and "size" not in t:
            o["size"] = common; o["nowrap"] = True
        elif o.get("size") and float(o["size"]) < 1:                    # size given as a fraction of the frame height
            o["size"] = int(round(float(o["size"]) * H))
        elif o.get("size"):
            o["size"] = int(round(float(o["size"]) * k))
        for b in dips:                                                  # words that change in a dip fade with it
            mid = b["start"] + b["dur"] / 2
            if "fade_in" not in t and abs(o["start"] - mid) <= max(0.35, b["dur"]):
                o["start"], o["fade_in"] = round(mid, 4), b["dur"] / 2
            if "fade_out" not in t and abs(o["end"] - mid) <= max(0.35, b["dur"]):
                o["end"], o["fade_out"] = round(mid, 4), b["dur"] / 2
        if "x" in t or "y" in t:                                        # centre of the block, as fractions
            o["x"] = f"{float(t.get('x', 0.5)):.4f}*W-w/2"
            o["y"] = f"{float(t.get('y', 0.5)):.4f}*H-h/2"
        overlays.append(o)
    au = rep.get("audio")
    audio = {"keep_clip_audio": False, "duck": "none"}
    if au:
        audio["voice"] = {"src": str((dir_ / au["file"]).resolve()), "start": 0}
        audio["lufs"] = float(np.clip(au.get("lufs") or -14.0, -24, -8))
    spec = {"size": f"{W}x{H}", "fps": fps, "background": "#000000", "clips": clips, "overlays": overlays, "audio": audio}
    sp = dir_ / "mimic.timeline.json"
    sp.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    raw = out.with_name(out.stem + ".raw" + out.suffix) if rep.get("fades", {}).get("in") or rep.get("fades", {}).get("out") else out
    trep = T.build(sp, raw, workers=workers)
    plan = planned_boundaries(trep)
    if raw != out:
        fi, fo = rep["fades"]["in"], rep["fades"]["out"]
        dur = A.probe(raw)["duration"]
        vf = ",".join(x for x in (f"fade=t=in:st=0:d={fi}" if fi else "", f"fade=t=out:st={dur - fo:.3f}:d={fo}" if fo else "") if x)
        subprocess.run([FF, "-y", "-v", "error", "-i", str(raw), "-vf", vf, "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(out)], check=True)
        raw.unlink(missing_ok=True)
    return compare(Path(rep["ref"]), out, dir_ / "compare", rep, plan)


# ───────────────────────── compare (the mimic gate) ─────────────────────────
PLAN_TYPE = {"fade": "dissolve", "fadeblack": "fadeblack", "fadewhite": "fadewhite", "slideleft": "slideleft",
             "slideright": "slideright", "slideup": "slideup", "slidedown": "slidedown", "wipeleft": "unknown"}


def planned_boundaries(trep: dict) -> list[dict]:
    """Where the timeline really put every boundary (its own report): xfades at their offsets, cuts at clip ends."""
    tr = {t["after_clip"]: t for t in trep.get("transitions") or []}
    out, t = [], 0.0
    clips = trep.get("clips") or []
    for i, c in enumerate(clips[:-1]):
        d = float(c["dur"])
        if i in tr:
            out.append({"start": round(tr[i]["at"], 4), "dur": tr[i]["dur"], "type": PLAN_TYPE.get(tr[i]["type"], "unknown")})
            t += d - tr[i]["dur"]
        else:
            t += d
            out.append({"start": round(t, 4), "dur": 0.0, "type": "cut"})
    return out


def _pcm(path: Path, rate: int = 8000) -> np.ndarray:
    r = subprocess.run([FF, "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", str(rate), "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(r.stdout, np.float32)


def compare(ref: Path, film: Path, out: Path, rep: dict | None = None, plan: list | None = None) -> dict:
    from PIL import Image
    out.mkdir(parents=True, exist_ok=True)
    ri, fi = A.probe(ref), A.probe(film)
    fps = ri["fps"] or 30.0
    rfr = frames(ref, 96, fps)
    rmed = frames(ref, 270, 4.0)
    ign = ignore_mask(np.stack([text_mask(f) for f in rmed]), rfr.shape[1:3]) if len(rmed) else None
    rb = boundaries(rfr, fps, ign)["boundaries"]
    ffr = frames(film, 96, fps)
    if ign is not None and ffr.shape[1:3] != rfr.shape[1:3]:
        import cv2
        ign = cv2.resize(ign.astype(np.uint8), (ffr.shape[2], ffr.shape[1]), interpolation=cv2.INTER_NEAREST) > 0
    fb = boundaries(ffr, fps, ign)["boundaries"]
    pairs, missing = [], []
    for b in rb:
        c = min(fb, key=lambda x: abs(x["start"] - b["start"]), default=None)
        if c is not None and abs(c["start"] - b["start"]) <= 0.25:
            pairs.append({"t": b["start"], "ref": b["type"], "film": c["type"], "frames_off": round((c["start"] - b["start"]) * fps, 1),
                          "dur_ref": b["dur"], "dur_film": c["dur"], "seen": "frames"})
            continue
        q = min(plan or [], key=lambda x: abs(x["start"] - b["start"]), default=None)
        if q is not None and abs(q["start"] - b["start"]) * fps <= 2 and (q["type"] == b["type"] or b["type"] == "unknown"):
            # two clips too alike for the detector to see the change: the timeline's own report placed it
            pairs.append({"t": b["start"], "ref": b["type"], "film": q["type"], "frames_off": round((q["start"] - b["start"]) * fps, 1),
                          "dur_ref": b["dur"], "dur_film": q["dur"], "seen": "plan"})
            continue
        missing.append(b)
    extra = [b for b in fb if all(abs(b["start"] - x["start"]) > 0.25 for x in rb)]
    a1, a2 = _pcm(ref), _pcm(film)
    corr, lag_ms = None, None
    if len(a1) > 800 and len(a2) > 800:
        n = min(len(a1), len(a2), 8000 * 60)
        x, y = a1[:n] - a1[:n].mean(), a2[:n] - a2[:n].mean()
        best = (-2.0, 0)
        for lag in range(-400, 401, 8):                                 # ±50 ms
            xs, ys = (x[lag:], y[:n - lag]) if lag >= 0 else (x[:n + lag], y[-lag:])
            c = float(np.dot(xs, ys) / (np.linalg.norm(xs) * np.linalg.norm(ys) + 1e-9))
            best = max(best, (c, lag))
        corr, lag_ms = round(best[0], 4), round(best[1] / 8.0, 1)
    times = sorted({round((s["own"][0] + s["own"][1]) / 2, 2) for s in (rep or {}).get("shots", [])} |
                   {round((t["start"] + t["end"]) / 2, 2) for t in (rep or {}).get("texts", [])}) or \
        [round(ri["duration"] * q, 2) for q in (0.1, 0.3, 0.5, 0.7, 0.9)]
    cells = []
    for t in times:
        still(ref, t, out / f"r_{t:.2f}.jpg"); still(film, t, out / f"f_{t:.2f}.jpg")
        cells.append(([Image.open(out / f"r_{t:.2f}.jpg"), Image.open(out / f"f_{t:.2f}.jpg")], f"{t:.2f}s  reference | new"))
    sheet(cells, out.parent / "compare.jpg", cols=4, cell_w=180)
    for p in out.glob("[rf]_*.jpg"):
        p.unlink()
    dur_off = round((fi["duration"] - ri["duration"]) * fps, 1)
    off = [abs(p["frames_off"]) for p in pairs]
    type_ok = sum(1 for p in pairs if p["ref"] == p["film"] or (p["ref"] == "unknown" and p["film"] in ("dissolve", "unknown")))
    checks = {
        "duration_within_2_frames": abs(dur_off) <= 2,
        "every_boundary_found": not missing,
        "boundaries_within_2_frames": all(o <= 2 for o in off),
        "transition_types_match": type_ok == len(pairs),
        "no_extra_boundaries": not extra,
        "audio_same": corr is None or (corr >= 0.95 and abs(lag_ms) <= 40),
    }
    res = {"ref": str(ref), "film": str(film), "fps": fps, "duration_offset_frames": dur_off, "boundaries": pairs,
           "missing": missing, "extra": extra, "mean_frames_off": round(float(np.mean(off)), 2) if off else 0.0,
           "seen_in_frames": sum(1 for p in pairs if p["seen"] == "frames"), "seen_in_plan_only": sum(1 for p in pairs if p["seen"] == "plan"),
           "audio": {"corr": corr, "lag_ms": lag_ms}, "checks": checks, "pass": all(checks.values()),
           "sheet": str(out.parent / "compare.jpg")}
    (out.parent / "compare.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    return res


# ───────────────────────── cli ─────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("study"); s.add_argument("ref"); s.add_argument("--out", default="")
    f = sub.add_parser("fonts"); f.add_argument("dir"); f.add_argument("--shot", type=int); f.add_argument("--top", type=int, default=12)
    m = sub.add_parser("match"); m.add_argument("dir"); m.add_argument("--pool", required=True)
    m.add_argument("--set", action="append", default=[]); m.add_argument("--strength", type=float, default=0.7)
    b = sub.add_parser("build"); b.add_argument("dir"); b.add_argument("--out", required=True)
    b.add_argument("--no-color", action="store_true"); b.add_argument("--no-text", action="store_true"); b.add_argument("--workers", type=int, default=0)
    l = sub.add_parser("layer"); l.add_argument("dir"); l.add_argument("--erase", action="append", default=[])
    l.add_argument("--snap", action="append", default=[], help="x0,y0,x1,y1@SHOT[:hmin,hmax,smin,vmin] — a moving element taken from one shot (OpenCV HSV gate)")
    c = sub.add_parser("compare"); c.add_argument("ref"); c.add_argument("film"); c.add_argument("--out", default="")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if a.cmd == "study":
        ref = Path(a.ref)
        rep = study(ref, Path(a.out) if a.out else ref.with_name(ref.stem + "_mimic"))
        print(json.dumps({"shots": len(rep["shots"]), "boundaries": [(b["start"], b["type"], b["dur"]) for b in rep["boundaries"]],
                          "fades": rep["fades"], "text_events": rep["text_events"], "audio": rep["audio"],
                          "dir": str(Path(a.out) if a.out else ref.with_name(ref.stem + "_mimic"))}, ensure_ascii=False, indent=1))
    elif a.cmd == "fonts":
        r = fonts(Path(a.dir), a.shot, a.top)
        print(json.dumps({"sheet": r["sheet"], "top": [(t["name"], t["score"]) for t in r["top"]]}, ensure_ascii=False, indent=1))
    elif a.cmd == "layer":
        boxes = [[float(v) for v in e.split(",")] for e in a.erase] or None
        snaps = []
        for sv in a.snap:
            box, _, rest = sv.partition("@"); shot, _, hsv = rest.partition(":")
            snaps.append({"box": [float(v) for v in box.split(",")], "shot": int(shot), **({"hsv": [int(v) for v in hsv.split(",")]} if hsv else {})})
        print(json.dumps(layer(Path(a.dir), boxes, snaps or None), ensure_ascii=False, indent=1))
    elif a.cmd == "match":
        r = match(Path(a.dir), Path(a.pool), a.set, a.strength)
        print(json.dumps([(p["shot"], Path(p["file"]).name, p["in"], p["speed"], p["cost"]) for p in r["picks"]], ensure_ascii=False, indent=1))
    elif a.cmd == "build":
        r = build(Path(a.dir), Path(a.out), not a.no_color, not a.no_text, a.workers)
        print(json.dumps({k: r[k] for k in ("pass", "checks", "duration_offset_frames", "mean_frames_off", "audio", "sheet")}, ensure_ascii=False, indent=1))
        return 0 if r["pass"] else 3
    elif a.cmd == "compare":
        film = Path(a.film)
        r = compare(Path(a.ref), film, Path(a.out) if a.out else film.with_name(film.stem + "_compare") / "frames")
        print(json.dumps({k: r[k] for k in ("pass", "checks", "duration_offset_frames", "mean_frames_off", "audio", "sheet")}, ensure_ascii=False, indent=1))
        return 0 if r["pass"] else 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
