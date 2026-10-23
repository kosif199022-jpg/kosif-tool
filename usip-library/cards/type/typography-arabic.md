# `typography-arabic` — الخطوط والنصوص العربية واللاتينية (99 بطاقة)

> مكتبة بروتوكول USIP v5.6 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/typography-arabic.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/type.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`ARAB-01` الكلمة كاملة لا الحرف](#arab-01--الكلمة-كاملة-لا-الحرف--whole-word-law)
- [`ARAB-02` حصر الاتجاه في عناصر النص](#arab-02--حصر-الاتجاه-في-عناصر-النص--rtl-scoping-for-renderers)
- [`ARAB-03` لا تباعد ولا مطّ — الكشيدة فقط](#arab-03--لا-تباعد-ولا-مطّ--الكشيدة-فقط--no-tracking-no-stretch--kashida-only)
- [`ARAB-04` بوابة تحميل الخط قبل الإطار الأول](#arab-04--بوابة-تحميل-الخط-قبل-الإطار-الأول--font-ready-gate-before-frame-0)
- [`ARAB-05` مساحة التشكيل وحواف الأقنعة](#arab-05--مساحة-التشكيل-وحواف-الأقنعة--harakat-headroom--mask-padding)
- [`ARAB-06` توجيه محرك التشكيل](#arab-06--توجيه-محرك-التشكيل--shaping-engine-routing)
- [`ARAB-07` كشف الاتجاه تلقائيًا](#arab-07--كشف-الاتجاه-تلقائيًا--auto-rtl-detection)
- [`ARAB-08` مفتاح لغة المحتوى](#arab-08--مفتاح-لغة-المحتوى--content-language-switch-arenboth)
- [`ARAB-09` نص حقيقي فوق لوحات التوليد](#arab-09--نص-حقيقي-فوق-لوحات-التوليد--real-type-over-generated-plates)
- [`ARAB-10` العربية داخل مشهد ثلاثي الأبعاد](#arab-10--العربية-داخل-مشهد-ثلاثي-الأبعاد--arabic-inside-3d-scenes)
- [`ARAB-11` خريطة أصوات الخطوط](#arab-11--خريطة-أصوات-الخطوط--arabic-font-voice-map)
- [`ARAB-12` كايرو المقسوم بنطاق يونيكود](#arab-12--كايرو-المقسوم-بنطاق-يونيكود--cairo-split-by-unicode-range)
- [`ARAB-13` اكتشاف الخطوط وسلسلة البدائل](#arab-13--اكتشاف-الخطوط-وسلسلة-البدائل--font-discovery--fallback-chain)
- [`ARAB-14` محمّل الخطوط الحي ومنتقي الخط](#arab-14--محمّل-الخطوط-الحي-ومنتقي-الخط--live-google-fonts-loader--picker)
- [`ARAB-15` اقترانات الخطوط](#arab-15--اقترانات-الخطوط--type-pairings)
- [`ARAB-16` سلّم أحجام الفيديو](#arab-16--سلّم-أحجام-الفيديو--video-type-scale-at-1080-px)
- [`ARAB-17` سلّم القراءة للشاشات](#arab-17--سلّم-القراءة-للشاشات--screen-reading-scale-v17--sqc)
- [`ARAB-18` قواعد التايبوغرافي العربي الحركي](#arab-18--قواعد-التايبوغرافي-العربي-الحركي--kinetic-arabic-grammar)
- [`ARAB-19` أقنعة الكلمات: إظهار وإخفاء](#arab-19--أقنعة-الكلمات-إظهار-وإخفاء--word-mask-reveal--hide)
- [`ARAB-20` صعود الكلمات من الضباب](#arab-20--صعود-الكلمات-من-الضباب--rise-from-blur-words)
- [`ARAB-21` مسح القناع من اليمين](#arab-21--مسح-القناع-من-اليمين--rtl-clip-wipe)
- [`ARAB-22` كتابة بقناع ناعم ورأس قلم](#arab-22--كتابة-بقناع-ناعم-ورأس-قلم--feathered-rtl-write-on-with-pen-head)
- [`ARAB-23` قناع ضربة فرشاة](#arab-23--قناع-ضربة-فرشاة--brush-stroke-mask-write-on)
- [`ARAB-24` سطور تصعد من خلف خط قطع](#arab-24--سطور-تصعد-من-خلف-خط-قطع--lines-rising-behind-a-cut-line)
- [`ARAB-25` انزلاق سطور عربية على Canvas](#arab-25--انزلاق-سطور-عربية-على-canvas--canvas-rtl-staggered-line-slide)
- [`ARAB-26` عنوان كلمات بنابض كل 160 مللي ثانية](#arab-26--عنوان-كلمات-بنابض-كل-160-مللي-ثانية--spring-word-stagger-title)
- [`ARAB-27` عنوان Remotion بنابض وأقراص كلمات](#arab-27--عنوان-remotion-بنابض-وأقراص-كلمات--remotion-spring-title--keyword-pills)
- [`ARAB-28` دخول الكلمة من العمق](#arab-28--دخول-الكلمة-من-العمق--3d-word-turn-in-from-depth)
- [`ARAB-29` الآلة الكاتبة بمؤشر](#arab-29--الآلة-الكاتبة-بمؤشر--typewriter-with-caret)
- [`ARAB-30` كلمة ضخمة من الضباب تنكمش إلى سطر](#arab-30--كلمة-ضخمة-من-الضباب-تنكمش-إلى-سطر--blur-in-hero-word-that-shrinks-into-the-sentence)
- [`ARAB-31` كبسولة الكلمات الدوّارة](#arab-31--كبسولة-الكلمات-الدوّارة--rolling-word-pill-with-growing-rings)
- [`ARAB-32` كشف بالحبر وسحب التركيز](#arab-32--كشف-بالحبر-وسحب-التركيز--ink-bleed--focus-pull-word-reveal)
- [`ARAB-33` كلمات على مسار دائري](#arab-33--كلمات-على-مسار-دائري--words-on-a-circular-path)
- [`ARAB-34` ضربة الكلمة المفتاحية بقناع صاعد](#arab-34--ضربة-الكلمة-المفتاحية-بقناع-صاعد--keyword-slam-with-upward-mask)
- [`ARAB-35` كلمة ترتطم وتستقر](#arab-35--كلمة-ترتطم-وتستقر--slam-and-settle-word)
- [`ARAB-36` ضربة الكلمة البطلة بتوهج](#arab-36--ضربة-الكلمة-البطلة-بتوهج--hero-word-punch-with-bloom)
- [`ARAB-37` الكلمة تمثّل معناها](#arab-37--الكلمة-تمثّل-معناها--word-acts-out-its-meaning)
- [`ARAB-38` صدى طباعي يتلاشى](#arab-38--صدى-طباعي-يتلاشى--typographic-echo)
- [`ARAB-39` تعبئات مذهّبة ومتدرجة ولمعة عابرة](#arab-39--تعبئات-مذهّبة-ومتدرجة-ولمعة-عابرة--gilded-gradient--sweeping-fills)
- [`ARAB-40` هرمية بثلاث مستويات](#arab-40--هرمية-بثلاث-مستويات--three-level-type-hierarchy)
- [`ARAB-41` تمييز الكلمة بالنجمة](#arab-41--تمييز-الكلمة-بالنجمة--asterisk-emphasis-convention)
- [`ARAB-42` خط متموّج تحت الكلمة المفتاحية](#arab-42--خط-متموّج-تحت-الكلمة-المفتاحية--squiggle-underline-highlight)
- [`ARAB-43` ممسحة التظليل من اليمين](#arab-43--ممسحة-التظليل-من-اليمين--rtl-highlighter-swipe)
- [`ARAB-44` ختم أحمر يرتطم](#arab-44--ختم-أحمر-يرتطم--rubber-stamp-slam)
- [`ARAB-45` علامة استفهام عملاقة مفرّغة](#arab-45--علامة-استفهام-عملاقة-مفرّغة--giant-outlined-question-mark)
- [`ARAB-46` ظل مزدوج مزاح](#arab-46--ظل-مزدوج-مزاح--offset-duotone-shadow-hero)
- [`ARAB-47` خط مضيء يتمدد تحت العنوان](#arab-47--خط-مضيء-يتمدد-تحت-العنوان--growing-glow-rule-under-the-title)
- [`ARAB-48` سطور تتكدس وتخفت](#arab-48--سطور-تتكدس-وتخفت--stacked-headline-lines-that-dim)
- [`ARAB-49` قوالب الموشن العربية الثمانية](#arab-49--قوالب-الموشن-العربية-الثمانية--eight-arabic-motion-templates)
- [`ARAB-50` شريط اسم سفلي تلقائي الاتجاه](#arab-50--شريط-اسم-سفلي-تلقائي-الاتجاه--auto-rtl-lower-third)
- [`ARAB-51` ثلاثة أشكال لعنوان الخطاف](#arab-51--ثلاثة-أشكال-لعنوان-الخطاف--hook-title-looks-box--kinetic--minimal)
- [`ARAB-52` صندوق عنوان يحافظ على مركزه](#arab-52--صندوق-عنوان-يحافظ-على-مركزه--centre-locked-resizing-title-box)
- [`ARAB-53` ترويسة اليوم بالهجري والميلادي](#arab-53--ترويسة-اليوم-بالهجري-والميلادي--hijri--gregorian-day-header)
- [`ARAB-54` أقراص وشارات وأرقام مرقّمة](#arab-54--أقراص-وشارات-وأرقام-مرقّمة--pills-chips--numbered-badges)
- [`ARAB-55` مكدّس عربي/إنجليزي](#arab-55--مكدّس-عربيإنجليزي--bilingual-arabicenglish-stacks--hud)
- [`ARAB-56` بطاقة شخصية من اليمين](#arab-56--بطاقة-شخصية-من-اليمين--rtl-character-card)
- [`ARAB-57` عنوان عربي سينمائي فوق الفيديو](#arab-57--عنوان-عربي-سينمائي-فوق-الفيديو--cinematic-arabic-headline-over-footage)
- [`ARAB-58` عنوان ASS متحرك لكل لقطة](#arab-58--عنوان-ass-متحرك-لكل-لقطة--per-shot-ass-animated-title-card)
- [`ARAB-59` غلاف بعنوان عربي مشكّل](#arab-59--غلاف-بعنوان-عربي-مشكّل--shaped-arabic-cover--thumbnail)
- [`ARAB-60` كاروسيل عربي PNG/PDF](#arab-60--كاروسيل-عربي-pngpdf--arabic-carousel-renderer)
- [`ARAB-61` طبقات نص الخط الزمني JSON](#arab-61--طبقات-نص-الخط-الزمني-json--timeline-json-text-overlays)
- [`ARAB-62` كاريوكي ASS عربي بثلاثة أنماط](#arab-62--كاريوكي-ass-عربي-بثلاثة-أنماط--arabic-ass-karaoke-captions-reels--cinema--punchy)
- [`ARAB-63` قانون زمن القراءة والكثافة](#arab-63--قانون-زمن-القراءة-والكثافة--reading-time--density-law)
- [`ARAB-64` منطقة الترجمة الآمنة وشكلها](#arab-64--منطقة-الترجمة-الآمنة-وشكلها--caption-safe-zone--look)
- [`ARAB-65` الكلمة المنطوقة تضيء](#arab-65--الكلمة-المنطوقة-تضيء--spoken-word-illumination-html-captions)
- [`ARAB-66` فيلم الكلمات من الصوت](#arab-66--فيلم-الكلمات-من-الصوت--verse-film-from-sound-song--poem--dua)
- [`ARAB-67` تقسيم الأسطر بالبرمجة الديناميكية](#arab-67--تقسيم-الأسطر-بالبرمجة-الديناميكية--dp-line-breaking-for-lyrics--dua)
- [`ARAB-68` اختيار الكلمة المفتاحية بالنبر](#arab-68--اختيار-الكلمة-المفتاحية-بالنبر--stress-based-keyword-picking)
- [`ARAB-69` توحيد النص العربي للمطابقة](#arab-69--توحيد-النص-العربي-للمطابقة--arabic-normalisation-for-alignment--matching)
- [`ARAB-70` النص المشكول مصدرًا للتوقيت](#arab-70--النص-المشكول-مصدرًا-للتوقيت--vowelled-source-text-over-asr)
- [`ARAB-71` ستايل الكلمات العاطفي](#arab-71--ستايل-الكلمات-العاطفي--emotional-lyric-style-preset)
- [`ARAB-72` العزل الاتجاهي](#arab-72--العزل-الاتجاهي--bidi-isolation)
- [`ARAB-73` نظام أرقام واحد وأرقام جدولية](#arab-73--نظام-أرقام-واحد-وأرقام-جدولية--one-digit-system--tabular-figures)
- [`ARAB-74` منسّق الأرقام الهندية الحتمي](#arab-74--منسّق-الأرقام-الهندية-الحتمي--deterministic-arabic-indic-money-formatter)
- [`ARAB-75` قراءة الأرقام والوحدات العربية](#arab-75--قراءة-الأرقام-والوحدات-العربية--digit-parsing--numberunit-detection)
- [`ARAB-76` صيغ الجمع ومطابقة العدد](#arab-76--صيغ-الجمع-ومطابقة-العدد--plural--count-agreement)
- [`ARAB-77` رقم يتحول إلى عنوان](#arab-77--رقم-يتحول-إلى-عنوان--number--headline)
- [`ARAB-78` حوار طباعي](#arab-78--حوار-طباعي--typographic-dialogue)
- [`ARAB-79` الدعوة والسعر بالعربية](#arab-79--الدعوة-والسعر-بالعربية--arabic-cta--price-isolation)
- [`ARAB-80` تسميات عربية مُسقطة على الخرائط والعوالم](#arab-80--تسميات-عربية-مُسقطة-على-الخرائط-والعوالم--projected-arabic-labels-maps--isometric--charts)
- [`ARAB-81` إصلاح أسماء الملفات العربية المشوّهة](#arab-81--إصلاح-أسماء-الملفات-العربية-المشوّهة--arabic-file-name-mojibake-repair)
- [`ARAB-82` سطر الحقوق الآمن](#arab-82--سطر-الحقوق-الآمن--safe-credit-line-burn)
- [`ARAB-83` تسمية الألوان بالعربية](#arab-83--تسمية-الألوان-بالعربية--arabic-colour-naming)
- [`ARAB-84` التقاط ستايل النص وإعادة تركيبه](#arab-84--التقاط-ستايل-النص-وإعادة-تركيبه--text-style-capture--compositing)
- [`ARAB-85` قياس حركة النص وتصنيفها](#arab-85--قياس-حركة-النص-وتصنيفها--text-animation-measurement--replay)
- [`ARAB-86` مطابقة الخط بالحبر](#arab-86--مطابقة-الخط-بالحبر--font-matching-by-ink)
- [`ARAB-87` ملاءمة العرض والتصغير التلقائي](#arab-87--ملاءمة-العرض-والتصغير-التلقائي--fit-width--shrink-to-fit)
- [`ARAB-88` نص مشكّل في المشاهد المرسومة واستيراد SVG](#arab-88--نص-مشكّل-في-المشاهد-المرسومة-واستيراد-svg--shaped-text-in-painted-scenes--svg-import)
- [`ARAB-89` طبقات نص عربي على Canvas](#arab-89--طبقات-نص-عربي-على-canvas--canvas-rtl-text-layer-helpers)
- [`ARAB-90` دوران كتلة النص 90° ككاميرا](#arab-90--دوران-كتلة-النص-90-ككاميرا--type-block-90-rotation-as-camera-move)
- [`ARAB-91` مصمم: نص عربي قابل للتعديل بتشكيل HarfRust وكشيدة](#arab-91--مصمم-نص-عربي-قابل-للتعديل-بتشكيل-harfrust-وكشيدة--mosamem-editable-arabic-text-with-harfrust-shaping-and-kashida-justification)
- [`ARAB-92` أربعة خطوط عربية مفتوحة يرفقها مصمم](#arab-92--أربعة-خطوط-عربية-مفتوحة-يرفقها-مصمم--four-open-arabic-fonts-bundled-by-mosamem-ibm-plex-sans-arabic-cairo-tajawal-amiri)
- [`ARAB-U01` خط El Messiri العربي مضمّن](#arab-u01--خط-el-messiri-العربي-مضمّن--el-messiri-arabic-display-font-bundled-ofl)
- [`ARAB-X01` كشف الكلمة العربية كاملة من اليمين](#arab-x01--كشف-الكلمة-العربية-كاملة-من-اليمين--rtl-whole-word-lyric-reveal-with-key-word-pop)
- [`ARAB-X02` ترشيح الخط لا الجزم به](#arab-x02--ترشيح-الخط-لا-الجزم-به--font-matches-are-candidates-not-identities)
- [`ARAB-X03` الزخرفة والكشيدة للنبذة فقط](#arab-x03--الزخرفة-والكشيدة-للنبذة-فقط--unicode-ornaments-and-kashida-bios-only)
- [`ARAB-X04` مطابقة الخط عبر محرك تشكيل حقيقي](#arab-x04--مطابقة-الخط-عبر-محرك-تشكيل-حقيقي--font-matching-through-a-real-shaper-chromiumharfbuzz)
- [`ARAB-X05` تجميع عائلة خط مطابقة من مصدرين OFL](#arab-x05--تجميع-عائلة-خط-مطابقة-من-مصدرين-ofl--assemble-a-matched-ofl-family-from-two-masters)
- [`ARAB-X06` عنوان خطي مركّب من حدود حروف مفتوحة](#arab-x06--عنوان-خطي-مركّب-من-حدود-حروف-مفتوحة--composed-calligraphic-title-from-ofl-outlines)

## البطاقات / cards

### `ARAB-01` — الكلمة كاملة لا الحرف / Whole-word law

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الحرف العربي يتغير شكله حسب موقعه، فكل span لحرف واحد يكسر الوصل؛ حرّك الكلمة أو العبارة أو السطر كوحدة. / Arabic letters change shape by position, so per-letter spans break joining; animate words, phrases or lines as units.

**متى:** حين تحرك نصا عربيا كلمة بكلمة وتريد ألا تنكسر الحروف المتصلة / when animating Arabic text and letters must stay joined instead of per-letter splits

**كيف:** Split on spaces only (keep ZWJ U+200D / ZWNJ U+200C inside words); one inline-block span per word inside a direction:rtl container; to 'write' a word progressively use a mask/clip wipe over the shaped word (ARAB-21/22), never letters. Latin in the same film may go per letter; Arabic goes per word or per shaped glyph-run (text-to-path). The tested canvas starter splits its title exactly this way. (code snippet in references/powers/typography-arabic.md)

**المعاملات:** Latin letter stagger 25 ms, in 40 px / 320 ms cubic-bezier(0.2,0.9,0.2,1), out 180 ms; Arabic word stagger 60–160 ms; ≤5–7 words per screen

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كلمة كاملة · اتصال الحروف · تفكيك الحروف · whole word · letter joining · split text · rtl · kinetic · حروف مقطعة · تحريك النص · نص متحرك · per-word animation · arabic text animation

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/starters/html-canvas/index.html:97`
- `kosif-tool/playbooks/arabic-typography.md:25`
- `100-superskills/skills/kinetic-typography-arabic/SKILL.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-typography/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-02` حصر الاتجاه في عناصر النص / RTL scoping for renderers (proven)
- `ARAB-03` لا تباعد ولا مطّ — الكشيدة فقط / No tracking, no stretch — kashida only (documented)

### `ARAB-02` — حصر الاتجاه في عناصر النص / RTL scoping for renderers

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** في HyperFrames يبدو ‎<html dir="rtl">‎ سليمًا في المعاينة لكن الرندر يخرج أسود بالكامل؛ ضع direction:rtl وunicode-bidi:isolate على عناصر النص فقط. / In HyperFrames <html dir="rtl"> previews fine but renders a fully black video; scope direction:rtl + unicode-bidi:isolate to text elements.

**متى:** عند رندر فيديو عربي في HyperFrames يخرج أسود رغم سلامة المعاينة / when a HyperFrames render of Arabic HTML comes out black though the preview looked fine

**كيف:** Keep <html lang="ar"> with no dir; CSS .line{direction:rtl;unicode-bidi:isolate}; Latin lockups get direction:ltr; numbers such as 24 get direction:ltr inside Arabic layouts. The vendor linter raises html_dir_attribute_breaks_render (severity error, also for dir="auto") and kosif-studio qa.py checks it too. Ordinary web pages (not renders) may keep <html dir=rtl> with logical CSS properties (margin-inline-start).

**المعاملات:** lint id html_dir_attribute_breaks_render

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** اتجاه · rtl · dir · hyperframes · black video · شاشة سوداء · unicode-bidi · lint · فيديو أسود · من اليمين لليسار · رندر · render black · direction css

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-one/vendor/hyperframes/packages/lint/src/rules/composition.ts:1150`
- `kosif-one/vendor/hyperframes/packages/lint/src/rules/composition.test.ts`
- `kosif-studio/motion/qa.py:62`
- `kosif-studio/tests/test_studio.py:549`

#### 7. قدرات قريبة في العائلة

- `ARAB-01` الكلمة كاملة لا الحرف / Whole-word law (proven)
- `ARAB-03` لا تباعد ولا مطّ — الكشيدة فقط / No tracking, no stretch — kashida only (documented)
- `ARAB-04` بوابة تحميل الخط قبل الإطار الأول / Font-ready gate before frame 0 (ready)

### `ARAB-03` — لا تباعد ولا مطّ — الكشيدة فقط / No tracking, no stretch — kashida only

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** letter-spacing يقطع الوصل وscaleX غير المتساوي يشوّه الضربات؛ الإطالة بالكشيدة (ـ U+0640) أو محور wdth فقط. / Letter-spacing breaks joins and non-uniform scaleX distorts strokes; elongate only with kashida or a wdth axis.

**متى:** حين تريد إطالة كلمة عربية أو توسيع عنوان دون أن تنقطع الحروف أو تتشوه / when elongating an Arabic word or widening a title without breaking joins or distorting strokes

**كيف:** letter-spacing:0 on every Arabic run (some owner hero CSS uses −.035em — keep that for Latin only); insert tatweel between two joining letters in designed titles, sparingly, never animated per character; scale the word uniformly (scale, never scaleX); for elastic width use a variable font's wdth axis. The Latin 'tracking 0.3em→0 in 0.6 s' entrance is Latin-only.

**المعاملات:** letter-spacing 0; kashida U+0640; uniform scale only

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كشيدة · تطويل · تباعد الحروف · kashida · tatweel · letter-spacing · tracking · stretch · مط الكلمة · تمديد العنوان · إطالة الحروف · elongation · wdth axis

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/playbooks/arabic-typography.md:28`
- `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`
- `100-superskills/skills/kosif-montage-motion/references/launch-video.md`
- `kosif-one/tools/kosif-omni/skills/kosif-web-design/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-01` الكلمة كاملة لا الحرف / Whole-word law (proven)
- `ARAB-02` حصر الاتجاه في عناصر النص / RTL scoping for renderers (proven)
- `ARAB-04` بوابة تحميل الخط قبل الإطار الأول / Font-ready gate before frame 0 (ready)
- `ARAB-05` مساحة التشكيل وحواف الأقنعة / Harakat headroom & mask padding (ready)

### `ARAB-04` — بوابة تحميل الخط قبل الإطار الأول / Font-ready gate before frame 0

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لا يبدأ الرندر ولا القياس قبل أن يُحمَّل كل وزن خط بعيّنة عربية، وإلا يُخبز الخط البديل في الفيديو. / Never capture or measure before every weight is loaded with an Arabic sample, or fallback glyphs get baked in.

**متى:** عند رندر نص عربي أو قياسه حتى لا يظهر خط بديل أو مربعات في الفيديو / when about to render or measure Arabic text, so fallback glyphs never get baked into the video

**كيف:** HTML: await document.fonts.load('800 62px "Cairo"', 'الأرنب') per weight, then document.fonts.ready; Basma fontsReady() gathers the caption font + Lalezar/Cairo/Reem Kufi/Plex + every family named in scene code (regex font:"…"), loads 400/700/900 with the sample 'بصمة Aa 123' and races a 4 s timeout. Remotion: loadFont({family, url: staticFile('X.woff2'), weight}) once per weight + delayRender. Measure only after the gate.

**المعاملات:** weights 400/700/900; timeout 4000 ms; sample = Arabic + Latin + digits

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تحميل الخط · خط بديل · font loading · fonts.ready · delayRender · fallback glyphs · tofu · الخط لا يظهر · مربعات بدل الحروف · انتظار الخط · font not loaded · first frame

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:136`
- `app/public/js/00_editor.js:2932`
- `kosif-atlas/skills/2712-remotion/10436-remotion-markup/local-fonts.md`
- `kosif-tool/playbooks/arabic-typography.md:15`

#### 7. قدرات قريبة في العائلة

- `ARAB-02` حصر الاتجاه في عناصر النص / RTL scoping for renderers (proven)
- `ARAB-03` لا تباعد ولا مطّ — الكشيدة فقط / No tracking, no stretch — kashida only (documented)
- `ARAB-05` مساحة التشكيل وحواف الأقنعة / Harakat headroom & mask padding (ready)
- `ARAB-06` توجيه محرك التشكيل / Shaping-engine routing (proven)

### `ARAB-05` — مساحة التشكيل وحواف الأقنعة / Harakat headroom & mask padding

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** النقاط والحركات تخرج عن صندوق السطر، فالقناع الضيق يقصّها؛ اترك 0.15–0.25em وزِد حشوة القناع من الأسفل. / Dots and diacritics overflow the line box, so tight masks clip them; leave 0.15–0.25 em and pad masks at the bottom.

**متى:** حين تقص الأقنعة نقاط الحروف أو الحركات أسفل الكلمة العربية / when masks or tight line boxes clip Arabic dots, kasra or descenders

**كيف:** motion-kit word mask = clip-path inset(-0.05em -0.05em 0 -0.05em) with padding .06em .04em .18em (extra bottom for kasra and descenders); titles line-height ≥1.25, body 1.5–1.85; line wrappers that rise from a cut line need generous line-height; inspect dots at the mask edge on a still frame.

**المعاملات:** headroom 0.15–0.25 em; mask padding .06/.04/.18 em; body lh 1.85 (v17)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تشكيل · حركات · نقاط · harakat · diacritics · tashkeel · mask · clip · line-height · قص النقاط · تباعد الأسطر · حشوة القناع · clipped dots · mask padding

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:129`
- `kosif-tool/playbooks/arabic-typography.md:71-73`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md`
- `kosif-audit-pro/patch/kosif-v17.css`

#### 7. قدرات قريبة في العائلة

- `ARAB-03` لا تباعد ولا مطّ — الكشيدة فقط / No tracking, no stretch — kashida only (documented)
- `ARAB-04` بوابة تحميل الخط قبل الإطار الأول / Font-ready gate before frame 0 (ready)
- `ARAB-06` توجيه محرك التشكيل / Shaping-engine routing (proven)
- `ARAB-07` كشف الاتجاه تلقائيًا / Auto RTL detection (ready)

### `ARAB-06` — توجيه محرك التشكيل / Shaping-engine routing

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** محرك واحد فقط يشكّل العربية: المتصفح (HarfBuzz) أو Pillow+RAQM أو libass — ولا تشكّل النص مرتين أبدًا. / Exactly one engine shapes Arabic — the browser, Pillow+RAQM or libass — never two in a row.

**متى:** حين يظهر النص العربي مقطعا أو معكوسا في صورة أو فيديو وتحتاج اختيار محرك تشكيل واحد / when Arabic comes out disjointed or reversed and you must pick one shaping engine

**كيف:** Chromium/Remotion/HyperFrames shape automatically and are best for full tashkeel (mimic sets engine:'browser' for harakat). Pillow here has RAQM 0.10.5 → pass RAW logical text with layout_engine=RAQM. Only when RAQM is absent use arabic_reshaper + python-bidi, and then the font must carry Presentation Forms-B (Amiri, Noto Naskh). In ffmpeg use the ass/subtitles filters (libass + HarfBuzz + FriBiDi), not drawtext. Owner model code: mm_render_text (RAQM → 'pil' engine, else 'ass' engine with two-background matting) and wbcompat._shape. Verified in this container on 2026-10-16 with Cairo: RAQM on raw text = correct; reshaper+bidi fed into RAQM = words and letters reversed; reshaper + BASIC layout = tofu on isolated forms (ا إ ر) because Cairo lacks those Presentation-Forms code points (Amiri and Noto Naskh carry FE70–FEFC); drawtext = the same tofu, and text_shaping=0 = disjoint, reversed letters. (code snippet in references/powers/typography-arabic.md)

**المعاملات:** PIL features.check('raqm') == True (0.10.5); ffmpeg 6.1.1 --enable-libass --enable-libfribidi --enable-libharfbuzz

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تشكيل · harfbuzz · raqm · pillow · arabic_reshaper · bidi · libass · drawtext · shaping · reversed text · نص معكوس · حروف منفصلة · نص مقلوب · ربط الحروف · disconnected letters · ffmpeg arabic

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:arabic-reshaper` ← python3 -c "import arabic-reshaper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/mimic/mm_render_text.py`
- `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:212`
- `100-superskills/skills/kosif-montage-motion/references/mimic.md`
- `kosif-atlas/skills/2329-localization-i18n-engineering/8940-i18n-foundations-and-icu/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-04` بوابة تحميل الخط قبل الإطار الأول / Font-ready gate before frame 0 (ready)
- `ARAB-05` مساحة التشكيل وحواف الأقنعة / Harakat headroom & mask padding (ready)
- `ARAB-07` كشف الاتجاه تلقائيًا / Auto RTL detection (ready)
- `ARAB-08` مفتاح لغة المحتوى / Content-language switch ar\|en\|both (proven)

### `ARAB-07` — كشف الاتجاه تلقائيًا / Auto RTL detection

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تعبير منتظم واحد يلتقط الحروف العربية فيقلب اتجاه الرسم والمحاذاة وجانب البطاقة تلقائيًا. / One regex spots Arabic letters and flips drawing direction, alignment and card side automatically.

**متى:** حين يختلط نص عربي وإنجليزي وتريد قلب الاتجاه والمحاذاة تلقائيا / when mixed Arabic and English input should flip direction, alignment and card side automatically

**كيف:** Canvas: ctx.direction = /[\u0600-\u06FF]/.test(s) ? 'rtl' : 'ltr'; lowerThird picks side and sets RTL on the box only; the review page's AR_RUN regex (U+0600–06FF, 0750–077F, FB50–FDFF, FE70–FEFF with ZWJ/ZWNJ, spaces and «») wraps each Arabic run in <bdi dir=rtl>.

**المعاملات:** ranges U+0600–06FF, 0750–077F, FB50–FDFF, FE70–FEFF

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كشف اللغة · اتجاه تلقائي · auto direction · detect arabic · regex · canvas · محاذاة لليمين · اكتشاف العربية · نص مختلط · rtl detection · text alignment

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `fastify-motion-bro/web/editorial.js:75`
- `app/public/js/00_editor.js:17`
- `kosif-studio/motion/kit/motion-kit.js:562`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:902`

#### 7. قدرات قريبة في العائلة

- `ARAB-05` مساحة التشكيل وحواف الأقنعة / Harakat headroom & mask padding (ready)
- `ARAB-06` توجيه محرك التشكيل / Shaping-engine routing (proven)
- `ARAB-08` مفتاح لغة المحتوى / Content-language switch ar\|en\|both (proven)
- `ARAB-09` نص حقيقي فوق لوحات التوليد / Real type over generated plates (proven)

### `ARAB-08` — مفتاح لغة المحتوى / Content-language switch ar\|en\|both

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خيار واحد عند تجهيز المشروع يحدد: عربي فقط، أو إنجليزي فقط، أو ثنائي اللغة مع اتجاه لكل سطر. / One scaffold flag fixes Arabic-only, English-only or bilingual with per-line direction.

**متى:** عند بدء مشروع موشن وتحديد هل النص عربي فقط أو إنجليزي فقط أو باللغتين / when scaffolding a project and choosing Arabic-only, English-only or bilingual text

**كيف:** python3 tools/kosif.py scaffold <style-id> <dir> --content-lang ar\|en\|both (default ar). ar = Arabic only, RTL, a clear Arabic face; both = Arabic and English together, each line with its own dir (English ~70% size under the Arabic, see ARAB-55).

**المعاملات:** default ar

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** لغة المحتوى · ثنائي اللغة · content language · bilingual · scaffold · kosif.py · عربي وإنجليزي · مشروع جديد · لغتين · arabic only · content-lang

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/tools/kosif.py:83`
- `kosif-tool/playbooks/arabic-typography.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-06` توجيه محرك التشكيل / Shaping-engine routing (proven)
- `ARAB-07` كشف الاتجاه تلقائيًا / Auto RTL detection (ready)
- `ARAB-09` نص حقيقي فوق لوحات التوليد / Real type over generated plates (proven)
- `ARAB-10` العربية داخل مشهد ثلاثي الأبعاد / Arabic inside 3D scenes (documented)

### `ARAB-09` — نص حقيقي فوق لوحات التوليد / Real type over generated plates

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نماذج الصور تشوّه الحروف العربية، فولّد المشهد بلا نص ثم ضع العربية طبقة HTML/SVG حقيقية بخط مفتوح. / Image models garble Arabic; generate textless art and overlay real HTML/SVG type in an open font.

**متى:** حين تولد صورة أو خلفية بالذكاء الاصطناعي وتحتاج عليها كتابة عربية سليمة / when you need correct Arabic text on an AI-generated image or background

**كيف:** Generation fields stay English; append 'No text, no labels, no captions, no watermark'; reserve a clean band (e.g. a bottom caption bar); the owner prompt linter REVISEs any prompt containing Arabic letters and the forge emits INFO arabic_text for U+0600–06FF; then set the Arabic in SVG/HTML/Remotion with Plex or Cairo and animate it in code. Comics: panels without text, bubbles drawn in code. If text must live inside the image, quote it for Ideogram (account/key) — still check the joins.

**المعاملات:** trigger range U+0600–06FF; overlay fonts IBM Plex Sans Arabic / Cairo

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صورة مولدة · ذكاء اصطناعي · بلا نص · textless · ai image · overlay · prompt lint · ideogram · كتابة على الصورة · حروف مشوهة · عنوان فوق الصورة · garbled text · text overlay

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-one/tools/kosif-omni/skills/kosif-image-studio/scripts/prompt_lint.py`
- `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/scripts/prompt_forge.py:121`
- `100-superskills/skills/image-prompt-forge/scripts/image_prompt_forge.py:56`
- `kosif-atlas/skills/1094-akbun-draw/2423-akbun-draw-webtoon-b`

#### 7. قدرات قريبة في العائلة

- `ARAB-07` كشف الاتجاه تلقائيًا / Auto RTL detection (ready)
- `ARAB-08` مفتاح لغة المحتوى / Content-language switch ar\|en\|both (proven)
- `ARAB-10` العربية داخل مشهد ثلاثي الأبعاد / Arabic inside 3D scenes (documented)
- `ARAB-11` خريطة أصوات الخطوط / Arabic font voice map (ready)

### `ARAB-10` — العربية داخل مشهد ثلاثي الأبعاد / Arabic inside 3D scenes

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لا تبثق العربية هندسةً ثلاثية الأبعاد من خط غير مُشكّل؛ ارسمها على نسيج Canvas باتجاه rtl أو ضعها طبقة HTML فوق المشهد. / Never extrude Arabic as 3D geometry from an unshaped font; use a CanvasTexture drawn RTL or an HTML overlay.

**متى:** حين تضع كلمة أو عنوانا عربيا داخل مشهد ثلاثي الأبعاد / when placing Arabic words or a title inside a 3D scene

**كيف:** Draw the whole line on a 2D canvas after the font gate (ctx.direction='rtl', ctx.textAlign='right', fillText(wholeString)) → THREE.CanvasTexture on a plane (anisotropy on, size ×2 for sharpness); or project an HTML label per frame (ARAB-80). Check joins on a rendered still.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ثلاثي الأبعاد · 3d · three.js · canvastexture · extrude · overlay · نص ثلاثي · مجسم · كتابة مجسمة · 3d text · texture

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/playbooks/3d.md:74`

#### 7. قدرات قريبة في العائلة

- `ARAB-08` مفتاح لغة المحتوى / Content-language switch ar\|en\|both (proven)
- `ARAB-09` نص حقيقي فوق لوحات التوليد / Real type over generated plates (proven)
- `ARAB-11` خريطة أصوات الخطوط / Arabic font voice map (ready)
- `ARAB-12` كايرو المقسوم بنطاق يونيكود / Cairo split by unicode-range (proven)

### `ARAB-11` — خريطة أصوات الخطوط / Arabic font voice map

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | كلها OFL-1.1؛ ما يشبه Thmanyah أو Dubai أو Diwani في المراجع خطوط مملوكة — مرجع فقط / all OFL-1.1; Thmanyah-, Dubai- and Diwani-like faces seen in references are proprietary — reference only. |

**ما هي:** عائلات OFL مرتبة حسب «الصوت» — كوفي، سانس حديث، نسخ، رقعة، عرض — وملفاتها موجودة على القرص. / OFL families sorted by voice — Kufi, modern sans, Naskh, Ruqaa, display — with the files already on disk.

**متى:** حين تختار خطا عربيا يناسب طابع الفيديو من الخطوط المتاحة على القرص / when choosing an Arabic typeface that fits the film's voice from the fonts already on disk

**كيف:** Pick by voice (table). Files on disk: 100-superskills/skills/kosif-mimic/assets/fonts (23 TTF + OFL-LICENSES.txt), kosif-tool/.claude/skills/kosif-superpowers/proofs/_shared/fonts (Amiri, Aref Ruqaa, Cairo variable, Lalezar, Reem Kufi variable, Tajawal Bold), kosif-earth-ci-fork/ui/art/fonts (Plex/Readex/Tajawal/Naskh woff2 subsets). The full catalogue (41 families / 81 faces) lives in mm_fonts_lib; its fetch pulls from google/fonts — raw.githubusercontent.com is reachable here, github.com raw is not.

**المعاملات:** catalogue: sans 12, naskh 10, display 8, kufi 4, rounded 2, hand 2, nastaliq 2, ruqaa 1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خطوط · كوفي · نسخ · رقعة · font · kufi · naskh · ruqaa · ofl · cairo · tajawal · amiri · lalezar · اختيار الخط · خط عربي · فونت · font choice · arabic typeface

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/_shared/fonts`
- `kosif-tool/.claude/skills/kosif-superpowers/scripts/mimic/mm_fonts_lib.py`
- `app/index.html:10`

#### 7. قدرات قريبة في العائلة

- `ARAB-09` نص حقيقي فوق لوحات التوليد / Real type over generated plates (proven)
- `ARAB-10` العربية داخل مشهد ثلاثي الأبعاد / Arabic inside 3D scenes (documented)
- `ARAB-12` كايرو المقسوم بنطاق يونيكود / Cairo split by unicode-range (proven)
- `ARAB-13` اكتشاف الخطوط وسلسلة البدائل / Font discovery & fallback chain (ready)

### `ARAB-12` — كايرو المقسوم بنطاق يونيكود / Cairo split by unicode-range

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** Cairo 600/800 في ملفي woff2 (عربي ولاتيني) تحت عائلة واحدة، مدمج في كل قوالب الموشن. / Cairo 600/800 shipped as Arabic + Latin woff2 subsets under one family, wired into every motion template.

**متى:** حين تضبط خط Cairo لقوالب الموشن بملف عربي وآخر لاتيني تحت عائلة واحدة / when wiring Cairo into motion templates as Arabic and Latin woff2 subsets of one family

**كيف:** @font-face family 'Cairo' for weights 800/600; the Arabic file covers U+0600-06FF, U+0750-077F, U+FB50-FDFF, U+FE70-FEFF (+U+0660-0669), the Latin file U+0000-00FF; mtemplates copies both into projects/NAME/assets/fonts; preload per ARAB-04. Earth uses the same split for Plex/Readex/Tajawal/Naskh (adds U+0870-088E). For renders use font-display:block (swap is for web pages). (code snippet in references/powers/typography-arabic.md)

**المعاملات:** Arabic 800 = 13,880 B, 600 = 13,828 B; Latin 800 = 15,256 B, 600 = 15,252 B

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cairo · القاهرة · unicode-range · woff2 · subset · font-face · تقسيم الخط · خط كايرو · تضمين الخط · ملف الخط · font subsetting · webfont

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/kit/fonts/cairo-arabic-800-normal.woff2`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/fonts/OFL-Cairo.txt`
- `100-superskills/skills/kosif-montage-motion/templates/motion/title-card.html:9`
- `kosif-earth-ci-fork/ui/ds/fonts.css`

#### 7. قدرات قريبة في العائلة

- `ARAB-10` العربية داخل مشهد ثلاثي الأبعاد / Arabic inside 3D scenes (documented)
- `ARAB-11` خريطة أصوات الخطوط / Arabic font voice map (ready)
- `ARAB-13` اكتشاف الخطوط وسلسلة البدائل / Font discovery & fallback chain (ready)
- `ARAB-14` محمّل الخطوط الحي ومنتقي الخط / Live Google Fonts loader & picker (ready)

### `ARAB-13` — اكتشاف الخطوط وسلسلة البدائل / Font discovery & fallback chain

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | Dubai خط مملوك (مايكروسوفت/دبي) للاستخدام المحلي فقط ولا يُشحن مع المشروع؛ بدائل Noto برخصة OFL / Dubai is proprietary — local use only, never ship it; Noto fallbacks are OFL. |

**ما هي:** يبحث عن ملفات خطوط تدعم العربية في مجلدات ويندوز ولينكس وماك وkit/fonts ويرتبها حسب الاكتمال — ويتوقف بدل الاستبدال الصامت. / Finds Arabic-capable font files across OS folders and kit/fonts, ranked by completeness — stop rather than silently substitute.

**متى:** حين تبحث عن خطوط تدعم العربية على الجهاز وتريد التوقف بدل استبدال صامت / when finding Arabic-capable fonts on the machine and refusing a silent substitution

**كيف:** python kosif-studio/motion/tools.py fonts. Pillow order (tools._ARABIC): NotoNaskhArabic → NotoSansArabic → NotoKufiArabic → Cairo → Tajawal → Almarai → Amiri → Scheherazade → KacstOne → DejaVuSans. CSS chain 'KD'/'KV': Dubai 300/500/700 → Noto Kufi/Sans Arabic → DejaVu. Remotion FONT: Noto Naskh → Noto Sans → Cairo → Tajawal → Plex → Segoe UI → DejaVu → system-ui. Here `fc-list :lang=ar` shows only DejaVu/FreeSerif/FreeMono/Unifont, so always point renders at repo font files (ARAB-11) or pass fontsdir= to libass.

**المعاملات:** check: fc-list :lang=ar; fonttools cmap check before render

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** اكتشاف الخطوط · خط بديل · fallback · fc-list · font discovery · noto · dubai · خطوط الجهاز · البحث عن خط · خط مفقود · installed fonts · missing font

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:fonttools` ← python3 -c "import fonttools" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-studio/motion/tools.py:79`
- `100-superskills/skills/kosif-montage-motion/scripts/tools.py:81`
- `kosif-studio/motion/templates/directed.html`
- `kosif-tool/starters/remotion/src/Film.tsx:34`

#### 7. قدرات قريبة في العائلة

- `ARAB-11` خريطة أصوات الخطوط / Arabic font voice map (ready)
- `ARAB-12` كايرو المقسوم بنطاق يونيكود / Cairo split by unicode-range (proven)
- `ARAB-14` محمّل الخطوط الحي ومنتقي الخط / Live Google Fonts loader & picker (ready)
- `ARAB-15` اقترانات الخطوط / Type pairings (proven)

### `ARAB-14` — محمّل الخطوط الحي ومنتقي الخط / Live Google Fonts loader & picker

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حقن رابط Google Fonts عند الطلب لتبديل خط الواجهة أو العنوان مباشرة أثناء المراجعة. / Inject a Google Fonts link on demand to swap the UI or title face live during review.

**متى:** حين تريد تجربة أكثر من خط للعنوان أو الواجهة مباشرة أثناء المراجعة / when trying different title or UI fonts live during a review

**كيف:** FONTS table + loadFont(id) creates <link id=sk-font-*> to fonts.googleapis.com/css2 with display=swap (+ preconnect fonts.gstatic.com), then sets --sk-font / --sk-font-display. Earth picker: Plex, Tajawal 400–800, Cairo 400–800, Almarai 400/700/800, Noto Kufi 400–800, Readex 400–700, Noto Naskh 400–700, system-ui; review page adds El Messiri, Amiri, Lalezar. fonts.googleapis.com is reachable here, but the final render must use vendored files (ARAB-12) so it never depends on the network.

**المعاملات:** 8 picker faces; review page 9 families

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** google fonts · منتقي الخط · font picker · تبديل الخط · live swap · تجربة الخطوط · تغيير الفونت · معاينة الخط · font preview · change font

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-earth-ci-fork/ui/layouts/shell.js:58`
- `kosif-audit-studio/index.html`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:9`
- `kosif-tool/starters/html-canvas/index.html:8`

#### 7. قدرات قريبة في العائلة

- `ARAB-12` كايرو المقسوم بنطاق يونيكود / Cairo split by unicode-range (proven)
- `ARAB-13` اكتشاف الخطوط وسلسلة البدائل / Font discovery & fallback chain (ready)
- `ARAB-15` اقترانات الخطوط / Type pairings (proven)
- `ARAB-16` سلّم أحجام الفيديو / Video type scale at 1080 px (documented)

### `ARAB-15` — اقترانات الخطوط / Type pairings

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عنوان كوفي فوق نص Plex، أو Readex للعربي مع Fraunces للاتيني — صوتان مختلفان بإيقاع واحد. / Kufi headlines over Plex body, or Readex Arabic with Fraunces Latin — two voices, one rhythm.

**متى:** حين تحتاج خطين متناسقين لعنوان ونص أو لعربي ولاتيني في تصميم واحد / when pairing a headline face with a body face, or Arabic with Latin, in one design

**كيف:** Editorial: .brand strong,h1,h2,h3 {font-family:'Noto Kufi Arabic','IBM Plex Sans Arabic'}; body Plex/Tajawal; hero h1 clamp(34px,5vw,68px) lh 1.16, hero p lh 2. Bilingual system: Fraunces 500/600 for Latin display + Readex Pro 300–700 for Arabic and UI, Latin tabular digits, scale 13/14/16/18/22/26/28 px, 4 px grid, radius 8/12/20/999. Ads: heavy Kufi with condensed uppercase Latin at matched x-height, ≥96 px. Rule: same mood, explicit size per script in tokens.json.

**المعاملات:** Kufi+Plex; Readex+Fraunces; Kufi+condensed Latin ≥96 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** اقتران الخطوط · pairing · kufi · plex · readex · fraunces · bilingual type · تنسيق الخطوط · خط العنوان · خط النص · font pairing · headline font

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-audit-studio/kosif-one-editorial-theme.css`
- `kosif-one/tools/kosif-web/docs/04-design-system.md`
- `kosif-tool/styles/pm-deifosv-04e4d3/BRIEF.md`
- `100-superskills/skills/brand-identity-logo/SKILL.md:24`

#### 7. قدرات قريبة في العائلة

- `ARAB-13` اكتشاف الخطوط وسلسلة البدائل / Font discovery & fallback chain (ready)
- `ARAB-14` محمّل الخطوط الحي ومنتقي الخط / Live Google Fonts loader & picker (ready)
- `ARAB-16` سلّم أحجام الفيديو / Video type scale at 1080 px (documented)
- `ARAB-17` سلّم القراءة للشاشات / Screen reading scale (v17 / SQC) (ready)

### `ARAB-16` — سلّم أحجام الفيديو / Video type scale at 1080 px

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الترجمة 56–72 بكسل، العناوين 96–180، التسميات ≥32 — والعربية أكبر 10–15% من نظيرها اللاتيني. / Captions 56–72 px, titles 96–180, labels ≥32 — Arabic runs 10–15% larger than Latin.

**متى:** حين تحدد أحجام الترجمة والعناوين والتسميات في فيديو 1080 بكسل / when sizing captions, titles and labels for a 1080 px video

**كيف:** Tokens: title 700 88–120 px lh 1.15 (STYLE.md) up to hero 120–220 px (kinetic type); support 56–80; body 500 44–56 lh 1.4; label 600 32–40 lh 1.2; numerals 600 48–72, LTR inside RTL; lh 1.5–1.7 body/captions, 1.25–1.35 titles; weights 600–900 in motion (thin weights shimmer); chart labels never below ~24 px at 1080p (~12 px web); right-align paragraphs, centre titles and captions.

**المعاملات:** captions 56–72; titles 96–180; labels ≥32; +10–15% vs Latin

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أحجام الخط · سلم الطباعة · type scale · font size · 1080 · line-height · weights · حجم الترجمة · مقاس الخط · حجم العنوان · caption size · title size

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/playbooks/arabic-typography.md:16-19`
- `kosif-tool/templates/STYLE.md`
- `kosif-tool/playbooks/kinetic-type.md`
- `kosif-atlas/skills/345-visuals/1242-html-diagram/references/svg-primitives.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-14` محمّل الخطوط الحي ومنتقي الخط / Live Google Fonts loader & picker (ready)
- `ARAB-15` اقترانات الخطوط / Type pairings (proven)
- `ARAB-17` سلّم القراءة للشاشات / Screen reading scale (v17 / SQC) (ready)
- `ARAB-18` قواعد التايبوغرافي العربي الحركي / Kinetic Arabic grammar (ready)

### `ARAB-17` — سلّم القراءة للشاشات / Screen reading scale (v17 / SQC)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أربع درجات واضحة مكبّرة للنقاط والتشكيل بإيقاع عمودي واحد وقياس 78ch — للواجهات التي تظهر داخل الفيديو. / Four clear steps enlarged for dots and diacritics, one vertical rhythm, 78ch measure — for UI shown inside films.

**متى:** حين تصمم واجهة أو لوحة تظهر داخل الفيديو وتحتاج أحجام قراءة عربية واضحة / when designing a UI or dashboard shown inside a film with readable Arabic sizes

**كيف:** v17 tokens xs 13, sm 14, base 15.5 (was 13.5), lg 17, xl 21, 2xl 27 px; leading 1.85 / tight 1.4; spacing 6/12/18/26/38; max-width 78ch (line 41→69 chars); print 11pt/1.6. SQC: 12/13.5/16/17/22/28 (+11) px, weights 400 body / 600 labels / 700–800 headings, no 900, body lh 1.7, one fluid title clamp(24px,1.4vw+17px,32px) 800. Stack: IBM Plex Sans Arabic → Tajawal → Noto Sans Arabic → Arial; mono IBM Plex Mono.

**المعاملات:** base 15.5 px; lh 1.85; 78ch

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** واجهة · سلم القراءة · ui type · reading scale · dashboard · plex · لوحة تحكم · أحجام الواجهة · وضوح القراءة · ui font size · line length

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-audit-pro/patch/kosif-v17.css`
- `kosif-earth-ci-fork/ui/ds/tokens.css:35`
- `kosif-audit-pro/app/globals.css:147`
- `kosif-earth-ci-fork/docs/design/SQC-IDENTITY-ar.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-15` اقترانات الخطوط / Type pairings (proven)
- `ARAB-16` سلّم أحجام الفيديو / Video type scale at 1080 px (documented)
- `ARAB-18` قواعد التايبوغرافي العربي الحركي / Kinetic Arabic grammar (ready)
- `ARAB-19` أقنعة الكلمات: إظهار وإخفاء / Word-mask reveal & hide (proven)

### `ARAB-18` — قواعد التايبوغرافي العربي الحركي / Kinetic Arabic grammar

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قسّم النص إلى وحدات معنى ≤5 كلمات، كلمة مفتاحية واحدة لها دخول مميز، والباقي يدخل بهدوء من اليمين. / Meaning units of ≤5 words, one keyword with a distinct entrance, the rest enters quietly from the right.

**متى:** حين تبني فيديو كلمات متحركة بالعربية وتحتاج قواعد التقسيم والتوقيت والحجم / when building Arabic kinetic type and need rules for chunking, timing and sizing

**كيف:** ≤7 words on 9:16 (12 on 16:9); two sizes per scene (hero 120–220 px, support 56–80); entrance 300–450 ms translateY 40–70 px cubic-bezier(0.22,1,0.36,1), opacity in the first 60%; stagger 70–120 ms, or words.json start − 60 ms; exit 200–300 ms, always shorter than the entrance; hold ≥ 0.3 s + 0.06 s × characters; weights 300 vs 900 for contrast; 0.35 s per word when there is no audio; read every line twice on the contact sheet. Scaffold: python3 tools/kosif.py scaffold kinetic-arabic <dir>; preview node tools/render_html.cjs --preview.

**المعاملات:** ≤5 words/unit; 0.35 s/word; entrance 300–450 ms; stagger 70–120 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تايبوغرافي حركي · kinetic typography · kinetic-arabic · words.json · stagger · hook · نص متحرك · كلمات متحركة · موشن تايبو · text animation · word timing

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/playbooks/kinetic-type.md`
- `kosif-tool/styles/kinetic-arabic/SKILL.md`
- `100-superskills/skills/kinetic-typography-arabic/SKILL.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-16` سلّم أحجام الفيديو / Video type scale at 1080 px (documented)
- `ARAB-17` سلّم القراءة للشاشات / Screen reading scale (v17 / SQC) (ready)
- `ARAB-19` أقنعة الكلمات: إظهار وإخفاء / Word-mask reveal & hide (proven)
- `ARAB-20` صعود الكلمات من الضباب / Rise-from-blur words (ready)

### `ARAB-19` — أقنعة الكلمات: إظهار وإخفاء / Word-mask reveal & hide

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT). |

**ما هي:** كل كلمة داخل قناعها الخاص تنزلق للأعلى واحدة بعد الأخرى، والحروف متصلة في كل إطار. / Each word slides up out of its own mask in turn, letters joined in every frame.

**متى:** حين تريد ظهور العنوان كلمة كلمة صاعدة من قناعها ثم اختفاءها بنظافة / when a title should reveal word by word sliding up from masks, then hide cleanly

**كيف:** MOTION.words(el) → span.mk-w (mask) > span.mk-wi; MOTION.revealWords(tl, el, at, {from:'top', dur:.7, stagger:.07, ease:'expo.out'}) = yPercent 115→0, opacity 0→1; a .num child pops scale 0→1 in 0.6 s with spring 'snappy'; MOTION.hideWords(tl, el, at, {to:'down', dur:.45, stagger:.04}) power4.inOut, visibility hidden at +0.3 s. Projects tune dur 1.1 / stagger 0.12 / ease settle. Plain-JS twin (kinetic_2d): start_i = 0.3 + 0.22·i s, p = clamp((t − start)/0.7), ease = 1 − (1 − p)³, translateY((1 − ease)·100%); remove CSS transitions before capture; highlight word #f59e0b + text-shadow 0 0 35px rgba(245,158,11,.6).

**المعاملات:** reveal 0.7 s / 0.07 s expo.out; hide 0.45 s / 0.04 s power4.inOut; yPercent ±115

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قناع الكلمات · إظهار · إخفاء · revealWords · hideWords · word mask · motion-kit · gsap · title · ظهور العنوان · دخول الكلمات · انيميشن كلمات · text reveal · slide up

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:156`
- `kosif-studio/motion/kit/motion-kit.js:129`
- `100-superskills/skills/kosif-montage-motion/templates/motion/title-card.html`
- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/kinetic_2d.html:111`

#### 7. قدرات قريبة في العائلة

- `ARAB-17` سلّم القراءة للشاشات / Screen reading scale (v17 / SQC) (ready)
- `ARAB-18` قواعد التايبوغرافي العربي الحركي / Kinetic Arabic grammar (ready)
- `ARAB-20` صعود الكلمات من الضباب / Rise-from-blur words (ready)
- `ARAB-21` مسح القناع من اليمين / RTL clip wipe (documented)

### `ARAB-20` — صعود الكلمات من الضباب / Rise-from-blur words

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT). |

**ما هي:** الكلمات تبدأ من حالة جزئية — شفافية 40%، أسفل قليلًا، ضبابية — ثم تستقر بسرعة؛ أنعم من القناع. / Words start partial — 40% opacity, slightly low, blurred — and settle fast; softer than a mask.

**متى:** حين تريد دخول كلمات ناعما من ضبابية خفيفة بدل قناع حاد / when words should settle in softly from a slight blur and offset rather than a hard mask

**كيف:** MOTION.riseWords(tl, el, at, {rise:26, blur:6, dur:.4, stagger:.1}) with E.out; projects use 30–40 px / 0.55–0.6 s / stagger 0.1–0.12 (water labels 0.8 s, stagger 0.05, power4.out). Infographic line variant: overflow:hidden container, inner translateY 70%→0 + blur 6→0 px, 450 ms, 80 ms per line, fast-in slow-out, small grey eyebrow above a bold white headline. Rounded-face brief: 24→0 px in 240 ms, 60 ms stagger at 72 px.

**المعاملات:** y 26→0 px; opacity .4→1; blur 6→0; 0.4 s; stagger 0.1 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صعود · ضبابية · riseWords · blur · rise · soft reveal · eyebrow · دخول ناعم · بلور · ظهور هادئ · blur in · fade up

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:175`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:70`
- `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:174-182`
- `style:infographic`

#### 7. قدرات قريبة في العائلة

- `ARAB-18` قواعد التايبوغرافي العربي الحركي / Kinetic Arabic grammar (ready)
- `ARAB-19` أقنعة الكلمات: إظهار وإخفاء / Word-mask reveal & hide (proven)
- `ARAB-21` مسح القناع من اليمين / RTL clip wipe (documented)
- `ARAB-22` كتابة بقناع ناعم ورأس قلم / Feathered RTL write-on with pen head (install)

### `ARAB-21` — مسح القناع من اليمين / RTL clip wipe

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الكلمة مكتملة التشكيل تنكشف من اليمين إلى اليسار بقصّ clip-path — كتابة بلا كسر للحروف. / A fully shaped word is uncovered right-to-left by a clip-path — writing without breaking letters.

**متى:** حين تريد كتابة كلمة عربية من اليمين إلى اليسار دون كسر الحروف / when an Arabic word should appear written right-to-left without breaking its letters

**كيف:** clip-path inset(0 0 0 100%) → inset(0 0 0 0) in 350–600 ms ease-out quart (recipe B: 500 ms); big-word recipe: a 200 px word wiped in over 450 ms, held 1 s, wiped out the same direction in 250 ms; Canvas: draw the word offscreen and grow a ctx.rect clip from the right; long words from words.json may fill right→left across their spoken duration. (code snippet in references/powers/typography-arabic.md)

**المعاملات:** 350–600 ms; ease-out quart cubic-bezier(.25,1,.5,1)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مسح · قناع · من اليمين · clip-path · wipe · rtl reveal · handwriting · كتابة الكلمة · كشف تدريجي · ظهور من اليمين · write on · reveal

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/playbooks/arabic-typography.md:26`
- `kosif-tool/playbooks/kinetic-type.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`
- `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-19` أقنعة الكلمات: إظهار وإخفاء / Word-mask reveal & hide (proven)
- `ARAB-20` صعود الكلمات من الضباب / Rise-from-blur words (ready)
- `ARAB-22` كتابة بقناع ناعم ورأس قلم / Feathered RTL write-on with pen head (install)
- `ARAB-23` قناع ضربة فرشاة / Brush-stroke mask write-on (documented)

### `ARAB-22` — كتابة بقناع ناعم ورأس قلم / Feathered RTL write-on with pen head

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الكلمة تظهر من اليمين بحافة ناعمة، وقلم أو ماركر يتبع الحافة كأنه يكتبها بيده. / A word appears from the right behind a soft edge while a pen or marker rides the edge as if writing it.

**متى:** حين تريد أن تبدو الكلمة مكتوبة بخط اليد وقلم يتبعها كفيديو السبورة / when a word should look handwritten with a pen riding the edge, whiteboard style

**كيف:** Basma TX.reveal(c, x0, x1, y0, y1, k, rtl, paint): clip up to the edge, then 6 thin slices with falling alpha form a feather of max(6 px, 8% width); it returns the edge x for the pen sprite. HTML (whiteboard reference): keep the text as HTML, mask-image linear-gradient(to left, #000 X%, transparent X+4%), X 0→100 over ~0.6 s per word, marker tip on the mask edge, 2° wiggle for 150 ms when a word completes. Chalk variant: chalk sprite takes the stroke colour, dust particles spawn at the last ~14 tip positions and fade in ~0.5 s. (code snippet in references/powers/typography-arabic.md)

**المعاملات:** feather max(6 px, 8%); 6 slices; ~0.6 s per word; wiggle 2° / 150 ms

**التثبيت:** cd app && npm install

**الوسوم:** كتابة يدوية · قلم · ماركر · سبورة · write-on · handwriting · pen · marker · whiteboard · feather mask · خط اليد · كتابة بالقلم · حافة ناعمة · pen reveal · soft edge

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `app/public/js/10_studio.js:194`
- `kosif-tool/playbooks/hand-drawn.md:75`
- `kosif-tool/styles/handwriting-reveal/SKILL.md`
- `style:whiteboard`

#### 7. قدرات قريبة في العائلة

- `ARAB-20` صعود الكلمات من الضباب / Rise-from-blur words (ready)
- `ARAB-21` مسح القناع من اليمين / RTL clip wipe (documented)
- `ARAB-23` قناع ضربة فرشاة / Brush-stroke mask write-on (documented)
- `ARAB-24` سطور تصعد من خلف خط قطع / Lines rising behind a cut line (proven)

### `ARAB-23` — قناع ضربة فرشاة / Brush-stroke mask write-on

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ضربة فرشاة SVG تُرسم وتعمل قناعًا يكشف عبارة مكتملة من اليمين إلى اليسار. / An SVG brush stroke draws on and acts as a mask that uncovers a finished phrase right-to-left.

**متى:** حين تريد كشف عبارة عربية بضربة فرشاة ترسم من اليمين / when a finished Arabic phrase should be uncovered by a brush stroke drawn right-to-left

**كيف:** SVG <mask> holding a thick round-cap brush path (pathLength=1, stroke-dasharray 1, stroke-dashoffset 1→0) drawn from right to left over the intact text; 0–0.5 s start, 0.5–2.5 s reveal, 2.5–4 s read.

**المعاملات:** 4 s total; reveal 2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** فرشاة · قناع · brush · mask · stroke-dashoffset · svg · calligraphy · ضربة فرشاة · رسم الخط · كشف العبارة · brush reveal · draw on

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`
- `kosif-tool/playbooks/hand-drawn.md:75`

#### 7. قدرات قريبة في العائلة

- `ARAB-21` مسح القناع من اليمين / RTL clip wipe (documented)
- `ARAB-22` كتابة بقناع ناعم ورأس قلم / Feathered RTL write-on with pen head (install)
- `ARAB-24` سطور تصعد من خلف خط قطع / Lines rising behind a cut line (proven)
- `ARAB-25` انزلاق سطور عربية على Canvas / Canvas RTL staggered line slide (ready)

### `ARAB-24` — سطور تصعد من خلف خط قطع / Lines rising behind a cut line

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT). |

**ما هي:** كل سطر من عنوان ثلاثي يصعد من خلف خط قطع غير مرئي بتأخير محسوب. / Each line of a three-line title rises from behind an invisible cut line with a measured delay.

**متى:** حين تريد عنوانا من عدة أسطر أو اقتباسا تصعد سطوره واحدا بعد الآخر / when a multi-line title or quote card should rise line by line from behind a cut

**كيف:** One overflow:hidden wrapper per line, inner translateY 100%→0; reveal 0–1.2 s, read 1.2–2.6 s, out 2.6–3 s. quote-card template: quote mark springs in, lines split by '\|' (≤6) rise .22 s apart, accent bar, author rises last. Give the wrapper extra line-height so dots are not clipped (ARAB-05).

**المعاملات:** 3 s cycle; line stagger .22 s; quote 6.4u

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سطور · اقتباس · line reveal · quote · mask rise · MG-012 · بطاقة اقتباس · عنوان متعدد الأسطر · صعود السطور · quote card · multi-line title

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/templates/motion/quote-card.html`
- `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:45`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-22` كتابة بقناع ناعم ورأس قلم / Feathered RTL write-on with pen head (install)
- `ARAB-23` قناع ضربة فرشاة / Brush-stroke mask write-on (documented)
- `ARAB-25` انزلاق سطور عربية على Canvas / Canvas RTL staggered line slide (ready)
- `ARAB-26` عنوان كلمات بنابض كل 160 مللي ثانية / Spring word-stagger title (proven)

### `ARAB-25` — انزلاق سطور عربية على Canvas / Canvas RTL staggered line slide

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نص المشهد يُلفّ إلى ≤4 أسطر عربية تنزلق من اليمين وتظهر تباعًا — بلا أي مكتبة. / Scene text wraps to ≤4 Arabic lines that slide in from the right one after another — no library.

**متى:** حين ترسم نص المشهد العربي على Canvas وتريد أسطره تنزلق من اليمين تباعا بلا مكتبة / for sliding wrapped Arabic lines in from the right on a Canvas without a library

**كيف:** splitArabic(text, maxChars) greedy by whole words (16 chars vertical / 26 horizontal, default 18), slice(0,4); ctx.direction='rtl'; font '700 {w·.074 \| w·.051}px …'; centre y = 0.68h; line height 1.25em; per line a = clamp(4p − 0.18k), x offset (1 − easeOutCubic(a))·0.4w; maxWidth 0.9w; shadow #0b1228 blur 0.03w. The source uses Tahoma — swap in Cairo after the font gate.

**المعاملات:** ≤4 lines; stagger 0.18 of progress; slide 40% width

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** canvas · انزلاق · slide in · line wrap · تقسيم الأسطر · stagger · أسطر متتالية · لف النص · دخول من اليمين · rtl canvas · no library

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `fastify-motion-bro/web/motion.js:3`

#### 7. قدرات قريبة في العائلة

- `ARAB-23` قناع ضربة فرشاة / Brush-stroke mask write-on (documented)
- `ARAB-24` سطور تصعد من خلف خط قطع / Lines rising behind a cut line (proven)
- `ARAB-26` عنوان كلمات بنابض كل 160 مللي ثانية / Spring word-stagger title (proven)
- `ARAB-27` عنوان Remotion بنابض وأقراص كلمات / Remotion spring title + keyword pills (install)

### `ARAB-26` — عنوان كلمات بنابض كل 160 مللي ثانية / Spring word-stagger title

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عنوان عربي من كلمات كاملة تصعد 70 بكسل وتكبر 0.92→1 بنابض، كلمة كل 160 ms، ثم تخرج معًا. / Whole Arabic words rise 70 px and scale 0.92→1 on a spring, 160 ms apart, then exit together.

**متى:** حين تريد عنوانا افتتاحيا تقفز كلماته العربية بنابض واحدة تلو الأخرى ثم تخرج معا / when an opening title's Arabic words should spring in one after another, then exit together

**كيف:** Per word a = 0.25 + 0.16·i s; prog(t, a, a + 0.55, spring 170/16); exit prog(t, 3.0, 3.35, inBack) translateY −60; Cairo 900 128 px, lh 1.25, gap 28 px, accent word #7ee8d2. Playbook twin (Remotion ArabicTitle): p = (frame − 4i)/12 → translateY (1 − p)·50; recipe A: rise 50 px over 400 ms ease-out quint, 120 ms stagger, key word 700–980 ms → accent + scale 1.08 spring 12/180; Cairo 900 140 px lh 1.3.

**المعاملات:** stagger 160 ms; spring 170/16; exit 3.0–3.35 s inBack

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نابض · spring · word stagger · title · عنوان · html-canvas · starter · عنوان متحرك · قفز الكلمات · ارتداد · bouncy title · word pop

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/starters/html-canvas/index.html:139`
- `kosif-tool/playbooks/arabic-typography.md:35-63`

#### 7. قدرات قريبة في العائلة

- `ARAB-24` سطور تصعد من خلف خط قطع / Lines rising behind a cut line (proven)
- `ARAB-25` انزلاق سطور عربية على Canvas / Canvas RTL staggered line slide (ready)
- `ARAB-27` عنوان Remotion بنابض وأقراص كلمات / Remotion spring title + keyword pills (install)
- `ARAB-28` دخول الكلمة من العمق / 3D word turn-in from depth (ready)

### `ARAB-27` — عنوان Remotion بنابض وأقراص كلمات / Remotion spring title + keyword pills

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | Remotion: مجاني للأفراد والشركات الصغيرة، والشركات الأكبر تحتاج رخصة شركة / free for individuals and small companies; larger companies need a Remotion company license (pinned 4.0.535). |

**ما هي:** خط لوني ينمو إلى 180 بكسل، ثم كلمات العنوان تقفز كل 5 إطارات، ثم أقراص الكلمات المفتاحية كل 4 إطارات. / An accent rule grows to 180 px, title words spring in every 5 frames, keyword pills every 4.

**متى:** حين تبني في Remotion عنوانا بنابض تتبعه شارات الكلمات المفتاحية / when building a Remotion spring title followed by keyword pills

**كيف:** Title: spring damping 14, stiffness 120, mass .9, rise 80 px, scale .85→1, staggerStart(i, 5, 6); pills: damping 12, stiffness 150; title 112 px 800 lh 1.3 #f4f1ea; pills 40 px 600, padding 12×30, radius 999, border 3 px accent@.9, bg accent@.14; chart/axis numbers via Intl.NumberFormat(lang === 'ar' ? 'ar-EG' : 'en-US').

**المعاملات:** title every 5 frames; pills every 4 frames

**التثبيت:** cd kosif-tool/starters/remotion && npm ci

**الوسوم:** remotion · spring · pills · أقراص · keyword · react · عنوان ريموشن · كلمات مفتاحية · شارات · keyword tags · title animation

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/starters/remotion/src/Film.tsx:130`
- `kosif-tool/starters/remotion/src/Film.tsx:303`

#### 7. قدرات قريبة في العائلة

- `ARAB-25` انزلاق سطور عربية على Canvas / Canvas RTL staggered line slide (ready)
- `ARAB-26` عنوان كلمات بنابض كل 160 مللي ثانية / Spring word-stagger title (proven)
- `ARAB-28` دخول الكلمة من العمق / 3D word turn-in from depth (ready)
- `ARAB-29` الآلة الكاتبة بمؤشر / Typewriter with caret (ready)

### `ARAB-28` — دخول الكلمة من العمق / 3D word turn-in from depth

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT). |

**ما هي:** كل كلمة تنقلب واقفة من العمق (rotationX) مع انقشاع الضباب وظل ناعم. / Each word tips up from depth (rotationX) as blur clears, with a soft shadow.

**متى:** حين تريد كلمات تنقلب واقفة من العمق بمنظور ثلاثي الأبعاد مع انقشاع ضبابية / when words should tip up from depth in 3D perspective as blur clears

**كيف:** GSAP from y 46k, z −220, rotationX −78, transformPerspective 900, transformOrigin 50% 100%, blur 10 px → 0; 0.62 s back.out(1.4) starting 0.1 s before the word's time; drop-shadow 0 5px 12px rgba(0,0,0,.65). The whole word turns, so shaping is never at risk. Render: node kosif-tool/tools/render_html.cjs --in index.html --out x.mp4 --mode virtual.

**المعاملات:** rotationX −78°; z −220; perspective 900; 0.62 s back.out(1.4)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عمق · ثلاثي · 3d word · rotationX · perspective · verse · turn-in · انقلاب الكلمة · دخول من العمق · منظور · flip in · depth reveal

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/templates/verse.html:222`

#### 7. قدرات قريبة في العائلة

- `ARAB-26` عنوان كلمات بنابض كل 160 مللي ثانية / Spring word-stagger title (proven)
- `ARAB-27` عنوان Remotion بنابض وأقراص كلمات / Remotion spring title + keyword pills (install)
- `ARAB-29` الآلة الكاتبة بمؤشر / Typewriter with caret (ready)
- `ARAB-30` كلمة ضخمة من الضباب تنكمش إلى سطر / Blur-in hero word that shrinks into the sentence (seen)

### `ARAB-29` — الآلة الكاتبة بمؤشر / Typewriter with caret

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT). |

**ما هي:** النص يُكتب بامتداد السلسلة نفسها فيعيد المتصفح تشكيل البادئة كل إطار، تمامًا كالكتابة على لوحة المفاتيح. / Text grows as a string so the browser reshapes the prefix each frame — exactly like keyboard typing.

**متى:** حين تريد نصا عربيا يكتب حرفا بحرف كالكتابة على الكيبورد مع مؤشر وامض / when Arabic text should type on like keyboard input with a blinking caret

**كيف:** MOTION.typeOn(tl, el, text, at, {cps:46, caret:true, hold:1}): dur = clamp(len/cps, 0.5, 1.2) s, writes text.slice(0, n) + '\|', caret blinks at 2 Hz while held; projects use cps 22–46, hold 0.5–0.6 s. Arabic-safe because it never wraps letters in spans; the last letter shows its final form until the next arrives. For tashkeel-heavy text step by grapheme (Intl.Segmenter) so a harakah never appears alone.

**المعاملات:** cps 22–46; dur 0.5–1.2 s; caret 2 Hz

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** آلة كاتبة · مؤشر · typewriter · typeOn · caret · prompt box · كتابة تلقائية · كيبورد · مؤشر وامض · typing effect · typing animation

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:193`
- `kosif-studio/motion/projects/showreel/index.html:74`

#### 7. قدرات قريبة في العائلة

- `ARAB-27` عنوان Remotion بنابض وأقراص كلمات / Remotion spring title + keyword pills (install)
- `ARAB-28` دخول الكلمة من العمق / 3D word turn-in from depth (ready)
- `ARAB-30` كلمة ضخمة من الضباب تنكمش إلى سطر / Blur-in hero word that shrinks into the sentence (seen)
- `ARAB-31` كبسولة الكلمات الدوّارة / Rolling word pill with growing rings (seen)

### `ARAB-30` — كلمة ضخمة من الضباب تنكمش إلى سطر / Blur-in hero word that shrinks into the sentence

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الكلمة الأولى تدخل ضخمة من ضبابية ثم يصغر حجمها لتصير أول جملة تتوالى كلماتها. / The first word lands huge out of blur, then shrinks to become the start of a sentence whose words follow.

**متى:** حين تبدأ الجملة بكلمة ضخمة تدخل من ضبابية ثم تصغر لتتبعها بقية الكلمات / when a sentence opens with one huge blurred-in word that shrinks into the line

**كيف:** Build: word1 opacity 0→1, blur 20→0 px, scale 1.1→1 in 0.5 s; then animate font-size ~22% → ~7% of frame height over 0.6 s ease-in-out (font-size re-shapes cleanly; never scaleX) while words 2..n enter 180 ms apart with cubic-bezier(.22,1,.36,1); exit = blur + translateX 40 px toward the line end.

**المعاملات:** blur 20 px; stagger 180 ms; size 22%→7% H

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كلمة بطلة · ضباب · hero word · blur in · shrink · launch · كلمة كبيرة · افتتاحية · تصغير الكلمة · big word · sentence build

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `style:product`
- `kosif-tool/styles/product`

#### 7. قدرات قريبة في العائلة

- `ARAB-28` دخول الكلمة من العمق / 3D word turn-in from depth (ready)
- `ARAB-29` الآلة الكاتبة بمؤشر / Typewriter with caret (ready)
- `ARAB-31` كبسولة الكلمات الدوّارة / Rolling word pill with growing rings (seen)
- `ARAB-32` كشف بالحبر وسحب التركيز / Ink-bleed / focus-pull word reveal (seen)

### `ARAB-31` — كبسولة الكلمات الدوّارة / Rolling word pill with growing rings

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كبسولة تتدحرج فيها الكلمات عموديًا (أيام ← ساعات ← دقائق) وحلقات خلفها تكبر مع كل خطوة. / Words roll vertically inside a pill (days → hours → minutes) while rings behind it grow each step.

**متى:** حين تريد تبديل كلمات داخل كبسولة بالتدحرج العمودي مثل أيام ثم ساعات ثم دقائق / when swapping words inside a pill by vertical roll, e.g. days to hours to minutes

**كيف:** Build: pill overflow:hidden; stacked words translateY −100% per step, ease-out 0.4 s; concentric pill outlines behind grow +40 px per step (3 steps), soft purple shadow.

**المعاملات:** 3 steps; +40 px per ring; 0.4 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كبسولة · تدحرج · word roll · pill · rings · ticker · تبديل الكلمات · كلمات دوارة · حلقات · rolling text · word swap

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `style:product`

#### 7. قدرات قريبة في العائلة

- `ARAB-29` الآلة الكاتبة بمؤشر / Typewriter with caret (ready)
- `ARAB-30` كلمة ضخمة من الضباب تنكمش إلى سطر / Blur-in hero word that shrinks into the sentence (seen)
- `ARAB-32` كشف بالحبر وسحب التركيز / Ink-bleed / focus-pull word reveal (seen)
- `ARAB-33` كلمات على مسار دائري / Words on a circular path (documented)

### `ARAB-32` — كشف بالحبر وسحب التركيز / Ink-bleed / focus-pull word reveal

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل كلمة تتجسد من ضبابية خفيفة كأن الحبر يتشربها، والكلمة السابقة ما زالت تنقشع. / Each word condenses from a light blur like ink bleeding in while the previous one is still clearing.

**متى:** حين تريد ظهور كلمات القصيدة أو الأغنية كالحبر يتشربها مع الصوت / when poem or lyric words should condense in like ink, synced to vocal onsets

**كيف:** Per word: opacity 0→1 + blur 4 px→0 + scale 0.96→1 in 200–300 ms with 80% overlap to the next; on vocal onset (words.json) the incoming word sharpens while the trailing one is still soft; colour adapts to background brightness (dark ink on bright sky, white on dark). Seen per character (CJK) and per word (Latin lyric); for Arabic it is per word only.

**المعاملات:** 200–300 ms per unit; 80% overlap; blur 4 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حبر · تركيز · ink bleed · focus pull · lyric · poem · blur · كلمات أغنية · قصيدة · ظهور ناعم · vocal sync · soft reveal

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `style:pm-demitiyageekzen-7770ad`
- `style:pm-samaote-5e2fc2`
- `kosif-tool/styles/pm-samaote-5e2fc2/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-30` كلمة ضخمة من الضباب تنكمش إلى سطر / Blur-in hero word that shrinks into the sentence (seen)
- `ARAB-31` كبسولة الكلمات الدوّارة / Rolling word pill with growing rings (seen)
- `ARAB-33` كلمات على مسار دائري / Words on a circular path (documented)
- `ARAB-34` ضربة الكلمة المفتاحية بقناع صاعد / Keyword slam with upward mask (ready)

### `ARAB-33` — كلمات على مسار دائري / Words on a circular path

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عبارة تدور ببطء حول منتج أو شمس ثم تتوقف والجزء المقروء في الأعلى. / A phrase circles a product or sun slowly and stops with the readable part on top.

**متى:** حين تريد عبارة تدور ببطء حول منتج أو شمس ثم تتوقف مقروءة / when a phrase should orbit a product or sun slowly and stop readable on top

**كيف:** 0–1 s appear, 1–3.5 s rotate, 3.5–5 s stop; place whole Arabic words by angle (each word its own rotated element) instead of per-glyph textPath; keep the rotation slow. Reference: words placed along an arc around the sun in a synced Latin lyric film.

**المعاملات:** 5 s loop

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مسار دائري · circle · textPath · arc · orbit · MG-017 · نص دائري · دوران النص · حول المنتج · circular text · rotating text

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-31` كبسولة الكلمات الدوّارة / Rolling word pill with growing rings (seen)
- `ARAB-32` كشف بالحبر وسحب التركيز / Ink-bleed / focus-pull word reveal (seen)
- `ARAB-34` ضربة الكلمة المفتاحية بقناع صاعد / Keyword slam with upward mask (ready)
- `ARAB-35` كلمة ترتطم وتستقر / Slam-and-settle word (documented)

### `ARAB-34` — ضربة الكلمة المفتاحية بقناع صاعد / Keyword slam with upward mask

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT). |

**ما هي:** الكلمة المنبورة تهبط بثقل: أصغر قليلًا، منخفضة، ضبابية، يكشفها قناع ينفتح للأعلى فتستقر حادة في ثلث ثانية. / The stressed word lands with weight: slightly small, low and blurred, uncovered by an upward-opening mask, sharp in a third of a second.

**متى:** حين تريد أن تهبط الكلمة المنبورة بثقل وتستقر حادة في ثلث ثانية / when a stressed keyword should land with weight and lock sharp in about a third of a second

**كيف:** slam(el, at, {from, y, blur, dur, ease, tail}): fromTo {opacity 0, scale .94, y 24·k, filter blur(10px), clipPath inset(100% −10% −45% −10%)} → {opacity 1, scale 1, y 0, blur 0, clipPath inset(−25% −10% −45% −10%)} in 0.34–0.36 s expo.out; keyword size 200·k, weight 700. Variants: from 1.12 / blur 14 / 0.18 s for a sharp 'إطلاقاً', blur 16 / 0.24 s for 'في الفعل'. Pick the word with ARAB-68.

**المعاملات:** scale .94→1; y 24k; blur 10→0; 0.34 s expo.out

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ضربة · كلمة مفتاحية · slam · keyword · emphasis · expo.out · clip mask · تأكيد الكلمة · إبراز · كلمة قوية · word punch · impact text

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-studio/motion/templates/directed.html`
- `100-superskills/skills/kosif-montage-motion/templates/directed.html:82`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:182`

#### 7. قدرات قريبة في العائلة

- `ARAB-32` كشف بالحبر وسحب التركيز / Ink-bleed / focus-pull word reveal (seen)
- `ARAB-33` كلمات على مسار دائري / Words on a circular path (documented)
- `ARAB-35` كلمة ترتطم وتستقر / Slam-and-settle word (documented)
- `ARAB-36` ضربة الكلمة البطلة بتوهج / Hero-word punch with bloom (seen)

### `ARAB-35` — كلمة ترتطم وتستقر / Slam-and-settle word

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الكلمة تسقط أبعد قليلًا من مكانها، ترتد مرة واحدة ثم تثبت — افتتاح إعلاني بثقل. / The word drops slightly past its slot, rebounds once and locks — a weighty ad opener.

**متى:** حين تحتاج افتتاحية إعلان بكلمة تسقط وترتد مرة ثم تثبت / for an ad opener where a word drops past its slot, rebounds once and locks

**كيف:** 0–0.4 s drop past the slot, 0.4–0.8 s one rebound (back.out(1.6) or cubic-bezier(.34,1.56,.64,1)), 0.8–2 s read; animate the word block (translateY + scale), never letters; one muted thud SFX on contact.

**المعاملات:** 2 s; overshoot back.out 1.6

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ارتطام · ارتداد · slam · settle · overshoot · MG-011 · افتتاحية إعلان · سقوط الكلمة · إعلان · ad opener · drop in

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-33` كلمات على مسار دائري / Words on a circular path (documented)
- `ARAB-34` ضربة الكلمة المفتاحية بقناع صاعد / Keyword slam with upward mask (ready)
- `ARAB-36` ضربة الكلمة البطلة بتوهج / Hero-word punch with bloom (seen)
- `ARAB-37` الكلمة تمثّل معناها / Word acts out its meaning (documented)

### `ARAB-36` — ضربة الكلمة البطلة بتوهج / Hero-word punch with bloom

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كلمة عربية ثقيلة بحجم 40% من ارتفاع الإطار تضرب للداخل من تكبير وضباب مع هالة متوهجة. / A heavy Arabic word at ~40% of frame height punches in from scale and blur with a glowing halo.

**متى:** حين تريد كلمة عربية ضخمة تضرب للداخل بتوهج في ذروة الفيديو / when a huge Arabic word should punch in with a glowing halo at the video's climax

**كيف:** Build: weight 900, ~40% of frame height; scale 1.15→1 and blur 8→0 px in 300 ms; glow = a duplicate of the word blurred 20 px at 40% opacity (white or orange #f27525) behind it. Climax variant: a giant glyph/word with a fire-texture glow, fade in 300 ms, hold 1 s.

**المعاملات:** 300 ms; glow copy blur 20 px @40%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كلمة بطلة · توهج · hero word · punch · bloom · glow · climax · ذروة · كلمة ضخمة · هالة · big word · impact

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `style:plotter`
- `style:pm-chrisjdimarco-f068db`

#### 7. قدرات قريبة في العائلة

- `ARAB-34` ضربة الكلمة المفتاحية بقناع صاعد / Keyword slam with upward mask (ready)
- `ARAB-35` كلمة ترتطم وتستقر / Slam-and-settle word (documented)
- `ARAB-37` الكلمة تمثّل معناها / Word acts out its meaning (documented)
- `ARAB-38` صدى طباعي يتلاشى / Typographic echo (documented)

### `ARAB-37` — الكلمة تمثّل معناها / Word acts out its meaning

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كلمة واحدة تؤدي معناها — «توسّع» تتسع، «سقوط» تسقط — والجملة ثابتة حولها. / One word performs its meaning — 'expansion' widens, 'fall' drops — while the sentence holds still.

**متى:** حين تريد كلمة واحدة تؤدي معناها حركيا كأن تتسع أو تسقط والجملة ثابتة / when one word should act out its meaning, widening or falling, while the sentence holds

**كيف:** MG-014: 0–0.6 s sentence, 0.6–1.5 s the word acts, 1.5–3 s read. Widen with uniform scale of the whole block or kashida/wdth, never scaleX; drop, shake or blur the word block. The reference showreel used squash/stretch, overshoot springs, motion blur and chromatic split on Latin words — for Arabic apply them to the whole word only.

**المعاملات:** 3 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** معنى الكلمة · word acts · squash · stretch · MG-014 · expressive type · حركة تعبيرية · كلمة تعبر · تايبوغرافي تعبيري · meaning animation · word motion

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-35` كلمة ترتطم وتستقر / Slam-and-settle word (documented)
- `ARAB-36` ضربة الكلمة البطلة بتوهج / Hero-word punch with bloom (seen)
- `ARAB-38` صدى طباعي يتلاشى / Typographic echo (documented)
- `ARAB-39` تعبئات مذهّبة ومتدرجة ولمعة عابرة / Gilded, gradient & sweeping fills (ready)

### `ARAB-38` — صدى طباعي يتلاشى / Typographic echo

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاث نسخ متأخرة تلاحق الكلمة ثم تلتقي عليها وتختفي، فتمنح العنوان طاقة. / Three delayed copies trail a word, converge on it and vanish, energising the headline.

**متى:** حين تريد إعطاء العنوان طاقة بنسخ متأخرة تلاحق الكلمة ثم تلتقي عليها / when energising a headline with delayed copies that trail a word and converge on it

**كيف:** 3–5 clones with delayed transforms and opacity 0.6→0.1; 0–0.7 s push, 0.7–1.2 s copies converge on the master, 1.2–2.5 s read; the master stays crisp and high-contrast; short tail-pulse SFX.

**المعاملات:** 2.5 s; 3 echoes; opacity 0.6→0.1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صدى · نسخ · echo · trail · clones · MG-018 · أثر الحركة · تكرار الكلمة · نسخ متتابعة · ghost copies · motion trail

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-36` ضربة الكلمة البطلة بتوهج / Hero-word punch with bloom (seen)
- `ARAB-37` الكلمة تمثّل معناها / Word acts out its meaning (documented)
- `ARAB-39` تعبئات مذهّبة ومتدرجة ولمعة عابرة / Gilded, gradient & sweeping fills (ready)
- `ARAB-40` هرمية بثلاث مستويات / Three-level type hierarchy (ready)

### `ARAB-39` — تعبئات مذهّبة ومتدرجة ولمعة عابرة / Gilded, gradient & sweeping fills

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** التدرج يملأ الحروف (background-clip:text) على الكلمة المشكّلة كاملة — ذهبي للفخامة، سماوي للتقني، ولمعة تمر على كلمة الذروة. / Gradients fill the glyphs of the whole shaped word — gold for luxury, sky for tech, a light sweep across the payoff word.

**متى:** حين تريد كلمة عربية بتعبئة ذهبية أو متدرجة أو لمعة تمر على كلمة الذروة / when an Arabic word needs a gold or gradient fill or a light sweep across the payoff word

**كيف:** -webkit-background-clip:text + -webkit-text-fill-color:transparent on the word element (table). Light sweep: background-size 300% and animate background-position across the payoff word once.

**المعاملات:** see table

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ذهبي · تدرج · لمعة · gold · gradient text · background-clip · sweep · luxury · فخم · نص ذهبي · تدرج لوني · بريق · shine · golden text

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:51`
- `100-superskills/skills/kosif-montage-motion/templates/verse.html:37`
- `kosif-one/projects/egypt-2120-animation/index.html:8-29`
- `kosif-studio/motion/projects/premium_edit/index.html:8`

#### 7. قدرات قريبة في العائلة

- `ARAB-37` الكلمة تمثّل معناها / Word acts out its meaning (documented)
- `ARAB-38` صدى طباعي يتلاشى / Typographic echo (documented)
- `ARAB-40` هرمية بثلاث مستويات / Three-level type hierarchy (ready)
- `ARAB-41` تمييز الكلمة بالنجمة / *Asterisk* emphasis convention (ready)

### `ARAB-40` — هرمية بثلاث مستويات / Three-level type hierarchy

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | المشروع الأصلي يستخدم Dubai (مملوك) — استبدله بـ Cairo/Tajawal عند الشحن؛ GSAP مدمج / original uses proprietary Dubai — swap to Cairo/Tajawal for shipping; GSAP vendored (standard no-charge license). |

**ما هي:** الكلام صغير، العبارة متوسطة، الكلمة المفتاحية ضخمة — فتعرف العين ماذا تقرأ أولًا. / Speech small, phrase medium, keyword huge — the eye knows what to read first.

**متى:** حين تحتاج ترتيب أحجام الكلام والعبارة والكلمة المفتاحية حتى تعرف العين ماذا تقرأ أولا / when sizing speech, phrase and keyword so the eye knows what to read first

**كيف:** Premium edit (1080×1920, one family 300/500/700): .l1 speech 54 px/500 at y 1452; .l2 phrase 96/700 at 1236; .l3 keyword 220/700 at 1196; an extreme word at 400 px doubles as a transition plane; payoff 250 px; soft 300-weight line at 150 px; credit 25 px/300 at 48% alpha; ivory text with double shadow 0 3px 16px .45 + 0 1px 2px .35; words land on their syllables. Explainer variant: captions 50 px at y 1400, keywords 48–150 px in the upper half (y 330–1220), section chips 40 px (ARAB-54).

**المعاملات:** 54 / 96 / 220 px (+400 plane)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هرمية · مستويات · hierarchy · caption · keyword · premium edit · reels · أحجام النص · تدرج الأحجام · ترتيب بصري · type hierarchy · text sizes

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-studio/motion/projects/premium_edit/index.html:8`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:24`
- `kosif-one/projects/whatsapp-motion/projects/success/index.html:28-40`
- `kosif-studio/out/FINAL_EDIT/EDIT_NOTES.txt`

#### 7. قدرات قريبة في العائلة

- `ARAB-38` صدى طباعي يتلاشى / Typographic echo (documented)
- `ARAB-39` تعبئات مذهّبة ومتدرجة ولمعة عابرة / Gilded, gradient & sweeping fills (ready)
- `ARAB-41` تمييز الكلمة بالنجمة / *Asterisk* emphasis convention (ready)
- `ARAB-42` خط متموّج تحت الكلمة المفتاحية / Squiggle underline highlight (seen)

### `ARAB-41` — تمييز الكلمة بالنجمة / *Asterisk* emphasis convention

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** المستخدم أو Claude يضع *نجمتين* حول كلمة واحدة في السطر، وكل ترجمة وستايل يقرأها فيلوّنها أو يضيئها. / The user or Claude wraps one word per line in *asterisks*; every caption and style reads it to colour or glow that word.

**متى:** حين تريد تحديد كلمة في السكربت ليلونها أو يبرزها كل ستايل وترجمة / when marking one word per script line so every caption and style colours or glows it

**كيف:** MK.mkLine/parseScript split lines, strip [brackets] and '...', keep {w, em}; drawCaptions/capWords render a *word* in the accent colour at 1.1× scale; one starred word per line.

**المعاملات:** 1 starred word per line; accent + 1.1× scale

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نجمة · تمييز · asterisk · emphasis · script markup · accent · تلوين كلمة · إبراز كلمة · السكربت · highlight word · markup

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `app/public/js/10_studio.js:44`
- `app/public/js/10_studio.js:57`
- `app/public/js/00_editor.js:345`

#### 7. قدرات قريبة في العائلة

- `ARAB-39` تعبئات مذهّبة ومتدرجة ولمعة عابرة / Gilded, gradient & sweeping fills (ready)
- `ARAB-40` هرمية بثلاث مستويات / Three-level type hierarchy (ready)
- `ARAB-42` خط متموّج تحت الكلمة المفتاحية / Squiggle underline highlight (seen)
- `ARAB-43` ممسحة التظليل من اليمين / RTL highlighter swipe (seen)

### `ARAB-42` — خط متموّج تحت الكلمة المفتاحية / Squiggle underline highlight

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الكلمة المفتاحية تتلون برتقاليًا بتوهج دافئ، وتحتها خط موجي مرسوم باليد يتماوج ببطء. / The keyword turns orange with a warm glow over a hand-drawn sine underline that slowly phase-shifts.

**متى:** حين تريد إبراز كلمة مفتاحية بلون برتقالي وخط موجي مرسوم باليد تحتها / when highlighting a keyword in orange with a hand-drawn wavy underline beneath it

**كيف:** Build: key word #f07f2e, glow #ffd0a0 blur 12 px; SVG sine underline amplitude 3 px, period 18 px, drawn right→left under the Arabic word, phase shifted slowly (rebuild d per frame).

**المعاملات:** #f07f2e; glow #ffd0a0 12 px; amp 3 px; period 18 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خط متموج · دودل · squiggle · underline · doodle · highlight · خط تحت الكلمة · تسطير · خط موجي · wavy line · hand drawn

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `style:doodle`
- `kosif-tool/styles/doodle`

#### 7. قدرات قريبة في العائلة

- `ARAB-40` هرمية بثلاث مستويات / Three-level type hierarchy (ready)
- `ARAB-41` تمييز الكلمة بالنجمة / *Asterisk* emphasis convention (ready)
- `ARAB-43` ممسحة التظليل من اليمين / RTL highlighter swipe (seen)
- `ARAB-44` ختم أحمر يرتطم / Rubber-stamp slam (seen)

### `ARAB-43` — ممسحة التظليل من اليمين / RTL highlighter swipe

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مستطيل أصفر مستدير يتمدد خلف الكلمة المفتاحية من اليمين إلى اليسار كقلم تظليل. / A rounded yellow bar grows behind the keyword from the right like a highlighter.

**متى:** حين تريد تظليل كلمة مفتاحية بمستطيل أصفر يتمدد من اليمين كقلم التحديد / when a yellow highlighter bar should grow behind a keyword from the right

**كيف:** Build: rounded rect behind the key word, #f2c94c at 70%, height 35% of the text, width 0→100% with transform-origin right under a bold title. Slanted variant: a skewed teal bar wipes in behind the key line while earlier lines dim (ARAB-48).

**المعاملات:** #f2c94c @70%; height 35%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تظليل · هايلايتر · highlighter · swipe · marker · rtl · قلم تحديد · تحديد الكلمة · خلفية الكلمة · highlight bar · text highlight

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `style:stickman`
- `style:pm-deifosv-04e4d3`

#### 7. قدرات قريبة في العائلة

- `ARAB-41` تمييز الكلمة بالنجمة / *Asterisk* emphasis convention (ready)
- `ARAB-42` خط متموّج تحت الكلمة المفتاحية / Squiggle underline highlight (seen)
- `ARAB-44` ختم أحمر يرتطم / Rubber-stamp slam (seen)
- `ARAB-45` علامة استفهام عملاقة مفرّغة / Giant outlined question mark (ready)

### `ARAB-44` — ختم أحمر يرتطم / Rubber-stamp slam

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ختم نصي أحمر مائل يرتطم بالبطاقة مع صوت ختم واهتزاز صغير. / A tilted red text stamp slams onto the card with a stamp sound and a micro shake.

**متى:** حين تريد ختما أحمر مائلا يرتطم بالبطاقة مع صوت ختم واهتزاز صغير / when a red rubber stamp should slam onto a card with a stamp sound and micro shake

**كيف:** Build: red outlined text box #eb5757, border 4 px, rotated ≈ −4°, scale 1.6→1 with slight overshoot and opacity 0→1 in ~200 ms, synced to a stamp SFX and a micro camera shake.

**المعاملات:** #eb5757; 4 px; −4°; 1.6→1; ~200 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ختم · stamp · slam · verdict · shake · ختم أحمر · اهتزاز · حكم · rubber stamp · camera shake

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `style:stickman`

#### 7. قدرات قريبة في العائلة

- `ARAB-42` خط متموّج تحت الكلمة المفتاحية / Squiggle underline highlight (seen)
- `ARAB-43` ممسحة التظليل من اليمين / RTL highlighter swipe (seen)
- `ARAB-45` علامة استفهام عملاقة مفرّغة / Giant outlined question mark (ready)
- `ARAB-46` ظل مزدوج مزاح / Offset duotone shadow hero (seen)

### `ARAB-45` — علامة استفهام عملاقة مفرّغة / Giant outlined question mark

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT). |

**ما هي:** «؟» مجوّفة عملاقة ترتطم دائرةً خلف السؤال، تستقر ثم تخفت وتنكمش. / A huge hollow '؟' slams in rotated behind the question, settles, dims and implodes.

**متى:** حين يطرح الفيديو سؤالا وتريد علامة استفهام عربية ضخمة مفرغة خلفه / when a question on screen needs a huge hollow Arabic question mark slamming in behind it

**كيف:** '؟' (U+061F) 420 px, color transparent, -webkit-text-stroke 3px #f5c97a; from scale 2.4, rotation −12, opacity 0 → 1 in 0.7 s E.out; fill eases to rgba(245,201,122,.18); out: scale .2 in 0.25 s E.in. MK.lineMeta flags questions so a style can trigger it (ARAB-75).

**المعاملات:** 420 px; stroke 3 px #f5c97a; 0.7 s in / 0.25 s out

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** علامة استفهام · سؤال · question mark · outline text · text-stroke · استفهام · نص مفرغ · حدود النص · hollow text · big question mark

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-one/projects/whatsapp-motion/projects/success/index.html:39-40`
- `kosif-one/projects/whatsapp-motion/projects/success/index.html:218-221`

#### 7. قدرات قريبة في العائلة

- `ARAB-43` ممسحة التظليل من اليمين / RTL highlighter swipe (seen)
- `ARAB-44` ختم أحمر يرتطم / Rubber-stamp slam (seen)
- `ARAB-46` ظل مزدوج مزاح / Offset duotone shadow hero (seen)
- `ARAB-47` خط مضيء يتمدد تحت العنوان / Growing glow rule under the title (ready)

### `ARAB-46` — ظل مزدوج مزاح / Offset duotone shadow hero

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كلمة كبيرة بالخط المحلي خلفها نسختان مزاحتان بالوردي والأزرق. / A big native-script word with two offset copies in pink and blue behind it.

**متى:** حين تريد كلمة كبيرة بطابع ملصق خلفها نسختان مزاحتان بالوردي والأزرق / when a big word needs a poster look with pink and blue offset copies behind it

**كيف:** Build: render the word large; two duplicates behind offset 6–10 px (8 px default) in pink and blue; fade/slide the stack in. Seen with Devanagari; for Arabic keep each copy a whole word.

**المعاملات:** offset 8 px; 2 colours

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ظل مزدوج · duotone · offset shadow · poster · history · ظل ملون · نسخ مزاحة · بوستر · color offset · layered text

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `style:pm-buildfastwithai-53234e`

#### 7. قدرات قريبة في العائلة

- `ARAB-44` ختم أحمر يرتطم / Rubber-stamp slam (seen)
- `ARAB-45` علامة استفهام عملاقة مفرّغة / Giant outlined question mark (ready)
- `ARAB-47` خط مضيء يتمدد تحت العنوان / Growing glow rule under the title (ready)
- `ARAB-48` سطور تتكدس وتخفت / Stacked headline lines that dim (seen)

### `ARAB-47` — خط مضيء يتمدد تحت العنوان / Growing glow rule under the title

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT). |

**ما هي:** بعد هبوط العنوان العربي يتمدد تحته خط رفيع متوهج ثم يتبعه سطر فرعي. / After the Arabic title lands, a thin glowing rule grows beneath it, then a subtitle follows.

**متى:** حين تريد خطا رفيعا متوهجا يتمدد تحت العنوان العربي بعد هبوطه ثم يظهر سطر فرعي / when a thin glowing rule should grow under a landed Arabic title before a subtitle

**كيف:** #rule height 3 px, background #e0a35a, box-shadow 0 0 14px; tl.fromTo(rule, {width:0}, {width:240, duration:1.1, ease:'power4.out'}, T + 0.35); title 92 px/800 right-aligned, sub 34 px/600 at T + 0.45; titleAt 1.7 s; anchor the rule on the right (transform-origin right) for RTL.

**المعاملات:** 3 px #e0a35a; 0→240 px in 1.1 s power4.out

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خط مضيء · glow rule · underline · title card · night · خط تحت العنوان · عنوان فرعي · فاصل متوهج · accent line · subtitle

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/index.html:18`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/index.html:61`

#### 7. قدرات قريبة في العائلة

- `ARAB-45` علامة استفهام عملاقة مفرّغة / Giant outlined question mark (ready)
- `ARAB-46` ظل مزدوج مزاح / Offset duotone shadow hero (seen)
- `ARAB-48` سطور تتكدس وتخفت / Stacked headline lines that dim (seen)
- `ARAB-49` قوالب الموشن العربية الثمانية / Eight Arabic motion templates (proven)

### `ARAB-48` — سطور تتكدس وتخفت / Stacked headline lines that dim

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سطر عنوان مع كل نبضة؛ الجديد بكامل لونه والسابق يخفت إلى رمادي 40%. / One headline line per beat; the new one in full colour while earlier lines dim to ~40% grey.

**متى:** حين تريد إضافة سطر عنوان مع كل نبضة بينما تخفت السطور السابقة / when adding one headline line per beat while earlier lines dim to grey

**كيف:** Build: lines stack one per beat (from the right for Arabic); each new line enters at full colour while the earlier ones tween to ~40% grey; two-tone headlines (cream + lime); the key line sits on a slanted highlighter bar (ARAB-43).

**المعاملات:** earlier lines → 40%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تكدس السطور · خفوت · stacked lines · dim · trailer · beat · إعلان تشويقي · تريلر · سطور متتابعة · beat sync · headline stack

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `style:pm-deifosv-04e4d3`

#### 7. قدرات قريبة في العائلة

- `ARAB-46` ظل مزدوج مزاح / Offset duotone shadow hero (seen)
- `ARAB-47` خط مضيء يتمدد تحت العنوان / Growing glow rule under the title (ready)
- `ARAB-49` قوالب الموشن العربية الثمانية / Eight Arabic motion templates (proven)
- `ARAB-50` شريط اسم سفلي تلقائي الاتجاه / Auto-RTL lower third (proven)

### `ARAB-49` — قوالب الموشن العربية الثمانية / Eight Arabic motion templates

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT). |

**ما هي:** ثمانية قوالب HTML/GSAP حتمية تتحول بأمر واحد إلى مشروع قابل للتعديل بخط Cairo وأقنعة كلمات. / Eight deterministic HTML/GSAP templates that become an editable Cairo/word-mask project with one command.

**متى:** حين تحتاج قالب موشن عربي جاهزا للتعديل كعنوان أو شريط اسم أو عد تنازلي أو خاتمة / when you need a ready editable Arabic motion template: title, lower third, countdown or end card

**كيف:** python scripts/mtemplates.py list \| show NAME \| new PROJECT --template NAME --set key=value … [--seconds S --size 1080x1920 --fps 30] → projects/PROJECT/index.html + assets (fonts, gsap, motion-kit); text is HTML-escaped and colours validated (#RRGGBB); render with motion.py render or kosif-tool/tools/render_html.cjs --mode virtual. Also from the web studio ('قالب موشن…'), MCP kosif_project_create {kind:'template'}, GET /api/templates. title-card, lower-third and quote-card are tested; the rest are code.

**المعاملات:** see table

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قوالب · templates · title-card · lower-third · quote-card · countdown · end-card · bullet-list · mtemplates · قالب جاهز · عد تنازلي · بطاقة نهاية · خاتمة الفيديو · motion template

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:35`
- `100-superskills/skills/kosif-montage-motion/templates/motion/title-card.html`
- `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:14`
- `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:127`

#### 7. قدرات قريبة في العائلة

- `ARAB-47` خط مضيء يتمدد تحت العنوان / Growing glow rule under the title (ready)
- `ARAB-48` سطور تتكدس وتخفت / Stacked headline lines that dim (seen)
- `ARAB-50` شريط اسم سفلي تلقائي الاتجاه / Auto-RTL lower third (proven)
- `ARAB-51` ثلاثة أشكال لعنوان الخطاف / Hook title looks: box · kinetic · minimal (install)

### `ARAB-50` — شريط اسم سفلي تلقائي الاتجاه / Auto-RTL lower third

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT). |

**ما هي:** بطاقة اسم ووظيفة في المنطقة الآمنة السفلية؛ تكتشف العربية فتنقل الجانب وتقلب الاتجاه على الصندوق فقط. / Name + role card in the lower safe area; detects Arabic, flips side, and applies RTL to the box only.

**متى:** حين تريد إظهار اسم المتحدث ووظيفته أسفل الشاشة مع ضبط الاتجاه للعربية تلقائيا / when showing a speaker's name and role low on screen with auto RTL for Arabic

**كيف:** MOTION.lowerThird(tl, root, at, {title, sub, accent, size, inset, bottom, barWidth, side, hold, font}): accent bar 4 px #E7B65A grows to 120 px in 0.4 s; title 44 px bold at +0.12 s; sub 0.55× size rgba(255,255,255,.75) at +0.24 s; inset 72 px, bottom 160 px; exit 0.3 s. Timeline JSON equivalent: overlays type lower-third {title, sub, accent}.

**المعاملات:** bar 4×120 px; title 44 px; sub 55%; in .4/.5 s; out .3 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شريط اسم · lower third · name tag · speaker · auto rtl · اسم المتحدث · تعريف الضيف · الثلث السفلي · name card · name and title

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-studio/motion/kit/motion-kit.js:562`
- `100-superskills/skills/kosif-montage-motion/templates/motion/lower-third.html`
- `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:39`
- `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-48` سطور تتكدس وتخفت / Stacked headline lines that dim (seen)
- `ARAB-49` قوالب الموشن العربية الثمانية / Eight Arabic motion templates (proven)
- `ARAB-51` ثلاثة أشكال لعنوان الخطاف / Hook title looks: box · kinetic · minimal (install)
- `ARAB-52` صندوق عنوان يحافظ على مركزه / Centre-locked resizing title box (documented)

### `ARAB-51` — ثلاثة أشكال لعنوان الخطاف / Hook title looks: box · kinetic · minimal

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عنوان يظهر في أول 3 ثوانٍ بأحد ثلاثة أشكال: صندوق ينزلق، كلمات تدق، أو سطر هادئ بخط تحتي. / A hook title for the first 3 s in one of three looks: sliding box, stomping words, or a minimal line with an underline.

**متى:** حين تحتاج عنوانا يشد الانتباه في أول ثلاث ثوان بشكل صندوق أو كلمات تدق أو سطر هادئ / when a hook title for the first 3 seconds needs a box, stomping-word or minimal look

**كيف:** drawTitle(): box = easeBack slide from +0.6W over 0.45 s, Lalezar at 8.5% of the short side on a rounded primary box; kinetic = Lalezar 12%, each word stomps from scale 2.3 (1 + 1.3) to 1 over 0.18 s, 0.16 s apart, black stroke, alternating accent; minimal = IBM Plex Sans Arabic 700 at 6%, ease-out rise 0.6 s, accent underline grows from the right over 0.8 s; all fade out 2.65–3 s.

**المعاملات:** visible 0–3 s; fade 0.35 s

**التثبيت:** cd app && npm install

**الوسوم:** خطاف · عنوان افتتاحي · hook · opening title · stomp · lalezar · بداية الفيديو · شد الانتباه · هوك · intro title · attention grabber

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `app/public/js/00_editor.js:318`

#### 7. قدرات قريبة في العائلة

- `ARAB-49` قوالب الموشن العربية الثمانية / Eight Arabic motion templates (proven)
- `ARAB-50` شريط اسم سفلي تلقائي الاتجاه / Auto-RTL lower third (proven)
- `ARAB-52` صندوق عنوان يحافظ على مركزه / Centre-locked resizing title box (documented)
- `ARAB-53` ترويسة اليوم بالهجري والميلادي / Hijri + Gregorian day header (ready)

### `ARAB-52` — صندوق عنوان يحافظ على مركزه / Centre-locked resizing title box

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عبارة قصيرة تُستبدل بأطول بينما الصندوق خلفها يتمدد بنعومة حول مركز ثابت. / A short phrase swaps for a longer one while its box stretches smoothly around a fixed centre.

**متى:** حين تستبدل عبارة قصيرة بأطول ويجب أن يتمدد الصندوق خلفها بنعومة حول مركزه / when swapping a short phrase for a longer one while its box stretches around a fixed centre

**كيف:** 0–1 s first phrase, 1–2 s swap + resize, 2–4 s second phrase; measure the real shaped text (getBBox / measureText after the font gate) and tween the rect width to it; test the longest string; leave margin for tashkeel; RTL anchor = centre.

**المعاملات:** 4 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صندوق عنوان · قياس النص · title box · measure text · resize · MG-016 · تبديل العبارة · خلفية النص · تمدد الصندوق · text swap · auto width

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-50` شريط اسم سفلي تلقائي الاتجاه / Auto-RTL lower third (proven)
- `ARAB-51` ثلاثة أشكال لعنوان الخطاف / Hook title looks: box · kinetic · minimal (install)
- `ARAB-53` ترويسة اليوم بالهجري والميلادي / Hijri + Gregorian day header (ready)
- `ARAB-54` أقراص وشارات وأرقام مرقّمة / Pills, chips & numbered badges (ready)

### `ARAB-53` — ترويسة اليوم بالهجري والميلادي / Hijri + Gregorian day header

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | اسم اليوم بخط Aldhabi (خط ويندوز مملوك لمايكروسوفت) — محلي فقط؛ للشحن استخدم Aref Ruqaa أو Amiri (OFL)؛ GSAP مدمج / Aldhabi is a Microsoft Windows font — local only; ship with Aref Ruqaa/Amiri; GSAP vendored. |

**ما هي:** اسم اليوم بخط خطاطي كبير، وفوقه الشهر الهجري وتحته التاريخ الميلادي مع خطين ذهبيين يُرسمان. / A big calligraphic day name with the Hijri month above, the Gregorian date below and two drawn gold rules.

**متى:** حين تريد بطاقة لليوم باسمه بخط كبير مع الشهر الهجري والتاريخ الميلادي كبطاقة جمعة أو دعاء / for a day card with a big calligraphic day name, Hijri month and Gregorian date, e.g. Friday or dua

**كيف:** #day 170 px #ffe7a8 with glow, blur-in (y 46, scale .92, blur 10 px → 0) at 0.25 s; #month Amiri Bold 54 px #f4cf6b via revealWords ('ربيع الثاني ٢٧'); #date Amiri Bold 50 px LTR, letter-spacing 3 px on the Latin digits only ('08 . 10 . 2026'); two gold rules drawn at 0.8 / 0.95 s. Hijri text from Intl.DateTimeFormat('ar-SA-u-ca-islamic-umalqura', {day:'numeric', month:'long'}).

**المعاملات:** day 170 px; month 54 px; date 50 px; rules at 0.8/0.95 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هجري · ميلادي · تاريخ · hijri · date header · dua · friday · calligraphy · التاريخ الهجري · جمعة مباركة · بطاقة اليوم · islamic date · day card

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-one/projects/thursday-dua-animation/source/index.html:18-21`
- `kosif-one/projects/thursday-dua-animation/source/index.html:95-101`
- `kosif-one/projects/thursday-dua-animation/source/index.html:190-194`

#### 7. قدرات قريبة في العائلة

- `ARAB-51` ثلاثة أشكال لعنوان الخطاف / Hook title looks: box · kinetic · minimal (install)
- `ARAB-52` صندوق عنوان يحافظ على مركزه / Centre-locked resizing title box (documented)
- `ARAB-54` أقراص وشارات وأرقام مرقّمة / Pills, chips & numbered badges (ready)
- `ARAB-55` مكدّس عربي/إنجليزي / Bilingual Arabic/English stacks & HUD (ready)

### `ARAB-54` — أقراص وشارات وأرقام مرقّمة / Pills, chips & numbered badges

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شارات صغيرة تنبثق، رقائق أقسام، ودوائر زجاجية بأرقام هندية — طبقة التنظيم فوق المشهد. / Pop-in tags, section chips and frosted badges with Arabic-Indic numerals — the organising layer over a scene.

**متى:** حين تحتاج طبقة تنظيم فوق المشهد من شارات منبثقة ورقائق أقسام ودوائر بأرقام هندية / when a scene needs pop-in tags, section chips or numbered badges with Arabic-Indic digits

**كيف:** Tag pill: padding 10×24 px, 24 px/800, radius 8, gradient 135deg #f59e0b → #d97706, shadow 0 10px 25px rgba(245,158,11,.4), scale 0.8→1 + fade in 0–0.5 s; description fades up 30 px at 1.0–1.8 s (34 px/500 #a1a1aa lh 1.5). Section chips 'تعريف ١': 40 px pill, radius 999, 2 px currentColor border, bg rgba(5,7,11,.45) + blur(6px). Glass step badge: .num 54 px circle rgba(255,255,255,.14), 1.5 px white .75 border, backdrop-filter blur(6px), digits ١ ٢ ٣ ٤; label 46/700 + line 25/300. Floating language chips: pop 90 ms apart, drift 6 px sine over 3 s.

**المعاملات:** pill 24 px/800; chip 40 px; badge 54 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شارة · قرص · رقم · pill · chip · badge · glass · arabic-indic · label · وسوم · ترقيم · تاج · tag · numbered badge

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/kinetic_2d.html:40`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/index.html:17`
- `kosif-one/projects/whatsapp-motion/projects/success/index.html:74-106`
- `style:isometric`

#### 7. قدرات قريبة في العائلة

- `ARAB-52` صندوق عنوان يحافظ على مركزه / Centre-locked resizing title box (documented)
- `ARAB-53` ترويسة اليوم بالهجري والميلادي / Hijri + Gregorian day header (ready)
- `ARAB-55` مكدّس عربي/إنجليزي / Bilingual Arabic/English stacks & HUD (ready)
- `ARAB-56` بطاقة شخصية من اليمين / RTL character card (seen)

### `ARAB-55` — مكدّس عربي/إنجليزي / Bilingual Arabic/English stacks & HUD

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سطر عربي في الأعلى وترجمة إنجليزية أصغر تحته، أو HUD يجمع عنوانًا عربيًا وسطرًا تقنيًا إنجليزيًا. / Arabic line on top with a smaller English line below, or a HUD pairing an Arabic headline with a technical English line.

**متى:** حين تعرض سطرا عربيا وتحته ترجمة إنجليزية أصغر أو واجهة HUD تجمع اللغتين / when showing Arabic with a smaller English line beneath, or a HUD pairing both languages

**كيف:** Arabic block RTL on top, English block LTR beneath at ~70% size (the doodle reference sits near 2.8:1 with muted blue English), each block with its own dir. HUD per stage: #ar Cairo 800 62 px rising 26 px over 0.2 s; #en mono 21 px built from live numbers; colour by stage — #ffb4a2 failure, #d0ff6a success, #eaffed default.

**المعاملات:** EN ≈70% of AR (doodle 2.8:1); HUD 62 / 21 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ثنائي اللغة · ترجمة · bilingual · hud · english subtitle · dual caption · عربي وانجليزي · ترجمة مزدوجة · سطرين · arabic english · two languages

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:82`
- `kosif-tool/playbooks/arabic-typography.md`
- `style:doodle`

#### 7. قدرات قريبة في العائلة

- `ARAB-53` ترويسة اليوم بالهجري والميلادي / Hijri + Gregorian day header (ready)
- `ARAB-54` أقراص وشارات وأرقام مرقّمة / Pills, chips & numbered badges (ready)
- `ARAB-56` بطاقة شخصية من اليمين / RTL character card (seen)
- `ARAB-57` عنوان عربي سينمائي فوق الفيديو / Cinematic Arabic headline over footage (ready)

### `ARAB-56` — بطاقة شخصية من اليمين / RTL character card

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صورة مؤطرة يسارًا، وعلى اليمين شارة ودور واسم ضخم وسطر تعريف. / Framed avatar left; right-aligned tag pill, role, huge name and a one-line bio.

**متى:** حين تقدم شخصيات أو أشخاصا ببطاقة فيها صورة واسم ضخم ودور وسطر تعريف / when introducing people with a card of avatar, huge name, role and one-line bio

**كيف:** Build: avatar frame on the left; right-aligned stack: tag pill, small role, huge name, one-line bio; gold/cream on navy and burgundy (#172237, #731521, #e9d5b0, #e0b23a); cards slide/fade about every 1.7 s; party names in pop-in pills.

**المعاملات:** card every ~1.7 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بطاقة شخصية · character card · profile · timeline · rtl · تعريف شخص · بروفايل · صورة واسم · bio card · avatar

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `style:pm-triglyceee-bd5b08`

#### 7. قدرات قريبة في العائلة

- `ARAB-54` أقراص وشارات وأرقام مرقّمة / Pills, chips & numbered badges (ready)
- `ARAB-55` مكدّس عربي/إنجليزي / Bilingual Arabic/English stacks & HUD (ready)
- `ARAB-57` عنوان عربي سينمائي فوق الفيديو / Cinematic Arabic headline over footage (ready)
- `ARAB-58` عنوان ASS متحرك لكل لقطة / Per-shot ASS animated title card (ready)

### `ARAB-57` — عنوان عربي سينمائي فوق الفيديو / Cinematic Arabic headline over footage

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عنوان عربي كبير متوازن بظل داكن ناعم وسطر علوي صغير، في الركن السفلي من بداية القراءة فوق اللقطات. / A large balanced Arabic headline with a soft dark shadow and a small eyebrow, bottom-start over footage.

**متى:** حين تضع عنوانا عربيا كبيرا متوازنا بظل ناعم فوق لقطات فيديو / when setting a large balanced Arabic headline with a soft shadow over footage

**كيف:** h2 font-size clamp(31px,4.9vw,65px), lh 1.18, weight 700, text-wrap:balance, text-shadow 0 3px 30px rgba(0,0,0,.45); eyebrow 12 px/700 (its .16em tracking only on Latin); description clamp(13px,1.7vw,17px) lh 1.9; phone h2 clamp(29px,8vw,42px); box width min(560px, 100% − 44px), inset-inline-start clamp(22px,6vw,110px). Drop the source's −.035em tracking on Arabic (ARAB-03).

**المعاملات:** lh 1.18; shadow 0 3px 30px .45

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عنوان سينمائي · فوق الفيديو · cinematic headline · footage · text-wrap balance · documentary · عنوان فوق اللقطة · وثائقي · ظل النص · text shadow · headline overlay

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-earth-ci-fork/ui/art/brand/earth-intro-20261009.css`
- `kosif-audit-studio/styles.css:166`
- `kosif-audit-studio/continuous-review.css:1`

#### 7. قدرات قريبة في العائلة

- `ARAB-55` مكدّس عربي/إنجليزي / Bilingual Arabic/English stacks & HUD (ready)
- `ARAB-56` بطاقة شخصية من اليمين / RTL character card (seen)
- `ARAB-58` عنوان ASS متحرك لكل لقطة / Per-shot ASS animated title card (ready)
- `ARAB-59` غلاف بعنوان عربي مشكّل / Shaped Arabic cover / thumbnail (ready)

### `ARAB-58` — عنوان ASS متحرك لكل لقطة / Per-shot ASS animated title card

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | الأصل يستخدم Dubai (مملوك) — استبدله بـ Cairo من proofs/_shared/fonts / original uses proprietary Dubai — swap to Cairo from proofs/_shared/fonts. |

**ما هي:** ملف ASS لكل لقطة فيه كلمة بطلة وسطر تفصيل يصعدان ويتلاشيان وشعار ثابت في الزاوية — يُحرق بـ libass بلا متصفح. / One ASS file per shot: hero word + detail line that rise and fade, plus a fixed corner tag — burned by libass, no browser.

**متى:** حين تريد حرق عنوان متحرك لكل لقطة بالـ ffmpeg دون متصفح / when burning an animated per-shot title card with ffmpeg and libass, no browser

**كيف:** ASS v4.00+ (PlayResX/Y = frame size, WrapStyle 2, UTF-8 BOM), three styles. Hero 60 px bold, outline 2.5, shadow 1.3, MarginV 210: {\an2\move(x,766,x,740,0,900)\fad(650,700)}; Detail 32 px, outline 1.4: {\move(x,812,x,793,300,1050)\fad(650,600)} starting +0.45 s; Tag 21 px {\an7\pos(30,38)\fad(400,600)}; burn with ffmpeg -vf "ass=scene_XX.ass:fontsdir=fonts"; style Encoding −1 (ARAB-62).

**المعاملات:** hero 60 px, move 26 px over 0.9 s; detail +0.45 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ass · libass · عنوان · title card · ffmpeg · move · fad · حرق العنوان · بطاقة عنوان · بدون متصفح · burn in · subtitle file

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:39-63`

#### 7. قدرات قريبة في العائلة

- `ARAB-56` بطاقة شخصية من اليمين / RTL character card (seen)
- `ARAB-57` عنوان عربي سينمائي فوق الفيديو / Cinematic Arabic headline over footage (ready)
- `ARAB-59` غلاف بعنوان عربي مشكّل / Shaped Arabic cover / thumbnail (ready)
- `ARAB-60` كاروسيل عربي PNG/PDF / Arabic carousel renderer (ready)

### `ARAB-59` — غلاف بعنوان عربي مشكّل / Shaped Arabic cover / thumbnail

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يأخذ إطارًا من الفيلم، يعتّم أسفله بتدرج منحنٍ، ويكتب عنوانًا عربيًا مشكّلًا (≤3 أسطر) وسطرًا ذهبيًا. / Grabs a frame, darkens the lower part with a curved gradient and sets a shaped Arabic title (≤3 lines) plus a gold subtitle.

**متى:** حين تحتاج صورة غلاف للفيديو من أحد إطاراته مع عنوان عربي مشكل / when making a video cover or thumbnail from a frame with a shaped Arabic title

**كيف:** python kosif-studio/motion/tools.py thumb FILM --out cover.jpg [--at 2.0 --text 'عنوان' --sub '…' --size 1080x1920] (same as kmotion thumb): optional reframe; gradient alpha 0.78·t² from 45% height; title 8.5% of the short side, stroke size/18, lh 1.25, wrap at 84% width, block ending at 80% H; sub 50% size #E7B65A; JPEG q93. It is correct here because Pillow RAQM shapes the raw text — do not install arabic-reshaper in this container (ARAB-06).

**المعاملات:** title 8.5% short side; gradient 0.78·t²; q93

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** غلاف · صورة مصغرة · thumbnail · cover · pillow · poster frame · ثمبنيل · صورة الغلاف · عنوان الغلاف · video cover · frame grab

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:arabic-reshaper` ← python3 -c "import arabic-reshaper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-59` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-studio/motion/tools.py:317`
- `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-57` عنوان عربي سينمائي فوق الفيديو / Cinematic Arabic headline over footage (ready)
- `ARAB-58` عنوان ASS متحرك لكل لقطة / Per-shot ASS animated title card (ready)
- `ARAB-60` كاروسيل عربي PNG/PDF / Arabic carousel renderer (ready)
- `ARAB-61` طبقات نص الخط الزمني JSON / Timeline-JSON text overlays (ready)

### `ARAB-60` — كاروسيل عربي PNG/PDF / Arabic carousel renderer

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يرسم شرائح كاروسيل عربية مع PDF وورقة لقطات، ويصغّر العناوين تلقائيًا إلى ≤4 أسطر. / Renders Arabic carousel slides + PDF + contact sheet, auto-shrinking titles to ≤4 lines.

**متى:** حين تحتاج شرائح كاروسيل عربية للسوشيال صورا وملف PDF مع تصغير العناوين تلقائيا / when producing Arabic carousel slides as PNGs and a PDF with auto-shrinking titles

**كيف:** python3 100-superskills/skills/kosif-social/scripts/social.py carousel spec.json --out dir → slide_NN.png + carousel.pdf + contact sheet; 1080×1350 or 1080×1440; Latin fallback font; brand bg/fg/accent/handle. Shaping here is Pillow RAQM on raw text (its reshaper import falls back). Font search prefers NotoKufiArabic-Bold → Cairo-Bold → Tajawal-Bold …; drop Cairo-Bold.ttf into ~/.fonts so it is not left on DejaVu.

**المعاملات:** 1080×1350 \| 1080×1440; ≤4 title lines

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كاروسيل · carousel · instagram · pdf · social · slides · شرائح · منشور انستجرام · سوشيال ميديا · post · png slides

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-60` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-social/scripts/social.py:316`
- `100-superskills/skills/kosif-social/examples/carousel.json`

#### 7. قدرات قريبة في العائلة

- `ARAB-58` عنوان ASS متحرك لكل لقطة / Per-shot ASS animated title card (ready)
- `ARAB-59` غلاف بعنوان عربي مشكّل / Shaped Arabic cover / thumbnail (ready)
- `ARAB-61` طبقات نص الخط الزمني JSON / Timeline-JSON text overlays (ready)
- `ARAB-62` كاريوكي ASS عربي بثلاثة أنماط / Arabic ASS karaoke captions (reels · cinema · punchy) (proven)

### `ARAB-61` — طبقات نص الخط الزمني JSON / Timeline-JSON text overlays

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نص أو شريط اسم يُعلن في ملف الخط الزمني بموضع وحجم وحركة جاهزة، فيُرسم مشكّلًا فوق اللقطات. / Text or lower thirds declared in the timeline JSON with position, size and a preset move, drawn shaped over footage.

**متى:** حين تضيف نصوصا أو شريط اسم فوق اللقطات بتعريفها في ملف الخط الزمني / when declaring text or lower-third overlays in the timeline JSON over footage

**كيف:** overlays: type text {pos, size, color, box, stroke, anim: fade\|rise\|drop\|slide-left\|slide-right\|none}, fade 0.35 s, 9:16 safe band 14–80% of height; type lower-third {title, sub, accent #E7B65A}. For full tashkeel switch the mimic text_style.engine to 'browser'.

**المعاملات:** anims fade\|rise\|drop\|slide-left\|slide-right\|none; fade 0.35 s; safe 14–80%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خط زمني · timeline · json · overlay · lower third · text anim · نص فوق الفيديو · كتابة على الفيديو · طبقة نص · text overlay · preset motion

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-61` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`
- `100-superskills/skills/kosif-montage-motion/references/mimic.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-59` غلاف بعنوان عربي مشكّل / Shaped Arabic cover / thumbnail (ready)
- `ARAB-60` كاروسيل عربي PNG/PDF / Arabic carousel renderer (ready)
- `ARAB-62` كاريوكي ASS عربي بثلاثة أنماط / Arabic ASS karaoke captions (reels · cinema · punchy) (proven)
- `ARAB-63` قانون زمن القراءة والكثافة / Reading-time & density law (documented)

### `ARAB-62` — كاريوكي ASS عربي بثلاثة أنماط / Arabic ASS karaoke captions (reels · cinema · punchy)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ترجمة تُحرق في الفيديو بحدث لكل كلمة منطوقة: لون التمييز ونبضة 112%→100% في 120 ms، وترتيب الكلمات العربي سليم. / Burned captions with one event per spoken word: highlight colour and a 112%→100% pop in 120 ms, Arabic word order intact.

**متى:** حين تريد ترجمة عربية محروقة في الفيديو تضيء كل كلمة لحظة نطقها / when burning Arabic captions into a video with each spoken word highlighted

**كيف:** python kosif-studio/motion/montage.py captions VIDEO --spec caps.json --style reels\|cinema\|punchy (also inside cut/voicecut). PlayRes = frame; sizes scale with the short side; side margins 6% W; ≤6 words per on-screen chunk; one Dialogue per word with {\1c<hi>\fscx112\fscy112\t(0,120,\fscx100\fscy100)}word{\r}; missing word times are split by letters + 2; style Encoding −1 so libass detects the RTL paragraph; burn ass=caps.ass,format=yuv420p, libx264 crf 17, audio copied untouched. Verified here with Cairo via fontsdir: Encoding −1 keeps 'كل إطار يسمع الموسيقى' in order; Encoding 1 + an override flips it to 'الموسيقى يسمع كل إطار'. Noto Arabic is not installed system-wide here, so pass fontsdir= (or register the repo fonts) or libass falls back. (code snippet in references/powers/typography-arabic.md)

**المعاملات:** pop 112%→100% / 120 ms; ≤6 words; Encoding −1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كاريوكي · ترجمة · سبتايتل · karaoke · captions · ass · libass · burn subtitles · reels · word highlight · كابشن · ترجمة محروقة · تمييز الكلمة · subtitles · word by word

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-62` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-studio/motion/montage.py:321`
- `kosif-studio/tests/test_studio.py:765`
- `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-60` كاروسيل عربي PNG/PDF / Arabic carousel renderer (ready)
- `ARAB-61` طبقات نص الخط الزمني JSON / Timeline-JSON text overlays (ready)
- `ARAB-63` قانون زمن القراءة والكثافة / Reading-time & density law (documented)
- `ARAB-64` منطقة الترجمة الآمنة وشكلها / Caption safe zone & look (documented)

### `ARAB-63` — قانون زمن القراءة والكثافة / Reading-time & density law

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كم كلمة على الشاشة وكم تبقى: معادلات ثابتة بدل التخمين. / How many words on screen and for how long — fixed formulas instead of guessing.

**متى:** حين تحدد كم كلمة تظهر على الشاشة وكم تبقى بدل التخمين / when deciding how many words go on screen and how long they stay, instead of guessing

**كيف:** Hook text: cold-open line bold and larger (0.16 of frame vs 0.12), ≤12 characters; other lines ≤18; max 2 lines; display = max(0.15 s × characters, 2 s), capped at 6 s; enter 0.3 s after a cut, leave 0.3 s before the next; count graphemes after shaping. Cards: 3–4 words (1–7), ~0.4 s per word, ≥0.5 s per card, a URL ≥1.7 s. Line hold ≥ 0.3 s + 0.06 s × characters after the last word lands. Captions 5–7 words.

**المعاملات:** t = max(0.15·chars, 2) ≤ 6 s; 0.3 s offsets; 0.4 s/word

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** زمن القراءة · كثافة · reading time · density · hook timing · words per card · مدة الظهور · عدد الكلمات · سرعة القراءة · on-screen duration · text timing

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-63` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/SKILL.md`
- `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`
- `kosif-tool/playbooks/kinetic-type.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-61` طبقات نص الخط الزمني JSON / Timeline-JSON text overlays (ready)
- `ARAB-62` كاريوكي ASS عربي بثلاثة أنماط / Arabic ASS karaoke captions (reels · cinema · punchy) (proven)
- `ARAB-64` منطقة الترجمة الآمنة وشكلها / Caption safe zone & look (documented)
- `ARAB-65` الكلمة المنطوقة تضيء / Spoken-word illumination (HTML captions) (seen)

### `ARAB-64` — منطقة الترجمة الآمنة وشكلها / Caption safe zone & look

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أين تجلس الترجمة وبأي سماكة حدّ وكم كلمة — للسينما وللمنصات. / Where captions sit, how thick the outline is and how many words — for cinema and for social.

**متى:** حين تضبط مكان الترجمة وسماكة حدها وعدد كلماتها للسينما أو للمنصات / when placing captions and setting outline and word count for cinema or social

**كيف:** Cinema: bottom-centre white, thin black outline 1–2, no box, no animation; one line preferred, max two growing upward; glyph height 3.5–4.5% of H, side margin ≥8%, bottom 8–10% (ASS Alignment=2, Shadow=0, MarginV ≈ 9% H; BorderStyle=3 gives an opaque box). Social: bold clear face (Cairo/Almarai), outline 6–8 px, deep shadow, 5–7 words, ≥280 px from the bottom on 9:16, safe band 14–80% of height; Naskh captions ≤8 words, mono only for code. Use OFL fonts only and stop if missing (fc-list \| grep -i <font>) rather than substitute.

**المعاملات:** glyph 3.5–4.5% H; margins 8%; outline 6–8 px social; ≥280 px bottom

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** منطقة آمنة · ترجمة · safe zone · subtitle · outline · margin · 9:16 · مكان الترجمة · هوامش · سبتايتل · caption position · subtitle style

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-64` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-atlas/skills/1096-akbun-editvideo/2431-akbun-davinciresolve-caption-template/SKILL.md`
- `100-superskills/skills/kosif-montage-motion/references/montage_grammar.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2464-davinciresolve-subtitle-devtalk/SKILL.md`
- `kosif-tool/styles/pm-jake11moran-a269c4/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-62` كاريوكي ASS عربي بثلاثة أنماط / Arabic ASS karaoke captions (reels · cinema · punchy) (proven)
- `ARAB-63` قانون زمن القراءة والكثافة / Reading-time & density law (documented)
- `ARAB-65` الكلمة المنطوقة تضيء / Spoken-word illumination (HTML captions) (seen)
- `ARAB-66` فيلم الكلمات من الصوت / Verse film from sound (song · poem · dua) (install)

### `ARAB-65` — الكلمة المنطوقة تضيء / Spoken-word illumination (HTML captions)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الجملة كلها ظاهرة كشبح باهت، وكل كلمة تتجسد وتأخذ اللون لحظة نطقها. / The whole line sits as a faint ghost; each word solidifies and takes colour as it is spoken.

**متى:** حين تريد الجملة ظاهرة باهتة وكل كلمة تضيء لحظة نطقها في ترجمة HTML / when a faint line should light up word by word as each is spoken, in HTML captions

**كيف:** Build: phrase at 25–60% opacity (doodle ghost ~25%, playbook recipe 60%); at words.json start − 40…80 ms the word goes to 100% + accent; emphasis words orange (#f27525 plotter / #f07f2e doodle); optional accent pill that hops word to word, scale 0.96→1.08 over 140 ms; long words may fill right→left over their duration; never change transcript words.

**المعاملات:** ghost 25–60%; lead 40–80 ms; pill 0.96→1.08 / 140 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إضاءة الكلمة · مزامنة · spoken word · karaoke html · ghost text · words.json · highlight · كاريوكي · تزامن الصوت · ترجمة متحركة · word sync · caption highlight

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-65` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `style:doodle`
- `style:plotter`
- `kosif-tool/playbooks/kinetic-type.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-63` قانون زمن القراءة والكثافة / Reading-time & density law (documented)
- `ARAB-64` منطقة الترجمة الآمنة وشكلها / Caption safe zone & look (documented)
- `ARAB-66` فيلم الكلمات من الصوت / Verse film from sound (song · poem · dua) (install)
- `ARAB-67` تقسيم الأسطر بالبرمجة الديناميكية / DP line breaking for lyrics & dua (proven)

### `ARAB-66` — فيلم الكلمات من الصوت / Verse film from sound (song · poem · dua)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT). \| faster-whisper MIT. |

**ما هي:** من أغنية أو قصيدة أو دعاء: كلمات محاذاة، أسطر مقروءة، مقاطع عند الوقفات، كلمة مفتاحية لكل سطر، وضوء يقوده الصوت — في verse.json قابل للتعديل. / From a song, poem or dua: aligned words, readable lines, sections at pauses, one keyword per line and sound-driven light — written to an editable verse.json.

**متى:** حين يعطيك المستخدم أغنية أو قصيدة أو دعاء صوتيا ويريد فيديو كلمات متزامنا / when the user supplies a song, poem or dua recording and wants a synced words film

**كيف:** python kosif-studio/motion/verse.py AUDIO --name N [--text lyrics.txt] [--words X.words.json] [--mood night\|dawn\|gold\|sea\|ink] [--accent #E7B65A] [--font 'Aref Ruqaa'] [--images …] [--music none\|auto] [--flat] [--render] (kmotion verse is the same). True text is aligned onto Whisper word times, diacritic/hamza tolerant (ARAB-69); lines 1.1–3.6 s, ≤7 words (ARAB-67); pause ≥3 s → new section, ≥4.5 s → interlude with an 8-point rosette; ~12 s sections; keywords ≥2 s apart (ARAB-68); concept icons sun, moon, heart, clock, money, trophy, road, question, check, home, rain, light; 3D words (ARAB-28), gilded fill (ARAB-39), dust and light rays; title/end cards 128k/42k with .25 s stagger, 0.7 s power3.out; custom display face from assets/display.ttf. Music is none by default — recitations stay unaccompanied. Arabic transcription wants a multilingual large-v3 model.

**المعاملات:** lines ≤7 words, 1.1–3.6 s; section pause 3 s; interlude 4.5 s; 24.8 s dua → 743 frames

**التثبيت:** pip install faster-whisper

**الوسوم:** قصيدة · دعاء · أغنية · شعر · verse · lyrics · poem · dua · whisper · kinetic · calm · فيديو كلمات · كلمات الأغنية · مزامنة الكلمات · lyric video · word alignment

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-66` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-studio/motion/verse.py`
- `kosif-one/tools/kosif-studio/motion/verse.py:1`
- `kosif-one/tools/kosif-studio/motion/projects/verse_dua/verse.json`
- `100-superskills/skills/kosif-montage-motion/scripts/verse.py:199`

#### 7. قدرات قريبة في العائلة

- `ARAB-64` منطقة الترجمة الآمنة وشكلها / Caption safe zone & look (documented)
- `ARAB-65` الكلمة المنطوقة تضيء / Spoken-word illumination (HTML captions) (seen)
- `ARAB-67` تقسيم الأسطر بالبرمجة الديناميكية / DP line breaking for lyrics & dua (proven)
- `ARAB-68` اختيار الكلمة المفتاحية بالنبر / Stress-based keyword picking (proven)

### `ARAB-67` — تقسيم الأسطر بالبرمجة الديناميكية / DP line breaking for lyrics & dua

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يختار نقاط القطع بحيث يكون كل سطر مقروءًا: لا قصير ولا طويل، عند الوقفات والترقيم وبدايات العبارات، ولا يقطع بعد حرف جر ولا داخل دعاء ثابت. / Chooses cut points so every line reads well — at pauses, punctuation and phrase openers, never after a particle or inside a fixed invocation.

**متى:** حين تقسم كلمات أغنية أو دعاء إلى أسطر مقروءة عند الوقفات دون قطع العبارات / when splitting lyrics or a dua into readable lines at pauses without cutting phrases

**كيف:** verse.segment(words, max_words=7): dynamic programming over cut points; target 1.1–3.6 s per line; break bonus 8·min(gap, 1) + punctuation 1.0 + phrase opener 0.8 (اللهم، يا، إلا، and dua imperatives اجعل/اغفر/ارحم…) + و-clause 0.6 + ف-clause 0.5; penalties: after a particle −0.7, inside numbers −0.8, a 'يا … يا' chain −1.0.

**المعاملات:** ≤7 words; 1.1–3.6 s; bonuses 8/1.0/0.8/0.6/0.5; penalties −0.7/−0.8/−1.0

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تقسيم الأسطر · line breaking · dynamic programming · dua · lyrics · segmentation · تقطيع الجمل · فواصل الأسطر · وقفات · line splitting · phrase breaks

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-67` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-studio/motion/verse.py:203`
- `kosif-studio/motion/verse.py:217`
- `kosif-studio/tests/test_studio.py:943`

#### 7. قدرات قريبة في العائلة

- `ARAB-65` الكلمة المنطوقة تضيء / Spoken-word illumination (HTML captions) (seen)
- `ARAB-66` فيلم الكلمات من الصوت / Verse film from sound (song · poem · dua) (install)
- `ARAB-68` اختيار الكلمة المفتاحية بالنبر / Stress-based keyword picking (proven)
- `ARAB-69` توحيد النص العربي للمطابقة / Arabic normalisation for alignment & matching (proven)

### `ARAB-68` — اختيار الكلمة المفتاحية بالنبر / Stress-based keyword picking

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يقيس نبر كل كلمة من علو الصوت وطولها ويختار كلمة واحدة لكل سطر، ولا يختار الحشو ولا الوحدات بعد الأرقام. / Scores each word's stress from loudness and length and picks one keyword per line — never fillers or units after numbers.

**متى:** حين تختار تلقائيا كلمة مفتاحية لكل سطر من علو الصوت وطول الكلمة / when automatically picking one keyword per line from loudness and word length

**كيف:** stress = 0.65·z(log rms) + 0.35·z(length); score = stress + 0.9·(i+1)/n (end focus) + 0.5 if the word recurs 2–3×; a unit after a number −3; ~130 stop/filler words excluded (MSA + Egyptian: ده، دي، كده، بس، يعني، اوي…); each keyword used once; spacing ≥1.2 s (direct) or score ≥0.75 and ≥2 s apart (verse).

**المعاملات:** 0.65/0.35 weights; end focus 0.9; recurrence +0.5; spacing 1.2 s / 2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كلمة مفتاحية · نبر · keyword · stress · stop words · egyptian · emphasis · إبراز تلقائي · علو الصوت · كلمات الحشو · loudness · auto keyword

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-68` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-studio/motion/direct.py:87`
- `kosif-studio/motion/direct.py:143`
- `kosif-studio/motion/verse.py:300`
- `kosif-studio/motion/direct.py:36`

#### 7. قدرات قريبة في العائلة

- `ARAB-66` فيلم الكلمات من الصوت / Verse film from sound (song · poem · dua) (install)
- `ARAB-67` تقسيم الأسطر بالبرمجة الديناميكية / DP line breaking for lyrics & dua (proven)
- `ARAB-69` توحيد النص العربي للمطابقة / Arabic normalisation for alignment & matching (proven)
- `ARAB-70` النص المشكول مصدرًا للتوقيت / Vowelled source text over ASR (documented)

### `ARAB-69` — توحيد النص العربي للمطابقة / Arabic normalisation for alignment & matching

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شكل مقارن للكلمة: بلا تشكيل ولا تطويل، ألفات موحدة، ى←ي، ة←ه، ؤ←و، ئ←ي، وأرقام لاتينية. / A comparable form of each word: no harakat or tatweel, unified alefs, ى→ي, ة→ه, ؤ→و, ئ→ي, Latin digits.

**متى:** حين تطابق كلمات عربية أو تبحث فيها وتحتاج إزالة التشكيل وتوحيد الألف والتاء والياء / when matching Arabic words and you need tashkeel removed and letter forms unified

**كيف:** NFKC; strip U+064B–U+065F, U+0670 and tatweel; أ إ آ ٱ → ا; ى → ي; ة → ه; ؤ → و; ئ → ي; ٠–٩ (and ۰–۹) → 0–9; drop punctuation; collapse spaces. Display text keeps its tashkeel — normalise only the matching copy. (code snippet in references/powers/typography-arabic.md)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** توحيد · تطبيع · normalise · normalization · alef · harakat · alignment · hashtag · إزالة التشكيل · توحيد الألف · مطابقة النص · text matching · strip diacritics

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-69` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-audit-studio/engine.js:31`
- `kosif-audit-studio/tests/voice.test.js:14`
- `kosif-studio/motion/verse.py:64`
- `kosif-one/tools/kosif-social/scripts/social.py`

#### 7. قدرات قريبة في العائلة

- `ARAB-67` تقسيم الأسطر بالبرمجة الديناميكية / DP line breaking for lyrics & dua (proven)
- `ARAB-68` اختيار الكلمة المفتاحية بالنبر / Stress-based keyword picking (proven)
- `ARAB-70` النص المشكول مصدرًا للتوقيت / Vowelled source text over ASR (documented)
- `ARAB-71` ستايل الكلمات العاطفي / Emotional lyric style preset (install)

### `ARAB-70` — النص المشكول مصدرًا للتوقيت / Vowelled source text over ASR

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** احتفظ بالتشكيل الكامل ووقفات الشاعر «..» في ملف الكلمات واجعله مصدر المحاذاة بدل الثقة بالتفريغ الآلي للغناء. / Keep full tashkeel and the poet's '..' pauses in the lyric file and align it, instead of trusting ASR on singing.

**متى:** حين يكون لديك نص القصيدة أو الأغنية مشكولا وتريد توقيته على الصوت بدل التفريغ الآلي / when you have the vowelled lyric text and should align it to audio instead of trusting ASR

**كيف:** lyrics.txt with complete harakat; pass it with --text so ASR only provides timing; split on '..' for phrase cards; display harakat through the browser engine (ARAB-06). Example: 31 vowelled lines.

**المعاملات:** 31 lines example

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تشكيل · نص مشكول · lyrics · tashkeel · alignment · asr · توقيت الكلمات · التفريغ الآلي · كلمات أغنية · lyrics file · word timing

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-70` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-one/projects/songreel-ghorba/lyrics.txt`

#### 7. قدرات قريبة في العائلة

- `ARAB-68` اختيار الكلمة المفتاحية بالنبر / Stress-based keyword picking (proven)
- `ARAB-69` توحيد النص العربي للمطابقة / Arabic normalisation for alignment & matching (proven)
- `ARAB-71` ستايل الكلمات العاطفي / Emotional lyric style preset (install)
- `ARAB-72` العزل الاتجاهي / Bidi isolation (ready)

### `ARAB-71` — ستايل الكلمات العاطفي / Emotional lyric style preset

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كلمات كبيرة لليلة بلونين تدفأ على الكلمات المميزة، بوكيه سابح، تسرّب ضوء يتنفس، والسطر السابق يطفو بعيدًا. / Big words on a two-colour night that warms on emphasised words, drifting bokeh, a breathing light leak, the previous line floating away.

**متى:** حين تريد فيديو كلمات أغنية بطابع ليلي دافئ عاطفي مع بوكيه وتسرب ضوء / for an emotional night-toned lyric video with warm emphasis, drifting bokeh and a light leak

**كيف:** STY.lyric: 9:16, calm, 2.0 words/s; Lalezar heads + Cairo body; bg #0E0A16 → bg2 #2A1236, ink #F7EFE6, dim rgba(247,239,230,.28), accent #FFB35C, glow #FF7A59; an underline grows with the voice; sfx shimmer/pop/swell; uses the real song words when audio exists.

**المعاملات:** 2.0 wps; #0E0A16/#2A1236/#F7EFE6/#FFB35C/#FF7A59

**التثبيت:** cd app && npm install

**الوسوم:** عاطفي · أغنية · lyric style · palette · night · bokeh · light leak · ستايل عاطفي · فيديو أغنية · ليلي · emotional · lyric video

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-71` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `app/public/js/10_studio.js:551`

#### 7. قدرات قريبة في العائلة

- `ARAB-69` توحيد النص العربي للمطابقة / Arabic normalisation for alignment & matching (proven)
- `ARAB-70` النص المشكول مصدرًا للتوقيت / Vowelled source text over ASR (documented)
- `ARAB-72` العزل الاتجاهي / Bidi isolation (ready)
- `ARAB-73` نظام أرقام واحد وأرقام جدولية / One digit system + tabular figures (ready)

### `ARAB-72` — العزل الاتجاهي / Bidi isolation

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الأسماء اللاتينية والأرقام داخل جملة عربية تقلب الترقيم وترتيبها ما لم تُعزل. / Latin names and numbers inside Arabic flip punctuation and order unless isolated.

**متى:** حين تنقلب الأرقام أو الأسماء الإنجليزية أو الترقيم داخل جملة عربية / when Latin names, numbers or punctuation flip order inside an Arabic sentence

**كيف:** <bdi> or unicode-bidi:isolate (plaintext for whole mixed lines) around Latin names, numbers, code and timecodes; control chars RLI U+2067 / LRI U+2066 / PDI U+2069; in ASS/ffmpeg add RLM U+200F at line edges; the review page wraps every Arabic run in <bdi dir=rtl> (AR_RUN regex); code blocks dir=ltr + isolate inside RTL pages; mirror arrows and progress fills, never logos, media or time axes.

**المعاملات:** RLI 2067 / LRI 2066 / PDI 2069 / RLM 200F

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عزل · اتجاه · bidi · bdi · isolate · mixed text · numbers · rlm · أرقام مقلوبة · ترتيب الكلمات · نص مختلط · punctuation flip · rtl ltr

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-72` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:902`
- `kosif-tool/playbooks/arabic-typography.md:48`
- `kosif-atlas/skills/2329-localization-i18n-engineering/8940-i18n-foundations-and-icu/SKILL.md`
- `kosif-tool/playbooks/code.md:73`

#### 7. قدرات قريبة في العائلة

- `ARAB-70` النص المشكول مصدرًا للتوقيت / Vowelled source text over ASR (documented)
- `ARAB-71` ستايل الكلمات العاطفي / Emotional lyric style preset (install)
- `ARAB-73` نظام أرقام واحد وأرقام جدولية / One digit system + tabular figures (ready)
- `ARAB-74` منسّق الأرقام الهندية الحتمي / Deterministic Arabic-Indic money formatter (proven)

### `ARAB-73` — نظام أرقام واحد وأرقام جدولية / One digit system + tabular figures

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اختر أرقامًا غربية أو هندية للفيلم كله، واجعلها جدولية حتى لا يرتجف العدّاد. / Choose Western or Arabic-Indic digits for the whole film and make them tabular so counters never jitter.

**متى:** حين تختار أرقاما غربية أو هندية للفيلم كله وتريد عدادا لا يرتجف / when choosing Western or Arabic-Indic digits for a film and a counter that never jitters

**كيف:** font-variant-numeric: tabular-nums; font-feature-settings "tnum" 1, "lnum" 1; Intl.NumberFormat('ar-EG') → ٠–٩, 'ar-SA-u-nu-latn' → 0–9 with Arabic grouping; toLocaleString('ar-EG') for quick Arabic-Indic; codes and dates in mono inside <bdi>; numerals LTR inside RTL; right-align numeric columns.

**المعاملات:** tnum + lnum; one digit system per film

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أرقام هندية · أرقام جدولية · digits · tabular nums · arabic-indic · counter · Intl.NumberFormat · عداد · الأرقام العربية · ثبات الأرقام · number jitter · western digits

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-73` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-earth-ci-fork/ui/ds/tokens.css:304`
- `kosif-earth-ci-fork/ui/components/charts.js:17`
- `kosif-tool/starters/remotion/src/Film.tsx:303`
- `kosif-tool/playbooks/charts.md:190`

#### 7. قدرات قريبة في العائلة

- `ARAB-71` ستايل الكلمات العاطفي / Emotional lyric style preset (install)
- `ARAB-72` العزل الاتجاهي / Bidi isolation (ready)
- `ARAB-74` منسّق الأرقام الهندية الحتمي / Deterministic Arabic-Indic money formatter (proven)
- `ARAB-75` قراءة الأرقام والوحدات العربية / Digit parsing & number/unit detection (ready)

### `ARAB-74` — منسّق الأرقام الهندية الحتمي / Deterministic Arabic-Indic money formatter

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يحوّل المبالغ بالوحدات الصغرى إلى نص مجمّع بعملة وأرقام هندية بلا Intl، بنفس الناتج في Node والمتصفح. / Formats minor-unit amounts into grouped money strings with Arabic-Indic digits and no Intl — identical in Node and browser.

**متى:** حين تعرض مبالغ مالية بأرقام هندية وعملة وتريد نفس النتيجة في Node والمتصفح / when formatting money with Arabic-Indic digits and currency identically in Node and the browser

**كيف:** import { formatMinor, toArabicDigits, formatPercent } from kosif-audit-pro/lib/kosif/format.mjs; formatMinor(minor, {exp:2, arabicDigits:true, currency:'ر.س'}); thousands ','; half-away-from-zero rounding; wrap the result in <bdi> (ARAB-72).

**المعاملات:** digits ٠١٢٣٤٥٦٧٨٩; exp 2; half-away-from-zero

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عملة · أرقام · money · currency · formatter · riyal · deterministic · مبلغ · ريال · تنسيق الأرقام · price format · number formatting

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-74` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-audit-pro/lib/kosif/format.mjs`
- `kosif-audit-pro/tests/kosif-engine.test.mjs:94`

#### 7. قدرات قريبة في العائلة

- `ARAB-72` العزل الاتجاهي / Bidi isolation (ready)
- `ARAB-73` نظام أرقام واحد وأرقام جدولية / One digit system + tabular figures (ready)
- `ARAB-75` قراءة الأرقام والوحدات العربية / Digit parsing & number/unit detection (ready)
- `ARAB-76` صيغ الجمع ومطابقة العدد / Plural & count agreement (ready)

### `ARAB-75` — قراءة الأرقام والوحدات العربية / Digit parsing & number/unit detection

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يحوّل الأرقام الهندية والفارسية إلى لاتينية ويكتشف الرقم ووحدته في سطر السكربت ليحرّكه ستايل العدّاد. / Maps Arabic-Indic and Persian digits to Latin and detects the figure and unit in a script line so a counter can animate it.

**متى:** حين تستخرج الرقم ووحدته من سطر السكربت ليتحرك كعداد أو تحول الأرقام الهندية للاتينية / when detecting a number and unit in a script line for a counter, or mapping Arabic-Indic digits to Latin

**كيف:** MK.latin maps ٠–٩, ۰–۹ and ٫/٬; MK.lineMeta regex picks the first number with units %, ٪, ألف, مليون, مليار, k, M; it also flags questions (؟) and quotes («) so styles can trigger ARAB-45 or a quote card.

**المعاملات:** units %, ٪, ألف, مليون, مليار, k, M

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أرقام · وحدات · مليون · digits · units · parse · counter · statistics · نسبة مئوية · تحويل الأرقام · إحصائيات · number detection · percent

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-75` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `app/public/js/10_studio.js:33`
- `app/public/js/10_studio.js:34`

#### 7. قدرات قريبة في العائلة

- `ARAB-73` نظام أرقام واحد وأرقام جدولية / One digit system + tabular figures (ready)
- `ARAB-74` منسّق الأرقام الهندية الحتمي / Deterministic Arabic-Indic money formatter (proven)
- `ARAB-76` صيغ الجمع ومطابقة العدد / Plural & count agreement (ready)
- `ARAB-77` رقم يتحول إلى عنوان / Number → headline (documented)

### `ARAB-76` — صيغ الجمع ومطابقة العدد / Plural & count agreement

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** العربية لها ست صيغ عددية؛ 1 و2 لهما لفظ خاص، و3–10 جمع، و11 فما فوق مفرد منصوب. / Arabic has six plural categories; 1 and 2 have their own words, 3–10 take the plural, 11+ the singular accusative.

**متى:** حين تكتب نصا يتغير حسب العدد وتحتاج صيغة المفرد أو المثنى أو الجمع الصحيحة / when text changes with a count and needs the right singular, dual or plural form

**كيف:** new Intl.PluralRules('ar').select(n) → zero/one/two/few/many/other, or ICU MessageFormat; UI rule: n=1 singular phrase, n=2 dual ('تعديلان بانتظار الإرسال'), 3–10 plural, ≥11 'N تعديلاً'; translation is meaning-based, glossary first, keeping {{vars}} and HTML.

**المعاملات:** 6 CLDR forms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** جمع · مثنى · عدد · plural · PluralRules · localization · i18n · dual · تمييز العدد · صيغة الجمع · ترجمة الواجهة · pluralization · count text

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-76` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:571`
- `kosif-atlas/skills/2329-localization-i18n-engineering/8940-i18n-foundations-and-icu/SKILL.md`
- `100-superskills/skills/translation-localization-ar/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-74` منسّق الأرقام الهندية الحتمي / Deterministic Arabic-Indic money formatter (proven)
- `ARAB-75` قراءة الأرقام والوحدات العربية / Digit parsing & number/unit detection (ready)
- `ARAB-77` رقم يتحول إلى عنوان / Number → headline (documented)
- `ARAB-78` حوار طباعي / Typographic dialogue (documented)

### `ARAB-77` — رقم يتحول إلى عنوان / Number → headline

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إحصائية كبيرة تعدّ ثم تتنحى لتفسح للجملة الشارحة بوحدتها ومصدرها الصغير. / A big statistic counts up, then steps aside for the explanatory sentence with its unit and a small source.

**متى:** حين تريد إحصائية كبيرة تعد ثم تتنحى لجملة تشرحها مع الوحدة والمصدر / when a big statistic should count up, then step aside for the sentence explaining it

**كيف:** 0–1.5 s the number counts up in tabular digits of the chosen system, 1.5–2.5 s it moves aside, 2.5–5 s the sentence mask-reveals (ARAB-19) with unit and source line; never invent a number. The infographic reference shows the counter side: odometer columns where lower digits spin more turns, hero number at 12–15% of height.

**المعاملات:** 5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** رقم · إحصائية · عداد · statistic · counter · headline · MG-019 · رقم متحرك · عد تصاعدي · أرقام كبيرة · count up · stat reveal

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-77` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`
- `style:infographic`

#### 7. قدرات قريبة في العائلة

- `ARAB-75` قراءة الأرقام والوحدات العربية / Digit parsing & number/unit detection (ready)
- `ARAB-76` صيغ الجمع ومطابقة العدد / Plural & count agreement (ready)
- `ARAB-78` حوار طباعي / Typographic dialogue (documented)
- `ARAB-79` الدعوة والسعر بالعربية / Arabic CTA & price isolation (documented)

### `ARAB-78` — حوار طباعي / Typographic dialogue

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سؤال يستقر على اليمين ثم ينسحب قليلًا ويدخل الجواب من الجهة المقابلة بلون ثانٍ. / A question settles on the right, withdraws slightly, and the answer enters from the other side in a second colour.

**متى:** حين تعرض سؤالا وجوابه نصا متحركا بجهتين ولونين / when showing a question and its answer as type on opposite sides in two colours

**كيف:** 0–2 s question, 2–2.6 s transition, 2.6–6 s answer with enough reading delay; two layers, two masks, alternating positions; never present an illustrative example as a real quote.

**المعاملات:** 6 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حوار · سؤال وجواب · dialogue · q&a · two voices · MG-020 · محادثة · سؤال وإجابة · صوتين · conversation · question answer

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-78` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-76` صيغ الجمع ومطابقة العدد / Plural & count agreement (ready)
- `ARAB-77` رقم يتحول إلى عنوان / Number → headline (documented)
- `ARAB-79` الدعوة والسعر بالعربية / Arabic CTA & price isolation (documented)
- `ARAB-80` تسميات عربية مُسقطة على الخرائط والعوالم / Projected Arabic labels (maps · isometric · charts) (install)

### `ARAB-79` — الدعوة والسعر بالعربية / Arabic CTA & price isolation

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الدعوة بفعل أمر، ونظام أرقام واحد، والعملة والرقم في وسم معزول واحد. / CTAs use an imperative verb, one digit system, and currency + number in one isolated span.

**متى:** حين تكتب دعوة لاتخاذ إجراء أو سعرا بالعربية في إعلان أو بطاقة نهاية / when writing an Arabic call to action or price in an ad or end card

**كيف:** Verbs: اشترك، حمّل، اطلب؛ <bdi>٤٩ ر.س</bdi>; end-card CTA 'تابعنا للمزيد' (ARAB-49).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** دعوة · سعر · cta · price · ad · bdi · اشترك · عملة · إعلان · call to action · end card

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-79` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/playbooks/ads.md:77`

#### 7. قدرات قريبة في العائلة

- `ARAB-77` رقم يتحول إلى عنوان / Number → headline (documented)
- `ARAB-78` حوار طباعي / Typographic dialogue (documented)
- `ARAB-80` تسميات عربية مُسقطة على الخرائط والعوالم / Projected Arabic labels (maps · isometric · charts) (install)
- `ARAB-81` إصلاح أسماء الملفات العربية المشوّهة / Arabic file-name mojibake repair (proven)

### `ARAB-80` — تسميات عربية مُسقطة على الخرائط والعوالم / Projected Arabic labels (maps · isometric · charts)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** التسميات عناصر HTML تُوضع كل إطار بإسقاط إحداثياتها على الشاشة، فتأخذ خط الفيلم العربي كاملًا. / Labels are HTML elements placed each frame by projecting their coordinates, so they get the film's full Arabic typography.

**متى:** حين تضع أسماء عربية على خريطة أو عالم أيزومتري أو رسم بياني بخط الفيلم / when placing Arabic labels on a map, isometric world or chart in the film's typography

**كيف:** Per frame p = map.project([lng, lat]) → {x, y, reveal}; absolutely positioned divs in the film's Arabic font, rise-and-fade ~0.7 s with an accent rule, pointer-events none; on a fixed plate apply the same translate/scale to label positions. Inside MapLibre symbol layers Arabic needs the RTL text plugin and Arabic glyph PBFs — overlays are safer. SVG worlds: HTML layer above the SVG, positioned by projecting world points; avoid SVG <text> with text-anchor end + rtl (misplaces). Charts: Arabic family on Arabic labels, measure with the real font, ≥24 px at 1080p, decide axis mirroring and digit style once.

**المعاملات:** label reveal ~0.7 s; ≥24 px at 1080p

**التثبيت:** npm i maplibre-gl

**الوسوم:** خريطة · تسميات · map labels · maplibre · isometric · projection · chart labels · أسماء الأماكن · خرائط · عناوين على الخريطة · geo labels · label placement

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:maplibre` ← npm ls maplibre أو وجود node_modules/maplibre
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-80` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-explainer-architecture.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/TECHNIQUE.md`
- `kosif-atlas/skills/345-visuals/1242-html-diagram/references/svg-primitives.md`
- `style:isometric`

#### 7. قدرات قريبة في العائلة

- `ARAB-78` حوار طباعي / Typographic dialogue (documented)
- `ARAB-79` الدعوة والسعر بالعربية / Arabic CTA & price isolation (documented)
- `ARAB-81` إصلاح أسماء الملفات العربية المشوّهة / Arabic file-name mojibake repair (proven)
- `ARAB-82` سطر الحقوق الآمن / Safe credit-line burn (ready)

### `ARAB-81` — إصلاح أسماء الملفات العربية المشوّهة / Arabic file-name mojibake repair

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يستعيد أسماء الملفات العربية التي تصل بترميز خاطئ ولا يقبل التخمين إلا إذا أنتج حرفين عربيين على الأقل. / Restores Arabic upload names that arrive mis-decoded, accepting a guess only if it yields at least two Arabic letters.

**متى:** حين تصل أسماء ملفات عربية مرفوعة برموز غريبة أو ترميز خاطئ / when uploaded Arabic file names arrive garbled or mis-decoded

**كيف:** server._unmojibake(): tries (latin-1→utf-8), (cp1252→utf-8), (latin-1→cp1256); then _safe_name() keeps word chars, '-', '.', space, the Arabic block U+0600–06FF and parentheses.

**المعاملات:** ≥2 Arabic letters to accept

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ترميز · أسماء الملفات · mojibake · encoding · cp1256 · upload · رموز غريبة · حروف مشوهة · اسم الملف · garbled filename · utf-8

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-81` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:77`
- `100-superskills/skills/kosif-montage-motion/tests/test_web.py:235`

#### 7. قدرات قريبة في العائلة

- `ARAB-79` الدعوة والسعر بالعربية / Arabic CTA & price isolation (documented)
- `ARAB-80` تسميات عربية مُسقطة على الخرائط والعوالم / Projected Arabic labels (maps · isometric · charts) (install)
- `ARAB-82` سطر الحقوق الآمن / Safe credit-line burn (ready)
- `ARAB-83` تسمية الألوان بالعربية / Arabic colour naming (ready)

### `ARAB-82` — سطر الحقوق الآمن / Safe credit-line burn

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يضيف اسم صاحب المادة صغيرًا أسفل الفيديو من ملف نصي، فلا يدخل نص غير موثوق إلى قواعد مرشحات ffmpeg. / Adds the source creator's credit small at the bottom from a text file, so untrusted text never enters the ffmpeg filter grammar.

**متى:** حين تضيف اسم صاحب المادة صغيرا أسفل الفيديو دون إدخال نص غير موثوق في فلاتر ffmpeg / when burning a small source credit at the bottom without untrusted text entering ffmpeg filters

**كيف:** reel --credit 'insta: name' → drawtext textfile=…, ≤300 chars, fontsize 1.3% H, white@0.5, y = 0.905·h. Latin handles only: drawtext here shapes Arabic through FriBiDi presentation forms and shows tofu with modern fonts (verified) — burn an Arabic credit as a one-line ASS event (ARAB-58/62) instead.

**المعاملات:** 1.3% H; white@0.5; y 0.905h; ≤300 chars

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حقوق · credit · drawtext · textfile · safe · attribution · نسب المحتوى · اسم صاحب المقطع · ذكر المصدر · creator credit · ffmpeg

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-82` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-studio/motion/reel.py:163`

#### 7. قدرات قريبة في العائلة

- `ARAB-80` تسميات عربية مُسقطة على الخرائط والعوالم / Projected Arabic labels (maps · isometric · charts) (install)
- `ARAB-81` إصلاح أسماء الملفات العربية المشوّهة / Arabic file-name mojibake repair (proven)
- `ARAB-83` تسمية الألوان بالعربية / Arabic colour naming (ready)
- `ARAB-84` التقاط ستايل النص وإعادة تركيبه / Text-style capture & compositing (proven)

### `ARAB-83` — تسمية الألوان بالعربية / Arabic colour naming

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يعطي أي لون اسمًا عربيًا تقريبيًا (الأحمر الداكن، الأخضر الزيتي، الكريمي…) من تدرجه وتشبعه وقيمته. / Gives any RGB colour a rough Arabic name (dark red, olive green, cream…) from hue, saturation and value.

**متى:** حين تحتاج اسما عربيا تقريبيا لأي لون مثل الأحمر الداكن أو الأخضر الزيتي / when you need a rough Arabic name for any RGB colour, like dark red or olive green

**كيف:** vectorize.name_ar(rgb); HSV thresholds: s < .14 or v < .12 → neutral; hue bands at 15/45/62/165/260/300/340°.

**المعاملات:** hue bands 15/45/62/165/260/300/340

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أسماء الألوان · colour names · palette · hsv · labels · اسم اللون · ألوان · وصف اللون · color name · rgb

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-83` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-studio/vectorize.py:105`

#### 7. قدرات قريبة في العائلة

- `ARAB-81` إصلاح أسماء الملفات العربية المشوّهة / Arabic file-name mojibake repair (proven)
- `ARAB-82` سطر الحقوق الآمن / Safe credit-line burn (ready)
- `ARAB-84` التقاط ستايل النص وإعادة تركيبه / Text-style capture & compositing (proven)
- `ARAB-85` قياس حركة النص وتصنيفها / Text-animation measurement & replay (ready)

### `ARAB-84` — التقاط ستايل النص وإعادة تركيبه / Text-style capture & compositing

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يقيس لون التعبئة وسماكة الحد والظل والتوهج والصندوق والمحاذاة لنص المرجع ثم يركّب النص الجديد بنفس الشكل. / Measures fill, outline, shadow, glow, box and alignment of reference text and composes new text with the same look.

**متى:** حين تريد كتابة نص جديد بنفس شكل نص في فيديو مرجعي من لون وحد وظل وتوهج / when composing new text with the same fill, outline, shadow and glow as text in a reference

**كيف:** mm_text style pass (consensus medians over events; OCR draft with Arabic tessdata only when tesseract exists — it does not here) → mm_render_text.compose(alpha, style) → RGBA with fill/outline/shadow (dx, dy, blur, opacity)/glow/box. mimic.json text_style {font, size as frame fraction, color, stroke, stroke_color, shadow, anim, fade, line_height, align, fit_width, engine:'browser'}; texts[] with start/end and x/y centre fractions (line h = bbox h / lines / 1.3). Example study: Diwani at 0.08 H (135 px at 1920), #fdfbf3, stroke 7 #000000, fade .35 s, lh 1.25.

**المعاملات:** stroke ~7 px at 1080; anim fade\|rise\|drop\|slide-left\|slide-right\|none

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** محاكاة · ستايل النص · mimic · text style · outline · shadow · reference · تقليد الستايل · نفس شكل النص · حد النص · copy text style · glow

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `tesseract` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-84` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/mimic/mm_text.py`
- `kosif-tool/.claude/skills/kosif-superpowers/scripts/mimic/mm_render_text.py`
- `kosif-one/projects/mimic-jumuah/study/mimic.json`
- `100-superskills/skills/kosif-montage-motion/references/mimic.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-82` سطر الحقوق الآمن / Safe credit-line burn (ready)
- `ARAB-83` تسمية الألوان بالعربية / Arabic colour naming (ready)
- `ARAB-85` قياس حركة النص وتصنيفها / Text-animation measurement & replay (ready)
- `ARAB-86` مطابقة الخط بالحبر / Font matching by ink (ready)

### `ARAB-85` — قياس حركة النص وتصنيفها / Text-animation measurement & replay

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يجد أحداث النص في المرجع ويقيس دخولها وخروجها ويصنّفها إلى 11 نوعًا، ثم يعيد تشغيل المنحنى نفسه بالخط المطابق. / Finds text events in a reference, measures entrance/exit, classifies 11 kinds and replays the same curve in the matched font.

**متى:** حين تريد معرفة كيف يدخل النص ويخرج في فيديو مرجعي وإعادة نفس الحركة / when measuring how text enters and exits in a reference video and replaying the same curve

**كيف:** mm_text.analyze_text measures visibility, displacement, scale, sharpness and per-word onsets → classify_anim; mm_textfx.EventLayer replays the normalised alpha/offset/scale/blur/word curves frame by frame. Kinds: cut, words, slide_up, slide_down, slide_left, slide_right, pop (overshoot > 1.03), zoom_in, zoom_out, blur, fade. Imports checked here (numpy + Pillow + ffmpeg; OpenCV optional and absent).

**المعاملات:** 11 kinds; pop when scale overshoot > 1.03

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قياس الحركة · تصنيف · measure · classify · text animation · mimic · replay · تحليل المرجع · حركة النص · تقليد الحركة · reference analysis · copy animation

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:numpy` ← python3 -c "import numpy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:opencv` ← python3 -c "import opencv" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-85` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/mimic/mm_text.py`
- `kosif-tool/.claude/skills/kosif-superpowers/scripts/mimic/mm_textfx.py`

#### 7. قدرات قريبة في العائلة

- `ARAB-83` تسمية الألوان بالعربية / Arabic colour naming (ready)
- `ARAB-84` التقاط ستايل النص وإعادة تركيبه / Text-style capture & compositing (proven)
- `ARAB-86` مطابقة الخط بالحبر / Font matching by ink (ready)
- `ARAB-87` ملاءمة العرض والتصغير التلقائي / Fit-width & shrink-to-fit (ready)

### `ARAB-86` — مطابقة الخط بالحبر / Font matching by ink

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يكتب النص نفسه بكل خط في المكتبة ويقارنه بحبر المرجع (النسبة، التقاطع المتسامح، سماكة الضربة) ويرتب النتائج في ورقة. / Renders the same text in every library face and ranks them against the reference ink (aspect, tolerant IoU, stroke thickness) on a sheet.

**متى:** حين تريد معرفة الخط المستخدم في مرجع ومطابقته من مكتبة الخطوط / when identifying which library font best matches the text in a reference

**كيف:** mm_fonts.match('work') at NORM_H 64 → spec.texts[i].font + sheets/fonts_evNN.png; mimic fonts PROJECT/study → fonts.jpg to pick visually (Naskh/Thuluth/Kufi/Diwani). Top scores are often close (≈0.334–0.339 in the Friday study) — always confirm on the sheet.

**المعاملات:** NORM_H 64

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مطابقة الخط · font matching · font id · ink · iou · mimic · ما هذا الخط · تعرف على الخط · خط مشابه · identify font · similar font

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-86` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/mimic/mm_fonts.py`
- `kosif-one/projects/mimic-jumuah/study/mimic.json`

#### 7. قدرات قريبة في العائلة

- `ARAB-84` التقاط ستايل النص وإعادة تركيبه / Text-style capture & compositing (proven)
- `ARAB-85` قياس حركة النص وتصنيفها / Text-animation measurement & replay (ready)
- `ARAB-87` ملاءمة العرض والتصغير التلقائي / Fit-width & shrink-to-fit (ready)
- `ARAB-88` نص مشكّل في المشاهد المرسومة واستيراد SVG / Shaped text in painted scenes & SVG import (documented)

### `ARAB-87` — ملاءمة العرض والتصغير التلقائي / Fit-width & shrink-to-fit

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حجم واحد يجعل أطول سطر يملأ 96% من العرض، أو تصغير تدريجي حتى يدخل النص في عدد أسطر محدد. / One shared size so the longest line fills 96% of the width, or stepwise shrinking until text fits a row budget.

**متى:** حين يكون النص أطول من المساحة وتريد تصغيره تلقائيا ليدخل في العرض أو عدد أسطر محدد / when text is too long and must auto-shrink to fill the width or fit a row budget

**كيف:** mimic text_style.fit_width .96; Basma TX.layout lays rows RTL from the right (space × 1.08, per-word centre x) and TX.fitLayout multiplies size by 0.9 up to 14 times until rows ≤ maxRows, lh 1.42·size; wbcompat textfit shrinks 1 px at a time to 84% width (min 9 px) then truncates; carousels stop at 4 lines.

**المعاملات:** fit .96; ×0.9 ×14; lh 1.42; 84% width

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ملاءمة · تصغير · fit text · shrink to fit · layout · rows · النص طويل · تصغير الخط · عدد الأسطر · auto size · text overflow

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-87` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:268`
- `app/public/js/10_studio.js:182`
- `100-superskills/skills/kosif-montage-motion/references/mimic.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-85` قياس حركة النص وتصنيفها / Text-animation measurement & replay (ready)
- `ARAB-86` مطابقة الخط بالحبر / Font matching by ink (ready)
- `ARAB-88` نص مشكّل في المشاهد المرسومة واستيراد SVG / Shaped text in painted scenes & SVG import (documented)
- `ARAB-89` طبقات نص عربي على Canvas / Canvas RTL text-layer helpers (ready)

### `ARAB-88` — نص مشكّل في المشاهد المرسومة واستيراد SVG / Shaped text in painted scenes & SVG import

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عملية نص في استوديو الرسم ترسم العربية بحجم الإخراج (حادة حتى 4K) بتعبئة متدرجة، وتستورد ‎<text>‎ من SVG. / A painter-scene text op drawing Arabic at output size (sharp to 4K) with gradient fills, plus SVG <text> import.

**متى:** حين تكتب نصا عربيا داخل مشهد مرسوم في استوديو الرسم أو تستورد نصوص SVG / when drawing Arabic text in a painter scene at output size or importing SVG text

**كيف:** text(s, x, y, size, colour\|gradient, anchor 'ms'\|'mm'\|'ls'\|'rs', bold, family 'sans'\|'serif'\|'mono', alpha, mode), supersampled; SVG <text>/<tspan> import honours font-size, text-anchor, weight ≥600 and gradient fills (first stop). Caveat in this container: its font table points at Windows files (Segoe UI/Arial/Tahoma) and falls back to Pillow's default font on Linux — map it to an OFL Arabic file before trusting it.

**المعاملات:** anchors ms/mm/ls/rs; weight ≥600 → bold

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مشهد مرسوم · svg · painter · vector scene · gradient text · pillow · نص على الرسم · استيراد svg · رسم · svg text · 4k text

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-88` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-studio/render.py:446`
- `kosif-studio/svg_import.py:369`
- `kosif-studio/scenes/ad_whole_sheep.py:99`
- `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-86` مطابقة الخط بالحبر / Font matching by ink (ready)
- `ARAB-87` ملاءمة العرض والتصغير التلقائي / Fit-width & shrink-to-fit (ready)
- `ARAB-89` طبقات نص عربي على Canvas / Canvas RTL text-layer helpers (ready)
- `ARAB-90` دوران كتلة النص 90° ككاميرا / Type-block 90° rotation as camera move (idea)

### `ARAB-89` — طبقات نص عربي على Canvas / Canvas RTL text-layer helpers

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** دوال ترسم العربية كلمات كاملة باتجاه تلقائي وحدّ وشفافية، وطبقات نص بنسب من الإطار حتى 5 أسطر. / Helpers that draw Arabic as whole words with auto direction, stroke and alpha, plus text layers sized in frame percentages up to 5 lines.

**متى:** حين ترسم نصا عربيا على Canvas بكلمات كاملة وحد وشفافية أو طبقات نص بنسب الإطار / when drawing Arabic on Canvas as whole words with stroke and alpha, or frame-relative text layers

**كيف:** U.text(str, x, y, size, color, {font, weight, align, alpha, stroke}) sets ctx.direction='rtl' when Arabic is detected, round-joined stroke; U.width() measures (default Lalezar → Cairo). Studio layer: weight 700, textAlign center, shadow #0009 blur 15, ≤5 lines split on \n at lh 1.35·size, max width 91%, ≤180 chars, size 2–60% of the short side (default 7%), x/y 0–100%. Playbook: ctx.textAlign='right' + fillText(wholeString) — the browser shapes it.

**المعاملات:** ≤5 lines; lh 1.35; max width 91%; size 2–60%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** canvas · طبقة نص · text layer · fillText · rtl · editor · كتابة على الكانفاس · حد النص · شفافية · text stroke · canvas text

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-89` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:76`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:158`
- `app/public/js/00_editor.js:17`
- `kosif-tool/playbooks/arabic-typography.md:65`

#### 7. قدرات قريبة في العائلة

- `ARAB-87` ملاءمة العرض والتصغير التلقائي / Fit-width & shrink-to-fit (ready)
- `ARAB-88` نص مشكّل في المشاهد المرسومة واستيراد SVG / Shaped text in painted scenes & SVG import (documented)
- `ARAB-90` دوران كتلة النص 90° ككاميرا / Type-block 90° rotation as camera move (idea)
- `ARAB-91` مصمم: نص عربي قابل للتعديل بتشكيل HarfRust وكشيدة / Mosamem: editable Arabic text with HarfRust shaping and kashida justification (install)

### `ARAB-90` — دوران كتلة النص 90° ككاميرا / Type-block 90° rotation as camera move

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تدور كتلة النص العربي كلها 90° كأن الكاميرا انقلبت، ويُكمل السطر التالي على المحور الجديد. / The whole Arabic text block rotates 90° as if the camera rolled, and the next line continues on the new axis.

**متى:** حين تريد انتقالا تدور فيه كتلة النص العربي 90 درجة كأن الكاميرا انقلبت / when the whole Arabic text block should rotate 90° like a camera roll into the next line

**كيف:** Untested idea from a brief: rotate the block (never single letters) 90° with a band of background at 60% to hide the turn; lay the next line out on the rotated axis; keep each word whole.

**المعاملات:** 90°; band = bg at 60%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** دوران · كاميرا · rotation · camera roll · transition · type block · انتقال · ترانزيشن · تدوير النص · rotate text · text transition

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-90` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/styles/pm-zheke-38deff/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-88` نص مشكّل في المشاهد المرسومة واستيراد SVG / Shaped text in painted scenes & SVG import (documented)
- `ARAB-89` طبقات نص عربي على Canvas / Canvas RTL text-layer helpers (ready)
- `ARAB-91` مصمم: نص عربي قابل للتعديل بتشكيل HarfRust وكشيدة / Mosamem: editable Arabic text with HarfRust shaping and kashida justification (install)
- `ARAB-92` أربعة خطوط عربية مفتوحة يرفقها مصمم / Four open Arabic fonts bundled by Mosamem (IBM Plex Sans Arabic, Cairo, Tajawal, Amiri) (documented)

### `ARAB-91` — مصمم: نص عربي قابل للتعديل بتشكيل HarfRust وكشيدة / Mosamem: editable Arabic text with HarfRust shaping and kashida justification

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `receipt` |
| الرخصة | GPL-3.0-or-later (Mosamem; link only, no code copied); HarfRust MIT/Apache-2.0 |

**ما هي:** محرك نص يشكّل العربية بـ HarfRust (أشكال الاتصال، لام ألف، التشكيل)، ويخلط العربية واللاتينية باتجاه صحيح، ويعكس الأقواس، ويضبط بالكشيدة، ويستعير الحرف الناقص من خط مرفق آخر؛ اختبارات التشكيل الذهبية نجحت هنا. — HarfRust shaping (joining forms, lam-alef, stacked marks), correct mixed Arabic/Latin order, mirrored brackets, kashida justification and fallback between bundled fonts; its shaping goldens passed here.

**متى:** كتابة عربية صحيحة على صورة أو تصميم / correct Arabic text on an image or design

**كيف:** In the app: the Text tool keeps text editable. Evidence: the 13 text tests (lam_alef_becomes_a_ligature, letters_take_their_joining_forms, justification_with_spaces_and_with_kashida, mixed_arabic_and_latin_read_correctly, diacritics_stack_and_nothing_is_missing …) passed in `cargo test -p mosamem-core`. For rendering inside this repo use the existing KOSIF Arabic text routes (HarfBuzz/Pillow-raqm); link Mosamem, do not copy its code.

**التثبيت:** Mosamem app, or Rust toolchain to run its tests

**الوسوم:** harfrust · shaping · تشكيل · kashida · كشيدة · arabic text · نص عربي · bidi · mosamem · مصمم

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-91` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `run here 2026-10-22: cargo test -p mosamem-core on Mosamem becfbe8 (outside the repo, cargo 1.97.0) → 95 passed, 0 failed (86 unit incl. 13 text shaping/layout goldens, 9 blend-formula); offline attempt failed (crates not cached)`
- `https://github.com/motalim-ai/mosamem`

#### 7. قدرات قريبة في العائلة

- `ARAB-89` طبقات نص عربي على Canvas / Canvas RTL text-layer helpers (ready)
- `ARAB-90` دوران كتلة النص 90° ككاميرا / Type-block 90° rotation as camera move (idea)
- `ARAB-92` أربعة خطوط عربية مفتوحة يرفقها مصمم / Four open Arabic fonts bundled by Mosamem (IBM Plex Sans Arabic, Cairo, Tajawal, Amiri) (documented)
- `ARAB-U01` خط El Messiri العربي مضمّن / El Messiri Arabic display font bundled (OFL) (proven)

### `ARAB-92` — أربعة خطوط عربية مفتوحة يرفقها مصمم / Four open Arabic fonts bundled by Mosamem (IBM Plex Sans Arabic, Cairo, Tajawal, Amiri)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | SIL OFL 1.1 |

**ما هي:** IBM Plex Sans Arabic وCairo وTajawal وAmiri، كلها برخصة SIL OFL 1.1، ويمكن جلبها من مستودعاتها الأصلية لا من مصمم. — All four are SIL OFL 1.1; fetch them from their own upstream repositories, not from Mosamem.

**متى:** اختيار خط عربي مفتوح الرخصة / pick an openly licensed Arabic font

**كيف:** Upstreams: github.com/IBM/plex, github.com/Gue3bara/Cairo, github.com/googlefonts/tajawal, github.com/aliftype/amiri. Keep each OFL.txt with the font file. The every_bundled_font_loads_and_weights_resolve test passed in the Mosamem cargo run.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خطوط عربية · arabic fonts · cairo · tajawal · amiri · plex · ofl

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-92` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `https://github.com/motalim-ai/mosamem/blob/main/THIRD-PARTY-NOTICES.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-90` دوران كتلة النص 90° ككاميرا / Type-block 90° rotation as camera move (idea)
- `ARAB-91` مصمم: نص عربي قابل للتعديل بتشكيل HarfRust وكشيدة / Mosamem: editable Arabic text with HarfRust shaping and kashida justification (install)
- `ARAB-U01` خط El Messiri العربي مضمّن / El Messiri Arabic display font bundled (OFL) (proven)
- `ARAB-X01` كشف الكلمة العربية كاملة من اليمين / RTL whole-word lyric reveal with key-word pop (documented)

### `ARAB-U01` — خط El Messiri العربي مضمّن / El Messiri Arabic display font bundled (OFL)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | SIL OFL 1.1 |

**ما هي:** El Messiri متغير (Regular–Bold، v2.020) مضمّن في proofs/_shared/fonts مع OFL-ElMessiri.txt؛ رسمتُه بتشكيل raqm صحيح في إثبات الرفع. خط عرض عربي أنيق للعناوين والأفلام الغنائية. — Elegant Arabic display face for titles and lyric films.

**متى:** عنوان عربي أنيق أو فيلم أغنية / an elegant Arabic title or lyric film

**كيف:** ImageFont.truetype('proofs/_shared/fonts/ElMessiri[wght].ttf', size) مع direction='rtl', language='ar'

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** el messiri · المسيري · messiri · مسيري · ofl

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-U01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/_shared/fonts/ElMessiri[wght].ttf`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/_shared/fonts/OFL-ElMessiri.txt`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/owner-uploads-20261023/sheet.jpg`

#### 7. قدرات قريبة في العائلة

- `ARAB-91` مصمم: نص عربي قابل للتعديل بتشكيل HarfRust وكشيدة / Mosamem: editable Arabic text with HarfRust shaping and kashida justification (install)
- `ARAB-92` أربعة خطوط عربية مفتوحة يرفقها مصمم / Four open Arabic fonts bundled by Mosamem (IBM Plex Sans Arabic, Cairo, Tajawal, Amiri) (documented)
- `ARAB-X01` كشف الكلمة العربية كاملة من اليمين / RTL whole-word lyric reveal with key-word pop (documented)
- `ARAB-X02` ترشيح الخط لا الجزم به / Font matches are candidates, not identities (documented)

### `ARAB-X01` — كشف الكلمة العربية كاملة من اليمين / RTL whole-word lyric reveal with key-word pop

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner (song audio and lyrics are third-party; not included) |

**ما هي:** كل كلمة عربية تنكشف كاملة بقناع يتحرك من اليمين إلى اليسار قبل نطقها بقليل، والكلمة المفتاحية أكبر وتنبض وتلمع بذهب متحرك. — Each Arabic word is revealed whole by a mask moving right to left just before it is sung; the key word is larger, pops and carries a moving gold sheen.

**متى:** فيلم كلمات أغنية أو شعر عربي — an Arabic lyric or poetry film.

**كيف:** canvas direction = 'rtl'; a clip rect grows right → left with an eOut3 curve over 0.5 s, starting 0.1 s before the word; rise 34 px; key word ×1.3 with a decaying pop 1 + 0.08·e^(−Δt/0.35) and a moving gold gradient; the active word gets an additive glow; exit with blur ≤ 10 px and rising seeded gold sparks. Letters are never split, so Arabic joining survives.

**المعاملات:** mask 0.5 s from −0.1 s; rise 34 px; key ×1.3, pop 0.08·e^(−Δt/0.35)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** arabic · rtl · lyrics · mask reveal · كلمات عربية · كشف · قناع

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-X01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `owner-upload:film_project/film/film.js`

#### 7. قدرات قريبة في العائلة

- `ARAB-92` أربعة خطوط عربية مفتوحة يرفقها مصمم / Four open Arabic fonts bundled by Mosamem (IBM Plex Sans Arabic, Cairo, Tajawal, Amiri) (documented)
- `ARAB-U01` خط El Messiri العربي مضمّن / El Messiri Arabic display font bundled (OFL) (proven)
- `ARAB-X02` ترشيح الخط لا الجزم به / Font matches are candidates, not identities (documented)
- `ARAB-X03` الزخرفة والكشيدة للنبذة فقط / Unicode ornaments and kashida: bios only (documented)

### `ARAB-X02` — ترشيح الخط لا الجزم به / Font matches are candidates, not identities

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `session` |
| الرخصة | owner |

**ما هي:** عند تقليد فيديو لا تقل «هذا الخط هو X» دون دليل؛ قدّم مرشحين بدرجة ثقة، وتأكد من الاحتياطي اللاتيني كي لا تظهر مربعات فارغة. — When imitating a video never state 'this font is X' without evidence; offer ranked candidates, and make sure there is a Latin fallback so no empty boxes appear.

**متى:** محاكاة فيديو مرجعي أو مطابقة هوية بصرية — imitating a reference video or matching a visual identity.

**كيف:** Report font candidates with evidence (shapes compared, sample frames); shape Arabic through HarfBuzz/RAQM; check mixed Arabic + Latin + digits in every label. Lesson from the owner's catalog renderer: a single Arabic font with no Latin fallback drew tofu boxes for 'Parallax', 'BPM', 'WebGL' inside Arabic labels.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** font matching · fallback · tofu · imitation · مطابقة الخط · خط احتياطي

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-X02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `owner-upload:KOSIF_SEE_Humanizer_Optimize_Graphify_v1.7.5/skills/kosif-see/references/VIDEO_IMITATION_ROUTING_V1.md`
- `session-2026-10-16:see-atlas#11.7`

#### 7. قدرات قريبة في العائلة

- `ARAB-U01` خط El Messiri العربي مضمّن / El Messiri Arabic display font bundled (OFL) (proven)
- `ARAB-X01` كشف الكلمة العربية كاملة من اليمين / RTL whole-word lyric reveal with key-word pop (documented)
- `ARAB-X03` الزخرفة والكشيدة للنبذة فقط / Unicode ornaments and kashida: bios only (documented)
- `ARAB-X04` مطابقة الخط عبر محرك تشكيل حقيقي / Font matching through a real shaper (Chromium/HarfBuzz) (proven)

### `ARAB-X03` — الزخرفة والكشيدة للنبذة فقط / Unicode ornaments and kashida: bios only

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `session` |
| الرخصة | owner |

**ما هي:** النص المزخرف بالرموز والمطوّل بالكشيدة يصلح لنبذة حساب، لكنه يكسر تشكيل الحروف العربية في الفيديو المرندر. — Ornament-wrapped and kashida-stretched text is fine for a social bio but breaks Arabic shaping in rendered video.

**متى:** طلب «زخرفة اسم» أو نص مزين لمنصة — a request to 'decorate a name' or style text for a platform.

**كيف:** Generate decorated bio text inline when asked (frames, stars, crescents, kashida), but in motion graphics animate real words with real fonts and stretch with font features or layout, never with tatweel characters. This is the useful core of the owner's 150 text-decoration methods (30 base styles × 5 variants).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** kashida · decoration · unicode · bio · كشيدة · زخرفة · تطويل

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-X03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `session-2026-10-16:motion-leftovers#5`
- `owner-upload:kosif-tool-ultra/kosif-500-methods.json`

#### 7. قدرات قريبة في العائلة

- `ARAB-X01` كشف الكلمة العربية كاملة من اليمين / RTL whole-word lyric reveal with key-word pop (documented)
- `ARAB-X02` ترشيح الخط لا الجزم به / Font matches are candidates, not identities (documented)
- `ARAB-X04` مطابقة الخط عبر محرك تشكيل حقيقي / Font matching through a real shaper (Chromium/HarfBuzz) (proven)
- `ARAB-X05` تجميع عائلة خط مطابقة من مصدرين OFL / Assemble a matched OFL family from two masters (proven)

### `ARAB-X04` — مطابقة الخط عبر محرك تشكيل حقيقي / Font matching through a real shaper (Chromium/HarfBuzz)

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اعرض سطور المرجع نفسها بكل خط مفتوح مرشّح عبر Chromium (الخط مضمّن كـ data URL) وقارنها بقصاصات الفيديو جنبًا إلى جنب؛ القرار بالبصمات (المركّبات المتراكبة «جم» و«محمد»، شكل ﷺ، الكاف والتاء المربوطة) لا بتقاطع الظلال. — Render the reference lines in every open candidate through headless Chromium and compare side-by-side sheets; decide by letterform signatures (stacked جم/محمد, the ﷺ form, kaf/taa-marbuta), not by silhouette IoU.

**متى:** حين يستخدم المرجع خطًا عربيًا مجهولًا وعليك اختيار أقرب خط مفتوح بأمانة. / a reference uses an unknown Arabic face and you must pick the closest open font honestly

**كيف:** `node .claude/skills/kosif-superpowers/scripts/render_text.cjs spec.json out/` with spec items {text, font, weight, size, variation}; build sheets with Pillow (video crop on top, candidates below at equal width); width ratios between lines are tie-breakers only because kashida and shadows distort them. Method and pitfalls in references/font-matching.md. Verified on the Friday-greeting reference: Amiri Bold matched; Scheherazade/Noto set the ligatures flat.

**المعاملات:** size 48–120 px; fonts as data URLs (file:// fails under setContent)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مطابقة الخط · font matching · harfbuzz · chromium · signatures · amiri · تشكيل

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-X04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/render_text.cjs`
- `kosif-tool/.claude/skills/kosif-superpowers/references/font-matching.md`
- `kosif-tool/fonts/kosif-jumuah/README.md`

#### 7. قدرات قريبة في العائلة

- `ARAB-X02` ترشيح الخط لا الجزم به / Font matches are candidates, not identities (documented)
- `ARAB-X03` الزخرفة والكشيدة للنبذة فقط / Unicode ornaments and kashida: bios only (documented)
- `ARAB-X05` تجميع عائلة خط مطابقة من مصدرين OFL / Assemble a matched OFL family from two masters (proven)
- `ARAB-X06` عنوان خطي مركّب من حدود حروف مفتوحة / Composed calligraphic title from OFL outlines (proven)

### `ARAB-X05` — تجميع عائلة خط مطابقة من مصدرين OFL / Assemble a matched OFL family from two masters

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | OFL-1.1 (sources and result) |

**ما هي:** حين تأتي العربية والأرقام من تصميمين مختلفين: اقتطع كل مصدر إلى نطاقات يونيكود منفصلة، ثبّت الأوزان من الخط المتغيّر، وحّد وحدات القياس والمقاييس الرأسية، ادمج بـ fontTools، وسمِّ العائلة باسم جديد لأن OFL تحجز الأسماء الأصلية. — Subset two OFL masters to disjoint ranges, instance the variable one, unify UPM and vertical metrics, merge with fontTools and rename (Reserved Font Names are never reused).

**متى:** حين لا يستطيع خط مفتوح واحد تغطية النص العربي والأرقام/اللاتينية معًا في مرجع. / one open face cannot cover both the Arabic text and the figures/Latin of a reference

**كيف:** `pip install fonttools brotli && python3 fonts/kosif-jumuah/build_font.py` → KOSIFJumuah-Regular/Bold .ttf + .woff2 from Amiri (Arabic, GSUB kept) and Bodoni Moda instanced at wght 400/600, opsz 11 (Latin figures); OFL.txt carries both notices; tests check family names, code points (letters, tatweel, ﷺ, digits), GSUB survival and fsType 0.

**المعاملات:** UPM 1000; Latin wght 400/600 opsz 11; Arabic blocks 0600–06FF, 0750–077F, 08A0–08FF, FB50–FDFF, FE70–FEFF

**التثبيت:** pip install fonttools brotli

**الوسوم:** fonttools · merge · subset · OFL · عائلة خط · amiri · bodoni

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:fonttools` ← python3 -c "import fonttools" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-X05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/fonts/kosif-jumuah/build_font.py`
- `kosif-tool/fonts/kosif-jumuah/OFL.txt`
- `kosif-tool/tests/test_fonts.py`

#### 7. قدرات قريبة في العائلة

- `ARAB-X03` الزخرفة والكشيدة للنبذة فقط / Unicode ornaments and kashida: bios only (documented)
- `ARAB-X04` مطابقة الخط عبر محرك تشكيل حقيقي / Font matching through a real shaper (Chromium/HarfBuzz) (proven)
- `ARAB-X06` عنوان خطي مركّب من حدود حروف مفتوحة / Composed calligraphic title from OFL outlines (proven)

### `ARAB-X06` — عنوان خطي مركّب من حدود حروف مفتوحة / Composed calligraphic title from OFL outlines

| الحقل | القيمة |
|---|---|
| العائلة | `typography-arabic` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/typography-arabic.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لا يوجد خط ثلث مفتوح الرخصة؛ ابنِ إيماءة العنوان من حدود حروف Amiri Bold: مطّ الألف واللام، تكبير الجيم حول مفصلها، كشيدة بعد الميم والعين، إمالة مجموعة «لجمعة» المتصلة لينحدر السطر مع بقاء الأعمدة رأسية، وتشكيل يوضع يدويًا؛ مسار لكل حرف ليُرسم تدريجيًا. — No open Thuluth exists; build the title's gesture from Amiri Bold outlines (stretched stems, scaled ج, kashida, a sheared connected group, hand-placed marks), one path per glyph for draw-on.

**متى:** حين يكون عنوان المرجع خط يد لا يعيد إنتاجه أي خط مفتوح. / a reference title is hand-set calligraphy that no open font reproduces

**كيف:** `python3 fonts/kosif-jumuah/demo/compose_title.py --set shear=0.18 --set alef_sy=1.6 --set jeem_s=1.3` → title-aljumuah.svg, inlined in demo/jumuah.html and drawn on with strokeDasharray/Dashoffset per path. Honest limit: Naskh pen, not Thuluth; for an exact match a calligrapher's SVG replaces the file or a licensed Thuluth font goes in via --font (kept outside the repo if not OFL-compatible). Keep the SVG group id distinct from the page's #title (transform-origin rules leak into SVG).

**المعاملات:** stems ×1.6; ج ×1.3; shear tan 0.18; marks damma/damma/fatha

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ثلث · thuluth · lettering · svg · draw-on · عنوان · compose

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:ARAB-X06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio` · `caption-lines` · `font-fidelity-lab` · `image-local-ai` · `mimic` · `motion-runtime`.
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

- `kosif-tool/fonts/kosif-jumuah/demo/compose_title.py`
- `kosif-tool/fonts/kosif-jumuah/demo/title-aljumuah.svg`
- `kosif-tool/fonts/kosif-jumuah/demo/jumuah.html`

#### 7. قدرات قريبة في العائلة

- `ARAB-X04` مطابقة الخط عبر محرك تشكيل حقيقي / Font matching through a real shaper (Chromium/HarfBuzz) (proven)
- `ARAB-X05` تجميع عائلة خط مطابقة من مصدرين OFL / Assemble a matched OFL family from two masters (proven)

