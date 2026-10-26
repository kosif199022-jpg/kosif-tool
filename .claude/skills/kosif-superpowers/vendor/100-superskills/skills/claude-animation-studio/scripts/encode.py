#!/usr/bin/env python3
"""يجمّع إطارات PNG إلى MP4 (H.264 yuv420p) بـ ffmpeg، ويدمج الصوت إن وُجد، ويبني لوحة تحقق contact-sheet.png.

usage:
  python encode.py --frames frames --fps 30 --out video.mp4 [--audio soundtrack.wav] [--crf 18] [--sheet 12]
  python encode.py --frames frames --fps 30 --out video.mp4 --gif preview.gif   # GIF معاينة مصغّر أيضاً

لوحة التحقق تحتاج Pillow (pip install pillow)؛ بدونها يُبنى الفيديو فقط.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg failed:\n{' '.join(cmd)}\n{r.stderr[-2000:]}")


def contact_sheet(frames: list[Path], out: Path, n: int, cols: int = 4) -> bool:
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return False
    if not frames:
        return False
    step = max(1, len(frames) // n)
    picks = frames[::step][:n]
    first = Image.open(picks[0])
    tw = 360
    th = int(first.height * tw / first.width)
    rows = (len(picks) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 8, rows * (th + 28) + 8), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    for i, p in enumerate(picks):
        im = Image.open(p).convert("RGB").resize((tw, th))
        x = 8 + (i % cols) * (tw + 8)
        y = 8 + (i // cols) * (th + 28)
        sheet.paste(im, (x, y))
        d.text((x + 4, y + th + 6), p.stem, fill=(230, 230, 230))
    sheet.save(out)
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", default="frames")
    ap.add_argument("--pattern", default="f_%04d.png")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--out", default="video.mp4")
    ap.add_argument("--audio", default="")
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--sheet", type=int, default=12, help="عدد الإطارات في لوحة التحقق (0 لتعطيلها)")
    ap.add_argument("--gif", default="")
    a = ap.parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg غير موجود في PATH")
    frames_dir = Path(a.frames)
    frames = sorted(frames_dir.glob("f_*.png"))
    if not frames:
        sys.exit(f"لا إطارات في {frames_dir}")
    out = Path(a.out)

    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(a.fps), "-i", str(frames_dir / a.pattern)]
    if a.audio:
        cmd += ["-i", a.audio, "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", str(a.crf), "-preset", "slow", "-movflags", "+faststart",
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", str(out)]
    run(cmd)

    if a.gif:
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(out), "-vf",
             "fps=12,scale=360:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse", a.gif])

    sheet_ok = False
    if a.sheet:
        sheet_ok = contact_sheet(frames, out.with_name("contact-sheet.png"), a.sheet)

    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=width,height,r_frame_rate,nb_frames,codec_name,pix_fmt", "-of", "json", str(out)],
                           capture_output=True, text=True)
    info = json.loads(probe.stdout)["streams"][0] if probe.returncode == 0 else {}
    report = {"out": str(out), "bytes": out.stat().st_size, "frames_in": len(frames), "fps": a.fps,
              "duration_s": round(len(frames) / a.fps, 2), "audio": bool(a.audio), "contact_sheet": sheet_ok, "stream": info}
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
