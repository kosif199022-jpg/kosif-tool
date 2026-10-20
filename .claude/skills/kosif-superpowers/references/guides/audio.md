# الصوت والإيقاع وتوقيت الكلمات — Audio, rhythm and word timing

تحليل الصوت الحقيقي إلى مرشحات طاقة وكلمات موقّتة وفرضيات BPM، ثم ربطها بقرارات الحركة.

Turning real audio into energy cues, timed words and tempo hypotheses, then into motion decisions.

Commands below are typed from the skill folder (`.claude/skills/kosif-superpowers/`) unless they say otherwise; `$SKILL_DIR` means that folder.

<!-- hub:area:audio:start -->

**الأدوات / tools (2)** — `python3 scripts/hub.py tool <id>` for every command, requirement and limit:

| tool | what it does | start with | evidence |
|---|---|---|---|
| `audio-cue-mapper` | Measures a 16-bit PCM WAV (up to 120 s) into a kosif.audio-cues.v1 JSON: a 50 ms RMS energy envelope and rising-energy onset candidates. It can also import existing WhisperX/KOSIF word timings after checking their order and range. It never invents BPM, beats, words or emotion. | `python3 scripts/audio_cue_mapper.py ./voice.wav --out ./out/cues.json` | tested-here |
| `music-rhythm-engine` | Turns a kosif.audio-cues.v1 file into tempo hypotheses. It scores 60–200 BPM against the measured onset candidates and returns the top three distinct tempos. It adds an estimated beat grid when the best match is at least 0.60, plus per-second energy sections relative to the track median. All results are flagged as unverified. | `python3 scripts/music_rhythm_engine.py ./out/cues.json --out ./out/rhythm.json` | tested-here |

<!-- hub:area:audio:end -->

## الفهرس / contents

1. [تنفيذ أصلي جديد — KOSIF Creative Intelligence (audio → motion)](#تنفيذ-أصلي-جديد--kosif-creative-intelligence-audio--motion)
2. [KOSIF Music Rhythm Intelligence — تحليل إيقاع عملي وربطه بالموشن](#kosif-music-rhythm-intelligence--تحليل-إيقاع-عملي-وربطه-بالموشن)

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
