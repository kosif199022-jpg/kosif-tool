#!/usr/bin/env python3
"""Download videos from links for montage — تحميل فيديوهات من الروابط للمونتاج.

A Linux/macOS port of the ideas in the owner's "Cinema C V32" a-Shell script
(yt-dlp wrapper): format fallback chain, browser-impersonation retry, cookies
file, audio-only, concurrent fragments, and an edit-safe H.264/AAC MP4.
Only the standard library is imported; yt-dlp and ffmpeg are used if present.

  python3 fetch_video.py URL [URL ...] [-o DIR] [--quality 1080|720|best|audio]
  python3 fetch_video.py --urls links.txt -o clips/
  python3 fetch_video.py URL --cookies cookies.txt      # private/age-gated, your own account
  python3 fetch_video.py URL --cookies-from-browser chrome   # same, read from your local browser
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
import urllib.parse
import sys
from pathlib import Path


def find_ytdlp(install: bool = True) -> list[str] | None:
    """yt-dlp as a command; in a cloud session a missing yt-dlp (and curl_cffi) is pip-installed once, quietly."""
    exe = os.environ.get("YTDLP") or shutil.which("yt-dlp")
    if exe:
        return [exe]
    if install:
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            from _deps import ensure  # noqa: PLC0415
            ensure(["yt_dlp", "curl_cffi"], quiet=False)
        except Exception:  # noqa: BLE001 — install is best effort; the message below covers the rest
            pass
        exe = shutil.which("yt-dlp")
        if exe:
            return [exe]
    try:
        import importlib.util  # noqa: PLC0415
        if importlib.util.find_spec("yt_dlp") is not None:
            return [sys.executable, "-m", "yt_dlp"]
    except (ImportError, ValueError):
        pass
    return None


def blocked(err: str, url: str) -> dict | None:
    """When a site refuses the cloud machine (bot check, IP block), say so plainly with the two honest ways forward."""
    try:
        from _deps import blocked_hint, is_blocked  # noqa: PLC0415
    except ImportError:
        return None
    return {"blocked": True, "hint": blocked_hint(url)} if is_blocked(err) else None


def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, capture_output=True, **kw)


QUALITY_ALIASES = {"4k": "2160", "2k": "1440", "uhd": "2160", "fhd": "1080", "hd": "720"}


def norm_quality(q: str) -> str:
    q = (q or "").strip().lower()
    q = QUALITY_ALIASES.get(q, q)
    if q.endswith("p"):
        q = q[:-1]
    if q in ("best", "audio") or q.isdigit():
        return q
    raise argparse.ArgumentTypeError(f"--quality must be best, audio, a height such as 1080 or 1080p, or 4k (got {q!r})")


def is_url(u: str) -> bool:
    try:
        parts = urllib.parse.urlsplit(u)
    except ValueError:
        return False
    return parts.scheme in ("http", "https") and bool(parts.netloc)


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


def attempt(ytdlp, url, out_dir, fmt, extra, cookies, imp, connections, proxy, browser=None):
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
    if browser:  # read the user's own login from a local browser; the cookies never leave this machine
        cmd += ["--cookies-from-browser", browser]
    if imp:
        cmd += ["--impersonate", imp]
    if proxy:
        cmd += ["--proxy", proxy]
    cmd += ["--", url]  # "--" stops a URL that starts with "-" from being read as a yt-dlp option
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
        path, err = attempt(ytdlp, url, out, f, extra, a.cookies, im, a.connections, a.proxy,
                            getattr(a, "cookies_from_browser", None))
        if path:
            p = Path(path)
            rec = {"url": url, "file": str(p), "attempt": i + 1, "impersonate": im, **probe(p), **info_for(p)}
            if a.safe and a.quality != "audio":
                s = edit_safe(p)
                rec["safe_file"] = str(s) if s else None
            return rec
    rec = {"url": url, "file": None, "error": err.strip()[-400:] or "download failed",
           "hint": "run --update (site changed), or supply --cookies for private/age-restricted posts"}
    rec.update(blocked(err, url) or {})
    return rec


def doctor(ytdlp) -> int:  # noqa: D103
    print("yt-dlp:", sh(ytdlp + ["--version"]).stdout.strip() if ytdlp else "MISSING (pip install yt-dlp curl_cffi)")
    print("ffmpeg:", "ok" if shutil.which("ffmpeg") else "MISSING")
    print("impersonation:", (impersonation(ytdlp) or "unavailable (pip install curl_cffi)") if ytdlp else "-")
    return 0 if ytdlp else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--urls", dest="urlfile", help="text file with one URL per line")
    ap.add_argument("-o", "--out", default="downloads")
    ap.add_argument("--quality", default="1080", type=norm_quality, help="best | 2160 | 1080 | 720 | 480 | audio (default 1080)")
    ap.add_argument("--cookies", help="Netscape-format cookies.txt exported from your own browser")
    ap.add_argument("--cookies-from-browser", metavar="BROWSER",
                    help="use your login from a local browser (chrome, firefox, edge, brave, safari…); nothing is copied or stored")
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
        print("yt-dlp not found and could not be installed: pip install yt-dlp curl_cffi"
              " (no network? ask the user to upload the video file instead)", file=sys.stderr)
        return 1
    urls = list(a.urls)
    if a.urlfile:
        urls += [l.strip() for l in Path(a.urlfile).read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    bad = [u for u in urls if not is_url(u)]
    if bad:
        print("skipping entries that are not http(s) URLs: " + ", ".join(repr(u[:60]) for u in bad), file=sys.stderr)
        urls = [u for u in urls if is_url(u)]
    if not urls:
        ap.print_usage()
        return 2
    results = []
    for u in urls:
        r = download(u, a, ytdlp)
        results.append(r)
        print(("OK   " + r["file"]) if r.get("file") else f"FAIL {u}\n     {r.get('error')}")
        if r.get("blocked"):
            print("BLOCKED " + r["hint"])
    (Path(a.out) / "manifest.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0 if all(r.get("file") for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
