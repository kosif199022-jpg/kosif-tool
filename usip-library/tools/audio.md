# أدوات المجال `audio` (6 أداة)

> مولّد من `data/tools.json`. [الفهرس الرئيسي](../README.md) · `python3 scripts/hub.py tool <id>` للبطاقة الحية.

### `audio-cue-mapper` — مستخرج إشارات التوقيت من الصوت / WAV audio cue mapper

| الحقل | القيمة |
|---|---|
| المسار | `scripts/audio_cue_mapper.py` (جذر: skill) |
| المجال | `audio` |
| الدليل | `tested-here` |
| العائلات | `audio-sync-captions`, `music-beat-sound` |

**ما تفعله:** يقيس ملف WAV بترميز PCM بعمق 16 بت (حتى 120 ثانية) ويُخرج ملف JSON جديدًا بصيغة kosif.audio-cues.v1 يضم غلاف طاقة RMS كل 50 ملي ثانية وبدايات صوتية مرشّحة عند ارتفاع الطاقة، ويستورد اختياريًا توقيتات كلمات جاهزة من WhisperX أو KOSIF بعد التحقق منها، دون أن يختلق سرعة إيقاع أو نبضات أو كلمات أو مشاعر.

**What it does:** Measures a 16-bit PCM WAV (up to 120 s) into a new kosif.audio-cues.v1 JSON with a 50 ms RMS energy envelope and rising-energy onset candidates, optionally importing validated WhisperX/KOSIF word timings, without ever inventing BPM, beats, words or emotion.

#### متى تُستدعى

- «حلّل الصوت ده وطلّع لي لحظات ارتفاع الطاقة عشان أركّب عليها القطعات»
- «استورد توقيت الكلمات من WhisperX وتأكد إنه سليم ومرتب»
- «أبي نقاط البداية في التعليق الصوتي عشان أزامن الأنيميشن عليها»
- «Measure onsets and energy in my voiceover WAV for motion sync»
- «Import my WhisperX word timings into a KOSIF cues file»

#### الأوامر

- **measure**: Reads the WAV in 50 ms windows and writes the RMS envelope and onset candidates (at least 0.12 s apart, at most 600) to a new JSON file. It then prints a one-line JSON summary.
  - `python3 scripts/audio_cue_mapper.py ./voice.wav --out ./out/cues.json`
- **measure-with-words**: Does the same and also imports words[] or segments[].words[] timings. It rejects missing or non-numeric times, overlap, reversal and words that run past the audio.
  - `python3 scripts/audio_cue_mapper.py ./voice.wav --aligned-words ./words.json --out ./out/cues.json`
- **help**: Shows the arguments: audio, --aligned-words and the required --out.
  - `python3 scripts/audio_cue_mapper.py --help`

#### المتطلبات والأمان

- binaries: python3
- الأمان: writes-files
- الموافقة: —
- الحدود: Detects amplitude jumps only: it does not estimate tempo or beats, does not transcribe, and does not read MP3/AAC or 8/24/32-bit WAV, which must first be converted to 16-bit PCM WAV elsewhere.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_creative_intelligence.py`
- مرجع: `.claude/skills/kosif-superpowers/references/creative-intelligence-execution.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/audio.md`
- مرجع: `.claude/skills/kosif-superpowers/references/music-rhythm-execution.md`
- مرجع: `.claude/skills/kosif-superpowers/references/reference-edit-execution.md`
- مرجع: `.claude/skills/kosif-superpowers/references/reference-visual-transfer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/capability-operating-manual.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:audio-cue-mapper --evidence <ملف>`.

### `caption-lines` — سطور الترجمة: من توقيت الكلمات إلى ترجمة مقروءة / Caption lines: word timings to readable SRT/VTT

| الحقل | القيمة |
|---|---|
| المسار | `scripts/caption_lines.py` (جذر: skill) |
| المجال | `audio` |
| الدليل | `tested-here` |
| العائلات | `audio-sync-captions`, `app-feature-transfer`, `typography-arabic` |

**ما تفعله:** كُتبت بعد دراسة «مونتاجي»: تقسم توقيت الكلمات إلى سطور ترجمة قصيرة بحد للكلمات والحروف والمدة، وتكسر عند الوقفة ونهاية الجملة والفاصلة، وتسد الفجوات القصيرة، وتضيف علامة الاتجاه للعربي، وتحذف ما يخترعه نموذج التفريغ مثل «ترجمة نانسي» و«اشتركوا في القناة» مع سرده؛ وlint يفحص أي ملف ترجمة.

**What it does:** Written after a read-only study of the Montaji Arabic video editor: groups word timings (atlas words.json, whisper.cpp -oj or faster-whisper JSON) into short caption lines by word count, characters, time on screen, pauses, sentence ends (including ؟ and ؛) and commas; closes short holes, extends short lines only into silence, can add a right-to-left mark for Arabic, and drops and lists phrases speech models invent (subtitle credits, subscribe outros, sound tags, punctuation-only and looping lines). lint checks any SRT/VTT/JSON for overlaps, durations, reading speed and the same phrases.

#### متى تُستدعى

- «قسّم التفريغ ده لسطور ترجمة قصيرة SRT»
- «Turn these Whisper word timestamps into readable captions»
- «نظّف الترجمة من الهلوسة زي ترجمة نانسي واشتركوا في القناة»
- «Lint this SRT for overlaps and reading speed»

#### الأوامر

- **group**: Words to SRT, VTT or JSON lines; reports the suspect lines it dropped.
  - `python3 scripts/caption_lines.py group words.json -o captions.srt --rlm`
- **lint**: Overlaps, too-short lines, reading speed above 17 chars/s and suspect phrases; exits 1 on any issue.
  - `python3 scripts/caption_lines.py lint captions.srt`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Reads and writes local files only; captions of someone else's speech follow the media's rights.
- الحدود: Does not transcribe: pair it with whisper.cpp or faster-whisper. The suspect-phrase list is short and generic, so a real spoken 'subscribe' is dropped too (use --keep-suspect). Line breaking counts characters, not rendered width.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_caption_lines.py`
- مرجع: `.claude/skills/kosif-superpowers/references/app-studies/montaji.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:caption-lines --evidence <ملف>`.

