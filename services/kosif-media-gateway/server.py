#!/usr/bin/env python3
"""KOSIF Media Gateway: an authenticated, bounded, no-bypass video intake service.

* Plain HTTP API (/v1/probe, /v1/download, /v1/files/<ticket>) and a stateless
  MCP Streamable-HTTP endpoint (/mcp) that Claude Code can add with
  `claude mcp add --transport http ... --header "Authorization: Bearer ..."`.
* Only fetches what the platform serves without signing in. It never sends
  cookies, never rotates IPs or proxies, and never touches CAPTCHA or DRM.
  When YouTube blocks the host (LOGIN_REQUIRED, HTTP 429, HTTP 403, proxy 502)
  the gateway reports the exact code and pauses further YouTube calls for a
  cool-down instead of retrying.
* Cinema C V34 intake rules: portrait-aware quality cap (yt-dlp `-S res:N`
  measures the shorter side, so 1080x1920 counts as 1080p), H.264/AAC
  preferred, lossless remux when the streams are already compatible, libx264
  fallback otherwise, and every output is decoded (head and tail) and fully
  demuxed before it is offered. The original download is kept as its own
  file; a partial or corrupt file is deleted and never reported as success.

Standard library only; yt-dlp, imageio-ffmpeg and deno come from requirements.txt.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

VERSION = "0.2.0"


def _env_int(name: str, default: int) -> int:
    try:
        return max(1, int(os.environ.get(name, default)))
    except ValueError:
        return default


MAX_MB = _env_int("KOSIF_MAX_MB", 45)
PER_HOUR = _env_int("KOSIF_DOWNLOADS_PER_HOUR", 3)
FILE_TTL = _env_int("KOSIF_FILE_TTL", 600)
UPLOAD_MB = _env_int("KOSIF_UPLOAD_MB", 150)
UPLOAD_TTL = _env_int("KOSIF_UPLOAD_TTL", 3600)
BLOCK_COOLDOWN = _env_int("KOSIF_BLOCK_COOLDOWN", 1800)
DOWNLOAD_TIMEOUT = _env_int("KOSIF_DOWNLOAD_TIMEOUT", 150)
PROBE_TIMEOUT = _env_int("KOSIF_PROBE_TIMEOUT", 45)
TRANSCODE_TIMEOUT = _env_int("KOSIF_TRANSCODE_TIMEOUT", 240)
PUBLIC_PROBE_EVERY = _env_int("KOSIF_PUBLIC_PROBE_EVERY", 900)
PUBLIC_PROBE_VIDEO = os.environ.get("KOSIF_PUBLIC_PROBE_VIDEO", "dYrEeavC3cw")
MAX_BODY = 8192
TEMP_PREFIX = "kosif-media-"

RIGHTS = ("owned", "written-permission", "public-domain", "cc-licensed", "youtube-authorized")
QUALITIES = (360, 480, 720, 1080)
_VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
_YT_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com", "youtu.be"}
# Non-YouTube hosts whose public files are freely licensed or that the owner
# can authorize; extend with KOSIF_EXTRA_HOSTS=host1,host2.
_DEFAULT_HOSTS = {"upload.wikimedia.org", "commons.wikimedia.org", "archive.org", "vimeo.com", "player.vimeo.com"}
BLOCK_CODES = {"YOUTUBE_LOGIN_REQUIRED", "YOUTUBE_HTTP_429", "YOUTUBE_HTTP_403", "YOUTUBE_PROXY_502"}

# yt-dlp command; tests replace it with a stub.
YTDLP_CMD = [sys.executable, "-m", "yt_dlp"]

_LOCK = threading.Lock()
_BUSY = threading.Lock()
_JOBS: dict[str, dict] = {}          # job id -> {"folder", "expires", "files": {ticket: meta}}
_ATTEMPTS: list[float] = []          # download attempts that reached the platform, last hour
_STATE = {"blocked_until": 0.0, "last_youtube": None, "public_probe_at": 0.0,
          "verified_downloads": 0, "started": time.time()}


# ---------------------------------------------------------------- sources

def allowed_hosts() -> set[str]:
    extra = {h.strip().lower() for h in os.environ.get("KOSIF_EXTRA_HOSTS", "").split(",") if h.strip()}
    return _DEFAULT_HOSTS | extra


def video_id(source: str) -> str | None:
    """YouTube id from a bare id or a watch / youtu.be / shorts / live / embed URL."""
    source = (source or "").strip()
    if _VIDEO_ID.fullmatch(source):
        return source
    try:
        u = urllib.parse.urlsplit(source)
    except ValueError:
        return None
    if u.scheme not in ("https", "http") or u.username or u.password or u.port not in (None, 443, 80):
        return None
    host = (u.hostname or "").lower().rstrip(".")
    path = [p for p in u.path.split("/") if p]
    candidate = ""
    if host == "youtu.be" and len(path) == 1:
        candidate = path[0]
    elif host in _YT_HOSTS and path == ["watch"]:
        candidate = urllib.parse.parse_qs(u.query).get("v", [""])[0]
    elif host in _YT_HOSTS and len(path) == 2 and path[0] in ("shorts", "live", "embed"):
        candidate = path[1]
    return candidate if _VIDEO_ID.fullmatch(candidate) else None


def parse_source(source: str) -> dict | None:
    """{'kind': 'youtube'|'url', 'url', 'id'} for an accepted source, else None (no SSRF to other hosts)."""
    vid = video_id(source)
    if vid:
        return {"kind": "youtube", "id": vid, "url": "https://www.youtube.com/watch?v=" + vid}
    try:
        u = urllib.parse.urlsplit((source or "").strip())
    except ValueError:
        return None
    host = (u.hostname or "").lower().rstrip(".")
    if (u.scheme != "https" or u.username or u.password or u.port not in (None, 443)
            or host not in allowed_hosts() or len(source) > 600):
        return None
    return {"kind": "url", "id": hashlib.sha256(source.encode()).hexdigest()[:11], "url": source.strip()}


# ---------------------------------------------------------------- diagnostics

_URLS = re.compile(r"https?://\S+")


def classify(stderr: str, kind: str = "youtube") -> dict:
    """Exact, sanitized reason for a yt-dlp failure. Nothing here tries to get around it."""
    s = stderr or ""
    low = s.lower()
    errors = [l for l in s.splitlines() if l.startswith("ERROR")] or [l for l in s.splitlines() if l.strip()]
    detail = _URLS.sub("[url]", errors[-1] if errors else "")[-300:]
    pre = "YOUTUBE_" if kind == "youtube" else "SOURCE_"
    if "sign in to confirm" in low or "not a bot" in low:
        code = pre + "LOGIN_REQUIRED"
    elif "429" in s or "too many requests" in low:
        code = pre + "HTTP_429"
    elif "502" in s and ("proxy" in low or "bad gateway" in low or "tunnel" in low):
        code = pre + "PROXY_502"
    elif "drm" in low:
        code = "DRM_PROTECTED"
    elif "max-filesize" in low or "larger than max" in low:
        code = "FILE_TOO_LARGE"
    elif "private video" in low or "members-only" in low or "age-restricted" in low or "confirm your age" in low:
        code = "ACCESS_RESTRICTED"
    elif "403" in s:
        code = pre + "HTTP_403"
    elif "video unavailable" in low or "not available" in low and "format" not in low:
        code = "VIDEO_UNAVAILABLE"
    elif "requested format is not available" in low:
        code = "FORMAT_UNAVAILABLE"
    else:
        code = "DOWNLOAD_FAILED"
    return {"code": code, "detail": detail}


def _note_youtube(code: str) -> None:
    with _LOCK:
        _STATE["last_youtube"] = {"code": code, "at": int(time.time())}
        if code in BLOCK_CODES:
            _STATE["blocked_until"] = time.time() + BLOCK_COOLDOWN


def _cooldown(kind: str) -> dict | None:
    if kind != "youtube":
        return None
    with _LOCK:
        left = int(_STATE["blocked_until"] - time.time())
        last = _STATE["last_youtube"]
    if left > 0:
        return {"ok": False, "error": (last or {}).get("code", "YOUTUBE_BLOCKED"), "cooldown_seconds": left,
                "retried": False,
                "note": "YouTube refused this host recently; no further request is sent until the cool-down ends. "
                        "No login, cookie, proxy or CAPTCHA bypass is attempted."}
    return None


# ---------------------------------------------------------------- tools

def ffmpeg_exe() -> str | None:
    found = os.environ.get("KOSIF_FFMPEG") or shutil.which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:  # noqa: BLE001
        return None


def js_runtime() -> str | None:
    """yt-dlp needs a JS runtime for YouTube's player; the deno wheel ships one."""
    try:
        import deno
        path = deno.find_deno_bin()
        if path and Path(path).is_file():
            return "deno:" + str(path)
    except Exception:  # noqa: BLE001
        pass
    if shutil.which("deno"):
        return "deno"
    if shutil.which("node"):
        return "node"
    return None


