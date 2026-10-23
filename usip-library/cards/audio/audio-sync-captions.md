# `audio-sync-captions` — الصوت والموسيقى والتعليق (61 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/audio-sync-captions.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/audio.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`SYNC-01` الصوت هو الساعة الرئيسية](#sync-01--الصوت-هو-الساعة-الرئيسية--audio-is-the-master-clock)
- [`SYNC-02` ملف توقيت الكلمات kosif-words/1](#sync-02--ملف-توقيت-الكلمات-kosif-words1--wordsjson-master-timing-schema)
- [`SYNC-03` محوّل الترجمات والتفريغ إلى words.json](#sync-03--محوّل-الترجمات-والتفريغ-إلى-wordsjson--subtitletranscript--wordsjson-converter)
- [`SYNC-04` حدود تسامح التزامن](#sync-04--حدود-تسامح-التزامن--sync-tolerances)
- [`SYNC-05` قياس التزامن إطارًا بإطار](#sync-05--قياس-التزامن-إطارًا-بإطار--frame-by-frame-sync-probe)
- [`SYNC-06` التحقق من توقيت جاهز](#sync-06--التحقق-من-توقيت-جاهز--pre-timed-transcript-validation)
- [`SYNC-07` تفريغ عربي محلي بتوقيت الكلمات](#sync-07--تفريغ-عربي-محلي-بتوقيت-الكلمات--local-arabic-word-timed-transcription-faster-whisper)
- [`SYNC-08` فخ نماذج .en](#sync-08--فخ-نماذج-en--the-en-model-trap)
- [`SYNC-09` توقيت حقيقي من فونيمات Piper](#sync-09--توقيت-حقيقي-من-فونيمات-piper--true-word-timing-from-piper-phonemes)
- [`SYNC-10` محاذاة النص الصحيح على التفريغ](#sync-10--محاذاة-النص-الصحيح-على-التفريغ--true-text-alignment-onto-asr)
- [`SYNC-11` تصحيح الكلمات مع حفظ التوقيت](#sync-11--تصحيح-الكلمات-مع-حفظ-التوقيت--transcript-fixes-that-keep-timing)
- [`SYNC-12` ضبط بداية الكلمة على النطق](#sync-12--ضبط-بداية-الكلمة-على-النطق--onset-snapping-of-word-stamps)
- [`SYNC-13` تجهيز الصوت للتفريغ وفخ التوقيت](#sync-13--تجهيز-الصوت-للتفريغ-وفخ-التوقيت--stt-audio-prep--its-timing-trap)
- [`SYNC-14` تفريغ سحابي مع فصل المتحدثين](#sync-14--تفريغ-سحابي-مع-فصل-المتحدثين--cloud-stt-with-diarisation)
- [`SYNC-15` تفريغ HyperFrames](#sync-15--تفريغ-hyperframes--hyperframes-transcribe-cli)
- [`SYNC-16` كشف الإعادات وتجميع المونتاج من النص](#sync-16--كشف-الإعادات-وتجميع-المونتاج-من-النص--retake-detection--transcript-driven-assembly)
- [`SYNC-17` توزيع النص على مقاطع الصوت](#sync-17--توزيع-النص-على-مقاطع-الصوت--text-over-voiced-spans-estimated)
- [`SYNC-18` توقيت الكلمات حسب الطول](#sync-18--توقيت-الكلمات-حسب-الطول--word-timing-by-length)
- [`SYNC-19` ميزانية الكلمات حسب الزمن](#sync-19--ميزانية-الكلمات-حسب-الزمن--narration-word-budgets)
- [`SYNC-20` سكريبت بتوقيت مكتوب](#sync-20--سكريبت-بتوقيت-مكتوب--timestamped-script-parser)
- [`SYNC-21` تجميع الكلمات حسب الطاقة](#sync-21--تجميع-الكلمات-حسب-الطاقة--word-grouping-by-energy)
- [`SYNC-22` موضع آمن وضمان الاختفاء](#sync-22--موضع-آمن-وضمان-الاختفاء--safe-placement--exit-guarantee)
- [`SYNC-23` ستايل الترجمة حسب نبرة الكلام](#sync-23--ستايل-الترجمة-حسب-نبرة-الكلام--caption-style-by-tone)
- [`SYNC-24` وضوح الترجمة العربية](#sync-24--وضوح-الترجمة-العربية--arabic-caption-legibility)
- [`SYNC-25` لا تغيّر كلام المتحدث، والحرق عند الطلب](#sync-25--لا-تغيّر-كلام-المتحدث-والحرق-عند-الطلب--verbatim-words-burn-only-when-asked)
- [`SYNC-26` إبراز تلقائي للكلمات المهمة](#sync-26--إبراز-تلقائي-للكلمات-المهمة--automatic-emphasis-words)
- [`SYNC-27` كاريوكي ASS عربي بحدث لكل كلمة](#sync-27--كاريوكي-ass-عربي-بحدث-لكل-كلمة--arabic-ass-karaoke-one-event-per-word)
- [`SYNC-28` سبعة ستايلات ترجمة جاهزة](#sync-28--سبعة-ستايلات-ترجمة-جاهزة--seven-named-caption-styles)
- [`SYNC-29` صفحات ترجمة + SRT/VTT/ASS](#sync-29--صفحات-ترجمة--srtvttass--caption-pages--jsonsrtvttass)
- [`SYNC-30` معايرة حجم ASS](#sync-30--معايرة-حجم-ass--ass-playres-calibration)
- [`SYNC-31` كاريوكي \k بشرائح متساوية](#sync-31--كاريوكي-k-بشرائح-متساوية--even-slice-k-karaoke-omni)
- [`SYNC-32` دخول الكلمة على بداية نطقها](#sync-32--دخول-الكلمة-على-بداية-نطقها--word-enters-on-its-spoken-start)
- [`SYNC-33` تعبئة كاريوكي من اليمين بقناع كامل الكلمة](#sync-33--تعبئة-كاريوكي-من-اليمين-بقناع-كامل-الكلمة--rtl-karaoke-fill-with-whole-word-clip-path)
- [`SYNC-34` كاريوكي الكبسولة في starter الكانفس](#sync-34--كاريوكي-الكبسولة-في-starter-الكانفس--canvas-karaoke-pill-html-canvas-starter)
- [`SYNC-35` ترجمة Remotion بالكلمة مع كشف الاتجاه](#sync-35--ترجمة-remotion-بالكلمة-مع-كشف-الاتجاه--remotion-word-captions-with-bidi-detection)
- [`SYNC-36` كلمات على مقاطعها مع كلمات ذهبية](#sync-36--كلمات-على-مقاطعها-مع-كلمات-ذهبية--syllable-timed-speech-captions-with-gold-keywords)
- [`SYNC-37` سطر شبحي يضيء كلمة بكلمة](#sync-37--سطر-شبحي-يضيء-كلمة-بكلمة--ghost-to-lit-line)
- [`SYNC-38` صندوق ينتقل للكلمة النشطة](#sync-38--صندوق-ينتقل-للكلمة-النشطة--word-hop-highlight-box)
- [`SYNC-39` ترجمة تُكتب لحظة النطق](#sync-39--ترجمة-تُكتب-لحظة-النطق--voice-timed-typewriter-captions)
- [`SYNC-40` عداد كلمة مفتاحية ودائرة على الكلمة](#sync-40--عداد-كلمة-مفتاحية-ودائرة-على-الكلمة--keyword-counter--on-word-annotations)
- [`SYNC-41` مكوّنات ترجمة HyperFrames](#sync-41--مكوّنات-ترجمة-hyperframes--hyperframes-caption-components)
- [`SYNC-42` ترجمة مدمجة: شريط وكلمة ذروة خلف المتحدث](#sync-42--ترجمة-مدمجة-شريط-وكلمة-ذروة-خلف-المتحدث--embedded-captions-rail--peak-word-behind-the-subject)
- [`SYNC-43` الأشرطة السفلية](#sync-43--الأشرطة-السفلية--lower-thirds)
- [`SYNC-44` ستايلات وحركات ترجمة بصمة](#sync-44--ستايلات-وحركات-ترجمة-بصمة--basma-caption-presets-animations--highlight-modes)
- [`SYNC-45` فيلم كلمات من صوت (أغنية، شعر، دعاء)](#sync-45--فيلم-كلمات-من-صوت-أغنية-شعر-دعاء--verse-film-from-sound)
- [`SYNC-46` Voice2Motion: موشن بالمعنى من الصوت](#sync-46--voice2motion-موشن-بالمعنى-من-الصوت--voice2motion-semantic-scenes)
- [`SYNC-47` إخراج تلقائي لمقطع متكلم](#sync-47--إخراج-تلقائي-لمقطع-متكلم--editor-style-auto-direction-of-a-talking-clip)
- [`SYNC-48` الريل التلقائي من الكلام](#sync-48--الريل-التلقائي-من-الكلام--automatic-talking-clip-reel)
- [`SYNC-49` إيقاع التلاوة والدعاء](#sync-49--إيقاع-التلاوة-والدعاء--recitation--dua-pacing)
- [`SYNC-50` توقيت سطر الأغنية](#sync-50--توقيت-سطر-الأغنية--lyric-line-timing)
- [`SYNC-51` ريل كلمات أغنية](#sync-51--ريل-كلمات-أغنية--songreel-lyric-reel)
- [`SYNC-52` لكل جملة منطوقة دليل بصري](#sync-52--لكل-جملة-منطوقة-دليل-بصري--one-visual-proof-per-spoken-claim)
- [`SYNC-53` كشف الصمت الثابت والتكيفي](#sync-53--كشف-الصمت-الثابت-والتكيفي--fixed--adaptive-silence-detection)
- [`SYNC-54` إصلاح انزياح الصوت المدموج](#sync-54--إصلاح-انزياح-الصوت-المدموج--joined-audio-drift-fix)
- [`SYNC-55` ذروة المؤثر على الحدث](#sync-55--ذروة-المؤثر-على-الحدث--sfx-peak-offset-alignment)
- [`SYNC-56` دمج المشاهد مع الصوت الأصلي بلا تعديل](#sync-56--دمج-المشاهد-مع-الصوت-الأصلي-بلا-تعديل--concat--untouched-original-audio-mux)
- [`SYNC-57` غلاف الجهارة وقنوات الصوت للحركة](#sync-57--غلاف-الجهارة-وقنوات-الصوت-للحركة--loudness-envelope--sound-channels-for-motion)
- [`SYNC-58` مزامنة الفم بستة أشكال](#sync-58--مزامنة-الفم-بستة-أشكال--six-shape-lip-sync)
- [`SYNC-U01` وسم مصدر التوقيت: عرض أم صوت أم تقديري](#sync-u01--وسم-مصدر-التوقيت-عرض-أم-صوت-أم-تقديري--timing-provenance-labels-display--voice--estimated)
- [`SYNC-X01` تحليل أغنية لفيلم كلمات](#sync-x01--تحليل-أغنية-لفيلم-كلمات--song-analysis-for-a-lyric-film-bands-kicks-word-times)
- [`SYNC-X02` قفل موضع مقطع الترجمة](#sync-x02--قفل-موضع-مقطع-الترجمة--caption-chunk-position-lock)

## البطاقات / cards

### `SYNC-01` — الصوت هو الساعة الرئيسية / Audio is the master clock

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صوت المستخدم لا يُعاد أخذ عيناته ولا يُمط ولا يُعاد توقيته؛ الصورة تتبع الصوت ومدة الفيلم = مدة الصوت مقربة لإطار. / The user's audio is never resampled, stretched or retimed; picture follows sound and film length = audio length rounded to frames.

**متى:** عند ضبط مدة الفيلم على صوت المستخدم دون مطه أو إعادة توقيته / when film length must follow the user's audio exactly, without stretching or resampling it

**كيف:** durationInFrames = ceil(audioSeconds × fps) from ffprobe -v error -show_entries format=duration -of csv=p=0 voice.mp3. Mux with node tools/render_html.cjs --audio voice.wav (apad/-shortest; the stream is copied, not re-timed) or Remotion <Audio> at frame 0 with calculateMetadata/getAudioDurationInSeconds. Loudness changes go on a separate delivery copy only. Proven in both proof films: audio 11.500 s vs master 11.500 s, 13/13 checks.

**المعاملات:** duration = ceil(sec × fps)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** الصوت ساعة · master clock · untouched audio · duration · ffprobe · مدة الفيديو · حفظ الصوت · تركيب الصوت · audio length · mux audio

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-tool/playbooks/audio-sync.md:15-16`
- `kosif-tool/tools/render_html.cjs:373`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`
- `kosif-tool/starters/remotion/src/Film.tsx:32`

#### 7. قدرات قريبة في العائلة

- `SYNC-02` ملف توقيت الكلمات kosif-words/1 / words.json master timing schema (proven)
- `SYNC-03` محوّل الترجمات والتفريغ إلى words.json / Subtitle/transcript → words.json converter (proven)

### `SYNC-02` — ملف توقيت الكلمات kosif-words/1 / words.json master timing schema

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ملف واحد [{word,start,end}] بالثواني، مرتب بلا تداخل، مع emphasis وscene اختياريين واللغة والاتجاه ومدة الصوت. / One sorted, non-overlapping [{word,start,end}] file in seconds, with optional emphasis/scene plus language, direction and audio duration.

**متى:** عند تجهيز ملف توقيت الكلمات الرئيسي الذي يقود الحركة في الفيلم / when preparing the master word-timing file (word, start, end) that drives the film

**كيف:** Scaffold copies templates/words.example.json to words.json; for file:// pages emit words.js (window.KOSIF_WORDS) with tools/words_convert.py words.json words.js. Both proof films are driven from words.json/words.js.

**المعاملات:** fields word/start/end (+emphasis, scene); seconds, ms precision

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** words.json · توقيت الكلمات · timing file · KOSIF_WORDS · مزامنة الكلمات · توقيت النص · تزامن · word timestamps · timing schema

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-tool/templates/words.example.json`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/words.json`
- `kosif-tool/starters/html-canvas/words.js`

#### 7. قدرات قريبة في العائلة

- `SYNC-01` الصوت هو الساعة الرئيسية / Audio is the master clock (proven)
- `SYNC-03` محوّل الترجمات والتفريغ إلى words.json / Subtitle/transcript → words.json converter (proven)
- `SYNC-04` حدود تسامح التزامن / Sync tolerances (proven)

### `SYNC-03` — محوّل الترجمات والتفريغ إلى words.json / Subtitle/transcript → words.json converter

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يحوّل SRT وVTT وWhisper JSON والقوائم وCSV/TSV إلى توقيت كلمات مرتب غير متداخل، ويزيح الكل بإزاحة ويفرض فجوة دنيا. / Converts SRT, VTT, Whisper JSON, flat lists and CSV/TSV into sorted, non-overlapping word timings, with a global offset and a minimum gap.

**متى:** حين يملك المستخدم ملف ترجمة SRT أو VTT أو تفريغ Whisper ويريده توقيت كلمات / when the user has SRT, VTT, Whisper JSON or CSV and needs it as words.json

**كيف:** python3 tools/words_convert.py in.srt out.json [--format srt\|vtt\|json\|csv\|tsv] [--offset -0.08] [--min-gap 0.02]; SRT/VTT cues spread words by letter count (phrase-level timing only — per-word effects want real word stamps); strips <tags>, {ASS} tags, dashes and ♪; min word 20 ms. Ran here on an Arabic SRT: 6 words, offset −0.05 s applied, then words.js emitted.

**المعاملات:** --offset −0.08; --min-gap 0.02; min word 20 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تحويل · srt · vtt · words_convert · offset · ملف ترجمة · سب تايتل · تحويل الترجمة · subtitles · whisper json

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-tool/tools/words_convert.py`
- `kosif-tool/tools/words_convert.py:122`
- `kosif-tool/playbooks/audio-sync.md:27`

#### 7. قدرات قريبة في العائلة

- `SYNC-01` الصوت هو الساعة الرئيسية / Audio is the master clock (proven)
- `SYNC-02` ملف توقيت الكلمات kosif-words/1 / words.json master timing schema (proven)
- `SYNC-04` حدود تسامح التزامن / Sync tolerances (proven)
- `SYNC-05` قياس التزامن إطارًا بإطار / Frame-by-frame sync probe (proven)

### `SYNC-04` — حدود تسامح التزامن / Sync tolerances

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الحركة تبدأ قبل الكلمة بـ 40–80 ms، والكلمة المفتاحية ≤ 100 ms، والباقي ≤ 150 ms، ولا قطع وسط كلمة، ولا حركة قبل أن تُسمع. / Motion starts 40–80 ms before the word; key words ≤ 100 ms, others ≤ 150 ms; never cut mid-word; never animate before it is heard.

**متى:** عند ضبط أو مراجعة دقة التزامن بين الحركة والكلمة المنطوقة / when setting or checking how close motion must land to each spoken word

**كيف:** offset_ms = \|word.start − motion_frame/fps\| × 1000 ≤ 100 for emphasis words; visual lead ≤ 80 ms; pauses > 400 ms end a phrase, > 600 ms allow a scene change, > 1.5 s need ambient motion. Log it in templates/TEST_REPORT.md. Measured in the proof: max \|Δ\| 33 ms (one frame), 0 early words; the spectrum film filled every word ≤ 35 ms after its start.

**المعاملات:** lead 40–80 ms; key ≤ 100 ms; others ≤ 150 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تسامح · tolerance · sync accuracy · lead · 100 ms · دقة التزامن · تأخير الحركة · مزامنة مع الكلام · timing offset · word sync

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-tool/playbooks/audio-sync.md:29`
- `kosif-tool/playbooks/audio-sync.md:34`
- `kosif-tool/templates/TEST_REPORT.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-02` ملف توقيت الكلمات kosif-words/1 / words.json master timing schema (proven)
- `SYNC-03` محوّل الترجمات والتفريغ إلى words.json / Subtitle/transcript → words.json converter (proven)
- `SYNC-05` قياس التزامن إطارًا بإطار / Frame-by-frame sync probe (proven)
- `SYNC-06` التحقق من توقيت جاهز / Pre-timed transcript validation (ready)

### `SYNC-05` — قياس التزامن إطارًا بإطار / Frame-by-frame sync probe

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يبحث كل إطار في الصفحة ويسجل أول إطار تظهر فيه كل كلمة، ثم يقارنه بزمن نطقها. / Seeks every frame of the page and records when each word first becomes visible, then compares it with its spoken start.

**متى:** عند التحقق إطارا بإطار من ظهور كل كلمة وقت نطقها بعد تعديل words.json / when verifying frame by frame that each word appears on its spoken start

**كيف:** node proofs/arabic-voice-kinetic/sync_probe.cjs index.html 30 100 → 'SYNC OK words=15 max\|delta\|=33 ms early=0'. Requires a deterministic window.__kosif.seek(t). Re-run whenever words.json changes.

**المعاملات:** fps 30; tolerance 100 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قياس التزامن · sync probe · qa · word onset · فحص التزامن · اختبار التوقيت · مراجعة الجودة · sync check · frame check

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/sync_probe.cjs`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-03` محوّل الترجمات والتفريغ إلى words.json / Subtitle/transcript → words.json converter (proven)
- `SYNC-04` حدود تسامح التزامن / Sync tolerances (proven)
- `SYNC-06` التحقق من توقيت جاهز / Pre-timed transcript validation (ready)
- `SYNC-07` تفريغ عربي محلي بتوقيت الكلمات / Local Arabic word-timed transcription (faster-whisper) (proven)

### `SYNC-06` — التحقق من توقيت جاهز / Pre-timed transcript validation

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يقبل words.json خارجيًا فقط إذا كان محدودًا ومتصاعدًا، فيعمل الريل بلا Whisper لكن لا بتوقيت مخترع. / Accepts an external words.json only if bounded and monotonic, so reels can run without Whisper but never with invented timing.

**متى:** حين يأتي المستخدم بملف words.json جاهز ويريد تشغيل الريل دون Whisper / when the user brings a ready words.json and the reel must run without Whisper

**كيف:** reel --transcript NAME.words.json → transcribe.load_transcript.

**المعاملات:** ≤ 10 MB; ≤ 20,000 segments; tolerance 0.02 s; end ≤ duration + 0.15 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تحقق · validation · words.json · monotonic · توقيت جاهز · تفريغ خارجي · ريل · pretimed transcript · external transcript

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-studio/motion/transcribe.py:89`

#### 7. قدرات قريبة في العائلة

- `SYNC-04` حدود تسامح التزامن / Sync tolerances (proven)
- `SYNC-05` قياس التزامن إطارًا بإطار / Frame-by-frame sync probe (proven)
- `SYNC-07` تفريغ عربي محلي بتوقيت الكلمات / Local Arabic word-timed transcription (faster-whisper) (proven)
- `SYNC-08` فخ نماذج .en / The .en model trap (documented)

### `SYNC-07` — تفريغ عربي محلي بتوقيت الكلمات / Local Arabic word-timed transcription (faster-whisper)

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صوت إلى مقاطع وكلمات بزمن بداية ونهاية واحتمال، دون إنترنت بعد تنزيل النموذج. / Speech → segments and words with start/end/probability, offline once the model is cached.

**متى:** حين يحتاج المستخدم تفريغ كلام عربي بتوقيت كل كلمة محليا دون إنترنت / when Arabic speech needs local, offline transcription with per-word timing

**كيف:** python transcribe.py SRC --model large-v3\|small\|auto --lang ar [--prompt '…'] → words.json + SRT (UTF-8 BOM) + captions.json; 16 kHz mono, CPU int8, beam 5, vad_filter, BatchedInferencePipeline batch 8 (≈ 3–4× faster). Ran here in the proof venv (small): 15/15 words matched the script, but starts were early by a median 135 ms and up to 670 ms after pauses → snap to onsets or prefer a forced aligner; human-voice error measured ~±150 ms (median 103, max 258).

**المعاملات:** 16 kHz mono; batch 8; error ~±150 ms

**التثبيت:** pip install faster-whisper # models from huggingface.co (reachable): small 466 MB, large-v3 3.1 GB

**الوسوم:** تفريغ · whisper · faster-whisper · asr · word timestamps · arabic · تحويل الكلام لنص · استخراج الترجمة · تفريغ صوتي · speech to text · offline

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `network` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-studio/motion/transcribe.py:36`
- `100-superskills/skills/kosif-montage-motion/scripts/transcribe.py`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/transcribe.py`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-05` قياس التزامن إطارًا بإطار / Frame-by-frame sync probe (proven)
- `SYNC-06` التحقق من توقيت جاهز / Pre-timed transcript validation (ready)
- `SYNC-08` فخ نماذج .en / The .en model trap (documented)
- `SYNC-09` توقيت حقيقي من فونيمات Piper / True word timing from Piper phonemes (proven)

### `SYNC-08` — فخ نماذج .en / The .en model trap

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نماذج Whisper ذات اللاحقة .en تترجم الكلام غير الإنجليزي إلى الإنجليزية بصمت بدل تفريغه. / Whisper models ending in .en silently translate non-English speech into English instead of transcribing it.

**متى:** عند اختيار نموذج Whisper لتفريغ كلام عربي أو غير إنجليزي / when choosing a Whisper model to transcribe Arabic or other non-English speech

**كيف:** Always pass --model explicitly (the HyperFrames CLI defaults to small.en!) with --language ar. Ladder: tiny 75 MB (pipeline test), base 142 MB, small 466 MB (default), medium 1.5 GB (noisy/music, minimum for lyrics), large-v3 3.1 GB (production), turbo = speed/accuracy sweet spot. Parakeet covers 25 European languages only — Arabic goes through Whisper. Convert to 16 kHz WAV first.

**المعاملات:** tiny 75 MB … large-v3 3.1 GB

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** whisper · en model · language ar · model size · trap · اختيار النموذج · تفريغ عربي · ترجمة خاطئة · small.en · transcription

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md`
- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transcript-guide.md`
- `kosif-one/vendor/hyperframes/skills/media-use/audio/references/transcribe.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-06` التحقق من توقيت جاهز / Pre-timed transcript validation (ready)
- `SYNC-07` تفريغ عربي محلي بتوقيت الكلمات / Local Arabic word-timed transcription (faster-whisper) (proven)
- `SYNC-09` توقيت حقيقي من فونيمات Piper / True word timing from Piper phonemes (proven)
- `SYNC-10` محاذاة النص الصحيح على التفريغ / True-text alignment onto ASR (proven)

### `SYNC-09` — توقيت حقيقي من فونيمات Piper / True word timing from Piper phonemes

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عند توليد الصوت بـ Piper تعطي مدة كل فونيم توقيت الكلمات الحقيقي بلا تفريغ. / When the voice is synthesised with Piper, phoneme durations give exact word timing without ASR.

**متى:** حين يكون التعليق الصوتي مولدا بـ Piper ونريد توقيت كلمات دقيقا بلا تفريغ / when the voice is synthesised with Piper and exact word timing is needed without ASR

**كيف:** synth_voice.py (length_scale 0.95, 0.30 s between sentences) → align_words.py → words.json; Whisper stamps stay in asr_start for audit. Proof: max \|Δ\| 33 ms, 0 early. Piper noise is unseeded, so make_voice.sh regenerates voice and words.json together.

**المعاملات:** length_scale 0.95; 0.30 s sentence gap

**التثبيت:** pip install piper-tts

**الوسوم:** piper · فونيمات · phoneme alignment · tts timing · تعليق صوتي · صوت مولد · توقيت الكلمات · text to speech · word timing

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:piper` ← python3 -c "import piper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/synth_voice.py`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/align_words.py`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/make_voice.sh`

#### 7. قدرات قريبة في العائلة

- `SYNC-07` تفريغ عربي محلي بتوقيت الكلمات / Local Arabic word-timed transcription (faster-whisper) (proven)
- `SYNC-08` فخ نماذج .en / The .en model trap (documented)
- `SYNC-10` محاذاة النص الصحيح على التفريغ / True-text alignment onto ASR (proven)
- `SYNC-11` تصحيح الكلمات مع حفظ التوقيت / Transcript fixes that keep timing (ready)

### `SYNC-10` — محاذاة النص الصحيح على التفريغ / True-text alignment onto ASR

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يضع كلمات الأغنية أو القصيدة أو الدعاء الصحيحة (بالتشكيل) على أزمنة كلمات التفريغ. / Puts the real lyrics/poem/dua words (with diacritics) onto recognised word times.

**متى:** عند وضع كلمات الأغنية أو القصيدة أو الدعاء الصحيحة بالتشكيل على أزمنة التفريغ / when the exact lyrics, poem or dua text must replace ASR words while keeping their times

**كيف:** verse.align(lines, asr) via difflib.SequenceMatcher on normalised words: equal or one-to-one blocks inherit times, uneven replacements share the span by length, missed words spread between timed neighbours; then verse.segment cuts lines before phrase openers, ≤ 7 words, never ending on a particle. Ran here: test_verse_reads_a_text_like_a_lyricist ok and tests.test_directors ok. Basma's bridge variant aligns with an LCS table and rejects matches below 40%.

**المعاملات:** fill step ≥ 0.05 s; min word 0.05 s; ≤ 7 words/line

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** محاذاة · نص صحيح · forced alignment · lyrics · dua · tashkeel · كلمات الأغنية · قصيدة · تشكيل · poem · text alignment

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-studio/motion/verse.py:83`
- `kosif-studio/tests/test_studio.py:943`
- `100-superskills/skills/kosif-montage-motion/tests/test_directors.py:42`
- `app/public/js/00_editor.js:2684`

#### 7. قدرات قريبة في العائلة

- `SYNC-08` فخ نماذج .en / The .en model trap (documented)
- `SYNC-09` توقيت حقيقي من فونيمات Piper / True word timing from Piper phonemes (proven)
- `SYNC-11` تصحيح الكلمات مع حفظ التوقيت / Transcript fixes that keep timing (ready)
- `SYNC-12` ضبط بداية الكلمة على النطق / Onset snapping of word stamps (documented)

### `SYNC-11` — تصحيح الكلمات مع حفظ التوقيت / Transcript fixes that keep timing

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يستبدل العبارات المسموعة خطأ وينشر الكلمات الصحيحة على المدى الأصلي. / Replaces misheard phrases while spreading the right words over the original span.

**متى:** حين يخطئ التفريغ في سماع كلمات أو لهجة ونريد تصحيحها دون فقد التوقيت / when ASR misheard words or dialect and the fixes must keep the original timing

**كيف:** --fix "ما حدش=محدش;بتعودش ضايع=متقعدش تضيّع" (direct, verse); merge split clitics and attached punctuation into displayable words; for the Quran use the user's exact text, never the ASR.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تصحيح · لهجة · transcript fix · clitics · أخطاء التفريغ · تعديل الكلمات · عامية · misheard words · dialect

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-studio/motion/direct.py:205`
- `kosif-studio/tests/test_studio.py:910`
- `kosif-tool/playbooks/audio-sync.md:76`

#### 7. قدرات قريبة في العائلة

- `SYNC-09` توقيت حقيقي من فونيمات Piper / True word timing from Piper phonemes (proven)
- `SYNC-10` محاذاة النص الصحيح على التفريغ / True-text alignment onto ASR (proven)
- `SYNC-12` ضبط بداية الكلمة على النطق / Onset snapping of word stamps (documented)
- `SYNC-13` تجهيز الصوت للتفريغ وفخ التوقيت / STT audio prep & its timing trap (documented)

### `SYNC-12` — ضبط بداية الكلمة على النطق / Onset snapping of word stamps

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طوابع النماذج تتأخر أو تتقدم عن بداية النطق المسموع؛ اربط كل كلمة بأقرب بداية صوتية. / Model stamps drift from the audible onset; snap each word to the nearest detected vocal onset.

**متى:** عند ملاحظة أن طوابع الكلمات تسبق النطق المسموع أو تتأخر عنه / when word stamps drift early or late from the audible onset and need snapping

**كيف:** Spectral-flux / energy-derivative onset detection near each stamp (±120 ms), keep the original in 'stamp', render one frame per word onset on a sheet to verify. Reported lag 50–80 ms for sung vocals; our Whisper run was early instead (median 135 ms) — measure which way yours drifts before correcting.

**المعاملات:** search ±120 ms; lag 50–80 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بداية النطق · onset · snap · lyrics timing · تأخر الكلمات · تقديم الترجمة · ضبط التوقيت · timing drift · vocal onset

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-10` محاذاة النص الصحيح على التفريغ / True-text alignment onto ASR (proven)
- `SYNC-11` تصحيح الكلمات مع حفظ التوقيت / Transcript fixes that keep timing (ready)
- `SYNC-13` تجهيز الصوت للتفريغ وفخ التوقيت / STT audio prep & its timing trap (documented)
- `SYNC-14` تفريغ سحابي مع فصل المتحدثين / Cloud STT with diarisation (key)

### `SYNC-13` — تجهيز الصوت للتفريغ وفخ التوقيت / STT audio prep & its timing trap

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** للتفريغ فقط: مرشح 200 Hz–3 kHz و16 kHz أحادي؛ لكن حذف الصمت أو تسريع الصوت يكسر التوقيت. / For transcription only: 200 Hz–3 kHz band and 16 kHz mono; silence removal or speed-up breaks the timeline.

**متى:** عند تجهيز الصوت للتفريغ مع الحذر من حذف الصمت أو التسريع الذي يكسر التوقيت / when preparing audio for transcription without breaking the timeline

**كيف:** ffmpeg -af 'highpass=f=200,lowpass=f=3000' -ar 16000 -ac 1 -c:a pcm_s16le. Silence removal (0.5 s at −30 dB) saves 10–40% of billed minutes and atempo 1.25 another 20%, but never use those outputs for words.json — always transcribe or align against the untouched original.

**المعاملات:** 16 kHz mono; HPF 200 / LPF 3000

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تجهيز الصوت · stt prep · 16 khz · timing trap · تنقية الصوت · فلتر الصوت · حذف الصمت · ffmpeg · band filter

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-atlas/skills/1845-deepgram-pack/5468-deepgram-cost-tuning/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-11` تصحيح الكلمات مع حفظ التوقيت / Transcript fixes that keep timing (ready)
- `SYNC-12` ضبط بداية الكلمة على النطق / Onset snapping of word stamps (documented)
- `SYNC-14` تفريغ سحابي مع فصل المتحدثين / Cloud STT with diarisation (key)
- `SYNC-15` تفريغ HyperFrames / HyperFrames transcribe CLI (install)

### `SYNC-14` — تفريغ سحابي مع فصل المتحدثين / Cloud STT with diarisation

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عند الحاجة لأسماء المتحدثين أو سرعة عالية: خدمات تفريغ مستضافة بتوقيت كلمات. / When speaker labels or fast turnaround matter: hosted ASR with word timings.

**متى:** حين نحتاج أسماء المتحدثين أو تفريغا سريعا عبر خدمة مستضافة / when speaker labels or fast turnaround call for hosted transcription with word timings

**كيف:** Deepgram nova-3 (smart_format, diarize, utterances), ElevenLabs scribe_v1 (diarize + word timestamps), AssemblyAI (speaker labels), Together whisper-large-v3 (80 MB upload / 4 h per request), Gemini verbatim segments of 3–8 words (≤ 18 MB inline). Normalise to [{text,start,end,speaker}] then words_convert. Each needs its own API key.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تفريغ سحابي · diarization · deepgram · elevenlabs · speakers · فصل المتحدثين · تعدد المتحدثين · تفريغ سريع · assemblyai · speaker labels

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `key:elevenlabs` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `pip:pyannote` ← python3 -c "import pyannote" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-atlas/skills/1845-deepgram-pack/5473-deepgram-hello-world/SKILL.md`
- `kosif-atlas/skills/1847-elevenlabs-pack/5515-elevenlabs-core-workflow-b`
- `app/public/js/00_editor.js:1525`

#### 7. قدرات قريبة في العائلة

- `SYNC-12` ضبط بداية الكلمة على النطق / Onset snapping of word stamps (documented)
- `SYNC-13` تجهيز الصوت للتفريغ وفخ التوقيت / STT audio prep & its timing trap (documented)
- `SYNC-15` تفريغ HyperFrames / HyperFrames transcribe CLI (install)
- `SYNC-16` كشف الإعادات وتجميع المونتاج من النص / Retake detection & transcript-driven assembly (documented)

### `SYNC-15` — تفريغ HyperFrames / HyperFrames transcribe CLI

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 |

**ما هي:** أمر واحد يفرّغ بـ Parakeet أو whisper.cpp ويخرج SRT/VTT أو كلمات. / One command transcribing via Parakeet or whisper.cpp to SRT/VTT or words.

**متى:** عند تفريغ فيديو أو صوت بأمر واحد إلى SRT أو VTT أو كلمات عبر HyperFrames / when one command should transcribe a clip to SRT, VTT or words via HyperFrames

**كيف:** npx hyperframes transcribe talk.mp4 --engine whisper --model small --language ar [--to srt\|vtt]; also normalises existing .srt/.vtt/openai.json into a word array. Never rely on the default model (small.en).

**التثبيت:** npx hyperframes transcribe <file> --engine whisper --model small --language ar

**الوسوم:** hyperframes · transcribe · parakeet · whisper.cpp · تفريغ · استخراج ترجمة · ملف ترجمة · srt · subtitles

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `key:openai` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/media-use/scripts/transcribe.mjs`
- `kosif-one/vendor/hyperframes/skills/media-use/references/operations.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-13` تجهيز الصوت للتفريغ وفخ التوقيت / STT audio prep & its timing trap (documented)
- `SYNC-14` تفريغ سحابي مع فصل المتحدثين / Cloud STT with diarisation (key)
- `SYNC-16` كشف الإعادات وتجميع المونتاج من النص / Retake detection & transcript-driven assembly (documented)
- `SYNC-17` توزيع النص على مقاطع الصوت / Text over voiced spans (estimated) (ready)

### `SYNC-16` — كشف الإعادات وتجميع المونتاج من النص / Retake detection & transcript-driven assembly

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الإعادات = مقاطع تبدأ بنفس الحروف العشرة خلال 60 ث، ويُحتفظ بالأخيرة؛ ثم يُبنى المونتاج من جدول نبضات بالنص. / Retakes = segments with the same first 10 characters within 60 s, keeping the last; then the edit is assembled from a transcript beat sheet.

**متى:** حين يحوي التسجيل جملا معادة ونريد الاحتفاظ بآخرها وبناء المونتاج من النص / when a recording has retakes and the edit should be assembled from the transcript

**كيف:** Inventory clips → beat sheet (beat \| message \| voice range \| screen \| length) for approval → assemble in beat order with a chapter marker per beat; keep an 'unused sentences' list; the first beat poses the question within 10 s. Never pick a non-default take without asking. Record narration at 48 kHz, ~1 s between sentences, clap once for multi-camera sync.

**المعاملات:** prefix 10 chars; window 60 s; hook ≤ 10 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إعادات · retakes · beat sheet · transcript edit · مونتاج من النص · حذف الإعادات · تقطيع · edit assembly · duplicate takes

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-atlas/skills/1096-akbun-editvideo/2451-davinciresolve-beats-devtalk/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2447-akbun-vlog-shootplan/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-14` تفريغ سحابي مع فصل المتحدثين / Cloud STT with diarisation (key)
- `SYNC-15` تفريغ HyperFrames / HyperFrames transcribe CLI (install)
- `SYNC-17` توزيع النص على مقاطع الصوت / Text over voiced spans (estimated) (ready)
- `SYNC-18` توقيت الكلمات حسب الطول / Word timing by length (proven)

### `SYNC-17` — توزيع النص على مقاطع الصوت / Text over voiced spans (estimated)

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بلا تفريغ: يضع النص على الأجزاء المسموعة بالترتيب وحسب طول الكلمة، ويسمّي النتيجة تقديرًا. / Without ASR, lays the text over the voiced stretches in order and by word length, and labels it estimated.

**متى:** حين لا يتوفر تفريغ ونريد توزيع النص على مقاطع الكلام المسموعة كتقدير / when no ASR is available and text must be spread over voiced spans as an estimate

**كيف:** verse.voiced_spans + estimate: 50 ms frames, threshold max(−45 dB, p20+6 dB), merge gaps < 0.35 s, spans > 0.15 s. Browser variants: Basma syncToSpeech (new segment after 5 words or a > 0.3 s gap) and region detection (thr max(0.008, 0.22·p90), merge 0.28 s, min 0.18 s). Voice2Motion marks such timing estimated_from_text_length_NOT_ASR.

**المعاملات:** frames 50 ms; merge < 0.35 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تقدير · voiced spans · no asr · estimate · بدون تفريغ · توزيع النص · توقيت تقريبي · approximate timing · speech regions

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-studio/motion/verse.py:121`
- `kosif-studio/motion/verse.py:145`
- `app/public/js/00_editor.js:1096`

#### 7. قدرات قريبة في العائلة

- `SYNC-15` تفريغ HyperFrames / HyperFrames transcribe CLI (install)
- `SYNC-16` كشف الإعادات وتجميع المونتاج من النص / Retake detection & transcript-driven assembly (documented)
- `SYNC-18` توقيت الكلمات حسب الطول / Word timing by length (proven)
- `SYNC-19` ميزانية الكلمات حسب الزمن / Narration word budgets (documented)

### `SYNC-18` — توقيت الكلمات حسب الطول / Word timing by length

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إذا كان للسطر زمن بلا أزمنة كلمات، يُقسم بين كلماته حسب عدد الحروف زائد ثابت. / When a caption line has no word times, its span is shared among words by letter count plus a constant.

**متى:** حين يكون لسطر الترجمة زمن بلا أزمنة كلمات ونريد توزيعه حسب طول الكلمات / when a caption line has a time span but no word times

**كيف:** montage.word_times with weight = len(word) + 2. Covered by test_montage_cuts_on_the_beat_and_captions_shape_arabic (ran here, ok).

**المعاملات:** weight = len + 2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** توزيع · word timing · by length · srt · طول الكلمة · عدد الحروف · سطر الترجمة · letter count · caption line

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-studio/motion/montage.py:341`
- `kosif-studio/tests/test_studio.py:765`

#### 7. قدرات قريبة في العائلة

- `SYNC-16` كشف الإعادات وتجميع المونتاج من النص / Retake detection & transcript-driven assembly (documented)
- `SYNC-17` توزيع النص على مقاطع الصوت / Text over voiced spans (estimated) (ready)
- `SYNC-19` ميزانية الكلمات حسب الزمن / Narration word budgets (documented)
- `SYNC-20` سكريبت بتوقيت مكتوب / Timestamped script parser (proven)

### `SYNC-19` — ميزانية الكلمات حسب الزمن / Narration word budgets

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حوّل المدة إلى عدد كلمات قبل كتابة التعليق كي لا تزدحم المشاهد. / Turn duration into a word budget before writing narration so scenes are not over-stuffed.

**متى:** قبل كتابة التعليق الصوتي لتحديد عدد الكلمات المناسب لمدة كل مشهد / before writing narration, to fit the word count to each scene's duration

**كيف:** ~150 words/min long-form; short-form 80–150 words for 20–45 s; per scene: 3–4 s → 8–12 words, 5–6 s → 15–22, 7–8 s → 22–30. Generated talking segments: words/2 s (≈ 2 wps), minimum 4 s, split above 15 s at a sentence. For Arabic measure the real TTS duration and retime from words.json rather than trusting counts; or generate TTS per sentence and set each scene to its clip length.

**المعاملات:** 150 wpm; ≈ 2 words/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ميزانية الكلمات · word budget · pacing · script length · طول السكريبت · كتابة التعليق · عدد الكلمات · narration · words per minute

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-atlas/skills/166-demo-video/535-demo-video/references/scene-design-system.md`
- `kosif-atlas/skills/259-quickdesign/865-quickdesign`
- `style:pm-linearuncle-5d2bae`

#### 7. قدرات قريبة في العائلة

- `SYNC-17` توزيع النص على مقاطع الصوت / Text over voiced spans (estimated) (ready)
- `SYNC-18` توقيت الكلمات حسب الطول / Word timing by length (proven)
- `SYNC-20` سكريبت بتوقيت مكتوب / Timestamped script parser (proven)
- `SYNC-21` تجميع الكلمات حسب الطاقة / Word grouping by energy (documented)

### `SYNC-20` — سكريبت بتوقيت مكتوب / Timestamped script parser

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يقبل أسطرًا مثل «0–3s: نص» ويوزع الكلمات على مقاطع 8/10 ث حسب البداية، ويرفض التوقيت الناقص أو المتداخل. / Accepts lines like '0–3s: text' and assigns words to 8/10 s clips by start time; rejects partial or overlapping stamps.

**متى:** حين يكتب المستخدم سكريبت بأسطر موقوتة مثل 0–3s ويريد توزيعه على المقاطع / when a script comes with timed lines like '0–3s: text' to split across clips

**كيف:** parseTimestamps regex ^(\d+(\.\d+)?)\s*[–—-]\s*(\d+(\.\d+)?)s?\s*:\s*(.+)$; clip index floor(start/len). Ran here: node --test tests/production-profiles.test.mjs → pass 10, fail 0.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سكريبت · timestamps · parser · script timing · سكريبت موقوت · توقيت مكتوب · تقسيم المقاطع · timed script · clips

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:67-77`
- `fastify-motion-bro/tests/production-profiles.test.mjs:75-81`

#### 7. قدرات قريبة في العائلة

- `SYNC-18` توقيت الكلمات حسب الطول / Word timing by length (proven)
- `SYNC-19` ميزانية الكلمات حسب الزمن / Narration word budgets (documented)
- `SYNC-21` تجميع الكلمات حسب الطاقة / Word grouping by energy (documented)
- `SYNC-22` موضع آمن وضمان الاختفاء / Safe placement & exit guarantee (documented)

### `SYNC-21` — تجميع الكلمات حسب الطاقة / Word grouping by energy

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طاقة عالية 2–3 كلمات، حوار 3–5، هدوء 4–6؛ والانقسام عند نهاية الجملة أو وقفة ≥ 150 ms. / High energy 2–3 words, conversational 3–5, calm 4–6; break on sentence ends or pauses ≥ 150 ms.

**متى:** عند تقسيم الترجمة إلى مجموعات كلمات تناسب طاقة الكلام ووقفاته / when splitting captions into word groups that match speech energy and pauses

**كيف:** Pages of ~1200 ms (Remotion createTikTokStyleCaptions combineTokensWithinMilliseconds 1200); one group visible at a time; Claude splits 2–5 words at natural pauses without separating prepositions and stars one word per line. Arabic: ≤ 6 words per screen in reels.

**المعاملات:** 2–3 / 3–5 / 4–6 words; pause 150 ms; page 1200 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تجميع · grouping · caption pages · words per line · تقسيم الترجمة · سطور الترجمة · عدد الكلمات في السطر · chunking · tiktok captions

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md`
- `kosif-atlas/skills/2712-remotion/10431-remotion-captions/display-captions.md`
- `app/public/js/00_editor.js:1510`

#### 7. قدرات قريبة في العائلة

- `SYNC-19` ميزانية الكلمات حسب الزمن / Narration word budgets (documented)
- `SYNC-20` سكريبت بتوقيت مكتوب / Timestamped script parser (proven)
- `SYNC-22` موضع آمن وضمان الاختفاء / Safe placement & exit guarantee (documented)
- `SYNC-23` ستايل الترجمة حسب نبرة الكلام / Caption style by tone (documented)

### `SYNC-22` — موضع آمن وضمان الاختفاء / Safe placement & exit guarantee

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الترجمة في المنطقة الآمنة، لا تغطي الوجوه، ومجموعة واحدة ظاهرة، وكل مجموعة تُخفى قسرًا عند نهايتها. / Captions sit in safe zones, never over faces, one group at a time, each force-hidden at its end.

**متى:** عند تحديد مكان الترجمة بعيدا عن الوجوه وواجهة المنصة وضمان اختفائها في وقتها / when placing captions in safe zones away from faces and platform UI, each group exiting on time

**كيف:** 16:9: 80–120 px from the bottom; 9:16: ~600–700 px from the bottom (keep ≥ 280 px clear of platform UI); full-width absolute container, overflow visible; exit tween 0.12 s then set opacity 0 + visibility hidden at group end; self-lint by seeking end + 0.01 s. fitTextFontSize maxWidth 1600/900, base 78, min 42, step 2. Basma 'auto' places captions in the third farthest from the tracked subject.

**المعاملات:** 16:9 bottom 80–120 px; 9:16 ~600–700 px; exit 0.12 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** منطقة آمنة · safe zone · placement · exit · faces · مكان الترجمة · إخفاء الترجمة · تداخل الترجمة · vertical video · caption position

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md`
- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/montage_grammar.md`
- `app/public/js/00_editor.js:2906`

#### 7. قدرات قريبة في العائلة

- `SYNC-20` سكريبت بتوقيت مكتوب / Timestamped script parser (proven)
- `SYNC-21` تجميع الكلمات حسب الطاقة / Word grouping by energy (documented)
- `SYNC-23` ستايل الترجمة حسب نبرة الكلام / Caption style by tone (documented)
- `SYNC-24` وضوح الترجمة العربية / Arabic caption legibility (documented)

### `SYNC-23` — ستايل الترجمة حسب نبرة الكلام / Caption style by tone

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اقرأ النص، حدد النبرة، ثم اختر الوزن والدخول واللون والحجم. / Read the transcript, detect tone, then pick weight, entrance, colour and size.

**متى:** عند اختيار شكل الترجمة وحركتها حسب نبرة الكلام: حماسي أو رسمي أو تعليمي أو قصصي / when picking caption weight, entrance, colour and size from the speech tone

**كيف:** Hype: 800–900 weight, scale-pop back.out(1.7) 0.1–0.2 s, 72–96 px. Corporate: 600–700, fade+slide power3.out 0.3 s, 56–72 px. Tutorial: mono 500–600, typewriter 0.4–0.5 s, 48–64 px. Story: serif 400–500, slow fade 0.5–0.6 s, 44–56 px. Social: rounded 700–800, elastic word-by-word, 56–80 px. Entry tones (stagger/hold): documentary 150/600 ms, conversational 80/400, energetic 50/300 pop, poetic 250/1200 etch. Soft = fade + 8 px drift; present = 6 px + 1.04 pop.

**المعاملات:** 44–96 px by tone

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نبرة · tone · caption style · hype · documentary · شكل الترجمة · خط الترجمة · حماسي · corporate · tutorial

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md`
- `kosif-one/vendor/hyperframes/skills/embedded-captions/references/motion-vocabulary.md`
- `kosif-one/vendor/hyperframes/skills/embedded-captions/references/typography-presets.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-21` تجميع الكلمات حسب الطاقة / Word grouping by energy (documented)
- `SYNC-22` موضع آمن وضمان الاختفاء / Safe placement & exit guarantee (documented)
- `SYNC-24` وضوح الترجمة العربية / Arabic caption legibility (documented)
- `SYNC-25` لا تغيّر كلام المتحدث، والحرق عند الطلب / Verbatim words; burn only when asked (documented)

### `SYNC-24` — وضوح الترجمة العربية / Arabic caption legibility

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الكلمة المنطوقة بلون مميز والباقي أبيض، حد أسود سميك وظل عميق، 5–7 كلمات، تباين ≥ 4.5:1. / Spoken word in a highlight colour, rest white; thick black outline and deep shadow; 5–7 words; contrast ≥ 4.5:1.

**متى:** حين تكون الترجمة العربية صعبة القراءة فوق الفيديو أو نحتاج تباينا كافيا / when Arabic captions must stay readable over video with enough contrast

**كيف:** Highlight #FFDE59 or #38BDF8; outline 6–8 px; Cairo, Noto Sans/Kufi/Naskh Arabic, Almarai; subtitles ≤ 42 chars/line, 1–2 lines, 1–7 s each. When there is no stroke, sample the caption band every 6th frame and add a dark/light plate only as strong as needed for 4.5:1 (max alpha 0.75). Bilingual block: Arabic on top RTL, English below LTR at 70% size, each with its own dir.

**المعاملات:** ≤ 42 chars; 1–7 s; ≥ 4.5:1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** وضوح · تباين · legibility · contrast · bilingual · قراءة الترجمة · حد أسود · ترجمة عربية · outline · readable captions

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/montage_grammar.md`
- `app/public/js/00_editor.js:3007`
- `kosif-tool/playbooks/arabic-typography.md:46`

#### 7. قدرات قريبة في العائلة

- `SYNC-22` موضع آمن وضمان الاختفاء / Safe placement & exit guarantee (documented)
- `SYNC-23` ستايل الترجمة حسب نبرة الكلام / Caption style by tone (documented)
- `SYNC-25` لا تغيّر كلام المتحدث، والحرق عند الطلب / Verbatim words; burn only when asked (documented)
- `SYNC-26` إبراز تلقائي للكلمات المهمة / Automatic emphasis words (ready)

### `SYNC-25` — لا تغيّر كلام المتحدث، والحرق عند الطلب / Verbatim words; burn only when asked

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الترجمة تعيد كلام المتحدث حرفيًا، والترجمة المحروقة فقط عند الطلب وإلا SRT/VTT جانبي. / Captions reproduce the speaker's words exactly; burn only on request, otherwise ship SRT/VTT sidecars.

**متى:** عند تسليم الترجمة: نقل كلام المتحدث حرفيا وحرقها فقط إذا طلبها المستخدم / when delivering captions verbatim, as SRT/VTT sidecars unless burning is requested

**كيف:** Diff caption text vs words.json in QA. Default deliverables: .srt + .vtt; soft track inside MP4: -c:s mov_text -metadata:s:s:0 language=ara (ran here: stream tagged 'ara'). Accessibility package: speech + [sound] cues, audio-description notes for visual-only beats.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حرفي · verbatim · srt · sidecar · accessibility · mov_text · ترجمة محروقة · ملف ترجمة جانبي · إتاحة · vtt · burned captions

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`
- `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`
- `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-23` ستايل الترجمة حسب نبرة الكلام / Caption style by tone (documented)
- `SYNC-24` وضوح الترجمة العربية / Arabic caption legibility (documented)
- `SYNC-26` إبراز تلقائي للكلمات المهمة / Automatic emphasis words (ready)
- `SYNC-27` كاريوكي ASS عربي بحدث لكل كلمة / Arabic ASS karaoke, one event per word (proven)

### `SYNC-26` — إبراز تلقائي للكلمات المهمة / Automatic emphasis words

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الأرقام والأسماء والكلمات العاطفية تُبرز، وفي السطر بلا إبراز تُختار الكلمة عند أعلى قمة صوت. / Numbers, brands and emotional words get emphasis; in lines without one, the word at the loudest local peak is starred.

**متى:** حين نريد إبراز الأرقام والأسماء والكلمات العاطفية تلقائيا في الترجمة / when numbers, brands and emotional words should be emphasised automatically

**كيف:** autoEm wraps any word with a digit in *…*; loudPeaks: 0.25 s smoothed dB envelope, local maxima ≥ 4 dB above the median within ±3 s, ≥ 1.2 s apart, 3–12 per clip; the starred word gets accent + bigger scale + overshoot. Karaoke intensity ladder: high energy = accent + glow + 15% pop; low = warm white + 3%.

**المعاملات:** ≥ 4 dB over median; spacing 1.2 s; pop 15% / 3%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إبراز · emphasis · keyword · loudness peak · numbers · كلمة مميزة · تمييز الكلمات · هايلايت · highlight words · accent word

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `app/public/js/00_editor.js:1875`
- `app/public/js/00_editor.js:3032`
- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/dynamic-techniques.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-24` وضوح الترجمة العربية / Arabic caption legibility (documented)
- `SYNC-25` لا تغيّر كلام المتحدث، والحرق عند الطلب / Verbatim words; burn only when asked (documented)
- `SYNC-27` كاريوكي ASS عربي بحدث لكل كلمة / Arabic ASS karaoke, one event per word (proven)
- `SYNC-28` سبعة ستايلات ترجمة جاهزة / Seven named caption styles (proven)

### `SYNC-27` — كاريوكي ASS عربي بحدث لكل كلمة / Arabic ASS karaoke, one event per word

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ترجمة محروقة يتلون فيها المنطوق وينبض، بحدث ASS لكل كلمة فيبقى التشكيل والترتيب سليمين. / Burned captions where the spoken word changes colour and pops, one ASS event per word so shaping and order stay intact.

**متى:** حين يطلب المستخدم ترجمة عربية محروقة كاريوكي تتلون فيها الكلمة المنطوقة وتنبض / when burned Arabic karaoke captions should colour and pop the spoken word

**كيف:** python montage.py captions VIDEO --spec caps.json --style reels\|cinema\|punchy\|tiktok\|hormozi\|boxed\|minimal (also inside cut/voicecut/reel). One Dialogue per word: {\1c<hi>\fscx112\fscy112\t(0,120,\fscx100\fscy100)}word; Encoding −1 (auto paragraph direction), WrapStyle 2, side margins 6% W, ≤ 6 words on screen, sizes scale with the short side; burn ass=caps.ass with fontsdir= (no Arabic system fonts here), crf 17, audio copied. Ran here: test_montage_cuts_on_the_beat_and_captions_shape_arabic ok (see ARAB-62 for the order check).

**المعاملات:** pop 112%→100% / 120 ms; ≤ 6 words; Encoding −1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كاريوكي · ass · libass · burn · arabic captions · karaoke · ترجمة محروقة · تلوين الكلمة · ريلز · burned subtitles · word highlight

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

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-studio/motion/montage.py:353`
- `kosif-studio/motion/montage.py:381`
- `kosif-studio/tests/test_studio.py:765`

#### 7. قدرات قريبة في العائلة

- `SYNC-25` لا تغيّر كلام المتحدث، والحرق عند الطلب / Verbatim words; burn only when asked (documented)
- `SYNC-26` إبراز تلقائي للكلمات المهمة / Automatic emphasis words (ready)
- `SYNC-28` سبعة ستايلات ترجمة جاهزة / Seven named caption styles (proven)
- `SYNC-29` صفحات ترجمة + SRT/VTT/ASS / Caption pages → JSON/SRT/VTT/ASS (proven)

### `SYNC-28` — سبعة ستايلات ترجمة جاهزة / Seven named caption styles

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** reels وcinema وpunchy وtiktok وhormozi وboxed وminimal بخطوط Noto العربية وألوان وأحجام مضبوطة. / reels, cinema, punchy, tiktok, hormozi, boxed and minimal with Noto Arabic faces, colours and sizes tuned.

**متى:** عند اختيار ستايل ترجمة جاهز للريلز أو تيك توك أو السينما بدل تصميمه من الصفر / when a ready caption preset (reels, tiktok, cinema…) is wanted instead of designing one

**كيف:** montage.ass(spec, 1080, 1920, style); colours are ASS &HAABBGGRR; sizes per 1080 px of the short side, margins per 1920 of height. Ran here: tests.test_v6 StyleAndRegistryTests.test_caption_styles ok. Table below.

**المعاملات:** see the style table

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ستايلات · reels · tiktok · hormozi · cinema · caption presets · شكل الترجمة · قوالب ترجمة · ترجمة جاهزة · punchy · minimal

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/montage.py:308`
- `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:170`
- `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:13`

#### 7. قدرات قريبة في العائلة

- `SYNC-26` إبراز تلقائي للكلمات المهمة / Automatic emphasis words (ready)
- `SYNC-27` كاريوكي ASS عربي بحدث لكل كلمة / Arabic ASS karaoke, one event per word (proven)
- `SYNC-29` صفحات ترجمة + SRT/VTT/ASS / Caption pages → JSON/SRT/VTT/ASS (proven)
- `SYNC-30` معايرة حجم ASS / ASS PlayRes calibration (documented)

### `SYNC-29` — صفحات ترجمة + SRT/VTT/ASS / Caption pages → JSON/SRT/VTT/ASS

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يحوّل كلمات Whisper أو SRT إلى صفحات ~1200 ms ويكتب JSON وSRT وVTT وASS كاريوكي. / Turns Whisper word stamps (or SRT) into ~1200 ms pages and writes JSON, SRT, VTT and ASS karaoke.

**متى:** حين نريد تحويل كلمات Whisper أو SRT إلى صفحات ترجمة وملفات SRT وVTT وASS / when Whisper word stamps or SRT must become caption pages plus JSON, SRT, VTT and ASS

**كيف:** python captions_pages.py words.json --page-ms 1200 --max-chars 42 --rtl --out captions. Ran here: 6 Arabic words → 2 pages, 4 files. Caveat found here: it expects [{text,start,end}] — a KOSIF words.json ({word,…}) raises KeyError 'text'; rename the key first. Its ASS uses \k per page; for burned Arabic prefer one event per word (SYNC-27).

**المعاملات:** 42 chars, 2 lines, 1–7 s per page

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صفحات · srt · vtt · ass · caption pages · tiktok pages · تصدير الترجمة · ملفات ترجمة · كاريوكي · json · whisper

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `100-superskills/skills/audio-reactive-captions-studio/scripts/captions_pages.py:95`
- `100-superskills/skills/audio-reactive-captions-studio/references/captions-rules.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-27` كاريوكي ASS عربي بحدث لكل كلمة / Arabic ASS karaoke, one event per word (proven)
- `SYNC-28` سبعة ستايلات ترجمة جاهزة / Seven named caption styles (proven)
- `SYNC-30` معايرة حجم ASS / ASS PlayRes calibration (documented)
- `SYNC-31` كاريوكي \k بشرائح متساوية / Even-slice \k karaoke (omni) (ready)

### `SYNC-30` — معايرة حجم ASS / ASS PlayRes calibration

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** دقة السكربت الافتراضية في SRT/libass تغيّر الحجم والهامش؛ عاير على إطارات 1080×1920 حقيقية. / libass's default script resolution rescales FontSize and MarginV; calibrate on real 1080×1920 frames.

**متى:** حين يظهر حجم الترجمة المحروقة أو هامشها خاطئا في فيديو 1080×1920 / when burned ASS/SRT font size or margins come out wrong on real frames

**كيف:** Set PlayResX/PlayResY = the frame; preview frames before the full burn; smaller white Arabic with black outline/shadow, bottom safe zone, no opaque box. Quick SRT burn: subtitles=captions.srt:force_style='FontName=Cairo,FontSize=22,Outline=2,MarginV=60' (sizes relative to the 384×288 default).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** playres · ass · calibration · font size · حجم الخط · هامش الترجمة · ترجمة محروقة · libass · margin

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-studio/motion/references/voice-open-footage-upgrade-2026-10-10.md`
- `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-28` سبعة ستايلات ترجمة جاهزة / Seven named caption styles (proven)
- `SYNC-29` صفحات ترجمة + SRT/VTT/ASS / Caption pages → JSON/SRT/VTT/ASS (proven)
- `SYNC-31` كاريوكي \k بشرائح متساوية / Even-slice \k karaoke (omni) (ready)
- `SYNC-32` دخول الكلمة على بداية نطقها / Word enters on its spoken start (proven)

### `SYNC-31` — كاريوكي \k بشرائح متساوية / Even-slice \k karaoke (omni)

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ستايلات tiktok/cinema/punchy تقسم الزمن بالتساوي بين الكلمات — شكل كاريوكي لا تزامن حقيقي. / tiktok/cinema/punchy styles split time evenly between words — a karaoke look, not true sync.

**متى:** عند استخدام ستايلات tiktok أو cinema أو punchy كشكل كاريوكي بزمن موزع بالتساوي / when a karaoke look with evenly split word time is acceptable

**كيف:** python scripts/smart_montage.py captions video.mp4 --spec captions.json --style tiktok (Cairo 68, outline 6, MarginV 280); \k per word = max(10 cs, duration/len(words)). Feed words.json times for real sync; label even-split timing as estimated.

**المعاملات:** \k ≥ 10 cs

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** k karaoke · even split · omni · estimated timing · كاريوكي · تقسيم متساو · ترجمة محروقة · tiktok · smart_montage

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/smart_montage.py:91`

#### 7. قدرات قريبة في العائلة

- `SYNC-29` صفحات ترجمة + SRT/VTT/ASS / Caption pages → JSON/SRT/VTT/ASS (proven)
- `SYNC-30` معايرة حجم ASS / ASS PlayRes calibration (documented)
- `SYNC-32` دخول الكلمة على بداية نطقها / Word enters on its spoken start (proven)
- `SYNC-33` تعبئة كاريوكي من اليمين بقناع كامل الكلمة / RTL karaoke fill with whole-word clip-path (proven)

### `SYNC-32` — دخول الكلمة على بداية نطقها / Word enters on its spoken start

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل كلمة تُكشف بقناع ناعم من اليمين مع صعود نابض وضباب يتلاشى، فتظهر في أول إطار بعد بداية نطقها. / Each word reveals through a soft right-to-left mask with a spring rise and de-blur, visible on the first frame at or after its start.

**متى:** حين نريد كلمات عربية تظهر بقناع ناعم من اليمين لحظة نطقها / when each word should reveal through a soft right-to-left mask exactly as it is spoken

**كيف:** Per word from words.json: mask wipe 0.42 s RTL over the whole word (never letters), spring rise 34 px (k = 180, c = 19), blur 9 → 0 px, opacity floor 12% so it shows on its first frame; key words turn gold #ffc56e with 28/70 px glow and an inOutCubic underline over the spoken length; finished sentences dim to 30% (keys 78%). Proof film: max \|Δ\| 33 ms, 0 early.

**المعاملات:** mask 0.42 s; rise 34 px; spring 180/19

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** دخول الكلمة · word reveal · mask wipe · kinetic captions · rtl · ظهور الكلمات · كتابة متحركة · تايبوغرافي · spring · kinetic typography

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/index.html`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-30` معايرة حجم ASS / ASS PlayRes calibration (documented)
- `SYNC-31` كاريوكي \k بشرائح متساوية / Even-slice \k karaoke (omni) (ready)
- `SYNC-33` تعبئة كاريوكي من اليمين بقناع كامل الكلمة / RTL karaoke fill with whole-word clip-path (proven)
- `SYNC-34` كاريوكي الكبسولة في starter الكانفس / Canvas karaoke pill (html-canvas starter) (proven)

### `SYNC-33` — تعبئة كاريوكي من اليمين بقناع كامل الكلمة / RTL karaoke fill with whole-word clip-path

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل كلمة تمتلئ بالذهبي من اليمين إلى اليسار عبر clip-path يغطي الكلمة كلها فلا تنفصل الحروف. / Each word fills gold right-to-left through a whole-word clip-path so joined letters never split.

**متى:** حين نريد تعبئة كل كلمة عربية بالذهبي من اليمين أثناء نطقها دون فصل الحروف / when Arabic words should fill gold right-to-left while spoken, letters kept joined

**كيف:** Cairo 800 at 60 px; clip-path inset animates across the word's spoken duration; the old line leaves 0.02 s after its last word and the next arrives 0.2 s before its first word, so two lines never overlap. Measured: every fill starts ≤ 35 ms after the spoken start. Caveat: the reveal edge may pass mid-word (letters stay joined).

**المعاملات:** line out +0.02 s; next in −0.2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كاريوكي · تعبئة · clip-path · rtl karaoke · fill · ذهبي · تلوين الكلمة · حروف متصلة · word fill · arabic karaoke

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/audio-reactive-spectrum/index.html`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/audio-reactive-spectrum/README.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-31` كاريوكي \k بشرائح متساوية / Even-slice \k karaoke (omni) (ready)
- `SYNC-32` دخول الكلمة على بداية نطقها / Word enters on its spoken start (proven)
- `SYNC-34` كاريوكي الكبسولة في starter الكانفس / Canvas karaoke pill (html-canvas starter) (proven)
- `SYNC-35` ترجمة Remotion بالكلمة مع كشف الاتجاه / Remotion word captions with bidi detection (install)

### `SYNC-34` — كاريوكي الكبسولة في starter الكانفس / Canvas karaoke pill (html-canvas starter)

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الجملة كاملة ظاهرة، والكلمة الحالية كبسولة فيروزية بنص داكن تنبض، والمنطوق أبيض والقادم باهت. / The whole phrase shows; the current word becomes a teal pill with dark text and a pop, past words white, future muted.

**متى:** عند الحاجة لترجمة كاريوكي في starter الكانفس تبرز الكلمة الحالية بكبسولة ملونة / when the html-canvas starter needs karaoke with the current word in a pill

**كيف:** phrases(words, 0.45) splits at pauses > 0.45 s; show from start − 0.15 to end + 0.5 with a 0.15/0.3 fade window; pop outBack 0.96 → 1.08 over 140 ms. Rendered in the scaffolded starter through render_html.cjs.

**المعاملات:** 64 px 700; pill r 22 pad 6×18; on #7ee8d2 text #0b1020; done #f3f7ff; upcoming #9fb0cc; bottom 210 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كبسولة · karaoke pill · canvas · starter · كاريوكي · إبراز الكلمة الحالية · ترجمة متحركة · html canvas · pill highlight

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-tool/starters/html-canvas/index.html:181`
- `kosif-tool/starters/html-canvas/timeline.js:82`

#### 7. قدرات قريبة في العائلة

- `SYNC-32` دخول الكلمة على بداية نطقها / Word enters on its spoken start (proven)
- `SYNC-33` تعبئة كاريوكي من اليمين بقناع كامل الكلمة / RTL karaoke fill with whole-word clip-path (proven)
- `SYNC-35` ترجمة Remotion بالكلمة مع كشف الاتجاه / Remotion word captions with bidi detection (install)
- `SYNC-36` كلمات على مقاطعها مع كلمات ذهبية / Syllable-timed speech captions with gold keywords (ready)

### `SYNC-35` — ترجمة Remotion بالكلمة مع كشف الاتجاه / Remotion word captions with bidi detection

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | Remotion برخصة الشركة؛ @remotion/captions نفسها MIT / Remotion company license; @remotion/captions itself is MIT. |

**ما هي:** يحمّل words.json ويجمعها في بطاقات (≤ 4 كلمات أو صمت > 0.6 ث)، يظهرها مبكرًا 0.15 ث، والكلمة النشطة تنبض 1.1×؛ الاتجاه من أول حرف قوي. / Loads words.json, groups cards (≤ 4 words or > 0.6 s silence), shows them 0.15 s early, springs the active word to 1.1×; direction from the first strong character.

**متى:** حين يحتاج مشروع Remotion ترجمة بالكلمة من words.json مع اتجاه عربي أو إنجليزي تلقائي / when a Remotion project needs word captions from words.json with automatic text direction

**كيف:** <Captions accent lang file maxWordsPerLine={4} gapSeconds={0.6} holdSeconds={0.35} leadSeconds={0.15}/>; spring damping 12, stiffness 220, mass .7; upcoming words 42% opacity. TikTok pages alternative: @remotion/captions createTikTokStyleCaptions (1200 ms) with the active token #39E508. SyncedLine: whole words spring in at start − 0.06 s.

**المعاملات:** 58 px 700 on rgba(8,10,16,.66) r 30; bottom 260 px

**التثبيت:** cd kosif-tool/starters/remotion && npm install

**الوسوم:** ريموشن · remotion captions · bidi · tiktok pages · ترجمة بالكلمة · اتجاه النص · عربي وإنجليزي · rtl · word captions

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-tool/starters/remotion/src/Captions.tsx:135`
- `kosif-tool/starters/remotion/src/Captions.tsx:39`
- `kosif-tool/playbooks/kinetic-type.md:57-75`

#### 7. قدرات قريبة في العائلة

- `SYNC-33` تعبئة كاريوكي من اليمين بقناع كامل الكلمة / RTL karaoke fill with whole-word clip-path (proven)
- `SYNC-34` كاريوكي الكبسولة في starter الكانفس / Canvas karaoke pill (html-canvas starter) (proven)
- `SYNC-36` كلمات على مقاطعها مع كلمات ذهبية / Syllable-timed speech captions with gold keywords (ready)
- `SYNC-37` سطر شبحي يضيء كلمة بكلمة / Ghost-to-lit line (seen)

### `SYNC-36` — كلمات على مقاطعها مع كلمات ذهبية / Syllable-timed speech captions with gold keywords

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل كلمة تصعد من ضبابية على زمنها، والكلمات المفتاحية بلون التمييز، والعبارة تخرج للأعلى قبل التالية. / Each word rises from blur on its own time, keywords in the accent colour, and the phrase exits upward before the next.

**متى:** عند كتابة ترجمة كلام تصعد كل كلمة فيها من ضبابية على زمنها مع كلمات مفتاحية ملونة / when speech captions should rise word by word from blur, with accent keywords

**كيف:** speech(el, [[word, t], …], accentWords): each word in a .wm clip-path mask; fromTo y 18 → 0, blur 6 → 0, 0.28 s power3.out at t − 0.04; exit opacity 0, y −14 in 0.22 s power3.in. Hand-corrected variant: phrases with <b>keyword</b> in gold #f5c97a, yPercent 105 → 0 in 0.32 s, out at next start − 0.16 s.

**المعاملات:** rise 18 px, blur 6 px, 0.28 s, lead 0.04 s; accent #E7B65A

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مقاطع · syllable · speech captions · gold keyword · mask · كلمات ذهبية · ضبابية · ظهور الكلمات · blur reveal · keyword color

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:171`
- `100-superskills/skills/kosif-montage-motion/templates/directed.html:73`
- `kosif-one/projects/whatsapp-motion/projects/success/index.html:156-205`

#### 7. قدرات قريبة في العائلة

- `SYNC-34` كاريوكي الكبسولة في starter الكانفس / Canvas karaoke pill (html-canvas starter) (proven)
- `SYNC-35` ترجمة Remotion بالكلمة مع كشف الاتجاه / Remotion word captions with bidi detection (install)
- `SYNC-37` سطر شبحي يضيء كلمة بكلمة / Ghost-to-lit line (seen)
- `SYNC-38` صندوق ينتقل للكلمة النشطة / Word-hop highlight box (seen)

### `SYNC-37` — سطر شبحي يضيء كلمة بكلمة / Ghost-to-lit line

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** السطر كاملًا بشفافية 25% أو رمادي، وكل كلمة ترتفع إلى 100% أو تبيضّ عند زمنها. / The whole line at 25% opacity (or grey); each word lifts to 100% (or white) at its time.

**متى:** حين نريد عرض السطر كاملا باهتا ثم إضاءة كل كلمة عند نطقها / when the whole line shows faded and each word lights up as it is spoken

**كيف:** Grey #555 → white (emphasis orange #f27525) with a 120 ms fade; or 25% → 100% in 150–200 ms; ≤ 2 lines; never split letters. Peach rounded highlight box on the target word (80 ms colour transition, padding 2×6 px) for language-learning looks.

**المعاملات:** fade 120–200 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شبحي · ghost caption · lit words · whiteboard · سطر باهت · إضاءة الكلمات · تعلم اللغة · language learning · fade highlight

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `style:plotter`
- `style:doodle`
- `style:pm-1stnoel-c20a89`

#### 7. قدرات قريبة في العائلة

- `SYNC-35` ترجمة Remotion بالكلمة مع كشف الاتجاه / Remotion word captions with bidi detection (install)
- `SYNC-36` كلمات على مقاطعها مع كلمات ذهبية / Syllable-timed speech captions with gold keywords (ready)
- `SYNC-38` صندوق ينتقل للكلمة النشطة / Word-hop highlight box (seen)
- `SYNC-39` ترجمة تُكتب لحظة النطق / Voice-timed typewriter captions (seen)

### `SYNC-38` — صندوق ينتقل للكلمة النشطة / Word-hop highlight box

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صندوق مستدير بلون العلامة ينزلق إلى الكلمة المنطوقة. / A rounded brand-coloured box slides to the spoken word.

**متى:** حين نريد صندوقا بلون العلامة ينتقل إلى الكلمة المنطوقة في الترجمة / when a brand-coloured box should slide to each spoken word

**كيف:** Box padding 6 px, slide 80 ms from words.json; TikTok-style red box #ff1745 in 0.08–0.16 s (HyperFrames caption-highlight); colour-only variant for calm content.

**المعاملات:** slide 80 ms; pad 6 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صندوق · highlight box · word hop · tiktok · تمييز الكلمة · خلفية الكلمة · هايلايت · brand color · active word

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `style:pm-gautam-mer1-2ae354`
- `kosif-one/vendor/hyperframes/registry/components/caption-highlight/caption-highlight.html`

#### 7. قدرات قريبة في العائلة

- `SYNC-36` كلمات على مقاطعها مع كلمات ذهبية / Syllable-timed speech captions with gold keywords (ready)
- `SYNC-37` سطر شبحي يضيء كلمة بكلمة / Ghost-to-lit line (seen)
- `SYNC-39` ترجمة تُكتب لحظة النطق / Voice-timed typewriter captions (seen)
- `SYNC-40` عداد كلمة مفتاحية ودائرة على الكلمة / Keyword counter & on-word annotations (seen)

### `SYNC-39` — ترجمة تُكتب لحظة النطق / Voice-timed typewriter captions

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حروف كل كلمة تُكتب بدءًا من بداية نطقها وموزعة على مدتها، بمؤشر رفيع. / Each word's letters type from its spoken start, spread over its duration, with a thin caret.

**متى:** حين نريد ترجمة تكتب حرفا حرفا لحظة نطق كل كلمة / when caption letters should type out over each word's spoken duration

**كيف:** Letters ~30–50 ms each within [start, end]; caret 2 px; omit full stops; box variant: mono lowercase typed 35 ms/char into a solid orange/yellow box with an underscore cursor. For Arabic type by grapheme clusters (Intl.Segmenter), never by code unit.

**المعاملات:** 30–50 ms/letter

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** آلة كاتبة · typewriter captions · voice timed · كتابة حرف حرف · مؤشر كتابة · ترجمة متزامنة · typing effect · caret

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `style:pm-rossaxbt-3085b7`
- `style:pm-gizakdag-b8c59e`

#### 7. قدرات قريبة في العائلة

- `SYNC-37` سطر شبحي يضيء كلمة بكلمة / Ghost-to-lit line (seen)
- `SYNC-38` صندوق ينتقل للكلمة النشطة / Word-hop highlight box (seen)
- `SYNC-40` عداد كلمة مفتاحية ودائرة على الكلمة / Keyword counter & on-word annotations (seen)
- `SYNC-41` مكوّنات ترجمة HyperFrames / HyperFrames caption components (install)

### `SYNC-40` — عداد كلمة مفتاحية ودائرة على الكلمة / Keyword counter & on-word annotations

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل ظهور لكلمة مفتاحية يزيد عدادًا بنبضة، أو دائرة/خط يُرسم لحظة نطقها. / Each occurrence of a keyword bumps a counter with a pop, or a circle/underline draws at its spoken onset.

**متى:** حين نريد عدادا يزيد مع كل تكرار لكلمة مفتاحية أو دائرة ترسم عند نطقها / when a keyword's occurrences bump a counter or a circle draws as it is spoken

**كيف:** Counter chip top-right, pop 1 → 1.25 → 1 in 200 ms at word.start; annotation: interpolate start frame = word.start × fps, draw 12–20 frames, hold to phrase end. Stressed-word variant: 1–3 words at a time, stressed word lime #d4ff3a at 1.4×.

**المعاملات:** pop 200 ms; draw 12–20 frames

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عداد · دائرة · keyword counter · annotation · underline · تكرار الكلمة · خط تحت الكلمة · تعليق توضيحي · circle draw · word count

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `style:pm-sab8a-364a5a`
- `kosif-atlas/skills/2712-remotion/10436-remotion-markup/text-highlights.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-38` صندوق ينتقل للكلمة النشطة / Word-hop highlight box (seen)
- `SYNC-39` ترجمة تُكتب لحظة النطق / Voice-timed typewriter captions (seen)
- `SYNC-41` مكوّنات ترجمة HyperFrames / HyperFrames caption components (install)
- `SYNC-42` ترجمة مدمجة: شريط وكلمة ذروة خلف المتحدث / Embedded captions: rail + peak word behind the subject (install)

### `SYNC-41` — مكوّنات ترجمة HyperFrames / HyperFrames caption components

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames Apache-2.0؛ تحمّل GSAP (رخصة GSAP القياسية، ليست MIT) وخطوط Google / HyperFrames Apache-2.0; loads GSAP (standard license, not MIT) and Google Fonts. |

**ما هي:** 17 معالجة ترجمة جاهزة (كبسولة كاريوكي، صدمة كلمة، نيون، غليتش، تدرج، خامة، خلف الشخص…) تقبل مصفوفة كلمات. / 17 ready caption treatments (pill karaoke, kinetic slam, neon, glitch, gradient, texture, behind-subject…) that accept a word array.

**متى:** عند اختيار معالجة ترجمة جاهزة مثل نيون أو غليتش أو كاريوكي في HyperFrames / when a ready HyperFrames caption treatment (neon, glitch, pill karaoke…) fits

**كيف:** 15 of 17 keep an inline TRANSCRIPT/WORDS array [{text,start,end}] — replace it with your words.json (keep data-duration = audio length, 30 fps). blend-difference and camera-follow use internal timing. Latin display fonts (Anton, Montserrat, Poppins…) — swap to Arabic faces and test shaping before use. Table below.

**التثبيت:** npx hyperframes add caption-pill-karaoke

**الوسوم:** hyperframes · caption components · karaoke · kinetic slam · neon captions · قوالب ترجمة · ترجمة نيون · غليتش · glitch · caption treatments

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-one/vendor/hyperframes/registry/components/caption-pill-karaoke/caption-pill-karaoke.html:153`
- `kosif-one/vendor/hyperframes/skills/hyperframes-registry/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-39` ترجمة تُكتب لحظة النطق / Voice-timed typewriter captions (seen)
- `SYNC-40` عداد كلمة مفتاحية ودائرة على الكلمة / Keyword counter & on-word annotations (seen)
- `SYNC-42` ترجمة مدمجة: شريط وكلمة ذروة خلف المتحدث / Embedded captions: rail + peak word behind the subject (install)
- `SYNC-43` الأشرطة السفلية / Lower thirds (install)

### `SYNC-42` — ترجمة مدمجة: شريط وكلمة ذروة خلف المتحدث / Embedded captions: rail + peak word behind the subject

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames Apache-2.0؛ تحمّل GSAP (رخصة GSAP القياسية، ليست MIT) وخطوط Google / HyperFrames Apache-2.0; loads GSAP (standard license, not MIT) and Google Fonts. |

**ما هي:** مقطع متحدث كما هو: شريط حرفي في الأمام، وكلمة ذروة نادرة خلف المتحدث عبر قناع. / An untouched talking clip: a verbatim rail in front and a scarce peak word composited behind the subject via a matte.

**متى:** حين نريد ترجمة لمقطع متحدث مع كلمة ذروة تظهر خلف الشخص عبر قناع / when a talking clip needs a verbatim caption rail plus a peak word behind the speaker

**كيف:** Decision gate → pick ONE of 35 identities (10 DNA + 25 themes; default 'anchor') → hyperframes init → prepare.sh (matte, transcribe, 50 ms audio envelope, safe zones) → theme.json or cinematic.json → preview-frames → render. ≤ 1 hero per thought block, ≥ 0.6 s air between heroes. Themes worth knowing: anchor (calm), stardust (poetic), chalkboard, dossier, neonsign, inkwater. Needs the HyperFrames toolchain + matte model.

**المعاملات:** 35 identities; hero gap ≥ 0.6 s

**التثبيت:** npx hyperframes init && bash scripts/prepare.sh <project>

**الوسوم:** مدمجة · embedded captions · behind subject · themes · podcast · خلف الشخص · مقطع متحدث · كلمة بارزة · matte · talking head

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-one/vendor/hyperframes/skills/embedded-captions/SKILL.md`
- `kosif-one/vendor/hyperframes/skills/embedded-captions/CATALOG.md`
- `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/make-theme.cjs`

#### 7. قدرات قريبة في العائلة

- `SYNC-40` عداد كلمة مفتاحية ودائرة على الكلمة / Keyword counter & on-word annotations (seen)
- `SYNC-41` مكوّنات ترجمة HyperFrames / HyperFrames caption components (install)
- `SYNC-43` الأشرطة السفلية / Lower thirds (install)
- `SYNC-44` ستايلات وحركات ترجمة بصمة / Basma caption presets, animations & highlight modes (install)

### `SYNC-43` — الأشرطة السفلية / Lower thirds

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames Apache-2.0؛ تحمّل GSAP (رخصة GSAP القياسية، ليست MIT) وخطوط Google / HyperFrames Apache-2.0; loads GSAP (standard license, not MIT) and Google Fonts. |

**ما هي:** 13 شريطًا سفليًا جاهزًا للأسماء والألقاب (بطاقة داكنة، كتلة لون، خط جانبي، كبسولة، إطار نيون، شريط أخبار…). / 13 ready name/title lower thirds (dark card, colour block, side rule, pill, neon border, news ticker…).

**متى:** حين نحتاج شريطا سفليا لاسم المتحدث ولقبه أو شريط أخبار / when a speaker's name and title need a lower third or a news ticker

**كيف:** npx hyperframes add lt-dark-card (or lt-clean-bar, lt-side-rule, lt-soft-pill, lt-neon-border, news-ticker…), 4.8 s each at 1920×1080. Arabic: mirror the layout (accent bar on the right, text right-aligned) and swap Oswald/Montserrat for Arabic faces. Speaker-coloured subtitles: tiny caps name in the character colour above the line.

**المعاملات:** 4.8 s

**التثبيت:** npx hyperframes add lt-dark-card

**الوسوم:** شريط سفلي · lower third · name tag · news ticker · اسم المتحدث · تعريف الضيف · لقب · title bar · name strap

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-one/vendor/hyperframes/registry/blocks/lt-dark-card/lt-dark-card.html`
- `kosif-one/vendor/hyperframes/registry/blocks/news-ticker/news-ticker.html`

#### 7. قدرات قريبة في العائلة

- `SYNC-41` مكوّنات ترجمة HyperFrames / HyperFrames caption components (install)
- `SYNC-42` ترجمة مدمجة: شريط وكلمة ذروة خلف المتحدث / Embedded captions: rail + peak word behind the subject (install)
- `SYNC-44` ستايلات وحركات ترجمة بصمة / Basma caption presets, animations & highlight modes (install)
- `SYNC-45` فيلم كلمات من صوت (أغنية، شعر، دعاء) / Verse film from sound (proven)

### `SYNC-44` — ستايلات وحركات ترجمة بصمة / Basma caption presets, animations & highlight modes

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 12 حركة لكل كلمة، 5 طرق إبراز، و7+5 ستايلات عربية جاهزة بأحجام نسبية. / 12 per-word animations, 5 highlight modes and 7 + 5 ready Arabic presets with relative sizes.

**متى:** عند اختيار حركة أو طريقة إبراز أو ستايل عربي جاهز للترجمة في بصمة / when choosing per-word animations, highlight modes or Arabic caption presets in Basma

**كيف:** Animations: pop, spring, stomp, mask, rise, karaoke, cascade, blur, wave, glitch, fade, slide. Highlights: box, color, underline, glow, none. Presets: ريلز (Noto Sans Arabic 7, chunk 6, #ffde59), سينما, قوي, تيك توك, كلمة واحدة, صندوق, هادئ; AutoEdit: cinema (Reem Kufi), trend (Lalezar, box), karaoke (Changa), neon (Rubik, glow), minimal (IBM Plex Sans Arabic). Sizes 5–14% of the short side; chunk 1–6; stroke 0–12.

**المعاملات:** size 5–14% short side; chunk 1–6

**التثبيت:** cd app && npm install

**الوسوم:** بصمة · basma · caption presets · arabic captions · حركات الترجمة · ستايل ترجمة · إبراز الكلمة · highlight modes · word animation

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `app/public/js/00_editor.js:347`
- `app/public/js/00_editor.js:2352`
- `app/public/js/50_autoedit.js:835`

#### 7. قدرات قريبة في العائلة

- `SYNC-42` ترجمة مدمجة: شريط وكلمة ذروة خلف المتحدث / Embedded captions: rail + peak word behind the subject (install)
- `SYNC-43` الأشرطة السفلية / Lower thirds (install)
- `SYNC-45` فيلم كلمات من صوت (أغنية، شعر، دعاء) / Verse film from sound (proven)
- `SYNC-46` Voice2Motion: موشن بالمعنى من الصوت / Voice2Motion semantic scenes (proven)

### `SYNC-45` — فيلم كلمات من صوت (أغنية، شعر، دعاء) / Verse film from sound

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فيلم تايبوغرافي حركي من أغنية أو قصيدة أو دعاء: الكلمات على أزمنتها، كلمة مفتاحية لكل سطر، ذروة، وضوء يقوده الصوت. / A kinetic-typography film from a song, poem or dua: words on their sung times, one keyword per line, a payoff and light driven by the sound.

**متى:** حين يريد المستخدم فيلم كلمات متحركة من أغنية أو قصيدة أو دعاء على توقيت الصوت / when the user wants a kinetic-typography film from a song, poem or dua audio

**كيف:** python verse.py AUDIO --name NAME [--text lyrics.txt \| --words X.words.json] [--title --mood night\|dawn\|gold\|sea\|ink --accent '#E7B65A' --images a.jpg … --music none --fix … --render]; sections at pauses ≥ 3 s, interludes ≥ 4.5 s with a breathing eight-point rosette; line size 124/104/88/74 px for ≤ 14/24/36/more chars; payoff ×1.22 held +2.2 s; words rise 30·k px from blur 9 in 0.42 s; keyword pulse 1.07 yoyo 0.18 s. Ran here: verse tests ok (test_studio + test_directors). Needs faster-whisper unless --words is given.

**المعاملات:** moods night/dawn/gold/sea/ink; line ≤ 7 words

**التثبيت:** pip install faster-whisper # models from huggingface.co (reachable): small 466 MB, large-v3 3.1 GB

**الوسوم:** فيلم كلمات · دعاء · قصيدة · lyric video · verse · poem · أغنية · كلمات متحركة · تايبوغرافي · song · kinetic typography

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `network` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-studio/motion/verse.py:246`
- `kosif-studio/motion/verse.py:394`
- `100-superskills/skills/kosif-montage-motion/templates/verse.html:62`
- `kosif-studio/tests/test_studio.py:943`

#### 7. قدرات قريبة في العائلة

- `SYNC-43` الأشرطة السفلية / Lower thirds (install)
- `SYNC-44` ستايلات وحركات ترجمة بصمة / Basma caption presets, animations & highlight modes (install)
- `SYNC-46` Voice2Motion: موشن بالمعنى من الصوت / Voice2Motion semantic scenes (proven)
- `SYNC-47` إخراج تلقائي لمقطع متكلم / Editor-style auto direction of a talking clip (proven)

### `SYNC-46` — Voice2Motion: موشن بالمعنى من الصوت / Voice2Motion semantic scenes

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل جملة تُصنف (طقس، زحام، دعم، استرداد، عام) وتُرسم كمشهد متحرك خاص بها يتفاعل مع غلاف الصوت، والأرقام من نص الجملة. / Each sentence is classified (weather, traffic, support, refund, generic) and drawn as its own animated scene reacting to the voice envelope, numbers taken from the cue text.

**متى:** حين يرسل المستخدم صوتا ويريد مشاهد موشن تعبر عن معنى كل جملة / when a voice recording should become animated scenes matching each sentence's meaning

**كيف:** python audio2motion.py AUDIO --cues cues.json \| --transcript t.txt [--out X.mp4 --fps 24 --size 540x960 --plan-only]; envelope 50 Hz from 8 kHz mono; 23 speech-energy bars; caption ease smoothstep 0.37 s; refuses empty transcripts and never claims ASR timing (estimated cues are labelled). Ran here: tests.test_audio2motion 8/8 ok. Owner's run: 29.4 s / 706 frames rendered in 10 s.

**المعاملات:** fps 12–60; ≤ 1920×1080; palette cyan (64,222,232), gold (255,196,79)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** voice2motion · صوت إلى موشن · voice note · semantic scenes · infographic · رسالة صوتية · موشن جرافيك · مشاهد متحركة · audio to video · animated scenes

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-studio/motion/audio2motion.py:80`
- `kosif-studio/motion/audio2motion.py:210`
- `kosif-studio/tests/test_audio2motion.py`

#### 7. قدرات قريبة في العائلة

- `SYNC-44` ستايلات وحركات ترجمة بصمة / Basma caption presets, animations & highlight modes (install)
- `SYNC-45` فيلم كلمات من صوت (أغنية، شعر، دعاء) / Verse film from sound (proven)
- `SYNC-47` إخراج تلقائي لمقطع متكلم / Editor-style auto direction of a talking clip (proven)
- `SYNC-48` الريل التلقائي من الكلام / Automatic talking-clip reel (ready)

### `SYNC-47` — إخراج تلقائي لمقطع متكلم / Editor-style auto direction of a talking clip

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** من توقيت الكلمات وصناديق الوجه يختار المخطط سطر الذروة، والكلمات المفتاحية بالتركيز الطرفي، وموتيف رقم متكرر، وكلمات الفصول، ومواضع آمنة من الوجه. / From word timings and face boxes the planner picks the payoff line, end-focus keywords, a number-ring motif, chapter words and face-safe placements.

**متى:** حين نريد إخراجا تلقائيا لمقطع متحدث يختار الذروة والكلمات المفتاحية ومواضع آمنة من الوجه / when a talking clip should be auto-directed: payoff line, keywords and face-safe captions

**كيف:** direct.plan(segs, shots, stress, W, H, dur) → {payoff, keys, motifs, captions, chapters}; never a filler, never the unit after a number; apply_fixes for dialect. kmotion direct CLIP --name … → edit.js → directed.html. Ran here: tests.test_directors ok.

**المعاملات:** punch expo.out 0.14 s; caption 54 px; keyword 200 px; chapter 380 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إخراج تلقائي · directed edit · talking clip · payoff · keywords · مقطع متحدث · مونتاج تلقائي · الفصول · face safe · chapters

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `100-superskills/skills/kosif-montage-motion/tests/test_directors.py:10`
- `kosif-studio/motion/templates/directed.html`

#### 7. قدرات قريبة في العائلة

- `SYNC-45` فيلم كلمات من صوت (أغنية، شعر، دعاء) / Verse film from sound (proven)
- `SYNC-46` Voice2Motion: موشن بالمعنى من الصوت / Voice2Motion semantic scenes (proven)
- `SYNC-48` الريل التلقائي من الكلام / Automatic talking-clip reel (ready)
- `SYNC-49` إيقاع التلاوة والدعاء / Recitation & dua pacing (documented)

### `SYNC-48` — الريل التلقائي من الكلام / Automatic talking-clip reel

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كلمات ← مسح ترجمة ← ترميم 1080×1920 ← صوت ← موسيقى عند الحاجة ← كاريوكي ← −14 LUFS ← بوابة. / words → decaption → restore 1080×1920 → voice → music only if none → karaoke → −14 LUFS → gate.

**متى:** حين يعطي المستخدم مقطع كلام ويريد ريلا عموديا جاهزا بترجمة كاريوكي / when a talking clip should become a finished 1080×1920 reel with karaoke captions

**كيف:** python scripts/kmotion.py reel CLIP.mp4 --out FINAL.mp4 [--transcript X.words.json --no-decaption --credit '@x' --model auto --style reels]. Without faster-whisper pass --transcript. See FOOT for the restoration chain.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ريل · reel · auto captions · talking clip · ريلز · فيديو عمودي · مسح الترجمة · decaption · vertical reel

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/reel.py`
- `kosif-studio/motion/reel.py:92`

#### 7. قدرات قريبة في العائلة

- `SYNC-46` Voice2Motion: موشن بالمعنى من الصوت / Voice2Motion semantic scenes (proven)
- `SYNC-47` إخراج تلقائي لمقطع متكلم / Editor-style auto direction of a talking clip (proven)
- `SYNC-49` إيقاع التلاوة والدعاء / Recitation & dua pacing (documented)
- `SYNC-50` توقيت سطر الأغنية / Lyric line timing (documented)

### `SYNC-49` — إيقاع التلاوة والدعاء / Recitation & dua pacing

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** آية أو سطر لكل شاشة، التغيير عند الوقف، انتقالات بطيئة، بلا ارتداد، ونتبع القارئ لا الإيقاع. / One verse/line per screen, change on waqf, slow crossfades, no bouncy effects; follow the reciter, not a beat grid.

**متى:** عند عمل فيديو لتلاوة قرآن أو دعاء يتبع القارئ ويغير الشاشة عند الوقف / when a Quran recitation or dua video should follow the reciter and change on waqf

**كيف:** Crossfade 600–900 ms; words reveal through a rising mask (0.65 s, stagger 0.09) and leave upward (0.35 s, stagger 0.03); no music under Quran recitation unless the user asks; reference-matched loudness (e.g. −12.75 LUFS) when mimicking a reel; the user's exact text with tashkeel.

**المعاملات:** crossfade 600–900 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تلاوة · قرآن · دعاء · recitation · waqf · no music · آيات · فيديو ديني · قارئ · quran · dua

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-tool/playbooks/audio-sync.md:51`
- `kosif-tool/playbooks/music.md:68`
- `kosif-one/projects/thursday-dua-animation/source/index.html:198-209`

#### 7. قدرات قريبة في العائلة

- `SYNC-47` إخراج تلقائي لمقطع متكلم / Editor-style auto direction of a talking clip (proven)
- `SYNC-48` الريل التلقائي من الكلام / Automatic talking-clip reel (ready)
- `SYNC-50` توقيت سطر الأغنية / Lyric line timing (documented)
- `SYNC-51` ريل كلمات أغنية / Songreel lyric reel (install)

### `SYNC-50` — توقيت سطر الأغنية / Lyric line timing

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** السطر يسبق الغناء، يبقى أثناءه، ويخرج بسرعة. / Lines lead the singing, hold while sung and exit quickly.

**متى:** عند توقيت ظهور أسطر الأغنية وبقائها واختفائها مع الغناء / when timing lyric lines to enter before, hold during and exit right after the singing

**كيف:** Enter 80–120 ms early (recipe: −100 ms with a 350 ms mask wipe); exit ≤ 200 ms (150 ms after the last word); words enter ≤ 40 ms from onset with 180 ms cubic-bezier(0.2,0.9,0.2,1) scale 0.92 → 1. Plan on a grid of tempo, bars, sections and every sung word; characters on one side, words on the other.

**المعاملات:** enter −80…−120 ms; exit ≤ 200 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أغنية · lyrics · line timing · lyric video · كلمات الأغنية · توقيت السطر · غناء · singing · song sync

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-tool/playbooks/music.md:28`
- `kosif-tool/playbooks/music.md:43`
- `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-48` الريل التلقائي من الكلام / Automatic talking-clip reel (ready)
- `SYNC-49` إيقاع التلاوة والدعاء / Recitation & dua pacing (documented)
- `SYNC-51` ريل كلمات أغنية / Songreel lyric reel (install)
- `SYNC-52` لكل جملة منطوقة دليل بصري / One visual proof per spoken claim (documented)

### `SYNC-51` — ريل كلمات أغنية / Songreel lyric reel

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تحليل بنية الأغنية، أسئلة بحث وتلوين لكل قسم، مجمع لقطات، قص، وبناء بالكلمات. / Song structure analysis, per-section queries and grades, a clip pool, cutting and building with lyrics.

**متى:** حين يريد المستخدم ريل كلمات لأغنية بلقطات مقطعة على أقسامها / when the user wants a lyric reel cut from a clip pool to a song's sections

**كيف:** songreel analyze SONG --name --lyrics; cut N --media; build N --model large-v3 --draft\|--render (≈ 45 s typical; clips < 360p rejected). Needs faster-whisper and footage (yt-dlp for pools).

**المعاملات:** ~45 s; reject < 360p

**التثبيت:** pip install faster-whisper # models from huggingface.co (reachable): small 466 MB, large-v3 3.1 GB

**الوسوم:** أغنية · songreel · lyric reel · music video · كليب · ريلز أغنية · لقطات · footage · song structure

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `yt-dlp` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `network` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/songreel.py`
- `100-superskills/skills/kosif-montage-motion/tests/test_songreel.py`

#### 7. قدرات قريبة في العائلة

- `SYNC-49` إيقاع التلاوة والدعاء / Recitation & dua pacing (documented)
- `SYNC-50` توقيت سطر الأغنية / Lyric line timing (documented)
- `SYNC-52` لكل جملة منطوقة دليل بصري / One visual proof per spoken claim (documented)
- `SYNC-53` كشف الصمت الثابت والتكيفي / Fixed & adaptive silence detection (proven)

### `SYNC-52` — لكل جملة منطوقة دليل بصري / One visual proof per spoken claim

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** في الأفلام التي يقودها الصوت، كل سطر منطوق يقابله صورة واحدة تثبته، والفعل يحدث على الكلمة التي تسميه. / In voice-led films each spoken line gets exactly one picture that proves it, and actions happen on the word that names them.

**متى:** عند بناء فيلم يقوده التعليق الصوتي بحيث تقابل كل جملة صورة تثبتها / when planning a voice-led film where every spoken line gets one visual proof

**كيف:** Beat table: spoken line \| visual proof \| entry/exit \| on-screen text. Cross-family sync rules: counters finish on the word that says the number (start 700–1000 ms earlier, ±100 ms); diagram nodes pop on their names, camera moves only in pauses > 400 ms; phone taps at emphasis start − 40 ms; photo cuts 2 frames (≈ 67 ms) before the emphasis word; gestures land 2–4 frames before the stressed word; particle bursts within one frame of transients.

**المعاملات:** ±100 ms; cut −2 frames; gesture −2…−4 frames

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** دليل بصري · narration · sync rules · explainer · تعليق صوتي · فيديو شرح · جدول المشاهد · beat table · voiceover

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-atlas/skills/101-video-skills/216-narrated-product-film/SKILL.md`
- `kosif-tool/playbooks/charts.md:201-208`
- `kosif-tool/playbooks/phone.md:198-205`
- `kosif-tool/playbooks/photos.md:205-211`

#### 7. قدرات قريبة في العائلة

- `SYNC-50` توقيت سطر الأغنية / Lyric line timing (documented)
- `SYNC-51` ريل كلمات أغنية / Songreel lyric reel (install)
- `SYNC-53` كشف الصمت الثابت والتكيفي / Fixed & adaptive silence detection (proven)
- `SYNC-54` إصلاح انزياح الصوت المدموج / Joined-audio drift fix (documented)

### `SYNC-53` — كشف الصمت الثابت والتكيفي / Fixed & adaptive silence detection

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اعثر على الهواء الميت بعتبة ثابتة أو بعتبة البوابة المقاسة لكل تسجيل. / Find dead air with a fixed threshold or with each recording's own measured gating threshold.

**متى:** حين نريد إيجاد فترات الصمت أو الهواء الميت في التسجيل لقصها / when finding dead air or silent gaps in a recording to cut them

**كيف:** Fixed: -af silencedetect=n=-35dB:d=0.5..0.7 -f null - (ran here: a 1 s gap reported 1.000–2.000 s). Adaptive: loudnorm print_format=json → input_thresh → silencedetect=noise=${thresh}dB:d=0.5; merge gaps < 0.2 s. EDL writer: silence_cut.py in --db -35 --min 0.6 --pad 0.12 --out edl.json; Python analyser: −50 dBFS, ≥ 0.5 s over 50 ms RMS.

**المعاملات:** −35 dB; d 0.5–0.7 s; pad 0.08–0.12 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صمت · silence · silencedetect · jump cut · edl · هواء ميت · قص الصمت · تقطيع · dead air · loudnorm

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

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-atlas/skills/2712-remotion/10436-remotion-markup/silence-detection.md`
- `100-superskills/skills/pro-video-editor-ffmpeg/scripts/silence_cut.py:19`
- `100-superskills/skills/kosif-montage-motion/scripts/omni/audio_analyze.py:147`

#### 7. قدرات قريبة في العائلة

- `SYNC-51` ريل كلمات أغنية / Songreel lyric reel (install)
- `SYNC-52` لكل جملة منطوقة دليل بصري / One visual proof per spoken claim (documented)
- `SYNC-54` إصلاح انزياح الصوت المدموج / Joined-audio drift fix (documented)
- `SYNC-55` ذروة المؤثر على الحدث / SFX peak-offset alignment (seen)

### `SYNC-54` — إصلاح انزياح الصوت المدموج / Joined-audio drift fix

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الدمج بالنسخ يبقي حشو كل قطعة فيتراكم الانزياح (~50 ms لكل وصلة)؛ فك وأعد الترميز مرة واحدة. / Copy-mode concat keeps each piece's encoder padding, so drift accumulates (~50 ms per join); decode and encode once.

**متى:** حين يتراكم انزياح بعد دمج ملفات صوت كثيرة بالنسخ / when joined audio pieces drift out of sync after copy-mode concat

**كيف:** ffmpeg -f concat -safe 0 -i list.txt -c:a libmp3lame -b:a 64k -ar 24000 -ac 1 -write_xing 0 joined.mp3; verify joined duration vs the sum of parts (measured 2.51 s → 0.06 s over 181 pieces). Better: concatenate WAV/PCM and encode once at delivery.

**المعاملات:** ~50 ms/join; MP3 frame 1152/576 samples

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** انزياح · drift · concat audio · mp3 padding · دمج الصوت · تأخر الصوت · عدم تزامن · out of sync · ffmpeg concat

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-atlas/skills/3323-joined-audio-transcript-drift/13837-joined-audio-transcript-drift/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-52` لكل جملة منطوقة دليل بصري / One visual proof per spoken claim (documented)
- `SYNC-53` كشف الصمت الثابت والتكيفي / Fixed & adaptive silence detection (proven)
- `SYNC-55` ذروة المؤثر على الحدث / SFX peak-offset alignment (seen)
- `SYNC-56` دمج المشاهد مع الصوت الأصلي بلا تعديل / Concat + untouched original audio mux (ready)

### `SYNC-55` — ذروة المؤثر على الحدث / SFX peak-offset alignment

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خزّن زمن الذروة داخل كل ملف مؤثر وابدأ الصوت عند زمن الحدث ناقص الذروة؛ والصاعدات تنتهي على الحدث. / Store each SFX file's internal peak time and start it at event − peak; risers align to their end.

**متى:** عند وضع مؤثر صوتي بحيث تقع ذروته بالضبط على الحدث البصري / when placing a sound effect so its peak lands exactly on the visual event

**كيف:** PEAK table per file (measure with astats or numpy argmax of \|x\|); start = eventTime − peak; risers end on the event; whoosh ≤ −18 dBFS on a separate stem.

**المعاملات:** PEAK per file

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مؤثرات · sfx · peak alignment · whoosh · transient · مؤثرات صوتية · ووش · توقيت المؤثر · sound effects · riser

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:numpy` ← python3 -c "import numpy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `style:product`
- `kosif-tool/playbooks/photos.md:205-211`

#### 7. قدرات قريبة في العائلة

- `SYNC-53` كشف الصمت الثابت والتكيفي / Fixed & adaptive silence detection (proven)
- `SYNC-54` إصلاح انزياح الصوت المدموج / Joined-audio drift fix (documented)
- `SYNC-56` دمج المشاهد مع الصوت الأصلي بلا تعديل / Concat + untouched original audio mux (ready)
- `SYNC-57` غلاف الجهارة وقنوات الصوت للحركة / Loudness envelope & sound channels for motion (ready)

### `SYNC-56` — دمج المشاهد مع الصوت الأصلي بلا تعديل / Concat + untouched original audio mux

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يجمع المشاهد المرندرة بالترتيب ويضع أغنية المستخدم تحتها كما هي، مع بصمة sha256 للمصدر. / Joins rendered segments in order and lays the user's original song underneath untouched, recording the source sha256.

**متى:** حين نجمع المشاهد المرندرة ونضع أغنية المستخدم الأصلية تحتها دون تعديل / when joining rendered segments and laying the user's original song under them untouched

**كيف:** ffmpeg -f concat -safe 0 -i concat.txt -i song.mp3 -map 0:v:0 -map 1:a:0 -t DUR -c:v copy -c:a aac -b:a 192k … ; only gentle edge fades (in 0.3 s, out 1.3 s) if asked; record sha256 of the source audio. Optional mux in fastify render.py: --audio path → -shortest (no loudness change).

**المعاملات:** fade in 0.3 s / out 1.3 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** دمج · mux · original audio · sha256 · song · تجميع المشاهد · أغنية أصلية · الصوت الأصلي · concat · ffmpeg

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:152-158`
- `fastify-motion-bro/scripts/render.py:15`

#### 7. قدرات قريبة في العائلة

- `SYNC-54` إصلاح انزياح الصوت المدموج / Joined-audio drift fix (documented)
- `SYNC-55` ذروة المؤثر على الحدث / SFX peak-offset alignment (seen)
- `SYNC-57` غلاف الجهارة وقنوات الصوت للحركة / Loudness envelope & sound channels for motion (ready)
- `SYNC-58` مزامنة الفم بستة أشكال / Six-shape lip sync (documented)

### `SYNC-57` — غلاف الجهارة وقنوات الصوت للحركة / Loudness envelope & sound channels for motion

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** غلاف RMS كل 50 ms وقنوات لكل إطار (bass/mid/high، ضربات، بدايات، صمت) تقود أي قيمة بصرية. / A 50 ms RMS envelope and per-frame channels (bass/mid/high, kicks, onsets, silence) drive any visual value.

**متى:** حين نريد أن تتفاعل الحركة مع الصوت: الباص والضربات والبدايات والصمت / when visuals should react to the sound: bass, kicks, onsets and silence

**كيف:** python motion.py channels TRACK.wav [--fps 30] → ch.json; in the page MOTION.channels(json): ch.v('bass',t), ch.kick(t), ch.onset(t), ch.silent(t). Verse halo R = 0.62·min(W,H)·(1 + 0.05·rms + 0.06·kick + 0.25·flare). Caption scale from RMS stays within 3–6% (proof: +4.5%). Browser mic meter: AnalyserNode fftSize 256, RMS × 4 clamped to 1.

**المعاملات:** hop sr/fps; nfft 4096 Hann; caption ±3–6%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** غلاف · rms · channels · audio reactive · envelope · تفاعل مع الصوت · ضربات الإيقاع · باص · bass · kicks

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:97`
- `kosif-one/tools/kosif-studio/motion/templates/verse.html:86`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/audio-reactive-spectrum/README.md`
- `kosif-audit-studio/voice.js:166`

#### 7. قدرات قريبة في العائلة

- `SYNC-55` ذروة المؤثر على الحدث / SFX peak-offset alignment (seen)
- `SYNC-56` دمج المشاهد مع الصوت الأصلي بلا تعديل / Concat + untouched original audio mux (ready)
- `SYNC-58` مزامنة الفم بستة أشكال / Six-shape lip sync (documented)
- `SYNC-U01` وسم مصدر التوقيت: عرض أم صوت أم تقديري / Timing provenance labels (display / voice / estimated) (documented)

### `SYNC-58` — مزامنة الفم بستة أشكال / Six-shape lip sync

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الفم يختار بين مغلق وA وO وE وM وF من طاقة الصوت أو نص السكريبت. / The mouth picks among closed, A, O, E, M, F from audio energy or the script.

**متى:** حين نحتاج شخصية متحركة يتحرك فمها مع الكلام أو الغناء / when an animated character's mouth must move with speech or sung lyrics

**كيف:** Map RMS (and phonemes when available from Piper/aligner) to a viseme per frame; hold each shape ≥ 2 frames to avoid flicker; replacement tiles synced to syllables for lyric characters.

**المعاملات:** 6 visemes; hold ≥ 2 frames

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مزامنة الفم · lip sync · visemes · mouth · حركة الفم · شخصية متكلمة · تحريك الفم · talking character · phonemes

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:piper` ← python3 -c "import piper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `100-superskills/skills/character-animation-2d/SKILL.md`
- `kosif-tool/styles/pm-davidshulmanfl-371638/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-56` دمج المشاهد مع الصوت الأصلي بلا تعديل / Concat + untouched original audio mux (ready)
- `SYNC-57` غلاف الجهارة وقنوات الصوت للحركة / Loudness envelope & sound channels for motion (ready)
- `SYNC-U01` وسم مصدر التوقيت: عرض أم صوت أم تقديري / Timing provenance labels (display / voice / estimated) (documented)
- `SYNC-X01` تحليل أغنية لفيلم كلمات / Song analysis for a lyric film (bands, kicks, word times) (documented)

### `SYNC-U01` — وسم مصدر التوقيت: عرض أم صوت أم تقديري / Timing provenance labels (display / voice / estimated)

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | owner |

**ما هي:** كل توقيت يحمل مصدره: ظهور العبارة على الشاشة من البكسلات (~33 ms عند 30 fps) توقيت عرض لا بداية صوت؛ الكلمات الموزعة تقديريًا داخل العبارة تُوسم ESTIMATED في اسم الملف؛ ملف JSON فيه timing_methods لكل نوع وtranscript_method. التفريغ الآلي فاته أول ~13 ث في إحدى الحزم وصححه النص الظاهر. — Never present estimated word timing as audio-aligned.

**متى:** تسليم توقيت كلمات أو ترجمة متزامنة / delivering word timing or synced captions

**كيف:** المحاذاة الحقيقية: faster-whisper أو whisper.cpp بطوابع كلمات ثم مقارنة بالنص الظاهر؛ وإلا فاذكر «تقديري».

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** timing · توقيت · word timing · توقيت الكلمات · estimated · تقديري · srt · lrc · alignment · محاذاة · دقيق · الكلمات · أغنية · song · lyrics

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-U01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/references/owner-uploads-review-20261023.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-57` غلاف الجهارة وقنوات الصوت للحركة / Loudness envelope & sound channels for motion (ready)
- `SYNC-58` مزامنة الفم بستة أشكال / Six-shape lip sync (documented)
- `SYNC-X01` تحليل أغنية لفيلم كلمات / Song analysis for a lyric film (bands, kicks, word times) (documented)
- `SYNC-X02` قفل موضع مقطع الترجمة / Caption chunk position lock (documented)

### `SYNC-X01` — تحليل أغنية لفيلم كلمات / Song analysis for a lyric film (bands, kicks, word times)

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | owner (song audio and lyrics are third-party; not included) |

**ما هي:** من ملف الأغنية استخرج أغلفة طاقة لكل إطار (باس، صوت المغني، حدة)، والضربات، والإيقاع، وأزمنة تقديرية للكلمات داخل نوافذ أسطر يعطيها المستخدم، مع وسم صادق لجودة التوقيت. — From the song file derive per-frame band envelopes (low, vocal, high), kicks, tempo and estimated word times inside user-given line windows, with an honest timing-quality label.

**متى:** فيلم كلمات أغنية بلا تفريغ صوتي آلي متاح — a lyric film when no ASR alignment is available.

**كيف:** Per video frame (hop = sr/fps) a Hann 2048 FFT: bands low 35–160 Hz, vocal 300–3200 Hz, high 4000–11000 Hz; RMS; spectral flux on log1p; normalise each by its 98th percentile, clip 1.2, light smoothing. Kicks = low-band rises > 0.18 that are local maxima (±2 frames). BPM by flux autocorrelation limited to 60–160 (beware half-time: a ~138 BPM feel read as 69.2). Word weights ∝ max(2, len(word)); span = 0.9 × line so the held last syllable keeps a tail; snap to vocal-band onsets within 0.22 s; min gap 0.12 s. Write words.json with timing_quality = 'line windows from user; edges from vocal energy; word times estimated (not ASR)'. The session distillation re-ran it: 56.92 s, bpm ~69.2, 25 kicks; line starts matched the shipped data except 2.033 vs 2.0 and 26.3 vs 26.333 — the edge refinement almost never moves a start. Prefer real alignment when audio-sync tools are available. Status note: the code is owner material that is not vendored in this skill; the numbers above are from one run on the owner's copy on 2026-10-16 and cannot be re-run from here, so this is 📄 documented, not ✅.

**المعاملات:** bands 35–160 / 300–3200 / 4000–11000 Hz; kick rise > 0.18; snap ≤ 0.22 s; gap ≥ 0.12 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** lyrics · words.json · onset · kick · song film · كلمات الأغنية · توقيت الكلمات

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-X01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

#### 6. الأدلة

- `owner-upload:film_project/film/analyze.py`
- `kosif-tool/.claude/skills/kosif-superpowers/references/external-skills.md`

#### 7. قدرات قريبة في العائلة

- `SYNC-58` مزامنة الفم بستة أشكال / Six-shape lip sync (documented)
- `SYNC-U01` وسم مصدر التوقيت: عرض أم صوت أم تقديري / Timing provenance labels (display / voice / estimated) (documented)
- `SYNC-X02` قفل موضع مقطع الترجمة / Caption chunk position lock (documented)

### `SYNC-X02` — قفل موضع مقطع الترجمة / Caption chunk position lock

| الحقل | القيمة |
|---|---|
| العائلة | `audio-sync-captions` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/audio-sync-captions.md)) |
| المجموعة | الصوت والموسيقى والتعليق (`audio`) |
| نوع المخرج (A25، A27) | صوت وتفريغ وموسيقى (`audio`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | unknown (reference only) |

**ما هي:** الكلمات تظهر واحدة واحدة في مكانها النهائي، والمقطع يحتفظ بموضع واحد طوال عمره حتى لو قُطعت الصورة تحته. — Words appear one by one in their final place, and a caption chunk keeps one position for its whole life even when the picture cuts underneath.

**متى:** ترجمات كلمة بكلمة على متحدث أو مونتاج سريع — word-by-word captions on a speaker or a fast edit.

**كيف:** Measure every word once with the real font on a canvas and justify lines across a shared width, so widths never depend on DOM timing; words arrive expo-out over 0.24 s with a small rise and blur; the block drifts up slowly; key words in an italic serif accent; validate the layout with visible word bounding boxes, not element boxes. For Arabic keep whole words and RTL order (ARAB rules).

**المعاملات:** word in 0.24 s expo-out; one position per chunk

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** captions · subtitles · word by word · layout · ترجمة · كلمة بكلمة

#### 1. الاستقبال (A25)

- الملف المصدر: مدخل حاجب ← لا يُفترض: المدخل مطلوب
- اللغة واللهجة: افتراض مكتوب ← تُكتشف من الملف وتُذكر
- صيغة المخرج: افتراض مكتوب ← نص مع توقيت الكلمات words.json
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `audio` ← المخرج `dataset`، والمنفّذ `method:SYNC-X02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner`.
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

#### 6. الأدلة

- `owner-upload:Claude_edit_skill_1/Claude edit skill/implementation/browser-reference/captions.js`

#### 7. قدرات قريبة في العائلة

- `SYNC-U01` وسم مصدر التوقيت: عرض أم صوت أم تقديري / Timing provenance labels (display / voice / estimated) (documented)
- `SYNC-X01` تحليل أغنية لفيلم كلمات / Song analysis for a lyric film (bands, kicks, word times) (documented)

