#!/usr/bin/env python3
"""Pinterest pins as footage — classify a pin before downloading it, then fetch only real video pins.

One helper shared by fetch_video.py (any pin link) and source_finder.py (pins found by a reverse image
search), so both follow the same rules. Standard library only; yt-dlp, ffprobe and ffmpeg run as programs.

1. Classify first, with ONE `yt-dlp -J` call limited to yt-dlp's Pinterest extractor
   (`--use-extractors pinterest --ignore-no-formats-error`). An image pin then comes back as metadata with
   no formats instead of the misleading "No video formats found!", and a pin that only embeds another site
   ends in "No suitable extractor found for URL <embed>" without that site ever being contacted:
     video        a pin with its own video formats: the only kind that is downloaded
     image        no video in the pin (about 60% of search hits in the 2026-10-29 scout run)
     gif          an animated GIF (the pin embeds i.pinimg.com/....gif): an image, not footage
     youtube      the pin embeds YouTube: "embedded YouTube, blocked on cloud", never retried or bypassed
     embedded     the pin embeds another site (Vimeo ...): fetch it from that site instead
     deleted      HTTP 404 on the pin's metadata: deleted or private, never retried
     cdn-refused  the metadata exists but the video server refused the file (HTTP 403/404 on video data)
     blocked      Pinterest refused the metadata request itself (HTTP 403/429)
     error        anything else, with yt-dlp's last error line
   `image`, `gif`, `youtube`, `embedded` and `deleted` are permanent (never asked again, by any run); `video`
   is reused once downloaded; `cdn-refused`, `blocked` and `error` are not retried in this run (one probe and
   at most one download per pin per process) but may be tried again by a later run.
2. Download a video pin into a private temp folder next to the destination, reusing the probe
   (`--load-info-json`, so Pinterest's API is not asked twice). yt-dlp's fragment files such as
   p<ID>.fV_HLSV3_MOBILE-1839.mp4 stay in that folder, only the finished file is moved out, and the folder
   is removed whatever happens, so parallel downloads never see each other's fragments.
3. Measure the result with ffprobe. Pinterest labels the V_720P format with the pin's display size
   (1080x1920) while the file is 720x1280: the label is recorded as `label_size`, the file's real size as
   width/height, and a GIF or still image that arrives in place of a video is detected by extension and
   codec and treated as an image.
4. Optionally drop the pin's own audio (video stream copied, no re-encode): most video pins carry the
   creator's music, which must never leak into a Quran or other dignified montage.
5. Write `<name>.pin.json` per pin: the verdict, the measurements and a credit record (pin URL, uploader
   if known, "licence unknown — credit and link"). A pin is often a re-upload: trace the original creator.
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import urllib.parse
import urllib.request
from pathlib import Path

SCHEMA = "kosif.pinterest_pin.v1"
LICENCE = "licence unknown — credit and link"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
PIN_RE = re.compile(r"pinterest\.[a-z.]+/pin/(?:[^/?#\"'\s]*--)?(\d{6,})", re.I)
YOUTUBE_RE = re.compile(r"(?:youtube(?:-nocookie)?\.com/(?:embed/|watch\?(?:[^\s#]*&)?v=|shorts/|v/)|youtu\.be/)([\w-]{11})", re.I)
SHORT_HOSTS = ("pin.it", "www.pin.it")
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".heic", ".avif"}
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi"}
STILL_CODECS = {"png", "mjpeg", "webp", "bmp", "jpeg2000", "tiff"}
PERMANENT = frozenset({"image", "gif", "youtube", "embedded", "deleted"})   # never tried again, by any run
KINDS = ("video", "image", "gif", "youtube", "embedded", "deleted", "cdn-refused", "blocked", "error")
CEILING = 720                       # Pinterest serves pin video at 720p at most (2026-10-29 scout run)
FORMAT = "bv*+ba/b"                 # Pinterest's height labels are display sizes, so no height filter
SIDE = ".pin.json"

_SEEN: dict = {}                    # (out dir, pin id) -> record: one attempt per pin per process
_SEEN_LOCK = threading.Lock()


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


# ------------------------------------------------------------------------------------------ links

def pin_id(text) -> str | None:
    """A bare pin id, or the id in a pinterest.<tld>/pin/[slug--]<id> link; None otherwise."""
    s = str(text or "").strip()
    if re.fullmatch(r"\d{6,}", s):
        return s
    m = PIN_RE.search(s)
    return m.group(1) if m else None


def pin_url(pid) -> str:
    return f"https://www.pinterest.com/pin/{pid}/"


def _host(url: str) -> str:
    try:
        return (urllib.parse.urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""


def is_short_link(url: str) -> bool:
    return _host(url) in SHORT_HOSTS


def is_pin_link(url: str) -> bool:
    """pinterest.<tld>/pin/<id> links and pin.it short links (boards and profiles are not pins)."""
    host = _host(url)
    return bool(("pinterest." in host and PIN_RE.search(url)) or host in SHORT_HOSTS)


def _open(req, timeout: float):
    return urllib.request.urlopen(req, timeout=timeout)  # noqa: S310 - https pin.it link only


def expand_short_link(url: str, timeout: float = 20) -> str:
    """Follow a pin.it short link (the Pinterest app's share link) to the pin's own URL."""
    if not is_short_link(url):
        return url
    with _open(urllib.request.Request(url, headers={"User-Agent": UA}), timeout) as r:
        return r.geturl()


def ytdlp_command() -> list | None:
    """yt-dlp as a command list (YTDLP env, the yt-dlp program, or python -m yt_dlp); None when absent."""
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


# ------------------------------------------------------------------------------------ classifying

def verdict(kind: str, reason: str, **extra) -> dict:
    """One classification: kind, a one-line reason and whether a later run may try the pin again."""
    permanent = kind in PERMANENT
    retry = None if kind == "video" else "never" if permanent else "not in this run"
    return {"kind": kind, "reason": reason, "permanent": permanent, "retry": retry, **extra}


def _embed_verdict(url: str) -> dict:
    """What a pin that only embeds `url` is: YouTube, a GIF or image file, or another site's video."""
    url = url.strip().rstrip(".,;")
    m = YOUTUBE_RE.search(url)
    host = _host(url)
    if m or host.endswith(("youtube.com", "youtu.be", "youtube-nocookie.com")):
        watch = f"https://www.youtube.com/watch?v={m.group(1)}" if m else url
        return verdict("youtube", f"embedded YouTube, blocked on cloud: the pin only embeds {watch}; not retried and "
                                  "not bypassed (fetch it on your own computer, or upload the file)", embed_url=watch)
    ext = Path(urllib.parse.urlsplit(url).path).suffix.lower()
    if ext == ".gif":
        return verdict("gif", "animated GIF pin: treated as an image, not footage; not downloaded", image_url=url)
    if ext in IMAGE_EXT:
        return verdict("image", "image pin: no video in it; not downloaded", image_url=url)
    return verdict("embedded", f"embedded video from {host or 'another site'}: the pin only links {url}; fetch it from "
                               "that site (fetch_video.py URL), not through Pinterest", embed_url=url)


def _fmt_ext(f: dict) -> str:
    ext = str(f.get("ext") or "").lower()
    if ext:
        return "." + ext.lstrip(".")
    return Path(urllib.parse.urlsplit(str(f.get("url") or "")).path).suffix.lower()


def _size(f: dict) -> str | None:
    w, h = f.get("width"), f.get("height")
    return f"{w}x{h}" if w and h else None


def _best_image(info: dict) -> str | None:
    thumbs = [t for t in info.get("thumbnails") or [] if isinstance(t, dict) and t.get("url")]
    if not thumbs:
        return info.get("thumbnail")
    return max(thumbs, key=lambda t: ((t.get("width") or 0) * (t.get("height") or 0), "/originals/" in t["url"]))["url"]


def classify_info(info) -> dict:
    """Classify a pin from yt-dlp -J output (a dict). Pure: no network, no files."""
    if not isinstance(info, dict):
        return verdict("error", "yt-dlp returned no metadata for the pin")
    if info.get("_type") in ("url", "url_transparent") and info.get("url"):
        return _embed_verdict(str(info["url"]))
    key = str(info.get("extractor_key") or info.get("extractor") or "").lower()
    if key and not key.startswith("pinterest"):        # resolved by another extractor (no --use-extractors)
        return _embed_verdict(str(info.get("webpage_url") or info.get("original_url") or info.get("url") or ""))
    formats = [f for f in info.get("formats") or [] if isinstance(f, dict)]
    if not formats and info.get("url"):
        formats = [info]
    visual = [f for f in formats if f.get("vcodec") != "none"]
    gifs = [f for f in visual if _fmt_ext(f) == ".gif" or str(f.get("vcodec") or "").lower() == "gif"]
    real = [f for f in visual if f not in gifs and _fmt_ext(f) not in IMAGE_EXT]
    if real:
        best = max(real, key=lambda f: ((f.get("width") or 0) * (f.get("height") or 0), f.get("tbr") or 0))
        label = _size(best)
        return verdict("video", "video pin" + (f" (formats labelled up to {label}, a display size: the file is "
                                               "measured after download)" if label else ""),
                       label_size=label, label_format=best.get("format_id"), duration=info.get("duration"))
    if gifs:
        g = gifs[0]
        size = _size(g)
        return verdict("gif", "animated GIF pin" + (f" ({size})" if size else "") + ": treated as an image, not footage; "
                       "not downloaded", image_url=g.get("url") or _best_image(info))
    return verdict("image", "image pin: no video in it (yt-dlp's 'No video formats found!' is expected here, not a bug); "
                            "not downloaded", image_url=_best_image(info))


def classify_error(stderr: str, stage: str = "probe") -> dict:
    """Classify a failed yt-dlp run from its stderr; stage is 'probe' (the -J call) or 'download'. Pure."""
    text = stderr or ""
    low = text.lower()
    errors = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("ERROR")]
    last = (errors or [ln.strip() for ln in text.splitlines() if ln.strip()] or ["no error text"])[-1][:300]
    m = re.search(r"No suitable extractor found for URL (\S+)", text)
    if m:
        return _embed_verdict(m.group(1))
    if "no such option" in low and ("use-extractors" in low or "load-info-json" in low):
        return verdict("error", "this yt-dlp is too old for the Pinterest path (no --use-extractors): run "
                                "python3 scripts/fetch_video.py --update")
    if "[youtube]" in low or ("youtube" in low and ("sign in to confirm" in low or "not a bot" in low)):
        y = YOUTUBE_RE.search(text)
        return _embed_verdict(f"https://www.youtube.com/watch?v={y.group(1)}" if y else "https://www.youtube.com/")
    if "no video formats found" in low:
        return verdict("image", "image pin: no video in it (yt-dlp's 'No video formats found!' is expected here, not a "
                                "bug); not downloaded")
    c = re.search(r"HTTP Error (\d{3})", text)
    code = int(c.group(1)) if c else None
    if stage == "probe":
        if code == 404:
            return verdict("deleted", "pin not found (HTTP 404 on its metadata): deleted or made private; never retried")
        if code in (401, 403, 429) or "too many requests" in low or "captcha" in low:
            return verdict("blocked", f"Pinterest refused the pin's metadata from this machine (HTTP {code or 'refusal'}); "
                                      "not retried in this run (try later, or from your own computer)")
    else:
        if code in (403, 404, 410):
            return verdict("cdn-refused", f"the pin's metadata exists but Pinterest's video server refused the file "
                                          f"(HTTP {code}); not retried in this run (it may work later or from your own "
                                          "computer)")
        if code == 429 or "too many requests" in low:
            return verdict("blocked", "Pinterest rate-limited the download (HTTP 429); not retried in this run")
    return verdict("error", f"yt-dlp failed: {last}")


