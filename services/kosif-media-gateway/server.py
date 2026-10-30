#!/usr/bin/env python3
"""KOSIF Media Gateway: minimal authenticated, bounded, no-bypass video service.

Uses standard HTTP + JSON-RPC MCP. Only attempts access YouTube currently
allows without authentication. Never sends browser cookies, rotates IPs, or
bypasses DRM/CAPTCHA. Files are temporary and not publicly exposed.
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

_VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
_RIGHTS = {"owned", "written-permission", "public-domain", "cc-licensed", "youtube-authorized"}
_LIMIT = 45 * 1024 * 1024
_JOBS: dict[str, tuple[str, float, int, str]] = {}
_LOCK = threading.Lock()
_DOWNLOAD_BUSY = threading.Lock()
_LAST_TIMES: list[float] = []


def video_id(source: str) -> str | None:
    if _VIDEO_ID.fullmatch(source):
        return source
    try:
        u = urllib.parse.urlsplit(source)
    except ValueError:
        return None
    if u.scheme != "https" or u.username or u.password:
        return None
    host = (u.hostname or "").lower().rstrip(".")
    path = u.path.strip("/").split("/")
    if host == "youtu.be" and len(path) == 1:
        candidate = path[0]
    elif host in ("youtube.com", "www.youtube.com", "m.youtube.com") and path == ["watch"]:
        candidate = urllib.parse.parse_qs(u.query).get("v", [""])[0]
    elif host in ("youtube.com", "www.youtube.com", "m.youtube.com") and len(path) == 2 and path[0] in ("shorts", "live", "embed"):
        candidate = path[1]
    else:
        return None
    return candidate if _VIDEO_ID.fullmatch(candidate) else None


def _ffmpeg() -> str | None:
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return shutil.which("ffmpeg")


def _execute(args: list[str], timeout: int) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)


def _sanitize_error(output: str) -> str:
    s = output[-1500:]
    if "Sign in to confirm" in s or "not a bot" in s:
        return "YOUTUBE_LOGIN_REQUIRED: the hosting IP is blocked; do not bypass login/CAPTCHA"
    if "429" in s:
        return "YOUTUBE_HTTP_429: rate limit at YouTube, no bypass attempted"
    if "403" in s:
        return "YOUTUBE_HTTP_403: permission denied by video host"
    if "DRM" in s.upper():
        return "DRM_OR_RESTRICTED: protected content is not downloadable here"
    return "DOWNLOAD_FAILED: " + re.sub(r"https?://\S+", "[url]", s)[-420:]


def _base_yt_args(vid: str) -> list[str]:
    return [
        sys.executable, "-m", "yt_dlp", "--no-config", "--no-playlist",
        "--no-warnings", "--retries", "1", "--fragment-retries", "1",
        "--extractor-retries", "1", "--socket-timeout", "12",
        "--", "https://www.youtube.com/watch?v=" + vid,
    ]


def probe(source: str) -> dict:
    vid = video_id(source)
    if not vid:
        return {"ok": False, "error": "INVALID_VIDEO_ID"}
    args = _base_yt_args(vid)
    args[-2:-2] = ["--skip-download", "--print", "%(id)s|%(duration)s|%(title).90s"]
    try:
        p = _execute(args, 40)
    except subprocess.TimeoutExpired:
        return {"ok": False, "video_id": vid, "error": "PROBE_TIMEOUT"}
    if p.returncode:
        return {"ok": False, "video_id": vid, "error": _sanitize_error(p.stderr)}
    return {"ok": True, "video_id": vid, "metadata": p.stdout[-300:].strip(), "downloaded": False}


def _prune() -> None:
    now = time.time()
    with _LOCK:
        for k, (path, until, _, _) in list(_JOBS.items()):
            if now >= until:
                Path(path).unlink(missing_ok=True)
                try:
                    Path(path).parent.rmdir()
                except OSError:
                    pass
                del _JOBS[k]
        _LAST_TIMES[:] = [t for t in _LAST_TIMES if now - t < 3600]


def download(source: str, rights: str) -> dict:
    vid = video_id(source)
    if not vid:
        return {"ok": False, "error": "INVALID_VIDEO_ID"}
    if rights not in _RIGHTS:
        return {"ok": False, "error": "EXPLICIT_DOWNLOAD_PERMISSION_REQUIRED"}
    _prune()
    with _LOCK:
        if len(_LAST_TIMES) >= 3:
            return {"ok": False, "error": "FREE_TIER_RATE_LIMIT_3_PER_HOUR"}
        _LAST_TIMES.append(time.time())
    if not _DOWNLOAD_BUSY.acquire(blocking=False):
        return {"ok": False, "error": "ALREADY_DOWNLOADING_ONE_AT_A_TIME"}
    folder = tempfile.mkdtemp(prefix="kosif-media-")
    destination = Path(folder) / (vid + ".mp4")
    try:
        ffmpeg = _ffmpeg()
        if not ffmpeg:
            return {"ok": False, "error": "FFMPEG_NOT_INSTALLED"}
        args = [
            sys.executable, "-m", "yt_dlp", "--no-config", "--no-playlist",
            "--no-warnings", "--retries", "1", "--fragment-retries", "1",
            "--extractor-retries", "1", "--socket-timeout", "12",
            "--max-filesize", "45M",
            "-f", "bv*+ba/b", "-S", "res:720,fps,vcodec:h264,acodec:aac",
            "--merge-output-format", "mp4", "--ffmpeg-location", ffmpeg,
            "-o", str(Path(folder) / "%(id)s.%(ext)s"),
            "--", "https://www.youtube.com/watch?v=" + vid
        ]
        try:
            p = _execute(args, 105)
        except subprocess.TimeoutExpired:
            return {"ok": False, "video_id": vid, "error": "DOWNLOAD_TIMEOUT"}
        if p.returncode:
            return {"ok": False, "video_id": vid, "error": _sanitize_error(p.stderr)}
        if not destination.is_file() or not (1024 <= destination.stat().st_size <= _LIMIT):
            return {"ok": False, "video_id": vid, "error": "NO_VALID_MP4_OR_SIZE_LIMIT"}
        try:
            verify = _execute([ffmpeg, "-nostdin", "-hide_banner", "-loglevel", "error",
                               "-i", str(destination), "-map", "0:v:0", "-frames:v", "1",
                               "-f", "null", "-"], 20)
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": "VERIFY_TIMEOUT"}
        if verify.returncode:
            return {"ok": False, "error": "VIDEO_DECODE_FAILED"}
        digest = hashlib.sha256(destination.read_bytes()).hexdigest()
        ticket = secrets.token_urlsafe(24)
        with _LOCK:
            _JOBS[ticket] = (str(destination), time.time() + 600, destination.stat().st_size, digest)
        return {"ok": True, "video_id": vid, "downloaded": True,
                "file_path": "/v1/files/" + ticket, "expires_in_seconds": 600,
                "size_bytes": destination.stat().st_size, "sha256": digest,
                "requires_bearer_header": True}
    finally:
        if not any(Path(entry[0]) == destination for entry in _JOBS.values()):
            shutil.rmtree(folder, ignore_errors=True)
        _DOWNLOAD_BUSY.release()


class Gateway(BaseHTTPRequestHandler):
    server_version = "KOSIF-Gateway/0.1"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args) -> None:
        # Never log authorization headers or user video IDs.
        pass

    def _json(self, status: int, payload: dict):
        content = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def _authorized(self) -> bool:
        key = os.environ.get("KOSIF_GATEWAY_TOKEN", "")
        raw = self.headers.get("Authorization", "")
        return bool(key) and hmac.compare_digest(raw, "Bearer " + key)

    def _body(self) -> dict | None:
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size < 2 or size > 8192:
                return None
            obj = json.loads(self.rfile.read(size))
            return obj if isinstance(obj, dict) else None
        except (ValueError, UnicodeError, OSError):
            return None

    def do_GET(self):
        _prune()
        path = urllib.parse.urlsplit(self.path).path
        if path == "/health":
            try:
                import yt_dlp
                installed = True
            except ImportError:
                installed = False
            self._json(200, {"service": "KOSIF Media Gateway", "alive": True,
                             "yt_dlp": installed, "ffmpeg": bool(_ffmpeg()),
                             "youtube_download_verified": False})
            return
        if not self._authorized():
            self._json(401, {"error": "AUTH_REQUIRED"})
            return
        if not path.startswith("/v1/files/"):
            self._json(404, {"error": "NOT_FOUND"})
            return
        ticket = path.rsplit("/", 1)[-1]
        with _LOCK:
            entry = _JOBS.get(ticket)
        if not entry or not Path(entry[0]).is_file():
            self._json(404, {"error": "FILE_EXPIRED_OR_MISSING"})
            return
        fpath, _, size, _ = entry
        self.send_response(200)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Content-Disposition", "attachment; filename=kosif-video.mp4")
        self.send_header("Content-Length", str(size))
        self.send_header("Cache-Control", "private, no-store")
        self.end_headers()
        with open(fpath, "rb") as fp:
            shutil.copyfileobj(fp, self.wfile, length=1024 * 1024)

    def do_POST(self):
        if not self._authorized():
            self._json(401, {"error": "AUTH_REQUIRED"})
            return
        data = self._body()
        if data is None:
            self._json(400, {"error": "INVALID_JSON_OR_TOO_LARGE"})
            return
        route = urllib.parse.urlsplit(self.path).path
        if route in ("/v1/probe", "/v1/download"):
            source = str(data.get("video", ""))
            out = probe(source) if route.endswith("probe") else download(source, str(data.get("rights", "")))
            self._json(200 if out.get("ok") else 422, out)
            return
        if route == "/mcp":
            method = data.get("method", "")
            reqid = data.get("id")
            if method == "notifications/initialized":
                self.send_response(202)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            if method == "initialize":
                result = {"protocolVersion": "2025-03-26",
                          "capabilities": {"tools": {}},
                          "serverInfo": {"name": "kosif-media-gateway", "version": "0.1.0"}}
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": [
                    {"name": "probe_youtube", "description": "Read-only connectivity check; no login, cookies or bypass.",
                     "inputSchema": {"type": "object", "properties": {"video": {"type": "string"}}, "required": ["video"]}},
                    {"name": "download_permitted_video", "description": "Download only when expressly authorized; max 45 MB, one at a time, 3/hour, no restrictions bypass.",
                     "inputSchema": {"type": "object", "properties": {
                         "video": {"type": "string"}, "rights": {"type": "string", "enum": sorted(_RIGHTS)}},
                         "required": ["video", "rights"]}}
                ]}
            elif method == "tools/call":
                params = data.get("params") or {}
                name = params.get("name")
                args = params.get("arguments") or {}
                if name == "probe_youtube":
                    payload = probe(str(args.get("video", "")))
                elif name == "download_permitted_video":
                    payload = download(str(args.get("video", "")), str(args.get("rights", "")))
                else:
                    payload = {"ok": False, "error": "UNKNOWN_TOOL"}
                result = {"content": [{"type": "text", "text": json.dumps(payload)}], "isError": not payload.get("ok")}
            else:
                self._json(200, {"jsonrpc": "2.0", "id": reqid,
                                 "error": {"code": -32601, "message": "METHOD_NOT_FOUND"}})
                return
            self._json(200, {"jsonrpc": "2.0", "id": reqid, "result": result})
            return
        self._json(404, {"error": "NOT_FOUND"})


if __name__ == "__main__":
    if not os.environ.get("KOSIF_GATEWAY_TOKEN"):
        raise SystemExit("KOSIF_GATEWAY_TOKEN must be configured")
    port = int(os.environ.get("PORT", "8000"))
    ThreadingHTTPServer(("0.0.0.0", port), Gateway).serve_forever()