### `music-rhythm-engine` — فرضيات إيقاع الموسيقى / Music rhythm hypotheses

| الحقل | القيمة |
|---|---|
| المسار | `scripts/music_rhythm_engine.py` (جذر: skill) |
| المجال | `audio` |
| الدليل | `tested-here` |
| العائلات | `music-beat-sound`, `easing-timing-rhythm` |

**ما تفعله:** يحوّل ملف kosif.audio-cues.v1 إلى ملف JSON جديد يضم حتى ثلاث فرضيات متمايزة لسرعة الإيقاع (يقيّم السرعات من 60 إلى 200 نبضة في الدقيقة مقابل البدايات المقيسة)، وشبكة نبضات تقديرية عندما يبلغ أفضل تطابق 0.60 أو أكثر، وأقسام طاقة لكل ثانية مقارنةً بوسيط المقطع، مع وسم كل النتائج بأنها غير مؤكدة.

**What it does:** Turns a kosif.audio-cues.v1 file into a new JSON of up to three distinct tempo hypotheses (60–200 BPM scored against measured onsets), an estimated beat grid when the best match is at least 0.60, and per-second energy sections relative to the track median, all flagged as unverified.

#### متى تُستدعى

- «طلّع لي البي بي إم التقريبي للمزيكا دي»
- «أبي شبكة نبضات عشان أقصّ الفيديو على الإيقاع»
- «اقترح سرعة الإيقاع للموسيقى من ملف cues.json»
- «Estimate the tempo and a beat grid from my measured audio cues»
- «Which seconds of the track are high energy so I can place the big cuts?»

#### الأوامر

- **estimate**: Scores every integer BPM from 60 to 200 against the onsets (±55 ms tolerance), keeps the top three hypotheses at least 6 BPM apart and builds a grid (at most 500 ticks) when the match is 0.60 or higher. It labels per-second RMS sections, writes a new JSON file and prints a summary.
  - `python3 scripts/music_rhythm_engine.py ./out/cues.json --out ./out/rhythm.json`
- **help**: Shows the arguments: the cues file and the required --out.
  - `python3 scripts/music_rhythm_engine.py --help`

#### المتطلبات والأمان

