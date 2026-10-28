#!/usr/bin/env python3
"""Download a TikTok photo post (slideshow) — تحميل بوست صور تيك توك (سلايد شو).

yt-dlp refuses photo posts ("Unsupported URL .../photo/<id>"). This tool takes the route that
worked on 2026-10-28:

  1. a short link (vt.tiktok.com, vm.tiktok.com, tiktok.com/t/...) is resolved by following its
     redirects to https://www.tiktok.com/@<user>/photo/<id>;
  2. that page is fetched with a mobile Safari User-Agent and the JSON inside
     <script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"> is read;
  3. __DEFAULT_SCOPE__["webapp.reflow.video.detail"].itemInfo.itemStruct gives desc, author.uniqueId,
     music.title and imagePost.images[] (imageURL.urlList, imageWidth, imageHeight);
  4. every image is saved as img00.jpg, img01.jpg ... (written to .part, renamed when complete,
     skipped on a rerun when already there; the extension follows the real file type);
  5. the post's sound comes from yt-dlp on the rewritten link https://www.tiktok.com/@<user>/video/<id>
     with -f ba (an mp3/m4a);
  6. meta.json records author, desc, music, source_url, image sizes, a credit line and what failed.

  python3 tiktok_photo.py fetch "https://vt.tiktok.com/XXXXXXX/" --out out/tiktok/post
  python3 tiktok_photo.py fetch URL --out DIR --html saved_page.html   # page saved on your device
  python3 tiktok_photo.py parse saved_page.html                        # offline: print the extracted JSON
  python3 tiktok_photo.py url "https://www.tiktok.com/@user/photo/123" # offline: classify and rewrite a link

Exit codes: 0 done, 1 usage or network error, 2 partial download (rerun to resume),
3 not a photo post (use yt-dlp or fetch_video.py), 4 the page JSON is missing or unreadable.

Standard library only; yt-dlp is used for the sound when it is installed (or YTDLP points at it).
TikTok's page structure can change without notice. The creator keeps every right: keep the credit
line, link the post, and reuse only what you own or have permission or a licence for.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "kosif.tiktok_photo.v1"
MOBILE_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 "
             "(KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1")
SCRIPT_ID = "__UNIVERSAL_DATA_FOR_REHYDRATION__"
DETAIL_KEYS = ("webapp.reflow.video.detail", "webapp.video-detail")  # mobile page first, desktop page as fallback
SHORT_HOSTS = {"vt.tiktok.com", "vm.tiktok.com"}
POST_PATH_RE = re.compile(r"^/@([A-Za-z0-9._-]{1,64})/(photo|video)/(\d{5,25})/?$")
PAGE_LIMIT = 12 * 1024 * 1024
IMAGE_LIMIT = 40 * 1024 * 1024
MAX_IMAGES = 60
ATTEMPTS = 2
PAUSE = 0.6  # seconds between requests; tests set it to 0
CREDIT_RIGHTS = ("Third-party post: the creator keeps all rights. Link and credit the post; reuse only "
                 "with the creator's permission or a licence, or keep it as private reference.")
LIMITS = ("TikTok's page structure can change without notice; private, removed or region-locked posts "
          "and networks that block tiktok.com fail (save the page on your device and use --html).")


class PageError(Exception):
    """The page has no readable post JSON."""


class NotPhotoPost(Exception):
    """The link or the page is a video post (or no post at all), not a photo slideshow."""

    def __init__(self, msg: str, post: dict | None = None):
        super().__init__(msg)
        self.post = post or {}


class FetchError(Exception):
    """An HTTP request failed or returned something unusable."""


# ------------------------------------------------------------------ links

def strip_query(url: str) -> str:
    p = urllib.parse.urlsplit(url.strip())
    return urllib.parse.urlunsplit((p.scheme, p.netloc, p.path, "", ""))


def photo_url(user: str, post_id: str) -> str:
    return f"https://www.tiktok.com/@{user}/photo/{post_id}"


def video_url(user: str, post_id: str) -> str:
    return f"https://www.tiktok.com/@{user}/video/{post_id}"


def is_tiktok_host(host: str) -> bool:
    host = (host or "").lower().split(":")[0]
    return host == "tiktok.com" or host.endswith(".tiktok.com")


def classify_url(url: str) -> dict:
    """Offline: what kind of TikTok link this is. kind = photo | video | short | other | foreign | invalid."""
    raw = (url or "").strip()
    p = urllib.parse.urlsplit(raw if "://" in raw else "https://" + raw)
    host = (p.hostname or "").lower()
    out = {"input": raw, "kind": "invalid", "user": None, "id": None, "photo_url": None, "video_url": None,
           "needs_resolve": False}
    if p.scheme not in ("http", "https") or not host:
        return out
    if not is_tiktok_host(host):
        out["kind"] = "foreign"
        return out
    if host in SHORT_HOSTS or re.match(r"^/t/[A-Za-z0-9]+/?$", p.path):
        out.update(kind="short", needs_resolve=True)
        return out
    m = POST_PATH_RE.match(p.path)
    if not m:
        out["kind"] = "other"
        return out
    user, kind, pid = m.groups()
    out.update(kind=kind, user=user, id=pid, photo_url=photo_url(user, pid), video_url=video_url(user, pid))
    return out


def rewrite_to_video(url: str) -> str:
    """https://www.tiktok.com/@u/photo/<id>?x=y -> https://www.tiktok.com/@u/video/<id> (the link yt-dlp reads)."""
    c = classify_url(url)
    if c["kind"] not in ("photo", "video"):
        raise ValueError(f"not a TikTok post link: {url}")
    return c["video_url"]


