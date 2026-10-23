# `atlas-media` — الصور والتحرير والتوليد (27 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/atlas-media.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/images.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`AMEDIA-01` تحويل نص لصوت واستنساخ وMؤثرات ElevenLabs](#amedia-01--تحويل-نص-لصوت-واستنساخ-وmؤثرات-elevenlabs--elevenlabs-tts-cloning-and-sound-effects)
- [`AMEDIA-02` فحص تسليم المزيج النهائي ليوتيوب 4K](#amedia-02--فحص-تسليم-المزيج-النهائي-ليوتيوب-4k--final-mix-delivery-check-for-youtube-4k)
- [`AMEDIA-03` مجموعات مؤثرات لعبة بمستويات صوت](#amedia-03--مجموعات-مؤثرات-لعبة-بمستويات-صوت--game-sfx-sets-with-loudness-classes)
- [`AMEDIA-04` تفريغ سحابي مع فصل المتحدثين والتوقيت](#amedia-04--تفريغ-سحابي-مع-فصل-المتحدثين-والتوقيت--hosted-stt-with-diarization-and-timestamps)
- [`AMEDIA-05` إصلاح انحراف التوقيت في دمج الصوت](#amedia-05--إصلاح-انحراف-التوقيت-في-دمج-الصوت--joined-audio-timestamp-drift-fix)
- [`AMEDIA-06` تفريغ محلي بـ whisper للملفات والبث](#amedia-06--تفريغ-محلي-بـ-whisper-للملفات-والبث--local-whisper-transcription-of-files-and-live-streams)
- [`AMEDIA-07` صياغة كلمات الأغاني وموجّهات Suno](#amedia-07--صياغة-كلمات-الأغاني-وموجّهات-suno--lyrics-and-suno-music-prompt-crafting)
- [`AMEDIA-08` صوت PipeWire داخل الحاويات](#amedia-08--صوت-pipewire-داخل-الحاويات--pipewire-audio-in-containers)
- [`AMEDIA-09` صوت ألعاب إجرائي بالكود](#amedia-09--صوت-ألعاب-إجرائي-بالكود--procedural-game-audio-from-python-code)
- [`AMEDIA-10` مقطوعة مُصنَّعة بحلقات متصلة](#amedia-10--مقطوعة-مُصنَّعة-بحلقات-متصلة--synthesized-score-with-seamless-loops)
- [`AMEDIA-11` اختيار طبقة ASR/TTS لوكيل صوتي](#amedia-11--اختيار-طبقة-asrtts-لوكيل-صوتي--voice-agent-asrtts-stack-selection)
- [`AMEDIA-12` توليد ومعايرة شرائط السبرايت](#amedia-12--توليد-ومعايرة-شرائط-السبرايت--anchored-sprite-strip-generation-and-normalization)
- [`AMEDIA-13` تريلر من لعب آلي حقيقي](#amedia-13--تريلر-من-لعب-آلي-حقيقي--gameplay-trailer-from-bot-playthroughs)
- [`AMEDIA-14` صورة شرح تعليمية أحادية اللون](#amedia-14--صورة-شرح-تعليمية-أحادية-اللون--monochrome-learning-explainer-image)
- [`AMEDIA-15` حركة نابضية وسطح زجاجي لمواقع بمستوى Awwwards](#amedia-15--حركة-نابضية-وسطح-زجاجي-لمواقع-بمستوى-awwwards--spring-physics-motion-and-a-layered-glass-surface)
- [`AMEDIA-16` نموذج الشيدر في React Three Fiber](#amedia-16--نموذج-الشيدر-في-react-three-fiber--glsl-shader-mental-model-in-react-three-fiber)
- [`AMEDIA-17` هيرو بخط حركي منفوخ تتصادم حروفه](#amedia-17--هيرو-بخط-حركي-منفوخ-تتصادم-حروفه--kinetic-inflated-typography-hero)
- [`AMEDIA-18` حقل حراري يلطّخه الإصبع (شيدر واحد)](#amedia-18--حقل-حراري-يلطّخه-الإصبع-شيدر-واحد--thermal-finger-trail-field-in-one-fragment-shader)
- [`AMEDIA-19` انتقالات العرض في React حسب ما تعنيه الحركة](#amedia-19--انتقالات-العرض-في-react-حسب-ما-تعنيه-الحركة--react-view-transitions-chosen-by-meaning)
- [`AMEDIA-20` حزمة تسليم من موجز إلى فيلم](#amedia-20--حزمة-تسليم-من-موجز-إلى-فيلم--brief-to-film-handoff-kit-with-a-named-upload-order)
- [`AMEDIA-21` فيديو عرض المنتج بأنماط احتياطية](#amedia-21--فيديو-عرض-المنتج-بأنماط-احتياطية--product-demo-video-pipeline-with-fallback-modes)
- [`AMEDIA-22` تشخيص FFmpeg: إطار متغير، HLS متعدد الدقات، فحص التيار](#amedia-22--تشخيص-ffmpeg-إطار-متغير-hls-متعدد-الدقات-فحص-التيار--ffmpeg-diagnostics-vfr-fix-aligned-abr-hls-stream-health)
- [`AMEDIA-23` قص بلا فقد على الإطارات المفتاحية](#amedia-23--قص-بلا-فقد-على-الإطارات-المفتاحية--lossless-keyframe-aligned-cutting-and-smart-cut)
- [`AMEDIA-24` مشهد After Effects بالسكربت: المواصفات أولاً](#amedia-24--مشهد-after-effects-بالسكربت-المواصفات-أولاً--scripted-after-effects-comps-spec-first-rigs-render-queue)
- [`AMEDIA-25` تغليف الفيديو: عنوان ونص مصغّرة لا يتكرران](#amedia-25--تغليف-الفيديو-عنوان-ونص-مصغّرة-لا-يتكرران--video-packaging-title-and-thumbnail-text-that-never-overlap)
- [`AMEDIA-26` Substance Painter: مساحة لون PBR وخبز الخرائط](#amedia-26--substance-painter-مساحة-لون-pbr-وخبز-الخرائط--substance-painter-pbr-colour-space-and-baking)
- [`AMEDIA-27` Godot 4: سكربت مُنمّط وفيزياء وتصدير بلا واجهة](#amedia-27--godot-4-سكربت-مُنمّط-وفيزياء-وتصدير-بلا-واجهة--godot-4-typed-gdscript-physics-timing-headless-export)

## البطاقات / cards

### `AMEDIA-01` — تحويل نص لصوت واستنساخ وMؤثرات ElevenLabs / ElevenLabs TTS, cloning and sound effects

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يولّد كلامًا بإعدادات صوت قابلة للضبط ويستنسخ الأصوات ويحوّل الصوت ويولّد مؤثرات. — Generate speech with tunable voice settings, clone voices from samples, and produce speech-to-speech, SFX and isolation.

**متى:** Building TTS, voice cloning, voice conversion, audio isolation or sound-effect generation on ElevenLabs.

**كيف:** 1) Install SDK and set API key via env. 2) textToSpeech.convert(voiceId, text, model eleven_multilingual_v2, voice_settings stability ~0.5, similarity ~0.75, style, speed 0.7-1.2) and pipe stream to file. 3) Instant clone from 30+ s of clean audio. 4) Use WebSocket streaming for chatbots. 5) Cut cost by model choice, caching repeated text and usage alerts; handle 429 with queue and backoff; verify webhook HMAC.

**المعاملات:** voice id, model, voice settings

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ElevenLabs · TTS · clone · استنساخ صوت

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:elevenlabs` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1847-elevenlabs-pack/5514-elevenlabs-core-workflow-a`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1847-elevenlabs-pack/5522-elevenlabs-performance-tuning`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-02` فحص تسليم المزيج النهائي ليوتيوب 4K / Final mix delivery check for YouTube 4K (documented)
- `AMEDIA-03` مجموعات مؤثرات لعبة بمستويات صوت / Game SFX sets with loudness classes (documented)

### `AMEDIA-02` — فحص تسليم المزيج النهائي ليوتيوب 4K / Final mix delivery check for YouTube 4K

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يصدّر ملف 4K ويتحقق من الدقة والإطارات والمدة والصوت وLUFS وذروة الصوت. — Render a 4K delivery file and verify resolution, fps, duration, AAC audio, LUFS and true peak with ffprobe and ebur128.

**متى:** Preparing a DaVinci Resolve mix for upload or any final render needing loudness QA.

**كيف:** 1) Duplicate timeline and keep original audio. 2) Render 3840x2160 H.264 (45 Mbps up to 30 fps, 68 at 60 fps) with AAC 48 kHz 320 kbps stereo. 3) ffprobe codec, size, fps, sample rate, channels, duration; frames within 1 of timeline. 4) ffmpeg -af ebur128=peak=true on the final file: target -14 LUFS +-1, true peak <= -1 dBTP. 5) On repeated failure stop and report; upload private by default.

**المعاملات:** loudness target

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** LUFS · render · تسليم · ffprobe

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1096-akbun-editvideo/2450-davinciresolve-audio-delivery`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-01` تحويل نص لصوت واستنساخ وMؤثرات ElevenLabs / ElevenLabs TTS, cloning and sound effects (documented)
- `AMEDIA-03` مجموعات مؤثرات لعبة بمستويات صوت / Game SFX sets with loudness classes (documented)
- `AMEDIA-04` تفريغ سحابي مع فصل المتحدثين والتوقيت / Hosted STT with diarization and timestamps (documented)

### `AMEDIA-03` — مجموعات مؤثرات لعبة بمستويات صوت / Game SFX sets with loudness classes

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0 / MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يولّد مجموعات مؤثرات بنسخ متعددة وفئات مستوى وتحذيرات للبدء المتأخر أو الترددات الضعيفة. — Render named effect sets with variants, level classes and warnings for late onset or inaudible lows.

**متى:** A game needs jump/coin/hit/win/UI sounds that sit together in a mix and play on phone speakers.

**كيف:** 1) Pick a kit (arcade, platformer, shooter, party, ui) or write a JSON spec of effect name, preset, pitch in semitones, length, seed, style (clean/retro/soft), level. 2) Render three variants for frequent sounds, one take for once-per-round signals. 3) Normalize by loudest 50 ms into classes ui -20, small -16, normal -12, big -9 dB, ceiling -1 dBFS. 4) Reject effects that start late or have little energy under about 300 Hz. 5) Review reel spectrogram image and warnings.

**المعاملات:** kit, style, variants

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** SFX · loudness · مؤثرات · مستويات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1511-homie/3901-sound`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1526-gamegen/4163-game-audio-procedural`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-01` تحويل نص لصوت واستنساخ وMؤثرات ElevenLabs / ElevenLabs TTS, cloning and sound effects (documented)
- `AMEDIA-02` فحص تسليم المزيج النهائي ليوتيوب 4K / Final mix delivery check for YouTube 4K (documented)
- `AMEDIA-04` تفريغ سحابي مع فصل المتحدثين والتوقيت / Hosted STT with diarization and timestamps (documented)
- `AMEDIA-05` إصلاح انحراف التوقيت في دمج الصوت / Joined-audio timestamp drift fix (documented)

### `AMEDIA-04` — تفريغ سحابي مع فصل المتحدثين والتوقيت / Hosted STT with diarization and timestamps

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يستدعي واجهة تفريغ سحابية للنسخ والترجمة وفصل المتحدثين وتوقيت الكلمات ضمن الحدود. — Call a hosted speech-to-text API for transcription, translation, speaker diarization and word timings within size limits.

**متى:** App needs batch or realtime transcription, captions or speaker segments via Together, Groq Whisper or ElevenLabs STT.

**كيف:** 1) Choose transport: REST batch, streaming, or realtime WebSocket (confirm PCM format first). 2) Respect batch limits: 80 MB direct upload, 1 GB URL fetch, 4 h per request; split longer audio. 3) Pass binary file handle in Python SDK. 4) Request verbose output for word timestamps or diarization and code for the richer response shape. 5) Use translations endpoint for English output.

**المعاملات:** model, response_format

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** STT · diarization · API · تفريغ · توقيت كلمات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pyannote` ← python3 -c "import pyannote" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3214-togetherai-skills/13585-together-audio`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1864-groq-pack/5867-groq-core-workflow-b`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-02` فحص تسليم المزيج النهائي ليوتيوب 4K / Final mix delivery check for YouTube 4K (documented)
- `AMEDIA-03` مجموعات مؤثرات لعبة بمستويات صوت / Game SFX sets with loudness classes (documented)
- `AMEDIA-05` إصلاح انحراف التوقيت في دمج الصوت / Joined-audio timestamp drift fix (documented)
- `AMEDIA-06` تفريغ محلي بـ whisper للملفات والبث / Local whisper transcription of files and live streams (documented)

### `AMEDIA-05` — إصلاح انحراف التوقيت في دمج الصوت / Joined-audio timestamp drift fix

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحافظ على تطابق توقيت النص والفصول بعد دمج مقاطع صوتية كثيرة. — Keep transcript, chapter and caption times aligned after concatenating many audio pieces.

**متى:** Subtitles drift later through a concatenated file, joined file longer than the sum of parts, ffmpeg non-monotonic dts warning, stitching TTS chunks.

**كيف:** 1) Diagnose: compare ffprobe sum of piece durations with joined duration. 2) Cause: copy-mode concat keeps each encoder's start/end padding and header frame (about 50 ms per join). 3) Frame-count arithmetic is still off, so do not rely on it. 4) Re-encode once at the end (or decode to PCM, concat, encode) so offsets are exact. 5) Verify by measuring the final file and checking last-chapter offset, never assume.

**المعاملات:** input file list, target codec

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ffmpeg · drift · concat · مزامنة · دمج صوت

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3323-joined-audio-transcript-drift/13837-joined-audio-transcript-drift`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-03` مجموعات مؤثرات لعبة بمستويات صوت / Game SFX sets with loudness classes (documented)
- `AMEDIA-04` تفريغ سحابي مع فصل المتحدثين والتوقيت / Hosted STT with diarization and timestamps (documented)
- `AMEDIA-06` تفريغ محلي بـ whisper للملفات والبث / Local whisper transcription of files and live streams (documented)
- `AMEDIA-07` صياغة كلمات الأغاني وموجّهات Suno / Lyrics and Suno music prompt crafting (documented)

### `AMEDIA-06` — تفريغ محلي بـ whisper للملفات والبث / Local whisper transcription of files and live streams

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يفرّغ الصوت أو الفيديو أو البث المباشر إلى نص بنموذج whisper محلي. — Transcribe audio, video or live streams to plain text with a local whisper model in batch or segmented live mode.

**متى:** Need a transcript of a podcast, interview, live stream or video audio track and no text source exists.

**كيف:** 1) Run an idempotent setup that ensures ffmpeg, yt-dlp/streamlink and a whisper runner. 2) Batch: pass file or URL (downloaded first with a time cap) and an output txt; read JSON with word count and a thin flag (under 1500 words). 3) Live: ffmpeg segments the stream into about 30 s chunks, each finished chunk is transcribed and appended to the output, stop on stream end, max minutes or Ctrl-C. 4) Run live mode in background and tail the file. Picture content is not read.

**المعاملات:** segment seconds, max minutes

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** whisper · transcribe · تفريغ · بث مباشر

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `yt-dlp` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/886-intel/1994-transcribe`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3214-togetherai-skills/13585-together-audio`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-04` تفريغ سحابي مع فصل المتحدثين والتوقيت / Hosted STT with diarization and timestamps (documented)
- `AMEDIA-05` إصلاح انحراف التوقيت في دمج الصوت / Joined-audio timestamp drift fix (documented)
- `AMEDIA-07` صياغة كلمات الأغاني وموجّهات Suno / Lyrics and Suno music prompt crafting (documented)
- `AMEDIA-08` صوت PipeWire داخل الحاويات / PipeWire audio in containers (documented)

### `AMEDIA-07` — صياغة كلمات الأغاني وموجّهات Suno / Lyrics and Suno music prompt crafting

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يبني بنية الأغنية ويكتب موجّهات Suno بكلمات موسومة أو خطة تأليف ElevenLabs. — Structure songs by section form and write Suno style prompts with tagged lyrics, or compose via ElevenLabs Music plans.

**متى:** Writing songs, themes or game scores and prompting AI music generators.

**كيف:** 1) Identify sections (verse, chorus, bridge, refrain) and form (AABA, verse/chorus, verse/refrain) with Pattison-style balance. 2) For Suno write a compact style prompt (genre, mood, instruments, tempo) plus lyrics with section tags. 3) Iterate with troubleshooting tips per genre. 4) For ElevenLabs Music build a composition plan for sung material via the creator's own account. 5) Keep a section list for later bar-aligned video cuts.

**المعاملات:** genre, mood, form

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Suno · lyrics · songwriting · كلمات أغاني

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:elevenlabs` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2475-songwriting/9606-song-form`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2475-songwriting/9607-suno`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1511-homie/3892-music`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-05` إصلاح انحراف التوقيت في دمج الصوت / Joined-audio timestamp drift fix (documented)
- `AMEDIA-06` تفريغ محلي بـ whisper للملفات والبث / Local whisper transcription of files and live streams (documented)
- `AMEDIA-08` صوت PipeWire داخل الحاويات / PipeWire audio in containers (documented)
- `AMEDIA-09` صوت ألعاب إجرائي بالكود / Procedural game audio from Python code (documented)

### `AMEDIA-08` — صوت PipeWire داخل الحاويات / PipeWire audio in containers

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تشغيل PipeWire مع WirePlumber وتوافق PulseAudio للصوت في الحاويات. — Run PipeWire with WirePlumber and PulseAudio compatibility for audio in containerized desktops.

**متى:** Audio missing or misrouted inside Docker or remote desktop sessions.

**كيف:** 1) Start pipewire, wireplumber and the pulse compatibility service in the session. 2) Confirm sockets in XDG_RUNTIME_DIR. 3) Point apps to the pulse socket. 4) List nodes and sinks to debug routing.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** PipeWire · Docker · صوت · حاويات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `docker` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2759-charly-selkies/10892-pipewire`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-06` تفريغ محلي بـ whisper للملفات والبث / Local whisper transcription of files and live streams (documented)
- `AMEDIA-07` صياغة كلمات الأغاني وموجّهات Suno / Lyrics and Suno music prompt crafting (documented)
- `AMEDIA-09` صوت ألعاب إجرائي بالكود / Procedural game audio from Python code (documented)
- `AMEDIA-10` مقطوعة مُصنَّعة بحلقات متصلة / Synthesized score with seamless loops (documented)

### `AMEDIA-09` — صوت ألعاب إجرائي بالكود / Procedural game audio from Python code

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يولّد مؤثرات وموسيقى قابلة للتكرار من كود بايثون ويصدّرها بصيغة OGG مع بيان. — Synthesize SFX and loop-ready music scores deterministically from seeds with numpy/scipy, exporting OGG plus manifest.

**متى:** Need license-clean original SFX, jingles, UI sounds or looping game music without samples or paid services.

**كيف:** 1) Write audio direction: cue table (id, mood, tempo, key, loop/one-shot) and SFX per game event. 2) Define a sonic identity (key, brightness, grit, space) in a shared style module. 3) Vendor the synth toolkit into the project tools dir. 4) Each SFX is a seeded function, each track a score; render via a build script writing OGG and manifest with SHA-256, duration, loop data. 5) Check objective metrics and spectrogram review images; cross-check EBU R128 with ffmpeg. Not suited to realistic acoustic instruments or vocals.

**المعاملات:** seed, key, tempo, cue list

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** synth · game audio · SFX · صوت إجرائي · ألعاب

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:numpy` ← python3 -c "import numpy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:scipy` ← python3 -c "import scipy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1526-gamegen/4163-game-audio-procedural`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1511-homie/3901-sound`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-07` صياغة كلمات الأغاني وموجّهات Suno / Lyrics and Suno music prompt crafting (documented)
- `AMEDIA-08` صوت PipeWire داخل الحاويات / PipeWire audio in containers (documented)
- `AMEDIA-10` مقطوعة مُصنَّعة بحلقات متصلة / Synthesized score with seamless loops (documented)
- `AMEDIA-11` اختيار طبقة ASR/TTS لوكيل صوتي / Voice-agent ASR/TTS stack selection (documented)

### `AMEDIA-10` — مقطوعة مُصنَّعة بحلقات متصلة / Synthesized score with seamless loops

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0 / MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يبني مقطوعة قصيرة من ملف JSON للأوتار والأنماط ويصدّر المزيج والسطور وحلقات بلا درز. — Build a short score from a JSON of chords and patterns and render mix, stems and seamless loop sections.

**متى:** Need a theme or looping bed with stems, bar grid for trailer cuts, or game music generated offline.

**كيف:** 1) Write score.json: tempo, key, instruments (level, pan, echo, reverb send, kick ducking), sections in whole bars with chords and per-instrument patterns, arrangement, loop sections. 2) Render mix at -14 LUFS (or -18 as a bed under effects) plus 24-bit master and per-instrument stems that sum to the mix. 3) Loops: render each section three times and keep the middle copy so reverb tails land at the loop head. 4) Check seam value (1 or less is seamless) and bar length; export plan.json bar grid for video cuts.

**المعاملات:** --loops, --lufs

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** loops · stems · music · حلقات · موسيقى

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1511-homie/3901-sound`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1526-gamegen/4163-game-audio-procedural`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-08` صوت PipeWire داخل الحاويات / PipeWire audio in containers (documented)
- `AMEDIA-09` صوت ألعاب إجرائي بالكود / Procedural game audio from Python code (documented)
- `AMEDIA-11` اختيار طبقة ASR/TTS لوكيل صوتي / Voice-agent ASR/TTS stack selection (documented)
- `AMEDIA-12` توليد ومعايرة شرائط السبرايت / Anchored sprite strip generation and normalization (documented)

### `AMEDIA-11` — اختيار طبقة ASR/TTS لوكيل صوتي / Voice-agent ASR/TTS stack selection

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يختار ويربط مزودي التعرف والتوليد الصوتي لوكيل صوتي حسب القناة واللغة والبث. — Choose and wire STT/TTS providers for a voice agent by channel bandwidth, language and streaming needs.

**متى:** Designing a phone or web voice agent, Twilio ConversationRelay, low-latency speech pipelines.

**كيف:** 1) Classify channel: narrowband telephony versus wideband web. 2) Pick provider by language coverage and streaming support. 3) Use bidirectional audio streaming (Twilio ConversationRelay handles ASR, TTS, barge-in). 4) Tune latency: model choice, streaming, caching, audio format. 5) Add rate-limit queues, health checks and rollback before production.

**المعاملات:** channel, languages

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** voice agent · Twilio · وكيل صوتي · ASR

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2261-conversational-ai-voice-engineering/8616-speech-recognition-and-synthesis`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2721-twilio-developer-kit/10514-twilio-voice-conversation-relay`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-09` صوت ألعاب إجرائي بالكود / Procedural game audio from Python code (documented)
- `AMEDIA-10` مقطوعة مُصنَّعة بحلقات متصلة / Synthesized score with seamless loops (documented)
- `AMEDIA-12` توليد ومعايرة شرائط السبرايت / Anchored sprite strip generation and normalization (documented)
- `AMEDIA-13` تريلر من لعب آلي حقيقي / Gameplay trailer from bot playthroughs (documented)

### `AMEDIA-12` — توليد ومعايرة شرائط السبرايت / Anchored sprite strip generation and normalization

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** توليد شريط حركة كامل من إطار معتمد ومعايرته بمقياس ومرساة موحدين. — Generate a whole animation strip from one approved seed and normalize to fixed frames with shared scale and anchor.

**متى:** 2D sprite animation or pixel-art sheets.

**كيف:** 1) Approved seed frame. 2) build_sprite_edit_canvas.py (slots, canvas). 3) One edit request for whole strip, with invariants. 4) normalize_sprite_strip.py: shared scale, bottom-center anchor. 5) Optionally lock frame 1. 6) render preview sheet.

**المعاملات:** frames,slot

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** sprite · pixel · سبرايت · بكسل

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2696-game-studio/10368-sprite-pipeline`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2460-pixel-art/9527-sprite`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-10` مقطوعة مُصنَّعة بحلقات متصلة / Synthesized score with seamless loops (documented)
- `AMEDIA-11` اختيار طبقة ASR/TTS لوكيل صوتي / Voice-agent ASR/TTS stack selection (documented)
- `AMEDIA-13` تريلر من لعب آلي حقيقي / Gameplay trailer from bot playthroughs (documented)
- `AMEDIA-14` صورة شرح تعليمية أحادية اللون / Monochrome learning explainer image (documented)

### `AMEDIA-13` — تريلر من لعب آلي حقيقي / Gameplay trailer from bot playthroughs

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تسجيل لعب آلي وقص على شبكة إيقاع بـ ffmpeg. — Record bot gameplay in Godot Movie Maker and cut on a beat-aligned grid with ffmpeg into 16:9, 9:16 and GIF.

**متى:** Promo trailer or devlog clip for a Godot game.

**كيف:** 1) Beat sheet approved. 2) BPM where bar = whole frames at 60fps (14400/BPM). 3) Render shots, cut by timeline.json. 4) Export 1080p60 H.264, -14 LUFS, vertical, GIF.

