"""KOSIF platforms — one checked delivery file per platform (TikTok, Reels, Shorts, YouTube, X, WhatsApp status,
LinkedIn, Snapchat): reframed to the platform's ratio (face-aware), encoded under its bitrate ceiling, measured
against its duration and size limits — a breach is reported, never silently trimmed.

    python platforms.py FILM.mp4 --out deliver --platforms tiktok,shorts,whatsapp [--title "عنوان"] [--mode smart|crop|blur]
    python platforms.py --list

Limits are the platforms' commonly published ones (2026); verify at use — the report says so.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

import tools  # noqa: E402

# ratio, size, longest clip (s), largest file (MB), video ceiling (kbps), audio (kbps), Arabic name
PLATFORMS = {
    "tiktok":   ("9:16", (1080, 1920), 600, 287, 12000, 192, "تيك توك"),
    "reels":    ("9:16", (1080, 1920), 180, 250, 12000, 192, "إنستغرام ريلز"),
    "shorts":   ("9:16", (1080, 1920), 180, 256, 12000, 192, "يوتيوب شورتس"),
    "youtube":  ("16:9", (1920, 1080), None, 2000, 16000, 256, "يوتيوب"),
    "x":        ("16:9", (1280, 720), 140, 512, 8000, 160, "إكس"),
    "whatsapp": ("9:16", (720, 1280), 30, 16, 2200, 96, "حالة واتساب"),
    "linkedin": ("1:1", (1080, 1080), 600, 200, 8000, 192, "لينكدإن"),
    "snapchat": ("9:16", (1080, 1920), 60, 32, 6000, 128, "سناب شات"),
}


def table() -> dict:
    return {k: {"name": v[6], "ratio": v[0], "size": f"{v[1][0]}x{v[1][1]}", "max_seconds": v[2], "max_mb": v[3], "video_kbps": v[4], "audio_kbps": v[5]} for k, v in PLATFORMS.items()}


def deliver(src: Path, out_dir: Path, platforms: list[str], title: str | None = None, mode: str = "smart", crf: int = 20) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    info = tools.probe(src)
    w, h, dur = info["video"]["w"], info["video"]["h"], info["duration"]
    rep = {"source": str(src), "seconds": round(dur, 2), "platforms": {}, "limits_note": "limits as commonly published by the platforms; verify at use"}
    tmp = Path(tempfile.mkdtemp(prefix="kosif_platforms_"))
    for p in platforms:
        if p not in PLATFORMS:
            rep["platforms"][p] = {"error": f"unknown platform; one of {', '.join(PLATFORMS)}"}; continue
        ratio, (W, H), max_s, max_mb, vk, ak, ar = PLATFORMS[p]
        plate, used = src, "copy"
        if abs(W / H - w / h) > 0.01 or (w, h) != (W, H):
            plate = tmp / f"{p}_plate.mp4"
            used = tools.aspect(src, plate, ratio, mode, (W, H))["mode"]
        dst = out_dir / f"{src.stem}_{p}.mp4"
        base = [tools.FF, "-y", "-v", "error", "-i", str(plate), "-c:v", "libx264", "-profile:v", "high", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-ar", "48000", "-c:a", "aac"]
        tools._run([*base, "-crf", str(crf), "-maxrate", f"{vk}k", "-bufsize", f"{2 * vk}k", "-b:a", f"{ak}k", str(dst)])
        mb = dst.stat().st_size / 1e6
        warnings = []
        if max_mb and mb > max_mb:                              # one tighter pass before giving up
            tools._run([*base, "-crf", str(crf + 6), "-maxrate", f"{vk // 2}k", "-bufsize", f"{vk}k", "-b:a", f"{max(64, ak // 2)}k", str(dst)])
            mb = dst.stat().st_size / 1e6
            if mb > max_mb:
                warnings.append(f"{mb:.1f} MB over the {max_mb} MB limit even after a tighter pass")
        if max_s and dur > max_s + 0.05:
            warnings.append(f"{dur:.1f} s is longer than the {max_s} s limit: trim (kmotion trim) or split")
        rep["platforms"][p] = {"file": str(dst), "name": ar, "size": f"{W}x{H}", "ratio": ratio, "reframe": used, "mb": round(mb, 2), "warnings": warnings}
    if title:
        rep["poster"] = tools.thumb(src, out_dir / f"{src.stem}_poster.jpg", 2.0, title)
    shutil.rmtree(tmp, ignore_errors=True)
    (out_dir / f"{src.stem}.platforms.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("film", nargs="?"); ap.add_argument("--out", default="deliver"); ap.add_argument("--platforms", default="tiktok,reels,shorts")
    ap.add_argument("--title"); ap.add_argument("--mode", default="smart", choices=["smart", "crop", "blur"]); ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list or not a.film:
        print(json.dumps(table(), ensure_ascii=False, indent=1)); return 0
    rep = deliver(Path(a.film), Path(a.out), [x.strip().lower() for x in a.platforms.split(",") if x.strip()], a.title, a.mode)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
