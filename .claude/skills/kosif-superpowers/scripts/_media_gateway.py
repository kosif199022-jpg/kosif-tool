#!/usr/bin/env python3
"""Client for the owner's KOSIF Media Gateway (services/kosif-media-gateway, hosted on Render Free).

    python3 _media_gateway.py health
    python3 _media_gateway.py probe dYrEeavC3cw [--media-check]
    python3 _media_gateway.py download URL_OR_ID --rights cc-licensed [--quality 720] [-o DIR]

fetch_video.py uses it with --gateway RIGHTS. Settings come from the environment only:
KOSIF_GATEWAY_URL (default below) and KOSIF_GATEWAY_TOKEN (never printed, logged or written).
Every downloaded file is checked against the gateway's SHA-256 and size and written atomically;
a mismatch deletes it. The gateway reports YouTube blocks; nothing here tries to get around them.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

DEFAULT_URL = "https://kosif-media-gateway-free-20261030.onrender.com"
RIGHTS = ("owned", "written-permission", "public-domain", "cc-licensed", "youtube-authorized")


class GatewayError(RuntimeError):
    pass


def config() -> tuple[str, str]:
    base = os.environ.get("KOSIF_GATEWAY_URL", DEFAULT_URL).rstrip("/")
    u = urlsplit(base)
    if u.scheme != "https" and u.hostname not in ("127.0.0.1", "localhost"):
        raise GatewayError("KOSIF_GATEWAY_URL must be https")
    return base, os.environ.get("KOSIF_GATEWAY_TOKEN", "")


def available() -> bool:
    try:
        return bool(config()[1])
    except GatewayError:
        return False


def _call(method: str, path: str, payload: dict | None = None, timeout: int = 330) -> tuple[int, dict]:
    base, token = config()
    headers = {"Accept": "application/json"}
    if path not in ("/health",):
        if not token:
            raise GatewayError("set KOSIF_GATEWAY_TOKEN in the environment")
        headers["Authorization"] = "Bearer " + token
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(base + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.load(e)
        except ValueError:
            return e.code, {"ok": False, "error": f"HTTP_{e.code}"}
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return 0, {"ok": False, "error": "GATEWAY_UNREACHABLE", "detail": str(getattr(e, "reason", e))[:200]}


def health(deep: bool = False) -> dict:
    return _call("GET", "/health?deep=1" if deep else "/health", timeout=120)[1]


def probe(video: str, media_check: bool = False) -> dict:
    return _call("POST", "/v1/probe", {"video": video, "media_check": media_check}, timeout=150)[1]


def _fetch(file_path: str, dest: Path, sha256: str, size: int) -> Path:
    base, token = config()
    tmp = dest.with_name(dest.name + ".part")
    req = urllib.request.Request(base + file_path, headers={"Authorization": "Bearer " + token})
    h = hashlib.sha256()
    got = 0
    try:
        with urllib.request.urlopen(req, timeout=300) as r, open(tmp, "wb") as fp:
            for chunk in iter(lambda: r.read(1 << 20), b""):
                fp.write(chunk)
                h.update(chunk)
                got += len(chunk)
    except (urllib.error.URLError, OSError) as e:
        tmp.unlink(missing_ok=True)
        raise GatewayError(f"file transfer failed: {getattr(e, 'reason', e)}") from e
    if got != size or h.hexdigest() != sha256:
        tmp.unlink(missing_ok=True)
        raise GatewayError("file transfer incomplete or SHA-256 mismatch; nothing kept")
    tmp.replace(dest)
    return dest


def download(video: str, out_dir: str | Path, rights: str, quality: int = 720) -> dict:
    """Ask the gateway to download and verify, then pull the original and the compatible MP4."""
    if rights not in RIGHTS:
        raise GatewayError("rights must be one of: " + ", ".join(RIGHTS))
    code, res = _call("POST", "/v1/download", {"video": video, "rights": rights, "quality": quality})
    rec = {"url": video, "provider": "kosif-media-gateway", "rights": rights, "file": None}
    if not res.get("ok"):
        rec.update(error=res.get("error") or f"HTTP_{code}", detail=res.get("detail"),
                   cooldown_seconds=res.get("cooldown_seconds"))
        if str(res.get("error", "")).startswith("YOUTUBE_"):
            rec["blocked"] = True
            rec["hint"] = ("The gateway host was refused by YouTube too (" + str(res.get("error")) + "). "
                           "No bypass is attempted: use your own device or upload the file.")
        return rec
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for f in res["files"]:
        dest = out / f["filename"]
        _fetch(f["file_path"], dest, f["sha256"], f["size_bytes"])
        rec["original_file" if f["role"] == "original" else "safe_file"] = str(dest)
        if f["role"] == "original":
            rec.update({k: f["media"].get(k) for k in ("duration", "width", "height", "vcodec", "acodec", "fps")})
            rec["sha256"] = f["sha256"]
    rec["file"] = rec.get("safe_file") or rec.get("original_file")
    rec.update(title=res.get("title"), license=res.get("license"), source_url=res.get("source_url"),
               verified=True, compatible=res.get("compatible"))
    return rec


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["health", "probe", "download"])
    ap.add_argument("video", nargs="?", default="dYrEeavC3cw")
    ap.add_argument("--rights", choices=RIGHTS)
    ap.add_argument("--quality", type=int, default=720, choices=(360, 480, 720, 1080))
    ap.add_argument("--media-check", action="store_true", help="probe: also read ~10 KB of a real stream")
    ap.add_argument("--deep", action="store_true", help="health: include the gateway's own fixed-video check")
    ap.add_argument("-o", "--out", default="downloads")
    a = ap.parse_args(argv)
    try:
        if a.action == "health":
            res = health(a.deep)
        elif a.action == "probe":
            res = probe(a.video, a.media_check)
        else:
            if not a.rights:
                ap.error("--rights is required for download")
            res = download(a.video, a.out, a.rights, a.quality)
    except GatewayError as e:
        res = {"ok": False, "error": str(e)}
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if (res.get("ok") or res.get("alive") or res.get("file")) else 2


if __name__ == "__main__":
    sys.exit(main())