def _run(cmd: list, timeout: float) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=timeout)


def probe(url: str, ytdlp: list, extra=(), timeout: float = 60) -> tuple[dict | None, dict]:
    """One `yt-dlp -J` call on a pin URL -> (the metadata or None, the verdict). Never downloads media."""
    cmd = list(ytdlp) + ["-J", "--no-playlist", "--no-warnings", "--ignore-no-formats-error",
                         "--use-extractors", "pinterest", *extra, "--", url]
    try:
        r = _run(cmd, timeout)
    except subprocess.TimeoutExpired:
        return None, verdict("error", f"the metadata request timed out after {int(timeout)} s; not retried in this run")
    except OSError as e:
        return None, verdict("error", f"yt-dlp could not be started: {e}")
    info = None
    if r.stdout.strip() and r.stdout.strip() != "null":
        try:
            info = json.loads(r.stdout)
        except ValueError:
            info = None
    if r.returncode != 0 or not isinstance(info, dict):
        return None, classify_error(r.stderr, "probe")
    return info, classify_info(info)


# ------------------------------------------------------------------------------------------ media

def probe_media(path) -> dict:
    """ffprobe: duration, width, height, fps, vcodec, acodec ({} when ffprobe is missing or fails)."""
    exe = shutil.which("ffprobe")
    if not exe:
        return {}
    p = subprocess.run([exe, "-v", "error", "-show_entries",
                        "format=duration:stream=codec_type,codec_name,width,height,r_frame_rate", "-of", "json", str(path)],
                       capture_output=True, text=True, errors="replace")
    try:
        j = json.loads(p.stdout)
    except ValueError:
        return {}
    v = next((s for s in j.get("streams", []) if s.get("codec_type") == "video"), {})
    a = next((s for s in j.get("streams", []) if s.get("codec_type") == "audio"), {})
    try:
        duration = round(float(j.get("format", {}).get("duration", 0) or 0), 2)
    except (TypeError, ValueError):
        duration = 0.0
    return {"duration": duration, "width": v.get("width"), "height": v.get("height"),
            "fps": v.get("r_frame_rate"), "vcodec": v.get("codec_name"), "acodec": a.get("codec_name")}