**المعاملات:** bpm

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** trailer · ffmpeg · تريلر · مونتاج

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1526-gamegen/4173-game-trailer`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-11` اختيار طبقة ASR/TTS لوكيل صوتي / Voice-agent ASR/TTS stack selection (documented)
- `AMEDIA-12` توليد ومعايرة شرائط السبرايت / Anchored sprite strip generation and normalization (documented)
- `AMEDIA-14` صورة شرح تعليمية أحادية اللون / Monochrome learning explainer image (documented)
- `AMEDIA-15` حركة نابضية وسطح زجاجي لمواقع بمستوى Awwwards / Spring-physics motion and a layered glass surface (documented)

### `AMEDIA-14` — صورة شرح تعليمية أحادية اللون / Monochrome learning explainer image

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحول الأوراق والأكواد إلى صور شرح 16:9 بسيطة بالأبيض والأسود. — Turn papers, code or concepts into minimal black-and-white 16:9 explainer images with sparse accent colour.

**متى:** Need study visuals for a paper, formula or process.

**كيف:** 1) White background, black/dark-gray titles, mid-gray notes. 2) Accent colour only where needed. 3) Pick layout: figure-centred, equation-centred, process or comparison. 4) Output 16:9.

**المعاملات:** layout

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** infographic · 16:9 · شرح · تصميم

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1094-akbun-draw/2418-akbun-draw-learning-mono`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-12` توليد ومعايرة شرائط السبرايت / Anchored sprite strip generation and normalization (documented)
- `AMEDIA-13` تريلر من لعب آلي حقيقي / Gameplay trailer from bot playthroughs (documented)
- `AMEDIA-15` حركة نابضية وسطح زجاجي لمواقع بمستوى Awwwards / Spring-physics motion and a layered glass surface (documented)
- `AMEDIA-16` نموذج الشيدر في React Three Fiber / GLSL shader mental model in React Three Fiber (documented)

