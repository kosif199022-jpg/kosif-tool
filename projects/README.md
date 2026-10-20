# Projects / المشاريع

Finished or in-progress films built with this repository. Each folder keeps its editable sources,
plan, word timings and QA notes; rendered media and stock footage stay out of git (see each `.gitignore`).

| Project | What it is | Format | Start here |
|---|---|---|---|
| [mafatih-al-tharwa](mafatih-al-tharwa/README.md) | مفاتيح الثروة — 10:40 archival-documentary motion film edited to a voice note | 9:16 · 1080×1920 · 30 fps | `README.md`, `PLAN.md`, `RIGHTS.md` |
| [egypt-saudi-salute](egypt-saudi-salute/PLAN.md) | Egypt–Saudi salute song film with flag-fill typography | 9:16 | `PLAN.md`, `STYLE.md`, `TEST_REPORT.md` |
| [dua-reels/monday](dua-reels/monday/analysis/TEST_REPORT.md) | دعاء صباح الاثنين — real footage, virtual camera, word-synced Arabic captions (10 shots) | 9:16 · 1080×1920 · 60 fps · 28.1 s | `analysis/TEST_REPORT.md`, `build/shots.json` |
| [dua-reels/tuesday-good-news](dua-reels/tuesday-good-news/analysis/transcript.txt) | دعاء يوم الثلاثاء (البشارة وراحة البال) — 13-shot plan | 9:16 · 1080×1920 · 60 fps · 27.8 s | `analysis/words.json`, `build/shots.json` |
| [dua-reels/tuesday-sunrise](dua-reels/tuesday-sunrise/analysis/transcript.txt) | دعاء صباح الثلاثاء (إشراقة الأمل) — 9-shot plan | 9:16 · 1080×1920 · 60 fps · 28.5 s | `analysis/words.json`, `build/shots.json` |

[PROMPT_TEMPLATE.md](PROMPT_TEMPLATE.md) is the master prompt for a new voice-to-motion film.

## Dua reels pipeline

Each reel folder has the same layout and is run from inside that folder (the scripts use relative paths):

```bash
cd projects/dua-reels/<reel>
python3 build/prep.py [SHOT_ID ...]          # trim, retime and pre-crop each source clip in build/shots.json → build/shot_<id>.mp4
node text/build_overlay.cjs stills 2 9.5     # check the Arabic typography at chosen seconds → text/still_<t>.png
node text/build_overlay.cjs frames           # render every overlay frame (transparent PNG, 60 fps) → build/ov/
python3 build/compose.py stills 2 9.5        # check composited frames → build/still_<t>.png
python3 build/compose.py film out/reel.mp4   # virtual camera + grade + overlay, original audio stream-copied
```

Needs Python with `numpy` and `opencv-python-headless`, Node with Playwright, and ffmpeg. The source
clips (`src` in `build/shots.json`), fonts (`fonts/`), the voice (`audio/original_audio.m4a`) and all
renders are not in git (stock-licence redistribution and size): restore them from the recorded sources,
and keep the supplied voice untouched.