def _run(args: list[str], timeout: int) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False,
                          stdin=subprocess.DEVNULL)


_DEPS: dict = {}


def dependencies() -> dict:
    """Run each dependency once (cached): a module that imports is not proof the binary works."""
    if _DEPS:
        return _DEPS
    out = {"yt_dlp": None, "ffmpeg": None, "libx264": False, "js_runtime": js_runtime()}
    try:
        p = _run(YTDLP_CMD + ["--version"], 30)
        out["yt_dlp"] = p.stdout.strip() if p.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        pass
    ff = ffmpeg_exe()
    if ff:
        try:
            p = _run([ff, "-hide_banner", "-version"], 15)
            if p.returncode == 0:
                out["ffmpeg"] = p.stdout.split("\n", 1)[0][:80]
                enc = _run([ff, "-hide_banner", "-encoders"], 15).stdout
                out["libx264"] = "libx264" in enc
        except (OSError, subprocess.TimeoutExpired):
            pass
    _DEPS.update(out)
    return _DEPS


# ---------------------------------------------------------------- media checks

_DUR = re.compile(r"Duration: (\d+):(\d+):(\d+(?:\.\d+)?)")
_VID = re.compile(r"Stream #\S+.*?: Video: (\w+).*?, (\d{2,5})x(\d{2,5})")
_AUD = re.compile(r"Stream #\S+.*?: Audio: (\w+)")
_ROT = re.compile(r"rotation of (-?\d+(?:\.\d+)?) degrees")
_FPS = re.compile(r"(\d+(?:\.\d+)?) fps")


def inspect(path: Path) -> dict:
    """Duration, display size and codecs from ffmpeg's own reading of the file (no ffprobe needed)."""
    ff = ffmpeg_exe()
    if not ff:
        return {}
    try:
        err = _run([ff, "-hide_banner", "-nostdin", "-i", str(path)], 30).stderr
    except (OSError, subprocess.TimeoutExpired):
        return {}
    info: dict = {}
    d = _DUR.search(err)
    if d:
        info["duration"] = round(int(d.group(1)) * 3600 + int(d.group(2)) * 60 + float(d.group(3)), 3)
    v = _VID.search(err)
    if v:
        w, h = int(v.group(2)), int(v.group(3))
        rot = _ROT.search(err)
        if rot and int(abs(float(rot.group(1)))) % 180 == 90:
            w, h = h, w
        info.update(vcodec=v.group(1), width=w, height=h, orientation="portrait" if h > w else "landscape" if w > h else "square")
        f = _FPS.search(err[v.start():])
        if f:
            info["fps"] = float(f.group(1))
    a = _AUD.search(err)
    info["acodec"] = a.group(1) if a else None
    return info


