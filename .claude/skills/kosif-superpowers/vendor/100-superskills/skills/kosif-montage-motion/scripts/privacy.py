"""KOSIF privacy — faces (or any region) pixelated, blurred or boxed before a clip is published; tracked across frames,
expanded by a margin, held through short misses; the sound is kept untouched.

    python privacy.py CLIP.mp4 --out safe.mp4 [--mode pixelate|blur|box] [--strength 18] [--pad 0.25]
    python privacy.py CLIP.mp4 --out safe.mp4 --region 0.55,0.1,0.3,0.3            a fixed region (x,y,w,h as fractions or pixels)
    python privacy.py CLIP.mp4 --out safe.mp4 --region 120,80,300,300,2.0,6.5      ... only between 2.0 s and 6.5 s
    python privacy.py CLIP.mp4 --out safe.mp4 --no-faces --region ...               regions only, no detection

Detection: faces.py (YuNet DNN when its model is present, Haar when the build has it, else the skin heuristic — the
report says which). A face that disappears for less than `--hold` seconds keeps its mask. Nothing is fabricated: the
mask covers what the detector found plus the margin; review the frames (kmotion sheet) before publishing.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

import faces  # noqa: E402
import tools  # noqa: E402

FF = tools.FF


class _Encoder:
    def __init__(self, out: Path, w: int, h: int, fps: float, crf: int = 17):
        self.p = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", f"{fps:.4f}",
                                   "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)],
                                  stdin=subprocess.PIPE, bufsize=w * h * 3 * 4)
        self.n = 0

    def frame(self, rgb: np.ndarray):
        self.p.stdin.write(np.ascontiguousarray(rgb).tobytes()); self.n += 1

    def close(self):
        self.p.stdin.close()
        if self.p.wait() != 0:
            raise RuntimeError(f"ffmpeg encoder failed after {self.n} frames")


# ───────────────────────── the masks ─────────────────────────
def pixelate(frame: np.ndarray, box: tuple[int, int, int, int], block: int = 18) -> None:
    x, y, w, h = box
    roi = frame[y:y + h, x:x + w]
    if roi.size == 0:
        return
    bh, bw = max(1, h // max(1, block)), max(1, w // max(1, block))
    hh, ww = (h // bh) * bh, (w // bw) * bw
    sub = roi[:hh, :ww].reshape(bh, hh // bh, bw, ww // bw, 3).mean(axis=(1, 3))
    up = np.repeat(np.repeat(sub, hh // bh, axis=0), ww // bw, axis=1).astype(np.uint8)
    roi[:hh, :ww] = up
    if hh < h:
        roi[hh:, :ww] = up[-1:, :]
    if ww < w:
        roi[:, ww:] = roi[:, ww - 1:ww]


def blur(frame: np.ndarray, box: tuple[int, int, int, int], strength: int = 18) -> None:
    x, y, w, h = box
    roi = frame[y:y + h, x:x + w]
    if roi.size == 0:
        return
    try:
        import cv2
        k = max(3, (strength * 2) | 1)
        frame[y:y + h, x:x + w] = cv2.GaussianBlur(roi, (k, k), 0)
    except ImportError:
        from scipy import ndimage
        frame[y:y + h, x:x + w] = ndimage.gaussian_filter(roi, sigma=(strength / 2, strength / 2, 0)).astype(np.uint8)


def box_fill(frame: np.ndarray, box: tuple[int, int, int, int], colour=(20, 20, 20)) -> None:
    x, y, w, h = box
    frame[y:y + h, x:x + w] = colour


def _expand(b, pad: float, W: int, H: int) -> tuple[int, int, int, int]:
    x, y, w, h = b[:4]
    dx, dy = w * pad, h * pad * 1.25                            # a little more above and below (hair, chin)
    x0, y0 = int(max(0, x - dx)), int(max(0, y - dy))
    x1, y1 = int(min(W, x + w + dx)), int(min(H, y + h + dy))
    return x0, y0, max(2, x1 - x0), max(2, y1 - y0)


def _iou(a, b) -> float:
    ax0, ay0, aw, ah = a; bx0, by0, bw, bh = b
    ix = max(0, min(ax0 + aw, bx0 + bw) - max(ax0, bx0)); iy = max(0, min(ay0 + ah, by0 + bh) - max(ay0, by0))
    inter = ix * iy
    return inter / float(aw * ah + bw * bh - inter + 1e-6)


def parse_region(s: str, W: int, H: int) -> dict:
    v = [float(p) for p in s.split(",")]
    if len(v) not in (4, 6):
        raise ValueError("--region x,y,w,h[,start,end]")
    x, y, w, h = v[:4]
    if all(0 <= q <= 1 for q in (x, y, w, h)):
        x, y, w, h = x * W, y * H, w * W, h * H
    return {"box": (int(x), int(y), int(w), int(h)), "start": v[4] if len(v) == 6 else 0.0, "end": v[5] if len(v) == 6 else 1e9}


# ───────────────────────── the pass ─────────────────────────
def anonymize(src: Path, out: Path, mode: str = "pixelate", strength: int = 18, pad: float = 0.25, every: int = 2, hold: float = 0.6,
              regions: list[dict] | None = None, detect_faces: bool = True, min_frac: float = 0.004) -> dict:
    src, out = Path(src), Path(out)
    info = tools.probe(src)
    W, H, fps = info["video"]["w"], info["video"]["h"], info["video"]["fps"]
    tmp = Path(tempfile.mkdtemp(prefix="kosif_privacy_"))
    vid = tmp / "video.mp4"
    dec = subprocess.Popen([FF, "-v", "error", "-i", str(src), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, bufsize=W * H * 3 * 4)
    enc = _Encoder(vid, W, H, fps)
    apply = {"pixelate": lambda f, b: pixelate(f, b, max(4, strength)), "blur": lambda f, b: blur(f, b, max(3, strength)), "box": lambda f, b: box_fill(f, b)}[mode]
    tracks: list[dict] = []                                      # {"box", "last": t, "n": hits}
    hold_frames = max(1, int(round(hold * fps)))
    n, found = 0, 0
    step = max(1, W // 480)                                     # detect on a ≤ 480 px wide copy, scale the boxes back
    try:
        while True:
            buf = dec.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                break
            frame = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
            t = n / fps
            if detect_faces and n % every == 0:
                small = frame[::step, ::step] if step > 1 else frame
                dets = [(x * step, y * step, w * step, h * step) for (x, y, w, h, _) in faces.detect(small, min_frac)]
                found += len(dets)
                for d in dets:
                    best = max(tracks, key=lambda tr: _iou(tr["box"], d), default=None)
                    if best and _iou(best["box"], d) > 0.25:
                        bx = tuple(int(0.6 * a + 0.4 * b) for a, b in zip(best["box"], d))     # settle, do not jitter
                        best.update(box=bx, last=n, n=best["n"] + 1)
                    else:
                        tracks.append({"box": d, "last": n, "n": 1})
            tracks = [tr for tr in tracks if n - tr["last"] <= hold_frames]
            for tr in tracks:
                apply(frame, _expand(tr["box"], pad, W, H))
            for rg in regions or []:
                if rg["start"] <= t <= rg["end"]:
                    x, y, w, h = rg["box"]
                    apply(frame, (max(0, x), max(0, y), min(W - max(0, x), w), min(H - max(0, y), h)))
            enc.frame(frame)
            n += 1
    finally:
        dec.stdout.close(); dec.wait()
        enc.close()
    out.parent.mkdir(parents=True, exist_ok=True)
    if info["audio"]:
        tools._run([FF, "-y", "-v", "error", "-i", str(vid), "-i", str(src), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(out)])
    else:
        shutil.copy2(vid, out)
    shutil.rmtree(tmp, ignore_errors=True)
    rep = {"file": str(out), "frames": n, "mode": mode, "detector": faces.which() if detect_faces else "none", "detections": found,
           "regions": len(regions or []), "pad": pad, "hold_s": hold, "size": f"{W}x{H}", "fps": fps,
           "note": "the mask covers what the detector found plus the margin; review frames before publishing"}
    out.with_suffix(".privacy.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clip"); ap.add_argument("--out", required=True)
    ap.add_argument("--mode", default="pixelate", choices=["pixelate", "blur", "box"])
    ap.add_argument("--strength", type=int, default=18, help="pixel block size / blur radius")
    ap.add_argument("--pad", type=float, default=0.25, help="margin around each face as a share of its size")
    ap.add_argument("--every", type=int, default=2, help="detect on every N-th frame")
    ap.add_argument("--hold", type=float, default=0.6, help="seconds a mask survives a missed detection")
    ap.add_argument("--region", action="append", default=[], help="x,y,w,h[,start,end] (fractions or pixels); repeatable")
    ap.add_argument("--no-faces", action="store_true", help="skip detection, mask the given regions only")
    ap.add_argument("--min-face", type=float, default=0.004, help="smallest face as a share of the frame area")
    a = ap.parse_args()
    info = tools.probe(Path(a.clip))
    regions = [parse_region(r, info["video"]["w"], info["video"]["h"]) for r in a.region]
    if a.no_faces and not regions:
        ap.error("--no-faces needs at least one --region")
    rep = anonymize(Path(a.clip), Path(a.out), a.mode, a.strength, a.pad, a.every, a.hold, regions, not a.no_faces, a.min_face)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
