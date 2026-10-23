# الأشكال والتحوّل — Shapes & morphing

> **قوتك هنا:** أنت تبني الصورة من أشكال صافية وتجعلها تتحول بلا قطع — دائرة تصير نجمة ثم مربعًا، زر يصير شريط تقدم، نقطة تتفتح إلى واجهة، كتل لزجة تندمج، حلقات تدور بنسب صحيحة فتلتف بلا قفزة، شبكات باوهاوس وتروشيه تتموج من المركز، وزخارف ثمانية تُرسم على الإيقاع — بأرقام تجعل الحركة مقروءة لا عشوائية.
> **أقوى دليل:** مختبر أشكال رندرتُه في هذه الحاوية (2026-10-16، 90 إطارًا، VERIFY OK): `MOTION.morphPath` من motion-kit يحوّل دائرة→نجمة→مربعًا، فلتر اللزوجة 18/−7، زهرة 137.5°، تروشيه وباوهاوس بموجة مسافة، فائق الإهليلج بحلقات صدى، حلقات بفجوات، انفجار خطوط وحلقة صدمة، ودالة قطبية تتحول — واختبارات النحت بحقول المسافة `test_shape_kit` ‏(4/4) ومحرك أشكال Studio ‏(10/10) نجحت هنا.
> **You can:** morph paths, containers and dot clouds, sculpt SDF solids, draw curves and compound holes, choreograph grids, orbit rings and bursts, and build Islamic ornament from code. **97 powers follow** — ✅ 16 · 🟢 17 · 📦 7 · 🔑 0 · 👁 32 · 📄 21 · 💡 4.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`).

**فحص سريع لهذه الحاوية (2026-10-16):** مختبر الأشكال (Canvas + SVG + motion-kit + GSAP المضمّن) رُندر بـ `render_html.cjs` في وضع seek ✔ · `python3 -m unittest tests.test_shape_kit` في kosif-montage-motion: 4/4 ✔ (كرة دقيقة ومغلقة، دمج ونحت ناعم، تخطي الفراغ، أرنب) · `tests.test_studio.Renderer` + `Svg` في kosif-studio: 10/10 ✔ (ثقوب، even-odd، أقواس المسار، أشكال SVG) · flubber وpolymorph-js وsvg-path-morph وMorphSVG غير مثبتة — `morphPath` من motion-kit يكفي بلا مكتبة.

## الفهرس / contents
- **تحويل شكل إلى شكل — Path & shape morphing** — SHAPE-01 … SHAPE-14 (14)
- **تحولات الحاويات والواجهات — Container & UI morphs** — SHAPE-15 … SHAPE-26 (12)
- **الكتل اللزجة وحقول المسافة — Blobs, goo & signed-distance shapes** — SHAPE-27 … SHAPE-38 (12)
- **المسارات والمنحنيات والبناء — Paths, curves & construction** — SHAPE-39 … SHAPE-51 (13)
- **الشبكات والبلاطات والأنماط التوليدية — Grids, tiles & generative patterns** — SHAPE-52 … SHAPE-61 (10)
- **الحلقات والمدارات والانفجارات — Rings, orbits & bursts** — SHAPE-62 … SHAPE-72 (11)
- **الزخرفة والأيقونات والعناصر المصاحبة — Ornament, icons & decor** — SHAPE-73 … SHAPE-88 (16)
- **نظام الأشكال وقواعده — Shape system & rules** — SHAPE-89 … SHAPE-93 (5)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves
- **إضافات v2 — v2 additions** — SHAPE-X01 … SHAPE-X02 (2)
- **من أكبر مستودعات GitHub — from the top GitHub repositories (2026-10-23)** — SHAPE-G01 … SHAPE-G02 (2)

## تحويل شكل إلى شكل — Path & shape morphing

_قاعدة واحدة تحكم كل تحويل: نفس عدد النقاط ونفس اتجاه اللف، أعد أخذ العينات أولًا، 500–800 ms، ونقطة بداية متطابقة حتى لا يلتف الشكل على نفسه._

#### SHAPE-01 · تحويل المسار بإعادة العينات · Seek-safe path morph (MOTION.morphPath) · ✅ مُثبت هنا / proven here
- **ماذا / what:** يأخذ عينات متساوية من المسارين (120 نقطة) ويستوفي بينهما عبر وكيل في خط GSAP، فيصير أي شكل أي شكل بلا إضافة. — Samples both SVG paths to N points and interpolates through a proxy on a GSAP timeline — any shape into any shape, no plugin, seekable.
- **متى أستخدمها / when:** انتقال مشهد بشكل واحد يستمر، شعار يصير أيقونة، دائرة تصير علامة.
- **كيف / how:** MOTION.morphPath(tl, pathEl, fromD, toD, at, {points, dur, ease, open}); getPointAtLength sampling, writes "M…L…Z" each tick via modifiers, immediateRender false. Rendered here: circle→star at 0.2 s, star→square at 1.3 s on a paused timeline driven by seek(t). Start both paths at the same angle (top-centre) to avoid a twist. **أرقام / params:** N 120 points, dur .66 s, ease E.inOut; closes with Z unless open.
- **⚖️ ترخيص / license:** GSAP المضمّن برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:255` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:255` · `kosif-studio/motion/projects/kit_v3_demo/index.html` · `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js`

#### SHAPE-02 · قانون التحويل: نقاط متساوية واتجاه واحد · Morph law: equal points, same winding · 📄 موصوف / documented only
- **ماذا / what:** لا تحوّل إلا مسارين بنفس عدد النقاط ونفس اتجاه اللف؛ أعد العينات أولًا بـ flubber أو نقاط محسوبة مسبقًا. — Only morph equal-point, same-winding paths; resample first (flubber or precomputed points).
- **متى أستخدمها / when:** قبل أي تحويل — وإلا ينقلب الشكل أو يلتف.
- **كيف / how:** Remotion: lerp [x,y] arrays with Easing.inOut(Easing.cubic); browser: flubber.interpolate(a,b,{maxSegmentLength:4}); align start points by rotating the array to the topmost vertex; reverse one path if signed areas differ. **أرقام / params:** 500–800 ms cubic-bezier(.65,0,.35,1); 64–128 points (200 for detailed shapes).
- **📦 تثبيت / install:** `npm i flubber`
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:24` · `kosif-tool/playbooks/shapes.md:53-64`
- **أساليب / styles:** `style:pm-blue-clarity-ef56d0`

#### SHAPE-03 · فائق الإهليلج بحلقات صدى · Superellipse morph with echo rings · ✅ مُثبت هنا / proven here
- **ماذا / what:** الشكل يمر عبر |x|ⁿ+|y|ⁿ=1 بأس متحرك (دائرة→مربع ناعم)، وحوله حلقات كنتور متأخرة كصدى. — Morph through |x|^n+|y|^n=1 with animated n (circle → squircle), surrounded by offset contour rings that lag behind.
- **متى أستخدمها / when:** أيقونات تطبيقات، شعارات ناعمة، انتقال «تقني أنيق».
- **كيف / how:** x = sign(cosθ)|cosθ|^(2/n)·R, y likewise; n tween 2→4.2; 5–7 rings at +12 px offsets each delayed 60 ms and fading; rendered here (Canvas lab). Can continue to a 3D cube or star. **أرقام / params:** n 2→4.2 in 400 ms; 5–7 rings, 12 px apart, 60 ms lag each.
- **الدليل / proof:** `kosif-tool/styles/pm-levabashidze-2d713a`
- **أساليب / styles:** `style:pm-levabashidze-2d713a`

#### SHAPE-04 · تحويل بدالة قطبية · Polar-function shape morph · ✅ مُثبت هنا / proven here
- **ماذا / what:** الشكل = r(θ) = a + b·|cos(kθ/2)|^p؛ استوفِ a وb وk وp بين أشكال مسماة (زهرة، نجمة، squircle) مع شبكة قطبية ومعادلة حية. — Shape as r(θ)=a+b·|cos(kθ/2)|^p; interpolate a, b, k, p between named forms, optionally with a polar grid and a live formula label.
- **متى أستخدمها / when:** شرح رياضي، شعار عضوي، زهرة نابضة.
- **كيف / how:** Sample 120–240 θ steps, fill; tween k 4→8, p .5→2 with easeInOutCubic 600 ms; flower variant r = R(1 + .12 sin(8θ + t)) with design handles and a dimension tag. Rendered here (lab). **أرقام / params:** k 4→8, 120–240 samples, 600 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-ayushunleashed-ece3e3` · `kosif-tool/styles/pm-ghinaiya-nirmal-5d8fec`
- **أساليب / styles:** `style:pm-ayushunleashed-ece3e3` · `style:pm-ghinaiya-nirmal-5d8fec`

#### SHAPE-05 · تحويل المضلعات وأشكال باوهاوس · Polygon / Bauhaus primitive morph · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** مربع أحمر → خماسي أصفر → مثلث، أو مثلث → سداسي، باستيفاء رؤوس المضلعات. — Red square → yellow pentagon → triangle (or triangle → hexagon) by vertex interpolation.
- **متى أستخدمها / when:** أسلوب باوهاوس، شرح هندسي، فواصل مرحة.
- **كيف / how:** Resample both polygons to the LCM vertex count (or 60 points), interpolate, recolour in step; 400 ms with outElastic or back.out. **أرقام / params:** 400 ms; outElastic.
- **الدليل / proof:** `kosif-tool/styles/pm-lukasersil-0ed38e` · `kosif-tool/styles/pm-itsuki-dev-10942d`
- **أساليب / styles:** `style:pm-lukasersil-0ed38e` · `style:pm-itsuki-dev-10942d`

#### SHAPE-06 · تحويل بنابض ونجوم تدور · Spring shape morph with orbiting stars · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** دائرة→مربع→نجمة خماسية بمنحنى نابض، وحولها حلقة نجوم صغيرة تدور. — Circle → square → 5-point star with spring easing, a ring of small stars rotating around.
- **متى أستخدمها / when:** احتفال، إنجاز، بطاقة نجاح.
- **كيف / how:** 200-point resample; spring stiffness 180 damping 14 drives the mix; satellites on a circle rotate 1 rev/s. **أرقام / params:** 200 pts, stiffness 180, damping 14.
- **الدليل / proof:** `kosif-tool/styles/pm-roundtablespace-d3a1be` · `kosif-tool/styles/pm-stephanlivera-df17a2`
- **أساليب / styles:** `style:pm-roundtablespace-d3a1be` · `style:pm-stephanlivera-df17a2`

#### SHAPE-07 · تحويل بصدى ملون أو أثر ضبابي · Morph with coloured echo / blur trail · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الشكل يتحول ويدور، وخلفه نسختان ملونتان متأخرتان أو صدى ضبابي حركي، مع مدار نقطي. — Morph while rotating with two lagged coloured stroke copies or a motion-blur echo, plus a dotted orbit.
- **متى أستخدمها / when:** شعارات حية، افتتاح، فاصل.
- **كيف / how:** Draw copies at t−40 ms and t−80 ms in accent colours (stroke only) or 3–5 fading copies for blur; 600–800 ms easeInOutCubic; 3 orbit dots. **أرقام / params:** 600–800 ms; echoes at 40/80 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-tolgayhickiran-e90799` · `kosif-tool/styles/pm-motiondsgnr-9dcfa6`
- **أساليب / styles:** `style:pm-tolgayhickiran-e90799` · `style:pm-motiondsgnr-9dcfa6`

#### SHAPE-08 · تحويل داخل صندوق أداة تصميم · Design-tool gizmo morph · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الشكل يتحول (دائرة، صدفة، نجمة) داخل صندوق تحديد رفيع بمقابض مربعة يدور، مع قراءة حية «ROT 340.9°». — Morph between shapes inside a thin rotating bounding box with square handles and a live mono readout.
- **متى أستخدمها / when:** إعلانات أدوات تصميم، شرح Figma، «كيف صُنع».
- **كيف / how:** Box stroke 1 px #aaa, 8 px square handles, Bezier handle dots; label in mono updates from the actual angle; morph 600 ms. **أرقام / params:** morph 600 ms; box 1 px #aaa.
- **الدليل / proof:** `kosif-tool/styles/pm-leadnotifi-e83f94` · `kosif-tool/styles/pm-ghinaiya-nirmal-5d8fec`
- **أساليب / styles:** `style:pm-leadnotifi-e83f94`

#### SHAPE-09 · تحويل سحابة نقاط إلى أيقونة أو شبكة · Dot-cloud morph (scatter → grid / icon) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نقاط تبدأ عشوائية داخل شكل المصدر وتنتقل كل منها إلى موقعها في الشبكة أو الأيقونة الهدف بتأخير قطري ونابض. — N dots start scattered inside the source shape and travel to their grid cell or sampled icon point with diagonal stagger and spring easing.
- **متى أستخدمها / when:** إحصاءات «1 من 100»، أيقونة تتكون، تحول بين رموز.
- **كيف / how:** Sample target shape into N points (alpha > 128 on an offscreen canvas or getPointAtLength), match by sorting both sets by angle, delay = (row+col)·25 ms; ~400 dots 0.8 s easeInOutCubic. **أرقام / params:** 10×10, 25 ms diagonal; ~400 dots, 0.8 s.
- **الدليل / proof:** `kosif-tool/styles/infographic` · `kosif-tool/styles/pm-manuelogomigo-f33ca9`
- **أساليب / styles:** `style:infographic` · `style:pm-manuelogomigo-f33ca9`