def still_kind(path, media: dict) -> str | None:
    """'gif' or 'image' when a downloaded file is not video footage (by extension, then codec); else None."""
    ext = Path(path).suffix.lower()
    codec = str((media or {}).get("vcodec") or "").lower()
    if ext == ".gif" or codec == "gif":
        return "gif"
    if ext in IMAGE_EXT or (codec in STILL_CODECS and ext not in VIDEO_EXT):
        return "image"
    return None


def remove_audio(path) -> tuple[bool, str]:
    """Drop every audio stream in place (first video stream copied, no re-encode). (ok, why-not)."""
    path = Path(path)
    exe = shutil.which("ffmpeg")
    if not exe:
        return False, "ffmpeg is not installed"
    tmp = path.with_name(path.stem + ".noaudio" + path.suffix)
    cmd = [exe, "-v", "error", "-y", "-i", str(path), "-map", "0:v:0", "-c", "copy", "-an", "-sn", "-dn"]
    if path.suffix.lower() in (".mp4", ".mov", ".m4v"):
        cmd += ["-movflags", "+faststart"]
    r = subprocess.run(cmd + [str(tmp)], capture_output=True, text=True, errors="replace")
    if r.returncode == 0 and tmp.is_file() and tmp.stat().st_size > 0:
        os.replace(tmp, path)
        return True, ""
    tmp.unlink(missing_ok=True)
    return False, (r.stderr.strip().splitlines() or ["ffmpeg failed"])[-1][:200]


