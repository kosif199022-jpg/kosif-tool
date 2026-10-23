# `texture-material` — الثري دي والمحاكاة والرندر (96 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/texture-material.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/3d.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`TEX-01` حبيبات SVG متدرجة قابلة للبحث](#tex-01--حبيبات-svg-متدرجة-قابلة-للبحث--seekable-stepped-svg-grain-motion-kit)
- [`TEX-02` حبيبات ببذرة رقم الإطار](#tex-02--حبيبات-ببذرة-رقم-الإطار--frame-seeded-grain-seek-pages)
- [`TEX-03` حبيبات غاوسية في Pillow](#tex-03--حبيبات-غاوسية-في-pillow--seeded-gaussian-luminance-grain-studio-painter)
- [`TEX-04` سلسلة تشطيب ffmpeg](#tex-04--سلسلة-تشطيب-ffmpeg--ffmpeg-film-finish-chain)
- [`TEX-05` مطابقة اللوك: تعتيم وحبيبات وأشرطة](#tex-05--مطابقة-اللوك-تعتيم-وحبيبات-وأشرطة--look-replication-solver-vignettegrainletterboxfades)
- [`TEX-06` حبيبات ثلاثية الأبعاد (FilmPass)](#tex-06--حبيبات-ثلاثية-الأبعاد-filmpass--3d-film-grain-pass)
- [`TEX-07` حبيبات 2% وانحراف لوني على الحواف](#tex-07--حبيبات-2-وانحراف-لوني-على-الحواف--2-grain--edge-only-chromatic-aberration)
- [`TEX-08` تلوين عتيق بغبار وخدوش](#tex-08--تلوين-عتيق-بغبار-وخدوش--vintage-film-grade-dust-scratches-split-tone)
- [`TEX-09` أسود دافئ بحبيبات وتعتيم](#tex-09--أسود-دافئ-بحبيبات-وتعتيم--warm-black-grain--vignette-grade)
- [`TEX-10` درجة الورق التحريري](#tex-10--درجة-الورق-التحريري--editorial-paper-grade)
- [`TEX-11` حبيبات مع زوايا HUD](#tex-11--حبيبات-مع-زوايا-hud--film-grain--hud-corners)
- [`TEX-12` عنوان محبب متوهج](#tex-12--عنوان-محبب-متوهج--grain-glow-title-card)
- [`TEX-13` خلفية ورق ثابتة 5–10%](#tex-13--خلفية-ورق-ثابتة-510--static-paperboard-texture)
- [`TEX-14` ورق ألوان مائية](#tex-14--ورق-ألوان-مائية--watercolour-paper-ground)
- [`TEX-15` رق قديم بحواف ونقاط رمل](#tex-15--رق-قديم-بحواف-ونقاط-رمل--parchment-vignette--sand-stipple)
- [`TEX-16` كولاج ورقي (S04)](#tex-16--كولاج-ورقي-s04--paper-collage-style-s04)
- [`TEX-17` لوحة قصاصات وشريط يثبّتها](#tex-17--لوحة-قصاصات-وشريط-يثبّتها--cut-out-board--tape-pin-mg-101102)
- [`TEX-18` تمزيق ورق يكشف ما تحته](#tex-18--تمزيق-ورق-يكشف-ما-تحته--paper-tear-reveal)
- [`TEX-19` رسمة ممسوحة كملصق](#tex-19--رسمة-ممسوحة-كملصق--scanned-drawing-as-sticker-cut-out)
- [`TEX-20` قصاصة جريدة ونقش](#tex-20--قصاصة-جريدة-ونقش--newspaper--engraving-cut-out)
- [`TEX-21` قفل أسلوب الأرشيف](#tex-21--قفل-أسلوب-الأرشيف--archival-scrapbook-style-lock)
- [`TEX-22` قفل الخلفية الورقية](#tex-22--قفل-الخلفية-الورقية--paper-sketch-background-lock)
- [`TEX-23` الورق المقصوص بعمق ثلاث طبقات](#tex-23--الورق-المقصوص-بعمق-ثلاث-طبقات--paper-cut-out-style-3-depth-parallax)
- [`TEX-24` ستوب موشن بارتعاش البذرة](#tex-24--ستوب-موشن-بارتعاش-البذرة--stop-motion-seeded-hold-jitter)
- [`TEX-25` صلصال مطفي وبصمات](#tex-25--صلصال-مطفي-وبصمات--claymation-matte--fingerprint-texture)
- [`TEX-26` مشهد أطفال بالكرايون](#tex-26--مشهد-أطفال-بالكرايون--crayon-paper-craft-kids-scene)
- [`TEX-27` النقص المقصود](#tex-27--النقص-المقصود--intentional-imperfection-wabi-sabi)
- [`TEX-28` إزالة الخلفية بلون الزاوية](#tex-28--إزالة-الخلفية-بلون-الزاوية--corner-colour-background-knockout)
- [`TEX-29` تظليل كرة بالهالفتون](#tex-29--تظليل-كرة-بالهالفتون--halftone-sphere-lambert-dots)
- [`TEX-30` هالفتون CMYK](#tex-30--هالفتون-cmyk--cmyk--gooey-halftone)
- [`TEX-31` نقاط هالفتون على القصاصة](#tex-31--نقاط-هالفتون-على-القصاصة--clipped-halftone-on-a-cut-out-card)
- [`TEX-32` موجة هالفتون ومواريه](#tex-32--موجة-هالفتون-ومواريه--halftone-ripple--moiré-overprint)
- [`TEX-33` خلفية أشرطة ضوء منقطة](#tex-33--خلفية-أشرطة-ضوء-منقطة--halftone-light-band-backdrop)
- [`TEX-34` صورة هالفتون ماكرو](#tex-34--صورة-هالفتون-ماكرو--halftone-macro-image)
- [`TEX-35` سماء متدرجة بتنقيط Bayer](#tex-35--سماء-متدرجة-بتنقيط-bayer--bayer-dithered-sky--stepped-stars)
- [`TEX-36` تعبئة تنقيط أحادية البت](#tex-36--تعبئة-تنقيط-أحادية-البت--1-bit-dither-fill-with-threshold-sweep)
- [`TEX-37` تعبئة حبيبات ريزو](#tex-37--تعبئة-حبيبات-ريزو--riso-grain-fill)
- [`TEX-38` طبقة حبيبات نقطية](#tex-38--طبقة-حبيبات-نقطية--dot-lattice-grain-overlay)
- [`TEX-39` مؤثرات الشيدر على الصورة والفيديو (18)](#tex-39--مؤثرات-الشيدر-على-الصورة-والفيديو-18--hyperframes-shader-media-effects-18-keys)
- [`TEX-40` بطاقة زجاجية فاخرة بعمق](#tex-40--بطاقة-زجاجية-فاخرة-بعمق--luxury-depth-glass-cards)
- [`TEX-41` وصفة الزجاج الداكن](#tex-41--وصفة-الزجاج-الداكن--dark-only-frosted-glass-panel-recipe)
- [`TEX-42` وصفات زجاج الواجهات](#tex-42--وصفات-زجاج-الواجهات--glassmorphism-ui-recipes-menus-toasts-bars-dialogs)
- [`TEX-43` غلاف زجاجي فوق عالم ثلاثي](#tex-43--غلاف-زجاجي-فوق-عالم-ثلاثي--glass-shell-over-a-live-3d-background)
- [`TEX-44` زجاج سائل بانكسار الحافة](#tex-44--زجاج-سائل-بانكسار-الحافة--liquid-glass-control-edge-refraction)
- [`TEX-45` حروف وأشكال من زجاج متجمد](#tex-45--حروف-وأشكال-من-زجاج-متجمد--frosted-glass-shapes-and-letters)
- [`TEX-46` زجاج بانكسار وتشتت لوني (3D)](#tex-46--زجاج-بانكسار-وتشتت-لوني-3d--refraction--chromatic-dispersion-glass)
- [`TEX-47` ذهب معدني بلمعة متحركة](#tex-47--ذهب-معدني-بلمعة-متحركة--metallic-gold-with-moving-sheen)
- [`TEX-48` كرة لامعة من تدرجات](#tex-48--كرة-لامعة-من-تدرجات--glossy-2d-sphere--orb-from-gradients)
- [`TEX-49` كروم يعكس المشهد حيًا](#tex-49--كروم-يعكس-المشهد-حيًا--chrome-via-live-cubecamera-reflection)
- [`TEX-50` ظلال ارتفاع ناعمة متعددة](#tex-50--ظلال-ارتفاع-ناعمة-متعددة--layered-soft-elevation-shadows)
- [`TEX-51` نسيج الضوضاء الكسرية](#tex-51--نسيج-الضوضاء-الكسرية--fractal-value-noise-material-studio-painter)
- [`TEX-52` نقش الحراشف والقرميد](#tex-52--نقش-الحراشف-والقرميد--scales--tiles-pattern)
- [`TEX-53` إضاءة بارزة بخريطة ارتفاع](#tex-53--إضاءة-بارزة-بخريطة-ارتفاع--relief-lighting-height-field--sss)
- [`TEX-54` سطح ماء يلمع](#tex-54--سطح-ماء-يلمع--water-surface-with-light-glints-studio)
- [`TEX-55` ضوضاء بيرلين وfbm وridged ببذرة](#tex-55--ضوضاء-بيرلين-وfbm-وridged-ببذرة--seeded-cpu-perlin--fbm--ridged-noise)
- [`TEX-56` خامات مولّدة بلا تنزيل](#tex-56--خامات-مولّدة-بلا-تنزيل--generated-textures-noisecanvas--normalfromheight--spritetex)
- [`TEX-57` خامة بدن خشبي مدهون](#tex-57--خامة-بدن-خشبي-مدهون--procedural-painted-wooden-hull)
- [`TEX-58` خامة قمر إجرائية](#tex-58--خامة-قمر-إجرائية--procedural-moon-texture)
- [`TEX-59` طوب إجرائي يتلوّن بالضوء](#tex-59--طوب-إجرائي-يتلوّن-بالضوء--procedural-brick-lit-by-a-light-map-multiply)
- [`TEX-60` غيوم SVG إجرائية](#tex-60--غيوم-svg-إجرائية--procedural-svg-clouds-feturbulence--displacement)
- [`TEX-61` كلمة عربية مملوءة بسائل](#tex-61--كلمة-عربية-مملوءة-بسائل--fluid-noise-filled-arabic-word)
- [`TEX-62` نص بأقنعة الخامات (66 قناعًا)](#tex-62--نص-بأقنعة-الخامات-66-قناعًا--texture-mask-text-66-pbr-masks)
- [`TEX-63` كتل شيدر المواد (WebGPU)](#tex-63--كتل-شيدر-المواد-webgpu--hyperframes-material-shader-blocks)
- [`TEX-64` حقل الحبيبات ونزف الحبر](#tex-64--حقل-الحبيبات-ونزف-الحبر--grain-field--ink-bleed-reveal-hyperframes)
- [`TEX-65` غيوم بخطوط فرشاة وسماء سديمية](#tex-65--غيوم-بخطوط-فرشاة-وسماء-سديمية--painterly-streak-clouds--nebula-skies)
- [`TEX-66` أرضية حمم بعروق مضيئة](#tex-66--أرضية-حمم-بعروق-مضيئة--veined-lava-floor-shader)
- [`TEX-67` شيدر ضربات فرشاة](#tex-67--شيدر-ضربات-فرشاة--stroke-based-painterly-shader)
- [`TEX-68` طبقات درجات للفرشاة الجافة](#tex-68--طبقات-درجات-للفرشاة-الجافة--tone-layers-for-a-dry-brush-look-rotoscope)
- [`TEX-69` فحص قابلية التكرار للخامات المولدة](#tex-69--فحص-قابلية-التكرار-للخامات-المولدة--seamless-tile-check-for-ai-textures)
- [`TEX-70` كتيب وصفات المواد للرسام](#tex-70--كتيب-وصفات-المواد-للرسام--material-recipe-sheet-flame-spray-steam-fur-atmosphere)
- [`TEX-71` تدرج شبكي وشبكة خطوط](#tex-71--تدرج-شبكي-وشبكة-خطوط--mesh-gradient--grid-backgrounds)
- [`TEX-72` ست خلفيات نقشية متحركة](#tex-72--ست-خلفيات-نقشية-متحركة--basma-animated-pattern-backgrounds-6--gradient)
- [`TEX-73` شبكة خطوط قطرية منجرفة](#tex-73--شبكة-خطوط-قطرية-منجرفة--drifting-diagonal-line-grid)
- [`TEX-74` شبكة نقطية تحريرية دقيقة](#tex-74--شبكة-نقطية-تحريرية-دقيقة--fine-dot-dash-editorial-grid)
- [`TEX-75` ورق مربعات وشبكة قياس](#tex-75--ورق-مربعات-وشبكة-قياس--graph-paper--graticule-grids)
- [`TEX-76` جدار نص وبيانات خافت](#tex-76--جدار-نص-وبيانات-خافت--faint-datatext-wall)
- [`TEX-77` أفق مدينة ليلي إجرائي](#tex-77--أفق-مدينة-ليلي-إجرائي--procedural-night-skyline-with-lit-windows)
- [`TEX-78` انعكاسات الشارع المبتل](#tex-78--انعكاسات-الشارع-المبتل--wet-street--floor-reflections)
- [`TEX-79` سبورة بآثار مسح](#tex-79--سبورة-بآثار-مسح--whiteboard-eraser-smudge-texture)
- [`TEX-80` حبيبات الطباشير](#tex-80--حبيبات-الطباشير--chalk-grain-overlay)
- [`TEX-81` تهشير داخل حدود الشكل](#tex-81--تهشير-داخل-حدود-الشكل--clipped-hatching--scribble-fill)
- [`TEX-82` أرضيات ورقية وبلاط](#tex-82--أرضيات-ورقية-وبلاط--paper-doodle-ground--tile-floor)
- [`TEX-83` مثال الحبيبات الدافئة](#tex-83--مثال-الحبيبات-الدافئة--warm-grain-example-project-hyperframes)
- [`TEX-84` عائلة مواد مطفية واحدة](#tex-84--عائلة-مواد-مطفية-واحدة--one-matte-material-family)
- [`TEX-85` وصفات PBR سريعة](#tex-85--وصفات-pbr-سريعة--quick-pbr-recipes-threejs)
- [`TEX-86` خامة القطيفة المحشوة](#tex-86--خامة-القطيفة-المحشوة--plush-felt-material-velvet-sheen--fibre)
- [`TEX-87` لمعان clearcoat للعين والأنف](#tex-87--لمعان-clearcoat-للعين-والأنف--glossy-clearcoat--eye-with-catch-lights)
- [`TEX-88` طقم مواد المختبر](#tex-88--طقم-مواد-المختبر--lab-material-set-plushglossleathermetal)
- [`TEX-89` فرو بالطبقات](#tex-89--فرو-بالطبقات--shell-fur)
- [`TEX-90` بقع لونية على المجسم](#tex-90--بقع-لونية-على-المجسم--colour-paint-stamps-on-sdf)
- [`TEX-91` شفافية الأشعة السينية للدمية](#tex-91--شفافية-الأشعة-السينية-للدمية--plush-x-ray-during-analysis)
- [`TEX-92` حصى وقصب](#tex-92--حصى-وقصب--pebbles--reed-blades)
- [`TEX-93` قاع بركة بانكسارات ضوئية](#tex-93--قاع-بركة-بانكسارات-ضوئية--pond-bed-terrain-with-caustics)
- [`TEX-94` أسفلت مبلل وطلاء عاكس](#tex-94--أسفلت-مبلل-وطلاء-عاكس--wet-asphalt--retro-reflective-road-paint)
- [`TEX-X01` حبيبات فيلم صحيحة](#tex-x01--حبيبات-فيلم-صحيحة--film-grain-done-right-post-mortem)
- [`TEX-X02` سلسلة مرور أرشيفية](#tex-x02--سلسلة-مرور-أرشيفية--archival-post-chain-order-webgl)

## البطاقات / cards

### `TEX-01` — حبيبات SVG متدرجة قابلة للبحث / Seekable stepped SVG grain (motion-kit)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طبقة feTurbulence رمادية تقفز بين 6 مواضع بخطوات CSS، فتتحرك الحبيبات ويظل كل إطار قابلًا للبحث. / Desaturated feTurbulence overlay that jumps between 6 offsets with steps(1), so grain moves yet every frame is seekable.

**متى:** حين تريد حبيبات فيلم متحركة فوق مشهد ويب مع بقاء كل إطار قابلًا للبحث والتصيير / when you need moving film grain over a web scene that stays seekable frame by frame

**كيف:** MOTION.grain(stage,{opacity,blend,freq,seed,z}) builds an SVG with feTurbulence fractalNoise + feColorMatrix saturate 0 on a 200% rect, animated by @keyframes mk-grain-jump 0.6 s steps(1). Pair with MOTION.vignette(stage,{inner:55,strength:.42}). Rendered here in virtual-time mode: frame-to-frame change only at the step boundaries, corners darkened 205→152 luma.

**المعاملات:** opacity .09 (projects use .05–.07), soft-light, baseFrequency .9, 2 octaves, 0.6 s loop of 6 positions; vignette inner 55%, strength .42–.5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حبيبات · فيلم · grain · film grain · feTurbulence · seekable · vignette · تعتيم · ملمس سينمائي · نويز · ضوضاء · noise overlay · svg filter

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-studio/motion/kit/motion-kit.js:440`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:440`
- `kosif-one/projects/thursday-dua-animation/source/index.html`
- `kosif-one/projects/whatsapp-motion/projects/success/index.html`

#### 7. قدرات قريبة في العائلة

- `TEX-02` حبيبات ببذرة رقم الإطار / Frame-seeded grain (seek pages) (proven)
- `TEX-03` حبيبات غاوسية في Pillow / Seeded Gaussian luminance grain (Studio painter) (ready)

### `TEX-02` — حبيبات ببذرة رقم الإطار / Frame-seeded grain (seek pages)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بدل الحركة بالـCSS، غيّر seed للفلتر من رقم الإطار داخل seek(t) فتولد حبيبات جديدة كل إطار بلا عشوائية. / Inside seek(t) set the feTurbulence seed from the frame number, so grain is fresh every frame and still deterministic.

**متى:** عند الحاجة لحبيبات تتجدد كل إطار وتعطي النتيجة نفسها عند إعادة التصيير داخل seek(t) / when grain must change every frame yet render identically on re-render via seek(t)

**كيف:** Keep one <filter><feTurbulence type=fractalNoise baseFrequency=.9 numOctaves=2> + saturate 0 over the stage with mix-blend-mode:soft-light; in seek: gt.setAttribute("seed", 1 + floor(t*24) % 97). For canvas, pre-make a 192×192 grey tile and translate it by a hash of the frame (Basma MK.grain). Rendered here: mean frame-to-frame delta 2.7 luma on a 360 px panel at 24 fps. (code snippet in references/powers/texture-material.md)

**المعاملات:** refresh 12–24 Hz; opacity 2–9%; soft-light or overlay

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حبيبات · بذرة · grain · seed · deterministic · seek · نويز متجدد · حبيبات متحركة · ضوضاء · per-frame noise · canvas grain

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/starters/html-canvas/index.html`
- `app/public/js/00_editor.js:75`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`

#### 7. قدرات قريبة في العائلة

- `TEX-01` حبيبات SVG متدرجة قابلة للبحث / Seekable stepped SVG grain (motion-kit) (proven)
- `TEX-03` حبيبات غاوسية في Pillow / Seeded Gaussian luminance grain (Studio painter) (ready)
- `TEX-04` سلسلة تشطيب ffmpeg / ffmpeg film finish chain (proven)

### `TEX-03` — حبيبات غاوسية في Pillow / Seeded Gaussian luminance grain (Studio painter)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عملية grain(amount, seed) في رسام KOSIF Studio تضيف حبيبات ضوئية ثابتة البذرة على الإطار كله. / KOSIF Studio painter op grain(amount, seed) adds seeded Gaussian luminance grain over the whole frame.

**متى:** حين ترسم إطارات برسام KOSIF Studio في Pillow وتريد حبيبات خفيفة فوق الإطار كله / when painting frames in the KOSIF Studio (Pillow) painter and adding light grain over the whole frame

**كيف:** Add grain() as the last op of the last step; keep amount tiny because H.264 smears it anyway; same seed across frames for a static print look, seed=frame for live grain.

**المعاملات:** typical .012–.02 (whale .018, duck .02, ad .012)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حبيبات · grain · pillow · studio · render.py · نويز · ضوضاء غاوسية · ملمس طباعة · gaussian noise · luminance grain

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-studio/render.py:791`
- `kosif-studio/references/drawing-guide.md`

#### 7. قدرات قريبة في العائلة

- `TEX-01` حبيبات SVG متدرجة قابلة للبحث / Seekable stepped SVG grain (motion-kit) (proven)
- `TEX-02` حبيبات ببذرة رقم الإطار / Frame-seeded grain (seek pages) (proven)
- `TEX-04` سلسلة تشطيب ffmpeg / ffmpeg film finish chain (proven)
- `TEX-05` مطابقة اللوك: تعتيم وحبيبات وأشرطة / Look replication solver (vignette/grain/letterbox/fades) (ready)

### `TEX-04` — سلسلة تشطيب ffmpeg / ffmpeg film finish chain

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بعد التلوين: حبيبات زمنية، تظليل أطراف π/5، هالة توهج خفيفة بالمزج screen، وأشرطة سينما 2.39:1 — في أمر واحد. / After grading: temporal grain, π/5 vignette, a light screen-blended bloom and 2.39:1 bars — one filtergraph.

**متى:** عند تشطيب فيديو بعد التلوين بحبيبات وتعتيم أطراف وتوهج وأشرطة سينما في أمر ffmpeg واحد / when finishing a graded video with grain, vignette, bloom and cinema bars in one ffmpeg command

**كيف:** Ran here on a 2 s test source (50 frames, OK). Order: grade → bloom → grain → vignette → bars; grain last-but-one so it is not blurred. For Remotion, a light-leak overlay sits on TransitionSeries.Overlay. (code snippet in references/powers/texture-material.md)

**المعاملات:** noise=alls=6–10:allf=t+u; vignette=PI/5; gblur sigma 20 + blend screen 0.25; letterbox via pad/drawbox

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ffmpeg · حبيبات · تعتيم · grain · vignette · bloom · letterbox · finish · أشرطة سينما · لوك سينمائي · توهج · cinematic look · filtergraph

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-atlas/skills/2712-remotion/10436-remotion-markup/transitions.md`

#### 7. قدرات قريبة في العائلة

- `TEX-02` حبيبات ببذرة رقم الإطار / Frame-seeded grain (seek pages) (proven)
- `TEX-03` حبيبات غاوسية في Pillow / Seeded Gaussian luminance grain (Studio painter) (ready)
- `TEX-05` مطابقة اللوك: تعتيم وحبيبات وأشرطة / Look replication solver (vignette/grain/letterbox/fades) (ready)
- `TEX-06` حبيبات ثلاثية الأبعاد (FilmPass) / 3D film grain pass (ready)

### `TEX-05` — مطابقة اللوك: تعتيم وحبيبات وأشرطة / Look replication solver (vignette/grain/letterbox/fades)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** kosif-mimic يحسب قوة التعتيم من نسبة إضاءة الزوايا إلى المركز، ويعوّض الحبيبات عما يمسحه ضغط H.264 حسب crf. / kosif-mimic solves vignette strength from the corner/centre luma ratio and boosts grain sigma to survive H.264 at a given crf.

**متى:** حين يريد المستخدم تقليد لوك فيديو مرجعي بقياس التعتيم والحبيبات والأشرطة والتلاشي بدل التخمين / when matching a reference video's look by measuring vignette, grain, letterbox and fades

**كيف:** mm_build.solve_vignette(ratio) → strength; grain_gain(crf) → multiplier for the measured grain; then add letterbox and fades as measured. Measure on the reference, never guess.

**المعاملات:** crf 17 default

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** محاكاة · mimic · grain · vignette · look match · مطابقة · تقليد الستايل · نفس اللوك · فيديو مرجعي · reference video · crf

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/mimic/mm_build.py`

#### 7. قدرات قريبة في العائلة

- `TEX-03` حبيبات غاوسية في Pillow / Seeded Gaussian luminance grain (Studio painter) (ready)
- `TEX-04` سلسلة تشطيب ffmpeg / ffmpeg film finish chain (proven)
- `TEX-06` حبيبات ثلاثية الأبعاد (FilmPass) / 3D film grain pass (ready)
- `TEX-07` حبيبات 2% وانحراف لوني على الحواف / 2% grain + edge-only chromatic aberration (documented)

### `TEX-06` — حبيبات ثلاثية الأبعاد (FilmPass) / 3D film grain pass

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تمريرة FilmPass في three-kit بزمن مربوط بإطار الإخراج، فتتحرك الحبيبات بحتمية في مشاهد WebGL. / three-kit post.film (three.js FilmPass) with its time uniform written from the output frame.

**متى:** عند إضافة حبيبات فيلم لمشهد three.js أو WebGL تتحرك بحتمية مع إطار الإخراج / when adding deterministic film grain to a three.js WebGL scene tied to the output frame

**كيف:** makeFrameLoop sets film.uniforms.time = t each frame; keep intensity low; TSL alternative film(color,{intensity,grayscale}) or a hash(uv+time) overlay in GLSL.

**المعاملات:** intensity .16 (lab .05); editorial ceiling ~2–3% visible grain

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** three.js · FilmPass · grain · post · حبيبات · مشهد ثلاثي الأبعاد · ملمس سينمائي · ما بعد المعالجة · webgl · post-processing

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:402`
- `kosif-studio/motion/kit/three-kit.js`
- `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/post-processing.md`

#### 7. قدرات قريبة في العائلة

- `TEX-04` سلسلة تشطيب ffmpeg / ffmpeg film finish chain (proven)
- `TEX-05` مطابقة اللوك: تعتيم وحبيبات وأشرطة / Look replication solver (vignette/grain/letterbox/fades) (ready)
- `TEX-07` حبيبات 2% وانحراف لوني على الحواف / 2% grain + edge-only chromatic aberration (documented)
- `TEX-08` تلوين عتيق بغبار وخدوش / Vintage film grade: dust, scratches, split-tone (seen)

### `TEX-07` — حبيبات 2% وانحراف لوني على الحواف / 2% grain + edge-only chromatic aberration

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قاعدة أواردز: حبيبات أحادية 2% لا تتجاوز 3%، وانزياح RGB صغير على أطراف الكادر فقط كعدسة حقيقية. / Awwwards rule: monochrome grain at 2% (never above 3%) and a tiny RGB split only near the frame edges.

**متى:** حين تريد ملمس عدسة حقيقية راقيًا: حبيبات خفيفة جدًا وانزياح ألوان على أطراف الكادر فقط / when you want a subtle real-lens finish: very light grain plus an RGB split only at the frame edges

**كيف:** Post pass offsetting R/B by distance from centre (shift ∝ r², 0 at centre); grain seeded per frame.

**المعاملات:** grain .02 (≤.03); RGB shift .002 uv at edges only

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** انحراف لوني · chromatic aberration · grain · lens · awwwards · حبيبات خفيفة · انزياح ألوان · تشوه العدسة · rgb split · subtle grain

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `TEX-05` مطابقة اللوك: تعتيم وحبيبات وأشرطة / Look replication solver (vignette/grain/letterbox/fades) (ready)
- `TEX-06` حبيبات ثلاثية الأبعاد (FilmPass) / 3D film grain pass (ready)
- `TEX-08` تلوين عتيق بغبار وخدوش / Vintage film grade: dust, scratches, split-tone (seen)
- `TEX-09` أسود دافئ بحبيبات وتعتيم / Warm-black grain + vignette grade (seen)

### `TEX-08` — تلوين عتيق بغبار وخدوش / Vintage film grade: dust, scratches, split-tone

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تمريرة أخيرة: تقسيم لوني دافئ/بنفسجي، حبيبات متحركة، ذرات غبار متفرقة وخدوش عمودية، تعتيم وتوهج خفيف. / Final pass: warm/violet split-tone, animated grain, sparse dust specks and vertical scratches, slight vignette and bloom.

**متى:** عند طلب لوك فيلم قديم أو أرشيفي بغبار وخدوش ووميض بروجكتر وتقسيم لوني دافئ / when the user asks for an old-film or archival look with dust, scratches, projector flicker and split-tone

**كيف:** Canvas/ffmpeg: grain .08; ~20 dust specks per frame at seeded random positions (1–3 px, life 1–2 frames); 0–2 vertical scratches 1 px at 30% white drifting; bloom threshold .8; projector flicker = 1 ± .03 noise.

**المعاملات:** grain .08, dust 20/frame, bloom threshold .8

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عتيق · أرشيف · vintage · dust · scratches · projector flicker · فيلم قديم · ريترو · خدوش · old film · split tone

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-nft-chen-5f8bb0`
- `fastify-motion-bro/scripts/profiles/vox-history.mjs:11`

#### 7. قدرات قريبة في العائلة

- `TEX-06` حبيبات ثلاثية الأبعاد (FilmPass) / 3D film grain pass (ready)
- `TEX-07` حبيبات 2% وانحراف لوني على الحواف / 2% grain + edge-only chromatic aberration (documented)
- `TEX-09` أسود دافئ بحبيبات وتعتيم / Warm-black grain + vignette grade (seen)
- `TEX-10` درجة الورق التحريري / Editorial paper grade (seen)

### `TEX-09` — أسود دافئ بحبيبات وتعتيم / Warm-black grain + vignette grade

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خلفية سوداء دافئة ‎#0a0907‎ بحبيبات متجددة كل إطار 3–10% وتعتيم قوي يجعل اللون المسطح يُقرأ كطباعة فاخرة. / Warm black #0a0907 with per-frame grain 3–10% and a strong radial vignette so flat colour reads premium.

**متى:** حين تبدو الألوان المسطحة رخيصة وتريد خلفية سوداء دافئة بحبيبات وتعتيم تعطي إحساسًا فاخرًا / when flat colour looks cheap and you want a warm-black grainy, vignetted ground that reads premium

**كيف:** Regenerate noise every frame; vignette to black at corners; on light/red scenes push edges −35% luminance.

**المعاملات:** grain 3–5% (gritty 8–10%), vignette 30–60% at corners

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أسود · حبيبات · تعتيم · warm black · grain · vignette · premium · فخامة · خلفية سوداء · لوك فاخر · dark background · luxury

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-robj3d3-b18fad`
- `kosif-tool/styles/pm-spearwtf-3c1fd1`
- `kosif-tool/styles/pm-grace-sunnyy-29bc61`
- `kosif-tool/styles/pm-sahildesigner23-ee3155`

#### 7. قدرات قريبة في العائلة

- `TEX-07` حبيبات 2% وانحراف لوني على الحواف / 2% grain + edge-only chromatic aberration (documented)
- `TEX-08` تلوين عتيق بغبار وخدوش / Vintage film grade: dust, scratches, split-tone (seen)
- `TEX-10` درجة الورق التحريري / Editorial paper grade (seen)
- `TEX-11` حبيبات مع زوايا HUD / Film grain + HUD corners (seen)

### `TEX-10` — درجة الورق التحريري / Editorial paper grade

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قاعدة كريمية ‎#efecdd‎ + ضوضاء 3% + تعتيم 10%، حبر شبه أسود ولون أحمر واحد للتوكيد. / Cream #efecdd base, 3% noise, 10% vignette, near-black ink and a single red accent.

**متى:** عند تصميم فيديو تحريري أو بيانات على خلفية ورقية كريمية بحبر داكن ولون أحمر واحد للتوكيد / for editorial or data videos on a cream paper ground with near-black ink and one red accent

**كيف:** Static paper noise (not boiling), vignette 10%; keep data labels clean of texture.

**المعاملات:** noise 3%, vignette 10%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ورق · تحريري · editorial · paper · cream · خلفية كريمية · صحفي · لون تأكيد · newspaper look · red accent

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-hbcoop-de365c`

#### 7. قدرات قريبة في العائلة

- `TEX-08` تلوين عتيق بغبار وخدوش / Vintage film grade: dust, scratches, split-tone (seen)
- `TEX-09` أسود دافئ بحبيبات وتعتيم / Warm-black grain + vignette grade (seen)
- `TEX-11` حبيبات مع زوايا HUD / Film grain + HUD corners (seen)
- `TEX-12` عنوان محبب متوهج / Grain-glow title card (seen)

### `TEX-11` — حبيبات مع زوايا HUD / Film grain + HUD corners

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حبيبات 6–10% متجددة كل إطار مع أقواس زوايا وملصقات mono صغيرة ومؤشر تقدم. / Per-frame grain 6–10% plus corner brackets, micro mono labels and a progress meter.

**متى:** حين تريد واجهة كاميرا بأقواس زوايا وملصقات صغيرة ومؤشر تقدم فوق حبيبات فيلم / when you want a camera HUD with corner brackets, tiny labels and a progress meter over film grain

**كيف:** Grain layer under a fixed HUD layer (HUD stays crisp, outside the camera transform).

**المعاملات:** grain 6–10%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** HUD · حبيبات · grain · camera ui · واجهة كاميرا · أقواس الزوايا · شريط تقدم · viewfinder · corner brackets

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-madhav-xo-f97f20`

#### 7. قدرات قريبة في العائلة

- `TEX-09` أسود دافئ بحبيبات وتعتيم / Warm-black grain + vignette grade (seen)
- `TEX-10` درجة الورق التحريري / Editorial paper grade (seen)
- `TEX-12` عنوان محبب متوهج / Grain-glow title card (seen)
- `TEX-13` خلفية ورق ثابتة 5–10% / Static paper/board texture (documented)

### `TEX-12` — عنوان محبب متوهج / Grain-glow title card

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عنوان ثقيل مملوء بخامة ضوضاء مع توهج خارجي 20px، يظهر من نقطة نجم واحدة. / Heavy title filled with noise texture, 20 px outer glow, fading in from a single star point.

**متى:** عند عمل عنوان افتتاحي ثقيل مملوء بخامة ضوضاء وتوهج يظهر من نقطة نجم / for a heavy opening title filled with noise texture and glow, appearing from a single star point

**كيف:** Noise texture via mask (TEX-62) at opacity .5; glow = blurred copy; scale-in from a star at the title centre.

**المعاملات:** noise .5; glow 20 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عنوان · توهج · title · grain · glow · عنوان افتتاحي · تايتل · نص متوهج · title card · noise texture

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-nolkeeg-bf062e`

#### 7. قدرات قريبة في العائلة

- `TEX-10` درجة الورق التحريري / Editorial paper grade (seen)
- `TEX-11` حبيبات مع زوايا HUD / Film grain + HUD corners (seen)
- `TEX-13` خلفية ورق ثابتة 5–10% / Static paper/board texture (documented)
- `TEX-14` ورق ألوان مائية / Watercolour paper ground (seen)

### `TEX-13` — خلفية ورق ثابتة 5–10% / Static paper/board texture

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طبقة ورق أو كرتون بشفافية 5–10% تبقى ثابتة؛ الغليان (boil) فقط حين يطلبه الأسلوب. / Paper or board overlay at 5–10% that stays still unless the style asks for boil.

**متى:** حين يحتاج المشهد ملمس ورق أو كرتون خفيفًا ثابتًا فوق الرسوم دون أن يغلي / when a scene needs a light, still paper or board texture overlay that does not boil

**كيف:** Procedural: feTurbulence baseFrequency .6–.9 + feColorMatrix to paper tone, multiply over the scene; or a licensed paper PNG. Same seed every frame (static).

**المعاملات:** opacity 5–10%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ورق · paper · texture · static · hand-drawn · خامة ورق · كرتون · ملمس · paper overlay · board texture

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/playbooks/hand-drawn.md:18`
- `fastify-motion-bro/scripts/profiles/stickman.mjs:4`

#### 7. قدرات قريبة في العائلة

- `TEX-11` حبيبات مع زوايا HUD / Film grain + HUD corners (seen)
- `TEX-12` عنوان محبب متوهج / Grain-glow title card (seen)
- `TEX-14` ورق ألوان مائية / Watercolour paper ground (seen)
- `TEX-15` رق قديم بحواف ونقاط رمل / Parchment vignette + sand stipple (seen)

### `TEX-14` — ورق ألوان مائية / Watercolour paper ground

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ورق كريمي ‎#f3e8cf‎ بملمس بارز مضروب فوق كل مشهد، وتلال بغسلة مائية وحافة حبر مرتجفة. / Cream #f3e8cf embossed paper multiplied over every scene; hills as a wobbly ink arc with a watercolour wash.

**متى:** عند رسم مشاهد قصصية بأسلوب الألوان المائية على ورق كريمي بارز وتلال بغسلة لونية / for storybook scenes in a watercolour style on embossed cream paper with washed hills

**كيف:** Paper = noise height → normal-ish emboss (TEX-56 normalFromHeight or two offset noise layers) multiply; wash = fill #c6c7a4 with darker blotches from low-frequency noise, edge darkening 1–2 px.

**المعاملات:** paper #f3e8cf; wash #c6c7a4

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ألوان مائية · watercolour · paper · wash · storybook · مائي · قصة مصورة · ورق بارز · embossed paper · illustration

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-abderrahmen-g-9e8ed0`

#### 7. قدرات قريبة في العائلة

- `TEX-12` عنوان محبب متوهج / Grain-glow title card (seen)
- `TEX-13` خلفية ورق ثابتة 5–10% / Static paper/board texture (documented)
- `TEX-15` رق قديم بحواف ونقاط رمل / Parchment vignette + sand stipple (seen)
- `TEX-16` كولاج ورقي (S04) / Paper collage style (S04) (documented)

### `TEX-15` — رق قديم بحواف ونقاط رمل / Parchment vignette + sand stipple

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تدرج شعاعي من ‎#ead9b5‎ إلى ‎#c9aa72‎ مع نقاط رمل داخل الصحارى فقط وخطوط طي خافتة. / Radial #ead9b5→#c9aa72 parchment, sand dots only inside deserts (point-in-polygon rejects seas) and faint fold lines.

**متى:** حين تحتاج خريطة قديمة على رق بحواف داكنة ونقاط رمل في الصحارى وخطوط طي / when you need an old map on parchment with darker edges, sand dots in deserts and fold lines

**كيف:** Seeded random dots r .6–1 px at 30% inside land polygons; fold lines 1 px at 8%; vignette darker edges.

**المعاملات:** dot r .6–1 px, opacity .3

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** رق · خريطة · parchment · map · stipple · sand · خريطة قديمة · صحراء · ورق قديم · old map · fold lines

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

#### 7. قدرات قريبة في العائلة

- `TEX-13` خلفية ورق ثابتة 5–10% / Static paper/board texture (documented)
- `TEX-14` ورق ألوان مائية / Watercolour paper ground (seen)
- `TEX-16` كولاج ورقي (S04) / Paper collage style (S04) (documented)
- `TEX-17` لوحة قصاصات وشريط يثبّتها / Cut-out board + tape pin (MG-101/102) (documented)

### `TEX-16` — كولاج ورقي (S04) / Paper collage style (S04)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قصاصات وشريط لاصق وحواف ملموسة؛ الطبقات تقفز بخفة وتتمزق وتنقلب كالصفحات. / Cut-outs, tape, tactile edges; layers hop lightly, tear and page-flip.

**متى:** عند طلب أسلوب كولاج ورقي بقصاصات وشريط لاصق وطبقات تقفز وتتمزق وتنقلب كالصفحات / when the user wants a paper-collage style with cut-outs and tape, layers hopping, tearing and page-flipping

**كيف:** PNG cut-outs + paper texture (procedural feTurbulence or licensed), small rotations ±2–6°, soft drop shadows; render with render_html.cjs. Too many textures crowd the frame — 2–3 materials max.

**المعاملات:** cost medium; ideas MG-004 MG-076 MG-101 MG-102 MG-103 MG-110

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كولاج · collage · paper · cut-out · tape · قص ولصق · قصاصات ورق · تقليب صفحات · scrapbook · page flip

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### 7. قدرات قريبة في العائلة

- `TEX-14` ورق ألوان مائية / Watercolour paper ground (seen)
- `TEX-15` رق قديم بحواف ونقاط رمل / Parchment vignette + sand stipple (seen)
- `TEX-17` لوحة قصاصات وشريط يثبّتها / Cut-out board + tape pin (MG-101/102) (documented)
- `TEX-18` تمزيق ورق يكشف ما تحته / Paper tear reveal (proven)

### `TEX-17` — لوحة قصاصات وشريط يثبّتها / Cut-out board + tape pin (MG-101/102)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صور مقصوصة تدخل بزوايا صغيرة وتبني لوحة حول عنوان، ثم شريط لاصق يمر على زاوية صورة ليثبتها. / Cut photos enter at small angles and build a board around a title; a tape strip then pins one corner.

**متى:** حين تريد صورًا مقصوصة تتجمع كلوحة حول عنوان ثم شريط لاصق يثبت زاوية صورة / when cut photos should gather into a board around a title and a tape strip pins one corner

**كيف:** MG-101: 0–1 s background, 1–4 s cut-outs, 4–7 s read; few rotation/scale keys per layer. MG-102: 0–1 s photo, 1–2 s tape revealed by a mask, 2–4 s hold; tape shadow very light (it sits on the paper).

**المعاملات:** 7 s / 4 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قصاصات · شريط لاصق · board · tape · collage · لوحة صور · صور مقصوصة · تثبيت بشريط · photo board · cut photos

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-collage-textures.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### 7. قدرات قريبة في العائلة

- `TEX-15` رق قديم بحواف ونقاط رمل / Parchment vignette + sand stipple (seen)
- `TEX-16` كولاج ورقي (S04) / Paper collage style (S04) (documented)
- `TEX-18` تمزيق ورق يكشف ما تحته / Paper tear reveal (proven)
- `TEX-19` رسمة ممسوحة كملصق / Scanned drawing as sticker cut-out (seen)

### `TEX-18` — تمزيق ورق يكشف ما تحته / Paper tear reveal

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | مكوّنات HyperFrames برخصة Apache-2.0 / HyperFrames components are Apache-2.0. |

**ما هي:** شقّ غير منتظم ينفتح من الوسط بحافتين ورقيتين بلب أبيض وظل، فيكشف المشهد التالي. / A ragged slit opens from the middle with two paper edges, white core and shadow, revealing the next scene.

**متى:** عند الانتقال لمشهد تالٍ بتمزيق ورقة من المنتصف بحواف خشنة وظل / when revealing the next scene by ripping the paper open from the middle with ragged edges and shadow

**كيف:** Jittered polygon edge (one sample per 12 px, ±13 px seeded) shared by both halves; translate halves apart ±170 px with a tiny rotation, shadowBlur 14, 4 px white stroke on the torn edge; never a smooth edge. Rendered here (lab, Canvas). HyperFrames ships torn-paper-rip (direction, tone cream\|kraft\|white, roughness 20–90) and paper-collage-reveal (4–8 scraps).

**المعاملات:** slit 0–0.7 s, tear 0.7–2.5 s, read 2.5–4 s; edge jitter ±13 px; shadow 14 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تمزيق · ورق · paper tear · rip · reveal · transition · ترانزيشن · انتقال ورقي · ورق ممزق · torn paper · scene reveal

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-collage-textures.md`
- `kosif-one/vendor/hyperframes/registry/components/torn-paper-rip/torn-paper-rip.html`
- `kosif-one/vendor/hyperframes/registry/components/paper-collage-reveal/paper-collage-reveal.html`

#### 7. قدرات قريبة في العائلة

- `TEX-16` كولاج ورقي (S04) / Paper collage style (S04) (documented)
- `TEX-17` لوحة قصاصات وشريط يثبّتها / Cut-out board + tape pin (MG-101/102) (documented)
- `TEX-19` رسمة ممسوحة كملصق / Scanned drawing as sticker cut-out (seen)
- `TEX-20` قصاصة جريدة ونقش / Newspaper / engraving cut-out (seen)

### `TEX-19` — رسمة ممسوحة كملصق / Scanned drawing as sticker cut-out

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رسمة يدوية تُقص إلى ألفا مع حد أبيض 6–10px وظل 4px ناعم فتبدو ملصقًا ورقيًا. / Mask a hand-drawn scan to alpha, dilate a 6–10 px white outline and add a soft 4 px drop shadow — a paper sticker.

**متى:** حين تريد تحويل رسمة يدوية ممسوحة إلى ملصق بحد أبيض وظل ناعم / when turning a scanned hand drawing into a paper sticker with a white outline and soft shadow

**كيف:** Pillow: alpha → MaxFilter(13) for the outline → white at 90% under the art → shadow = blurred alpha offset 2 px at 20%. Background knockout by corner colour (TEX-28) first if the scan has a flat ground.

**المعاملات:** outline #ffffff 90%, 6–10 px; shadow rgba(0,0,0,.2) offset 2 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ملصق · sticker · cut-out · outline · scan · استيكر · حد أبيض · رسمة يدوية · white border · drop shadow

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-abderrahmen-g-9e8ed0`
- `kosif-tool/styles/pm-koldo2k-5cff87`

#### 7. قدرات قريبة في العائلة

- `TEX-17` لوحة قصاصات وشريط يثبّتها / Cut-out board + tape pin (MG-101/102) (documented)
- `TEX-18` تمزيق ورق يكشف ما تحته / Paper tear reveal (proven)
- `TEX-20` قصاصة جريدة ونقش / Newspaper / engraving cut-out (seen)
- `TEX-21` قفل أسلوب الأرشيف / Archival scrapbook style lock (ready)

### `TEX-20` — قصاصة جريدة ونقش / Newspaper / engraving cut-out

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صورة أبيض وأسود بهالفتون أو نقش، بحد أبيض 6px وظل 30% — جمالية الأرشيف والوثائقي. / B&W halftone or engraved object with a 6 px white border and 30% shadow — archival/documentary look.

**متى:** عند طلب جمالية أرشيفية أو وثائقية: صورة أبيض وأسود بهالفتون أو نقش مع حد أبيض وظل / for an archival or documentary look: a B&W halftone or engraved cut-out with white border and shadow

**كيف:** Desaturate 100%, apply halftone (TEX-34) or engraving (TEX-39 shader effect), then the sticker recipe; on white grounds keep the etching unbordered.

**المعاملات:** stroke white 6 px, shadow blur 12 px at 30%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** جريدة · نقش · newspaper · engraving · archival · وثائقي · أبيض وأسود · قصاصة · documentary · halftone

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-koldo2k-5cff87`
- `kosif-tool/styles/pm-lexnlin-038035`

#### 7. قدرات قريبة في العائلة

- `TEX-18` تمزيق ورق يكشف ما تحته / Paper tear reveal (proven)
- `TEX-19` رسمة ممسوحة كملصق / Scanned drawing as sticker cut-out (seen)
- `TEX-21` قفل أسلوب الأرشيف / Archival scrapbook style lock (ready)
- `TEX-22` قفل الخلفية الورقية / Paper sketch background lock (ready)

### `TEX-21` — قفل أسلوب الأرشيف / Archival scrapbook style lock

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** وصف ثابت يُلصق في كل لقطة vox-history: جرائد بنية، حبيبات، خطوط مسح، هالفتون، صور ممزقة بحواف بيضاء، دبابيس وخيط أحمر، وميض بروجكتر. / A STYLE constant pasted into every vox-history clip prompt: sepia newsprint, grain, scan lines, halftone, torn photos, tacks, red thread, projector flicker.

**متى:** حين تولّد عدة لقطات بالذكاء الاصطناعي بأسلوب أرشيف تاريخي وتريدها متسقة بوصف أسلوب واحد / when generating several AI clips in an archival history style and keeping them consistent with one style block

**كيف:** Repeat the exact same style block in every generation request; keep stamps generic (no real logos); add stop-motion entrances in the edit.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أرشيف · vox · style lock · scrapbook · ai prompt · ثبات الأسلوب · برومبت · فيديو تاريخي · consistent style · history video

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `fastify-motion-bro/scripts/profiles/vox-history.mjs:11`
- `fastify-motion-bro/skills/vox-history/SKILL.md:12`

#### 7. قدرات قريبة في العائلة

- `TEX-19` رسمة ممسوحة كملصق / Scanned drawing as sticker cut-out (seen)
- `TEX-20` قصاصة جريدة ونقش / Newspaper / engraving cut-out (seen)
- `TEX-22` قفل الخلفية الورقية / Paper sketch background lock (ready)
- `TEX-23` الورق المقصوص بعمق ثلاث طبقات / Paper cut-out style (3-depth parallax) (documented)

### `TEX-22` — قفل الخلفية الورقية / Paper sketch background lock

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خلفية ورق/سبورة مرسومة يدويًا بلا عمق واقعي، مكررة في كل لقطات stickman حتى تطابق الشخصية ثنائية الأبعاد. / A flat hand-drawn paper/whiteboard background block repeated in all stickman prompts to match the 2D figure.

**متى:** عند توليد لقطات stickman بالذكاء الاصطناعي وتريد خلفية ورقية مرسومة يدويًا ثابتة فيها كلها / when generating stickman AI clips that must share the same flat hand-drawn paper background

**كيف:** BACKGROUNDS.paper string reused verbatim in all 5 prompts; no photoreal depth words.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ورق · stickman · style lock · paper · whiteboard · ستيك مان · خلفية مرسومة · ثبات الخلفية · consistent background · prompt

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `fastify-motion-bro/scripts/profiles/stickman.mjs:4`

#### 7. قدرات قريبة في العائلة

- `TEX-20` قصاصة جريدة ونقش / Newspaper / engraving cut-out (seen)
- `TEX-21` قفل أسلوب الأرشيف / Archival scrapbook style lock (ready)
- `TEX-23` الورق المقصوص بعمق ثلاث طبقات / Paper cut-out style (3-depth parallax) (documented)
- `TEX-24` ستوب موشن بارتعاش البذرة / Stop-motion seeded hold jitter (documented)

### `TEX-23` — الورق المقصوص بعمق ثلاث طبقات / Paper cut-out style (3-depth parallax)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ورق كريمي ‎#F6EBD9‎ بألوان ورقية خافتة وظل ورقي صلب، بارالاكس بثلاثة أعماق وتمايل خفيف. / Cream #F6EBD9 paper, muted paper colours, a hard paper drop shadow, 3-depth parallax and gentle sway.

**متى:** حين يطلب المستخدم أسلوب ورق مقصوص دافئ بطبقات بعمق وتمايل خفيف وظل ورقي / when the user asks for a warm paper cut-out style with layered depth parallax, gentle sway and paper shadows

**كيف:** Layers at depth 1 / 0.6 / 0.3; filter drop-shadow(0 8px 0 rgba(0,0,0,.18)); sway ±2° sine; type Amiri 700 / Lateef + Tajawal 500. Scaffold the base style with python3 tools/kosif.py scaffold cutout-paper <dir> (paper texture 5–10%, hinge-pivot rigs, on twos).

**المعاملات:** #F6EBD9 #D96B4A #5B8C5A #3B6EA8; shadow 0 8px 0 .18; parallax 1/0.6/0.3; sway ±2°

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ورق مقصوص · paper cut · parallax · cutout · تراث · قصاصات ورق · طبقات عمق · تمايل · layered depth · papercraft

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `100-superskills/skills/trend-animation-styles/references/styles.md`
- `kosif-tool/styles/cutout-paper/SKILL.md`
- `kosif-tool/styles/cutout-paper/STYLE.json`

#### 7. قدرات قريبة في العائلة

- `TEX-21` قفل أسلوب الأرشيف / Archival scrapbook style lock (ready)
- `TEX-22` قفل الخلفية الورقية / Paper sketch background lock (ready)
- `TEX-24` ستوب موشن بارتعاش البذرة / Stop-motion seeded hold jitter (documented)
- `TEX-25` صلصال مطفي وبصمات / Claymation matte + fingerprint texture (documented)

### `TEX-24` — ستوب موشن بارتعاش البذرة / Stop-motion seeded hold jitter

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تحريك على الاثنين (12 إطارًا/ث) مع ارتعاش ±1.5px و±0.6° لكل إطار ممسوك من بذرة، فيتنفس المشهد كالصلصال. / Animate on twos with a seeded ±1.5 px / ±0.6° jitter per held frame so the set breathes like stop-motion.

**متى:** عند محاكاة الستوب موشن أو الصلصال: تحريك على الاثنين مع ارتعاش خفيف لكل إطار ممسوك / to fake stop-motion or clay animation: animating on twos with a slight seeded jitter per held frame

**كيف:** hold = floor(t*12); jitter = hash(hold, layerId) → dx, dy, rot; photo textures + contact shadows. Scaffold: python3 tools/kosif.py scaffold stop-motion <dir>.

**المعاملات:** on twos; ±1.5 px, ±0.6°

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ستوب موشن · stop motion · jitter · on twos · clay · رعشة · تحريك إطار بإطار · صلصال · frame by frame · 12 fps

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/stop-motion/SKILL.md`
- `kosif-tool/styles/stop-motion/STYLE.json`
- `kosif-tool/styles/pm-davidshulmanfl-371638/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `TEX-22` قفل الخلفية الورقية / Paper sketch background lock (ready)
- `TEX-23` الورق المقصوص بعمق ثلاث طبقات / Paper cut-out style (3-depth parallax) (documented)
- `TEX-25` صلصال مطفي وبصمات / Claymation matte + fingerprint texture (documented)
- `TEX-26` مشهد أطفال بالكرايون / Crayon paper-craft kids scene (seen)

### `TEX-25` — صلصال مطفي وبصمات / Claymation matte + fingerprint texture

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شخصيات صلصال بخامة مطفية (roughness 0.6–0.9) وانضغاط وتمدد، مع طبقة بصمات 12% وضوء مفتاحي علوي-يسار. / Clay characters with matte material (roughness 0.6–0.9) and squash/stretch, plus a 12% fingerprint overlay and baked top-left key light.

**متى:** حين تريد شخصيات صلصال بخامة مطفية وانضغاط وتمدد وآثار بصمات خفيفة / when you want clay characters with a matte surface, squash and stretch and a faint fingerprint overlay

**كيف:** Three.js MeshStandardMaterial roughness .6–.9 or 2D soft shading; squash scaleY .7 / scaleX 1.3 over 80 ms; fingerprint = procedural concentric ridges (sin of distance + noise) multiplied at 12%. Scaffold: python3 tools/kosif.py scaffold claymation <dir>.

**المعاملات:** roughness .6–.9; squash .7/1.3 in 80 ms; fingerprints 12% multiply

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صلصال · claymation · matte · fingerprint · squash · كلاي · بصمات · انضغاط وتمدد · clay character · squash and stretch

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/claymation/SKILL.md`
- `kosif-tool/styles/claymation/STYLE.json`
- `kosif-tool/styles/pm-davidshulmanfl-371638/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `TEX-23` الورق المقصوص بعمق ثلاث طبقات / Paper cut-out style (3-depth parallax) (documented)
- `TEX-24` ستوب موشن بارتعاش البذرة / Stop-motion seeded hold jitter (documented)
- `TEX-26` مشهد أطفال بالكرايون / Crayon paper-craft kids scene (seen)
- `TEX-27` النقص المقصود / Intentional imperfection (wabi-sabi) (documented)

### `TEX-26` — مشهد أطفال بالكرايون / Crayon paper-craft kids scene

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أشكال بملمس كرايون (شمس، غيوم، قوس قزح، تلال) بحد داكن 3px ودمية زغبية بعيون كبيرة. / Crayon-textured shapes (sun, clouds, rainbow, hills) with 3 px dark outlines and a fuzzy big-eyed puppet.

**متى:** عند عمل مشهد أطفال بخامة ألوان شمع: شمس وغيوم وقوس قزح وتلال بحد داكن ودمية / for a kids' scene with crayon texture: sun, clouds, rainbow and hills with dark outlines and a puppet

**كيف:** Fill with a clipped stroke-hatch or noise threshold texture (TEX-81 hatching), outline 3 px; speech balloon with two-colour bubbly text.

**المعاملات:** texture fill + 3 px dark outline

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كرايون · أطفال · crayon · kids · paper craft · ألوان شمع · رسوم أطفال · قوس قزح · children · rainbow

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-emollick-8661a8`

#### 7. قدرات قريبة في العائلة

- `TEX-24` ستوب موشن بارتعاش البذرة / Stop-motion seeded hold jitter (documented)
- `TEX-25` صلصال مطفي وبصمات / Claymation matte + fingerprint texture (documented)
- `TEX-27` النقص المقصود / Intentional imperfection (wabi-sabi) (documented)
- `TEX-28` إزالة الخلفية بلون الزاوية / Corner-colour background knockout (ready)

### `TEX-27` — النقص المقصود / Intentional imperfection (wabi-sabi)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** دفء من عدم التماثل الخفيف وتفاوت سماكة الخط وملمس الورق، مع إبقاء أجزاء البيانات نظيفة. / Warmth from slight asymmetry, varied stroke width and paper texture — but keep data parts clean.

**متى:** حين يبدو التصميم باردًا ومثاليًا وتريد دفئًا يدويًا بعدم تماثل خفيف مع إبقاء الأرقام نظيفة / when a design feels cold and perfect and needs handmade warmth via slight asymmetry, keeping numbers clean

**كيف:** Rotate elements ±1–2°, vary stroke width ±15%, irregular spacing; paper overlay; never on numbers/labels.

**المعاملات:** rotation ±1–2°

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نقص مقصود · wabi-sabi · imperfection · handmade · لمسة يدوية · عدم تماثل · دفء · hand-drawn feel · asymmetry

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-atlas/skills/1503-universal-design-principles/3743-wabi-sabi-imperfection`

#### 7. قدرات قريبة في العائلة

- `TEX-25` صلصال مطفي وبصمات / Claymation matte + fingerprint texture (documented)
- `TEX-26` مشهد أطفال بالكرايون / Crayon paper-craft kids scene (seen)
- `TEX-28` إزالة الخلفية بلون الزاوية / Corner-colour background knockout (ready)
- `TEX-29` تظليل كرة بالهالفتون / Halftone sphere (Lambert dots) (proven)

### `TEX-28` — إزالة الخلفية بلون الزاوية / Corner-colour background knockout

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | MIT (vendor scroll-world). |

**ما هي:** يعزل الرسمة أو المشهد بحذف كل ما يشبه متوسط لون الزوايا ضمن تسامح RGB. / Floats a scene by flood-removing the background that matches the averaged corner colour within an RGB tolerance.

**متى:** عند فصل رسمة أو مشهد عن خلفية مسطحة بلون واحد قبل تحويله لملصق / when removing a flat single-colour background from a drawing or scene before making it a sticker

**كيف:** python3 knockout.py in.png out.png with Pillow; TOL env sets the Euclidean tolerance; follow with the sticker outline (TEX-19).

**المعاملات:** TOL=34 Euclidean RGB

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إزالة خلفية · knockout · alpha · cut-out · pillow · حذف الخلفية · شيل الخلفية · تفريغ · remove background · transparent png

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-one/vendor/scroll-world/skills/scroll-world/references/knockout.py:25`

#### 7. قدرات قريبة في العائلة

- `TEX-26` مشهد أطفال بالكرايون / Crayon paper-craft kids scene (seen)
- `TEX-27` النقص المقصود / Intentional imperfection (wabi-sabi) (documented)
- `TEX-29` تظليل كرة بالهالفتون / Halftone sphere (Lambert dots) (proven)
- `TEX-30` هالفتون CMYK / CMYK / gooey halftone (documented)

### `TEX-29` — تظليل كرة بالهالفتون / Halftone sphere (Lambert dots)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة نقاط نصف قطر كل منها = إضاءة لامبرت لكرة افتراضية، والضوء يدور فتتحرك الظلال نقطة نقطة. / Dot grid whose radius = Lambert(normal·light) of a virtual sphere; the light orbits so shading moves dot by dot.

**متى:** حين تريد كرة مظللة بنقاط هالفتون يتحرك ظلها نقطة نقطة مع ضوء يدور / when you want a sphere shaded with halftone dots whose shading moves dot by dot under an orbiting light

**كيف:** For each grid cell inside the disc: n = (dx, dy, √(1−r²)); r_dot = rmax·max(0, n·L) + .4. Rendered here (Canvas lab, light orbiting at 2 rad/s). (code snippet in references/powers/texture-material.md)

**المعاملات:** grid 14 px, rmax 6 px, #f04a2a on #f6efe3

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هالفتون · halftone · lambert · sphere · dots · print · كرة منقطة · نقاط طباعة · ضوء دوار · dot shading · orbiting light

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-ayushunleashed-ece3e3`

#### 7. قدرات قريبة في العائلة

- `TEX-27` النقص المقصود / Intentional imperfection (wabi-sabi) (documented)
- `TEX-28` إزالة الخلفية بلون الزاوية / Corner-colour background knockout (ready)
- `TEX-30` هالفتون CMYK / CMYK / gooey halftone (documented)
- `TEX-31` نقاط هالفتون على القصاصة / Clipped halftone on a cut-out card (ready)

### `TEX-30` — هالفتون CMYK / CMYK / gooey halftone

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط بحجم الإضاءة؛ نسخة CMYK بأربع شبكات مائلة C15 M75 Y0 K45 بمزج طرحي، ونسخة لزجة بـ smooth-min. / Luma-sized dots; CMYK uses four rotated grids C15 M75 Y0 K45 subtractively; a gooey variant uses smooth-min.

**متى:** عند طلب لوك طباعة CMYK أو بوب آرت بنقاط هالفتون مائلة متعددة الأحبار أو نقاط لزجة / for a CMYK print or pop-art look with rotated multi-ink halftone dots, or a gooey dot variant

**كيف:** GLSL or numpy offline: per channel rotate uv, cell centre, sample 3×3 neighbours to avoid clipping, fwidth antialias; multiply channels.

**المعاملات:** angles C15 M75 Y0 K45

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** CMYK · هالفتون · halftone · pop art · print · بوب آرت · طباعة ملونة · نقاط لزجة · gooey dots · glsl

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:numpy` ← python3 -c "import numpy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `TEX-28` إزالة الخلفية بلون الزاوية / Corner-colour background knockout (ready)
- `TEX-29` تظليل كرة بالهالفتون / Halftone sphere (Lambert dots) (proven)
- `TEX-31` نقاط هالفتون على القصاصة / Clipped halftone on a cut-out card (ready)
- `TEX-32` موجة هالفتون ومواريه / Halftone ripple & moiré overprint (seen)

### `TEX-31` — نقاط هالفتون على القصاصة / Clipped halftone on a cut-out card

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط كل 10px بنمط قطري بلون النص 8% مقصوصة داخل بطاقة البطل — ملمس طباعة بلا صور. / Dots every 10 px in a diagonal pattern at 8% of the text colour, clipped to the hero card — print feel, no images.

**متى:** حين تريد ملمس طباعة خفيفًا داخل بطاقة العنوان بنقاط قطرية بلا صور / when you want a light print texture inside a hero card using diagonal dots, no images

**كيف:** ctx.clip(card); dot where (floor(x/10s)+floor(y/10s)) % 4 == 0, radius 1.7·scale.

**المعاملات:** cell 10 px; r 1.7 px; 8% alpha

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هالفتون · halftone · editorial · card · clip · بطاقة · نقاط · ملمس طباعة · print texture · canvas

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `fastify-motion-bro/web/editorial.js:63-66`

#### 7. قدرات قريبة في العائلة

- `TEX-29` تظليل كرة بالهالفتون / Halftone sphere (Lambert dots) (proven)
- `TEX-30` هالفتون CMYK / CMYK / gooey halftone (documented)
- `TEX-32` موجة هالفتون ومواريه / Halftone ripple & moiré overprint (seen)
- `TEX-33` خلفية أشرطة ضوء منقطة / Halftone light-band backdrop (seen)

### `TEX-32` — موجة هالفتون ومواريه / Halftone ripple & moiré overprint

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة نقاط يقود نصف قطرها حقل موجي شعاعي، وشبكة ثانية بزاوية مختلفة تصنع مواريه الطباعة. / Dot grid driven by a radial wave field; a second screen at another angle creates overprint moiré.

**متى:** عند الحاجة لخلفية نقاط هالفتون تنبض بموجات دائرية مع مواريه طباعة من شبكتين / when you need a halftone dot background pulsing with radial waves and overprint moiré from two screens

**كيف:** r = rmax·(.5 + .5·sin(k·d − ω·t)); second grid rotated 30° in another ink with multiply; ring speed 1 ring / 0.5 s. Variants: dot ring (radius by a distance field), corner blobs drifting.

**المعاملات:** 16 px screen, angles 15° & 45°, 1 ring / 0.5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هالفتون · مواريه · halftone · moire · ripple · wave · موجات · نبض · طباعة متراكبة · overprint · dot pattern

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-fionntobin-97b7af`
- `kosif-tool/styles/pm-ultimaxbt-bbebf5`
- `kosif-tool/styles/pm-rendesr-86be44`
- `kosif-tool/styles/pm-polydao-7a572b`

#### 7. قدرات قريبة في العائلة

- `TEX-30` هالفتون CMYK / CMYK / gooey halftone (documented)
- `TEX-31` نقاط هالفتون على القصاصة / Clipped halftone on a cut-out card (ready)
- `TEX-33` خلفية أشرطة ضوء منقطة / Halftone light-band backdrop (seen)
- `TEX-34` صورة هالفتون ماكرو / Halftone macro image (seen)

### `TEX-33` — خلفية أشرطة ضوء منقطة / Halftone light-band backdrop

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أشرطة تدرج قطرية في الزوايا مملوءة بنقاط هالفتون ونمط دوائر، تتلاشى نحو المركز وتنجرف ببطء. / Diagonal gradient bands at the corners filled with halftone dots and a circuit pattern, radially faded to the centre, drifting.

**متى:** حين تحتاج خلفية بأشرطة ضوء قطرية في الزوايا مملوءة بنقاط تتلاشى نحو المركز وتنجرف ببطء / when you need a backdrop of diagonal light bands at the corners filled with dots fading to the centre

**كيف:** Mask = radial fade; band angle −35°; dot pitch 6–8 px; opacity .3–.5; drift 5–10 px/s. Sunburst variant: rotating conic rays + dot overlay.

**المعاملات:** angle −35°, pitch 6–8 px, opacity .3–.5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هالفتون · أشعة · halftone · sunburst · background · خلفية متحركة · أشرطة ضوء · نقاط · light bands · backdrop

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-elliot-garreffa-f334bc`
- `kosif-tool/styles/pm-topi-003-b0e12c`

#### 7. قدرات قريبة في العائلة

- `TEX-31` نقاط هالفتون على القصاصة / Clipped halftone on a cut-out card (ready)
- `TEX-32` موجة هالفتون ومواريه / Halftone ripple & moiré overprint (seen)
- `TEX-34` صورة هالفتون ماكرو / Halftone macro image (seen)
- `TEX-35` سماء متدرجة بتنقيط Bayer / Bayer-dithered sky + stepped stars (proven)

### `TEX-34` — صورة هالفتون ماكرو / Halftone macro image

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شيدر شبكة نقاط فوق صورة رمادية — الصورة الفوتوغرافية تصير ملصقًا مطبوعًا. / Dot-screen shader over a greyscale photo — the photo becomes a printed poster.

**متى:** عند تحويل صورة فوتوغرافية إلى بوستر مطبوع بشبكة نقاط هالفتون / when turning a photo into a printed-poster look with a halftone dot screen

**كيف:** Greyscale → cell-centre luma → dot radius; or HyperFrames media effect halftone (TEX-39).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هالفتون · صورة · halftone · photo · poster · بوستر · تأثير طباعة · نقاط · dot screen · print effect

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-reflex-cloud-72ffe5`

#### 7. قدرات قريبة في العائلة

- `TEX-32` موجة هالفتون ومواريه / Halftone ripple & moiré overprint (seen)
- `TEX-33` خلفية أشرطة ضوء منقطة / Halftone light-band backdrop (seen)
- `TEX-35` سماء متدرجة بتنقيط Bayer / Bayer-dithered sky + stepped stars (proven)
- `TEX-36` تعبئة تنقيط أحادية البت / 1-bit dither fill with threshold sweep (seen)

### `TEX-35` — سماء متدرجة بتنقيط Bayer / Bayer-dithered sky + stepped stars

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تدرج سماء بثلاث إلى أربع درجات نيلية/بنفسجية مع تنقيط Bayer ‏4×4، ونجوم 1–2px تومض بخطوات. / Sky gradient quantised to 3–4 indigo/purple bands with a 4×4 Bayer matrix; 1–2 px stars twinkling in steps.

**متى:** حين تريد سماء بكسل آرت ريترو بتدرج من درجات قليلة وتنقيط ونجوم تومض / when you want a retro pixel-art sky with a banded dithered gradient and twinkling stars

**كيف:** v = y/H·(n−1); i = floor(v); pick band i+1 when frac(v) > (B[y&3][x&3]+.5)/16. Stars toggle at 4 fps from a seeded list. Rendered here (Canvas lab).

**المعاملات:** 4×4 Bayer [0 8 2 10 / 12 4 14 6 / 3 11 1 9 / 15 7 13 5]; twinkle 4 fps

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تنقيط · Bayer · dither · pixel · sky · retro · بكسل آرت · سماء ليلية · نجوم · pixel art · night sky

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-0xevinho-3777d8`

#### 7. قدرات قريبة في العائلة

- `TEX-33` خلفية أشرطة ضوء منقطة / Halftone light-band backdrop (seen)
- `TEX-34` صورة هالفتون ماكرو / Halftone macro image (seen)
- `TEX-36` تعبئة تنقيط أحادية البت / 1-bit dither fill with threshold sweep (seen)
- `TEX-37` تعبئة حبيبات ريزو / Riso grain fill (seen)

### `TEX-36` — تعبئة تنقيط أحادية البت / 1-bit dither fill with threshold sweep

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تنقيط Bayer أو رقعة شطرنج برتقالي على أسود يملأ منطقة، ويُحرّك العتبة لعمل مسح. / Bayer/checker dither of orange on black filling a region; animate the threshold to sweep.

**متى:** عند ملء منطقة بتنقيط ريترو أحادي البت وتحريك العتبة لعمل مسح كاشف / when filling a region with retro 1-bit dithering and animating the threshold as a sweep reveal

**كيف:** threshold(t) from 0→1 over 600 ms; cell 8 px (scale the Bayer matrix ×2); pixelated rendering (imageSmoothingEnabled=false).

**المعاملات:** cell 8 px, sweep 600 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تنقيط · 1-bit · dither · retro · sweep · بكسل · كشف تدريجي · رقعة شطرنج · bayer · threshold reveal

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-anthonyriera-9b1b2a`

#### 7. قدرات قريبة في العائلة

- `TEX-34` صورة هالفتون ماكرو / Halftone macro image (seen)
- `TEX-35` سماء متدرجة بتنقيط Bayer / Bayer-dithered sky + stepped stars (proven)
- `TEX-37` تعبئة حبيبات ريزو / Riso grain fill (seen)
- `TEX-38` طبقة حبيبات نقطية / Dot-lattice grain overlay (proven)

### `TEX-37` — تعبئة حبيبات ريزو / Riso grain fill

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قناع عتبة من feTurbulence على أشكال مسطحة بحبرين أو ثلاثة، فيبدو كطباعة ريزوغراف. / feTurbulence threshold mask on flat shapes in 2–3 inks — risograph look.

**متى:** حين تريد أشكالًا مسطحة بحبرين أو ثلاثة بملمس طباعة ريزوغراف وانزياح طفيف / when flat shapes should look risograph-printed in 2–3 inks with slight misregistration

**كيف:** feTurbulence baseFrequency .9 → feComponentTransfer discrete/threshold → feComposite in with the shape; slight misregistration 1–2 px per ink.

**المعاملات:** freq .9, 2–3 inks

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ريزو · riso · grain · print · ink · ريزوغراف · طباعة حبر · ملمس محبب · risograph · misregistration

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-rneayan-474bcf`

#### 7. قدرات قريبة في العائلة

- `TEX-35` سماء متدرجة بتنقيط Bayer / Bayer-dithered sky + stepped stars (proven)
- `TEX-36` تعبئة تنقيط أحادية البت / 1-bit dither fill with threshold sweep (seen)
- `TEX-38` طبقة حبيبات نقطية / Dot-lattice grain overlay (proven)
- `TEX-39` مؤثرات الشيدر على الصورة والفيديو (18) / HyperFrames shader media effects (18 keys) (install)

### `TEX-38` — طبقة حبيبات نقطية / Dot-lattice grain overlay

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة نقاط دقيقة 0.6px كل 6px فوق خلفية داكنة تعطي إحساس الطباعة بلا صور. / A 0.6 px dot lattice every 6 px over a dark hero gives a printed feel with no images.

**متى:** عند إضافة ملمس طباعة خفيف بشبكة نقاط دقيقة فوق خلفية داكنة بـ CSS دون صور / when adding a subtle printed feel with a fine CSS dot lattice over a dark hero, no images

**كيف:** ::after{inset:0; background-image:radial-gradient(#ffffff16 .6px,transparent .6px); background-size:6px 6px; opacity:.25; pointer-events:none}. Rendered here: at #fff16 it is almost invisible after H.264 — go to #fff30–40 for video.

**المعاملات:** dot .6 px; grid 6 px; opacity .25 (web) — stronger for video

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نقاط · dot grain · lattice · css · print · شبكة نقاط · ملمس · خلفية داكنة · dot pattern · overlay

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-audit-studio/studio.css:58`

#### 7. قدرات قريبة في العائلة

- `TEX-36` تعبئة تنقيط أحادية البت / 1-bit dither fill with threshold sweep (seen)
- `TEX-37` تعبئة حبيبات ريزو / Riso grain fill (seen)
- `TEX-39` مؤثرات الشيدر على الصورة والفيديو (18) / HyperFrames shader media effects (18 keys) (install)
- `TEX-40` بطاقة زجاجية فاخرة بعمق / Luxury depth glass cards (proven)

### `TEX-39` — مؤثرات الشيدر على الصورة والفيديو (18) / HyperFrames shader media effects (18 keys)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0. |

**ما هي:** مؤثرات لحظية على اللقطات: blur, pixelate, chromaBleed, tapeDamage, filmArtifacts, halftone, twoInkPrint, ascii, dither, bloom, monoScreen, scanlines, chromaticAberration, crtCurvature, digitalGlitch, engraving, crosshatch, kuwahara + grain وvignette. / Realtime footage effects: 18 keys from blur to kuwahara painterly, plus grain + vignette details.

**متى:** حين تريد تطبيق مؤثر لحظي على لقطة فيديو أو صورة مثل VHS أو CRT أو جليتش أو بكسلة أو ASCII / when applying a realtime effect to footage: VHS tape damage, CRT, glitch, pixelate, ASCII and more

**كيف:** Set effects.<key> 0..1 in data-color-grading on the media element (media-treatment); never fake them with CSS overlays. Not rendered here.

**التثبيت:** npm i -D hyperframes

**الوسوم:** شيدر · مؤثرات · halftone · dither · ascii · vhs · crt · kuwahara · engraving · hyperframes · جليتش · بكسلة · فلتر فيديو · glitch · pixelate · scanlines

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-one/vendor/hyperframes/packages/core/src/colorGrading.ts`
- `kosif-one/vendor/hyperframes/skills/media-use/references/media-treatments.md`

#### 7. قدرات قريبة في العائلة

- `TEX-37` تعبئة حبيبات ريزو / Riso grain fill (seen)
- `TEX-38` طبقة حبيبات نقطية / Dot-lattice grain overlay (proven)
- `TEX-40` بطاقة زجاجية فاخرة بعمق / Luxury depth glass cards (proven)
- `TEX-41` وصفة الزجاج الداكن / Dark-only frosted glass panel recipe (documented)

### `TEX-40` — بطاقة زجاجية فاخرة بعمق / Luxury depth glass cards

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بطاقات زجاج تنزلق بعمق وبارالاكس فوق شبكة تدرج حية، بحافة علوية مضيئة وظلين ناعمين. / Glass cards sliding in depth and parallax over a live mesh gradient, with a lit top edge and two soft shadows.

**متى:** عند عرض بطاقات زجاجية فاخرة تنزلق بعمق وبارالاكس فوق خلفية تدرج حية / for luxury frosted-glass cards sliding in depth and parallax over a live mesh gradient

**كيف:** background linear rgba(255,255,255,.16)→.035; backdrop-filter blur(22px) saturate(150%); radius 30 px; inset top highlight 1 px .45 + inner edge 1 px .13; shadows 0 40px 80px −30px (.7) and 0 12px 24px −8px (.35); put a faint star pattern/bokeh under the cards so the frost is visible. Rendered here in proofs/glass-luxury-logo (13/13) and in the texture lab.

**المعاملات:** blur 22 px, saturate 150%, depths 1.0/0.7/0.45, defocus 1.6 + 3.2·(1−depth) px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** زجاج · فاخر · glass · glassmorphism · backdrop-filter · luxury · parallax · زجاج مصنفر · بطاقات · تمويه الخلفية · frosted glass · mesh gradient

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/glass-luxury-logo/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/glass-luxury-logo/index.html`

#### 7. قدرات قريبة في العائلة

- `TEX-38` طبقة حبيبات نقطية / Dot-lattice grain overlay (proven)
- `TEX-39` مؤثرات الشيدر على الصورة والفيديو (18) / HyperFrames shader media effects (18 keys) (install)
- `TEX-41` وصفة الزجاج الداكن / Dark-only frosted glass panel recipe (documented)
- `TEX-42` وصفات زجاج الواجهات / Glassmorphism UI recipes (menus, toasts, bars, dialogs) (ready)

### `TEX-41` — وصفة الزجاج الداكن / Dark-only frosted glass panel recipe

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لوح زجاجي: تمويه خلفي 28px (40px للنوافذ البارزة)، تعبئة بيضاء 5%، حد متدرج من الأعلى، وظل محيطي واسع — على الخلفيات الداكنة فقط. / Frosted panel: 28 px backdrop blur (40 px spotlight), 5% white fill, top-lit gradient border, wide ambient shadow — dark backgrounds only.

**متى:** حين تحتاج لوحًا أو شارة زجاجية مصنفرة على خلفية داكنة بحد مضيء وظل واسع / when you need a frosted glass panel or badge on a dark background with a lit border and wide shadow

**كيف:** backdrop-filter blur(28px); background rgba(255,255,255,.05); 1px border with a 180° gradient .12→.02 (border-image or mask trick); box-shadow 0 24px 80px rgba(0,0,0,.25). Badge variant: pill radius 9999, blur 12 px, border .15, cyan glow 0 8px 32px rgba(56,189,248,.2).

**المعاملات:** blur 28/40 px; fill .05; border .12→.02; shadow 0 24px 80px .25

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** زجاج · glass · frosted · panel · badge · زجاج مصنفر · وضع داكن · شارة · dark mode · blur

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`
- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:34`

#### 7. قدرات قريبة في العائلة

- `TEX-39` مؤثرات الشيدر على الصورة والفيديو (18) / HyperFrames shader media effects (18 keys) (install)
- `TEX-40` بطاقة زجاجية فاخرة بعمق / Luxury depth glass cards (proven)
- `TEX-42` وصفات زجاج الواجهات / Glassmorphism UI recipes (menus, toasts, bars, dialogs) (ready)
- `TEX-43` غلاف زجاجي فوق عالم ثلاثي / Glass shell over a live 3D background (ready)

### `TEX-42` — وصفات زجاج الواجهات / Glassmorphism UI recipes (menus, toasts, bars, dialogs)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أسطح شفافة بتمويه مع تشبع معزز لقوائم وتلميحات وتنبيهات وشريط علوي ونافذة حوار — من أنظمة تصميم المالك. / Translucent saturated-blur surfaces for dropdowns, tooltips, toasts, sticky top bars and dialogs — from the owner design systems.

**متى:** عند تصميم قوائم وتنبيهات وتلميحات وشريط علوي ونوافذ حوار زجاجية شفافة في الواجهة / when styling dropdowns, toasts, tooltips, top bars and dialogs as translucent blurred glass

**كيف:** dropdown saturate(180%) blur(24px) radius 24; tooltip blur(20px); toast saturate(180%) blur(22px); top bar color-mix(surface 92%) + saturate(1.4) blur(10px); scrim rgba(0,0,0,.32) blur(6px); audit topbars color-mix(var(--card) 92–96%) + blur 12–20 px; dialog radius 22 shadow 0 30px 100px #15111a45.

**المعاملات:** blur 6/10/12–24 px; saturate 140–180%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** زجاج · واجهة · glass · ui · toast · menu · dialog · قوائم · تنبيهات · نافذة حوار · glassmorphism · tooltip

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-earth-ci-fork/ui/ds/components.css:196`
- `kosif-earth-ci-fork/ui/ds/components.css:224`
- `kosif-audit-pro/app/globals.css:308`
- `kosif-audit-studio/studio.css:117`

#### 7. قدرات قريبة في العائلة

- `TEX-40` بطاقة زجاجية فاخرة بعمق / Luxury depth glass cards (proven)
- `TEX-41` وصفة الزجاج الداكن / Dark-only frosted glass panel recipe (documented)
- `TEX-43` غلاف زجاجي فوق عالم ثلاثي / Glass shell over a live 3D background (ready)
- `TEX-44` زجاج سائل بانكسار الحافة / Liquid glass control (edge refraction) (seen)

### `TEX-43` — غلاف زجاجي فوق عالم ثلاثي / Glass shell over a live 3D background

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بطاقة تطفو كزجاج فوق عالم WebGL بملء الشاشة يظهر خلال 1.6 ث، مع غسلة زعفرانية. / A UI card floats as frosted glass over a full-screen WebGL world that fades in over 1.6 s, with a saffron wash.

**متى:** حين تضع بطاقة واجهة زجاجية فوق عالم WebGL ثلاثي الأبعاد بملء الشاشة يظهر تدريجيًا / when floating a frosted-glass UI card over a full-screen WebGL world that fades in

**كيف:** .world fixed inset 0 opacity 0→1 1.6 s; .shell rgba(255,253,249,.96) + blur(14px) (.94 on phones); panel gradient 180° rgba(29,24,20,.12)→.58 + saffron 160° rgba(217,83,14,.26).

**المعاملات:** blur 14 px; alpha .96/.94; fade 1.6 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** زجاج · webgl · glass · shell · 3d background · خلفية ثلاثية الأبعاد · بطاقة زجاج · تلاشي · fullscreen webgl · ui card

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-earth-ci-fork/unlock.html:75`
- `kosif-earth-ci-fork/docs/design/SQC-IDENTITY-ar.md`

#### 7. قدرات قريبة في العائلة

- `TEX-41` وصفة الزجاج الداكن / Dark-only frosted glass panel recipe (documented)
- `TEX-42` وصفات زجاج الواجهات / Glassmorphism UI recipes (menus, toasts, bars, dialogs) (ready)
- `TEX-44` زجاج سائل بانكسار الحافة / Liquid glass control (edge refraction) (seen)
- `TEX-45` حروف وأشكال من زجاج متجمد / Frosted glass shapes and letters (seen)

### `TEX-44` — زجاج سائل بانكسار الحافة / Liquid glass control (edge refraction)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جسم مموّه 14px، وفي شريط حافة 12px نسخة مكبرة 1.06× تحاكي الانكسار، مع تعبئة حليبية ولمعة علوية وهالة باستيل خلفه. / Body blurred 14 px; in a 12 px edge band a 1.06× magnified copy fakes refraction; milky fill, top sheen and a pastel aura behind.

**متى:** عند طلب زر أو عنصر تحكم بأسلوب الزجاج السائل بانكسار عند الحافة ولمعة وهالة / when the user wants a liquid-glass button or control with edge refraction, sheen and a soft aura

**كيف:** Canvas: capture backdrop → blur body; clip ring band and draw backdrop scaled 1.06 about the centre, slightly blurred; 1 px bright rim; soft lift shadow. HyperFrames blocks ios26-liquid-glass / macos-tahoe-liquid-glass / liquid-glass-widgets exist (npx hyperframes add …, untested here).

**المعاملات:** body blur 14 px, edge band 12 px, magnify 1.06

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** زجاج سائل · liquid glass · refraction · ios · button · زر زجاجي · انكسار الحافة · لمعة · glass button · canvas

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `os:macos` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-rossaxbt-3085b7`
- `kosif-one/vendor/hyperframes/registry/blocks/ios26-liquid-glass`

#### 7. قدرات قريبة في العائلة

- `TEX-42` وصفات زجاج الواجهات / Glassmorphism UI recipes (menus, toasts, bars, dialogs) (ready)
- `TEX-43` غلاف زجاجي فوق عالم ثلاثي / Glass shell over a live 3D background (ready)
- `TEX-45` حروف وأشكال من زجاج متجمد / Frosted glass shapes and letters (seen)
- `TEX-46` زجاج بانكسار وتشتت لوني (3D) / Refraction + chromatic dispersion glass (install)

### `TEX-45` — حروف وأشكال من زجاج متجمد / Frosted glass shapes and letters

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نسخة مموّهة 20–40px ومفتّحة +20% من الخلفية مقصوصة على مسار الشكل أو النص، بحافة علوية 1px. / A blurred (20–40 px), +20% lightened copy of the backdrop clipped to a shape or text path, with a bright 1 px top rim.

**متى:** حين تريد حروفًا أو أشكالًا أو صندوق إدخال من زجاج متجمد يطل على الخلفية المموهة / when you want letters, shapes or a prompt box made of frosted glass over a blurred backdrop

**كيف:** Clip(text path) → draw blurred backdrop → white overlay .25 → rim rgba(255,255,255,.7). Prompt-box variant: blur 24 px saturate 1.4, white 35%, radius 60, springs open with ~2% width overshoot. Arabic letters: clip with the shaped word, never per-letter.

**المعاملات:** blur 30 px, overlay .25, rim .7

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** زجاج · حروف · glass text · frosted · prompt box · نص زجاجي · زجاج مصنفر · كتابة عربية · clip path · glass letters

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-notdwd-7de38a`
- `kosif-tool/styles/pm-notdwd-c2037d`

#### 7. قدرات قريبة في العائلة

- `TEX-43` غلاف زجاجي فوق عالم ثلاثي / Glass shell over a live 3D background (ready)
- `TEX-44` زجاج سائل بانكسار الحافة / Liquid glass control (edge refraction) (seen)
- `TEX-46` زجاج بانكسار وتشتت لوني (3D) / Refraction + chromatic dispersion glass (install)
- `TEX-47` ذهب معدني بلمعة متحركة / Metallic gold with moving sheen (proven)

### `TEX-46` — زجاج بانكسار وتشتت لوني (3D) / Refraction + chromatic dispersion glass

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أجسام زجاج/كريستال تكسر الخلفية وتفصلها إلى حواف قوس قزح. / Glass/crystal objects that bend the background and split it into rainbow fringes.

**متى:** عند عرض أجسام زجاج أو كريستال ثلاثية الأبعاد تكسر الخلفية وتفصلها لحواف قوس قزح / for 3D glass or crystal objects that bend the background and split it into rainbow fringes

**كيف:** Render background to an FBO; refract(eye, normal, 1/IOR) per channel with separate IOR for R/G/B; backside pass first for internal dispersion. Shortcut: drei MeshTransmissionMaterial (React).

**المعاملات:** IOR 1.31 base; per-channel IOR spread ~.02

**التثبيت:** npm i three @react-three/fiber @react-three/drei

**الوسوم:** زجاج · انكسار · refraction · dispersion · crystal · three.js · كريستال · قوس قزح · تشتت · rainbow · ior

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `TEX-44` زجاج سائل بانكسار الحافة / Liquid glass control (edge refraction) (seen)
- `TEX-45` حروف وأشكال من زجاج متجمد / Frosted glass shapes and letters (seen)
- `TEX-47` ذهب معدني بلمعة متحركة / Metallic gold with moving sheen (proven)
- `TEX-48` كرة لامعة من تدرجات / Glossy 2D sphere / orb from gradients (seen)

### `TEX-47` — ذهب معدني بلمعة متحركة / Metallic gold with moving sheen

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كلمة ذهبية من أربع طبقات: توهج، حافة محفورة، تدرج معدني بسبع وقفات، ولمعة بقناع 105° تعبر الكلمة. / Gold word in four stacked copies: glow, engraved edge, a 7-stop metal gradient and a 105° masked sheen sweeping across.

**متى:** حين تريد كلمة أو شعارًا ذهبيًا فاخرًا بلمعة تعبر النص / when you want a luxurious gold word or logo with a moving sheen sweeping across the text

**كيف:** Gradient 180°: #fff4d6 0, #f0d793 16, #c9a24a 40, #8a6424 56, #b88d3a 68, #f2dc9c 86, #fff4d6 100 via background-clip:text; glow #c9a24a blur 26 px .42; edge #4a3110 offset 4 px; sheen copy #fffaf0→#ffe9b8 visible in a ±9% band (plus a thinner .55 follower). Rendered in proofs/glass-luxury-logo.

**المعاملات:** sheen band ±9%, angle 105°, glide easing cubic-bezier(.65,0,.35,1)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ذهب · معدن · لمعة · gold · metallic · sheen · luxury · نص ذهبي · شعار · فخامة · gold text · shine

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/glass-luxury-logo/README.md`

#### 7. قدرات قريبة في العائلة

- `TEX-45` حروف وأشكال من زجاج متجمد / Frosted glass shapes and letters (seen)
- `TEX-46` زجاج بانكسار وتشتت لوني (3D) / Refraction + chromatic dispersion glass (install)
- `TEX-48` كرة لامعة من تدرجات / Glossy 2D sphere / orb from gradients (seen)
- `TEX-49` كروم يعكس المشهد حيًا / Chrome via live CubeCamera reflection (install)

### `TEX-48` — كرة لامعة من تدرجات / Glossy 2D sphere / orb from gradients

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كرة لامعة بتدرجات شعاعية متراكبة: جسم، انعكاسات دوارة، بقعة لمعان علوية يسار، ضوء حافة وتوهج خارجي. / Stacked radial gradients: body, rotating inner reflections, top-left specular, rim light and outer glow.

**متى:** عند رسم كرة أو أورب لامعة ثنائية الأبعاد بالتدرجات فقط مع لمعة وضوء حافة وتوهج / when drawing a glossy 2D orb or sphere from gradients only, with specular, rim light and glow

**كيف:** Body #5b9bff→#1239a0 (or #a88bff→#6c3bff), rim #c9f4ff; white elliptical blurred specular at top (opacity .6), small orange inner hotspot, outer purple glow + faint concentric halo rings.

**المعاملات:** highlight .6; rim 2–4 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كرة · لامع · orb · glossy · sphere · gradient · أورب · كرة مضيئة · تدرجات · radial gradient · specular

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/infographic`
- `kosif-tool/styles/product`

#### 7. قدرات قريبة في العائلة

- `TEX-46` زجاج بانكسار وتشتت لوني (3D) / Refraction + chromatic dispersion glass (install)
- `TEX-47` ذهب معدني بلمعة متحركة / Metallic gold with moving sheen (proven)
- `TEX-49` كروم يعكس المشهد حيًا / Chrome via live CubeCamera reflection (install)
- `TEX-50` ظلال ارتفاع ناعمة متعددة / Layered soft elevation shadows (ready)

### `TEX-49` — كروم يعكس المشهد حيًا / Chrome via live CubeCamera reflection

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كرة مرآة تعكس الوادي الحقيقي عبر كاميرا مكعبة تُحدّث كل إطار. / A mirror sphere reflects the actual scene through a cube camera updated every frame.

**متى:** حين تريد كرة كروم أو مرآة تعكس المشهد الثلاثي نفسه حيًا كل إطار / when you want a chrome mirror sphere reflecting the actual 3D scene live every frame

**كيف:** WebGLCubeRenderTarget(256, HalfFloat, mipmaps); CubeCamera(.05, 600); MeshStandardMaterial metalness 1, roughness .06, envMap = cube; per frame: hide orb → cubeCam.update → show. The demo project loads assets/main.bundle.js, which is not built in this checkout — install esbuild and bundle first; the kit itself (three-kit.bundle.js) is prebuilt.

**المعاملات:** 256², half float; roughness .06

**التثبيت:** cd 100-superskills/skills/kosif-montage-motion/scripts && npm install three@0.186.1 esbuild && python3 motion.py bundle sound_ground

**الوسوم:** كروم · انعكاس · chrome · cubecamera · reflection · three.js · مرآة · معدن عاكس · كرة كروم · mirror · env map

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:esbuild` ← npm ls esbuild أو وجود node_modules/esbuild
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:51`
- `100-superskills/skills/kosif-montage-motion/SKILL.md:106`

#### 7. قدرات قريبة في العائلة

- `TEX-47` ذهب معدني بلمعة متحركة / Metallic gold with moving sheen (proven)
- `TEX-48` كرة لامعة من تدرجات / Glossy 2D sphere / orb from gradients (seen)
- `TEX-50` ظلال ارتفاع ناعمة متعددة / Layered soft elevation shadows (ready)
- `TEX-51` نسيج الضوضاء الكسرية / Fractal value-noise material (Studio painter) (proven)

### `TEX-50` — ظلال ارتفاع ناعمة متعددة / Layered soft elevation shadows

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاثة مستويات ظل من ظل تلامس رفيع وظل محيطي كبير بانتشار سالب ملوّن بلون العلامة الداكن. / Three elevation tokens: a hairline contact shadow plus a large negative-spread ambient shadow tinted with the brand dark.

**متى:** عند الحاجة لظلال ارتفاع ناعمة لبطاقات الواجهة بثلاثة مستويات ملوّنة بلون العلامة الداكن / when UI cards need soft layered elevation shadows in three levels tinted with the brand dark

**كيف:** cobalt: 0 1px 2px rgba(11,16,48,.05), 0 12px 32px −24px rgba(11,16,48,.36) / 0 18px 40px −22px .32 / 0 32px 80px −28px .48; ledger uses rgba(29,24,20,…).

**المعاملات:** --sk-shadow-1/2/3

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ظل · shadow · elevation · tokens · depth · ظلال ناعمة · بطاقات · عمق · box-shadow · soft shadow

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-earth-ci-fork/ui/ds/tokens.css:184`

#### 7. قدرات قريبة في العائلة

- `TEX-48` كرة لامعة من تدرجات / Glossy 2D sphere / orb from gradients (seen)
- `TEX-49` كروم يعكس المشهد حيًا / Chrome via live CubeCamera reflection (install)
- `TEX-51` نسيج الضوضاء الكسرية / Fractal value-noise material (Studio painter) (proven)
- `TEX-52` نقش الحراشف والقرميد / Scales / tiles pattern (proven)

### `TEX-51` — نسيج الضوضاء الكسرية / Fractal value-noise material (Studio painter)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ضوضاء قيمية متعددة الطبقات ببذرة داخل الشكل، تقرأها العين كجلد أو صخر أو خطوط ماء أو فرو أو ضباب. / Seeded multi-octave value noise inside a shape that reads as skin, rock, water streaks, fur or fog.

**متى:** حين تريد إعطاء شكل مسطح ملمس جلد أو صخر أو ماء أو فرو أو ضباب في رسام Studio / when giving a flat shape a skin, rock, water, fur or fog texture in the Studio painter

**كيف:** noise(shape, amount, cell, seed, mode="multiply"\|"normal"\|"add"\|"screen", colour, octaves=4, stretch=(sx,sy)). Test test_realism_primitives_change_a_flat_fill passed here.

**المعاملات:** skin cell 10–14 multiply; water stretch (6,1); cloud cell 60 + blur; rock cell 26 + cold rim; sky 160 multiply .35

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ضوضاء · noise · fbm · skin · rock · pillow · studio · ملمس · صخر · جلد · value noise · texture

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-studio/render.py:496`
- `kosif-studio/references/drawing-guide.md:62`
- `kosif-studio/tests/test_studio.py:71`
- `100-superskills/skills/pixel-studio-painter/scripts/render.py`

#### 7. قدرات قريبة في العائلة

- `TEX-49` كروم يعكس المشهد حيًا / Chrome via live CubeCamera reflection (install)
- `TEX-50` ظلال ارتفاع ناعمة متعددة / Layered soft elevation shadows (ready)
- `TEX-52` نقش الحراشف والقرميد / Scales / tiles pattern (proven)
- `TEX-53` إضاءة بارزة بخريطة ارتفاع / Relief lighting (height field + SSS) (proven)

### `TEX-52` — نقش الحراشف والقرميد / Scales / tiles pattern

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أقواس متداخلة متعاقبة مقصوصة على الشكل: حراشف زواحف، جلد سمك، قرميد أسقف. / Staggered overlapping arcs clipped to a shape: reptile scales, fish skin, roof tiles.

**متى:** عند تغطية جسم بنقش حراشف زواحف أو جلد سمك أو قرميد سقف / when covering a body with a reptile-scale, fish-skin or roof-tile pattern

**كيف:** Pillow: scales(shape, size=14, colour, alpha=.35, width=1, stagger=True) over shade()/relief() (tested here). SVG: <pattern width=22 height=16 patternUnits=userSpaceOnUse> of arcs, fill the body twice — gradient then url(#scales) (duck_dragon.py).

**المعاملات:** row step size·.55; dragon hide size 8 alpha .22 width .8; SVG tile 22×16 strokes #052e16 1.6 .55 + #4ade80 1 .25

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حراشف · قرميد · scales · tiles · dragon · pattern · تنين · سمك · زواحف · fish scales · svg pattern

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-studio/render.py:539`
- `kosif-studio/tests/test_studio.py:71`
- `kosif-studio/scenes/whale_dragon.py:164`
- `kosif-one/projects/duck-vs-dragon/duck_dragon.py`

#### 7. قدرات قريبة في العائلة

- `TEX-50` ظلال ارتفاع ناعمة متعددة / Layered soft elevation shadows (ready)
- `TEX-51` نسيج الضوضاء الكسرية / Fractal value-noise material (Studio painter) (proven)
- `TEX-53` إضاءة بارزة بخريطة ارتفاع / Relief lighting (height field + SSS) (proven)
- `TEX-54` سطح ماء يلمع / Water surface with light glints (Studio) (ready)

### `TEX-53` — إضاءة بارزة بخريطة ارتفاع / Relief lighting (height field + SSS)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يضيء الشكل كحقل ارتفاع بتشتت تحت السطح ونتوءات وخشونة وفرينل ولمعان. / Lights a shape as a height field with subsurface scattering, bumps, roughness, Fresnel and specular.

**متى:** حين تريد إضاءة شكل كحقل ارتفاع بنتوءات ولمعان وتشتت تحت السطح ليبدو مجسمًا / when lighting a shape as a height field with bumps, specular and subsurface scattering so it reads as solid

**كيف:** relief(shape, lights=[(x,y,z,colour,power)], base, ambient=.22, bulge=.6, plateau=.5, bumps=[(scale,amp)], sss, roughness). Tested here (test_camera_ops_run_and_change_the_picture: >30 distinct colours in the lit patch).

**المعاملات:** ambient .22, bulge .6, plateau .5; bumps e.g. [(2,20),(.5,4)], sss 4, roughness .5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إضاءة · ارتفاع · relief · height field · sss · fresnel · تجسيم · بروز · لمعان · bump · specular

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-studio/render.py:618`
- `kosif-studio/tests/test_studio.py:81`
- `kosif-studio/scenes/whale_dragon.py`

#### 7. قدرات قريبة في العائلة

- `TEX-51` نسيج الضوضاء الكسرية / Fractal value-noise material (Studio painter) (proven)
- `TEX-52` نقش الحراشف والقرميد / Scales / tiles pattern (proven)
- `TEX-54` سطح ماء يلمع / Water surface with light glints (Studio) (ready)
- `TEX-55` ضوضاء بيرلين وfbm وridged ببذرة / Seeded CPU Perlin / fBm / ridged noise (ready)

### `TEX-54` — سطح ماء يلمع / Water surface with light glints (Studio)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أمواج من حقل ضوضاء ممدود، اللون يمزج العمق والسماء حسب ميل كل وجه، وكل ضوء يترك أثر لمعان. / Waves as a stretched noise height field; colour mixes deep and sky by facet tilt; each light leaves a trail of specular glints.

**متى:** عند رسم سطح بحر أو ماء بأمواج تمزج العمق والسماء ولمعات ضوء، حتى في مشهد عاصف / when painting a sea or water surface with waves mixing depth and sky and trails of light glints, storms included

**كيف:** water(area, lights, deep, sky, cell, stretch, height, seed, shininess, spec, octaves) in render.py (not covered by a test).

**المعاملات:** deep #0a1118, sky #2a3a4c, cell 18, stretch 6, height 6, shininess 60, spec 1.2; storm #060a0f/#28323f cell 20 stretch 7 height 7 shininess 70

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ماء · بحر · water · glints · specular · studio · أمواج · لمعان الماء · عاصفة · sea · waves

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-studio/render.py:652`
- `kosif-studio/scenes/whale_dragon.py:115`

#### 7. قدرات قريبة في العائلة

- `TEX-52` نقش الحراشف والقرميد / Scales / tiles pattern (proven)
- `TEX-53` إضاءة بارزة بخريطة ارتفاع / Relief lighting (height field + SSS) (proven)
- `TEX-55` ضوضاء بيرلين وfbm وridged ببذرة / Seeded CPU Perlin / fBm / ridged noise (ready)
- `TEX-56` خامات مولّدة بلا تنزيل / Generated textures: noiseCanvas / normalFromHeight / spriteTex (ready)

### `TEX-55` — ضوضاء بيرلين وfbm وridged ببذرة / Seeded CPU Perlin / fBm / ridged noise

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ضوضاء ثنائية حتمية (بذرة 1337) للتضاريس والخامات وتوزيع العناصر. / Deterministic 2D Perlin, fractal Brownian motion and ridged noise (seed 1337) for terrain, textures and placement.

**متى:** حين تحتاج ضوضاء حتمية للتضاريس أو الخامات أو توزيع العناصر في three-kit / when you need deterministic noise for terrain, textures or placing items in three-kit

**كيف:** three-kit.bundle.js → K3.perlin(x,y), K3.fbm(x,y,oct,lac,gain), K3.ridged(x,y,oct) + smooth/ramp/clamp01/lerp. Outside the kit: simplex-noise (npm) or opensimplex (pip).

**المعاملات:** fbm oct 5 lac 2.0 gain .5; ridged lac 2.1 gain .5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ضوضاء · perlin · fbm · ridged · noise · terrain · تضاريس · توزيع عشوائي · ضوضاء بيرلين · procedural · simplex

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-studio/motion/kit/three-kit.js:24`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:24`
- `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:24`

#### 7. قدرات قريبة في العائلة

- `TEX-53` إضاءة بارزة بخريطة ارتفاع / Relief lighting (height field + SSS) (proven)
- `TEX-54` سطح ماء يلمع / Water surface with light glints (Studio) (ready)
- `TEX-56` خامات مولّدة بلا تنزيل / Generated textures: noiseCanvas / normalFromHeight / spriteTex (ready)
- `TEX-57` خامة بدن خشبي مدهون / Procedural painted wooden hull (proven)

### `TEX-56` — خامات مولّدة بلا تنزيل / Generated textures: noiseCanvas / normalFromHeight / spriteTex

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يولد خامات Canvas من دوال، وخرائط normal من دوال ارتفاع، وسبرايت جسيمات ناعمة/حلقية/خطية. / Canvas textures from functions, normal maps from height functions and soft/ring/streak particle sprites — no downloads.

**متى:** عند الحاجة لخامات أو خرائط normal أو سبرايت جسيمات في three.js دون تحميل أي صور / when you need textures, normal maps or particle sprites in three.js without downloading images

**كيف:** K3.noiseCanvas(N,(x,y)=>[r,g,b,a]); K3.normalFromHeight(N, h, strength); K3.spriteTex("soft"\|"ring"\|"streak"); RepeatWrapping.

**المعاملات:** sprites 128 px; ring warm stop rgba(255,220,180,.35)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خامة · normal map · procedural texture · sprite · three.js · خرائط نورمال · جسيمات · بدون صور · particles · canvas texture

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-studio/motion/kit/three-kit.js:41`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:48`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:57`

#### 7. قدرات قريبة في العائلة

- `TEX-54` سطح ماء يلمع / Water surface with light glints (Studio) (ready)
- `TEX-55` ضوضاء بيرلين وfbm وridged ببذرة / Seeded CPU Perlin / fBm / ridged noise (ready)
- `TEX-57` خامة بدن خشبي مدهون / Procedural painted wooden hull (proven)
- `TEX-58` خامة قمر إجرائية / Procedural moon texture (proven)

### `TEX-57` — خامة بدن خشبي مدهون / Procedural painted wooden hull

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أشرطة طلاء، فواصل ألواح، عروق خشب وطلاء مقشور لقارب تقليدي — على Canvas بلا صور. / Paint bands, plank seams, wood grain and chipped paint for a traditional boat — generated on a canvas.

**متى:** حين تحتاج بدن قارب خشبي تقليدي مدهون بأشرطة وألواح وطلاء مقشور دون صور / when you need a traditional painted wooden boat hull with plank seams and chipped paint, no images

**كيف:** Canvas 1024×256 bands [0–.30 #4a1f17, .30–.78 #1d5f78, .78–.84 #e9e2cf, .84–.92 #b5432c, .92–1 #c89a52]; seam every 9 px; n = fbm(x/60,y/5)·.10 + noise·.05 − .12 where fbm(x/9,y/140) < −.35 (chips); CanvasTexture sRGB, anisotropy 8, roughness .62. Frames rendered here from night_boat via window.seek (SwiftShader WebGL).

**المعاملات:** 1024×256; seam 9 px; chip threshold −.35

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خشب · قارب · wood · hull · procedural · three.js · مركب · طلاء مقشور · ألواح خشب · boat · wood grain

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:25`

#### 7. قدرات قريبة في العائلة

- `TEX-55` ضوضاء بيرلين وfbm وridged ببذرة / Seeded CPU Perlin / fBm / ridged noise (ready)
- `TEX-56` خامات مولّدة بلا تنزيل / Generated textures: noiseCanvas / normalFromHeight / spriteTex (ready)
- `TEX-58` خامة قمر إجرائية / Procedural moon texture (proven)
- `TEX-59` طوب إجرائي يتلوّن بالضوء / Procedural brick lit by a light map (multiply) (proven)

### `TEX-58` — خامة قمر إجرائية / Procedural moon texture

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قمر مكتمل من الرياضيات: إعتام الحافة، بحار داكنة من الضوضاء، فوهات صغيرة، حافة ألفا ناعمة، ساطع بما يكفي للتوهج. / A full moon from maths: limb darkening, noise maria, small craters, soft alpha edge, bright enough to bloom.

**متى:** عند الحاجة لقمر مكتمل ساطع في مشهد ليلي مولّد رياضيًا بفوهات وبحار داكنة / when you need a bright full moon for a night scene, generated mathematically with maria and craters

**كيف:** 512² canvas: limb = (1−r²)^.22; maria = smooth(.05,.35,fbm(2.2u,2.2v,5))·.32; craters = max(0,fbm(14u,14v,3))·.12; rgb(255,250,236)·l; disc 2.1° wide at 9000 units; halo sprite ×7 at .28. Rendered here (night_boat frames).

**المعاملات:** limb exponent .22; maria .32; craters .12; halo ×7 .28

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قمر · ليل · moon · procedural · night · رمضان · بدر · قمر مكتمل · سماء ليلية · full moon · craters

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:115`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:156`

#### 7. قدرات قريبة في العائلة

- `TEX-56` خامات مولّدة بلا تنزيل / Generated textures: noiseCanvas / normalFromHeight / spriteTex (ready)
- `TEX-57` خامة بدن خشبي مدهون / Procedural painted wooden hull (proven)
- `TEX-59` طوب إجرائي يتلوّن بالضوء / Procedural brick lit by a light map (multiply) (proven)
- `TEX-60` غيوم SVG إجرائية / Procedural SVG clouds (feTurbulence + displacement) (proven)

### `TEX-59` — طوب إجرائي يتلوّن بالضوء / Procedural brick lit by a light map (multiply)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جدار طوب ببذرة ثابتة يُضرب في خريطة ضوء من انبعاث مموّه، فيأخذ لون اللافتة وتبقى فواصل الملاط معتمة. / Seeded procedural brick multiplied by a light map built from blurred emission, so it takes the sign colour while mortar stays dark.

**متى:** حين يجب أن يتلون جدار طوب بضوء لافتة نيون بينما تبقى فواصل الملاط معتمة / when a brick wall must take the colour of a neon sign's light while the mortar stays dark

**كيف:** Light map at ¼ res = ambient #1b1f30 + emission blurred 40 px ×1.0 + 140 px ×1.95, multiplied into brick (row 24 px, offset half on odd rows, mortar 3 px, per-brick tone from noise, fine grain). Rendered in proofs/neon-glow (13/13) and the texture lab.

**المعاملات:** seed 20261016; ambient #1b1f30; blur 40/140 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** طوب · جدار · brick · wall · light map · neon · نيون · لافتة · إضاءة جدار · sign glow · mortar

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-59` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/index.html`

#### 7. قدرات قريبة في العائلة

- `TEX-57` خامة بدن خشبي مدهون / Procedural painted wooden hull (proven)
- `TEX-58` خامة قمر إجرائية / Procedural moon texture (proven)
- `TEX-60` غيوم SVG إجرائية / Procedural SVG clouds (feTurbulence + displacement) (proven)
- `TEX-61` كلمة عربية مملوءة بسائل / Fluid-noise filled Arabic word (proven)

### `TEX-60` — غيوم SVG إجرائية / Procedural SVG clouds (feTurbulence + displacement)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سحب ركامية ناعمة من قطوع ناقصة يشوّهها ضوضاء كسرية وتمويه، فوق تدرج سماء وشمس شعاعية — 2.6KB بدل صورة. / Soft cumulus from plain ellipses distorted by fractal noise and blurred, over a sky gradient and radial sun — 2.6 KB instead of a raster.

**متى:** عند الحاجة لسماء بسحب ناعمة وشمس كخلفية SVG خفيفة الحجم بدل صورة / when you need a sky of soft clouds and sun as a lightweight SVG instead of a raster image

**كيف:** feTurbulence fractalNoise baseFrequency .011, 5 octaves, seed 11 → feDisplacementMap scale 70 (R/G) → feGaussianBlur 5; far layer .009 / 4 oct / scale 55 / blur 12; sky #f1e3bf .3 #d4b06a .62 #f2732d 1 #1d1814; sun radial cx .62 cy .18. Drift by translating the group, never by changing the seed. Rendered here (lab).

**المعاملات:** viewBox 800×600, preserveAspectRatio xMidYMid slice

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** غيوم · سماء · clouds · sky · feTurbulence · svg · سحب · شمس · خلفية سماء · cumulus · lightweight

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-60` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-earth-ci-fork/ui/art/kosif-sky.svg`
- `kosif-earth-ci-fork/docs/design/KOSIF-LUXE.md`

#### 7. قدرات قريبة في العائلة

- `TEX-58` خامة قمر إجرائية / Procedural moon texture (proven)
- `TEX-59` طوب إجرائي يتلوّن بالضوء / Procedural brick lit by a light map (multiply) (proven)
- `TEX-61` كلمة عربية مملوءة بسائل / Fluid-noise filled Arabic word (proven)
- `TEX-62` نص بأقنعة الخامات (66 قناعًا) / Texture-mask text (66 PBR masks) (install)

### `TEX-61` — كلمة عربية مملوءة بسائل / Fluid-noise filled Arabic word

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ضوضاء fbm مشوّهة المجال بثلاثة ألوان تملأ كلمة عربية كاملة كقناع، ثم يكبر القناع حتى يملأ السائل الكادر. / Domain-warped fbm in three colours fills a whole shaped Arabic word as a mask; the mask then scales up until the fluid fills the frame.

**متى:** حين تريد كلمة عربية مملوءة بسائل ملون متحرك ثم تكبر حتى يملأ السائل الكادر كانتقال / when an Arabic word is filled with moving coloured fluid, then scales up until the fluid fills the frame as a transition

**كيف:** Canvas: draw warped fbm (w = fbm(p/90 + t·.3); v = fbm(p/60 + 2w)) quantised to 3 inks, then globalCompositeOperation="destination-in" + fillText(word) with direction rtl — the word stays joined. Rendered here (lab, Lalezar). For the transition, animate the font size/scale 1→12 and overlay outline text.

**المعاملات:** fbm 4–5 octaves, warp 2×; inks #2f4bff #e8503c #ff7ad9

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سائل · عربي · fluid · mask · fbm · text fill · domain warp · كلمة عربية · تعبئة النص · ترانزيشن · arabic text · liquid

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-61` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-prasenx-8d9323`
- `kosif-tool/playbooks/arabic-typography.md`

#### 7. قدرات قريبة في العائلة

- `TEX-59` طوب إجرائي يتلوّن بالضوء / Procedural brick lit by a light map (multiply) (proven)
- `TEX-60` غيوم SVG إجرائية / Procedural SVG clouds (feTurbulence + displacement) (proven)
- `TEX-62` نص بأقنعة الخامات (66 قناعًا) / Texture-mask text (66 PBR masks) (install)
- `TEX-63` كتل شيدر المواد (WebGPU) / HyperFrames material shader blocks (install)

### `TEX-62` — نص بأقنعة الخامات (66 قناعًا) / Texture-mask text (66 PBR masks)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | المكوّن Apache-2.0؛ الأقنعة من ambientCG برخصة CC0 / component Apache-2.0, masks CC0 (ambientCG). |

**ما هي:** أقنعة إضاءة CSS تثقب خامة داخل الحروف: طوب، رخام، خشب، حمم، ثلج، جلد… من خرائط ambientCG. / CSS luminance masks punch texture into letterforms: bricks, marble, wood, lava, snow, leather… from ambientCG colour maps.

**متى:** عند كتابة نص بحروف مملوءة بخامة طوب أو رخام أو خشب أو حمم أو ثلج أو جلد / when letters should be filled with a texture such as brick, marble, wood, lava, snow or leather

**كيف:** npx hyperframes add texture-mask-text; classes texture-text + hf-texture-<name>; lint rules texture_class_unknown / texture_text_missing_mask. For Arabic, apply the mask to the whole shaped word element. The 66 PNG masks also ship inside held-text-strobe-burst assets.

**المعاملات:** 66 masks: asphalt, bark, bricks, carpet, concrete, diamond-plate, fabric, grass, ground, lava, leather, marble, metal, onyx, plaster, paving, road, rock, snow, tiles, travertine, wood, wood-floor…

**التثبيت:** npx hyperframes add texture-mask-text

**الوسوم:** خامة · نص · texture text · mask · marble · lava · wood · حروف بخامة · رخام · خشب · textured letters · hyperframes

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-62` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-one/vendor/hyperframes/registry/components/texture-mask-text/registry-item.json`
- `kosif-one/vendor/hyperframes/packages/lint/src/rules/textures.ts`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/templates/held-text-strobe-burst/assets/texture-mask-text/masks/lava.png`

#### 7. قدرات قريبة في العائلة

- `TEX-60` غيوم SVG إجرائية / Procedural SVG clouds (feTurbulence + displacement) (proven)
- `TEX-61` كلمة عربية مملوءة بسائل / Fluid-noise filled Arabic word (proven)
- `TEX-63` كتل شيدر المواد (WebGPU) / HyperFrames material shader blocks (install)
- `TEX-64` حقل الحبيبات ونزف الحبر / Grain field & ink-bleed reveal (HyperFrames) (install)

### `TEX-63` — كتل شيدر المواد (WebGPU) / HyperFrames material shader blocks

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 + مكتبة Shaders برخصة MIT (راجع shaders.THIRD-PARTY-LICENSES.txt) / Apache-2.0 AND MIT. |

**ما هي:** خلفيات/أجسام شيدر جاهزة مدتها 2 ث: chrome-orb, liquid-metal, marble, obsidian, plastic, holographic, thin-film, water, frost, fractal/gabor/worley noise، وغيرها (aurora, plasma, nebula, mesh-gradient, halftone-field…). / Ready 2 s shader plates: chrome, liquid metal, marble, obsidian, plastic, holographic, thin film, water, frost, fractal/Gabor/Worley noise and more.

**متى:** حين تحتاج خلفية أو جسمًا جاهزًا بشيدر مادة: كروم أو معدن سائل أو رخام أو هولوغرام أو ماء أو صقيع / when you need a ready shader plate: chrome, liquid metal, marble, holographic, water, frost and more

**كيف:** npx hyperframes add <block> (or put lib/shaders.iife.js next to the page) then <canvas data-shader="Marble" width=1920 height=1080> inside a root marked data-requires-webgpu data-no-timeline. Needs a WebGPU-capable Chromium — not verified here (only WebGL via SwiftShader was).

**المعاملات:** 1920×1080, 2 s; shaders.iife.js 1,444,793 B (shaders 4.0.0)

**التثبيت:** npx hyperframes add marble

**الوسوم:** شيدر · رخام · معدن سائل · marble · liquid metal · holographic · webgpu · hyperframes · كروم · هولوغرام · خلفية شيدر · chrome · shader background

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-63` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-one/vendor/hyperframes/registry/blocks/marble/registry-item.json`
- `kosif-one/vendor/hyperframes/registry/blocks/liquid-metal/liquid-metal.html`
- `kosif-one/vendor/hyperframes/registry/blocks/chrome-orb/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### 7. قدرات قريبة في العائلة

- `TEX-61` كلمة عربية مملوءة بسائل / Fluid-noise filled Arabic word (proven)
- `TEX-62` نص بأقنعة الخامات (66 قناعًا) / Texture-mask text (66 PBR masks) (install)
- `TEX-64` حقل الحبيبات ونزف الحبر / Grain field & ink-bleed reveal (HyperFrames) (install)
- `TEX-65` غيوم بخطوط فرشاة وسماء سديمية / Painterly streak clouds & nebula skies (seen)

### `TEX-64` — حقل الحبيبات ونزف الحبر / Grain field & ink-bleed reveal (HyperFrames)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0. |

**ما هي:** حقل نقاط ملوّن ينجرف فوق تدرج في حلقة، وحبر سائل يتفتح في الورق بفلتر لزج ثم ينكمش لعلامة حادة. / Accent-tinted dot field drifting in a seamless loop; liquid ink blooming through paper with a gooey blur+threshold filter, then resolving to a crisp mark.

**متى:** عند الحاجة لحقل نقاط ملون متحرك في حلقة أو حبر يتفتح في الورق ثم يستقر كعلامة حادة / for a looping tinted dot field, or liquid ink blooming through paper and resolving into a crisp mark

**كيف:** npx hyperframes add grain-field \| grain-overlay \| ink-bleed-reveal; mount on a class="clip" div with data-composition-src + data-start/data-duration/data-track-index; overrides via data-variable-values JSON; extra duration becomes hold, never time-stretch. Gooey filter = feGaussianBlur 10 → feColorMatrix alpha ×18 −7.

**المعاملات:** grain-field density fine\|coarse; ink blobs 4–6; exit none\|fade\|up

**التثبيت:** npx hyperframes add ink-bleed-reveal

**الوسوم:** حبر · حبيبات · ink bleed · gooey · grain field · hyperframes · نزف الحبر · كشف علامة · حلقة متكررة · ink reveal · seamless loop

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-64` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-one/vendor/hyperframes/registry/components/grain-field/grain-field.html`
- `kosif-one/vendor/hyperframes/registry/components/ink-bleed-reveal/ink-bleed-reveal.html`
- `kosif-one/vendor/hyperframes/registry/components/grain-overlay/grain-overlay.html`

#### 7. قدرات قريبة في العائلة

- `TEX-62` نص بأقنعة الخامات (66 قناعًا) / Texture-mask text (66 PBR masks) (install)
- `TEX-63` كتل شيدر المواد (WebGPU) / HyperFrames material shader blocks (install)
- `TEX-65` غيوم بخطوط فرشاة وسماء سديمية / Painterly streak clouds & nebula skies (seen)
- `TEX-66` أرضية حمم بعروق مضيئة / Veined lava floor shader (seen)

### `TEX-65` — غيوم بخطوط فرشاة وسماء سديمية / Painterly streak clouds & nebula skies

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ضوضاء fbm مشوّهة المجال تُقصّ إلى خطوط ناعمة ملوّنة بتدرج السماء مع ميل نحو الشمس؛ ونسخة سديمية بنفسجية بنجوم. / Domain-warped fbm thresholded into soft streaks tinted by the sky gradient and toward the sun; a purple nebula variant with stars.

**متى:** حين تريد سماء بغيوم كخطوط فرشاة ملونة نحو الشمس أو سماء سديمية بنفسجية بنجوم / when you want a sky of brush-streak clouds tinted toward the sun, or a purple nebula sky with stars

**كيف:** Fragment shader or offline numpy: fbm 4–5 octaves, warp .3, drift .01 uv/s; rim tint toward the sun position; nebula = fbm purple/magenta + seeded star points.

**المعاملات:** fbm 4–5 oct, warp .3, drift .01 uv/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** غيوم · سديم · clouds · nebula · shader · sky · سماء فضائية · نجوم · خطوط فرشاة · space · painterly

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:numpy` ← python3 -c "import numpy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-65` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-demitiyageekzen-7770ad`
- `kosif-tool/styles/pm-ryzoft-4f85bd`

#### 7. قدرات قريبة في العائلة

- `TEX-63` كتل شيدر المواد (WebGPU) / HyperFrames material shader blocks (install)
- `TEX-64` حقل الحبيبات ونزف الحبر / Grain field & ink-bleed reveal (HyperFrames) (install)
- `TEX-66` أرضية حمم بعروق مضيئة / Veined lava floor shader (seen)
- `TEX-67` شيدر ضربات فرشاة / Stroke-based painterly shader (idea)

### `TEX-66` — أرضية حمم بعروق مضيئة / Veined lava floor shader

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سطح بضوضاء ridged مطلقة تُقص إلى عروق برتقالية رفيعة فوق قاعدة بنفسجية عنابية، تزحف ببطء. / abs(fbm) ridged noise thresholded into thin orange veins over a purple-maroon base, slowly scrolling.

**متى:** عند الحاجة لأرضية حمم بعروق برتقالية رفيعة مضيئة تزحف ببطء فوق قاعدة داكنة / when you need a lava floor with thin glowing orange veins slowly scrolling over a dark base

**كيف:** Plane + fragment shader: v = 1 − smoothstep(0, .03, abs(fbm(uv·3 + t·.05))); colour mix(#4a2040, #f0a040, v) + bloom on the veins.

**المعاملات:** ridge width .03, #f0a040 on #4a2040, scroll .05/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حمم · lava · ridged · shader · veins · صخر منصهر · عروق مضيئة · أرضية نارية · glowing veins · fbm

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-66` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-gorden-sun-041f56`

#### 7. قدرات قريبة في العائلة

- `TEX-64` حقل الحبيبات ونزف الحبر / Grain field & ink-bleed reveal (HyperFrames) (install)
- `TEX-65` غيوم بخطوط فرشاة وسماء سديمية / Painterly streak clouds & nebula skies (seen)
- `TEX-67` شيدر ضربات فرشاة / Stroke-based painterly shader (idea)
- `TEX-68` طبقات درجات للفرشاة الجافة / Tone layers for a dry-brush look (rotoscope) (install)

### `TEX-67` — شيدر ضربات فرشاة / Stroke-based painterly shader

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاثة أحجام ضربات ترتعش 1–2px بتردد 6Hz فتبدو الأسطح مرسومة باليد، وسماء من ضربات موجّهة بحقل تدفق. / Three stroke sizes jittering 1–2 px at 6 Hz so surfaces look hand-painted; sky of flow-field-oriented stroke sprites.

**متى:** حين يطلب المستخدم أن تبدو الأسطح مرسومة يدويًا بضربات فرشاة مرتعشة كلوحة فنية / when the user wants surfaces to look hand-painted with jittering brush strokes like a painting

**كيف:** Untested idea from a brief: instanced stroke quads oriented along curl-noise, colour sampled from the underlying render, re-seeded at 6 Hz (on threes). HyperFrames kuwahara effect (TEX-39) is the cheap fallback.

**المعاملات:** 3 sizes; 1–2 px jitter @ 6 Hz

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** فرشاة · لوحة · painterly · brush strokes · flow field · رسم يدوي · لوحة فنية · ضربات · hand-painted · kuwahara

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-67` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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
- `kosif-tool/styles/pm-mandelduck-95fd08`

#### 7. قدرات قريبة في العائلة

- `TEX-65` غيوم بخطوط فرشاة وسماء سديمية / Painterly streak clouds & nebula skies (seen)
- `TEX-66` أرضية حمم بعروق مضيئة / Veined lava floor shader (seen)
- `TEX-68` طبقات درجات للفرشاة الجافة / Tone layers for a dry-brush look (rotoscope) (install)
- `TEX-69` فحص قابلية التكرار للخامات المولدة / Seamless-tile check for AI textures (ready)

### `TEX-68` — طبقات درجات للفرشاة الجافة / Tone layers for a dry-brush look (rotoscope)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تتبّع الرسمة نفسها على عدة مستويات رمادية وتعبئة كل مستوى بلونه الوسيط لالتقاط خطوط الفرشاة الجافة. / Trace the same drawing at several grey levels and fill each with its median colour to capture dry-brush streaks.

**متى:** عند تحويل رسمة إلى فيكتور مع الحفاظ على خطوط الفرشاة الجافة بعدة مستويات رمادية / when vectorising a drawing while keeping dry-brush streaks via several grey tone levels

**كيف:** Multi-threshold contour tracing, fill bottom-up even-odd; 3–6 levels (6 gives marginal gain for 1.4× points). vtracer/potracer do the tracing.

**المعاملات:** levels 3–6

**التثبيت:** pip install vtracer

**الوسوم:** فرشاة جافة · تتبع · dry brush · trace · vector · rotoscope · تحويل لفيكتور · روتوسكوب · مستويات رمادي · vectorize · vtracer

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:vtracer` ← python3 -c "import vtracer" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-68` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-atlas/skills/2414-animation/9357-rotoscope`

#### 7. قدرات قريبة في العائلة

- `TEX-66` أرضية حمم بعروق مضيئة / Veined lava floor shader (seen)
- `TEX-67` شيدر ضربات فرشاة / Stroke-based painterly shader (idea)
- `TEX-69` فحص قابلية التكرار للخامات المولدة / Seamless-tile check for AI textures (ready)
- `TEX-70` كتيب وصفات المواد للرسام / Material recipe sheet (flame, spray, steam, fur, atmosphere) (documented)

### `TEX-69` — فحص قابلية التكرار للخامات المولدة / Seamless-tile check for AI textures

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 (atlas item). |

**ما هي:** المولدات ضعيفة في الخامات المتكررة؛ قِس فرق الحواف واعرض 2×2 قبل استخدامها خلفية. / Generators tile badly: measure seam difference and preview 2×2 before using a texture as a background.

**متى:** قبل استخدام خامة مولدة بالذكاء الاصطناعي كخلفية متكررة: قياس فرق الحواف ومعاينة 2×2 / before using an AI-generated texture as a repeating background: measure seam difference and preview 2×2

**كيف:** Seam score = mean \|left−right\| + \|top−bottom\| edge columns; > 2 shows as grid lines → mirror-blend edges or tile manually; fit to drawn size (e.g. 1024 px, ≤ 250 KB), JPEG/WebP for pictures, PNG only for alpha.

**المعاملات:** seam > 2 visible; 1024 px; ≤ 250 KB

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تكرار · seamless · tile · ai texture · qa · خامة متكررة · فحص الجودة · حواف · tileable · seam check

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-69` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-atlas/skills/1511-homie/3889-art`

#### 7. قدرات قريبة في العائلة

- `TEX-67` شيدر ضربات فرشاة / Stroke-based painterly shader (idea)
- `TEX-68` طبقات درجات للفرشاة الجافة / Tone layers for a dry-brush look (rotoscope) (install)
- `TEX-70` كتيب وصفات المواد للرسام / Material recipe sheet (flame, spray, steam, fur, atmosphere) (documented)
- `TEX-71` تدرج شبكي وشبكة خطوط / Mesh-gradient + grid backgrounds (documented)

### `TEX-70` — كتيب وصفات المواد للرسام / Material recipe sheet (flame, spray, steam, fur, atmosphere)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** وصفات مكتوبة: لهب بطبقات جمع من الأحمر للأبيض مع توهج، رذاذ نقاط+تمويه، بخار سحابة screen، فرو أنابيب متوازية، والمسافة غلالة زرقاء. / Written recipes: flames as add layers red→white with glow; spray as dots + blur; steam as a screen cloud; fur as parallel tubes; distance as a blue screen veil.

**متى:** حين ترسم لهبًا أو رذاذًا أو بخارًا أو فروًا أو عمقًا جويًا في الرسام وتحتاج وصفة جاهزة / when painting flame, spray, steam, fur or atmospheric distance and you need a ready recipe

**كيف:** Follow references/drawing-guide.md §3; atmosphere = fill(rect, colour, .2, blur=30, mode="screen"); far edges blur 1–3.

**المعاملات:** veil .2 screen blur 30

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** وصفات · لهب · بخار · recipes · flame · steam · atmosphere · نار · رذاذ · فرو · spray · fur

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-70` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-studio/references/drawing-guide.md:62`

#### 7. قدرات قريبة في العائلة

- `TEX-68` طبقات درجات للفرشاة الجافة / Tone layers for a dry-brush look (rotoscope) (install)
- `TEX-69` فحص قابلية التكرار للخامات المولدة / Seamless-tile check for AI textures (ready)
- `TEX-71` تدرج شبكي وشبكة خطوط / Mesh-gradient + grid backgrounds (documented)
- `TEX-72` ست خلفيات نقشية متحركة / Basma animated pattern backgrounds (6 + gradient) (install)

### `TEX-71` — تدرج شبكي وشبكة خطوط / Mesh-gradient + grid backgrounds

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خلفيات جوية من تدرجين شعاعيين متراكبين وشبكة 1px خافتة وحبيبات 2% ضد التكسر، أو تدرج شبكي على GPU خلف الواجهة. / Two stacked radial gradients, a faint 1 px grid and 2% grain against banding — or a GPU mesh gradient behind crisp UI.

**متى:** عند الحاجة لخلفية جوية من تدرجين شعاعيين وشبكة خطوط خافتة وحبيبات ضد التكسر خلف الواجهة / for an atmospheric background of radial gradients, a faint line grid and grain against banding behind UI

**كيف:** radial-gradient(ellipse at 20% 80%, rgba(r,g,b,.3) 0, transparent 50%) + one at 80%/20% (.2); grid = two linear-gradients 1 px rgba(255,255,255,.03) every 50 px; animate centres slowly. GPU option: @paper-design/shaders-react MeshGradient (Apache-2.0) behind a z-index:1 UI with a static CSS fallback. A seek-driven 6-point Gaussian mesh (σ² .11 at 192×108, upscaled) runs in proofs/glass-luxury-logo.

**المعاملات:** radials .3/.2 → 50%; grid 50 px @ 3%; grain 2%; mesh #00F0FF/#7000FF/#000

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تدرج · mesh gradient · grid · background · aurora · خلفية متدرجة · تدرج شعاعي · شبكة خطوط · radial gradient · banding

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-71` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/animation-patterns.md`
- `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/references/shader-backed-ui.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/glass-luxury-logo/README.md`

#### 7. قدرات قريبة في العائلة

- `TEX-69` فحص قابلية التكرار للخامات المولدة / Seamless-tile check for AI textures (ready)
- `TEX-70` كتيب وصفات المواد للرسام / Material recipe sheet (flame, spray, steam, fur, atmosphere) (documented)
- `TEX-72` ست خلفيات نقشية متحركة / Basma animated pattern backgrounds (6 + gradient) (install)
- `TEX-73` شبكة خطوط قطرية منجرفة / Drifting diagonal line grid (ready)

### `TEX-72` — ست خلفيات نقشية متحركة / Basma animated pattern backgrounds (6 + gradient)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** aurora, grid, dots, waves, stars, rays + تدرج دوّار ولون ثابت، كلها تتجاوب مع الإيقاع. / aurora, grid, dots, waves, stars, rays plus a rotating gradient and solid — all beat-aware.

**متى:** حين تحتاج خلفية متحركة جاهزة تتجاوب مع الإيقاع: شفق أو شبكة أو نقاط أو أمواج أو نجوم أو أشعة / when you need a ready beat-reactive animated background: aurora, grid, dots, waves, stars or rays

**كيف:** drawPattern(): aurora = 4 screen-blended radial blobs on Lissajous paths (radius .5·max(W,H) + beat); grid 9% spacing drifting .35 sp/s + accent radial; dots 7% grid, size wave sin(d·14 − 2.2t); waves 6 sine bands amplitude 3.5% H; stars 140 twinkling + horizon glow; rays 14 wedges at .08 rad/s; gradient rotates .25 rad/s.

**المعاملات:** aurora\|grid\|dots\|waves\|stars\|rays\|gradient\|solid

**التثبيت:** cd app && npm install

**الوسوم:** خلفية · aurora · pattern · beat · basma · stars · rays · خلفية متحركة · شفق · إيقاع الموسيقى · animated background · beat sync

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-72` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `app/public/js/00_editor.js:2418`
- `app/public/js/00_editor.js:2443`
- `app/index.html:49`

#### 7. قدرات قريبة في العائلة

- `TEX-70` كتيب وصفات المواد للرسام / Material recipe sheet (flame, spray, steam, fur, atmosphere) (documented)
- `TEX-71` تدرج شبكي وشبكة خطوط / Mesh-gradient + grid backgrounds (documented)
- `TEX-73` شبكة خطوط قطرية منجرفة / Drifting diagonal line grid (ready)
- `TEX-74` شبكة نقطية تحريرية دقيقة / Fine dot-dash editorial grid (ready)

### `TEX-73` — شبكة خطوط قطرية منجرفة / Drifting diagonal line grid

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة خافتة من خطوط مائلة وأفقية تتمايل برفق فتعطي الخلفية الفارغة حياة. / A faint grid of slanted lines plus horizontals swaying gently — motion for an empty background.

**متى:** عند وجود خلفية فارغة تحتاج حركة هادئة: شبكة خطوط مائلة خافتة تتمايل برفق / when an empty background needs quiet motion: a faint slanted-line grid swaying gently

**كيف:** globalAlpha .13; spacing min(w,h)/12; slanted lines from (x + sin(t·.15)·25, 0) to (x + .15w, h); horizontals every spacing.

**المعاملات:** alpha .13; sway ±25 px at .15 rad/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شبكة · خطوط · grid · diagonal · background · خطوط مائلة · خلفية فاضية · حركة هادئة · subtle motion · canvas

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-73` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:66`

#### 7. قدرات قريبة في العائلة

- `TEX-71` تدرج شبكي وشبكة خطوط / Mesh-gradient + grid backgrounds (documented)
- `TEX-72` ست خلفيات نقشية متحركة / Basma animated pattern backgrounds (6 + gradient) (install)
- `TEX-74` شبكة نقطية تحريرية دقيقة / Fine dot-dash editorial grid (ready)
- `TEX-75` ورق مربعات وشبكة قياس / Graph-paper & graticule grids (seen)

### `TEX-74` — شبكة نقطية تحريرية دقيقة / Fine dot-dash editorial grid

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة ثابتة منخفضة التباين من شرطات صغيرة تعطي إحساس ورق تحريري بلا خطوط قطرية. / Stationary low-contrast grid of tiny dashes — an editorial paper feel with no diagonals.

**متى:** حين تريد خلفية تحريرية هادئة بشبكة شرطات دقيقة ثابتة منخفضة التباين / when you want a calm editorial background of a still, low-contrast grid of tiny dashes

**كيف:** Vertical dashes every .10w from .07w, step .051h, length 2·scale; horizontals the same; stroke at 55% alpha, width max(.5, .7·scale).

**المعاملات:** 10% × 5.1% spacing

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شبكة · تحريري · grid · editorial · dashes · شرطات · خلفية هادئة · ورق · dot grid · subtle background

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-74` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `fastify-motion-bro/web/editorial.js:43-46`

#### 7. قدرات قريبة في العائلة

- `TEX-72` ست خلفيات نقشية متحركة / Basma animated pattern backgrounds (6 + gradient) (install)
- `TEX-73` شبكة خطوط قطرية منجرفة / Drifting diagonal line grid (ready)
- `TEX-75` ورق مربعات وشبكة قياس / Graph-paper & graticule grids (seen)
- `TEX-76` جدار نص وبيانات خافت / Faint data/text wall (seen)

### `TEX-75` — ورق مربعات وشبكة قياس / Graph-paper & graticule grids

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة 1px داكنة ‎#1a1a1a‎ على ‎#090909‎ أو شبكة قياس 10×8 خضراء داكنة مع علامات صغرى وتعتيم. / 1 px #1a1a1a grid on #090909, or a 10×8 dark-green graticule with minor ticks and vignette.

**متى:** عند الحاجة لخلفية ورق مربعات داكنة أو شبكة قياس خضراء بعلامات صغرى وتعتيم / when you need a dark graph-paper grid or a dark-green graticule with minor ticks and vignette

**كيف:** Cell 40–48 px at 1280 w; grain .06; graticule #0f2a1a 1 px at .35 + ticks every 1/5 cell; radial vignette.

**المعاملات:** cell 40–48 px; grain .06; graticule opacity .35

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ورق مربعات · graph paper · graticule · grid · plotter · شبكة قياس · مربعات · خلفية داكنة · ticks · dark grid

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-75` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/plotter`
- `kosif-tool/styles/pm-rneayan-ea6129`

#### 7. قدرات قريبة في العائلة

- `TEX-73` شبكة خطوط قطرية منجرفة / Drifting diagonal line grid (ready)
- `TEX-74` شبكة نقطية تحريرية دقيقة / Fine dot-dash editorial grid (ready)
- `TEX-76` جدار نص وبيانات خافت / Faint data/text wall (seen)
- `TEX-77` أفق مدينة ليلي إجرائي / Procedural night skyline with lit windows (ready)

### `TEX-76` — جدار نص وبيانات خافت / Faint data/text wall

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خلفية داكنة مملوءة بأعمدة نص mono صغير 6–10% تنزلق ببطء تحت توهج بنفسجي، أو صفوف تنزلق باتجاهين خلف العنوان. / Dark ground filled with tiny mono text columns at 6–10% scrolling slowly under a violet glow, or rows scrolling in opposite directions behind a headline.

**متى:** حين تريد خلفية داكنة من نص أو بيانات خافتة تنزلق ببطء خلف العنوان / when you want a dark backdrop of faint scrolling text or data columns behind a headline

**كيف:** Mono 9 px at .08 scrolling 10 px/s; dense variant 40–80 px/s alternating direction per row; keep the headline on a solid band. Arabic walls: whole words per row, RTL scroll.

**المعاملات:** mono 9 px, opacity .08, 10 px/s (dense 40–80 px/s)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** جدار نص · بيانات · text wall · data texture · mono · خلفية نصوص · نص متحرك · تمرير · scrolling text · headline background

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-76` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-kmasiff-cc72cb`
- `kosif-tool/styles/pm-madebyjmayala-b9204d`
- `kosif-tool/styles/pm-souravbhar871-61f424`

#### 7. قدرات قريبة في العائلة

- `TEX-74` شبكة نقطية تحريرية دقيقة / Fine dot-dash editorial grid (ready)
- `TEX-75` ورق مربعات وشبكة قياس / Graph-paper & graticule grids (seen)
- `TEX-77` أفق مدينة ليلي إجرائي / Procedural night skyline with lit windows (ready)
- `TEX-78` انعكاسات الشارع المبتل / Wet street / floor reflections (proven)

### `TEX-77` — أفق مدينة ليلي إجرائي / Procedural night skyline with lit windows

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كتل مدينة بارتفاعات عشوائية ونوافذ مضاءة بلونين، تولد مرة واحدة من دالة hash حتمية. / City blocks of random heights with windows lit in two tones, generated once from a deterministic hash.

**متى:** عند الحاجة لأفق مدينة ليلي بأبراج ونوافذ مضاءة يتولد بحتمية دون صور / when you need a night city skyline with towers and lit windows generated deterministically

**كيف:** skyline(): 30 towers h 105–340, w 62–108; windows 3.5×6 lit if rnd > .43 (#4b99a2 / #9c976e, .15–.55); architecture(): 12 mid buildings 200 px wide, 23×28 windows lit if rnd > .37.

**المعاملات:** 30 towers; lit > .43

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مدينة · ليل · skyline · city · windows · procedural · أبراج · نوافذ مضيئة · مدينة ليلية · towers · night city

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-77` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:31`

#### 7. قدرات قريبة في العائلة

- `TEX-75` ورق مربعات وشبكة قياس / Graph-paper & graticule grids (seen)
- `TEX-76` جدار نص وبيانات خافت / Faint data/text wall (seen)
- `TEX-78` انعكاسات الشارع المبتل / Wet street / floor reflections (proven)
- `TEX-79` سبورة بآثار مسح / Whiteboard eraser-smudge texture (seen)

### `TEX-78` — انعكاسات الشارع المبتل / Wet street / floor reflections

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أرض مبتلة من بقع ضوء ملونة وفواصل رصف منظورية وخطوط لمعان أفقية متقطعة، ونسخة مرآة داكنة مموجة للبطل. / Wet ground of coloured light pools, perspective paving joints and broken horizontal glints, plus a dark rippled mirror of the hero.

**متى:** حين يحتاج المشهد أرضًا مبتلة بانعكاسات أضواء ملونة ونسخة مرآة مموجة للبطل / when a scene needs wet ground with coloured light reflections and a dark rippled mirror of the hero

**كيف:** Canvas: street gradient #17343f→#030b16, 85 broken reflection lines, hero drawn scale(1,−.25) at .085. Proof film version: mirrored 3 px slices with ripple, sharp layer in puddles + 16 px blurred layer on asphalt, Fresnel fade .9→.25 — rendered in proofs/neon-glow (13/13).

**المعاملات:** slices 3 px; blur 16 px; Fresnel .9→.25; mirror opacity .085

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** انعكاس · مبتل · wet floor · reflection · rain · neon · شارع · مطر · بركة ماء · puddles · street

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-78` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/README.md`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:109`

#### 7. قدرات قريبة في العائلة

- `TEX-76` جدار نص وبيانات خافت / Faint data/text wall (seen)
- `TEX-77` أفق مدينة ليلي إجرائي / Procedural night skyline with lit windows (ready)
- `TEX-79` سبورة بآثار مسح / Whiteboard eraser-smudge texture (seen)
- `TEX-80` حبيبات الطباشير / Chalk grain overlay (seen)

### `TEX-79` — سبورة بآثار مسح / Whiteboard eraser-smudge texture

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بضع ضربات رمادية فاتحة جدًا مموّهة على ‎#f6f6f4‎ مع ظل داخلي خفيف للإطار. / A few very light grey rounded strokes with a large blur over #f6f6f4, plus a subtle inner border shadow.

**متى:** عند رسم سبورة بيضاء بآثار مسح خفيفة وظل داخلي للإطار / when drawing a whiteboard with faint eraser smudges and a subtle inner border shadow

**كيف:** 4–6 seeded strokes, opacity .05–.1, blur 8–12 px, static; inner shadow inset 0 0 40px rgba(0,0,0,.06).

**المعاملات:** opacity .05–.1, blur 8–12 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سبورة · whiteboard · smudge · eraser · سبورة بيضاء · آثار مسح · ممحاة · board texture · inner shadow

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-79` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/whiteboard`

#### 7. قدرات قريبة في العائلة

- `TEX-77` أفق مدينة ليلي إجرائي / Procedural night skyline with lit windows (ready)
- `TEX-78` انعكاسات الشارع المبتل / Wet street / floor reflections (proven)
- `TEX-80` حبيبات الطباشير / Chalk grain overlay (seen)
- `TEX-81` تهشير داخل حدود الشكل / Clipped hatching / scribble fill (seen)

### `TEX-80` — حبيبات الطباشير / Chalk grain overlay

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طبقة SVG ثابتة بكامل السبورة: feTurbulence → feColorMatrix بلون السبورة، تصنع نمش الطباشير فوق الرسوم. / Static full-board SVG layer: feTurbulence → feColorMatrix into board-coloured specks over the drawings.

**متى:** حين تريد أن تظهر الرسوم على سبورة طباشير بنمش طباشير فوقها دون تشويه الخطوط / when drawings on a chalkboard should get chalk specks over them without distorting the strokes

**كيف:** baseFrequency ~.9, opacity ~.35; do not displace the strokes (feDisplacementMap ruins legibility).

**المعاملات:** freq ~.9, opacity ~.35

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** طباشير · chalk · chalkboard · grain · سبورة طباشير · طبشورة · نمش · blackboard · svg grain

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-80` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/chalkboard`

#### 7. قدرات قريبة في العائلة

- `TEX-78` انعكاسات الشارع المبتل / Wet street / floor reflections (proven)
- `TEX-79` سبورة بآثار مسح / Whiteboard eraser-smudge texture (seen)
- `TEX-81` تهشير داخل حدود الشكل / Clipped hatching / scribble fill (seen)
- `TEX-82` أرضيات ورقية وبلاط / Paper doodle ground & tile floor (seen)

### `TEX-81` — تهشير داخل حدود الشكل / Clipped hatching / scribble fill

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مسار متعرج قطري يغطي الشكل ويُرسم بتقدم الشرطة، مقصوص بحدود الشكل — تلوين ماركر أو طباشير. / A diagonal zigzag over the shape bbox drawn by dash progress and clipped to the shape — marker or chalk fill.

**متى:** عند تلوين شكل بخطوط متعرجة كالماركر أو الطباشير تُرسم تدريجيًا داخل حدوده / when filling a shape with a zigzag marker or chalk scribble drawn on progressively inside its bounds

**كيف:** zigzag spacing 10–12 px at 60°, stroke-dasharray progress, clipPath = shape, opacity ~.55; chalky robe variant: short lighter diagonal hatches 6–8 px at .3.

**المعاملات:** spacing 10–12 px, 60°, .55 (chalk 6–8 px, .3)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تهشير · hatching · scribble · marker · fill · تلوين يدوي · ماركر · شخبطة · draw-on · zigzag

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-81` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/whiteboard`
- `kosif-tool/styles/doodle`

#### 7. قدرات قريبة في العائلة

- `TEX-79` سبورة بآثار مسح / Whiteboard eraser-smudge texture (seen)
- `TEX-80` حبيبات الطباشير / Chalk grain overlay (seen)
- `TEX-82` أرضيات ورقية وبلاط / Paper doodle ground & tile floor (seen)
- `TEX-83` مثال الحبيبات الدافئة / warm-grain example project (HyperFrames) (install)

### `TEX-82` — أرضيات ورقية وبلاط / Paper doodle ground & tile floor

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ورق غائم بخط أرض مرسوم باليد، أو بلاط بكسل متكرر 32px — أبسط أرضية تعطي المكان هوية. / Cloudy paper with a hand-drawn baseline, or a repeating 32 px pixel tile floor.

**متى:** حين يحتاج المشهد أرضية بسيطة: ورق غائم بخط أرض مرسوم باليد أو بلاط بكسل متكرر / when a scene needs a simple ground: cloudy paper with a hand-drawn baseline or a repeating pixel tile floor

**كيف:** Paper: low-frequency noise multiply + wobbly baseline path; tile: CanvasPattern of a 32 px tile with imageSmoothingEnabled=false.

**المعاملات:** tile 32 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أرضية · بلاط · ground · tile · paper · pixel · أرض · خط الأرض · بكسل آرت · floor · baseline

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-82` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/styles/pm-ajith-io-ea7f2d`
- `kosif-tool/styles/pm-aisongman-71ffac`

#### 7. قدرات قريبة في العائلة

- `TEX-80` حبيبات الطباشير / Chalk grain overlay (seen)
- `TEX-81` تهشير داخل حدود الشكل / Clipped hatching / scribble fill (seen)
- `TEX-83` مثال الحبيبات الدافئة / warm-grain example project (HyperFrames) (install)
- `TEX-84` عائلة مواد مطفية واحدة / One matte material family (documented)

### `TEX-83` — مثال الحبيبات الدافئة / warm-grain example project (HyperFrames)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0. |

**ما هي:** مشروع كريمي ‎#f5f0e0‎ بخامة حبيبات وخط Outfit لمدة 10 ث — مرجع لوحة وخط. / Cream #f5f0e0 starter with grain texture and Outfit, 10 s — a palette/type reference.

**متى:** عند البحث عن مرجع لوحة ألوان وخط بأسلوب كريمي دافئ بحبيبات لمشروع HyperFrames / when looking for a warm cream grain palette and type reference for a HyperFrames project

**كيف:** npx hyperframes init --example warm-grain; the local copy lacks its sub-compositions (captions/graphics/intro), so use it as a style reference only.

**المعاملات:** 1920×1080; 10 s

**التثبيت:** npx hyperframes init --example warm-grain

**الوسوم:** دافئ · حبيبات · warm · grain · starter · hyperframes · لوحة ألوان · خط · كريمي · palette · outfit font

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-83` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-one/vendor/hyperframes/registry/examples/warm-grain/index.html`

#### 7. قدرات قريبة في العائلة

- `TEX-81` تهشير داخل حدود الشكل / Clipped hatching / scribble fill (seen)
- `TEX-82` أرضيات ورقية وبلاط / Paper doodle ground & tile floor (seen)
- `TEX-84` عائلة مواد مطفية واحدة / One matte material family (documented)
- `TEX-85` وصفات PBR سريعة / Quick PBR recipes (Three.js) (documented)

### `TEX-84` — عائلة مواد مطفية واحدة / One matte material family

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثبّت عائلة مادة واحدة: مطفي للصلصال واللوبولي، واللمعان للمنتج البطل فقط. / Keep one material family: matte for clay and low-poly, gloss reserved for hero products.

**متى:** حين تبني مشهدًا ثلاثي الأبعاد صلصاليًا أو لوبولي وتريد خامات مطفية موحدة مع لمعان للمنتج البطل فقط / when building a clay or low-poly 3D scene with one matte material family, gloss only for the hero product

**كيف:** MeshStandardMaterial roughness in the matte range; one hero gloss at most.

**المعاملات:** roughness .6–.9; sample 0x7ee8d2 roughness .7

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مطفي · matte · material · three.js · rule · لو بولي · خامة موحدة · صلصال · low poly · roughness

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-84` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-tool/playbooks/3d.md:16`
- `kosif-tool/playbooks/3d.md:59`

#### 7. قدرات قريبة في العائلة

- `TEX-82` أرضيات ورقية وبلاط / Paper doodle ground & tile floor (seen)
- `TEX-83` مثال الحبيبات الدافئة / warm-grain example project (HyperFrames) (install)
- `TEX-85` وصفات PBR سريعة / Quick PBR recipes (Three.js) (documented)
- `TEX-86` خامة القطيفة المحشوة / Plush felt material (velvet sheen + fibre) (ready)

### `TEX-85` — وصفات PBR سريعة / Quick PBR recipes (Three.js)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إعدادات سريعة: معدن لامع metalness .8 roughness .2، وأجزاء ذاتية الإضاءة بـ emissive. / Shiny metal metalness .8 / roughness .2; self-lit parts via emissive + emissiveIntensity.

**متى:** عند الحاجة لإعداد سريع لمعدن لامع أو أجزاء مضيئة ذاتيًا يلتقطها التوهج في three.js / when you need quick settings for shiny metal or self-lit parts that bloom catches in three.js

**كيف:** MeshStandardMaterial/MeshPhysicalMaterial; metal .8–.85 / rough .15–.2; emissiveIntensity .8 so bloom catches it.

**المعاملات:** metalness .8–.85, roughness .15–.2, emissiveIntensity .8

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** PBR · معدن · metal · emissive · three.js · معدن لامع · إضاءة ذاتية · توهج · shiny metal · bloom

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-85` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/animation_craft.md`
- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:132`

#### 7. قدرات قريبة في العائلة

- `TEX-83` مثال الحبيبات الدافئة / warm-grain example project (HyperFrames) (install)
- `TEX-84` عائلة مواد مطفية واحدة / One matte material family (documented)
- `TEX-86` خامة القطيفة المحشوة / Plush felt material (velvet sheen + fibre) (ready)
- `TEX-87` لمعان clearcoat للعين والأنف / Glossy clearcoat + eye with catch-lights (ready)

### `TEX-86` — خامة القطيفة المحشوة / Plush felt material (velvet sheen + fibre)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مادة فيزيائية بألوان رؤوس، لمعان مخملي، حافة زغب بلون القماش نفسه وضوضاء ألياف بفضاء الجسم بلا UV. / Vertex-coloured physical material with velvet sheen, a fuzz rim in the fabric colour and object-space fibre noise — no UVs.

**متى:** حين تريد شخصية محشوة أو دمية قماشية بلمعان مخملي وزغب وألياف دون UV / when you want a plush or felt character with velvet sheen, a fuzz rim and fibre noise, no UVs

**كيف:** K3S.plushMaterial({fuzz, fibre, fibreScale, sheen, sheenRoughness, sheenColor, fuzzTint, roughness}) from shape-kit.js on the three-kit bundle.

**المعاملات:** roughness .82; sheen 1.0; sheenRoughness .42; sheenColor #fff4f6; fuzz .38; fibre .22; fibreScale 520/m; rim power 2.2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قطيفة · plush · felt · velvet · sheen · character · دمية · مخمل · لعبة محشوة · plush toy · fuzz

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-86` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-studio/motion/kit/shape-kit.js:286`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:286`
- `100-superskills/skills/kosif-montage-motion/references/shape-kit.md`

#### 7. قدرات قريبة في العائلة

- `TEX-84` عائلة مواد مطفية واحدة / One matte material family (documented)
- `TEX-85` وصفات PBR سريعة / Quick PBR recipes (Three.js) (documented)
- `TEX-87` لمعان clearcoat للعين والأنف / Glossy clearcoat + eye with catch-lights (ready)
- `TEX-88` طقم مواد المختبر / Lab material set (plush/gloss/leather/metal) (ready)

### `TEX-87` — لمعان clearcoat للعين والأنف / Glossy clearcoat + eye with catch-lights

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مادة داكنة لامعة للعيون والأنوف، وعين بصلبة وقزحية وبؤبؤ وقرنية ولمعتين. / Dark glossy clearcoat for eyes/noses; eye() with sclera/iris/pupil/cornea and two catch-lights.

**متى:** عند صنع عيون وأنوف لامعة لشخصية ثلاثية الأبعاد بقزحية وبؤبؤ ولمعتي ضوء / when making glossy eyes and noses for a 3D character with iris, pupil and two catch-lights

**كيف:** K3S.glossMaterial(color,{roughness, env}); K3S.eye({r, tall}); K3S.tube(points, r, colour) for mouths/stitches; makeEye in lab-kit.

**المعاملات:** #15100f; roughness .08; clearcoat 1, clearcoatRoughness .04; ior 1.5; envMapIntensity 1.6; eye tall 1.12, catch-lights upper-outer

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عين · لمعان · eye · clearcoat · gloss · character · عيون · أنف · قزحية · catch-lights · iris

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-87` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-studio/motion/kit/shape-kit.js:311`
- `kosif-one/tools/kosif-studio/motion/kit/shape-kit.js:316`

#### 7. قدرات قريبة في العائلة

- `TEX-85` وصفات PBR سريعة / Quick PBR recipes (Three.js) (documented)
- `TEX-86` خامة القطيفة المحشوة / Plush felt material (velvet sheen + fibre) (ready)
- `TEX-88` طقم مواد المختبر / Lab material set (plush/gloss/leather/metal) (ready)
- `TEX-89` فرو بالطبقات / Shell fur (ready)

### `TEX-88` — طقم مواد المختبر / Lab material set (plush/gloss/leather/metal)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مواد سريعة لمشاهد مختبر المنتج: قطيفة، لامع، جلد، معدن. / Quick materials for product-lab scenes: plush, gloss, leather, metal.

**متى:** حين تحتاج مواد سريعة لمشهد مختبر منتج: قطيفة أو لامع أو جلد أو معدن / when you need quick materials for a product-lab scene: plush, gloss, leather or metal

**كيف:** K3.plushMaterial(c), K3.glossMaterial(c,{roughness}), K3.leatherMaterial(c), K3.metalMaterial(c) from lab-kit.js.

**المعاملات:** plush r .95; gloss clearcoat 1 r .08; leather #15171a r .55 m .05; metal #d8dde3 r .25 m .95

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مواد · جلد · معدن · leather · metal · materials · product · منتج · قطيفة · لامع · plush · gloss

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-88` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-studio/motion/kit/lab-kit.js:49`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:49`

#### 7. قدرات قريبة في العائلة

- `TEX-86` خامة القطيفة المحشوة / Plush felt material (velvet sheen + fibre) (ready)
- `TEX-87` لمعان clearcoat للعين والأنف / Glossy clearcoat + eye with catch-lights (ready)
- `TEX-89` فرو بالطبقات / Shell fur (ready)
- `TEX-90` بقع لونية على المجسم / Colour paint stamps on SDF (ready)

### `TEX-89` — فرو بالطبقات / Shell fur

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نسخ طبقية من الشبكة مدفوعة على العموديات بخرائط نقاط ألفا، جذور أغمق وجاذبية على الطبقات الخارجية. / Layered shells pushed along normals with dot alpha maps; darker roots and gravity sag on outer shells.

**متى:** عند إضافة فرو أو شعر لحيوان أو شخصية ثلاثية الأبعاد بطبقات متراكبة / when adding fur or hair to a 3D animal or character using stacked shell layers

**كيف:** K3.makeFur(mesh,{layers, length, repeat, color, rootShade, gravity, density, seed}) (lab-kit.js); recolour live: shell.material.color.lerp(target).multiplyScalar(.55 + .45·(i+1)/n). Projects: rabbit 7 layers .09, lion 8 layers .07, mane 10 shells .18 m.

**المعاملات:** layers 10 (8–12 at 540p, 16 at 1080p); length .12; repeat 14; rootShade .72; gravity .35; alphaTest .1→.78; hair texture 256 px density .55

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** فرو · fur · shell · hair · animal · three.js · شعر · حيوانات · زغب · furry · mane

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-89` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-studio/motion/kit/lab-kit.js:28`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/src/main.js:14`

#### 7. قدرات قريبة في العائلة

- `TEX-87` لمعان clearcoat للعين والأنف / Glossy clearcoat + eye with catch-lights (ready)
- `TEX-88` طقم مواد المختبر / Lab material set (plush/gloss/leather/metal) (ready)
- `TEX-90` بقع لونية على المجسم / Colour paint stamps on SDF (ready)
- `TEX-91` شفافية الأشعة السينية للدمية / Plush X-ray during analysis (ready)

### `TEX-90` — بقع لونية على المجسم / Colour paint stamps on SDF

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بقع لونية كروية/بيضاوية ناعمة (خدود، بطن، وسائد الكف) بلا هندسة إضافية. / Soft spherical/ellipsoidal colour stamps (blush, belly patch, paw pads) with no extra geometry.

**متى:** حين تريد إضافة خدود وردية أو بقعة بطن أو وسائد كف لشخصية دون هندسة إضافية / when adding blush cheeks, a belly patch or paw pads to a character without extra geometry

**كيف:** S.paint(c, r, colour, {soft, radii, amount, rot}).

**المعاملات:** soft default r·.5; amount 1; blush r .015 soft .009 amount .8

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** طلاء · paint · blush · sdf · character · خدود · بقع لون · تلوين المجسم · paw pads · belly patch

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-90` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-studio/motion/kit/shape-kit.js:98`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:98`

#### 7. قدرات قريبة في العائلة

- `TEX-88` طقم مواد المختبر / Lab material set (plush/gloss/leather/metal) (ready)
- `TEX-89` فرو بالطبقات / Shell fur (ready)
- `TEX-91` شفافية الأشعة السينية للدمية / Plush X-ray during analysis (ready)
- `TEX-92` حصى وقصب / Pebbles & reed blades (ready)

### `TEX-91` — شفافية الأشعة السينية للدمية / Plush X-ray during analysis

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الدمية الناعمة تصير شبه شفافة أثناء تحليل بنيتها ثم تعود معتمة. / The plush character turns semi-transparent while its internal structure is analysed, then returns opaque.

**متى:** عند كشف البنية الداخلية لدمية أثناء تحليلها بجعلها شبه شفافة ثم إعادتها معتمة / when revealing a plush character's internal structure by making it semi-transparent, then opaque again

**كيف:** All materials transparent; opacity = base·(1 − .66·xr), depthWrite only when > .98; xr = smooth(joint−.05, joint+.3)·(1 − smooth(rank+.05, rank+.42)).

**المعاملات:** max fade .66

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أشعة سينية · x-ray · transparent · analysis · plush · شفافية · هيكل داخلي · دمية · see-through · opacity

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-91` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:53`

#### 7. قدرات قريبة في العائلة

- `TEX-89` فرو بالطبقات / Shell fur (ready)
- `TEX-90` بقع لونية على المجسم / Colour paint stamps on SDF (ready)
- `TEX-92` حصى وقصب / Pebbles & reed blades (ready)
- `TEX-93` قاع بركة بانكسارات ضوئية / Pond bed terrain with caustics (install)

### `TEX-92` — حصى وقصب / Pebbles & reed blades

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حصى نهري مُنسَّخ من إيكوساهيدرا مشوهة بالضوضاء في عناقيد بأربع عائلات لون، وأعواد قصب مستدقة تتمايل. / Instanced water-worn stones from noise-deformed icosahedra clumped in drifts (4 HSL colour families), plus tapered swaying reed blades.

**متى:** حين تحتاج حصى نهريًا متناثرًا في عناقيد وأعواد قصب تتمايل في مشهد ثلاثي الأبعاد / when you need river pebbles scattered in clumps and swaying reed blades in a 3D scene

**كيف:** K3.makePebbles({n, region, accept, height, size, flat, clump, seed}); K3.makeBlades({n, region, tall, width, seed}).

**المعاملات:** pebbles n 2400, size .06 m (×.4–2.8), flat .5; blades n 1500, tall .9 m

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حصى · قصب · pebbles · reeds · instanced · nature · حجارة · ضفة نهر · طبيعة · river stones · scatter

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-92` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `kosif-studio/motion/kit/three-kit.js:724`
- `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:746`

#### 7. قدرات قريبة في العائلة

- `TEX-90` بقع لونية على المجسم / Colour paint stamps on SDF (ready)
- `TEX-91` شفافية الأشعة السينية للدمية / Plush X-ray during analysis (ready)
- `TEX-93` قاع بركة بانكسارات ضوئية / Pond bed terrain with caustics (install)
- `TEX-94` أسفلت مبلل وطلاء عاكس / Wet asphalt + retro-reflective road paint (install)

### `TEX-93` — قاع بركة بانكسارات ضوئية / Pond bed terrain with caustics

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قاع بركة ملوّن بالعمق والميل (طمي، رمل، طين، طحلب) مع كاوستكس متحركة تمتص الأحمر مع العمق. / Pond bowl coloured by depth and slope (silt, sand, mud, moss) with animated caustics absorbing red with depth.

**متى:** عند بناء قاع بركة بالطمي والرمل والطين والطحالب مع انكسارات ضوء متحركة / when building a pond bed of silt, sand, mud and moss with animated caustics

**كيف:** makeTerrain({size 44, seg 320, albedoRepeat 10, normalRepeat 22, normalScale .8, texSize 512}); addCaustics(material,{time, level 0, strength 3.2, scale 5.5, absorb [1.35,.42,1.0], sun}); pebbles 2600 × .038 + rim 170 × .24. The demo project loads assets/main.bundle.js, which is not built in this checkout — install esbuild and bundle first; the kit itself (three-kit.bundle.js) is prebuilt.

**المعاملات:** silt #4a4532 sand #857a5c mud #2e2a20 moss #3d5a26 #5f7a33

**التثبيت:** cd 100-superskills/skills/kosif-montage-motion/scripts && npm install three@0.186.1 esbuild && python3 motion.py bundle koi_pond

**الوسوم:** بركة · كاوستكس · caustics · pond · terrain · water · قاع الماء · ضوء تحت الماء · طحلب · underwater light · pond bed

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:esbuild` ← npm ls esbuild أو وجود node_modules/esbuild
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-93` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:9`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:39`

#### 7. قدرات قريبة في العائلة

- `TEX-91` شفافية الأشعة السينية للدمية / Plush X-ray during analysis (ready)
- `TEX-92` حصى وقصب / Pebbles & reed blades (ready)
- `TEX-94` أسفلت مبلل وطلاء عاكس / Wet asphalt + retro-reflective road paint (install)
- `TEX-X01` حبيبات فيلم صحيحة / Film grain done right (post-mortem) (documented)

### `TEX-94` — أسفلت مبلل وطلاء عاكس / Wet asphalt + retro-reflective road paint

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أسفلت ليلي قليل الخشونة يلمع مع المصابيح، وشرطات وسط وخطوط حواف تتوهج بخفة. / Slightly wet low-roughness asphalt glinting with lamps; centre dashes and edge lines glowing faintly.

**متى:** حين تحتاج طريقًا ليليًا بأسفلت مبلل يلمع مع المصابيح وخطوط طلاء تتوهج بخفة / when you need a night road with wet asphalt glinting under lamps and faintly glowing lane paint

**كيف:** Road ribbon from CatmullRom (800 segments, 8 m wide) MeshStandard 0x15161a roughness .32; paint 0xe8e4da emissive 0x6a6658 ×.6; 340 instanced dashes .16×3 m every 12 m; edge lines .14 m at ±(4−.35) m. The demo project loads assets/main.bundle.js, which is not built in this checkout — install esbuild and bundle first; the kit itself (three-kit.bundle.js) is prebuilt.

**المعاملات:** roughness .32; emissive ×.6; dash every 12 m

**التثبيت:** cd 100-superskills/skills/kosif-montage-motion/scripts && npm install three@0.186.1 esbuild && python3 motion.py bundle blue_hour

**الوسوم:** أسفلت · طريق · asphalt · road · wet · night · شارع · خطوط الطريق · مصابيح · lane markings · street

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:esbuild` ← npm ls esbuild أو وجود node_modules/esbuild
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-94` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:64`

#### 7. قدرات قريبة في العائلة

- `TEX-92` حصى وقصب / Pebbles & reed blades (ready)
- `TEX-93` قاع بركة بانكسارات ضوئية / Pond bed terrain with caustics (install)
- `TEX-X01` حبيبات فيلم صحيحة / Film grain done right (post-mortem) (documented)
- `TEX-X02` سلسلة مرور أرشيفية / Archival post chain order (WebGL) (documented)

### `TEX-X01` — حبيبات فيلم صحيحة / Film grain done right (post-mortem)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | unknown (reference only) |

**ما هي:** حبيبات بدت «ملصقًا ثابتًا» رغم أنها تتغير كل إطار؛ التشخيص والإصلاح يعلّمان كيف تُصنع حبيبات تعيش داخل الصورة. — Grain that looked like a static sticker although it changed every frame; the diagnosis and fix show how to make grain that lives inside the picture.

**متى:** مظهر أرشيفي أو سينمائي، أو أي حبيبات متحركة — an archival or filmic look, or any animated grain.

**كيف:** Causes found: coarse 2.4 px clumps with 60 % of the energy in deep shadows/highlights; a clump layer that was ONE noise field translated ≈ (32, 18) px per frame, so consecutive frames correlated 0.52–0.54 (a pattern sliding over the picture) while per-frame residual correlation was only ~0.035; grain in screen coordinates while gate weave moved the picture (grain detached); sine-hash 1 px grain losing GPU precision for large arguments (patterned, changed character at each cut); frame index modulo 997 repeating the sequence at 39.9 s. Fix: sparse-convolution noise (one Gaussian blob per cell, 3×3 neighbourhood, kernel e^−4.5 at one cell so no seams), two octaves (1.15 px fine, 2.6 px coarse ≈ 10 % of variance), hashed by (cell, frame) with sine-free hashes, sampled at the weaved film position, weighted to mid-tones, normalised std. Policy: UI/SaaS films keep grain static and ≤ 0.02–0.04 luma (or none); documentary grain must move, but in film coordinates.

**المعاملات:** fine 1.15 px + coarse 2.6 px (~10 %); no modulo index; film coordinates

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** film grain · noise · archival · webgl · حبيبات · ضوضاء · أرشيفي

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-X01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `owner-upload:Claude_edit_skill_1/Claude edit skill/implementation/browser-reference/picture.js`

#### 7. قدرات قريبة في العائلة

- `TEX-93` قاع بركة بانكسارات ضوئية / Pond bed terrain with caustics (install)
- `TEX-94` أسفلت مبلل وطلاء عاكس / Wet asphalt + retro-reflective road paint (install)
- `TEX-X02` سلسلة مرور أرشيفية / Archival post chain order (WebGL) (documented)

### `TEX-X02` — سلسلة مرور أرشيفية / Archival post chain order (WebGL)

| الحقل | القيمة |
|---|---|
| العائلة | `texture-material` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/texture-material.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | unknown (reference only) |

**ما هي:** ترتيب مراحل المظهر الأرشيفي مهم: الاهتزاز والنعومة قبل التوهج، والتدريج ثم عمر الطبعة، ثم التعتيم، ثم الحبيبات بإحداثيات الفيلم، ثم الغبار والوميض. — The order of archival-look stages matters: weave and softness before bloom, grade then print age, then vignette, then grain in film coordinates, then dust and flash.

**متى:** مونتاج وثائقي أو أرشيفي بالأبيض والأسود أو بلون فيلمي — a documentary or archival edit in B&W or film colour.

**كيف:** compose → bright-pass + 4× downsample → separable 13-tap Gaussian (σ ≈ 3.2 texels at ¼ res ≈ 13 px full res) → main pass: gate weave (≈ 1 px slow drift + per-frame jitter; more for older prints) → lens/emulsion softness 0.8 px (≤ 1.4 old print) → bloom/halation → grade (doc \| light neutral B&W \| film) → print and archive age (low-frequency density breathing, value noise on a 3-cell lattice) → vignette → grain in film coordinates (TEX-X01) → dust and scratches → flash. Keep one texture-orientation convention across framebuffer passes (GL bottom-up vs top-down uploads).

**المعاملات:** blur σ ≈ 3.2 texels @ ¼; weave ≈ 1 px; softness 0.8–1.4 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** archival · gate weave · halation · post chain · أرشيفي · سلسلة معالجة

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:TEX-X02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cat-fur-upgrade`.
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

- `owner-upload:Claude_edit_skill_1/Claude edit skill/implementation/browser-reference/picture.js`

#### 7. قدرات قريبة في العائلة

- `TEX-94` أسفلت مبلل وطلاء عاكس / Wet asphalt + retro-reflective road paint (install)
- `TEX-X01` حبيبات فيلم صحيحة / Film grain done right (post-mortem) (documented)

