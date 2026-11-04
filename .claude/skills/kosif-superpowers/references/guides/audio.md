# الصوت والإيقاع وتوقيت الكلمات — Audio, rhythm and word timing

تحليل الصوت الحقيقي إلى مرشحات طاقة وكلمات موقّتة وفرضيات BPM، ثم ربطها بقرارات الحركة.

Turning real audio into energy cues, timed words and tempo hypotheses, then into motion decisions.

Commands below are typed from the skill folder (`.claude/skills/kosif-superpowers/`) unless they say otherwise; `$SKILL_DIR` means that folder.

<!-- hub:area:audio:start -->

**الأدوات / tools (7)** — `python3 scripts/hub.py tool <id>` for every command, requirement and limit:

| tool | what it does | start with | evidence |
|---|---|---|---|
| `audio-cue-mapper` | Measures a 16-bit PCM WAV (up to 120 s) into a new kosif.audio-cues.v1 JSON with a 50 ms RMS energy envelope and rising-energy onset candidates, optionally importing validated WhisperX/KOSIF word timings, without ever inventing BPM, beats, words or emotion. | `python3 scripts/audio_cue_mapper.py ./voice.wav --out ./out/cues.json` | tested-here |
| `music-rhythm-engine` | Turns a kosif.audio-cues.v1 file into a new JSON of up to three distinct tempo hypotheses (60–200 BPM scored against measured onsets), an estimated beat grid when the best match is at least 0.60, and per-second energy sections relative to the track median, all flagged as unverified. | `python3 scripts/music_rhythm_engine.py ./out/cues.json --out ./out/rhythm.json` | tested-here |
| `repo-words-convert` (repo root) | Converts SRT/VTT subtitles, Whisper-style JSON or word,start,end CSV/TSV into the atlas words.json timing list ([{word,start,end}] in seconds), with an optional global offset and minimum gap between words. When the destination ends in .js it writes a words.js file (window.KOSIF_WORDS) instead. | `python3 tools/words_convert.py ./captions.srt ./words.json` | tested-here |
| `repo-transcribe-audio` (repo root) | Transcribes an audio file with Gemini generateContent (inline under ~14 MB, Files API above). On failure it prints Google's own error message with a fix hint (invalid key, no access, missing model, quota, size), retries 429/5xx, tries the next model, and with --engine auto falls back to local faster-whisper. --check tests the key without audio. | `python3 tools/transcribe_audio.py ./voice.wav --json ./out/transcript.json` | tested-here |
| `tts-script` | Prepares an Arabic or mixed-language narration script for any TTS engine: splits it into request-sized chunks at sentence ends, then clause marks, then between words (never mid-word, never across paragraphs); estimates speech time per chunk from words per minute plus sentence, clause and paragraph pauses with Arabic word counting; and writes SSML 1.0 with paragraphs, sentences, breaks at punctuation and lang tags around Latin runs (or Arabic runs in a Latin script). | `printf 'مرحبا بكم في KOSIF Studio. هذا اختبار، قصير جدا!\n\nفقرة ثانية؟ نعم.\n' \| python3 scripts/tts_script.py chunk - --max-chars 30` | tested-here |
| `caption-lines` | Written after a read-only study of the Montaji Arabic video editor: groups word timings (atlas words.json, whisper.cpp -oj or faster-whisper JSON) into short caption lines by word count, characters, time on screen, pauses, sentence ends (including ؟ and ؛) and commas; closes short holes, extends short lines only into silence, can add a right-to-left mark for Arabic, and drops and lists phrases speech models invent (subtitle credits, subscribe outros, sound tags, punctuation-only and looping lines). lint checks any SRT/VTT/JSON for overlaps, durations, reading speed and the same phrases. | `python3 scripts/caption_lines.py group words.json -o captions.srt --rlm` | tested-here |
| `suno-bridge` | The local half of the Suno MCP connector (A46). doctor prints the endpoint, OAuth scopes from the committed probe and the consent rule; probe makes an unauthenticated read-only HTTP check (401 = healthy, no credits); plan turns an Arabic or English request into a Suno brief (style tags, structure, lyric scaffold, duration, dialect, vocals-only for dua/nasheed) with a SHA-256 approval_digest and never generates; receipt checks the generation tool's returned JSON (song id, link, duration, optional downloaded file hash) against the digest the user approved and refuses any mismatch. | `python3 scripts/suno_bridge.py doctor` | tested-here |

<!-- hub:area:audio:end -->

## الفهرس / contents

