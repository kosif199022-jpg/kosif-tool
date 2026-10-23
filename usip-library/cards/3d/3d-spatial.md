# `3d-spatial` — الثري دي والمحاكاة والرندر (53 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/3d-spatial.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/3d.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`3D-01` متى يكون 3D مبررًا](#3d-01--متى-يكون-3d-مبررًا--real-3d-vs-25d-decision)
- [`3D-02` منصة العمق 2.5D](#3d-02--منصة-العمق-25d--25d-css-depth-rig)
- [`3D-03` صورة ثابتة بعمق طبقات](#3d-03--صورة-ثابتة-بعمق-طبقات--still-photo-with-layered-depth)
- [`3D-04` جسم ذهبي بسماكة مزيفة](#3d-04--جسم-ذهبي-بسماكة-مزيفة--fake-3d-extrusion--parallel-projection)
- [`3D-05` العالم الأيزومتري](#3d-05--العالم-الأيزومتري--isometric-worlds)
- [`3D-06` حقول المكعبات المتموجة](#3d-06--حقول-المكعبات-المتموجة--cube-heightfield-waves--voxel-ripples)
- [`3D-07` جدران البطاقات المائلة](#3d-07--جدران-البطاقات-المائلة--tilted-card--screenshot-walls)
- [`3D-08` تحويلات البطاقات ثلاثية الأبعاد بالـCSS](#3d-08--تحويلات-البطاقات-ثلاثية-الأبعاد-بالـcss--css-3d-card-transforms)
- [`3D-09` طيران الكاميرا في عالم CSS](#3d-09--طيران-الكاميرا-في-عالم-css--css-3d-camera-flight--depth-scatter)
- [`3D-10` الأرضيات الشبكية والخريطة المائلة](#3d-10--الأرضيات-الشبكية-والخريطة-المائلة--perspective-grid-floors--tilted-planes)
- [`3D-11` حلقات مدارية مائلة ورفع العقد](#3d-11--حلقات-مدارية-مائلة-ورفع-العقد--pseudo-3d-orbit-rings--hover-lift)
- [`3D-12` الأنفاق](#3d-12--الأنفاق--tunnels)
- [`3D-13` مكونات HyperFrames ثلاثية الأبعاد](#3d-13--مكونات-hyperframes-ثلاثية-الأبعاد--hyperframes-3d-components--blocks)
- [`3D-14` مشروع three-kit ثلاثي الأبعاد](#3d-14--مشروع-three-kit-ثلاثي-الأبعاد--kosif-three-kit-3d-project)
- [`3D-15` عقد مشهد Three.js الحتمي](#3d-15--عقد-مشهد-threejs-الحتمي--deterministic-threejs-seek-scene)
- [`3D-16` ثلاثي الأبعاد في Remotion](#3d-16--ثلاثي-الأبعاد-في-remotion--remotion-threecanvas)
- [`3D-17` بوابات ومشهد داخل مشهد](#3d-17--بوابات-ومشهد-داخل-مشهد--portals--render-to-texture)
- [`3D-18` عالم البلورات بـ WebGL خام](#3d-18--عالم-البلورات-بـ-webgl-خام--raw-webgl-procedural-crystal-shards)
- [`3D-19` 3D مرسوم برمجيًا على Canvas](#3d-19--3d-مرسوم-برمجيًا-على-canvas--software-rendered-3d-on-canvas)
- [`3D-20` كرات وحلقات من النقاط](#3d-20--كرات-وحلقات-من-النقاط--point-spheres-particle-tori--dot-globes)
- [`3D-21` الرسم بالأشعة ودوال المسافة](#3d-21--الرسم-بالأشعة-ودوال-المسافة--raymarched-sdf-scenes)
- [`3D-22` نماذج GLB بحركة مضبوطة على الزمن](#3d-22--نماذج-glb-بحركة-مضبوطة-على-الزمن--glb-models-with-seeked-animation)
- [`3D-23` Blender بلا واجهة](#3d-23--blender-بلا-واجهة--headless-blender-bpy)
- [`3D-24` تحليق Cesium فوق تضاريس ومدن حقيقية](#3d-24--تحليق-cesium-فوق-تضاريس-ومدن-حقيقية--cesium-terrain--city-flyovers)
- [`3D-25` تضاريس إجرائية](#3d-25--تضاريس-إجرائية--procedural-terrain)
- [`3D-26` غابة صنوبر بالمثيلات](#3d-26--غابة-صنوبر-بالمثيلات--instanced-conifer-forest)
- [`3D-27` السماء والشمس والإضاءة البيئية](#3d-27--السماء-والشمس-والإضاءة-البيئية--sky-sun--gradient-ibl)
- [`3D-28` البحر والماء](#3d-28--البحر-والماء--sea--water-surfaces)
- [`3D-29` السحب](#3d-29--السحب--clouds)
- [`3D-30` بركة الكوي والعشب والتفاصيل الحية](#3d-30--بركة-الكوي-والعشب-والتفاصيل-الحية--koi-pond-reeds--living-details)
- [`3D-31` مؤشرات المقياس: جبال وطريق وأضواء بعيدة](#3d-31--مؤشرات-المقياس-جبال-وطريق-وأضواء-بعيدة--scale-cues-ridge-layers-road-ribbon-far-lights)
- [`3D-32` بدن قارب بمعادلات](#3d-32--بدن-قارب-بمعادلات--parametric-lofted-boat-hull)
- [`3D-33` مدينة المستقبل: نوافذ وطاقة وعمارة](#3d-33--مدينة-المستقبل-نوافذ-وطاقة-وعمارة--future-city-kit-windows-solar-fields-architecture)
- [`3D-34` مركبات ودعائم من أشكال أولية](#3d-34--مركبات-ودعائم-من-أشكال-أولية--props--vehicles-from-primitives)
- [`3D-35` مناورات طيران على مسار](#3d-35--مناورات-طيران-على-مسار--aircraft-spline-manoeuvres--chase-cam)
- [`3D-36` وصفة الإضاءة السينمائية](#3d-36--وصفة-الإضاءة-السينمائية--cinematic-3d-lighting-recipe)
- [`3D-37` المواد الفيزيائية](#3d-37--المواد-الفيزيائية--physical-materials-glass-chrome-wet-iridescent)
- [`3D-38` سلسلة ما بعد المعالجة](#3d-38--سلسلة-ما-بعد-المعالجة--post-stack-bloom-aces-film)
- [`3D-39` استوديو المنتج الكريمي](#3d-39--استوديو-المنتج-الكريمي--studio-sweep-backdrop--stage-disc)
- [`3D-40` مجسمات بطل جاهزة](#3d-40--مجسمات-بطل-جاهزة--hero-objects-geode-knot-coin)
- [`3D-41` مشهد سينمائي بإطار واحد](#3d-41--مشهد-سينمائي-بإطار-واحد--cinematic-single-frame-3d-page-recipe)
- [`3D-42` نحت SDF وشبكة الأسطح](#3d-42--نحت-sdf-وشبكة-الأسطح--sdf-sculpting--surface-nets-mesher)
- [`3D-43` حركات الكاميرا على مسار](#3d-43--حركات-الكاميرا-على-مسار--spline-camera-moves--narrated-fly-throughs)
- [`3D-44` المنصة الدوارة للمنتج](#3d-44--المنصة-الدوارة-للمنتج--product-turntable-recipe)
- [`3D-45` المنظر المفكك](#3d-45--المنظر-المفكك--exploded-view)
- [`3D-46` سيارة مفككة بالتوليد](#3d-46--سيارة-مفككة-بالتوليد--generated-car-exploded-view-pipeline)
- [`3D-47` المقاطع العرضية ومشاهد التضاريس العلمية](#3d-47--المقاطع-العرضية-ومشاهد-التضاريس-العلمية--cutaways--honest-terrain-science-scenes)
- [`3D-48` عنصر واحد يحمل القصة](#3d-48--عنصر-واحد-يحمل-القصة--persistent-subject-across-chapters)
- [`3D-49` النص داخل المشهد ثلاثي الأبعاد](#3d-49--النص-داخل-المشهد-ثلاثي-الأبعاد--type-in-3d-space)
- [`3D-50` أزرار وأجهزة ثلاثية الأبعاد](#3d-50--أزرار-وأجهزة-ثلاثية-الأبعاد--3d-product-interactions-button-lid)
- [`3D-51` الأرض يرسمها الصوت](#3d-51--الأرض-يرسمها-الصوت--music-driven-3d-land)
- [`3D-52` أفكار ثلاثية الأبعاد غير منفذة](#3d-52--أفكار-ثلاثية-الأبعاد-غير-منفذة--unbuilt-3d-ideas)
- [`3D-G01` حلقة رندر three.js حتمية](#3d-g01--حلقة-رندر-threejs-حتمية--deterministic-threejs-render-loop)

## البطاقات / cards

### `3D-01` — متى يكون 3D مبررًا / Real 3D vs 2.5D decision

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** استخدم 3D الحقيقي فقط حين يجب أن تدور الكاميرا حول الأشياء أو تعبر خلالها، أو حين يكشف العمق أو التضاريس أو الحجب بنية يخفيها 2D؛ وإلا فالعمق المزيف بطبقات أفضل. / True 3D only when the camera must travel around/through objects or depth reveals structure; otherwise fake depth with layers.

**متى:** أول قرار في أي فكرة «ثلاثية» / the first call on any '3D' idea.

**كيف:** decide in PLAN.md: turntables, fly-throughs, worlds, point clouds, terrain, trajectories, globes → Three.js seek scene or @remotion/three; everything else → DOM/Canvas layers at depth factors (3D-02); orthographic for chart-like 2.5D, perspective only when depth cues matter; every 3D shot needs static key frames that still prove the claim; one photo has no back side — real 3D needs a model.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** 3D decision · 2.5D · depth · متى 3D

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/playbooks/3d.md:9`
- `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/when-3d-is-justified.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### 7. قدرات قريبة في العائلة

- `3D-02` منصة العمق 2.5D / 2.5D CSS depth rig (ready)
- `3D-03` صورة ثابتة بعمق طبقات / Still photo with layered depth (documented)

### `3D-02` — منصة العمق 2.5D / 2.5D CSS depth rig

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طبقات بمنظور وtranslateZ مع تكبير مسبق يعادل البعد، ودورانات صغيرة فقط / عمق مقنع في لقطة واحدة متصلة. — Perspective + translateZ per layer with pre-scale and small rotations.

**متى:** صور، بطاقات، ملصقات، عناوين بعمق / photos, cards, posters, titles with depth.

**كيف:** parent perspective 1200px, transform-style preserve-3d; layers bg −400, mid −120, subject 0, occluder +200, each pre-scaled by (1200 − z)/1200 so it fills the frame; rotateY ≤ 6°, rotateX ≤ 4°; 8° orbit over 2000–3000 ms sine; orbit card −4° → +4° with a foreground occluder passing, caption pill spring (16/140), settle +2° and push 1.04. Real depth needs a perspective parent, preserve-3d, z travel, rotation and occlusion — scale alone is fake. fake3d style: python3 tools/kosif.py scaffold fake3d <dir>.

**المعاملات:** perspective 1200; z −400/−120/0/+200; ≤6°/4°

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** 2.5D · parallax · perspective · translateZ · عمق

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/playbooks/photos.md:36`
- `kosif-tool/playbooks/photos.md:86`
- `kosif-tool/styles/fake3d/SKILL.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `3D-01` متى يكون 3D مبررًا / Real 3D vs 2.5D decision (documented)
- `3D-03` صورة ثابتة بعمق طبقات / Still photo with layered depth (documented)
- `3D-04` جسم ذهبي بسماكة مزيفة / Fake-3D extrusion & parallel projection (ready)

### `3D-03` — صورة ثابتة بعمق طبقات / Still photo with layered depth

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** المقدمة والموضوع والخلفية لصورة أرشيفية تتحرك بسرعات مختلفة أثناء اقتراب بطيء. / Foreground, subject and background of a still move at different rates during a slow push.

**متى:** صور تاريخية، ألبومات، وثائقي / archive photos, documentaries.

**كيف:** MG-056: 0–1 s hold, 1–6 s depth move, 6–8 s stop; cut the photo into 3 layers from a depth map (Z ≈ 0.45 … 1.22), inpaint the gaps, scale each layer by camera^Z; large moves reveal missing pixels — stay inside cut boundaries or inpaint; keep one pixel density across layers.

**المعاملات:** 8 s; Z 0.45–1.22

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** photo parallax · depth map · 2.5D photo · صورة بعمق

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md`
- `kosif-tool/styles/pm-koldo2k-5cff87`
- `kosif-atlas/skills/1526-gamegen/4175-game-world-building/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `3D-01` متى يكون 3D مبررًا / Real 3D vs 2.5D decision (documented)
- `3D-02` منصة العمق 2.5D / 2.5D CSS depth rig (ready)
- `3D-04` جسم ذهبي بسماكة مزيفة / Fake-3D extrusion & parallel projection (ready)
- `3D-05` العالم الأيزومتري / Isometric worlds (ready)

### `3D-04` — جسم ذهبي بسماكة مزيفة / Fake-3D extrusion & parallel projection

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جسم مسطح ذهبي بسماكة حقيقية المظهر يدور في لقطة واحدة وينتهي على ملصق: الشكل يُرسم N مرة مزاحًا على العمودي ويُسقط بمصفوفة واحدة. / A flat golden object with apparent thickness turns in one shot.

**متى:** شعارات ورموز بلا WebGL / logos and emblems without WebGL.

**كيف:** draw the same path N times offset along the projected face normal from back to front, darker toward the back (N = screen thickness / 1.5 px; gold #fff1bc → #f5b54a → #b4641a), top layer = lit face with gradient; rotate the object's u,v axes in 3D, project, and apply transform='matrix(ux,uy,vx,vy,cx,cy)' to the flat path, flipping to the back colour when facing away. Basma STY.fake3d: 16:9, calm, 1.9 wps, Alexandria, ink #2A1441, wall #EFE7DA, +2.4 s poster tail. Build sequence: outline draw-on 0.6 s → face fill 0.3 s → extrusion 0.5 s from a sparkle (DRAW-04).

**المعاملات:** layer step 1.5 px; poster +2.4 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** fake 3D · extrusion · matrix projection · gold · سماكة

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `app/public/js/10_studio.js:655`
- `kosif-tool/styles/fake3d`
- `kosif-tool/styles/fake3d/STYLE.json`

#### 7. قدرات قريبة في العائلة

- `3D-02` منصة العمق 2.5D / 2.5D CSS depth rig (ready)
- `3D-03` صورة ثابتة بعمق طبقات / Still photo with layered depth (documented)
- `3D-05` العالم الأيزومتري / Isometric worlds (ready)
- `3D-06` حقول المكعبات المتموجة / Cube heightfield waves & voxel ripples (seen)

### `3D-05` — العالم الأيزومتري / Isometric worlds

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إسقاط أيزومتري بدالة واحدة لكل نقطة، ترتيب عمق بمجموع x+y، ونوافذ وأبواب ملصقة على الأوجه، وكاميرا تنتقل بين مناطق ملونة. / One projection function for every point, painter's sort by x + y, face-mapped details, a camera travelling between zones.

**متى:** رحلات، أنظمة، مدن مصغرة، لوجستيات / journeys, systems, miniature cities.

**كيف:** X = OX + (x − y)·cos30·S, Y = OY + (x + y)·0.5·S − z·S (use it for camera targets and text anchors too); sort ground items by x + y, elevated items after what is beneath; matrix() maps flat rects onto box faces for windows/doors/signs; Three.js: OrthographicCamera pitched 35.264°, fixed grid unit; build wave: tiles rise by (i + j)·40 ms, buildings extrude 300 ms, then small agents walk. python3 tools/kosif.py scaffold isometric <dir>; Basma STY.isometric: 16:9, 2.0 wps, Readex Pro, bg #EEF1FF/#F4F1FF, ink #1E1B4B, zones #E4F5DC/#EEF0F8/#F6EEDC/#E9E4FA/#E4F2F5, colours #6366F1/#F59E0B/#14B8A6/#E11D48/#EC4899/#3B82F6; flat style sheet: 3 shades per hue for cube faces, ≤40 elements.

**المعاملات:** cos30 = 0.866; pitch 35.264°; 40 ms/tile

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** isometric · projection · depth sort · diorama · أيزومتري

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/isometric/SKILL.md`
- `kosif-tool/playbooks/3d.md:44`
- `app/public/js/10_studio.js:593`
- `kosif-tool/styles/isometric`

#### 7. قدرات قريبة في العائلة

- `3D-03` صورة ثابتة بعمق طبقات / Still photo with layered depth (documented)
- `3D-04` جسم ذهبي بسماكة مزيفة / Fake-3D extrusion & parallel projection (ready)
- `3D-06` حقول المكعبات المتموجة / Cube heightfield waves & voxel ripples (seen)
- `3D-07` جدران البطاقات المائلة / Tilted card & screenshot walls (seen)

### `3D-06` — حقول المكعبات المتموجة / Cube heightfield waves & voxel ripples

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة صناديق مكررة ترتفع كموجة شعاعية أو حلقية أو حسب بيانات، بقمم ملونة عشوائيًا وكاميرا مائلة. / A grid of instanced boxes rising as radial/ring waves or to data.

**متى:** خلفيات تقنية، خرائط حرارية ثلاثية / tech backgrounds, 3D heatmaps.

**كيف:** InstancedMesh grid 16×16 … 40×40; height = A·max(0, sin(r·f − ω·t)) (A 0.5–3 units, ω 2–4 rad/s) + noise; tops randomly orange/blue/white or 5% accent; isometric/orthographic or 45° perspective with soft shadows; data heatmap 24×16: scale.y to the value with a spring staggered 10 ms by distance from the hotspot (overshoot 1.1), colour grey → yellow → red; DOF on a bouncing glossy sphere.

**المعاملات:** ω 2–4 rad/s; stagger 10 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** voxel · heightfield · cube wave · instancing · مكعبات

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/pm-tequilafunks-97f6c9`
- `kosif-tool/styles/pm-sudeepsd-1a3485`
- `kosif-tool/styles/pm-levabashidze-2d713a`

#### 7. قدرات قريبة في العائلة

- `3D-04` جسم ذهبي بسماكة مزيفة / Fake-3D extrusion & parallel projection (ready)
- `3D-05` العالم الأيزومتري / Isometric worlds (ready)
- `3D-07` جدران البطاقات المائلة / Tilted card & screenshot walls (seen)
- `3D-08` تحويلات البطاقات ثلاثية الأبعاد بالـCSS / CSS 3D card transforms (documented)

### `3D-07` — جدران البطاقات المائلة / Tilted card & screenshot walls

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة صور أو لقطات مواقع على مستوى مائل تنجرف ببطء وعنوان كبير فوقها. / A grid of thumbnails on a tilted plane drifting slowly under a headline.

**متى:** «أعمالنا»، معارض، افتتاحيات / portfolios, showcases, openers.

**كيف:** plane rotateX(20–50°) rotateZ(−15…−20°) with perspective 1200px, drift 30–60 px/s (or 3–4%/s), card radius 12 px, outer tiles blurred, dark radial scrim behind the headline; fly-over variant: camera translates then levels to focus one card (~1.5 s); floating variant: 4–6 cards at the edges rotated ±6° drifting 20–40 px over 4 s.

**المعاملات:** rotateX 20–50°; drift 30–60 px/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** card wall · tilted grid · showcase · جدار بطاقات

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/pm-listudio-820c7b`
- `kosif-tool/styles/pm-arjunsh1607-93005d`
- `kosif-tool/styles/pm-danilowm-d3720d`

#### 7. قدرات قريبة في العائلة

- `3D-05` العالم الأيزومتري / Isometric worlds (ready)
- `3D-06` حقول المكعبات المتموجة / Cube heightfield waves & voxel ripples (seen)
- `3D-08` تحويلات البطاقات ثلاثية الأبعاد بالـCSS / CSS 3D card transforms (documented)
- `3D-09` طيران الكاميرا في عالم CSS / CSS 3D camera flight & depth scatter (documented)

### `3D-08` — تحويلات البطاقات ثلاثية الأبعاد بالـCSS / CSS 3D card transforms

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قلب البطاقات ودورانها وميلها بالمنظور دون WebGL: قلب على الإيقاع، تقليب صفحات، مكعب كلمات، مروحة بطاقات، شريط أسطواني. / Perspective flips, tilts and carousels without WebGL.

**متى:** كشف منتج، مقارنة، قوائم / product reveals, comparisons.

**كيف:** parent perspective 900–1200px, preserve-3d, back face rotateY(180deg), backface-visibility hidden; rotationY 360 + rotationX 15 over 1.2 s sine.inOut; 3d-card-flip anchored to a downbeat (best span 0.8–1.6 s); page leaves rotateY ~150 ms per page with blur; text cube faces rotate 90° in 600 ms ease-in-out; card fan rotateY ±12° with opposing rotateZ, then float sin offsets (6 px, 3 s); cylinder carousel: cards at rotateY(step) translateZ(r ≈ 900px), rotate the group, floor reflection; poster tilt rotateY(−12°) rotateX(6°) with coloured slabs sliding out behind (800 ms).

**المعاملات:** perspective 900–1200; flip 0.8–1.6 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** card flip · CSS 3D · carousel · tilt · قلب بطاقات

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/3d-card-flip/scene.html`
- `kosif-tool/styles/pm-twoclipping-6dd14e`

#### 7. قدرات قريبة في العائلة

- `3D-06` حقول المكعبات المتموجة / Cube heightfield waves & voxel ripples (seen)
- `3D-07` جدران البطاقات المائلة / Tilted card & screenshot walls (seen)
- `3D-09` طيران الكاميرا في عالم CSS / CSS 3D camera flight & depth scatter (documented)
- `3D-10` الأرضيات الشبكية والخريطة المائلة / Perspective grid floors & tilted planes (seen)

### `3D-09` — طيران الكاميرا في عالم CSS / CSS 3D camera flight & depth scatter

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عالم preserve-3d يُحرَّك من حالة كاميرا واحدة على مراحل: غوص في شبكة مائلة، سحب للخلف، عبور بطاقات واقفة، تباطؤ للتركيز؛ وعناصر تتبعثر في سحابة عمق ثم تتجمع. / A preserve-3d world tweened leg by leg from one camera state; elements scatter into a depth cloud and assemble.

**متى:** افتتاحيات ديناميكية بلا WebGL / dynamic openers without WebGL.

**كيف:** landings power4.out, repositions power2.inOut, DOF via a --dof var on leaf elements; depth scatter/assemble: perspective 1400px, index-derived offsets, cloud spin power1.out, settle to a flat layout; orbit 3D flip entry: perspective 1800px, translateZ(220px) wins paint order, gsap.set the orbit start before phase 1; z-depth chaos: 30–50 chips at random x/y/z flying toward camera with blur ∝ \|z − focus\| (0–14 px) over 1.5–2 s; verify depth with angled ghost diagnostics.

**المعاملات:** perspective 1400–1800; blur 0–14 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** camera flight · depth scatter · CSS world · طيران الكاميرا

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/3d-camera-flight.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/depth-scatter-assemble.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/orbit-3d-entry.md`

#### 7. قدرات قريبة في العائلة

- `3D-07` جدران البطاقات المائلة / Tilted card & screenshot walls (seen)
- `3D-08` تحويلات البطاقات ثلاثية الأبعاد بالـCSS / CSS 3D card transforms (documented)
- `3D-10` الأرضيات الشبكية والخريطة المائلة / Perspective grid floors & tilted planes (seen)
- `3D-11` حلقات مدارية مائلة ورفع العقد / Pseudo-3D orbit rings & hover lift (ready)

### `3D-10` — الأرضيات الشبكية والخريطة المائلة / Perspective grid floors & tilted planes

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أرضية شبكة بمنظور تتلاشى نحو الأفق، حروف عملاقة واقفة عليها، أو خريطة مائلة تقف فوقها أشياء قائمة. / A grid floor fading to the horizon, standing billboard letters, or a tilted map with upright sprites.

**متى:** سينث ويف، تقنية، رحلات على خريطة / synthwave, tech, map journeys.

**كيف:** CSS rotateX(70deg) grid (alpha .15) fading to black, horizon at 30–55% height, 40 px module, dolly forward; synthwave variant with a point sphere above; tilted map: wrap the SVG in perspective(1400px) rotateX(θ ≈ 50°) and draw upright sprites in an overlay at Y' = Y·cosθ, z = Y·sinθ, scale = P/(P − z).

**المعاملات:** rotateX 70°; P = 1400, θ ≈ 50°

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** grid floor · synthwave · tilted map · أرضية شبكية

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/map-journey`
- `kosif-tool/styles/plotter`
- `kosif-tool/styles/pm-pankajkumar-dev-0bee87`

#### 7. قدرات قريبة في العائلة

- `3D-08` تحويلات البطاقات ثلاثية الأبعاد بالـCSS / CSS 3D card transforms (documented)
- `3D-09` طيران الكاميرا في عالم CSS / CSS 3D camera flight & depth scatter (documented)
- `3D-11` حلقات مدارية مائلة ورفع العقد / Pseudo-3D orbit rings & hover lift (ready)
- `3D-12` الأنفاق / Tunnels (seen)

### `3D-11` — حلقات مدارية مائلة ورفع العقد / Pseudo-3D orbit rings & hover lift

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حلقتان إهليلجيتان خلف عنصر بطل، إحداهما مائلة والأخرى تنكشف بالدوران، وعقد ترتفع نحو المشاهد. / Two elliptical rings behind a hero, one tilted, one revealing by rotation; nodes lifting toward the viewer.

**متى:** لوحات وعناصر بطل بلا WebGL / hero dials without WebGL.

**كيف:** ::before rotateX(18deg) rotateZ(−20deg) with ring shadows; ::after rotate(−35deg) scaleY(.46) via orbit-reveal from rotate(−10deg) scaleY(.25) over 1.5 s ease-studio, atmosphere-in scale .86 → 1; rings 250 px / 248×220 px, borders #d9f3c730 / #cec1e13d; nodes preserve-3d lifting translateZ(40px) scale(1.08) in .35 s.

**المعاملات:** 1.5 s; translateZ 40 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** orbit rings · pseudo 3D · CSS · حلقات

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-audit-studio/studio.css:68`
- `kosif-audit-studio/cinema/cinemaTheme.css`

#### 7. قدرات قريبة في العائلة

- `3D-09` طيران الكاميرا في عالم CSS / CSS 3D camera flight & depth scatter (documented)
- `3D-10` الأرضيات الشبكية والخريطة المائلة / Perspective grid floors & tilted planes (seen)
- `3D-12` الأنفاق / Tunnels (seen)
- `3D-13` مكونات HyperFrames ثلاثية الأبعاد / HyperFrames 3D components & blocks (install)

### `3D-12` — الأنفاق / Tunnels

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أشكال متداخلة تتكبر أسيًا وتدور فتصنع نفقًا، أو نفق مربعات سلكية، أو نفق معرض بألواح وصور تتضخم نحو الكاميرا. / Nested polygons scaling exponentially, wire square tunnels, or a gallery tunnel of slabs and images.

**متى:** انتقالات سرعة، افتتاحيات / speed transitions, openers.

**كيف:** 6–20 nested hexagons/squares with scale = s0·k^(i + speed·t) mod range and incremental rotation, dashed strokes, radiating speed lines; HyperFrames gallery-tunnel: infinite square tunnel of saturated slabs (#FF6A00, #AB54F7, #EA3737, #0072E3, #00AA3C, #FFB200) and caller images, speed 3, fog 14.25.

**المعاملات:** 6–20 layers

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** tunnel · nested polygons · speed · نفق

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/pm-crazyalphaaa-bc7e75`
- `kosif-tool/styles/pm-itsuki-dev-10942d`
- `kosif-one/vendor/hyperframes/registry/blocks/gallery-tunnel/gallery-tunnel.html`

#### 7. قدرات قريبة في العائلة

- `3D-10` الأرضيات الشبكية والخريطة المائلة / Perspective grid floors & tilted planes (seen)
- `3D-11` حلقات مدارية مائلة ورفع العقد / Pseudo-3D orbit rings & hover lift (ready)
- `3D-13` مكونات HyperFrames ثلاثية الأبعاد / HyperFrames 3D components & blocks (install)
- `3D-14` مشروع three-kit ثلاثي الأبعاد / KOSIF three-kit 3D project (ready)

### `3D-13` — مكونات HyperFrames ثلاثية الأبعاد / HyperFrames 3D components & blocks

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0; bundled assets carry their own licences (e.g. CC0 HDR, BSL Clipper) |

**ما هي:** مكونات وكتل جاهزة للعمق والمجسمات: رصة بطاقات بكاميرا، شريط منظوري، بطاقتان كالكتاب، بطاقات تدور، قرص منتج، بطل زجاجي، عنوان شظايا، بوابة سلكية، نفق معرض. / Ready depth and 3D components and blocks.

**متى:** تركيبات HyperFrames / HyperFrames compositions.

**كيف:** npx hyperframes add <name>: camera-rig-depth-stack, perspective-marquee (tilt flat\|standard\|steep), split-tilt-cards (book-open rotateY, badges spring-pop), three-orbiting-cards, tilt-card, canopy-part-title (3D leaves part, 12 s), code-slice-hero (cells flip under a depth field), cuboid-carousel (bevelled PBR cuboids on a wave, 6.67 s), exploded-stack (isometric plates explode with labels, 5 s), glass-hero (glass object refracting a giant headline, 5 s), glass-shard-title (Voronoi shards, 12.16 s — local copy lacks its matcap), orbit-card (10 s), product-turntable (6 s seamless loop, drop in a GLB), wireframe-portal-title (8 s), frost-sequence-camera-orbit (22.5 s, WebGPU shaders — local copy lacks its shard atlas), gallery-tunnel. Most load three (0.147–0.184) from a CDN; Latin fonts — swap to Arabic faces on canvas textures.

**المعاملات:** 16 items; 5–22.5 s

**التثبيت:** npx hyperframes add product-turntable

**الوسوم:** hyperframes · 3D components · turntable · glass hero · tilt cards

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/registry/blocks/product-turntable/product-turntable.html`
- `kosif-one/vendor/hyperframes/registry/blocks/glass-hero/glass-hero.html`
- `kosif-one/vendor/hyperframes/registry/blocks/exploded-stack/exploded-stack.html`
- `kosif-one/vendor/hyperframes/registry/components/camera-rig-depth-stack/camera-rig-depth-stack.html`

#### 7. قدرات قريبة في العائلة

- `3D-11` حلقات مدارية مائلة ورفع العقد / Pseudo-3D orbit rings & hover lift (ready)
- `3D-12` الأنفاق / Tunnels (seen)
- `3D-14` مشروع three-kit ثلاثي الأبعاد / KOSIF three-kit 3D project (ready)
- `3D-15` عقد مشهد Three.js الحتمي / Deterministic Three.js seek scene (ready)

### `3D-14` — مشروع three-kit ثلاثي الأبعاد / KOSIF three-kit 3D project

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مشروع 3D جاهز على حزمة window.K3 بلا npm: محرك عرض بمنحنى نغمات وظلال، وكتل عالم إجرائية، ورندر بمحرك الاستوديو. / A 3D project on the pre-bundled window.K3 kit: tone-mapped renderer, procedural world blocks, studio render.

**متى:** أي مشهد ثلاثي الأبعاد حقيقي / any real 3D scene.

**كيف:** python scripts/kmotion.py new NAME --3d --seconds 10 (or motion.py new NAME --3d) → src/main.js; without npm the import is rewritten to window.K3 and three-kit.bundle.js is copied (esbuild is not installed here, so kit edits cannot be re-bundled); render with motion.py render --engine studio. makeRenderer(canvas, W, H, {tone:'aces'\|'agx'\|'neutral', exposure:.6}): pixelRatio 1, PCF shadows, preserveDrawingBuffer — ACES punchy, AgX hue-stable highlights for fire/neon/sunsets, Khronos Neutral for products.

**المعاملات:** exposure 0.6; tone aces\|agx\|neutral

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** three-kit · K3 · tone mapping · ACES · AgX · renderer

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:esbuild` ← npm ls esbuild أو وجود node_modules/esbuild
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-studio/motion/kit/three-kit.js`
- `kosif-studio/motion/kit/three-kit.bundle.js`
- `100-superskills/skills/kosif-montage-motion/SKILL.md:85`
- `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:76`

#### 7. قدرات قريبة في العائلة

- `3D-12` الأنفاق / Tunnels (seen)
- `3D-13` مكونات HyperFrames ثلاثية الأبعاد / HyperFrames 3D components & blocks (install)
- `3D-15` عقد مشهد Three.js الحتمي / Deterministic Three.js seek scene (ready)
- `3D-16` ثلاثي الأبعاد في Remotion / Remotion ThreeCanvas (install)

### `3D-15` — عقد مشهد Three.js الحتمي / Deterministic Three.js seek scene

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صفحة HTML واحدة بـ render(t) حتمية، تُلتقط إطارًا إطارًا بمتصفح بلا واجهة: لا THREE.Clock، الكاميرا دالة للزمن، وتسخين المظللات قبل أول إطار. / One HTML page with a deterministic render(t), captured frame by frame headless.

**متى:** كل مشهد WebGL يصبح فيديو / every WebGL scene that becomes video.

**كيف:** renderer {preserveDrawingBuffer:true}; window.__kosif = {duration, fps, seek} (render_html.cjs) or window.__ready + render(t) + __duration (html_render.py / film.py animate); wait for fonts, warm shaders with seek(0) → seek(mid) → seek(0), gl.finish() after each frame, set ready only after the first real frame; one camera move per shot as a function of t; template scene-3d.html: three@0.169, ACES exposure 1.05, UnrealBloom (0.7, 0.6, 0.82), < 150k visible tris. python html_render.py page.html out.png --size 1920x1080 --t 2.5 renders one deterministic frame (finds Chromium at /opt/pw-browsers).

**المعاملات:** < 150k tris; bloom .7/.6/.82

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** three.js · seek · deterministic · headless · WebGL · render

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/tools/render_html.cjs`
- `kosif-studio/html_render.py`
- `100-superskills/skills/claude-animation-studio/templates/scene-3d.html`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/three.md`

#### 7. قدرات قريبة في العائلة

- `3D-13` مكونات HyperFrames ثلاثية الأبعاد / HyperFrames 3D components & blocks (install)
- `3D-14` مشروع three-kit ثلاثي الأبعاد / KOSIF three-kit 3D project (ready)
- `3D-16` ثلاثي الأبعاد في Remotion / Remotion ThreeCanvas (install)
- `3D-17` بوابات ومشهد داخل مشهد / Portals & render-to-texture (install)

### `3D-16` — ثلاثي الأبعاد في Remotion / Remotion ThreeCanvas

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Remotion company license |

**ما هي:** مشاهد React Three Fiber تُرندر بدقة الإطار لأن كل حركة من رقم الإطار. / R3F scenes rendered frame-exactly by driving everything from the frame number.

**متى:** مشاريع Remotion بعناصر 3D / Remotion projects with 3D.

**كيف:** @remotion/three <ThreeCanvas width height> with ambient 0.4 + directional 0.8; rotation = frame·0.02; never useFrame() from R3F and no self-animating shaders (pass frame as a uniform).

**المعاملات:** ambient .4; directional .8

**التثبيت:** npm i @remotion/three three @react-three/fiber

**الوسوم:** remotion · R3F · ThreeCanvas · 3D

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10436-remotion-markup/3d.md`

#### 7. قدرات قريبة في العائلة

- `3D-14` مشروع three-kit ثلاثي الأبعاد / KOSIF three-kit 3D project (ready)
- `3D-15` عقد مشهد Three.js الحتمي / Deterministic Three.js seek scene (ready)
- `3D-17` بوابات ومشهد داخل مشهد / Portals & render-to-texture (install)
- `3D-18` عالم البلورات بـ WebGL خام / Raw-WebGL procedural crystal shards (proven)

### `3D-17` — بوابات ومشهد داخل مشهد / Portals & render-to-texture

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مشهد خارج الشاشة يُرسم في خامة على لوح، مع بارالاكس بنسخ مصفوفة الكاميرا الرئيسية. / An offscreen scene rendered into a texture on a plane, parallaxed by copying the main camera.

**متى:** نوافذ إلى عوالم، شاشات داخل مشاهد / windows into worlds, screens in scenes.

**كيف:** R3F createPortal + useFBO (or a WebGLRenderTarget in plain three); sample in screen space with gl_FragCoord.xy / resolution; render the portal pass before the main pass each frame.

**التثبيت:** npm i @react-three/fiber @react-three/drei three

**الوسوم:** portal · render to texture · FBO · بوابة

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `3D-15` عقد مشهد Three.js الحتمي / Deterministic Three.js seek scene (ready)
- `3D-16` ثلاثي الأبعاد في Remotion / Remotion ThreeCanvas (install)
- `3D-18` عالم البلورات بـ WebGL خام / Raw-WebGL procedural crystal shards (proven)
- `3D-19` 3D مرسوم برمجيًا على Canvas / Software-rendered 3D on canvas (seen)

### `3D-18` — عالم البلورات بـ WebGL خام / Raw-WebGL procedural crystal shards

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مشهد WebGL1 بلا مكتبات لشظايا بلورية منخفضة المضلعات تنجرف وتدور وتتمايل في الضباب خلف الواجهة، حتمي بالبذرة. / A library-free WebGL1 scene of drifting low-poly crystal shards, deterministic per seed.

**متى:** خلفيات حية خفيفة جدًا (~18 KB) / very light living backgrounds.

**كيف:** SQCCrystal.mount(canvas, {density, interactive, scroll, still, seed, palette}) → {setMood, pulse, destroy, frames, shards}; shard = irregular hexagonal prism (6 sides, irregularity .45) with pointed caps and flat per-face normals, 24 triangles / 72 vertices; N = round((phone ? 14 : 30)·(weak device ? 0.7 : 1)·density) ≥ 6; z slab −4…−18; spin ±(.12, .17, .1) rad/s; bob sin(.5t + φ)·(.15….5); fov .95 rad; LCG seed 20261005; tests 4/4 passed here.

**المعاملات:** 24 tris/shard; ~18 KB

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** WebGL · crystals · procedural · lightweight · بلورات

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-earth-ci-fork/ui/art/crystal-world.js`
- `kosif-earth-ci-fork/tools/crystal_world.test.mjs`

#### 7. قدرات قريبة في العائلة

- `3D-16` ثلاثي الأبعاد في Remotion / Remotion ThreeCanvas (install)
- `3D-17` بوابات ومشهد داخل مشهد / Portals & render-to-texture (install)
- `3D-19` 3D مرسوم برمجيًا على Canvas / Software-rendered 3D on canvas (seen)
- `3D-20` كرات وحلقات من النقاط / Point spheres, particle tori & dot globes (seen)

### `3D-19` — 3D مرسوم برمجيًا على Canvas / Software-rendered 3D on canvas

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إسقاط رؤوس مجسم بمصفوفة منظور، ترتيب الأوجه من الخلف للأمام، وتظليل مسطح بضوء واحد / بلا WebGL. — Project a mesh with a perspective matrix, sort faces back to front, flat-shade with one light.

**متى:** مجسمات بسيطة سلكية أو مسطحة، أسلوب تقني / simple wireframe/flat-shaded objects.

**كيف:** rotate vertices on two axes (60–90°/s), project with f / (z + d), painter-sort faces by mean z, shade by max(0, n·l); wireframe → shaded transition by fading fill in; ~128–420 faces; HUD extras: two tilted orbit ellipses, crop brackets, numeric readout, giant outline word behind at 10%; words placed on a 3D ring around the object, depth-scaled. (code snippet in references/powers/3d-spatial.md)

**المعاملات:** ~128–420 faces; 60–90°/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** software 3D · projection · painter's algorithm · wireframe · canvas

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/pm-grace-sunnyy-29bc61`
- `kosif-tool/styles/pm-teslachartz-c58b32`
- `kosif-tool/styles/pm-gizakdag-b8c59e`

#### 7. قدرات قريبة في العائلة

- `3D-17` بوابات ومشهد داخل مشهد / Portals & render-to-texture (install)
- `3D-18` عالم البلورات بـ WebGL خام / Raw-WebGL procedural crystal shards (proven)
- `3D-20` كرات وحلقات من النقاط / Point spheres, particle tori & dot globes (seen)
- `3D-21` الرسم بالأشعة ودوال المسافة / Raymarched SDF scenes (seen)

### `3D-20` — كرات وحلقات من النقاط / Point spheres, particle tori & dot globes

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط على كرة فيبوناتشي أو طارة تدور وتُسقط بحجم ولون حسب العمق، مع مدارات، وتحول طارة إلى كرة، وكرة أرضية من نقاط اليابسة. / Fibonacci-sphere or torus points rotating with depth-based size/colour, orbits, torus → sphere morphs, dot-matrix globes.

**متى:** ذكاء اصطناعي، شبكات، عالمية / AI, networks, global themes.

**كيف:** 500–2000 points (globe ~20k sampled on a land mask with warm city dots), rotate Y 20–40°/s (globe 3°/s), size and alpha by z, colour by depth (violet → red, pink → blue), additive glow; 1–2 tilted elliptical orbits with small moving dots; morph by lerping each point between its torus and sphere positions; fresnel rim + bloom for globes; macro science opener: ~1500 instanced spheres in a translucent glass sphere with a blurred background and an italic 'Fig. 1' caption.

**المعاملات:** 500–2000 pts; 20–40°/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** point sphere · fibonacci · particle torus · dot globe · كرة نقاط

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/pm-jasonzhou1993-8595e0`
- `kosif-tool/styles/pm-ghinaiya-nirmal-5d8fec`
- `kosif-tool/styles/pm-nolkeeg-bf062e`
- `kosif-tool/styles/pm-shinskinakamoto-20190b`

#### 7. قدرات قريبة في العائلة

- `3D-18` عالم البلورات بـ WebGL خام / Raw-WebGL procedural crystal shards (proven)
- `3D-19` 3D مرسوم برمجيًا على Canvas / Software-rendered 3D on canvas (seen)
- `3D-21` الرسم بالأشعة ودوال المسافة / Raymarched SDF scenes (seen)
- `3D-22` نماذج GLB بحركة مضبوطة على الزمن / GLB models with seeked animation (ready)

### `3D-21` — الرسم بالأشعة ودوال المسافة / Raymarched SDF scenes

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فقاعات معدنية ملتحمة، كرات زجاجية تكسر النص، سحب حجمية، وثقب أسود يحني الضوء / كلها في شيدر شاشة كاملة. — Metaballs, refracting glass spheres, volumetric clouds and black-hole lensing in a full-screen shader.

**متى:** لقطات بطل مجردة، فضاء، فخامة / abstract hero shots, space, luxury.

**كيف:** SDF smooth-union spheres (k ≈ 0.5) with fresnel rim and specular or orange-blue gradient; glass: refraction of a type texture with chromatic dispersion, 96 steps; clouds/smoke: 64–128 steps accumulating FBM density, bounded loops; black hole: integrate light paths with approximate bending (step 0.05–0.1 r_s, 200–400 steps), thin turbulent disk 3–15 r_s over a star map; pass t as a uniform, never self-animate.

**المعاملات:** 64–128 steps; k 0.5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** raymarching · SDF · metaballs · black hole · شيدر

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/pm-zaqailo-212ad3`
- `kosif-tool/styles/pm-ndhabarde11-f155b4`
- `kosif-tool/styles/pm-rebutonepress-810f78`
- `kosif-atlas/skills/2199-lvtd-skills/8087-game-sdf-and-field-modeling/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `3D-19` 3D مرسوم برمجيًا على Canvas / Software-rendered 3D on canvas (seen)
- `3D-20` كرات وحلقات من النقاط / Point spheres, particle tori & dot globes (seen)
- `3D-22` نماذج GLB بحركة مضبوطة على الزمن / GLB models with seeked animation (ready)
- `3D-23` Blender بلا واجهة / Headless Blender (bpy) (install)

### `3D-22` — نماذج GLB بحركة مضبوطة على الزمن / GLB models with seeked animation

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تحميل نموذج GLB جاهز أو مصنوع في Blender وضبط حركته الهيكلية على الزمن المطلق. / Load a GLB and seek its skeletal/object animation to absolute time.

**متى:** شخصيات أو منتجات جاهزة / ready characters or products.

**كيف:** m = await K3.loadModel(url, {clip, offset, speed, caustics}); m.userData.set(t) → mixer.setTime (motion.py bundle inlines the GLB as a data URL); pipeline: Blender → glTF 2.0/GLB with applied transforms, consistent units/pivots, colour maps sRGB, normal/roughness non-colour → glTF Transform prune/dedup/simplify, Meshopt or Draco geometry, KTX2/BasisU textures; addWave for cloth/flags; licence any downloaded model.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** GLB · glTF · AnimationMixer · Blender · نموذج

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `blender` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-studio/motion/kit/three-kit.js:964`
- `kosif-atlas/skills/2696-game-studio/10370-web-3d-asset-pipeline/SKILL.md`
- `kosif-atlas/skills/1526-gamegen/4161-blender-game-assets/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `3D-20` كرات وحلقات من النقاط / Point spheres, particle tori & dot globes (seen)
- `3D-21` الرسم بالأشعة ودوال المسافة / Raymarched SDF scenes (seen)
- `3D-23` Blender بلا واجهة / Headless Blender (bpy) (install)
- `3D-24` تحليق Cesium فوق تضاريس ومدن حقيقية / Cesium terrain & city flyovers (key)

### `3D-23` — Blender بلا واجهة / Headless Blender (bpy)

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Blender GPL-2.0-or-later (outputs are yours) |

**ما هي:** Blender كمكتبة بايثون لبناء المشاهد ورندرها أو تصدير GLB؛ وBlender MCP وCinema 4D وSpline خارج الحاوية. / Blender as a Python module for scenes, renders and GLB export.

**متى:** نمذجة معقدة أو رندر Cycles / complex modelling or Cycles renders.

**كيف:** pip install bpy (Blender 5.2, ~400 MB) then build the scene in Python, keep the frame → time mapping explicit, export GLB for three-kit (3D-22) or render frames with Eevee/Cycles (CPU only here — slow); Blender MCP, Cinema 4D MoGraph/Redshift (paid) and Spline (proprietary) need the user's own install or account.

**التثبيت:** pip install bpy

**الوسوم:** blender · bpy · cycles · export · بلندر

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `blender` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`
- `kosif-atlas/skills/228-mas-3d-games/706-cinema-4d/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `3D-21` الرسم بالأشعة ودوال المسافة / Raymarched SDF scenes (seen)
- `3D-22` نماذج GLB بحركة مضبوطة على الزمن / GLB models with seeked animation (ready)
- `3D-24` تحليق Cesium فوق تضاريس ومدن حقيقية / Cesium terrain & city flyovers (key)
- `3D-25` تضاريس إجرائية / Procedural terrain (ready)

### `3D-24` — تحليق Cesium فوق تضاريس ومدن حقيقية / Cesium terrain & city flyovers

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تحليق كطائرة مروحية فوق تضاريس حقيقية أو مدن ثلاثية واقعية، يُرندر إطارًا إطارًا. / Helicopter-style flights over real terrain or photoreal cities, frame by frame.

**متى:** رحلات جغرافية، عقارات، سياحة / geography, real estate, tourism.

**كيف:** Cesium 1.143 from a CDN after setting CESIUM_BASE_URL; landscape: MapTiler terrain-quantized-mesh-v2 + satellite-v2 (MapTiler key, no Cesium ion token); city: Google Photorealistic 3D Tiles with the globe hidden (Google Maps key; promo clips ≤ 30 s), maximumScreenSpaceError 4 for hero landmarks, 6–8 wide; render a mid-frame still before the full clip; globe checks: record longitude origin, verify ≥3 known places, shortest-path rotation, unwrap the antimeridian.

**المعاملات:** SSE 4 hero / 6–8 wide

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cesium · 3D tiles · terrain flyover · globe · تحليق

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/TECHNIQUE.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `3D-22` نماذج GLB بحركة مضبوطة على الزمن / GLB models with seeked animation (ready)
- `3D-23` Blender بلا واجهة / Headless Blender (bpy) (install)
- `3D-25` تضاريس إجرائية / Procedural terrain (ready)
- `3D-26` غابة صنوبر بالمثيلات / Instanced conifer forest (ready)

### `3D-25` — تضاريس إجرائية / Procedural terrain

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سطح تزيحه دالة ارتفاع (ضوضاء متعرجة، التواء المجال، نهر محفور) بألوان من الارتفاع والميل وخرائط تفصيل مكررة. / A plane displaced by a height function with height/slope colours and tiled detail maps.

**متى:** جبال، كثبان، وديان، خلجان / mountains, dunes, valleys, bays.

**كيف:** K3.makeTerrain({height(x,z), colour(h,slope,x,z,c), seg:560, size:4600, texSize:1024, albedoRepeat:60, normalRepeat:90, normalScale:.55, roughness:.95}); alpineColour palette snow #f4f7fb, rock #5d5a58/#7a6f66, grass #4e6e34/#6b8a3c, sand #b9a77a, deep #2f4a3a; mountains behind a bay: warp x,z by 180·fbm(.0009), ridge 820·exp(−((z+1250)/820)²)·(.55 + .45·ridged), hills 260·ridged(.0011), detail 55·fbm(.004) + 14·fbm(.02), river x = 140·sin(z/420) − 220 carved 150·exp(−d²/(2·55²)); dunes: vnoise fbm 5 octaves (×0.5 amp, ×2.03 freq), dune = 4.5·fbm(x·.006) + 1.8·fbm(x·.02 + 9) − 3, sand #E2B577 → #B9824B.

**المعاملات:** seg 560; size 4600 m

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** terrain · fbm · ridged noise · mountains · تضاريس

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-studio/motion/kit/three-kit.js:112`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:7`
- `kosif-one/projects/egypt-2120-animation/index.html`

#### 7. قدرات قريبة في العائلة

- `3D-23` Blender بلا واجهة / Headless Blender (bpy) (install)
- `3D-24` تحليق Cesium فوق تضاريس ومدن حقيقية / Cesium terrain & city flyovers (key)
- `3D-26` غابة صنوبر بالمثيلات / Instanced conifer forest (ready)
- `3D-27` السماء والشمس والإضاءة البيئية / Sky, sun & gradient IBL (ready)

### `3D-26` — غابة صنوبر بالمثيلات / Instanced conifer forest

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حتى 22 ألف شجرة صنوبر بطبقتين وتيجان متعرجة ببذرة، توزع بقاعدة قبول حسب الارتفاع والميل والتكتل. / Up to 22k instanced two-tier conifers placed by an accept rule.

**متى:** جبال وغابات وطبيعة / mountains, forests, nature.

**كيف:** K3.makeForest({height, region:[x0,x1,z0,z1], accept(x,z,h), max:22000, scale, hue:.25 ± .035, tiers:4, thinFrom:300, thinTo:430, seed}); K3.coniferCrown(tiers, seed); trunk #4a3524; per-tree colour.

**المعاملات:** max 22000; 4 tiers + spire

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** forest · conifer · instancing · غابة

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-studio/motion/kit/three-kit.js:150`
- `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:174`

#### 7. قدرات قريبة في العائلة

- `3D-24` تحليق Cesium فوق تضاريس ومدن حقيقية / Cesium terrain & city flyovers (key)
- `3D-25` تضاريس إجرائية / Procedural terrain (ready)
- `3D-27` السماء والشمس والإضاءة البيئية / Sky, sun & gradient IBL (ready)
- `3D-28` البحر والماء / Sea & water surfaces (ready)

### `3D-27` — السماء والشمس والإضاءة البيئية / Sky, sun & gradient IBL

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سماء رايلي/مي فيزيائية تتبع الشمس فيها القصة (فجر ← نهار ← غيم ← صفاء)، أو قبب سماء مكتوبة لمزاج معين، وإضاءة بيئية من تدرج بلا ملفات HDRI. / A physical sky whose sun follows the story, custom mood skies, and IBL from a gradient.

**متى:** كل مشهد خارجي / every outdoor scene.

**كيف:** sky = makeSky(scene, {turbidity, rayleigh, mie, mieG, scale}); sky.setSun(elev, azim) e.g. elev 2.5 + 24·smooth(0, 6.5) − 8·smooth(8, 10) + 12·smooth(12.5, 15.5), turbidity 3 + 7·overcast; fog colour = sky horizon colour (aerial perspective), FogExp2 #c9d6e2 1.1e-4; custom domes (BackSide sphere ShaderMaterial): blue hour zen (.02,.045,.13) mid (.07,.15,.36) horizon (.30,.34,.52) + afterglow band exp(−9y)·g³·(1,.45,.2), night moon glow pow(m,900)·1.2 + pow(m,60)·.16; envFromGradient(renderer, scene, {top, horizon, ground, sun, sunColor, sunPower}) with environmentIntensity .5–.55.

**المعاملات:** fog 1.1e-4; env .5–.55

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** sky · sun · IBL · fog · blue hour · سماء

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:64`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:26`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:32`

#### 7. قدرات قريبة في العائلة

- `3D-25` تضاريس إجرائية / Procedural terrain (ready)
- `3D-26` غابة صنوبر بالمثيلات / Instanced conifer forest (ready)
- `3D-28` البحر والماء / Sea & water surfaces (ready)
- `3D-29` السحب / Clouds (ready)

### `3D-28` — البحر والماء / Sea & water surfaces

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بحر عاكس بخرائط نورمال، بحر ليلي يعكس القمر بأمواج طويلة، ماء ضحل صافٍ يُظهر القاع، وبحر من شبكة ارتفاعات بزبد. / Reflective sea, moonlit swell, shallow clear water and a height-field sea with whitecaps.

**متى:** شواطئ، قوارب، برك / coasts, boats, ponds.

**كيف:** makeSea({size:30000, res:768}) (Three Water, FBM normals); night: makeSea({size:24000, res:1024, color:0x061525, distortion:3.2, waveSize:2.4, normals: normalFromHeight(512, …)}) with sunDirection = moon, kelvin(4100)·.9, boat heave .09·sin(1.25t + .4) + .035·sin(2.3t + 1.7); shallow: makeShallowWater({seg:300, amp:.006, clarity:.72, deep:0x1c3a22, shallow:0x4d6a45, skyTop:0x8fb3d8, skyHorizon:0xe9c48e, ripples:28}); whitecaps: Plane 320² displaced by 4 noise octaves + .45·sin(.3x + .1y), crest blend smoothstep(h, .9, 1.7) to white, clearcoat 1, roughness .24; Gerstner sunset ocean: 4–8 waves (λ 2–30 m, A .05–.4 m), fresnel sky mix, glitter path from a 5° sun.

**المعاملات:** res 768–1024; heave .09

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** sea · water · reflection · waves · بحر

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-studio/motion/kit/three-kit.js`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:186`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:58`
- `kosif-studio/scenes/whale_dragon_3d.html:86`

#### 7. قدرات قريبة في العائلة

- `3D-26` غابة صنوبر بالمثيلات / Instanced conifer forest (ready)
- `3D-27` السماء والشمس والإضاءة البيئية / Sky, sun & gradient IBL (ready)
- `3D-29` السحب / Clouds (ready)
- `3D-30` بركة الكوي والعشب والتفاصيل الحية / Koi pond, reeds & living details (ready)

### `3D-29` — السحب / Clouds

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لوح سحب يُرسم بالأشعة في 36 خطوة، أو سحب ركامية كرتونية من تجمعات كرات بتدرج ثلاثي. / A raymarched cloud slab, or toon cumulus from sphere clusters.

**متى:** سماء واقعية أو كرتونية / realistic or toon skies.

**كيف:** three-kit cloud slab (36 raymarch steps) with the sun from the sky model; toon: 20–60 instanced spheres per cloud, 3-band ramp violet #5a3a8a shadow / pink #b066a0 mid / peach #f0c09a rim from a low (~5°) sun, soft fresnel outline.

**المعاملات:** 36 steps; 20–60 spheres

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** clouds · raymarch · toon cumulus · سحب

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/SKILL.md:106`
- `kosif-tool/styles/pm-nft-chen-5f8bb0`

#### 7. قدرات قريبة في العائلة

- `3D-27` السماء والشمس والإضاءة البيئية / Sky, sun & gradient IBL (ready)
- `3D-28` البحر والماء / Sea & water surfaces (ready)
- `3D-30` بركة الكوي والعشب والتفاصيل الحية / Koi pond, reeds & living details (ready)
- `3D-31` مؤشرات المقياس: جبال وطريق وأضواء بعيدة / Scale cues: ridge layers, road ribbon, far lights (ready)

### `3D-30` — بركة الكوي والعشب والتفاصيل الحية / Koi pond, reeds & living details

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ماء ضحل بتموجات حلقات البتلات، كاويات، سبع سمكات كوي، بتلات تسقط، حصى، قصب يتمايل، وشمس مرقطة عبر الأغصان بمسار كاميرا واحد. / A living pond: caustics, koi, falling petals, pebbles, swaying reeds and dappled sun.

**متى:** لقطات هادئة فاخرة، طبيعة يابانية / calm premium nature shots.

**كيف:** makeShallowWater, addCaustics, makeKoi (CHAR-43), makePetals, makePebbles, makeBlades({n:1500, tall:.9, width:.02, hue:.24}) swaying 1.4 Hz (bend ∝ height²), makeDappledSun, cameraPath; pond ellipse 6.4 × 4.1 m, exposure .62, fog #CBB08A .011, 10 s 1080p30.

**المعاملات:** 1500 blades; 1.4 Hz sway

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** koi pond · grass · reeds · caustics · بركة

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-studio/motion/projects/koi_pond/src/main.js:1`
- `kosif-studio/motion/kit/three-kit.js:746`

#### 7. قدرات قريبة في العائلة

- `3D-28` البحر والماء / Sea & water surfaces (ready)
- `3D-29` السحب / Clouds (ready)
- `3D-31` مؤشرات المقياس: جبال وطريق وأضواء بعيدة / Scale cues: ridge layers, road ribbon, far lights (ready)
- `3D-32` بدن قارب بمعادلات / Parametric lofted boat hull (ready)

### `3D-31` — مؤشرات المقياس: جبال وطريق وأضواء بعيدة / Scale cues: ridge layers, road ribbon, far lights

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طبقات جبال بعيدة بحواف متعرجة، طريق على منحنى مع تسوية الأرض حوله، وأضواء شاطئ بعيدة على بعد 6 كم تعطي المشهد حجمه. / Distant ridge layers, a curved road ribbon with flattened terrain, and far shore lights for scale.

**متى:** مشاهد ليلية وطرق ومسافات كبيرة / night roads, vast landscapes.

**كيف:** ridges: PlaneGeometry(dz·4.2, hgt·1.6, 400, 1) whose top vertices follow ridged noise, layers [700 m, 140], [1400, 260], [2600, 420], [4500, 650]; road: CatmullRom centreline sampled every 20 m to −4200, offset by the normal, triangulated (N 800), terrain height × smooth(ROAD_W, ROAD_W + 30, \|x − roadX(z)\|); far lights: 150 Points at z ≈ −6480, height 4–18 m, 70% kelvin(2200–3100) else 5200, size 1.6 px, additive, opacity .75, fog off. blue_hour renders light trails with render --blur 16 --shutter 30 --stack lighten.

**المعاملات:** ridges 700–4500 m; lights at ~6.5 km

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** scale cues · ridges · road · light trails · مقياس

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:54`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:178`
- `kosif-studio/motion/projects/blue_hour/src/main.js:1`

#### 7. قدرات قريبة في العائلة

- `3D-29` السحب / Clouds (ready)
- `3D-30` بركة الكوي والعشب والتفاصيل الحية / Koi pond, reeds & living details (ready)
- `3D-32` بدن قارب بمعادلات / Parametric lofted boat hull (ready)
- `3D-33` مدينة المستقبل: نوافذ وطاقة وعمارة / Future city kit (windows, solar fields, architecture) (ready)

### `3D-32` — بدن قارب بمعادلات / Parametric lofted boat hull

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بدن فلوكة يتولد من منحنيات العرض والحافة والقاعدة على طوله، مع الصاري والشراع المطوي والحبال. / A felucca hull generated from beam, sheer and keel curves, with mast, yard and rigging.

**متى:** النيل، البحر، القصص التراثية / the Nile, the sea, heritage stories.

**كيف:** beam(s) = 1.12·sin(π(.13 + .87s))^.62; sheer(s) = .78 + .62s^3.2 + .22(1 − s)^5; keel(s) = −.62·sin(π(.04 + .96s))^.45; x = side·b·(1 − (1 − φ)^2.4); grid 72 × 16 per side; L 7.2 m; yard rotated −1.02 rad, 8.6 m; sail = 9 tapered cylinders.

**المعاملات:** L 7.2 m; 72×16 grid

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** boat · felucca · loft · parametric · قارب

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:14`

#### 7. قدرات قريبة في العائلة

- `3D-30` بركة الكوي والعشب والتفاصيل الحية / Koi pond, reeds & living details (ready)
- `3D-31` مؤشرات المقياس: جبال وطريق وأضواء بعيدة / Scale cues: ridge layers, road ribbon, far lights (ready)
- `3D-33` مدينة المستقبل: نوافذ وطاقة وعمارة / Future city kit (windows, solar fields, architecture) (ready)
- `3D-34` مركبات ودعائم من أشكال أولية / Props & vehicles from primitives (seen)

### `3D-33` — مدينة المستقبل: نوافذ وطاقة وعمارة / Future city kit (windows, solar fields, architecture)

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** آلاف المباني المكررة بنوافذ مضاءة تُحسب من الموضع، حقول مرايا شمسية وألواح ومحاور ري، وعناصر عمارة مستقبلية: مزارع عمودية، قطار مغناطيسي، برج لوتس، منارة. / Instanced night city with computed windows, solar fields and futuristic props.

**متى:** رؤى مستقبلية لمدن عربية / future visions of Arab cities.

**كيف:** InstancedMesh up to 2600 boxes skipping avenues (gx % 6, gz % 7); window grid (u/2.4, y/3.2), mask .18–.82 × .22–.78, lit if hash > 1 − lit (.32–.8), warm #FFC77A / cool #8FE6FF, base #0B1226, rim pow(1 − \|N·V\|, 3)·.35 #3B5BA8, bands step(.985, fract(y/38 + seed)), fog #121A44 .0021; 900 heliostats lookAt a receiver (metal 1, roughness .05, env 2.2) pulsing 1 + .08·sin 9t, 2400 panels, 160 pivots; props with emissive colours × > 1 so bloom catches them (farm tiers #7CFF9F ×2.2, maglev stripe #59E3FF ×4, lotus petals #FF8FD0 at .26, Pharos bands #FFD9A0 ×5). Showcase: Egypt 2120 (1080×1920, 18 s, 6 shots, Three 0.169, Cairo glass captions, synthesised Hijaz score).

**المعاملات:** 2600 buildings; 900 heliostats

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** future city · solarpunk · instancing · windows · مدينة المستقبل

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/projects/egypt-2120-animation/index.html`
- `kosif-one/projects/egypt-2120-animation/README.md`

#### 7. قدرات قريبة في العائلة

- `3D-31` مؤشرات المقياس: جبال وطريق وأضواء بعيدة / Scale cues: ridge layers, road ribbon, far lights (ready)
- `3D-32` بدن قارب بمعادلات / Parametric lofted boat hull (ready)
- `3D-34` مركبات ودعائم من أشكال أولية / Props & vehicles from primitives (seen)
- `3D-35` مناورات طيران على مسار / Aircraft spline manoeuvres & chase cam (seen)

### `3D-34` — مركبات ودعائم من أشكال أولية / Props & vehicles from primitives

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طائرة من دالة مصنع واحدة، مركبة كرتونية منخفضة المضلعات بحد أسود، دعائم مكتب، بلاطة خشبية بخامة مرسومة، صخور عائمة، كهف، وجزيرة ديوراما. / Vehicles and set dressing built from primitives.

**متى:** مشاهد سريعة بلا نماذج جاهزة / quick scenes without downloaded models.

**كيف:** lathe fuselage + extruded wings + prop blades with per-part materials; box primitives with MeshToon + black outline pass; mug cylinder + liquid disc + steam sprites, hex pencil, paper plane; RoundedBoxGeometry(1, 1, .35, 4, .08) with a canvas grain texture (#d3bb9b / #a58862) and a serif letter; displaced cones/cylinders with vertical striation and fog .02; flatShaded displaced icosahedrons (detail 1, displacement .3) in crimson #350006 fog 10–40; floating island disc with layered rim at fov 30.

**المعاملات:** toon + outline; fog .02

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** props · primitives · low poly · toon · دعائم

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/pm-buildfastwithai-ed9447`
- `kosif-tool/styles/pm-anilraok-eff262`
- `kosif-tool/styles/pm-gorden-sun-041f56`

#### 7. قدرات قريبة في العائلة

- `3D-32` بدن قارب بمعادلات / Parametric lofted boat hull (ready)
- `3D-33` مدينة المستقبل: نوافذ وطاقة وعمارة / Future city kit (windows, solar fields, architecture) (ready)
- `3D-35` مناورات طيران على مسار / Aircraft spline manoeuvres & chase cam (seen)
- `3D-36` وصفة الإضاءة السينمائية / Cinematic 3D lighting recipe (ready)

### `3D-35` — مناورات طيران على مسار / Aircraft spline manoeuvres & chase cam

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طائرة على مسار Catmull-Rom تميل بزاوية تُشتق من انحناء المسار، مع لفات وغطسات مكتوبة، وكاميرا مطاردة تميل معها. / A plane on a spline banking from curvature, with scripted rolls and a banking chase cam.

**متى:** طيران، سفر، مغامرة / flight, travel, adventure.

**كيف:** bank = atan(v²·κ/g) capped at 80°; add barrel-roll / spiral-dive segments; chase camera behind and above with lag; over procedural patchwork terrain + fog.

**المعاملات:** bank ≤ 80°

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** aircraft · banking · spline · chase cam · طيران

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/pm-nft-chen-5f8bb0`
- `kosif-tool/styles/pm-buildfastwithai-ed9447`

#### 7. قدرات قريبة في العائلة

- `3D-33` مدينة المستقبل: نوافذ وطاقة وعمارة / Future city kit (windows, solar fields, architecture) (ready)
- `3D-34` مركبات ودعائم من أشكال أولية / Props & vehicles from primitives (seen)
- `3D-36` وصفة الإضاءة السينمائية / Cinematic 3D lighting recipe (ready)
- `3D-37` المواد الفيزيائية / Physical materials (glass, chrome, wet, iridescent) (ready)

### `3D-36` — وصفة الإضاءة السينمائية / Cinematic 3D lighting recipe

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ضوء مفتاح واحد باتجاه واحد وحرارة لونية محددة، ثلاث نقاط بنسبة 5:1، وإعدادات جاهزة (رامبرانت، صدفة، حاد، ناعم جدًا، شمس). / One key with a defined Kelvin, 5:1 three-point rigs and named presets.

**متى:** كل مشهد 3D / every 3D scene.

**كيف:** three-kit lightRig {key, fillStops 2, rimStops 0.5, keyK 5600, fillK 6500, rimK 4300} (5:1); lightPreset rembrandt / clamshell / edgy / ultrasoft / short / broad / sun; playbook: key 45°, fill 30%, rim; fov 40–55 (85 mm ≈ 24°); primitives + seeded InstancedMesh crowds; Standard/Physical + PMREM env; custom shaders only for sky/water; fog colour from the sky horizon.

**المعاملات:** 5:1; 5600/6500/4300 K; fov 40–55

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** lighting · three point · Kelvin · rembrandt · إضاءة

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `100-superskills/skills/hyperframes-animation-studio/scripts/kit/three-kit.js`
- `100-superskills/skills/cinematic-3d-scene/SKILL.md`
- `kosif-tool/playbooks/3d.md`

#### 7. قدرات قريبة في العائلة

- `3D-34` مركبات ودعائم من أشكال أولية / Props & vehicles from primitives (seen)
- `3D-35` مناورات طيران على مسار / Aircraft spline manoeuvres & chase cam (seen)
- `3D-37` المواد الفيزيائية / Physical materials (glass, chrome, wet, iridescent) (ready)
- `3D-38` سلسلة ما بعد المعالجة / Post stack (bloom, ACES, film) (ready)

### `3D-37` — المواد الفيزيائية / Physical materials (glass, chrome, wet, iridescent)

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** زجاج بنفاذية وانكسار وتشتت، كروم عاكس، جلد مبلل بطبقة لامعة، فقاعات متقزحة، وخرائط نتوء وخشونة تُولَّد في Canvas بلا تحميل صور. / Glass, chrome, wet clearcoat, iridescent shells and canvas-generated bump/roughness maps.

**متى:** لقطات منتج وبطل فاخرة / premium product and hero shots.

**كيف:** glass: MeshPhysicalMaterial transmission 1, thickness 1.4, ior 1.5–1.62, dispersion .35, iridescence .9, clearcoat 1, attenuation colour + distance (transmission over a text plane refracts the type); chrome: metalness 1, roughness .05–.2 with an env map and a coloured rim light; wet skin: clearcoat 1 over rough hide; noiseTexture(size, scale, octaves, base, amp, seedZ) with three's ImprovedNoise → CanvasTexture RepeatWrapping (skin bump 512/24/5 oct, roughness 256/10/4); iridescent blob: noise-displaced sphere with thin-film/fresnel rainbow; emissive × > 1 with toneMapped:false to feed bloom.

**المعاملات:** ior 1.5–1.62; roughness .05–.2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** glass · chrome · clearcoat · iridescence · PBR · مواد

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-studio/scenes/whale_dragon_3d.html:60`
- `kosif-studio/scenes/whale_dragon_3d.html:1`

#### 7. قدرات قريبة في العائلة

- `3D-35` مناورات طيران على مسار / Aircraft spline manoeuvres & chase cam (seen)
- `3D-36` وصفة الإضاءة السينمائية / Cinematic 3D lighting recipe (ready)
- `3D-38` سلسلة ما بعد المعالجة / Post stack (bloom, ACES, film) (ready)
- `3D-39` استوديو المنتج الكريمي / Studio sweep, backdrop & stage disc (ready)

### `3D-38` — سلسلة ما بعد المعالجة / Post stack (bloom, ACES, film)

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بلوم بعتبة عالية، منحنى ACES، حبيبات فيلم، وإخراج sRGB / ومعالجة خفيفة سريعة للاستوديو. — High-threshold bloom, ACES, film grain and sRGB output; a fast lite post for the studio.

**متى:** كل مشهد WebGL يحتاج توهجًا / any WebGL scene needing glow.

**كيف:** EffectComposer → RenderPass → UnrealBloomPass(strength .22–.7, radius .5–.6, threshold .82–.9) → FilmPass .22 → OutputPass; ACES exposure .6–1.55 by scene; HalfFloat render target with 4× MSAA; K3S.makeLitePost(renderer, scene, camera, W, H) for bloom + grade; three-kit bloom .22/.6/.9; keep bloom threshold ≥ .9 for cute/product scenes so only emissives glow; letterbox opening 70 px → 0 over 2.2 s in the scene3d template.

**المعاملات:** bloom .22–.7 / .5–.6 / .82–.9

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** bloom · post processing · ACES · film grain · ما بعد المعالجة

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-studio/scenes/whale_dragon_3d.html:266`
- `kosif-studio/motion/kit/shape-kit.js`
- `100-superskills/skills/claude-animation-studio/templates/scene-3d.html`
- `kosif-studio/motion/templates/scene3d/src/main.js`

#### 7. قدرات قريبة في العائلة

- `3D-36` وصفة الإضاءة السينمائية / Cinematic 3D lighting recipe (ready)
- `3D-37` المواد الفيزيائية / Physical materials (glass, chrome, wet, iridescent) (ready)
- `3D-39` استوديو المنتج الكريمي / Studio sweep, backdrop & stage disc (ready)
- `3D-40` مجسمات بطل جاهزة / Hero objects (geode, knot, coin) (ready)

### `3D-39` — استوديو المنتج الكريمي / Studio sweep, backdrop & stage disc

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خلفية استوديو لا نهائية كريمية بظل تلامس وشبكة خافتة وثلاث إضاءات ناعمة، أو خلفية متدرجة وقرص قياس بمسح ضوئي. / A cream infinite sweep with contact shadow, faint grid and soft three-light rig, or a gradient backdrop and a scanning stage disc.

**متى:** عرض منتجات وشخصيات / product and character showcases.

**كيف:** K3.studio(scene, {bg:'#f1efe8', grid}) — shadow .22, grid 16 m / 32 div #c9d8c2 / #d9e4d4 at .35, key 2.6 white at (3, 6, 4), fill #dfe8ff .9, rim 1.4, hemi .9 #ffffff / #cfd8c8; K3S.studioBackdrop({inner, mid, outer, cy}) and K3S.stageDisc({radius:.24, color:0x9dffb4, shadow:.5}) with a scan sweep.

**المعاملات:** key 2.6; fill .9; rim 1.4

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** studio · sweep · backdrop · product stage · استوديو

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:194`
- `kosif-one/tools/kosif-studio/motion/kit/shape-kit.js:336`

#### 7. قدرات قريبة في العائلة

- `3D-37` المواد الفيزيائية / Physical materials (glass, chrome, wet, iridescent) (ready)
- `3D-38` سلسلة ما بعد المعالجة / Post stack (bloom, ACES, film) (ready)
- `3D-40` مجسمات بطل جاهزة / Hero objects (geode, knot, coin) (ready)
- `3D-41` مشهد سينمائي بإطار واحد / Cinematic single-frame 3D page recipe (ready)

### `3D-40` — مجسمات بطل جاهزة / Hero objects (geode, knot, coin)

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جيود بلوري: قشرة معدنية داكنة بنواة متوهجة وحلقتين مداريتين تدور بسرعات مختلفة؛ عقدة طارة متوهجة؛ عملة كرومية. / Ready hero objects for tech/AI and finance.

**متى:** افتتاحيات تقنية وذكاء اصطناعي ومال / tech, AI and finance openers.

**كيف:** geode: IcosahedronGeometry(2.2, 2) MeshStandard #0f172a metalness .85 roughness .15; inner OctahedronGeometry(1.4) emissive #0284c7 ×.8; two TorusGeometry(3.6, .04, 16, 100) MeshBasic #38bdf8 at .6 tilted π/3 and π/4; rotations .45/.6/.8/.9/.3/.4 rad/s from t; knot: TubeGeometry torus knot (2,3) with gradient emissive; coin: extruded bevelled disc, metalness 1 roughness .2, ~40°/s tumble behind the headline.

**المعاملات:** shell r 2.2; core 1.4; rings 3.6

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** hero object · geode · torus knot · coin · مجسم بطل

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:128`
- `kosif-tool/styles/pm-eyishazyer-af035b`
- `kosif-tool/styles/pm-micheleharmonic-77628e`

#### 7. قدرات قريبة في العائلة

- `3D-38` سلسلة ما بعد المعالجة / Post stack (bloom, ACES, film) (ready)
- `3D-39` استوديو المنتج الكريمي / Studio sweep, backdrop & stage disc (ready)
- `3D-41` مشهد سينمائي بإطار واحد / Cinematic single-frame 3D page recipe (ready)
- `3D-42` نحت SDF وشبكة الأسطح / SDF sculpting & surface-nets mesher (proven)

### `3D-41` — مشهد سينمائي بإطار واحد / Cinematic single-frame 3D page recipe

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لقطة Three.js حتمية: مواد فيزيائية، مفتاح بارد بظلال ناعمة، نار دافئة متذبذبة، ضباب، جسيمات إضافية للنار والرذاذ، ومطر خطوط، وبلوم وفيلم. / A deterministic Three.js shot with cold key, flickering fire light, fog, additive particles, rain and bloom.

**متى:** لوحة ملحمية أو غلاف / epic stills and covers.

**كيف:** one HTML with an importmap to three@0.170; ACES exposure 1.55; PCFSoftShadowMap 2048; FogExp2 0x0d151f .013; cold DirectionalLight 0xcfe0ff 3.2; fire PointLight 0xff8a3a 140 flickering ±25 at 23 rad/s + SpotLight 0xffa050 220; Hemisphere 0x4a5e80 / 0x070a10 .9; bloom (.32, .5, .88); FilmPass .22; fov 46; set window.__ready after the first composer.render; render with html_render.py or film.py animate.

**المعاملات:** exposure 1.55; bloom .32/.5/.88

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cinematic still · fire light · fog · Three.js · لقطة سينمائية

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-studio/scenes/whale_dragon_3d.html:1`
- `kosif-one/tools/kosif-studio/scenes/whale_dragon_3d.html`
- `kosif-studio/references/drawing-guide.md:99`

#### 7. قدرات قريبة في العائلة

- `3D-39` استوديو المنتج الكريمي / Studio sweep, backdrop & stage disc (ready)
- `3D-40` مجسمات بطل جاهزة / Hero objects (geode, knot, coin) (ready)
- `3D-42` نحت SDF وشبكة الأسطح / SDF sculpting & surface-nets mesher (proven)
- `3D-43` حركات الكاميرا على مسار / Spline camera moves & narrated fly-throughs (ready)

### `3D-42` — نحت SDF وشبكة الأسطح / SDF sculpting & surface-nets mesher

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كرات وإهليلجات ومخاريط مدورة وصناديق وطارات تُدمج بنعومة وتُحفر وتُلوَّن، ثم تتحول إلى شبكة مغلقة بألوان رؤوس ونورمال من الحقل. / Smooth-unioned SDF primitives meshed into a watertight vertex-coloured mesh.

**متى:** تمائم، أشياء لطيفة، أشكال عضوية / mascots, cute objects, organic shapes.

**كيف:** const S = K3S.sculpt().sphere(c, r).ellipsoid(c, [rx, ry, rz], {rot}).capsule(a, b, r1, r2).box(c, [hx, hy, hz], round).torus(c, R, r) with {k, op, rot, color}, .paint(); geo = S.mesh({cells:96 (bunny 132), project, slack}) — coarse-to-fine surface nets (block 4 cells, refine near the surface, 2 Newton projection steps) → geometry.userData.stats {grid, evals, vertices, triangles, ms}; S.hit(from, dir, maxDist) ray-marches (256 steps, step .8·d) to place eyes/buttons exactly on the surface. Tests passed here: sphere volume ratio .9996, area .9998, 0 open edges, 56% of the grid evaluated; bunny > 50k triangles (≈274k at full res in ~4 s).

**المعاملات:** cells 96–136; block 4

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** SDF · sculpt · surface nets · mesh · نحت

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:183`
- `100-superskills/skills/kosif-montage-motion/tests/test_shape_kit.py:21`
- `kosif-studio/motion/kit/shape-kit.js:183`

#### 7. قدرات قريبة في العائلة

- `3D-40` مجسمات بطل جاهزة / Hero objects (geode, knot, coin) (ready)
- `3D-41` مشهد سينمائي بإطار واحد / Cinematic single-frame 3D page recipe (ready)
- `3D-43` حركات الكاميرا على مسار / Spline camera moves & narrated fly-throughs (ready)
- `3D-44` المنصة الدوارة للمنتج / Product turntable recipe (documented)

### `3D-43` — حركات الكاميرا على مسار / Spline camera moves & narrated fly-throughs

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كاميرا على مسار Catmull-Rom بحركة واحدة لكل لقطة، مدار هادئ، أو تحليق تتزامن نقاطه مع كلمات التعليق. / Catmull-Rom camera paths, one move per shot, gentle orbits, narration-locked fly-throughs.

**متى:** كل لقطة 3D / every 3D shot.

**كيف:** python3 tools/kosif.py scaffold cinematic-3d <dir>; CatmullRom paths 2–5 s ease-in-out sine; orbit 10–25°/s; fov 40–55; three camera keys per template shot (scene3d: fov 38, sun elevation 6 → 26°, azimuth 165 → 115°, exposure .46 → .58); narration-locked: waypoint times from words.json (e.g. 4 waypoints in 6 s); chaptered scale tour: tween position/target 2.5 s easeInOutCubic between chapter waypoints; reusable 3D set as an explainer stage with 6–12 s eased dolly/orbit per chapter (fov 35–50°); lines on the ground as thin quads 2 mm above the mesh so they follow perspective and get occluded.

**المعاملات:** 2–5 s paths; orbit 10–25°/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** camera path · spline · fly-through · orbit · كاميرا

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/cinematic-3d/SKILL.md`
- `kosif-tool/playbooks/3d.md:48`
- `kosif-studio/motion/templates/scene3d/src/main.js`
- `kosif-tool/styles/pm-blueoctopusai-dd17bd`

#### 7. قدرات قريبة في العائلة

- `3D-41` مشهد سينمائي بإطار واحد / Cinematic single-frame 3D page recipe (ready)
- `3D-42` نحت SDF وشبكة الأسطح / SDF sculpting & surface-nets mesher (proven)
- `3D-44` المنصة الدوارة للمنتج / Product turntable recipe (documented)
- `3D-45` المنظر المفكك / Exploded view (documented)

### `3D-44` — المنصة الدوارة للمنتج / Product turntable recipe

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** المنتج يسقط على قاعدة، يدور 90° مع اقتراب، تُرسم تسمية، ثم ثبات بطل. / Product drops on a plinth, orbits 90° with push-in, callout draws, hero hold.

**متى:** إعلانات منتجات / product ads.

**كيف:** 0–0.6 s drop (ease-in quad + spring damping 12); 0.6–4.6 s orbit 90° (sine in-out) with push-in; 2.0–2.4 s callout draws (ease-out cubic, EXPL-29); 4.6–6.0 s hero hold; for a full 360° loop use HyperFrames product-turntable (3D-13) or K3.shot('turntable') holds (CHAR-45).

**المعاملات:** 0.6 / 4.6 / 6.0 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** turntable · product · plinth · منصة دوارة

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/playbooks/3d.md:35`

#### 7. قدرات قريبة في العائلة

- `3D-42` نحت SDF وشبكة الأسطح / SDF sculpting & surface-nets mesher (proven)
- `3D-43` حركات الكاميرا على مسار / Spline camera moves & narrated fly-throughs (ready)
- `3D-45` المنظر المفكك / Exploded view (documented)
- `3D-46` سيارة مفككة بالتوليد / Generated car exploded-view pipeline (key)

### `3D-45` — المنظر المفكك / Exploded view

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أجزاء المنتج تبتعد على محاور منطقية مع تسميات قصيرة ثم تعود / دون اختراع أجزاء داخلية. — Parts move apart along sensible axes with short labels, then reassemble — never inventing internals.

**متى:** «ما بداخل المنتج» / 'what's inside'.

**كيف:** MG-031: 0–1 s product, 1–3 s explode, 3–5 s labels, 5–7 s reassemble; offset child meshes along their normals or Y with a 150 ms stagger; independent PNG layers in an HTML stack when no model exists; HyperFrames exploded-stack for isometric layer plates; K3.schematic explode (EXPL-52) for characters.

**المعاملات:** 7 s; stagger 150 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** exploded view · parts · product · تفكيك

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-product-ads.md`
- `kosif-tool/styles/pm-mdaman010-e7226a`
- `kosif-tool/styles/pm-sayan-shanky-f850d8`

#### 7. قدرات قريبة في العائلة

- `3D-43` حركات الكاميرا على مسار / Spline camera moves & narrated fly-throughs (ready)
- `3D-44` المنصة الدوارة للمنتج / Product turntable recipe (documented)
- `3D-46` سيارة مفككة بالتوليد / Generated car exploded-view pipeline (key)
- `3D-47` المقاطع العرضية ومشاهد التضاريس العلمية / Cutaways & honest terrain science scenes (documented)

### `3D-46` — سيارة مفككة بالتوليد / Generated car exploded-view pipeline

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** من صورة السيارة إلى منظر مفكك صورةً لصورة، ثم فيديو 8 ث: انجراف بدخان، توقف، تفكك موجّه، وإعادة تركيب. / Car photo → image-to-image exploded view → 8 s drift / explode / reassemble clip.

**متى:** إعلانات سيارات وتريندات «التفكيك» / car ads and exploded-view trends.

**كيف:** fastify car-exploded profile: 47 makers in 5 groups / 154 models drive the BRAND → MODEL → DETAILS menus (profile tests passed here); prompt 2 separates hood, panels, wheels, tyres, interior, seats, chassis and drivetrain on a dark-grey gradient using image 1 as the mandatory base (keep uncertain internals generic); prompt 3 uses IMAGE 1 (assembled) + IMAGE 2 (exploded) as anchors: 0–2 s drift in with tyre smoke, 2–3 s hold with a gentle 3/4 orbit, 3–5.5 s servo-guided separation, 5.5–8 s exact reverse reassembly. Same family of locked settings: storybook park world (late golden hour, round trees, cobblestone path). Needs an image-to-image and a video generator key.

**المعاملات:** 0–2 / 2–3 / 3–5.5 / 5.5–8 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** car · exploded · image to video · generation · سيارة

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `fastify-motion-bro/scripts/profiles/car-exploded.mjs`
- `fastify-motion-bro/tests/production-profiles.test.mjs`
- `fastify-motion-bro/scripts/profiles/character-romance.mjs`

#### 7. قدرات قريبة في العائلة

- `3D-44` المنصة الدوارة للمنتج / Product turntable recipe (documented)
- `3D-45` المنظر المفكك / Exploded view (documented)
- `3D-47` المقاطع العرضية ومشاهد التضاريس العلمية / Cutaways & honest terrain science scenes (documented)
- `3D-48` عنصر واحد يحمل القصة / Persistent subject across chapters (documented)

### `3D-47` — المقاطع العرضية ومشاهد التضاريس العلمية / Cutaways & honest terrain science scenes

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مستويات قطع متحركة تكشف الداخل، وتضاريس بلوح ماء عند مستوى البحر، مع مسطرة مقياس وتصريح بالتضخيم الرأسي. / Animated clipping planes and terrain with a sea-level sheet, scale bars and stated vertical exaggeration.

**متى:** زلازل، مياه جوفية، سدود، تشريح أجهزة / earthquakes, aquifers, dams, device anatomy.

**كيف:** Three.js renderer.localClippingEnabled + material.clippingPlanes animated between named states (1 s reveal), colour-code internals; name what is measured vs schematic; correct terms (epicentre at the surface, hypocentre underground); scale/depth axes; water as a sea-level sheet over submerged terrain; compute cut faces from object bounds; capture 2+ rotation angles for QA.

**المعاملات:** 1 s reveal

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cutaway · clipping plane · terrain science · مقطع عرضي

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/cutaway-terrain-and-domain-scenes.md`
- `kosif-tool/styles/pm-konstantinsaifo-96fc89`

#### 7. قدرات قريبة في العائلة

- `3D-45` المنظر المفكك / Exploded view (documented)
- `3D-46` سيارة مفككة بالتوليد / Generated car exploded-view pipeline (key)
- `3D-48` عنصر واحد يحمل القصة / Persistent subject across chapters (documented)
- `3D-49` النص داخل المشهد ثلاثي الأبعاد / Type in 3D space (seen)

### `3D-48` — عنصر واحد يحمل القصة / Persistent subject across chapters

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مجسم واحد يحمل السرد كله: مجمّع، مفكك، آلية داخلية، ثم يعاد تجميعه / بخط زمني طبيعي 0–1. — One object carries the whole narrative across chapters.

**متى:** شرح منتج طويل / long product explainers.

**كيف:** one persistent scene; lathe geometry + instanced detail; a normalised 0–1 timeline drives the poses (map it to frame time for video); a white-model look (white MeshStandard, soft light, colour only on flows) keeps attention on the mechanism.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** persistent subject · chapters · product story · عنصر واحد

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/examples/cinematic/README.md`
- `kosif-tool/styles/pm-mdaman010-e7226a`

#### 7. قدرات قريبة في العائلة

- `3D-46` سيارة مفككة بالتوليد / Generated car exploded-view pipeline (key)
- `3D-47` المقاطع العرضية ومشاهد التضاريس العلمية / Cutaways & honest terrain science scenes (documented)
- `3D-49` النص داخل المشهد ثلاثي الأبعاد / Type in 3D space (seen)
- `3D-50` أزرار وأجهزة ثلاثية الأبعاد / 3D product interactions (button, lid) (seen)

### `3D-49` — النص داخل المشهد ثلاثي الأبعاد / Type in 3D space

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نص ملفوف على كرة دوّارة، كلمة مبثوقة، ممر من كلمات عملاقة، أو مكعب كلمات / والعربية دائمًا على خامة مرسومة لا هندسة مبثوقة. — Text on a spinning sphere, extruded words, word corridors — Arabic always on a drawn texture.

**متى:** عناوين مذهلة ثلاثية الأبعاد / spectacular 3D titles.

**كيف:** paragraph drawn to a canvas texture (Arabic: ctx.direction='rtl', whole shaped line, ARAB-10) mapped on a sphere (30% H, 15°/s) over an emissive fire-noise shader with a fresnel rim #ff9a2a; Latin TextGeometry depth .3 em (cream face, orange sides) rotating from −30° Y over 900 ms easeOutCubic, or stacked offset layers; corridor: text planes along z with a dolly; never extrude Arabic from an unshaped font.

**المعاملات:** sphere 30% H; 15°/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** 3D text · canvas texture · extrude · Arabic 3D · نص ثلاثي

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/pm-ajith-io-4c248f`
- `kosif-tool/styles/pm-sahildesigner23-ee3155`
- `kosif-tool/styles/pm-itisrazak-3ad902/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `3D-47` المقاطع العرضية ومشاهد التضاريس العلمية / Cutaways & honest terrain science scenes (documented)
- `3D-48` عنصر واحد يحمل القصة / Persistent subject across chapters (documented)
- `3D-50` أزرار وأجهزة ثلاثية الأبعاد / 3D product interactions (button, lid) (seen)
- `3D-51` الأرض يرسمها الصوت / Music-driven 3D land (ready)

### `3D-50` — أزرار وأجهزة ثلاثية الأبعاد / 3D product interactions (button, lid)

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لقطة منخفضة لصندوق زر أركيد بإضاءة حافة حمراء/زرقاء يضغطه مؤشر فينخفض بوميض، وغطاء حاسوب يُغلق 110°←0°. / A low-angle arcade button pressed with a flash, and a laptop lid closing 110° → 0°.

**متى:** إعلانات تقنية وألعاب / tech and game ads.

**كيف:** button press 150 ms with complementary rim lights and an emissive flash; hinge-rotate the lid 110° → 0° in ~1 s ease-in-out while the screen dims; hidden-object beat: hint (tail flick 2–4 s, glint 120 ms) then pop 0.8 → 1 with cubic-bezier(.34,1.56,.64,1) in 350 ms and a 3-stroke sparkle.

**المعاملات:** press 150 ms; lid ~1 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** button press · laptop · product interaction · زر

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/pm-spearwtf-3c1fd1`
- `kosif-tool/styles/pm-cansincengiz-me-cf68dd`
- `kosif-tool/styles/pm-mandelduck-95fd08/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `3D-48` عنصر واحد يحمل القصة / Persistent subject across chapters (documented)
- `3D-49` النص داخل المشهد ثلاثي الأبعاد / Type in 3D space (seen)
- `3D-51` الأرض يرسمها الصوت / Music-driven 3D land (ready)
- `3D-52` أفكار ثلاثية الأبعاد غير منفذة / Unbuilt 3D ideas (idea)

### `3D-51` — الأرض يرسمها الصوت / Music-driven 3D land

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل قيمة من تحليل الموسيقى: الطيف يصير وادٍ، الجهير نهر حمم، الركلات ترمي شرارات وتضغط كرة كروم، وعند توقف الشريط يتجمد العالم والكاميرا تنجرف. / Every value from the score: spectrogram canyon, bass lava river, kick sparks, tape-stop bullet time.

**متى:** كليبات موسيقية تجريبية / experimental music visuals.

**كيف:** three-kit makeSpectrumGround + spectrumOnTape + makeSparks + makeGlitchPass fed by channels.json and spectrum_height.png (motion.py channels TRACK.wav); 8 tape-seconds across 120 m; fog #1A0A16 .018; fov 36; silence flips the picture negative; spin-up whips the camera home.

**المعاملات:** 8 tape-s over 120 m

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** music visualizer · spectrogram · audio reactive · 3D · صوت

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-studio/motion/projects/sound_ground/src/main.js:1`

#### 7. قدرات قريبة في العائلة

- `3D-49` النص داخل المشهد ثلاثي الأبعاد / Type in 3D space (seen)
- `3D-50` أزرار وأجهزة ثلاثية الأبعاد / 3D product interactions (button, lid) (seen)
- `3D-52` أفكار ثلاثية الأبعاد غير منفذة / Unbuilt 3D ideas (idea)
- `3D-G01` حلقة رندر three.js حتمية / Deterministic three.js render loop (documented)

### `3D-52` — أفكار ثلاثية الأبعاد غير منفذة / Unbuilt 3D ideas

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كاميرا مشي بمنظور الشخص الأول داخل لوحة، مجرة نقاط المعاني، مشهد «مجرة المراجعة»، وسرد ثلاثي بالتمرير / أفكار بلا كود جاهز. — First-person walks, embedding galaxies, an audit galaxy and scroll-driven 3D — no ready code.

**متى:** حين يطلب المستخدم شيئًا جديدًا من هذا النوع / when a user asks for one of these.

**كيف:** first-person walk: 1.4 m/s, head bob 2 cm at 1.8 Hz, FOV 70°, no cuts, low-poly scene in a painting's palette; embedding galaxy: UMAP/t-SNE computed offline, WebGL points, fly between labelled clusters, state that distances are approximate; audit galaxy: central 'financial core' sphere + orbital risk network + evidence nodes (config object only); scroll-world: pre-rendered camera dives scrubbed by scroll (vendor skill; needs AI clips) — for video, drive the same timeline by t; kosif-tool styles scroll-world and lowpoly-3d (flatShading, roughness .6–.9, drop-in 0.4 s + spring 12) scaffold the look.

**المعاملات:** 1.4 m/s; bob 2 cm @1.8 Hz

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** first person · embedding galaxy · scroll world · ideas · أفكار

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/styles/pm-mandelduck-95fd08/BRIEF.md`
- `kosif-audit-studio/cinema/threeAuditScene.js`
- `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md`
- `kosif-tool/styles/lowpoly-3d/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `3D-50` أزرار وأجهزة ثلاثية الأبعاد / 3D product interactions (button, lid) (seen)
- `3D-51` الأرض يرسمها الصوت / Music-driven 3D land (ready)
- `3D-G01` حلقة رندر three.js حتمية / Deterministic three.js render loop (documented)

### `3D-G01` — حلقة رندر three.js حتمية / Deterministic three.js render loop

| الحقل | القيمة |
|---|---|
| العائلة | `3d-spatial` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/3d-spatial.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** حرّك المشهد بالزمن لا بعدد الإطارات، واضبط الألوان والدقة مرة واحدة، وفي التصدير اجعل الزمن مدخلًا تبحث إليه لا ساعة حقيقية. — Drive the scene by time, not frame count, set colour and resolution once, and for export make time an input you seek to, not the wall clock.

**متى:** مشهد ثلاثي الأبعاد للويب أو لفيديو / a 3D scene for the web or for a video

**كيف:** update(t) sets every transform from t; live: t from a clock delta; export: t = frame / fps (no requestAnimationFrame timing). renderer.setPixelRatio(min(devicePixelRatio, 2)), sRGB output colour space, ACES filmic tone mapping with exposure ≈1; damped orbit controls need update() every frame; dispose geometries, materials and textures when a shot ends. Render frames headless and verify duration and fps (tools/verify_video.py).

**المعاملات:** pixel ratio ≤ 2; export t = frame/fps

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** three.js · render loop · deterministic · tone mapping · webgl · ثري جي إس · ثلاثي الأبعاد · رندر

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:3D-G01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-api-audit` · `blender-bridge` · `blender-cat-fur-upgrade` · `blender-cinematic-bridge` · `blender-cycles-render` · `blender-rescue-scene`.
- مراحل النوع: المقياس والوحدات ← المجسم ← الخامات والإضاءة ← معاينة منخفضة ← رندر ← فتح في عارض مستقل.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المقياس والوحدات صحيحة ← قياس الأبعاد
- إلزامي: الملف يُفتح في عارض مستقل ← عارض glTF
- جودة: الإضاءة والكاميرا تخدم القراءة ← لقطات ثابتة
- جودة: زمن الرندر ضمن المتاح، بمعاينة قبله ← توقيت إطار واحد × عدد الإطارات
- أمر الحكم في الوضع 1: `think.py qa model3d --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `3D-51` الأرض يرسمها الصوت / Music-driven 3D land (ready)
- `3D-52` أفكار ثلاثية الأبعاد غير منفذة / Unbuilt 3D ideas (idea)

