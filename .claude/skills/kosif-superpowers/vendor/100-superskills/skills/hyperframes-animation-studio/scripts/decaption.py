"""KOSIF decaption — erase burned-in subtitles (and a fixed credit line) from a video, measured, not guessed.

    python decaption.py VIDEO --out CLEAN.mp4 [--band 0.45:0.56] [--keep-credit] [--report]

How (each step learned on a real reel):
1. Ink: caption strokes are near-white or saturated yellow AND sit within a few pixels of a black outline; the scene
   (sky, skin, shirts, railings) almost never combines the two.
2. Band: the rows where ink appears across the clip (found automatically unless --band is given).
3. Credit: pixels inside the band that are white in most frames = a fixed watermark/credit line (erased unless
   --keep-credit; credit the source in your own typography instead).
4. Shots: cut detection; a shot whose picture barely moves outside the band is "locked off".
5. Locked-off shots: every band pixel is uncovered in some frame (captions change) → rebuild it from the per-pixel
   median of its uncovered samples — the real background, no smear. Pixels never uncovered are inpainted.
6. Moving shots (talking heads): inpaint the strokes. Only runs as wide as a caption line count (≥ 22 % of the frame
   width): teeth next to a dark mouth look exactly like ink and must never be erased.
7. Fades: masks are carried ±3 frames so a caption that dims in or out is still removed.
Limits: where a caption crossed a mouth, the inpainted lip can look soft; a learned video-inpainting model does better.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

FF = shutil.which("ffmpeg") or "ffmpeg"


def ink(region: np.ndarray, min_run: int) -> np.ndarray:
    """Caption-stroke mask (uint8 0/1) of a BGR region, grown over the outline and the codec halo."""
    hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
    v, s, h = hsv[..., 2].astype(np.int16), hsv[..., 1].astype(np.int16), hsv[..., 0].astype(np.int16)
    white = (v > 205) & (s < 55)
    yellow = (h > 16) & (h < 38) & (s > 110) & (v > 150)
    near_dark = cv2.dilate((v < 70).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))) > 0
    core = ((white | yellow) & near_dark).astype(np.uint8)
    line = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_RECT, (31, 13)))       # letters and dots join their line
    n, lab, st, _ = cv2.connectedComponentsWithStats(line)
    ok = np.zeros(n, bool)
    ok[1:] = st[1:, 2] >= min_run
    core &= ok[lab].astype(np.uint8)
    return cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))


def _frames(path: Path):
    cap = cv2.VideoCapture(str(path))
    while True:
        ok, f = cap.read()
        if not ok:
            break
        yield f


def analyse(path: Path, band: tuple[float, float] | None = None) -> dict:
    cap = cv2.VideoCapture(str(path))
    W, H, fps = int(cap.get(3)), int(cap.get(4)), cap.get(5) or 30.0
    rows = np.zeros(H, np.float64)
    prev_small, diffs, motion, lum = None, [], [], []
    for i, f in enumerate(_frames(path)):
        small = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (90, 160)).astype(np.float32)
        lum.append(float(small.mean()))
        diffs.append(0.0 if prev_small is None else float(np.abs(small - prev_small).mean()))
        prev_small = small
        if band is None and i % 3 == 0:
            rows += ink(f, 45).sum(axis=1)
    n = len(diffs)
    if band is None:
        r = np.convolve(rows, np.ones(9) / 9, mode="same")
        hot = r > max(1e-9, r.max()) * 0.12
        ys = np.flatnonzero(hot)
        if len(ys) == 0:
            return {"W": W, "H": H, "fps": fps, "frames": n, "band": None}
        y0, y1 = max(0, int(ys.min()) - 14), min(H, int(ys.max()) + 14)
    else:
        y0, y1 = int(band[0] * H), int(band[1] * H)
    d = np.asarray(diffs)
    thr = max(12.0, float(np.median(d)) * 6)
    # a cut: a local maximum far above its neighbourhood (codecs often spread one cut over two frames)
    cuts = [0]
    for i in range(1, n):
        lo, hi = max(1, i - 15), min(n, i + 16)
        around = np.median(np.r_[d[lo:max(lo, i - 2)], d[min(hi, i + 3):hi]]) if hi - lo > 6 else np.median(d)
        if d[i] > thr and d[i] >= d[i - 1] and (i + 1 >= n or d[i] >= d[i + 1]) and d[i] > 4 * max(around, 0.5) and i - cuts[-1] > 5:
            cuts.append(i)
    cuts.append(n)
    shots = [(cuts[k], cuts[k + 1]) for k in range(len(cuts) - 1) if cuts[k + 1] - cuts[k] > 0]
    return {"W": W, "H": H, "fps": fps, "frames": n, "band": [y0, y1], "shots": shots, "lum": lum}


def decaption(src: Path, out: Path, band: tuple[float, float] | None = None, keep_credit: bool = False) -> dict:
    src, out = Path(src), Path(out)
    A = analyse(src, band)
    if A["band"] is None:
        shutil.copy2(src, out)
        return {"file": str(out), "captions": False}
    W, H, fps, n = A["W"], A["H"], A["fps"], A["frames"]
    y0, y1 = A["band"]
    talk_run = max(60, int(0.22 * W))
    # pass 1: band crops, per-frame masks, credit frequency, per-shot motion outside the band
    crops, masks = [], []
    white_freq = np.zeros((y1 - y0, W), np.float32); bright = 0
    outside = []
    prev_out = None
    for f in _frames(src):
        b = f[y0:y1]
        crops.append(b.copy())
        masks.append(ink(b, 45))
        if f.mean() > 12:
            hsv = cv2.cvtColor(b, cv2.COLOR_BGR2HSV)
            white_freq += ((hsv[..., 2] > 185) & (hsv[..., 1] < 60)); bright += 1
        o = cv2.resize(cv2.cvtColor(np.vstack([f[:y0], f[y1:]]), cv2.COLOR_BGR2GRAY), (60, 100)).astype(np.float32)
        outside.append(0.0 if prev_out is None else float(np.abs(o - prev_out).mean()))
        prev_out = o
    credit = np.zeros((y1 - y0, W), np.uint8)
    if not keep_credit and bright:
        c = (white_freq / bright > 0.55).astype(np.uint8)
        k, lab, st, _ = cv2.connectedComponentsWithStats(c)
        for i in range(1, k):
            if st[i, 3] <= 45 and st[i, 4] < 0.05 * c.size:
                credit[lab == i] = 1
        credit = cv2.dilate(credit, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    # moving shots: re-detect with the caption-line width rule (teeth are never a caption line)
    plan = []
    for a, b in A["shots"]:
        moving = float(np.median(outside[a + 1:b] or [0])) > 1.2
        plan.append({"from": a, "to": b, "locked": not moving})
        if moving:
            for i in range(a, b):
                masks[i] = ink(crops[i], talk_run)
    # fades: carry each mask ±3 frames within its shot
    carried = [m.copy() for m in masks]
    for p in plan:
        for i in range(p["from"], p["to"]):
            for j in range(max(p["from"], i - 3), min(p["to"], i + 4)):
                carried[i] |= masks[j]
    # fades: while a shot dims, the caption dims with it below the ink threshold — use its shape from the last bright frames
    for p in plan:
        ids = list(range(p["from"], p["to"]))
        ref = float(np.median([A["lum"][i] for i in ids])) if ids else 0
        bright = [i for i in ids if A["lum"][i] >= 0.85 * ref]
        for i in ids:
            if A["lum"][i] < 0.85 * ref and bright:
                near = sorted(bright, key=lambda j: abs(j - i))[:24]
                for j in near:
                    carried[i] |= masks[j]
    # locked shots: the band rebuilt from uncovered samples
    plates = {}
    for k, p in enumerate(plan):
        if not p["locked"]:
            continue
        idx = [i for i in range(p["from"], p["to"]) if A["lum"][i] > 12]
        if len(idx) < 8:
            continue
        stack = np.stack([crops[i] for i in idx]).astype(np.float32)
        cover = np.stack([(carried[i] > 0) | (credit > 0) for i in idx])
        with np.errstate(all="ignore"), __import__("warnings").catch_warnings():
            __import__("warnings").simplefilter("ignore")
            plate = np.nanmedian(np.where(cover[..., None], np.nan, stack), axis=0)        # NaN where never uncovered (expected)
        never = np.isnan(plate[..., 0])
        plates[k] = (np.nan_to_num(plate).astype(np.uint8), never, float(np.mean([A["lum"][i] for i in idx])))
    # pass 2: write
    tmp = out.with_suffix(".video.mp4")
    ff = subprocess.Popen([FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps:.5f}", "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-pix_fmt", "yuv420p", str(tmp)], stdin=subprocess.PIPE)
    shot_of = np.zeros(n, int)
    for k, p in enumerate(plan):
        shot_of[p["from"]:p["to"]] = k
    for i, f in enumerate(_frames(src)):
        m = ((carried[i] > 0) | (credit > 0))
        if m.any() and f.mean() > 2:
            k = shot_of[i]
            band_img = f[y0:y1]
            rest = m.copy()
            if k in plates:
                plate, never, lum0 = plates[k]
                gain = min(1.5, A["lum"][i] / max(1.0, lum0))
                use = m & ~never
                band_img[use] = np.clip(plate[use].astype(np.float32) * gain, 0, 255).astype(np.uint8)
                rest = m & never
            if rest.any():
                full = np.zeros((H, W), np.uint8); full[y0:y1] = rest.astype(np.uint8) * 255
                f = cv2.inpaint(f, full, 9, cv2.INPAINT_TELEA)
        # leftover specks of the yellow accent (skin is never this saturated): a last tiny inpaint
        hsv = cv2.cvtColor(f[y0:y1], cv2.COLOR_BGR2HSV)
        yl = ((hsv[..., 0] > 16) & (hsv[..., 0] < 38) & (hsv[..., 1] > 120) & (hsv[..., 2] > 140)).astype(np.uint8)
        wh = ((hsv[..., 2] > 200) & (hsv[..., 1] < 55)).astype(np.uint8)          # lone letter dots: tiny isolated white blobs
        k, lab, st, _ = cv2.connectedComponentsWithStats(wh)
        small = np.zeros(k, bool); small[1:] = st[1:, 4] <= 24
        yl |= (small[lab] & (cv2.dilate((carried[i] > 0).astype(np.uint8), np.ones((15, 15), np.uint8)) > 0)).astype(np.uint8)
        if yl.any() and yl.sum() < 400:
            full = np.zeros((H, W), np.uint8); full[y0:y1] = cv2.dilate(yl, np.ones((5, 5), np.uint8)) * 255
            f = cv2.inpaint(f, full, 4, cv2.INPAINT_TELEA)
        ff.stdin.write(f.tobytes())
    ff.stdin.close(); ff.wait()
    subprocess.run([FF, "-y", "-v", "error", "-i", str(tmp), "-i", str(src), "-map", "0:v", "-map", "1:a?", "-c:v", "copy", "-c:a", "copy",
                    "-shortest", str(out)], check=True)
    tmp.unlink(missing_ok=True)
    return {"file": str(out), "captions": True, "band": [y0, y1], "shots": plan, "credit_pixels": int(credit.sum())}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video"); ap.add_argument("--out", required=True); ap.add_argument("--band", help="y0:y1 as fractions of the height")
    ap.add_argument("--keep-credit", action="store_true")
    a = ap.parse_args()
    band = tuple(float(x) for x in a.band.split(":")) if a.band else None
    rep = decaption(Path(a.video), Path(a.out), band, a.keep_credit)
    print(json.dumps(rep, ensure_ascii=False))


if __name__ == "__main__":
    main()
