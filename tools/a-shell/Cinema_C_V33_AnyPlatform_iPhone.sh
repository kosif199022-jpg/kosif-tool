#!/bin/sh
# Cinema C V33 — AnyPlatform — iPhone / a-Shell
# Built on V32 AudioLab (all proven paths kept). New in V33:
# - Photos SAFE no longer dies when the iPhone hardware encoder fails
#   (h264_videotoolbox -12903) on an a-Shell ffmpeg without libx264:
#     1) instant lossless REMUX when the file is already H.264/HEVC
#        (most TikTok/Instagram/YouTube<=1080p downloads) - no encoding at all
#     2) hardware H.264 -> hardware H.264 at <=1080p -> hardware HEVC
#        -> libx264 (only if this ffmpeg has it) -> built-in MPEG-4
#     every encoder is checked in `ffmpeg -encoders` before use
# - Smarter quality selection: prefers H.264/HEVC + AAC on every site
#   (TikTok reports "h264", not "avc1"), so Photos usually needs no re-encode
# - Paste a whole share text: the URL is extracted; empty Enter = clipboard
# - Several files from one post (carousels) are all kept, none refused
# - Failed download -> offers to update yt-dlp and retries once
# - c --safe [FILE] : rebuild Photos SAFE for a file you already downloaded
# - c --doctor      : live test of every encoder on THIS iPhone
#
# New in V32:
# - 11) AUDIO LAB: voice only / music only / both / video without music /
#        video without voice / AI studio stems (Demucs) / original audio
# - c --lab [FILE] : process a file you already downloaded (no internet)
# - Download auto-recovery: simple-format retry -> browser impersonation retry
# - c --update : update yt-dlp (fixes most TikTok/Instagram extractor errors)
# Recovery release based on historically proven behavior:
# - V17 UX: c -> URL -> quality -> Photos/Files -> exact downloaded file
# - V11/Cinema_Photos output discovery: unique work directory, no --print-to-file
# - Manual Photos: create a separate Photos-safe MP4, then open it
#
# Photos SAFE normalization:
# - H.264 video
# - AAC audio
# - yuv420p pixel format
# - MP4 +faststart
# - original download preserved
# - no ffprobe dependency

set -u

APP='Cinema C'
VERSION='33.0-AnyPlatform-iPhone'

HOME_DIR=${HOME:-.}
BIN_DIR="$HOME_DIR/Documents/bin"
DOWNLOAD_DIR=${CINEMA_DOWNLOAD_DIR:-"$HOME_DIR/Documents/Cinema_Downloads"}
STATE_DIR="$HOME_DIR/Documents/.cinema"

CONNECTIONS=${CINEMA_CONNECTIONS:-8}
INPUT=''
INSTALL=0
COOKIES=''
YTDLP=''
SAVE_MODE='ask'   # ask | photos | files
OUTPUT_FILE=''
PHOTOS_SAFE_FILE=''
WORK_DIR=''

# Facebook profile batch state (isolated from the proven single-video path)
FB_PROFILE_ID=''
FB_BATCH_DIR=''
FB_LINKS_FILE=''
FB_ARCHIVE_FILE=''
FB_SCAN_DIR=''
FB_SOCKET_TIMEOUT=${CINEMA_FB_SOCKET_TIMEOUT:-6}
FB_IMPERSONATE=''
FB_LOGIN_REQUIRED=0
FB_STATUS=''
FB_LAST_LOG=''
FB_DEBUG=0
FB_SETUP_COOKIES=0
FB_DOCTOR=0

# V32 Audio Lab / maintenance flags
LAB_LOCAL=0
LAB_FILE=''
LAB_MODE=''
LAB_LAST=''
LAB_DOCTOR=0
SETUP_AI=0
DO_UPDATE=0

# V33 flags
SAFE_LOCAL=0
SAFE_FILE=''
DOCTOR=0
OUTPUTS=''        # newline list of every completed file of the last download
ENC_CACHE=''
SAFE_LOG=''

say() { printf '%s\n' "$*"; }
err() { printf 'ERROR: %s\n' "$*" >&2; }
warn() { printf 'WARN: %s\n' "$*" >&2; }
have() { command -v "$1" >/dev/null 2>&1; }

usage() {
  say 'Cinema C V33 — AnyPlatform — iPhone / a-Shell'
  say ''
  say 'Daily use:'
  say '  c'
  say ''
  say 'Single video (TikTok, Instagram, YouTube, X, Facebook, Snapchat, ...):'
  say '  paste a video/reel URL (or the whole share text) -> quality -> Photos SAFE or Files'
  say '  press Enter on an empty prompt to use the URL in the clipboard'
  say ''
  say 'Fix a file you already downloaded for Photos:'
  say '  c --safe               (pick from Cinema_Downloads)'
  say '  c --safe "file.mp4"'
  say ''
  say 'Facebook profile:'
  say '  paste: https://www.facebook.com/profile.php?id=NUMERIC_ID'
  say '  Cinema checks whether Facebook exposes the profile to this shell.'
  say '  If Facebook redirects to LOGIN, Cinema stops cleanly and asks for cookies.'
  say ''
  say 'Audio Lab (separate voice / music):'
  say '  c  -> paste URL -> 11'
  say '  c --lab                (pick a file from Cinema_Downloads)'
  say '  c --lab "file.mp4"     (process a specific file, offline)'
  say '  c --setup-ai           (optional studio-quality AI stems)'
  say '  c --lab-doctor'
  say ''
  say 'Maintenance:'
  say '  c --update             (update yt-dlp; fixes most site errors)'
  say '  c --doctor             (tests yt-dlp, ffmpeg and every encoder on this iPhone)'
  say ''
  say 'Install once:'
  say '  sh ./Cinema_C_V33_AnyPlatform_iPhone.sh --install'
  say ''
  say 'Facebook authentication:'
  say '  c --setup-facebook-cookies'
  say '  c --cookies facebook_cookies.txt "PROFILE_URL"'
  say ''
  say 'Diagnostics:'
  say '  c --fb-doctor'
  say '  c --fb-debug "PROFILE_URL"'
  say '  c --version'
  say ''
  say 'Important: Facebook profile-wide enumeration is best-effort.'
  say 'Cinema never claims that hidden/dynamic videos were all discovered.'
}

cleanup() {
  status=$?
  if [ -n "${WORK_DIR:-}" ] && [ -d "$WORK_DIR" ]; then
    rm -rf "$WORK_DIR" 2>/dev/null || true
  fi
  exit "$status"
}
trap cleanup EXIT INT TERM

find_ytdlp() {
  if have yt-dlp && yt-dlp --version >/dev/null 2>&1; then
    YTDLP='yt-dlp'
    return 0
  fi
  if have yt_dlp && yt_dlp --version >/dev/null 2>&1; then
    YTDLP='yt_dlp'
    return 0
  fi
  return 1
}

run_ytdlp() {
  "$YTDLP" "$@"
}

validate_connections() {
  case "$CONNECTIONS" in
    ''|*[!0-9]*)
      err '-N must be a whole number from 1 to 16.'
      exit 1
      ;;
  esac
  [ "$CONNECTIONS" -ge 1 ] && [ "$CONNECTIONS" -le 16 ] || {
    err '-N must be from 1 to 16.'
    exit 1
  }

  case "$FB_SOCKET_TIMEOUT" in
    ''|*[!0-9]*)
      err 'CINEMA_FB_SOCKET_TIMEOUT must be a whole number.'
      exit 1
      ;;
  esac
  [ "$FB_SOCKET_TIMEOUT" -ge 3 ] && [ "$FB_SOCKET_TIMEOUT" -le 15 ] || {
    err 'CINEMA_FB_SOCKET_TIMEOUT must be from 3 to 15 seconds.'
    exit 1
  }

}

validate_cookie_file() {
  [ -z "$COOKIES" ] && return 0

  [ -f "$COOKIES" ] || {
    err "Cookies file not found: $COOKIES"
    return 1
  }

  first_line=$(sed -n '1p' "$COOKIES" 2>/dev/null || true)
  case "$first_line" in
    '# Netscape HTTP Cookie File'|'# HTTP Cookie File')
      return 0
      ;;
  esac

  warn 'Cookies file does not start with a Netscape/Mozilla cookie header.'
  say 'Expected first line: # Netscape HTTP Cookie File'
  return 1
}


setup_facebook_cookies() {
  say 'Facebook profile authentication setup'
  say '-------------------------------------'
  say 'Facebook may redirect profile pages to LOGIN when the shell is not authenticated.'
  say ''
  say 'Cinema accepts a yt-dlp cookies file in Netscape/Mozilla format.'
  say 'Recommended filename in a-Shell Documents:'
  say '  facebook_cookies.txt'
  say ''
  say 'The first line must be one of:'
  say '  # Netscape HTTP Cookie File'
  say '  # HTTP Cookie File'
  say ''
  say 'Then run:'
  say '  c --cookies facebook_cookies.txt "PROFILE_URL"'
  say ''
  say 'If Documents/facebook_cookies.txt exists and is valid, plain `c` can use it automatically for a Facebook profile.'
  say ''
  say 'SECURITY: cookies are login credentials. Do not share this file.'
}

maybe_use_default_facebook_cookies() {
  [ -n "$COOKIES" ] && return 0

  default_cookie="$HOME_DIR/Documents/facebook_cookies.txt"
  [ -f "$default_cookie" ] || return 0

  previous_cookie=$COOKIES
  COOKIES=$default_cookie
  if validate_cookie_file >/dev/null 2>&1; then
    say '[C][auth] Using Documents/facebook_cookies.txt'
    return 0
  fi

  COOKIES=$previous_cookie
  return 0
}

parse_args() {
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --install)
        INSTALL=1
        shift
        ;;
      --photos)
        SAVE_MODE='photos'
        shift
        ;;
      --files)
        SAVE_MODE='files'
        shift
        ;;
      -N)
        [ "$#" -ge 2 ] || { err '-N needs a number'; exit 1; }
        CONNECTIONS=$2
        shift 2
        ;;
      --cookies)
        [ "$#" -ge 2 ] || { err '--cookies needs a file'; exit 1; }
        COOKIES=$2
        shift 2
        ;;
      --output)
        [ "$#" -ge 2 ] || { err '--output needs a folder'; exit 1; }
        DOWNLOAD_DIR=$2
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      --fb-doctor)
        FB_DOCTOR=1
        shift
        ;;
      --fb-debug)
        FB_DEBUG=1
        shift
        ;;
      --setup-facebook-cookies)
        FB_SETUP_COOKIES=1
        shift
        ;;
      --lab)
        LAB_LOCAL=1
        shift
        if [ "$#" -gt 0 ]; then
          case "$1" in -*) ;; *) LAB_FILE=$1; shift ;; esac
        fi
        ;;
      --lab-doctor)
        LAB_DOCTOR=1
        shift
        ;;
      --setup-ai)
        SETUP_AI=1
        shift
        ;;
      --update)
        DO_UPDATE=1
        shift
        ;;
      --safe)
        SAFE_LOCAL=1
        shift
        if [ "$#" -gt 0 ]; then
          case "$1" in -*) ;; *) SAFE_FILE=$1; shift ;; esac
        fi
        ;;
      --doctor)
        DOCTOR=1
        shift
        ;;
      --version)
        say "$APP $VERSION"
        exit 0
        ;;
      -*)
        err "Unknown option: $1"
        exit 1
        ;;
      *)
        [ -z "$INPUT" ] && INPUT=$1
        shift
        ;;
    esac
  done
  validate_connections
  validate_cookie_file || exit 1
}