def verify(path: Path, expected_duration: float | None = None) -> dict:
    """A real decoder pass: full demux, first frames, last seconds and audio; rejects partial files."""
    ff = ffmpeg_exe()
    if not ff:
        return {"ok": False, "error": "FFMPEG_NOT_INSTALLED"}
    if not path.is_file() or path.stat().st_size < 1024:
        return {"ok": False, "error": "EMPTY_OR_MISSING_FILE"}
    info = inspect(path)
    if not info.get("vcodec") or not info.get("width") or not info.get("duration"):
        return {"ok": False, "error": "NO_VIDEO_STREAM", **info}
    base = [ff, "-hide_banner", "-nostdin", "-v", "error", "-xerror"]
    checks = {
        "demux": base + ["-i", str(path), "-map", "0", "-c", "copy", "-f", "null", "-"],
        "decode_head": base + ["-i", str(path), "-map", "0:v:0", "-frames:v", "5", "-f", "null", "-"],
        "decode_tail": base + ["-sseof", "-2", "-i", str(path), "-map", "0:v:0", "-f", "null", "-"],
    }
    if info.get("acodec"):
        checks["decode_audio"] = base + ["-i", str(path), "-map", "0:a:0", "-t", "3", "-f", "null", "-"]
    for name, cmd in checks.items():
        try:
            p = _run(cmd, 90)
        except (OSError, subprocess.TimeoutExpired):
            return {"ok": False, "error": "VERIFY_TIMEOUT", "check": name, **info}
        if p.returncode != 0 or p.stderr.strip():
            return {"ok": False, "error": "CORRUPT_OR_INCOMPLETE", "check": name,
                    "detail": _URLS.sub("[url]", p.stderr.strip())[-200:], **info}
    if expected_duration and info["duration"] + max(1.0, 0.03 * expected_duration) < expected_duration:
        return {"ok": False, "error": "INCOMPLETE_DURATION", "expected_duration": expected_duration, **info}
    return {"ok": True, "decoder": "ffmpeg", "checks": list(checks), **info}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fp:
        for chunk in iter(lambda: fp.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def make_compatible(src: Path, info: dict, folder: Path) -> dict:
    """H.264/AAC MP4 with +faststart: stream copy when already compatible (lossless), libx264 otherwise."""
    ff = ffmpeg_exe()
    dst = folder / "compatible.mp4"
    tmp = folder / "compatible.pending.mp4"
    base = [ff, "-y", "-nostdin", "-hide_banner", "-loglevel", "error", "-i", str(src),
            "-map", "0:v:0", "-map", "0:a:0?", "-sn", "-dn"]
    trials = []
    if info.get("vcodec") == "h264" and info.get("acodec") in (None, "aac"):
        trials.append(("remux", base + ["-c", "copy", "-tag:v", "avc1", "-movflags", "+faststart", str(tmp)]))
    if dependencies().get("libx264"):
        trials.append(("libx264", base + ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                                          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                                          "-movflags", "+faststart", str(tmp)]))
    last = "NO_ENCODER"
    for method, cmd in trials:
        tmp.unlink(missing_ok=True)
        try:
            p = _run(cmd, TRANSCODE_TIMEOUT if method != "remux" else 60)
        except subprocess.TimeoutExpired:
            last = "TRANSCODE_TIMEOUT"
            continue
        if p.returncode:
            last = "ENCODE_FAILED"
            continue
        check = verify(tmp, info.get("duration"))
        if check.get("ok"):
            tmp.replace(dst)
            return {"ok": True, "method": method, "lossless": method == "remux", "path": dst, "media": check}
        last = check.get("error", "VERIFY_FAILED")
    tmp.unlink(missing_ok=True)
    return {"ok": False, "error": last}


# ---------------------------------------------------------------- jobs

def _drop(job: dict) -> None:
    shutil.rmtree(job["folder"], ignore_errors=True)


def prune() -> None:
    now = time.time()
    with _LOCK:
        for key, job in list(_JOBS.items()):
            if now >= job["expires"]:
                _drop(job)
                del _JOBS[key]
        _ATTEMPTS[:] = [t for t in _ATTEMPTS if now - t < 3600]


def clean_stale_temp() -> int:
    """Remove folders a crashed or restarted process left behind."""
    removed = 0
    root = Path(tempfile.gettempdir())
    live = {j["folder"] for j in _JOBS.values()}
    for d in root.glob(TEMP_PREFIX + "*"):
        if str(d) not in live and d.is_dir() and time.time() - d.stat().st_mtime > FILE_TTL:
            shutil.rmtree(d, ignore_errors=True)
            removed += 1
    return removed


def find_file(ticket: str) -> dict | None:
    with _LOCK:
        for job in _JOBS.values():
            meta = job["files"].get(ticket)
            if meta and time.time() < job["expires"]:
                return meta
    return None


# ---------------------------------------------------------------- probe & download

def _yt_common(src: dict) -> list[str]:
    args = ["--no-config", "--no-playlist", "--retries", "1", "--fragment-retries", "2",
            "--extractor-retries", "1", "--socket-timeout", "15", "--no-cache-dir"]
    rt = dependencies().get("js_runtime")
    if rt and src["kind"] == "youtube":
        args += ["--js-runtimes", rt]
    return args


