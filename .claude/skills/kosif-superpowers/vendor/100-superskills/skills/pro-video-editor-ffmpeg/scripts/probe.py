#!/usr/bin/env python3
"""يفحص ملفات الفيديو/الصوت بـ ffprobe: الكودك، والدقة، ومعدل الإطارات (ثابت/متغير)، والمدة، والصوت، ومواضع الإطارات المفتاحية.

usage: python probe.py file1.mp4 [file2.mov ...] [--keyframes] [--json out.json]
--keyframes يطبع أزمنة الإطارات المفتاحية (I-frames) لاستخدامها في القصّ بلا إعادة ترميز (-c copy).
"""
import argparse
import json
import shutil
import subprocess
import sys
from fractions import Fraction


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffprobe failed: {' '.join(cmd)}\n{r.stderr[-800:]}")
    return r.stdout


def probe(path: str, keyframes: bool) -> dict:
    data = json.loads(run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path]))
    out = {"file": path, "duration_s": float(data["format"].get("duration", 0) or 0), "size_bytes": int(data["format"].get("size", 0) or 0),
           "container": data["format"].get("format_name"), "video": None, "audio": [], "warnings": []}
    for s in data["streams"]:
        if s["codec_type"] == "video" and out["video"] is None:
            r = Fraction(s.get("r_frame_rate", "0/1")); a = Fraction(s.get("avg_frame_rate", "0/1"))
            vfr = a and r and abs(float(r) - float(a)) > 0.01
            out["video"] = {"codec": s.get("codec_name"), "width": s.get("width"), "height": s.get("height"),
                            "fps": round(float(r), 3) if r else None, "avg_fps": round(float(a), 3) if a else None,
                            "pix_fmt": s.get("pix_fmt"), "nb_frames": s.get("nb_frames"), "bitrate": s.get("bit_rate"),
                            "color": {k: s.get(k) for k in ("color_primaries", "color_transfer", "color_space")},
                            "vfr_suspect": bool(vfr)}
            if vfr:
                out["warnings"].append("معدل إطارات متغير محتمل (VFR): حوّل بـ -vf fps=30 قبل القطع الدقيق لتجنب انزياح الصوت")
            if s.get("pix_fmt") not in ("yuv420p", None):
                out["warnings"].append(f"pix_fmt={s.get('pix_fmt')}: للويب استخدم -pix_fmt yuv420p")
        elif s["codec_type"] == "audio":
            out["audio"].append({"codec": s.get("codec_name"), "sample_rate": s.get("sample_rate"), "channels": s.get("channels"),
                                 "bitrate": s.get("bit_rate"), "lang": (s.get("tags") or {}).get("language")})
    if keyframes and out["video"]:
        pk = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_packets", "-show_entries", "packet=pts_time,flags",
                             "-print_format", "json", path]))
        kf = sorted(float(p["pts_time"]) for p in pk.get("packets", []) if "K" in p.get("flags", "") and p.get("pts_time") not in (None, "N/A"))
        out["keyframes_s"] = [round(k, 3) for k in kf]
        if len(kf) > 1:
            gaps = [b - a for a, b in zip(kf, kf[1:])]
            out["gop_s"] = {"min": round(min(gaps), 2), "max": round(max(gaps), 2), "mean": round(sum(gaps) / len(gaps), 2)}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--keyframes", action="store_true")
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    if not shutil.which("ffprobe"):
        sys.exit("ffprobe غير موجود في PATH")
    res = [probe(f, a.keyframes) for f in a.files]
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if a.json:
        open(a.json, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
    for r in res:
        v = r["video"] or {}
        print(f"{r['file']}: {r['duration_s']:.2f}s {v.get('width')}x{v.get('height')} {v.get('fps')}fps {v.get('codec')} {v.get('pix_fmt')} | audio: {len(r['audio'])}"
              + (f" | keyframes: {len(r.get('keyframes_s', []))} (GOP≈{r.get('gop_s', {}).get('mean', 'n/a')}s)" if a.keyframes else ""))
        for w in r["warnings"]:
            print("  !", w)


if __name__ == "__main__":
    main()
