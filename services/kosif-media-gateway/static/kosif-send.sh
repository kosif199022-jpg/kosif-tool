#!/bin/sh
# kosif-send: download a video ON THIS iPHONE (a-Shell) and send it to the owner's KOSIF Media Gateway,
# so Claude can fetch and analyse it. The download uses this phone's own connection, like Cinema C.
#
#   kosif-send --setup          paste the gateway token once (stored in ~/Documents/.kosif/token, mode 600)
#   kosif-send URL              download with yt-dlp (H.264/AAC first, portrait aware) and upload
#   kosif-send --file PATH      upload a video already on the phone (Cinema C output, Photos export)
#   kosif-send --check          show the gateway status
#
# The token is never printed and never put on a command line (curl reads it from a private header file).
# No cookies, no login: what YouTube refuses on this phone is refused here too.
set -u

GATEWAY="${KOSIF_GATEWAY_URL:-https://kosif-media-gateway-free-20261030.onrender.com}"
HOME_DIR="${HOME:-.}/Documents/.kosif"
TOKEN_FILE="$HOME_DIR/token"
OUT_DIR="${HOME:-.}/Documents/KOSIF_Sent"
QUALITY="${KOSIF_QUALITY:-1080}"

say() { printf '%s\n' "$*"; }
die() { printf 'kosif-send: %s\n' "$*" >&2; exit 1; }

mkdir -p "$HOME_DIR" "$OUT_DIR" || die "cannot create folders"
chmod 700 "$HOME_DIR" 2>/dev/null

setup() {
  umask 077
  say "الصق توكن البوابة واضغط Enter (مش هيظهر تاني):"
  stty -echo 2>/dev/null
  IFS= read -r tok
  stty echo 2>/dev/null
  tok=$(printf '%s' "$tok" | tr -d ' \r\n')
  [ -n "$tok" ] || die "مفيش توكن"
  printf '%s' "$tok" > "$TOKEN_FILE" || die "cannot save token"
  chmod 600 "$TOKEN_FILE" 2>/dev/null
  say "اتحفظ. جرّب: kosif-send --check"
}

auth_header_file() {
  [ -s "$TOKEN_FILE" ] || die "شغّل kosif-send --setup الأول"
  umask 077
  hdr="$HOME_DIR/.hdr.$$"
  printf 'Authorization: Bearer %s\n' "$(cat "$TOKEN_FILE")" > "$hdr"
  printf '%s' "$hdr"
}

check() {
  curl -sS --max-time 90 "$GATEWAY/health" || die "البوابة مش بترد"
  say ""
}

# Keep only plain ASCII URL characters (a link pasted with Arabic text around it still works).
clean_url() {
  printf '%s' "$1" | tr -c 'A-Za-z0-9:/?&=._~%#@!$+,;-' ' ' | tr ' ' '\n' | grep -E '^https?://' | head -n 1 | sed 's/[.,;!]*$//'
}

download() {
  url=$(clean_url "$1")
  case "$url" in http*://*) ;; *) die "ده مش لينك: $1" ;; esac
  command -v yt-dlp >/dev/null 2>&1 || die "yt-dlp مش متسطب في a-Shell (pip install yt-dlp)"
  work="$HOME_DIR/work.$$"
  mkdir -p "$work"
  # Cinema C V34 rule: res:N caps the SHORTER side, so a 1080x1920 Short counts as 1080p.
  path=$(yt-dlp --no-config --no-playlist --newline --no-progress \
      -f "bv*[vcodec~='^(avc|h264)']+ba[acodec~='^(mp4a|aac)']/bv*+ba/b[ext=mp4]/b" \
      -S "res:$QUALITY,fps,vcodec:h264,acodec:aac" --merge-output-format mp4 \
      -o "$work/%(title).80B [%(id)s].%(ext)s" --print after_move:filepath -- "$url" | tail -n 1)
  if [ -z "$path" ] || [ ! -s "$path" ]; then
    rm -rf "$work"
    die "التحميل فشل على الموبايل كمان (شوف الرسالة فوق)"
  fi
  final="$OUT_DIR/$(basename "$path")"
  mv "$path" "$final" && rm -rf "$work"
  SRC_URL="$url"
  FILE="$final"
}

upload() {
  f="$1"
  [ -s "$f" ] || die "الملف مش موجود: $f"
  size=$(wc -c < "$f" | tr -d ' ')
  name=$(basename "$f" | tr -cd 'A-Za-z0-9._ -' )
  [ -n "$name" ] || name="video.mp4"
  hdr=$(auth_header_file)
  say "برفع $(basename "$f") ($((size / 1048576)) MB)…"
  res=$(curl -sS --max-time 900 -X POST "$GATEWAY/v1/upload" -H "@$hdr" \
        -H "Content-Type: video/mp4" -H "X-Filename: $name" -H "X-Source-Url: ${SRC_URL:-}" \
        --data-binary "@$f")
  rc=$?
  rm -f "$hdr"
  [ $rc -eq 0 ] || die "الرفع فشل (curl $rc). البوابة المجانية ممكن تكون نايمة: جرّب تاني بعد دقيقة"
  case "$res" in
    *'"ok": true'*) say "وصل لـ KOSIF واتأكد منه. قول لـ Claude: «رفعت»"
                    printf '%s\n' "$res" | sed -n 's/.*"upload_id": "\([0-9a-f]*\)".*/upload_id: \1/p' ;;
    *) say "البوابة رفضت الملف:"; printf '%s\n' "$res"; exit 1 ;;
  esac
}

SRC_URL=""
FILE=""
case "${1:-}" in
  --setup) setup ;;
  --check) check ;;
  --file) [ -n "${2:-}" ] || die "اكتب مسار الملف"; upload "$2" ;;
  ""|-h|--help) sed -n '2,12p' "$0" ;;
  *) download "$1"; upload "$FILE" ;;
esac
