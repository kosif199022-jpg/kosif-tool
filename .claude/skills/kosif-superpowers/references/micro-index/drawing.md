# الرسم والأشكال والتصميم — Drawing & visual composition

[← الفهرس الدقيق / micro index](README.md) · 306 powers

## الفهرس / contents

- [brand-logo-identity (motion)](#brand-logo-identity-motion)
- [diagrams-explainers-code (motion)](#diagrams-explainers-code-motion)
- [hand-drawn-draw-on (motion)](#hand-drawn-draw-on-motion)
- [pixel-retro-stylized (motion)](#pixel-retro-stylized-motion)
- [shapes-morph-geometry (motion)](#shapes-morph-geometry-motion)


## brand-logo-identity (motion)

chapter: [brand-logo-identity](../powers/brand-logo-identity.md) · card: `usip-library/cards/drawing/brand-logo-identity.md` · tools: `brand-tokens`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| BRAND-13 | ✅ | تحويل الشعار النقطي إلى متجه بألوانه · Raster logo → true-colour vector layers | SP-0190 SVG logo construction rules & logo suite | python3 |
| BRAND-15 | ✅ | شعارات KOSIF المبنية بالكود · Owner marks built in code (SQC, K marks, ram, cloud) | SP-0190 SVG logo construction rules & logo suite | — |
| BRAND-17 | ✅ | كشف فاخر بالزجاج والذهب · Luxury glass-and-gold reveal (proof film) | SP-0190 SVG logo construction rules & logo suite | — |
| BRAND-18 | ✅ | رسم الخط ثم التعبئة · Stroke draw-on then fill | SP-0190 SVG logo construction rules & logo suite | python3 |
| BRAND-33 | ✅ | مكتبة بطاقات الختام للثيمات (17) · Per-theme end-card library (17) + user-owned wordmark slot | SP-0190 SVG logo construction rules & logo suite | — |
| BRAND-37 | ✅ | قوالب الموشن العربية الثمانية · Eight Arabic motion templates (logo-reveal, end-card …) | SP-0190 SVG logo construction rules & logo suite | python3, fonts:arabic |
| BRAND-05 | 🟢 | أنظمة تصميم جاهزة للكاميرا (frame.md) · Video-first design presets (frame.md) | SP-0190 SVG logo construction rules & logo suite | chromium, npm:hyperframes |
| BRAND-12 | 🟢 | قواعد بناء الشعار SVG · SVG logo construction rules & logo suite | SP-0190 SVG logo construction rules & logo suite | node, pip:fonttools |
| BRAND-22 | 🟢 | انكماش التباعد إلى الشعار (لاتيني فقط) · Tracking-collapse lockup (Latin only) | SP-0190 SVG logo construction rules & logo suite | — |
| BRAND-35 | 🟢 | إطار البث الثابت وتوقيع الزاوية · Persistent broadcast chrome & corner signature | SP-0190 SVG logo construction rules & logo suite | — |
| BRAND-42 | 🟢 | ملصق إعلان منتج عربي متجهي · Arabic vector product-ad poster (whole lamb) | SP-0190 SVG logo construction rules & logo suite | pip:pillow |
| BRAND-43 | 🟢 | نظام «ورق الدفتر» ولوك المانيفست · Ledger-paper design system & manifest title look | SP-0190 SVG logo construction rules & logo suite | pip:faster-whisper |
| BRAND-09 | 📦 | حقيبة العلامة في بصمة · Basma brand kit: import, palette-from-logo, watermark & end card | SP-0190 SVG logo construction rules & logo suite | node |
| BRAND-25 | 📦 | كشوف وختام HyperFrames الجاهزة · HyperFrames logo blocks (sting, tiles, extruded, outro, intro, split-pulse) | SP-0190 SVG logo construction rules & logo suite | npm:three, npm:hyperframes |
| BRAND-26 | 📦 | بطاقة شعار Remotion بحلقة وشيفرون · Remotion logo card: ring draw + chevron mark | SP-0190 SVG logo construction rules & logo suite | npm:remotion |
| BRAND-10 | 🔑 | جلب الشعار الرسمي لا رسمه · Official logo resolution (never redraw) | SP-0190 SVG logo construction rules & logo suite | npm:hyperframes, key:unspecified |
| BRAND-11 | 🔑 | استيراد Figma وCanva · Figma / Canva import | SP-0190 SVG logo construction rules & logo suite | npm:gsap, key:unspecified |
| BRAND-16 | 🔑 | توليد الشعار بالذكاء ثم تنقيحه · AI mark generation (Recraft / prompt) then curate | SP-0190 SVG logo construction rules & logo suite | key:unspecified |
| BRAND-21 | 👁 | الرمز وحده ثم الكلمة تنكشف بجانبه · Mark alone, then wordmark unfolds beside it | SP-0190 SVG logo construction rules & logo suite | — |
| BRAND-24 | 👁 | بكرات القمار والخط الأفقي · Slot-reel & horizon-line reveals | SP-0190 SVG logo construction rules & logo suite | — |
| BRAND-39 | 👁 | مصفوفة مولّد الرمز البارامتري · Parametric mark-generator matrix | SP-0190 SVG logo construction rules & logo suite | — |
| BRAND-41 | 👁 | لوكات الكلمة الشعار · Wordmark treatments (glow, gradient, per-letter colour, footer, hyphen) | SP-0190 SVG logo construction rules & logo suite | — |
| BRAND-01 | 📄 | بريف الشعار: الشيء الواحد · Logo brief: the ONE THING | SP-0190 SVG logo construction rules & logo suite | — |
| BRAND-04 | 📄 | رموز بثلاث طبقات ومصفوفة العلامات · Three-tier tokens & multi-brand theming | SP-0190 SVG logo construction rules & logo suite | npm:gsap, npm:remotion |
| BRAND-19 | 📄 | شعار يتجمع من أجزائه · Assembled mark (blocks · dots · tiles · particles) | SP-0190 SVG logo construction rules & logo suite | — |
| BRAND-20 | 📄 | كشوف القناع: ظل، ضباب، ختم، فراغ سالب · Mask reveals: shadow pass, fog, ink stamp, negative space | SP-0190 SVG logo construction rules & logo suite | — |
| BRAND-27 | 💡 | كشف سائل بإزاحة الأثر · Liquid trail-displacement logo reveal | SP-0190 SVG logo construction rules & logo suite | — |
| BRAND-08 | ✅ | من الموقع إلى مادة الفيلم · Site → film material (palette, fonts, CTAs) | SP-0191 CTA end card with a cursor click | chromium |
| BRAND-36 | 🟢 | غمر لون العلامة · Brand-colour flood end frame | SP-0191 CTA end card with a cursor click | fonts:arabic |
| BRAND-29 | 👁 | ختام بنقرة مؤشر · CTA end card with a cursor click | SP-0191 CTA end card with a cursor click | — |
| BRAND-31 | 👁 | بطاقات الإصدار والمطوّرين · Release & developer end cards (version · terminal · Out now) | SP-0191 CTA end card with a cursor click | node |
| BRAND-32 | 👁 | بطاقات الهوية الشخصية · Personal identity cards (name typed · contacts · chrome name) | SP-0191 CTA end card with a cursor click | — |
| BRAND-40 | 👁 | أنظمة البطاقات والشارات · Card & badge systems (neo-brutalist, seal, pill, banner) | SP-0191 CTA end card with a cursor click | — |
| BRAND-03 | 🟢 | ورقة نظام العلامة للفيديو · Video brand-system sheet | SP-0192 Brand book anatomy & voice | python3 |
| BRAND-02 | 📄 | مقابلة العميل بلا هوية · Identity interview for no-brand clients | SP-0192 Brand book anatomy & voice | npm:hyperframes, fonts:arabic |
| BRAND-06 | 📄 | كتاب العلامة وصوتها · Brand book anatomy & voice | SP-0192 Brand book anatomy & voice | npm:axe |
| BRAND-07 | 📄 | بوابة ترخيص الخطوط والملكية · Font-licence & IP gate | SP-0192 Brand book anatomy & voice | fonts:arabic |
| BRAND-38 | 📄 | مونتاج شبكة العلامة · Brand grid montage | SP-0192 Brand book anatomy & voice | imagemagick |
| BRAND-14 | ✅ | مجموعات الأيقونات وأيقونات التطبيق · Icon families, app icons & favicon sets | SP-0193 End-card anatomy (icon · wordmark · tag… | python3, chromium |
| BRAND-34 | 📦 | كتل الختام والدليل الاجتماعي · Closer blocks: CTA close/lockup, social proof, testimonials, trust strip | SP-0193 End-card anatomy (icon · wordmark · tag… | npm:hyperframes |
| BRAND-23 | 👁 | قفل المدار وانفجار الشرارات · Orbit-lock icon reveal & radial bursts | SP-0193 End-card anatomy (icon · wordmark · tag… | — |
| BRAND-28 | 👁 | تشريح بطاقة الختام · End-card anatomy (icon · wordmark · tagline · URL pill · CTA) | SP-0193 End-card anatomy (icon · wordmark · tag… | — |
| BRAND-30 | 👁 | النقطة كتوقيع العلامة · Brand full-stop dot | SP-0193 End-card anatomy (icon · wordmark · tag… | — |

## diagrams-explainers-code (motion)

chapter: [diagrams-explainers-code](../powers/diagrams-explainers-code.md) · card: `usip-library/cards/drawing/diagrams-explainers-code.md` · tools: `diagram-layout`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| EXPL-50 | ✅ | التوأم الإنشائي: حلّال الجملونات · Structural twin truss solver | SP-0247 Explainer diagram composition | python3 |
| EXPL-54 | ✅ | دورة الماء التعليمية المسطحة · Flat educational water cycle | SP-0247 Explainer diagram composition | fonts:arabic |
| EXPL-25 | 🟢 | دورة ورمز ينتقل · Cycle diagram, travelling token & loop arrow | SP-0247 Explainer diagram composition | — |
| EXPL-26 | 🟢 | شريط المراحل ومؤشر الخطوات · Stage tracker pills & steppers | SP-0247 Explainer diagram composition | — |
| EXPL-29 | 🟢 | تسميات بخطوط قائدة · Leader-line callouts (2D & 3D) | SP-0247 Explainer diagram composition | — |
| EXPL-51 | 🟢 | فيلم التوأم الإنشائي · Structural twin film (truss on a character) | SP-0247 Explainer diagram composition | python3 |
| EXPL-53 | 🟢 | شرح علمي ثلاثي الأبعاد بأربع مراحل · Four-stage 3D science explainer | SP-0247 Explainer diagram composition | — |
| EXPL-58 | 🟢 | فئات المخططات والكود في بصمة · Basma diagram & code film categories | SP-0247 Explainer diagram composition | — |
| EXPL-11 | 📦 | مخططات Mermaid من نص · Mermaid text-to-diagram | SP-0247 Explainer diagram composition | npm:mermaid |
| EXPL-24 | 📦 | مسار قرار ومخطط انسيابي · Decision path & flowchart | SP-0247 Explainer diagram composition | npm:hyperframes |
| EXPL-33 | 📦 | كتابة بتذبذب مزروع · Seeded typing animation | SP-0247 Explainer diagram composition | npm:remotion |
| EXPL-40 | 📦 | كتل HyperFrames للكود · HyperFrames code blocks | SP-0247 Explainer diagram composition | npm:three, npm:gsap, npm:hyperframes |
| EXPL-41 | 📦 | من طلب دمج أو نص إلى فيديو شرح · PR-to-video & faceless explainer pipelines | SP-0247 Explainer diagram composition | pip:kokoro, npm:hyperframes |
| EXPL-44 | 📦 | معادلة تتكون خطوة خطوة · Equation built step by step (bidi-safe) | SP-0247 Explainer diagram composition | node |
| EXPL-X01 | 📦 | فيديو شرح بـManim · Manim explainer workflow | SP-0247 Explainer diagram composition | ffmpeg, python3, latex, npm:remotion … |
| EXPL-20 | 👁 | التفرع إلى عدة · Fan-out branches & tree cascades | SP-0247 Explainer diagram composition | — |
| EXPL-21 | 👁 | مخطط يُبنى مع الصوت · Voice-synced diagram build | SP-0247 Explainer diagram composition | pip:faster-whisper |
| EXPL-30 | 👁 | طبقات شفافة إيزومترية · Isometric translucent layer stack | SP-0247 Explainer diagram composition | — |
| EXPL-31 | 👁 | التضخيم والمقارنة بالمقياس · Exaggerated scale & size comparison | SP-0247 Explainer diagram composition | — |
| EXPL-38 | 👁 | كود ومعاينة حية · Code + live preview split | SP-0247 Explainer diagram composition | — |
| EXPL-47 | 👁 | برهان بصري بطيران الخلايا · Cell-flight visual proof | SP-0247 Explainer diagram composition | — |
| EXPL-48 | 👁 | شروح تعلم الآلة · ML explainer devices | SP-0247 Explainer diagram composition | — |
| EXPL-49 | 👁 | لوحة قياسات حية · Live telemetry & math HUD | SP-0247 Explainer diagram composition | — |
| EXPL-61 | 👁 | أدوات بصرية للشرح · Explainer visual devices | SP-0247 Explainer diagram composition | — |
| EXPL-01 | 📄 | قواعد تركيب مخطط الشرح · Explainer diagram composition | SP-0247 Explainer diagram composition | — |
| EXPL-03 | 📄 | اختيار نوع المخطط والتخطيط · Diagram type & layout chooser | SP-0247 Explainer diagram composition | npm:mermaid |
| EXPL-05 | 📄 | عكس المخطط للعربية · Mirrored RTL diagrams | SP-0247 Explainer diagram composition | — |
| EXPL-07 | 📄 | إطار الشرح الأحادي · Learning-mono explainer frame | SP-0247 Explainer diagram composition | — |
| EXPL-10 | 📄 | مخططات SVG برمجية بالملليمتر · Programmatic SVG schematics | SP-0247 Explainer diagram composition | pip:fonttools |
| EXPL-22 | 📄 | التكبير على مكوّن وقبل/بعد · Zoom into component & before/after diagram | SP-0247 Explainer diagram composition | ffmpeg |
| EXPL-28 | 📄 | مقارنة سرعة عادلة · Fair speed comparison | SP-0247 Explainer diagram composition | — |
| EXPL-35 | 📄 | إبراز السطر والتمرير والخطأ · Line highlight, scroll & error sweep | SP-0247 Explainer diagram composition | — |
| EXPL-36 | 📄 | كشف الفرق · Diff reveal | SP-0247 Explainer diagram composition | — |
| EXPL-56 | 📄 | نظام بطاقات الفيديو الشارح · Explainer card system | SP-0247 Explainer diagram composition | node, chromium |
| EXPL-G01 | 📄 | قواعد مشهد الشرح الرياضي · Explainer scene grammar | SP-0247 Explainer diagram composition | — |
| EXPL-G02 | 📄 | مخطط بنية سحابية بالكود ثم كشفه · Architecture diagram as code, revealed by cluster | SP-0247 Explainer diagram composition | — |
| EXPL-U01 | 📄 | قائمة الأساليب الخمسة للموشن بالكود · Five code-rendered motion-graphics styles menu | SP-0247 Explainer diagram composition | — |
| EXPL-U02 | 📄 | لقطة التحليل المجمّدة · Frozen analysis beat overlay | SP-0247 Explainer diagram composition | — |
| EXPL-43 | 💡 | شجرة ملفات تتحول إلى أعمدة · Folder tree to bar chart | SP-0247 Explainer diagram composition | — |
| EXPL-15 | 🟢 | خريطة الكيان في المنتصف · Entity node map with flow edges | SP-0248 Marching-dash flow edges | — |
| EXPL-18 | 🟢 | خطوط تدفق متحركة · Marching-dash flow edges | SP-0248 Marching-dash flow edges | — |
| EXPL-52 | 🟢 | منظر تخطيطي ومفكك · Schematic, wireframe & exploded view | SP-0248 Marching-dash flow edges | — |
| EXPL-62 | 🟢 | أسلوب الرسومات التقنية · Tech blueprint style | SP-0248 Marching-dash flow edges | python3 |
| EXPL-46 | 👁 | دوائر فورييه والجيب · Fourier epicycles & unit-circle sine | SP-0248 Marching-dash flow edges | — |
| EXPL-17 | 📄 | نبضة بيانات على الرابط · Data pulse along edges | SP-0248 Marching-dash flow edges | — |
| EXPL-23 | 📄 | الخط الزمني برأس تشغيل · Timeline with playhead | SP-0248 Marching-dash flow edges | — |
| EXPL-34 | 📄 | جلسة الطرفية · Terminal session scene | SP-0248 Marching-dash flow edges | — |
| EXPL-42 | 📄 | حرّك ما يفعله الكود · Mechanism beat: animate behaviour, not code | SP-0248 Marching-dash flow edges | npm:gsap, claude:tools |
| EXPL-57 | 📄 | الوثيقة المصدر وقلم التظليل · Source document & article excerpt overlay | SP-0248 Marching-dash flow edges | — |
| EXPL-59 | 🟢 | رسومات استعارية لكل جملة · Metaphor graphic per spoken claim | SP-0249 Causal build order & node states | — |
| EXPL-60 | 👁 | بطاقات المقارنة والتشبيه والقوائم · Trade-off, analogy & checklist cards | SP-0249 Causal build order & node states | — |
| EXPL-02 | 📄 | قواعد العقد والروابط · Node & edge grammar | SP-0249 Causal build order & node states | key:unspecified |
| EXPL-04 | 📄 | ترتيب البناء السببي وحالات العقد · Causal build order & node states | SP-0249 Causal build order & node states | — |
| EXPL-16 | 📄 | عملية من ثلاث خطوات · Three-step process recipe | SP-0249 Causal build order & node states | — |
| EXPL-27 | 📄 | خطأ ثم تصحيح · Mistake then correction | SP-0249 Causal build order & node states | — |
| EXPL-55 | 📄 | قواعد الدقة والوضوح للأطفال · Science accuracy & causal-step rules | SP-0249 Causal build order & node states | — |
| EXPL-13 | 📦 | سبورة Excalidraw ولوحات JSON Canvas · Excalidraw & JSON Canvas boards | SP-0250 Force-directed concept graph | node, chromium |
| EXPL-14 | 📦 | شبكة مفاهيم بقوة الجذب · Force-directed concept graph | SP-0250 Force-directed concept graph | npm:d3 |
| EXPL-19 | 📦 | محور وأذرع ومدارات · Hub-and-spoke, constellations & orbits | SP-0250 Force-directed concept graph | npm:hyperframes |
| EXPL-39 | 👁 | كود مجرد ورقائق · Abstract code pills & token chips | SP-0250 Force-directed concept graph | — |
| EXPL-63 | 📄 | لوحات ستوري بورد SVG مصغرة · SVG thumbnail storyboards | SP-0250 Force-directed concept graph | — |
| EXPL-64 | 💡 | نموذج مجرة الأدلة · Evidence galaxy graph model | SP-0250 Force-directed concept graph | — |
| EXPL-06 | 📄 | ألوان دلالية للأدوار · Semantic role colours | SP-0251 On-screen code typography | npm:mermaid |
| EXPL-12 | 📄 | مخططات D2 · D2 declarative diagrams | SP-0251 On-screen code typography | npm:mermaid |
| EXPL-32 | 📄 | طباعة الكود على الشاشة · On-screen code typography | SP-0251 On-screen code typography | — |
| EXPL-37 | 📄 | نافذة كود مشروحة · Annotated code-window figure | SP-0251 On-screen code typography | — |
| EXPL-45 | 📦 | Manim للاشتقاق والنهايات · Manim derivations & limits | SP-0252 Closure limits for minimal icons | python3 |
| EXPL-09 | 🔑 | توليد أيقونات بخلفية شفافة · Transparent icon generation | SP-0252 Closure limits for minimal icons | pip:pillow, pip:onnxruntime, pip:rembg, key:unspecified |
| EXPL-08 | 📄 | حدود الأيقونات المختصرة · Closure limits for minimal icons | SP-0252 Closure limits for minimal icons | — |

## hand-drawn-draw-on (motion)

chapter: [hand-drawn-draw-on](../powers/hand-drawn-draw-on.md) · card: `usip-library/cards/drawing/hand-drawn-draw-on.md` · tools: `app-studio-paint` · `atlas-render` · `code-drawing-master` · `color-media` · `creative-paint` · `creative-principles` · `creative-reasoning-bridge` · `drawing-academy` …

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| DRAW-52 | ✅ | صورة إلى برنامج بايثون · Image to standalone Pillow program | SP-0277 Workbench Pillow film | pip:pillow |
| DRAW-01 | ✅ | رسم المسار بإزاحة الشرطة · SVG stroke draw-on | SP-0304 Deterministic hand-drawn film via make_… | — |
| DRAW-03 | ✅ | سرعة القلم والرفع · Pen speed & lifts | SP-0304 Deterministic hand-drawn film via make_… | — |
| DRAW-04 | ✅ | ترتيب الرسم البشري ووصفة «ارسم وسمِّ» · Human draw order & draw-and-label | SP-0304 Deterministic hand-drawn film via make_… | — |
| DRAW-06 | ✅ | رأس يتبع الخط: يد، ماركر، طباشيرة · Pen-tip followers: hand, marker, chalk | SP-0304 Deterministic hand-drawn film via make_… | npm:remotion |
| DRAW-14 | ✅ | قوالب موشن بالقلم · Pen-drawn motion templates | SP-0304 Deterministic hand-drawn film via make_… | python3 |
| DRAW-33 | ✅ | سبورة بيضاء · Whiteboard | SP-0304 Deterministic hand-drawn film via make_… | python3 |
| DRAW-49 | ✅ | فيلم الرسم · Drawing film (picture forming as MP4) | SP-0304 Deterministic hand-drawn film via make_… | python3 |
| DRAW-50 | ✅ | الرسم بترتيب الكود نفسه · PIL command recorder | SP-0304 Deterministic hand-drawn film via make_… | pip:pillow |
| DRAW-53 | ✅ | استيراد SVG والتحويل إلى متجهات · SVG import & vectorize to draw steps | SP-0304 Deterministic hand-drawn film via make_… | python3 |
| DRAW-54 | ✅ | محوّل مسارات SVG إلى نقاط · SVG path sampler | SP-0304 Deterministic hand-drawn film via make_… | python3 |
| DRAW-34 | 🟢 | سبورة سينمائية · Whiteboard cinematic | SP-0304 Deterministic hand-drawn film via make_… | python3 |
| DRAW-35 | 🟢 | سبورة الطباشير · Chalkboard | SP-0304 Deterministic hand-drawn film via make_… | python3, fonts:arabic |
| DRAW-36 | 🟢 | قصص الدودل · Doodle stories | SP-0304 Deterministic hand-drawn film via make_… | python3, fonts:arabic |
| DRAW-37 | 🟢 | قلم البلوتر · Plotter pen | SP-0304 Deterministic hand-drawn film via make_… | python3 |
| DRAW-38 | 🟢 | إطار بإطار على اثنين · Frame-by-frame on twos | SP-0304 Deterministic hand-drawn film via make_… | python3 |
| DRAW-47 | 🟢 | من مخطط سلكي إلى مجسم · Wireframe draw → solid formation | SP-0304 Deterministic hand-drawn film via make_… | npm:three |
| DRAW-58 | 🟢 | إعادة رسم مخرجات مولدة كمتجهات · Generated raster → hand vector recreation | SP-0304 Deterministic hand-drawn film via make_… | — |
| DRAW-59 | 📦 | مكونات HyperFrames للرسم اليدوي · HyperFrames hand-drawn components | SP-0304 Deterministic hand-drawn film via make_… | npm:gsap, npm:hyperframes, key:unspecified |
| DRAW-20 | 👁 | خربشة توضيحية فوق الصورة · Doodle annotations on footage | SP-0304 Deterministic hand-drawn film via make_… | — |
| DRAW-26 | 📄 | غليان الخط · Line boil | SP-0304 Deterministic hand-drawn film via make_… | npm:hyperframes |
| DRAW-42 | 📄 | خريطة رحلة مرسومة باليد · Hand-drawn route sketch map | SP-0304 Deterministic hand-drawn film via make_… | — |
| DRAW-55 | 📄 | الرسم بالفأرة في برنامج الرسام · Drawing by mouse in Windows Paint | SP-0304 Deterministic hand-drawn film via make_… | — |
| DRAW-56 | 📄 | رسم فوق لقطات مولدة · Draw-over film on generated bases | SP-0304 Deterministic hand-drawn film via make_… | ffmpeg, chromium |
| DRAW-G01 | 📄 | رسم يدوي خشن ثابت البذرة · Seeded rough hand-drawn rendering | SP-0304 Deterministic hand-drawn film via make_… | — |
| DRAW-U01 | 📄 | فيلم يد مرسومة حتمي بـmake_frame(t) · Deterministic hand-drawn film via make_frame(t) | SP-0304 Deterministic hand-drawn film via make_… | ffmpeg, python3 |
| DRAW-15 | ✅ | كتابة بقناع فرشاة من اليمين · Brush-mask write-on (RTL) | SP-0305 Brush-mask write-on (RTL) | fonts:arabic |
| DRAW-48 | ✅ | ترتيب الرسام في الكشف · Painter reveal orders | SP-0305 Brush-mask write-on (RTL) | — |
| DRAW-24 | 🟢 | خط الرحلة من اليمين · Journey line draw-on (RTL) | SP-0305 Brush-mask write-on (RTL) | — |
| DRAW-16 | 📦 | كتابة حقيقية بترتيب الضربات (لاتيني) · True glyph write-on with stroke order (Latin) | SP-0305 Brush-mask write-on (RTL) | python3, npm:gsap, npm:hyperframes |
| DRAW-21 | 👁 | شطب بخربشة ثم إعادة كتابة · Scribble strike-through rewrite | SP-0305 Brush-mask write-on (RTL) | — |
| DRAW-22 | 👁 | ملاحظة يدوية داخل إطار · Boxed handwritten callout | SP-0305 Brush-mask write-on (RTL) | npm:hyperframes |
| DRAW-08 | 📄 | كشف متعدد الأجزاء بالطول التراكمي · Cumulative-length multi-segment reveal | SP-0305 Brush-mask write-on (RTL) | — |
| DRAW-30 | 📄 | محرك فرشاة الحبر الحتمي · Deterministic ink-brush engine | SP-0305 Brush-mask write-on (RTL) | chromium |
| DRAW-43 | 📄 | مخططات تجادل لا تعرض · Diagrams that argue (sketch patterns) | SP-0305 Brush-mask write-on (RTL) | — |
| DRAW-X01 | 📄 | ريشة تكتب السطر الفعلي · Quill that writes the actual line (ink frontier) | SP-0305 Brush-mask write-on (RTL) | — |
| DRAW-02 | 🟢 | قلم مكتبة الحركة برأس يهبط · Kit drawPath with landing head & flowDash | SP-0306 Striped ribbon draw-on | — |
| DRAW-05 | 🟢 | رابط مخطط برأس سهم · Diagram edge draw-on with arrowhead | SP-0306 Striped ribbon draw-on | npm:remotion, key:unspecified |
| DRAW-10 | 🟢 | نهر يمتلئ ثم يجري · River fill then flow | SP-0306 Striped ribbon draw-on | — |
| DRAW-11 | 🟢 | المحراب بقلم ذهبي · Gold-pen arch draw-on | SP-0306 Striped ribbon draw-on | — |
| DRAW-09 | 📦 | سلامة رسم المسارات · SVG draw-on safety | SP-0306 Striped ribbon draw-on | npm:hyperframes |
| DRAW-60 | 📦 | مكتبات الرسم التدريجي · Draw-on libraries | SP-0306 Striped ribbon draw-on | npm:remotion |
| DRAW-32 | 👁 | خطوط ماء موازية للساحل · Triple coastline water lines | SP-0306 Striped ribbon draw-on | — |
| DRAW-46 | 👁 | شريط مخطط يُرسم · Striped ribbon draw-on | SP-0306 Striped ribbon draw-on | — |
| DRAW-G02 | 📄 | زخم السحب والارتداد المطاطي · Drag momentum and rubber-band edges | SP-0306 Striped ribbon draw-on | — |
| DRAW-07 | ✅ | رأس متوهج يجرّ الخط · Glowing head draw | SP-0307 Line micro-graphics over footage | — |
| DRAW-12 | 🟢 | رسوم خطية صغيرة فوق الفيديو · Line micro-graphics over footage | SP-0307 Line micro-graphics over footage | — |
| DRAW-13 | 🟢 | أيقونات المعنى المرسومة · Meaning icons drawn on | SP-0307 Line micro-graphics over footage | — |
| DRAW-44 | 👁 | رسوم خطية استعارية تتحرك · Line-art metaphor motions | SP-0307 Line micro-graphics over footage | — |
| DRAW-17 | 📄 | ترجمة بخط اليد تُكتب · Handwritten typewriter caption | SP-0307 Line micro-graphics over footage | — |
| DRAW-39 | 📄 | رسومات الماركر للقصص · Marker-doodle story illustrations | SP-0307 Line micro-graphics over footage | — |
| DRAW-45 | 📄 | قص الرسومات من صفحة الكراسة · Sketch cut-out lift & eraser wipe | SP-0307 Line micro-graphics over footage | — |
| DRAW-57 | 📄 | دراسة أسلوب مرسوم بالتتبع · Rotoscope style study & style pack | SP-0307 Line micro-graphics over footage | — |
| DRAW-P01 | 📄 | قصة الخط الواحد المستمر حتى الشعار · Continuous-line logo story (one stroke → three beats → wordmark loop) | SP-0307 Line micro-graphics over footage | pip:numpy |
| DRAW-28 | ✅ | خطوط بضغط على طريقة perfect-freehand · Pressure strokes & clipped hatching | SP-0308 Pressure strokes & clipped hatching | node |
| DRAW-29 | 🟢 | حبر بصمة بضغط وتظليل · Basma INK pressure strokes & hatching | SP-0308 Pressure strokes & clipped hatching | — |
| DRAW-27 | 📦 | رسم خشن بأسلوب Rough.js · Rough.js / Excalidraw sketch rendering | SP-0308 Pressure strokes & clipped hatching | node |
| DRAW-25 | 📄 | عدم الكمال المقصود · Deliberate imperfection | SP-0308 Pressure strokes & clipped hatching | — |
| DRAW-31 | 📄 | ملمس الرصاص والطباشير بالمرشحات · Pencil & chalk texture filters | SP-0308 Pressure strokes & clipped hatching | — |
| DRAW-40 | 📄 | مشهد الرصاص الهادئ بلون واحد · Quiet pencil one-accent scene | SP-0308 Pressure strokes & clipped hatching | — |
| DRAW-41 | 📄 | إطارات ستوري بورد بالرصاص · Pencil storyboard frames | SP-0308 Pressure strokes & clipped hatching | — |
| DRAW-19 | ✅ | دائرة يدوية مرتعشة · Hand-drawn circle emphasis | SP-0309 Hand-drawn circle emphasis | — |
| DRAW-51 | ✅ | الرسم المطابق تمامًا · Exact-match painting | SP-0309 Hand-drawn circle emphasis | — |
| DRAW-23 | 📦 | علامات rough-notation · Rough-notation marks | SP-0309 Hand-drawn circle emphasis | npm:remotion |
| DRAW-18 | 📄 | أنماط قلم التحديد · Marker emphasis modes | SP-0309 Hand-drawn circle emphasis | — |

## pixel-retro-stylized (motion)

chapter: [pixel-retro-stylized](../powers/pixel-retro-stylized.md) · card: `usip-library/cards/drawing/pixel-retro-stylized.md` · tools: —

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| RETRO-01 | ✅ | مشهد بكسل في ملف HTML واحد · Self-contained pixel cutscene (one HTML) | SP-0363 Pixel VFX by palette-step fades | ffmpeg, node, chromium |
| RETRO-10 | ✅ | هافتون وشاشات CMYK · Halftone & CMYK screens | SP-0363 Pixel VFX by palette-step fades | pip:pillow, npm:hyperframes |
| RETRO-16 | ✅ | CRT وخطوط المسح وVHS · CRT, scanlines & VHS damage | SP-0363 Pixel VFX by palette-step fades | ffmpeg, npm:hyperframes |
| RETRO-22 | ✅ | تحويل المشهد إلى ASCII · ASCII render pass | SP-0363 Pixel VFX by palette-step fades | npm:hyperframes |
| RETRO-03 | 🟢 | عفريتات مقفلة اللوحة ومولّد الوضعيات · Palette-locked sprites & procedural pose generator | SP-0363 Pixel VFX by palette-step fades | pip:pillow |
| RETRO-13 | 🟢 | ملصق مسطّح من صورة (k ألوان) · Flat-paint poster vectorisation (k colours) | SP-0363 Pixel VFX by palette-step fades | pip:opencv |
| RETRO-14 | 📦 | معالجات الصورة الطباعية في HyperFrames · HyperFrames print treatments (engraving, crosshatch, Kuwahara, two-ink, halftone) | SP-0363 Pixel VFX by palette-step fades | npm:hyperframes |
| RETRO-17 | 📦 | لقطات تبدو على شاشة حقيقية · On-screen display & camcorder HUD | SP-0363 Pixel VFX by palette-step fades | npm:gsap, npm:hyperframes |
| RETRO-07 | 👁 | ديوراما بكسل بانعكاس ماء · Pixel diorama with water reflection | SP-0363 Pixel VFX by palette-step fades | — |
| RETRO-15 | 👁 | عالم المانغا: خطوط سرعة وحبر · Manga speed-line burst world | SP-0363 Pixel VFX by palette-step fades | — |
| RETRO-18 | 👁 | لوحة LED نقطية وشريط أخبار · LED dot-matrix ticker | SP-0363 Pixel VFX by palette-step fades | — |
| RETRO-25 | 👁 | تموّج أوب آرت · Op-art concentric moiré | SP-0363 Pixel VFX by palette-step fades | — |
| RETRO-04 | 📄 | مؤثرات بكسل بخطوات اللوحة · Palette-stepped pixel VFX sheets | SP-0363 Pixel VFX by palette-step fades | python3 |
| RETRO-21 | 📄 | تليمتري CRT الداكن · Tactical telemetry / CRT-dark system | SP-0363 Pixel VFX by palette-step fades | — |
| RETRO-23 | 📄 | عائلة الخلايا: LED، ليغو، كروشيه، زجاج مموج · Cell-pattern family: LED, Lego, crochet, fluted glass, threshold matrices | SP-0363 Pixel VFX by palette-step fades | ffmpeg |
| RETRO-31 | 📄 | بذور لوكات الريترو · Retro seed presets (vintage OS, arcade, neobrutalism, neon) | SP-0363 Pixel VFX by palette-step fades | fonts:arabic, npm:axe |
| RETRO-X01 | 📄 | شاشة LED نقطية وكلمات بكسل حقيقية · LED dot lattice bulge and true pixel words | SP-0363 Pixel VFX by palette-step fades | — |
| RETRO-09 | 💡 | فاصل بكسل داخل مونتاج حديث · Pixel chapter break inside a modern edit | SP-0363 Pixel VFX by palette-step fades | ffmpeg |
| RETRO-06 | ✅ | حركة على شبكة صحيحة والرسم على الاثنين · Integer-grid motion & animating on twos | SP-0364 RGB-split glitch word on the beat | — |
| RETRO-28 | ✅ | كلمة غليتش RGB على النوتات · RGB-split glitch word on the beat | SP-0364 RGB-split glitch word on the beat | ffmpeg, npm:hyperframes |
| RETRO-29 | ✅ | ثيمات التايب الحركي المقفلة (J، K، N، Q) · Locked kinetic themes: Brutalist Acid · Retro 70s · Paper Craft · Y2K Chrome | SP-0364 RGB-split glitch word on the beat | — |
| RETRO-26 | 🟢 | تقطيع رقمي قصير للعناصر · DOM glitch stutter (motion-kit) | SP-0364 RGB-split glitch word on the beat | — |
| RETRO-27 | 🟢 | تمريرة غليتش ثلاثية الأبعاد · Analysis-keyed 3D glitch pass | SP-0364 RGB-split glitch word on the beat | npm:three |
| RETRO-19 | 📦 | أثر الأوسيلوسكوب الفوسفوري · Oscilloscope phosphor trace | SP-0364 RGB-split glitch word on the beat | npm:hyperframes |
| RETRO-12 | 📄 | الذكريات على شرائط الفيلم · Memories on film strips | SP-0364 RGB-split glitch word on the beat | imagemagick |
| RETRO-20 | 📄 | سينث ويف / ريترو ويف · Synthwave / retrowave | SP-0364 RGB-split glitch word on the beat | python3, npm:three |
| RETRO-02 | ✅ | الإضاءة والتلاشي بدثر Bayer · Bayer-dither fades & palette-stepped light | SP-0365 Bayer-dither fades & palette-stepped li… | — |
| RETRO-11 | ✅ | ريزوغراف وانزياح الحبر · Risograph misregistration & two-ink print | SP-0365 Bayer-dither fades & palette-stepped li… | ffmpeg, pip:pillow |
| RETRO-24 | ✅ | الدثر المرتب والدثر بالانتشار · Ordered & error-diffusion dither passes | SP-0365 Bayer-dither fades & palette-stepped li… | ffmpeg, node |
| RETRO-08 | 👁 | واجهات ألعاب 8-بت: HUD وحوار وبطاقة عنوان · 8-bit HUD, dialogue box & game title card | SP-0365 Bayer-dither fades & palette-stepped li… | — |
| RETRO-05 | 📄 | البلاطات والبارالاكس · Seamless tiles & parallax rules | SP-0365 Bayer-dither fades & palette-stepped li… | node, chromium |
| RETRO-30 | 📄 | لوفاي دافئ متكرر · Lo-fi / cozy loop | SP-0365 Bayer-dither fades & palette-stepped li… | fonts:arabic |

## shapes-morph-geometry (motion)

chapter: [shapes-morph-geometry](../powers/shapes-morph-geometry.md) · card: `usip-library/cards/drawing/shapes-morph-geometry.md` · tools: `code-drawing-master` · `motion-director` · `motion-engine-js` · `native-3d` · `native-glb` · `smart-draw` · `unified-draw` · `unified-media`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| SHAPE-01 | ✅ | تحويل المسار بإعادة العينات · Seek-safe path morph (MOTION.morphPath) | SP-0397 MorphSVG plugin morph (HyperFrames rule) | npm:gsap |
| SHAPE-03 | ✅ | فائق الإهليلج بحلقات صدى · Superellipse morph with echo rings | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-04 | ✅ | تحويل بدالة قطبية · Polar-function shape morph | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-41 | ✅ | محلل لغة مسارات SVG كاملة · Full SVG path parser (Studio) | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-42 | ✅ | أشكال مركبة بثقوب · Even-odd compound shapes & holes | SP-0397 MorphSVG plugin morph (HyperFrames rule) | pip:pillow |
| SHAPE-43 | ✅ | عدة الأشكال الأساسية ولغة المشهد · Basic shape kit & Step scene language | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-56 | ✅ | زهرة النقاط الذهبية · Phyllotaxis dot flower (137.5°) | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-17 | 🟢 | سلسلة: نقطة → زر → شريط تقدم · Morph chain: dot → button → progress bar → full stop | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-75 | 🟢 | فوانيس ومسجد ونوافذ · Swaying lanterns & mosque silhouette | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-77 | 🟢 | مكتبة 16 أيقونة متجهة · 16-icon vector hero library | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-12 | 📦 | تحول متعدد الأوجه · Facet morph (36 low-poly triangles) | SP-0397 MorphSVG plugin morph (HyperFrames rule) | npm:hyperframes |
| SHAPE-39 | 📦 | الحركة على مسار SVG · Motion along an SVG path | SP-0397 MorphSVG plugin morph (HyperFrames rule) | chromium, npm:gsap |
| SHAPE-88 | 📦 | فاصل بشعرة · Hairline separator (HyperFrames) | SP-0397 MorphSVG plugin morph (HyperFrames rule) | npm:hyperframes |
| SHAPE-05 | 👁 | تحويل المضلعات وأشكال باوهاوس · Polygon / Bauhaus primitive morph | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-06 | 👁 | تحويل بنابض ونجوم تدور · Spring shape morph with orbiting stars | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-07 | 👁 | تحويل بصدى ملون أو أثر ضبابي · Morph with coloured echo / blur trail | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-08 | 👁 | تحويل داخل صندوق أداة تصميم · Design-tool gizmo morph | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-09 | 👁 | تحويل سحابة نقاط إلى أيقونة أو شبكة · Dot-cloud morph (scatter → grid / icon) | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-11 | 👁 | رسم يدوي يصير نظيفًا · Sketch-to-clean morph | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-18 | 👁 | جزيرة ديناميكية وزر ينفتح نافذة · Dynamic-island / button-to-window morph | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-24 | 👁 | الشعار يصير بؤبؤ عين · Logo-to-iris / eye opening | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-02 | 📄 | قانون التحويل: نقاط متساوية واتجاه واحد · Morph law: equal points, same winding | SP-0397 MorphSVG plugin morph (HyperFrames rule) | npm:remotion |
| SHAPE-13 | 📄 | تحويل SVG بإضافة MorphSVG · MorphSVG plugin morph (HyperFrames rule) | SP-0397 MorphSVG plugin morph (HyperFrames rule) | npm:gsap, npm:hyperframes |
| SHAPE-14 | 📄 | أسلوب الأشكال السائلة · Liquid-morph style | SP-0397 MorphSVG plugin morph (HyperFrames rule) | python3, npm:hyperframes |
| SHAPE-15 | 📄 | العنصر المشترك (FLIP) · FLIP / shared-element continuity | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-16 | 📄 | البطاقة كمرساة انتقال · Card-morph anchor handoff | SP-0397 MorphSVG plugin morph (HyperFrames rule) | npm:gsap |
| SHAPE-20 | 📄 | أيقونة القائمة تصير إغلاقًا · Hamburger-to-close morph | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-21 | 📄 | التحول عبر حالات الواجهة · Morph through UI states | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-78 | 📄 | أيقونات SVG حية · Living SVG icons | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-G01 | 📄 | رقم متحرك واحد يقود كل الأشكال · One animated value drives every dependent shape | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-G02 | 📄 | تحويل يطابق الأجزاء المشتركة · Morph that matches shared parts | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-X01 | 📄 | تحوّل هندسي بلا مزج · Geometric morph without a crossfade (letter → planet) | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-X02 | 📄 | لقطة متصلة من عناصر مشتركة · One continuous shot from shared elements | SP-0397 MorphSVG plugin morph (HyperFrames rule) | — |
| SHAPE-92 | 💡 | التصاق مغناطيسي وكل شيء من المركز · Magnet snap spring & centre-origin rule | SP-0397 MorphSVG plugin morph (HyperFrames rule) | npm:remotion |
| SHAPE-52 | ✅ | شبكة بلاطات باوهاوس · Bauhaus tile grid (glyph swap on a distance wave) | SP-0398 Bauhaus tile grid (glyph swap on a dist… | — |
| SHAPE-53 | ✅ | بلاطات تروشيه بموجة تلوين · Truchet tiles with a recolour wave | SP-0398 Bauhaus tile grid (glyph swap on a dist… | — |
| SHAPE-23 | 🟢 | حلقة → قزحية → غمر لوني · Ring → iris → colour flood | SP-0398 Bauhaus tile grid (glyph swap on a dist… | — |
| SHAPE-74 | 🟢 | وردة الفواصل الموسيقية · Interlude rosette (verse template) | SP-0398 Bauhaus tile grid (glyph swap on a dist… | python3 |
| SHAPE-76 | 🟢 | غيمة من دوائر تكبر وتعتم · Circle-cluster cloud that grows and darkens | SP-0398 Bauhaus tile grid (glyph swap on a dist… | — |
| SHAPE-61 | 📦 | كتل أنماط شيدرية وشبكة متحركة · HyperFrames pattern shaders & dynamic grid | SP-0398 Bauhaus tile grid (glyph swap on a dist… | npm:hyperframes |
| SHAPE-54 | 👁 | موجة في شبكة أشكال · Distance-delayed grid wave (rotate / scale / morph) | SP-0398 Bauhaus tile grid (glyph swap on a dist… | — |
| SHAPE-59 | 👁 | كسيريات وزخارف رياضية · Fractals, kolam, golden spiral, kaleidoscope | SP-0398 Bauhaus tile grid (glyph swap on a dist… | — |
| SHAPE-60 | 👁 | جدار أيقونات مائل · Tilted icon wall | SP-0398 Bauhaus tile grid (glyph swap on a dist… | — |
| SHAPE-71 | 👁 | مربع يصير دائرة مع أقمار · Square→circle with satellites & star pop | SP-0398 Bauhaus tile grid (glyph swap on a dist… | — |
| SHAPE-81 | 👁 | ملصقات زخرفية وكبسولات وسوم · Decor stickers, hazard tape & floating tag pills | SP-0398 Bauhaus tile grid (glyph swap on a dist… | — |
| SHAPE-55 | 📄 | بلاطات تنقلب وشريط لا ينتهي · Tile flips & endless strip loops (MG-116/117) | SP-0398 Bauhaus tile grid (glyph swap on a dist… | — |
| SHAPE-62 | 📄 | حلقات دوران بنسب صحيحة · Integer-ratio rotation loops (MG-112/115) | SP-0398 Bauhaus tile grid (glyph swap on a dist… | — |
| SHAPE-79 | 📄 | قواعد الأيقونة: شبكة 24 والإغلاق · Icon rules: 24 px grid & closure | SP-0398 Bauhaus tile grid (glyph swap on a dist… | — |
| SHAPE-89 | 📄 | وحدة 24 وشبكة أعمدة · Base-unit grid system | SP-0398 Bauhaus tile grid (glyph swap on a dist… | — |
| SHAPE-93 | 📄 | أسلوب المرح الهندسي (S07) · Playful geometric style (S07) | SP-0398 Bauhaus tile grid (glyph swap on a dist… | node, chromium |
| SHAPE-66 | ✅ | انفجار خطوط شعاعي · Radial line burst | SP-0399 Radial line burst | — |
| SHAPE-68 | ✅ | أشعة شمسية دوارة · Rotating sunburst ground | SP-0399 Radial line burst | — |
| SHAPE-46 | 🟢 | سلاسل جبال بالإزاحة · Midpoint-displacement mountain ridges | SP-0399 Radial line burst | — |
| SHAPE-50 | 🟢 | خيوط موجية وأشرطة متلوية · Sine strands & ribbon loops | SP-0399 Radial line burst | — |
| SHAPE-51 | 🟢 | خطان قطريان فقط · Exactly two drifting diagonal lines | SP-0399 Radial line burst | npm:three |
| SHAPE-49 | 👁 | خطوط متدفقة ومسارات مخططة · Flowing dashes, striped tubes, dotted trails | SP-0399 Radial line burst | — |
| SHAPE-57 | 👁 | منحنيات ليساجو · Lissajous curves & tangles | SP-0399 Radial line burst | — |
| SHAPE-58 | 👁 | خطوط توليدية بأسلوب Joy Division · Ridge-line generative waves | SP-0399 Radial line burst | — |
| SHAPE-69 | 👁 | حلقة نقاط تتسع بخطوط شعاعية · Expanding dot ring with radial lines | SP-0399 Radial line burst | — |
| SHAPE-83 | 👁 | شريط تظليل مائل خلف النص · Slanted highlighter bar wipe | SP-0399 Radial line burst | — |
| SHAPE-87 | 👁 | بحر خطوط مع شخصية رمزية · Line-art sea with mascot | SP-0399 Radial line burst | — |
| SHAPE-32 | ✅ | نحت بحقول المسافة إلى مجسم مغلق · SDF sculpting to a watertight mesh | SP-0400 Smooth CSG (add / sub / and) | — |
| SHAPE-33 | ✅ | دمج ونحت وتقاطع ناعم · Smooth CSG (add / sub / and) | SP-0400 Smooth CSG (add / sub / and) | — |
| SHAPE-34 | 🟢 | استعلام الحقل لتثبيت العناصر · Field queries for placement | SP-0400 Smooth CSG (add / sub / and) | — |
| SHAPE-45 | 🟢 | أنبوب بنصف قطر متغير · Variable-radius tube (limbs, tails, flames, hair) | SP-0400 Smooth CSG (add / sub / and) | — |
| SHAPE-47 | 👁 | صندوق أيزومتري بثلاث درجات · Three-tone isometric box | SP-0400 Smooth CSG (add / sub / and) | — |
| SHAPE-48 | 👁 | بناء نقطة ثم خط ثم مستوى · Point → line → plane build | SP-0400 Smooth CSG (add / sub / and) | — |
| SHAPE-86 | 👁 | شاشة مقسومة واستعارة الكسوف · Split-screen eclipse metaphor | SP-0400 Smooth CSG (add / sub / and) | — |
| SHAPE-31 | 📄 | أشكال بدوال المسافة · 2D signed-distance shapes (union, morph, glow) | SP-0400 Smooth CSG (add / sub / and) | pip:numpy |
| SHAPE-90 | 📄 | سلالم الأقطار والخطوط والفراغ · Primitive, radius & stroke scales | SP-0400 Smooth CSG (add / sub / and) | — |
| SHAPE-67 | ✅ | حلقة صدمة أرضية ونبض قلب · Shockwave ring & heartbeat ripple | SP-0401 Shockwave ring & heartbeat ripple | — |
| SHAPE-65 | 🟢 | حلقات مدارية إهليلجية · Orbital ellipse rings & accents | SP-0401 Shockwave ring & heartbeat ripple | — |
| SHAPE-10 | 👁 | شريط ينثني فيصير حلقة · Bar bends into a ring | SP-0401 Shockwave ring & heartbeat ripple | — |
| SHAPE-22 | 👁 | نقطة تتفتح إلى واجهة أو نظام · Dot-to-interface / dot-to-system bloom | SP-0401 Shockwave ring & heartbeat ripple | — |
| SHAPE-72 | 👁 | بوابة دوامية ومصباح فرينل · Swirl portal & Fresnel lamp room | SP-0401 Shockwave ring & heartbeat ripple | — |
| SHAPE-38 | 📄 | تموج ضغطة بحرارة · Press ripple with heat bloom | SP-0401 Shockwave ring & heartbeat ripple | — |
| SHAPE-25 | 💡 | نقرة وتحول لعلامة صح · Tap ripple + circle-to-check morph | SP-0401 Shockwave ring & heartbeat ripple | — |
| SHAPE-63 | ✅ | حلقات متحدة المركز بفجوات · Rotating gapped concentric rings | SP-0402 Two-edge stretchy indicator | — |
| SHAPE-91 | 🟢 | انضغاط وتمدد بحفظ المساحة · Area-preserving squash & stretch | SP-0402 Two-edge stretchy indicator | — |
| SHAPE-80 | 📦 | طبقات أشكال وملصقات منبثقة · Shape layers & sticker/emoji pop-ups | SP-0402 Two-edge stretchy indicator | node, fonts:arabic |
| SHAPE-19 | 👁 | مؤشر مطاطي بحافتين · Two-edge stretchy indicator | SP-0402 Two-edge stretchy indicator | — |
| SHAPE-37 | 👁 | إطار مطاطي وقناع قضمة · Rubber-frame strain & bite mask | SP-0402 Two-edge stretchy indicator | — |
| SHAPE-82 | 👁 | مروحة بطاقات وصور · Card / photo / swatch fan-out | SP-0402 Two-edge stretchy indicator | — |
| SHAPE-35 | 🟢 | حقل كتل وبقعة زاوية · Drifting blob field & corner blob | SP-0403 Noise-displaced 3D blob | — |
| SHAPE-73 | 🟢 | الزخرفة الثمانية من الكود · Islamic eight-point rosette builder | SP-0403 Noise-displaced 3D blob | — |
| SHAPE-28 | 📦 | الانقسام اللزج والكتلة الناعمة · Gooey split & soft blob touch (HyperFrames) | SP-0403 Noise-displaced 3D blob | npm:gsap, npm:hyperframes |
| SHAPE-30 | 📦 | كتلة عضوية بضوضاء الرؤوس · Noise-displaced 3D blob | SP-0403 Noise-displaced 3D blob | npm:three |
| SHAPE-36 | 👁 | كتلة متدرجة أو متحولة خلف النص · Gradient / morphing blob behind text | SP-0403 Noise-displaced 3D blob | — |
| SHAPE-84 | 👁 | تغيير لون الكلمة داخل الكرة · Clip-path colour flip over a moving lens | SP-0403 Noise-displaced 3D blob | — |
| SHAPE-27 | ✅ | فلتر اللزوجة · SVG goo / metaball filter | SP-0404 Metaball clay assembly | — |
| SHAPE-85 | 👁 | تجميع من شظايا أو قطع · Shard / piece assembly along a path | SP-0404 Metaball clay assembly | — |
| SHAPE-26 | 💡 | ظرف يتحول لشارة / تجمع إلى شعار · Envelope→badge, converge→monogram, collapse→dot | SP-0404 Metaball clay assembly | — |
| SHAPE-29 | 💡 | تجمع الصلصال بالكرات · Metaball clay assembly | SP-0404 Metaball clay assembly | — |
| SHAPE-44 | 🟢 | منحنيات كاتمول-روم · Catmull-Rom smooth curves | SP-0405 Catmull-Rom smooth curves | — |
| SHAPE-64 | 🟢 | عنقود أقواس مدارية ونواة نابضة · Orbiting arc cluster + pulsing donut core | SP-0405 Catmull-Rom smooth curves | — |
| SHAPE-70 | 👁 | نفق مربعات حلزوني · Spiral square tunnel & nested squares | SP-0405 Catmull-Rom smooth curves | — |
| SHAPE-40 | 📄 | اختيار المنحنى وسرعة ثابتة · Spline choice + arc-length constant speed | SP-0405 Catmull-Rom smooth curves | — |
