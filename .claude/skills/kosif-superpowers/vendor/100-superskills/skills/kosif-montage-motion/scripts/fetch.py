"""Fetch videos and images from Pinterest (a pin, a board, a section) — and from the other sites yt-dlp reads (TikTok,
Instagram, Facebook, YouTube, X…) — into the media library, ready for montage. Method from the user's Cinema C (V32):
yt-dlp with a simple-format retry, the original file kept, and an edit-safe copy (H.264 + AAC + yuv420p + faststart,
constant frame rate) made for the timeline.

    python scripts/kmotion.py fetch URL [URL …] [--max 30] [--only video|image] [--out DIR] [--cookies cookies.txt]
    python scripts/kmotion.py fetch --list URL           what a pin/board holds, without downloading

Every file is recorded in DIR/fetch-credits.json (source link, title, creator, type, size, duration). Pins are the
creators' work: use them as references, or in a published film only when you have the rights; keep the credits.
Logins are never typed by this tool: public pins need none; for your own private boards pass a cookies.txt you
exported yourself (--cookies).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
FF = shutil.which("ffmpeg") or "ffmpeg"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"


def default_out() -> Path:
    home = Path(os.environ.get("KOSIF_MOTION_HOME") or HERE.parent)
    return home / "workbench" / "media"                      # the studio's media library (the site and kosif_media list it)


def _ydl(opts: dict):
    try:
        import yt_dlp
    except ImportError:
        raise SystemExit("yt-dlp is missing: python -m pip install yt-dlp  (claude.ai: scripts/cloud_setup.py --install)")
    base = {"quiet": True, "no_warnings": True, "noprogress": True, "http_headers": {"User-Agent": UA}, "retries": 3, "socket_timeout": 20,
            "ignore_no_formats_error": True}                  # an image pin: no video formats, but its image list comes back
    return yt_dlp.YoutubeDL({**base, **opts})


def _entries(url: str, cookies: str | None, max_items: int) -> list[dict]:
    """Pins of a URL (a single pin → one entry; a board → up to max_items), as yt-dlp info dicts."""
    opts = {"extract_flat": "in_playlist", "playlistend": max_items}
    if cookies:
        opts["cookiefile"] = cookies
    with _ydl(opts) as y:
        info = y.extract_info(url, download=False)
    if info is None:
        return [_image_from_page(url)]
    if info.get("_type") in ("playlist", "multi_video"):
        out = []
        for e in list(info.get("entries") or [])[:max_items]:
            u = e.get("url") or e.get("webpage_url")
            if not u:
                continue
            if not u.startswith("http"):
                u = f"https://www.pinterest.com/pin/{e.get('id') or u}/"
            out.append(_full(u, cookies) or {"webpage_url": u, "id": e.get("id"), "error": "unreadable"})
        return out
    return [info if info.get("formats") is not None or info.get("thumbnails") else _full(url, cookies)]


def _full(url: str, cookies: str | None) -> dict | None:
    opts = {"cookiefile": cookies} if cookies else {}
    try:
        with _ydl(opts) as y:
            return y.extract_info(url, download=False)
    except Exception as e:  # noqa: BLE001 — an image pin has no video formats: yt-dlp raises, the page still has the image
        msg = str(e)
        if "No video formats" in msg or "no video" in msg.lower():
            return _image_from_page(url)
        return {"webpage_url": url, "error": msg[:200]}


def _image_from_page(url: str) -> dict:
    """An image pin: the largest image the page names (og:image → /originals/)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    html = urllib.request.urlopen(req, timeout=25).read(4_000_000).decode("utf-8", "replace")
    m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', html)
    src = m.group(1) if m else None
    if src:
        src = re.sub(r"/\d+x(?:\d+)?(_\w+)?/", "/originals/", src)        # i.pinimg.com/736x/… → /originals/…
    title = (re.search(r"<title[^>]*>(.*?)</title>", html, re.S) or [None, ""])[1].strip()
    pid = (re.search(r"/pin/(?:[\w-]+--)?(\d+)", url) or [None, re.sub(r"\W+", "_", url)[-24:]])[1]
    return {"id": pid, "webpage_url": url, "title": title, "thumbnails": [{"url": src}] if src else [], "formats": None, "image_only": True}


def _best_image(info: dict) -> str | None:
    th = [t for t in (info.get("thumbnails") or []) if t.get("url")]
    if not th:
        return None
    orig = [t["url"] for t in th if "/originals/" in t["url"]]
    if orig:
        return orig[0]
    return max(th, key=lambda t: (t.get("width") or 0) * (t.get("height") or 0))["url"]


def _download_image(url: str, out: Path) -> Path:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.pinterest.com/"})
    data = urllib.request.urlopen(req, timeout=40).read(60_000_000)
    ext = (re.search(r"\.(jpe?g|png|webp|gif)(?:$|\?)", url, re.I) or [None, "jpg"])[1].lower().replace("jpeg", "jpg")
    f = out.with_suffix("." + ext)
    f.write_bytes(data)
    if ext == "webp":                                          # the engine and the browsers in every route read PNG
        png = f.with_suffix(".png")
        subprocess.run([FF, "-y", "-v", "error", "-i", str(f), str(png)], check=True)
        return png
    return f


