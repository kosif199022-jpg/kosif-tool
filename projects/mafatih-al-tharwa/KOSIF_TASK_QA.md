# KOSIF_TASK_QA.md — Keys to Wealth motion film

Confidence: **V** verified · **S** strongly supported · **A** assumption. Status: R resolved · T requires testing · U requires user input.

| ID | Category | Question | Answer | Evidence | Conf. | Action | Status |
|---|---|---|---|---|---|---|---|
| Q-001 | Objective | What does the user want? | A full motion-graphics video edited to their voice note, with precise sync, using any footage needed. | Request text | V | Build a complete film of the whole 10:40 audio | R |
| Q-002 | Objective | What is the audio? | 640.29 s Gulf-Arabic monologue by "Coach Abu Faisal" introducing the "مفاتيح الثروة" programme (Carnegie → Hill → Proctor → Thinking Into Results). | Full transcript | V | Story-driven chapters | R |
| Q-003 | Requirements | Which aspect ratio? | Not stated. Chose 9:16 1080×1920 (KOSIF default; voice note suggests phone audience). | AGENTS.md / style SKILL | A | Layout for 9:16; 16:9 needs a relayout | U |
| Q-004 | Requirements | Must the audio stay untouched? | Yes (CLAUDE.md). Master muxes the original AAC stream with `-c:a copy`. | CLAUDE.md | V | Separate optional −14 LUFS variant only | R |
| Q-005 | Capabilities | Is a transcriber available? | Not installed; faster-whisper 1.2.1 installed in a venv, model large-v3-turbo downloaded from HF. | pip / run log | V | Word timestamps on CPU int8 | R |
| Q-006 | Reliability | Why did the first transcription crash? | PyAV API mismatch (`metadata_errors`). Fixed by decoding WAV with numpy and passing the array. | Traceback | V | Patched transcriber | R |
| Q-007 | Quality | Did VAD drop speech? | Yes: 214.8–224.5 s. Re-transcribed that window without VAD and inserted 10 words. | silencedetect energy; fill.json | V | Captions + hero 18 cover it | R |
| Q-008 | Quality | How accurate is the transcript? | Good timings; ~110 mishearings (names, dialect). Corrected by (time, original text) matching so a wrong key cannot silently edit another line. | Audit table | V | prep_words.py FIX list | R |
| Q-009 | Quality | What happens to timing when a correction changes word count? | Segment span redistributed by character length; segments are 0.5–2 s so error stays small. | Code | S | Key heroes use unmodified word starts | R |
| Q-010 | Sync | What sync tolerance is achieved? | Hero triggers are hard-coded to word starts (0–100 ms lead); caption words light 60 ms early, frame-quantised (±17 ms). | overlay.js times vs words.json | V | — | R |
| Q-011 | Resources | Where can footage legally come from? | archive.org Public Domain items (reachable, licence in metadata). Pexels/Pixabay need API keys; Wikimedia API rate-limited (429). | curl tests | V | Used 7 PD films | R |
| Q-012 | Licensing | Are the chosen films really PD? | archive.org metadata `licenseurl = creativecommons.org/licenses/publicdomain/` for all 7. | metadata API, RIGHTS.md | S | SHA-256 + per-film usage logged | R |
| Q-013 | Licensing | Could intertitles or third-party text leak in? | Shots with intertitles/English cards were excluded by eye from contact sheets; clips never run past their source shot. | Contact sheets; overflow post-pass | V | Check in final contact sheet | R |
| Q-014 | Creative | How to unify 1928–1956 B&W and colour footage? | Desaturate → sepia matrix → contrast/gamma, grain and vignette: one "gold archive" look. | Test frame | V | Applied to all 167 clips | R |
| Q-015 | Creative | 4:3 footage in a 9:16 frame? | Sharp 960×720 film card over a blurred, darkened full-bleed copy; gold frame and corner brackets. | Test frame | V | — | R |
| Q-016 | Creative | How to keep 10 minutes engaging? | Cut every ~3.8 s on phrase boundaries; ~43 hero graphics on key words; chapter labels; gold dust; cut flashes. | PLAN.md | S | — | R |
| Q-017 | Creative | Which beats deserve a hero graphic? | Names, numbers (100 years, 500, 100 M, $6,000/$4,000, $25,000, 5 countries, $1 M, 12 lessons), turning points (miracle, goal, debt vs goal, hidden lesson). | words.json key-word list | S | 43 heroes | R |
| Q-018 | Arabic | Are Arabic letters ever split? | No: whole words/lines are wiped with clip-path; no letter-spacing. | Code review, stills | V | — | R |
| Q-019 | Arabic | Numbers inside Arabic lines? | Rendered in `<bdi>` LTR isolates inside RTL lines; first version had wrong order on "+100 عام", which was fixed and re-checked. | Stills 13.9 s / 115.5 s | V | — | R |
| Q-020 | Arabic | Fonts? | Reem Kufi, Cairo, Amiri: OFL, loaded locally before frame 0 (`__kosifReady`). | fonts/, OFL files | V | No network at render time | R |
| Q-021 | Architecture | Render the footage inside the browser? | No: HTML `<video>` seeking per frame is slow and codec support in Playwright Chromium is uncertain. ffmpeg builds b-roll; the browser renders only a transparent overlay. | Design decision | S | Layered pipeline | R |
| Q-022 | Architecture | How to avoid huge intermediates? | Overlay PNGs are piped straight into ffmpeg's overlay filter per chunk; no frame dumps. | render_film.cjs | V | — | R |
| Q-023 | Performance | How to use 4 CPUs? | 4 frame-range chunks in parallel, each with its own Chromium + ffmpeg; concat with stream copy. | Render logs | V | — | R |
| Q-024 | Determinism | Is each frame a pure function of t? | Yes: seeded RNG, no timers/Date, state recomputed in seek(t) (captions rebuild on index change). | Code | S | Chunks render identically at their boundaries | T |
| Q-025 | Quality | Frame-exact length? | b-roll clips are cut on integer frame boundaries; broll.mp4 = 19,209 frames = round(640.29×30). | ffprobe count | V | — | R |
| Q-026 | Testing | How was layout verified before rendering? | 4 rounds of composited preview stills (56 frames); fixed title overlap, RTL numbers, dot grid, pill overlap, debt-column overflow, banner wrap, missing ✓ glyph. | stills sheets | V | — | R |
| Q-027 | Testing | Final checks? | tools/verify_video.py (streams, duration, fps, frame count, audio match), ffprobe, final contact sheet, sync spot checks. | TEST_REPORT.md | V | — | R |
| Q-028 | Safe areas | Do platform UIs cover content? | Card and captions are inside the 12% top/bottom safe band; the header logo (y≈96–210) and progress bar (y≈1812) are decorative and may be covered by TikTok/Reels UI. | Layout | S | Noted as open issue | R |
| Q-029 | Loudness | Is −14 LUFS met? | Source is −22.4 LUFS. The untouched master keeps that; a separate `-social` file is loudnorm'ed to −14 LUFS. | ebur128 | V | Two deliverables | R |
| Q-030 | Accuracy | Are on-screen facts beyond the speech added? | Avoided. Only spoken facts are shown; book titles are the Arabic titles the speaker uses. | PLAN.md | S | — | R |
| Q-031 | Delivery | What does the user receive? | MP4 master (+ social loudness variant), editable sources (overlay.html/js, build_broll.py, render_film.cjs, prep_words.py), words.json, PLAN/STYLE/RIGHTS/TEST_REPORT. | Project folder | V | — | R |
| Q-032 | Persistence | Will files survive the container? | Only if committed/pushed or downloaded; not pushed without the user's request. | Environment docs | V | Ask the user | U |
