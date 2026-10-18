# KOSIF Code Drawing Master — Executable Skills for Claude

KOSIF Superpowers includes original callable tools for actual vector drawing, rather than only listing repositories. It combines an original procedural actor/scene generator, a validated timed storyboard, and a deterministic SVG renderer compatible with the existing KOSIF MP4 pipeline.

## Implemented now

- Humans drawn from 20 articulated SVG parts: face, eyes, nose, mouth, hair, ears, hands, jacket, shirt, trousers, shoes. Three facial expressions (happy, sad, determined).
- Cats from 14 SVG parts: ears, whiskers, paws, tail and facial details.
- Six animated actions: idle, walk, run, wave, point, sit, with named shoulder/knee pivots. These are stylized procedural rigs, NOT motion-captured animations.
- Two procedural environments: street with facades/windows/lamps and park with trees/paths.
- Sequential pen-stroke reveal, tracking of active path with a small pen-tip dot. This is NOT a photorealistic hand.
- Original shape morphing between corresponding polygons (3–64 paired vertices). Flubber-style arbitrary path topology morphing is NOT yet available.
- Camera pan/zoom and precisely seekable video time.
- Exact caption placement from imported WhisperX timestamp JSON. Unaligned or overlapping words fail; speech recognition is NOT part of the script.
- Editable storyboard JSON and self-contained HTML, with optional MP4 export if the full KOSIF renderer/Chromium/FFmpeg stack is present.

## Commands to actually produce drawings

From the kosif-tool repository root:

    SKILL_DIR=.claude/skills/kosif-superpowers
    python3 "$SKILL_DIR/scripts/code_drawing_master.py" --cast human+cat --expression determined --location street --action walk --duration 9 --fps 30 --out ./storyboard.json --html ./storyboard.html
    python3 "$SKILL_DIR/scripts/code_drawing_master.py" --cast cat --expression happy --location park --action run --out ./cat-park.json --html ./cat-park.html

To attach real aligned voice words from WhisperX exported JSON with segments[].words, or a JSON document with words[].text/start/end:

    python3 "$SKILL_DIR/scripts/code_drawing_master.py" --cast human --action wave --words-json ./aligned-words.json --out ./talk.json --html ./talk.html

The script does not invent words or timestamps, and will not overwrite existing files. Review the resulting HTML source, then render only with the full repository and a configured host:

    python3 "$SKILL_DIR/scripts/motion_director.py" render ./talk.html --out ./talk.mp4 --audio ./voice.wav
    python3 tools/verify_video.py ./talk.mp4 --aspect 9:16 --fps 30 --duration 9 --audio ./voice.wav

The MP4 is NOT proven until the render and audiovisual verification run successfully. Keep original audio as the master clock and preserve Arabic word boundaries.

## Six learning/production stages

1. Geometry: lines, circles, cubic curves, safe coordinates, color, fill and stroke, SVG path lengths.
2. Portrait characters: ordered head, eyes, nose, mouth, eyebrows, hair, torso, arms, legs, clothes, facial emotion.
3. Environment: urban street, park, props, depth and motion composition; maintain consistent identities.
4. Hand drawing: staged paths + tracked pen-tip geometry; no simulated photo hand claim.
5. Acting: true time indexed walk/run/wave/point/sit, eased joint rotation and pan/zoom. For complex 2D/3D/IK, inspect and use an appropriate licensed external rig engine.
6. Audio and video: externally verified word timestamps -> storyboard -> seek(t) -> frames -> MP4 -> audio/video QA.

## Verified GitHub project references and precise capability status

| GitHub | Lessons integrated in original KOSIF code | Status of upstream runtime |
|---|---|---|
| [Theatre.js](https://github.com/theatre-js/theatre) | Frame-indexed movement/keyframes | External; @theatre/core Apache-2.0, Studio AGPL-3.0 |
| [Flubber](https://github.com/veltman/flubber) | Smooth polygon morphing | Original matched-vertex subset only; upstream MIT |
| [WhisperX](https://github.com/m-bain/whisperX) | Word timestamp JSON | Importer included, ASR unbundled; BSD-2-Clause |
| [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | Reference scene boundaries | Existing ffmpeg heuristic probe, not PySceneDetect |
| [Animated Drawings](https://github.com/facebookresearch/AnimatedDrawings) | Articulated 2D figures | Original simplified actor rigs; upstream archived 2025, MIT |
| [SVG.js](https://github.com/svgdotjs/svg.js) | Editable vector scene model | Original SVG engine bundled; SVG.js not installed |
| [Konva](https://github.com/konvajs/konva) | Editable Canvas scene graph | UI editor not implemented |
| [Motionity](https://github.com/alyssaxuu/motionity) | Timeline, keyframes and layers | UI editor not bundled |
| [Natron](https://github.com/NatronGitHub/Natron) | Compositing graph | Reference only; GPL-2.0 |
| [Editly](https://github.com/mifi/editly) | Code-driven MP4 | Existing KOSIF renderer, Editly not installed |

No third-party engine source has been copied into the new drawing code. The two user-provided 100-repository tables are learning leads, not an auditable list of 200 independently verified repo URLs; many entries have ambiguous names, and some repeat. Locate exact repo owner, inspect actual code/docs, verify its component license, implement a specific original adapter, and test before upgrading its status. Reading examples does not modify Claude's trained weights.

## Evidence and limitations

    python3 -m unittest discover -s "$SKILL_DIR/evals" -p 'test_code_drawing_master.py' -v
    node --test "$SKILL_DIR/evals/test_code_drawing_engine.mjs"
    python3 "$SKILL_DIR/scripts/check_skill.py" --evals

Tests cover actual actor source generation, injected SVG/coordinate rejection, external word timestamp integrity, actor drawing progression, per-joint movement, shape morphing, and file overwrite protections.

Not implemented yet: photorealistic drawing hand, full character turnaround perspectives, IK/collision solver, lip sync, real-time source-video object motion tracking and visual-fidelity scoring, full multi-track timeline editor. These require separate measured integrations and should never be misrepresented as working.
