# JohnHeibel/ClaudeAnimationBase — REA dissection (@0ac8bf2b31942376cb6b8c4074715595d512acd2, 2,796★, MIT)

## What it really does
Browser-side 2D hand-painted cartoon kit + agent rulebook. studio.html loads p5 2.x + p5.brush 2.2.3, then config → core → clawd → timeline → sheets → one scene. noLoop(); frames drawn on demand by `window.renderAt(t)` (core.js:301): set T, redraw, composite (core.js:293-300) to a 2D canvas, lettering, multiply grain + vignette. drawWorld(t) (timeline.js:340-350) picks the active shot from a sorted [t0, fn] list and calls fn(t, lt, dur).
render.mjs (puppeteer-core + system Chrome): --sheet/--strip, --crop/--crop-at (follows a world point through the camera), --stills, --png, --frames (parallel, resumable JPEG), --encode (libx264 CRF17 + AAC), --clip (mjpeg pipe). gpu_probe.mjs prints the WebGL renderer for 4 flag sets.
Determinism: no state between frames; boilSeed(key) = FNV-1a(`key|floor(T*12)`) reseeds random per element (core.js:25-26, 288); linework boils at 12 drawings/s (on twos at 24 fps).

## Capabilities (12)
1. Viewer "reads" timing sheet (guide 49-59, 115-141, 447-461). 2. Per-element boil seeding (core.js:19-26, 288). 3. Pure frame contract fn(t, lt, dur), shots, LOOPS (timeline.js:1-50). 4. Parallel, resumable, atomic frames: workers pull next missing frame, <1000 B = missing, .tmp→rename (render.mjs:116-136; encode 45-53). 5. Contact sheet / strip / crop / crop-at (core.js:302-317, 89-97; render.mjs:88-96). 6. GPU backend flags + probe (render.mjs:55-68). 7. Acted emotion changes (clawd.js:542-615). 8. Closed-form acting: jump, take, stroll, spring/ring, arcPt, onTwos, pulse/beatN, kf (core.js:28-84). 9. brushWipe + irisShape for any polygon (timeline.js:357-380; core.js:117-127). 10. Paper look: seeded stains/fibres, multiplied grain, additive glow (core.js:99-116, 246-265). 11. Rulebook: avoid twinning, review budget, 15 common failures (guide 15-110, 169-200, 423-441). 12. p5.brush quirk: draw each shape around its own centre at zoom ≥2 (core.js:174-184).

## Covered vs new
Covered already: pure-frame story.js, Chromium+ffmpeg render with resume, sheet stills and freeze QA (cartoon-audio-short); easing/keyframes (motion-toolkit); strips/onion skin (video-eyes); contact sheets (cinema-lab).
New: reads timing as a checkable storyboard; boil discipline + jitter failure; atomic size-checked frames with a worker pool; crop-at through the camera; ANGLE GPU selection (our kit hard-codes SwiftShader, 3-10 s/frame); 2D p5.brush painted medium; acted emotions; brush wipe and shaped iris; avoid-twinning and ending-rhymes-opening rules.

## Native: native_cab.py (stdlib + numpy + opencv; exit 0 ok / 3 review / 2 error)
reads-lint (overlap, too-short reads 0.4 s + 0.2 s per hard word, final read ≥1.0 s, missing transitions, on-screen text EN+AR; our heuristic thresholds), boil-audit (jitter_ratio = same-boil vs cross-boil change; >0.5 = jitter; frozen runs ≥0.4 s), seed (bit-exact with JS: `sky|0` → 3552230858), todo (missing frames), same (two renders pixel-identical, tol 2).
Self-test: `{"self_test": "PASS", ... reads_lint good ok / bad 7 errors 5 warnings, boil_audit good 0.0263 buggy 1.0009, same ok}`.
Not ported: p5.brush engine and the character rig (JS + npm, link only), crop-at.

## Caveats
Needs npm, Chrome, ffmpeg (not run). renderSheet evals --crop-at strings (core.js:307). Google Fonts fetched at load. The "no on-screen text" rule conflicts with Arabic kinetic type; the owner's request wins.

## REA log
analyze_javascript_application on render.mjs, gpu_probe.mjs, src/core.js, timeline.js, config.js → ev_a14f641a313cb205139c30f8cc96a77bda0d3174fc4f8b9ef3db96a1a3cc4624 (parent ev_eccc988454083d897d8962acf805e87ad135d53aad6bff1118497cec53cd62ec): 5 files, 0 parse failures, 7,614 AST nodes, child-process 4 (ffmpeg), network/timer 0. close_binary ok. Rest read by hand.