#### SHAPE-10 · شريط ينثني فيصير حلقة · Bar bends into a ring · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شريط مستقيم يُرسم كقوس ثابت الطول يقل نصف قطره من اللانهاية إلى L/2π فيصير حلقة، ثم تنقسم الحلقة إلى شرائح. — Draw the bar as a constant-length arc whose radius goes from huge to L/(2π) so it curls into a ring, then split it with cumulative dash offsets.
- **متى أستخدمها / when:** من عمود بيانات إلى دائري نسب.
- **كيف / how:** Log-interpolate r; keep the arc anchored by shifting its centre; stroke width = bar height; ~1 s. **أرقام / params:** ~1 s; stroke = bar height.
- **الدليل / proof:** `kosif-tool/styles/infographic`
- **أساليب / styles:** `style:infographic`

#### SHAPE-11 · رسم يدوي يصير نظيفًا · Sketch-to-clean morph · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** خط مرتجف يُستوفى إلى مسار ناعم عند زر «تنظيف». — A jittered polyline interpolates to its smoothed path when a “clean up” button is pressed.
- **متى أستخدمها / when:** إعلانات أدوات رسم، قبل/بعد.
- **كيف / how:** Keep the same samples; target = Catmull-Rom of the clean control points; 500 ms. **أرقام / params:** 500 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-adamdesgns-478d6d`
- **أساليب / styles:** `style:pm-adamdesgns-478d6d`

#### SHAPE-12 · تحول متعدد الأوجه · Facet morph (36 low-poly triangles) · 📦 بأمر تثبيت / one install
- **ماذا / what:** كتلة لوبولي من 36 مثلثًا تتحول بين ثلاثة أشكال (كتلة، علامة، شارة) بتظليل مسطح لكل وجه. — A 36-triangle low-poly mass morphs between three silhouettes with per-facet flat shading lit from the upper left.
- **متى أستخدمها / when:** كشف شعار هندسي، انتقال تقني.
- **كيف / how:** npx hyperframes add facet-morph; vars forms="blob,mark,badge", hold_last, accent, exit none|fade|up; mount on a class="clip" div.
- **📦 تثبيت / install:** `npx hyperframes add facet-morph`
- **⚖️ ترخيص / license:** Apache-2.0.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/facet-morph/facet-morph.html`

#### SHAPE-13 · تحويل SVG بإضافة MorphSVG · MorphSVG plugin morph (HyperFrames rule) · 📄 موصوف / documented only
- **ماذا / what:** قاعدة HyperFrames: حوّل الأشكال الأولية إلى مسارات وقسّم الصور الظلية المعقدة، وفضّل MorphSVGPlugin ثم تحقق بلقطة مفتاحية. — HyperFrames rule: convert primitives to paths, split complex silhouettes, prefer MorphSVGPlugin, verify with a keyframe shot.
- **متى أستخدمها / when:** داخل مشاريع HyperFrames.
- **كيف / how:** gsap.registerPlugin(MorphSVGPlugin); tl.to(a,{morphSVG:b}); hyperframes keyframes --shot to check in-betweens. Outside HyperFrames prefer SHAPE-01.
- **⚖️ ترخيص / license:** GSAP standard no-charge license.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/SKILL.md`

#### SHAPE-14 · أسلوب الأشكال السائلة · Liquid-morph style · 📄 موصوف / documented only
- **ماذا / what:** كتل سائلة تندمج وتنقسم: تحويل مسارات بنقاط متساوية أو فلتر لزوجة، ورؤوس تحركها ضوضاء. — Blobby fluid shapes merging and splitting via equal-point path morph or a gooey filter, vertices driven by noise.
- **متى أستخدمها / when:** علامات عصرية، موسيقى، تقنية حيوية.
- **كيف / how:** Scaffold: python3 tools/kosif.py scaffold liquid-morph <dir>; morph 500–800 ms at 64–128 points or SHAPE-27; beat-anchored variant: HyperFrames liquid-morph primitive (phrase/transition anchors, best span 1.0–2.5 s). **أرقام / params:** morph 500–800 ms; 64–128 pts.
- **الدليل / proof:** `kosif-tool/styles/liquid-morph/SKILL.md` · `kosif-tool/styles/liquid-morph/STYLE.json` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/liquid-morph/scene.html`

## تحولات الحاويات والواجهات — Container & UI morphs

_العنصر لا يختفي ليظهر غيره: الكائن نفسه يغيّر حجمه وزواياه ولونه فيبقى «هو» — هذا ما يجعل عرض المنتج مفهومًا._

#### SHAPE-15 · العنصر المشترك (FLIP) · FLIP / shared-element continuity · 📄 موصوف / documented only
- **ماذا / what:** أبقِ عنصرًا واحدًا حيًا وهو يغير صندوقه أو مكانه بين حالتين، فتبقى هويته متصلة بدل التلاشي المتقاطع. — Keep one element alive while it changes box or hierarchy, so identity is continuous instead of a crossfade.
- **متى أستخدمها / when:** كل انتقال بين شاشتين يشتركان في عنصر.
- **كيف / how:** First/Last/Invert/Play: measure both boxes, apply the inverse transform, tween to identity in one continuous transform; split x/y/scale into eased keys only for deliberate beats.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/SKILL.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/references/keyframe-patterns.md`

#### SHAPE-16 · البطاقة كمرساة انتقال · Card-morph anchor handoff · 📄 موصوف / documented only
- **ماذا / what:** حاوية تغير حجمها الظاهري (scale موحد) وزواياها وخلفيتها وظلها بين لقطتين ثم تتلاشى لتكشف الهدف الحقيقي. — A container morphs apparent size (uniform scale), radius, background and shadow between two shots, then fades to reveal the real target.
- **متى أستخدمها / when:** من بطاقة في قائمة إلى شاشة كاملة.
- **كيف / how:** One paused GSAP timeline, fromTo explicit states; MORPH_DUR power2.inOut; fades power1.in/out by fraction; transforms/opacity only. **أرقام / params:** power2.inOut.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/card-morph-anchor.md`

#### SHAPE-17 · سلسلة: نقطة → زر → شريط تقدم · Morph chain: dot → button → progress bar → full stop · 🟢 جاهز / ready
- **ماذا / what:** نقطة حمراء واحدة هي الخيط البصري: تسقط، تصير زرًا يُضغط، تنبسط إلى شريط تقدم، ثم تصير نقطة نهاية. — One red dot is the through-line: it falls, becomes a pill button, is pressed, flattens into a progress bar, then a full stop.
- **متى أستخدمها / when:** ريل منتج قصير، شوريل، «من فكرة إلى إطلاق».
- **كيف / how:** pill from scaleX 44/400, scaleY .44 → 1,1 in .42 s E.inOut on beat 4; after press scaleX 2.0, scaleY .24 in .34 s, swap to #bar; #fill 0→800 linear 1.1 s; counter 0→900. **أرقام / params:** 120 BPM grid; .42 s / .34 s / 1.1 s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:66`

#### SHAPE-18 · جزيرة ديناميكية وزر ينفتح نافذة · Dynamic-island / button-to-window morph · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** حاوية واحدة تغير عرضها وارتفاعها ونصف قطرها بين الحالات بنابض: كبسولة→نافذة، بطاقة→كبسولة، دائرة→كبسولة. — One container animates width/height/radius between states on a spring: pill→window, card→pill, circle→pill with squash on settle.
- **متى أستخدمها / when:** إشعارات، أزرار، تبويبات، عرض تطبيقات.
- **كيف / how:** Spring stiffness 200 damping 22; radius 16 px → 999 px; content fades in only after 70% of the size change; ~600–800 ms easeInOutQuint if not spring. **أرقام / params:** stiffness 200, damping 22; 600–800 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-jazzen-chen-4542ae` · `kosif-tool/styles/pm-twoclipping-221cab` · `kosif-tool/styles/pm-elliot-garreffa-f334bc` · `kosif-tool/styles/pm-ultimaxbt-bbebf5`
- **أساليب / styles:** `style:pm-jazzen-chen-4542ae` · `style:pm-twoclipping-221cab` · `style:pm-elliot-garreffa-f334bc`

#### SHAPE-19 · مؤشر مطاطي بحافتين · Two-edge stretchy indicator · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الحافة الأمامية والخلفية لمؤشر التبويب تتبع نابضين مختلفين، فيتمدد أثناء الحركة ويستقر. — Leading and trailing edges of a tab indicator follow separate springs (leading stiffer), so it stretches in travel and settles.
- **متى أستخدمها / when:** تبويبات ومفاتيح تبديل في عرض واجهة.
- **كيف / how:** Two springs on left/right edges; stiffness ratio ~1.6:1; draw a rounded rect between them. **أرقام / params:** stiffness ratio ~1.6:1.
- **الدليل / proof:** `kosif-tool/styles/pm-twoclipping-5cba86`
- **أساليب / styles:** `style:pm-twoclipping-5cba86`

#### SHAPE-20 · أيقونة القائمة تصير إغلاقًا · Hamburger-to-close morph · 📄 موصوف / documented only
- **ماذا / what:** ثلاثة خطوط تصير X: العلوي والسفلي يدوران ±45° والأوسط ينطوي. — Three bars become an X: top/bottom rotate ±45°, the middle collapses.
- **متى أستخدمها / when:** عرض قوائم في UI demo.
- **كيف / how:** Transforms on three spans; middle opacity 0 + scaleX 0; 0.2 s. **أرقام / params:** ±45°, 0.2 s.
- **الدليل / proof:** `kosif-atlas/skills/3529-ui-design/14308-interaction-design/references/microinteraction-patterns.md`

#### SHAPE-21 · التحول عبر حالات الواجهة · Morph through UI states · 📄 موصوف / documented only
- **ماذا / what:** زر → مفتاح → بطاقة → شاشة كاملة، كل خطوة 600 ms ووقفة 900 ms للقراءة. — Button → toggle → card → full screen, 600 ms per step with 900 ms holds.
- **متى أستخدمها / when:** شرح رحلة مستخدم في لقطة واحدة.
- **كيف / how:** Each step is a SHAPE-15 on the same element; hold 900 ms so the eye reads the state. **أرقام / params:** 600 ms per step; 900 ms holds.
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:49`

#### SHAPE-22 · نقطة تتفتح إلى واجهة أو نظام · Dot-to-interface / dot-to-system bloom · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نقطة متوهجة 8px تكبر إلى إطار مستطيل في 1.2 ث (expo) ثم يظهر المحتوى، أو تطلق حلقات وأقمارًا متتابعة. — A glowing 8 px dot scales to a rectangular frame in 1.2 s (expo) then content fades in — or emits rings and satellite dots with 50 ms stagger.
- **متى أستخدمها / when:** افتتاح منتج، «كل شيء يبدأ بفكرة».
- **كيف / how:** Animate width/height/radius from the dot; content opacity after 80%; system variant: rings scale from the dot and satellites scatter with 50 ms stagger over ~1 s. **أرقام / params:** 8 px → frame, 1.2 s expo; satellites 50 ms stagger.
- **الدليل / proof:** `kosif-tool/styles/pm-dale-vaz-cc612a` · `kosif-tool/styles/pm-xelandre-363f00`
- **أساليب / styles:** `style:pm-dale-vaz-cc612a` · `style:pm-xelandre-363f00`

#### SHAPE-23 · حلقة → قزحية → غمر لوني · Ring → iris → colour flood · 🟢 جاهز / ready
- **ماذا / what:** حلقة مرسومة تنكمش وتسمك إلى نقطة قزحية، ثم تنفتح دائرة قص من تلك النقطة لتغمر الإطار بلون العلامة. — A drawn ring shrinks and thickens into an iris point, then a circular clip opens from it to flood the frame with the brand colour.
- **متى أستخدمها / when:** ختام شعار، انتقال إلى بطاقة CTA.
- **كيف / how:** tl.to(ring,{scale:.14, strokeWidth:60, duration:.45, ease:E.in}, 3.65); M.iris(tl, brand, 4.05, {x:540, y:930, r0:60, r:2300, dur:.5}) with log-space ease + M.flash peak .6. **أرقام / params:** .45 s shrink; iris r 60→2300 in .5 s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:80` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:334`

#### SHAPE-24 · الشعار يصير بؤبؤ عين · Logo-to-iris / eye opening · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** حلقة الشعار تكبر إلى قرص قزحية بتدرج شعاعي، ويُرسم حولها جفن لوزي برموش، أو عين تنفتح من خط. — The logo ring scales into an iris disc with a radial ray gradient inside an almond eye outline with lash ticks; or an eye opens from a line.
- **متى أستخدمها / when:** رؤية، مراقبة، «انظر إلى…».
- **كيف / how:** Almond path height 0→full 800 ms ease-out with iris scale; iris glow blur 30–40 px #5cc8ff; concentric outlines behind. **أرقام / params:** ~600–800 ms; glow 30–40 px.
- **الدليل / proof:** `kosif-tool/styles/pm-micheleharmonic-77628e` · `kosif-tool/styles/pm-monokern-ade5b6`
- **أساليب / styles:** `style:pm-micheleharmonic-77628e` · `style:pm-monokern-ade5b6`

