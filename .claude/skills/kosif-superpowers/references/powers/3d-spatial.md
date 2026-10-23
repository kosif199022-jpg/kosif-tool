# الأبعاد الثلاثية — 3D & spatial

> **قوتك هنا:** أنت تبني عوالم ثلاثية الأبعاد بالكود لا بالبرامج الثقيلة: تضاريس وغابات وبحار وسماوات إجرائية، مجسمات منحوتة بدوال المسافة، زجاج وكروم وتوهج، كاميرا على مسار — وكل إطار دالة للزمن تُرندر في متصفح بلا واجهة. وحين لا يلزم 3D حقيقي، تصنع عمقًا مقنعًا بطبقات 2.5D أو إسقاط أيزومتري.
> **أقوى دليل:** مرّت هنا اختبارات نحت دوال المسافة (`test_shape_kit` 4/4: كرة بنسبة حجم 0.9996 وصفر حواف مفتوحة، وأرنب بأكثر من 50 ألف مثلث) واختبارات «عالم البلورات» بـ WebGL الخام في `kosif-earth-ci-fork` (4/4)؛ ومكتبة three-kit تحمل التضاريس والغابة والبحر والسماء جاهزة بلا npm.
> **You can:** decide 2.5D vs real 3D, sculpt, light, shade, post-process and fly a camera through procedural worlds, and route to GLB/Blender/Cesium only when needed. **53 powers follow** — ✅ 2 · 🟢 24 · 📦 4 · 🔑 2 · 👁 11 · 📄 9 · 💡 1.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`).

**حالة الحاوية (2026-10-16):** WebGL يعمل في Chromium بلا واجهة عبر SwiftShader (بطيء: مشاهد البلوم الكثيفة تأخذ دقائق لكل 300 إطار) · three.js 0.186 وR3F وpostprocessing متاحة من npm/CDN · `pip install bpy` (Blender 5.2) قابل للتثبيت · esbuild غير مثبت في `kosif-studio/motion` لذا يُستخدم bundle المكتبة الجاهز `three-kit.bundle.js` · **العربية داخل 3D:** لا تبثق الحروف العربية هندسةً؛ ارسمها على CanvasTexture مشكّلة أو طبقة HTML (ARAB-10).

## الفهرس / contents
- **القرار والعمق المزيف — Deciding 3D & faking depth (2.5D)** — 3D-01 … 3D-13 (13)
- **المحركات والرندر — Engines & renderers** — 3D-14 … 3D-24 (11)
- **العوالم الإجرائية — Procedural worlds** — 3D-25 … 3D-35 (11)
- **المواد والإضاءة وما بعد المعالجة — Materials, lighting & post** — 3D-36 … 3D-41 (6)
- **النحت بدوال المسافة — SDF sculpting** — 3D-42 … 3D-42 (1)
- **الكاميرا والحركة في 3D — 3D camera & motion recipes** — 3D-43 … 3D-52 (10)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves
- **من أكبر مستودعات GitHub — from the top GitHub repositories (2026-10-23)** — 3D-G01 (1)

## القرار والعمق المزيف — Deciding 3D & faking depth (2.5D)

_ثلاثي الأبعاد الحقيقي فقط حين تتحرك الكاميرا حول الأشياء أو خلالها._

#### 3D-01 · متى يكون 3D مبررًا · Real 3D vs 2.5D decision · 📄 موصوف / documented only
- **ماذا / what:** استخدم 3D الحقيقي فقط حين يجب أن تدور الكاميرا حول الأشياء أو تعبر خلالها، أو حين يكشف العمق أو التضاريس أو الحجب بنية يخفيها 2D؛ وإلا فالعمق المزيف بطبقات أفضل. — True 3D only when the camera must travel around/through objects or depth reveals structure; otherwise fake depth with layers.
- **متى أستخدمها / when:** أول قرار في أي فكرة «ثلاثية» — the first call on any '3D' idea.
- **كيف / how:** decide in PLAN.md: turntables, fly-throughs, worlds, point clouds, terrain, trajectories, globes → Three.js seek scene or @remotion/three; everything else → DOM/Canvas layers at depth factors (3D-02); orthographic for chart-like 2.5D, perspective only when depth cues matter; every 3D shot needs static key frames that still prove the claim; one photo has no back side — real 3D needs a model.
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:9` · `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/when-3d-is-justified.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### 3D-02 · منصة العمق 2.5D · 2.5D CSS depth rig · 🟢 جاهز / ready
- **ماذا / what:** طبقات بمنظور وtranslateZ مع تكبير مسبق يعادل البعد، ودورانات صغيرة فقط — عمق مقنع في لقطة واحدة متصلة. — Perspective + translateZ per layer with pre-scale and small rotations.
- **متى أستخدمها / when:** صور، بطاقات، ملصقات، عناوين بعمق — photos, cards, posters, titles with depth.
- **كيف / how:** parent perspective 1200px, transform-style preserve-3d; layers bg −400, mid −120, subject 0, occluder +200, each pre-scaled by (1200 − z)/1200 so it fills the frame; rotateY ≤ 6°, rotateX ≤ 4°; 8° orbit over 2000–3000 ms sine; orbit card −4° → +4° with a foreground occluder passing, caption pill spring (16/140), settle +2° and push 1.04. Real depth needs a perspective parent, preserve-3d, z travel, rotation and occlusion — scale alone is fake. fake3d style: python3 tools/kosif.py scaffold fake3d <dir>. **أرقام / params:** perspective 1200; z −400/−120/0/+200; ≤6°/4°.
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:36` · `kosif-tool/playbooks/photos.md:86` · `kosif-tool/styles/fake3d/SKILL.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/SKILL.md`

#### 3D-03 · صورة ثابتة بعمق طبقات · Still photo with layered depth · 📄 موصوف / documented only
- **ماذا / what:** المقدمة والموضوع والخلفية لصورة أرشيفية تتحرك بسرعات مختلفة أثناء اقتراب بطيء. — Foreground, subject and background of a still move at different rates during a slow push.
- **متى أستخدمها / when:** صور تاريخية، ألبومات، وثائقي — archive photos, documentaries.
- **كيف / how:** MG-056: 0–1 s hold, 1–6 s depth move, 6–8 s stop; cut the photo into 3 layers from a depth map (Z ≈ 0.45 … 1.22), inpaint the gaps, scale each layer by camera^Z; large moves reveal missing pixels — stay inside cut boundaries or inpaint; keep one pixel density across layers. **أرقام / params:** 8 s; Z 0.45–1.22.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md` · `kosif-tool/styles/pm-koldo2k-5cff87` · `kosif-atlas/skills/1526-gamegen/4175-game-world-building/SKILL.md`

#### 3D-04 · جسم ذهبي بسماكة مزيفة · Fake-3D extrusion & parallel projection · 🟢 جاهز / ready
- **ماذا / what:** جسم مسطح ذهبي بسماكة حقيقية المظهر يدور في لقطة واحدة وينتهي على ملصق: الشكل يُرسم N مرة مزاحًا على العمودي ويُسقط بمصفوفة واحدة. — A flat golden object with apparent thickness turns in one shot.
- **متى أستخدمها / when:** شعارات ورموز بلا WebGL — logos and emblems without WebGL.
- **كيف / how:** draw the same path N times offset along the projected face normal from back to front, darker toward the back (N = screen thickness / 1.5 px; gold #fff1bc → #f5b54a → #b4641a), top layer = lit face with gradient; rotate the object's u,v axes in 3D, project, and apply transform='matrix(ux,uy,vx,vy,cx,cy)' to the flat path, flipping to the back colour when facing away. Basma STY.fake3d: 16:9, calm, 1.9 wps, Alexandria, ink #2A1441, wall #EFE7DA, +2.4 s poster tail. Build sequence: outline draw-on 0.6 s → face fill 0.3 s → extrusion 0.5 s from a sparkle (DRAW-04). **أرقام / params:** layer step 1.5 px; poster +2.4 s.
- **الدليل / proof:** `app/public/js/10_studio.js:655` · `kosif-tool/styles/fake3d` · `kosif-tool/styles/fake3d/STYLE.json`

#### 3D-05 · العالم الأيزومتري · Isometric worlds · 🟢 جاهز / ready
- **ماذا / what:** إسقاط أيزومتري بدالة واحدة لكل نقطة، ترتيب عمق بمجموع x+y، ونوافذ وأبواب ملصقة على الأوجه، وكاميرا تنتقل بين مناطق ملونة. — One projection function for every point, painter's sort by x + y, face-mapped details, a camera travelling between zones.
- **متى أستخدمها / when:** رحلات، أنظمة، مدن مصغرة، لوجستيات — journeys, systems, miniature cities.
- **كيف / how:** X = OX + (x − y)·cos30·S, Y = OY + (x + y)·0.5·S − z·S (use it for camera targets and text anchors too); sort ground items by x + y, elevated items after what is beneath; matrix() maps flat rects onto box faces for windows/doors/signs; Three.js: OrthographicCamera pitched 35.264°, fixed grid unit; build wave: tiles rise by (i + j)·40 ms, buildings extrude 300 ms, then small agents walk. python3 tools/kosif.py scaffold isometric <dir>; Basma STY.isometric: 16:9, 2.0 wps, Readex Pro, bg #EEF1FF/#F4F1FF, ink #1E1B4B, zones #E4F5DC/#EEF0F8/#F6EEDC/#E9E4FA/#E4F2F5, colours #6366F1/#F59E0B/#14B8A6/#E11D48/#EC4899/#3B82F6; flat style sheet: 3 shades per hue for cube faces, ≤40 elements. **أرقام / params:** cos30 = 0.866; pitch 35.264°; 40 ms/tile.
- **الدليل / proof:** `kosif-tool/styles/isometric/SKILL.md` · `kosif-tool/playbooks/3d.md:44` · `app/public/js/10_studio.js:593` · `kosif-tool/styles/isometric`

#### 3D-06 · حقول المكعبات المتموجة · Cube heightfield waves & voxel ripples · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شبكة صناديق مكررة ترتفع كموجة شعاعية أو حلقية أو حسب بيانات، بقمم ملونة عشوائيًا وكاميرا مائلة. — A grid of instanced boxes rising as radial/ring waves or to data.
- **متى أستخدمها / when:** خلفيات تقنية، خرائط حرارية ثلاثية — tech backgrounds, 3D heatmaps.
- **كيف / how:** InstancedMesh grid 16×16 … 40×40; height = A·max(0, sin(r·f − ω·t)) (A 0.5–3 units, ω 2–4 rad/s) + noise; tops randomly orange/blue/white or 5% accent; isometric/orthographic or 45° perspective with soft shadows; data heatmap 24×16: scale.y to the value with a spring staggered 10 ms by distance from the hotspot (overshoot 1.1), colour grey → yellow → red; DOF on a bouncing glossy sphere. **أرقام / params:** ω 2–4 rad/s; stagger 10 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-tequilafunks-97f6c9` · `kosif-tool/styles/pm-sudeepsd-1a3485` · `kosif-tool/styles/pm-levabashidze-2d713a`