install_self() {
  mkdir -p "$BIN_DIR" || { err "Cannot create $BIN_DIR"; exit 1; }
  cp "$0" "$BIN_DIR/c" || { err 'Install failed'; exit 1; }
  chmod +x "$BIN_DIR/c" 2>/dev/null || true
  have rehash && rehash >/dev/null 2>&1 || true
  say "OK: $APP $VERSION installed."
  say 'From now on type: c'
  say 'Photos SAFE needs no Shortcut; ffmpeg builds a compatibility MP4 first.'
  say 'Facebook profile mode is best-effort; LOGIN redirects become AUTH_REQUIRED.'
  say 'For Facebook cookies help: c --setup-facebook-cookies'
  say 'For diagnostics: c --fb-doctor'
  say 'Audio Lab: menu option 11, or c --lab for files already downloaded.'
  say 'NEW: Photos SAFE remuxes H.264/HEVC instantly and survives encoder failures.'
  say 'NEW: c --safe fixes an existing download; c --doctor tests this iPhone.'
}

prompt_url() {
  if [ -z "$INPUT" ]; then
    say ''
    printf 'Paste video URL (Enter = clipboard): '
    IFS= read -r INPUT || INPUT=''
  fi

  INPUT=$(printf '%s' "$INPUT" | tr -d '\r')
  if [ -z "$INPUT" ] && have pbpaste; then
    INPUT=$(pbpaste 2>/dev/null | tr -d '\r' | tr '\n' ' ')
    [ -z "$INPUT" ] || say '[C] Using the clipboard.'
  fi

  # Share sheets paste "caption... https://vt.tiktok.com/xyz/ ..." - keep
  # only the first http(s) link and drop trailing punctuation.
  url=$(printf '%s\n' "$INPUT" | grep -Eo 'https?://[^[:space:]"<>]+' | sed -n '1p')
  if [ -n "$url" ]; then
    url=$(printf '%s' "$url" | sed 's/[),.;!]*$//')
    [ "$url" = "$INPUT" ] || say "[C] URL: $url"
    INPUT=$url
  fi

  case "$INPUT" in
    http://*|https://*) ;;
    *)
      err 'Invalid URL'
      exit 1
      ;;
  esac
}


is_facebook_profile_url() {
  case "$INPUT" in
    *facebook.com/profile.php\?*id=[0-9]*|*facebook.com/profile.php\?id=[0-9]*)
      return 0
      ;;
  esac
  return 1
}

extract_facebook_profile_id() {
  FB_PROFILE_ID=$(printf '%s\n' "$INPUT" | sed -n 's/.*[?&]id=\([0-9][0-9]*\).*/\1/p' | sed -n '1p')
  [ -n "$FB_PROFILE_ID" ]
}

fb_profile_paths() {
  FB_BATCH_DIR="$DOWNLOAD_DIR/Facebook_Profile_$FB_PROFILE_ID"
  FB_LINKS_FILE="$STATE_DIR/facebook_profile_${FB_PROFILE_ID}_links.txt"
  FB_ARCHIVE_FILE="$STATE_DIR/facebook_profile_${FB_PROFILE_ID}_archive.txt"
  FB_SCAN_DIR="$STATE_DIR/facebook_scan_${FB_PROFILE_ID}_last"

  # Keep the most recent scan artifacts only. They are useful for diagnosis,
  # but old scans should not accumulate forever.
  rm -rf "$FB_SCAN_DIR" 2>/dev/null || true
  mkdir -p "$FB_BATCH_DIR" "$FB_SCAN_DIR" "$STATE_DIR" || return 1
}

detect_fb_impersonation() {
  FB_IMPERSONATE=''

  targets=$("$YTDLP" --list-impersonate-targets 2>/dev/null || true)

  # Jev Q012 favored Safari before Chrome. More importantly, V30 never
  # impersonates on the first attempt; this target is fallback-only.
  if printf '%s\n' "$targets" | grep -E '^Safari([[:space:]-]|$)' | grep -Evi 'unavailable|not available' >/dev/null 2>&1; then
    FB_IMPERSONATE='safari'
    return 0
  fi

  if printf '%s\n' "$targets" | grep -E '^Chrome([[:space:]-]|$)' | grep -Evi 'unavailable|not available' >/dev/null 2>&1; then
    FB_IMPERSONATE='chrome'
    return 0
  fi

  return 1
}

facebook_doctor() {
  say 'Cinema Facebook Doctor'
  say '----------------------'
  say "Cinema: $VERSION"

  if ! find_ytdlp; then
    say 'yt-dlp: NOT FOUND'
    return 1
  fi

  ver=$("$YTDLP" --version 2>/dev/null || printf 'unknown')
  say "yt-dlp: $ver"
  say "profile socket timeout: ${FB_SOCKET_TIMEOUT}s"
  say 'profile shell watchdog: disabled (a-Shell has no fork-based job control)'

  if detect_fb_impersonation; then
    say "browser impersonation: available ($FB_IMPERSONATE)"
  else
    say 'browser impersonation: unavailable (not fatal)'
  fi

  if have ffmpeg; then
    say 'ffmpeg: available'
  else
    say 'ffmpeg: unavailable'
  fi

  say ''
  say 'For profile-wide Facebook discovery, a login wall may require:'
  say '  c --cookies cookies.txt "PROFILE_URL"'
  say 'The cookies file must be Netscape/Mozilla format.'
  return 0
}

count_lines_file() {
  f=$1
  if [ -f "$f" ]; then
    wc -l < "$f" 2>/dev/null | tr -d ' '
  else
    printf '0'
  fi
}

parse_facebook_dump_shell() {
  page=$1
  normalized="$FB_SCAN_DIR/normalized_$$.txt"
  : > "$normalized"

  # No Python and no executable heredoc: both were removed from this release.
  # Normalize common JSON/HTML escaping before extracting candidate IDs.
  sed 's#\\/#/#g; s#\\u0026#\&#g; s#&amp;#\&#g' "$page" > "$normalized" 2>/dev/null || {
    rm -f "$normalized" 2>/dev/null || true
    return 1
  }

  # /reel/123...
  grep -Eo '/reel/[0-9]{6,}' "$normalized" 2>/dev/null | \
    sed -n 's#^/reel/\([0-9][0-9]*\)$#https://www.facebook.com/reel/\1#p' \
    >> "$FB_LINKS_FILE" || true

  # /watch/?...v=123... and /video.php?...v=123...
  grep -Eo '(/watch/\?[^" <]*v=[0-9]{6,}|/video\.php\?[^" <]*v=[0-9]{6,})' "$normalized" 2>/dev/null | \
    sed -n 's/.*[?&]v=\([0-9][0-9]*\).*/https:\/\/www.facebook.com\/watch\/?v=\1/p' \
    >> "$FB_LINKS_FILE" || true

  # Facebook JSON payloads often expose video_id/videoId even when a direct
  # permalink is absent in the server-rendered HTML.
  grep -Eo '"(video_id|videoId)"[[:space:]]*:[[:space:]]*"[0-9]{6,}"' "$normalized" 2>/dev/null | \
    sed -n 's/.*"\([0-9][0-9]*\)"$/https:\/\/www.facebook.com\/watch\/?v=\1/p' \
    >> "$FB_LINKS_FILE" || true

  # Common permalink path: /name/videos/.../123456
  grep -Eo '/[^" <]+/videos/([^/" <]+/)?[0-9]{6,}' "$normalized" 2>/dev/null | \
    sed -n 's#.*/\([0-9][0-9]*\)$#https://www.facebook.com/watch/?v=\1#p' \
    >> "$FB_LINKS_FILE" || true

  rm -f "$normalized" 2>/dev/null || true
  return 0
}

dedupe_fb_links() {
  [ -s "$FB_LINKS_FILE" ] || return 1

  tmp="$FB_LINKS_FILE.tmp"
  seen="$FB_SCAN_DIR/seen_ids.txt"
  : > "$tmp"
  : > "$seen"

  fb_total=$(wc -l < "$FB_LINKS_FILE" | tr -d ' ')
  fb_i=0
  while [ "$fb_i" -lt "$fb_total" ]; do
    fb_i=$((fb_i + 1))
    u=$(sed -n "${fb_i}p" "$FB_LINKS_FILE")
    [ -n "$u" ] || continue
    vid=''

    case "$u" in
      *facebook.com/reel/*)
        vid=$(printf '%s\n' "$u" | sed -n 's#.*facebook\.com/reel/\([0-9][0-9]*\).*#\1#p')
        ;;
      *\?v=[0-9]*|*\&v=[0-9]*)
        vid=$(printf '%s\n' "$u" | sed -n 's/.*[?&]v=\([0-9][0-9]*\).*/\1/p')
        ;;
    esac

    [ -n "$vid" ] || continue

    if ! grep -qx "$vid" "$seen" 2>/dev/null; then
      printf '%s\n' "$vid" >> "$seen"
      printf '%s\n' "$u" >> "$tmp"
    fi
  done

  mv "$tmp" "$FB_LINKS_FILE"
  [ -s "$FB_LINKS_FILE" ]
}