# ------------------------------------------------------------------ network (tests replace these two)

def http_get(url: str, referer: str | None = None, limit: int = PAGE_LIMIT, timeout: int = 30) -> bytes:
    """GET with the mobile Safari User-Agent; refuses non-https, oversized and truncated answers."""
    if urllib.parse.urlsplit(url).scheme != "https":
        raise FetchError(f"only https links are fetched: {url[:80]}")
    headers = {"User-Agent": MOBILE_UA, "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9"}
    if referer:
        headers["Referer"] = referer
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as r:
            data = r.read(limit + 1)
            expected = r.headers.get("Content-Length")
    except urllib.error.HTTPError as e:
        hint = " (this network may block tiktok.com: save the page on your device and use --html)" \
            if e.code in (403, 405, 407, 451) else ""
        raise FetchError(f"HTTP {e.code} for {urllib.parse.urlsplit(url).netloc}{hint}") from None
    except (urllib.error.URLError, OSError) as e:
        raise FetchError(f"network error for {urllib.parse.urlsplit(url).netloc}: {getattr(e, 'reason', e)}") from None
    if len(data) > limit:
        raise FetchError(f"answer larger than {limit} bytes")
    if expected and expected.isdigit() and int(expected) != len(data):
        raise FetchError(f"truncated: got {len(data)} of {expected} bytes")
    return data