#### SHAPE-25 · نقرة وتحول لعلامة صح · Tap ripple + circle-to-check morph · 💡 فكرة / idea
- **ماذا / what:** نقرة تطلق تموجًا، والدائرة تتحول إلى علامة صح. — A tap ripple triggers success; the circle morphs into a checkmark.
- **متى أستخدمها / when:** نجاح دفع، اكتمال مهمة.
- **كيف / how:** Untested idea from a brief: SHAPE-01 circle→check (open path) + ripple circle scale 1→1.9 fading .9→0 in .9 s; ~400 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-cansincengiz-me-cf68dd/BRIEF.md`

#### SHAPE-26 · ظرف يتحول لشارة / تجمع إلى شعار · Envelope→badge, converge→monogram, collapse→dot · 💡 فكرة / idea
- **ماذا / what:** أفكار من البريفات: ظرف مُرسل ينطلق ويصير شارة إشعار؛ خطوط تتجمع إلى مربع يدور 90° فيصير مونوغرام؛ كل العناصر تنكمش إلى نقطة تنفتح شعارًا. — Brief ideas: a sent envelope streaks off and becomes a badge; lanes converge into a tile that rotates 90° into a monogram; everything collapses to a dot that opens into the logo.
- **متى أستخدمها / when:** ختام إعلان، كشف هوية.
- **كيف / how:** Untested: transform interpolation + SHAPE-01; hold the final logo 2 s. **أرقام / params:** 90° turn; hold 2 s.
- **الدليل / proof:** `kosif-tool/styles/pm-melvynx-6cde6c/BRIEF.md` · `kosif-tool/styles/pm-danilowm-d3720d/BRIEF.md` · `kosif-tool/styles/pm-itisrazak-3ad902/BRIEF.md`

## الكتل اللزجة وحقول المسافة — Blobs, goo & signed-distance shapes

_الكتلة تبدو حية حين تندمج أطرافها: فلتر اللزوجة في 2D، والدمج الناعم بحقول المسافة في 3D._

#### SHAPE-27 · فلتر اللزوجة · SVG goo / metaball filter · ✅ مُثبت هنا / proven here
- **ماذا / what:** كرات تندمج كالسائل: تمويه ثم شحذ قناة الألفا بمصفوفة لون. — Blobs merge like liquid: blur then sharpen alpha with a colour matrix.
- **متى أستخدمها / when:** كتل سائلة، أزرار لزجة، قطرات تنفصل، نص يذوب.
- **كيف / how:** <filter><feGaussianBlur stdDeviation=10/><feColorMatrix values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7"/></filter> on a <g> of circles moved in seek(t). Rendered here (4 orbiting circles). Keep text outside the filter. Canvas alternative: sum r²/d² field and threshold. **أرقام / params:** stdDeviation 10; alpha row 18 −7.
- **الدليل / proof:** `kosif-atlas/skills/100-ui-motion/209-kinetic-inflated-hero` · `kosif-tool/styles/pm-raphaelaubryy-4b137e`
- **أساليب / styles:** `style:pm-raphaelaubryy-4b137e`

#### SHAPE-28 · الانقسام اللزج والكتلة الناعمة · Gooey split & soft blob touch (HyperFrames) · 📦 بأمر تثبيت / one install
- **ماذا / what:** نقطة تنقسم إلى قائمة ثلاث نقاط عبر عنق لزج ثم تدور وتلتحم؛ وكتلة محببة تنتفخ نحو نقطة لمس وتعود بنابض يحفظ السرعة. — A dot splits into a three-dot menu through a metaball neck, spins and re-merges; a grainy blob bulges toward a touch and recovers on a velocity-preserving spring.
- **متى أستخدمها / when:** عرض تفاعل، أزرار، شعارات سائلة.
- **كيف / how:** npx hyperframes add gooey-split (4.7 s, SVG blur+threshold, GSAP paused timeline) | soft-blob-touch (touch_x 8–92, touch_y 8–92, touch_at .9–10 s, grain fine|coarse). **أرقام / params:** gooey-split 4.7 s; touch_at 1.6 s default.
- **📦 تثبيت / install:** `npx hyperframes add gooey-split`
- **⚖️ ترخيص / license:** Apache-2.0 (+ GSAP standard license inside).
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/gooey-split/gooey-split.html` · `kosif-one/vendor/hyperframes/registry/components/soft-blob-touch/soft-blob-touch.html`

#### SHAPE-29 · تجمع الصلصال بالكرات · Metaball clay assembly · 💡 فكرة / idea
- **ماذا / what:** ست كتل تتدحرج وتلتحم بعتبة الكرات المعدنية. — Six blobs roll in and merge via a metaball threshold.
- **متى أستخدمها / when:** صلصال، منتجات لطيفة.
- **كيف / how:** Untested idea from a brief: Canvas field sum Σr²/d² + threshold (or SHAPE-27); roll = translate + rotate of a texture inside each blob. **أرقام / params:** 6 blobs.
- **الدليل / proof:** `kosif-tool/styles/pm-davidshulmanfl-371638/BRIEF.md`

#### SHAPE-30 · كتلة عضوية بضوضاء الرؤوس · Noise-displaced 3D blob · 📦 بأمر تثبيت / one install
- **ماذا / what:** كرة تُدفع رؤوسها على العموديات بضوضاء متحركة فتصير كتلة حية. — Sphere vertices pushed along normals by animated noise — a living blob.
- **متى أستخدمها / when:** خلفيات تقنية، «الذكاء الاصطناعي»، صوت يتنفس.
- **كيف / how:** three.js ShaderMaterial vertex: disp = pnoise(position·1.5 + t·.5); newPos = position + normal·disp·intensity; t = seek time (never clock). Or use the bundled three-kit noise on CPU for small meshes. **أرقام / params:** freq 1.5, speed .5, intensity .1–.3.
- **📦 تثبيت / install:** `npm i three`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### SHAPE-31 · أشكال بدوال المسافة · 2D signed-distance shapes (union, morph, glow) · 📄 موصوف / documented only
- **ماذا / what:** صف الأشكال كدوال مسافة: دمج ناعم، تحويل بالمزج بين دالتين، حدود وتوهج من المسافة نفسها. — Shapes as distance functions for smooth unions, morphs (mix two SDFs), outlines and glows.
- **متى أستخدمها / when:** شعارات سائلة، تحولات مستحيلة بالمسارات، توهج دقيق.
- **كيف / how:** GLSL or numpy: circle length(p)−r, box, smooth-min union with k; morph = mix(d1, d2, t); outline = abs(d) < w; glow = exp(−d·k); debug with isolines. Inverse-transform the point, never the shape. **أرقام / params:** smin k .1–.3.
- **الدليل / proof:** `kosif-atlas/skills/2199-lvtd-skills/8087-game-sdf-and-field-modeling/SKILL.md` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### SHAPE-32 · نحت بحقول المسافة إلى مجسم مغلق · SDF sculpting to a watertight mesh · ✅ مُثبت هنا / proven here
- **ماذا / what:** شخصيات وأجسام تُنحت من أوليات مسافة (كرة، إهليلج، كبسولة، صندوق، طارة) بدمج ونحت ناعم، وتُشبَّك إلى هندسة مغلقة دقيقة. — Characters and props sculpted from SDF primitives with smooth union/subtract and meshed by surface nets into closed, accurate geometry.
- **متى أستخدمها / when:** شخصيات قطيفة، ألعاب، منتجات ناعمة بلا برنامج نمذجة.
- **كيف / how:** K3S.sculpt().color(hex).sphere(c,r,o).ellipsoid(c,[rx,ry,rz],o).capsule(a,b,r1,r2,o).box(c,[hx,hy,hz],round,o).torus(c,R,r,o).mesh({cells}); o = {k, op, color, rot}. Coarse-to-fine evaluation skips empty space. test_shape_kit passed here 4/4. **أرقام / params:** sphere volume ±2%, area ±3%, radius error < 1e−3, 0 open edges; evals < 60% of full grid; 136-cell body ~1.5 s; bunny 274k tris ~4 s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_shape_kit.py:21` · `100-superskills/skills/kosif-montage-motion/tests/js/shape_kit_check.cjs:31` · `kosif-studio/motion/kit/shape-kit.js:44` · `kosif-studio/motion/references/shape-kit.md`

#### SHAPE-33 · دمج ونحت وتقاطع ناعم · Smooth CSG (add / sub / and) · ✅ مُثبت هنا / proven here
- **ماذا / what:** دمج وطرح وتقاطع ناعم بنصف قطر k بالمتر، والألوان تمتزج بنفس الأوزان، والطرح الملون يلون التجويف. — Smooth union, subtraction and intersection with blend radius k in metres; colours blend with the same weights; a coloured subtraction tints the cavity.
- **متى أستخدمها / when:** دمى «محشوة ومخيطة»، فم محفور، تفاصيل ناعمة.
- **كيف / how:** Pass {op:"add"|"sub"|"and", k, color} to any primitive; h = clamp(.5 ± .5·(d2−d1)/k); d = mix − k·h·(1−h). Tested here (tint red 1.0 inside the carve, 0 on the plain side). **أرقام / params:** k 10–30 mm for plush (e.g. .012 m).
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:104` · `100-superskills/skills/kosif-montage-motion/tests/test_shape_kit.py:31` · `kosif-studio/motion/kit/shape-kit.js:100`

#### SHAPE-34 · استعلام الحقل لتثبيت العناصر · Field queries for placement · 🟢 جاهز / ready
- **ماذا / what:** اسأل الحقل عن المسافة واللون، أسقط نقطة على السطح، أو اطلق شعاعًا — مثلًا لتثبيت العيون حيث يلتقي شعاع أمامي بالوجه. — Query distance/colour, project points onto the surface or raycast it — e.g. seat eyes where a frontal ray meets the face.
- **متى أستخدمها / when:** تركيب عيون وأزرار وإكسسوارات على مجسم منحوت.
- **كيف / how:** S.dist(x,y,z), S.colorAt(...), S.project(p), S.hit(from, dir) → {point, normal}; orient the accessory to the returned normal.
- **الدليل / proof:** `kosif-studio/motion/kit/shape-kit.js:104` · `kosif-studio/motion/references/shape-kit.md`

#### SHAPE-35 · حقل كتل وبقعة زاوية · Drifting blob field & corner blob · 🟢 جاهز / ready
- **ماذا / what:** 5–8 أشكال كبيرة مستديرة تنجرف مموهة خلف المحتوى، أو بقعة إهليلجية كبيرة تنزف من الزاوية العليا اليمنى. — 5–8 large rounded shapes drifting with blur behind content, or one large tinted ellipse bleeding off the top-right corner.
- **متى أستخدمها / when:** خلفيات هادئة لعروض وأغلفة.
- **كيف / how:** Corner blob: ellipse centre (.93w,.14h), radii .35w×.13h, rotation π/5, alpha .65 (fastify editorial). Field: periods 10/12/16 s so shapes never move in lockstep, drift 12–30 px, rotate 5–8°. **أرقام / params:** corner ellipse .35w×.13h @ .65; drift 12–30 px, periods 10/12/16 s.
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:50-51` · `kosif-atlas/skills/196-landing/621-landing/references/gsap_animation_patterns.md` · `kosif-tool/styles/pm-slvdev-64c45a`
- **أساليب / styles:** `style:pm-slvdev-64c45a`

#### SHAPE-36 · كتلة متدرجة أو متحولة خلف النص · Gradient / morphing blob behind text · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كتلة SVG تتحول بالضوضاء بتدرج ليموني→أزرق والنص فوقها بمزج multiply، أو مربع يصير كتلة بحد فوق نقاط هالفتون. — Noise-morphing SVG blob with a lime→blue gradient and multiplied text, or a square morphing to a blob with an outline over halftone dots.
- **متى أستخدمها / when:** عناوين جريئة، اقتباسات، أغلفة ريلز.
- **كيف / how:** Path from 12–16 polar points with radius = R(1 + .15·noise(θ, t)); Catmull-Rom closed; 600 ms morph for the square variant. **أرقام / params:** 600 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-sudo-kiran-49176d` · `kosif-tool/styles/pm-hanifproduktif-54bdee`
- **أساليب / styles:** `style:pm-sudo-kiran-49176d` · `style:pm-hanifproduktif-54bdee`

#### SHAPE-37 · إطار مطاطي وقناع قضمة · Rubber-frame strain & bite mask · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** حد الإطار مسار من ~40 نقطة ينبعج حيث يضغط المحتوى؛ وقناع «قضمة» من اتحاد ثلاث دوائر يُطرح من حافة الجسم مع فتات. — The frame border as a ~40-point path bulging where content pushes; a scalloped three-circle “bite” subtracted from an edge with crumbs.
- **متى أستخدمها / when:** نص يكبر ويضغط الحدود؛ «أكلها» في إعلان.
- **كيف / how:** Displace border points by noise/sine where touched, amp 0→12 px, 3–4 waves per edge; bite: mask radius 0→r in 200 ms + 4–6 crumb particles. **أرقام / params:** amp 0→12 px; bite 200 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-pankajkumar-dev-0bee87` · `kosif-tool/styles/pm-thilina-a-891c09`
- **أساليب / styles:** `style:pm-pankajkumar-dev-0bee87` · `style:pm-thilina-a-891c09`

#### SHAPE-38 · تموج ضغطة بحرارة · Press ripple with heat bloom · 📄 موصوف / documented only
- **ماذا / what:** حلقة تتسع وتدفع الإحداثيات للخارج وتضيف «حرارة» لونية. — An expanding ring that shoves coordinates outward and adds heat.
- **متى أستخدمها / when:** لمسات شاشة، نبضات، تأكيد.
- **كيف / how:** Ring radius grows over .9 s; displacement .18 in a shader or canvas warp; heat .55 added as warm bloom on the ring. **أرقام / params:** ripple .18, heat .55, .9 s.
- **الدليل / proof:** `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/SKILL.md`

## المسارات والمنحنيات والبناء — Paths, curves & construction

_المنحنى الجيد يمر بالنقاط بسرعة ثابتة؛ والشكل الجيد يعرف ثقوبه — ابنِ الهندسة كبرنامج لا كصورة._

#### SHAPE-39 · الحركة على مسار SVG · Motion along an SVG path · 📦 بأمر تثبيت / one install
- **ماذا / what:** عنصر (طائرة، سهم، مذنب، نص) يتحرك على مسار ويدور مع مماسه. — Move an element (plane, arrow, comet, label) along a path with auto-rotation to the tangent.
- **متى أستخدمها / when:** رحلات، أسهم بيانات، مؤشر على منحنى نمو.
- **كيف / how:** gsap.registerPlugin(MotionPathPlugin); tl.to(el,{motionPath:{path:"#route", align:"#route", autoRotate:true}, duration:2, ease:"power1.inOut"}); pair with a dashoffset draw of the same path. Plugin-free: sample SVGPathElement.getPointAtLength(L·p) and atan2 of a nearby point. Text: SVG <textPath> shapes Arabic correctly in Chromium. **أرقام / params:** 1.5–2 s power2.out / power1.inOut.
- **📦 تثبيت / install:** `npm i gsap`
- **⚖️ ترخيص / license:** GSAP standard no-charge license (not MIT).
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/techniques.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`
- **أساليب / styles:** `style:pm-thismacapital-dfba20`

