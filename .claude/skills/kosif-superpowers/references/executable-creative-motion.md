# KOSIF Superpowers — Executable Creative Motion Lab v1

**This module is not a list of links.** It ships executable original KOSIF code for timed SVG animation, moving characters, camera moves, a scene compiler, a local reference-video timing probe and project-scaffold generators for external engines.

## الفهرس / contents

- [True capability matrix](#true-capability-matrix)
- [Start producing something, rather than just suggesting technologies](#start-producing-something-rather-than-just-suggesting-technologies)
- [How the 25 technologies transfer practical ideas to KOSIF](#how-the-25-technologies-transfer-practical-ideas-to-kosif)
- [Minimal custom JSON example](#minimal-custom-json-example)
- [Honest validation](#honest-validation)

## True capability matrix

| Job | Included executable component | Requirements | Honest runtime state |
|---|---|---|---|
| Create validated 9:16 scene JSON | scripts/motion_director.py sample and compile | Python 3.8+ | Bundled source |
| Draw vector paths like a real pen | assets/motion_engine.js via strokeDashoffset | Browser | Bundled source |
| Move character after drawing | animated SVG puppet limb rotations + moving outer group | Browser | Bundled source |
| Camera pan, zoom, easing | same engine via time-indexed transforms | Browser | Bundled source |
| Sync displayed Arabic words | JSON words with start/end timestamps | Actual timed transcript supplied | Bundled source, alignment not included |
| Generate real MP4 | bundled KOSIF resources/motion-runtime/render_html.cjs | Skill-only or full repo, Node, Playwright/Chromium, ffmpeg/ffprobe | Host-dependent |
| Video metadata + heuristic cut detection | scripts/motion_reference_probe.py | ffprobe, optionally ffmpeg | Host-dependent, real command |
| Create GSAP/Rough/Vivus projects | scripts/motion_stack.py scaffold gsap | User-installed npm dependencies | Generates source only |
| Create Remotion React composition | scripts/motion_stack.py scaffold remotion | User-installed Remotion and license | Generates source only |
| Create Manim animation scene | scripts/motion_stack.py scaffold manim | User-installed Manim | Generates source only |
| Create interactive 3D scene | scripts/motion_stack.py scaffold three | User-installed Three.js + Vite | Generates source only |
| Create accelerated 2D scene | scripts/motion_stack.py scaffold pixi | User-installed PixiJS + Vite | Generates source only |
| Create generative art sketch | scripts/motion_stack.py scaffold p5 | User-installed p5.js + Vite | Generates source only |
| Identify 25 external creative engines | data/motion_sources.json | None | Registry is reference, not installed code |

## Start producing something, rather than just suggesting technologies

Commands from the kosif-tool repository root:

    SKILL_DIR=.claude/skills/kosif-superpowers
    python3 "$SKILL_DIR/scripts/motion_director.py" doctor
    python3 "$SKILL_DIR/scripts/motion_director.py" sample --out ./storyboard.json
    python3 "$SKILL_DIR/scripts/motion_director.py" compile ./storyboard.json --out ./movie.html

The resulting HTML is an original seekable SVG animation with 3 scenes, 9 seconds, revealed paths, Arabic subtitles timed from the supplied scene words, camera pan/zoom, and articulated moving character. Preview movie.html in a browser. It uses no third-party JS imports. Edit storyboard.json and compile into another new file to produce your own project.

The JavaScript contract is window.__kosif = {duration, fps, seek(t)}. Calling seek(2.5) draws exactly 2.5 seconds into the timeline; it does not depend on real-time animation speed, so a frame-by-frame renderer can call seek(i/fps) for every frame.

**Audio workflow:** user-provided audio is the master timeline. A user's uploaded audio is not transcribed or force-aligned by this program. Obtain accurate word timestamps using actual alignment tooling if available, then put them into scene.words, not guessed times. Arabic words remain intact.

### Reference video — actual metadata and rough cuts, not invented 1:1 motion extraction

    python3 "$SKILL_DIR/scripts/motion_reference_probe.py" /authorized/local/reference.mp4 --cuts --out ./reference-evidence.json

Outputs real duration, video dimensions, frame-rate string, audio stream presence and heuristic visual-cut timestamp candidates using ffprobe/ffmpeg. Does not track poses, decompile a video, recreate its typography or guarantee visual similarity. For meaningful imitation, inspect permitted video frames, track elements separately, estimate motion and timing, and compare keyframes with the newly rendered result.

### MP4 render via bundled KOSIF-owned renderer

This skill **bundles a copied KOSIF-owned MIT renderer** at resources/motion-runtime/render_html.cjs and a verification script at scripts/verify_video.py (plus aspects.py). It can be used from a skill-only Claude upload provided that Node.js, a configured Playwright/Chromium installation, ffmpeg and ffprobe exist in the execution environment. Packaging code does not install these runtimes or prove a video was rendered.

    python3 "$SKILL_DIR/scripts/motion_director.py" render ./movie.html --out ./movie.mp4 --audio /absolute/path/voice.wav
    python3 "$SKILL_DIR/scripts/verify_video.py" ./movie.mp4 --aspect 9:16 --fps 30 --duration 9 --audio /absolute/path/voice.wav

Never claim MP4 created until the output file and verification are observed. The renderer encodes/muxes as documented; the audio should not be retimed, but actual codec, loudness and duration still require verification. For silent clips omit --audio and use the correct no-audio verification.

### Optional third-party project scaffolds (not installers)

    python3 "$SKILL_DIR/scripts/motion_stack.py" list
    python3 "$SKILL_DIR/scripts/motion_stack.py" doctor
    python3 "$SKILL_DIR/scripts/motion_stack.py" scaffold gsap --out ./kosif-gsap
    python3 "$SKILL_DIR/scripts/motion_stack.py" scaffold remotion --out ./kosif-remotion
    python3 "$SKILL_DIR/scripts/motion_stack.py" scaffold manim --out ./kosif-manim
    python3 "$SKILL_DIR/scripts/motion_stack.py" scaffold three --out ./kosif-three
    python3 "$SKILL_DIR/scripts/motion_stack.py" scaffold pixi --out ./kosif-pixi
    python3 "$SKILL_DIR/scripts/motion_stack.py" scaffold p5 --out ./kosif-p5

The GSAP project imports installed gsap, roughjs and vivus, and exposes a frame-seekable animation timeline. The Remotion project includes a valid React composition and render script; install dependencies only when the user approves and check the Remotion company license for commercial usage. The Manim project includes a Python Scene with path creation and MoveAlongPath. The Three.js, PixiJS, and p5.js scaffolds include original frame-seekable interactive renderers, but depend on locally installed library packages and must be built and tested before runtime claims. Generated sources require real package versions and full environment verification; they are not pre-bundled copies of the underlying engines.

## How the 25 technologies transfer practical ideas to KOSIF

| Goal | Original ecosystems | Actual route |
|---|---|---|
| Handwriting and whiteboard | Excalidraw, tldraw, Rough.js, Vivus, Paper.js | Native SVG stroke-draw engine bundled; optional Rough/Vivus adapter |
| Keyframes, easing, effects | Anime.js, GSAP, Motion, Mo.js, Motion Canvas | Native time-indexed movements bundled; GSAP editable scaffold |
| 2D graphics and editor | PixiJS, Fabric.js, p5.js, Graphite | Procedural SVG vectors bundled; full Canvas editor not bundled |
| 3D and rigs | Three.js, React Three Fiber, Blender | Future authorized backend, not installed |
| 2D animation studio | OpenToonz, Krita, Synfig, Pencil2D | Native minimal SVG puppet bundled, not equivalent to those applications |
| Explanation and infographics | Manim, Motion Canvas | Manim scaffold and native timeline bundled |
| Render and audio | Remotion, FFmpeg | Existing KOSIF HTML video renderer and optional Remotion scaffold |
| Lottie playback | Lottie Web | Source integration idea; requires separately licensed JSON assets |

No third-party source or binaries are copied into this module. Every external engine retains its own license; check actual file-level licensing, dependencies and current releases before installation. Remotion has special commercial/company terms and GSAP has a standard license; do not assume GitHub stars or source visibility grant resale rights.

## Minimal custom JSON example

    {
      "version":1, "width":1080, "height":1920, "fps":30, "duration":4,
      "scenes":[{
        "id":"first", "start":0, "end":4, "background":"#f4f0e6",
        "camera":{"fromZoom":1, "toZoom":1.1, "start":0, "end":4},
        "words":[{"text":"مرحبًا", "start":0.1, "end":1.1}],
        "elements":[
          {"type":"text", "text":"خط يُرسم", "x":540, "y":400, "start":0.2, "end":1.2},
          {"type":"path", "d":"M100 600 L980 600", "start":0.6, "end":2.5},
          {"type":"character", "x":520, "y":1200, "start":1.3, "end":2.2,
            "move":{"fromX":-70, "toX":100, "start":2.2, "end":4}}
        ]
      }]
    }

Scene intervals must be continuous and word intervals ordered. SVG paths and colors are validated; external scripts/URLs are not accepted; output file overwrite is disallowed.

## Honest validation

    python3 -m unittest discover -s "$SKILL_DIR/evals" -p 'test_motion_*.py' -v
    node --check "$SKILL_DIR/assets/motion_engine.js"
    python3 "$SKILL_DIR/scripts/check_skill.py" --evals

The skill cannot claim frame-accurate visual matching without rendered frames and reference comparison. A compiled HTML proves source generation only, and a working website alone does not prove MP4 delivery.

### Reusable animation kernel (additional independently tested primitives)

The original KOSIF resource at resources/motion-runtime/motion_toolkit.mjs exports 12 deterministic primitives: easing, interpolation, arbitrary multikeyframe tracks, SVG stroke reveal, camera movement, walk-cycle joint angles, parallax, seeded hand-drawn jitter, SMPTE-style frame timecode, whole-word Arabic subtitle cues, and output frame-contract validation. Import it from Node.js or an ES-module browser context in an authorized local project; no npm packages required.

An independently editable film is included as resources/motion-runtime/doodle-film.template.html. Its placeholders __TITLE__, __SUBTITLE__, __DURATION__, __FPS__ are substituted by the companion Python scaffold in the feature branch; in the merged canonical skill use motion_director.py sample + compile for customizable scene generation, or copy the template and replace these placeholders with properly escaped values before preview. The DOM contract test evals/test_motion_template.mjs proves that seek(t) changes the strokes/camera/character at different times, but is not a Chrome visual QA or MP4 artifact.

### Packaging for use inside Claude

    python3 "$SKILL_DIR/scripts/package_skill.py" --lite -o ./dist/kosif-superpowers.skill

The skill ZIP includes the KOSIF SVG engine, executable motion director, optional provider project scaffolds, bundled portable HTML renderer and verification scripts. The GitHub CI build also uploads a installable skill artifact on successful checks. It still requires matching runtime dependencies, installed securely with the user's authorization.
