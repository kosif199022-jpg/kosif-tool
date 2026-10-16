# التزامن مع الكلام والترجمة — Audio sync & captions

> فصل مُجمَّع آليًا من 343 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **325 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 325 powers deduplicated by name from 343 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 23 · 🟢 جاهز 38 · 📦 بأمر تثبيت 143 · 🔑 مفتاح/خدمة 8 · 👁 شوهد في فيديو 32 · 📄 موصوف 73 · 💡 فكرة 8

#### SYNC-01 · صوت إلى موشن حسب المعنى · Voice2Motion semantic scenes · ✅ مُثبت هنا
- **ماذا / what:** Audio + transcript -> Pillow frames: each sentence classified (weather, traffic, support, refund, generic) and drawn as its own animated scene, amplitude-driven, numbers taken from the cue text.
- **كيف / how:** python audio2motion.py ... (kmotion audio2motion); cue sheet or estimate_cues(text, duration) by word weight.
- **أرقام / params:** audio envelope 50 Hz from 8 kHz mono; refuses empty transcripts; never claims ASR timing
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/audio2motion.py` · `kosif-one/tools/kosif-studio/tests/test_audio2motion.py` · `kosif-studio/motion/audio2motion.py:80` · `kosif-studio/motion/audio2motion.py:210`

#### SYNC-02 · محلل السكريبت بالتوقيت · Timestamped script parser · ✅ مُثبت هنا
- **ماذا / what:** Accepts lines like '0–3s: text' (en dash, em dash or hyphen) and assigns words to 8/10 s clips by start time, overriding pace estimates; rejects partial or overlapping stamps.
- **كيف / how:** parseTimestamps(script) regex ^(\d+(\.\d+)?)\s*[–—-]\s*(\d+(\.\d+)?)s?\s*:\s*(.+)$; clip index floor(start/len).
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:67-77,96-97` · `fastify-motion-bro/tests/production-profiles.test.mjs:75-81`

#### SYNC-03 · الريل التلقائي · reel automatic pipeline · ✅ مُثبت هنا
- **ماذا / what:** words → decaption → restore 1080x1920 → voice → music only if none → karaoke → −14 LUFS → gate.
- **كيف / how:** python scripts/kmotion.py reel CLIP.mp4 --out FINAL.mp4 [--transcript X.words.json --no-decaption --credit '@x' --model auto]
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### SYNC-04 · تحويل الصوت لموشن · audio2motion Voice2Motion · ✅ مُثبت هنا
- **ماذا / what:** Voice + cue sheet → 2D semantic scenes per cue kind (weather, traffic, support, refund, generic), reacting to RMS envelope bars, shaped Arabic captions, progress bar, original audio, voice normalised −14 LUFS.
- **كيف / how:** python scripts/kmotion.py audio2motion voice.wav --cues cues.json --out out.mp4 --fps 30 --size 1080x1920 [--keep-level]; audio2motion.py --transcript t.txt --plan-only
- **أرقام / params:** 29.4 s/706 frames in 10 s; estimated timing labelled estimated_from_text_length_NOT_ASR
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### SYNC-05 · إخراج تلقائي لمقطع متكلم كالمونتير · Editor-style auto direction of a talking clip · ✅ مُثبت هنا
- **ماذا / what:** From word timings and face boxes, the planner picks the payoff line (after the refrain), content keywords by end-focus (never fillers, never the unit after a number), one ring motif on a repeated number, chapter words for cuts, and face-safe placements; ASR fixes like 'ما حدش=محدش' are applied.
- **كيف / how:** direct.plan(segs, shots, stress, W, H, dur) → {payoff, keys, motifs, captions, chapters}; direct.apply_fixes(segs, 'wrong=right'); kmotion direct CLIP --name …
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_directors.py:10`

#### SYNC-06 · محاذاة كلمات الأغنية والدعاء وتقسيمها · Lyric/poem/dua alignment and phrasing · ✅ مُثبت هنا
- **ماذا / what:** The true Arabic text with diacritics is aligned onto ASR words (misheard words keep their slot, missed words sit after neighbours), lines are cut before phrase openers, ≤7 words, never ending on a particle, keeping fixed phrases whole; the plan marks the refrain's last return as payoff and one secti…
- **كيف / how:** verse.align(lines, asr); verse.segment(words); verse.plan(lines, levels, dur, W, H, title, n_images) → {lines, payoff, refrain, sections, cards}; kmotion verse AUDIO --name … --title …
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_directors.py:42`

#### SYNC-07 · أنماط الترجمة العربية ASS · Caption styles (ASS) for Arabic · ✅ مُثبت هنا
- **ماذا / what:** Burned karaoke captions in seven named styles; hormozi shows one word per event, boxed uses an opaque box, minimal has no pop.
- **كيف / how:** montage.ass(spec, 1080, 1920, style) for reels (Noto Sans Arabic 74), cinema (Noto Naskh 46), punchy (Noto Kufi 72), tiktok (Kufi 84, ≤4 words, pop 120%/90 ms), hormozi (Kufi 96, 1 word, green), boxed (Sans 66, box &H66000000), minimal (Naskh 54, no pop).
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:170`

#### SYNC-08 · مزج الصوت دون زمن حقيقي · Offline audio mix (OfflineAudioContext) · ✅ مُثبت هنا
- **ماذا / what:** Places each video clip's own sound at its slot on the timeline and the soundtrack from zero, then renders one exact stereo buffer faster than real time.
- **كيف / how:** audioPlan(project) → items {assetId, when, offset, duration, volume}; mixAudio(plan, decode, 48000, OfflineAudioContext) with one gain node per source; decode via fetch(blob URL) + decodeAudioData.
- **أرقام / params:** 48 kHz stereo; soundtrack default 0.6
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/offline.mjs:16` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/offline.mjs:120` · `100-superskills/skills/kosif-montage-motion/tests/studio/offline.test.mjs`

#### SYNC-09 · مقياس الجهارة وتطبيعها في المتصفح · In-browser BS.1770-4 loudness meter and −14 LUFS normaliser · ✅ مُثبت هنا
- **ماذا / what:** Measures integrated loudness with K-weighting and gating and applies one gain so the export lands at −14 LUFS without the sample peak passing −1.5 dBFS (reports when the peak limited it).
- **كيف / how:** measureLoudness(channels, sr): high-shelf (f0 1681.97 Hz, +4 dB, Q 0.7072) + RLB high-pass (38.135 Hz, Q 0.5003), 400 ms blocks every 100 ms, −70 LUFS absolute and −10 LU relative gates; normalizeLoudness(channels, sr, −14, −1.5).
- **أرقام / params:** target −14 LUFS; ceiling −1.5 dBFS sample peak (margin under −1 dBTP); not a true-peak limiter
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/offline.mjs:31` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/offline.mjs:59` · `100-superskills/skills/kosif-montage-motion/tests/studio/offline.test.mjs`

#### SYNC-10 · دمج المشاهد مع الصوت الأصلي بلا تعديل · Concat + untouched original audio mux · ✅ مُثبت هنا
- **ماذا / what:** Joins rendered segments in film order and lays the user's original song underneath without re-editing the source file; clip audio is dropped.
- **كيف / how:** Write concat.txt (file 'scene_XX.mp4'), ffmpeg -f concat -safe 0 -i concat.txt -i song.mp3 -map 0:v:0 -map 1:a:0 -t 48 -c:v copy (or re-encode with ass) -c:a aac -b:a 192k -ar 44100 -af afade=t=in:st=0:d=0.3,afade=t=out:st=46.7:d=1.3 -movflags +faststart; record sha256 of the source audio.
- **أرقام / params:** AAC 192k 44.1 kHz; fade in 0.3 s, fade out 1.3 s; trim 00:00-00:48
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:152-158` · `kosif-one/projects/KOSIF_Motion_Ghorba/tools/render_ghorba_preview.py:150-162` · `kosif-one/projects/KOSIF_Motion_Ghorba/tools/render_ghorba_preview.py:180`

#### SYNC-11 · تحليل الصوت إلى قنوات · Audio analysis channels + tape clock + magma spectrogram · ✅ مُثبت هنا
- **ماذا / what:** Per-frame rms, bass/mid/high, onset strength, kicks, onsets, silence, centroid, pitch dive/rise, playback speed and a tape clock; plus spectrogram.png and spectrum_height.png.
- **كيف / how:** python motion.py channels TRACK.wav [--fps 30] [--bpm] [--out ch.json]; read with MOTION.channels in the page.
- **أرقام / params:** nfft 4096 Hann; hop sr/fps
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/qa.py:1` · `kosif-one/tools/kosif-studio/motion/references/x-trend-2026.md`

#### SYNC-12 · ترجمة صفحات وكاريوكي · TikTok-style caption pages + SRT/VTT/ASS karaoke · ✅ مُثبت هنا
- **ماذا / what:** Turns Whisper word timestamps (or SRT) into ~1200 ms pages, writes JSON, SRT, VTT and ASS karaoke, preserves leading spaces, RTL flag.
- **كيف / how:** python captions_pages.py words.json --page-ms 1200 --max-chars 42 --rtl --out captions
- **أرقام / params:** 42 chars/line, 2 lines, 1-7 s/page
- **الدليل / proof:** `100-superskills/skills/audio-reactive-captions-studio/scripts/captions_pages.py:95`

#### SYNC-13 · ترجمة كاريوكي كلمة بكلمة · Karaoke word captions (ASS) · ✅ مُثبت هنا
- **ماذا / what:** Burned captions where the spoken word changes colour and pops; one ASS event per word so Arabic shapes and orders correctly; at most 6 words on screen.
- **كيف / how:** python montage.py captions VIDEO --spec caps.json [--style reels|cinema|punchy]; also used by cut/voicecut/reel
- **أرقام / params:** highlight \1c + \fscx112\fscy112 → 100 % in 120 ms; max_words 6; Encoding −1 (auto paragraph direction); WrapStyle 2; margins 6 % W; sizes scale with the short side
- **الدليل / proof:** `kosif-studio/motion/montage.py:353` · `kosif-studio/motion/montage.py:381` · `kosif-studio/tests/test_studio.py:765`

#### SYNC-14 · توقيت الكلمات حسب الطول · Word timing by length · ✅ مُثبت هنا
- **ماذا / what:** When a caption line has no word times, its span is shared among words by letter count plus a constant.
- **كيف / how:** montage.word_times
- **أرقام / params:** weight = len(word) + 2
- **الدليل / proof:** `kosif-studio/motion/montage.py:341` · `kosif-studio/tests/test_studio.py:765`

#### SYNC-15 · تصحيح النص مع حفظ التوقيت · Transcript fixes that keep timing · ✅ مُثبت هنا
- **ماذا / what:** Replaces misheard phrases while spreading the target words over the original span.
- **كيف / how:** --fix "ما حدش=محدش;بتعودش ضايع=متقعدش تضيّع" (direct, verse)
- **الدليل / proof:** `kosif-studio/motion/direct.py:205` · `kosif-studio/tests/test_studio.py:910`

#### SYNC-16 · كتابة ملفات النص · Transcript writers (words.json / SRT / captions.json) · ✅ مُثبت هنا
- **ماذا / what:** Writes the timed words, an SRT with BOM for players, and a captions spec the montage/captions tools read.
- **كيف / how:** transcribe.write_all(segs, base)
- **أرقام / params:** SRT UTF-8-sig HH:MM:SS,mmm
- **الدليل / proof:** `kosif-studio/motion/transcribe.py:119` · `kosif-studio/tests/test_studio.py:882`

#### SYNC-17 · محاذاة النص الصحيح على التفريغ · True-text alignment onto ASR · ✅ مُثبت هنا
- **ماذا / what:** Puts the real lyrics/poem/dua words on recognised word times: equal or one-to-one blocks inherit times, uneven replacements share the span by length, missed words are spread between timed neighbours.
- **كيف / how:** verse.align via difflib.SequenceMatcher on normalised words
- **أرقام / params:** unmatched fill step ≥0.05 s; min word 0.05 s
- **الدليل / proof:** `kosif-studio/motion/verse.py:83` · `kosif-studio/tests/test_studio.py:943`

#### SYNC-18 · ترجمة متزامنة بالكلمة (كاريوكي) · Word-level karaoke captions (canvas) · ✅ مُثبت هنا
- **ماذا / what:** Phrases split at pauses >0.45 s; whole phrase is shown, current word becomes a teal pill with dark text and an outBack scale pop 0.96->1.08, past words turn white, future words muted.
- **كيف / how:** phrases(words,0.45); show from start-0.15 to end+0.5 with window01 fade 0.15/0.3; pop over 140 ms
- **أرقام / params:** 64 px 700, pill padding 6x18 radius 22, on bg #7ee8d2 text #0b1020, done #f3f7ff, upcoming #9fb0cc; bottom 210 px
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:181` · `kosif-tool/starters/html-canvas/timeline.js:82` · `kosif-tool/starters/html-canvas/index.html:40`

#### SYNC-19 · ملف الكلمات كمتغير JS · words.js / KOSIF_WORDS global · ✅ مُثبت هنا
- **ماذا / what:** Word timings as window.KOSIF_WORDS so the page works from file:// without fetch; generated from words.json.
- **كيف / how:** python3 tools/words_convert.py words.json words.js
- **الدليل / proof:** `kosif-tool/starters/html-canvas/words.js`

#### SYNC-20 · مخطط توقيت الكلمات · words.json master timing schema (kosif-words/1) · ✅ مُثبت هنا
- **ماذا / what:** Timing file with word/start/end seconds plus optional emphasis:true and scene index; carries language, direction, audio, sample_rate, duration_s, text.
- **كيف / how:** templates/words.example.json copied by scaffold as words.json
- **أرقام / params:** sample 48000 Hz, 9 words, 4.2 s
- **الدليل / proof:** `kosif-tool/templates/words.example.json`

#### SYNC-21 · تحويل الترجمات والتفريغ إلى توقيت كلمات · Subtitle/transcript -> words.json converter · ✅ مُثبت هنا
- **ماذا / what:** Converts SRT/VTT cues (words spread proportional to letter count), Whisper JSON (segments.words or segment text), flat lists, {words:[]} and CSV/TSV into sorted, non-overlapping word timings; .js destination emits window.KOSIF_WORDS.
- **كيف / how:** python3 tools/words_convert.py in.srt out.json [--format srt|vtt|json|csv|tsv] [--offset -0.08] [--min-gap 0.02]
- **أرقام / params:** strips <tags>, {ASS} tags, dash/♪ tokens; min word length 20 ms; times rounded to ms
- **الدليل / proof:** `kosif-tool/tools/words_convert.py`

#### SYNC-22 · تقديم وتأخير التوقيت · Sync offset nudging (--offset/--min-gap) · ✅ مُثبت هنا
- **ماذا / what:** Shift every timestamp earlier/later and enforce a minimum gap between words to fix transcriber drift.
- **كيف / how:** --offset -0.08 --min-gap 0.02
- **الدليل / proof:** `kosif-tool/tools/words_convert.py:122`

#### SYNC-23 · صيغة words.json والمحوّل · words.json format and converter · ✅ مُثبت هنا
- **ماذا / what:** Master timing file [{word,start,end}] in seconds, sorted, non-overlapping; converted from Whisper JSON/SRT/VTT/CSV.
- **كيف / how:** python3 tools/words_convert.py voice.json words.json (also --format srt|vtt|json|csv|tsv, --offset, --min-gap); words.js for html-canvas.
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:27` · `kosif-tool/playbooks/audio-sync.md:32` · `kosif-tool/tools/words_convert.py`

#### SYNC-24 · نمط ترجمة reels · Caption style reels · 🟢 جاهز
- **ماذا / what:** Arabic karaoke caption style 'reels'.
- **كيف / how:** python scripts/kmotion.py captions CLIP.mp4 --spec caps.json --style reels
- **أرقام / params:** Noto Sans Arabic 74, white, spoken word yellow pops
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/montage.py:308` · `100-superskills/skills/kosif-montage-motion/SKILL.md:391` · `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`

#### SYNC-25 · نمط ترجمة cinema · Caption style cinema · 🟢 جاهز
- **ماذا / what:** Arabic karaoke caption style 'cinema'.
- **كيف / how:** python scripts/kmotion.py captions CLIP.mp4 --spec caps.json --style cinema
- **أرقام / params:** Noto Naskh Arabic 46, soft highlight, pop 104
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/montage.py:308` · `100-superskills/skills/kosif-montage-motion/SKILL.md:391` · `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`

#### SYNC-26 · نمط ترجمة punchy · Caption style punchy · 🟢 جاهز
- **ماذا / what:** Arabic karaoke caption style 'punchy'.
- **كيف / how:** python scripts/kmotion.py captions CLIP.mp4 --spec caps.json --style punchy
- **أرقام / params:** Noto Kufi Arabic 72, thick 8 outline, pop 116
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/montage.py:308` · `100-superskills/skills/kosif-montage-motion/SKILL.md:391` · `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`

#### SYNC-27 · نمط ترجمة tiktok · Caption style tiktok · 🟢 جاهز
- **ماذا / what:** Arabic karaoke caption style 'tiktok'.
- **كيف / how:** python scripts/kmotion.py captions CLIP.mp4 --spec caps.json --style tiktok
- **أرقام / params:** Noto Kufi Arabic 84, ≤4 words, outline 10, pop 120/90 ms
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/montage.py:308` · `100-superskills/skills/kosif-montage-motion/SKILL.md:391` · `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`

#### SYNC-28 · نمط ترجمة hormozi · Caption style hormozi · 🟢 جاهز
- **ماذا / what:** Arabic karaoke caption style 'hormozi'.
- **كيف / how:** python scripts/kmotion.py captions CLIP.mp4 --spec caps.json --style hormozi
- **أرقام / params:** Noto Kufi Arabic 96, one word, green highlight, pop 118/80 ms
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/montage.py:308` · `100-superskills/skills/kosif-montage-motion/SKILL.md:391` · `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`

#### SYNC-29 · نمط ترجمة boxed · Caption style boxed · 🟢 جاهز
- **ماذا / what:** Arabic karaoke caption style 'boxed'.
- **كيف / how:** python scripts/kmotion.py captions CLIP.mp4 --spec caps.json --style boxed
- **أرقام / params:** Noto Sans Arabic 66, ≤5 words, semi-opaque box
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/montage.py:308` · `100-superskills/skills/kosif-montage-motion/SKILL.md:391` · `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`

#### SYNC-30 · نمط ترجمة minimal · Caption style minimal · 🟢 جاهز
- **ماذا / what:** Arabic karaoke caption style 'minimal'.
- **كيف / how:** python scripts/kmotion.py captions CLIP.mp4 --spec caps.json --style minimal
- **أرقام / params:** Noto Naskh Arabic 54, ≤7 words, no pop, interviews
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/montage.py:308` · `100-superskills/skills/kosif-montage-motion/SKILL.md:391` · `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`

#### SYNC-31 · ستايل ترجمة كاريوكي: cinema · Karaoke caption style: cinema · 🟢 جاهز
- **ماذا / what:** Burned-in Arabic karaoke captions where the spoken word is coloured and pops; one ASS event per word so Arabic shapes and orders correctly.
- **كيف / how:** python montage.py captions VIDEO --spec caps.json --style cinema (or reel --style cinema); spec from transcribe.py or voice.py timings.
- **أرقام / params:** font Noto Naskh Arabic; size 46 per 1080 px height; primary #EAEAEA; highlight #FFE6A8 (ASS &H00A8E6FF); outline 3; shadow 2; bottom margin 150 per 1920; max 6 words per line
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/montage.py:225` · `kosif-one/tools/kosif-studio/motion/montage.py:257` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/smart_montage.py:92` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/smart_montage.py:81`

#### SYNC-32 · ستايل ترجمة كاريوكي: punchy · Karaoke caption style: punchy · 🟢 جاهز
- **ماذا / what:** Burned-in Arabic karaoke captions where the spoken word is coloured and pops; one ASS event per word so Arabic shapes and orders correctly.
- **كيف / how:** python montage.py captions VIDEO --spec caps.json --style punchy (or reel --style punchy); spec from transcribe.py or voice.py timings.
- **أرقام / params:** font Noto Kufi Arabic; size 72 per 1080 px height; primary #FFFFFF; highlight #38BDF8 (ASS &H00F8BD38); outline 8; shadow 4; bottom margin 330 per 1920; max 6 words per line
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/montage.py:225` · `kosif-one/tools/kosif-studio/motion/montage.py:257` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/smart_montage.py:93` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/smart_montage.py:81`

#### SYNC-33 · كلمات حركية متزامنة مع توقيت الكلام · Per-word kinetic text synced to word timestamps · 🟢 جاهز
- **ماذا / what:** Each word appears at its spoken onset, sliding in with a horizontal offset that decays word by word so the line seems to settle like a camera.
- **كيف / how:** Read words.json/transcript.json onsets, wrap words in inline-block spans, add one tween per word at its onset time. For Arabic keep words whole and slide from the right (RTL).
- **أرقام / params:** slide x 80,60,50,25,12px decaying; y 14; 0.35s power2.out; word margin 0.12em
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### SYNC-34 · تجهيز الصوت للتفريغ وفخ التوقيت · STT audio prep and its timing trap · 🟢 جاهز
- **ماذا / what:** For transcription only: high-pass 200 Hz / low-pass 3 kHz on noisy audio and 16 kHz mono PCM. Silence removal (0.5 s at -30 dB) can cut billable minutes 10-40% and 1.25x atempo another 20%, but both break the alignment with the original timeline - never use such outputs for caption or word timing un…
- **كيف / how:** ffmpeg -af 'highpass=f=200,lowpass=f=3000' -ar 16000 -ac 1 -c:a pcm_s16le; always transcribe or force-align against the untouched original for words.json (Whisper needs install; Deepgram needs a key).
- **أرقام / params:** 16 kHz mono; HPF 200 / LPF 3000; silenceremove 0.5 s @ -30 dB; atempo 1.25
- **الدليل / proof:** `kosif-atlas/skills/1845-deepgram-pack/5468-deepgram-cost-tuning/SKILL.md` · `kosif-atlas/skills/1845-deepgram-pack/5466-deepgram-core-workflow-a/SKILL.md`