1. [تنفيذ أصلي جديد — KOSIF Creative Intelligence (audio → motion)](#تنفيذ-أصلي-جديد--kosif-creative-intelligence-audio--motion)
2. [KOSIF Music Rhythm Intelligence — تحليل إيقاع عملي وربطه بالموشن](#kosif-music-rhythm-intelligence--تحليل-إيقاع-عملي-وربطه-بالموشن)
3. [Suno — أغنية بإذن وإيصال](#suno--أغنية-بإذن-وإيصال)

## تنفيذ أصلي جديد — KOSIF Creative Intelligence (audio → motion)

لربط صوت حقيقي بالرسم وتحريك الشخصيات والكاميرا، افتح [دليل Creative Intelligence التنفيذي](../creative-intelligence-execution.md) بدل الاكتفاء بروابط Librosa وWhisperX وRemotion. الجسر الموجود الآن:
- `scripts/audio_cue_mapper.py` يحلل WAV PCM بقياس RMS وتغيرات الطاقة، ويستورد كلمات WhisperX المحددة زمنيًا دون تخمين.
- `scripts/creative_reasoning_bridge.py` يقارن doodle وkinetic وcinematic بمعايير معلنة ثم يولد ملف Storyboard مطابقًا لعقد `motion_director.py`، مع تقرير قرار قابل للمراجعة.
- `evals/test_creative_intelligence.py` يغطي توقيت الكلمات العربية وتداخلها وثبات النتائج وحماية الملفات من الاستبدال.

    python3 $SKILL_DIR/scripts/audio_cue_mapper.py ./voice.wav --aligned-words ./words.json --out ./cues.json
    python3 $SKILL_DIR/scripts/creative_reasoning_bridge.py ./cues.json --out ./scene.json --report ./decisions.json
    python3 $SKILL_DIR/scripts/motion_director.py compile ./scene.json --out ./film.html
    python3 -m unittest discover -s $SKILL_DIR/evals -p test_creative_intelligence.py -v

حدود الإثبات: مرشحات تغيرات الطاقة ليست BPM أو ضربات موسيقية مؤكدة، وتحليل الطاقة لا يستنتج مشاعر الأغنية ولا معناها. الفيديو MP4 لا يُعد منجزًا حتى يُرندر وتُقاس إطاراته ومساره الصوتي. لا تنسخ ملفات مكتبات الطرف الثالث أو تحول المستودعات إلى شارات ✅ دون اختبارات وترخيص.

## KOSIF Music Rhythm Intelligence — تحليل إيقاع عملي وربطه بالموشن

لتحليل موسيقى أو أغنية عند وجود ملف PCM WAV محلي، استخدم [محرك الإيقاع التنفيذي](../music-rhythm-execution.md): يحسب عدة فرضيات BPM من مرشحات تغيّر الطاقة التي قِيست فعلاً، ويخرج فترات الطاقة العالية والمنخفضة. لا تخمّن كلمات الأغاني أو مشاعر المطرب أو تضع شارة ثقة زائفة، فالسرعة هنا تقدير قابل للنقض.

    python3 $SKILL_DIR/scripts/audio_cue_mapper.py ./voice.wav --out ./cues.json
    python3 $SKILL_DIR/scripts/music_rhythm_engine.py ./cues.json --out ./rhythm.json
    python3 $SKILL_DIR/scripts/reference_edit_engine.py --probe ./cuts.json --cues ./cues.json --out ./new-film-project

مشروع Remotion المولّد يستفيد من مرشحات الصوت لتكبير وتحريك الأشكال واللقطات وفق الإطار، ولا يقتصر على عرض بيانات BPM. التقييم الصحيح يتطلب معاينة الفيديو والصوت، ولا يتحول تخمين BPM إلى حقيقة مؤكدة بدون اختبار مرجعي.

## Captions from word timings

After transcription (whisper.cpp with `-ml 1 -oj`, faster-whisper, or an atlas `words.json`), `caption_lines.py` turns the words into lines people can read: at most four words or 32 characters, at most 3.2 s on screen, a new line at a pause or a sentence end (`؟ ؛ . !`), short holes closed, short lines extended only into silence. It drops the phrases speech models invent over silence or music and lists them, so nothing disappears silently; `--keep-suspect` keeps them marked instead. Add `--rlm` for Arabic SRT so players keep end punctuation on the left.

    python3 $SKILL_DIR/scripts/caption_lines.py group ./words.json -o ./captions.srt --rlm
    python3 $SKILL_DIR/scripts/caption_lines.py lint ./captions.srt

The rules came from a read-only study of an Arabic desktop editor ([montaji.md](../app-studies/montaji.md)); the code, thresholds and phrase list are KOSIF's own.

## Suno — أغنية بإذن وإيصال

التوليد نفسه بيحصل من موصّل Suno MCP (`https://api.suno.com/mcp`، دخول بحساب Suno، الملحق A46). `scripts/suno_bridge.py` هو النص المحلي: بيجهّز البرومبت، وبيربط موافقة المستخدم ببصمة، وبيراجع النتيجة. عمره ما بيولّد ولا بيصرف رصيد.

    python3 $SKILL_DIR/scripts/suno_bridge.py doctor                       # الحالة والصلاحيات من غير شبكة
    python3 $SKILL_DIR/scripts/suno_bridge.py plan "نشيد رمضان بدون موسيقى" --out out/suno/plan.json
    # اعرض الستايل والكلمات والمدة، استنى «موافق»، نادِ أداة التوليد في موصّل Suno، احفظ ردها JSON
    python3 $SKILL_DIR/scripts/suno_bridge.py receipt --plan out/suno/plan.json --result out/suno/result.json --approved-digest <digest> --out out/suno/receipt.json

- أي تعديل في البرومبت بيغيّر البصمة، فلازم موافقة جديدة. `receipt` بيرفض لو البصمة مختلفة أو الرد مفيهوش معرّف أغنية.
- التنين الأسود بيشغّله كـ adapter (`tool:suno-bridge`، أمر `plan`) فبيطلع برومبت Suno لأي مهمة فيها موسيقى، مع إيصال SHA-256.
