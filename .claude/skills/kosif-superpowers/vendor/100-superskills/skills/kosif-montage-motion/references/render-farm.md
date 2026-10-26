# Faster renders without losing quality

## On one PC (measured 2026-10-09: i7-1165G7, 4 cores, 7.8 GB, Iris Xe; the 5 s 3D boat at 1920×1080)
| mode | time | use |
|---|---|---|
| `kmotion preview` (half size, 15 fps, JPEG) | 28 s | every review round |
| `render --blur 1 --capture jpeg` | 87 s | quick full-size check (SSIM 0.990 vs PNG) |
| `render --blur 1` (PNG) | 117 s | — |
| `kmotion final --blur 4` (PNG, slow/CRF 16, poster, gate) | 173 s render, 186 s total | the one delivery render |
Most of the time is the browser drawing and capturing frames, not encoding: x264 slow vs medium cost nothing
measurable, Quick Sync would save little. The browsers in parallel are capped by free memory (3–4 here): close
Chrome and other heavy apps, plug the charger in, Windows power mode "Best performance".

## Across machines: `scripts/shard.py`
`plan` gives frame ranges; `render --shard i --of N` draws one range to a segment at the final settings; `join`
concatenates the segments losslessly (same encoder settings), adds the page's sound, bakes the poster and runs the
gate. The page is deterministic, so a joined film equals a single-machine render.

## GitHub Actions (repository kosif199022-jpg/kosif-render-lab, workflow `kosif-render`)
Run: Actions → kosif-render → Run workflow (project, shards, blur), or
`gh workflow run kosif-render.yml --repo kosif199022-jpg/kosif-render-lab -f project=night_boat -f shards=6 -f blur=4`.
The film, its poster and per-shard timings come back as the `film` artifact; the run summary has the table.
Facts to weigh (GitHub's terms as of 2026 — verify at use): hosted runners have no GPU, so WebGL scenes draw in
software; each runner spends time installing ffmpeg and Chromium before drawing; a private repository uses the
account's included minutes and stops when billing fails (first attempt on 2026-10-09: "recent account payments have
failed or your spending limit needs to be increased"); a public repository runs free but its files are public.
Expect gains for long films (many frames to share out), not for 5–10 s ones, and measure before relying on it.