fetch_fb_page_dump() {
  index=$1
  total=$2
  url=$3
  page_dir="$FB_SCAN_DIR/fetch_$index"

  rm -rf "$page_dir" 2>/dev/null || true
  mkdir -p "$page_dir" || return 1

  say "[C][scan] $index/$total checking Facebook..."

  attempt=1
  while [ "$attempt" -le 2 ]; do
    log_file="$page_dir/fetch_$attempt.log"
    FB_LAST_LOG=$log_file

    old_pwd=$(pwd)
    cd "$page_dir" || {
      err 'STATUS=SCAN_DIR_ERROR'
      return 1
    }

    set -- --ignore-errors --skip-download --write-pages \
      --quiet --no-warnings --no-progress \
      --socket-timeout "$FB_SOCKET_TIMEOUT" \
      --retries 0 --extractor-retries 0 --fragment-retries 0 \
      --no-playlist \
      --add-header 'Accept-Language:en-US,en;q=0.8'

    [ -z "$COOKIES" ] || set -- "$@" --cookies "$COOKIES"

    if [ "$attempt" -eq 2 ] && [ -n "$FB_IMPERSONATE" ]; then
      set -- "$@" --impersonate "$FB_IMPERSONATE"
    fi

    set -- "$@" "$url"

    "$YTDLP" "$@" >"$log_file" 2>&1
    rc=$?

    cd "$old_pwd" 2>/dev/null || cd "$HOME_DIR/Documents" 2>/dev/null || true

    login_seen=0
    if grep -Eqi 'facebook\.com/login/|Unsupported URL: https://(www\.)?facebook\.com/login/|_fb_noscript|login_next' "$log_file" 2>/dev/null; then
      login_seen=1
    fi

    for page in "$page_dir"/*.dump; do
      [ -f "$page" ] || continue
      case "$(basename "$page")" in
        *facebook.com_login*|*login_next*|*login_*)
          login_seen=1
          ;;
      esac
    done

    if [ "$login_seen" -eq 1 ]; then
      FB_LOGIN_REQUIRED=1
      FB_STATUS='AUTH_REQUIRED'
      say '[C][auth] STATUS=AUTH_REQUIRED'
      say '[C][auth] Facebook redirected profile discovery to LOGIN.'
      if [ "$FB_DEBUG" -eq 1 ]; then
        say '[C][debug] Last Facebook fetch log:'
        tail -n 20 "$log_file" 2>/dev/null || true
      fi
      return 2
    fi

    dump_count=0
    before=$(count_lines_file "$FB_LINKS_FILE")

    for page in "$page_dir"/*.dump; do
      [ -f "$page" ] || continue
      dump_count=$((dump_count + 1))
      parse_facebook_dump_shell "$page" || true
    done

    dedupe_fb_links >/dev/null 2>&1 || true
    after=$(count_lines_file "$FB_LINKS_FILE")

    if [ "$dump_count" -gt 0 ]; then
      if [ "$after" -gt "$before" ] 2>/dev/null; then
        say "[C][scan] +$((after - before)) candidates (total $after)"
      else
        say '[C][scan] page received; +0 candidates'
      fi
      FB_STATUS='PAGE_RECEIVED'
      if [ "$FB_DEBUG" -eq 1 ]; then
        say '[C][debug] Last Facebook fetch log:'
        tail -n 20 "$log_file" 2>/dev/null || true
      fi
      return 0
    fi

    if [ "$attempt" -eq 1 ] && [ -n "$FB_IMPERSONATE" ]; then
      say "[C][scan] no page; retry once with $FB_IMPERSONATE..."
      attempt=2
      continue
    fi

    FB_STATUS='NO_PAGE'
    say '[C][scan] STATUS=NO_PAGE'
    if [ "$FB_DEBUG" -eq 1 ]; then
      say '[C][debug] Last Facebook fetch log:'
      tail -n 20 "$log_file" 2>/dev/null || true
    fi
    return 0
  done

  return 0
}

scan_facebook_profile() {
  : > "$FB_LINKS_FILE"
  FB_LOGIN_REQUIRED=0
  FB_STATUS=''
  detect_fb_impersonation >/dev/null 2>&1 || true

  if [ -n "$FB_IMPERSONATE" ]; then
    say "[C][scan] fallback browser available: $FB_IMPERSONATE"
  fi

  fetch_fb_page_dump 1 3 "$INPUT"
  rc=$?
  [ "$rc" -eq 2 ] && return 2

  before=$(count_lines_file "$FB_LINKS_FILE")
  fetch_fb_page_dump 2 3 "https://www.facebook.com/profile.php?id=$FB_PROFILE_ID&sk=reels_tab"
  rc=$?
  [ "$rc" -eq 2 ] && return 2
  after=$(count_lines_file "$FB_LINKS_FILE")
  say "[C][scan] reels surface added $((after - before)) candidates."

  discovered=$(count_lines_file "$FB_LINKS_FILE")
  if [ "$discovered" -eq 0 ] 2>/dev/null; then
    before=$discovered
    fetch_fb_page_dump 3 3 "https://m.facebook.com/profile.php?id=$FB_PROFILE_ID&sk=reels_tab"
    rc=$?
    [ "$rc" -eq 2 ] && return 2
    after=$(count_lines_file "$FB_LINKS_FILE")
    say "[C][scan] mobile fallback added $((after - before)) candidates."
  else
    say '[C][scan] candidates found; mobile fallback skipped.'
  fi

  dedupe_fb_links
}

run_fb_bulk_video() {
  video_url=$1
  selector=$2
  tpl="$FB_BATCH_DIR/%(title).100B [%(id)s].%(ext)s"

  bulk_connections=$CONNECTIONS
  [ "$bulk_connections" -le 4 ] || bulk_connections=4

  set -- --no-playlist --continue --newline --no-part \
    --concurrent-fragments "$bulk_connections" \
    --retries 10 --fragment-retries 10 --extractor-retries 3 \
    --socket-timeout 30 \
    --download-archive "$FB_ARCHIVE_FILE" \
    -f "$selector" -S "$FORMAT_SORT" -o "$tpl"

  [ -z "$COOKIES" ] || set -- "$@" --cookies "$COOKIES"

  if have ffmpeg; then
    set -- "$@" --merge-output-format mp4
  fi

  set -- "$@" "$video_url"
  run_ytdlp "$@"
}

facebook_profile_flow() {
  maybe_use_default_facebook_cookies

  extract_facebook_profile_id || {
    err 'Could not read the Facebook profile numeric ID.'
    return 1
  }

  fb_profile_paths || {
    err 'Could not create Facebook batch folders.'
    return 1
  }

  say ''
  say "[C] Facebook profile detected: $FB_PROFILE_ID"
  say '[C] Best-effort mode: Facebook does not expose a stable public bulk-video API to yt-dlp.'
  say ''
  say 'Profile quality:'
  say ' 1) BEST available'
  say ' 2) 1080p or lower'
  say ' 3) 720p or lower'
  say ' 0) Cancel'
  printf 'Number: '
  IFS= read -r q || q=''

  case "$q" in
    0) return 0 ;;
    1) set_quality_cap ''; selector=$(best_selector) ;;
    2) set_quality_cap 1080; selector=$(selector_for_height 1080) ;;
    3) set_quality_cap 720; selector=$(selector_for_height 720) ;;
    *) err 'Wrong number.'; return 1 ;;
  esac

  say ''
  say '[C] Profile discovery starting.'
  say "[C] Socket timeout: ${FB_SOCKET_TIMEOUT}s; extraction retries: 0."
  [ -z "$COOKIES" ] || say "[C][auth] Cookies file: $COOKIES"

  scan_facebook_profile
  scan_rc=$?

  if [ "$scan_rc" -eq 2 ] || [ "$FB_LOGIN_REQUIRED" -eq 1 ]; then
    say ''
    say '========================================'
    say '[C] STATUS=AUTH_REQUIRED'
    say '[C] Facebook profile bulk discovery needs a logged-in Facebook session.'
    if [ -z "$COOKIES" ]; then
      say ''
      say 'Next step: put a valid Netscape/Mozilla cookie file in Documents as:'
      say '  facebook_cookies.txt'
      say ''
      say 'Then run the same daily command again:'
      say '  c'
      say ''
      say 'For setup help:'
      say '  c --setup-facebook-cookies'
    else
      say ''
      say 'The supplied cookies were rejected or are stale.'
      say 'Export a fresh logged-in Facebook cookies file and retry.'
    fi
    say ''
    say 'Single Facebook reel/video URLs still work normally.'
    say '========================================'
    return 0
  fi

  if [ "$scan_rc" -ne 0 ]; then
    err 'No candidate Facebook video/reel links were exposed to Cinema.'
    say 'This does NOT mean the profile has no videos.'
    say ''
    if [ -z "$COOKIES" ]; then
      say 'Retry with a fresh Netscape-format cookies file:'
      say "  c --cookies cookies.txt \"$INPUT\""
    else
      say 'Cookies were supplied, but Facebook still did not expose a bulk list.'
    fi
    say ''
    say 'Single Facebook reel/video URLs remain supported.'
    return 1
  fi

  discovered=$(count_lines_file "$FB_LINKS_FILE")
  say ''
  say "[C] Candidate links discovered: $discovered"
  say '[C] This count is NOT a guarantee that every profile video was exposed.'
  say "[C] Batch folder: $FB_BATCH_DIR"
  printf 'Download these candidates now? [y/N]: '
  IFS= read -r yn || yn=''

  case "$yn" in
    y|Y|yes|YES) ;;
    *) say 'Cancelled.'; return 0 ;;
  esac

  if [ "$discovered" -gt 50 ] 2>/dev/null; then
    say "[C] Large batch: $discovered candidates."
    printf 'Confirm large download again? [y/N]: '
    IFS= read -r yn2 || yn2=''
    case "$yn2" in
      y|Y|yes|YES) ;;
      *) say 'Cancelled.'; return 0 ;;
    esac
  fi

  attempted=0
  downloaded=0
  skipped=0
  failed=0

  fb_total=$(wc -l < "$FB_LINKS_FILE" | tr -d ' ')
  fb_i=0
  while [ "$fb_i" -lt "$fb_total" ]; do
    fb_i=$((fb_i + 1))
    video_url=$(sed -n "${fb_i}p" "$FB_LINKS_FILE")
    [ -n "$video_url" ] || continue

    attempted=$((attempted + 1))
    before=$(count_lines_file "$FB_ARCHIVE_FILE")

    say ''
    say "[$attempted/$discovered] $video_url"

    if run_fb_bulk_video "$video_url" "$selector"; then
      after=$(count_lines_file "$FB_ARCHIVE_FILE")
      if [ "$after" -gt "$before" ] 2>/dev/null; then
        downloaded=$((downloaded + 1))
      else
        skipped=$((skipped + 1))
      fi
    else
      failed=$((failed + 1))
      warn "Failed: $video_url"
    fi
  done

  say ''
  say '========================================'
  say '[C] Facebook profile batch finished.'
  say "[C] Discovered: $discovered"
  say "[C] New downloads: $downloaded"
  say "[C] Already downloaded/skipped: $skipped"
  say "[C] Failed: $failed"
  say "[C] Folder: $FB_BATCH_DIR"
  say '========================================'

  [ "$downloaded" -gt 0 ] || [ "$skipped" -gt 0 ]
}

show_menu() {
  say ''
  say 'Choose quality:'
  say '----------------------------------------'
  say ' 1) BEST quality — automatic'
  say ' 2) 4K / 2160p or lower'
  say ' 3) 2K / 1440p or lower'
  say ' 4) Full HD / 1080p or lower'
  say ' 5) HD / 720p or lower'
  say ' 6) SD / 480p or lower'
  say ' 7) FAST MP4 — ready video+audio'
  say ' 8) AUDIO — M4A'
  say ' 9) AUDIO — MP3'
  say '10) EXACT site formats — show IDs'
  say '11) AUDIO LAB — voice / music separation'
  say ' 0) Cancel'
  say '----------------------------------------'
}

choose_destination() {
  media_kind=$1

  if [ "$media_kind" = 'audio' ]; then
    SAVE_MODE='files'
    return 0
  fi

  [ "$SAVE_MODE" = 'ask' ] || return 0

  say ''
  say 'Save after download:'
  say ' 1) Photos SAFE   — verify by rebuilding to iPhone-safe MP4'
  say ' 2) Files only    — Cinema_Downloads'
  printf 'Number: '
  IFS= read -r dst || dst=''

  case "$dst" in
    1) SAVE_MODE='photos' ;;
    2) SAVE_MODE='files' ;;
    *)
      err 'Wrong number.'
      exit 1
      ;;
  esac
}

# Codecs the iPhone Photos app accepts as-is. Sites spell them differently:
# YouTube "avc1.64001F", TikTok "h264" / "h265" / "bytevc1", others "hvc1"/"hev1".
IOS_VC="[vcodec~='^(avc|h264|hvc|hev|h265|bytevc1)']"
IOS_AC="[acodec~='^(mp4a|aac)']"

# Sort order inside every selector: highest resolution first, then H.264
# and AAC over VP9/AV1/Opus. A quality cap is "res:N", which yt-dlp measures
# on the SHORTER side - a portrait 1080x1920 TikTok counts as 1080p, whereas
# a [height<=1080] filter would wrongly drop it to 540p.
FORMAT_SORT='res,fps,vcodec:h264,acodec:aac'

set_quality_cap() {
  # $1 = max height (shorter side), empty = no cap
  if [ -n "${1:-}" ]; then
    FORMAT_SORT="res:$1,fps,vcodec:h264,acodec:aac"
  else
    FORMAT_SORT='res,fps,vcodec:h264,acodec:aac'
  fi
}

selector_for_height() {
  # Pair with: set_quality_cap "$h"
  h=$1
  if [ "$h" -gt 1080 ] && have ffmpeg; then
    # 2K/4K usually exist only as VP9/AV1: take the real resolution and let
    # Photos SAFE convert it, instead of silently falling back to H.264 1080p.
    printf '%s' "bv*+ba$IOS_AC/bv*+ba/b/best"
  else
    best_selector
  fi
}

best_selector() {
  # BEST = best quality the iPhone can save without re-encoding.
  if have ffmpeg; then
    printf '%s' "bv*$IOS_VC+ba$IOS_AC/bv*$IOS_VC+ba/b$IOS_VC/bv*+ba/b/best"
  else
    printf '%s' "b$IOS_VC/b[ext=mp4]/best"
  fi
}

new_work_dir() {
  mkdir -p "$STATE_DIR" "$DOWNLOAD_DIR" || {
    err 'Cannot create working folders.'
    exit 1
  }

  stamp=$(date '+%Y%m%d_%H%M%S' 2>/dev/null || printf 'job')
  WORK_DIR="$STATE_DIR/job_${stamp}_$$"
  mkdir -p "$WORK_DIR" || {
    err 'Cannot create unique download job folder.'
    exit 1
  }
}

OUTPUT_COUNT=0

collect_outputs() {
  # Historical method: inspect the unique job folder only after yt-dlp exits.
  # Ignore known temporary/metadata files. A post can hold several videos
  # (carousels): every completed file is moved, OUTPUT_FILE is the first.
  OUTPUTS=''
  OUTPUT_COUNT=0
  first=''

  for f in "$WORK_DIR"/*; do
    [ -f "$f" ] || continue
    case "$f" in
      *.part|*.ytdl|*.temp|*.tmp|*.json|*.description|*.jpg|*.jpeg|*.png|*.webp)
        continue
        ;;
    esac

    case "$f" in
      *.mp4|*.MP4|*.m4v|*.M4V|*.mov|*.MOV|*.mkv|*.MKV|*.webm|*.WEBM|*.m4a|*.M4A|*.mp3|*.MP3|*.aac|*.AAC|*.opus|*.OPUS)
        OUTPUT_FILE=$f
        move_to_downloads || return 1
        OUTPUTS="${OUTPUTS}$OUTPUT_FILE
"
        OUTPUT_COUNT=$((OUTPUT_COUNT + 1))
        [ -n "$first" ] || first=$OUTPUT_FILE
        ;;
    esac
  done

  if [ "$OUTPUT_COUNT" -eq 0 ]; then
    err 'yt-dlp finished but no completed media file was found.'
    return 1
  fi

  OUTPUT_FILE=$first
  return 0
}

move_to_downloads() {
  [ -n "$OUTPUT_FILE" ] && [ -f "$OUTPUT_FILE" ] || return 1

  base=${OUTPUT_FILE##*/}
  dest="$DOWNLOAD_DIR/$base"

  if [ -e "$dest" ]; then
    stamp=$(date '+%Y%m%d_%H%M%S' 2>/dev/null || printf '%s' "$$")
    dest="$DOWNLOAD_DIR/Cinema_${stamp}_$base"
  fi

  mv "$OUTPUT_FILE" "$dest" || {
    err 'Could not move the completed file into Cinema_Downloads.'
    return 1
  }

  OUTPUT_FILE=$dest
  return 0
}

