# الملمس والخامات — Texture & material

> **قوتك هنا:** أنت تعطي السطح المسطح جسدًا — حبيبات فيلم تتحرك مع كل إطار، ورق وقصاصات وتمزيق، هالفتون وتنقيط طباعي، زجاج يجمّد ما خلفه، كروم وقطيفة وفرو في 3D، وضوضاء إجرائية تصنع جلدًا وصخرًا وماءً وغيمًا — كلها من كود بلا صور مُنزّلة.
> **أقوى دليل:** فيلم `proofs/neon-glow` (طوب إجرائي يتلوّن بضوء اللافتة، أرض مبتلة تعكسها، حبيبات وتظليل أطراف) و`proofs/glass-luxury-logo` (زجاج blur 22px بعمق، ذهب معدني بأربع طبقات) — كلاهما رُندر هنا ونجح في 13/13 فحصًا؛ ومختبر خامات رندرتُه في هذه الحاوية (2026-10-16): حبيبات feTurbulence ببذرة لكل إطار، هالفتون لامبرت، تنقيط Bayer، زجاج، تمزيق ورق، غيوم SVG، طوب مضاء، وكلمة عربية مملوءة بسائل fbm — وMOTION.grain/vignette من motion-kit في وضع الساعة الافتراضية.
> **You can:** grain, print, paper, glass, chrome, plush, fur, noise-built skin/rock/water and living backgrounds in CSS/SVG, Canvas, Pillow, three.js and ffmpeg. **96 powers follow** — ✅ 18 · 🟢 24 · 📦 11 · 🔑 0 · 👁 26 · 📄 16 · 💡 1.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`).

**فحص سريع لهذه الحاوية (2026-10-16):** `render_html.cjs` يرندر صفحات CSS/SVG/Canvas بالوضعين seek وvirtual ✔ · ffmpeg 6.1.1: سلسلة `noise` + `vignette` + `gblur/blend screen` + `pad` تعمل ✔ · WebGL في Chromium هنا يعمل عبر SwiftShader (رندرتُ إطارات `night_boat` بخامة البدن الخشبي والقمر الإجرائي عبر `window.seek` من motion-kit)، لكن وضع virtual في `render_html.cjs` انتهت مهلته (beginFrame 30 s) على صفحة WebGL — استعمل مسار seek · كتل HyperFrames الشيدرية (marble, liquid-metal…) تتطلب WebGPU ولم تُختبر هنا.

## الفهرس / contents
- **الحبيبات والتشطيب السينمائي — Grain & film finish** — TEX-01 … TEX-12 (12)
- **الورق والكولاج والقصاصات — Paper, collage & cut-outs** — TEX-13 … TEX-28 (16)
- **الطباعة: هالفتون وتنقيط وريزو — Print: halftone, dither & riso** — TEX-29 … TEX-39 (11)
- **الزجاج والكروم والأسطح اللامعة — Glass, chrome & gloss** — TEX-40 … TEX-50 (11)
- **الضوضاء الإجرائية والخامات المولّدة — Procedural noise & generated materials** — TEX-51 … TEX-70 (20)
- **الخلفيات الحية والشبكات والجدران — Living backgrounds, grids & walls** — TEX-71 … TEX-83 (13)
- **الخامات ثلاثية الأبعاد — 3D materials** — TEX-84 … TEX-94 (11)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves
- **إضافات v2 — v2 additions** — TEX-X01 … TEX-X02 (2)

## الحبيبات والتشطيب السينمائي — Grain & film finish

_الطبقة الأخيرة فوق كل فيلم: تقتل تدرّج الألوان المتكسّر (banding) وتعطي الإطار جسدًا. دائمًا ببذرة مرتبطة برقم الإطار حتى يبقى الرندر حتميًا._

#### TEX-01 · حبيبات SVG متدرجة قابلة للبحث · Seekable stepped SVG grain (motion-kit) · ✅ مُثبت هنا / proven here
- **ماذا / what:** طبقة feTurbulence رمادية تقفز بين 6 مواضع بخطوات CSS، فتتحرك الحبيبات ويظل كل إطار قابلًا للبحث. — Desaturated feTurbulence overlay that jumps between 6 offsets with steps(1), so grain moves yet every frame is seekable.
- **متى أستخدمها / when:** أي فيلم HTML/GSAP ثنائي الأبعاد — اللمسة الافتراضية الأخيرة.
- **كيف / how:** MOTION.grain(stage,{opacity,blend,freq,seed,z}) builds an SVG with feTurbulence fractalNoise + feColorMatrix saturate 0 on a 200% rect, animated by @keyframes mk-grain-jump 0.6 s steps(1). Pair with MOTION.vignette(stage,{inner:55,strength:.42}). Rendered here in virtual-time mode: frame-to-frame change only at the step boundaries, corners darkened 205→152 luma. **أرقام / params:** opacity .09 (projects use .05–.07), soft-light, baseFrequency .9, 2 octaves, 0.6 s loop of 6 positions; vignette inner 55%, strength .42–.5.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:440` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:440` · `kosif-one/projects/thursday-dua-animation/source/index.html` · `kosif-one/projects/whatsapp-motion/projects/success/index.html`

#### TEX-02 · حبيبات ببذرة رقم الإطار · Frame-seeded grain (seek pages) · ✅ مُثبت هنا / proven here
- **ماذا / what:** بدل الحركة بالـCSS، غيّر seed للفلتر من رقم الإطار داخل seek(t) فتولد حبيبات جديدة كل إطار بلا عشوائية. — Inside seek(t) set the feTurbulence seed from the frame number, so grain is fresh every frame and still deterministic.
- **متى أستخدمها / when:** صفحات seek (html-canvas starter) أو أي رندر يجب أن يتطابق بايتًا ببايت.
- **كيف / how:** Keep one <filter><feTurbulence type=fractalNoise baseFrequency=.9 numOctaves=2> + saturate 0 over the stage with mix-blend-mode:soft-light; in seek: gt.setAttribute("seed", 1 + floor(t*24) % 97). For canvas, pre-make a 192×192 grey tile and translate it by a hash of the frame (Basma MK.grain). Rendered here: mean frame-to-frame delta 2.7 luma on a 360 px panel at 24 fps. **أرقام / params:** refresh 12–24 Hz; opacity 2–9%; soft-light or overlay.

```js
const turb = document.querySelector('#grain feTurbulence');
function seek(t){                       // deterministic grain, new every frame
  turb.setAttribute('seed', 1 + Math.floor(t * 24) % 97);
  /* …draw the rest of the frame… */
}
```

- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html` · `app/public/js/00_editor.js:75` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`

#### TEX-03 · حبيبات غاوسية في Pillow · Seeded Gaussian luminance grain (Studio painter) · 🟢 جاهز / ready
- **ماذا / what:** عملية grain(amount, seed) في رسام KOSIF Studio تضيف حبيبات ضوئية ثابتة البذرة على الإطار كله. — KOSIF Studio painter op grain(amount, seed) adds seeded Gaussian luminance grain over the whole frame.
- **متى أستخدمها / when:** صور ثابتة وأفلام مرسومة بـ render.py (الحوت، البطة، الإعلان).
- **كيف / how:** Add grain() as the last op of the last step; keep amount tiny because H.264 smears it anyway; same seed across frames for a static print look, seed=frame for live grain. **أرقام / params:** typical .012–.02 (whale .018, duck .02, ad .012).
- **الدليل / proof:** `kosif-studio/render.py:791` · `kosif-studio/references/drawing-guide.md`

#### TEX-04 · سلسلة تشطيب ffmpeg · ffmpeg film finish chain · ✅ مُثبت هنا / proven here
- **ماذا / what:** بعد التلوين: حبيبات زمنية، تظليل أطراف π/5، هالة توهج خفيفة بالمزج screen، وأشرطة سينما 2.39:1 — في أمر واحد. — After grading: temporal grain, π/5 vignette, a light screen-blended bloom and 2.39:1 bars — one filtergraph.
- **متى أستخدمها / when:** مونتاج فيديو حقيقي أو تشطيب نهائي لأي MP4 بلا متصفح.
- **كيف / how:** Ran here on a 2 s test source (50 frames, OK). Order: grade → bloom → grain → vignette → bars; grain last-but-one so it is not blurred. For Remotion, a light-leak overlay sits on TransitionSeries.Overlay. **أرقام / params:** noise=alls=6–10:allf=t+u; vignette=PI/5; gblur sigma 20 + blend screen 0.25; letterbox via pad/drawbox.

```bash
ffmpeg -i in.mp4 -filter_complex "[0]split[a][b];[b]gblur=sigma=20[g];\
[a][g]blend=all_mode=screen:all_opacity=0.25,noise=alls=8:allf=t+u,vignette=PI/5" \
  -c:v libx264 -crf 17 -pix_fmt yuv420p -c:a copy out.mp4
```

- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/transitions.md`

#### TEX-05 · مطابقة اللوك: تعتيم وحبيبات وأشرطة · Look replication solver (vignette/grain/letterbox/fades) · 🟢 جاهز / ready
- **ماذا / what:** kosif-mimic يحسب قوة التعتيم من نسبة إضاءة الزوايا إلى المركز، ويعوّض الحبيبات عما يمسحه ضغط H.264 حسب crf. — kosif-mimic solves vignette strength from the corner/centre luma ratio and boosts grain sigma to survive H.264 at a given crf.
- **متى أستخدمها / when:** «اعمل مثل هذا الفيديو» — حين تقيس مرجعًا وتعيد لوكه.
- **كيف / how:** mm_build.solve_vignette(ratio) → strength; grain_gain(crf) → multiplier for the measured grain; then add letterbox and fades as measured. Measure on the reference, never guess. **أرقام / params:** crf 17 default.
- **الدليل / proof:** `100-superskills/skills/kosif-mimic/scripts/mm_build.py:130`

#### TEX-06 · حبيبات ثلاثية الأبعاد (FilmPass) · 3D film grain pass · 🟢 جاهز / ready
- **ماذا / what:** تمريرة FilmPass في three-kit بزمن مربوط بإطار الإخراج، فتتحرك الحبيبات بحتمية في مشاهد WebGL. — three-kit post.film (three.js FilmPass) with its time uniform written from the output frame.
- **متى أستخدمها / when:** كل مشهد three.js يُرندر إلى فيديو.
- **كيف / how:** makeFrameLoop sets film.uniforms.time = t each frame; keep intensity low; TSL alternative film(color,{intensity,grayscale}) or a hash(uv+time) overlay in GLSL. **أرقام / params:** intensity .16 (lab .05); editorial ceiling ~2–3% visible grain.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:402` · `kosif-studio/motion/kit/three-kit.js` · `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/post-processing.md`

#### TEX-07 · حبيبات 2% وانحراف لوني على الحواف · 2% grain + edge-only chromatic aberration · 📄 موصوف / documented only
- **ماذا / what:** قاعدة أواردز: حبيبات أحادية 2% لا تتجاوز 3%، وانزياح RGB صغير على أطراف الكادر فقط كعدسة حقيقية. — Awwwards rule: monochrome grain at 2% (never above 3%) and a tiny RGB split only near the frame edges.
- **متى أستخدمها / when:** واجهات وأفلام نظيفة فاخرة — حين تريد عمقًا بلا اتساخ.
- **كيف / how:** Post pass offsetting R/B by distance from centre (shift ∝ r², 0 at centre); grain seeded per frame. **أرقام / params:** grain .02 (≤.03); RGB shift .002 uv at edges only.
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### TEX-08 · تلوين عتيق بغبار وخدوش · Vintage film grade: dust, scratches, split-tone · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** تمريرة أخيرة: تقسيم لوني دافئ/بنفسجي، حبيبات متحركة، ذرات غبار متفرقة وخدوش عمودية، تعتيم وتوهج خفيف. — Final pass: warm/violet split-tone, animated grain, sparse dust specks and vertical scratches, slight vignette and bloom.
- **متى أستخدمها / when:** أرشيف، حنين، وثائقي، قصة «زمان».
- **كيف / how:** Canvas/ffmpeg: grain .08; ~20 dust specks per frame at seeded random positions (1–3 px, life 1–2 frames); 0–2 vertical scratches 1 px at 30% white drifting; bloom threshold .8; projector flicker = 1 ± .03 noise. **أرقام / params:** grain .08, dust 20/frame, bloom threshold .8.
- **الدليل / proof:** `kosif-tool/styles/pm-nft-chen-5f8bb0` · `fastify-motion-bro/scripts/profiles/vox-history.mjs:11`
- **أساليب / styles:** `style:pm-nft-chen-5f8bb0`

#### TEX-09 · أسود دافئ بحبيبات وتعتيم · Warm-black grain + vignette grade · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** خلفية سوداء دافئة ‎#0a0907‎ بحبيبات متجددة كل إطار 3–10% وتعتيم قوي يجعل اللون المسطح يُقرأ كطباعة فاخرة. — Warm black #0a0907 with per-frame grain 3–10% and a strong radial vignette so flat colour reads premium.
- **متى أستخدمها / when:** افتتاحيات فاخرة، تريلر، عروض ليلية.
- **كيف / how:** Regenerate noise every frame; vignette to black at corners; on light/red scenes push edges −35% luminance. **أرقام / params:** grain 3–5% (gritty 8–10%), vignette 30–60% at corners.
- **الدليل / proof:** `kosif-tool/styles/pm-robj3d3-b18fad` · `kosif-tool/styles/pm-spearwtf-3c1fd1` · `kosif-tool/styles/pm-grace-sunnyy-29bc61` · `kosif-tool/styles/pm-sahildesigner23-ee3155`
- **أساليب / styles:** `style:pm-robj3d3-b18fad` · `style:pm-spearwtf-3c1fd1` · `style:pm-grace-sunnyy-29bc61` · `style:pm-sahildesigner23-ee3155`

#### TEX-10 · درجة الورق التحريري · Editorial paper grade · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** قاعدة كريمية ‎#efecdd‎ + ضوضاء 3% + تعتيم 10%، حبر شبه أسود ولون أحمر واحد للتوكيد. — Cream #efecdd base, 3% noise, 10% vignette, near-black ink and a single red accent.
- **متى أستخدمها / when:** شرح تحريري، مقال مرئي، قصص بيانات هادئة.
- **كيف / how:** Static paper noise (not boiling), vignette 10%; keep data labels clean of texture. **أرقام / params:** noise 3%, vignette 10%.
- **الدليل / proof:** `kosif-tool/styles/pm-hbcoop-de365c`
- **أساليب / styles:** `style:pm-hbcoop-de365c`

#### TEX-11 · حبيبات مع زوايا HUD · Film grain + HUD corners · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** حبيبات 6–10% متجددة كل إطار مع أقواس زوايا وملصقات mono صغيرة ومؤشر تقدم. — Per-frame grain 6–10% plus corner brackets, micro mono labels and a progress meter.
- **متى أستخدمها / when:** تقني، تصوير «كاميرا»، عروض منتجات بروح التصوير.
- **كيف / how:** Grain layer under a fixed HUD layer (HUD stays crisp, outside the camera transform). **أرقام / params:** grain 6–10%.
- **الدليل / proof:** `kosif-tool/styles/pm-madhav-xo-f97f20`
- **أساليب / styles:** `style:pm-madhav-xo-f97f20`

#### TEX-12 · عنوان محبب متوهج · Grain-glow title card · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** عنوان ثقيل مملوء بخامة ضوضاء مع توهج خارجي 20px، يظهر من نقطة نجم واحدة. — Heavy title filled with noise texture, 20 px outer glow, fading in from a single star point.
- **متى أستخدمها / when:** بطاقة عنوان فيلم أو أغنية.
- **كيف / how:** Noise texture via mask (TEX-62) at opacity .5; glow = blurred copy; scale-in from a star at the title centre. **أرقام / params:** noise .5; glow 20 px.
- **الدليل / proof:** `kosif-tool/styles/pm-nolkeeg-bf062e`
- **أساليب / styles:** `style:pm-nolkeeg-bf062e`

## الورق والكولاج والقصاصات — Paper, collage & cut-outs

_الخامة الملموسة: ورق ثابت، قصاصات بحواف بيضاء، شريط لاصق، تمزيق — والقاعدة: الورق لا يغلي إلا إذا طلب الأسلوب ذلك._

#### TEX-13 · خلفية ورق ثابتة 5–10% · Static paper/board texture · 📄 موصوف / documented only
- **ماذا / what:** طبقة ورق أو كرتون بشفافية 5–10% تبقى ثابتة؛ الغليان (boil) فقط حين يطلبه الأسلوب. — Paper or board overlay at 5–10% that stays still unless the style asks for boil.
- **متى أستخدمها / when:** كل أسلوب مرسوم يدويًا أو كولاج.
- **كيف / how:** Procedural: feTurbulence baseFrequency .6–.9 + feColorMatrix to paper tone, multiply over the scene; or a licensed paper PNG. Same seed every frame (static). **أرقام / params:** opacity 5–10%.
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:18` · `fastify-motion-bro/scripts/profiles/stickman.mjs:4`

