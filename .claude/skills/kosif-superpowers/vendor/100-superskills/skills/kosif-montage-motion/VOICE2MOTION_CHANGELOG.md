# KOSIF Voice2Motion v5.1 — source-based enhancement

## Baseline
Existing v5 uploaded package: `verse` (kinetic texts from audio), `direct` (visuals in talking footage), `kmotion` CLI. `ultra-motion-montage.zip`: beat detector, smart montage, QA; Omni handoff: video/audio/cinema director skill descriptions.

## New capability
- New `audio2motion` CLI route in `kmotion.py`.
- Deterministic Python/Pillow scene renderer with structured voice cue sheet.
- Semantic visual routes: weather, traffic, support, refund, generic.
- RMS voice-reactive motion, speech captions, time progress bar, original-audio mux.
- Timings in demo estimated from speech and silence. No ASR/forced alignment claimed.
- `--transcript` approximate fallback + `--plan-only` editable JSON.
- Seven regression unit tests, plus verified 28.84s 720×1280 @ 30 fps sample render.

## Scope/limitations
This is a locally installable code integration, not a live ChatGPT plugin update. Voice and screen motion are generated offline using original vector art. It does not create 3D character performances from speech automatically.
The shipped merged source excludes original font binaries; install system fonts or merge into an existing local copy for legacy typography assets.