#### 3D-07 · جدران البطاقات المائلة · Tilted card & screenshot walls · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شبكة صور أو لقطات مواقع على مستوى مائل تنجرف ببطء وعنوان كبير فوقها. — A grid of thumbnails on a tilted plane drifting slowly under a headline.
- **متى أستخدمها / when:** «أعمالنا»، معارض، افتتاحيات — portfolios, showcases, openers.
- **كيف / how:** plane rotateX(20–50°) rotateZ(−15…−20°) with perspective 1200px, drift 30–60 px/s (or 3–4%/s), card radius 12 px, outer tiles blurred, dark radial scrim behind the headline; fly-over variant: camera translates then levels to focus one card (~1.5 s); floating variant: 4–6 cards at the edges rotated ±6° drifting 20–40 px over 4 s. **أرقام / params:** rotateX 20–50°; drift 30–60 px/s.
- **الدليل / proof:** `kosif-tool/styles/pm-listudio-820c7b` · `kosif-tool/styles/pm-arjunsh1607-93005d` · `kosif-tool/styles/pm-danilowm-d3720d`

#### 3D-08 · تحويلات البطاقات ثلاثية الأبعاد بالـCSS · CSS 3D card transforms · 📄 موصوف / documented only
- **ماذا / what:** قلب البطاقات ودورانها وميلها بالمنظور دون WebGL: قلب على الإيقاع، تقليب صفحات، مكعب كلمات، مروحة بطاقات، شريط أسطواني. — Perspective flips, tilts and carousels without WebGL.
- **متى أستخدمها / when:** كشف منتج، مقارنة، قوائم — product reveals, comparisons.
- **كيف / how:** parent perspective 900–1200px, preserve-3d, back face rotateY(180deg), backface-visibility hidden; rotationY 360 + rotationX 15 over 1.2 s sine.inOut; 3d-card-flip anchored to a downbeat (best span 0.8–1.6 s); page leaves rotateY ~150 ms per page with blur; text cube faces rotate 90° in 600 ms ease-in-out; card fan rotateY ±12° with opposing rotateZ, then float sin offsets (6 px, 3 s); cylinder carousel: cards at rotateY(step) translateZ(r ≈ 900px), rotate the group, floor reflection; poster tilt rotateY(−12°) rotateX(6°) with coloured slabs sliding out behind (800 ms). **أرقام / params:** perspective 900–1200; flip 0.8–1.6 s.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/3d-card-flip/scene.html` · `kosif-tool/styles/pm-twoclipping-6dd14e`

#### 3D-09 · طيران الكاميرا في عالم CSS · CSS 3D camera flight & depth scatter · 📄 موصوف / documented only
- **ماذا / what:** عالم preserve-3d يُحرَّك من حالة كاميرا واحدة على مراحل: غوص في شبكة مائلة، سحب للخلف، عبور بطاقات واقفة، تباطؤ للتركيز؛ وعناصر تتبعثر في سحابة عمق ثم تتجمع. — A preserve-3d world tweened leg by leg from one camera state; elements scatter into a depth cloud and assemble.
- **متى أستخدمها / when:** افتتاحيات ديناميكية بلا WebGL — dynamic openers without WebGL.
- **كيف / how:** landings power4.out, repositions power2.inOut, DOF via a --dof var on leaf elements; depth scatter/assemble: perspective 1400px, index-derived offsets, cloud spin power1.out, settle to a flat layout; orbit 3D flip entry: perspective 1800px, translateZ(220px) wins paint order, gsap.set the orbit start before phase 1; z-depth chaos: 30–50 chips at random x/y/z flying toward camera with blur ∝ |z − focus| (0–14 px) over 1.5–2 s; verify depth with angled ghost diagnostics. **أرقام / params:** perspective 1400–1800; blur 0–14 px.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/3d-camera-flight.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/depth-scatter-assemble.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/orbit-3d-entry.md`

#### 3D-10 · الأرضيات الشبكية والخريطة المائلة · Perspective grid floors & tilted planes · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** أرضية شبكة بمنظور تتلاشى نحو الأفق، حروف عملاقة واقفة عليها، أو خريطة مائلة تقف فوقها أشياء قائمة. — A grid floor fading to the horizon, standing billboard letters, or a tilted map with upright sprites.
- **متى أستخدمها / when:** سينث ويف، تقنية، رحلات على خريطة — synthwave, tech, map journeys.
- **كيف / how:** CSS rotateX(70deg) grid (alpha .15) fading to black, horizon at 30–55% height, 40 px module, dolly forward; synthwave variant with a point sphere above; tilted map: wrap the SVG in perspective(1400px) rotateX(θ ≈ 50°) and draw upright sprites in an overlay at Y' = Y·cosθ, z = Y·sinθ, scale = P/(P − z). **أرقام / params:** rotateX 70°; P = 1400, θ ≈ 50°.
- **الدليل / proof:** `kosif-tool/styles/map-journey` · `kosif-tool/styles/plotter` · `kosif-tool/styles/pm-pankajkumar-dev-0bee87`

#### 3D-11 · حلقات مدارية مائلة ورفع العقد · Pseudo-3D orbit rings & hover lift · 🟢 جاهز / ready
- **ماذا / what:** حلقتان إهليلجيتان خلف عنصر بطل، إحداهما مائلة والأخرى تنكشف بالدوران، وعقد ترتفع نحو المشاهد. — Two elliptical rings behind a hero, one tilted, one revealing by rotation; nodes lifting toward the viewer.
- **متى أستخدمها / when:** لوحات وعناصر بطل بلا WebGL — hero dials without WebGL.
- **كيف / how:** ::before rotateX(18deg) rotateZ(−20deg) with ring shadows; ::after rotate(−35deg) scaleY(.46) via orbit-reveal from rotate(−10deg) scaleY(.25) over 1.5 s ease-studio, atmosphere-in scale .86 → 1; rings 250 px / 248×220 px, borders #d9f3c730 / #cec1e13d; nodes preserve-3d lifting translateZ(40px) scale(1.08) in .35 s. **أرقام / params:** 1.5 s; translateZ 40 px.
- **الدليل / proof:** `kosif-audit-studio/studio.css:68` · `kosif-audit-studio/cinema/cinemaTheme.css`

