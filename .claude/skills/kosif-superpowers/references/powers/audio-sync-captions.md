# التزامن مع الكلام والترجمة — Audio sync & captions

> **قوتك هنا:** تجعل الصوت ساعة الفيلم: تفرّغ العربية بتوقيت الكلمات، تحاذي النص الصحيح بتشكيله على التفريغ، وتدخل كل كلمة على موعد نطقها — ثم تقيس الفرق إطارًا بإطار بدل أن تفترضه. وتحرق ترجمة كاريوكي عربية بسبعة ستايلات دون أن يتغير ترتيب الكلمات.
> **أقوى دليل:** فيلم `proofs/arabic-voice-kinetic` (أقصى فرق 33 ms، صفر كلمات مبكرة، 15/15 كلمة) و`proofs/audio-reactive-spectrum` (تعبئة كل كلمة ≤ 35 ms بعد نطقها)؛ واختبارات الكاريوكي والقصيدة وVoice2Motion والإخراج التلقائي نجحت هنا، و`words_convert.py` حوّل SRT عربيًا أمامي.
> **You can:** keep audio untouched, transcribe and align Arabic, estimate honestly without ASR, design and burn captions, animate words on their times and build films from sound. **58 powers follow** — ✅ 20 · 🟢 9 · 📦 7 · 🔑 1 · 👁 5 · 📄 16 · 💡 0.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`).

**فحص سريع لهذه الحاوية (2026-10-16):** ffmpeg مع libass/FriBiDi/HarfBuzz ✔ · faster-whisper وPiper يعملان داخل venv أفلام الإثبات (ليسا في Python النظام → `pip install`) · huggingface.co متاح لتنزيل النماذج · لا خطوط عربية نظامية → مرّر `fontsdir=` لـ libass.

## الفهرس / contents
- **الصوت ساعة رئيسية وملف words.json — Audio as master clock & words.json** — SYNC-01 … SYNC-06 (6)
- **التفريغ والمحاذاة — Transcription & alignment** — SYNC-07 … SYNC-16 (10)
- **توقيت بلا تفريغ — Timing without ASR** — SYNC-17 … SYNC-20 (4)
- **قواعد تصميم الترجمة — Caption design rules** — SYNC-21 … SYNC-26 (6)
- **ترجمة كاريوكي محروقة — Burned karaoke captions (ASS)** — SYNC-27 … SYNC-31 (5)
- **ترجمة حركية في HTML وRemotion — Kinetic captions in HTML & Remotion** — SYNC-32 … SYNC-44 (13)
- **أفلام من الصوت — Films from sound** — SYNC-45 … SYNC-52 (8)
- **الصمت والقص والتزامن الصوتي — Silence, cuts & audio sync utilities** — SYNC-53 … SYNC-58 (6)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves

## الصوت ساعة رئيسية وملف words.json — Audio as master clock & words.json

_الصوت لا يُمس؛ كل حركة تتبع ملف توقيت الكلمات، وكل تزامن يُقاس لا يُفترض._

#### SYNC-01 · الصوت هو الساعة الرئيسية · Audio is the master clock · ✅ مُثبت هنا / proven here
- **ماذا / what:** صوت المستخدم لا يُعاد أخذ عيناته ولا يُمط ولا يُعاد توقيته؛ الصورة تتبع الصوت ومدة الفيلم = مدة الصوت مقربة لإطار. — The user's audio is never resampled, stretched or retimed; picture follows sound and film length = audio length rounded to frames.
- **متى أستخدمها / when:** كل فيلم معه صوت — every film with supplied audio.
- **كيف / how:** durationInFrames = ceil(audioSeconds × fps) from ffprobe -v error -show_entries format=duration -of csv=p=0 voice.mp3. Mux with node tools/render_html.cjs --audio voice.wav (apad/-shortest; the stream is copied, not re-timed) or Remotion <Audio> at frame 0 with calculateMetadata/getAudioDurationInSeconds. Loudness changes go on a separate delivery copy only. Proven in both proof films: audio 11.500 s vs master 11.500 s, 13/13 checks. **أرقام / params:** duration = ceil(sec × fps)
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:15-16` · `kosif-tool/tools/render_html.cjs:373` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md` · `kosif-tool/starters/remotion/src/Film.tsx:32`

#### SYNC-02 · ملف توقيت الكلمات kosif-words/1 · words.json master timing schema · ✅ مُثبت هنا / proven here
- **ماذا / what:** ملف واحد [{word,start,end}] بالثواني، مرتب بلا تداخل، مع emphasis وscene اختياريين واللغة والاتجاه ومدة الصوت. — One sorted, non-overlapping [{word,start,end}] file in seconds, with optional emphasis/scene plus language, direction and audio duration.
- **متى أستخدمها / when:** قبل أي ترجمة أو حركة متزامنة — before any caption or synced motion.
- **كيف / how:** Scaffold copies templates/words.example.json to words.json; for file:// pages emit words.js (window.KOSIF_WORDS) with tools/words_convert.py words.json words.js. Both proof films are driven from words.json/words.js. **أرقام / params:** fields word/start/end (+emphasis, scene); seconds, ms precision
- **الدليل / proof:** `kosif-tool/templates/words.example.json` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/words.json` · `kosif-tool/starters/html-canvas/words.js`

#### SYNC-03 · محوّل الترجمات والتفريغ إلى words.json · Subtitle/transcript → words.json converter · ✅ مُثبت هنا / proven here
- **ماذا / what:** يحوّل SRT وVTT وWhisper JSON والقوائم وCSV/TSV إلى توقيت كلمات مرتب غير متداخل، ويزيح الكل بإزاحة ويفرض فجوة دنيا. — Converts SRT, VTT, Whisper JSON, flat lists and CSV/TSV into sorted, non-overlapping word timings, with a global offset and a minimum gap.
- **متى أستخدمها / when:** المستخدم أعطاك SRT أو تفريغًا جاهزًا — the user hands you an SRT or transcript.
- **كيف / how:** python3 tools/words_convert.py in.srt out.json [--format srt|vtt|json|csv|tsv] [--offset -0.08] [--min-gap 0.02]; SRT/VTT cues spread words by letter count (phrase-level timing only — per-word effects want real word stamps); strips <tags>, {ASS} tags, dashes and ♪; min word 20 ms. Ran here on an Arabic SRT: 6 words, offset −0.05 s applied, then words.js emitted. **أرقام / params:** --offset −0.08; --min-gap 0.02; min word 20 ms
- **الدليل / proof:** `kosif-tool/tools/words_convert.py` · `kosif-tool/tools/words_convert.py:122` · `kosif-tool/playbooks/audio-sync.md:27`

#### SYNC-04 · حدود تسامح التزامن · Sync tolerances · ✅ مُثبت هنا / proven here
- **ماذا / what:** الحركة تبدأ قبل الكلمة بـ 40–80 ms، والكلمة المفتاحية ≤ 100 ms، والباقي ≤ 150 ms، ولا قطع وسط كلمة، ولا حركة قبل أن تُسمع. — Motion starts 40–80 ms before the word; key words ≤ 100 ms, others ≤ 150 ms; never cut mid-word; never animate before it is heard.
- **متى أستخدمها / when:** مراجعة كل فيلم متزامن — reviewing every synced film.
- **كيف / how:** offset_ms = |word.start − motion_frame/fps| × 1000 ≤ 100 for emphasis words; visual lead ≤ 80 ms; pauses > 400 ms end a phrase, > 600 ms allow a scene change, > 1.5 s need ambient motion. Log it in templates/TEST_REPORT.md. Measured in the proof: max |Δ| 33 ms (one frame), 0 early words; the spectrum film filled every word ≤ 35 ms after its start. **أرقام / params:** lead 40–80 ms; key ≤ 100 ms; others ≤ 150 ms
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:29` · `kosif-tool/playbooks/audio-sync.md:34` · `kosif-tool/templates/TEST_REPORT.md` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`

#### SYNC-05 · قياس التزامن إطارًا بإطار · Frame-by-frame sync probe · ✅ مُثبت هنا / proven here
- **ماذا / what:** يبحث كل إطار في الصفحة ويسجل أول إطار تظهر فيه كل كلمة، ثم يقارنه بزمن نطقها. — Seeks every frame of the page and records when each word first becomes visible, then compares it with its spoken start.
- **متى أستخدمها / when:** قبل التسليم في أي فيلم كلمات — before delivering any word-synced film.
- **كيف / how:** node proofs/arabic-voice-kinetic/sync_probe.cjs index.html 30 100 → 'SYNC OK words=15 max|delta|=33 ms early=0'. Requires a deterministic window.__kosif.seek(t). Re-run whenever words.json changes. **أرقام / params:** fps 30; tolerance 100 ms
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/sync_probe.cjs` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`

#### SYNC-06 · التحقق من توقيت جاهز · Pre-timed transcript validation · 🟢 جاهز / ready
- **ماذا / what:** يقبل words.json خارجيًا فقط إذا كان محدودًا ومتصاعدًا، فيعمل الريل بلا Whisper لكن لا بتوقيت مخترع. — Accepts an external words.json only if bounded and monotonic, so reels can run without Whisper but never with invented timing.
- **متى أستخدمها / when:** المستخدم أرسل توقيتًا من أداة أخرى — timing from another tool.
- **كيف / how:** reel --transcript NAME.words.json → transcribe.load_transcript. **أرقام / params:** ≤ 10 MB; ≤ 20,000 segments; tolerance 0.02 s; end ≤ duration + 0.15 s
- **الدليل / proof:** `kosif-studio/motion/transcribe.py:89`

## التفريغ والمحاذاة — Transcription & alignment

_من صوت إلى كلمات بتوقيتها: Whisper متعدد اللغات، محاذاة النص الصحيح، وتصحيح لا يكسر التوقيت._