ytdlp_attempt() {
  # $1 selector ; $2 action ; $3 impersonate target (optional)
  y_sel=$1
  y_act=$2
  y_imp=${3:-}

  if [ -n "${WORK_DIR:-}" ] && [ -d "$WORK_DIR" ]; then
    rm -rf "$WORK_DIR" 2>/dev/null || true
  fi
  new_work_dir
  tpl="$WORK_DIR/%(title).120B [%(id)s].%(ext)s"

  # Deliberately no --print-to-file and no last_output.txt.
  set -- --no-playlist --continue --newline --no-part \
    --concurrent-fragments "$CONNECTIONS" \
    --retries 10 --fragment-retries 10 --extractor-retries 3 \
    --socket-timeout 30 \
    -f "$y_sel" -S "$FORMAT_SORT" -o "$tpl"

  [ -z "$COOKIES" ] || set -- "$@" --cookies "$COOKIES"
  [ -z "$y_imp" ] || set -- "$@" --impersonate "$y_imp"

  case "$y_act" in
    merge)
      if have ffmpeg; then
        set -- "$@" --merge-output-format mp4
      fi
      ;;
    m4a)
      if have ffmpeg; then
        set -- "$@" -x --audio-format m4a
      fi
      ;;
    mp3)
      if ! have ffmpeg; then
        err 'MP3 needs ffmpeg. Choose M4A instead.'
        return 1
      fi
      set -- "$@" -x --audio-format mp3 --audio-quality 0
      ;;
    none)
      ;;
    *)
      err "Internal action error: $y_act"
      return 1
      ;;
  esac

  set -- "$@" "$INPUT"
  run_ytdlp "$@"
}

run_download() {
  selector=$1
  action=$2

  if ! ytdlp_attempt "$selector" "$action" ''; then
    recovered=0
    case "$action" in
      merge|none) fallback='bv*+ba/b/best' ;;
      *) fallback='ba/b/best' ;;
    esac

    if [ "$fallback" != "$selector" ]; then
      warn 'First attempt failed; retrying with any available format...'
      ytdlp_attempt "$fallback" "$action" '' && recovered=1
    fi

    if [ "$recovered" -eq 0 ] && detect_fb_impersonation >/dev/null 2>&1; then
      warn "Retrying once with browser impersonation ($FB_IMPERSONATE)..."
      ytdlp_attempt "$fallback" "$action" "$FB_IMPERSONATE" && recovered=1
    fi

    if [ "$recovered" -eq 0 ]; then
      err 'yt-dlp reported a download error.'
      say 'Most common fix: the site changed and yt-dlp needs an update.'
      printf 'Update yt-dlp now and retry once? [Y/n]: '
      IFS= read -r up || up=''
      case "$up" in
        n|N|no|NO) ;;
        *)
          if update_ytdlp; then
            say '[C] Retrying with the updated yt-dlp...'
            ytdlp_attempt "$fallback" "$action" '' && recovered=1
          fi
          ;;
      esac
    fi

    if [ "$recovered" -eq 0 ]; then
      err 'Download still failed.'
      say 'Private/age-restricted/login-only posts need your cookies:'
      say '  c --cookies cookies.txt "URL"'
      say 'Check the link opens in Safari without logging in.'
      return 1
    fi
  fi

  collect_outputs || return 1

  say ''
  if [ "$OUTPUT_COUNT" -gt 1 ]; then
    say "DONE: $OUTPUT_COUNT files"
    printf '%s' "$OUTPUTS" | sed '/^$/d; s/^/  /'
  else
    say "DONE: $OUTPUT_FILE"
  fi
  return 0
}

show_exact_formats() {
  say ''
  say '[C] Actual formats reported by the site:'
  say '----------------------------------------'

  set -- -F --no-playlist --socket-timeout 30 --retries 3
  [ -z "$COOKIES" ] || set -- "$@" --cookies "$COOKIES"
  set -- "$@" "$INPUT"

  run_ytdlp "$@" || return 1

  say '----------------------------------------'
  printf 'Type format ID (example 18 or 137+140): '
  IFS= read -r fid || fid=''
  [ -n "$fid" ] || {
    err 'Empty format ID'
    return 1
  }

  choose_destination video
  say "[C] Downloading format: $fid"
  run_download "$fid" merge
}


# ---------------- Photos SAFE (V33) ----------------
# a-Shell's ffmpeg has no libx264, and the iPhone hardware encoder can refuse
# a session (h264_videotoolbox -12903), e.g. when a-Shell is not on screen.
# So: never encode when a copy is enough, and only try encoders that exist.

has_encoder() {
  have ffmpeg || return 1
  if [ -z "$ENC_CACHE" ] || [ ! -s "$ENC_CACHE" ]; then
    mkdir -p "$STATE_DIR" 2>/dev/null || true
    ENC_CACHE="$STATE_DIR/ffmpeg_encoders.txt"
    ffmpeg -nostdin -hide_banner -encoders > "$ENC_CACHE" 2>/dev/null || return 1
  fi
  grep -Eq "^[[:space:]]*[A-Z.]{6}[[:space:]]+$1[[:space:]]" "$ENC_CACHE"
}

SRC_VCODEC=''
SRC_PIXFMT=''
SRC_W=0
SRC_H=0
SRC_ACODEC=''

probe_media() {
  # Reads codecs from `ffmpeg -i` (no ffprobe: it stalled on-device before).
  info="$STATE_DIR/.probe.txt"
  ffmpeg -nostdin -hide_banner -i "$1" > /dev/null 2> "$info" || true

  vline=$(grep 'Stream #.*Video:' "$info" 2>/dev/null | grep -v 'attached pic' | sed -n '1p')
  aline=$(grep 'Stream #.*Audio:' "$info" 2>/dev/null | sed -n '1p')

  SRC_VCODEC=$(printf '%s' "$vline" | sed -n 's/.*Video: \([A-Za-z0-9_]*\).*/\1/p')
  SRC_ACODEC=$(printf '%s' "$aline" | sed -n 's/.*Audio: \([A-Za-z0-9_]*\).*/\1/p')
  SRC_PIXFMT=$(printf '%s' "$vline" | grep -Eo '(yuvj?4[0-9]{2}p[0-9a-z]*|nv12|p010le|gbrp[0-9a-z]*|rgb[0-9a-z]*|bgr[0-9a-z]*)' | sed -n '1p')
  dims=$(printf '%s' "$vline" | grep -Eo ' [0-9]{2,5}x[0-9]{2,5}' | sed -n '1p' | tr -d ' ')
  SRC_W=${dims%x*}
  SRC_H=${dims#*x}
  case "$SRC_W" in ''|*[!0-9]*) SRC_W=0 ;; esac
  case "$SRC_H" in ''|*[!0-9]*) SRC_H=0 ;; esac
}