# ---------------------------------------------------------------------------------------- records

def credit_record(url: str, info: dict | None = None) -> dict:
    """Who to credit: the pin link, the uploader when Pinterest names one, and an unknown licence."""
    info = info if isinstance(info, dict) else {}
    up = str(info.get("uploader") or "").strip() or None
    title = str(info.get("title") or "").strip() or None
    return {"pin": url, "uploader": up, "uploader_id": info.get("uploader_id"), "title": title, "licence": LICENCE,
            "line": f"Pinterest pin {url}" + (f" by {up}" if up else " (uploader unknown)") + f" — {LICENCE}",
            "note": "A pin is often a re-upload: trace the original creator and reuse the footage only with their "
                    "permission or a licence."}


def sidecar(out_dir, name: str) -> Path:
    return Path(out_dir) / f"{name}{SIDE}"


def read_record(out_dir, name: str) -> dict | None:
    try:
        rec = json.loads(sidecar(out_dir, name).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return rec if isinstance(rec, dict) and rec.get("schema") == SCHEMA else None


def _write_record(out_dir, name: str, rec: dict) -> dict:
    p = sidecar(out_dir, name)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, p)
    rec["sidecar"] = str(p)
    return rec


def summary_line(rec: dict) -> str:
    return f"{rec.get('kind', 'error'):<11} {rec.get('pin_id') or rec.get('url')}  {rec.get('reason', '')}"