#### TEX-14 · ورق ألوان مائية · Watercolour paper ground · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ورق كريمي ‎#f3e8cf‎ بملمس بارز مضروب فوق كل مشهد، وتلال بغسلة مائية وحافة حبر مرتجفة. — Cream #f3e8cf embossed paper multiplied over every scene; hills as a wobbly ink arc with a watercolour wash.
- **متى أستخدمها / when:** قصص أطفال، حكايات، شعر هادئ.
- **كيف / how:** Paper = noise height → normal-ish emboss (TEX-56 normalFromHeight or two offset noise layers) multiply; wash = fill #c6c7a4 with darker blotches from low-frequency noise, edge darkening 1–2 px. **أرقام / params:** paper #f3e8cf; wash #c6c7a4.
- **الدليل / proof:** `kosif-tool/styles/pm-abderrahmen-g-9e8ed0`
- **أساليب / styles:** `style:pm-abderrahmen-g-9e8ed0`

#### TEX-15 · رق قديم بحواف ونقاط رمل · Parchment vignette + sand stipple · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** تدرج شعاعي من ‎#ead9b5‎ إلى ‎#c9aa72‎ مع نقاط رمل داخل الصحارى فقط وخطوط طي خافتة. — Radial #ead9b5→#c9aa72 parchment, sand dots only inside deserts (point-in-polygon rejects seas) and faint fold lines.
- **متى أستخدمها / when:** خرائط رحلات، تاريخ، سيرة.
- **كيف / how:** Seeded random dots r .6–1 px at 30% inside land polygons; fold lines 1 px at 8%; vignette darker edges. **أرقام / params:** dot r .6–1 px, opacity .3.
- **الدليل / proof:** `kosif-tool/styles/map-journey`
- **أساليب / styles:** `style:map-journey`

#### TEX-16 · كولاج ورقي (S04) · Paper collage style (S04) · 📄 موصوف / documented only
- **ماذا / what:** قصاصات وشريط لاصق وحواف ملموسة؛ الطبقات تقفز بخفة وتتمزق وتنقلب كالصفحات. — Cut-outs, tape, tactile edges; layers hop lightly, tear and page-flip.
- **متى أستخدمها / when:** محتوى شخصي ومرح يُبنى من صور المستخدم.
- **كيف / how:** PNG cut-outs + paper texture (procedural feTurbulence or licensed), small rotations ±2–6°, soft drop shadows; render with render_html.cjs. Too many textures crowd the frame — 2–3 materials max. **أرقام / params:** cost medium; ideas MG-004 MG-076 MG-101 MG-102 MG-103 MG-110.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### TEX-17 · لوحة قصاصات وشريط يثبّتها · Cut-out board + tape pin (MG-101/102) · 📄 موصوف / documented only
- **ماذا / what:** صور مقصوصة تدخل بزوايا صغيرة وتبني لوحة حول عنوان، ثم شريط لاصق يمر على زاوية صورة ليثبتها. — Cut photos enter at small angles and build a board around a title; a tape strip then pins one corner.
- **متى أستخدمها / when:** ملخص رحلة، ذكريات، «قبل وبعد».
- **كيف / how:** MG-101: 0–1 s background, 1–4 s cut-outs, 4–7 s read; few rotation/scale keys per layer. MG-102: 0–1 s photo, 1–2 s tape revealed by a mask, 2–4 s hold; tape shadow very light (it sits on the paper). **أرقام / params:** 7 s / 4 s.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-collage-textures.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### TEX-18 · تمزيق ورق يكشف ما تحته · Paper tear reveal · ✅ مُثبت هنا / proven here
- **ماذا / what:** شقّ غير منتظم ينفتح من الوسط بحافتين ورقيتين بلب أبيض وظل، فيكشف المشهد التالي. — A ragged slit opens from the middle with two paper edges, white core and shadow, revealing the next scene.
- **متى أستخدمها / when:** انتقال كولاج، كشف منتج، «الحقيقة خلف…».
- **كيف / how:** Jittered polygon edge (one sample per 12 px, ±13 px seeded) shared by both halves; translate halves apart ±170 px with a tiny rotation, shadowBlur 14, 4 px white stroke on the torn edge; never a smooth edge. Rendered here (lab, Canvas). HyperFrames ships torn-paper-rip (direction, tone cream|kraft|white, roughness 20–90) and paper-collage-reveal (4–8 scraps). **أرقام / params:** slit 0–0.7 s, tear 0.7–2.5 s, read 2.5–4 s; edge jitter ±13 px; shadow 14 px.
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0 / HyperFrames components are Apache-2.0.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-collage-textures.md` · `kosif-one/vendor/hyperframes/registry/components/torn-paper-rip/torn-paper-rip.html` · `kosif-one/vendor/hyperframes/registry/components/paper-collage-reveal/paper-collage-reveal.html`

#### TEX-19 · رسمة ممسوحة كملصق · Scanned drawing as sticker cut-out · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** رسمة يدوية تُقص إلى ألفا مع حد أبيض 6–10px وظل 4px ناعم فتبدو ملصقًا ورقيًا. — Mask a hand-drawn scan to alpha, dilate a 6–10 px white outline and add a soft 4 px drop shadow — a paper sticker.
- **متى أستخدمها / when:** شخصيات يرسمها المستخدم، قصص أطفال، كولاج.
- **كيف / how:** Pillow: alpha → MaxFilter(13) for the outline → white at 90% under the art → shadow = blurred alpha offset 2 px at 20%. Background knockout by corner colour (TEX-28) first if the scan has a flat ground. **أرقام / params:** outline #ffffff 90%, 6–10 px; shadow rgba(0,0,0,.2) offset 2 px.
- **الدليل / proof:** `kosif-tool/styles/pm-abderrahmen-g-9e8ed0` · `kosif-tool/styles/pm-koldo2k-5cff87`
- **أساليب / styles:** `style:pm-abderrahmen-g-9e8ed0` · `style:pm-koldo2k-5cff87`

#### TEX-20 · قصاصة جريدة ونقش · Newspaper / engraving cut-out · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** صورة أبيض وأسود بهالفتون أو نقش، بحد أبيض 6px وظل 30% — جمالية الأرشيف والوثائقي. — B&W halftone or engraved object with a 6 px white border and 30% shadow — archival/documentary look.
- **متى أستخدمها / when:** تاريخ، أرشيف، تعليق سياسي.
- **كيف / how:** Desaturate 100%, apply halftone (TEX-34) or engraving (TEX-39 shader effect), then the sticker recipe; on white grounds keep the etching unbordered. **أرقام / params:** stroke white 6 px, shadow blur 12 px at 30%.
- **الدليل / proof:** `kosif-tool/styles/pm-koldo2k-5cff87` · `kosif-tool/styles/pm-lexnlin-038035`
- **أساليب / styles:** `style:pm-koldo2k-5cff87` · `style:pm-lexnlin-038035`

#### TEX-21 · قفل أسلوب الأرشيف · Archival scrapbook style lock · 🟢 جاهز / ready
- **ماذا / what:** وصف ثابت يُلصق في كل لقطة vox-history: جرائد بنية، حبيبات، خطوط مسح، هالفتون، صور ممزقة بحواف بيضاء، دبابيس وخيط أحمر، وميض بروجكتر. — A STYLE constant pasted into every vox-history clip prompt: sepia newsprint, grain, scan lines, halftone, torn photos, tacks, red thread, projector flicker.
- **متى أستخدمها / when:** حين تولّد لقطات بالذكاء الاصطناعي لقصة تاريخية وتريدها متسقة.
- **كيف / how:** Repeat the exact same style block in every generation request; keep stamps generic (no real logos); add stop-motion entrances in the edit.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/vox-history.mjs:11` · `fastify-motion-bro/skills/vox-history/SKILL.md:12`

#### TEX-22 · قفل الخلفية الورقية · Paper sketch background lock · 🟢 جاهز / ready
- **ماذا / what:** خلفية ورق/سبورة مرسومة يدويًا بلا عمق واقعي، مكررة في كل لقطات stickman حتى تطابق الشخصية ثنائية الأبعاد. — A flat hand-drawn paper/whiteboard background block repeated in all stickman prompts to match the 2D figure.
- **متى أستخدمها / when:** سلاسل لقطات مولدة لشخصية عصا أو شرح مرسوم.
- **كيف / how:** BACKGROUNDS.paper string reused verbatim in all 5 prompts; no photoreal depth words.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/stickman.mjs:4`

#### TEX-23 · الورق المقصوص بعمق ثلاث طبقات · Paper cut-out style (3-depth parallax) · 📄 موصوف / documented only
- **ماذا / what:** ورق كريمي ‎#F6EBD9‎ بألوان ورقية خافتة وظل ورقي صلب، بارالاكس بثلاثة أعماق وتمايل خفيف. — Cream #F6EBD9 paper, muted paper colours, a hard paper drop shadow, 3-depth parallax and gentle sway.
- **متى أستخدمها / when:** قصص تعليمية دافئة، تراث، أطفال.
- **كيف / how:** Layers at depth 1 / 0.6 / 0.3; filter drop-shadow(0 8px 0 rgba(0,0,0,.18)); sway ±2° sine; type Amiri 700 / Lateef + Tajawal 500. Scaffold the base style with python3 tools/kosif.py scaffold cutout-paper <dir> (paper texture 5–10%, hinge-pivot rigs, on twos). **أرقام / params:** #F6EBD9 #D96B4A #5B8C5A #3B6EA8; shadow 0 8px 0 .18; parallax 1/0.6/0.3; sway ±2°.
- **الدليل / proof:** `100-superskills/skills/trend-animation-styles/references/styles.md` · `kosif-tool/styles/cutout-paper/SKILL.md` · `kosif-tool/styles/cutout-paper/STYLE.json`

#### TEX-24 · ستوب موشن بارتعاش البذرة · Stop-motion seeded hold jitter · 📄 موصوف / documented only
- **ماذا / what:** تحريك على الاثنين (12 إطارًا/ث) مع ارتعاش ±1.5px و±0.6° لكل إطار ممسوك من بذرة، فيتنفس المشهد كالصلصال. — Animate on twos with a seeded ±1.5 px / ±0.6° jitter per held frame so the set breathes like stop-motion.
- **متى أستخدمها / when:** صلصال، ألعاب، منتجات «يدوية».
- **كيف / how:** hold = floor(t*12); jitter = hash(hold, layerId) → dx, dy, rot; photo textures + contact shadows. Scaffold: python3 tools/kosif.py scaffold stop-motion <dir>. **أرقام / params:** on twos; ±1.5 px, ±0.6°.
- **الدليل / proof:** `kosif-tool/styles/stop-motion/SKILL.md` · `kosif-tool/styles/stop-motion/STYLE.json` · `kosif-tool/styles/pm-davidshulmanfl-371638/BRIEF.md`
- **أساليب / styles:** `style:pm-davidshulmanfl-371638`

#### TEX-25 · صلصال مطفي وبصمات · Claymation matte + fingerprint texture · 📄 موصوف / documented only
- **ماذا / what:** شخصيات صلصال بخامة مطفية (roughness 0.6–0.9) وانضغاط وتمدد، مع طبقة بصمات 12% وضوء مفتاحي علوي-يسار. — Clay characters with matte material (roughness 0.6–0.9) and squash/stretch, plus a 12% fingerprint overlay and baked top-left key light.
- **متى أستخدمها / when:** إعلانات مرحة، أطفال، شخصيات لطيفة.
- **كيف / how:** Three.js MeshStandardMaterial roughness .6–.9 or 2D soft shading; squash scaleY .7 / scaleX 1.3 over 80 ms; fingerprint = procedural concentric ridges (sin of distance + noise) multiplied at 12%. Scaffold: python3 tools/kosif.py scaffold claymation <dir>. **أرقام / params:** roughness .6–.9; squash .7/1.3 in 80 ms; fingerprints 12% multiply.
- **الدليل / proof:** `kosif-tool/styles/claymation/SKILL.md` · `kosif-tool/styles/claymation/STYLE.json` · `kosif-tool/styles/pm-davidshulmanfl-371638/BRIEF.md`
- **أساليب / styles:** `style:pm-davidshulmanfl-371638`

#### TEX-26 · مشهد أطفال بالكرايون · Crayon paper-craft kids scene · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** أشكال بملمس كرايون (شمس، غيوم، قوس قزح، تلال) بحد داكن 3px ودمية زغبية بعيون كبيرة. — Crayon-textured shapes (sun, clouds, rainbow, hills) with 3 px dark outlines and a fuzzy big-eyed puppet.
- **متى أستخدمها / when:** محتوى أطفال، حضانات، تعليم مبكر.
- **كيف / how:** Fill with a clipped stroke-hatch or noise threshold texture (TEX-81 hatching), outline 3 px; speech balloon with two-colour bubbly text. **أرقام / params:** texture fill + 3 px dark outline.
- **الدليل / proof:** `kosif-tool/styles/pm-emollick-8661a8`
- **أساليب / styles:** `style:pm-emollick-8661a8`

#### TEX-27 · النقص المقصود · Intentional imperfection (wabi-sabi) · 📄 موصوف / documented only
- **ماذا / what:** دفء من عدم التماثل الخفيف وتفاوت سماكة الخط وملمس الورق، مع إبقاء أجزاء البيانات نظيفة. — Warmth from slight asymmetry, varied stroke width and paper texture — but keep data parts clean.
- **متى أستخدمها / when:** أي أسلوب يدوي يبدو «رقميًا جدًا».
- **كيف / how:** Rotate elements ±1–2°, vary stroke width ±15%, irregular spacing; paper overlay; never on numbers/labels. **أرقام / params:** rotation ±1–2°.
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3743-wabi-sabi-imperfection`

