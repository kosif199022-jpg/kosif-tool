"""Optional, explicitly opt-in SnapAny YouTube proxy provider for KOSIF.

Official API: https://platform.snapany.com/docs/youtube-proxy-download
The provider charges prepaid credits. No requests without user's opt-in:
KOSIF_SNAPANY_ENABLED=1 + KOSIF_SNAPANY_API_KEY + per-request confirm_credits.
No CAPTCHA/DRM bypass, no cookies, no bulk extraction, and no auto-pay.
"""
from __future__ import annotations
import json
import os
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

_ENDPOINT = "https://api.snapany.com/openapi/v1/youtube/proxy-download"
_RIGHTS = {"owned", "written-permission", "public-domain", "cc-licensed", "youtube-authorized"}
_QUALITIES = {360, 480, 720, 1080}
_LOCK = threading.Lock()
_BUSY = threading.Lock()
_TIMES: list[float] = []
_VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")


def configured() -> bool:
    return bool(os.environ.get("KOSIF_SNAPANY_API_KEY")) and os.environ.get("KOSIF_SNAPANY_ENABLED") == "1"


def status() -> dict:
    with _LOCK:
        now = time.time()
        _TIMES[:] = [x for x in _TIMES if now - x < 86400]
        used = len(_TIMES)
    return {
        "provider": "SnapAny official API",
        "configured": configured(),
        "enabled": os.environ.get("KOSIF_SNAPANY_ENABLED") == "1",
        "requires_per_request_credit_confirmation": True,
        "calls_last_24h": used,
        "max_calls_per_24h": 2,
        "credits": "Provider quotes 4 credits per 10 minutes, rounded up. Confirm pricing yourself.",
        "billing": "Prepaid, not free unlimited. Disable auto top-up in the provider console.",
    }


def _video_id(raw: str) -> str | None:
    raw = (raw or "").strip()
    if _VIDEO_ID.fullmatch(raw):
        return raw
    try:
        u = urllib.parse.urlsplit(raw)
        if u.scheme != "https" or u.username or u.password or u.port not in (None, 443):
            return None
        hostname = (u.hostname or "").lower().rstrip(".")
        parts = [x for x in u.path.split("/") if x]
        if hostname == "youtu.be" and len(parts) == 1:
            candidate = parts[0]
        elif hostname in {"youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com"}:
            if parts == ["watch"]:
                candidate = urllib.parse.parse_qs(u.query).get("v", [""])[0]
            elif len(parts) == 2 and parts[0] in ("shorts", "live", "embed"):
                candidate = parts[1]
            else:
                return None
        else:
            return None
    except ValueError:
        return None
    return candidate if _VIDEO_ID.fullmatch(candidate) else None


def _safe_media_url(raw) -> str | None:
    if not isinstance(raw, str) or len(raw) > 4096:
        return None
    try:
        u = urllib.parse.urlsplit(raw)
    except ValueError:
        return None
    # Only provider supplied HTTPS URLs are exposed to users, never fetched by our backend.
    if u.scheme != "https" or not u.hostname or u.username or u.password:
        return None
    host = u.hostname.lower().rstrip(".")
    if host in {"localhost", "0.0.0.0"} or host.endswith((".localhost", ".local", ".internal")):
        return None
    return raw


def resolve(video: str, rights: str, quality: int, confirm_credits: bool) -> dict:
    vid = _video_id(video)
    if not vid:
        return {"ok": False, "error": "INVALID_YOUTUBE_URL"}
    if rights not in _RIGHTS:
        return {"ok": False, "error": "DOWNLOAD_RIGHTS_REQUIRED"}
    if quality not in _QUALITIES:
        return {"ok": False, "error": "INVALID_QUALITY"}
    if confirm_credits is not True:
        return {"ok": False, "error": "CREDIT_SPEND_CONFIRMATION_REQUIRED"}
    if not configured():
        return {"ok": False, "error": "SNAPANY_NOT_CONFIGURED",
                "setup": "Create SnapAny free account and put SNAPANY API key in Render KOSIF_SNAPANY_API_KEY; set KOSIF_SNAPANY_ENABLED=1 only after approval."}
    if not _BUSY.acquire(blocking=False):
        return {"ok": False, "error": "PROVIDER_BUSY"}
    try:
        with _LOCK:
            now = time.time()
            _TIMES[:] = [t for t in _TIMES if now - t < 86400]
            if len(_TIMES) >= 2:
                return {"ok": False, "error": "PROVIDER_DAILY_LIMIT", "retry_after_seconds": int(86400-(now-_TIMES[0]))}
            _TIMES.append(now)  # reserve a slot before hitting a billable endpoint
        request = urllib.request.Request(
            _ENDPOINT,
            method="POST",
            data=json.dumps({"url": "https://www.youtube.com/watch?v=" + vid}).encode("utf-8"),
            headers={
                "Authorization": "Bearer " + os.environ["KOSIF_SNAPANY_API_KEY"],
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "KOSIF-Media-Gateway/0.2",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=55) as resp:
                raw = resp.read(1024 * 1024 + 1)
                if len(raw) > 1024 * 1024:
                    return {"ok": False, "error": "PROVIDER_RESPONSE_TOO_LARGE"}
                data = json.loads(raw)
        except urllib.error.HTTPError as exc:
            # Never echo vendor error body: could include URL tokens or secrets.
            return {"ok": False, "error": {
                401: "PROVIDER_BAD_API_KEY", 402: "PROVIDER_CREDITS_EXHAUSTED",
                403: "PROVIDER_ACCESS_DENIED", 429: "PROVIDER_RATE_LIMIT",
            }.get(exc.code, "PROVIDER_HTTP_ERROR"), "provider_http_status": exc.code}
        except (urllib.error.URLError, TimeoutError, ValueError, OSError):
            return {"ok": False, "error": "PROVIDER_NETWORK_OR_RESPONSE_ERROR"}
        if not isinstance(data, dict):
            return {"ok": False, "error": "PROVIDER_BAD_RESPONSE"}
        options = []
        for media in data.get("medias", [])[:15]:
            if not isinstance(media, dict) or media.get("media_type") != "video":
                continue
            for variant in (media.get("variants") or [])[:25]:
                if not isinstance(variant, dict):
                    continue
                try:
                    q = int(variant.get("quality", 0))
                except (TypeError, ValueError):
                    continue
                if q <= 0 or q > quality:
                    continue
                vurl = _safe_media_url(variant.get("video_proxy_url"))
                aurl = _safe_media_url(variant.get("audio_proxy_url"))
                if vurl:
                    options.append({
                        "quality": q, "fps": variant.get("fps"),
                        "video_proxy_url": vurl, "audio_proxy_url": aurl,
                        "video_ext": str(variant.get("video_ext", ""))[:12],
                        "audio_ext": str(variant.get("audio_ext", ""))[:12],
                        "requires_mux": bool(aurl),
                    })
            murl = _safe_media_url(media.get("resource_proxy_url"))
            if murl:
                options.append({"quality": None, "video_proxy_url": murl, "audio_proxy_url": None,
                                "requires_mux": False, "source": "resource"})
        options.sort(key=lambda x: x.get("quality") or 0, reverse=True)
        return {
            "ok": bool(options),
            "error": None if options else "PROVIDER_NO_PROXY_URL",
            "provider": "SnapAny",
            "video_id": vid,
            "title": str(data.get("title", ""))[:160],
            "rights": rights,
            "downloaded": False,  # Important: links returned; file transfer not yet proven.
            "credits_may_have_been_charged": True,
            "links_are_temporary": True,
            "options": options[:16],
        }
    finally:
        _BUSY.release()