def resolve_short(url: str, timeout: int = 20) -> str:
    """Follow a short link's redirects (like curl -sIL) and return the final link without its query string."""
    req = urllib.request.Request(url if "://" in url else "https://" + url, headers={"User-Agent": MOBILE_UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            final = r.geturl()
    except urllib.error.HTTPError as e:
        raise FetchError(f"HTTP {e.code} while resolving the short link") from None
    except (urllib.error.URLError, OSError) as e:
        raise FetchError(f"network error while resolving the short link: {getattr(e, 'reason', e)}") from None
    return strip_query(final)


# ------------------------------------------------------------------ page parsing (offline)

def extract_universal_json(html: str) -> dict:
    m = re.search(r"<script\b[^>]*\bid=[\"']" + SCRIPT_ID + r"[\"'][^>]*>(.*?)</script>", html, re.S | re.I)
    if not m:
        other = [s for s in ("SIGI_STATE", "__NEXT_DATA__") if s in html]
        extra = f" (found {', '.join(other)} instead: the page structure changed)" if other else \
            " (a login wall, a bot check or a changed page structure)"
        raise PageError(f'no <script id="{SCRIPT_ID}"> in the page{extra}')
    try:
        data = json.loads(m.group(1).strip())
    except json.JSONDecodeError as e:
        raise PageError(f"the {SCRIPT_ID} JSON does not parse: {e}") from None
    if not isinstance(data, dict):
        raise PageError(f"the {SCRIPT_ID} JSON is not an object")
    return data


def item_struct(data: dict) -> dict:
    scope = data.get("__DEFAULT_SCOPE__")
    if not isinstance(scope, dict):
        raise PageError("the page JSON has no __DEFAULT_SCOPE__")
    statuses = []
    for key in DETAIL_KEYS:
        detail = scope.get(key)
        if not isinstance(detail, dict):
            continue
        item = (detail.get("itemInfo") or {}).get("itemStruct")
        if isinstance(item, dict) and item.get("id"):
            return item
        statuses.append(str(detail.get("statusCode")))
    if statuses:
        raise PageError(f"the page holds no post (statusCode {', '.join(statuses)}: removed, private or region-locked?)")
    raise PageError(f"no {' / '.join(DETAIL_KEYS)} entry in __DEFAULT_SCOPE__ (the page structure changed)")


def summarize(item: dict) -> dict:
    """The fields this tool keeps, plus the image list when the post is a photo post."""
    author = item.get("author") if isinstance(item.get("author"), dict) else {}
    music = item.get("music") if isinstance(item.get("music"), dict) else {}
    user, pid = str(author.get("uniqueId") or ""), str(item.get("id") or "")
    images = []
    image_post = item.get("imagePost") if isinstance(item.get("imagePost"), dict) else {}
    for i, img in enumerate(image_post.get("images") or []):
        if not isinstance(img, dict):
            continue
        urls = [u for u in ((img.get("imageURL") or {}).get("urlList") or []) if isinstance(u, str) and u.startswith("https://")]
        images.append({"index": i, "width": img.get("imageWidth"), "height": img.get("imageHeight"), "urls": urls})
    return {
        "id": pid,
        "author": user,
        "nickname": author.get("nickname") or "",
        "desc": item.get("desc") or "",
        "music": {"title": music.get("title") or "", "author": music.get("authorName") or ""},
        "is_photo": bool(images),
        "image_count": len(images),
        "images": images,
        "photo_url": photo_url(user, pid) if user and pid else None,
        "video_url": video_url(user, pid) if user and pid else None,
    }


def extract_post(html: str) -> dict:
    """Page HTML -> post summary; raises PageError (no JSON) or NotPhotoPost (a video post)."""
    post = summarize(item_struct(extract_universal_json(html)))
    if not post["is_photo"]:
        raise NotPhotoPost("this is a video post, not a photo slideshow: download it with yt-dlp "
                           "(python3 scripts/fetch_video.py URL)", post)
    if not any(img["urls"] for img in post["images"]):
        raise PageError("the photo post lists no https image links")
    return post


# ------------------------------------------------------------------ downloading

def sniff_ext(data: bytes) -> str | None:
    if data[:3] == b"\xff\xd8\xff":
        return "jpg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    if data[4:8] == b"ftyp" and data[8:12] in (b"heic", b"heix", b"mif1", b"avif"):
        return "avif" if data[8:12] == b"avif" else "heic"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    return None


def existing_image(out: Path, stem: str) -> Path | None:
    for p in sorted(out.glob(stem + ".*")):
        if p.suffix not in (".part",) and p.stat().st_size > 0:
            return p
    return None


def download_image(img: dict, out: Path, stem: str, referer: str, force: bool = False) -> dict:
    rec = {"index": img["index"], "width": img.get("width"), "height": img.get("height"), "file": None,
           "ok": False, "bytes": 0, "sha256": None,
           "host": urllib.parse.urlsplit(img["urls"][0]).hostname if img["urls"] else None}
    have = None if force else existing_image(out, stem)
    if have is not None:
        data = have.read_bytes()
        rec.update(file=have.name, ok=True, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), resumed=True)
        return rec
    errors = []
    for url in img["urls"][:3]:  # urlList[0] first, mirrors after
        for attempt in range(ATTEMPTS):
            try:
                data = http_get(url, referer=referer, limit=IMAGE_LIMIT)
                ext = sniff_ext(data)
                if ext is None:
                    raise FetchError("the answer is not an image")
                part = out / f"{stem}.{ext}.part"
                part.write_bytes(data)
                final = out / f"{stem}.{ext}"
                os.replace(part, final)
                rec.update(file=final.name, ok=True, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
                return rec
            except FetchError as e:
                errors.append(str(e))
                if PAUSE:
                    time.sleep(PAUSE * (attempt + 1))
    rec["error"] = "; ".join(dict.fromkeys(errors)) or "no https image link"
    return rec


def find_ytdlp() -> list[str] | None:
    exe = os.environ.get("YTDLP") or shutil.which("yt-dlp")
    if exe:
        return [exe]
    try:
        import importlib.util  # noqa: PLC0415
        if importlib.util.find_spec("yt_dlp") is not None:
            return [sys.executable, "-m", "yt_dlp"]
    except (ImportError, ValueError):
        pass
    return None


def fetch_audio(link: str, out: Path, force: bool = False, timeout: int = 600) -> dict:
    rec = {"file": None, "ok": False, "tool": "yt-dlp", "from": link}
    if not force:
        have = [p for p in sorted(out.glob("audio.*")) if p.suffix not in (".part", ".ytdl", ".tmp")]
        if have:
            rec.update(file=have[0].name, ok=True, resumed=True)
            return rec
    ytdlp = find_ytdlp()
    if not ytdlp:
        rec["error"] = "yt-dlp not installed (pip install yt-dlp); the images are unaffected"
        return rec
    cmd = ytdlp + ["-f", "ba", "--no-playlist", "--no-progress", "-o", str(out / "audio.%(ext)s"), "--", link]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        rec["error"] = f"yt-dlp did not finish: {e}"
        return rec
    have = [p for p in sorted(out.glob("audio.*")) if p.suffix not in (".part", ".ytdl", ".tmp")]
    if proc.returncode == 0 and have:
        rec.update(file=have[0].name, ok=True)
    else:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-1:] or ["no audio file was written"]
        rec["error"] = f"yt-dlp exit {proc.returncode}: {tail[0][:300]}"
    return rec


def write_json(path: Path, obj: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


# ------------------------------------------------------------------ commands

def say(msg: str) -> None:
    print(msg, file=sys.stderr)


def not_photo_hint(link: str | None) -> str:
    target = link or "<the link>"
    return (f"not a photo post — ليس بوست صور. For a video use yt-dlp: "
            f"python3 scripts/fetch_video.py \"{target}\"  (or: yt-dlp \"{target}\")")


def cmd_url(a) -> int:
    c = classify_url(a.link)
    c["input"] = strip_query(c["input"]) if c["kind"] in ("photo", "video", "other") else c["input"]
    print(json.dumps(c, ensure_ascii=False, indent=2))
    return 0 if c["kind"] in ("photo", "video", "short") else 1


def cmd_parse(a) -> int:
    path = Path(a.html)
    try:
        html = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        say(f"cannot read {path}: {e}")
        return 1
    try:
        post = extract_post(html)
    except PageError as e:
        say(f"page JSON missing or unreadable: {e}")
        return 4
    except NotPhotoPost as e:
        if e.post:
            print(json.dumps(e.post, ensure_ascii=False, indent=None if a.compact else 2))
        say(f"{e}\n{not_photo_hint(e.post.get('video_url'))}")
        return 3
    print(json.dumps(post, ensure_ascii=False, indent=None if a.compact else 2))
    return 0


def cmd_fetch(a) -> int:
    if not a.url and not a.html:
        say("give a TikTok link, or --html with a saved page")
        return 1
    source = strip_query(a.url) if a.url else None
    want_id = classify_url(a.url)["id"] if a.url else None
    if a.html:
        try:
            html = Path(a.html).read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            say(f"cannot read {a.html}: {e}")
            return 1
    else:
        c = classify_url(a.url)
        if c["kind"] in ("invalid", "foreign"):
            say(f"not a TikTok link: {a.url}")
            return 1
        if c["kind"] == "short":
            try:
                resolved = resolve_short(a.url)
            except FetchError as e:
                say(f"could not resolve the short link: {e}")
                return 1
            say(f"resolved: {resolved}")
            c = classify_url(resolved)
        if c["kind"] not in ("photo", "video"):
            say(f"the link does not lead to a /@user/photo/<id> post: {c['input']}")
            return 1
        want_id = c["id"]
        # a /video/ link is checked too: the page, not the link, says whether the post is a slideshow
        page = c["photo_url"] if c["kind"] == "photo" else c["video_url"]
        try:
            html = http_get(page).decode("utf-8", errors="replace")
        except FetchError as e:
            say(f"could not fetch the post page: {e}")
            return 1
    try:
        post = extract_post(html)
    except PageError as e:
        say(f"page JSON missing or unreadable: {e}")
        return 4
    except NotPhotoPost as e:
        say(f"{e}\n{not_photo_hint(e.post.get('video_url') or source)}")
        return 3
    if want_id and post["id"] != want_id:
        say(f"warning: the page describes post {post['id']}, the link names {want_id}")
    images = post["images"][: a.max_images]
    if len(post["images"]) > len(images):
        say(f"note: {len(post['images'])} images listed, keeping the first {len(images)} (--max-images)")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    referer = post["photo_url"] or "https://www.tiktok.com/"
    recs = []
    for img in images:
        rec = download_image(img, out, f"img{img['index']:02d}", referer, force=a.force)
        recs.append(rec)
        say(f"img{img['index']:02d}: " + (f"{rec['file']} ({rec['bytes']} bytes)" if rec["ok"] else f"FAILED {rec['error']}"))
        if PAUSE and not rec.get("resumed"):
            time.sleep(PAUSE)
    if a.no_audio:
        audio = {"file": None, "ok": False, "skipped": True}
    elif post["video_url"]:
        audio = fetch_audio(post["video_url"], out, force=a.force)
        say("audio: " + (audio["file"] if audio["ok"] else f"FAILED {audio.get('error')}"))
    else:
        audio = {"file": None, "ok": False, "error": "no author/id to build the /video/ link"}
    failed = [r["index"] for r in recs if not r["ok"]]
    complete = not failed and (audio["ok"] or bool(audio.get("skipped")))
    meta = {
        "schema": SCHEMA,
        "source_url": source or post["photo_url"],
        "resolved_url": post["photo_url"],
        "audio_url": post["video_url"],
        "post_id": post["id"],
        "author": {"unique_id": post["author"], "nickname": post["nickname"]},
        "desc": post["desc"],
        "music": post["music"],
        "image_count": len(images),
        "downloaded": len(recs) - len(failed),
        "failed": failed,
        "images": recs,
        "audio": audio,
        "complete": complete,
        "fetched_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "credit": f"Photos by @{post['author']} on TikTok — {post['photo_url']}",
        "rights": CREDIT_RIGHTS,
        "limits": LIMITS,
    }
    write_json(out / "meta.json", meta)
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    if not complete:
        say(f"partial download: {len(failed)} image(s) failed{'' if audio['ok'] or audio.get('skipped') else ', audio failed'}; "
            "rerun the same command to resume (finished files are kept)")
        return 2
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="tiktok_photo.py",
        description="Download a TikTok photo post (slideshow) that yt-dlp rejects: images, sound and meta.json. "
                    "تحميل بوست صور تيك توك: الصور والصوت وملف وصف.",
        epilog="Respect creators: keep the credit line, link the post, reuse only with permission or a licence.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch", help="resolve the link, download every image, the sound and write meta.json")
    f.add_argument("url", nargs="?", help="a photo-post link or a vt.tiktok.com / vm.tiktok.com short link")
    f.add_argument("--out", required=True, help="output folder (created if missing)")
    f.add_argument("--html", help="a saved copy of the post page instead of fetching it (images still download)")
    f.add_argument("--no-audio", action="store_true", help="skip the yt-dlp sound download")
    f.add_argument("--force", action="store_true", help="download again even when files are already there")
    f.add_argument("--max-images", type=int, default=MAX_IMAGES, help=f"cap on images (default {MAX_IMAGES})")
    f.set_defaults(func=cmd_fetch)
    p = sub.add_parser("parse", help="offline: print the post JSON extracted from a saved page")
    p.add_argument("html", help="a saved TikTok post page (.html)")
    p.add_argument("--compact", action="store_true", help="one-line JSON")
    p.set_defaults(func=cmd_parse)
    u = sub.add_parser("url", help="offline: classify a link and show its /photo/ and /video/ forms")
    u.add_argument("link")
    u.set_defaults(func=cmd_url)
    return ap


def main(argv: list[str] | None = None) -> int:
    a = build_parser().parse_args(argv)
    if getattr(a, "max_images", 1) < 1:
        say("--max-images must be at least 1")
        return 1
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
