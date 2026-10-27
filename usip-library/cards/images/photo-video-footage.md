# `photo-video-footage` — الصور والتحرير والتوليد (71 بطاقة)

> مكتبة بروتوكول USIP v5.6 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/photo-video-footage.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/images.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`FOOT-01` انضباط ترخيص الصور واللقطات](#foot-01--انضباط-ترخيص-الصور-واللقطات--media-licensing-discipline)
- [`FOOT-02` تنزيل لقطة مفتوحة مع إيصال مصدر](#foot-02--تنزيل-لقطة-مفتوحة-مع-إيصال-مصدر--open-footage-downloader-with-provenance)
- [`FOOT-03` جلب من المنصات مع الاعتمادات](#foot-03--جلب-من-المنصات-مع-الاعتمادات--socialpinterest-fetch-with-credits-yt-dlp)
- [`FOOT-04` مجمع لقطات بأسئلة بحث ثنائية اللغة](#foot-04--مجمع-لقطات-بأسئلة-بحث-ثنائية-اللغة--per-shot-bilingual-footage-pool)
- [`FOOT-05` مكتبة وسائط محلية مع فحص](#foot-05--مكتبة-وسائط-محلية-مع-فحص--local-media-library-with-probe)
- [`FOOT-06` تايملاين زمني متعدد الكاميرات](#foot-06--تايملاين-زمني-متعدد-الكاميرات--chronological-multi-camera-timeline)
- [`FOOT-07` إعدادات تسجيل الشاشة](#foot-07--إعدادات-تسجيل-الشاشة--screen-capture-defaults)
- [`FOOT-08` كشف اللقطات إلى تايملاين](#foot-08--كشف-اللقطات-إلى-تايملاين--sceneshot-detection--timeline)
- [`FOOT-09` لوحة لقطات واختيار الغلاف](#foot-09--لوحة-لقطات-واختيار-الغلاف--contact-sheet--cover-frame-mining)
- [`FOOT-10` اختيار أنشط نافذة في اللقطة](#foot-10--اختيار-أنشط-نافذة-في-اللقطة--motion-energy-window-picking)
- [`FOOT-11` قص البدايات المعيبة وتجميع المكرر](#foot-11--قص-البدايات-المعيبة-وتجميع-المكرر--bad-head-trimming--duplicate-take-grouping)
- [`FOOT-12` تحليل تعريض الصورة ونصائح بالعربية](#foot-12--تحليل-تعريض-الصورة-ونصائح-بالعربية--image-exposure-analysis--arabic-fix-advice)
- [`FOOT-13` دراسة ريل مرجعي بدقة الإطار](#foot-13--دراسة-ريل-مرجعي-بدقة-الإطار--reference-reel-study-mimic)
- [`FOOT-14` تحليل فيديو مرجعي إلى نبضات](#foot-14--تحليل-فيديو-مرجعي-إلى-نبضات--video-breakdown-to-beats)
- [`FOOT-15` تشخيص قبل رفع الدقة](#foot-15--تشخيص-قبل-رفع-الدقة--upscale-triage)
- [`FOOT-16` مترجم تايملاين JSON](#foot-16--مترجم-تايملاين-json--json-timeline-compiler-cuts-ramps-overlays)
- [`FOOT-17` قص دقيق بالإطار](#foot-17--قص-دقيق-بالإطار--frame-accurate-trim-re-encode)
- [`FOOT-18` دمج مقاطع مختلفة دون كسر الصوت](#foot-18--دمج-مقاطع-مختلفة-دون-كسر-الصوت--fit-and-join-concat)
- [`FOOT-19` منحدرات السرعة والتصوير البطيء](#foot-19--منحدرات-السرعة-والتصوير-البطيء--speed-ramps--slow-motion)
- [`FOOT-20` قص الصمت](#foot-20--قص-الصمت--silence-jump-cut)
- [`FOOT-21` تجميد إطار وتكرار حلقة](#foot-21--تجميد-إطار-وتكرار-حلقة--freeze-frame--loop)
- [`FOOT-22` محرر KOSIF Studio في المتصفح](#foot-22--محرر-kosif-studio-في-المتصفح--kosif-studio-browser-montage-editor)
- [`FOOT-23` مونتاج مستقل أو متتابع في Remotion](#foot-23--مونتاج-مستقل-أو-متتابع-في-remotion--remotion-clip-editing-independent-vs-ripple)
- [`FOOT-24` تثبيت الاهتزاز](#foot-24--تثبيت-الاهتزاز--stabilisation-vidstab-2-pass)
- [`FOOT-25` إزالة التشويش والتوضيح وسلسلة الترميم](#foot-25--إزالة-التشويش-والتوضيح-وسلسلة-الترميم--denoise-sharpen--restoration-chain)
- [`FOOT-26` مسح الترجمة المحروقة](#foot-26--مسح-الترجمة-المحروقة--burned-caption-eraser-decaption)
- [`FOOT-27` تمويه الوجوه والمناطق](#foot-27--تمويه-الوجوه-والمناطق--face--region-privacy-masks)
- [`FOOT-28` مفتاح اللون الأخضر](#foot-28--مفتاح-اللون-الأخضر--chroma-key)
- [`FOOT-29` تعديل الصورة: إعادة تلوين تحفظ الظلال](#foot-29--تعديل-الصورة-إعادة-تلوين-تحفظ-الظلال--picture-edits-shading-preserving-recolour)
- [`FOOT-30` معالجة الصور بـ ImageMagick](#foot-30--معالجة-الصور-بـ-imagemagick--imagemagick-still-post-processing)
- [`FOOT-31` عزل الشخص بقناع شفاف](#foot-31--عزل-الشخص-بقناع-شفاف--person-matte--background-removal)
- [`FOOT-32` عنوان خلف المتحدث](#foot-32--عنوان-خلف-المتحدث--title-behind-the-speaker)
- [`FOOT-33` متحدث مقصوص فوق عوالم متبدلة](#foot-33--متحدث-مقصوص-فوق-عوالم-متبدلة--rotoscoped-speaker-over-swapped-worlds)
- [`FOOT-34` تسمية متتبعة ودائرة اهتمام](#foot-34--تسمية-متتبعة-ودائرة-اهتمام--tracked-callout--attention-ring)
- [`FOOT-35` إدراج بمنظور مثبت بأربع نقاط](#foot-35--إدراج-بمنظور-مثبت-بأربع-نقاط--planar-corner-pin-inserts)
- [`FOOT-36` تجميد الشخص والعالم يمشي](#foot-36--تجميد-الشخص-والعالم-يمشي--freeze-the-subject-keep-the-world-moving)
- [`FOOT-37` سينماغراف](#foot-37--سينماغراف--cinemagraph)
- [`FOOT-38` مقارنة قبل وبعد صادقة](#foot-38--مقارنة-قبل-وبعد-صادقة--honest-beforeafter-wipe)
- [`FOOT-39` كين بيرنز الصحيح](#foot-39--كين-بيرنز-الصحيح--ken-burns-done-well)
- [`FOOT-40` بارالاكس مستوي بمعاملات عمق](#foot-40--بارالاكس-مستوي-بمعاملات-عمق--planar-parallax-with-depth-factors)
- [`FOOT-41` كشف بارالاكس ثلاثي ومن الكولاج إلى البطل](#foot-41--كشف-بارالاكس-ثلاثي-ومن-الكولاج-إلى-البطل--three-layer-reveal--collage--hero)
- [`FOOT-42` حماية النص فوق الصور واللقطات](#foot-42--حماية-النص-فوق-الصور-واللقطات--text-protection-over-photos--footage)
- [`FOOT-43` صورة أرشيف تنفتح على الحاضر](#foot-43--صورة-أرشيف-تنفتح-على-الحاضر--archive-photo-opens-onto-the-present)
- [`FOOT-44` قواعد الصور للعربية](#foot-44--قواعد-الصور-للعربية--rtl-photo-layout-rules)
- [`FOOT-45` أساليب الصور الجاهزة](#foot-45--أساليب-الصور-الجاهزة--photo-styles-to-scaffold)
- [`FOOT-46` شرائح الفلاتر وجدار الصور](#foot-46--شرائح-الفلاتر-وجدار-الصور--filter-strips--tile-walls)
- [`FOOT-47` لوح لقطات كل إطاراته مفتاحية](#foot-47--لوح-لقطات-كل-إطاراته-مفتاحية--all-intra-seekable-footage-plate)
- [`FOOT-48` عرض الأفقي في 9:16 فوق نسخة مموهة](#foot-48--عرض-الأفقي-في-916-فوق-نسخة-مموهة--landscape-in-916-over-a-blurred-fill)
- [`FOOT-49` لقطة متحدث تحت الرسوم](#foot-49--لقطة-متحدث-تحت-الرسوم--real-footage-plate-under-graphics)
- [`FOOT-50` محرك المونتاج الموجّه](#foot-50--محرك-المونتاج-الموجّه--directed-edit-engine)
- [`FOOT-51` إعادة تغليف المتحدث ببطاقات](#foot-51--إعادة-تغليف-المتحدث-ببطاقات--talking-head-recut-with-designed-cards)
- [`FOOT-52` فيديو ولوتي داخل HTML](#foot-52--فيديو-ولوتي-داخل-html--video--lottie-inside-html-compositions)
- [`FOOT-53` مشغل مقدمة سينمائية متكيف](#foot-53--مشغل-مقدمة-سينمائية-متكيف--adaptive-cinematic-intro-player)
- [`FOOT-54` مونتاج تلقائي على الموسيقى](#foot-54--مونتاج-تلقائي-على-الموسيقى--auto-montage-to-music)
- [`FOOT-55` ريل من مقطع كلام بأمر واحد](#foot-55--ريل-من-مقطع-كلام-بأمر-واحد--one-command-talking-clip-reel)
- [`FOOT-56` ريلز من فيديو طويل](#foot-56--ريلز-من-فيديو-طويل--reels-from-a-long-video)
- [`FOOT-57` المونتاج الذكي الكامل من الكلام](#foot-57--المونتاج-الذكي-الكامل-من-الكلام--smart-full-montage-from-speech-autoedit)
- [`FOOT-58` مونتاج لقطات المستخدم على الإيقاع (بصمة)](#foot-58--مونتاج-لقطات-المستخدم-على-الإيقاع-بصمة--basma-automatic-beat-montage)
- [`FOOT-D01` ريل «الدعاء» من لقطاتك وصوتك](#foot-d01--ريل-الدعاء-من-لقطاتك-وصوتك--الدعاء-friday-dua-reel-kit)
- [`FOOT-D02` انتقالات كاب كات على الصورة فقط](#foot-d02--انتقالات-كاب-كات-على-الصورة-فقط--capcut-style-transitions-under-fixed-text)
- [`FOOT-D03` قياس أسلوب ريل من الإطارات](#foot-d03--قياس-أسلوب-ريل-من-الإطارات--measure-a-reels-style-from-its-frames)
- [`FOOT-P01` إعادة مونتاج اللقطات من قائمة قطع محدودة](#foot-p01--إعادة-مونتاج-اللقطات-من-قائمة-قطع-محدودة--bounded-edl-recut-trimconcat-with-denoise-and-loudnorm)
- [`FOOT-U01` مطابقة المسودة بلقطات المصدر](#foot-u01--مطابقة-المسودة-بلقطات-المصدر--match-a-draft-back-to-its-source-shots)
- [`FOOT-U02` كاشف القفزات: اقطع قبل القفزة](#foot-u02--كاشف-القفزات-اقطع-قبل-القفزة--jump-cut-finder-cut-on-the-frame-before)
- [`FOOT-U03` قناع شخص بلا تعلم آلي](#foot-u03--قناع-شخص-بلا-تعلم-آلي--person-matte-without-ml)
- [`FOOT-X01` انضباط مونتاج المادة الحقيقية](#foot-x01--انضباط-مونتاج-المادة-الحقيقية--real-footage-edit-discipline-source-to-programme-map)
- [`FOOT-X02` فحص القدرة واختبارات قصيرة قبل التصدير](#foot-x02--فحص-القدرة-واختبارات-قصيرة-قبل-التصدير--capability-preflight-and-short-tests-before-an-expensive-export)
- [`FOOT-X03` القص الدقيق بالإطار يحتاج إعادة ترميز](#foot-x03--القص-الدقيق-بالإطار-يحتاج-إعادة-ترميز--frame-accurate-trims-need-a-re-encode)
- [`FOOT-X04` طبقات أدوات المونتاج وحالات المشروع](#foot-x04--طبقات-أدوات-المونتاج-وحالات-المشروع--footage-editing-layers-and-project-state-hygiene)
- [`FOOT-X05` عقد محاكاة فيديو مرجعي](#foot-x05--عقد-محاكاة-فيديو-مرجعي--reference-video-imitation-contract-8-steps)
- [`FOOT-X06` فاحص المرجع المرخّص: صفحة أو ملف أو HLS ← قياسات](#foot-x06--فاحص-المرجع-المرخّص-صفحة-أو-ملف-أو-hls--قياسات--permissioned-reference-inspector-page--direct--hls--measurements)

## البطاقات / cards

### `FOOT-01` — انضباط ترخيص الصور واللقطات / Media licensing discipline

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مسموح: ما أكّده المستخدم، الملكية العامة/CC0، CC BY مع الإسناد، والمخزون بإيصال؛ ممنوع: لقطات المراجع والمكشوط وND وNC التجاري. / Allowed: user-confirmed, PD/CC0, CC BY with attribution, receipted stock; banned: reference frames, scraped media, ND, NC in commercial work.

**متى:** حين تحتاج التأكد من حق استخدام صورة أو لقطة قبل وضعها في الفيديو أو الإعلان / when checking whether a photo or clip may be used, with attribution and one asset-log row per file

**كيف:** One ASSETS.md row per file (source, licence, author, URL). Editorial-only images never go in ads; people need model releases; AI images only when asked and declared. Faceless channels: any clip showing the speaker's face even for one frame is audio-only; sample 1 frame/s through face detection.

**المعاملات:** one ASSETS.md row per file

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ترخيص · حقوق · license · attribution · cc0 · assets.md · حقوق النشر · ملكية عامة · إذن استخدام · copyright · creative commons

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/photos.md:11`
- `kosif-atlas/skills/1096-akbun-editvideo/2451-davinciresolve-beats-devtalk/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-02` تنزيل لقطة مفتوحة مع إيصال مصدر / Open-footage downloader with provenance (ready)
- `FOOT-03` جلب من المنصات مع الاعتمادات / Social/Pinterest fetch with credits (yt-dlp) (install)

### `FOOT-02` — تنزيل لقطة مفتوحة مع إيصال مصدر / Open-footage downloader with provenance

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ينزّل رابط HTTPS واحدًا من مضيف مسموح، يرفض صفحات التحدي، يحدّ الحجم، ويكتب إيصالًا بالبصمة والرخصة. / Downloads one explicit HTTPS URL from an allow-listed open host, refuses challenge pages, caps size and writes a hashed provenance receipt.

**متى:** حين يريد المستخدم تنزيل لقطة مفتوحة الترخيص من رابط مباشر مع حفظ مصدرها ورخصتها / when downloading one open-licence clip from a direct HTTPS link with a hashed provenance receipt

**كيف:** python motion.py openclip URL --out clip.mp4 [--license-note '…'] (open_footage.py). Here: commons.wikimedia.org and archive.org are reachable; pexels.com, pixabay.com and NASA images answer 403 from this container — ask the user for files instead.

**المعاملات:** hosts *.wikimedia.org, *.pexels.com; https only; 64 KiB–500 MiB; timeout 120 s; SHA-256 sidecar .source.json (kosif-open-footage-v1)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** لقطات مفتوحة · ويكيميديا · open footage · provenance · wikimedia · تنزيل فيديو · تحميل لقطة · إيصال المصدر · download clip · archive.org

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/open_footage.py`
- `kosif-studio/motion/test_open_footage.py`
- `kosif-studio/motion/references/voice-open-footage-upgrade-2026-10-10.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-01` انضباط ترخيص الصور واللقطات / Media licensing discipline (documented)
- `FOOT-03` جلب من المنصات مع الاعتمادات / Social/Pinterest fetch with credits (yt-dlp) (install)
- `FOOT-04` مجمع لقطات بأسئلة بحث ثنائية اللغة / Per-shot bilingual footage pool (documented)

### `FOOT-03` — جلب من المنصات مع الاعتمادات / Social/Pinterest fetch with credits (yt-dlp)

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** روابط بنترست وتيك توك وإنستغرام ويوتيوب وX إلى مكتبة وسائط بنسخة تحرير وملف اعتمادات. / Pinterest, TikTok, Instagram, YouTube and X links into a media library with an edit-safe copy and a credits file.

**متى:** لما يرسل المستخدم روابط تيك توك أو إنستغرام أو يوتيوب أو بنترست ليجمعها في مكتبة وسائط باعتماداتها / when pulling TikTok, Instagram, YouTube, Pinterest or X links into a media library with credits

**كيف:** python scripts/kmotion.py fetch URL… --max 30 --only video\|image [--list] [--cookies]; edit copy H.264 yuv420p CFR ≤ 60 fps + AAC 48 kHz; fetch-credits.json; duplicates skipped. The test skips here because yt-dlp is not installed. Safe single-URL variant: https only, global IPs only, ≤ 150 MB, ≤ 900 s, ≤ 720p, sha256 receipt. TikTok needs an impersonation backend (curl_cffi) — otherwise ask for the file. Downloaded media keeps its source licence: reference ≠ permission.

**المعاملات:** --max 30; edit copy ≤ 60 fps

**التثبيت:** pip install yt-dlp

**الوسوم:** تحميل · بنترست · yt-dlp · fetch · credits · tiktok · تنزيل من يوتيوب · تيك توك · انستا · youtube download · instagram

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `yt-dlp` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/fetch.py`
- `100-superskills/skills/kosif-montage-motion/tests/test_fetch_lab.py:66`
- `kosif-one/projects/KOSIF_Motion_Ghorba/tools/kosif_c_video_fetch.py:24-49`

#### 7. قدرات قريبة في العائلة

- `FOOT-01` انضباط ترخيص الصور واللقطات / Media licensing discipline (documented)
- `FOOT-02` تنزيل لقطة مفتوحة مع إيصال مصدر / Open-footage downloader with provenance (ready)
- `FOOT-04` مجمع لقطات بأسئلة بحث ثنائية اللغة / Per-shot bilingual footage pool (documented)
- `FOOT-05` مكتبة وسائط محلية مع فحص / Local media library with probe (ready)

### `FOOT-04` — مجمع لقطات بأسئلة بحث ثنائية اللغة / Per-shot bilingual footage pool

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل لقطة في المرجع تُوصف بـ 1–3 عبارات بحث إنجليزية وعربية لتجمع لقطات جديدة بنفس المعنى. / Each reference shot is described by 1–3 English + Arabic searches so new footage with the same meaning lands in one pool.

**متى:** حين تبحث عن لقطات جديدة تحمل معنى كل لقطة في الفيديو المرجعي بعبارات بحث عربية وإنجليزية / when sourcing new footage that matches each reference shot via English and Arabic search phrases

**كيف:** shots[].query e.g. ['incense burner smoke aesthetic', 'bakhoor mabkhara']; 2–3 candidates per shot, clip ≥ shot length (or ≥ 0.67× when slowed), ≥ 720p, no watermark or burned text; credit every pin. When the host is unreachable publish an intermediary page with key frames and search buttons for the user to fetch.

**المعاملات:** 2–3 candidates/shot; ≥ 720p

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بحث لقطات · footage pool · pinterest · queries · b-roll · لقطات بديلة · كلمات بحث · بي رول · search terms · reference shots

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/projects/mimic-jumuah/study/mimic.json`
- `100-superskills/skills/kosif-montage-motion/references/mimic.md`
- `kosif-tool/.claude/skills/kosif-superpowers/references/mimic.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-02` تنزيل لقطة مفتوحة مع إيصال مصدر / Open-footage downloader with provenance (ready)
- `FOOT-03` جلب من المنصات مع الاعتمادات / Social/Pinterest fetch with credits (yt-dlp) (install)
- `FOOT-05` مكتبة وسائط محلية مع فحص / Local media library with probe (ready)
- `FOOT-06` تايملاين زمني متعدد الكاميرات / Chronological multi-camera timeline (documented)

### `FOOT-05` — مكتبة وسائط محلية مع فحص / Local media library with probe

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رفع بالسحب والإفلات، كل ملف يُفحص (مدة، فيديو، صوت) ويُصنف. / Drag-and-drop upload, every file probed (duration, video, audio) and classified.

**متى:** عند رفع ملفات فيديو وصوت وصور إلى مكتبة محلية تفحص مدة كل ملف ومساراته وتصنفه / when uploading video, audio and image files to a local library that probes and classifies each one

**كيف:** POST /api/media (multipart, 1 MB chunks), GET/DELETE /api/media/NAME; index in workbench/media/.index.json. Accepts mp4 mov mkv webm avi m4v mp3 wav m4a aac flac ogg png jpg webp gif json txt srt; ≤ 4 GB per file.

**المعاملات:** ≤ 4 GB/file; names ≤ 150 chars

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مكتبة وسائط · media library · probe · upload · رفع ملفات · سحب وإفلات · فحص الملفات · drag and drop · file import

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:58`
- `100-superskills/skills/kosif-montage-motion/tests/test_web.py:145`

#### 7. قدرات قريبة في العائلة

- `FOOT-03` جلب من المنصات مع الاعتمادات / Social/Pinterest fetch with credits (yt-dlp) (install)
- `FOOT-04` مجمع لقطات بأسئلة بحث ثنائية اللغة / Per-shot bilingual footage pool (documented)
- `FOOT-06` تايملاين زمني متعدد الكاميرات / Chronological multi-camera timeline (documented)
- `FOOT-07` إعدادات تسجيل الشاشة / Screen-capture defaults (documented)

### `FOOT-06` — تايملاين زمني متعدد الكاميرات / Chronological multi-camera timeline

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رتّب كل اللقطات على زمن التصوير مع تصحيح فرق ساعة كل كاميرا. / Sort every clip on recorded time, correcting each camera's clock offset.

**متى:** حين تصوّر بأكثر من كاميرا وتريد ترتيب اللقطات حسب وقت التصوير مع ضبط فرق ساعة كل كاميرا / when sorting clips from several cameras by recorded time, correcting each camera's clock offset

**كيف:** Read creation_time via ffprobe (or exiftool); measure one offset per camera from a pair of clips of the same moment (--offset prefix=seconds); timeline fps = the most common clip fps; dry-run table: file, time, camera, resolution, fps, gamma.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** متعدد الكاميرات · multicam · chronological · creation_time · ترتيب اللقطات · وقت التصوير · مزامنة الكاميرات · clock offset · sort clips

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1096-akbun-editvideo/2443-akbun-davinciresolve-timeline-chrono/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-04` مجمع لقطات بأسئلة بحث ثنائية اللغة / Per-shot bilingual footage pool (documented)
- `FOOT-05` مكتبة وسائط محلية مع فحص / Local media library with probe (ready)
- `FOOT-07` إعدادات تسجيل الشاشة / Screen-capture defaults (documented)
- `FOOT-08` كشف اللقطات إلى تايملاين / Scene/shot detection → timeline (proven)

### `FOOT-07` — إعدادات تسجيل الشاشة / Screen-capture defaults

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جدول تسجيل في آخر الستوري بورد وإعدادات موحدة لكل اللقطات. / A recording table at the end of the storyboard and one set of capture settings.

**متى:** قبل تسجيل لقطات الشاشة حين تريد إعدادات موحدة للدقة ومعدل الإطارات والصوت والمؤشر / before recording screen captures, for one consistent set of resolution, fps, audio tracks and cursor settings

**كيف:** Native resolution (e.g. 3840×2160), 30 fps matching the timeline, per-window capture, enlarged cursor, mic and system audio on separate tracks, H.264/H.265 CQP 18–20, editor font ≥ 16 pt (terminal 18), notifications off, history cleared.

**المعاملات:** 3840×2160; 30 fps; CQP 18–20

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تسجيل شاشة · screen recording · capture settings · تصوير الشاشة · سكرين ريكورد · إعدادات التسجيل · screencast · system audio

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1096-akbun-editvideo/2449-akbun-vlog-storyboard/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-05` مكتبة وسائط محلية مع فحص / Local media library with probe (ready)
- `FOOT-06` تايملاين زمني متعدد الكاميرات / Chronological multi-camera timeline (documented)
- `FOOT-08` كشف اللقطات إلى تايملاين / Scene/shot detection → timeline (proven)
- `FOOT-09` لوحة لقطات واختيار الغلاف / Contact sheet & cover-frame mining (proven)

### `FOOT-08` — كشف اللقطات إلى تايملاين / Scene/shot detection → timeline

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يكشف القطعات بـ scdet، يرسم لوحة لقطات، يقسّم، ويكتب مواصفة تايملاين بانتقالات. / Detects cuts with scdet, draws a contact sheet, splits, and writes a timeline spec with transitions.

**متى:** حين تريد تقسيم فيديو إلى لقطاته تلقائيًا ومعرفة أماكن القطعات وبناء تايملاين منها / when automatically splitting a video at its cuts into shots, a contact sheet and a timeline spec

**كيف:** python scripts/kmotion.py scenes CLIP.mp4 --sheet shots.png --timeline edit.json [--split DIR --transition fade]; API scenes.detect(clip, threshold=10, min_len=.5). Ran here: tests.test_v6 ScenesTests ok (3 shots found at 2.0 s and 4.0 s ±0.15). Robust variant in decaption.analyse: 90×160 grey diff, threshold max(12, 6×median), > 4× local median over ±15 frames, cuts ≥ 5 frames apart (codecs that smear a cut over two frames).

**المعاملات:** threshold 10 (0–100); min 0.5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كشف اللقطات · قطعات · scene detection · scdet · shots · contact sheet · تقسيم الفيديو · مشاهد · تقطيع تلقائي · split video · cut detection

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/scenes.py`
- `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:113`
- `kosif-studio/motion/decaption.py:63`

#### 7. قدرات قريبة في العائلة

- `FOOT-06` تايملاين زمني متعدد الكاميرات / Chronological multi-camera timeline (documented)
- `FOOT-07` إعدادات تسجيل الشاشة / Screen-capture defaults (documented)
- `FOOT-09` لوحة لقطات واختيار الغلاف / Contact sheet & cover-frame mining (proven)
- `FOOT-10` اختيار أنشط نافذة في اللقطة / Motion-energy window picking (ready)

### `FOOT-09` — لوحة لقطات واختيار الغلاف / Contact sheet & cover-frame mining

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عيّنات عبر المدة كلها في لوحة واحدة، ثم اختيار إطار غلاف يشرح الفيديو بنظرة. / Samples across the whole duration on one sheet, then a cover frame that explains the video at a glance.

**متى:** حين تحتاج صورة غلاف أو ثمبنيل تشرح الفيديو بنظرة، أو لوحة إطارات تلخص المقطع كله / when picking a cover frame or thumbnail that explains the video at a glance, or one sheet summarising it

**كيف:** ffmpeg -i in.mp4 -vf "fps=2,scale=320:-1,tile=3x2" -frames:v 1 sheet.png, or select='gt(scene,0.3)' for change-driven sheets. Skip transition, blurred, first and last frames; shortlist distinct candidates with timestamps; for composed films render the chosen moment straight from the composition at each target size; animated covers loop with a ~0.4 s crossfade; check at phone size. تحققتُ منه في هذه الحاوية (ffmpeg 6.1.1، 2026-10-16) / verified in this container (ffmpeg 6.1.1, 2026-10-16).

**المعاملات:** scene ~0.3; loop crossfade ~0.4 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** لوحة لقطات · غلاف · thumbnail · contact sheet · cover · صورة مصغرة · ثمبنيل · اختيار إطار · frame grab · animated cover

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/101-video-skills/222-video-thumbnails/SKILL.md`
- `kosif-one/projects/ghorba-motion-v2/make_contact.py`

#### 7. قدرات قريبة في العائلة

- `FOOT-07` إعدادات تسجيل الشاشة / Screen-capture defaults (documented)
- `FOOT-08` كشف اللقطات إلى تايملاين / Scene/shot detection → timeline (proven)
- `FOOT-10` اختيار أنشط نافذة في اللقطة / Motion-energy window picking (ready)
- `FOOT-11` قص البدايات المعيبة وتجميع المكرر / Bad-head trimming & duplicate-take grouping (documented)

### `FOOT-10` — اختيار أنشط نافذة في اللقطة / Motion-energy window picking

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لكل خانة إيقاع تُختار أنشط نافذة غير مستخدمة من اللقطة التالية حسب طاقة فرق الإطارات. / For each beat slot the most active unused window of the next clip is chosen by frame-difference energy.

**متى:** حين تقطع لقطات على الإيقاع وتريد اختيار أكثر جزء فيه حركة من كل لقطة بالقياس لا بالتخمين / when cutting to beats and the most active unused window of each clip should be picked by measured motion

**كيف:** montage.energy(clip, fps=6) + montage.pick(…); rank segments by measured motion, never guess. Basma's probe samples every clamp(D/30, 0.5, 2) s for motion, sharpness and brightness and treats motion > 45 as an internal cut.

**المعاملات:** energy at 6 fps

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** طاقة الحركة · motion energy · best window · shot picking · أفضل جزء · لقطة حيوية · قطع على الإيقاع · frame difference · beat slots

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-studio/motion/montage.py:105`
- `kosif-studio/motion/montage.py:42`
- `app/public/js/10_studio.js:1865`

#### 7. قدرات قريبة في العائلة

- `FOOT-08` كشف اللقطات إلى تايملاين / Scene/shot detection → timeline (proven)
- `FOOT-09` لوحة لقطات واختيار الغلاف / Contact sheet & cover-frame mining (proven)
- `FOOT-11` قص البدايات المعيبة وتجميع المكرر / Bad-head trimming & duplicate-take grouping (documented)
- `FOOT-12` تحليل تعريض الصورة ونصائح بالعربية / Image exposure analysis + Arabic fix advice (ready)

### `FOOT-11` — قص البدايات المعيبة وتجميع المكرر / Bad-head trimming & duplicate-take grouping

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مقاطع الهاتف تبدأ بثانية بيضاء أو غير مركزة؛ واللقطات المتقاربة المتشابهة مكررة. / Phone clips start with ~1 s of white or soft frames; near-identical takes are duplicates.

**متى:** عند تنظيف لقطات الموبايل من الثانية الأولى البيضاء أو غير الواضحة وجمع اللقطات المكررة المتشابهة / when cleaning phone clips of white or soft opening frames and grouping near-identical duplicate takes

**كيف:** Compare the first 2 s with a 2–5 s reference window: trim until mean luma is within ±20% and focus (Laplacian variance, cv2 is installed here) recovers; skip clips < 5 s; gimbal cameras need no trim. Duplicates: shot within 2 min and middle-frame luma histograms correlate ≥ 0.9 → keep the sharpest after the user confirms. Large pools: perceptual hash (dHash) with PIL + numpy.

**المعاملات:** ±20% luma; Δt ≤ 2 min; corr ≥ 0.9

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تنظيف · مكرر · duplicates · trim head · laplacian · dhash · لقطات الموبايل · حذف التكرار · بداية بيضاء · phone footage · similar takes

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:numpy` ← python3 -c "import numpy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:opencv` ← python3 -c "import opencv" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1096-akbun-editvideo/2454-davinciresolve-cut-travelflow/SKILL.md`
- `kosif-atlas/skills/3385-fiftyone/13900-fiftyone-find-duplicates/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-09` لوحة لقطات واختيار الغلاف / Contact sheet & cover-frame mining (proven)
- `FOOT-10` اختيار أنشط نافذة في اللقطة / Motion-energy window picking (ready)
- `FOOT-12` تحليل تعريض الصورة ونصائح بالعربية / Image exposure analysis + Arabic fix advice (ready)
- `FOOT-13` دراسة ريل مرجعي بدقة الإطار / Reference-reel study (mimic) (proven)

### `FOOT-12` — تحليل تعريض الصورة ونصائح بالعربية / Image exposure analysis + Arabic fix advice

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يقيس نسب الإضاءة والمدى والقص والظلال المسحوقة ويحكم على التعريض، ثم يقترح الإصلاح بالعربية. / Measures luma percentiles, range, clipping and crushed shadows, gives an exposure verdict and Arabic fix advice.

**متى:** حين يسأل المستخدم هل صورته مظلمة أو محروقة الإضاءة ويريد تشخيص التعريض ونصائح إصلاح بالعربية / when the user asks if a photo is too dark or blown out and wants an exposure verdict with Arabic fix tips

**كيف:** python3 scripts/omni/image_analyze.py IMAGE [--summary]; EXIF-transposed, ≤ 1600 px, Rec.709 luma. Advice triggers: clipped > 2%, crushed > 10%, range < 120, soft, noisy, colour cast, subject off the thirds grid.

**المعاملات:** clip ≥ 250; crushed ≤ 5; over if mean > 185 or clipped > 5%; under if mean < 60 or crushed > 15%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تعريض · تحليل صورة · exposure · histogram · arabic advice · إضاءة الصورة · صورة مظلمة · صورة محروقة · overexposed · underexposed

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:120`
- `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:207`

#### 7. قدرات قريبة في العائلة

- `FOOT-10` اختيار أنشط نافذة في اللقطة / Motion-energy window picking (ready)
- `FOOT-11` قص البدايات المعيبة وتجميع المكرر / Bad-head trimming & duplicate-take grouping (documented)
- `FOOT-13` دراسة ريل مرجعي بدقة الإطار / Reference-reel study (mimic) (proven)
- `FOOT-14` تحليل فيديو مرجعي إلى نبضات / Video breakdown to beats (ready)

### `FOOT-13` — دراسة ريل مرجعي بدقة الإطار / Reference-reel study (mimic)

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يقيس كل حد قطع أو ذوبان أو تعتيم أو انزلاق بالإطار، وأطوال اللقطات، والمظهر، ومنطقة النص، والصوت. / Measures every cut/dissolve/dip/slide boundary to the frame, shot lengths, look, text zone, fades, flashes and audio.

**متى:** حين يريد المستخدم محاكاة ريل مرجعي بدقة الإطار: أماكن القطعات والانتقالات وأطوال اللقطات ومنطقة النص / when matching a reference reel frame-accurately: cuts, dissolves, shot lengths, look, text zone and audio

**كيف:** python scripts/kmotion.py mimic study REF.mp4 --out PROJECT/study → shots.jpg, strip.jpg (frame/0.5 s), text/shot_XX.png, mimic.json. Then mimic layer DIR --erase x0,y0,x1,y1 lifts the fixed design layer as overlay.png (creator handles erased, badges snapped by HSV). Ran here: tests.test_mimic all ok (frame-exact cuts, dissolve place/length, dip, exposure fades inside a shot not counted as cuts). Measure the reference — never copy its media.

**المعاملات:** boundaries cut/dissolve/fadeblack/fadewhite/slide*

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** محاكاة · مرجع · mimic · reference reel · boundaries · تقليد ريل · تحليل ريل · نفس الستايل · transitions · shot lengths

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/mimic.py`
- `100-superskills/skills/kosif-montage-motion/tests/test_mimic.py`
- `100-superskills/skills/kosif-montage-motion/references/mimic.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-11` قص البدايات المعيبة وتجميع المكرر / Bad-head trimming & duplicate-take grouping (documented)
- `FOOT-12` تحليل تعريض الصورة ونصائح بالعربية / Image exposure analysis + Arabic fix advice (ready)
- `FOOT-14` تحليل فيديو مرجعي إلى نبضات / Video breakdown to beats (ready)
- `FOOT-15` تشخيص قبل رفع الدقة / Upscale triage (documented)

### `FOOT-14` — تحليل فيديو مرجعي إلى نبضات / Video breakdown to beats

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نبضات ≤ 3 ث مع لوحة ألوان لكل نبضة وطاقة الحركة والتحريك والانتقال المتوقع والجهارة والإيقاع. / Beats ≤ 3 s with a per-beat hex palette, motion energy, pan, likely transition, loudness, tempo and onsets.

**متى:** حين تريد تفكيك فيديو مرجعي إلى نبضات قصيرة بألوانها وحركتها وإيقاعها لإعادة بنائه مشهدًا مشهدًا / when breaking a reference video into short beats with palette, motion, likely transitions, loudness and tempo

**كيف:** kmotion analyze VIDEO --max-beat 3.0 [--transcribe] [--batch DIR]. For a scene-by-scene recreation schema sample ~12 evenly spaced frames ≤ 1024 px and describe shot type, camera motion, lighting and mood per scene, with scene N's end frame = scene N+1's start.

**المعاملات:** beats ≤ 3 s; 12 samples ≤ 1024 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تحليل · breakdown · palette · tempo · reference · تفكيك فيديو · لوحة ألوان · تحليل مشاهد · scene by scene · beats

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/analyze.py`
- `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/references/books-drive-ledger.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-12` تحليل تعريض الصورة ونصائح بالعربية / Image exposure analysis + Arabic fix advice (ready)
- `FOOT-13` دراسة ريل مرجعي بدقة الإطار / Reference-reel study (mimic) (proven)
- `FOOT-15` تشخيص قبل رفع الدقة / Upscale triage (documented)
- `FOOT-16` مترجم تايملاين JSON / JSON timeline compiler (cuts, ramps, overlays) (proven)

### `FOOT-15` — تشخيص قبل رفع الدقة / Upscale triage

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رفع الدقة يعيد الحجم والحدة لا المعلومة المفقودة. / Upscaling restores size and sharpness, not missing information.

**متى:** قبل رفع دقة صورة أو فيديو منخفض الجودة لتعرف هل التكبير سيفيد أم أن التفاصيل مفقودة أصلًا / before upscaling a low-res photo or video, to judge whether enlarging helps or the detail is simply missing

**كيف:** Jagged edges from low resolution → upscale; uniform focus blur → no; JPEG blocks or ISO noise → partial; pixelated logo → fetch the SVG. Save as name_upN.png, never overwrite the source. Modest scaling with ffmpeg scale flags=lanczos; AI upscalers (Real-ESRGAN, Topaz) need install or keys and run once on the final concat, not per segment. Source rule: long side ≥ 1.5× displayed size at max scale (1080×1920 at 1.12 → ~2400 px).

**المعاملات:** long side ≥ 1.5× display

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** رفع الدقة · upscale · resolution · lanczos · esrgan · تحسين الجودة · تكبير الصورة · صورة مبكسلة · low resolution · blurry image

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2976-pwdev-social-media/12579-asset-upscale/SKILL.md`
- `kosif-tool/playbooks/photos.md:26`

#### 7. قدرات قريبة في العائلة

- `FOOT-13` دراسة ريل مرجعي بدقة الإطار / Reference-reel study (mimic) (proven)
- `FOOT-14` تحليل فيديو مرجعي إلى نبضات / Video breakdown to beats (ready)
- `FOOT-16` مترجم تايملاين JSON / JSON timeline compiler (cuts, ramps, overlays) (proven)
- `FOOT-17` قص دقيق بالإطار / Frame-accurate trim (re-encode) (ready)

### `FOOT-16` — مترجم تايملاين JSON / JSON timeline compiler (cuts, ramps, overlays)

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مواصفة JSON للمقاطع والصور وبطاقات اللون مع قص وزوم وتلوين ومنحدرات سرعة وانتقالات وطبقات نص وترجمة تُرندر في أمر FFmpeg واحد مع بوابة جودة. / A JSON spec of clips, stills and colour cards with in/out, zoom, grade, speed ramps, transitions and text/caption overlays compiles into one FFmpeg render with a QA gate.

**متى:** حين تريد بناء مونتاج كامل من ملف مواصفات بمقاطع وصور وزوم وتلوين وانتقالات ونصوص ورندره مرة واحدة / when describing a whole edit as JSON (clips, stills, zoom, grade, ramps, transitions, text) and rendering it in one pass

**كيف:** kmotion timeline --example edit.json, then timeline.build(spec, out, workers, inspect) → report {seconds, transitions, audio, gate{lufs}}. Ramps [[t, speed]…] → setpts with log(); atempo chain (0.25 → atempo=0.5,atempo=0.5); ratio '1:1' → 1080×1080; overlays: text anim 'rise' with box #00000080, lower-third, logo upper-right ×.5, progress #E7B65A 4 px, captions style 'tiktok'; music ducked under clip audio at −14 LUFS. Ran here: test_v6 TimelineTests (build_film, validation, text_png) and RampTests ok.

**المعاملات:** example: 9:16, 30 fps, bg #0d1b2a; clip zoom 1.0→1.08 grade teal_orange, circleopen 0.6 s; ramp [[0,1],[2,.3],[4,1]]

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تايملاين · مونتاج · timeline · json edit · speed ramp · ffmpeg · مواصفة مونتاج · انتقالات · نص على الفيديو · edit spec · lower third

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:34`
- `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:64`
- `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:896`

#### 7. قدرات قريبة في العائلة

- `FOOT-14` تحليل فيديو مرجعي إلى نبضات / Video breakdown to beats (ready)
- `FOOT-15` تشخيص قبل رفع الدقة / Upscale triage (documented)
- `FOOT-17` قص دقيق بالإطار / Frame-accurate trim (re-encode) (ready)
- `FOOT-18` دمج مقاطع مختلفة دون كسر الصوت / Fit-and-join concat (ready)

### `FOOT-17` — قص دقيق بالإطار / Frame-accurate trim (re-encode)

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اقطع من أي إطار بإعادة الترميز؛ القص بلا ترميز يعمل فقط على الإطارات المفتاحية. / Cut at any frame by re-encoding; stream-copy cuts only work on keyframes.

**متى:** حين تريد قص جزء من فيديو بدءًا من إطار محدد بالضبط دون تجمد الصورة في البداية / when cutting a clip at an exact frame by re-encoding, avoiding the frozen picture of stream-copy cuts

**كيف:** python tools.py trim CLIP --from 3.2 --to 9.8 --out part.mp4 (crf 18 yuv420p, AAC 192k 48 kHz). Raw: ffmpeg -ss T -i in -to D -c:v libx264 -crf 18 -preset slow -c:a aac -b:a 192k -pix_fmt yuv420p -movflags +faststart. -c copy only when the in-point is an I-frame, otherwise 2–5 s of frozen picture; inside compositions prefer non-destructive trim props (data-media-start, trimBefore).

**المعاملات:** crf 18; AAC 192k

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قص · trim · frame accurate · keyframe · re-encode · قص الفيديو · تقطيع مقطع · قص بالثانية · cut clip · frozen frames

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/tools.py:247`
- `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`
- `kosif-atlas/skills/2712-remotion/10436-remotion-markup/ffmpeg.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-15` تشخيص قبل رفع الدقة / Upscale triage (documented)
- `FOOT-16` مترجم تايملاين JSON / JSON timeline compiler (cuts, ramps, overlays) (proven)
- `FOOT-18` دمج مقاطع مختلفة دون كسر الصوت / Fit-and-join concat (ready)
- `FOOT-19` منحدرات السرعة والتصوير البطيء / Speed ramps & slow motion (proven)

### `FOOT-18` — دمج مقاطع مختلفة دون كسر الصوت / Fit-and-join concat

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يدمج المقاطع بالترتيب ويلائم كل واحد في مقاس واحد ويملأ المقاطع الصامتة بصمت. / Joins clips in order, fitting each to one size and filling silent clips with silence so audio never breaks.

**متى:** حين تدمج عدة مقاطع بمقاسات أو معدلات إطارات مختلفة في فيديو واحد دون أن ينقطع الصوت / when joining clips of different sizes or frame rates into one video without the audio breaking

**كيف:** python tools.py concat A.mp4 B.mp4 --out all.mp4 [--size 1080x1920 --fps 30] (pad black, anullsrc 48 kHz stereo). Same-codec clips: concat demuxer (-f concat -safe 0 -i list.txt -c copy). Mixed: per input fps=30,scale=W:H:force_original_aspect_ratio=increase,crop=W:H,setsar=1 then concat=n=N:v=1:a=1.

**المعاملات:** 48 kHz stereo silence fill

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** دمج · concat · join · normalise · دمج الفيديوهات · تجميع مقاطع · لصق مقاطع · merge videos · mixed sizes

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/tools.py:256`
- `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-16` مترجم تايملاين JSON / JSON timeline compiler (cuts, ramps, overlays) (proven)
- `FOOT-17` قص دقيق بالإطار / Frame-accurate trim (re-encode) (ready)
- `FOOT-19` منحدرات السرعة والتصوير البطيء / Speed ramps & slow motion (proven)
- `FOOT-20` قص الصمت / Silence jump-cut (ready)

### `FOOT-19` — منحدرات السرعة والتصوير البطيء / Speed ramps & slow motion

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سرعة متغيرة على اللقطة مع الحفاظ على طبقة الصوت، أو سرعة ثابتة بطيئة. / Variable speed along a clip with pitch-preserved audio, or a constant slow rate.

**متى:** حين يطلب المستخدم تسريع لقطة أو تبطيئها أو سلو موشن متغيرًا مع الحفاظ على طبقة الصوت / when the user wants a speed ramp, slow motion or variable speed on a clip with pitch-preserved audio

**كيف:** Timeline ramp [[t, speed]…] (RampTests ok here) maps time with setpts and chains atempo (each factor 0.5–2). Quick check here: setpts='if(lt(T,1),PTS,PTS*2)' runs. HyperFrames: data-playback-rate 0.1–10 (consumed source = timeline × rate) or a 'rate' lane in data-automation; later starts shift by old/rate. Slow-mo below 0.5× from 30 fps footage stutters — ask for 60/120 fps sources.

**المعاملات:** atempo 0.5–2 per stage; rate 0.1–10

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سرعة · بطيء · speed ramp · slow motion · atempo · setpts · سلو موشن · تسريع الفيديو · تبطيء اللقطة · variable speed · slow mo

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:64`
- `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/creator-editing-recipes.md`
- `kosif-one/vendor/hyperframes/docs/reference/speed-ramps.mdx`

#### 7. قدرات قريبة في العائلة

- `FOOT-17` قص دقيق بالإطار / Frame-accurate trim (re-encode) (ready)
- `FOOT-18` دمج مقاطع مختلفة دون كسر الصوت / Fit-and-join concat (ready)
- `FOOT-20` قص الصمت / Silence jump-cut (ready)
- `FOOT-21` تجميد إطار وتكرار حلقة / Freeze frame & loop (ready)

### `FOOT-20` — قص الصمت / Silence jump-cut

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يحذف الوقفات صورةً وصوتًا في مرور واحد. / Removes pauses from picture and sound in one pass.

**متى:** حين يريد المستخدم حذف الوقفات والسكتات من مقطع كلام صورةً وصوتًا ليصير الإيقاع أسرع / when removing pauses, silences and filler words from a talking clip, picture and sound together

**كيف:** python scripts/kmotion.py silence CLIP.mp4 --out cut.mp4 --threshold -35 --min 0.45 --pad 0.08. Transcript-driven alternative (HyperFrames transcript-cut.mjs): remove ranges, filler words and silences ≥ 0.8 s from word timestamps. Keep 80 ms pads so words never clip.

**المعاملات:** −35 dB; min 0.45 s; pad 0.08 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صمت · قص الصمت · silence · jump cut · filler words · حذف الوقفات · إزالة السكتات · تقطيع الكلام · remove pauses · dead air

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/SKILL.md`
- `kosif-one/vendor/hyperframes/skills/media-use/scripts/transcript-cut.mjs`

#### 7. قدرات قريبة في العائلة

- `FOOT-18` دمج مقاطع مختلفة دون كسر الصوت / Fit-and-join concat (ready)
- `FOOT-19` منحدرات السرعة والتصوير البطيء / Speed ramps & slow motion (proven)
- `FOOT-21` تجميد إطار وتكرار حلقة / Freeze frame & loop (ready)
- `FOOT-22` محرر KOSIF Studio في المتصفح / KOSIF Studio browser montage editor (ready)

### `FOOT-21` — تجميد إطار وتكرار حلقة / Freeze frame & loop

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** امسك لحظة بصورة ثابتة لمدة محددة، أو كرر مقطعًا بذيل يذوب في رأسه. / Hold a moment as a still for N seconds, or loop a clip with its tail dissolving into its head.

**متى:** حين تريد تثبيت لحظة من الفيديو كصورة ثابتة لثوانٍ، أو تكرار مقطع في حلقة بلا قفزة / when holding a moment as a still for a few seconds, or looping a clip with its tail dissolving into its head

**كيف:** Freeze: extract the frame (ffmpeg -ss T -frames:v 1) and place it as an <img> clip (data-start, data-duration), deciding audio continue/trim/silence explicitly. Loop: kmotion loop --seconds 30. Dress the freeze with paper/tape/flash (HyperFrames freeze-frame-dressing, 4 s).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تجميد · freeze frame · hold · loop · تثبيت لقطة · فريز · تكرار المقطع · seamless loop · still frame

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/SKILL.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/creator-editing-recipes.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-19` منحدرات السرعة والتصوير البطيء / Speed ramps & slow motion (proven)
- `FOOT-20` قص الصمت / Silence jump-cut (ready)
- `FOOT-22` محرر KOSIF Studio في المتصفح / KOSIF Studio browser montage editor (ready)
- `FOOT-23` مونتاج مستقل أو متتابع في Remotion / Remotion clip editing: independent vs ripple (install)

### `FOOT-22` — محرر KOSIF Studio في المتصفح / KOSIF Studio browser montage editor

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** محرر محلي بلا رفع: استيراد، مشاهد على تايملاين، طبقات نص وأشكال، صوت، تراجع، حفظ، ومعاينة حية. / A local upload-free editor: import, scenes on a timeline, text/shape layers, soundtrack, undo, save/open, live preview.

**متى:** حين يريد المستخدم محرر مونتاج بسيطًا في المتصفح يعمل محليًا بلا رفع، بتايملاين ونصوص وصوت / when the user wants a simple local in-browser montage editor with timeline, text layers, soundtrack and live preview

**كيف:** Serve the site and open /studio/. Limits: 60 s project, 24 clips, 24 overlays, 48 assets, 200 MB per file, canvas 1280×720 / 720×1280 / 720×720. Projects import into the FFmpeg timeline: POST /api/studio/import → studio_import.convert() (StudioImportTests ok here).

**المعاملات:** 60 s; 24 clips; 200 MB/file

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** محرر · editor · browser · studio · timeline ui · محرر فيديو · مونتاج في المتصفح · معاينة حية · video editor · kosif studio

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:1`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/model.mjs:13`
- `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:528`

#### 7. قدرات قريبة في العائلة

- `FOOT-20` قص الصمت / Silence jump-cut (ready)
- `FOOT-21` تجميد إطار وتكرار حلقة / Freeze frame & loop (ready)
- `FOOT-23` مونتاج مستقل أو متتابع في Remotion / Remotion clip editing: independent vs ripple (install)
- `FOOT-24` تثبيت الاهتزاز / Stabilisation (vidstab 2-pass) (proven)

### `FOOT-23` — مونتاج مستقل أو متتابع في Remotion / Remotion clip editing: independent vs ripple

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Remotion برخصة الشركة؛ @remotion/transitions غير مرخصة MIT / Remotion company license; @remotion/transitions is UNLICENSED on npm. |

**ما هي:** نموذجان: مقاطع بمواضع مطلقة (فراغات وتداخل مسموح) أو تسلسل متتابع يزيح ما بعده. / Two models: absolutely placed clips (gaps/overlaps allowed) or ripple sequences where one change shifts all later clips.

**متى:** حين تبني مونتاج مقاطع في Remotion وتختار بين مواضع مطلقة مستقلة أو تسلسل متتابع يزيح ما بعده / when editing clips in Remotion and choosing absolute placement or ripple sequences that shift later clips

**كيف:** Independent: each <Video> with from/trimBefore/durationInFrames. Ripple: <TransitionSeries> of <TransitionSeries.Sequence durationInFrames> wrapping <Video trimBefore>. Remotion bundles ffmpeg via npx remotion ffmpeg/ffprobe.

**التثبيت:** cd kosif-tool/starters/remotion && npm install

**الوسوم:** ريموشن · remotion · ripple edit · sequence · ترتيب المقاطع · تايملاين · قص المقاطع · transitionseries · trim clips

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10436-remotion-markup/video-editing.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-21` تجميد إطار وتكرار حلقة / Freeze frame & loop (ready)
- `FOOT-22` محرر KOSIF Studio في المتصفح / KOSIF Studio browser montage editor (ready)
- `FOOT-24` تثبيت الاهتزاز / Stabilisation (vidstab 2-pass) (proven)
- `FOOT-25` إزالة التشويش والتوضيح وسلسلة الترميم / Denoise, sharpen & restoration chain (proven)

### `FOOT-24` — تثبيت الاهتزاز / Stabilisation (vidstab 2-pass)

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تثبيت بمرورين عبر vidstab أو deshake عند غيابه — فقط عندما يكون الاهتزاز مقاسًا. / Two-pass vidstab stabilisation (deshake fallback) — only when shake is measured.

**متى:** حين تكون اللقطة مهتزة اهتزازًا مقاسًا فعلًا وتحتاج تثبيتًا دون انحناء الحواف / when a clip has measured camera shake and needs two-pass stabilisation with limited crop

**كيف:** python tools.py stabilize CLIP --out steady.mp4 [--strength 10]: vidstabdetect shakiness=min(10,s) accuracy=15 → vidstabtransform smoothing=2 s optzoom=1 + unsharp 5:5:0.5; fallback deshake rx=ry=32. Ran here on a test clip: method 'vidstab (2-pass)', duration preserved. Prefer similarity mode and keep crop ≤ 10%; if edges bend, lower strength.

**المعاملات:** strength 10; crop ≤ 10%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تثبيت · اهتزاز · stabilize · vidstab · deshake · فيديو مهزوز · لقطة مهتزة · رعشة الكاميرا · shaky video · steady

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/tools.py:303`
- `kosif-atlas/skills/1096-akbun-editvideo/2454-davinciresolve-cut-travelflow/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-22` محرر KOSIF Studio في المتصفح / KOSIF Studio browser montage editor (ready)
- `FOOT-23` مونتاج مستقل أو متتابع في Remotion / Remotion clip editing: independent vs ripple (install)
- `FOOT-25` إزالة التشويش والتوضيح وسلسلة الترميم / Denoise, sharpen & restoration chain (proven)
- `FOOT-26` مسح الترجمة المحروقة / Burned-caption eraser (decaption) (proven)

### `FOOT-25` — إزالة التشويش والتوضيح وسلسلة الترميم / Denoise, sharpen & restoration chain

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نظّف ضوضاء الإضاءة المنخفضة واستعد حدة الحواف، ثم سوداء أنظف وانحناء إضاءات ودرجات وسطى أدفأ. / Clean low-light noise and restore edges, then cleaner blacks, highlight roll-off and warmer mids.

**متى:** حين تكون اللقطة مشوشة من الإضاءة المنخفضة أو باهتة الحواف وتحتاج تنظيفًا وتوضيحًا وتحسين ألوان / when low-light footage is noisy or soft and needs denoise, sharpening and a gentle restoration grade

**كيف:** Fast: hqdn3d=4:3:6:4.5,unsharp=5:5:0.6; better/slower: nlmeans=s=3..5; archival chroma: chromanr. Reel chain: hqdn3d=1.2:1.2:3:3, Lanczos reframe, eq=contrast=1.12:brightness=-0.015:saturation=1.07:gamma=0.97, curves, colorbalance, cas=0.3. تحققتُ منه في هذه الحاوية (ffmpeg 6.1.1، 2026-10-16) / verified in this container (ffmpeg 6.1.1, 2026-10-16).

**المعاملات:** hqdn3d 4:3:6:4.5; nlmeans s 3–5; cas 0.3

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تشويش · ترميم · denoise · sharpen · restoration · hqdn3d · إزالة النويز · توضيح الصورة · إضاءة منخفضة · noise reduction · low light

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md`
- `kosif-one/tools/kosif-studio/motion/reel.py:35`

#### 7. قدرات قريبة في العائلة

- `FOOT-23` مونتاج مستقل أو متتابع في Remotion / Remotion clip editing: independent vs ripple (install)
- `FOOT-24` تثبيت الاهتزاز / Stabilisation (vidstab 2-pass) (proven)
- `FOOT-26` مسح الترجمة المحروقة / Burned-caption eraser (decaption) (proven)
- `FOOT-27` تمويه الوجوه والمناطق / Face & region privacy masks (install)

### `FOOT-26` — مسح الترجمة المحروقة / Burned-caption eraser (decaption)

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يجد حبر الترجمة الأبيض أو الأصفر بحد أسود، ويعيد بناء اللقطات الثابتة من وسيط البكسل ويرمم المتحركة. / Finds white/yellow caption ink next to a black outline; rebuilds locked-off shots from the per-pixel median and inpaints moving shots.

**متى:** حين يريد المستخدم إزالة ترجمة محروقة بيضاء أو صفراء من الفيديو وإعادة بناء ما تحتها / when erasing burned-in white or yellow subtitles from a video and rebuilding the picture underneath

**كيف:** python decaption.py VIDEO --out CLEAN.mp4 [--band 0.45:0.56] [--keep-credit] [--report]. Ran here: test_decaption_erases_a_burned_caption ok.

**المعاملات:** white V>205 S<55; yellow H 16–38 S>110 V>150; dark outline V<70 within 9 px; masks ±3 frames; Telea inpaint r 9; output crf 12

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ترجمة محروقة · decaption · remove subtitles · inpaint · مسح الكتابة · حذف الترجمة · إزالة النص · hardcoded subtitles · erase text

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/decaption.py:38`
- `kosif-studio/motion/decaption.py:99`
- `kosif-studio/tests/test_studio.py:850`

#### 7. قدرات قريبة في العائلة

- `FOOT-24` تثبيت الاهتزاز / Stabilisation (vidstab 2-pass) (proven)
- `FOOT-25` إزالة التشويش والتوضيح وسلسلة الترميم / Denoise, sharpen & restoration chain (proven)
- `FOOT-27` تمويه الوجوه والمناطق / Face & region privacy masks (install)
- `FOOT-28` مفتاح اللون الأخضر / Chroma key (proven)

### `FOOT-27` — تمويه الوجوه والمناطق / Face & region privacy masks

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** وجوه أو مناطق تُبكسل أو تُموه أو تُغطى في كل إطار مع تتبع وهامش واستمرار عند ضياع الكشف، والصوت كما هو. / Faces or regions pixelated, blurred or boxed every frame with tracking, margin and hold through misses; audio untouched.

**متى:** حين تحتاج إخفاء وجوه أشخاص أو منطقة حساسة في الفيديو ببكسلة أو تمويه يتتبعها في كل إطار / when hiding faces or a sensitive region in a video with tracked blur, pixelation or boxes, audio untouched

**كيف:** python scripts/kmotion.py privacy CLIP.mp4 --out safe.mp4 --mode pixelate\|blur\|box [--strength 18 --pad 0.25 --every 2 --hold 0.6] [--region x,y,w,h[,from,to]]. Detectors YuNet > Haar > skin. Here cv2 5.0 is present but has no Haar data, the YuNet ONNX is not shipped, and the skin fallback needs scipy — the test errors on that import. Manual regions work. Rules: faces ≥ 40 px tall at 4K are identifiable; one soft window over the whole path (softness ≥ 30%); mosaic block ≈ face height/4. ffmpeg crop→pixelize→overlay is verified here.

**المعاملات:** block = face/4; softness ≥ 30%; strength 18

**التثبيت:** pip install scipy # or put face_detection_yunet_2023mar.onnx in scripts/kit/models/

**الوسوم:** خصوصية · تمويه الوجوه · privacy · face blur · pixelate · mosaic · إخفاء الوجه · تغبيش · بكسلة · anonymize · blur region

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:opencv` ← python3 -c "import opencv" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:scipy` ← python3 -c "import scipy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:onnxruntime` ← python3 -c "import onnxruntime" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `model:yunet` ← النموذج المحلي موجود في مجلد النماذج قبل التشغيل
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/privacy.py`
- `100-superskills/skills/kosif-montage-motion/scripts/faces.py`
- `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:132`
- `kosif-atlas/skills/1096-akbun-editvideo/2456-davinciresolve-face-mosaic/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-25` إزالة التشويش والتوضيح وسلسلة الترميم / Denoise, sharpen & restoration chain (proven)
- `FOOT-26` مسح الترجمة المحروقة / Burned-caption eraser (decaption) (proven)
- `FOOT-28` مفتاح اللون الأخضر / Chroma key (proven)
- `FOOT-29` تعديل الصورة: إعادة تلوين تحفظ الظلال / Picture edits: shading-preserving recolour (proven)

### `FOOT-28` — مفتاح اللون الأخضر / Chroma key

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أزل خلفية خضراء أو زرقاء أو سادة وركّب المتحدث فوق لقطات أو رسوم جديدة. / Remove a green, blue or plain backdrop and composite the speaker over new footage or graphics.

**متى:** حين يصور المتحدث أمام شاشة خضراء أو زرقاء ويريد استبدال الخلفية بلقطات أو رسوم جديدة / when removing a green, blue or plain backdrop to composite the speaker over new footage or graphics

**كيف:** [fg]chromakey=0x00FF00:similarity=0.10..0.18:blend=0.05..0.1,despill=type=green[k];[bg][k]overlay (YUV sources chromakey, RGB colorkey). تحققتُ منه في هذه الحاوية (ffmpeg 6.1.1، 2026-10-16) / verified in this container (ffmpeg 6.1.1, 2026-10-16). Browser variant (Basma chromaMask): YCbCr chroma distance with a luma term, smoothstep soft edge between 0.55·tol and tol, mask blur W/360; auto key from four 8×8 corner patches.

**المعاملات:** similarity 0.10–0.18; blend 0.05–0.1; Basma key #00b140 tol 0.22

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كروما · شاشة خضراء · chroma key · green screen · despill · تغيير الخلفية · خلفية خضراء · كروما كي · blue screen · background replace

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md`
- `app/public/js/00_editor.js:2468`

#### 7. قدرات قريبة في العائلة

- `FOOT-26` مسح الترجمة المحروقة / Burned-caption eraser (decaption) (proven)
- `FOOT-27` تمويه الوجوه والمناطق / Face & region privacy masks (install)
- `FOOT-29` تعديل الصورة: إعادة تلوين تحفظ الظلال / Picture edits: shading-preserving recolour (proven)
- `FOOT-30` معالجة الصور بـ ImageMagick / ImageMagick still post-processing (ready)

### `FOOT-29` — تعديل الصورة: إعادة تلوين تحفظ الظلال / Picture edits: shading-preserving recolour

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** «غيّر الذهبي إلى الأزرق» يُفهم محليًا بلا ذكاء اصطناعي، ويعيد التلوين مع حفظ الطيات والظلال. / 'Change the gold to blue' is parsed locally without AI and recoloured while keeping folds and shadows.

**متى:** حين يطلب المستخدم تغيير لون شيء في الصورة مثل «خلي القميص أحمر» مع بقاء الظلال والطيات / when the user asks to change an object's colour in a photo, e.g. 'make the shirt red', keeping folds and shadows

**كيف:** python edit_pack.py photo.jpg 'make the shirt red'; recolor(img, src_hex, dst_hex, tolerance=40, region, keep_shading=True) scales HSV saturation/value; also adjust, tint, paint, write, erase (blur-fill), flip. 18 Arabic colour names (ذهبي #d4a53a، كحلي #1f2d6b، عنابي #7b1e2b …). The original is kept as a <<KOSIF:ORIGINAL:sha>> key so any AI edits a program, not the bytes. Ran here: local-edit and colour-request tests ok.

**المعاملات:** tolerance 34–42; HSV match ≤ .6

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إعادة تلوين · تعديل صورة · recolor · photo edit · arabic colours · تغيير اللون · غير لون · استبدال لون · change color · color swap

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/edit_pack.py:36`
- `kosif-studio/edit_pack.py:226`
- `kosif-studio/tests/test_studio.py:410`

#### 7. قدرات قريبة في العائلة

- `FOOT-27` تمويه الوجوه والمناطق / Face & region privacy masks (install)
- `FOOT-28` مفتاح اللون الأخضر / Chroma key (proven)
- `FOOT-30` معالجة الصور بـ ImageMagick / ImageMagick still post-processing (ready)
- `FOOT-31` عزل الشخص بقناع شفاف / Person matte / background removal (install)

### `FOOT-30` — معالجة الصور بـ ImageMagick / ImageMagick still post-processing

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قص ملء، إزالة الأبيض إلى شفافية، تقليم، تحويل وتدفئة قبل التحريك. / Fill-crop, white-to-alpha, trim, convert and warm grade before animating.

**متى:** قبل تحريك صورة ثابتة حين تحتاج قصها لمقاس محدد أو جعل الأبيض شفافًا أو تقليمها أو تدفئة ألوانها / before animating a still: fill-crop to size, white to transparent, trim, convert to WebP or warm the grade

**كيف:** Here the binary is 'convert' (ImageMagick 6), not 'magick'. Fill-crop: -resize WxH^ -gravity center -extent WxH; white→alpha: -fuzz 10% -transparent white, then -channel A -blur 0x1 -level 50%,100%; -trim +repage; WebP -quality 85; warm -modulate 100,110,105; -contrast-stretch 2%x1%. Single-colour logo backdrop alternative (Basma removeImgBG): corner colours must agree (spread ≤ 70), edge flood fill, anti-aliased alpha.

**المعاملات:** fuzz 10–15%; q 85

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** imagemagick · convert · قص · شفافية · crop · transparent · تجهيز الصور · إزالة الأبيض · تحويل الصيغة · webp · resize

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/881-codex-seo/1954-seo-image-gen`
- `app/public/js/00_editor.js:2572`

#### 7. قدرات قريبة في العائلة

- `FOOT-28` مفتاح اللون الأخضر / Chroma key (proven)
- `FOOT-29` تعديل الصورة: إعادة تلوين تحفظ الظلال / Picture edits: shading-preserving recolour (proven)
- `FOOT-31` عزل الشخص بقناع شفاف / Person matte / background removal (install)
- `FOOT-32` عنوان خلف المتحدث / Title behind the speaker (documented)

### `FOOT-31` — عزل الشخص بقناع شفاف / Person matte / background removal

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames Apache-2.0؛ مكتبة u2net وأوزانها تُنزَّل عند أول تشغيل / HyperFrames is Apache-2.0; u2net weights download on first run. |

**ما هي:** يخرج قصاصة شفافة للمتحدث (webm/mov/png ألفا) مع لوح خلفي معكوس اختياري. / Produces a transparent cut-out of the presenter (webm/mov/png alpha) with an optional inverse plate.

**متى:** حين يريد المستخدم عزل المتحدث عن خلفيته في فيديو أو صورة وإخراجه بخلفية شفافة / when cutting the presenter out of footage or stills as a transparent alpha cut-out, with an optional background plate

**كيف:** npx hyperframes remove-background presenter.mp4 -o presenter.webm [--background-output plate.mp4] [--quality fast\|balanced\|best (crf 30/18/12)] [--device auto\|cpu]; u2net human seg at 320×320, ~9 fps on CoreML (slower on CPU here). Alternatives: pip install rembg (stills/frames), MediaPipe selfie segmentation in the browser (CDN), Transformers.js image-segmentation / depth-estimation in Node (models from Hugging Face, reachable).

**المعاملات:** 320×320 matte; quality crf 30/18/12

**التثبيت:** npx hyperframes remove-background in.mp4 -o out.webm

**الوسوم:** عزل · إزالة الخلفية · matte · remove background · rembg · segmentation · حذف الخلفية · قص الشخص · خلفية شفافة · cutout · alpha video

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:torch` ← python3 -c "import torch" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:rembg` ← python3 -c "import rembg" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `pip:mediapipe` ← python3 -c "import mediapipe" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/docs/guides/remove-background.mdx`
- `kosif-one/vendor/hyperframes/skills/media-use/audio/references/remove-background.md`
- `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/matte.cjs`
- `app/public/js/00_editor.js:2466`

#### 7. قدرات قريبة في العائلة

- `FOOT-29` تعديل الصورة: إعادة تلوين تحفظ الظلال / Picture edits: shading-preserving recolour (proven)
- `FOOT-30` معالجة الصور بـ ImageMagick / ImageMagick still post-processing (ready)
- `FOOT-32` عنوان خلف المتحدث / Title behind the speaker (documented)
- `FOOT-33` متحدث مقصوص فوق عوالم متبدلة / Rotoscoped speaker over swapped worlds (seen)

### `FOOT-32` — عنوان خلف المتحدث / Title behind the speaker

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عنوان كبير يظهر خلف جسد المتحدث ووجهه واضح. / A large title appears behind the speaker's body while the face stays clear.

**متى:** حين يريد المستخدم عنوانًا كبيرًا يظهر خلف جسم المتحدث بينما وجهه يبقى ظاهرًا أمامه / when a big headline should appear behind the speaker's body while the face stays in front and clear

**كيف:** Three layers in lockstep with the same data-start: z1 full mp4 base, z2 headline, z3 alpha webm cut-out. Timing 0–1 s shot, 1–2 s title reveal, 2–5 s hold. Check hair and hands; never cover eyes or mouth. Photo version: title sandwiched between background and cut-out subject (≤ 3 layers).

**المعاملات:** 5 s; 3 layers

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نص خلف الشخص · text behind subject · occlusion · podcast · عنوان خلف المتحدث · كتابة ورا الشخص · تأثير العمق · depth title · layered text

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:z3` ← python3 -c "import z3" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/composition-patterns.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md`
- `kosif-tool/playbooks/photos.md:18-19`

#### 7. قدرات قريبة في العائلة

- `FOOT-30` معالجة الصور بـ ImageMagick / ImageMagick still post-processing (ready)
- `FOOT-31` عزل الشخص بقناع شفاف / Person matte / background removal (install)
- `FOOT-33` متحدث مقصوص فوق عوالم متبدلة / Rotoscoped speaker over swapped worlds (seen)
- `FOOT-34` تسمية متتبعة ودائرة اهتمام / Tracked callout & attention ring (ready)

### `FOOT-33` — متحدث مقصوص فوق عوالم متبدلة / Rotoscoped speaker over swapped worlds

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** المتحدث مقصوص بحد أبيض فوق خلفية مختلفة لكل جملة. / The speaker, cut out with a white outline, sits over a different backdrop per sentence.

**متى:** حين تريد قص المتحدث بحد أبيض كالملصق وتبديل الخلفية خلفه مع كل جملة / when cutting the speaker out with a white sticker outline and swapping the backdrop at each sentence

**كيف:** Matte per frame (FOOT-31), add a 6–8 px white outline and a 20 px soft shadow, swap the backdrop on sentence boundaries from words.json.

**المعاملات:** outline 6–8 px; shadow 20 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قص المتحدث · rotoscope · sticker outline · backdrop swap · تغيير الخلفية · ملصق · حد أبيض · sentence sync · cutout

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `style:pm-sab8a-364a5a`

#### 7. قدرات قريبة في العائلة

- `FOOT-31` عزل الشخص بقناع شفاف / Person matte / background removal (install)
- `FOOT-32` عنوان خلف المتحدث / Title behind the speaker (documented)
- `FOOT-34` تسمية متتبعة ودائرة اهتمام / Tracked callout & attention ring (ready)
- `FOOT-35` إدراج بمنظور مثبت بأربع نقاط / Planar corner-pin inserts (documented)

### `FOOT-34` — تسمية متتبعة ودائرة اهتمام / Tracked callout & attention ring

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقطة وخط قصير مثبتان على جزء متحرك، أو دائرة رفيعة تلاحق تفصيلة صغيرة أثناء الشرح. / A dot and short leader stay pinned to a moving part, or a thin ring follows a small detail during the explanation.

**متى:** حين تشرح جزءًا صغيرًا متحركًا في اللقطة وتريد نقطة بخط تسمية أو دائرة تلاحقه / when a dot with a short label line, or a thin ring, must stay pinned to a moving detail while it is explained

**كيف:** Track to a null with an OpenCV point tracker (cv2 5.0 is importable here) or manual keys every few frames + interpolation; draw the overlay in HTML at the tracked coordinates. Hide the label when the target is occluded or leaves frame; never cover the evidence. Timing: 0–1 intro, 1–2 line appears, 2–6 track.

**المعاملات:** 6 s / 5 s beats

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تتبع · tracking · callout · attention ring · opencv · تتبع حركة · دائرة تمييز · تسمية متحركة · motion tracking · label

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:opencv` ← python3 -c "import opencv" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-32` عنوان خلف المتحدث / Title behind the speaker (documented)
- `FOOT-33` متحدث مقصوص فوق عوالم متبدلة / Rotoscoped speaker over swapped worlds (seen)
- `FOOT-35` إدراج بمنظور مثبت بأربع نقاط / Planar corner-pin inserts (documented)
- `FOOT-36` تجميد الشخص والعالم يمشي / Freeze the subject, keep the world moving (documented)

### `FOOT-35` — إدراج بمنظور مثبت بأربع نقاط / Planar corner-pin inserts

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ملصق يتبع منظور حائط والكاميرا تتحرك، أو بطاقة في يد تصبح رسمًا يتبع ميلها والأصابع فوقها. / A sticker follows a wall's perspective as the camera moves, or a card held in a hand becomes a diagram following its tilt with fingers on top.

**متى:** حين تريد إدخال ملصق أو رسم على حائط أو بطاقة في اليد بحيث يتبع منظورها وحركة الكاميرا / when inserting a sticker or diagram onto a wall or a hand-held card so it follows the perspective as the camera moves

**كيف:** Four-corner keyframes (manual or an OpenCV homography) → CSS matrix3d per frame, or ffmpeg perspective=x0:y0:x1:y1:x2:y2:x3:y3 (تحققتُ منه في هذه الحاوية (ffmpeg 6.1.1، 2026-10-16) / verified in this container (ffmpeg 6.1.1, 2026-10-16).). Add matching grain and blur; finger masks + their shadow stay on top. No fake certificates or ads.

**المعاملات:** 6 s each

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** منظور · corner pin · planar track · homography · insert · أربع زوايا · تركيب صورة · تتبع سطح · perspective · matrix3d

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:opencv` ← python3 -c "import opencv" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md`
- `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-33` متحدث مقصوص فوق عوالم متبدلة / Rotoscoped speaker over swapped worlds (seen)
- `FOOT-34` تسمية متتبعة ودائرة اهتمام / Tracked callout & attention ring (ready)
- `FOOT-36` تجميد الشخص والعالم يمشي / Freeze the subject, keep the world moving (documented)
- `FOOT-37` سينماغراف / Cinemagraph (install)

### `FOOT-36` — تجميد الشخص والعالم يمشي / Freeze the subject, keep the world moving

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** المؤدي يتجمد داخل الإطار والخلفية القصيرة تستمر. / The performer freezes while a short background keeps moving.

**متى:** حين تريد أن يتجمد الشخص في الكادر بينما الخلفية تستمر في الحركة، أو تكرار وضعياته كأشباح زمنية / when the performer freezes while the background keeps moving, or for spaced ghost poses as time markers

**كيف:** 0–1 s motion, 1–3 s subject frozen, 3–4 s return: frozen frame of the person + matte overlaid on the running plate; a clean plate where the original body ghosts through. Chronophotography variant: 3 frozen, spaced poses with an opacity/colour gradient, then motion resumes — copies are time markers, not extra people.

**المعاملات:** 4 s; 3 ghost poses in 5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تجميد · freeze subject · chronophotography · ghost poses · تجميد الشخص · إيقاف الزمن · أشباح · time freeze · clean plate

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-music-sports.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-34` تسمية متتبعة ودائرة اهتمام / Tracked callout & attention ring (ready)
- `FOOT-35` إدراج بمنظور مثبت بأربع نقاط / Planar corner-pin inserts (documented)
- `FOOT-37` سينماغراف / Cinemagraph (install)
- `FOOT-38` مقارنة قبل وبعد صادقة / Honest before/after wipe (documented)

### `FOOT-37` — سينماغراف / Cinemagraph

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames Apache-2.0؛ مكتبة u2net وأوزانها تُنزَّل عند أول تشغيل / HyperFrames is Apache-2.0; u2net weights download on first run. |

**ما هي:** صورة ثابتة فيها منطقة واحدة حية (بخار فوق فنجان) بدورة تقسم المدة فتتكرر بلا قفزة. / A still with one feathered living region (steam over a cup) whose period divides the duration so it loops seamlessly.

**متى:** حين تريد صورة ثابتة فيها جزء واحد يتحرك كالبخار فوق الفنجان ويتكرر بلا قفزة / when turning a still into a seamless loop where only one masked region, like steam over a cup, moves

**كيف:** Driven only by seek time; period divides the clip length. HyperFrames block cinemagraph (10 s, swap the placeholder for your still + masked looping video).

**المعاملات:** 10 s; period \| duration

**التثبيت:** npx hyperframes add cinemagraph

**الوسوم:** سينماغراف · cinemagraph · living photo · loop · صورة متحركة · صورة حية · جزء متحرك · moving photo · seamless loop

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/registry/blocks/cinemagraph/cinemagraph.html`

#### 7. قدرات قريبة في العائلة

- `FOOT-35` إدراج بمنظور مثبت بأربع نقاط / Planar corner-pin inserts (documented)
- `FOOT-36` تجميد الشخص والعالم يمشي / Freeze the subject, keep the world moving (documented)
- `FOOT-38` مقارنة قبل وبعد صادقة / Honest before/after wipe (documented)
- `FOOT-39` كين بيرنز الصحيح / Ken Burns done well (proven)

### `FOOT-38` — مقارنة قبل وبعد صادقة / Honest before/after wipe

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خط فاصل يتحرك بين الأصل والنتيجة بنفس الكادر. / A divider moves between original and result in the same framing.

**متى:** حين تعرض الفرق قبل التعديل وبعده بخط فاصل يتحرك على نفس الكادر / when showing before vs after with a moving divider over the same framing, without changing light or lens

**كيف:** 0–1 s define both, 1–4 s divider moves, 4–6 s stop; linear mask + 2 px divider + date/condition label. Never change light or lens between the sides. Local: HTML clip-path inset, or ffmpeg overlay with an animated crop. Matte-vs-composite split (key pass left, final right) is a strong compositing reveal.

**المعاملات:** 6 s; divider 2 px; wipe 600 ms–1.2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قبل وبعد · before after · split · comparison · مقارنة النتيجة · خط فاصل · سلايدر مقارنة · wipe · divider

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-product-ads.md`
- `style:pm-blueoctopusai-dd17bd`

#### 7. قدرات قريبة في العائلة

- `FOOT-36` تجميد الشخص والعالم يمشي / Freeze the subject, keep the world moving (documented)
- `FOOT-37` سينماغراف / Cinemagraph (install)
- `FOOT-39` كين بيرنز الصحيح / Ken Burns done well (proven)
- `FOOT-40` بارالاكس مستوي بمعاملات عمق / Planar parallax with depth factors (ready)

### `FOOT-39` — كين بيرنز الصحيح / Ken Burns done well

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** دفع أو تحريك بسرعة ثابتة، حركات متناوبة، بلا توقفات منحنية، والتحريك من اليمين للعربية. / Constant-velocity push or pan, alternating moves, no eased stops; pans run right-to-left for Arabic.

**متى:** حين تحرك صورًا ثابتة بزوم أو تحريك هادئ بسرعة ثابتة، مع اتجاه من اليمين لليسار للعربي / when animating still photos with a constant-speed push or pan, alternating moves and right-to-left pans for Arabic

**كيف:** 1.00→1.06 over 4–6 s (1–1.5%/s), ceiling 1.12, pan < 6% of width; linear or cubic-bezier(0.37,0,0.63,1) before a cut. ffmpeg: zoompan=z='min(1+0.0004*on,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1080x1920:fps=30 (تحققتُ منه في هذه الحاوية (ffmpeg 6.1.1، 2026-10-16) / verified in this container (ffmpeg 6.1.1, 2026-10-16). — feed a source ≥ 1.5× the output to avoid zoompan jitter). Documentary hold: push 1.055 + pan 4% over 4.5 s, lower third enters 600–1100 ms.

**المعاملات:** 1.00→1.06 / 4–6 s; max 1.12

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كين بيرنز · ken burns · zoompan · push · photo motion · تحريك الصور · زوم على الصورة · زوم بطيء · slow zoom · pan

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/photos.md:32`
- `kosif-tool/playbooks/photos.md:48-55`
- `100-superskills/skills/trend-animation-styles/references/styles.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-37` سينماغراف / Cinemagraph (install)
- `FOOT-38` مقارنة قبل وبعد صادقة / Honest before/after wipe (documented)
- `FOOT-40` بارالاكس مستوي بمعاملات عمق / Planar parallax with depth factors (ready)
- `FOOT-41` كشف بارالاكس ثلاثي ومن الكولاج إلى البطل / Three-layer reveal & collage → hero (documented)

### `FOOT-40` — بارالاكس مستوي بمعاملات عمق / Planar parallax with depth factors

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إزاحة كل طبقة = إزاحة الكاميرا × معامل عمقها، مع حركة مقصودة وانجراف دائم بجيبين. / Layer offset = camera offset × depth factor, plus an intentional move and a perpetual two-sine drift.

**متى:** حين تحول صورة ثابتة إلى مشهد بعمق بطبقات تتحرك بسرعات مختلفة مع انجراف خفيف دائم / when turning a layered still into 2.5D depth with per-layer depth factors and a gentle perpetual drift

**كيف:** x = 6·sin(2πt/7) + 4·sin(2πt/11), y periods 9 s / 13 s; one camera function (pan + drift + linear zoom) × depth in both Remotion and the Canvas seek version (ParallaxPhoto, 1080×1920, 5 s). Skip parallax when the long side < 1600 px or the subject can't be separated. Oversize each layer by 2× max travel + 4% and put a 1.3× copy blurred 24 px behind to hide edges; depth blur ~1 px per 100 px of distance (bg 3, mid 1), never on the subject.

**المعاملات:** bg 0.15 · mid 0.45 · subject 1.0 · occluder 1.4; zoom ≤ 1.10; drift ≤ 12 px; pans 30–60 px/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بارالاكس · parallax · 2.5d · depth layers · photo · عمق الصورة · طبقات متحركة · تحريك الصور · camera drift · depth effect

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/photos.md:34`
- `kosif-tool/playbooks/photos.md:103-185`
- `kosif-tool/playbooks/photos.md:20`
- `kosif-tool/playbooks/photos.md:22`
- `kosif-tool/styles/parallax-2d/STYLE.json`

#### 7. قدرات قريبة في العائلة

- `FOOT-38` مقارنة قبل وبعد صادقة / Honest before/after wipe (documented)
- `FOOT-39` كين بيرنز الصحيح / Ken Burns done well (proven)
- `FOOT-41` كشف بارالاكس ثلاثي ومن الكولاج إلى البطل / Three-layer reveal & collage → hero (documented)
- `FOOT-42` حماية النص فوق الصور واللقطات / Text protection over photos & footage (documented)

### `FOOT-41` — كشف بارالاكس ثلاثي ومن الكولاج إلى البطل / Three-layer reveal & collage → hero

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طبقات تظهر، الشخص يقفز، تحريك 40 بكسل، والعنوان ينزلق بين الخلفية والشخص؛ أو شبكة صور تنهار إلى صورة بطل. / Layers fade, the subject pops, a 40 px pan, the title slides between background and subject; or a photo grid collapses to one hero.

**متى:** حين تريد كشف صورة بطبقات يقفز فيها الشخص ويمر العنوان خلفه، أو شبكة صور تنهار إلى صورة واحدة / when revealing a layered photo with the title sliding behind the subject, or a photo grid collapsing to one hero

**كيف:** Reveal: bg scale 1.15, mid 1.06; subject 200–800 ms spring 14/120; pan 400–2600 ms; title 900–1400 ms; push 1.5%/s. Collage: 2×3 grid enters from the top-right (RTL) with 60 ms stagger over 400 ms, drifts 20 px, exits 250 ms with 40 ms stagger, hero pushes 1.06.

**المعاملات:** subject spring 14/120; grid stagger 60 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كشف · كولاج · parallax reveal · collage · hero photo · شبكة صور · كشف الصورة · عنوان بين الطبقات · photo grid · layer reveal

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/photos.md:57-65`
- `kosif-tool/playbooks/photos.md:67-74`

#### 7. قدرات قريبة في العائلة

- `FOOT-39` كين بيرنز الصحيح / Ken Burns done well (proven)
- `FOOT-40` بارالاكس مستوي بمعاملات عمق / Planar parallax with depth factors (ready)
- `FOOT-42` حماية النص فوق الصور واللقطات / Text protection over photos & footage (documented)
- `FOOT-43` صورة أرشيف تنفتح على الحاضر / Archive photo opens onto the present (documented)

### `FOOT-42` — حماية النص فوق الصور واللقطات / Text protection over photos & footage

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** النص فوق صورة مزدحمة يجلس على تدرج لا مربع أسود، ويُتحقق من التباين إطارًا بإطار. / Text over a busy picture sits on a gradient scrim, not a black box, and contrast is checked per frame.

**متى:** حين يكون النص فوق صورة أو لقطة مزدحمة صعب القراءة ويحتاج تدرجًا خلفه وفحص تباين / when text over a busy photo or footage is hard to read and needs a gradient scrim and per-frame contrast checks

**كيف:** Gradient 0.6→0 over 35% of frame height, contrast ≥ 4.5:1, text ≥ 36 px; or a 40–60% black scrim, a solid pill, or stroke/shadow. Verify luminance in the caption band with ffmpeg signalstats YAVG per frame (تحققتُ منه في هذه الحاوية (ffmpeg 6.1.1، 2026-10-16) / verified in this container (ffmpeg 6.1.1, 2026-10-16).). Dark product plates: navy multiply overlay 40–55% + vignette so oversized type reads.

**المعاملات:** scrim 0.6→0 / 35% H; contrast ≥ 4.5:1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حماية النص · تباين · scrim · legibility · contrast · signalstats · وضوح النص · قراءة النص · تدرج خلف النص · readability · text over video

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/photos.md:23`
- `kosif-tool/playbooks/photos.md:197`
- `kosif-atlas/skills/1503-universal-design-principles/3825-legibility-contrast-and-spacing/SKILL.md`
- `style:pm-deifosv-04e4d3`

#### 7. قدرات قريبة في العائلة

- `FOOT-40` بارالاكس مستوي بمعاملات عمق / Planar parallax with depth factors (ready)
- `FOOT-41` كشف بارالاكس ثلاثي ومن الكولاج إلى البطل / Three-layer reveal & collage → hero (documented)
- `FOOT-43` صورة أرشيف تنفتح على الحاضر / Archive photo opens onto the present (documented)
- `FOOT-44` قواعد الصور للعربية / RTL photo layout rules (documented)

### `FOOT-43` — صورة أرشيف تنفتح على الحاضر / Archive photo opens onto the present

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إطار صورة قديمة يتمدد حتى يطابق المكان نفسه في لقطة حديثة ثم يذوب. / An old print's frame expands to match the same place in modern footage, then dissolves.

**متى:** حين تريد أن تتمدد صورة أرشيف قديمة حتى تطابق المكان نفسه في لقطة حديثة ثم تذوب فيها / when an old archive print should expand to match the same place in modern footage, then dissolve into it

**كيف:** 0–2 s photo, 2–5 s match (perspective corner pin + scale), 5–8 s modern scene with a tuned dissolve; show the photo date; never imply a false location match; sound moves from old to modern ambience. Documentary style: warm dark #15130F, ivory #EFE6D8, red #C0392B; Amiri 700 + IBM Plex Sans Arabic 500; Ken Burns 1.0→1.08 over 6 s.

**المعاملات:** 8 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أرشيف · وثائقي · archive · documentary · then and now · صورة قديمة · الماضي والحاضر · زمان والآن · old photo · match dissolve

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-cinematic-titles.md`
- `100-superskills/skills/trend-animation-styles/references/styles.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-41` كشف بارالاكس ثلاثي ومن الكولاج إلى البطل / Three-layer reveal & collage → hero (documented)
- `FOOT-42` حماية النص فوق الصور واللقطات / Text protection over photos & footage (documented)
- `FOOT-44` قواعد الصور للعربية / RTL photo layout rules (documented)
- `FOOT-45` أساليب الصور الجاهزة / Photo styles to scaffold (ready)

### `FOOT-44` — قواعد الصور للعربية / RTL photo layout rules

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الكشف من اليمين، الشبكات من أعلى اليمين، الشخص يسار والنص يمين، ولا تعكس صورة فيها كتابة أو علم أو شعار. / Reveals RTL, grids from top-right, subject left and text right; never mirror photos with writing, flags, logos or steering wheels.

**متى:** حين تصمم حركة صور لفيديو عربي وتحتاج اتجاه الكشف ومكان الشخص والنص وتجنب عكس الصور / when laying out photos for Arabic video: RTL reveals, subject left and text right, never mirroring writing or logos

**كيف:** Margins 5% / 12%; pills inherit their layer's transform; fixed depth order background → mid → cut-out subject → graphics.

**المعاملات:** margins 5%/12%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عربي · rtl · photo layout · mirroring · من اليمين لليسار · اتجاه عربي · عكس الصورة · arabic layout · margins

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/playbooks/photos.md:193-199`

#### 7. قدرات قريبة في العائلة

- `FOOT-42` حماية النص فوق الصور واللقطات / Text protection over photos & footage (documented)
- `FOOT-43` صورة أرشيف تنفتح على الحاضر / Archive photo opens onto the present (documented)
- `FOOT-45` أساليب الصور الجاهزة / Photo styles to scaffold (ready)
- `FOOT-46` شرائح الفلاتر وجدار الصور / Filter strips & tile walls (seen)

### `FOOT-45` — أساليب الصور الجاهزة / Photo styles to scaffold

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بارالاكس 2D، مونتاج مختلط فيروسي، ومونتاج تحريري — جاهزة للبناء. / 2D parallax, viral mixed media and editorial montage — ready to scaffold.

**متى:** حين تريد البدء سريعًا بفيديو صور بأسلوب بارالاكس أو ميكس ميديا فيروسي أو مونتاج تحريري جاهز / when starting a photo-based video from a ready 2D parallax, viral mixed-media or editorial montage style

**كيف:** python3 tools/kosif.py scaffold parallax-2d\|viral-mixed-media\|editorial <dir>; list --category photos (34 entries). Viral mixed media: beat-cut every 1–2 s, cut-outs with contact shadow, ≤ 7 words of kinetic type, grain 2–4%. Editorial: photo rig + type grid, masks and wipes 350–500 ms, one grade, grain, vignette 10–15%.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سكافولد · parallax-2d · viral mixed media · editorial · photos · قوالب صور · فيديو من صور · أسلوب جاهز · template · photo montage

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/styles/parallax-2d/SKILL.md`
- `kosif-tool/styles/viral-mixed-media/SKILL.md`
- `kosif-tool/styles/editorial/SKILL.md`
- `kosif-tool/playbooks/photos.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-43` صورة أرشيف تنفتح على الحاضر / Archive photo opens onto the present (documented)
- `FOOT-44` قواعد الصور للعربية / RTL photo layout rules (documented)
- `FOOT-46` شرائح الفلاتر وجدار الصور / Filter strips & tile walls (seen)
- `FOOT-47` لوح لقطات كل إطاراته مفتاحية / All-intra seekable footage plate (proven)

### `FOOT-46` — شرائح الفلاتر وجدار الصور / Filter strips & tile walls

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الصورة نفسها في أعمدة بفلتر مختلف لكل عمود، أو جدار مربعات 9:16 تنجرف ببطء. / The same photo in N columns, each with its own filter; or a wall of 9:16 tiles drifting slowly.

**متى:** حين تريد عرض نفس الصورة بعدة فلاتر في أعمدة متجاورة، أو جدار مربعات صور ينجرف ببطء / when showing one photo in columns with a different filter each, or a slowly drifting wall of 9:16 tiles

**كيف:** Columns reveal with 80 ms stagger and labels below; tile wall at varied offsets drifting 10–40 px/s; collage flash variant: scanned detail crops hard-cut every 300 ms with a click per hit.

**المعاملات:** stagger 80 ms; flash 300 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** فلاتر · جدار · filter strips · tile wall · collage flash · مقارنة فلاتر · جدار صور · شبكة صور · photo wall · filter comparison

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `style:pm-oliahmed205-3e31c4`
- `style:pm-twoclipping-6dd14e`
- `kosif-tool/styles/pm-abderrahmen-g-9e8ed0/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-44` قواعد الصور للعربية / RTL photo layout rules (documented)
- `FOOT-45` أساليب الصور الجاهزة / Photo styles to scaffold (ready)
- `FOOT-47` لوح لقطات كل إطاراته مفتاحية / All-intra seekable footage plate (proven)
- `FOOT-48` عرض الأفقي في 9:16 فوق نسخة مموهة / Landscape in 9:16 over a blurred fill (proven)

### `FOOT-47` — لوح لقطات كل إطاراته مفتاحية / All-intra seekable footage plate

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يعيد ترميز المقطع بحيث كل إطار مفتاحي، فيُبحث <video> داخل التكوين بدقة الإطار، ويطبع الوسم الجاهز. / Re-encodes a clip so every frame is a keyframe, letting a <video> inside a composition seek frame-exactly; prints the tag to paste.

**متى:** حين تضع فيديو داخل تكوين HTML وتحتاج أن يُبحث فيه بدقة الإطار أثناء الرندر / when a <video> inside an HTML composition must seek frame-exactly, by re-encoding every frame as a keyframe

**كيف:** python motion.py footage CLIP --out projects/X/assets/clip.mp4 [--from 0 --dur 5 --width 1280 --fps 30] (libx264 -g 1 crf 16, Lanczos, muted, yuv420p, +faststart). In the page: <video data-start data-duration muted>; the motion-kit shim seeks currentTime = t − start, hides it outside its span and waits for 'seeked' (0.5 ms tolerance). Ran here: a 3 s test clip came out with all 90 frames as keyframes and the ready tag.

**المعاملات:** -g 1; crf 16; width 1280; 30 fps

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** لقطات · all-intra · seek · video in html · keyframes · فيديو داخل الصفحة · دقة الإطار · إعادة ترميز · frame exact · motion-kit

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/motion.py:496`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:474`
- `100-superskills/skills/kosif-montage-motion/scripts/motion.py:548`

#### 7. قدرات قريبة في العائلة

- `FOOT-45` أساليب الصور الجاهزة / Photo styles to scaffold (ready)
- `FOOT-46` شرائح الفلاتر وجدار الصور / Filter strips & tile walls (seen)
- `FOOT-48` عرض الأفقي في 9:16 فوق نسخة مموهة / Landscape in 9:16 over a blurred fill (proven)
- `FOOT-49` لقطة متحدث تحت الرسوم / Real footage plate under graphics (ready)

### `FOOT-48` — عرض الأفقي في 9:16 فوق نسخة مموهة / Landscape in 9:16 over a blurred fill

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الإطار الأفقي كاملًا فوق نسخة مكبرة مموهة بدل قص الوسط الذي يخفي الحدث. / The whole landscape frame over a blurred enlarged copy instead of a centre crop that hides the action.

**متى:** حين تحول فيديو أفقيًا إلى طولي 9:16 وتريد إظهار الكادر كاملًا فوق نسخة مموهة بدل قص الوسط / when fitting a landscape clip into 9:16 vertical by placing the whole frame over a blurred enlarged copy

**كيف:** split → scale+crop to 1080×1920 + boxblur=40:2 → overlay the 1080-wide foreground centred (تحققتُ منه في هذه الحاوية (ffmpeg 6.1.1، 2026-10-16) / verified in this container (ffmpeg 6.1.1, 2026-10-16).). The montage tool picks this chain automatically (_fit_chain, MixedMontage test ok here). Screenshots never appear raw: rounded 12–16 px corners, shadow and a designed background or device frame.

**المعاملات:** 1080×1920; boxblur 40:2; radius 12–16 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** 9:16 · تمويه الخلفية · blur fill · vertical · reframe · تحويل لطولي · فيديو أفقي · خلفية مموهة · landscape to vertical · reels

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/tests/test_fetch_lab.py:93`
- `kosif-atlas/skills/1511-homie/3903-video/references/DELIVERY.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-46` شرائح الفلاتر وجدار الصور / Filter strips & tile walls (seen)
- `FOOT-47` لوح لقطات كل إطاراته مفتاحية / All-intra seekable footage plate (proven)
- `FOOT-49` لقطة متحدث تحت الرسوم / Real footage plate under graphics (ready)
- `FOOT-50` محرك المونتاج الموجّه / Directed-edit engine (ready)

### `FOOT-49` — لقطة متحدث تحت الرسوم / Real footage plate under graphics

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مقطع الكلام العمودي هو اللوح، والرسوم والضوء والجسيمات والترجمة طبقات HTML فوقه، وكاميرا افتراضية تحركه. / The vertical talking clip is the plate; graphics, light, particles and captions are HTML layers above it, with a virtual camera moving the plate.

**متى:** حين يكون لديك مقطع متحدث عمودي وتريد رسومًا وإضاءة وجسيمات وترجمة فوقه مع كاميرا افتراضية تحركه / when a vertical talking clip is the base plate with HTML graphics, light, particles and captions layered on top

**كيف:** <div id=cam><video id=plate data-start=0 data-duration=… muted></div> + layers (#bloom, #rays, #scrim 52%→.74, #vig, #dim, #particles) + SVG + type; prepare the plate with FOOT-47. Opening: plate starts saturate(.55) brightness(.92) and blooms to full colour in 0.6 s power3.out as the hook word lands, dim overlay 0.42→0 in 0.55 s. Under kinetic type: alternate push 1.04→1.10 / 1.10→1.04 per shot (smoothstep), kick +1.8%, payoff brightness +22%.

**المعاملات:** 1080×1920, 30 fps; push 1.04↔1.10

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** لوح · متحدث · footage plate · talking head · overlay · رسوم فوق الفيديو · موشن جرافيك · جسيمات · virtual camera · captions

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:45`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:144`
- `100-superskills/skills/kosif-montage-motion/templates/verse.html:140`

#### 7. قدرات قريبة في العائلة

- `FOOT-47` لوح لقطات كل إطاراته مفتاحية / All-intra seekable footage plate (proven)
- `FOOT-48` عرض الأفقي في 9:16 فوق نسخة مموهة / Landscape in 9:16 over a blurred fill (proven)
- `FOOT-50` محرك المونتاج الموجّه / Directed-edit engine (ready)
- `FOOT-51` إعادة تغليف المتحدث ببطاقات / Talking-head recut with designed cards (install)

### `FOOT-50` — محرك المونتاج الموجّه / Directed-edit engine

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP مدمج برخصة GSAP القياسية — ليست MIT / vendored GSAP under its standard license (not MIT). |

**ما هي:** يحوّل مواصفة تحرير فوق لقطة متحدث إلى تايملاين واحد: دفع بطيء لكل لقطة، ضربات كلمات مفتاحية، ثلاثة مستويات نص، فصول، ونهاية مقصودة. / Turns an edit spec over a talking-head plate into one timeline: slow push per shot, keyword punches, three text levels, chapters and a deliberate end.

**متى:** حين تريد تحويل مقطع متحدث إلى مونتاج موجه بزوم بطيء وضربات على الكلمات المهمة ونصوص وفصول / when turning a talking-head clip into a directed edit with slow pushes, keyword punch-ins, text levels and chapters

**كيف:** kmotion direct CLIP → edit.js (window.EDIT: shots, punches, captions, keys, motifs, chapters, payoff, credit, palette) → directed.html builds the GSAP timeline; sizes designed at 1080 px wide.

**المعاملات:** punch expo.out 0.14 s then −60% over 0.6 s; hook dim .38→0 in .55 s; ivory #F5F0E6; accent #E7B65A

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مونتاج موجه · directed edit · talking head · punch in · زوم على الكلمات · فصول · مونتاج متحدث · gsap · keyword punches

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/templates/directed.html:44`
- `100-superskills/skills/kosif-montage-motion/scripts/direct.py`

#### 7. قدرات قريبة في العائلة

- `FOOT-48` عرض الأفقي في 9:16 فوق نسخة مموهة / Landscape in 9:16 over a blurred fill (proven)
- `FOOT-49` لقطة متحدث تحت الرسوم / Real footage plate under graphics (ready)
- `FOOT-51` إعادة تغليف المتحدث ببطاقات / Talking-head recut with designed cards (install)
- `FOOT-52` فيديو ولوتي داخل HTML / Video & Lottie inside HTML compositions (install)

### `FOOT-51` — إعادة تغليف المتحدث ببطاقات / Talking-head recut with designed cards

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 + MIT (مقتبس من vtake-skills) |

**ما هي:** مقابلة أو بودكاست كما هو، مع بطاقات متزامنة مع النص: عناوين، أسماء، أرقام، اقتباسات، لوحات جانبية، صورة داخل صورة. / An interview/podcast untouched, wrapped in transcript-synced cards: titles, lower-thirds, data callouts, pull-quotes, side panels, PiP.

**متى:** حين يريد المستخدم تغليف مقابلة أو بودكاست ببطاقات عناوين وأسماء وأرقام واقتباسات متزامنة مع الكلام / when wrapping an untouched interview or podcast in transcript-synced titles, lower-thirds, data callouts and quotes

**كيف:** ffprobe + audio → hyperframes transcribe → corrected transcript → storyboard.json (schemaVersion 3; layout, themeId, seed; cards[zone, startSec]) → per-card HTML → one paused master timeline → render. Footage stays untouched; the wrapper tweens between layouts.

**التثبيت:** npx hyperframes transcribe talk.mp4

**الوسوم:** بودكاست · مقابلة · talking head · lower third · pull quote · اسم المتحدث · بطاقات نصية · اقتباسات · picture in picture · transcript sync

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/talking-head-recut/SKILL.md`
- `kosif-one/vendor/hyperframes/skills/talking-head-recut/media-contract.test.mjs`

#### 7. قدرات قريبة في العائلة

- `FOOT-49` لقطة متحدث تحت الرسوم / Real footage plate under graphics (ready)
- `FOOT-50` محرك المونتاج الموجّه / Directed-edit engine (ready)
- `FOOT-52` فيديو ولوتي داخل HTML / Video & Lottie inside HTML compositions (install)
- `FOOT-53` مشغل مقدمة سينمائية متكيف / Adaptive cinematic intro player (proven)

### `FOOT-52` — فيديو ولوتي داخل HTML / Video & Lottie inside HTML compositions

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لقطات مكتومة في إطار مستدير وحركات Lottie متجهة داخل التايملاين، تُبحث من الساعة الرئيسية. / Muted footage in a rounded frame and Lottie vector animations inside the timeline, sought from the master clock.

**متى:** حين تضيف فيديو مكتومًا في إطار مستدير أو رسوم Lottie داخل تكوين HTML متزامنة مع الساعة الرئيسية / when embedding muted footage or Lottie animations in an HTML composition, seeked from the master clock

**كيف:** Seek video.currentTime and lottie goToAndStop(frame) from t (autoplay false). Frame example 680×840 r16; Lottie pop 0.3→1 in 0.35 s back.out(1.6). Backdrops (Basma drawBG): cover fit, blur, 5% breathing zoom on stills, dim 0–0.8.

**المعاملات:** lottie pop 0.35 s back.out(1.6)

**التثبيت:** npm i lottie-web

**الوسوم:** لوتي · lottie · video embed · html composition · رسوم متجهة · إطار مستدير · تضمين فيديو · vector animation · rounded frame

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:lottie` ← npm ls lottie أو وجود node_modules/lottie
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`
- `app/public/js/00_editor.js:2443`

#### 7. قدرات قريبة في العائلة

- `FOOT-50` محرك المونتاج الموجّه / Directed-edit engine (ready)
- `FOOT-51` إعادة تغليف المتحدث ببطاقات / Talking-head recut with designed cards (install)
- `FOOT-53` مشغل مقدمة سينمائية متكيف / Adaptive cinematic intro player (proven)
- `FOOT-54` مونتاج تلقائي على الموسيقى / Auto montage to music (proven)

### `FOOT-53` — مشغل مقدمة سينمائية متكيف / Adaptive cinematic intro player

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طبقة فيلم كامل الشاشة تختار 4K أو 720p حسب الشاشة والشبكة، ولا تحجب الشاشة الحقيقية أبدًا. / A full-screen film overlay that picks 4K or 720p by viewport and network and never blocks the real entry screen.

**متى:** حين يحتاج موقع فيديو مقدمة سينمائية بملء الشاشة يختار الجودة حسب الشاشة والشبكة ولا يعطل الدخول / when a website needs a full-screen intro film that picks 4K or 720p by viewport and network and never blocks entry

**كيف:** 4K only if width ≥ 1100 px, effectiveType not 2g/3g and no saveData; on error retry 720p once; poster fallback; failsafe close 14 s; close 950 ms after 'ended'; skip when seen this session, deep link, reduced motion, saveData or deviceMemory ≤ 2; muted autoplay + sound toggle; focus trap; Escape skips. Ran here: node tools/brand_art.test.mjs → pass 5, fail 0.

**المعاملات:** breakpoint 1100 px; failsafe 14 s; end hold 950 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مقدمة · intro player · adaptive · 4k · web delivery · فيديو افتتاحي · مقدمة موقع · تشغيل تلقائي · splash video · 720p

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-earth-ci-fork/ui/art/brand/earth-intro-20261009.js`
- `kosif-earth-ci-fork/tools/brand_art.test.mjs`

#### 7. قدرات قريبة في العائلة

- `FOOT-51` إعادة تغليف المتحدث ببطاقات / Talking-head recut with designed cards (install)
- `FOOT-52` فيديو ولوتي داخل HTML / Video & Lottie inside HTML compositions (install)
- `FOOT-54` مونتاج تلقائي على الموسيقى / Auto montage to music (proven)
- `FOOT-55` ريل من مقطع كلام بأمر واحد / One-command talking-clip reel (ready)

### `FOOT-54` — مونتاج تلقائي على الموسيقى / Auto montage to music

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إيقاعات، أفضل النوافذ، دفع للصور، الأفقي فوق نسخة مموهة، −14 LUFS، واعتمادات. / Beats, best windows, photo pushes, landscape over a blurred copy, −14 LUFS and credits.

**متى:** حين يعطي المستخدم مجموعة لقطات وصور ومقطوعة موسيقية ويريد مونتاجًا تلقائيًا مقطوعًا على الإيقاع / when the user hands over clips, photos and a music track and wants an automatic beat-cut montage

**كيف:** kmotion montage MEDIA --music track --ratio 9:16 [--grade] [--voice] [--captions]; montage.cut([dir], music, out, ratio='9:16', punch=False). Ran here: MixedMontage folder-photos-and-fit test ok. Grammar: quick ~1 s and breathing ~3 s shots, breathing shots end on downbeats, zoom punches on downbeats (2× supersampled), grades teal_orange, golden_hour, cyberpunk, vintage_film, matrix_tech, clean_commercial, magma_night, blue_hour, sodium_night; sidechain ducking; −14 LUFS / −1 dBTP.

**المعاملات:** quick ~1 s / breathing ~3 s; −14 LUFS

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مونتاج تلقائي · auto montage · beat cut · music video · grades · مونتاج على الموسيقى · تقطيع على البيت · مونتاج صور وفيديو · music sync · kmotion

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/montage.py`
- `100-superskills/skills/kosif-montage-motion/tests/test_fetch_lab.py:93`
- `kosif-studio/motion/montage.py:42`

#### 7. قدرات قريبة في العائلة

- `FOOT-52` فيديو ولوتي داخل HTML / Video & Lottie inside HTML compositions (install)
- `FOOT-53` مشغل مقدمة سينمائية متكيف / Adaptive cinematic intro player (proven)
- `FOOT-55` ريل من مقطع كلام بأمر واحد / One-command talking-clip reel (ready)
- `FOOT-56` ريلز من فيديو طويل / Reels from a long video (key)

### `FOOT-55` — ريل من مقطع كلام بأمر واحد / One-command talking-clip reel

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مقطع كلام خام ← ريل عمودي: تفريغ ومسح ترجمة بالتوازي، ترميم وتأطير، سلسلة صوت، موسيقى عند الحاجة، كاريوكي واعتماد، −14 LUFS وبوابة تسليم. / Raw talking clip → finished vertical short: transcribe + decaption in parallel, restore + reframe, voice chain, music only if none, karaoke + credit, −14 LUFS, delivery gate.

**متى:** حين يرسل المستخدم مقطع كلام خامًا ويريد ريلًا عموديًا جاهزًا بترجمة كاريوكي وصوت منظف بأمر واحد / when turning a raw talking clip into a finished vertical reel with karaoke captions and a cleaned voice in one command

**كيف:** python reel.py CLIP.mp4 --out FINAL.mp4 [--size 1080x1920 --model large-v3\|small --music auto\|none\|bed.wav --style reels\|tiktok\|hormozi\|boxed\|minimal\|cinema\|punchy --credit '…' --transcript words.json]. Owner's recorded run IMG_9262: gate ok, −14.5 LUFS, TP −2.7, caption band 598–706. Needs faster-whisper for transcription (see SYNC).

**المعاملات:** intermediate crf 12; final crf 16; −14 LUFS

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ريل · مقطع كلام · talking reel · auto edit · shorts · ترجمة كاريوكي · تيك توك · مونتاج تلقائي · karaoke captions · vertical video

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/reel.py:92`
- `kosif-studio/out/reel_test/IMG_9262_reel.reel.json`
- `100-superskills/skills/kosif-montage-motion/scripts/reel.py`

#### 7. قدرات قريبة في العائلة

- `FOOT-53` مشغل مقدمة سينمائية متكيف / Adaptive cinematic intro player (proven)
- `FOOT-54` مونتاج تلقائي على الموسيقى / Auto montage to music (proven)
- `FOOT-56` ريلز من فيديو طويل / Reels from a long video (key)
- `FOOT-57` المونتاج الذكي الكامل من الكلام / Smart full montage from speech (AutoEdit) (key)

### `FOOT-56` — ريلز من فيديو طويل / Reels from a long video

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يقطع 1–8 ريلز من محاضرة طويلة: خطّاف إلى خلاصة ينتهي بجملة كاملة، ثم ترجمة وعنوان وكاميرا متحدث وصوت منظف. / Cuts 1–8 vertical reels from a long talk: self-contained hook-to-payoff highlights ending on full sentences, then captions, a hook title, talking-head camera and cleaned speech.

**متى:** حين يريد المستخدم استخراج عدة ريلز قصيرة من محاضرة أو بودكاست طويل تبدأ بخطّاف وتنتهي بجملة كاملة / when cutting several vertical reels from a long talk, each a hook-to-payoff highlight ending on a full sentence

**كيف:** REELS.find({count, length}): count 5 (> 600 s), 3 (> 180 s) else 2, max 8; length 15–75 s (default 40); an AI picks from a timed transcript (≤ 24,000 chars). Local fallback REELS.local scores windows by words/second snapped to sentences (break on . ! ؟ ? … or > 9 s) — usable without a key. Shorts handles: 60 s + 2×15 s pre/post needs 90 s of source.

**المعاملات:** 1–8 reels; 15–75 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ريلز · مقاطع قصيرة · highlights · long video · podcast clips · تقطيع محاضرة · أهم المقاطع · شورتس · hook · repurpose

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `app/public/js/10_studio.js:4017`
- `app/public/js/10_studio.js:4039`
- `100-superskills/skills/reels-shorts-factory/references/sources.md:148`

#### 7. قدرات قريبة في العائلة

- `FOOT-54` مونتاج تلقائي على الموسيقى / Auto montage to music (proven)
- `FOOT-55` ريل من مقطع كلام بأمر واحد / One-command talking-clip reel (ready)
- `FOOT-57` المونتاج الذكي الكامل من الكلام / Smart full montage from speech (AutoEdit) (key)
- `FOOT-58` مونتاج لقطات المستخدم على الإيقاع (بصمة) / Basma automatic beat montage (key)

### `FOOT-57` — المونتاج الذكي الكامل من الكلام / Smart full montage from speech (AutoEdit)

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صوت أو فيديو ← تفريغ بالكلمة ← سيناريو ومشاهد ← لقطات مطابقة ← قطع على الكلمات ← ترجمة ← مراجعة ← رندر. / Audio/video → word-level transcript → scenario and scenes → matching footage → cuts on the words → captions → review → render.

**متى:** حين يكون لدى المستخدم تعليق صوتي أو فيديو كلام ويريد مونتاجًا كاملًا بلقطات مطابقة للكلمات وترجمة / when building a full montage from a voice-over or talk: word-level transcript, matching footage, word cuts, captions

**كيف:** window.BasmaAutoEdit.run (9:16, pace med, 2 caption words); sources Openverse/Wikimedia (+ Pexels/Pixabay with keys — blocked from this container), motion-graphics inserts, SFX, VFX plan (grade, particles, grain, leak, vignette, letterbox, ≤ 4 crash-zoom accents). Needs the Basma app and its AI keys. Rule: cover silences and abstract explanation with real footage, one mood and one light across the pool.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مونتاج ذكي · b-roll · auto edit · voice over · stock · تعليق صوتي · لقطات مساندة · سيناريو · openverse · autoedit

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `app/public/js/50_autoedit.js:4`
- `app/public/js/50_autoedit.js:427`
- `100-superskills/skills/kosif-montage-motion/references/montage_grammar.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-55` ريل من مقطع كلام بأمر واحد / One-command talking-clip reel (ready)
- `FOOT-56` ريلز من فيديو طويل / Reels from a long video (key)
- `FOOT-58` مونتاج لقطات المستخدم على الإيقاع (بصمة) / Basma automatic beat montage (key)
- `FOOT-D01` ريل «الدعاء» من لقطاتك وصوتك / «الدعاء» Friday dua reel kit (proven)

### `FOOT-58` — مونتاج لقطات المستخدم على الإيقاع (بصمة) / Basma automatic beat montage

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حتى 24 لقطة وصورة: يدرس كل لقطة، يرتبها الذكاء من لوحة مرقمة، ويقطع على الإيقاع مع حركات كاميرا وانتقالات ومؤثرات. / Up to 24 clips/photos: probes each, an AI orders them from a numbered contact sheet, cuts on the beat with camera moves, transitions and SFX.

**متى:** حين يرفع المستخدم حتى 24 لقطة وصورة ويريد مونتاجًا على الإيقاع يرتبه الذكاء الاصطناعي بحركات وانتقالات / when up to 24 user clips and photos should be AI-ordered and cut on the beat with camera moves, transitions and SFX

**كيف:** MON.run: probe in parallel batches of 3; 4-column numbered sheet; AI decides order, hook title, 0–6 lines, pace and grade; lengths snapped to beats within 0.4 s; bestWindow picks lively, sharp, well-lit windows away from cuts. Pro variant (PROMONT) adds template motion inserts.

**المعاملات:** ≤ 24 clips; 4–180 s; snap ≤ 0.4 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بصمة · basma · beat montage · contact sheet ai · مونتاج على الإيقاع · ترتيب اللقطات · مؤثرات صوتية · auto edit · transitions

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `app/public/js/10_studio.js:1865`
- `app/public/js/10_studio.js:2069`
- `app/public/js/30_promontage.js:41`

#### 7. قدرات قريبة في العائلة

- `FOOT-56` ريلز من فيديو طويل / Reels from a long video (key)
- `FOOT-57` المونتاج الذكي الكامل من الكلام / Smart full montage from speech (AutoEdit) (key)
- `FOOT-D01` ريل «الدعاء» من لقطاتك وصوتك / «الدعاء» Friday dua reel kit (proven)
- `FOOT-D02` انتقالات كاب كات على الصورة فقط / CapCut-style transitions under fixed text (proven)

### `FOOT-D01` — ريل «الدعاء» من لقطاتك وصوتك / «الدعاء» Friday dua reel kit

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | kit code: repo licence; fonts: SIL OFL 1.1 |

**ما هي:** أسلوب «الدعاء» المقاس محفوظ كعدة: عبارة = لقطة = سطر، عنوان «الجُمُعَة» ثلث، تاريخ برقم يوم يطير، سطر ذهبي، سطر دعاء أبيض بهالة داكنة، وانتقالات ضبابية/مرآة/زوم، والصوت منسوخ دون تعديل. / The measured «الدعاء» style saved as a kit: phrase = shot = line, Thuluth «الجُمُعَة» title, date with a flying day number, gold subtitle, white dua line with a tight dark halo, blur/mirror/zoom transitions, voice stream-copied untouched.

**متى:** حين يريد المستخدم ريل دعاء ليوم الجمعة من لقطاته وصوته بعنوان بالثلث وتاريخ وسطور دعاء متزامنة / when making a Friday dua reel from the user's clips and voice: Thuluth title, flying date, synced lines, audio untouched

**كيف:** Fill project.json (clips, lines with start/end or an asr.json, date, audio) from styles/dua/kit/example, then python3 styles/dua/kit/build_dua.py project.json --preview, then --out reel.mp4. Measured spec in styles/dua/dua.style.json. Proof: 15.4 s, 462 frames, 13/13 verify checks, 665/665 audio packets byte-identical.

**المعاملات:** 1080×1920 · 30 fps · CRF 18 · cut on phrase onset · line in +0.2 s / out −0.3 s · fades 0.17/0.15 s · day flight 0.1→1.1 s easeOutCubic

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** الدعاء · دعاء · ليلة الجمعة · dua · friday reel · islamic reel · style kit · thuluth title · يوم الجمعة · ريل ديني · خط الثلث · religious reel · jumuah

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-D01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/dua-style/README.md`
- `kosif-tool/styles/dua/kit/build_dua.py`
- `kosif-tool/styles/dua/dua.style.json`
- `kosif-tool/styles/dua/ANALYSIS.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-57` المونتاج الذكي الكامل من الكلام / Smart full montage from speech (AutoEdit) (key)
- `FOOT-58` مونتاج لقطات المستخدم على الإيقاع (بصمة) / Basma automatic beat montage (key)
- `FOOT-D02` انتقالات كاب كات على الصورة فقط / CapCut-style transitions under fixed text (proven)
- `FOOT-D03` قياس أسلوب ريل من الإطارات / Measure a reel's style from its frames (proven)

### `FOOT-D02` — انتقالات كاب كات على الصورة فقط / CapCut-style transitions under fixed text

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | kit code: repo licence; fonts: SIL OFL 1.1 |

**ما هي:** أربعة انتقالات مقاسة تطبق على اللقطات تحت طبقة نص لا تتأثر: دخول ضبابي، مرآة ثم ضبابية، زوم قطع، ضبابية دوّارة. / Four measured transitions applied to footage below an untouched text layer: blur_in, mirror_out_blur_in, zoom_out_cut, spin_zoom_blur.

**متى:** حين تريد انتقالات مثل كاب كات (ضبابية، مرآة، زوم، دوران) على اللقطات فقط والنص فوقها يبقى واضحًا / when applying CapCut-style blur, mirror, zoom or spin transitions to footage while the text layer above stays sharp

**كيف:** apply_transition() in styles/dua/kit/build_dua.py: blur_in starts at ~28 px motion blur and clears in 0.17–0.35 s easeOutCubic; mirror reflects the lower half 0.3 s before the cut; zoom pushes 6 % in 0.1 s; spin grows a radial blur over 0.45 s. Text layers are composited after the transition so they never blur.

**المعاملات:** blur 28 px → 0 · mirror pre 0.3 s · push 6 %/0.1 s · spin 0.45 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** انتقالات · ضبابية · مرآة · blur transition · mirror transition · zoom blur · capcut · ترانزيشن · كاب كات · انتقال دوار · spin transition · zoom transition

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-D02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/dua-style/README.md`
- `kosif-tool/styles/dua/kit/build_dua.py`
- `kosif-tool/styles/dua/dua.style.json`
- `kosif-tool/styles/dua/ANALYSIS.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-58` مونتاج لقطات المستخدم على الإيقاع (بصمة) / Basma automatic beat montage (key)
- `FOOT-D01` ريل «الدعاء» من لقطاتك وصوتك / «الدعاء» Friday dua reel kit (proven)
- `FOOT-D03` قياس أسلوب ريل من الإطارات / Measure a reel's style from its frames (proven)
- `FOOT-P01` إعادة مونتاج اللقطات من قائمة قطع محدودة / Bounded EDL recut: trim/concat with denoise and loudnorm (documented)

### `FOOT-D03` — قياس أسلوب ريل من الإطارات / Measure a reel's style from its frames

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | kit code: repo licence; fonts: SIL OFL 1.1 |

**ما هي:** تحويل ريل مرجعي إلى مواصفة قابلة للتنفيذ: القطعات وتطابقها مع العبارات، ألوان النص بأقنعة، صناديق الطبقات، الهالة، تلوين اللقطات بـLab، الانتقالات، والصوت (LUFS وتفريغ). / Turn a reference reel into an executable spec: cuts vs phrase onsets, text colours via masks, layer boxes, halo profile, per-shot Lab grade, transitions and audio (LUFS, ASR).

**متى:** حين تريد تحويل ريل مرجعي إلى مواصفة أسلوب مقاسة: القطعات وألوان النص والهالة والتلوين والانتقالات والصوت / when turning a reference reel into a measured style spec: cuts, text colours, halo, grade, transitions, loudness

**كيف:** Run scripts/mimic/mm_analyze.py for shots and transitions, then measure text colour from white/gold masks rather than its auto colour (it can latch onto the shadow), radial luma rings for the halo, ffmpeg ebur128 for loudness and faster-whisper on a numpy array for phrase onsets. Write the result as <id>.style.json + ANALYSIS.md (measured vs assumed) as in styles/dua.

**المعاملات:** cut tolerance ≤ 0.18 s · colour masks over ≥ 6 frames · halo rings 1–12 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تحليل أسلوب · قياس · style analysis · reference measurement · mimic · color mask · تقليد ستايل · نفس أسلوب الريل · ألوان النص · style spec · lufs

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:numpy` ← python3 -c "import numpy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-D03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/dua-style/README.md`
- `kosif-tool/styles/dua/kit/build_dua.py`
- `kosif-tool/styles/dua/dua.style.json`
- `kosif-tool/styles/dua/ANALYSIS.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-D01` ريل «الدعاء» من لقطاتك وصوتك / «الدعاء» Friday dua reel kit (proven)
- `FOOT-D02` انتقالات كاب كات على الصورة فقط / CapCut-style transitions under fixed text (proven)
- `FOOT-P01` إعادة مونتاج اللقطات من قائمة قطع محدودة / Bounded EDL recut: trim/concat with denoise and loudnorm (documented)
- `FOOT-U01` مطابقة المسودة بلقطات المصدر / Match a draft back to its source shots (documented)

### `FOOT-P01` — إعادة مونتاج اللقطات من قائمة قطع محدودة / Bounded EDL recut: trim/concat with denoise and loudnorm

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner package (own work) |

**ما هي:** يأخذ فيديو أصليًا وقائمة نطاقات --cut START:END فيقصّها ويرتبها ويعيد قياسها إلى مقاس الهدف مع صوتها، ويترك الأصل كما هو. / Takes a source and explicit --cut ranges, trims, concatenates and reframes them with their audio, leaving the original untouched.

**متى:** حين يعطي المستخدم أوقات بداية ونهاية لأجزاء من فيديو ويريد قصها وتجميعها مع تنقية الصوت وضبط علوه / when the user gives start:end ranges to cut from a source and join in order, with optional denoise and loudnorm

**كيف:** ffprobe first; each range must be finite, 0 ≤ a < b ≤ duration+0.03 and ≥ 0.10 s; at most 30 cuts; refuses output == input. Per cut: trim + setpts, scale=W:H:force_original_aspect_ratio=decrease, pad centred, fps, setsar=1, yuv420p; audio atrim + asetpts + aresample=48000 (+ afftdn=nf=-25 with --denoise); concat=n:v=1:a=1; --normalize appends loudnorm=I=-16:TP=-1.5:LRA=11. No-audio sources get -an. Prints a JSON receipt (duration, streams, cuts, denoised). Re-ran here on the bundled 4 s test clip with --cut 0:1.2 --cut 2:3.4 --denoise --normalize → 2.625 s, h264 480×854 24 fps + AAC. Note: loudnorm here targets −16 LUFS; the superpowers delivery target is −14 LUFS, so pass the final mix through your own loudnorm step. Status note: the code is owner material that is not vendored in this skill; the numbers above are from one run on the owner's copy on 2026-10-16 and cannot be re-run from here, so this is 📄 documented, not ✅.

**المعاملات:** ≤30 cuts · ≥0.1 s each · afftdn nf=-25 · loudnorm I=-16 TP=-1.5 LRA=11 · crf 21 · default 480×854@24

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** edl · recut · trim · concat · afftdn · loudnorm · مونتاج · قص · تنقية صوت · قائمة قطع · تجميع أجزاء · توحيد الصوت · cut list · timestamps

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-P01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/tools/video_edit.py`
- `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/tests/test_v3_edit.py`
- `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/examples/Edited_Footage_Real.mp4`

#### 7. قدرات قريبة في العائلة

- `FOOT-D02` انتقالات كاب كات على الصورة فقط / CapCut-style transitions under fixed text (proven)
- `FOOT-D03` قياس أسلوب ريل من الإطارات / Measure a reel's style from its frames (proven)
- `FOOT-U01` مطابقة المسودة بلقطات المصدر / Match a draft back to its source shots (documented)
- `FOOT-U02` كاشف القفزات: اقطع قبل القفزة / Jump-cut finder: cut on the frame before (documented)

### `FOOT-U01` — مطابقة المسودة بلقطات المصدر / Match a draft back to its source shots

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | Claude AI Motion Graphics (Tao Prompts) — ideas and numbers only, code not copied |

**ما هي:** صغّر كل إطار من المسودة والمصادر إلى 96×54 رمادي واختر أقل متوسط فرق مطلق ← (اللقطة، زمن المصدر) لكل إطار؛ خطأ < 15 = استخدام كامل، وأعلى = داخل بطاقة أو بمؤثر؛ ملاءمة خطية تعطي الإزاحة (src = t − c). — Recover which shot and source time each frame of a user mock-up uses.

**متى:** المستخدم أرسل مسودة مونتاج ويريدها بجودة عالية / rebuilding a user's rough draft

**كيف:** قفزات السطوع حيث تفشل المطابقة غالبًا مؤثرات مخبوزة: افحصها قبل «إصلاحها».

**المعاملات:** 96×54 gray; MAD < 15 = full frame

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** draft · مسودة · match · مطابقة · source · mock-up · offset

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-U01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/references/owner-uploads-review-20261023.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-D03` قياس أسلوب ريل من الإطارات / Measure a reel's style from its frames (proven)
- `FOOT-P01` إعادة مونتاج اللقطات من قائمة قطع محدودة / Bounded EDL recut: trim/concat with denoise and loudnorm (documented)
- `FOOT-U02` كاشف القفزات: اقطع قبل القفزة / Jump-cut finder: cut on the frame before (documented)
- `FOOT-U03` قناع شخص بلا تعلم آلي / Person matte without ML (documented)

### `FOOT-U02` — كاشف القفزات: اقطع قبل القفزة / Jump-cut finder: cut on the frame before

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | Claude AI Motion Graphics (Tao Prompts) — ideas and numbers only, code not copied |

**ما هي:** إطار تغيّره عن السابق > نسبة × الوسيط المحلي = قفزة داخل لقطة مركبة من عدة مآخذ؛ ضع قطع القسم على الإطار قبل القفزة وإلا ومض المأخذ التالي إطارًا واحدًا. — Find hard cuts inside a talking-head clip; cut one frame before them.

**متى:** قص فيديو متكلم مركب من مآخذ / editing a multi-take talking head

**كيف:** على مجلد إطارات؛ نسبة افتراضية ~4–6 × الوسيط المحلي.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** jump cut · قفزة · talking head · cut · قطع · frame

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-U02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/references/owner-uploads-review-20261023.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-P01` إعادة مونتاج اللقطات من قائمة قطع محدودة / Bounded EDL recut: trim/concat with denoise and loudnorm (documented)
- `FOOT-U01` مطابقة المسودة بلقطات المصدر / Match a draft back to its source shots (documented)
- `FOOT-U03` قناع شخص بلا تعلم آلي / Person matte without ML (documented)
- `FOOT-X01` انضباط مونتاج المادة الحقيقية / Real-footage edit discipline (source-to-programme map) (documented)

### `FOOT-U03` — قناع شخص بلا تعلم آلي / Person matte without ML

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | Claude AI Motion Graphics (Tao Prompts) — ideas and numbers only, code not copied |

**ما هي:** GrabCut بنصف الدقة ببذور (بيضاوي الوجه والجذع أمامي ومناطق خلفية معروفة) يُنشر من قناع الإطار السابق (مُآكل = أمامي، شريط موسّع = محتمل)، ثم مرشح موجّه بالدقة الكاملة (r=10 eps=2e-4 ثم r=4 eps=1e-4) ومزج زمني؛ النص خلف الرأس = النص ثم person × matte. — Seeded, propagated GrabCut + guided filter for text behind a speaker.

**متى:** نص خلف الشخص بلا نموذج تقطيع / text behind a person without a segmentation model

**كيف:** البذور تهم في الإطار الأول فقط؛ للكاميرا الثابتة أضف مضلعًا أماميًا ثابتًا (مكتب).

**المعاملات:** guided filter r=10/eps=2e-4 then r=4/eps=1e-4

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** matte · قناع · rotoscope · behind head · خلف الرأس · grabcut · person

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-U03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/references/owner-uploads-review-20261023.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-U01` مطابقة المسودة بلقطات المصدر / Match a draft back to its source shots (documented)
- `FOOT-U02` كاشف القفزات: اقطع قبل القفزة / Jump-cut finder: cut on the frame before (documented)
- `FOOT-X01` انضباط مونتاج المادة الحقيقية / Real-footage edit discipline (source-to-programme map) (documented)
- `FOOT-X02` فحص القدرة واختبارات قصيرة قبل التصدير / Capability preflight and short tests before an expensive export (documented)

### `FOOT-X01` — انضباط مونتاج المادة الحقيقية / Real-footage edit discipline (source-to-programme map)

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | unknown (reference only) |

**ما هي:** المادة الأصلية هي الأساس: احفظ مدتها وترتيبها وكلامها ووقفاتها ونسبتها وصوتها، وابنِ خريطة زمن من المصدر إلى البرنامج قبل أي إضافة. — The source is the base: keep its duration, order, speech, pauses, aspect and sound, and build a source-to-programme time map before adding anything.

**متى:** مونتاج متحدث أو مقابلة أو فيديو أرسله المستخدم — editing a talking head, interview or user video.

**كيف:** Transcript + time map; account for cuts already baked into the source (never reveal stray frames of an adjacent take when returning from B-roll); when shifting a shot boundary keep the absolute timing of spoken words; choose fps from the actual source; do not upscale without reason; long videos get fewer inserts and more reading time; no presenter → no splits or presenter captions. Names, numbers, interfaces and quotes must match the source; ask about an unintelligible phrase rather than inventing it. Presenter splits: a restrained push entry only for horizontal splits with one presenter; the insert keeps its final crop through the slide; the presenter is re-cropped, never squeezed (crop aspect = card aspect).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** footage · edit · transcript · talking head · مونتاج · مادة حقيقية · متحدث

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-X01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `owner-upload:Claude_edit_skill_1/Claude edit skill/SKILL.md`
- `owner-upload:Claude_edit_skill_1/Claude edit skill/implementation/browser-reference/split-layout.js`

#### 7. قدرات قريبة في العائلة

- `FOOT-U02` كاشف القفزات: اقطع قبل القفزة / Jump-cut finder: cut on the frame before (documented)
- `FOOT-U03` قناع شخص بلا تعلم آلي / Person matte without ML (documented)
- `FOOT-X02` فحص القدرة واختبارات قصيرة قبل التصدير / Capability preflight and short tests before an expensive export (documented)
- `FOOT-X03` القص الدقيق بالإطار يحتاج إعادة ترميز / Frame-accurate trims need a re-encode (proven)

### `FOOT-X02` — فحص القدرة واختبارات قصيرة قبل التصدير / Capability preflight and short tests before an expensive export

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | unknown (reference only) |

**ما هي:** قبل وعد بملف MP4 تأكد من الوصول إلى المصدر وفك الصورة والصوت وأدوات التصدير والخطوط والأقنعة، واصنع اختبارات قصيرة أولًا. — Before promising an MP4 confirm access to the source, picture and audio decode, export tools, fonts and masks, and make short tests first.

**متى:** بداية أي مونتاج على مادة المستخدم — the start of any edit on user footage.

**كيف:** If something is missing say exactly what and the smallest way forward; never present HTML, code or a plan as a finished video; work on a copy (an installed skill directory may be read-only). Short tests: light and dark B-roll, B&W, typography, one split, one mask. Keep layers clean (source, inserts, text, masks, sound) and the previous version. Rights: a Pinterest find does not establish usage rights; generation is optional and needs an agreed budget; generated imagery is never presented as historical evidence. Deliver the MP4, an editable project, a dependency list and sources; if music was added, also a version without it. 'Contact sheets and numbers do not replace watching and listening'; never report an unperformed check as passed.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** preflight · rights · b-roll · delivery · فحص مسبق · حقوق · تسليم

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-X02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `owner-upload:Claude_edit_skill_1/Claude edit skill/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-U03` قناع شخص بلا تعلم آلي / Person matte without ML (documented)
- `FOOT-X01` انضباط مونتاج المادة الحقيقية / Real-footage edit discipline (source-to-programme map) (documented)
- `FOOT-X03` القص الدقيق بالإطار يحتاج إعادة ترميز / Frame-accurate trims need a re-encode (proven)
- `FOOT-X04` طبقات أدوات المونتاج وحالات المشروع / Footage editing layers and project-state hygiene (documented)

### `FOOT-X03` — القص الدقيق بالإطار يحتاج إعادة ترميز / Frame-accurate trims need a re-encode

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | MIT (ECC, (c) 2026 Affaan Mustafa) |

**ما هي:** القص بنسخ التدفق دون ترميز يلتصق بالإطارات المفتاحية؛ للقص الدقيق أعد الترميز. — Stream-copy trims snap to keyframes; re-encode for frame-accurate cuts.

**متى:** قص لقطات على ضربات أو كلمات بدقة إطار — cutting shots on beats or words to the frame.

**كيف:** Ran here (V8) on a 10 s 30 fps clip with a keyframe every 60 frames, asking for 1.3–3.3 s (60 frames from frame 39): output seeking with -c copy started at the next keyframe (frame 60) → 41 frames, 1.367 s; input seeking with -c copy kept 62 frames / 2.167 s; re-encoding (`ffmpeg -ss 1.3 -to 3.3 -i in.mp4 -c:v libx264 …`) gave exactly 60 frames, 2.000 s, starting at frame 39. Use -c copy only for rough, keyframe-aligned trims; use proxies (scale=960:-2, ultrafast, crf 28) for previews.

**المعاملات:** copy: 41 or 62 frames vs requested 60; re-encode: 60

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** trim · keyframe · gop · ffmpeg · stream copy · قص · إطار مفتاحي

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-X03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/references/external-skills.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/motion-v2/README.md`
- `https://github.com/affaan-m/ECC/tree/main/skills/taste-application/SKILL.md`
- `https://github.com/affaan-m/ECC/tree/main/skills/video-editing/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-X01` انضباط مونتاج المادة الحقيقية / Real-footage edit discipline (source-to-programme map) (documented)
- `FOOT-X02` فحص القدرة واختبارات قصيرة قبل التصدير / Capability preflight and short tests before an expensive export (documented)
- `FOOT-X04` طبقات أدوات المونتاج وحالات المشروع / Footage editing layers and project-state hygiene (documented)
- `FOOT-X05` عقد محاكاة فيديو مرجعي / Reference-video imitation contract (8 steps) (documented)

### `FOOT-X04` — طبقات أدوات المونتاج وحالات المشروع / Footage editing layers and project-state hygiene

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | MIT (ECC, (c) 2026 Affaan Mustafa) |

**ما هي:** لا تجعل أداة واحدة تفعل كل شيء: التقاط، ثم بنية بالذكاء (نص، مواضيع، مقاطع ميتة، قائمة قص)، ثم ffmpeg، ثم Remotion، ثم صوت أو صورة مولدة، ثم برنامج مونتاج للتشطيب. — Do not make one tool do everything: capture, then AI structure (transcript, topics, dead sections, edit list), then ffmpeg, then Remotion, then generated audio/visuals, then an editor for finishing.

**متى:** مشروع مونتاج طويل أو متعدد الأدوات — a long or multi-tool edit project.

**كيف:** The model's job is structure: transcript, topics, dead sections, the EDL and scaffolded ffmpeg commands. Checkpoint the project before and after editor or audio-workstation changes; an API read-back is not proof it was saved; keep rendered media, the editable project and the approval as separate states; audition generated music for silence.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** editing pipeline · edl · ffmpeg · remotion · مونتاج · خط عمل

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-X04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `https://github.com/affaan-m/ECC/tree/main/skills/video-editing/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-X02` فحص القدرة واختبارات قصيرة قبل التصدير / Capability preflight and short tests before an expensive export (documented)
- `FOOT-X03` القص الدقيق بالإطار يحتاج إعادة ترميز / Frame-accurate trims need a re-encode (proven)
- `FOOT-X05` عقد محاكاة فيديو مرجعي / Reference-video imitation contract (8 steps) (documented)
- `FOOT-X06` فاحص المرجع المرخّص: صفحة أو ملف أو HLS ← قياسات / Permissioned reference inspector: page / direct / HLS → measurements (proven)

### `FOOT-X05` — عقد محاكاة فيديو مرجعي / Reference-video imitation contract (8 steps)

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner |

**ما هي:** لتقليد مونتاج فيديو أرسله المستخدم: افحص، حلّل، طابق النص العربي، احفظ الصوت، استخدم مادة مرخصة، ارندر فقط بأداة متاحة، افحص، ثم سلّم مع تقرير الفروقات. — To imitate a user's reference edit: inspect, analyse, match the Arabic overlay, keep the audio, use licensed assets, render only with an available executor, QA, and deliver with a discrepancy report.

**متى:** «اعمل مثل هذا الفيديو» أو «نفس المونتاج» — 'make it like this video' or 'the same edit'.

**كيف:** 1 inspect (ffprobe; originals read-only; timestamped deterministic frame samples) → 2 analyse (separate scene cuts from camera motion; classify cut/fade/wipe/slide/zoom-blur with measured ranges; keep uncertainty explicit) → 3 Arabic overlay (region geometry, in/out spans, font candidates not identities ARAB-X02, HarfBuzz shaping, mixed script and digits) → 4 audio (original when authorised; no invented word precision) → 5 assets (Pinterest = mood only; licensed media; never copy watermarks) → 6 render only with an exposed executor, else return the plan marked EXECUTOR_NOT_EXPOSED → 7 QA gates (MP4 exists, codec/duration/fps, non-frozen motion, safe zones, Arabic legibility, overlay timing, licence manifest, before/after storyboard; any failure blocks an 'exact match' claim) → 8 deliver MP4 + editable JSON shot plan + storyboard + font-candidate report + discrepancy summary. Not this route: a still image with the same font, Suno lyrics, motion from audio without a reference video, imitating email wording, or only downloading a link.

**المعاملات:** 8 steps; failed gate → no 'exact match'

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** imitation · reference video · recreate edit · محاكاة · نفس المونتاج · فيديو مرجعي

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-X05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `owner-upload:KOSIF_SEE_Humanizer_Optimize_Graphify_v1.7.5/skills/kosif-see/references/VIDEO_IMITATION_ROUTING_V1.md`

#### 7. قدرات قريبة في العائلة

- `FOOT-X03` القص الدقيق بالإطار يحتاج إعادة ترميز / Frame-accurate trims need a re-encode (proven)
- `FOOT-X04` طبقات أدوات المونتاج وحالات المشروع / Footage editing layers and project-state hygiene (documented)
- `FOOT-X06` فاحص المرجع المرخّص: صفحة أو ملف أو HLS ← قياسات / Permissioned reference inspector: page / direct / HLS → measurements (proven)

### `FOOT-X06` — فاحص المرجع المرخّص: صفحة أو ملف أو HLS ← قياسات / Permissioned reference inspector: page / direct / HLS → measurements

| الحقل | القيمة |
|---|---|
| العائلة | `photo-video-footage` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/photo-video-footage.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يكتشف روابط الوسائط في الصفحة (video/source، Open Graph، JSON-LD، النصوص البرمجية)، يجلب الملف المباشر أو بث HLS غير المشفّر (أعلى جودة، مع مسار صوت منفصل)، يرفض DRM والمضيفين الخاصين والأحجام الكبيرة، يعيد التغليف ثم يقيس: probe وcontact sheet وقطعات المشاهد ولوحة ألوان وتقرير ثنائي اللغة في .kosif-cache. — Discovers media URLs on a page, fetches direct or unencrypted HLS media (top variant, separate audio), refuses DRM/private hosts/oversize, remuxes and measures: probe, contact sheet, scene cuts, palette, bilingual REPORT.md in .kosif-cache.

**متى:** عندما تنص قاعدة AGENTS.md رقم 3 على مراقبة المرجع قبل التنفيذ، وبصورة مشروعة / AGENTS.md rule 3: observe the reference before implementing, lawfully

**كيف:** `python3 .claude/skills/kosif-superpowers/scripts/fetch_reference.py <page-or-media-url> [--list \| --pick N] [--frames 8 --scene 0.3 --max-mb 400]`; outputs reference.mp4, probe.json, contact.png, cuts.json, palette.json, REPORT.md; blob: players need the browser's network panel first (references/reference-inspection.md). Measured values go to STYLE.md *Observed*; nothing fetched is committed.

**المعاملات:** --max-mb 400; --scene 0.3; 8 frames; sequential bounded HLS segments

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مرجع · reference · hls · m3u8 · contact sheet · palette · scene cuts · rights

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:FOOT-X06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `adobe-mcp-bridges` · `app-studio` · `app-studio-paint` · `cinema-lab` · `cinematic-broll-render` · `cinematic-cut-planner`.
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
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/fetch_reference.py`
- `kosif-tool/.claude/skills/kosif-superpowers/references/reference-inspection.md`
- `kosif-tool/tests/test_reference_fetch_security.py`
- `kosif-tool/tests/test_superpowers_catalog.py`

#### 7. قدرات قريبة في العائلة

- `FOOT-X04` طبقات أدوات المونتاج وحالات المشروع / Footage editing layers and project-state hygiene (documented)
- `FOOT-X05` عقد محاكاة فيديو مرجعي / Reference-video imitation contract (8 steps) (documented)