safe_ff() {
  # ffmpeg with errors captured to a FILE (no pipes: proven safer on a-Shell)
  ffmpeg -y -nostdin -hide_banner -loglevel error "$@" 2> "$SAFE_LOG"
}

safe_show_log() {
  [ -s "$SAFE_LOG" ] || return 0
  say '[C] ffmpeg said:'
  tail -n 3 "$SAFE_LOG" 2>/dev/null || true
}

safe_check() {
  # $1 = candidate file. Non-empty and one video frame decodes.
  [ -s "$1" ] || return 1
  ffmpeg -nostdin -hide_banner -loglevel error -i "$1" \
    -map 0:v:0 -frames:v 1 -f null /dev/null > /dev/null 2>&1
}

safe_audio_args() {
  # Sets AUDIO_ARGS for the current source.
  case "$SRC_ACODEC" in
    '') AUDIO_ARGS='-an' ;;
    aac) AUDIO_ARGS='-c:a copy' ;;
    *) AUDIO_ARGS='-c:a aac -b:a 192k' ;;
  esac
}

safe_bitrate() {
  long=$SRC_W
  [ "$SRC_H" -gt "$long" ] && long=$SRC_H
  if [ "$long" -ge 3000 ]; then printf '20000k'
  elif [ "$long" -ge 2000 ]; then printf '12000k'
  elif [ "$long" -ge 1200 ]; then printf '8000k'
  else printf '5000k'; fi
}

# Even width/height (H.264 needs it); optional long-edge cap.
EVEN_VF='scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p'
CAP1080_VF="scale='if(gt(iw,ih),min(1920,iw),-2)':'if(gt(iw,ih),-2,min(1920,ih))',scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p"

safe_try_encode() {
  # $1 label ; $2 vf ; rest = video codec args
  label=$1; vf=$2; shift 2
  say "[C] Trying $label..."
  rm -f "$tmp" 2>/dev/null || true
  # shellcheck disable=SC2086
  if safe_ff -i "$OUTPUT_FILE" -map 0:v:0 -map 0:a:0? -sn -dn \
      -vf "$vf" "$@" $AUDIO_ARGS -movflags +faststart "$tmp" \
     && safe_check "$tmp"; then
    SAFE_METHOD=$label
    return 0
  fi
  safe_show_log
  rm -f "$tmp" 2>/dev/null || true
  return 1
}

make_photos_safe_copy() {
  [ -n "$OUTPUT_FILE" ] && [ -f "$OUTPUT_FILE" ] || {
    err 'No downloaded video was found for Photos preparation.'
    return 1
  }

  have ffmpeg || {
    err 'Photos SAFE needs ffmpeg in a-Shell.'
    return 1
  }

  mkdir -p "$STATE_DIR" 2>/dev/null || true
  SAFE_LOG="$STATE_DIR/last_safe_ffmpeg.txt"
  SAFE_METHOD=''

  base=${OUTPUT_FILE##*/}
  stem=${base%.*}
  PHOTOS_SAFE_FILE="$DOWNLOAD_DIR/PhotosSafe_${stem}.mp4"

  if [ -e "$PHOTOS_SAFE_FILE" ]; then
    stamp=$(date '+%Y%m%d_%H%M%S' 2>/dev/null || printf '%s' "$$")
    PHOTOS_SAFE_FILE="$DOWNLOAD_DIR/PhotosSafe_${stamp}_${stem}.mp4"
  fi

  tmp="$PHOTOS_SAFE_FILE.tmp.mp4"
  rm -f "$tmp" 2>/dev/null || true

  say ''
  say '[C] Checking export compatibility before Photos...'
  probe_media "$OUTPUT_FILE"
  [ -n "$SRC_VCODEC" ] || {
    err 'This file has no video track (audio only?). Use Files instead.'
    return 1
  }
  say "[C] Source: video ${SRC_VCODEC} ${SRC_PIXFMT:-?} ${SRC_W}x${SRC_H}, audio ${SRC_ACODEC:-none}"
  say '[C] Original downloaded file will be kept.'
  safe_audio_args

  # 1) Already an iPhone codec -> lossless remux, no encoder involved.
  vtag=''
  case "$SRC_VCODEC:$SRC_PIXFMT" in
    h264:yuv420p|h264:yuvj420p) vtag='avc1' ;;
    hevc:yuv420p|hevc:yuvj420p|hevc:yuv420p10le) vtag='hvc1' ;;
  esac
  if [ -n "$vtag" ]; then
    say '[C] Already iPhone-compatible: copying streams (no quality loss)...'
    # shellcheck disable=SC2086
    if safe_ff -i "$OUTPUT_FILE" -map 0:v:0 -map 0:a:0? -sn -dn \
        -c:v copy -tag:v "$vtag" $AUDIO_ARGS -movflags +faststart "$tmp" \
       && safe_check "$tmp"; then
      SAFE_METHOD="lossless copy ($SRC_VCODEC)"
    else
      safe_show_log
      rm -f "$tmp" 2>/dev/null || true
      say '[C] Copy was not accepted; converting instead.'
      # A re-encode cannot copy the audio of a broken container either.
      [ "$SRC_ACODEC" = '' ] || AUDIO_ARGS='-c:a aac -b:a 192k'
    fi
  fi

  # 2) Convert. Every encoder is checked before use.
  if [ -z "$SAFE_METHOD" ]; then
    br=$(safe_bitrate)
    say '[C] Converting to H.264. Keep a-Shell OPEN on screen until it finishes:'
    say '[C] iOS blocks the hardware encoder in the background (error -12903).'

    if has_encoder h264_videotoolbox; then
      safe_try_encode 'hardware H.264' "$EVEN_VF" \
        -c:v h264_videotoolbox -b:v "$br" -allow_sw 1 -profile:v high \
        || safe_try_encode 'hardware H.264 (<=1080p)' "$CAP1080_VF" \
          -c:v h264_videotoolbox -b:v 8000k -allow_sw 1 \
        || true
    fi
    if [ -z "$SAFE_METHOD" ] && has_encoder hevc_videotoolbox; then
      safe_try_encode 'hardware HEVC' "$EVEN_VF" \
        -c:v hevc_videotoolbox -b:v "$br" -allow_sw 1 -tag:v hvc1 || true
    fi
    if [ -z "$SAFE_METHOD" ] && has_encoder libx264; then
      safe_try_encode 'software H.264 (libx264)' "$EVEN_VF" \
        -c:v libx264 -preset veryfast -crf 18 || true
    fi
    if [ -z "$SAFE_METHOD" ] && has_encoder mpeg4; then
      # Built into every ffmpeg. Photos plays MPEG-4 Part 2; quality is
      # lower than H.264, so it is the last resort.
      safe_try_encode 'built-in MPEG-4 (last resort)' "$CAP1080_VF" \
        -c:v mpeg4 -q:v 2 -tag:v mp4v || true
    fi
  fi

  [ -n "$SAFE_METHOD" ] || {
    rm -f "$tmp" 2>/dev/null || true
    err 'Could not build a Photos-safe MP4 with any encoder on this iPhone.'
    say 'Run: c --doctor   (shows which encoders work here)'
    say 'Then retry this file without downloading again:'
    say "  c --safe \"$OUTPUT_FILE\""
    return 1
  }

  mv "$tmp" "$PHOTOS_SAFE_FILE" || {
    rm -f "$tmp" 2>/dev/null || true
    err 'Could not finalize the Photos-safe MP4.'
    return 1
  }

  say "[C] Method: $SAFE_METHOD"
  say "[C] Photos-safe MP4 ready: $PHOTOS_SAFE_FILE"
  return 0
}

open_exact_video_for_photos() {
  [ -n "$PHOTOS_SAFE_FILE" ] && [ -f "$PHOTOS_SAFE_FILE" ] || return 1

  say ''
  say '[C] Opening the Photos-safe MP4...'
  say '[C] In the iOS panel choose: Save Video.'

  if have open; then
    open "$PHOTOS_SAFE_FILE" >/dev/null 2>&1 && return 0
  fi

  if have view; then
    view "$PHOTOS_SAFE_FILE" >/dev/null 2>&1 && return 0
  fi

  err 'Could not open the Photos-safe video automatically.'
  return 1
}

is_video_file() {
  case "$1" in
    *.m4a|*.M4A|*.mp3|*.MP3|*.aac|*.AAC|*.opus|*.OPUS|*.wav|*.WAV) return 1 ;;
  esac
  return 0
}

finish_one_photos() {
  if make_photos_safe_copy; then
    open_exact_video_for_photos || {
      say 'Open this Photos-safe file manually from Files, then Share -> Save Video:'
      say "$PHOTOS_SAFE_FILE"
    }
    return 0
  fi
  err 'Photos SAFE preparation failed.'
  say 'Original download was preserved here:'
  say "$OUTPUT_FILE"
  return 1
}

finish() {
  case "$SAVE_MODE" in
    photos)
      [ -n "$OUTPUTS" ] || OUTPUTS="$OUTPUT_FILE
"
      n_out=$(printf '%s' "$OUTPUTS" | sed '/^$/d' | wc -l | tr -d ' ')
      i_out=0
      rc_out=0
      while [ "$i_out" -lt "$n_out" ]; do
        i_out=$((i_out + 1))
        OUTPUT_FILE=$(printf '%s' "$OUTPUTS" | sed '/^$/d' | sed -n "${i_out}p")
        is_video_file "$OUTPUT_FILE" || continue
        [ "$n_out" -le 1 ] || say "[C] File $i_out/$n_out: ${OUTPUT_FILE##*/}"
        finish_one_photos || rc_out=1
        if [ "$i_out" -lt "$n_out" ]; then
          printf 'Press Enter for the next file... '
          IFS= read -r _ || true
        fi
      done
      return "$rc_out"
      ;;
    files)
      if [ "$OUTPUT_COUNT" -gt 1 ] 2>/dev/null; then
        say "Saved in Files: $DOWNLOAD_DIR"
      else
        say "Saved in Files: $OUTPUT_FILE"
      fi
      ;;
  esac
}

# =====================================================================
# V32 AUDIO LAB — separate VOICE and MUSIC from any video/audio
#   Offline engines (run on the iPhone, no internet after model fetch):
#     VOICE : center(mid) extraction + speech band + RNNoise (arnndn)
#             neural speech model + FFT denoise + loudness normalize
#     MUSIC : phase-cancel karaoke (removes centered vocals) while
#             restoring the bass/kick from the mid channel
#   Cloud engine (studio quality, optional):
#     AI STEMS : Demucs (htdemucs) on Replicate — needs your API token
# All work happens in a unique job folder; the source file is never touched.
# =====================================================================