#### TEX-28 · إزالة الخلفية بلون الزاوية · Corner-colour background knockout · 🟢 جاهز / ready
- **ماذا / what:** يعزل الرسمة أو المشهد بحذف كل ما يشبه متوسط لون الزوايا ضمن تسامح RGB. — Floats a scene by flood-removing the background that matches the averaged corner colour within an RGB tolerance.
- **متى أستخدمها / when:** تحويل رسمة على ورق أبيض أو لقطة شاشة إلى قصاصة شفافة.
- **كيف / how:** python3 knockout.py in.png out.png with Pillow; TOL env sets the Euclidean tolerance; follow with the sticker outline (TEX-19). **أرقام / params:** TOL=34 Euclidean RGB.
- **⚖️ ترخيص / license:** MIT (vendor scroll-world).
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/references/knockout.py:25`

## الطباعة: هالفتون وتنقيط وريزو — Print: halftone, dither & riso

_نقط بحجم الضوء، شبكات مائلة، Bayer وريزو — الخامة الطباعية التي تجعل الشكل المسطح يبدو مطبوعًا لا مرسومًا بالكمبيوتر._

#### TEX-29 · تظليل كرة بالهالفتون · Halftone sphere (Lambert dots) · ✅ مُثبت هنا / proven here
- **ماذا / what:** شبكة نقاط نصف قطر كل منها = إضاءة لامبرت لكرة افتراضية، والضوء يدور فتتحرك الظلال نقطة نقطة. — Dot grid whose radius = Lambert(normal·light) of a virtual sphere; the light orbits so shading moves dot by dot.
- **متى أستخدمها / when:** أيقونات، كواكب، منتجات بأسلوب طباعة.
- **كيف / how:** For each grid cell inside the disc: n = (dx, dy, √(1−r²)); r_dot = rmax·max(0, n·L) + .4. Rendered here (Canvas lab, light orbiting at 2 rad/s). **أرقام / params:** grid 14 px, rmax 6 px, #f04a2a on #f6efe3.

```js
for (let y = 7; y < H; y += 14) for (let x = 7; x < W; x += 14) {
  const dx = (x - cx) / R, dy = (y - cy) / R, r2 = dx*dx + dy*dy;
  if (r2 > 1) continue;
  const l = Math.max(0, dx*L[0] + dy*L[1] + Math.sqrt(1 - r2)*L[2]);
  ctx.beginPath(); ctx.arc(x, y, 6*l + .4, 0, 7); ctx.fill();
}
```

- **الدليل / proof:** `kosif-tool/styles/pm-ayushunleashed-ece3e3`
- **أساليب / styles:** `style:pm-ayushunleashed-ece3e3`

#### TEX-30 · هالفتون CMYK · CMYK / gooey halftone · 📄 موصوف / documented only
- **ماذا / what:** نقاط بحجم الإضاءة؛ نسخة CMYK بأربع شبكات مائلة C15 M75 Y0 K45 بمزج طرحي، ونسخة لزجة بـ smooth-min. — Luma-sized dots; CMYK uses four rotated grids C15 M75 Y0 K45 subtractively; a gooey variant uses smooth-min.
- **متى أستخدمها / when:** بوب آرت، مجلات، ملصقات.
- **كيف / how:** GLSL or numpy offline: per channel rotate uv, cell centre, sample 3×3 neighbours to avoid clipping, fwidth antialias; multiply channels. **أرقام / params:** angles C15 M75 Y0 K45.
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### TEX-31 · نقاط هالفتون على القصاصة · Clipped halftone on a cut-out card · 🟢 جاهز / ready
- **ماذا / what:** نقاط كل 10px بنمط قطري بلون النص 8% مقصوصة داخل بطاقة البطل — ملمس طباعة بلا صور. — Dots every 10 px in a diagonal pattern at 8% of the text colour, clipped to the hero card — print feel, no images.
- **متى أستخدمها / when:** بطاقات تحريرية، عناوين، ملصقات.
- **كيف / how:** ctx.clip(card); dot where (floor(x/10s)+floor(y/10s)) % 4 == 0, radius 1.7·scale. **أرقام / params:** cell 10 px; r 1.7 px; 8% alpha.
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:63-66`

#### TEX-32 · موجة هالفتون ومواريه · Halftone ripple & moiré overprint · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شبكة نقاط يقود نصف قطرها حقل موجي شعاعي، وشبكة ثانية بزاوية مختلفة تصنع مواريه الطباعة. — Dot grid driven by a radial wave field; a second screen at another angle creates overprint moiré.
- **متى أستخدمها / when:** خلفيات موسيقية، انتقالات، شعارات.
- **كيف / how:** r = rmax·(.5 + .5·sin(k·d − ω·t)); second grid rotated 30° in another ink with multiply; ring speed 1 ring / 0.5 s. Variants: dot ring (radius by a distance field), corner blobs drifting. **أرقام / params:** 16 px screen, angles 15° & 45°, 1 ring / 0.5 s.
- **الدليل / proof:** `kosif-tool/styles/pm-fionntobin-97b7af` · `kosif-tool/styles/pm-ultimaxbt-bbebf5` · `kosif-tool/styles/pm-rendesr-86be44` · `kosif-tool/styles/pm-polydao-7a572b`
- **أساليب / styles:** `style:pm-fionntobin-97b7af` · `style:pm-ultimaxbt-bbebf5` · `style:pm-rendesr-86be44` · `style:pm-polydao-7a572b`

#### TEX-33 · خلفية أشرطة ضوء منقطة · Halftone light-band backdrop · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** أشرطة تدرج قطرية في الزوايا مملوءة بنقاط هالفتون ونمط دوائر، تتلاشى نحو المركز وتنجرف ببطء. — Diagonal gradient bands at the corners filled with halftone dots and a circuit pattern, radially faded to the centre, drifting.
- **متى أستخدمها / when:** خلفيات تقنية وعروض منتجات.
- **كيف / how:** Mask = radial fade; band angle −35°; dot pitch 6–8 px; opacity .3–.5; drift 5–10 px/s. Sunburst variant: rotating conic rays + dot overlay. **أرقام / params:** angle −35°, pitch 6–8 px, opacity .3–.5.
- **الدليل / proof:** `kosif-tool/styles/pm-elliot-garreffa-f334bc` · `kosif-tool/styles/pm-topi-003-b0e12c`
- **أساليب / styles:** `style:pm-elliot-garreffa-f334bc` · `style:pm-topi-003-b0e12c`

#### TEX-34 · صورة هالفتون ماكرو · Halftone macro image · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شيدر شبكة نقاط فوق صورة رمادية — الصورة الفوتوغرافية تصير ملصقًا مطبوعًا. — Dot-screen shader over a greyscale photo — the photo becomes a printed poster.
- **متى أستخدمها / when:** صور المستخدم في أسلوب جريء أو تحريري.
- **كيف / how:** Greyscale → cell-centre luma → dot radius; or HyperFrames media effect halftone (TEX-39).
- **الدليل / proof:** `kosif-tool/styles/pm-reflex-cloud-72ffe5`
- **أساليب / styles:** `style:pm-reflex-cloud-72ffe5`

#### TEX-35 · سماء متدرجة بتنقيط Bayer · Bayer-dithered sky + stepped stars · ✅ مُثبت هنا / proven here
- **ماذا / what:** تدرج سماء بثلاث إلى أربع درجات نيلية/بنفسجية مع تنقيط Bayer ‏4×4، ونجوم 1–2px تومض بخطوات. — Sky gradient quantised to 3–4 indigo/purple bands with a 4×4 Bayer matrix; 1–2 px stars twinkling in steps.
- **متى أستخدمها / when:** بكسل آرت، ريترو، ألعاب، ليل هادئ.
- **كيف / how:** v = y/H·(n−1); i = floor(v); pick band i+1 when frac(v) > (B[y&3][x&3]+.5)/16. Stars toggle at 4 fps from a seeded list. Rendered here (Canvas lab). **أرقام / params:** 4×4 Bayer [0 8 2 10 / 12 4 14 6 / 3 11 1 9 / 15 7 13 5]; twinkle 4 fps.
- **الدليل / proof:** `kosif-tool/styles/pm-0xevinho-3777d8`
- **أساليب / styles:** `style:pm-0xevinho-3777d8`

#### TEX-36 · تعبئة تنقيط أحادية البت · 1-bit dither fill with threshold sweep · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** تنقيط Bayer أو رقعة شطرنج برتقالي على أسود يملأ منطقة، ويُحرّك العتبة لعمل مسح. — Bayer/checker dither of orange on black filling a region; animate the threshold to sweep.
- **متى أستخدمها / when:** انتقالات ريترو، كشف شعار، واجهات طرفية.
- **كيف / how:** threshold(t) from 0→1 over 600 ms; cell 8 px (scale the Bayer matrix ×2); pixelated rendering (imageSmoothingEnabled=false). **أرقام / params:** cell 8 px, sweep 600 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-anthonyriera-9b1b2a`
- **أساليب / styles:** `style:pm-anthonyriera-9b1b2a`

#### TEX-37 · تعبئة حبيبات ريزو · Riso grain fill · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** قناع عتبة من feTurbulence على أشكال مسطحة بحبرين أو ثلاثة، فيبدو كطباعة ريزوغراف. — feTurbulence threshold mask on flat shapes in 2–3 inks — risograph look.
- **متى أستخدمها / when:** ملصقات فنية، أغلفة، هوية مرحة.
- **كيف / how:** feTurbulence baseFrequency .9 → feComponentTransfer discrete/threshold → feComposite in with the shape; slight misregistration 1–2 px per ink. **أرقام / params:** freq .9, 2–3 inks.
- **الدليل / proof:** `kosif-tool/styles/pm-rneayan-474bcf`
- **أساليب / styles:** `style:pm-rneayan-474bcf`

#### TEX-38 · طبقة حبيبات نقطية · Dot-lattice grain overlay · ✅ مُثبت هنا / proven here
- **ماذا / what:** شبكة نقاط دقيقة 0.6px كل 6px فوق خلفية داكنة تعطي إحساس الطباعة بلا صور. — A 0.6 px dot lattice every 6 px over a dark hero gives a printed feel with no images.
- **متى أستخدمها / when:** أبطال واجهات داكنة، بطاقات، شرائح.
- **كيف / how:** ::after{inset:0; background-image:radial-gradient(#ffffff16 .6px,transparent .6px); background-size:6px 6px; opacity:.25; pointer-events:none}. Rendered here: at #fff16 it is almost invisible after H.264 — go to #fff30–40 for video. **أرقام / params:** dot .6 px; grid 6 px; opacity .25 (web) — stronger for video.
- **الدليل / proof:** `kosif-audit-studio/studio.css:58`

#### TEX-39 · مؤثرات الشيدر على الصورة والفيديو (18) · HyperFrames shader media effects (18 keys) · 📦 بأمر تثبيت / one install
- **ماذا / what:** مؤثرات لحظية على اللقطات: blur, pixelate, chromaBleed, tapeDamage, filmArtifacts, halftone, twoInkPrint, ascii, dither, bloom, monoScreen, scanlines, chromaticAberration, crtCurvature, digitalGlitch, engraving, crosshatch, kuwahara + grain وvignette. — Realtime footage effects: 18 keys from blur to kuwahara painterly, plus grain + vignette details.
- **متى أستخدمها / when:** تحويل فيديو المستخدم إلى طباعة/شريط/نقش/لوحة داخل مشروع HyperFrames.
- **كيف / how:** Set effects.<key> 0..1 in data-color-grading on the media element (media-treatment); never fake them with CSS overlays. Not rendered here.
- **📦 تثبيت / install:** `npm i -D hyperframes`
- **⚖️ ترخيص / license:** Apache-2.0.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/core/src/colorGrading.ts` · `kosif-one/vendor/hyperframes/skills/media-use/references/media-treatments.md`

