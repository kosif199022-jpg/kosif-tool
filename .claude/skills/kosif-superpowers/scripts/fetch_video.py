#!/usr/bin/env python3
"""Download videos from links for montage — تحميل فيديوهات من الروابط للمونتاج.

A Linux/macOS port of the ideas in the owner's "Cinema C V32" a-Shell script
(yt-dlp wrapper): format fallback chain, browser-impersonation retry, cookies
file, audio-only, concurrent fragments, and an edit-safe H.264/AAC MP4.
Only the standard library is imported; yt-dlp and ffmpeg are used if present.

  python3 fetch_video.py URL [URL ...] [-o DIR] [--quality 1080|720|best|audio]
  python3 fetch_video.py --urls links.txt -o clips/
  python3 fetch_video.py URL --cookies cookies.txt      # private/age-gated, your own account
  python3 fetch_video.py URL --safe                     # also build an edit-safe MP4 copy
  python3 fetch_video.py --doctor | --update

Writes <DIR>/<title> [<id>].<ext> and a manifest.json (url, file, duration, title, uploader,
license field if the site exposes one). Use only content you have the right to use.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_ytdlp() -> list[str] | None:
    exe = os.environ.get("YTDLP") or shutil.which("yt-dlp")
    if exe:
        return [exe]
    try:
        import yt_dlp  # noqa: F401
        return [sys.executable, "-m", "yt_dlp"]
    except ImportError:
        return None


def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, capture_output=True, **kw)


def selector(quality: str) -> tuple[str, list[str]]:
    """Return (format selector, extra args)."""
    if quality == "audio":
        return "ba/b", ["-x", "--audio-format", "m4a"]
    cap = "" if quality == "best" else f"[height<={int(quality)}]"
    return f"bv*{cap}+ba/b{cap}/best", ["--merge-output-format", "mp4"]


def impersonation(ytdlp: list[str]) -> str | None:
    out = sh(ytdlp + ["--list-impersonate-targets"]).stdout
    for want in ("Safari", "Chrome"):
        for line in out.splitlines():
            if line.startswith(want) and "unavailable" not in line.lower():
                return want.lower()
    return None


def attempt(ytdlp, url, out_dir, fmt, extra, cookies, imp, connections, proxy):
    cmd = ytdlp + ["--no-playlist", "--continue", "--newline", "--no-part", "--no-progress",
                   "--concurrent-fragments", str(connections), "--retries", "10",
                   "--fragment-retries", "10", "--extractor-retries", "3", "--socket-timeout", "30",
                   "-f", fmt, "-o", str(out_dir / "%(title).120B [%(id)s].%(ext)s"),
                   "--print", "after_move:filepath", "--write-info-json", "--no-clean-info-json"]
    cmd += extra
    if shutil.which("node"):  # YouTube needs a JS runtime for full-quality formats
        cmd += ["--js-runtimes", "node"]
    if cookies:
        cmd += ["--cookies", cookies]
    if imp:
        cmd += ["--impersonate", imp]
    if proxy:
        cmd += ["--proxy", proxy]
    cmd.append(url)
    p = sh(cmd)
    paths = [l for l in p.stdout.splitlines() if l.strip() and Path(l.strip()).is_file()]
    return (paths[-1].strip() if p.returncode == 0 and paths else None), p.stderr[-600:]


def edit_safe(src: Path) -> Path | None:
    """H.264 + AAC + yuv420p + faststart copy that every editor/Photos app accepts."""
    if not shutil.which("ffmpeg"):
        return None
    dst = src.with_name(src.stem + ".safe.mp4")
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src), "-map", "0:v:0", "-map", "0:a:0?",
           "-sn", "-dn", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(dst)]
    return dst if sh(cmd).returncode == 0 and dst.is_file() and dst.stat().st_size else None


def probe(path: Path) -> dict:
    if not shutil.which("ffprobe"):
        return {}
    p = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name,width,height,r_frame_rate",
            "-of", "json", str(path)])
    try:
        j = json.loads(p.stdout)
    except json.JSONDecodeError:
        return {}
    v = next((s for s in j.get("streams", []) if s.get("codec_type") == "video"), {})
    a = next((s for s in j.get("streams", []) if s.get("codec_type") == "audio"), {})
    return {"duration": round(float(j.get("format", {}).get("duration", 0) or 0), 2), "width": v.get("width"), "height": v.get("height"),
            "fps": v.get("r_frame_rate"), "vcodec": v.get("codec_name"), "acodec": a.get("codec_name")}


def info_for(path: Path) -> dict:
    j = path.with_suffix(".info.json")
    if not j.is_file():
        return {}
    try:
        d = json.loads(j.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return {k: d.get(k) for k in ("title", "uploader", "id", "extractor_key", "license", "webpage_url", "upload_date")}


def download(url, a, ytdlp) -> dict:
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    fmt, extra = selector(a.quality)
    fb = "ba/b/best" if a.quality == "audio" else "bv*+ba/b/best"
    tries = [(fmt, None), (fb, None)]
    imp = impersonation(ytdlp)
    if imp:
        tries.append((fb, imp))
    err = ""
    for i, (f, im) in enumerate(tries):
        path, err = attempt(ytdlp, url, out, f, extra, a.cookies, im, a.connections, a.proxy)
        if path:
            p = Path(path)
            rec = {"url": url, "file": str(p), "attempt": i + 1, "impersonate": im, **probe(p), **info_for(p)}
            if a.safe and a.quality != "audio":
                s = edit_safe(p)
                rec["safe_file"] = str(s) if s else None
            return rec
    return {"url": url, "file": None, "error": err.strip()[-400:] or "download failed",
            "hint": "run --update (site changed), or supply --cookies for private/age-restricted posts"}


def doctor(ytdlp) -> int:
    print("yt-dlp:", sh(ytdlp + ["--version"]).stdout.strip() if ytdlp else "MISSING (pip install yt-dlp curl_cffi)")
    print("ffmpeg:", "ok" if shutil.which("ffmpeg") else "MISSING")
    print("impersonation:", (impersonation(ytdlp) or "unavailable (pip install curl_cffi)") if ytdlp else "-")
    return 0 if ytdlp else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--urls", dest="urlfile", help="text file with one URL per line")
    ap.add_argument("-o", "--out", default="downloads")
    ap.add_argument("--quality", default="1080", help="best | 2160 | 1080 | 720 | 480 | audio (default 1080)")
    ap.add_argument("--cookies", help="Netscape-format cookies.txt exported from your own browser")
    ap.add_argument("--connections", type=int, default=8)
    ap.add_argument("--proxy")
    ap.add_argument("--safe", action="store_true", help="also write an edit-safe H.264/AAC copy (.safe.mp4)")
    ap.add_argument("--doctor", action="store_true")
    ap.add_argument("--update", action="store_true")
    a = ap.parse_args(argv)
    ytdlp = find_ytdlp()
    if a.update:
        return subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp", "curl_cffi"])
    if a.doctor:
        return doctor(ytdlp)
    if not ytdlp:
        print("yt-dlp not found: pip install yt-dlp curl_cffi", file=sys.stderr)
        return 1
    urls = list(a.urls)
    if a.urlfile:
        urls += [l.strip() for l in Path(a.urlfile).read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    if not urls:
        ap.print_usage()
        return 2
    results = []
    for u in urls:
        r = download(u, a, ytdlp)
        results.append(r)
        print(("OK   " + r["file"]) if r.get("file") else f"FAIL {u}\n     {r.get('error')}")
    (Path(a.out) / "manifest.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0 if all(r.get("file") for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