### `AMEDIA-15` — حركة نابضية وسطح زجاجي لمواقع بمستوى Awwwards / Spring-physics motion and a layered glass surface

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحرّك العناصر بفيزياء النابض بدلاً من منحنيات المدة، ويبني السطح الزجاجي من أربع طبقات. — Animates with spring physics instead of duration curves and composes glass from four layers.

**متى:** حركة ناعمة، أنيميشن موقع فاخر، زجاج ضبابي / spring animation, premium web motion, glassmorphism

**كيف:** 1) Springs, not ease-in-out: slight overshoot (about 1.05x) then settle at 1.0, landing in 400-700 ms by travel distance (Framer Motion spring or GSAP; CSS only as fallback). 2) Glass stack bottom to top: backdrop blur 20-40 px (28 standard, 40 for modal), fill rgba(255,255,255,.05), 1 px inner border with a top-lit gradient, very soft wide ambient shadow. 3) Glass only on dark backgrounds, never with a solid fill. 4) Pair with noise, SDF and particle techniques for hero scenes.

**المعاملات:** overshoot 1.05; 400-700 ms; blur 28/40 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** spring · glass · زجاج · حركة · Framer Motion · GSAP

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:animejs` ← npm ls animejs أو وجود node_modules/animejs
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/95-awwwards-motion/204-awwwards-motion`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-13` تريلر من لعب آلي حقيقي / Gameplay trailer from bot playthroughs (documented)
- `AMEDIA-14` صورة شرح تعليمية أحادية اللون / Monochrome learning explainer image (documented)
- `AMEDIA-16` نموذج الشيدر في React Three Fiber / GLSL shader mental model in React Three Fiber (documented)
- `AMEDIA-17` هيرو بخط حركي منفوخ تتصادم حروفه / Kinetic inflated typography hero (documented)

### `AMEDIA-16` — نموذج الشيدر في React Three Fiber / GLSL shader mental model in React Three Fiber

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يشرح كيف تتكوّن المادة المخصصة من شيدر رؤوس وشيدر بكسلات، وكيف تمر البيانات عبر uniforms وvaryings. — Explains how a custom material is a vertex plus fragment program and how data flows through uniforms and varyings.

**متى:** شيدر، GLSL، تأثير ثلاثي الأبعاد على الويب / shader, GLSL, R3F custom material

**كيف:** 1) Mesh = geometry + material; a shader material replaces the material with two GPU programs: the vertex shader writes gl_Position per vertex, the fragment shader writes the colour per pixel. 2) Uniforms carry JS values (time, mouse, textures) identical for all vertices; memoize the uniforms object and update values in useFrame. 3) Varyings pass data (uv, normals) from vertex to fragment. 4) Attributes are per-vertex data available only in the vertex stage. 5) Build effects from noise (Perlin, simplex, curl, FBM), SDFs and render targets for multi-pass work.

**المعاملات:** uniforms, varyings

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** shader · GLSL · شيدر · three.js · R3F · WebGL

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/95-awwwards-motion/204-awwwards-motion`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-14` صورة شرح تعليمية أحادية اللون / Monochrome learning explainer image (documented)
- `AMEDIA-15` حركة نابضية وسطح زجاجي لمواقع بمستوى Awwwards / Spring-physics motion and a layered glass surface (documented)
- `AMEDIA-17` هيرو بخط حركي منفوخ تتصادم حروفه / Kinetic inflated typography hero (documented)
- `AMEDIA-18` حقل حراري يلطّخه الإصبع (شيدر واحد) / Thermal finger-trail field in one fragment shader (documented)

### `AMEDIA-17` — هيرو بخط حركي منفوخ تتصادم حروفه / Kinetic inflated typography hero

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يملأ الشاشة بحروف لينة منفوخة تتحرك وتتصادم وتتجنب النصوص والأزرار كعوائق، مع تأثير كلمة تختفي وتعود. — Fills the viewport with soft inflated letters that drift, collide and flow around copy and buttons as obstacles, with a disappearing-word effect.

**متى:** خط متحرك، تايبوغرافي حركي، هيرو تفاعلي / kinetic typography hero, physics letters

**كيف:** 1) Full-bleed 100svh section; translucent nav; one compact support-copy block near lower centre and two CTAs. 2) Letters occupy the whole canvas including edges; text and buttons are physics obstacles (Matter.js or similar). 3) Optional: deform real font outlines with opentype.js into soft bodies; SVG filters for goo and blur. 4) Invisible-word effect: per-letter stagger, defocus to blur, opacity toward zero, slight rotation or drift, short hold, refocus. 5) Pointer and scroll are optional forces; run requestAnimationFrame only for the physics loop. 6) Avoid the standard centred-headline-plus-screenshot hero.

**المعاملات:** stagger, blur, hold

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** kinetic typography · خط متحرك · Matter.js · hero · physics

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:matter` ← npm ls matter أو وجود node_modules/matter
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/100-ui-motion/209-kinetic-inflated-hero`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-15` حركة نابضية وسطح زجاجي لمواقع بمستوى Awwwards / Spring-physics motion and a layered glass surface (documented)
- `AMEDIA-16` نموذج الشيدر في React Three Fiber / GLSL shader mental model in React Three Fiber (documented)
- `AMEDIA-18` حقل حراري يلطّخه الإصبع (شيدر واحد) / Thermal finger-trail field in one fragment shader (documented)
- `AMEDIA-19` انتقالات العرض في React حسب ما تعنيه الحركة / React View Transitions chosen by meaning (documented)

