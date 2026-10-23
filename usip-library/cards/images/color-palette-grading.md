# `color-palette-grading` — الصور والتحرير والتوليد (87 بطاقة)

> مكتبة بروتوكول USIP v5.6 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/color-palette-grading.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/images.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`COLOR-01` أحد عشر لوكًا جاهزًا بـFFmpeg](#color-01--أحد-عشر-لوكًا-جاهزًا-بـffmpeg--eleven-ffmpeg-grade-presets)
- [`COLOR-02` ترميم الفوتيج القديم](#color-02--ترميم-الفوتيج-القديم--restore-grade-for-old-or-soft-footage)
- [`COLOR-03` تلوينات مشاريع بسطر واحد](#color-03--تلوينات-مشاريع-بسطر-واحد--one-line-project-grades-muted-ghorba-navy-door--rtl-mirror)
- [`COLOR-04` خَبز أي تلوين في LUT](#color-04--خَبز-أي-تلوين-في-lut--bake-any-grade-into-a-hald-clut--cube-and-apply-luts)
- [`COLOR-05` لوكات المتصفح بالفلاتر وطبقات الدمج](#color-05--لوكات-المتصفح-بالفلاتر-وطبقات-الدمج--browser-looks-css-filter--blend-mode-tint-layers)
- [`COLOR-06` سلسلة FFmpeg المُصدّرة من «بصمة»](#color-06--سلسلة-ffmpeg-المُصدّرة-من-بصمة--basma-fingerprint-grade-chain-export)
- [`COLOR-07` أمزجة فيلم الكلمات وتلوينها](#color-07--أمزجة-فيلم-الكلمات-وتلوينها--verse-moods-palette-plus-matching-footage-grade)
- [`COLOR-08` مكتبة اللوكات المسماة](#color-08--مكتبة-اللوكات-المسماة--named-film-stock-and-photo-looks-library)
- [`COLOR-09` نموذج تلوين HyperFrames](#color-09--نموذج-تلوين-hyperframes--hyperframes-webgl-grade-model-17-presets-and-media-treatment-cli)
- [`COLOR-10` وصفات المعالجة وممرات الملاحظات](#color-10--وصفات-المعالجة-وممرات-الملاحظات--hyperframes-treatment-recipes-and-feedback-lanes)
- [`COLOR-11` لوكات LUT مع بديل حتمي](#color-11--لوكات-lut-مع-بديل-حتمي--lut-looks-with-deterministic-buildcube-fallback)
- [`COLOR-12` كشف التلوين بالمقارنة](#color-12--كشف-التلوين-بالمقارنة--grade-split-reveal-flat--graded-sweep)
- [`COLOR-13` ترتيب عقد التلوين](#color-13--ترتيب-عقد-التلوين--grade-order-technical-before-creative)
- [`COLOR-14` كشف اللوج قبل LUT](#color-14--كشف-اللوج-قبل-lut--log-detection-before-a-conversion-lut)
- [`COLOR-15` التعريض حسب وقت اليوم](#color-15--التعريض-حسب-وقت-اليوم--exposure-bands-by-time-of-day--cut-jump-caps)
- [`COLOR-16` توازن الأبيض بالبكسلات المحايدة](#color-16--توازن-الأبيض-بالبكسلات-المحايدة--neutral-pixel-white-balance)
- [`COLOR-17` تباين حول محور مع حماية القص](#color-17--تباين-حول-محور-مع-حماية-القص--pivot-contrast-with-clip-guard)
- [`COLOR-18` أرضية تشبع وانحدار سينمائي](#color-18--أرضية-تشبع-وانحدار-سينمائي--saturation-floor-with-film-roll-off)
- [`COLOR-19` تعزيز السماء فقط](#color-19--تعزيز-السماء-فقط--sky-hue-window-boost)
- [`COLOR-20` لوكات مقاسة بأهداف السكوب](#color-20--لوكات-مقاسة-بأهداف-السكوب--scope-target-looks-japan-summer-new-york-still-tokyo-night)
- [`COLOR-21` توجيه التلوين حسب اللقطة وأرضية الإضاءة](#color-21--توجيه-التلوين-حسب-اللقطة-وأرضية-الإضاءة--per-shot-type-direction-one-light-floor-value-before-colour)
- [`COLOR-22` تحليل حرارة اللون والميل والتشبع](#color-22--تحليل-حرارة-اللون-والميل-والتشبع--colour-analysis-cct-cast-colourfulness-6-colour-palette)
- [`COLOR-23` إزاحة الميرد واختيار الجل](#color-23--إزاحة-الميرد-واختيار-الجل--mired-shift--ctoctb-gel)
- [`COLOR-24` استخراج الباليت وتسمية الألوان](#color-24--استخراج-الباليت-وتسمية-الألوان--palette-extraction-colour-naming-and-δe)
- [`COLOR-25` باليت وخلفية لكل نبضة من المرجع](#color-25--باليت-وخلفية-لكل-نبضة-من-المرجع--reference-palette--background-per-beat)
- [`COLOR-26` نقل رينهارد إلى LUT لكل لقطة](#color-26--نقل-رينهارد-إلى-lut-لكل-لقطة--reinhard-lab-transfer--per-shot-cube)
- [`COLOR-27` مطابقة اللقطات بنقل لوني محدود](#color-27--مطابقة-اللقطات-بنقل-لوني-محدود--bounded-colour-transfer--hungarian-shot-match)
- [`COLOR-28` إصلاح تلقائي ومطابقة مرجع في «بصمة»](#color-28--إصلاح-تلقائي-ومطابقة-مرجع-في-بصمة--basma-measured-auto-fix-reference-match-and-look-classifier)
- [`COLOR-29` تغيير لون بلون مع الحفاظ على الظل](#color-29--تغيير-لون-بلون-مع-الحفاظ-على-الظل--local-recolour-ab-keeping-shading-arabic-requests)
- [`COLOR-30` ألوان الشعار الحقيقية](#color-30--ألوان-الشعار-الحقيقية--logo-true-colours--antialias-blend-detection)
- [`COLOR-31` هوية كاملة من لون واحد](#color-31--هوية-كاملة-من-لون-واحد--one-hex--full-wcag-token-set--9-accent-presets)
- [`COLOR-32` هوية «دفتر KOSIF»](#color-32--هوية-دفتر-kosif--dafter-kosif-ledger-identity-default-light--night)
- [`COLOR-33` مظاهر KOSIF EARTH](#color-33--مظاهر-kosif-earth--kosif-earth-identity-looks-14)
- [`COLOR-34` إعادة تلوين حسب الدور](#color-34--إعادة-تلوين-حسب-الدور--role-based-palette-remap-brandcss)
- [`COLOR-35` تحويل انتقائي ذهبي→جليدي](#color-35--تحويل-انتقائي-ذهبيجليدي--selective-goldice-hue-rotation-image-and-video)
- [`COLOR-36` باليتات الشيدر كمتغيرات](#color-36--باليتات-الشيدر-كمتغيرات--shader-palettes-as-uniforms-crystal-world)
- [`COLOR-37` باليتات منتجات التدقيق](#color-37--باليتات-منتجات-التدقيق--kosif-audit-palettes--cascade-order-theming)
- [`COLOR-38` ثيمات Kinetic Flow السبعة عشر](#color-38--ثيمات-kinetic-flow-السبعة-عشر--kinetic-flow-locked-themes-aq--custom-r)
- [`COLOR-39` باليتات الافتتاحي الفيروسي](#color-39--باليتات-الافتتاحي-الفيروسي--viral-editorial-palettes-13--8020-rule)
- [`COLOR-40` باليتات أفلام المالك](#color-40--باليتات-أفلام-المالك--owner-film-palettes-from-shipped-projects)
- [`COLOR-41` باليتات القوالب وخاناتها](#color-41--باليتات-القوالب-وخاناتها--starter-palettes-and-palette-slots)
- [`COLOR-42` ثيمات HyperFrames وعقد الرموز](#color-42--ثيمات-hyperframes-وعقد-الرموز--hyperframes-themes--18-token-contract)
- [`COLOR-43` مكتبات باليتات جاهزة](#color-43--مكتبات-باليتات-جاهزة--ready-palette-libraries-families-deck-presets-recut-themes-demo-kit-dark-ladders)
- [`COLOR-44` اللون حسب العاطفة والقطاع والثقافة](#color-44--اللون-حسب-العاطفة-والقطاع-والثقافة--brand-colour-by-emotion-sector-and-culture)
- [`COLOR-45` ألوان الحالات الدلالية](#color-45--ألوان-الحالات-الدلالية--semantic-status-colours-soft-tint-chips-5-stop-ladder)
- [`COLOR-46` باليتات آمنة لعمى الألوان](#color-46--باليتات-آمنة-لعمى-الألوان--colour-blind-safe-categorical-palettes)
- [`COLOR-47` خرائط الألوان وتسلسل الرسم البياني](#color-47--خرائط-الألوان-وتسلسل-الرسم-البياني--colormap-semantics-and-chart-colour-hierarchy)
- [`COLOR-48` التدرج الحراري بسبع محطات](#color-48--التدرج-الحراري-بسبع-محطات--thermal-7-stop-heat-ramp)
- [`COLOR-49` تدرجا ماغما والجبل](#color-49--تدرجا-ماغما-والجبل--magma-colormap-and-alpine-terrain-ramp)
- [`COLOR-50` مولّد التناغم اللوني](#color-50--مولّد-التناغم-اللوني--harmony-generator-2d3d--harmony-detector)
- [`COLOR-51` تدرجات إدراكية OKLCH وظلال بإزاحة الصبغة](#color-51--تدرجات-إدراكية-oklch-وظلال-بإزاحة-الصبغة--perceptual-oklch-ramps-and-hue-shifted-shading)
- [`COLOR-52` حساب التباين WCAG](#color-52--حساب-التباين-wcag--wcag-contrast-math-role-tiers-and-alpha-flattening)
- [`COLOR-53` الوضع الداكن بلا قلب](#color-53--الوضع-الداكن-بلا-قلب--dark-variant-without-inversion)
- [`COLOR-54` لون تمييز واحد بمعنى واحد](#color-54--لون-تمييز-واحد-بمعنى-واحد--one-accent-one-meaning-5-of-the-frame)
- [`COLOR-55` أنظمة لونين أو ثلاثة صارمة](#color-55--أنظمة-لونين-أو-ثلاثة-صارمة--strict-two--and-three-colour-systems)
- [`COLOR-56` قفل الأسلوب وبصمة المرجع](#color-56--قفل-الأسلوب-وبصمة-المرجع--style-lock-and-reference-style-dna--exact-hex-after-generation)
- [`COLOR-57` تحويل النغمات ACES وAgX وNeutral](#color-57--تحويل-النغمات-aces-وagx-وneutral--tone-mapping-choice-aces-agx-or-neutral)
- [`COLOR-58` تمريرة المظهر](#color-58--تمريرة-المظهر--look-pass-gamut-mask-purkinje-night-vision-split-toning)
- [`COLOR-59` المنظور الجوي](#color-59--المنظور-الجوي--aerial-perspective-3-channel-fog-fog-toward-the-sun-sky-bounce)
- [`COLOR-60` تمريرة تلوين الشيدر](#color-60--تمريرة-تلوين-الشيدر--shader-grade-pass-driven-by-story-or-music)
- [`COLOR-61` ألوان مصادر الضوء العملية](#color-61--ألوان-مصادر-الضوء-العملية--named-practical-light-colours-sodium-mercury-moon-flame)
- [`COLOR-62` تشطيب الرسام الفيلمي](#color-62--تشطيب-الرسام-الفيلمي--painter-filmic-curve-split-tone-grade-and-grain)
- [`COLOR-63` انضغاط الإضاءات العالية](#color-63--انضغاط-الإضاءات-العالية--highlight-roll-off-quantiser)
- [`COLOR-64` التعتيم الطرفي في كل محرك](#color-64--التعتيم-الطرفي-في-كل-محرك--vignette-in-every-engine)
- [`COLOR-65` تدرجات بشفافية وأنماط دمج](#color-65--تدرجات-بشفافية-وأنماط-دمج--gradient-paints-with-alpha-stops-and-blend-modes)
- [`COLOR-66` قلب القطبية بين الفصول](#color-66--قلب-القطبية-بين-الفصول--polarity-flip-inkpaper-at-act-boundaries)
- [`COLOR-67` فصول وضربات بحقول لونية](#color-67--فصول-وضربات-بحقول-لونية--colour-field-chapter-and-beat-flips)
- [`COLOR-68` ضربة لون كامل للإطار](#color-68--ضربة-لون-كامل-للإطار--full-bleed-accent-beat--brand-flash-fill)
- [`COLOR-69` تحريك تدرج السماء ووقت اليوم](#color-69--تحريك-تدرج-السماء-ووقت-اليوم--sky-stop-tweening-time-of-day-and-seasons)
- [`COLOR-70` التلوين كقصة](#color-70--التلوين-كقصة--grade-change-as-story-drain-bloom-freeze-to-grey)
- [`COLOR-71` منطق الألوان السردي](#color-71--منطق-الألوان-السردي--narrative-colour-logic-problem--solution)
- [`COLOR-72` لون لكل عنصر](#color-72--لون-لكل-عنصر--per-item-hue-coding-at-equal-luminance)
- [`COLOR-73` صبغة الإطار للحدث](#color-73--صبغة-الإطار-للحدث--full-frame-event-tint-and-flash)
- [`COLOR-74` حلقات بتدرج الصبغة ودوران اللون](#color-74--حلقات-بتدرج-الصبغة-ودوران-اللون--hue-indexed-rings-and-slow-hue-rotation)
- [`COLOR-75` عنوان بلونين وكلمة مميزة](#color-75--عنوان-بلونين-وكلمة-مميزة--two-tone-headline-and-accent-word)
- [`COLOR-76` شريط عينات الألوان](#color-76--شريط-عينات-الألوان--swatch-strip-reveal)
- [`COLOR-77` باليت مفهرسة من 16 لونًا](#color-77--باليت-مفهرسة-من-16-لونًا--indexed-16-colour-palette-with-alternating-accent-flash)
- [`COLOR-78` أرضيات داكنة شعاعية](#color-78--أرضيات-داكنة-شعاعية--radial-dark-grounds)
- [`COLOR-79` أرضية ورقية كريمية](#color-79--أرضية-ورقية-كريمية--warm-paper-editorial-ground)
- [`COLOR-80` خلفية بقع ضبابية متحركة](#color-80--خلفية-بقع-ضبابية-متحركة--drifting-blob--mesh-gradient-ambient-ground)
- [`COLOR-81` لوحات شيدر WebGPU](#color-81--لوحات-شيدر-webgpu--webgpu-shader-colour-plates)
- [`COLOR-82` توحيد الطبقات](#color-82--توحيد-الطبقات--unify-the-stack-one-grade-grain-vignette)
- [`COLOR-83` سلم المعالجة](#color-83--سلم-المعالجة--treatment-ladder-colour--duotone--halftone--vector)
- [`COLOR-84` تشطيب الكولاج العتيق مع الوميض](#color-84--تشطيب-الكولاج-العتيق-مع-الوميض--vintage-collage-finish-with-exposure-flicker)
- [`COLOR-85` لوحات الغروب والسايكدلك والدفع الأحادي](#color-85--لوحات-الغروب-والسايكدلك-والدفع-الأحادي--sunsetsynthwave-psychedelic-and-monohue-push-palettes)
- [`COLOR-86` طين أبيض ولون للبيانات فقط](#color-86--طين-أبيض-ولون-للبيانات-فقط--white-clay-render-with-colour-only-for-data)
- [`COLOR-X01` حزمة أسلوب مقيسة والتدريج بالقياس](#color-x01--حزمة-أسلوب-مقيسة-والتدريج-بالقياس--measured-style-pack-and-grading-by-measurement)

## البطاقات / cards

### `COLOR-01` — أحد عشر لوكًا جاهزًا بـFFmpeg / Eleven FFmpeg grade presets

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جدول GRADES في montage.py: أحد عشر تلوينًا مسمّى (curves/colorbalance/eq) تطبّقه على مقطع أو على كل لقطة في المونتاج، والحبيبات مبذورة فتتكرر النتيجة نفسها. / The montage.py GRADES table: eleven named curves/colorbalance/eq grades for one clip or per cut, with seeded grain so re-renders are identical.

**متى:** حين يريد المستخدم لوكًا سينمائيًا جاهزًا لمقطع أو لكل لقطة في المونتاج مع بقاء الصوت كما هو / when the user wants a ready named colour look on one clip or on every cut of a montage

**كيف:** CLI: `python montage.py grade CLIP.mp4 --preset teal_orange [--out X.mp4]` (also `kmotion grade`, `montage cut --grade`, timeline JSON `clips[].grade`, `smart_montage.py grade`). Output libx264 -preset medium -crf 17, format=yuv420p, audio stream copied untouched. The same chain can be pasted into any `-vf`. Verified in this container on 2026-10-16: all 11 chains ran on testsrc2 with rc=0 (blue_hour pulls YAVG 121.6→108.2 and V 127→133.7; teal_orange pushes U to 135.6), and kosif-studio's test asserts blue_hour + sodium_night run through ffmpeg. The kosif-studio, 100-superskills and kosif-one/tools tables match value for value (only line endings differ); kosif-omni's smart_montage carries the first six at CRF 18 with unseeded vintage grain alls=12 — prefer the seeded table. (code snippet in references/powers/color-palette-grading.md) (full table in references/powers/color-palette-grading.md)

**المعاملات:** 11 presets; CRF 17 (smart_montage CRF 18); grain all_seed=7; audio -c:a copy

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تلوين · لوك · فلتر · مونتاج · grade · color grading · ffmpeg · teal orange · golden hour · cyberpunk · vintage · blue hour · preset · لوك سينمائي · كلرنج · فلاتر جاهزة · cinematic look · film look

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-studio/motion/montage.py:42`
- `kosif-studio/tests/test_studio.py:818`
- `100-superskills/skills/kosif-montage-motion/scripts/montage.py:42`
- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/smart_montage.py:29`

#### 7. قدرات قريبة في العائلة

- `COLOR-02` ترميم الفوتيج القديم / Restore grade for old or soft footage (proven)
- `COLOR-03` تلوينات مشاريع بسطر واحد / One-line project grades (muted Ghorba, navy door + RTL mirror) (proven)

### `COLOR-02` — ترميم الفوتيج القديم / Restore grade for old or soft footage

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تلوين إنقاذ: إزالة ضوضاء زمنية خفيفة، سواد أنظف، انضغاط للإضاءات، دفء خفيف في المنتصف، وشحذ متكيف — ونسخة FINAL_EDIT المضبوطة يدويًا التي شُحنت. / A rescue grade: light temporal denoise, cleaner blacks, highlight roll-off, warmer mids and contrast-adaptive sharpening — plus the hand-tuned FINAL_EDIT variant that shipped.

**متى:** حين يكون الفيديو قديمًا أو ناعمًا أو فيه تشويش ويحتاج تنظيفًا وسوادًا أنظف وتوضيحًا / when old, soft or noisy footage needs a rescue grade: light denoise, cleaner blacks and sharpening

**كيف:** `montage.py grade CLIP --preset restore`. Chain: hqdn3d=1.2:1.2:3:3 → eq contrast 1.12 brightness −0.015 saturation 1.07 gamma 0.97 → curves all `0/0 .06/.035 .25/.22 .5/.5 .8/.82 .94/.93 1/.97` → colorbalance rs .012 bs −.01 rm .025 gm .005 bm −.02 → cas 0.3. FINAL_EDIT (talking head, Lanczos 720×1280→1080×1920): eq contrast 1.12 brightness −0.02 saturation 1.10 gamma 0.96, same curves, colorbalance rs .015 bs −.01 rm .01, cas 0.32. Ran here on testsrc2 (rc=0). Upscale before CAS, never after.

**المعاملات:** hqdn3d 1.2:1.2:3:3; gamma .97/.96; cas .3/.32; whites capped at .97

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ترميم · تحسين · فيديو قديم · شحذ · restore · denoise · sharpen · cas · old footage · talking head · إزالة التشويش · توضيح الصورة · جودة الفيديو · noise reduction · enhance video

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-studio/motion/montage.py:42`
- `100-superskills/skills/kosif-montage-motion/scripts/montage.py:53`
- `kosif-studio/out/FINAL_EDIT/project/grade.txt`
- `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:12`

#### 7. قدرات قريبة في العائلة

- `COLOR-01` أحد عشر لوكًا جاهزًا بـFFmpeg / Eleven FFmpeg grade presets (proven)
- `COLOR-03` تلوينات مشاريع بسطر واحد / One-line project grades (muted Ghorba, navy door + RTL mirror) (proven)
- `COLOR-04` خَبز أي تلوين في LUT / Bake any grade into a Hald CLUT / .cube and apply LUTs (proven)

### `COLOR-03` — تلوينات مشاريع بسطر واحد / One-line project grades (muted Ghorba, navy door + RTL mirror)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تلوينات صغيرة شُحنت في مشاريع حقيقية: «الغربة» الهادئ المعتم قليلًا بنسختين، وتلوين colorbalance يسحب لقطة رمادية نحو الكحلي مع عكس أفقي ليفرغ اليمين للنص العربي. / Small grades shipped in real projects: the quiet, slightly darker Ghorba look in two calibrations, and a colorbalance pull from charcoal toward brand navy with an hflip so empty space sits on the right for Arabic text.

**متى:** حين يريد المستخدم لوكًا هادئًا معتمًا بسطر واحد، أو سحب لقطة رمادية للكحلي مع عكسها ليفرغ اليمين للنص العربي / for a quiet muted one-line grade, or a grey shot pulled to navy and mirrored for Arabic text

**كيف:** Ghorba v1 `eq=contrast=1.08:saturation=0.86:brightness=-0.023`, v2 `eq=contrast=1.06:saturation=0.95:brightness=-0.009` inside the per-shot -vf. Navy door: `-vf "hflip,colorbalance=rs=-.10:gs=-.03:bs=.25:rm=-.05:bm=.10"` then H.264 width 1280 crf 27 -an +faststart. All three ran here on testsrc2 (rc=0).

**المعاملات:** sat .86/.95; brightness −.023/−.009; bs +.25 navy pull

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حزين · هادئ · كحلي · عكس · muted · melancholy · navy · hflip · rtl · eq · لوك حزين · ألوان باهتة · مساحة للنص · desaturated · mirror flip

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:146`
- `kosif-one/projects/KOSIF_Motion_Ghorba/tools/render_ghorba_preview.py:139`
- `kosif-earth-ci-fork/docs/design/HIGGSFIELD_VISUALS_ar.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-01` أحد عشر لوكًا جاهزًا بـFFmpeg / Eleven FFmpeg grade presets (proven)
- `COLOR-02` ترميم الفوتيج القديم / Restore grade for old or soft footage (proven)
- `COLOR-04` خَبز أي تلوين في LUT / Bake any grade into a Hald CLUT / .cube and apply LUTs (proven)
- `COLOR-05` لوكات المتصفح بالفلاتر وطبقات الدمج / Browser looks: CSS filter + blend-mode tint layers (proven)

### `COLOR-04` — خَبز أي تلوين في LUT / Bake any grade into a Hald CLUT / .cube and apply LUTs

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تحوّل أي سلسلة FFmpeg إلى صورة Hald أو ملف .cube بحجم 33 نقطة، ثم تطبقها بـlut3d أو haldclut بنتيجة شبه مطابقة — وتطبق LUT التحويل أو LUT الإبداعي من الكاميرا بالطريقة نفسها. / Turn any FFmpeg chain into a Hald image or a 33-point .cube and re-apply it with lut3d/haldclut almost identically; camera conversion and creative LUTs go in the same way.

**متى:** حين يريد المستخدم حفظ لوك كملف LUT لإعادة استخدامه، أو تطبيق LUT تحويل أو LUT إبداعي من الكاميرا / when the user wants to save a grade as a reusable .cube LUT, or apply a camera conversion or creative LUT

**كيف:** haldclutsrc=8 (64³ entries) → run the grade chain on that one frame → apply with `[v][hald]haldclut=interp=tetrahedral`, or resample the Hald to a 33³ .cube (NumPy, R fastest) and use `lut3d=file=look.cube:interp=tetrahedral`. Verified here with teal_orange on 640×360 testsrc2: Hald vs direct grade PSNR 51.9 dB, 33³ cube vs direct 47.9 dB. Spatial or temporal parts (noise, unsharp, cas, vignette) do not bake — re-add them after the LUT. Use 33- or 65-point cubes and tetrahedral interpolation on 10-bit sources to avoid banding; never apply a conversion LUT twice. (code snippet in references/powers/color-palette-grading.md)

**المعاملات:** haldclutsrc level 8; cube 33³ (or 65³); PSNR 51.9 / 47.9 dB measured

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** LUT · كيوب · هالد · تصدير اللوك · lut3d · haldclut · cube · bake · export look · ملف لوت · حفظ اللوك · تطبيق لوت · 3d lut · lut export

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:numpy` ← python3 -c "import numpy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-studio/motion/montage.py:42`
- `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2435-akbun-davinciresolve-logconvert/SKILL.md`
- `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-02` ترميم الفوتيج القديم / Restore grade for old or soft footage (proven)
- `COLOR-03` تلوينات مشاريع بسطر واحد / One-line project grades (muted Ghorba, navy door + RTL mirror) (proven)
- `COLOR-05` لوكات المتصفح بالفلاتر وطبقات الدمج / Browser looks: CSS filter + blend-mode tint layers (proven)
- `COLOR-06` سلسلة FFmpeg المُصدّرة من «بصمة» / Basma fingerprint grade chain export (ready)

### `COLOR-05` — لوكات المتصفح بالفلاتر وطبقات الدمج / Browser looks: CSS filter + blend-mode tint layers

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أحد عشر لوكًا من محرر «بصمة» تُبنى من فلتر CSS واحد وطبقات صبغة بأنماط دمج، مع منزلقات تباين وتشبع وإضاءة، وتلوين «الحبر والزعفران» الذي يعيد تلوين فيديو بلا إعادة ترميز. / Basma's eleven looks built from one CSS filter plus blended tint layers, with contrast/saturation/brightness sliders, and the 'ink & saffron' re-tone that recolours a clip at runtime without re-encoding.

**متى:** حين يحتاج المستخدم فلاتر لونية فورية في المتصفح بمنزلقات تباين وتشبع، أو إعادة تلوين فيديو دون إعادة ترميز / for instant in-browser looks with sliders, or recolouring a video without re-encoding

**كيف:** Canvas: ctx.filter = look.f, drawImage, then for each tint [hex, alpha, mode] set globalAlpha + globalCompositeOperation and fillRect; then gradeFilter adds contrast() saturate() brightness() from sliders (contrast 0.8–1.4, saturate 0.5–1.6, brightness 0.8–1.2, vignette 0–0.8, optional soft-light tint alpha 0.16). Ink & saffron (video element): grayscale(1) sepia(.5) saturate(1.35) hue-rotate(-8deg) contrast(1.05) brightness(.82); banner wash linear-gradient(160deg, rgba(217,83,14,.55), rgba(29,24,20,.9)) with background-blend-mode:color. All 12 rendered in Chromium (Playwright) in this container on 2026-10-16. (code snippet in references/powers/color-palette-grading.md) (full table in references/powers/color-palette-grading.md)

**المعاملات:** 11 looks + ink_saffron; slider ranges c .8–1.4 / s .5–1.6 / b .8–1.2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** فلتر · لوك فوري · متصفح · زعفران · css filter · canvas · blend mode · soft-light · browser grade · sepia · فلاتر ويب · منزلقات · صبغة لونية · live filter · web look

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `app/public/js/00_editor.js:204`
- `app/public/js/00_editor.js:217`
- `kosif-earth-ci-fork/unlock.html:85`
- `kosif-earth-ci-fork/ui/ds/sqc.css:308`

#### 7. قدرات قريبة في العائلة

- `COLOR-03` تلوينات مشاريع بسطر واحد / One-line project grades (muted Ghorba, navy door + RTL mirror) (proven)
- `COLOR-04` خَبز أي تلوين في LUT / Bake any grade into a Hald CLUT / .cube and apply LUTs (proven)
- `COLOR-06` سلسلة FFmpeg المُصدّرة من «بصمة» / Basma fingerprint grade chain export (ready)
- `COLOR-07` أمزجة فيلم الكلمات وتلوينها / Verse moods: palette plus matching footage grade (ready)

### `COLOR-06` — سلسلة FFmpeg المُصدّرة من «بصمة» / Basma fingerprint grade chain export

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سكربت بايثون مُصدَّر من استوديو «بصمة» يعيد إنتاج التلوين بفلاتر FFmpeg عادية: eq وcolorbalance وفينيت وحبيبات وأشرطة سينما. / The Python script Basma exports reproduces a look with plain FFmpeg: eq, colorbalance, vignette, grain and letterbox bars.

**متى:** حين يريد المستخدم إعادة إنتاج لوك «بصمة» خارج المحرر بسكربت بايثون وفلاتر FFmpeg عادية / when a Basma look must be reproduced outside the editor as a Python script of plain FFmpeg filters

**كيف:** grade_chain(): eq=contrast:saturation:brightness=(b−1)·0.5; teal_orange → colorbalance rs=−0.08:bs=0.10:rh=0.08:bh=−0.06; bw → hue=s=0; warm/cool → colorbalance rm/bm ±0.6·k; vignette=PI/5 when strength > 0.3; grain → noise=alls=6+40·g:allf=t; letterbox → drawbox 10.5% top and bottom. Pure FFmpeg, nothing to install.

**المعاملات:** vignette PI/5 if >0.3; grain alls 6+40g; letterbox 10.5%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تصدير · سكربت · أشرطة سينما · export · letterbox · colorbalance · grain · vignette · بصمة · حبيبات فيلم · تعتيم الأطراف · python script · ffmpeg chain

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

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `app/public/js/10_studio.js:1683`

#### 7. قدرات قريبة في العائلة

- `COLOR-04` خَبز أي تلوين في LUT / Bake any grade into a Hald CLUT / .cube and apply LUTs (proven)
- `COLOR-05` لوكات المتصفح بالفلاتر وطبقات الدمج / Browser looks: CSS filter + blend-mode tint layers (proven)
- `COLOR-07` أمزجة فيلم الكلمات وتلوينها / Verse moods: palette plus matching footage grade (ready)
- `COLOR-08` مكتبة اللوكات المسماة / Named film-stock and photo looks library (documented)

### `COLOR-07` — أمزجة فيلم الكلمات وتلوينها / Verse moods: palette plus matching footage grade

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خمسة أمزجة (ليل، فجر، ذهب، بحر، حبر) لكل منها لوحة سماء/هالة/ذرات، وكل مزاج يختار تلوين الفوتيج المناسب تلقائيًا، والفيلم يزداد إضاءة على طول قوسه. / Five moods (night, dawn, gold, sea, ink), each a sky/halo/mote palette that also picks the matching footage grade; the film brightens along its arc.

**متى:** حين يصنع المستخدم فيلم كلمات لأغنية أو قصيدة أو دعاء ويريد مزاجًا لونيًا (ليل، فجر، ذهب، بحر، حبر) يطابقه تلوين الفوتيج / for a lyric, poem or dua film needing a mood palette with a matching footage grade

**كيف:** `verse.py AUDIO --mood night\|dawn\|gold\|sea\|ink --accent '#E7B65A'`; songreel MOOD_GRADE maps night→blue_hour, dawn/gold→golden_hour, sea→teal_orange, ink→vintage_film (COLOR-01). Each section shifts hue +7°/−5° and brightness rises 0.9→1.15 over the film. (full table in references/powers/color-palette-grading.md)

**المعاملات:** night #0B0F1E/#221C3B glow #ECBD51 mote #F9E094; dawn #12142B/#994329/#FAA442/#FFDDA3; gold #110D09/#372715/#EEAD2B/#FBD774; sea #07131D/#16444B/#3CDDD2/#ACF6F6; ink #0A0A0A/#1C1C1C/#B2B2B2/#EBEBEB

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** دعاء · قصيدة · أغنية · مزاج · ليل · فجر · mood · verse · lyric film · sky palette · dua · فيديو كلمات · ألوان المزاج · سماء ليلية · lyrics video · mood palette

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/verse.py:49`
- `100-superskills/skills/kosif-montage-motion/scripts/songreel.py:78`
- `100-superskills/skills/kosif-montage-motion/templates/verse.html:79`
- `kosif-one/tools/kosif-studio/motion/templates/verse.html:64`

#### 7. قدرات قريبة في العائلة

- `COLOR-05` لوكات المتصفح بالفلاتر وطبقات الدمج / Browser looks: CSS filter + blend-mode tint layers (proven)
- `COLOR-06` سلسلة FFmpeg المُصدّرة من «بصمة» / Basma fingerprint grade chain export (ready)
- `COLOR-08` مكتبة اللوكات المسماة / Named film-stock and photo looks library (documented)
- `COLOR-09` نموذج تلوين HyperFrames / HyperFrames WebGL grade model, 17 presets and media-treatment CLI (install)

### `COLOR-08` — مكتبة اللوكات المسماة / Named film-stock and photo looks library

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قاموس لوكات بأسماء يفهمها العميل: أفلام كوداك وفوجي وسينستيل، و«بليتش بايباس» و«ويس أندرسون» الباستيل، وسبعة لوكات صور بوحدات أدوبي. / A vocabulary of looks a client recognises: Kodak/Fuji/CineStill stocks, bleach bypass, pastel Wes, and seven photo-set looks in Adobe units.

**متى:** حين يذكر العميل اسم لوك معروف مثل كوداك بورترا أو فوجي أو سينستيل أو باستيل ويس أندرسون ويريده في الفيديو / when a client names a known film stock or look (Portra, CineStill, bleach bypass, Wes pastel) and wants it

**كيف:** Director KB (CSS base + mood): teal_orange (blockbuster, contrast 1.12 sat 1.15), bleach_bypass (gritty, contrast 1.3 sat .6), cold_desat (sad, sat .6 brightness .96), warm_vintage (nostalgia, sepia .25 contrast .95), kodak_portra (intimate, contrast .95 brightness 1.04), vision3_500t (filmic night, contrast 1.1), cinestill_800t (dreamy neon, contrast 1.08 sat 1.1), fuji_velvia (vivid travel, contrast 1.2 sat 1.45), noir_bw (grayscale, contrast 1.4), neon_cyber (contrast 1.15 sat 1.35), pastel_wes (contrast .88). Film shorthand: Portra 400, Ektar 100, CineStill 800T split tone #D4A050 highlights / #1A3040 shadows, Velvia. Photo looks (Adobe units — exact needs the Adobe connector; approximate locally with colortemperature/vibrance/eq or a numpy .cube): Warm & Golden temp 32/120 lum 67 vibrance +15; Bright & Airy 20/60/62 sat −10 vibrance +10 brightness +15; Moody & Cinematic 20/−50/45 sat −20 contrast +25; Cool & Fresh 18/−123/45 vibrance +10. Translate to COLOR-01/05 chains; never promise an exact stock emulation.

**المعاملات:** 11 KB grades; CineStill split #D4A050/#1A3040; 7 photo looks

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كوداك · فيلم · سينمائي · قاموس · film stock · portra · cinestill · bleach bypass · velvia · look names · لوك فيلم · فوجي · ألوان باستيل · kodak · fuji · wes anderson

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:numpy` ← python3 -c "import numpy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `app/public/js/10_studio.js:8`
- `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/prompt-library.md`
- `kosif-atlas/skills/103-adobe-for-creativity/230-adobe-batch-edit-photos/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-06` سلسلة FFmpeg المُصدّرة من «بصمة» / Basma fingerprint grade chain export (ready)
- `COLOR-07` أمزجة فيلم الكلمات وتلوينها / Verse moods: palette plus matching footage grade (ready)
- `COLOR-09` نموذج تلوين HyperFrames / HyperFrames WebGL grade model, 17 presets and media-treatment CLI (install)
- `COLOR-10` وصفات المعالجة وممرات الملاحظات / HyperFrames treatment recipes and feedback lanes (install)

### `COLOR-09` — نموذج تلوين HyperFrames / HyperFrames WebGL grade model, 17 presets and media-treatment CLI

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** محرك تلوين WebGL كامل: تعريض وتباين وإضاءات وظلال وأبيض وأسود وحرارة وصبغة وحيوية وتشبع، وعجلات وثلاثة منحنيات وحتى أربع تحديدات HSL وحبيبات وفينيت وLUT، مع 17 إعدادًا جاهزًا وأداة تحفظ المعالجة على العنصر. / A full WebGL grade: exposure/contrast/highlights/shadows/whites/blacks/temperature/tint/vibrance/saturation, wheels, curves, up to 4 HSL selections, grain, vignette, custom .cube, 17 presets, and a CLI that persists the treatment on an element.

**متى:** حين يحتاج المستخدم تلوينًا كاملًا داخل HyperFrames بعجلات ومنحنيات وتحديدات HSL وLUT مع حفظ المعالجة على العنصر / for a full WebGL grade in HyperFrames with wheels, curves, HSL selections, LUT and a persisted treatment

**كيف:** Grade object `{preset, intensity, adjust:{exposure −2..2, others −1..1}, details:{vignette, vignetteFeather, grain, grainSize}, colorSpace:'rec709'}`. Persist: `npx hyperframes media-treatment --selector '#hero' --grading '<json>' --apply --json`; measure with `--analyze --json`; list controls with `--capabilities --json`. Presets: neutral, warm-daylight (exposure .06 contrast .07 temperature .18 sat .08), clean-studio, skin-soft, food-pop (contrast .1 temperature .14 sat .18), night-lift, muted-editorial (sat −.12 vignette .1), vintage-wash, mono-clean (sat −1), mono-fade, soft-boost, bright-pop, deep-contrast (contrast .2), creator-camcorder, vhs-playback, editorial-halftone, two-ink-print. grade-compare renders a 16-cell A/B sheet. Vendored source in kosif-one/vendor/hyperframes; the CLI is not installed here.

**المعاملات:** 17 presets; HSL selections ≤4; exposure −2..2; grade-compare 16 cells

**التثبيت:** npm i -D hyperframes@0.8.164 # then: npx hyperframes media-treatment --capabilities --json

**الوسوم:** هايبرفريمز · تلوين ويب · منحنيات · hyperframes · webgl grade · presets · hsl · media-treatment · skin-soft · عجلات الألوان · تعريض · حرارة اللون · color wheels · curves · vignette

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-one/vendor/hyperframes/packages/core/src/colorGrading.ts:448`
- `kosif-one/vendor/hyperframes/packages/cli/src/commands/media-treatment.ts`
- `kosif-one/vendor/hyperframes/docs/guides/color-grading.mdx`
- `kosif-one/vendor/hyperframes/skills/media-use/references/grading.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-07` أمزجة فيلم الكلمات وتلوينها / Verse moods: palette plus matching footage grade (ready)
- `COLOR-08` مكتبة اللوكات المسماة / Named film-stock and photo looks library (documented)
- `COLOR-10` وصفات المعالجة وممرات الملاحظات / HyperFrames treatment recipes and feedback lanes (install)
- `COLOR-11` لوكات LUT مع بديل حتمي / LUT looks with deterministic buildCube fallback (install)

### `COLOR-10` — وصفات المعالجة وممرات الملاحظات / HyperFrames treatment recipes and feedback lanes

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 19 بذرة معالجة مختبرة (بورتريه طبيعي، صقل منتج، VHS، 8 ملم، هافتون، طباعة بلونين...) وقاعدة تحوّل ملاحظة العميل الغامضة إلى «ممر» معالجة محدد. / 19 tested treatment seeds (natural portrait, product polish, VHS, 8mm, halftone, two-ink print…) plus a rule that maps vague client feedback to one treatment lane.

**متى:** حين تأتي ملاحظة عميل غامضة مثل «غامق» أو «باهت» أو «عايزه سينمائي» وتحتاج معالجة محددة، أو لوك VHS أو 8 ملم أو هافتون / when vague client feedback must map to one treatment lane, or for VHS, 8mm, halftone or print looks

**كيف:** Lanes: correction (too dark/flat/warm) → wheels/curves/HSL secondary → preset or custom treatment (premium, cinematic) → shader effect (retro, print, ASCII, glitch, camcorder) → privacy blur/pixelate → framing/motion → seek-safe treatment keyframes. First inspect an early/middle/late contact sheet (`hyperframes snapshot <p> --frames 3`), then start from a seed and tune only inside its bounded ranges; adjust values are absolute, not deltas. (full table in references/powers/color-palette-grading.md)

**المعاملات:** Natural Portrait {preset:'skin-soft', intensity:0.6}; VHS grain .16 tapeDamage .82 tapeTracking .85 chromaBleed .5 CA .18 scanlines .35 glitch .32

**التثبيت:** npm i -D hyperframes@0.8.164

**الوسوم:** معالجة · VHS · هافتون · ملاحظات العميل · treatment · vhs · halftone · dither · crt · feedback lane · ريترو · شريط فيديو · 8 ملم · retro · 8mm · client notes

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-one/vendor/hyperframes/skills/media-use/references/media-treatment-recipes.md`
- `kosif-one/vendor/hyperframes/skills/media-use/references/media-treatments.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-08` مكتبة اللوكات المسماة / Named film-stock and photo looks library (documented)
- `COLOR-09` نموذج تلوين HyperFrames / HyperFrames WebGL grade model, 17 presets and media-treatment CLI (install)
- `COLOR-11` لوكات LUT مع بديل حتمي / LUT looks with deterministic buildCube fallback (install)
- `COLOR-12` كشف التلوين بالمقارنة / Grade Split Reveal (flat → graded sweep) (install)

### `COLOR-11` — لوكات LUT مع بديل حتمي / LUT looks with deterministic buildCube fallback

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاثة لوكات LUT مفهرسة تُجلب عند الطلب، ومع غياب الشبكة تُبنى محليًا من معاملاتها بمكعب 33³ — فلا تعتمد على ملف مجهول. / Three indexed LUT looks fetched on demand; offline they are rebuilt locally from parameters as a 33³ cube.

**متى:** حين يريد المستخدم لوك LUT جاهزًا (تيل وبرتقالي، بليتش، فيلم باهت) يعمل حتى بلا إنترنت ببناء المكعب محليًا / when a ready LUT look is needed that still works offline by rebuilding the 33³ cube locally

**كيف:** `npx hyperframes media-use resolve --type lut …` (add `--local-only` to force buildCube). teal-orange-blockbuster (intensity .85; contrast .18; split tone shadows [−.04,.05,.09] highlights [.1,.04,−.03]); bleach-bypass (.8; contrast .55, saturation −.72); film-fade (.75; blacks +.35, contrast −.28, temperature +.16). Never paste a .cube into context — reference the file.

**المعاملات:** cube 33³ default; 3 looks

**التثبيت:** npm i -D hyperframes@0.8.164

**الوسوم:** LUT · بليتش · أفلام · lut · bleach bypass · film fade · offline · buildCube · بدون إنترنت · تيل وبرتقالي · لوت جاهز · teal orange · hyperframes

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-one/vendor/hyperframes/skills/media-use/luts/index.json`
- `kosif-one/vendor/hyperframes/skills/media-use/luts/README.md`
- `kosif-one/vendor/hyperframes/skills/media-use/references/grading.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-09` نموذج تلوين HyperFrames / HyperFrames WebGL grade model, 17 presets and media-treatment CLI (install)
- `COLOR-10` وصفات المعالجة وممرات الملاحظات / HyperFrames treatment recipes and feedback lanes (install)
- `COLOR-12` كشف التلوين بالمقارنة / Grade Split Reveal (flat → graded sweep) (install)
- `COLOR-13` ترتيب عقد التلوين / Grade order: technical before creative (documented)

### `COLOR-12` — كشف التلوين بالمقارنة / Grade Split Reveal (flat → graded sweep)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | registry compositions are timed with GSAP — GSAP 'Standard no-charge' license (gsap.com/standard-license), not MIT. |

**ما هي:** الصورة نفسها مرتين — خام ومُلوّنة — بحافة صلبة تمسح الإطار، تتوقف للمقارنة، ثم تستقر على النسخة الملوّنة؛ والتلوينان حقيقيان بـWebGL. / The same picture twice — flat and graded — with a hard edge that sweeps, pauses for comparison, then commits to the grade; both are real WebGL grades.

**متى:** حين يريد المستخدم إظهار الفرق قبل التلوين وبعده بحافة تمسح الصورة نفسها ثم تستقر على النسخة الملونة / for a before/after grade reveal where an edge sweeps from flat to graded and settles on the grade

**كيف:** `npx hyperframes add grade-split-reveal` → mount on a `.clip` div with data-composition-src/data-start/data-duration/data-track-index and JSON data-variable-values. Looks: warm-cinematic (deep-contrast, contrast .28, temp .18, vibrance .26, vignette .3, grain .1) \| cool-teal (contrast .32, temp −.26, tint .08) \| bleach-bypass (contrast .54, sat −.46, grain .18); split 62% (25–85); edge hairline 2 px \| bold 6 px \| hidden. Extra duration becomes hold, never time-stretch. Pure-HTML alternative: two stacked layers, top one clip-path inset animated left→right.

**المعاملات:** split 62% (25–85); edge 2/6 px; 3 looks

**التثبيت:** npm i -D hyperframes@0.8.164 && npx hyperframes add grade-split-reveal

**الوسوم:** قبل وبعد · مقارنة · before after · split reveal · wipe · grade compare · قبل وبعد التلوين · مسحة كشف · عرض الفرق · comparison · flat vs graded

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-one/vendor/hyperframes/registry/components/grade-split-reveal/grade-split-reveal.html`
- `kosif-one/vendor/hyperframes/registry/components/grade-split-reveal/registry-item.json`
- `kosif-one/vendor/hyperframes/docs/catalog/components/grade-split-reveal.mdx`

#### 7. قدرات قريبة في العائلة

- `COLOR-10` وصفات المعالجة وممرات الملاحظات / HyperFrames treatment recipes and feedback lanes (install)
- `COLOR-11` لوكات LUT مع بديل حتمي / LUT looks with deterministic buildCube fallback (install)
- `COLOR-13` ترتيب عقد التلوين / Grade order: technical before creative (documented)
- `COLOR-14` كشف اللوج قبل LUT / Log detection before a conversion LUT (proven)

### `COLOR-13` — ترتيب عقد التلوين / Grade order: technical before creative

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** التصحيح التقني أولًا لكل لقطة ثم عقدة «لوك» إبداعية منفصلة؛ لا تخلطهما أبدًا. / Per-clip technical correction first, then a separate creative LOOK node; never mix the two.

**متى:** حين يبدأ المستخدم تلوين مشروع في دافنشي ويحتاج ترتيب العقد: تصحيح تقني لكل لقطة أولًا ثم عقدة لوك إبداعية منفصلة / when setting up a Resolve grade: technical correction per clip first, then a separate creative look node

**كيف:** Resolve: EXPOSURE → WB (before the Log→Rec.709 transform) → CST/LUT → CONTRAST → SAT (ceiling ~1.25 with shadow/highlight roll-off) → LOOK as a new serial node; LUT/CST runs first in time and everything is measured on its output. DWG/Intermediate path: input CST → global exposure → WB → contrast 1.3 pivot 0.336 → colour-slice sat → selective → output CST → creative LUT, tetrahedral. FFmpeg analogue: eq/exposure → colorbalance/colortemperature → lut3d → eq=contrast → hue=s → look LUT/curves, each its own filter. Phone footage needs less.

**المعاملات:** SAT ≤1.25; DWG contrast 1.3 pivot 0.336

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ترتيب · دافنشي · تصحيح · node order · resolve · primary correction · workflow · تصحيح الألوان · عقد التلوين · خطوات التلوين · color correction · davinci · look node

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow/references/look-scopes.md`
- `100-superskills/skills/davinci-resolve-pipeline/references/color-grading-order.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-11` لوكات LUT مع بديل حتمي / LUT looks with deterministic buildCube fallback (install)
- `COLOR-12` كشف التلوين بالمقارنة / Grade Split Reveal (flat → graded sweep) (install)
- `COLOR-14` كشف اللوج قبل LUT / Log detection before a conversion LUT (proven)
- `COLOR-15` التعريض حسب وقت اليوم / Exposure bands by time of day + cut jump caps (proven)

### `COLOR-14` — كشف اللوج قبل LUT / Log detection before a conversion LUT

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لا تطبق LUT تحويل Log إلا على لقطة ثبت أنها Log؛ وسم bt709 والمظهر الباهت ليسا دليلًا. / Apply a Log→Rec.709 LUT only to clips proven Log; a bt709 tag or a flat look is not evidence.

**متى:** قبل تطبيق LUT تحويل من Log إلى Rec.709، للتأكد أن اللقطة مصورة Log فعلًا لا باهتة فقط / before applying a Log→Rec.709 conversion LUT, to verify the clip is truly Log and not just flat

**كيف:** Priority: user profile > NLE input colour space/gamma containing 'log' > `ffprobe -show_streams -of json` color_transfer containing 'log' > 8-bit yuv420p ⇒ not Log (Apple Log / I-Log are 10-bit). Some Log files are tagged bt709. Then `lut3d=Log_to_Rec709.cube` (65-point), once only. `--selftest` passed in this container on 2026-10-16 (PYTHONPATH = the exposure skill's scripts). Live CDL writes need DaVinci Resolve Studio (paid app, not here); in this container apply the same numbers with FFmpeg.

**المعاملات:** 10-bit required for Apple Log / I-Log; 65-point cube

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** لوج · تحويل · آيفون · log · apple log · ffprobe · color_transfer · rec709 · تصوير لوج · فيديو باهت · كشف الصيغة · log footage · conversion lut · 10-bit

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-atlas/skills/1096-akbun-editvideo/2435-akbun-davinciresolve-logconvert/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2435-akbun-davinciresolve-logconvert/scripts/logconvert.py`

#### 7. قدرات قريبة في العائلة

- `COLOR-12` كشف التلوين بالمقارنة / Grade Split Reveal (flat → graded sweep) (install)
- `COLOR-13` ترتيب عقد التلوين / Grade order: technical before creative (documented)
- `COLOR-15` التعريض حسب وقت اليوم / Exposure bands by time of day + cut jump caps (proven)
- `COLOR-16` توازن الأبيض بالبكسلات المحايدة / Neutral-pixel white balance (proven)

### `COLOR-15` — التعريض حسب وقت اليوم / Exposure bands by time of day + cut jump caps

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لا تساوِ إضاءة كل اللقطات: الليل أغمق والساعة الذهبية الأسطع، وحدّ أقصى لقفزة الإضاءة بين لقطتين متتاليتين حتى لا تتعب العين. / Don't normalise everything: night darker, golden hour brightest, and cap the brightness jump between adjacent cuts to avoid flicker fatigue.

**متى:** حين تختلف إضاءة اللقطات بين ليل ونهار وغروب ويريد المستخدم ضبطها دون تسويتها ومنع قفزات الإضاءة بين القطعات / when matching exposure across night, day and golden-hour shots while capping jumps between cuts

**كيف:** Measure median luma (10-bit 0–1023): night 120–280, morning 320–460, day 420–560, golden 440–600, blue hour 310–485. Adjacent tail→head difference ≤60 same period / ≤120 across periods; per-clip shift ≤±120; >0.5% pixels clipped lowers target by 40; tolerance 15; sunrise/sunset windows ±30 min / 1.5 h. FFmpeg: `signalstats` YAVG → `eq=brightness/gamma`. `--selftest` passed in this container on 2026-10-16 (PYTHONPATH = the exposure skill's scripts). Live CDL writes need DaVinci Resolve Studio (paid app, not here); in this container apply the same numbers with FFmpeg.

**المعاملات:** bands 120–280 / 320–460 / 420–560 / 440–600 / 310–485; jump ≤60/≤120

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إضاءة · تعريض · وقت اليوم · exposure · time of day · signalstats · shot matching · توحيد الإضاءة · ساعة ذهبية · قفزة الإضاءة · brightness · flicker · luma

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-atlas/skills/1096-akbun-editvideo/2434-akbun-davinciresolve-exposure/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2434-akbun-davinciresolve-exposure/scripts/exposure_scope.py`

#### 7. قدرات قريبة في العائلة

- `COLOR-13` ترتيب عقد التلوين / Grade order: technical before creative (documented)
- `COLOR-14` كشف اللوج قبل LUT / Log detection before a conversion LUT (proven)
- `COLOR-16` توازن الأبيض بالبكسلات المحايدة / Neutral-pixel white balance (proven)
- `COLOR-17` تباين حول محور مع حماية القص / Pivot contrast with clip guard (proven)

### `COLOR-16` — توازن الأبيض بالبكسلات المحايدة / Neutral-pixel white balance

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تقدير الصبغة من البكسلات الرمادية متوسطة الإضاءة، وتثبيت الأخضر وتحريك الأحمر والأزرق — مع خيار إبقاء دفء أو برودة مقصودة. / Estimate the cast from low-saturation mid-brightness pixels, hold G and move R/B, optionally keeping a deliberate warm or cool bias.

**متى:** حين يكون في الفيديو أو الصورة ميل لوني غير مرغوب ويحتاج ضبط توازن الأبيض تلقائيًا / when footage has an unwanted colour cast and needs automatic white balance, optionally keeping a warm or cool bias

**كيف:** Downscale to 320 px; neutral = max channel 25–85% and saturation ≤20%; need ≥0.5% of pixels; target R−B = 0 (or +30 warm / −20 cool on request); CDL Offset ±0.10, Slope 1±0.20, ≤3 secant iterations. FFmpeg: colorbalance / colortemperature / colorchannelmixer, or `grayworld` (built in here). `--selftest` passed in this container on 2026-10-16 (PYTHONPATH = the exposure skill's scripts). Live CDL writes need DaVinci Resolve Studio (paid app, not here); in this container apply the same numbers with FFmpeg.

**المعاملات:** R−B 0/+30/−20; offset ±.10; slope 1±.20

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** توازن الأبيض · صبغة · white balance · cast · grayworld · neutral · ضبط الأبيض · ميل لوني · تصحيح الصبغة · auto white balance · colortemperature

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-atlas/skills/1096-akbun-editvideo/2444-akbun-davinciresolve-whitebalance/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2444-akbun-davinciresolve-whitebalance/scripts/whitebalance.py`

#### 7. قدرات قريبة في العائلة

- `COLOR-14` كشف اللوج قبل LUT / Log detection before a conversion LUT (proven)
- `COLOR-15` التعريض حسب وقت اليوم / Exposure bands by time of day + cut jump caps (proven)
- `COLOR-17` تباين حول محور مع حماية القص / Pivot contrast with clip guard (proven)
- `COLOR-18` أرضية تشبع وانحدار سينمائي / Saturation floor with film roll-off (proven)

### `COLOR-17` — تباين حول محور مع حماية القص / Pivot contrast with clip guard

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تباين S حول نقطة ارتكاز تناسب فضاء العقدة، ويتراجع تلقائيًا إذا بدأ السواد أو البياض بالقص. / S-contrast around a pivot matched to the node space that backs off automatically if blacks or whites clip.

**متى:** حين تبدو الصورة مسطحة وتحتاج تباينًا أقوى دون أن يحترق الأبيض أو ينسحق الأسود / when a flat image needs stronger S-contrast without clipping blacks or whites

**كيف:** Default 1.15 (range 0.5–1.5), pivot 0.435 on the LUT path, 0.336 for DaVinci Intermediate; clipping if p1 < 16 or p99 > 1008 (10-bit) or >0.5% clipped → reduce, max 3 retries, stop at 1.0. FFmpeg: curves S or eq=contrast with a pivoted lutyuv. `--selftest` passed in this container on 2026-10-16 (PYTHONPATH = the exposure skill's scripts). Live CDL writes need DaVinci Resolve Studio (paid app, not here); in this container apply the same numbers with FFmpeg.

**المعاملات:** 1.15; pivot .435/.336; p1<16, p99>1008

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تباين · contrast · pivot · clipping · s-curve · صورة مسطحة · منحنى S · احتراق الأبيض · flat image · contrast curve

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-atlas/skills/1096-akbun-editvideo/2432-akbun-davinciresolve-contrast/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2432-akbun-davinciresolve-contrast/scripts/contrast.py`

#### 7. قدرات قريبة في العائلة

- `COLOR-15` التعريض حسب وقت اليوم / Exposure bands by time of day + cut jump caps (proven)
- `COLOR-16` توازن الأبيض بالبكسلات المحايدة / Neutral-pixel white balance (proven)
- `COLOR-18` أرضية تشبع وانحدار سينمائي / Saturation floor with film roll-off (proven)
- `COLOR-19` تعزيز السماء فقط / Sky hue-window boost (proven)

### `COLOR-18` — أرضية تشبع وانحدار سينمائي / Saturation floor with film roll-off

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أضف تشبعًا فقط للقطات الباهتة عن نطاق وقتها (لا تنقص أبدًا)، بحد 1.25، واخفض التشبع في الظلال والإضاءات العالية كما يفعل الفيلم. / Only add saturation to clips below their time-of-day band (never remove), capped at 1.25, rolling saturation off in shadows and highlights like film.

**متى:** حين تبدو بعض اللقطات باهتة الألوان ويريد المستخدم رفع التشبع بحد آمن مع خفضه في الظلال والإضاءات كالفيلم / when dull clips need a capped saturation lift with film-like roll-off in shadows and highlights

**كيف:** Bands (mean max−min, 10-bit): morning 50–110, day 60–120, afternoon 60–130, evening 45–100, night 30–80; Sat = floor/measured ≤1.25; roll-off below 15% and above 85% luma down to 60%. FFmpeg: eq=saturation / hue=s plus a luma-selective lutyuv. `--selftest` passed in this container on 2026-10-16 (PYTHONPATH = the exposure skill's scripts). Live CDL writes need DaVinci Resolve Studio (paid app, not here); in this container apply the same numbers with FFmpeg.

**المعاملات:** cap 1.25; roll-off 15%/85% → 60%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تشبع · saturation · roll-off · film · vibrance · ألوان باهتة · حيوية الألوان · زيادة الألوان · dull colors · color boost

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-atlas/skills/1096-akbun-editvideo/2440-akbun-davinciresolve-saturation/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2440-akbun-davinciresolve-saturation/scripts/saturation.py`

#### 7. قدرات قريبة في العائلة

- `COLOR-16` توازن الأبيض بالبكسلات المحايدة / Neutral-pixel white balance (proven)
- `COLOR-17` تباين حول محور مع حماية القص / Pivot contrast with clip guard (proven)
- `COLOR-19` تعزيز السماء فقط / Sky hue-window boost (proven)
- `COLOR-20` لوكات مقاسة بأهداف السكوب / Scope-target looks (Japan summer, New York, Still, Tokyo night) (documented)

### `COLOR-19` — تعزيز السماء فقط / Sky hue-window boost

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تعميق السماء الزرقاء وحدها بنافذة لونية ناعمة حول 215°، دون لمس العشب أو البشرة. / Deepen blue skies only, with a soft hue window around 215°, leaving grass and skin alone.

**متى:** حين يريد المستخدم سماء أعمق زرقة دون أن يتغير لون العشب أو البشرة / when the user wants a deeper blue sky without touching grass or skin tones

**كيف:** Resolve DCTL: weight w falls off outside 215° ±20°, sat × (1 + 0.25w), lum × (1 − 0.1w), measured on the upper half. FFmpeg 6.1 here: `huesaturation=colors=b+c:saturation=0.25:intensity=-0.04:strength=5` — tested on a synthetic frame: sky #7fa8d8→#70a0da while grass #6b8a3c and skin #d9a27a stayed identical. `--selftest` passed in this container on 2026-10-16 (PYTHONPATH = the exposure skill's scripts). Live CDL writes need DaVinci Resolve Studio (paid app, not here); in this container apply the same numbers with FFmpeg. (code snippet in references/powers/color-palette-grading.md)

**المعاملات:** hue 215° width 40° sat 1.25 lum 0.9; ffmpeg strength 5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سماء · أزرق · تحديد لوني · sky · qualifier · huesaturation · secondary · تعميق السماء · لون البشرة · تلوين انتقائي · blue sky · selective color · hue window

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-atlas/skills/1096-akbun-editvideo/2442-akbun-davinciresolve-sky/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2442-akbun-davinciresolve-sky/scripts/sky.py`

#### 7. قدرات قريبة في العائلة

- `COLOR-17` تباين حول محور مع حماية القص / Pivot contrast with clip guard (proven)
- `COLOR-18` أرضية تشبع وانحدار سينمائي / Saturation floor with film roll-off (proven)
- `COLOR-20` لوكات مقاسة بأهداف السكوب / Scope-target looks (Japan summer, New York, Still, Tokyo night) (documented)
- `COLOR-21` توجيه التلوين حسب اللقطة وأرضية الإضاءة / Per-shot-type direction, one light floor, value before colour (documented)

### `COLOR-20` — لوكات مقاسة بأهداف السكوب / Scope-target looks (Japan summer, New York, Still, Tokyo night)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لوكات إبداعية مكتوبة كأهداف قياس على مخرج Rec.709: نسب IRE لـP10/P50/P95 ونصف قطر عناقيد اللون على الفكتورسكوب. / Creative looks written as measurable targets on the Rec.709 output: P10/P50/P95 in IRE and colour-cluster radius on a normalised vectorscope.

**متى:** حين يريد المستخدم لوكًا مثل صيف اليابان أو نيويورك أو ليل طوكيو محددًا بقياسات IRE وفكتورسكوب / for creative looks (Japan summer, New York, Tokyo night) defined as measurable IRE and vectorscope targets

**كيف:** Y'=0.2126R'+0.7152G'+0.0722B', IRE=100·Y'; Cb=(B'−Y')/1.8556, Cr=(R'−Y')/1.5748; radius normalised to the 100% colour-bar hexagon. Build with curves/colorbalance/lut3d, compare +0/+1/+2 stop variants, then measure. (full table in references/powers/color-palette-grading.md)

**المعاملات:** see table

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سكوب · قياس · طوكيو · IRE · vectorscope · scopes · measured look · tokyo night · فكتورسكوب · لوك نيويورك · صيف اليابان · japan summer · new york

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-atlas/skills/1096-akbun-editvideo/2436-akbun-davinciresolve-look-japan-summer/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2437-akbun-davinciresolve-look-new-york/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2438-akbun-davinciresolve-look-still/SKILL.md`
- `kosif-atlas/skills/1096-akbun-editvideo/2439-akbun-davinciresolve-look-tokyo-night`

#### 7. قدرات قريبة في العائلة

- `COLOR-18` أرضية تشبع وانحدار سينمائي / Saturation floor with film roll-off (proven)
- `COLOR-19` تعزيز السماء فقط / Sky hue-window boost (proven)
- `COLOR-21` توجيه التلوين حسب اللقطة وأرضية الإضاءة / Per-shot-type direction, one light floor, value before colour (documented)
- `COLOR-22` تحليل حرارة اللون والميل والتشبع / Colour analysis: CCT, cast, colourfulness, 6-colour palette (proven)

### `COLOR-21` — توجيه التلوين حسب اللقطة وأرضية الإضاءة / Per-shot-type direction, one light floor, value before colour

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جدول تلوين لكل نوع لقطة، وأرضية إضاءة واحدة وسقف واحد للفيلم كله، والقيمة (الفاتح/الغامق) تُقرر قبل اللون. / A grade table per shot type, one luminance floor and ceiling per film, and value (light/dark) decided before hue.

**متى:** حين يجمع الفيلم لقطات متحدث وتسجيل شاشة وجرافيك ويحتاج توجيه تلوين لكل نوع وأرضية إضاءة واحدة / when a film mixes talking heads, screen recordings and graphics and needs per-type grade direction

**كيف:** Table shot type \| colour direction \| notes: talking head = base grade with warm ambient pull; screen recordings crisp, high-contrast on text; graphics on the brand background; animation free palette; drifting scenes get a correction note. Name one floor (deepest black) and the brightest section's ceiling — no jumps dark→white. Realistic tonal range > 150 of 255; peak saturation only in fire and eyes.

**المعاملات:** tonal range >150/255; one floor per film

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قيمة · إضاءة · توجيه · value · luminance floor · shot type · direction · تسجيل شاشة · متحدث للكاميرا · اتساق الإضاءة · screen recording · consistency

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-atlas/skills/3067-youtube/13229-creator-visual-director/SKILL.md`
- `100-superskills/skills/motion-director-pro/references/motion-floor.md`
- `kosif-studio/references/drawing-guide.md:62`

#### 7. قدرات قريبة في العائلة

- `COLOR-19` تعزيز السماء فقط / Sky hue-window boost (proven)
- `COLOR-20` لوكات مقاسة بأهداف السكوب / Scope-target looks (Japan summer, New York, Still, Tokyo night) (documented)
- `COLOR-22` تحليل حرارة اللون والميل والتشبع / Colour analysis: CCT, cast, colourfulness, 6-colour palette (proven)
- `COLOR-23` إزاحة الميرد واختيار الجل / Mired shift → CTO/CTB gel (proven)

### `COLOR-22` — تحليل حرارة اللون والميل والتشبع / Colour analysis: CCT, cast, colourfulness, 6-colour palette

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أداة تقرأ صورة أو إطارًا وتعطيك: حرارة اللون بالكلفن، وميله الدافئ/البارد، ومقدار الألوان، وتوزيع الإضاءة، وستة ألوان سائدة بحصصها. / Reads an image or frame and returns CCT in kelvin, warm/cool cast, colourfulness, tonal zones and six dominant colours with shares.

**متى:** حين يريد المستخدم معرفة حرارة لون صورة أو إطار بالكلفن وهل هو دافئ أم بارد وما ألوانه السائدة / when the user wants to measure an image's kelvin, warm/cool cast, colourfulness and six dominant colours

**كيف:** `python3 kosif-one/tools/kosif-omni/skills/kosif-vision/scripts/image_analyze.py FRAME.png` → JSON: exposure (p1/median/p99, clipped %, zones, verdict), colour (McCamy CCT via sRGB→linear→XYZ, valid 1000–25000 K; cast warm if R̄−B̄ > 12, cool if < −12; colourfulness = hypot(σrg, σyb) + 0.3·hypot(μrg, μyb) labelled <15 not … >82 highly) and palette (median-cut to 6 on a 256 px thumbnail). Ran here on a graded frame.

**المعاملات:** cast ±12; CCT 1000–25000 K; palette k=6 @256 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تحليل · كلفن · حرارة اللون · analysis · cct · kelvin · colourfulness · cast · palette · قياس الألوان · دافئ وبارد · ألوان سائدة · dominant colors · color temperature

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-one/tools/kosif-omni/skills/kosif-vision/scripts/image_analyze.py:100`
- `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:59`
- `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:120`

#### 7. قدرات قريبة في العائلة

- `COLOR-20` لوكات مقاسة بأهداف السكوب / Scope-target looks (Japan summer, New York, Still, Tokyo night) (documented)
- `COLOR-21` توجيه التلوين حسب اللقطة وأرضية الإضاءة / Per-shot-type direction, one light floor, value before colour (documented)
- `COLOR-23` إزاحة الميرد واختيار الجل / Mired shift → CTO/CTB gel (proven)
- `COLOR-24` استخراج الباليت وتسمية الألوان / Palette extraction, colour naming and ΔE (proven)

### `COLOR-23` — إزاحة الميرد واختيار الجل / Mired shift → CTO/CTB gel

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حساب حتمي: من حرارة إلى حرارة كم «ميرد» وأي جل يقرّبك — لتخطيط إضاءة لقطة أو برومبت أو مشهد ثلاثي الأبعاد مقنع. / Deterministic maths: mired shift between two colour temperatures and the nearest gel, for believable lighting in shots, prompts and 3D.

**متى:** حين يخطط المستخدم إضاءة لقطة أو مشهد ثلاثي الأبعاد ويريد معرفة الجل المناسب للانتقال من حرارة لون إلى أخرى / when planning lighting and you need the mired shift and nearest CTO/CTB gel between two colour temperatures

**كيف:** `echo '{"op":"mired","from_k":3200,"to_k":5600}' \| python3 light_calc.py` → shift = 1e6/to − 1e6/from. Ran here: −133.9 → Full CTB, 'cooler (blue)'. Gels: Full CTB −159, ½ CTB −68, ¼ CTB −30, ⅛ CTB −12, ⅛ CTO +20, ¼ CTO +42, ½ CTO +81, Full CTO +159.

**المعاملات:** 3200→5600 K = −133.9 mired → Full CTB

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كلفن · جل · إضاءة · mired · gel · cto · ctb · kelvin · lighting · فلتر إضاءة · حرارة اللون · تخطيط الإضاءة · color temperature · light planning

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-one/tools/kosif-omni/skills/kosif-lighting/scripts/light_calc.py:69`
- `kosif-one/tools/kosif-omni/skills/kosif-lighting/scripts/light_calc.py:22`
- `100-superskills/skills/kosif-montage-motion/scripts/omni/light_calc.py:69`

#### 7. قدرات قريبة في العائلة

- `COLOR-21` توجيه التلوين حسب اللقطة وأرضية الإضاءة / Per-shot-type direction, one light floor, value before colour (documented)
- `COLOR-22` تحليل حرارة اللون والميل والتشبع / Colour analysis: CCT, cast, colourfulness, 6-colour palette (proven)
- `COLOR-24` استخراج الباليت وتسمية الألوان / Palette extraction, colour naming and ΔE (proven)
- `COLOR-25` باليت وخلفية لكل نبضة من المرجع / Reference palette + background per beat (proven)

### `COLOR-24` — استخراج الباليت وتسمية الألوان / Palette extraction, colour naming and ΔE

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يسحب الألوان السائدة من أي مرجع ويسمّيها بأقرب اسم من 20 اسمًا بمسافة Lab، ويقيس الفرق ΔE — لبناء قفل أسلوب أو جملة يفهمها العميل. / Pulls dominant colours from any reference, names them by nearest Lab distance among 20 names, and measures ΔE — for a style lock or a client-readable sentence.

**متى:** حين يرسل المستخدم صورة أو مرجعًا ويريد استخراج ألوانه بأكواد hex وتسميتها أو قياس الفرق بين لونين / when the user wants dominant colours pulled from a reference, named, and compared by ΔE

**كيف:** mm_color.palette(img, k=5) → [{hex, share, name}], color_name(rgb), delta_e(c1,c2) — ran here (testsrc → #9DFE77 green 49.7%, #A300FC purple 31.3%). Studio qa.study → k-means k=6 (KMEANS_PP, 30 iters, eps 0.5, 3 attempts) into style_guide.md (needs OpenCV). Basma analyzeRef: 16–72 samples every 0.25 s at 40×40, 512-bucket RGB histogram weighted 0.25+saturation, keep colours with L1 > 90; darkest → bg, most saturated → accent.

**المعاملات:** 20 names; k 5–6; Basma L1 > 90

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** استخراج الألوان · باليت · تسمية · palette extraction · kmeans · delta e · color name · reference · ألوان الصورة · كود اللون · فرق اللون · hex codes · dominant colors · style lock

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:opencv` ← python3 -c "import opencv" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/mimic/mm_color.py`
- `kosif-studio/motion/qa.py:383`
- `app/public/js/00_editor.js:1299`

#### 7. قدرات قريبة في العائلة

- `COLOR-22` تحليل حرارة اللون والميل والتشبع / Colour analysis: CCT, cast, colourfulness, 6-colour palette (proven)
- `COLOR-23` إزاحة الميرد واختيار الجل / Mired shift → CTO/CTB gel (proven)
- `COLOR-25` باليت وخلفية لكل نبضة من المرجع / Reference palette + background per beat (proven)
- `COLOR-26` نقل رينهارد إلى LUT لكل لقطة / Reinhard Lab transfer → per-shot .cube (proven)

### `COLOR-25` — باليت وخلفية لكل نبضة من المرجع / Reference palette + background per beat

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يقسم فيديو مرجعيًا إلى نبضات (قطع، ذوبان، دخول) ويعطي كل نبضة لون خلفية وباليت، بدقة ±8 لكل قناة في الاختبار. / Splits a reference video into beats (cuts, dissolves, entrances) and gives each beat a background hex and palette, within ±8 per channel on synthetic tests.

**متى:** حين يحلل المستخدم فيديو مرجعيًا ويريد لون الخلفية والباليت لكل نبضة أو مقطع / when breaking down a reference video into beats (cuts, dissolves, entrances) with a background hex and palette each

**كيف:** `analyze.analyze(film, out)` → analysis.json {width, height, aspect, duration, beats:[{t0,t1,background,palette:[{hex}]}], scenes, audio:{lufs}} + overview.jpg, timeline.jpg, brief.json and 3 frames per beat; beats ≤3.05 s. tests/test_analyze.py ran here: 5 tests OK.

**المعاملات:** ±8/channel; beats ≤3.05 s; 3 frames per beat

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مرجع · تحليل · نبضة · reference · beats · background · breakdown · فيديو مرجعي · لون الخلفية · تفكيك المرجع · scene palette · reference analysis

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `100-superskills/skills/kosif-montage-motion/tests/test_analyze.py:50`
- `100-superskills/skills/kosif-montage-motion/tests/test_analyze.py:39`

#### 7. قدرات قريبة في العائلة

- `COLOR-23` إزاحة الميرد واختيار الجل / Mired shift → CTO/CTB gel (proven)
- `COLOR-24` استخراج الباليت وتسمية الألوان / Palette extraction, colour naming and ΔE (proven)
- `COLOR-26` نقل رينهارد إلى LUT لكل لقطة / Reinhard Lab transfer → per-shot .cube (proven)
- `COLOR-27` مطابقة اللقطات بنقل لوني محدود / Bounded colour transfer + Hungarian shot match (proven)

### `COLOR-26` — نقل رينهارد إلى LUT لكل لقطة / Reinhard Lab transfer → per-shot .cube

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يطابق إحصاءات Lab للقطة جديدة مع لقطة مرجعية ويخبزها في LUT بحجم 33³ يُطبق لكل لقطة على حدة. / Matches a new shot's Lab statistics to a reference shot and bakes it into a 33³ LUT applied per shot.

**متى:** حين يريد المستخدم أن تشبه ألوان لقطة جديدة لقطة مرجعية وتُحفظ المطابقة كملف LUT لكل لقطة / when a new shot must match a reference shot's colours, baked into a per-shot 33³ .cube

**كيف:** lab_stats(src) / lab_stats(ref) → reinhard_lut(src, dst, size=33, strength=0.85, max_gain=2.2) → write_cube → apply_lut or FFmpeg lut3d. Ran here: mean Lab (69.0, 14.8, 10.3) moved toward the sodium_night reference (62.7, 11.7, 17.1) → (64.4, 10.4, 16.1); the written .cube also applied with ffmpeg lut3d (rc=0). Gains clamped so flat sources cannot explode. (code snippet in references/powers/color-palette-grading.md)

**المعاملات:** size 33; strength .85; max_gain 2.2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مطابقة · نقل اللون · رينهارد · color transfer · reinhard · lab · match · lut per shot · مطابقة الألوان · توحيد اللقطات · لقطة مرجعية · color match · 3d lut · reference shot

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/mimic/mm_color.py`
- `kosif-tool/.claude/skills/kosif-superpowers/scripts/mimic/mm_build.py`

#### 7. قدرات قريبة في العائلة

- `COLOR-24` استخراج الباليت وتسمية الألوان / Palette extraction, colour naming and ΔE (proven)
- `COLOR-25` باليت وخلفية لكل نبضة من المرجع / Reference palette + background per beat (proven)
- `COLOR-27` مطابقة اللقطات بنقل لوني محدود / Bounded colour transfer + Hungarian shot match (proven)
- `COLOR-28` إصلاح تلقائي ومطابقة مرجع في «بصمة» / Basma measured auto-fix, reference match and look classifier (install)

### `COLOR-27` — مطابقة اللقطات بنقل لوني محدود / Bounded colour transfer + Hungarian shot match

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يختار لكل لقطة مرجعية أنسب مقطع ونقطة بداية من مكتبتك (لون، تباين، تشبع، حركة) بالتعيين المجري، ثم ينقل اللون بمكسب وإزاحة محدودين لا ينفلتان. / Picks, for every reference shot, the best pool clip and in-point (colour, contrast, saturation, motion) by Hungarian assignment, then transfers colour with clamped gain/offset.

**متى:** حين يريد المستخدم تقليد مونتاج مرجعي باختيار أنسب مقطع من مكتبته لكل لقطة ثم نقل اللون إليه دون مبالغة / when recreating a reference edit: best pool clip per shot, then a clamped colour transfer

**كيف:** `mimic match PROJECT/study --pool POOL [--set N=file@sec] [--strength 0.7]`; colour_transfer(look{mean,std}, mean, std, strength) → per channel (gain, offset) with 0.6 ≤ gain ≤ 1.6 and −120 ≤ offset ≤ 120; windows containing source cuts are rejected. Real study: costs 0.356–0.602, gains .82–1.6, offsets −73…+113. tests/test_mimic.py ran here: 10 tests OK.

**المعاملات:** gain .6–1.6; offset ±120; strength .7

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مطابقة · محاكاة · مونتاج · mimic · hungarian · shot match · colour transfer · تقليد مونتاج · اختيار اللقطات · مكتبة مقاطع · reference edit · clip pool

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `100-superskills/skills/kosif-montage-motion/tests/test_mimic.py:91`
- `100-superskills/skills/kosif-montage-motion/references/mimic.md`
- `kosif-one/projects/mimic-jumuah/study/match.json`

#### 7. قدرات قريبة في العائلة

- `COLOR-25` باليت وخلفية لكل نبضة من المرجع / Reference palette + background per beat (proven)
- `COLOR-26` نقل رينهارد إلى LUT لكل لقطة / Reinhard Lab transfer → per-shot .cube (proven)
- `COLOR-28` إصلاح تلقائي ومطابقة مرجع في «بصمة» / Basma measured auto-fix, reference match and look classifier (install)
- `COLOR-29` تغيير لون بلون مع الحفاظ على الظل / Local recolour A→B keeping shading (Arabic requests) (proven)

### `COLOR-28` — إصلاح تلقائي ومطابقة مرجع في «بصمة» / Basma measured auto-fix, reference match and look classifier

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يصلح الفيديو المعتم أو المسطح أو المصبوغ من بكسلاته بلا ذكاء اصطناعي ويشرح الإصلاح بالعربية، ويطابق مقطعك مع مرجع، ويسمّي لوك المرجع. / Fixes dark/flat/cast footage from its own pixels without AI and explains the fix in Arabic, matches a clip to a reference, and labels the reference's look.

**متى:** حين يكون الفيديو معتمًا أو مسطحًا أو مصبوغًا ويريد المستخدم إصلاحًا تلقائيًا يُشرح بالعربية أو مطابقته مع مرجع / when dark, flat or tinted footage needs a measured auto-fix explained in Arabic, or a match to a reference

**كيف:** measureFix(): luma percentiles p02/p50/p98; contrast = clamp(200/range, 0.9, 1.3) when range < 200; brightness toward mid 118 (0.85–1.3) when mid outside 112–150; saturation clamp(0.24/s, 1, 1.25) when 0.05 < s < 0.18; grey-world on near-neutral pixels (s < 0.22, 50 < l < 215, ≥6% of pixels) → per-channel gains 0.82–1.18 as a multiply colour. Match: contrast ratio clamp 0.8–1.4, saturate 0.5–1.6, brightness 0.8–1.2, tint = reference mean hex, bw when ref saturation < 0.08, letterbox copied. DNA classifier: sat < 0.07 → bw; blue shadows > 6 with red highlights > 10 → teal_orange; warmth > 0.1 → golden (sat > 0.3) or warm; warmth < −0.05 → blue_hour (mean L < 90) or cool; contrast > 0.26 & sat > 0.32 → clean; sat > 0.45 & dark → cyber. Runs inside the Basma editor (Vite app).

**المعاملات:** contrast .9–1.3; gains .82–1.18; mid 118

**التثبيت:** cd /home/user/app && npm install && npm run dev

**الوسوم:** إصلاح تلقائي · مطابقة مرجع · بصمة · auto fix · grey world · reference match · look classifier · فيديو معتم · تحسين تلقائي · تصحيح ألوان · dark video · auto color correction

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:esbuild` ← npm ls esbuild أو وجود node_modules/esbuild
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `app/public/js/00_editor.js:2976`
- `app/public/js/00_editor.js:2364`
- `app/public/js/10_studio.js:1213`

#### 7. قدرات قريبة في العائلة

- `COLOR-26` نقل رينهارد إلى LUT لكل لقطة / Reinhard Lab transfer → per-shot .cube (proven)
- `COLOR-27` مطابقة اللقطات بنقل لوني محدود / Bounded colour transfer + Hungarian shot match (proven)
- `COLOR-29` تغيير لون بلون مع الحفاظ على الظل / Local recolour A→B keeping shading (Arabic requests) (proven)
- `COLOR-30` ألوان الشعار الحقيقية / Logo true colours + antialias-blend detection (install)

### `COLOR-29` — تغيير لون بلون مع الحفاظ على الظل / Local recolour A→B keeping shading (Arabic requests)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** «غيّر الأحمر إلى أزرق» تُنفذ محليًا: قناع لوني بتسامح، ثم استبدال الصبغة مع إبقاء الطيات والظلال، وفهم طلبات العربية والإنجليزية. / 'Change red to blue' done locally: a tolerant colour mask, hue replacement that keeps folds and shading, and parsing of Arabic or English requests.

**متى:** حين يطلب المستخدم «غيّر الأحمر إلى أزرق» أو تغيير لون عنصر في صورة مع بقاء الظلال والطيات / when the user asks to change one colour to another in an image while keeping folds and shading

**كيف:** edit_pack TOOLS: recolor(img, src_hex, dst_hex, tolerance=40, region=None, keep_shading=True) via HSV (V scaled by dst/src, S scaled), plus adjust(brightness/contrast/saturation/sharpness), tint(hex, 0.3), erase(softness 14). parse_colour_request('غيّر الأحمر إلى أزرق') → ('#d62828', '#2f6fd6'). Ran here: gold #c9a227 → #1ac5d9 (target #19c3d9) while a red block stayed #b5432c.

**المعاملات:** tolerance 40–42; tint .3; Pillow only

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تغيير اللون · تلوين جزئي · recolor · change color · mask · tint · arabic request · استبدال لون · تعديل صورة · غير اللون · replace color · color swap · pillow

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `100-superskills/skills/pixel-studio-painter/scripts/edit_pack.py:50`
- `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-27` مطابقة اللقطات بنقل لوني محدود / Bounded colour transfer + Hungarian shot match (proven)
- `COLOR-28` إصلاح تلقائي ومطابقة مرجع في «بصمة» / Basma measured auto-fix, reference match and look classifier (install)
- `COLOR-30` ألوان الشعار الحقيقية / Logo true colours + antialias-blend detection (install)
- `COLOR-31` هوية كاملة من لون واحد / One hex → full WCAG token set (+ 9 accent presets) (proven)

### `COLOR-30` — ألوان الشعار الحقيقية / Logo true colours + antialias-blend detection

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يستخرج ألوان الشعار الفعلية كمتوسطات للبكسلات النقية، ويتعرف على بكسلات التنعيم عند الحواف فلا يحسبها ألوانًا جديدة. / Finds a logo's true colours as means of pure pixels and recognises antialias edge blends so they are not mistaken for palette colours.

**متى:** حين يريد المستخدم ألوان الشعار الحقيقية بأكواد hex من صورة دون أن تختلط بها ألوان التنعيم عند الحواف / when extracting a logo's exact colours from an image, ignoring antialiased edge blends

**كيف:** vectorize._palette(rgba, max_colors=16, min_share=.001): quantise /8 to rank, keep candidates ≥30 apart, average everything within 22. _edge_blends tests 4 neighbour directions (neighbour contrast > 40, t in 0.08–0.92, distance < 18); _mixture least-squares 2–3 colour weights 6–94% within tol 16. vectorize.py imports OpenCV, which is not installed here.

**المعاملات:** max 16 colours; ≥30 apart; blend tol 16

**التثبيت:** pip install opencv-python-headless

**الوسوم:** شعار · ألوان دقيقة · logo colors · antialias · vectorize · brand · لوجو · ألوان الهوية · استخراج ألوان · brand colors · logo palette · hex

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:opencv` ← python3 -c "import opencv" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-studio/vectorize.py:45`
- `kosif-studio/vectorize.py:24`
- `kosif-studio/scenes/aghnam_logo.json`

#### 7. قدرات قريبة في العائلة

- `COLOR-28` إصلاح تلقائي ومطابقة مرجع في «بصمة» / Basma measured auto-fix, reference match and look classifier (install)
- `COLOR-29` تغيير لون بلون مع الحفاظ على الظل / Local recolour A→B keeping shading (Arabic requests) (proven)
- `COLOR-31` هوية كاملة من لون واحد / One hex → full WCAG token set (+ 9 accent presets) (proven)
- `COLOR-32` هوية «دفتر KOSIF» / Dafter KOSIF ledger identity (default, light + night) (proven)

### `COLOR-31` — هوية كاملة من لون واحد / One hex → full WCAG token set (+ 9 accent presets)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تعطي لونًا واحدًا فتحصل على ثيم فاتح وداكن وألوان حالات ومسافات وأحجام خط وتوقيتات حركة — كل زوج يمر اختبار التباين — مع كتلة CSS جاهزة. / Give one colour and get light + dark themes, status colours, spacing, type scale and motion tokens — every pair contrast-checked — plus a ready CSS block.

**متى:** حين يعطي المستخدم لونًا واحدًا لعلامته ويريد ثيمًا فاتحًا وداكنًا بألوان حالات ومسافات وخطوط / when one brand hex must become light and dark themes, status colours and type tokens, all contrast-checked

**كيف:** `echo '{"brand":"#8a5a2b","name":"k"}' \| python3 design_tokens.py` (also MCP kosif_design_tokens): lightness is walked until text pairs reach 4.6:1 and UI pairs 3:1; CSS has :root, prefers-color-scheme dark guarded by :not([data-theme=light]), [data-theme=dark] and reduced-motion 0 ms. Ran here: #8a5a2b → dark brand #d4985e, light ink #221911 on #faf9f7 = 16.42:1, all 22 checked pairs pass. Runtime twin in EARTH: accentTokens(hex, dark, surface) mixes toward black (light) until 3:1 or toward white (dark) until 4:1 in steps of .08 (max .9), on-brand white if ≥3.2 else #06101f, brand-2 = 32% white mix, deep = 55% toward #0b1f3a, soft = 11% (22% dark), gradient 135° b2 0% / c 55% / deep 100%. Nine accent presets feed it: كوبالت #2340c4, زمردي #0f9d6c, أخضر وطني #006c35, فيروزي #0e8a9a, ملكي #6b4ee6, عنبري #c2410c, ذهبي #b8862b, قرمزي #d0343f, فحمي #3b4a5e. (code snippet in references/powers/color-palette-grading.md)

**المعاملات:** text 4.6:1, UI 3:1; status hues ok 140° warn 35° bad 4° info 200° (s .65); space 4–64 px; type ratio 1.25; t-fast 120 ms, t 180 ms; ease cubic-bezier(.2,.8,.2,1)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هوية · لون واحد · رموز تصميم · تباين · brand tokens · design tokens · wcag · dark mode · accent · ثيم · وضع داكن · هوية بصرية · color palette · css variables · theme generator

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:axe` ← npm ls axe أو وجود node_modules/axe
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-one/tools/kosif-omni/skills/kosif-web-design/scripts/design_tokens.py:62`
- `kosif-earth-ci-fork/ui/layouts/shell.js:76`
- `kosif-earth-ci-fork/ui/layouts/shell.js:69`
- `kosif-atlas/skills/196-landing/621-landing/scripts/brand_palette_validator.py`

#### 7. قدرات قريبة في العائلة

- `COLOR-29` تغيير لون بلون مع الحفاظ على الظل / Local recolour A→B keeping shading (Arabic requests) (proven)
- `COLOR-30` ألوان الشعار الحقيقية / Logo true colours + antialias-blend detection (install)
- `COLOR-32` هوية «دفتر KOSIF» / Dafter KOSIF ledger identity (default, light + night) (proven)
- `COLOR-33` مظاهر KOSIF EARTH / KOSIF EARTH identity looks (14) (ready)

### `COLOR-32` — هوية «دفتر KOSIF» / Dafter KOSIF ledger identity (default, light + night)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الهوية الافتراضية: ورق دفاتر كريمي، بطاقات بيضاء دافئة، حبر فحمي للعناوين والأزرار، ولون زعفران واحد للعلامات والحالة النشطة — ونسخة ليلية. / The default identity: cream ledger paper, warm white cards, charcoal ink for rails/headings/buttons and a single saffron accent — with a night twin.

**متى:** حين يحتاج المستخدم الهوية الافتراضية لـKOSIF بورق كريمي وحبر فحمي ولون زعفران واحد، أو نسختها الليلية / for KOSIF's default ledger identity: cream paper, charcoal ink and one saffron accent, plus its night twin

**كيف:** html[data-look=kosif][data-brand=ledger] (+ [data-theme=dark]); map bg/ink/accent to scene background, type and highlight. Saffron text uses the darker step #a53e07 (5.9:1); ink #1d1814 is 17:1. identity_unity.test.mjs ran here (5/5 pass).

**المعاملات:** light: bg #fbf8f3 surface #fffdf9 line #e3d9cc ink #1d1814 ink-2 #4b4139 saffron #d9530e text #a53e07 soft #fbe9dc ok #2c7a4b warn #a76a10 bad #b3261e info #2f5f8f; night: bg #161310 surface #1c1814 ink #f5ede3 brand #f2732d gold-ink #ff9a5f grad 135° #ff9a5f→#f2732d 45%→#a53e07

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** دفتر · زعفران · هوية كاشف · كريمي · ledger · saffron · kosif identity · cream · هوية افتراضية · وضع ليلي · حبر فحمي · default theme · night mode

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-earth-ci-fork/ui/ds/tokens.css:263`
- `kosif-earth-ci-fork/ui/ds/tokens.css:284`
- `kosif-earth-ci-fork/docs/design/SQC-IDENTITY-ar.md`
- `kosif-earth-ci-fork/tools/identity_unity.test.mjs`

#### 7. قدرات قريبة في العائلة

- `COLOR-30` ألوان الشعار الحقيقية / Logo true colours + antialias-blend detection (install)
- `COLOR-31` هوية كاملة من لون واحد / One hex → full WCAG token set (+ 9 accent presets) (proven)
- `COLOR-33` مظاهر KOSIF EARTH / KOSIF EARTH identity looks (14) (ready)
- `COLOR-34` إعادة تلوين حسب الدور / Role-based palette remap (brandCSS) (proven)

### `COLOR-33` — مظاهر KOSIF EARTH / KOSIF EARTH identity looks (14)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أربعة عشر مظهرًا مختبرًا في واجهة المالك، منها عربية الروح (تراث الوادي، نجد الفاخر، الواحة، الدفتر المسطر) — كلها رموز CSS تنقلها مباشرة إلى مشهد. / Fourteen identity looks from the owner's app, several with Arabic character (Heritage Valley, Najd luxe, Oasis, Notebook) — CSS tokens you lift straight into a scene.

**متى:** حين يريد المستخدم مظهرًا بروح عربية مثل تراث الوادي أو نجد الفاخر أو الواحة وينقل ألوانه إلى مشهد / for an Arabic-flavoured identity look (Heritage Valley, Najd luxe, Oasis) lifted into a scene as CSS tokens

**كيف:** Select with [data-look=…] / [data-brand=…] (+ [data-theme=dark]); copy --sk-* values into :root of the composition. Cobalt & Ice is covered by identity_unity.test.mjs (ran here); the rest are owner CSS. Earth-office door forbids a full-image green tint or hue-rotate; intro amber is a title-card palette over space footage. (full table in references/powers/color-palette-grading.md)

**المعاملات:** see table

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نجد · تراث · واحة · كحلي وذهبي · najd · heritage · navy gold · identity · theme · هوية عربية · ألوان تراثية · مظاهر جاهزة · arabic style · css tokens · oasis

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-earth-ci-fork/ui/ds/tokens.css:162`
- `kosif-earth-ci-fork/ui/ds/tokens.css:378`
- `kosif-earth-ci-fork/ui/ds/tokens.css:7`
- `kosif-earth-ci-fork/ui/art/brand/earth-office-door.css`

#### 7. قدرات قريبة في العائلة

- `COLOR-31` هوية كاملة من لون واحد / One hex → full WCAG token set (+ 9 accent presets) (proven)
- `COLOR-32` هوية «دفتر KOSIF» / Dafter KOSIF ledger identity (default, light + night) (proven)
- `COLOR-34` إعادة تلوين حسب الدور / Role-based palette remap (brandCSS) (proven)
- `COLOR-35` تحويل انتقائي ذهبي→جليدي / Selective gold→ice hue rotation (image and video) (proven)

### `COLOR-34` — إعادة تلوين حسب الدور / Role-based palette remap (brandCSS)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يعيد كتابة أوراق أنماط مصممة بالكوبالت إلى هوية الدفتر حسب الدور: النص زعفران مقروء، الخلفيات المعبأة حبر، والخطوط زعفران — مع الحفاظ على الشفافية. / Rewrites cobalt-authored stylesheets into the ledger identity by role: text → readable saffron, filled backgrounds → ink, strokes → saffron, alpha suffixes kept.

**متى:** حين يريد المستخدم تحويل ملفات CSS مصممة بألوان الكوبالت إلى هوية الدفتر تلقائيًا حسب دور كل لون / when rewriting cobalt-coloured stylesheets into the ledger identity by role: text, filled backgrounds, strokes

**كيف:** brandCSS(css): three role regexes for #2340c4 (color: → #a53e07, background: → #1d1814, else → #d9530e), then a 44-pair hex table and an rgba() triplet table (e.g. #0b1030→#1d1814, #19c3d9→#f2732d, #f4f6fb→#fbf8f3, rgba(35,64,196,…)→rgba(217,83,14,…)). Used for print, letterhead, charts print CSS and presentations. identity_unity.test.mjs ran here (5/5).

**المعاملات:** 3 role rules + 44 hex pairs + rgba table

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إعادة تلوين · هوية · remap · rebrand · role · css rewrite · تغيير الهوية · استبدال الألوان · تحويل الثيم · color swap · stylesheet · brand migration

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-earth-ci-fork/ui/core/sk.js:348`
- `kosif-earth-ci-fork/tools/identity_unity.test.mjs`

#### 7. قدرات قريبة في العائلة

- `COLOR-32` هوية «دفتر KOSIF» / Dafter KOSIF ledger identity (default, light + night) (proven)
- `COLOR-33` مظاهر KOSIF EARTH / KOSIF EARTH identity looks (14) (ready)
- `COLOR-35` تحويل انتقائي ذهبي→جليدي / Selective gold→ice hue rotation (image and video) (proven)
- `COLOR-36` باليتات الشيدر كمتغيرات / Shader palettes as uniforms (Crystal World) (proven)

### `COLOR-35` — تحويل انتقائي ذهبي→جليدي / Selective gold→ice hue rotation (image and video)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يدير نطاق الذهبي فقط إلى سماوي جليدي بأوزان ناعمة، ويقرّب الكحلي نحو الكوبالت، ويترك الخشب والبشرة والأحمر كما هي — للصور وللفيديو إطارًا بإطار. / Rotates only the gold hue band to ice cyan with smooth weights, nudges navy to cobalt and leaves wood, skin and reds untouched — stills or MP4 frame by frame.

**متى:** حين يريد المستخدم تحويل الذهبي فقط في صورة أو فيديو إلى سماوي جليدي مع بقاء البشرة والخشب والأحمر كما هي / when only the gold tones in an image or video must turn ice cyan while skin, wood and reds stay untouched

**كيف:** `python3 tools/brand/recolor_ice.py IN OUT` (webp/png/jpg or mp4). NumPy HSV: w = smooth(h,18,30)·(1−smooth(h,62,74))·smooth(s,.08,.22); target hue 190+(h−45)·.35; blue band 196–248 pulled half-way to 228; s·(1−.1w), v·(1−.06w). Video: rawvideo rgb24 pipe → libx264 -preset slow -crf 24 yuv420p +faststart (audio dropped — re-mux the original audio). Ran here: #c9a227 → #34a6bd, red #b5432c unchanged, navy #0b1f3a → #0b1a3a.

**المعاملات:** gold ~22–68° → ice ~185–195°; crf 24; webp q82

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تحويل لوني · ذهبي · جليدي · hue rotation · selective color · recolor video · brand · تغيير لون · سماوي · ألوان الهوية · gold to cyan · hsv

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:numpy` ← python3 -c "import numpy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-earth-ci-fork/tools/brand/recolor_ice.py`
- `kosif-earth-ci-fork/docs/design/HIGGSFIELD_VISUALS_ar.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-33` مظاهر KOSIF EARTH / KOSIF EARTH identity looks (14) (ready)
- `COLOR-34` إعادة تلوين حسب الدور / Role-based palette remap (brandCSS) (proven)
- `COLOR-36` باليتات الشيدر كمتغيرات / Shader palettes as uniforms (Crystal World) (proven)
- `COLOR-37` باليتات منتجات التدقيق / KOSIF audit palettes + cascade-order theming (proven)

### `COLOR-36` — باليتات الشيدر كمتغيرات / Shader palettes as uniforms (Crystal World)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عالم بلوري ثلاثي الأبعاد بلوحتين (كوبالت وجليد / حبر وزعفران كهرماني) تُمرَّر كمتغيرات، ولا لون مثبت داخل الشيدر — والاختبار يفرض ذلك. / A crystal-world shader with two palettes (cobalt ice / ledger amber) passed as uniforms; no colour is hard-coded in the shader and a test enforces it.

**متى:** حين يبني المستخدم مشهد شيدر ثلاثي الأبعاد ويريد تبديل لوحته بين هويتين دون تثبيت أي لون داخل الكود / when a 3D shader scene must switch between brand palettes passed as uniforms, with no colour hard-coded

**كيف:** PALETTES.cobalt / PALETTES.ledger chosen from data-brand or an explicit option. cobalt iceA (.043,.063,.19) iceB (.10,.76,.85) skyB (.86,.95,1) rim (.60,.93,.97); ledger iceA (.114,.094,.078) iceB (.85,.33,.055) skyB (.98,.95,.90) rim (.98,.76,.55) snow (1,.9,.78). identity_unity.test.mjs ran here (5/5).

**المعاملات:** 2 palettes × iceA/iceB/skyB/rim/snow uniforms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شيدر · متغيرات · بلوري · shader uniforms · palette · webgl · identity · ثلاثي الأبعاد · تبديل الهوية · كوبالت · crystal · theme switch

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-earth-ci-fork/ui/art/crystal-world.js:102`
- `kosif-earth-ci-fork/tools/identity_unity.test.mjs`

#### 7. قدرات قريبة في العائلة

- `COLOR-34` إعادة تلوين حسب الدور / Role-based palette remap (brandCSS) (proven)
- `COLOR-35` تحويل انتقائي ذهبي→جليدي / Selective gold→ice hue rotation (image and video) (proven)
- `COLOR-37` باليتات منتجات التدقيق / KOSIF audit palettes + cascade-order theming (proven)
- `COLOR-38` ثيمات Kinetic Flow السبعة عشر / Kinetic-flow locked themes A–Q + custom R (proven)

### `COLOR-37` — باليتات منتجات التدقيق / KOSIF audit palettes + cascade-order theming

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لوحات «ريش الطيور» الفاتحة والداكنة، ولوحة القيادة النيلية، والثيم التحريري البنفسجي الذهبي الكريمي، ولوحات التراث والليل — مقفلة باختبارات، وطبقات ثيم تُرتب بالتحميل. / Feather light/dark, the indigo dashboard, the purple-gold-cream editorial theme, heritage and night palettes — locked by tests, themes layered by cascade order.

**متى:** حين يحتاج المستخدم ألوان لوحة قيادة أو تقرير تدقيق بثيم فاتح وداكن وترتيب صحيح لملفات الثيم / for dashboard and audit-report palettes with light/dark themes and a tested theme-file cascade order

**كيف:** Copy the :root block; switch html[data-theme=dark]; status hues: primary violet focus, teal done, amber attention, coral risk. Cascade: continuous-review.css → dashboard-theme.css → product-model.css → kosif-one-editorial-theme.css; the test asserts that order and that meta theme-color (#24113f) is a colour the final theme paints. palette.test.mjs (5/5) and dashboard-theme.test.js (5/5) ran here. (full table in references/powers/color-palette-grading.md)

**المعاملات:** see table

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تدقيق · بنفسجي وذهبي · ثيم · audit · dashboard · feather · cascade · dark theme · لوحة قيادة · وضع داكن · ألوان الحالات · status colors · light theme · editorial theme

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-audit-pro/app/globals.css:21`
- `kosif-audit-pro/tests/palette.test.mjs`
- `kosif-audit-studio/kosif-one-editorial-theme.css`
- `kosif-audit-studio/tests/dashboard-theme.test.js`

#### 7. قدرات قريبة في العائلة

- `COLOR-35` تحويل انتقائي ذهبي→جليدي / Selective gold→ice hue rotation (image and video) (proven)
- `COLOR-36` باليتات الشيدر كمتغيرات / Shader palettes as uniforms (Crystal World) (proven)
- `COLOR-38` ثيمات Kinetic Flow السبعة عشر / Kinetic-flow locked themes A–Q + custom R (proven)
- `COLOR-39` باليتات الافتتاحي الفيروسي / Viral-editorial palettes 1–3 + 80/20 rule (proven)

### `COLOR-38` — ثيمات Kinetic Flow السبعة عشر / Kinetic-flow locked themes A–Q + custom R

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سبعة عشر ثيمًا مقفلًا لفيديوهات التايبوغرافي الحركي: خلفية ولون بطل ولون صغير وخط وخامة وانتقال ونهاية — تُكرر حرفيًا في كل برومبت مقطع، مع ثيم R مخصص يتحقق من الـhex. / Seventeen locked kinetic-type themes (background, hero, small colour, font, finish, transition, end card) repeated verbatim in every clip prompt, plus a custom theme R with hex validation.

**متى:** حين يصنع المستخدم فيديو تايبوغرافي حركي ويريد ثيمًا مقفلًا (خلفية ولون وخط وانتقال) يتكرر في كل مقطع / for kinetic typography videos needing a locked theme repeated in every clip prompt, or a custom hex theme

**كيف:** kinetic-flow setup {"theme":"A"} → STYLE LOCK paragraph repeated in every clip; R requires background, accent (^#[0-9a-f]{6}$), font, finish, overlay, animation, transition (small defaults #333333, end card 'fade to black'); S copies a reference (COLOR-56). production-profiles.test.mjs ran here (10/10). (full table in references/powers/color-palette-grading.md)

**المعاملات:** 17 themes; 7 required keys for R

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ثيمات · تايبوغرافي · قفل الأسلوب · kinetic · themes · style lock · neon · gold noir · swiss · نصوص متحركة · ثيم مخصص · ستايل ثابت · kinetic typography · custom theme · prompt

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:4`
- `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:24-30,44-54`
- `fastify-motion-bro/tests/production-profiles.test.mjs:67-74`

#### 7. قدرات قريبة في العائلة

- `COLOR-36` باليتات الشيدر كمتغيرات / Shader palettes as uniforms (Crystal World) (proven)
- `COLOR-37` باليتات منتجات التدقيق / KOSIF audit palettes + cascade-order theming (proven)
- `COLOR-39` باليتات الافتتاحي الفيروسي / Viral-editorial palettes 1–3 + 80/20 rule (proven)
- `COLOR-40` باليتات أفلام المالك / Owner film palettes from shipped projects (ready)

### `COLOR-39` — باليتات الافتتاحي الفيروسي / Viral-editorial palettes 1–3 + 80/20 rule

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاث لوحات للمحرك التحريري: توقيع تحريري (أوف وايت + بنفسجي)، تقني داكن (رمادي أردوازي + فيروزي)، أكاديمي عالي التباين (كريمي + طوبي) — وكل تسلسل 80% محايد و20% لون واحد. / Three palettes for the editorial renderer — Signature Editorial, Dark Technical, High-Contrast Academic — and each sequence is ~80% neutral, ~20% one accent.

**متى:** حين يصنع المستخدم فيديو شرح تحريري ويحتاج لوحة جاهزة (فاتحة بنفسجية، تقنية داكنة، أكاديمية) بنسبة 80% محايد و20% لون / for editorial explainer videos needing one of three palettes with an ~80% neutral / 20% accent split

**كيف:** PALETTES['1'\|'2'\|'3'] → compileStoryboard.palette → editorial renderer. viral-editorial.test.mjs (7/7) and production-profiles.test.mjs (10/10) ran here.

**المعاملات:** 1: bg #F4F1EC grid #D7D4D0 accent #6134B9 text #24212A line #D5CFD9 shape #E6DFF5; 2: #1B252C / #36414A / #24DAD1 / #EFF8F7 / #364B50 / #24373B; 3: #F1E9DD / #D8CAB8 / #BC5935 / #2C2928 / #DFCEBD / #E9D1C0; 80/20

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تحريري · فيروسي · 80/20 · editorial · viral · palette · explainer · فيديو شرح · ألوان محايدة · فيروزي · dark technical · academic

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `fastify-motion-bro/scripts/viral-editorial.mjs:6`
- `fastify-motion-bro/docs/VIRAL-EDITORIAL-DNA.md:19`
- `fastify-motion-bro/tests/viral-editorial.test.mjs`

#### 7. قدرات قريبة في العائلة

- `COLOR-37` باليتات منتجات التدقيق / KOSIF audit palettes + cascade-order theming (proven)
- `COLOR-38` ثيمات Kinetic Flow السبعة عشر / Kinetic-flow locked themes A–Q + custom R (proven)
- `COLOR-40` باليتات أفلام المالك / Owner film palettes from shipped projects (ready)
- `COLOR-41` باليتات القوالب وخاناتها / Starter palettes and palette slots (proven)

### `COLOR-40` — باليتات أفلام المالك / Owner film palettes from shipped projects

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لوحات خرجت من أفلام ومشاريع حقيقية — كحلي وذهبي، عاجي وحبر وذهبي، نيون مختبري، مدينة ممطرة، بحر ليلي، نقطة حمراء — جاهزة للنسخ. / Palettes lifted from real shipped films and projects — navy/gold, ivory/ink/gold, lab neon, rainy neon city, night sea, red dot — ready to copy.

**متى:** حين يريد المستخدم باليت جاهزة من أفلام حقيقية مثل كحلي وذهبي أو مدينة نيون ممطرة أو بحر ليلي / when the user wants a ready palette from shipped films: navy/gold, ivory/ink, lab neon, rainy neon city, night sea

**كيف:** Copy the :root tokens or the hex roles; keep one carrier/accent per palette (COLOR-54). midnight_cat and duck-vs-dragon are tested-code; the rest are owner code. (full table in references/powers/color-palette-grading.md)

**المعاملات:** see table

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** باليت · كحلي وذهبي · نيون · ألوان أفلام · palette · navy gold · neon city · film palette · ألوان جاهزة · مدينة ممطرة · بحر ليلي · ready palette · night sea

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:23`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:14`
- `kosif-one/projects/duck-vs-dragon/duck_dragon.py:13-56`
- `fastify-motion-bro/web/motion.js:9-21`

#### 7. قدرات قريبة في العائلة

- `COLOR-38` ثيمات Kinetic Flow السبعة عشر / Kinetic-flow locked themes A–Q + custom R (proven)
- `COLOR-39` باليتات الافتتاحي الفيروسي / Viral-editorial palettes 1–3 + 80/20 rule (proven)
- `COLOR-41` باليتات القوالب وخاناتها / Starter palettes and palette slots (proven)
- `COLOR-42` ثيمات HyperFrames وعقد الرموز / HyperFrames themes + 18-token contract (ready)

### `COLOR-41` — باليتات القوالب وخاناتها / Starter palettes and palette slots

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قالب Canvas المختبر يبدأ بلوحة «كحلي وتركوازي» وخلفية شعاعية وشبكة 90 بكسل؛ وSTYLE.md فيه خانات الألوان؛ وقالب Remotion يأخذ لون التمييز كخاصية. / The tested canvas starter opens on 'midnight teal' with a radial backdrop and a 90 px grid; STYLE.md carries the colour slots; the Remotion starter takes the accent as a prop.

**متى:** حين يبدأ المستخدم مشروعًا من قالب ويحتاج ألوانه الافتراضية أو خانات الألوان في STYLE.md أو لون التمييز في Remotion / when starting from a template: its default palette, STYLE.md colour slots or the Remotion accent

**كيف:** html-canvas: --bg #0b1020 --ink #f3f7ff --muted #9fb0cc --accent #7ee8d2 --accent-2 #ffb86b; stage radial-gradient(#182446 → #0b1020 55%); grid rgba(255,255,255,.045) every 90 px at opacity .6. templates/STYLE.md §4.1 defaults (marked estimated): bg #0B0F19 fg #F5F7FA accent #FFB020 muted #8A93A6 line #2A3346. Remotion: ink #0b0d12, paper #f4f1ea, accent prop (default #ff7a1a, example #19c37d) + withAlpha(color, a) (appends hex byte or uses color-mix) — Remotion needs `npm i` in starters/remotion and is under the Remotion company license.

**المعاملات:** midnight teal; grid 90 px @ .045; STYLE.md 5 tokens; accent prop

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قالب · بداية · خانات الألوان · starter · scaffold · remotion · withAlpha · style.md · مشروع جديد · ألوان افتراضية · خلفية كحلية · default palette · accent color · canvas

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-tool/starters/html-canvas/index.html:9`
- `kosif-tool/templates/STYLE.md`
- `kosif-tool/starters/remotion/src/Film.tsx:49`
- `kosif-tool/starters/remotion/props.example.json`

#### 7. قدرات قريبة في العائلة

- `COLOR-39` باليتات الافتتاحي الفيروسي / Viral-editorial palettes 1–3 + 80/20 rule (proven)
- `COLOR-40` باليتات أفلام المالك / Owner film palettes from shipped projects (ready)
- `COLOR-42` ثيمات HyperFrames وعقد الرموز / HyperFrames themes + 18-token contract (ready)
- `COLOR-43` مكتبات باليتات جاهزة / Ready palette libraries (families, deck presets, recut themes, demo kit, dark ladders) (documented)

### `COLOR-42` — ثيمات HyperFrames وعقد الرموز / HyperFrames themes + 18-token contract

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ملف ثيم واحد يعيد تلوين كل المكونات لأنها تقرأ 18 متغير CSS نفسها (لوحة، خط، شكل، حركة) — وثلاثة ثيمات جاهزة: محايد، جريء، تحريري. / One theme file restyles every component because all read the same 18 CSS custom properties (palette, type, shape, motion); three ready themes: neutral, bold, editorial.

**متى:** حين يريد المستخدم تغيير ألوان وخطوط وحركة كل مكونات HyperFrames دفعة واحدة بملف ثيم واحد / when one theme file should restyle every HyperFrames component through 18 shared CSS custom properties

**كيف:** One :root defines --bg --fg --muted --surface --border --brand --accent --accent-2 --font-display --font-body --font-mono --radius --space-1..3 --dur-beat --ease-standard --ease-emphasis; primitives use var(--fg, #f8fafc) and never declare tokens in :root. Link themes/*.css before compositions (plain CSS, nothing to install).

**المعاملات:** neutral: #f3f4f6 / #111318 / brand #1d4ed8 / #0284c7 / #60a5fa, Inter, beat .4 s; bold: #080611 / #fff8ff / #ff3d81 / #7c5cff / #00d4ff, Impact, beat .32 s, overshoot cubic-bezier(.34,1.56,.64,1); editorial: #e9e1d2 / #202725 / #246b63 / #31776f / #8a6549, Georgia, beat .48 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ثيم · رموز · متغيرات CSS · theme · tokens · css variables · hyperframes · تغيير الثيم · ألوان وخطوط · ثيم جاهز · design tokens · theme file

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-one/vendor/hyperframes/themes/CONTRACT.md`
- `kosif-one/vendor/hyperframes/themes/neutral.css`
- `kosif-one/vendor/hyperframes/themes/bold.css`
- `kosif-one/vendor/hyperframes/themes/editorial.css`

#### 7. قدرات قريبة في العائلة

- `COLOR-40` باليتات أفلام المالك / Owner film palettes from shipped projects (ready)
- `COLOR-41` باليتات القوالب وخاناتها / Starter palettes and palette slots (proven)
- `COLOR-43` مكتبات باليتات جاهزة / Ready palette libraries (families, deck presets, recut themes, demo kit, dark ladders) (documented)
- `COLOR-44` اللون حسب العاطفة والقطاع والثقافة / Brand colour by emotion, sector and culture (documented)

### `COLOR-43` — مكتبات باليتات جاهزة / Ready palette libraries (families, deck presets, recut themes, demo kit, dark ladders)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مئات الألوان مرتبة حسب الغرض: 9 عائلات × 8 صفوف، و12 ستايل عروض بخطوطها، و6 ثيمات بطاقات، وطقم ديمو داكن دلالي، وسلالم خلفيات داكنة. / Hundreds of colours sorted by purpose: 9 families × 8 rows, 12 deck presets with fonts, 6 recut card themes, a semantic dark demo kit and dark-ground ladders.

**متى:** حين يحتاج المستخدم اختيار لوحة ألوان جاهزة حسب الغرض (نيون، باستيل، شركات، فاخر) لعرض أو فيديو أو ديمو داكن / when picking a ready palette by purpose (neon, pastel, corporate, premium) for a deck, video or dark demo

**كيف:** Pick ONE row and declare one bg, one fg, one accent before writing HTML; never mix rows. Demo kit timing: entrances 0.5–0.8 s cubic-bezier(0.16,1,0.3,1), gaps 0.2–0.4 s, crossfade 0.3–0.5 s, hold 1–2 s. Heading text gradient #FFFFFF→#9B9B9B on dark / #000000→#666666 on light. The Arko sushi palette (#131209 / #f3eadb / #d0703a) sits in vendor code with no licence — look, don't copy. (full table in references/powers/color-palette-grading.md)

**المعاملات:** 9×8 rows (~360 hex); 12 deck presets; 6 recut themes

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مكتبة ألوان · باليتات جاهزة · palette library · presets · neon · pastel · corporate · premium · ألوان عروض · ثيم داكن · اختيار الألوان · deck colors · dark theme · color scheme

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-creative/palettes/dark-premium.md`
- `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/STYLE_PRESETS.md`
- `kosif-one/vendor/hyperframes/skills/talking-head-recut/SKILL.md`
- `kosif-atlas/skills/166-demo-video/535-demo-video/references/scene-design-system.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-41` باليتات القوالب وخاناتها / Starter palettes and palette slots (proven)
- `COLOR-42` ثيمات HyperFrames وعقد الرموز / HyperFrames themes + 18-token contract (ready)
- `COLOR-44` اللون حسب العاطفة والقطاع والثقافة / Brand colour by emotion, sector and culture (documented)
- `COLOR-45` ألوان الحالات الدلالية / Semantic status colours (soft-tint chips, 5-stop ladder) (proven)

### `COLOR-44` — اللون حسب العاطفة والقطاع والثقافة / Brand colour by emotion, sector and culture

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جدول يقترح لونًا أساسيًا حسب الشعور المطلوب، وأعراف القطاعات، وتنبيه لمعاني الألوان عند الجمهور العربي والخليجي والمصري. / A table proposing a primary by desired emotion, sector conventions, and a watch-list for colour meanings with Arabic, Gulf and Egyptian audiences.

**متى:** حين يسأل المستخدم أي لون يناسب علامته حسب الشعور أو القطاع، أو ماذا يعني اللون للجمهور الخليجي أو المصري / when choosing a brand colour by emotion or sector, and its meaning for Arab, Gulf or Egyptian audiences

**كيف:** Pick one primary, derive light/dark/alpha in HSL (lighten 15%, darken 8%, glow rgba(primary,.12)) and validate 4.5:1. Never use the same hue for primary and destructive; finance blue/green trust, health calm teal; run a competitive audit and decide fit vs break. Before locking, list what each colour means to the target audience (red, white, green, yellow differ by culture) and add text cues.

**المعاملات:** trust #1E40AF; navy #1E3A5F; energy #DC2626; warm #EA580C; growth #16A34A; teal #0D9488; premium #7C3AED; developer #4F46E5; heritage amber #D97706; neutral #374151

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عاطفة · قطاع · ثقافة · معنى اللون · emotion · industry · culture · brand color · symbolism · لون العلامة · علم نفس الألوان · جمهور عربي · color psychology · brand identity · primary color

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-atlas/skills/3454-brand-landingpage/14160-brand-landingpage/references/stitch-architecture.md`
- `kosif-atlas/skills/1567-tonone/4427-form-palette`
- `kosif-atlas/skills/1503-universal-design-principles/3813-color`

#### 7. قدرات قريبة في العائلة

- `COLOR-42` ثيمات HyperFrames وعقد الرموز / HyperFrames themes + 18-token contract (ready)
- `COLOR-43` مكتبات باليتات جاهزة / Ready palette libraries (families, deck presets, recut themes, demo kit, dark ladders) (documented)
- `COLOR-45` ألوان الحالات الدلالية / Semantic status colours (soft-tint chips, 5-stop ladder) (proven)
- `COLOR-46` باليتات آمنة لعمى الألوان / Colour-blind-safe categorical palettes (ready)

### `COLOR-45` — ألوان الحالات الدلالية / Semantic status colours (soft-tint chips, 5-stop ladder)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل حالة (نجاح، تحذير، خطر، معلومة) لها صبغة خفيفة خلفية ولون قوي أمامي وأيقونة، وسلّم من خمس درجات لكل لون — فالمعنى لا يحمله اللون وحده. / Each status gets a pale tint background, a strong foreground and an icon, plus a five-stop ladder per hue — meaning never rides on colour alone.

**متى:** حين يحتاج المستخدم ألوان حالات (نجاح، تحذير، خطأ، معلومة) لشارات أو واجهة مع أيقونة وسلم درجات / for success, warning, error and info chips with tint backgrounds, icons and a five-stop ladder per hue

**كيف:** Chip: 36×36 rounded tile, bg = soft token, fg = strong token, icon 18 px (violet #f0edfa/#5b2acb, teal #e4f4f3/#087f86, amber #fff1d7/#ad6700, coral #fbe8ea/#c93343) — palette.test.mjs ran here. Ladder: 50 tinted bg, 300 border/icon, 500 fill, 700 text on tint, 900 text on dark (50+700 passes AA body; 50+500 large text only). Default hues HSL success 142 (70%), warning 38 (90%), destructive 0 (75%), info 220 (90%). Diagram pairs light fill + dark stroke: start #fed7aa/#c2410c, success #a7f3d0/#047857, decision #fef3c7/#b45309, AI #ddd6fe/#6d28d9, error #fecaca/#b91c1c; inactive dashed. Seen: 2×3 dark glass verdict cards with corner glow radius 120 px α .35, stagger 80 ms.

**المعاملات:** tile 36 px icon 18 px; stops 50/300/500/700/900

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حالات · نجاح · خطأ · شارات · status · success · error · chips · semantic · تحذير · ألوان الواجهة · تنبيهات · warning · badges · ui colors

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-audit-pro/app/globals.css:1297`
- `kosif-audit-pro/tests/palette.test.mjs`
- `kosif-atlas/skills/1503-universal-design-principles/3815-color-semantic-systems`
- `kosif-atlas/skills/2790-work/11181-draw-excalidraw`

#### 7. قدرات قريبة في العائلة

- `COLOR-43` مكتبات باليتات جاهزة / Ready palette libraries (families, deck presets, recut themes, demo kit, dark ladders) (documented)
- `COLOR-44` اللون حسب العاطفة والقطاع والثقافة / Brand colour by emotion, sector and culture (documented)
- `COLOR-46` باليتات آمنة لعمى الألوان / Colour-blind-safe categorical palettes (ready)
- `COLOR-47` خرائط الألوان وتسلسل الرسم البياني / Colormap semantics and chart colour hierarchy (documented)

### `COLOR-46` — باليتات آمنة لعمى الألوان / Colour-blind-safe categorical palettes

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أوكابي-إيتو وبول تول ولوحة الفئات السبع بإضاءة متساوية — ومع كل لون شكل أو تسمية، لأن 8% من الرجال لا يميزون الأحمر من الأخضر. / Okabe-Ito, Paul Tol and a matched-lightness 7-hue set — always paired with shape or label, because ~8% of men miss red/green.

**متى:** حين يرسم المستخدم مخططًا بفئات متعددة ويريد ألوانًا يميزها المصابون بعمى الألوان مع أشكال أو تسميات / when a multi-category chart needs colour-blind-safe hues paired with shapes or labels

**كيف:** Okabe-Ito #E69F00 #56B4E9 #009E73 #F0E442 #0072B2 #D55E00 #CC79A7 #000000 (on white use #0072B2 #D55E00 #009E73 #CC79A7 #000000 for 3:1). Tol Bright #4477AA #EE6677 #228833 #CCBB44 #66CCEE #AA3377 #BBBBBB (7); High-contrast #004488 #DDAA33 #BB5566 (3, best in greyscale); Vibrant #EE7733 #0077BB #33BBEE #EE3377 #CC3311 #009988 #BBBBBB. 7-hue: hsl(220 70% 55%) (160 60% 45%) (40 90% 55%) (310 60% 55%) (10 70% 55%) (270 50% 55%) (85 50% 45%). Never interpolate these; ≤5–7 categories; add icons, direct labels, dashes; simulate with Chrome 'Emulate vision deficiencies'.

**المعاملات:** Okabe-Ito 8 (5 on white); Tol 7/3/7/9/6; ≤7 hues

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عمى الألوان · إتاحة · رسم بياني · colorblind · okabe-ito · paul tol · categorical · accessibility · ألوان آمنة · مخطط بياني · عمى الأحمر والأخضر · color blind safe · chart palette · red green

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/assets/color_palettes.py`
- `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/references/color_palettes.md`
- `kosif-atlas/skills/1503-universal-design-principles/3815-color-semantic-systems`
- `kosif-atlas/skills/1503-universal-design-principles/3814-color-accessibility-and-mode`

#### 7. قدرات قريبة في العائلة

- `COLOR-44` اللون حسب العاطفة والقطاع والثقافة / Brand colour by emotion, sector and culture (documented)
- `COLOR-45` ألوان الحالات الدلالية / Semantic status colours (soft-tint chips, 5-stop ladder) (proven)
- `COLOR-47` خرائط الألوان وتسلسل الرسم البياني / Colormap semantics and chart colour hierarchy (documented)
- `COLOR-48` التدرج الحراري بسبع محطات / Thermal 7-stop heat ramp (proven)

### `COLOR-47` — خرائط الألوان وتسلسل الرسم البياني / Colormap semantics and chart colour hierarchy

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اختر نوع الخريطة اللونية حسب معنى البيانات، ولون تمييز واحد يحمل الاستنتاج والباقي رمادي، ولكل لون معنى واحد في الفيلم كله. / Pick the colormap by what the data means; one accent carries the insight, context stays grey; each hue has exactly one meaning per film.

**متى:** حين يلون المستخدم رسمًا بيانيًا أو خريطة بيانات ويحتاج اختيار خريطة لونية متسلسلة أو متباعدة ولون تمييز واحد للاستنتاج / when choosing a sequential or diverging colormap and one insight accent for a chart

**كيف:** Sequential = monotonic lightness (viridis, plasma, inferno, magma, cividis); diverging only around a meaningful centre (RdBu_r, PuOr, BrBG) with a centred norm (e.g. vmin −2, centre 0, vmax 5), no-data in neutral grey; cyclic for angles/hours; ColorBrewer at its exact class count; no rainbow for ordered values. Chart hierarchy: ≤4 hues, chrome at 20–30% contrast, highlight 100% vs others 35–45%, no gradients/shadows/perspective on data. Write a role→hex ledger before animating; accent on ≤2 marks; never let red/green or blue/purple alone carry a distinction.

**المعاملات:** ≤4 hues; chrome 20–30%; others 35–45%; accent ≤2 marks

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بيانات · خريطة لونية · رسم بياني · colormap · viridis · diverging · chart color · insight · تصور البيانات · ألوان الرسم البياني · تدرج البيانات · data viz · sequential · colorbrewer

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-tool/playbooks/charts.md:19-20`
- `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/references/color_palettes.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10318-accessibility-and-inclusive-visualizatio/references/color-contrast-and-redundant-encoding.md`
- `kosif-atlas/skills/317-data/942-data-visualization/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-45` ألوان الحالات الدلالية / Semantic status colours (soft-tint chips, 5-stop ladder) (proven)
- `COLOR-46` باليتات آمنة لعمى الألوان / Colour-blind-safe categorical palettes (ready)
- `COLOR-48` التدرج الحراري بسبع محطات / Thermal 7-stop heat ramp (proven)
- `COLOR-49` تدرجا ماغما والجبل / Magma colormap and alpine terrain ramp (ready)

### `COLOR-48` — التدرج الحراري بسبع محطات / Thermal 7-stop heat ramp

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تدرج كاميرا حرارية (بارد، عميق، أخضر، أصفر، برتقالي، أحمر، أبيض) لحقول الحرارة وخرائط الشدة، مع سقف يمنعه من الاحتراق للأبيض. / A heat-camera ramp (cold, deep, green, yellow, orange, red, white) for heat fields and intensity maps, capped so it never blows to white.

**متى:** حين يريد المستخدم مظهر كاميرا حرارية أو خريطة شدة ملونة لحقل حرارة دون أن يحترق للأبيض / for a heat-camera look or intensity map colouring a heat field, capped so it never blows to white

**كيف:** Map heat 0–1 through seven stops blended with smoothstep at 0, .12, .30, .45, .60, .78, 1; cap heat at 0.75; background heat 0.34–0.66; keep dark→light so heat reads as brightness when you swap in a brand ramp. Full-screen fragment shader: fbm 5 octaves warp-the-warp, melt cycle 6 s, blob 0.37, flow 0.26, rim 0.6, halo 0.45; trail 24 points fading over 1.6 s.

**المعاملات:** stops 0/.12/.30/.45/.60/.78/1; cap .75

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حراري · خريطة حرارة · thermal · heatmap · ramp · shader · كاميرا حرارية · تدرج ألوان · خريطة شدة · heat camera · intensity map · gradient

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/SKILL.md`
- `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/references/thermal-finger-trail.html`

#### 7. قدرات قريبة في العائلة

- `COLOR-46` باليتات آمنة لعمى الألوان / Colour-blind-safe categorical palettes (ready)
- `COLOR-47` خرائط الألوان وتسلسل الرسم البياني / Colormap semantics and chart colour hierarchy (documented)
- `COLOR-49` تدرجا ماغما والجبل / Magma colormap and alpine terrain ramp (ready)
- `COLOR-50` مولّد التناغم اللوني / Harmony generator 2D/3D + harmony detector (proven)

### `COLOR-49` — تدرجا ماغما والجبل / Magma colormap and alpine terrain ramp

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تدرج ماغما مضغوط (أسود → بنفسجي → أرجواني → مرجاني → برتقالي → ذهبي باهت) للطيف الصوتي، وتدرج جبلي يلون التضاريس بالارتفاع والميل. / A compact magma ramp (black→violet→magenta→coral→orange→pale gold) for spectrograms, and an alpine ramp that colours terrain by height and slope.

**متى:** حين يلون المستخدم طيفًا صوتيًا (سبيكتروغرام) أو تضاريس جبلية حسب الارتفاع والميل / for colouring an audio spectrogram with a magma ramp, or terrain by height and slope

**كيف:** qa._magma(v) stops 0 (0,0,4) · .2 (40,11,84) · .4 (120,28,109) · .6 (192,58,118) · .75 (236,105,89) · .88 (251,165,74) · 1 (252,253,191). K3.alpineColour as makeTerrain colour: deep #2f4a3a (<−5 m), sand #b9a77a → grass #4e6e34 (5–25 m), grass2 #6b8a3c, rock #5d5a58/#7a6f66 (120–420 m, slope .28–.6), snow #f4f7fb above 520–700 m.

**المعاملات:** magma 7 stops; alpine 6 bands

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ماغما · تضاريس · طيف صوتي · magma · spectrogram · terrain · alpine · ramp · سبيكتروغرام · جبال · ارتفاع · audio visualization · height colors · colormap

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-studio/motion/qa.py:439`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:135`

#### 7. قدرات قريبة في العائلة

- `COLOR-47` خرائط الألوان وتسلسل الرسم البياني / Colormap semantics and chart colour hierarchy (documented)
- `COLOR-48` التدرج الحراري بسبع محطات / Thermal 7-stop heat ramp (proven)
- `COLOR-50` مولّد التناغم اللوني / Harmony generator 2D/3D + harmony detector (proven)
- `COLOR-51` تدرجات إدراكية OKLCH وظلال بإزاحة الصبغة / Perceptual OKLCH ramps and hue-shifted shading (documented)

### `COLOR-50` — مولّد التناغم اللوني / Harmony generator 2D/3D + harmony detector

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يبني ألوانًا متكاملة أو متجاورة أو ثلاثية أو منقسمة أو رباعية من درجة أساس واحدة، كنصوص CSS أو ألوان three.js — ويصنّف لوحة موجودة. / Builds complementary/analogous/triadic/split/tetradic hues from one base as CSS strings or THREE.Color, and classifies an existing palette.

**متى:** حين يريد المستخدم ألوانًا متناسقة من لون أساس واحد (متكاملة، متجاورة، ثلاثية) أو معرفة نوع تناغم لوحة موجودة / for complementary, analogous or triadic colours from one base hue, or classifying a palette

**كيف:** MOTION.palette(scheme, baseHue, {sat, light:[…]}) → {hues, css}; K3.harmony(scheme, hue, {sat .6, light .5}) → THREE.Color. Offsets: complementary 0/180, analogous −30/0/30, triadic 0/120/240, split 0/150/210, tetradic 0/60/180/240; defaults S 60% L 50%. blue_hour uses harmony('complementary', 222) → [222, 42] (blue sky vs orange lamps). Keep one family dominant, the complement only as accent. Detector: take chromatic colours (OKLCH C ≥ 0.04), test mono (±15°), analogous (±30°), complementary, split (±150°), triadic (±120°), square — tolerance ±15°; free combinations allowed but flagged. Ran here in Chromium (vendored kit/gsap.min.js + motion-kit.js): MOTION.palette('split', 210) → hues [210, 0, 60] as hsl(… 60% 50%), ('complementary', 222) → [222, 42].

**المعاملات:** offsets as listed; tolerance ±15°; C ≥ .04

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تناغم · ألوان متكاملة · عجلة الألوان · harmony · complementary · triadic · analogous · color wheel · ألوان متناسقة · دائرة الألوان · توليد ألوان · color scheme · three.js · split complementary

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-studio/motion/kit/motion-kit.js:113`
- `kosif-studio/motion/kit/three-kit.js:1176`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:24`
- `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/references/color-harmony-math.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-48` التدرج الحراري بسبع محطات / Thermal 7-stop heat ramp (proven)
- `COLOR-49` تدرجا ماغما والجبل / Magma colormap and alpine terrain ramp (ready)
- `COLOR-51` تدرجات إدراكية OKLCH وظلال بإزاحة الصبغة / Perceptual OKLCH ramps and hue-shifted shading (documented)
- `COLOR-52` حساب التباين WCAG / WCAG contrast math, role tiers and alpha flattening (proven)

### `COLOR-51` — تدرجات إدراكية OKLCH وظلال بإزاحة الصبغة / Perceptual OKLCH ramps and hue-shifted shading

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ابنِ السلالم في OKLCH حتى تبدو الخطوات متساوية فعلًا، وحرّك الصبغة: الظلال تبرد والإضاءات تدفأ بدل التغميق فقط؛ ولا أبيض نقي ولا رمادي محايد في لوحة فنية. / Build ramps in OKLCH so steps look even, and shift hue — shadows cooler, highlights warmer — instead of just darkening; no pure white or neutral grey in a painterly palette.

**متى:** حين يبني المستخدم سلم درجات للون يبدو متساويًا للعين، أو يريد ظلالًا أبرد وإضاءات أدفأ بدل التغميق فقط / when building even-looking colour ramps in OKLCH, or hue-shifted shading with cooler shadows and warmer lights

**كيف:** sRGB → linear → OKLab → OKLCH (Ottosson 2020); keep H within ±10° per family, vary L and C; Chromium renders oklch() natively in HTML/Remotion. Neutral ramp check: OKLCH L per stop, deltas d, uniformity = 1 − (max\|d\| − min\|d\|)/mean\|d\| ≥ 0.7. Material ramps 3–5 steps rotating hue 10–20° and raising saturation in darks. Painting family: deep blues, pale yellows, a green touch, warm ochre.

**المعاملات:** hue drift ≤10°; uniformity ≥0.7; shift 10–20°/step

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** OKLCH · تدرج · ظلال · إدراكي · oklch · perceptual · ramp · hue shift · shading · سلم ألوان · درجات اللون · ظلال باردة · color ramp · color scale · painterly

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/references/color-harmony-math.md`
- `kosif-atlas/skills/2460-pixel-art/9527-sprite`
- `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/css-techniques.md`
- `kosif-tool/styles/pm-mandelduck-95fd08/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-49` تدرجا ماغما والجبل / Magma colormap and alpine terrain ramp (ready)
- `COLOR-50` مولّد التناغم اللوني / Harmony generator 2D/3D + harmony detector (proven)
- `COLOR-52` حساب التباين WCAG / WCAG contrast math, role tiers and alpha flattening (proven)
- `COLOR-53` الوضع الداكن بلا قلب / Dark variant without inversion (documented)

### `COLOR-52` — حساب التباين WCAG / WCAG contrast math, role tiers and alpha flattening

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** احسب الإضاءة النسبية ونسبة التباين لكل نص فوق خلفيته قبل الرندر، بعتبة حسب دور النص، وادمج الشفافية أولًا لأن اللوحة الزجاجية فوق الفيديو تتغير. / Compute relative luminance and contrast for every caption/background pair before render, with thresholds by role, flattening alpha first because a glass plate over video changes.

**متى:** حين يضع المستخدم نصًا أو كابشن فوق خلفية أو لوح زجاجي فوق فيديو ويريد التأكد أنه مقروء قبل الرندر / when checking caption or text contrast over a background or translucent plate on video before render

**كيف:** Decode sRGB (c/12.92 if c ≤ 0.04045 else ((c+0.055)/1.055)^2.4), L = 0.2126R + 0.7152G + 0.0722B, ratio = (Lmax+0.05)/(Lmin+0.05). Body 4.5:1 (AAA 7:1); large text/UI/brand/links 3:1; disabled/hover optional — only body failures block delivery. Translucent plates: out = fg·α + bg·(1−α) per channel, sampling the darkest and brightest frames under the plate. Accessibility cut: AAA pairs, solid borders, no text over gradients (@media (prefers-contrast: more)). design_tokens.py implements this and ran here (22 pairs pass). (code snippet in references/powers/color-palette-grading.md)

**المعاملات:** 4.5 / 3.0 / none; AAA 7:1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تباين · إتاحة · قراءة · contrast · wcag · accessibility · luminance · captions · وضوح النص · كابشن · مقروئية · readability · text contrast · subtitles

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:axe` ← npm ls axe أو وجود node_modules/axe
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-one/tools/kosif-omni/skills/kosif-web-design/scripts/design_tokens.py:92`
- `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/references/color-harmony-math.md`
- `kosif-atlas/skills/2199-lvtd-skills/8013-color-math-accessibility`
- `100-superskills/skills/brand-identity-logo/SKILL.md:23`

#### 7. قدرات قريبة في العائلة

- `COLOR-50` مولّد التناغم اللوني / Harmony generator 2D/3D + harmony detector (proven)
- `COLOR-51` تدرجات إدراكية OKLCH وظلال بإزاحة الصبغة / Perceptual OKLCH ramps and hue-shifted shading (documented)
- `COLOR-53` الوضع الداكن بلا قلب / Dark variant without inversion (documented)
- `COLOR-54` لون تمييز واحد بمعنى واحد / One accent, one meaning (~5% of the frame) (ready)

### `COLOR-53` — الوضع الداكن بلا قلب / Dark variant without inversion

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لا تقلب الألوان: خلفية قريبة من الأسود بصبغة الهوية، نص أوف وايت، وألوان الهوية أقل تشبعًا وأفتح قليلًا — وتجنب الأسود والأبيض النقيين. / Don't invert: a brand-tinted near-black ground, off-white text, brand colours desaturated and lifted — and avoid pure #000/#fff.

**متى:** حين يريد المستخدم نسخة داكنة من تصميم أو هوية دون قلب الألوان، بخلفية شبه سوداء ونص أوف وايت / when making a dark variant of a design or brand without inverting colours: tinted near-black ground, off-white text

**كيف:** bg hsl(220 10% 8%), text ~hsl(0 0% 90%); brand hsl(220 90% 50%) → hsl(220 70% 60%) (sat −20 pts, L +10 pts); darkest ~#111827 to avoid halation; use #0a0a0a and #fafaf9 instead of black/white; text tiers by opacity 100/60/40%, borders 10%. Re-run contrast in both modes.

**المعاملات:** sat −20, L +10; tiers 100/60/40/10%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** داكن · ليلي · dark mode · night · halation · inversion · وضع داكن · خلفية سوداء · نسخة ليلية · dark theme · off-white · contrast

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-atlas/skills/1503-universal-design-principles/3814-color-accessibility-and-mode`
- `kosif-atlas/skills/3438-ux-design/14124-top-design`

#### 7. قدرات قريبة في العائلة

- `COLOR-51` تدرجات إدراكية OKLCH وظلال بإزاحة الصبغة / Perceptual OKLCH ramps and hue-shifted shading (documented)
- `COLOR-52` حساب التباين WCAG / WCAG contrast math, role tiers and alpha flattening (proven)
- `COLOR-54` لون تمييز واحد بمعنى واحد / One accent, one meaning (~5% of the frame) (ready)
- `COLOR-55` أنظمة لونين أو ثلاثة صارمة / Strict two- and three-colour systems (seen)

### `COLOR-54` — لون تمييز واحد بمعنى واحد / One accent, one meaning (~5% of the frame)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لون تمييز واحد بمعنى واحد يغطي نحو 5% من البكسلات، ولحظة واحدة يملأ فيها الإطار؛ الوصول يُصبغ ثم يرتاح إلى المحايد؛ والمحايدات تميل لصبغة الهوية لا للرمادي. / One accent with one meaning on ~5% of pixels and one full-bleed beat; arrivals tint then relax to neutral; neutrals lean toward the brand hue instead of pure grey.

**متى:** حين يبدو التصميم أو الفيديو مزدحمًا بالألوان ويحتاج المستخدم لون تمييز واحدًا بمعنى واحد والباقي محايد / when a design or video feels over-coloured and needs one accent with one meaning against neutrals

**كيف:** Lock roles before animating: one primary, a ~9-stop neutral ramp, success/warning/destructive as a separate axis (≈5 roles). Sequences ~80% neutral / ~20% accent; accent marks exactly one element per composition and never a placeholder (stand-in cards, avatars and series are alpha steps of the ink). Arrival tints relax to neutral over 12–50 frames. premium_edit takes --ivory/--ink/--accent/--accent2 (#F5F0E6 / #121417 / #E7B65A / #F3D9A4). Seen as ink black #090909, bone #f4f1ea and one signal orange #f27525 used only for the active element; light canvas with one #ff4c2d for selection, cursor and impact numbers.

**المعاملات:** accent ≈5% pixels; 80/20; tint relax 12–50 f; 5 roles

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** لون واحد · تمييز · بساطة · one accent · restraint · 80/20 · focus · neutral · لون مميز · ألوان محايدة · تقليل الألوان · accent color · minimal palette · color roles

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `lean` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-studio/motion/direct.py:288`
- `kosif-studio/motion/references/craft-numbers.md`
- `kosif-earth-ci-fork/docs/design/SQC-IDENTITY-ar.md`
- `kosif-one/vendor/hyperframes/registry/components/CATALOG.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-52` حساب التباين WCAG / WCAG contrast math, role tiers and alpha flattening (proven)
- `COLOR-53` الوضع الداكن بلا قلب / Dark variant without inversion (documented)
- `COLOR-55` أنظمة لونين أو ثلاثة صارمة / Strict two- and three-colour systems (seen)
- `COLOR-56` قفل الأسلوب وبصمة المرجع / Style lock and reference style-DNA (+ exact hex after generation) (proven)

### `COLOR-55` — أنظمة لونين أو ثلاثة صارمة / Strict two- and three-colour systems

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أنت أنتجت أفلامًا بلونين أو ثلاثة فقط حيث التباين نفسه يصنع الإيقاع: حبر وورق ولون إشارة، تُقلب الأدوار بين الفصول. / You have produced films with only two or three colours where contrast itself makes the rhythm: ink, paper and one signal colour, roles swapped between chapters.

**متى:** حين يريد المستخدم فيلمًا أو موشن بلونين أو ثلاثة فقط (حبر وورق ولون إشارة) تتبادل الأدوار بين الفصول / for a film using only two or three colours (ink, paper, one signal) with roles swapped between chapters

**كيف:** Choose ink + paper + one signal; every element must use one of them (no tints except alpha of ink); flip ground per chapter or bar (COLOR-66/67); max 3 hues, white type on a saturated single ground for heroes; avoid multi-gradients, sparkles and purple 'AI' clichés. Build: CSS vars --ink/--paper/--signal, scenes swap which is ground. (full table in references/powers/color-palette-grading.md)

**المعاملات:** 2–3 hues only; flip per chapter/bar

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** لونان · ثلاثة ألوان · بساطة · two colour · three colour · minimal · ink paper · signal · ألوان محدودة · مينيمال · حبر وورق · limited palette · role swap

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `style:pm-fionntobin-97b7af`
- `style:pm-grace-sunnyy-29bc61`
- `style:pm-leadnotifi-e83f94`
- `kosif-atlas/skills/100-ui-motion/209-kinetic-inflated-hero/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-53` الوضع الداكن بلا قلب / Dark variant without inversion (documented)
- `COLOR-54` لون تمييز واحد بمعنى واحد / One accent, one meaning (~5% of the frame) (ready)
- `COLOR-56` قفل الأسلوب وبصمة المرجع / Style lock and reference style-DNA (+ exact hex after generation) (proven)
- `COLOR-57` تحويل النغمات ACES وAgX وNeutral / Tone-mapping choice: ACES, AgX or Neutral (ready)

### `COLOR-56` — قفل الأسلوب وبصمة المرجع / Style lock and reference style-DNA (+ exact hex after generation)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قفل أسلوب يُنسخ حرفيًا في كل لقطة (5 ألوان hex، إضاءة، عدسة، تلوين، حبيبات، حقبة، 3 كلمات مزاج)، ووضع S ينسخ لوك مرجع بعد فحص 5–8 لقطات فعلًا — والهوية الدقيقة تُطبق في طبقة الحركة لا تُترك لمولد الصور. / A style lock copied verbatim into every shot (5 hex, lighting, lens, grade, grain, era, 3 mood words); mode S copies a reference look only after inspecting 5–8 frames; exact brand hex is applied in the motion layer, not trusted to the generator.

**متى:** حين يريد المستخدم ثبات الألوان والأسلوب في كل اللقطات المولدة أو تقليد لوك مرجع بعد فحصه / when keeping palette and style locked across generated shots, or copying a reference look after inspecting frames

**كيف:** Intake 4–6 named hex (one bg = lightest, one accent). kinetic-flow theme S → REFERENCE stage demands DNA (palette hex, typography, objects, transitions, timing) → SCRIPT, label 'Reference: <name>'; never copy words, logos or people. Generators: 3–10 style references, then grade or overlay the true hex (e.g. a #8B2635 band) in HTML/SVG/Remotion — seeds do not transfer across models. production-profiles.test.mjs ran here (10/10).

**المعاملات:** 5 HEX + 3 mood words; 5–8 screenshots; 3–10 refs

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قفل الأسلوب · مرجع · هوية دقيقة · style lock · reference · style dna · brand hex · generation · ثبات الأسلوب · اتساق اللقطات · تقليد مرجع · consistent style · image generator

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:22,46`
- `fastify-motion-bro/tests/production-profiles.test.mjs:67-74`
- `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/prompt-library.md`
- `kosif-atlas/skills/2306-generative-web-media/8850-brand-conditioned-generation`

#### 7. قدرات قريبة في العائلة

- `COLOR-54` لون تمييز واحد بمعنى واحد / One accent, one meaning (~5% of the frame) (ready)
- `COLOR-55` أنظمة لونين أو ثلاثة صارمة / Strict two- and three-colour systems (seen)
- `COLOR-57` تحويل النغمات ACES وAgX وNeutral / Tone-mapping choice: ACES, AgX or Neutral (ready)
- `COLOR-58` تمريرة المظهر / Look pass: gamut mask, Purkinje night vision, split toning (ready)

### `COLOR-57` — تحويل النغمات ACES وAgX وNeutral / Tone-mapping choice: ACES, AgX or Neutral

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اختيار منحنى تحويل النغمات لكل لقطة: ACES قوي، AgX يحفظ صبغة الإضاءات الساطعة (نيون ونار)، وNeutral أمين لألوان المنتجات. / Pick the tone curve per shot: ACES punchy, AgX keeps hue in bright highlights (neon, fire), PBR Neutral faithful for products.

**متى:** حين يرندر المستخدم مشهد three.js ويختار تحويل النغمات: قوي، أو يحفظ ألوان النيون والنار، أو أمين لألوان المنتج / when choosing ACES, AgX or Neutral tone mapping per 3D shot

**كيف:** K3.makeRenderer(canvas, W, H, {tone:'aces'\|'agx'\|'neutral', exposure}) — pixelRatio 1, PCFShadowMap, preserveDrawingBuffer. Shipped exposures: blue_hour agx 1.05, night_boat agx .95, bunny neutral .9, lab neutral 1.0, koi .62, sound_ground .7; omni cinematic template uses ACESFilmic exposure 1.25 with FogExp2(#030712, .035). Runs in Chromium with no npm install through the pre-built `kit/three-kit.bundle.js` (904 KB IIFE with three.js inside); the ES-module `three-kit.js` needs `three` resolvable.

**المعاملات:** exposure .5–1.25; agx for lamps/neon, neutral for products

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تحويل النغمات · ثلاثي · tone mapping · aces · agx · neutral · exposure · three.js · ثلاثي الأبعاد · نيون · ألوان المنتج · 3d render · highlights · product shot

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-studio/motion/kit/three-kit.js:76`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:17`
- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:102`
- `kosif-studio/motion/references/book-lessons.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-55` أنظمة لونين أو ثلاثة صارمة / Strict two- and three-colour systems (seen)
- `COLOR-56` قفل الأسلوب وبصمة المرجع / Style lock and reference style-DNA (+ exact hex after generation) (proven)
- `COLOR-58` تمريرة المظهر / Look pass: gamut mask, Purkinje night vision, split toning (ready)
- `COLOR-59` المنظور الجوي / Aerial perspective: 3-channel fog, fog toward the sun, sky bounce (ready)

### `COLOR-58` — تمريرة المظهر / Look pass: gamut mask, Purkinje night vision, split toning

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تمريرة بعد الرندر: قناع طيف يخفض تشبع الألوان خارج إسفين مختار فتتماسك اللوحة، ورؤية ليلية تُزرّق الظلال وتغرق الأحمر أولًا، وتقسيم لوني دافئ/بارد. / A post pass: a gamut mask that desaturates hues outside a chosen wedge, Purkinje night vision that turns darks rod-blue and sinks reds first, and warm-light / cool-shadow split toning.

**متى:** حين يريد المستخدم تماسك ألوان مشهد ثلاثي الأبعاد بعد الرندر، أو ليلًا مقنعًا يزرق الظلال، أو تقسيمًا دافئًا وباردًا / for a post pass: gamut mask, night vision or warm/cool split toning

**كيف:** const look = K3.makeLookPass({warm, cool}); composer.addPass(look); look.userData.set({gamut:[centreHueDeg, widthDeg, strength], night:0..1, split:0..1}) before OutputPass. Gamut edge feather 25° beyond half-width; night rod weights (.05,.55,.40), tint (.72,.86,1.12) on luma .02–.35, darken 25%; split warm #ffc98a / cool #5a7fb8, luma ramp .1–.7, strength ×0.35. Shipped: blue_hour {night .55, split .45, warm #ffb36a, cool #4a6aa8}; night_boat {night .35, split .55, warm #ffa860, cool #4f6fa8}. Runs in Chromium with no npm install through the pre-built `kit/three-kit.bundle.js` (904 KB IIFE with three.js inside); the ES-module `three-kit.js` needs `three` resolvable.

**المعاملات:** gamut feather 25°; split ×.35; night darken 25%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** رؤية ليلية · قناع الطيف · تقسيم لوني · gamut mask · night vision · purkinje · split toning · look pass · مشهد ليلي · تماسك الألوان · دافئ وبارد · post processing · night scene · warm cool

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1148`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1164`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:124`
- `kosif-studio/motion/kit/three-kit.js:1147`

#### 7. قدرات قريبة في العائلة

- `COLOR-56` قفل الأسلوب وبصمة المرجع / Style lock and reference style-DNA (+ exact hex after generation) (proven)
- `COLOR-57` تحويل النغمات ACES وAgX وNeutral / Tone-mapping choice: ACES, AgX or Neutral (ready)
- `COLOR-59` المنظور الجوي / Aerial perspective: 3-channel fog, fog toward the sun, sky bounce (ready)
- `COLOR-60` تمريرة تلوين الشيدر / Shader grade pass driven by story or music (ready)

### `COLOR-59` — المنظور الجوي / Aerial perspective: 3-channel fog, fog toward the sun, sky bounce

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ضباب بثلاث قنوات (الأزرق يتشتت أكثر) فيصبح البعيد أزرق وأقل تباينًا؛ والضباب يدفأ حين تنظر نحو شمس منخفضة ويبقى باردًا بعيدًا عنها — قواعد غورني في الكود. / Per-channel fog (blue scatters most) so distance turns bluer and flatter; haze warms toward a low sun and stays cool away from it — Gurney's rules in code.

**متى:** حين يريد المستخدم عمقًا مقنعًا في مشهد طبيعي ثلاثي الأبعاد فيصبح البعيد أزرق وأقل تباينًا والضباب يدفأ نحو الشمس / for believable depth in a 3D landscape: distance bluer and flatter, haze warming toward a low sun

**كيف:** K3.aerialPerspective({scatter:[0.62, 0.85, 1.25]}) before the first render (patches the fog chunk), scene.fog colour = horizon sky (FogExp2). Per frame K3.fogTowardSun(scene, camera, sunDir, cool, warm, amount) with weight = max(0, dot(view, sun))³ × amount; skyBounce({sky, ground}) cool from above, warm from below. blue_hour: four identical dark ridges 0x2b2420 at 0.7/1.4/2.6/4.5 km, FogExp2(0x8790b0, 0.00062), cool 0x8790b0, warm 0xc49a8a, amount .9, scatter [.55,.8,1.3]. Seen: exponential fog tinted to sky #90b5ca. Runs in Chromium with no npm install through the pre-built `kit/three-kit.bundle.js` (904 KB IIFE with three.js inside); the ES-module `three-kit.js` needs `three` resolvable.

**المعاملات:** scatter [.62,.85,1.25]; weight dot³; ridges .7/1.4/2.6/4.5 km

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ضباب · منظور جوي · غروب · aerial perspective · fog · atmosphere · gurney · haze · عمق المشهد · طبيعة · شمس منخفضة · depth · landscape · sun haze

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-59` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1131`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1201`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:54`
- `kosif-studio/motion/references/book-lessons.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-57` تحويل النغمات ACES وAgX وNeutral / Tone-mapping choice: ACES, AgX or Neutral (ready)
- `COLOR-58` تمريرة المظهر / Look pass: gamut mask, Purkinje night vision, split toning (ready)
- `COLOR-60` تمريرة تلوين الشيدر / Shader grade pass driven by story or music (ready)
- `COLOR-61` ألوان مصادر الضوء العملية / Named practical light colours (sodium, mercury, moon, flame) (ready)

### `COLOR-60` — تمريرة تلوين الشيدر / Shader grade pass driven by story or music

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تلوين نهائي على مستوى الشيدر: ظلال باردة وإضاءات دافئة، دفء، رفع للسواد، انحراف لوني عند الحواف، فينيت وحبيبات — والمفاتيح تتغير كل إطار مع القصة أو الموسيقى. / A shader finish: cool shadows / warm highlights, warmth, black lift, edge chromatic aberration, vignette and grain — uniforms change per frame with story or music.

**متى:** حين يريد المستخدم تشطيبًا لونيًا نهائيًا في الشيدر يتغير مع القصة أو يتفاعل مع الموسيقى والباص / when a shader finish (split tone, lift, vignette, grain, aberration) must change per frame with story or music

**كيف:** post.grade.uniforms uWarm / uLift / uVig / uCA: shadows (0.92,0.98,1.08), highlights (1.08,1.0,0.92), warm tint (1.05,.98,.9) × uWarm .5, vignette .42 smoothstep .35–.95, CA 1.2 px at 1920 scaled by radius. Shipped: koi warm .55 lift .02; sound_ground lift .08 ('no pure black') and warm .45 + .3·bass; water_cycle warm .75→.2 over 5 s, lift .08·overcast. Egypt-2120 pass after OutputPass: CA dot(d,d)·.006, saturation mix 1.08, oval vignette .38 smoothstep(.25,.85,\|d·(1.1,.82)\|), grain (hash−.5)·.028 stepped at 1/30 s. Runs in Chromium with no npm install through the pre-built `kit/three-kit.bundle.js` (904 KB IIFE with three.js inside); the ES-module `three-kit.js` needs `three` resolvable.

**المعاملات:** vig .38–.42; CA .006 / 1.2 px; grain .028; lift .02–.08

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تشطيب · انحراف لوني · حبيبات · دفء · film finish · chromatic aberration · grain · lift · audio reactive · تفاعل مع الموسيقى · باص · فينيت · music reactive · vignette · shader

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-60` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:389`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:69`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:104`
- `kosif-one/projects/egypt-2120-animation/index.html:436-444`

#### 7. قدرات قريبة في العائلة

- `COLOR-58` تمريرة المظهر / Look pass: gamut mask, Purkinje night vision, split toning (ready)
- `COLOR-59` المنظور الجوي / Aerial perspective: 3-channel fog, fog toward the sun, sky bounce (ready)
- `COLOR-61` ألوان مصادر الضوء العملية / Named practical light colours (sodium, mercury, moon, flame) (ready)
- `COLOR-62` تشطيب الرسام الفيلمي / Painter filmic curve, split-tone grade and grain (proven)

### `COLOR-61` — ألوان مصادر الضوء العملية / Named practical light colours (sodium, mercury, moon, flame)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ألوان مسماة لمصادر حقيقية — صوديوم، زئبق، قمر، لهب — وحرارات متباينة (قمر 4100K مقابل فانوس 1900K) تجعل الليل مقنعًا. / Named real-source colours — sodium, mercury, moon, flame — and contrasting temperatures (4100 K moon vs 1900 K lantern) that make night believable.

**متى:** حين يبني المستخدم مشهدًا ليليًا ويريد ألوان مصادر ضوء حقيقية مثل الصوديوم والقمر والفانوس ليبدو مقنعًا / when a night scene needs real practical-light colours (sodium, mercury, moon, flame) to feel believable

**كيف:** K3.lightColor('sodium'\|'mercury'\|'moon'\|'flame') from LIGHT_SOURCES. night_boat: sky zenith (0.004,0.008,0.024), horizon (0.035,0.058,0.105), fog #0d1626, sea #061525, lantern #ff9a3c, title #f3ead8, rule #e0a35a — one ember source against navy and silver. Plan the gel with COLOR-23. Runs in Chromium with no npm install through the pre-built `kit/three-kit.bundle.js` (904 KB IIFE with three.js inside); the ES-module `three-kit.js` needs `three` resolvable.

**المعاملات:** moon 4100 K; lantern 1900 K #ff9a3c

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مصابيح · قمر · نار · صوديوم · practical lights · sodium · moonlight · lantern · kelvin · إضاءة ليلية · فانوس · لهب · night scene · flame · mercury

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-61` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `100-superskills/skills/kosif-montage-motion/SKILL.md:106`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:137`
- `kosif-studio/motion/references/book-lessons.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-59` المنظور الجوي / Aerial perspective: 3-channel fog, fog toward the sun, sky bounce (ready)
- `COLOR-60` تمريرة تلوين الشيدر / Shader grade pass driven by story or music (ready)
- `COLOR-62` تشطيب الرسام الفيلمي / Painter filmic curve, split-tone grade and grain (proven)
- `COLOR-63` انضغاط الإضاءات العالية / Highlight roll-off quantiser (proven)

### `COLOR-62` — تشطيب الرسام الفيلمي / Painter filmic curve, split-tone grade and grain

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** في مشاهد الرسم بالكود: منحنى ACES فيلمي بتعريض وتباين وتشبع ورفع، وتلوين يرفع الظلال نحو لون والإضاءات نحو آخر، وحبيبات مبذورة. / For code-painted scenes: an ACES-fitted filmic curve with exposure/contrast/saturation/lift, a shadows→colour / highlights→colour grade, and seeded grain.

**متى:** حين يرسم المستخدم مشهدًا بالكود ويريد تشطيبًا فيلميًا بمنحنى ACES وتلوين ظلال وإضاءات وحبيبات / for code-painted scenes needing an ACES-fitted filmic curve, a shadow/highlight split grade and seeded grain

**كيف:** filmic(exposure, contrast, saturation, lift) with y = x(2.51x+.03)/(x(2.43x+.59)+.14) — scenes that use it set ROLLOFF = 1.0; grade(shadows, highlights, amount, contrast); grain(amount, seed). Shipped: whale (1.0, 1.14, 1.04); dragon night grade #0b0820 / #ffe9cf .45 c1.06; duck storm #0a1426 / #ffe2c4 .4 c1.08. Ran here via render.py on a gradient plate: mean abs change filmic 26.7, grade 2.1, grain 4.1 (the module imports without OpenCV; its unittest file needs OpenCV).

**المعاملات:** ACES fit; grade amount .4–.45; grain .02

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** فيلمي · رسام · تقسيم لوني · filmic · aces · split tone · painter · pillow · رسم بالكود · حبيبات · منحنى فيلمي · film grain · code painting · tone curve

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:opencv` ← python3 -c "import opencv" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-62` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-studio/render.py:769`
- `kosif-studio/render.py:797`
- `kosif-studio/scenes/whale_dragon.py:287`
- `kosif-studio/scenes/dragon_girl.py:414`

#### 7. قدرات قريبة في العائلة

- `COLOR-60` تمريرة تلوين الشيدر / Shader grade pass driven by story or music (ready)
- `COLOR-61` ألوان مصادر الضوء العملية / Named practical light colours (sodium, mercury, moon, flame) (ready)
- `COLOR-63` انضغاط الإضاءات العالية / Highlight roll-off quantiser (proven)
- `COLOR-64` التعتيم الطرفي في كل محرك / Vignette in every engine (proven)

### `COLOR-63` — انضغاط الإضاءات العالية / Highlight roll-off quantiser

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يحوّل اللوحة العائمة إلى 8 بت بكتف tanh فوق نقطة ركبة، فتبقى النار والتوهج غنية بدل القص — وركبة 1.0 تحفظ ألوان الشعار بدقة. / Converts the float canvas to 8-bit with a tanh shoulder above a knee so fire and glows stay rich instead of clipping; knee 1.0 keeps logo colours exact.

**متى:** حين تحترق النار أو التوهج إلى أبيض مسطح عند تحويل الصورة إلى 8 بت، أو يجب أن تبقى ألوان الشعار مطابقة تمامًا / when fire and glows clip to flat white converting to 8-bit, or logo colours must stay exact

**كيف:** to_uint8(rolloff=k): x > k → k + (1−k)·tanh((x−k)/(1−k)); default 0.82, filmic scenes 1.0. Ran here: a pure white fill renders (244,244,244) at the default knee and (255,255,255) at 1.0. (code snippet in references/powers/color-palette-grading.md)

**المعاملات:** knee .82 default; 1.0 exact colours

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إضاءات عالية · قص · توهج · highlight rolloff · tanh · clipping · tone curve · احتراق الإضاءة · نار · 8 بت · blown highlights · glow · 8-bit

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-63` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-studio/render.py:820`
- `kosif-studio/scenes/whale_dragon.py:30`
- `kosif-studio/tests/test_studio.py:99`

#### 7. قدرات قريبة في العائلة

- `COLOR-61` ألوان مصادر الضوء العملية / Named practical light colours (sodium, mercury, moon, flame) (ready)
- `COLOR-62` تشطيب الرسام الفيلمي / Painter filmic curve, split-tone grade and grain (proven)
- `COLOR-64` التعتيم الطرفي في كل محرك / Vignette in every engine (proven)
- `COLOR-65` تدرجات بشفافية وأنماط دمج / Gradient paints with alpha stops and blend modes (proven)

### `COLOR-64` — التعتيم الطرفي في كل محرك / Vignette in every engine

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تعتيم الأطراف لتركيز العين في المركز — بنفس الروح في Canvas وthree.js وFFmpeg وCSS ومشاهد الرسام. / Edge darkening that focuses the centre — the same intent in Canvas, three.js, FFmpeg, CSS and painter scenes.

**متى:** حين يريد المستخدم تعتيم حواف الإطار لتوجيه العين للمركز في Canvas أو three.js أو FFmpeg أو CSS / when the user wants a vignette to focus the centre, in Canvas, three.js, FFmpeg, CSS or painter scenes

**كيف:** 2D motion-kit: MOTION.vignette(stage, {inner:55%, strength:.42, z:89}) = transparent to 55% → rgba(0,0,0,.42). Painter: vignette(strength) smoothstep from 35% of the half-diagonal, typical .45–.6 (ran here). TSL/WebGPU: v = clamp(1 − dist·1.5, 0, 1); color.rgb *= v. FFmpeg: vignette=PI/5 (Basma uses it when strength > 0.3; I used PI/4.5 in tests). CSS: radial-gradient overlay. Photo stacks 10–15% (COLOR-82).

**المعاملات:** inner 55% / .42; painter .45–.6; TSL falloff 1.5; ffmpeg PI/5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تعتيم الأطراف · فينيت · تركيز · vignette · focus · edges · تغميق الحواف · تركيز العين · إطار مظلم · darken edges · ffmpeg · css

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-64` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-studio/render.py:782`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:457`
- `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/post-processing.md`
- `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:457`

#### 7. قدرات قريبة في العائلة

- `COLOR-62` تشطيب الرسام الفيلمي / Painter filmic curve, split-tone grade and grain (proven)
- `COLOR-63` انضغاط الإضاءات العالية / Highlight roll-off quantiser (proven)
- `COLOR-65` تدرجات بشفافية وأنماط دمج / Gradient paints with alpha stops and blend modes (proven)
- `COLOR-66` قلب القطبية بين الفصول / Polarity flip ink↔paper at act boundaries (proven)

### `COLOR-65` — تدرجات بشفافية وأنماط دمج / Gradient paints with alpha stops and blend modes

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تعبئة أي شكل أو نص بتدرج خطي أو شعاعي بمحطات تحمل شفافية (#rrggbbaa)، مع تنعيم ودمج normal/add/screen/multiply. / Fill any shape or text with linear/radial gradients whose stops carry alpha (#rrggbbaa), softened by blur, with normal/add/screen/multiply blending.

**متى:** حين يريد المستخدم تعبئة شكل أو نص بتدرج لوني خطي أو شعاعي بشفافية وأنماط دمج / when filling a shape or text with a linear or radial gradient with alpha stops and blend modes

**كيف:** lin((x1,y1),(x2,y2),[(0,c0),…,(1,cn)]) / rad((cx,cy), r, stops), evaluated per pixel by Ctx.paint; fill(shape, paint, alpha, blur, mode). Ran here with a #0b1020→#ffb86b plate.

**المعاملات:** stops with alpha; modes normal/add/screen/multiply

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تدرج · شفافية · دمج · gradient · alpha · blend mode · radial · linear · تدرج لوني · تعبئة · تدرج للنص · gradient fill · screen · multiply

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-65` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-studio/render.py:46`
- `kosif-studio/render.py:346`
- `kosif-one/tools/kosif-studio/render.py:397`

#### 7. قدرات قريبة في العائلة

- `COLOR-63` انضغاط الإضاءات العالية / Highlight roll-off quantiser (proven)
- `COLOR-64` التعتيم الطرفي في كل محرك / Vignette in every engine (proven)
- `COLOR-66` قلب القطبية بين الفصول / Polarity flip ink↔paper at act boundaries (proven)
- `COLOR-67` فصول وضربات بحقول لونية / Colour-field chapter and beat flips (seen)

### `COLOR-66` — قلب القطبية بين الفصول / Polarity flip ink↔paper at act boundaries

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | motion-kit runs on GSAP — GSAP 'Standard no-charge' license (gsap.com/standard-license), not MIT. |

**ما هي:** المسرح يبدّل الخلفية والمقدمة (حبر↔ورق) عند حدود الفصل راكبًا القطع — من الفوضى المظلمة إلى الحل المضيء، أو من الفاتح إلى «الصورة الأكبر». / The stage swaps background and foreground (ink↔paper) at an act boundary, riding a cut — dark chaos to airy solution, or light to the 'bigger picture'.

**متى:** حين يريد المستخدم قلب الخلفية والنص بين الداكن والفاتح عند انتقال فصل في الفيديو مع القطع / when swapping background and text ink↔paper at an act boundary on a cut, e.g. dark chaos to light solution

**كيف:** MOTION.polarity(tl, stage, at, bg, fg) = one tl.to on backgroundColor + color, 0.1 s (6 f) E.smooth, only at act boundaries, never on a static frame. Ran here in Chromium with the vendored gsap: at t=0.9 s bg rgb(11,13,18), at 1.05 s mid-grey rgb(128,127,126), at 1.2 s rgb(244,241,234) with ink inverted. Observed variants: instant 0-frame switch on a drop with the hero held in place; e-ink style 2–4-frame invert flash then swap (<150 ms); #fafcf9→#0e271e over ~500 ms keeping white cards; charcoal #201f1a→cream #f6efe7 over ~300 ms at ~⅓ of the film; same hue family 90%→25% lightness for act 2.

**المعاملات:** 0.1 s E.smooth; 0–500 ms variants

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قلب القطبية · داكن فاتح · فصل · polarity · invert · act break · dark light · عكس الألوان · انتقال · أبيض وأسود · color invert · transition · gsap

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-66` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:368`
- `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:368`
- `style:pm-ik-builds-b8bdcf`
- `style:pm-xelandre-363f00`

#### 7. قدرات قريبة في العائلة

- `COLOR-64` التعتيم الطرفي في كل محرك / Vignette in every engine (proven)
- `COLOR-65` تدرجات بشفافية وأنماط دمج / Gradient paints with alpha stops and blend modes (proven)
- `COLOR-67` فصول وضربات بحقول لونية / Colour-field chapter and beat flips (seen)
- `COLOR-68` ضربة لون كامل للإطار / Full-bleed accent beat / brand flash fill (seen)

### `COLOR-67` — فصول وضربات بحقول لونية / Colour-field chapter and beat flips

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل فصل أو ضربة يملك خلفية مسطحة مشبعة من 3–4 ألوان للهوية، والقطع نفسه يصبح تغيير لون، ولون النص ينقلب ليبقى مقروءًا. / Each chapter or beat owns one flat saturated ground from a 3–4-colour brand set; every cut is also a colour change and text inverts to stay legible.

**متى:** حين يريد المستخدم أن يغيّر كل قطع أو ضربة إيقاع لون الخلفية بالكامل من ألوان الهوية مع بقاء النص مقروءًا / when every cut or beat should change the flat background to another colour from a 3–4 colour brand set

**كيف:** Keep ink colours constant, rotate grounds; flood the next colour across the frame (~400 ms) or hard-cut on the beat (≤1 flip per bar, never tweened when the brief says instant). Owner base: MOTION.polarity for two colours; HyperFrames palette-flip primitive re-skins via 0 ms variable flips anchored to section changes (needs gsap on the page — vendored as kit/gsap.min.js). (code snippet in references/powers/color-palette-grading.md) (full table in references/powers/color-palette-grading.md)

**المعاملات:** 3–4 grounds; flood ~400 ms or 0 ms on beat; ≤1 flip/bar

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خلفيات ملونة · إيقاع · فصول · color field · beat flip · chapter colors · flat background · تغيير الخلفية · ضربة الإيقاع · ألوان الهوية · background flip · on beat · brand colors

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-67` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `style:pm-bizibeast-10f264`
- `style:pm-jhylee95-e1152f`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/palette-flip/scene.html`
- `kosif-tool/styles/pm-reflex-cloud-72ffe5/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-65` تدرجات بشفافية وأنماط دمج / Gradient paints with alpha stops and blend modes (proven)
- `COLOR-66` قلب القطبية بين الفصول / Polarity flip ink↔paper at act boundaries (proven)
- `COLOR-68` ضربة لون كامل للإطار / Full-bleed accent beat / brand flash fill (seen)
- `COLOR-69` تحريك تدرج السماء ووقت اليوم / Sky-stop tweening: time of day and seasons (ready)

### `COLOR-68` — ضربة لون كامل للإطار / Full-bleed accent beat / brand flash fill

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لحظة واحدة يمتلئ فيها الإطار كله بلون الهوية أو لون صادم — للنكتة أو الوعد أو الشعار — ثم يعود المسرح. / One moment where the whole frame floods with the brand or a shock colour — for the punchline, promise or logo — then the stage returns.

**متى:** حين يريد المستخدم لحظة يمتلئ فيها الإطار كله بلون الهوية أو لون صادم عند النكتة أو الوعد أو الشعار / for one moment where the whole frame floods with the brand or a shock colour on a punchline, promise or logo

**كيف:** Tween the stage background to the brand for ~0.8 s while the hero shrinks to a tile (#1ed760 → darker #18a04a), or hard-cut to a flat accent frame with tone-on-tone serif text 15% darker and hold ~0.7 s, then collapse to a centre dash; or switch to lime for one scene with a hard cut or 200 ms fade, then back to cream; or one white punchline card in a dark film, cut in/out on the beat (~1 s). This is the one full-bleed beat COLOR-54 allows.

**المعاملات:** hold .7–1 s; fade ≤200 ms; tone-on-tone −15%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** وميض · لون الهوية · ضربة · brand flash · full bleed · accent beat · punchline · امتلاء الإطار · لحظة الشعار · نكتة · color flash · logo moment · hard cut

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-68` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `style:pm-brainextends-e19ac3`
- `style:pm-marouanegazouzi-6071d5`
- `style:pm-0xnfrith-5be616`
- `style:pm-robvjourney-ce3e1a`

#### 7. قدرات قريبة في العائلة

- `COLOR-66` قلب القطبية بين الفصول / Polarity flip ink↔paper at act boundaries (proven)
- `COLOR-67` فصول وضربات بحقول لونية / Colour-field chapter and beat flips (seen)
- `COLOR-69` تحريك تدرج السماء ووقت اليوم / Sky-stop tweening: time of day and seasons (ready)
- `COLOR-70` التلوين كقصة / Grade change as story (drain, bloom, freeze to grey) (ready)

### `COLOR-69` — تحريك تدرج السماء ووقت اليوم / Sky-stop tweening: time of day and seasons

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | GSAP 'Standard no-charge' license (gsap.com/standard-license), not MIT. |

**ما هي:** لوحة الفيلم كلها تنجرف بتحريك محطات تدرج السماء: ليل → فجر → صباح، أو غروب → شفق → ليل في لقطة واحدة، أو دورة الفصول — مع إضاءة المصابيح حين يعتم. / The whole film palette drifts by tweening sky-gradient stops: night→dawn→morning, sunset→dusk→night in one take, or a season cycle — lamps switch on as it darkens.

**متى:** حين يريد المستخدم أن تتحول السماء من ليل إلى فجر إلى صباح أو من غروب إلى ليل في لقطة واحدة، أو دورة الفصول / when the sky should drift night→dawn→morning or sunset→dusk→night in one take, or cycle the seasons

**كيف:** GSAP on SVG stop-color: tl.to('#s0', {attr:{'stop-color':…}, duration:11, ease:'sine.inOut'}, 0) then a 13.7 s second leg; silhouette fill #1d0f2c→#3a1d3c; veil opacity .38→.22 linear; stars fade out from 2 s over 9 s. Thursday-dua stops: night #0b1033/#3b1f5e/#b9507a → dawn #2b3d86/#c4677a/#ffb066 → morning #34509a/#f2a079/#ffd890. Observed: sunset #f0bd9f/#e58c8c → dusk #9f6986 → night #292142 over ~25 s; day→night with a cool grey multiply 0→35% #6a6f86 and a 300 px lamp glow; 3D: sun elevation + exposure −2 EV over 4–6 s, fog to teal-black; season parameter 0..4 (~7 s each, 1–2 s crossfades) swapping tree fill and particle emitter. gsap is vendored as kit/gsap.min.js. (code snippet in references/powers/color-palette-grading.md)

**المعاملات:** legs 11 s + 13.7 s; ~25 s single take; seasons 7 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سماء · فجر · غروب · فصول · وقت اليوم · sky gradient · time of day · sunset · dawn · seasons · شروق · ليل ونهار · تدرج السماء · sunrise · day night cycle · gsap

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-69` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-one/projects/thursday-dua-animation/source/index.html:142-151`
- `style:pm-demitiyageekzen-7770ad`
- `style:pm-itsolelehmann-e47532`
- `kosif-tool/styles/pm-kamstudiolabs-0b0824/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-67` فصول وضربات بحقول لونية / Colour-field chapter and beat flips (seen)
- `COLOR-68` ضربة لون كامل للإطار / Full-bleed accent beat / brand flash fill (seen)
- `COLOR-70` التلوين كقصة / Grade change as story (drain, bloom, freeze to grey) (ready)
- `COLOR-71` منطق الألوان السردي / Narrative colour logic (problem → solution) (seen)

### `COLOR-70` — التلوين كقصة / Grade change as story (drain, bloom, freeze to grey)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP 'Standard no-charge' license when timed with GSAP. |

**ما هي:** اللون يحكي المغزى: صورة المال تنطفئ للرمادي بصبغة حمراء عند «غير سعيد»، وصورة الفرح تومض ثم تستقر دافئة مشبعة، واللحظة تزداد غنى — أو يتجمد اللون للرمادي لمدة مقطع موسيقي ثم يعود. / Colour carries the moral: the money plate drains to grey with a red cast on 'unhappy', the joy plate flashes over-bright and settles warm and saturated, the moment keeps getting richer — or colour freezes to grey for one bar and snaps back.

**متى:** حين يريد المستخدم أن يحكي اللون المعنى: صورة تنطفئ للرمادي عند الحزن أو تتوهج دافئة عند الفرح / when colour should carry the story: drain to grey, bloom warm on joy, or freeze to grey for one bar

**كيف:** GSAP on img CSS filter: drain grayscale(.9) brightness(.7) contrast(1.15) in 0.6 s + tint rgba(80,0,0,.22); joy brightness(1.6) saturate(.6) → brightness(1) saturate(1.15) in 0.9 s; moment saturate(.9) → saturate(1.25) brightness(1.05) over 8 s; tints rgba(10,30,45,.25), rgba(20,60,110,.18), rgba(255,170,60,.08). Freeze: saturate(0) + a slight contrast drop switched in 1 frame, held one bar, snapped back on the downbeat.

**المعاملات:** drain .6 s; bloom .9 s; enrich 8 s; freeze = 1 bar

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قصة · مشاعر · رمادي · تجميد · story grade · desaturate · emotion · freeze · أبيض وأسود · حزن وفرح · تلوين درامي · black and white · mood shift · css filter

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-70` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-one/projects/whatsapp-motion/projects/success/index.html:52-59`
- `kosif-one/projects/whatsapp-motion/projects/success/index.html:146-150`
- `style:pm-samaote-5e2fc2`

#### 7. قدرات قريبة في العائلة

- `COLOR-68` ضربة لون كامل للإطار / Full-bleed accent beat / brand flash fill (seen)
- `COLOR-69` تحريك تدرج السماء ووقت اليوم / Sky-stop tweening: time of day and seasons (ready)
- `COLOR-71` منطق الألوان السردي / Narrative colour logic (problem → solution) (seen)
- `COLOR-72` لون لكل عنصر / Per-item hue coding at equal luminance (seen)

### `COLOR-71` — منطق الألوان السردي / Narrative colour logic (problem → solution)

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لون واحد لكل فصل سردي: أحمر متوهج لنقاط الألم وسماوي للعرض، وبطاقة يقلب توهجها ونصها من الأحمر للسماوي لتظهر المشكلة وهي تُحل؛ ولكل مرحلة حياة أرضيتها. / One accent per narrative act: red glow for pain points, cyan for the offer, a card whose glow and text flip red→cyan as the problem is solved; each life stage owns its ground.

**متى:** حين يصنع المستخدم فيديو أو عرضًا يبدأ بمشكلة وينتهي بحل ويريد لونًا لكل مرحلة، كأحمر للمشكلة وسماوي للعرض / for problem→solution videos or pitches with one accent per act: red for pain points, cyan for the offer

**كيف:** Ground #0a1822→#10374b radial, red #e8333f for the problem (glow + second headline line), cyan #1fb3e6 for the offer, green #2ee6a0 for proof; flip a card's glow + text over ~300 ms at the turn. Red reserved for mistakes, green for fixes (#c9463d / #1f7a4f on cream #eee8dc). Navy base, white type, orange ≤15% of the frame; red/green only in charts.

**المعاملات:** 1 accent per act; orange ≤15%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مشكلة وحل · سرد · أحمر · problem solution · narrative color · pitch · transformation · عرض تقديمي · نقاط الألم · فيديو إعلاني · pain points · storytelling · promo video

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-71` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `style:pm-ceowinkz-7c776b`
- `style:pm-henkvaness-0e06af`
- `style:pm-loicrambo-ad6830`
- `kosif-tool/styles/pm-ceowinkz-7c776b/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-69` تحريك تدرج السماء ووقت اليوم / Sky-stop tweening: time of day and seasons (ready)
- `COLOR-70` التلوين كقصة / Grade change as story (drain, bloom, freeze to grey) (ready)
- `COLOR-72` لون لكل عنصر / Per-item hue coding at equal luminance (seen)
- `COLOR-73` صبغة الإطار للحدث / Full-frame event tint and flash (seen)

### `COLOR-72` — لون لكل عنصر / Per-item hue coding at equal luminance

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل عنصر أو صوت أو فئة يحصل على صبغة واحدة تتكرر في شارته ونقطته وإطاره وتوهجه، بإضاءة متقاربة على خلفية ثابتة — والعين تتبع العنصر بلونه. / Each item, voice or class gets one hue reused on its pill, bullet, brackets and glow, at similar luminance on a constant ground — the eye tracks it by colour.

**متى:** حين يعرض المستخدم عدة عناصر أو أصوات أو فئات ويريد لكل منها لونًا ثابتًا تتبعه العين في كل ظهور / when several items, voices or classes each need one consistent hue the eye can track across pills, bullets and glows

**كيف:** Hues at ~70% saturation and similar lightness (check with COLOR-46/52); keep the base constant (navy); reuse the same colours in the recap list. Observed sets: items orange/blue/purple/amber/green/pink; instruments cyan glock, amber marimba, violet bass, red drums, yellow cymbals on navy; skills lime #c6f432 primary + #7b4fe8 / #ff2e88 / #3fd0e6 on #0a0815; multi-ink black #1c1c1c structure, red #c42d3f errors, blue #2b4a9b definitions, green #2f8a5b conclusions; hot #e8665a / cold #3ec7c0; one solid colour column per faction; sentiment classes teal/pink/yellow crossfaded.

**المعاملات:** ~70% saturation; equal luminance; ≤7 hues

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ترميز لوني · فئات · آلات · color coding · per item · categories · legend · لون لكل عنصر · تمييز الفئات · قائمة · item colors · voices · instruments

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-72` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `style:pm-gigabit-million-16b3a0`
- `style:pm-kamstudiolabs-447565`
- `style:pm-tak3sh8-be5012`
- `style:pm-ibrahimwasim240-809370`

#### 7. قدرات قريبة في العائلة

- `COLOR-70` التلوين كقصة / Grade change as story (drain, bloom, freeze to grey) (ready)
- `COLOR-71` منطق الألوان السردي / Narrative colour logic (problem → solution) (seen)
- `COLOR-73` صبغة الإطار للحدث / Full-frame event tint and flash (seen)
- `COLOR-74` حلقات بتدرج الصبغة ودوران اللون / Hue-indexed rings and slow hue rotation (seen)

### `COLOR-73` — صبغة الإطار للحدث / Full-frame event tint and flash

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يُصبغ الإطار كله بلون الحدث طوال مدته (تعويذة زرقاء، قرمزية، حمراء) ويقوى للحظة الاصطدام؛ وحالة الخطأ تصبغ حتى 15% عنبري. / Multiply/overlay the whole frame with the event colour for its duration (blue, crimson, red spell), flashing stronger on impact; an error state tints up to 15% amber.

**متى:** حين يقع في المشهد حدث مثل تعويذة أو اصطدام أو خطأ ويريد المستخدم صبغ الإطار كله بلونه مع وميض لحظة الضربة / when a spell, impact or error should tint the whole frame in its colour, flashing stronger on impact

**كيف:** Overlay div or Canvas fillRect with mix-blend-mode multiply/overlay at 30–60% for the cast, 2–3 frames stronger on impact, then release; for UI errors cap at 15%. Keep text contrast checked (COLOR-52).

**المعاملات:** tint 30–60%; flash 2–3 frames; error ≤15%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صبغة · وميض · حدث · tint · flash · impact · error state · تعويذة · اصطدام · صبغ الإطار · color overlay · spell · hit flash

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-73` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `style:pm-0xevinho-3777d8`
- `kosif-tool/styles/pm-jake11moran-a269c4/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-71` منطق الألوان السردي / Narrative colour logic (problem → solution) (seen)
- `COLOR-72` لون لكل عنصر / Per-item hue coding at equal luminance (seen)
- `COLOR-74` حلقات بتدرج الصبغة ودوران اللون / Hue-indexed rings and slow hue rotation (seen)
- `COLOR-75` عنوان بلونين وكلمة مميزة / Two-tone headline and accent word (seen)

### `COLOR-74` — حلقات بتدرج الصبغة ودوران اللون / Hue-indexed rings and slow hue rotation

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صبغة كل حلقة تُشتق من ترتيبها (وردي في الداخل حتى فيروزي في الخارج)، والعداد يأخذ لون الحلقة الداخلية؛ أو خلفية تدور صبغتها 360° كل 10 ثوانٍ بدل القطع. / Each ring's hue comes from its index (pink inside to teal outside) and the counter takes the innermost hue; or a background that rotates 360° per 10 s instead of cutting.

**متى:** حين يريد المستخدم حلقات متداخلة تتدرج ألوانها حسب ترتيبها، أو خلفية يدور لونها ببطء بدل القطع / for concentric rings coloured by index (pink inside to teal outside) or a background slowly rotating hue instead of cutting

**كيف:** hue = 330° → 185° across ring index, HSL L ~65% S ~80% on near-black; or step 30° per ring around the wheel. Rotation: CSS filter hue-rotate or a shader uniform 360°/10 s while keeping text ≥4.5:1 (check at the worst hue).

**المعاملات:** 330°→185°; L 65% S 80%; 360°/10 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حلقات · دوران الصبغة · عداد · hue rotate · rings · rainbow · index color · ألوان متدرجة · خلفية متغيرة · دوائر · hue cycle · concentric · counter

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-74` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `style:pm-kantamk-61f410`
- `kosif-tool/styles/pm-kantamk-61f410/BRIEF.md`
- `kosif-tool/styles/pm-monokern-ade5b6/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-72` لون لكل عنصر / Per-item hue coding at equal luminance (seen)
- `COLOR-73` صبغة الإطار للحدث / Full-frame event tint and flash (seen)
- `COLOR-75` عنوان بلونين وكلمة مميزة / Two-tone headline and accent word (seen)
- `COLOR-76` شريط عينات الألوان / Swatch-strip reveal (seen)

### `COLOR-75` — عنوان بلونين وكلمة مميزة / Two-tone headline and accent word

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أول العبارة بلون والنكتة بلون الهوية، أو كلمة واحدة لكل ضربة تأخذ تعبئة ليمونية وخطًا سميكًا تحتها — واللون نفسه لكل الأزرار التفاعلية. / First phrase in one colour, punchline in the brand colour, or one word per beat gets a lime fill and thick underline — the same colour reused on interactive pills.

**متى:** حين يريد المستخدم عنوانًا بلونين أو إبراز كلمة واحدة في كل ضربة بلون الهوية وخط سميك تحتها / for a two-tone headline with the punchline in the brand colour, or one highlighted word per beat with a thick underline

**كيف:** Cream #f3f0e4 + lime #d8f24a on navy #07131f; black heavy grotesk #111 with the last 1–2 words in brand orange #ef5a0c and an orange dot bullet on the kicker; strict black/white + lime #c5fc34 for the beat word, magenta #ff2bd6 only for bars and bullets. For Arabic apply the colour to whole words (see ARAB powers).

**المعاملات:** 1 accent word per beat; underline thick

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عنوان · كلمة مميزة · لونان · headline · accent word · two tone · highlight · إبراز كلمة · تايتل · خط تحت الكلمة · keyword highlight · underline · title

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-75` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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
- `style:pm-paulo-kombucha-96431c`
- `style:pm-techhalla-7acbc2`

#### 7. قدرات قريبة في العائلة

- `COLOR-73` صبغة الإطار للحدث / Full-frame event tint and flash (seen)
- `COLOR-74` حلقات بتدرج الصبغة ودوران اللون / Hue-indexed rings and slow hue rotation (seen)
- `COLOR-76` شريط عينات الألوان / Swatch-strip reveal (seen)
- `COLOR-77` باليت مفهرسة من 16 لونًا / Indexed 16-colour palette with alternating accent flash (idea)

### `COLOR-76` — شريط عينات الألوان / Swatch-strip reveal

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صف من ستة مربعات ألوان بأسماء hex تحتها يظهر من اليسار لليمين كدليل «كتاب الأسلوب». / A row of six colour squares with hex labels pops in left to right as a 'style book' proof.

**متى:** حين يريد المستخدم عرض لوحة ألوان الهوية في الفيديو كمربعات بأكواد hex تظهر بالتتابع / when showing a brand palette on screen as a row of swatches with hex labels popping in one by one

**كيف:** 40 px squares, mono hex labels 8 px under each, stagger 50 ms, scale 0→1 with a small overshoot; feed it the palette from COLOR-24 or COLOR-31 (RTL layouts reverse the order).

**المعاملات:** 40 px; mono 8 px; stagger 50 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عينات ألوان · هوية · swatches · style guide · palette reveal · لوحة الألوان · كتاب الأسلوب · أكواد الألوان · hex labels · brand book

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-76` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `style:pm-kyonax-on-tech-aabc1d`

#### 7. قدرات قريبة في العائلة

- `COLOR-74` حلقات بتدرج الصبغة ودوران اللون / Hue-indexed rings and slow hue rotation (seen)
- `COLOR-75` عنوان بلونين وكلمة مميزة / Two-tone headline and accent word (seen)
- `COLOR-77` باليت مفهرسة من 16 لونًا / Indexed 16-colour palette with alternating accent flash (idea)
- `COLOR-78` أرضيات داكنة شعاعية / Radial dark grounds (proven)

### `COLOR-77` — باليت مفهرسة من 16 لونًا / Indexed 16-colour palette with alternating accent flash

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فكرة: سقف 16 لونًا للفيلم كله، ولونا تمييز يتبادلان على الإطارات الفردية والزوجية لثلاثة إطارات عند كل تعويذة، وومضة أخيرة بأربعة ألوان. / Idea: cap the whole film at 16 colours; two accents alternate on odd/even frames for 3 frames per spell, and a final 4-colour flash.

**متى:** حين يريد المستخدم فيلمًا بطابع ريترو محدودًا بستة عشر لونًا مع ومضة تمييز متناوبة عند كل تعويذة / for a retro look capping the whole film at 16 colours, with two accents alternating on frame parity per spell

**كيف:** Untested: keep an indexed palette array, quantise every frame to it (Pillow quantize with a fixed palette or HyperFrames ordered dither), swap the two accent indices on frame parity for 3 frames.

**المعاملات:** 16 colours; 2 accents; 3-frame flash

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بكسل · ريترو · 16 لون · indexed palette · pixel art · retro · flash · بكسل آرت · تقليل الألوان · لوحة محدودة · quantize · dither

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-77` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-tool/styles/pm-0xevinho-3777d8/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-75` عنوان بلونين وكلمة مميزة / Two-tone headline and accent word (seen)
- `COLOR-76` شريط عينات الألوان / Swatch-strip reveal (seen)
- `COLOR-78` أرضيات داكنة شعاعية / Radial dark grounds (proven)
- `COLOR-79` أرضية ورقية كريمية / Warm paper editorial ground (seen)

### `COLOR-78` — أرضيات داكنة شعاعية / Radial dark grounds

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خلفية داكنة بمركز أفتح قليلًا — كحلي تقني، جمر دافئ، توهج أحمر، HUD دافئ — وهي بداية القالب المختبر. / A dark ground with a slightly lighter centre — tech navy, ember, red glow, warm HUD — and the tested starter's default.

**متى:** حين يحتاج المستخدم خلفية داكنة غير مسطحة بمركز أفتح قليلًا لفيديو تقني أو موشن أو مشهد ثلاثي الأبعاد / when a scene needs a dark ground with a slightly lighter centre: tech navy, ember, red glow or warm HUD

**كيف:** Canvas starter: radial-gradient(#182446 → #0b1020 55%) + 90 px grid at .045 (tested). Fastify: createLinearGradient(0,0,w,h) stop0 #0c1728 on even scenes / #132337 on odd → #090d1d, so consecutive scenes breathe. 3D: K3S.studioBackdrop({inner #1e4a44, mid #0c2224 at 55%, outer #050c0d, cy .42}) as scene.background (512 px canvas). Observed: navy #131e35 → #0a121f; ember: black + off-centre #43211a at 40%; warm HUD #3a1a0e → #0e0e0b + 40 px grid at 4% + vignette; dark + radial red 15%; navy + gold accent.

**المعاملات:** centre→edge 55%; grid 90 px @ .045; alt start per scene

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خلفية داكنة · شعاعي · كحلي · dark background · radial gradient · navy · hud · خلفية تقنية · توهج · شبكة · tech background · backdrop · grid

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-78` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-tool/starters/html-canvas/index.html:14`
- `fastify-motion-bro/web/motion.js:9`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:336`
- `style:pm-tankazunori0914-0fc886`

#### 7. قدرات قريبة في العائلة

- `COLOR-76` شريط عينات الألوان / Swatch-strip reveal (seen)
- `COLOR-77` باليت مفهرسة من 16 لونًا / Indexed 16-colour palette with alternating accent flash (idea)
- `COLOR-79` أرضية ورقية كريمية / Warm paper editorial ground (seen)
- `COLOR-80` خلفية بقع ضبابية متحركة / Drifting blob / mesh-gradient ambient ground (install)

### `COLOR-79` — أرضية ورقية كريمية / Warm paper editorial ground

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ورق كريمي دافئ بحبر شبه أسود ولون واحد للفعل، مع فينيت شعاعي خفيف — للفصول الهادئة والخاتمات العاطفية والشرح التحريري. / Warm cream paper with near-black ink and one action colour, under a faint radial vignette — for calm chapters, emotional outros and editorial explainers.

**متى:** حين يريد المستخدم خلفية ورقية كريمية دافئة لفصل هادئ أو خاتمة عاطفية أو شرح تحريري / for a warm cream paper ground with near-black ink and one action colour, for calm chapters, emotional outros or explainers

**كيف:** Base #f4eee0 / ink #1f1b17 / highlight #f6cf9a / action #d9472b; radial #fcf7ed → #f2ebe1 with rust #c0502e; #efefe5 with an 8% vignette behind dark UI cards; #e6e1d2 with a 35% edge vignette and coral accent words in italic serif; split variant: two close grounds #f6f2e9 / #ebdcc7 with a soft shadow seam, coffee ink #3e2a20, terracotta #b0643a. Owner equivalents: ledger #fbf8f3 (COLOR-32), viral-editorial palettes 1/3 (COLOR-39).

**المعاملات:** vignette 8–35%; one action colour

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ورق · كريمي · تحريري · paper · cream · editorial · warm background · خلفية فاتحة · بيج · خاتمة · light background · beige · outro

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-79` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `style:pm-1stnoel-c20a89`
- `style:pm-ho-ba-f3f0e9`
- `style:pm-kloss-xyz-15182a`
- `style:pm-sarut0bisasuke-cefa43`

#### 7. قدرات قريبة في العائلة

- `COLOR-77` باليت مفهرسة من 16 لونًا / Indexed 16-colour palette with alternating accent flash (idea)
- `COLOR-78` أرضيات داكنة شعاعية / Radial dark grounds (proven)
- `COLOR-80` خلفية بقع ضبابية متحركة / Drifting blob / mesh-gradient ambient ground (install)
- `COLOR-81` لوحات شيدر WebGPU / WebGPU shader colour plates (install)

### `COLOR-80` — خلفية بقع ضبابية متحركة / Drifting blob / mesh-gradient ambient ground

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | the HyperFrames blocks are timed with GSAP — GSAP 'Standard no-charge' license; the pure-CSS recipe needs no licence. |

**ما هي:** 3–4 بقع لونية ضخمة شديدة الضبابية تنجرف ببطء على أساس فاتح أو داكن — شفق بنفسجي برتقالي أسفل الإطار، أو باستيل خوخي ولافندر، أو تدرج خطي باستيل مع شبكة نقاط. / 3–4 huge, heavily blurred colour blobs drifting slowly over a light or dark base — violet/orange aurora along the bottom, peach/lavender pastels, or a pastel linear gradient with a dot grid.

**متى:** حين يريد المستخدم خلفية ناعمة متحركة من بقع لونية ضبابية تنجرف ببطء، بنفسجية برتقالية أو باستيل / when the user wants a soft animated background of huge blurred colour blobs drifting slowly, aurora or pastel

**كيف:** Pure CSS (works now): absolutely positioned divs with radial-gradient(closest-side, colour, transparent), size 60–80% of width, opacity .15–.9, blur 120–300 px, sine drift period 8–12 s (10–40 px per 10 s); warm one blob up on a key event. Pastel linear: linear-gradient(180deg, #c4a4ed, #f3daed) with #1c1838 text (>7:1), or 30° peach #f6eada → lavender #dfe4f2 with 1 px dots every 24 px at 8%. Shader: noise(uv·k + t·0.05) mixing #00F0FF / #7000FF / #000000. HyperFrames ready blocks: mesh-gradient-bg, mk-background (10 s, 1920×1080, GSAP). (code snippet in references/powers/color-palette-grading.md)

**المعاملات:** blur 120–300 px; period 8–12 s; dots 1 px / 24 px @ 8%

**التثبيت:** npm i -D hyperframes@0.8.164 && npx hyperframes add mesh-gradient-bg

**الوسوم:** بقع ضبابية · شفق · باستيل · خلفية متحركة · mesh gradient · aurora · blob · pastel · ambient · خلفية ناعمة · تدرج متحرك · ضبابي · animated gradient · soft background · css

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-80` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `style:product`
- `kosif-one/vendor/hyperframes/registry/components/mesh-gradient-bg/mesh-gradient-bg.html`
- `kosif-one/vendor/hyperframes/registry/blocks/mk-background/mk-background.html`
- `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-78` أرضيات داكنة شعاعية / Radial dark grounds (proven)
- `COLOR-79` أرضية ورقية كريمية / Warm paper editorial ground (seen)
- `COLOR-81` لوحات شيدر WebGPU / WebGPU shader colour plates (install)
- `COLOR-82` توحيد الطبقات / Unify the stack: one grade, grain, vignette (documented)

### `COLOR-81` — لوحات شيدر WebGPU / WebGPU shader colour plates

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 AND MIT (see lib/shaders.THIRD-PARTY-LICENSES.txt). |

**ما هي:** سبع خلفيات شيدر جاهزة مدة كل منها ثانيتان: بقعة مرجانية، عجلة ألوان، تدرج متدفق، خريطة حرارية، تدرج شبكي، بلازما، دوامة. / Seven ready 2 s shader plates: coral Blob, ColorWheel, FlowingGradient, Heatmap orb, MeshGradient, Plasma, Swirl.

**متى:** حين يحتاج المستخدم خلفية شيدر متحركة جاهزة مثل بلازما أو دوامة أو تدرج متدفق أو عجلة ألوان / when a ready animated shader background is needed: plasma, swirl, flowing gradient, mesh gradient or colour wheel

**كيف:** `npx hyperframes add blob\|color-wheel\|flowing-gradient\|heatmap\|mesh-gradient\|plasma\|swirl`, or place lib/shaders.iife.js (1,444,793 bytes, shaders 4.0.0) beside the HTML and declare <canvas data-shader="Plasma" width=1920 height=1080> in a root marked data-requires-webgpu data-no-timeline. Rendering needs a WebGPU-capable Chromium — headless WebGPU is not verified here; fall back to COLOR-80's CSS blobs if it fails.

**المعاملات:** 7 shaders; 1920×1080; 2 s loops

**التثبيت:** npm i -D hyperframes@0.8.164 && npx hyperframes add plasma

**الوسوم:** شيدر · بلازما · خلفية · webgpu · shader · plasma · gradient · background plate · خلفية متحركة · دوامة · تدرج متدفق · animated background · swirl · hyperframes

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-81` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-one/vendor/hyperframes/registry/blocks/plasma/plasma.html`
- `kosif-one/vendor/hyperframes/registry/blocks/mesh-gradient/registry-item.json`
- `kosif-one/vendor/hyperframes/registry/blocks/blob/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### 7. قدرات قريبة في العائلة

- `COLOR-79` أرضية ورقية كريمية / Warm paper editorial ground (seen)
- `COLOR-80` خلفية بقع ضبابية متحركة / Drifting blob / mesh-gradient ambient ground (install)
- `COLOR-82` توحيد الطبقات / Unify the stack: one grade, grain, vignette (documented)
- `COLOR-83` سلم المعالجة / Treatment ladder: colour → duotone → halftone → vector (documented)

### `COLOR-82` — توحيد الطبقات / Unify the stack: one grade, grain, vignette

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تلوين واحد فوق التركيب كله، وحبيبات 2–4%، وفينيت 10–15%، وظل تلامس لكل قصاصة — حتى تُقرأ الطبقات كصورة واحدة. / One grade over the whole composition, 2–4% grain, a 10–15% vignette and a contact shadow for every cut-out, so layers read as one photograph.

**متى:** حين تبدو طبقات الكولاج أو القصاصات منفصلة ويريد المستخدم أن تُقرأ كصورة واحدة بتلوين وحبيبات وفينيت موحد / when composited layers or cut-outs look pasted on and must read as one photo with one grade, grain and vignette

**كيف:** Grade the final composite, not each layer (a per-layer warm over-sharpened HDR grade never fuses); grain 2–4%; vignette 10–15%; contact shadow blur 24 px, offset 0, opacity .35. Check question before render: is one grade plus grain applied to the whole stack?

**المعاملات:** grain 2–4%; vignette 10–15%; shadow 24 px @ .35

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كولاج · توحيد · حبيبات · collage · composite · grain · unify · تركيب · دمج الطبقات · ظل تلامس · layers · cut-out · contact shadow

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-82` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-tool/playbooks/photos.md:21`

#### 7. قدرات قريبة في العائلة

- `COLOR-80` خلفية بقع ضبابية متحركة / Drifting blob / mesh-gradient ambient ground (install)
- `COLOR-81` لوحات شيدر WebGPU / WebGPU shader colour plates (install)
- `COLOR-83` سلم المعالجة / Treatment ladder: colour → duotone → halftone → vector (documented)
- `COLOR-84` تشطيب الكولاج العتيق مع الوميض / Vintage collage finish with exposure flicker (seen)

### `COLOR-83` — سلم المعالجة / Treatment ladder: colour → duotone → halftone → vector

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الصورة تنزل درجات الأسلوب على الإيقاع أو الكلمات: لون كامل، ثنائي اللون، هافتون، ثم فيكتور مسطح — ونسخ بوب آرت ثنائية اللون بتوقيت متتابع. / A photo steps down stylisations on beats or words: full colour, duotone, halftone, flat vector — plus pop-art duotone clones with offset timing.

**متى:** حين يريد المستخدم أن تتحول صورة على الإيقاع أو الكلمات من ألوان كاملة إلى لونين ثم هافتون ثم فيكتور مسطح / when a photo should step on beats or words from full colour to duotone, halftone, then flat vector

**كيف:** duotone 300 ms → halftone 300 ms → flat vector 400 ms, each on a beat or word boundary; luma threshold 0.5; dot pitch 8–12 px at 1080 width. Duotone = map luma between two hex (CSS: grayscale + two blended layers; FFmpeg: format=gray then lut/colorize; HyperFrames two-ink-print). Tiles: one duotone shader per tile with staggered starts.

**المعاملات:** 300/300/400 ms; threshold .5; pitch 8–12 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ثنائي اللون · هافتون · بوب آرت · duotone · halftone · pop art · stylize · لونين · نقاط طباعة · تحويل الصورة · flat vector · on beat · two ink

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-83` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `kosif-tool/playbooks/photos.md:42`
- `style:pm-topi-003-b0e12c`

#### 7. قدرات قريبة في العائلة

- `COLOR-81` لوحات شيدر WebGPU / WebGPU shader colour plates (install)
- `COLOR-82` توحيد الطبقات / Unify the stack: one grade, grain, vignette (documented)
- `COLOR-84` تشطيب الكولاج العتيق مع الوميض / Vintage collage finish with exposure flicker (seen)
- `COLOR-85` لوحات الغروب والسايكدلك والدفع الأحادي / Sunset/synthwave, psychedelic and monohue-push palettes (seen)

### `COLOR-84` — تشطيب الكولاج العتيق مع الوميض / Vintage collage finish with exposure flicker

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عوالم كولاج فوتوغرافي بتلوين عتيق باهت: نزع 40% من التشبع، صبغة سيبيا، فينيت داكن، حبيبات متحركة، ووميض تعريض خفيف. / Photo-collage worlds under a muted vintage grade: ~40% desaturation, sepia tint, dark vignette, animated grain and a slight exposure flicker.

**متى:** حين يريد المستخدم لوكًا قديمًا باهتًا بسيبيا وحبيبات ووميض تعريض خفيف لكولاج صور / for a muted vintage collage look: desaturation, sepia tint, dark vignette, moving grain and slight exposure flicker

**كيف:** Observed numbers: vignette 0.6, grain 8%, flicker ±3% luminance; palette #221d17 / #332b22 / #6b746d / #a09b89 / #c4c2b3 / #928573. FFmpeg recipe (this exact chain ran here; YAVG swung 89.3–99.3 across 30 frames): hue=s=0.6 → a 50% sepia colorchannelmixer → eq brightness 0.03·sin(2π·6t) with eval=frame → vignette → noise alls=8 allf=t+u. (code snippet in references/powers/color-palette-grading.md)

**المعاملات:** desat 40%; vignette .6; grain 8%; flicker ±3% at ~6 Hz

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عتيق · سيبيا · وميض · كولاج · vintage · sepia · flicker · collage · film · لوك قديم · فيلم قديم · حبيبات · retro · old film · ffmpeg

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-84` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `style:pm-koldo2k-5cff87`

#### 7. قدرات قريبة في العائلة

- `COLOR-82` توحيد الطبقات / Unify the stack: one grade, grain, vignette (documented)
- `COLOR-83` سلم المعالجة / Treatment ladder: colour → duotone → halftone → vector (documented)
- `COLOR-85` لوحات الغروب والسايكدلك والدفع الأحادي / Sunset/synthwave, psychedelic and monohue-push palettes (seen)
- `COLOR-86` طين أبيض ولون للبيانات فقط / White clay render with colour only for data (seen)

### `COLOR-85` — لوحات الغروب والسايكدلك والدفع الأحادي / Sunset/synthwave, psychedelic and monohue-push palettes

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سماء خوخية وردية نيلية مع ظلال بنفسجية وإضاءات برتقالية، وشمس عملاقة مخططة، ولوحة سايكدلك نيلية برتقالية وردية ليمونية، ودفع كل الصور نحو بنفسجي واحد بسواد مسحوق. / Peach→pink→indigo skies with purple shadows and orange highlights, a giant striped sun, an indigo/orange/pink/lemon psychedelic palette, and pushing all imagery toward one violet with crushed blacks.

**متى:** حين يريد المستخدم سماء غروب وردية نيلية أو شمس سينثويف مخططة أو ألوان سايكدلك أو دفع الصور نحو بنفسجي واحد / for sunset or synthwave skies, a psychedelic palette, or pushing all imagery toward one violet

**كيف:** Sunset: sky #f5c798 → #e5a880 → #9a6766 → #170926, lift shadows to purple, highlights to orange, slight vignette. Synthwave sun: radial red gradient disc with horizontal dark bands in its bottom third. Monohue push: base #0c0b10, accent #9a6cf0, crush blacks, lift highlights, grain 4% + vignette for cohesion (FFmpeg: hue=s=0.4 then colorbalance toward violet, or a Reinhard transfer to a violet reference, COLOR-26).

**المعاملات:** sunset 4 stops; violet push grain 4%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** غروب · سينثويف · بنفسجي · سايكدلك · sunset · synthwave · psychedelic · monochrome push · violet · شمس مخططة · سماء وردية · دفع لوني · striped sun · crushed blacks

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-85` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `style:pm-axtonliu-0b861d`
- `style:pm-chrisjdimarco-f068db`
- `style:pm-gizakdag-cf4ae6`
- `style:pm-influencer-seo-ce8c33`

#### 7. قدرات قريبة في العائلة

- `COLOR-83` سلم المعالجة / Treatment ladder: colour → duotone → halftone → vector (documented)
- `COLOR-84` تشطيب الكولاج العتيق مع الوميض / Vintage collage finish with exposure flicker (seen)
- `COLOR-86` طين أبيض ولون للبيانات فقط / White clay render with colour only for data (seen)
- `COLOR-X01` حزمة أسلوب مقيسة والتدريج بالقياس / Measured style pack and grading by measurement (documented)

### `COLOR-86` — طين أبيض ولون للبيانات فقط / White clay render with colour only for data

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مشهد ثلاثي الأبعاد كله رمادي فاتح كالطين، بإضاءة نصف كروية وضباب أبيض، واللون محجوز فقط لتدفق البيانات. / A 3D scene entirely in light-grey clay under hemisphere light and white fog, with colour reserved only for data flows.

**متى:** حين يريد المستخدم مشهدًا ثلاثي الأبعاد رماديًا كالطين بالكامل مع حجز اللون لتدفق البيانات فقط / for a 3D scene entirely in light-grey clay with colour reserved only for the moving data flows

**كيف:** MeshStandardMaterial light grey (roughness high), HemisphereLight, white FogExp2; tone mapping neutral (COLOR-57); the only saturated colour is the moving data (one hue per flow, COLOR-72).

**المعاملات:** 1 data hue per flow; everything else grey

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** طين · ثلاثي · بيانات · clay render · monochrome 3d · data flow · architecture · ثلاثي الأبعاد · رمادي فاتح · تدفق البيانات · grey scene · data visualization

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-86` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `style:pm-sayan-shanky-f850d8`

#### 7. قدرات قريبة في العائلة

- `COLOR-84` تشطيب الكولاج العتيق مع الوميض / Vintage collage finish with exposure flicker (seen)
- `COLOR-85` لوحات الغروب والسايكدلك والدفع الأحادي / Sunset/synthwave, psychedelic and monohue-push palettes (seen)
- `COLOR-X01` حزمة أسلوب مقيسة والتدريج بالقياس / Measured style pack and grading by measurement (documented)

### `COLOR-X01` — حزمة أسلوب مقيسة والتدريج بالقياس / Measured style pack and grading by measurement

| الحقل | القيمة |
|---|---|
| العائلة | `color-palette-grading` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/color-palette-grading.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | MIT (ECC, (c) 2026 Affaan Mustafa) |

**ما هي:** البرومبت لا يصنع تدريجًا لونيًا؛ القياس يصنعه: قِس الكروما لكل منطقة إضاءة والوسيط والتباين ونسبة الخلفية الداكنة، ثم طبّق الفرق. — A prompt cannot deliver a grade; measurement can: measure chroma per lightness zone, medians, contrast and dark-background share, then apply the difference.

**متى:** مطابقة مظهر فيديو مرجعي أو تثبيت لون سلسلة لقطات مولدة — matching a reference look or locking colour across generated shots.

**كيف:** Measure in CIELAB: chroma per L* zone with edges [0, 15, 35, 55, 75, 100] (print the whole curve); median + MAD, not mean + std (skew inflated a mean ~2×, 36.9 vs 17.5); contrast = std(L*); background share = pixels below L* 10 as its own statistic; mask UI chrome (letterbox, status bar, icons) first. Generate neutral ('Colour: none. Render neutral.') and grade afterwards: in the source, three paid generations moved midtone a* only +1.9…+0.3 against a +24.9 target, while one measured pass hit chroma MAE 1.88. Apply: direct measurement beat a baked LUT (MAE 1.58); anchor tone instead of CDF matching when histograms differ (background kept 69 % vs 26 %); grade in batches of 6 frames (48 ran out of memory); never ship on MAE alone, check the background share too. One pack per genre.

**المعاملات:** L* zones 0/15/35/55/75/100; median+MAD; batch 6 frames

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** grade · lut · lab · style match · measurement · تدريج لوني · قياس · مطابقة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:COLOR-X01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `app-studio-paint` · `fetch-reference` · `mimic` · `reference-edit-engine` · `reference-visual-fingerprint` · `style-library`.
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

- `https://github.com/affaan-m/ECC/tree/main/skills/taste-distillation/SKILL.md`
- `https://github.com/affaan-m/ECC/tree/main/skills/taste-application/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `COLOR-85` لوحات الغروب والسايكدلك والدفع الأحادي / Sunset/synthwave, psychedelic and monohue-push palettes (seen)
- `COLOR-86` طين أبيض ولون للبيانات فقط / White clay render with colour only for data (seen)