def probe(source: str, media_check: bool = False) -> dict:
    src = parse_source(source)
    if not src:
        return {"ok": False, "error": "INVALID_SOURCE",
                "hint": "11-character YouTube id, a YouTube/Shorts URL, or an https URL on an allowed host"}
    blocked = _cooldown(src["kind"])
    if blocked:
        return {**blocked, "video_id": src["id"]}
    args = YTDLP_CMD + _yt_common(src) + ["--skip-download", "-J", "--", src["url"]]
    try:
        p = _run(args, PROBE_TIMEOUT)
    except subprocess.TimeoutExpired:
        return {"ok": False, "video_id": src["id"], "error": "PROBE_TIMEOUT"}
    if p.returncode:
        diag = classify(p.stderr, src["kind"])
        if src["kind"] == "youtube":
            _note_youtube(diag["code"])
        return {"ok": False, "video_id": src["id"], "error": diag["code"], "detail": diag["detail"],
                "retried": False}
    try:
        data = json.loads(p.stdout)
    except ValueError:
        return {"ok": False, "video_id": src["id"], "error": "PROBE_BAD_JSON"}
    if src["kind"] == "youtube":
        _note_youtube("OK")
    fmts = [f for f in data.get("formats") or [] if f.get("vcodec") not in (None, "none")]
    out = {"ok": True, "video_id": src["id"], "downloaded": False,
            "title": (data.get("title") or "")[:120], "duration": data.get("duration"),
            "width": data.get("width"), "height": data.get("height"),
            "license": data.get("license"), "uploader": (data.get("uploader") or "")[:80],
            "video_formats": len(fmts),
            "h264_formats": sum(1 for f in fmts if str(f.get("vcodec", "")).startswith(("avc", "h264")))}
    if media_check:
        out["media_access"] = _media_check(src)
        if out["media_access"]["code"] != "OK":
            out["ok"] = False
            out["error"] = out["media_access"]["code"]
    return out


def _media_check(src: dict) -> dict:
    """Reading metadata is not downloading: fetch only the first ~10 KB of a real stream (yt-dlp --test)."""
    folder = Path(tempfile.mkdtemp(prefix=TEMP_PREFIX))
    try:
        args = YTDLP_CMD + _yt_common(src) + ["--test", "-f", "18/b[ext=mp4]/b/bv*", "-S", "res:360",
                                               "-o", str(folder / "check.%(ext)s"), "--", src["url"]]
        try:
            p = _run(args, PROBE_TIMEOUT)
        except subprocess.TimeoutExpired:
            return {"code": "MEDIA_CHECK_TIMEOUT"}
        if p.returncode:
            diag = classify(p.stderr, src["kind"])
            if src["kind"] == "youtube":
                _note_youtube(diag["code"])
            return diag
        got = sum(f.stat().st_size for f in folder.iterdir() if f.is_file())
        return {"code": "OK" if got > 0 else "MEDIA_EMPTY", "bytes_read": got}
    finally:
        shutil.rmtree(folder, ignore_errors=True)


def _selector(quality: int) -> list[str]:
    # Cinema C V34: res:N caps the SHORTER side (portrait 1080x1920 == 1080p); prefer H.264 + AAC.
    ios_v = "[vcodec~='^(avc|h264)']"
    ios_a = "[acodec~='^(mp4a|aac)']"
    return ["-f", f"bv*{ios_v}+ba{ios_a}/bv*+ba/b{ios_v}/b[ext=mp4]/b",
            "-S", f"res:{quality},fps,vcodec:h264,acodec:aac", "--merge-output-format", "mp4"]


def _file_entry(path: Path, media: dict, role: str, name: str) -> tuple[str, dict]:
    ticket = secrets.token_urlsafe(24)
    return ticket, {"path": str(path), "size_bytes": path.stat().st_size, "sha256": sha256(path),
                    "role": role, "filename": name, "media": media}