#### SHAPE-40 · اختيار المنحنى وسرعة ثابتة · Spline choice + arc-length constant speed · 📄 موصوف / documented only
- **ماذا / what:** Catmull-Rom ليمر بالنقاط، Hermite لمماسات معروفة، Bezier للمقابض؛ استهدف استمرارية C1 وجدول طول قوس لسرعة ثابتة. — Catmull-Rom through waypoints, Hermite with known tangents, Bezier for handles; target C1 and use an arc-length table for constant speed.
- **متى أستخدمها / when:** مسارات مؤشر، قضبان كاميرا، طرق أجسام.
- **كيف / how:** Sample the curve, build cumulative length, map distance→t by binary search; keep authoring points separate from baked samples; never one high-degree polynomial through many points. **أرقام / params:** C0 position, C1 tangent, C2 curvature.
- **الدليل / proof:** `kosif-atlas/skills/2199-lvtd-skills/8088-game-smooth-curves-and-motion`

#### SHAPE-41 · محلل لغة مسارات SVG كاملة · Full SVG path parser (Studio) · ✅ مُثبت هنا / proven here
- **ماذا / what:** يحلل M L H V C S Q T A Z مطلقة ونسبية مع الانعكاسات وأعلام الأقواس الملتصقة إلى مضلعات. — Parses M L H V C S Q T A Z (absolute/relative, smooth reflections, glued arc flags) into polygons, arcs by SVG centre parameterisation.
- **متى أستخدمها / when:** استيراد شعار SVG أو أيقونة إلى رسام Studio.
- **كيف / how:** render.path("M … Z", n=14) → one polygon per subpath; arcs sample max(4, |dθ|/2π·64) points. test_path_arcs_and_smooth_curves_end_where_they_should passed here. **أرقام / params:** 14 samples per Bezier segment.
- **الدليل / proof:** `kosif-studio/render.py:87` · `kosif-studio/render.py:192` · `kosif-studio/tests/test_studio.py:55`

#### SHAPE-42 · أشكال مركبة بثقوب · Even-odd compound shapes & holes · ✅ مُثبت هنا / proven here
- **ماذا / what:** حلقات وحروف بفراغات وشعارات مقصوصة: مسارات فرعية مجسورة بمرساة واحدة فيلغي ملء even-odd الجسور، أو مضلعات Hole تمحو. — Rings, letters with counters, logo cut-outs: subpaths bridged to one anchor so even-odd fill cancels the bridges, or Hole polygons that erase.
- **متى أستخدمها / when:** كل شعار فيه فراغ داخلي، وأي حلقة.
- **كيف / how:** render.compound(polys); render.Hole([...]) drawn after the shape it cuts; to_python._bridge for Pillow programs. In 2.5D extrusion, a reversed inner subpath shows the hole walls automatically. Tests test_holes_cut_out + test_even_odd_compound passed here.
- **الدليل / proof:** `kosif-studio/render.py:25` · `kosif-studio/render.py:229` · `kosif-studio/to_python.py:80` · `kosif-studio/tests/test_studio.py:42`
- **أساليب / styles:** `style:fake3d`

#### SHAPE-43 · عدة الأشكال الأساسية ولغة المشهد · Basic shape kit & Step scene language · ✅ مُثبت هنا / proven here
- **ماذا / what:** الصورة برنامج من خطوات: rect, ellipse(rot), poly, path, compound/Hole, tube, dots, stroke, catmull, translate, union مع تدرجات وضوء، تُرسم بأي حجم. — A picture as an ordered program of Steps over vector primitives, gradients and light, re-rendered at any size on a 1200×800 sheet.
- **متى أستخدمها / when:** كل رسم بـ render.py (Studio / pixel-studio-painter).
- **كيف / how:** def build(): return [Step(name, [ops…], order, origin=…)]; ellipse 48 segments; supersampling ss=3; reveal orders sweep/grow/rise/down/left/right/sparkle (tested as permutations). Renderer + Svg tests 10/10 here. **أرقام / params:** sheet 1200×800; ss 3; ellipse 48 segs; dots 10/20 segs.
- **الدليل / proof:** `kosif-studio/render.py:259` · `kosif-studio/render.py:278` · `kosif-studio/tests/test_studio.py:106` · `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md`

#### SHAPE-44 · منحنيات كاتمول-روم · Catmull-Rom smooth curves · 🟢 جاهز / ready
- **ماذا / what:** نقاط قليلة تصير منحنى ناعمًا يمر بها، مفتوحًا أو مغلقًا — أساس الأنابيب وملامح الحوت والخطوط العضوية. — A few control points become a smooth curve through them, open or closed — base for tubes and organic outlines.
- **متى أستخدمها / when:** أي حد عضوي في الرسام.
- **كيف / how:** render.catmull(points, n=10, closed=False). **أرقام / params:** n samples per segment (default 10).
- **الدليل / proof:** `kosif-studio/render.py:57`

