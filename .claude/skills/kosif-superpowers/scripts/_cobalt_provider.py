#!/usr/bin/env python3
"""Opt-in Cobalt gateway for owned/licensed YouTube videos.

The user must explicitly supply a Cobalt instance whose operator authorizes API
access. This gateway makes no direct YouTube requests, but the provider still
needs the video's canonical URL. It is NOT a guarantee that YouTube works;
DRM, login, geo, anti-bot and provider errors are not bypassed.
"""
from __future__ import annotations

import hashlib
import ipaddress
import json
import os
import re
import shutil
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

_VIDEO_ID = re.compile(r"^[a-zA-Z0-9_-]{11}$")
_RIGHTS = frozenset({"owned", "direct-permission", "public-domain", "cc0", "cc-by", "cc-by-sa"})
_MAX_REPLY = 1000000
_MAX_DOWNLOAD = 750 * 1024 * 1024


class GatewayError(RuntimeError):
    pass


def youtube_id(value: str) -> str | None:
    """Accept a bare 11-character ID, watch, Shorts, live, embed or youtu.be URL."""
    if _VIDEO_ID.fullmatch(value):
        return value
    try:
        u = urllib.parse.urlsplit(value)
    except ValueError:
        return None
    host = (u.hostname or "").lower().rstrip(".")
    if u.scheme not in ("http", "https") or u.username or u.password:
        return None
    if host == "youtu.be":
        result = u.path.strip("/").split("/")[0]
    elif host in ("youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com"):
        path = u.path.strip("/").split("/")
        if path[:1] == ["watch"]:
            result = urllib.parse.parse_qs(u.query).get("v", [""])[0]
        elif path[:1] and path[0] in ("shorts", "embed", "live") and len(path) == 2:
            result = path[1]
        else:
            return None
    else:
        return None
    return result if _VIDEO_ID.fullmatch(result) else None


def canonical_url(source: str) -> str:
    vid = youtube_id(source)
    if not vid:
        raise GatewayError("unsupported YouTube URL or ID")
    return "https://www.youtube.com/watch?v=" + vid


def _endpoint(raw: str, allow_loopback: bool = False) -> str:
    try:
        u = urllib.parse.urlsplit(raw)
    except ValueError as e:
        raise GatewayError("invalid gateway endpoint") from e
    host = (u.hostname or "").lower().rstrip(".")
    loopback = host in ("localhost", "127.0.0.1", "::1")
    if not host or u.username or u.password or u.query or u.fragment or u.path not in ("", "/"):
        raise GatewayError("gateway must be an API root with no credentials, query or path")
    if u.scheme != "https" and not (allow_loopback and loopback and u.scheme == "http"):
        raise GatewayError("HTTPS required (HTTP loopback allowed for local tests only)")
    try:
        addr = ipaddress.ip_address(host)
    except ValueError:
        addr = None
    if addr and not addr.is_global and not (allow_loopback and addr.is_loopback):
        raise GatewayError("private or reserved gateway IP prohibited")
    if loopback and not allow_loopback:
        raise GatewayError("loopback gateway requires the explicit local test flag")
    return raw.rstrip("/")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise GatewayError("gateway attempted an unexpected redirect")


def _open(request, timeout=35):
    return urllib.request.build_opener(_NoRedirect()).open(request, timeout=timeout)


def _checked_tunnel(api: str, url: str) -> str:
    try:
        root, media = urllib.parse.urlsplit(api), urllib.parse.urlsplit(url)
    except ValueError as e:
        raise GatewayError("invalid tunnel URL") from e
    if (root.scheme, root.netloc.lower()) != (media.scheme, media.netloc.lower()):
        raise GatewayError("gateway did not return a same-origin tunnel")
    if not media.path.startswith("/tunnel") or media.username or media.password or media.fragment:
        raise GatewayError("gateway did not return a valid tunnel")
    return url