- binaries: python3
- الأمان: writes-files
- الموافقة: —
- الحدود: Gives a heuristic tempo guess from onset alignment only: half- and double-time errors are common, fewer than 4 onsets gives no tempo, and it detects no chords, mood or lyrics.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_music_rhythm_engine.py`
- مرجع: `.claude/skills/kosif-superpowers/references/music-rhythm-execution.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/audio.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:music-rhythm-engine --evidence <ملف>`.

### `repo-transcribe-audio` — تفريغ الصوت بـ Gemini مع رسائل خطأ واضحة / Gemini audio transcription with readable errors

| الحقل | القيمة |
|---|---|
| المسار | `tools/transcribe_audio.py` (جذر: repo) |
| المجال | `audio` |
| الدليل | `tested-here` |
| العائلات | `voice-tts`, `audio-sync-captions` |

**ما تفعله:** يفرّغ ملفًا صوتيًا عبر Gemini generateContent (داخل الطلب حتى نحو 14 ميجابايت، وعبر Files API لما هو أكبر). عند الفشل يطبع رسالة جوجل نفسها مع تلميح للحل (مفتاح غير صالح، لا صلاحية، نموذج غير موجود، حصة، حجم)، ويعيد المحاولة مع 429 و5xx، ويجرّب النموذج التالي، ومع --engine auto يرجع إلى faster-whisper محليًا. ويختبر --check المفتاح دون صوت.

**What it does:** Transcribes an audio file with Gemini generateContent (inline under ~14 MB, Files API above). On failure it prints Google's own error message with a fix hint (invalid key, no access, missing model, quota, size), retries 429/5xx, tries the next model, and with --engine auto falls back to local faster-whisper. --check tests the key without audio.

#### متى تُستدعى

- «Transcribe this test voice clip to verify the content»
- «My Gemini transcription failed with HTTP error, why?»
- «فرّغ ملف الصوت ده واتأكد إن الكلام صح»
- «اختبر مفتاح Gemini قبل التفريغ»

#### الأوامر

- **transcribe**: Sends the audio to Gemini (models tried in order), prints the text and writes {engine, model, text}; exit 0 ok, 1 every engine failed, 2 bad input.
  - `python3 tools/transcribe_audio.py ./voice.wav --json ./out/transcript.json`
- **whisper only**: Transcribes locally with faster-whisper (small, int8, CPU); no key or network.
  - `python3 tools/transcribe_audio.py ./voice.wav --engine whisper --language ar`
- **check**: Reads the model record with the key and prints ok or Google's error with a hint; sends no audio.
  - `python3 tools/transcribe_audio.py --check`

#### المتطلبات والأمان

- binaries: python3
- network: true
- optional: faster-whisper
- الأمان: network
- الموافقة: Uploads the audio file to Google's Gemini API using the GEMINI_API_KEY in the environment (paid usage may apply); use --engine whisper to keep the audio local.
- الحدود: Needs a valid GEMINI_API_KEY for the Gemini path; the whisper fallback needs faster-whisper installed and gives text only (no dialect or speaker notes). It does not return word timestamps.

#### الاختبارات والأدلة

- `tests/test_transcribe_audio.py`
- مرجع: `CLAUDE.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:repo-transcribe-audio --evidence <ملف>`.

### `repo-words-convert` — محوّل الترجمات إلى توقيت الكلمات / Subtitle to words.json converter

| الحقل | القيمة |
|---|---|
| المسار | `tools/words_convert.py` (جذر: repo) |
| المجال | `audio` |
| الدليل | `tested-here` |
| العائلات | `audio-sync-captions` |

**ما تفعله:** يحوّل ملفات الترجمة SRT وVTT ومخرجات JSON بأسلوب Whisper وملفات CSV/TSV ذات الأعمدة word,start,end إلى ملف توقيت الكلمات words.json الخاص بالأطلس (قائمة [{word,start,end}] بالثواني)، مع إزاحة زمنية عامة وحدّ أدنى للفجوة بين الكلمات عند الطلب. وإذا انتهى اسم الوجهة بـ ‎.js كتب ملف words.js ‏(window.KOSIF_WORDS) بدلًا من ذلك.

**What it does:** Converts SRT/VTT subtitles, Whisper-style JSON or word,start,end CSV/TSV into the atlas words.json timing list ([{word,start,end}] in seconds), with an optional global offset and minimum gap between words. When the destination ends in .js it writes a words.js file (window.KOSIF_WORDS) instead.

#### متى تُستدعى

- «حوّل ملف الترجمة srt إلى words.json»
- «عندي تفريغ Whisper وأبغى توقيت الكلمات للستارتر»
- «قدّم توقيت كل الكلمات 80 ملّي ثانية»
- «convert captions.vtt into words.json for word-synced kinetic text»
- «turn whisper output into a words.js file for the html-canvas starter»
- «shift all word timings earlier by 0.08 s»

#### الأوامر

- **srt**: Splits each subtitle cue into words and spreads the cue's time span across them, weighted by word length; inline <...> and {...} tags are stripped.
  - `python3 tools/words_convert.py ./captions.srt ./words.json`
- **whisper-json**: Reads segments[].words, {words:[...]} or a flat list (segments without words are spread from their text) and moves every timestamp by the offset (negative means earlier, clamped at 0).
  - `python3 tools/words_convert.py ./whisper.json ./words.json --offset -0.08`
- **vtt**: Parses WebVTT (WEBVTT header, NOTE, STYLE and REGION blocks and cue settings are skipped) and enforces a minimum gap between consecutive words.
  - `python3 tools/words_convert.py ./cues.vtt ./words.json --min-gap 0.02 --format vtt`
- **csv**: Reads word,start,end rows (header optional; times in seconds or [hh:]mm:ss.mmm). Use a .tsv file or --format tsv for tab-separated input.
  - `python3 tools/words_convert.py ./words.csv ./words.json`
- **js**: Writes 'window.KOSIF_WORDS = [...]' for pages opened from file://, such as the html-canvas starter.
  - `python3 tools/words_convert.py templates/words.example.json ./words.js`
- **help**: Shows the formats, options and examples.
  - `python3 tools/words_convert.py --help`

#### المتطلبات والأمان

- binaries: python3
- الأمان: writes-files
- الموافقة: Overwrites the destination file without asking; confirm before pointing it at an existing words.json or words.js (the docstring example targets the tracked starters/html-canvas/words.js).
- الحدود: For SRT/VTT, word times are estimated by spreading each cue's span by word length, not by real forced alignment, and only word/start/end are kept (emphasis or scene fields are dropped).

#### الاختبارات والأدلة

- `tests/test_tools_extra.py`
- مرجع: `playbooks/audio-sync.md`
- مرجع: `starters/html-canvas/README.md`
- مرجع: `playbooks/kinetic-type.md`
- مرجع: `README.md`
- مرجع: `.claude/skills/kosif-superpowers/references/capabilities.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:repo-words-convert --evidence <ملف>`.

### `tts-script` — تجهيز نص التعليق الصوتي: تقطيع آمن وتقدير المدة وSSML / TTS script prep: prosody-safe chunks, duration estimate and SSML

| الحقل | القيمة |
|---|---|
| المسار | `scripts/tts_script.py` (جذر: skill) |
| المجال | `audio` |
| الدليل | `tested-here` |
| العائلات | `voice-tts` |

**ما تفعله:** يجهز نص التعليق العربي أو المختلط لأي محرك تحويل نص إلى كلام: يقطعه عند نهايات الجمل ثم الفواصل ثم بين الكلمات دون كسر كلمة، ويقدر مدة كل قطعة بعدد الكلمات في الدقيقة مع الوقفات، ويكتب SSML بوقفات عند علامات الترقيم ووسوم لغة حول الكلمات الإنجليزية.

**What it does:** Prepares an Arabic or mixed-language narration script for any TTS engine: splits it into request-sized chunks at sentence ends, then clause marks, then between words (never mid-word, never across paragraphs); estimates speech time per chunk from words per minute plus sentence, clause and paragraph pauses with Arabic word counting; and writes SSML 1.0 with paragraphs, sentences, breaks at punctuation and lang tags around Latin runs (or Arabic runs in a Latin script).

#### متى تُستدعى

- «قسم نص التعليق الصوتي لقطع مناسبة لـ ElevenLabs»
- «التعليق ده هياخد كام ثانية؟»
- «اعمل SSML للنص العربي بوقفات عند الفواصل»
- «Split my narration script into TTS-safe chunks»
- «Estimate how long this voice-over will run»
- «Generate SSML with breaks and language tags for a mixed Arabic/English script»

#### الأوامر

- **chunk**: Chunks at most N characters with their end type (sentence, clause, word, paragraph).
  - `printf 'مرحبا بكم في KOSIF Studio. هذا اختبار، قصير جدا!\n\nفقرة ثانية؟ نعم.\n' \| python3 scripts/tts_script.py chunk - --max-chars 30`
- **estimate**: Seconds per chunk (speech + pauses), start times and total mm:ss.
  - `printf 'مرحبا بكم في KOSIF Studio. هذا اختبار، قصير جدا!\n\nفقرة ثانية؟ نعم.\n' \| python3 scripts/tts_script.py estimate - --wpm 140`
- **ssml**: SSML 1.0 document with <p>, <s>, <break> and <lang> around Latin runs.
  - `printf 'مرحبا بكم في KOSIF Studio. هذا اختبار، قصير جدا!\n' \| python3 scripts/tts_script.py ssml - --lang ar-EG --xml`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: —
- الحدود: Timing is a words-per-minute estimate (numbers and abbreviations count as one word; real length depends on the voice); SSML support for <lang> and break times varies by engine.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_tts_script.py`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:tts-script --evidence <ملف>`.