LAB_DIR_NAME='Audio_Lab'
LAB_FMT='m4a'          # m4a | mp3 | wav
LAB_STRENGTH=1         # 1 normal, 2 strong (double neural pass)
LAB_SRC=''             # local media file being processed
LAB_JOB=''
LAB_WAV=''
LAB_STEREO=0           # 1 = real stereo (side channel has content)
LAB_STEM=''
LAB_OUTS=''            # newline list of produced files
FILTER_CACHE=''
RNN_MODEL=${CINEMA_RNN_MODEL:-lq}   # lq = voice vs general noise (best for music beds)
REPLICATE_MODEL='ryan5453/demucs'
REPLICATE_FALLBACK_VERSION='5a7041cc9b82e5a558fea6b3d7b12dea89625e89da33f0447bd727c2d0ab9e77'
REPLICATE_TOKEN_FILE="$HOME_DIR/Documents/replicate_token.txt"

lab_ff() {
  # ffmpeg with errors captured to a FILE (no pipes: proven safer on a-Shell)
  ffmpeg -y -nostdin -hide_banner -loglevel error "$@" 2> "$STATE_DIR/last_lab_ffmpeg.txt"
  rc=$?
  if [ "$rc" -ne 0 ] && [ -s "$STATE_DIR/last_lab_ffmpeg.txt" ]; then
    say '[LAB] ffmpeg said:'
    tail -n 8 "$STATE_DIR/last_lab_ffmpeg.txt" 2>/dev/null || true
  fi
  return "$rc"
}

has_filter() {
  have ffmpeg || return 1
  if [ -z "$FILTER_CACHE" ] || [ ! -s "$FILTER_CACHE" ]; then
    mkdir -p "$STATE_DIR" 2>/dev/null || true
    FILTER_CACHE="$STATE_DIR/ffmpeg_filters.txt"
    ffmpeg -hide_banner -filters > "$FILTER_CACHE" 2>/dev/null || return 1
  fi
  grep -Eq "[[:space:]]$1[[:space:]]" "$FILTER_CACHE"
}

rnn_model_path() {
  printf '%s' "$STATE_DIR/models/$RNN_MODEL.rnnn"
}

ensure_rnn_model() {
  m=$(rnn_model_path)
  [ -s "$m" ] && return 0
  have curl || return 1
  mkdir -p "$STATE_DIR/models" || return 1
  say "[LAB] Downloading neural voice model ($RNN_MODEL.rnnn, one time only)..."
  for u in \
    "https://raw.githubusercontent.com/richardpl/arnndn-models/master/$RNN_MODEL.rnnn" \
    "https://github.com/richardpl/arnndn-models/raw/master/$RNN_MODEL.rnnn"
  do
    if curl -L --fail --silent --show-error --connect-timeout 15 --max-time 120 \
        -o "$m.tmp" "$u" 2>/dev/null && [ -s "$m.tmp" ]; then
      mv "$m.tmp" "$m" && return 0
    fi
    rm -f "$m.tmp" 2>/dev/null || true
  done
  return 1
}

lab_new_job() {
  mkdir -p "$STATE_DIR" || return 1
  stamp=$(date '+%Y%m%d_%H%M%S' 2>/dev/null || printf 'lab')
  LAB_JOB="$STATE_DIR/lab_${stamp}_$$"
  mkdir -p "$LAB_JOB" || return 1
  LAB_OUTS=''
}

lab_cleanup() {
  [ -n "$LAB_JOB" ] && [ -d "$LAB_JOB" ] && rm -rf "$LAB_JOB" 2>/dev/null
  LAB_JOB=''
  return 0
}

lab_out_dir() {
  d="$DOWNLOAD_DIR/$LAB_DIR_NAME"
  mkdir -p "$d" || return 1
  printf '%s' "$d"
}

lab_unique() {
  # $1 = desired path ; prints a non-existing path
  p=$1
  if [ ! -e "$p" ]; then printf '%s' "$p"; return; fi
  stem=${p%.*}; ext=${p##*.}
  stamp=$(date '+%H%M%S' 2>/dev/null || printf '%s' "$$")
  printf '%s' "${stem}_${stamp}.${ext}"
}

lab_add_out() {
  LAB_OUTS="${LAB_OUTS}$1
"
}

# Decode the first audio stream to a clean 48 kHz PCM WAV and classify it.
lab_prepare() {
  src=$1
  [ -f "$src" ] || { err "File not found: $src"; return 1; }
  have ffmpeg || { err 'Audio Lab needs ffmpeg in a-Shell.'; return 1; }

  base=${src##*/}
  LAB_STEM=${base%.*}
  LAB_STEM=$(printf '%s' "$LAB_STEM" | sed 's/^PhotosSafe_//; s/^Cinema_[0-9]*_[0-9]*_//; s/[\/:*?"<>|]/_/g')
  LAB_WAV="$LAB_JOB/source.wav"

  say '[LAB] Decoding audio...'
  lab_ff -i "$src" -vn -sn -dn -map 0:a:0 -ar 48000 -c:a pcm_s16le "$LAB_WAV" || {
    err 'This file has no readable audio track.'
    return 1
  }

  info="$LAB_JOB/info.txt"
  ffmpeg -nostdin -hide_banner -i "$LAB_WAV" > /dev/null 2> "$info" || true
  LAB_STEREO=0
  if grep -Eq 'Audio:.*(mono|1 channels)' "$info" 2>/dev/null; then
    say '[LAB] Source is MONO.'
    return 0
  fi

  # Real stereo or "fake stereo" (identical L/R)? Measure the side channel.
  side="$LAB_JOB/side.txt"
  ffmpeg -nostdin -hide_banner -i "$LAB_WAV" -af 'pan=mono|c0=c0-c1,volumedetect' \
    -f null "$LAB_JOB/.null" > /dev/null 2> "$side" || true
  mv_db=$(sed -n 's/.*max_volume: *\(-*[0-9.inf]*\) dB.*/\1/p' "$side" | sed -n '1p')
  mv_int=${mv_db%%.*}
  case "$mv_int" in
    ''|*inf*) LAB_STEREO=0 ;;
    *) if [ "$mv_int" -gt -45 ] 2>/dev/null; then LAB_STEREO=1; fi ;;
  esac
  if [ "$LAB_STEREO" -eq 1 ]; then
    say "[LAB] Real stereo detected (side peak ${mv_db} dB)."
  else
    say '[LAB] Stereo channels are identical (mono content).'
  fi
  return 0
}

lab_encode() {
  # $1 = wav in ; $2 = output path WITHOUT extension ; prints final path via LAB_LAST
  in=$1; outbase=$2
  case "$LAB_FMT" in
    mp3) out=$(lab_unique "$outbase.mp3"); set -- -c:a libmp3lame -q:a 0 ;;
    wav) out=$(lab_unique "$outbase.wav"); set -- -c:a pcm_s16le ;;
    *)   out=$(lab_unique "$outbase.m4a"); set -- -c:a aac -b:a 256k -movflags +faststart ;;
  esac
  lab_ff -i "$in" -ac 2 "$@" "$out" || return 1
  LAB_LAST=$out
  lab_add_out "$out"
  return 0
}

lab_voice_wav() {
  # Produces $LAB_JOB/voice.wav
  chain=''
  [ "$LAB_STEREO" -eq 1 ] && chain='pan=mono|c0=0.5*c0+0.5*c1,'
  chain="${chain}highpass=f=80,lowpass=f=8000"

  neural=0
  if has_filter arnndn && ensure_rnn_model; then
    m=$(rnn_model_path)
    chain="$chain,arnndn=m='$m'"
    [ "$LAB_STRENGTH" -ge 2 ] && chain="$chain,arnndn=m='$m'"
    neural=1
  fi
  if has_filter afftdn; then
    if [ "$neural" -eq 1 ]; then chain="$chain,afftdn=nf=-30"
    else chain="$chain,afftdn=nr=24:nf=-28"; fi
  fi
  chain="$chain,dynaudnorm=f=200:g=11,alimiter=limit=0.95"

  if [ "$neural" -eq 1 ]; then
    say "[LAB] VOICE: neural speech isolation (RNNoise/$RNN_MODEL, strength $LAB_STRENGTH)..."
  else
    warn 'Neural model unavailable; using basic FFT voice filter (lower quality).'
  fi
  lab_ff -i "$LAB_WAV" -af "$chain" -ar 48000 -c:a pcm_s16le "$LAB_JOB/voice.wav"
}

lab_music_wav() {
  # Produces $LAB_JOB/music.wav (vocals removed). Needs real stereo.
  if [ "$LAB_STEREO" -ne 1 ]; then
    err 'MUSIC-only offline mode needs a real stereo mix.'
    say 'This source is mono, so vocals and music cannot be split by phase.'
    say 'Use option 6 (AI STEMS) for this file.'
    return 2
  fi
  say '[LAB] MUSIC: removing centered vocals, restoring bass...'
  fc='[0:a]asplit=2[a][b];'
  fc="$fc[a]pan=stereo|c0=c0-c1|c1=c1-c0,highpass=f=140[s];"
  fc="$fc[b]pan=mono|c0=0.5*c0+0.5*c1,lowpass=f=140,pan=stereo|c0=c0|c1=c0[l];"
  fc="$fc[s][l]amerge=inputs=2,pan=stereo|c0=c0+c2|c1=c1+c3,alimiter=limit=0.95[out]"
  lab_ff -i "$LAB_WAV" -filter_complex "$fc" -map '[out]' -ar 48000 -c:a pcm_s16le "$LAB_JOB/music.wav"
}

lab_mux_video() {
  # $1 = video source ; $2 = processed wav ; $3 = label
  vsrc=$1; wav=$2; label=$3
  od=$(lab_out_dir) || return 1
  out=$(lab_unique "$od/$LAB_STEM - $label.mp4")
  say "[LAB] Building video: $label ..."
  lab_ff -i "$vsrc" -i "$wav" -map 0:v:0 -map 1:a:0 -c:v copy \
    -c:a aac -b:a 192k -ac 2 -shortest -movflags +faststart "$out" || {
      rm -f "$out" 2>/dev/null || true
      say '[LAB] Video copy failed; re-encoding video...'
      # a-Shell's ffmpeg has no libx264: use only encoders that exist.
      ok=0
      for enc in h264_videotoolbox libx264 mpeg4; do
        has_encoder "$enc" || continue
        case "$enc" in
          h264_videotoolbox) set -- -c:v h264_videotoolbox -b:v 8000k -allow_sw 1 ;;
          libx264) set -- -c:v libx264 -preset veryfast -crf 18 ;;
          mpeg4) set -- -c:v mpeg4 -q:v 2 -tag:v mp4v ;;
        esac
        if lab_ff -i "$vsrc" -i "$wav" -map 0:v:0 -map 1:a:0 \
            -vf "$EVEN_VF" "$@" \
            -c:a aac -b:a 192k -ac 2 -shortest -movflags +faststart "$out"; then
          ok=1
          break
        fi
        rm -f "$out" 2>/dev/null || true
      done
      [ "$ok" -eq 1 ] || return 1
    }
  LAB_LAST=$out
  lab_add_out "$out"
}

has_video_stream() {
  ffmpeg -nostdin -hide_banner -i "$1" > /dev/null 2> "$STATE_DIR/.vinfo.txt" || true
  grep -q 'Video:' "$STATE_DIR/.vinfo.txt" 2>/dev/null && ! grep -q 'Video:.*attached pic' "$STATE_DIR/.vinfo.txt" 2>/dev/null
}

