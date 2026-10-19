# مفاتيح الثروة — Keys to Wealth (motion film)

A 10:40 vertical 9:16 (1080×1920, 30 fps, footage full-bleed) archival-documentary motion film edited to Coach Abu Faisal's voice note.

| File | What it is |
|---|---|
| `out/mafatih-al-tharwa_master.mp4` | Master: CRF 18 video, **original voice stream copied untouched** (−22.4 LUFS as recorded) |
| `out/mafatih-al-tharwa_social-14LUFS.mp4` | Share copy: CRF 24 video, voice loudness-normalised to −14 LUFS / −1.5 dBTP for Reels/TikTok/WhatsApp |
| `words.json` | 992 hand-corrected word timings (the sync master) |
| `PLAN.md` · `STYLE.md` · `RIGHTS.md` · `TEST_REPORT.md` · `KOSIF_TASK_QA.md` | Plan, design tokens, footage provenance, measured checks, decision register |
| `src/` | Editable sources (below) · `data/` raw Whisper output, shot list, cut list · `preview/` contact sheets |

## Rebuild / edit

```bash
# 1. transcript → words.json + src/captions.js (edit the FIX list in prep_words.py to change caption text)
python3 src/prep_words.py data .            # expects data/whisper.json and data/fill.json
# 2. re-download footage (archive.org public domain, see RIGHTS.md) into footage/, trim fades, then build the b-roll track
python3 src/scan_shots.py footage data/shots.json data/shot_trims.json
python3 src/build_broll.py footage data/shots.json src/captions.js build && cp build/cuts.js src/ && cp build/cuts.json data/
# 3. preview any frames (edit hero graphics in src/overlay.js — every hero is keyed to word times)
node src/render_film.cjs --broll build/broll.mp4 --stills 6.8,72,189.6 --out stills
# 4. full render in 4 parallel chunks, then concat and mux the voice untouched
node src/render_film.cjs --broll build/broll.mp4 --from 0 --to 4802 --out part0.mp4   # … 4802-9604, 9604-14406, 14406-19209
ffmpeg -f concat -safe 0 -i parts.txt -c copy video.mp4
ffmpeg -i video.mp4 -i voice.m4a -map 0:v -map 1:a -c copy -movflags +faststart master.mp4
python3 ../../tools/verify_video.py master.mp4 --aspect 9:16 --fps 30 --duration 640.29 --audio voice.m4a
```
Open `src/overlay.html?dev&t=72` in a browser to inspect a single overlay frame. Requires Node + Playwright/Chromium + ffmpeg; Python 3 (+ faster-whisper only to re-transcribe).