## الزجاج والكروم والأسطح اللامعة — Glass, chrome & gloss

_الزجاج يحتاج شيئًا خلفه ليجمّده، والكروم يحتاج عالمًا ليعكسه — بلا خلفية حية يصير الزجاج رماديًا ميتًا._

#### TEX-40 · بطاقة زجاجية فاخرة بعمق · Luxury depth glass cards · ✅ مُثبت هنا / proven here
- **ماذا / what:** بطاقات زجاج تنزلق بعمق وبارالاكس فوق شبكة تدرج حية، بحافة علوية مضيئة وظلين ناعمين. — Glass cards sliding in depth and parallax over a live mesh gradient, with a lit top edge and two soft shadows.
- **متى أستخدمها / when:** هوية فاخرة، كشف شعار، عرض قيم.
- **كيف / how:** background linear rgba(255,255,255,.16)→.035; backdrop-filter blur(22px) saturate(150%); radius 30 px; inset top highlight 1 px .45 + inner edge 1 px .13; shadows 0 40px 80px −30px (.7) and 0 12px 24px −8px (.35); put a faint star pattern/bokeh under the cards so the frost is visible. Rendered here in proofs/glass-luxury-logo (13/13) and in the texture lab. **أرقام / params:** blur 22 px, saturate 150%, depths 1.0/0.7/0.45, defocus 1.6 + 3.2·(1−depth) px.
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/glass-luxury-logo/README.md` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/glass-luxury-logo/index.html`

#### TEX-41 · وصفة الزجاج الداكن · Dark-only frosted glass panel recipe · 📄 موصوف / documented only
- **ماذا / what:** لوح زجاجي: تمويه خلفي 28px (40px للنوافذ البارزة)، تعبئة بيضاء 5%، حد متدرج من الأعلى، وظل محيطي واسع — على الخلفيات الداكنة فقط. — Frosted panel: 28 px backdrop blur (40 px spotlight), 5% white fill, top-lit gradient border, wide ambient shadow — dark backgrounds only.
- **متى أستخدمها / when:** بطاقات UI فوق مشاهد داكنة أو ثلاثية الأبعاد.
- **كيف / how:** backdrop-filter blur(28px); background rgba(255,255,255,.05); 1px border with a 180° gradient .12→.02 (border-image or mask trick); box-shadow 0 24px 80px rgba(0,0,0,.25). Badge variant: pill radius 9999, blur 12 px, border .15, cyan glow 0 8px 32px rgba(56,189,248,.2). **أرقام / params:** blur 28/40 px; fill .05; border .12→.02; shadow 0 24px 80px .25.
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:34`

#### TEX-42 · وصفات زجاج الواجهات · Glassmorphism UI recipes (menus, toasts, bars, dialogs) · 🟢 جاهز / ready
- **ماذا / what:** أسطح شفافة بتمويه مع تشبع معزز لقوائم وتلميحات وتنبيهات وشريط علوي ونافذة حوار — من أنظمة تصميم المالك. — Translucent saturated-blur surfaces for dropdowns, tooltips, toasts, sticky top bars and dialogs — from the owner design systems.
- **متى أستخدمها / when:** محاكاة واجهة تطبيق داخل فيلم (UI demo).
- **كيف / how:** dropdown saturate(180%) blur(24px) radius 24; tooltip blur(20px); toast saturate(180%) blur(22px); top bar color-mix(surface 92%) + saturate(1.4) blur(10px); scrim rgba(0,0,0,.32) blur(6px); audit topbars color-mix(var(--card) 92–96%) + blur 12–20 px; dialog radius 22 shadow 0 30px 100px #15111a45. **أرقام / params:** blur 6/10/12–24 px; saturate 140–180%.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/components.css:196` · `kosif-earth-ci-fork/ui/ds/components.css:224` · `kosif-audit-pro/app/globals.css:308` · `kosif-audit-studio/studio.css:117`

#### TEX-43 · غلاف زجاجي فوق عالم ثلاثي · Glass shell over a live 3D background · 🟢 جاهز / ready
- **ماذا / what:** بطاقة تطفو كزجاج فوق عالم WebGL بملء الشاشة يظهر خلال 1.6 ث، مع غسلة زعفرانية. — A UI card floats as frosted glass over a full-screen WebGL world that fades in over 1.6 s, with a saffron wash.
- **متى أستخدمها / when:** صفحات هبوط ومقدمات هوية فوق مشهد ثلاثي.
- **كيف / how:** .world fixed inset 0 opacity 0→1 1.6 s; .shell rgba(255,253,249,.96) + blur(14px) (.94 on phones); panel gradient 180° rgba(29,24,20,.12)→.58 + saffron 160° rgba(217,83,14,.26). **أرقام / params:** blur 14 px; alpha .96/.94; fade 1.6 s.
- **الدليل / proof:** `kosif-earth-ci-fork/unlock.html:75` · `kosif-earth-ci-fork/docs/design/SQC-IDENTITY-ar.md`

#### TEX-44 · زجاج سائل بانكسار الحافة · Liquid glass control (edge refraction) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** جسم مموّه 14px، وفي شريط حافة 12px نسخة مكبرة 1.06× تحاكي الانكسار، مع تعبئة حليبية ولمعة علوية وهالة باستيل خلفه. — Body blurred 14 px; in a 12 px edge band a 1.06× magnified copy fakes refraction; milky fill, top sheen and a pastel aura behind.
- **متى أستخدمها / when:** محاكاة iOS 26 / macOS Tahoe، أزرار ومفاتيح فاخرة.
- **كيف / how:** Canvas: capture backdrop → blur body; clip ring band and draw backdrop scaled 1.06 about the centre, slightly blurred; 1 px bright rim; soft lift shadow. HyperFrames blocks ios26-liquid-glass / macos-tahoe-liquid-glass / liquid-glass-widgets exist (npx hyperframes add …, untested here). **أرقام / params:** body blur 14 px, edge band 12 px, magnify 1.06.
- **الدليل / proof:** `kosif-tool/styles/pm-rossaxbt-3085b7` · `kosif-one/vendor/hyperframes/registry/blocks/ios26-liquid-glass`
- **أساليب / styles:** `style:pm-rossaxbt-3085b7`

#### TEX-45 · حروف وأشكال من زجاج متجمد · Frosted glass shapes and letters · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نسخة مموّهة 20–40px ومفتّحة +20% من الخلفية مقصوصة على مسار الشكل أو النص، بحافة علوية 1px. — A blurred (20–40 px), +20% lightened copy of the backdrop clipped to a shape or text path, with a bright 1 px top rim.
- **متى أستخدمها / when:** عناوين زجاجية، صناديق كتابة (prompt box)، كروت.
- **كيف / how:** Clip(text path) → draw blurred backdrop → white overlay .25 → rim rgba(255,255,255,.7). Prompt-box variant: blur 24 px saturate 1.4, white 35%, radius 60, springs open with ~2% width overshoot. Arabic letters: clip with the shaped word, never per-letter. **أرقام / params:** blur 30 px, overlay .25, rim .7.
- **الدليل / proof:** `kosif-tool/styles/pm-notdwd-7de38a` · `kosif-tool/styles/pm-notdwd-c2037d`
- **أساليب / styles:** `style:pm-notdwd-7de38a` · `style:pm-notdwd-c2037d`

#### TEX-46 · زجاج بانكسار وتشتت لوني (3D) · Refraction + chromatic dispersion glass · 📦 بأمر تثبيت / one install
- **ماذا / what:** أجسام زجاج/كريستال تكسر الخلفية وتفصلها إلى حواف قوس قزح. — Glass/crystal objects that bend the background and split it into rainbow fringes.
- **متى أستخدمها / when:** منتجات زجاجية، شعارات كريستالية، لقطات بطل.
- **كيف / how:** Render background to an FBO; refract(eye, normal, 1/IOR) per channel with separate IOR for R/G/B; backside pass first for internal dispersion. Shortcut: drei MeshTransmissionMaterial (React). **أرقام / params:** IOR 1.31 base; per-channel IOR spread ~.02.
- **📦 تثبيت / install:** `npm i three @react-three/fiber @react-three/drei`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### TEX-47 · ذهب معدني بلمعة متحركة · Metallic gold with moving sheen · ✅ مُثبت هنا / proven here
- **ماذا / what:** كلمة ذهبية من أربع طبقات: توهج، حافة محفورة، تدرج معدني بسبع وقفات، ولمعة بقناع 105° تعبر الكلمة. — Gold word in four stacked copies: glow, engraved edge, a 7-stop metal gradient and a 105° masked sheen sweeping across.
- **متى أستخدمها / when:** شعارات فاخرة، مناسبات، عناوين ذهبية عربية.
- **كيف / how:** Gradient 180°: #fff4d6 0, #f0d793 16, #c9a24a 40, #8a6424 56, #b88d3a 68, #f2dc9c 86, #fff4d6 100 via background-clip:text; glow #c9a24a blur 26 px .42; edge #4a3110 offset 4 px; sheen copy #fffaf0→#ffe9b8 visible in a ±9% band (plus a thinner .55 follower). Rendered in proofs/glass-luxury-logo. **أرقام / params:** sheen band ±9%, angle 105°, glide easing cubic-bezier(.65,0,.35,1).
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/glass-luxury-logo/README.md`

#### TEX-48 · كرة لامعة من تدرجات · Glossy 2D sphere / orb from gradients · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كرة لامعة بتدرجات شعاعية متراكبة: جسم، انعكاسات دوارة، بقعة لمعان علوية يسار، ضوء حافة وتوهج خارجي. — Stacked radial gradients: body, rotating inner reflections, top-left specular, rim light and outer glow.
- **متى أستخدمها / when:** إنفوغراف، أيقونات منتج، «كرة الذكاء».
- **كيف / how:** Body #5b9bff→#1239a0 (or #a88bff→#6c3bff), rim #c9f4ff; white elliptical blurred specular at top (opacity .6), small orange inner hotspot, outer purple glow + faint concentric halo rings. **أرقام / params:** highlight .6; rim 2–4 px.
- **الدليل / proof:** `kosif-tool/styles/infographic` · `kosif-tool/styles/product`
- **أساليب / styles:** `style:infographic` · `style:product`

#### TEX-49 · كروم يعكس المشهد حيًا · Chrome via live CubeCamera reflection · 📦 بأمر تثبيت / one install
- **ماذا / what:** كرة مرآة تعكس الوادي الحقيقي عبر كاميرا مكعبة تُحدّث كل إطار. — A mirror sphere reflects the actual scene through a cube camera updated every frame.
- **متى أستخدمها / when:** أجسام كروم بطلة، شعارات معدنية ثلاثية.
- **كيف / how:** WebGLCubeRenderTarget(256, HalfFloat, mipmaps); CubeCamera(.05, 600); MeshStandardMaterial metalness 1, roughness .06, envMap = cube; per frame: hide orb → cubeCam.update → show. The demo project loads assets/main.bundle.js, which is not built in this checkout — install esbuild and bundle first; the kit itself (three-kit.bundle.js) is prebuilt. **أرقام / params:** 256², half float; roughness .06.
- **📦 تثبيت / install:** `cd 100-superskills/skills/kosif-montage-motion/scripts && npm install three@0.186.1 esbuild && python3 motion.py bundle sound_ground`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:51` · `100-superskills/skills/kosif-montage-motion/SKILL.md:106`

