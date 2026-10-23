# `light-glow-bloom` — الثري دي والمحاكاة والرندر (87 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/light-glow-bloom.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/3d.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`GLOW-01` لافتة نيون عربية حيّة](#glow-01--لافتة-نيون-عربية-حيّة--living-arabic-neon-sign-ignition--wall-light--wet-reflection--synced-hum)
- [`GLOW-02` جدول الاشتعال والوميض المعطوب](#glow-02--جدول-الاشتعال-والوميض-المعطوب--ignition--faulty-tube-flicker-schedule)
- [`GLOW-03` أنبوب نيون SVG بأربع طبقات](#glow-03--أنبوب-نيون-svg-بأربع-طبقات--svg-neon-tube-4-stroke-stack)
- [`GLOW-04` توهج النص النيوني بثلاثة ظلال لكل كلمة](#glow-04--توهج-النص-النيوني-بثلاثة-ظلال-لكل-كلمة--neon-text-glow-triple-shadow-per-word)
- [`GLOW-05` توهج الكلمة النشطة في الترجمة](#glow-05--توهج-الكلمة-النشطة-في-الترجمة--active-caption-word-glow)
- [`GLOW-06` ترجمة عربية بتوهج ASS مزدوج الطبقة](#glow-06--ترجمة-عربية-بتوهج-ass-مزدوج-الطبقة--two-layer-ass-glow-for-arabic-captions)
- [`GLOW-07` مرشح توهج SVG ونسخة مموهة](#glow-07--مرشح-توهج-svg-ونسخة-مموهة--svg-blur-merge-glow--blurred-duplicate)
- [`GLOW-08` رأس ضوئي يسري على الخط وشطب متوهج](#glow-08--رأس-ضوئي-يسري-على-الخط-وشطب-متوهج--travelling-light-head-on-a-stroke-glint-comet-glowing-strike)
- [`GLOW-09` خط كهربائي متوهج برأس أبيض](#glow-09--خط-كهربائي-متوهج-برأس-أبيض--electric-draw-head-route-line)
- [`GLOW-10` توهج فوسفوري وخطوط نيون على Canvas](#glow-10--توهج-فوسفوري-وخطوط-نيون-على-canvas--phosphor--canvas-neon-stroke-glow)
- [`GLOW-11` حافة متدرجة متوهجة وظل بلون العنصر](#glow-11--حافة-متدرجة-متوهجة-وظل-بلون-العنصر--gradient-rim-glow-border--hue-matched-glow-shadow)
- [`GLOW-12` كلمة من نقاط مضيئة](#glow-12--كلمة-من-نقاط-مضيئة--dot-matrix-glowing-word)
- [`GLOW-13` نفق نيون واندفاع للأمام](#glow-13--نفق-نيون-واندفاع-للأمام--neon-tunnel--streak-zoom-through)
- [`GLOW-14` توهج مضاف متدرج في الرسم بالكود](#glow-14--توهج-مضاف-متدرج-في-الرسم-بالكود--painter-additive-glow-stack-blades-magic-embers)
- [`GLOW-15` وصفة البرق والقوس الكهربائي](#glow-15--وصفة-البرق-والقوس-الكهربائي--lightning-bolt-electric-arc--3d-double-flash)
- [`GLOW-16` بركة ضوء شعاعية خلف العنوان](#glow-16--بركة-ضوء-شعاعية-خلف-العنوان--hero-radial-glow-pool-bloom-in-bounded-breathe-point-origin)
- [`GLOW-17` غسيل خلفية بعدة توهجات وقاعدة الخلفية الحية](#glow-17--غسيل-خلفية-بعدة-توهجات-وقاعدة-الخلفية-الحية--multi-blob-wash-corner-glows--the-living-backdrop-rule)
- [`GLOW-18` خلفيات الاستوديو الإجرائية: شفق وغروب ومدار](#glow-18--خلفيات-الاستوديو-الإجرائية-شفق-وغروب-ومدار--studio-procedural-glow-backdrops-aurora--sunset--grid)
- [`GLOW-19` ستارة الشفق](#glow-19--ستارة-الشفق--aurora-drift--aurora-curtains)
- [`GLOW-20` بقعة ضوء تتبع العنصر](#glow-20--بقعة-ضوء-تتبع-العنصر--follow-spot--feathered-spotlight)
- [`GLOW-21` حلقات هالة متحدة المركز](#glow-21--حلقات-هالة-متحدة-المركز--concentric-halo-rings)
- [`GLOW-22` نبضة وهالة لفت الانتباه](#glow-22--نبضة-وهالة-لفت-الانتباه--pulse-ring-halo--the-attention-set)
- [`GLOW-23` كلمة تنفجر بتوهج وحلقة](#glow-23--كلمة-تنفجر-بتوهج-وحلقة--burst-word-with-glow--expanding-ring)
- [`GLOW-24` هالة تتنفس مع الصوت وأشعة وغبار القصيدة](#glow-24--هالة-تتنفس-مع-الصوت-وأشعة-وغبار-القصيدة--voicebeat-breathing-halo-shafts--dust-verse-light)
- [`GLOW-25` دائرة سحرية بكسل بتوهج منقّط](#glow-25--دائرة-سحرية-بكسل-بتوهج-منقّط--pixel-magic-circle-dithered-glow)
- [`GLOW-26` سلسلة ما بعد المعالجة السينمائية (makePost)](#glow-26--سلسلة-ما-بعد-المعالجة-السينمائية-makepost--three-kit-cinematic-post-stack-makepost)
- [`GLOW-27` بلوم بلون مصدره على المواد المشعة](#glow-27--بلوم-بلون-مصدره-على-المواد-المشعة--emissive-colour-corona-bloom-and-hit-lit-rings)
- [`GLOW-28` جدول البلوم والتعريض لكل لقطة](#glow-28--جدول-البلوم-والتعريض-لكل-لقطة--per-shot-bloom--exposure-presets-cinematic--lite--lab)
- [`GLOW-29` بلوم TSL وWebGPU](#glow-29--بلوم-tsl-وwebgpu--tsl--webgpu-bloom-selective-mrt--lens-nodes)
- [`GLOW-30` بلوم الرسم الثابت](#glow-30--بلوم-الرسم-الثابت--painter-highlight-bloom-stills--painted-films)
- [`GLOW-31` الدمج المضاف على لوحة عائمة](#glow-31--الدمج-المضاف-على-لوحة-عائمة--float-canvas-light-compositing-add--screen-above-10)
- [`GLOW-32` تعتيم الأطراف](#glow-32--تعتيم-الأطراف--vignette-css--canvas--kit--painter)
- [`GLOW-33` الانحراف اللوني للعدسة](#glow-33--الانحراف-اللوني-للعدسة--lens-chromatic-aberration-edge-weighted)
- [`GLOW-34` انقسام RGB على الضربة](#glow-34--انقسام-rgb-على-الضربة--rgb-split-hit-jitter)
- [`GLOW-35` تمويه السرعة وتلطيخ التكبير وكشف التركيز](#glow-35--تمويه-السرعة-وتلطيخ-التكبير-وكشف-التركيز--velocity-blur-zoom-smear-title--focus-pull-glow)
- [`GLOW-36` مؤثرات وسائط HyperFrames وسلسلة VFX](#glow-36--مؤثرات-وسائط-hyperframes-وسلسلة-vfx--hyperframes-media-effects--per-pixel-vfx-chain)
- [`GLOW-37` مكتبة مؤثرات ريموشن](#glow-37--مكتبة-مؤثرات-ريموشن--remotion-remotioneffects-glow--lightleak--starburst--shine)
- [`GLOW-38` تأثيرات ما بعد المعالجة على عناصر HTML](#glow-38--تأثيرات-ما-بعد-المعالجة-على-عناصر-html--html-in-canvas-post-fx--typegpu-liquid-glass)
- [`GLOW-39` مظهر الهولوجرام](#glow-39--مظهر-الهولوجرام--hologram-look)
- [`GLOW-40` التوهج على النص علامة توليد](#glow-40--التوهج-على-النص-علامة-توليد--qa-glow-on-type-is-a-tell)
- [`GLOW-41` مسحة ضوء على جملة الذروة](#glow-41--مسحة-ضوء-على-جملة-الذروة--payoff-light-sweep-through-letterforms)
- [`GLOW-42` لمعة البطاقة والزر وانعكاس الزجاج](#glow-42--لمعة-البطاقة-والزر-وانعكاس-الزجاج--ui-sheen-family-card-scan-button-glint-one-pass-glass-band)
- [`GLOW-43` مرور الضوء المفتاحي على المنتج](#glow-43--مرور-الضوء-المفتاحي-على-المنتج--travelling-key-light-pass-product-hero-light-thread-reveal)
- [`GLOW-44` لمعة تدور مع الجسم](#glow-44--لمعة-تدور-مع-الجسم--rotation-locked-specular-sheen-fake-3d-chrome)
- [`GLOW-45` خط مسح ليزري وشريط إضاءة يمسح الكود](#glow-45--خط-مسح-ليزري-وشريط-إضاءة-يمسح-الكود--laser-scan-line--scanning-highlight-bar)
- [`GLOW-46` بريق نجمي وشرر القلم](#glow-46--بريق-نجمي-وشرر-القلم--twinkle-sparkles--pen-sparks)
- [`GLOW-47` أشعة إلهية وبلوم فوق اللقطة بـ CSS](#glow-47--أشعة-إلهية-وبلوم-فوق-اللقطة-بـ-css--css-god-rays--bloom-layer-over-footage)
- [`GLOW-48` أشعة الشمس في المشهد ثلاثي الأبعاد](#glow-48--أشعة-الشمس-في-المشهد-ثلاثي-الأبعاد--screen-space-god-rays-3d-sun)
- [`GLOW-49` انفجار أشعة شمسي دوّار](#glow-49--انفجار-أشعة-شمسي-دوّار--rotating-sunburst--ray-burst-backdrop)
- [`GLOW-50` وهج العدسة ثلاثي الأبعاد](#glow-50--وهج-العدسة-ثلاثي-الأبعاد--3d-lens-flare-that-follows-the-sun)
- [`GLOW-51` فلير أنامورفي بأشباح](#glow-51--فلير-أنامورفي-بأشباح--anamorphic-flare-with-ghosts-painter--streak-field)
- [`GLOW-52` ألواح ضوء WebGPU جاهزة](#glow-52--ألواح-ضوء-webgpu-جاهزة--webgpu-shader-light-plates-godrays--lensflare--lightedge--prism-)
- [`GLOW-53` تسريب ضوء وحرق فيلم](#glow-53--تسريب-ضوء-وحرق-فيلم--light-leak-overexposure--film-burn-transition)
- [`GLOW-54` ومضة الإطار وانفجار الضوء](#glow-54--ومضة-الإطار-وانفجار-الضوء--flash-frame-double-strike--light-burst-transition)
- [`GLOW-55` أشعة يلقيها النص ونص بشعاع المؤشر](#glow-55--أشعة-يلقيها-النص-ونص-بشعاع-المؤشر--volumetric-rays-cast-by-a-wordmark--cursor-light-text)
- [`GLOW-56` الشمس والهالة والكسوف](#glow-56--الشمس-والهالة-والكسوف--blooming-sun-corona--eclipse-2d-and-3d)
- [`GLOW-57` إضاءة ثلاثية بالوقفات والكلفن](#glow-57--إضاءة-ثلاثية-بالوقفات-والكلفن--three-point-rig-in-stops--kelvin-k3lightrig)
- [`GLOW-58` قوالب البورتريه السبعة](#glow-58--قوالب-البورتريه-السبعة--seven-portrait-rig-presets-k3lightpreset)
- [`GLOW-59` ثمانية عشر إعداد إضاءة وخطة الطاقم](#glow-59--ثمانية-عشر-إعداد-إضاءة-وخطة-الطاقم--18-named-lighting-setups--the-lightplan-deliverable)
- [`GLOW-60` حاسبة الضوء](#glow-60--حاسبة-الضوء--light-calculator-ratio--softness--falloff--ev--guide-number--shutter-angle--mired)
- [`GLOW-61` حرارة اللون والجيلاتين ومصادر مسماة](#glow-61--حرارة-اللون-والجيلاتين-ومصادر-مسماة--kelvin--rgb-gels--19-named-light-sources)
- [`GLOW-62` ارتداد السماء وضباب نحو الشمس](#glow-62--ارتداد-السماء-وضباب-نحو-الشمس--sky-bounce-fog-toward-the-sun--blue-hour-painting)
- [`GLOW-63` إضاءة الحافة في الرسم](#glow-63--إضاءة-الحافة-في-الرسم--painter-rim-light--two-colour-wet-rims)
- [`GLOW-64` تظليل الحجم نحو الضوء](#glow-64--تظليل-الحجم-نحو-الضوء--form-shading-toward-a-light-point)
- [`GLOW-65` جسم مضاء فيزيائيًا وسحب مجسمة](#glow-65--جسم-مضاء-فيزيائيًا-وسحب-مجسمة--physically-lit-relief-bodies--cloud-decks)
- [`GLOW-66` مظلل البلورة: فرينل ولمعة وانعكاس سماء](#glow-66--مظلل-البلورة-فرينل-ولمعة-وانعكاس-سماء--fresnel--blinn-glasscrystal-shader)
- [`GLOW-67` زجاج بانكسار وتشتت وكرات زجاجية](#glow-67--زجاج-بانكسار-وتشتت-وكرات-زجاجية--refraction-dispersion--glass-orbs)
- [`GLOW-68` حافة نيون من ألوان الواجهة وإضاءة نابضة](#glow-68--حافة-نيون-من-ألوان-الواجهة-وإضاءة-نابضة--accent-rim-rig-from-the-ui-palette-pulsing)
- [`GLOW-69` استوديو كريمي بثلاث إضاءات](#glow-69--استوديو-كريمي-بثلاث-إضاءات--cream-studio-sweep-with-a-soft-3-light-rig)
- [`GLOW-70` ظل وانعكاس متسقان مع مفتاح واحد](#glow-70--ظل-وانعكاس-متسقان-مع-مفتاح-واحد--one-key-consistency-shadow-lit-edge--reflection)
- [`GLOW-71` قراءة إضاءة صورة مرجعية](#glow-71--قراءة-إضاءة-صورة-مرجعية--read-the-light-of-a-reference-image)
- [`GLOW-72` وصفات إضاءة مقفلة لمولدات الصور والفيديو](#glow-72--وصفات-إضاءة-مقفلة-لمولدات-الصور-والفيديو--locked-lighting-phrases-for-ai-plates)
- [`GLOW-73` سماء فيزيائية وشمس وبيئة من تدرج](#glow-73--سماء-فيزيائية-وشمس-وبيئة-من-تدرج--physical-sky-sun-fill--gradient-environment)
- [`GLOW-74` ضوء متسلل بين الأوراق](#glow-74--ضوء-متسلل-بين-الأوراق--dappled-sunlight-komorebi-gobo)
- [`GLOW-75` كاوستكس تحت الماء](#glow-75--كاوستكس-تحت-الماء--underwater-caustics--absorption)
- [`GLOW-76` التعريض الطويل وخطوط الضوء](#glow-76--التعريض-الطويل-وخطوط-الضوء--long-exposure-lighten-stack--continuous-light-trails)
- [`GLOW-77` هالات ومخاريط المصابيح ثنائية الأبعاد](#glow-77--هالات-ومخاريط-المصابيح-ثنائية-الأبعاد--2d-practical-halos-lamp-cones-lit-windows--fireflies)
- [`GLOW-78` أضواء المدينة الليلية ثلاثية الأبعاد](#glow-78--أضواء-المدينة-الليلية-ثلاثية-الأبعاد--3d-night-practicals-sodium-lamps-additive-point-sprites--bokeh)
- [`GLOW-79` ارتعاش الفانوس والشمعة](#glow-79--ارتعاش-الفانوس-والشمعة--lantern--candle-flicker-organic)
- [`GLOW-80` شعاع منارة دوّار](#glow-80--شعاع-منارة-دوّار--rotating-lighthouse--beacon-beam)
- [`GLOW-81` قمر مرسوم بهالة](#glow-81--قمر-مرسوم-بهالة--painted-moon-with-halo)
- [`GLOW-82` انعكاس الضوء على الأرض المبللة والماء](#glow-82--انعكاس-الضوء-على-الأرض-المبللة-والماء--wet-floor--water-reflections-of-light-and-titles)
- [`GLOW-83` حقل حراري وتلوين دوبلر](#glow-83--حقل-حراري-وتلوين-دوبلر--thermal-heat-ramp-field--doppler-beamed-glow)
- [`GLOW-84` عناوين الضباب وشق الضوء وكشف الفخامة الهادئة](#glow-84--عناوين-الضباب-وشق-الضوء-وكشف-الفخامة-الهادئة--fog-layer--light-slit-titles-quiet-premium)
- [`GLOW-P01` كتابة مسار نيون نقطية بطبقتي توهج في Pillow](#glow-p01--كتابة-مسار-نيون-نقطية-بطبقتي-توهج-في-pillow--raster-neon-path-write-in-pillow-blurred-halo--hot-core)
- [`GLOW-X01` مرور العدسة «مصوَّر لا مرسوم»](#glow-x01--مرور-العدسة-مصوَّر-لا-مرسوم--photographed-lens-pass-barrel-fringes-bloom-vignette-grain)
- [`GLOW-X02` نواة توهج ملوّنة وحدود الوميض](#glow-x02--نواة-توهج-ملوّنة-وحدود-الوميض--tinted-bloom-cores-and-flash-limits)

## البطاقات / cards

### `GLOW-01` — لافتة نيون عربية حيّة / Living Arabic neon sign (ignition · wall light · wet reflection · synced hum)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لافتة «قهوة» تشتعل على جدار طوب مبلل، و«OPEN LATE» حرفًا حرفًا بحرف T معطوب، وفنجان يُرسم بضوء يسري، وكل ذلك ينعكس على الأرض والصوت من الجدول نفسه. / A 10 s 9:16 neon-sign film: «قهوة» ignites on wet bricks, OPEN LATE lights letter by letter with a faulty T, a cup draws on with a travelling hot spot, the floor reflects it all and the sound comes from the same schedule.

**متى:** حين يطلب المستخدم لافتة نيون عربية تشتعل على جدار مبلل مع انعكاس على الأرض وطنين متزامن / when the user wants an Arabic neon sign that ignites with wall light, wet-floor reflection and synced hum

**كيف:** Seek-driven Canvas page (window.__kosif.seek) rendered with render_html.cjs. Emission layer E = pure tube colour × level, then composited 5× with globalCompositeOperation 'lighter', each copy blurred; radii ≥26 px are blurred at ½ or ¼ resolution and scaled up (cheap and identical-looking). Wall light = ¼-res light map (ambient #1b1f30 + 40 px blur ×1.0 + 140 px blur ×1.95) multiplied onto a seeded brick albedo, so bricks take the sign colour and mortar stays dark. White-hot core from a distance field of the glyph mask (edge colour → mid at d1 → core at d2; Arabic 5/12 px, Latin 4/9 px) — never strokeText, because variable-font outlines overlap and the stroke draws seams through joined Arabic letters. Arabic word stays whole (browser-shaped); Latin letters are separate tubes. Camera push 1.0→1.075 + ±2 px handheld; reflection = 3 px flipped strips with ripple, sharp in puddles + 16 px blur film, Fresnel fade .9→.25; 90 rain streaks lit by the sign; grain + vignette. Sound: 120 Hz hum ∝ lit level, crackle on each rising edge, wet car pass panned with the headlight, normalised to −14 LUFS. (code snippet in references/powers/light-glow-bloom.md)

**المعاملات:** glow stack [3 px α.95, 10 α.75, 26 α.55 @½, 64 α.42 @¼, 140 α.30 @¼]; pink #ff2d95/#ff8fc8/#fff1f8, cyan #17d9ff/#93f0ff/#f0fdff, amber #ff9a1a/#ffc77a/#fff7e8, unlit glass #2a1820 rim #6a3a52; Cairo variable wght 420 @270 px (Arabic), 640 @100 px +22 px tracking (Latin), tube ≈20 px; verify 13/13: 1080×1920, 30 fps, 300 frames, 10.000 s, −14.1 LUFS, TP −1.4 dBFS; ≈13 min render on 4 cores

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نيون · لافتة · توهج · انعكاس · مطر · neon · sign · glow · lighter · reflection · rain · 9:16 · arabic · لافتة مضيئة · يافطة نيون · لافتة قهوة · glowing sign · neon ignition

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/index.html`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/schedule.js`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/sound.py`

#### 7. قدرات قريبة في العائلة

- `GLOW-02` جدول الاشتعال والوميض المعطوب / Ignition & faulty-tube flicker schedule (proven)
- `GLOW-03` أنبوب نيون SVG بأربع طبقات / SVG neon tube (4-stroke stack) (proven)

### `GLOW-02` — جدول الاشتعال والوميض المعطوب / Ignition & faulty-tube flicker schedule

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الأنابيب تشتعل من جدول JSON واحد من مقاطع [بداية، نهاية، شدة] يقرأه الرسم والصوت معًا: توهج مسبق، ضربات بإطار واحد، انقطاعات، ثم تسخين. / Tubes light from one JSON schedule of [start, end, level] segments read by both picture and sound: pre-glow, one-frame strikes, dropouts, then a warm-up ramp.

**متى:** عند الحاجة لوميض نيون معطوب أو تشغيل متقطع يتزامن فيه الضوء والصوت من جدول واحد / when neon tubes need a faulty flicker or ignition sequence with picture and sound driven by one schedule

**كيف:** schedule.js holds plain JSON after 'window.NEON_SCHEDULE ='; segLevel(segs,t) returns the level of the active segment (0 outside), the last segment ends at 99 (stays lit) with a warm-up; hum = 1 − 0.035·sin(2π·4.7·t) − 0.03·noise per tube. Latin letters start at 2.3 + 0.1·i with their own 3-segment pattern; one 'faulty' tube gets extra dropouts. sound.py parses the same JSON (regex) → crackle on every rising edge, 120 Hz hum (+harmonics) ∝ lit level, buzz on the faulty tube. Alternatives: SVG sign flicker opacity .45 + .25·sin(1.4t); HyperFrames neon-flicker primitive anchored to hold/texture events (best span 0.5–2.5 s).

**المعاملات:** arabic [[.50,.70,.12],[.70,.733,.9],[.80,.833,.35],[.967,1,1],[1.10,1.233,.6],[1.30,1.333,.95],[1.40,1.433,.45],[1.50,99,1]]; warm-up 0.5 s outCubic; latin pattern [[0,.034,.85],[.10,.134,.45],[.20,99,1]]; faulty dropouts 7.80–7.967 s; one frame at 30 fps = 0.033 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** وميض · اشتعال · تشغيل · طنين · flicker · ignition · schedule · hum · sound sync · neon · لمبة بتقطع · تزامن الصوت · أنبوب معطوب · faulty tube · warm-up · flicker timing

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/schedule.js`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/sound.py`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/neon-flicker/scene.html`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:124`

#### 7. قدرات قريبة في العائلة

- `GLOW-01` لافتة نيون عربية حيّة / Living Arabic neon sign (ignition · wall light · wet reflection · synced hum) (proven)
- `GLOW-03` أنبوب نيون SVG بأربع طبقات / SVG neon tube (4-stroke stack) (proven)
- `GLOW-04` توهج النص النيوني بثلاثة ظلال لكل كلمة / Neon text glow (triple shadow, per word) (proven)

### `GLOW-03` — أنبوب نيون SVG بأربع طبقات / SVG neon tube (4-stroke stack)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خط لافتة نيون من أربع ضربات للمسار نفسه: هالتان عريضتان باهتتان، والأنبوب الملون، وقلب رفيع شبه أبيض. / A neon line drawn as four stacked strokes of one path: two wide faint halos, the coloured tube and a thin near-white core.

**متى:** حين تحتاج خطًا أو لافتة نيون حادة بأي مقاس دون مرشحات في SVG / for crisp, filter-free neon lines or signs in SVG that stay sharp at any scale, with a cheap flicker

**كيف:** Same path four times, round caps/joins; animate group opacity for flicker. Cheap (no filters), crisp at any scale, and the tested midnight-cat scene uses it for signs. (code snippet in references/powers/light-glow-bloom.md)

**المعاملات:** w 1.7–3 px; 7w @ .045, 3w @ .12, w @ 1, 0.24w #f2ffff @ .85; flicker .45 + .25·sin(1.4t)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نيون · SVG · خطوط · neon tube · svg · stroke stack · line art · city · خط مضيء · أنبوب نيون · رسم متجه · glow line · vector neon

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:13`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:13`

#### 7. قدرات قريبة في العائلة

- `GLOW-01` لافتة نيون عربية حيّة / Living Arabic neon sign (ignition · wall light · wet reflection · synced hum) (proven)
- `GLOW-02` جدول الاشتعال والوميض المعطوب / Ignition & faulty-tube flicker schedule (proven)
- `GLOW-04` توهج النص النيوني بثلاثة ظلال لكل كلمة / Neon text glow (triple shadow, per word) (proven)
- `GLOW-05` توهج الكلمة النشطة في الترجمة / Active caption-word glow (install)

### `GLOW-04` — توهج النص النيوني بثلاثة ظلال لكل كلمة / Neon text glow (triple shadow, per word)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثلاثة ظلال متراكبة 8 و24 و64 بكسل بلون واحد تجعل النص أنبوب نيون، تُطبَّق على كل كلمة لا على الحاوية. / Three stacked text-shadows (8, 24, 64 px) in one colour make type read as neon — applied per word span, never on the parent.

**متى:** حين يطلب المستخدم عنوانًا أو كلمة بشكل نيون متوهج، بما فيها الكلمات العربية المتصلة / when the user wants a headline or word styled as glowing neon text, including joined Arabic words

**كيف:** text-shadow: 0 0 8px C, 0 0 24px C, 0 0 64px rgba(C,.6); fill a near-white tint (#eafcff) so the core reads hot. Arabic: one inline-block span per whole word inside direction:rtl. Glow on a parent with translucent children draws a visible rectangle — put it on the active word only. Style rules from the neon sheets: near-black #05060A, max 2 neon colours (#39FF14 / #FF2BD6 / #00E5FF), ≤3 flashes/s, RGB split only 2 frames. Scaffold the house style with `python3 tools/kosif.py scaffold neon-tech <dir>` (seeded particle bursts 400–1300 px/s, 150–600 particles). Verified in this container 2026-10-16: Arabic «نور الليل» with per-word spans rendered through render_html.cjs (VERIFY OK 2.4 s, 30 fps).

**المعاملات:** C = #00E5FF; blur 8/24/64 px, last at α .6; ≤2 colours; ≤3 flashes/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نيون · ظل النص · عنوان · neon text · text-shadow · neon-tech · cyber · per word · نص متوهج · كتابة نيون · خط مضيء · glowing text · css glow

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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
- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/audio-reactive.md`
- `kosif-tool/styles/neon-tech/SKILL.md`
- `kosif-tool/tools/render_html.cjs`

#### 7. قدرات قريبة في العائلة

- `GLOW-02` جدول الاشتعال والوميض المعطوب / Ignition & faulty-tube flicker schedule (proven)
- `GLOW-03` أنبوب نيون SVG بأربع طبقات / SVG neon tube (4-stroke stack) (proven)
- `GLOW-05` توهج الكلمة النشطة في الترجمة / Active caption-word glow (install)
- `GLOW-06` ترجمة عربية بتوهج ASS مزدوج الطبقة / Two-layer ASS glow for Arabic captions (proven)

### `GLOW-05` — توهج الكلمة النشطة في الترجمة / Active caption-word glow

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames (Apache-2.0) components animate with GSAP 3.14 — GSAP standard 'no charge' license (gsap.com/standard-license), not OSI. |

**ما هي:** الكلمة المنطوقة أو المميزة بنجمة تتوهج بلون التمييز داخل الترجمة. / The spoken (or starred) caption word glows in the accent colour.

**متى:** حين يريد المستخدم أن تتوهج الكلمة المنطوقة داخل الترجمة أو السبتايتل بلون مميز / when the spoken or highlighted word in captions should glow in an accent colour

**كيف:** Canvas: shadowColor = accent, shadowBlur = 0.5 × fontSize, offset 0, on the active word only (Basma 'glow' highlight; AutoEdit caption style 'neon'). HyperFrames caption-neon-glow component for HTML films. Keep the glow on the word, not the line box.

**المعاملات:** shadowBlur 0.5·fontSize; neon pair #FF0099 / #00FFF0; accent set #FCFF00 #53FF01 #FF0002

**التثبيت:** cd /home/user/app && npm install # Basma Studio (Vite) — or: npx hyperframes@0.8.164 add caption-neon-glow

**الوسوم:** ترجمة · كاريوكي · كلمة نشطة · captions · karaoke · active word · neon caption · highlight · سبتايتل · تمييز الكلمة · ترجمة متوهجة · word highlight · subtitle glow

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `npm:esbuild` ← npm ls esbuild أو وجود node_modules/esbuild
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `app/public/js/00_editor.js:403`
- `app/public/js/00_editor.js:2352`
- `kosif-one/vendor/hyperframes/registry/components/caption-neon-glow/caption-neon-glow.html`

#### 7. قدرات قريبة في العائلة

- `GLOW-03` أنبوب نيون SVG بأربع طبقات / SVG neon tube (4-stroke stack) (proven)
- `GLOW-04` توهج النص النيوني بثلاثة ظلال لكل كلمة / Neon text glow (triple shadow, per word) (proven)
- `GLOW-06` ترجمة عربية بتوهج ASS مزدوج الطبقة / Two-layer ASS glow for Arabic captions (proven)
- `GLOW-07` مرشح توهج SVG ونسخة مموهة / SVG blur-merge glow & blurred duplicate (proven)

### `GLOW-06` — ترجمة عربية بتوهج ASS مزدوج الطبقة / Two-layer ASS glow for Arabic captions

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** توهج تحت الترجمة العربية برسم السطر نفسه مرتين: طبقة خلفية بحد سميك شبه شفاف وطبقة أمامية بحد رفيع حاد، وكلاهما يكبر قليلًا وهو يصعد. / A glow under Arabic captions by drawing the same line twice: a back layer with a thick semi-transparent outline and a crisp front layer, both scaling up slightly as they rise.

**متى:** عند حرق ترجمة عربية بتوهج ناعم تحتها وحركة صعود خفيفة عبر ملفات ASS وffmpeg / for burning Arabic subtitles with a soft glow layer and a gentle rise-in using ASS styles and ffmpeg

**كيف:** Two ASS styles: 'Glow' on Layer 0 (outline 9, primary alpha &H80, optional \blur6) and 'Main' on Layer 1 (outline 3, shadow 2) with identical override tags \move(360,1060,360,1020,0,650)\fad(230,400)\fscx94\fscy94\t(0,650,\fscx100\fscy100); opening title \move(360,1030,360,950,0,950)\fad(300,650) \fscx88→107 over 950 ms. Swap ',' for the Arabic comma '،'. Verified here 2026-10-16 with Tajawal Bold: the default libass shaping turned the isolated ا of «القلب» into an empty box (with Cairo too) — pass shaping=complex and ship the font via fontsdir. (code snippet in references/powers/light-glow-bloom.md)

**المعاملات:** Noto Kufi Arabic (or Tajawal/Cairo) 57 px glow/main, 79 px title; Glow outline 9 α 0x80 (#DFF2FF / outline #8B5D3E); Main outline 3 shadow 2; MarginV 205–210; PlayRes 720×1280

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ترجمة · ASS · توهج · libass · ffmpeg · captions · glow · arabic subtitles · shaping · سبتايتل عربي · حرق الترجمة · ترجمة متحركة · burned subtitles · subtitle styling

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-one/projects/KOSIF_Motion_Ghorba/tools/render_ghorba_preview.py:52-77`
- `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:52-54`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/_shared/fonts/Tajawal-Bold.ttf`

#### 7. قدرات قريبة في العائلة

- `GLOW-04` توهج النص النيوني بثلاثة ظلال لكل كلمة / Neon text glow (triple shadow, per word) (proven)
- `GLOW-05` توهج الكلمة النشطة في الترجمة / Active caption-word glow (install)
- `GLOW-07` مرشح توهج SVG ونسخة مموهة / SVG blur-merge glow & blurred duplicate (proven)
- `GLOW-08` رأس ضوئي يسري على الخط وشطب متوهج / Travelling light head on a stroke (glint, comet, glowing strike) (proven)

### `GLOW-07` — مرشح توهج SVG ونسخة مموهة / SVG blur-merge glow & blurred duplicate

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مسار أو شكل يتوهج بدمج نسخة مموهة منه تحت الشكل الحاد. / A path or shape glows by merging a Gaussian-blurred copy under the crisp original.

**متى:** حين يحتاج مسار أو شكل SVG إلى توهج ناعم حوله، أو ضوء ارتطام كبير يملأ الإطار / when an SVG path or shape needs a soft glow around it, or a big full-frame impact light

**كيف:** <filter x=-50% y=-50% width=200% height=200%> feGaussianBlur stdDeviation 6 → feMerge(blur, SourceGraphic). For light sources draw the blurred copy (filters blur3/blur8/blur20, opacity .9) then the sharp shape on top; a big impact light is a full-frame radialGradient rect. Without filters: duplicate layer, blur, 30% opacity. Verified here in the render_html test (gold arc, stdDeviation 6).

**المعاملات:** stdDeviation 3 / 6 / 8 / 20; region −50%..200%; impact glow r 560 #fdba74 .75 → #f97316 0; end-card wave blur 12 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** SVG · مرشح · تمويه · svg filter · feGaussianBlur · feMerge · blurred duplicate · glow · توهج · هالة · شكل مضيء · soft glow · vector glow

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-one/projects/duck-vs-dragon/duck_dragon.py:61-63`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:56`
- `kosif-studio/motion/projects/premium_edit/index.html:56`
- `kosif-tool/styles/pm-aschapmann-131210/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-05` توهج الكلمة النشطة في الترجمة / Active caption-word glow (install)
- `GLOW-06` ترجمة عربية بتوهج ASS مزدوج الطبقة / Two-layer ASS glow for Arabic captions (proven)
- `GLOW-08` رأس ضوئي يسري على الخط وشطب متوهج / Travelling light head on a stroke (glint, comet, glowing strike) (proven)
- `GLOW-09` خط كهربائي متوهج برأس أبيض / Electric draw-head route line (install)

### `GLOW-08` — رأس ضوئي يسري على الخط وشطب متوهج / Travelling light head on a stroke (glint, comet, glowing strike)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقطة ساخنة تجري على مسار وهو يُرسم، أو وميض قصير يجري على حواف حرف، أو خط أحمر متوهج يشطب كلمة. / A hot spot rides a stroke as it draws, a short glint runs along an outlined glyph, or a glowing red line strikes a word out.

**متى:** حين يُرسم خط أو حرف ويريد المستخدم نقطة ضوء تجري عليه، أو شطب كلمة بخط أحمر متوهج / when a stroke or glyph draws on with a light dot riding it, or a word is struck out with a glowing red line

**كيف:** SVG path pathLength=1, stroke-dashoffset 1→0 (~1 s); head = getPointAtLength(L·p) drawn as a 4–6 px white dot with a 12 px glow; or a second dash of length 0.04 (≈8% of length) at the same offset in the accent with drop-shadow 6–12 px; fade the head over 0.5 s after arrival. Pulses travel at constant speed (2400 px/s) and the target blooms .6→1 with 5% overshoot in 400 ms. Strike: 4 px red #e8322a scaleX 0→1 from the reading start, 400 ms power3.out, 10 px glow, then swap the word. Arabic: start the head on the right. Verified here (neon cup head; render_html arc with head).

**المعاملات:** draw ~1 s; head dash .04; glow 6–12 px; pulse 2400 px/s, 40 px glow; strike 400 ms; Basma pen head r .07·m α .42 + 8 sparks

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** رأس ضوئي · رسم · مذنب · شطب · light head · draw-on · comet · tracing beam · strike-through · glint · نقطة مضيئة · رسم الخط · شطب كلمة · light trail · stroke reveal

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/index.html`
- `kosif-one/vendor/hyperframes/registry/components/tracing-beam/tracing-beam.html`
- `app/public/js/10_studio.js:292`
- `kosif-tool/styles/pm-influencer-seo-ce8c33/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-06` ترجمة عربية بتوهج ASS مزدوج الطبقة / Two-layer ASS glow for Arabic captions (proven)
- `GLOW-07` مرشح توهج SVG ونسخة مموهة / SVG blur-merge glow & blurred duplicate (proven)
- `GLOW-09` خط كهربائي متوهج برأس أبيض / Electric draw-head route line (install)
- `GLOW-10` توهج فوسفوري وخطوط نيون على Canvas / Phosphor / canvas neon stroke glow (seen)

### `GLOW-09` — خط كهربائي متوهج برأس أبيض / Electric draw-head route line

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Remotion company license (free for individuals and small teams; companies above the threshold need a paid license — remotion.dev/license). |

**ما هي:** مسار أو نهر يُرسم وآخر 3% منه أبيض ساخن فوق قلب ثلجي وتوهج أزرق، ثم يخبو الرأس بعد الوصول. / A route or river whose leading 3% glows white-hot over an icy core and blue glow, the head fading after arrival.

**متى:** عند رسم مسار على خريطة أو نهر بخط أزرق كهربائي يتقدمه رأس أبيض ساخن / for drawing a map route or river as an electric blue line led by a white-hot head

**كيف:** Four stacked line layers bottom→top: glow #49C6FF width 11 opacity .32 blur 6; core #E8F7FF width 3; head-glow rgba(120,225,255,.95) width 16 blur 9; head #FFFFFF width 4.5. Head source = slice from (drawn − 3%) to drawn; head opacity 1 while drawing, 0 over 0.5 s after. No dark casing under it. The same stack ports 1:1 to SVG in render_html.

**المعاملات:** head = last 3%; widths 11/3/16/4.5; blur 6/9; fade 0.5 s; bg #101315

**التثبيت:** npm i remotion@4.0.536 @remotion/cli@4.0.536 maplibre-gl@6.14.0

**الوسوم:** خريطة · مسار · كهربائي · route · map · river · electric line · draw head · remotion · خط سير · رسم مسار · خريطة متحركة · animated map · route line · glowing path

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `npm:maplibre` ← npm ls maplibre أو وجود node_modules/maplibre
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-explainer-architecture.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/assets/tokens.ts`

#### 7. قدرات قريبة في العائلة

- `GLOW-07` مرشح توهج SVG ونسخة مموهة / SVG blur-merge glow & blurred duplicate (proven)
- `GLOW-08` رأس ضوئي يسري على الخط وشطب متوهج / Travelling light head on a stroke (glint, comet, glowing strike) (proven)
- `GLOW-10` توهج فوسفوري وخطوط نيون على Canvas / Phosphor / canvas neon stroke glow (seen)
- `GLOW-11` حافة متدرجة متوهجة وظل بلون العنصر / Gradient rim-glow border & hue-matched glow shadow (install)

### `GLOW-10` — توهج فوسفوري وخطوط نيون على Canvas / Phosphor / canvas neon stroke glow

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خطوط راسم إشارات خضراء تتوهج وتترك أثرًا باهتًا، وحلقة نشطة أقوى من البقية. / Oscilloscope-green strokes glow and leave a fading afterglow; the active ring outshines the rest.

**متى:** حين يطلب المستخدم شكل شاشة راسم إشارات بخطوط خضراء متوهجة تترك أثرًا يخبو / when the user wants green oscilloscope-style glowing strokes on canvas with a fading afterglow

**كيف:** Build recipe: Canvas globalCompositeOperation 'lighter', strokeStyle #4dff9a at α .6, shadowBlur 10–14 with shadowColor = stroke; two passes per path (wide faint + thin bright 1.5–2 px) on #030706; persistence = redraw last frame at ~.85 before drawing the new one; additive overlaps brighten. Rings: shadowBlur 12–20, active α 1, others .6.

**المعاملات:** core 1.5–2 px; blur 10–14 px; bg #030706; persistence ≈ .85/frame

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** فوسفور · راسم · oscilloscope · phosphor · canvas · shadowBlur · afterglow · rings · أثر ضوئي · خطوط متوهجة · إشارة خضراء · green glow · trail fade

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `style:pm-rneayan-ea6129`
- `style:pm-kantamk-61f410`

#### 7. قدرات قريبة في العائلة

- `GLOW-08` رأس ضوئي يسري على الخط وشطب متوهج / Travelling light head on a stroke (glint, comet, glowing strike) (proven)
- `GLOW-09` خط كهربائي متوهج برأس أبيض / Electric draw-head route line (install)
- `GLOW-11` حافة متدرجة متوهجة وظل بلون العنصر / Gradient rim-glow border & hue-matched glow shadow (install)
- `GLOW-12` كلمة من نقاط مضيئة / Dot-matrix glowing word (seen)

### `GLOW-11` — حافة متدرجة متوهجة وظل بلون العنصر / Gradient rim-glow border & hue-matched glow shadow

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames (Apache-2.0) components animate with GSAP 3.14 — GSAP standard 'no charge' license (gsap.com/standard-license), not OSI. |

**ما هي:** كبسولة أو بطاقة أو هاتف بحافة متدرجة تتوهج من نسخة مموهة خلفها، وأيقونة بظل ملون من لونها. / A pill, card or phone with a gradient rim glowing from a blurred duplicate behind it; icons with a shadow in their own hue.

**متى:** حين تحتاج كبسولة أو بطاقة أو هاتفًا بحافة متدرجة متوهجة، أو أيقونة بظل من لونها / for giving a pill, card or phone mockup a glowing gradient rim, or icons a shadow in their own colour

**كيف:** Rim: black rounded rect (radius 999 px), 2 px conic-gradient border (green→yellow→red or #d946ef→#6c3bff), blurred duplicate 20–40 px behind. Focus: box-shadow 0 0 24px accent@40%. Drawn version: HyperFrames outline-draw (conic border drawn clockwise, clean closure). Hue shadow: 0 20px 50px rgba(hue,.35) under a glossy squircle; hex badge = gradient stroke + drop-shadow 0 0 12px gold; padlock keyhole glow blur 20 px as the shackle drops in 250 ms.

**المعاملات:** border 2 px; blur 30 px; focus 24 px @40%; outline-draw thickness 6 (1–20) radius 24 (0–80) progress 0–100

**التثبيت:** npx hyperframes@0.8.164 add outline-draw

**الوسوم:** حافة · بطاقة · أيقونة · ظل ملون · rim glow · border · conic gradient · focus · icon shadow · badge · إطار متوهج · حدود ملونة · كبسولة · glowing border · gradient outline

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-one/vendor/hyperframes/registry/components/outline-draw/outline-draw.html`
- `style:product`
- `style:pm-jazzen-chen-4542ae`
- `style:pm-wozu-co-242285`

#### 7. قدرات قريبة في العائلة

- `GLOW-09` خط كهربائي متوهج برأس أبيض / Electric draw-head route line (install)
- `GLOW-10` توهج فوسفوري وخطوط نيون على Canvas / Phosphor / canvas neon stroke glow (seen)
- `GLOW-12` كلمة من نقاط مضيئة / Dot-matrix glowing word (seen)
- `GLOW-13` نفق نيون واندفاع للأمام / Neon tunnel / streak zoom-through (seen)

### `GLOW-12` — كلمة من نقاط مضيئة / Dot-matrix glowing word

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كلمة تُبنى من شبكة نقاط مضيئة تتوهج مع وميض في وسطها. / A word built from a grid of glowing dots, with a flare at the centre.

**متى:** حين يطلب المستخدم كلمة مبنية من نقاط مضيئة كلوحة LED مع ومضة في وسطها / when a word should be built from glowing dots like an LED board, with a flare at the centre

**كيف:** Build recipe: render the shaped WHOLE word to an offscreen canvas (Arabic stays joined), sample its alpha on a grid, draw a 4 px dot where alpha > .5 with additive blending, then a 20 px bloom pass and a soft flare at the centre; reveal dots by distance from centre.

**المعاملات:** dot 4 px; bloom 20 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نقاط · LED · dot matrix · led · sampling · glow word · شاشة ليد · نص منقط · حروف مضيئة · led board · dotted text

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `style:pm-lukasersil-0ed38e`

#### 7. قدرات قريبة في العائلة

- `GLOW-10` توهج فوسفوري وخطوط نيون على Canvas / Phosphor / canvas neon stroke glow (seen)
- `GLOW-11` حافة متدرجة متوهجة وظل بلون العنصر / Gradient rim-glow border & hue-matched glow shadow (install)
- `GLOW-13` نفق نيون واندفاع للأمام / Neon tunnel / streak zoom-through (seen)
- `GLOW-14` توهج مضاف متدرج في الرسم بالكود / Painter additive glow stack (blades, magic, embers) (proven)

### `GLOW-13` — نفق نيون واندفاع للأمام / Neon tunnel / streak zoom-through

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حلقات نيون مستطيلة أو قضبان ضوء تندفع نحو الكاميرا مع خطوط سرعة وتوهج. / Neon rounded-rect rings or light bars rush toward camera with speed lines and bloom.

**متى:** عند الحاجة لانتقال سريع يندفع عبر نفق حلقات نيون أو قضبان ضوء نحو الكاميرا / for a fast transition that rushes through a tunnel of neon rings or light bars toward camera

**كيف:** Build recipe: 20–30 rounded-rect rings (red/blue/white) with scale = 1/z as z decreases each frame, additive blend; radial speed lines; 2–3 frames of horizontal slice glitch at the peak. Bar variant: bright coloured bars stretch toward camera over 500 ms, bloom 1.5, sparks.

**المعاملات:** 20–30 rings; 500 ms; bloom strength 1.5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نفق · اندفاع · انتقال · tunnel · zoom-through · speed lines · neon · transition · ترانزيشن · نفق ضوئي · زووم سريع · light tunnel · fly-through

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `style:pm-prasenx-8d9323`
- `style:pm-spearwtf-3c1fd1`

#### 7. قدرات قريبة في العائلة

- `GLOW-11` حافة متدرجة متوهجة وظل بلون العنصر / Gradient rim-glow border & hue-matched glow shadow (install)
- `GLOW-12` كلمة من نقاط مضيئة / Dot-matrix glowing word (seen)
- `GLOW-14` توهج مضاف متدرج في الرسم بالكود / Painter additive glow stack (blades, magic, embers) (proven)
- `GLOW-15` وصفة البرق والقوس الكهربائي / Lightning bolt, electric arc & 3D double flash (ready)

### `GLOW-14` — توهج مضاف متدرج في الرسم بالكود / Painter additive glow stack (blades, magic, embers)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ضوء يفيض من شكل: الشكل نفسه يُملأ بالإضافة ويموَّه بنصف قطر، ويتكرر بأنصاف أقطار متناقصة. / Light spilling from a shape: the shape filled additively and blurred, repeated at shrinking radii.

**متى:** حين ترسم بالكود سيفًا مضيئًا أو سحرًا أو جمرًا يفيض منه الضوء بطبقات توهج متدرجة / when code-painting a glowing blade, magic or embers with light spilling out in stacked glow layers

**كيف:** glow(shape, colour, radius, alpha) == fill(shape, colour, alpha, blur=radius, mode='add') on the float canvas; stack 2–3 glows of decreasing radius, then the solid near-white fill. Ran here 2026-10-16: render.py rendered the blade stack + shade + rim + flare at 600×400 in 0.12 s. (code snippet in references/powers/light-glow-bloom.md)

**المعاملات:** blade: glow 40 #1a8cff .5 → 14 #3fd0ff .95 → 4 #b8f2ff 1 → fill #f2fdff; spill example glow(ellipse(900,200,90), '#8a7ad0', 40, .5)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سيف · سحر · رسم بالكود · blade · magic · painter · additive · render.py · glow stack · سيف مضيء · جمر · هالة سحرية · glowing blade · embers

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/render.py:407`
- `kosif-studio/scenes/dragon_girl.py:377`
- `kosif-one/tools/kosif-studio/render.py:407`
- `100-superskills/skills/pixel-studio-painter/scripts/render.py`

#### 7. قدرات قريبة في العائلة

- `GLOW-12` كلمة من نقاط مضيئة / Dot-matrix glowing word (seen)
- `GLOW-13` نفق نيون واندفاع للأمام / Neon tunnel / streak zoom-through (seen)
- `GLOW-15` وصفة البرق والقوس الكهربائي / Lightning bolt, electric arc & 3D double flash (ready)
- `GLOW-16` بركة ضوء شعاعية خلف العنوان / Hero radial glow pool (bloom-in, bounded breathe, point origin) (proven)

### `GLOW-15` — وصفة البرق والقوس الكهربائي / Lightning bolt, electric arc & 3D double flash

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** برق متعرج بفرع وتوهج أزرق عريض وقلب أبيض رفيع وغسلة سماء، أو ومضتان قصيرتان تضيئان مشهدًا ثلاثي الأبعاد. / A jagged branching bolt with a wide blue glow, thin white core and sky wash — or two short pulses lighting a 3D scene.

**متى:** حين يحتاج المشهد برقًا متعرجًا أو قوسًا كهربائيًا أو ومضتي برق تضيئان مشهدًا ثلاثي الأبعاد / when a scene needs a jagged lightning bolt, an electric arc or a double flash lighting a 3D scene

**كيف:** 2D (render.py, seeded): random walk x += U(−30,18), y += U(18,34) until y 430, one branch; glow(stroke(bolt,10), '#8fb4ff', 30, .7) + fill(stroke(bolt,2.6), '#f6f9ff') + radial screen wash .18 (#9fbcf0). 3D: flash = max(0,1−\|t−10.6\|/.09) + .55·max(0,1−\|t−10.82\|/.07) drives a 9000-intensity point light, exposure +.05·flash and cloud colour ×(1+1.6·flash) — rule: lightning = a 2-frame spike of light + exposure. Music: HyperFrames electric-arc primitive on accent/glitch events (0.1–0.6 s).

**المعاملات:** pulses 90 ms + 70 ms (2nd at 55%); bolt #8fb4ff / #f6f9ff / wash #9fbcf0

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** برق · عاصفة · كهرباء · lightning · bolt · electric arc · storm · flash · impact · صاعقة · شرارة كهربائية · ومضة برق · thunderbolt · zap

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/scenes/whale_dragon.py:107`
- `kosif-studio/scenes/duck_dragon.py:114`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:70`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/electric-arc/scene.html`

#### 7. قدرات قريبة في العائلة

- `GLOW-13` نفق نيون واندفاع للأمام / Neon tunnel / streak zoom-through (seen)
- `GLOW-14` توهج مضاف متدرج في الرسم بالكود / Painter additive glow stack (blades, magic, embers) (proven)
- `GLOW-16` بركة ضوء شعاعية خلف العنوان / Hero radial glow pool (bloom-in, bounded breathe, point origin) (proven)
- `GLOW-17` غسيل خلفية بعدة توهجات وقاعدة الخلفية الحية / Multi-blob wash, corner glows & the living-backdrop rule (ready)

### `GLOW-16` — بركة ضوء شعاعية خلف العنوان / Hero radial glow pool (bloom-in, bounded breathe, point origin)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بركة ضوء ناعمة بلون العلامة خلف العنوان أو الشعار تجذب العين بلا شكل صلب، تتفتح ثم تتنفس بحدود. / A soft brand-tinted pool of light behind the title or logo pulls the eye without a hard shape; it blooms in, then breathes within bounds.

**متى:** حين يحتاج العنوان أو الشعار ضوءًا ناعمًا خلفه بلون العلامة يجذب العين ثم يتنفس / for a soft brand-tinted light pool behind a title or logo that blooms in, then gently breathes

**كيف:** UI: radial-gradient(circle, rgba(accent,.12) 0%, transparent 70%). Film: bloom in with power2.out to peak opacity ≤ .45, then a linear-driven breathe ±6%. Logo: #0645e2 at 40% to black, radius ≈50% W, mark scales .9→1 with blur 8→0, wordmark staggers in. Point origin: 1 px #ffd2a8 dot, halo #ff7a2a α .5→0 growing 4→40 px over 3 s with a ±10% pulse every 1.2 s; swell = dot scale + halo 2× radius at .6 in 600 ms. Remotion starter: radial-gradient(120% 80% at 50% 18%, accent@.3, #0b0d12 62%) + 44 px dot grid drifting .35/.21 px per frame. Verified here (render_html test: cyan pool .45 + breathe).

**المعاملات:** alpha .12 (UI) / ≤ .45 (film); fade to 0 at 70%; breathe ±6%; point halo 4→40 px / 3 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هالة · توهج خلفي · شعار · radial glow · hero · logo · cta · breathe · backdrop · إضاءة خلفية · ظهور الشعار · لوجو · logo reveal · soft light pool

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-atlas/skills/196-landing/621-landing`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/ambient-glow-bloom.md`
- `kosif-tool/starters/remotion/src/Film.tsx:77`

#### 7. قدرات قريبة في العائلة

- `GLOW-14` توهج مضاف متدرج في الرسم بالكود / Painter additive glow stack (blades, magic, embers) (proven)
- `GLOW-15` وصفة البرق والقوس الكهربائي / Lightning bolt, electric arc & 3D double flash (ready)
- `GLOW-17` غسيل خلفية بعدة توهجات وقاعدة الخلفية الحية / Multi-blob wash, corner glows & the living-backdrop rule (ready)
- `GLOW-18` خلفيات الاستوديو الإجرائية: شفق وغروب ومدار / Studio procedural glow backdrops (aurora · sunset · grid) (proven)

### `GLOW-17` — غسيل خلفية بعدة توهجات وقاعدة الخلفية الحية / Multi-blob wash, corner glows & the living-backdrop rule

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بقع لونية ناعمة كبيرة في زوايا الخلفية، و2–5 عناصر محيطية بطيئة تُبقي المشهد حيًا. / Large soft colour blobs in the background corners, plus 2–5 slow ambient decoratives that keep a scene alive.

**متى:** عند تصميم خلفية واجهة أو مشهد ببقع لون ناعمة في الزوايا وعناصر بطيئة تبقيها حية / for a UI or scene background with soft corner colour blobs and slow ambient decoratives that keep it alive

**كيف:** Fixed ::before layer (z-index −1, pointer-events none) with two radial-gradients via color-mix: violet 7% at 58% 0% (solid 0–18%, fade 46%) + teal 5% at 18% 42% (0–12%, fade 38%). Page wash: radial-gradient(600px 400px at 95% −5%, rgba(99,102,241,.08)), (500px 380px at −5% 40%, rgba(6,182,212,.07)), (500px 380px at 100% 85%, rgba(236,72,153,.06)); editorial: 700×420 at 96% −8% rgba(75,35,119,.10) + 520×380 at −10% 45% rgba(200,163,93,.08). Living layer: pick 2–5 of breathing accent glow, ghost text at 3–8% drifting, pulsing hairlines, grain, thematic shapes. On dark grounds never a full-screen linear gradient (H.264 banding) — radial or solid + local glow + grain.

**المعاملات:** blob alphas .05–.10; ghost text 3–8%; 2–5 decoratives

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** خلفية · بقع ضوء · خلفية حية · wash · blobs · living background · banding · ui backdrop · خلفية متدرجة · بقع لونية · خلفية موقع · gradient background · ambient motion

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-audit-pro/app/globals.css:271`
- `kosif-audit-studio/dashboard-theme.css`
- `kosif-audit-studio/kosif-one-editorial-theme.css`
- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/house-style.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-15` وصفة البرق والقوس الكهربائي / Lightning bolt, electric arc & 3D double flash (ready)
- `GLOW-16` بركة ضوء شعاعية خلف العنوان / Hero radial glow pool (bloom-in, bounded breathe, point origin) (proven)
- `GLOW-18` خلفيات الاستوديو الإجرائية: شفق وغروب ومدار / Studio procedural glow backdrops (aurora · sunset · grid) (proven)
- `GLOW-19` ستارة الشفق / Aurora drift / aurora curtains (install)

### `GLOW-18` — خلفيات الاستوديو الإجرائية: شفق وغروب ومدار / Studio procedural glow backdrops (aurora · sunset · grid)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مشاهد خلفية مرسومة حيًا: شبكة مائلة تنجرف، توهج شعاعي يدور على مسار ليساجو، ثلاث حلقات بيضاوية، و38 جسيمًا. / Live-drawn backdrop scenes: drifting diagonal grid, a radial glow wandering on a Lissajous path, three rotating ellipse rings and 38 particles.

**متى:** حين يريد المستخدم خلفية متحركة جاهزة بطابع شفق أو غروب أو شبكة مع توهج متجول وجسيمات / when the user wants a ready animated backdrop preset (aurora, sunset or grid) with a wandering glow and particles

**كيف:** Click the preset (data-preset='aurora'\|'sunset'\|'grid') or set clip {type:'demo', preset}; drawDemo() paints from t. Wandering glow: createRadialGradient at x = w/2 + sin(.32t)·.13w, y = .48h + cos(.38t)·.08h, inner r·.08, outer r = .39·min(w,h); stops 0 preset colour α 0x55, .68 #77cfc017, 1 transparent.

**المعاملات:** aurora #071520→#12343a (60%)→#22584d, line #83c8cf, glow #57d2ba55, rings #65c6bb66 · sunset #22121e→#512823→#c6773c, line #ffc08b, glow #ecaa6155 · grid #101225→#272244→#41466b, glow #9985ed55; clip 6 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** شفق · غروب · خلفية · aurora · sunset · grid · lissajous · procedural backdrop · studio preset · خلفية متحركة · جسيمات · قالب خلفية · animated background · particles

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:65`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:67`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/index.html`

#### 7. قدرات قريبة في العائلة

- `GLOW-16` بركة ضوء شعاعية خلف العنوان / Hero radial glow pool (bloom-in, bounded breathe, point origin) (proven)
- `GLOW-17` غسيل خلفية بعدة توهجات وقاعدة الخلفية الحية / Multi-blob wash, corner glows & the living-backdrop rule (ready)
- `GLOW-19` ستارة الشفق / Aurora drift / aurora curtains (install)
- `GLOW-20` بقعة ضوء تتبع العنصر / Follow-spot & feathered spotlight (install)

### `GLOW-19` — ستارة الشفق / Aurora drift / aurora curtains

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames (Apache-2.0) components animate with GSAP 3.14 — GSAP standard 'no charge' license (gsap.com/standard-license), not OSI. |

**ما هي:** ثلاث بقع شفق بلون التمييز تنجرف في حلقة متصلة فوق قاعدة داكنة، أو ستائر شفق خضراء وبنفسجية بمظلل WebGPU. / Three accent-tinted aurora blobs drift in a seamless loop over a dark base — or green/violet curtains from a WebGPU shader.

**متى:** حين تحتاج خلفية شفق قطبي متحركة تدور بلا قطع أو ستائر شفق خضراء وبنفسجية / for a seamlessly looping aurora background, or green and violet aurora curtains from a shader

**كيف:** CSS: `npx hyperframes@0.8.164 add aurora-drift`, mount on a class='clip' div (data-start/duration/track-index, data-variable-values JSON); colours from the 18 theme tokens; extra duration becomes hold, never time-stretch. Shader: data-shader='Aurora' canvas in a root marked data-requires-webgpu (see GLOW-52). Seen in style:product: blurred blue-violet-purple blobs + orange at right along the bottom third of #06050a.

**المعاملات:** accent green\|blue\|violet; mood deep\|bright; faint vignette

**التثبيت:** npx hyperframes@0.8.164 add aurora-drift

**الوسوم:** شفق · خلفية · aurora · blobs · loop · hyperframes · webgpu · الشفق القطبي · خلفية متحركة · أضواء الشمال · northern lights · aurora curtains

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-one/vendor/hyperframes/registry/components/aurora-drift/aurora-drift.html`
- `kosif-one/vendor/hyperframes/registry/blocks/aurora/aurora.html`
- `style:product`

#### 7. قدرات قريبة في العائلة

- `GLOW-17` غسيل خلفية بعدة توهجات وقاعدة الخلفية الحية / Multi-blob wash, corner glows & the living-backdrop rule (ready)
- `GLOW-18` خلفيات الاستوديو الإجرائية: شفق وغروب ومدار / Studio procedural glow backdrops (aurora · sunset · grid) (proven)
- `GLOW-20` بقعة ضوء تتبع العنصر / Follow-spot & feathered spotlight (install)
- `GLOW-21` حلقات هالة متحدة المركز / Concentric halo rings (ready)

### `GLOW-20` — بقعة ضوء تتبع العنصر / Follow-spot & feathered spotlight

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames (Apache-2.0) components animate with GSAP 3.14 — GSAP standard 'no charge' license (gsap.com/standard-license), not OSI. |

**ما هي:** توهج خلفي كبير ينتقل مركزه إلى العنصر النشط، أو تعتيم كل الإطار إلا بيضاوي ناعم ينزلق بين الأهداف. / A big backdrop glow whose centre glides to the active element, or a dimmed frame except a feathered ellipse gliding between targets.

**متى:** حين يريد المستخدم تسليط الضوء على العنصر النشط وتعتيم الباقي مع انزلاق البقعة بين الأهداف / when the user wants to spotlight the active element and dim the rest, with the light gliding between targets

**كيف:** Follow: black bg + one radial (#0a3d91 ≈25%, radius ≈60% W) whose centre lerps to the active object per scene. Feather: HyperFrames yt-feather-highlight — ellipse position/size are CSS vars, so it glides. Spotlight card: scripted cursor-following spot + lit border. Pedestal: radial ellipse under the object. Paper spot: radius 15% W travelling over 3 s.

**المعاملات:** radius ≈60% W @25%; paper spot 15% W / 3 s

**التثبيت:** npx hyperframes@0.8.164 add yt-feather-highlight

**الوسوم:** بقعة ضوء · تتبع · تركيز · spotlight · follow spot · feather · focus · pedestal · تسليط الضوء · تعتيم · إبراز عنصر · highlight element · dim background

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-one/vendor/hyperframes/registry/components/yt-feather-highlight/yt-feather-highlight.html`
- `kosif-one/vendor/hyperframes/registry/components/spotlight-card/spotlight-card.html`
- `style:infographic`

#### 7. قدرات قريبة في العائلة

- `GLOW-18` خلفيات الاستوديو الإجرائية: شفق وغروب ومدار / Studio procedural glow backdrops (aurora · sunset · grid) (proven)
- `GLOW-19` ستارة الشفق / Aurora drift / aurora curtains (install)
- `GLOW-21` حلقات هالة متحدة المركز / Concentric halo rings (ready)
- `GLOW-22` نبضة وهالة لفت الانتباه / Pulse ring, halo & the attention set (ready)

### `GLOW-21` — حلقات هالة متحدة المركز / Concentric halo rings

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** دوائر زخرفية من ظلال box-shadow منتشرة بشفافية ضئيلة تعطي هالة رادار خلف المحتوى. / Decorative circles from stacked spread box-shadows at very low alpha give a radar/atmosphere halo behind content.

**متى:** عند الحاجة لحلقات هالة زخرفية خافتة كالرادار خلف محتوى أو شعار / for faint decorative concentric halo rings, radar-like, behind content or a logo mark

**كيف:** box-shadow: 0 0 0 45px rgba(255,255,255,.025), 0 0 0 95px rgba(255,255,255,.018) on a 420 px circle (studio4: #bdd1c004/#bdd1c005 at 50/100 px). Ember variant: brown-orange radial behind the mark (radius ≈35% H) + 2–3 thin 1 px rings at 20% + orbiting flare dots, rotating 10°/s.

**المعاملات:** circle 420–470 px; spreads 24/45/50/95/100 px; alpha .018–.04

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هالة · حلقات · رادار · halo · rings · box-shadow · ember · radar · دوائر · خلفية دوائر · توهج خافت · concentric circles · decorative circles

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-audit-studio/styles.css:167`
- `kosif-audit-studio/studio.css:57`
- `style:pm-robj3d3-b18fad`

#### 7. قدرات قريبة في العائلة

- `GLOW-19` ستارة الشفق / Aurora drift / aurora curtains (install)
- `GLOW-20` بقعة ضوء تتبع العنصر / Follow-spot & feathered spotlight (install)
- `GLOW-22` نبضة وهالة لفت الانتباه / Pulse ring, halo & the attention set (ready)
- `GLOW-23` كلمة تنفجر بتوهج وحلقة / Burst word with glow & expanding ring (proven)

### `GLOW-22` — نبضة وهالة لفت الانتباه / Pulse ring, halo & the attention set

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حلقة تتسع وتخبو عددًا محددًا من المرات لتأكيد حالة، ومفردات قليلة للفت الانتباه لكل منها معنى. / An outline ring scales out and fades a fixed number of times to confirm a state, plus a small vocabulary of focus effects, each with a meaning.

**متى:** حين يحتاج عنصر جديد أو حالة إلى لفت النظر بنبضة حلقة محدودة العدد أو تأثير تركيز له معنى / when a new item or state needs attention via a ring pulse that runs a fixed count, or another meaningful focus effect

**كيف:** Ring ::after with border, keyframes, iteration-count 2, then stop. Menu: pulse (new/alert, low amplitude, 1–2 cycles); halo (current focus without changing the mark); sparkle (positive discovery only); ember/fire (heat/overload — never human tragedy); glow trail (active route); shockwave (when distance from an origin matters: 1–3 circles .2→3, opacity .6→0, stroke thinning, 600–900 ms expo.out + 4 px shake for 150 ms). Progress head: 8 px #d9f3c7 dot with box-shadow 0 0 16px #d9f3c7bb at the top of the ring. Let the mark settle static.

**المعاملات:** health .55→2.4, 900 ms, delay 320 ms, ×2 (8 px teal dot + 4 px halo); current stage .85→1.45, 900 ms, delay 480 ms, ×2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نبضة · لفت انتباه · موجة صدمة · pulse · ring · attention · shockwave · halo · data focus · تنبيه · حلقة نابضة · إشعار · notification pulse · alert · focus effect

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-audit-pro/app/globals.css:576`
- `kosif-audit-studio/studio.css:73`
- `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/particle-effects-and-flow.md`
- `style:pm-maxalexweber-67688b`

#### 7. قدرات قريبة في العائلة

- `GLOW-20` بقعة ضوء تتبع العنصر / Follow-spot & feathered spotlight (install)
- `GLOW-21` حلقات هالة متحدة المركز / Concentric halo rings (ready)
- `GLOW-23` كلمة تنفجر بتوهج وحلقة / Burst word with glow & expanding ring (proven)
- `GLOW-24` هالة تتنفس مع الصوت وأشعة وغبار القصيدة / Voice/beat-breathing halo, shafts & dust (verse light) (install)

### `GLOW-23` — كلمة تنفجر بتوهج وحلقة / Burst word with glow & expanding ring

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كلمة بطلة تقفز من 0.55 إلى 1 بنابض مع توهج ناعم بينما تتسع حلقة لون التمييز حتى 1500 بكسل وتخبو. / A hero word pops 0.55→1 on a spring with a soft glow while a 6 px accent ring expands to 1500 px and fades.

**متى:** حين تحتاج كلمة بطلة تقفز بنابض مع توهج وحلقة بلون التمييز تتسع وتخبو / for a hero word that pops in on a spring with a soft glow while an accent ring expands and fades

**كيف:** Tested html-canvas starter: pop prog(local, .2, .75, spring 150/14); ring prog(local, .25, 1.3, outExpo), width 10 + r·1500; text-shadow 0 0 60px rgba(126,232,210,.55).

**المعاملات:** 220 px weight 900 #fff; glow 60 px rgba(126,232,210,.55); ring 6 px #7ee8d2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** انفجار · كلمة بطلة · حلقة · burst · pop · spring · ring · hero word · كلمة قافزة · ظهور كلمة · تأكيد · word pop · expanding ring

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-tool/starters/html-canvas/index.html:28`
- `kosif-tool/starters/html-canvas/index.html:168`

#### 7. قدرات قريبة في العائلة

- `GLOW-21` حلقات هالة متحدة المركز / Concentric halo rings (ready)
- `GLOW-22` نبضة وهالة لفت الانتباه / Pulse ring, halo & the attention set (ready)
- `GLOW-24` هالة تتنفس مع الصوت وأشعة وغبار القصيدة / Voice/beat-breathing halo, shafts & dust (verse light) (install)
- `GLOW-25` دائرة سحرية بكسل بتوهج منقّط / Pixel magic circle (dithered glow) (seen)

### `GLOW-24` — هالة تتنفس مع الصوت وأشعة وغبار القصيدة / Voice/beat-breathing halo, shafts & dust (verse light)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** هالة مركزية تتضخم مع علو الصوت والضربات، وأشعة ضوء بطيئة وغبار يطير نحو العدسة، ووميض على الجملة الختامية. / A central halo swells with loudness and kicks, slow light shafts and dust fly toward the lens, and a flare marks the payoff.

**متى:** عند تحريك هالة وأشعة وغبار ضوئي تتنفس مع علو الصوت والضربات في قصيدة أو دعاء / when a halo, light shafts and dust should breathe with voice loudness and kicks, e.g. a recited verse or prayer

**كيف:** verse.html draw(t) reads window.SOUND channels (rms, bass, kick) and state.flare. Halo radius and alpha below; drawDepth(): 9 light shafts from above, spread .13 rad, length 1.35 H, alpha .05 + .04·rms + .05·kick; 140 dust points flying at z-speed .025–.075 (near ones ×3.2 softer); payoff flare 0→1 in .5 s, back over 2.2 s; kicks send rings, onsets lift motes. Keep it subtle: no EQ bars, no strobing, no beat claim without a detector. The halo maths alone runs in any seek page (render_html verified).

**المعاملات:** R = .62·min(W,H)·(1 + .05 rms + .06 kick + .25 flare); inner α .20 + .16 rms + .14 kick + .35 flare; drum bloom 200 px / 400 ms decay

**التثبيت:** pip install faster-whisper # measured word times for verse.py; without it timings are reported as 'estimated'

**الوسوم:** صوت · دعاء · قصيدة · هالة · audio reactive · halo · verse · god rays · dust · kick · تفاعل مع الصوت · إلقاء شعري · أشعة ضوء · voice reactive · light shafts

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `100-superskills/skills/kosif-montage-motion/templates/verse.html:130`
- `100-superskills/skills/kosif-montage-motion/templates/verse.html:99`
- `kosif-studio/motion/verse.py:382`
- `kosif-one/vendor/brag/skills/brag/references/audio.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-22` نبضة وهالة لفت الانتباه / Pulse ring, halo & the attention set (ready)
- `GLOW-23` كلمة تنفجر بتوهج وحلقة / Burst word with glow & expanding ring (proven)
- `GLOW-25` دائرة سحرية بكسل بتوهج منقّط / Pixel magic circle (dithered glow) (seen)
- `GLOW-26` سلسلة ما بعد المعالجة السينمائية (makePost) / Three-kit cinematic post stack (makePost) (proven)

### `GLOW-25` — دائرة سحرية بكسل بتوهج منقّط / Pixel magic circle (dithered glow)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حلقة رونية تحت الساحر تدور بإطارات متقطعة بتوهج منقط بلون التعويذة. / A rune ring under the caster rotating in stepped frames with a dithered glow in the spell colour.

**متى:** حين يطلب المستخدم دائرة سحرية بأسلوب البكسل آرت تدور بخطوات متقطعة وتوهج منقط / when the user wants a pixel-art magic circle rotating in stepped frames with a dithered glow

**كيف:** Build recipe: ellipse ring + rune dots on a low-res canvas, rotate in steps at 8 fps (not smooth), glow as an ordered-dither halo (Bayer 4×4) instead of blur so it stays pixel-crisp; alternate two colours on the flash; upscale nearest-neighbour.

**المعاملات:** 8 fps rotation; 2-colour alternating flash

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بكسل · سحر · ريترو · pixel · magic circle · dither · retro · 8 fps · بكسل آرت · تعويذة · دائرة رونية · pixel art · spell effect

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `style:pm-0xevinho-3777d8`

#### 7. قدرات قريبة في العائلة

- `GLOW-23` كلمة تنفجر بتوهج وحلقة / Burst word with glow & expanding ring (proven)
- `GLOW-24` هالة تتنفس مع الصوت وأشعة وغبار القصيدة / Voice/beat-breathing halo, shafts & dust (verse light) (install)
- `GLOW-26` سلسلة ما بعد المعالجة السينمائية (makePost) / Three-kit cinematic post stack (makePost) (proven)
- `GLOW-27` بلوم بلون مصدره على المواد المشعة / Emissive colour-corona bloom (and hit-lit rings) (proven)

### `GLOW-26` — سلسلة ما بعد المعالجة السينمائية (makePost) / Three-kit cinematic post stack (makePost)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حارس NaN، ثم بلوم Unreal، ثم أشعة من الشمس، ثم عمق مجال، ثم تلوين وتعتيم وانحراف لوني، ثم حبيبات — في استدعاء واحد. / NaN/firefly guard → Unreal bloom → screen-space sun rays → bokeh DOF → grade (split tone, vignette, CA) → film grain → output, in one call.

**متى:** عند إضافة سلسلة ما بعد معالجة سينمائية كاملة لمشهد three.js: بلوم وأشعة وعمق مجال وحبيبات / for adding a full cinematic post stack to a three.js scene: bloom, sun rays, depth of field, grade and grain

**كيف:** Load the prebuilt bundle (three r186 inside, no npm): <script src=three-kit.bundle.js> → window.K3. post = K3.makePost(renderer, scene, camera, W, H, {bloom, bloomThreshold, aperture, maxblur, vignette, ca, grain, clampMax}); per frame post.sunOnScreen(sunDir) then post.composer.render(0). Verified here 2026-10-16 (Playwright Chromium, --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader, WebGL 2.0): emissive torus K3.kelvin(1900) + cyan orb with the defaults gave a clean corona in each source colour; bloom .9 / threshold .6 washed the whole frame orange. Realism rules: exposure .5–.62, bloom threshold ≥ .9, sun in front of lens only at sunrise; ≈1–1.5 s/frame at 1080p. (code snippet in references/powers/light-glow-bloom.md)

**المعاملات:** guard clamp 48; bloom .22 radius .6 threshold .9; rays 64 samples decay .972 ×.55; bokeh focus 900 aperture 4e-5 maxblur .0035; vignette .42; CA 1.2; grain .16; shadows tint (.92,.98,1.08) highs (1.08,1,.92)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بلوم · ما بعد المعالجة · three.js · bloom · post stack · makePost · unreal bloom · dof · grain · vignette · مظهر سينمائي · عمق المجال · حبيبات فيلم · cinematic look · sun rays · color grade

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/motion/kit/three-kit.js:361`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.bundle.js`
- `kosif-studio/tests/test_studio.py:606`
- `kosif-studio/motion/references/hyperframes-authoring.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-24` هالة تتنفس مع الصوت وأشعة وغبار القصيدة / Voice/beat-breathing halo, shafts & dust (verse light) (install)
- `GLOW-25` دائرة سحرية بكسل بتوهج منقّط / Pixel magic circle (dithered glow) (seen)
- `GLOW-27` بلوم بلون مصدره على المواد المشعة / Emissive colour-corona bloom (and hit-lit rings) (proven)
- `GLOW-28` جدول البلوم والتعريض لكل لقطة / Per-shot bloom & exposure presets (cinematic · lite · lab) (ready)

### `GLOW-27` — بلوم بلون مصدره على المواد المشعة / Emissive colour-corona bloom (and hit-lit rings)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل مصدر ساطع يلبس هالة بلونه هو، والسطوح المضاءة لا تتوهج؛ الألوان تأتي من الانبعاث فوق مشهد داكن. / Every bright source wears a halo in its own colour while lit surfaces stay clean; colour comes from emission over a dark scene.

**متى:** حين يجب أن تتوهج المصابيح والمصادر الساطعة بهالة بلونها فوق مشهد داكن دون أن تتوهج الأسطح البيضاء / when bright sources should bloom in their own colour over a dark scene while lit and white surfaces stay clean

**كيف:** Keep albedo dark (value < .2) and drive colour through emissive materials; threshold below the lamps but above lit surfaces (≥ .9 for realism, .2–.5 only for stylised neon caves); generous radius .6–.75, corona in the source colour, never grey. White objects that must not glow → selective bloom: render emissive into a separate MRT target, bloom it at threshold 0 (strength 1.5, radius .5), add to colour. Beat ring: emissive torus, on hit emissiveIntensity 4 decaying exponentially (τ ≈ 250 ms), random neon hue, bloom 1.2–1.8 at threshold .2. Verified in the K3 render above.

**المعاملات:** realism threshold ≥ .9; corona radius .6–.75; selective MRT 0 / 1.5 / .5; hit decay τ ≈ 250 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هالة لونية · انبعاث · بلوم انتقائي · emissive · corona · selective bloom · mrt · beat ring · مواد مضيئة · توهج المصابيح · كهف نيون · glowing lamps · bloom threshold

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `100-superskills/skills/kosif-montage-motion/references/book-lessons.md`
- `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/post-processing.md`
- `kosif-studio/motion/kit/three-kit.js:361`
- `style:pm-gorden-sun-041f56`

#### 7. قدرات قريبة في العائلة

- `GLOW-25` دائرة سحرية بكسل بتوهج منقّط / Pixel magic circle (dithered glow) (seen)
- `GLOW-26` سلسلة ما بعد المعالجة السينمائية (makePost) / Three-kit cinematic post stack (makePost) (proven)
- `GLOW-28` جدول البلوم والتعريض لكل لقطة / Per-shot bloom & exposure presets (cinematic · lite · lab) (ready)
- `GLOW-29` بلوم TSL وWebGPU / TSL / WebGPU bloom, selective MRT & lens nodes (install)

### `GLOW-28` — جدول البلوم والتعريض لكل لقطة / Per-shot bloom & exposure presets (cinematic · lite · lab)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل لقطة تحمل قيم البلوم والعتبة ونصف القطر والتعريض الخاصة بها، فيتغير المزاج مع القطع فورًا. / Each shot carries its own bloom strength/threshold/radius and exposure, so a cut changes mood instantly.

**متى:** عند ضبط البلوم والتعريض لكل لقطة على حدة ليتغير المزاج فورًا مع القطع / for setting bloom and exposure per shot so the mood shifts instantly on each cut

**كيف:** Plug the numbers into makePost / K3S.makeLitePost / K3.labPost (all inside the verified bundle). Exposure fades in over 0–0.35 s and drops 10% in the last 0.6 s of each shot. labPost is tuned for software GL (rays off, DOF optional). The source projects themselves bundle 'three' from npm (rebuild with the install line), but the numbers need nothing new. (full table in references/powers/light-glow-bloom.md)

**المعاملات:** see table

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إعدادات · تعريض · لقطة · presets · exposure · aces · lite post · lab post · per shot · بلوم · مزاج اللقطة · قطع · shot mood · bloom settings

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:122`
- `kosif-one/projects/egypt-2120-animation/index.html:190`
- `kosif-studio/motion/kit/shape-kit.js:365`
- `kosif-studio/motion/kit/lab-kit.js:272`

#### 7. قدرات قريبة في العائلة

- `GLOW-26` سلسلة ما بعد المعالجة السينمائية (makePost) / Three-kit cinematic post stack (makePost) (proven)
- `GLOW-27` بلوم بلون مصدره على المواد المشعة / Emissive colour-corona bloom (and hit-lit rings) (proven)
- `GLOW-29` بلوم TSL وWebGPU / TSL / WebGPU bloom, selective MRT & lens nodes (install)
- `GLOW-30` بلوم الرسم الثابت / Painter highlight bloom (stills & painted films) (install)

### `GLOW-29` — بلوم TSL وWebGPU / TSL / WebGPU bloom, selective MRT & lens nodes

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بلوم بعتبة وبلوم انتقائي وضبابية حركة وانحراف لوني كعُقد TSL في WebGPURenderer. / Threshold bloom, selective bloom, velocity motion blur and chromatic aberration as TSL nodes on WebGPURenderer.

**متى:** حين يعمل المشهد على WebGPURenderer ويحتاج بلومًا بعتبة أو انتقائيًا وضبابية حركة وانحرافًا لونيًا / when a WebGPURenderer scene needs threshold or selective bloom, velocity motion blur and chromatic aberration as nodes

**كيف:** bloom(scenePassColor) from three/addons/tsl/display/BloomNode.js, output = color.add(bloomPass); selective: emissive → MRT target, bloom at threshold 0; motionBlur(color, scenePass.getTextureNode('velocity')); chromaticAberration(color, {offset: vec2(.002)}). WebGPU in headless Chromium here needs --enable-unsafe-webgpu --enable-features=Vulkan --use-angle=swiftshader --enable-unsafe-swiftshader (adapter verified 2026-10-16; no TSL scene rendered yet).

**المعاملات:** bloom threshold .5 strength 1 radius .5; selective 0 / 1.5 / .5; CA offset .002

**التثبيت:** npm i three@0.186.1

**الوسوم:** WebGPU · TSL · بلوم · webgpu · tsl · bloom node · selective bloom · motion blur · ضبابية الحركة · انحراف لوني · ما بعد المعالجة · chromatic aberration · post processing

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/post-processing.md`
- `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/SKILL.md`
- `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-27` بلوم بلون مصدره على المواد المشعة / Emissive colour-corona bloom (and hit-lit rings) (proven)
- `GLOW-28` جدول البلوم والتعريض لكل لقطة / Per-shot bloom & exposure presets (cinematic · lite · lab) (ready)
- `GLOW-30` بلوم الرسم الثابت / Painter highlight bloom (stills & painted films) (install)
- `GLOW-31` الدمج المضاف على لوحة عائمة / Float-canvas light compositing (add / screen above 1.0) (proven)

### `GLOW-30` — بلوم الرسم الثابت / Painter highlight bloom (stills & painted films)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الضوء فوق العتبة ينسكب حوله بنصفي قطر كالعدسة على لوحة الرسم بالكود. / Light above a threshold spills into its surroundings at two radii, like a lens, on the code-painted canvas.

**متى:** عند إضافة بلوم كالعدسة حول المناطق الساطعة في صورة ثابتة أو فيلم مرسوم بالكود / for adding lens-like bloom around the bright areas of a code-painted still or painted film

**كيف:** bloom(threshold, radius, strength, tint) adds blur(hi, r)·strength·tint + blur(hi, 3r)·strength·.5·tint, where hi = max(canvas − threshold, 0). Checked here: glow/shade/rim/flare run, but bloom() and chroma() stop with ModuleNotFoundError: cv2 until OpenCV is installed.

**المعاملات:** default .75 / 30 / .6; whale .8 / 24 / .32 tint #ffe6d0; AI-plate recipe .72 / 26 / .5

**التثبيت:** pip install opencv-python-headless

**الوسوم:** بلوم · رسم · لوحة · bloom · painter · stills · opencv · render.py · وهج · إضاءة ساطعة · صورة ثابتة · highlight glow · lens bloom

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:opencv` ← python3 -c "import opencv" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/render.py:732`
- `kosif-studio/scenes/whale_dragon.py:287`
- `kosif-one/tools/kosif-studio/render.py:732`

#### 7. قدرات قريبة في العائلة

- `GLOW-28` جدول البلوم والتعريض لكل لقطة / Per-shot bloom & exposure presets (cinematic · lite · lab) (ready)
- `GLOW-29` بلوم TSL وWebGPU / TSL / WebGPU bloom, selective MRT & lens nodes (install)
- `GLOW-31` الدمج المضاف على لوحة عائمة / Float-canvas light compositing (add / screen above 1.0) (proven)
- `GLOW-32` تعتيم الأطراف / Vignette (CSS · canvas · kit · painter) (proven)

### `GLOW-31` — الدمج المضاف على لوحة عائمة / Float-canvas light compositing (add / screen above 1.0)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أربعة أوضاع دمج على لوحة float32 بلا قص، فيتجاوز الضوء المضاف 1.0 ثم ينحدر بنعومة بدل أن يُقص. / Four blend modes on an unclipped float32 canvas, so additive light can exceed 1.0 and roll off later instead of clipping.

**متى:** حين تتراكم أضواء كثيرة وتحتاج دمجًا مضافًا أو بوضع الشاشة دون قص فوق الأبيض ثم انحدارًا ناعمًا / when stacked lights need add or screen blending without clipping above white, then a smooth roll-off

**كيف:** Pass mode= to fill()/text()/noise(); screen is reg += col·a·(1 − min(reg, 1)) so glows over 1.0 are not clipped; multiply darkens for shadows/texture; render_image(rolloff .82) or filmic() (ACES-style curve) maps >1 back. Browser equivalents: Canvas globalCompositeOperation 'lighter' (add) / 'screen', CSS mix-blend-mode: screen.

**المعاملات:** mode ∈ {normal, add, screen, multiply}; alpha 0..1; paint '#rrggbbaa'; rolloff .82

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أوضاع الدمج · إضافة · شاشة · blend modes · additive · screen · float canvas · tone mapping · دمج الطبقات · تراكب الضوء · قص الإضاءة · light compositing · highlight clipping

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/render.py:366`
- `kosif-studio/render.py:397`
- `100-superskills/skills/pixel-studio-painter/scripts/render.py`

#### 7. قدرات قريبة في العائلة

- `GLOW-29` بلوم TSL وWebGPU / TSL / WebGPU bloom, selective MRT & lens nodes (install)
- `GLOW-30` بلوم الرسم الثابت / Painter highlight bloom (stills & painted films) (install)
- `GLOW-32` تعتيم الأطراف / Vignette (CSS · canvas · kit · painter) (proven)
- `GLOW-33` الانحراف اللوني للعدسة / Lens chromatic aberration (edge-weighted) (proven)

### `GLOW-32` — تعتيم الأطراف / Vignette (CSS · canvas · kit · painter)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تعتيم الحواف لتركيز العين في الوسط، بأربع طرق جاهزة. / Darkens the frame edges to focus the centre, four ready ways.

**متى:** حين يريد المستخدم تعتيم حواف الإطار لتركيز العين في الوسط بلمسة سينمائية / when the user wants darkened frame edges to pull focus to the centre with a cinematic touch

**كيف:** CSS: full-frame div box-shadow inset 0 0 160px rgba(0,0,0,.85), pointer-events none (verified in the render_html test). Canvas: radial from .3·min(W,H) transparent to .75·max(W,H) rgba(0,0,0,v). motion-kit: MOTION.vignette(stage, {inner, strength, z}). Painter: vignette(strength .5), smoothstep from d .35. Over footage: 72% × 58% ellipse to .55. HyperFrames vignette component as a drop-in.

**المعاملات:** inset 160 px α .85; canvas v 0–.8 (MK .32–.78); kit inner 55% strength .42; footage .55

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تعتيم الأطراف · فينييت · vignette · focus · edges · cinematic · تغميق الحواف · إطار داكن · تركيز النظر · dark edges · edge darkening

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:68`
- `kosif-studio/motion/kit/motion-kit.js:457`
- `app/public/js/00_editor.js:289`
- `kosif-studio/render.py`

#### 7. قدرات قريبة في العائلة

- `GLOW-30` بلوم الرسم الثابت / Painter highlight bloom (stills & painted films) (install)
- `GLOW-31` الدمج المضاف على لوحة عائمة / Float-canvas light compositing (add / screen above 1.0) (proven)
- `GLOW-33` الانحراف اللوني للعدسة / Lens chromatic aberration (edge-weighted) (proven)
- `GLOW-34` انقسام RGB على الضربة / RGB-split hit jitter (seen)

### `GLOW-33` — الانحراف اللوني للعدسة / Lens chromatic aberration (edge-weighted)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الأحمر والأزرق يتباعدان قليلًا نحو أطراف الإطار كما في عدسة حقيقية. / Red and blue drift apart toward the frame edges, as in a real lens.

**متى:** عند إضافة انفصال خفيف للأحمر والأزرق عند أطراف الإطار لمحاكاة عدسة حقيقية / for adding a subtle red/blue split toward the frame edges to mimic a real lens

**كيف:** Shader: sample R/G/B at offsets scaled by distance from centre (≈0.002 UV at the edge, zero at the centre). makePost grade pass: off = d·(ca/1920)·\|d\|·4 with d = uv − .5, so the split grows quadratically toward the edges (ca 1.2–1.4; ran in the verified K3 render); TSL chromaticAberration(color, {offset: vec2(.002)}); painter chroma(1.5) scales R/B by 1 ± amount·2/max(W,H) about the centre (needs OpenCV).

**المعاملات:** offset .002 at edges; makePost ca 1.2 (sound_ground 1.4); labPost .4

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** انحراف لوني · عدسة · chromatic aberration · lens · edges · rgb fringe · تشوه العدسة · حواف ملونة · مظهر سينمائي · color fringing · lens effect

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:opencv` ← python3 -c "import opencv" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/motion/kit/three-kit.js:361`
- `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`
- `kosif-studio/render.py:756`

#### 7. قدرات قريبة في العائلة

- `GLOW-31` الدمج المضاف على لوحة عائمة / Float-canvas light compositing (add / screen above 1.0) (proven)
- `GLOW-32` تعتيم الأطراف / Vignette (CSS · canvas · kit · painter) (proven)
- `GLOW-34` انقسام RGB على الضربة / RGB-split hit jitter (seen)
- `GLOW-35` تمويه السرعة وتلطيخ التكبير وكشف التركيز / Velocity blur, zoom-smear title & focus-pull glow (seen)

### `GLOW-34` — انقسام RGB على الضربة / RGB-split hit jitter

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نسخ حمراء وسماوية مزاحة ترتجف إطارين أو ثلاثة عند الضربة ثم يعود السكون. / Red and cyan offset copies jitter for 2–3 frames on a hit, then stillness returns.

**متى:** حين يريد المستخدم رجفة انقسام ألوان أحمر وسماوي لإطارين أو ثلاثة على الضربة ثم يعود الهدوء / when the user wants a red/cyan RGB-split jitter for 2–3 frames on a hit, then stillness

**كيف:** Build recipe: draw the layer three times with R +3 px and B −3 px in screen blend (idle 2–4 px), spike to 8–12 px on hits for 2–3 frames; text: red/cyan duplicates offset 4 px, mix-blend screen, jitter 3–5 frames; onion-skin: previous 3 frames tinted cyan/pink at 40%; add horizontal slice displacement only on heavy beats. Owner glitch pass (makeGlitchPass) exists in the trend notes but has not run here.

**المعاملات:** idle 2–4 px; hits 8–12 px for 2–3 frames; text offset 4 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** انقسام ألوان · غليتش · ضربة · rgb split · glitch · hit · chromatic · onion skin · جليتش · تشويش · اهتزاز · color split · impact jitter

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `style:pm-gizakdag-b8c59e`
- `style:pm-micheleharmonic-77628e`
- `style:pm-majin-appsheet-2d3c1a`
- `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-32` تعتيم الأطراف / Vignette (CSS · canvas · kit · painter) (proven)
- `GLOW-33` الانحراف اللوني للعدسة / Lens chromatic aberration (edge-weighted) (proven)
- `GLOW-35` تمويه السرعة وتلطيخ التكبير وكشف التركيز / Velocity blur, zoom-smear title & focus-pull glow (seen)
- `GLOW-36` مؤثرات وسائط HyperFrames وسلسلة VFX / HyperFrames media effects & per-pixel VFX chain (install)

### `GLOW-35` — تمويه السرعة وتلطيخ التكبير وكشف التركيز / Velocity blur, zoom-smear title & focus-pull glow

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تمويه اتجاهي يتبع السرعة ويختفي عند السكون، وعنوان ختامي يدخل بخطوط تكبير ثم يتوهج، وشعار يظهر من ضبابية مع توهج. / Directional blur proportional to velocity (zero at rest), an end title that enters as zoom streaks then glows, and a logo pulled into focus with a glow.

**متى:** حين تحتاج العناصر المتحركة تمويهًا اتجاهيًا حسب السرعة، أو عنوانًا ختاميًا بخطوط تكبير، أو شعارًا يظهر من الضبابية / for velocity-based directional blur, an end title entering as zoom streaks, or a logo pulled into focus

**كيف:** Build recipe: per layer compute velocity; SVG feGaussianBlur stdDeviation on the motion axis ≈ .25 · px/frame (cap 24 px), filter region x −50% width 200%, same ease as the move; or an echo trail collapsing into the lead. End title: 20–30 scaled faded copies of the wordmark on a black radial bg, then one white word with tight 8 px glow + 60 px halo shrinking ≈1 px/frame (1650→500 px wide), ease-in collapse. Focus pull: blur 20→0 + glow fade over 600 ms; radial zoom-blur spin ≈ .3. HyperFrames' shutter motion-blur component (shutterAngle 360–720, 16 samples, +3.38 dB PSNR vs AE) is documented but not installed.

**المعاملات:** blur ≈ .25·px/frame, cap 24 px; glow 8 px + halo 60 px; focus 600 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تمويه حركة · تكبير · تركيز · motion blur · velocity · zoom smear · focus pull · end title · ضبابية الحركة · عنوان النهاية · ظهور الشعار · directional blur · logo reveal

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `style:pm-notdwd-7de38a`
- `style:pm-reflex-cloud-72ffe5`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/references/motion-blur.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/motion-blur-streak.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-33` الانحراف اللوني للعدسة / Lens chromatic aberration (edge-weighted) (proven)
- `GLOW-34` انقسام RGB على الضربة / RGB-split hit jitter (seen)
- `GLOW-36` مؤثرات وسائط HyperFrames وسلسلة VFX / HyperFrames media effects & per-pixel VFX chain (install)
- `GLOW-37` مكتبة مؤثرات ريموشن / Remotion @remotion/effects (glow · lightLeak · starburst · shine) (documented)

### `GLOW-36` — مؤثرات وسائط HyperFrames وسلسلة VFX / HyperFrames media effects & per-pixel VFX chain

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** معالجات غير هدّامة للصور والفيديو (Bloom وBlur وPixelate) وسلسلة نواة WebGL تُعاد رسمها حتميًا عند كل seek. / Non-destructive image/video treatments (Bloom, Blur, Pixelate) and a WebGL2 kernel chain repainted deterministically on every seek.

**متى:** عند تطبيق بلوم أو تمويه أو بكسلة على صورة أو فيديو دون المساس بالأصل في HyperFrames / for non-destructive Bloom, Blur or Pixelate treatments or a WebGL VFX chain on images and video in HyperFrames

**كيف:** `hyperframes media-treatment --selector <css> --apply` writes data attributes (source untouched); VFX chain: data-vfx-chain='{"version":1,"nodes":[{"type":"displacement-map"},{"type":"wave-warp"}]}' with an explicit pixel box on .hf-vfx-in; animate params through CSS custom properties.

**المعاملات:** families Bloom · Blur · Pixelate; nodes displacement-map · wave-warp · noise

**التثبيت:** npm i -D hyperframes@0.8.164 # then: npx hyperframes media-treatment --selector '#clip' --apply

**الوسوم:** هايبرفريمز · بلوم · فيديو · hyperframes · media effects · bloom · vfx chain · webgl · تمويه · بكسلة · تأثيرات فيديو · pixelate · non-destructive

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`
- `kosif-one/vendor/hyperframes/docs/guides/vfx-chain.mdx`

#### 7. قدرات قريبة في العائلة

- `GLOW-34` انقسام RGB على الضربة / RGB-split hit jitter (seen)
- `GLOW-35` تمويه السرعة وتلطيخ التكبير وكشف التركيز / Velocity blur, zoom-smear title & focus-pull glow (seen)
- `GLOW-37` مكتبة مؤثرات ريموشن / Remotion @remotion/effects (glow · lightLeak · starburst · shine) (documented)
- `GLOW-38` تأثيرات ما بعد المعالجة على عناصر HTML / HTML-in-canvas post-FX & TypeGPU liquid glass (documented)

### `GLOW-37` — مكتبة مؤثرات ريموشن / Remotion @remotion/effects (glow · lightLeak · starburst · shine)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | Remotion company license (free for individuals and small teams; companies above the threshold need a paid license — remotion.dev/license). |

**ما هي:** قرابة 55 مؤثر WebGL2/Canvas تُطبَّق كمصفوفة effects على الفيديو أو الصورة، منها glow وlightLeak وstarburst وshine. / About 55 WebGL2/canvas effects applied as an effects array on Video/Solid/CanvasImage, including glow, lightLeak, starburst and shine.

**متى:** عند العمل في Remotion والحاجة لتوهج أو تسريب ضوء أو لمعة أو انفجار نجمي كتأثير جاهز / when working in Remotion and needing ready glow, light-leak, shine or starburst effects on video or images

**كيف:** npx remotion add @remotion/effects; Config.setChromiumOpenGlRenderer('angle'); lightLeak({progress, seed, hueShift}) inside TransitionSeries.Overlay (hueShift 120 green, 240 blue); custom createEffect({type, backend: '2d'\|'webgl2'\|'webgpu', apply, schema}). @remotion/effects is NOT in this container's probe list — run `npm view @remotion/effects version` before promising it.

**المعاملات:** ~55 effects; hueShift 120 / 240

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ريموشن · مؤثرات · remotion · effects · light leak · starburst · shine · glow · تسريب ضوء · لمعة · تأثيرات جاهزة · video effects · webgl

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-atlas/skills/2712-remotion/10436-remotion-markup/effects.md`
- `kosif-atlas/skills/2712-remotion/10436-remotion-markup/light-leaks.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-35` تمويه السرعة وتلطيخ التكبير وكشف التركيز / Velocity blur, zoom-smear title & focus-pull glow (seen)
- `GLOW-36` مؤثرات وسائط HyperFrames وسلسلة VFX / HyperFrames media effects & per-pixel VFX chain (install)
- `GLOW-38` تأثيرات ما بعد المعالجة على عناصر HTML / HTML-in-canvas post-FX & TypeGPU liquid glass (documented)
- `GLOW-39` مظهر الهولوجرام / Hologram look (install)

### `GLOW-38` — تأثيرات ما بعد المعالجة على عناصر HTML / HTML-in-canvas post-FX & TypeGPU liquid glass

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** التقاط عنصر HTML حي كنسيج ومعالجته بـ GLSL أو WGSL: بلوم ثلاثي الأبعاد، زجاج سائل، CRT، تموج، تفتت. / Capture live DOM as a texture and post-process it with GLSL/WGSL: 3D rotation with bloom, liquid glass, CRT, ripples, shatter.

**متى:** حين يريد المستخدم معالجة عنصر HTML حي بتأثيرات مثل الزجاج السائل أو CRT أو التموج أو التفتت / when the user wants live HTML elements post-processed with shaders: liquid glass, CRT, ripples, shatter or bloom

**كيف:** Effect catalogue (10): 3D rotation with bloom, magnetic cursor distortion, shatter, liquid surface, portal reveal, noise dissolve, holographic/iridescent, scan lines + CRT, frosted glass, pixel sort. TypeGPU: video-backed liquid glass, rounded-rect SDF pill, frosted blur via a downsample pass. Needs drawElementImage (html-in-canvas flag) + WebGPU in the render environment — not verified here; prefer the K3 or Canvas routes.

**المعاملات:** 10 named effects

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** زجاج سائل · CRT · html in canvas · liquid glass · typegpu · post fx · webgpu · زجاج مصنفر · تموج · تفتت · shatter · frosted glass · glsl

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/html-in-canvas-patterns.md`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/typegpu.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-36` مؤثرات وسائط HyperFrames وسلسلة VFX / HyperFrames media effects & per-pixel VFX chain (install)
- `GLOW-37` مكتبة مؤثرات ريموشن / Remotion @remotion/effects (glow · lightLeak · starburst · shine) (documented)
- `GLOW-39` مظهر الهولوجرام / Hologram look (install)
- `GLOW-40` التوهج على النص علامة توليد / QA: glow on type is a tell (proven)

### `GLOW-39` — مظهر الهولوجرام / Hologram look

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إضاءة حافة فرينل وخطوط مسح وإضافة ووميض خفيف وبلوم بعتبة منخفضة تصنع هولوجرامًا. / Fresnel rim + scanlines + additive blending + slight flicker + low-threshold bloom make a hologram.

**متى:** حين يطلب المستخدم مظهر هولوجرام خيالي بحافة مضيئة وخطوط مسح ووميض خفيف / when the user wants a sci-fi hologram look with a Fresnel rim, scanlines and a slight flicker

**كيف:** three.js: emissive += rimColor·pow(1 − \|dot(eye, normal)\|, 2–4); fragment scanline term sin(y·k + t) with ≈300–800 lines over the screen height; AdditiveBlending, depthWrite false; a slight opacity flicker (a few %, never a strobe); bloom threshold low. Or the WebGPU 'Hologram' plate (pale blue orb with scan rings, GLOW-52).

**المعاملات:** fresnel power 2–4; 300–800 scanlines/screen

**التثبيت:** npm i three@0.186.1 # or: npx hyperframes@0.8.164 add hologram (WebGPU)

**الوسوم:** هولوجرام · خيال علمي · hologram · fresnel · scanlines · sci-fi · additive · هولوغرام · صورة مجسمة · خطوط مسح · holographic · rim glow

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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
- `kosif-one/vendor/hyperframes/registry/blocks/hologram/hologram.html`

#### 7. قدرات قريبة في العائلة

- `GLOW-37` مكتبة مؤثرات ريموشن / Remotion @remotion/effects (glow · lightLeak · starburst · shine) (documented)
- `GLOW-38` تأثيرات ما بعد المعالجة على عناصر HTML / HTML-in-canvas post-FX & TypeGPU liquid glass (documented)
- `GLOW-40` التوهج على النص علامة توليد / QA: glow on type is a tell (proven)
- `GLOW-41` مسحة ضوء على جملة الذروة / Payoff light sweep through letterforms (proven)

### `GLOW-40` — التوهج على النص علامة توليد / QA: glow on type is a tell

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فحص الجودة يحذّر من ظل نص كبير أو ملون لأنه علامة سريعة على عمل مولَّد؛ الظل الداكن الناعم أفضل. / The QA linter flags large or coloured text-shadow as a quick tell of generated work; prefer dark soft shadows.

**متى:** عند مراجعة الجودة لاكتشاف توهج كبير أو ملون على النص يفضح أن العمل مولَّد / when reviewing quality to catch large or coloured text glow that makes work look generated

**كيف:** qa.py lint warns when text-shadow blur ≥ 20 px or the shadow colour is not black. Glow belongs on one hero word or a neon sign (GLOW-01/04), never on captions or body text — the owner playbooks list 'glow and chromatic aberration on body text' as a do-not.

**المعاملات:** warn: text-shadow blur ≥ 20 px or non-black

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** جودة · فحص · ظل النص · qa · lint · text-shadow · ai tell · مراجعة · أخطاء التصميم · توهج النص · design review · text glow

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/motion/qa.py:68`
- `kosif-tool/playbooks/kinetic-type.md:104`

#### 7. قدرات قريبة في العائلة

- `GLOW-38` تأثيرات ما بعد المعالجة على عناصر HTML / HTML-in-canvas post-FX & TypeGPU liquid glass (documented)
- `GLOW-39` مظهر الهولوجرام / Hologram look (install)
- `GLOW-41` مسحة ضوء على جملة الذروة / Payoff light sweep through letterforms (proven)
- `GLOW-42` لمعة البطاقة والزر وانعكاس الزجاج / UI sheen family: card scan, button glint, one-pass glass band (ready)

### `GLOW-41` — مسحة ضوء على جملة الذروة / Payoff light sweep through letterforms

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شريط ساطع يعبر الكلمة عبر تدرج مقصوص على النص، فيعطي لمعة معدنية على كلمة الختام. / A bright band travels through the word via a gradient clipped to the text — a metallic glint on the payoff word.

**متى:** حين تحتاج كلمة الختام لمعة ضوء معدنية تعبر حروفها، مع اتجاه صحيح للعربية / for a metallic light glint sweeping through the payoff word's letters, with right-to-left support for Arabic

**كيف:** background-clip:text with an oversized gradient (background-size 300% 100%) and tween background-position. Set the gradient with background-image (the 'background' shorthand placed after background-clip resets the clip and paints a solid block). LTR sweep 100%→0% travels left→right; for Arabic run 0%→100% so the light moves with the reading (the vendored shimmer utility auto-reverses for RTL). Payoff mode: dim everything else to .3, the line slams from scale 1.08 + blur 16. Variants: HyperFrames text-shimmer (sweep_at 1.2 s), shimmer-sweep, chrome-sweep / spotlight-sweep primitives on downbeats (0.6–2 s). Verified here: Arabic «القمّة» swept in the render_html test. (code snippet in references/powers/light-glow-bloom.md)

**المعاملات:** gradient 100°: ivory 0–40%, #fff7e2 47%, #fff 50%, #fff7e2 53%, ivory 60–100%; 0.75 s power2.inOut (verse 1.0 s); drop-shadow 0 4px 18px rgba(0,0,0,.5); shimmer util 2 s linear, spread calc(3ch + 40px)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** لمعة · جملة الختام · تدرج · light sweep · shimmer · background-clip · payoff · metallic · rtl · لمعة معدنية · كلمة الختام · نص لامع · text shine · glint

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:35`
- `100-superskills/skills/kosif-montage-motion/templates/directed.html:120`
- `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/gradient-text-sweep.md`
- `kosif-audit-pro/vendor/shadcn-tailwind-4.13.0.css:536`

#### 7. قدرات قريبة في العائلة

- `GLOW-39` مظهر الهولوجرام / Hologram look (install)
- `GLOW-40` التوهج على النص علامة توليد / QA: glow on type is a tell (proven)
- `GLOW-42` لمعة البطاقة والزر وانعكاس الزجاج / UI sheen family: card scan, button glint, one-pass glass band (ready)
- `GLOW-43` مرور الضوء المفتاحي على المنتج / Travelling key-light pass (product hero, light-thread reveal) (install)

### `GLOW-42` — لمعة البطاقة والزر وانعكاس الزجاج / UI sheen family: card scan, button glint, one-pass glass band

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شريط ضوء قطري يعبر البطاقة مرة، ولمعة بيضاء على الزر، وشريط انعكاس يعبر زجاج الهاتف مرة لكل دوران — ولا شيء يتكرر. / A diagonal band crosses the card once, a white glint crosses the button, a reflection band crosses phone glass once per rotation — nothing loops.

**متى:** عند إضافة لمعة تعبر بطاقة أو زرًا أو زجاج هاتف مرة واحدة دون تكرار في الواجهة / for a one-time sheen crossing a card, button or phone glass in a UI, never looping

**كيف:** Card: ::before inset −65% −18%, linear-gradient(112deg, transparent 42%, primary 10% at 50%, transparent 58%), translate 42%→−42% with rotate 6deg. Button: ::after 24% wide, rotate(14deg), transparent → rgba(255,255,255,.55) → transparent, translateX 0→520% (fine pointers only). Glass: linear-gradient(115deg, transparent 40%, rgba(255,255,255,.14) 50%, transparent 60%) once per rotation; emerging-from-dark variant 1800 ms at 25%. HyperFrames gloss-sweep: card lands with a restrained slam and catches one specular sweep (angle 25°, −60..60).

**المعاملات:** card 950 ms ease-cinematic, delay 260 ms, peak 35%; button 720 ms, opacity 0→.9 at 24%→0; glass 1.2 s cubic-bezier(.33,1,.68,1) peak .12–.16

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** لمعة · زر · بطاقة · زجاج · sheen · glint · card · button · glass reflection · once · لمعان · واجهة مستخدم · شاشة الهاتف · ui shine · shine sweep

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-audit-pro/app/globals.css:1142`
- `kosif-audit-pro/app/globals.css:412`
- `kosif-tool/playbooks/phone.md:42`
- `kosif-one/vendor/hyperframes/registry/components/gloss-sweep/gloss-sweep.html`

#### 7. قدرات قريبة في العائلة

- `GLOW-40` التوهج على النص علامة توليد / QA: glow on type is a tell (proven)
- `GLOW-41` مسحة ضوء على جملة الذروة / Payoff light sweep through letterforms (proven)
- `GLOW-43` مرور الضوء المفتاحي على المنتج / Travelling key-light pass (product hero, light-thread reveal) (install)
- `GLOW-44` لمعة تدور مع الجسم / Rotation-locked specular sheen (fake 3D, chrome) (seen)

### `GLOW-43` — مرور الضوء المفتاحي على المنتج / Travelling key-light pass (product hero, light-thread reveal)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | HyperFrames (Apache-2.0) components animate with GSAP 3.14 — GSAP standard 'no charge' license (gsap.com/standard-license), not OSI. |

**ما هي:** ضوء مفتاحي يعبر المشهد مرة فيتغير كل بريق وظل معه، أو خيط ضوء يكشف حواف منتج داكن قبل إضاءته كاملًا. / A key light crosses the scene once and every highlight and shadow shifts with it, or a thin light thread traces a dark product's outline before it is fully lit.

**متى:** حين يُعرض منتج فاخر في إعلان ويحتاج ضوءًا يعبره مرة أو خيط ضوء يكشف حوافه الداكنة / for a premium product ad where a key light sweeps across once, or a thin light thread reveals a dark product's edges

**كيف:** HyperFrames light-sweep-pass: one --light-x custom property drives the soft diagonal band and all slotted highlights/shadows in lockstep. Ads playbook: push 3–5% per beat or a 15–30° turn + a light sweep of 800 ms, product ≥ 40% of frame height. MG-037 (dark product): 0–1 s partial dark, 1–3 s sweep, 3–5 s full reveal via a moving light mask over differently exposed copies — fake light cannot recover missing detail. S02 Quiet premium: slow scale 1.00→1.04, few transitions.

**المعاملات:** angle 115° (60–160); sweep_at .9 s; strength subtle\|standard; sweep 800 ms

**التثبيت:** npx hyperframes@0.8.164 add light-sweep-pass

**الوسوم:** منتج · ضوء مفتاحي · إعلان · product · key light · light sweep · reveal · premium · ads · إعلان منتج · كشف المنتج · تصوير منتجات · product reveal · commercial

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-one/vendor/hyperframes/registry/components/light-sweep-pass/light-sweep-pass.html`
- `kosif-tool/playbooks/ads.md:18`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-product-ads.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-41` مسحة ضوء على جملة الذروة / Payoff light sweep through letterforms (proven)
- `GLOW-42` لمعة البطاقة والزر وانعكاس الزجاج / UI sheen family: card scan, button glint, one-pass glass band (ready)
- `GLOW-44` لمعة تدور مع الجسم / Rotation-locked specular sheen (fake 3D, chrome) (seen)
- `GLOW-45` خط مسح ليزري وشريط إضاءة يمسح الكود / Laser scan line & scanning highlight bar (ready)

### `GLOW-44` — لمعة تدور مع الجسم / Rotation-locked specular sheen (fake 3D, chrome)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** وجه الجسم يُضاء حسب زاوية دورانه، ولمعة متدرجة تنزلق عليه بقدر الدوران. / The object's face brightens by its rotation angle and a gradient highlight slides across it in proportion.

**متى:** حين يدور جسم مسطح وتريد لمعة معدنية تتحرك مع زاوية الدوران لتوحي بالعمق / when a rotating flat object needs a chrome highlight that slides with the rotation angle to fake 3D

**كيف:** Build recipe: fixed light from top-left; face brightness = max(0, dot(normal, lightDir)); move a linear-gradient highlight stop across the face ∝ rotation angle; extruded edge one shade darker. Music cue: HyperFrames chrome-sweep primitive on downbeat/reveal (0.6–1.4 s).

**المعاملات:** light fixed top-left; sweep ∝ angle

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** معدن · ثلاثي أبعاد مزيف · لمعة · fake 3d · specular · chrome · sheen · rotation · كروم · دوران · لمعان معدني · metal shine · pseudo 3d

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `style:fake3d`
- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/chrome-sweep/scene.html`

#### 7. قدرات قريبة في العائلة

- `GLOW-42` لمعة البطاقة والزر وانعكاس الزجاج / UI sheen family: card scan, button glint, one-pass glass band (ready)
- `GLOW-43` مرور الضوء المفتاحي على المنتج / Travelling key-light pass (product hero, light-thread reveal) (install)
- `GLOW-45` خط مسح ليزري وشريط إضاءة يمسح الكود / Laser scan line & scanning highlight bar (ready)
- `GLOW-46` بريق نجمي وشرر القلم / Twinkle sparkles & pen sparks (seen)

### `GLOW-45` — خط مسح ليزري وشريط إضاءة يمسح الكود / Laser scan line & scanning highlight bar

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خط أحمر متوهج يصعد وينزل داخل إطار مسح، أو شريط ضوء يمسح الكود فتبيض الأسطر التي يعبرها. / A glowing red line sweeps up and down inside a scan frame, or a light bar travels down code and the lines it passes turn white.

**متى:** حين يطلب المستخدم خط مسح ليزري يصعد وينزل في إطار، أو شريط ضوء يمر على الكود ويبرز أسطره / when the user wants a laser scan line sweeping inside a frame, or a light bar highlighting code lines as it passes

**كيف:** Laser: height 2 px, background var(--sk-bad), box-shadow 0 0 8px; @keyframes top 10%→90%→10% 2 s ease-in-out infinite; frame 2 px dashed rgba(255,255,255,.85) + box-shadow 0 0 0 4000px rgba(0,0,0,.45) to darken the surround. Code bar: 2 px core + 40 px soft gradient above, ≈1 line per 80 ms, yellow #f2c230 at α .6, passed lines grey→white.

**المعاملات:** 2 s cycle; glow 8 px; surround .45; code bar 1 line / 80 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ليزر · مسح · كود · laser · scan line · scanner · code highlight · ماسح ضوئي · خط أحمر · تمييز الكود · scanning · scan frame

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-earth-ci-fork/ui/features/enterprise.css:348`
- `style:pm-kyonax-on-tech-aabc1d`
- `style:pm-tstfully-0aa6b4`

#### 7. قدرات قريبة في العائلة

- `GLOW-43` مرور الضوء المفتاحي على المنتج / Travelling key-light pass (product hero, light-thread reveal) (install)
- `GLOW-44` لمعة تدور مع الجسم / Rotation-locked specular sheen (fake 3D, chrome) (seen)
- `GLOW-46` بريق نجمي وشرر القلم / Twinkle sparkles & pen sparks (seen)
- `GLOW-47` أشعة إلهية وبلوم فوق اللقطة بـ CSS / CSS god rays & bloom layer over footage (proven)

### `GLOW-46` — بريق نجمي وشرر القلم / Twinkle sparkles & pen sparks

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نجوم رباعية تكبر وتدور وتختفي حول العنوان، وشرر صغير حتمي حول رأس القلم. / 4-point stars scale up, spin and vanish around a headline; small deterministic sparks around a pen head.

**متى:** حين يحتاج عنوان أو خبر سار نجومًا لامعة تومض حوله، أو شررًا صغيرًا حول رأس القلم / when a headline or good-news moment needs twinkling star sparkles, or small sparks around a pen head

**كيف:** Build recipe: star path scale 0→1→0 with rotation over 600 ms at seeded positions, 6–10 alive at once; pen head: radial glow r .07·m α .42 + 8 deterministic 2 px sparks within .01–.045·m redrawn each frame from a per-frame seed (Basma). Sparkle means good news only (attention menu).

**المعاملات:** life 600 ms; 6–10 concurrent; 8 sparks 2 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بريق · نجوم · شرر · sparkle · twinkle · stars · pen spark · لمعان · نجوم لامعة · خبر سار · glitter · shine

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `style:pm-deebeeeff-50fcd0`
- `app/public/js/10_studio.js:267`

#### 7. قدرات قريبة في العائلة

- `GLOW-44` لمعة تدور مع الجسم / Rotation-locked specular sheen (fake 3D, chrome) (seen)
- `GLOW-45` خط مسح ليزري وشريط إضاءة يمسح الكود / Laser scan line & scanning highlight bar (ready)
- `GLOW-47` أشعة إلهية وبلوم فوق اللقطة بـ CSS / CSS god rays & bloom layer over footage (proven)
- `GLOW-48` أشعة الشمس في المشهد ثلاثي الأبعاد / Screen-space god rays (3D sun) (ready)

### `GLOW-47` — أشعة إلهية وبلوم فوق اللقطة بـ CSS / CSS god rays & bloom layer over footage

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أشعة مخروطية متكررة مقنّعة لتتلاشى للأسفل، وبلوم شعاعي دافئ بوضع screen قرب البطل، فوق لقطة حقيقية أو رسم. / Repeating conic rays masked to fade downward and a warm radial bloom in screen mode near the subject, over real footage or drawings.

**متى:** عند إضافة أشعة ضوء ووهج دافئ فوق لقطة فيديو حقيقية أو رسم باستخدام طبقات CSS / for adding god rays and a warm bloom over real footage or drawings using CSS layers

**كيف:** #rays repeating-conic-gradient(from 168deg at 590px −260px, 0° → α .13 at 2.2° → 0 at 5° → 0 at 9°), mix-blend screen, mask linear 0 → .6 → transparent at 75%; #bloom radial ellipse 380×520 at 60px 300px rgba(255,214,150,.5) → .16 → 0, screen; bottom scrim 52%→100% to .74 for captions; deliberate dip to black .32 s power2.in. 2D variant: warm trapezoids #ffc76a at 20–35% with linear fade + 30–60 twinkling motes. Verified here (render_html test: rays + pool + vignette).

**المعاملات:** rays 2.2°/5°/9° α .13; bloom .5→.16→0; cues bloom .85 at 3.6 s, 1.0 at 11.55 s, rays .45→1 at 16 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أشعة · ضوء إلهي · فوق الفيديو · god rays · conic gradient · footage · bloom · screen blend · أشعة ضوء · وهج دافئ · لقطة حقيقية · light rays · css overlay

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:20`
- `kosif-studio/motion/projects/premium_edit/index.html:20`
- `style:fake3d`

#### 7. قدرات قريبة في العائلة

- `GLOW-45` خط مسح ليزري وشريط إضاءة يمسح الكود / Laser scan line & scanning highlight bar (ready)
- `GLOW-46` بريق نجمي وشرر القلم / Twinkle sparkles & pen sparks (seen)
- `GLOW-48` أشعة الشمس في المشهد ثلاثي الأبعاد / Screen-space god rays (3D sun) (ready)
- `GLOW-49` انفجار أشعة شمسي دوّار / Rotating sunburst / ray-burst backdrop (seen)

### `GLOW-48` — أشعة الشمس في المشهد ثلاثي الأبعاد / Screen-space god rays (3D sun)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ضبابية شعاعية بـ 64 عينة من موضع الشمس على الشاشة، مقصورة على البكسلات الساطعة ومنطقة السماء. / A 64-tap radial blur from the on-screen sun, limited to bright pixels and the sky region.

**متى:** حين يظهر قرص الشمس في مشهد ثلاثي الأبعاد وتريد أشعة ضوء تنبثق منه / when the sun is on screen in a 3D scene and you want light rays streaming from it

**كيف:** Inside makePost: post.rays.uniforms.uAmount.value = k only while post.sunOnScreen(sun) is true; dithered and masked above the sun height to avoid water-glitter lattices. Time it: amount = inFront ? .9·(1 − smooth(2.5, 5, t)) + .3 + .35·overcast : 0; music: .35 + .45·kick toward an eclipse.

**المعاملات:** 64 samples; stride .55 of sun distance; decay .972/sample; luma threshold .7; output ×.55

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أشعة الشمس · ثلاثي الأبعاد · god rays · sun · three.js · volumetric · screen space · أشعة حجمية · شعاع الشمس · ضوء سماوي · light shafts · sun rays

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/motion/kit/three-kit.js:378`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:372`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:99`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:129`

#### 7. قدرات قريبة في العائلة

- `GLOW-46` بريق نجمي وشرر القلم / Twinkle sparkles & pen sparks (seen)
- `GLOW-47` أشعة إلهية وبلوم فوق اللقطة بـ CSS / CSS god rays & bloom layer over footage (proven)
- `GLOW-49` انفجار أشعة شمسي دوّار / Rotating sunburst / ray-burst backdrop (seen)
- `GLOW-50` وهج العدسة ثلاثي الأبعاد / 3D lens flare that follows the sun (ready)

### `GLOW-49` — انفجار أشعة شمسي دوّار / Rotating sunburst / ray-burst backdrop

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أشعة رفيعة من مركز تدور ببطء خلف شعار أو بطل أو كلمة «ترقية»، بشعاع مركزي أبيض وحافة قوس قزح أحيانًا. / Thin rays from a centre rotate slowly behind a logo, hero or LEVEL UP stamp, sometimes with a white central beam and rainbow fringe.

**متى:** حين يحتاج شعار أو بطل أو لحظة ترقية خلفية أشعة تدور ببطء توحي بالاحتفال / for a slowly rotating ray-burst backdrop behind a logo, hero or level-up stamp to sell a celebration

**كيف:** Build recipe: repeating-conic-gradient wedges (24–48 thin rays, or 12–16 alternating purple/magenta for level-ups), radial mask, screen blend, rotate 2–20°/s; golden backdrop = radial + conic rays + rings at .4; trailer: radial streaks behind a bevelled gold serif (#f1d38a→#8a5a1a), frame within frame. WebGPU 'SunBurst' plate as an alternative (GLOW-52). (code snippet in references/powers/light-glow-bloom.md)

**المعاملات:** 24–48 rays (12–16 for level-up); rotate 20°/s; opacity .4

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أشعة · احتفال · ترقية · sunburst · rays · celebration · level up · conic · أشعة دوارة · خلفية شعار · خلفية احتفالية · ray burst · rotating rays

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `style:pm-gizakdag-b8c59e`
- `style:pm-ibrahimwasim240-809370`
- `style:pm-kentcdodds-6fa8cf`
- `style:pm-emollick-8661a8`

#### 7. قدرات قريبة في العائلة

- `GLOW-47` أشعة إلهية وبلوم فوق اللقطة بـ CSS / CSS god rays & bloom layer over footage (proven)
- `GLOW-48` أشعة الشمس في المشهد ثلاثي الأبعاد / Screen-space god rays (3D sun) (ready)
- `GLOW-50` وهج العدسة ثلاثي الأبعاد / 3D lens flare that follows the sun (ready)
- `GLOW-51` فلير أنامورفي بأشباح / Anamorphic flare with ghosts (painter + streak field) (proven)

### `GLOW-50` — وهج العدسة ثلاثي الأبعاد / 3D lens flare that follows the sun

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فلير من خمسة عناصر مولّدة (أقراص وحلقات) مثبت باتجاه الشمس ويختفي حين تُحجب. / A five-element flare from generated soft and ring sprites, placed along the sun direction and hidden when the sun is occluded.

**متى:** حين تظهر الشمس في مشهد three.js وتريد وهج عدسة يتبعها ويختفي عند حجبها / when the sun appears in a three.js scene and needs a lens flare that follows it and hides when occluded

**كيف:** const f = K3.makeLensflare({color}); place at sunDir × 9000 + camera.position; f.visible = post.sunOnScreen(sun) (e.g. && t < 7.5); fade it with overcast and lightning.

**المعاملات:** soft 420 px @0 #ffe2b0; ring 90 @.35 #ffd0a0; soft 60 @.55 #aad4ff; ring 140 @.75 #ffc8a0; soft 40 @.95 #ffffff

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** وهج العدسة · فلير · شمس · lens flare · sun · three.js · sprites · لمعة العدسة · فلير شمس · ثلاثي الأبعاد · flare · sun glare

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/motion/kit/three-kit.js:312`
- `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:312`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:99`

#### 7. قدرات قريبة في العائلة

- `GLOW-48` أشعة الشمس في المشهد ثلاثي الأبعاد / Screen-space god rays (3D sun) (ready)
- `GLOW-49` انفجار أشعة شمسي دوّار / Rotating sunburst / ray-burst backdrop (seen)
- `GLOW-51` فلير أنامورفي بأشباح / Anamorphic flare with ghosts (painter + streak field) (proven)
- `GLOW-52` ألواح ضوء WebGPU جاهزة / WebGPU shader light plates (Godrays · LensFlare · LightEdge · Prism …) (install)

### `GLOW-51` — فلير أنامورفي بأشباح / Anamorphic flare with ghosts (painter + streak field)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قلب ناعم وخط أفقي طويل بداخله خط أبيض، وأقراص أشباح باهتة معكوسة عبر مركز الإطار. / A soft core glow, a long horizontal streak with a white inner streak, and faint ghost discs mirrored through the frame centre.

**متى:** حين يطلب المستخدم وهجًا أنامورفيًا سينمائيًا بخط أفقي طويل وأقراص أشباح حول مصدر ضوء / when the user wants a cinematic anamorphic flare: soft core, long horizontal streak and ghost discs

**كيف:** Painter: flare(centre, colour, size, streak, strength, ghosts=3) = glow(core) + additive streak ellipse (streak × .09·size) + white inner streak (.55·streak × .04·size) + ghosts at t = 1 + .55k mirrored through the centre — ran here 2026-10-16. Screen-space version: 3–5 ghost rings along the sun→centre axis + bloom on highlights > .9. Many-point field: HyperFrames vfx-anamorphic-flare (140 drifting emitters, high-pass .3, 80 horizontal taps at ¼ res, tint #7a8aff).

**المعاملات:** default #ffb070, size 120, streak 420, strength .6 (whale 100/360/.38); field intensity 5, streakLength 1 (0.1–6), timeScale .5, backdrop #04040a

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أنامورفي · فلير · خط أفقي · anamorphic · flare · streak · ghosts · lens · وهج سينمائي · خط ضوء أفقي · أشباح العدسة · cinematic flare · horizontal streak

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/render.py:741`
- `kosif-studio/scenes/whale_dragon.py:287`
- `kosif-one/vendor/hyperframes/registry/blocks/vfx-anamorphic-flare/vfx-anamorphic-flare.html`
- `style:pm-axtonliu-0b861d`

#### 7. قدرات قريبة في العائلة

- `GLOW-49` انفجار أشعة شمسي دوّار / Rotating sunburst / ray-burst backdrop (seen)
- `GLOW-50` وهج العدسة ثلاثي الأبعاد / 3D lens flare that follows the sun (ready)
- `GLOW-52` ألواح ضوء WebGPU جاهزة / WebGPU shader light plates (Godrays · LensFlare · LightEdge · Prism …) (install)
- `GLOW-53` تسريب ضوء وحرق فيلم / Light leak, overexposure & film-burn transition (install)

### `GLOW-52` — ألواح ضوء WebGPU جاهزة / WebGPU shader light plates (Godrays · LensFlare · LightEdge · Prism …)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Shader library MIT (Shader Effects Inc., shaders 4.0.0) + HyperFrames Apache-2.0 — ship lib/shaders.THIRD-PARTY-LICENSES.txt with the film. |

**ما هي:** لوحات خلفية بمظللات WebGPU لمدة ثانيتين: أشعة إلهية، فلير، حافة مضيئة، منشور، خيوط ضوء، شفق وغيرها. / 2-second WebGPU shader backgrounds: god rays, lens flare, light edge, prism, light strands, aurora and more.

**متى:** عند الحاجة لخلفية مظلل جاهزة مدتها ثانيتان: أشعة إلهية أو فلير أو منشور أو شفق عبر WebGPU / for ready 2-second WebGPU shader backgrounds such as god rays, lens flare, light edge, prism or aurora

**كيف:** `npx hyperframes@0.8.164 add <id>` or put lib/shaders.iife.js beside the HTML and declare <canvas data-shader='Godrays' width=1920 height=1080> in a root marked data-requires-webgpu data-no-timeline. A WebGPU adapter exists here only with --enable-unsafe-webgpu --enable-features=Vulkan --use-angle=swiftshader --enable-unsafe-swiftshader (checked 2026-10-16); no plate has been rendered yet — preview one frame first. The library has 36 looks; the light ones are in the table below. (full table in references/powers/light-glow-bloom.md)

**المعاملات:** 1920×1080; 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)

**التثبيت:** npx hyperframes@0.8.164 add godrays

**الوسوم:** WebGPU · مظلل · خلفية · webgpu · shader · godrays · lens flare · prism · aurora · plates · خلفية ضوئية · أشعة إلهية · منشور · light background · hyperframes

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-one/vendor/hyperframes/registry/blocks/godrays/godrays.html`
- `kosif-one/vendor/hyperframes/registry/blocks/lens-flare/lens-flare.html`
- `kosif-one/vendor/hyperframes/registry/blocks/aurora/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### 7. قدرات قريبة في العائلة

- `GLOW-50` وهج العدسة ثلاثي الأبعاد / 3D lens flare that follows the sun (ready)
- `GLOW-51` فلير أنامورفي بأشباح / Anamorphic flare with ghosts (painter + streak field) (proven)
- `GLOW-53` تسريب ضوء وحرق فيلم / Light leak, overexposure & film-burn transition (install)
- `GLOW-54` ومضة الإطار وانفجار الضوء / Flash frame, double strike & light-burst transition (proven)

### `GLOW-53` — تسريب ضوء وحرق فيلم / Light leak, overexposure & film-burn transition

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames (Apache-2.0) components animate with GSAP 3.14 — GSAP standard 'no charge' license (gsap.com/standard-license), not OSI. |

**ما هي:** ضوء دافئ يغسل القطع، أو تحترق اللقطة إلى الأبيض، أو بقع حرق تعبر الإطار. / Warm light washes over the cut, the outgoing shot blows out to white, or burn blobs sweep across.

**متى:** حين يريد المستخدم انتقالًا دافئًا بتسريب ضوء أو احتراق اللقطة للأبيض أو حرق فيلم، كما في مشاهد الذكريات / when the user wants a warm light-leak, white blow-out or film-burn transition, e.g. for memory scenes

**كيف:** CSS: oversized (≥2400 px) blurred warm blobs moving x 300–600 px at opacity .4–.9 over ≈.5 s; overexposure: filter brightness(1.5)→(3) + scale 1.03→1.06, then a white overlay 0→1→0 over ≈.9 s. Drifting canvas leak (Basma): radial at x = W·(.5 + .65 sin .31t), y = H·(.12 + .1 cos .23t), r = .75·max(W,H), rgba(255,170,90,leak) → rgba(255,80,60,.35·leak) at 45% → 0, globalCompositeOperation 'screen'. Rainbow wash: full-frame blurred gradient pass 600 ms. Ready-made: HyperFrames organic-light-leak-overlay (4 s), the 'light-leak' WebGL transition.

**المعاملات:** leak 0–.6 (AutoEdit up to .9); blobs ≥2400 px; brightness 1.5→3; burn ≈.9 s

**التثبيت:** npx hyperframes@0.8.164 add organic-light-leak-overlay # or: cd /home/user/app && npm install (Basma)

**الوسوم:** تسريب ضوء · حرق فيلم · انتقال · light leak · film burn · overexposure · transition · memory · ترانزيشن · ذكريات · فلاش أبيض · burn transition · white out

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions/css-light.md`
- `app/public/js/00_editor.js:287`
- `kosif-one/vendor/hyperframes/registry/blocks/organic-light-leak-overlay/organic-light-leak-overlay.html`
- `style:pm-gizakdag-cf4ae6`

#### 7. قدرات قريبة في العائلة

- `GLOW-51` فلير أنامورفي بأشباح / Anamorphic flare with ghosts (painter + streak field) (proven)
- `GLOW-52` ألواح ضوء WebGPU جاهزة / WebGPU shader light plates (Godrays · LensFlare · LightEdge · Prism …) (install)
- `GLOW-54` ومضة الإطار وانفجار الضوء / Flash frame, double strike & light-burst transition (proven)
- `GLOW-55` أشعة يلقيها النص ونص بشعاع المؤشر / Volumetric rays cast by a wordmark / cursor-light text (install)

### `GLOW-54` — ومضة الإطار وانفجار الضوء / Flash frame, double strike & light-burst transition

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ومضة بيضاء أو بلون التمييز مع ضربة ثانية اختيارية، أو كرة ضوء بحلقة وخط أنامورفي تكبر ثم يقطع المشهد. / A white/accent flash with an optional second strike, or a light orb with a ring and anamorphic streak that scales up before the cut.

**متى:** حين يحتاج القطع أو لحظة الذروة ومضة بيضاء أو ضربة مزدوجة أو كرة ضوء تكبر قبل الانتقال / when a cut or emotional peak needs a white or accent flash, a double strike, or a growing light orb before the cut

**كيف:** MOTION.flash(tl, el, at, {peak, dur, again}) on a full-frame div. Warm accent version: radial-gradient(circle at 50% 55%, #fff1c8, #ffbf6b 45%, transparent 80%) with mix-blend screen on the three emotional peaks only. Light-burst transition: white-core/blue-halo orb + thin ring + full-width anamorphic streak (4–6 px, 20 px blur) + short radial sparks, scale .3→1.2 over ≈300 ms additive, then cut. Hit flash 80 ms linear + 8 ghosts over 120 ms. Respect ≤3 flashes/s. Verified here (render_html test: .06 s attack, cubic decay .35 s).

**المعاملات:** attack .06 s to .85; decay .35 s power4.out; again 50% at +.16 s; dua peaks 10.99 s .55/.9 · 18.75 s .35/.6 · 22.95 s .6/1.1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ومضة · وميض · انتقال · flash · strobe · impact · light burst · transition · فلاش · ومضة بيضاء · ذروة · white flash · flash cut

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:325`
- `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:325`
- `kosif-one/projects/thursday-dua-animation/source/index.html:212-217`
- `style:pm-marouanegazouzi-6071d5`

#### 7. قدرات قريبة في العائلة

- `GLOW-52` ألواح ضوء WebGPU جاهزة / WebGPU shader light plates (Godrays · LensFlare · LightEdge · Prism …) (install)
- `GLOW-53` تسريب ضوء وحرق فيلم / Light leak, overexposure & film-burn transition (install)
- `GLOW-55` أشعة يلقيها النص ونص بشعاع المؤشر / Volumetric rays cast by a wordmark / cursor-light text (install)
- `GLOW-56` الشمس والهالة والكسوف / Blooming sun, corona & eclipse (2D and 3D) (install)

### `GLOW-55` — أشعة يلقيها النص ونص بشعاع المؤشر / Volumetric rays cast by a wordmark / cursor-light text

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames (Apache-2.0) components animate with GSAP 3.14 — GSAP standard 'no charge' license (gsap.com/standard-license), not OSI. |

**ما هي:** كلمة تُلقي أشعة ضوء حجمية نحو مؤشر ضوء يتحرك، أو نص يُكشف بتوهج المؤشر وظلال لونية. / A wordmark casts volumetric light rays toward a sweeping light cursor, or text is revealed by a cursor glow with chromatic shadow rays.

**متى:** حين يريد المستخدم كلمة أو شعارًا نصيًا يلقي أشعة ضوء نحو مؤشر متحرك، أو نصًا يُكشف بضوء المؤشر / when a wordmark should cast volumetric rays toward a moving light cursor, or text is revealed by a cursor glow

**كيف:** HyperFrames text-spectral-rays primitive (the shader owns the wordmark; anchor to phrase/sweep events, best span 2.5–5 s) or the vfx-text-cursor block (WebGL + Canvas 2D + SVG, 8 s). Arabic: render the shaped whole word to a texture first; the block's default font (Big Shoulders Display) is Latin-only.

**المعاملات:** spectral rays 2.5–5 s; text-cursor 8 s 1920×1080

**التثبيت:** npx hyperframes@0.8.164 add vfx-text-cursor

**الوسوم:** أشعة · نص · مؤشر · volumetric rays · wordmark · cursor light · reveal · كشف النص · ضوء متحرك · شعار نصي · text reveal · light rays

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/text-spectral-rays/scene.html`
- `kosif-one/vendor/hyperframes/registry/blocks/vfx-text-cursor/vfx-text-cursor.html`

#### 7. قدرات قريبة في العائلة

- `GLOW-53` تسريب ضوء وحرق فيلم / Light leak, overexposure & film-burn transition (install)
- `GLOW-54` ومضة الإطار وانفجار الضوء / Flash frame, double strike & light-burst transition (proven)
- `GLOW-56` الشمس والهالة والكسوف / Blooming sun, corona & eclipse (2D and 3D) (install)
- `GLOW-57` إضاءة ثلاثية بالوقفات والكلفن / Three-point rig in stops & Kelvin (K3.lightRig) (proven)

### `GLOW-56` — الشمس والهالة والكسوف / Blooming sun, corona & eclipse (2D and 3D)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شمس بثلاث طبقات توهج وأشعة دوارة، وشروق خلف الأفق، وقرص قمر أسود بهالة برتقالية تتسع مع الباص. / A sun with three stacked glows and slowly turning rays, a sunrise behind the horizon, and a black moon disc whose orange corona widens with the bass.

**متى:** حين يحتاج المشهد شمسًا متوهجة أو شروقًا خلف الأفق أو كسوفًا تتسع هالته مع الباص / when a scene needs a glowing sun, a sunrise behind the horizon or an eclipse whose corona widens with the bass

**كيف:** 2D: noise-textured disc core #fcfaca → mid #f7b54a → outer #c0461c, additive outer glow as 3 stacked blurs 40/120/300 px, ray sprites rotating ≈2°/s, intensity ramps per section; finale: brand-colour radial (radius 60% of frame) rising behind the horizon over 2 s easeOut. 3D shader: disc = 1 − smoothstep(.072, .075, r); corona = exp(−max(0, r − .074)·(46 − 12·uBass))·(.55 + 1.1·uBass), colour (1, .42, .16), uBass = clamp(bass·1.1 + kick·.35). Black sun: dark disc + thin emissive annulus (≈2% of radius, strength 20–40, #f2d7a8), bloom threshold .8, jagged edge noise.

**المعاملات:** blurs 40/120/300 px; rays 2°/s; corona falloff 46 − 12·bass

**التثبيت:** npm i three@0.186.1 esbuild # rebuild sound_ground as-is; or port the shader to window.K3

**الوسوم:** شمس · كسوف · شروق · هالة · sun · eclipse · corona · sunrise · bass reactive · قرص الشمس · أفق · تفاعل مع الباص · sun glow · solar eclipse

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:esbuild` ← npm ls esbuild أو وجود node_modules/esbuild
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:23`
- `style:pm-samaote-5e2fc2`
- `style:pm-aschapmann-131210`
- `style:pm-theparuchh-6e08c3`

#### 7. قدرات قريبة في العائلة

- `GLOW-54` ومضة الإطار وانفجار الضوء / Flash frame, double strike & light-burst transition (proven)
- `GLOW-55` أشعة يلقيها النص ونص بشعاع المؤشر / Volumetric rays cast by a wordmark / cursor-light text (install)
- `GLOW-57` إضاءة ثلاثية بالوقفات والكلفن / Three-point rig in stops & Kelvin (K3.lightRig) (proven)
- `GLOW-58` قوالب البورتريه السبعة / Seven portrait rig presets (K3.lightPreset) (ready)

### `GLOW-57` — إضاءة ثلاثية بالوقفات والكلفن / Three-point rig in stops & Kelvin (K3.lightRig)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مفتاح وتعبئة وحافة تُحدَّد كما في موقع التصوير: التعبئة N وقفات تحت المفتاح، والحافة M وقفات، ولكل ضوء حرارته. / Key, fill and rim set as on a real set: fill N stops under key, rim M stops over/under, each light with its own Kelvin.

**متى:** عند إضاءة مشهد ثلاثي الأبعاد كموقع تصوير حقيقي بمفتاح وتعبئة وحافة محسوبة بالوقفات والكلفن / for lighting a 3D scene like a real set: key, fill and rim set in stops and Kelvin, per shot

**كيف:** rig = K3.lightRig(scene, {...}); rig.set({...}) per shot; rig.ratio() reports the lighting ratio. Playbook rule: one rig per film, never default grey lighting; minimal three.js sample Hemisphere(0xffffff, 0x223344, .6) + Directional(0xffffff, 1.2) at (3,4,2). Verified here: ratio() = 5 with the defaults (K3 bundle in Chromium). (code snippet in references/powers/light-glow-bloom.md)

**المعاملات:** key 3.0 @5600 K az −40 el 35 (shadows); fill 6500 K az 45 el 10, −2 stops (5:1); rim 4300 K az 160 el 40, +.5 stop; distance 10

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إضاءة ثلاثية · وقفات · كلفن · three-point · key fill rim · stops · kelvin · rig · إضاءة سينمائية · ضوء رئيسي · ضوء التعبئة · lighting setup · three.js lights

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/motion/kit/three-kit.js:1009`
- `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:1009`
- `kosif-tool/playbooks/3d.md:15`
- `kosif-tool/playbooks/3d.md:60-61`

#### 7. قدرات قريبة في العائلة

- `GLOW-55` أشعة يلقيها النص ونص بشعاع المؤشر / Volumetric rays cast by a wordmark / cursor-light text (install)
- `GLOW-56` الشمس والهالة والكسوف / Blooming sun, corona & eclipse (2D and 3D) (install)
- `GLOW-58` قوالب البورتريه السبعة / Seven portrait rig presets (K3.lightPreset) (ready)
- `GLOW-59` ثمانية عشر إعداد إضاءة وخطة الطاقم / 18 named lighting setups & the /lightplan deliverable (documented)

### `GLOW-58` — قوالب البورتريه السبعة / Seven portrait rig presets (K3.lightPreset)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إعدادات مصوري البورتريه كتركيبات جاهزة، ونعومة الظل محسوبة من حجم المصدر ومسافته. / Photographers' portrait setups as ready rigs, with shadow softness derived from source size and distance.

**متى:** حين يريد المستخدم إضاءة بورتريه جاهزة كرامبرانت أو الصدفة بنعومة ظل من حجم المصدر ومسافته / when the user wants ready portrait lighting like Rembrandt or clamshell, with shadow softness from source size and distance

**كيف:** const rig = K3.lightPreset(scene, name, {target, distance, key}); rig.softness gives the apparent size in degrees (shadow.radius = deg/3). Table below. (full table in references/powers/light-glow-bloom.md)

**المعاملات:** see table

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بورتريه · رامبرانت · portrait · rembrandt · clamshell · presets · softness · إضاءة بورتريه · إضاءة وجه · ظل ناعم · portrait lighting · soft shadows

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/motion/kit/three-kit.js:1108`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1110`
- `kosif-studio/motion/references/book-lessons.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-56` الشمس والهالة والكسوف / Blooming sun, corona & eclipse (2D and 3D) (install)
- `GLOW-57` إضاءة ثلاثية بالوقفات والكلفن / Three-point rig in stops & Kelvin (K3.lightRig) (proven)
- `GLOW-59` ثمانية عشر إعداد إضاءة وخطة الطاقم / 18 named lighting setups & the /lightplan deliverable (documented)
- `GLOW-60` حاسبة الضوء / Light calculator (ratio · softness · falloff · EV · guide number · shutter angle · mired) (proven)

### `GLOW-59` — ثمانية عشر إعداد إضاءة وخطة الطاقم / 18 named lighting setups & the /lightplan deliverable

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جدول إعدادات بالزاوية والنسبة والكلفن والمزاج وجملة برومبت، وخطة إضاءة كاملة يمكن تسليمها لطاقم أو إعادة بنائها ثلاثيًا. / A preset table with angle, ratio, Kelvin, mood and a prompt fragment, plus a full lighting plan a crew can execute or 3D can rebuild.

**متى:** حين يطلب المستخدم إعداد إضاءة معروفًا أو خطة إضاءة كاملة ينفذها طاقم تصوير أو يعاد بناؤها ثلاثيًا / when the user asks for a named lighting setup or a full lighting plan a crew can execute or a 3D scene can rebuild

**كيف:** Pick a setup → compute ratios/gels with light_calc (GLOW-60) → /lightplan: mood line → ASCII top view (12 = behind, 6 = camera) → per-light table (role, fixture, modifier, power/stops, height, angle, distance, gel) → computed ratios & exposure → camera ISO/shutter/aperture/WB → budget version (window + lamp + foam board + phone light) → common mistakes → English prompt fragment. /relight freezes identity/pose. Product: big soft key + fill + rim to edge glass/metal, one consistent shadow; Kelvin per source, avoid unintended mixing. (full table in references/powers/light-glow-bloom.md)

**المعاملات:** see table

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إعدادات إضاءة · خطة إضاءة · برومبت · lighting presets · light plan · rembrandt · neon noir · golden hour · crew · طاقم التصوير · مخطط إضاءة · تصوير سينمائي · lighting diagram · cinematography

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-59` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-one/tools/kosif-omni/skills/kosif-lighting/references/lighting-presets.md`
- `kosif-one/tools/kosif-omni/skills/kosif-lighting/SKILL.md`
- `100-superskills/skills/kosif-montage-motion/references/visual-catalog.md`
- `100-superskills/skills/photo-lighting-plan/SKILL.md:22`

#### 7. قدرات قريبة في العائلة

- `GLOW-57` إضاءة ثلاثية بالوقفات والكلفن / Three-point rig in stops & Kelvin (K3.lightRig) (proven)
- `GLOW-58` قوالب البورتريه السبعة / Seven portrait rig presets (K3.lightPreset) (ready)
- `GLOW-60` حاسبة الضوء / Light calculator (ratio · softness · falloff · EV · guide number · shutter angle · mired) (proven)
- `GLOW-61` حرارة اللون والجيلاتين ومصادر مسماة / Kelvin → RGB, gels & 19 named light sources (proven)

### `GLOW-60` — حاسبة الضوء / Light calculator (ratio · softness · falloff · EV · guide number · shutter angle · mired)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حسابات تصوير حتمية: نسبة الإضاءة ومزاجها، نعومة المصدر، سقوط الضوء بالمسافة، قيمة التعريض، وزاوية الغالق. / Deterministic photo/cinema maths: lighting ratio and mood, source softness, distance falloff, exposure value, shutter angle.

**متى:** عند حساب نسبة الإضاءة أو نعومة المصدر أو سقوط الضوء بالمسافة أو التعريض أو زاوية الغالق بدقة / for calculating lighting ratio, source softness, distance falloff, exposure value or shutter angle exactly

**كيف:** echo '[{"op":"ratio","key_stops_over_fill":2}, ...]' \| python3 scripts/omni/light_calc.py (or the MCP kosif_light_calc, list via ops=[…]); JS twins K3.softnessDeg(size, dist) = 2·atan(size/2d), K3.falloffStops(d1, d2) = 2·log2(d2/d1). Ran here 2026-10-16, results in params.

**المعاملات:** ratio 2 stops → 5:1 'dramatic' (≤2.5 flat, ≤4.5 natural, ≤9 dramatic, else noir); 4:1 → fill 1.58 stops; softness 1.2 m @1.5 m → 43.6° 'soft' (>45 very soft, >20 soft, >8 medium); falloff 2 m→4 m = 2 stops; EV f/2.8 1/125 ISO100 = 9.94; 24 fps @180° = 1/48 s; GN 60 ISO100 5 m → f/12; mired 5600→3200 = +133.9 Full CTO

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حاسبة · نسبة الإضاءة · تعريض · light calculator · ratio · inverse square · softness · ev · shutter angle · mired · حسابات التصوير · زاوية الغالق · سقوط الضوء · exposure calc · falloff

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-60` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/omni/light_calc.py:40`
- `kosif-one/tools/kosif-omni/skills/kosif-lighting/scripts/light_calc.py:45`
- `kosif-one/tools/kosif-omni/mcp-server/tests/test_server.py:198`
- `kosif-studio/motion/kit/three-kit.js:1026`

#### 7. قدرات قريبة في العائلة

- `GLOW-58` قوالب البورتريه السبعة / Seven portrait rig presets (K3.lightPreset) (ready)
- `GLOW-59` ثمانية عشر إعداد إضاءة وخطة الطاقم / 18 named lighting setups & the /lightplan deliverable (documented)
- `GLOW-61` حرارة اللون والجيلاتين ومصادر مسماة / Kelvin → RGB, gels & 19 named light sources (proven)
- `GLOW-62` ارتداد السماء وضباب نحو الشمس / Sky bounce, fog toward the sun & blue-hour painting (ready)

### `GLOW-61` — حرارة اللون والجيلاتين ومصادر مسماة / Kelvin → RGB, gels & 19 named light sources

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تحويل الكلفن إلى لون RGB، وحساب إزاحة المايرد وأقرب جيلاتين CTO/CTB، وجدول 19 مصدر ضوء حقيقي. / Kelvin → linear RGB, the mired shift and nearest CTO/CTB gel, and a table of 19 real light sources.

**متى:** حين تحتاج تحويل حرارة اللون بالكلفن إلى RGB أو اختيار جيلاتين تصحيح أو لون مصدر ضوء حقيقي / when converting Kelvin to RGB, picking a correction gel or matching the colour of a real light source

**كيف:** K3.kelvin(K) → THREE.Color (Tanner Helland Planckian fit, 1000–40000 K); K3.gel(fromK, toK) → {mired, gel}; K3.lightColor(name) from K3.LIGHT_SOURCES. Verified here: kelvin(1900) = #ff8400, kelvin(3200) = #ffb87b, gel(5600, 3200) = {mired 134, 'Full CTO'}. Shore lights kelvin(2200–3100) at 70% / kelvin(5200).

**المعاملات:** candle 1850 K, firelight 1900, sodium #ffa040, tungsten 2700, halogen 3200, sunrise 3000, golden_hour 3500, led_warm 3000, led_neutral 4000, mercury #bff0dc, metal_halide 4300, fluorescent #e8f5e6, moonlight #9fb4d9, daylight 5600, overcast 6500, open_shade 8000, blue_sky 11000, neon_red #ff2a3a, neon_blue #3a7bff; gels Full CTB −159 · ½ −68 · ¼ −30 · ⅛ −12 · ⅛ CTO +20 · ¼ +42 · ½ +81 · Full +159

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كلفن · حرارة اللون · جيلاتين · kelvin · color temperature · gel · cto · ctb · sodium · light sources · لون الضوء · ضوء دافئ · ضوء بارد · warm light · kelvin to rgb

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-61` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/motion/kit/three-kit.js:992`
- `kosif-studio/motion/kit/three-kit.js:1001`
- `kosif-studio/motion/kit/three-kit.js:1183`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:137`

#### 7. قدرات قريبة في العائلة

- `GLOW-59` ثمانية عشر إعداد إضاءة وخطة الطاقم / 18 named lighting setups & the /lightplan deliverable (documented)
- `GLOW-60` حاسبة الضوء / Light calculator (ratio · softness · falloff · EV · guide number · shutter angle · mired) (proven)
- `GLOW-62` ارتداد السماء وضباب نحو الشمس / Sky bounce, fog toward the sun & blue-hour painting (ready)
- `GLOW-63` إضاءة الحافة في الرسم / Painter rim light & two-colour wet rims (proven)

### `GLOW-62` — ارتداد السماء وضباب نحو الشمس / Sky bounce, fog toward the sun & blue-hour painting

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** السطوح المظللة المواجهة للأعلى تبرد من السماء والمواجهة للأسفل تدفأ من الأرض، والضباب يدفأ فقط حين تواجه الكاميرا شمسًا منخفضة. / Up-facing shadow planes go cool from the sky, down-facing ones warm from the ground, and haze warms only when the camera faces a low sun.

**متى:** حين يحتاج مشهد خارجي ثلاثي الأبعاد ارتدادًا باردًا من السماء ودافئًا من الأرض وضبابًا نحو الشمس / when an outdoor 3D scene needs cool sky bounce, warm ground bounce, sun-facing haze or a blue-hour look

**كيف:** K3.skyBounce(scene, {sky, ground, intensity}); K3.fogTowardSun(scene, camera, sunDir, cool, warm, amount) each frame (alignment³). Blue-hour recipe (Gurney lessons in 3D): aerialPerspective scatter [.55, .8, 1.3], AgX tone mapping exposure 1.05, FogExp2 #8790B0 .00062, fov 32, ridges at .7/1.4/2.6/4.5 km, sodium lamps with colour corona against the blue sky, weak sunrise-coloured directional .35 for the afterglow, 1600 stars on a rotating pole.

**المعاملات:** sky = blue_sky 11000 K, ground #b07a4a, intensity .6; blue_hour sky 0x5a7ab8 ground 0x6a4a36 1.25

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ارتداد · ساعة زرقاء · ضباب · sky bounce · hemisphere · blue hour · aerial perspective · fog · ضوء السماء · ضباب جوي · منظر طبيعي · outdoor lighting · haze

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-62` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/motion/kit/three-kit.js:1194`
- `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:1201`
- `kosif-studio/motion/projects/blue_hour/src/main.js:1`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:93`

#### 7. قدرات قريبة في العائلة

- `GLOW-60` حاسبة الضوء / Light calculator (ratio · softness · falloff · EV · guide number · shutter angle · mired) (proven)
- `GLOW-61` حرارة اللون والجيلاتين ومصادر مسماة / Kelvin → RGB, gels & 19 named light sources (proven)
- `GLOW-63` إضاءة الحافة في الرسم / Painter rim light & two-colour wet rims (proven)
- `GLOW-64` تظليل الحجم نحو الضوء / Form shading toward a light point (proven)

### `GLOW-63` — إضاءة الحافة في الرسم / Painter rim light & two-colour wet rims

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الحافة المواجهة لاتجاه الضوء تأخذ شريطًا ناعمًا من لونه — الحيلة التي تفصل الظلال عن الخلفية. / The edge band facing the light direction gets a soft band of its colour — the trick that separates silhouettes from the background.

**متى:** عند فصل الأشكال عن الخلفية في الرسم بالكود بشريط ضوء على الحافة المواجهة لمصدر الضوء / for separating code-painted silhouettes from the background with a soft rim band facing the light

**كيف:** rim(shape, toward=(dx,dy), width, colour, alpha, soft=.6, mode='add') = shape mask minus a copy shifted away from the light, softened. Three-light cinematic setup: a cool key (moon/lightning), a warm key (fire/sunset) and a dim ambient; every body gets a rim from each key in its true direction, the warm one stronger near its source. Wet surfaces: two opposing rims. Ran here 2026-10-16.

**المعاملات:** width 2–4 (+ wide soft pass 8–10, soft 2–2.4, α .3); wet: rim((.7,−1), 2.6, '#ff9a4a', .8) + rim((−.4,−1), 1.8, '#9fb5da', .55); whale lights COLD (1010,120,520,#cfe0ff,1.0) · WARM (684,356,150,#ff8a3a,1.7) · AMBIENT (600,−400,900,#5a6c88,.35)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** إضاءة الحافة · ظل · رسم · rim light · silhouette · painter · wet · two-colour rim · فصل عن الخلفية · حافة مضيئة · ضوء خلفي · edge light · separation

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-63` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/render.py:412`
- `kosif-studio/scenes/duck_dragon.py:229`
- `kosif-studio/references/drawing-guide.md:62`
- `kosif-studio/scenes/whale_dragon.py:30`

#### 7. قدرات قريبة في العائلة

- `GLOW-61` حرارة اللون والجيلاتين ومصادر مسماة / Kelvin → RGB, gels & 19 named light sources (proven)
- `GLOW-62` ارتداد السماء وضباب نحو الشمس / Sky bounce, fog toward the sun & blue-hour painting (ready)
- `GLOW-64` تظليل الحجم نحو الضوء / Form shading toward a light point (proven)
- `GLOW-65` جسم مضاء فيزيائيًا وسحب مجسمة / Physically lit relief bodies & cloud decks (install)

### `GLOW-64` — تظليل الحجم نحو الضوء / Form shading toward a light point

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تدرج شعاعي من اللون المضاء إلى الداكن مزاح نحو الضوء يجعل الشكل المسطح يبدو مستديرًا. / A radial gradient from lit to dark, offset toward the light, makes a flat shape read as rounded.

**متى:** حين يبدو شكل مرسوم مسطحًا وتريده مستديرًا بتدرج من المضاء إلى الداكن مزاح نحو الضوء / when a painted flat shape should read as rounded via a lit-to-dark radial gradient offset toward the light

**كيف:** shade(shape, light_xy, lit, dark, core=.35, soft=0): hotspot offset = r·core toward the light, gradient radius r·(1 + core). Tested (test_studio.py:71) and ran here in the smoke render.

**المعاملات:** core .35; radius r·(1 + core)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تظليل · حجم · shading · volume · form · painter · gradient · تجسيم · تدرج شعاعي · ظل وضوء · radial gradient · 3d look

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-64` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/render.py:524`
- `kosif-studio/tests/test_studio.py:71`
- `kosif-one/tools/kosif-studio/render.py:524`

#### 7. قدرات قريبة في العائلة

- `GLOW-62` ارتداد السماء وضباب نحو الشمس / Sky bounce, fog toward the sun & blue-hour painting (ready)
- `GLOW-63` إضاءة الحافة في الرسم / Painter rim light & two-colour wet rims (proven)
- `GLOW-65` جسم مضاء فيزيائيًا وسحب مجسمة / Physically lit relief bodies & cloud decks (install)
- `GLOW-66` مظلل البلورة: فرينل ولمعة وانعكاس سماء / Fresnel + Blinn glass/crystal shader (proven)

### `GLOW-65` — جسم مضاء فيزيائيًا وسحب مجسمة / Physically lit relief bodies & cloud decks

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يحوّل الشكل المسطح إلى حجم مضاء: حقل ارتفاع، نتوءات متعددة المقاييس، إضاءة نقطية حقيقية مع لمعة وفرينل وتشتت تحت السطح. / Turns a flat silhouette into a lit volume: height field, multi-scale bumps, real point lights with Blinn specular, Fresnel and subsurface scattering.

**متى:** حين تريد تحويل شكل مسطح في الرسم بالكود إلى جسم مجسم مضاء أو طبقة سحب لها حجم / when turning a flat code-painted silhouette into a lit volumetric body or a cloud deck with real point lights

**كيف:** relief(shape, lights, base, ambient, bulge, plateau, shininess, spec, bump, bump_cell, seed, fresnel, fres_col, soft, bumps=[(amp, cell)], sss, sss_col, roughness); clouds = relief(deck, [COLD, fire, AMBIENT], '#1c2430', .25, .9, .7, 8, .08, bumps=[(14,46),(5,14)], seed=12, soft=5, sss=8) between dark blurred fills. Needs OpenCV (Sobel normals) — not installed here.

**المعاملات:** ambient .22, bulge .6, plateau .5, shininess 30, spec .5; whale bumps [(2,40),(.9,12),(.3,3.5)], sss 2.5 #e8d8d0, roughness .55

**التثبيت:** pip install opencv-python-headless

**الوسوم:** حجم · سحب · جلد · relief · height field · subsurface · clouds · painter · opencv · تجسيم · ملمس · إضاءة نقطية · bump map · 3d shading

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:opencv` ← python3 -c "import opencv" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-65` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/render.py:573`
- `kosif-studio/render.py:618`
- `kosif-studio/scenes/whale_dragon.py:93`

#### 7. قدرات قريبة في العائلة

- `GLOW-63` إضاءة الحافة في الرسم / Painter rim light & two-colour wet rims (proven)
- `GLOW-64` تظليل الحجم نحو الضوء / Form shading toward a light point (proven)
- `GLOW-66` مظلل البلورة: فرينل ولمعة وانعكاس سماء / Fresnel + Blinn glass/crystal shader (proven)
- `GLOW-67` زجاج بانكسار وتشتت وكرات زجاجية / Refraction, dispersion & glass orbs (install)

### `GLOW-66` — مظلل البلورة: فرينل ولمعة وانعكاس سماء / Fresnel + Blinn glass/crystal shader

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مظلل يجعل البلورات المضلعة تُقرأ زجاجًا: لون بحسب الاتجاه، سماء منعكسة، حافة فرينل، لمعة حادة، وضباب. / A fragment shader that makes faceted crystals read as glass: body colour by normal, reflected sky, Fresnel rim, sharp Blinn highlight, fog.

**متى:** حين يجب أن تبدو بلورات أو أجسام مضلعة كالزجاج أو الجليد في مشهد ثلاثي الأبعاد / when faceted crystals or shapes in a 3D scene should read as glass or ice

**كيف:** Tested in the earth crystal world. Fresnel power 2–4 sells glass/atmospheres; Blinn-Phong half = normalize(eye + light), spec = pow(dot(n, h), shininess). (code snippet in references/powers/light-glow-bloom.md)

**المعاملات:** fresnel exp 2.6; spec exp 64; rim .9; fog near 6 far 24; key light dir (.5, .9, .6)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** زجاج · بلورة · فرينل · glass · crystal · fresnel · blinn-phong · shader · ice · جليد · كريستال · لمعة · specular · faceted

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-66` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-earth-ci-fork/ui/art/crystal-world.js:46`
- `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`
- `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-64` تظليل الحجم نحو الضوء / Form shading toward a light point (proven)
- `GLOW-65` جسم مضاء فيزيائيًا وسحب مجسمة / Physically lit relief bodies & cloud decks (install)
- `GLOW-67` زجاج بانكسار وتشتت وكرات زجاجية / Refraction, dispersion & glass orbs (install)
- `GLOW-68` حافة نيون من ألوان الواجهة وإضاءة نابضة / Accent rim rig from the UI palette (pulsing) (install)

### `GLOW-67` — زجاج بانكسار وتشتت وكرات زجاجية / Refraction, dispersion & glass orbs

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أجسام زجاجية تكسر ما خلفها بمعامل انكسار، وتشتت لوني لكل قناة، وكرة زجاجية بلمعة علوية وهالات. / Glass that bends what is behind it by IOR, per-channel dispersion, and glass orbs with a top highlight and halos.

**متى:** حين يحتاج المشهد زجاجًا يكسر ما خلفه أو تشتتًا لونيًا أو كرة زجاجية لامعة بهالات / when a scene needs glass that bends what is behind it, colour dispersion, or a glossy glass orb with halos

**كيف:** three.js: refract(view, normal, 1/IOR); per-channel IOR for dispersion; Fresnel rim; backside FBO trick. CSS orb: radial-gradient circle + backdrop-filter blur + an inner highlight crescent (+ 3–4 faint concentric halo rings, inner orange hotspot as in style:product). HyperFrames cosmic-orb block: iridescent soap-bubble planet with nebula bands and edge chromatic aberration.

**المعاملات:** IOR 1/1.31 (ice) … 1.45–1.5 (glass); cosmic-orb hue 268, accent 196, spin .035, size .86, backdrop #04040a, 10 s

**التثبيت:** npm i three@0.186.1 # or: npx hyperframes@0.8.164 add cosmic-orb

**الوسوم:** زجاج · انكسار · كرة · glass · refraction · dispersion · ior · orb · lens · كرة زجاجية · انكسار الضوء · شفافية · glass sphere · transparent

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-67` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`
- `kosif-one/vendor/hyperframes/registry/blocks/cosmic-orb/cosmic-orb.html`
- `style:pm-hbcoop-de365c`
- `style:product`

#### 7. قدرات قريبة في العائلة

- `GLOW-65` جسم مضاء فيزيائيًا وسحب مجسمة / Physically lit relief bodies & cloud decks (install)
- `GLOW-66` مظلل البلورة: فرينل ولمعة وانعكاس سماء / Fresnel + Blinn glass/crystal shader (proven)
- `GLOW-68` حافة نيون من ألوان الواجهة وإضاءة نابضة / Accent rim rig from the UI palette (pulsing) (install)
- `GLOW-69` استوديو كريمي بثلاث إضاءات / Cream studio sweep with a soft 3-light rig (ready)

### `GLOW-68` — حافة نيون من ألوان الواجهة وإضاءة نابضة / Accent rim rig from the UI palette (pulsing)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شخصية أو جسم يُضاء كمنتج: مفتاح دافئ ناعم وتعبئة باردة وحافتان ملونتان من ألوان الواجهة، وأضواء تنبض فيتنفس الجسم. / A character or object lit like a product: soft warm key, cool fill and two coloured rims from the overlay palette, with pulsing accents so it breathes.

**متى:** عند إضاءة شخصية أو جسم ثلاثي الأبعاد كمنتج بحافتين ملونتين من ألوان الواجهة وأضواء نابضة / when lighting a 3D character or object like a product, with two coloured rims from the UI palette and pulsing accents

**كيف:** bunny_twin: DirectionalLight 0xfff3ea 2.3 (shadow 1024, radius 6, bias −.0004); Hemisphere 0xd8fff2/0x1a2624 .32; SpotLight 0x9dffb4 2.4 and 0xffb8d0 1.5 (dist 3, angle .7, penumbra .6); envFromGradient top 0x8fd6c4 sunPower 2.5, environmentIntensity .5. cinematic_3d: ambient #0f172a 1.5; dir #38bdf8 3.5 at (5,8,5); rim point #f43f5e 5.0 range 50 at (−6,−2,−4); gold point #fbbf24 4.0 range 40 at (4,−4,3); per frame gold = 3.5 + 1.2·sin(3t), rim = 4.0 + 1.5·cos(2.5t).

**المعاملات:** pulse 3 rad/s & 2.5 rad/s, amplitude 1.2 & 1.5

**التثبيت:** npm i three@0.186.1 esbuild

**الوسوم:** حافة نيون · شخصية · منتج · rim light · accent · hud palette · pulsing lights · three.js · إضاءة شخصية · أضواء نابضة · ألوان الواجهة · character lighting · colored rim

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:esbuild` ← npm ls esbuild أو وجود node_modules/esbuild
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-68` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:30`
- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:112`
- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:206`

#### 7. قدرات قريبة في العائلة

- `GLOW-66` مظلل البلورة: فرينل ولمعة وانعكاس سماء / Fresnel + Blinn glass/crystal shader (proven)
- `GLOW-67` زجاج بانكسار وتشتت وكرات زجاجية / Refraction, dispersion & glass orbs (install)
- `GLOW-69` استوديو كريمي بثلاث إضاءات / Cream studio sweep with a soft 3-light rig (ready)
- `GLOW-70` ظل وانعكاس متسقان مع مفتاح واحد / One-key consistency: shadow, lit edge & reflection (ready)

### `GLOW-69` — استوديو كريمي بثلاث إضاءات / Cream studio sweep with a soft 3-light rig

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خلفية سويب كريمية وظل تلامس وشبكة باهتة وإضاءة ناعمة ثلاثية لأفلام المختبر والمنتج. / A cream sweep background, contact shadow, faint grid and a soft three-light rig for product-lab films.

**متى:** حين يحتاج فيلم منتج أو مختبر خلفية استوديو كريمية بظل تلامس وإضاءة ناعمة ثلاثية / for a product or lab film needing a cream studio sweep with contact shadow and a soft three-light rig

**كيف:** K3.studio(scene, {bg, grid}) from lab-kit; pair with labPost (rays off, tuned for software GL).

**المعاملات:** bg #f1efe8; key 2.6 at (3,6,4); fill 0xdfe8ff .9; rim 1.4; hemisphere .9; shadow opacity .22; grid #c9d8c2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** استوديو · منتج · مختبر · studio sweep · product · lab · soft light · contact shadow · خلفية فاتحة · تصوير منتج · إضاءة ناعمة · seamless backdrop · clean studio

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-69` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-one/tools/kosif-studio/motion/kit/lab-kit.js:194`
- `100-superskills/skills/kosif-montage-motion/SKILL.md:101`

#### 7. قدرات قريبة في العائلة

- `GLOW-67` زجاج بانكسار وتشتت وكرات زجاجية / Refraction, dispersion & glass orbs (install)
- `GLOW-68` حافة نيون من ألوان الواجهة وإضاءة نابضة / Accent rim rig from the UI palette (pulsing) (install)
- `GLOW-70` ظل وانعكاس متسقان مع مفتاح واحد / One-key consistency: shadow, lit edge & reflection (ready)
- `GLOW-71` قراءة إضاءة صورة مرجعية / Read the light of a reference image (ready)

### `GLOW-70` — ظل وانعكاس متسقان مع مفتاح واحد / One-key consistency: shadow, lit edge & reflection

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إزاحة الظل وحافة الإضاءة وشريط الانعكاس كلها تتفق مع مفتاح واحد أعلى اليسار، وتُعاد حسابها مع الدوران والارتفاع. / Shadow offset, lit-edge highlight and reflection band all agree with one top-left key and are recomputed with yaw and lift.

**متى:** حين يجب أن يتفق ظل المنتج أو الهاتف وحافته المضيئة وانعكاسه مع ضوء رئيسي واحد أثناء الدوران / when shadows, edge highlights and reflections on a phone or product must agree with one key light as it turns

**كيف:** box-shadow `${-yaw*1.6}px 48px 90px rgba(0,0,0,.55)`, inset 1px rgba(255,255,255,.09); reflection linear-gradient(115deg, transparent 40%, rgba(255,255,255,.14) 50%, transparent 60%); recompute per frame from yaw and lift. MG-034 shadow-first: 0–1 s a separate shadow layer slides in, 1–2 s the product lands into it, 2–5 s benefit; its size/blur follow the product's Y and its direction matches the photo's light.

**المعاملات:** shadow down 40–60 px, x ≈ −yaw×1.6; ambient blur 60–100 px @50%; contact 8–12 px @35%; reflection 10–16% white; 140 px rise → blur +30%, opacity −20%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ظل · انعكاس · اتساق · shadow · reflection · consistency · phone · product · key light · اتساق الإضاءة · ظل المنتج · موك اب · lighting consistency · drop shadow

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-70` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-tool/playbooks/phone.md:23`
- `kosif-tool/playbooks/phone.md:43`
- `kosif-tool/playbooks/phone.md:128-138`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-product-ads.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-68` حافة نيون من ألوان الواجهة وإضاءة نابضة / Accent rim rig from the UI palette (pulsing) (install)
- `GLOW-69` استوديو كريمي بثلاث إضاءات / Cream studio sweep with a soft 3-light rig (ready)
- `GLOW-71` قراءة إضاءة صورة مرجعية / Read the light of a reference image (ready)
- `GLOW-72` وصفات إضاءة مقفلة لمولدات الصور والفيديو / Locked lighting phrases for AI plates (key)

### `GLOW-71` — قراءة إضاءة صورة مرجعية / Read the light of a reference image

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يخمّن أي جانب أسطع وكم وقفة بين المضاء والظل من متوسطات الإضاءة، كتقدير صريح. / Guesses which side is brighter and the lit-to-shadow ratio in stops from luminance halves — reported as a heuristic.

**متى:** حين يعطي المستخدم صورة مرجعية ويريد مطابقة إضاءتها: أي جانب أسطع وكم وقفة بين الضوء والظل / when the user gives a reference image and wants to match its lighting: brighter side and lit-to-shadow ratio

**كيف:** image_analyze.py analyze(): mean luma of left/right/top/bottom halves; side_ratio_stops = log2(lit/shade); lighting_ratio = 2^stops : 1; then feed K3.lightRig / lightPreset and keep shadows pointing the same way (GLOW-70).

**المعاملات:** side threshold 8 luma levels

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مطابقة · تحليل صورة · match lighting · reference · image analysis · ratio · صورة مرجعية · مطابقة الإضاءة · اتجاه الضوء · light direction · lighting ratio

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-71` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:120`

#### 7. قدرات قريبة في العائلة

- `GLOW-69` استوديو كريمي بثلاث إضاءات / Cream studio sweep with a soft 3-light rig (ready)
- `GLOW-70` ظل وانعكاس متسقان مع مفتاح واحد / One-key consistency: shadow, lit edge & reflection (ready)
- `GLOW-72` وصفات إضاءة مقفلة لمولدات الصور والفيديو / Locked lighting phrases for AI plates (key)
- `GLOW-73` سماء فيزيائية وشمس وبيئة من تدرج / Physical sky, sun, fill & gradient environment (ready)

### `GLOW-72` — وصفات إضاءة مقفلة لمولدات الصور والفيديو / Locked lighting phrases for AI plates

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جمل إضاءة قصيرة تغيّر المزاج بثبات، ووصفات مقفلة لكل نوع إنتاج تُنسخ كما هي في كل مقطع. / Short lighting phrases that reliably change mood, and locked per-genre recipes copied verbatim into every clip.

**متى:** عند كتابة برومبت لمولد صور أو فيديو يحتاج إضاءة ثابتة المزاج ومتسقة بين كل المقاطع / when writing image or video generation prompts that need a reliable lighting mood, locked across every clip

**كيف:** One key-light phrase + direction + temperature (e.g. warm directional light from a high window camera-left, soft Rembrandt triangle); rim/volumetric for hero and abstract plates, flat/even for icons and diagrams. Locks: car = large softbox key front-left + thin right rim + soft floor reflection; food = golden overhead practical + left softbox + gentle counter shadows; fitness = single overhead teal-blue rim fading to black, close shot 4–6 s with a localised red/orange heat-map glow on the target muscle (labels in post); documentary L = amber top spotlight with smoke haze. The prompt builders are tested here; the picture itself needs a generation service — the profiles target Google Flow / Veo (food-flow.mjs:98), so that account (or another image/video API key) is required.

**المعاملات:** vocabulary: natural, studio, rim, soft directional, volumetric rays, flat/even, golden hour, high key, Rembrandt, chiaroscuro

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** برومبت · توليد · إضاءة · prompt · ai plates · lighting vocabulary · consistency · kling · image generation · وصف الإضاءة · مولد صور · توليد فيديو · prompt lighting · ai video

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-72` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `fastify-motion-bro/scripts/profiles/car-exploded.mjs:56`
- `fastify-motion-bro/scripts/profiles/fitness.mjs:32`
- `fastify-motion-bro/tests/production-profiles.test.mjs:29-32`
- `kosif-atlas/skills/1446-marketing-skills/3504-image`

#### 7. قدرات قريبة في العائلة

- `GLOW-70` ظل وانعكاس متسقان مع مفتاح واحد / One-key consistency: shadow, lit edge & reflection (ready)
- `GLOW-71` قراءة إضاءة صورة مرجعية / Read the light of a reference image (ready)
- `GLOW-73` سماء فيزيائية وشمس وبيئة من تدرج / Physical sky, sun, fill & gradient environment (ready)
- `GLOW-74` ضوء متسلل بين الأوراق / Dappled sunlight (komorebi gobo) (ready)

### `GLOW-73` — سماء فيزيائية وشمس وبيئة من تدرج / Physical sky, sun, fill & gradient environment

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قبة سماء بتشتت جوي وشمس بالارتفاع والسمت، وضوء شمس يلقي ظلًا مع تعبئة من جهة الكاميرا، وبيئة انعكاس من تدرج محدود. / An atmospheric-scattering sky with the sun placed by elevation/azimuth, a shadow-casting sun with a camera-side fill, and a bounded gradient environment for reflections.

**متى:** حين يحتاج مشهد ثلاثي الأبعاد سماء واقعية وشمسًا بزاوية محددة تلقي ظلالًا وبيئة للانعكاسات / when a 3D scene needs a realistic sky, a sun placed by angle casting shadows, and an environment for reflections

**كيف:** sky = K3.makeSky(scene, {turbidity, rayleigh, mie, mieG}); sky.setSun(elevDeg, azimDeg); K3.makeSunLight(scene, {intensity, shadowSize, bounds, far}); K3.makeFill(scene, 0xcfe0ff) (intensity set per frame); K3.envFromGradient(renderer, scene, {top, horizon, ground, sun, sunColor, sunPower}) — PMREM from a bounded gradient avoids the Sky shader's sun-disk Inf/NaN black rectangles (envFromSky is the risky alternative). Procedural dome alternative: back-faced sphere shader with a 3-colour gradient, sun = pow(s,1800/size)·30 + pow(s,40)·.8 + pow(s,6)·.25, hashed twinkling stars.

**المعاملات:** turbidity 3, rayleigh 1.6, mie .004, mieG .85, scale 45000; sun 3.0, shadow map 4096, bounds 2300, bias −.0005, normalBias 2; env top #7da2cc horizon #f0cfa0 ground #3a3a2a sun #ffd29a power 6; domes: dawn #1C4C98/#F0A878, golden #2E4A7A/#FFB067, night #03061A/#1A1F54, blue hour #081433/#D9806A

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** سماء · شمس · بيئة · sky · sun · preetham · environment map · pmrem · fill light · سماء واقعية · ظلال الشمس · إضاءة نهارية · daylight · atmospheric scattering

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-73` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/motion/kit/three-kit.js:86`
- `kosif-studio/motion/kit/three-kit.js:98`
- `kosif-studio/motion/kit/three-kit.js:480`
- `kosif-one/projects/egypt-2120-animation/index.html:80-98`

#### 7. قدرات قريبة في العائلة

- `GLOW-71` قراءة إضاءة صورة مرجعية / Read the light of a reference image (ready)
- `GLOW-72` وصفات إضاءة مقفلة لمولدات الصور والفيديو / Locked lighting phrases for AI plates (key)
- `GLOW-74` ضوء متسلل بين الأوراق / Dappled sunlight (komorebi gobo) (ready)
- `GLOW-75` كاوستكس تحت الماء / Underwater caustics & absorption (ready)

### `GLOW-74` — ضوء متسلل بين الأوراق / Dappled sunlight (komorebi gobo)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كشاف بنسيج أوراق مولّد ينزلق قليلًا مع الزمن فتتحرك ظلال الأوراق على الأرض والماء. / A spotlight projecting a generated leafy cookie that slides slightly over time, so leaf shadows move on ground and water.

**متى:** حين يريد المستخدم ضوء شمس يتسلل بين أوراق الشجر فتتحرك ظلالها على الأرض أو الماء / when the user wants sunlight filtering through leaves, with leaf shadows moving on the ground or water

**كيف:** const d = K3.makeDappledSun(scene, {intensity, angle, color, density, floor, seed, shadowSize}); d.place(sunDir, target, dist); per frame d.setDapple(t); feed d.matrix() + texture to water (uDapple). SpotLight decay 0 makes it sun-like.

**المعاملات:** colour #ffd9a6 (koi #ffcf96); intensity 4 (3–5; koi 4.2); angle .24 rad (koi .19); penumbra .35; tex 512; floor .16; density .15; shadow 4096

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أوراق · شمس · ظلال · komorebi · dappled light · gobo · cookie · garden · ظل الشجر · حديقة · ضوء متقطع · leaf shadows · sun through trees

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-74` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/motion/kit/three-kit.js:765`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:35`
- `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:765`

#### 7. قدرات قريبة في العائلة

- `GLOW-72` وصفات إضاءة مقفلة لمولدات الصور والفيديو / Locked lighting phrases for AI plates (key)
- `GLOW-73` سماء فيزيائية وشمس وبيئة من تدرج / Physical sky, sun, fill & gradient environment (ready)
- `GLOW-75` كاوستكس تحت الماء / Underwater caustics & absorption (ready)
- `GLOW-76` التعريض الطويل وخطوط الضوء / Long-exposure lighten stack & continuous light trails (ready)

### `GLOW-75` — كاوستكس تحت الماء / Underwater caustics & absorption

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شبكة ضوء متحركة على السطوح تحت الماء من الشمس المباشرة فقط، مع امتصاص لوني بالعمق. / A moving caustic light network on surfaces below the waterline from direct sun only, plus per-channel absorption with depth.

**متى:** حين يحتاج مشهد تحت الماء أو بركة شبكة ضوء متحركة على السطوح مع تغير اللون بالعمق / when an underwater or pond scene needs a moving caustic light network on surfaces and colour absorption with depth

**كيف:** K3.addCaustics(material, {level, strength, scale, absorb, sun, time}) patches any Standard/Physical material.

**المعاملات:** strength 1.6; scale 1.6 (≈5.5 for 5–15 cm garden-pond cells); absorb RGB [1.6, .55, .42]/m; fades in 0–.12 m, gone by 1.2–3 m

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ماء · كاوستكس · caustics · underwater · absorption · pond · sea · تحت الماء · بركة · قاع البحر · water light · light network

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-75` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/motion/kit/three-kit.js:561`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:561`
- `kosif-studio/motion/references/hyperframes-authoring.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-73` سماء فيزيائية وشمس وبيئة من تدرج / Physical sky, sun, fill & gradient environment (ready)
- `GLOW-74` ضوء متسلل بين الأوراق / Dappled sunlight (komorebi gobo) (ready)
- `GLOW-76` التعريض الطويل وخطوط الضوء / Long-exposure lighten stack & continuous light trails (ready)
- `GLOW-77` هالات ومخاريط المصابيح ثنائية الأبعاد / 2D practical halos, lamp cones, lit windows & fireflies (proven)

### `GLOW-76` — التعريض الطويل وخطوط الضوء / Long-exposure lighten stack & continuous light trails

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تراكم عينات داخل الإطار: وضع «الأسطع» لمسارات النجوم والسيارات والرسم بالضوء، والمتوسط لماء حريري. / Sub-frame accumulation: 'lighten' keeps each pixel's brightest sample for star trails, car trails and light painting; 'average' gives silky water.

**متى:** حين يطلب المستخدم مسارات نجوم أو أضواء سيارات أو رسمًا بالضوء أو ماءً حريريًا بالتعريض الطويل / when the user wants star trails, car light trails, light painting or silky water via long-exposure stacking

**كيف:** render --blur 16 --shutter 30 --stack lighten\|average (window.__stack='lighten' with __blur > 1; MaxEquation blending). A light that moves farther than its size between sub-samples leaves dots — stretch it: mesh.scale.z = 1 + K3.trailLength(speed)/(2·radius), gap = speed·(shutter/fps)/k. 2D trails: keep the last 8–10 positions and draw them additively with decreasing alpha (tail ≈150 ms; orbit arcs with a 40% tail and a hot head sprite).

**المعاملات:** 1 s exposure per frame at 30 fps; 16 sub-samples; shutter 30; 2D tail 8–10 positions

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تعريض طويل · خطوط ضوء · نجوم · long exposure · light trails · star trails · lighten · silky water · مسارات السيارات · رسم بالضوء · ماء حريري · light painting · car trails

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-76` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/motion/kit/three-kit.js:1221`
- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:442`
- `kosif-studio/tests/test_studio.py:793`
- `100-superskills/skills/kosif-montage-motion/references/book-lessons.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-74` ضوء متسلل بين الأوراق / Dappled sunlight (komorebi gobo) (ready)
- `GLOW-75` كاوستكس تحت الماء / Underwater caustics & absorption (ready)
- `GLOW-77` هالات ومخاريط المصابيح ثنائية الأبعاد / 2D practical halos, lamp cones, lit windows & fireflies (proven)
- `GLOW-78` أضواء المدينة الليلية ثلاثية الأبعاد / 3D night practicals: sodium lamps, additive point sprites & bokeh (install)

### `GLOW-77` — هالات ومخاريط المصابيح ثنائية الأبعاد / 2D practical halos, lamp cones, lit windows & fireflies

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** برك ضوء من تدرجات شعاعية للقمر واللافتات والمصابيح، ومخاريط شفافة تحت أعمدة الإنارة، ونوافذ تضاء ويراعات. / Soft light pools from radial gradients (moon, signs, lamps), translucent cones under street lamps, windows switching on and fireflies.

**متى:** عند رسم مشهد ليلي ثنائي الأبعاد بمصابيح شارع ومخاريط ضوء وهالات ونوافذ تضاء ويراعات / for a 2D night scene with street-lamp cones, soft halos, windows switching on and fireflies

**كيف:** SVG radialGradient defs layered over the scene with transparent edges (tested in midnight_cat). Practical pool: warm amber core → transparent in screen blend over a darkened scene, brightness falling off with distance from the lantern. Windows: switch on in sequence with warm fill + additive radial bloom 30–60 px; winter lamps fade pink → warm cream with a radial halo (80 px, 1 s) and slight room darkening; fireflies = small yellow dots with blurred halos on noise paths pulsing 1–2 Hz.

**المعاملات:** moon #a9d7ce .33 → #509eac .12 → 0; cyanHalo #28eee5 .2; roseHalo #ff4566 .23 pulsing .76 + .07·sin 5t; lampHalo #ffe3a4 .45 → #ffd378 .10 at 17%; beam #ffe4a3 .06 → 0; pool core #fff1cf, mid #f2b25a 40%, radius 200–400 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مصابيح · نوافذ · يراعات · هالة · lamp · halo · practical light · windows · fireflies · night city · أعمدة الإنارة · مشهد ليلي · إضاءة الشارع · street lamp · night scene

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-77` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:14`
- `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:16`
- `style:pm-kamstudiolabs-0b0824`
- `style:pm-abderrahmen-g-9e8ed0`

#### 7. قدرات قريبة في العائلة

- `GLOW-75` كاوستكس تحت الماء / Underwater caustics & absorption (ready)
- `GLOW-76` التعريض الطويل وخطوط الضوء / Long-exposure lighten stack & continuous light trails (ready)
- `GLOW-78` أضواء المدينة الليلية ثلاثية الأبعاد / 3D night practicals: sodium lamps, additive point sprites & bokeh (install)
- `GLOW-79` ارتعاش الفانوس والشمعة / Lantern & candle flicker (organic) (install)

### `GLOW-78` — أضواء المدينة الليلية ثلاثية الأبعاد / 3D night practicals: sodium lamps, additive point sprites & bokeh

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صف مصابيح صوديوم يُقرأ ضوءًا حقيقيًا بثمن رخيص، ونقاط ضوء مضافة لأضواء المدن والطائرات المسيّرة، وكرات بوكيه في الخلفية. / A row of sodium lamps that reads as real light cheaply, additive point sprites for city lights and drones, and bokeh orbs far behind.

**متى:** حين يحتاج مشهد ليلي ثلاثي الأبعاد صف مصابيح شارع أو آلاف أضواء المدينة والطائرات المسيرة أو بوكيه بكلفة منخفضة / when a 3D night scene needs cheap street-lamp rows, thousands of city or drone lights, or background bokeh

**كيف:** Lamps: 24 lamps every 45 m — emissive sodium×9 sphere r .22 (blooms), additive soft pool plane 16×16 m in sodium×.55 on wet asphalt (roughness .32), only the nearest 6 as true PointLight(sodium, 70, 45, 2). Points: BufferGeometry with position/color/aSize/aAlpha, ShaderMaterial transparent, depthWrite false, AdditiveBlending; gl_PointSize = clamp(aSize·1100/−mv.z, 1.5, 90); fragment a = smoothstep(.5, 0, d)², rgb·a·alpha·2.2; 5000 typical, FBO ping-pong for 100k+. Bokeh: 3–5 emissive spheres far behind (blue + warm orange, radius 3–6% of frame) through DOF, or soft sprite discs.

**المعاملات:** sodium #ffa040; 6 real lights; point size 1.5–90 px; 5000 points

**التثبيت:** npm i three@0.186.1 esbuild

**الوسوم:** صوديوم · مدينة ليلية · بوكيه · sodium · street lamps · point sprites · additive · bokeh · city lights · أضواء الشوارع · درونز · إضاءة ليلية · drones · night scene

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:esbuild` ← npm ls esbuild أو وجود node_modules/esbuild
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-78` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:96`
- `kosif-one/projects/egypt-2120-animation/index.html:142-158`
- `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`
- `style:pm-anilraok-eff262`

#### 7. قدرات قريبة في العائلة

- `GLOW-76` التعريض الطويل وخطوط الضوء / Long-exposure lighten stack & continuous light trails (ready)
- `GLOW-77` هالات ومخاريط المصابيح ثنائية الأبعاد / 2D practical halos, lamp cones, lit windows & fireflies (proven)
- `GLOW-79` ارتعاش الفانوس والشمعة / Lantern & candle flicker (organic) (install)
- `GLOW-80` شعاع منارة دوّار / Rotating lighthouse / beacon beam (install)

### `GLOW-79` — ارتعاش الفانوس والشمعة / Lantern & candle flicker (organic)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فانوس يرتعش بموجتين من الضوضاء ولا يهبط تحت 80%، فيقود الضوء النقطي واللهب والتوهج وبركة الماء معًا. / A lantern flickers with two octaves of noise and never drops below ~80%, driving point light, flame, glow sprite and water pool together.

**متى:** حين يحتاج فانوس أو شمعة أو نار ارتعاشًا طبيعيًا لا يهبط كثيرًا ويحرك اللهب والوهج معًا / when a lantern, candle or fire light needs an organic flicker that never dips too low and drives flame and glow together

**كيف:** fl = .9 + .07·perlin(7t, 1.3) + .04·perlin(19t, 4.1); lamp.intensity = 9·fl (range 26, decay 1.6); flame colour LANTERN×13·fl; glow opacity .32·fl; pool .85·fl; lantern swings .06·sin(1.1t + 1.3). Candle/fire presets: 1800–2200 K (candle 1850, firelight 1900), 6:1 ratio. Neon is different: it strikes and drops out (GLOW-02), it does not wobble.

**المعاملات:** floor ≈80%; octaves 7 Hz & 19 Hz; intensity 9, range 26, decay 1.6

**التثبيت:** npm i three@0.186.1 esbuild

**الوسوم:** فانوس · شمعة · لهب · lantern · candle · flicker · flame · perlin · نار · ضوء الشموع · ارتعاش · firelight · organic flicker

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:esbuild` ← npm ls esbuild أو وجود node_modules/esbuild
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-79` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:230`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:84`
- `100-superskills/skills/kosif-montage-motion/references/lighting-presets.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-77` هالات ومخاريط المصابيح ثنائية الأبعاد / 2D practical halos, lamp cones, lit windows & fireflies (proven)
- `GLOW-78` أضواء المدينة الليلية ثلاثية الأبعاد / 3D night practicals: sodium lamps, additive point sprites & bokeh (install)
- `GLOW-80` شعاع منارة دوّار / Rotating lighthouse / beacon beam (install)
- `GLOW-81` قمر مرسوم بهالة / Painted moon with halo (ready)

### `GLOW-80` — شعاع منارة دوّار / Rotating lighthouse / beacon beam

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شعاع ضوء حجمي مزيف: مخروطان مفتوحان بمظلل مضاف تتلاشى شفافيته على الطول، يدور حول المصباح. / A fake volumetric beam: two open cones with an additive shader whose alpha fades along the length, rotating around the lamp.

**متى:** حين يحتاج مشهد بحري ليلي شعاع منارة أو فنار دوارًا حول المصباح / when a night-sea scene needs a rotating lighthouse or beacon beam sweeping around the lamp

**كيف:** 3D: ConeGeometry(55, 900, 32, 1, true) translated −450, rotated ±90° inside a pivot; fragment a = pow(1 − v, 1.6)·.55·(.6 + .4·sin(u·2π·3)); beamPivot.rotation.y = 1.25t + 1.2; bloom at the source (≈1.5). 2D: two opposite triangular wedges (10–14°) from the lamp, linear alpha .35 → 0, 'lighter' blend, one revolution ≈6 s; failure beat: 3 flicker pulses of 400 ms, then cut to dark.

**المعاملات:** beam #FFE7B8; 1.25 rad/s (3D) or 6 s/rev (2D); wedge 10–14°

**التثبيت:** npm i three@0.186.1 # 3D cone; the 2D wedge needs nothing

**الوسوم:** منارة · شعاع · lighthouse · beacon · volumetric beam · cone · night sea · فنار · بحر ليلي · ضوء دوار · rotating light · light beam

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-80` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-one/projects/egypt-2120-animation/index.html:412-418`
- `kosif-tool/styles/pm-kamstudiolabs-0b0824/BRIEF.md`
- `style:pm-kamstudiolabs-0b0824`
- `style:pm-ryzoft-4f85bd`

#### 7. قدرات قريبة في العائلة

- `GLOW-78` أضواء المدينة الليلية ثلاثية الأبعاد / 3D night practicals: sodium lamps, additive point sprites & bokeh (install)
- `GLOW-79` ارتعاش الفانوس والشمعة / Lantern & candle flicker (organic) (install)
- `GLOW-81` قمر مرسوم بهالة / Painted moon with halo (ready)
- `GLOW-82` انعكاس الضوء على الأرض المبللة والماء / Wet-floor & water reflections of light and titles (proven)

### `GLOW-81` — قمر مرسوم بهالة / Painted moon with halo

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قمر كامل: هالة بنفسجية واسعة، قرص كريمي مضاء من أعلى اليسار، فوهات ناعمة، وهالة داخلية دافئة. / A full moon: wide purple halo, cream-to-tan disc lit from upper left, soft crater blotches and a warm inner halo.

**متى:** حين تريد رسم قمر بدر بالكود بهالة بنفسجية وقرص كريمي وفوهات ناعمة لمشهد ليلي / when code-painting a full moon with a purple halo, cream disc and soft craters for a night scene

**كيف:** glow(ellipse r·2.4, '#4f3f86', 70, .55); fill(ellipse, rad(offset, r·1.55, ['#fffaf0', '#f7e6c2', '#dcb47e'])); crater ellipses #b99467 α .2–.3 blur 4–9; glow #f1d29a 26 .32. Uses only glow/fill (verified here).

**المعاملات:** radius 150 at (845, 232)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قمر · ليل · هالة · moon · halo · night · painter · بدر · قمر مكتمل · سماء ليلية · full moon · night sky

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-81` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-studio/scenes/dragon_girl.py:150`
- `kosif-studio/render.py:407`

#### 7. قدرات قريبة في العائلة

- `GLOW-79` ارتعاش الفانوس والشمعة / Lantern & candle flicker (organic) (install)
- `GLOW-80` شعاع منارة دوّار / Rotating lighthouse / beacon beam (install)
- `GLOW-82` انعكاس الضوء على الأرض المبللة والماء / Wet-floor & water reflections of light and titles (proven)
- `GLOW-83` حقل حراري وتلوين دوبلر / Thermal heat-ramp field & Doppler-beamed glow (ready)

### `GLOW-82` — انعكاس الضوء على الأرض المبللة والماء / Wet-floor & water reflections of light and titles

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الأرض المبللة تعكس اللافتة بشرائح مقلوبة متموجة وخفوت فرينل، والعناوين تطفو فوق انعكاس مكسور، وعمود ضوء ذهبي على النهر. / Wet ground mirrors the sign as rippled flipped strips with Fresnel fade; titles float over a broken reflection; a golden column of light lies on the river.

**متى:** حين تحتاج انعكاس لافتة أو عنوان على أرض مبللة أو ماء، أو عمود ضوء ذهبي على نهر / when a sign or title should reflect on a wet floor or water, or a golden light column should lie on a river

**كيف:** Neon proof: mirror around the wall/floor junction in 3 px strips with ripple, a sharp layer inside puddle masks (2 px blur + short streaks) and a 16 px half-res film on the rest of the asphalt, × Fresnel fade .9 (far) → .25 (near), rain-drop ripples in puddles, junction AO — rendered here. Titles: MG-057 vertically flipped copy + gradient mask + perspective skew (CSS scaleY(−1) + mask-image); MG-079 reflection distorted by a displacement map from the water texture (SVG feDisplacementMap + animated feTurbulence). Sunset sea: animated normal-map ripples (scale .02), spec power 200 toward the sun, fog .0015. Lit pavilion: thin warm-gold edge strokes #f6e2b0 (1–2 px), bloom 12–20 px ramping on over 2 s, long reflection column on the water. A dark far bank sells water.

**المعاملات:** strips 3 px; puddle blur 2 px, film 16 px @½; Fresnel .9→.25; MG-057 5 s, MG-079 7 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** انعكاس · أرض مبللة · ماء · reflection · wet floor · puddles · fresnel · water · river · مطر · برك ماء · انعكاس العنوان · rain reflection · mirror

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-82` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/index.html`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-cinematic-titles.md`
- `style:pm-demitiyageekzen-7770ad`

#### 7. قدرات قريبة في العائلة

- `GLOW-80` شعاع منارة دوّار / Rotating lighthouse / beacon beam (install)
- `GLOW-81` قمر مرسوم بهالة / Painted moon with halo (ready)
- `GLOW-83` حقل حراري وتلوين دوبلر / Thermal heat-ramp field & Doppler-beamed glow (ready)
- `GLOW-84` عناوين الضباب وشق الضوء وكشف الفخامة الهادئة / Fog-layer & light-slit titles (quiet premium) (documented)

### `GLOW-83` — حقل حراري وتلوين دوبلر / Thermal heat-ramp field & Doppler-beamed glow

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مظلل واحد: كتلة FBM مشوهة مرتين تُلوَّن بمنحدر حرارة من سبع درجات وتُلطَّخ بأثر إصبع؛ وقرص يضيء ويزرق من جهة الاقتراب. / One shader: a double domain-warped FBM blob mapped through a 7-stop heat ramp and smeared by a finger trail; and a disk brightened and blue-shifted on its approaching side.

**متى:** حين يطلب المستخدم مظهرًا حراريًا أو خريطة حرارة متحركة، أو قرصًا يسطع ويزرق من جهة الاقتراب / when the user wants an animated heat-map look, or a disk that brightens and blue-shifts on its approaching side

**كيف:** Heat stops at 0/.12/.30/.45/.60/.78/1 via smoothstep, heat capped .75; 24 trail points (life 1.6 s, smudge 9, radius .17, follow .3), melt cycle 6 s, blob .37, press ripple .18 / bloom .55 / .9 s. For video, script the 'finger' as keyframed points. Doppler (seen): intensity ∝ δ^3–4 — brighten/blue-shift the approaching side, dim/red-shift the receding one, then heavy bloom (20–40 px, threshold .7). Ember/fire means heat or overload, never human tragedy.

**المعاملات:** 7 stops; 24 pts / 1.6 s / smudge 9; Doppler δ^3–4, bloom 20–40 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حراري · خريطة حرارة · دوبلر · thermal · heat map · fbm · doppler · black hole · shader · ثقب أسود · تدرج حراري · تلطيخ · heat ramp · domain warp

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-83` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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
- `style:pm-rebutonepress-810f78`

#### 7. قدرات قريبة في العائلة

- `GLOW-81` قمر مرسوم بهالة / Painted moon with halo (ready)
- `GLOW-82` انعكاس الضوء على الأرض المبللة والماء / Wet-floor & water reflections of light and titles (proven)
- `GLOW-84` عناوين الضباب وشق الضوء وكشف الفخامة الهادئة / Fog-layer & light-slit titles (quiet premium) (documented)
- `GLOW-P01` كتابة مسار نيون نقطية بطبقتي توهج في Pillow / Raster neon path-write in Pillow (blurred halo + hot core) (documented)

### `GLOW-84` — عناوين الضباب وشق الضوء وكشف الفخامة الهادئة / Fog-layer & light-slit titles (quiet premium)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** عنوان ثابت بين طبقتي ضباب تتحركان بسرعتين، أو خط ضوء رفيع يتسع ليكشف عنوان فصل ثم يخفت. / A title holds between two fog layers moving at different speeds, or a thin line of light widens to reveal a chapter title, then dims.

**متى:** عند كشف عنوان فصل وثائقي بهدوء فخم بين طبقتي ضباب أو بخط ضوء رفيع يتسع / for a quiet premium reveal of a documentary chapter title between fog layers or via a widening light slit

**كيف:** MG-071: 0–2 s atmosphere, 2–4 s appear, 4–8 s read; screen/alpha layering with graded fog depth; haze must never block reading (local: procedural canvas-noise fog with mix-blend-mode screen). MG-072: 0–1 s line, 1–3 s widen, 3–6 s hold; horizontal moving mask + limited glow; avoid fast flashes and white that eats the letters. S02 Quiet premium: measured contrast, restrained shadows, a little sheen, slow 1.00→1.04 drifts, few transitions — gloss cannot rescue a weak source.

**المعاملات:** MG-071 8 s; MG-072 6 s; drift 1.00→1.04

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ضباب · شق ضوء · عنوان فصل · fog · light slit · chapter title · premium · documentary · عنوان وثائقي · كشف العنوان · شبورة · title reveal · haze

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-84` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-cinematic-titles.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-82` انعكاس الضوء على الأرض المبللة والماء / Wet-floor & water reflections of light and titles (proven)
- `GLOW-83` حقل حراري وتلوين دوبلر / Thermal heat-ramp field & Doppler-beamed glow (ready)
- `GLOW-P01` كتابة مسار نيون نقطية بطبقتي توهج في Pillow / Raster neon path-write in Pillow (blurred halo + hot core) (documented)
- `GLOW-X01` مرور العدسة «مصوَّر لا مرسوم» / Photographed lens pass (barrel, fringes, bloom, vignette, grain) (documented)

### `GLOW-P01` — كتابة مسار نيون نقطية بطبقتي توهج في Pillow / Raster neon path-write in Pillow (blurred halo + hot core)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner package (own work) |

**ما هي:** خط نيون يُرسم تدريجيًا بلا متصفح: هالة مموهة مدموجة ثم قلب ساطع ونقطة رأس بيضاء. / A neon line writes on without a browser: a blurred halo blended in, then a bright core and a white tip dot.

**متى:** حين تحتاج خط نيون يُكتب تدريجيًا بلا متصفح بهالة مموهة وقلب ساطع عبر Pillow / when a neon line must write on without a browser, rendered with Pillow as a blurred halo plus hot core

**كيف:** Path = 321 points of a decaying sine (amplitude 95 px, 3 half-waves, e^(−i/600)). Visible count = len·min(1, t/2.6). Halo: draw the partial path 17 px wide in (0,150,195) on a black layer, GaussianBlur(21), Image.blend(base, halo, 0.44). Core: 6 px (31,200,245) then 2 px (204,254,255), joint="curve"; tip = 10 px white ellipse. Dark ground (8,11,23) with faint 48 px scan lines; Arabic caption with direction="rtl". frame(t) is pure — re-rendering t=2.5 gives identical bytes. Re-ran here: 4 s 480×854 24 fps MP4 + still PNG; frame looked clean. Raster cousin of GLOW-03 (SVG 4-stroke tube) for Pillow/ffmpeg-only pipelines. Status note: the code is owner material that is not vendored in this skill; the numbers above are from one run on the owner's copy on 2026-10-16 and cannot be re-run from here, so this is 📄 documented, not ✅.

**المعاملات:** halo 17 px · blur 21 · blend 0.44 · core 6 px + 2 px · write-on 2.6 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** neon · pillow · glow · path draw · نيون · توهج · raster · خط متوهج · رسم تدريجي · بدون متصفح · write-on · headless

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-P01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/tools/render_neon.py`
- `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/examples/Neon_Path_Draw.mp4`
- `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/examples/Neon_Path_Draw.png`

#### 7. قدرات قريبة في العائلة

- `GLOW-83` حقل حراري وتلوين دوبلر / Thermal heat-ramp field & Doppler-beamed glow (ready)
- `GLOW-84` عناوين الضباب وشق الضوء وكشف الفخامة الهادئة / Fog-layer & light-slit titles (quiet premium) (documented)
- `GLOW-X01` مرور العدسة «مصوَّر لا مرسوم» / Photographed lens pass (barrel, fringes, bloom, vignette, grain) (documented)
- `GLOW-X02` نواة توهج ملوّنة وحدود الوميض / Tinted bloom cores and flash limits (documented)

### `GLOW-X01` — مرور العدسة «مصوَّر لا مرسوم» / Photographed lens pass (barrel, fringes, bloom, vignette, grain)

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | owner (no LICENSE file) |

**ما هي:** مرور أخير على الإطارات يضيف ما تفعله عدسة حقيقية: انتفاخ برميلي، حواف لونية شعاعية، توهج للمناطق المضيئة على ثلاث درجات، تعتيم أطراف، وحبيبات خفيفة. — A final pass over rendered frames adding what a real lens does: barrel bulge, radial colour fringes, three-scale bloom on highlights, vignette and fine grain.

**متى:** فيلم متجهي نظيف يبدو رخيصًا أو مسطحًا — a clean vector film that looks cheap or flat.

**كيف:** Owner script lens.py (numpy + Pillow; not vendored): `python3 lens.py frames_dir out_dir --fps 30 [--k .04 --ca 1.5 --bloom .35 --thr .72 --vig .35 --grain .02] [--sched sched.json]`. Bloom from highlights above thr at three radii (h·0.006 / 0.02 / 0.06, weights 0.7 / 1 / 0.45, screen blend, auto-off on bright frames); barrel k with R/B sampled slightly apart (radial fringes); vignette smoothstep(0.35 → 1.25 r); luma grain seeded per frame, strongest in mid-tones. Per-scene overrides via --sched. Ran here (V7) on 960×540 test frames: corner −27 % (65.3 → 47.8), a halo +6.1 next to a white disc, grain std 0 → 4.1 and re-seeded every frame, ±1 px R/B fringe near the edge; 1.2 s for 3 frames. WebGL equivalents that worked: CA 0.0032·r (0.012 was far too much), CRT barrel 0.2, paper 0.035–0.05, scanlines 0.32, vignette 0.3–0.7. Status note: the code is owner material that is not vendored in this skill; the numbers above are from one run on the owner's copy on 2026-10-16 and cannot be re-run from here, so this is 📄 documented, not ✅.

**المعاملات:** k .04; CA 1.5 px; bloom .35 @ thr .72; vignette .35; grain .02

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** lens · bloom · vignette · chromatic aberration · grain · عدسة · توهج · تعتيم الأطراف

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:numpy` ← python3 -c "import numpy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-X01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `kosif-tool/.claude/skills/kosif-superpowers/references/external-skills.md`
- `owner-upload:motion-saas_skill/higgsfield-motion-saas/scripts/code/lens.py`

#### 7. قدرات قريبة في العائلة

- `GLOW-84` عناوين الضباب وشق الضوء وكشف الفخامة الهادئة / Fog-layer & light-slit titles (quiet premium) (documented)
- `GLOW-P01` كتابة مسار نيون نقطية بطبقتي توهج في Pillow / Raster neon path-write in Pillow (blurred halo + hot core) (documented)
- `GLOW-X02` نواة توهج ملوّنة وحدود الوميض / Tinted bloom cores and flash limits (documented)

### `GLOW-X02` — نواة توهج ملوّنة وحدود الوميض / Tinted bloom cores and flash limits

| الحقل | القيمة |
|---|---|
| العائلة | `light-glow-bloom` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/light-glow-bloom.md)) |
| المجموعة | الثري دي والمحاكاة والرندر (`3d`) |
| نوع المخرج (A25، A27) | ثلاثي الأبعاد (`model3d`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `archive` |
| الرخصة | owner (no LICENSE file) |

**ما هي:** التوهج الأبيض النقي يبدو رخيصًا؛ لوّن نواته، وأطلق الوميض من نقطة الفعل، ولا تتجاوز حدود الأمان. — Pure white bloom reads cheap: tint its core, bloom flashes from the action point, and stay inside safety limits.

**متى:** ضربات وكشف شعار وتوهجات نيون — hits, logo reveals and neon glows.

**كيف:** Tint the bloom core toward the light's colour; a flash blooms from the action point; at most one big flash per second; accessibility: ≤ 3 flashes per second and a full white frame ≤ 2 frames.

**المعاملات:** ≤ 1 big flash/s; ≤ 3 flashes/s; white ≤ 2 frames

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** bloom · flash · safety · tint · وميض · توهج · أمان

#### 1. الاستقبال (A25)

- صيغة التسليم: افتراض مكتوب ← GLB للمجسم أو MP4 للرندر
- العتاد وزمن الرندر: افتراض مكتوب ← CPU بلا GPU، بمعاينة منخفضة أولًا
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `model3d`، والمنفّذ `method:GLOW-X02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `blender-cinema`.
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

- `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/client-taste.md`
- `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`

#### 7. قدرات قريبة في العائلة

- `GLOW-P01` كتابة مسار نيون نقطية بطبقتي توهج في Pillow / Raster neon path-write in Pillow (blurred halo + hot core) (documented)
- `GLOW-X01` مرور العدسة «مصوَّر لا مرسوم» / Photographed lens pass (barrel, fringes, bloom, vignette, grain) (documented)

