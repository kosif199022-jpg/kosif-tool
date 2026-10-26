# `voice-tts` — الصوت والموسيقى والتعليق (55 بطاقة)

> مكتبة بروتوكول USIP v5.6 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/voice-tts.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/audio.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`VOICE-01` تعليق عربي محلي بـ Piper](#voice-01--تعليق-عربي-محلي-بـ-piper--piper-offline-arabic-tts)
- [`VOICE-02` صوت ويندوز العربي (نايف) بالجدول الزمني](#voice-02--صوت-ويندوز-العربي-نايف-بالجدول-الزمني--windows-onecore-arabic-narration-naayf)
- [`VOICE-03` Kokoro المحلي (بلا عربية)](#voice-03--kokoro-المحلي-بلا-عربية--kokoro-local-tts-no-arabic-voice)
- [`VOICE-04` نطق المتصفح العربي ar-SA](#voice-04--نطق-المتصفح-العربي-ar-sa--browser-web-speech-fallback-ar-sa)
- [`VOICE-05` أصوات Edge العصبية والمولدات المبنية عليها](#voice-05--أصوات-edge-العصبية-والمولدات-المبنية-عليها--edge-neural-voices--scene-file-generators)
- [`VOICE-06` تعليق ElevenLabs بإعدادات جاهزة](#voice-06--تعليق-elevenlabs-بإعدادات-جاهزة--elevenlabs-narration-presets)
- [`VOICE-07` اختيار النموذج والصيغة حسب الاستخدام](#voice-07--اختيار-النموذج-والصيغة-حسب-الاستخدام--model--output-format-choice)
- [`VOICE-08` تقسيم النص الطويل مع حفظ النبرة](#voice-08--تقسيم-النص-الطويل-مع-حفظ-النبرة--long-script-chunking-with-prosody-context)
- [`VOICE-09` استنساخ صوت بموافقة صاحبه](#voice-09--استنساخ-صوت-بموافقة-صاحبه--consented-voice-cloning)
- [`VOICE-10` تحويل صوت إلى صوت](#voice-10--تحويل-صوت-إلى-صوت--speech-to-speech-re-voice)
- [`VOICE-11` Gemini TTS بثلاثين صوتًا](#voice-11--gemini-tts-بثلاثين-صوتًا--gemini-tts-with-30-prebuilt-voices)
- [`VOICE-12` إخراج أداء الصوت بواسطة Claude](#voice-12--إخراج-أداء-الصوت-بواسطة-claude--claude-directed-voice-performance)
- [`VOICE-13` حوار بأكثر من متكلم](#voice-13--حوار-بأكثر-من-متكلم--multi-speaker-dialogue-production)
- [`VOICE-14` HeyGen Starfish بطوابع زمنية للكلمات](#voice-14--heygen-starfish-بطوابع-زمنية-للكلمات--heygen-starfish-tts-with-word-timestamps)
- [`VOICE-15` محرك الصوت الموحد audio_meta.json](#voice-15--محرك-الصوت-الموحد-audio_metajson--unified-audio-engine-voice--words--bgm--sfx)
- [`VOICE-16` كتالوج Together للصوت](#voice-16--كتالوج-together-للصوت--together-ai-tts-catalog)
- [`VOICE-17` أوضاع مخرج الصوت الخارجي](#voice-17--أوضاع-مخرج-الصوت-الخارجي--kosif-voice-director-provider-modes)
- [`VOICE-18` ميزانية الكلمات في الثانية](#voice-18--ميزانية-الكلمات-في-الثانية--words-per-second-budget)
- [`VOICE-19` السرعة حسب المحتوى — أعد التوليد ولا تمطّ](#voice-19--السرعة-حسب-المحتوى--أعد-التوليد-ولا-تمطّ--read-speed-by-content--regenerate-never-stretch)
- [`VOICE-20` نص النطق غير نص الشاشة](#voice-20--نص-النطق-غير-نص-الشاشة--spoken-form-vs-on-screen-form)
- [`VOICE-21` قواعد كتابة التعليق للمشهد](#voice-21--قواعد-كتابة-التعليق-للمشهد--scene-narration-writing-rules)
- [`VOICE-22` سكربت تعليق بوسوم أداء SSML](#voice-22--سكربت-تعليق-بوسوم-أداء-ssml--vo-script-with-performance-tags-ssml)
- [`VOICE-23` نص التعليق المقفل SCRIPT.md](#voice-23--نص-التعليق-المقفل-scriptmd--locked-narration-file-scriptmd)
- [`VOICE-24` توجيه الصوت باللهجات العربية](#voice-24--توجيه-الصوت-باللهجات-العربية--arabic-dialect-voice-direction-workflow)
- [`VOICE-25` اختيار اللغة واللهجة في المقابلة](#voice-25--اختيار-اللغة-واللهجة-في-المقابلة--language--dialect-intake-field)
- [`VOICE-26` شخصية اليوتيوبر المصري](#voice-26--شخصية-اليوتيوبر-المصري--egyptian-youtuber-voice-persona)
- [`VOICE-27` صوت الراوي الوثائقي المقفل](#voice-27--صوت-الراوي-الوثائقي-المقفل--locked-documentary-narrator-voice)
- [`VOICE-28` جمل صوت المدرب](#voice-28--جمل-صوت-المدرب--coach-voice-cue-lines)
- [`VOICE-29` مواصفات تسجيل الصوت البشري](#voice-29--مواصفات-تسجيل-الصوت-البشري--human-vo-recording-spec)
- [`VOICE-30` مدرب اللغة الثنائي](#voice-30--مدرب-اللغة-الثنائي--language-coach-aren-skill)
- [`VOICE-31` مدة المشهد = طول التعليق + هامش](#voice-31--مدة-المشهد--طول-التعليق--هامش--scene-duration-from-voice-length)
- [`VOICE-32` توقيت كلمات التعليق المولد بـ faster-whisper](#voice-32--توقيت-كلمات-التعليق-المولد-بـ-faster-whisper--word-timings-from-the-generated-voice-faster-whisper)
- [`VOICE-33` إعادة لصق النص المعروف على توقيت ويسبر](#voice-33--إعادة-لصق-النص-المعروف-على-توقيت-ويسبر--re-attach-the-known-script-to-whisper-timings)
- [`VOICE-34` إيقاع يقوده التعليق](#voice-34--إيقاع-يقوده-التعليق--voice-led-pacing)
- [`VOICE-35` قراءة صوتية بتظليل الكلمة المنطوقة](#voice-35--قراءة-صوتية-بتظليل-الكلمة-المنطوقة--read-aloud-karaoke-highlight)
- [`VOICE-36` ترجمة تُكتب على توقيت الصوت](#voice-36--ترجمة-تُكتب-على-توقيت-الصوت--typewriter-captions-on-voice-word-times)
- [`VOICE-37` موجة الصوت ومؤشر التشغيل](#voice-37--موجة-الصوت-ومؤشر-التشغيل--voice-waveform-with-playhead)
- [`VOICE-38` محاضرة مروية: رسم يتقدم مع الجمل](#voice-38--محاضرة-مروية-رسم-يتقدم-مع-الجمل--narrated-lecture-draw-on-paced-to-sentences)
- [`VOICE-39` سلسلة تنظيف الصوت البشري](#voice-39--سلسلة-تنظيف-الصوت-البشري--voice-clean-up-chain)
- [`VOICE-40` وصفات إصلاح الصوت بالأعراض](#voice-40--وصفات-إصلاح-الصوت-بالأعراض--voice-repair-presets-by-symptom)
- [`VOICE-41` أزياء صوتية للشخصيات](#voice-41--أزياء-صوتية-للشخصيات--character-voice-costumes)
- [`VOICE-42` مختبر الصوت: عزل الصوت وفصل الموسيقى](#voice-42--مختبر-الصوت-عزل-الصوت-وفصل-الموسيقى--audiolab-voice-isolation--stem-split)
- [`VOICE-43` خفض الموسيقى تحت التعليق](#voice-43--خفض-الموسيقى-تحت-التعليق--music-ducking-under-the-voice)
- [`VOICE-44` التسليم بجهارة −14 LUFS وفحص البوابة](#voice-44--التسليم-بجهارة-14-lufs-وفحص-البوابة--14-lufs-delivery--gate)
- [`VOICE-45` وصل المقاطع كـ WAV لا MP3](#voice-45--وصل-المقاطع-كـ-wav-لا-mp3--join-chunks-as-pcm-not-mp3-copy)
- [`VOICE-46` محادثة صوتية عربية لحظية عبر WebRTC](#voice-46--محادثة-صوتية-عربية-لحظية-عبر-webrtc--realtime-arabic-speech-to-speech-webrtc)
- [`VOICE-47` مقاطعة المساعد بالكلام](#voice-47--مقاطعة-المساعد-بالكلام--barge-in-interruption)
- [`VOICE-48` موجه نوايا صوتي عربي حتمي](#voice-48--موجه-نوايا-صوتي-عربي-حتمي--deterministic-arabic-voice-intent-router)
- [`VOICE-49` كرة الصوت بحالاتها](#voice-49--كرة-الصوت-بحالاتها--voice-orb-state-animation)
- [`VOICE-50` نبض حلقة زر الميكروفون العائم](#voice-50--نبض-حلقة-زر-الميكروفون-العائم--live-mic-fab-ring-pulse)
- [`VOICE-51` التقاط ميكروفون نظيف](#voice-51--التقاط-ميكروفون-نظيف--clean-mic-capture-constraints)
- [`VOICE-52` تسجيل الصوت وتنزيله](#voice-52--تسجيل-الصوت-وتنزيله--mediarecorder-capture--download)
- [`VOICE-53` لا تقليد لأصوات حقيقية](#voice-53--لا-تقليد-لأصوات-حقيقية--never-imitate-real-voices)
- [`VOICE-54` لا ادعاء بلا ملف](#voice-54--لا-ادعاء-بلا-ملف--no-audio-claim-without-a-receipt)
- [`VOICE-55` نظافة تكلفة الحروف](#voice-55--نظافة-تكلفة-الحروف--tts-character-cost-hygiene)

## البطاقات / cards

### `VOICE-01` — تعليق عربي محلي بـ Piper / Piper offline Arabic TTS

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `receipt` |
| الرخصة | piper-tts is GPL-3.0-or-later (call it as a CLI, do not vendor its code); the kareem dataset licence is 'see URL' on the model card — check before commercial delivery. |

**ما هي:** تحوّل نصًا عربيًا إلى WAV على المعالج دون إنترنت ودون مفتاح، بصوت ar_JO-kareem. / Synthesises Arabic narration on CPU, offline and keyless, with the ar_JO-kareem voice.

**متى:** حين تحتاج تعليقًا صوتيًا عربيًا من نص دون إنترنت ودون مفتاح أو اشتراك / when you need Arabic narration from text offline on CPU, with no API key

**كيف:** Install piper-tts in a venv, download the voice model (.onnx + .onnx.json) from huggingface.co/rhasspy/piper-voices (ar/ar_JO/kareem/medium, 63 MB), pipe the text in. Output is 22.05 kHz mono; resample to 48 kHz and loudnorm before muxing (VOICE-44). One sentence per line so --sentence-silence places breaths. Ran here: a 10-word Arabic line → 7.43 s WAV at -16.5 LUFS integrated; with --length-scale 1.15 and --sentence-silence 0.35 two sentences → 7.13 s. (code snippet in references/powers/voice-tts.md)

**المعاملات:** voice ar_JO-kareem-medium (1 speaker, 22050 Hz); inference noise_scale 0.667, noise_w 0.8, length_scale 1.0 (1.1–1.2 = slower, calmer); --sentence-silence 0.2–0.5 s; --volume 1.0

**التثبيت:** python3 -m venv .venv && .venv/bin/pip install piper-tts && curl -L -O https://huggingface.co/rhasspy/piper-voices/resolve/main/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx{,.json}

**الوسوم:** بايبر · تعليق عربي · دون إنترنت · piper · offline tts · arabic voice · kareem · تحويل نص لصوت · تعليق صوتي · قراءة النص · text to speech · voiceover

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:piper` ← python3 -c "import piper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:onnxruntime` ← python3 -c "import onnxruntime" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `network` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `run here 2026-10-16: piper-tts 1.8.0 → ar.wav 7.43 s, -16.5 LUFS`
- `probe.md: piper-tts 1.8.0 installable, huggingface.co reachable`

#### 7. قدرات قريبة في العائلة

- `VOICE-02` صوت ويندوز العربي (نايف) بالجدول الزمني / Windows OneCore Arabic narration (Naayf) (documented)
- `VOICE-03` Kokoro المحلي (بلا عربية) / Kokoro local TTS (no Arabic voice) (install)

### `VOICE-02` — صوت ويندوز العربي (نايف) بالجدول الزمني / Windows OneCore Arabic narration (Naayf)

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سكربت المالك voice.py ينطق النص بأصوات ويندوز المثبتة (Microsoft Naayf ar-SA) ويُخرج مسارًا واحدًا وتوقيت كل سطر. / Owner script voice.py speaks a timed script with installed Windows voices (Microsoft Naayf ar-SA) and writes one track plus per-line timings.

**متى:** حين يعمل المستخدم على ويندوز ويريد تعليقًا عربيًا بأصوات الجهاز المثبتة مع توقيت لكل سطر / when on Windows and you want Arabic (ar-SA) narration from installed voices plus per-line timings

**كيف:** PowerShell + SSML prosody under the hood. `python voice.py --list`; `voice.py out.wav --text '…' --voice Naayf --rate -5%`; or `--script lines.json [--seconds 15]` → out.wav + out.json [{t,end,text}] for captions and ducking. Trims silence (\|x\|>0.004) keeping 20 ms head / 80 ms tail, resamples to 48 kHz stereo, peak 0.89. In a composition mark it `<audio data-role="voice">` so the mux ducks other clips and normalises to -14 LUFS. The Basma editor calls the same voices through the local bridge (GET /api/voices, POST /api/voice {lines:[{t,text}],voice:'Naayf',seconds}). Owner code, but it needs powershell.exe + OneCore → it does NOT run in this Linux container; use VOICE-01 here.

**المعاملات:** default rate −4 % (CLI examples −5 %), pitch +0 %; 48 kHz stereo; peak 0.89; head 20 ms / tail 80 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نايف · ويندوز · تعليق دون إنترنت · naayf · onecore · windows tts · ssml · voice.py · صوت سعودي · توقيت الأسطر · تعليق صوتي · ar-sa · line timings

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/voice.py:82`
- `kosif-one/tools/kosif-studio/motion/voice.py`
- `100-superskills/skills/kosif-montage-motion/scripts/voice.py`
- `app/public/js/00_editor.js:2638`

#### 7. قدرات قريبة في العائلة

- `VOICE-01` تعليق عربي محلي بـ Piper / Piper offline Arabic TTS (proven)
- `VOICE-03` Kokoro المحلي (بلا عربية) / Kokoro local TTS (no Arabic voice) (install)
- `VOICE-04` نطق المتصفح العربي ar-SA / Browser Web Speech fallback (ar-SA) (ready)

### `VOICE-03` — Kokoro المحلي (بلا عربية) / Kokoro local TTS (no Arabic voice)

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** محرك محلي مجاني بـ 54 صوتًا في 8 لغات؛ أول حرف من معرّف الصوت يحدد اللغة — ولا صوت عربي فيه. / Free CPU TTS with 54 voices in 8 languages; the voice-id prefix encodes language — no Arabic voice.

**متى:** حين تحتاج تعليقًا مجانيًا على المعالج بالإنجليزية أو لغة أخرى غير العربية، فلا صوت عربي في Kokoro / when you need free local narration in English or another non-Arabic language

**كيف:** Prefixes a/b/e/f/h/i/j/p/z = en-US/en-GB/es/fr/hi/it/ja/pt-BR/zh; good voices af_heart, af_nova, am_adam, bf_emma. Python: `pip install kokoro soundfile` (~311 MB model from huggingface.co; non-English needs espeak-ng, not installed here). JS: `npm i kokoro-js` (1.2.1). The HyperFrames wrapper `npx hyperframes tts` is NOT installable here (@hyperframes/cli 404 on npm).

**المعاملات:** speed 0.7–0.8 tutorial · 1.0 natural · 1.1–1.2 upbeat; 24 kHz output

**التثبيت:** pip install kokoro soundfile # or: npm i kokoro-js

**الوسوم:** كوكورو · صوت إنجليزي · kokoro · af_heart · local tts · english narration · تعليق إنجليزي · صوت مجاني · تحويل نص لصوت · free tts · kokoro-js

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:kokoro` ← python3 -c "import kokoro" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:soundfile` ← python3 -c "import soundfile" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `network` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/tts.md`
- `kosif-one/vendor/hyperframes/docs/packages/cli.mdx`
- `kosif-one/vendor/brag/skills/brag/SKILL.md`
- `probe.md: kokoro 0.7.16, kokoro-js 1.2.1`

#### 7. قدرات قريبة في العائلة

- `VOICE-01` تعليق عربي محلي بـ Piper / Piper offline Arabic TTS (proven)
- `VOICE-02` صوت ويندوز العربي (نايف) بالجدول الزمني / Windows OneCore Arabic narration (Naayf) (documented)
- `VOICE-04` نطق المتصفح العربي ar-SA / Browser Web Speech fallback (ar-SA) (ready)
- `VOICE-05` أصوات Edge العصبية والمولدات المبنية عليها / Edge neural voices & scene-file generators (documented)

### `VOICE-04` — نطق المتصفح العربي ar-SA / Browser Web Speech fallback (ar-SA)

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حين لا توجد جلسة صوتية، يقرأ التطبيق الرد بصوت الجهاز العربي عبر Web Speech API. / With no live session, the app reads replies aloud with the device's Arabic voice via the Web Speech API.

**متى:** حين يحتاج تطبيق ويب قراءة الرد بصوت الجهاز العربي في غياب جلسة صوتية، لا لتسجيل تعليق نهائي / when a web app should read replies aloud with the device's Arabic voice, not for final narration

**كيف:** Strip bullets/asterisks first (`text.replace(/[•*]/g,'')`), `speechSynthesis.cancel()` then speak a `SpeechSynthesisUtterance` with `lang='ar-SA'`; onstart/onend toggle the speaking state (drives VOICE-49). Voice quality depends on the viewer's OS and is not capturable by a headless render — never use it for an MP4. (code snippet in references/powers/voice-tts.md)

**المعاملات:** lang ar-SA; default rate/pitch (owner code sets none)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نطق المتصفح · قراءة الرد · web speech · speechSynthesis · ar-SA · fallback · قراءة بصوت عال · صوت الجهاز · تطبيق ويب · read aloud · browser tts

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-audit-studio/voice.js:380`
- `kosif-earth-ci-fork/ui/features/assistant.js:281`

#### 7. قدرات قريبة في العائلة

- `VOICE-02` صوت ويندوز العربي (نايف) بالجدول الزمني / Windows OneCore Arabic narration (Naayf) (documented)
- `VOICE-03` Kokoro المحلي (بلا عربية) / Kokoro local TTS (no Arabic voice) (install)
- `VOICE-05` أصوات Edge العصبية والمولدات المبنية عليها / Edge neural voices & scene-file generators (documented)
- `VOICE-06` تعليق ElevenLabs بإعدادات جاهزة / ElevenLabs narration presets (key)

### `VOICE-05` — أصوات Edge العصبية والمولدات المبنية عليها / Edge neural voices & scene-file generators

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مولدات تحول ملف مشاهد (YAML أو JSON) إلى فيديو مروي بأصوات Edge مع ترجمة تلقائية، وفي Edge أصوات عربية مصرية وسعودية. / Generators that turn a scenes file (YAML or JSON) into a narrated MP4 with Edge neural voices and auto subtitles; Edge has ar-EG and ar-SA voices.

**متى:** حين تريد تحويل ملف مشاهد إلى فيديو مروي بترجمة تلقائية بأصوات Edge، ومنها المصرية والسعودية / when turning a scenes file into a narrated video with auto subtitles using Edge voices, incl. ar-EG and ar-SA

**كيف:** video-guide-creator: YAML (title-card, bullet-points, outro or screencast steps with CSS selectors) → Docker → MP4; brand presets hold colours, voice, language, logo (default en-US-AriaNeural — switch to an ar-* voice). framecraft: scenes.json → Playwright frames → Edge TTS → FFmpeg 1920x1080 with --auto-duration. Here: `pip install edge-tts` works but speech.platform.bing.com answered 400 in the probe, the Docker image is not built and uv/framecraft are external → treat as documented. Transferable idea: a KOSIF YAML → HTML scene generator feeding VOICE-01.

**المعاملات:** default en-US-AriaNeural; Arabic voices exist for ar-EG and ar-SA

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إيدج · يامل · فيديو إرشادي · edge-tts · yaml guide · framecraft · auto duration · شرح برنامج · صوت مصري · ترجمة تلقائية · screencast · narrated video

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `docker` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2836-video-guide/11537-video-guide-creator/SKILL.md`
- `kosif-atlas/skills/2836-video-guide/11537-video-guide-creator/references/slide-templates.md`
- `kosif-atlas/skills/1644-framecraft/4629-demo-video`
- `probe.md: speech.platform.bing.com 400`

#### 7. قدرات قريبة في العائلة

- `VOICE-03` Kokoro المحلي (بلا عربية) / Kokoro local TTS (no Arabic voice) (install)
- `VOICE-04` نطق المتصفح العربي ar-SA / Browser Web Speech fallback (ar-SA) (ready)
- `VOICE-06` تعليق ElevenLabs بإعدادات جاهزة / ElevenLabs narration presets (key)
- `VOICE-07` اختيار النموذج والصيغة حسب الاستخدام / Model & output-format choice (key)

### `VOICE-06` — تعليق ElevenLabs بإعدادات جاهزة / ElevenLabs narration presets

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مقطع MP3 لكل مشهد بنموذج eleven_multilingual_v2 وإعدادات صوت مضبوطة لكل استخدام. / One MP3 per scene via eleven_multilingual_v2 with tuned voice settings per use case.

**متى:** حين تريد ملف تعليق MP3 لكل مشهد بإعدادات صوت مضبوطة لكل استخدام عبر ElevenLabs / when you want one MP3 per scene with use-case voice presets via ElevenLabs

**كيف:** POST /v1/text-to-speech/{voiceId} (or @elevenlabs/elevenlabs-js textToSpeech.convert) with model_id eleven_multilingual_v2 and voice_settings; key in env ELEVENLABS_API_KEY. Then size each scene to its file (VOICE-31: Remotion calculateMetadata sums durations). Presets: narration stability 0.5 / similarity 0.75 / style 0–0.3; conversational 0.4 / 0.6 / 0.3; cloned voice similarity 0.85. 5000 chars per request.

**المعاملات:** stability 0–1, similarity_boost 0–1, style 0–1, speed 0.7–1.2; ≤5000 chars/request

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إليفن لابز · تعليق تجاري · elevenlabs · multilingual_v2 · voice settings · stability · تعليق صوتي · إعدادات الصوت · تحويل نص لصوت · tts presets · narration

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `key:elevenlabs` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1847-elevenlabs-pack/5514-elevenlabs-core-workflow-a`
- `kosif-atlas/skills/2712-remotion/10436-remotion-markup/voiceover.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-04` نطق المتصفح العربي ar-SA / Browser Web Speech fallback (ar-SA) (ready)
- `VOICE-05` أصوات Edge العصبية والمولدات المبنية عليها / Edge neural voices & scene-file generators (documented)
- `VOICE-07` اختيار النموذج والصيغة حسب الاستخدام / Model & output-format choice (key)
- `VOICE-08` تقسيم النص الطويل مع حفظ النبرة / Long-script chunking with prosody context (key)

### `VOICE-07` — اختيار النموذج والصيغة حسب الاستخدام / Model & output-format choice

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جدول يختار نموذج ElevenLabs حسب زمن الاستجابة والتعبير، وصيغة المخرج حسب الوجهة. / Picks the ElevenLabs model by latency vs expressiveness and the output format by destination.

**متى:** حين تختار نموذج ElevenLabs حسب سرعة الاستجابة والتعبير، وصيغة الملف للمونتاج أو التسليم / when picking an ElevenLabs model by latency vs expressiveness and the output format for editing or delivery

**كيف:** flash (~75 ms TTFB) for realtime, turbo (~150 ms), multilingual_v2 (~300 ms) for narration, v3 (~500 ms, 70+ languages incl. Arabic) for maximum expression. flash/turbo cost 0.5 credit/char, v2/v3 1.0. Format: pcm_44100 for editing, mp3_44100_128 (~16 KB/s) for delivery, mp3_22050_32 only for streaming previews.

**المعاملات:** TTFB flash 75 / turbo 150 / v2 300 / v3 500 ms; credits 0.5 vs 1.0 per char

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نموذج الصوت · صيغة الصوت · model choice · pcm · latency · eleven_v3 · اختيار النموذج · تكلفة الحروف · صيغة المخرج · mp3 · realtime

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:elevenlabs` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1847-elevenlabs-pack/5522-elevenlabs-performance-tuning`
- `kosif-atlas/skills/1847-elevenlabs-pack/5516-elevenlabs-cost-tuning`

#### 7. قدرات قريبة في العائلة

- `VOICE-05` أصوات Edge العصبية والمولدات المبنية عليها / Edge neural voices & scene-file generators (documented)
- `VOICE-06` تعليق ElevenLabs بإعدادات جاهزة / ElevenLabs narration presets (key)
- `VOICE-08` تقسيم النص الطويل مع حفظ النبرة / Long-script chunking with prosody context (key)
- `VOICE-09` استنساخ صوت بموافقة صاحبه / Consented voice cloning (key)

### `VOICE-08` — تقسيم النص الطويل مع حفظ النبرة / Long-script chunking with prosody context

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يقسم النص الأطول من حد الطلب مع تمرير النص المجاور لكل قطعة كي تتصل النبرة عبر الوصلات. / Splits over-limit scripts while passing neighbouring text so intonation flows across joins.

**متى:** حين يكون نص التعليق أطول من حد الطلب وتريد تقسيمه دون أن تنقطع النبرة عند الوصلات / when a narration script exceeds the request limit and must be split without breaking intonation at joins

**كيف:** Split on sentence ends below 5000 chars; send previous_text / next_text with each chunk; decode every chunk to WAV and concat the WAVs (or concat with re-encode) — never `-c copy` MP3s, whose frame padding drifts word timings by tens of ms per join (see VOICE-45).

**المعاملات:** chunk < 5000 chars; joins in PCM

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تقسيم النص · نبرة · chunking · previous_text · prosody · long script · نص طويل · دمج المقاطع · وصلات الصوت · concat · request limit

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1847-elevenlabs-pack/5514-elevenlabs-core-workflow-a`
- `kosif-atlas/skills/3323-joined-audio-transcript-drift/13837-joined-audio-transcript-drift`

#### 7. قدرات قريبة في العائلة

- `VOICE-06` تعليق ElevenLabs بإعدادات جاهزة / ElevenLabs narration presets (key)
- `VOICE-07` اختيار النموذج والصيغة حسب الاستخدام / Model & output-format choice (key)
- `VOICE-09` استنساخ صوت بموافقة صاحبه / Consented voice cloning (key)
- `VOICE-10` تحويل صوت إلى صوت / Speech-to-speech re-voice (key)

### `VOICE-09` — استنساخ صوت بموافقة صاحبه / Consented voice cloning

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صوت مخصص من عينات نظيفة قصيرة لمتحدث موافق — عبر ElevenLabs أو HeyGen. / A custom voice from short clean samples of a consenting speaker — ElevenLabs or HeyGen.

**متى:** حين يريد المستخدم صوتًا مخصصًا مستنسخًا من عينات نظيفة لمتحدث موافق / when the user wants a custom cloned voice from clean samples of a consenting speaker

**كيف:** ElevenLabs: client.voices.add({name,files}) with 1–25 files, ≥30 s total clean speech, no music; then similarity 0.85. HeyGen: heygen-voice.mjs clone uploads base64 mp3/wav, polls until complete (gives up at 120 s), prints the voice id; list/delete supported. Its 14 mocked tests ran green here, the real call needs HEYGEN_ACCESS_TOKEN. Consent first (VOICE-53).

**المعاملات:** min 30 s clean speech; 1–25 samples; mp3 or wav only; 120 s clone deadline

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** استنساخ · صوت المالك · voice clone · consent · heygen · elevenlabs · صوت مخصص · نسخ الصوت · عينات صوتية · custom voice · voice samples

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:elevenlabs` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1847-elevenlabs-pack/5514-elevenlabs-core-workflow-a`
- `kosif-one/vendor/hyperframes/skills/media-use/audio/scripts/heygen-voice.mjs`
- `kosif-one/vendor/hyperframes/skills/media-use/audio/scripts/heygen-voice.test.mjs`

#### 7. قدرات قريبة في العائلة

- `VOICE-07` اختيار النموذج والصيغة حسب الاستخدام / Model & output-format choice (key)
- `VOICE-08` تقسيم النص الطويل مع حفظ النبرة / Long-script chunking with prosody context (key)
- `VOICE-10` تحويل صوت إلى صوت / Speech-to-speech re-voice (key)
- `VOICE-11` Gemini TTS بثلاثين صوتًا / Gemini TTS with 30 prebuilt voices (key)

### `VOICE-10` — تحويل صوت إلى صوت / Speech-to-speech re-voice

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يعيد أداء تسجيل بشري بصوت آخر مع الحفاظ على توقيته وانفعاله. / Re-voices a recorded performance in another voice while keeping its timing and emotion.

**متى:** حين لديك تسجيل بشري وتريد إعادة أدائه بصوت آخر مع الحفاظ على توقيته وانفعاله / when you have a recorded performance and want it re-voiced in another voice keeping timing and emotion

**كيف:** speechToSpeech.convert(voiceId,{audio, model_id:'eleven_english_sts_v2', remove_background_noise:true}); input 1 s–5 min. Because the timing survives, the words.json you already built on the guide take stays valid.

**المعاملات:** input 1 s–5 min; remove_background_noise true

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تحويل الصوت · إعادة الأداء · speech to speech · voice changer · guide take · تغيير الصوت · صوت آخر · مغير الصوت · re-voice · sts

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1847-elevenlabs-pack/5515-elevenlabs-core-workflow-b`

#### 7. قدرات قريبة في العائلة

- `VOICE-08` تقسيم النص الطويل مع حفظ النبرة / Long-script chunking with prosody context (key)
- `VOICE-09` استنساخ صوت بموافقة صاحبه / Consented voice cloning (key)
- `VOICE-11` Gemini TTS بثلاثين صوتًا / Gemini TTS with 30 prebuilt voices (key)
- `VOICE-12` إخراج أداء الصوت بواسطة Claude / Claude-directed voice performance (key)

### `VOICE-11` — Gemini TTS بثلاثين صوتًا / Gemini TTS with 30 prebuilt voices

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** محرر بصمة يسجّل التعليق العربي بـ Gemini ويضعه على الخط الزمني، ويغلف PCM بترويسة WAV. / The Basma editor records Arabic narration with Gemini TTS and drops it on the timeline, wrapping PCM as WAV.

**متى:** حين تريد تسجيل تعليق عربي بأحد أصوات Gemini الجاهزة ووضعه على الخط الزمني في محرر بصمة / when recording Arabic narration with a prebuilt Gemini voice onto the Basma editor timeline

**كيف:** responseModalities AUDIO + prebuiltVoiceConfig; L16 PCM at 24 kHz wrapped with a 44-byte WAV header; models gemini-3.8-flash-tts (default), 3.8-flash-lite-tts, 2.5-flash-preview-tts; captions re-sync from the voice's voiced stretches. Needs a Gemini API key.

**المعاملات:** 30 voices: Kore, Puck, Charon, Zephyr, Fenrir, Leda, Orus, Aoede, Callirrhoe, Autonoe, Enceladus, Iapetus, Umbriel, Algieba, Despina, Erinome, Algenib, Rasalgethi, Laomedeia, Achernar, Alnilam, Schedar, Gacrux, Pulcherrima, Achird, Zubenelgenubi, Vindemiatrix, Sadachbia, Sadaltager, Sulafat; 24 kHz PCM; temperature ~0.85, top-p ~0.95 for persona reads

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** جيميني · بصمة · ثلاثون صوتًا · gemini tts · kore · puck · pcm wav header · تعليق صوتي · تحويل نص لصوت · أصوات جاهزة · prebuilt voices · basma

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `app/public/js/00_editor.js:1927`
- `app/public/js/10_studio.js:2198`
- `app/public/js/10_studio.js:2193`

#### 7. قدرات قريبة في العائلة

- `VOICE-09` استنساخ صوت بموافقة صاحبه / Consented voice cloning (key)
- `VOICE-10` تحويل صوت إلى صوت / Speech-to-speech re-voice (key)
- `VOICE-12` إخراج أداء الصوت بواسطة Claude / Claude-directed voice performance (key)
- `VOICE-13` حوار بأكثر من متكلم / Multi-speaker dialogue production (key)

### `VOICE-12` — إخراج أداء الصوت بواسطة Claude / Claude-directed voice performance

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قبل أن ينطق المحرك، تكتب أنت ملاحظة أداء JSON: النبرة والطاقة والسرعة والطبقة والوقفات والكلمات المشددة وأنسب صوت. / Before the engine speaks you write a JSON performance note: tone, energy, pace, pitch, pauses, stressed words and the best voice.

**متى:** حين تريد أن يبدو التعليق المولد مُخرجًا، فتحدد قبله النبرة والطاقة والسرعة والوقفات والكلمات المشددة / when you want generated narration to sound directed by setting tone, energy, pace, pauses and stress first

**كيف:** VOICE.direct(text) → {note ≤60 words, voice, pace 2–4 wps, energy 1–10, pitch low\|mid\|high, stress[]}; the Gemini wrapper prefixes Cairo-colloquial pronunciation rules (ج hard g, ق glottal stop, ث → s/t, ذ → z/d). The direction half needs no key — apply the same JSON to Piper (length_scale from pace) or any engine. (code snippet in references/powers/voice-tts.md)

**المعاملات:** pace 2–4 words/s; energy 1–10; note ≤ 60 words

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إخراج الصوت · ملاحظة أداء · voice direction · performance note · stress words · pace · نبرة الصوت · أداء صوتي · وقفات · tone · delivery

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:piper` ← python3 -c "import piper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `app/public/js/10_studio.js:4112`

#### 7. قدرات قريبة في العائلة

- `VOICE-10` تحويل صوت إلى صوت / Speech-to-speech re-voice (key)
- `VOICE-11` Gemini TTS بثلاثين صوتًا / Gemini TTS with 30 prebuilt voices (key)
- `VOICE-13` حوار بأكثر من متكلم / Multi-speaker dialogue production (key)
- `VOICE-14` HeyGen Starfish بطوابع زمنية للكلمات / HeyGen Starfish TTS with word timestamps (key)

### `VOICE-13` — حوار بأكثر من متكلم / Multi-speaker dialogue production

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** من فكرة، تكتب نصًا قصيرًا بشخصيات، يُنطق كل سطر بصوت متكلمه ثم يُدمج في مسار حوار واحد. / From an idea you write a short multi-persona script; each line is voiced in its speaker's voice and mixed into one track.

**متى:** حين يريد المستخدم حوارًا بين أكثر من شخصية بصوت مختلف لكل متكلم في مسار واحد / when the user wants a multi-character dialogue with a distinct voice per speaker mixed into one track

**كيف:** fromIdea(): Claude JSON {title, logline, speakers[{name,voice,persona}], lines[{speaker,text,delivery,beat}]} with a hook within 2 s and an arc hook → build → peak → turn → resolve; Gemini may critique; per-line TTS from female pools (Kore, Zephyr, Leda, Aoede…) and male pools (Puck, Charon, Fenrir, Orus…); concatenated mix; then the smart montage runs.

**المعاملات:** hook ≤ 2 s; 5-beat arc; one voice per speaker locked for the whole piece

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حوار · متكلمون · بودكاست · dialogue · multi speaker · personas · شخصيات · أصوات متعددة · نص حواري · script · conversation

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `app/public/js/50_autoedit.js:1191`

#### 7. قدرات قريبة في العائلة

- `VOICE-11` Gemini TTS بثلاثين صوتًا / Gemini TTS with 30 prebuilt voices (key)
- `VOICE-12` إخراج أداء الصوت بواسطة Claude / Claude-directed voice performance (key)
- `VOICE-14` HeyGen Starfish بطوابع زمنية للكلمات / HeyGen Starfish TTS with word timestamps (key)
- `VOICE-15` محرك الصوت الموحد audio_meta.json / Unified audio engine (voice + words + BGM + SFX) (key)

### `VOICE-14` — HeyGen Starfish بطوابع زمنية للكلمات / HeyGen Starfish TTS with word timestamps

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مزود يعيد طوابع زمنية للكلمات داخل الاستجابة نفسها، فلا حاجة لتفريغ لاحق. / A provider that returns word timestamps in the response itself, so no post-transcription is needed.

**متى:** حين تريد صوتًا مولدًا يعود معه توقيت كل كلمة مباشرة دون تفريغ لاحق / when you want generated speech that returns per-word timestamps directly, with no post-transcription

**كيف:** node heygen-tts.mjs …; provider order in the vendor engine: HeyGen Starfish (timestamps) → ElevenLabs (none) → Kokoro-82M; Gemini as an explicit alternative. Speed is validated before any TTS runs (0, 5, −1 and text are refused). Ran here: 24/26 mocked tests pass (the 2 failures are bundled-SFX path tests, not TTS). Real calls need HEYGEN_ACCESS_TOKEN.

**المعاملات:** speed must be a positive number in range; docs narrator ref. 145–155 wpm, music bed ~−31 LUFS under it

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** طوابع الكلمات · هاي جن · heygen · starfish · word timestamps · توقيت الكلمات · تحويل نص لصوت · بدون تفريغ · tts · timestamps

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:kokoro` ← python3 -c "import kokoro" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `key:elevenlabs` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/media-use/audio/scripts/heygen-tts.mjs`
- `kosif-one/vendor/hyperframes/skills/media-use/audio/scripts/heygen-tts.test.mjs`
- `kosif-one/vendor/hyperframes/skills/media-use/audio/references/tts.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-12` إخراج أداء الصوت بواسطة Claude / Claude-directed voice performance (key)
- `VOICE-13` حوار بأكثر من متكلم / Multi-speaker dialogue production (key)
- `VOICE-15` محرك الصوت الموحد audio_meta.json / Unified audio engine (voice + words + BGM + SFX) (key)
- `VOICE-16` كتالوج Together للصوت / Together AI TTS catalog (key)

### `VOICE-15` — محرك الصوت الموحد audio_meta.json / Unified audio engine (voice + words + BGM + SFX)

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سكربت واحد يولد التعليق بتوقيت الكلمات والموسيقى والمؤثرات ويسجلها في audio_meta.json للمزامنة والترجمة. / One script generates narration with word timings, background music and SFX cues, recorded in audio_meta.json.

**متى:** حين تحتاج توليد التعليق بتوقيت الكلمات مع الموسيقى الخلفية والمؤثرات في ملف واحد للمزامنة والترجمة / when generating narration with word timings plus music and SFX cues in one manifest for sync

**كيف:** node audio.mjs --script SCRIPT.md --storyboard STORYBOARD.md --hyperframes . --out audio_meta.json --voice <id> (run in background); wait-bgm.mjs before render when BGM is still generating. The pattern (one manifest = master clock) is reusable with VOICE-01 + VOICE-32 locally; the script itself needs provider keys.

**المعاملات:** outputs: voice wav, bgm, sfx, audio_meta.json

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** محرك الصوت · بيان الصوت · audio engine · audio_meta · bgm · sfx · manifest · موسيقى خلفية · مؤثرات صوتية · مزامنة · word timings · narration

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/media-use/audio/scripts/audio.mjs`
- `kosif-one/vendor/hyperframes/skills/media-use/audio/scripts/audio.test.mjs`
- `kosif-one/vendor/hyperframes/skills/media-use/audio/scripts/wait-bgm.mjs`

#### 7. قدرات قريبة في العائلة

- `VOICE-13` حوار بأكثر من متكلم / Multi-speaker dialogue production (key)
- `VOICE-14` HeyGen Starfish بطوابع زمنية للكلمات / HeyGen Starfish TTS with word timestamps (key)
- `VOICE-16` كتالوج Together للصوت / Together AI TTS catalog (key)
- `VOICE-17` أوضاع مخرج الصوت الخارجي / KOSIF Voice Director provider modes (documented)

### `VOICE-16` — كتالوج Together للصوت / Together AI TTS catalog

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** واجهة مستضافة لـ Kokoro وOrpheus وCartesia Sonic عبر REST والبث وWebSocket. / Hosted TTS API for Kokoro, Orpheus and Cartesia Sonic over REST, streaming and WebSocket.

**متى:** حين تريد صوتًا مستضافًا من Kokoro أو Orpheus أو Cartesia Sonic عبر REST أو البث وتقارن الأسعار / when you want hosted Kokoro, Orpheus or Cartesia Sonic TTS over REST or streaming and compare prices

**كيف:** together>=2.0: client.audio.speech.create(model, input, voice, response_format) then write_to_file(). Key required.

**المعاملات:** Kokoro $4 / 1M chars · Orpheus $15 / 1M · Sonic-2 $65 / 1M

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** توغيذر · أسعار الصوت · together ai · orpheus · cartesia sonic · صوت مستضاف · بث الصوت · تحويل نص لصوت · streaming tts · websocket

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:kokoro` ← python3 -c "import kokoro" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/3214-togetherai-skills/13585-together-audio`
- `kosif-atlas/skills/3214-togetherai-skills/13585-together-audio/references/tts-models.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-14` HeyGen Starfish بطوابع زمنية للكلمات / HeyGen Starfish TTS with word timestamps (key)
- `VOICE-15` محرك الصوت الموحد audio_meta.json / Unified audio engine (voice + words + BGM + SFX) (key)
- `VOICE-17` أوضاع مخرج الصوت الخارجي / KOSIF Voice Director provider modes (documented)
- `VOICE-18` ميزانية الكلمات في الثانية / Words-per-second budget (documented)

### `VOICE-17` — أوضاع مخرج الصوت الخارجي / KOSIF Voice Director provider modes

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عقد لمزود خارجي: نص بالمشاعر، إكمال حلقة، سكربت مخرج، ووضع صوت (إخراج → اختيار أصوات → توليد) مع ذاكرة نطق وإعادة توليد دور واحد. / Contract for an external provider: Emotion Text, Full Episode Completion, Director Script, and Audio mode (direct → cast → render) with pronunciation memory and selective turn re-render.

**متى:** حين تعمل مع مزود صوت خارجي على حلقات وتريد ثبات الأصوات بينها وإعادة توليد دور واحد فقط / when working with an external voice provider on episodes, keeping casting stable and re-rendering one turn

**كيف:** Stable casting across episodes; re-render only the changed turn; report backend config errors verbatim; songs go to song generation, never to TTS.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مخرج الصوت · ذاكرة النطق · voice director · casting · re-render turn · حلقات · توزيع الأصوات · مشاعر · episodes · emotion text

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-source-router/references/providers/voice-director-v10.4.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-15` محرك الصوت الموحد audio_meta.json / Unified audio engine (voice + words + BGM + SFX) (key)
- `VOICE-16` كتالوج Together للصوت / Together AI TTS catalog (key)
- `VOICE-18` ميزانية الكلمات في الثانية / Words-per-second budget (documented)
- `VOICE-19` السرعة حسب المحتوى — أعد التوليد ولا تمطّ / Read speed by content — regenerate, never stretch (proven)

### `VOICE-18` — ميزانية الكلمات في الثانية / Words-per-second budget

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تحسب عدد الكلمات المسموح لكل مشهد من مدته قبل التوليد. / Computes the allowed word count per scene from its duration before any TTS.

**متى:** حين تكتب تعليقًا لمشهد بمدة محددة وتحتاج معرفة عدد الكلمات المناسب قبل التوليد / when writing narration for a fixed-length scene and you need the right word count before TTS

**كيف:** English narration 2.5 wps (15 s ≈ 37 words, 30 s ≈ 75, 60 s ≈ 150); direction spec 2.3–2.7 wps with total within ±5 % of target. By genre: ads 150–170 wpm, narration 130–150, meditation 100–120. Scene fill: 3–4 s → 8–12 words (~70 %), 5–6 s → 15–22 (~75 %), 7–8 s → 22–30 (~80 %). Arabic carries fewer words per second than English (longer words, more syllables) — budget ~15–20 % fewer words and measure with the real voice (the Piper test line ran at ~1.35 wps).

**المعاملات:** 2.3–2.7 wps; ±5 % total; ads 150–170 / narration 130–150 / meditation 100–120 wpm

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كلمات في الثانية · إيقاع التعليق · words per second · wpm · word budget · pacing · عدد الكلمات · طول النص · مدة المشهد · script length · word count

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:piper` ← python3 -c "import piper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/narration.md`
- `100-superskills/skills/voiceover-tts-direction/SKILL.md`
- `kosif-one/tools/kosif-omni/skills/kosif-audio/SKILL.md`
- `kosif-atlas/skills/166-demo-video/535-demo-video/references/scene-design-system.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-16` كتالوج Together للصوت / Together AI TTS catalog (key)
- `VOICE-17` أوضاع مخرج الصوت الخارجي / KOSIF Voice Director provider modes (documented)
- `VOICE-19` السرعة حسب المحتوى — أعد التوليد ولا تمطّ / Read speed by content — regenerate, never stretch (proven)
- `VOICE-20` نص النطق غير نص الشاشة / Spoken form vs on-screen form (documented)

### `VOICE-19` — السرعة حسب المحتوى — أعد التوليد ولا تمطّ / Read speed by content — regenerate, never stretch

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أبطئ للشرح الكثيف وأسرع قليلًا للخطّاف، بتغيير معامل السرعة في المحرك لا بمطّ الملف. / Slower for dense explanation, slightly faster for hooks — change the engine's speed, never time-stretch the file.

**متى:** حين يكون التعليق أسرع أو أبطأ من اللازم، فتعيد توليده بسرعة مختلفة بدل مط الملف / when narration is too fast or slow, so you regenerate at a new speed instead of stretching the audio

**كيف:** Speed 0.7–0.8 tutorial · 1.0 natural · 1.1–1.2 upbeat; avoid ≥1.5. Piper's knob is the inverse (length_scale 1.15 = slower). Ran here: same two Arabic sentences with --length-scale 1.15 --sentence-silence 0.35 → 7.13 s; re-generation keeps formants natural where atempo/rubberband stretching smears consonants.

**المعاملات:** speed 0.7–1.2 (avoid ≥1.5); Piper length_scale ≈ 1/speed

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سرعة الإلقاء · مط الصوت · speed · length scale · regenerate · no time-stretch · إبطاء الصوت · تسريع الصوت · سرعة التعليق · atempo · slow down

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:piper` ← python3 -c "import piper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `run here 2026-10-16: piper --length-scale 1.15 → 7.13 s`
- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/tts.md`
- `kosif-atlas/skills/1847-elevenlabs-pack/5514-elevenlabs-core-workflow-a`

#### 7. قدرات قريبة في العائلة

- `VOICE-17` أوضاع مخرج الصوت الخارجي / KOSIF Voice Director provider modes (documented)
- `VOICE-18` ميزانية الكلمات في الثانية / Words-per-second budget (documented)
- `VOICE-20` نص النطق غير نص الشاشة / Spoken form vs on-screen form (documented)
- `VOICE-21` قواعد كتابة التعليق للمشهد / Scene narration writing rules (documented)

### `VOICE-20` — نص النطق غير نص الشاشة / Spoken form vs on-screen form

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** المحرك يقرأ النطاقات والاختصارات والأرقام حرفيًا؛ اكتب الشكل المنطوق في التعليق واترك الإملاء الحقيقي على الشاشة. / TTS reads domains, acronyms and numbers literally; write the spoken form in narration and keep the real spelling on screen.

**متى:** حين يخطئ محرك الصوت في نطق الأرقام أو الاختصارات أو المواقع، فتكتب الشكل المنطوق وتترك الإملاء للشاشة / when TTS misreads numbers, acronyms or domains, so you write the spoken form and keep spelling on screen

**كيف:** Keep two files per scene: `say.txt` (to TTS) and `show.txt` (to captions). Pronunciation map per project: '.com' → 'دوت كوم', 'API' → 'إيه بي آي', '$1.9T' → 'قرابة تريليوني دولار', '٢٠٢٦' → 'ألفين وستة وعشرين'. Add tashkeel only on ambiguous words (عَلِم/عِلْم). Then align captions to the spoken words but display show.txt (ARAB captions family). (code snippet in references/powers/voice-tts.md)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نطق · تشكيل · أرقام منطوقة · pronunciation map · spoken form · tashkeel · acronyms · نطق خاطئ · الأرقام · اختصارات · mispronunciation · numbers

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2836-video-guide/11537-video-guide-creator/references/pronunciation.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/narration.md`
- `100-superskills/skills/voiceover-tts-direction/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-18` ميزانية الكلمات في الثانية / Words-per-second budget (documented)
- `VOICE-19` السرعة حسب المحتوى — أعد التوليد ولا تمطّ / Read speed by content — regenerate, never stretch (proven)
- `VOICE-21` قواعد كتابة التعليق للمشهد / Scene narration writing rules (documented)
- `VOICE-22` سكربت تعليق بوسوم أداء SSML / VO script with performance tags (SSML) (documented)

### `VOICE-21` — قواعد كتابة التعليق للمشهد / Scene narration writing rules

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فكرة واحدة لكل مشهد، ابدأ بالفعل، لا مصطلحات، تباين بعبارات قصيرة، وصف الحدث قبل ظهوره بلحظة. / One idea per scene, lead with the verb, no jargon, short contrast counts, describe an on-screen action just before it happens.

**متى:** حين تكتب نص التعليق لمشاهد فيديو وتريده قصيرًا واضحًا يسبق الحدث على الشاشة بلحظة / when writing scene narration that is short, clear and lands just before the on-screen action

**كيف:** If a sentence needs 'and' (و) it is two scenes. Contrast in counts: '24 تبويبًا. نقرة واحدة. 5 مجموعات.' Narrate an action ~0.3–0.5 s before it appears so the eye arrives with the ear. Strong first line (hook within 2 s). Each scene's narration in its own text file feeding TTS and caption timing. The script complements the visuals; it never reads the on-screen text aloud.

**المعاملات:** 1 idea / scene; action narrated 0.3–0.5 s early; hook ≤ 2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كتابة التعليق · فكرة واحدة · narration rules · one idea per scene · contrast lines · نص الفيديو · سكريبت · خطاف · hook · voiceover script

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/166-demo-video/535-demo-video/SKILL.md`
- `kosif-atlas/skills/2836-video-guide/11537-video-guide-creator/SKILL.md`
- `kosif-one/vendor/brag/skills/brag/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-19` السرعة حسب المحتوى — أعد التوليد ولا تمطّ / Read speed by content — regenerate, never stretch (proven)
- `VOICE-20` نص النطق غير نص الشاشة / Spoken form vs on-screen form (documented)
- `VOICE-22` سكربت تعليق بوسوم أداء SSML / VO script with performance tags (SSML) (documented)
- `VOICE-23` نص التعليق المقفل SCRIPT.md / Locked narration file (SCRIPT.md) (documented)

### `VOICE-22` — سكربت تعليق بوسوم أداء SSML / VO script with performance tags (SSML)

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سكربت منطوق: جمل قصيرة، أرقام وعملات وتواريخ كما تُقال، وسوم وقفة وتشديد وسرعة، ومواصفات صوت. / A spoken-style script with pauses, emphasis and rate tags plus a voice profile, for TTS or a human reader.

**متى:** حين تجهز سكربت تعليق منطوقًا فيه وقفات وتشديد وسرعة ومواصفات صوت لمحرك أو قارئ بشري / when preparing a spoken VO script with pause, emphasis and rate tags plus a voice profile

**كيف:** Write vo-script.md (profile: gender, age, tone, dialect, pace) + ssml.xml. Inline markup: [pause 0.5s], *emphasis*, (emotion). Map to engines: SSML <break time='500ms'/> and <prosody rate='-5%'> for Windows/Edge; sentence-silence and length_scale for Piper; voice_settings for ElevenLabs. After generation measure duration, level, peaks and mispronounced words.

**المعاملات:** duration within ±5 %; pauses 0.3–0.8 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ssml · وسوم الأداء · سكربت · vo script · pause tags · emphasis · وقفات · تشديد · معلق صوتي · voice profile · prosody

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:piper` ← python3 -c "import piper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `key:elevenlabs` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/voiceover-tts-direction/SKILL.md`
- `kosif-one/tools/kosif-omni/skills/kosif-audio/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-20` نص النطق غير نص الشاشة / Spoken form vs on-screen form (documented)
- `VOICE-21` قواعد كتابة التعليق للمشهد / Scene narration writing rules (documented)
- `VOICE-23` نص التعليق المقفل SCRIPT.md / Locked narration file (SCRIPT.md) (documented)
- `VOICE-24` توجيه الصوت باللهجات العربية / Arabic dialect voice-direction workflow (documented)

### `VOICE-23` — نص التعليق المقفل SCRIPT.md / Locked narration file (SCRIPT.md)

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ملف تعليق مقفل: ترويسة بالمزود والإعدادات والإخراج، ثم كتلة لكل سطر بالإطار ودليل الزمن وملاحظة الأداء والنص المنطوق. / A locked narration file: header with provider/settings/direction, then one block per line with frame, time guide, delivery note and spoken text.

**متى:** حين تريد تثبيت نص التعليق في ملف واحد بإعدادات المزود وملاحظة أداء لكل سطر / when locking narration in one file with provider settings and a delivery note per line

**كيف:** Blocks `## Line N — label (Frame N)` with Time guide, Delivery note and the indented spoken text fed to TTS. Real timing comes from TTS word timestamps (VOICE-32), never from the Time guide.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سكربت مقفل · script.md · locked script · delivery note · نص التعليق · ملاحظة الأداء · ملف السكربت · narration file · voiceover

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/hyperframes/references/script-format.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-21` قواعد كتابة التعليق للمشهد / Scene narration writing rules (documented)
- `VOICE-22` سكربت تعليق بوسوم أداء SSML / VO script with performance tags (SSML) (documented)
- `VOICE-24` توجيه الصوت باللهجات العربية / Arabic dialect voice-direction workflow (documented)
- `VOICE-25` اختيار اللغة واللهجة في المقابلة / Language & dialect intake field (ready)

### `VOICE-24` — توجيه الصوت باللهجات العربية / Arabic dialect voice-direction workflow

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خط نصي أولًا يجعل الصوت المولد طبيعيًا بالمصرية أو الفصحى أو السعودية أو الشامية أو المغربية أو الخليجية. / Text-first pipeline that makes TTS sound native in Egyptian, MSA, Saudi, Levantine, Moroccan or Gulf Arabic.

**متى:** حين يريد المستخدم تعليقًا مولدًا يبدو طبيعيًا بالمصرية أو السعودية أو الشامية أو المغربية أو الخليجية أو الفصحى / when TTS must sound native in Egyptian, Saudi, Levantine, Moroccan, Gulf Arabic or MSA

**كيف:** Brief → rewrite for the ear (short sentences, breath points) → pronunciation memory table (written → spoken; phonetic spelling fixes slang) → per-block direction (emotion, energy 1–5, pace, pauses, emphasis) → render only if a provider is exposed (preview first; no paid credits without approval) → measure (kosif_audio_analyze). Never mix dialects inside one block.

**المعاملات:** energy 1–5; one dialect per block

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** لهجات · مصري · خليجي · شامي · dialect · egyptian · gulf · msa · عامية · فصحى · سعودي · مغربي · levantine · saudi

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-voice/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-22` سكربت تعليق بوسوم أداء SSML / VO script with performance tags (SSML) (documented)
- `VOICE-23` نص التعليق المقفل SCRIPT.md / Locked narration file (SCRIPT.md) (documented)
- `VOICE-25` اختيار اللغة واللهجة في المقابلة / Language & dialect intake field (ready)
- `VOICE-26` شخصية اليوتيوبر المصري / Egyptian YouTuber voice persona (documented)

### `VOICE-25` — اختيار اللغة واللهجة في المقابلة / Language & dialect intake field

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الموجز يسجل لغة النص ولهجة الصوت (فصحى، مصري، سعودي، إنجليزي؛ الافتراضي ar-EG) ويمررها إلى STYLE.md. / The brief records on-screen language and voice dialect (fusha, Egyptian, Saudi, English; default ar-EG) and passes it to STYLE.md.

**متى:** عند بداية المشروع حين تسجل في الموجز لغة النص على الشاشة ولهجة الصوت لاختيار محرك الصوت / at project intake, recording on-screen language and voice dialect to choose the voice engine

**كيف:** brief.language in the fastify-motion-bro CLI; the voice engine and pronunciation map are then chosen from it (ar-SA → Piper/Naayf; ar-EG → Gemini persona VOICE-26).

**المعاملات:** default ar-EG

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** اللهجة · اللغة · مقابلة · intake · language · dialect · الموجز · فصحى · مصري · brief · voice engine

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:piper` ← python3 -c "import piper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `fastify-motion-bro/docs/QUESTIONS.md:6`
- `fastify-motion-bro/scripts/cli.mjs:14`

#### 7. قدرات قريبة في العائلة

- `VOICE-23` نص التعليق المقفل SCRIPT.md / Locked narration file (SCRIPT.md) (documented)
- `VOICE-24` توجيه الصوت باللهجات العربية / Arabic dialect voice-direction workflow (documented)
- `VOICE-26` شخصية اليوتيوبر المصري / Egyptian YouTuber voice persona (documented)
- `VOICE-27` صوت الراوي الوثائقي المقفل / Locked documentary narrator voice (proven)

### `VOICE-26` — شخصية اليوتيوبر المصري / Egyptian YouTuber voice persona

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** راوٍ مصري دافئ متحمس بقواعد نطق وأرقام مصرية دقيقة. / A warm, energetic Egyptian narrator persona with exact pronunciation and number rules.

**متى:** حين يريد المستخدم راويًا مصريًا دافئًا متحمسًا بأسلوب اليوتيوبرز بنطق وأرقام مصرية صحيحة / when the user wants a warm, energetic Egyptian YouTuber-style narrator with correct pronunciation and numbers

**كيف:** Fillers sparingly (يا جماعة، بصوا بقى، تمام؟، زي ما انتم شايفين); ج as hard g; ق as glottal stop; ث → s/t; ذ → z/d; natural breaths. Numbers: 11 حداشر, 12 اتناشر, 15 خمستاشر, 100 مية, 1000 ألف; جنيه = geneh. Gemini temperature ~0.85, top-p ~0.95.

**المعاملات:** ≤1 filler per 3 sentences; temperature 0.85; top-p 0.95

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مصري · يوتيوبر · عامية · egyptian persona · fillers · youtuber · راوي مصري · لهجة مصرية · تعليق حماسي · egyptian arabic · narrator

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-voice/SKILL.md`
- `app/public/js/10_studio.js:4112`

#### 7. قدرات قريبة في العائلة

- `VOICE-24` توجيه الصوت باللهجات العربية / Arabic dialect voice-direction workflow (documented)
- `VOICE-25` اختيار اللغة واللهجة في المقابلة / Language & dialect intake field (ready)
- `VOICE-27` صوت الراوي الوثائقي المقفل / Locked documentary narrator voice (proven)
- `VOICE-28` جمل صوت المدرب / Coach voice cue lines (proven)

### `VOICE-27` — صوت الراوي الوثائقي المقفل / Locked documentary narrator voice

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** وصف صوت ثابت في كل مقطع (راوٍ ذكوري عميق جاد بصدى بكرة فيلم قديمة) وجملة واحدة أقل من 20 كلمة لكل مقطع. / An identical voice description in every clip (deep, serious male narrator, slightly reverberant like an old film reel) and one sentence under 20 words per clip.

**متى:** حين تولد عدة مقاطع وثائقية وتريد صوت راوٍ عميق جاد ثابتًا لا يتغير بينها / when generating several documentary clips that must keep one deep, serious narrator voice without drift

**كيف:** VOICE constant + narrate(topic,i,n) truncated to 19 words, plus projector hum and paper snaps. Locking the description prevents voice drift between generated clips. Ran here: production-profiles test 10/10 pass, asserting <20 words and the VOICE string in every 10 s clip prompt.

**المعاملات:** < 20 words per 10 s clip; same voice string in every prompt

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** راوي وثائقي · فوكس · صوت مقفل · documentary narrator · vox · voice lock · وثائقي · صوت عميق · ثبات الصوت · documentary · clip prompts

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `fastify-motion-bro/scripts/profiles/vox-history.mjs:12`
- `fastify-motion-bro/tests/production-profiles.test.mjs:41`
- `run here 2026-10-16: node --test tests/production-profiles.test.mjs → 10/10`

#### 7. قدرات قريبة في العائلة

- `VOICE-25` اختيار اللغة واللهجة في المقابلة / Language & dialect intake field (ready)
- `VOICE-26` شخصية اليوتيوبر المصري / Egyptian YouTuber voice persona (documented)
- `VOICE-28` جمل صوت المدرب / Coach voice cue lines (proven)
- `VOICE-29` مواصفات تسجيل الصوت البشري / Human VO recording spec (documented)

### `VOICE-28` — جمل صوت المدرب / Coach voice cue lines

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جمل تدريب أمرية قصيرة منفصلة عن وصف اللقطة (تحكم في النزول، شد عضلات البطن). / Short imperative coaching lines kept separate from the shot description.

**متى:** حين تصنع فيديو تمارين وتحتاج جملًا تدريبية قصيرة تُقال مع كل حركة / when making a workout video that needs short coaching lines spoken with each rep

**كيف:** COACH array (5 generic) + per-muscle arrays for Abs, Chest, Back (15 lines); one cue per rep phase; keep them ≤ 6 words so they land inside a 2 s movement. Profile tests ran here (10/10).

**المعاملات:** 5 generic + 15 muscle-specific lines; ≤ 6 words each

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مدرب · لياقة · أوامر صوتية · coach cues · fitness · imperative · تمارين · جيم · رياضة · workout · exercise

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `fastify-motion-bro/scripts/profiles/fitness.mjs:16`
- `run here 2026-10-16: production-profiles tests 10/10`

#### 7. قدرات قريبة في العائلة

- `VOICE-26` شخصية اليوتيوبر المصري / Egyptian YouTuber voice persona (documented)
- `VOICE-27` صوت الراوي الوثائقي المقفل / Locked documentary narrator voice (proven)
- `VOICE-29` مواصفات تسجيل الصوت البشري / Human VO recording spec (documented)
- `VOICE-30` مدرب اللغة الثنائي / Language Coach (AR/EN) skill (documented)

### `VOICE-29` — مواصفات تسجيل الصوت البشري / Human VO recording spec

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مواصفات تسجيل المعلق البشري حتى يصل الملف صالحًا للمزامنة والمعالجة. / Recording spec for a human voice-over so the file arrives sync- and processing-ready.

**متى:** حين سيسجل معلق بشري صوته وتريد أن يصلك الملف صالحًا للمزامنة والمعالجة / when a human voice-over will be recorded and the file must arrive ready for sync and processing

**كيف:** Cardioid mic at 10–15 cm with a pop filter; peaks ≈ −12 dBFS; 48 kHz / 24-bit WAV; podcast noise floor < −60 dBFS; record room tone 5 s first (feeds afftdn). Then VOICE-39 cleanup, never re-timing.

**المعاملات:** 10–15 cm; peaks −12 dBFS; 48 kHz/24-bit; noise floor < −60 dBFS

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تسجيل · ميكروفون · recording spec · 48 khz · noise floor · تسجيل صوتي · معلق · مايك · voice over · mic setup

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-audio/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-27` صوت الراوي الوثائقي المقفل / Locked documentary narrator voice (proven)
- `VOICE-28` جمل صوت المدرب / Coach voice cue lines (proven)
- `VOICE-30` مدرب اللغة الثنائي / Language Coach (AR/EN) skill (documented)
- `VOICE-31` مدة المشهد = طول التعليق + هامش / Scene duration from voice length (proven)

### `VOICE-30` — مدرب اللغة الثنائي / Language Coach (AR/EN) skill

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مهارة المالك لتعلم اللغة بالممارسة؛ تفيد في كتابة تعليق ثنائي اللغة وترجمة سطر بسطر. / Owner skill for practice-based language learning; useful for bilingual narration and line-by-line translation.

**متى:** حين تكتب تعليقًا بلغتين أو تترجم النص سطرًا بسطر بين العربية والإنجليزية / when writing bilingual narration or translating a script line by line between Arabic and English

**كيف:** Load language-coach-arabic-english (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مدرب اللغة · ثنائي اللغة · language coach · bilingual · ترجمة · عربي إنجليزي · تعلم اللغة · translation · arabic english

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/language-coach-arabic-english/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-28` جمل صوت المدرب / Coach voice cue lines (proven)
- `VOICE-29` مواصفات تسجيل الصوت البشري / Human VO recording spec (documented)
- `VOICE-31` مدة المشهد = طول التعليق + هامش / Scene duration from voice length (proven)
- `VOICE-32` توقيت كلمات التعليق المولد بـ faster-whisper / Word timings from the generated voice (faster-whisper) (proven)

### `VOICE-31` — مدة المشهد = طول التعليق + هامش / Scene duration from voice length

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تولد التعليق أولًا ثم تقيس كل ملف وتحدد مدة المشهد منه بدل العكس. / Generate narration first, measure each file, and size every scene from it — never the reverse.

**متى:** حين تحدد مدد مشاهد الفيديو وتريدها مطابقة لطول التعليق المولد لا العكس / when sizing each scene's duration from its generated narration length rather than the reverse

**كيف:** Per scene: dur = ffprobe(vo_n) + 0.3–1.5 s buffer (1.5 s for demo scenes with UI to read). Remotion: calculateMetadata sums the scene durations; HTML: write the start times into the timeline JSON. Ran here: Arabic VO (loudnorm −14) muxed over a 1080x1920/30 fps plate of exactly ffprobe length → verify_video 11/11 PASS, delivered audio 7.430 s vs master 7.430 s. (code snippet in references/powers/voice-tts.md)

**المعاملات:** buffer 0.3–1.5 s; audio vs master ±50 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مدة المشهد · التعليق أولًا · auto duration · calculateMetadata · ffprobe · طول المشهد · مزامنة الصوت · توقيت المشاهد · remotion · scene timing

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `run here 2026-10-16: vo.mp4 verify_video 11/11, 7.430 vs 7.430 s`
- `kosif-tool/tools/verify_video.py`
- `kosif-atlas/skills/2712-remotion/10436-remotion-markup/voiceover.md`
- `kosif-atlas/skills/166-demo-video/535-demo-video/references/scene-design-system.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-29` مواصفات تسجيل الصوت البشري / Human VO recording spec (documented)
- `VOICE-30` مدرب اللغة الثنائي / Language Coach (AR/EN) skill (documented)
- `VOICE-32` توقيت كلمات التعليق المولد بـ faster-whisper / Word timings from the generated voice (faster-whisper) (proven)
- `VOICE-33` إعادة لصق النص المعروف على توقيت ويسبر / Re-attach the known script to Whisper timings (documented)

### `VOICE-32` — توقيت كلمات التعليق المولد بـ faster-whisper / Word timings from the generated voice (faster-whisper)

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تفرّغ الصوت المولد بطوابع زمنية لكل كلمة ثم تحوله إلى words.json لتتزامن الحركة والترجمة. / Transcribe the generated voice with per-word timestamps and convert to words.json so motion and captions sync.

**متى:** حين تريد مزامنة الحركة أو الترجمة مع كل كلمة في تعليق مولد فتحتاج توقيتها الدقيق / when you need per-word timings from a generated voice to sync motion and captions

**كيف:** pip install faster-whisper; resample to 16 kHz mono f32 and pass the numpy array (in this venv PyAV 19 rejects faster-whisper's open() kwargs, so do not pass a path); WhisperModel('small', device='cpu', compute_type='int8'), language='ar', word_timestamps=True; dump segments → `python3 kosif-tool/tools/words_convert.py ar.whisper.json words.json`. Ran in an earlier session's venv (2026-10-16; not installed in the current container, so install first): 10 words, 0.00 → 7.26 s. Lesson: Whisper split «محليًا» into «محل» + «ين» — always re-attach to the known script (VOICE-33). (code snippet in references/powers/voice-tts.md)

**المعاملات:** 16 kHz mono; model small int8 on CPU (large-v3 for final); key words ≤ 100 ms, others ≤ 150 ms

**التثبيت:** pip install faster-whisper

**الوسوم:** توقيت الكلمات · ويسبر · words.json · faster-whisper · word timestamps · alignment · تفريغ الصوت · مزامنة الترجمة · تزامن الحركة · transcription · subtitle sync

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:numpy` ← python3 -c "import numpy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `earlier session 2026-10-16 (venv; not installed in the current container, pip install faster-whisper): faster-whisper 1.2.1 small → words.json 10 words`
- `kosif-tool/playbooks/audio-sync.md:26`
- `kosif-tool/tools/words_convert.py`
- `100-superskills/skills/audio-reactive-captions-studio/references/captions-rules.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-30` مدرب اللغة الثنائي / Language Coach (AR/EN) skill (documented)
- `VOICE-31` مدة المشهد = طول التعليق + هامش / Scene duration from voice length (proven)
- `VOICE-33` إعادة لصق النص المعروف على توقيت ويسبر / Re-attach the known script to Whisper timings (documented)
- `VOICE-34` إيقاع يقوده التعليق / Voice-led pacing (seen)

### `VOICE-33` — إعادة لصق النص المعروف على توقيت ويسبر / Re-attach the known script to Whisper timings

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لأنك كتبت النص بنفسك، اعرض كلماتك أنت واستعمل من ويسبر التوقيت فقط. / Because you wrote the script, display your own words and take only the timing from Whisper.

**متى:** حين تعرف النص الأصلي وتريد عرض كلماتك أنت مع أخذ التوقيت فقط من تفريغ ويسبر / when you wrote the script and want to show your own words while taking only the timing from Whisper

**كيف:** Normalise both sides (strip tashkeel, unify أ/إ/آ → ا, ة → ه, ى → ي); walk script words and greedily consume Whisper tokens until the normalised concatenation matches (handles splits like محل+ين and merges); start = first token start, end = last token end. If drift persists use WhisperX forced alignment (pip install whisperx). Never edit timings by hand, only text.

**المعاملات:** match on normalised text; fall back to WhisperX

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** محاذاة · النص المعروف · forced alignment · whisperx · script alignment · أخطاء التفريغ · تصحيح الترجمة · مطابقة النص · whisper · transcript fix

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/audio-sync.md:26`
- `kosif-tool/tools/words_convert.py`

#### 7. قدرات قريبة في العائلة

- `VOICE-31` مدة المشهد = طول التعليق + هامش / Scene duration from voice length (proven)
- `VOICE-32` توقيت كلمات التعليق المولد بـ faster-whisper / Word timings from the generated voice (faster-whisper) (proven)
- `VOICE-34` إيقاع يقوده التعليق / Voice-led pacing (seen)
- `VOICE-35` قراءة صوتية بتظليل الكلمة المنطوقة / Read-aloud karaoke highlight (seen)

### `VOICE-34` — إيقاع يقوده التعليق / Voice-led pacing

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل فكرة بصرية تبقى بطول جملتها (~4–6 ث) مع حركات دقيقة مربوطة بالكلمات المفتاحية. / Each visual idea holds for its sentence (~4–6 s) with micro-animations tied to key words.

**متى:** حين تبني فيديو شرح يقوده التعليق وتريد بقاء كل فكرة بصرية بطول جملتها مع حركات على الكلمات المفتاحية / when building a narration-led explainer where each visual holds for its sentence with key-word micro-animations

**كيف:** Generate TTS first; one idea per sentence; key-word sync ≤ 100 ms; camera drifts during pauses so the frame never dies (pauses > 1.5 s need movement). Seen: the 60 s cream-paper explainer (~5 s per idea, static ratio ~0.65), the Fusha doodle parable (camera moves in pauses), a 457 s Chinese edge-tts Manim explainer (visuals step per sentence).

**المعاملات:** ~4–6 s per idea; key word ≤ 100 ms; pause > 1.5 s → ambient motion

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إيقاع التعليق · فكرة لكل جملة · voice-led · pacing · hold · فيديو شرح · كلمات مفتاحية · مزامنة · explainer · key words

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `style:pm-1stnoel-c20a89`
- `style:doodle`
- `style:pm-linearuncle-5d2bae`
- `kosif-tool/playbooks/audio-sync.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-32` توقيت كلمات التعليق المولد بـ faster-whisper / Word timings from the generated voice (faster-whisper) (proven)
- `VOICE-33` إعادة لصق النص المعروف على توقيت ويسبر / Re-attach the known script to Whisper timings (documented)
- `VOICE-35` قراءة صوتية بتظليل الكلمة المنطوقة / Read-aloud karaoke highlight (seen)
- `VOICE-36` ترجمة تُكتب على توقيت الصوت / Typewriter captions on voice word times (seen)

### `VOICE-35` — قراءة صوتية بتظليل الكلمة المنطوقة / Read-aloud karaoke highlight

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الجملة تبدأ رمادية وتتحول كل كلمة منطوقة إلى الحبر الداكن، والكلمة الحالية داخل صندوق تظليل. / The sentence starts grey, each spoken word turns to ink, and the current word sits in a highlight box.

**متى:** حين تريد نصًا على الشاشة تتلون كل كلمة فيه لحظة نطقها مع صندوق حول الكلمة الحالية / when you want on-screen text where each word inks in as spoken, with a box on the current word

**كيف:** From words.json: all words at ink #8a7b70 (or 25 % opacity ghosts as in the doodle reel), at word.start − 60 ms tween to #1f1b17 over 120 ms; a peach box #f6cf9a slides behind the current word (x/width tween 140 ms outBack). Arabic: whole words only, RTL container (ARAB-01). Doodle variant: key word recoloured orange with a wiggling squiggle underline.

**المعاملات:** lead 60 ms; 120 ms colour tween; ghosts 25 % opacity; box #f6cf9a on #f4eee0

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كاريوكي · تظليل الكلمة · read aloud · karaoke · word highlight · ترجمة كلمة بكلمة · إبراز الكلمة · قراءة مصاحبة · word by word · captions

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `style:pm-1stnoel-c20a89`
- `style:doodle`
- `kosif-tool/playbooks/audio-sync.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-33` إعادة لصق النص المعروف على توقيت ويسبر / Re-attach the known script to Whisper timings (documented)
- `VOICE-34` إيقاع يقوده التعليق / Voice-led pacing (seen)
- `VOICE-36` ترجمة تُكتب على توقيت الصوت / Typewriter captions on voice word times (seen)
- `VOICE-37` موجة الصوت ومؤشر التشغيل / Voice waveform with playhead (seen)

### `VOICE-36` — ترجمة تُكتب على توقيت الصوت / Typewriter captions on voice word times

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الكلمات تُكتب بمؤشر رفيع في اللحظة التي ينطقها الصوت، والكلمة المؤكدة بتدرج متوهج. / Words type in with a thin caret exactly as the voice speaks them; the emphasised word lands in a glowing gradient.

**متى:** حين تريد ترجمة تُكتب كلمة كلمة لحظة نطقها مع إبراز الكلمة المؤكدة بتدرج متوهج / when you want captions that type in word by word exactly as spoken, with the key word in a glowing gradient

**كيف:** Seen in a 22 s 1:1 launch film with an ElevenLabs VO over music ducked at the drop: captions typed at the voice word table inside a glass pill, no full stops, key word filled #f06aa8 → #8a6cf5 → #5d8cf7 with a faint glow, slow camera push 1.0 → 1.04 per scene. Build: per word, reveal at word.start, caret blink 530 ms; Arabic types per word not per letter.

**المعاملات:** reveal at word.start; caret blink 530 ms; push 1.0 → 1.04

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** آلة كاتبة · ترجمة متزامنة · typewriter captions · caret · launch film · كتابة النص · كلمة بكلمة · فيلم إطلاق · word sync · subtitles

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:elevenlabs` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `style:pm-rossaxbt-3085b7`

#### 7. قدرات قريبة في العائلة

- `VOICE-34` إيقاع يقوده التعليق / Voice-led pacing (seen)
- `VOICE-35` قراءة صوتية بتظليل الكلمة المنطوقة / Read-aloud karaoke highlight (seen)
- `VOICE-37` موجة الصوت ومؤشر التشغيل / Voice waveform with playhead (seen)
- `VOICE-38` محاضرة مروية: رسم يتقدم مع الجمل / Narrated lecture: draw-on paced to sentences (seen)

### `VOICE-37` — موجة الصوت ومؤشر التشغيل / Voice waveform with playhead

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رسم موجة الصوت مع رأس تشغيل يتقدم بينما الرسم التوضيحي يكتمل متزامنًا مع الكلام. / A drawn voice waveform with a progressing playhead while an illustration completes in sync with speech.

**متى:** حين تريد إظهار موجة الصوت على الشاشة ومؤشرًا يتقدم معها أثناء الكلام / when you want an on-screen voice waveform with a playhead advancing as the speech plays

**كيف:** Pre-compute peaks: `ffmpeg -i vo.wav -ac 1 -ar 100 -f f32le -` → 100 values/s → abs → bars 3 px wide / 2 px gap, height = peak × 60 px, rounded caps, played bars #3b69f3, unplayed #5c5c6f at 30 %; playhead x = t/dur × width. Seen in a 30 s SaaS explainer on #f8f5ec with a photosynthesis diagram synced to the waveform.

**المعاملات:** 100 peaks/s; bar 3 px + gap 2 px; #3b69f3 / #5c5c6f

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** موجة الصوت · رأس التشغيل · waveform · playhead · audio visual · شكل الموجة · تصور الصوت · مؤشر التشغيل · audio bars · peaks

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `style:pm-sudo-kiran-6609ed`

#### 7. قدرات قريبة في العائلة

- `VOICE-35` قراءة صوتية بتظليل الكلمة المنطوقة / Read-aloud karaoke highlight (seen)
- `VOICE-36` ترجمة تُكتب على توقيت الصوت / Typewriter captions on voice word times (seen)
- `VOICE-38` محاضرة مروية: رسم يتقدم مع الجمل / Narrated lecture: draw-on paced to sentences (seen)
- `VOICE-39` سلسلة تنظيف الصوت البشري / Voice clean-up chain (proven)

### `VOICE-38` — محاضرة مروية: رسم يتقدم مع الجمل / Narrated lecture: draw-on paced to sentences

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سبورة يرسم عليها قلم ظاهر عنصرًا تلو الآخر بسرعة التعليق، والترجمة تتبدل كل جملة تحت اللوح. / A whiteboard where a visible marker draws element after element at narration speed, subtitles swapping per sentence below the board.

**متى:** حين يريد المستخدم فيديو شرح على سبورة يرسم فيه قلم عنصرًا مع كل جملة من التعليق / when the user wants a whiteboard lesson where a marker draws one element per narrated sentence

**كيف:** Per narration sentence: one draw-on element (seconds per element = sentence length), marker icon rides the stroke tip and changes cap colour with ink (#1c1c1c, #c42d3f, #2b4a9b, #2f8a5b); eraser wipe between chapters; subtitles 1–2 centred lines. Seen in a 308 s lecture (static ratio 0.945 — narration carries it) and a bilingual-subtitle whiteboard walk-through.

**المعاملات:** 1 element per sentence; subtitle swap per sentence; eraser wipe between chapters

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** محاضرة · سبورة · رسم مع التعليق · lecture · whiteboard · draw-on · narration · درس · شرح تعليمي · فيديو تعليمي · explainer · marker

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `style:pm-tak3sh8-be5012`
- `style:pm-lemomo-ai-0d9cff`

#### 7. قدرات قريبة في العائلة

- `VOICE-36` ترجمة تُكتب على توقيت الصوت / Typewriter captions on voice word times (seen)
- `VOICE-37` موجة الصوت ومؤشر التشغيل / Voice waveform with playhead (seen)
- `VOICE-39` سلسلة تنظيف الصوت البشري / Voice clean-up chain (proven)
- `VOICE-40` وصفات إصلاح الصوت بالأعراض / Voice repair presets by symptom (documented)

### `VOICE-39` — سلسلة تنظيف الصوت البشري / Voice clean-up chain

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قطع الهدير، إزالة ضوضاء خفيفة، دفء وحضور بالمعادل، تخفيف الصفير، وضغط لطيف للمقاطع الناطقة. / High-pass, light denoise, warmth and presence EQ, de-ess and gentle compression for talking clips.

**متى:** حين يكون في تسجيل الكلام هدير أو ضوضاء أو صفير وتريد صوتًا أدفأ وأوضح / when a talking clip has rumble, noise or sibilance and needs a warmer, clearer voice

**كيف:** Owner chain in reel.py (identical in kosif-studio, kosif-one and kosif-montage-motion). Ran here on a test signal + loudnorm → −15.9 LUFS integrated, 48 kHz. (code snippet in references/powers/voice-tts.md)

**المعاملات:** HPF 70 Hz; afftdn nr 6 nf −42; +1.2 dB @220 Hz; +2.2 dB @3.2 kHz (w 1.4); −1 dB @9 kHz; deesser i 0.35; comp thr 0.12 ratio 2.5 att 10 ms rel 160 ms makeup 1.6

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تنظيف الصوت · معادل · ضغط · voice cleanup · eq · deesser · compressor · ffmpeg · إزالة الضوضاء · تحسين الصوت · صوت واضح · denoise · high-pass

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/reel.py:38`
- `kosif-one/tools/kosif-studio/motion/reel.py:38`
- `100-superskills/skills/kosif-montage-motion/scripts/reel.py:38`
- `run here 2026-10-16: chain + loudnorm → −15.9 LUFS`

#### 7. قدرات قريبة في العائلة

- `VOICE-37` موجة الصوت ومؤشر التشغيل / Voice waveform with playhead (seen)
- `VOICE-38` محاضرة مروية: رسم يتقدم مع الجمل / Narrated lecture: draw-on paced to sentences (seen)
- `VOICE-40` وصفات إصلاح الصوت بالأعراض / Voice repair presets by symptom (documented)
- `VOICE-41` أزياء صوتية للشخصيات / Character voice costumes (proven)

### `VOICE-40` — وصفات إصلاح الصوت بالأعراض / Voice repair presets by symptom

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تشخيص العرض أولًا ثم إصلاح واحد: الطنين، الطين، الصندوقية، الحدة، الوضوح. / Diagnose the symptom first, then one fix: rumble, mud, boxiness, harshness, clarity.

**متى:** حين يبدو الصوت فيه هدير أو كتمة أو صندوقية أو حدة أو ضعف وضوح وتريد تشخيص العرض وإصلاحه / when a voice sounds rumbly, muddy, boxy, harsh or unclear and you want to diagnose and fix that symptom

**كيف:** Vendor presets voice-clean (rumble → mud → even loudness → clarity → peak ceiling), voice-broadcast (+ boxiness, air, warmth), voice-warm (+ weight); singles rumble-cut, room-gate, boom-tame, harsh-tame. The HyperFrames fx-chain is not installable here, so apply the same numbers as ffmpeg `equalizer=f=…:t=q:w=Q:g=…`.

**المعاملات:** boom 200 Hz −4 dB Q1.4; mud 250 Hz −3 dB Q1.2; boxiness 400 Hz −3 dB Q1.4; clarity 3 kHz +2.5 dB Q1; harshness 3.2 kHz −3 dB Q1.6; rumble HPF 80 Hz

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إصلاح الصوت · طين · صندوقية · voice repair · mud · boxiness · harshness · صوت مكتوم · حدة الصوت · معادلة · equalizer · clarity

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/hyperframes-audio/references/presets.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-audio/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-38` محاضرة مروية: رسم يتقدم مع الجمل / Narrated lecture: draw-on paced to sentences (seen)
- `VOICE-39` سلسلة تنظيف الصوت البشري / Voice clean-up chain (proven)
- `VOICE-41` أزياء صوتية للشخصيات / Character voice costumes (proven)
- `VOICE-42` مختبر الصوت: عزل الصوت وفصل الموسيقى / Audiolab voice isolation & stem split (proven)

### `VOICE-41` — أزياء صوتية للشخصيات / Character voice costumes

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تلوين متعمد للصوت: هاتف، راديو AM، مكبر صوت، شريط قديم، نداء عام، إنتركم — واحد فقط في كل مرة. / Deliberate voice styling: telephone, AM radio, megaphone, lo-fi tape, PA system, intercom — never stack two.

**متى:** حين يراد أن يبدو صوت شخصية كأنه عبر هاتف أو راديو قديم أو مكبر صوت أو إنتركم / when a character's voice should sound like a telephone, AM radio, megaphone, lo-fi tape or intercom

**كيف:** Vendor names 7 presets (telephone, radio-am, megaphone, lofi-tape, pa-system, intercom, doofus-worble) for its fx-chain; the ffmpeg equivalents below rendered here on the Piper Arabic line (telephone 7.43 s, megaphone 7.47 s, room 7.57 s). (code snippet in references/powers/voice-tts.md)

**المعاملات:** telephone HPF 300 / LPF 3400 + comp 4:1; megaphone HPF 500 / LPF 4000 + acrusher 10-bit mix 0.25 + 40 ms slap; room aecho 60\|140 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هاتف · راديو · مكبر صوت · telephone voice · radio · megaphone · costume · مؤثر صوتي · صوت تليفون · صوت قديم · voice effect · intercom · lo-fi

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:piper` ← python3 -c "import piper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/hyperframes-audio/references/presets.md`
- `run here 2026-10-16: tel.wav / mega.wav / reverb.wav rendered`

#### 7. قدرات قريبة في العائلة

- `VOICE-39` سلسلة تنظيف الصوت البشري / Voice clean-up chain (proven)
- `VOICE-40` وصفات إصلاح الصوت بالأعراض / Voice repair presets by symptom (documented)
- `VOICE-42` مختبر الصوت: عزل الصوت وفصل الموسيقى / Audiolab voice isolation & stem split (proven)
- `VOICE-43` خفض الموسيقى تحت التعليق / Music ducking under the voice (proven)

### `VOICE-42` — مختبر الصوت: عزل الصوت وفصل الموسيقى / Audiolab voice isolation & stem split

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يعزل الكلام بـ RNNoise + إزالة ضوضاء FFT، أو يلغي الموسيقى من المركز، بخمسة أوضاع. / Isolates speech with RNNoise + FFT denoise, or centre-cancels music, in five modes.

**متى:** حين يريد المستخدم عزل الكلام عن الضوضاء أو حذف الموسيقى من خلفية مقطع / when the user wants to isolate speech from noise or remove the music behind a clip

**كيف:** `python scripts/kmotion.py audiolab FILE --mode voice\|music\|both\|novoice\|nomusic [--strong]`; centre-cancel works on stereo only; bass below 140 Hz restored after phase cancel. Measured speech/pause contrast 11.2 → 40.9 dB.

**المعاملات:** modes voice\|music\|both\|novoice\|nomusic; --strong; bass restore < 140 Hz; contrast 11.2 → 40.9 dB

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عزل الصوت · فصل الموسيقى · audiolab · rnnoise · stem split · denoise · إزالة الضوضاء · شيل المزيكا · تنقية الصوت · remove music · vocal isolation · noise reduction

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/audiolab.py`
- `100-superskills/skills/kosif-montage-motion/SKILL.md`
- `100-superskills/skills/kosif-montage-motion/references/operating-manual.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-40` وصفات إصلاح الصوت بالأعراض / Voice repair presets by symptom (documented)
- `VOICE-41` أزياء صوتية للشخصيات / Character voice costumes (proven)
- `VOICE-43` خفض الموسيقى تحت التعليق / Music ducking under the voice (proven)
- `VOICE-44` التسليم بجهارة −14 LUFS وفحص البوابة / −14 LUFS delivery + gate (proven)

### `VOICE-43` — خفض الموسيقى تحت التعليق / Music ducking under the voice

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الموسيقى تنخفض تلقائيًا كلما تكلم الصوت وتعود في الوقفات. / The music dips automatically whenever the voice speaks and returns in the pauses.

**متى:** حين يجب أن تنخفض موسيقى الخلفية تلقائيا أثناء التعليق الصوتي وتعود في الوقفات / when background music should dip automatically under the voiceover and come back in the pauses

**كيف:** Owner convention: mark `<audio data-role="voice">` and the mux ducks the other clips. Raw ffmpeg: sidechaincompress with the voice as key. Ran here: music bed 220 Hz −31.5 dB before the voice → −48.5 dB under it (≈ 17 dB duck), then loudnorm → −14.8 LUFS. For a gentler bed use ratio 4 (≈ −8 to −12 dB). (code snippet in references/powers/voice-tts.md)

**المعاملات:** threshold 0.03; ratio 4–8; attack 20 ms; release 400 ms; bed ~ −31 LUFS under VO

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خفض الموسيقى · داكينغ · ducking · sidechain · music bed · موسيقى خلفية · تعليق صوتي · وطي المزيكا · background music · voiceover mix

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/references/hyperframes-authoring.md`
- `kosif-one/tools/kosif-studio/motion/voice.py`
- `run here 2026-10-16: sidechaincompress −31.5 → −48.5 dB`

#### 7. قدرات قريبة في العائلة

- `VOICE-41` أزياء صوتية للشخصيات / Character voice costumes (proven)
- `VOICE-42` مختبر الصوت: عزل الصوت وفصل الموسيقى / Audiolab voice isolation & stem split (proven)
- `VOICE-44` التسليم بجهارة −14 LUFS وفحص البوابة / −14 LUFS delivery + gate (proven)
- `VOICE-45` وصل المقاطع كـ WAV لا MP3 / Join chunks as PCM, not MP3 copy (documented)

### `VOICE-44` — التسليم بجهارة −14 LUFS وفحص البوابة / −14 LUFS delivery + gate

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تسليم الصوت عند −14 LUFS وذروة حقيقية ≤ −1 dBFS، مع فحص آلي للطول والصيغة. / Deliver at −14 LUFS with true peak ≤ −1 dBFS, verified by an automatic gate.

**متى:** عند تسليم الصوت النهائي لفيديو أو بودكاست بجهارة قياسية مع فحص الذروة / when delivering final audio for a video or podcast at a standard loudness with a true-peak check

**كيف:** loudnorm=I=-14:TP=-1.5:LRA=11 (−16 for podcasts), 48 kHz stereo, AAC 192k, then `python3 kosif-tool/tools/verify_video.py film.mp4 --audio vo.wav --lufs -14`. Ran here: 11/11 PASS, −14.8 LUFS, TP −4.3 dBFS.

**المعاملات:** I −14 ±1.5 LUFS; TP ≤ −1 dBFS; ≥ 44.1 kHz; audio vs master ±50 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** جهارة · لوفس · بوابة التسليم · loudness · lufs · true peak · delivery gate · ضبط مستوى الصوت · تطبيع الصوت · علو الصوت · loudnorm · normalize audio · podcast

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/tools/verify_video.py`
- `run here 2026-10-16: verify_video 11/11 PASS`
- `kosif-studio/motion/references/hyperframes-authoring.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-42` مختبر الصوت: عزل الصوت وفصل الموسيقى / Audiolab voice isolation & stem split (proven)
- `VOICE-43` خفض الموسيقى تحت التعليق / Music ducking under the voice (proven)
- `VOICE-45` وصل المقاطع كـ WAV لا MP3 / Join chunks as PCM, not MP3 copy (documented)
- `VOICE-46` محادثة صوتية عربية لحظية عبر WebRTC / Realtime Arabic speech-to-speech (WebRTC) (key)

### `VOICE-45` — وصل المقاطع كـ WAV لا MP3 / Join chunks as PCM, not MP3 copy

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ضمّ قطع التعليق بعد فكها إلى WAV؛ نسخ MP3 مباشرة يضيف حشوًا يزيح توقيت الكلمات. / Concatenate narration chunks after decoding to WAV; MP3 stream-copy adds padding that drifts word timings.

**متى:** عند دمج عدة مقاطع تعليق صوتي في ملف واحد دون أن ينحرف توقيت الكلمات / when joining several narration chunks into one file without drifting word timings

**كيف:** Decode each chunk to 48 kHz PCM, concat with the concat filter (or concat demuxer on WAVs), then transcribe the JOINED file once — never add per-chunk transcripts with offsets.

**المعاملات:** MP3 encoder delay ≈ 1105 samples per chunk

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** وصل الصوت · انحراف التوقيت · concat · drift · pcm join · دمج الصوت · توقيت الكلمات · تعليق صوتي · merge audio · wav · narration

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/3323-joined-audio-transcript-drift/13837-joined-audio-transcript-drift`
- `kosif-atlas/skills/1847-elevenlabs-pack/5514-elevenlabs-core-workflow-a`

#### 7. قدرات قريبة في العائلة

- `VOICE-43` خفض الموسيقى تحت التعليق / Music ducking under the voice (proven)
- `VOICE-44` التسليم بجهارة −14 LUFS وفحص البوابة / −14 LUFS delivery + gate (proven)
- `VOICE-46` محادثة صوتية عربية لحظية عبر WebRTC / Realtime Arabic speech-to-speech (WebRTC) (key)
- `VOICE-47` مقاطعة المساعد بالكلام / Barge-in interruption (key)

### `VOICE-46` — محادثة صوتية عربية لحظية عبر WebRTC / Realtime Arabic speech-to-speech (WebRTC)

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** المتصفح يفتح اتصال WebRTC ويرسل عرض SDP إلى Worker يضيف المفتاح وإعدادات الجلسة، ثم صوت باتجاهين وقناة أحداث. / The browser opens WebRTC, posts its SDP offer to a Cloudflare Worker that adds the key and session config, then streams two-way audio with an events channel.

**متى:** حين يطلب المستخدم مساعدا صوتيا يتحاور بالعربية لحظيا داخل المتصفح / when building a browser voice assistant that talks back and forth in Arabic in real time

**كيف:** voice.js createVoiceAssistant().start(); worker POST /api/realtime/session → realtime calls with model gpt-realtime, input transcription gpt-4o-mini-transcribe (language ar), server_vad turn detection, output voice 'marin'; session.update injects file context (≤ 14000 chars); fallback = deterministic router VOICE-48. Needs OPENAI_API_KEY as a Worker secret.

**المعاملات:** Content-Type application/sdp; SDP ≤ 200000 bytes; data channel 'oai-events'; context ≤ 14000 chars

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مساعد صوتي · لحظي · realtime · webrtc · speech to speech · cloudflare worker · محادثة صوتية · دردشة صوتية · مساعد بالعربي · voice assistant · voice chat · openai

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:openai` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-audit-studio/voice.js:254`
- `kosif-audit-studio/cloudflare/realtime-worker.js`
- `kosif-earth-ci-fork/ui/audit/classic/voice.js`

#### 7. قدرات قريبة في العائلة

- `VOICE-44` التسليم بجهارة −14 LUFS وفحص البوابة / −14 LUFS delivery + gate (proven)
- `VOICE-45` وصل المقاطع كـ WAV لا MP3 / Join chunks as PCM, not MP3 copy (documented)
- `VOICE-47` مقاطعة المساعد بالكلام / Barge-in interruption (key)
- `VOICE-48` موجه نوايا صوتي عربي حتمي / Deterministic Arabic voice intent router (proven)

### `VOICE-47` — مقاطعة المساعد بالكلام / Barge-in interruption

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إذا تكلم المستخدم أثناء كلام المساعد، تنقلب الواجهة إلى الاستماع ويُلغى الرد. / If the user speaks while the assistant talks, the UI flips to listening and the response is cancelled.

**متى:** حين يجب أن يتوقف المساعد الصوتي عن الكلام فور أن يبدأ المستخدم بالحديث / when the voice assistant must stop talking as soon as the user starts speaking

**كيف:** On event input_audio_buffer.speech_started while state = speaking → emit 'interrupted'; interrupt() sends {type:'response.cancel'} over the data channel.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مقاطعة · barge-in · interrupt · response.cancel · إيقاف الرد · قطع الكلام · مساعد صوتي · stop speaking · voice assistant

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-audit-studio/voice.js:204`
- `kosif-audit-studio/voice.js:351`

#### 7. قدرات قريبة في العائلة

- `VOICE-45` وصل المقاطع كـ WAV لا MP3 / Join chunks as PCM, not MP3 copy (documented)
- `VOICE-46` محادثة صوتية عربية لحظية عبر WebRTC / Realtime Arabic speech-to-speech (WebRTC) (key)
- `VOICE-48` موجه نوايا صوتي عربي حتمي / Deterministic Arabic voice intent router (proven)
- `VOICE-49` كرة الصوت بحالاتها / Voice orb state animation (ready)

### `VOICE-48` — موجه نوايا صوتي عربي حتمي / Deterministic Arabic voice intent router

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** موجه قواعد يحول الكلام العربي المطبع إلى تنقل بين الشاشات وإجابات حالة، دون اختراع أرقام. / A rule router mapping normalised Arabic utterances to screen navigation and status answers, never inventing numbers.

**متى:** حين يراد تحويل أوامر صوتية عربية إلى تنقل بين الشاشات وإجابات حالة بقواعد ثابتة / when Arabic voice commands should navigate screens and answer status questions by fixed rules

**كيف:** routeIntent(transcript, context, api) with VIEW_WORDS (18 views) and has() keyword checks; unknown → guidance reply. Ran here: node --test tests/voice.test.js → 3/3 pass (navigation, status, unknown).

**المعاملات:** 18 view vocabularies; 3 tests

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نوايا · موجه · حتمي · intent router · deterministic · arabic commands · أوامر صوتية · تنقل بالصوت · قواعد ثابتة · voice commands · navigation · rule based

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-audit-studio/voice.js:45`
- `kosif-audit-studio/tests/voice.test.js`
- `run here 2026-10-16: voice.test.js 3/3`

#### 7. قدرات قريبة في العائلة

- `VOICE-46` محادثة صوتية عربية لحظية عبر WebRTC / Realtime Arabic speech-to-speech (WebRTC) (key)
- `VOICE-47` مقاطعة المساعد بالكلام / Barge-in interruption (key)
- `VOICE-49` كرة الصوت بحالاتها / Voice orb state animation (ready)
- `VOICE-50` نبض حلقة زر الميكروفون العائم / Live mic FAB ring pulse (ready)

### `VOICE-49` — كرة الصوت بحالاتها / Voice orb state animation

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كرة 44 بكسل تروي حالة الجلسة: خاملة بنفسجية، تستمع فيروزية بثلاث حلقات، تفكر بدوامة مخروطية، تتكلم بنبض تنفس. / A 44 px orb narrating the session: idle violet, listening teal with three rings, thinking conic swirl, speaking breathing pulse.

**متى:** حين تحتاج واجهة مساعد صوتي مؤشرا متحركا يوضح هل هو خامل أو يستمع أو يفكر أو يتكلم / when a voice UI needs an animated indicator for idle, listening, thinking and speaking

**كيف:** Set data-state on #voiceOrb (idle\|listening\|thinking\|speaking); keyframes orb-pulse, orb-spin, orb-breathe. (code snippet in references/powers/voice-tts.md)

**المعاملات:** idle radial at 35% 35% #c4b5fd → #6d28d9 60% → #1e1b4b; listening #99f6e4 → #0f766e → #042f2e + 8 px halo rgba(15,118,110,.18), rings 1.8 s ease-out scale .6 → 1.9 delays 0/.6/1.2 s; thinking conic #a78bfa,#6d28d9,#0f766e spin 1.2 s linear; speaking scale 1.1 breathe 1 s + 10 px halo

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كرة الصوت · حالات · voice orb · listening · speaking · css keyframes · مؤشر الحالة · أنيميشن · واجهة صوتية · status indicator · voice ui · animation

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-audit-studio/styles.css:823`
- `kosif-audit-studio/app.js:2049`

#### 7. قدرات قريبة في العائلة

- `VOICE-47` مقاطعة المساعد بالكلام / Barge-in interruption (key)
- `VOICE-48` موجه نوايا صوتي عربي حتمي / Deterministic Arabic voice intent router (proven)
- `VOICE-50` نبض حلقة زر الميكروفون العائم / Live mic FAB ring pulse (ready)
- `VOICE-51` التقاط ميكروفون نظيف / Clean mic capture constraints (ready)

### `VOICE-50` — نبض حلقة زر الميكروفون العائم / Live mic FAB ring pulse

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** زر ميكروفون عائم بتدرج يطلق حلقة متسعة طوال الجلسة الحية. / A floating gradient mic button that emits an expanding ring while the session is live.

**متى:** حين تريد زر ميكروفون عائما تخرج منه حلقة نابضة متسعة أثناء الجلسة الحية / when a floating mic button should emit an expanding pulse ring while the session is live

**كيف:** .voice-fab.live .voice-fab-ring { animation: voice-ring 1.6s ease-out infinite }.

**المعاملات:** FAB 60 px (KOSIF4 50 px); gradient 140deg #6d28d9 → #0f766e (KOSIF4 135deg #453556 → #395744); ring scale 1 → 1.7, opacity .8 → 0; hover −2 px, scale 1.03

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** زر الميكروفون · نبض · mic button · fab · pulse ring · زر عائم · مايك · تأثير نبض · floating button · microphone · css animation

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-audit-studio/styles.css:810`
- `kosif-audit-studio/studio.css:118`

#### 7. قدرات قريبة في العائلة

- `VOICE-48` موجه نوايا صوتي عربي حتمي / Deterministic Arabic voice intent router (proven)
- `VOICE-49` كرة الصوت بحالاتها / Voice orb state animation (ready)
- `VOICE-51` التقاط ميكروفون نظيف / Clean mic capture constraints (ready)
- `VOICE-52` تسجيل الصوت وتنزيله / MediaRecorder capture + download (ready)

### `VOICE-51` — التقاط ميكروفون نظيف / Clean mic capture constraints

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يُفتح الميكروفون بإلغاء الصدى وكبت الضوضاء والتحكم الآلي بالكسب. / The mic opens with echo cancellation, noise suppression and auto gain.

**متى:** عند فتح الميكروفون في المتصفح والحاجة إلى صوت نظيف بلا صدى أو ضوضاء / when opening the browser mic and needing clean input without echo or background noise

**كيف:** navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true, noiseSuppression:true, autoGainControl:true}}). For a VO take meant for the film, turn autoGainControl OFF (it pumps) and clean later with VOICE-39.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ميكروفون · إلغاء الصدى · getUserMedia · echo cancellation · noise suppression · كبت الضوضاء · مايك · تسجيل نظيف · auto gain · browser mic

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-audit-studio/voice.js:259`

#### 7. قدرات قريبة في العائلة

- `VOICE-49` كرة الصوت بحالاتها / Voice orb state animation (ready)
- `VOICE-50` نبض حلقة زر الميكروفون العائم / Live mic FAB ring pulse (ready)
- `VOICE-52` تسجيل الصوت وتنزيله / MediaRecorder capture + download (ready)
- `VOICE-53` لا تقليد لأصوات حقيقية / Never imitate real voices (documented)

### `VOICE-52` — تسجيل الصوت وتنزيله / MediaRecorder capture + download

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مساعد صغير يسجل MediaStream إلى Blob ويطلق تنزيل الملف. / A small helper that records a MediaStream into a Blob and triggers a file download.

**متى:** حين يريد المستخدم تسجيل صوت من المتصفح وحفظه كملف على جهازه / when the user wants to record audio in the browser and save it as a downloadable file

**كيف:** createAudioRecorder(stream) → {start, stop(): Promise<Blob>}; downloadAudioBlob(blob, 'kosif-response.webm') revokes the object URL after 1000 ms. Convert to WAV with ffmpeg before sync work.

**المعاملات:** default mime audio/webm; revoke delay 1000 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تسجيل · تنزيل · mediarecorder · webm · download · تسجيل صوت · حفظ الملف · تحميل · record audio · blob

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-audit-studio/audio-export.js`

#### 7. قدرات قريبة في العائلة

- `VOICE-50` نبض حلقة زر الميكروفون العائم / Live mic FAB ring pulse (ready)
- `VOICE-51` التقاط ميكروفون نظيف / Clean mic capture constraints (ready)
- `VOICE-53` لا تقليد لأصوات حقيقية / Never imitate real voices (documented)
- `VOICE-54` لا ادعاء بلا ملف / No audio claim without a receipt (documented)

### `VOICE-53` — لا تقليد لأصوات حقيقية / Never imitate real voices

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لا اسم شخص حقيقي ولا صوته ولا «بأسلوب فلان» في توليد الصوت أو الموسيقى؛ الاستنساخ بموافقة فقط، والإفصاح عن الصوت المصطنع حيث يلزم. / No real person's name, voice or 'in the style of' prompt for voice or music; clone only with consent; disclose synthetic voices where required.

**متى:** حين يطلب المستخدم صوتا أو موسيقى تشبه شخصا حقيقيا أو بأسلوب فنان معين / when a request asks for a real person's voice, a voice clone or music in the style of someone

**كيف:** Describe timbre in words instead (deep, warm, slightly raspy, mid-40s, measured). Keep the consent record next to any cloned voice id.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أخلاقيات · موافقة · تقليد · voice ethics · consent · impersonation · استنساخ الصوت · انتحال الشخصية · صوت مصطنع · voice clone · synthetic voice

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1511-homie/3892-music/references/RIGHTS.md`
- `kosif-one/tools/kosif-omni/skills/kosif-voice/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `VOICE-51` التقاط ميكروفون نظيف / Clean mic capture constraints (ready)
- `VOICE-52` تسجيل الصوت وتنزيله / MediaRecorder capture + download (ready)
- `VOICE-54` لا ادعاء بلا ملف / No audio claim without a receipt (documented)
- `VOICE-55` نظافة تكلفة الحروف / TTS character-cost hygiene (documented)

### `VOICE-54` — لا ادعاء بلا ملف / No audio claim without a receipt

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لا تقل إن الصوت وُلّد أو سُمع إلا ومعك ملف ومدة وجهارة مقاسة. / Never claim audio was rendered (or heard) without a file, a duration and a measured loudness.

**متى:** عند الإبلاغ بأن صوتا ولد أو سمع، مع ذكر ملفه ومدته وجهارته المقاسة / when reporting that audio was rendered or heard, backed by its file, duration and measured loudness

**كيف:** Report: path, ffprobe duration, integrated LUFS, true peak, and words.json count. Style observations that say 'not listened to' stay labelled that way.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إيصال · صدق · receipt · honesty · measured · تحقق · إثبات · تقرير الصوت · verification · ffprobe · audio report

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-voice/SKILL.md`
- `kosif-tool/tools/verify_video.py`

#### 7. قدرات قريبة في العائلة

- `VOICE-52` تسجيل الصوت وتنزيله / MediaRecorder capture + download (ready)
- `VOICE-53` لا تقليد لأصوات حقيقية / Never imitate real voices (documented)
- `VOICE-55` نظافة تكلفة الحروف / TTS character-cost hygiene (documented)

### `VOICE-55` — نظافة تكلفة الحروف / TTS character-cost hygiene

| الحقل | القيمة |
|---|---|
| العائلة | `voice-tts` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/voice-tts.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** انزع markdown وHTML وخزّن الأسطر المكررة قبل الدفع بالحرف. / Strip markdown/HTML and cache repeated lines before paying per character.

**متى:** عند تحويل نص إلى كلام بخدمة تحاسب بالحرف والرغبة في خفض التكلفة مع تكرار التجارب / when paying per character for text-to-speech and wanting to cut cost across repeated renders

**كيف:** Pre-clean text; cache key sha256(voice:model:settings:text); re-render only changed lines (the Voice Director's selective re-render follows the same idea).

**المعاملات:** saves 5–15 % characters; 80–95 % cache hits on iterations

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تكلفة · تخزين مؤقت · cost · cache · sha256 · توفير · تحويل النص لكلام · تنظيف النص · tts cost · text cleanup

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:VOICE-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `repo-transcribe-audio` · `tts-script`.
- مراحل النوع: قياس الملف (مدة، جهارة) ← معالجة على نسخة ← تفريغ أو مزامنة ← عينات استماع ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: التسجيل الأصلي محفوظ وأي معالجة على نسخة ← MD5 قبل وبعد
- جودة: الجهارة والذروة مقيسة ومبلغة ← ffmpeg ebur128
- جودة: توقيت الكلمات متسق مع الموجة ← عينات استماع عند 5 نقاط
- إلزامي: الآيات من المصحف لا من التفريغ ← مطابقة مع نص المصحف
- أمر الحكم في الوضع 1: `think.py qa audio --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1847-elevenlabs-pack/5516-elevenlabs-cost-tuning`
- `kosif-atlas/skills/1847-elevenlabs-pack/5522-elevenlabs-performance-tuning`

#### 7. قدرات قريبة في العائلة

- `VOICE-53` لا تقليد لأصوات حقيقية / Never imitate real voices (documented)
- `VOICE-54` لا ادعاء بلا ملف / No audio claim without a receipt (documented)

