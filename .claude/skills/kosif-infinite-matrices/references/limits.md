# Technical limits — read before claiming anything

## What is proven

- Inside the numerical model of recipe KMX-R-0001, the memory field causes the motes to keep drawing the beam's path after the beam stops: removing the coupling (B, identical memory) or the persistence (C) removes most of the effect in 8/8 seeds, and the effect grows monotonically with the coupling gain.
- The rendered scene is deterministic (same t, same pixels), has no page errors, and shows the difference after the beam stops (A vs B ≈ 4% of pixels, motes only; A vs C ≈ 74%).
- The MP4 passes `tools/verify_video.py` for duration, frame count, size, fps and audio presence.

## What is not proven

- Nothing about real glass, photochromic materials or optics.
- No human has rated the look or the meaning yet (EXP-0001 has 0 ratings), so it is not `PRODUCTION_READY`.
- Not globally novel: only checked against the 86 references, the 283 seeds and the ledger.
- The 283 hypothesis seeds are untested and unrendered. EXP-0001 is a new recipe, not one of them.
- The code-brick labels are static inferences (E2). No reference style was reconstructed (E3).
- The MP4's score is quiet (about −25.6 LUFS against the −14 LUFS check in `verify_video.py`); it is a sound-effects bed, not a mastered mix.

## Engine limits (v1)

- One stimulus (figure-eight beam), one structure (Voronoi tiles), one dynamics law (gradient steering). Other mechanisms need new adapters and tests.
- Particles read memory but never write it; feedback is one-directional by design so the A/B/C test stays clean.
- Pure Python: 48×27 grid, 160 particles, 300 frames takes about 2 s per condition; the full experiment (3 conditions × 8 seeds + 5 dose levels) about 30 s. Larger grids scale linearly with cells × frames.
- The scene embeds all frames (≈ 2.5 MB for EXP-0001). Long or large runs need a lower grid, fewer particles, or a streamed format.

## Environment limits

- `--render` needs node + Playwright + Chromium; `--mp4` also needs ffmpeg. `doctor` reports both. `scripts/atlas_render.py` additionally needs Python Playwright, which this cloud image does not have; `tools/render_html.cjs` (node) is used instead.
- REA was installed with `npm install --ignore-scripts rea-agents@6.7.0` in a scratch folder; `rea setup` (which edits the client configuration) was not run, and native providers (Ghidra, Hopper, IDA, JADX, Kuna) are not installed or needed for JavaScript source.
- The extracted archive and REA's raw JSON (≈ 100 MB) stay outside git; rerun the commands in [code-bricks.md](code-bricks.md) to regenerate them.
