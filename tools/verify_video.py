#!/usr/bin/env python3
"""Delivery gate: verify a rendered video against the request and fill TEST_REPORT values.

Checks with ffprobe/ffmpeg (both must be on PATH):
  - container and codecs (H.264 + AAC expected by default)
  - width × height and aspect ratio
  - frame rate and frame count versus the requested duration
  - audio stream presence, channels, sample rate
  - integrated loudness (EBU R128) and true peak, versus a target (default -14 LUFS)
  - optional: the delivered audio duration matches a supplied master audio file (±50 ms)

Usage:
  python3 tools/verify_video.py film.mp4 --aspect 9:16 --fps 30 --duration 15 [--audio voice.mp3] [--lufs -14] [--json report.json]
Exit code 1 when any check fails.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aspects import ratio_of  # noqa: E402  (any W:H, WxH or name)


def probe(path: str) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-count_frames", "-of", "json", path], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def loudness(path: str) -> dict | None:
    try:
        out = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    except FileNotFoundError:
        return None
    text = out.stderr
    i = text.rfind("Integrated loudness")
    if i < 0:
        return None
    tail = text[i:]
    li = re.search(r"I:\s*(-?[\d.]+) LUFS", tail)
    lra = re.search(r"LRA:\s*(-?[\d.]+) LU", tail)
    peak = re.search(r"Peak:\s*(-?[\d.]+) dBFS", tail)
    return {"integrated_lufs": float(li.group(1)) if li else None, "lra": float(lra.group(1)) if lra else None, "true_peak_dbfs": float(peak.group(1)) if peak else None}


def frac(s: str) -> float:
    if "/" in s:
        a, b = s.split("/")
        return float(a) / float(b) if float(b) else 0.0
    return float(s)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--aspect", help="any ratio: 9:16, 21:9, 2.35:1, 1920x816, reel, cinema…")
    ap.add_argument("--fps", type=float)
    ap.add_argument("--duration", type=float, help="expected duration in seconds")
    ap.add_argument("--audio", help="master audio file whose duration the video must match")
    ap.add_argument("--lufs", type=float, default=-14.0, help="target integrated loudness (±1.5 LU accepted)")
    ap.add_argument("--no-audio", action="store_true", help="the deliverable is intentionally silent")
    ap.add_argument("--json", help="write the report as JSON here")
    args = ap.parse_args()
    for tool in ("ffprobe", "ffmpeg"):
        if not shutil.which(tool):
            print(f"{tool} not found on PATH", file=sys.stderr)
            return 2

    info = probe(args.video)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    checks: list[tuple[str, bool, str]] = []
    report: dict = {"file": args.video}
    if not v:
        print("no video stream", file=sys.stderr)
        return 1
    w, h = int(v["width"]), int(v["height"])
    fps = frac(v.get("avg_frame_rate") or v.get("r_frame_rate") or "0")
    frames = int(v.get("nb_read_frames") or v.get("nb_frames") or 0)
    dur = float(info["format"].get("duration") or 0)
    report.update({"codec": v.get("codec_name"), "width": w, "height": h, "fps": round(fps, 3), "frames": frames, "duration_s": round(dur, 3), "pix_fmt": v.get("pix_fmt")})
    checks.append(("video codec is H.264", v.get("codec_name") == "h264", v.get("codec_name", "?")))
    checks.append(("pixel format is 4:2:0 8-bit (universal playback)", v.get("pix_fmt") in ("yuv420p", "yuvj420p"), v.get("pix_fmt", "?")))
    checks.append(("even dimensions", w % 2 == 0 and h % 2 == 0, f"{w}x{h}"))
    if args.aspect:
        checks.append((f"aspect is {args.aspect}", abs(w / h - ratio_of(args.aspect)) < 0.01, f"{w}x{h} = {w / h:.3f}"))
    if args.fps:
        checks.append((f"frame rate is {args.fps:g}", abs(fps - args.fps) < 0.05, f"{fps:.3f}"))
    if args.duration:
        checks.append((f"duration is {args.duration:g} s (±1 frame)", abs(dur - args.duration) <= (1 / fps if fps else 0.05) + 0.001, f"{dur:.3f} s"))
        if fps:
            checks.append(("frame count matches duration × fps", abs(frames - round(args.duration * fps)) <= 1, f"{frames} frames"))
    if args.no_audio:
        checks.append(("no audio stream (silent deliverable)", a is None, "present" if a else "absent"))
    else:
        checks.append(("audio stream present", a is not None, a.get("codec_name", "?") if a else "absent"))
        if a:
            report.update({"audio_codec": a.get("codec_name"), "channels": a.get("channels"), "sample_rate": a.get("sample_rate")})
            checks.append(("audio codec is AAC", a.get("codec_name") == "aac", a.get("codec_name", "?")))
            checks.append(("sample rate ≥ 44.1 kHz", int(a.get("sample_rate") or 0) >= 44100, str(a.get("sample_rate"))))
            lu = loudness(args.video)
            if lu:
                report["loudness"] = lu
                if lu.get("integrated_lufs") is not None:
                    checks.append((f"integrated loudness {args.lufs:g} LUFS ±1.5", abs(lu["integrated_lufs"] - args.lufs) <= 1.5, f"{lu['integrated_lufs']} LUFS"))
                if lu.get("true_peak_dbfs") is not None:
                    checks.append(("true peak ≤ -1 dBFS", lu["true_peak_dbfs"] <= -1.0, f"{lu['true_peak_dbfs']} dBFS"))
            if args.audio:
                master = probe(args.audio)
                mdur = float(master["format"].get("duration") or 0)
                adur = float(a.get("duration") or dur)
                report["master_audio_s"] = round(mdur, 3)
                checks.append(("delivered audio length matches master (±50 ms)", abs(adur - mdur) <= 0.05, f"{adur:.3f} vs {mdur:.3f}"))

    report["checks"] = [{"check": c, "pass": ok, "value": val} for c, ok, val in checks]
    width = max(len(c) for c, _, _ in checks)
    for c, ok, val in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {c.ljust(width)}  {val}")
    failed = [c for c, ok, _ in checks if not ok]
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=1)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
