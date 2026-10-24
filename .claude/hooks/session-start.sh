#!/bin/bash
# Installs the download tools (yt-dlp, curl_cffi, instaloader) at the start of every Claude Code cloud session,
# so TikTok/YouTube/Instagram links work without a manual pip step. Never fails the session.
# Local machines are left alone unless KOSIF_AUTOINSTALL=1; KOSIF_NO_AUTOINSTALL=1 turns it off everywhere.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ] && [ -z "${KOSIF_AUTOINSTALL:-}" ]; then exit 0; fi
if [ -n "${KOSIF_NO_AUTOINSTALL:-}" ]; then exit 0; fi
DIR="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
timeout 300 python3 "$DIR/.claude/skills/kosif-superpowers/scripts/_deps.py" install >/dev/null 2>&1 || true
if ! command -v ffmpeg >/dev/null 2>&1 && command -v apt-get >/dev/null 2>&1 && [ "$(id -u)" = "0" ]; then
  timeout 240 bash -c 'apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg' >/dev/null 2>&1 || true
fi
exit 0
