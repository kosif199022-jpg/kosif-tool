# KOSIF Character IK — analytic, word-cued two-bone character animation

## Executable verified capability (2026-10-19)

`scripts/character_ik.py` adds **an original two-bone inverse-kinematics arm rig** with deterministic motion start times (from explicitly supplied words.json), integrated with `creative_paint.py` for actual images and animation export.

It DOES NOT reverse engineer or copy Adobe Animate or Paint code. It uses standard analytic geometry, Pillow, and FFmpeg.

### Example usage

From repository root, in PowerShell:

```powershell
$R = '.claude/skills/kosif-superpowers'
python "$R/scripts/character_ik.py" doctor
python "$R/scripts/character_ik.py" render --scene "$R/templates/ik-wave-demo.json" --words "$R/templates/ik-wave-words.json" --time 0.8 --output pose.png
python "$R/scripts/character_ik.py" render --scene "$R/templates/ik-wave-demo.json" --words "$R/templates/ik-wave-words.json" --time 0.8 --output pose.svg
python "$R/scripts/character_ik.py" render --scene "$R/templates/ik-wave-demo.json" --words "$R/templates/ik-wave-words.json" --fps 24 --output wave.mp4
```

Optional `--audio narration.m4a` **only for MP4**: the source audio must already be AAC encoded and match the scene's duration; the encoder copies AAC packets rather than re-encoding, and independently checks data hashes of every audio packet (same coded payload in the input and output). It never edits or stretches narration. Unsupported source codecs are deliberately refused rather than silently transcoded.

### Formats and motion semantics
- `kosif.ik.v1` JSON describes canvas, shoulder point, upper/lower bone length, elbow bend sign and targets.
- First target is an initial stable pose at `time=0`, `travel=0`.
- Subsequent targets trigger at an exact `time` or from the `start` of a selected `word` with optional 1-based `occurrence`. Requires a verified, supplied `words.json` containing word/start/end data; the tool **does not transcribe audio**.
- The pose stays still until each cue. Then the target moves along a smoothstep path of configurable `travel` seconds. Overlapping cues fail validation.
- Analytic IK solves an elbow position with fixed upper/forearm lengths via law of cosines, handling unreachable targets by clamping to nearest reachable radius.
- Exports PNG/SVG at specified `--time`, GIF/MP4 for all frames. MP4 uses H.264 and fixed FPS; GIF may coalesce duplicate visual frames but preserves cumulative duration.
- No existing output overwritten; no executable inputs or arbitrary external code.
- Boundaries: 128..2048 canvas dimensions, 0.1..30 seconds, 600 frames at most, 100 cues, shoulder and limb positions should remain in the viewable canvas.

### Verification
```powershell
python -m unittest discover -s .claude/skills/kosif-superpowers/evals -p test_character_ik.py -v
```
18/18 successful on the user's Windows laptop, including:
- exact limb lengths, bend direction, unreachable targets,
- no early movement before word start and deterministic cue timing,
- malformed input and overlapping cue rejection,
- PNG/SVG/GIF/MP4 exports,
- real H.264 video via FFmpeg,
- AAC packet copy and negative rejection of non-AAC source,
- real CLI invocation.

Demo proof in PRIVATE local directory `KOSIF_RESEARCH_PRIVATE_20261019/ik_character_proof_20261019`:
- `ik_frame.png` (640×640) SHA-256 `d5e853abed3311fe2d47e02c3c19dc367cc57d507ccc7033ca3ce5f8688e7ae0`
- `ik_frame.svg` SHA-256 `a7805c6b41e0c312ca29c0e92bf2f1c60380f2b511afa2d36216a37f95db80c8`
- `ik_wave.mp4` verified by ffprobe as H.264, 640×640, 24 fps, 48 frames SHA-256 `7d3f2730794f38e3be567abb7b2564a1a1a2f902862e1a3527e1e5d43456e4c2`.

### Honest limitations
- This is a single-arm 2D rig; it is NOT a complete humanoid skeletal animator, auto-rigger, 3D IK/FK solver, mocap model or commercial motion editor.
- No auto lip-sync, audio transcription or speaker segmentation. If the words file is wrong, cue timing will be wrong.
- The GIF format merges identical frames; audio is unsupported in GIF.
- MP4 with original audio requires AAC-compatible sources; PCM/WAV is not silently converted. Original audio packet integrity is verified only when `--audio` is used.
- SVG is a static vector pose at a given time, not animated SVG.

### Transfer to Claude Code
Read this document and `templates/ik-wave-demo.json`. Create an original JSON with target positions and, optionally, word cues. Probe dependencies with `doctor`, render 1–2 proof frames, inspect generated images, run tests, then export final MP4. Link to existing `code_drawing_master.py` for richer character paths and `cinematic_film_pipeline.py` for full-film editing.
