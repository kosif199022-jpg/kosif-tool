#!/usr/bin/env python3
"""يكتشف مقاطع الصمت بـ ffmpeg silencedetect ويولّد قائمة قرارات (EDL) تحذفها مع هامش، جاهزة لـ edl_render.py.

usage: python silence_cut.py input.mp4 [--db -35] [--min 0.6] [--pad 0.12] [--out edl.json]
--db عتبة الصمت بالديسيبل، --min أقصر صمت يُحذف بالثواني، --pad هامش يُترك حول الكلام.
"""
import argparse
import json
import re
import subprocess
import sys


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--db", type=float, default=-35)
    ap.add_argument("--min", type=float, default=0.6)
    ap.add_argument("--pad", type=float, default=0.12)
    ap.add_argument("--out", default="edl.json")
    a = ap.parse_args()
    dur = duration(a.input)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", a.input, "-af", f"silencedetect=noise={a.db}dB:d={a.min}", "-f", "null", "-"],
                       capture_output=True, text=True)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    silences = list(zip(starts, ends + ([dur] if len(ends) < len(starts) else [])))
    # keep segments = complement of silences, padded
    keep, cursor = [], 0.0
    for s, e in silences:
        ks, ke = cursor, min(dur, s + a.pad)
        if ke - ks > 0.05:
            keep.append([round(max(0, ks - (a.pad if keep else 0)), 3), round(ke, 3)])
        cursor = max(cursor, e - a.pad)
    if dur - cursor > 0.05:
        keep.append([round(cursor, 3), round(dur, 3)])
    removed = round(dur - sum(e - s for s, e in keep), 2)
    edl = {"fps": 30, "size": None, "sources": {"a": a.input},
           "clips": [{"src": "a", "in": s, "out": e, "transition": {"type": "cut"} if i == 0 else {"type": "cut"}} for i, (s, e) in enumerate(keep)],
           "audio": {"loudnorm": {"I": -14, "TP": -1.0, "LRA": 11}}, "notes": f"silence<{a.db}dB≥{a.min}s removed with pad {a.pad}s"}
    open(a.out, "w", encoding="utf-8").write(json.dumps(edl, ensure_ascii=False, indent=1))
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps({"duration_s": round(dur, 2), "silences": len(silences), "segments_kept": len(keep), "removed_s": removed, "edl": a.out}, ensure_ascii=False))


if __name__ == "__main__":
    main()