#### SYNC-35 · تجميع كلمات الترجمة وموضعها · Caption word grouping & placement · 🟢 جاهز
- **ماذا / what:** High energy 2-3 words per group, conversational 3-5, calm 4-6; break on sentence ends or pauses ≥150 ms. Landscape: 80-120 px from bottom; portrait: ~600-700 px from bottom; one group visible at a time; never over the face.
- **كيف / how:** fitTextFontSize(maxWidth 1600 landscape / 900 portrait, base 78, min 42, step 2); container full-width absolute, overflow visible; hard kill each group: fade 0.12 s then set visibility hidden at group end; self-lint by seeking end+0.01.
- **أرقام / params:** 2-6 words; 150 ms pause break
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md`

#### SYNC-36 · كابشن آلة كاتبة مع كلمة مفتاحية · Typewriter caption with keyword highlight · 🟢 جاهز
- **ماذا / what:** Small guide sentence then a 2-3x larger pale-yellow serif keyword; write-on reveal timed to speech.
- **كيف / how:** Fusion Text+ Write On End or GSAP text reveal; keyword #FFE67A; reveal ~65% of clip; underline/circle draw-on after full reveal.
- **أرقام / params:** #FFE67A, 2-3x
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2431-akbun-davinciresolve-caption-template`

#### SYNC-37 · كلمات تظهر مع الكلام · Per-word kinetic typography synced to transcript · 🟢 جاهز
- **ماذا / what:** Each word enters at its spoken onset from words.json.
- **كيف / how:** Wrap words in inline-block spans; GSAP tl.from(word,{x,y:14,opacity:0,duration:0.35,ease:'power2.out'},onset). For Arabic animate whole words only.
- **أرقام / params:** dur 0.35s; y 14px
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/SKILL.md`

#### SYNC-38 · مقياس مستوى الميكروفون · Mic RMS level meter (Web Audio) · 🟢 جاهز
- **ماذا / what:** Computes a 0-1 loudness value from the microphone for driving visuals.
- **كيف / how:** AudioContext -> createMediaStreamSource(stream) -> AnalyserNode (fftSize 256); getByteTimeDomainData; RMS of (v-128)/128, multiplied by 4, clamped to 1.
- **أرقام / params:** fftSize 256 (128 samples); gain x4; clamp 1
- **الدليل / proof:** `kosif-audit-studio/voice.js:166` · `kosif-audit-studio/voice.js:368`

#### SYNC-39 · فقاعات النص المتدفق · Streaming transcript bubbles · 🟢 جاهز
- **ماذا / what:** Assistant transcript deltas render as an italic interim line, then commit to chat bubbles; user bubbles align to start, assistant to end, each with a squared tail corner and a source label.
- **كيف / how:** handleRealtimeEvent: response.output_audio_transcript.delta -> 'interim'; .done -> 'reply'; appendVoiceBubble(role,text,meta).
- **أرقام / params:** bubble max-width 88%, padding 10x14px, radius 16px with 4px tail corner, 13.5px/1.65; interim 12.5px italic muted; meta 10.5px
- **الدليل / proof:** `kosif-audit-studio/voice.js:204` · `kosif-audit-studio/app.js:2054` · `kosif-audit-studio/styles.css:839`

#### SYNC-40 · الإملاء الصوتي العربي · Arabic dictation (Web Speech STT) · 🟢 جاهز
- **ماذا / what:** Mic button transcribes Arabic speech into the input with live interim text.
- **كيف / how:** SR = SpeechRecognition||webkitSpeechRecognition; rec.lang='ar-SA'; interimResults=true; continuous=false; toast when unsupported.
- **أرقام / params:** ar-SA
- **الدليل / proof:** `kosif-earth-ci-fork/ui/features/assistant.js:285`

#### SYNC-41 · ترجمة كاريوكي · Karaoke captions ASS · 🟢 جاهز
- **ماذا / what:** One ASS event per word with highlight colour and pop so Arabic stays shaped; words timed by length if no times.
- **كيف / how:** python scripts/kmotion.py captions CLIP.mp4 --spec caps.json --style …
- **أرقام / params:** 120 ms pop; ASS Encoding -1; weights len+2
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### SYNC-42 · خفض الموسيقى تحت الصوت · Sidechain music ducking · 🟢 جاهز
- **ماذا / what:** Music bed ducks under voice or footage speech.
- **كيف / how:** sidechaincompress threshold 0.02 ratio 12 attack 20 release 300 (timeline/montage); motion.py uses 0.03/6/380
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:815` · `100-superskills/skills/kosif-montage-motion/scripts/montage.py:260` · `100-superskills/skills/kosif-montage-motion/scripts/motion.py:435`

#### SYNC-43 · تطبيع الصوت -14 · Two-pass loudness -14 LUFS · 🟢 جاهز
- **ماذا / what:** Measure then linear loudnorm to target with limiter.
- **كيف / how:** loudnorm I=-14 TP=-1.5 LRA=11 two-pass
- **أرقام / params:** -14 LUFS, TP -1.5
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:652`

#### SYNC-44 · تفريغ بتوقيت الكلمات · Transcribe word times · 🟢 جاهز
- **ماذا / what:** faster-whisper words.json, SRT (BOM), captions.json.
- **كيف / how:** transcribe.py SRC --model large-v3 --lang ar --vad auto
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/transcribe.py`

#### SYNC-45 · صوت إلى موشن · Voice2Motion · 🟢 جاهز
- **ماذا / what:** Audio + transcript/cues → semantic motion graphic (weather/traffic/support/refund/generic) via Pillow.
- **كيف / how:** audio2motion.py AUDIO --transcript t.txt --fps 24 --size 540x960
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/audio2motion.py:88` · `100-superskills/skills/kosif-montage-motion/scripts/test_audio2motion.py`

#### SYNC-46 · قياس الجهارة المتكاملة · Integrated loudness measurement (BS.1770-4, offline) · 🟢 جاهز
- **ماذا / what:** Measures integrated LUFS of any audio file with K-weighting applied as a zero-phase frequency-domain filter, 400 ms blocks every 100 ms and absolute/relative gating, plus the gain needed to reach a delivery target.
- **كيف / how:** python3 scripts/omni/audio_analyze.py FILE [--target streaming|podcast|broadcast|club] [--summary]; WAV read natively (8/16/24/32-bit), other formats via soundfile or an ffmpeg → 24-bit WAV conversion.
- **أرقام / params:** gates −70 LUFS absolute, −10 LU relative; surround channels 4–5 weighted 1.41; verified here on a 6 s 440 Hz tone at −28.5 dBFS → −32.21 LUFS, gain +18.21 dB to −14
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/audio_analyze.py:87` · `100-superskills/skills/kosif-montage-motion/scripts/omni/audio_analyze.py:112` · `100-superskills/skills/kosif-montage-motion/scripts/omni/audio_analyze.py:195`

#### SYNC-47 · أهداف الجهارة للتسليم · Loudness delivery targets · 🟢 جاهز
- **ماذا / what:** Four named loudness / true-peak targets for mixing and checks.
- **كيف / how:** audio_analyze.py --target NAME; report.target.gain_to_target_db.
- **أرقام / params:** streaming −14 LUFS / −1.0 dBTP · podcast −16 / −1.0 · broadcast −23 / −1.0 · club −8 / −0.3
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/audio_analyze.py:30`

#### SYNC-48 · القمة الحقيقية التقريبية · Approximate true-peak (4× oversampling) · 🟢 جاهز
- **ماذا / what:** Estimates inter-sample peaks by 4× polyphase oversampling with a Kaiser-windowed sinc, per channel.
- **كيف / how:** true_peak(x, factor=4, taps_per_phase=12): 48-tap sinc · kaiser(β 8), each phase normalised to unity DC gain, np.convolve mode 'same'.
- **أرقام / params:** 4×, 12 taps per phase, Kaiser β 8
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/audio_analyze.py:131`

#### SYNC-49 · كاشف مقاطع الصمت · Silence segment finder · 🟢 جاهز
- **ماذا / what:** Lists quiet stretches (start, end) in seconds, useful for jump cuts and for aligning motion to pauses.
- **كيف / how:** silence(mono, sr, thr_db=−50, min_len=0.5) over 50 ms RMS windows; in the report as silence_segments.
- **أرقام / params:** threshold −50 dBFS; minimum 0.5 s; window 50 ms
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/audio_analyze.py:147`

#### SYNC-50 · توازن الطيف وسطوعه · Spectral balance, brightness and band energy · 🟢 جاهز
- **ماذا / what:** Reports the spectral centroid with a dark/balanced/bright label and the share of energy in six bands over the first 60 s.
- **كيف / how:** analyze(): rfft of mono; BANDS; brightness dark < 1200 Hz ≤ balanced < 3500 Hz ≤ bright.
- **أرقام / params:** bands sub 20–60, bass 60–250, low_mid 250–500, mid 500–2000, presence 2000–6000, air 6000–20000 Hz
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/audio_analyze.py:31` · `100-superskills/skills/kosif-montage-motion/scripts/omni/audio_analyze.py:195`

#### SYNC-51 · ارتباط الستيريو وتوازنه · Stereo correlation and balance · 🟢 جاهز
- **ماذا / what:** Checks phase correlation (negative = mono-compatibility problem) and left/right level balance in dB.
- **كيف / how:** analyze(): correlation = Σ(l·r)/√(Σl²·Σr²); balance_db_L_minus_R from channel RMS.
- **أرقام / params:** warn if correlation < 0 or |balance| > 1.5 dB
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/audio_analyze.py:195` · `100-superskills/skills/kosif-montage-motion/scripts/omni/audio_analyze.py:237`

#### SYNC-52 · اقتراحات إصلاح الصوت بالعربية · Audio auto-fix suggestions in Arabic · 🟢 جاهز
- **ماذا / what:** Turns the measurements into concrete Arabic fixes: clipping, true peak above target, gain to target, DC offset high-pass, low-mid mud cut, presence boost for dull speech, phase and balance problems.
- **كيف / how:** fixes(report) and summary_ar(report) (printed with --summary).
- **أرقام / params:** DC > 0.005 → high-pass 20 Hz; low_mid share > 0.35 → cut 2–4 dB at 250–500 Hz; presence < 0.03 and dark → lift 2–5 kHz; |gain| > 1 dB → apply gain
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/audio_analyze.py:237` · `100-superskills/skills/kosif-montage-motion/scripts/omni/audio_analyze.py:260`

#### SYNC-53 · حرق الترجمة على الفيديو · ASS subtitle burn-in (ffmpeg ass filter) · 🟢 جاهز
- **ماذا / what:** Renders any .ass file onto video with escaped path handling.
- **كيف / how:** ffmpeg -i in.mp4 -vf "ass='path'" -c:v libx264 -preset fast -crf 18 -c:a copy out.mp4 (path backslashes -> '/', ':' -> '\:').
- **أرقام / params:** CRF 18, preset fast, audio copy
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/smart_montage.py:140`

#### SYNC-54 · قنوات الصوت داخل الأنيميشن · Sound channels in the browser (MOTION.channels) · 🟢 جاهز
- **ماذا / what:** Reads the per-frame analysis JSON so any visual value can be driven by the soundtrack (bass, kicks, onsets, silence, tape clock).
- **كيف / how:** const ch = MOTION.channels(json); ch.v('bass',t), ch.kick(t), ch.onset(t), ch.beat(t), ch.tape(t), ch.silent(t), ch.near('onsets',t,0.05).
- **أرقام / params:** fps from JSON (default 30); kick pulse attack 1 tau 5
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:97`

#### SYNC-55 · ستايل ترجمة كاريوكي: reels · Karaoke caption style: reels · 🟢 جاهز
- **ماذا / what:** Burned-in Arabic karaoke captions where the spoken word is coloured and pops; one ASS event per word so Arabic shapes and orders correctly.
- **كيف / how:** python montage.py captions VIDEO --spec caps.json --style reels (or reel --style reels); spec from transcribe.py or voice.py timings.
- **أرقام / params:** font Noto Sans Arabic; size 74 per 1080 px height; primary #FFFFFF; highlight #FFDE59 (ASS &H0059DEFF); outline 6; shadow 3; bottom margin 300 per 1920; max 6 words per line
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/montage.py:225` · `kosif-one/tools/kosif-studio/motion/montage.py:257`

#### SYNC-56 · تطبيع الصوت بمرورين · Two-pass loudnorm · 🟢 جاهز
- **ماذا / what:** Measure then apply EBU R128 loudness normalisation with measured values (linear).
- **كيف / how:** Pass1 loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null; pass2 with measured_I/TP/LRA/thresh/offset, linear=true. Automated in edl_render.measure_loudness.
- **أرقام / params:** I -14 LUFS, TP -1 dBTP, LRA 11
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md` · `100-superskills/skills/pro-video-editor-ffmpeg/scripts/edl_render.py:48`

#### SYNC-57 · قص الصمت تلقائياً · Silence-cut EDL generator · 🟢 جاهز
- **ماذا / what:** Detects silences and writes an EDL keeping speech with padding.
- **كيف / how:** python3 silence_cut.py in --db -35 --min 0.6 --pad 0.12 --out edl.json (ffmpeg silencedetect).
- **أرقام / params:** -35 dB, >=0.6 s, pad 0.12 s
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/scripts/silence_cut.py:19`

#### SYNC-58 · قالب ترجمة الكلمة المنطوقة · Highlighted spoken-word caption template · 🟢 جاهز
- **ماذا / what:** Renders current page, highlights spoken word in one colour or scale 1.08, safe area bottom 20% margins 8%.
- **كيف / how:** templates/captions.html
- **أرقام / params:** hi #39E508; ink #FFFFFF; shadow rgba(0,0,0,.75); Cairo 900; sync +-1 frame on 5 samples
- **الدليل / proof:** `100-superskills/skills/audio-reactive-captions-studio/templates/captions.html` · `100-superskills/skills/audio-reactive-captions-studio/references/captions-rules.md`

#### SYNC-59 · التحقق من نص مؤقت مسبقاً · Pre-timed transcript validation · 🟢 جاهز
- **ماذا / what:** Accepts an external words.json only if it is bounded and monotonic, so reels can run without Whisper but never with invented timing.
- **كيف / how:** reel --transcript NAME.words.json → transcribe.load_transcript
- **أرقام / params:** ≤10 MB; ≤20,000 segments; word/segment tolerance 0.02 s; end ≤ duration + 0.15 s
- **الدليل / proof:** `kosif-studio/motion/transcribe.py:89`

#### SYNC-60 · تقدير التوقيت من مقاطع الصوت · Voiced-span timing estimate · 🟢 جاهز
- **ماذا / what:** Without any ASR, lays the text over the voiced parts of the audio in order and by word length, and labels it estimated.
- **كيف / how:** verse.voiced_spans + estimate
- **أرقام / params:** 50 ms frames; threshold max(−45 dB, p20+6 dB); merge gaps <0.35 s; spans >0.15 s
- **الدليل / proof:** `kosif-studio/motion/verse.py:121` · `kosif-studio/motion/verse.py:145`

#### SYNC-61 · قاعدة عدم المساس بالصوت · Untouched-voice rule · 🟢 جاهز
- **ماذا / what:** Supplied voice is the master clock; never resample, stretch or retime it; picture follows sound.
- **كيف / how:** render_html --audio (apad/-shortest) or Remotion <Audio> at frame 0
- **الدليل / proof:** `kosif-tool/templates/claude_request.en.txt` · `kosif-tool/tools/render_html.cjs:373`

#### SYNC-62 · تفريغ البث المباشر على دفعات · Live-stream chunked transcription · 📦 بأمر تثبيت
- **ماذا / what:** Transcribe an ongoing stream by cutting it into fixed chunks and transcribing each finished chunk, appending to a tail-able text file.
- **كيف / how:** ffmpeg -f segment -segment_time 30 from HLS/RTMP/Icecast URL (streamlink/yt-dlp resolve platform lives) -> whisper per chunk
- **أرقام / params:** 30 s chunks
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/886-intel/1994-transcribe/SKILL.md` · `kosif-atlas/skills/886-intel/1994-transcribe`

#### SYNC-63 · صيغة الترجمة في ريموشن · Remotion Caption JSON type · 📦 بأمر تثبيت
- **ماذا / what:** A standard caption record with text, startMs, endMs, timestampMs, confidence, used across transcribe/import/display.
- **كيف / how:** import type {Caption} from '@remotion/captions'; load JSON with useDelayRender; also parse SRT via import-srt helper. Our words.json can be mapped to this shape (ms).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10431-remotion-captions/SKILL.md` · `kosif-atlas/skills/2712-remotion/10431-remotion-captions/display-captions.md`

#### SYNC-64 · فخ نماذج whisper الإنجليزية · Whisper language trap · 📦 بأمر تثبيت
- **ماذا / what:** Models with the .en suffix translate non-English speech into English instead of transcribing it.
- **كيف / how:** For Arabic always use multilingual models (small/medium/large-v3) with --language ar; model sizes tiny 75MB, base 142MB, small 466MB, medium 1.5GB, large-v3 3.1GB; convert to 16kHz WAV first (ffmpeg -ar 16000); enable token-level timestamps.
- **أرقام / params:** 16 kHz; small=466MB; large-v3=3.1GB
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transcript-guide.md` · `kosif-atlas/skills/2712-remotion/10431-remotion-captions/transcribe-captions.md`

#### SYNC-65 · التحكم بالصوت في ريموشن · Remotion audio control · 📦 بأمر تثبيت
- **ماذا / what:** Layer, trim, delay and ramp audio tracks inside a React composition.
- **كيف / how:** <Audio src trimBefore={2*fps} trimAfter={10*fps} volume={0.5 | f=>interpolate(f,...)}/> from @remotion/media; delay by wrapping in <Sequence from>; multiple <Audio> layer naturally. Keep the user's voice track untouched; duck music with a volume callback.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/audio.md`

#### SYNC-66 · مدة ديناميكية حسب الصوت · calculateMetadata dynamic duration · 📦 بأمر تثبيت
- **ماذا / what:** Compute composition duration, size and props before render from asset metadata (voiceover lengths, source video size).
- **كيف / how:** calculateMetadata async: get durations (Mediabunny helpers) -> durationInFrames = ceil(sec*fps); per-scene voice files sum to total; can set defaultCodec/pixelFormat per composition.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/calculate-metadata.md` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/voiceover.md`

#### SYNC-67 · سجل تعليقات الأفعال أثناء التسجيل · Action-captions log during recording · 📦 بأمر تثبيت
- **ماذا / what:** Log a short caption at the instant of each visible browser action so the video gets an aligned caption track (videoTime + text).
- **كيف / how:** Fire the caption call in parallel with the action; convert to VTT/ASS; atlas tool uses a Chrome extension at ~5 fps (too low for motion), so prefer own Playwright timestamps.
- **أرقام / params:** captureVisibleTab ~5 fps; caption JSON {videoTime, text}
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2354-power-platform/9079-record-screen`

#### SYNC-68 · تجميع المونتاج من النص المفرغ · Transcript-driven beat assembly · 📦 بأمر تثبيت
- **ماذا / what:** Edit voice-led videos from the transcript: inventory every clip (type, face, length, sentence count, one-line summary), propose a beat sheet (beat | message | voice source range | screen | length) for user approval, then assemble segments in beat order with a CHAPTER marker per beat and GFX markers …
- **كيف / how:** Transcribe with word timestamps (whisper large-v3-turbo with word_timestamps or provided words.json); convert sentence times to frames; place voice on A1 and visuals on V1 at the same record frame; keep an 'unused sentences' list; first beat must pose the question/promise within 10 s.
- **أرقام / params:** hook within 10 s; target 5-7 min, <10 min
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2451-davinciresolve-beats-devtalk/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2460-davinciresolve-story-devtalk/SKILL.md`

#### SYNC-69 · ترجمة على طريقة تيك توك مع تمييز الكلمة · TikTok-style caption pages + word highlight · 📦 بأمر تثبيت
- **ماذا / what:** Group word-level captions into short pages and colour the currently spoken token.
- **كيف / how:** Remotion @remotion/captions: Caption{text,startMs,endMs,timestampMs,confidence}; createTikTokStyleCaptions({captions, combineTokensWithinMilliseconds:1200}); each page in a <Sequence from=startMs/1000*fps>; active token = frame time between token.fromMs/toMs -> colour #39E508; keep leading spaces and whiteSpace:'pre'. npx remotion add @remotion/captions (needs install).
- **أرقام / params:** page switch 1200 ms; highlight #39E508
- **تثبيت / install:** `npx remotion add @remotion/captions (needs install)`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10431-remotion-captions/display-captions.md` · `kosif-atlas/skills/2712-remotion/10431-remotion-captions/SKILL.md`

#### SYNC-70 · استيراد ملفات SRT/VTT · SRT/VTT import into caption pipeline · 📦 بأمر تثبيت
- **ماذا / what:** Reuse existing subtitles as timed caption data (phrase-level timing only; per-word effects need word timestamps).
- **كيف / how:** Remotion parseSrt({input}) from @remotion/captions; HyperFrames 'npx hyperframes transcribe file.srt|.vtt|openai.json' normalises to word array
- **تثبيت / install:** `npx hyperframes transcribe file`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10431-remotion-captions/import-srt-captions.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transcript-guide.md`

#### SYNC-71 · ترجمة تلقائية من الصوت في ريزولف · Resolve auto-subtitles from audio · 📦 بأمر تثبيت
- **ماذا / what:** Generate a subtitle track from speech inside Resolve, then correct proper nouns/terms against the transcript; track styling has no API and is set once in the Inspector.
- **كيف / how:** Timeline.CreateSubtitlesFromAudio({language, charsPerLine 18, lineBreak, gap 0}); never call InsertFusionTitleIntoTimeline mid-timeline (it splits V1 and ripples all unlocked tracks).
- **أرقام / params:** charsPerLine 18
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2464-davinciresolve-subtitle-devtalk/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2465-davinciresolve-subtitle-travelnote/SKILL.md`

#### SYNC-72 · تفريغ محلي بـ Whisper مع توقيت الكلمات · Local Whisper transcription with word timestamps · 📦 بأمر تثبيت
- **ماذا / what:** Transcribe speech to segments and words locally; foundation for captions, cuts, beat sync.
- **كيف / how:** faster-whisper WhisperModel('large-v3') + BatchedInferencePipeline(batch 8), word_timestamps -> {segments:[{start,end,text,words:[{start,end,word}]}]}; Apple: mlx_whisper.transcribe(path, path_or_hf_repo='mlx-community/whisper-large-v3-turbo', language=..., word_timestamps=True); whisper.cpp via Remotion installWhisperCpp(version 1.5.5) with tokenLevelTimestamps. Convert input to 16 kHz WAV first. Not installed here (pip install faster-whisper).
- **أرقام / params:** 16 kHz mono; batch 8
- **تثبيت / install:** `pip install faster-whisper)`
- **الدليل / proof:** `kosif-atlas/skills/2451-knowledge/9503-video-digest/extraction/transcript/asr_transcribe.py` · `kosif-atlas/skills/1096-akbun-editvideo/2451-davinciresolve-beats-devtalk/SKILL.md` · `kosif-atlas/skills/2712-remotion/10431-remotion-captions/transcribe-captions.md`

#### SYNC-73 · اختيار حجم نموذج Whisper · Whisper model size ladder · 📦 بأمر تثبيت
- **ماذا / what:** tiny 75 MB (pipeline test), base 142 MB (short clean), small 466 MB (default), medium 1.5 GB (noisy/music; minimum for lyrics), large-v3 3.1 GB (production); turbo is the speed/accuracy sweet spot.
- **كيف / how:** pick per content; for sung lyrics prefer supplying known lyrics and forced-aligning
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transcript-guide.md` · `kosif-atlas/skills/1864-groq-pack/5867-groq-core-workflow-b/SKILL.md`