### `AMEDIA-18` — حقل حراري يلطّخه الإصبع (شيدر واحد) / Thermal finger-trail field in one fragment shader

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** سطح يشبه كاميرا حرارية يسحب الإصبع ألوانه كطلاء مبلل ثم يعود، بشيدر واحد بلا قوام أو مخازن. — A heat-camera surface the pointer smears like wet paint that relaxes back, all in one fragment shader with no textures or buffers.

**متى:** تأثير حراري، تأثير لمس تفاعلي، شيدر يتبع الماوس / thermal effect, interactive smear shader, cursor trail

**كيف:** 1) Field: 5-octave fbm warps the coordinates, a second fbm warps them again. 2) A soft blob breathes via two low-frequency polar sines; heat 0-1, background 0.34-0.66, capped at 0.75. 3) Colour: thermal(heat) through seven smoothstep stops at 0, .12, .30, .45, .60, .78, 1 (teal, green, yellow, orange, red). 4) JS keeps the last 24 trail points with position, velocity and age; the field is sampled from where the finger came from, so colour drags along the path. 5) Defaults: smudge 9 (above ~14 tears), radius 0.17, follow 0.3 per frame, spacing 0.01, life 1.6 s; press ring expands for 0.9 s. 6) One focal object on dark ground, no text on top, cap DPR on weak phones.