def download(source: str, rights: str, quality: int | str = 720, base_url: str = "") -> dict:
    src = parse_source(source)
    if not src:
        return {"ok": False, "error": "INVALID_SOURCE"}
    if rights not in RIGHTS:
        return {"ok": False, "error": "EXPLICIT_DOWNLOAD_PERMISSION_REQUIRED", "allowed_rights": list(RIGHTS)}
    try:
        quality = int(str(quality).rstrip("p"))
    except ValueError:
        return {"ok": False, "error": "INVALID_QUALITY", "allowed": list(QUALITIES)}
    if quality not in QUALITIES:
        return {"ok": False, "error": "INVALID_QUALITY", "allowed": list(QUALITIES)}
    blocked = _cooldown(src["kind"])
    if blocked:
        return {**blocked, "video_id": src["id"]}
    prune()
    if not _BUSY.acquire(blocking=False):
        return {"ok": False, "error": "BUSY_ONE_DOWNLOAD_AT_A_TIME", "retry_after_seconds": 30}
    folder = Path(tempfile.mkdtemp(prefix=TEMP_PREFIX))
    keep = False
    try:
        with _LOCK:
            if len(_ATTEMPTS) >= PER_HOUR:
                oldest = min(_ATTEMPTS)
                return {"ok": False, "error": "RATE_LIMIT_PER_HOUR", "limit": PER_HOUR,
                        "retry_after_seconds": int(3600 - (time.time() - oldest)) + 1}
            _ATTEMPTS.append(time.time())
        ff = ffmpeg_exe()
        if not ff:
            return {"ok": False, "error": "FFMPEG_NOT_INSTALLED"}
        args = YTDLP_CMD + _yt_common(src) + _selector(quality) + [
            "--max-filesize", f"{MAX_MB}M", "--ffmpeg-location", ff, "--no-mtime",
            "--write-info-json", "--no-write-playlist-metafiles",
            "-o", str(folder / "source.%(ext)s"), "--print", "after_move:filepath", "--", src["url"]]
        try:
            p = _run(args, DOWNLOAD_TIMEOUT)
        except subprocess.TimeoutExpired:
            return {"ok": False, "video_id": src["id"], "error": "DOWNLOAD_TIMEOUT", "limit_seconds": DOWNLOAD_TIMEOUT}
        if p.returncode:
            diag = classify(p.stderr, src["kind"])
            if src["kind"] == "youtube":
                _note_youtube(diag["code"])
            return {"ok": False, "video_id": src["id"], "error": diag["code"], "detail": diag["detail"], "retried": False}
        printed = [Path(l.strip()) for l in p.stdout.splitlines() if l.strip()]
        original = next((f for f in reversed(printed) if f.is_file() and f.parent == folder), None)
        if not original:
            return {"ok": False, "video_id": src["id"], "error": "NO_OUTPUT_FILE"}
        if original.stat().st_size > MAX_MB * 1024 * 1024:
            return {"ok": False, "video_id": src["id"], "error": "FILE_TOO_LARGE", "limit_mb": MAX_MB}
        meta = {}
        info_json = folder / "source.info.json"
        if info_json.is_file():
            try:
                meta = json.loads(info_json.read_text(encoding="utf-8"))
            except ValueError:
                meta = {}
            info_json.unlink(missing_ok=True)
        expected = meta.get("duration") if isinstance(meta.get("duration"), (int, float)) else None
        check = verify(original, expected)
        if not check.get("ok"):
            return {"ok": False, "video_id": src["id"], "error": check.get("error"), "verify": check}
        if src["kind"] == "youtube":
            _note_youtube("OK")
        files = {}
        ticket, entry = _file_entry(original, check, "original", f"{src['id']}.original{original.suffix}")
        files[ticket] = entry
        compat = make_compatible(original, check, folder)
        if compat.get("ok"):
            t2, e2 = _file_entry(compat["path"], compat["media"], "compatible", f"{src['id']}.mp4")
            e2.update(method=compat["method"], lossless=compat["lossless"])
            files[t2] = e2
        job_id = secrets.token_hex(8)
        with _LOCK:
            _JOBS[job_id] = {"folder": str(folder), "expires": time.time() + FILE_TTL, "files": files}
            _STATE["verified_downloads"] += 1
        keep = True
        out = []
        for t, e in files.items():
            item = {k: v for k, v in e.items() if k != "path"}
            item["file_path"] = "/v1/files/" + t
            if base_url:
                item["url"] = base_url.rstrip("/") + item["file_path"]
            out.append(item)
        return {"ok": True, "video_id": src["id"], "downloaded": True, "verified": True, "rights": rights,
                "quality_cap_short_side": quality, "title": (meta.get("title") or "")[:120],
                "license": meta.get("license"), "source_url": meta.get("webpage_url") or src["url"],
                "files": out, "compatible": ({"ok": True, "method": compat["method"], "lossless": compat["lossless"]}
                                             if compat.get("ok") else {"ok": False, "error": compat.get("error")}),
                "expires_in_seconds": FILE_TTL, "requires_bearer_header": True}
    finally:
        if not keep:
            shutil.rmtree(folder, ignore_errors=True)
        _BUSY.release()


_SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]+")


def ingest_upload(stream, length: int, filename: str = "", source_url: str = "", base_url: str = "") -> dict:
    """A file the owner's own device downloaded (a-Shell / Cinema C) and sent here: verify, keep, serve.

    The platform download happened on the owner's network; this only receives the bytes."""
    if length <= 0:
        return {"ok": False, "error": "LENGTH_REQUIRED"}
    if length > UPLOAD_MB * 1024 * 1024:
        return {"ok": False, "error": "FILE_TOO_LARGE", "limit_mb": UPLOAD_MB}
    prune()
    folder = Path(tempfile.mkdtemp(prefix=TEMP_PREFIX))
    keep = False
    try:
        stem = _SAFE_NAME.sub("_", Path(filename or "upload.mp4").stem)[:60] or "upload"
        suffix = Path(filename or "x.mp4").suffix.lower()
        suffix = suffix if suffix in (".mp4", ".mov", ".m4v", ".webm", ".mkv") else ".mp4"
        original = folder / ("upload" + suffix)
        h = hashlib.sha256()
        left = length
        with open(original, "wb") as fp:
            while left > 0:
                chunk = stream.read(min(1 << 20, left))
                if not chunk:
                    break
                fp.write(chunk)
                h.update(chunk)
                left -= len(chunk)
        if left:
            return {"ok": False, "error": "UPLOAD_INCOMPLETE", "missing_bytes": left}
        check = verify(original)
        if not check.get("ok"):
            return {"ok": False, "error": check.get("error"), "verify": check}
        files = {}
        ticket, entry = _file_entry(original, check, "original", f"{stem}.original{suffix}")
        files[ticket] = entry
        compat = make_compatible(original, check, folder)
        if compat.get("ok"):
            t2, e2 = _file_entry(compat["path"], compat["media"], "compatible", f"{stem}.mp4")
            e2.update(method=compat["method"], lossless=compat["lossless"])
            files[t2] = e2
        job_id = secrets.token_hex(8)
        created = time.time()
        with _LOCK:
            _JOBS[job_id] = {"folder": str(folder), "expires": created + UPLOAD_TTL, "files": files,
                             "kind": "upload", "created": created, "name": stem,
                             "source_url": source_url[:300] if source_url.startswith("https://") else ""}
        keep = True
        return {"ok": True, "upload_id": job_id, "verified": True, "files": _public_files(files, base_url),
                "expires_in_seconds": UPLOAD_TTL}
    finally:
        if not keep:
            shutil.rmtree(folder, ignore_errors=True)