#### 3D-12 · الأنفاق · Tunnels · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** أشكال متداخلة تتكبر أسيًا وتدور فتصنع نفقًا، أو نفق مربعات سلكية، أو نفق معرض بألواح وصور تتضخم نحو الكاميرا. — Nested polygons scaling exponentially, wire square tunnels, or a gallery tunnel of slabs and images.
- **متى أستخدمها / when:** انتقالات سرعة، افتتاحيات — speed transitions, openers.
- **كيف / how:** 6–20 nested hexagons/squares with scale = s0·k^(i + speed·t) mod range and incremental rotation, dashed strokes, radiating speed lines; HyperFrames gallery-tunnel: infinite square tunnel of saturated slabs (#FF6A00, #AB54F7, #EA3737, #0072E3, #00AA3C, #FFB200) and caller images, speed 3, fog 14.25. **أرقام / params:** 6–20 layers.
- **الدليل / proof:** `kosif-tool/styles/pm-crazyalphaaa-bc7e75` · `kosif-tool/styles/pm-itsuki-dev-10942d` · `kosif-one/vendor/hyperframes/registry/blocks/gallery-tunnel/gallery-tunnel.html`

#### 3D-13 · مكونات HyperFrames ثلاثية الأبعاد · HyperFrames 3D components & blocks · 📦 بأمر تثبيت / one install
- **ماذا / what:** مكونات وكتل جاهزة للعمق والمجسمات: رصة بطاقات بكاميرا، شريط منظوري، بطاقتان كالكتاب، بطاقات تدور، قرص منتج، بطل زجاجي، عنوان شظايا، بوابة سلكية، نفق معرض. — Ready depth and 3D components and blocks.
- **متى أستخدمها / when:** تركيبات HyperFrames — HyperFrames compositions.
- **كيف / how:** npx hyperframes add <name>: camera-rig-depth-stack, perspective-marquee (tilt flat|standard|steep), split-tilt-cards (book-open rotateY, badges spring-pop), three-orbiting-cards, tilt-card, canopy-part-title (3D leaves part, 12 s), code-slice-hero (cells flip under a depth field), cuboid-carousel (bevelled PBR cuboids on a wave, 6.67 s), exploded-stack (isometric plates explode with labels, 5 s), glass-hero (glass object refracting a giant headline, 5 s), glass-shard-title (Voronoi shards, 12.16 s — local copy lacks its matcap), orbit-card (10 s), product-turntable (6 s seamless loop, drop in a GLB), wireframe-portal-title (8 s), frost-sequence-camera-orbit (22.5 s, WebGPU shaders — local copy lacks its shard atlas), gallery-tunnel. Most load three (0.147–0.184) from a CDN; Latin fonts — swap to Arabic faces on canvas textures. **أرقام / params:** 16 items; 5–22.5 s.
- **تثبيت / install:** `npx hyperframes add product-turntable`
- **رخصة / license:** Apache-2.0; bundled assets carry their own licences (e.g. CC0 HDR, BSL Clipper)
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/product-turntable/product-turntable.html` · `kosif-one/vendor/hyperframes/registry/blocks/glass-hero/glass-hero.html` · `kosif-one/vendor/hyperframes/registry/blocks/exploded-stack/exploded-stack.html` · `kosif-one/vendor/hyperframes/registry/components/camera-rig-depth-stack/camera-rig-depth-stack.html`

## المحركات والرندر — Engines & renderers

_كيف يتحول مشهد WebGL إلى فيديو حتمي._

#### 3D-14 · مشروع three-kit ثلاثي الأبعاد · KOSIF three-kit 3D project · 🟢 جاهز / ready
- **ماذا / what:** مشروع 3D جاهز على حزمة window.K3 بلا npm: محرك عرض بمنحنى نغمات وظلال، وكتل عالم إجرائية، ورندر بمحرك الاستوديو. — A 3D project on the pre-bundled window.K3 kit: tone-mapped renderer, procedural world blocks, studio render.
- **متى أستخدمها / when:** أي مشهد ثلاثي الأبعاد حقيقي — any real 3D scene.
- **كيف / how:** python scripts/kmotion.py new NAME --3d --seconds 10 (or motion.py new NAME --3d) → src/main.js; without npm the import is rewritten to window.K3 and three-kit.bundle.js is copied (esbuild is not installed here, so kit edits cannot be re-bundled); render with motion.py render --engine studio. makeRenderer(canvas, W, H, {tone:'aces'|'agx'|'neutral', exposure:.6}): pixelRatio 1, PCF shadows, preserveDrawingBuffer — ACES punchy, AgX hue-stable highlights for fire/neon/sunsets, Khronos Neutral for products. **أرقام / params:** exposure 0.6; tone aces|agx|neutral.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js` · `kosif-studio/motion/kit/three-kit.bundle.js` · `100-superskills/skills/kosif-montage-motion/SKILL.md:85` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:76`

#### 3D-15 · عقد مشهد Three.js الحتمي · Deterministic Three.js seek scene · 🟢 جاهز / ready
- **ماذا / what:** صفحة HTML واحدة بـ render(t) حتمية، تُلتقط إطارًا إطارًا بمتصفح بلا واجهة: لا THREE.Clock، الكاميرا دالة للزمن، وتسخين المظللات قبل أول إطار. — One HTML page with a deterministic render(t), captured frame by frame headless.
- **متى أستخدمها / when:** كل مشهد WebGL يصبح فيديو — every WebGL scene that becomes video.
- **كيف / how:** renderer {preserveDrawingBuffer:true}; window.__kosif = {duration, fps, seek} (render_html.cjs) or window.__ready + render(t) + __duration (html_render.py / film.py animate); wait for fonts, warm shaders with seek(0) → seek(mid) → seek(0), gl.finish() after each frame, set ready only after the first real frame; one camera move per shot as a function of t; template scene-3d.html: three@0.169, ACES exposure 1.05, UnrealBloom (0.7, 0.6, 0.82), < 150k visible tris. python html_render.py page.html out.png --size 1920x1080 --t 2.5 renders one deterministic frame (finds Chromium at /opt/pw-browsers). **أرقام / params:** < 150k tris; bloom .7/.6/.82.
- **الدليل / proof:** `kosif-tool/tools/render_html.cjs` · `kosif-studio/html_render.py` · `100-superskills/skills/claude-animation-studio/templates/scene-3d.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/three.md`

#### 3D-16 · ثلاثي الأبعاد في Remotion · Remotion ThreeCanvas · 📦 بأمر تثبيت / one install
- **ماذا / what:** مشاهد React Three Fiber تُرندر بدقة الإطار لأن كل حركة من رقم الإطار. — R3F scenes rendered frame-exactly by driving everything from the frame number.
- **متى أستخدمها / when:** مشاريع Remotion بعناصر 3D — Remotion projects with 3D.
- **كيف / how:** @remotion/three <ThreeCanvas width height> with ambient 0.4 + directional 0.8; rotation = frame·0.02; never useFrame() from R3F and no self-animating shaders (pass frame as a uniform). **أرقام / params:** ambient .4; directional .8.
- **تثبيت / install:** `npm i @remotion/three three @react-three/fiber`
- **رخصة / license:** Remotion company license
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/3d.md`

#### 3D-17 · بوابات ومشهد داخل مشهد · Portals & render-to-texture · 📦 بأمر تثبيت / one install
- **ماذا / what:** مشهد خارج الشاشة يُرسم في خامة على لوح، مع بارالاكس بنسخ مصفوفة الكاميرا الرئيسية. — An offscreen scene rendered into a texture on a plane, parallaxed by copying the main camera.
- **متى أستخدمها / when:** نوافذ إلى عوالم، شاشات داخل مشاهد — windows into worlds, screens in scenes.
- **كيف / how:** R3F createPortal + useFBO (or a WebGLRenderTarget in plain three); sample in screen space with gl_FragCoord.xy / resolution; render the portal pass before the main pass each frame.
- **تثبيت / install:** `npm i @react-three/fiber @react-three/drei three`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### 3D-18 · عالم البلورات بـ WebGL خام · Raw-WebGL procedural crystal shards · ✅ مُثبت هنا / proven here
- **ماذا / what:** مشهد WebGL1 بلا مكتبات لشظايا بلورية منخفضة المضلعات تنجرف وتدور وتتمايل في الضباب خلف الواجهة، حتمي بالبذرة. — A library-free WebGL1 scene of drifting low-poly crystal shards, deterministic per seed.
- **متى أستخدمها / when:** خلفيات حية خفيفة جدًا (~18 KB) — very light living backgrounds.
- **كيف / how:** SQCCrystal.mount(canvas, {density, interactive, scroll, still, seed, palette}) → {setMood, pulse, destroy, frames, shards}; shard = irregular hexagonal prism (6 sides, irregularity .45) with pointed caps and flat per-face normals, 24 triangles / 72 vertices; N = round((phone ? 14 : 30)·(weak device ? 0.7 : 1)·density) ≥ 6; z slab −4…−18; spin ±(.12, .17, .1) rad/s; bob sin(.5t + φ)·(.15….5); fov .95 rad; LCG seed 20261005; tests 4/4 passed here. **أرقام / params:** 24 tris/shard; ~18 KB.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/crystal-world.js` · `kosif-earth-ci-fork/tools/crystal_world.test.mjs`

#### 3D-19 · 3D مرسوم برمجيًا على Canvas · Software-rendered 3D on canvas · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** إسقاط رؤوس مجسم بمصفوفة منظور، ترتيب الأوجه من الخلف للأمام، وتظليل مسطح بضوء واحد — بلا WebGL. — Project a mesh with a perspective matrix, sort faces back to front, flat-shade with one light.
- **متى أستخدمها / when:** مجسمات بسيطة سلكية أو مسطحة، أسلوب تقني — simple wireframe/flat-shaded objects.
- **كيف / how:** rotate vertices on two axes (60–90°/s), project with f / (z + d), painter-sort faces by mean z, shade by max(0, n·l); wireframe → shaded transition by fading fill in; ~128–420 faces; HUD extras: two tilted orbit ellipses, crop brackets, numeric readout, giant outline word behind at 10%; words placed on a 3D ring around the object, depth-scaled. **أرقام / params:** ~128–420 faces; 60–90°/s.

```js
function project([x, y, z], a, b, f = 600, d = 6) {      // yaw a, pitch b
  const x1 = x * Math.cos(a) - z * Math.sin(a), z1 = x * Math.sin(a) + z * Math.cos(a);
  const y1 = y * Math.cos(b) - z1 * Math.sin(b), z2 = y * Math.sin(b) + z1 * Math.cos(b);
  const s = f / (z2 + d); return [W / 2 + x1 * s, H / 2 + y1 * s, z2];
}
// faces.sort((p, q) => meanZ(q) - meanZ(p)); fill with shade = max(0, dot(normal, light))
```

- **الدليل / proof:** `kosif-tool/styles/pm-grace-sunnyy-29bc61` · `kosif-tool/styles/pm-teslachartz-c58b32` · `kosif-tool/styles/pm-gizakdag-b8c59e`

#### 3D-20 · كرات وحلقات من النقاط · Point spheres, particle tori & dot globes · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نقاط على كرة فيبوناتشي أو طارة تدور وتُسقط بحجم ولون حسب العمق، مع مدارات، وتحول طارة إلى كرة، وكرة أرضية من نقاط اليابسة. — Fibonacci-sphere or torus points rotating with depth-based size/colour, orbits, torus → sphere morphs, dot-matrix globes.
- **متى أستخدمها / when:** ذكاء اصطناعي، شبكات، عالمية — AI, networks, global themes.
- **كيف / how:** 500–2000 points (globe ~20k sampled on a land mask with warm city dots), rotate Y 20–40°/s (globe 3°/s), size and alpha by z, colour by depth (violet → red, pink → blue), additive glow; 1–2 tilted elliptical orbits with small moving dots; morph by lerping each point between its torus and sphere positions; fresnel rim + bloom for globes; macro science opener: ~1500 instanced spheres in a translucent glass sphere with a blurred background and an italic 'Fig. 1' caption. **أرقام / params:** 500–2000 pts; 20–40°/s.
- **الدليل / proof:** `kosif-tool/styles/pm-jasonzhou1993-8595e0` · `kosif-tool/styles/pm-ghinaiya-nirmal-5d8fec` · `kosif-tool/styles/pm-nolkeeg-bf062e` · `kosif-tool/styles/pm-shinskinakamoto-20190b`

#### 3D-21 · الرسم بالأشعة ودوال المسافة · Raymarched SDF scenes · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** فقاعات معدنية ملتحمة، كرات زجاجية تكسر النص، سحب حجمية، وثقب أسود يحني الضوء — كلها في شيدر شاشة كاملة. — Metaballs, refracting glass spheres, volumetric clouds and black-hole lensing in a full-screen shader.
- **متى أستخدمها / when:** لقطات بطل مجردة، فضاء، فخامة — abstract hero shots, space, luxury.
- **كيف / how:** SDF smooth-union spheres (k ≈ 0.5) with fresnel rim and specular or orange-blue gradient; glass: refraction of a type texture with chromatic dispersion, 96 steps; clouds/smoke: 64–128 steps accumulating FBM density, bounded loops; black hole: integrate light paths with approximate bending (step 0.05–0.1 r_s, 200–400 steps), thin turbulent disk 3–15 r_s over a star map; pass t as a uniform, never self-animate. **أرقام / params:** 64–128 steps; k 0.5.
- **الدليل / proof:** `kosif-tool/styles/pm-zaqailo-212ad3` · `kosif-tool/styles/pm-ndhabarde11-f155b4` · `kosif-tool/styles/pm-rebutonepress-810f78` · `kosif-atlas/skills/2199-lvtd-skills/8087-game-sdf-and-field-modeling/SKILL.md`

#### 3D-22 · نماذج GLB بحركة مضبوطة على الزمن · GLB models with seeked animation · 🟢 جاهز / ready
- **ماذا / what:** تحميل نموذج GLB جاهز أو مصنوع في Blender وضبط حركته الهيكلية على الزمن المطلق. — Load a GLB and seek its skeletal/object animation to absolute time.
- **متى أستخدمها / when:** شخصيات أو منتجات جاهزة — ready characters or products.
- **كيف / how:** m = await K3.loadModel(url, {clip, offset, speed, caustics}); m.userData.set(t) → mixer.setTime (motion.py bundle inlines the GLB as a data URL); pipeline: Blender → glTF 2.0/GLB with applied transforms, consistent units/pivots, colour maps sRGB, normal/roughness non-colour → glTF Transform prune/dedup/simplify, Meshopt or Draco geometry, KTX2/BasisU textures; addWave for cloth/flags; licence any downloaded model.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:964` · `kosif-atlas/skills/2696-game-studio/10370-web-3d-asset-pipeline/SKILL.md` · `kosif-atlas/skills/1526-gamegen/4161-blender-game-assets/SKILL.md`

#### 3D-23 · Blender بلا واجهة · Headless Blender (bpy) · 📦 بأمر تثبيت / one install
- **ماذا / what:** Blender كمكتبة بايثون لبناء المشاهد ورندرها أو تصدير GLB؛ وBlender MCP وCinema 4D وSpline خارج الحاوية. — Blender as a Python module for scenes, renders and GLB export.
- **متى أستخدمها / when:** نمذجة معقدة أو رندر Cycles — complex modelling or Cycles renders.
- **كيف / how:** pip install bpy (Blender 5.2, ~400 MB) then build the scene in Python, keep the frame → time mapping explicit, export GLB for three-kit (3D-22) or render frames with Eevee/Cycles (CPU only here — slow); Blender MCP, Cinema 4D MoGraph/Redshift (paid) and Spline (proprietary) need the user's own install or account.
- **تثبيت / install:** `pip install bpy`
- **رخصة / license:** Blender GPL-2.0-or-later (outputs are yours)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md` · `kosif-atlas/skills/228-mas-3d-games/706-cinema-4d/SKILL.md`

#### 3D-24 · تحليق Cesium فوق تضاريس ومدن حقيقية · Cesium terrain & city flyovers · 🔑 مفتاح أو خدمة / needs key
- **ماذا / what:** تحليق كطائرة مروحية فوق تضاريس حقيقية أو مدن ثلاثية واقعية، يُرندر إطارًا إطارًا. — Helicopter-style flights over real terrain or photoreal cities, frame by frame.
- **متى أستخدمها / when:** رحلات جغرافية، عقارات، سياحة — geography, real estate, tourism.
- **كيف / how:** Cesium 1.143 from a CDN after setting CESIUM_BASE_URL; landscape: MapTiler terrain-quantized-mesh-v2 + satellite-v2 (MapTiler key, no Cesium ion token); city: Google Photorealistic 3D Tiles with the globe hidden (Google Maps key; promo clips ≤ 30 s), maximumScreenSpaceError 4 for hero landmarks, 6–8 wide; render a mid-frame still before the full clip; globe checks: record longitude origin, verify ≥3 known places, shortest-path rotation, unwrap the antimeridian. **أرقام / params:** SSE 4 hero / 6–8 wide.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/TECHNIQUE.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/SKILL.md`

## العوالم الإجرائية — Procedural worlds

_سماء وأرض وماء وغابة — كلها من دوال._

#### 3D-25 · تضاريس إجرائية · Procedural terrain · 🟢 جاهز / ready
- **ماذا / what:** سطح تزيحه دالة ارتفاع (ضوضاء متعرجة، التواء المجال، نهر محفور) بألوان من الارتفاع والميل وخرائط تفصيل مكررة. — A plane displaced by a height function with height/slope colours and tiled detail maps.
- **متى أستخدمها / when:** جبال، كثبان، وديان، خلجان — mountains, dunes, valleys, bays.
- **كيف / how:** K3.makeTerrain({height(x,z), colour(h,slope,x,z,c), seg:560, size:4600, texSize:1024, albedoRepeat:60, normalRepeat:90, normalScale:.55, roughness:.95}); alpineColour palette snow #f4f7fb, rock #5d5a58/#7a6f66, grass #4e6e34/#6b8a3c, sand #b9a77a, deep #2f4a3a; mountains behind a bay: warp x,z by 180·fbm(.0009), ridge 820·exp(−((z+1250)/820)²)·(.55 + .45·ridged), hills 260·ridged(.0011), detail 55·fbm(.004) + 14·fbm(.02), river x = 140·sin(z/420) − 220 carved 150·exp(−d²/(2·55²)); dunes: vnoise fbm 5 octaves (×0.5 amp, ×2.03 freq), dune = 4.5·fbm(x·.006) + 1.8·fbm(x·.02 + 9) − 3, sand #E2B577 → #B9824B. **أرقام / params:** seg 560; size 4600 m.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:112` · `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:7` · `kosif-one/projects/egypt-2120-animation/index.html`

#### 3D-26 · غابة صنوبر بالمثيلات · Instanced conifer forest · 🟢 جاهز / ready
- **ماذا / what:** حتى 22 ألف شجرة صنوبر بطبقتين وتيجان متعرجة ببذرة، توزع بقاعدة قبول حسب الارتفاع والميل والتكتل. — Up to 22k instanced two-tier conifers placed by an accept rule.
- **متى أستخدمها / when:** جبال وغابات وطبيعة — mountains, forests, nature.
- **كيف / how:** K3.makeForest({height, region:[x0,x1,z0,z1], accept(x,z,h), max:22000, scale, hue:.25 ± .035, tiers:4, thinFrom:300, thinTo:430, seed}); K3.coniferCrown(tiers, seed); trunk #4a3524; per-tree colour. **أرقام / params:** max 22000; 4 tiers + spire.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:150` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:174`

#### 3D-27 · السماء والشمس والإضاءة البيئية · Sky, sun & gradient IBL · 🟢 جاهز / ready
- **ماذا / what:** سماء رايلي/مي فيزيائية تتبع الشمس فيها القصة (فجر ← نهار ← غيم ← صفاء)، أو قبب سماء مكتوبة لمزاج معين، وإضاءة بيئية من تدرج بلا ملفات HDRI. — A physical sky whose sun follows the story, custom mood skies, and IBL from a gradient.
- **متى أستخدمها / when:** كل مشهد خارجي — every outdoor scene.
- **كيف / how:** sky = makeSky(scene, {turbidity, rayleigh, mie, mieG, scale}); sky.setSun(elev, azim) e.g. elev 2.5 + 24·smooth(0, 6.5) − 8·smooth(8, 10) + 12·smooth(12.5, 15.5), turbidity 3 + 7·overcast; fog colour = sky horizon colour (aerial perspective), FogExp2 #c9d6e2 1.1e-4; custom domes (BackSide sphere ShaderMaterial): blue hour zen (.02,.045,.13) mid (.07,.15,.36) horizon (.30,.34,.52) + afterglow band exp(−9y)·g³·(1,.45,.2), night moon glow pow(m,900)·1.2 + pow(m,60)·.16; envFromGradient(renderer, scene, {top, horizon, ground, sun, sunColor, sunPower}) with environmentIntensity .5–.55. **أرقام / params:** fog 1.1e-4; env .5–.55.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:64` · `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:26` · `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:32`

#### 3D-28 · البحر والماء · Sea & water surfaces · 🟢 جاهز / ready
- **ماذا / what:** بحر عاكس بخرائط نورمال، بحر ليلي يعكس القمر بأمواج طويلة، ماء ضحل صافٍ يُظهر القاع، وبحر من شبكة ارتفاعات بزبد. — Reflective sea, moonlit swell, shallow clear water and a height-field sea with whitecaps.
- **متى أستخدمها / when:** شواطئ، قوارب، برك — coasts, boats, ponds.
- **كيف / how:** makeSea({size:30000, res:768}) (Three Water, FBM normals); night: makeSea({size:24000, res:1024, color:0x061525, distortion:3.2, waveSize:2.4, normals: normalFromHeight(512, …)}) with sunDirection = moon, kelvin(4100)·.9, boat heave .09·sin(1.25t + .4) + .035·sin(2.3t + 1.7); shallow: makeShallowWater({seg:300, amp:.006, clarity:.72, deep:0x1c3a22, shallow:0x4d6a45, skyTop:0x8fb3d8, skyHorizon:0xe9c48e, ripples:28}); whitecaps: Plane 320² displaced by 4 noise octaves + .45·sin(.3x + .1y), crest blend smoothstep(h, .9, 1.7) to white, clearcoat 1, roughness .24; Gerstner sunset ocean: 4–8 waves (λ 2–30 m, A .05–.4 m), fresnel sky mix, glitter path from a 5° sun. **أرقام / params:** res 768–1024; heave .09.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:186` · `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:58` · `kosif-studio/scenes/whale_dragon_3d.html:86`

#### 3D-29 · السحب · Clouds · 🟢 جاهز / ready
- **ماذا / what:** لوح سحب يُرسم بالأشعة في 36 خطوة، أو سحب ركامية كرتونية من تجمعات كرات بتدرج ثلاثي. — A raymarched cloud slab, or toon cumulus from sphere clusters.
- **متى أستخدمها / when:** سماء واقعية أو كرتونية — realistic or toon skies.
- **كيف / how:** three-kit cloud slab (36 raymarch steps) with the sun from the sky model; toon: 20–60 instanced spheres per cloud, 3-band ramp violet #5a3a8a shadow / pink #b066a0 mid / peach #f0c09a rim from a low (~5°) sun, soft fresnel outline. **أرقام / params:** 36 steps; 20–60 spheres.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:106` · `kosif-tool/styles/pm-nft-chen-5f8bb0`

#### 3D-30 · بركة الكوي والعشب والتفاصيل الحية · Koi pond, reeds & living details · 🟢 جاهز / ready
- **ماذا / what:** ماء ضحل بتموجات حلقات البتلات، كاويات، سبع سمكات كوي، بتلات تسقط، حصى، قصب يتمايل، وشمس مرقطة عبر الأغصان بمسار كاميرا واحد. — A living pond: caustics, koi, falling petals, pebbles, swaying reeds and dappled sun.
- **متى أستخدمها / when:** لقطات هادئة فاخرة، طبيعة يابانية — calm premium nature shots.
- **كيف / how:** makeShallowWater, addCaustics, makeKoi (CHAR-43), makePetals, makePebbles, makeBlades({n:1500, tall:.9, width:.02, hue:.24}) swaying 1.4 Hz (bend ∝ height²), makeDappledSun, cameraPath; pond ellipse 6.4 × 4.1 m, exposure .62, fog #CBB08A .011, 10 s 1080p30. **أرقام / params:** 1500 blades; 1.4 Hz sway.
- **الدليل / proof:** `kosif-studio/motion/projects/koi_pond/src/main.js:1` · `kosif-studio/motion/kit/three-kit.js:746`

#### 3D-31 · مؤشرات المقياس: جبال وطريق وأضواء بعيدة · Scale cues: ridge layers, road ribbon, far lights · 🟢 جاهز / ready
- **ماذا / what:** طبقات جبال بعيدة بحواف متعرجة، طريق على منحنى مع تسوية الأرض حوله، وأضواء شاطئ بعيدة على بعد 6 كم تعطي المشهد حجمه. — Distant ridge layers, a curved road ribbon with flattened terrain, and far shore lights for scale.
- **متى أستخدمها / when:** مشاهد ليلية وطرق ومسافات كبيرة — night roads, vast landscapes.
- **كيف / how:** ridges: PlaneGeometry(dz·4.2, hgt·1.6, 400, 1) whose top vertices follow ridged noise, layers [700 m, 140], [1400, 260], [2600, 420], [4500, 650]; road: CatmullRom centreline sampled every 20 m to −4200, offset by the normal, triangulated (N 800), terrain height × smooth(ROAD_W, ROAD_W + 30, |x − roadX(z)|); far lights: 150 Points at z ≈ −6480, height 4–18 m, 70% kelvin(2200–3100) else 5200, size 1.6 px, additive, opacity .75, fog off. blue_hour renders light trails with render --blur 16 --shutter 30 --stack lighten. **أرقام / params:** ridges 700–4500 m; lights at ~6.5 km.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:54` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:178` · `kosif-studio/motion/projects/blue_hour/src/main.js:1`

#### 3D-32 · بدن قارب بمعادلات · Parametric lofted boat hull · 🟢 جاهز / ready
- **ماذا / what:** بدن فلوكة يتولد من منحنيات العرض والحافة والقاعدة على طوله، مع الصاري والشراع المطوي والحبال. — A felucca hull generated from beam, sheer and keel curves, with mast, yard and rigging.
- **متى أستخدمها / when:** النيل، البحر، القصص التراثية — the Nile, the sea, heritage stories.
- **كيف / how:** beam(s) = 1.12·sin(π(.13 + .87s))^.62; sheer(s) = .78 + .62s^3.2 + .22(1 − s)^5; keel(s) = −.62·sin(π(.04 + .96s))^.45; x = side·b·(1 − (1 − φ)^2.4); grid 72 × 16 per side; L 7.2 m; yard rotated −1.02 rad, 8.6 m; sail = 9 tapered cylinders. **أرقام / params:** L 7.2 m; 72×16 grid.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:14`

#### 3D-33 · مدينة المستقبل: نوافذ وطاقة وعمارة · Future city kit (windows, solar fields, architecture) · 🟢 جاهز / ready
- **ماذا / what:** آلاف المباني المكررة بنوافذ مضاءة تُحسب من الموضع، حقول مرايا شمسية وألواح ومحاور ري، وعناصر عمارة مستقبلية: مزارع عمودية، قطار مغناطيسي، برج لوتس، منارة. — Instanced night city with computed windows, solar fields and futuristic props.
- **متى أستخدمها / when:** رؤى مستقبلية لمدن عربية — future visions of Arab cities.
- **كيف / how:** InstancedMesh up to 2600 boxes skipping avenues (gx % 6, gz % 7); window grid (u/2.4, y/3.2), mask .18–.82 × .22–.78, lit if hash > 1 − lit (.32–.8), warm #FFC77A / cool #8FE6FF, base #0B1226, rim pow(1 − |N·V|, 3)·.35 #3B5BA8, bands step(.985, fract(y/38 + seed)), fog #121A44 .0021; 900 heliostats lookAt a receiver (metal 1, roughness .05, env 2.2) pulsing 1 + .08·sin 9t, 2400 panels, 160 pivots; props with emissive colours × > 1 so bloom catches them (farm tiers #7CFF9F ×2.2, maglev stripe #59E3FF ×4, lotus petals #FF8FD0 at .26, Pharos bands #FFD9A0 ×5). Showcase: Egypt 2120 (1080×1920, 18 s, 6 shots, Three 0.169, Cairo glass captions, synthesised Hijaz score). **أرقام / params:** 2600 buildings; 900 heliostats.
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html` · `kosif-one/projects/egypt-2120-animation/README.md`

#### 3D-34 · مركبات ودعائم من أشكال أولية · Props & vehicles from primitives · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** طائرة من دالة مصنع واحدة، مركبة كرتونية منخفضة المضلعات بحد أسود، دعائم مكتب، بلاطة خشبية بخامة مرسومة، صخور عائمة، كهف، وجزيرة ديوراما. — Vehicles and set dressing built from primitives.
- **متى أستخدمها / when:** مشاهد سريعة بلا نماذج جاهزة — quick scenes without downloaded models.
- **كيف / how:** lathe fuselage + extruded wings + prop blades with per-part materials; box primitives with MeshToon + black outline pass; mug cylinder + liquid disc + steam sprites, hex pencil, paper plane; RoundedBoxGeometry(1, 1, .35, 4, .08) with a canvas grain texture (#d3bb9b / #a58862) and a serif letter; displaced cones/cylinders with vertical striation and fog .02; flatShaded displaced icosahedrons (detail 1, displacement .3) in crimson #350006 fog 10–40; floating island disc with layered rim at fov 30. **أرقام / params:** toon + outline; fog .02.
- **الدليل / proof:** `kosif-tool/styles/pm-buildfastwithai-ed9447` · `kosif-tool/styles/pm-anilraok-eff262` · `kosif-tool/styles/pm-gorden-sun-041f56`

#### 3D-35 · مناورات طيران على مسار · Aircraft spline manoeuvres & chase cam · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** طائرة على مسار Catmull-Rom تميل بزاوية تُشتق من انحناء المسار، مع لفات وغطسات مكتوبة، وكاميرا مطاردة تميل معها. — A plane on a spline banking from curvature, with scripted rolls and a banking chase cam.
- **متى أستخدمها / when:** طيران، سفر، مغامرة — flight, travel, adventure.
- **كيف / how:** bank = atan(v²·κ/g) capped at 80°; add barrel-roll / spiral-dive segments; chase camera behind and above with lag; over procedural patchwork terrain + fog. **أرقام / params:** bank ≤ 80°.
- **الدليل / proof:** `kosif-tool/styles/pm-nft-chen-5f8bb0` · `kosif-tool/styles/pm-buildfastwithai-ed9447`

## المواد والإضاءة وما بعد المعالجة — Materials, lighting & post

_الضوء يصنع الفخامة: مفتاح واحد، مواد فيزيائية، وبلوم محسوب._

#### 3D-36 · وصفة الإضاءة السينمائية · Cinematic 3D lighting recipe · 🟢 جاهز / ready
- **ماذا / what:** ضوء مفتاح واحد باتجاه واحد وحرارة لونية محددة، ثلاث نقاط بنسبة 5:1، وإعدادات جاهزة (رامبرانت، صدفة، حاد، ناعم جدًا، شمس). — One key with a defined Kelvin, 5:1 three-point rigs and named presets.
- **متى أستخدمها / when:** كل مشهد 3D — every 3D scene.
- **كيف / how:** three-kit lightRig {key, fillStops 2, rimStops 0.5, keyK 5600, fillK 6500, rimK 4300} (5:1); lightPreset rembrandt / clamshell / edgy / ultrasoft / short / broad / sun; playbook: key 45°, fill 30%, rim; fov 40–55 (85 mm ≈ 24°); primitives + seeded InstancedMesh crowds; Standard/Physical + PMREM env; custom shaders only for sky/water; fog colour from the sky horizon. **أرقام / params:** 5:1; 5600/6500/4300 K; fov 40–55.
- **الدليل / proof:** `100-superskills/skills/hyperframes-animation-studio/scripts/kit/three-kit.js` · `100-superskills/skills/cinematic-3d-scene/SKILL.md` · `kosif-tool/playbooks/3d.md`

#### 3D-37 · المواد الفيزيائية · Physical materials (glass, chrome, wet, iridescent) · 🟢 جاهز / ready
- **ماذا / what:** زجاج بنفاذية وانكسار وتشتت، كروم عاكس، جلد مبلل بطبقة لامعة، فقاعات متقزحة، وخرائط نتوء وخشونة تُولَّد في Canvas بلا تحميل صور. — Glass, chrome, wet clearcoat, iridescent shells and canvas-generated bump/roughness maps.
- **متى أستخدمها / when:** لقطات منتج وبطل فاخرة — premium product and hero shots.
- **كيف / how:** glass: MeshPhysicalMaterial transmission 1, thickness 1.4, ior 1.5–1.62, dispersion .35, iridescence .9, clearcoat 1, attenuation colour + distance (transmission over a text plane refracts the type); chrome: metalness 1, roughness .05–.2 with an env map and a coloured rim light; wet skin: clearcoat 1 over rough hide; noiseTexture(size, scale, octaves, base, amp, seedZ) with three's ImprovedNoise → CanvasTexture RepeatWrapping (skin bump 512/24/5 oct, roughness 256/10/4); iridescent blob: noise-displaced sphere with thin-film/fresnel rainbow; emissive × > 1 with toneMapped:false to feed bloom. **أرقام / params:** ior 1.5–1.62; roughness .05–.2.
- **الدليل / proof:** `kosif-studio/scenes/whale_dragon_3d.html:60` · `kosif-studio/scenes/whale_dragon_3d.html:1`

#### 3D-38 · سلسلة ما بعد المعالجة · Post stack (bloom, ACES, film) · 🟢 جاهز / ready
- **ماذا / what:** بلوم بعتبة عالية، منحنى ACES، حبيبات فيلم، وإخراج sRGB — ومعالجة خفيفة سريعة للاستوديو. — High-threshold bloom, ACES, film grain and sRGB output; a fast lite post for the studio.
- **متى أستخدمها / when:** كل مشهد WebGL يحتاج توهجًا — any WebGL scene needing glow.
- **كيف / how:** EffectComposer → RenderPass → UnrealBloomPass(strength .22–.7, radius .5–.6, threshold .82–.9) → FilmPass .22 → OutputPass; ACES exposure .6–1.55 by scene; HalfFloat render target with 4× MSAA; K3S.makeLitePost(renderer, scene, camera, W, H) for bloom + grade; three-kit bloom .22/.6/.9; keep bloom threshold ≥ .9 for cute/product scenes so only emissives glow; letterbox opening 70 px → 0 over 2.2 s in the scene3d template. **أرقام / params:** bloom .22–.7 / .5–.6 / .82–.9.
- **الدليل / proof:** `kosif-studio/scenes/whale_dragon_3d.html:266` · `kosif-studio/motion/kit/shape-kit.js` · `100-superskills/skills/claude-animation-studio/templates/scene-3d.html` · `kosif-studio/motion/templates/scene3d/src/main.js`

#### 3D-39 · استوديو المنتج الكريمي · Studio sweep, backdrop & stage disc · 🟢 جاهز / ready
- **ماذا / what:** خلفية استوديو لا نهائية كريمية بظل تلامس وشبكة خافتة وثلاث إضاءات ناعمة، أو خلفية متدرجة وقرص قياس بمسح ضوئي. — A cream infinite sweep with contact shadow, faint grid and soft three-light rig, or a gradient backdrop and a scanning stage disc.
- **متى أستخدمها / when:** عرض منتجات وشخصيات — product and character showcases.
- **كيف / how:** K3.studio(scene, {bg:'#f1efe8', grid}) — shadow .22, grid 16 m / 32 div #c9d8c2 / #d9e4d4 at .35, key 2.6 white at (3, 6, 4), fill #dfe8ff .9, rim 1.4, hemi .9 #ffffff / #cfd8c8; K3S.studioBackdrop({inner, mid, outer, cy}) and K3S.stageDisc({radius:.24, color:0x9dffb4, shadow:.5}) with a scan sweep. **أرقام / params:** key 2.6; fill .9; rim 1.4.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:194` · `kosif-one/tools/kosif-studio/motion/kit/shape-kit.js:336`

#### 3D-40 · مجسمات بطل جاهزة · Hero objects (geode, knot, coin) · 🟢 جاهز / ready
- **ماذا / what:** جيود بلوري: قشرة معدنية داكنة بنواة متوهجة وحلقتين مداريتين تدور بسرعات مختلفة؛ عقدة طارة متوهجة؛ عملة كرومية. — Ready hero objects for tech/AI and finance.
- **متى أستخدمها / when:** افتتاحيات تقنية وذكاء اصطناعي ومال — tech, AI and finance openers.
- **كيف / how:** geode: IcosahedronGeometry(2.2, 2) MeshStandard #0f172a metalness .85 roughness .15; inner OctahedronGeometry(1.4) emissive #0284c7 ×.8; two TorusGeometry(3.6, .04, 16, 100) MeshBasic #38bdf8 at .6 tilted π/3 and π/4; rotations .45/.6/.8/.9/.3/.4 rad/s from t; knot: TubeGeometry torus knot (2,3) with gradient emissive; coin: extruded bevelled disc, metalness 1 roughness .2, ~40°/s tumble behind the headline. **أرقام / params:** shell r 2.2; core 1.4; rings 3.6.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:128` · `kosif-tool/styles/pm-eyishazyer-af035b` · `kosif-tool/styles/pm-micheleharmonic-77628e`

#### 3D-41 · مشهد سينمائي بإطار واحد · Cinematic single-frame 3D page recipe · 🟢 جاهز / ready
- **ماذا / what:** لقطة Three.js حتمية: مواد فيزيائية، مفتاح بارد بظلال ناعمة، نار دافئة متذبذبة، ضباب، جسيمات إضافية للنار والرذاذ، ومطر خطوط، وبلوم وفيلم. — A deterministic Three.js shot with cold key, flickering fire light, fog, additive particles, rain and bloom.
- **متى أستخدمها / when:** لوحة ملحمية أو غلاف — epic stills and covers.
- **كيف / how:** one HTML with an importmap to three@0.170; ACES exposure 1.55; PCFSoftShadowMap 2048; FogExp2 0x0d151f .013; cold DirectionalLight 0xcfe0ff 3.2; fire PointLight 0xff8a3a 140 flickering ±25 at 23 rad/s + SpotLight 0xffa050 220; Hemisphere 0x4a5e80 / 0x070a10 .9; bloom (.32, .5, .88); FilmPass .22; fov 46; set window.__ready after the first composer.render; render with html_render.py or film.py animate. **أرقام / params:** exposure 1.55; bloom .32/.5/.88.
- **الدليل / proof:** `kosif-studio/scenes/whale_dragon_3d.html:1` · `kosif-one/tools/kosif-studio/scenes/whale_dragon_3d.html` · `kosif-studio/references/drawing-guide.md:99`

## النحت بدوال المسافة — SDF sculpting

_أشكال عضوية ناعمة تُنحت بالكود وتصبح شبكة مغلقة._

#### 3D-42 · نحت SDF وشبكة الأسطح · SDF sculpting & surface-nets mesher · ✅ مُثبت هنا / proven here
- **ماذا / what:** كرات وإهليلجات ومخاريط مدورة وصناديق وطارات تُدمج بنعومة وتُحفر وتُلوَّن، ثم تتحول إلى شبكة مغلقة بألوان رؤوس ونورمال من الحقل. — Smooth-unioned SDF primitives meshed into a watertight vertex-coloured mesh.
- **متى أستخدمها / when:** تمائم، أشياء لطيفة، أشكال عضوية — mascots, cute objects, organic shapes.
- **كيف / how:** const S = K3S.sculpt().sphere(c, r).ellipsoid(c, [rx, ry, rz], {rot}).capsule(a, b, r1, r2).box(c, [hx, hy, hz], round).torus(c, R, r) with {k, op, rot, color}, .paint(); geo = S.mesh({cells:96 (bunny 132), project, slack}) — coarse-to-fine surface nets (block 4 cells, refine near the surface, 2 Newton projection steps) → geometry.userData.stats {grid, evals, vertices, triangles, ms}; S.hit(from, dir, maxDist) ray-marches (256 steps, step .8·d) to place eyes/buttons exactly on the surface. Tests passed here: sphere volume ratio .9996, area .9998, 0 open edges, 56% of the grid evaluated; bunny > 50k triangles (≈274k at full res in ~4 s). **أرقام / params:** cells 96–136; block 4.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:183` · `100-superskills/skills/kosif-montage-motion/tests/test_shape_kit.py:21` · `kosif-studio/motion/kit/shape-kit.js:183`

## الكاميرا والحركة في 3D — 3D camera & motion recipes

_مسار واحد لكل لقطة، وكل شيء دالة للزمن._

#### 3D-43 · حركات الكاميرا على مسار · Spline camera moves & narrated fly-throughs · 🟢 جاهز / ready
- **ماذا / what:** كاميرا على مسار Catmull-Rom بحركة واحدة لكل لقطة، مدار هادئ، أو تحليق تتزامن نقاطه مع كلمات التعليق. — Catmull-Rom camera paths, one move per shot, gentle orbits, narration-locked fly-throughs.
- **متى أستخدمها / when:** كل لقطة 3D — every 3D shot.
- **كيف / how:** python3 tools/kosif.py scaffold cinematic-3d <dir>; CatmullRom paths 2–5 s ease-in-out sine; orbit 10–25°/s; fov 40–55; three camera keys per template shot (scene3d: fov 38, sun elevation 6 → 26°, azimuth 165 → 115°, exposure .46 → .58); narration-locked: waypoint times from words.json (e.g. 4 waypoints in 6 s); chaptered scale tour: tween position/target 2.5 s easeInOutCubic between chapter waypoints; reusable 3D set as an explainer stage with 6–12 s eased dolly/orbit per chapter (fov 35–50°); lines on the ground as thin quads 2 mm above the mesh so they follow perspective and get occluded. **أرقام / params:** 2–5 s paths; orbit 10–25°/s.
- **الدليل / proof:** `kosif-tool/styles/cinematic-3d/SKILL.md` · `kosif-tool/playbooks/3d.md:48` · `kosif-studio/motion/templates/scene3d/src/main.js` · `kosif-tool/styles/pm-blueoctopusai-dd17bd`

#### 3D-44 · المنصة الدوارة للمنتج · Product turntable recipe · 📄 موصوف / documented only
- **ماذا / what:** المنتج يسقط على قاعدة، يدور 90° مع اقتراب، تُرسم تسمية، ثم ثبات بطل. — Product drops on a plinth, orbits 90° with push-in, callout draws, hero hold.
- **متى أستخدمها / when:** إعلانات منتجات — product ads.
- **كيف / how:** 0–0.6 s drop (ease-in quad + spring damping 12); 0.6–4.6 s orbit 90° (sine in-out) with push-in; 2.0–2.4 s callout draws (ease-out cubic, EXPL-29); 4.6–6.0 s hero hold; for a full 360° loop use HyperFrames product-turntable (3D-13) or K3.shot('turntable') holds (CHAR-45). **أرقام / params:** 0.6 / 4.6 / 6.0 s.
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:35`

#### 3D-45 · المنظر المفكك · Exploded view · 📄 موصوف / documented only
- **ماذا / what:** أجزاء المنتج تبتعد على محاور منطقية مع تسميات قصيرة ثم تعود — دون اختراع أجزاء داخلية. — Parts move apart along sensible axes with short labels, then reassemble — never inventing internals.
- **متى أستخدمها / when:** «ما بداخل المنتج» — 'what's inside'.
- **كيف / how:** MG-031: 0–1 s product, 1–3 s explode, 3–5 s labels, 5–7 s reassemble; offset child meshes along their normals or Y with a 150 ms stagger; independent PNG layers in an HTML stack when no model exists; HyperFrames exploded-stack for isometric layer plates; K3.schematic explode (EXPL-52) for characters. **أرقام / params:** 7 s; stagger 150 ms.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-product-ads.md` · `kosif-tool/styles/pm-mdaman010-e7226a` · `kosif-tool/styles/pm-sayan-shanky-f850d8`

#### 3D-46 · سيارة مفككة بالتوليد · Generated car exploded-view pipeline · 🔑 مفتاح أو خدمة / needs key
- **ماذا / what:** من صورة السيارة إلى منظر مفكك صورةً لصورة، ثم فيديو 8 ث: انجراف بدخان، توقف، تفكك موجّه، وإعادة تركيب. — Car photo → image-to-image exploded view → 8 s drift / explode / reassemble clip.
- **متى أستخدمها / when:** إعلانات سيارات وتريندات «التفكيك» — car ads and exploded-view trends.
- **كيف / how:** fastify car-exploded profile: 47 makers in 5 groups / 154 models drive the BRAND → MODEL → DETAILS menus (profile tests passed here); prompt 2 separates hood, panels, wheels, tyres, interior, seats, chassis and drivetrain on a dark-grey gradient using image 1 as the mandatory base (keep uncertain internals generic); prompt 3 uses IMAGE 1 (assembled) + IMAGE 2 (exploded) as anchors: 0–2 s drift in with tyre smoke, 2–3 s hold with a gentle 3/4 orbit, 3–5.5 s servo-guided separation, 5.5–8 s exact reverse reassembly. Same family of locked settings: storybook park world (late golden hour, round trees, cobblestone path). Needs an image-to-image and a video generator key. **أرقام / params:** 0–2 / 2–3 / 3–5.5 / 5.5–8 s.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/car-exploded.mjs` · `fastify-motion-bro/tests/production-profiles.test.mjs` · `fastify-motion-bro/scripts/profiles/character-romance.mjs`

#### 3D-47 · المقاطع العرضية ومشاهد التضاريس العلمية · Cutaways & honest terrain science scenes · 📄 موصوف / documented only
- **ماذا / what:** مستويات قطع متحركة تكشف الداخل، وتضاريس بلوح ماء عند مستوى البحر، مع مسطرة مقياس وتصريح بالتضخيم الرأسي. — Animated clipping planes and terrain with a sea-level sheet, scale bars and stated vertical exaggeration.
- **متى أستخدمها / when:** زلازل، مياه جوفية، سدود، تشريح أجهزة — earthquakes, aquifers, dams, device anatomy.
- **كيف / how:** Three.js renderer.localClippingEnabled + material.clippingPlanes animated between named states (1 s reveal), colour-code internals; name what is measured vs schematic; correct terms (epicentre at the surface, hypocentre underground); scale/depth axes; water as a sea-level sheet over submerged terrain; compute cut faces from object bounds; capture 2+ rotation angles for QA. **أرقام / params:** 1 s reveal.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/cutaway-terrain-and-domain-scenes.md` · `kosif-tool/styles/pm-konstantinsaifo-96fc89`

#### 3D-48 · عنصر واحد يحمل القصة · Persistent subject across chapters · 📄 موصوف / documented only
- **ماذا / what:** مجسم واحد يحمل السرد كله: مجمّع، مفكك، آلية داخلية، ثم يعاد تجميعه — بخط زمني طبيعي 0–1. — One object carries the whole narrative across chapters.
- **متى أستخدمها / when:** شرح منتج طويل — long product explainers.
- **كيف / how:** one persistent scene; lathe geometry + instanced detail; a normalised 0–1 timeline drives the poses (map it to frame time for video); a white-model look (white MeshStandard, soft light, colour only on flows) keeps attention on the mechanism.
- **الدليل / proof:** `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/examples/cinematic/README.md` · `kosif-tool/styles/pm-mdaman010-e7226a`

#### 3D-49 · النص داخل المشهد ثلاثي الأبعاد · Type in 3D space · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نص ملفوف على كرة دوّارة، كلمة مبثوقة، ممر من كلمات عملاقة، أو مكعب كلمات — والعربية دائمًا على خامة مرسومة لا هندسة مبثوقة. — Text on a spinning sphere, extruded words, word corridors — Arabic always on a drawn texture.
- **متى أستخدمها / when:** عناوين مذهلة ثلاثية الأبعاد — spectacular 3D titles.
- **كيف / how:** paragraph drawn to a canvas texture (Arabic: ctx.direction='rtl', whole shaped line, ARAB-10) mapped on a sphere (30% H, 15°/s) over an emissive fire-noise shader with a fresnel rim #ff9a2a; Latin TextGeometry depth .3 em (cream face, orange sides) rotating from −30° Y over 900 ms easeOutCubic, or stacked offset layers; corridor: text planes along z with a dolly; never extrude Arabic from an unshaped font. **أرقام / params:** sphere 30% H; 15°/s.
- **الدليل / proof:** `kosif-tool/styles/pm-ajith-io-4c248f` · `kosif-tool/styles/pm-sahildesigner23-ee3155` · `kosif-tool/styles/pm-itisrazak-3ad902/BRIEF.md`

#### 3D-50 · أزرار وأجهزة ثلاثية الأبعاد · 3D product interactions (button, lid) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** لقطة منخفضة لصندوق زر أركيد بإضاءة حافة حمراء/زرقاء يضغطه مؤشر فينخفض بوميض، وغطاء حاسوب يُغلق 110°←0°. — A low-angle arcade button pressed with a flash, and a laptop lid closing 110° → 0°.
- **متى أستخدمها / when:** إعلانات تقنية وألعاب — tech and game ads.
- **كيف / how:** button press 150 ms with complementary rim lights and an emissive flash; hinge-rotate the lid 110° → 0° in ~1 s ease-in-out while the screen dims; hidden-object beat: hint (tail flick 2–4 s, glint 120 ms) then pop 0.8 → 1 with cubic-bezier(.34,1.56,.64,1) in 350 ms and a 3-stroke sparkle. **أرقام / params:** press 150 ms; lid ~1 s.
- **الدليل / proof:** `kosif-tool/styles/pm-spearwtf-3c1fd1` · `kosif-tool/styles/pm-cansincengiz-me-cf68dd` · `kosif-tool/styles/pm-mandelduck-95fd08/BRIEF.md`

#### 3D-51 · الأرض يرسمها الصوت · Music-driven 3D land · 🟢 جاهز / ready
- **ماذا / what:** كل قيمة من تحليل الموسيقى: الطيف يصير وادٍ، الجهير نهر حمم، الركلات ترمي شرارات وتضغط كرة كروم، وعند توقف الشريط يتجمد العالم والكاميرا تنجرف. — Every value from the score: spectrogram canyon, bass lava river, kick sparks, tape-stop bullet time.
- **متى أستخدمها / when:** كليبات موسيقية تجريبية — experimental music visuals.
- **كيف / how:** three-kit makeSpectrumGround + spectrumOnTape + makeSparks + makeGlitchPass fed by channels.json and spectrum_height.png (motion.py channels TRACK.wav); 8 tape-seconds across 120 m; fog #1A0A16 .018; fov 36; silence flips the picture negative; spin-up whips the camera home. **أرقام / params:** 8 tape-s over 120 m.
- **الدليل / proof:** `kosif-studio/motion/projects/sound_ground/src/main.js:1`

#### 3D-52 · أفكار ثلاثية الأبعاد غير منفذة · Unbuilt 3D ideas · 💡 فكرة / idea
- **ماذا / what:** كاميرا مشي بمنظور الشخص الأول داخل لوحة، مجرة نقاط المعاني، مشهد «مجرة المراجعة»، وسرد ثلاثي بالتمرير — أفكار بلا كود جاهز. — First-person walks, embedding galaxies, an audit galaxy and scroll-driven 3D — no ready code.
- **متى أستخدمها / when:** حين يطلب المستخدم شيئًا جديدًا من هذا النوع — when a user asks for one of these.
- **كيف / how:** first-person walk: 1.4 m/s, head bob 2 cm at 1.8 Hz, FOV 70°, no cuts, low-poly scene in a painting's palette; embedding galaxy: UMAP/t-SNE computed offline, WebGL points, fly between labelled clusters, state that distances are approximate; audit galaxy: central 'financial core' sphere + orbital risk network + evidence nodes (config object only); scroll-world: pre-rendered camera dives scrubbed by scroll (vendor skill; needs AI clips) — for video, drive the same timeline by t; kosif-tool styles scroll-world and lowpoly-3d (flatShading, roughness .6–.9, drop-in 0.4 s + spring 12) scaffold the look. **أرقام / params:** 1.4 m/s; bob 2 cm @1.8 Hz.
- **الدليل / proof:** `kosif-tool/styles/pm-mandelduck-95fd08/BRIEF.md` · `kosif-audit-studio/cinema/threeAuditScene.js` · `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md` · `kosif-tool/styles/lowpoly-3d/SKILL.md`

## توليفات قوية / power combos

- **رحلة طبيعة سينمائية / cinematic nature flight:** 3D-25 + 3D-26 + 3D-27 + 3D-28 + 3D-29 + 3D-43 + GLOW + ARAB-10 — جبال وغابة وبحر وسحب، شمس تشرق مع القصة، كاميرا على مسار، وعنوان عربي على خامة.
- **إعلان منتج فاخر / premium product:** 3D-39 + 3D-37 + 3D-38 + 3D-44 + EXPL-29 + TYPE — قرص كريمي، زجاج أو كروم، بلوم بعتبة 0.9، دوران 90° وتسمية تُرسم.
- **تميمة ثلاثية الأبعاد / 3D mascot:** 3D-42 + CHAR-40 + CHAR-36 + 3D-36 — نحت SDF مختبر، تنفس ورمش، إضاءة 5:1.
- **مدينة عربية مستقبلية / future Arab city:** 3D-33 + 3D-27 + 3D-38 + 3D-43 + MUSIC — نوافذ مضاءة، حقول طاقة، عمارة متوهجة، وكاميرا بين ست لقطات.
- **شرح أيزومتري / isometric explainer:** 3D-05 + 3D-06 + EXPL-26 + CAM — عالم أيزومتري تبنيه موجة قطرية وكاميرا تنتقل بين مناطق مرقمة.
- **عمق من صورة واحدة / depth from one photo:** 3D-03 + 3D-02 + FOOT + GLOW — ثلاث طبقات من خريطة عمق، اقتراب بطيء، دون كشف بكسلات مفقودة.
- **بصريات موسيقية / music visuals:** 3D-51 + 3D-06 + BEAT + PART — وادٍ من الطيف وأعمدة تتموج مع الركلات.
- **قلب بطاقات على الإيقاع / beat card flips:** 3D-08 + 3D-07 + BEAT + TRANS — بطاقات تنقلب على الضربة القوية فوق جدار مائل ينجرف.

## أخطاء ممنوعة / never do

1. **لا 3D حقيقي حين يكفي 2.5D** — يكلف رندرًا بطيئًا (SwiftShader) دون مكسب؛ اسأل: هل تتحرك الكاميرا حول الشيء؟ (3D-01).
2. **لا تبثق العربية كهندسة من خط غير مشكّل** — الحروف تتفكك وتنعكس؛ CanvasTexture أو طبقة HTML (3D-49، ARAB-10).
3. **لا THREE.Clock ولا useFrame ولا شيدر يحرك نفسه** — الإطارات لا تتطابق؛ مرر t كمتغير (3D-15/16).
4. **لا تعلن الجاهزية قبل أول إطار حقيقي وتسخين المظللات** — أول إطارات الفيديو تخرج سوداء أو ناقصة (3D-15).
5. **لا تكبير طبقة صورة حتى تنكشف الفراغات** — ابق داخل حدود القص أو املأ الفراغ (3D-03).
6. **لا تخترع أجزاء داخلية لمنتج حقيقي في المنظر المفكك** — اتركها عامة أو اسأل (3D-45/46).
7. **لا تضخيم رأسي بلا تصريح في مشاهد التضاريس العلمية** — اكتب المقياس والتضخيم (3D-47).
8. **لا بلوم بعتبة منخفضة على مشهد منتج أو شخصية لطيفة** — يغسل الألوان؛ عتبة ≥ 0.9 والانبعاث فقط يتوهج (3D-38).
9. **لا نماذج GLB أو HDRI مجهولة الرخصة** — رخّص كل نموذج، والإضاءة البيئية من تدرج تكفي غالبًا (3D-22/27).
10. **لا تعتمد على esbuild لإعادة حزم المكتبة هنا** — غير مثبت؛ استخدم three-kit.bundle.js الجاهز (3D-14).

## أقوى 5 حركات توقيع / 5 signature moves

1. **3D-25 + 3D-27 — جبال وسماء تتبع القصة:** تضاريس ملتوية بنهر محفور تحت شمس تشرق من 6° إلى 26°.
2. **3D-42 — نحت SDF:** أي تميمة لطيفة كشبكة مغلقة مختبرة هنا.
3. **3D-02 — منصة العمق 2.5D:** أرخص عمق مقنع: أربع طبقات، دوران ≤6°، مدار 8° في 2–3 ث.
4. **3D-05 — العالم الأيزومتري:** دالة إسقاط واحدة وموجة بناء قطرية بـ 40 ملّي ثانية لكل بلاطة.
5. **3D-37 + 3D-38 — زجاج وبلوم:** زجاج فيزيائي يكسر العنوان خلفه وبلوم بعتبة عالية — لقطة البطل الفاخرة.

## من أكبر مستودعات GitHub — from the top GitHub repositories (2026-10-23)

_قدرات من أشهر مستودعات GitHub ذات الترخيص المفتوح (MIT)، مكتوبة بكلماتنا لا منسوخة، وسجل كل مستودع في [github-top-1000.md](../github-top-1000.md). 🟢 = الكود هنا في `scripts/motion_physics.py` واختباره `evals/test_motion_physics.py`. — Powers from the most-starred open-licence (MIT) GitHub repositories, restated in our own words; per-repo record in github-top-1000.md; 🟢 = code here in scripts/motion_physics.py with its test._

#### 3D-G01 · حلقة رندر three.js حتمية · Deterministic three.js render loop · 📄 موصوف / documented only
- **ماذا / what:** حرّك المشهد بالزمن لا بعدد الإطارات، واضبط الألوان والدقة مرة واحدة، وفي التصدير اجعل الزمن مدخلًا تبحث إليه لا ساعة حقيقية. — Drive the scene by time, not frame count, set colour and resolution once, and for export make time an input you seek to, not the wall clock.
- **متى أستخدمها / when:** مشهد ثلاثي الأبعاد للويب أو لفيديو / a 3D scene for the web or for a video
- **كيف / how:** update(t) sets every transform from t; live: t from a clock delta; export: t = frame / fps (no requestAnimationFrame timing). renderer.setPixelRatio(min(devicePixelRatio, 2)), sRGB output colour space, ACES filmic tone mapping with exposure ≈1; damped orbit controls need update() every frame; dispose geometries, materials and textures when a shot ends. Render frames headless and verify duration and fps (tools/verify_video.py). **أرقام / params:** pixel ratio ≤ 2; export t = frame/fps.
- **الرخصة / license:** MIT
- **المصدر / source:** https://github.com/mrdoob/three.js (MIT) — restated in our own words