**المعاملات:** smudge 9, radius .17, follow .3, 24 points

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** shader · thermal · حراري · WebGL · interactive · تفاعلي

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/100-ui-motion/211-thermal-finger-trail`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-16` نموذج الشيدر في React Three Fiber / GLSL shader mental model in React Three Fiber (documented)
- `AMEDIA-17` هيرو بخط حركي منفوخ تتصادم حروفه / Kinetic inflated typography hero (documented)
- `AMEDIA-19` انتقالات العرض في React حسب ما تعنيه الحركة / React View Transitions chosen by meaning (documented)
- `AMEDIA-20` حزمة تسليم من موجز إلى فيلم / Brief-to-film handoff kit with a named upload order (documented)

### `AMEDIA-19` — انتقالات العرض في React حسب ما تعنيه الحركة / React View Transitions chosen by meaning

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يختار نوع الانتقال بين الصفحات والعناصر حسب ما يريد أن يقوله للمستخدم: نفس العنصر، بيانات وصلت، ترتيب جديد… — Chooses page and element transitions by what they tell the user: same thing deeper, data arrived, new arrangement...

**متى:** انتقال بين الصفحات، أنيميشن تنقل، view transition / view transitions, page transition, shared element

**كيف:** 1) Priority: shared element (name) for going deeper; Suspense reveal for data loaded; per-item key for list reorder; enter/exit for appear/disappear; route-level last. 2) Hierarchical navigation uses typed nav-forward/nav-back; tabs use a plain fade or none; background refresh uses default none. 3) Next.js App Router already bundles the canary React that has ViewTransition, do not install react@canary there; elsewhere install canary react and react-dom. 4) Browser support Chromium 125+, Firefox 144+, Safari 18.2+, with graceful degradation.

