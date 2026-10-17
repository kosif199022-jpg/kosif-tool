# KOSIF Superpowers — Motion Runtime & Engine Fusion

**This is an executable capability pack, not just a repo bookmark list.** KOSIF now owns original deterministic SVG/JS motion code, a safe film creator, reusable math and animation utilities, 25 engine route cards, and the existing HTML→MP4/FFmpeg renderer from the full kosif-tool checkout.

## Working KOSIF-owned capabilities

| Capability | Working implementation |
|---|---|
| Arabic hand-drawn whiteboard | SVG stroke reveal, tracked virtual pen, cream paper |
| Editable vector film | Standalone film.html with window.__kosif.seek(t) |
| Multi-keyframe interpolation | motion_toolkit.mjs: interpolate(), timeline() |
| Easing | linear, smooth, cubic, ease-in/out |
| Sketch look | seededSketchLine() original jittered deterministic path |
| Camera | camera() pan/zoom and parallax() |
| Basic moving character | walkRig() plus SVG body/arm/leg transforms |
| Explainer diagram | Incrementally revealed bars in template |
| Arabic captions | wordCueState() tracks complete Arabic words |
| Frame arithmetic | timeCode(), assertFrameContract() |
| MP4 export pathway | Existing tools/render_html.cjs requires Playwright, FFmpeg and Chromium |

These are runnable local motion mechanics, not claims that Blender, GSAP, Remotion, Lottie, or any other provider is preinstalled. Full character rigging, auto-motion-video imitation, full timeline editor and proprietary plugins are not implemented by this small core.

## CLAUDE: execute instead of just describing

1. Run the skill script:

       python3 $SKILL_DIR/scripts/motion_runtime.py doctor
       python3 $SKILL_DIR/scripts/motion_runtime.py engines --family whiteboard

2. For a real editable whiteboard film, create a new directory (must not exist):

       python3 $SKILL_DIR/scripts/motion_runtime.py scaffold --out /absolute/new_project --title "قصيف يرسم" --subtitle "الرسم والتحريك بالكود" --duration 8 --fps 30

3. Open the generated film.html in a browser. Check frame states by calling window.__kosif.seek(2.5), window.__kosif.seek(4) and window.__kosif.seek(7) separately. An HTML file alone is not a verified film.
4. Render only after checking current dependencies in the complete kosif-tool checkout:

       python3 $SKILL_DIR/scripts/motion_runtime.py render --in /absolute/new_project/film.html --out /absolute/new_project/preview.png --fps 30 --run
       python3 $SKILL_DIR/scripts/motion_runtime.py render --in /absolute/new_project/film.html --out /absolute/new_project/film.mp4 --fps 30 --run

   Requires Node.js, a configured Chromium/Playwright runtime, the repository renderer and FFmpeg. Does not install anything. The repository may be unavailable inside a skill-only upload.
5. To incorporate original voice use --audio /absolute/original.wav with MP4. User audio stays the master clock; align beats/words to the storyboard and revise frame timings, not the voice.
6. After render, inspect frames and ffprobe output. From full repo root:

       python3 tools/verify_video.py /absolute/new_project/film.mp4 --aspect 9:16 --fps 30 --duration 8

   Add --audio /absolute/original.wav only when original voice was included. Record exact artifact paths and failures. Do not call preview or CLI exit-code proof of creative correctness.

**Limit:** The example uses a fixed eight-second sequence; increasing duration requires extending the actual drawing/character/storyboard. This produces true moving frames, not static slide cuts, but is not a generalized movie editor.

## The 25 external engines as optional adapters

The new data/motion_engines.json records URL, family, capability, license note, installation requirements, and current scope for all 25 requested external projects.

- Sketch: native SVG + seededSketchLine and optional Rough.js/Vivus, if installed and tested.
- Timeline and effects: native timeline/ease primitives, optional Anime.js/Motion/GSAP/Mo.js.
- Vector editors: Excalidraw, tldraw, Fabric, Paper, Graphite. Use external editors or versions only with permission; preserve editable SVG paths.
- 2D graphics: PixiJS, p5.js, Lottie Web and the native SVG layer.
- 3D: Three.js and React Three Fiber, Blender for real rigs/Grease Pencil.
- 2D character: Krita, Pencil2D, OpenToonz, Synfig, with original assets and separately tested exports.
- Explanatory: Manim or Motion Canvas if their runtimes are configured.
- React video: Remotion (existing KOSIF starter) with version and commercial licensing check.
- Rendering: KOSIF render_html with FFmpeg for MP4; resolution, frame rate and audio track must be verified on the actual file.

Select the fewest engines required to satisfy a particular brief. Do not preload all 25. Learn from their methods and implement original code; never bundle entire repos, copyrighted assets or tools without the required license and user permission. A GitHub license field saying NOASSERTION is not permission to redistribute.

No extra 25 "proven capabilities" are added to KOSIF's historic 4,223-count power catalog. Those are external backend options and designs; working original utilities have their own independent test evidence.

## Forward development

Exact animation matching to a user-provided reference requires measured shot cuts, tracking, path geometry recovery, keyframe fitting, text correspondence and rendered side-by-side QA. This is a separate future capability; this pack does not falsely claim to reproduce arbitrary third-party footage.

## Verification

    python3 -m unittest discover -s "$SKILL_DIR/evals" -p test_motion_runtime.py -v
    node --test "$SKILL_DIR/evals/test_motion_toolkit.mjs"

Python tests cover scaffold, deterministic structure and output/overwrite safety. Node tests cover interpolation and timing math. Browser render and media QA must be tested separately with an actual artifact.
