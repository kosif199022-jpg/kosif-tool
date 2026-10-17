# KOSIF Reference Edit Engine — executable source-style-to-timeline transfer

This is an original runnable program inside KOSIF Superpowers, not a list of repositories and not the official Higgsfield Katana engine. The original implementation translates measured **cut timing** from an authorized reference video to an independent editable React/Remotion video project that contains original motion and optionally user-owned replacement footage.

## Workflow

Probe the video with installed FFmpeg/ffprobe first (original source media is never copied):

    SKILL_DIR=.claude/skills/kosif-superpowers
    python3 "$SKILL_DIR/scripts/motion_reference_probe.py" ./my-owned-reference.mp4 --cuts --out ./reference-cuts.json

If an audio recording is available, create a 16-bit PCM WAV copy without modifying the original, and optionally import externally verified WhisperX word timestamps:

    python3 "$SKILL_DIR/scripts/audio_cue_mapper.py" ./voice.wav --aligned-words ./verified-words.json --out ./cues.json

Generate a NEW Remotion project. Audio duration takes precedence as master clock if you pass the cues:

    python3 "$SKILL_DIR/scripts/reference_edit_engine.py" --probe ./reference-cuts.json --cues ./cues.json --fps 30 --out ./new-kosif-reference-project

The generated project is editable, not a fixed demo: edit src/plan.json cuts/phrases/motion fields and src/Video.jsx React scene design. src/Root.jsx declares the video Composition; src/index.jsx registers it. package.json contains the actual Remotion scripts.

### Optional own footage and soundtrack

Create my-assets.json with clip names for each source-detected shot (exactly one clip per shot) and optionally one full-length user-owned audio track. Example for a reference with exactly two shots:

    {"clips":["take1.mp4","take2.mp4"],"audio":"voice.wav"}

Then run:

    python3 "$SKILL_DIR/scripts/reference_edit_engine.py" --probe ./reference-cuts.json --cues ./cues.json --manifest ./my-assets.json --assets-dir ./my-assets --out ./new-remotion-project

Only authorized replacement clips and user audio are copied. Directory traversal, symlinks, missing assets and oversized files are rejected. The reference video itself is NEVER copied or bundled. If no clips are provided, original animated circles/shapes, camera zoom and text are displayed (no static screenshot slideshow).

Inside the generated project, after reviewing Remotion's applicable commercial license and authorizing installation:

    npm install
    npm run studio
    npm run render

These are instructions; KOSIF does not silently download or install dependencies. Running the Python project generator is NOT equivalent to completing an MP4 render. Review media codecs, cuts, Arabic caption layout, audio sync, frame continuity, and actual output with a video tool before claiming film quality.

## Genuine skill capabilities now implemented

| Capability | Original executable | Verification scope |
|---|---|---|
| Source cut timestamps -> frame-exact shot boundaries | scripts/reference_edit_engine.py : plan | Python unit tests |
| Scale reference rhythm to different original-audio clock | plan(probe,cues) | Unit tests |
| Protect word-level subtitles across editing cuts | choose safe frame boundary or fail closed | Unit tests |
| Editable Remotion Composition with actual React sources | creates package.json and src/*.jsx | Generated file inspection tests |
| User-owned footage replacement per shot | safe manifest + asset copy | Safe-path/copy tests |
| Original continuously moving shapes and slow clip camera movement | src/Video.jsx frame-driven progress/zoom | Code generated; browser render unverified |
| Inference/evidence separation | decision-report.json | Unit tests |
| Secure, nonoverwriting project output | create_project | Unit tests |

## Upstream evidence, not bundled third-party code

- Remotion: https://github.com/remotion-dev/remotion — inspected source README; React video composition with Sequence/Composition/OffthreadVideo/Audio; SPECIAL commercial license. No Remotion code is copied into this skill.
- Motion Starter Kit: https://github.com/motalim-ai/motion-starter-kit — user style approval and source-ownership rules, MIT according to README. No gallery assets bundled.
- PySceneDetect: https://github.com/Breakthrough/PySceneDetect — scene and cut detection; existing KOSIF implementation uses ffmpeg heuristics. BSD-3-Clause.
- Higgsfield Skills: https://github.com/higgsfield-ai/skills — independently installable AI skills, MIT; official Katana service/credits not automatically enabled.
- SAM 2 and CoTracker: object masks and tracked points are not yet embedded or exercised; they require model install, media rights and performance measurement.

**Precise boundaries:** Cut timing is extracted from FFmpeg and can be wrong for dissolves. No automatic shot semantics, segmentation, full camera reconstruction, arbitrary effect reconstruction, voice emotion inference, true beat tracking, reference face imitation or cloned transitions. KOSIF rebuilds a new original editable timeline inspired by the measured structure, not the pixels.

## Verification

    python3 -m unittest discover -s "$SKILL_DIR/evals" -p test_reference_edit_engine.py -v
    python3 "$SKILL_DIR/scripts/check_skill.py" --evals

Only after a real machine installs dependencies, runs Remotion Studio, renders MP4, and verifies picture + audio, may the final video be labelled rendered/verified. For commercial use, verify each package, pretrained-model weight and asset license independently.