**المعاملات:** transition type

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** view transitions · React · انتقالات · Next.js · animation

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2931-react/12175-vercel-react-view-transitions`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-17` هيرو بخط حركي منفوخ تتصادم حروفه / Kinetic inflated typography hero (documented)
- `AMEDIA-18` حقل حراري يلطّخه الإصبع (شيدر واحد) / Thermal finger-trail field in one fragment shader (documented)
- `AMEDIA-20` حزمة تسليم من موجز إلى فيلم / Brief-to-film handoff kit with a named upload order (documented)
- `AMEDIA-21` فيديو عرض المنتج بأنماط احتياطية / Product demo video pipeline with fallback modes (documented)

### `AMEDIA-20` — حزمة تسليم من موجز إلى فيلم / Brief-to-film handoff kit with a named upload order

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحوّل طلباً من سطر واحد إلى مجلد جاهز لمحرك الفيديو: موجز، ترتيب رفع، أصول، إطارات مرجعية، وبيان بالعيوب. — Turns a one-line ask into a folder ready for a video engine: brief, upload order, assets, reference frames and a manifest of known defects.

**متى:** تجهيز ملفات فيديو للمحرك، موجز فيلم، تسليم مشروع موشن / film brief kit, handoff folder for video generation

**كيف:** 1) Deliver PROMPT.md (one page in the engine's own vocabulary: scenes, cues, named easings), START-HERE.md (which files to upload, in which order, in one message), ATTACH/ (every asset), frames/ (reference stills whose filenames carry the instruction) and KIT.md (each file, pixel size, known defects). 2) Every prompt lists, in order: the brief, the transformation chain as match anchors (what becomes what), the asset list with real filenames, and the failure conditions for this specific film. 3) Name what is missing; never invent a substitute asset.

**المعاملات:** kit files

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** film brief · موجز · video · handoff · تسليم · motion

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2681-emulo/10272-video`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-18` حقل حراري يلطّخه الإصبع (شيدر واحد) / Thermal finger-trail field in one fragment shader (documented)
- `AMEDIA-19` انتقالات العرض في React حسب ما تعنيه الحركة / React View Transitions chosen by meaning (documented)
- `AMEDIA-21` فيديو عرض المنتج بأنماط احتياطية / Product demo video pipeline with fallback modes (documented)
- `AMEDIA-22` تشخيص FFmpeg: إطار متغير، HLS متعدد الدقات، فحص التيار / FFmpeg diagnostics: VFR fix, aligned ABR HLS, stream health (documented)

### `AMEDIA-21` — فيديو عرض المنتج بأنماط احتياطية / Product demo video pipeline with fallback modes

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يصنع فيديو عرض أو شرح منتج من مشاهد HTML ولقطات وتعليق صوتي، ويتحول لوضع يدوي إن غابت الأدوات. — Builds a product demo from HTML scenes, screenshots and narration, falling back to a manual mode when tools are missing.

**متى:** فيديو عرض منتج، ديمو، فيديو شرح تطبيق / product demo video, feature walkthrough, promo

**كيف:** 1) Probe the tools: browser automation for screenshots, a TTS engine, ffmpeg. 2) Full mode: HTML scene files -> screenshots -> narration audio -> ffmpeg composite; manual mode: write the scenes and give exact ffmpeg commands. 3) Pick a story structure (problem, solution, proof, call to action). 4) Terminal tools get dark monospace scenes with typed text; concepts get text-led scenes in the brand colours. 5) Size each scene to its narration length, then verify duration and audio.

