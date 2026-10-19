# KOSIF_TASK_QA.md — question register (condensed)

Confidence: V = verified by a command/output, S = strongly supported, A = assumption.

| ID | Category | Question | Answer | Conf. | Decision |
|---|---|---|---|---|---|
| Q-001 | Objective | What does the user want? | A motion video of the attached photo, made to feel like live footage with camera moves, synced to the attached song, with well-styled captions. | V (request) | Single-photo 2.5D film + karaoke lyrics |
| Q-002 | Objective | "Caption" = on-screen lyrics or post text? | Both are plausible. | A | On-screen lyric captions + a post caption in CAPTION.md |
| Q-003 | Resources | What audio is supplied? | 196.82 s MP3 with embedded lyrics and section markers. | V (ffprobe) | Lyrics used verbatim; film = full song |
| Q-004 | Resources | Is there a reference video? | No. | V | Original treatment; nothing claimed as watched |
| Q-005 | Requirements | Should other footage be downloaded? | User allowed it, but asked that *their* photo be what appears. Stock footage of other people/places would contradict that. | S | No stock footage; all motion from the photo + coded graphics |
| Q-006 | Capability | Speech timing tool available? | faster-whisper installed and run (large-v3-turbo). | V | Transcribe |
| Q-007 | Quality | Is Whisper word timing within 100 ms? | No: MMS forced alignment on the Demucs vocal stem shows Whisper line starts 0.3–0.5 s early (word median 0.18 s). | V | Use forced-aligned times; Whisper only as fallback (6/185 words) |
| Q-008 | Capability | Can the people be separated from the background? | isnet missed the white thobe; BiRefNet-portrait cut both men cleanly. | V (visual check) | BiRefNet mask |
| Q-009 | Quality | Will close-ups at 2–3× be soft? | Source is 941 px wide. | V | EDSR ×2 super-resolution |
| Q-010 | Reliability | Does parallax reveal holes behind the people? | Yes: first build showed a light head-shaped halo. | V (frames) | Joint people+flag inpaint, sky fill per row, flags extended behind heads; re-checked frames |
| Q-011 | Creativity | How do we make a still look live? | Wind through the flags, breathing/drift, rack focus, whip pans, dust, light leaks, grade per section, beat punches. | S | Implemented |
| Q-012 | Arabic | Do the captions keep letters joined? | Whole-word spans, R→L clip wipes, no letter-spacing; checked in rendered frames. | V | — |
| Q-013 | Audio | Normalise to −14 LUFS? | Conflicts with "preserve the user's audio untouched". | S | Audio not normalised; loudness measured and reported |
| Q-014 | Performance | Render time? | PNG capture took ~900 ms/frame; `optimizeForSpeed` cut it to ~150 ms (still lossless). | V | Patched tools/render_html.cjs; 3 parallel chunks |
| Q-015 | Licensing | Are all assets cleared? | User's photo/song; OFL fonts; original code-drawn graphics. | V | ASSETS.md |
| Q-016 | Content | Any sensitive imagery? | The Saudi flag carries the shahada; it is shown as in the photo and only moved by gentle wind. | S | Lyric captions sit in the lower third, away from the flags |