# ---------------- AI STEMS (Replicate / Demucs) ----------------

json_str() {
  # $1 key ; $2 file -> first "key":"value"
  tr -d '\n' < "$2" | grep -o "\"$1\" *: *\"[^\"]*\"" | sed -n '1s/.*: *"\(.*\)"$/\1/p'
}

replicate_token() {
  if [ -n "${REPLICATE_API_TOKEN:-}" ]; then printf '%s' "$REPLICATE_API_TOKEN"; return 0; fi
  [ -s "$REPLICATE_TOKEN_FILE" ] || return 1
  t=''
  IFS= read -r t < "$REPLICATE_TOKEN_FILE" || true
  t=$(printf '%s' "$t" | tr -d '\r\n ')
  [ -n "$t" ] || return 1
  printf '%s' "$t"
}

setup_ai() {
  say 'AI STEMS setup (Demucs on Replicate)'
  say '------------------------------------'
  say 'Gives studio-grade separation: pure vocals + pure music (no vocals).'
  say 'Works for songs, nasheeds, mono files — things offline mode cannot split.'
  say 'Cost: pay-per-use on replicate.com (usually cents per song).'
  say ''
  say '1) Create an account at https://replicate.com'
  say '2) Account -> API tokens -> copy your token (starts with r8_)'
  say ''
  printf 'Paste token now (or Enter to skip): '
  IFS= read -r tok || tok=''
  tok=$(printf '%s' "$tok" | tr -d '\r\n ')
  if [ -n "$tok" ]; then
    printf '%s\n' "$tok" > "$REPLICATE_TOKEN_FILE" && chmod 600 "$REPLICATE_TOKEN_FILE" 2>/dev/null
    say "Saved: $REPLICATE_TOKEN_FILE"
    say 'SECURITY: this token can spend your Replicate credit. Do not share it.'
  else
    say "Later: put the token alone in $REPLICATE_TOKEN_FILE"
  fi
}

lab_ai_stems() {
  have curl || { err 'AI STEMS needs curl.'; return 1; }
  tok=$(replicate_token) || {
    err 'No Replicate token yet.'
    say 'Run once: c --setup-ai'
    return 1
  }
  auth="Authorization: Bearer $tok"
  api='https://api.replicate.com/v1'

  say '[AI] Compressing audio for upload...'
  up="$LAB_JOB/upload.mp3"
  lab_ff -i "$LAB_WAV" -ac 2 -c:a libmp3lame -b:a 256k "$up" || return 1

  say '[AI] Uploading...'
  r="$LAB_JOB/file.json"
  curl -sS --fail --connect-timeout 20 --max-time 600 -X POST -H "$auth" \
    -F "content=@$up;type=audio/mpeg" "$api/files" -o "$r" || {
      err 'Upload failed (check token / internet).'
      return 1
    }
  furl=$(tr -d '\n' < "$r" | grep -o '"get" *: *"[^"]*"' | sed -n '1s/.*: *"\(.*\)"$/\1/p')
  [ -n "$furl" ] || { err 'Upload response had no file URL.'; cat "$r"; return 1; }

  ver=$REPLICATE_FALLBACK_VERSION
  m="$LAB_JOB/model.json"
  if curl -sS --fail --connect-timeout 15 --max-time 30 -H "$auth" "$api/models/$REPLICATE_MODEL" -o "$m" 2>/dev/null; then
    v=$(tr -d '\n' < "$m" | grep -o '"latest_version" *: *{ *"id" *: *"[0-9a-f]*"' | sed -n '1s/.*"\([0-9a-f]*\)"$/\1/p')
    [ -n "$v" ] && ver=$v
  fi

  say '[AI] Separating with Demucs (htdemucs)... this can take 1-3 minutes.'
  body="{\"version\":\"$ver\",\"input\":{\"audio\":\"$furl\",\"stem\":\"vocals\",\"output_format\":\"mp3\",\"mp3_bitrate\":320}}"
  p="$LAB_JOB/pred.json"
  curl -sS --fail --connect-timeout 20 --max-time 90 -X POST -H "$auth" \
    -H 'Content-Type: application/json' -H 'Prefer: wait=60' \
    -d "$body" "$api/predictions" -o "$p" || { err 'Could not start AI job.'; cat "$p" 2>/dev/null; return 1; }

  pid=$(json_str id "$p")
  status=$(json_str status "$p")
  tries=0
  while [ "$status" != 'succeeded' ]; do
    case "$status" in
      failed|canceled)
        err "AI job $status."
        json_str error "$p"
        return 1
        ;;
    esac
    tries=$((tries + 1))
    [ "$tries" -le 120 ] || { err 'AI job timed out (10 min).'; return 1; }
    say "[AI] status: ${status:-starting} ..."
    sleep 5
    curl -sS --fail --connect-timeout 15 --max-time 30 -H "$auth" "$api/predictions/$pid" -o "$p" || true
    status=$(json_str status "$p")
  done

  od=$(lab_out_dir) || return 1
  # Output is an object: {"vocals": "https://...", "no_vocals": "https://...", ...}
  pairs="$LAB_JOB/pairs.txt"
  tr -d '\n' < "$p" | sed 's/.*"output" *: *{\([^}]*\)}.*/\1/' | \
    grep -o '"[a-z_]*" *: *"https://[^"]*"' > "$pairs" 2>/dev/null || true
  [ -s "$pairs" ] || { err 'AI finished but returned no stems.'; return 1; }

  got=0
  npairs=$(wc -l < "$pairs" | tr -d ' ')
  i=0
  while [ "$i" -lt "$npairs" ]; do
    i=$((i + 1))
    line=$(sed -n "${i}p" "$pairs")
    key=$(printf '%s' "$line" | sed -n 's/^"\([a-z_]*\)".*/\1/p')
    url=$(printf '%s' "$line" | sed -n 's/.*"\(https:[^"]*\)"$/\1/p')
    [ -n "$key" ] && [ -n "$url" ] || continue
    case "$key" in
      vocals) label='AI_VOICE' ;;
      no_vocals) label='AI_MUSIC' ;;
      *) label="AI_$(printf '%s' "$key" | tr 'a-z' 'A-Z')" ;;
    esac
    tmp="$LAB_JOB/$key.mp3"
    say "[AI] Downloading $label ..."
    curl -sS -L --fail --connect-timeout 20 --max-time 600 -o "$tmp" "$url" || continue
    lab_encode "$tmp" "$od/$LAB_STEM - $label" && got=$((got + 1))
    [ "$key" = 'vocals' ] && cp "$tmp" "$LAB_JOB/voice_ai.mp3" 2>/dev/null
    [ "$key" = 'no_vocals' ] && cp "$tmp" "$LAB_JOB/music_ai.mp3" 2>/dev/null
  done
  [ "$got" -gt 0 ]
}

# ---------------- menus / flows ----------------

lab_menu() {
  say ''
  say 'AUDIO LAB — what do you want?'
  say '----------------------------------------'
  say ' 1) VOICE only   — clean speech, music removed'
  say ' 2) MUSIC only   — vocals removed (karaoke)'
  say ' 3) BOTH         — voice file + music file'
  say ' 4) VIDEO + voice only  (music muted in video)'
  say ' 5) VIDEO + music only  (voice muted in video)'
  say ' 6) AI STEMS     — studio quality (Demucs, online)'
  say ' 7) Original audio only (no processing)'
  say ' 0) Cancel'
  say '----------------------------------------'
  say 'Offline 1-5 are best for speech over background music.'
  say 'For songs/singing or mono files, choose 6.'
  printf 'Number: '
  IFS= read -r LAB_MODE || LAB_MODE=''
  case "$LAB_MODE" in
    0) return 1 ;;
    1|2|3|4|5|6|7) ;;
    *) err 'Wrong number.'; return 1 ;;
  esac

  case "$LAB_MODE" in
    1|3|4)
      say ''
      say 'Voice strength:'
      say ' 1) Normal (natural voice)'
      say ' 2) Strong (more music removed, voice may sound thinner)'
      printf 'Number [1]: '
      IFS= read -r s || s=''
      [ "$s" = '2' ] && LAB_STRENGTH=2
      ;;
  esac

  case "$LAB_MODE" in
    4|5) ;;
    *)
      say ''
      say 'Audio format:'
      say ' 1) M4A (iPhone, default)   2) MP3   3) WAV (lossless)'
      printf 'Number [1]: '
      IFS= read -r f || f=''
      case "$f" in 2) LAB_FMT='mp3' ;; 3) LAB_FMT='wav' ;; *) LAB_FMT='m4a' ;; esac
      ;;
  esac
  return 0
}

lab_needs_video() {
  case "$LAB_MODE" in 4|5) return 0 ;; esac
  return 1
}

lab_process() {
  # $1 = local media file
  LAB_SRC=$1
  lab_new_job || { err 'Cannot create lab job folder.'; return 1; }
  lab_prepare "$LAB_SRC" || { lab_cleanup; return 1; }
  od=$(lab_out_dir) || { lab_cleanup; return 1; }
  rc=0

  case "$LAB_MODE" in
    1)
      lab_voice_wav && lab_encode "$LAB_JOB/voice.wav" "$od/$LAB_STEM - VOICE" || rc=1
      ;;
    2)
      lab_music_wav && lab_encode "$LAB_JOB/music.wav" "$od/$LAB_STEM - MUSIC" || rc=1
      ;;
    3)
      lab_voice_wav && lab_encode "$LAB_JOB/voice.wav" "$od/$LAB_STEM - VOICE" || rc=1
      if lab_music_wav; then
        lab_encode "$LAB_JOB/music.wav" "$od/$LAB_STEM - MUSIC" || rc=1
      fi
      ;;
    4|5)
      if ! has_video_stream "$LAB_SRC"; then
        err 'This file has no video track. Choose 1-3 instead.'
        rc=1
      elif [ "$LAB_MODE" -eq 4 ]; then
        lab_voice_wav && lab_mux_video "$LAB_SRC" "$LAB_JOB/voice.wav" 'VIDEO_VOICE' || rc=1
      else
        lab_music_wav && lab_mux_video "$LAB_SRC" "$LAB_JOB/music.wav" 'VIDEO_MUSIC' || rc=1
      fi
      ;;
    6)
      lab_ai_stems || rc=1
      ;;
    7)
      lab_encode "$LAB_WAV" "$od/$LAB_STEM - ORIGINAL" || rc=1
      ;;
  esac

  lab_cleanup
  say ''
  if [ -n "$LAB_OUTS" ]; then
    say '========================================'
    say '[LAB] Ready:'
    printf '%s' "$LAB_OUTS" | sed '/^$/d; s/^/  /'
    say "[LAB] Folder: $od"
    say '========================================'
  fi
  [ "$rc" -eq 0 ] || return 1

  # A processed VIDEO can go through the proven Photos SAFE flow.
  if lab_needs_video && [ -n "${LAB_LAST:-}" ] && [ -f "$LAB_LAST" ]; then
    OUTPUT_FILE=$LAB_LAST
    OUTPUTS=''
    OUTPUT_COUNT=1
    choose_destination video
    finish
    return $?
  fi
  if have open && [ -n "${LAB_LAST:-}" ] && [ -f "$LAB_LAST" ]; then
    open "$LAB_LAST" >/dev/null 2>&1 || true
  fi
  return 0
}