#### TEX-50 · ظلال ارتفاع ناعمة متعددة · Layered soft elevation shadows · 🟢 جاهز / ready
- **ماذا / what:** ثلاثة مستويات ظل من ظل تلامس رفيع وظل محيطي كبير بانتشار سالب ملوّن بلون العلامة الداكن. — Three elevation tokens: a hairline contact shadow plus a large negative-spread ambient shadow tinted with the brand dark.
- **متى أستخدمها / when:** بطاقات وأجهزة ونوافذ تحتاج «وزنًا» لا يشبه ظل الويب الرمادي.
- **كيف / how:** cobalt: 0 1px 2px rgba(11,16,48,.05), 0 12px 32px −24px rgba(11,16,48,.36) / 0 18px 40px −22px .32 / 0 32px 80px −28px .48; ledger uses rgba(29,24,20,…). **أرقام / params:** --sk-shadow-1/2/3.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/tokens.css:184`

## الضوضاء الإجرائية والخامات المولّدة — Procedural noise & generated materials

_لا تنزّل خامة: الضوضاء ببذرة تصنع الجلد والصخر والماء والغيم والرخام والحمم — وتبقى حتمية وقابلة للتعديل._

#### TEX-51 · نسيج الضوضاء الكسرية · Fractal value-noise material (Studio painter) · ✅ مُثبت هنا / proven here
- **ماذا / what:** ضوضاء قيمية متعددة الطبقات ببذرة داخل الشكل، تقرأها العين كجلد أو صخر أو خطوط ماء أو فرو أو ضباب. — Seeded multi-octave value noise inside a shape that reads as skin, rock, water streaks, fur or fog.
- **متى أستخدمها / when:** أي رسم بـ render.py يحتاج مادة لا لونًا مسطحًا.
- **كيف / how:** noise(shape, amount, cell, seed, mode="multiply"|"normal"|"add"|"screen", colour, octaves=4, stretch=(sx,sy)). Test test_realism_primitives_change_a_flat_fill passed here. **أرقام / params:** skin cell 10–14 multiply; water stretch (6,1); cloud cell 60 + blur; rock cell 26 + cold rim; sky 160 multiply .35.
- **الدليل / proof:** `kosif-studio/render.py:496` · `kosif-studio/references/drawing-guide.md:62` · `kosif-studio/tests/test_studio.py:71` · `100-superskills/skills/pixel-studio-painter/scripts/render.py`

#### TEX-52 · نقش الحراشف والقرميد · Scales / tiles pattern · ✅ مُثبت هنا / proven here
- **ماذا / what:** أقواس متداخلة متعاقبة مقصوصة على الشكل: حراشف زواحف، جلد سمك، قرميد أسقف. — Staggered overlapping arcs clipped to a shape: reptile scales, fish skin, roof tiles.
- **متى أستخدمها / when:** تنانين، أسماك، بيوت تراثية.
- **كيف / how:** Pillow: scales(shape, size=14, colour, alpha=.35, width=1, stagger=True) over shade()/relief() (tested here). SVG: <pattern width=22 height=16 patternUnits=userSpaceOnUse> of arcs, fill the body twice — gradient then url(#scales) (duck_dragon.py). **أرقام / params:** row step size·.55; dragon hide size 8 alpha .22 width .8; SVG tile 22×16 strokes #052e16 1.6 .55 + #4ade80 1 .25.
- **الدليل / proof:** `kosif-studio/render.py:539` · `kosif-studio/tests/test_studio.py:71` · `kosif-studio/scenes/whale_dragon.py:164` · `kosif-one/projects/duck-vs-dragon/duck_dragon.py`

#### TEX-53 · إضاءة بارزة بخريطة ارتفاع · Relief lighting (height field + SSS) · ✅ مُثبت هنا / proven here
- **ماذا / what:** يضيء الشكل كحقل ارتفاع بتشتت تحت السطح ونتوءات وخشونة وفرينل ولمعان. — Lights a shape as a height field with subsurface scattering, bumps, roughness, Fresnel and specular.
- **متى أستخدمها / when:** كائنات «ممتلئة» واقعية في الرسم ثنائي الأبعاد (حوت، تنين، فاكهة).
- **كيف / how:** relief(shape, lights=[(x,y,z,colour,power)], base, ambient=.22, bulge=.6, plateau=.5, bumps=[(scale,amp)], sss, roughness). Tested here (test_camera_ops_run_and_change_the_picture: >30 distinct colours in the lit patch). **أرقام / params:** ambient .22, bulge .6, plateau .5; bumps e.g. [(2,20),(.5,4)], sss 4, roughness .5.
- **الدليل / proof:** `kosif-studio/render.py:618` · `kosif-studio/tests/test_studio.py:81` · `kosif-studio/scenes/whale_dragon.py`

#### TEX-54 · سطح ماء يلمع · Water surface with light glints (Studio) · 🟢 جاهز / ready
- **ماذا / what:** أمواج من حقل ضوضاء ممدود، اللون يمزج العمق والسماء حسب ميل كل وجه، وكل ضوء يترك أثر لمعان. — Waves as a stretched noise height field; colour mixes deep and sky by facet tilt; each light leaves a trail of specular glints.
- **متى أستخدمها / when:** بحر، بحيرة، مطر على سطح.
- **كيف / how:** water(area, lights, deep, sky, cell, stretch, height, seed, shininess, spec, octaves) in render.py (not covered by a test). **أرقام / params:** deep #0a1118, sky #2a3a4c, cell 18, stretch 6, height 6, shininess 60, spec 1.2; storm #060a0f/#28323f cell 20 stretch 7 height 7 shininess 70.
- **الدليل / proof:** `kosif-studio/render.py:652` · `kosif-studio/scenes/whale_dragon.py:115`

#### TEX-55 · ضوضاء بيرلين وfbm وridged ببذرة · Seeded CPU Perlin / fBm / ridged noise · 🟢 جاهز / ready
- **ماذا / what:** ضوضاء ثنائية حتمية (بذرة 1337) للتضاريس والخامات وتوزيع العناصر. — Deterministic 2D Perlin, fractal Brownian motion and ridged noise (seed 1337) for terrain, textures and placement.
- **متى أستخدمها / when:** كل مشهد three-kit أو Canvas يحتاج تنوعًا طبيعيًا.
- **كيف / how:** three-kit.bundle.js → K3.perlin(x,y), K3.fbm(x,y,oct,lac,gain), K3.ridged(x,y,oct) + smooth/ramp/clamp01/lerp. Outside the kit: simplex-noise (npm) or opensimplex (pip). **أرقام / params:** fbm oct 5 lac 2.0 gain .5; ridged lac 2.1 gain .5.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:24` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:24` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:24`

#### TEX-56 · خامات مولّدة بلا تنزيل · Generated textures: noiseCanvas / normalFromHeight / spriteTex · 🟢 جاهز / ready
- **ماذا / what:** يولد خامات Canvas من دوال، وخرائط normal من دوال ارتفاع، وسبرايت جسيمات ناعمة/حلقية/خطية. — Canvas textures from functions, normal maps from height functions and soft/ring/streak particle sprites — no downloads.
- **متى أستخدمها / when:** أي سطح ثلاثي يحتاج خامة أو نتوءًا، وأي جسيمات.
- **كيف / how:** K3.noiseCanvas(N,(x,y)=>[r,g,b,a]); K3.normalFromHeight(N, h, strength); K3.spriteTex("soft"|"ring"|"streak"); RepeatWrapping. **أرقام / params:** sprites 128 px; ring warm stop rgba(255,220,180,.35).
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:41` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:48` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:57`

#### TEX-57 · خامة بدن خشبي مدهون · Procedural painted wooden hull · ✅ مُثبت هنا / proven here
- **ماذا / what:** أشرطة طلاء، فواصل ألواح، عروق خشب وطلاء مقشور لقارب تقليدي — على Canvas بلا صور. — Paint bands, plank seams, wood grain and chipped paint for a traditional boat — generated on a canvas.
- **متى أستخدمها / when:** قوارب، أبواب تراثية، أثاث خشبي.
- **كيف / how:** Canvas 1024×256 bands [0–.30 #4a1f17, .30–.78 #1d5f78, .78–.84 #e9e2cf, .84–.92 #b5432c, .92–1 #c89a52]; seam every 9 px; n = fbm(x/60,y/5)·.10 + noise·.05 − .12 where fbm(x/9,y/140) < −.35 (chips); CanvasTexture sRGB, anisotropy 8, roughness .62. Frames rendered here from night_boat via window.seek (SwiftShader WebGL). **أرقام / params:** 1024×256; seam 9 px; chip threshold −.35.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:25`

#### TEX-58 · خامة قمر إجرائية · Procedural moon texture · ✅ مُثبت هنا / proven here
- **ماذا / what:** قمر مكتمل من الرياضيات: إعتام الحافة، بحار داكنة من الضوضاء، فوهات صغيرة، حافة ألفا ناعمة، ساطع بما يكفي للتوهج. — A full moon from maths: limb darkening, noise maria, small craters, soft alpha edge, bright enough to bloom.
- **متى أستخدمها / when:** ليل، دعاء، رمضان، قصص هادئة.
- **كيف / how:** 512² canvas: limb = (1−r²)^.22; maria = smooth(.05,.35,fbm(2.2u,2.2v,5))·.32; craters = max(0,fbm(14u,14v,3))·.12; rgb(255,250,236)·l; disc 2.1° wide at 9000 units; halo sprite ×7 at .28. Rendered here (night_boat frames). **أرقام / params:** limb exponent .22; maria .32; craters .12; halo ×7 .28.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:115` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:156`

#### TEX-59 · طوب إجرائي يتلوّن بالضوء · Procedural brick lit by a light map (multiply) · ✅ مُثبت هنا / proven here
- **ماذا / what:** جدار طوب ببذرة ثابتة يُضرب في خريطة ضوء من انبعاث مموّه، فيأخذ لون اللافتة وتبقى فواصل الملاط معتمة. — Seeded procedural brick multiplied by a light map built from blurred emission, so it takes the sign colour while mortar stays dark.
- **متى أستخدمها / when:** جدران ليلية، نيون، شوارع.
- **كيف / how:** Light map at ¼ res = ambient #1b1f30 + emission blurred 40 px ×1.0 + 140 px ×1.95, multiplied into brick (row 24 px, offset half on odd rows, mortar 3 px, per-brick tone from noise, fine grain). Rendered in proofs/neon-glow (13/13) and the texture lab. **أرقام / params:** seed 20261016; ambient #1b1f30; blur 40/140 px.
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/README.md` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/index.html`

#### TEX-60 · غيوم SVG إجرائية · Procedural SVG clouds (feTurbulence + displacement) · ✅ مُثبت هنا / proven here
- **ماذا / what:** سحب ركامية ناعمة من قطوع ناقصة يشوّهها ضوضاء كسرية وتمويه، فوق تدرج سماء وشمس شعاعية — 2.6KB بدل صورة. — Soft cumulus from plain ellipses distorted by fractal noise and blurred, over a sky gradient and radial sun — 2.6 KB instead of a raster.
- **متى أستخدمها / when:** سماء نهارية/غروب، خلفيات هوية دافئة.
- **كيف / how:** feTurbulence fractalNoise baseFrequency .011, 5 octaves, seed 11 → feDisplacementMap scale 70 (R/G) → feGaussianBlur 5; far layer .009 / 4 oct / scale 55 / blur 12; sky #f1e3bf .3 #d4b06a .62 #f2732d 1 #1d1814; sun radial cx .62 cy .18. Drift by translating the group, never by changing the seed. Rendered here (lab). **أرقام / params:** viewBox 800×600, preserveAspectRatio xMidYMid slice.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/kosif-sky.svg` · `kosif-earth-ci-fork/docs/design/KOSIF-LUXE.md`

#### TEX-61 · كلمة عربية مملوءة بسائل · Fluid-noise filled Arabic word · ✅ مُثبت هنا / proven here
- **ماذا / what:** ضوضاء fbm مشوّهة المجال بثلاثة ألوان تملأ كلمة عربية كاملة كقناع، ثم يكبر القناع حتى يملأ السائل الكادر. — Domain-warped fbm in three colours fills a whole shaped Arabic word as a mask; the mask then scales up until the fluid fills the frame.
- **متى أستخدمها / when:** عناوين أغانٍ، افتتاحيات جريئة، انتقال من الكلمة إلى المشهد.
- **كيف / how:** Canvas: draw warped fbm (w = fbm(p/90 + t·.3); v = fbm(p/60 + 2w)) quantised to 3 inks, then globalCompositeOperation="destination-in" + fillText(word) with direction rtl — the word stays joined. Rendered here (lab, Lalezar). For the transition, animate the font size/scale 1→12 and overlay outline text. **أرقام / params:** fbm 4–5 octaves, warp 2×; inks #2f4bff #e8503c #ff7ad9.
- **الدليل / proof:** `kosif-tool/styles/pm-prasenx-8d9323` · `kosif-tool/playbooks/arabic-typography.md`
- **أساليب / styles:** `style:pm-prasenx-8d9323`

#### TEX-62 · نص بأقنعة الخامات (66 قناعًا) · Texture-mask text (66 PBR masks) · 📦 بأمر تثبيت / one install
- **ماذا / what:** أقنعة إضاءة CSS تثقب خامة داخل الحروف: طوب، رخام، خشب، حمم، ثلج، جلد… من خرائط ambientCG. — CSS luminance masks punch texture into letterforms: bricks, marble, wood, lava, snow, leather… from ambientCG colour maps.
- **متى أستخدمها / when:** عناوين ضخمة بمادة، ملصقات، ضربة كلمة على الإيقاع.
- **كيف / how:** npx hyperframes add texture-mask-text; classes texture-text + hf-texture-<name>; lint rules texture_class_unknown / texture_text_missing_mask. For Arabic, apply the mask to the whole shaped word element. The 66 PNG masks also ship inside held-text-strobe-burst assets. **أرقام / params:** 66 masks: asphalt, bark, bricks, carpet, concrete, diamond-plate, fabric, grass, ground, lava, leather, marble, metal, onyx, plaster, paving, road, rock, snow, tiles, travertine, wood, wood-floor….
- **📦 تثبيت / install:** `npx hyperframes add texture-mask-text`
- **⚖️ ترخيص / license:** المكوّن Apache-2.0؛ الأقنعة من ambientCG برخصة CC0 / component Apache-2.0, masks CC0 (ambientCG).
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/texture-mask-text/registry-item.json` · `kosif-one/vendor/hyperframes/packages/lint/src/rules/textures.ts` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/templates/held-text-strobe-burst/assets/texture-mask-text/masks/lava.png`