**المعاملات:** scene count, voice

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** demo video · فيديو عرض · ffmpeg · TTS · walkthrough

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/166-demo-video/535-demo-video`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-19` انتقالات العرض في React حسب ما تعنيه الحركة / React View Transitions chosen by meaning (documented)
- `AMEDIA-20` حزمة تسليم من موجز إلى فيلم / Brief-to-film handoff kit with a named upload order (documented)
- `AMEDIA-22` تشخيص FFmpeg: إطار متغير، HLS متعدد الدقات، فحص التيار / FFmpeg diagnostics: VFR fix, aligned ABR HLS, stream health (documented)
- `AMEDIA-23` قص بلا فقد على الإطارات المفتاحية / Lossless keyframe-aligned cutting and smart cut (documented)

### `AMEDIA-22` — تشخيص FFmpeg: إطار متغير، HLS متعدد الدقات، فحص التيار / FFmpeg diagnostics: VFR fix, aligned ABR HLS, stream health

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يشخّص انزياح الصوت والصورة وأخطاء الطوابع الزمنية، ويبني بث HLS بعدة دقات بإطارات مفتاحية متوافقة. — Diagnoses A/V drift and timestamp errors and builds multi-rendition HLS with aligned keyframes.

**متى:** الصوت غير متزامن، تحويل فيديو، بث HLS / audio drift, VFR video, HLS ladder, ffprobe

**كيف:** 1) Inspect first: ffprobe -show_streams -of json; look for variable frame rate (screen and phone recordings), odd PTS/DTS, missing audio. 2) VFR drift: force constant frame rate (-vsync cfr / fps filter) before editing. 3) 'Non-monotonous DTS': remux with regenerated timestamps (-fflags +genpts). 4) ABR ladder: H.264 as the reach floor plus HEVC/AV1 for efficiency; renditions 1080/720/480 with identical GOP (-g 60 -keyint_min 60 -sc_threshold 0) so segments align. 5) 'Unknown encoder h264_nvenc' means the build or driver lacks NVENC; fall back to libx264.

**المعاملات:** GOP 60, renditions 1080/720/480

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ffmpeg · ffprobe · HLS · sync · تزامن · transcode

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/235-mas-video-lab/754-ffmpeg`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-20` حزمة تسليم من موجز إلى فيلم / Brief-to-film handoff kit with a named upload order (documented)
- `AMEDIA-21` فيديو عرض المنتج بأنماط احتياطية / Product demo video pipeline with fallback modes (documented)
- `AMEDIA-23` قص بلا فقد على الإطارات المفتاحية / Lossless keyframe-aligned cutting and smart cut (documented)
- `AMEDIA-24` مشهد After Effects بالسكربت: المواصفات أولاً / Scripted After Effects comps: spec first, rigs, render queue (documented)

### `AMEDIA-23` — قص بلا فقد على الإطارات المفتاحية / Lossless keyframe-aligned cutting and smart cut

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يقص الفيديو بنسخ التيار دون إعادة ترميز، ويتجنب الشاشة السوداء بالقص على إطارات I أو بإعادة ترميز الجزء الصغير فقط. — Cuts video by stream copy without re-encoding, avoiding black starts by cutting on I-frames or re-encoding only the partial GOP.

**متى:** قص فيديو بدون فقد جودة، شاشة سوداء بعد القص / lossless cut, keyframe cut, black frames after trim

**كيف:** 1) Black or frozen first seconds = the cut started on a P/B frame; snap the in-point to the previous keyframe or use smart cut (re-encode only from the chosen frame to the next I-frame). 2) Audio plays but video freezes after export: set avoid_negative_ts make_zero. 3) Keep secondary audio, subtitles and chapters by mapping all streams (-map 0). 4) Generate cut lists with millisecond segments as project files so the edit is reproducible.

**المعاملات:** cut points, streams

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** lossless · قص · keyframe · ffmpeg · trim

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/235-mas-video-lab/756-losslesscut`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-21` فيديو عرض المنتج بأنماط احتياطية / Product demo video pipeline with fallback modes (documented)
- `AMEDIA-22` تشخيص FFmpeg: إطار متغير، HLS متعدد الدقات، فحص التيار / FFmpeg diagnostics: VFR fix, aligned ABR HLS, stream health (documented)
- `AMEDIA-24` مشهد After Effects بالسكربت: المواصفات أولاً / Scripted After Effects comps: spec first, rigs, render queue (documented)
- `AMEDIA-25` تغليف الفيديو: عنوان ونص مصغّرة لا يتكرران / Video packaging: title and thumbnail text that never overlap (documented)

### `AMEDIA-24` — مشهد After Effects بالسكربت: المواصفات أولاً / Scripted After Effects comps: spec first, rigs, render queue

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ينشئ مشاهد After Effects بالسكربت بمواصفات محددة وأدوات تحكم قابلة لإعادة الاستخدام وطابور تصيير صريح. — Creates After Effects compositions by script with a fixed spec, reusable control rigs and an explicit render queue.

**متى:** سكربت أفتر إفكتس، قالب لوور ثيرد، أتمتة AE / After Effects script, lower third template, ExtendScript

