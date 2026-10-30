#!/usr/bin/env bash
# yt_get.sh <youtube-url> [out-dir]
#
# KOSIF / USIP download tool for YouTube (and anything else yt-dlp supports).
# Runs on YOUR device (Mac, PC, a-Shell on iPhone), from a home internet connection.
# Writes the video plus a receipt.json that the protocol can check.
#
# Chain (stops at the first step that produces a playable file):
#   1. yt-dlp as-is            (needs a JS runtime: deno or node, YouTube requires it since 2025)
#   2. yt-dlp + your cookies   (YT_COOKIES=cookies.txt, or YT_BROWSER=chrome|safari|firefox|edge|brave)
#   3. update yt-dlp, retry 1 and 2 once
#
# Env:
#   YT_QUALITY   max height, default 1080
#   YT_COOKIES   path to a Netscape cookies.txt exported from your own logged-in browser
#   YT_BROWSER   read cookies straight from this browser on this device
#   YT_AUDIO=1   audio only (m4a)
#
# Only download videos you own or have permission to use.
set -u
URL=${1:-}; OUT=${2:-$PWD/yt_downloads}
[ -z "$URL" ] && { echo "usage: yt_get.sh <url> [out-dir]"; exit 2; }
mkdir -p "$OUT" || exit 2
Q=${YT_QUALITY:-1080}
LOG="$OUT/yt_get.log"; : > "$LOG"
say() { printf '%s\n' "$*" | tee -a "$LOG"; }
have() { command -v "$1" >/dev/null 2>&1; }

# ---------- preflight ----------
if have yt-dlp; then YTDLP=(yt-dlp)
elif python3 -c 'import yt_dlp' 2>/dev/null; then YTDLP=(python3 -m yt_dlp)
else  # auto-install, like Cinema C V13 ensure_ytdlp
  say "yt-dlp missing -> installing with pip"
  python3 -m pip install --disable-pip-version-check -q -U 'yt-dlp[default]' >>"$LOG" 2>&1 \
    && YTDLP=(python3 -m yt_dlp) || { say "install failed -> run: python3 -m pip install -U 'yt-dlp[default]'"; exit 3; }
fi
have ffmpeg || say "WARN: ffmpeg missing, falling back to single-file formats (lower quality)."
JS=""
for r in deno node bun qjs quickjs; do have $r && { JS=$r; break; }; done
[ -z "$JS" ] && say "WARN: no JS runtime (deno/node/quickjs). YouTube often fails without one -> install deno: https://deno.com"
JSARGS=(); [ -n "$JS" ] && [ "$JS" != deno ] && JSARGS=(--js-runtimes "$( [ "$JS" = qjs ] && echo quickjs:$(command -v qjs) || echo $JS )")

if [ "${YT_AUDIO:-0}" = 1 ]; then FMT=(-f "ba[ext=m4a]/ba" -x --audio-format m4a)
elif have ffmpeg; then FMT=(-f "bv*[height<=$Q][vcodec^=avc1]+ba[ext=m4a]/bv*[height<=$Q]+ba/b[height<=$Q]/b" --merge-output-format mp4)
else FMT=(-f "b[height<=$Q]/b"); fi

COOK=()
if [ -n "${YT_COOKIES:-}" ]; then
  head -1 "$YT_COOKIES" 2>/dev/null | grep -q 'HTTP Cookie File' || say "WARN: $YT_COOKIES has no Netscape header."
  COOK=(--cookies "$YT_COOKIES")
elif [ -n "${YT_BROWSER:-}" ]; then COOK=(--cookies-from-browser "$YT_BROWSER"); fi

run() {  # $1 = step name, rest = extra args
  local step=$1; shift
  say "== step: $step"
  "${YTDLP[@]}" --no-playlist --newline --retries 5 --fragment-retries 10 "${JSARGS[@]}" \
    "${FMT[@]}" "$@" -o "$OUT/%(title).80B [%(id)s].%(ext)s" \
    --print after_move:filepath "$URL" 2>>"$LOG" | tail -1 > "$OUT/.last"
  local f; f=$(cat "$OUT/.last" 2>/dev/null)
  [ -n "$f" ] && [ -s "$f" ] && { FILE=$f; STEP=$step; return 0; }
  say "   failed: $(grep -m1 -E 'ERROR' "$LOG" | cut -c1-160)"
  return 1
}

