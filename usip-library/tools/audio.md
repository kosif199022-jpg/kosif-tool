# أدوات المجال `audio` (3 أداة)

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