#### TEX-63 · كتل شيدر المواد (WebGPU) · HyperFrames material shader blocks · 📦 بأمر تثبيت / one install
- **ماذا / what:** خلفيات/أجسام شيدر جاهزة مدتها 2 ث: chrome-orb, liquid-metal, marble, obsidian, plastic, holographic, thin-film, water, frost, fractal/gabor/worley noise، وغيرها (aurora, plasma, nebula, mesh-gradient, halftone-field…). — Ready 2 s shader plates: chrome, liquid metal, marble, obsidian, plastic, holographic, thin film, water, frost, fractal/Gabor/Worley noise and more.
- **متى أستخدمها / when:** لوح خلفي تحت عنوان، أو جسم مادي بطل، داخل مشروع HyperFrames.
- **كيف / how:** npx hyperframes add <block> (or put lib/shaders.iife.js next to the page) then <canvas data-shader="Marble" width=1920 height=1080> inside a root marked data-requires-webgpu data-no-timeline. Needs a WebGPU-capable Chromium — not verified here (only WebGL via SwiftShader was). **أرقام / params:** 1920×1080, 2 s; shaders.iife.js 1,444,793 B (shaders 4.0.0).
- **📦 تثبيت / install:** `npx hyperframes add marble`
- **⚖️ ترخيص / license:** Apache-2.0 + مكتبة Shaders برخصة MIT (راجع shaders.THIRD-PARTY-LICENSES.txt) / Apache-2.0 AND MIT.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/marble/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/liquid-metal/liquid-metal.html` · `kosif-one/vendor/hyperframes/registry/blocks/chrome-orb/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### TEX-64 · حقل الحبيبات ونزف الحبر · Grain field & ink-bleed reveal (HyperFrames) · 📦 بأمر تثبيت / one install
- **ماذا / what:** حقل نقاط ملوّن ينجرف فوق تدرج في حلقة، وحبر سائل يتفتح في الورق بفلتر لزج ثم ينكمش لعلامة حادة. — Accent-tinted dot field drifting in a seamless loop; liquid ink blooming through paper with a gooey blur+threshold filter, then resolving to a crisp mark.
- **متى أستخدمها / when:** خلفيات دافئة وكشف شعار عضوي.
- **كيف / how:** npx hyperframes add grain-field | grain-overlay | ink-bleed-reveal; mount on a class="clip" div with data-composition-src + data-start/data-duration/data-track-index; overrides via data-variable-values JSON; extra duration becomes hold, never time-stretch. Gooey filter = feGaussianBlur 10 → feColorMatrix alpha ×18 −7. **أرقام / params:** grain-field density fine|coarse; ink blobs 4–6; exit none|fade|up.
- **📦 تثبيت / install:** `npx hyperframes add ink-bleed-reveal`
- **⚖️ ترخيص / license:** Apache-2.0.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/grain-field/grain-field.html` · `kosif-one/vendor/hyperframes/registry/components/ink-bleed-reveal/ink-bleed-reveal.html` · `kosif-one/vendor/hyperframes/registry/components/grain-overlay/grain-overlay.html`

#### TEX-65 · غيوم بخطوط فرشاة وسماء سديمية · Painterly streak clouds & nebula skies · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ضوضاء fbm مشوّهة المجال تُقصّ إلى خطوط ناعمة ملوّنة بتدرج السماء مع ميل نحو الشمس؛ ونسخة سديمية بنفسجية بنجوم. — Domain-warped fbm thresholded into soft streaks tinted by the sky gradient and toward the sun; a purple nebula variant with stars.
- **متى أستخدمها / when:** سماء حالمة، أنمي، فضاء.
- **كيف / how:** Fragment shader or offline numpy: fbm 4–5 octaves, warp .3, drift .01 uv/s; rim tint toward the sun position; nebula = fbm purple/magenta + seeded star points. **أرقام / params:** fbm 4–5 oct, warp .3, drift .01 uv/s.
- **الدليل / proof:** `kosif-tool/styles/pm-demitiyageekzen-7770ad` · `kosif-tool/styles/pm-ryzoft-4f85bd`
- **أساليب / styles:** `style:pm-demitiyageekzen-7770ad` · `style:pm-ryzoft-4f85bd`

#### TEX-66 · أرضية حمم بعروق مضيئة · Veined lava floor shader · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** سطح بضوضاء ridged مطلقة تُقص إلى عروق برتقالية رفيعة فوق قاعدة بنفسجية عنابية، تزحف ببطء. — abs(fbm) ridged noise thresholded into thin orange veins over a purple-maroon base, slowly scrolling.
- **متى أستخدمها / when:** ألعاب، خيال، مشاهد طاقة.
- **كيف / how:** Plane + fragment shader: v = 1 − smoothstep(0, .03, abs(fbm(uv·3 + t·.05))); colour mix(#4a2040, #f0a040, v) + bloom on the veins. **أرقام / params:** ridge width .03, #f0a040 on #4a2040, scroll .05/s.
- **الدليل / proof:** `kosif-tool/styles/pm-gorden-sun-041f56`
- **أساليب / styles:** `style:pm-gorden-sun-041f56`

#### TEX-67 · شيدر ضربات فرشاة · Stroke-based painterly shader · 💡 فكرة / idea
- **ماذا / what:** ثلاثة أحجام ضربات ترتعش 1–2px بتردد 6Hz فتبدو الأسطح مرسومة باليد، وسماء من ضربات موجّهة بحقل تدفق. — Three stroke sizes jittering 1–2 px at 6 Hz so surfaces look hand-painted; sky of flow-field-oriented stroke sprites.
- **متى أستخدمها / when:** أسلوب لوحة زيتية / فان غوخ.
- **كيف / how:** Untested idea from a brief: instanced stroke quads oriented along curl-noise, colour sampled from the underlying render, re-seeded at 6 Hz (on threes). HyperFrames kuwahara effect (TEX-39) is the cheap fallback. **أرقام / params:** 3 sizes; 1–2 px jitter @ 6 Hz.
- **الدليل / proof:** `kosif-tool/styles/pm-mandelduck-95fd08/BRIEF.md` · `kosif-tool/styles/pm-mandelduck-95fd08`
- **أساليب / styles:** `style:pm-mandelduck-95fd08`

#### TEX-68 · طبقات درجات للفرشاة الجافة · Tone layers for a dry-brush look (rotoscope) · 📦 بأمر تثبيت / one install
- **ماذا / what:** تتبّع الرسمة نفسها على عدة مستويات رمادية وتعبئة كل مستوى بلونه الوسيط لالتقاط خطوط الفرشاة الجافة. — Trace the same drawing at several grey levels and fill each with its median colour to capture dry-brush streaks.
- **متى أستخدمها / when:** تحويل لوحة/رسمة ممسوحة إلى متجه متحرك.
- **كيف / how:** Multi-threshold contour tracing, fill bottom-up even-odd; 3–6 levels (6 gives marginal gain for 1.4× points). vtracer/potracer do the tracing. **أرقام / params:** levels 3–6.
- **📦 تثبيت / install:** `pip install vtracer`
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9357-rotoscope`

#### TEX-69 · فحص قابلية التكرار للخامات المولدة · Seamless-tile check for AI textures · 🟢 جاهز / ready
- **ماذا / what:** المولدات ضعيفة في الخامات المتكررة؛ قِس فرق الحواف واعرض 2×2 قبل استخدامها خلفية. — Generators tile badly: measure seam difference and preview 2×2 before using a texture as a background.
- **متى أستخدمها / when:** كل خامة ولّدتها بالذكاء الاصطناعي أو نزّلتها.
- **كيف / how:** Seam score = mean |left−right| + |top−bottom| edge columns; > 2 shows as grid lines → mirror-blend edges or tile manually; fit to drawn size (e.g. 1024 px, ≤ 250 KB), JPEG/WebP for pictures, PNG only for alpha. **أرقام / params:** seam > 2 visible; 1024 px; ≤ 250 KB.
- **⚖️ ترخيص / license:** Apache-2.0 (atlas item).
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3889-art`

#### TEX-70 · كتيب وصفات المواد للرسام · Material recipe sheet (flame, spray, steam, fur, atmosphere) · 📄 موصوف / documented only
- **ماذا / what:** وصفات مكتوبة: لهب بطبقات جمع من الأحمر للأبيض مع توهج، رذاذ نقاط+تمويه، بخار سحابة screen، فرو أنابيب متوازية، والمسافة غلالة زرقاء. — Written recipes: flames as add layers red→white with glow; spray as dots + blur; steam as a screen cloud; fur as parallel tubes; distance as a blue screen veil.
- **متى أستخدمها / when:** قبل كتابة build() لأي مشهد رسام.
- **كيف / how:** Follow references/drawing-guide.md §3; atmosphere = fill(rect, colour, .2, blur=30, mode="screen"); far edges blur 1–3. **أرقام / params:** veil .2 screen blur 30.
- **الدليل / proof:** `kosif-studio/references/drawing-guide.md:62`

## الخلفيات الحية والشبكات والجدران — Living backgrounds, grids & walls

_الخلفية لا تقف ميتة ولا تسرق العين: حركة بطيئة جدًا (≤ 0.35 وحدة/ث) وتباين منخفض تحت النص._

#### TEX-71 · تدرج شبكي وشبكة خطوط · Mesh-gradient + grid backgrounds · 📄 موصوف / documented only
- **ماذا / what:** خلفيات جوية من تدرجين شعاعيين متراكبين وشبكة 1px خافتة وحبيبات 2% ضد التكسر، أو تدرج شبكي على GPU خلف الواجهة. — Two stacked radial gradients, a faint 1 px grid and 2% grain against banding — or a GPU mesh gradient behind crisp UI.
- **متى أستخدمها / when:** افتتاحيات تقنية، شرائح، عروض SaaS.
- **كيف / how:** radial-gradient(ellipse at 20% 80%, rgba(r,g,b,.3) 0, transparent 50%) + one at 80%/20% (.2); grid = two linear-gradients 1 px rgba(255,255,255,.03) every 50 px; animate centres slowly. GPU option: @paper-design/shaders-react MeshGradient (Apache-2.0) behind a z-index:1 UI with a static CSS fallback. A seek-driven 6-point Gaussian mesh (σ² .11 at 192×108, upscaled) runs in proofs/glass-luxury-logo. **أرقام / params:** radials .3/.2 → 50%; grid 50 px @ 3%; grain 2%; mesh #00F0FF/#7000FF/#000.
- **الدليل / proof:** `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/animation-patterns.md` · `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/references/shader-backed-ui.md` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/glass-luxury-logo/README.md`

#### TEX-72 · ست خلفيات نقشية متحركة · Basma animated pattern backgrounds (6 + gradient) · 📦 بأمر تثبيت / one install
- **ماذا / what:** aurora, grid, dots, waves, stars, rays + تدرج دوّار ولون ثابت، كلها تتجاوب مع الإيقاع. — aurora, grid, dots, waves, stars, rays plus a rotating gradient and solid — all beat-aware.
- **متى أستخدمها / when:** ريلز موسيقية وخلفيات ترجمة في محرر Basma.
- **كيف / how:** drawPattern(): aurora = 4 screen-blended radial blobs on Lissajous paths (radius .5·max(W,H) + beat); grid 9% spacing drifting .35 sp/s + accent radial; dots 7% grid, size wave sin(d·14 − 2.2t); waves 6 sine bands amplitude 3.5% H; stars 140 twinkling + horizon glow; rays 14 wedges at .08 rad/s; gradient rotates .25 rad/s. **أرقام / params:** aurora|grid|dots|waves|stars|rays|gradient|solid.
- **📦 تثبيت / install:** `cd app && npm install`
- **الدليل / proof:** `app/public/js/00_editor.js:2418` · `app/public/js/00_editor.js:2443` · `app/index.html:49`

#### TEX-73 · شبكة خطوط قطرية منجرفة · Drifting diagonal line grid · 🟢 جاهز / ready
- **ماذا / what:** شبكة خافتة من خطوط مائلة وأفقية تتمايل برفق فتعطي الخلفية الفارغة حياة. — A faint grid of slanted lines plus horizontals swaying gently — motion for an empty background.
- **متى أستخدمها / when:** استوديو، شاشات انتظار، خلفية عنوان.
- **كيف / how:** globalAlpha .13; spacing min(w,h)/12; slanted lines from (x + sin(t·.15)·25, 0) to (x + .15w, h); horizontals every spacing. **أرقام / params:** alpha .13; sway ±25 px at .15 rad/s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:66`

#### TEX-74 · شبكة نقطية تحريرية دقيقة · Fine dot-dash editorial grid · 🟢 جاهز / ready
- **ماذا / what:** شبكة ثابتة منخفضة التباين من شرطات صغيرة تعطي إحساس ورق تحريري بلا خطوط قطرية. — Stationary low-contrast grid of tiny dashes — an editorial paper feel with no diagonals.
- **متى أستخدمها / when:** أسلوب تحريري، مجلات، قصص بيانات.
- **كيف / how:** Vertical dashes every .10w from .07w, step .051h, length 2·scale; horizontals the same; stroke at 55% alpha, width max(.5, .7·scale). **أرقام / params:** 10% × 5.1% spacing.
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:43-46`

#### TEX-75 · ورق مربعات وشبكة قياس · Graph-paper & graticule grids · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شبكة 1px داكنة ‎#1a1a1a‎ على ‎#090909‎ أو شبكة قياس 10×8 خضراء داكنة مع علامات صغرى وتعتيم. — 1 px #1a1a1a grid on #090909, or a 10×8 dark-green graticule with minor ticks and vignette.
- **متى أستخدمها / when:** راسم/بلوتر، أوسيلوسكوب، رسوم هندسية.
- **كيف / how:** Cell 40–48 px at 1280 w; grain .06; graticule #0f2a1a 1 px at .35 + ticks every 1/5 cell; radial vignette. **أرقام / params:** cell 40–48 px; grain .06; graticule opacity .35.
- **الدليل / proof:** `kosif-tool/styles/plotter` · `kosif-tool/styles/pm-rneayan-ea6129`
- **أساليب / styles:** `style:plotter` · `style:pm-rneayan-ea6129`

#### TEX-76 · جدار نص وبيانات خافت · Faint data/text wall · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** خلفية داكنة مملوءة بأعمدة نص mono صغير 6–10% تنزلق ببطء تحت توهج بنفسجي، أو صفوف تنزلق باتجاهين خلف العنوان. — Dark ground filled with tiny mono text columns at 6–10% scrolling slowly under a violet glow, or rows scrolling in opposite directions behind a headline.
- **متى أستخدمها / when:** أمن، بيانات، ذكاء اصطناعي، «حجم المعلومات».
- **كيف / how:** Mono 9 px at .08 scrolling 10 px/s; dense variant 40–80 px/s alternating direction per row; keep the headline on a solid band. Arabic walls: whole words per row, RTL scroll. **أرقام / params:** mono 9 px, opacity .08, 10 px/s (dense 40–80 px/s).
- **الدليل / proof:** `kosif-tool/styles/pm-kmasiff-cc72cb` · `kosif-tool/styles/pm-madebyjmayala-b9204d` · `kosif-tool/styles/pm-souravbhar871-61f424`
- **أساليب / styles:** `style:pm-kmasiff-cc72cb` · `style:pm-madebyjmayala-b9204d` · `style:pm-souravbhar871-61f424`

