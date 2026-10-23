# `shapes-morph-geometry` — الرسم والأشكال والتصميم (97 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/shapes-morph-geometry.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/drawing.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`SHAPE-01` تحويل المسار بإعادة العينات](#shape-01--تحويل-المسار-بإعادة-العينات--seek-safe-path-morph-motionmorphpath)
- [`SHAPE-02` قانون التحويل: نقاط متساوية واتجاه واحد](#shape-02--قانون-التحويل-نقاط-متساوية-واتجاه-واحد--morph-law-equal-points-same-winding)
- [`SHAPE-03` فائق الإهليلج بحلقات صدى](#shape-03--فائق-الإهليلج-بحلقات-صدى--superellipse-morph-with-echo-rings)
- [`SHAPE-04` تحويل بدالة قطبية](#shape-04--تحويل-بدالة-قطبية--polar-function-shape-morph)
- [`SHAPE-05` تحويل المضلعات وأشكال باوهاوس](#shape-05--تحويل-المضلعات-وأشكال-باوهاوس--polygon--bauhaus-primitive-morph)
- [`SHAPE-06` تحويل بنابض ونجوم تدور](#shape-06--تحويل-بنابض-ونجوم-تدور--spring-shape-morph-with-orbiting-stars)
- [`SHAPE-07` تحويل بصدى ملون أو أثر ضبابي](#shape-07--تحويل-بصدى-ملون-أو-أثر-ضبابي--morph-with-coloured-echo--blur-trail)
- [`SHAPE-08` تحويل داخل صندوق أداة تصميم](#shape-08--تحويل-داخل-صندوق-أداة-تصميم--design-tool-gizmo-morph)
- [`SHAPE-09` تحويل سحابة نقاط إلى أيقونة أو شبكة](#shape-09--تحويل-سحابة-نقاط-إلى-أيقونة-أو-شبكة--dot-cloud-morph-scatter--grid--icon)
- [`SHAPE-10` شريط ينثني فيصير حلقة](#shape-10--شريط-ينثني-فيصير-حلقة--bar-bends-into-a-ring)
- [`SHAPE-11` رسم يدوي يصير نظيفًا](#shape-11--رسم-يدوي-يصير-نظيفًا--sketch-to-clean-morph)
- [`SHAPE-12` تحول متعدد الأوجه](#shape-12--تحول-متعدد-الأوجه--facet-morph-36-low-poly-triangles)
- [`SHAPE-13` تحويل SVG بإضافة MorphSVG](#shape-13--تحويل-svg-بإضافة-morphsvg--morphsvg-plugin-morph-hyperframes-rule)
- [`SHAPE-14` أسلوب الأشكال السائلة](#shape-14--أسلوب-الأشكال-السائلة--liquid-morph-style)
- [`SHAPE-15` العنصر المشترك (FLIP)](#shape-15--العنصر-المشترك-flip--flip--shared-element-continuity)
- [`SHAPE-16` البطاقة كمرساة انتقال](#shape-16--البطاقة-كمرساة-انتقال--card-morph-anchor-handoff)
- [`SHAPE-17` سلسلة: نقطة → زر → شريط تقدم](#shape-17--سلسلة-نقطة--زر--شريط-تقدم--morph-chain-dot--button--progress-bar--full-stop)
- [`SHAPE-18` جزيرة ديناميكية وزر ينفتح نافذة](#shape-18--جزيرة-ديناميكية-وزر-ينفتح-نافذة--dynamic-island--button-to-window-morph)
- [`SHAPE-19` مؤشر مطاطي بحافتين](#shape-19--مؤشر-مطاطي-بحافتين--two-edge-stretchy-indicator)
- [`SHAPE-20` أيقونة القائمة تصير إغلاقًا](#shape-20--أيقونة-القائمة-تصير-إغلاقًا--hamburger-to-close-morph)
- [`SHAPE-21` التحول عبر حالات الواجهة](#shape-21--التحول-عبر-حالات-الواجهة--morph-through-ui-states)
- [`SHAPE-22` نقطة تتفتح إلى واجهة أو نظام](#shape-22--نقطة-تتفتح-إلى-واجهة-أو-نظام--dot-to-interface--dot-to-system-bloom)
- [`SHAPE-23` حلقة → قزحية → غمر لوني](#shape-23--حلقة--قزحية--غمر-لوني--ring--iris--colour-flood)
- [`SHAPE-24` الشعار يصير بؤبؤ عين](#shape-24--الشعار-يصير-بؤبؤ-عين--logo-to-iris--eye-opening)
- [`SHAPE-25` نقرة وتحول لعلامة صح](#shape-25--نقرة-وتحول-لعلامة-صح--tap-ripple--circle-to-check-morph)
- [`SHAPE-26` ظرف يتحول لشارة / تجمع إلى شعار](#shape-26--ظرف-يتحول-لشارة--تجمع-إلى-شعار--envelopebadge-convergemonogram-collapsedot)
- [`SHAPE-27` فلتر اللزوجة](#shape-27--فلتر-اللزوجة--svg-goo--metaball-filter)
- [`SHAPE-28` الانقسام اللزج والكتلة الناعمة](#shape-28--الانقسام-اللزج-والكتلة-الناعمة--gooey-split--soft-blob-touch-hyperframes)
- [`SHAPE-29` تجمع الصلصال بالكرات](#shape-29--تجمع-الصلصال-بالكرات--metaball-clay-assembly)
- [`SHAPE-30` كتلة عضوية بضوضاء الرؤوس](#shape-30--كتلة-عضوية-بضوضاء-الرؤوس--noise-displaced-3d-blob)
- [`SHAPE-31` أشكال بدوال المسافة](#shape-31--أشكال-بدوال-المسافة--2d-signed-distance-shapes-union-morph-glow)
- [`SHAPE-32` نحت بحقول المسافة إلى مجسم مغلق](#shape-32--نحت-بحقول-المسافة-إلى-مجسم-مغلق--sdf-sculpting-to-a-watertight-mesh)
- [`SHAPE-33` دمج ونحت وتقاطع ناعم](#shape-33--دمج-ونحت-وتقاطع-ناعم--smooth-csg-add--sub--and)
- [`SHAPE-34` استعلام الحقل لتثبيت العناصر](#shape-34--استعلام-الحقل-لتثبيت-العناصر--field-queries-for-placement)
- [`SHAPE-35` حقل كتل وبقعة زاوية](#shape-35--حقل-كتل-وبقعة-زاوية--drifting-blob-field--corner-blob)
- [`SHAPE-36` كتلة متدرجة أو متحولة خلف النص](#shape-36--كتلة-متدرجة-أو-متحولة-خلف-النص--gradient--morphing-blob-behind-text)
- [`SHAPE-37` إطار مطاطي وقناع قضمة](#shape-37--إطار-مطاطي-وقناع-قضمة--rubber-frame-strain--bite-mask)
- [`SHAPE-38` تموج ضغطة بحرارة](#shape-38--تموج-ضغطة-بحرارة--press-ripple-with-heat-bloom)
- [`SHAPE-39` الحركة على مسار SVG](#shape-39--الحركة-على-مسار-svg--motion-along-an-svg-path)
- [`SHAPE-40` اختيار المنحنى وسرعة ثابتة](#shape-40--اختيار-المنحنى-وسرعة-ثابتة--spline-choice--arc-length-constant-speed)
- [`SHAPE-41` محلل لغة مسارات SVG كاملة](#shape-41--محلل-لغة-مسارات-svg-كاملة--full-svg-path-parser-studio)
- [`SHAPE-42` أشكال مركبة بثقوب](#shape-42--أشكال-مركبة-بثقوب--even-odd-compound-shapes--holes)
- [`SHAPE-43` عدة الأشكال الأساسية ولغة المشهد](#shape-43--عدة-الأشكال-الأساسية-ولغة-المشهد--basic-shape-kit--step-scene-language)
- [`SHAPE-44` منحنيات كاتمول-روم](#shape-44--منحنيات-كاتمول-روم--catmull-rom-smooth-curves)
- [`SHAPE-45` أنبوب بنصف قطر متغير](#shape-45--أنبوب-بنصف-قطر-متغير--variable-radius-tube-limbs-tails-flames-hair)
- [`SHAPE-46` سلاسل جبال بالإزاحة](#shape-46--سلاسل-جبال-بالإزاحة--midpoint-displacement-mountain-ridges)
- [`SHAPE-47` صندوق أيزومتري بثلاث درجات](#shape-47--صندوق-أيزومتري-بثلاث-درجات--three-tone-isometric-box)
- [`SHAPE-48` بناء نقطة ثم خط ثم مستوى](#shape-48--بناء-نقطة-ثم-خط-ثم-مستوى--point--line--plane-build)
- [`SHAPE-49` خطوط متدفقة ومسارات مخططة](#shape-49--خطوط-متدفقة-ومسارات-مخططة--flowing-dashes-striped-tubes-dotted-trails)
- [`SHAPE-50` خيوط موجية وأشرطة متلوية](#shape-50--خيوط-موجية-وأشرطة-متلوية--sine-strands--ribbon-loops)
- [`SHAPE-51` خطان قطريان فقط](#shape-51--خطان-قطريان-فقط--exactly-two-drifting-diagonal-lines)
- [`SHAPE-52` شبكة بلاطات باوهاوس](#shape-52--شبكة-بلاطات-باوهاوس--bauhaus-tile-grid-glyph-swap-on-a-distance-wave)
- [`SHAPE-53` بلاطات تروشيه بموجة تلوين](#shape-53--بلاطات-تروشيه-بموجة-تلوين--truchet-tiles-with-a-recolour-wave)
- [`SHAPE-54` موجة في شبكة أشكال](#shape-54--موجة-في-شبكة-أشكال--distance-delayed-grid-wave-rotate--scale--morph)
- [`SHAPE-55` بلاطات تنقلب وشريط لا ينتهي](#shape-55--بلاطات-تنقلب-وشريط-لا-ينتهي--tile-flips--endless-strip-loops-mg-116117)
- [`SHAPE-56` زهرة النقاط الذهبية](#shape-56--زهرة-النقاط-الذهبية--phyllotaxis-dot-flower-1375)
- [`SHAPE-57` منحنيات ليساجو](#shape-57--منحنيات-ليساجو--lissajous-curves--tangles)
- [`SHAPE-58` خطوط توليدية بأسلوب Joy Division](#shape-58--خطوط-توليدية-بأسلوب-joy-division--ridge-line-generative-waves)
- [`SHAPE-59` كسيريات وزخارف رياضية](#shape-59--كسيريات-وزخارف-رياضية--fractals-kolam-golden-spiral-kaleidoscope)
- [`SHAPE-60` جدار أيقونات مائل](#shape-60--جدار-أيقونات-مائل--tilted-icon-wall)
- [`SHAPE-61` كتل أنماط شيدرية وشبكة متحركة](#shape-61--كتل-أنماط-شيدرية-وشبكة-متحركة--hyperframes-pattern-shaders--dynamic-grid)
- [`SHAPE-62` حلقات دوران بنسب صحيحة](#shape-62--حلقات-دوران-بنسب-صحيحة--integer-ratio-rotation-loops-mg-112115)
- [`SHAPE-63` حلقات متحدة المركز بفجوات](#shape-63--حلقات-متحدة-المركز-بفجوات--rotating-gapped-concentric-rings)
- [`SHAPE-64` عنقود أقواس مدارية ونواة نابضة](#shape-64--عنقود-أقواس-مدارية-ونواة-نابضة--orbiting-arc-cluster--pulsing-donut-core)
- [`SHAPE-65` حلقات مدارية إهليلجية](#shape-65--حلقات-مدارية-إهليلجية--orbital-ellipse-rings--accents)
- [`SHAPE-66` انفجار خطوط شعاعي](#shape-66--انفجار-خطوط-شعاعي--radial-line-burst)
- [`SHAPE-67` حلقة صدمة أرضية ونبض قلب](#shape-67--حلقة-صدمة-أرضية-ونبض-قلب--shockwave-ring--heartbeat-ripple)
- [`SHAPE-68` أشعة شمسية دوارة](#shape-68--أشعة-شمسية-دوارة--rotating-sunburst-ground)
- [`SHAPE-69` حلقة نقاط تتسع بخطوط شعاعية](#shape-69--حلقة-نقاط-تتسع-بخطوط-شعاعية--expanding-dot-ring-with-radial-lines)
- [`SHAPE-70` نفق مربعات حلزوني](#shape-70--نفق-مربعات-حلزوني--spiral-square-tunnel--nested-squares)
- [`SHAPE-71` مربع يصير دائرة مع أقمار](#shape-71--مربع-يصير-دائرة-مع-أقمار--squarecircle-with-satellites--star-pop)
- [`SHAPE-72` بوابة دوامية ومصباح فرينل](#shape-72--بوابة-دوامية-ومصباح-فرينل--swirl-portal--fresnel-lamp-room)
- [`SHAPE-73` الزخرفة الثمانية من الكود](#shape-73--الزخرفة-الثمانية-من-الكود--islamic-eight-point-rosette-builder)
- [`SHAPE-74` وردة الفواصل الموسيقية](#shape-74--وردة-الفواصل-الموسيقية--interlude-rosette-verse-template)
- [`SHAPE-75` فوانيس ومسجد ونوافذ](#shape-75--فوانيس-ومسجد-ونوافذ--swaying-lanterns--mosque-silhouette)
- [`SHAPE-76` غيمة من دوائر تكبر وتعتم](#shape-76--غيمة-من-دوائر-تكبر-وتعتم--circle-cluster-cloud-that-grows-and-darkens)
- [`SHAPE-77` مكتبة 16 أيقونة متجهة](#shape-77--مكتبة-16-أيقونة-متجهة--16-icon-vector-hero-library)
- [`SHAPE-78` أيقونات SVG حية](#shape-78--أيقونات-svg-حية--living-svg-icons)
- [`SHAPE-79` قواعد الأيقونة: شبكة 24 والإغلاق](#shape-79--قواعد-الأيقونة-شبكة-24-والإغلاق--icon-rules-24-px-grid--closure)
- [`SHAPE-80` طبقات أشكال وملصقات منبثقة](#shape-80--طبقات-أشكال-وملصقات-منبثقة--shape-layers--stickeremoji-pop-ups)
- [`SHAPE-81` ملصقات زخرفية وكبسولات وسوم](#shape-81--ملصقات-زخرفية-وكبسولات-وسوم--decor-stickers-hazard-tape--floating-tag-pills)
- [`SHAPE-82` مروحة بطاقات وصور](#shape-82--مروحة-بطاقات-وصور--card--photo--swatch-fan-out)
- [`SHAPE-83` شريط تظليل مائل خلف النص](#shape-83--شريط-تظليل-مائل-خلف-النص--slanted-highlighter-bar-wipe)
- [`SHAPE-84` تغيير لون الكلمة داخل الكرة](#shape-84--تغيير-لون-الكلمة-داخل-الكرة--clip-path-colour-flip-over-a-moving-lens)
- [`SHAPE-85` تجميع من شظايا أو قطع](#shape-85--تجميع-من-شظايا-أو-قطع--shard--piece-assembly-along-a-path)
- [`SHAPE-86` شاشة مقسومة واستعارة الكسوف](#shape-86--شاشة-مقسومة-واستعارة-الكسوف--split-screen-eclipse-metaphor)
- [`SHAPE-87` بحر خطوط مع شخصية رمزية](#shape-87--بحر-خطوط-مع-شخصية-رمزية--line-art-sea-with-mascot)
- [`SHAPE-88` فاصل بشعرة](#shape-88--فاصل-بشعرة--hairline-separator-hyperframes)
- [`SHAPE-89` وحدة 24 وشبكة أعمدة](#shape-89--وحدة-24-وشبكة-أعمدة--base-unit-grid-system)
- [`SHAPE-90` سلالم الأقطار والخطوط والفراغ](#shape-90--سلالم-الأقطار-والخطوط-والفراغ--primitive-radius--stroke-scales)
- [`SHAPE-91` انضغاط وتمدد بحفظ المساحة](#shape-91--انضغاط-وتمدد-بحفظ-المساحة--area-preserving-squash--stretch)
- [`SHAPE-92` التصاق مغناطيسي وكل شيء من المركز](#shape-92--التصاق-مغناطيسي-وكل-شيء-من-المركز--magnet-snap-spring--centre-origin-rule)
- [`SHAPE-93` أسلوب المرح الهندسي (S07)](#shape-93--أسلوب-المرح-الهندسي-s07--playful-geometric-style-s07)
- [`SHAPE-G01` رقم متحرك واحد يقود كل الأشكال](#shape-g01--رقم-متحرك-واحد-يقود-كل-الأشكال--one-animated-value-drives-every-dependent-shape)
- [`SHAPE-G02` تحويل يطابق الأجزاء المشتركة](#shape-g02--تحويل-يطابق-الأجزاء-المشتركة--morph-that-matches-shared-parts)
- [`SHAPE-X01` تحوّل هندسي بلا مزج](#shape-x01--تحوّل-هندسي-بلا-مزج--geometric-morph-without-a-crossfade-letter--planet)
- [`SHAPE-X02` لقطة متصلة من عناصر مشتركة](#shape-x02--لقطة-متصلة-من-عناصر-مشتركة--one-continuous-shot-from-shared-elements)

## البطاقات / cards

### `SHAPE-01` — تحويل المسار بإعادة العينات / Seek-safe path morph (MOTION.morphPath)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP المضمّن برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license. |

**ما هي:** يأخذ عينات متساوية من المسارين (120 نقطة) ويستوفي بينهما عبر وكيل في خط GSAP، فيصير أي شكل أي شكل بلا إضافة. / Samples both SVG paths to N points and interpolates through a proxy on a GSAP timeline — any shape into any shape, no plugin, seekable.

**متى:** حين يريد المستخدم تحويل شكل SVG إلى أي شكل آخر بسلاسة دون إضافات مع إمكان التقديم والترجيع / when any SVG shape should morph into another, plugin-free and seekable on a GSAP timeline

**كيف:** MOTION.morphPath(tl, pathEl, fromD, toD, at, {points, dur, ease, open}); getPointAtLength sampling, writes "M…L…Z" each tick via modifiers, immediateRender false. Rendered here: circle→star at 0.2 s, star→square at 1.3 s on a paused timeline driven by seek(t). Start both paths at the same angle (top-centre) to avoid a twist.

**المعاملات:** N 120 points, dur .66 s, ease E.inOut; closes with Z unless open

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تحويل · مورف · morph · path · svg · shape · seek · تحول الأشكال · دائرة إلى نجمة · شكل يتحول · shape tween · gsap

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-studio/motion/kit/motion-kit.js:255`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:255`
- `kosif-studio/motion/projects/kit_v3_demo/index.html`
- `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js`

#### 7. قدرات قريبة في العائلة

- `SHAPE-02` قانون التحويل: نقاط متساوية واتجاه واحد / Morph law: equal points, same winding (documented)
- `SHAPE-03` فائق الإهليلج بحلقات صدى / Superellipse morph with echo rings (proven)

### `SHAPE-02` — قانون التحويل: نقاط متساوية واتجاه واحد / Morph law: equal points, same winding

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لا تحوّل إلا مسارين بنفس عدد النقاط ونفس اتجاه اللف؛ أعد العينات أولًا بـ flubber أو نقاط محسوبة مسبقًا. / Only morph equal-point, same-winding paths; resample first (flubber or precomputed points).

**متى:** عند تجهيز مسارين للتحويل أو ظهور التواء وتشوه أثناء المورف / when preparing two paths for a morph or fixing a twist in the in-betweens

**كيف:** Remotion: lerp [x,y] arrays with Easing.inOut(Easing.cubic); browser: flubber.interpolate(a,b,{maxSegmentLength:4}); align start points by rotating the array to the topmost vertex; reverse one path if signed areas differ.

**المعاملات:** 500–800 ms cubic-bezier(.65,0,.35,1); 64–128 points (200 for detailed shapes)

**التثبيت:** npm i flubber

**الوسوم:** تحويل · flubber · resample · winding · morph rule · إعادة العينات · التواء الشكل · اتجاه اللف · equal points · path twist

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/playbooks/shapes.md:24`
- `kosif-tool/playbooks/shapes.md:53-64`

#### 7. قدرات قريبة في العائلة

- `SHAPE-01` تحويل المسار بإعادة العينات / Seek-safe path morph (MOTION.morphPath) (proven)
- `SHAPE-03` فائق الإهليلج بحلقات صدى / Superellipse morph with echo rings (proven)
- `SHAPE-04` تحويل بدالة قطبية / Polar-function shape morph (proven)

### `SHAPE-03` — فائق الإهليلج بحلقات صدى / Superellipse morph with echo rings

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الشكل يمر عبر \|x\|ⁿ+\|y\|ⁿ=1 بأس متحرك (دائرة→مربع ناعم)، وحوله حلقات كنتور متأخرة كصدى. / Morph through \|x\|^n+\|y\|^n=1 with animated n (circle → squircle), surrounded by offset contour rings that lag behind.

**متى:** حين يطلب تحويل دائرة إلى مربع ناعم الزوايا مع حلقات صدى متأخرة حوله / when a circle should turn into a squircle with lagging echo contour rings around it

**كيف:** x = sign(cosθ)\|cosθ\|^(2/n)·R, y likewise; n tween 2→4.2; 5–7 rings at +12 px offsets each delayed 60 ms and fading; rendered here (Canvas lab). Can continue to a 3D cube or star.

**المعاملات:** n 2→4.2 in 400 ms; 5–7 rings, 12 px apart, 60 ms lag each

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** فائق الإهليلج · squircle · superellipse · echo · morph · مربع ناعم · حلقات صدى · دائرة لمربع · circle to square · contour rings

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-levabashidze-2d713a`

#### 7. قدرات قريبة في العائلة

- `SHAPE-01` تحويل المسار بإعادة العينات / Seek-safe path morph (MOTION.morphPath) (proven)
- `SHAPE-02` قانون التحويل: نقاط متساوية واتجاه واحد / Morph law: equal points, same winding (documented)
- `SHAPE-04` تحويل بدالة قطبية / Polar-function shape morph (proven)
- `SHAPE-05` تحويل المضلعات وأشكال باوهاوس / Polygon / Bauhaus primitive morph (seen)

### `SHAPE-04` — تحويل بدالة قطبية / Polar-function shape morph

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الشكل = r(θ) = a + b·\|cos(kθ/2)\|^p؛ استوفِ a وb وk وp بين أشكال مسماة (زهرة، نجمة، squircle) مع شبكة قطبية ومعادلة حية. / Shape as r(θ)=a+b·\|cos(kθ/2)\|^p; interpolate a, b, k, p between named forms, optionally with a polar grid and a live formula label.

**متى:** حين يريد أشكالًا من معادلة قطبية تتحول بين زهرة ونجمة مع عرض المعادلة حية / when shapes from a polar equation should morph between flower, star and squircle with a live formula

**كيف:** Sample 120–240 θ steps, fill; tween k 4→8, p .5→2 with easeInOutCubic 600 ms; flower variant r = R(1 + .12 sin(8θ + t)) with design handles and a dimension tag. Rendered here (lab).

**المعاملات:** k 4→8, 120–240 samples, 600 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قطبي · polar · formula · flower · morph · math · معادلة · شكل رياضي · شبكة قطبية · polar grid · equation

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-ayushunleashed-ece3e3`
- `kosif-tool/styles/pm-ghinaiya-nirmal-5d8fec`

#### 7. قدرات قريبة في العائلة

- `SHAPE-02` قانون التحويل: نقاط متساوية واتجاه واحد / Morph law: equal points, same winding (documented)
- `SHAPE-03` فائق الإهليلج بحلقات صدى / Superellipse morph with echo rings (proven)
- `SHAPE-05` تحويل المضلعات وأشكال باوهاوس / Polygon / Bauhaus primitive morph (seen)
- `SHAPE-06` تحويل بنابض ونجوم تدور / Spring shape morph with orbiting stars (seen)

### `SHAPE-05` — تحويل المضلعات وأشكال باوهاوس / Polygon / Bauhaus primitive morph

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مربع أحمر → خماسي أصفر → مثلث، أو مثلث → سداسي، باستيفاء رؤوس المضلعات. / Red square → yellow pentagon → triangle (or triangle → hexagon) by vertex interpolation.

**متى:** حين يطلب تحول أشكال هندسية بسيطة كمربع وخماسي ومثلث بأسلوب باوهاوس / when simple primitives like a square, pentagon and triangle should morph in a Bauhaus look

**كيف:** Resample both polygons to the LCM vertex count (or 60 points), interpolate, recolour in step; 400 ms with outElastic or back.out.

**المعاملات:** 400 ms; outElastic

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مضلع · باوهاوس · polygon · bauhaus · morph · مربع · مثلث · أشكال هندسية · vertex morph · geometric shapes

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-lukasersil-0ed38e`
- `kosif-tool/styles/pm-itsuki-dev-10942d`

#### 7. قدرات قريبة في العائلة

- `SHAPE-03` فائق الإهليلج بحلقات صدى / Superellipse morph with echo rings (proven)
- `SHAPE-04` تحويل بدالة قطبية / Polar-function shape morph (proven)
- `SHAPE-06` تحويل بنابض ونجوم تدور / Spring shape morph with orbiting stars (seen)
- `SHAPE-07` تحويل بصدى ملون أو أثر ضبابي / Morph with coloured echo / blur trail (seen)

### `SHAPE-06` — تحويل بنابض ونجوم تدور / Spring shape morph with orbiting stars

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** دائرة→مربع→نجمة خماسية بمنحنى نابض، وحولها حلقة نجوم صغيرة تدور. / Circle → square → 5-point star with spring easing, a ring of small stars rotating around.

**متى:** حين يريد تحول دائرة إلى مربع ثم نجمة بحركة نابضة مع نجوم صغيرة تدور حولها / when a circle should spring into a square then a star with small stars orbiting around

**كيف:** 200-point resample; spring stiffness 180 damping 14 drives the mix; satellites on a circle rotate 1 rev/s.

**المعاملات:** 200 pts, stiffness 180, damping 14

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نابض · نجمة · spring · morph · star · نجوم تدور · حركة نابضة · دائرة لنجمة · orbiting stars · circle to star

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-roundtablespace-d3a1be`
- `kosif-tool/styles/pm-stephanlivera-df17a2`

#### 7. قدرات قريبة في العائلة

- `SHAPE-04` تحويل بدالة قطبية / Polar-function shape morph (proven)
- `SHAPE-05` تحويل المضلعات وأشكال باوهاوس / Polygon / Bauhaus primitive morph (seen)
- `SHAPE-07` تحويل بصدى ملون أو أثر ضبابي / Morph with coloured echo / blur trail (seen)
- `SHAPE-08` تحويل داخل صندوق أداة تصميم / Design-tool gizmo morph (seen)

### `SHAPE-07` — تحويل بصدى ملون أو أثر ضبابي / Morph with coloured echo / blur trail

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الشكل يتحول ويدور، وخلفه نسختان ملونتان متأخرتان أو صدى ضبابي حركي، مع مدار نقطي. / Morph while rotating with two lagged coloured stroke copies or a motion-blur echo, plus a dotted orbit.

**متى:** حين يتحول شكل وهو يدور ويحتاج نسخًا ملونة متأخرة أو أثرًا ضبابيًا خلفه / when a rotating shape morph needs lagged coloured copies or a motion-blur trail behind it

**كيف:** Draw copies at t−40 ms and t−80 ms in accent colours (stroke only) or 3–5 fading copies for blur; 600–800 ms easeInOutCubic; 3 orbit dots.

**المعاملات:** 600–800 ms; echoes at 40/80 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صدى · echo · blur trail · morph · orbit · أثر حركة · موشن بلر · نسخ ملونة · motion blur · afterimage

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-tolgayhickiran-e90799`
- `kosif-tool/styles/pm-motiondsgnr-9dcfa6`

#### 7. قدرات قريبة في العائلة

- `SHAPE-05` تحويل المضلعات وأشكال باوهاوس / Polygon / Bauhaus primitive morph (seen)
- `SHAPE-06` تحويل بنابض ونجوم تدور / Spring shape morph with orbiting stars (seen)
- `SHAPE-08` تحويل داخل صندوق أداة تصميم / Design-tool gizmo morph (seen)
- `SHAPE-09` تحويل سحابة نقاط إلى أيقونة أو شبكة / Dot-cloud morph (scatter → grid / icon) (seen)

### `SHAPE-08` — تحويل داخل صندوق أداة تصميم / Design-tool gizmo morph

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الشكل يتحول (دائرة، صدفة، نجمة) داخل صندوق تحديد رفيع بمقابض مربعة يدور، مع قراءة حية «ROT 340.9°». / Morph between shapes inside a thin rotating bounding box with square handles and a live mono readout.

**متى:** حين يُراد مشهد بطابع برامج التصميم يتحول فيه الشكل داخل صندوق تحديد بمقابض وقراءة زاوية / when a morph should look like a design app: a rotating bounding box with handles and an angle readout

**كيف:** Box stroke 1 px #aaa, 8 px square handles, Bezier handle dots; label in mono updates from the actual angle; morph 600 ms.

**المعاملات:** morph 600 ms; box 1 px #aaa

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أداة تصميم · gizmo · handles · figma · morph · صندوق تحديد · مقابض · واجهة تصميم · bounding box · design ui

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-leadnotifi-e83f94`
- `kosif-tool/styles/pm-ghinaiya-nirmal-5d8fec`

#### 7. قدرات قريبة في العائلة

- `SHAPE-06` تحويل بنابض ونجوم تدور / Spring shape morph with orbiting stars (seen)
- `SHAPE-07` تحويل بصدى ملون أو أثر ضبابي / Morph with coloured echo / blur trail (seen)
- `SHAPE-09` تحويل سحابة نقاط إلى أيقونة أو شبكة / Dot-cloud morph (scatter → grid / icon) (seen)
- `SHAPE-10` شريط ينثني فيصير حلقة / Bar bends into a ring (seen)

### `SHAPE-09` — تحويل سحابة نقاط إلى أيقونة أو شبكة / Dot-cloud morph (scatter → grid / icon)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط تبدأ عشوائية داخل شكل المصدر وتنتقل كل منها إلى موقعها في الشبكة أو الأيقونة الهدف بتأخير قطري ونابض. / N dots start scattered inside the source shape and travel to their grid cell or sampled icon point with diagonal stagger and spring easing.

**متى:** حين يريد نقاطًا متناثرة تتجمع لتكوّن شبكة أو أيقونة في إنفوجرافيك / when scattered dots should gather into a grid or an icon, e.g. in an infographic

**كيف:** Sample target shape into N points (alpha > 128 on an offscreen canvas or getPointAtLength), match by sorting both sets by angle, delay = (row+col)·25 ms; ~400 dots 0.8 s easeInOutCubic.

**المعاملات:** 10×10, 25 ms diagonal; ~400 dots, 0.8 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نقاط · dot morph · scatter · grid · icon · infographic · نقاط متناثرة · تجمع النقاط · تكوين أيقونة · dots assemble · stagger

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/infographic`
- `kosif-tool/styles/pm-manuelogomigo-f33ca9`

#### 7. قدرات قريبة في العائلة

- `SHAPE-07` تحويل بصدى ملون أو أثر ضبابي / Morph with coloured echo / blur trail (seen)
- `SHAPE-08` تحويل داخل صندوق أداة تصميم / Design-tool gizmo morph (seen)
- `SHAPE-10` شريط ينثني فيصير حلقة / Bar bends into a ring (seen)
- `SHAPE-11` رسم يدوي يصير نظيفًا / Sketch-to-clean morph (seen)

### `SHAPE-10` — شريط ينثني فيصير حلقة / Bar bends into a ring

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شريط مستقيم يُرسم كقوس ثابت الطول يقل نصف قطره من اللانهاية إلى L/2π فيصير حلقة، ثم تنقسم الحلقة إلى شرائح. / Draw the bar as a constant-length arc whose radius goes from huge to L/(2π) so it curls into a ring, then split it with cumulative dash offsets.

**متى:** حين يتحول شريط بيانات مستقيم إلى حلقة أو مخطط دائري ثم ينقسم إلى شرائح / when a straight data bar should curl into a ring or donut and then split into segments

**كيف:** Log-interpolate r; keep the arc anchored by shifting its centre; stroke width = bar height; ~1 s.

**المعاملات:** ~1 s; stroke = bar height

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شريط · حلقة · bar to ring · donut · data · مخطط دائري · رسم بياني · شرائح · ring chart · curl

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/infographic`

#### 7. قدرات قريبة في العائلة

- `SHAPE-08` تحويل داخل صندوق أداة تصميم / Design-tool gizmo morph (seen)
- `SHAPE-09` تحويل سحابة نقاط إلى أيقونة أو شبكة / Dot-cloud morph (scatter → grid / icon) (seen)
- `SHAPE-11` رسم يدوي يصير نظيفًا / Sketch-to-clean morph (seen)
- `SHAPE-12` تحول متعدد الأوجه / Facet morph (36 low-poly triangles) (install)

### `SHAPE-11` — رسم يدوي يصير نظيفًا / Sketch-to-clean morph

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خط مرتجف يُستوفى إلى مسار ناعم عند زر «تنظيف». / A jittered polyline interpolates to its smoothed path when a “clean up” button is pressed.

**متى:** حين يريد إظهار رسم يدوي مرتجف يتحول إلى خط نظيف ناعم كقبل وبعد / when a shaky hand-drawn line should turn into a clean smooth path, before/after style

**كيف:** Keep the same samples; target = Catmull-Rom of the clean control points; 500 ms.

**المعاملات:** 500 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** رسم · تنظيف · sketch · clean up · before after · خط يدوي · تنعيم · شخبطة · smoothing · hand drawn

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-adamdesgns-478d6d`

#### 7. قدرات قريبة في العائلة

- `SHAPE-09` تحويل سحابة نقاط إلى أيقونة أو شبكة / Dot-cloud morph (scatter → grid / icon) (seen)
- `SHAPE-10` شريط ينثني فيصير حلقة / Bar bends into a ring (seen)
- `SHAPE-12` تحول متعدد الأوجه / Facet morph (36 low-poly triangles) (install)
- `SHAPE-13` تحويل SVG بإضافة MorphSVG / MorphSVG plugin morph (HyperFrames rule) (documented)

### `SHAPE-12` — تحول متعدد الأوجه / Facet morph (36 low-poly triangles)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0. |

**ما هي:** كتلة لوبولي من 36 مثلثًا تتحول بين ثلاثة أشكال (كتلة، علامة، شارة) بتظليل مسطح لكل وجه. / A 36-triangle low-poly mass morphs between three silhouettes with per-facet flat shading lit from the upper left.

**متى:** حين يطلب كتلة لوبولي من مثلثات تتحول بين أشكال كعلامة أو شارة بتظليل مسطح / when a low-poly triangle mass should morph between silhouettes like a mark or badge with flat shading

**كيف:** npx hyperframes add facet-morph; vars forms="blob,mark,badge", hold_last, accent, exit none\|fade\|up; mount on a class="clip" div.

**التثبيت:** npx hyperframes add facet-morph

**الوسوم:** لوبولي · low poly · facet · morph · hyperframes · مثلثات · تظليل مسطح · شارة · flat shading · triangles

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-one/vendor/hyperframes/registry/components/facet-morph/facet-morph.html`

#### 7. قدرات قريبة في العائلة

- `SHAPE-10` شريط ينثني فيصير حلقة / Bar bends into a ring (seen)
- `SHAPE-11` رسم يدوي يصير نظيفًا / Sketch-to-clean morph (seen)
- `SHAPE-13` تحويل SVG بإضافة MorphSVG / MorphSVG plugin morph (HyperFrames rule) (documented)
- `SHAPE-14` أسلوب الأشكال السائلة / Liquid-morph style (documented)

### `SHAPE-13` — تحويل SVG بإضافة MorphSVG / MorphSVG plugin morph (HyperFrames rule)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP standard no-charge license. |

**ما هي:** قاعدة HyperFrames: حوّل الأشكال الأولية إلى مسارات وقسّم الصور الظلية المعقدة، وفضّل MorphSVGPlugin ثم تحقق بلقطة مفتاحية. / HyperFrames rule: convert primitives to paths, split complex silhouettes, prefer MorphSVGPlugin, verify with a keyframe shot.

**متى:** عند تحويل أشكال SVG داخل HyperFrames بإضافة MorphSVG مع التحقق بلقطات مفتاحية / when morphing SVG shapes in HyperFrames with the MorphSVG plugin and checking in-betweens via keyframe shots

**كيف:** gsap.registerPlugin(MorphSVGPlugin); tl.to(a,{morphSVG:b}); hyperframes keyframes --shot to check in-betweens. Outside HyperFrames prefer SHAPE-01.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** MorphSVG · gsap · morph · hyperframes · تحويل SVG · إضافة · لقطة مفتاحية · svg morph · keyframes

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-11` رسم يدوي يصير نظيفًا / Sketch-to-clean morph (seen)
- `SHAPE-12` تحول متعدد الأوجه / Facet morph (36 low-poly triangles) (install)
- `SHAPE-14` أسلوب الأشكال السائلة / Liquid-morph style (documented)
- `SHAPE-15` العنصر المشترك (FLIP) / FLIP / shared-element continuity (documented)

### `SHAPE-14` — أسلوب الأشكال السائلة / Liquid-morph style

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كتل سائلة تندمج وتنقسم: تحويل مسارات بنقاط متساوية أو فلتر لزوجة، ورؤوس تحركها ضوضاء. / Blobby fluid shapes merging and splitting via equal-point path morph or a gooey filter, vertices driven by noise.

**متى:** حين يطلب أسلوبًا سائلًا لأشكال تندمج وتنقسم كالقطرات أو انتقالًا سائلًا على الإيقاع / for a liquid style of blobby shapes merging and splitting, or a beat-anchored liquid transition

**كيف:** Scaffold: python3 tools/kosif.py scaffold liquid-morph <dir>; morph 500–800 ms at 64–128 points or SHAPE-27; beat-anchored variant: HyperFrames liquid-morph primitive (phrase/transition anchors, best span 1.0–2.5 s).

**المعاملات:** morph 500–800 ms; 64–128 pts

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سائل · liquid · blob · style · morph · قطرات · اندماج · انتقال سائل · fluid · gooey

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/liquid-morph/SKILL.md`
- `kosif-tool/styles/liquid-morph/STYLE.json`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/liquid-morph/scene.html`

#### 7. قدرات قريبة في العائلة

- `SHAPE-12` تحول متعدد الأوجه / Facet morph (36 low-poly triangles) (install)
- `SHAPE-13` تحويل SVG بإضافة MorphSVG / MorphSVG plugin morph (HyperFrames rule) (documented)
- `SHAPE-15` العنصر المشترك (FLIP) / FLIP / shared-element continuity (documented)
- `SHAPE-16` البطاقة كمرساة انتقال / Card-morph anchor handoff (documented)

### `SHAPE-15` — العنصر المشترك (FLIP) / FLIP / shared-element continuity

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أبقِ عنصرًا واحدًا حيًا وهو يغير صندوقه أو مكانه بين حالتين، فتبقى هويته متصلة بدل التلاشي المتقاطع. / Keep one element alive while it changes box or hierarchy, so identity is continuous instead of a crossfade.

**متى:** حين ينتقل عنصر واحد بين مكانين أو حجمين ويجب أن يبقى متصلًا بدل التلاشي المتقاطع / when one element changes size or place between two states and must stay continuous instead of crossfading

**كيف:** First/Last/Invert/Play: measure both boxes, apply the inverse transform, tween to identity in one continuous transform; split x/y/scale into eased keys only for deliberate beats.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** FLIP · shared element · continuity · ui · transition · انتقال سلس · تغيير الحجم · ترانزيشن · layout transition · morph

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/SKILL.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/references/keyframe-patterns.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-13` تحويل SVG بإضافة MorphSVG / MorphSVG plugin morph (HyperFrames rule) (documented)
- `SHAPE-14` أسلوب الأشكال السائلة / Liquid-morph style (documented)
- `SHAPE-16` البطاقة كمرساة انتقال / Card-morph anchor handoff (documented)
- `SHAPE-17` سلسلة: نقطة → زر → شريط تقدم / Morph chain: dot → button → progress bar → full stop (ready)

### `SHAPE-16` — البطاقة كمرساة انتقال / Card-morph anchor handoff

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حاوية تغير حجمها الظاهري (scale موحد) وزواياها وخلفيتها وظلها بين لقطتين ثم تتلاشى لتكشف الهدف الحقيقي. / A container morphs apparent size (uniform scale), radius, background and shadow between two shots, then fades to reveal the real target.

**متى:** حين تتحول بطاقة أو حاوية بين لقطتين ثم تسلّم المشهد للعنصر الحقيقي / when a card or container morphs between two shots and hands off to reveal the real target

**كيف:** One paused GSAP timeline, fromTo explicit states; MORPH_DUR power2.inOut; fades power1.in/out by fraction; transforms/opacity only.

**المعاملات:** power2.inOut

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بطاقة · card morph · handoff · ui · انتقال بطاقة · حاوية · ترانزيشن · shot transition · container

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/card-morph-anchor.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-14` أسلوب الأشكال السائلة / Liquid-morph style (documented)
- `SHAPE-15` العنصر المشترك (FLIP) / FLIP / shared-element continuity (documented)
- `SHAPE-17` سلسلة: نقطة → زر → شريط تقدم / Morph chain: dot → button → progress bar → full stop (ready)
- `SHAPE-18` جزيرة ديناميكية وزر ينفتح نافذة / Dynamic-island / button-to-window morph (seen)

### `SHAPE-17` — سلسلة: نقطة → زر → شريط تقدم / Morph chain: dot → button → progress bar → full stop

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقطة حمراء واحدة هي الخيط البصري: تسقط، تصير زرًا يُضغط، تنبسط إلى شريط تقدم، ثم تصير نقطة نهاية. / One red dot is the through-line: it falls, becomes a pill button, is pressed, flattens into a progress bar, then a full stop.

**متى:** حين يريد خيطًا بصريًا تتحول فيه نقطة إلى زر يُضغط ثم شريط تقدم ثم نقطة نهاية / when one dot should become a pressed button, then a progress bar, then a full stop

**كيف:** pill from scaleX 44/400, scaleY .44 → 1,1 in .42 s E.inOut on beat 4; after press scaleX 2.0, scaleY .24 in .34 s, swap to #bar; #fill 0→800 linear 1.1 s; counter 0→900.

**المعاملات:** 120 BPM grid; .42 s / .34 s / 1.1 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نقطة · زر · شريط تقدم · morph chain · button · progress · تحميل · عداد · ضغط زر · loading bar · through-line

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:66`

#### 7. قدرات قريبة في العائلة

- `SHAPE-15` العنصر المشترك (FLIP) / FLIP / shared-element continuity (documented)
- `SHAPE-16` البطاقة كمرساة انتقال / Card-morph anchor handoff (documented)
- `SHAPE-18` جزيرة ديناميكية وزر ينفتح نافذة / Dynamic-island / button-to-window morph (seen)
- `SHAPE-19` مؤشر مطاطي بحافتين / Two-edge stretchy indicator (seen)

### `SHAPE-18` — جزيرة ديناميكية وزر ينفتح نافذة / Dynamic-island / button-to-window morph

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حاوية واحدة تغير عرضها وارتفاعها ونصف قطرها بين الحالات بنابض: كبسولة→نافذة، بطاقة→كبسولة، دائرة→كبسولة. / One container animates width/height/radius between states on a spring: pill→window, card→pill, circle→pill with squash on settle.

**متى:** حين تتحول كبسولة إلى نافذة أو بطاقة إلى كبسولة بحركة نابضة كالجزيرة الديناميكية / when a pill expands into a window or a card shrinks to a pill on a spring, dynamic-island style

**كيف:** Spring stiffness 200 damping 22; radius 16 px → 999 px; content fades in only after 70% of the size change; ~600–800 ms easeInOutQuint if not spring.

**المعاملات:** stiffness 200, damping 22; 600–800 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** جزيرة · كبسولة · dynamic island · pill · container morph · spring · زر يتحول لنافذة · توسع · واجهة تطبيق · button expand · squash

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-jazzen-chen-4542ae`
- `kosif-tool/styles/pm-twoclipping-221cab`
- `kosif-tool/styles/pm-elliot-garreffa-f334bc`
- `kosif-tool/styles/pm-ultimaxbt-bbebf5`

#### 7. قدرات قريبة في العائلة

- `SHAPE-16` البطاقة كمرساة انتقال / Card-morph anchor handoff (documented)
- `SHAPE-17` سلسلة: نقطة → زر → شريط تقدم / Morph chain: dot → button → progress bar → full stop (ready)
- `SHAPE-19` مؤشر مطاطي بحافتين / Two-edge stretchy indicator (seen)
- `SHAPE-20` أيقونة القائمة تصير إغلاقًا / Hamburger-to-close morph (documented)

### `SHAPE-19` — مؤشر مطاطي بحافتين / Two-edge stretchy indicator

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الحافة الأمامية والخلفية لمؤشر التبويب تتبع نابضين مختلفين، فيتمدد أثناء الحركة ويستقر. / Leading and trailing edges of a tab indicator follow separate springs (leading stiffer), so it stretches in travel and settles.

**متى:** حين يحتاج مؤشر تبويبات يتمدد أثناء انتقاله بين التبويبات ثم يستقر / when a tab indicator should stretch while sliding between tabs and then settle

**كيف:** Two springs on left/right edges; stiffness ratio ~1.6:1; draw a rounded rect between them.

**المعاملات:** stiffness ratio ~1.6:1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مؤشر · tab indicator · stretchy · spring · ui · تبويبات · مؤشر مطاطي · خط تحت التبويب · tabs · elastic

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-twoclipping-5cba86`

#### 7. قدرات قريبة في العائلة

- `SHAPE-17` سلسلة: نقطة → زر → شريط تقدم / Morph chain: dot → button → progress bar → full stop (ready)
- `SHAPE-18` جزيرة ديناميكية وزر ينفتح نافذة / Dynamic-island / button-to-window morph (seen)
- `SHAPE-20` أيقونة القائمة تصير إغلاقًا / Hamburger-to-close morph (documented)
- `SHAPE-21` التحول عبر حالات الواجهة / Morph through UI states (documented)

### `SHAPE-20` — أيقونة القائمة تصير إغلاقًا / Hamburger-to-close morph

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاثة خطوط تصير X: العلوي والسفلي يدوران ±45° والأوسط ينطوي. / Three bars become an X: top/bottom rotate ±45°, the middle collapses.

**متى:** حين يطلب تحويل أيقونة القائمة ذات الخطوط الثلاثة إلى علامة إغلاق X / when the three-line menu icon should turn into an X close icon

**كيف:** Transforms on three spans; middle opacity 0 + scaleX 0; 0.2 s.

**المعاملات:** ±45°, 0.2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قائمة · hamburger · close · icon morph · ui · ثلاث شرط · إغلاق · زر القائمة · menu icon · x icon

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-atlas/skills/3529-ui-design/14308-interaction-design/references/microinteraction-patterns.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-18` جزيرة ديناميكية وزر ينفتح نافذة / Dynamic-island / button-to-window morph (seen)
- `SHAPE-19` مؤشر مطاطي بحافتين / Two-edge stretchy indicator (seen)
- `SHAPE-21` التحول عبر حالات الواجهة / Morph through UI states (documented)
- `SHAPE-22` نقطة تتفتح إلى واجهة أو نظام / Dot-to-interface / dot-to-system bloom (seen)

### `SHAPE-21` — التحول عبر حالات الواجهة / Morph through UI states

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** زر → مفتاح → بطاقة → شاشة كاملة، كل خطوة 600 ms ووقفة 900 ms للقراءة. / Button → toggle → card → full screen, 600 ms per step with 900 ms holds.

**متى:** حين يريد عرض تحول عنصر واحد عبر حالات واجهة متتابعة من زر إلى شاشة كاملة / when one element should morph through successive UI states from a button to a full screen

**كيف:** Each step is a SHAPE-15 on the same element; hold 900 ms so the eye reads the state.

**المعاملات:** 600 ms per step; 900 ms holds

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حالات · ui states · morph · flow · زر · شاشة كاملة · تدفق الواجهة · button to fullscreen · toggle

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/playbooks/shapes.md:49`

#### 7. قدرات قريبة في العائلة

- `SHAPE-19` مؤشر مطاطي بحافتين / Two-edge stretchy indicator (seen)
- `SHAPE-20` أيقونة القائمة تصير إغلاقًا / Hamburger-to-close morph (documented)
- `SHAPE-22` نقطة تتفتح إلى واجهة أو نظام / Dot-to-interface / dot-to-system bloom (seen)
- `SHAPE-23` حلقة → قزحية → غمر لوني / Ring → iris → colour flood (ready)

### `SHAPE-22` — نقطة تتفتح إلى واجهة أو نظام / Dot-to-interface / dot-to-system bloom

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقطة متوهجة 8px تكبر إلى إطار مستطيل في 1.2 ث (expo) ثم يظهر المحتوى، أو تطلق حلقات وأقمارًا متتابعة. / A glowing 8 px dot scales to a rectangular frame in 1.2 s (expo) then content fades in — or emits rings and satellite dots with 50 ms stagger.

**متى:** حين تبدأ الواجهة أو النظام من نقطة متوهجة تكبر إلى إطار يظهر فيه المحتوى / when an interface or system should bloom from a glowing dot into a frame as content fades in

**كيف:** Animate width/height/radius from the dot; content opacity after 80%; system variant: rings scale from the dot and satellites scatter with 50 ms stagger over ~1 s.

**المعاملات:** 8 px → frame, 1.2 s expo; satellites 50 ms stagger

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نقطة · تفتح · dot bloom · interface · reveal · نقطة متوهجة · كشف الواجهة · أقمار · glowing dot · satellites

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-dale-vaz-cc612a`
- `kosif-tool/styles/pm-xelandre-363f00`

#### 7. قدرات قريبة في العائلة

- `SHAPE-20` أيقونة القائمة تصير إغلاقًا / Hamburger-to-close morph (documented)
- `SHAPE-21` التحول عبر حالات الواجهة / Morph through UI states (documented)
- `SHAPE-23` حلقة → قزحية → غمر لوني / Ring → iris → colour flood (ready)
- `SHAPE-24` الشعار يصير بؤبؤ عين / Logo-to-iris / eye opening (seen)

### `SHAPE-23` — حلقة → قزحية → غمر لوني / Ring → iris → colour flood

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حلقة مرسومة تنكمش وتسمك إلى نقطة قزحية، ثم تنفتح دائرة قص من تلك النقطة لتغمر الإطار بلون العلامة. / A drawn ring shrinks and thickens into an iris point, then a circular clip opens from it to flood the frame with the brand colour.

**متى:** حين يريد انتقالًا تنكمش فيه حلقة إلى نقطة ثم تنفتح دائرة تغمر الكادر بلون العلامة / for a transition where a ring shrinks to a point and a circular iris floods the frame with the brand colour

**كيف:** tl.to(ring,{scale:.14, strokeWidth:60, duration:.45, ease:E.in}, 3.65); M.iris(tl, brand, 4.05, {x:540, y:930, r0:60, r:2300, dur:.5}) with log-space ease + M.flash peak .6.

**المعاملات:** .45 s shrink; iris r 60→2300 in .5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قزحية · iris · flood · ring · brand · transition · انتقال دائري · غمر لوني · لون البراند · circle wipe · iris wipe

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:80`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:334`

#### 7. قدرات قريبة في العائلة

- `SHAPE-21` التحول عبر حالات الواجهة / Morph through UI states (documented)
- `SHAPE-22` نقطة تتفتح إلى واجهة أو نظام / Dot-to-interface / dot-to-system bloom (seen)
- `SHAPE-24` الشعار يصير بؤبؤ عين / Logo-to-iris / eye opening (seen)
- `SHAPE-25` نقرة وتحول لعلامة صح / Tap ripple + circle-to-check morph (idea)

### `SHAPE-24` — الشعار يصير بؤبؤ عين / Logo-to-iris / eye opening

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حلقة الشعار تكبر إلى قرص قزحية بتدرج شعاعي، ويُرسم حولها جفن لوزي برموش، أو عين تنفتح من خط. / The logo ring scales into an iris disc with a radial ray gradient inside an almond eye outline with lash ticks; or an eye opens from a line.

**متى:** حين يتحول الشعار إلى بؤبؤ عين داخل جفن لوزي أو تنفتح عين من خط / when a logo ring should become an eye's iris inside an almond outline, or an eye opens from a line

**كيف:** Almond path height 0→full 800 ms ease-out with iris scale; iris glow blur 30–40 px #5cc8ff; concentric outlines behind.

**المعاملات:** ~600–800 ms; glow 30–40 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عين · قزحية · eye · iris · logo morph · بؤبؤ · لوجو · فتح العين · eye open · radial gradient

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-micheleharmonic-77628e`
- `kosif-tool/styles/pm-monokern-ade5b6`

#### 7. قدرات قريبة في العائلة

- `SHAPE-22` نقطة تتفتح إلى واجهة أو نظام / Dot-to-interface / dot-to-system bloom (seen)
- `SHAPE-23` حلقة → قزحية → غمر لوني / Ring → iris → colour flood (ready)
- `SHAPE-25` نقرة وتحول لعلامة صح / Tap ripple + circle-to-check morph (idea)
- `SHAPE-26` ظرف يتحول لشارة / تجمع إلى شعار / Envelope→badge, converge→monogram, collapse→dot (idea)

### `SHAPE-25` — نقرة وتحول لعلامة صح / Tap ripple + circle-to-check morph

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقرة تطلق تموجًا، والدائرة تتحول إلى علامة صح. / A tap ripple triggers success; the circle morphs into a checkmark.

**متى:** حين يريد إظهار نجاح عملية بنقرة تموج ودائرة تتحول إلى علامة صح / when a tap ripple should confirm success as a circle morphs into a checkmark

**كيف:** Untested idea from a brief: SHAPE-01 circle→check (open path) + ripple circle scale 1→1.9 fading .9→0 in .9 s; ~400 ms.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صح · check · success · ripple · morph · تأكيد · نقرة · تم بنجاح · checkmark · tap

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-cansincengiz-me-cf68dd/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-23` حلقة → قزحية → غمر لوني / Ring → iris → colour flood (ready)
- `SHAPE-24` الشعار يصير بؤبؤ عين / Logo-to-iris / eye opening (seen)
- `SHAPE-26` ظرف يتحول لشارة / تجمع إلى شعار / Envelope→badge, converge→monogram, collapse→dot (idea)
- `SHAPE-27` فلتر اللزوجة / SVG goo / metaball filter (proven)

### `SHAPE-26` — ظرف يتحول لشارة / تجمع إلى شعار / Envelope→badge, converge→monogram, collapse→dot

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أفكار من البريفات: ظرف مُرسل ينطلق ويصير شارة إشعار؛ خطوط تتجمع إلى مربع يدور 90° فيصير مونوغرام؛ كل العناصر تنكمش إلى نقطة تنفتح شعارًا. / Brief ideas: a sent envelope streaks off and becomes a badge; lanes converge into a tile that rotates 90° into a monogram; everything collapses to a dot that opens into the logo.

**متى:** حين يحتاج ختامًا تتجمع فيه العناصر إلى شعار أو مونوغرام أو يتحول ظرف مرسل إلى شارة إشعار / for an outro where elements converge into a logo or monogram, or a sent envelope becomes a badge

**كيف:** Untested: transform interpolation + SHAPE-01; hold the final logo 2 s.

**المعاملات:** 90° turn; hold 2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شعار · outro · monogram · badge · converge · ختام · لوجو · ظرف · إشعار · envelope · notification

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-melvynx-6cde6c/BRIEF.md`
- `kosif-tool/styles/pm-danilowm-d3720d/BRIEF.md`
- `kosif-tool/styles/pm-itisrazak-3ad902/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-24` الشعار يصير بؤبؤ عين / Logo-to-iris / eye opening (seen)
- `SHAPE-25` نقرة وتحول لعلامة صح / Tap ripple + circle-to-check morph (idea)
- `SHAPE-27` فلتر اللزوجة / SVG goo / metaball filter (proven)
- `SHAPE-28` الانقسام اللزج والكتلة الناعمة / Gooey split & soft blob touch (HyperFrames) (install)

### `SHAPE-27` — فلتر اللزوجة / SVG goo / metaball filter

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كرات تندمج كالسائل: تمويه ثم شحذ قناة الألفا بمصفوفة لون. / Blobs merge like liquid: blur then sharpen alpha with a colour matrix.

**متى:** حين يريد كرات أو دوائر تلتحم كالسائل بفلتر SVG لزج / when blobs or circles should merge like liquid using an SVG goo filter

**كيف:** <filter><feGaussianBlur stdDeviation=10/><feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 18 -7"/></filter> on a <g> of circles moved in seek(t). Rendered here (4 orbiting circles). Keep text outside the filter. Canvas alternative: sum r²/d² field and threshold.

**المعاملات:** stdDeviation 10; alpha row 18 −7

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** لزوجة · goo · metaball · blob · svg filter · liquid · سائل · التحام · كرات · gaussian blur · merge

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-atlas/skills/100-ui-motion/209-kinetic-inflated-hero`
- `kosif-tool/styles/pm-raphaelaubryy-4b137e`

#### 7. قدرات قريبة في العائلة

- `SHAPE-25` نقرة وتحول لعلامة صح / Tap ripple + circle-to-check morph (idea)
- `SHAPE-26` ظرف يتحول لشارة / تجمع إلى شعار / Envelope→badge, converge→monogram, collapse→dot (idea)
- `SHAPE-28` الانقسام اللزج والكتلة الناعمة / Gooey split & soft blob touch (HyperFrames) (install)
- `SHAPE-29` تجمع الصلصال بالكرات / Metaball clay assembly (idea)

### `SHAPE-28` — الانقسام اللزج والكتلة الناعمة / Gooey split & soft blob touch (HyperFrames)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 (+ GSAP standard license inside). |

**ما هي:** نقطة تنقسم إلى قائمة ثلاث نقاط عبر عنق لزج ثم تدور وتلتحم؛ وكتلة محببة تنتفخ نحو نقطة لمس وتعود بنابض يحفظ السرعة. / A dot splits into a three-dot menu through a metaball neck, spins and re-merges; a grainy blob bulges toward a touch and recovers on a velocity-preserving spring.

**متى:** حين تنقسم نقطة إلى قائمة ثلاث نقاط بعنق لزج أو تنتفخ كتلة نحو نقطة لمس في HyperFrames / when a dot splits into a three-dot menu via a gooey neck, or a blob bulges toward a touch, in HyperFrames

**كيف:** npx hyperframes add gooey-split (4.7 s, SVG blur+threshold, GSAP paused timeline) \| soft-blob-touch (touch_x 8–92, touch_y 8–92, touch_at .9–10 s, grain fine\|coarse).

**المعاملات:** gooey-split 4.7 s; touch_at 1.6 s default

**التثبيت:** npx hyperframes add gooey-split

**الوسوم:** لزج · gooey · blob · touch · hyperframes · انقسام · لمسة · ثلاث نقاط · split · metaball

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

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-one/vendor/hyperframes/registry/blocks/gooey-split/gooey-split.html`
- `kosif-one/vendor/hyperframes/registry/components/soft-blob-touch/soft-blob-touch.html`

#### 7. قدرات قريبة في العائلة

- `SHAPE-26` ظرف يتحول لشارة / تجمع إلى شعار / Envelope→badge, converge→monogram, collapse→dot (idea)
- `SHAPE-27` فلتر اللزوجة / SVG goo / metaball filter (proven)
- `SHAPE-29` تجمع الصلصال بالكرات / Metaball clay assembly (idea)
- `SHAPE-30` كتلة عضوية بضوضاء الرؤوس / Noise-displaced 3D blob (install)

### `SHAPE-29` — تجمع الصلصال بالكرات / Metaball clay assembly

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ست كتل تتدحرج وتلتحم بعتبة الكرات المعدنية. / Six blobs roll in and merge via a metaball threshold.

**متى:** حين يريد مشهد كتل كالصلصال تتدحرج وتلتحم معًا / when clay-like blobs should roll in and merge together

**كيف:** Untested idea from a brief: Canvas field sum Σr²/d² + threshold (or SHAPE-27); roll = translate + rotate of a texture inside each blob.

**المعاملات:** 6 blobs

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صلصال · metaball · clay · merge · كتل · التحام · تدحرج · roll in · blobs

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-davidshulmanfl-371638/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-27` فلتر اللزوجة / SVG goo / metaball filter (proven)
- `SHAPE-28` الانقسام اللزج والكتلة الناعمة / Gooey split & soft blob touch (HyperFrames) (install)
- `SHAPE-30` كتلة عضوية بضوضاء الرؤوس / Noise-displaced 3D blob (install)
- `SHAPE-31` أشكال بدوال المسافة / 2D signed-distance shapes (union, morph, glow) (documented)

### `SHAPE-30` — كتلة عضوية بضوضاء الرؤوس / Noise-displaced 3D blob

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كرة تُدفع رؤوسها على العموديات بضوضاء متحركة فتصير كتلة حية. / Sphere vertices pushed along normals by animated noise — a living blob.

**متى:** حين يريد كرة ثلاثية الأبعاد تتموج كأنها كتلة عضوية حية / when a 3D sphere should ripple into a living organic blob

**كيف:** three.js ShaderMaterial vertex: disp = pnoise(position·1.5 + t·.5); newPos = position + normal·disp·intensity; t = seek time (never clock). Or use the bundled three-kit noise on CPU for small meshes.

**المعاملات:** freq 1.5, speed .5, intensity .1–.3

**التثبيت:** npm i three

**الوسوم:** كتلة · blob · noise · vertex shader · three.js · ثلاثي الأبعاد · كرة · عضوي · 3d sphere · organic

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-28` الانقسام اللزج والكتلة الناعمة / Gooey split & soft blob touch (HyperFrames) (install)
- `SHAPE-29` تجمع الصلصال بالكرات / Metaball clay assembly (idea)
- `SHAPE-31` أشكال بدوال المسافة / 2D signed-distance shapes (union, morph, glow) (documented)
- `SHAPE-32` نحت بحقول المسافة إلى مجسم مغلق / SDF sculpting to a watertight mesh (proven)

### `SHAPE-31` — أشكال بدوال المسافة / 2D signed-distance shapes (union, morph, glow)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صف الأشكال كدوال مسافة: دمج ناعم، تحويل بالمزج بين دالتين، حدود وتوهج من المسافة نفسها. / Shapes as distance functions for smooth unions, morphs (mix two SDFs), outlines and glows.

**متى:** حين يرسم أشكالًا بالشيدر تحتاج دمجًا ناعمًا أو تحويلًا أو حدودًا وتوهجًا / when shader-drawn shapes need smooth unions, morphs, outlines or glows from distance functions

**كيف:** GLSL or numpy: circle length(p)−r, box, smooth-min union with k; morph = mix(d1, d2, t); outline = abs(d) < w; glow = exp(−d·k); debug with isolines. Inverse-transform the point, never the shape.

**المعاملات:** smin k .1–.3

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** دوال المسافة · SDF · smooth min · glow · shader · شيدر · توهج · حدود · glsl · outline · distance field

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:numpy` ← python3 -c "import numpy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-atlas/skills/2199-lvtd-skills/8087-game-sdf-and-field-modeling/SKILL.md`
- `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-29` تجمع الصلصال بالكرات / Metaball clay assembly (idea)
- `SHAPE-30` كتلة عضوية بضوضاء الرؤوس / Noise-displaced 3D blob (install)
- `SHAPE-32` نحت بحقول المسافة إلى مجسم مغلق / SDF sculpting to a watertight mesh (proven)
- `SHAPE-33` دمج ونحت وتقاطع ناعم / Smooth CSG (add / sub / and) (proven)

### `SHAPE-32` — نحت بحقول المسافة إلى مجسم مغلق / SDF sculpting to a watertight mesh

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شخصيات وأجسام تُنحت من أوليات مسافة (كرة، إهليلج، كبسولة، صندوق، طارة) بدمج ونحت ناعم، وتُشبَّك إلى هندسة مغلقة دقيقة. / Characters and props sculpted from SDF primitives with smooth union/subtract and meshed by surface nets into closed, accurate geometry.

**متى:** حين يريد نحت شخصية أو مجسم من أوليات كالكرة والكبسولة والصندوق إلى شبكة مغلقة دقيقة / when sculpting a character or prop from sphere, capsule and box primitives into a closed accurate mesh

**كيف:** K3S.sculpt().color(hex).sphere(c,r,o).ellipsoid(c,[rx,ry,rz],o).capsule(a,b,r1,r2,o).box(c,[hx,hy,hz],round,o).torus(c,R,r,o).mesh({cells}); o = {k, op, color, rot}. Coarse-to-fine evaluation skips empty space. test_shape_kit passed here 4/4.

**المعاملات:** sphere volume ±2%, area ±3%, radius error < 1e−3, 0 open edges; evals < 60% of full grid; 136-cell body ~1.5 s; bunny 274k tris ~4 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نحت · SDF · sculpt · mesh · surface nets · character · 3d · مجسم · شخصية ثلاثية · كبسولة · watertight · primitives

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `100-superskills/skills/kosif-montage-motion/tests/test_shape_kit.py:21`
- `100-superskills/skills/kosif-montage-motion/tests/js/shape_kit_check.cjs:31`
- `kosif-studio/motion/kit/shape-kit.js:44`
- `kosif-studio/motion/references/shape-kit.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-30` كتلة عضوية بضوضاء الرؤوس / Noise-displaced 3D blob (install)
- `SHAPE-31` أشكال بدوال المسافة / 2D signed-distance shapes (union, morph, glow) (documented)
- `SHAPE-33` دمج ونحت وتقاطع ناعم / Smooth CSG (add / sub / and) (proven)
- `SHAPE-34` استعلام الحقل لتثبيت العناصر / Field queries for placement (ready)

### `SHAPE-33` — دمج ونحت وتقاطع ناعم / Smooth CSG (add / sub / and)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** دمج وطرح وتقاطع ناعم بنصف قطر k بالمتر، والألوان تمتزج بنفس الأوزان، والطرح الملون يلون التجويف. / Smooth union, subtraction and intersection with blend radius k in metres; colours blend with the same weights; a coloured subtraction tints the cavity.

**متى:** عند دمج أو طرح أو تقاطع أشكال مجسمة بحواف ناعمة مع مزج الألوان أو تلوين التجويف / when smoothly adding, carving or intersecting primitives with blended colours or a tinted cavity

**كيف:** Pass {op:"add"\|"sub"\|"and", k, color} to any primitive; h = clamp(.5 ± .5·(d2−d1)/k); d = mix − k·h·(1−h). Tested here (tint red 1.0 inside the carve, 0 on the plain side).

**المعاملات:** k 10–30 mm for plush (e.g. .012 m)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** دمج ناعم · CSG · smooth union · subtract · sdf · طرح · تقاطع · تجويف · intersection · blend radius

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:104`
- `100-superskills/skills/kosif-montage-motion/tests/test_shape_kit.py:31`
- `kosif-studio/motion/kit/shape-kit.js:100`

#### 7. قدرات قريبة في العائلة

- `SHAPE-31` أشكال بدوال المسافة / 2D signed-distance shapes (union, morph, glow) (documented)
- `SHAPE-32` نحت بحقول المسافة إلى مجسم مغلق / SDF sculpting to a watertight mesh (proven)
- `SHAPE-34` استعلام الحقل لتثبيت العناصر / Field queries for placement (ready)
- `SHAPE-35` حقل كتل وبقعة زاوية / Drifting blob field & corner blob (ready)

### `SHAPE-34` — استعلام الحقل لتثبيت العناصر / Field queries for placement

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اسأل الحقل عن المسافة واللون، أسقط نقطة على السطح، أو اطلق شعاعًا — مثلًا لتثبيت العيون حيث يلتقي شعاع أمامي بالوجه. / Query distance/colour, project points onto the surface or raycast it — e.g. seat eyes where a frontal ray meets the face.

**متى:** حين يحتاج تثبيت عناصر كالعيون على سطح مجسم بإسقاط النقاط أو إطلاق شعاع / when seating accessories like eyes on a sculpted surface by projecting points or raycasting

**كيف:** S.dist(x,y,z), S.colorAt(...), S.project(p), S.hit(from, dir) → {point, normal}; orient the accessory to the returned normal.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** استعلام · raycast · placement · sdf · eyes · تثبيت · عيون · إسقاط على السطح · surface normal · project point

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-studio/motion/kit/shape-kit.js:104`
- `kosif-studio/motion/references/shape-kit.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-32` نحت بحقول المسافة إلى مجسم مغلق / SDF sculpting to a watertight mesh (proven)
- `SHAPE-33` دمج ونحت وتقاطع ناعم / Smooth CSG (add / sub / and) (proven)
- `SHAPE-35` حقل كتل وبقعة زاوية / Drifting blob field & corner blob (ready)
- `SHAPE-36` كتلة متدرجة أو متحولة خلف النص / Gradient / morphing blob behind text (seen)

### `SHAPE-35` — حقل كتل وبقعة زاوية / Drifting blob field & corner blob

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 5–8 أشكال كبيرة مستديرة تنجرف مموهة خلف المحتوى، أو بقعة إهليلجية كبيرة تنزف من الزاوية العليا اليمنى. / 5–8 large rounded shapes drifting with blur behind content, or one large tinted ellipse bleeding off the top-right corner.

**متى:** حين يريد خلفية هادئة من كتل مستديرة مموهة تنجرف أو بقعة لونية تخرج من الزاوية / for a calm background of blurred rounded shapes drifting, or a tinted blob bleeding off a corner

**كيف:** Corner blob: ellipse centre (.93w,.14h), radii .35w×.13h, rotation π/5, alpha .65 (fastify editorial). Field: periods 10/12/16 s so shapes never move in lockstep, drift 12–30 px, rotate 5–8°.

**المعاملات:** corner ellipse .35w×.13h @ .65; drift 12–30 px, periods 10/12/16 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كتل · blob · background · drift · ambient · خلفية متحركة · بقعة · تمويه · corner blob · soft shapes

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `fastify-motion-bro/web/editorial.js:50-51`
- `kosif-atlas/skills/196-landing/621-landing/references/gsap_animation_patterns.md`
- `kosif-tool/styles/pm-slvdev-64c45a`

#### 7. قدرات قريبة في العائلة

- `SHAPE-33` دمج ونحت وتقاطع ناعم / Smooth CSG (add / sub / and) (proven)
- `SHAPE-34` استعلام الحقل لتثبيت العناصر / Field queries for placement (ready)
- `SHAPE-36` كتلة متدرجة أو متحولة خلف النص / Gradient / morphing blob behind text (seen)
- `SHAPE-37` إطار مطاطي وقناع قضمة / Rubber-frame strain & bite mask (seen)

### `SHAPE-36` — كتلة متدرجة أو متحولة خلف النص / Gradient / morphing blob behind text

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كتلة SVG تتحول بالضوضاء بتدرج ليموني→أزرق والنص فوقها بمزج multiply، أو مربع يصير كتلة بحد فوق نقاط هالفتون. / Noise-morphing SVG blob with a lime→blue gradient and multiplied text, or a square morphing to a blob with an outline over halftone dots.

**متى:** حين يحتاج كتلة متدرجة الألوان تتحول بالضوضاء خلف عنوان أو نص / when a noise-morphing gradient blob should sit behind a headline or text

**كيف:** Path from 12–16 polar points with radius = R(1 + .15·noise(θ, t)); Catmull-Rom closed; 600 ms morph for the square variant.

**المعاملات:** 600 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كتلة · نص · blob · text · gradient · تدرج · خلفية النص · هالفتون · multiply · halftone

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-sudo-kiran-49176d`
- `kosif-tool/styles/pm-hanifproduktif-54bdee`

#### 7. قدرات قريبة في العائلة

- `SHAPE-34` استعلام الحقل لتثبيت العناصر / Field queries for placement (ready)
- `SHAPE-35` حقل كتل وبقعة زاوية / Drifting blob field & corner blob (ready)
- `SHAPE-37` إطار مطاطي وقناع قضمة / Rubber-frame strain & bite mask (seen)
- `SHAPE-38` تموج ضغطة بحرارة / Press ripple with heat bloom (documented)

### `SHAPE-37` — إطار مطاطي وقناع قضمة / Rubber-frame strain & bite mask

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حد الإطار مسار من ~40 نقطة ينبعج حيث يضغط المحتوى؛ وقناع «قضمة» من اتحاد ثلاث دوائر يُطرح من حافة الجسم مع فتات. / The frame border as a ~40-point path bulging where content pushes; a scalloped three-circle “bite” subtracted from an edge with crumbs.

**متى:** حين يريد إطارًا مطاطيًا ينبعج تحت ضغط المحتوى أو قضمة تُقتطع من حافة شكل مع فتات / when a frame border should bulge under content, or a bite should be cut from an edge with crumbs

**كيف:** Displace border points by noise/sine where touched, amp 0→12 px, 3–4 waves per edge; bite: mask radius 0→r in 200 ms + 4–6 crumb particles.

**المعاملات:** amp 0→12 px; bite 200 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مطاطي · قضمة · rubber · bite · mask · انبعاج · فتات · حافة · bulge · crumbs

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-pankajkumar-dev-0bee87`
- `kosif-tool/styles/pm-thilina-a-891c09`

#### 7. قدرات قريبة في العائلة

- `SHAPE-35` حقل كتل وبقعة زاوية / Drifting blob field & corner blob (ready)
- `SHAPE-36` كتلة متدرجة أو متحولة خلف النص / Gradient / morphing blob behind text (seen)
- `SHAPE-38` تموج ضغطة بحرارة / Press ripple with heat bloom (documented)
- `SHAPE-39` الحركة على مسار SVG / Motion along an SVG path (install)

### `SHAPE-38` — تموج ضغطة بحرارة / Press ripple with heat bloom

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حلقة تتسع وتدفع الإحداثيات للخارج وتضيف «حرارة» لونية. / An expanding ring that shoves coordinates outward and adds heat.

**متى:** حين يريد ضغطة يتسع منها تموج يدفع الصورة للخارج مع توهج دافئ / when a press should send out an expanding ripple that warps outward with a warm heat bloom

**كيف:** Ring radius grows over .9 s; displacement .18 in a shader or canvas warp; heat .55 added as warm bloom on the ring.

**المعاملات:** ripple .18, heat .55, .9 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تموج · ripple · press · heat · touch · ضغطة · توهج · تشويه · warp · bloom

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

#### 7. قدرات قريبة في العائلة

- `SHAPE-36` كتلة متدرجة أو متحولة خلف النص / Gradient / morphing blob behind text (seen)
- `SHAPE-37` إطار مطاطي وقناع قضمة / Rubber-frame strain & bite mask (seen)
- `SHAPE-39` الحركة على مسار SVG / Motion along an SVG path (install)
- `SHAPE-40` اختيار المنحنى وسرعة ثابتة / Spline choice + arc-length constant speed (documented)

### `SHAPE-39` — الحركة على مسار SVG / Motion along an SVG path

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP standard no-charge license (not MIT). |

**ما هي:** عنصر (طائرة، سهم، مذنب، نص) يتحرك على مسار ويدور مع مماسه. / Move an element (plane, arrow, comet, label) along a path with auto-rotation to the tangent.

**متى:** حين يتحرك عنصر كطائرة أو سهم أو نص على مسار ويدور مع اتجاهه / when an element like a plane, arrow or label should travel along a path and turn with it

**كيف:** gsap.registerPlugin(MotionPathPlugin); tl.to(el,{motionPath:{path:"#route", align:"#route", autoRotate:true}, duration:2, ease:"power1.inOut"}); pair with a dashoffset draw of the same path. Plugin-free: sample SVGPathElement.getPointAtLength(L·p) and atan2 of a nearby point. Text: SVG <textPath> shapes Arabic correctly in Chromium.

**المعاملات:** 1.5–2 s power2.out / power1.inOut

**التثبيت:** npm i gsap

**الوسوم:** مسار · motion path · autoRotate · textPath · route · gsap · طائرة · سهم · خط سير · path follow · plane

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/techniques.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-37` إطار مطاطي وقناع قضمة / Rubber-frame strain & bite mask (seen)
- `SHAPE-38` تموج ضغطة بحرارة / Press ripple with heat bloom (documented)
- `SHAPE-40` اختيار المنحنى وسرعة ثابتة / Spline choice + arc-length constant speed (documented)
- `SHAPE-41` محلل لغة مسارات SVG كاملة / Full SVG path parser (Studio) (proven)

### `SHAPE-40` — اختيار المنحنى وسرعة ثابتة / Spline choice + arc-length constant speed

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** Catmull-Rom ليمر بالنقاط، Hermite لمماسات معروفة، Bezier للمقابض؛ استهدف استمرارية C1 وجدول طول قوس لسرعة ثابتة. / Catmull-Rom through waypoints, Hermite with known tangents, Bezier for handles; target C1 and use an arc-length table for constant speed.

**متى:** عند اختيار نوع المنحنى لحركة تمر بنقاط محددة أو لضبط سرعة ثابتة على المسار / when picking a spline through waypoints or getting constant speed along a curve

**كيف:** Sample the curve, build cumulative length, map distance→t by binary search; keep authoring points separate from baked samples; never one high-degree polynomial through many points.

**المعاملات:** C0 position, C1 tangent, C2 curvature

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** منحنى · spline · catmull-rom · arc length · constant speed · سرعة ثابتة · نقاط مرور · بيزييه · bezier · hermite · waypoints

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-atlas/skills/2199-lvtd-skills/8088-game-smooth-curves-and-motion`

#### 7. قدرات قريبة في العائلة

- `SHAPE-38` تموج ضغطة بحرارة / Press ripple with heat bloom (documented)
- `SHAPE-39` الحركة على مسار SVG / Motion along an SVG path (install)
- `SHAPE-41` محلل لغة مسارات SVG كاملة / Full SVG path parser (Studio) (proven)
- `SHAPE-42` أشكال مركبة بثقوب / Even-odd compound shapes & holes (proven)

### `SHAPE-41` — محلل لغة مسارات SVG كاملة / Full SVG path parser (Studio)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يحلل M L H V C S Q T A Z مطلقة ونسبية مع الانعكاسات وأعلام الأقواس الملتصقة إلى مضلعات. / Parses M L H V C S Q T A Z (absolute/relative, smooth reflections, glued arc flags) into polygons, arcs by SVG centre parameterisation.

**متى:** حين يحتاج تحويل بيانات مسار SVG بكل أوامرها وأقواسها إلى مضلعات للرسم / when converting SVG path data with all commands and arcs into polygons to draw

**كيف:** render.path("M … Z", n=14) → one polygon per subpath; arcs sample max(4, \|dθ\|/2π·64) points. test_path_arcs_and_smooth_curves_end_where_they_should passed here.

**المعاملات:** 14 samples per Bezier segment

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مسار · svg path · parser · arc · studio · تحليل المسار · مضلعات · أوامر المسار · path data · bezier

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-studio/render.py:87`
- `kosif-studio/render.py:192`
- `kosif-studio/tests/test_studio.py:55`

#### 7. قدرات قريبة في العائلة

- `SHAPE-39` الحركة على مسار SVG / Motion along an SVG path (install)
- `SHAPE-40` اختيار المنحنى وسرعة ثابتة / Spline choice + arc-length constant speed (documented)
- `SHAPE-42` أشكال مركبة بثقوب / Even-odd compound shapes & holes (proven)
- `SHAPE-43` عدة الأشكال الأساسية ولغة المشهد / Basic shape kit & Step scene language (proven)

### `SHAPE-42` — أشكال مركبة بثقوب / Even-odd compound shapes & holes

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حلقات وحروف بفراغات وشعارات مقصوصة: مسارات فرعية مجسورة بمرساة واحدة فيلغي ملء even-odd الجسور، أو مضلعات Hole تمحو. / Rings, letters with counters, logo cut-outs: subpaths bridged to one anchor so even-odd fill cancels the bridges, or Hole polygons that erase.

**متى:** حين يرسم حلقة أو حرفًا مفرغًا أو شعارًا مقصوصًا يحتاج ثقوبًا داخلية / when drawing rings, letters with counters or logo cut-outs that need inner holes

**كيف:** render.compound(polys); render.Hole([...]) drawn after the shape it cuts; to_python._bridge for Pillow programs. In 2.5D extrusion, a reversed inner subpath shows the hole walls automatically. Tests test_holes_cut_out + test_even_odd_compound passed here.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ثقوب · even-odd · compound · hole · logo · فراغات · قص · حروف مفرغة · cut-out · counters

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-studio/render.py:25`
- `kosif-studio/render.py:229`
- `kosif-studio/to_python.py:80`
- `kosif-studio/tests/test_studio.py:42`

#### 7. قدرات قريبة في العائلة

- `SHAPE-40` اختيار المنحنى وسرعة ثابتة / Spline choice + arc-length constant speed (documented)
- `SHAPE-41` محلل لغة مسارات SVG كاملة / Full SVG path parser (Studio) (proven)
- `SHAPE-43` عدة الأشكال الأساسية ولغة المشهد / Basic shape kit & Step scene language (proven)
- `SHAPE-44` منحنيات كاتمول-روم / Catmull-Rom smooth curves (ready)

### `SHAPE-43` — عدة الأشكال الأساسية ولغة المشهد / Basic shape kit & Step scene language

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الصورة برنامج من خطوات: rect, ellipse(rot), poly, path, compound/Hole, tube, dots, stroke, catmull, translate, union مع تدرجات وضوء، تُرسم بأي حجم. / A picture as an ordered program of Steps over vector primitives, gradients and light, re-rendered at any size on a 1200×800 sheet.

**متى:** حين يريد بناء صورة متجهة كبرنامج خطوات من أشكال أولية تُرسم بأي حجم وبترتيب كشف / when building a vector picture as ordered steps of primitives, re-rendered at any size with reveal orders

**كيف:** def build(): return [Step(name, [ops…], order, origin=…)]; ellipse 48 segments; supersampling ss=3; reveal orders sweep/grow/rise/down/left/right/sparkle (tested as permutations). Renderer + Svg tests 10/10 here.

**المعاملات:** sheet 1200×800; ss 3; ellipse 48 segs; dots 10/20 segs

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أشكال · primitives · scene language · studio · vector · رسم متجه · خطوات · كشف تدريجي · steps · reveal order

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-studio/render.py:259`
- `kosif-studio/render.py:278`
- `kosif-studio/tests/test_studio.py:106`
- `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-41` محلل لغة مسارات SVG كاملة / Full SVG path parser (Studio) (proven)
- `SHAPE-42` أشكال مركبة بثقوب / Even-odd compound shapes & holes (proven)
- `SHAPE-44` منحنيات كاتمول-روم / Catmull-Rom smooth curves (ready)
- `SHAPE-45` أنبوب بنصف قطر متغير / Variable-radius tube (limbs, tails, flames, hair) (ready)

### `SHAPE-44` — منحنيات كاتمول-روم / Catmull-Rom smooth curves

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط قليلة تصير منحنى ناعمًا يمر بها، مفتوحًا أو مغلقًا — أساس الأنابيب وملامح الحوت والخطوط العضوية. / A few control points become a smooth curve through them, open or closed — base for tubes and organic outlines.

**متى:** حين يريد منحنى ناعمًا يمر بنقاط قليلة لرسم خطوط عضوية أو أنابيب / when a few control points should become a smooth curve for organic outlines or tubes

**كيف:** render.catmull(points, n=10, closed=False).

**المعاملات:** n samples per segment (default 10)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كاتمول-روم · catmull-rom · curve · organic · منحنى ناعم · نقاط تحكم · خطوط عضوية · smooth curve · spline

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-studio/render.py:57`

#### 7. قدرات قريبة في العائلة

- `SHAPE-42` أشكال مركبة بثقوب / Even-odd compound shapes & holes (proven)
- `SHAPE-43` عدة الأشكال الأساسية ولغة المشهد / Basic shape kit & Step scene language (proven)
- `SHAPE-45` أنبوب بنصف قطر متغير / Variable-radius tube (limbs, tails, flames, hair) (ready)
- `SHAPE-46` سلاسل جبال بالإزاحة / Midpoint-displacement mountain ridges (ready)

### `SHAPE-45` — أنبوب بنصف قطر متغير / Variable-radius tube (limbs, tails, flames, hair)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ضربة عضوية على عمود فقري ناعم بنصف قطر لكل نقطة، كاتحاد أرباع وأقراص فلا تنثقب المنعطفات الحادة. / Organic stroke along a smooth spine with per-point radius, built as quads + discs so tight bends never punch holes.

**متى:** حين يرسم أطرافًا أو ذيولًا أو لهبًا أو شعرًا كضربة بسمك متغير / when drawing limbs, tails, flames or hair as a stroke with varying thickness

**كيف:** render.tube(spine, radii, n=8) (discs every n//2 samples where r > .6); 3D: K3S.tube(points, r, color, {segments}) Catmull-Rom TubeGeometry 32 segments × 8 radial, roughness .6. Outlines: render.stroke(polys, width) with round caps.

**المعاملات:** 2D n 8; 3D 32×8 segments

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أنبوب · tube · stroke · limbs · tail · أطراف · ذيل · لهب · شعر · flames · hair

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-studio/render.py:286`
- `kosif-studio/render.py:241`
- `kosif-studio/scenes/dragon_girl.py:229`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:329`

#### 7. قدرات قريبة في العائلة

- `SHAPE-43` عدة الأشكال الأساسية ولغة المشهد / Basic shape kit & Step scene language (proven)
- `SHAPE-44` منحنيات كاتمول-روم / Catmull-Rom smooth curves (ready)
- `SHAPE-46` سلاسل جبال بالإزاحة / Midpoint-displacement mountain ridges (ready)
- `SHAPE-47` صندوق أيزومتري بثلاث درجات / Three-tone isometric box (seen)

### `SHAPE-46` — سلاسل جبال بالإزاحة / Midpoint-displacement mountain ridges

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صور ظلية لجبال متعددة الطبقات بالإزاحة العشوائية للنقطة الوسطى مع قمم منحوتة، مملوءة حتى أسفل الصفحة. / Layered mountain silhouettes by recursive midpoint displacement with optional carved peaks.

**متى:** حين يحتاج المشهد سلاسل جبال بصور ظلية متعددة الطبقات للخلفية أو البارالاكس / when a scene needs layered mountain silhouettes, e.g. as parallax backdrops

**كيف:** scenes/dragon_girl.ridge(seed, base, amp, rough=.55, peaks=[(x, height, width)]); 7 rounds, amplitude × rough per round; stack 3–4 layers lighter with distance.

**المعاملات:** 7 rounds; rough .55

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** جبال · mountains · midpoint displacement · landscape · parallax · خلفية · طبيعة · صور ظلية · silhouette · ridges

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-studio/scenes/dragon_girl.py:20`

#### 7. قدرات قريبة في العائلة

- `SHAPE-44` منحنيات كاتمول-روم / Catmull-Rom smooth curves (ready)
- `SHAPE-45` أنبوب بنصف قطر متغير / Variable-radius tube (limbs, tails, flames, hair) (ready)
- `SHAPE-47` صندوق أيزومتري بثلاث درجات / Three-tone isometric box (seen)
- `SHAPE-48` بناء نقطة ثم خط ثم مستوى / Point → line → plane build (seen)

### `SHAPE-47` — صندوق أيزومتري بثلاث درجات / Three-tone isometric box

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاثة مضلعات من لون واحد (أعلى أفتح، يسار متوسط، يمين أغمق) مع حافة علوية بيضاء شفافة وظل أرضي ناعم. / Three polygons of one hue (top lightest, left mid, right darkest) plus a thin translucent white top edge and soft ground shadow.

**متى:** حين يرسم صندوقًا أو مكعبًا أيزومتريًا بثلاث درجات من لون واحد مع ظل ناعم / when drawing an isometric box in three tones of one hue with a soft ground shadow

**كيف:** Lightness steps ~+12 / 0 / −12%; 30° projection; shadow ellipse blur 20 px at 20%.

**المعاملات:** +12/0/−12% lightness

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أيزومتري · isometric · box · 2.5d · مكعب · ظل أرضي · درجات اللون · cube · shading

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/isometric`

#### 7. قدرات قريبة في العائلة

- `SHAPE-45` أنبوب بنصف قطر متغير / Variable-radius tube (limbs, tails, flames, hair) (ready)
- `SHAPE-46` سلاسل جبال بالإزاحة / Midpoint-displacement mountain ridges (ready)
- `SHAPE-48` بناء نقطة ثم خط ثم مستوى / Point → line → plane build (seen)
- `SHAPE-49` خطوط متدفقة ومسارات مخططة / Flowing dashes, striped tubes, dotted trails (seen)

### `SHAPE-48` — بناء نقطة ثم خط ثم مستوى / Point → line → plane build

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يبدأ من نقطة تقاطع بإحداثياتها، تمتد إلى مسطرة بعلامات، ثم تنبثق إلى مستوى مائل يحمل النص. / Start from a crosshair point with a coordinate label, stretch to a ruler line with ticks, then extrude/skew into a plane carrying text.

**متى:** حين يريد بناءً تدريجيًا من نقطة إلى خط بمسطرة ثم مستوى مائل يحمل النص / when a build should grow from a point to a ruler line to a skewed plane carrying text

**كيف:** Each stage ~1.2 s easeInOutExpo; skew −25° for the plane.

**المعاملات:** 1.2 s per stage; skew −25°

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نقطة · خط · مستوى · construction · build · مسطرة · إحداثيات · بناء تدريجي · ruler · plane

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-ayushunleashed-ece3e3`

#### 7. قدرات قريبة في العائلة

- `SHAPE-46` سلاسل جبال بالإزاحة / Midpoint-displacement mountain ridges (ready)
- `SHAPE-47` صندوق أيزومتري بثلاث درجات / Three-tone isometric box (seen)
- `SHAPE-49` خطوط متدفقة ومسارات مخططة / Flowing dashes, striped tubes, dotted trails (seen)
- `SHAPE-50` خيوط موجية وأشرطة متلوية / Sine strands & ribbon loops (ready)

### `SHAPE-49` — خطوط متدفقة ومسارات مخططة / Flowing dashes, striped tubes, dotted trails

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قناة ماء بشرطات بيضاء تنزلق، أنبوب مخطط من ثلاث ضربات متناقصة، أثر نقطي لقوس رمي، خط نبض قلب، وحبل يتدلى بوزن الكلمة. / A water channel with sliding white dashes, a striped tube of three decreasing strokes, a dotted throw arc, an ECG spike line, a rope sagging under a word.

**متى:** حين يحتاج خطوطًا متدفقة كقناة ماء أو أثر قوس رمي أو خط نبض أو حبلًا يتدلى / when lines should flow like a water channel, trace a throw arc, spike like an ECG or sag like a rope

**كيف:** strokeDashoffset flow: dash 20/60 px at ~40 px/s (MOTION.flowDash(tl, path, at, dur, {pattern:"28 22", cycles:6})); stripes = same path stroked 3× red/white/blue; throw = Bezier with dots every 8 px fading; rope = quadratic with control y += sag 30–60 px on a spring.

**المعاملات:** dash 20/60 px @ 40 px/s; sag 30–60 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شرطات · تدفق · dash flow · stripes · rope · ecg · trail · نبض القلب · حبل · خطوط متقطعة · dashed line · flow

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-studio/motion/kit/motion-kit.js:247`
- `kosif-tool/styles/doodle`
- `kosif-tool/styles/pm-ajith-io-b5626e`
- `kosif-tool/styles/pm-gdgtify-287ddf`

#### 7. قدرات قريبة في العائلة

- `SHAPE-47` صندوق أيزومتري بثلاث درجات / Three-tone isometric box (seen)
- `SHAPE-48` بناء نقطة ثم خط ثم مستوى / Point → line → plane build (seen)
- `SHAPE-50` خيوط موجية وأشرطة متلوية / Sine strands & ribbon loops (ready)
- `SHAPE-51` خطان قطريان فقط / Exactly two drifting diagonal lines (ready)

### `SHAPE-50` — خيوط موجية وأشرطة متلوية / Sine strands & ribbon loops

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاث موجات جيبية ملونة تعبر النصف السفلي وتكبر سعتها مع تقدم المشهد، أو أشرطة متدرجة سميكة بنقاط تحكم تتحرك ببطء. / Three coloured sine waves crossing the lower half, growing in amplitude as the scene progresses; or thick gradient ribbon loops with slowly moving control points.

**متى:** حين يريد خلفية من موجات جيبية ملونة أو أشرطة متدرجة تتلوى ببطء تحت النص / for a background of coloured sine waves or slowly moving gradient ribbon loops under text

**كيف:** y = h(.55 + .07·line) + sin(x/w·3π + 2·phase + 1.9·line)·(10 + 12p), step 4 px, colours #d3f66a #6ad8d1 #e995ff alpha .42; ribbons: 2–3 cubic paths, stroke ~6% of frame, gradient strokes, round caps, opacity .35 under text; 7-band rainbow ribbon y = sin(xk + t).

**المعاملات:** 3 waves, amplitude 10→22 px; ribbons 6% stroke

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** موجة · جيب · sine · ribbon · strands · background · موجات · أشرطة · قوس قزح · waves · rainbow

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `fastify-motion-bro/web/motion.js:16`
- `kosif-tool/styles/pm-gonzalomacagno-2de1a9`
- `kosif-tool/styles/pm-hoyoyoda-3a5c08`

#### 7. قدرات قريبة في العائلة

- `SHAPE-48` بناء نقطة ثم خط ثم مستوى / Point → line → plane build (seen)
- `SHAPE-49` خطوط متدفقة ومسارات مخططة / Flowing dashes, striped tubes, dotted trails (seen)
- `SHAPE-51` خطان قطريان فقط / Exactly two drifting diagonal lines (ready)
- `SHAPE-52` شبكة بلاطات باوهاوس / Bauhaus tile grid (glyph swap on a distance wave) (proven)

### `SHAPE-51` — خطان قطريان فقط / Exactly two drifting diagonal lines

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** توقيع: خطان منحنيان شفافان خلف كل شيء ينجرفان باستمرار ولا يتوقفان — أبدًا ثلاثة. / Signature motif: two translucent curved diagonals behind everything, drifting continuously — never three.

**متى:** حين يطلب توقيعًا بصريًا تحريريًا من خطين قطريين منحنيين ينجرفان خلف المحتوى / for an editorial signature of exactly two curved diagonal lines drifting behind the content

**كيف:** For k in 0..1: ox = sin(.20·phase + 2.3k)·.035w, oy = cos(.16·phase + k)·.02h; quadratic from (−.2w + .63w·k, .93h) via (.30w + .41w·k, .43h) to (.65w + .5w·k, −.10h); stroke 50% alpha, 1.6·scale. The storyboard test asserts exact_background_lines = 2 (fastify tests 24/24 passed here).

**المعاملات:** 2 lines; drift ±3.5% w, ±2% h

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خطان · two lines · editorial · signature · background · خطوط قطرية · توقيع بصري · خلفية · diagonal lines · drift

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `fastify-motion-bro/web/editorial.js:47-49`
- `fastify-motion-bro/docs/VIRAL-EDITORIAL-DNA.md:18`
- `fastify-motion-bro/tests/viral-editorial.test.mjs:8`

#### 7. قدرات قريبة في العائلة

- `SHAPE-49` خطوط متدفقة ومسارات مخططة / Flowing dashes, striped tubes, dotted trails (seen)
- `SHAPE-50` خيوط موجية وأشرطة متلوية / Sine strands & ribbon loops (ready)
- `SHAPE-52` شبكة بلاطات باوهاوس / Bauhaus tile grid (glyph swap on a distance wave) (proven)
- `SHAPE-53` بلاطات تروشيه بموجة تلوين / Truchet tiles with a recolour wave (proven)

### `SHAPE-52` — شبكة بلاطات باوهاوس / Bauhaus tile grid (glyph swap on a distance wave)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل خلية ترسم واحدًا من {ربع دائرة، مثلث، شريط، دائرة} بلوحة 4–5 ألوان، وتبدّل شكلها ولونها بدوران متتابع حسب المسافة. / Each cell draws one of {quarter circle, triangle, bar, circle} in a 4–5 colour palette and swaps glyph/colour with rotation staggered by distance.

**متى:** حين يريد شبكة بلاطات هندسية بأسلوب باوهاوس تتبدل أشكالها وألوانها بموجة أو على الإيقاع / when a Bauhaus tile grid should swap shapes and colours in a wave or on the beat

**كيف:** step = floor(max(0, t·4 − d·.3)) with d = x+y (diagonal) or distance from centre; rotate step·90°; palette red #d6341f, yellow #e9c634, blue #2135bc, black on cream #f3ead8. Rendered here (6×6 lab). On beat: advance one step per beat.

**المعاملات:** 8×5 to 16×9 cells; stagger 15–40 ms; swap every 200–250 ms or 1 beat; back.inOut(1.7)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** باوهاوس · bauhaus · tile grid · quarter circle · geometric · beat · بلاطات · أرباع دوائر · على الإيقاع · pattern · glyph swap

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-leonkohli-6dc01b`
- `kosif-tool/styles/pm-prasenx-8d9323`
- `kosif-tool/styles/pm-samuel-spitz-974923`
- `kosif-tool/styles/pm-zaqailo-212ad3`

#### 7. قدرات قريبة في العائلة

- `SHAPE-50` خيوط موجية وأشرطة متلوية / Sine strands & ribbon loops (ready)
- `SHAPE-51` خطان قطريان فقط / Exactly two drifting diagonal lines (ready)
- `SHAPE-53` بلاطات تروشيه بموجة تلوين / Truchet tiles with a recolour wave (proven)
- `SHAPE-54` موجة في شبكة أشكال / Distance-delayed grid wave (rotate / scale / morph) (seen)

### `SHAPE-53` — بلاطات تروشيه بموجة تلوين / Truchet tiles with a recolour wave

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بلاطات بأرباع دوائر بدوران عشوائي، وموجة شعاعية تديرها 90° وتلونها بالأحمر مع اضمحلال. / Quarter-arc Truchet tiles at random rotations; a radial wave front rotates them 90° and tints them red with falloff.

**متى:** حين يريد نمط بلاطات بأقواس تدور وتتلون بموجة شعاعية كخلفية توليدية / when quarter-arc tiles should rotate and recolour under a radial wave as a generative pattern

**كيف:** Per tile two quarter arcs at opposite corners, stroke 14–18 px round caps; p = clamp(t·speed − d·k), rotation += ease(p)·90°, colour accent while 0<p<1. Rendered here (lab).

**المعاملات:** tile 60–80 px, stroke 14–18 px, delay 20–40 ms per tile, wave 600 px/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تروشيه · truchet · tiles · generative · wave · نمط توليدي · أقواس · موجة لونية · pattern · quarter arcs

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-levabashidze-2d713a`
- `kosif-tool/styles/pm-roundtablespace-d3a1be`
- `kosif-tool/styles/pm-stephanlivera-df17a2`

#### 7. قدرات قريبة في العائلة

- `SHAPE-51` خطان قطريان فقط / Exactly two drifting diagonal lines (ready)
- `SHAPE-52` شبكة بلاطات باوهاوس / Bauhaus tile grid (glyph swap on a distance wave) (proven)
- `SHAPE-54` موجة في شبكة أشكال / Distance-delayed grid wave (rotate / scale / morph) (seen)
- `SHAPE-55` بلاطات تنقلب وشريط لا ينتهي / Tile flips & endless strip loops (MG-116/117) (documented)

### `SHAPE-54` — موجة في شبكة أشكال / Distance-delayed grid wave (rotate / scale / morph)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة مربعات أو نقاط أو معينات: كل خلية تدور 45–90° أو تتحول مربعًا→دائرة أو تكبر حسب sin(المسافة − t). / Grid of squares/dots/diamonds: each cell rotates 45–90°, morphs square→circle (border-radius) or scales by sin(distance − t).

**متى:** حين يريد موجة تسري في شبكة مربعات أو نقاط فتدور أو تكبر أو تصير دوائر بالتتابع / when a wave should ripple through a grid of squares or dots, rotating, scaling or rounding them in sequence

**كيف:** delay = (x+y)·25 ms or distance·30–40 ms; border-radius 0→50%; 4×4 grid: 40 ms per cell, 400 ms each; ripple variant swaps shape/colour with a 200 ms scale pop; spring ripple stiffness 220 damping 12 at 900 px/s.

**المعاملات:** cell 30 px gap 40 px; 25–40 ms per cell; 400–600 ms each

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شبكة · موجة · grid wave · ripple · stagger · distance delay · تموج · تتابع · مربعات · dots grid · square to circle

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/playbooks/shapes.md:47`
- `kosif-tool/styles/pm-jasonzhou1993-8595e0`
- `kosif-tool/styles/pm-teslachartz-c58b32`
- `kosif-tool/styles/pm-ndhabarde11-f155b4`

#### 7. قدرات قريبة في العائلة

- `SHAPE-52` شبكة بلاطات باوهاوس / Bauhaus tile grid (glyph swap on a distance wave) (proven)
- `SHAPE-53` بلاطات تروشيه بموجة تلوين / Truchet tiles with a recolour wave (proven)
- `SHAPE-55` بلاطات تنقلب وشريط لا ينتهي / Tile flips & endless strip loops (MG-116/117) (documented)
- `SHAPE-56` زهرة النقاط الذهبية / Phyllotaxis dot flower (137.5°) (proven)

### `SHAPE-55` — بلاطات تنقلب وشريط لا ينتهي / Tile flips & endless strip loops (MG-116/117)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة بلاطات تنقلب صفًا صفًا إلى لون ثانٍ وتعود؛ وصف صور ينزلق وطرفه يلاقي بدايته. / A tile grid flips row by row to a second colour and back; a row of images scrolls with its end meeting its start.

**متى:** حين يريد بلاطات تنقلب صفًا صفًا أو شريط صور ينزلق بلا نهاية في حلقة سلسة / when tiles should flip row by row or an image strip should scroll endlessly in a seamless loop

**كيف:** MG-116: 0–4 s flip, 4–8 s return, scaleX or 2.5D rotate with row delay, no harsh flashing. MG-117: move exactly one repeat-unit width (gaps included) in 10 s using two identical copies, linear — a miscounted gap causes a jump.

**المعاملات:** 8 s / 10 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بلاطات · شريط · loop · tile flip · marquee · انقلاب · شريط صور · تكرار · seamless · image strip

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-loops-backgrounds.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-53` بلاطات تروشيه بموجة تلوين / Truchet tiles with a recolour wave (proven)
- `SHAPE-54` موجة في شبكة أشكال / Distance-delayed grid wave (rotate / scale / morph) (seen)
- `SHAPE-56` زهرة النقاط الذهبية / Phyllotaxis dot flower (137.5°) (proven)
- `SHAPE-57` منحنيات ليساجو / Lissajous curves & tangles (seen)

### `SHAPE-56` — زهرة النقاط الذهبية / Phyllotaxis dot flower (137.5°)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** n نقطة بزاوية i·137.5° ونصف قطر c·√i تكوّن زهرة عباد شمس تدور ببطء. / n dots at angle i·137.5°, radius c·√i — a sunflower that rotates slowly.

**متى:** حين يريد نقاطًا مرتبة كزهرة عباد الشمس أو توزيع عناصر حول مركز بالزاوية الذهبية / when dots should form a sunflower pattern or items be spread around a centre by the golden angle

**كيف:** Rendered here (400 dots, hue ramp, rotation .4 rad/s). Same law places N items around a centre without geometry data: r = R√((i+.6)/n), a = i·2.39996 rad (earth sales-geo engine, R = min(58, 20+3n)).

**المعاملات:** n ≈ 400; 137.5° (2.39996 rad); r = c√i

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** زهرة · زاوية ذهبية · phyllotaxis · golden angle · sunflower · generative · عباد الشمس · توزيع النقاط · دوران بطيء · spiral · dot distribution

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-earth-ci-fork/app/src/engine/fusion/sales/sales-geo-engine.ts:83`
- `kosif-tool/styles/pm-ajith-io-b5626e`
- `kosif-tool/styles/pm-mrtanviir-132457`

#### 7. قدرات قريبة في العائلة

- `SHAPE-54` موجة في شبكة أشكال / Distance-delayed grid wave (rotate / scale / morph) (seen)
- `SHAPE-55` بلاطات تنقلب وشريط لا ينتهي / Tile flips & endless strip loops (MG-116/117) (documented)
- `SHAPE-57` منحنيات ليساجو / Lissajous curves & tangles (seen)
- `SHAPE-58` خطوط توليدية بأسلوب Joy Division / Ridge-line generative waves (seen)

### `SHAPE-57` — منحنيات ليساجو / Lissajous curves & tangles

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** x = A sin(at+δ)، y = B sin(bt) بنسب 3:2 و5:4، عشرون نسخة بانجراف بطيء لـ δ ومزج جمعي. / x = A sin(at+δ), y = B sin(bt) at 3:2, 5:4; 20 copies with drifting δ, additive low alpha, glow.

**متى:** حين يريد منحنيات ليساجو متشابكة متوهجة بطابع راسم الذبذبات / when glowing tangled Lissajous curves with an oscilloscope look are wanted

**كيف:** δ drift .2 rad/s; neon stroke with glow (GLOW); 3D variant (sin 3t, sin 2t, sin 5t).

**المعاملات:** δ .2 rad/s; 20 copies

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ليساجو · lissajous · oscilloscope · math · curves · راسم الذبذبات · منحنيات متشابكة · نيون · neon · glow

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-rneayan-ea6129`
- `kosif-tool/styles/pm-math-files-39c9d0`

#### 7. قدرات قريبة في العائلة

- `SHAPE-55` بلاطات تنقلب وشريط لا ينتهي / Tile flips & endless strip loops (MG-116/117) (documented)
- `SHAPE-56` زهرة النقاط الذهبية / Phyllotaxis dot flower (137.5°) (proven)
- `SHAPE-58` خطوط توليدية بأسلوب Joy Division / Ridge-line generative waves (seen)
- `SHAPE-59` كسيريات وزخارف رياضية / Fractals, kolam, golden spiral, kaleidoscope (seen)

### `SHAPE-58` — خطوط توليدية بأسلوب Joy Division / Ridge-line generative waves

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 40–60 خطًا أفقيًا تزاح بالضوضاء قرب المركز مع أشرطة ملونة تنزلق. / 40–60 horizontal polylines displaced by noise near the centre, with coloured bars sliding across.

**متى:** حين يريد خطوطًا أفقية متراكبة تتموج بالضوضاء قرب المنتصف بأسلوب Joy Division / when stacked horizontal lines should be noise-displaced near the centre in a Joy Division ridge style

**كيف:** Amplitude ramp 0→60 px toward the centre (Gaussian window); fill each line with background to occlude the ones behind; gradient red→blue by row.

**المعاملات:** 40–60 lines; amp 0→60 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خطوط · ridgeline · joy division · generative · noise · خطوط أفقية · موجات · توليدي · waves · lines

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-motiondsgnr-9dcfa6`

#### 7. قدرات قريبة في العائلة

- `SHAPE-56` زهرة النقاط الذهبية / Phyllotaxis dot flower (137.5°) (proven)
- `SHAPE-57` منحنيات ليساجو / Lissajous curves & tangles (seen)
- `SHAPE-59` كسيريات وزخارف رياضية / Fractals, kolam, golden spiral, kaleidoscope (seen)
- `SHAPE-60` جدار أيقونات مائل / Tilted icon wall (seen)

### `SHAPE-59` — كسيريات وزخارف رياضية / Fractals, kolam, golden spiral, kaleidoscope

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سيربنسكي يُبنى عمقًا عمقًا، كولام يلف حول شبكة نقاط بنقطة متوهجة تقوده، حلزون ذهبي فوق مربعات فيبوناتشي، جوليا بالشيدر، وتماثل كاليدوسكوبي. / Sierpinski depth by depth, a kolam loop weaving around a dot grid led by a glowing dot, a golden spiral over Fibonacci tiles, a Julia shader, kaleidoscope symmetry.

**متى:** حين يريد زخارف رياضية متحركة: سيربنسكي أو كولام أو حلزون ذهبي أو جوليا أو مشكال / when animated math patterns are wanted: Sierpinski, kolam, golden spiral, Julia set or kaleidoscope

**كيف:** Sierpinski 4–6 levels × 200 ms; kolam 7×5 dots one closed path drawn by dashoffset; Fibonacci tiles #c8b8f0→#e6dcf8 then quarter-arc chain 1.5–2 s; Julia z²+c purple→orange; kaleidoscope = polar fold n = 6–12 of a rotating texture (wedge 10°/s).

**المعاملات:** Sierpinski 4–6 × 200 ms; kaleidoscope 6–12 folds

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كسيري · fractal · kolam · fibonacci · kaleidoscope · julia · حلزون ذهبي · مشكال · فيبوناتشي · sierpinski · golden spiral

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-59` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-buildfastwithai-53234e`
- `kosif-tool/styles/pm-ddryo-loos-300829`
- `kosif-tool/styles/pm-math-files-39c9d0`
- `kosif-tool/styles/pm-monokern-ade5b6`

#### 7. قدرات قريبة في العائلة

- `SHAPE-57` منحنيات ليساجو / Lissajous curves & tangles (seen)
- `SHAPE-58` خطوط توليدية بأسلوب Joy Division / Ridge-line generative waves (seen)
- `SHAPE-60` جدار أيقونات مائل / Tilted icon wall (seen)
- `SHAPE-61` كتل أنماط شيدرية وشبكة متحركة / HyperFrames pattern shaders & dynamic grid (install)

### `SHAPE-60` — جدار أيقونات مائل / Tilted icon wall

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة بلاطات مستديرة بأيقونات خطية، مائلة −12° وتنجرف قطريًا، وبلاطة واحدة أسطع. / Grid of rounded tiles with line icons rotated ~−12° drifting diagonally, one tile highlighted.

**متى:** حين يريد خلفية جدار أيقونات مائلة تنجرف لعرض التكاملات مع إبراز أيقونة واحدة / for a tilted, drifting wall of icon tiles, e.g. showing integrations, with one tile highlighted

**كيف:** Tile 90 px, radius 18 px, opacity .25–.4, drift 20 px/s; highlight = full opacity + accent border.

**المعاملات:** 90 px, r 18, drift 20 px/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أيقونات · icon wall · integrations · grid · جدار أيقونات · تكاملات · خلفية · tilted · highlight

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-60` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-gabrielbuzziv-4ff0c6`

#### 7. قدرات قريبة في العائلة

- `SHAPE-58` خطوط توليدية بأسلوب Joy Division / Ridge-line generative waves (seen)
- `SHAPE-59` كسيريات وزخارف رياضية / Fractals, kolam, golden spiral, kaleidoscope (seen)
- `SHAPE-61` كتل أنماط شيدرية وشبكة متحركة / HyperFrames pattern shaders & dynamic grid (install)
- `SHAPE-62` حلقات دوران بنسب صحيحة / Integer-ratio rotation loops (MG-112/115) (documented)

### `SHAPE-61` — كتل أنماط شيدرية وشبكة متحركة / HyperFrames pattern shaders & dynamic grid

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 (+ MIT shaders library). |

**ما هي:** حلقات متموجة، حلزون أوب آرت، خطوط قطرية، خلايا فورونوي (WebGPU)، وشبكة متحركة بمتغيرات CSS. / Ripples, op-art spiral, sliding stripes, Voronoi cells (WebGPU shaders) and a CSS-variable dynamic grid.

**متى:** حين يحتاج خلفيات أنماط من HyperFrames كتموجات أو حلزون أو خطوط أو خلايا فورونوي أو شبكة متحركة / for HyperFrames pattern plates: ripples, op-art spiral, stripes, Voronoi cells or a dynamic grid

**كيف:** npx hyperframes add ripples \| spiral \| stripes \| voronoi (data-shader, data-requires-webgpu — WebGPU not verified here) \| dynamic-grid (density fine\|standard\|coarse, weight hairline\|standard\|bold).

**المعاملات:** 2 s plates, 1920×1080

**التثبيت:** npx hyperframes add dynamic-grid

**الوسوم:** شيدر · voronoi · spiral · stripes · ripples · grid · hyperframes · أنماط · خلفية · خداع بصري · op-art · webgpu

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-61` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-one/vendor/hyperframes/registry/blocks/voronoi/voronoi.html`
- `kosif-one/vendor/hyperframes/registry/components/dynamic-grid/dynamic-grid.html`

#### 7. قدرات قريبة في العائلة

- `SHAPE-59` كسيريات وزخارف رياضية / Fractals, kolam, golden spiral, kaleidoscope (seen)
- `SHAPE-60` جدار أيقونات مائل / Tilted icon wall (seen)
- `SHAPE-62` حلقات دوران بنسب صحيحة / Integer-ratio rotation loops (MG-112/115) (documented)
- `SHAPE-63` حلقات متحدة المركز بفجوات / Rotating gapped concentric rings (proven)

### `SHAPE-62` — حلقات دوران بنسب صحيحة / Integer-ratio rotation loops (MG-112/115)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط تدور حول مركز بعيدًا عن النص، أو قوسان بسرعتين مترابطتين حول مركز واحد — نسب دورات صحيحة تضمن حلقة بلا قفزة. / Dots orbit a centre away from the text, or two arcs rotate at related speeds — integer turn ratios guarantee a seamless loop.

**متى:** حين يريد نقاطًا أو أقواسًا تدور حول مركز في حلقة تتكرر بلا قفزة عند نقطة الوصل / when orbiting dots or arcs must loop seamlessly with no jump at the seam

**كيف:** MG-112: exactly one turn in 6 s, linear, evenly spaced angles. MG-115: arc A 1 turn, arc B 2 turns per 6 s around a shared centre; never export the first frame twice at the seam (render t ∈ [0, T)).

**المعاملات:** 6 s; ratio 1:2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حلقة · loop · seamless · rotation · orbit · تكرار سلس · دوران · بلا قفزة · integer ratio · arcs

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-62` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-loops-backgrounds.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-60` جدار أيقونات مائل / Tilted icon wall (seen)
- `SHAPE-61` كتل أنماط شيدرية وشبكة متحركة / HyperFrames pattern shaders & dynamic grid (install)
- `SHAPE-63` حلقات متحدة المركز بفجوات / Rotating gapped concentric rings (proven)
- `SHAPE-64` عنقود أقواس مدارية ونواة نابضة / Orbiting arc cluster + pulsing donut core (ready)

### `SHAPE-63` — حلقات متحدة المركز بفجوات / Rotating gapped concentric rings

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** N قوسًا متحد المركز لكل منها فجوة، تدور بسرعات متناوبة الاتجاه. / N concentric arcs each with a gap, rotating at alternating-sign speeds.

**متى:** حين يريد مؤشر تحميل أو زخرفة من حلقات متحدة المركز بفجوات تدور باتجاهات متعاكسة / for a loader or motif of gapped concentric rings spinning in alternating directions

**كيف:** arc from gapStart+gap to gapStart+2π; gapStart_i += ω_i·dt with alternating sign; equal spacing; round caps. Rendered here (12 rings). Collapse variant: 6 rings 90–360°/s scale to a centre dot in 500 ms easeIn.

**المعاملات:** N 12, stroke 6–8 px, spacing ~13–14 px, ω .3–1.2 rad/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حلقات · concentric rings · gap · loader · rotation · مؤشر تحميل · دوائر · تحميل · spinner · arcs

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-63` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-kantamk-61f410`
- `kosif-tool/styles/pm-leonkohli-6dc01b`

#### 7. قدرات قريبة في العائلة

- `SHAPE-61` كتل أنماط شيدرية وشبكة متحركة / HyperFrames pattern shaders & dynamic grid (install)
- `SHAPE-62` حلقات دوران بنسب صحيحة / Integer-ratio rotation loops (MG-112/115) (documented)
- `SHAPE-64` عنقود أقواس مدارية ونواة نابضة / Orbiting arc cluster + pulsing donut core (ready)
- `SHAPE-65` حلقات مدارية إهليلجية / Orbital ellipse rings & accents (ready)

### `SHAPE-64` — عنقود أقواس مدارية ونواة نابضة / Orbiting arc cluster + pulsing donut core

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ستة أقواس 270° تدور حول مركز بمسافات متغيرة بلونين، ونواة دائرية ليمونية تتنفس في الوسط. / Six 270° arcs orbit a centre at varying distance in teal/lime with pulsing opacity; a breathing lime donut core in the middle.

**متى:** حين يريد عنصرًا مركزيًا حيًا من أقواس تدور حول نواة دائرية تتنفس / when a central motif of orbiting arcs around a breathing donut core is wanted

**كيف:** Arc k: angle = .5·phase + kπ/3, dist = w(.15 + .055 sin), radius w(.04 + .016 sin), sweep 1.5π, #89d6ce / #d5f375, alpha .24 + .25 sin²; core r = w(.12 + .025 sin(1.25 phase)) #c9f96d with inner #0a1724 at .58r.

**المعاملات:** 6 arcs, 270°; core 12% ± 2.5% w

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مدار · أقواس · orbit · arcs · core · pulse · نواة · تنفس · دوران · donut · breathing

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-64` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `fastify-motion-bro/web/motion.js:13-14`
- `fastify-motion-bro/web/motion.js:15`

#### 7. قدرات قريبة في العائلة

- `SHAPE-62` حلقات دوران بنسب صحيحة / Integer-ratio rotation loops (MG-112/115) (documented)
- `SHAPE-63` حلقات متحدة المركز بفجوات / Rotating gapped concentric rings (proven)
- `SHAPE-65` حلقات مدارية إهليلجية / Orbital ellipse rings & accents (ready)
- `SHAPE-66` انفجار خطوط شعاعي / Radial line burst (proven)

### `SHAPE-65` — حلقات مدارية إهليلجية / Orbital ellipse rings & accents

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاث حلقات إهليلجية مائلة تدور ببطء حول مركز التوهج، أو حلقة رفيعة تدور حول البطل، أو نجمة رباعية دوارة. / Three tilted concentric ellipses rotating slowly around the glow centre, a thin orbit ring around the hero, or a spinning four-spoke starburst.

**متى:** حين يريد حلقات مدارية إهليلجية مائلة حول مركز توهج أو حول البطل أو نجمة دوارة / for tilted orbital ellipse rings around a glow or hero object, or a spinning starburst accent

**كيف:** ctx.rotate(.1·t); radii r(.66 + .18i) × r(.2 + .11i), tilt .3 + .65i rad, line .002·min(w,h); hero ring ellipse (.5w,.405h) .283w × .157h, rotation sin(.1 phase)·.12; starburst translate(.82w,.273h), rotate(.21 phase), spokes 10→24 px; satellites on a dashed ellipse tilted 20°.

**المعاملات:** 3 rings at .1 rad/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مدار · إهليلج · orbit ring · ellipse · starburst · حلقات مائلة · أقمار · نجمة · tilted rings · satellites

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-65` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:68`
- `fastify-motion-bro/web/editorial.js:67-70`
- `kosif-tool/styles/pm-samuel-spitz-974923`

#### 7. قدرات قريبة في العائلة

- `SHAPE-63` حلقات متحدة المركز بفجوات / Rotating gapped concentric rings (proven)
- `SHAPE-64` عنقود أقواس مدارية ونواة نابضة / Orbiting arc cluster + pulsing donut core (ready)
- `SHAPE-66` انفجار خطوط شعاعي / Radial line burst (proven)
- `SHAPE-67` حلقة صدمة أرضية ونبض قلب / Shockwave ring & heartbeat ripple (proven)

### `SHAPE-66` — انفجار خطوط شعاعي / Radial line burst

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 12–60 خطًا تنطلق من المركز بأطوال وألوان متفاوتة بـ expo.out مع تتابع 20 ms، ثم تخبو. / 12–60 lines shoot from the centre with varied length/colour, expo.out, 20 ms stagger, then fade.

**متى:** حين يريد انفجار خطوط من المركز لإبراز لحظة أو ضربة إيقاع / when lines should burst from the centre to emphasise a moment or a beat

**كيف:** r0 = 20 + 30b, r1 = 40 + 120b with b = 1 − (1−p)^5; alternate accent/primary; fade over the second half. Rendered here (14 lines). Basma TEMPLATES.shapes: 14 lines from m(.1 + .25k) to m(.16 + .42k)·jitter + ring .42m·k in .6–1 s.

**المعاملات:** 400–600 ms expo.out; 12–60 rays; stagger 20 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** انفجار · خطوط شعاعية · burst · rays · emphasis · beat · إبراز · أشعة · ضربة الإيقاع · radial lines · accent

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-66` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `app/public/js/00_editor.js:518`
- `kosif-tool/styles/pm-teslachartz-c58b32`
- `kosif-tool/styles/pm-shinskinakamoto-20190b`
- `kosif-tool/styles/pm-stephanlivera-df17a2`

#### 7. قدرات قريبة في العائلة

- `SHAPE-64` عنقود أقواس مدارية ونواة نابضة / Orbiting arc cluster + pulsing donut core (ready)
- `SHAPE-65` حلقات مدارية إهليلجية / Orbital ellipse rings & accents (ready)
- `SHAPE-67` حلقة صدمة أرضية ونبض قلب / Shockwave ring & heartbeat ripple (proven)
- `SHAPE-68` أشعة شمسية دوارة / Rotating sunburst ground (proven)

### `SHAPE-67` — حلقة صدمة أرضية ونبض قلب / Shockwave ring & heartbeat ripple

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حلقة إهليلجية مسطحة (y×0.25) تتسع 0→300px في 500ms وتخبو؛ أو حلقة ثانية تكبر 1→1.9 وتخبو على نبضتين. / Flattened ellipse ring (y×.25) expanding 0→300 px in 500 ms with fade; or a second ring scaling 1→1.9 and fading on beats.

**متى:** حين يريد حلقة صدمة تتسع على الأرض عند ارتطام أو نبضة قلب تتموج على الإيقاع / for a ground shockwave ring on an impact or a heartbeat ripple on the beats

**كيف:** Rendered here (shockwave under the burst). Heartbeat: circle r150 #f5c97a 5 px drawn 1.1 s, ring2 scale 1→1.9, opacity .9→0 in .9 s E.out at the beat times.

**المعاملات:** 0→300 px / 500 ms; heartbeat 1→1.9 in .9 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صدمة · نبض · shockwave · heartbeat · ring · impact · ارتطام · موجة صدمة · نبضة · pulse · ripple

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-67` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-one/projects/whatsapp-motion/projects/success/index.html`
- `kosif-tool/styles/pm-chrisjdimarco-f068db`

#### 7. قدرات قريبة في العائلة

- `SHAPE-65` حلقات مدارية إهليلجية / Orbital ellipse rings & accents (ready)
- `SHAPE-66` انفجار خطوط شعاعي / Radial line burst (proven)
- `SHAPE-68` أشعة شمسية دوارة / Rotating sunburst ground (proven)
- `SHAPE-69` حلقة نقاط تتسع بخطوط شعاعية / Expanding dot ring with radial lines (seen)

### `SHAPE-68` — أشعة شمسية دوارة / Rotating sunburst ground

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 24–36 إسفينًا متناوبًا بلونين متقاربين يدور ببطء خلف العنوان مع تعتيم شعاعي. / 24–36 alternating wedge rays in two close tones rotating slowly behind the title, with radial vignette.

**متى:** حين يريد خلفية أشعة شمسية دوارة بطابع ريترو خلف العنوان / for a retro rotating sunburst background behind a title

**كيف:** conic-gradient repeating wedges or canvas arcs; tone delta ~8% lightness; rotation 3–10°/s. Rendered here (28 wedges, .12 rad/s).

**المعاملات:** 24–36 rays; 3–10°/s; Δ lightness ~8%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أشعة · sunburst · rays · background · retro · خلفية دوارة · ريترو · عنوان · rotating · wedges

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-68` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-deebeeeff-50fcd0`
- `kosif-tool/styles/pm-majin-appsheet-2d3c1a`
- `kosif-tool/styles/pm-allforbigfire-86ff3c`

#### 7. قدرات قريبة في العائلة

- `SHAPE-66` انفجار خطوط شعاعي / Radial line burst (proven)
- `SHAPE-67` حلقة صدمة أرضية ونبض قلب / Shockwave ring & heartbeat ripple (proven)
- `SHAPE-69` حلقة نقاط تتسع بخطوط شعاعية / Expanding dot ring with radial lines (seen)
- `SHAPE-70` نفق مربعات حلزوني / Spiral square tunnel & nested squares (seen)

### `SHAPE-69` — حلقة نقاط تتسع بخطوط شعاعية / Expanding dot ring with radial lines

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط الشعار تتضاعف حول دائرة أكبر (8→24) وخطوط بنفسجية رفيعة تشع خلفها نحو أطراف الكادر. / Logo dots duplicate around a larger circle (8 → 24) while thin violet lines radiate behind toward the frame edges.

**متى:** حين تتضاعف نقاط الشعار حول دائرة أكبر مع خطوط شعاعية خلفها / when logo dots should multiply around a larger circle with radial lines behind

**كيف:** Ring radius 40% width; lines 1.5 px #8a6cff; satellites stagger 30 ms.

**المعاملات:** 8 → 24 dots; ring 40% w

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نقاط · حلقة · dot ring · radial lines · logo · شعار · لوجو · خطوط شعاعية · logo animation · radiate

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-69` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-micheleharmonic-77628e`

#### 7. قدرات قريبة في العائلة

- `SHAPE-67` حلقة صدمة أرضية ونبض قلب / Shockwave ring & heartbeat ripple (proven)
- `SHAPE-68` أشعة شمسية دوارة / Rotating sunburst ground (proven)
- `SHAPE-70` نفق مربعات حلزوني / Spiral square tunnel & nested squares (seen)
- `SHAPE-71` مربع يصير دائرة مع أقمار / Square→circle with satellites & star pop (seen)

### `SHAPE-70` — نفق مربعات حلزوني / Spiral square tunnel & nested squares

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مربعات متداخلة كل منها ×0.9 ومدار 8° بلونين متناوبين، أو 8 مربعات تدور بتأخير 50ms، أو نفق من نسخ الشعار. / Nested squares each ×.9 and rotated 8° in alternating colours, 8 squares rotating with 50 ms delay, or a tunnel of logo outlines.

**متى:** حين يريد نفقًا حلزونيًا من مربعات متداخلة أو نسخ الشعار، مثلًا مع تغيّر السرعة / when nested squares or logo outlines should form a spiral tunnel, e.g. for speed ramps

**كيف:** Loop: scale every copy by 1/.9 per period and wrap; tunnel of outlines with a ticking counter for speed ramps.

**المعاملات:** ×.9, 8° per level; delay 50 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نفق · مربعات · tunnel · spiral · nested · مربعات متداخلة · دوامة · سرعة · zoom loop · logo

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-70` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-zheke-38deff`
- `kosif-tool/styles/pm-safarkhanshuvo-ffd52d`
- `kosif-tool/styles/pm-jasonzhou1993-8595e0/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-68` أشعة شمسية دوارة / Rotating sunburst ground (proven)
- `SHAPE-69` حلقة نقاط تتسع بخطوط شعاعية / Expanding dot ring with radial lines (seen)
- `SHAPE-71` مربع يصير دائرة مع أقمار / Square→circle with satellites & star pop (seen)
- `SHAPE-72` بوابة دوامية ومصباح فرينل / Swirl portal & Fresnel lamp room (seen)

### `SHAPE-71` — مربع يصير دائرة مع أقمار / Square→circle with satellites & star pop

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** border-radius 0→50% مع دوران وثلاث نقاط تدور على حلقة رفيعة، أو نجمة تقفز بـ outBack ونجوم صغيرة حولها. / border-radius 0→50% with rotation while three dots orbit on a thin ring; or a star popping with outBack and small orbiting stars.

**متى:** حين يتحول مربع إلى دائرة وهو يدور مع أقمار حوله أو تقفز نجمة بين نجوم صغيرة / when a square should round into a circle while rotating with orbiting dots, or a star should pop in

**كيف:** Morph 500 ms; orbit 1 rev/s; background polka grid pulses.

**المعاملات:** 500 ms; 1 rev/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أقمار · satellites · star pop · border-radius · مربع لدائرة · نجمة · قفزة · square to circle · orbit

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-71` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-shinskinakamoto-20190b`
- `kosif-tool/styles/pm-stephanlivera-df17a2`

#### 7. قدرات قريبة في العائلة

- `SHAPE-69` حلقة نقاط تتسع بخطوط شعاعية / Expanding dot ring with radial lines (seen)
- `SHAPE-70` نفق مربعات حلزوني / Spiral square tunnel & nested squares (seen)
- `SHAPE-72` بوابة دوامية ومصباح فرينل / Swirl portal & Fresnel lamp room (seen)
- `SHAPE-73` الزخرفة الثمانية من الكود / Islamic eight-point rosette builder (ready)

### `SHAPE-72` — بوابة دوامية ومصباح فرينل / Swirl portal & Fresnel lamp room

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حلقة طارة متوهجة حول قرص ضوضاء ملتوٍ قطبيًا؛ أو شبكة معينات فوق أسطوانة متوهجة بعدسة حلقات تشتعل في 400ms. / Glowing torus ring around a polar-twisted noise disc; or a diamond-pane lattice over a glowing cylinder with a concentric-ellipse lens igniting in ~400 ms.

**متى:** حين يريد بوابة دوامية متوهجة أو غرفة مصباح منارة بعدسة حلقات تشتعل / for a glowing swirl portal or a lighthouse lamp room whose ring lens ignites

**كيف:** Twist: θ += k/(r+ε) before sampling noise; lattice 40 px cells, glow blur 30–60 px, bloom spike on ignition.

**المعاملات:** ignite 400 ms; lattice 40 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بوابة · portal · swirl · fresnel · lighthouse · دوامة · منارة · توهج · glow · torus

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-72` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-ryzoft-4f85bd`
- `kosif-tool/styles/pm-kamstudiolabs-0b0824`

#### 7. قدرات قريبة في العائلة

- `SHAPE-70` نفق مربعات حلزوني / Spiral square tunnel & nested squares (seen)
- `SHAPE-71` مربع يصير دائرة مع أقمار / Square→circle with satellites & star pop (seen)
- `SHAPE-73` الزخرفة الثمانية من الكود / Islamic eight-point rosette builder (ready)
- `SHAPE-74` وردة الفواصل الموسيقية / Interlude rosette (verse template) (ready)

### `SHAPE-73` — الزخرفة الثمانية من الكود / Islamic eight-point rosette builder

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نجمة ثمانية من مربعين مدارين 45° + نجمة 16 رأسًا + دائرة + نجمة داخلية، يُرسم كل جزء بالتتابع وتدور الوردة كلها ببطء. / An eight-point star from two squares at 0/45°, a 16-vertex star, a circle and an inner star, each drawn in sequence while the rosette slowly turns.

**متى:** حين يريد زخرفة إسلامية ثمانية تُرسم قطعة قطعة من الكود وتدور ببطء / when an Islamic eight-point rosette should be drawn piece by piece in code and slowly turn

**كيف:** sq(78,0), sq(78,π/4), star8(120,92), circle r48, star8(30,14); M.drawPath each at .4 + .18i s for 1.3 s, opacity .85; rotate 0→45° over the film; stroke #f6d27a width 3→5 on the key word.

**المعاملات:** draw 1.3 s, stagger .18 s; stroke #f6d27a 3→5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** زخرفة · نجمة ثمانية · خاتم · islamic · rosette · khatam · geometry · زخرفة إسلامية · نجمة · هندسة إسلامية · eight-point star · draw-on

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-73` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-one/projects/thursday-dua-animation/source/index.html`

#### 7. قدرات قريبة في العائلة

- `SHAPE-71` مربع يصير دائرة مع أقمار / Square→circle with satellites & star pop (seen)
- `SHAPE-72` بوابة دوامية ومصباح فرينل / Swirl portal & Fresnel lamp room (seen)
- `SHAPE-74` وردة الفواصل الموسيقية / Interlude rosette (verse template) (ready)
- `SHAPE-75` فوانيس ومسجد ونوافذ / Swaying lanterns & mosque silhouette (ready)

### `SHAPE-74` — وردة الفواصل الموسيقية / Interlude rosette (verse template)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** في الوقفات الطويلة (≥ 4.5 ث) تُرسم وردة ثمانية تتنفس على الإيقاع ثم تنسحب. / During long pauses (≥ 4.5 s) an eight-point rosette is drawn, breathes on the beat, then withdraws.

**متى:** حين يحتاج ملء وقفة طويلة بين الأبيات بوردة ثمانية تتنفس على الإيقاع / when a long pause between verses needs an eight-point rosette breathing on the beat

**كيف:** verse.py writes interludes into verse.json (start = end + .8 s, end = next − .5 s, ≥ 1.5 s); verse.html ROSETTES: two squares at 0/45° + circle .42R #F7F2E8 .7, R 150k, stroke 2.2k accent, rotate 9°/s, beat scale +7%, draw 1.1 s stagger .12.

**المعاملات:** pause ≥ 4.5 s; 9°/s; beat +7%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** وردة · فاصل · interlude · rosette · verse · beat · وقفة · أبيات · قصيدة · pause · breathing

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-74` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-studio/motion/templates/verse.html`
- `kosif-studio/motion/verse.py:258`
- `100-superskills/skills/kosif-montage-motion/templates/verse.html:298`

#### 7. قدرات قريبة في العائلة

- `SHAPE-72` بوابة دوامية ومصباح فرينل / Swirl portal & Fresnel lamp room (seen)
- `SHAPE-73` الزخرفة الثمانية من الكود / Islamic eight-point rosette builder (ready)
- `SHAPE-75` فوانيس ومسجد ونوافذ / Swaying lanterns & mosque silhouette (ready)
- `SHAPE-76` غيمة من دوائر تكبر وتعتم / Circle-cluster cloud that grows and darkens (ready)

### `SHAPE-75` — فوانيس ومسجد ونوافذ / Swaying lanterns & mosque silhouette

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فانوسان من أشكال SVG يتأرجحان كالبندول بتوهج يتنفس، وصورة ظلية لقبة ومئذنتين بنوافذ مقوسة ترتعش. / Two SVG lanterns swinging like pendulums with breathing glow; a dome-and-two-minarets silhouette with softly flickering arched windows.

**متى:** حين يحتاج مشهدًا رمضانيًا أو إسلاميًا بفوانيس تتأرجح وصورة ظلية لمسجد بنوافذ مضيئة / for a Ramadan or Islamic scene with swinging lanterns and a mosque silhouette with lit windows

**كيف:** Lantern: chain line, radial glow r120, cap, hexagon body #ffcf72 .92 stroke #c48a2c, ribs #b07a22; rotation ±3.5° yoyo 2.2/2.5 s (svgOrigin 0 0); glow .7→1 yoyo .96 s. Mosque paths #1d0f2c, ground #140920; 8 windows #ffc768 .55→1 yoyo .9–1.7 s at random offsets (seeded).

**المعاملات:** ±3.5°, 2.2/2.5 s; windows .55→1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** فانوس · مسجد · رمضان · lantern · mosque · islamic · فوانيس · قبة · مئذنة · ramadan · pendulum

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-75` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-one/projects/thursday-dua-animation/source/index.html`

#### 7. قدرات قريبة في العائلة

- `SHAPE-73` الزخرفة الثمانية من الكود / Islamic eight-point rosette builder (ready)
- `SHAPE-74` وردة الفواصل الموسيقية / Interlude rosette (verse template) (ready)
- `SHAPE-76` غيمة من دوائر تكبر وتعتم / Circle-cluster cloud that grows and darkens (ready)
- `SHAPE-77` مكتبة 16 أيقونة متجهة / 16-icon vector hero library (ready)

### `SHAPE-76` — غيمة من دوائر تكبر وتعتم / Circle-cluster cloud that grows and darkens

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** غيوم من خمس دوائر وقاعدة مستديرة تكبر فوق البحر وتنجرف وتعتم قبل المطر ثم تصفو. / Clouds of five circles and a rounded base grow, drift and darken before rain, then lighten.

**متى:** حين يشرح دورة الماء أو الطقس بغيوم تكبر وتعتم قبل المطر ثم تصفو / when explaining the water cycle or weather with clouds that grow and darken before rain

**كيف:** circles (0,0,62) (−75,18,46) (78,18,50) (−32,−34,52) (38,−40,58) + rect 248×58 rx29; scale .2→1 (3.8–5.0 s), drift 4.9–6.2 s; #FFFFFF→#A6B9CC, base #DCE8F2→#8FA3B8 for dark 6.0–6.5 s, back after 8.3 s.

**المعاملات:** 5 circles + base; scale .2→1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** غيمة · cloud · weather · water cycle · explainer · سحاب · مطر · دورة الماء · rain · clouds

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-76` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-one/projects/water-cycle-animation/index.html`

#### 7. قدرات قريبة في العائلة

- `SHAPE-74` وردة الفواصل الموسيقية / Interlude rosette (verse template) (ready)
- `SHAPE-75` فوانيس ومسجد ونوافذ / Swaying lanterns & mosque silhouette (ready)
- `SHAPE-77` مكتبة 16 أيقونة متجهة / 16-icon vector hero library (ready)
- `SHAPE-78` أيقونات SVG حية / Living SVG icons (documented)

### `SHAPE-77` — مكتبة 16 أيقونة متجهة / 16-icon vector hero library

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أيقونات Canvas مرسومة بالكود تصلح أبطالًا: عين، دماغ، محفظة، نقود، شاشة، ساعة رملية، مصباح، صاروخ، ساعة، مؤشر، رسم بياني، درج، دومينو، كتاب، أشخاص، شطرنج + نجمة. / Hand-coded Canvas icons usable as hero objects (eye, brain, wallet, money, screen, hourglass, bulb, rocket, clock, cursor, chart, stairs, domino, book, people, chess + star).

**متى:** حين يحتاج أيقونة بطلة مرسومة بالكود كعين أو دماغ أو صاروخ أو ساعة رملية / when a code-drawn hero icon is needed, such as an eye, brain, rocket or hourglass

**كيف:** icon(ctx, name, r, accent, ink) with round joins, stroke .08r; choose via scene.hero.

**المعاملات:** 16 named + default

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أيقونات · icons · canvas · hero · library · أيقونة · رموز · صاروخ · vector icons · hero object

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-77` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `fastify-motion-bro/web/editorial.js:12-34`

#### 7. قدرات قريبة في العائلة

- `SHAPE-75` فوانيس ومسجد ونوافذ / Swaying lanterns & mosque silhouette (ready)
- `SHAPE-76` غيمة من دوائر تكبر وتعتم / Circle-cluster cloud that grows and darkens (ready)
- `SHAPE-78` أيقونات SVG حية / Living SVG icons (documented)
- `SHAPE-79` قواعد الأيقونة: شبكة 24 والإغلاق / Icon rules: 24 px grid & closure (documented)

### `SHAPE-78` — أيقونات SVG حية / Living SVG icons

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حرّك أجزاء الأيقونة الداخلية: عقارب ساعة، ريش مروحة، نقاط نابضة، خطوط تدفق — بدوران حول مركز دقيق. / Animate inner SVG parts (clock hands, fan blades, pulsing dots, dash-flow lines) with rotate(deg cx cy) for exact centres.

**متى:** حين يريد أيقونة تتحرك أجزاؤها الداخلية كعقارب ساعة أو ريش مروحة أو نقاط نابضة / when an icon's inner parts should animate, like clock hands, fan blades or pulsing dots

**كيف:** setAttribute("transform", `rotate(${d} ${cx} ${cy})`); ease none for linear rotation; one paused timeline, fromTo explicit states.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أيقونة حية · living icon · svg · rotate · clock · أيقونة متحركة · عقارب · مروحة · animated icon · fan

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-78` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/svg-icon-enrichment.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-76` غيمة من دوائر تكبر وتعتم / Circle-cluster cloud that grows and darkens (ready)
- `SHAPE-77` مكتبة 16 أيقونة متجهة / 16-icon vector hero library (ready)
- `SHAPE-79` قواعد الأيقونة: شبكة 24 والإغلاق / Icon rules: 24 px grid & closure (documented)
- `SHAPE-80` طبقات أشكال وملصقات منبثقة / Shape layers & sticker/emoji pop-ups (install)

### `SHAPE-79` — قواعد الأيقونة: شبكة 24 والإغلاق / Icon rules: 24 px grid & closure

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة 24px، خط 2px، نهايات دائرية، viewBox مربع، بلا نص، < 4KB؛ والإيحاء بالشكل بفجوات ونهايات متحاذية — اختبرها في 8–16px. / 24 px grid, 2 px stroke, round caps, square viewBox, no text, < 4 KB; imply forms with gaps and aligned terminals (closure) — test at 8–16 px.

**متى:** عند تصميم أيقونة أو مراجعتها لتبقى واضحة في الأحجام الصغيرة على شبكة 24 / when designing or checking an icon so it reads clearly at small sizes on a 24 px grid

**كيف:** Test at 16/24/48/192 px; draw-on works especially well with closure because the eye completes the form early.

**المعاملات:** 24 px / 2 px; test 8–16 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أيقونة · icon grid · closure · rules · تصميم أيقونة · شبكة · حجم صغير · stroke · small size

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-79` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `100-superskills/skills/svg-illustration-icons/SKILL.md:21`
- `kosif-atlas/skills/1503-universal-design-principles/3812-closure-implied-shapes`

#### 7. قدرات قريبة في العائلة

- `SHAPE-77` مكتبة 16 أيقونة متجهة / 16-icon vector hero library (ready)
- `SHAPE-78` أيقونات SVG حية / Living SVG icons (documented)
- `SHAPE-80` طبقات أشكال وملصقات منبثقة / Shape layers & sticker/emoji pop-ups (install)
- `SHAPE-81` ملصقات زخرفية وكبسولات وسوم / Decor stickers, hazard tape & floating tag pills (seen)

### `SHAPE-80` — طبقات أشكال وملصقات منبثقة / Shape layers & sticker/emoji pop-ups

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** دائرة أو شريط مستدير كخط تحت النص في محرر الاستوديو؛ وإيموجي ونص وملصقات تنبثق بنابض وتمايل في Basma. / Studio overlay shapes (circle or rounded underline bar); Basma emoji/text/sticker pop-ups springing in with a slight wobble.

**متى:** حين يريد إضافة دائرة أو خط تحت النص، أو إيموجي ونص وملصقات تنبثق بنابض / when adding a circle or underline shape, or emoji, text and sticker pop-ups with a spring

**كيف:** Studio: overlay.type="shape", "circle" (arc size/2) or "rectangle" (roundRect h .24·size, r max(2,.06·size)), default 16% #52dbc6. Basma drawOverlays(): spring(z .4, w 17) scale, rotate sin(3l)·.03, .2 s fade-out; positions top 30%, centre 47%, bottom 64%, corner (78%,16%); emoji 17% m; text Lalezar 6.5% on an accent pill.

**المعاملات:** spring z .4 ω 17; size 16%

**التثبيت:** cd app && npm install

**الوسوم:** ملصقات · إيموجي · stickers · emoji · overlay · pop · خط تحت النص · استيكر · دائرة تمييز · underline · wobble

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

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-80` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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
- `app/public/js/00_editor.js:412`

#### 7. قدرات قريبة في العائلة

- `SHAPE-78` أيقونات SVG حية / Living SVG icons (documented)
- `SHAPE-79` قواعد الأيقونة: شبكة 24 والإغلاق / Icon rules: 24 px grid & closure (documented)
- `SHAPE-81` ملصقات زخرفية وكبسولات وسوم / Decor stickers, hazard tape & floating tag pills (seen)
- `SHAPE-82` مروحة بطاقات وصور / Card / photo / swatch fan-out (seen)

### `SHAPE-81` — ملصقات زخرفية وكبسولات وسوم / Decor stickers, hazard tape & floating tag pills

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نجوم مضلعة وشرائط تحذير مخططة في الزوايا تتمايل، وكبسولات وسوم بيضاء تطفو حول العنوان بدوران عشوائي. / Starburst polygons and striped hazard tapes wobbling in corners; white tag pills floating around the headline at random tilts.

**متى:** حين يريد ملصقات زخرفية وشرائط تحذير متمايلة أو وسومًا تطفو حول العنوان / when wobbling starburst stickers, hazard tapes or floating tag pills around a headline are wanted

**كيف:** Stickers rotate ±6° over 2 s yoyo, colours rotate per scene; 6 pills radius 999, 1 px #c4d8e5 border, ±6° tilt, pop-in stagger 120 ms, idle bob 4 px period 3–4 s, avoid the centre.

**المعاملات:** ±6°/2 s; pills stagger 120 ms, bob 4 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ملصقات · كبسولات · stickers · tags · pills · decor · شريط تحذير · وسوم · عنوان · hazard tape · floating

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-81` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-0xnfrith-5be616`
- `kosif-tool/styles/pm-alex-prompter-1ea044`

#### 7. قدرات قريبة في العائلة

- `SHAPE-79` قواعد الأيقونة: شبكة 24 والإغلاق / Icon rules: 24 px grid & closure (documented)
- `SHAPE-80` طبقات أشكال وملصقات منبثقة / Shape layers & sticker/emoji pop-ups (install)
- `SHAPE-82` مروحة بطاقات وصور / Card / photo / swatch fan-out (seen)
- `SHAPE-83` شريط تظليل مائل خلف النص / Slanted highlighter bar wipe (seen)

### `SHAPE-82` — مروحة بطاقات وصور / Card / photo / swatch fan-out

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نسخ البطاقة خلفها تنفتح كمروحة حول محور مشترك بإزاحة ودوران متدرج، مع ألسنة مرقمة أو عداد. / Duplicates behind a card fan out around a shared pivot with offset and stepped rotation, with numbered tabs or a count label.

**متى:** حين يريد مجموعة بطاقات أو صور أو عينات ألوان تنفتح كمروحة من خلف بطاقة / when a stack of cards, photos or colour swatches should fan out from behind one card

**كيف:** 6 cards offset x +18 px and +2..+6° (or ±12–25° around a pivot for photos), stagger 70–80 ms, 400–500 ms easeOutBack(1.2).

**المعاملات:** 5–8 items, stagger 70–80 ms, 400–500 ms back.out

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مروحة · بطاقات · fan · cards · stack · swatches · صور · عينات ألوان · كومة · photos · fan out

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-82` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-bogdandragomir-35e024`
- `kosif-tool/styles/pm-lester-tyy-f897f7`
- `kosif-tool/styles/pm-ercankeskinx-ec2568`

#### 7. قدرات قريبة في العائلة

- `SHAPE-80` طبقات أشكال وملصقات منبثقة / Shape layers & sticker/emoji pop-ups (install)
- `SHAPE-81` ملصقات زخرفية وكبسولات وسوم / Decor stickers, hazard tape & floating tag pills (seen)
- `SHAPE-83` شريط تظليل مائل خلف النص / Slanted highlighter bar wipe (seen)
- `SHAPE-84` تغيير لون الكلمة داخل الكرة / Clip-path colour flip over a moving lens (seen)

### `SHAPE-83` — شريط تظليل مائل خلف النص / Slanted highlighter bar wipe

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مستطيل مائل يكبر أفقيًا من 0 إلى 1 خلف سطر نص، أكبر قليلًا من صندوقه. / A skewed rectangle scales X from 0 to 1 behind a text line, slightly larger than the text box.

**متى:** حين يريد إبراز سطر نص بشريط تظليل مائل يمتد خلفه، ومن اليمين للعربي / when a text line needs a slanted highlighter bar sweeping in behind it, from the right for Arabic

**كيف:** skewX −8°, 180–250 ms easeOutCubic; for Arabic grow from the right (transform-origin right).

**المعاملات:** skewX −8°, 180–250 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تظليل · highlighter · bar · emphasis · text · إبراز · ماركر · خلفية النص · highlight · marker

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-83` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-deifosv-04e4d3`

#### 7. قدرات قريبة في العائلة

- `SHAPE-81` ملصقات زخرفية وكبسولات وسوم / Decor stickers, hazard tape & floating tag pills (seen)
- `SHAPE-82` مروحة بطاقات وصور / Card / photo / swatch fan-out (seen)
- `SHAPE-84` تغيير لون الكلمة داخل الكرة / Clip-path colour flip over a moving lens (seen)
- `SHAPE-85` تجميع من شظايا أو قطع / Shard / piece assembly along a path (seen)

### `SHAPE-84` — تغيير لون الكلمة داخل الكرة / Clip-path colour flip over a moving lens

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صف كلمات مرسوم مرتين: نسخة داكنة، ونسخة بيضاء مقصوصة بدائرة الكرة، والصف ينزلق فتتلون كل كلمة حين تعبرها. / Render a word row twice — dark copy, and a white copy clipped with clip-path: circle() at the orb — and slide the row so each word flips inside the orb.

**متى:** حين يريد صف كلمات ينزلق فيتغير لون كل كلمة عند مرورها داخل دائرة كالعدسة / when a sliding row of words should flip colour as each passes inside a circle lens

**كيف:** orb r ~70 px; row speed ~1 word / .8 s; for Arabic slide left→right so words enter from the right.

**المعاملات:** orb r 70 px; 0.8 s per word

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قص · clip-path · lens · colour flip · words · تغيير اللون · عدسة · كرة · orb · text

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-84` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/product`

#### 7. قدرات قريبة في العائلة

- `SHAPE-82` مروحة بطاقات وصور / Card / photo / swatch fan-out (seen)
- `SHAPE-83` شريط تظليل مائل خلف النص / Slanted highlighter bar wipe (seen)
- `SHAPE-85` تجميع من شظايا أو قطع / Shard / piece assembly along a path (seen)
- `SHAPE-86` شاشة مقسومة واستعارة الكسوف / Split-screen eclipse metaphor (seen)

### `SHAPE-85` — تجميع من شظايا أو قطع / Shard / piece assembly along a path

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مثلثات تبدأ خارج الشاشة مدارة وتنزلق إلى أماكنها، أو قطع هيكل تسافر على قوس منقط وتلتحم بتجاوز بسيط. / Triangles start off-screen rotated and ease into slots; or skeleton pieces travel along a dotted arc and snap together with slight overshoot.

**متى:** حين يريد قطعًا أو شظايا تأتي من خارج الشاشة وتلتحم في أماكنها لبناء شكل / when shards or pieces should fly in from off-screen and snap together into a shape

**كيف:** Per piece: start = random off-screen pose (seeded), path = quadratic arc, 600 ms ease-out, stagger 40 ms, total ~1.2 s.

**المعاملات:** stagger 40 ms; 600 ms each

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شظايا · تجميع · shards · assemble · snap · قطع · التحام · بناء · pieces · fly in

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-85` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-tdinh-me-815acb`
- `kosif-tool/styles/pm-gigabit-million-16b3a0`

#### 7. قدرات قريبة في العائلة

- `SHAPE-83` شريط تظليل مائل خلف النص / Slanted highlighter bar wipe (seen)
- `SHAPE-84` تغيير لون الكلمة داخل الكرة / Clip-path colour flip over a moving lens (seen)
- `SHAPE-86` شاشة مقسومة واستعارة الكسوف / Split-screen eclipse metaphor (seen)
- `SHAPE-87` بحر خطوط مع شخصية رمزية / Line-art sea with mascot (seen)

### `SHAPE-86` — شاشة مقسومة واستعارة الكسوف / Split-screen eclipse metaphor

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نصف كريمي ونصف أسود: دائرة مفرغة في جهة ونقطة حمراء في الأخرى تنزلقان وتتداخلان ككسوف. / Half cream / half black; an outline circle and a filled red dot slide toward each other and overlap into an eclipse.

**متى:** حين يريد استعارة بصرية على شاشة مقسومة نصفين تنزلق فيها دائرتان وتتداخلان ككسوف / for a split-screen metaphor where two circles slide together and overlap like an eclipse

**كيف:** ~1.5 s ease-in-out; difference blend at the overlap.

**المعاملات:** ~1.5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كسوف · eclipse · split screen · metaphor · شاشة مقسومة · تداخل · استعارة بصرية · overlap · difference blend

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-86` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-samaote-5e2fc2`

#### 7. قدرات قريبة في العائلة

- `SHAPE-84` تغيير لون الكلمة داخل الكرة / Clip-path colour flip over a moving lens (seen)
- `SHAPE-85` تجميع من شظايا أو قطع / Shard / piece assembly along a path (seen)
- `SHAPE-87` بحر خطوط مع شخصية رمزية / Line-art sea with mascot (seen)
- `SHAPE-88` فاصل بشعرة / Hairline separator (HyperFrames) (install)

### `SHAPE-87` — بحر خطوط مع شخصية رمزية / Line-art sea with mascot

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 4–6 مسارات جيبية أفقية بانجراف طور وسرعات بارالاكس، وشخصية مسطحة صغيرة تتمايل وتعبر. / 4–6 horizontal SVG sine paths with slow phase drift at parallax speeds; a small flat mascot bobs (±4°) and crosses.

**متى:** حين يريد بحرًا مرسومًا بخطوط موجية متحركة تعبره شخصية رمزية صغيرة / when a line-art sea of drifting waves should be crossed by a small bobbing mascot

**كيف:** Wave amplitude 4–10 px, period 6 s; bob 1.5 s; a passing train/vehicle strip with 30 px motion blur for fast occlusion.

**المعاملات:** amp 4–10 px, 6 s; bob ±4°/1.5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بحر · خطوط · sea · mascot · line art · موج · شخصية · تمايل · waves · parallax

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-87` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-aschapmann-131210`
- `kosif-tool/styles/pm-itsolelehmann-e47532`

#### 7. قدرات قريبة في العائلة

- `SHAPE-85` تجميع من شظايا أو قطع / Shard / piece assembly along a path (seen)
- `SHAPE-86` شاشة مقسومة واستعارة الكسوف / Split-screen eclipse metaphor (seen)
- `SHAPE-88` فاصل بشعرة / Hairline separator (HyperFrames) (install)
- `SHAPE-89` وحدة 24 وشبكة أعمدة / Base-unit grid system (documented)

### `SHAPE-88` — فاصل بشعرة / Hairline separator (HyperFrames)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0. |

**ما هي:** فاصل 1px أفقي أو عمودي بكشف تقدمي آمن للبحث. / 1-pixel structural separator with a seek-safe progress reveal.

**متى:** حين يحتاج فاصلًا رفيعًا أفقيًا أو عموديًا يظهر تدريجيًا في تخطيط HyperFrames / when a thin horizontal or vertical divider with a progressive reveal is needed in HyperFrames

**كيف:** npx hyperframes add separator; orientation horizontal\|vertical; thickness hairline\|medium\|bold; tone neutral\|accent\|warning.

**التثبيت:** npx hyperframes add separator

**الوسوم:** فاصل · separator · hairline · layout · خط فاصل · تقسيم · خط رفيع · divider · line reveal

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-88` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-one/vendor/hyperframes/registry/components/separator/separator.html`

#### 7. قدرات قريبة في العائلة

- `SHAPE-86` شاشة مقسومة واستعارة الكسوف / Split-screen eclipse metaphor (seen)
- `SHAPE-87` بحر خطوط مع شخصية رمزية / Line-art sea with mascot (seen)
- `SHAPE-89` وحدة 24 وشبكة أعمدة / Base-unit grid system (documented)
- `SHAPE-90` سلالم الأقطار والخطوط والفراغ / Primitive, radius & stroke scales (documented)

### `SHAPE-89` — وحدة 24 وشبكة أعمدة / Base-unit grid system

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل المقاسات مضاعفات وحدة أساس على شبكة أعمدة، والإطار الأخير يستقر على الشبكة تمامًا. / All sizes multiples of a base unit on a column grid; final frames land exactly on grid.

**متى:** عند ضبط المقاسات والمسافات على وحدة أساس وشبكة أعمدة لتستقر الإطارات بدقة / when sizes and spacing must follow a base unit and column grid so final frames land on grid

**كيف:** unit 24 px; 8 or 12 columns; snap end states, not in-betweens.

**المعاملات:** 24 px; 8/12 columns

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شبكة · وحدة · grid · unit · system · مسافات · أعمدة · تخطيط · columns · spacing

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-89` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/playbooks/shapes.md:15`
- `kosif-tool/playbooks/shapes.md:29`

#### 7. قدرات قريبة في العائلة

- `SHAPE-87` بحر خطوط مع شخصية رمزية / Line-art sea with mascot (seen)
- `SHAPE-88` فاصل بشعرة / Hairline separator (HyperFrames) (install)
- `SHAPE-90` سلالم الأقطار والخطوط والفراغ / Primitive, radius & stroke scales (documented)
- `SHAPE-91` انضغاط وتمدد بحفظ المساحة / Area-preserving squash & stretch (ready)

### `SHAPE-90` — سلالم الأقطار والخطوط والفراغ / Primitive, radius & stroke scales

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاثة أشكال أولية كحد أقصى، لونان + خلفية، أقطار 0/8/24/50%، خطوط 2/4/8، وفراغ سلبي ≥ 30%. / Max three primitives, two colours + background, radii 0/8/24/50%, strokes 2/4/8, ≥ 30% negative space.

**متى:** عند وضع حدود للأشكال والألوان والزوايا والخطوط والفراغ في تصميم هندسي / when setting limits for primitives, colours, corner radii, strokes and empty space in a geometric design

**كيف:** Nested radius: inner = outer − gap when gap < 32 px and result > 2 (16 px outer, 8 px gap → 8 px).

**المعاملات:** radii 0/8/24/50%; strokes 2/4/8; ≥ 30% empty

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سلالم · radius · stroke · negative space · rules · زوايا مستديرة · فراغ · قواعد التصميم · corner radius · design rules

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-90` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/playbooks/shapes.md:16-18`
- `kosif-one/vendor/ai-design-skills/skills/landing-page-design/SKILL.md:225`

#### 7. قدرات قريبة في العائلة

- `SHAPE-88` فاصل بشعرة / Hairline separator (HyperFrames) (install)
- `SHAPE-89` وحدة 24 وشبكة أعمدة / Base-unit grid system (documented)
- `SHAPE-91` انضغاط وتمدد بحفظ المساحة / Area-preserving squash & stretch (ready)
- `SHAPE-92` التصاق مغناطيسي وكل شيء من المركز / Magnet snap spring & centre-origin rule (idea)

### `SHAPE-91` — انضغاط وتمدد بحفظ المساحة / Area-preserving squash & stretch

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عند الاصطدام ينضغط الشكل (0.7/1.3) 80ms حول نقطة التلامس ثم يعود بنابض. / On impact squash (scaleY .7 / scaleX 1.3) for 80 ms around the contact point, then spring back.

**متى:** حين يرتطم شكل بشيء فينضغط ويتمدد حول نقطة التلامس ثم يعود بنابض / when a shape hits something and should squash and stretch around the contact point, then spring back

**كيف:** Canvas: ctx.scale(1 + .3s, 1 − .3s) about the contact; s = KOSIF.window01(t, hit, hit + .08, .02, .06) in the html-canvas starter; spring {damping 10, stiffness 220}.

**المعاملات:** .7/1.3 for 80 ms; spring d10 k220

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** انضغاط · squash · stretch · impact · spring · ارتطام · ارتداد · مرونة · bounce · contact point

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-91` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/playbooks/shapes.md:25`
- `kosif-tool/playbooks/shapes.md:66`
- `kosif-tool/starters/html-canvas/index.html`

#### 7. قدرات قريبة في العائلة

- `SHAPE-89` وحدة 24 وشبكة أعمدة / Base-unit grid system (documented)
- `SHAPE-90` سلالم الأقطار والخطوط والفراغ / Primitive, radius & stroke scales (documented)
- `SHAPE-92` التصاق مغناطيسي وكل شيء من المركز / Magnet snap spring & centre-origin rule (idea)
- `SHAPE-93` أسلوب المرح الهندسي (S07) / Playful geometric style (S07) (documented)

### `SHAPE-92` — التصاق مغناطيسي وكل شيء من المركز / Magnet snap spring & centre-origin rule

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الأشكال تلتصق في أماكنها بتجاوز واحد؛ وفي بعض الأساليب كل التحويلات حول مركز الإطار وكل دخول منه. / Primitives snap into place with one overshoot; in some styles every transform pivots on the frame centre and every entrance starts there.

**متى:** حين يريد أشكالًا تلتصق في أماكنها بتجاوز واحد أو أسلوبًا تبدأ فيه كل الحركات من مركز الإطار / when shapes should snap into place with one overshoot, or every move should pivot from the frame centre

**كيف:** Untested brief ideas: Remotion spring stiffness 220 damping 14, or UI cubic-bezier(.16,1,.3,1) 400–600 ms; transform-origin 960px 540px.

**المعاملات:** k 220 d 14; origin (960,540)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مغناطيس · snap · spring · centre origin · rule · التصاق · تجاوز · مركز الكادر · overshoot · magnet

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-92` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-tool/styles/pm-quickdesignio-dd93d0/BRIEF.md`
- `kosif-tool/styles/pm-marouanegazouzi-6071d5/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-90` سلالم الأقطار والخطوط والفراغ / Primitive, radius & stroke scales (documented)
- `SHAPE-91` انضغاط وتمدد بحفظ المساحة / Area-preserving squash & stretch (ready)
- `SHAPE-93` أسلوب المرح الهندسي (S07) / Playful geometric style (S07) (documented)
- `SHAPE-G01` رقم متحرك واحد يقود كل الأشكال / One animated value drives every dependent shape (documented)

### `SHAPE-93` — أسلوب المرح الهندسي (S07) / Playful geometric style (S07)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لوحة محدودة جريئة، دوائر وبطاقات وأيقونات، قفزات صغيرة وتبديل أشكال وإيقاع متنوع — حي من أصول بسيطة. / Limited bold palette, circles, cards and icons; small bounces, shape swaps, varied rhythm.

**متى:** حين يطلب أسلوبًا مرحًا هندسيًا بألوان جريئة ودوائر وبطاقات وأيقونات تقفز / for a playful geometric style with a bold palette and bouncing circles, cards and icons

**كيف:** SVG primitives + overshoot easings + staggered entrances, rendered with render_html.cjs; over-bouncing distracts — one overshoot per entrance.

**المعاملات:** ideas MG-008 MG-029 MG-061 MG-081 MG-083 MG-108 MG-115

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مرح · هندسي · playful · geometric · style · ألوان جريئة · دوائر · حيوي · bold palette · bounce

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-93` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`
- `kosif-tool/playbooks/shapes.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-91` انضغاط وتمدد بحفظ المساحة / Area-preserving squash & stretch (ready)
- `SHAPE-92` التصاق مغناطيسي وكل شيء من المركز / Magnet snap spring & centre-origin rule (idea)
- `SHAPE-G01` رقم متحرك واحد يقود كل الأشكال / One animated value drives every dependent shape (documented)
- `SHAPE-G02` تحويل يطابق الأجزاء المشتركة / Morph that matches shared parts (documented)

### `SHAPE-G01` — رقم متحرك واحد يقود كل الأشكال / One animated value drives every dependent shape

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** حرّك قيمة واحدة (متتبع) واجعل كل شكل يعتمد عليها يُعاد رسمه من دالة في كل إطار، بدل تحريك كل شكل وحده. — Animate one value (a tracker) and redraw every dependent shape from a function of it each frame, instead of animating each shape alone.

**متى:** رسوم شرح فيها نقطة على منحنى، أو عداد وأعمدة، أو زاوية ومثلث / explainers with a dot on a curve, a counter and bars, or an angle and a triangle

**كيف:** Manim pattern: ValueTracker t → always_redraw(lambda: Dot(axes.c2p(t, f(t)))) plus a label and a tangent from the same t; then animate only t. In HTML: one state value, every element computed in render(t). Dependencies can never drift apart, and seeking any frame is exact.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** manim · valuetracker · updater · always_redraw · dependent animation · متتبع · رسوم شرح · إعادة رسم

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-G01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `SHAPE-92` التصاق مغناطيسي وكل شيء من المركز / Magnet snap spring & centre-origin rule (idea)
- `SHAPE-93` أسلوب المرح الهندسي (S07) / Playful geometric style (S07) (documented)
- `SHAPE-G02` تحويل يطابق الأجزاء المشتركة / Morph that matches shared parts (documented)
- `SHAPE-X01` تحوّل هندسي بلا مزج / Geometric morph without a crossfade (letter → planet) (documented)

### `SHAPE-G02` — تحويل يطابق الأجزاء المشتركة / Morph that matches shared parts

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** عند تحويل معادلة أو نص أو شكل إلى آخر، أبقِ الأجزاء المتطابقة في مكانها وحرّكها، وحوّل المختلف فقط، بدل ذوبان كل شيء في كل شيء. — When morphing one equation, text or shape into another, keep matching parts and move them, morph only what differs, instead of melting everything into everything.

**متى:** خطوات حل معادلة، تغيير كلمة في عنوان، تطور شعار / equation steps, swapping a word in a title, logo evolution

**كيف:** Split both states into parts with stable keys (tokens, glyphs, sub-paths); matched keys tween position/scale; unmatched old parts fade or shrink out, new ones fade or grow in; order point lists before a path morph so vertices pair by position. Manim: TransformMatchingTex / TransformMatchingShapes; ReplacementTransform when the target object replaces the source in the scene.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** morph · transform matching · equation animation · manim · تحويل · معادلة · تطابق

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-G02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `SHAPE-93` أسلوب المرح الهندسي (S07) / Playful geometric style (S07) (documented)
- `SHAPE-G01` رقم متحرك واحد يقود كل الأشكال / One animated value drives every dependent shape (documented)
- `SHAPE-X01` تحوّل هندسي بلا مزج / Geometric morph without a crossfade (letter → planet) (documented)
- `SHAPE-X02` لقطة متصلة من عناصر مشتركة / One continuous shot from shared elements (documented)

### `SHAPE-X01` — تحوّل هندسي بلا مزج / Geometric morph without a crossfade (letter → planet)

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner (no LICENSE file) |

**ما هي:** حوّل شكلًا إلى آخر عبر سلسلة أشكال وسيطة تحمل النقاط نفسها، لا بمزج صورتين. — Turn one shape into another through a chain of intermediate shapes carrying the same points, never by crossfading two images.

**متى:** حرف من الشعار يصبح كوكبًا أو كرة أو أيقونة — a logo letter becoming a planet, sphere or icon.

**كيف:** Letter O → ellipse → 3D ring → 6 meridian copies → wire sphere → dotted Earth: map source points onto each stage, depth-sort, draw the back half at α 0.3.

**المعاملات:** 6 meridians; back half α 0.3

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** morph · letter · sphere · points · تحوّل · كرة · نقاط

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-X01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-G01` رقم متحرك واحد يقود كل الأشكال / One animated value drives every dependent shape (documented)
- `SHAPE-G02` تحويل يطابق الأجزاء المشتركة / Morph that matches shared parts (documented)
- `SHAPE-X02` لقطة متصلة من عناصر مشتركة / One continuous shot from shared elements (documented)

### `SHAPE-X02` — لقطة متصلة من عناصر مشتركة / One continuous shot from shared elements

| الحقل | القيمة |
|---|---|
| العائلة | `shapes-morph-geometry` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/shapes-morph-geometry.md)) |
| المجموعة | الرسم والأشكال والتصميم (`drawing`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner (no LICENSE file) |

**ما هي:** العناصر نفسها تعيد ترتيب نفسها من شكل إلى آخر (مروحة ثم رسم بياني ثم حلقة) فتصنع فيلمًا بلا قطع. — The same elements rearrange from one formation to the next (fan, then graph, then ring), making a film with no cuts.

**متى:** فيلم بيانات أو منتج بلا قطع — a data or product film without cuts.

**كيف:** 28 tiles with pose functions fan → graph → ring; greedy nearest assignment between formations; ring slots sorted by angle so paths never cross; stagger 0.014–0.02 s; pinhole projection f 1500.

**المعاملات:** 28 tiles; stagger 0.014–0.02 s; f 1500

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** formation · continuous shot · tiles · assignment · تشكيل · لقطة متصلة

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:SHAPE-X02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
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

- `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`

#### 7. قدرات قريبة في العائلة

- `SHAPE-G02` تحويل يطابق الأجزاء المشتركة / Morph that matches shared parts (documented)
- `SHAPE-X01` تحوّل هندسي بلا مزج / Geometric morph without a crossfade (letter → planet) (documented)