def reset_memory() -> None:
    """Forget which pins this process already tried (tests, or a long-lived caller starting a new run)."""
    with _SEEN_LOCK:
        _SEEN.clear()


# ------------------------------------------------------------------------------------------ fetch

def _result_file(tmp: Path, name: str, stdout: str) -> Path | None:
    """The finished file yt-dlp wrote in tmp: never a fragment (name.f<format>.ext), part or info file."""
    for line in reversed((stdout or "").splitlines()):
        p = Path(line.strip())
        if line.strip() and p.is_file() and p.parent == tmp and p.stem == name:
            return p
    hits = [p for p in sorted(tmp.iterdir()) if p.is_file() and p.stem == name
            and p.suffix.lower() not in (".json", ".part", ".ytdl", ".temp", ".tmp")]
    return hits[0] if hits else None


def classify_link(link, ytdlp: list | None = None, extra=(), timeout: float = 60) -> dict:
    """Classify one pin (link, pin.it link or id) without downloading anything or writing any file."""
    rec, url = _start(link)
    if rec.get("kind"):
        return rec
    cmd = ytdlp or ytdlp_command()
    if not cmd:
        rec.update(verdict("error", "yt-dlp is not installed: pip install yt-dlp"))
        return rec
    info, v = probe(url, cmd, extra, timeout)
    rec.update(v)
    rec["credit"] = credit_record(url, info)
    return rec


def _start(link) -> tuple[dict, str]:
    """A fresh record and the canonical pin URL (pin.it links are followed once)."""
    link = str(link or "").strip()
    url = pin_url(link) if re.fullmatch(r"\d{6,}", link) else link
    rec = {"schema": SCHEMA, "link": link, "url": url, "pin_id": None, "checked": _now(), "file": None}
    if is_short_link(url):
        try:
            url = expand_short_link(url)
        except Exception as e:  # noqa: BLE001 - any network failure is reported as this pin's one-line reason
            rec.update(verdict("error", f"the pin.it short link could not be opened ({str(e)[:120]}); not retried"))
            return rec, url
    pid = pin_id(url)
    if not pid:
        rec.update(verdict("error", "not a Pinterest pin link (pinterest.<tld>/pin/<id>/ or a pin.it link)"))
        return rec, url
    url = pin_url(pid)
    rec.update(url=url, pin_id=pid)
    return rec, url


