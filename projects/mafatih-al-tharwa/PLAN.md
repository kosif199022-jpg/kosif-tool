# PLAN.md — مفاتيح الثروة (Keys to Wealth)

> Style: `kinetic-arabic` · Deliverable: 9:16 · 1080x1920 · 30 fps · 640.29 s (19,209 frames) · master clock = the supplied voice note

## 1. Summary

| Item | Value |
|---|---|
| One-line concept | An archival-documentary motion film: the story Coach Abu Faisal tells (Carnegie → Napoleon Hill → Bob Proctor → Thinking Into Results) told with public-domain 1928–1956 footage, gold kinetic Arabic captions and ~43 hero motion graphics fired on spoken key words. |
| Source material | User voice note (Gulf Arabic, 10:40, mono AAC 44.1 kHz); 7 public-domain archive.org films (see RIGHTS.md) |
| Master clock | Supplied audio; word timings from faster-whisper large-v3-turbo, hand-corrected (words.json) |
| Playbooks | kinetic-type, arabic-typography, audio-sync, render-pipeline |
| Stack | ffmpeg b-roll track (src/build_broll.py) + deterministic HTML/SVG/Canvas overlay with `window.__kosif.seek(t)` (src/overlay.html, overlay.js) composited frame-by-frame by Playwright + ffmpeg (src/render_film.cjs) |

## 2. Layers (every frame)

1. **B-roll** — 167 graded clips (mean 3.8 s) cut on caption boundaries; each has a push-in, pull-out or pan. Sepia-gold monochrome, film grain, vignette. Sharp 960×720 film card over a blurred copy.
2. **Scrim** — darkens the card only while a hero graphic is on (footage keeps ghosting through).
3. **Hero graphics** — table below.
4. **Captions** — phrase-level (≤ 6 words, break on pauses > 0.45 s), each word lights gold 60 ms before its spoken onset, key words (names, numbers, debt/goal…) keep a gold underline that sweeps right→left across the word's duration.
5. **Chrome** — key logo + chapter label (wipes in on each chapter), chapter progress bar, archive tag, drifting gold dust, a soft light flash on every b-roll cut.

## 3. Chapters

| # | Start (s) | Chapter |
|---|---|---|
| 00 | 0.0 | Intro |
| 01 | 14.5 | Andrew Carnegie |
| 02 | 56.8 | Napoleon Hill |
| 03 | 117.8 | Bob Proctor |
| 04 | 226.7 | The goal |
| 05 | 266.2 | Debt or goal? |
| 06 | 336.0 | Starting from zero |
| 07 | 402.2 | The hidden lesson |
| 08 | 473.6 | Nightingale-Conant |
| 09 | 548.8 | Thinking Into Results |
| 10 | 606.6 | Keys to Wealth |

## 4. Hero motion graphics (times are from words.json)