def _public_files(files: dict, base_url: str = "") -> list[dict]:
    out = []
    for t, e in files.items():
        item = {k: v for k, v in e.items() if k != "path"}
        item["file_path"] = "/v1/files/" + t
        if base_url:
            item["url"] = base_url.rstrip("/") + item["file_path"]
        out.append(item)
    return out


def inbox(base_url: str = "") -> dict:
    """Uploads still held, newest first."""
    prune()
    with _LOCK:
        jobs = [(k, j) for k, j in _JOBS.items() if j.get("kind") == "upload"]
    jobs.sort(key=lambda kj: kj[1]["created"], reverse=True)
    return {"ok": True, "uploads": [{"upload_id": k, "name": j["name"], "source_url": j["source_url"],
                                     "age_seconds": int(time.time() - j["created"]),
                                     "expires_in_seconds": int(j["expires"] - time.time()),
                                     "files": _public_files(j["files"], base_url)} for k, j in jobs]}


def status() -> dict:
    prune()
    with _LOCK:
        left = max(0, int(_STATE["blocked_until"] - time.time()))
        return {"service": "KOSIF Media Gateway", "version": VERSION, "alive": True,
                "dependencies": dependencies(),
                "youtube": {"last_result": _STATE["last_youtube"], "cooldown_seconds": left},
                "youtube_download_verified": _STATE["verified_downloads"] > 0,
                "verified_downloads_since_start": _STATE["verified_downloads"],
                "limits": {"max_mb": MAX_MB, "upload_mb": UPLOAD_MB, "upload_ttl_seconds": UPLOAD_TTL, "downloads_per_hour": PER_HOUR, "file_ttl_seconds": FILE_TTL,
                           "download_timeout_seconds": DOWNLOAD_TIMEOUT, "concurrent_downloads": 1,
                           "attempts_last_hour": len(_ATTEMPTS)},
                "allowed_hosts": sorted(allowed_hosts()), "uptime_seconds": int(time.time() - _STATE["started"])}


def public_probe() -> dict:
    """Unauthenticated, fixed-video reachability check, at most once per KOSIF_PUBLIC_PROBE_EVERY seconds."""
    with _LOCK:
        due = time.time() - _STATE["public_probe_at"] >= PUBLIC_PROBE_EVERY
        if due:
            _STATE["public_probe_at"] = time.time()
    if not due:
        return {"skipped": "RECENTLY_CHECKED", "last_result": _STATE["last_youtube"]}
    r = probe(PUBLIC_PROBE_VIDEO, media_check=True)
    return {k: r.get(k) for k in ("ok", "video_id", "error", "detail", "cooldown_seconds", "duration", "media_access",
                                  "width", "height", "video_formats", "h264_formats") if k in r}


# ---------------------------------------------------------------- MCP

MCP_VERSIONS = ("2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05")
_SOURCE_DESC = "YouTube id (11 chars), a YouTube/Shorts/youtu.be URL, or an https URL on an allowed host"
TOOLS = [
    {"name": "gateway_status",
     "description": "Gateway health, real dependency checks, limits and the last YouTube result / cool-down.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
     "annotations": {"readOnlyHint": True, "openWorldHint": False}},
    {"name": "list_uploads",
     "description": "Videos the owner's own device downloaded and sent to the gateway (POST /v1/upload), newest "
                    "first, each verified with a real decoder, with bearer-protected links to the original and an H.264/AAC MP4.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
     "annotations": {"readOnlyHint": True, "openWorldHint": False}},
    {"name": "probe_youtube",
     "description": "Read-only check whether the gateway host can read a video's metadata without signing in. "
                    "Reports LOGIN_REQUIRED / HTTP_429 / HTTP_403 / PROXY_502 exactly; never bypasses them.",
     "inputSchema": {"type": "object", "properties": {
         "video": {"type": "string", "description": _SOURCE_DESC},
         "media_check": {"type": "boolean", "default": False,
                         "description": "Also read the first ~10 KB of a real stream; metadata alone does not prove a download will work"}},
         "required": ["video"], "additionalProperties": False},
     "annotations": {"readOnlyHint": True, "openWorldHint": True}},
    {"name": "download_permitted_video",
     "description": "Download a video you own or are licensed to use, verify it with a real decoder, and return "
                    "bearer-protected links to the original file and an H.264/AAC MP4 (lossless remux when possible). "
                    f"Max {MAX_MB} MB, one at a time, {PER_HOUR} per hour, files expire after {FILE_TTL} s.",
     "inputSchema": {"type": "object", "properties": {
         "video": {"type": "string", "description": _SOURCE_DESC},
         "rights": {"type": "string", "enum": list(RIGHTS), "description": "Why you may download it"},
         "quality": {"type": "integer", "enum": list(QUALITIES), "default": 720,
                     "description": "Cap on the shorter side (portrait 1080x1920 counts as 1080)"}},
         "required": ["video", "rights"], "additionalProperties": False},
     "annotations": {"readOnlyHint": False, "destructiveHint": False, "openWorldHint": True}},
]


