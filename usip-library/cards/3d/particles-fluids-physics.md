# `particles-fluids-physics` — الثري دي والمحاكاة والرندر (77 بطاقة)

> مكتبة بروتوكول USIP v5.6 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/particles-fluids-physics.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/3d.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`PART-01` ضجيج حتمي بالهاش وmulberry32](#part-01--ضجيج-حتمي-بالهاش-وmulberry32--deterministic-hash--seeded-rng)
- [`PART-02` الجسيم دالة للزمن لا حالة](#part-02--الجسيم-دالة-للزمن-لا-حالة--closed-form-particles-state-free-seek)
- [`PART-03` الجسيم يعني شيئًا](#part-03--الجسيم-يعني-شيئًا--particle-meaning-rule)
- [`PART-04` ميزانية الأحجام والألوان والعدد](#part-04--ميزانية-الأحجام-والألوان-والعدد--size--colour--count-budget)
- [`PART-05` المؤثر على إطار التلامس](#part-05--المؤثر-على-إطار-التلامس--impact-on-the-contact-frame)
- [`PART-06` انفجار ببذرة وجاذبية](#part-06--انفجار-ببذرة-وجاذبية--seeded-analytic-burst)
- [`PART-07` وصفة انفجار الكشف](#part-07--وصفة-انفجار-الكشف--reveal-burst-recipe)
- [`PART-08` قصاصات احتفال تنقلب](#part-08--قصاصات-احتفال-تنقلب--confetti-burst--rain-with-3d-flip)
- [`PART-09` انفجارات HyperFrames الجاهزة](#part-09--انفجارات-hyperframes-الجاهزة--hyperframes-burst-primitives-particle-burst-radial-burst-lines)
- [`PART-10` شرطات وشرارات الاصطدام](#part-10--شرطات-وشرارات-الاصطدام--radial-dash-burst--impact-spark-lines)
- [`PART-11` تحطم إلى مربعات أو شظايا](#part-11--تحطم-إلى-مربعات-أو-شظايا--shatter-to-squares--shards--ring-shards)
- [`PART-12` انفجار سحابة صور أو بطاقات](#part-12--انفجار-سحابة-صور-أو-بطاقات--image-card-burst-cloud)
- [`PART-13` انفجار فتح إنجاز ونجوم ذهبية](#part-13--انفجار-فتح-إنجاز-ونجوم-ذهبية--achievement-unlock-star-burst)
- [`PART-14` مؤثرات بكسل بخطوات اللوحة](#part-14--مؤثرات-بكسل-بخطوات-اللوحة--pixel-vfx-by-palette-step-fades)
- [`PART-15` جسيمات تتجمع كلمة عربية](#part-15--جسيمات-تتجمع-كلمة-عربية--particles-gather-into-a-shaped-arabic-word)
- [`PART-16` تفكك النص إلى جسيمات أو جمر](#part-16--تفكك-النص-إلى-جسيمات-أو-جمر--text-dissolve--disintegrate-to-embers)
- [`PART-17` أيقونة أو شعار يتكون من سحابة نقاط](#part-17--أيقونة-أو-شعار-يتكون-من-سحابة-نقاط--icon--logo-coalescing-from-a-point-cloud)
- [`PART-18` جسيمات تتحول إلى بيانات أو واجهة](#part-18--جسيمات-تتحول-إلى-بيانات-أو-واجهة--particles--chart--grid--ui)
- [`PART-19` كشف صورة بالجسيمات](#part-19--كشف-صورة-بالجسيمات--particle-image-reveal-hyperframes)
- [`PART-20` سحابة تتحول من حلقة إلى كرة](#part-20--سحابة-تتحول-من-حلقة-إلى-كرة--point-cloud-shape-morph-torus--sphere-helix--strands)
- [`PART-21` من فيديو إلى جسم جسيمي](#part-21--من-فيديو-إلى-جسم-جسيمي--mocap-performer-silhouette--particle-body)
- [`PART-22` صندوق الضوضاء](#part-22--صندوق-الضوضاء--noise-toolbox-perlin--simplex--curl--fbm--warp)
- [`PART-23` حقل curl تحليلي خالٍ من التباعد](#part-23--حقل-curl-تحليلي-خالٍ-من-التباعد--analytic-curl-field-stream-function)
- [`PART-24` خطوط حقل التدفق](#part-24--خطوط-حقل-التدفق--flow-field-streak-lines)
- [`PART-25` سرير تدفق ولزوجة على الإيقاع](#part-25--سرير-تدفق-ولزوجة-على-الإيقاع--beat-anchored-flow-field-bed--gooey-metaball-hyperframes)
- [`PART-26` تدفق الجسيمات على المسارات](#part-26--تدفق-الجسيمات-على-المسارات--particle-flow-along-routes--network-edges)
- [`PART-27` طبقات التدفق في deck.gl](#part-27--طبقات-التدفق-في-deckgl--deckgl-flow-layers-trips-arcs-hex)
- [`PART-28` حقل حراري يُلطخ بالإصبع](#part-28--حقل-حراري-يُلطخ-بالإصبع--thermal-finger-trail-smear-field)
- [`PART-29` شبكة نقاط تتأثر بجاذب](#part-29--شبكة-نقاط-تتأثر-بجاذب--dot-grid-displacement-around-an-attractor)
- [`PART-30` حزم موجات وشرائط خطوط](#part-30--حزم-موجات-وشرائط-خطوط--noisy-multi-trace-waveform--line-ribbon-waves)
- [`PART-31` آثار الحركة والضوء](#part-31--آثار-الحركة-والضوء--motion-trails-from-time-sampled-history)
- [`PART-32` مطر motion-kit](#part-32--مطر-motion-kit--motionrain-seeded-svgdom-rain)
- [`PART-33` بخار motion-kit](#part-33--بخار-motion-kit--motionvapour-steam-puffs)
- [`PART-34` تلألؤ ونجوم](#part-34--تلألؤ-ونجوم--motionsparkle--star-twinkle)
- [`PART-35` غبار طافٍ وحقل عمق](#part-35--غبار-طافٍ-وحقل-عمق--drifting-dust-motes--depth-field)
- [`PART-36` أنظمة Basma الخمسة](#part-36--أنظمة-basma-الخمسة--basma-particle-overlays-dust-bokeh-sparks-snow-confetti)
- [`PART-37` مطر بطبقتين وبرك ورذاذ](#part-37--مطر-بطبقتين-وبرك-ورذاذ--two-layer-parallax-rain-puddle-ripples--splashes)
- [`PART-38` مطر الرسام بطبقات وضوء نار](#part-38--مطر-الرسام-بطبقات-وضوء-نار--painted-rain-with-exposure-smear-studio)
- [`PART-39` مطر وضباب ومطر الغيمة](#part-39--مطر-وضباب-ومطر-الغيمة--rain--fog-bands-cloud-rain-with-splash-rings)
- [`PART-40` جسيمات موسمية وبتلات](#part-40--جسيمات-موسمية-وبتلات--seasonal-particles--falling-petals)
- [`PART-41` ثلج وحقل نجوم HyperFrames](#part-41--ثلج-وحقل-نجوم-hyperframes--hyperframes-snow--starfield-blocks)
- [`PART-42` ثلج وجمر على المعالج الرسومي](#part-42--ثلج-وجمر-على-المعالج-الرسومي--gpu-snow--ember-point-sprites)
- [`PART-43` ذرات صاعدة وحلقات الركلة](#part-43--ذرات-صاعدة-وحلقات-الركلة--rising-motes--kick-rings-verse)
- [`PART-44` هالة شعاعية وجسيمات صاعدة](#part-44--هالة-شعاعية-وجسيمات-صاعدة--radial-aura--drifting-particle-canvas)
- [`PART-45` خلفيات هادئة حلقية](#part-45--خلفيات-هادئة-حلقية--ambient-background-loops-mg-111113114)
- [`PART-46` كرة جسيمات فيبوناتشي](#part-46--كرة-جسيمات-فيبوناتشي--fibonacci-particle-sphere)
- [`PART-47` مجرة حلزونية](#part-47--مجرة-حلزونية--spiral-galaxy-differential-rotation)
- [`PART-48` قفزة فضائية وخطوط سرعة](#part-48--قفزة-فضائية-وخطوط-سرعة--hyperspace-warp-starfield)
- [`PART-49` حلقة جسيمات وكوكبة](#part-49--حلقة-جسيمات-وكوكبة--particle-torus--constellation)
- [`PART-50` نقاط مضيئة ثلاثية جمعية](#part-50--نقاط-مضيئة-ثلاثية-جمعية--additive-glowing-point-sprites-threejs)
- [`PART-51` جسيمات GPU بمئة ألف](#part-51--جسيمات-gpu-بمئة-ألف--gpu-particles-fbo-ping-pong--tsl-compute-100k)
- [`PART-52` دوامة وشفط وشظايا طافية](#part-52--دوامة-وشفط-وشظايا-طافية--particle-vortex-suck-in--floating-shards)
- [`PART-53` نفث النار بطبقات](#part-53--نفث-النار-بطبقات--layered-fire-breath)
- [`PART-54` جمر ودخان وتعتيم](#part-54--جمر-ودخان-وتعتيم--embers-sparks--smoke-atmosphere)
- [`PART-55` شرر على ساعة الشريط](#part-55--شرر-على-ساعة-الشريط--event-sparks-on-the-tape-clock-three-kit)
- [`PART-56` بخار وغيوم من عناقيد بيضاوية](#part-56--بخار-وغيوم-من-عناقيد-بيضاوية--ellipse-cluster-clouds-smoke--steam-studio)
- [`PART-57` رذاذ وزبد وانهمار ماء](#part-57--رذاذ-وزبد-وانهمار-ماء--spray-foam--water-sheeting)
- [`PART-58` بحر عاكس وماء ضحل شفاف](#part-58--بحر-عاكس-وماء-ضحل-شفاف--reflective-sea--shallow-see-through-water-three-kit)
- [`PART-59` شيدر ماء منمّط ورسام الماء](#part-59--شيدر-ماء-منمّط-ورسام-الماء--stylised-water-shader--flat-sea-path)
- [`PART-60` أنظمة الطقس ثلاثية الأبعاد](#part-60--أنظمة-الطقس-ثلاثية-الأبعاد--3d-weather-vapour-cloud-slab-rain-flocks)
- [`PART-61` حياة البركة: كوي وبتلات وقصب](#part-61--حياة-البركة-كوي-وبتلات-وقصب--pond-life-koi-petals-lily-pads-reeds-sway)
- [`PART-62` مسارات ضوء السيارات](#part-62--مسارات-ضوء-السيارات--long-exposure-car-light-trails)
- [`PART-63` سكب وارتفاع السائل](#part-63--سكب-وارتفاع-السائل--pour-stream--liquid-fill-with-wobble)
- [`PART-64` سائل ملون ومعدن سائل](#part-64--سائل-ملون-ومعدن-سائل--fluid-sim-backdrop--chrome-metaballs)
- [`PART-65` لهب عادم وشعلة](#part-65--لهب-عادم-وشعلة--exhaust-plume--canvas-fire-emitter)
- [`PART-66` أشعة تحت الماء وفوانيس عائمة](#part-66--أشعة-تحت-الماء-وفوانيس-عائمة--underwater-rays--floating-lanterns)
- [`PART-67` محاكاة هوديني](#part-67--محاكاة-هوديني--houdini-flip--pyro--vellum--rbd--karma)
- [`PART-68` كرة ترتد بمعامل ارتداد](#part-68--كرة-ترتد-بمعامل-ارتداد--gravity-bounce-with-restitution--dotted-trail)
- [`PART-69` كرة داخل حلقات دوارة](#part-69--كرة-داخل-حلقات-دوارة--ball-in-rotating-gapped-rings-escape-sim)
- [`PART-70` سقوط وتكدس الأجسام](#part-70--سقوط-وتكدس-الأجسام--drops-piles--toppling-stacks)
- [`PART-71` محركات الأجسام الصلبة](#part-71--محركات-الأجسام-الصلبة--rigid-body-engines-rapier--cannon-es--matter-js)
- [`PART-72` حركات فيزيائية جاهزة](#part-72--حركات-فيزيائية-جاهزة--hyperframes-physical-motions-pendulum-physical-exit-stack-shuffle)
- [`PART-73` أوتار تهتز عند الاصطدام](#part-73--أوتار-تهتز-عند-الاصطدام--vibrating-strings-on-impact)
- [`PART-74` أسراب الطيور والحروف (boids)](#part-74--أسراب-الطيور-والحروف-boids--flocks--boids-birds-letters-stipple)
- [`PART-75` رمية قوسية بأشباح](#part-75--رمية-قوسية-بأشباح--parabolic-toss-with-ghost-trail)
- [`PART-U01` حقل كشف بالضجيج والمسافة من المركز](#part-u01--حقل-كشف-بالضجيج-والمسافة-من-المركز--noise--centre-distance-reveal-field)
- [`PART-X01` مطر الرموز وموجات الحروف](#part-x01--مطر-الرموز-وموجات-الحروف--code-rain-glyph-streams-and-the-crash-beat)

## البطاقات / cards

### `PART-01` — ضجيج حتمي بالهاش وmulberry32 / Deterministic hash / seeded RNG

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** استبدل Math.random بدالة هاش أو مولد ببذرة، فكل إطار يُرسم مطابقًا في كل رندر وبأي ترتيب. / Replace Math.random with an integer hash or a seeded PRNG so every frame renders identically, in any order.

**متى:** حين تتغير الجسيمات أو الوميض بين رندر وآخر وتحتاج نتيجة ثابتة في كل إطار / when random values must render identically on every frame and every re-render

**كيف:** rnd(i) = fract(sin(i·127.1 + 311.7)·43758.5453) for per-index values; KOSIF.rng(seed) = mulberry32 for sequences; motion-kit MOTION.rng(seed); flicker = hash(i, floor(t·10)). Everything in the lab and the proof films uses this (seed 20261016/20261015). (code snippet in references/powers/particles-fluids-physics.md)

**المعاملات:** e.g. 200 points, brightness = hash(i, floor(t·10))

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بذرة · حتمي · seed · hash · deterministic · mulberry32 · rng · عشوائي ثابت · توليد عشوائي · نفس النتيجة · random · reproducible render

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/starters/html-canvas/timeline.js:40`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:9`
- `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/particles-to-arabic/README.md`

#### 7. قدرات قريبة في العائلة

- `PART-02` الجسيم دالة للزمن لا حالة / Closed-form particles (state-free seek) (proven)
- `PART-03` الجسيم يعني شيئًا / Particle meaning rule (documented)

### `PART-02` — الجسيم دالة للزمن لا حالة / Closed-form particles (state-free seek)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** موقع كل جسيم يُحسب من t مباشرة (بالستي، سحب مغلق، دوري)، أو تُخزّن خطوات المحاكاة مسبقًا ثم يُبحث فيها — فلا حالة تتراكم بين الإطارات. / Compute each particle from t (ballistic, closed-form drag, periodic wrap) or pre-bake simulation steps and look them up — no state carried between frames.

**متى:** عند الحاجة لتقديم الجسيمات أو ترجيعها لأي لحظة دون تراكم حالة بين الإطارات / when particles must be seekable to any frame without carrying state between frames

**كيف:** Ballistic: p = p0 + v·τ + ½g·τ²; drag: p = p0 + v·(1 − e^(−kτ))/k; wrap: y = (y0 + v·t) mod H; stateful fields (curl advection) integrated once at 60 Hz with RK2 and stored, seek = linear interpolation between stored steps (particles-to-arabic). Bake Blender/Houdini sims to sequences — GLB does not carry them.

**المعاملات:** RK2 @ 60 Hz pre-baked; drag k 2.4/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صيغة مغلقة · closed form · bake · seek · simulation · deterministic · قفز للإطار · محاكاة مخبوزة · جاذبية · scrubbing · ballistic

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `blender` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/particles-to-arabic/README.md`
- `kosif-atlas/skills/1526-gamegen/4164-game-audio-vfx/SKILL.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/particle-burst.md`

#### 7. قدرات قريبة في العائلة

- `PART-01` ضجيج حتمي بالهاش وmulberry32 / Deterministic hash / seeded RNG (proven)
- `PART-03` الجسيم يعني شيئًا / Particle meaning rule (documented)
- `PART-04` ميزانية الأحجام والألوان والعدد / Size / colour / count budget (documented)

### `PART-03` — الجسيم يعني شيئًا / Particle meaning rule

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الجسيمات تُظهر كمية→بنية أو طاقة أو تدفقًا أو تفككًا؛ احذف الغبار الزخرفي. في الفيديو التحليلي كل جسيم كيان أو عينة أو حامل اتجاه أو مؤشر تركيز. / Particles show quantity→structure, energy, flow or dissolution; remove decorative dust. In analytic video each particle is an entity, sample, direction carrier or focus cue.

**متى:** حين تفكر في إضافة جسيمات للزينة أو تريدها أن تعبر عن كمية أو تدفق في فيديو تحليلي / when deciding whether particles belong on screen and what each one stands for

**كيف:** State the unit on screen or in VO; cap counts; sample instead of drawing every edge; pair with static width/labels for quantity; end on a static frame; avoid for aggregated or uncertain human harm.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** معنى · meaning · data · rule · particles · زخرفة · فيديو تحليلي · تمثيل البيانات · data storytelling · decorative dust

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/playbooks/particles.md:9`
- `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/particle-effects-and-flow.md`

#### 7. قدرات قريبة في العائلة

- `PART-01` ضجيج حتمي بالهاش وmulberry32 / Deterministic hash / seeded RNG (proven)
- `PART-02` الجسيم دالة للزمن لا حالة / Closed-form particles (state-free seek) (proven)
- `PART-04` ميزانية الأحجام والألوان والعدد / Size / colour / count budget (documented)
- `PART-05` المؤثر على إطار التلامس / Impact on the contact frame (documented)

### `PART-04` — ميزانية الأحجام والألوان والعدد / Size / colour / count budget

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاثة أحجام 4/8/14px، لونان كحد أقصى، 150–600 جسيم في Canvas و≤ 20,000 في WebGL، خلف النص وبكثافة غير متساوية. / Sizes 4/8/14 px, ≤ 2 colours, 150–600 on Canvas 2D, ≤ 20,000 WebGL points, behind type, uneven density.

**متى:** عند ضبط عدد الجسيمات وأحجامها وألوانها حتى لا تزدحم الشاشة أو يثقل الأداء / when setting particle count, sizes and colours for Canvas 2D or WebGL

**كيف:** Burst speeds 400–1300 px/s, gravity 60–150 px/s², flow-field noise scale .0025; go GPU (instanced/FBO) beyond ~5k.

**المعاملات:** 4/8/14 px; 150–600 Canvas; ≤ 20k WebGL

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ميزانية · budget · count · sizes · rule · عدد الجسيمات · أداء · زحمة · performance · particle count

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/playbooks/particles.md:15-18`
- `kosif-tool/playbooks/particles.md`

#### 7. قدرات قريبة في العائلة

- `PART-02` الجسيم دالة للزمن لا حالة / Closed-form particles (state-free seek) (proven)
- `PART-03` الجسيم يعني شيئًا / Particle meaning rule (documented)
- `PART-05` المؤثر على إطار التلامس / Impact on the contact frame (documented)
- `PART-06` انفجار ببذرة وجاذبية / Seeded analytic burst (proven)

### `PART-05` — المؤثر على إطار التلامس / Impact on the contact frame

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الانفجار والمؤثر الصوتي يقعان على إطار التلامس أو القمة الفعلي لا على بداية المقطع. / Bursts and hit SFX land on the actual contact/apex frame, not the clip start.

**متى:** حين يجب أن يقع الانفجار أو صوت الضربة على لحظة التلامس تمامًا لا على بداية المقطع / when bursts and hit sounds must land exactly on the contact frame

**كيف:** One event list drives both audio and particles (e.g. SOUND.kicks, makeSparks event times); respect reduced-motion and flashing limits.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تلامس · impact · contact frame · sfx · sync · مزامنة · مؤثر صوتي · ضربة · hit timing · audio sync

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-atlas/skills/1526-gamegen/4164-game-audio-vfx`

#### 7. قدرات قريبة في العائلة

- `PART-03` الجسيم يعني شيئًا / Particle meaning rule (documented)
- `PART-04` ميزانية الأحجام والألوان والعدد / Size / colour / count budget (documented)
- `PART-06` انفجار ببذرة وجاذبية / Seeded analytic burst (proven)
- `PART-07` وصفة انفجار الكشف / Reveal-burst recipe (documented)

### `PART-06` — انفجار ببذرة وجاذبية / Seeded analytic burst

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 160 جسيمًا ببذرة ثابتة تنفجر من المركز بمسافة expo.out وتمايل وجاذبية خفيفة وتلاشٍ inOutCubic — دالة خالصة للزمن. / 160 seeded particles explode from the centre with expo.out distance, wobble, slight gravity and an inOutCubic fade — a pure function of t.

**متى:** عند طلب انفجار جسيمات من المركز يتكرر بالشكل نفسه في كل رندر / when you need a repeatable particle explosion from the centre as a pure function of time

**كيف:** rng(20261015): angle, speed 400–1300 px (420–1320 in the starter), size 4–14, 70% #7ee8d2 / 30% #ffb86b; d = outExpo(life)·sp; alpha = 1 − inOutCubic(life); y += life·120; r shrinks 60%. Rendered here twice: the lab panel and the html-canvas starter itself (render_html.cjs, 7–10.5 s, burst + ring around «الفكرة»).

**المعاملات:** 160 parts; 400–1300 px/s; gravity 60–150 px/s²; life .7–1.0

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** انفجار · burst · seeded · gravity · explosion · reveal · فرقعة · جسيمات متطايرة · تفجير · particle explosion · canvas burst

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/starters/html-canvas/index.html:118`
- `kosif-tool/playbooks/particles.md:52-66`

#### 7. قدرات قريبة في العائلة

- `PART-04` ميزانية الأحجام والألوان والعدد / Size / colour / count budget (documented)
- `PART-05` المؤثر على إطار التلامس / Impact on the contact frame (documented)
- `PART-07` وصفة انفجار الكشف / Reveal-burst recipe (documented)
- `PART-08` قصاصات احتفال تنقلب / Confetti burst / rain with 3D flip (proven)

### `PART-07` — وصفة انفجار الكشف / Reveal-burst recipe

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الكلمة البطلة تكبر بنابض، ثم ينطلق 160 جسيمًا وحلقة تتسع وتخبو. / Hero word springs in, seeded particles burst, a ring expands and fades.

**متى:** حين تريد إظهار كلمة رئيسية بقفزة نابضية يتبعها انفجار جسيمات وحلقة تتسع / for revealing a hero word with a spring pop, a particle burst and an expanding ring

**كيف:** Word 0–250 ms spring (damping 14, stiffness 150); 160 particles 50–3000 ms; ring 100–1100 ms outExpo (SHAPE shockwave).

**المعاملات:** word 250 ms; ring 1 s outExpo

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كشف · reveal · burst · ring · hero word · ظهور كلمة · عنوان · موجة صدمة · word reveal · shockwave

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/playbooks/particles.md:38-40`

#### 7. قدرات قريبة في العائلة

- `PART-05` المؤثر على إطار التلامس / Impact on the contact frame (documented)
- `PART-06` انفجار ببذرة وجاذبية / Seeded analytic burst (proven)
- `PART-08` قصاصات احتفال تنقلب / Confetti burst / rain with 3D flip (proven)
- `PART-09` انفجارات HyperFrames الجاهزة / HyperFrames burst primitives (particle-burst, radial-burst-lines) (install)

### `PART-08` — قصاصات احتفال تنقلب / Confetti burst / rain with 3D flip

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مستطيلات صغيرة بألوان العلامة تنطلق للأعلى وتسقط بجاذبية وتتمايل وتنقلب (scaleY = cos). / Small brand-coloured rectangles launch up, fall with gravity, sway and flip in 3D (scaleY = cos).

**متى:** لما يطلب المستخدم احتفالًا بقصاصات ملونة تنطلق وتتساقط وتنقلب، مثل بطاقة الختام / when the user wants a celebration with confetti bursting, falling and flipping, e.g. an end card

**كيف:** Per piece: x = x0 + vx·t + sin(3t + ph)·20, y = y0 + vy·t + ½g·t², rotate spin·t, scale(1, cos(8t + ph)); 20–300 pieces, g 600–900 px/s², life 1–2.5 s. Rendered here (70 pieces, closed form). HyperFrames confetti component is the seeded drop-in.

**المعاملات:** 40–150 pcs; g 600–900 px/s²; sway 20 px; life 1.5–2.5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قصاصات · احتفال · confetti · celebration · end card · كونفيتي · فرحة · تهنئة · party · falling paper

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-one/vendor/hyperframes/registry/components/confetti/confetti.html`
- `kosif-tool/styles/isometric`
- `kosif-tool/styles/pm-deebeeeff-50fcd0`

#### 7. قدرات قريبة في العائلة

- `PART-06` انفجار ببذرة وجاذبية / Seeded analytic burst (proven)
- `PART-07` وصفة انفجار الكشف / Reveal-burst recipe (documented)
- `PART-09` انفجارات HyperFrames الجاهزة / HyperFrames burst primitives (particle-burst, radial-burst-lines) (install)
- `PART-10` شرطات وشرارات الاصطدام / Radial dash burst & impact spark lines (seen)

### `PART-09` — انفجارات HyperFrames الجاهزة / HyperFrames burst primitives (particle-burst, radial-burst-lines)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 (+ GSAP standard license). |

**ما هي:** انفجار جسيمات وانفجار خطوط سرعة شعاعية مثبتان على أحداث الموسيقى (drop / crash / surge)، وقاعدة انفجار حتمي ≤ 40 جسيمًا. / Particle explosion and radial speed-line bursts anchored to music events, plus the deterministic burst rule (≤ ~40 particles, closed-form gravity).

**متى:** حين تريد انفجار جسيمات أو خطوط سرعة شعاعية على لحظة الدروب أو الضربة في الموسيقى / when particle or radial speed-line bursts must hit a music drop, crash or surge

**كيف:** Copy music-to-video/references/motion-primitives/particle-burst/scene.html or radial-burst-lines/scene.html; anchor to audiomap events; best span .2–1.2 s / .2–.8 s.

**المعاملات:** ≤ ~40 particles; chips radius 2 px

**التثبيت:** npm i -D hyperframes

**الوسوم:** انفجار · beat · drop · hyperframes · speed lines · إيقاع · موسيقى · خطوط شعاعية · music sync · crash

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/particle-burst/scene.html`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/radial-burst-lines/scene.html`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/particle-burst.md`

#### 7. قدرات قريبة في العائلة

- `PART-07` وصفة انفجار الكشف / Reveal-burst recipe (documented)
- `PART-08` قصاصات احتفال تنقلب / Confetti burst / rain with 3D flip (proven)
- `PART-10` شرطات وشرارات الاصطدام / Radial dash burst & impact spark lines (seen)
- `PART-11` تحطم إلى مربعات أو شظايا / Shatter to squares / shards / ring shards (seen)

### `PART-10` — شرطات وشرارات الاصطدام / Radial dash burst & impact spark lines

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 80–150 شرطة قصيرة من المركز بسرعة متباطئة تدور مع اتجاهها وتخبو بثلاثة ألوان؛ أو 4–6 خطوط قصيرة عند نقطة الاصطدام. / 80–150 short segments from the centre, decelerating, rotated along velocity, fading in a 3-colour mix; or 4–6 short radial lines at an impact point.

**متى:** عند الحاجة لشرطات تنطلق من المركز أو خطوط شرر قصيرة عند نقطة اصطدام / for radial dash bursts from the centre or short spark lines at an impact point

**كيف:** White 70% / yellow 20% / red 10%; life 600–900 ms; impact lines life 200 ms at 200 px/s; tracer variant: bursts of 6–10 additive streaks at ~3000 u/s, life .3 s, #fff2d0.

**المعاملات:** 80–150 dashes, 600–900 ms; impact 4–6 lines, 200 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شرطات · شرر · dash burst · impact · tracers · اصطدام · خطوط سرعة · ضربة · spark lines · hit effect

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-sudeepsd-1a3485`
- `kosif-tool/styles/pm-kamstudiolabs-447565`
- `kosif-tool/styles/pm-nft-chen-5f8bb0`

#### 7. قدرات قريبة في العائلة

- `PART-08` قصاصات احتفال تنقلب / Confetti burst / rain with 3D flip (proven)
- `PART-09` انفجارات HyperFrames الجاهزة / HyperFrames burst primitives (particle-burst, radial-burst-lines) (install)
- `PART-11` تحطم إلى مربعات أو شظايا / Shatter to squares / shards / ring shards (seen)
- `PART-12` انفجار سحابة صور أو بطاقات / Image-card burst cloud (seen)

### `PART-11` — تحطم إلى مربعات أو شظايا / Shatter to squares / shards / ring shards

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الجسم يُستبدل بمربعات تحمل ألوانه وتُقذف على حلزون مع انحراف لوني، أو مثلثات تنفجر من نواة متوهجة، أو حلقة تتشظى أقواسًا. / Replace the object with coloured square particles flung on a spiral with RGB split, triangles exploding from a glowing core, or a ring splitting into arc shards.

**متى:** لما يطلب المستخدم أن يتكسر جسم أو حلقة إلى مربعات أو شظايا متطايرة / when an object or a ring should break apart into flying squares or shards

**كيف:** 300–600 squares, 600 ms, R/B offset 4–8 px + motion blur; shards 600 ms easeOutExpo with spin; ring: 24 shards 400–600 px/s fading 500 ms, or ~60 glowing dots sampled on the ring drifting 40–120 px/s for 2 s.

**المعاملات:** 300–600 squares; 24 ring shards

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تحطم · شظايا · shatter · shards · rgb split · تكسير · تهشم · تفتت · break apart · fragments

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-teslachartz-c58b32`
- `kosif-tool/styles/pm-zaqailo-212ad3`
- `kosif-tool/styles/pm-kantamk-61f410`

#### 7. قدرات قريبة في العائلة

- `PART-09` انفجارات HyperFrames الجاهزة / HyperFrames burst primitives (particle-burst, radial-burst-lines) (install)
- `PART-10` شرطات وشرارات الاصطدام / Radial dash burst & impact spark lines (seen)
- `PART-12` انفجار سحابة صور أو بطاقات / Image-card burst cloud (seen)
- `PART-13` انفجار فتح إنجاز ونجوم ذهبية / Achievement unlock star burst (seen)

### `PART-12` — انفجار سحابة صور أو بطاقات / Image-card burst cloud

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ~120 بطاقة صور مستديرة تنطلق شعاعيًا بأعماق مختلفة وتبطؤ إلى سحابة طافية حول كبسولة نص. / ~120 rounded image cards fly radially at varied depth (scale .4–1.2), slowing to a drifting cloud around a caption pill.

**متى:** حين تعرض مجموعة صور أو بطاقات تنطلق من المركز ثم تطفو حول عنوان / when many image cards should burst out radially and float around a caption

**كيف:** Burst 700 ms expo-out then drift 10 px/s; soft shadows; slight rotation; depth blur by scale.

**المعاملات:** ~120 cards; 700 ms; drift 10 px/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صور · سحابة · image burst · cards · community · بطاقات صور · معرض صور · صور متطايرة · photo cloud · gallery

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-rossaxbt-3085b7`
- `kosif-tool/styles/pm-macrohou-33959d`

#### 7. قدرات قريبة في العائلة

- `PART-10` شرطات وشرارات الاصطدام / Radial dash burst & impact spark lines (seen)
- `PART-11` تحطم إلى مربعات أو شظايا / Shatter to squares / shards / ring shards (seen)
- `PART-13` انفجار فتح إنجاز ونجوم ذهبية / Achievement unlock star burst (seen)
- `PART-14` مؤثرات بكسل بخطوات اللوحة / Pixel VFX by palette-step fades (documented)

### `PART-13` — انفجار فتح إنجاز ونجوم ذهبية / Achievement unlock star burst

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 80 نجمة ذهبية تنطلق شعاعيًا بجاذبية خفيفة وتخبو في 2 ث. / 80 gold star particles radial with light gravity, fading over 2 s.

**متى:** عند لحظة فتح إنجاز أو مكافأة تحتاج انفجار نجوم ذهبية يتلاشى / for an achievement unlock or reward moment with a fading gold star burst

**كيف:** Gravity .05 per frame-unit, colours #e3b75a / #fff; star sprite 4-point sparkle.

**المعاملات:** 80 stars; fade 2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إنجاز · نجوم · achievement · unlock · gold · مكافأة · فوز · ذهبي · reward · star burst

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-bthreeagency-b9b8d9`

#### 7. قدرات قريبة في العائلة

- `PART-11` تحطم إلى مربعات أو شظايا / Shatter to squares / shards / ring shards (seen)
- `PART-12` انفجار سحابة صور أو بطاقات / Image-card burst cloud (seen)
- `PART-14` مؤثرات بكسل بخطوات اللوحة / Pixel VFX by palette-step fades (documented)
- `PART-15` جسيمات تتجمع كلمة عربية / Particles gather into a shaped Arabic word (proven)

### `PART-14` — مؤثرات بكسل بخطوات اللوحة / Pixel VFX by palette-step fades

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شرر وضربات وانفجارات وتعاويذ تكبر وتنفجر وتخبو بالنزول على سلم لوني من الساطع إلى الداكن، لا بالشفافية؛ أو تموت بفقد بكسل كل إطار. / Sparks, slashes, explosions and spells grow, burst and fade by stepping down a bright→dark ramp — never alpha; or die by losing 1 px per frame.

**متى:** حين يطلب مؤثرات بكسل آرت بطابع الألعاب القديمة كشرر وضربات وتعاويذ تخبو بدرجات اللون / for pixel-art sparks, slashes, explosions or spells that fade by palette steps

**كيف:** Procedural draw(frame) in Pillow; hold the impact frame 2–3 frames; ramp 4–6 colours; shrink-to-die: 24 particles, 3–5 frame life.

**المعاملات:** ramp 4–6 colours; hold 2–3 frames

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بكسل · pixel vfx · palette · retro · sprite · بكسل آرت · ألعاب قديمة · تعويذة · pixel art · spell effect

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-atlas/skills/2460-pixel-art/9530-vfx`
- `kosif-tool/styles/pm-0xevinho-3777d8/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `PART-12` انفجار سحابة صور أو بطاقات / Image-card burst cloud (seen)
- `PART-13` انفجار فتح إنجاز ونجوم ذهبية / Achievement unlock star burst (seen)
- `PART-15` جسيمات تتجمع كلمة عربية / Particles gather into a shaped Arabic word (proven)
- `PART-16` تفكك النص إلى جسيمات أو جمر / Text dissolve / disintegrate to embers (documented)

### `PART-15` — جسيمات تتجمع كلمة عربية / Particles gather into a shaped Arabic word

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 6000 جسيم تسبح في حقل curl ثم تنجذب من اليمين إلى نقاط مأخوذة من صورة الكلمة المشكّلة كاملة، فتبقى الحروف متصلة. / 6,000 particles swim in a curl field, then attract right-to-left to points sampled from the whole shaped word, so letters stay joined.

**متى:** لما يطلب المستخدم أن تتجمع الجسيمات وتكوّن كلمة أو عنوانًا عربيًا بحروف متصلة / when particles should assemble into a joined Arabic word or title

**كيف:** Render the word once with the shaper on a hidden canvas, take alpha > 150 pixels on a 2 px step, Fisher–Yates shuffle with the seed; start_i = 2.2 + 1.1·(.72·(1−u) + .28·rand) s (u = x position, right first), duration 1.75 s inOutCubic, curved path ±.18–.50; then breathe, light sweep, and explode (drag k 2.4/s, buoyancy −46τ²). Proven in proofs/particles-to-arabic (13/13).

**المعاملات:** N 6000; seed 20261016; step 2 px; travel 1.75 s; shockwave 3200 px/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** جسيمات · كلمة عربية · تجمع · particles to text · arabic · gather · curl · تكوين نص · عنوان عربي · حروف متصلة · text formation · word reveal

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/particles-to-arabic/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/particles-to-arabic/index.html`
- `kosif-tool/playbooks/particles.md:27`

#### 7. قدرات قريبة في العائلة

- `PART-13` انفجار فتح إنجاز ونجوم ذهبية / Achievement unlock star burst (seen)
- `PART-14` مؤثرات بكسل بخطوات اللوحة / Pixel VFX by palette-step fades (documented)
- `PART-16` تفكك النص إلى جسيمات أو جمر / Text dissolve / disintegrate to embers (documented)
- `PART-17` أيقونة أو شعار يتكون من سحابة نقاط / Icon / logo coalescing from a point cloud (seen)

### `PART-16` — تفكك النص إلى جسيمات أو جمر / Text dissolve / disintegrate to embers

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بكسلات الكلمة تُستبدل بجسيمات تصعد وتخبو، أو تتحرر من اليسار لليمين بعتبة ضوضاء وتتحول من الأبيض إلى البرتقالي كجمر. / Word pixels become particles that drift up and fade, or are released by a sweeping noise threshold and turn white→orange like embers.

**متى:** حين يريد أن تتلاشى الكلمة وتتفتت إلى جسيمات أو جمر متصاعد / when a word should break up into rising particles or glowing embers and vanish

**كيف:** Arabic: sample the whole shaped word and keep it readable ≥ 1 s first; drift 200 px over 1.5 s; ember variant 20–60k points (GPU), release sweep 1.2 s (for Arabic sweep right→left), curl velocity, additive, life 2 s. HyperFrames particle-text-dissolve does in/out with one painter (no per-particle tweens).

**المعاملات:** drift 200 px / 1.5 s; hold ≥ 1 s; sweep 1.2 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تفكك · جمر · dissolve · disintegrate · embers · text · تلاشي النص · اختفاء · تبخر · text vanish · particle text

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/playbooks/particles.md:44`
- `kosif-tool/playbooks/particles.md:72`
- `kosif-one/vendor/hyperframes/registry/components/particle-text-dissolve/particle-text-dissolve.html`

#### 7. قدرات قريبة في العائلة

- `PART-14` مؤثرات بكسل بخطوات اللوحة / Pixel VFX by palette-step fades (documented)
- `PART-15` جسيمات تتجمع كلمة عربية / Particles gather into a shaped Arabic word (proven)
- `PART-17` أيقونة أو شعار يتكون من سحابة نقاط / Icon / logo coalescing from a point cloud (seen)
- `PART-18` جسيمات تتحول إلى بيانات أو واجهة / Particles → chart / grid / UI (seen)

### `PART-17` — أيقونة أو شعار يتكون من سحابة نقاط / Icon / logo coalescing from a point cloud

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط تُؤخذ على مسار الأيقونة تبدأ مبعثرة في سحابة دمعية وتقفز بنابض إلى أهدافها، مع توهج نقطة البؤرة. / Points sampled along an icon path start scattered in a teardrop cloud and spring to their targets, with a glowing focal point.

**متى:** عند كشف شعار أو أيقونة تتكون من نقاط مبعثرة تقفز إلى أماكنها / for a logo or icon reveal that assembles from scattered points springing into place

**كيف:** 300–6000 points, spring stiffness 120 damping 18 (~600 ms), additive + bloom 1.5; X-glyph variant: 80–150 glyph particles scatter .6 s then converge .8 s and crossfade to the real logo; pixel-logo variant eases to bitmap grid cells over 1.5 s.

**المعاملات:** 300–6000 pts; spring 120/18; ~600 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أيقونة · شعار · point cloud · logo reveal · coalesce · لوجو · ظهور الشعار · تجمع نقاط · logo animation · points assemble

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-bogdandragomir-35e024`
- `kosif-tool/styles/pm-madhav-xo-f97f20`
- `kosif-tool/styles/pm-robj3d3-b18fad`

#### 7. قدرات قريبة في العائلة

- `PART-15` جسيمات تتجمع كلمة عربية / Particles gather into a shaped Arabic word (proven)
- `PART-16` تفكك النص إلى جسيمات أو جمر / Text dissolve / disintegrate to embers (documented)
- `PART-18` جسيمات تتحول إلى بيانات أو واجهة / Particles → chart / grid / UI (seen)
- `PART-19` كشف صورة بالجسيمات / Particle image reveal (HyperFrames) (install)

### `PART-18` — جسيمات تتحول إلى بيانات أو واجهة / Particles → chart / grid / UI

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل جسيم ينتقل إلى نقطة هدف (عناقيد، صناديق مدرج تكراري، خلايا شبكة) ثم تخبو النقاط وتظهر الواجهة مكانها. / Each particle lerps to a target set (clusters, histogram bins, snapped grid cells), then the dots fade while UI layers fade up.

**متى:** حين تتحول الجسيمات إلى رسم بياني أو شبكة أو واجهة تطبيق في فيديو شرح بيانات / when particles should morph into a chart, histogram, grid or UI

**كيف:** Targets from chart geometry; 1.2 s easeInOut; grid pitch ~24 px, 600 ms easeInOutCubic stagger 0–300 ms by distance; prompt→particles→chart morph 700 ms (idea).

**المعاملات:** 1.2 s; grid 24 px; stagger ≤ 300 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بيانات · مدرج · particles to chart · histogram · ui · رسم بياني · إنفوجرافيك · تحول · data viz · morph

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-ismailfahmi-557268`
- `kosif-tool/styles/pm-bogdandragomir-35e024`
- `kosif-tool/styles/pm-listudio-820c7b/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `PART-16` تفكك النص إلى جسيمات أو جمر / Text dissolve / disintegrate to embers (documented)
- `PART-17` أيقونة أو شعار يتكون من سحابة نقاط / Icon / logo coalescing from a point cloud (seen)
- `PART-19` كشف صورة بالجسيمات / Particle image reveal (HyperFrames) (install)
- `PART-20` سحابة تتحول من حلقة إلى كرة / Point-cloud shape morph (torus ↔ sphere, helix → strands) (seen)

### `PART-19` — كشف صورة بالجسيمات / Particle image reveal (HyperFrames)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0. |

**ما هي:** حقل جسيمات ببذرة يتقارب بينما تنكشف صورة تحته، والآثار ترق حتى تصفو. / A seeded particle field converges while an image reveals beneath, trails thinning until clean.

**متى:** لما يطلب كشف صورة تظهر تدريجيًا تحت حقل جسيمات يتقارب / when an image should be revealed beneath a converging particle field

**كيف:** npx hyperframes add particle-image-reveal; density low\|med\|high; direction ltr\|center (use center or mirror for Arabic layouts).

**التثبيت:** npx hyperframes add particle-image-reveal

**الوسوم:** كشف صورة · image reveal · particles · hyperframes · ظهور صورة · إظهار صورة · تقارب الجسيمات · photo reveal

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-one/vendor/hyperframes/registry/components/particle-image-reveal/particle-image-reveal.html`

#### 7. قدرات قريبة في العائلة

- `PART-17` أيقونة أو شعار يتكون من سحابة نقاط / Icon / logo coalescing from a point cloud (seen)
- `PART-18` جسيمات تتحول إلى بيانات أو واجهة / Particles → chart / grid / UI (seen)
- `PART-20` سحابة تتحول من حلقة إلى كرة / Point-cloud shape morph (torus ↔ sphere, helix → strands) (seen)
- `PART-21` من فيديو إلى جسم جسيمي / Mocap: performer silhouette → particle body (ready)

### `PART-20` — سحابة تتحول من حلقة إلى كرة / Point-cloud shape morph (torus ↔ sphere, helix → strands)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** N نقطة لكل منها هدفان (سطح طارة وسطح كرة) تُستوفى مع خطوط قصيرة باتجاه السرعة وتدرج برتقالي→أزرق؛ أو لولب مزدوج يصير خيوطًا. / N points with two targets (torus surface, sphere surface) lerped with velocity streaks and an orange→blue ramp; or a double helix whose points become strands.

**متى:** عند تحويل سحابة نقاط من شكل إلى آخر مثل حلقة إلى كرة أو لولب إلى خيوط / for morphing a 3D point cloud between shapes, like torus to sphere or helix to strands

**كيف:** N 5–10k, morph 1.5 s, slow y-rotation; pair targets by sorting both sets by (θ, φ) to avoid crossing chaos.

**المعاملات:** 5–10k pts; 1.5 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سحابة نقاط · torus · sphere · morph · helix · تحول الأشكال · كرة · لولب · shape transform · 3d points

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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
- `kosif-tool/styles/pm-madebyjmayala-b9204d`

#### 7. قدرات قريبة في العائلة

- `PART-18` جسيمات تتحول إلى بيانات أو واجهة / Particles → chart / grid / UI (seen)
- `PART-19` كشف صورة بالجسيمات / Particle image reveal (HyperFrames) (install)
- `PART-21` من فيديو إلى جسم جسيمي / Mocap: performer silhouette → particle body (ready)
- `PART-22` صندوق الضوضاء / Noise toolbox (Perlin / Simplex / curl / fBm / warp) (documented)

### `PART-21` — من فيديو إلى جسم جسيمي / Mocap: performer silhouette → particle body

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** من فيديو بكاميرا ثابتة: خلفية وسيطة، فرق، تنظيف بالمورفولوجيا، ونقاط ثابتة لكل إطار تغذي جسمًا جسيميًا في three-kit. / From a fixed-camera video: median background, difference, morphology cleanup and a stable seeded point set per frame for a three-kit particle body.

**متى:** حين يريد تحويل راقص أو شخص في فيديو بكاميرا ثابتة إلى جسم من الجسيمات / when turning a performer in a fixed-camera video into a particle body

**كيف:** python motion.py mocap VIDEO --out body.json [--fps 30 --points 1200 --from 0 --dur D] → makeParticleBody.

**المعاملات:** 480 px; threshold 28; Gaussian 5×5; open/close 5×5; 30× candidates seed 7; coords 0–1000

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** التقاط حركة · mocap · silhouette · particle body · dance · رقص · راقص · تتبع الجسم · motion capture · video to particles

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-studio/motion/qa.py:598`
- `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### 7. قدرات قريبة في العائلة

- `PART-19` كشف صورة بالجسيمات / Particle image reveal (HyperFrames) (install)
- `PART-20` سحابة تتحول من حلقة إلى كرة / Point-cloud shape morph (torus ↔ sphere, helix → strands) (seen)
- `PART-22` صندوق الضوضاء / Noise toolbox (Perlin / Simplex / curl / fBm / warp) (documented)
- `PART-23` حقل curl تحليلي خالٍ من التباعد / Analytic curl field (stream-function) (proven)

### `PART-22` — صندوق الضوضاء / Noise toolbox (Perlin / Simplex / curl / fBm / warp)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** Perlin للكتل، Simplex للتدرجات، curl لحركة سائلة بلا تباعد، fBm للغيم والتضاريس، وتشويه المجال (warp the warp) للتدفق الملتف. / Perlin for blobs, Simplex for gradients, curl for divergence-free fluid motion, fBm for clouds/terrain, domain warping for curling flow.

**متى:** عند اختيار نوع الضوضاء المناسب لحركة سائلة أو غيوم أو تضاريس أو تدفق ملتف / when choosing a noise type for fluid motion, clouds, terrain or curling flow

**كيف:** GLSL noise in shaders or JS (three-kit K3.fbm, simplex-noise); fBm 4–6 octaves; drive time uniform from frame/fps, never clock.elapsedTime. Analytic fallback: 3–4 summed prime-frequency sines scrolled .1–.3 units/s.

**المعاملات:** fBm 5 oct; freq 1.5; speed .5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ضوضاء · curl · perlin · simplex · fbm · domain warp · غيوم · تضاريس · تشويش · noise texture · procedural noise

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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
- `kosif-tool/playbooks/code.md:28`

#### 7. قدرات قريبة في العائلة

- `PART-20` سحابة تتحول من حلقة إلى كرة / Point-cloud shape morph (torus ↔ sphere, helix → strands) (seen)
- `PART-21` من فيديو إلى جسم جسيمي / Mocap: performer silhouette → particle body (ready)
- `PART-23` حقل curl تحليلي خالٍ من التباعد / Analytic curl field (stream-function) (proven)
- `PART-24` خطوط حقل التدفق / Flow-field streak lines (proven)

### `PART-23` — حقل curl تحليلي خالٍ من التباعد / Analytic curl field (stream-function)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** دالة تيار ψ من سبع موجات جيبية، والسرعة = (∂ψ/∂y, −∂ψ/∂x) بمشتقات تحليلية — جسيمات تدور ولا تتكدس. / A stream function ψ of 7 sine waves; velocity = (∂ψ/∂y, −∂ψ/∂x) with analytic derivatives — particles swirl and never clump.

**متى:** حين تحتاج جسيمات تدور وتلتف كالسائل دون أن تتكدس في مكان واحد / when particles must swirl like a fluid without clumping together

**كيف:** Wavelengths 260–1020 px, speeds 38–84 px/s, +18 px/s updraft; integrate RK2 at 60 Hz and pre-store (see PART-02). Proven in proofs/particles-to-arabic.

**المعاملات:** 7 waves; λ 260–1020 px; RK2 60 Hz

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** curl · stream function · divergence free · flow · swirl · دوران · التفاف · حركة سائلة · fluid motion · no clumping

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/particles-to-arabic/README.md`

#### 7. قدرات قريبة في العائلة

- `PART-21` من فيديو إلى جسم جسيمي / Mocap: performer silhouette → particle body (ready)
- `PART-22` صندوق الضوضاء / Noise toolbox (Perlin / Simplex / curl / fBm / warp) (documented)
- `PART-24` خطوط حقل التدفق / Flow-field streak lines (proven)
- `PART-25` سرير تدفق ولزوجة على الإيقاع / Beat-anchored flow-field bed & gooey metaball (HyperFrames) (install)

### `PART-24` — خطوط حقل التدفق / Flow-field streak lines

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** آلاف الجسيمات تتبع زاوية من ضوضاء تحليلية وتُرسم خطوطًا قصيرة بمزج جمعي — شعر أو ريح أو مغناطيس. / Particles follow an angle from analytic noise and are drawn as short additive streaks — hair, wind, magnetism.

**متى:** عند رسم خطوط ناعمة تتبع حقل ضوضاء كالشعر أو الريح أو المغناطيس، أو خلفية خلف العناوين / for noise-driven streak lines like hair, wind or magnetism, or a backdrop behind titles

**كيف:** angle = noise(x·.0025, y·.0025, t·.2)·2π, speed 40–120 px/s; draw 14-step polylines at alpha .25 with "lighter". Rendered here (500 seeds). Carpet variant: grid of 24×5 px segments rotated to noise(x,y,t)·2π (scale .004); backdrop at 15% opacity, .2 units/s behind titles.

**المعاملات:** noise scale .0025–.004; 40–120 px/s; alpha .1–.25

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حقل تدفق · flow field · streaks · generative · noise · ريح · شعر · مغناطيس · خلفية متحركة · wind lines · generative art

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/playbooks/particles.md:26`
- `kosif-tool/playbooks/code.md:47`
- `kosif-tool/styles/pm-ismailfahmi-557268`

#### 7. قدرات قريبة في العائلة

- `PART-22` صندوق الضوضاء / Noise toolbox (Perlin / Simplex / curl / fBm / warp) (documented)
- `PART-23` حقل curl تحليلي خالٍ من التباعد / Analytic curl field (stream-function) (proven)
- `PART-25` سرير تدفق ولزوجة على الإيقاع / Beat-anchored flow-field bed & gooey metaball (HyperFrames) (install)
- `PART-26` تدفق الجسيمات على المسارات / Particle flow along routes & network edges (documented)

### `PART-25` — سرير تدفق ولزوجة على الإيقاع / Beat-anchored flow-field bed & gooey metaball (HyperFrames)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0. |

**ما هي:** خلفية curl توليدية تمتد على المقطع كله، وحقل كرات لزجة على البناء والإسقاط. / A generative curl-noise background bed for the whole span, and a gooey metaball field anchored to build/drop.

**متى:** حين تحتاج خلفية توليدية متدفقة طوال المقطع أو كرات لزجة على البناء والدروب الموسيقي / when you need a flowing generative background bed or gooey blobs tied to a music build or drop

**كيف:** Copy motion-primitives/bg-flow-field/scene.html (best span 4–12 s) or gooey-metaball/scene.html (1.5–3 s); anchor to audiomap events.

**التثبيت:** npm i -D hyperframes

**الوسوم:** تدفق · flow field · metaball · beat · hyperframes · خلفية · كرات لزجة · موسيقى · gooey · generative background

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/bg-flow-field/scene.html`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/gooey-metaball/scene.html`

#### 7. قدرات قريبة في العائلة

- `PART-23` حقل curl تحليلي خالٍ من التباعد / Analytic curl field (stream-function) (proven)
- `PART-24` خطوط حقل التدفق / Flow-field streak lines (proven)
- `PART-26` تدفق الجسيمات على المسارات / Particle flow along routes & network edges (documented)
- `PART-27` طبقات التدفق في deck.gl / deck.gl flow layers (trips, arcs, hex) (install)

### `PART-26` — تدفق الجسيمات على المسارات / Particle flow along routes & network edges

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط تسافر على طرق أو أنابيب أو حواف شبكة لتظهر الاتجاه والنشاط بآثار تخبو. / Dots travelling along routes, pipes or network edges to show direction and activity, with fading trails.

**متى:** عند إظهار الاتجاه والنشاط على طرق أو أنابيب أو شبكة بنقاط متحركة تترك أثرًا / for showing direction and activity with dots moving along routes, pipes or network edges

**كيف:** Precompute paths; each particle phase + speed; pos = pointAt((t·speed + phase) % 1); trail = last 8–20 samples with decaying opacity; never all edges at once — filter to the focus neighbourhood. Canvas for a few hundred, Pixi ParticleContainer/three Points for many. Playbook: 600 ms per traversal.

**المعاملات:** trail 8–20 samples; 600 ms per traversal

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تدفق · مسار · flow along path · network · data stream · أنابيب · نشاط الشبكة · اتجاه الحركة · pipes · moving dots

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:p5` ← npm ls p5 أو وجود node_modules/p5
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/particle-effects-and-flow.md`
- `kosif-tool/playbooks/particles.md:46`

#### 7. قدرات قريبة في العائلة

- `PART-24` خطوط حقل التدفق / Flow-field streak lines (proven)
- `PART-25` سرير تدفق ولزوجة على الإيقاع / Beat-anchored flow-field bed & gooey metaball (HyperFrames) (install)
- `PART-27` طبقات التدفق في deck.gl / deck.gl flow layers (trips, arcs, hex) (install)
- `PART-28` حقل حراري يُلطخ بالإصبع / Thermal finger-trail smear field (documented)

### `PART-27` — طبقات التدفق في deck.gl / deck.gl flow layers (trips, arcs, hex)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طبقات GPU لحركة على الخرائط: رحلات بآثار تخبو، أقواس منشأ-وجهة، مسارات، وتجميع سداسي. / GPU map layers: timestamped trips with fading trails, OD arcs, paths, hex aggregation.

**متى:** لما يطلب خريطة متحركة برحلات أو أقواس من منشأ إلى وجهة أو كثافة سداسية / when animating a map with trips, origin-destination arcs or hexagon density

**كيف:** TripsLayer currentTime = frame time; ArcLayer (state geodesic vs schematic); HexagonLayer for density; over MapLibre.

**التثبيت:** npm i deck.gl maplibre-gl

**الوسوم:** deck.gl · trips · arcs · map flow · geo · خريطة · رحلات · أقواس · maplibre · origin destination

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:maplibre` ← npm ls maplibre أو وجود node_modules/maplibre
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/deckgl-d3-geo-stack-selection.md`

#### 7. قدرات قريبة في العائلة

- `PART-25` سرير تدفق ولزوجة على الإيقاع / Beat-anchored flow-field bed & gooey metaball (HyperFrames) (install)
- `PART-26` تدفق الجسيمات على المسارات / Particle flow along routes & network edges (documented)
- `PART-28` حقل حراري يُلطخ بالإصبع / Thermal finger-trail smear field (documented)
- `PART-29` شبكة نقاط تتأثر بجاذب / Dot-grid displacement around an attractor (seen)

### `PART-28` — حقل حراري يُلطخ بالإصبع / Thermal finger-trail smear field

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كتلة حرارية من ضوضاء مشوهة المجال عبر سلم حراري بسبع وقفات، وأثر مؤشر يسحبها كطلاء مبلل ثم تلتئم، وضغطة ترسل حلقة. / A heat-camera blob of domain-warped noise through a seven-stop ramp; a pointer trail drags it like wet paint and heals; a press sends a ripple ring.

**متى:** حين يريد مؤثر كاميرا حرارية يُلطخ بأثر الإصبع ثم يلتئم مع موجة عند الضغط / for a heat-camera blob smeared by a finger or pointer trail, with a ripple on press

**كيف:** Single WebGL1 fragment shader; 24 trail points (pos, velocity, age; life 1.6 s) as uniforms; disp += vel·smoothstep(r,0,d)·age; uv += disp·9. In video, script the finger as a Catmull-Rom path. Atlas reference HTML (needs a CDN panel) not rendered here.

**المعاملات:** fbm 5 oct; ramp 0/.12/.30/.45/.60/.78/1; smudge 9 (>14 tears); radius .17; ripple .18, bloom .55, .9 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حراري · thermal · smear · trail · shader · fluid · كاميرا حرارية · لمس الشاشة · تلطيخ · heat camera · finger trail

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/SKILL.md`
- `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/references/thermal-finger-trail.html`

#### 7. قدرات قريبة في العائلة

- `PART-26` تدفق الجسيمات على المسارات / Particle flow along routes & network edges (documented)
- `PART-27` طبقات التدفق في deck.gl / deck.gl flow layers (trips, arcs, hex) (install)
- `PART-29` شبكة نقاط تتأثر بجاذب / Dot-grid displacement around an attractor (seen)
- `PART-30` حزم موجات وشرائط خطوط / Noisy multi-trace waveform & line-ribbon waves (seen)

### `PART-29` — شبكة نقاط تتأثر بجاذب / Dot-grid displacement around an attractor

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة نقاط تُزاح بعيدًا عن جسم متحرك وتتلون بالمسافة، وسلسلة كرات تتبع القائد بتأخر. / Grid dots pushed away from a moving attractor and tinted by distance; a chain of balls follows the leader with lag.

**متى:** عند الحاجة لشبكة نقاط تبتعد عن جسم متحرك وتتلون بالمسافة، أو سلسلة كرات تتبعه / for a dot grid pushed away by a moving object, or a chain of balls following a leader

**كيف:** grid 24–28 px, falloff radius 160–200 px, spring back to rest; chain 15 balls lagging 2 frames each; inverse-square attraction (clamped) for hero pulls.

**المعاملات:** grid 24–28 px; radius 160–200 px; chain lag 2 frames

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** جاذب · شبكة نقاط · attractor · displacement · cursor field · تنافر · مؤشر · سلسلة كرات · repel · dot grid

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-chatgptastra-0d95c7`
- `kosif-tool/styles/pm-himanshutwtxs-5f4b43`
- `kosif-tool/playbooks/particles.md:28`
- `kosif-atlas/skills/342-kernel/1223-frontend/motion/cursor-field.md`

#### 7. قدرات قريبة في العائلة

- `PART-27` طبقات التدفق في deck.gl / deck.gl flow layers (trips, arcs, hex) (install)
- `PART-28` حقل حراري يُلطخ بالإصبع / Thermal finger-trail smear field (documented)
- `PART-30` حزم موجات وشرائط خطوط / Noisy multi-trace waveform & line-ribbon waves (seen)
- `PART-31` آثار الحركة والضوء / Motion trails from time-sampled history (ready)

### `PART-30` — حزم موجات وشرائط خطوط / Noisy multi-trace waveform & line-ribbon waves

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 15 خطًا عبر العرض = مجموع 3 جيوب + ضوضاء بمزج جمعي؛ أو 100–200 منحنى رفيع بتدرج برتقالي→أرجواني→أزرق. / 15 polylines = sum of 3 sines + simplex noise, additive; or 100–200 thin sine curves with an orange→magenta→blue gradient.

**متى:** حين تريد خطوطًا موجية متعددة كإشارة صوتية أو شرائط منحنيات متدرجة كخلفية / for multi-line noisy waveforms or gradient sine-line ribbons as a backdrop

**كيف:** Trace: amp 20–60 px, 200 points, alpha .25; ribbons: lineWidth .6, alpha .3, 3–4 bands; parallax wave layers 1 : .6 : .3, amp 10–30 px.

**المعاملات:** 15 traces; 100–200 ribbons

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** موجات · waveform · ribbons · lines · audio · موجة صوتية · منحنيات · خلفية · sine waves · gradient lines

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-rneayan-ea6129`
- `kosif-tool/styles/pm-jasonzhou1993-8595e0`
- `kosif-tool/styles/pm-faroukzy-9ff23e`

#### 7. قدرات قريبة في العائلة

- `PART-28` حقل حراري يُلطخ بالإصبع / Thermal finger-trail smear field (documented)
- `PART-29` شبكة نقاط تتأثر بجاذب / Dot-grid displacement around an attractor (seen)
- `PART-31` آثار الحركة والضوء / Motion trails from time-sampled history (ready)
- `PART-32` مطر motion-kit / MOTION.rain (seeded SVG/DOM rain) (proven)

### `PART-31` — آثار الحركة والضوء / Motion trails from time-sampled history

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل متحرك يُرسم K مرة في أزمنة أسبق بحجم وشفافية متناقصين؛ أو ذيل مدبب يقل عرضه نحو الطرف. / Each mover is drawn K times at slightly earlier times with shrinking size and alpha; or a tapered tail whose width falls toward the end.

**متى:** عند إضافة ذيل أو أثر ضوئي خلف جسم متحرك كمذنب أو طائرة مسيّرة / for adding a fading trail or light streak behind moving objects like comets or drones

**كيف:** for k < K: position at t − k·dt; head size 3.4–4.2, tail 2.2–2.6·(1 − k/K), alpha .55–.7·(1 − k/K); egypt-2120: 36 drones × 16 samples (dt .045), 9 lanes × 30 taxis × 14 (dt .03); tapered trail ~.3 s, width 6→0 px; ribbons: last 60 wingtip positions, alpha .8→0.

**المعاملات:** K 12–16; dt .03–.045 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أثر · ذيل · trail · light trail · comet · history · ذيل ضوئي · مذنب · أثر الحركة · motion trail · afterimage

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-one/projects/egypt-2120-animation/index.html`

#### 7. قدرات قريبة في العائلة

- `PART-29` شبكة نقاط تتأثر بجاذب / Dot-grid displacement around an attractor (seen)
- `PART-30` حزم موجات وشرائط خطوط / Noisy multi-trace waveform & line-ribbon waves (seen)
- `PART-32` مطر motion-kit / MOTION.rain (seeded SVG/DOM rain) (proven)
- `PART-33` بخار motion-kit / MOTION.vapour (steam puffs) (proven)

### `PART-32` — مطر motion-kit / MOTION.rain (seeded SVG/DOM rain)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | GSAP standard no-charge license (vendored). |

**ما هي:** خطوط مطر مائلة ببذرة بطول وعرض وسرعة لكل قطرة، تظهر وتخبو مع الحاوية. / Seeded slanted rain streaks (SVG lines or divs) with per-drop length/width/speed and container fades.

**متى:** لما يطلب المستخدم مطرًا بسيطًا مائلًا فوق مشهد SVG أو عناصر الصفحة / when the user wants simple slanted rain over an SVG or DOM scene

**كيف:** MOTION.rain(tl, container, {n, x0..y1, fall, len, angle, color, at, dur, seed}). Rendered here. Gotcha found here: each drop starts at at − dur + delay, so use at ≥ fall (~.6 s) or the first drops sit above the frame.

**المعاملات:** n 240; fall .55 s; len 46 px (×.6–1.4); width 1–2.6 px; angle −8°; rgba(220,235,255,.75); fade .6/.8 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مطر · rain · motion-kit · svg · weather · أمطار · شتا · قطرات · rainfall · rain streaks

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-studio/motion/kit/motion-kit.js:265`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:265`

#### 7. قدرات قريبة في العائلة

- `PART-30` حزم موجات وشرائط خطوط / Noisy multi-trace waveform & line-ribbon waves (seen)
- `PART-31` آثار الحركة والضوء / Motion trails from time-sampled history (ready)
- `PART-33` بخار motion-kit / MOTION.vapour (steam puffs) (proven)
- `PART-34` تلألؤ ونجوم / MOTION.sparkle & star twinkle (proven)

### `PART-33` — بخار motion-kit / MOTION.vapour (steam puffs)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** دوائر ببذرة تصعد وتكبر وتنجرف وتخبو كبخار أو دخان أو نفَس. / Seeded circles that rise, grow, drift and fade like steam, smoke or breath.

**متى:** حين تحتاج بخارًا يتصاعد من كوب أو دخانًا خفيفًا أو أنفاسًا تخرج وتتلاشى / for rising steam from a cup, light smoke or breath that drifts and fades

**كيف:** MOTION.vapour(tl, svgGroup, {n, r, rise, height, drift, spread, color, at, dur, x0, x1, y0, seed}); rendered here over #2b3a55. Wisp variant: 9-point polylines x + 14 sin(y/60 + 5t + x) rising 420 px, opacity sin(πp)·.9; coffee curls: 3 thin bezier strokes rising 40 px/s fading .4→0, loop 3 s.

**المعاملات:** n 70; r 18 px; rise 2.6 s; height 320 px; drift 120 px; scale .5→1.4

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بخار · دخان · vapour · steam · smoke · قهوة · كوب ساخن · أنفاس · coffee steam · breath

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-studio/motion/kit/motion-kit.js:283`
- `kosif-one/projects/water-cycle-animation/index.html`

#### 7. قدرات قريبة في العائلة

- `PART-31` آثار الحركة والضوء / Motion trails from time-sampled history (ready)
- `PART-32` مطر motion-kit / MOTION.rain (seeded SVG/DOM rain) (proven)
- `PART-34` تلألؤ ونجوم / MOTION.sparkle & star twinkle (proven)
- `PART-35` غبار طافٍ وحقل عمق / Drifting dust motes & depth field (proven)

### `PART-34` — تلألؤ ونجوم / MOTION.sparkle & star twinkle

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط ببذرة تتلألأ (شفافية ذهاب وإياب) عبر منطقة: نجوم، غبار، سحر. / Seeded dots twinkling (yoyo opacity) across a region: stars, dust, magic.

**متى:** عند الحاجة لنجوم أو غبار سحري يلمع ويخفت في منطقة من المشهد / for twinkling stars, dust or magic sparkles across a region of the scene

**كيف:** MOTION.sparkle(tl, group, {n, x0..y1, color, at, seed}); rendered here (#ffe9b8). Canvas variant: alpha = .5 + .5 sin(t·(3 + .2f) + f), cross sparkles for the brightest, washed out near the moon.

**المعاملات:** n 40; r 1–3.2 px; opacity .15↔1 over .6–1.8 s; 40 repeats; sine.inOut

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تلألؤ · نجوم · sparkle · twinkle · stars · لمعان · سحر · بريق · glitter · magic

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-studio/motion/kit/motion-kit.js:300`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:66`

#### 7. قدرات قريبة في العائلة

- `PART-32` مطر motion-kit / MOTION.rain (seeded SVG/DOM rain) (proven)
- `PART-33` بخار motion-kit / MOTION.vapour (steam puffs) (proven)
- `PART-35` غبار طافٍ وحقل عمق / Drifting dust motes & depth field (proven)
- `PART-36` أنظمة Basma الخمسة / Basma particle overlays (dust, bokeh, sparks, snow, confetti) (install)

### `PART-35` — غبار طافٍ وحقل عمق / Drifting dust motes & depth field

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط صغيرة مضيئة تنجرف وتتمايل بسرعات وشفافيات متفاوتة — تعطي الهواء جسمًا خلف الواجهات والنصوص. / Small luminous dots drifting and bobbing at staggered speeds/opacities — body for the air behind UI and text.

**متى:** حين تبدو الخلفية فارغة وتحتاج ذرات غبار مضيئة تطفو لتعطي الهواء عمقًا خلف النص / when an empty backdrop needs floating luminous dust to give depth behind text

**كيف:** Proof: 110 dust motes in proofs/arabic-voice-kinetic. Recipes: studio 38 motes x = (137.3i + t·(5 + i%3)) mod w, y = (sin(2.71i + .18t)·.42 + .5)·h; fastify 26 golden-ratio dots (k·.618 mod 1) ±15/±20 px; depth: 40–80 dots, size 2–6 px, 5–15 px/s, varied blur; over footage: warm radial dots screen-blended, rising and fading in 1.6 s.

**المعاملات:** 26–110 motes; 5–15 px/s; alpha .07–.48

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** غبار · dust · motes · atmosphere · depth · ذرات · جو · خلفية · floating particles · ambience

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:69`
- `fastify-motion-bro/web/motion.js:11`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:157`

#### 7. قدرات قريبة في العائلة

- `PART-33` بخار motion-kit / MOTION.vapour (steam puffs) (proven)
- `PART-34` تلألؤ ونجوم / MOTION.sparkle & star twinkle (proven)
- `PART-36` أنظمة Basma الخمسة / Basma particle overlays (dust, bokeh, sparks, snow, confetti) (install)
- `PART-37` مطر بطبقتين وبرك ورذاذ / Two-layer parallax rain, puddle ripples & splashes (proven)

### `PART-36` — أنظمة Basma الخمسة / Basma particle overlays (dust, bokeh, sparks, snow, confetti)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** طبقات جسيمات حتمية في محرر Basma كدالة للزمن: غبار صاعد، بوكيه، شرر، ثلج، قصاصات. / Deterministic overlays in the Basma editor: rising dust, bokeh, sparks, snow, confetti — pure functions of time.

**متى:** عند إضافة طبقة جسيمات جاهزة في محرر Basma: غبار أو بوكيه أو شرر أو ثلج أو قصاصات / for adding a ready particle overlay in the Basma editor: dust, bokeh, sparks, snow or confetti

**كيف:** drawParticles(): dust 54 dots rising 1.8%/s twinkle .18–.48; bokeh 16 screen discs 3–10% m alpha .08–.15; sparks 54 accent dots rising 12%/s "lighter"; snow 54 falling 6%/s; confetti 46 flips falling 16%/s; rnd(i) = frac(sin(127.1i + 311.7)·43758.5453).

**المعاملات:** dust\|bokeh\|sparks\|confetti\|snow

**التثبيت:** cd app && npm install

**الوسوم:** basma · bokeh · snow · sparks · confetti · dust · طبقة جسيمات · غبار · ثلج · قصاصات · particle overlay

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `app/public/js/00_editor.js:234`

#### 7. قدرات قريبة في العائلة

- `PART-34` تلألؤ ونجوم / MOTION.sparkle & star twinkle (proven)
- `PART-35` غبار طافٍ وحقل عمق / Drifting dust motes & depth field (proven)
- `PART-37` مطر بطبقتين وبرك ورذاذ / Two-layer parallax rain, puddle ripples & splashes (proven)
- `PART-38` مطر الرسام بطبقات وضوء نار / Painted rain with exposure smear (Studio) (ready)

### `PART-37` — مطر بطبقتين وبرك ورذاذ / Two-layer parallax rain, puddle ripples & splashes

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مطر بعيد رفيع كثير بطيء، وقريب سميك قليل سريع بإزاحة بارالاكس، وحلقات برك إهليلجية ورذاذ بالستي عند كل خطوة. / Far rain (many, thin, slow) and near rain (few, thick, fast) with parallax; elliptical puddle ripples and ballistic splash droplets at each footfall.

**متى:** حين يطلب مشهد مطر بعمق بطبقتين وبركًا تتموج ورذاذًا يتطاير مع كل خطوة / for deep two-layer parallax rain with rippling puddles and splashes at each footstep

**كيف:** far 152 drops 340–600 px/s, 11–25 px, #86b7c9 .8 px α .13, parallax .03; near 32 drops 630 px/s 37 px #95d6df 1.3 px α .17 parallax .1; wrap 1450×850; 20 ripples rx 5→29 ry 1→5; 11 droplets/event vx ±105, vy −45…−129, g 145 px/s², life .63 s. midnight_cat frame rendered here via window.seek; proofs/neon-glow adds 90 streaks + puddle rings.

**المعاملات:** 152 + 32 drops; 11 droplets × .63 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مطر · برك · rain · puddle · splash · parallax · رذاذ · تموجات · خطوات · ripples · footsteps

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:108`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:108`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/README.md`

#### 7. قدرات قريبة في العائلة

- `PART-35` غبار طافٍ وحقل عمق / Drifting dust motes & depth field (proven)
- `PART-36` أنظمة Basma الخمسة / Basma particle overlays (dust, bokeh, sparks, snow, confetti) (install)
- `PART-38` مطر الرسام بطبقات وضوء نار / Painted rain with exposure smear (Studio) (ready)
- `PART-39` مطر وضباب ومطر الغيمة / Rain + fog bands; cloud rain with splash rings (seen)

### `PART-38` — مطر الرسام بطبقات وضوء نار / Painted rain with exposure smear (Studio)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خطوط مائلة بطبقتي عمق وطبقة دافئة مضاءة بالنار ثم تمويه حركي اتجاهي. / Slanted strokes in two depth layers, a warm fire-lit layer, then directional motion blur.

**متى:** عند رسم مطر بطبقات عمق يضيئه وهج نار دافئ ثم تمويه حركي في Studio / for painted rain in depth layers lit by warm firelight, then motion blur, in Studio

**كيف:** rain(seed, n, x0, x1, y0, y1, length, width, slant=−.25) → stroke(); colours #a8bbd4/.15, #cddcef/.2, fire-lit #ffb066 add; then motion_blur.

**المعاملات:** 520 + 150 + 160 streaks; lengths 24/60/36

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مطر · رسام · rain · studio · painted · وهج النار · تمويه حركي · رسم · motion blur · firelight

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-studio/scenes/whale_dragon.py:55`
- `kosif-studio/scenes/duck_dragon.py:24`

#### 7. قدرات قريبة في العائلة

- `PART-36` أنظمة Basma الخمسة / Basma particle overlays (dust, bokeh, sparks, snow, confetti) (install)
- `PART-37` مطر بطبقتين وبرك ورذاذ / Two-layer parallax rain, puddle ripples & splashes (proven)
- `PART-39` مطر وضباب ومطر الغيمة / Rain + fog bands; cloud rain with splash rings (seen)
- `PART-40` جسيمات موسمية وبتلات / Seasonal particles & falling petals (ready)

### `PART-39` — مطر وضباب ومطر الغيمة / Rain + fog bands; cloud rain with splash rings

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 300–500 خط مطر مائل 10–15° مع 2–3 أشرطة ضباب مموهة تنجرف؛ أو شرطات زرقاء تسقط من بصمة الغيمة وتولد حلقات عند الأرض. / 300–500 streaks at 10–15° with 2–3 blurred fog bands drifting; or blue dashes falling from a cloud footprint spawning ground rings.

**متى:** حين يحتاج المشهد مطرًا مع ضباب منجرف، أو غيمة تمطر وتصنع حلقات على الأرض كدورة الماء / for rain with drifting fog bands, or a cloud raining with ground rings as in a water cycle

**كيف:** Streak alpha .25–.4, length 12–24 px; doodle: 40–60 streaks, fall 600–900 ms, ring 300 ms; loop 38 drops at 950 px/s below the cloud base (water-cycle).

**المعاملات:** 300–500 streaks; fog 2–3 bands

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ضباب · مطر · fog · rain · cloud · غيمة · شبورة · دورة الماء · mist · water cycle

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-kamstudiolabs-0b0824`
- `kosif-tool/styles/doodle`
- `kosif-one/projects/water-cycle-animation/index.html`

#### 7. قدرات قريبة في العائلة

- `PART-37` مطر بطبقتين وبرك ورذاذ / Two-layer parallax rain, puddle ripples & splashes (proven)
- `PART-38` مطر الرسام بطبقات وضوء نار / Painted rain with exposure smear (Studio) (ready)
- `PART-40` جسيمات موسمية وبتلات / Seasonal particles & falling petals (ready)
- `PART-41` ثلج وحقل نجوم HyperFrames / HyperFrames snow & starfield blocks (install)

### `PART-40` — جسيمات موسمية وبتلات / Seasonal particles & falling petals

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بتلات وأوراق وثلج تنجرف قطريًا مع الريح؛ وبتلات ورد تسقط وتتمايل وتدور كدالة للزمن وحده. / Blossoms, leaves and snow drifting diagonally with the wind; rose petals falling, swaying and spinning as a function of t alone.

**متى:** عند طلب بتلات ورد أو أوراق خريف أو ثلج تتساقط وتتمايل مع الريح / when rose petals, leaves or snow should fall and sway with the wind

**كيف:** 22 petals from M.rng(11): period 7–12 s, y = −60 + 2050·((t/dur + ph) % 1), x += drift·u (±170) + sin(1.3t + 9ph)·(20–50), rotate ±300–700°·u, #e8436a/#f27b93 .9; seasonal: 60–150 particles, vx −100…−300 px/s, sway 10 px; chalk dust: dots from the drawing tip fall with g ~400 px/s² fading .5 s.

**المعاملات:** 22 petals; 7–12 s periods

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بتلات · ثلج · أوراق · petals · snow · leaves · seasonal · ورد · خريف · تساقط · falling leaves · blossoms

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-one/projects/thursday-dua-animation/source/index.html`

#### 7. قدرات قريبة في العائلة

- `PART-38` مطر الرسام بطبقات وضوء نار / Painted rain with exposure smear (Studio) (ready)
- `PART-39` مطر وضباب ومطر الغيمة / Rain + fog bands; cloud rain with splash rings (seen)
- `PART-41` ثلج وحقل نجوم HyperFrames / HyperFrames snow & starfield blocks (install)
- `PART-42` ثلج وجمر على المعالج الرسومي / GPU snow / ember point sprites (ready)

### `PART-41` — ثلج وحقل نجوم HyperFrames / HyperFrames snow & starfield blocks

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0. |

**ما هي:** ثلج آمن للبحث بحجم وسرعة وشفافية مترابطة للعمق وقناع يبقي المركز صافيًا؛ وسماء بثلاث طبقات أحجام تتلألأ في طبقتي بارالاكس. / Seek-safe snow with size/speed/opacity correlated for depth and a radial mask keeping the centre clear; a night sky with three size tiers twinkling in two parallax layers.

**متى:** حين تريد ثلجًا متساقطًا بعمق يترك المنتصف صافيًا أو سماء ليلية بنجوم تتلألأ / for depth-correct falling snow that keeps the centre clear, or a twinkling night sky

**كيف:** npx hyperframes add snow (density sparse\|dense, speed calm\|gust, 6 s) \| starfield (tone warm\|cool\|white, speed slow\|fast).

**التثبيت:** npx hyperframes add snow

**الوسوم:** ثلج · نجوم · snow · starfield · hyperframes · سماء ليلية · شتاء · تساقط الثلج · night sky · snowfall

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-one/vendor/hyperframes/registry/blocks/snow/snow.html`
- `kosif-one/vendor/hyperframes/registry/blocks/starfield/starfield.html`

#### 7. قدرات قريبة في العائلة

- `PART-39` مطر وضباب ومطر الغيمة / Rain + fog bands; cloud rain with splash rings (seen)
- `PART-40` جسيمات موسمية وبتلات / Seasonal particles & falling petals (ready)
- `PART-42` ثلج وجمر على المعالج الرسومي / GPU snow / ember point sprites (ready)
- `PART-43` ذرات صاعدة وحلقات الركلة / Rising motes + kick rings (verse) (ready)

### `PART-42` — ثلج وجمر على المعالج الرسومي / GPU snow / ember point sprites

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط تسقط وتتمايل وتخبو مع العمق بمزج جمعي — ثلج للأزرق وجمر دافئ للبني. / Point sprites that fall, sway and fade with depth, additively blended — snow for cobalt, embers for ledger.

**متى:** عند الحاجة لثلج أو جمر في مشهد ثلاثي الأبعاد يسقط ويتمايل ويخفت مع العمق / for 3D snow or embers as point sprites that fall, sway and fade with depth

**كيف:** Vertex: y = mod(y − t·(.25 + .15 size), 16) − 8; x += .25 sin(.6t + 3.1z + 7 size); pointSize = (1.5 + 3.5 size)·dpr·clamp(10/d, .2, 2.5); alpha clamp(1.2 − d/22, .05, .8); fragment round sprite, smoothstep; blend ONE,ONE, depthMask false. Pass t from the frame.

**المعاملات:** 160 (phone) / 360 (desktop); field 24×16×(2..20)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ثلج · جمر · gpu · point sprites · webgl · snow · embers · ثلاثي الأبعاد · شيدر · توهج · 3d particles · additive blend

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-earth-ci-fork/ui/art/crystal-world.js:65`
- `kosif-earth-ci-fork/ui/art/crystal-world.js:149`

#### 7. قدرات قريبة في العائلة

- `PART-40` جسيمات موسمية وبتلات / Seasonal particles & falling petals (ready)
- `PART-41` ثلج وحقل نجوم HyperFrames / HyperFrames snow & starfield blocks (install)
- `PART-43` ذرات صاعدة وحلقات الركلة / Rising motes + kick rings (verse) (ready)
- `PART-44` هالة شعاعية وجسيمات صاعدة / Radial aura + drifting particle canvas (ready)

### `PART-43` — ذرات صاعدة وحلقات الركلة / Rising motes + kick rings (verse)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 72 ذرة ضوء تصعد وتتلألأ وترتفع مع البدايات الصوتية، وكل ركلة طبل ترسل حلقة تتسع 1.3 ث. / 72 light motes rise and twinkle, lifted by onsets; each kick sends an expanding ring for 1.3 s.

**متى:** حين تريد ذرات ضوء تتصاعد مع الصوت وحلقات تتسع مع كل ضربة طبل / when light motes should rise with the audio and rings pulse on each kick drum

**كيف:** verse.html draw(t) with SOUND.kicks; "lighter"; motes r 2–9 px, speed .006–.026/s; ring radius (.16 + .42·dt)·min(W,H), alpha .22·(1 − dt/1.3)². Audio-driven variant proven in proofs/audio-reactive-spectrum (90 seeded particles, onset shockwaves .7 s).

**المعاملات:** 72 motes; ring 1.3 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ذرات · ركلة · motes · kick · beat · audio reactive · طبل · إيقاع · تفاعل مع الصوت · kick drum · pulse rings

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `100-superskills/skills/kosif-montage-motion/templates/verse.html:153`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/audio-reactive-spectrum/README.md`

#### 7. قدرات قريبة في العائلة

- `PART-41` ثلج وحقل نجوم HyperFrames / HyperFrames snow & starfield blocks (install)
- `PART-42` ثلج وجمر على المعالج الرسومي / GPU snow / ember point sprites (ready)
- `PART-44` هالة شعاعية وجسيمات صاعدة / Radial aura + drifting particle canvas (ready)
- `PART-45` خلفيات هادئة حلقية / Ambient background loops (MG-111/113/114) (documented)

### `PART-44` — هالة شعاعية وجسيمات صاعدة / Radial aura + drifting particle canvas

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خلفية Canvas بتوهج شعاعي كهرماني/سماوي وعشرات النقاط تصعد وتلتف. / A Canvas background with a soft amber/sky radial glow and dozens of dots drifting upward and wrapping.

**متى:** عند الحاجة لخلفية بسيطة بتوهج دائري ونقاط تصعد ببطء خلف المحتوى / for a simple backdrop with a soft radial glow and slowly rising dots

**كيف:** createRadialGradient(W/2,H/2,50,W/2,H/2,.7W) amber .15 / sky .08 / transparent; 60 particles y = (y0 − 40·speed·t) mod H at alpha .4; seed the RNG (mulberry32) — the template uses Math.random as shipped.

**المعاملات:** 60 particles r 2–6 px, 40–120 px/s, #f59e0b / #38bdf8

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هالة · aura · particles · background · canvas · توهج · خلفية بسيطة · نقاط صاعدة · radial glow · gradient

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/kinetic_2d.html:128`

#### 7. قدرات قريبة في العائلة

- `PART-42` ثلج وجمر على المعالج الرسومي / GPU snow / ember point sprites (ready)
- `PART-43` ذرات صاعدة وحلقات الركلة / Rising motes + kick rings (verse) (ready)
- `PART-45` خلفيات هادئة حلقية / Ambient background loops (MG-111/113/114) (documented)
- `PART-46` كرة جسيمات فيبوناتشي / Fibonacci particle sphere (proven)

### `PART-45` — خلفيات هادئة حلقية / Ambient background loops (MG-111/113/114)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كتلتان مموهتان تتباعدان وتعودان، ثلاثة خطوط موجية خلف عنوان بودكاست، وذرات ضوء تنجرف بأعماق مختلفة. / Two blurred blobs drift apart and back; three wavy lines behind a podcast title; light specks drifting at varied depth.

**متى:** حين تحتاج خلفية هادئة تتكرر بلا قفزة خلف بودكاست أو عنوان / for a calm, seamlessly looping background behind a podcast or title

**كيف:** 8 s / 8 s / 10 s loops; every speck cycle must divide the loop length; t mod period; tiny dither noise against banding; test gradients for banding after compression.

**المعاملات:** 8 / 8 / 10 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حلقة · خلفية · ambient loop · podcast · seamless · تكرار · لوب · هادئ · loop · calm background

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-loops-backgrounds.md`

#### 7. قدرات قريبة في العائلة

- `PART-43` ذرات صاعدة وحلقات الركلة / Rising motes + kick rings (verse) (ready)
- `PART-44` هالة شعاعية وجسيمات صاعدة / Radial aura + drifting particle canvas (ready)
- `PART-46` كرة جسيمات فيبوناتشي / Fibonacci particle sphere (proven)
- `PART-47` مجرة حلزونية / Spiral galaxy (differential rotation) (proven)

### `PART-46` — كرة جسيمات فيبوناتشي / Fibonacci particle sphere

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** N نقطة بالزاوية الذهبية على كرة، تدور وتُسقط بمنظور وتُرتب بالعمق، حجمها وشفافيتها بالعمق، وبعضها نقاط لهجة حمراء. / N golden-angle points on a sphere, rotated, perspective-projected, depth-sorted, size/alpha by z, a few red accent points.

**متى:** لما يطلب كرة أو كوكبًا من النقاط يدور بعمق، كرمز للذكاء الاصطناعي أو للعالم / when the user wants a rotating 3D sphere of points, e.g. an AI or globe motif

**كيف:** y = 1 − 2(i+.5)/N, r = √(1−y²), θ = 2.39996·i; rotate in y; f = 2.6/(3.2 − z); alpha .25 + .6·(z+1)/2. Rendered here (900 points). Gather/collapse: radius 0→R ease-out 1.5 s, R→0 ease-in .6 s into an origin dot; chips can pop at projected points.

**المعاملات:** N 600–3000; FOV ~42°; alpha by depth

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كرة · فيبوناتشي · fibonacci sphere · point cloud · globe · ai · كوكب · ذكاء اصطناعي · كرة أرضية · dot sphere · rotating sphere

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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
- `kosif-tool/styles/pm-kloss-xyz-b9b3f6`
- `kosif-tool/styles/pm-crazyalphaaa-bc7e75`

#### 7. قدرات قريبة في العائلة

- `PART-44` هالة شعاعية وجسيمات صاعدة / Radial aura + drifting particle canvas (ready)
- `PART-45` خلفيات هادئة حلقية / Ambient background loops (MG-111/113/114) (documented)
- `PART-47` مجرة حلزونية / Spiral galaxy (differential rotation) (proven)
- `PART-48` قفزة فضائية وخطوط سرعة / Hyperspace warp starfield (proven)

### `PART-47` — مجرة حلزونية / Spiral galaxy (differential rotation)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط على أذرع حلزونية لوغاريتمية ملونة حسب الذراع، تدور بسرعة زاوية ∝ 1/r فيلتف الداخل أسرع. / Points on log-spiral arms coloured by arm, rotating with angular speed ∝ 1/r so the core winds faster.

**متى:** عند طلب مجرة حلزونية دوارة أو مشهد فضائي بنقاط ملونة على أذرع / for a rotating spiral galaxy or a space scene of coloured points on arms

**كيف:** arm = i % 3, d = rand^.6, a = arm·2.094 + 4d + jitter; angle += t·.9/(d + .15); y squashed .55; additive. Rendered here (2500 points). HyperFrames spiral-galaxy: 20,000 GPU sprites, 3 arms, rate .25, glow 1.9, core #ffa575, rim #311599.

**المعاملات:** 2.5k–20k points; 2–3 arms; ω ∝ 1/r

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مجرة · galaxy · spiral · space · differential rotation · فضاء · كون · نجوم · cosmos · universe

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-one/vendor/hyperframes/registry/blocks/spiral-galaxy/spiral-galaxy.html`
- `kosif-tool/styles/pm-shneural-2abdfa`
- `kosif-tool/styles/pm-tolgayhickiran-e90799`

#### 7. قدرات قريبة في العائلة

- `PART-45` خلفيات هادئة حلقية / Ambient background loops (MG-111/113/114) (documented)
- `PART-46` كرة جسيمات فيبوناتشي / Fibonacci particle sphere (proven)
- `PART-48` قفزة فضائية وخطوط سرعة / Hyperspace warp starfield (proven)
- `PART-49` حلقة جسيمات وكوكبة / Particle torus & constellation (seen)

### `PART-48` — قفزة فضائية وخطوط سرعة / Hyperspace warp starfield

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ~600 نقطة بعمق z تُسقط x/z وy/z ويُرسم خط من الموضع السابق للحالي، والسرعة تقفز على الإسقاط الموسيقي. / ~600 points with depth; project x/z, y/z and draw a line from the previous to the current projection; speed ramps up on drops.

**متى:** حين يريد قفزة بسرعة الضوء أو نفقًا من النجوم، أو انتقالًا بين مشهدين على الدروب / for a light-speed star warp, a star tunnel, or a warp transition between scenes on a drop

**كيف:** Speed 2→30 units/frame; stroke 1 px #9db4ff α .6 (cap line width ~2.5 px); rendered here. Tunnel variant: 3000 points on a cylinder moving to camera as streaks with a dark centre; warp-star transition between scenes .8 s, streak 50–200 px.

**المعاملات:** ~600 stars; speed 2→30

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قفزة · فضاء · warp · hyperspace · speed lines · tunnel · سرعة الضوء · نفق نجوم · انتقال · light speed · scene transition

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-maxalexweber-67688b`
- `kosif-tool/styles/pm-leonkohli-6dc01b`
- `kosif-tool/styles/pm-nolkeeg-bf062e`

#### 7. قدرات قريبة في العائلة

- `PART-46` كرة جسيمات فيبوناتشي / Fibonacci particle sphere (proven)
- `PART-47` مجرة حلزونية / Spiral galaxy (differential rotation) (proven)
- `PART-49` حلقة جسيمات وكوكبة / Particle torus & constellation (seen)
- `PART-50` نقاط مضيئة ثلاثية جمعية / Additive glowing point sprites (three.js) (ready)

### `PART-49` — حلقة جسيمات وكوكبة / Particle torus & constellation

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط على سطح طارة تدور على محورين بشفافية بالعمق؛ أو نجوم عشوائية تتصل خطوطها بالأقرب تحت هالة بنفسجية. / Points on a torus rotating on two axes with depth alpha; or random stars linked to near neighbours under a violet haze.

**متى:** عند الحاجة لحلقة نقاط دوارة أو نجوم تتصل بخطوط كشبكة كوكبة / for a rotating torus of points or stars linked by lines like a constellation

**كيف:** Torus R 1, r .35, 2000 points, red accent subset; constellation: connect pairs with d < 90 px, line alpha ∝ 1 − d/90.

**المعاملات:** 2000 pts; link < 90 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** طارة · كوكبة · torus · constellation · network · نجوم متصلة · خطوط · شبكة اتصال · connected dots · star map

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-roundtablespace-d3a1be`
- `kosif-tool/styles/pm-codestackr-c071bf`
- `kosif-tool/styles/pm-dale-vaz-cc612a`

#### 7. قدرات قريبة في العائلة

- `PART-47` مجرة حلزونية / Spiral galaxy (differential rotation) (proven)
- `PART-48` قفزة فضائية وخطوط سرعة / Hyperspace warp starfield (proven)
- `PART-50` نقاط مضيئة ثلاثية جمعية / Additive glowing point sprites (three.js) (ready)
- `PART-51` جسيمات GPU بمئة ألف / GPU particles: FBO ping-pong & TSL compute (100k+) (install)

### `PART-50` — نقاط مضيئة ثلاثية جمعية / Additive glowing point sprites (three.js)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مئات النقاط المضيئة في حجم تدور ببطء حول البطل، بتلاشٍ ناعم من gl_PointCoord. / Hundreds of glowing points scattered in a volume, slowly rotating around the hero, with a gl_PointCoord falloff.

**متى:** حين يحتاج مشهد ثلاثي الأبعاد مئات النقاط المتوهجة تدور ببطء حول العنصر الرئيسي / when a 3D scene needs hundreds of glowing points slowly orbiting the hero

**كيف:** cinematic_3d: 400 positions in a 20×25×20 box; PointsMaterial #38bdf8 size .08 opacity .75 AdditiveBlending; rotation.y = .08t. Shader version: s = pow(1 − distance(gl_PointCoord, .5), 3), depthWrite false, 5000 points ±2.

**المعاملات:** 400–5000 points; falloff power 3

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نقاط مضيئة · point sprites · additive · three.js · sparkle · توهج · ثلاثي الأبعاد · جسيمات · glow · floating lights

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:165`
- `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `PART-48` قفزة فضائية وخطوط سرعة / Hyperspace warp starfield (proven)
- `PART-49` حلقة جسيمات وكوكبة / Particle torus & constellation (seen)
- `PART-51` جسيمات GPU بمئة ألف / GPU particles: FBO ping-pong & TSL compute (100k+) (install)
- `PART-52` دوامة وشفط وشظايا طافية / Particle vortex, suck-in & floating shards (seen)

### `PART-51` — جسيمات GPU بمئة ألف / GPU particles: FBO ping-pong & TSL compute (100k+)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خزّن مواقع الجسيمات في خامة عائمة وحدّثها في تمريرة محاكاة (FBO)، أو بمخازن حوسبة في WebGPU TSL — لمئة ألف جسيم وأكثر. / Store positions in a float texture updated in a simulation pass (FBO ping-pong), or in WebGPU TSL storage buffers — 100k+ particles.

**متى:** عند الحاجة لمحاكاة مئة ألف جسيم أو أكثر على كرت الشاشة / when you need to simulate 100k+ particles on the GPU

**كيف:** DataTexture RGBA float → SimulationMaterial → WebGLRenderTarget (two, ping-pong) → points read uPositions; TSL: instancedArray(N,"vec3"), Fn(…)().compute(N), renderer.compute(update). Seed initial positions; for video advance exactly one step per frame. WebGPU unverified here — FBO on WebGL is the safe path.

**المعاملات:** N 100k; gravity −9.8, bounce .7, friction .98

**التثبيت:** npm i three

**الوسوم:** GPU · FBO · compute · 100k · webgpu · tsl · كرت الشاشة · عدد ضخم · محاكاة · webgl · ping-pong

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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
- `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/examples/particle-system.js`

#### 7. قدرات قريبة في العائلة

- `PART-49` حلقة جسيمات وكوكبة / Particle torus & constellation (seen)
- `PART-50` نقاط مضيئة ثلاثية جمعية / Additive glowing point sprites (three.js) (ready)
- `PART-52` دوامة وشفط وشظايا طافية / Particle vortex, suck-in & floating shards (seen)
- `PART-53` نفث النار بطبقات / Layered fire breath (ready)

### `PART-52` — دوامة وشفط وشظايا طافية / Particle vortex, suck-in & floating shards

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** 3000 نقطة على حلزون زاويتها تزيد k/r، أو بطاقات تلتف نحو البطل وهي تصغر، أو شظايا نيون تطفو وتدور في المقدمة. / 3k points on a spiral with angle += k/r; cards spiralling into the hero while shrinking; neon shards drifting and spinning in the foreground.

**متى:** حين يريد دوامة جسيمات أو عناصر تُشفط نحو البطل وهي تصغر، أو شظايا نيون طافية / for a particle vortex, items sucked into the hero, or floating neon shards

**كيف:** Suck-in 300–500 ms easeInCubic, rotation 90–180°, radial scribble lines; shards ~40 instanced, .5 rad/s, size for depth of field.

**المعاملات:** 3k pts; suck 300–500 ms; 40 shards

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** دوامة · vortex · suck in · shards · spiral · شفط · إعصار · نيون · whirlpool · swirl

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-3xtihor-0f6911`
- `kosif-tool/styles/pm-ik-builds-b8bdcf`
- `kosif-tool/styles/pm-gorden-sun-041f56`

#### 7. قدرات قريبة في العائلة

- `PART-50` نقاط مضيئة ثلاثية جمعية / Additive glowing point sprites (three.js) (ready)
- `PART-51` جسيمات GPU بمئة ألف / GPU particles: FBO ping-pong & TSL compute (100k+) (install)
- `PART-53` نفث النار بطبقات / Layered fire breath (ready)
- `PART-54` جمر ودخان وتعتيم / Embers, sparks & smoke atmosphere (ready)

### `PART-53` — نفث النار بطبقات / Layered fire breath

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نار من أنابيب لهب جمعية من الأحمر إلى الأبيض بتمايل ببذرة وانحناء، مع مخروط توهج وألسنة ملتفة ورذاذ اصطدام. / Fire as stacked additive flame tubes red→white with seeded wobble and bend, a wide glow cone, curling tongues and an impact splash.

**متى:** لما يطلب نارًا أو نفث لهب من تنين مع توهج ورذاذ عند الاصطدام / when the user wants fire breath or flames from a dragon, with a glow cone and impact splash

**كيف:** Studio: flame(seed, a, b, r0, r1, wob, bend) — 7 red #ff3d0a (.5, blur 3), 5 orange #ff9326 (.65, 2.4), 3 yellow #ffe7a2 (.85), 1 white (.75), all mode "add", radius tapers t^.75·(1 − .55t^6). SVG (duck_dragon.py): outer #dc2626 + blur20 #f97316, mid #f97316, core #fde68a, hot #fffbeb blur 8, 12 tongues, splash fan every 20°.

**المعاملات:** 16 tubes in 4 colours; splash ±80° every 20°

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نار · لهب · fire · flame · dragon · تنين · حريق · نفث النار · fire breath · burning

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-studio/scenes/dragon_girl.py:108`
- `kosif-studio/scenes/whale_dragon.py:247`
- `kosif-one/projects/duck-vs-dragon/duck_dragon.py`

#### 7. قدرات قريبة في العائلة

- `PART-51` جسيمات GPU بمئة ألف / GPU particles: FBO ping-pong & TSL compute (100k+) (install)
- `PART-52` دوامة وشفط وشظايا طافية / Particle vortex, suck-in & floating shards (seen)
- `PART-54` جمر ودخان وتعتيم / Embers, sparks & smoke atmosphere (ready)
- `PART-55` شرر على ساعة الشريط / Event sparks on the tape clock (three-kit) (install)

### `PART-54` — جمر ودخان وتعتيم / Embers, sparks & smoke atmosphere

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شرر ببذرة بأربعة ألوان نار، ودخان من قطوع مموهة كبيرة، وجمر على مسار النار يطفو للأعلى بعيدًا عن وجه البطل. / Seeded embers in four fire colours, large blurred smoke ellipses, and sparks scattered along the fire path drifting up, kept off the hero’s face.

**متى:** عند إضافة جو من الشرر والدخان والجمر المتطاير حول مشهد نار / for adding drifting embers, sparks and smoke atmosphere around a fire scene

**كيف:** duck_dragon: 110 embers r ∈ {1.2…3.8}, #fde047 #fbbf24 #fb923c #f97316 .55–1; 9 smoke ellipses rx 120–260 ry 18–40 .16 blur 20; vignette r 950 to black .6. Studio: dots(emb) #ffd27a .9 add + halos ×3 #ff7a2a .45 blur 2.4, order "sparkle"; Gaussian σ 36–44 px along the path, lift ≤ 100.

**المعاملات:** 110–440 embers; smoke .16 blur 20

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** جمر · دخان · embers · smoke · sparks · شرار · تعتيم · أجواء نار · vignette · fire atmosphere

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-one/projects/duck-vs-dragon/duck_dragon.py`
- `kosif-studio/scenes/dragon_girl.py:408`
- `kosif-studio/scenes/whale_dragon.py:282`

#### 7. قدرات قريبة في العائلة

- `PART-52` دوامة وشفط وشظايا طافية / Particle vortex, suck-in & floating shards (seen)
- `PART-53` نفث النار بطبقات / Layered fire breath (ready)
- `PART-55` شرر على ساعة الشريط / Event sparks on the tape clock (three-kit) (install)
- `PART-56` بخار وغيوم من عناقيد بيضاوية / Ellipse-cluster clouds, smoke & steam (Studio) (ready)

### `PART-55` — شرر على ساعة الشريط / Event sparks on the tape clock (three-kit)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شرر جمعي يُقذف عند الأحداث الصوتية ويتحرك على ساعة الشريط، فيعلق في الهواء حين يتوقف المسار. / Additive sparks thrown at sound events that move on the tape clock, so they hang in the air when the track stops.

**متى:** حين يُقذف الشرر مع الأحداث الصوتية ويجب أن يتجمد في الهواء عند توقف الشريط / when sparks fired on sound events must hang mid-air as the track stops

**كيف:** K3.makeSparks([{t,x,y,z}], {per, speed, gravity, drift, color, size, seed}); userData.set(t, tapeFn). sound_ground: per 90, speed 6.5, gravity 7, drift 15 m/s, 2400 slow embers 0xff9a5a. Break variant: 26 sparks ballistic from a midpoint + torus flash ring red→green on repair. The demo project loads assets/main.bundle.js, which is not built in this checkout (koi_pond threw a load error here) — install esbuild and bundle first; the kit functions themselves ship in the prebuilt three-kit.bundle.js.

**المعاملات:** per 60; speed 5; gravity 6; life .5–1.6 s; #ffa040

**التثبيت:** cd 100-superskills/skills/kosif-montage-motion/scripts && npm install three@0.186.1 esbuild && python3 motion.py bundle sound_ground

**الوسوم:** شرر · sparks · tape stop · beat · three.js · توقف الصوت · تجميد · إيقاع · tape clock · freeze

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

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-studio/motion/kit/three-kit.js:886`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:56`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:93`

#### 7. قدرات قريبة في العائلة

- `PART-53` نفث النار بطبقات / Layered fire breath (ready)
- `PART-54` جمر ودخان وتعتيم / Embers, sparks & smoke atmosphere (ready)
- `PART-56` بخار وغيوم من عناقيد بيضاوية / Ellipse-cluster clouds, smoke & steam (Studio) (ready)
- `PART-57` رذاذ وزبد وانهمار ماء / Spray, foam & water sheeting (ready)

### `PART-56` — بخار وغيوم من عناقيد بيضاوية / Ellipse-cluster clouds, smoke & steam (Studio)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عناقيد قطوع ببذرة مستدقة الأطراف تُقرأ غيمًا حين تموّه، ونسخ مزاحة بمزج screen/add لقمم مقمرة وبطون مضاءة بالنار، وبخار عند تصادم نار وماء. / Seeded tapered ellipse clusters read as clouds when blurred; offset screen/add copies give moonlit tops and fire-lit bellies; steam where fire meets water.

**متى:** عند رسم غيوم أو دخان أو بخار في Studio بإضاءة القمر أو النار، أو بخار حيث تلتقي نار وماء / for painting clouds, smoke or steam in Studio lit by moon or fire, or steam where fire meets water

**كيف:** cloud(cx, cy, w, h, n, seed) + fill(blur 12–20) + translated fill(mode "screen"\|"add"); steam: #d6dde6 .45 blur 12 screen + noise .5 cell 20 + translate 14 #ff8a3a .32 add + glow #fff0c0 26 .7 + 6 tongues.

**المعاملات:** ellipse w .07–.16, h .3–.6; blur 13–17

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** غيوم · بخار · clouds · steam · smoke · studio · سحاب · ضوء القمر · رسم · moonlit · cloud painting

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-studio/scenes/dragon_girl.py:36`
- `kosif-studio/scenes/whale_dragon.py:257`

#### 7. قدرات قريبة في العائلة

- `PART-54` جمر ودخان وتعتيم / Embers, sparks & smoke atmosphere (ready)
- `PART-55` شرر على ساعة الشريط / Event sparks on the tape clock (three-kit) (install)
- `PART-57` رذاذ وزبد وانهمار ماء / Spray, foam & water sheeting (ready)
- `PART-58` بحر عاكس وماء ضحل شفاف / Reflective sea & shallow see-through water (three-kit) (proven)

### `PART-57` — رذاذ وزبد وانهمار ماء / Spray, foam & water sheeting

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رذاذ نقاط غاوسية أبيض ودافئ، وزبد على قمم الأمواج، وصفائح ماء تنهمر من الجسم ثم تمويه حركي. / Gaussian spray dots in white and warm add, foam along wave crests, water sheets running off a body, then motion blur.

**متى:** حين يحتاج المشهد رذاذ ماء أو زبدًا على الأمواج أو ماء ينهمر عن جسم، أو قفزة سمكة / for water spray, foam on wave crests, water running off a body, or a fish jump

**كيف:** spray(seed, cx, cy, n, sx, sy, up, sizes) + foam(seed, y, amp, n) + motion_blur; 3D fish jump: 60 spray points y = .05 + vy·u − 4.9u² (u ≤ .7 s) + two additive rings .9·e^(−.9u), scale .6 + 3.4u, second .35 s later.

**المعاملات:** 460 dots σ 160×70; 5 foam rows

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** رذاذ · زبد · spray · foam · splash · water · أمواج · سمكة · بحر · waves · fish jump

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-studio/scenes/whale_dragon.py:65`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:205`

#### 7. قدرات قريبة في العائلة

- `PART-55` شرر على ساعة الشريط / Event sparks on the tape clock (three-kit) (install)
- `PART-56` بخار وغيوم من عناقيد بيضاوية / Ellipse-cluster clouds, smoke & steam (Studio) (ready)
- `PART-58` بحر عاكس وماء ضحل شفاف / Reflective sea & shallow see-through water (three-kit) (proven)
- `PART-59` شيدر ماء منمّط ورسام الماء / Stylised water shader / flat sea path (ready)

### `PART-58` — بحر عاكس وماء ضحل شفاف / Reflective sea & shallow see-through water (three-kit)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سطح three.js Water بخرائط موج مولدة وانعكاس الشمس؛ وماء ضحل بمجموع جيوب وحلقات تموج وفرينل ولمعة GGX وشفافية ملونة بالعمق. / three.js Water plane with generated wave normals and sun reflection; shallow water with sum-of-sines swell, ripple rings, Fresnel, GGX glint and depth-tinted transmission.

**متى:** عند الحاجة لبحر عاكس بلمعان الشمس أو القمر، أو ماء ضحل شفاف بتموجات في مشهد ثلاثي الأبعاد / for a reflective 3D sea with sun or moon glitter, or shallow see-through water with ripples

**كيف:** K3.makeSea({size 30000, res 768, color #0e4a63, distortion 2.4, waveSize 3}) — night_boat frames rendered here (moon glitter, fish-jump rings). K3.makeShallowWater({width 30, depth 30, seg 256, ripples 24, amp .012, clarity .62, deep #0d3b3a, shallow #2f6f62, skyTop #6f9cc8, horizon #f2d6b0, bank #26301c}); w.userData.ripple(x,z,t0,amp); addCaustics scale ≈5.5.

**المعاملات:** sea res 768; shallow 256 seg, 24 rings, life 3.5 s, front .34 m/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بحر · ماء · sea · water · reflection · fresnel · three.js · محيط · انعكاس · تموجات · ocean · ripples

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:245`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js`
- `kosif-studio/motion/kit/three-kit.js:506`

#### 7. قدرات قريبة في العائلة

- `PART-56` بخار وغيوم من عناقيد بيضاوية / Ellipse-cluster clouds, smoke & steam (Studio) (ready)
- `PART-57` رذاذ وزبد وانهمار ماء / Spray, foam & water sheeting (ready)
- `PART-59` شيدر ماء منمّط ورسام الماء / Stylised water shader / flat sea path (ready)
- `PART-60` أنظمة الطقس ثلاثية الأبعاد / 3D weather: vapour, cloud slab, rain, flocks (install)

### `PART-59` — شيدر ماء منمّط ورسام الماء / Stylised water shader / flat sea path

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ماء بثلاثة جيوب مجموعة ومشتقات تحليلية وانعكاس فرينل ولمعة شمس ولمعات مهشّرة وضباب؛ أو سطح بحر مسطح بجيب ورغوة على القمة. / Three summed sine waves with analytic normals, Fresnel sky, hot sun specular, hashed glints and fog; or a flat sea path rebuilt per frame with crest foam.

**متى:** حين تريد ماء منمّطًا كالنيل بأمواج ولمعان شمس وضباب، أو سطح بحر مسطح ثنائي الأبعاد / for stylised water like the Nile with waves, sun glints and fog, or a flat 2D sea

**كيف:** fres = pow(1 − N·V, 4); spec = pow(R·L, 400)·14 + pow(R·L, 24)·.5; sparkle step(.9965, hash(floor(xz·1.6) + floor(9t))); fog 1 − exp(−(d·den)²). Flat: y = 790 + 9 sin(2πx/180 + 2.2t), gradient #2B86E0→#1559A8, foam #CFE9FF 5 px .8.

**المعاملات:** Nile deep #0A3A66 sky #7FB2E0 amp .12; flat amp 9 px λ 180 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ماء · شيدر · water shader · nile · sea · fresnel · نهر · أمواج · لمعان · river · waves

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-59` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-one/projects/egypt-2120-animation/index.html`
- `kosif-one/projects/water-cycle-animation/index.html`

#### 7. قدرات قريبة في العائلة

- `PART-57` رذاذ وزبد وانهمار ماء / Spray, foam & water sheeting (ready)
- `PART-58` بحر عاكس وماء ضحل شفاف / Reflective sea & shallow see-through water (three-kit) (proven)
- `PART-60` أنظمة الطقس ثلاثية الأبعاد / 3D weather: vapour, cloud slab, rain, flocks (install)
- `PART-61` حياة البركة: كوي وبتلات وقصب / Pond life: koi, petals, lily pads, reeds, sway (install)

### `PART-60` — أنظمة الطقس ثلاثية الأبعاد / 3D weather: vapour, cloud slab, rain, flocks

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بخار نقطي يصعد، طبقة سحب حجمية بالأشعة تتغير تغطيتها ولونها مع القصة، مطر آلاف الخطوط، وأسراب طيور تعبر قرب مستوى التركيز. / Rising vapour points, a raymarched volumetric cloud slab whose cover and colour follow the story, thousands of rain streaks, and bird flocks crossing near focus.

**متى:** عند بناء طقس ثلاثي الأبعاد يتغير مع القصة: سحب ومطر وبخار وأسراب طيور / for 3D weather that follows the story: clouds, rain, vapour and bird flocks

**كيف:** K3.makeVapour({n 1400, life 6–10 s, additive, alpha ×.16}); K3.makeCloudSlab({size [7000,520,4200], centre [0,1240,−900]}) 36 view steps × 3 light taps, powder term; K3.makeRain({n 9000, 900–1400 u/s, slant 120}); K3.makeFlock({n 16–18, path, t0, t1, flap sin 9t}); all driven by userData.set(t, …) ramps (water_cycle_3d). The demo project loads assets/main.bundle.js, which is not built in this checkout (koi_pond threw a load error here) — install esbuild and bundle first; the kit functions themselves ship in the prebuilt three-kit.bundle.js.

**المعاملات:** vapour 1400; rain 9000; cloud 36×3 steps

**التثبيت:** cd 100-superskills/skills/kosif-montage-motion/scripts && npm install three@0.186.1 esbuild && python3 motion.py bundle water_cycle_3d

**الوسوم:** طقس · سحب · مطر · طيور · weather · clouds · rain · flock · three.js · جو · بخار · دورة الماء · volumetric · water cycle

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

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-60` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-studio/motion/kit/three-kit.js:273`
- `kosif-studio/motion/kit/three-kit.js:325`
- `kosif-studio/motion/kit/three-kit.js:203`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:34`

#### 7. قدرات قريبة في العائلة

- `PART-58` بحر عاكس وماء ضحل شفاف / Reflective sea & shallow see-through water (three-kit) (proven)
- `PART-59` شيدر ماء منمّط ورسام الماء / Stylised water shader / flat sea path (ready)
- `PART-61` حياة البركة: كوي وبتلات وقصب / Pond life: koi, petals, lily pads, reeds, sway (install)
- `PART-62` مسارات ضوء السيارات / Long-exposure car light trails (install)

### `PART-61` — حياة البركة: كوي وبتلات وقصب / Pond life: koi, petals, lily pads, reeds, sway

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سبع أسماك كوي تنثني على مسارات ليساجو بأعماق مختلفة، 170 بتلة تسقط وتطفو وتصنع حلقات، زنابق تتمايل، وآلاف أعواد القصب والعشب تميل مع الريح. / Seven koi bend along Lissajous paths at depths, 170 petals fall and float (ringing the water), lily pads bob, thousands of reeds and grass blades sway.

**متى:** حين يطلب مشهد بركة بأسماك كوي وبتلات طافية وزنابق وقصب وعشب يتمايل مع الريح / for a pond scene with koi, floating petals, lily pads and reeds swaying in the wind

**كيف:** makeKoi({length .62–.92, amp .10–.14}); x = cx + ax sin(dir·w·t + ph), z = cz + az sin(2·dir·w·t + ph2), depth −.22…−.52; K3.makePetals({n 120–170, fall 2.4–4.6 s, ripple amp .0016–.0024}); makeBlades 2200 (tall .95, amp .07, 1.2 Hz) + 6000 (tall .22, amp .25, 1.7 Hz); K3.addSway(mat, {amp .06, freq 1.3 Hz}) bend ∝ height²; flags K3.addWave(amp .08, 2.4 Hz, λ .9). The demo project loads assets/main.bundle.js, which is not built in this checkout (koi_pond threw a load error here) — install esbuild and bundle first; the kit functions themselves ship in the prebuilt three-kit.bundle.js.

**المعاملات:** 7 koi; 170 petals; 8200 blades

**التثبيت:** cd 100-superskills/skills/kosif-montage-motion/scripts && npm install three@0.186.1 esbuild && python3 motion.py bundle koi_pond

**الوسوم:** كوي · بتلات · قصب · koi · petals · sway · cloth · flag · بركة · أسماك · عشب · pond · grass · lily pads

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

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-61` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:50`
- `kosif-studio/motion/kit/three-kit.js:685`
- `kosif-studio/motion/kit/three-kit.js:591`
- `kosif-studio/motion/kit/three-kit.js:977`

#### 7. قدرات قريبة في العائلة

- `PART-59` شيدر ماء منمّط ورسام الماء / Stylised water shader / flat sea path (ready)
- `PART-60` أنظمة الطقس ثلاثية الأبعاد / 3D weather: vapour, cloud slab, rain, flocks (install)
- `PART-62` مسارات ضوء السيارات / Long-exposure car light trails (install)
- `PART-63` سكب وارتفاع السائل / Pour stream & liquid fill with wobble (seen)

### `PART-62` — مسارات ضوء السيارات / Long-exposure car light trails

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أضواء خلفية تبتعد وأمامية تقترب تصير خطوطًا متصلة بمط كل ضوء على اتجاه حركته. / Tail lights going away and headlights coming in become continuous streaks by stretching each light along its motion.

**متى:** عند الحاجة لخطوط أضواء السيارات الطويلة في مدينة ليلية كأنها تصوير بتعريض طويل / for long-exposure car light streaks in a night city

**كيف:** 18 cars, 22–27 m/s, wrap 1560 m; tail 0xff1e1e ×6, head 0xfff1d8 ×6 spheres r .16; scale.z = 1 + trailLength(v)/(2·.16)·1.2, offset forward so the streak never sits inside the body. Studio also has a long-exposure "lighten" pass for light trails; its test errored in this container, so treat that path as unverified. The demo project loads assets/main.bundle.js, which is not built in this checkout (koi_pond threw a load error here) — install esbuild and bundle first; the kit functions themselves ship in the prebuilt three-kit.bundle.js.

**المعاملات:** 18 cars; ×6 emissive

**التثبيت:** cd 100-superskills/skills/kosif-montage-motion/scripts && npm install three@0.186.1 esbuild && python3 motion.py bundle blue_hour

**الوسوم:** أضواء · سيارات · light trails · long exposure · night city · مدينة ليلية · شارع · تعريض طويل · traffic · headlights

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

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-62` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:107`

#### 7. قدرات قريبة في العائلة

- `PART-60` أنظمة الطقس ثلاثية الأبعاد / 3D weather: vapour, cloud slab, rain, flocks (install)
- `PART-61` حياة البركة: كوي وبتلات وقصب / Pond life: koi, petals, lily pads, reeds, sway (install)
- `PART-63` سكب وارتفاع السائل / Pour stream & liquid fill with wobble (seen)
- `PART-64` سائل ملون ومعدن سائل / Fluid sim backdrop & chrome metaballs (seen)

### `PART-63` — سكب وارتفاع السائل / Pour stream & liquid fill with wobble

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** زجاجة تميل وتسكب خيطًا من عنقها، والمنسوب يرتفع بقص مستطيل مع تموج سطح مخمد، وسحب قشدة تنتشر داخل السائل. / A bottle tilts and pours a stream from its neck; the level rises via a clip rect with a damped surface wobble; cream clouds diffuse inside the liquid.

**متى:** لما يطلب زجاجة تسكب مشروبًا وكوبًا يمتلئ بسائل يتموج أو قشدة تنتشر داخله / when a bottle should pour and a glass fill with wobbling liquid or diffusing cream

**كيف:** Enter 500 ms easeOutBack, rotate ~−45° about the neck, 4–6 px stream grows then retracts, exit 400 ms; level cubic-bezier(.33,0,.2,1) 2.5–3 s, wobble 2–4 px @ 1.5 Hz damped 600 ms; cream: 6–10 blobs blur 12–20 px drifting with noise, clipped to the liquid, ~3 s; ice cubes easeOutBounce 700 ms, 12 px bounce, 180 ms stagger.

**المعاملات:** pour 2.5–3 s; wobble 2–4 px @ 1.5 Hz

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سكب · سائل · pour · liquid fill · drink · wobble · مشروب · كوب · زجاجة · pouring · glass fill

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-63` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-ror-fly-9950f1`
- `kosif-tool/styles/pm-sarut0bisasuke-cefa43`

#### 7. قدرات قريبة في العائلة

- `PART-61` حياة البركة: كوي وبتلات وقصب / Pond life: koi, petals, lily pads, reeds, sway (install)
- `PART-62` مسارات ضوء السيارات / Long-exposure car light trails (install)
- `PART-64` سائل ملون ومعدن سائل / Fluid sim backdrop & chrome metaballs (seen)
- `PART-65` لهب عادم وشعلة / Exhaust plume & canvas fire emitter (seen)

### `PART-64` — سائل ملون ومعدن سائل / Fluid sim backdrop & chrome metaballs

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سوائل مستقرة على GPU بحقن صبغة خلف نص محدد؛ أو 3–5 كرات SDF تدور وتلتحم بمادة كروم؛ أو كرات بخطوط كنتور. / GPU stable fluids with dye injection behind outlined text; 3–5 raymarched SDF spheres orbiting and merging in chrome; or metaballs with marching-squares iso-contours.

**متى:** حين تحتاج خلفية سائل ملون خلف نص، أو كرات معدنية كالكروم تلتحم، أو خطوط كنتور / for a dye-fluid backdrop behind text, merging chrome metaballs, or iso-contour blobs

**كيف:** Chrome: smooth k .4, orbit .5 Hz, env-map; contours: sum of 7 radial fields, 4–6 iso levels; HyperFrames vfx-liquid-background (vertex displacement plane, 12 s) is the installable option.

**المعاملات:** k .4; 7 balls; 4–6 contours

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سائل · fluid sim · metaball · chrome · contours · معدن سائل · كروم · خلفية سائلة · liquid background · blobs

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-64` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-lukasersil-0ed38e`
- `kosif-tool/styles/pm-sahildesigner23-ee3155`
- `kosif-tool/styles/pm-teslachartz-c58b32`
- `kosif-one/vendor/hyperframes/registry/blocks/vfx-liquid-background/vfx-liquid-background.html`

#### 7. قدرات قريبة في العائلة

- `PART-62` مسارات ضوء السيارات / Long-exposure car light trails (install)
- `PART-63` سكب وارتفاع السائل / Pour stream & liquid fill with wobble (seen)
- `PART-65` لهب عادم وشعلة / Exhaust plume & canvas fire emitter (seen)
- `PART-66` أشعة تحت الماء وفوانيس عائمة / Underwater rays & floating lanterns (seen)

### `PART-65` — لهب عادم وشعلة / Exhaust plume & canvas fire emitter

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مخروط جمعي بضوضاء وأشرطة ماسية ساطعة (بنفسجي→أبيض)، أو باعث يولد 30–60 جسيمًا في الإطار تصعد بسلم أبيض→أصفر→أحمر. / Additive noisy cone with bright shock-diamond bands (violet→white core), or an emitter spawning 30–60 particles/frame rising white→yellow→red→transparent.

**متى:** عند الحاجة لعادم صاروخ أو شعلة أو باعث نار يطلق جسيمات تصعد وتتغير ألوانها / for a rocket exhaust plume or a fire emitter whose particles rise and change colour

**كيف:** Emitter as closed form: particle i born at floor(t·rate) with hash-seeded velocity, age = t − birth, colour ramp by age, "lighter"; cube exhaust: emissive cubes ~1 s life, 40/s; heat streaks: red line sprites rising and fading.

**المعاملات:** 30–60 / frame; life ~1 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عادم · لهب · exhaust · plume · emitter · rocket · صاروخ · نار · حرارة · torch · fire particles

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:torch` ← python3 -c "import torch" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-65` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-konstantinsaifo-96fc89`
- `kosif-tool/styles/pm-chrisjdimarco-f068db`
- `kosif-tool/styles/pm-ivanfioravanti-bd9261`

#### 7. قدرات قريبة في العائلة

- `PART-63` سكب وارتفاع السائل / Pour stream & liquid fill with wobble (seen)
- `PART-64` سائل ملون ومعدن سائل / Fluid sim backdrop & chrome metaballs (seen)
- `PART-66` أشعة تحت الماء وفوانيس عائمة / Underwater rays & floating lanterns (seen)
- `PART-67` محاكاة هوديني / Houdini FLIP / Pyro / Vellum / RBD + Karma (key)

### `PART-66` — أشعة تحت الماء وفوانيس عائمة / Underwater rays & floating lanterns

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تدرج أزرق بأشعة ضوء قطرية شفافة، قناديل تتمايل وفقاعات تصعد؛ أو فوانيس لوتس مضيئة تطفو على الماء بوميض وانعكاس قصير. / Blue gradient with translucent diagonal light shafts, bobbing jellyfish and rising bubbles; or glowing lotus lanterns drifting on water with flicker and a short reflection streak.

**متى:** حين يريد مشهدًا تحت البحر بأشعة ضوء وقناديل وفقاعات، أو فوانيس مضيئة تطفو على الماء / for an underwater scene with light shafts, jellyfish and bubbles, or glowing lanterns on water

**كيف:** Bob 10 px @ .4 Hz; bubbles 20–40 px/s with wobble; lanterns 8–15, flicker .85–1.0 @ 3–6 Hz, drift 5–10 px/s.

**المعاملات:** bob 10 px/.4 Hz; 8–15 lanterns

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تحت الماء · فوانيس · underwater · bubbles · lanterns · فقاعات · قناديل البحر · أشعة ضوء · jellyfish · light rays

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-66` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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
- `kosif-tool/styles/pm-demitiyageekzen-7770ad`

#### 7. قدرات قريبة في العائلة

- `PART-64` سائل ملون ومعدن سائل / Fluid sim backdrop & chrome metaballs (seen)
- `PART-65` لهب عادم وشعلة / Exhaust plume & canvas fire emitter (seen)
- `PART-67` محاكاة هوديني / Houdini FLIP / Pyro / Vellum / RBD + Karma (key)
- `PART-68` كرة ترتد بمعامل ارتداد / Gravity bounce with restitution & dotted trail (proven)

### `PART-67` — محاكاة هوديني / Houdini FLIP / Pyro / Vellum / RBD + Karma

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | Houdini تجاري (SideFX) / commercial SideFX licence. |

**ما هي:** محاليل احترافية للسوائل والدخان والقماش والأجسام الصلبة، وجسيمات curl بـ VEX، تتطلب ترخيصًا تجاريًا. / Pro fluid, smoke, cloth and rigid-body solvers and VEX curl-flow particles — commercial licence required.

**متى:** عند الحاجة لمحاكاة احترافية لسوائل أو دخان أو قماش أو أجسام صلبة في Houdini بترخيص تجاري / when pro fluid, smoke, cloth or rigid-body simulation in Houdini is needed, with a commercial licence

**كيف:** hython headless baking; VEX: @v = lerp(@v, noise·speed, blend); orient to velocity; @pscale shrinks from 70% of life. Not available here — use PART-23 / PART-51 instead.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هوديني · houdini · flip · pyro · vex · simulation · محاكاة سوائل · دخان · قماش · cloth · rigid body

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-67` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-atlas/skills/228-mas-3d-games/708-houdini/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `PART-65` لهب عادم وشعلة / Exhaust plume & canvas fire emitter (seen)
- `PART-66` أشعة تحت الماء وفوانيس عائمة / Underwater rays & floating lanterns (seen)
- `PART-68` كرة ترتد بمعامل ارتداد / Gravity bounce with restitution & dotted trail (proven)
- `PART-69` كرة داخل حلقات دوارة / Ball in rotating gapped rings (escape sim) (seen)

### `PART-68` — كرة ترتد بمعامل ارتداد / Gravity bounce with restitution & dotted trail

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** y″ = −g مع عكس السرعة × e عند التلامس، ونقطة كل N إطارات تترك أثر قطع مكافئ منقط مع تسمية «e = 0.75». / Integrate y″ = −g, reflect velocity ×e on contact, stamp a dot every N frames to leave a dotted parabola, annotated “e = 0.75”.

**متى:** حين يشرح الفيديو ارتداد كرة بالجاذبية ومعامل الارتداد مع أثر منقط للمسار / for explaining a ball bouncing under gravity with restitution and a dotted path

**كيف:** Fixed dt = 1/60 replayed from frame 0 inside seek (deterministic); e .75–.85; g 900 px/s²; dot 4 px #c9452c every 2–4 frames. Rendered here. Add squash 20% on impact and stretch 10% in flight (SHAPE squash).

**المعاملات:** e .75–.85; dt 1/60; dot every 2–4 frames

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ارتداد · جاذبية · bounce · restitution · physics · parabola · كرة · شرح فيزياء · قطع مكافئ · ball bounce · squash stretch

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-68` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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
- `kosif-tool/styles/pm-deifosv-04e4d3/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `PART-66` أشعة تحت الماء وفوانيس عائمة / Underwater rays & floating lanterns (seen)
- `PART-67` محاكاة هوديني / Houdini FLIP / Pyro / Vellum / RBD + Karma (key)
- `PART-69` كرة داخل حلقات دوارة / Ball in rotating gapped rings (escape sim) (seen)
- `PART-70` سقوط وتكدس الأجسام / Drops, piles & toppling stacks (seen)

### `PART-69` — كرة داخل حلقات دوارة / Ball in rotating gapped rings (escape sim)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كرة ترتد داخل 12 حلقة دوارة بفجوات؛ تنعكس السرعة حول العمودي وتمر من الفجوة فتختفي الحلقة متشظية. / A ball ricochets inside 12 rotating gapped rings; velocity reflects about the normal and passes through the gap, the ring then shatters.

**متى:** لما يطلب فيديو مريحًا لكرة ترتد داخل حلقات دوارة وتهرب من فجواتها فتتحطم الحلقة / for a satisfying clip of a ball bouncing inside rotating gapped rings that shatter as it escapes

**كيف:** Fixed sub-steps (120 Hz at 60 fps or 4/frame); when \|p − c\| ≥ R − r: v −= 2(v·n)n, restitution 1; gap test via atan2 within the rotating window (gap 28–40°); rings ω .3 + .08i alternating; tapered trail .3 s.

**المعاملات:** 12 rings; gap 28–40°; speed ~600 px/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حلقات · كرة · ring escape · satisfying · physics · reflection · مريح للأعصاب · هروب الكرة · ارتداد · bouncing ball · gap escape

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-69` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-kantamk-61f410`
- `kosif-tool/styles/pm-kantamk-61f410/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `PART-67` محاكاة هوديني / Houdini FLIP / Pyro / Vellum / RBD + Karma (key)
- `PART-68` كرة ترتد بمعامل ارتداد / Gravity bounce with restitution & dotted trail (proven)
- `PART-70` سقوط وتكدس الأجسام / Drops, piles & toppling stacks (seen)
- `PART-71` محركات الأجسام الصلبة / Rigid-body engines (Rapier / cannon-es / matter-js) (install)

### `PART-70` — سقوط وتكدس الأجسام / Drops, piles & toppling stacks

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بطاقات تسقط بارتداد وتتكدس ثم يتمايل البرج وينهار؛ أيقونات تسقط في وعاء؛ ملصقات تتكوم أسفل الشاشة؛ برطمان يمتلئ بعداد. / Cards drop with bounce and stack, the tower sways and topples; icons fall into a bowl; posters pile along the bottom; a jar fills with a counter.

**متى:** حين تسقط بطاقات أو أيقونات أو ملصقات وتتكدس، أو ينهار برج، أو يمتلئ برطمان مع عداد / when cards, icons or posters drop and pile up, a tower topples, or a jar fills with a counter

**كيف:** Each item as phases of t: drop ~300 ms easeOutBounce (stagger 400 ms), shared sway growing to 6°, topple about base, settle; icons 500 ms easeInQuad + 15% bounce, ±15°; jar g ~2500 px/s², restitution .3, 1 item / 120 ms; posters 40–60, ±30°, stagger 30 ms (or pre-baked rigid bodies).

**المعاملات:** drop 300 ms; restitution .3; 1 item / 120 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سقوط · تكدس · drop · pile · stack · topple · jar · انهيار · برج · عداد · falling · collapse

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-70` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/stickman`
- `kosif-tool/styles/pm-wozu-co-242285`
- `kosif-tool/styles/pm-thilina-a-891c09`
- `kosif-tool/styles/pm-lester-tyy-f897f7`

#### 7. قدرات قريبة في العائلة

- `PART-68` كرة ترتد بمعامل ارتداد / Gravity bounce with restitution & dotted trail (proven)
- `PART-69` كرة داخل حلقات دوارة / Ball in rotating gapped rings (escape sim) (seen)
- `PART-71` محركات الأجسام الصلبة / Rigid-body engines (Rapier / cannon-es / matter-js) (install)
- `PART-72` حركات فيزيائية جاهزة / HyperFrames physical motions (pendulum, physical exit, stack shuffle) (install)

### `PART-71` — محركات الأجسام الصلبة / Rigid-body engines (Rapier / cannon-es / matter-js)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شعارات ومكعبات تسقط وتتكدس بفيزياء حقيقية في 2D أو 3D. / Logos and voxels falling and stacking with real physics in 2D or 3D.

**متى:** عند الحاجة لسقوط شعارات أو مكعبات وتكدسها بفيزياء حقيقية في 2D أو 3D مع خبز النتائج قبل الرندر / when logos or cubes must fall and stack with real 2D or 3D physics, baked before render

**كيف:** Step a fixed dt = 1/fps per frame from a seeded initial state and bake positions to JSON, then render frames from the bake (never real-time). @react-three/rapier for R3F; matter-js for 2D.

**المعاملات:** dt 1/fps; bake first

**التثبيت:** npm i @dimforge/rapier3d-compat matter-js cannon-es

**الوسوم:** فيزياء · rapier · matter-js · cannon · rigid body · أجسام صلبة · سقوط · تصادم · physics engine · collision

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:matter` ← npm ls matter أو وجود node_modules/matter
- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-71` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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
- `kosif-atlas/skills/2696-game-studio/10367-react-three-fiber-game/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `PART-69` كرة داخل حلقات دوارة / Ball in rotating gapped rings (escape sim) (seen)
- `PART-70` سقوط وتكدس الأجسام / Drops, piles & toppling stacks (seen)
- `PART-72` حركات فيزيائية جاهزة / HyperFrames physical motions (pendulum, physical exit, stack shuffle) (install)
- `PART-73` أوتار تهتز عند الاصطدام / Vibrating strings on impact (seen)

### `PART-72` — حركات فيزيائية جاهزة / HyperFrames physical motions (pendulum, physical exit, stack shuffle)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0. |

**ما هي:** محتوى معلق يتأرجح بندوليًا ويستقر، بطاقة تخرج بزخم حقيقي (رمي، سقوط، انزلاق) بلا تلاشٍ، ورصة بطاقات تُخلط بكتلة. / Content swings into rest like a damped pendulum, a card exits with real momentum (toss/drop/slide), and a 3–5 card stack reshuffles with mass.

**متى:** حين يريد عنصرًا يتأرجح كالبندول ويستقر، أو بطاقة تخرج برمية أو سقوط، أو خلط رصة بطاقات / when content swings to rest like a pendulum, a card exits by toss or drop, or a card stack reshuffles

**كيف:** npx hyperframes add pendulum-swing (pivot top-center\|left\|right, amplitude gentle\|standard\|wide) \| physical-exit (mode toss\|drop\|slide) \| spring-stack-shuffle (cues "0.9, 1.7, 1.95"). Reactive displacement rule: the intruder tween drives the victim, victim durations 40–50% of the intruder.

**التثبيت:** npx hyperframes add pendulum-swing

**الوسوم:** بندول · زخم · pendulum · physical exit · shuffle · hyperframes · تأرجح · خروج · خلط بطاقات · swing · card exit

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-72` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-one/vendor/hyperframes/registry/components/pendulum-swing/pendulum-swing.html`
- `kosif-one/vendor/hyperframes/registry/components/physical-exit/physical-exit.html`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/reactive-displacement.md`

#### 7. قدرات قريبة في العائلة

- `PART-70` سقوط وتكدس الأجسام / Drops, piles & toppling stacks (seen)
- `PART-71` محركات الأجسام الصلبة / Rigid-body engines (Rapier / cannon-es / matter-js) (install)
- `PART-73` أوتار تهتز عند الاصطدام / Vibrating strings on impact (seen)
- `PART-74` أسراب الطيور والحروف (boids) / Flocks & boids (birds, letters, stipple) (seen)

### `PART-73` — أوتار تهتز عند الاصطدام / Vibrating strings on impact

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خمسة منحنيات أفقية؛ عند الاصطدام تأخذ نقطة التحكم سعة A تخمد بجيب مخمد. / Five horizontal quadratics; on impact the control point gets amplitude A decaying as a damped sine.

**متى:** عند اهتزاز أوتار أو خطوط أفقية لحظة الاصطدام ثم تخمد تدريجيًا / for horizontal strings or lines that vibrate on impact and gradually settle

**كيف:** offset = A·e^(−6t)·sin(30t), A ≈ 4% of height, 400 ms.

**المعاملات:** A 4% h; e^(−6t) sin 30t

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أوتار · strings · damped sine · impact · music · اهتزاز · ذبذبة · خطوط تهتز · vibration · string wobble

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-73` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-1littlecoder-9fef89`

#### 7. قدرات قريبة في العائلة

- `PART-71` محركات الأجسام الصلبة / Rigid-body engines (Rapier / cannon-es / matter-js) (install)
- `PART-72` حركات فيزيائية جاهزة / HyperFrames physical motions (pendulum, physical exit, stack shuffle) (install)
- `PART-74` أسراب الطيور والحروف (boids) / Flocks & boids (birds, letters, stipple) (seen)
- `PART-75` رمية قوسية بأشباح / Parabolic toss with ghost trail (idea)

### `PART-74` — أسراب الطيور والحروف (boids) / Flocks & boids (birds, letters, stipple)

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سرب V يرفرف على مسار، أو 8192 نقطة بفصل ومحاذاة وتماسك، أو حروف تطير كسرب فوق سماء متدرجة. / Flapping V-birds on a path, 8,192 boids with separation/alignment/cohesion, or glyph sprites flocking over a gradient sky.

**متى:** لما يطلب سرب طيور يطير على مسار أو آلاف النقاط تتحرك كسرب، أو كلمات تطير كسرب / when the user wants a bird flock on a path, thousands of flocking dots, or words flying as a swarm

**كيف:** three-kit makeFlock n 18 (ready, see PART-60); boids: precompute on CPU with fixed dt and bake, draw 1–2 px dots with a soft projected shadow; gulls 3–5 flapping 3 Hz on slow paths. For Arabic letter flocks fly whole words, not letters.

**المعاملات:** n 18 / 8192; flap 3 Hz

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سرب · طيور · boids · flock · birds · نوارس · طيران · حروف طائرة · swarm · gulls

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-74` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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
- `kosif-tool/styles/pm-ajith-io-ea7f2d`
- `kosif-tool/styles/pm-axtonliu-0b861d`
- `kosif-studio/motion/kit/three-kit.js:203`

#### 7. قدرات قريبة في العائلة

- `PART-72` حركات فيزيائية جاهزة / HyperFrames physical motions (pendulum, physical exit, stack shuffle) (install)
- `PART-73` أوتار تهتز عند الاصطدام / Vibrating strings on impact (seen)
- `PART-75` رمية قوسية بأشباح / Parabolic toss with ghost trail (idea)
- `PART-U01` حقل كشف بالضجيج والمسافة من المركز / Noise + centre-distance reveal field (proven)

### `PART-75` — رمية قوسية بأشباح / Parabolic toss with ghost trail

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رمز يُقذف على قطع مكافئ ويترك 12 نسخة شبحية تخبو. / A token thrown on a parabola leaving 12 fading ghost copies.

**متى:** حين يُرمى رمز أو عنصر على قوس ويترك نسخًا شبحية تتلاشى خلفه / when a token is thrown on an arc leaving fading ghost copies behind

**كيف:** Untested brief idea: sample the arc at 12 earlier times (PART-31), 900 ms total, trail fade 200 ms.

**المعاملات:** 900 ms; 12 ghosts

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** رمية · toss · parabola · ghost trail · قذف · قوس · أثر شبحي · throw · arc

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-75` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/styles/pm-paulo-kombucha-96431c/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `PART-73` أوتار تهتز عند الاصطدام / Vibrating strings on impact (seen)
- `PART-74` أسراب الطيور والحروف (boids) / Flocks & boids (birds, letters, stipple) (seen)
- `PART-U01` حقل كشف بالضجيج والمسافة من المركز / Noise + centre-distance reveal field (proven)
- `PART-X01` مطر الرموز وموجات الحروف / Code rain, glyph streams and the crash beat (documented)

### `PART-U01` — حقل كشف بالضجيج والمسافة من المركز / Noise + centre-distance reveal field

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | Claude AI Motion Graphics (Tao Prompts) — ideas and numbers only, code not copied |

**ما هي:** field = 0.55·noise + 0.45·\|x−0.5\|·2 و alpha = clip((p·1.15 − field)/0.12) مع شريط مضيء على الجبهة؛ الجسيمات تبدأ قبل الجبهة بـ0.2 ث فقط (110–340 px إزاحة، مسارات منحنية) وتصل مع مرورها. — Organic dissolve that reveals from the centre outward; particles arrive with the front.

**متى:** ظهور عنصر أو شاشة بتفكك عضوي / an element materialising with an organic dissolve

**كيف:** أضف حدًا (edge) إلى الحقل لرسم الخطوط أولًا؛ للخروج اعكس p.

**المعاملات:** threshold 0.12; overshoot 1.15; particles start ≤0.2 s early

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** dissolve · reveal · كشف · particles · جسيمات · noise · ضجيج · materialise

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-U01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/owner-uploads-20261023/proof_uploads.py`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/owner-uploads-20261023/receipt.json`

#### 7. قدرات قريبة في العائلة

- `PART-74` أسراب الطيور والحروف (boids) / Flocks & boids (birds, letters, stipple) (seen)
- `PART-75` رمية قوسية بأشباح / Parabolic toss with ghost trail (idea)
- `PART-X01` مطر الرموز وموجات الحروف / Code rain, glyph streams and the crash beat (documented)

### `PART-X01` — مطر الرموز وموجات الحروف / Code rain, glyph streams and the crash beat

| الحقل | القيمة |
|---|---|
| العائلة | `particles-fluids-physics` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/particles-fluids-physics.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner (no LICENSE file) |

**ما هي:** عدّة «داخل النظام»: مطر رموز وتيارات حروف على منحنيات وحلقات صدمة من الرموز ولحظة انهيار. — An 'inside the system' kit: code rain, glyph streams on curves, glyph shockwave rings and a crash beat.

**متى:** فيلم تقني أو أمني أو لحظة «تعطل» — a tech or security film or a 'crash' moment.

**كيف:** Use a glyph atlas per (font, size, colour, weight) for thousands of glyphs. Rain: per-column 80–420 px/s, length 4–30, head glyph changes at 16 Hz, trail at 2.5 Hz, alpha (1 − j/L)^1.5 · 0.8, glyphs ≥ 30 px at α 0.8 on dark to survive the lens pass. Streams: ~38 glyphs along quadratic Béziers over 0.72 s. Shockwave rings of 56/40 glyphs, r 240 → 1250 px. Crash beat: freeze + dim the rain to 0.4, resume at 1.3×, 36 px tear bands, a red modal with back(.16), shake 16 px at 5 Hz decaying at 9, CRT collapse scaleY → 0.015.

**المعاملات:** rain 80–420 px/s; head 16 Hz; trail 2.5 Hz; glyph ≥ 30 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** code rain · glyphs · matrix · shockwave · مطر الرموز · حروف · انهيار

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:PART-X01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `infinite-matrices` · `particles`.
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

- `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/code-engine.md`

#### 7. قدرات قريبة في العائلة

- `PART-75` رمية قوسية بأشباح / Parabolic toss with ghost trail (idea)
- `PART-U01` حقل كشف بالضجيج والمسافة من المركز / Noise + centre-distance reveal field (proven)