#### SYNC-07 · تفريغ عربي محلي بتوقيت الكلمات · Local Arabic word-timed transcription (faster-whisper) · ✅ مُثبت هنا / proven here
- **ماذا / what:** صوت إلى مقاطع وكلمات بزمن بداية ونهاية واحتمال، دون إنترنت بعد تنزيل النموذج. — Speech → segments and words with start/end/probability, offline once the model is cached.
- **متى أستخدمها / when:** أي صوت بشري يحتاج ترجمة أو تزامن — any human voice to caption or sync.
- **كيف / how:** python transcribe.py SRC --model large-v3|small|auto --lang ar [--prompt '…'] → words.json + SRT (UTF-8 BOM) + captions.json; 16 kHz mono, CPU int8, beam 5, vad_filter, BatchedInferencePipeline batch 8 (≈ 3–4× faster). Ran here in the proof venv (small): 15/15 words matched the script, but starts were early by a median 135 ms and up to 670 ms after pauses → snap to onsets or prefer a forced aligner; human-voice error measured ~±150 ms (median 103, max 258). **أرقام / params:** 16 kHz mono; batch 8; error ~±150 ms
- **الدليل / proof:** `kosif-studio/motion/transcribe.py:36` · `100-superskills/skills/kosif-montage-motion/scripts/transcribe.py` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/transcribe.py` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`
- **📦 تثبيت / install:** `pip install faster-whisper  # models from huggingface.co (reachable): small 466 MB, large-v3 3.1 GB`

#### SYNC-08 · فخ نماذج .en · The .en model trap · 📄 موصوف / documented only
- **ماذا / what:** نماذج Whisper ذات اللاحقة .en تترجم الكلام غير الإنجليزي إلى الإنجليزية بصمت بدل تفريغه. — Whisper models ending in .en silently translate non-English speech into English instead of transcribing it.
- **متى أستخدمها / when:** قبل أي تفريغ عربي — before any Arabic transcription.
- **كيف / how:** Always pass --model explicitly (the HyperFrames CLI defaults to small.en!) with --language ar. Ladder: tiny 75 MB (pipeline test), base 142 MB, small 466 MB (default), medium 1.5 GB (noisy/music, minimum for lyrics), large-v3 3.1 GB (production), turbo = speed/accuracy sweet spot. Parakeet covers 25 European languages only — Arabic goes through Whisper. Convert to 16 kHz WAV first. **أرقام / params:** tiny 75 MB … large-v3 3.1 GB
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transcript-guide.md` · `kosif-one/vendor/hyperframes/skills/media-use/audio/references/transcribe.md`

#### SYNC-09 · توقيت حقيقي من فونيمات Piper · True word timing from Piper phonemes · ✅ مُثبت هنا / proven here
- **ماذا / what:** عند توليد الصوت بـ Piper تعطي مدة كل فونيم توقيت الكلمات الحقيقي بلا تفريغ. — When the voice is synthesised with Piper, phoneme durations give exact word timing without ASR.
- **متى أستخدمها / when:** صوت مولّد لفيلم كلمات — a generated voice for a word film.
- **كيف / how:** synth_voice.py (length_scale 0.95, 0.30 s between sentences) → align_words.py → words.json; Whisper stamps stay in asr_start for audit. Proof: max |Δ| 33 ms, 0 early. Piper noise is unseeded, so make_voice.sh regenerates voice and words.json together. **أرقام / params:** length_scale 0.95; 0.30 s sentence gap
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/synth_voice.py` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/align_words.py` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/make_voice.sh`
- **📦 تثبيت / install:** `pip install piper-tts`

