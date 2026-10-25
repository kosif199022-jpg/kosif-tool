#!/usr/bin/env python3
"""Download dependencies: check them, install them, and explain a blocked download.

    python3 scripts/_deps.py            # report yt-dlp, yt-dlp-ejs, curl_cffi, instaloader, ffmpeg (never fails)
    python3 scripts/_deps.py install    # pip install whatever is missing (quiet, never fails)

Stdlib only. The SessionStart hook (.claude/hooks/session-start.sh) runs `install` in cloud sessions,
so a fresh session can download TikTok/YouTube/Instagram links without a manual pip step.
Set KOSIF_NO_AUTOINSTALL=1 to turn every automatic install off.
"""
from __future__ import annotations

import importlib
import importlib.util
import os
import shutil
import site
import subprocess
import sys

# python module -> pip package. All four are pure pip installs; no system-wide or paid installs here.
# yt-dlp-ejs carries the YouTube JS challenge solver; without it YouTube drops most formats (yt-dlp >= 2025.11).
DOWNLOAD_DEPS = {"yt_dlp": "yt-dlp", "yt_dlp_ejs": "yt-dlp-ejs", "curl_cffi": "curl_cffi", "instaloader": "instaloader"}


def has_module(mod: str) -> bool:
    try:
        return importlib.util.find_spec(mod) is not None
    except (ImportError, ValueError):
        return False


def missing(mods=None) -> list[str]:
    return [m for m in (mods or DOWNLOAD_DEPS) if not has_module(m)]


def autoinstall_allowed() -> bool:
    """Install on our own only in Claude Code cloud sessions (fresh, throwaway machines), never on a user's computer or in CI."""
    if os.environ.get("KOSIF_NO_AUTOINSTALL"):
        return False
    return os.environ.get("CLAUDE_CODE_REMOTE") == "true" or bool(os.environ.get("KOSIF_AUTOINSTALL"))


def pip_install(packages: list[str], timeout: int = 240) -> bool:
    """pip install quietly; retries with --break-system-packages / --user for externally managed Pythons."""
    if not packages:
        return True
    base = [sys.executable, "-m", "pip", "install", "--quiet", "--disable-pip-version-check", "--upgrade"]
    for extra in ([], ["--break-system-packages"], ["--user", "--break-system-packages"]):
        try:
            p = subprocess.run(base + extra + packages, capture_output=True, text=True, timeout=timeout)
        except (OSError, subprocess.TimeoutExpired):
            return False
        if p.returncode == 0:
            importlib.invalidate_caches()
            try:  # a --user install lands in a directory this process may not have on sys.path yet
                user_site = site.getusersitepackages()
                if user_site not in sys.path:
                    sys.path.append(user_site)
            except AttributeError:
                pass
            return True
        out = (p.stderr + p.stdout).lower()
        if "externally-managed" not in out and "permission denied" not in out and "--user" not in out:
            return False  # a real failure (no network, no wheel): another flag will not fix it
    return False


def ensure(mods=None, quiet: bool = True) -> list[str]:
    """Install missing modules when allowed. Returns what is still missing afterwards."""
    gone = missing(mods)
    if gone and autoinstall_allowed():
        if not quiet:
            print("installing: " + " ".join(DOWNLOAD_DEPS.get(m, m) for m in gone), file=sys.stderr)
        pip_install([DOWNLOAD_DEPS.get(m, m) for m in gone])
        gone = missing(gone)
    return gone


# ------------------------------------------------------------------ blocked downloads
# Messages a site sends when it refuses a cloud/datacenter request. We report them plainly and stop:
# no bot-check or login circumvention, ever.
BLOCK_MARKERS = (
    "sign in to confirm", "not a bot", "confirm you're not a bot", "captcha", "bot check", "verify you are human",
    "ip address is blocked", "your ip", "blocked", "http error 403", "403: forbidden", "http error 429", "too many requests",
    "rate-limit", "rate limit", "login required", "requested content is not available", "log in for access",
    "this content isn't available", "geo restriction", "not available in your country",
)


def is_blocked(err: str) -> bool:
    e = (err or "").lower()
    return any(m in e for m in BLOCK_MARKERS)


def blocked_hint(url: str = "") -> str:
    site_name = next((s for s in ("tiktok", "instagram", "youtube", "facebook", "twitter", "x.com") if s in (url or "").lower()), "the site")
    return (f"{site_name} refused this download from the cloud machine (bot check / IP block). This is not a bug and "
            "will not be bypassed. Options: (1) run the same command on your own computer, signed in to the site in your browser: "
            "python3 .claude/skills/kosif-superpowers/scripts/fetch_video.py URL --cookies-from-browser chrome  "
            "(or firefox/safari/edge); (2) download the video in the app and upload the file here, then work from the file. | "
            f"الموقع ({site_name}) رفض التحميل من جهاز السحابة. الحل: شغّل نفس الأمر على جهازك مع --cookies-from-browser، "
            "أو نزّل الفيديو من التطبيق وارفعه هنا.")


def report() -> dict:
    return {**{DOWNLOAD_DEPS[m]: has_module(m) for m in DOWNLOAD_DEPS},
            "yt-dlp (cli)": bool(shutil.which("yt-dlp")), "ffmpeg": bool(shutil.which("ffmpeg")), "ffprobe": bool(shutil.which("ffprobe"))}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["install"]:
        gone = missing()
        if gone:
            ok = pip_install([DOWNLOAD_DEPS[m] for m in gone])
            print(("installed: " if ok else "could not install (no network?): ") + " ".join(DOWNLOAD_DEPS[m] for m in gone))
    for k, v in report().items():
        print(f"[{'ok' if v else '--'}] {k}")
    if not shutil.which("ffmpeg"):
        print("ffmpeg missing: apt-get install -y ffmpeg (Linux) or brew install ffmpeg (macOS); needed for merging and audio extraction")
    return 0  # a report, never a failure: one missing tool must not break a chained command


if __name__ == "__main__":
    sys.exit(main())