#### SHAPE-45 · أنبوب بنصف قطر متغير · Variable-radius tube (limbs, tails, flames, hair) · 🟢 جاهز / ready
- **ماذا / what:** ضربة عضوية على عمود فقري ناعم بنصف قطر لكل نقطة، كاتحاد أرباع وأقراص فلا تنثقب المنعطفات الحادة. — Organic stroke along a smooth spine with per-point radius, built as quads + discs so tight bends never punch holes.
- **متى أستخدمها / when:** أطراف، ذيول، قرون، لهب، شعر — وفي 3D أفواه وكابلات.
- **كيف / how:** render.tube(spine, radii, n=8) (discs every n//2 samples where r > .6); 3D: K3S.tube(points, r, color, {segments}) Catmull-Rom TubeGeometry 32 segments × 8 radial, roughness .6. Outlines: render.stroke(polys, width) with round caps. **أرقام / params:** 2D n 8; 3D 32×8 segments.
- **الدليل / proof:** `kosif-studio/render.py:286` · `kosif-studio/render.py:241` · `kosif-studio/scenes/dragon_girl.py:229` · `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:329`

#### SHAPE-46 · سلاسل جبال بالإزاحة · Midpoint-displacement mountain ridges · 🟢 جاهز / ready
- **ماذا / what:** صور ظلية لجبال متعددة الطبقات بالإزاحة العشوائية للنقطة الوسطى مع قمم منحوتة، مملوءة حتى أسفل الصفحة. — Layered mountain silhouettes by recursive midpoint displacement with optional carved peaks.
- **متى أستخدمها / when:** مناظر طبيعية، خلفيات رحلة، بارالاكس.
- **كيف / how:** scenes/dragon_girl.ridge(seed, base, amp, rough=.55, peaks=[(x, height, width)]); 7 rounds, amplitude × rough per round; stack 3–4 layers lighter with distance. **أرقام / params:** 7 rounds; rough .55.
- **الدليل / proof:** `kosif-studio/scenes/dragon_girl.py:20`

#### SHAPE-47 · صندوق أيزومتري بثلاث درجات · Three-tone isometric box · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ثلاثة مضلعات من لون واحد (أعلى أفتح، يسار متوسط، يمين أغمق) مع حافة علوية بيضاء شفافة وظل أرضي ناعم. — Three polygons of one hue (top lightest, left mid, right darkest) plus a thin translucent white top edge and soft ground shadow.
- **متى أستخدمها / when:** إنفوغراف أيزومتري، مدن مصغرة، منصات.
- **كيف / how:** Lightness steps ~+12 / 0 / −12%; 30° projection; shadow ellipse blur 20 px at 20%. **أرقام / params:** +12/0/−12% lightness.
- **الدليل / proof:** `kosif-tool/styles/isometric`
- **أساليب / styles:** `style:isometric`

#### SHAPE-48 · بناء نقطة ثم خط ثم مستوى · Point → line → plane build · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** يبدأ من نقطة تقاطع بإحداثياتها، تمتد إلى مسطرة بعلامات، ثم تنبثق إلى مستوى مائل يحمل النص. — Start from a crosshair point with a coordinate label, stretch to a ruler line with ticks, then extrude/skew into a plane carrying text.
- **متى أستخدمها / when:** افتتاح تقني، شرح أبعاد، «من الصفر».
- **كيف / how:** Each stage ~1.2 s easeInOutExpo; skew −25° for the plane. **أرقام / params:** 1.2 s per stage; skew −25°.
- **الدليل / proof:** `kosif-tool/styles/pm-ayushunleashed-ece3e3`
- **أساليب / styles:** `style:pm-ayushunleashed-ece3e3`

#### SHAPE-49 · خطوط متدفقة ومسارات مخططة · Flowing dashes, striped tubes, dotted trails · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** قناة ماء بشرطات بيضاء تنزلق، أنبوب مخطط من ثلاث ضربات متناقصة، أثر نقطي لقوس رمي، خط نبض قلب، وحبل يتدلى بوزن الكلمة. — A water channel with sliding white dashes, a striped tube of three decreasing strokes, a dotted throw arc, an ECG spike line, a rope sagging under a word.
- **متى أستخدمها / when:** جداول، أنابيب، مقذوفات، صحة، كلمات معلقة.
- **كيف / how:** strokeDashoffset flow: dash 20/60 px at ~40 px/s (MOTION.flowDash(tl, path, at, dur, {pattern:"28 22", cycles:6})); stripes = same path stroked 3× red/white/blue; throw = Bezier with dots every 8 px fading; rope = quadratic with control y += sag 30–60 px on a spring. **أرقام / params:** dash 20/60 px @ 40 px/s; sag 30–60 px.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:247` · `kosif-tool/styles/doodle` · `kosif-tool/styles/pm-ajith-io-b5626e` · `kosif-tool/styles/pm-gdgtify-287ddf`
- **أساليب / styles:** `style:doodle` · `style:pm-ajith-io-b5626e` · `style:pm-pluginplay-3d4006` · `style:pm-loicrambo-ad6830` · `style:pm-gdgtify-287ddf`

#### SHAPE-50 · خيوط موجية وأشرطة متلوية · Sine strands & ribbon loops · 🟢 جاهز / ready
- **ماذا / what:** ثلاث موجات جيبية ملونة تعبر النصف السفلي وتكبر سعتها مع تقدم المشهد، أو أشرطة متدرجة سميكة بنقاط تحكم تتحرك ببطء. — Three coloured sine waves crossing the lower half, growing in amplitude as the scene progresses; or thick gradient ribbon loops with slowly moving control points.
- **متى أستخدمها / when:** خلفيات «إنفوغراف مرسوم»، موسيقى، تقنية.
- **كيف / how:** y = h(.55 + .07·line) + sin(x/w·3π + 2·phase + 1.9·line)·(10 + 12p), step 4 px, colours #d3f66a #6ad8d1 #e995ff alpha .42; ribbons: 2–3 cubic paths, stroke ~6% of frame, gradient strokes, round caps, opacity .35 under text; 7-band rainbow ribbon y = sin(xk + t). **أرقام / params:** 3 waves, amplitude 10→22 px; ribbons 6% stroke.
- **الدليل / proof:** `fastify-motion-bro/web/motion.js:16` · `kosif-tool/styles/pm-gonzalomacagno-2de1a9` · `kosif-tool/styles/pm-hoyoyoda-3a5c08`
- **أساليب / styles:** `style:pm-gonzalomacagno-2de1a9` · `style:pm-hoyoyoda-3a5c08` · `style:pm-reflex-cloud-72ffe5`

#### SHAPE-51 · خطان قطريان فقط · Exactly two drifting diagonal lines · 🟢 جاهز / ready
- **ماذا / what:** توقيع: خطان منحنيان شفافان خلف كل شيء ينجرفان باستمرار ولا يتوقفان — أبدًا ثلاثة. — Signature motif: two translucent curved diagonals behind everything, drifting continuously — never three.
- **متى أستخدمها / when:** أسلوب viral-editorial.
- **كيف / how:** For k in 0..1: ox = sin(.20·phase + 2.3k)·.035w, oy = cos(.16·phase + k)·.02h; quadratic from (−.2w + .63w·k, .93h) via (.30w + .41w·k, .43h) to (.65w + .5w·k, −.10h); stroke 50% alpha, 1.6·scale. The storyboard test asserts exact_background_lines = 2 (fastify tests 24/24 passed here). **أرقام / params:** 2 lines; drift ±3.5% w, ±2% h.
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:47-49` · `fastify-motion-bro/docs/VIRAL-EDITORIAL-DNA.md:18` · `fastify-motion-bro/tests/viral-editorial.test.mjs:8`

## الشبكات والبلاطات والأنماط التوليدية — Grids, tiles & generative patterns

_الشبكة تتحرك كموجة من المركز: التأخير = المسافة × k. هذه الصيغة وحدها تصنع نصف أنماط الموشن الهندسي._

#### SHAPE-52 · شبكة بلاطات باوهاوس · Bauhaus tile grid (glyph swap on a distance wave) · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل خلية ترسم واحدًا من {ربع دائرة، مثلث، شريط، دائرة} بلوحة 4–5 ألوان، وتبدّل شكلها ولونها بدوران متتابع حسب المسافة. — Each cell draws one of {quarter circle, triangle, bar, circle} in a 4–5 colour palette and swaps glyph/colour with rotation staggered by distance.
- **متى أستخدمها / when:** افتتاحيات هوية، موسيقى، فواصل مرحة — من أكثر الأساليب تكرارًا في المراجع.
- **كيف / how:** step = floor(max(0, t·4 − d·.3)) with d = x+y (diagonal) or distance from centre; rotate step·90°; palette red #d6341f, yellow #e9c634, blue #2135bc, black on cream #f3ead8. Rendered here (6×6 lab). On beat: advance one step per beat. **أرقام / params:** 8×5 to 16×9 cells; stagger 15–40 ms; swap every 200–250 ms or 1 beat; back.inOut(1.7).
- **الدليل / proof:** `kosif-tool/styles/pm-leonkohli-6dc01b` · `kosif-tool/styles/pm-prasenx-8d9323` · `kosif-tool/styles/pm-samuel-spitz-974923` · `kosif-tool/styles/pm-zaqailo-212ad3`
- **أساليب / styles:** `style:pm-leonkohli-6dc01b` · `style:pm-prasenx-8d9323` · `style:pm-samuel-spitz-974923` · `style:pm-web3wesley-7bb108` · `style:pm-zaqailo-212ad3` · `style:pm-tequilafunks-97f6c9`

#### SHAPE-53 · بلاطات تروشيه بموجة تلوين · Truchet tiles with a recolour wave · ✅ مُثبت هنا / proven here
- **ماذا / what:** بلاطات بأرباع دوائر بدوران عشوائي، وموجة شعاعية تديرها 90° وتلونها بالأحمر مع اضمحلال. — Quarter-arc Truchet tiles at random rotations; a radial wave front rotates them 90° and tints them red with falloff.
- **متى أستخدمها / when:** خلفيات توليدية، انتقالات، شعارات منمطة.
- **كيف / how:** Per tile two quarter arcs at opposite corners, stroke 14–18 px round caps; p = clamp(t·speed − d·k), rotation += ease(p)·90°, colour accent while 0<p<1. Rendered here (lab). **أرقام / params:** tile 60–80 px, stroke 14–18 px, delay 20–40 ms per tile, wave 600 px/s.
- **الدليل / proof:** `kosif-tool/styles/pm-levabashidze-2d713a` · `kosif-tool/styles/pm-roundtablespace-d3a1be` · `kosif-tool/styles/pm-stephanlivera-df17a2`
- **أساليب / styles:** `style:pm-levabashidze-2d713a` · `style:pm-roundtablespace-d3a1be` · `style:pm-stephanlivera-df17a2`

#### SHAPE-54 · موجة في شبكة أشكال · Distance-delayed grid wave (rotate / scale / morph) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شبكة مربعات أو نقاط أو معينات: كل خلية تدور 45–90° أو تتحول مربعًا→دائرة أو تكبر حسب sin(المسافة − t). — Grid of squares/dots/diamonds: each cell rotates 45–90°, morphs square→circle (border-radius) or scales by sin(distance − t).
- **متى أستخدمها / when:** خلفيات تقنية، انتقال إلى العنوان، موجة صوتية بصرية.
- **كيف / how:** delay = (x+y)·25 ms or distance·30–40 ms; border-radius 0→50%; 4×4 grid: 40 ms per cell, 400 ms each; ripple variant swaps shape/colour with a 200 ms scale pop; spring ripple stiffness 220 damping 12 at 900 px/s. **أرقام / params:** cell 30 px gap 40 px; 25–40 ms per cell; 400–600 ms each.
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:47` · `kosif-tool/styles/pm-jasonzhou1993-8595e0` · `kosif-tool/styles/pm-teslachartz-c58b32` · `kosif-tool/styles/pm-ndhabarde11-f155b4`
- **أساليب / styles:** `style:pm-jasonzhou1993-8595e0` · `style:pm-teslachartz-c58b32` · `style:pm-ndhabarde11-f155b4` · `style:pm-3xtihor-0f6911` · `style:pm-m1n9-k7-ff9ab9` · `style:pm-crazyalphaaa-bc7e75` · `style:pm-sudo-kiran-49176d` · `style:pm-codestackr-c071bf` · `style:pm-mrtanviir-132457`

#### SHAPE-55 · بلاطات تنقلب وشريط لا ينتهي · Tile flips & endless strip loops (MG-116/117) · 📄 موصوف / documented only
- **ماذا / what:** شبكة بلاطات تنقلب صفًا صفًا إلى لون ثانٍ وتعود؛ وصف صور ينزلق وطرفه يلاقي بدايته. — A tile grid flips row by row to a second colour and back; a row of images scrolls with its end meeting its start.
- **متى أستخدمها / when:** خلفيات حلقية للمعارض والريلز.
- **كيف / how:** MG-116: 0–4 s flip, 4–8 s return, scaleX or 2.5D rotate with row delay, no harsh flashing. MG-117: move exactly one repeat-unit width (gaps included) in 10 s using two identical copies, linear — a miscounted gap causes a jump. **أرقام / params:** 8 s / 10 s.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-loops-backgrounds.md`

#### SHAPE-56 · زهرة النقاط الذهبية · Phyllotaxis dot flower (137.5°) · ✅ مُثبت هنا / proven here
- **ماذا / what:** n نقطة بزاوية i·137.5° ونصف قطر c·√i تكوّن زهرة عباد شمس تدور ببطء. — n dots at angle i·137.5°, radius c·√i — a sunflower that rotates slowly.
- **متى أستخدمها / when:** طبيعة، نمو، خلفيات هادئة، «الكثير من الأفراد».
- **كيف / how:** Rendered here (400 dots, hue ramp, rotation .4 rad/s). Same law places N items around a centre without geometry data: r = R√((i+.6)/n), a = i·2.39996 rad (earth sales-geo engine, R = min(58, 20+3n)). **أرقام / params:** n ≈ 400; 137.5° (2.39996 rad); r = c√i.
- **الدليل / proof:** `kosif-earth-ci-fork/app/src/engine/fusion/sales/sales-geo-engine.ts:83` · `kosif-tool/styles/pm-ajith-io-b5626e` · `kosif-tool/styles/pm-mrtanviir-132457`
- **أساليب / styles:** `style:pm-ajith-io-b5626e` · `style:pm-mrtanviir-132457` · `style:pm-umangratani-57f86a`

#### SHAPE-57 · منحنيات ليساجو · Lissajous curves & tangles · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** x = A sin(at+δ)، y = B sin(bt) بنسب 3:2 و5:4، عشرون نسخة بانجراف بطيء لـ δ ومزج جمعي. — x = A sin(at+δ), y = B sin(bt) at 3:2, 5:4; 20 copies with drifting δ, additive low alpha, glow.
- **متى أستخدمها / when:** رياضيات، موسيقى، أوسيلوسكوب.
- **كيف / how:** δ drift .2 rad/s; neon stroke with glow (GLOW); 3D variant (sin 3t, sin 2t, sin 5t). **أرقام / params:** δ .2 rad/s; 20 copies.
- **الدليل / proof:** `kosif-tool/styles/pm-rneayan-ea6129` · `kosif-tool/styles/pm-math-files-39c9d0`
- **أساليب / styles:** `style:pm-rneayan-ea6129` · `style:pm-math-files-39c9d0`

#### SHAPE-58 · خطوط توليدية بأسلوب Joy Division · Ridge-line generative waves · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** 40–60 خطًا أفقيًا تزاح بالضوضاء قرب المركز مع أشرطة ملونة تنزلق. — 40–60 horizontal polylines displaced by noise near the centre, with coloured bars sliding across.
- **متى أستخدمها / when:** موسيقى، بيانات، أغلفة.
- **كيف / how:** Amplitude ramp 0→60 px toward the centre (Gaussian window); fill each line with background to occlude the ones behind; gradient red→blue by row. **أرقام / params:** 40–60 lines; amp 0→60 px.
- **الدليل / proof:** `kosif-tool/styles/pm-motiondsgnr-9dcfa6`
- **أساليب / styles:** `style:pm-motiondsgnr-9dcfa6`

#### SHAPE-59 · كسيريات وزخارف رياضية · Fractals, kolam, golden spiral, kaleidoscope · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** سيربنسكي يُبنى عمقًا عمقًا، كولام يلف حول شبكة نقاط بنقطة متوهجة تقوده، حلزون ذهبي فوق مربعات فيبوناتشي، جوليا بالشيدر، وتماثل كاليدوسكوبي. — Sierpinski depth by depth, a kolam loop weaving around a dot grid led by a glowing dot, a golden spiral over Fibonacci tiles, a Julia shader, kaleidoscope symmetry.
- **متى أستخدمها / when:** شرح رياضي، تراث هندسي، خلفيات منومة.
- **كيف / how:** Sierpinski 4–6 levels × 200 ms; kolam 7×5 dots one closed path drawn by dashoffset; Fibonacci tiles #c8b8f0→#e6dcf8 then quarter-arc chain 1.5–2 s; Julia z²+c purple→orange; kaleidoscope = polar fold n = 6–12 of a rotating texture (wedge 10°/s). **أرقام / params:** Sierpinski 4–6 × 200 ms; kaleidoscope 6–12 folds.
- **الدليل / proof:** `kosif-tool/styles/pm-buildfastwithai-53234e` · `kosif-tool/styles/pm-ddryo-loos-300829` · `kosif-tool/styles/pm-math-files-39c9d0` · `kosif-tool/styles/pm-monokern-ade5b6`
- **أساليب / styles:** `style:pm-buildfastwithai-53234e` · `style:pm-ddryo-loos-300829` · `style:pm-math-files-39c9d0` · `style:pm-monokern-ade5b6`

#### SHAPE-60 · جدار أيقونات مائل · Tilted icon wall · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شبكة بلاطات مستديرة بأيقونات خطية، مائلة −12° وتنجرف قطريًا، وبلاطة واحدة أسطع. — Grid of rounded tiles with line icons rotated ~−12° drifting diagonally, one tile highlighted.
- **متى أستخدمها / when:** خلفيات «تكاملات»، تطبيقات، منصات.
- **كيف / how:** Tile 90 px, radius 18 px, opacity .25–.4, drift 20 px/s; highlight = full opacity + accent border. **أرقام / params:** 90 px, r 18, drift 20 px/s.
- **الدليل / proof:** `kosif-tool/styles/pm-gabrielbuzziv-4ff0c6`
- **أساليب / styles:** `style:pm-gabrielbuzziv-4ff0c6`

#### SHAPE-61 · كتل أنماط شيدرية وشبكة متحركة · HyperFrames pattern shaders & dynamic grid · 📦 بأمر تثبيت / one install
- **ماذا / what:** حلقات متموجة، حلزون أوب آرت، خطوط قطرية، خلايا فورونوي (WebGPU)، وشبكة متحركة بمتغيرات CSS. — Ripples, op-art spiral, sliding stripes, Voronoi cells (WebGPU shaders) and a CSS-variable dynamic grid.
- **متى أستخدمها / when:** لوح خلفي جاهز داخل مشروع HyperFrames.
- **كيف / how:** npx hyperframes add ripples | spiral | stripes | voronoi (data-shader, data-requires-webgpu — WebGPU not verified here) | dynamic-grid (density fine|standard|coarse, weight hairline|standard|bold). **أرقام / params:** 2 s plates, 1920×1080.
- **📦 تثبيت / install:** `npx hyperframes add dynamic-grid`
- **⚖️ ترخيص / license:** Apache-2.0 (+ MIT shaders library).
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/voronoi/voronoi.html` · `kosif-one/vendor/hyperframes/registry/components/dynamic-grid/dynamic-grid.html`

## الحلقات والمدارات والانفجارات — Rings, orbits & bursts

_الحلقة تلتف بلا قفزة حين تكون نسب الدوران أعدادًا صحيحة؛ والانفجار يُقرأ حين يخرج سريعًا (expo.out) ويخبو ببطء._

#### SHAPE-62 · حلقات دوران بنسب صحيحة · Integer-ratio rotation loops (MG-112/115) · 📄 موصوف / documented only
- **ماذا / what:** نقاط تدور حول مركز بعيدًا عن النص، أو قوسان بسرعتين مترابطتين حول مركز واحد — نسب دورات صحيحة تضمن حلقة بلا قفزة. — Dots orbit a centre away from the text, or two arcs rotate at related speeds — integer turn ratios guarantee a seamless loop.
- **متى أستخدمها / when:** كل خلفية أو أيقونة يجب أن تلتف (loop).
- **كيف / how:** MG-112: exactly one turn in 6 s, linear, evenly spaced angles. MG-115: arc A 1 turn, arc B 2 turns per 6 s around a shared centre; never export the first frame twice at the seam (render t ∈ [0, T)). **أرقام / params:** 6 s; ratio 1:2.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-loops-backgrounds.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### SHAPE-63 · حلقات متحدة المركز بفجوات · Rotating gapped concentric rings · ✅ مُثبت هنا / proven here
- **ماذا / what:** N قوسًا متحد المركز لكل منها فجوة، تدور بسرعات متناوبة الاتجاه. — N concentric arcs each with a gap, rotating at alternating-sign speeds.
- **متى أستخدمها / when:** تحميل، تقنية، نبض صوت، خلفية عنوان.
- **كيف / how:** arc from gapStart+gap to gapStart+2π; gapStart_i += ω_i·dt with alternating sign; equal spacing; round caps. Rendered here (12 rings). Collapse variant: 6 rings 90–360°/s scale to a centre dot in 500 ms easeIn. **أرقام / params:** N 12, stroke 6–8 px, spacing ~13–14 px, ω .3–1.2 rad/s.
- **الدليل / proof:** `kosif-tool/styles/pm-kantamk-61f410` · `kosif-tool/styles/pm-leonkohli-6dc01b`
- **أساليب / styles:** `style:pm-kantamk-61f410` · `style:pm-leonkohli-6dc01b`

#### SHAPE-64 · عنقود أقواس مدارية ونواة نابضة · Orbiting arc cluster + pulsing donut core · 🟢 جاهز / ready
- **ماذا / what:** ستة أقواس 270° تدور حول مركز بمسافات متغيرة بلونين، ونواة دائرية ليمونية تتنفس في الوسط. — Six 270° arcs orbit a centre at varying distance in teal/lime with pulsing opacity; a breathing lime donut core in the middle.
- **متى أستخدمها / when:** خلفيات fastify motion، شاشات «يفكر».
- **كيف / how:** Arc k: angle = .5·phase + kπ/3, dist = w(.15 + .055 sin), radius w(.04 + .016 sin), sweep 1.5π, #89d6ce / #d5f375, alpha .24 + .25 sin²; core r = w(.12 + .025 sin(1.25 phase)) #c9f96d with inner #0a1724 at .58r. **أرقام / params:** 6 arcs, 270°; core 12% ± 2.5% w.
- **الدليل / proof:** `fastify-motion-bro/web/motion.js:13-14` · `fastify-motion-bro/web/motion.js:15`

#### SHAPE-65 · حلقات مدارية إهليلجية · Orbital ellipse rings & accents · 🟢 جاهز / ready
- **ماذا / what:** ثلاث حلقات إهليلجية مائلة تدور ببطء حول مركز التوهج، أو حلقة رفيعة تدور حول البطل، أو نجمة رباعية دوارة. — Three tilted concentric ellipses rotating slowly around the glow centre, a thin orbit ring around the hero, or a spinning four-spoke starburst.
- **متى أستخدمها / when:** جو «دراسة/علم»، إطار حول منتج أو أيقونة.
- **كيف / how:** ctx.rotate(.1·t); radii r(.66 + .18i) × r(.2 + .11i), tilt .3 + .65i rad, line .002·min(w,h); hero ring ellipse (.5w,.405h) .283w × .157h, rotation sin(.1 phase)·.12; starburst translate(.82w,.273h), rotate(.21 phase), spokes 10→24 px; satellites on a dashed ellipse tilted 20°. **أرقام / params:** 3 rings at .1 rad/s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:68` · `fastify-motion-bro/web/editorial.js:67-70` · `kosif-tool/styles/pm-samuel-spitz-974923`
- **أساليب / styles:** `style:pm-samuel-spitz-974923`

#### SHAPE-66 · انفجار خطوط شعاعي · Radial line burst · ✅ مُثبت هنا / proven here
- **ماذا / what:** 12–60 خطًا تنطلق من المركز بأطوال وألوان متفاوتة بـ expo.out مع تتابع 20 ms، ثم تخبو. — 12–60 lines shoot from the centre with varied length/colour, expo.out, 20 ms stagger, then fade.
- **متى أستخدمها / when:** توكيد كلمة، ضربة إيقاع، اكتشاف، افتتاح.
- **كيف / how:** r0 = 20 + 30b, r1 = 40 + 120b with b = 1 − (1−p)^5; alternate accent/primary; fade over the second half. Rendered here (14 lines). Basma TEMPLATES.shapes: 14 lines from m(.1 + .25k) to m(.16 + .42k)·jitter + ring .42m·k in .6–1 s. **أرقام / params:** 400–600 ms expo.out; 12–60 rays; stagger 20 ms.
- **الدليل / proof:** `app/public/js/00_editor.js:518` · `kosif-tool/styles/pm-teslachartz-c58b32` · `kosif-tool/styles/pm-shinskinakamoto-20190b` · `kosif-tool/styles/pm-stephanlivera-df17a2`
- **أساليب / styles:** `style:pm-teslachartz-c58b32` · `style:pm-shinskinakamoto-20190b` · `style:pm-stephanlivera-df17a2` · `style:pm-sudo-kiran-49176d` · `style:pm-mandelduck-95fd08`

#### SHAPE-67 · حلقة صدمة أرضية ونبض قلب · Shockwave ring & heartbeat ripple · ✅ مُثبت هنا / proven here
- **ماذا / what:** حلقة إهليلجية مسطحة (y×0.25) تتسع 0→300px في 500ms وتخبو؛ أو حلقة ثانية تكبر 1→1.9 وتخبو على نبضتين. — Flattened ellipse ring (y×.25) expanding 0→300 px in 500 ms with fade; or a second ring scaling 1→1.9 and fading on beats.
- **متى أستخدمها / when:** هبوط جسم، ضربة، نبض، «عش كل لحظة».
- **كيف / how:** Rendered here (shockwave under the burst). Heartbeat: circle r150 #f5c97a 5 px drawn 1.1 s, ring2 scale 1→1.9, opacity .9→0 in .9 s E.out at the beat times. **أرقام / params:** 0→300 px / 500 ms; heartbeat 1→1.9 in .9 s.
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html` · `kosif-tool/styles/pm-chrisjdimarco-f068db`
- **أساليب / styles:** `style:pm-chrisjdimarco-f068db`

#### SHAPE-68 · أشعة شمسية دوارة · Rotating sunburst ground · ✅ مُثبت هنا / proven here
- **ماذا / what:** 24–36 إسفينًا متناوبًا بلونين متقاربين يدور ببطء خلف العنوان مع تعتيم شعاعي. — 24–36 alternating wedge rays in two close tones rotating slowly behind the title, with radial vignette.
- **متى أستخدمها / when:** بطاقات «بطل»، ريترو، احتفال، أغلفة.
- **كيف / how:** conic-gradient repeating wedges or canvas arcs; tone delta ~8% lightness; rotation 3–10°/s. Rendered here (28 wedges, .12 rad/s). **أرقام / params:** 24–36 rays; 3–10°/s; Δ lightness ~8%.
- **الدليل / proof:** `kosif-tool/styles/pm-deebeeeff-50fcd0` · `kosif-tool/styles/pm-majin-appsheet-2d3c1a` · `kosif-tool/styles/pm-allforbigfire-86ff3c`
- **أساليب / styles:** `style:pm-deebeeeff-50fcd0` · `style:pm-majin-appsheet-2d3c1a` · `style:pm-allforbigfire-86ff3c`

#### SHAPE-69 · حلقة نقاط تتسع بخطوط شعاعية · Expanding dot ring with radial lines · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نقاط الشعار تتضاعف حول دائرة أكبر (8→24) وخطوط بنفسجية رفيعة تشع خلفها نحو أطراف الكادر. — Logo dots duplicate around a larger circle (8 → 24) while thin violet lines radiate behind toward the frame edges.
- **متى أستخدمها / when:** كشف هوية، شبكة، «مجتمع».
- **كيف / how:** Ring radius 40% width; lines 1.5 px #8a6cff; satellites stagger 30 ms. **أرقام / params:** 8 → 24 dots; ring 40% w.
- **الدليل / proof:** `kosif-tool/styles/pm-micheleharmonic-77628e`
- **أساليب / styles:** `style:pm-micheleharmonic-77628e`

#### SHAPE-70 · نفق مربعات حلزوني · Spiral square tunnel & nested squares · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** مربعات متداخلة كل منها ×0.9 ومدار 8° بلونين متناوبين، أو 8 مربعات تدور بتأخير 50ms، أو نفق من نسخ الشعار. — Nested squares each ×.9 and rotated 8° in alternating colours, 8 squares rotating with 50 ms delay, or a tunnel of logo outlines.
- **متى أستخدمها / when:** سرعة، دوار، انتقال للداخل.
- **كيف / how:** Loop: scale every copy by 1/.9 per period and wrap; tunnel of outlines with a ticking counter for speed ramps. **أرقام / params:** ×.9, 8° per level; delay 50 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-zheke-38deff` · `kosif-tool/styles/pm-safarkhanshuvo-ffd52d` · `kosif-tool/styles/pm-jasonzhou1993-8595e0/BRIEF.md`
- **أساليب / styles:** `style:pm-zheke-38deff` · `style:pm-safarkhanshuvo-ffd52d`

#### SHAPE-71 · مربع يصير دائرة مع أقمار · Square→circle with satellites & star pop · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** border-radius 0→50% مع دوران وثلاث نقاط تدور على حلقة رفيعة، أو نجمة تقفز بـ outBack ونجوم صغيرة حولها. — border-radius 0→50% with rotation while three dots orbit on a thin ring; or a star popping with outBack and small orbiting stars.
- **متى أستخدمها / when:** أيقونات حية، إنجاز، «جديد».
- **كيف / how:** Morph 500 ms; orbit 1 rev/s; background polka grid pulses. **أرقام / params:** 500 ms; 1 rev/s.
- **الدليل / proof:** `kosif-tool/styles/pm-shinskinakamoto-20190b` · `kosif-tool/styles/pm-stephanlivera-df17a2`
- **أساليب / styles:** `style:pm-shinskinakamoto-20190b` · `style:pm-stephanlivera-df17a2`

#### SHAPE-72 · بوابة دوامية ومصباح فرينل · Swirl portal & Fresnel lamp room · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** حلقة طارة متوهجة حول قرص ضوضاء ملتوٍ قطبيًا؛ أو شبكة معينات فوق أسطوانة متوهجة بعدسة حلقات تشتعل في 400ms. — Glowing torus ring around a polar-twisted noise disc; or a diamond-pane lattice over a glowing cylinder with a concentric-ellipse lens igniting in ~400 ms.
- **متى أستخدمها / when:** خيال، بوابات، منارات.
- **كيف / how:** Twist: θ += k/(r+ε) before sampling noise; lattice 40 px cells, glow blur 30–60 px, bloom spike on ignition. **أرقام / params:** ignite 400 ms; lattice 40 px.
- **الدليل / proof:** `kosif-tool/styles/pm-ryzoft-4f85bd` · `kosif-tool/styles/pm-kamstudiolabs-0b0824`
- **أساليب / styles:** `style:pm-ryzoft-4f85bd` · `style:pm-kamstudiolabs-0b0824`

## الزخرفة والأيقونات والعناصر المصاحبة — Ornament, icons & decor

_الزخرفة الإسلامية تُبنى من مربعين ودائرة؛ والأيقونة الجيدة تُقرأ في 16px — كل عنصر مصاحب يخدم البطل ولا ينافسه._

#### SHAPE-73 · الزخرفة الثمانية من الكود · Islamic eight-point rosette builder · 🟢 جاهز / ready
- **ماذا / what:** نجمة ثمانية من مربعين مدارين 45° + نجمة 16 رأسًا + دائرة + نجمة داخلية، يُرسم كل جزء بالتتابع وتدور الوردة كلها ببطء. — An eight-point star from two squares at 0/45°, a 16-vertex star, a circle and an inner star, each drawn in sequence while the rosette slowly turns.
- **متى أستخدمها / when:** دعاء، مناسبات إسلامية، فواصل، هوية تراثية.
- **كيف / how:** sq(78,0), sq(78,π/4), star8(120,92), circle r48, star8(30,14); M.drawPath each at .4 + .18i s for 1.3 s, opacity .85; rotate 0→45° over the film; stroke #f6d27a width 3→5 on the key word. **أرقام / params:** draw 1.3 s, stagger .18 s; stroke #f6d27a 3→5.
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html`

#### SHAPE-74 · وردة الفواصل الموسيقية · Interlude rosette (verse template) · 🟢 جاهز / ready
- **ماذا / what:** في الوقفات الطويلة (≥ 4.5 ث) تُرسم وردة ثمانية تتنفس على الإيقاع ثم تنسحب. — During long pauses (≥ 4.5 s) an eight-point rosette is drawn, breathes on the beat, then withdraws.
- **متى أستخدمها / when:** أفلام الشعر والأغاني والأدعية من الصوت.
- **كيف / how:** verse.py writes interludes into verse.json (start = end + .8 s, end = next − .5 s, ≥ 1.5 s); verse.html ROSETTES: two squares at 0/45° + circle .42R #F7F2E8 .7, R 150k, stroke 2.2k accent, rotate 9°/s, beat scale +7%, draw 1.1 s stagger .12. **أرقام / params:** pause ≥ 4.5 s; 9°/s; beat +7%.
- **الدليل / proof:** `kosif-studio/motion/templates/verse.html` · `kosif-studio/motion/verse.py:258` · `100-superskills/skills/kosif-montage-motion/templates/verse.html:298`

#### SHAPE-75 · فوانيس ومسجد ونوافذ · Swaying lanterns & mosque silhouette · 🟢 جاهز / ready
- **ماذا / what:** فانوسان من أشكال SVG يتأرجحان كالبندول بتوهج يتنفس، وصورة ظلية لقبة ومئذنتين بنوافذ مقوسة ترتعش. — Two SVG lanterns swinging like pendulums with breathing glow; a dome-and-two-minarets silhouette with softly flickering arched windows.
- **متى أستخدمها / when:** رمضان، ليلة الجمعة، أعياد.
- **كيف / how:** Lantern: chain line, radial glow r120, cap, hexagon body #ffcf72 .92 stroke #c48a2c, ribs #b07a22; rotation ±3.5° yoyo 2.2/2.5 s (svgOrigin 0 0); glow .7→1 yoyo .96 s. Mosque paths #1d0f2c, ground #140920; 8 windows #ffc768 .55→1 yoyo .9–1.7 s at random offsets (seeded). **أرقام / params:** ±3.5°, 2.2/2.5 s; windows .55→1.
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html`

#### SHAPE-76 · غيمة من دوائر تكبر وتعتم · Circle-cluster cloud that grows and darkens · 🟢 جاهز / ready
- **ماذا / what:** غيوم من خمس دوائر وقاعدة مستديرة تكبر فوق البحر وتنجرف وتعتم قبل المطر ثم تصفو. — Clouds of five circles and a rounded base grow, drift and darken before rain, then lighten.
- **متى أستخدمها / when:** شرح دورة الماء، طقس، قصص أطفال.
- **كيف / how:** circles (0,0,62) (−75,18,46) (78,18,50) (−32,−34,52) (38,−40,58) + rect 248×58 rx29; scale .2→1 (3.8–5.0 s), drift 4.9–6.2 s; #FFFFFF→#A6B9CC, base #DCE8F2→#8FA3B8 for dark 6.0–6.5 s, back after 8.3 s. **أرقام / params:** 5 circles + base; scale .2→1.
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/index.html`

#### SHAPE-77 · مكتبة 16 أيقونة متجهة · 16-icon vector hero library · 🟢 جاهز / ready
- **ماذا / what:** أيقونات Canvas مرسومة بالكود تصلح أبطالًا: عين، دماغ، محفظة، نقود، شاشة، ساعة رملية، مصباح، صاروخ، ساعة، مؤشر، رسم بياني، درج، دومينو، كتاب، أشخاص، شطرنج + نجمة. — Hand-coded Canvas icons usable as hero objects (eye, brain, wallet, money, screen, hourglass, bulb, rocket, clock, cursor, chart, stairs, domino, book, people, chess + star).
- **متى أستخدمها / when:** ريلز تحريرية بلا أصول خارجية.
- **كيف / how:** icon(ctx, name, r, accent, ink) with round joins, stroke .08r; choose via scene.hero. **أرقام / params:** 16 named + default.
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:12-34`

#### SHAPE-78 · أيقونات SVG حية · Living SVG icons · 📄 موصوف / documented only
- **ماذا / what:** حرّك أجزاء الأيقونة الداخلية: عقارب ساعة، ريش مروحة، نقاط نابضة، خطوط تدفق — بدوران حول مركز دقيق. — Animate inner SVG parts (clock hands, fan blades, pulsing dots, dash-flow lines) with rotate(deg cx cy) for exact centres.
- **متى أستخدمها / when:** أي أيقونة ثابتة في مشهد — اجعلها تعمل.
- **كيف / how:** setAttribute("transform", `rotate(${d} ${cx} ${cy})`); ease none for linear rotation; one paused timeline, fromTo explicit states.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/svg-icon-enrichment.md`

#### SHAPE-79 · قواعد الأيقونة: شبكة 24 والإغلاق · Icon rules: 24 px grid & closure · 📄 موصوف / documented only
- **ماذا / what:** شبكة 24px، خط 2px، نهايات دائرية، viewBox مربع، بلا نص، < 4KB؛ والإيحاء بالشكل بفجوات ونهايات متحاذية — اختبرها في 8–16px. — 24 px grid, 2 px stroke, round caps, square viewBox, no text, < 4 KB; imply forms with gaps and aligned terminals (closure) — test at 8–16 px.
- **متى أستخدمها / when:** رسم أي أيقونة جديدة.
- **كيف / how:** Test at 16/24/48/192 px; draw-on works especially well with closure because the eye completes the form early. **أرقام / params:** 24 px / 2 px; test 8–16 px.
- **الدليل / proof:** `100-superskills/skills/svg-illustration-icons/SKILL.md:21` · `kosif-atlas/skills/1503-universal-design-principles/3812-closure-implied-shapes`

#### SHAPE-80 · طبقات أشكال وملصقات منبثقة · Shape layers & sticker/emoji pop-ups · 📦 بأمر تثبيت / one install
- **ماذا / what:** دائرة أو شريط مستدير كخط تحت النص في محرر الاستوديو؛ وإيموجي ونص وملصقات تنبثق بنابض وتمايل في Basma. — Studio overlay shapes (circle or rounded underline bar); Basma emoji/text/sticker pop-ups springing in with a slight wobble.
- **متى أستخدمها / when:** توكيد سريع في مونتاج الريلز.
- **كيف / how:** Studio: overlay.type="shape", "circle" (arc size/2) or "rectangle" (roundRect h .24·size, r max(2,.06·size)), default 16% #52dbc6. Basma drawOverlays(): spring(z .4, w 17) scale, rotate sin(3l)·.03, .2 s fade-out; positions top 30%, centre 47%, bottom 64%, corner (78%,16%); emoji 17% m; text Lalezar 6.5% on an accent pill. **أرقام / params:** spring z .4 ω 17; size 16%.
- **📦 تثبيت / install:** `cd app && npm install`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:76` · `app/public/js/00_editor.js:412`

#### SHAPE-81 · ملصقات زخرفية وكبسولات وسوم · Decor stickers, hazard tape & floating tag pills · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نجوم مضلعة وشرائط تحذير مخططة في الزوايا تتمايل، وكبسولات وسوم بيضاء تطفو حول العنوان بدوران عشوائي. — Starburst polygons and striped hazard tapes wobbling in corners; white tag pills floating around the headline at random tilts.
- **متى أستخدمها / when:** ريلز مرحة، عروض SaaS، شارات.
- **كيف / how:** Stickers rotate ±6° over 2 s yoyo, colours rotate per scene; 6 pills radius 999, 1 px #c4d8e5 border, ±6° tilt, pop-in stagger 120 ms, idle bob 4 px period 3–4 s, avoid the centre. **أرقام / params:** ±6°/2 s; pills stagger 120 ms, bob 4 px.
- **الدليل / proof:** `kosif-tool/styles/pm-0xnfrith-5be616` · `kosif-tool/styles/pm-alex-prompter-1ea044`
- **أساليب / styles:** `style:pm-0xnfrith-5be616` · `style:pm-alex-prompter-1ea044`

#### SHAPE-82 · مروحة بطاقات وصور · Card / photo / swatch fan-out · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نسخ البطاقة خلفها تنفتح كمروحة حول محور مشترك بإزاحة ودوران متدرج، مع ألسنة مرقمة أو عداد. — Duplicates behind a card fan out around a shared pivot with offset and stepped rotation, with numbered tabs or a count label.
- **متى أستخدمها / when:** «مجموعة كاملة»، ألبوم، عينات ألوان.
- **كيف / how:** 6 cards offset x +18 px and +2..+6° (or ±12–25° around a pivot for photos), stagger 70–80 ms, 400–500 ms easeOutBack(1.2). **أرقام / params:** 5–8 items, stagger 70–80 ms, 400–500 ms back.out.
- **الدليل / proof:** `kosif-tool/styles/pm-bogdandragomir-35e024` · `kosif-tool/styles/pm-lester-tyy-f897f7` · `kosif-tool/styles/pm-ercankeskinx-ec2568`
- **أساليب / styles:** `style:pm-bogdandragomir-35e024` · `style:pm-lester-tyy-f897f7` · `style:pm-ercankeskinx-ec2568` · `style:pm-thayto-dev-44b911`

#### SHAPE-83 · شريط تظليل مائل خلف النص · Slanted highlighter bar wipe · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** مستطيل مائل يكبر أفقيًا من 0 إلى 1 خلف سطر نص، أكبر قليلًا من صندوقه. — A skewed rectangle scales X from 0 to 1 behind a text line, slightly larger than the text box.
- **متى أستخدمها / when:** توكيد سطر، عناوين تحريرية.
- **كيف / how:** skewX −8°, 180–250 ms easeOutCubic; for Arabic grow from the right (transform-origin right). **أرقام / params:** skewX −8°, 180–250 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-deifosv-04e4d3`
- **أساليب / styles:** `style:pm-deifosv-04e4d3`

#### SHAPE-84 · تغيير لون الكلمة داخل الكرة · Clip-path colour flip over a moving lens · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** صف كلمات مرسوم مرتين: نسخة داكنة، ونسخة بيضاء مقصوصة بدائرة الكرة، والصف ينزلق فتتلون كل كلمة حين تعبرها. — Render a word row twice — dark copy, and a white copy clipped with clip-path: circle() at the orb — and slide the row so each word flips inside the orb.
- **متى أستخدمها / when:** عرض قيم أو مزايا متتابعة، منتج.
- **كيف / how:** orb r ~70 px; row speed ~1 word / .8 s; for Arabic slide left→right so words enter from the right. **أرقام / params:** orb r 70 px; 0.8 s per word.
- **الدليل / proof:** `kosif-tool/styles/product`
- **أساليب / styles:** `style:product`

#### SHAPE-85 · تجميع من شظايا أو قطع · Shard / piece assembly along a path · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** مثلثات تبدأ خارج الشاشة مدارة وتنزلق إلى أماكنها، أو قطع هيكل تسافر على قوس منقط وتلتحم بتجاوز بسيط. — Triangles start off-screen rotated and ease into slots; or skeleton pieces travel along a dotted arc and snap together with slight overshoot.
- **متى أستخدمها / when:** كشف شكل أو شعار، تعليم تشريح.
- **كيف / how:** Per piece: start = random off-screen pose (seeded), path = quadratic arc, 600 ms ease-out, stagger 40 ms, total ~1.2 s. **أرقام / params:** stagger 40 ms; 600 ms each.
- **الدليل / proof:** `kosif-tool/styles/pm-tdinh-me-815acb` · `kosif-tool/styles/pm-gigabit-million-16b3a0`
- **أساليب / styles:** `style:pm-tdinh-me-815acb` · `style:pm-gigabit-million-16b3a0`

#### SHAPE-86 · شاشة مقسومة واستعارة الكسوف · Split-screen eclipse metaphor · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نصف كريمي ونصف أسود: دائرة مفرغة في جهة ونقطة حمراء في الأخرى تنزلقان وتتداخلان ككسوف. — Half cream / half black; an outline circle and a filled red dot slide toward each other and overlap into an eclipse.
- **متى أستخدمها / when:** مقارنة، «لقاء»، استعارة بصرية.
- **كيف / how:** ~1.5 s ease-in-out; difference blend at the overlap. **أرقام / params:** ~1.5 s.
- **الدليل / proof:** `kosif-tool/styles/pm-samaote-5e2fc2`
- **أساليب / styles:** `style:pm-samaote-5e2fc2`

#### SHAPE-87 · بحر خطوط مع شخصية رمزية · Line-art sea with mascot · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** 4–6 مسارات جيبية أفقية بانجراف طور وسرعات بارالاكس، وشخصية مسطحة صغيرة تتمايل وتعبر. — 4–6 horizontal SVG sine paths with slow phase drift at parallax speeds; a small flat mascot bobs (±4°) and crosses.
- **متى أستخدمها / when:** إعلانات لطيفة، رحلات، أطفال.
- **كيف / how:** Wave amplitude 4–10 px, period 6 s; bob 1.5 s; a passing train/vehicle strip with 30 px motion blur for fast occlusion. **أرقام / params:** amp 4–10 px, 6 s; bob ±4°/1.5 s.
- **الدليل / proof:** `kosif-tool/styles/pm-aschapmann-131210` · `kosif-tool/styles/pm-itsolelehmann-e47532`
- **أساليب / styles:** `style:pm-aschapmann-131210` · `style:pm-itsolelehmann-e47532`

#### SHAPE-88 · فاصل بشعرة · Hairline separator (HyperFrames) · 📦 بأمر تثبيت / one install
- **ماذا / what:** فاصل 1px أفقي أو عمودي بكشف تقدمي آمن للبحث. — 1-pixel structural separator with a seek-safe progress reveal.
- **متى أستخدمها / when:** تخطيطات تحريرية، جداول، بطاقات.
- **كيف / how:** npx hyperframes add separator; orientation horizontal|vertical; thickness hairline|medium|bold; tone neutral|accent|warning.
- **📦 تثبيت / install:** `npx hyperframes add separator`
- **⚖️ ترخيص / license:** Apache-2.0.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/separator/separator.html`

## نظام الأشكال وقواعده — Shape system & rules

_ثلاثة أشكال أولية، لونان وخلفية، سلم أقطار وسلم خطوط، و30% فراغ — النظام هو ما يجعل البساطة فاخرة._

#### SHAPE-89 · وحدة 24 وشبكة أعمدة · Base-unit grid system · 📄 موصوف / documented only
- **ماذا / what:** كل المقاسات مضاعفات وحدة أساس على شبكة أعمدة، والإطار الأخير يستقر على الشبكة تمامًا. — All sizes multiples of a base unit on a column grid; final frames land exactly on grid.
- **متى أستخدمها / when:** كل مشهد أشكال.
- **كيف / how:** unit 24 px; 8 or 12 columns; snap end states, not in-betweens. **أرقام / params:** 24 px; 8/12 columns.
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:15` · `kosif-tool/playbooks/shapes.md:29`

#### SHAPE-90 · سلالم الأقطار والخطوط والفراغ · Primitive, radius & stroke scales · 📄 موصوف / documented only
- **ماذا / what:** ثلاثة أشكال أولية كحد أقصى، لونان + خلفية، أقطار 0/8/24/50%، خطوط 2/4/8، وفراغ سلبي ≥ 30%. — Max three primitives, two colours + background, radii 0/8/24/50%, strokes 2/4/8, ≥ 30% negative space.
- **متى أستخدمها / when:** تصميم أي مشهد هندسي قبل التحريك.
- **كيف / how:** Nested radius: inner = outer − gap when gap < 32 px and result > 2 (16 px outer, 8 px gap → 8 px). **أرقام / params:** radii 0/8/24/50%; strokes 2/4/8; ≥ 30% empty.
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:16-18` · `kosif-one/vendor/ai-design-skills/skills/landing-page-design/SKILL.md:225`

#### SHAPE-91 · انضغاط وتمدد بحفظ المساحة · Area-preserving squash & stretch · 🟢 جاهز / ready
- **ماذا / what:** عند الاصطدام ينضغط الشكل (0.7/1.3) 80ms حول نقطة التلامس ثم يعود بنابض. — On impact squash (scaleY .7 / scaleX 1.3) for 80 ms around the contact point, then spring back.
- **متى أستخدمها / when:** كل قفزة أو ارتطام أو ضغطة زر.
- **كيف / how:** Canvas: ctx.scale(1 + .3s, 1 − .3s) about the contact; s = KOSIF.window01(t, hit, hit + .08, .02, .06) in the html-canvas starter; spring {damping 10, stiffness 220}. **أرقام / params:** .7/1.3 for 80 ms; spring d10 k220.
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:25` · `kosif-tool/playbooks/shapes.md:66` · `kosif-tool/starters/html-canvas/index.html`

#### SHAPE-92 · التصاق مغناطيسي وكل شيء من المركز · Magnet snap spring & centre-origin rule · 💡 فكرة / idea
- **ماذا / what:** الأشكال تلتصق في أماكنها بتجاوز واحد؛ وفي بعض الأساليب كل التحويلات حول مركز الإطار وكل دخول منه. — Primitives snap into place with one overshoot; in some styles every transform pivots on the frame centre and every entrance starts there.
- **متى أستخدمها / when:** أساليب هندسية صارمة ومرتبة.
- **كيف / how:** Untested brief ideas: Remotion spring stiffness 220 damping 14, or UI cubic-bezier(.16,1,.3,1) 400–600 ms; transform-origin 960px 540px. **أرقام / params:** k 220 d 14; origin (960,540).
- **الدليل / proof:** `kosif-tool/styles/pm-quickdesignio-dd93d0/BRIEF.md` · `kosif-tool/styles/pm-marouanegazouzi-6071d5/BRIEF.md`

#### SHAPE-93 · أسلوب المرح الهندسي (S07) · Playful geometric style (S07) · 📄 موصوف / documented only
- **ماذا / what:** لوحة محدودة جريئة، دوائر وبطاقات وأيقونات، قفزات صغيرة وتبديل أشكال وإيقاع متنوع — حي من أصول بسيطة. — Limited bold palette, circles, cards and icons; small bounces, shape swaps, varied rhythm.
- **متى أستخدمها / when:** تعليم، تطبيقات، محتوى خفيف — لا للمواضيع الجادة.
- **كيف / how:** SVG primitives + overshoot easings + staggered entrances, rendered with render_html.cjs; over-bouncing distracts — one overshoot per entrance. **أرقام / params:** ideas MG-008 MG-029 MG-061 MG-081 MG-083 MG-108 MG-115.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md` · `kosif-tool/playbooks/shapes.md`

## توليفات قوية / power combos

- **هوية باوهاوس على الإيقاع / Bauhaus beat ident:** SHAPE-52 + SHAPE-53 + BEAT (خطوة لكل نبضة) + SHAPE-01 (الشبكة تنهار إلى الشعار) + COLOR (أحمر/أصفر/أزرق/أسود على كريمي).
- **ليلة دعاء / night dua:** SHAPE-73 + SHAPE-75 + SHAPE-74 + TEX (قمر إجرائي) + GLOW (هالة ذهبية) + ARAB (كلمات من العمق) + VOICE — الوردة تُرسم في الوقفات فقط.
- **ريل منتج من نقطة / product reel from a dot:** SHAPE-17 + SHAPE-18 + SHAPE-23 + UI (لقطات الواجهة) + EASE (E.inOut على شبكة 120 BPM) — النقطة نفسها خيط القصة حتى بطاقة CTA.
- **إنفوغراف حي / living infographic:** SHAPE-09 + SHAPE-10 + DATA (القيم الحقيقية) + SHAPE-56 + DRAW (رسم المحاور) — من «1 من 100» إلى دائري نسب بلا قطع.
- **شعار سائل / liquid logo:** SHAPE-27 + SHAPE-31 + SHAPE-01 + GLOW + PART (قطرات تنفصل) + TRANS (الكتلة تغمر الإطار) — الكتل تندمج ثم تستقر حروفًا (الكلمة العربية قناع واحد).
- **شخصية قطيفة من الحقول / plush character:** SHAPE-32 + SHAPE-33 + SHAPE-34 + TEX (خامة القطيفة والفرو) + CHAR (هيكل الأرنب) + 3D (إضاءة استوديو).
- **شرح رياضي / math explainer:** SHAPE-04 + SHAPE-03 + SHAPE-57 + SHAPE-59 + EXPL (معادلة حية) + ARAB (تسميات عربية) — الشكل والمعادلة يتحركان معًا.
- **ضربة توكيد / emphasis hit:** SHAPE-66 + SHAPE-67 + BEAT (onset) + TYPE/ARAB (كلمة بطلة) + CAM (هزة 12px تخمد) — كما في انفجار proofs/particles-to-arabic.

## أخطاء ممنوعة / never do

1. **لا تحوّل مسارين بعدد نقاط أو اتجاه لف مختلف** — الشكل ينقلب أو يلتف على نفسه في المنتصف؛ أعد العينات وحاذِ نقطة البداية (SHAPE-02).
2. **لا تحوّل حروفًا عربية حرفًا حرفًا بالمسارات** — الحروف المتصلة تنفصل؛ حوّل الكلمة كمسار واحد أو استعمل قناعًا.
3. **لا تلاشي متقاطع حين يوجد عنصر مشترك** — يكسر الهوية؛ استعمل FLIP أو تحول الحاوية (SHAPE-15، SHAPE-18).
4. **لا حلقات بنسب دوران غير صحيحة في فيديو يلتف** — يظهر قفز عند نقطة الالتفاف؛ نسب صحيحة ولا تصدّر الإطار الأول مرتين (SHAPE-62).
5. **لا عشوائية بلا بذرة في الشبكات والأنماط** — كل رندر يختلف؛ hash(x, y, seed) لكل خلية.
6. **لا أكثر من ثلاثة أشكال أولية ولونين** — يضيع النظام ويصير الكادر ضوضاء (SHAPE-90).
7. **لا ترتد كل الأشكال (overshoot) في كل دخول** — الارتداد الزائد يشتت؛ تجاوز واحد للبطل والباقي ease-out.
8. **لا فلتر لزوجة على النص** — العتبة تأكل الحواف والنقاط العربية؛ النص خارج مجموعة الفلتر (SHAPE-27).
9. **لا تطلب MorphSVG أو flubber في رندر هنا قبل تثبيتها** — غير مثبتة؛ SHAPE-01 من motion-kit يعمل بلا مكتبة.
10. **لا تقلّد بلاطات باوهاوس وتروشيه من فيديو مرجعي حرفيًا** — ابنِ من القانون (موجة مسافة + لوحة) بلوحة وإيقاع المستخدم.

## أقوى 5 حركات توقيع / 5 signature moves

1. **SHAPE-01 — تحويل المسار الآمن للبحث:** دائرة→نجمة→مربع في 0.66 ث بـ 120 نقطة، بلا مكتبة، مُثبت هنا.
2. **SHAPE-52 — شبكة باوهاوس بموجة المسافة:** خطوة لكل نبضة، أربعة أشكال وأربعة ألوان — أكثر نمط هندسي تكرارًا في المراجع.
3. **SHAPE-27 — كتل تندمج:** stdDeviation 10 ومصفوفة 18/−7 — سائل في سطرين.
4. **SHAPE-73 — الوردة الثمانية:** مربعان ودائرة تُرسم بالتتابع وتدور 45° — توقيع الأفلام الإسلامية.
5. **SHAPE-66 + SHAPE-67 — الانفجار وحلقة الصدمة:** 14 خطًا بـ expo.out وحلقة مسطحة 0→300px في 500ms على الضربة.

## إضافات v2 — v2 additions

_قدرات أُضيفت في الإصدار الثاني من حزم المالك (higgsfield-motion-saas وhiggsfield-motion-claude ومهارة المونتاج التحريرية وفيلم الأغنية وKOSIF SEE) ومن مهارات ECC (رخصة MIT)، مكتوبة بكلماتنا. ✅ هنا = شُغّلت في جلسة 2026-10-16 وسجلها في [external-skills.md](../external-skills.md)؛ مسارات `owner-upload:` تشير إلى أرشيفات المالك لا إلى هذا المستودع. — v2 additions from the owner's packages and ECC skills (MIT), in our own words; ✅ = run in this session, log in external-skills.md; `owner-upload:` paths point into the owner's archives, not this repo._

#### SHAPE-X01 · تحوّل هندسي بلا مزج · Geometric morph without a crossfade (letter → planet) · 📄 موصوف / documented only
- **ماذا / what:** حوّل شكلًا إلى آخر عبر سلسلة أشكال وسيطة تحمل النقاط نفسها، لا بمزج صورتين. — Turn one shape into another through a chain of intermediate shapes carrying the same points, never by crossfading two images.
- **متى أستخدمها / when:** حرف من الشعار يصبح كوكبًا أو كرة أو أيقونة — a logo letter becoming a planet, sphere or icon.
- **كيف / how:** Letter O → ellipse → 3D ring → 6 meridian copies → wire sphere → dotted Earth: map source points onto each stage, depth-sort, draw the back half at α 0.3. **أرقام / params:** 6 meridians; back half α 0.3.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`

#### SHAPE-X02 · لقطة متصلة من عناصر مشتركة · One continuous shot from shared elements · 📄 موصوف / documented only
- **ماذا / what:** العناصر نفسها تعيد ترتيب نفسها من شكل إلى آخر (مروحة ثم رسم بياني ثم حلقة) فتصنع فيلمًا بلا قطع. — The same elements rearrange from one formation to the next (fan, then graph, then ring), making a film with no cuts.
- **متى أستخدمها / when:** فيلم بيانات أو منتج بلا قطع — a data or product film without cuts.
- **كيف / how:** 28 tiles with pose functions fan → graph → ring; greedy nearest assignment between formations; ring slots sorted by angle so paths never cross; stagger 0.014–0.02 s; pinhole projection f 1500. **أرقام / params:** 28 tiles; stagger 0.014–0.02 s; f 1500.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`

## من أكبر مستودعات GitHub — from the top GitHub repositories (2026-10-23)

_قدرات من أشهر مستودعات GitHub ذات الترخيص المفتوح (MIT)، مكتوبة بكلماتنا لا منسوخة، وسجل كل مستودع في [github-top-1000.md](../github-top-1000.md). 🟢 = الكود هنا في `scripts/motion_physics.py` واختباره `evals/test_motion_physics.py`. — Powers from the most-starred open-licence (MIT) GitHub repositories, restated in our own words; per-repo record in github-top-1000.md; 🟢 = code here in scripts/motion_physics.py with its test._

#### SHAPE-G01 · رقم متحرك واحد يقود كل الأشكال · One animated value drives every dependent shape · 📄 موصوف / documented only
- **ماذا / what:** حرّك قيمة واحدة (متتبع) واجعل كل شكل يعتمد عليها يُعاد رسمه من دالة في كل إطار، بدل تحريك كل شكل وحده. — Animate one value (a tracker) and redraw every dependent shape from a function of it each frame, instead of animating each shape alone.
- **متى أستخدمها / when:** رسوم شرح فيها نقطة على منحنى، أو عداد وأعمدة، أو زاوية ومثلث / explainers with a dot on a curve, a counter and bars, or an angle and a triangle
- **كيف / how:** Manim pattern: ValueTracker t → always_redraw(lambda: Dot(axes.c2p(t, f(t)))) plus a label and a tangent from the same t; then animate only t. In HTML: one state value, every element computed in render(t). Dependencies can never drift apart, and seeking any frame is exact.
- **الرخصة / license:** MIT
- **المصدر / source:** https://github.com/3b1b/manim and https://github.com/ManimCommunity/manim (MIT) — restated in our own words

#### SHAPE-G02 · تحويل يطابق الأجزاء المشتركة · Morph that matches shared parts · 📄 موصوف / documented only
- **ماذا / what:** عند تحويل معادلة أو نص أو شكل إلى آخر، أبقِ الأجزاء المتطابقة في مكانها وحرّكها، وحوّل المختلف فقط، بدل ذوبان كل شيء في كل شيء. — When morphing one equation, text or shape into another, keep matching parts and move them, morph only what differs, instead of melting everything into everything.
- **متى أستخدمها / when:** خطوات حل معادلة، تغيير كلمة في عنوان، تطور شعار / equation steps, swapping a word in a title, logo evolution
- **كيف / how:** Split both states into parts with stable keys (tokens, glyphs, sub-paths); matched keys tween position/scale; unmatched old parts fade or shrink out, new ones fade or grow in; order point lists before a path morph so vertices pair by position. Manim: TransformMatchingTex / TransformMatchingShapes; ReplacementTransform when the target object replaces the source in the scene.
- **الرخصة / license:** MIT
- **المصدر / source:** https://github.com/ManimCommunity/manim (MIT; TransformMatchingTex/Shapes) — restated in our own words