def download(source: str, out: str | Path, api: str, *, rights: str, quality: str = "1080",
             key_env: str = "KOSIF_COBALT_API_KEY", allow_loopback: bool = False,
             max_bytes: int = _MAX_DOWNLOAD) -> dict:
    """Download via authorized gateway, check MP4 with ffprobe, and produce a receipt."""
    if rights not in _RIGHTS:
        raise GatewayError("explicit owned/licensed rights required")
    vid = youtube_id(source)
    if not vid:
        raise GatewayError("unsupported YouTube ID or URL")
    api = _endpoint(api, allow_loopback=allow_loopback)
    quality = str(quality).strip().lower()
    if quality not in {"best", "2160", "1440", "1080", "720", "480", "360"}:
        raise GatewayError("unsupported Cobalt video quality")
    key = os.environ.get(key_env, "") if key_env else ""
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    if key:
        headers["Authorization"] = "Api-Key " + key
    body = json.dumps({"url": canonical_url(source), "videoQuality": "max" if quality == "best" else quality,
                       "youtubeVideoCodec": "h264", "youtubeVideoContainer": "mp4",
                       "downloadMode": "auto", "alwaysProxy": True}).encode()
    req = urllib.request.Request(api + "/", body, headers=headers, method="POST")
    try:
        with _open(req) as reply:
            raw = reply.read(_MAX_REPLY + 1)
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise GatewayError("gateway request failed: " + type(e).__name__) from e
    if len(raw) > _MAX_REPLY:
        raise GatewayError("gateway JSON response too large")
    try:
        result = json.loads(raw)
    except (ValueError, UnicodeError) as e:
        raise GatewayError("invalid gateway JSON") from e
    if not isinstance(result, dict):
        raise GatewayError("invalid gateway response")
    status = result.get("status")
    if status == "error":
        err = result.get("error") or {}
        code = err.get("code", "unknown") if isinstance(err, dict) else "unknown"
        raise GatewayError("gateway rejected the video: " + str(code)[:120])
    if status != "tunnel":
        raise GatewayError("gateway returned " + repr(status) + ", not a verified tunnel")
    tunnel = _checked_tunnel(api, str(result.get("url", "")))
    target = Path(out)
    target.mkdir(parents=True, exist_ok=True)
    dest = target / ("youtube-" + vid + ".mp4")
    part = target / (".youtube-" + vid + ".part")
    digest = hashlib.sha256()
    total = 0
    try:
        request = urllib.request.Request(tunnel, headers={"Accept": "video/*,application/octet-stream"})
        with _open(request, timeout=90) as stream, part.open("wb") as f:
            announced = stream.headers.get("Content-Length", "")
            if announced.isdecimal() and int(announced) > max_bytes:
                raise GatewayError("video exceeds configured size limit")
            while True:
                block = stream.read(1024 * 1024)
                if not block:
                    break
                total += len(block)
                if total > max_bytes:
                    raise GatewayError("video exceeds configured size limit")
                f.write(block)
                digest.update(block)
        if total < 512:
            raise GatewayError("response too small to be video")
        if not shutil.which("ffprobe"):
            raise GatewayError("ffprobe required to verify media")
        proc = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(part)],
                              capture_output=True, text=True, timeout=30)
        if proc.returncode:
            raise GatewayError("downloaded data is not readable media")
        metadata = json.loads(proc.stdout)
        video = next((s for s in metadata.get("streams", []) if s.get("codec_type") == "video"), None)
        if not video:
            raise GatewayError("no video stream found")
        duration = float(metadata.get("format", {}).get("duration", 0))
        if duration <= 0:
            raise GatewayError("invalid video duration")
        part.replace(dest)
        return {"url": canonical_url(source), "file": str(dest), "provider": "cobalt-opt-in", "id": vid,
                "verified": True, "rights": rights, "sha256": digest.hexdigest(), "bytes": total,
                "duration": duration, "width": video.get("width"), "height": video.get("height"),
                "vcodec": video.get("codec_name"), "source_host": "youtube.com"}
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise GatewayError("gateway tunnel failed: " + type(e).__name__) from e
    finally:
        part.unlink(missing_ok=True)