#### SYNC-74 · تفريغ محلي بكلمات مؤقتة (Whisper) · Local whisper word-timestamp transcription · 📦 بأمر تثبيت
- **ماذا / what:** Transcribe speech locally with per-word start/end times to drive captions and cuts.
- **كيف / how:** openai-whisper or whisper.cpp / mlx-whisper (Mac) with word_timestamps=True; model large-v3-turbo for quality; needs pip install + model download.
- **أرقام / params:** models tiny 75MB … large-v3 3.1GB
- **تثبيت / install:** `pip install + model download`
- **الدليل / proof:** `kosif-atlas/skills/886-intel/1994-transcribe` · `kosif-atlas/skills/1096-akbun-editvideo/2451-davinciresolve-beats-devtalk` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transcript-guide.md`

#### SYNC-75 · استيراد ملفات الترجمة الجاهزة · Import SRT/VTT/OpenAI JSON transcripts · 📦 بأمر تثبيت
- **ماذا / what:** Normalize existing subtitle files into a word array; SRT/VTT give phrase-level only.
- **كيف / how:** hyperframes transcribe captions.srt or own parser into [{text,start,end}].
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transcript-guide.md`

#### SYNC-76 · دائرة حول الكلمة عند نطقها · Keyword circle/underline synced to word timing · 📦 بأمر تثبيت
- **ماذا / what:** Trigger a hand-drawn circle or underline exactly at the spoken onset of a keyword from words.json.
- **كيف / how:** Map word start time*fps to the annotation's interpolate start frame; length 12-20 frames; hold until phrase end.
- **أرقام / params:** onset from words.json; 12-20 frames draw
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/text-highlights.md` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### SYNC-77 · حركات الكابشن الاثنا عشر · Caption animation presets (12) · 📦 بأمر تثبيت
- **ماذا / what:** Twelve per-word caption animations driven by each word's spoken start time.
- **كيف / how:** drawCaptions(): pop (scale 0.6->1 easeBack 0.16 s), spring (0.35+0.65*spring(z=0.38,w=18)), stomp (1+1.25 -> 1 over 0.18 s, alpha in 0.07 s), mask (words rise from a clip mask, U.E.out over 0.5 s, 0.08 s stagger), rise (from 40% opacity, rise 0.5 fs, 0.4 s, 0.1 s stagger), karaoke (unspoken 45% white, current accent), cascade (0.07 s stagger, 0.2 s, rise 0.45 fs), blur (blur 0.22 fs -> 0 over 0.45 s), wave (sin(t*5.5+i*0.8)*0.09 fs), glitch (red #ff0050 / cyan #00c8ff offset 0.14 fs for 0.2 s), …
- **أرقام / params:** pop|spring|stomp|mask|rise|karaoke|cascade|blur|wave|glitch|fade|slide
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:347` · `app/index.html:316`

#### SYNC-78 · طرق إبراز الكلمة الحالية · Caption word highlight modes · 📦 بأمر تثبيت
- **ماذا / what:** The currently spoken word is emphasised with a box, colour, growing underline or glow.
- **كيف / how:** box = primary rounded rect 1.22 fs high radius 0.18 fs; color = accent fill; underline = accent bar 0.11 fs growing with easeOut over 0.18 s; glow = shadowColor accent, shadowBlur 0.5 fs; none.
- **أرقام / params:** box|color|underline|glow|none
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:393` · `app/index.html:316`

#### SYNC-79 · ستايلات الكابشن الجاهزة السبعة · Caption style presets (7) · 📦 بأمر تثبيت
- **ماذا / what:** One-click caption looks ported from the montage tool's karaoke presets.
- **كيف / how:** CAP_STYLES chips merge into S.style.caption and set accent: ريلز (Noto Sans Arabic 7, chunk 6, pop, colour, stroke 6, #ffde59); سينما (Noto Naskh 5.2, line, rise, stroke 3, #ffe6a8); قوي (Noto Kufi 6.8, pop, stroke 8, #38bdf8); تيك توك (Noto Kufi 7.8, chunk 4, spring, stroke 10, #ffe04d); كلمة واحدة (Noto Kufi 9, chunk 1, stomp, stroke 9, #39ff88); صندوق (Noto Sans 6.2, chunk 5, pop, box, stroke 2, #ffe04d); هادئ (Noto Naskh 5.4, line, mask, no highlight, stroke 2).
- **أرقام / params:** sizes are % of short side
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:2352`

#### SYNC-80 · ستايلات كابشن المونتاج الذكي · AutoEdit caption presets (5) · 📦 بأمر تثبيت
- **ماذا / what:** Five caption presets used by the smart full-montage pipeline.
- **كيف / how:** CAPS: cinema (Reem Kufi 11, bottom, mask, colour, stroke 7); trend (Lalezar 12, centre, pop, box, stroke 10); karaoke (Changa 10, bottom, karaoke, stroke 8); neon (Rubik 11, centre, blur, glow, stroke 4); minimal (IBM Plex Sans Arabic 8, bottom, fade, none, stroke 3); word mode with cfg.capWords (default 2); 16:9 caps size at 8.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/50_autoedit.js:835`

#### SYNC-81 · مقاس ومكان وطريقة الكابشن · Caption layout controls · 📦 بأمر تثبيت
- **ماذا / what:** Word-by-word chunks or full lines, size, stroke, shadow and vertical position including an automatic subject-avoiding position.
- **كيف / how:** caption.mode word|line; chunk 1-6 words; size 5-14% of short side (1.1x in word mode); stroke 0-12 (lineWidth=stroke*fs/60, black); shadow rgba(0,0,0,.55) blur 0.25 fs; position top 24%, center 52%, bottom 76% (72% with letterbox), auto = third farthest from tracked subject (bottom +0.04 bias); max width 84%; line height 1.35 fs.
- **أرقام / params:** size 5-14; chunk 1-6; stroke 0-12
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:347` · `app/public/js/00_editor.js:2906` · `app/index.html:316`

#### SYNC-82 · لوحة تباين تلقائية خلف الكابشن · Adaptive caption contrast plate · 📦 بأمر تثبيت
- **ماذا / what:** When captions have no stroke, the band behind them is sampled and a dark or light rounded plate is added only as strong as needed to reach readable contrast.
- **كيف / how:** capPlate(): every 6th frame draws the caption band into a 24x8 probe canvas, computes linear luminance (gamma 2.2) 10th/90th percentiles, WCAG ratio vs text colour; if < 4.5:1 sets plate alpha up to 0.75, eased by 0.2 per frame; plate radius 0.3 fs, shadow blur 0.3 fs.
- **أرقام / params:** target 4.5:1; max alpha 0.75; probe 24x8
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:3007`

#### SYNC-83 · توزيع النص على أماكن الكلام · Text-to-speech-stretch caption sync · 📦 بأمر تثبيت
- **ماذا / what:** Lays pasted transcript words over the stretches where speech energy was detected so captions follow pauses (no model needed).
- **كيف / how:** syncToSpeech(text,voiced,dur): words spread evenly over total voiced time, new segment after 5 words or a >0.3 s gap, min 0.25 s; falls back to spreadText (5 words/segment evenly) when voiced < 8% of duration.
- **أرقام / params:** 5 words/segment; gap 0.3 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:1096` · `app/public/js/00_editor.js:1089`

#### SYNC-84 · إبراز تلقائي للأرقام وأعلى صوت · Automatic emphasis from digits and loudness peaks · 📦 بأمر تثبيت
- **ماذا / what:** Numbers are starred automatically, and in lines without a star the word spoken at the loudest local peak gets the star.
- **كيف / how:** autoEm wraps any word with a digit in *...*; loudPeaks(): 0.25 s smoothed dB envelope inside speech, local maxima >= 4 dB above the median within +-3 s, kept >= 1.2 s apart, 3-12 per clip; emPeak stars the word under the top peak (>= 3 letters).
- **أرقام / params:** 4 dB over median; +-3 s window; spacing 1.2 s; 3-12 peaks
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:1875` · `app/public/js/00_editor.js:3032` · `app/public/js/00_editor.js:3042`

#### SYNC-85 · تصدير واستيراد SRT · SRT/VTT caption export and import · 📦 بأمر تثبيت
- **ماذا / what:** Captions export as SRT and import from SRT/VTT, stripping tags.
- **كيف / how:** srtT() formats HH:MM:SS,mmm; import regex accepts ',' or '.' millis and multi-line cues, strips <tags>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:2193` · `app/public/js/00_editor.js:2201`

#### SYNC-86 · مطابقة كلمات الفيلم مع التعليق · Voice-over word alignment for motion films · 📦 بأمر تثبيت
- **ماذا / what:** Places every drawn word of a motion film on the voiced stretches of a narration file, weighted by word length.
- **كيف / how:** MK.alignVoice(F,voiced,at): weight per word max(2,len)+1.5 mapped across voiced time; film length = max(last word + 1 s, last voiced + 0.8 s).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:74`

#### SYNC-87 · اكتشاف أماكن الكلام · Speech/voiced region detection · 📦 بأمر تثبيت
- **ماذا / what:** Detects stretches of speech or sound from the RMS envelope for caption timing, cut points and ducking.
- **كيف / how:** threshold = max(0.008, p90(env)*0.22); merge gaps < 0.28 s; drop stretches < 0.18 s; also reports silence ratio and gaps/minute used by the content classifier.
- **أرقام / params:** thr max(0.008,0.22*p90); merge 0.28 s; min 0.18 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:1081` · `app/public/js/00_editor.js:1083`

#### SYNC-88 · دمج الصوت الاختياري · Optional audio mux · 📦 بأمر تثبيت
- **ماذا / what:** Muxes a user-supplied licensed voice or soundtrack under the rendered video, trimmed to the shorter stream; silent otherwise.
- **كيف / how:** render.py --audio path -> ffmpeg -map 0:v -map 1:a -c:a aac -b:a 192k -shortest; else -an. No loudness normalisation or alignment.
- **أرقام / params:** AAC 192 kb/s; -shortest
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `fastify-motion-bro/scripts/render.py:15,40-41`

#### SYNC-89 · أمر: تفريغ صوتي · CLI: transcribe · 📦 بأمر تثبيت
- **ماذا / what:** ASR: --engine auto|parakeet|whisper, --model tiny.en..large-v3 (default small.en), --language, --to srt|vtt, --preserve-cues, --optional.
- **كيف / how:** npx hyperframes transcribe ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** ASR: --engine auto|parakeet|whisper, --model tiny.en..large-v3 (default small.en), --language, --to srt|vtt, --preserve-cues, --optional.
- **تثبيت / install:** `npx hyperframes transcribe`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### SYNC-90 · حفر الصوت للتعليق · Voiceover carve / ducking · 📦 بأمر تثبيت
- **ماذا / what:** Spectral dip carved into a music group under voice so speech stays clear.
- **كيف / how:** data-fx-carve on VO clip + data-audio-group on music; amount 0 / 0.25 (6dB 3 bands default) / 0.5 (10dB).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/reference/audio-effects.mdx`

#### SYNC-91 · ترجمة من التفريغ · Captions from transcript · 📦 بأمر تثبيت
- **ماذا / what:** Whisper/Parakeet word timings patched into a caption track; lint guards overflow, track kind, hard-kill exits.
- **كيف / how:** hyperframes transcribe --to srt|vtt or init --audio; registry caption-* components (pill-karaoke, kinetic-slam, neon-glow, emoji-pop, gradient-fill ...).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/captions-and-recuts.mdx` · `kosif-one/vendor/hyperframes/docs/guides/voice-and-audio.mdx` · `kosif-one/vendor/hyperframes/packages/lint/src/rules/captions.ts`