def _rpc_error(reqid, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": reqid, "error": {"code": code, "message": message}}


def mcp_handle(msg, base_url: str = "") -> dict | None:
    """One JSON-RPC message -> response dict, or None for notifications and client responses."""
    if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0":
        return _rpc_error(msg.get("id") if isinstance(msg, dict) else None, -32600, "Invalid Request")
    if "method" not in msg:
        return None                           # a response from the client; nothing to answer
    method, reqid = msg.get("method"), msg.get("id")
    if "id" not in msg:
        return None                           # notification (initialized, cancelled, ...)
    params = msg.get("params") or {}
    if not isinstance(params, dict):
        return _rpc_error(reqid, -32602, "params must be an object")
    if method == "initialize":
        asked = str(params.get("protocolVersion", ""))
        result = {"protocolVersion": asked if asked in MCP_VERSIONS else MCP_VERSIONS[0],
                  "capabilities": {"tools": {"listChanged": False}},
                  "serverInfo": {"name": "kosif-media-gateway", "version": VERSION},
                  "instructions": "Use gateway_status first. Download only with a real rights reason. "
                                  "A YouTube block is reported, never bypassed."}
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        name, args = params.get("name"), params.get("arguments") or {}
        if not isinstance(args, dict):
            return _rpc_error(reqid, -32602, "arguments must be an object")
        if name == "gateway_status":
            payload = status()
            payload["ok"] = True
        elif name == "list_uploads":
            payload = inbox(base_url)
        elif name == "probe_youtube":
            payload = probe(str(args.get("video", "")), bool(args.get("media_check")))
        elif name == "download_permitted_video":
            payload = download(str(args.get("video", "")), str(args.get("rights", "")),
                               args.get("quality", 720), base_url)
        else:
            return _rpc_error(reqid, -32602, f"Unknown tool: {name}")
        result = {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}],
                  "structuredContent": payload, "isError": not payload.get("ok")}
    else:
        return _rpc_error(reqid, -32601, f"Method not found: {method}")
    return {"jsonrpc": "2.0", "id": reqid, "result": result}


# ---------------------------------------------------------------- HTTP