def _download_video(url: str, out_stem: Path, cookies: str | None) -> Path:
    opts = {"outtmpl": str(out_stem) + ".%(ext)s", "merge_output_format": "mp4", "format": "bv*+ba/b"}
    if cookies:
        opts["cookiefile"] = cookies
    for fmt in ("bv*+ba/b", "b"):                               # Cinema C: retry once with a simple single-file format
        opts["format"] = fmt
        try:
            with _ydl(opts) as y:
                info = y.extract_info(url, download=True)
            f = Path(y.prepare_filename(info)).with_suffix(".mp4")
            if not f.exists():
                f = next(iter(sorted(out_stem.parent.glob(out_stem.name + ".*"))), f)
            if f.exists():
                return f
        except Exception as e:  # noqa: BLE001
            last = e
    raise RuntimeError(f"download failed: {str(last)[:200]}")


def edit_safe(src: Path) -> Path:
    """H.264 yuv420p at a constant frame rate (≤ 60), AAC 48 kHz stereo, faststart — what the timeline and every
    platform read; the original stays untouched next to it."""
    out = src.with_name(src.stem + ".edit.mp4")
    r = subprocess.run([FF, "-hide_banner", "-i", str(src)], capture_output=True, text=True)   # info level: the stream list
    fps = 30.0
    m = re.search(r"(\d+(?:\.\d+)?) fps", r.stderr)
    if m:
        fps = min(60.0, max(12.0, float(m.group(1))))
    has_audio = " Audio: " in r.stderr
    if " Video: " not in r.stderr:
        raise RuntimeError(f"{src.name}: no video stream")
    cmd = [FF, "-y", "-v", "error", "-i", str(src), "-vf", f"fps={fps:g},scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p",
           "-c:v", "libx264", "-preset", "medium", "-crf", "17"]
    cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"] if has_audio else ["-an"]
    subprocess.run(cmd + ["-movflags", "+faststart", str(out)], check=True)
    # a download or encode cut short (app closed, network drop) leaves a file that probes fine but cannot be decoded
    chk = subprocess.run([FF, "-v", "error", "-xerror", "-i", str(out), "-f", "null", "-"], capture_output=True, text=True)
    if chk.returncode != 0 or chk.stderr.strip():
        out.unlink(missing_ok=True)
        raise RuntimeError(f"{src.name}: broken video (decode check failed) — fetch it again")
    return out


def fetch(urls: list[str], out: Path, max_items: int = 30, only: str | None = None, cookies: str | None = None, dry: bool = False) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    cred_f = out / "fetch-credits.json"
    credits = json.loads(cred_f.read_text(encoding="utf-8")) if cred_f.exists() else []
    # a source counts as fetched only while its file is still there (a quarantined or deleted clip is fetched again)
    alive = lambda c: any(c.get(k) and Path(c[k]).exists() for k in ("edit", "file"))   # noqa: E731
    credits = [c for c in credits if alive(c)]
    seen = {c.get("source") for c in credits}
    got, skipped = [], []
    for url in urls:
        try:
            items = _entries(url, cookies, max_items)
        except Exception as e:  # noqa: BLE001
            skipped.append({"url": url, "why": str(e)[:200]}); continue
        for info in items:
            src = info.get("webpage_url") or url
            kind = "image" if info.get("image_only") or not info.get("formats") else "video"
            row = {"source": src, "id": str(info.get("id") or ""), "title": info.get("title"), "creator": info.get("uploader"), "type": kind,
                   "duration": info.get("duration")}
            if info.get("error"):
                skipped.append({"url": src, "why": info["error"]}); continue
            if kind == "image" and not _best_image(info):            # no image list from yt-dlp: read the page itself
                info = _image_from_page(src)
            if only and kind != only:
                continue
            if dry:
                got.append(row); continue
            if src in seen:
                skipped.append({"url": src, "why": "already fetched"}); continue
            stem = out / f"{re.sub(r'[^0-9A-Za-z_-]+', '_', row['id'] or str(int(time.time())))}"
            try:
                if kind == "video":
                    f = _download_video(src, stem, cookies)
                    row["file"] = str(f); row["edit"] = str(edit_safe(f))
                else:
                    img = _best_image(info)
                    if not img:
                        raise RuntimeError("no image on the pin")
                    row["file"] = str(_download_image(img, stem))
                row["bytes"] = Path(row["file"]).stat().st_size
                row["fetched"] = time.strftime("%Y-%m-%d %H:%M:%S")
                credits.append(row); seen.add(src); got.append(row)
            except Exception as e:  # noqa: BLE001
                skipped.append({"url": src, "why": str(e)[:200]})
    if not dry:
        cred_f.write_text(json.dumps(credits, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"out": str(out), "fetched" if not dry else "found": got, "skipped": skipped,
            "note": "pins belong to their creators: references, or use only with rights; fetch-credits.json keeps the sources"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="+"); ap.add_argument("--out"); ap.add_argument("--max", type=int, default=30)
    ap.add_argument("--only", choices=["video", "image"]); ap.add_argument("--cookies"); ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    res = fetch(a.urls, Path(a.out) if a.out else default_out(), a.max, a.only, a.cookies, a.list)
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