#### SYNC-92 · ترجمة عاكسة تلقائيًا · Blend Difference · 📦 بأمر تثبيت
- **ماذا / what:** Caption text that flips black/white per pixel against the footage via mix-blend-mode: difference.
- **كيف / how:** Install with `npx hyperframes add caption-blend-difference` (copies to compositions/components/caption-blend-difference.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render`…
- **أرقام / params:** expo.out 0.6 s
- **تثبيت / install:** `npx hyperframes add caption-blend-difference` (copies to compositions/components/caption-blend-difference`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-blend-difference/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-blend-difference/caption-blend-difference.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-blend-difference.mdx`

#### SYNC-93 · ترجمة بكاميرا متراجعة · Camera Follow Captions · 📦 بأمر تثبيت
- **ماذا / what:** A sentence is written into a world much larger than the frame; every new word is sized against what came before and the camera pulls back at a constant rate so each new word lands at the same screen size.
- **كيف / how:** Install with `npx hyperframes add caption-camera-follow` (copies to compositions/components/caption-camera-follow.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (head…
- **أرقام / params:** Helvetica Neue; accents gold #ffd84d|green #34d399|blue #38bdf8|violet #a78bfa; framing tight|standard|wide; smear off|subtle|standard|heavy; vars: accent=gold[gold|green|blue|violet]; framing=standard[tight|standard|wide]; smear=standard[off|subtle|standard|heavy]
- **تثبيت / install:** `npx hyperframes add caption-camera-follow` (copies to compositions/components/caption-camera-follow`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-camera-follow/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-camera-follow/caption-camera-follow.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-camera-follow.mdx`

#### SYNC-94 · ترجمة بمسح القص · Clip Wipe · 📦 بأمر تثبيت
- **ماذا / what:** Each word is revealed with a left-to-right clip-path wipe.
- **كيف / how:** Install with `npx hyperframes add caption-clip-wipe` (copies to compositions/components/caption-clip-wipe.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chr…
- **أرقام / params:** Poppins 800; white with #FFD700 active; power2.out 0.3 s; Google Fonts: Poppins
- **تثبيت / install:** `npx hyperframes add caption-clip-wipe` (copies to compositions/components/caption-clip-wipe`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-clip-wipe/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-clip-wipe/caption-clip-wipe.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-clip-wipe.mdx`

#### SYNC-95 · ترجمة تحريرية مزدوجة الخط · Editorial Emphasis · 📦 بأمر تثبيت
- **ماذا / what:** Two-font captions where emphasis words jump to a much larger italic serif against a small sans body.
- **كيف / how:** Install with `npx hyperframes add caption-editorial-emphasis` (copies to compositions/components/caption-editorial-emphasis.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes ren…
- **أرقام / params:** Playfair Display 800 italic + Inter 400; cream #f5f0d0; Google Fonts: Inter, Playfair Display
- **تثبيت / install:** `npx hyperframes add caption-editorial-emphasis` (copies to compositions/components/caption-editorial-emphasis`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-editorial-emphasis/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-editorial-emphasis/caption-editorial-emphasis.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-editorial-emphasis.mdx`

#### SYNC-96 · ترجمة بالإيموجي · Emoji Pop · 📦 بأمر تثبيت
- **ماذا / what:** Stroked bold captions with inline emoji and a horizontal squeeze entrance.
- **كيف / how:** Install with `npx hyperframes add caption-emoji-pop` (copies to compositions/components/caption-emoji-pop.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chr…
- **أرقام / params:** Gabarito 900; #FF76FF #FF0002 #B2F7FF on #000 stroke; Google Fonts: Gabarito
- **تثبيت / install:** `npx hyperframes add caption-emoji-pop` (copies to compositions/components/caption-emoji-pop`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-emoji-pop/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-emoji-pop/caption-emoji-pop.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-emoji-pop.mdx`

#### SYNC-97 · ترجمة غليتش ألوان · Glitch RGB · 📦 بأمر تثبيت
- **ماذا / what:** Captions with RGB channel separation and CRT scanline overlay flicker.
- **كيف / how:** Install with `npx hyperframes add caption-glitch-rgb` (copies to compositions/components/caption-glitch-rgb.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless C…
- **أرقام / params:** Space Grotesk 700; #ff003c / #00e5ff; jitter 0.045-0.12 s; Google Fonts: Space Grotesk
- **تثبيت / install:** `npx hyperframes add caption-glitch-rgb` (copies to compositions/components/caption-glitch-rgb`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-glitch-rgb/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-glitch-rgb/caption-glitch-rgb.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-glitch-rgb.mdx`

#### SYNC-98 · ترجمة بتدرج لوني · Gradient Fill · 📦 بأمر تثبيت
- **ماذا / what:** Gradient-clipped captions that bounce in elastically.
- **كيف / how:** Install with `npx hyperframes add caption-gradient-fill` (copies to compositions/components/caption-gradient-fill.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (head…
- **أرقام / params:** Montserrat 900; gradient #fe9f1b #f76e49 #ff2063 #fd56cb #ef7aff; Google Fonts: Montserrat
- **تثبيت / install:** `npx hyperframes add caption-gradient-fill` (copies to compositions/components/caption-gradient-fill`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-gradient-fill/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-gradient-fill/caption-gradient-fill.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-gradient-fill.mdx`

#### SYNC-99 · ترجمة بإبراز أحمر · Highlight · 📦 بأمر تثبيت
- **ماذا / what:** TikTok-style red box sweeps behind the currently spoken word.
- **كيف / how:** Install with `npx hyperframes add caption-highlight` (copies to compositions/components/caption-highlight.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chr…
- **أرقام / params:** Montserrat 800; box #ff1745/#df1238; 0.08-0.16 s; Google Fonts: Montserrat
- **تثبيت / install:** `npx hyperframes add caption-highlight` (copies to compositions/components/caption-highlight`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-highlight/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-highlight/caption-highlight.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-highlight.mdx`

#### SYNC-100 · ترجمة الكلمة الصادمة · Kinetic Slam · 📦 بأمر تثبيت
- **ماذا / what:** One word at a time fills the screen, alternating entry direction with back-out overshoot.
- **كيف / how:** Install with `npx hyperframes add caption-kinetic-slam` (copies to compositions/components/caption-kinetic-slam.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headle…
- **أرقام / params:** Anton; #FFD700 accent; back.out(1.7)/back.out(2.2), expo.out 0.2 s; Google Fonts: Anton
- **تثبيت / install:** `npx hyperframes add caption-kinetic-slam` (copies to compositions/components/caption-kinetic-slam`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-kinetic-slam/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-kinetic-slam/caption-kinetic-slam.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-kinetic-slam.mdx`

#### SYNC-101 · ترجمة فك الشفرة · Matrix Decode · 📦 بأمر تثبيت
- **ماذا / what:** Each caption word scrambles through random glyphs before resolving.
- **كيف / how:** Install with `npx hyperframes add caption-matrix-decode` (copies to compositions/components/caption-matrix-decode.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (head…
- **أرقام / params:** Space Grotesk 700; #00ff41; Google Fonts: Space Grotesk
- **تثبيت / install:** `npx hyperframes add caption-matrix-decode` (copies to compositions/components/caption-matrix-decode`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-matrix-decode/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-matrix-decode/caption-matrix-decode.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-matrix-decode.mdx`

#### SYNC-102 · ترجمة نيون متعددة · Neon Accent · 📦 بأمر تثبيت
- **ماذا / what:** Captions with multi-colour neon accent words that wiggle and drift.
- **كيف / how:** Install with `npx hyperframes add caption-neon-accent` (copies to compositions/components/caption-neon-accent.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless…
- **أرقام / params:** Montserrat 800; #FCFF00 #53FF01 #FF0002; sine.inOut drift; Google Fonts: Montserrat
- **تثبيت / install:** `npx hyperframes add caption-neon-accent` (copies to compositions/components/caption-neon-accent`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-neon-accent/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-neon-accent/caption-neon-accent.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-neon-accent.mdx`

#### SYNC-103 · ترجمة نيون متوهج · Neon Glow · 📦 بأمر تثبيت
- **ماذا / what:** Cyan/magenta neon glow captions with flickering keyword accents.
- **كيف / how:** Install with `npx hyperframes add caption-neon-glow` (copies to compositions/components/caption-neon-glow.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chr…
- **أرقام / params:** Outfit 900; #FF0099 / #00FFF0; steps(1) flicker 0.06 s; Google Fonts: Outfit
- **تثبيت / install:** `npx hyperframes add caption-neon-glow` (copies to compositions/components/caption-neon-glow`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-neon-glow/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-neon-glow/caption-neon-glow.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-neon-glow.mdx`

#### SYNC-104 · ترجمة خلف الشخص · Parallax Layers · 📦 بأمر تثبيت
- **ماذا / what:** Large serif captions layered behind the subject for a 3D depth read, with a vertical stretch entrance (needs a matte/cutout of the subject).
- **كيف / how:** Install with `npx hyperframes add caption-parallax-layers` (copies to compositions/components/caption-parallax-layers.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (…
- **أرقام / params:** Instrument Serif; red #e50914/#a30610; Google Fonts: Instrument Serif
- **تثبيت / install:** `npx hyperframes add caption-parallax-layers` (copies to compositions/components/caption-parallax-layers`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-parallax-layers/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-parallax-layers/caption-parallax-layers.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-parallax-layers.mdx`

#### SYNC-105 · ترجمة بانفجار جزيئات · Particle Burst · 📦 بأمر تثبيت
- **ماذا / what:** Keyword words fire coloured particle explosions as they appear.
- **كيف / how:** Install with `npx hyperframes add caption-particle-burst` (copies to compositions/components/caption-particle-burst.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (he…
- **أرقام / params:** Outfit 900; #FFD700; back.out(1.5); Google Fonts: Outfit
- **تثبيت / install:** `npx hyperframes add caption-particle-burst` (copies to compositions/components/caption-particle-burst`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-particle-burst/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-particle-burst/caption-particle-burst.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-particle-burst.mdx`

#### SYNC-106 · ترجمة كاريوكي داخل كبسولة · Pill Karaoke · 📦 بأمر تثبيت
- **ماذا / what:** Captions sit in a dark pill and each word changes colour exactly on its spoken timestamp.
- **كيف / how:** Install with `npx hyperframes add caption-pill-karaoke` (copies to compositions/components/caption-pill-karaoke.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headle…
- **أرقام / params:** Poppins 700; pill #1C1E1D, idle #A6A6A6, active #e7e5e7; TRANSCRIPT [{text,start,end}]; Google Fonts: Poppins
- **تثبيت / install:** `npx hyperframes add caption-pill-karaoke` (copies to compositions/components/caption-pill-karaoke`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-pill-karaoke/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-pill-karaoke/caption-pill-karaoke.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-pill-karaoke.mdx`

#### SYNC-107 · ترجمة بخامة متحركة · Texture · 📦 بأمر تثبيت
- **ماذا / what:** Big uppercase captions filled with a flowing texture mask.
- **كيف / how:** Install with `npx hyperframes add caption-texture` (copies to compositions/components/caption-texture.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **أرقام / params:** Anton; textures lava|marble|metal|wood|concrete|rock (PNG files shipped); vars: texture=lava; Google Fonts: Anton
- **تثبيت / install:** `npx hyperframes add caption-texture` (copies to compositions/components/caption-texture`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-texture/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-texture/caption-texture.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-texture.mdx`

#### SYNC-108 · ترجمة بتغير الوزن · Weight Shift · 📦 بأمر تثبيت
- **ماذا / what:** Elegant caption lines that move between light and bold weights.
- **كيف / how:** Install with `npx hyperframes add caption-weight-shift` (copies to compositions/components/caption-weight-shift.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headle…
- **أرقام / params:** Montserrat 300->700; Google Fonts: Montserrat
- **تثبيت / install:** `npx hyperframes add caption-weight-shift` (copies to compositions/components/caption-weight-shift`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-weight-shift/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/caption-weight-shift/caption-weight-shift.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/caption-weight-shift.mdx`

#### SYNC-109 · شريط أخبار بيلد · Lower Third — BILD Style · 📦 بأمر تثبيت
- **ماذا / what:** News lower third with tight text boxes: white headline bar with red drop shadow and red sub-line with white shadow.
- **كيف / how:** Install with `npx hyperframes add lower-third-bild` (copies the full composition to compositions/lower-third-bild.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Barlow Condensed Bold/ExtraBold; #dd0000, #212529; vars: TXT_MAIN_1_Line=BILD EXKLUSIV; TXT_SUB=Sonderbericht; 1920x1080; duration 8 s
- **تثبيت / install:** `npx hyperframes add lower-third-bild` (copies the full composition to compositions/lower-third-bild`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/lower-third-bild/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/lower-third-bild/lower-third-bild.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/lower-third-bild.mdx`

#### SYNC-110 · شريط سفلي بخط لوني · Lower Third — Accent Underline · 📦 بأمر تثبيت
- **ماذا / what:** Cardless lower third: name rises, accent rule draws left to right, role fades in; text-shadowed for footage.
- **كيف / how:** Install with `npx hyperframes add lt-accent-underline` (copies the full composition to compositions/lt-accent-underline.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Oswald + Space Mono; accent #46e5b7; 4.8 s; 1920x1080; duration 4.8 s
- **تثبيت / install:** `npx hyperframes add lt-accent-underline` (copies the full composition to compositions/lt-accent-underline`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/lt-accent-underline/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/lt-accent-underline/lt-accent-underline.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/lt-accent-underline.mdx`

#### SYNC-111 · شريط سفلي كتلة جريئة · Lower Third — Bold Block · 📦 بأمر تثبيت
- **ماذا / what:** High-energy lower third: dark block wipes in, uppercase name slams up, accent tag pops.
- **كيف / how:** Install with `npx hyperframes add lt-bold-block` (copies the full composition to compositions/lt-bold-block.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Archivo Black + Space Mono; #141518; back.out(1.6/2); 1920x1080; duration 4.8 s
- **تثبيت / install:** `npx hyperframes add lt-bold-block` (copies the full composition to compositions/lt-bold-block`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/lt-bold-block/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/lt-bold-block/lt-bold-block.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/lt-bold-block.mdx`

#### SYNC-112 · شريط سفلي نظيف · Lower Third — Clean Bar · 📦 بأمر تثبيت
- **ماذا / what:** Minimal white card with accent tab, name + role, clip-wipe entrance.
- **كيف / how:** Install with `npx hyperframes add lt-clean-bar` (copies the full composition to compositions/lt-clean-bar.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Montserrat; tab #ff5a36; text #0f1115/#5a6170; 1920x1080; duration 4.8 s
- **تثبيت / install:** `npx hyperframes add lt-clean-bar` (copies the full composition to compositions/lt-clean-bar`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/lt-clean-bar/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/lt-clean-bar/lt-clean-bar.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/lt-clean-bar.mdx`

#### SYNC-113 · شريط سفلي كتلة ملونة · Lower Third — Color Block · 📦 بأمر تثبيت
- **ماذا / what:** Bold accent block slides in with overshoot, condensed name and mono role.
- **كيف / how:** Install with `npx hyperframes add lt-color-block` (copies the full composition to compositions/lt-color-block.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** League Gothic + Space Mono; #2756ff; back.out(1.4); 1920x1080; duration 4.8 s
- **تثبيت / install:** `npx hyperframes add lt-color-block` (copies the full composition to compositions/lt-color-block`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/lt-color-block/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/lt-color-block/lt-color-block.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/lt-color-block.mdx`

#### SYNC-114 · شريط سفلي بطاقة داكنة · Lower Third — Dark Card · 📦 بأمر تثبيت
- **ماذا / what:** Charcoal card for bright footage: name, drawn accent underline, role; slide-up entrance.
- **كيف / how:** Install with `npx hyperframes add lt-dark-card` (copies the full composition to compositions/lt-dark-card.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Montserrat; accent #f5b942; muted #aeb6c2; 1920x1080; duration 4.8 s
- **تثبيت / install:** `npx hyperframes add lt-dark-card` (copies the full composition to compositions/lt-dark-card`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/lt-dark-card/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/lt-dark-card/lt-dark-card.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/lt-dark-card.mdx`

#### SYNC-115 · شريط سفلي بعنوان صغير · Lower Third — Kicker Name · 📦 بأمر تثبيت
- **ماذا / what:** Cardless lower third with accent kicker tag, heavy name and drawn baseline.
- **كيف / how:** Install with `npx hyperframes add lt-kicker-name` (copies the full composition to compositions/lt-kicker-name.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Archivo Black + Space Mono; #46e5b7; 1920x1080; duration 4.8 s
- **تثبيت / install:** `npx hyperframes add lt-kicker-name` (copies the full composition to compositions/lt-kicker-name`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/lt-kicker-name/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/lt-kicker-name/lt-kicker-name.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/lt-kicker-name.mdx`

#### SYNC-116 · شريط سفلي بكشف القناع · Lower Third — Mask Reveal · 📦 بأمر تثبيت
- **ماذا / what:** Cardless: an accent sweep crosses and clip-reveals a heavy name; role fades up.
- **كيف / how:** Install with `npx hyperframes add lt-mask-reveal` (copies the full composition to compositions/lt-mask-reveal.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Montserrat; sweep #ffd23f; 1920x1080; duration 4.8 s
- **تثبيت / install:** `npx hyperframes add lt-mask-reveal` (copies the full composition to compositions/lt-mask-reveal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/lt-mask-reveal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/lt-mask-reveal/lt-mask-reveal.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/lt-mask-reveal.mdx`

#### SYNC-117 · شريط سفلي بإطار نيون · Neon Border · 📦 بأمر تثبيت
- **ماذا / what:** Two light arcs travel a rounded panel edge and snap corner to corner with soft three-layer bloom, framing name and role.
- **كيف / how:** Install with `npx hyperframes add lt-neon-border` (copies the full composition to compositions/lt-neon-border.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** accent #cc9149; movement step|glide; speed 1.6; cornerRadius 26; thickness 5; arcLength 22; glow 1; Inter; vars: name=Dr. Maya Chen; role=Host · Neuroscientist; accent=#cc9149; movement=step[step|glide]; speed=1.6(0.2..6); cornerRadius=26(0..90); thickness=5(1..16); arcLength=22(5..100); glow=1(0..2…
- **تثبيت / install:** `npx hyperframes add lt-neon-border` (copies the full composition to compositions/lt-neon-border`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/lt-neon-border/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/lt-neon-border/lt-neon-border.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/lt-neon-border.mdx`

#### SYNC-118 · شريط سفلي بخط جانبي · Lower Third — Side Rule · 📦 بأمر تثبيت
- **ماذا / what:** Cardless with a vertical accent bar, condensed display name and mono role.
- **كيف / how:** Install with `npx hyperframes add lt-side-rule` (copies the full composition to compositions/lt-side-rule.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** League Gothic + JetBrains Mono; #46e5b7; 1920x1080; duration 4.8 s
- **تثبيت / install:** `npx hyperframes add lt-side-rule` (copies the full composition to compositions/lt-side-rule`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/lt-side-rule/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/lt-side-rule/lt-side-rule.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/lt-side-rule.mdx`

#### SYNC-119 · شريط سفلي كبسولة · Lower Third — Soft Pill · 📦 بأمر تثبيت
- **ماذا / what:** Rounded white pill with status dot, name + role, scale-pop entrance.
- **كيف / how:** Install with `npx hyperframes add lt-soft-pill` (copies the full composition to compositions/lt-soft-pill.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Montserrat; #ff5a36; back.out(1.7/3); 1920x1080; duration 4.8 s
- **تثبيت / install:** `npx hyperframes add lt-soft-pill` (copies the full composition to compositions/lt-soft-pill`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/lt-soft-pill/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/lt-soft-pill/lt-soft-pill.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/lt-soft-pill.mdx`

#### SYNC-120 · شريطان متراكبان · Lower Third — Stack Bars · 📦 بأمر تثبيت
- **ماذا / what:** Dark name bar wipes from the left while an accent role bar wipes from the right.
- **كيف / how:** Install with `npx hyperframes add lt-stack-bars` (copies the full composition to compositions/lt-stack-bars.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Archivo Black + Space Mono; #141518 / #ffd23f; 1920x1080; duration 4.8 s
- **تثبيت / install:** `npx hyperframes add lt-stack-bars` (copies the full composition to compositions/lt-stack-bars`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/lt-stack-bars/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/lt-stack-bars/lt-stack-bars.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/lt-stack-bars.mdx`

#### SYNC-121 · إبراز متزامن بالصوت · Word-Sweep Highlight · 📦 بأمر تثبيت
- **ماذا / what:** Sentence whose word-by-word emphasis follows one scalar; tween the scalar to match a voiceover.
- **كيف / how:** Install with `npx hyperframes add mk-callout-highlight` (copies the full composition to compositions/mk-callout-highlight.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 8 s; 1920x1080; duration 8 s
- **تثبيت / install:** `npx hyperframes add mk-callout-highlight` (copies the full composition to compositions/mk-callout-highlight`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/mk-callout-highlight/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/mk-callout-highlight/mk-callout-highlight.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/mk-callout-highlight.mdx`

#### SYNC-122 · شريط الأخبار · News Ticker · 📦 بأمر تثبيت
- **ماذا / what:** Broadcast lower-third ticker with LIVE label, headline ribbon and scrolling crawl.
- **كيف / how:** Install with `npx hyperframes add news-ticker` (copies the full composition to compositions/news-ticker.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Inter; red #e11d2e; navy #050b15; 7 s; 1920x1080; duration 7 s
- **تثبيت / install:** `npx hyperframes add news-ticker` (copies the full composition to compositions/news-ticker`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/news-ticker/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/news-ticker/news-ticker.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/news-ticker.mdx`

#### SYNC-123 · صيغة توقيت كلمات الترجمة · Word-timed caption transcript format · 📦 بأمر تثبيت
- **ماذا / what:** 15 of the 17 caption components keep an inline word list with start/end seconds (named TRANSCRIPT, WORDS or W, sometimes grouped into GROUPS/BLOCKS lines), so a words.json from any aligner can drive them; caption-blend-difference and caption-camera-follow use their own internal timing.
- **كيف / how:** Replace the TRANSCRIPT/WORDS array in caption-*.html with [{text, start, end}] from your aligner (the platform also ships an ASR path via Parakeet TDT 0.6B v3, CC-BY-4.0, outside this scope); keep data-duration equal to audio length; 30 fps root.
- **أرقام / params:** TRANSCRIPT [{text:"Every", start:0.0, end:0.3}, ...]; data-fps 30; 1920x1080
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-pill-karaoke/caption-pill-karaoke.html:153` · `kosif-one/vendor/hyperframes/CREDITS.md`

#### SYNC-124 · توهج الكلمات المفتاحية مع توقيت الكلام · ASR keyword glow synced to word timestamps · 📦 بأمر تثبيت
- **ماذا / what:** Words glow, scale and change color when spoken, using an attack-sustain-release envelope over per-word {start,end} timestamps driving a --glow CSS variable.
- **كيف / how:** Read hyperframes-animation/rules/asr-keyword-glow.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** one linear driver (ease none, must not change); envelope 0 before start, linear attack, sustain, release to REST_LEVEL
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/asr-keyword-glow.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### SYNC-125 · ما لا تغطيه أدوات الصوت · Not covered by shipped audio tools · 📦 بأمر تثبيت
- **ماذا / what:** No proper de-essing, noise removal or tone match; no automatic waveform sync or drift correction.
- **كيف / how:** Say so and offer alternatives.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-audio/references/presets.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-audio/SKILL.md`

#### SYNC-126 · مكونات الترجمة في المكتبة · Registry caption components · 📦 بأمر تثبيت
- **ماذا / what:** Named caption treatments: caption-blend-difference, caption-camera-follow, caption-clip-wipe, caption-editorial-emphasis, caption-emoji-pop, caption-glitch-rgb, caption-gradient-fill, caption-highlight, caption-kinetic-slam, caption-matrix-decode, caption-neon-accent, caption-neon-glow, caption-para…
- **كيف / how:** npx hyperframes add <caption-component>; `hyperframes add captions` installs every caption-tagged block.
- **أرقام / params:** 17 caption components
- **تثبيت / install:** `npx hyperframes add <caption-component>`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components` · `kosif-one/vendor/hyperframes/skills/hyperframes-registry/SKILL.md`

#### SYNC-127 · كتل الشريط السفلي · Registry lower-third blocks · 📦 بأمر تثبيت
- **ماذا / what:** lt-accent-underline, lt-bold-block, lt-clean-bar, lt-color-block, lt-dark-card, lt-kicker-name, lt-mask-reveal, lt-neon-border, lt-side-rule, lt-soft-pill, lt-stack-bars, lower-third-bild, yt-lower-third.
- **كيف / how:** npx hyperframes add lt-*.
- **أرقام / params:** 13 lower thirds
- **تثبيت / install:** `npx hyperframes add lt-*`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks`

#### SYNC-128 · التفريغ النصي بتوقيت الكلمات · Transcription with word timestamps (Parakeet / whisper.cpp) · 📦 بأمر تثبيت
- **ماذا / what:** Word-timed transcript {text, words:[{text,start,end}]}; default NVIDIA Parakeet-TDT (25 European languages, avg WER ~6.05%) falling back to whisper.cpp (99 languages).
- **كيف / how:** node <skill>/scripts/transcribe.mjs --input talk.mp4 --out talk.transcribe.json; or npx hyperframes transcribe talk.mp4 --engine auto|parakeet|whisper; models install parakeet (~640 MB).
- **أرقام / params:** Arabic must go through whisper: --model small|medium|large-v3 --language ar (never .en models)
- **تثبيت / install:** `npx hyperframes transcribe talk`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/references/operations.md` · `kosif-one/vendor/hyperframes/skills/media-use/scripts/transcribe.mjs` · `kosif-one/vendor/hyperframes/skills/media-use/scripts/transcribe.test.mjs`

#### SYNC-129 · قاعدة اللغة وأحجام نماذج Whisper · Whisper language rule and model sizes · 📦 بأمر تثبيت
- **ماذا / what:** .en models translate non-English to English silently; known non-English uses --model small --language <iso>; sizes tiny 75 MB, base 142 MB, small 466 MB, medium 1.5 GB, large-v3 3.1 GB; music with vocals start medium.
- **كيف / how:** Always pass --model explicitly (CLI default small.en).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/audio/references/transcribe.md`

#### SYNC-130 · من الصوت المولد إلى الترجمة · TTS to captions (word timing paths) · 📦 بأمر تثبيت
- **ماذا / what:** Path A: HeyGen returns word timestamps in one call; Path B: Gemini/ElevenLabs/Kokoro audio then transcription for timings.
- **كيف / how:** audio/references/tts-to-captions.md.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/audio/references/tts-to-captions.md`

#### SYNC-131 · قواعد تأليف الترجمة · Caption authoring doctrine · 📦 بأمر تثبيت
- **ماذا / what:** Style detection from transcript (visual feel, palette, font mood, animation); per-word emphasis for brands, ALL CAPS, numbers, emotional words, CTAs; tone table: hype 72-96 px heavy 800-900 scale-pop back.out(1.7) 0.1-0.2 s; corporate 56-72 px fade+slide power3.out 0.3 s; tutorial 48-64 px typewrite…
- **كيف / how:** audio/references/captions/authoring.md; groups 2-3 words (high energy), 3-5 (conversational), 4-6 (calm); break on sentences or 150 ms+ pauses; landscape bottom 80-120 px; portrait ~600-700 px from bottom; one group visible; caption exit guarantee.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/audio/references/captions/authoring.md`

#### SYNC-132 · سلم طاقة الترجمة المتحركة · Dynamic caption energy ladder + audio-reactive captions · 📦 بأمر تثبيت
- **ماذا / what:** Karaoke highlight baseline at every energy; high = accent glow + 15% scale pop, scatter/drop exits; low = warm white shift + 3% scale, collapse exit; music sources must modulate caption intensity from extracted audio bands.
- **كيف / how:** audio/references/captions/motion.md; alternate highlight styles every 2-4 groups.
- **أرقام / params:** 15% vs 3% scale
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/audio/references/captions/motion.md`

#### SYNC-133 · ترجمة مدمجة: شريط سفلي وكلمة ذروة خلف المتحدث · Embedded captions workflow (rail + embed behind subject) · 📦 بأمر تثبيت
- **ماذا / what:** Adds captions to an untouched single-subject talking-head clip: drop filler, verbatim lower-third rail in front, and a scarce 'embed' peak word composited behind the subject via a matte (<=1 hero per thought block, >=0.6 s air between heroes).
- **كيف / how:** Decision gate -> pick ONE of 35 identities from CATALOG.md -> `hyperframes init` -> `bash scripts/prepare.sh <project>` (matte || transcribe || audio-envelope, then safe-zones) -> author theme.json or cinematic.json -> `node scripts/preview-frames.cjs <project>` -> render-and-composite.sh / render-theme.sh -> final.mp4.
- **أرقام / params:** 35 identities (10 classic DNA + 25 themes); default 'anchor'
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/SKILL.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-134 · تفريغ بتوقيت الكلمات للترجمة · Word-level transcription for captions · 📦 بأمر تثبيت
- **ماذا / what:** Native Whisper through the hyperframes CLI producing transcript.json word timings; warns on near-silent audio.
- **كيف / how:** node scripts/transcribe.cjs <project>; WHISPER_MODEL=medium override.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/transcribe.cjs` · `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/transcribe.test.mjs`

#### SYNC-135 · منحنى الجهارة كل 50 مللي ثانية · RMS loudness envelope (50 ms) · 📦 بأمر تثبيت
- **ماذا / what:** Per-50 ms RMS envelope of the source audio so hero entrance amplitude follows how hard a word was spoken.
- **كيف / how:** node scripts/audio-envelope.cjs <project> -> envelope.json.
- **أرقام / params:** 50 ms hop
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/audio-envelope.cjs`

#### SYNC-136 · مترجم الثيمات للترجمة · Theme compiler (make-theme.cjs) · 📦 بأمر تثبيت
- **ماذا / what:** Compiles a theme DNA (fonts, palette, body paradigm rail/panel/poem/takeover, hero, plate reactions, linkages) + transcript into the caption composition, then renders and applies plate reactions.
- **كيف / how:** author theme.json -> node scripts/make-theme.cjs -> bash scripts/render-theme.sh <project> -> final_fx.mp4.
- **أرقام / params:** 8621-line compiler
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/make-theme.cjs` · `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/make-theme.test.mjs` · `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/render-theme.sh`

#### SYNC-137 · مترجم الوضع السينمائي · Cinematic compiler (make-cinematic.cjs + DNA engine) · 📦 بأمر تثبيت
- **ماذا / what:** Thought-blocks (lines of words, plane, at most one hero) in cinematic.json compile to plan.json then index.html through the DNA engine; fill-timings fixes word times by sequence; fit-fonts shrinks overflowing groups pre-render.
- **كيف / how:** node scripts/make-cinematic.cjs <project>; scripts/fill-timings.cjs; scripts/fit-fonts.cjs; scripts/make-composition.cjs.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/make-cinematic.cjs` · `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/make-composition.cjs` · `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/fill-timings.cjs`

#### SYNC-138 · مفردات حركة دخول الكلمات العشر · Caption word-entry motion vocabulary (10 moves) · 📦 بأمر تثبيت
- **ماذا / what:** typewriter, word-fade-up (default), word-pop, swipe-reveal, drop-and-settle, etch, crosshair, breathing-hold, cascade, burn-in; tone table: documentary 150 ms stagger / 600 ms hold (burn-in 70% + fade-up 30%), conversational 80/400 fade-up, energetic 50/300 pop, poetic 250/1200 etch, broadcast burn-…
- **كيف / how:** references/motion-vocabulary.md -> GSAP parameters.
- **أرقام / params:** see what
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/references/motion-vocabulary.md`

#### SYNC-139 · نبرة الترجمة: ناعمة أو حاضرة · Caption tone field soft vs present · 📦 بأمر تثبيت
- **ماذا / what:** soft = fade + 8 px y drift power2.out (memory, intro, dream); present = 6 px y + 1.04 scale pop power3.out (emphasis, crown); auto-pick by superlatives, discourse markers, dream vocabulary, final crown line (one per video).
- **كيف / how:** references/typography-presets.md.
- **أرقام / params:** 8 px / 6 px + 1.04
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/references/typography-presets.md`

#### SYNC-140 · قواعد تجميع كلمات الترجمة · Caption grouping rules · 📦 بأمر تثبيت
- **ماذا / what:** Break groups on sentence boundaries, pauses and max word counts; time groups from word start/end; editorial surgery allowed.
- **كيف / how:** references/caption-grouping.md.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/references/caption-grouping.md`

#### SYNC-141 · هوية ترجمة: cream · Caption identity (DNA): cream · 📦 بأمر تثبيت
- **ماذا / what:** Scene-embedded column-flow caption language 'cream': warm poetic light, emergence + glow; dark/mid warm scenes (band luma < 150).
- **كيف / how:** Pick in CATALOG.md; author cinematic.json with dna 'cream'; compile via make-cinematic.cjs; accent/shadow/blur adapt to the scene.
- **أرقام / params:** Inter, warm cream, screen blend
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/cream.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/README.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-142 · هوية ترجمة: ink · Caption identity (DNA): ink · 📦 بأمر تثبيت
- **ماذا / what:** Scene-embedded column-flow caption language 'ink': letterpress printed on bright surfaces (band luma > 150).
- **كيف / how:** Pick in CATALOG.md; author cinematic.json with dna 'ink'; compile via make-cinematic.cjs; accent/shadow/blur adapt to the scene.
- **أرقام / params:** Inter near-black, multiply blend
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/ink.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/README.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-143 · هوية ترجمة: editorial · Caption identity (DNA): editorial · 📦 بأمر تثبيت
- **ماذا / what:** Scene-embedded column-flow caption language 'editorial': lowercase italic serif hero, magazine elegance.
- **كيف / how:** Pick in CATALOG.md; author cinematic.json with dna 'editorial'; compile via make-cinematic.cjs; accent/shadow/blur adapt to the scene.
- **أرقام / params:** Bodoni Moda, bone
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/editorial.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/README.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-144 · هوية ترجمة: keynote · Caption identity (DNA): keynote · 📦 بأمر تثبيت
- **ماذا / what:** Scene-embedded column-flow caption language 'keynote': confident centered slides-in-the-scene; line-wipe reveals, hero wipes up.
- **كيف / how:** Pick in CATALOG.md; author cinematic.json with dna 'keynote'; compile via make-cinematic.cjs; accent/shadow/blur adapt to the scene.
- **أرقام / params:** Inter 800 opaque white
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/keynote.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/README.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-145 · هوية ترجمة: documentary · Caption identity (DNA): documentary · 📦 بأمر تثبيت
- **ماذا / what:** Scene-embedded column-flow caption language 'documentary': burn-in stillness, bone on charcoal, no hero.
- **كيف / how:** Pick in CATALOG.md; author cinematic.json with dna 'documentary'; compile via make-cinematic.cjs; accent/shadow/blur adapt to the scene.
- **أرقام / params:** Inter, bone
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/documentary.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/README.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-146 · هوية ترجمة: loud · Caption identity (DNA): loud · 📦 بأمر تثبيت
- **ماذا / what:** Scene-embedded column-flow caption language 'loud': percussion type competing with the face; single-unit slam + ripple; body in front.
- **كيف / how:** Pick in CATALOG.md; author cinematic.json with dna 'loud'; compile via make-cinematic.cjs; accent/shadow/blur adapt to the scene.
- **أرقام / params:** Anton, scene-sampled accent
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/loud.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/README.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-147 · هوية ترجمة: neon · Caption identity (DNA): neon · 📦 بأمر تثبيت
- **ماذا / what:** Scene-embedded column-flow caption language 'neon': captions as neon signage, flicker-ignite, hero powers on with strobe (glow 0.5).
- **كيف / how:** Pick in CATALOG.md; author cinematic.json with dna 'neon'; compile via make-cinematic.cjs; accent/shadow/blur adapt to the scene.
- **أرقام / params:** Orbitron, electric cyan
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/neon.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/README.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-148 · هوية ترجمة: glitch · Caption identity (DNA): glitch · 📦 بأمر تثبيت
- **ماذا / what:** Scene-embedded column-flow caption language 'glitch': corrupted-feed RGB-split echo layers converge on each beat, 0.10-0.12 s percussion.
- **كيف / how:** Pick in CATALOG.md; author cinematic.json with dna 'glitch'; compile via make-cinematic.cjs; accent/shadow/blur adapt to the scene.
- **أرقام / params:** Space Grotesk
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/glitch.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/README.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-149 · هوية ترجمة: chrome · Caption identity (DNA): chrome · 📦 بأمر تثبيت
- **ماذا / what:** Scene-embedded column-flow caption language 'chrome': liquid-metal gradient hero with one sheen sweep.
- **كيف / how:** Pick in CATALOG.md; author cinematic.json with dna 'chrome'; compile via make-cinematic.cjs; accent/shadow/blur adapt to the scene.
- **أرقام / params:** Audiowide, background-clip text
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/chrome.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/README.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-150 · هوية ترجمة: velocity · Caption identity (DNA): velocity · 📦 بأمر تثبيت
- **ماذا / what:** Scene-embedded column-flow caption language 'velocity': every word arrives along its motion vector with streak + skew, hero speed-trail echoes.
- **كيف / how:** Pick in CATALOG.md; author cinematic.json with dna 'velocity'; compile via make-cinematic.cjs; accent/shadow/blur adapt to the scene.
- **أرقام / params:** Teko italic
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/velocity.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/dna/README.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-151 · هوية ترجمة (ثيم): anchor · Caption identity (theme): anchor · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'anchor' (calm register): verbatim fade-up rail + one settled climax with drawn accent underline (default).
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/anchor.json; run render-theme.sh.
- **أرقام / params:** Sora; #F2EFE9 / accent #D9B98C
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/anchor.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-152 · هوية ترجمة (ثيم): ordnance · Caption identity (theme): ordnance · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'ordnance' (loud register): stamped military-marking rail + detonation apex; room reacts.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/ordnance.json; run render-theme.sh.
- **أرقام / params:** Anton + Space Grotesk; #EDE6D8 / hot #FFB347
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/ordnance.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-153 · هوية ترجمة (ثيم): terminal · Caption identity (theme): terminal · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'terminal' (creator-tech register): typed console panel + glyph-decode apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/terminal.json; run render-theme.sh.
- **أرقام / params:** VT323 + Orbitron; #bfeefe / #66e0ff / #ff5fd6
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/terminal.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-154 · هوية ترجمة (ثيم): neonsign · Caption identity (theme): neonsign · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'neonsign' (creator-warm register): warm tube rail + hand-written neon apex drawn stroke by stroke.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/neonsign.json; run render-theme.sh.
- **أرقام / params:** Space Grotesk + Hershey; #ffe9d6 / #ff3fae
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/neonsign.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-155 · هوية ترجمة (ثيم): stardust · Caption identity (theme): stardust · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'stardust' (poetic register): accumulating poem; letters condense from dust and return.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/stardust.json; run render-theme.sh.
- **أرقام / params:** Cormorant Garamond; #f7f0dd
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/stardust.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-156 · هوية ترجمة (ثيم): stomp · Caption identity (theme): stomp · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'stomp' (takeover register): full-frame hard-cut typographic takeover cards with a void before the drop.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/stomp.json; run render-theme.sh.
- **أرقام / params:** Anton; #F5F1E8 / #FF5C39
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/stomp.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-157 · هوية ترجمة (ثيم): lastpage · Caption identity (theme): lastpage · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'lastpage' (literary-prophetic register): manuscript rail + blurred future-field revealed by one rack focus.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/lastpage.json; run render-theme.sh.
- **أرقام / params:** Cormorant Garamond; #F0E9D8
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/lastpage.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-158 · هوية ترجمة (ثيم): scoreboard · Caption identity (theme): scoreboard · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'scoreboard' (loud register): split-flap chyron rail flip-cycling wrong words before clacking onto the real one + departures-board apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/scoreboard.json; run render-theme.sh.
- **أرقام / params:** Teko + Anton; #F5EEDD / #FFB347
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/scoreboard.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-159 · هوية ترجمة (ثيم): transit · Caption identity (theme): transit · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'transit' (loud register): amber dot-matrix LED departure strip, column-by-column illumination wipe.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/transit.json; run render-theme.sh.
- **أرقام / params:** VT323; #FFB000 / green #36E57A
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/transit.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-160 · هوية ترجمة (ثيم): vhs · Caption identity (theme): vhs · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'vhs' (retro-analog register): camcorder OSD rail (PLAY, REC, blinking timestamp) + REC-freeze tracking-slam apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/vhs.json; run render-theme.sh.
- **أرقام / params:** VT323; #F2F2EE / red #FF2E2E
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/vhs.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-161 · هوية ترجمة (ثيم): arcade · Caption identity (theme): arcade · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'arcade' (loud register): 8-bit attract-mode HUD rail with CRT scanlines + pixel-block boss-intro apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/arcade.json; run render-theme.sh.
- **أرقام / params:** Press Start 2P; #00E5FF / #FF2E88 / #FFE600
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/arcade.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-162 · هوية ترجمة (ثيم): dossier · Caption identity (theme): dossier · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'dossier' (archival-noir register): manila case-file strip typed char by char + rubber-stamp apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/dossier.json; run render-theme.sh.
- **أرقام / params:** Special Elite; paper #d8c49a / stamp red #b3271e
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/dossier.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-163 · هوية ترجمة (ثيم): laser · Caption identity (theme): laser · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'laser' (loud register): words ignited where green and magenta beams converge + 6-beam laser-cage apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/laser.json; run render-theme.sh.
- **أرقام / params:** Audiowide; #58ff9d / #ff4df0
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/laser.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-164 · هوية ترجمة (ثيم): thunder · Caption identity (theme): thunder · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'thunder' (loud register): slate storm grade, slanted rain in front of subject, branched-bolt strike apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/thunder.json; run render-theme.sh.
- **أرقام / params:** Sora + Anton; #EEF4FB / #9FD0FF
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/thunder.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-165 · هوية ترجمة (ثيم): hologram · Caption identity (theme): hologram · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'hologram' (sleek register): volumetric projection plate with scanlines + hologram-boot apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/hologram.json; run render-theme.sh.
- **أرقام / params:** Orbitron; #C7F1FF / #7AE8FF / #FF5FD6
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/hologram.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-166 · هوية ترجمة (ثيم): biolume · Caption identity (theme): biolume · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'biolume' (dreamy register): abyss grade with breathing vignette, living bioluminescent captions + bloom apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/biolume.json; run render-theme.sh.
- **أرقام / params:** Fredoka; #E9FFFA / #6DF2E0 / #9D7BFF
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/biolume.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-167 · هوية ترجمة (ثيم): aurora · Caption identity (theme): aurora · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'aurora' (elegant register): two aurora blobs drift, silk serif rail with rose-to-teal sheen + ribbon draw-on apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/aurora.json; run render-theme.sh.
- **أرقام / params:** Cormorant Garamond + Hershey; #FF9EC4 / #7FE0D4 / #B9A8FF
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/aurora.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-168 · هوية ترجمة (ثيم): spectrum · Caption identity (theme): spectrum · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'spectrum' (tech-retro register): always-alive oscilloscope scope band + phosphor trace-write apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/spectrum.json; run render-theme.sh.
- **أرقام / params:** VT323 + Hershey; #4dff88
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/spectrum.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-169 · هوية ترجمة (ثيم): papercut · Caption identity (theme): papercut · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'papercut' (playful register): stop-motion paper chips placed one by one + papermat apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/papercut.json; run render-theme.sh.
- **أرقام / params:** Inter + Anton + Caveat; #ff4f3f on #f6edd8
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/papercut.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-170 · هوية ترجمة (ثيم): popup · Caption identity (theme): popup · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'popup' (playful register): pop-up book page: words pop up on a hinge (rotationX back.out) + centerfold starburst.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/popup.json; run render-theme.sh.
- **أرقام / params:** Baloo 2; #33271a / #6cb6e3
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/popup.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-171 · هوية ترجمة (ثيم): chalkboard · Caption identity (theme): chalkboard · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'chalkboard' (scholarly-warm register): deep-green chalk band, words scribbled (2-frame pop + steps(4)) + chalkwrite apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/chalkboard.json; run render-theme.sh.
- **أرقام / params:** Caveat + Hershey; #f3f6ee / #f3d96b on #1d3328
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/chalkboard.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-172 · هوية ترجمة (ثيم): graffiti · Caption identity (theme): graffiti · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'graffiti' (loud-street register): marker words flick onto a crooked rail + spray-tagged handstyle apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/graffiti.json; run render-theme.sh.
- **أرقام / params:** Permanent Marker + Hershey; #ffd23f / #ff2e88
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/graffiti.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-173 · هوية ترجمة (ثيم): brush · Caption identity (theme): brush · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'brush' (contemplative-elegant register): washi paper band, words brush-wiped behind a traveling brush shadow + sumi-e gesture apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/brush.json; run render-theme.sh.
- **أرقام / params:** Shippori Mincho + Hershey; sumi #19120b on washi
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/brush.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-174 · هوية ترجمة (ثيم): inkwater · Caption identity (theme): inkwater · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'inkwater' (contemplative-still register): three-row ink rail, Mincho words bleed into paper washes + ink-drop bloom apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/inkwater.json; run render-theme.sh.
- **أرقام / params:** Shippori Mincho; #14110e on #fffaee
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/inkwater.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-175 · هوية ترجمة (ثيم): ransom · Caption identity (theme): ransom · 📦 بأمر تثبيت
- **ماذا / what:** Theme 'ransom' (loud-collage register): every word a chip cut from a different page + ransom-note slam apex.
- **كيف / how:** Shortlist via CATALOG.md heuristics; author theme.json from themes/ransom.json; run render-theme.sh.
- **أرقام / params:** Anton + Inter + Special Elite + Permanent Marker; #ffd23f accent
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/ransom.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`

#### SYNC-176 · فئة موشن: الأشرطة السفلية · Motion-graphics category: Lower thirds & overlays · 📦 بأمر تثبيت
- **ماذا / what:** Category module: name/title bars, callouts, social overlays ~3-6 s, transparent export.
- **كيف / how:** Director sets category 'lower-thirds' in shot-plan.json; builder follows motion-graphics/categories/lower-thirds/module.md reuse-first.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/lower-thirds/module.md` · `kosif-one/vendor/hyperframes/skills/motion-graphics/SKILL.md`

#### SYNC-177 · بناء مسار الترجمة بجلد القالب · Caption track builder with preset skins · 📦 بأمر تثبيت
- **ماذا / what:** Builds compositions/captions.html from STORYBOARD frame durations and audio_meta word timings into absolute caption groups using the preset caption-skin (or a default pill) with brand tokens; snug line-height 1.1 pill.
- **كيف / how:** node <skill>/scripts/captions.mjs build --storyboard STORYBOARD.md --audio-meta audio_meta.json --hyperframes . --out caption_groups.json.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/faceless-explainer/scripts/captions.mjs` · `kosif-one/vendor/hyperframes/skills/faceless-explainer/scripts/captions.test.mjs` · `kosif-one/vendor/hyperframes/skills/pr-to-video/scripts/captions.test.mjs`

#### SYNC-178 · التفريغ الصوتي · transcribe Whisper · 📦 بأمر تثبيت
- **ماذا / what:** faster-whisper word times → words.json, .srt, captions.json; VAD; batched decoding; openai-whisper fallback.
- **كيف / how:** python scripts/kmotion.py transcribe CLIP.mp4 --model large-v3|auto
- **أرقام / params:** batched 3–4x on CPU (≥1.1)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### SYNC-179 · ترجمة كلام تظهر على المقاطع المنطوقة · Syllable-timed speech caption · 📦 بأمر تثبيت
- **ماذا / what:** Each word of a spoken line appears on its own timestamp with a short rise and blur-to-sharp; chosen keywords switch to the accent colour.
- **كيف / how:** speech(el, [[word, t], …], accentWords): wrap each word in .wm (clip-path inset mask) > .w; tl.fromTo(word, {y:18, opacity:0, blur 6px}, {y:0, opacity:1, blur 0, 0.28 s, power3.out}, t − 0.04); exit out(el, at, 0.22): opacity 0, y −14, power3.in.
- **أرقام / params:** rise 18 px, blur 6 px, 0.28 s, lead 0.04 s; accent #E7B65A
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:171` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:197`

#### SYNC-180 · بطاقات إنفوجرافيك دلالية من الصوت · Voice2Motion semantic infographic cards · 📦 بأمر تثبيت
- **ماذا / what:** A voice message becomes a vertical motion piece: each cue kind gets its own graphic (weather sun with temperature card, perspective road with cars and 'leave 10 min early', support ticket with duplicate charges, refund check ring with progress dots), a caption box with live waveform bars, header wit…
- **كيف / how:** assistant.cues.json [{start, end, text, kind: weather|traffic|support|refund}] → kmotion audio2motion voice.wav --cues …; output 720×1280 30 fps 865 frames 28.84 s; QA report with voice correlation.
- **أرقام / params:** dark navy bg, cyan accents, amber/red/mint status colours
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/examples/voice2motion/assistant.cues.json` · `100-superskills/skills/kosif-montage-motion/examples/voice2motion/storyboard.jpg` · `100-superskills/skills/kosif-montage-motion/examples/voice2motion/qa_report.json`

#### SYNC-181 · معيار الصوت -14 · Loudness target EBU R128 -14 LUFS · 📦 بأمر تثبيت
- **ماذا / what:** Platform master loudness and true peak.
- **كيف / how:** two-stage loudnorm + limiter in timeline/motion mux
- **أرقام / params:** -14 LUFS; -1.0 dBTP (timeline default TP -1.5)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/montage_grammar.md` · `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md` · `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### SYNC-182 · ترجمة كاريوكي · Karaoke word highlight · 📦 بأمر تثبيت
- **ماذا / what:** Spoken word lit in accent colour while rest stays white.
- **كيف / how:** kmotion captions / timeline captions overlay
- **أرقام / params:** #FFDE59 yellow or #38BDF8 cyan on white
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/montage_grammar.md` · `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`

#### SYNC-183 · فيلم من الصوت · Verse / audio2motion · 📦 بأمر تثبيت
- **ماذا / what:** Film from voice/song/dua/poem with symbols by meaning, counters.
- **كيف / how:** kmotion verse AUDIO | audio2motion AUDIO
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/operating-manual.md` · `100-superskills/skills/kosif-montage-motion/scripts/verse.py` · `100-superskills/skills/kosif-montage-motion/scripts/audio2motion.py`

#### SYNC-184 · ريل كلمات أغنية · Songreel lyric reel · 📦 بأمر تثبيت
- **ماذا / what:** Structure analysis, per-section queries/grade, Pinterest pool, cut, build with whisper large-v3.
- **كيف / how:** songreel analyze SONG --name --lyrics; cut N --media; build N --model large-v3 --draft/--render
- **أرقام / params:** --seconds 45 typical; reject <360p clips
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/operating-manual.md` · `100-superskills/skills/kosif-montage-motion/scripts/songreel.py` · `100-superskills/skills/kosif-montage-motion/tests/test_songreel.py`

#### SYNC-185 · ستايل ترجمة كاريوكي: تيك توك · Karaoke caption style: TikTok · 📦 بأمر تثبيت
- **ماذا / what:** Burned-in ASS subtitle style where each word gets an equal \k karaoke slice; libass shapes Arabic RTL correctly (checked here with a fallback font).
- **كيف / how:** python scripts/smart_montage.py captions video.mp4 --spec captions.json --style tiktok; captions.json = [{start,end,text,words[]}]; writes video.ass (PlayRes 1080x1920) and burns with ffmpeg -vf ass=. Note: words not yet spoken show the secondary colour and turn primary when reached; timing is split evenly, not from real word timestamps — feed words.json times to get true sync.
- **أرقام / params:** Cairo 68, white primary &H00FFFFFF, yellow secondary &H0000FFFF, black outline 6, shadow 8, back &H80000000, bold, bottom-centre, margins L/R 40, MarginV 280; \k per word = max(10 cs, duration/len(words))
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/smart_montage.py:91` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/smart_montage.py:81` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/montage_grammar.md`

#### SYNC-186 · صوت التلاوة فقط بنفس العلو · Voice-only audio with reference loudness · 📦 بأمر تثبيت
- **ماذا / what:** For a supplication reel the clips are muted and only the reference voice is kept, mastered to the reference's measured loudness instead of a generic target.
- **كيف / how:** audio {music:false, voice:true, sfx:0, duck:'none', keep_clip_audio:false, lufs:-12.75, measured_lufs:-12.75}.
- **أرقام / params:** -12.75 LUFS
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/mimic-jumuah/جمعة-محاكاة.raw.timeline.json` · `kosif-one/projects/mimic-jumuah/study/mimic.timeline.json`

#### SYNC-187 · ستايل ريل كلمات أغنية مشكولة · Song lyric reel of a vocalised poem (style) · 📦 بأمر تثبيت
- **ماذا / what:** A planned lyric reel for the Ghorba song: a fully vowelled Arabic poem (tashkeel on every letter) about an empty chair, a video call with mother and the promise 'سأعود', cut over Pinterest clip pools per section.
- **كيف / how:** kmotion songreel analyze -> words/captions/srt, then queries/cut/build; pins.json lists 30/16/20 pin IDs for sections s08/s09/s10.
- **أرقام / params:** 31 lyric lines; 66 pins
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/songreel-ghorba/lyrics.txt` · `kosif-one/projects/songreel-ghorba/pins.json`

#### SYNC-188 · ظهور الكلمات مع التلاوة · Word-by-word recitation reveal · 📦 بأمر تثبيت
- **ماذا / what:** Each line of the dua appears word by word rising through a mask exactly when it is recited, and leaves upward before the next line.
- **كيف / how:** say(id,at)=M.revealWords(tl,el,at,{dur:.65,stagger:.09,ease:E.out}); off(ids,at)=M.hideWords(...,{dur:.35,stagger:.03}); cue times written from the voice (0.45, 1.95, 4.95, 7.05, 8.0, 10.99, 12.95, 15.9, 16.95, 18.75, 20.0, 21.95, 22.95 s).
- **أرقام / params:** 13 lines in 9 cards; card 780x420 at top 930
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html:198-209`

#### SYNC-189 · تفريغ بتوقيت الكلمات · Word-level ASR timings package (words.json, SRT, words.txt) · 📦 بأمر تثبيت
- **ماذا / what:** Speech transcribed into segments with per-word start/end and confidence, exported as JSON, a two-cue SRT and a plain 'start-end word' list for planning cuts.
- **كيف / how:** words.json [{start,end,text,words:[{text,start,end,p}]}]; voice.srt; words.txt lines '0.50-0.84 بتعمل'.
- **أرقام / params:** 144 words over 44.42 s; mean confidence .866, min .018
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/voice.words.json` · `kosif-one/projects/whatsapp-motion/voice.srt` · `kosif-one/projects/whatsapp-motion/words.txt`

#### SYNC-190 · ترجمة مصححة بكلمات ذهبية · Human-corrected phrase captions with gold keywords · 📦 بأمر تثبيت
- **ماذا / what:** Speech captions phrase by phrase at the bottom; each word rises out of its own mask, the key word(s) of the phrase are gold, and the phrase exits upward just before the next one. Text is rewritten by hand from the raw ASR (fixing misheard Egyptian words).
- **كيف / how:** CAPS=[[start,end,'text with <b>keyword</b>']]; split into masked spans (clip-path inset(-0.1em -0.1em 0 -0.1em)); gold spans #f5c97a; in yPercent 105 -> 0 0.32 s stagger min(.06, 0.5*len/words) E.out; out at next start-0.16 s, yPercent -105 in 0.16 s E.in.
- **أرقام / params:** .cap 50 px bold, top 1400 px, line-height 1.35, shadow 0 4px 18px rgba(0,0,0,.85); 20 phrases
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html:30-32` · `kosif-one/projects/whatsapp-motion/projects/success/index.html:156-205`

#### SYNC-191 · تفريغ بتوقيت الكلمات · Word-timed transcription (faster-whisper) · 📦 بأمر تثبيت
- **ماذا / what:** Speech to words with start/end times offline; writes words.json, an SRT with BOM, and the captions spec.
- **كيف / how:** python transcribe.py VIDEO_OR_AUDIO [--model large-v3|small|base|auto] [--lang ar] [--out DIR].
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/transcribe.py`

#### SYNC-192 · هالة وحلقات تتفاعل مع الصوت · Sound-driven halo, rings and motes · 📦 بأمر تثبيت
- **ماذا / what:** Loudness breathes a halo, kicks swell it and send rings, onsets lift rising motes.
- **كيف / how:** verse.html reads embedded channels (sound.js): R = 0.62*min(W,H)*(1+0.05*rms+0.06*kick+0.25*flare).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/templates/verse.html:86`

#### SYNC-193 · قراءة النص العربي من الفيديو · Arabic OCR draft of on-screen text · 📦 بأمر تثبيت
- **ماذا / what:** OCR draft of reference text lines (Tesseract Arabic data shipped) that a human/Claude then corrects; never invent text.
- **كيف / how:** mm_text.ocr_line with assets/tessdata/ara.traineddata.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_text.py` · `kosif-one/tools/kosif-mimic/assets/tessdata/ara.traineddata`

#### SYNC-194 · قالب المونتاج الموجَّه · Directed edit template (talking footage) · 📦 بأمر تثبيت
- **ماذا / what:** Voice-led edit over a plate video: per-shot slow push on the subject, keyword punches, word-timed speech captions, big keyword slams, number-ring motifs, chapter planes at cuts, payoff with light sweep, credit, dip to black.
- **كيف / how:** direct.py writes edit.js (window.EDIT: W,H,duration,shots,camera,captions,keys,motifs,chapters,payoff,credit,palette,hook,end) -> templates/directed.html; render via shim.
- **أرقام / params:** ivory #F5F0E6, accent #E7B65A; sizes designed at 1080 px wide; caption 54 px, keyword 200 px, chapter 380 px, payoff 92/230 px; punch expo.out .14 s then -60% over .6 s; hook dim .38 -> 0 in .55 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/templates/directed.html`

#### SYNC-195 · كابتشن على المقاطع · Word-on-syllable speech captions · 📦 بأمر تثبيت
- **ماذا / what:** Each spoken word rises from blur exactly at its timestamp; keywords coloured in accent.
- **كيف / how:** speech(words[{text,t,key}], y, size) inside directed.html.
- **أرقام / params:** rise 18·k px, blur 6 px -> 0, .28 s power3.out at t-0.04; exit .2 s up 14 px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/templates/directed.html`

#### SYNC-196 · محرك أفلام الأبيات · Verse film engine (lyric/poem/dua) · 📦 بأمر تثبيت
- **ماذا / what:** Arabic lyric/poem/dua film from a sung or recited track: words rise on their own times, keyword glows, payoff flares the sky, sections step hue, optional per-section photos with slow push.
- **كيف / how:** verse.py writes verse.js (window.VERSE) + sound.js (window.SOUND channels) -> templates/verse.html.
- **أرقام / params:** word rise 30·k px blur 9 -> 0 .42 s; keyword pulse 1.07 yoyo .18 s; line exit -46·k px .45 s; pictures scale 1.04 -> 1.13; title card 128 px, sub 42 px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/templates/verse.html`

#### SYNC-197 · تفريغ الكلام بالكلمات · faster-whisper word transcription · 📦 بأمر تثبيت
- **ماذا / what:** Offline speech → segments with per-word start/end/probability, Arabic by default; batched pipeline when available, openai-whisper fallback, model auto-picked from the local cache.
- **كيف / how:** python transcribe.py SRC [--model large-v3|small|base|auto --lang ar --prompt '...' --out DIR --no-batch]
- **أرقام / params:** 16 kHz mono; CPU int8; beam 5; vad_filter; word_timestamps; BatchedInferencePipeline batch 8 (≈3-4× faster); auto order large-v3 > large-v2 > medium > small > base
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/transcribe.py:36` · `kosif-studio/motion/transcribe.py:47`

#### SYNC-198 · فيلم كلمات من الصوت · Verse film from sound · 📦 بأمر تثبيت
- **ماذا / what:** A kinetic-typography film from a song, poem, dua or voice-over: timing from Whisper (or aligned true text), lines, sections at pauses ≥3 s, interludes ≥4.5 s with a breathing eight-point rosette, one keyword per line, a payoff, symbols by meaning, light driven by the sound, optional pictures per sec…
- **كيف / how:** python verse.py AUDIO --name NAME [--text lyrics.txt --words X.words.json --title --sub --size 1080x1920 --mood night --accent '#E7B65A' --images a.jpg … --music none --credit --model large-v3 --fix --fps 30 --render]
- **أرقام / params:** line size 124/104/88/74 px for ≤14/24/36/more chars; payoff ×1.22, hold +2.2 s (else +1.4); sections ≥1 per picture or per 12 s; title card if first word ≥1.5 s else header ≤6 s; end card if ≥2 s tail
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/verse.py:246` · `kosif-studio/motion/verse.py:394` · `kosif-studio/tests/test_studio.py:943`

#### SYNC-199 · كلمات متحركة · Style: Subtitle punch (subtitle-punch) · 📦 بأمر تثبيت
- **ماذا / what:** Word-by-word punchy captions synced to speech.
- **كيف / how:** words.json timing; each word at start-0.06s; pop 1->1.12->1 280ms spring d12 s180; captions 56-72px. Scaffold: python3 tools/kosif.py scaffold subtitle-punch <dir>.
- **أرقام / params:** <=100ms key words
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:subtitle-punch` · `kosif-tool/playbooks/kinetic-type.md`

#### SYNC-200 · مزامنة صوتية بالكلمة · Word-level audio sync · 📦 بأمر تثبيت
- **ماذا / what:** Voice is master clock; words.json drives every action.
- **كيف / how:** ffprobe duration; whisper --word_timestamps True (or WhisperX); tools/words_convert.py (json/SRT/VTT/CSV) -> words.json; animate at start-0.04..0.08s.
- **أرقام / params:** key words<=100ms, others<=150ms; pause>400ms ends phrase, >600ms scene change, >1.5s needs motion
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md` · `kosif-tool/tools/words_convert.py`

#### SYNC-201 · ترجمة بالكلمة مع كشف الاتجاه · Remotion word-level captions with bidi detection · 📦 بأمر تثبيت
- **ماذا / what:** Loads public/words.json under delayRender, groups into cards by max 4 words or >0.6 s silence, shows a card 0.15 s early and holds 0.35 s; active word turns accent and springs to 1.1x, upcoming words 42% opacity; direction set from first strong character.
- **كيف / how:** <Captions accent lang file maxWordsPerLine=4 gapSeconds=0.6 holdSeconds=0.35 leadSeconds=0.15/>; spring damping 12 stiffness 220 mass .7
- **أرقام / params:** 58 px 700 lh 1.45 white on rgba(8,10,16,.66) radius 30 padding 20x38, bottom 260 px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/starters/remotion/src/Captions.tsx:135` · `kosif-tool/starters/remotion/src/Captions.tsx:39` · `kosif-tool/starters/remotion/src/Captions.tsx:64`

#### SYNC-202 · الصوت كساعة رئيسية في Remotion · Audio as master clock in Remotion · 📦 بأمر تثبيت
- **ماذا / what:** Put voice in public/, set AUDIO_FILE, it mounts <Audio> at frame 0; optional calculateMetadata with getAudioDurationInSeconds makes durationInFrames follow the voice.
- **كيف / how:** const AUDIO_FILE='voice.mp3'; npm install @remotion/media-utils@4.0.535
- **أرقام / params:** Math.ceil(seconds*FPS)
- **تثبيت / install:** `npm install @remotion/media-utils@4`
- **الدليل / proof:** `kosif-tool/starters/remotion/src/Film.tsx:32` · `kosif-tool/starters/remotion/README.md`

#### SYNC-203 · إبراز الكلمة المتزامن في Remotion · Remotion synced word highlight · 📦 بأمر تثبيت
- **ماذا / what:** Find active word from frame time and colour it.
- **كيف / how:** words.findIndex(w=> t>=w.start-0.06 && t<w.end); <Audio src=staticFile('voice.mp3')>.
- **أرقام / params:** highlight #7ee8d2 on #fff, 64 px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:59-70`

#### SYNC-204 · سطر متزامن في Remotion · Remotion SyncedLine · 📦 بأمر تثبيت
- **ماذا / what:** Whole words spring in at start−0.06 s and turn accent while spoken.
- **كيف / how:** spring {damping 200, durationInFrames 12}; translateY 50→0; dir rtl; 96 px 800 weight; colours #7ee8d2/#f3f7ff; html-canvas: KOSIF.prog(t, w.start-0.06, w.start+0.34, Ease.outQuint).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/kinetic-type.md:57-75`

#### SYNC-205 · تفريغ سحابي مع تمييز المتحدثين · Cloud STT with diarisation · 🔑 مفتاح/خدمة
- **ماذا / what:** When speaker labels or very fast turnaround are needed, use hosted ASR: Deepgram nova-3 (smart_format, diarize, utterances), ElevenLabs scribe_v1 (diarize + word timestamps), AssemblyAI /v2/transcript (speech_models, speaker labels), Together (openai/whisper-large-v3, nvidia/parakeet-tdt-0.6b-v3 wit…
- **كيف / how:** SDK call with API key; normalise output to [{text,start,end,speaker}]
- **الدليل / proof:** `kosif-atlas/skills/1845-deepgram-pack/5473-deepgram-hello-world/SKILL.md` · `kosif-atlas/skills/1847-elevenlabs-pack/5515-elevenlabs-core-workflow-b/SKILL.md` · `kosif-atlas/skills/1828-assemblyai-pack/5094-assemblyai-core-workflow-a/SKILL.md`

#### SYNC-206 · تفريغ Scribe مع فصل المتحدثين · ElevenLabs Scribe STT with diarization · 🔑 مفتاح/خدمة
- **ماذا / what:** Cloud transcription with word timestamps and speaker labels.
- **كيف / how:** speechToText.convert({audio,model_id:'scribe_v1',diarize:true}); per audio minute.
- **الدليل / proof:** `kosif-atlas/skills/1847-elevenlabs-pack/5515-elevenlabs-core-workflow-b`

#### SYNC-207 · تفريغ عبر Together · Together Whisper/Parakeet STT · 🔑 مفتاح/خدمة
- **ماذا / what:** Hosted whisper-large-v3 / Parakeet with translation, diarization, word timings, realtime.
- **كيف / how:** client.audio.transcriptions.create(file,model='openai/whisper-large-v3',timestamp granularities).
- **أرقام / params:** 80MB upload, 1GB URL, 4h/request
- **الدليل / proof:** `kosif-atlas/skills/3214-togetherai-skills/13585-together-audio/references/stt-models.md`

#### SYNC-208 · ترجمة بعد التوليد بالتعرف على الكلام · Post-generation ASR captions instead of model-drawn captions · 🔑 مفتاح/خدمة
- **ماذا / what:** Captions for generated clips are made from real speech recognition with word timings after the video exists, never requested in the prompt.
- **كيف / how:** Hosted: quickdesign video subtitle (ElevenLabs ASR + libass) presets default Montserrat 65 px 5 words/line, tiktok 100 px 1 word, minimal Inter 60 px 8 words; locally: whisper/words.json + Remotion or ASS karaoke.
- **أرقام / params:** 65/100/60 px; 5/1/8 words per line
- **الدليل / proof:** `kosif-atlas/skills/259-quickdesign/865-quickdesign` · `kosif-atlas/skills/1446-marketing-skills/3531-video`

#### SYNC-209 · تفريغ محلي ومحاذاة كلمة بكلمة · Local ASR + forced word alignment (bridge) · 🔑 مفتاح/خدمة
- **ماذا / what:** With the local bridge, faster-whisper gives real word times; pasted text is aligned to them with longest-common-subsequence and unmatched words interpolated.
- **كيف / how:** transcribeLocal posts a length-prefixed JSON+file frame to BRIDGE/api/transcribe {model:'small',lang:'ar'}; alignWords(user,asr) builds an LCS table on normalised words, interpolates gaps; rejected below 40% match; capsFromWords breaks at 5 words, >0.35 s pause or end punctuation; words with p<0.5 flagged.
- **أرقام / params:** model small; match >= 0.4; 5 words/line; pause 0.35 s
- **الدليل / proof:** `app/public/js/00_editor.js:2667` · `app/public/js/00_editor.js:2673` · `app/public/js/00_editor.js:2684`

#### SYNC-210 · تفريغ Gemini بالعامية · Gemini verbatim transcription · 🔑 مفتاح/خدمة
- **ماذا / what:** Gemini listens to the uploaded clip and returns timed caption segments in the original language and dialect.
- **كيف / how:** geminiJSON with inlineData (file <= 18 MB) and a prompt for [{start,end,text}] segments of 3-8 words; Studio version AIR.transcribe resamples to 16 kHz mono WAV (toWav16k) and aligns words to a 10 ms energy envelope.
- **أرقام / params:** max 18 MB inline; 3-8 words/segment; 16 kHz mono
- **الدليل / proof:** `app/public/js/00_editor.js:1525` · `app/public/js/10_studio.js:2535` · `app/public/js/50_autoedit.js:201`

#### SYNC-211 · تقسيم الكابشن بذكاء Claude · Claude smart caption splitting · 🔑 مفتاح/خدمة
- **ماذا / what:** Claude splits a transcript into 2-5 word caption lines at natural pauses, never separating prepositions, and stars the single strongest word.
- **كيف / how:** askJSON prompt with rules (keep every word in order, 2-5 words/line, star one word); lines are re-timed with syncToSpeech word estimates.
- **أرقام / params:** 2-5 words/line; transcript cap 8000 chars
- **الدليل / proof:** `app/public/js/00_editor.js:1510`

#### SYNC-212 · فيلم مرسوم على صوت مرفوع · Sound-to-film: film drawn on an uploaded voice or song · 🔑 مفتاح/خدمة
- **ماذا / what:** When a narration, poem or song file is uploaded and a film is requested, the film's words and timings come from the audio itself (transcribed and aligned) instead of a new voice-over.
- **كيف / how:** Agent rule: intent film + voice/song file -> motion_film with voice:false; KIT.build with voiceFile (+timedLines from transcription) sets film length to the exact audio duration; optional Claude animations for 1-4 key lines (FILM.animate, middle band, no text) and Gemini pictures in the style's FILM.LOOK.
- **الدليل / proof:** `app/public/js/10_studio.js:3251` · `app/public/js/10_studio.js:1011` · `app/public/js/10_studio.js:4178`

#### SYNC-213 · كتابة كلمة كلمة مع ظل باهت · Word-by-word ghost caption · 👁 شوهد في فيديو
- **ماذا / what:** render the full Arabic line at ~25% opacity, then raise each word to 100% at its words.json start time; never split letters
- **أرقام / params:** fade 150-200 ms per word; 2 lines max
- **الدليل / proof:** `style:doodle`

#### SYNC-214 · كلمات تضيء مع الصوت · Ghost-to-lit voice caption · 👁 شوهد في فيديو
- **ماذا / what:** show the full sentence in grey #555, switch each word to white (or orange for emphasis) at its word timestamp with a 120 ms fade
- **أرقام / params:** words.json driven; emphasis colour #f27525
- **الدليل / proof:** `style:plotter`

#### SYNC-215 · تظليل الكلمة المنطوقة كالكاريوكي · Karaoke narration highlight · 👁 شوهد في فيديو
- **ماذا / what:** Sentence rendered grey; each word turns ink at its TTS timestamp; current/target word gets a soft peach rounded highlight box
- **أرقام / params:** colour transition 80 ms, highlight padding 2px 6px
- **الدليل / proof:** `style:pm-1stnoel-c20a89`

#### SYNC-216 · كلمات صوتية مكتوبة · Written onomatopoeia tags · 👁 شوهد في فيديو
- **ماذا / what:** Tiny hand-lettered sound words (chirp!, tweet!) with 3-5 radiating tick lines appear at the moment a character calls, scale 0->1 in 120 ms, fade after ~600 ms; pair each with a synthesized sfx
- **أرقام / params:** 16-20 px, rotate ±8°
- **الدليل / proof:** `style:pm-abderrahmen-g-9e8ed0`

#### SYNC-217 · تسمية بكلمة مضيئة · Word-highlight caption · 👁 شوهد في فيديو
- **ماذا / what:** current word coloured, next line greyed
- **الدليل / proof:** `style:pm-ajith-io-c52e09`

#### SYNC-218 · سرد بكبسولة نصية · Caption pill narration · 👁 شوهد في فيديو
- **ماذا / what:** top-centre pill text swaps every ~6 s
- **الدليل / proof:** `style:pm-buildfastwithai-ed9447`

#### SYNC-219 · كرة صوت بأشواك شعاعية · Voice orb radial spikes · 👁 شوهد في فيديو
- **ماذا / what:** sphere with radial lines lengths driven by amplitude
- **أرقام / params:** 64 spikes
- **الدليل / proof:** `style:pm-charlesmendez-73b6e4`

#### SYNC-220 · ترجمة باسم المتحدث · Speaker subtitle · 👁 شوهد في فيديو
- **ماذا / what:** tiny caps speaker name above line, fade in/out
- **الدليل / proof:** `style:pm-faroukzy-9ff23e`

#### SYNC-221 · تمييز الكلمة المنطوقة · Word-hop caption highlight · 👁 شوهد في فيديو
- **ماذا / what:** Bold captions over footage; a rounded purple box slides to the active word using words.json timing
- **أرقام / params:** box pad 6 px, slide 80 ms
- **الدليل / proof:** `style:pm-gautam-mer1-2ae354`

#### SYNC-222 · خط زمني بموجة وكلمات · Waveform scrub timeline · 👁 شوهد في فيديو
- **ماذا / what:** Filmstrip thumbnails + word chips + waveform with fixed centre playhead, content slides left
- **أرقام / params:** speed matches audio
- **الدليل / proof:** `style:pm-gautam-mer1-2ae354`

#### SYNC-223 · ترجمة كاتبة في صندوق · Typewriter subtitle box · 👁 شوهد في فيديو
- **ماذا / what:** mono lowercase text typed 35 ms/char into solid orange or yellow box with underscore cursor
- **أرقام / params:** box padding 6x12px
- **الدليل / proof:** `style:pm-gizakdag-b8c59e`

#### SYNC-224 · تعليقات صوتية بين أقواس · Bracketed sound captions · 👁 شوهد في فيديو
- **ماذا / what:** [SOUND DESCRIPTION] box lower-centre per scene
- **الدليل / proof:** `style:pm-henkpoley-3d3407`

#### SYNC-225 · كلمات مقطعة على الإيقاع · Beat-cut word stack · 👁 شوهد في فيديو
- **ماذا / what:** one huge word per beat, hard cut, small accent word above
- **أرقام / params:** 250-500 ms/word
- **الدليل / proof:** `style:pm-heyiammallik-e72d17`

#### SYNC-226 · ترجمة كاراوكي · Karaoke caption fill · 👁 شوهد في فيديو
- **ماذا / what:** caption line in grey, current word coloured blue, past words dark; driven by words.json
- **الدليل / proof:** `style:pm-itisrazak-3ad902`

#### SYNC-227 · شريط تعليق أسود كراوٍ صامت · Caption pill narrator · 👁 شوهد في فيديو
- **ماذا / what:** Black rounded pill near the bottom with one short line per beat; one key word coloured in brand accent; swap with fade/slide
- **أرقام / params:** pill radius 999, padding 10/22 px, swap 250 ms
- **الدليل / proof:** `style:pm-justincooperman-e7bbc4`

#### SYNC-228 · سطر ترجمة وثائقي · Documentary subtitle line · 👁 شوهد في فيديو
- **ماذا / what:** one sentence centred bottom, fades per scene
- **الدليل / proof:** `style:pm-kloss-xyz-fe0c31`

#### SYNC-229 · بطاقة ترجمة ثنائية اللغة · Bilingual subtitle card · 👁 شوهد في فيديو
- **ماذا / what:** white rounded card bottom-centre with soft shadow: line 1 handwritten English, line 2 smaller second language; swap per sentence at voice timestamps
- **أرقام / params:** card radius 8 px, padding 12 px
- **الدليل / proof:** `style:pm-lemomo-ai-0d9cff`

#### SYNC-230 · ترجمة متزامنة مع التعليق الآلي · Sentence-synced subtitles with TTS · 👁 شوهد في فيديو
- **ماذا / what:** generate TTS per sentence, measure each clip, set scene wait = clip duration; burn subtitle box at bottom centre per sentence
- **أرقام / params:** subtitle ~3% H, dark box 70% opacity, bottom margin ~5%
- **الدليل / proof:** `style:pm-linearuncle-5d2bae`

#### SYNC-231 · شريط ترجمة ملصوق بكتابة حرفية · Taped caption strip typewriter · 👁 شوهد في فيديو
- **ماذا / what:** Off-white card with two translucent masking-tape corners on dark bottom band; text reveals letter by letter at ~25 chars/s
- **أرقام / params:** card 88% width, tape #e4d9b0 alpha 0.7 rotated ±20°
- **الدليل / proof:** `style:pm-nikolajankovic-ce4ff4`

#### SYNC-232 · ترجمات جملة بجملة داخل الشريط السفلي · Sentence subtitles in letterbox · 👁 شوهد في فيديو
- **ماذا / what:** One sentence per caption, centred, crossfaded, timed to narration/music phrases; for Arabic use RTL shaping and Naskh/sans
- **أرقام / params:** fade 300 ms, min hold 2.5 s, max 42 chars/line
- **الدليل / proof:** `style:pm-rebutonepress-810f78`

#### SYNC-233 · ترجمة تُكتب لحظة نطق الكلمة · Voice-timed typewriter captions · 👁 شوهد في فيديو
- **ماذا / what:** From word timestamps (Whisper aligned per phrase), type each word's letters starting at word.start spread over its duration; thin caret; omit full stops
- **أرقام / params:** caret 2 px, letters ~30-50 ms each
- **الدليل / proof:** `style:pm-rossaxbt-3085b7`

#### SYNC-234 · ترجمة ملونة باسم المتحدث · Speaker-coloured subtitles · 👁 شوهد في فيديو
- **ماذا / what:** small caps name in character colour + line text, bottom centre
- **الدليل / proof:** `style:pm-ryzoft-4f85bd`

#### SYNC-235 · عداد كلمة مفتاحية متزامن مع التفريغ · Keyword counter synced to transcript · 👁 شوهد في فيديو
- **ماذا / what:** From word timestamps, find every occurrence of a keyword; at each word.start increment a chip counter with scale pop 1->1.25->1
- **أرقام / params:** pop 200 ms, chip top-right, mono label
- **الدليل / proof:** `style:pm-sab8a-364a5a`

#### SYNC-236 · ترجمة كلمة بكلمة مع تلوين الكلمة المهمة · Word-by-word captions with emphasis colour · 👁 شوهد في فيديو
- **ماذا / what:** Show 1-3 words at a time at word.start, keep previous line, colour the stressed word lime #d4ff3a and 1.4x size
- **أرقام / params:** fade 80 ms, left-third placement
- **الدليل / proof:** `style:pm-sab8a-364a5a`

#### SYNC-237 · عدّاد تنازلي لطول الأغنية · Song-length countdown clock · 👁 شوهد في فيديو
- **ماذا / what:** format remaining seconds as MM:SS (frames as 2nd field) from audio duration minus currentTime; ends at 00:00 exactly on the last frame
- **أرقام / params:** update every frame; tabular figures
- **الدليل / proof:** `style:pm-samaote-5e2fc2`

#### SYNC-238 · موجة صوت مع مؤشر · Voice waveform with playhead · 👁 شوهد في فيديو
- **ماذا / what:** Bars from amplitude array; played part coloured, playhead x=t/dur
- **أرقام / params:** 80-120 bars
- **الدليل / proof:** `style:pm-sudo-kiran-6609ed`

#### SYNC-239 · شريط ترجمة متزامن مع التعليق · Narration-synced subtitle band · 👁 شوهد في فيديو
- **ماذا / what:** one sentence per caption in plain sans, centred under the board, swapped at sentence boundaries from the TTS timing
- **أرقام / params:** max 2 lines, ~2.5% frame height
- **الدليل / proof:** `style:pm-tak3sh8-be5012`

#### SYNC-240 · موجة صوتية · Waveform bars · 👁 شوهد في فيديو
- **ماذا / what:** bars heights from noise, red
- **الدليل / proof:** `style:pm-tstfully-0aa6b4`

#### SYNC-241 · لافتة معلقة · Hanging sign caption · 👁 شوهد في فيديو
- **ماذا / what:** dark board, serif line crossfade 600 ms
- **الدليل / proof:** `style:pm-x4b47x-9cc84f`

#### SYNC-242 · كابشن داخل كبسولة · Subtitle pill captions · 👁 شوهد في فيديو
- **ماذا / what:** Dark rounded pill bottom-centre, white small text, one accent word coloured
- **أرقام / params:** radius 6 px
- **الدليل / proof:** `style:pm-xelandre-363f00`

#### SYNC-243 · شريط ترجمة متزامن · Narration subtitle bar · 👁 شوهد في فيديو
- **ماذا / what:** bottom-centre 2-line caption swapped per sentence from timing json
- **الدليل / proof:** `style:pm-yunn260414-60d996`

#### SYNC-244 · مزامنة قمة المؤثر مع الحدث · SFX peak-offset alignment · 👁 شوهد في فيديو
- **ماذا / what:** store each SFX file's internal peak time; start the sound at eventTime - peak so the transient lands on the visual event; risers aligned to their end
- **أرقام / params:** PEAK table per file
- **الدليل / proof:** `style:product`

#### SYNC-245 · أسلوب الترجمة حسب نبرة الكلام · Caption style by tone · 📄 موصوف
- **ماذا / what:** Read the transcript, detect tone, then pick font weight, entrance, color and size for captions.
- **كيف / how:** Hype 800-900 weight, scale-pop back.out(1.7) 0.1-0.2s, 72-96px; corporate 600-700, fade+slide power3.out 0.3s, 56-72px; tutorial mono 500-600, typewriter 0.4-0.5s, 48-64px; storytelling serif 400-500 slow fade 0.5-0.6s 44-56px; social rounded 700-800 elastic word-by-word 56-80px.
- **أرقام / params:** sizes 44-96px
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md`

#### SYNC-246 · تجميع الكلمات في الترجمة · Word grouping for captions · 📄 موصوف
- **ماذا / what:** Group spoken words into short pages based on energy, pauses and sentence ends.
- **كيف / how:** High energy 2-3 words, conversational 3-5, calm 4-6; break on sentence end, pauses >=150ms, or max count. Remotion: createTikTokStyleCaptions({captions, combineTokensWithinMilliseconds:1200}) -> pages with tokens; render each page in a <Sequence>; whiteSpace:'pre'.
- **أرقام / params:** 2-3/3-5/4-6 words; pause 150ms; 1200ms pages
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md` · `kosif-atlas/skills/2712-remotion/10431-remotion-captions/display-captions.md`

#### SYNC-247 · موضع الترجمة وضمان اختفائها · Caption placement & exit guarantee · 📄 موصوف
- **ماذا / what:** Captions sit in safe zones, never cover faces, only one group visible, and each group is force-hidden at its end time.
- **كيف / how:** Landscape: bottom 80-120px; portrait: ~600-700px from bottom; full-width absolute container (no left:50% translate trick); overflow visible; exit tween 0.12s then tl.set(el,{opacity:0,visibility:'hidden'}, group.end); self-lint by seeking to end+0.01 and checking computed style.
- **أرقام / params:** bottom 80-120px; exit 0.12s
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md`

#### SYNC-248 · شدة إبراز الكاريوكي · Karaoke highlight intensity ladder · 📄 موصوف
- **ماذا / what:** Active-word highlighting whose scale, color and glow scale with energy; emphasis words always break the pattern.
- **كيف / how:** High: accent color + glow + 15% scale pop, scatter/drop exits, alternate styles every 2 groups; low: warm white shift + 3% scale, collapse exit, alternate every 4; emphasis words (brand, ALL CAPS, numbers, emotion) get bigger scale + overshoot ease; Remotion: compare token.fromMs/toMs to absolute time, highlight color e.g. #39E508.
- **أرقام / params:** pop 15% high / 3% low
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/dynamic-techniques.md` · `kosif-atlas/skills/2712-remotion/10431-remotion-captions/display-captions.md`

#### SYNC-249 · كشف الصمت التكيفي · Adaptive silence detection · 📄 موصوف
- **ماذا / what:** Measure loudness first, then use the measured gating threshold as the silence floor so detection adapts to each recording.
- **كيف / how:** ffmpeg -i in -map 0:a -af loudnorm=print_format=json -f null - -> input_thresh; then -af silencedetect=noise=${THRESH}dB:d=0.5; merge near-contiguous silences (gap <0.2s); leading silence only if first start <0.5s; apply as trimBefore/trimAfter in frames (floor/ceil).
- **أرقام / params:** d=0.5s; merge gap 0.2s
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/silence-detection.md`

#### SYNC-250 · ضبط بداية الكلمة على النطق · Lyric onset snapping · 📄 موصوف
- **ماذا / what:** Model word timestamps can lag the audible onset by 50-80ms; snap each word to the nearest detected vocal onset so lyric type pops on the consonant.
- **كيف / how:** Onset detection (spectral flux) near each stamp, keep original in 'stamp'; render a sheet of one frame per word onset to verify.
- **أرقام / params:** lag 50-80 ms
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md`

#### SYNC-251 · طباعة حركية كلمة بكلمة من التفريغ · Per-word kinetic typography from transcript · 📄 موصوف
- **ماذا / what:** Words appear one by one at their spoken start times; emphasis words get stronger entrances.
- **كيف / how:** For each word in words.json: tl.from(span,{y:20, autoAlpha:0, duration:0.25, ease:'power3.out'}, word.start); emphasis (numbers, brand, emotion) scale 1.15 + accent color + back.out. Arabic: wrap whole words, direction:rtl, never split letters.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md`

#### SYNC-252 · تسميات الخطوات في فيديو الشرح · UI tutorial captions as action labels · 📄 موصوف
- **ماذا / what:** Teach the real path with one short line per decision using plain action labels, describing the action just before it happens and matching the visible state.
- **كيف / how:** Caption style e.g. 'CHOOSE A FILE', 'PRESS RECORD', 'REVIEW THE RESULT' (Arabic: اختر الملف، اضغط تسجيل، راجع النتيجة).
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/220-ui-tutorial-video` · `kosif-atlas/skills/2836-video-guide/11537-video-guide-creator`

#### SYNC-253 · لكل جملة منطوقة دليل بصري واحد · One visual proof per spoken claim · 📄 موصوف
- **ماذا / what:** In voice-led films every narrated line is paired with exactly one picture that proves or clarifies it, and actions happen on the word that names them.
- **كيف / how:** Build a beat table: spoken line | visual proof | entry/exit | on-screen text. Keep per-line and per-word timings (words.json) so a re-read can retime captions and picture automatically. Mix music under intelligible speech; SFX only on visible actions.
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/216-narrated-product-film/SKILL.md`

#### SYNC-254 · ميزانية الكلمات حسب الزمن · Narration pacing budgets · 📄 موصوف
- **ماذا / what:** Convert duration into a word budget before writing narration so scenes are not over-stuffed.
- **كيف / how:** Long-form ~150 words/min; short-form spoken script 80-150 words for 20-45 s; per-scene budgets for demo narration: 3-4 s -> 8-12 words (~70% fill), 5-6 s -> 15-22 words (~75%), 7-8 s -> 22-30 words (~80%). For Arabic, measure actual TTS/recording duration and retime via words.json rather than trusting counts.
- **أرقام / params:** 150 wpm; 3-4s:8-12w; 5-6s:15-22w; 7-8s:22-30w
- **الدليل / proof:** `kosif-atlas/skills/3067-youtube/13226-creator-script-agent/SKILL.md` · `kosif-atlas/skills/1802-content-multiplier/4838-channel-formats/channels/short-video.md` · `kosif-atlas/skills/166-demo-video/535-demo-video/references/scene-design-system.md`

#### SYNC-255 · حزمة الإتاحة للفيديو · Accessibility package for video · 📄 موصوف
- **ماذا / what:** Deliver a closed-caption script covering speech and meaningful sound effects, audio-description notes for visual-only moments, and caption styling per platform.
- **كيف / how:** Generate SRT/VTT from words.json; mark [sound] cues; list visual-only beats for description; keep burned captions inside safe zones.
- **الدليل / proof:** `kosif-atlas/skills/1520-digital-marketing-pro/4133-video-script/SKILL.md`

#### SYNC-256 · كشف الإعادات في التسجيل · Retake detection heuristic · 📄 موصوف
- **ماذا / what:** Repeated takes of the same line are found as transcript segments whose first 10 characters match and start within 60 s; by default only the last take is kept.
- **كيف / how:** Run over words.json/segments in Python; mark groups for review when ambiguous; never pick a non-default take without asking.
- **أرقام / params:** prefix 10 chars; window 60 s; keep last
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2451-davinciresolve-beats-devtalk/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2453-davinciresolve-cut-devtalk/SKILL.md`

#### SYNC-257 · منهج فيديو الكلمات على شبكة الإيقاع · Lyric-video method on a beat grid · 📄 موصوف
- **ماذا / what:** Music/lyric videos plan everything on a grid of tempo, beats, bars, sections and every sung word; word stamps are snapped to the nearest vocal onset (model stamps ran 50-80 ms late) so lyric type pops on the consonant; characters sit on one side of frame, words on the other; shots start and end on b…
- **كيف / how:** Write a one-page style sheet first (one real aesthetic risk, palette hex values with meanings, 2-3 typefaces each with a job, a 'never appears' list); generate words.json from the vocal, snap onsets with an energy-derivative detector, then animate typography per word in the HTML timeline.
- **أرقام / params:** onset correction 50-80 ms
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md` · `kosif-atlas/skills/1511-homie/3903-video/SKILL.md`

#### SYNC-258 · MG-013 تلوين الكلمات مع التعليق · MG-013 Karaoke word colouring · 📄 موصوف
- **ماذا / what:** Text is static and one word at a time turns the brand colour as it is spoken.
- **كيف / how:** 0-0.5 s appear, 0.5-5.2 s colour per spoken word, 5.2-6 s hold. Split into word ranges, drive fill from words.json start times (kosif-tool audio-sync playbook); keep original audio, no extra clicks; check sync manually and never change the speaker's words.
- **أرقام / params:** 6 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### SYNC-259 · تسجيل الصوت ومزامنة التصفيق والكلام القابل للقص · Voice capture, clap sync and cut-friendly speech · 📄 موصوف
- **ماذا / what:** Record narration at 48 kHz, mic 15-20 cm from the mouth, peaks near -12 dB, fridge/AC off; clap once in front of all cameras before a multi-camera take; leave about one second between sentences to create clean cut points; say list numbers aloud ('first, second') so numbered titles can land on them; …
- **كيف / how:** Sync by detecting the clap transient (numpy cross-correlation or ffmpeg astats peaks) and offsetting tracks; cut on gaps found with ffmpeg silencedetect.
- **أرقام / params:** 48 kHz; 15-20 cm; peak -12 dB; ~1 s pauses
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2447-akbun-vlog-shootplan/SKILL.md`

#### SYNC-260 · إصلاح انزياح التوقيت بعد دمج الصوت · Joined-audio drift fix · 📄 موصوف
- **ماذا / what:** Copy-mode concat keeps each piece's encoder padding and header frame, so timestamps summed from ffprobe durations drift later and later (measured ~50 ms per join; 9.1 s over 181 MP3 pieces). Decode and encode once to make durations add up.
- **كيف / how:** ffmpeg -f concat -safe 0 -i list.txt -c:a libmp3lame -b:a 64k -ar 24000 -ac 1 -write_xing 0 joined.mp3 ; verify by comparing joined duration with sum of parts. MP3 frame = 1152 samples (32/44.1/48k) or 576 (16/22.05/24k).
- **أرقام / params:** drift 2.51 s -> 0.06 s after single encode
- **الدليل / proof:** `kosif-atlas/skills/3323-joined-audio-transcript-drift/13837-joined-audio-transcript-drift/SKILL.md`

#### SYNC-261 · كشف الصمت للقص التلقائي · Silence detection for jump-cut editing · 📄 موصوف
- **ماذا / what:** Find dead air to remove with a fixed or adaptive threshold; adaptive uses the file's own EBU gating threshold so quiet and loud recordings behave the same.
- **كيف / how:** fixed: -af silencedetect=n=-35dB:d=0.7 -f null - ; adaptive: run loudnorm=print_format=json, take input_thresh, then silencedetect=noise=${input_thresh}dB:d=0.5 ; parse silence_start/silence_end; merge gaps <0.2 s for lead/trail blocks
- **أرقام / params:** d 0.5-0.7 s; noise -35 dB or input_thresh
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/silence-detection.md` · `kosif-atlas/skills/1096-akbun-editvideo/2453-davinciresolve-cut-devtalk/SKILL.md`

#### SYNC-262 · لا تستخدم نماذج en مع العربي · Never use .en Whisper models for Arabic · 📄 موصوف
- **ماذا / what:** English-only Whisper models translate non-English audio into English instead of transcribing; for Arabic or unknown language use the multilingual model with an explicit language code.
- **كيف / how:** --model small|medium|large-v3 --language ar (no .en); unknown -> omit language for autodetect
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transcript-guide.md`

#### SYNC-263 · نماذج .en تترجم ولا تفرغ · .en models translate — never use for Arabic · 📄 موصوف
- **ماذا / what:** English-only whisper models silently translate non-English audio; for Arabic always use multilingual model with language=ar.
- **كيف / how:** whisper --model small|medium|large-v3 --language ar
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transcript-guide.md`

#### SYNC-264 · تفريغ داخل DaVinci Resolve · Resolve built-in transcription · 📄 موصوف
- **ماذا / what:** Use MediaPoolItem.TranscribeAudio()/GetTranscription() in Resolve Studio 20+ before falling back to whisper.
- **كيف / how:** Resolve scripting API; set transcriptionLanguage.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2451-davinciresolve-beats-devtalk`

#### SYNC-265 · ربط نبرة الكلام بأسلوب الكابشن · Tone-to-caption style map · 📄 موصوف
- **ماذا / what:** Choose caption font weight, animation and size from transcript tone.
- **كيف / how:** GSAP/CSS: hype=heavy 800-900, back.out(1.7) 0.1-0.2s, 72-96px; corporate 600-700 power3.out 0.3s 56-72px; tutorial mono typewriter 0.4-0.5s; story serif power2.out 0.5-0.6s; social rounded elastic word-by-word.
- **أرقام / params:** see how
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md`

#### SYNC-266 · تجميع كلمات الكابشن · Caption word grouping · 📄 موصوف
- **ماذا / what:** Group words by energy and break on sentences or pauses.
- **كيف / how:** hype 2-3 words, conversational 3-5, calm 4-6; break at pauses >=150ms.
- **أرقام / params:** 150ms
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md`

#### SYNC-267 · إبراز كلمات بعينها · Per-word emphasis styling · 📄 موصوف
- **ماذا / what:** Brand names, numbers, CTAs and emotional words get colour/scale/overshoot treatment.
- **كيف / how:** Tag tokens in words.json; apply accent class + back.out overshoot.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md`

#### SYNC-268 · موضع الكابشن الآمن · Caption safe placement · 📄 موصوف
- **ماذا / what:** Bottom 80-120px on 16:9, ~600-700px from bottom on 9:16, never over face, one group at a time, overflow visible.
- **كيف / how:** fitTextFontSize maxWidth 1600/900, base 78, min 42.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md`

#### SYNC-269 · مواصفة الترجمة السينمائية · Cinema subtitle spec · 📄 موصوف
- **ماذا / what:** Static white subtitle with thin dark outline, 1-2 lines, bottom anchored so lines grow upward.
- **كيف / how:** Resolve Fusion Text+ template or HTML: glyph height 3.5-4.5% of frame, side margin >=8%, bottom 8-10%.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2431-akbun-davinciresolve-caption-template`

#### SYNC-270 · لا تغير كلام المتحدث · Never alter transcript words · 📄 موصوف
- **ماذا / what:** Captions must reproduce speaker words exactly unless asked.
- **كيف / how:** Diff caption text vs words.json in QA.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### SYNC-271 · ترجمة مدمجة عند الطلب فقط · Captions only when asked · 📄 موصوف
- **ماذا / what:** Burned-in captions can ruin a client's own subtitle pass; render them only when requested, else deliver SRT/VTT.
- **كيف / how:** Export sidecar .srt/.vtt by default; burn via ffmpeg subtitles/ass filter on request.
- **الدليل / proof:** `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`

#### SYNC-272 · ظهور الكلمات بانزلاق متناقص · Per-word kinetic typography with decaying slide · 📄 موصوف
- **ماذا / what:** Words appear at transcript onsets, each sliding in from a decreasing offset.
- **كيف / how:** GSAP timeline .from(word,{x:slide,y:14,opacity:0,duration:0.35,ease:'power2.out'},onset); RTL: slide from the left side mirrored for Arabic.
- **أرقام / params:** slides 80,60,50,25,12px
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### SYNC-273 · حساب مدة المقطع من عدد كلمات النص · Script-to-duration math for spoken AI segments · 📄 موصوف
- **ماذا / what:** Size each generated talking segment from its word count so the model neither rushes nor pads dead air.
- **كيف / how:** raw = words / 2 (≈2 words/s; 2.5 still natural); duration = ceil(raw); minimum 4 s; if >15 s split at a sentence boundary; add 1-2 s only for a post-speech gesture or CTA hold; keep the user's script verbatim in quotes and default to 'The person says'.
- **أرقام / params:** 2 wps; 4-15 s; ~30 words per 15 s
- **الدليل / proof:** `kosif-atlas/skills/259-quickdesign/865-quickdesign`

#### SYNC-274 · ترجمة متزامنة مع المقاطع · Syllable-timed speech captions · 📄 موصوف
- **ماذا / what:** Caption words appear on their own spoken times, rising from blur; keywords coloured accent.
- **كيف / how:** directed.html speech(): words[{text,t,key}] from EDIT.captions; also verse.html lines.
- **أرقام / params:** per word y 18*k -> 0, blur 6px -> 0, 0.28 s power3.out at t-0.04; caption size 54*k; exit 0.2 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/directed.html:73`

#### SYNC-275 · محرك القصيدة الصوتية · Verse engine: sound-only typographic film · 📄 موصوف
- **ماذا / what:** A lyric/poem/dua film from audio alone: words appear on their sung times over a sky whose light breathes with the voice; sections, motifs, cards and end are generated.
- **كيف / how:** python scripts/verse.py AUDIO NAME [--text|--words] [--mood night|dawn|gold|sea|ink] [--accent] [--images ...]; writes verse.js + sound.js (channels) next to verse.html; render with motion.py.
- **أرقام / params:** line font 100*k weight 700, line-height 1.55, text-wrap balance; words y 30*k blur 9px 0.42 s (flat mode); keyword pulse 1.07 0.18 s yoyo; line exit 0.45 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/verse.html:62` · `100-superskills/skills/kosif-montage-motion/scripts/verse.py:437`

#### SYNC-276 · فيلم كلمات من صوت · Lyric / poem / dua film from sound · 📄 موصوف
- **ماذا / what:** Turns a song, poem or supplication recording into a kinetic-words film project, optionally with a lyrics file and a title, in one of five moods.
- **كيف / how:** From the studio: recipe 'verse' (form in the الوصفات tab, POST /api/jobs {recipe:'verse', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py verse …`.
- **أرقام / params:** audio (file); --name verse; --text lyrics file; --title; --mood night|dawn|gold|sea|ink (default night)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:27`

#### SYNC-277 · Voice2Motion: موشن من الصوت حسب المعنى · Voice2Motion: meaning-driven motion graphics from audio · 📄 موصوف
- **ماذا / what:** Generates motion graphics whose symbols follow what is being said in a voice track, optionally driven by a cues JSON or a transcript.
- **كيف / how:** From the studio: recipe 'audio2motion' (form in the الوصفات tab, POST /api/jobs {recipe:'audio2motion', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py audio2motion …`.
- **أرقام / params:** audio; --cues JSON; --transcript; --out out/voice2motion.mp4
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:30`

#### SYNC-278 · قص الصمت · Silence cut (jump cut) · 📄 موصوف
- **ماذا / what:** Removes silent gaps from a talking clip to make jump cuts.
- **كيف / how:** From the studio: recipe 'silence' (form in the الوصفات tab, POST /api/jobs {recipe:'silence', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py silence …`.
- **أرقام / params:** clip; --out out/cut.mp4
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:69`

#### SYNC-279 · ترجمة كاريوكي عربية محروقة · Burned-in Arabic karaoke captions · 📄 موصوف
- **ماذا / what:** Burns word-timed Arabic captions with the spoken word highlighted into a video in one of seven styles.
- **كيف / how:** From the studio: recipe 'captions' (form in the الوصفات tab, POST /api/jobs {recipe:'captions', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py captions …`.
- **أرقام / params:** video; --spec captions.json; --style reels|tiktok|hormozi|boxed|minimal|cinema|punchy; --out out/captioned.mp4
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:75`

#### SYNC-280 · تفريغ بالكلمات والأزمنة · Word-level transcription + SRT · 📄 موصوف
- **ماذا / what:** Transcribes speech with per-word timestamps and writes an SRT (faster-whisper).
- **كيف / how:** From the studio: recipe 'transcribe' (form in the الوصفات tab, POST /api/jobs {recipe:'transcribe', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py transcribe …`.
- **أرقام / params:** src; --model large-v3|small|auto
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:78`

#### SYNC-281 · أسلوب ترجمة: ريلز · Caption style: Reels (reels) · 📄 موصوف
- **ماذا / what:** The 'reels' burned-in Arabic karaoke caption look (ASS subtitles with the spoken word highlighted).
- **كيف / how:** Recipe captions --style reels (or reel --style reels); colours are ASS &HAABBGGRR; sizes per 1080 px of the short side, margins per 1920 of height.
- **أرقام / params:** Noto Sans Arabic 74 (per 1080 short side), white, spoken word yellow (&H0059DEFF) pulsing 112%, outline 6, shadow 3, margin 300, ≤ 6 words
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:13` · `100-superskills/skills/kosif-montage-motion/scripts/montage.py:309`

#### SYNC-282 · أسلوب ترجمة: سينما · Caption style: Cinema (cinema) · 📄 موصوف
- **ماذا / what:** The 'cinema' burned-in Arabic karaoke caption look (ASS subtitles with the spoken word highlighted).
- **كيف / how:** Recipe captions --style cinema (or reel --style cinema); colours are ASS &HAABBGGRR; sizes per 1080 px of the short side, margins per 1920 of height.
- **أرقام / params:** Noto Naskh Arabic 46, #EAEAEA, soft highlight &H00A8E6FF, pop 104%, outline 3, shadow 2, margin 150
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:13` · `100-superskills/skills/kosif-montage-motion/scripts/montage.py:310`

#### SYNC-283 · أسلوب ترجمة: قوي · Caption style: Punchy (punchy) · 📄 موصوف
- **ماذا / what:** The 'punchy' burned-in Arabic karaoke caption look (ASS subtitles with the spoken word highlighted).
- **كيف / how:** Recipe captions --style punchy (or reel --style punchy); colours are ASS &HAABBGGRR; sizes per 1080 px of the short side, margins per 1920 of height.
- **أرقام / params:** Noto Kufi Arabic 72, white, highlight &H00F8BD38, pop 116%, outline 8, shadow 4, margin 330
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:13` · `100-superskills/skills/kosif-montage-motion/scripts/montage.py:311`

#### SYNC-284 · أسلوب ترجمة: تيك توك · Caption style: TikTok (tiktok) · 📄 موصوف
- **ماذا / what:** The 'tiktok' burned-in Arabic karaoke caption look (ASS subtitles with the spoken word highlighted).
- **كيف / how:** Recipe captions --style tiktok (or reel --style tiktok); colours are ASS &HAABBGGRR; sizes per 1080 px of the short side, margins per 1920 of height.
- **أرقام / params:** Noto Kufi Arabic 84, ≤ 4 words, thick outline 10, no shadow, highlight &H004DE0FF, pop 120% for 90 ms, margin 420
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:13` · `100-superskills/skills/kosif-montage-motion/scripts/montage.py:313`

#### SYNC-285 · أسلوب ترجمة: كلمة كلمة · Caption style: Hormozi (one word at a time) (hormozi) · 📄 موصوف
- **ماذا / what:** The 'hormozi' burned-in Arabic karaoke caption look (ASS subtitles with the spoken word highlighted).
- **كيف / how:** Recipe captions --style hormozi (or reel --style hormozi); colours are ASS &HAABBGGRR; sizes per 1080 px of the short side, margins per 1920 of height.
- **أرقام / params:** Noto Kufi Arabic 96, 1 word on screen, vivid green highlight &H0088FF39, pop 118% for 80 ms, outline 9, margin 440
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:13` · `100-superskills/skills/kosif-montage-motion/scripts/montage.py:314`

#### SYNC-286 · أسلوب ترجمة: صندوق · Caption style: Boxed (boxed) · 📄 موصوف
- **ماذا / what:** The 'boxed' burned-in Arabic karaoke caption look (ASS subtitles with the spoken word highlighted).
- **كيف / how:** Recipe captions --style boxed (or reel --style boxed); colours are ASS &HAABBGGRR; sizes per 1080 px of the short side, margins per 1920 of height.
- **أرقام / params:** Noto Sans Arabic 66, ≤ 5 words, opaque box BorderStyle 3 back &H66000000, pop 108%, outline 2, margin 300
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:13` · `100-superskills/skills/kosif-montage-motion/scripts/montage.py:315`

#### SYNC-287 · أسلوب ترجمة: بسيط · Caption style: Minimal (minimal) · 📄 موصوف
- **ماذا / what:** The 'minimal' burned-in Arabic karaoke caption look (ASS subtitles with the spoken word highlighted).
- **كيف / how:** Recipe captions --style minimal (or reel --style minimal); colours are ASS &HAABBGGRR; sizes per 1080 px of the short side, margins per 1920 of height.
- **أرقام / params:** Noto Naskh Arabic 54, ≤ 7 words, no pop (100%), not bold, #F2F2F2 both colours, outline 2, shadow 1, margin 220 — for interviews
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:13` · `100-superskills/skills/kosif-montage-motion/scripts/montage.py:316`

#### SYNC-288 · قواعد وضوح الترجمة العربية · Arabic caption legibility rules · 📄 موصوف
- **ماذا / what:** Rules that keep Arabic captions readable on any background and clear of platform UI.
- **كيف / how:** Spoken word in a highlight colour, rest white; thick black outline + deep shadow; 5-7 words per screen; keep >= 280 px clear at the bottom of 9:16; contrast >= 4.5:1; video subtitles max 42 chars/line, 1-2 lines, 1-7 s each.
- **أرقام / params:** highlight #FFDE59 or #38BDF8; outline 6-8 px; fonts Cairo, Montserrat, Almarai; safe zone 280 px
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/montage_grammar.md` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/SKILL.md` · `kosif-one/tools/kosif-omni/skills/kosif-video/SKILL.md`

#### SYNC-289 · حرق الترجمة · Burned-in subtitles (libass) · 📄 موصوف
- **ماذا / what:** Burn SRT into picture with forced style.
- **كيف / how:** subtitles=captions.srt:force_style='FontName=Cairo,FontSize=22,Outline=2,MarginV=60'
- **أرقام / params:** Cairo 22, outline 2, MarginV 60
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### SYNC-290 · ترجمة قابلة للإيقاف · Soft subtitle track · 📄 موصوف
- **ماذا / what:** Embed SRT as mov_text track tagged Arabic.
- **كيف / how:** -i captions.srt -c copy -c:s mov_text -metadata:s:s:0 language=ara
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### SYNC-291 · قاعدة قراءة الترجمة · Caption readability rule · 📄 موصوف
- **ماذا / what:** Subtitle line limits.
- **كيف / how:** 42 chars/line, 2 lines, 1-7 s on screen, in safe area, never over faces.
- **أرقام / params:** 42 chars, 2 lines, 1-7 s
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### SYNC-292 · ترجمة Text+ · Text+ subtitle in Resolve · 📄 موصوف
- **ماذا / what:** Append a Text+ template from Media Pool to SUBTITLE track and edit via Fusion comp; avoid InsertFusionTitleIntoTimeline (ripples V1).
- **كيف / how:** AppendToTimeline + GetFusionCompByIndex(1)
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/color-grading-order.md`

#### SYNC-293 · إنتاج بودكاست · Podcast production pipeline · 📄 موصوف
- **ماذا / what:** Format, timed outline (30 s hook, intro, 3 parts, outro CTA), graded guest questions, audio plan, show notes with chapters, 3 short captioned clips.
- **كيف / how:** Playbook; audio to -16 LUFS stereo / -19 mono, -1 dBTP, denoise + gentle compression.
- **الدليل / proof:** `100-superskills/skills/podcast-production/SKILL.md`

#### SYNC-294 · مزامنة الفم بستة أشكال · Six-shape lip sync · 📄 موصوف
- **ماذا / what:** Mouth picks among closed, A, O, E, M, F from audio energy or script text.
- **كيف / how:** Map RMS/phonemes to shape per frame.
- **أرقام / params:** 6 visemes
- **الدليل / proof:** `100-superskills/skills/character-animation-2d/SKILL.md`

#### SYNC-295 · ترجمة بكلمة مميزة · Keyword-highlight captions · 📄 موصوف
- **ماذا / what:** 1-2 lines, max 42 chars, highlighted keyword.
- **كيف / how:** captions.srt + template
- **أرقام / params:** 42 chars
- **الدليل / proof:** `100-superskills/skills/reels-shorts-factory/SKILL.md:24`

#### SYNC-296 · مواصفة الترجمة · Subtitle spec · 📄 موصوف
- **ماذا / what:** 42 chars/line, 2 lines, 1-7 s each, synced to word onset; never cover faces/key text.
- **كيف / how:** SRT + ffmpeg subtitles burn
- **الدليل / proof:** `100-superskills/skills/video-editing-captions/SKILL.md:24`

#### SYNC-297 · مونتاج يقوده الصوت · Voice-first montage · 📄 موصوف
- **ماذا / what:** Narration is the timing authority: cuts on phrase boundaries (or a 3-5 s cadence), no fake BPM from speech, best footage-energy windows, natural audio ducked under voice.
- **كيف / how:** motion.py montage --voice NARRATION (voice_plan/voice_cut in montage.py).
- **أرقام / params:** cuts ≥ 1.8 s and ≤ 6.5 s; final segment reserved ≥ 1.8 s; output -14 LUFS / -1.5 dBTP; 1080×1920 H.264 yuv420p 30 fps AAC (97.88 s live test)
- **الدليل / proof:** `kosif-studio/motion/references/voice-open-footage-upgrade-2026-10-10.md`

#### SYNC-298 · معايرة حجم الترجمة · ASS caption PlayRes calibration · 📄 موصوف
- **ماذا / what:** SRT/libass default script resolution scales FontSize and MarginV; calibrate against real 1080×1920 preview frames.
- **كيف / how:** Smaller white Arabic text, black outline/shadow, bottom safe zone, no opaque box.
- **الدليل / proof:** `kosif-studio/motion/references/voice-open-footage-upgrade-2026-10-10.md`

#### SYNC-299 · كاريوكي كلمة بكلمة · Karaoke captions one event per word · 📄 موصوف
- **ماذا / what:** One ASS event per spoken word with a highlight colour and a 120 ms pop keeps Arabic shaped and ordered.
- **كيف / how:** montage.py captions VIDEO --spec caps.json (accepts voice.py timings; Noto Sans/Kufi/Naskh Arabic).
- **أرقام / params:** pop 120 ms; words timed by length when no timings
- **الدليل / proof:** `kosif-studio/motion/references/hyperframes-authoring.md` · `kosif-studio/motion/references/x-trend-2026.md`

#### SYNC-300 · قاعدة دقة التزامن للكلمات المفتاحية · Key-word sync tolerance rule · 📄 موصوف
- **ماذا / what:** Motion linked to an emphasis word must start within 100 ms of the spoken word; a visual lead of max 80 ms is allowed, never animate before it is heard.
- **كيف / how:** offset_ms=|word.start - motion_frame/fps|*1000 <= 100
- **أرقام / params:** 100 ms tolerance, 80 ms lead
- **الدليل / proof:** `kosif-tool/templates/PLAN.md` · `kosif-tool/templates/TEST_REPORT.md`

#### SYNC-301 · ترجمة ثنائية اللغة · Bilingual caption block · 📄 موصوف
- **ماذا / what:** Arabic line on top RTL, English below LTR at reduced size, each block with its own dir.
- **أرقام / params:** English 70% size
- **الدليل / proof:** `kosif-tool/playbooks/arabic-typography.md:46`

#### SYNC-302 · إضاءة الكلمة قبل نطقها · Karaoke word lead for Arabic · 📄 موصوف
- **ماذا / what:** Highlight each whole word slightly before it is spoken; long words may fill RTL across their duration.
- **كيف / how:** From words.json start.
- **أرقام / params:** lead 40–80 ms
- **الدليل / proof:** `kosif-tool/playbooks/arabic-typography.md:79`

#### SYNC-303 · الصوت هو الساعة الرئيسية · Audio as master clock · 📄 موصوف
- **ماذا / what:** Voice is never edited/stretched/resampled; animation fits audio; scene times from audio rounded to frames.
- **كيف / how:** durationInFrames = ceil(audioSeconds × fps).
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:15-16` · `kosif-tool/playbooks/audio-sync.md:72`

#### SYNC-304 · قياس مدة الصوت · Probe audio duration · 📄 موصوف
- **ماذا / what:** Get audio length to set film duration.
- **كيف / how:** ffprobe -v error -show_entries format=duration -of csv=p=0 voice.mp3
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:25`

#### SYNC-305 · دمج السوابق وعلامات الترقيم · Clitic/punctuation merge for Arabic transcripts · 📄 موصوف
- **ماذا / what:** Merge Whisper's split clitics and attached punctuation into displayable words; use the user's exact text for Qur'an.
- **كيف / how:** Manual edit keeping timings.
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:76` · `kosif-tool/playbooks/audio-sync.md:28`

#### SYNC-306 · حدود التسامح في المزامنة · Sync tolerances · 📄 موصوف
- **ماذا / what:** Lead animation before speech; tight tolerance on key words; cut only on pauses.
- **أرقام / params:** start at word.start − 40…80 ms; key words ≤ 100 ms; others ≤ 150 ms; never cut mid-word
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:29` · `kosif-tool/playbooks/audio-sync.md:34`

#### SYNC-307 · التعامل مع الصمت · Silence handling · 📄 موصوف
- **ماذا / what:** Pauses are scene-change opportunities; long pauses need ambient motion; phrases end at pauses.
- **أرقام / params:** phrase break > 400 ms; scene change > 600 ms; motion required > 1.5 s
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:17` · `kosif-tool/playbooks/audio-sync.md:36`

#### SYNC-308 · وصفة ترجمة الشرح المسرود · Narrated explainer caption recipe · 📄 موصوف
- **ماذا / what:** Phrase fades in before its start, active word highlighted, key-word visual pops, phrase fades after end.
- **أرقام / params:** phrase in at start−0.15 s; word highlight at start−0.06 s outBack 140 ms; visual pop +0.3 s spring; out +0.4 s
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:42-49`

#### SYNC-309 · إيقاع التلاوة والقصيدة · Recitation / poem pacing · 📄 موصوف
- **ماذا / what:** One verse per screen, change on waqf, slow crossfades, no bouncy effects; follow reciter not beat grid.
- **أرقام / params:** crossfade 600–900 ms
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:51` · `kosif-tool/playbooks/music.md:68`

#### SYNC-310 · الإيماءة تسبق الكلمة · Body-leads-voice gesture timing · 📄 موصوف
- **ماذا / what:** Gestures land before the stressed word; SFX on contact frames.
- **أرقام / params:** gesture 2–4 frames early
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:81`

#### SYNC-311 · مزامنة الأرقام المنطوقة · Spoken-number sync for charts · 📄 موصوف
- **ماذا / what:** Counter finishes on the word that says the number; bars finish at end of naming phrase; line draw spans trend sentence; log in TEST_REPORT.
- **كيف / how:** words.json emphasis flag; counter starts 700–1000 ms earlier.
- **أرقام / params:** ±100 ms; visuals lead ≤ 150 ms; ≤ 3 frames at 30 fps; 120 BPM → stagger 125/250 ms
- **الدليل / proof:** `kosif-tool/playbooks/charts.md:201-208`

#### SYNC-312 · مزامنة المخطط · Diagram sync rules · 📄 موصوف
- **ماذا / what:** Node pops on its name, edges during connecting phrase, camera only in pauses.
- **أرقام / params:** ≤ 100 ms; pauses > 400 ms
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:77`

#### SYNC-313 · ترجمة كاريوكي بحبة · Karaoke caption pill · 📄 موصوف
- **ماذا / what:** Phrase at 60% opacity, active word 100% with accent pill.
- **أرقام / params:** pill scale 0.96→1.08 over 140 ms
- **الدليل / proof:** `kosif-tool/playbooks/kinetic-type.md:47`

#### SYNC-314 · توقيت سطر الأغنية · Lyric line timing · 📄 موصوف
- **ماذا / what:** Lines lead singing, hold while sung, exit quickly.
- **أرقام / params:** enter 80–120 ms early (recipe: −100 ms, 350 ms mask wipe); exit ≤ 200 ms (150 ms after last word)
- **الدليل / proof:** `kosif-tool/playbooks/music.md:28` · `kosif-tool/playbooks/music.md:43`

#### SYNC-315 · مزامنة الجسيمات · Particle audio sync · 📄 موصوف
- **ماذا / what:** Bursts on transients within one frame; flow speed may follow smoothed loudness.
- **أرقام / params:** smoothing 200 ms
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:78`

#### SYNC-316 · مزامنة أحداث الجهاز مع الكلمات · Device event sync to words · 📄 موصوف
- **ماذا / what:** Tap at emphasis word start−40 ms; rotation spans phrase; scroll on sentence starts; island on word start; 100 ms visual quiet zone.
- **كيف / how:** Math.round(start*fps).
- **أرقام / params:** tolerance 100 ms; scroll ≤ 1 per 450 ms; island collapse +300 ms after sentence
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:198-205`

#### SYNC-317 · مزامنة قطع الصور · Photo cut sync · 📄 موصوف
- **ماذا / what:** Cut 2 frames before emphasis word; moves change on phrase boundaries; settle within 300 ms after sentence; never audio-reactive photos; SFX separate stem.
- **أرقام / params:** 2 frames ≈ 67 ms at 30 fps; lead 40–70 ms; ≤ 100 ms; whoosh ≤ −18 dBFS; pan direction change every 2 or 4 bars
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:205-211`

#### SYNC-318 · تنسيق ترجمة ASS · ASS caption styling · 💡 فكرة
- **ماذا / what:** Styled burned captions with outline, shadow, karaoke \k timing.
- **كيف / how:** Generate .ass from words.json (\k centiseconds per word), ffmpeg -vf ass=file.ass with fontsdir; libass shapes Arabic via HarfBuzz.
- **أرقام / params:** Outline 3-4, Shadow 0-2
- **الدليل / proof:** `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### SYNC-319 · فم بالمقاطع · Phoneme mouth tiles · 💡 فكرة
- **ماذا / what:** Mouth cycles six phoneme replacement tiles synced to lyric syllables.
- **كيف / how:** Map syllable timings → tile index.
- **أرقام / params:** 6 phonemes
- **الدليل / proof:** `style:pm-davidshulmanfl-371638`

#### SYNC-320 · ترجمة كلمة بكلمة · Word-timed caption pop · 💡 فكرة
- **ماذا / what:** Each caption word lands at its words.json start, tolerance 40 ms; active word in accent.
- **كيف / how:** words.json → per-word opacity/scale.
- **أرقام / params:** 120 ms; scale 0.96→1; ±40 ms
- **الدليل / proof:** `style:pm-gautam-mer1-2ae354`

#### SYNC-321 · ثلاث أنماط ترجمة · Caption preset trio · 💡 فكرة
- **ماذا / what:** Clean, boxed, outlined caption presets shown alternately in Arabic/English.
- **كيف / how:** CSS presets; 240 ms crossfade every 2 s.
- **أرقام / params:** 48 px; 6 px gap
- **الدليل / proof:** `style:pm-gautam-mer1-2ae354`

#### SYNC-322 · دخول الكلمات على التوقيت · Word-onset lyric entrance · 💡 فكرة
- **ماذا / what:** Words enter from words.json onsets.
- **كيف / how:** Remotion reading word timing.
- **أرقام / params:** <=40 ms from onset; 180 ms cubic-bezier(0.2,0.9,0.2,1) scale 0.92->1; exit 240 ms cubic-bezier(0.6,0,0.9,0.4)
- **الدليل / proof:** `style:pm-samaote-5e2fc2`

#### SYNC-323 · عدم لمس الصوت · Untouched user track · 💡 فكرة
- **ماذا / what:** No remix, ducking or stretch.
- **الدليل / proof:** `style:pm-samaote-5e2fc2`

#### SYNC-324 · تمييز كاريوكي باللون · Colour-only karaoke highlight · 💡 فكرة
- **ماذا / what:** Active word changes colour only.
- **أرقام / params:** lines 220 ms, 12 px, 60 ms stagger; >=28 px
- **الدليل / proof:** `style:pm-tstfully-0aa6b4`

#### SYNC-325 · موجة تتحول لنص · Waveform-to-text cascade · 💡 فكرة
- **ماذا / what:** counters easeOutExpo 1200-1400 ms; push 4% at 5-9 s
- **الدليل / proof:** `style:pm-tstfully-0aa6b4`
