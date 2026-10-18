# KOSIF Creative Intelligence — executable sound-to-motion capability

## What works today

KOSIF's original standard-library audio adapter (`scripts/audio_cue_mapper.py`) reads **16-bit uncompressed PCM WAV** mono/stereo, 8–192 kHz and 0.1–120 s, and measures real **RMS energy envelopes** and **rising-energy transient candidates** at approximately 50 ms granularity. Optional `--aligned-words` imports existing WhisperX/KOSIF word timings, validates finite numbers and nonoverlap, and does **not** fabricate timestamps, transcriptions or emotion.

`scripts/creative_reasoning_bridge.py` converts the cues and words into **an editable storyboard in the existing KOSIF motion-director schema**, three comparable style scores with decision explanations, an evidence record and a consistency-checked scene timeline. Its SVG scenes contain **timed text, gradually drawn path, an articulated character, camera zoom and motion**. The scoring is **a declared deterministic design heuristic**, NOT evidence that Claude understood the lyrics or a trained aesthetic assessor.

This is genuine executable transfer into the skill, without copying any upstream source; it uses native Python and the existing KOSIF SVG renderer. The following optional upstream tools are candidates for distinct licensed adapters (not bundled): librosa/Essentia for richer spectral/tempo analysis; WhisperX for timed speech; CLAP/Qwen for semantic audio inference; Remotion for React MP4 composition; DSPy and DeepEval for measurable agent evaluation.

## Reproducible commands

From `kosif-tool` repository root:

```bash
SKILL_DIR=.claude/skills/kosif-superpowers
python3 "$SKILL_DIR/scripts/audio_cue_mapper.py" ./voice.wav --aligned-words ./words.json --out ./cues.json
python3 "$SKILL_DIR/scripts/creative_reasoning_bridge.py" ./cues.json --style auto --out ./scene.json --report ./decision.json
python3 "$SKILL_DIR/scripts/motion_director.py" compile ./scene.json --out ./film.html
python3 "$SKILL_DIR/scripts/motion_director.py" render ./film.html --out ./film.mp4 --audio ./voice.wav
python3 tools/verify_video.py ./film.mp4 --aspect 9:16 --fps 30 --duration 9 --audio ./voice.wav
```

`words.json` may be `{ "words": [{"text":"مرحبا", "start":0.5, "end":1.1}] }` or WhisperX `{"segments":[{"words":[{"word":"مرحبا","start":0.5,"end":1.1}]}]}`; times must be source-audio seconds. The `--aligned-words` option is optional. If the input speech is not a WAV, transcode to the supported PCM format **separately** while preserving the original audio for final export; alignment remains anchored to original playback timeline. The actual audio track is never modified by either KOSIF bridge.

For a landscape storyboard add `--landscape`. To force visual style choose `--style doodle`, `--style kinetic` or `--style cinematic`; with `--style auto`, the skill picks based on its published deterministic heuristic, not a guaranteed musical emotional analysis.

## Acceptance tests

```bash
python3 -m unittest discover -s "$SKILL_DIR/evals" -p test_creative_intelligence.py -v
python3 -m unittest discover -s "$SKILL_DIR/evals" -p 'test_*.py' -q
python3 "$SKILL_DIR/scripts/check_skill.py" --json
```

The storyboard validator checks ordered scenes, word boundaries, permissible Arabic text, safe SVG path syntax, and serializable timestamps. Successful tests mean the **source generation path** works in that environment. Rendering an MP4 requires Node.js, Playwright/Chromium and FFmpeg; its audio track, duration and visual content still need independent verification. Original catalog numbers remain unchanged until a new power is evaluated and recorded with a valid proof; this add-on's tests and real artifacts are separate evidence.

## Decision integrity and constraints

- Audio envelope/transients are **not** guaranteed tempo or downbeats; `bpm: null`, `verified_beats: false` until robust upstream analysis and ground-truth testing.
- `emotion: null`: transients cannot verify sadness, hope, or narrative meaning. Claude should interpret lyrics and story using the actual words and user direction, mark uncertainty, and optionally request correction of mistranscribed singing.
- Candidate style ranking is **explainable but subjective**; expose all scores and let a user override.
- Arabic words are kept whole, never split into individual letters. Do not invent alignment or claim ±100 ms without reference measurements.
- Do not upload third-party repository archives or perform bulk copies into the production package by default. License-check each component, scripts, media and model weights separately; do not treat linked licenses as blanket reuse permission.
- If two JSON outputs exist, the CLI declines to overwrite them; retain original materials.