**كيف:** 1) Define width, height, frame rate and duration before any layer. 2) Expressions for procedural or linked motion; keyframes for deliberate curves. 3) Build controller nulls and parent rigs instead of hard-coding layer indices. 4) Set the output module explicitly (format, path, post-render action) and catch missing template errors. 5) Use studio-licensed fonts and check substitution; test the script against the studio's AE major version.

**المعاملات:** comp spec

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** After Effects · ExtendScript · أفتر إفكتس · motion graphics · lower third

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/235-mas-video-lab/751-adobe-after-effects`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-22` تشخيص FFmpeg: إطار متغير، HLS متعدد الدقات، فحص التيار / FFmpeg diagnostics: VFR fix, aligned ABR HLS, stream health (documented)
- `AMEDIA-23` قص بلا فقد على الإطارات المفتاحية / Lossless keyframe-aligned cutting and smart cut (documented)
- `AMEDIA-25` تغليف الفيديو: عنوان ونص مصغّرة لا يتكرران / Video packaging: title and thumbnail text that never overlap (documented)
- `AMEDIA-26` Substance Painter: مساحة لون PBR وخبز الخرائط / Substance Painter PBR colour space and baking (documented)

### `AMEDIA-25` — تغليف الفيديو: عنوان ونص مصغّرة لا يتكرران / Video packaging: title and thumbnail text that never overlap

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يكتب عنوان الفيديو ونص الصورة المصغرة كزوج: العنوان يحمل الموضوع والكلمات المفتاحية، والمصغرة تحمل التوتر. — Writes title and thumbnail text as a pair: the title carries topic and keywords, the thumbnail carries the tension.

**متى:** عنوان يوتيوب، صورة مصغرة، ثمبنيل / YouTube title, thumbnail text, video packaging

**كيف:** 1) Tag intent: search (front-load the query phrase), browse (more intrigue, the thumbnail breaks the pattern), or both (package for search, thumbnail does browse). 2) Reject any pair where a thumbnail word repeats in the title. 3) Title ≤60 characters where possible; thumbnail text 1-3 words (4 is a caption). 4) Clarity beats curiosity; never promise more than the video delivers. 5) Thumbnail: one accent colour, high contrast, a real face with a readable expression when the format calls for it, nothing that does not earn its place. 6) Always give at least three pairs or three fixes.

**المعاملات:** title ≤60 chars; thumb 1-3 words

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** thumbnail · ثمبنيل · YouTube · يوتيوب · title · عنوان

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1520-digital-marketing-pro/4132-video-packaging`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3067-youtube/13228-creator-thumbnail-agent`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-23` قص بلا فقد على الإطارات المفتاحية / Lossless keyframe-aligned cutting and smart cut (documented)
- `AMEDIA-24` مشهد After Effects بالسكربت: المواصفات أولاً / Scripted After Effects comps: spec first, rigs, render queue (documented)
- `AMEDIA-26` Substance Painter: مساحة لون PBR وخبز الخرائط / Substance Painter PBR colour space and baking (documented)
- `AMEDIA-27` Godot 4: سكربت مُنمّط وفيزياء وتصدير بلا واجهة / Godot 4: typed GDScript, physics timing, headless export (documented)

### `AMEDIA-26` — Substance Painter: مساحة لون PBR وخبز الخرائط / Substance Painter PBR colour space and baking

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يضبط ترميز الألوان الصحيح لقنوات PBR ويحل مشكلات خبز خرائط النورمال ويؤتمت التصدير. — Sets the right colour encoding per PBR channel, fixes normal-map baking artefacts and automates export.

**متى:** خامات ثلاثية الأبعاد، نورمال ماب، تكستشر PBR / PBR textures, normal map baking, texture export

**كيف:** 1) sRGB for BaseColor and Emissive; linear for Normal, Roughness, Metallic, AO and Height. 2) Ray misses and seams: increase frontal/rear ray distance or use a cage; match low/high meshes by name suffix. 3) Long 4K/8K bakes crashing on Windows = GPU timeout (TDR); bake lower or raise the timeout. 4) Script projects, texture-set resolution, channel packing and batch export with the Python API; headless material builds with the Substance automation tools.

**المعاملات:** channel colour spaces

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** PBR · texture · خامات · Substance · normal map · 3D

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/228-mas-3d-games/709-substance-painter`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-24` مشهد After Effects بالسكربت: المواصفات أولاً / Scripted After Effects comps: spec first, rigs, render queue (documented)
- `AMEDIA-25` تغليف الفيديو: عنوان ونص مصغّرة لا يتكرران / Video packaging: title and thumbnail text that never overlap (documented)
- `AMEDIA-27` Godot 4: سكربت مُنمّط وفيزياء وتصدير بلا واجهة / Godot 4: typed GDScript, physics timing, headless export (documented)

### `AMEDIA-27` — Godot 4: سكربت مُنمّط وفيزياء وتصدير بلا واجهة / Godot 4: typed GDScript, physics timing, headless export

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-media` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-media.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يكتب ألعاب Godot بأنواع صريحة ويضع الحركة في حلقة الفيزياء ويصدّر للويب والمنصات من سطر الأوامر. — Writes Godot games with static types, keeps movement in the physics loop and exports to web and desktop from the CLI.

**متى:** لعبة Godot، تطوير لعبة، تصدير لعبة للويب / Godot game, game export, character controller

**كيف:** 1) Typed GDScript 2.0 (@export, @onready, Array[T]). 2) Move CharacterBody2D/3D in _physics_process; add coyote time and jump buffering; update the camera in the same step to avoid jitter. 3) Decouple with signals and an autoload event bus. 4) Export with godot --headless --export-release per platform in CI. 5) Blank web build = missing cross-origin isolation headers (COOP/COEP) needed for SharedArrayBuffer. 6) Similar engine notes exist in the Atlas for Bevy (ECS), Unity and Unreal.

**المعاملات:** export presets

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Godot · game · لعبة · GDScript · تطوير ألعاب

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:AMEDIA-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/228-mas-3d-games/707-godot`

#### 7. قدرات قريبة في العائلة

- `AMEDIA-25` تغليف الفيديو: عنوان ونص مصغّرة لا يتكرران / Video packaging: title and thumbnail text that never overlap (documented)
- `AMEDIA-26` Substance Painter: مساحة لون PBR وخبز الخرائط / Substance Painter PBR colour space and baking (documented)