def fetch(link, out_dir, *, name: str | None = None, prefix: str = "p", ytdlp: list | None = None,
          strip_audio: bool = False, extra=(), probe_timeout: float = 60, timeout: float = 300) -> dict:
    """Classify one pin, download it only when it is a video, measure it, optionally strip its audio, and write
    <out_dir>/<name>.pin.json. Returns the record; record["file"] is the finished video or None.

    `name` defaults to `<prefix><pin id>`, built after a pin.it link is followed, so the same pin gets the same
    file and sidecar names whether it was given as a pin.it link, a full link or a bare id.

    A pin is tried once per process; a later call (another run) skips pins whose sidecar holds a permanent
    kind and reuses a finished file. Nothing is ever retried in a loop."""
    out_dir = Path(out_dir)
    rec, url = _start(link)
    if rec.get("kind"):
        return rec
    pid = rec["pin_id"]
    name = name or f"{prefix}{pid}"
    key = (str(out_dir.resolve()), pid)
    with _SEEN_LOCK:
        if key in _SEEN:
            return dict(_SEEN[key], repeated=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    old = read_record(out_dir, name)
    done = next((p for p in (out_dir / f"{name}{e}" for e in (".mp4", ".webm", ".mov", ".m4v", ".mkv")) if p.is_file()), None)
    if done:                                             # finished by an earlier run: reuse, never download again
        rec = dict(old) if old and old.get("kind") == "video" else dict(rec, **verdict("video", "video pin: already downloaded"))
        rec.update(file=str(done), reused=True)
        if strip_audio and rec.get("audio") != "stripped" and (probe_media(done).get("acodec") or not shutil.which("ffprobe")):
            ok, why = remove_audio(done)
            if ok:
                rec.update(audio="stripped", acodec=None)
            else:                                        # fail closed, as for a new download; the file is left alone
                rec.update(verdict("error", f"could not strip the audio of the earlier download {done.name} ({why}); "
                                            "not used, so its music cannot leak into the edit"), file=None)
        rec = _write_record(out_dir, name, rec)
    elif old and old.get("permanent"):                    # image, gif, embed or deleted: never asked again
        rec = dict(old, cached=True)
    else:
        rec = _fetch_new(rec, url, out_dir, name, ytdlp, strip_audio, extra, probe_timeout, timeout)
    with _SEEN_LOCK:
        _SEEN[key] = rec
    return rec


def _fetch_new(rec, url, out_dir: Path, name, ytdlp, strip_audio, extra, probe_timeout, timeout) -> dict:
    cmd = ytdlp or ytdlp_command()
    if not cmd:
        rec.update(verdict("error", "yt-dlp is not installed: pip install yt-dlp"))
        return _write_record(out_dir, name, rec)
    info, v = probe(url, cmd, extra, probe_timeout)
    rec.update(v)
    rec["credit"] = credit_record(url, info)
    if v["kind"] != "video":
        return _write_record(out_dir, name, rec)
    tmp = Path(tempfile.mkdtemp(prefix=f".{name}-", suffix=".tmp", dir=out_dir))
    try:
        (tmp / "probe.json").write_text(json.dumps(info, ensure_ascii=False), encoding="utf-8")
        dl = list(cmd) + ["--load-info-json", str(tmp / "probe.json"), "--no-warnings", "--no-playlist",
                          "-f", FORMAT, "--merge-output-format", "mp4", "-o", str(tmp / f"{name}.%(ext)s"),
                          "--print", "after_move:filepath", *extra]
        try:
            r = _run(dl, timeout)
        except subprocess.TimeoutExpired:
            rec.update(verdict("error", f"the download timed out after {int(timeout)} s; nothing kept, not retried in "
                                        "this run"))
            return _write_record(out_dir, name, rec)
        got = _result_file(tmp, name, r.stdout)
        if r.returncode != 0 or not got:
            rec.update(classify_error(r.stderr, "download") if r.returncode != 0 else
                       verdict("error", "yt-dlp reported success but wrote no file; not retried in this run"))
            return _write_record(out_dir, name, rec)
        media = probe_media(got)
        still = still_kind(got, media)
        if still:
            size = f" ({media['width']}x{media['height']})" if media.get("width") else ""
            rec.update(verdict(still, f"the pin's file is {'an animated GIF' if still == 'gif' else 'a still image'}{size}, "
                                      "not video: treated as an image, not kept as footage"))
            return _write_record(out_dir, name, rec)
        if strip_audio:
            if media.get("acodec") or not media:
                ok, why = remove_audio(got)
                if not ok:
                    rec.update(verdict("error", f"could not strip the pin's own audio ({why}); nothing kept, so its "
                                                "music cannot leak into the edit"))
                    return _write_record(out_dir, name, rec)
                rec["audio"] = "stripped"
                media = probe_media(got) or media
            else:
                rec["audio"] = "none (the file has no audio stream)"
        else:
            rec["audio"] = ("kept: the pin's own audio, usually the creator's music" if media.get("acodec")
                            else "none (the file has no audio stream)" if media else "unknown (ffprobe is not installed)")
        dest = out_dir / f"{name}{got.suffix.lower()}"
        os.replace(got, dest)
        rec["file"] = str(dest)
        rec.update({k: media.get(k) for k in ("width", "height", "duration", "fps", "vcodec", "acodec")})
        label, real = rec.get("label_size"), _size(media)
        rec["resolution_verified"] = bool(real)
        if not real:
            rec["size_note"] = ("not measured (ffprobe is not installed): do not trust the format label"
                                + (f" {label}" if label else "") + f"; Pinterest serves video at {CEILING}p at most")
        elif label and label != real:
            rec["size_note"] = (f"Pinterest labels this pin {label}, its display size; the file is {real} "
                                f"(measured by ffprobe). Pinterest serves video at {CEILING}p at most.")
        rec["reason"] = f"video pin: downloaded, {real or 'size not measured'}" + (", audio stripped"
                                                                                   if rec["audio"] == "stripped" else "")
        return _write_record(out_dir, name, rec)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
