# patch-gg/pixelfx — REA dissection (@044e12a45dc9cc312cec50ee606dfc98afe5adc2, 6,311★, MIT © 2026 Patch, © 2026 Hugo Duprez)

## What it really does
Dependency-free JS ES-module library drawing ~244 pixel-art VFX procedurally (no images). Each effect `src/fx/<category>/<name>.js` exports `meta` (size, origin, duration, loop, fps, palette, seed) and `draw(p,t,o)` or `create(o)`. A Painter draws into two buffers: **color** (opaque pixels faded only by a 4×4 Bayer dither, painter.js:10,46-53; blended discs for smoke, painter.js:69-77) and **light** (additive glow, fx.js:187-218). Simulations substep at 120 Hz regardless of output fps (fx.js:153-155). Everything seeded (mulberry32 + integer hash, math.js:54-99); check.mjs:93 rejects Math.random. act.js adds an acting character: 12 fps pose holds (34-43), hit-stop freeze + decaying shake (239-270). Tools: contact sheets, MP4/GIF via spawned ffmpeg (fxlib.mjs:258), Aseprite sprite sheets (221-240), lint, localhost gallery. skills/pixelfx/SKILL.md = draft → render → look → refine loop.

## Capabilities (14)
1. Colour + additive light composite; over transparency light is premultiplied, alpha = brightest channel — fx.js:187 (native)
2. Bayer ordered-dither alpha — painter.js:10,46 (native)
3. Pixel-art particles: SPARK floor bounce, FIRE cooling to SMOKE, SMOKE, EMBER, BRAND, GRIT — sim.js:31-236 (native: explosion, sparks, campfire, embers)
4. 120 Hz fixed substeps — fx.js:153 (native)
5. 28 hue-shifted ramps, fit() and stepped at() — color.js:37-80 (native ramp-map)
6. Hit-stop freeze, decaying shake, 12 fps holds — act.js:34-43,239-270 (native on real footage)
7. Anime impact frame (two ink frames + two inverted) — impacts/impact-frame.js:16-73 (native)
8. Level-set field wipes — transitions/_lib.js:121-152
9. fbm-ranked pixel dissolve — transitions/pixel-dissolve.js:222-250
10. CRT off/on — transitions/crt-off.js:17-70
11. Tileable/looping noise — math.js:129-152
12. Aseprite sprite-sheet export — tools/lib/fxlib.mjs:221-240 (native --sheet)
13. VFX lint — tools/check.mjs
14. Sprites from strings + pixel fonts — painter.js:304-334, font.js

## Covered vs new
Covered: Bayer fade, dither, CRT look, manga burst, glitch, ASCII, riso (kosif-dragon-mind fam_pixel_retro_stylized.py); generic SVG particles (particles.py); beat freeze-cut; cinema-lab wipes/LUTs.
New: two-buffer colour/light model with transparency-correct glow; pixel-art particle physics; hue-shifted ramp library with no-blend mapping; hit-stop + shake + 12 fps holds + impact frame on real footage; Aseprite sheets. Field wipes and pixel dissolve: next port candidates.

## Native: native_pixelfx.py (numpy + OpenCV, --json)
`palettes`; `ramp-map IN OUT [--palette --pixel --no-dither]`; `fx {explosion,sparks,campfire,embers} OUT [--bg video|image|#hex|transparent --size --pixel --x --y --seed --palette --light --sheet]`; `hitstop IN OUT --hits --stop --shake --amp --impact --step`; `self-test`.
Self-test: `{"ok": true, "passed": 19, "total": 19}` (ramp colours only, dither, light→alpha [254,128,0,172], seed determinism, explosion flares then dies, sparks bounce at ground, RGBA sheet 36 frames, freeze adds frames, impact two-tone, shake settles, step=12 → 12 unique frames). 480×270 45-frame explosion ≈1 s. Agent visually checked demo/contact.png (white flash → fireballs cooling to red → grey smoke).
Examples: `fx explosion out.mp4 --bg clip.mp4 --size 1080x1920 --pixel 6 --x 540 --y 1200` · `hitstop clip.mp4 hit.mp4 --hits 2.35 --stop 0.12 --shake 0.3 --amp 10 --impact` · `ramp-map photo.jpg retro.png --palette neon --pixel 6`

## License
MIT; sim.js adapts Sprite Fusion (MIT), act.js adapts Hollow Crown (MIT). Palette hex data reused with attribution in the docstring. **Do NOT vendor gallery/fonts/PatchPixel-Regular.woff2 (all rights reserved).**

## Caveats
Effects authored ≈320×180: render low-res, upscale nearest. Python particles suit hundreds, not tens of thousands. Hit-stop stretches time: retime audio separately. Repo tools spawn ffmpeg and a localhost server; never npm install.

## REA log
analyze_javascript_application, 7 src/core files → parent ev_e9d82930fb4292c962ee55849c7adedf3a204f7a586bab439bdf8a6939da1087, view ev_426df204fdd1407328085d9eaf8b2bf633cdb19825d336536c03ec085bea6744, root sha256 ace505275d8adb729c51d8e83f54a34fa6c4f0aaadb4c053a11c066ea45fcd5f: 7 parsed, 0 failures, 17,906 AST nodes; request/child-process/timer/event/config = 0 (pure computation). Partial (288 files unselected). close_binary ok. Rest read by hand; no repo code run.