| # | Start (s) | End (s) | Type | Beat | Motion |
|---|---|---|---|---|---|
| 1 | 3.90 | 14.45 | hero | Title | custom SVG draw-on / counters / 3D |
| 2 | 19.90 | 28.20 | nameCard | Andrew Carnegie — أندرو كارنيجي | gold bar grows, name wipes right→left, subtitle rises, chips pop |
| 3 | 28.60 | 41.00 | quote | wisdom dies with them | ornament draws, lines mask-wipe right→left on their words |
| 4 | 48.90 | 55.90 | quote | give me a young man | ornament draws, lines mask-wipe right→left on their words |
| 5 | 58.30 | 66.50 | nameCard | Napoleon Hill — نابليون هيل | gold bar grows, name wipes right→left, subtitle rises, chips pop |
| 6 | 69.30 | 86.20 | hero | 500 millionaires | custom SVG draw-on / counters / 3D |
| 7 | 88.70 | 95.40 | hero | how they act, think, talk | custom SVG draw-on / counters / 3D |
| 8 | 97.50 | 104.85 | hero | massive information → one book | custom SVG draw-on / counters / 3D |
| 9 | 104.85 | 116.60 | hero | Think and Grow Rich, 100 million copies | custom SVG draw-on / counters / 3D |
| 10 | 124.90 | 131.60 | nameCard | Bob Proctor & Ray Stanford — بوب بروكتر | gold bar grows, name wipes right→left, subtitle rises, chips pop |
| 11 | 131.70 | 137.95 | nameCard | Bob Proctor & Ray Stanford — راي ستانفورد | gold bar grows, name wipes right→left, subtitle rises, chips pop |
| 12 | 142.10 | 147.70 | hero | Bob Proctor & Ray Stanford | custom SVG draw-on / counters / 3D |
| 13 | 148.10 | 153.20 | quote | take this book | ornament draws, lines mask-wipe right→left on their words |
| 14 | 157.90 | 161.00 | hero | impossible | custom SVG draw-on / counters / 3D |
| 15 | 161.00 | 176.30 | hero | two years, every day | custom SVG draw-on / counters / 3D |
| 16 | 186.00 | 197.90 | hero | debt 6,000 vs income 4,000 | custom SVG draw-on / counters / 3D |
| 17 | 201.90 | 215.00 | hero | the miracle is in your hands | custom SVG draw-on / counters / 3D |
| 18 | 216.70 | 224.70 | quote | his deep belief in me | ornament draws, lines mask-wipe right→left on their words |
| 19 | 233.80 | 238.95 | hero | set a goal | custom SVG draw-on / counters / 3D |
| 20 | 238.95 | 244.20 | hero | five hours a day | custom SVG draw-on / counters / 3D |
| 21 | 244.20 | 252.50 | hero | Earl Nightingale's record, in the car | custom SVG draw-on / counters / 3D |
| 22 | 254.50 | 262.50 | hero | goal: $25,000 | custom SVG draw-on / counters / 3D |
| 23 | 266.20 | 336.05 | hero | debt vs goal | custom SVG draw-on / counters / 3D |
| 24 | 344.90 | 352.10 | hero | the cleaning sign | custom SVG draw-on / counters / 3D |
| 25 | 356.80 | 363.40 | quote | decided to work in cleaning / be patient | ornament draws, lines mask-wipe right→left on their words |
| 26 | 366.00 | 371.40 | quote | decided to work in cleaning / be patient | ornament draws, lines mask-wipe right→left on their words |
| 27 | 373.50 | 380.40 | hero | mop and tools | custom SVG draw-on / counters / 3D |
| 28 | 384.20 | 401.70 | hero | the company grows: staff, 5 countries, 5 years, $1M a year | custom SVG draw-on / counters / 3D |
| 29 | 407.20 | 416.50 | equation | how did you become a millionaire / the equation | pills pop in sequence, result wipes or stamps |
| 30 | 419.50 | 433.40 | equation | how did you become a millionaire / the equation | pills pop in sequence, result wipes or stamps |
| 31 | 433.30 | 446.20 | hero | the hidden lesson | custom SVG draw-on / counters / 3D |
| 32 | 451.60 | 472.70 | hero | most rich people vs Bob | custom SVG draw-on / counters / 3D |
| 33 | 481.90 | 490.70 | nameCard | Nightingale-Conant — نايتنجيل وكونانت | gold bar grows, name wipes right→left, subtitle rises, chips pop |
| 34 | 503.00 | 511.40 | hero | not the salary — to learn | custom SVG draw-on / counters / 3D |
| 35 | 512.40 | 516.60 | hero | sales rise | custom SVG draw-on / counters / 3D |
| 36 | 520.90 | 526.40 | hero | the secret: a key turning | custom SVG draw-on / counters / 3D |
| 37 | 526.40 | 536.10 | hero | You Were Born Rich | custom SVG draw-on / counters / 3D |
| 38 | 549.80 | 559.30 | hero | timeline 1981 — 2002 | custom SVG draw-on / counters / 3D |
| 39 | 564.90 | 570.60 | hero | a new program for individuals and companies | custom SVG draw-on / counters / 3D |
| 40 | 571.10 | 601.60 | hero | Thinking Into Results — 12 lessons | custom SVG draw-on / counters / 3D |
| 41 | 606.60 | 616.60 | nameCard | Coach Abu Faisal — كوتش أبو فيصل | gold bar grows, name wipes right→left, subtitle rises, chips pop |
| 42 | 619.10 | 633.10 | hero | simple, Sharia-compliant, Arab mindset | custom SVG draw-on / counters / 3D |
| 43 | 633.10 | 640.29 | hero | end card | custom SVG draw-on / counters / 3D |

Between heroes the archival card plays clean with captions, so the film alternates footage and graphics roughly every 5–15 s.

## 5. Transitions used

- Hard cuts on b-roll at caption/phrase boundaries, each with a 0.3 s gold light flash.
- Hero in/out: 0.3 s ease-out fade + element-level wipes (right→left), pops (back easing), rises and stamps (scale 2.4→1 + damped shake).
- Chapter label: right→left mask wipe.

## 6. Render plan

1. `python3 src/prep_words.py <work> .` → words.json + src/captions.js
2. `python3 src/build_broll.py footage shots.json src/captions.js build` → build/broll.mp4 (19,209 frames) + cuts.json/cuts.js
3. `node src/render_film.cjs --broll build/broll.mp4 --stills 6.8,24,72 --out stills` (preview)
4. 4 parallel `--from/--to` chunks → concat → mux the original AAC stream untouched → `tools/verify_video.py`.