#### TEX-77 · أفق مدينة ليلي إجرائي · Procedural night skyline with lit windows · 🟢 جاهز / ready
- **ماذا / what:** كتل مدينة بارتفاعات عشوائية ونوافذ مضاءة بلونين، تولد مرة واحدة من دالة hash حتمية. — City blocks of random heights with windows lit in two tones, generated once from a deterministic hash.
- **متى أستخدمها / when:** مشاهد ليلية، قصص مدن، خلفيات شخصيات.
- **كيف / how:** skyline(): 30 towers h 105–340, w 62–108; windows 3.5×6 lit if rnd > .43 (#4b99a2 / #9c976e, .15–.55); architecture(): 12 mid buildings 200 px wide, 23×28 windows lit if rnd > .37. **أرقام / params:** 30 towers; lit > .43.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:31`

#### TEX-78 · انعكاسات الشارع المبتل · Wet street / floor reflections · ✅ مُثبت هنا / proven here
- **ماذا / what:** أرض مبتلة من بقع ضوء ملونة وفواصل رصف منظورية وخطوط لمعان أفقية متقطعة، ونسخة مرآة داكنة مموجة للبطل. — Wet ground of coloured light pools, perspective paving joints and broken horizontal glints, plus a dark rippled mirror of the hero.
- **متى أستخدمها / when:** نيون، مطر، ليل سينمائي.
- **كيف / how:** Canvas: street gradient #17343f→#030b16, 85 broken reflection lines, hero drawn scale(1,−.25) at .085. Proof film version: mirrored 3 px slices with ripple, sharp layer in puddles + 16 px blurred layer on asphalt, Fresnel fade .9→.25 — rendered in proofs/neon-glow (13/13). **أرقام / params:** slices 3 px; blur 16 px; Fresnel .9→.25; mirror opacity .085.
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/README.md` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:109`

#### TEX-79 · سبورة بآثار مسح · Whiteboard eraser-smudge texture · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** بضع ضربات رمادية فاتحة جدًا مموّهة على ‎#f6f6f4‎ مع ظل داخلي خفيف للإطار. — A few very light grey rounded strokes with a large blur over #f6f6f4, plus a subtle inner border shadow.
- **متى أستخدمها / when:** شرح بالسبورة البيضاء.
- **كيف / how:** 4–6 seeded strokes, opacity .05–.1, blur 8–12 px, static; inner shadow inset 0 0 40px rgba(0,0,0,.06). **أرقام / params:** opacity .05–.1, blur 8–12 px.
- **الدليل / proof:** `kosif-tool/styles/whiteboard`
- **أساليب / styles:** `style:whiteboard`

#### TEX-80 · حبيبات الطباشير · Chalk grain overlay · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** طبقة SVG ثابتة بكامل السبورة: feTurbulence → feColorMatrix بلون السبورة، تصنع نمش الطباشير فوق الرسوم. — Static full-board SVG layer: feTurbulence → feColorMatrix into board-coloured specks over the drawings.
- **متى أستخدمها / when:** أسلوب السبورة السوداء.
- **كيف / how:** baseFrequency ~.9, opacity ~.35; do not displace the strokes (feDisplacementMap ruins legibility). **أرقام / params:** freq ~.9, opacity ~.35.
- **الدليل / proof:** `kosif-tool/styles/chalkboard`
- **أساليب / styles:** `style:chalkboard`

#### TEX-81 · تهشير داخل حدود الشكل · Clipped hatching / scribble fill · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** مسار متعرج قطري يغطي الشكل ويُرسم بتقدم الشرطة، مقصوص بحدود الشكل — تلوين ماركر أو طباشير. — A diagonal zigzag over the shape bbox drawn by dash progress and clipped to the shape — marker or chalk fill.
- **متى أستخدمها / when:** سبورة، دودل، رسوم أطفال.
- **كيف / how:** zigzag spacing 10–12 px at 60°, stroke-dasharray progress, clipPath = shape, opacity ~.55; chalky robe variant: short lighter diagonal hatches 6–8 px at .3. **أرقام / params:** spacing 10–12 px, 60°, .55 (chalk 6–8 px, .3).
- **الدليل / proof:** `kosif-tool/styles/whiteboard` · `kosif-tool/styles/doodle`
- **أساليب / styles:** `style:whiteboard` · `style:doodle`

#### TEX-82 · أرضيات ورقية وبلاط · Paper doodle ground & tile floor · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ورق غائم بخط أرض مرسوم باليد، أو بلاط بكسل متكرر 32px — أبسط أرضية تعطي المكان هوية. — Cloudy paper with a hand-drawn baseline, or a repeating 32 px pixel tile floor.
- **متى أستخدمها / when:** دودل، ألعاب بكسل.
- **كيف / how:** Paper: low-frequency noise multiply + wobbly baseline path; tile: CanvasPattern of a 32 px tile with imageSmoothingEnabled=false. **أرقام / params:** tile 32 px.
- **الدليل / proof:** `kosif-tool/styles/pm-ajith-io-ea7f2d` · `kosif-tool/styles/pm-aisongman-71ffac`
- **أساليب / styles:** `style:pm-ajith-io-ea7f2d` · `style:pm-aisongman-71ffac`

#### TEX-83 · مثال الحبيبات الدافئة · warm-grain example project (HyperFrames) · 📦 بأمر تثبيت / one install
- **ماذا / what:** مشروع كريمي ‎#f5f0e0‎ بخامة حبيبات وخط Outfit لمدة 10 ث — مرجع لوحة وخط. — Cream #f5f0e0 starter with grain texture and Outfit, 10 s — a palette/type reference.
- **متى أستخدمها / when:** بداية سريعة لأسلوب دافئ محبب.
- **كيف / how:** npx hyperframes init --example warm-grain; the local copy lacks its sub-compositions (captions/graphics/intro), so use it as a style reference only. **أرقام / params:** 1920×1080; 10 s.
- **📦 تثبيت / install:** `npx hyperframes init --example warm-grain`
- **⚖️ ترخيص / license:** Apache-2.0.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/examples/warm-grain/index.html`

## الخامات ثلاثية الأبعاد — 3D materials

_عائلة مادة واحدة لكل فيلم: مطفي للصلصال واللوبولي، واللمعان محجوز للمنتج البطل._

#### TEX-84 · عائلة مواد مطفية واحدة · One matte material family · 📄 موصوف / documented only
- **ماذا / what:** ثبّت عائلة مادة واحدة: مطفي للصلصال واللوبولي، واللمعان للمنتج البطل فقط. — Keep one material family: matte for clay and low-poly, gloss reserved for hero products.
- **متى أستخدمها / when:** بداية أي مشهد three.js.
- **كيف / how:** MeshStandardMaterial roughness in the matte range; one hero gloss at most. **أرقام / params:** roughness .6–.9; sample 0x7ee8d2 roughness .7.
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:16` · `kosif-tool/playbooks/3d.md:59`

#### TEX-85 · وصفات PBR سريعة · Quick PBR recipes (Three.js) · 📄 موصوف / documented only
- **ماذا / what:** إعدادات سريعة: معدن لامع metalness .8 roughness .2، وأجزاء ذاتية الإضاءة بـ emissive. — Shiny metal metalness .8 / roughness .2; self-lit parts via emissive + emissiveIntensity.
- **متى أستخدمها / when:** منتجات وأجهزة ثلاثية.
- **كيف / how:** MeshStandardMaterial/MeshPhysicalMaterial; metal .8–.85 / rough .15–.2; emissiveIntensity .8 so bloom catches it. **أرقام / params:** metalness .8–.85, roughness .15–.2, emissiveIntensity .8.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/animation_craft.md` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:132`

#### TEX-86 · خامة القطيفة المحشوة · Plush felt material (velvet sheen + fibre) · 🟢 جاهز / ready
- **ماذا / what:** مادة فيزيائية بألوان رؤوس، لمعان مخملي، حافة زغب بلون القماش نفسه وضوضاء ألياف بفضاء الجسم بلا UV. — Vertex-coloured physical material with velvet sheen, a fuzz rim in the fabric colour and object-space fibre noise — no UVs.
- **متى أستخدمها / when:** دمى، شخصيات لطيفة، ألعاب أطفال.
- **كيف / how:** K3S.plushMaterial({fuzz, fibre, fibreScale, sheen, sheenRoughness, sheenColor, fuzzTint, roughness}) from shape-kit.js on the three-kit bundle. **أرقام / params:** roughness .82; sheen 1.0; sheenRoughness .42; sheenColor #fff4f6; fuzz .38; fibre .22; fibreScale 520/m; rim power 2.2.
- **الدليل / proof:** `kosif-studio/motion/kit/shape-kit.js:286` · `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:286` · `100-superskills/skills/kosif-montage-motion/references/shape-kit.md`

#### TEX-87 · لمعان clearcoat للعين والأنف · Glossy clearcoat + eye with catch-lights · 🟢 جاهز / ready
- **ماذا / what:** مادة داكنة لامعة للعيون والأنوف، وعين بصلبة وقزحية وبؤبؤ وقرنية ولمعتين. — Dark glossy clearcoat for eyes/noses; eye() with sclera/iris/pupil/cornea and two catch-lights.
- **متى أستخدمها / when:** شخصيات ثلاثية تحتاج حياة في النظرة.
- **كيف / how:** K3S.glossMaterial(color,{roughness, env}); K3S.eye({r, tall}); K3S.tube(points, r, colour) for mouths/stitches; makeEye in lab-kit. **أرقام / params:** #15100f; roughness .08; clearcoat 1, clearcoatRoughness .04; ior 1.5; envMapIntensity 1.6; eye tall 1.12, catch-lights upper-outer.
- **الدليل / proof:** `kosif-studio/motion/kit/shape-kit.js:311` · `kosif-one/tools/kosif-studio/motion/kit/shape-kit.js:316`

#### TEX-88 · طقم مواد المختبر · Lab material set (plush/gloss/leather/metal) · 🟢 جاهز / ready
- **ماذا / what:** مواد سريعة لمشاهد مختبر المنتج: قطيفة، لامع، جلد، معدن. — Quick materials for product-lab scenes: plush, gloss, leather, metal.
- **متى أستخدمها / when:** عرض منتج ثلاثي سريع.
- **كيف / how:** K3.plushMaterial(c), K3.glossMaterial(c,{roughness}), K3.leatherMaterial(c), K3.metalMaterial(c) from lab-kit.js. **أرقام / params:** plush r .95; gloss clearcoat 1 r .08; leather #15171a r .55 m .05; metal #d8dde3 r .25 m .95.
- **الدليل / proof:** `kosif-studio/motion/kit/lab-kit.js:49` · `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:49`

#### TEX-89 · فرو بالطبقات · Shell fur · 🟢 جاهز / ready
- **ماذا / what:** نسخ طبقية من الشبكة مدفوعة على العموديات بخرائط نقاط ألفا، جذور أغمق وجاذبية على الطبقات الخارجية. — Layered shells pushed along normals with dot alpha maps; darker roots and gravity sag on outer shells.
- **متى أستخدمها / when:** حيوانات، دمى، عشب قصير.
- **كيف / how:** K3.makeFur(mesh,{layers, length, repeat, color, rootShade, gravity, density, seed}) (lab-kit.js); recolour live: shell.material.color.lerp(target).multiplyScalar(.55 + .45·(i+1)/n). Projects: rabbit 7 layers .09, lion 8 layers .07, mane 10 shells .18 m. **أرقام / params:** layers 10 (8–12 at 540p, 16 at 1080p); length .12; repeat 14; rootShade .72; gravity .35; alphaTest .1→.78; hair texture 256 px density .55.
- **الدليل / proof:** `kosif-studio/motion/kit/lab-kit.js:28` · `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/src/main.js:14`

#### TEX-90 · بقع لونية على المجسم · Colour paint stamps on SDF · 🟢 جاهز / ready
- **ماذا / what:** بقع لونية كروية/بيضاوية ناعمة (خدود، بطن، وسائد الكف) بلا هندسة إضافية. — Soft spherical/ellipsoidal colour stamps (blush, belly patch, paw pads) with no extra geometry.
- **متى أستخدمها / when:** شخصيات SDF في shape-kit.
- **كيف / how:** S.paint(c, r, colour, {soft, radii, amount, rot}). **أرقام / params:** soft default r·.5; amount 1; blush r .015 soft .009 amount .8.
- **الدليل / proof:** `kosif-studio/motion/kit/shape-kit.js:98` · `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:98`

#### TEX-91 · شفافية الأشعة السينية للدمية · Plush X-ray during analysis · 🟢 جاهز / ready
- **ماذا / what:** الدمية الناعمة تصير شبه شفافة أثناء تحليل بنيتها ثم تعود معتمة. — The plush character turns semi-transparent while its internal structure is analysed, then returns opaque.
- **متى أستخدمها / when:** شرح «من الداخل»، تشريح، تقنية.
- **كيف / how:** All materials transparent; opacity = base·(1 − .66·xr), depthWrite only when > .98; xr = smooth(joint−.05, joint+.3)·(1 − smooth(rank+.05, rank+.42)). **أرقام / params:** max fade .66.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:53`

#### TEX-92 · حصى وقصب · Pebbles & reed blades · 🟢 جاهز / ready
- **ماذا / what:** حصى نهري مُنسَّخ من إيكوساهيدرا مشوهة بالضوضاء في عناقيد بأربع عائلات لون، وأعواد قصب مستدقة تتمايل. — Instanced water-worn stones from noise-deformed icosahedra clumped in drifts (4 HSL colour families), plus tapered swaying reed blades.
- **متى أستخدمها / when:** بِرك، شواطئ، حدائق.
- **كيف / how:** K3.makePebbles({n, region, accept, height, size, flat, clump, seed}); K3.makeBlades({n, region, tall, width, seed}). **أرقام / params:** pebbles n 2400, size .06 m (×.4–2.8), flat .5; blades n 1500, tall .9 m.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:724` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:746`

#### TEX-93 · قاع بركة بانكسارات ضوئية · Pond bed terrain with caustics · 📦 بأمر تثبيت / one install
- **ماذا / what:** قاع بركة ملوّن بالعمق والميل (طمي، رمل، طين، طحلب) مع كاوستكس متحركة تمتص الأحمر مع العمق. — Pond bowl coloured by depth and slope (silt, sand, mud, moss) with animated caustics absorbing red with depth.
- **متى أستخدمها / when:** أسماك كوي، ماء صافٍ، طبيعة هادئة.
- **كيف / how:** makeTerrain({size 44, seg 320, albedoRepeat 10, normalRepeat 22, normalScale .8, texSize 512}); addCaustics(material,{time, level 0, strength 3.2, scale 5.5, absorb [1.35,.42,1.0], sun}); pebbles 2600 × .038 + rim 170 × .24. The demo project loads assets/main.bundle.js, which is not built in this checkout — install esbuild and bundle first; the kit itself (three-kit.bundle.js) is prebuilt. **أرقام / params:** silt #4a4532 sand #857a5c mud #2e2a20 moss #3d5a26 #5f7a33.
- **📦 تثبيت / install:** `cd 100-superskills/skills/kosif-montage-motion/scripts && npm install three@0.186.1 esbuild && python3 motion.py bundle koi_pond`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:9` · `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:39`

#### TEX-94 · أسفلت مبلل وطلاء عاكس · Wet asphalt + retro-reflective road paint · 📦 بأمر تثبيت / one install
- **ماذا / what:** أسفلت ليلي قليل الخشونة يلمع مع المصابيح، وشرطات وسط وخطوط حواف تتوهج بخفة. — Slightly wet low-roughness asphalt glinting with lamps; centre dashes and edge lines glowing faintly.
- **متى أستخدمها / when:** طرق ليلية، سيارات، رحلات.
- **كيف / how:** Road ribbon from CatmullRom (800 segments, 8 m wide) MeshStandard 0x15161a roughness .32; paint 0xe8e4da emissive 0x6a6658 ×.6; 340 instanced dashes .16×3 m every 12 m; edge lines .14 m at ±(4−.35) m. The demo project loads assets/main.bundle.js, which is not built in this checkout — install esbuild and bundle first; the kit itself (three-kit.bundle.js) is prebuilt. **أرقام / params:** roughness .32; emissive ×.6; dash every 12 m.
- **📦 تثبيت / install:** `cd 100-superskills/skills/kosif-montage-motion/scripts && npm install three@0.186.1 esbuild && python3 motion.py bundle blue_hour`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:64`

## توليفات قوية / power combos

- **ليل نيون ممطر / rainy neon night:** TEX-59 (طوب يتلوّن بالضوء) + TEX-78 (أرض مبتلة) + TEX-01 (حبيبات) + GLOW (نيون بخمس طبقات) + PART (مطر وحلقات) + CAM (اقتراب 1.0→1.075 مع اهتزاز يدوي) — كما في proofs/neon-glow.
- **كشف هوية فاخرة / luxury reveal:** TEX-40 (بطاقات زجاج بعمق) + TEX-47 (ذهب بلمعة) + TEX-71 (تدرج شبكي حي) + BRAND (رسم الشعار) + EASE (luxe/glide/settle) — كما في proofs/glass-luxury-logo.
- **وثائقي أرشيفي / archival documentary:** TEX-21 (قفل الأرشيف) + TEX-20 (قصاصة جريدة) + TEX-08 (غبار وخدوش) + TEX-18 (تمزيق) + FOOT (صور المستخدم) + STORY (vox) — قصاصات تُثبّت بالشريط والخيط الأحمر.
- **قصة أطفال ورقية / paper storybook:** TEX-23 (ورق مقصوص 3 أعماق) + TEX-14 (ورق مائي) + TEX-19 (ملصق بحد أبيض) + CHAR (مفاصل الدمية) + VOICE (راوٍ) — بارالاكس 1/0.6/0.3 وتمايل ±2°.
- **سبورة تعليمية / whiteboard lesson:** TEX-79 (آثار المسح) + TEX-81 (تهشير مقصوص) + DRAW (رسم الماركر) + ARAB (كتابة بقناع) + CAM (اقتراب لكل جزء) — كما في style:whiteboard.
- **ريل موسيقي طباعي / print-style music reel:** TEX-29 (هالفتون لامبرت) + TEX-32 (موجة هالفتون) + TEX-35 (تنقيط Bayer) + BEAT (النبضة تحرك الضوء والعتبة) + RETRO — نقاط تتنفس مع الإيقاع.
- **عنوان أغنية سائل / fluid lyric title:** TEX-61 (كلمة عربية بسائل) + TRANS (القناع يكبر ليصير المشهد) + SYNC (موعد الكلمة) + GLOW (توهج خارجي) — الكلمة تبقى متصلة لأنها قناع واحد.
- **ليلة رمضانية / Ramadan night:** TEX-58 (قمر إجرائي) + TEX-57 (بدن خشبي) + 3D (ماء وقارب) + GLOW (هالة القمر) + VOICE (دعاء بلا موسيقى) — كما في مشروع night_boat الذي رُندرت إطاراته هنا.
- **منتج ثلاثي لامع / glossy 3D product:** TEX-84 (عائلة مادة واحدة) + TEX-49 (كروم يعكس المشهد) + TEX-46 (زجاج بانكسار) + LIGHT/GLOW (إضاءة استوديو) + CAM (دوران مداري) + UI (بطاقة زجاجية فوقه TEX-42).

## أخطاء ممنوعة / never do

1. **لا حبيبات Math.random() بلا بذرة** — كل رندر يخرج مختلفًا ويتكسر الضغط بين التشغيلات؛ اربط البذرة برقم الإطار (TEX-02) أو استعمل الخطوات المتدرجة (TEX-01).
2. **لا حبيبات فوق 3% في الأفلام النظيفة ولا حبيبات قبل التمويه** — الحبيبات القوية تأكل التفاصيل وتضخم حجم الملف، والتمويه بعدها يحوّلها لبقع؛ الحبيبات آخر طبقة قبل التعتيم.
3. **لا زجاج فوق خلفية مسطحة** — backdrop-filter لا يرى شيئًا ليجمّده فيظهر رماديًا ميتًا؛ ضع تدرجًا حيًا أو بوكيه أو نجومًا تحته (TEX-40).
4. **لا ورق يغلي إلا إذا طلب الأسلوب** — تغيّر بذرة الورق كل إطار يصنع وميضًا متعبًا؛ الورق ثابت والحركة للطبقات فوقه (TEX-13).
5. **لا حافة تمزيق ناعمة تمامًا** — التمزيق اليدوي غير منتظم بلب أبيض وظل؛ الحافة الملساء تفضح «القناع الرقمي» (TEX-18).
6. **لا تقصّ خامة على حروف عربية مفصولة** — القناع أو الخامة على الكلمة المشكّلة كاملة، وإلا تنفصل الحروف (TEX-61، TEX-62).
7. **لا تخلط أكثر من 2–3 خامات في الكادر** — الكولاج المزدحم يضيع البطل؛ خامة أرضية + خامة بطل + حبيبات فقط.
8. **لا خامات على الأرقام والملصقات وخطوط البيانات** — النقص المقصود للجو، والبيانات تبقى حادة ومقروءة (TEX-27).
9. **لا تستعمل خامة مولّدة بلا فحص الحواف** — الخياطة تظهر كشبكة خطوط عند التكرار؛ قِس وعالج قبل الاستخدام (TEX-69).
10. **لا تعتمد على كتل HyperFrames الشيدرية في رندر هنا قبل اختبارها** — تتطلب WebGPU، وما تحقق هنا هو WebGL عبر SwiftShader فقط؛ احتفظ ببديل Canvas/SVG.
11. **لا تحاكي مؤثرات الشيدر على الفيديو بطبقات CSS** — في HyperFrames اضبط effects.<key> على الوسيط نفسه (TEX-39)؛ الطبقات المزيفة لا تتبع المحتوى.
12. **لا تكثر اللمعان في 3D** — عائلة مطفية واحدة واللمعان للبطل فقط؛ كل شيء لامع = لا شيء بطل (TEX-84).

## أقوى 5 حركات توقيع / 5 signature moves

1. **TEX-01 — حبيبات motion-kit المتدرجة + تعتيم:** سطر واحد في نهاية كل فيلم HTML: opacity .05–.09، soft-light، تعتيم .42 — حتمي ومُختبر هنا.
2. **TEX-40 — بطاقات الزجاج بعمق:** blur 22px saturate 150% وحافة علوية وظلّان فوق خلفية حية — مُثبت في فيلم glass-luxury-logo.
3. **TEX-61 — كلمة عربية مملوءة بسائل:** fbm مشوّه بثلاثة أحبار داخل الكلمة المشكلة، ثم يكبر القناع ليصير المشهد التالي.
4. **TEX-59 + TEX-78 — جدار يتلوّن وأرض تعكس:** الضوء يُبنى مرة ويُضرب في الطوب ويُعكس على الأرض المبتلة — سر واقعية فيلم النيون.
5. **TEX-29 — هالفتون لامبرت بضوء يدور:** كرة من نقاط فقط تُظلَّل وتدور — طباعة حية في 20 سطرًا.

## إضافات v2 — v2 additions

_قدرات أُضيفت في الإصدار الثاني من حزم المالك (higgsfield-motion-saas وhiggsfield-motion-claude ومهارة المونتاج التحريرية وفيلم الأغنية وKOSIF SEE) ومن مهارات ECC (رخصة MIT)، مكتوبة بكلماتنا. ✅ هنا = شُغّلت في جلسة 2026-10-16 وسجلها في [external-skills.md](../external-skills.md)؛ مسارات `owner-upload:` تشير إلى أرشيفات المالك لا إلى هذا المستودع. — v2 additions from the owner's packages and ECC skills (MIT), in our own words; ✅ = run in this session, log in external-skills.md; `owner-upload:` paths point into the owner's archives, not this repo._

#### TEX-X01 · حبيبات فيلم صحيحة · Film grain done right (post-mortem) · 📄 موصوف / documented only
- **ماذا / what:** حبيبات بدت «ملصقًا ثابتًا» رغم أنها تتغير كل إطار؛ التشخيص والإصلاح يعلّمان كيف تُصنع حبيبات تعيش داخل الصورة. — Grain that looked like a static sticker although it changed every frame; the diagnosis and fix show how to make grain that lives inside the picture.
- **متى أستخدمها / when:** مظهر أرشيفي أو سينمائي، أو أي حبيبات متحركة — an archival or filmic look, or any animated grain.
- **كيف / how:** Causes found: coarse 2.4 px clumps with 60 % of the energy in deep shadows/highlights; a clump layer that was ONE noise field translated ≈ (32, 18) px per frame, so consecutive frames correlated 0.52–0.54 (a pattern sliding over the picture) while per-frame residual correlation was only ~0.035; grain in screen coordinates while gate weave moved the picture (grain detached); sine-hash 1 px grain losing GPU precision for large arguments (patterned, changed character at each cut); frame index modulo 997 repeating the sequence at 39.9 s. Fix: sparse-convolution noise (one Gaussian blob per cell, 3×3 neighbourhood, kernel e^−4.5 at one cell so no seams), two octaves (1.15 px fine, 2.6 px coarse ≈ 10 % of variance), hashed by (cell, frame) with sine-free hashes, sampled at the weaved film position, weighted to mid-tones, normalised std. Policy: UI/SaaS films keep grain static and ≤ 0.02–0.04 luma (or none); documentary grain must move, but in film coordinates. **أرقام / params:** fine 1.15 px + coarse 2.6 px (~10 %); no modulo index; film coordinates.
- **الرخصة / license:** unknown (reference only)
- **المصدر / source:** `owner-upload:Claude_edit_skill_1/Claude edit skill/implementation/browser-reference/picture.js`
- **الدليل / proof:** `owner-upload:Claude_edit_skill_1/Claude edit skill/implementation/browser-reference/picture.js`

#### TEX-X02 · سلسلة مرور أرشيفية · Archival post chain order (WebGL) · 📄 موصوف / documented only
- **ماذا / what:** ترتيب مراحل المظهر الأرشيفي مهم: الاهتزاز والنعومة قبل التوهج، والتدريج ثم عمر الطبعة، ثم التعتيم، ثم الحبيبات بإحداثيات الفيلم، ثم الغبار والوميض. — The order of archival-look stages matters: weave and softness before bloom, grade then print age, then vignette, then grain in film coordinates, then dust and flash.
- **متى أستخدمها / when:** مونتاج وثائقي أو أرشيفي بالأبيض والأسود أو بلون فيلمي — a documentary or archival edit in B&W or film colour.
- **كيف / how:** compose → bright-pass + 4× downsample → separable 13-tap Gaussian (σ ≈ 3.2 texels at ¼ res ≈ 13 px full res) → main pass: gate weave (≈ 1 px slow drift + per-frame jitter; more for older prints) → lens/emulsion softness 0.8 px (≤ 1.4 old print) → bloom/halation → grade (doc | light neutral B&W | film) → print and archive age (low-frequency density breathing, value noise on a 3-cell lattice) → vignette → grain in film coordinates (TEX-X01) → dust and scratches → flash. Keep one texture-orientation convention across framebuffer passes (GL bottom-up vs top-down uploads). **أرقام / params:** blur σ ≈ 3.2 texels @ ¼; weave ≈ 1 px; softness 0.8–1.4 px.
- **الرخصة / license:** unknown (reference only)
- **المصدر / source:** `owner-upload:Claude_edit_skill_1/Claude edit skill/implementation/browser-reference/picture.js`
- **الدليل / proof:** `owner-upload:Claude_edit_skill_1/Claude edit skill/implementation/browser-reference/picture.js`
