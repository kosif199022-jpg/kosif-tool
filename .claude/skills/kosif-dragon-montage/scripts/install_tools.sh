#!/usr/bin/env bash
# Dragon Montage — install the tools the protocol needs (Linux / macOS).
# The owner runs this; Claude never does. Idempotent: it asks dm_doctor.py what is
# MISSING and installs only that, so running it twice does nothing the second time.
#
#   bash .claude/skills/kosif-dragon-montage/scripts/install_tools.sh [--tier required|recommended|all] [--yes] [--dry-run]
#
# Model files (e.g. the YuNet face model) come as `dm_doctor.py fetch <id>` lines in the plan
# (sha256-checked, saved to the skill's git-ignored models/ folder).
# Python libraries go into <repo>/.venv (created if absent). Run the montage with
# <repo>/.venv/bin/python afterwards.
set -euo pipefail

TIER=recommended; YES=0; DRY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --tier) TIER="$2"; shift 2 ;;
    --yes|-y) YES=1; shift ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) sed -n 2,12p "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../../../.." && pwd)"
cd "$ROOT"

case "$(uname -s)" in
  Darwin) OS=macos ;;
  Linux) OS=linux ;;
  *) echo "Use install_tools.ps1 on Windows." >&2; exit 2 ;;
esac

SUDO=""
if [ "$OS" = linux ] && [ "$(id -u)" != 0 ]; then SUDO="sudo"; fi

# 1) Python itself (needed to run the doctor).
if ! command -v python3 >/dev/null 2>&1; then
  echo "== Python 3 مش موجود — هثبته"
  if [ "$OS" = linux ]; then $SUDO apt-get update && $SUDO apt-get install -y python3 python3-venv python3-pip
  else brew install python@3.13; fi
fi

# 2) A venv for the Python libraries (PEP 668 blocks system pip on new distros).
VENV="${KOSIF_VENV:-$ROOT/.venv}"
if [ ! -x "$VENV/bin/python" ]; then
  echo "== هعمل venv في $VENV"
  if [ "$DRY" = 0 ]; then python3 -m venv "$VENV" || { $SUDO apt-get install -y python3-venv && python3 -m venv "$VENV"; }; fi
fi
PY="$VENV/bin/python"; [ -x "$PY" ] || PY=python3

# 3) Ask the doctor for the exact plan (missing only) and run it line by line.
PLAN="$("$PY" "$HERE/dm_doctor.py" install-plan --os "$OS" --tier "$TIER" --python "$PY")"
echo "$PLAN"
CMDS="$(printf '%s\n' "$PLAN" | grep -v '^#' | grep -v '^[[:space:]]*$' || true)"
if [ -z "$CMDS" ]; then echo "✅ مفيش حاجة ناقصة."; exit 0; fi
[ "$DRY" = 1 ] && exit 0
if [ "$YES" = 0 ]; then
  read -r -p "أنفّذ الأوامر دي؟ [y/N] " ans
  case "$ans" in y|Y|yes) ;; *) echo "اتلغى."; exit 0 ;; esac
fi
while IFS= read -r line; do
  [ "$(id -u)" = 0 ] && line="${line//sudo /}"
  echo "→ $line"
  bash -c "$line" || echo "⚠️ فشل: $line (كمّل الباقي)"
done <<< "$CMDS"

# 4) Verify.
"$PY" "$HERE/dm_doctor.py" doctor --tier "$TIER" || true
