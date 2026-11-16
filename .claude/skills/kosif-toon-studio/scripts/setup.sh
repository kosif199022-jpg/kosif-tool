#!/usr/bin/env bash
# One-time setup: downloads the free OFL fonts (Google Fonts) into ../fonts. Needs python3 numpy opencv pillow, ffmpeg.
set -e
D="$(cd "$(dirname "$0")/.." && pwd)"; F="$D/fonts"; mkdir -p "$F"
G=https://raw.githubusercontent.com/google/fonts/main/ofl
[ -f "$F/ArchivoBlack.ttf" ] || curl -fsSL -o "$F/ArchivoBlack.ttf" "$G/archivoblack/ArchivoBlack-Regular.ttf"
[ -f "$F/Cairo-900.ttf" ] || { curl -fsSL -o "$F/Cairo-var.ttf" "$G/cairo/Cairo%5Bslnt,wght%5D.ttf" && python3 - "$F" <<'P'
import sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
f=sys.argv[1]; v=TTFont(f+"/Cairo-var.ttf"); instantiateVariableFont(v,{"wght":900,"slnt":0},inplace=True); v.save(f+"/Cairo-900.ttf")
P
rm -f "$F/Cairo-var.ttf"; }
python3 -c "import cv2, numpy, PIL; from PIL import features; print('python ok, raqm (Arabic shaping):', features.check('raqm'))"
ffmpeg -version | head -1
ls "$D/sfx"/*.mp3 >/dev/null 2>&1 && echo "sfx ok" || echo "sfx missing: see sfx/README.md (films still render, effects are silent)"
echo ready