#### SYNC-10 · محاذاة النص الصحيح على التفريغ · True-text alignment onto ASR · ✅ مُثبت هنا / proven here
- **ماذا / what:** يضع كلمات الأغنية أو القصيدة أو الدعاء الصحيحة (بالتشكيل) على أزمنة كلمات التفريغ. — Puts the real lyrics/poem/dua words (with diacritics) onto recognised word times.
- **متى أستخدمها / when:** قرآن، دعاء، شعر، أغنية — Quran, dua, poetry, songs (always the user's exact text).
- **كيف / how:** verse.align(lines, asr) via difflib.SequenceMatcher on normalised words: equal or one-to-one blocks inherit times, uneven replacements share the span by length, missed words spread between timed neighbours; then verse.segment cuts lines before phrase openers, ≤ 7 words, never ending on a particle. Ran here: test_verse_reads_a_text_like_a_lyricist ok and tests.test_directors ok. Basma's bridge variant aligns with an LCS table and rejects matches below 40%. **أرقام / params:** fill step ≥ 0.05 s; min word 0.05 s; ≤ 7 words/line
- **الدليل / proof:** `kosif-studio/motion/verse.py:83` · `kosif-studio/tests/test_studio.py:943` · `100-superskills/skills/kosif-montage-motion/tests/test_directors.py:42` · `app/public/js/00_editor.js:2684`

#### SYNC-11 · تصحيح الكلمات مع حفظ التوقيت · Transcript fixes that keep timing · 🟢 جاهز / ready
- **ماذا / what:** يستبدل العبارات المسموعة خطأ وينشر الكلمات الصحيحة على المدى الأصلي. — Replaces misheard phrases while spreading the right words over the original span.
- **متى أستخدمها / when:** لهجة مصرية أو خليجية أساء Whisper سماعها — dialect words Whisper misheard.
- **كيف / how:** --fix "ما حدش=محدش;بتعودش ضايع=متقعدش تضيّع" (direct, verse); merge split clitics and attached punctuation into displayable words; for the Quran use the user's exact text, never the ASR.
- **الدليل / proof:** `kosif-studio/motion/direct.py:205` · `kosif-studio/tests/test_studio.py:910` · `kosif-tool/playbooks/audio-sync.md:76`

#### SYNC-12 · ضبط بداية الكلمة على النطق · Onset snapping of word stamps · 📄 موصوف / documented only
- **ماذا / what:** طوابع النماذج تتأخر أو تتقدم عن بداية النطق المسموع؛ اربط كل كلمة بأقرب بداية صوتية. — Model stamps drift from the audible onset; snap each word to the nearest detected vocal onset.
- **متى أستخدمها / when:** أغانٍ وكلمات تضرب على الحرف — lyrics that must pop on the consonant.
- **كيف / how:** Spectral-flux / energy-derivative onset detection near each stamp (±120 ms), keep the original in 'stamp', render one frame per word onset on a sheet to verify. Reported lag 50–80 ms for sung vocals; our Whisper run was early instead (median 135 ms) — measure which way yours drifts before correcting. **أرقام / params:** search ±120 ms; lag 50–80 ms
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`

#### SYNC-13 · تجهيز الصوت للتفريغ وفخ التوقيت · STT audio prep & its timing trap · 📄 موصوف / documented only
- **ماذا / what:** للتفريغ فقط: مرشح 200 Hz–3 kHz و16 kHz أحادي؛ لكن حذف الصمت أو تسريع الصوت يكسر التوقيت. — For transcription only: 200 Hz–3 kHz band and 16 kHz mono; silence removal or speed-up breaks the timeline.
- **متى أستخدمها / when:** صوت مزعج أو تفريغ سحابي مدفوع — noisy audio or paid cloud STT.
- **كيف / how:** ffmpeg -af 'highpass=f=200,lowpass=f=3000' -ar 16000 -ac 1 -c:a pcm_s16le. Silence removal (0.5 s at −30 dB) saves 10–40% of billed minutes and atempo 1.25 another 20%, but never use those outputs for words.json — always transcribe or align against the untouched original. **أرقام / params:** 16 kHz mono; HPF 200 / LPF 3000
- **الدليل / proof:** `kosif-atlas/skills/1845-deepgram-pack/5468-deepgram-cost-tuning/SKILL.md`

#### SYNC-14 · تفريغ سحابي مع فصل المتحدثين · Cloud STT with diarisation · 🔑 مفتاح أو خدمة / needs key or service
- **ماذا / what:** عند الحاجة لأسماء المتحدثين أو سرعة عالية: خدمات تفريغ مستضافة بتوقيت كلمات. — When speaker labels or fast turnaround matter: hosted ASR with word timings.
- **متى أستخدمها / when:** بودكاست بعدة متحدثين — multi-speaker podcasts.
- **كيف / how:** Deepgram nova-3 (smart_format, diarize, utterances), ElevenLabs scribe_v1 (diarize + word timestamps), AssemblyAI (speaker labels), Together whisper-large-v3 (80 MB upload / 4 h per request), Gemini verbatim segments of 3–8 words (≤ 18 MB inline). Normalise to [{text,start,end,speaker}] then words_convert. Each needs its own API key.
- **الدليل / proof:** `kosif-atlas/skills/1845-deepgram-pack/5473-deepgram-hello-world/SKILL.md` · `kosif-atlas/skills/1847-elevenlabs-pack/5515-elevenlabs-core-workflow-b` · `app/public/js/00_editor.js:1525`

#### SYNC-15 · تفريغ HyperFrames · HyperFrames transcribe CLI · 📦 بأمر تثبيت / one install
- **ماذا / what:** أمر واحد يفرّغ بـ Parakeet أو whisper.cpp ويخرج SRT/VTT أو كلمات. — One command transcribing via Parakeet or whisper.cpp to SRT/VTT or words.
- **متى أستخدمها / when:** داخل مشاريع HyperFrames — inside HyperFrames projects.
- **كيف / how:** npx hyperframes transcribe talk.mp4 --engine whisper --model small --language ar [--to srt|vtt]; also normalises existing .srt/.vtt/openai.json into a word array. Never rely on the default model (small.en).
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/scripts/transcribe.mjs` · `kosif-one/vendor/hyperframes/skills/media-use/references/operations.md`
- **📦 تثبيت / install:** `npx hyperframes transcribe <file> --engine whisper --model small --language ar`
- **⚖️ ترخيص / license:** Apache-2.0

#### SYNC-16 · كشف الإعادات وتجميع المونتاج من النص · Retake detection & transcript-driven assembly · 📄 موصوف / documented only
- **ماذا / what:** الإعادات = مقاطع تبدأ بنفس الحروف العشرة خلال 60 ث، ويُحتفظ بالأخيرة؛ ثم يُبنى المونتاج من جدول نبضات بالنص. — Retakes = segments with the same first 10 characters within 60 s, keeping the last; then the edit is assembled from a transcript beat sheet.
- **متى أستخدمها / when:** تسجيلات طويلة بأخطاء وإعادات — long recordings with flubs and retakes.
- **كيف / how:** Inventory clips → beat sheet (beat | message | voice range | screen | length) for approval → assemble in beat order with a chapter marker per beat; keep an 'unused sentences' list; the first beat poses the question within 10 s. Never pick a non-default take without asking. Record narration at 48 kHz, ~1 s between sentences, clap once for multi-camera sync. **أرقام / params:** prefix 10 chars; window 60 s; hook ≤ 10 s
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2451-davinciresolve-beats-devtalk/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2447-akbun-vlog-shootplan/SKILL.md`

## توقيت بلا تفريغ — Timing without ASR

_عندما لا يوجد Whisper: قدّر بصدق ووسم التقدير، ولا تدّعِ توقيتًا لم تقسه._

#### SYNC-17 · توزيع النص على مقاطع الصوت · Text over voiced spans (estimated) · 🟢 جاهز / ready
- **ماذا / what:** بلا تفريغ: يضع النص على الأجزاء المسموعة بالترتيب وحسب طول الكلمة، ويسمّي النتيجة تقديرًا. — Without ASR, lays the text over the voiced stretches in order and by word length, and labels it estimated.
- **متى أستخدمها / when:** نص معروف وصوت بلا Whisper — known text, no ASR available.
- **كيف / how:** verse.voiced_spans + estimate: 50 ms frames, threshold max(−45 dB, p20+6 dB), merge gaps < 0.35 s, spans > 0.15 s. Browser variants: Basma syncToSpeech (new segment after 5 words or a > 0.3 s gap) and region detection (thr max(0.008, 0.22·p90), merge 0.28 s, min 0.18 s). Voice2Motion marks such timing estimated_from_text_length_NOT_ASR. **أرقام / params:** frames 50 ms; merge < 0.35 s
- **الدليل / proof:** `kosif-studio/motion/verse.py:121` · `kosif-studio/motion/verse.py:145` · `app/public/js/00_editor.js:1096`

#### SYNC-18 · توقيت الكلمات حسب الطول · Word timing by length · ✅ مُثبت هنا / proven here
- **ماذا / what:** إذا كان للسطر زمن بلا أزمنة كلمات، يُقسم بين كلماته حسب عدد الحروف زائد ثابت. — When a caption line has no word times, its span is shared among words by letter count plus a constant.
- **متى أستخدمها / when:** SRT بلا كلمات — phrase-level SRT.
- **كيف / how:** montage.word_times with weight = len(word) + 2. Covered by test_montage_cuts_on_the_beat_and_captions_shape_arabic (ran here, ok). **أرقام / params:** weight = len + 2
- **الدليل / proof:** `kosif-studio/motion/montage.py:341` · `kosif-studio/tests/test_studio.py:765`

#### SYNC-19 · ميزانية الكلمات حسب الزمن · Narration word budgets · 📄 موصوف / documented only
- **ماذا / what:** حوّل المدة إلى عدد كلمات قبل كتابة التعليق كي لا تزدحم المشاهد. — Turn duration into a word budget before writing narration so scenes are not over-stuffed.
- **متى أستخدمها / when:** كتابة سكريبت لصوت مولّد — scripting for a generated voice.
- **كيف / how:** ~150 words/min long-form; short-form 80–150 words for 20–45 s; per scene: 3–4 s → 8–12 words, 5–6 s → 15–22, 7–8 s → 22–30. Generated talking segments: words/2 s (≈ 2 wps), minimum 4 s, split above 15 s at a sentence. For Arabic measure the real TTS duration and retime from words.json rather than trusting counts; or generate TTS per sentence and set each scene to its clip length. **أرقام / params:** 150 wpm; ≈ 2 words/s
- **الدليل / proof:** `kosif-atlas/skills/166-demo-video/535-demo-video/references/scene-design-system.md` · `kosif-atlas/skills/259-quickdesign/865-quickdesign` · `style:pm-linearuncle-5d2bae`

#### SYNC-20 · سكريبت بتوقيت مكتوب · Timestamped script parser · ✅ مُثبت هنا / proven here
- **ماذا / what:** يقبل أسطرًا مثل «0–3s: نص» ويوزع الكلمات على مقاطع 8/10 ث حسب البداية، ويرفض التوقيت الناقص أو المتداخل. — Accepts lines like '0–3s: text' and assigns words to 8/10 s clips by start time; rejects partial or overlapping stamps.
- **متى أستخدمها / when:** المستخدم كتب التوقيت بنفسه — the user wrote timings in the script.
- **كيف / how:** parseTimestamps regex ^(\d+(\.\d+)?)\s*[–—-]\s*(\d+(\.\d+)?)s?\s*:\s*(.+)$; clip index floor(start/len). Ran here: node --test tests/production-profiles.test.mjs → pass 10, fail 0.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:67-77` · `fastify-motion-bro/tests/production-profiles.test.mjs:75-81`

## قواعد تصميم الترجمة — Caption design rules

_كم كلمة، أين، بأي حجم، ومتى تختفي — قبل اختيار أي ستايل._

#### SYNC-21 · تجميع الكلمات حسب الطاقة · Word grouping by energy · 📄 موصوف / documented only
- **ماذا / what:** طاقة عالية 2–3 كلمات، حوار 3–5، هدوء 4–6؛ والانقسام عند نهاية الجملة أو وقفة ≥ 150 ms. — High energy 2–3 words, conversational 3–5, calm 4–6; break on sentence ends or pauses ≥ 150 ms.
- **متى أستخدمها / when:** كل ترجمة — every caption track.
- **كيف / how:** Pages of ~1200 ms (Remotion createTikTokStyleCaptions combineTokensWithinMilliseconds 1200); one group visible at a time; Claude splits 2–5 words at natural pauses without separating prepositions and stars one word per line. Arabic: ≤ 6 words per screen in reels. **أرقام / params:** 2–3 / 3–5 / 4–6 words; pause 150 ms; page 1200 ms
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md` · `kosif-atlas/skills/2712-remotion/10431-remotion-captions/display-captions.md` · `app/public/js/00_editor.js:1510`

#### SYNC-22 · موضع آمن وضمان الاختفاء · Safe placement & exit guarantee · 📄 موصوف / documented only
- **ماذا / what:** الترجمة في المنطقة الآمنة، لا تغطي الوجوه، ومجموعة واحدة ظاهرة، وكل مجموعة تُخفى قسرًا عند نهايتها. — Captions sit in safe zones, never over faces, one group at a time, each force-hidden at its end.
- **متى أستخدمها / when:** كل ترجمة محروقة — every burned caption.
- **كيف / how:** 16:9: 80–120 px from the bottom; 9:16: ~600–700 px from the bottom (keep ≥ 280 px clear of platform UI); full-width absolute container, overflow visible; exit tween 0.12 s then set opacity 0 + visibility hidden at group end; self-lint by seeking end + 0.01 s. fitTextFontSize maxWidth 1600/900, base 78, min 42, step 2. Basma 'auto' places captions in the third farthest from the tracked subject. **أرقام / params:** 16:9 bottom 80–120 px; 9:16 ~600–700 px; exit 0.12 s
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/montage_grammar.md` · `app/public/js/00_editor.js:2906`

#### SYNC-23 · ستايل الترجمة حسب نبرة الكلام · Caption style by tone · 📄 موصوف / documented only
- **ماذا / what:** اقرأ النص، حدد النبرة، ثم اختر الوزن والدخول واللون والحجم. — Read the transcript, detect tone, then pick weight, entrance, colour and size.
- **متى أستخدمها / when:** اختيار ستايل الترجمة — choosing a caption style.
- **كيف / how:** Hype: 800–900 weight, scale-pop back.out(1.7) 0.1–0.2 s, 72–96 px. Corporate: 600–700, fade+slide power3.out 0.3 s, 56–72 px. Tutorial: mono 500–600, typewriter 0.4–0.5 s, 48–64 px. Story: serif 400–500, slow fade 0.5–0.6 s, 44–56 px. Social: rounded 700–800, elastic word-by-word, 56–80 px. Entry tones (stagger/hold): documentary 150/600 ms, conversational 80/400, energetic 50/300 pop, poetic 250/1200 etch. Soft = fade + 8 px drift; present = 6 px + 1.04 pop. **أرقام / params:** 44–96 px by tone
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/references/motion-vocabulary.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/references/typography-presets.md`

#### SYNC-24 · وضوح الترجمة العربية · Arabic caption legibility · 📄 موصوف / documented only
- **ماذا / what:** الكلمة المنطوقة بلون مميز والباقي أبيض، حد أسود سميك وظل عميق، 5–7 كلمات، تباين ≥ 4.5:1. — Spoken word in a highlight colour, rest white; thick black outline and deep shadow; 5–7 words; contrast ≥ 4.5:1.
- **متى أستخدمها / when:** كل ترجمة عربية — every Arabic caption.
- **كيف / how:** Highlight #FFDE59 or #38BDF8; outline 6–8 px; Cairo, Noto Sans/Kufi/Naskh Arabic, Almarai; subtitles ≤ 42 chars/line, 1–2 lines, 1–7 s each. When there is no stroke, sample the caption band every 6th frame and add a dark/light plate only as strong as needed for 4.5:1 (max alpha 0.75). Bilingual block: Arabic on top RTL, English below LTR at 70% size, each with its own dir. **أرقام / params:** ≤ 42 chars; 1–7 s; ≥ 4.5:1
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/montage_grammar.md` · `app/public/js/00_editor.js:3007` · `kosif-tool/playbooks/arabic-typography.md:46`

#### SYNC-25 · لا تغيّر كلام المتحدث، والحرق عند الطلب · Verbatim words; burn only when asked · 📄 موصوف / documented only
- **ماذا / what:** الترجمة تعيد كلام المتحدث حرفيًا، والترجمة المحروقة فقط عند الطلب وإلا SRT/VTT جانبي. — Captions reproduce the speaker's words exactly; burn only on request, otherwise ship SRT/VTT sidecars.
- **متى أستخدمها / when:** كل تسليم فيه كلام — every delivery with speech.
- **كيف / how:** Diff caption text vs words.json in QA. Default deliverables: .srt + .vtt; soft track inside MP4: -c:s mov_text -metadata:s:s:0 language=ara (ran here: stream tagged 'ara'). Accessibility package: speech + [sound] cues, audio-description notes for visual-only beats.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md` · `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md` · `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### SYNC-26 · إبراز تلقائي للكلمات المهمة · Automatic emphasis words · 🟢 جاهز / ready
- **ماذا / what:** الأرقام والأسماء والكلمات العاطفية تُبرز، وفي السطر بلا إبراز تُختار الكلمة عند أعلى قمة صوت. — Numbers, brands and emotional words get emphasis; in lines without one, the word at the loudest local peak is starred.
- **متى أستخدمها / when:** اختيار الكلمة البطلة في كل سطر — picking each line's hero word.
- **كيف / how:** autoEm wraps any word with a digit in *…*; loudPeaks: 0.25 s smoothed dB envelope, local maxima ≥ 4 dB above the median within ±3 s, ≥ 1.2 s apart, 3–12 per clip; the starred word gets accent + bigger scale + overshoot. Karaoke intensity ladder: high energy = accent + glow + 15% pop; low = warm white + 3%. **أرقام / params:** ≥ 4 dB over median; spacing 1.2 s; pop 15% / 3%
- **الدليل / proof:** `app/public/js/00_editor.js:1875` · `app/public/js/00_editor.js:3032` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/dynamic-techniques.md`

## ترجمة كاريوكي محروقة — Burned karaoke captions (ASS)

_ترجمة عربية تُحرق بلا متصفح: حدث لكل كلمة، Encoding −1، وسبعة ستايلات جاهزة._

#### SYNC-27 · كاريوكي ASS عربي بحدث لكل كلمة · Arabic ASS karaoke, one event per word · ✅ مُثبت هنا / proven here
- **ماذا / what:** ترجمة محروقة يتلون فيها المنطوق وينبض، بحدث ASS لكل كلمة فيبقى التشكيل والترتيب سليمين. — Burned captions where the spoken word changes colour and pops, one ASS event per word so shaping and order stay intact.
- **متى أستخدمها / when:** ريلز وفيديوهات كلام — reels and talking videos.
- **كيف / how:** python montage.py captions VIDEO --spec caps.json --style reels|cinema|punchy|tiktok|hormozi|boxed|minimal (also inside cut/voicecut/reel). One Dialogue per word: {\1c<hi>\fscx112\fscy112\t(0,120,\fscx100\fscy100)}word; Encoding −1 (auto paragraph direction), WrapStyle 2, side margins 6% W, ≤ 6 words on screen, sizes scale with the short side; burn ass=caps.ass with fontsdir= (no Arabic system fonts here), crf 17, audio copied. Ran here: test_montage_cuts_on_the_beat_and_captions_shape_arabic ok (see ARAB-62 for the order check). **أرقام / params:** pop 112%→100% / 120 ms; ≤ 6 words; Encoding −1
- **الدليل / proof:** `kosif-studio/motion/montage.py:353` · `kosif-studio/motion/montage.py:381` · `kosif-studio/tests/test_studio.py:765`

#### SYNC-28 · سبعة ستايلات ترجمة جاهزة · Seven named caption styles · ✅ مُثبت هنا / proven here
- **ماذا / what:** reels وcinema وpunchy وtiktok وhormozi وboxed وminimal بخطوط Noto العربية وألوان وأحجام مضبوطة. — reels, cinema, punchy, tiktok, hormozi, boxed and minimal with Noto Arabic faces, colours and sizes tuned.
- **متى أستخدمها / when:** اختيار شكل الترجمة بكلمة واحدة — picking a caption look in one word.
- **كيف / how:** montage.ass(spec, 1080, 1920, style); colours are ASS &HAABBGGRR; sizes per 1080 px of the short side, margins per 1920 of height. Ran here: tests.test_v6 StyleAndRegistryTests.test_caption_styles ok. Table below. **أرقام / params:** see the style table
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/montage.py:308` · `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:170` · `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:13`

#### SYNC-29 · صفحات ترجمة + SRT/VTT/ASS · Caption pages → JSON/SRT/VTT/ASS · ✅ مُثبت هنا / proven here
- **ماذا / what:** يحوّل كلمات Whisper أو SRT إلى صفحات ~1200 ms ويكتب JSON وSRT وVTT وASS كاريوكي. — Turns Whisper word stamps (or SRT) into ~1200 ms pages and writes JSON, SRT, VTT and ASS karaoke.
- **متى أستخدمها / when:** تسليم ملفات ترجمة لكل المنصات — caption files for every platform.
- **كيف / how:** python captions_pages.py words.json --page-ms 1200 --max-chars 42 --rtl --out captions. Ran here: 6 Arabic words → 2 pages, 4 files. Caveat found here: it expects [{text,start,end}] — a KOSIF words.json ({word,…}) raises KeyError 'text'; rename the key first. Its ASS uses \k per page; for burned Arabic prefer one event per word (SYNC-27). **أرقام / params:** 42 chars, 2 lines, 1–7 s per page
- **الدليل / proof:** `100-superskills/skills/audio-reactive-captions-studio/scripts/captions_pages.py:95` · `100-superskills/skills/audio-reactive-captions-studio/references/captions-rules.md`

#### SYNC-30 · معايرة حجم ASS · ASS PlayRes calibration · 📄 موصوف / documented only
- **ماذا / what:** دقة السكربت الافتراضية في SRT/libass تغيّر الحجم والهامش؛ عاير على إطارات 1080×1920 حقيقية. — libass's default script resolution rescales FontSize and MarginV; calibrate on real 1080×1920 frames.
- **متى أستخدمها / when:** عندما تبدو الترجمة ضخمة أو صغيرة جدًا — captions look too big or small.
- **كيف / how:** Set PlayResX/PlayResY = the frame; preview frames before the full burn; smaller white Arabic with black outline/shadow, bottom safe zone, no opaque box. Quick SRT burn: subtitles=captions.srt:force_style='FontName=Cairo,FontSize=22,Outline=2,MarginV=60' (sizes relative to the 384×288 default).
- **الدليل / proof:** `kosif-studio/motion/references/voice-open-footage-upgrade-2026-10-10.md` · `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### SYNC-31 · كاريوكي \k بشرائح متساوية · Even-slice \k karaoke (omni) · 🟢 جاهز / ready
- **ماذا / what:** ستايلات tiktok/cinema/punchy تقسم الزمن بالتساوي بين الكلمات — شكل كاريوكي لا تزامن حقيقي. — tiktok/cinema/punchy styles split time evenly between words — a karaoke look, not true sync.
- **متى أستخدمها / when:** عندما لا يوجد توقيت كلمات — when no word timings exist.
- **كيف / how:** python scripts/smart_montage.py captions video.mp4 --spec captions.json --style tiktok (Cairo 68, outline 6, MarginV 280); \k per word = max(10 cs, duration/len(words)). Feed words.json times for real sync; label even-split timing as estimated. **أرقام / params:** \k ≥ 10 cs
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/smart_montage.py:91`

**ستايلات ASS السبعة / the seven ASS styles** (1080×1920؛ الأحجام لكل 1080 من الضلع القصير):

| style | الخط / font | الحجم | التمييز / highlight | النبضة / pop | حدود | كلمات | الاستخدام |
|---|---|---|---|---|---|---|---|
| reels | Noto Sans Arabic | 74 | أصفر #FFDE59 | 112% | outline 6, shadow 3, margin 300 | ≤ 6 | الافتراضي للريلز |
| cinema | Noto Naskh Arabic | 46 | ناعم #FFE6A8 | 104% | outline 3, margin 150 | ≤ 6 | أفلام هادئة |
| punchy | Noto Kufi Arabic | 72 | سماوي #38BDF8 | 116% | outline 8, margin 330 | ≤ 6 | تحفيزي |
| tiktok | Noto Kufi Arabic | 84 | #FFE04D | 120% / 90 ms | outline 10 | ≤ 4 | تيك توك |
| hormozi | Noto Kufi Arabic | 96 | أخضر #39FF88 | 118% / 80 ms | outline 9, margin 440 | 1 | كلمة كلمة |
| boxed | Noto Sans Arabic | 66 | — | 108% | صندوق &H66000000 | ≤ 5 | خلفيات مزدحمة |
| minimal | Noto Naskh Arabic | 54 | بلا | 100% | outline 2 | ≤ 7 | مقابلات |

## ترجمة حركية في HTML وRemotion — Kinetic captions in HTML & Remotion

_الكلمة تدخل على موعد نطقها بقناع كامل الكلمة — مُقاسة إلى إطار واحد في أفلام الإثبات._

#### SYNC-32 · دخول الكلمة على بداية نطقها · Word enters on its spoken start · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل كلمة تُكشف بقناع ناعم من اليمين مع صعود نابض وضباب يتلاشى، فتظهر في أول إطار بعد بداية نطقها. — Each word reveals through a soft right-to-left mask with a spring rise and de-blur, visible on the first frame at or after its start.
- **متى أستخدمها / when:** أفلام الكلمات من الصوت، الشعر، الخطب — word films from voice, poetry, speeches.
- **كيف / how:** Per word from words.json: mask wipe 0.42 s RTL over the whole word (never letters), spring rise 34 px (k = 180, c = 19), blur 9 → 0 px, opacity floor 12% so it shows on its first frame; key words turn gold #ffc56e with 28/70 px glow and an inOutCubic underline over the spoken length; finished sentences dim to 30% (keys 78%). Proof film: max |Δ| 33 ms, 0 early. **أرقام / params:** mask 0.42 s; rise 34 px; spring 180/19
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/index.html` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`

#### SYNC-33 · تعبئة كاريوكي من اليمين بقناع كامل الكلمة · RTL karaoke fill with whole-word clip-path · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل كلمة تمتلئ بالذهبي من اليمين إلى اليسار عبر clip-path يغطي الكلمة كلها فلا تنفصل الحروف. — Each word fills gold right-to-left through a whole-word clip-path so joined letters never split.
- **متى أستخدمها / when:** كاريوكي عربي في HTML — Arabic karaoke in HTML.
- **كيف / how:** Cairo 800 at 60 px; clip-path inset animates across the word's spoken duration; the old line leaves 0.02 s after its last word and the next arrives 0.2 s before its first word, so two lines never overlap. Measured: every fill starts ≤ 35 ms after the spoken start. Caveat: the reveal edge may pass mid-word (letters stay joined). **أرقام / params:** line out +0.02 s; next in −0.2 s
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/audio-reactive-spectrum/index.html` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/audio-reactive-spectrum/README.md`

#### SYNC-34 · كاريوكي الكبسولة في starter الكانفس · Canvas karaoke pill (html-canvas starter) · ✅ مُثبت هنا / proven here
- **ماذا / what:** الجملة كاملة ظاهرة، والكلمة الحالية كبسولة فيروزية بنص داكن تنبض، والمنطوق أبيض والقادم باهت. — The whole phrase shows; the current word becomes a teal pill with dark text and a pop, past words white, future muted.
- **متى أستخدمها / when:** ترجمة سريعة جاهزة في kosif-tool — quick ready captions in kosif-tool.
- **كيف / how:** phrases(words, 0.45) splits at pauses > 0.45 s; show from start − 0.15 to end + 0.5 with a 0.15/0.3 fade window; pop outBack 0.96 → 1.08 over 140 ms. Rendered in the scaffolded starter through render_html.cjs. **أرقام / params:** 64 px 700; pill r 22 pad 6×18; on #7ee8d2 text #0b1020; done #f3f7ff; upcoming #9fb0cc; bottom 210 px
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:181` · `kosif-tool/starters/html-canvas/timeline.js:82`

#### SYNC-35 · ترجمة Remotion بالكلمة مع كشف الاتجاه · Remotion word captions with bidi detection · 📦 بأمر تثبيت / one install
- **ماذا / what:** يحمّل words.json ويجمعها في بطاقات (≤ 4 كلمات أو صمت > 0.6 ث)، يظهرها مبكرًا 0.15 ث، والكلمة النشطة تنبض 1.1×؛ الاتجاه من أول حرف قوي. — Loads words.json, groups cards (≤ 4 words or > 0.6 s silence), shows them 0.15 s early, springs the active word to 1.1×; direction from the first strong character.
- **متى أستخدمها / when:** أفلام Remotion — Remotion films.
- **كيف / how:** <Captions accent lang file maxWordsPerLine={4} gapSeconds={0.6} holdSeconds={0.35} leadSeconds={0.15}/>; spring damping 12, stiffness 220, mass .7; upcoming words 42% opacity. TikTok pages alternative: @remotion/captions createTikTokStyleCaptions (1200 ms) with the active token #39E508. SyncedLine: whole words spring in at start − 0.06 s. **أرقام / params:** 58 px 700 on rgba(8,10,16,.66) r 30; bottom 260 px
- **الدليل / proof:** `kosif-tool/starters/remotion/src/Captions.tsx:135` · `kosif-tool/starters/remotion/src/Captions.tsx:39` · `kosif-tool/playbooks/kinetic-type.md:57-75`
- **📦 تثبيت / install:** `cd kosif-tool/starters/remotion && npm install`
- **⚖️ ترخيص / license:** Remotion برخصة الشركة؛ @remotion/captions نفسها MIT / Remotion company license; @remotion/captions itself is MIT.

#### SYNC-36 · كلمات على مقاطعها مع كلمات ذهبية · Syllable-timed speech captions with gold keywords · 🟢 جاهز / ready
- **ماذا / what:** كل كلمة تصعد من ضبابية على زمنها، والكلمات المفتاحية بلون التمييز، والعبارة تخرج للأعلى قبل التالية. — Each word rises from blur on its own time, keywords in the accent colour, and the phrase exits upward before the next.
- **متى أستخدمها / when:** ريل كلام مصقول فوق لقطة — a polished talking reel over footage.
- **كيف / how:** speech(el, [[word, t], …], accentWords): each word in a .wm clip-path mask; fromTo y 18 → 0, blur 6 → 0, 0.28 s power3.out at t − 0.04; exit opacity 0, y −14 in 0.22 s power3.in. Hand-corrected variant: phrases with <b>keyword</b> in gold #f5c97a, yPercent 105 → 0 in 0.32 s, out at next start − 0.16 s. **أرقام / params:** rise 18 px, blur 6 px, 0.28 s, lead 0.04 s; accent #E7B65A
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:171` · `100-superskills/skills/kosif-montage-motion/templates/directed.html:73` · `kosif-one/projects/whatsapp-motion/projects/success/index.html:156-205`

#### SYNC-37 · سطر شبحي يضيء كلمة بكلمة · Ghost-to-lit line · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** السطر كاملًا بشفافية 25% أو رمادي، وكل كلمة ترتفع إلى 100% أو تبيضّ عند زمنها. — The whole line at 25% opacity (or grey); each word lifts to 100% (or white) at its time.
- **متى أستخدمها / when:** شرح هادئ أو سبورة — calm explainers and whiteboards.
- **كيف / how:** Grey #555 → white (emphasis orange #f27525) with a 120 ms fade; or 25% → 100% in 150–200 ms; ≤ 2 lines; never split letters. Peach rounded highlight box on the target word (80 ms colour transition, padding 2×6 px) for language-learning looks. **أرقام / params:** fade 120–200 ms
- **الدليل / proof:** `style:plotter` · `style:doodle` · `style:pm-1stnoel-c20a89`

#### SYNC-38 · صندوق ينتقل للكلمة النشطة · Word-hop highlight box · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** صندوق مستدير بلون العلامة ينزلق إلى الكلمة المنطوقة. — A rounded brand-coloured box slides to the spoken word.
- **متى أستخدمها / when:** ترجمة ريلز حديثة — modern reel captions.
- **كيف / how:** Box padding 6 px, slide 80 ms from words.json; TikTok-style red box #ff1745 in 0.08–0.16 s (HyperFrames caption-highlight); colour-only variant for calm content. **أرقام / params:** slide 80 ms; pad 6 px
- **الدليل / proof:** `style:pm-gautam-mer1-2ae354` · `kosif-one/vendor/hyperframes/registry/components/caption-highlight/caption-highlight.html`

#### SYNC-39 · ترجمة تُكتب لحظة النطق · Voice-timed typewriter captions · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** حروف كل كلمة تُكتب بدءًا من بداية نطقها وموزعة على مدتها، بمؤشر رفيع. — Each word's letters type from its spoken start, spread over its duration, with a thin caret.
- **متى أستخدمها / when:** عروض تقنية وتعليمية — tech and tutorial pieces.
- **كيف / how:** Letters ~30–50 ms each within [start, end]; caret 2 px; omit full stops; box variant: mono lowercase typed 35 ms/char into a solid orange/yellow box with an underscore cursor. For Arabic type by grapheme clusters (Intl.Segmenter), never by code unit. **أرقام / params:** 30–50 ms/letter
- **الدليل / proof:** `style:pm-rossaxbt-3085b7` · `style:pm-gizakdag-b8c59e`

#### SYNC-40 · عداد كلمة مفتاحية ودائرة على الكلمة · Keyword counter & on-word annotations · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كل ظهور لكلمة مفتاحية يزيد عدادًا بنبضة، أو دائرة/خط يُرسم لحظة نطقها. — Each occurrence of a keyword bumps a counter with a pop, or a circle/underline draws at its spoken onset.
- **متى أستخدمها / when:** التأكيد على مصطلح متكرر — emphasising a recurring term.
- **كيف / how:** Counter chip top-right, pop 1 → 1.25 → 1 in 200 ms at word.start; annotation: interpolate start frame = word.start × fps, draw 12–20 frames, hold to phrase end. Stressed-word variant: 1–3 words at a time, stressed word lime #d4ff3a at 1.4×. **أرقام / params:** pop 200 ms; draw 12–20 frames
- **الدليل / proof:** `style:pm-sab8a-364a5a` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/text-highlights.md`

#### SYNC-41 · مكوّنات ترجمة HyperFrames · HyperFrames caption components · 📦 بأمر تثبيت / one install
- **ماذا / what:** 17 معالجة ترجمة جاهزة (كبسولة كاريوكي، صدمة كلمة، نيون، غليتش، تدرج، خامة، خلف الشخص…) تقبل مصفوفة كلمات. — 17 ready caption treatments (pill karaoke, kinetic slam, neon, glitch, gradient, texture, behind-subject…) that accept a word array.
- **متى أستخدمها / when:** ستايل ترجمة مميز بسرعة — a distinctive caption look fast.
- **كيف / how:** 15 of 17 keep an inline TRANSCRIPT/WORDS array [{text,start,end}] — replace it with your words.json (keep data-duration = audio length, 30 fps). blend-difference and camera-follow use internal timing. Latin display fonts (Anton, Montserrat, Poppins…) — swap to Arabic faces and test shaping before use. Table below.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/caption-pill-karaoke/caption-pill-karaoke.html:153` · `kosif-one/vendor/hyperframes/skills/hyperframes-registry/SKILL.md`
- **📦 تثبيت / install:** `npx hyperframes add caption-pill-karaoke`
- **⚖️ ترخيص / license:** HyperFrames Apache-2.0؛ تحمّل GSAP (رخصة GSAP القياسية، ليست MIT) وخطوط Google / HyperFrames Apache-2.0; loads GSAP (standard license, not MIT) and Google Fonts.

#### SYNC-42 · ترجمة مدمجة: شريط وكلمة ذروة خلف المتحدث · Embedded captions: rail + peak word behind the subject · 📦 بأمر تثبيت / one install
- **ماذا / what:** مقطع متحدث كما هو: شريط حرفي في الأمام، وكلمة ذروة نادرة خلف المتحدث عبر قناع. — An untouched talking clip: a verbatim rail in front and a scarce peak word composited behind the subject via a matte.
- **متى أستخدمها / when:** مقاطع بودكاست سينمائية — cinematic podcast clips.
- **كيف / how:** Decision gate → pick ONE of 35 identities (10 DNA + 25 themes; default 'anchor') → hyperframes init → prepare.sh (matte, transcribe, 50 ms audio envelope, safe zones) → theme.json or cinematic.json → preview-frames → render. ≤ 1 hero per thought block, ≥ 0.6 s air between heroes. Themes worth knowing: anchor (calm), stardust (poetic), chalkboard, dossier, neonsign, inkwater. Needs the HyperFrames toolchain + matte model. **أرقام / params:** 35 identities; hero gap ≥ 0.6 s
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/SKILL.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/make-theme.cjs`
- **📦 تثبيت / install:** `npx hyperframes init && bash scripts/prepare.sh <project>`
- **⚖️ ترخيص / license:** HyperFrames Apache-2.0؛ تحمّل GSAP (رخصة GSAP القياسية، ليست MIT) وخطوط Google / HyperFrames Apache-2.0; loads GSAP (standard license, not MIT) and Google Fonts.

#### SYNC-43 · الأشرطة السفلية · Lower thirds · 📦 بأمر تثبيت / one install
- **ماذا / what:** 13 شريطًا سفليًا جاهزًا للأسماء والألقاب (بطاقة داكنة، كتلة لون، خط جانبي، كبسولة، إطار نيون، شريط أخبار…). — 13 ready name/title lower thirds (dark card, colour block, side rule, pill, neon border, news ticker…).
- **متى أستخدمها / when:** مقابلات وبودكاست ونشرات — interviews, podcasts, news-style.
- **كيف / how:** npx hyperframes add lt-dark-card (or lt-clean-bar, lt-side-rule, lt-soft-pill, lt-neon-border, news-ticker…), 4.8 s each at 1920×1080. Arabic: mirror the layout (accent bar on the right, text right-aligned) and swap Oswald/Montserrat for Arabic faces. Speaker-coloured subtitles: tiny caps name in the character colour above the line. **أرقام / params:** 4.8 s
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/lt-dark-card/lt-dark-card.html` · `kosif-one/vendor/hyperframes/registry/blocks/news-ticker/news-ticker.html`
- **📦 تثبيت / install:** `npx hyperframes add lt-dark-card`
- **⚖️ ترخيص / license:** HyperFrames Apache-2.0؛ تحمّل GSAP (رخصة GSAP القياسية، ليست MIT) وخطوط Google / HyperFrames Apache-2.0; loads GSAP (standard license, not MIT) and Google Fonts.

#### SYNC-44 · ستايلات وحركات ترجمة بصمة · Basma caption presets, animations & highlight modes · 📦 بأمر تثبيت / one install
- **ماذا / what:** 12 حركة لكل كلمة، 5 طرق إبراز، و7+5 ستايلات عربية جاهزة بأحجام نسبية. — 12 per-word animations, 5 highlight modes and 7 + 5 ready Arabic presets with relative sizes.
- **متى أستخدمها / when:** داخل محرر بصمة — inside the Basma editor.
- **كيف / how:** Animations: pop, spring, stomp, mask, rise, karaoke, cascade, blur, wave, glitch, fade, slide. Highlights: box, color, underline, glow, none. Presets: ريلز (Noto Sans Arabic 7, chunk 6, #ffde59), سينما, قوي, تيك توك, كلمة واحدة, صندوق, هادئ; AutoEdit: cinema (Reem Kufi), trend (Lalezar, box), karaoke (Changa), neon (Rubik, glow), minimal (IBM Plex Sans Arabic). Sizes 5–14% of the short side; chunk 1–6; stroke 0–12. **أرقام / params:** size 5–14% short side; chunk 1–6
- **الدليل / proof:** `app/public/js/00_editor.js:347` · `app/public/js/00_editor.js:2352` · `app/public/js/50_autoedit.js:835`
- **📦 تثبيت / install:** `cd app && npm install`

**مكوّنات ترجمة HyperFrames / caption components** (📦 `npx hyperframes add <name>`):

| المكوّن | الشكل | أرقام |
|---|---|---|
| caption-pill-karaoke | كبسولة داكنة، الكلمة تتلون على زمنها | pill #1C1E1D, idle #A6A6A6 |
| caption-highlight | صندوق أحمر يكتسح خلف الكلمة | #ff1745, 0.08–0.16 s |
| caption-kinetic-slam | كلمة واحدة تملأ الشاشة باتجاهات متناوبة | back.out(1.7/2.2), 0.2 s |
| caption-clip-wipe | كل كلمة تُكشف بمسح clip-path | #FFD700 active, 0.3 s |
| caption-editorial-emphasis | جسم sans صغير + كلمة serif مائلة ضخمة | cream #f5f0d0 |
| caption-neon-glow / neon-accent | توهج نيون ووميض للكلمات المفتاحية | #FF0099 / #00FFF0, steps(1) 0.06 s |
| caption-glitch-rgb / matrix-decode | فصل ألوان RGB / فك شيفرة | jitter 0.045–0.12 s; #00ff41 |
| caption-gradient-fill / texture | تعبئة متدرجة أو خامة (lava, marble, metal…) | elastic bounce |
| caption-emoji-pop / particle-burst | إيموجي مدمج / انفجار جزيئات عند الكلمة | back.out(1.5) |
| caption-parallax-layers | ترجمة serif خلف الشخص (تحتاج قناعًا) | red #e50914 |
| caption-camera-follow | عالم أكبر من الإطار والكاميرا تتراجع بثبات | توقيت داخلي |
| caption-blend-difference | نص يقلب أبيض/أسود حسب البكسل | توقيت داخلي |
| caption-weight-shift | سطر يتحرك بين وزن خفيف وعريض | 300 → 700 |

تنبيه: كلها مصممة بخطوط لاتينية — بدّل إلى خط عربي واختبر التشكيل والاتجاه قبل الاستخدام.

## أفلام من الصوت — Films from sound

_صوت أو أغنية أو دعاء يدخل؛ فيلم كلمات أو موشن بالمعنى يخرج — والصوت كما هو._

#### SYNC-45 · فيلم كلمات من صوت (أغنية، شعر، دعاء) · Verse film from sound · ✅ مُثبت هنا / proven here
- **ماذا / what:** فيلم تايبوغرافي حركي من أغنية أو قصيدة أو دعاء: الكلمات على أزمنتها، كلمة مفتاحية لكل سطر، ذروة، وضوء يقوده الصوت. — A kinetic-typography film from a song, poem or dua: words on their sung times, one keyword per line, a payoff and light driven by the sound.
- **متى أستخدمها / when:** «اعمل فيديو لهذا الدعاء/القصيدة» — 'make a video of this dua/poem'.
- **كيف / how:** python verse.py AUDIO --name NAME [--text lyrics.txt | --words X.words.json] [--title --mood night|dawn|gold|sea|ink --accent '#E7B65A' --images a.jpg … --music none --fix … --render]; sections at pauses ≥ 3 s, interludes ≥ 4.5 s with a breathing eight-point rosette; line size 124/104/88/74 px for ≤ 14/24/36/more chars; payoff ×1.22 held +2.2 s; words rise 30·k px from blur 9 in 0.42 s; keyword pulse 1.07 yoyo 0.18 s. Ran here: verse tests ok (test_studio + test_directors). Needs faster-whisper unless --words is given. **أرقام / params:** moods night/dawn/gold/sea/ink; line ≤ 7 words
- **الدليل / proof:** `kosif-studio/motion/verse.py:246` · `kosif-studio/motion/verse.py:394` · `100-superskills/skills/kosif-montage-motion/templates/verse.html:62` · `kosif-studio/tests/test_studio.py:943`
- **📦 تثبيت / install:** `pip install faster-whisper  # models from huggingface.co (reachable): small 466 MB, large-v3 3.1 GB`

#### SYNC-46 · Voice2Motion: موشن بالمعنى من الصوت · Voice2Motion semantic scenes · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل جملة تُصنف (طقس، زحام، دعم، استرداد، عام) وتُرسم كمشهد متحرك خاص بها يتفاعل مع غلاف الصوت، والأرقام من نص الجملة. — Each sentence is classified (weather, traffic, support, refund, generic) and drawn as its own animated scene reacting to the voice envelope, numbers taken from the cue text.
- **متى أستخدمها / when:** رسالة صوتية تتحول إلى إنفوغراف — a voice note into an infographic reel.
- **كيف / how:** python audio2motion.py AUDIO --cues cues.json | --transcript t.txt [--out X.mp4 --fps 24 --size 540x960 --plan-only]; envelope 50 Hz from 8 kHz mono; 23 speech-energy bars; caption ease smoothstep 0.37 s; refuses empty transcripts and never claims ASR timing (estimated cues are labelled). Ran here: tests.test_audio2motion 8/8 ok. Owner's run: 29.4 s / 706 frames rendered in 10 s. **أرقام / params:** fps 12–60; ≤ 1920×1080; palette cyan (64,222,232), gold (255,196,79)
- **الدليل / proof:** `kosif-studio/motion/audio2motion.py:80` · `kosif-studio/motion/audio2motion.py:210` · `kosif-studio/tests/test_audio2motion.py`

#### SYNC-47 · إخراج تلقائي لمقطع متكلم · Editor-style auto direction of a talking clip · ✅ مُثبت هنا / proven here
- **ماذا / what:** من توقيت الكلمات وصناديق الوجه يختار المخطط سطر الذروة، والكلمات المفتاحية بالتركيز الطرفي، وموتيف رقم متكرر، وكلمات الفصول، ومواضع آمنة من الوجه. — From word timings and face boxes the planner picks the payoff line, end-focus keywords, a number-ring motif, chapter words and face-safe placements.
- **متى أستخدمها / when:** «مونتاج احترافي لهذا الكلام» قابل للتعديل — an editable directed edit.
- **كيف / how:** direct.plan(segs, shots, stress, W, H, dur) → {payoff, keys, motifs, captions, chapters}; never a filler, never the unit after a number; apply_fixes for dialect. kmotion direct CLIP --name … → edit.js → directed.html. Ran here: tests.test_directors ok. **أرقام / params:** punch expo.out 0.14 s; caption 54 px; keyword 200 px; chapter 380 px
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_directors.py:10` · `kosif-studio/motion/templates/directed.html`

#### SYNC-48 · الريل التلقائي من الكلام · Automatic talking-clip reel · 🟢 جاهز / ready
- **ماذا / what:** كلمات ← مسح ترجمة ← ترميم 1080×1920 ← صوت ← موسيقى عند الحاجة ← كاريوكي ← −14 LUFS ← بوابة. — words → decaption → restore 1080×1920 → voice → music only if none → karaoke → −14 LUFS → gate.
- **متى أستخدمها / when:** ريل من فيديو كلام بأمر واحد — a reel from a talking clip in one command.
- **كيف / how:** python scripts/kmotion.py reel CLIP.mp4 --out FINAL.mp4 [--transcript X.words.json --no-decaption --credit '@x' --model auto --style reels]. Without faster-whisper pass --transcript. See FOOT for the restoration chain.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/reel.py` · `kosif-studio/motion/reel.py:92`

#### SYNC-49 · إيقاع التلاوة والدعاء · Recitation & dua pacing · 📄 موصوف / documented only
- **ماذا / what:** آية أو سطر لكل شاشة، التغيير عند الوقف، انتقالات بطيئة، بلا ارتداد، ونتبع القارئ لا الإيقاع. — One verse/line per screen, change on waqf, slow crossfades, no bouncy effects; follow the reciter, not a beat grid.
- **متى أستخدمها / when:** قرآن، أدعية، أناشيد بلا موسيقى — Quran, duas, a cappella nasheeds.
- **كيف / how:** Crossfade 600–900 ms; words reveal through a rising mask (0.65 s, stagger 0.09) and leave upward (0.35 s, stagger 0.03); no music under Quran recitation unless the user asks; reference-matched loudness (e.g. −12.75 LUFS) when mimicking a reel; the user's exact text with tashkeel. **أرقام / params:** crossfade 600–900 ms
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:51` · `kosif-tool/playbooks/music.md:68` · `kosif-one/projects/thursday-dua-animation/source/index.html:198-209`

#### SYNC-50 · توقيت سطر الأغنية · Lyric line timing · 📄 موصوف / documented only
- **ماذا / what:** السطر يسبق الغناء، يبقى أثناءه، ويخرج بسرعة. — Lines lead the singing, hold while sung and exit quickly.
- **متى أستخدمها / when:** فيديوهات كلمات الأغاني — lyric videos.
- **كيف / how:** Enter 80–120 ms early (recipe: −100 ms with a 350 ms mask wipe); exit ≤ 200 ms (150 ms after the last word); words enter ≤ 40 ms from onset with 180 ms cubic-bezier(0.2,0.9,0.2,1) scale 0.92 → 1. Plan on a grid of tempo, bars, sections and every sung word; characters on one side, words on the other. **أرقام / params:** enter −80…−120 ms; exit ≤ 200 ms
- **الدليل / proof:** `kosif-tool/playbooks/music.md:28` · `kosif-tool/playbooks/music.md:43` · `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md`

#### SYNC-51 · ريل كلمات أغنية · Songreel lyric reel · 📦 بأمر تثبيت / one install
- **ماذا / what:** تحليل بنية الأغنية، أسئلة بحث وتلوين لكل قسم، مجمع لقطات، قص، وبناء بالكلمات. — Song structure analysis, per-section queries and grades, a clip pool, cutting and building with lyrics.
- **متى أستخدمها / when:** أغنية + لقطات مزاجية — a song plus mood footage.
- **كيف / how:** songreel analyze SONG --name --lyrics; cut N --media; build N --model large-v3 --draft|--render (≈ 45 s typical; clips < 360p rejected). Needs faster-whisper and footage (yt-dlp for pools). **أرقام / params:** ~45 s; reject < 360p
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/songreel.py` · `100-superskills/skills/kosif-montage-motion/tests/test_songreel.py`
- **📦 تثبيت / install:** `pip install faster-whisper  # models from huggingface.co (reachable): small 466 MB, large-v3 3.1 GB`

#### SYNC-52 · لكل جملة منطوقة دليل بصري · One visual proof per spoken claim · 📄 موصوف / documented only
- **ماذا / what:** في الأفلام التي يقودها الصوت، كل سطر منطوق يقابله صورة واحدة تثبته، والفعل يحدث على الكلمة التي تسميه. — In voice-led films each spoken line gets exactly one picture that proves it, and actions happen on the word that names them.
- **متى أستخدمها / when:** شرح منتج أو فيلم توضيحي بتعليق — narrated product or explainer films.
- **كيف / how:** Beat table: spoken line | visual proof | entry/exit | on-screen text. Cross-family sync rules: counters finish on the word that says the number (start 700–1000 ms earlier, ±100 ms); diagram nodes pop on their names, camera moves only in pauses > 400 ms; phone taps at emphasis start − 40 ms; photo cuts 2 frames (≈ 67 ms) before the emphasis word; gestures land 2–4 frames before the stressed word; particle bursts within one frame of transients. **أرقام / params:** ±100 ms; cut −2 frames; gesture −2…−4 frames
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/216-narrated-product-film/SKILL.md` · `kosif-tool/playbooks/charts.md:201-208` · `kosif-tool/playbooks/phone.md:198-205` · `kosif-tool/playbooks/photos.md:205-211`

## الصمت والقص والتزامن الصوتي — Silence, cuts & audio sync utilities

_أدوات صغيرة تمنع كوارث كبيرة: صمت مُقاس، دمج بلا انزياح، ومؤثر تقع ذروته على الحدث._

#### SYNC-53 · كشف الصمت الثابت والتكيفي · Fixed & adaptive silence detection · ✅ مُثبت هنا / proven here
- **ماذا / what:** اعثر على الهواء الميت بعتبة ثابتة أو بعتبة البوابة المقاسة لكل تسجيل. — Find dead air with a fixed threshold or with each recording's own measured gating threshold.
- **متى أستخدمها / when:** قص الصمت أو تحديد نقاط القطع — jump cuts or cut points.
- **كيف / how:** Fixed: -af silencedetect=n=-35dB:d=0.5..0.7 -f null - (ran here: a 1 s gap reported 1.000–2.000 s). Adaptive: loudnorm print_format=json → input_thresh → silencedetect=noise=${thresh}dB:d=0.5; merge gaps < 0.2 s. EDL writer: silence_cut.py in --db -35 --min 0.6 --pad 0.12 --out edl.json; Python analyser: −50 dBFS, ≥ 0.5 s over 50 ms RMS. **أرقام / params:** −35 dB; d 0.5–0.7 s; pad 0.08–0.12 s
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/silence-detection.md` · `100-superskills/skills/pro-video-editor-ffmpeg/scripts/silence_cut.py:19` · `100-superskills/skills/kosif-montage-motion/scripts/omni/audio_analyze.py:147`

#### SYNC-54 · إصلاح انزياح الصوت المدموج · Joined-audio drift fix · 📄 موصوف / documented only
- **ماذا / what:** الدمج بالنسخ يبقي حشو كل قطعة فيتراكم الانزياح (~50 ms لكل وصلة)؛ فك وأعد الترميز مرة واحدة. — Copy-mode concat keeps each piece's encoder padding, so drift accumulates (~50 ms per join); decode and encode once.
- **متى أستخدمها / when:** تعليق صوتي مولد جملة جملة ثم مدموج — TTS generated per sentence then joined.
- **كيف / how:** ffmpeg -f concat -safe 0 -i list.txt -c:a libmp3lame -b:a 64k -ar 24000 -ac 1 -write_xing 0 joined.mp3; verify joined duration vs the sum of parts (measured 2.51 s → 0.06 s over 181 pieces). Better: concatenate WAV/PCM and encode once at delivery. **أرقام / params:** ~50 ms/join; MP3 frame 1152/576 samples
- **الدليل / proof:** `kosif-atlas/skills/3323-joined-audio-transcript-drift/13837-joined-audio-transcript-drift/SKILL.md`

#### SYNC-55 · ذروة المؤثر على الحدث · SFX peak-offset alignment · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** خزّن زمن الذروة داخل كل ملف مؤثر وابدأ الصوت عند زمن الحدث ناقص الذروة؛ والصاعدات تنتهي على الحدث. — Store each SFX file's internal peak time and start it at event − peak; risers align to their end.
- **متى أستخدمها / when:** كل نقرة وضربة وwhoosh — every click, hit and whoosh.
- **كيف / how:** PEAK table per file (measure with astats or numpy argmax of |x|); start = eventTime − peak; risers end on the event; whoosh ≤ −18 dBFS on a separate stem. **أرقام / params:** PEAK per file
- **الدليل / proof:** `style:product` · `kosif-tool/playbooks/photos.md:205-211`

#### SYNC-56 · دمج المشاهد مع الصوت الأصلي بلا تعديل · Concat + untouched original audio mux · 🟢 جاهز / ready
- **ماذا / what:** يجمع المشاهد المرندرة بالترتيب ويضع أغنية المستخدم تحتها كما هي، مع بصمة sha256 للمصدر. — Joins rendered segments in order and lays the user's original song underneath untouched, recording the source sha256.
- **متى أستخدمها / when:** فيلم مشاهد على أغنية المستخدم — scene films over the user's song.
- **كيف / how:** ffmpeg -f concat -safe 0 -i concat.txt -i song.mp3 -map 0:v:0 -map 1:a:0 -t DUR -c:v copy -c:a aac -b:a 192k … ; only gentle edge fades (in 0.3 s, out 1.3 s) if asked; record sha256 of the source audio. Optional mux in fastify render.py: --audio path → -shortest (no loudness change). **أرقام / params:** fade in 0.3 s / out 1.3 s
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:152-158` · `fastify-motion-bro/scripts/render.py:15`

#### SYNC-57 · غلاف الجهارة وقنوات الصوت للحركة · Loudness envelope & sound channels for motion · 🟢 جاهز / ready
- **ماذا / what:** غلاف RMS كل 50 ms وقنوات لكل إطار (bass/mid/high، ضربات، بدايات، صمت) تقود أي قيمة بصرية. — A 50 ms RMS envelope and per-frame channels (bass/mid/high, kicks, onsets, silence) drive any visual value.
- **متى أستخدمها / when:** ترجمة أو هالة تتنفس مع الصوت — captions or halos breathing with the voice.
- **كيف / how:** python motion.py channels TRACK.wav [--fps 30] → ch.json; in the page MOTION.channels(json): ch.v('bass',t), ch.kick(t), ch.onset(t), ch.silent(t). Verse halo R = 0.62·min(W,H)·(1 + 0.05·rms + 0.06·kick + 0.25·flare). Caption scale from RMS stays within 3–6% (proof: +4.5%). Browser mic meter: AnalyserNode fftSize 256, RMS × 4 clamped to 1. **أرقام / params:** hop sr/fps; nfft 4096 Hann; caption ±3–6%
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:97` · `kosif-one/tools/kosif-studio/motion/templates/verse.html:86` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/audio-reactive-spectrum/README.md` · `kosif-audit-studio/voice.js:166`

#### SYNC-58 · مزامنة الفم بستة أشكال · Six-shape lip sync · 📄 موصوف / documented only
- **ماذا / what:** الفم يختار بين مغلق وA وO وE وM وF من طاقة الصوت أو نص السكريبت. — The mouth picks among closed, A, O, E, M, F from audio energy or the script.
- **متى أستخدمها / when:** شخصيات تتكلم — talking characters (see CHAR).
- **كيف / how:** Map RMS (and phonemes when available from Piper/aligner) to a viseme per frame; hold each shape ≥ 2 frames to avoid flicker; replacement tiles synced to syllables for lyric characters. **أرقام / params:** 6 visemes; hold ≥ 2 frames
- **الدليل / proof:** `100-superskills/skills/character-animation-2d/SKILL.md` · `kosif-tool/styles/pm-davidshulmanfl-371638/BRIEF.md`

## توليفات قوية / power combos

- **فيلم دعاء ليلي / night dua film:** SYNC-10 + SYNC-45 + SYNC-49 + SYNC-32 + GLOW (أشعة فجر) + PART (غبار) + VOICE (بلا موسيقى) — النص الصحيح بتشكيله على صوت القارئ، آية لكل شاشة.
- **ريل كلام بكاريوكي / talking reel:** SYNC-07 + SYNC-11 + SYNC-27 + SYNC-26 + FOOT (ريل تلقائي) + BEAT (خفض الموسيقى) + QA (SYNC-05) — ترجمة reels بنبضة 120 ms ولا كلمة مبكرة.
- **فيلم كلمات بصوت مولّد / generated-voice word film:** VOICE (Piper) + SYNC-09 + SYNC-32 + CAM (كاميرا تتبع الجملة) + COLOR (ليل إلى فجر) — كما في proofs/arabic-voice-kinetic.
- **طيف صوتي بكاريوكي / audio-reactive karaoke:** SYNC-57 + SYNC-33 + BEAT (16 نطاقًا لكل إطار) + SHAPE (72 عمودًا) — كما في proofs/audio-reactive-spectrum.
- **رسالة صوتية إلى إنفوغراف / voice note to infographic:** SYNC-46 + SYNC-17 + DATA (أرقام من النص) + FORMAT (9:16) — مشاهد بالمعنى وتوقيت موسوم بأنه تقدير عند غياب التفريغ.
- **بودكاست سينمائي / cinematic podcast clip:** SYNC-42 + SYNC-43 + SYNC-47 + FOOT (SYNC-47 + عزل المتحدث) — شريط حرفي وكلمة ذروة خلف المتحدث.
- **شرح مسرود ببيانات / narrated data explainer:** SYNC-52 + SYNC-34 + DATA (عداد ينتهي على الرقم المنطوق) + DIAG (عقدة تظهر عند اسمها) — كل جملة بدليل واحد.
- **فيديو كلمات أغنية / lyric video:** SYNC-50 + SYNC-12 + SYNC-51 + BEAT (شبكة الإيقاع) + TRANS (قطعات على البار) — السطر يسبق الغناء 100 ms ويخرج بسرعة.

## أخطاء ممنوعة / never do

1. **لا تمط الصوت ولا تعد أخذ عيناته ولا تغيّر توقيته** — الصورة تتبع الصوت؛ تعديل الجهارة على نسخة تسليم فقط (SYNC-01).
2. **لا نماذج Whisper .en للعربية، ولا تعتمد على الافتراضي small.en في HyperFrames** — يترجم بدل أن يفرّغ (SYNC-08).
3. **لا تستخدم صوتًا محذوف الصمت أو مسرّعًا لتوقيت الكلمات** — كل الأزمنة تنكسر (SYNC-13).
4. **لا تدّعِ توقيتًا لم تقسه** — التقدير يُوسم تقديرًا، والتزامن يُقاس بـ SYNC-05 (Whisper وحده خطؤه ~±150 ms).
5. **لا تغيّر كلام المتحدث ولا نص القرآن** — حرفيًا، ونص المستخدم بتشكيله (SYNC-25, SYNC-10).
6. **لا تحرق الترجمة إن لم تُطلب** — سلّم SRT/VTT؛ الحرق قد يفسد ترجمة العميل (SYNC-25).
7. **لا drawtext لنص عربي ولا Encoding ثابت مع تلوين الكلمة** — مربعات فارغة أو ترتيب معكوس؛ ASS بحدث لكل كلمة وEncoding −1 (SYNC-27).
8. **لا تقسم الكلمة العربية إلى حروف في الكاريوكي** — قناع يغطي الكلمة كلها (SYNC-33).
9. **لا تمرر words.json بصيغة {word} إلى captions_pages.py** — جرّبتها: KeyError 'text'؛ حوّل المفتاح أولًا (SYNC-29).
10. **لا موسيقى تحت تلاوة القرآن ما لم يطلب المستخدم، ولا حركات مرتدة على التلاوة** (SYNC-49).
11. **لا تدمج مقاطع MP3 بالنسخ ثم تجمع مددها** — انزياح ~50 ms لكل وصلة (SYNC-54).

## أقوى 5 حركات توقيع / 5 signature moves

1. **SYNC-32 — الكلمة على موعد نطقها:** قناع 0.42 ث من اليمين، صعود نابض 34 بكسل، وأقصى فرق مقاس 33 ms.
2. **SYNC-27 + SYNC-28 — كاريوكي ASS عربي:** حدث لكل كلمة، نبضة 112%→100% في 120 ms، وسبعة ستايلات باسم واحد.
3. **SYNC-10 + SYNC-45 — فيلم دعاء أو قصيدة من الصوت:** النص الصحيح على أزمنة التفريغ، سطر ≤ 7 كلمات، وضوء يتنفس مع الصوت.
4. **SYNC-46 — رسالة صوتية تصير موشن بالمعنى:** طقس وزحام ودعم واسترداد، كل جملة مشهد.
5. **SYNC-05 — قِس قبل أن تسلّم:** «SYNC OK» أو لا تسليم.
