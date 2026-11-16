#!/usr/bin/env bash
# Creates a new short project:  bash tools/setup.sh <project_dir>
# Needs: node, python3 + numpy + Pillow, ffmpeg, Playwright Chromium. three.js, the toon library and the Arabic font are vendored, so no network is needed for them.
set -e
KIT="$(cd "$(dirname "$0")/.." && pwd)"; P="${1:?project dir}"
mkdir -p "$P/web/lib" "$P/web/fonts" "$P/work" "$P/stills" "$P/out"
cp "$KIT"/fonts/*.ttf "$P/web/fonts/"
cp "$KIT"/engine/*.js "$KIT"/engine/index.html "$P/web/"
cp "$KIT"/example/soldier/story.js "$P/web/story.js"        # starting point: rewrite for the new story
cp "$KIT"/example/soldier/audio.py "$P/audio.py"            # starting point: rewrite the cue table
cp "$KIT"/tools/*.mjs "$KIT"/tools/*.py "$KIT"/tools/finish.sh "$P/" 2>/dev/null || true
[ -f "$KIT/vendor/three.module.js" ] && cp "$KIT/vendor/three.module.js" "$P/web/lib/"
# three.js r160 (module build). npm first, then a sparse git clone (works where only GitHub is reachable).
if [ ! -f "$P/web/lib/three.module.js" ]; then
  ( cd /tmp && rm -rf _three && mkdir _three && cd _three && npm pack three@0.160.0 >/dev/null 2>&1 && tar xzf three-0.160.0.tgz && cp package/build/three.module.js "$P/web/lib/" ) \
  || ( cd /tmp && rm -rf _t3 && git clone -q --depth 1 --filter=blob:none --sparse --branch r160 https://github.com/mrdoob/three.js _t3 && cd _t3 && git sparse-checkout set build && cp build/three.module.js "$P/web/lib/" )
fi
# toon base: the Pen / head / face library from mromidev/claude-animated-shorts, types stripped
if [ -f "$KIT/vendor/toonbase.js" ]; then cp "$KIT/vendor/toonbase.js" "$P/web/toonbase.js"; else
  if [ ! -f "$KIT/vendor/toon.ts" ]; then mkdir -p "$KIT/vendor"; git clone -q --depth 1 https://github.com/mromidev/claude-animated-shorts /tmp/_cas && cp /tmp/_cas/templates/bridge/toon.ts "$KIT/vendor/toon.ts"; fi
  node -e "const m=require('node:module'),fs=require('fs');fs.writeFileSync(process.argv[2],m.stripTypeScriptTypes(fs.readFileSync(process.argv[1],'utf8'),{mode:'transform'}))" "$KIT/vendor/toon.ts" "$P/web/toonbase.js"
fi
cat "$P/web/toonbase.js" "$P/web/roman.js" > "$P/web/toon.js"
# playwright: use a global install if there is one
mkdir -p "$P/node_modules"
if [ ! -e "$P/node_modules/playwright" ]; then
  if [ -e "$(npm root -g)/playwright" ]; then ln -sf "$(npm root -g)/playwright" "$P/node_modules/playwright"
  else ( cd "$P" && npm i --no-audit --no-fund playwright >/dev/null ) || echo "Playwright missing: run npm i playwright && npx playwright install chromium"; fi
fi
echo "ready: $P   (after editing cast code run: cat web/toonbase.js web/roman.js > web/toon.js)"