FILE=""; STEP=""
attempt() {
  run plain && return 0
  [ ${#COOK[@]} -gt 0 ] && run cookies "${COOK[@]}" && return 0
  return 1
}
attempt || {
  say "== updating yt-dlp and retrying"
  "${YTDLP[@]}" -U >>"$LOG" 2>&1 || python3 -m pip install -q -U 'yt-dlp[default]' >>"$LOG" 2>&1
  attempt
}

if [ -z "$FILE" ]; then
  say "FAIL. Most likely fixes, in order:"
  grep -q 'not a bot\|Sign in' "$LOG" && say " - YouTube wants a login: YT_BROWSER=chrome yt_get.sh '$URL'  (be logged in to YouTube in that browser)"
  [ -z "$JS" ] && say " - install deno: curl -fsSL https://deno.land/install.sh | sh"
  say " - you are probably on a cloud/VPN IP. Run this on your own device and home connection."
  printf '{"tool":"yt_get","url":"%s","ok":false,"log":"%s"}\n' "$URL" "$LOG" > "$OUT/receipt.json"
  exit 1
fi

# ---------- verify + receipt ----------
# Like Cinema C V22 strict verify: the file must really be media with a duration, not an HTML error page.
if have ffprobe; then
  D0=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$FILE" 2>/dev/null | cut -d. -f1)
  if [ -z "$D0" ] || [ "$D0" = N/A ]; then
    say "FAIL verify: $FILE is not readable media"
    printf '{"tool":"yt_get","url":"%s","ok":false,"reason":"verify"}\n' "$URL" > "$OUT/receipt.json"; exit 4
  fi
fi

# ---------- Photos-safe copy (idea from Cinema C) ----------
# h264 + aac plays everywhere (iPhone Photos, Premiere, browsers). Copy streams if already so,
# otherwise re-encode once. The original download is kept.
if [ "${YT_AUDIO:-0}" != 1 ] && have ffprobe && have ffmpeg; then
  VC=$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 "$FILE")
  AC=$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 "$FILE")
  SAFE="$(dirname "$FILE")/PhotosSafe_$(basename "${FILE%.*}").mp4"
  if [ "$VC" = h264 ] && { [ -z "$AC" ] || [ "$AC" = aac ]; }; then
    say "Photos-safe: already h264/${AC:-none}, copying streams (no quality loss)"
    ffmpeg -loglevel error -y -i "$FILE" -c copy -movflags +faststart "$SAFE" 2>>"$LOG"
  else
    say "Photos-safe: source is $VC/$AC, re-encoding to h264/aac"
    ffmpeg -loglevel error -y -i "$FILE" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
      -c:a aac -b:a 192k -movflags +faststart "$SAFE" 2>>"$LOG"
  fi
  [ -s "$SAFE" ] && say "Photos-safe MP4: $SAFE" || SAFE=""
fi

DUR=""; RES=""
if have ffprobe; then
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$FILE")
  RES=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "$FILE")
fi
SHA=$( (sha256sum "$FILE" 2>/dev/null || shasum -a 256 "$FILE") | cut -d' ' -f1)
SIZE=$(wc -c < "$FILE" | tr -d ' ')
python3 - "$URL" "$FILE" "$STEP" "$SIZE" "$SHA" "$DUR" "$RES" "$OUT/receipt.json" "${SAFE:-}" <<'PY'
import json, sys, datetime
u, f, step, size, sha, dur, res, out, safe = sys.argv[1:]
json.dump({"tool": "yt_get", "ok": True, "url": u, "file": f, "step": step, "photos_safe": safe or None,
           "bytes": int(size), "sha256": sha, "duration_s": dur or None,
           "resolution": res or None,
           "at": datetime.datetime.now(datetime.timezone.utc).isoformat()},
          open(out, "w"), ensure_ascii=False, indent=2)
PY
say "OK ($STEP): $FILE"
say "receipt: $OUT/receipt.json"