lab_pick_local() {
  # Interactive picker over media in Cinema_Downloads.
  # a-Shell note: never use `while read ... < file` here — in a-Shell that
  # read can fall back to the KEYBOARD. Plain for-loops + sed only.
  list="$STATE_DIR/lab_pick.txt"
  mkdir -p "$STATE_DIR" "$DOWNLOAD_DIR" 2>/dev/null || true
  : > "$list"
  say ''
  say 'Pick a file from Cinema_Downloads:'
  say '----------------------------------------'
  n=0
  for f in "$DOWNLOAD_DIR"/* "$DOWNLOAD_DIR/$LAB_DIR_NAME"/*; do
    [ -f "$f" ] || continue
    case "$f" in
      *.mp4|*.MP4|*.m4v|*.mov|*.MOV|*.mkv|*.webm|*.m4a|*.M4A|*.mp3|*.MP3|*.wav|*.WAV|*.aac|*.opus|*.ogg|*.flac) ;;
      *) continue ;;
    esac
    n=$((n + 1))
    printf '%s\n' "$f" >> "$list"
    say "$(printf '%2d' "$n")) ${f##*/}"
  done
  [ "$n" -gt 0 ] || { err "No media files found in $DOWNLOAD_DIR"; return 1; }
  say ' 0) Cancel'
  say '----------------------------------------'
  printf 'Number: '
  IFS= read -r k || k=''
  case "$k" in ''|0|*[!0-9]*) return 1 ;; esac
  [ "$k" -le "$n" ] || { err 'Wrong number.'; return 1; }
  LAB_SRC=$(sed -n "${k}p" "$list")
  [ -n "$LAB_SRC" ] && [ -f "$LAB_SRC" ]
}

lab_local_flow() {
  # c --lab [FILE]
  have ffmpeg || { err 'Audio Lab needs ffmpeg in a-Shell.'; return 1; }
  if [ -n "$LAB_FILE" ]; then
    LAB_SRC=$LAB_FILE
    [ -f "$LAB_SRC" ] || [ ! -f "$DOWNLOAD_DIR/$LAB_SRC" ] || LAB_SRC="$DOWNLOAD_DIR/$LAB_SRC"
  else
    lab_pick_local || return 1
  fi
  [ -f "$LAB_SRC" ] || { err "File not found: $LAB_SRC"; return 1; }
  say "[LAB] File: ${LAB_SRC##*/}"
  lab_menu || return 0
  lab_process "$LAB_SRC"
}

lab_url_flow() {
  # menu option 11: URL -> download -> lab
  lab_menu || return 0
  if lab_needs_video; then
    say '[LAB] Downloading video (best iPhone-friendly MP4)...'
    run_download "$(best_selector)" merge || return 1
  else
    say '[LAB] Downloading best audio...'
    if have ffmpeg; then
      run_download 'bestaudio/best' m4a || return 1
    else
      run_download 'bestaudio[ext=m4a]/bestaudio' none || return 1
    fi
  fi
  lab_process "$OUTPUT_FILE"
}

lab_doctor() {
  say 'Cinema Audio Lab Doctor'
  say '-----------------------'
  if have ffmpeg; then say 'ffmpeg: OK'; else say 'ffmpeg: MISSING (Audio Lab disabled)'; return 1; fi
  for flt in arnndn afftdn dynaudnorm alimiter amerge pan volumedetect; do
    if has_filter "$flt"; then say "filter $flt: OK"; else say "filter $flt: missing"; fi
  done
  if [ -s "$(rnn_model_path)" ]; then say "voice model ($RNN_MODEL): installed"
  elif ensure_rnn_model; then say "voice model ($RNN_MODEL): downloaded now"
  else say "voice model ($RNN_MODEL): NOT available (basic filter fallback)"; fi
  if replicate_token >/dev/null 2>&1; then say 'AI STEMS token: set'; else say 'AI STEMS token: not set (c --setup-ai)'; fi
  if have curl; then say 'curl: OK'; else say 'curl: missing'; fi
  return 0
}

safe_local_flow() {
  # c --safe [FILE] : Photos SAFE for a file already on the iPhone (offline).
  have ffmpeg || { err 'Photos SAFE needs ffmpeg in a-Shell.'; return 1; }
  if [ -n "$SAFE_FILE" ]; then
    LAB_SRC=$SAFE_FILE
    [ -f "$LAB_SRC" ] || [ ! -f "$DOWNLOAD_DIR/$LAB_SRC" ] || LAB_SRC="$DOWNLOAD_DIR/$LAB_SRC"
  else
    lab_pick_local || return 1
  fi
  [ -f "$LAB_SRC" ] || { err "File not found: $LAB_SRC"; return 1; }
  OUTPUT_FILE=$LAB_SRC
  OUTPUTS=''
  OUTPUT_COUNT=1
  SAVE_MODE='photos'
  finish
}

doctor_encode_test() {
  # $1 label ; rest = codec args. 1-second synthetic clip, nothing downloaded.
  label=$1; shift
  t="$STATE_DIR/.doctor_test.mp4"
  rm -f "$t" 2>/dev/null || true
  if ffmpeg -y -nostdin -hide_banner -loglevel error \
      -f lavfi -i 'testsrc2=size=720x1280:rate=30:duration=1' \
      -pix_fmt yuv420p "$@" "$t" > /dev/null 2> "$STATE_DIR/.doctor_err.txt" \
     && [ -s "$t" ]; then
    say "  $label: WORKS"
  else
    say "  $label: FAILS ($(tail -n 1 "$STATE_DIR/.doctor_err.txt" 2>/dev/null))"
  fi
  rm -f "$t" 2>/dev/null || true
}

doctor() {
  say "$APP $VERSION — Doctor"
  say '----------------------------------------'
  mkdir -p "$STATE_DIR" 2>/dev/null || true
  if find_ytdlp; then
    say "yt-dlp: $("$YTDLP" --version 2>/dev/null || printf 'unknown')"
    if detect_fb_impersonation; then
      say "browser impersonation: $FB_IMPERSONATE"
    else
      say 'browser impersonation: unavailable (normal on iPhone; not fatal)'
    fi
  else
    say 'yt-dlp: NOT FOUND  ->  pip install yt-dlp'
  fi
  if have pbpaste; then say 'clipboard (pbpaste): OK'; else say 'clipboard (pbpaste): missing'; fi
  if ! have ffmpeg; then
    say 'ffmpeg: MISSING (Photos SAFE and Audio Lab disabled)'
    return 1
  fi
  say 'ffmpeg: OK'
  say ''
  say 'Encoders present in this ffmpeg:'
  for enc in h264_videotoolbox hevc_videotoolbox libx264 mpeg4 aac; do
    if has_encoder "$enc"; then say "  $enc: yes"; else say "  $enc: no"; fi
  done
  say ''
  say 'Live test on this iPhone (keep a-Shell on screen):'
  has_encoder h264_videotoolbox && doctor_encode_test 'hardware H.264' -c:v h264_videotoolbox -b:v 2000k -allow_sw 1
  has_encoder hevc_videotoolbox && doctor_encode_test 'hardware HEVC' -c:v hevc_videotoolbox -b:v 2000k -allow_sw 1 -tag:v hvc1
  has_encoder libx264 && doctor_encode_test 'software H.264' -c:v libx264 -preset veryfast
  has_encoder mpeg4 && doctor_encode_test 'built-in MPEG-4' -c:v mpeg4 -q:v 2 -tag:v mp4v
  say ''
  say 'Photos SAFE copies H.264/HEVC files without any encoder, so most'
  say 'downloads work even when every encoder above FAILS.'
  return 0
}

update_ytdlp() {
  say '[C] Updating yt-dlp...'
  if have pip; then pip install --upgrade yt-dlp && return 0; fi
  if have python3; then python3 -m pip install --upgrade yt-dlp && return 0; fi
  err 'pip not found. In a-Shell run: pip install --upgrade yt-dlp'
  return 1
}

main() {
  parse_args "$@"

  if [ "$INSTALL" -eq 1 ]; then
    install_self
    exit 0
  fi

  if [ "$FB_SETUP_COOKIES" -eq 1 ]; then
    setup_facebook_cookies
    exit 0
  fi

  if [ "$SETUP_AI" -eq 1 ]; then
    setup_ai
    exit 0
  fi

  if [ "$DO_UPDATE" -eq 1 ]; then
    update_ytdlp
    exit $?
  fi

  if [ "$LAB_DOCTOR" -eq 1 ]; then
    lab_doctor
    exit $?
  fi

  if [ "$DOCTOR" -eq 1 ]; then
    doctor
    exit $?
  fi

  if [ "$SAFE_LOCAL" -eq 1 ]; then
    safe_local_flow
    exit $?
  fi

  # Offline: works on files already on the iPhone, yt-dlp not required.
  if [ "$LAB_LOCAL" -eq 1 ]; then
    lab_local_flow
    exit $?
  fi

  find_ytdlp || {
    err 'yt-dlp not found.'
    exit 1
  }

  if [ "$FB_DOCTOR" -eq 1 ]; then
    facebook_doctor
    exit $?
  fi

  prompt_url

  if is_facebook_profile_url; then
    facebook_profile_flow
    exit $?
  fi

  show_menu
  printf 'Number: '
  IFS= read -r choice || choice=''

  case "$choice" in
    0)
      exit 0
      ;;
    1)
      choose_destination video
      say '[C] Downloading BEST...'
      sel=$(best_selector)
      run_download "$sel" merge || exit 1
      ;;
    2|3|4|5|6)
      case "$choice" in
        2) h=2160; label='2160p' ;;
        3) h=1440; label='1440p' ;;
        4) h=1080; label='1080p' ;;
        5) h=720;  label='720p' ;;
        6) h=480;  label='480p' ;;
      esac
      choose_destination video
      say "[C] Downloading $label or best lower quality..."
      set_quality_cap "$h"
      sel=$(selector_for_height "$h")
      run_download "$sel" merge || exit 1
      ;;
    7)
      choose_destination video
      say '[C] Downloading FAST MP4...'
      run_download 'b[ext=mp4]/best' none || exit 1
      ;;
    8)
      choose_destination audio
      say '[C] Downloading AUDIO M4A...'
      if have ffmpeg; then
        run_download 'bestaudio' m4a || exit 1
      else
        run_download 'bestaudio[ext=m4a]/bestaudio' none || exit 1
      fi
      ;;
    9)
      choose_destination audio
      say '[C] Downloading AUDIO MP3...'
      run_download 'bestaudio' mp3 || exit 1
      ;;
    10)
      show_exact_formats || exit 1
      ;;
    11)
      lab_url_flow
      exit $?
      ;;
    *)
      err 'Wrong number.'
      exit 1
      ;;
  esac

  finish
}

main "$@"
