# KOSIF Cinema Pro — verified multi-pass editing

**Feature branch:** `feat/cinematic-pro-conductor-20261031` · **Pull request:** #188.

This package integrates existing KOSIF Montage Pro stages; it does not independently call every catalogued AI skill or promise film-like results without footage, visual review and a real renderer.

## Execution

From the repository root:

```sh
S=.claude/skills/kosif-superpowers/scripts
python3 "$S/cinematic_pro_conductor.py" doctor
python3 "$S/cinematic_pro_conductor.py" plan --kind video --recipe cinematic-reel
python3 "$S/cinematic_pro_conductor.py" run input.mp4 --job out/cinema/reel --recipe cinematic-reel --style 30
python3 "$S/cinematic_pro_conductor.py" run voice.wav --job out/cinema/audio --recipe cinematic-audio
```

Recipes:

- `single` (default): one supported Montage Pro option with verified video deliverable.
- `cinematic-reel` (video): measured highlight selection → 9:16 reframe → film-look colour grading. The video from the previous stage is the actual input to the next stage.
- `cinematic-audio` (audio): cue-driven kinetic motion/HTML render → film look. Requires ffmpeg, node, and installed working Chromium/Playwright renderer.
- `--transcribe-local` is optional and uses only a previously cached local transcription model; it never downloads one.

Every pass records source and output hashes/verification evidence in `cinema_pro_receipt.json`, and a failed pass stops the remaining work. `verified` means technical MP4 checks passed; it is **not** a rating for visual beauty or word alignment. Human QA is still required for cuts, Arabic text, audio timing, exposure, and relevance.

## Validation

- The 2026-10-31 isolated branch CI test pass for multi-pass contracts: 8 tests succeeded using mocks and synthetic paths.
- The skill generator performed 14 catalog/structure checks with no errors, and 110/110 routing evaluations passed. The remaining legacy proof warning covers motion power records whose verification artifacts are not in this copy.
- Rendering with a real user's video and independent frame-by-frame aesthetic review **has not been performed** in this update.
- The free Render media gateway remains an independent service and cannot be assumed to download YouTube videos blocked by platform anti-bot checks.

## Next production acceptance

With authorized local footage and soundtrack, confirm actual render in MP4/H.264, 1080×1920 / 30 FPS for cinematic-reel, video stream and soundtrack consistency, expected duration, original-source checksum unchanged, no frozen/black shots, coherent story and manual viewing of transition boundaries. No paid calls or unattended downloads.
