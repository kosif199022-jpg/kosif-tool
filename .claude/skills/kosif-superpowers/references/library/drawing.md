# الرسم والأشكال والتصميم — Drawing & visual composition (`drawing`)

> مكتبة بروتوكول USIP v5.6، مولّدة بـ `scripts/smart_capabilities.py library` من `data/powers/*.json` و`data/tools.json`؛ لا تُحرَّر يدويًا. الدليل: [A28 اختيار القدرات](../protocol/A28-capability-routing.md) · [الفهرس](INDEX.md) · [النواة](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

## الفهرس / contents

- [متى تستخدم هذه المجموعة / when](#متى-تستخدم-هذه-المجموعة--when)
- [الحالة بالأرقام / status](#الحالة-بالأرقام--status)
- [الأدوات القابلة للتشغيل / runnable tools](#الأدوات-القابلة-للتشغيل--runnable-tools)
- [العائلات / families](#العائلات--families)
- [كل القدرات / every power](#كل-القدرات--every-power)

## متى تستخدم هذه المجموعة / when

كلمات التوجيه: draw line stroke path shape circle polygon vector svg logo illustration diagram رسم خطوط أشكال دائرة مضلع شعار مخطط

خط العمل المقترح (هدف تصميم، لم يُختبر كوحدة واحدة): الخطوط والمسارات → الأشكال والهندسة → الدمج في مشهد/لوحة → التصدير والتحقق

العضوية في المجموعة تصنيف للتوجيه، لا دليل على أن القدرات تعمل معًا: اربطها بخط عمل مختبر فقط.

## الحالة بالأرقام / status

| الحالة | العدد | المعنى |
|---|---:|---|
| `proven` | 53 | ✅ proven: a proof exists in the catalog; still check its requirements here before calling it ready |
| `ready` | 55 | 🟢 ready: runnable without setup according to the catalog |
| `documented` | 89 | 📄 documented: a described method; needs building or wiring before it runs |
| `seen` | 66 | 👁 seen: observed in a reference or demo, not executed here |
| `install` | 31 | 📦 install: needs a package, binary or model first |
| `key` | 4 | 🔑 key: needs an account, key or paid service (ask before any spend) |
| `idea` | 8 | 💡 idea: not built |
| **المجموع** | **306** | |

## الأدوات القابلة للتشغيل / runnable tools

| الأداة | ما تفعله | ابدأ بـ | الدليل |
|---|---|---|---|
| `app-studio-paint` | حزمة الرسم في استوديو التطبيقات | `python3 -c "import sys; sys.path.insert(0,'scripts'); import app_studio; print(app_studio.PAINT_BATCH['effects'])"` | tested-here |
| `atlas-render` | رندر أفلام الشرح: ستوريبورد وفحص حتمية وMP4 حقيقي بصوت مُركّب | `python3 scripts/atlas_render.py check` | tested-here |
| `brand-tokens` | رموز الهوية: ألوان الشعار ورموز بثلاث طبقات ومصفوفة تباين WCAG | `echo '<svg xmlns="http://www.w3.org/2000/svg"><rect fill="#1d4ed8"/><circle fill="#1D4ED8"/><path stroke="#f59e0b"/><text fill="#475569">K</text></svg>' \| python3 scripts/brand_tokens.py palette -` | tested-here |
| `code-drawing-master` | رسم الشخصيات والمشاهد بالكود | `python3 scripts/code_drawing_master.py --cast human+cat --expression happy --location street --action walk --out ./story.json --html ./story.html` | tested-here |
| `color-media` | محرك الخامات الملوّنة: ألوان خشبية وفرشاة زيت وألوان مائية لأي صورة | `python3 scripts/color_media.py draw --photo in.png --out out/x --medium oil` | tested-here |
| `creative-paint` | الرسم الإبداعي بالطبقات | `python3 scripts/creative_paint.py doctor` | tested-here |
| `creative-principles` | دراسة الرسم التدريجي والظل الأصلي | `python3 scripts/creative_principles.py construct --input original-shapes.json --out-prefix out/stage` | tested-elsewhere |
| `creative-reasoning-bridge` | جسر الصوت إلى لوحة القصة | `python3 scripts/creative_reasoning_bridge.py ./cues.json --style auto --out ./out/scene.json --report ./out/decision.json` | tested-here |
| `diagram-layout` | تخطيط المخططات: فحص الرسم البياني وتخطيط طبقي حتمي وSVG جاهز للعربية | `python3 scripts/diagram_layout.py lint /tmp/graph.json --max-label 24 --max-nodes 9` | tested-here |
| `drawing-academy` | أكاديمية الرسم والدروس المبنية على مصادر | `python3 scripts/drawing_academy.py index` | tested-elsewhere |
| `drawing-council` | مجلس خبراء الرسم: أحد عشر خبيرًا من بطاقات الكتب الـ48 يراجعون الصورة قبل إرسالها | `python3 scripts/drawing_council.py roster --markdown` | tested-here |
| `drawing-methods` | أطلس مناهج كتب الرسم مع رسم بنائي بالطبقات | `python3 scripts/drawing_methods.py find "ارسم وش شخصية بتضحك"` | tested-here |
| `drawing-visual-qa` | مدرب الرسم من فصول الكتب والتشخيص البصري المستقل | `python3 scripts/drawing_visual_qa.py curriculum "ارسم شخصية كرتونية بمنظور وإضاءة" --out out/lessons.json` | tested-here |
| `motion-director` | مُصرِّف حركة SVG المتزامنة مع الصوت | `python3 scripts/motion_director.py doctor` | tested-here |
| `motion-engine-js` | محرك حركة SVG | `python3 scripts/motion_director.py compile ./scene.json --out ./out/film.html` | tested-here |
| `motion-kit-bridge` | جسر توقيتات Motion Starter Kit | `python3 scripts/motion_kit_bridge.py styles` | tested-here |
| `motion-runtime` | إنشاء فيلم سبورة مرسوم وتصييره | `python3 scripts/motion_runtime.py doctor` | tested-here |
| `motion-toolkit` | مكتبة رياضيات الحركة | `node --input-type=module -e "import {ease, timeCode} from './resources/motion-runtime/motion_toolkit.mjs'; console.log(ease(0.5,'cubic'), timeCode(2.5,30))"` | tested-here |
| `native-3d` | رندر ثلاثي الأبعاد مستقل عن Blender | `python3 scripts/native_3d.py doctor` | tested-here |
| `native-glb` | مُصدِّر GLB مستقل عن Blender | `python3 scripts/native_glb.py --scene templates/blender-demo.json --output ./out/scene.glb` | tested-here |
| `perspective-color-lab` | منظور هندسي ومقاييس التباين اللوني | `python3 scripts/perspective_color_lab.py perspective --input scene.json --out out/scene.svg` | tested-elsewhere |
| `portrait-pipeline` | نسخة مرسومة أو ملوّنة باليد لأي صورة أو مشهد متخيَّل: رصاص، فحم، حبر، ألوان خشبية، فرشاة زيت أو ألوان مائية | `python3 scripts/portrait_pipeline.py draw --photo photo.png --out out/portrait --models <dir with face_landmarker.task and selfie_multiclass.tflite>` | tested-here |
| `smart-draw` | الرسم الذكي ومساعد الأشكال | `python3 scripts/smart_draw.py doctor` | tested-here |
| `style-atlas-bridge` | أطلس الأساليب الكامل (86 طريقة): بحث وتوليف وموجز إنتاج وهيكل مشروع شرح | `python3 scripts/style_atlas_bridge.py families` | tested-here |
| `unified-draw` | الرسم الموحد: خطوط وأشكال وطبقات وتصدير | `python3 scripts/unified_draw.py doctor` | tested-here |
| `unified-media` | محرر الوسائط الموحد: صور ورسم وتحريك وفيديو | `python3 scripts/unified_media.py doctor` | tested-here |

الأوامر نسبية إلى مجلد المهارة (أو جذر المستودع لأدوات `tools/`)؛ `python3 scripts/hub.py tool <id>` يعطي كل الأوامر والمتطلبات والحدود.

## العائلات / families

| العائلة | القدرات | الفصل |
|---|---:|---|
| `brand-logo-identity` | 43 | [brand-logo-identity.md](../powers/brand-logo-identity.md) |
| `diagrams-explainers-code` | 69 | [diagrams-explainers-code.md](../powers/diagrams-explainers-code.md) |
| `hand-drawn-draw-on` | 65 | [hand-drawn-draw-on.md](../powers/hand-drawn-draw-on.md) |
| `pixel-retro-stylized` | 32 | [pixel-retro-stylized.md](../powers/pixel-retro-stylized.md) |
| `shapes-morph-geometry` | 97 | [shapes-morph-geometry.md](../powers/shapes-morph-geometry.md) |

## كل القدرات / every power

مرتبة بالحالة ثم العائلة ثم المعرّف. `hub.py` و`skill_intelligence.py deep <ID>` يعطيان بطاقة القدرة كاملة بدليلها.

| المعرّف | الاسم | English | الحالة | المتطلبات |
|---|---|---|---|---|
| `BRAND-08` | من الموقع إلى مادة الفيلم | Site → film material (palette, fonts, CTAs) | proven | chromium |
| `BRAND-13` | تحويل الشعار النقطي إلى متجه بألوانه | Raster logo → true-colour vector layers | proven | python3 |
| `BRAND-14` | مجموعات الأيقونات وأيقونات التطبيق | Icon families, app icons & favicon sets | proven | python3, chromium |
| `BRAND-15` | شعارات KOSIF المبنية بالكود | Owner marks built in code (SQC, K marks, ram, cloud) | proven |  |
| `BRAND-17` | كشف فاخر بالزجاج والذهب | Luxury glass-and-gold reveal (proof film) | proven |  |
| `BRAND-18` | رسم الخط ثم التعبئة | Stroke draw-on then fill | proven | python3 |
| `BRAND-33` | مكتبة بطاقات الختام للثيمات (17) | Per-theme end-card library (17) + user-owned wordmark slot | proven |  |
| `BRAND-37` | قوالب الموشن العربية الثمانية | Eight Arabic motion templates (logo-reveal, end-card …) | proven | python3, fonts:arabic |
| `EXPL-50` | التوأم الإنشائي: حلّال الجملونات | Structural twin truss solver | proven | python3 |
| `EXPL-54` | دورة الماء التعليمية المسطحة | Flat educational water cycle | proven | fonts:arabic |
| `DRAW-01` | رسم المسار بإزاحة الشرطة | SVG stroke draw-on | proven |  |
| `DRAW-03` | سرعة القلم والرفع | Pen speed & lifts | proven |  |
| `DRAW-04` | ترتيب الرسم البشري ووصفة «ارسم وسمِّ» | Human draw order & draw-and-label | proven |  |
| `DRAW-06` | رأس يتبع الخط: يد، ماركر، طباشيرة | Pen-tip followers: hand, marker, chalk | proven | npm:remotion |
| `DRAW-07` | رأس متوهج يجرّ الخط | Glowing head draw | proven |  |
| `DRAW-14` | قوالب موشن بالقلم | Pen-drawn motion templates | proven | python3 |
| `DRAW-15` | كتابة بقناع فرشاة من اليمين | Brush-mask write-on (RTL) | proven | fonts:arabic |
| `DRAW-19` | دائرة يدوية مرتعشة | Hand-drawn circle emphasis | proven |  |
| `DRAW-28` | خطوط بضغط على طريقة perfect-freehand | Pressure strokes & clipped hatching | proven | node |
| `DRAW-33` | سبورة بيضاء | Whiteboard | proven | python3 |
| `DRAW-48` | ترتيب الرسام في الكشف | Painter reveal orders | proven |  |
| `DRAW-49` | فيلم الرسم | Drawing film (picture forming as MP4) | proven | python3 |
| `DRAW-50` | الرسم بترتيب الكود نفسه | PIL command recorder | proven | pip:pillow |
| `DRAW-51` | الرسم المطابق تمامًا | Exact-match painting | proven |  |
| `DRAW-52` | صورة إلى برنامج بايثون | Image to standalone Pillow program | proven | pip:pillow |
| `DRAW-53` | استيراد SVG والتحويل إلى متجهات | SVG import & vectorize to draw steps | proven | python3 |
| `DRAW-54` | محوّل مسارات SVG إلى نقاط | SVG path sampler | proven | python3 |
| `RETRO-01` | مشهد بكسل في ملف HTML واحد | Self-contained pixel cutscene (one HTML) | proven | ffmpeg, node, chromium |
| `RETRO-02` | الإضاءة والتلاشي بدثر Bayer | Bayer-dither fades & palette-stepped light | proven |  |
| `RETRO-06` | حركة على شبكة صحيحة والرسم على الاثنين | Integer-grid motion & animating on twos | proven |  |
| `RETRO-10` | هافتون وشاشات CMYK | Halftone & CMYK screens | proven | pip:pillow, npm:hyperframes |
| `RETRO-11` | ريزوغراف وانزياح الحبر | Risograph misregistration & two-ink print | proven | ffmpeg, pip:pillow |
| `RETRO-16` | CRT وخطوط المسح وVHS | CRT, scanlines & VHS damage | proven | ffmpeg, npm:hyperframes |
| `RETRO-22` | تحويل المشهد إلى ASCII | ASCII render pass | proven | npm:hyperframes |
| `RETRO-24` | الدثر المرتب والدثر بالانتشار | Ordered & error-diffusion dither passes | proven | ffmpeg, node |
| `RETRO-28` | كلمة غليتش RGB على النوتات | RGB-split glitch word on the beat | proven | ffmpeg, npm:hyperframes |
| `RETRO-29` | ثيمات التايب الحركي المقفلة (J، K، N، Q) | Locked kinetic themes: Brutalist Acid · Retro 70s · Paper Craft · Y2K Chrome | proven |  |
| `SHAPE-01` | تحويل المسار بإعادة العينات | Seek-safe path morph (MOTION.morphPath) | proven | npm:gsap |
| `SHAPE-03` | فائق الإهليلج بحلقات صدى | Superellipse morph with echo rings | proven |  |
| `SHAPE-04` | تحويل بدالة قطبية | Polar-function shape morph | proven |  |
| `SHAPE-27` | فلتر اللزوجة | SVG goo / metaball filter | proven |  |
| `SHAPE-32` | نحت بحقول المسافة إلى مجسم مغلق | SDF sculpting to a watertight mesh | proven |  |
| `SHAPE-33` | دمج ونحت وتقاطع ناعم | Smooth CSG (add / sub / and) | proven |  |
| `SHAPE-41` | محلل لغة مسارات SVG كاملة | Full SVG path parser (Studio) | proven |  |
| `SHAPE-42` | أشكال مركبة بثقوب | Even-odd compound shapes & holes | proven | pip:pillow |
| `SHAPE-43` | عدة الأشكال الأساسية ولغة المشهد | Basic shape kit & Step scene language | proven |  |
| `SHAPE-52` | شبكة بلاطات باوهاوس | Bauhaus tile grid (glyph swap on a distance wave) | proven |  |
| `SHAPE-53` | بلاطات تروشيه بموجة تلوين | Truchet tiles with a recolour wave | proven |  |
| `SHAPE-56` | زهرة النقاط الذهبية | Phyllotaxis dot flower (137.5°) | proven |  |
| `SHAPE-63` | حلقات متحدة المركز بفجوات | Rotating gapped concentric rings | proven |  |
| `SHAPE-66` | انفجار خطوط شعاعي | Radial line burst | proven |  |
| `SHAPE-67` | حلقة صدمة أرضية ونبض قلب | Shockwave ring & heartbeat ripple | proven |  |
| `SHAPE-68` | أشعة شمسية دوارة | Rotating sunburst ground | proven |  |
| `BRAND-03` | ورقة نظام العلامة للفيديو | Video brand-system sheet | ready | python3 |
| `BRAND-05` | أنظمة تصميم جاهزة للكاميرا (frame.md) | Video-first design presets (frame.md) | ready | chromium, npm:hyperframes |
| `BRAND-12` | قواعد بناء الشعار SVG | SVG logo construction rules & logo suite | ready | node, pip:fonttools |
| `BRAND-22` | انكماش التباعد إلى الشعار (لاتيني فقط) | Tracking-collapse lockup (Latin only) | ready |  |
| `BRAND-35` | إطار البث الثابت وتوقيع الزاوية | Persistent broadcast chrome & corner signature | ready |  |
| `BRAND-36` | غمر لون العلامة | Brand-colour flood end frame | ready | fonts:arabic |
| `BRAND-42` | ملصق إعلان منتج عربي متجهي | Arabic vector product-ad poster (whole lamb) | ready | pip:pillow |
| `BRAND-43` | نظام «ورق الدفتر» ولوك المانيفست | Ledger-paper design system & manifest title look | ready | pip:faster-whisper |
| `EXPL-15` | خريطة الكيان في المنتصف | Entity node map with flow edges | ready |  |
| `EXPL-18` | خطوط تدفق متحركة | Marching-dash flow edges | ready |  |
| `EXPL-25` | دورة ورمز ينتقل | Cycle diagram, travelling token & loop arrow | ready |  |
| `EXPL-26` | شريط المراحل ومؤشر الخطوات | Stage tracker pills & steppers | ready |  |
| `EXPL-29` | تسميات بخطوط قائدة | Leader-line callouts (2D & 3D) | ready |  |
| `EXPL-51` | فيلم التوأم الإنشائي | Structural twin film (truss on a character) | ready | python3 |
| `EXPL-52` | منظر تخطيطي ومفكك | Schematic, wireframe & exploded view | ready |  |
| `EXPL-53` | شرح علمي ثلاثي الأبعاد بأربع مراحل | Four-stage 3D science explainer | ready |  |
| `EXPL-58` | فئات المخططات والكود في بصمة | Basma diagram & code film categories | ready |  |
| `EXPL-59` | رسومات استعارية لكل جملة | Metaphor graphic per spoken claim | ready |  |
| `EXPL-62` | أسلوب الرسومات التقنية | Tech blueprint style | ready | python3 |
| `DRAW-02` | قلم مكتبة الحركة برأس يهبط | Kit drawPath with landing head & flowDash | ready |  |
| `DRAW-05` | رابط مخطط برأس سهم | Diagram edge draw-on with arrowhead | ready | npm:remotion, key:unspecified |
| `DRAW-10` | نهر يمتلئ ثم يجري | River fill then flow | ready |  |
| `DRAW-11` | المحراب بقلم ذهبي | Gold-pen arch draw-on | ready |  |
| `DRAW-12` | رسوم خطية صغيرة فوق الفيديو | Line micro-graphics over footage | ready |  |
| `DRAW-13` | أيقونات المعنى المرسومة | Meaning icons drawn on | ready |  |
| `DRAW-24` | خط الرحلة من اليمين | Journey line draw-on (RTL) | ready |  |
| `DRAW-29` | حبر بصمة بضغط وتظليل | Basma INK pressure strokes & hatching | ready |  |
| `DRAW-34` | سبورة سينمائية | Whiteboard cinematic | ready | python3 |
| `DRAW-35` | سبورة الطباشير | Chalkboard | ready | python3, fonts:arabic |
| `DRAW-36` | قصص الدودل | Doodle stories | ready | python3, fonts:arabic |
| `DRAW-37` | قلم البلوتر | Plotter pen | ready | python3 |
| `DRAW-38` | إطار بإطار على اثنين | Frame-by-frame on twos | ready | python3 |
| `DRAW-47` | من مخطط سلكي إلى مجسم | Wireframe draw → solid formation | ready | npm:three |
| `DRAW-58` | إعادة رسم مخرجات مولدة كمتجهات | Generated raster → hand vector recreation | ready |  |
| `RETRO-03` | عفريتات مقفلة اللوحة ومولّد الوضعيات | Palette-locked sprites & procedural pose generator | ready | pip:pillow |
| `RETRO-13` | ملصق مسطّح من صورة (k ألوان) | Flat-paint poster vectorisation (k colours) | ready | pip:opencv |
| `RETRO-26` | تقطيع رقمي قصير للعناصر | DOM glitch stutter (motion-kit) | ready |  |
| `RETRO-27` | تمريرة غليتش ثلاثية الأبعاد | Analysis-keyed 3D glitch pass | ready | npm:three |
| `SHAPE-17` | سلسلة: نقطة → زر → شريط تقدم | Morph chain: dot → button → progress bar → full stop | ready |  |
| `SHAPE-23` | حلقة → قزحية → غمر لوني | Ring → iris → colour flood | ready |  |
| `SHAPE-34` | استعلام الحقل لتثبيت العناصر | Field queries for placement | ready |  |
| `SHAPE-35` | حقل كتل وبقعة زاوية | Drifting blob field & corner blob | ready |  |
| `SHAPE-44` | منحنيات كاتمول-روم | Catmull-Rom smooth curves | ready |  |
| `SHAPE-45` | أنبوب بنصف قطر متغير | Variable-radius tube (limbs, tails, flames, hair) | ready |  |
| `SHAPE-46` | سلاسل جبال بالإزاحة | Midpoint-displacement mountain ridges | ready |  |
| `SHAPE-50` | خيوط موجية وأشرطة متلوية | Sine strands & ribbon loops | ready |  |
| `SHAPE-51` | خطان قطريان فقط | Exactly two drifting diagonal lines | ready | npm:three |
| `SHAPE-64` | عنقود أقواس مدارية ونواة نابضة | Orbiting arc cluster + pulsing donut core | ready |  |
| `SHAPE-65` | حلقات مدارية إهليلجية | Orbital ellipse rings & accents | ready |  |
| `SHAPE-73` | الزخرفة الثمانية من الكود | Islamic eight-point rosette builder | ready |  |
| `SHAPE-74` | وردة الفواصل الموسيقية | Interlude rosette (verse template) | ready | python3 |
| `SHAPE-75` | فوانيس ومسجد ونوافذ | Swaying lanterns & mosque silhouette | ready |  |
| `SHAPE-76` | غيمة من دوائر تكبر وتعتم | Circle-cluster cloud that grows and darkens | ready |  |
| `SHAPE-77` | مكتبة 16 أيقونة متجهة | 16-icon vector hero library | ready |  |
| `SHAPE-91` | انضغاط وتمدد بحفظ المساحة | Area-preserving squash & stretch | ready |  |
| `BRAND-01` | بريف الشعار: الشيء الواحد | Logo brief: the ONE THING | documented |  |
| `BRAND-02` | مقابلة العميل بلا هوية | Identity interview for no-brand clients | documented | npm:hyperframes, fonts:arabic |
| `BRAND-04` | رموز بثلاث طبقات ومصفوفة العلامات | Three-tier tokens & multi-brand theming | documented | npm:gsap, npm:remotion |
| `BRAND-06` | كتاب العلامة وصوتها | Brand book anatomy & voice | documented | npm:axe |
| `BRAND-07` | بوابة ترخيص الخطوط والملكية | Font-licence & IP gate | documented | fonts:arabic |
| `BRAND-19` | شعار يتجمع من أجزائه | Assembled mark (blocks · dots · tiles · particles) | documented |  |
| `BRAND-20` | كشوف القناع: ظل، ضباب، ختم، فراغ سالب | Mask reveals: shadow pass, fog, ink stamp, negative space | documented |  |
| `BRAND-38` | مونتاج شبكة العلامة | Brand grid montage | documented | imagemagick |
| `EXPL-01` | قواعد تركيب مخطط الشرح | Explainer diagram composition | documented |  |
| `EXPL-02` | قواعد العقد والروابط | Node & edge grammar | documented | key:unspecified |
| `EXPL-03` | اختيار نوع المخطط والتخطيط | Diagram type & layout chooser | documented | npm:mermaid |
| `EXPL-04` | ترتيب البناء السببي وحالات العقد | Causal build order & node states | documented |  |
| `EXPL-05` | عكس المخطط للعربية | Mirrored RTL diagrams | documented |  |
| `EXPL-06` | ألوان دلالية للأدوار | Semantic role colours | documented | npm:mermaid |
| `EXPL-07` | إطار الشرح الأحادي | Learning-mono explainer frame | documented |  |
| `EXPL-08` | حدود الأيقونات المختصرة | Closure limits for minimal icons | documented |  |
| `EXPL-10` | مخططات SVG برمجية بالملليمتر | Programmatic SVG schematics | documented | pip:fonttools |
| `EXPL-12` | مخططات D2 | D2 declarative diagrams | documented | npm:mermaid |
| `EXPL-16` | عملية من ثلاث خطوات | Three-step process recipe | documented |  |
| `EXPL-17` | نبضة بيانات على الرابط | Data pulse along edges | documented |  |
| `EXPL-22` | التكبير على مكوّن وقبل/بعد | Zoom into component & before/after diagram | documented | ffmpeg |
| `EXPL-23` | الخط الزمني برأس تشغيل | Timeline with playhead | documented |  |
| `EXPL-27` | خطأ ثم تصحيح | Mistake then correction | documented |  |
| `EXPL-28` | مقارنة سرعة عادلة | Fair speed comparison | documented |  |
| `EXPL-32` | طباعة الكود على الشاشة | On-screen code typography | documented |  |
| `EXPL-34` | جلسة الطرفية | Terminal session scene | documented |  |
| `EXPL-35` | إبراز السطر والتمرير والخطأ | Line highlight, scroll & error sweep | documented |  |
| `EXPL-36` | كشف الفرق | Diff reveal | documented |  |
| `EXPL-37` | نافذة كود مشروحة | Annotated code-window figure | documented |  |
| `EXPL-42` | حرّك ما يفعله الكود | Mechanism beat: animate behaviour, not code | documented | npm:gsap, claude:tools |
| `EXPL-55` | قواعد الدقة والوضوح للأطفال | Science accuracy & causal-step rules | documented |  |
| `EXPL-56` | نظام بطاقات الفيديو الشارح | Explainer card system | documented | node, chromium |
| `EXPL-57` | الوثيقة المصدر وقلم التظليل | Source document & article excerpt overlay | documented |  |
| `EXPL-63` | لوحات ستوري بورد SVG مصغرة | SVG thumbnail storyboards | documented |  |
| `EXPL-G01` | قواعد مشهد الشرح الرياضي | Explainer scene grammar | documented |  |
| `EXPL-G02` | مخطط بنية سحابية بالكود ثم كشفه | Architecture diagram as code, revealed by cluster | documented |  |
| `EXPL-U01` | قائمة الأساليب الخمسة للموشن بالكود | Five code-rendered motion-graphics styles menu | documented |  |
| `EXPL-U02` | لقطة التحليل المجمّدة | Frozen analysis beat overlay | documented |  |
| `DRAW-08` | كشف متعدد الأجزاء بالطول التراكمي | Cumulative-length multi-segment reveal | documented |  |
| `DRAW-17` | ترجمة بخط اليد تُكتب | Handwritten typewriter caption | documented |  |
| `DRAW-18` | أنماط قلم التحديد | Marker emphasis modes | documented |  |
| `DRAW-25` | عدم الكمال المقصود | Deliberate imperfection | documented |  |
| `DRAW-26` | غليان الخط | Line boil | documented | npm:hyperframes |
| `DRAW-30` | محرك فرشاة الحبر الحتمي | Deterministic ink-brush engine | documented | chromium |
| `DRAW-31` | ملمس الرصاص والطباشير بالمرشحات | Pencil & chalk texture filters | documented |  |
| `DRAW-39` | رسومات الماركر للقصص | Marker-doodle story illustrations | documented |  |
| `DRAW-40` | مشهد الرصاص الهادئ بلون واحد | Quiet pencil one-accent scene | documented |  |
| `DRAW-41` | إطارات ستوري بورد بالرصاص | Pencil storyboard frames | documented |  |
| `DRAW-42` | خريطة رحلة مرسومة باليد | Hand-drawn route sketch map | documented |  |
| `DRAW-43` | مخططات تجادل لا تعرض | Diagrams that argue (sketch patterns) | documented |  |
| `DRAW-45` | قص الرسومات من صفحة الكراسة | Sketch cut-out lift & eraser wipe | documented |  |
| `DRAW-55` | الرسم بالفأرة في برنامج الرسام | Drawing by mouse in Windows Paint | documented |  |
| `DRAW-56` | رسم فوق لقطات مولدة | Draw-over film on generated bases | documented | ffmpeg, chromium |
| `DRAW-57` | دراسة أسلوب مرسوم بالتتبع | Rotoscope style study & style pack | documented |  |
| `DRAW-G01` | رسم يدوي خشن ثابت البذرة | Seeded rough hand-drawn rendering | documented |  |
| `DRAW-G02` | زخم السحب والارتداد المطاطي | Drag momentum and rubber-band edges | documented |  |
| `DRAW-P01` | قصة الخط الواحد المستمر حتى الشعار | Continuous-line logo story (one stroke → three beats → wordmark loop) | documented | pip:numpy |
| `DRAW-U01` | فيلم يد مرسومة حتمي بـmake_frame(t) | Deterministic hand-drawn film via make_frame(t) | documented | ffmpeg, python3 |
| `DRAW-X01` | ريشة تكتب السطر الفعلي | Quill that writes the actual line (ink frontier) | documented |  |
| `RETRO-04` | مؤثرات بكسل بخطوات اللوحة | Palette-stepped pixel VFX sheets | documented | python3 |
| `RETRO-05` | البلاطات والبارالاكس | Seamless tiles & parallax rules | documented | node, chromium |
| `RETRO-12` | الذكريات على شرائط الفيلم | Memories on film strips | documented | imagemagick |
| `RETRO-20` | سينث ويف / ريترو ويف | Synthwave / retrowave | documented | python3, npm:three |
| `RETRO-21` | تليمتري CRT الداكن | Tactical telemetry / CRT-dark system | documented |  |
| `RETRO-23` | عائلة الخلايا: LED، ليغو، كروشيه، زجاج مموج | Cell-pattern family: LED, Lego, crochet, fluted glass, threshold matrices | documented | ffmpeg |
| `RETRO-30` | لوفاي دافئ متكرر | Lo-fi / cozy loop | documented | fonts:arabic |
| `RETRO-31` | بذور لوكات الريترو | Retro seed presets (vintage OS, arcade, neobrutalism, neon) | documented | fonts:arabic, npm:axe |
| `RETRO-X01` | شاشة LED نقطية وكلمات بكسل حقيقية | LED dot lattice bulge and true pixel words | documented |  |
| `SHAPE-02` | قانون التحويل: نقاط متساوية واتجاه واحد | Morph law: equal points, same winding | documented | npm:remotion |
| `SHAPE-13` | تحويل SVG بإضافة MorphSVG | MorphSVG plugin morph (HyperFrames rule) | documented | npm:gsap, npm:hyperframes |
| `SHAPE-14` | أسلوب الأشكال السائلة | Liquid-morph style | documented | python3, npm:hyperframes |
| `SHAPE-15` | العنصر المشترك (FLIP) | FLIP / shared-element continuity | documented |  |
| `SHAPE-16` | البطاقة كمرساة انتقال | Card-morph anchor handoff | documented | npm:gsap |
| `SHAPE-20` | أيقونة القائمة تصير إغلاقًا | Hamburger-to-close morph | documented |  |
| `SHAPE-21` | التحول عبر حالات الواجهة | Morph through UI states | documented |  |
| `SHAPE-31` | أشكال بدوال المسافة | 2D signed-distance shapes (union, morph, glow) | documented | pip:numpy |
| `SHAPE-38` | تموج ضغطة بحرارة | Press ripple with heat bloom | documented |  |
| `SHAPE-40` | اختيار المنحنى وسرعة ثابتة | Spline choice + arc-length constant speed | documented |  |
| `SHAPE-55` | بلاطات تنقلب وشريط لا ينتهي | Tile flips & endless strip loops (MG-116/117) | documented |  |
| `SHAPE-62` | حلقات دوران بنسب صحيحة | Integer-ratio rotation loops (MG-112/115) | documented |  |
| `SHAPE-78` | أيقونات SVG حية | Living SVG icons | documented |  |
| `SHAPE-79` | قواعد الأيقونة: شبكة 24 والإغلاق | Icon rules: 24 px grid & closure | documented |  |
| `SHAPE-89` | وحدة 24 وشبكة أعمدة | Base-unit grid system | documented |  |
| `SHAPE-90` | سلالم الأقطار والخطوط والفراغ | Primitive, radius & stroke scales | documented |  |
| `SHAPE-93` | أسلوب المرح الهندسي (S07) | Playful geometric style (S07) | documented | node, chromium |
| `SHAPE-G01` | رقم متحرك واحد يقود كل الأشكال | One animated value drives every dependent shape | documented |  |
| `SHAPE-G02` | تحويل يطابق الأجزاء المشتركة | Morph that matches shared parts | documented |  |
| `SHAPE-X01` | تحوّل هندسي بلا مزج | Geometric morph without a crossfade (letter → planet) | documented |  |
| `SHAPE-X02` | لقطة متصلة من عناصر مشتركة | One continuous shot from shared elements | documented |  |
| `BRAND-21` | الرمز وحده ثم الكلمة تنكشف بجانبه | Mark alone, then wordmark unfolds beside it | seen |  |
| `BRAND-23` | قفل المدار وانفجار الشرارات | Orbit-lock icon reveal & radial bursts | seen |  |
| `BRAND-24` | بكرات القمار والخط الأفقي | Slot-reel & horizon-line reveals | seen |  |
| `BRAND-28` | تشريح بطاقة الختام | End-card anatomy (icon · wordmark · tagline · URL pill · CTA) | seen |  |
| `BRAND-29` | ختام بنقرة مؤشر | CTA end card with a cursor click | seen |  |
| `BRAND-30` | النقطة كتوقيع العلامة | Brand full-stop dot | seen |  |
| `BRAND-31` | بطاقات الإصدار والمطوّرين | Release & developer end cards (version · terminal · Out now) | seen | node |
| `BRAND-32` | بطاقات الهوية الشخصية | Personal identity cards (name typed · contacts · chrome name) | seen |  |
| `BRAND-39` | مصفوفة مولّد الرمز البارامتري | Parametric mark-generator matrix | seen |  |
| `BRAND-40` | أنظمة البطاقات والشارات | Card & badge systems (neo-brutalist, seal, pill, banner) | seen |  |
| `BRAND-41` | لوكات الكلمة الشعار | Wordmark treatments (glow, gradient, per-letter colour, footer, hyphen) | seen |  |
| `EXPL-20` | التفرع إلى عدة | Fan-out branches & tree cascades | seen |  |
| `EXPL-21` | مخطط يُبنى مع الصوت | Voice-synced diagram build | seen | pip:faster-whisper |
| `EXPL-30` | طبقات شفافة إيزومترية | Isometric translucent layer stack | seen |  |
| `EXPL-31` | التضخيم والمقارنة بالمقياس | Exaggerated scale & size comparison | seen |  |
| `EXPL-38` | كود ومعاينة حية | Code + live preview split | seen |  |
| `EXPL-39` | كود مجرد ورقائق | Abstract code pills & token chips | seen |  |
| `EXPL-46` | دوائر فورييه والجيب | Fourier epicycles & unit-circle sine | seen |  |
| `EXPL-47` | برهان بصري بطيران الخلايا | Cell-flight visual proof | seen |  |
| `EXPL-48` | شروح تعلم الآلة | ML explainer devices | seen |  |
| `EXPL-49` | لوحة قياسات حية | Live telemetry & math HUD | seen |  |
| `EXPL-60` | بطاقات المقارنة والتشبيه والقوائم | Trade-off, analogy & checklist cards | seen |  |
| `EXPL-61` | أدوات بصرية للشرح | Explainer visual devices | seen |  |
| `DRAW-20` | خربشة توضيحية فوق الصورة | Doodle annotations on footage | seen |  |
| `DRAW-21` | شطب بخربشة ثم إعادة كتابة | Scribble strike-through rewrite | seen |  |
| `DRAW-22` | ملاحظة يدوية داخل إطار | Boxed handwritten callout | seen | npm:hyperframes |
| `DRAW-32` | خطوط ماء موازية للساحل | Triple coastline water lines | seen |  |
| `DRAW-44` | رسوم خطية استعارية تتحرك | Line-art metaphor motions | seen |  |
| `DRAW-46` | شريط مخطط يُرسم | Striped ribbon draw-on | seen |  |
| `RETRO-07` | ديوراما بكسل بانعكاس ماء | Pixel diorama with water reflection | seen |  |
| `RETRO-08` | واجهات ألعاب 8-بت: HUD وحوار وبطاقة عنوان | 8-bit HUD, dialogue box & game title card | seen |  |
| `RETRO-15` | عالم المانغا: خطوط سرعة وحبر | Manga speed-line burst world | seen |  |
| `RETRO-18` | لوحة LED نقطية وشريط أخبار | LED dot-matrix ticker | seen |  |
| `RETRO-25` | تموّج أوب آرت | Op-art concentric moiré | seen |  |
| `SHAPE-05` | تحويل المضلعات وأشكال باوهاوس | Polygon / Bauhaus primitive morph | seen |  |
| `SHAPE-06` | تحويل بنابض ونجوم تدور | Spring shape morph with orbiting stars | seen |  |
| `SHAPE-07` | تحويل بصدى ملون أو أثر ضبابي | Morph with coloured echo / blur trail | seen |  |
| `SHAPE-08` | تحويل داخل صندوق أداة تصميم | Design-tool gizmo morph | seen |  |
| `SHAPE-09` | تحويل سحابة نقاط إلى أيقونة أو شبكة | Dot-cloud morph (scatter → grid / icon) | seen |  |
| `SHAPE-10` | شريط ينثني فيصير حلقة | Bar bends into a ring | seen |  |
| `SHAPE-11` | رسم يدوي يصير نظيفًا | Sketch-to-clean morph | seen |  |
| `SHAPE-18` | جزيرة ديناميكية وزر ينفتح نافذة | Dynamic-island / button-to-window morph | seen |  |
| `SHAPE-19` | مؤشر مطاطي بحافتين | Two-edge stretchy indicator | seen |  |
| `SHAPE-22` | نقطة تتفتح إلى واجهة أو نظام | Dot-to-interface / dot-to-system bloom | seen |  |
| `SHAPE-24` | الشعار يصير بؤبؤ عين | Logo-to-iris / eye opening | seen |  |
| `SHAPE-36` | كتلة متدرجة أو متحولة خلف النص | Gradient / morphing blob behind text | seen |  |
| `SHAPE-37` | إطار مطاطي وقناع قضمة | Rubber-frame strain & bite mask | seen |  |
| `SHAPE-47` | صندوق أيزومتري بثلاث درجات | Three-tone isometric box | seen |  |
| `SHAPE-48` | بناء نقطة ثم خط ثم مستوى | Point → line → plane build | seen |  |
| `SHAPE-49` | خطوط متدفقة ومسارات مخططة | Flowing dashes, striped tubes, dotted trails | seen |  |
| `SHAPE-54` | موجة في شبكة أشكال | Distance-delayed grid wave (rotate / scale / morph) | seen |  |
| `SHAPE-57` | منحنيات ليساجو | Lissajous curves & tangles | seen |  |
| `SHAPE-58` | خطوط توليدية بأسلوب Joy Division | Ridge-line generative waves | seen |  |
| `SHAPE-59` | كسيريات وزخارف رياضية | Fractals, kolam, golden spiral, kaleidoscope | seen |  |
| `SHAPE-60` | جدار أيقونات مائل | Tilted icon wall | seen |  |
| `SHAPE-69` | حلقة نقاط تتسع بخطوط شعاعية | Expanding dot ring with radial lines | seen |  |
| `SHAPE-70` | نفق مربعات حلزوني | Spiral square tunnel & nested squares | seen |  |
| `SHAPE-71` | مربع يصير دائرة مع أقمار | Square→circle with satellites & star pop | seen |  |
| `SHAPE-72` | بوابة دوامية ومصباح فرينل | Swirl portal & Fresnel lamp room | seen |  |
| `SHAPE-81` | ملصقات زخرفية وكبسولات وسوم | Decor stickers, hazard tape & floating tag pills | seen |  |
| `SHAPE-82` | مروحة بطاقات وصور | Card / photo / swatch fan-out | seen |  |
| `SHAPE-83` | شريط تظليل مائل خلف النص | Slanted highlighter bar wipe | seen |  |
| `SHAPE-84` | تغيير لون الكلمة داخل الكرة | Clip-path colour flip over a moving lens | seen |  |
| `SHAPE-85` | تجميع من شظايا أو قطع | Shard / piece assembly along a path | seen |  |
| `SHAPE-86` | شاشة مقسومة واستعارة الكسوف | Split-screen eclipse metaphor | seen |  |
| `SHAPE-87` | بحر خطوط مع شخصية رمزية | Line-art sea with mascot | seen |  |
| `BRAND-09` | حقيبة العلامة في بصمة | Basma brand kit: import, palette-from-logo, watermark & end card | install | node |
| `BRAND-25` | كشوف وختام HyperFrames الجاهزة | HyperFrames logo blocks (sting, tiles, extruded, outro, intro, split-pulse) | install | npm:three, npm:hyperframes |
| `BRAND-26` | بطاقة شعار Remotion بحلقة وشيفرون | Remotion logo card: ring draw + chevron mark | install | npm:remotion |
| `BRAND-34` | كتل الختام والدليل الاجتماعي | Closer blocks: CTA close/lockup, social proof, testimonials, trust strip | install | npm:hyperframes |
| `EXPL-11` | مخططات Mermaid من نص | Mermaid text-to-diagram | install | npm:mermaid |
| `EXPL-13` | سبورة Excalidraw ولوحات JSON Canvas | Excalidraw & JSON Canvas boards | install | node, chromium |
| `EXPL-14` | شبكة مفاهيم بقوة الجذب | Force-directed concept graph | install | npm:d3 |
| `EXPL-19` | محور وأذرع ومدارات | Hub-and-spoke, constellations & orbits | install | npm:hyperframes |
| `EXPL-24` | مسار قرار ومخطط انسيابي | Decision path & flowchart | install | npm:hyperframes |
| `EXPL-33` | كتابة بتذبذب مزروع | Seeded typing animation | install | npm:remotion |
| `EXPL-40` | كتل HyperFrames للكود | HyperFrames code blocks | install | npm:three, npm:gsap, npm:hyperframes |
| `EXPL-41` | من طلب دمج أو نص إلى فيديو شرح | PR-to-video & faceless explainer pipelines | install | pip:kokoro, npm:hyperframes |
| `EXPL-44` | معادلة تتكون خطوة خطوة | Equation built step by step (bidi-safe) | install | node |
| `EXPL-45` | Manim للاشتقاق والنهايات | Manim derivations & limits | install | python3 |
| `EXPL-X01` | فيديو شرح بـManim | Manim explainer workflow | install | ffmpeg, python3, latex, npm:remotion |
| `DRAW-09` | سلامة رسم المسارات | SVG draw-on safety | install | npm:hyperframes |
| `DRAW-16` | كتابة حقيقية بترتيب الضربات (لاتيني) | True glyph write-on with stroke order (Latin) | install | python3, npm:gsap, npm:hyperframes |
| `DRAW-23` | علامات rough-notation | Rough-notation marks | install | npm:remotion |
| `DRAW-27` | رسم خشن بأسلوب Rough.js | Rough.js / Excalidraw sketch rendering | install | node |
| `DRAW-59` | مكونات HyperFrames للرسم اليدوي | HyperFrames hand-drawn components | install | npm:gsap, npm:hyperframes, key:unspecified |
| `DRAW-60` | مكتبات الرسم التدريجي | Draw-on libraries | install | npm:remotion |
| `RETRO-14` | معالجات الصورة الطباعية في HyperFrames | HyperFrames print treatments (engraving, crosshatch, Kuwahara, two-ink, halftone) | install | npm:hyperframes |
| `RETRO-17` | لقطات تبدو على شاشة حقيقية | On-screen display & camcorder HUD | install | npm:gsap, npm:hyperframes |
| `RETRO-19` | أثر الأوسيلوسكوب الفوسفوري | Oscilloscope phosphor trace | install | npm:hyperframes |
| `SHAPE-12` | تحول متعدد الأوجه | Facet morph (36 low-poly triangles) | install | npm:hyperframes |
| `SHAPE-28` | الانقسام اللزج والكتلة الناعمة | Gooey split & soft blob touch (HyperFrames) | install | npm:gsap, npm:hyperframes |
| `SHAPE-30` | كتلة عضوية بضوضاء الرؤوس | Noise-displaced 3D blob | install | npm:three |
| `SHAPE-39` | الحركة على مسار SVG | Motion along an SVG path | install | chromium, npm:gsap |
| `SHAPE-61` | كتل أنماط شيدرية وشبكة متحركة | HyperFrames pattern shaders & dynamic grid | install | npm:hyperframes |
| `SHAPE-80` | طبقات أشكال وملصقات منبثقة | Shape layers & sticker/emoji pop-ups | install | node, fonts:arabic |
| `SHAPE-88` | فاصل بشعرة | Hairline separator (HyperFrames) | install | npm:hyperframes |
| `BRAND-10` | جلب الشعار الرسمي لا رسمه | Official logo resolution (never redraw) | key | npm:hyperframes, key:unspecified |
| `BRAND-11` | استيراد Figma وCanva | Figma / Canva import | key | npm:gsap, key:unspecified |
| `BRAND-16` | توليد الشعار بالذكاء ثم تنقيحه | AI mark generation (Recraft / prompt) then curate | key | key:unspecified |
| `EXPL-09` | توليد أيقونات بخلفية شفافة | Transparent icon generation | key | pip:pillow, pip:onnxruntime, pip:rembg, key:unspecified |
| `BRAND-27` | كشف سائل بإزاحة الأثر | Liquid trail-displacement logo reveal | idea |  |
| `EXPL-43` | شجرة ملفات تتحول إلى أعمدة | Folder tree to bar chart | idea |  |
| `EXPL-64` | نموذج مجرة الأدلة | Evidence galaxy graph model | idea |  |
| `RETRO-09` | فاصل بكسل داخل مونتاج حديث | Pixel chapter break inside a modern edit | idea | ffmpeg |
| `SHAPE-25` | نقرة وتحول لعلامة صح | Tap ripple + circle-to-check morph | idea |  |
| `SHAPE-26` | ظرف يتحول لشارة / تجمع إلى شعار | Envelope→badge, converge→monogram, collapse→dot | idea |  |
| `SHAPE-29` | تجمع الصلصال بالكرات | Metaball clay assembly | idea |  |
| `SHAPE-92` | التصاق مغناطيسي وكل شيء من المركز | Magnet snap spring & centre-origin rule | idea | npm:remotion |