class Gateway(BaseHTTPRequestHandler):
    server_version = "KOSIF-Gateway/" + VERSION
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args) -> None:
        # Never log headers (bearer token) or request bodies; method + path + status only.
        if os.environ.get("KOSIF_ACCESS_LOG") == "1":
            sys.stderr.write(f"{self.command} {urllib.parse.urlsplit(self.path).path.split('/v1/files/')[0]} {args[1] if len(args) > 1 else ''}\n")

    def _send(self, status_code: int, payload, headers: dict | None = None) -> None:
        content = b"" if payload is None else json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status_code)
        if payload is not None:
            self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        if self.close_connection:
            self.send_header("Connection", "close")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if content and self.command != "HEAD":
            self.wfile.write(content)

    def _authorized(self) -> bool:
        key = os.environ.get("KOSIF_GATEWAY_TOKEN", "")
        raw = self.headers.get("Authorization", "")
        return bool(key) and hmac.compare_digest(raw.encode(), ("Bearer " + key).encode())

    def _deny(self) -> None:
        self._send(401, {"ok": False, "error": "AUTH_REQUIRED"}, {"WWW-Authenticate": 'Bearer realm="kosif-media-gateway"'})

    def _base_url(self) -> str:
        ext = os.environ.get("RENDER_EXTERNAL_URL") or os.environ.get("KOSIF_PUBLIC_URL")
        if ext:
            return ext
        host = self.headers.get("Host", "")
        return ("http://" + host) if re.fullmatch(r"[A-Za-z0-9.\-]+(:\d+)?", host) else ""

    def _body(self):
        """(object, error code) with a hard size cap; reads nothing unbounded."""
        try:
            size = int(self.headers.get("Content-Length", "-1"))
        except ValueError:
            return None, "LENGTH_REQUIRED"
        if size < 0:
            return None, "LENGTH_REQUIRED"
        if size > MAX_BODY:
            return None, "BODY_TOO_LARGE"
        try:
            return json.loads(self.rfile.read(size) or b"null"), None
        except (ValueError, UnicodeError):
            return None, "INVALID_JSON"

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        prune()
        parts = urllib.parse.urlsplit(self.path)
        path = parts.path
        if path in ("/", "/health", "/healthz"):
            body = status()
            if "deep=1" in parts.query:
                body["public_probe"] = public_probe()
            self._send(200, body)
            return
        static = {"/browser": ("browser.html", "text/html; charset=utf-8"),
                  "/browser/": ("browser.html", "text/html; charset=utf-8"),
                  "/kosif-send.sh": ("kosif-send.sh", "text/plain; charset=utf-8")}
        if path in static:
            fname, ctype = static[path]
            page = (Path(__file__).resolve().parent / "static" / fname).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(page)))
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(page)
            return
        if path == "/mcp":
            self._send(405, {"error": "SSE_STREAM_NOT_SUPPORTED"}, {"Allow": "POST"})
            return
        if path.startswith("/.well-known/"):
            self._send(404, {"error": "NO_OAUTH_USE_BEARER_HEADER"})
            return
        if not self._authorized():
            self._deny()
            return
        if path == "/v1/inbox":
            self._send(200, inbox(self._base_url()))
            return
        if not path.startswith("/v1/files/"):
            self._send(404, {"error": "NOT_FOUND"})
            return
        meta = find_file(path.rsplit("/", 1)[-1])
        if not meta or not Path(meta["path"]).is_file():
            self._send(404, {"error": "FILE_EXPIRED_OR_MISSING"})
            return
        self.send_response(200)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Content-Disposition", f'attachment; filename="{meta["filename"]}"')
        self.send_header("Content-Length", str(meta["size_bytes"]))
        self.send_header("X-Content-SHA256", meta["sha256"])
        self.send_header("Cache-Control", "private, no-store")
        self.end_headers()
        if self.command == "HEAD":
            return
        with open(meta["path"], "rb") as fp:
            try:
                shutil.copyfileobj(fp, self.wfile, length=1 << 20)
            except (BrokenPipeError, ConnectionResetError):
                pass

    def handle_expect_100(self):
        """curl sends `Expect: 100-continue` for big bodies: refuse a bad token or an oversized upload
        before the phone sends a single byte."""
        if not self._authorized():
            self.close_connection = True
            self._deny()
            return False
        if urllib.parse.urlsplit(self.path).path == "/v1/upload":
            try:
                length = int(self.headers.get("Content-Length", "-1"))
            except ValueError:
                length = -1
            if length > UPLOAD_MB * 1024 * 1024:
                self.close_connection = True
                self._send(413, {"ok": False, "error": "FILE_TOO_LARGE", "limit_mb": UPLOAD_MB})
                return False
        return super().handle_expect_100()

    def _upload(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", "-1"))
        except ValueError:
            length = -1
        if not self._authorized():
            self.close_connection = True       # the body is not read
            self._deny()
            return
        if length < 0 or length > UPLOAD_MB * 1024 * 1024:
            self.close_connection = True
            self._send(413 if length > 0 else 411, {"ok": False, "error": "FILE_TOO_LARGE" if length > 0 else "LENGTH_REQUIRED",
                                                    "limit_mb": UPLOAD_MB})
            return
        if not _BUSY.acquire(blocking=False):
            self.close_connection = True
            self._send(409, {"ok": False, "error": "BUSY_ONE_DOWNLOAD_AT_A_TIME", "retry_after_seconds": 30},
                       {"Retry-After": "30"})
            return
        try:
            name = urllib.parse.unquote(self.headers.get("X-Filename", ""))[:200]
            src = urllib.parse.unquote(self.headers.get("X-Source-Url", ""))[:300]
            out = ingest_upload(self.rfile, length, name, src, self._base_url())
        finally:
            _BUSY.release()
        if out.get("error") == "UPLOAD_INCOMPLETE":
            self.close_connection = True
        self._send(200 if out.get("ok") else 422, out)

    def do_DELETE(self):
        if urllib.parse.urlsplit(self.path).path == "/mcp":
            self._send(405, {"error": "STATELESS_NO_SESSION"}, {"Allow": "POST"})
        else:
            self._send(405, {"error": "METHOD_NOT_ALLOWED"})

    def do_POST(self):
        route = urllib.parse.urlsplit(self.path).path
        if route == "/v1/upload":
            self._upload()
            return
        # Read (bounded) before answering, so an early 401 never leaves body bytes on a keep-alive
        # connection; anything unread closes the connection instead.
        data, err = self._body()
        if err in ("BODY_TOO_LARGE", "LENGTH_REQUIRED"):
            self.close_connection = True
        if not self._authorized():
            self._deny()
            return
        if err:
            self._send(413 if err == "BODY_TOO_LARGE" else 411 if err == "LENGTH_REQUIRED" else 400,
                       {"ok": False, "error": err} if route != "/mcp" else _rpc_error(None, -32700, "Parse error: " + err))
            return
        if route == "/mcp":
            if isinstance(data, list):
                if not data:
                    self._send(400, _rpc_error(None, -32600, "Empty batch"))
                    return
                replies = [r for r in (mcp_handle(m, self._base_url()) for m in data) if r is not None]
                self._send(200, replies) if replies else self._send(202, None)
                return
            reply = mcp_handle(data, self._base_url())
            self._send(200, reply) if reply is not None else self._send(202, None)
            return
        if not isinstance(data, dict):
            self._send(400, {"ok": False, "error": "JSON_OBJECT_REQUIRED"})
            return
        source = str(data.get("video") or data.get("url") or "")
        if route == "/v1/probe":
            out = probe(source, bool(data.get("media_check")))
        elif route == "/v1/download":
            out = download(source, str(data.get("rights", "")), data.get("quality", 720), self._base_url())
        elif route == "/v1/status":
            out = {**status(), "ok": True}
        else:
            self._send(404, {"ok": False, "error": "NOT_FOUND"})
            return
        self._send(http_status(out), out, {"Retry-After": str(out["retry_after_seconds"])} if out.get("retry_after_seconds") else None)


def http_status(out: dict) -> int:
    if out.get("ok"):
        return 200
    e = str(out.get("error", ""))
    if e in ("INVALID_SOURCE", "EXPLICIT_DOWNLOAD_PERMISSION_REQUIRED", "INVALID_QUALITY"):
        return 400
    if e == "BUSY_ONE_DOWNLOAD_AT_A_TIME":
        return 409
    if e == "RATE_LIMIT_PER_HOUR" or out.get("cooldown_seconds"):
        return 429
    if e in ("DOWNLOAD_TIMEOUT", "PROBE_TIMEOUT"):
        return 504
    return 422


def make_server(port: int, host: str = "0.0.0.0") -> ThreadingHTTPServer:
    srv = ThreadingHTTPServer((host, port), Gateway)
    srv.daemon_threads = True
    return srv


def _janitor() -> None:
    while True:
        time.sleep(60)
        prune()


if __name__ == "__main__":
    if not os.environ.get("KOSIF_GATEWAY_TOKEN"):
        raise SystemExit("KOSIF_GATEWAY_TOKEN must be configured")
    if len(os.environ["KOSIF_GATEWAY_TOKEN"]) < 32:
        print("warning: KOSIF_GATEWAY_TOKEN is shorter than 32 characters; rotate it", file=sys.stderr)
    clean_stale_temp()
    threading.Thread(target=_janitor, daemon=True).start()
    make_server(int(os.environ.get("PORT", "8000"))).serve_forever()
