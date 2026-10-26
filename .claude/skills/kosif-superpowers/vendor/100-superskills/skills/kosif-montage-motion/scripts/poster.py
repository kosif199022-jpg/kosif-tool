"""The poster: the strongest settled frame of a film, saved as a JPEG and (with --bake) written into frame 0, because
almost every player and platform (Slack, X, Discord, WhatsApp) takes its idle thumbnail from frame 0 and ignores cover
metadata. Only frame 0's pixels change: same frame count, same duration, sound copied. Idea from /brag (MIT,
latent-spaces/brag), step 4.

    python scripts/kmotion.py poster FILM.mp4                    pick the frame by itself → FILM.poster.jpg
    python scripts/kmotion.py poster FILM.mp4 --at 3.2 --bake    a frame you chose, baked as frame 0 (FILM is replaced)
    python scripts/kmotion.py poster FILM.mp4 --bake --out OUT.mp4

Picking (when --at is not given): frames sampled at 8 fps; each scored by detail (Laplacian variance), contrast and
stillness against its neighbours (a settled frame: text fully in, not mid-transition), never the first 0.4 s or the
last 0.3 s, never a near-black frame. You know the film's strongest beat better — pass --at when you do.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

FF = shutil.which("ffmpeg") or "ffmpeg"
FP = shutil.which("ffprobe") or "ffprobe"


def probe(film: Path) -> dict:
    r = subprocess.run([FP, "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,nb_read_packets,r_frame_rate:format=duration", "-of", "json", str(film)],
                       capture_output=True, text=True, check=True)
    d = json.loads(r.stdout); s = d["streams"][0]
    num, den = (int(x) for x in s["r_frame_rate"].split("/"))
    return {"w": int(s["width"]), "h": int(s["height"]), "frames": int(s.get("nb_read_packets") or 0),
            "fps": num / den, "duration": float(d["format"]["duration"])}


def _frames(film: Path, fps: float = 8.0, width: int = 320):
    info = probe(film)
    h = int(round(info["h"] * width / info["w"] / 2) * 2)
    r = subprocess.run([FF, "-v", "error", "-i", str(film), "-vf", f"fps={fps},scale={width}:{h},format=gray", "-f", "rawvideo", "-"],
                       capture_output=True, check=True)
    arr = np.frombuffer(r.stdout, np.uint8)
    n = arr.size // (width * h)
    return arr[: n * width * h].reshape(n, h, width).astype(np.float32), fps, info


def pick(film: Path) -> dict:
    fr, fps, info = _frames(film)
    n = len(fr)
    if n == 0:
        raise SystemExit(f"{film}: no frames")
    lap = lambda f: (f[1:-1, 1:-1] * 4 - f[:-2, 1:-1] - f[2:, 1:-1] - f[1:-1, :-2] - f[1:-1, 2:]).var()  # noqa: E731
    rows = []
    for i in range(n):
        t = i / fps
        if t < 0.4 or t > info["duration"] - 0.3:
            continue
        f = fr[i]
        mean = float(f.mean())
        if mean < 12:
            continue
        motion = np.mean([np.abs(f - fr[j]).mean() for j in (i - 1, i + 1) if 0 <= j < n] or [0.0])
        detail, contrast = float(np.log1p(lap(f))), float(f.std())
        score = detail * contrast / (1.0 + motion / 2.0)
        rows.append({"t": round(t, 3), "score": round(float(score), 2), "detail": round(detail, 2), "contrast": round(contrast, 1), "motion": round(float(motion), 2)})
    if not rows:
        rows = [{"t": round(info["duration"] / 2, 3), "score": 0, "detail": 0, "contrast": 0, "motion": 0}]
    rows.sort(key=lambda r: -r["score"])
    return {"t": rows[0]["t"], "top": rows[:5], "film": info}


def extract(film: Path, t: float, out: Path) -> Path:
    subprocess.run([FF, "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(film), "-frames:v", "1", "-q:v", "2", str(out)], check=True)
    return out


def bake(film: Path, poster: Path, out: Path) -> dict:
    """Frame 0 := the poster. Every other frame and all timing untouched; the sound is copied."""
    before = probe(film)
    tmp = out.with_suffix(".baking.mp4")
    subprocess.run([FF, "-y", "-v", "error", "-i", str(film), "-i", str(poster), "-filter_complex",
                    "[1:v]scale=iw:ih[p];[0:v][p]overlay=0:0:enable='eq(n,0)',format=yuv420p[v]", "-map", "[v]", "-map", "0:a?",
                    "-c:v", "libx264", "-crf", "12", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
                    str(tmp)], check=True)
    after = probe(tmp)
    if after["frames"] != before["frames"] or abs(after["duration"] - before["duration"]) > 1.5 / max(1.0, before["fps"]):
        tmp.unlink(missing_ok=True)
        raise SystemExit(f"bake changed the film ({before['frames']}→{after['frames']} frames, {before['duration']}→{after['duration']} s): kept the original")
    tmp.replace(out)
    return {"frames": after["frames"], "duration": after["duration"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("film"); ap.add_argument("--at", type=float, help="the second to use (default: picked)")
    ap.add_argument("--jpg", help="poster file (default FILM.poster.jpg)"); ap.add_argument("--bake", action="store_true", help="write the poster into frame 0")
    ap.add_argument("--out", help="baked film (default: replace FILM)")
    a = ap.parse_args()
    film = Path(a.film)
    rep: dict = {"film": str(film)}
    if a.at is None:
        p = pick(film); rep.update({"picked": True, "t": p["t"], "candidates": p["top"]})
    else:
        rep.update({"picked": False, "t": a.at})
    jpg = Path(a.jpg) if a.jpg else film.with_suffix(".poster.jpg")
    rep["poster"] = str(extract(film, rep["t"], jpg))
    if a.bake:
        out = Path(a.out) if a.out else film
        rep["baked"] = {"out": str(out), **bake(film, jpg, out)}
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
