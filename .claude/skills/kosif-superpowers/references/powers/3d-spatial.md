# الأبعاد الثلاثية — 3D & spatial

> فصل مُجمَّع آليًا من 236 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **230 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 230 powers deduplicated by name from 236 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 11 · 🟢 جاهز 12 · 📦 بأمر تثبيت 87 · 🔑 مفتاح/خدمة 5 · 👁 شوهد في فيديو 96 · 📄 موصوف 12 · 💡 فكرة 7

#### 3D-01 · غابة صنوبر · Instanced conifer forest · ✅ مُثبت هنا
- **ماذا / what:** Thousands of instanced two-tier conifers with jagged tier rims, clumping and per-tree colour.
- **كيف / how:** K3.makeForest({height, region:[x0,x1,z0,z1], accept(x,z,h), max, scale, hue, tiers, thinFrom, thinTo, seed}); K3.coniferCrown(tiers, seed).
- **أرقام / params:** max 22000; tiers 4 + spire; hue .25; trunk #4a3524; thinning 300-430 m
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:150` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:174` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:150` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:174`

#### 3D-02 · توليد الشبكة · Surface-nets mesher (coarse-to-fine) · ✅ مُثبت هنا
- **ماذا / what:** Turns the SDF into a watertight BufferGeometry with projected vertices, field normals and vertex colours, evaluating only near the surface.
- **كيف / how:** S.mesh({cells, project, slack}) -> geometry; geometry.userData.stats {grid, evals, vertices, triangles, ms}.
- **أرقام / params:** cells 96 default (bunny 132); block 4; 2 Newton projection steps; tested sphere volume ratio .9996, area .9998, 0 open edges, 56% of grid evaluated
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:183` · `100-superskills/skills/kosif-montage-motion/tests/test_shape_kit.py:21` · `kosif-studio/motion/kit/shape-kit.js:183` · `kosif-studio/motion/references/shape-kit.md`

#### 3D-03 · عالم البلورات - شظايا WebGL إجرائية · Crystal World - raw WebGL procedural shards · ✅ مُثبت هنا
- **ماذا / what:** An original, library-free WebGL1 scene of low-poly ice/amber crystal shards that drift, spin and bob in fog behind UI; deterministic per seed so it looks the same each visit.
- **كيف / how:** SQCCrystal.mount(canvas,{density,interactive,scroll,still,seed,palette}) -> {setMood,pulse,destroy,frames,shards}. Shard = irregular hexagonal prism (6 sides, irregularity .45) with pointed caps, flat per-face normals; N = round((phone?14:30)*(cores<=4||mem<=4?0.7:1)*density), min 6; placed in slab z -4..-18; spin w ~(+-.12,+-.17,+-.1) rad/s; bob sin(t*.5+phase)*(.15..5); perspective fov .95 rad near .1 far 60; LCG rng seed 20261005.
- **أرقام / params:** 24 triangles / 72 vertices per shard; radius .35-.85; length 1.2-3.4; scale .6-1.5; ~18 KB; version 1.1.0
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/crystal-world.js` · `kosif-earth-ci-fork/tools/crystal_world.test.mjs` · `kosif-earth-ci-fork/docs/rebuild/COMPANY_FIRST_REBUILD_ar.md:37`

#### 3D-04 · قفل عالم الحديقة الحالمة · Storybook park world lock · ✅ مُثبت هنا
- **ماذا / what:** Original fairytale urban park at late golden hour: pastel sky, soft bounce light, round trees, cobblestone path, uncluttered storybook 3D.
- **كيف / how:** setting constant repeated in every prompt.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/character-romance.mjs:5`

#### 3D-05 · كتالوج السيارات · Car brand/model catalogue · ✅ مُثبت هنا
- **ماذا / what:** 47 makers in 5 groups (mass-market 15, luxury 10, performance/exotic 9, electric 7, off-road/SUV 6) with 154 notable models.
- **كيف / how:** BRANDS / MODELS constants drive the BRAND -> MODEL -> DETAILS menus.
- **أرقام / params:** 47 brands; 154 models
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/car-exploded.mjs:3-35` · `fastify-motion-bro/tests/production-profiles.test.mjs:33-40`

#### 3D-06 · منظر مفكك من صورة لصورة · Exploded-view image-to-image · ✅ مُثبت هنا
- **ماذا / what:** Prompt 2: using image 1 as mandatory base, separate hood, panels, wheels, tyres, interior, seats, chassis and drivetrain along sensible axes on a dark-grey gradient, no callouts.
- **كيف / how:** Image-to-image with identity preservation; keep uncertain internals generic.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/car-exploded.mjs:57`

#### 3D-07 · فيديو انجراف وتفكيك وإعادة تركيب · Drift-explode-reassemble video · ✅ مُثبت هنا
- **ماذا / what:** Prompt 3: dual-reference 8 s clip: 0–2 s drift in with tyre smoke and stop; 2–3 s hold with gentle 3/4 orbit; 3–5.5 s servo-guided separation into the exploded pose; 5.5–8 s exact reverse reassembly with lock-in.
- **كيف / how:** Uses IMAGE 1 (assembled) and IMAGE 2 (exploded) as identity/geometry anchors.
- **أرقام / params:** 0–2 / 2–3 / 3–5.5 / 5.5–8 s
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/car-exploded.mjs:58`

#### 3D-08 · تضاريس · Heightfield terrain with detail maps · ✅ مُثبت هنا
- **ماذا / what:** Plane displaced by any height(x,z) function, vertex-coloured by a colour function, with tiled albedo + normal detail.
- **كيف / how:** K3.makeTerrain({height, colour, seg, size, texSize, albedoRepeat, normalRepeat, normalScale, roughness}); helper slopeOf(height,x,z).
- **أرقام / params:** seg 560; size 4600 m; tex 1024; albedo repeat 60; normal repeat 90; normalScale .55; roughness .95
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:112` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:146`

#### 3D-09 · نحت بدوال المسافة · SDF sculpting primitives · ✅ مُثبت هنا
- **ماذا / what:** Build soft organic shapes from signed-distance primitives in metres, each with optional rotation and colour.
- **كيف / how:** Load three-kit.bundle.js then shape-kit.js; const S=K3S.sculpt().sphere(c,r).ellipsoid(c,[rx,ry,rz],{rot}).capsule(a,b,r1,r2).box(c,[hx,hy,hz],round).torus(c,R,r); S.mesh({cells}).
- **أرقام / params:** primitives: sphere, ellipsoid (IQ bound), capsule = round cone (IQ sdRoundCone), rounded box, torus (xz ring)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:18` · `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:44` · `100-superskills/skills/kosif-montage-motion/tests/test_shape_kit.py`

#### 3D-10 · قالب مختبر كوسف · Template: KOSIF LAB 01 (rabbit x lion) · ✅ مُثبت هنا
- **ماذا / what:** 20 s product-lab 3D film: plush rabbit and lion on a cream sweep, wireframe-to-plush formation, lens walks the circle through SHAPE/JOINT/LOAD/BREAK/SWAP/RANK with HUD callouts, ear flop, tail swap, dip to ink.
- **كيف / how:** python motion.py new NAME --lab --seconds 20 --size WxH --title T; edit src/main.js; render via motion.py render.
- **أرقام / params:** tone neutral exposure 1.0; camera fov 26-32; 7 orbit stops (0,3,6.5,9.5,13,16,18 s); callouts ear/eye/mane/tail; rendered OK in headless Chromium/SwiftShader (t=8 s)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/lab/index.html` · `100-superskills/skills/kosif-montage-motion/templates/lab/main.js` · `100-superskills/skills/kosif-montage-motion/scripts/motion.py:175`

#### 3D-11 · قالب مشهد ثلاثي: خليج وجبال · Template: scene3d (alpine bay at sunrise) · ✅ مُثبت هنا
- **ماذا / what:** Cinematic 3D landscape: ridged mountains behind a bay, forest, reflective sea, cloud slab, sunrise with god rays and lens flare, letterbox opening, Arabic title and end title.
- **كيف / how:** python motion.py new NAME --3d ...; without npm the import is rewritten to window.K3 and the pre-bundled kit is copied; with npm run motion.py bundle.
- **أرقام / params:** fog FogExp2 #c9d6e2 .00011; fov 38; sun elevation 6 -> 26 deg; exposure .46 -> .58; letterbox 70 px -> 0 over 2.2 s; rendered OK in headless Chromium (t=4 s)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/scene3d/index.html` · `100-superskills/skills/kosif-montage-motion/templates/scene3d/src/main.js` · `100-superskills/skills/kosif-montage-motion/scripts/motion.py:181`

#### 3D-12 · حلقات مدارية مائلة · Tilted orbit rings (pseudo-3D) · 🟢 جاهز
- **ماذا / what:** Two elliptical outline rings behind the hero dial: one tilted with rotateX/rotateZ, one squashed ellipse that reveals by rotating into place.
- **كيف / how:** ::before transform rotateX(18deg) rotateZ(-20deg) with ring shadows; ::after rotate(-35deg) scaleY(.46) via keyframe orbit-reveal from rotate(-10deg) scaleY(.25); atmosphere-in scale .86->1.
- **أرقام / params:** orbit-reveal 1.5s ease-studio; atmosphere-in 1.5s; rings 250px / 248x220px; border #d9f3c730 / #cec1e13d
- **الدليل / proof:** `kosif-audit-studio/studio.css:68` · `kosif-audit-studio/studio.css:121`

#### 3D-13 · رفع العقد ثلاثي الأبعاد عند المرور · CSS 3D hover lift for nodes · 🟢 جاهز
- **ماذا / what:** Galaxy nodes preserve 3D and pop toward the viewer on hover.
- **كيف / how:** transform-style: preserve-3d; hover transform translateZ(40px) scale(1.08); transition .35s ease.
- **أرقام / params:** translateZ 40px; scale 1.08; 350ms
- **الدليل / proof:** `kosif-audit-studio/cinema/cinemaTheme.css`

#### 3D-14 · بطاقة بطل عائمة بظلال · Floating 2.5D hero card with shadows · 🟢 جاهز
- **ماذا / what:** Rounded card carrying the hero icon flies in from lower right with rotation, then floats with depth breathing and lags a soft contact shadow.
- **كيف / how:** card .47w x .49w radius .06w in shape colour; drop shadow rgba(0,0,0,.18) blur 30*scale offsetY 15*scale; contact ellipse rgba(0,0,0,.12); start offset (+.32w,+.49h) and +.15 rad, float y sin*0.009h, depth scale 1±.023, wobble ±.018 rad, exit drop .13h.
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:54-62`

#### 3D-15 · قصب وعشب · Reeds / grass blades · 🟢 جاهز
- **ماذا / what:** Instanced tapered blades with wind sway.
- **كيف / how:** K3.makeBlades({n, region, accept, height, tall, width, amp, freq, hue}).
- **أرقام / params:** n 1500; tall .9 m; width .02; hue .24
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:746`

#### 3D-16 · تحميل نماذج GLB · GLB model loader with seekable animation · 🟢 جاهز
- **ماذا / what:** Loads ready-made or Blender GLBs and seeks their skeletal/object animation to absolute time.
- **كيف / how:** await K3.loadModel(url, {clip, offset, speed, caustics}); root.userData.set(t) -> mixer.setTime.
- **أرقام / params:** shadows on all meshes; clip by name or index
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:964`

#### 3D-17 · إسقاط على السطح · Surface ray hit / projection · 🟢 جاهز
- **ماذا / what:** Ray-marches to the sculpt surface to place eyes, buttons or mouth lines exactly on the face.
- **كيف / how:** S.hit(from, dir, maxDist) -> {point, normal}; S.project(p, steps).
- **أرقام / params:** 256 march steps; step 0.8*d; 8 Newton projection steps
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:160` · `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:166`

#### 3D-18 · استوديو كريمي · Cream studio sweep · 🟢 جاهز
- **ماذا / what:** Product-lab set: cream infinite sweep, contact shadow, faint grid and soft three-light rig.
- **كيف / how:** K3.studio(scene, {bg, grid}).
- **أرقام / params:** bg #f1efe8; shadow .22; grid 16 m/32 div #c9d8c2/#d9e4d4 at .35; key 2.6 white (3,6,4); fill #dfe8ff .9; rim 1.4; hemi .9 #ffffff/#cfd8c8
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:194`

#### 3D-19 · محرك عرض بمنحنى نغمات · Tone-mapped WebGL renderer (ACES / AgX / Neutral) · 🟢 جاهز
- **ماذا / what:** Deterministic Three.js renderer with shadows and a choice of tone curve: ACES punchy, AgX hue-stable highlights (fire/neon/sunsets), Khronos Neutral for products.
- **كيف / how:** makeRenderer(canvas, W, H, {tone:'aces'|'agx'|'neutral', exposure}) from three-kit (pre-bundled as window.K3 in three-kit.bundle.js).
- **أرقام / params:** pixelRatio 1, PCF shadows, preserveDrawingBuffer, exposure 0.6
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:76` · `kosif-one/tools/kosif-studio/motion/references/book-lessons.md`

#### 3D-20 · تضاريس إجرائية بألوان جبلية · Procedural terrain with alpine colouring · 🟢 جاهز
- **ماذا / what:** Height-function terrain (ridged FBM, domain warp) with vertex colours from height/slope and tiled detail maps.
- **كيف / how:** makeTerrain({height, colour, seg, size, detail}); alpineColour(h, slope, x, z, c); slopeOf(height,x,z).
- **أرقام / params:** seg 560, size 4600; palette snow #f4f7fb, rock #5d5a58/#7a6f66, grass #4e6e34/#6b8a3c, sand #b9a77a, deep #2f4a3a
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:112` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:135`

#### 3D-21 · بحر عاكس · Reflective sea · 🟢 جاهز
- **ماذا / what:** Three.js Water plane with FBM normal maps reflecting sky and sun.
- **كيف / how:** makeSea({size, res, normals}).
- **أرقام / params:** size 30000, texture 768
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:245`

#### 3D-22 · تحميل نموذج GLB متحرك · GLB model with animation sought to t · 🟢 جاهز
- **ماذا / what:** Loads a ready or Blender-made GLB and seeks its skeletal/object animation to absolute time (mixer.setTime).
- **كيف / how:** await loadModel(url) after motion.py bundle (GLB inlined as data URL).
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:964`

#### 3D-23 · خلفية استوديو وقرص قياس · Studio backdrop, measuring disc and lite post · 🟢 جاهز
- **ماذا / what:** Background sweep, a measuring stage disc with a scan sweep, and a fast bloom+grade post stack.
- **كيف / how:** K3S.studioBackdrop(), K3S.stageDisc(), K3S.makeLitePost(renderer, scene, camera, W, H).
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/shape-kit.js:336` · `kosif-one/tools/kosif-studio/motion/kit/shape-kit.js:343` · `kosif-one/tools/kosif-studio/motion/kit/shape-kit.js:365`

#### 3D-24 · ستايل العالم الأيزومتريك · Isometric world style · 📦 بأمر تثبيت
- **ماذا / what:** One coloured isometric world; the camera travels zone to zone with numbered cards and a stage bar, for journeys or systems.
- **كيف / how:** STY.isometric: 16:9, bright, 2.0 wps, Readex Pro; bg #EEF1FF/#F4F1FF ink #1E1B4B zones #E4F5DC/#EEF0F8/#F6EEDC/#E9E4FA/#E4F2F5, colours #6366F1/#F59E0B/#14B8A6/#E11D48/#EC4899/#3B82F6; lines 'Stage: ...'; sfx pop/swish/blip/shimmer.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:593` · `100-superskills/skills/trend-animation-styles/references/styles.md`

#### 3D-25 · ثلاثي الأبعاد في ريموشن · Remotion 3D with ThreeCanvas · 📦 بأمر تثبيت
- **ماذا / what:** React Three Fiber scenes rendered frame-exactly by driving all motion from the frame number.
- **كيف / how:** @remotion/three <ThreeCanvas width height> with ambient (0.4) + directional (0.8) lights; rotation = frame*0.02; useFrame() from R3F forbidden; shaders must not self-animate.
- **أرقام / params:** ambient 0.4; directional 0.8
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/3d.md`

#### 3D-26 · عنصر واحد يستمر عبر الفصول · Persistent subject across chapters (exploded product) · 📦 بأمر تثبيت
- **ماذا / what:** One 3D object carries the whole narrative across chapters: assembled, exploded, internal mechanism, reassembled, with native-scroll timeline; render loop sleeps when pose settles.
- **كيف / how:** Three.js persistent scene, lathe geometry, instanced detail, normalized 0-1 timeline driving poses; for video map timeline to frame time.
- **أرقام / params:** chapter rail + motion toggle; checked at 1280x720 and 390x844
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/examples/cinematic/README.md`

#### 3D-27 · بوابات ومشهد داخل مشهد · Portal / render-to-texture scenes · 📦 بأمر تثبيت
- **ماذا / what:** Render an offscreen scene into a texture on a plane, with parallax by copying main camera matrix.
- **كيف / how:** R3F createPortal + useFBO; gl_FragCoord.xy/res screen-space sampling.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### 3D-28 · من بلندر إلى GLB · Blender to GLB pipeline · 📦 بأمر تثبيت
- **ماذا / what:** Model in Blender, export glTF 2.0/GLB, optimize with glTF Transform, load in Three.js.
- **كيف / how:** glTF Transform prune/dedup/simplify; Meshopt or Draco geometry; KTX2/BasisU textures; apply transforms, consistent units/pivots; colour maps sRGB, normal/roughness non-color.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2696-game-studio/10370-web-3d-asset-pipeline/SKILL.md` · `kosif-atlas/skills/1526-gamegen/4161-blender-game-assets/SKILL.md`

#### 3D-29 · مقاطع عرضية وتضاريس · Cutaway / terrain scenes · 📦 بأمر تثبيت
- **ماذا / what:** Clip objects with animated cut planes; terrain with sea-level sheet and shoreline contours; label vertical exaggeration.
- **كيف / how:** Three.js clippingPlanes animated between named states; scale bars.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/cutaway-terrain-and-domain-scenes.md`

#### 3D-30 · مشاهد المقاطع والتضاريس العلمية · Cutaway and terrain science scenes · 📦 بأمر تثبيت
- **ماذا / what:** Rules for honest mechanism scenes (earthquakes, aquifers, dams): scale bars, stated vertical exaggeration, sea-level water sheets.
- **كيف / how:** Name what is measured vs schematic; use correct terms (epicenter at surface, hypocenter underground); show scale/depth axes and exaggeration; water as a sea-level sheet over submerged terrain; compute cut faces from object bounds; capture 2+ rotation angles for QA.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/cutaway-terrain-and-domain-scenes.md`

#### 3D-31 · مجرة النقاط المضمنة · Embedding / point-cloud galaxy · 📦 بأمر تثبيت
- **ماذا / what:** Thousands of items projected to 2D/3D (UMAP/t-SNE) shown as a glowing point cloud that clusters by meaning.
- **كيف / how:** Compute embeddings and a 2D projection offline, render as WebGL points (Three.js or regl-scatterplot), fly the camera between labelled clusters; state that distances are approximate.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/3385-fiftyone/13898-fiftyone-embeddings-visualization/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/webgl-2d-animation-patterns.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10322-data-visualization/references/default-stack-selection.md`

#### 3D-32 · ستايل ثلاثي الأبعاد المزيف · Fake 3D golden object style · 📦 بأمر تثبيت
- **ماذا / what:** A flat golden object with real thickness turns in one continuous shot and ends on a poster.
- **كيف / how:** STY.fake3d: 16:9, calm, 1.9 wps, Alexandria; ink #2A1441 gold #FFF1BC/#F5B54A/#B4641A wall #EFE7DA; +2.4 s poster tail; sfx shimmer/swish/swell.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:655`

#### 3D-33 · سرد ثلاثي الأبعاد بالتمرير · Scroll-linked 3D storytelling (idea) · 📦 بأمر تثبيت
- **ماذا / what:** Scroll-scrubbed 3D storyboarding direction from oso95/scroll-world (MIT); not installed.
- **كيف / how:** Would require Three.js/WebGL implementation.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `fastify-motion-bro/docs/ENGINE_ROUTER.md:7` · `fastify-motion-bro/docs/SOURCE_AUDIT.md:5` · `fastify-motion-bro/docs/ROADMAP.md:6`

#### 3D-34 · DOM كخامة WebGL · HTML-in-canvas textures · 📦 بأمر تثبيت
- **ماذا / what:** Live DOM rendered into canvas as WebGL texture.
- **كيف / how:** Blocks tagged html-in-canvas; browser support limited.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/html-in-canvas.mdx`

#### 3D-35 · رصّة بطاقات بعمق · Camera Rig Depth Stack · 📦 بأمر تثبيت
- **ماذا / what:** 3D stack of cards with depth spacing, parallax and a focus shift like a camera rig.
- **كيف / how:** Install with `npx hyperframes add camera-rig-depth-stack` (copies to compositions/components/camera-rig-depth-stack.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (he…
- **تثبيت / install:** `npx hyperframes add camera-rig-depth-stack` (copies to compositions/components/camera-rig-depth-stack`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/camera-rig-depth-stack/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/camera-rig-depth-stack/camera-rig-depth-stack.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/camera-rig-depth-stack.mdx`

#### 3D-36 · شريط منظوري · Perspective Marquee · 📦 بأمر تثبيت
- **ماذا / what:** 3D-tilted marquee whose words roll toward a horizon.
- **كيف / how:** Install with `npx hyperframes add perspective-marquee` (copies to compositions/components/perspective-marquee.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless…
- **أرقام / params:** tilt flat|standard|steep; vars: tilt=standard[flat|standard|steep]; travel=standard[short|standard|long]; tone=ink[ink|paper|accent]; words=COMPONENTS, PRIMITIVES, TRANSITIONS, AGENTS
- **تثبيت / install:** `npx hyperframes add perspective-marquee` (copies to compositions/components/perspective-marquee`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/perspective-marquee/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/perspective-marquee/perspective-marquee.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/perspective-marquee.mdx`

#### 3D-37 · بطاقتان كالكتاب · Split Tilt Cards · 📦 بأمر تثبيت
- **ماذا / what:** Two cards arrive from opposite wings with mirrored rotateY book-open tilts under one perspective, badges spring-pop on inner edges, phase-opposed idle float.
- **كيف / how:** Install with `npx hyperframes add split-tilt-cards` (copies to compositions/components/split-tilt-cards.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chrom…
- **أرقام / params:** badge_a v1; badge_b v2; vars: label_a=Before; label_b=After; badge_a=v1; badge_b=v2; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add split-tilt-cards` (copies to compositions/components/split-tilt-cards`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/split-tilt-cards/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/split-tilt-cards/split-tilt-cards.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/split-tilt-cards.mdx`

#### 3D-38 · بطاقات تدور ثلاثية الأبعاد · Three Orbiting Cards · 📦 بأمر تثبيت
- **ماذا / what:** Three.js scene of cards orbiting, driven by a paused GSAP timeline for deterministic renders.
- **كيف / how:** Install with `npx hyperframes add three-orbiting-cards` (copies to compositions/components/three-orbiting-cards.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headle…
- **تثبيت / install:** `npx hyperframes add three-orbiting-cards` (copies to compositions/components/three-orbiting-cards`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/three-orbiting-cards/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/three-orbiting-cards/three-orbiting-cards.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/three-orbiting-cards.mdx`

#### 3D-39 · بطاقة مائلة · Tilt Card · 📦 بأمر تثبيت
- **ماذا / what:** Card with depth layers and hover-style parallax tilt.
- **كيف / how:** Install with `npx hyperframes add tilt-card` (copies to compositions/components/tilt-card.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame capt…
- **أرقام / params:** glow tight|standard|wide; accent indigo|emerald|violet; vars: eyebrow=Primitive; headline=Agent-ready motion; glow=standard[tight|standard|wide]; accent=indigo[indigo|emerald|violet]
- **تثبيت / install:** `npx hyperframes add tilt-card` (copies to compositions/components/tilt-card`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/tilt-card/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/tilt-card/tilt-card.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/tilt-card.mdx`

#### 3D-40 · عنوان بين الأوراق · Canopy Part Title · 📦 بأمر تثبيت
- **ماذا / what:** 3D leaves sweep through and part to reveal the headline (Three.js 0.170 from CDN, Gelasio font).
- **كيف / how:** Install with `npx hyperframes add canopy-part-title` (copies the full composition to compositions/canopy-part-title.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.170.0 (CDN), Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 12 s; leaf textures origin unconfirmed; Google Fonts: Gelasio; 1920x1080; duration 12 s
- **تثبيت / install:** `npx hyperframes add canopy-part-title` (copies the full composition to compositions/canopy-part-title`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/canopy-part-title/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/canopy-part-title/canopy-part-title.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/canopy-part-title.mdx`

#### 3D-41 · عنوان بلاطات متقلبة · Code Slice Hero · 📦 بأمر تثبيت
- **ماذا / what:** Tiled headline surface flips cell by cell under a sweeping depth field to reveal a rear headline.
- **كيف / how:** Install with `npx hyperframes add code-slice-hero` (copies the full composition to compositions/code-slice-hero.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Geist Bold (OFL) bundled; GSAP vendored; 1920x1080; duration 8 s
- **تثبيت / install:** `npx hyperframes add code-slice-hero` (copies the full composition to compositions/code-slice-hero`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/code-slice-hero/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/code-slice-hero/code-slice-hero.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/code-slice-hero.mdx`

#### 3D-42 · دوار المكعبات · Cuboid Carousel · 📦 بأمر تثبيت
- **ماذا / what:** Chain of bevelled PBR cuboids rides a travelling wave as a content carousel.
- **كيف / how:** Install with `npx hyperframes add cuboid-carousel` (copies the full composition to compositions/cuboid-carousel.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js (vendored/bundled), Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Three r185 + GSAP vendored; Inter via Google Fonts; 6.67 s; Google Fonts: Inter; 1920x1080; duration 6.67 s
- **تثبيت / install:** `npx hyperframes add cuboid-carousel` (copies the full composition to compositions/cuboid-carousel`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/cuboid-carousel/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/cuboid-carousel/cuboid-carousel.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/cuboid-carousel.mdx`

#### 3D-43 · المكدس المتفجر · Exploded Stack · 📦 بأمر تثبيت
- **ماذا / what:** Isometric layer plates explode apart with a label per layer, hold, then collapse (architecture/system diagrams).
- **كيف / how:** Install with `npx hyperframes add exploded-stack` (copies the full composition to compositions/exploded-stack.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.184.0 (CDN), Canvas 2D painter, inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Three.js; 5 s; 1920x1080; duration 5 s
- **تثبيت / install:** `npx hyperframes add exploded-stack` (copies the full composition to compositions/exploded-stack`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/exploded-stack/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/exploded-stack/exploded-stack.html`

#### 3D-44 · شعار الجليد المداري · Frost Sequence Camera Orbit · 📦 بأمر تثبيت
- **ماذا / what:** Orbiting camera follows an ice logo that erodes, reforms into two text moments and fades. [Local copy lacks 2 declared file(s), e.g. assets/shards-atlas.png.]
- **كيف / how:** Install with `npx hyperframes add frost-sequence-camera-orbit` (copies the full composition to compositions/frost-sequence-camera-orbit.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGPU Shaders library v4 (lib/shaders.iife.js, <canvas data-shader>), GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 22.5 s; Three r185, three-mesh-bvh 0.9.14, opentype.js, Clipper 6.4.2 (BSL-1.0); Geist; 1920x1080; duration 22.5 s
- **تثبيت / install:** `npx hyperframes add frost-sequence-camera-orbit` (copies the full composition to compositions/frost-sequence-camera-orbit`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/frost-sequence-camera-orbit/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/frost-sequence-camera-orbit/frost-sequence-camera-orbit.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/frost-sequence-camera-orbit.mdx`

#### 3D-45 · نفق المعرض · Gallery Tunnel · 📦 بأمر تثبيت
- **ماذا / what:** Infinite square tunnel tiled with saturated slabs and caller images that swell toward camera and pass, fogging at the far end.
- **كيف / how:** Install with `npx hyperframes add gallery-tunnel` (copies the full composition to compositions/gallery-tunnel.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.147.0 (CDN), GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** palette #FF6A00,#AB54F7,#EA3737,#0072E3,#00AA3C,#FFB200; speed 3; fog 14.25; grid 2; Three 0.147; vars: images=; imageMix=0.5(0..1); speed=3(0..8); palette=#FF6A00,#AB54F7,#EA3737,#0072E3,#00AA3C,#FFB200; grid=2(1..4); fill=0.5(0..1); fog=14.25(3..14.5); edgeColor=#B0B0B0; edgeOpacity=0.5(0..1); bac…
- **تثبيت / install:** `npx hyperframes add gallery-tunnel` (copies the full composition to compositions/gallery-tunnel`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/gallery-tunnel/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/gallery-tunnel/gallery-tunnel.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/gallery-tunnel.mdx`

#### 3D-46 · بطل زجاجي · Glass Hero · 📦 بأمر تثبيت
- **ماذا / what:** Solid glass object rises before a giant headline and keeps turning so the type refracts and disperses through it.
- **كيف / how:** Install with `npx hyperframes add glass-hero` (copies the full composition to compositions/glass-hero.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.184.0 (CDN), Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Three.js; 1920x1080; duration 5 s
- **تثبيت / install:** `npx hyperframes add glass-hero` (copies the full composition to compositions/glass-hero`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/glass-hero/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/glass-hero/glass-hero.html`

#### 3D-47 · عنوان الشظايا الزجاجية · Glass Shard Title · 📦 بأمر تثبيت
- **ماذا / what:** Glass Voronoi shards fly through fog and tile into the headline. [Local copy lacks 1 declared file(s), e.g. assets/matcap-1.png.]
- **كيف / how:** Install with `npx hyperframes add glass-shard-title` (copies the full composition to compositions/glass-shard-title.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** d3-delaunay 6.0.4, Ferndale Studio HDR (CC0), Cormorant Garamond; 12.16 s; 1920x1080; duration 12.16 s
- **تثبيت / install:** `npx hyperframes add glass-shard-title` (copies the full composition to compositions/glass-shard-title`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/glass-shard-title/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/glass-shard-title/glass-shard-title.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/glass-shard-title.mdx`

#### 3D-48 · بطاقة المدار · Orbit Card · 📦 بأمر تثبيت
- **ماذا / what:** Single feature card orbits a dot sphere on approved Blender camera motion.
- **كيف / how:** Install with `npx hyperframes add orbit-card` (copies the full composition to compositions/orbit-card.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Archivo (OFL); Three r185; 10 s; 1920x1080; duration 10 s
- **تثبيت / install:** `npx hyperframes add orbit-card` (copies the full composition to compositions/orbit-card`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/orbit-card/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/orbit-card/orbit-card.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/orbit-card.mdx`

#### 3D-49 · قرص المنتج الدوار · Product Turntable · 📦 بأمر تثبيت
- **ماذا / what:** A product spins one full turn on a studio plinth in a seamless loop; drop in a GLB/glTF or keep the built-in drink can with your own label.
- **كيف / how:** Install with `npx hyperframes add product-turntable` (copies the full composition to compositions/product-turntable.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.184.0 (CDN), Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Three.js; 6 s loop; 1920x1080; duration 6 s
- **تثبيت / install:** `npx hyperframes add product-turntable` (copies the full composition to compositions/product-turntable`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/product-turntable/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/product-turntable/product-turntable.html`

#### 3D-50 · عنوان البوابة السلكية · Wireframe Portal Title · 📦 بأمر تثبيت
- **ماذا / what:** Wireframe portal bursts open, title passes through, then letters swap into a second phrase.
- **كيف / how:** Install with `npx hyperframes add wireframe-portal-title` (copies the full composition to compositions/wireframe-portal-title.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.181.2 (CDN), WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Three 0.181.2 CDN + clipper-lib; Geist; 8 s; 1920x1080; duration 8 s
- **تثبيت / install:** `npx hyperframes add wireframe-portal-title` (copies the full composition to compositions/wireframe-portal-title`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/wireframe-portal-title/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/wireframe-portal-title/wireframe-portal-title.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/wireframe-portal-title.mdx`

#### 3D-51 · طيران كاميرا ثلاثي الأبعاد · 3D perspective camera flight · 📦 بأمر تثبيت
- **ماذا / what:** A perspective stage + preserve-3d world whose pose (translate3d + rotateX/Y) is tweened leg by leg from one camera state: dive into angled grid, tilt-to-flatten pull-back, fly past standing cards, decelerate into focus.
- **كيف / how:** Read hyperframes-animation/rules/3d-camera-flight.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** landings power4.out; repositions power2.inOut; DoF via --dof var on leaf elements
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/3d-camera-flight.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### 3D-52 · دخول بالدوران ثلاثي الأبعاد ثم مدار · Orbit 3D flip entry · 📦 بأمر تثبيت
- **ماذا / what:** Elements flip in from 3D (rotateX + rotateY + translateZ) at their orbital start position then settle into continuous elliptical orbit.
- **كيف / how:** Read hyperframes-animation/rules/orbit-3d-entry.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** perspective 1800 px; translateZ(220px) wins paint order; gsap.set orbit start BEFORE phase 1; entry back.out(FLIP_BACK)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/orbit-3d-entry.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### 3D-53 · تبعثر في العمق ثم تجمّع · Depth scatter / assemble · 📦 بأمر تثبيت
- **ماذا / what:** N elements scatter into or assemble from a rotating 3D depth cloud with index-derived offsets, settling to a flat layout; tumble-swap and radial-explode variants.
- **كيف / how:** Read hyperframes-animation/rules/depth-scatter-assemble.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** perspective 1400 px; cloud spin power1.out; index stagger
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/depth-scatter-assemble.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### 3D-54 · محول Three.js للمشاهد ثلاثية الأبعاد · Three.js adapter (3D scenes, AnimationMixer) · 📦 بأمر تثبيت
- **ماذا / what:** 3D scenes, GLTF models, camera cuts inside one canvas and AnimationMixer clips seeked by HyperFrames time via hf-seek.
- **كيف / how:** adapters/three.md: basic pattern, addon loading (GLTFLoader), heavy setup, mixer, camera cuts, lighting lit meshes.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/three.md`

#### 3D-55 · قاعدة العمق الحقيقي · Real 3D depth rule (scale alone is fake) · 📦 بأمر تثبيت
- **ماذا / what:** Depth needs a perspective parent, preserve-3d, z travel, rotation, camera/world motion, occlusion and layer order; prove with angled ghost diagnostics.
- **كيف / how:** `npx hyperframes keyframes . --shot <file> --ghost --angle <angle>`.
- **تثبيت / install:** `npx hyperframes keyframes`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/SKILL.md`

#### 3D-56 · حركة إيقاعية: 3d-card-flip · Beat motion primitive: 3d-card-flip · 📦 بأمر تثبيت
- **ماذا / what:** 3D card flip rotateY, anchored to music events (downbeat / swap).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/3d-card-flip/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: downbeat / swap; best span 0.8-1.6 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/3d-card-flip/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### 3D-57 · كوسف: عدّة الواقعية ثلاثية الأبعاد والإضاءة · KOSIF: Three.js realism kit and lighting rigs · 📦 بأمر تثبيت
- **ماذا / what:** three-kit.js: sky/sun/terrain/forest/sea/clouds/particles, shallow see-through water with caustics, lightRig {key, fillStops 2, rimStops 0.5, keyK 5600, fillK 6500, rimK 4300} (5:1 ratio), lightPreset rembrandt/clamshell/edgy/ultrasoft/short/broad/sun, aerial perspective fog = sky horizon color, sho…
- **كيف / how:** python3 scripts/motion.py new NAME --3d; examples koi_pond, water_cycle_3d, blue_hour, sound_ground.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/hyperframes-animation-studio/scripts/kit/three-kit.js` · `100-superskills/skills/hyperframes-animation-studio/SKILL.md` · `100-superskills/skills/hyperframes-animation-studio/scripts/examples/koi_pond/src/main.js`

#### 3D-58 · مشروع ثلاثي الأبعاد · New 3D project (three-kit) · 📦 بأمر تثبيت
- **ماذا / what:** Scaffold src/main.js on window.K3 bundle (no npm needed).
- **كيف / how:** python scripts/kmotion.py new NAME --3d --seconds 10; kmotion kit-bundle after kit edits (esbuild)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:85`

#### 3D-59 · السماء والتضاريس والغابة والبحر · Sky, terrain, forest, sea, clouds, flocks · 📦 بأمر تثبيت
- **ماذا / what:** Procedural world blocks: Preetham sky, ridged FBM terrain 560², InstancedMesh forest ~20k conifers, Water with normal map, raymarched cloud slab 36 steps.
- **كيف / how:** three-kit.js (window.K3) in a --3d project; render --engine studio
- **أرقام / params:** bloom 0.22/0.6/0.9; terrain tex repeat 60–90
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:106` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### 3D-60 · الكوي والبتلات والحصى · Koi, petals, pebbles, blades, sway · 📦 بأمر تثبيت
- **ماذا / what:** Living things: lofted koi with seeded kohaku/sanke/showa/ogon skins; petals that ring water; water-worn pebbles; reeds swaying bend∝height².
- **كيف / how:** three-kit.js (window.K3) in a --3d project; render --engine studio
- **أرقام / params:** makeKoi, makePetals, makePebbles, makeBlades, addSway
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:106` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### 3D-61 · تحميل نماذج GLB · GLB model load + cloth wave · 📦 بأمر تثبيت
- **ماذا / what:** Load GLB with animation sought to t; addWave for cloth/flags.
- **كيف / how:** three-kit.js (window.K3) in a --3d project; render --engine studio
- **أرقام / params:** loadModel(url), addWave
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:106` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### 3D-62 · نحت المجسمات بدوال المسافة · SDF sculpting shape kit · 📦 بأمر تثبيت
- **ماذا / what:** Sphere/ellipsoid/round-cone/box/torus with smooth union, carve, intersect, paint → watertight mesh via coarse-to-fine surface nets.
- **كيف / how:** shape-kit.js / lab-kit.js in a 3D project; read references/shape-kit.md
- **أرقام / params:** window.K3S; bunny 274,184 tris ≈4 s per page
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:101` · `100-superskills/skills/kosif-montage-motion/SKILL.md:113` · `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### 3D-63 · مظهر المختبر التخطيطي · Lab kit schematic look · 📦 بأمر تثبيت
- **ماذا / what:** Plush hero on cream sweep, orbiting lens with stops, dashed callouts and measurement cards, instrument HUD.
- **كيف / how:** shape-kit.js / lab-kit.js in a 3D project; read references/shape-kit.md
- **أرقام / params:** python scripts/kmotion.py new NAME --lab --seconds 20 --fps 24 --size 960x540
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:101` · `100-superskills/skills/kosif-montage-motion/SKILL.md:113` · `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### 3D-64 · ماء ضحل صافٍ بألوان السماء والضفة · Shallow clear water with sky and bank colours · 📦 بأمر تثبيت
- **ماذا / what:** Clear shallow pond water that shows the bed, reflects a gradient sky and a dark bank, ripples where petals land and receives dapples.
- **كيف / how:** makeShallowWater({width 2·RX+1, depth 2·RZ+1, seg 300, amp .006, clarity .72, deep 0x1c3a22, shallow 0x4d6a45, skyTop 0x8fb3d8, skyHorizon 0xe9c48e, bank 0x232d1a, bankHeight .14, ripples 28}); water.userData.set(t, sun, colour).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:58`

#### 3D-65 · بدن قارب ممدود بمعادلات · Parametric lofted boat hull · 📦 بأمر تثبيت
- **ماذا / what:** A felucca hull is generated from beam, sheer and keel curves along its length and a bilge-to-topside profile, plus transom, gunwales, floor, thwarts, mast, slanted yard with furled sail and rigging.
- **كيف / how:** beam(s)=1.12·sin(π(0.13+0.87s))^0.62; sheer(s)=0.78+0.62s^3.2+0.22(1−s)^5; keel(s)=−0.62·sin(π(0.04+0.96s))^0.45; x = side·b·(1−(1−φ)^2.4); grid 72×16 per side; L 7.2 m; yard rotated −1.02 rad, 8.6 m; sail = 9 tapered cylinders.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:14` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:39`

#### 3D-66 · تضاريس جبلية ملتوية بنهر محفور · Domain-warped mountain terrain with carved river · 📦 بأمر تثبيت
- **ماذا / what:** A mountain range behind a bay: warped ridged noise for eroded ridges, rolling hills, fine detail, land sinking under the sea toward camera, and a Gaussian river channel along a sine path.
- **كيف / how:** warp x,z by 180·fbm(0.0009); ridge 820·exp(−((z+1250)/820)²)·(0.55+0.45·ridged(0.0006)); hills 260·ridged(0.0011); detail 55·fbm(.004)+14·fbm(.02); river x = 140·sin(z/420)−220 carved 150·exp(−d²/(2·55²)); makeTerrain({height, colour: alpineColour}).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:7`

#### 3D-67 · خطوط جبال من ضوضاء متعرجة · Ridge silhouettes from ridged noise · 📦 بأمر تثبيت
- **ماذا / what:** Distant mountain layers as displaced planes whose top edge follows ridged noise, placed at increasing distance for depth.
- **كيف / how:** PlaneGeometry(dz·4.2, hgt·1.6, 400, 1), top vertices y = hgt·(0.35+0.65·ridged(2.2x+seed, 3.1seed, 5)) − 0.2hgt; layers [700 m,140], [1400,260], [2600,420], [4500,650].
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:54`

#### 3D-68 · شريط طريق مبني على منحنى · Curve-based road ribbon · 📦 بأمر تثبيت
- **ماذا / what:** A road follows a curved centreline: sample a CatmullRom curve, offset left/right by the normal, triangulate; terrain is flattened near the road with a smooth falloff.
- **كيف / how:** roadX(z)=22·sin(min(0,z+60)/380)+…; points every 20 m to −4200; N=800; ground height ×smooth(ROAD_W, ROAD_W+30, |x−roadX(z)|).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:13` · `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:71`

#### 3D-69 · سماء فيزيائية بشمس متحركة · Physical sky with moving sun · 📦 بأمر تثبيت
- **ماذا / what:** A Rayleigh/Mie sky where the sun's elevation and azimuth follow the story (dawn → day → overcast → clearing) and fog colour/density follow it too.
- **كيف / how:** sky = makeSky(scene, {turbidity, rayleigh, mie, mieG, scale}); sun = sky.setSun(elev, azim); water: elev 2.5+24·smooth(0,6.5)−8·smooth(8,10)+12·smooth(12.5,15.5); turbidity 3+7·overcast; koi setSun(17°, 142°) turbidity 5, rayleigh 1.4.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:64` · `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:30`

#### 3D-70 · سماوات مخصصة بالتظليل · Custom gradient sky shaders · 📦 بأمر تثبيت
- **ماذا / what:** Hand-written sky domes for specific moods: blue-hour gradient with afterglow band and Earth's shadow, night navy with Mie moon glow, violet/magma eclipse sky.
- **كيف / how:** BackSide SphereGeometry ShaderMaterial; blue_hour zen (.02,.045,.13) mid (.07,.15,.36) hor (.30,.34,.52) + band exp(−9y)·g³ (1,.45,.2); night: pow(m,900)·1.2 + pow(m,60)·.16 + pow(m,8)·.05; includes tonemapping/colorspace chunks.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:26` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:139` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:23`

#### 3D-71 · بحر بانعكاس مستوٍ وموج طويل · Planar-reflection sea with swell normals · 📦 بأمر تثبيت
- **ماذا / what:** Open sea using a planar reflection water surface whose 'sun' is the moon, with a custom low-swell normal map, so a glitter path runs to camera and the boat rides heave/pitch/roll.
- **كيف / how:** makeSea({size 24000, res 1024, color 0x061525, distortion 3.2, waveSize 2.4, normals: normalFromHeight(512, fbm(x/48)·.7 + fbm(x/11+9)·.3, 2.6)}); uniforms sunDirection = MOON_DIR, sunColor = kelvin(4100)·.9, time .55t; heave .09 sin(1.25t+.4)+.035 sin(2.3t+1.7).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:186` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:226`

#### 3D-72 · إضاءة بيئية من تدرج · Environment from gradient (IBL) · 📦 بأمر تثبيت
- **ماذا / what:** Image-based lighting generated from a simple sky/horizon/ground gradient plus a sun lobe, no HDRI files.
- **كيف / how:** envFromGradient(renderer, scene, {top, horizon, ground, sun, sunColor, sunPower}); scene.environmentIntensity .5–.55; e.g. koi top 0x8fb1d6 horizon 0xf2c894 ground 0x34402a sun 0xffcf8f ×5; sound_ground horizon 0x8a2a1a sun 0xff8a4a ×3.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:32` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:30` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:39`

#### 3D-73 · أضواء الشاطئ البعيد كمؤشر حجم · Far shore lights and horizon scale cues · 📦 بأمر تثبيت
- **ماذا / what:** A scatter of tiny warm and white points 6–7 km away on the horizon gives the sea its scale and streaks in the reflection.
- **كيف / how:** 150 Points at z ≈ −6480, x −5200…1800, height 4–18 m; 70% kelvin(2200–3100), else kelvin(5200); size 1.6 px no attenuation, additive, opacity .75, fog off.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:178`

#### 3D-74 · نحت SDF · SDF sculpt shape-kit · 📦 بأمر تثبيت
- **ماذا / what:** Soft primitives smooth-unioned and surface-net meshed into watertight vertex-coloured mesh.
- **كيف / how:** K3S.sculpt().ellipsoid/sphere/capsule/box/torus(...,{k,op,rot,color}).paint().mesh({cells})
- **أرقام / params:** 136 cells ~1.5 s; bunny 274k tris ~4 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/shape-kit.md` · `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js` · `100-superskills/skills/kosif-montage-motion/tests/test_shape_kit.py`

#### 3D-75 · خلفية الاستوديو · Studio backdrop/stage disc/lite post · 📦 بأمر تثبيت
- **ماذا / what:** Background, scan-sweep disc, bloom+grade post.
- **كيف / how:** K3S.studioBackdrop, stageDisc, makeLitePost
- **أرقام / params:** bloom threshold >=0.9
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/shape-kit.md`

#### 3D-76 · هيكل الشبكة · Truss overlay · 📦 بأمر تثبيت
- **ماذا / what:** Structural-twin truss riding the rig.
- **كيف / how:** K3S.trussOverlay(model,{nodeParts})
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/shape-kit.md` · `100-superskills/skills/kosif-montage-motion/references/STRUCTURAL_TWIN.md`

#### 3D-77 · تكامل: Three.js · Integration: Three.js · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### 3D-78 · تكامل: React Three Fiber + Drei · Integration: React Three Fiber + Drei · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### 3D-79 · تكامل: Babylon.js · Integration: Babylon.js · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### 3D-80 · مجسم الجيود البلوري ثلاثي الأبعاد · Crystalline geode hero object (Three.js) · 📦 بأمر تثبيت
- **ماذا / what:** A dark metallic icosahedron shell with a glowing octahedron core and two thin orbiting rings, rotating at different rates — a ready 'tech/AI' hero object.
- **كيف / how:** cinematic_3d.html: IcosahedronGeometry(2.2,2) + MeshStandardMaterial{color #0f172a, metalness .85, roughness .15}; inner OctahedronGeometry(1.4) emissive #0284c7 intensity .8; two TorusGeometry(3.6,0.04,16,100) MeshBasic #38bdf8 opacity .6; rotations per t (0.45/0.6/0.8/0.9/0.3/0.4 rad/s).
- **أرقام / params:** shell r=2.2 detail 2; core r=1.4; rings r=3.6 tube 0.04; ring tilt PI/3 and PI/4
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:128` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:197`

#### 3D-81 · ستايل مصر ٢١٢٠ المستقبلية · Egypt 2120 hopeful solarpunk (style) · 📦 بأمر تثبيت
- **ماذا / what:** An 18 s vertical WebGL film imagining Egypt in 2120: orbit view of the Nile as a lotus of lights, Giza at dawn with heliostats and a solar city, golden-hour Nile valley with vertical farms and a maglev, Cairo at night with a lotus tower and air-taxi lanes, Alexandria at blue hour with a reborn Pharo…
- **كيف / how:** Three.js 0.169 scenes S1-S5 switched by a shot table, one deterministic render(t), Cairo glass captions over the canvas, frame capture with Playwright, locally synthesised Hijaz soundtrack.
- **أرقام / params:** 1080x1920, 30 fps, 18 s, 6 shots: 0-2.6 / 2.6-6.0 / 6.0-9.5 / 9.5-13.5 / 13.5-16.5 / 16.5-18
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html` · `kosif-one/projects/egypt-2120-animation/README.md`

#### 3D-82 · تضاريس بالضوضاء الكسرية · Value noise + fbm terrain · 📦 بأمر تثبيت
- **ماذا / what:** Dunes and valley ground generated from smooth value noise summed over 5 octaves, with vertex colours by height and distance to the river.
- **كيف / how:** vnoise with smoothstep interpolation of sin-hash corners; fbm 5 octaves, amplitude x0.5, frequency x2.03; terrain() displaces a rotated PlaneGeometry (size 4000-5000, 220-300 segments) and writes vertex colours, computeVertexNormals; MeshStandardMaterial vertexColors roughness .95.
- **أرقام / params:** dune = 4.5 fbm(x*.006) + 1.8 fbm(x*.02+9) - 3; sand #E2B577 -> #B9824B; field colours #3E8A35 #5FA544 #8DBF4A #A9C463 #4F9A3C
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html:67-71` · `kosif-one/projects/egypt-2120-animation/index.html:160-165` · `kosif-one/projects/egypt-2120-animation/index.html:214-216`

#### 3D-83 · شيدر نوافذ المدينة ليلاً · Night-city window shader (instanced) · 📦 بأمر تثبيت
- **ماذا / what:** Thousands of instanced box buildings get lit windows computed from world position (consistent at any height), warm/cool window colours, rim light and horizontal light bands, with fog.
- **كيف / how:** InstancedMesh(Box translated to base) up to 2600 instances on a grid skipping avenues (gx%6, gz%7) as flight corridors; fragment: grid cell (u/2.4, y/3.2), window mask .18-.82 x .22-.78, on if hash>1-lit, colour mix(warm,cool,hash>.62) x(.55..1.3); rim pow(1-|N.V|,3)*.35; band step(.985,fract(y/38+seed)).
- **أرقام / params:** warm #FFC77A, cool #8FE6FF, base #0B1226, rim #3B5BA8, lit .32-.8, fog #121A44 .0021
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html:122-140` · `kosif-one/projects/egypt-2120-animation/index.html:331-339`

#### 3D-84 · حقول طاقة شمسية بالتكرار · Instanced solar fields (heliostats, panels, pivots) · 📦 بأمر تثبيت
- **ماذا / what:** Clean-energy landscapes from instancing: 900 heliostat mirrors aimed at a glowing receiver tower, 168 foreground mirrors tilted to the sun on posts, 2400 dark solar panels in blocks and up to 160 green centre-pivot circles.
- **كيف / how:** InstancedMesh + Object3D.lookAt(target) + rotateX(PI/2) per instance; metal 1 roughness .05 envMapIntensity 2.2; receiver sphere MeshBasic colour x14 pulsing 1+.08 sin(9t).
- **أرقام / params:** heliostats 900 around (-620,420) r 40-190; panels 12 blocks x200 tilt -.45; pivots r 16-34
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html:229-243` · `kosif-one/projects/egypt-2120-animation/index.html:282-292`

#### 3D-85 · عناصر عمارة مستقبلية · Futuristic architecture kit (vertical farm, maglev, lotus tower, Pharos) · 📦 بأمر تثبيت
- **ماذا / what:** Ready procedural props: glass vertical farms with glowing green torus tiers, a maglev track (CatmullRom tube + pylons) with capsule cars and cyan stripe, a lotus tower with 8 additive pink petals, 4 rotating holographic rings and obelisk spires, a three-tier Pharos lighthouse with glowing bands, gla…
- **كيف / how:** Primitive geometries + MeshPhysicalMaterial (transmission/clearcoat) + emissive MeshBasic colours multiplied >1 so bloom catches them.
- **أرقام / params:** farm tiers #7CFF9F x2.2 every 7 units; maglev stripe #59E3FF x4; petals #FF8FD0 op .26; rings #5FF0FF op .5; lighthouse bands #FFD9A0 x5, lamp #FFF3D6 x26; turbine lamps #FF4A3A x10
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html:294-311` · `kosif-one/projects/egypt-2120-animation/index.html:340-354` · `kosif-one/projects/egypt-2120-animation/index.html:391-411`

#### 3D-86 · تصيير إطار HTML ثلاثي الأبعاد · Single-frame HTML/Three.js renderer · 📦 بأمر تثبيت
- **ماذا / what:** Renders one deterministic frame of an HTML/WebGL page (waits for window.__ready, seeks render(t)).
- **كيف / how:** python html_render.py page.html out.png [--size 1920x1080] [--t 2.5]; finds Edge/Chrome/Chromium or /opt/pw-browsers.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/html_render.py`

#### 3D-87 · مشهد الحوت والتنين ثلاثي الأبعاد · 3D whale vs dragon showcase page · 📦 بأمر تثبيت
- **ماذا / what:** Reference Three.js page: wet clearcoat skin with procedural bump/roughness, translucent wing membranes, cold lightning key, warm fire light, fog, additive fire/embers/steam/spray, rain streaks, bloom, grain, ACES.
- **كيف / how:** Open scenes/whale_dragon_3d.html via html_render.py or as a film with film.py animate.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/scenes/whale_dragon_3d.html`

#### 3D-88 · رندر HTML ثلاثي الأبعاد · HTML/Three.js deterministic frame render · 📦 بأمر تثبيت
- **ماذا / what:** Headless Edge/Chrome renders a page with window.__ready / render(t) / __duration contract to PNG; Three.js realism: MeshPhysicalMaterial (clearcoat, transmission, sheen), cold DirectionalLight soft shadows + warm PointLight + dim HemisphereLight, FogExp2, additive Points, LineSegments rain, UnrealBl…
- **كيف / how:** python3 html_render.py page.html x.png --size 1920x1080 --t T --scale 1
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/scripts/html_render.py:94` · `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md`

#### 3D-89 · قالب مشهد ثلاثي الأبعاد · Three.js cinematic scene template · 📦 بأمر تثبيت
- **ماذا / what:** Three.js 0.169 scene with hero object, procedural city, key+rim lights, ACES tone mapping and UnrealBloom post.
- **كيف / how:** templates/scene-3d.html; renderer preserveDrawingBuffer true; camera as function of t.
- **أرقام / params:** three@0.169.0; ACESFilmic exposure 1.05; UnrealBloomPass(strength 0.7, radius 0.6, threshold 0.82); <150k tris
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/templates/scene-3d.html`

#### 3D-90 · تضاريس إجرائية · Procedural terrain · 📦 بأمر تثبيت
- **ماذا / what:** Height-function terrain with slope/height vertex colours plus tiled procedural albedo and normal detail maps.
- **كيف / how:** K3.makeTerrain({height(x,z), colour(h,slope,x,z,c), seg, size, texSize, albedoRepeat, normalRepeat, normalScale}).
- **أرقام / params:** seg 560, size 4600, texSize 1024, albedo repeat 60, normal repeat 90, normalScale .55, roughness .95
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:112`

#### 3D-91 · قصب وعشب · Reed / grass blades · 📦 بأمر تثبيت
- **ماذا / what:** Instanced tapered strips with wind sway.
- **كيف / how:** K3.makeBlades({n, region, tall, width, amp, freq, hue}).
- **أرقام / params:** n 1500, tall .9 m, width .02, hue .24, sway 1.4 Hz
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:746`

#### 3D-92 · تحميل نماذج GLB · GLB model loader with sought animation · 📦 بأمر تثبيت
- **ماذا / what:** Loads a GLB (bundled as data URL) and seeks its AnimationMixer to t.
- **كيف / how:** const m = await K3.loadModel(url, {clip, offset, speed}); m.userData.set(t).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:964`

#### 3D-93 · قالب المشهد ثلاثي الأبعاد · Cinematic 3D landscape template · 📦 بأمر تثبيت
- **ماذا / what:** Alpine bay at sunrise: ridged terrain, forest, sea, cloud slab, lens flare, post stack, three camera keys, sun swinging off-axis, letterbox opening and RTL title words.
- **كيف / how:** python3 motion.py new NAME --3d; edit src/main.js; motion.py bundle -> assets/main.bundle.js; motion.py render --engine studio.
- **أرقام / params:** fog exp2 #c9d6e2 1.1e-4; fov 38; sun elevation 6 -> 26°, azimuth 165 -> 115°; exposure .46 -> .58; letterbox 70 px -> 0 over 2.2 s; title 112 px/800
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/templates/scene3d/index.html` · `kosif-studio/motion/templates/scene3d/src/main.js` · `kosif-studio/tests/test_studio.py:606`

#### 3D-94 · وصفة مشهد ثلاثي الأبعاد بـ Three.js · Three.js single-frame cinematic 3D page recipe · 📦 بأمر تثبيت
- **ماذا / what:** A deterministic Three.js shot: PBR MeshPhysicalMaterial (clearcoat for wet skin, rough hide), cold directional key with soft shadows, warm point + spot fire light, hemisphere fill, FogExp2, additive Points for fire/embers/steam/spray, LineSegments rain, UnrealBloom + FilmPass + OutputPass with ACES.
- **كيف / how:** Write one HTML with an importmap to three@0.170.0; set window.__ready after the first composer.render; render via html_render.py or film.py animate.
- **أرقام / params:** ACES exposure 1.55; PCFSoftShadowMap 2048; fog 0x0d151f density .013; cold 0xcfe0ff 3.2; fire PointLight 0xff8a3a 140 (flicker +-25 at 23 rad/s); SpotLight 0xffa050 220; Hemisphere 0x4a5e80/0x070a10 .9; bloom (.32, .5, .88); FilmPass .22; camera fov 46
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/scenes/whale_dragon_3d.html:1` · `kosif-studio/scenes/whale_dragon_3d.html:266` · `kosif-studio/references/drawing-guide.md:99`

#### 3D-95 · خرائط نتوء وخشونة إجرائية · Procedural noise bump/roughness textures in canvas · 📦 بأمر تثبيت
- **ماذا / what:** Generates tiling grayscale noise textures in a 2D canvas with three's ImprovedNoise for bump and roughness maps — no image downloads.
- **كيف / how:** noiseTexture(size, scale, octaves, base, amp, seedZ) -> CanvasTexture RepeatWrapping; softDisc() radial sprite for particles.
- **أرقام / params:** skin bump 512/24/5 oct; roughness 256/10/4; hide bump 512/40/5
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/scenes/whale_dragon_3d.html:60`

#### 3D-96 · بحر من شبكة ارتفاعات مع زبد · Height-field sea mesh with whitecaps · 📦 بأمر تثبيت
- **ماذا / what:** A 320x320-segment plane displaced by multi-octave noise plus a long swell sine; vertex colours blend to white on crests; wet clearcoat material.
- **كيف / how:** PlaneGeometry(320,320,320,320); h = sum noise*a (4 octaves) + .45 sin(.3x+.1y); cap = smoothstep(h,.9,1.7); MeshPhysicalMaterial roughness .24 clearcoat 1.
- **أرقام / params:** colours 0x14222e -> 0xdfe8f0
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/scenes/whale_dragon_3d.html:86`

#### 3D-97 · دورة المياه ثلاثية الأبعاد · Cinematic 3D water cycle · 📦 بأمر تثبيت
- **ماذا / what:** 17 s explainer film on the three-kit: domain-warped ridged mountains with a carved river, forest, flock, sea, cloud slab, lens flare, vapour, rain and keyed camera, with Arabic titles.
- **كيف / how:** projects/water_cycle_3d (src/main.js + bundle) → render --engine studio
- **أرقام / params:** 1920×1080 30 fps 17 s; fog #C9D6E2 0.00011; fov 38; terrain ridge 820 m
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/water_cycle_3d/src/main.js:1` · `kosif-studio/out/water_cycle_3d.mp4`

#### 3D-98 · بركة الكوي · Koi pond at golden hour · 📦 بأمر تثبيت
- **ماذا / what:** Realism-block 3D scene: shallow water with swell and petal rings, caustics, seven bending koi, falling petals, pebbles, wind-swayed reeds, dappled sun through a canopy, one slow camera path.
- **كيف / how:** three-kit makeShallowWater, addCaustics, makeKoi, makePetals, makePebbles, makeBlades, makeDappledSun, cameraPath
- **أرقام / params:** pond ellipse 6.4×4.1 m; exposure 0.62; fog #CBB08A 0.011; 10 s 1080p30
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/koi_pond/src/main.js:1` · `kosif-studio/out/koi_pond.mp4`

#### 3D-99 · الصوت يرسم الأرض · Sound-drawn land (spectrogram canyon) · 📦 بأمر تثبيت
- **ماذا / what:** Every value comes from the score analysis: the spectrogram becomes a canyon, bass a lava river, kicks throw sparks and squash a chrome orb; on tape-stop the world freezes while the camera drifts (bullet time), silence flips the picture negative, spin-up whips the camera home.
- **كيف / how:** three-kit makeSpectrumGround, spectrumOnTape, makeSparks, makeGlitchPass + channels.json + spectrum_height.png
- **أرقام / params:** 8 tape-seconds across 120 m; fog #1A0A16 0.018; fov 36; 10 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/sound_ground/src/main.js:1` · `kosif-studio/out/sound_ground.mp4`

#### 3D-100 · طريق الساعة الزرقاء · Blue-hour road with light trails · 📦 بأمر تثبيت
- **ماذا / what:** Night-photography film: a slow push at road height while cars become light trails and stars draw short arcs in a one-second exposure.
- **كيف / how:** projects/blue_hour; render --blur 16 --shutter 30 --stack lighten
- **أرقام / params:** 8 s 1080p30; complementary blue/orange
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/blue_hour/src/main.js:1` · `kosif-studio/out/blue_hour.mp4`

#### 3D-101 · أرنب قطيفة كتوأم هيكلي · Plush bunny structural twin · 📦 بأمر تثبيت
- **ماذا / what:** A cute SDF-sculpted plush bunny becomes a 3D space truss, is loaded, breaks at the left ear root, is repaired by a member swap and ranked — every on-screen number from the solver's output.
- **كيف / how:** shape-kit S.bunny({cells:136}) + structural_twin.py v0.2 report → assets/twin.js
- **أرقام / params:** 1080×1920 30 fps 5 s; beats shape 0, joint .85, load 1.65, break 2.55 (t 2.66), swap 3.35, rank 4.15; load up to 3× baseline; spring f 3.2 Hz ζ 0.32; 35 nodes 109 members, first failure 2.38×
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/bunny_twin/src/main.js:1` · `kosif-studio/motion/projects/bunny_twin/twin/report.json`

#### 3D-102 · مشاهد 3D سينمائية · Style: Cinematic 3D (cinematic-3d) · 📦 بأمر تثبيت
- **ماذا / what:** True 3D scenes with spline camera moves and 3-point lighting.
- **كيف / how:** Three.js; CatmullRom camera paths 2-5s ease-in-out sine; key 45 deg, fill 30%, rim; fov 40-55. Scaffold: python3 tools/kosif.py scaffold cinematic-3d <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:cinematic-3d` · `kosif-tool/playbooks/3d.md`

#### 3D-103 · مجسمات Low Poly · Style: Low poly 3D (lowpoly-3d) · 📦 بأمر تثبيت
- **ماذا / what:** Faceted low-poly models, flat shading, matte materials.
- **كيف / how:** Three.js flatShading, roughness 0.6-0.9; drop-in objects 0.4s + spring damping 12. Scaffold: python3 tools/kosif.py scaffold lowpoly-3d <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:lowpoly-3d` · `kosif-tool/playbooks/3d.md`

#### 3D-104 · عالم تمرير · Style: Scroll world (scroll-world) · 📦 بأمر تثبيت
- **ماذا / what:** A world revealed as if scrolled through: layered sections passing the camera.
- **كيف / how:** 2.5D/Three.js stacked sections, camera dolly 0.3-1.2 units/s; sections enter as camera passes. Scaffold: python3 tools/kosif.py scaffold scroll-world <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:scroll-world` · `kosif-tool/playbooks/3d.md`

#### 3D-105 · عمق 2.5D · Style: Fake 3D (2.5D) (fake3d) · 📦 بأمر تثبيت
- **ماذا / what:** Depth illusion from flat layers, single continuous shot.
- **كيف / how:** CSS perspective 1200px, translateZ per layer (-400,-120,0,+200); pre-scale by (1200-z)/1200. Scaffold: python3 tools/kosif.py scaffold fake3d <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:fake3d` · `kosif-tool/playbooks/3d.md`

#### 3D-106 · عالم أيزومتريك · Style: Isometric world (isometric) · 📦 بأمر تثبيت
- **ماذا / what:** Isometric diorama world with camera travelling between zones.
- **كيف / how:** Orthographic camera, 35.264 deg pitch, fixed grid unit; or SVG iso transform. Scaffold: python3 tools/kosif.py scaffold isometric <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:isometric` · `kosif-tool/playbooks/3d.md`

#### 3D-107 · ثلاثي الأبعاد · Category: 3D · 📦 بأمر تثبيت
- **ماذا / what:** Capability family '3d' (10 catalog entries) with a dedicated bilingual playbook of timings and recipes.
- **كيف / how:** Read playbooks/3d.md (visual grammar, motion mechanics, scene recipes, QA); build in starters/html-canvas or starters/remotion; filter catalog with python3 tools/kosif.py list --category 3d.
- **أرقام / params:** key 45deg fill 30% rim; fov 40-55 (85mm ~24); spline 2-5s; orbit 10-25deg/s; iso 35.264deg
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/3d.md` · `kosif-tool/catalog/categories.json` · `kosif-tool/catalog/meta.json`

#### 3D-108 · كاميرا أيزومترية متعامدة · Isometric orthographic camera · 📦 بأمر تثبيت
- **ماذا / what:** Isometric worlds with an orthographic camera and fixed grid unit.
- **كيف / how:** Three.js OrthographicCamera pitched at true isometric angle; fixed grid unit.
- **أرقام / params:** 30° projection; true iso camera pitch 35.264°
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:17`

#### 3D-109 · وصفة المنصة الدوارة للمنتج · Product turntable recipe · 📦 بأمر تثبيت
- **ماذا / what:** Product drops on plinth, orbits 90° with push-in, callout draws, hero hold.
- **كيف / how:** Three.js seek scene or 2.5D.
- **أرقام / params:** 0–0.6 s drop (ease-in quad+spring); 0.6–4.6 s orbit 90° (sine in-out); 2.0–2.4 s callout draws (ease-out cubic); 4.6–6.0 s hold
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:35-42`

#### 3D-110 · تحليق متزامن مع السرد · Narration-locked fly-through · 📦 بأمر تثبيت
- **ماذا / what:** Camera follows a spline through waypoints, each aligned to a narration term.
- **كيف / how:** Waypoint times from words.json.
- **أرقام / params:** 4 waypoints in 6 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:48` · `kosif-tool/playbooks/3d.md:80`

#### 3D-111 · سينما فور دي · Cinema 4D MoGraph / Redshift · 🔑 مفتاح/خدمة
- **ماذا / what:** Procedural cloner/field motion graphics and Redshift GPU renders with ACEScg.
- **كيف / how:** c4dpy scripting; Alembic/USD export. Paid.
- **الدليل / proof:** `kosif-atlas/skills/228-mas-3d-games/706-cinema-4d/SKILL.md`

#### 3D-112 · أنماط التحليق ثلاثي الأبعاد بسيزيوم · Cesium 3D flyover modes · 🔑 مفتاح/خدمة
- **ماذا / what:** Helicopter-style flights through real terrain (landscape mode) or photoreal cities (city mode) rendered frame by frame.
- **كيف / how:** Landscape: MapTiler terrain-quantized-mesh-v2 + satellite-v2 (no Cesium ion token). City: Google Photorealistic 3D Tiles with the globe hidden, maximumScreenSpaceError 4 for hero landmarks, 6-8 for wide shots. Load Cesium 1.143 from CDN after setting CESIUM_BASE_URL. Render a mid-frame still before the full clip.
- **أرقام / params:** SSE 4 hero / 6-8 wide; Cesium 1.143; Google promo clips <= 30 s
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/TECHNIQUE.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/references/3d-data-sources.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/references/3d-flyover-architecture.md`

#### 3D-113 · تكامل: Blender MCP · Integration: Blender MCP · 🔑 مفتاح/خدمة
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### 3D-114 · تكامل: Spline MCP · Integration: Spline MCP · 🔑 مفتاح/خدمة
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### 3D-115 · عالم ثلاثي بالتمرير · Scroll-scrubbed fly-through world · 🔑 مفتاح/خدمة
- **ماذا / what:** Landing page where scroll position drives currentTime of pre-rendered AI camera clips so the camera flies scene to scene without cuts.
- **كيف / how:** Stills -> dive clips -> connectors -> encode -> mountScrollWorld.
- **أرقام / params:** N stills, N dives, N-1 connectors
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md`

#### 3D-116 · أرضية شبكية منظورية · Perspective grid floor · 👁 شوهد في فيديو
- **ماذا / what:** CSS 3D rotateX(~70deg) grid plane or Three.js GridHelper under a slowly drifting camera; HUD cards float above
- **أرقام / params:** fade grid to black at distance
- **الدليل / proof:** `style:plotter` · `style:pm-maxalexweber-67688b`

#### 3D-117 · كرة جزيئات · Particle sphere · 👁 شوهد في فيديو
- **ماذا / what:** fibonacci sphere points projected, rotate Y
- **أرقام / params:** 500 pts
- **الدليل / proof:** `style:pm-mrtanviir-132457` · `style:pm-rendesr-86be44`

#### 3D-118 · سُمك مزيف بتكديس نسخ الشكل · Fake-3D extrusion by stacked layers · 👁 شوهد في فيديو
- **ماذا / what:** draw the same path N times offset along the projected face normal from back to front, colour darkening toward the back; N = screen thickness / 1.5 px; top layer = lit face with gradient
- **أرقام / params:** gold #fff1bc->#f5b54a->#b4641a, layer step 1.5 px
- **الدليل / proof:** `style:fake3d`

#### 3D-119 · إسقاط متوازي بمصفوفة واحدة · Parallel projection via one matrix() · 👁 شوهد في فيديو
- **ماذا / what:** rotate the object's local u,v axes in 3D, project to 2D; transform='matrix(ux,uy,vx,vy,cx,cy)' on the flat path; flip to back colour when facing away
- **أرقام / params:** yaw/pitch/roll per frame
- **الدليل / proof:** `style:fake3d`

#### 3D-120 · دالة إسقاط أيزومتريك · Isometric projection function · 👁 شوهد في فيديو
- **ماذا / what:** X = OX + (x - y) * cos30 * S; Y = OY + (x + y) * 0.5 * S - z * S; use for every world point including camera targets and text anchors
- **أرقام / params:** S = unit px, cos30 = 0.866
- **الدليل / proof:** `style:isometric`

#### 3D-121 · لصق نوافذ وأبواب على أوجه الصندوق · Face-mapped details via matrix() · 👁 شوهد في فيديو
- **ماذا / what:** compute matrix() that maps a flat rect onto a box face; draw windows/doors/signs in flat coordinates inside it
- **أرقام / params:** per-face affine
- **الدليل / proof:** `style:isometric`

#### 3D-122 · ترتيب العمق بمجموع x+y · Painter's depth sort by x+y · 👁 شوهد في فيديو
- **ماذا / what:** sort ground items by (x + y) ascending; elevated items (floating island, box on van) drawn after what is beneath; avoid tall buildings in front of key action
- **أرقام / params:** view dir (1,1,1)
- **الدليل / proof:** `style:isometric`

#### 3D-123 · خريطة مائلة وأشياء واقفة عليها · Tilted map plane with standing sprites · 👁 شوهد في فيديو
- **ماذا / what:** wrap SVG in div perspective(1400px) rotateX(theta); for upright sprites compute Y' = Y cos(theta), z = Y sin(theta), scale = P/(P - z), and draw them in an overlay at that position/scale so they stand
- **كيف / how:** wrap SVG in div perspective(1400px) rotateX(theta); for upright sprites compute Y' = Y cos(theta), z = Y sin(theta), scale = P/(P - z), and draw them in an overlay at that position/scale so they stand upright
- **أرقام / params:** P=1400, theta ~50deg
- **الدليل / proof:** `style:map-journey`

#### 3D-124 · فوضى عناصر تطير بعمق · Z-depth chaos field · 👁 شوهد في فيديو
- **ماذا / what:** spawn 30-50 UI chips/notes at random x/y and z; animate translateZ toward camera and rotate slightly; blur proportional to |z - focus|
- **أرقام / params:** perspective 1200 px, blur 0-14 px, 1.5-2 s
- **الدليل / proof:** `style:pm-agonaliu-466a8f`

#### 3D-125 · نص ملتف حول كرة دوّارة · Text wrapped on rotating sphere · 👁 شوهد في فيديو
- **ماذا / what:** render paragraph to canvas texture, map onto sphere with emissive fire noise shader beneath; rotate y; add fresnel rim glow
- **أرقام / params:** sphere 30% H, rotation 15°/s, rim #ff9a2a
- **الدليل / proof:** `style:pm-ajith-io-4c248f`

#### 3D-126 · كرة نقاط · Fibonacci point sphere · 👁 شوهد في فيديو
- **ماذا / what:** fibonacci sphere points projected, rotate Y
- **أرقام / params:** ~500 pts
- **الدليل / proof:** `style:pm-ajith-io-b5626e`

#### 3D-127 · شريط بطاقات · 3D card ribbon · 👁 شوهد في فيديو
- **ماذا / what:** instanced cards along a sine spline flowing in z
- **الدليل / proof:** `style:pm-ajith-io-ea7f2d`

#### 3D-128 · مركبة كرتونية منخفضة المضلعات · Toon low-poly vehicle · 👁 شوهد في فيديو
- **ماذا / what:** box primitives, MeshToon, black outline pass
- **الدليل / proof:** `style:pm-allforbigfire-86ff3c`

#### 3D-129 · ديوراما على قرص عائم · Floating diorama disc · 👁 شوهد في فيديو
- **ماذا / what:** cylinder island with layered rim, low-poly props, soft shadows
- **أرقام / params:** orthographic-ish FOV 30
- **الدليل / proof:** `style:pm-anas0ra-e57aea`

#### 3D-130 · حجر خشبي مستدير الحواف · Rounded wooden tile · 👁 شوهد في فيديو
- **ماذا / what:** RoundedBoxGeometry(1,1,0.35, 4, 0.08); canvas texture with procedural grain lines and serif letter + small score number
- **أرقام / params:** base #d3bb9b, grain #a58862
- **الدليل / proof:** `style:pm-anilraok-eff262`

#### 3D-131 · تأثيث مشهد المكتب · Desk prop set dressing · 👁 شوهد في فيديو
- **ماذا / what:** cylinder mug with orange material + dark liquid disc, steam sprites; hex pencil with eraser; paper plane with crossword canvas texture
- **أرقام / params:** warm key + cool fill
- **الدليل / proof:** `style:pm-anilraok-eff262`

#### 3D-132 · جدار لقطات مواقع مائل · Tilted screenshot wall · 👁 شوهد في فيديو
- **ماذا / what:** grid of screenshots on a plane rotateX(50deg) rotateZ(-20deg), slow translate pan, blur outer tiles
- **أرقام / params:** pan 3-4% per second
- **الدليل / proof:** `style:pm-arjunsh1607-93005d`

#### 3D-133 · بحر غروب مولَّد إجرائيًا · Procedural sunset ocean · 👁 شوهد في فيديو
- **ماذا / what:** sum of 4-8 Gerstner waves on a large plane; fresnel mix of sky colour and deep water; specular highlight from low sun creates glitter path
- **أرقام / params:** wavelengths 2-30 m, amplitude 0.05-0.4 m; sun elevation ~5°
- **الدليل / proof:** `style:pm-axtonliu-0b861d`

#### 3D-134 · كرة نقاط بمدارات · Point sphere with orbits · 👁 شوهد في فيديو
- **ماذا / what:** 1000 fibonacci points, rotate Y, two elliptical rings
- **الدليل / proof:** `style:pm-blue-clarity-ef56d0`

#### 3D-135 · مسرح ثلاثي الأبعاد كديكور للشرح · 3D stage as explainer set · 👁 شوهد في فيديو
- **ماذا / what:** build one reusable 3D environment (stadium) with low-poly props; for each chapter set a camera pose and animate a 6-12 s eased dolly/orbit while overlays explain
- **أرقام / params:** FOV 35-50°, move 8-12 s easeInOutSine
- **الدليل / proof:** `style:pm-blueoctopusai-dd17bd`

#### 3D-136 · خط مرسوم على الأرض بمنظور صحيح · Perspective-correct line on ground · 👁 شوهد في فيديو
- **ماذا / what:** render the key line as a thin quad lying on the field mesh (slightly above to avoid z-fighting) so it follows camera perspective and terrain; occlude by player meshes
- **أرقام / params:** width 0.3 m, yellow #f2d21b, offset 2 mm
- **الدليل / proof:** `style:pm-blueoctopusai-dd17bd`

#### 3D-137 · افتتاحية لقطة علمية مكبّرة · Macro science-figure opener · 👁 شوهد في فيديو
- **ماذا / what:** Instanced spheres (~1500, r 4-8 px) inside a translucent glass sphere with Fresnel rim; blurred duplicate capsules in background (DOF blur 30-40 px); italic 'Fig. 1' caption below
- **أرقام / params:** jitter amplitude 1-2 px, push-in scale 1.0->1.06 over 1.2 s
- **الدليل / proof:** `style:pm-bogdandragomir-35e024`

#### 3D-138 · مروحة بطاقات بمنظور · Perspective card fan · 👁 شوهد في فيديو
- **ماذا / what:** 3 sleeves enter with rotateY ±12° and opposing rotateZ tilts, spread into 6 smaller; later 4 covers float with coordinated sin offsets and z-order
- **أرقام / params:** perspective 1200px, float amp 6px period 3 s
- **الدليل / proof:** `style:pm-brainextends-e19ac3`

#### 3D-139 · مركبة إجرائية من أشكال أولية · Procedural vehicle from primitives · 👁 شوهد في فيديو
- **ماذا / what:** one factory function builds fuselage lathe, wings extrude, prop blades; materials per part
- **الدليل / proof:** `style:pm-buildfastwithai-ed9447`

#### 3D-140 · طيران فوق تضاريس إجرائية · Procedural terrain flyover · 👁 شوهد في فيديو
- **ماذا / what:** noise-based patchwork ground + fog, chase cam with banking
- **الدليل / proof:** `style:pm-buildfastwithai-ed9447`

#### 3D-141 · إغلاق غطاء جهاز ثلاثي · 3D device lid close · 👁 شوهد في فيديو
- **ماذا / what:** Hinge-rotate laptop lid 110°→0° with ease-in-out, screen dims
- **أرقام / params:** ~1 s
- **الدليل / proof:** `style:pm-cansincengiz-me-cf68dd`

#### 3D-142 · نفق المضلعات · Polygon tunnel · 👁 شوهد في فيديو
- **ماذا / what:** Nested hexagons/pentagons scaled exponentially and rotated, dashed strokes, speed lines radiating
- **أرقام / params:** 6–8 layers
- **الدليل / proof:** `style:pm-crazyalphaaa-bc7e75`

#### 3D-143 · تحليق فوق شبكة بطاقات · 3D card-grid flight · 👁 شوهد في فيديو
- **ماذا / what:** CSS 3D rotateX ~50° plane of cards, camera translates then levels to focus one card
- **أرقام / params:** ~1.5 s
- **الدليل / proof:** `style:pm-danilowm-d3720d`

#### 3D-144 · أنابيب عقدة متوهجة · Glowing torus knot tubes · 👁 شوهد في فيديو
- **ماذا / what:** TubeGeometry knot (2,3), gradient emissive, rotate
- **الدليل / proof:** `style:pm-eyishazyer-af035b`

#### 3D-145 · بلاطات متساوية القياس ترتفع إلى مكعبات · Isometric tile rise · 👁 شوهد في فيديو
- **ماذا / what:** Flat parallelogram tiles in true isometric projection extrude upward in a travelling wave
- **أرقام / params:** elevation 35.264°, azimuth 45°, wave 60 ms per column
- **الدليل / proof:** `style:pm-fionntobin-97b7af`

#### 3D-146 · غرفة ثلاثية الأبعاد إيزومترية · Isometric 3D room reveal · 👁 شوهد في فيديو
- **ماذا / what:** cutaway diorama room in pastel palette, items appear progressively as progress grows
- **أرقام / params:** 2 walls + floor, soft shadows
- **الدليل / proof:** `style:pm-gabrielbuzziv-4ff0c6`

#### 3D-147 · حلقة وكرة جسيمات ثلاثية الأبعاد · 3D particle torus/sphere · 👁 شوهد في فيديو
- **ماذا / what:** points on a torus parametric surface rotated in 3D and projected; colour by depth violet->red; morph torus->sphere
- **أرقام / params:** ~2000 points, rotate 30°/s, additive glow
- **الدليل / proof:** `style:pm-ghinaiya-nirmal-5d8fec`

#### 3D-148 · مكعب سلكي دوّار · Wireframe cube spin · 👁 شوهد في فيديو
- **ماذا / what:** project 8 vertices with rotation matrices, draw 12 edges in orange with slight duplicate offset (sketchy)
- **أرقام / params:** rotate 40°/s on two axes
- **الدليل / proof:** `style:pm-gizakdag-b8c59e`

#### 3D-149 · كهف منخفض المضلعات · Low-poly cave set · 👁 شوهد في فيديو
- **ماذا / what:** Scatter flatShaded displaced icosahedrons around a descending path, dark crimson material, fog to black
- **أرقام / params:** detail 1, displacement 0.3, fog near 10 far 40, color #350006
- **الدليل / proof:** `style:pm-gorden-sun-041f56`

#### 3D-150 · مجسم منخفض المضلعات مرسوم برمجيًا · Software-rendered low-poly object · 👁 شوهد في فيديو
- **ماذا / what:** Project an octahedron (or any low-poly mesh) with a simple perspective matrix, sort faces back-to-front, flat-shade with one light; rotate on two axes; surround with 2 tilted orbit ellipses, crop brac
- **كيف / how:** Project an octahedron (or any low-poly mesh) with a simple perspective matrix, sort faces back-to-front, flat-shade with one light; rotate on two axes; surround with 2 tilted orbit ellipses, crop brackets and a numeric readout panel; giant outline word behind at 10% opacity
- **أرقام / params:** ~128 tris, FOV ~40 deg, rotation 60-90 deg/s
- **الدليل / proof:** `style:pm-grace-sunnyy-29bc61`

#### 3D-151 · جدار مصغّرات بمنظور مائل · Tilted perspective thumbnail wall · 👁 شوهد في فيديو
- **ماذا / what:** grid of rounded thumbnails on a plane rotated (rotateX ~50°, rotateZ ~-20°) drifting slowly, headline in italic serif + bold violet sans above
- **أرقام / params:** 4x4 tiles, drift 40 px/s
- **الدليل / proof:** `style:pm-influencer-seo-ce8c33`

#### 3D-152 · تقليب صفحات ثلاثي الأبعاد · 3D page flip · 👁 شوهد في فيديو
- **ماذا / what:** CSS 3D rotateY on page leaves with motion blur loop
- **أرقام / params:** ~150ms/page
- **الدليل / proof:** `style:pm-itisrazak-3ad902`

#### 3D-153 · نفق مربعات سلكية · Wire square tunnel · 👁 شوهد في فيديو
- **ماذا / what:** nested squares rotated incrementally with perspective
- **أرقام / params:** 20 layers
- **الدليل / proof:** `style:pm-itsuki-dev-10942d`

#### 3D-154 · تضاريس فوكسل · Voxel terrain · 👁 شوهد في فيديو
- **ماذا / what:** box instanced grid with height noise, flat shading, warm palette
- **أرقام / params:** cube 1u, fog 0.02
- **الدليل / proof:** `style:pm-ivanfioravanti-bd9261`

#### 3D-155 · كرة نقاط ثلاثية الأبعاد فوق أرضية شبكية · 3D point sphere over grid floor · 👁 شوهد في فيديو
- **ماذا / what:** Fibonacci sphere of ~2000 points projected in perspective, slow Y rotation, depth-faded colour pink->blue; synthwave perspective grid floor below on navy
- **أرقام / params:** r 300 px, rot 20 deg/s, fov 50
- **الدليل / proof:** `style:pm-jasonzhou1993-8595e0`

#### 3D-156 · جدار لقطات ثلاثي الأبعاد · 3D screenshot wall fly-over · 👁 شوهد في فيديو
- **ماذا / what:** grid of UI cards in CSS 3D rotateX 50°, translate camera
- **أرقام / params:** 3 s
- **الدليل / proof:** `style:pm-jayscambler-3f8889`

#### 3D-157 · مشاهد إيزومترية تنزلق · Isometric room push · 👁 شوهد في فيديو
- **ماذا / what:** Panels slide horizontally like carousel
- **أرقام / params:** 700 ms
- **الدليل / proof:** `style:pm-jesscaroline7-1ff7cb`

#### 3D-158 · كرة معدنية بالأشعة · Raymarched chrome blob · 👁 شوهد في فيديو
- **ماذا / what:** SDF smooth-union spheres, fresnel rim
- **الدليل / proof:** `style:pm-johnsavage-ai-b091c0`

#### 3D-159 · طبقات عمق بباراللاكس · Depth-map parallax layers · 👁 شوهد في فيديو
- **ماذا / what:** split a photo into 3 layers from a depth map, inpaint gaps, scale each layer by camera^Z with different Z
- **أرقام / params:** Z 0.45..1.22
- **الدليل / proof:** `style:pm-koldo2k-5cff87`

#### 3D-160 · مقطع عرضي · Cutaway section · 👁 شوهد في فيديو
- **ماذا / what:** clipping plane through model, colour-code internals
- **أرقام / params:** 1 s reveal
- **الدليل / proof:** `style:pm-konstantinsaifo-96fc89`

#### 3D-161 · صور تدور · Orbiting thumbnails · 👁 شوهد في فيديو
- **ماذا / what:** thumbnails on ellipse orbit around card
- **الدليل / proof:** `style:pm-l3d1c-0e35a3`

#### 3D-162 · حقل مكعبات بارتفاعات متموجة · Extruded cube heightfield · 👁 شوهد في فيديو
- **ماذا / what:** Instanced boxes on a grid whose height = sin wave of distance+time; perspective camera tilted 45°, soft shadows
- **أرقام / params:** grid 20x20, amp 0.5 unit, wave speed 2 rad/s
- **الدليل / proof:** `style:pm-leonkohli-6dc01b`

#### 3D-163 · أرضية مكعبات ترتفع كموجة · Isometric cube heightfield wave · 👁 شوهد في فيديو
- **ماذا / what:** Grid of cubes in isometric projection whose heights follow a radial sine wave; tint cubes inside a mask shape with accent
- **أرقام / params:** 24x24 grid, amplitude 2 units, speed 2 rad/s
- **الدليل / proof:** `style:pm-levabashidze-2d713a`

#### 3D-164 · جدار بطاقات مائل ثلاثي الأبعاد · Tilted 3D card wall · 👁 شوهد في فيديو
- **ماذا / what:** Grid of image cards on a plane with CSS perspective (rotateX ~20 deg, rotateZ ~-15 deg) slowly translating diagonally; headline centred over a dark radial scrim
- **أرقام / params:** perspective 1200 px, drift 30-60 px/s, card radius 12 px
- **الدليل / proof:** `style:pm-listudio-820c7b`

#### 3D-165 · كرة لامعة · Glossy 3D blob · 👁 شوهد في فيديو
- **ماذا / what:** noise-displaced sphere, clearcoat material with coloured rim lights
- **الدليل / proof:** `style:pm-lukasersil-0ed38e`

#### 3D-166 · كتلة سائلة لامعة · Metaball blob · 👁 شوهد في فيديو
- **ماذا / what:** raymarched/SDF smooth-union spheres with specular
- **الدليل / proof:** `style:pm-m1n9-k7-ff9ab9`

#### 3D-167 · طبقات متساوية القياس · Isometric layer stack · 👁 شوهد في فيديو
- **ماذا / what:** 4 rhombus planes stacked vertically with corner nodes, vertical light lines and side labels
- **أرقام / params:** plane gap 40 px, labels mono 10 px, staggered drop-in 120 ms
- **الدليل / proof:** `style:pm-madhav-xo-f97f20`

#### 3D-168 · المشي داخل لوحة · Painting walk-in · 👁 شوهد في فيديو
- **ماذا / what:** low-poly scene textured in painting palette, FPS camera
- **الدليل / proof:** `style:pm-mandelduck-95fd08`

#### 3D-169 · سطح موجي سلكي · Wireframe ripple surface · 👁 شوهد في فيديو
- **ماذا / what:** z=cos(kr-wt)/(1+r) mesh projection
- **الدليل / proof:** `style:pm-math-files-39c9d0`

#### 3D-170 · نموذج ثلاثي الأبعاد أبيض شارح · White-model 3D explainer · 👁 شوهد في فيديو
- **ماذا / what:** MeshStandardMaterial white, soft light, color only on flows
- **الدليل / proof:** `style:pm-mdaman010-e7226a`

#### 3D-171 · منظر مفكك · Exploded view · 👁 شوهد في فيديو
- **ماذا / what:** offset layers along Y with stagger 150 ms
- **الدليل / proof:** `style:pm-mdaman010-e7226a`

#### 3D-172 · عملة كرومية ثلاثية الأبعاد · Chrome 3D coin hero · 👁 شوهد في فيديو
- **ماذا / what:** extruded disc with bevelled rim and logo pockets, environment-mapped metallic material, rotating/tumbling in perspective behind headline type
- **أرقام / params:** metalness 1, roughness 0.2, rotate ~40°/s
- **الدليل / proof:** `style:pm-micheleharmonic-77628e`

#### 3D-173 · فقاعة متقزحة · Iridescent chrome blob · 👁 شوهد في فيديو
- **ماذا / what:** noise sphere with thin-film/fresnel rainbow shading
- **الدليل / proof:** `style:pm-monokern-ade5b6`

#### 3D-174 · كرات زجاجية بانكسار · Raymarched glass spheres · 👁 شوهد في فيديو
- **ماذا / what:** GLSL SDF raymarch with refraction of a type texture plus chromatic dispersion
- **أرقام / params:** 96 steps
- **الدليل / proof:** `style:pm-ndhabarde11-f155b4`

#### 3D-175 · سحب ركامية كرتونية من تجمعات كرات · Toon cumulus from sphere clusters · 👁 شوهد في فيديو
- **ماذا / what:** Build each cloud from 20-60 instanced spheres with a 3-band toon ramp (violet shadow, pink mid, peach rim lit by low sun); add soft outline/fresnel rim
- **أرقام / params:** ramp #5a3a8a/#b066a0/#f0c09a, sun elevation ~5 deg
- **الدليل / proof:** `style:pm-nft-chen-5f8bb0`

#### 3D-176 · مناورات طيران على مسار منحني · Aircraft spline manoeuvres · 👁 شوهد في فيديو
- **ماذا / what:** Animate plane along a Catmull-Rom path; derive bank angle from path curvature (lateral acceleration) and add scripted barrel roll / spiral dive segments
- **أرقام / params:** bank = atan(v^2*k/g), max 80 deg
- **الدليل / proof:** `style:pm-nft-chen-5f8bb0`

#### 3D-177 · كرة أرضية من نقاط مضيئة · Dot-matrix glowing globe · 👁 شوهد في فيديو
- **ماذا / what:** Sphere with points sampled on land mask; warm city-light dots; Fresnel rim glow in blue-white; slow rotation; bloom pass
- **أرقام / params:** ~20k points; rim glow strength high; rotate 3°/s
- **الدليل / proof:** `style:pm-nolkeeg-bf062e`

#### 3D-178 · جدار صور مائل · 3D photo wall · 👁 شوهد في فيديو
- **ماذا / what:** grid of cards rotateX 20 rotateY -25 perspective 1200, drift translate
- **الدليل / proof:** `style:pm-oliahmed205-3e31c4`

#### 3D-179 · ميلان الملصق ثلاثي الأبعاد مع ألواح · 3D poster tilt with slabs · 👁 شوهد في فيديو
- **ماذا / what:** perspective 1200px; rotate poster rotateY(-12deg) rotateX(6deg) and push back; coloured slabs translateZ behind it slide out
- **أرقام / params:** 800 ms, drop shadow 0 20px 40px rgba(0,0,0,.2)
- **الدليل / proof:** `style:pm-pankajkumar-dev-0bee87`

#### 3D-180 · أرضية شبكية منظورية بحروف عملاقة واقفة · Perspective grid floor with standing letters · 👁 شوهد في فيديو
- **ماذا / what:** plane with line grid in perspective (vanishing point mid-top), giant flat-colour letters placed as billboards on it; dolly forward
- **أرقام / params:** grid 40 px module, horizon at 30% h
- **الدليل / proof:** `style:pm-pankajkumar-dev-0bee87`

#### 3D-181 · موجة مكعبات متساوية القياس · Isometric extruded-cube wave · 👁 شوهد في فيديو
- **ماذا / what:** grid ~16x16 of boxes in orthographic isometric view; height = sin(dist - t) + noise; a few lime caps as accents; red sides, white tops
- **أرقام / params:** wave speed ~1 cycle/s
- **الدليل / proof:** `style:pm-prasenx-8d9323`

#### 3D-182 · مكعب نصي ثلاثي · Text cube rotation · 👁 شوهد في فيديو
- **ماذا / what:** CSS 3D cube faces with words, rotateY 90° ease-in-out 600ms
- **الدليل / proof:** `style:pm-raphaelaubryy-4b137e`

#### 3D-183 · ثقب أسود بانحناء ضوء محسوب · Ray-marched black hole lensing · 👁 شوهد في فيديو
- **ماذا / what:** Fragment shader integrating light paths in Schwarzschild metric (or approximate bending), sample a thin disk with turbulence texture and background star map
- **أرقام / params:** step 0.05-0.1 r_s, 200-400 steps, disk inner 3 r_s outer 15 r_s
- **الدليل / proof:** `style:pm-rebutonepress-810f78`

#### 3D-184 · حرف ثلاثي مبثوق · Extruded 3D letter · 👁 شوهد في فيديو
- **ماذا / what:** stacked offset layers or Three TextGeometry, rotate Y
- **الدليل / proof:** `style:pm-reflex-cloud-72ffe5`

#### 3D-185 · أرضية شطرنج · Perspective checker floor · 👁 شوهد في فيديو
- **ماذا / what:** rotateX 70 plane scrolling
- **الدليل / proof:** `style:pm-safarkhanshuvo-ffd52d`

#### 3D-186 · كلمة مجسمة ثلاثية الأبعاد · 3D extruded word · 👁 شوهد في فيديو
- **ماذا / what:** TextGeometry with depth, cream face, orange sides, rotate from -30° Y with tilt and drop shadow
- **أرقام / params:** depth 0.3 em, 900 ms easeOutCubic
- **الدليل / proof:** `style:pm-sahildesigner23-ee3155`

#### 3D-187 · تموج مكعبات حلقي · Voxel ring ripple · 👁 شوهد في فيديو
- **ماذا / what:** Instanced cubes in grid; colour/height driven by concentric ring function of radius - time
- **أرقام / params:** ring speed 3 u/s, accent cells random 5%
- **الدليل / proof:** `style:pm-sahildesigner23-ee3155`

#### 3D-188 · كرة كروم عاكسة · Chrome sphere env-map · 👁 شوهد في فيديو
- **ماذا / what:** Three.js MeshStandard metalness 1 roughness 0.05, env map, red rim light
- **الدليل / proof:** `style:pm-samuel-spitz-974923`

#### 3D-189 · جولة تكبير عبر مستويات المقياس · Scale-zoom chaptered 3D tour · 👁 شوهد في فيديو
- **ماذا / what:** Three.js scene per level; tween camera position/target 2.5 s easeInOutCubic between chapter waypoints
- **أرقام / params:** 11 chapters
- **الدليل / proof:** `style:pm-sayan-shanky-f850d8`

#### 3D-190 · عرض مفكك للعتاد · Exploded hardware view · 👁 شوهد في فيديو
- **ماذا / what:** offset child meshes along normal 0→1 with ease
- **الدليل / proof:** `style:pm-sayan-shanky-f850d8`

#### 3D-191 · كرة نقاط ثلاثية مع مدارات · 3D point sphere with orbits · 👁 شوهد في فيديو
- **ماذا / what:** Fibonacci-sphere points projected in perspective, rotated; tilted ellipses as orbits with small moving dots
- **أرقام / params:** ~800 points; rotate 40°/s
- **الدليل / proof:** `style:pm-shinskinakamoto-20190b`

#### 3D-192 · حقل أعمدة ثلاثية الأبعاد · Extruded column field · 👁 شوهد في فيديو
- **ماذا / what:** instanced boxes on a grid; heights driven by noise/wave; random tiles recoloured red/blue; perspective camera with depth of field and a bouncing glossy sphere
- **أرقام / params:** grid 30x20, wave period ~1 s, DOF focus on sphere
- **الدليل / proof:** `style:pm-shneural-2abdfa`

#### 3D-193 · زر ثلاثي الأبعاد سينمائي · Cinematic 3D product button · 👁 شوهد في فيديو
- **ماذا / what:** Low-angle shot of an arcade button box with red/blue rim lights, cursor presses it, button depresses with flash
- **أرقام / params:** press 150 ms, rim lights complementary
- **الدليل / proof:** `style:pm-spearwtf-3c1fd1`

#### 3D-194 · حلقة جزيئات · Particle torus · 👁 شوهد في فيديو
- **ماذا / what:** points on torus param, perspective project, rotate on X/Y
- **أرقام / params:** ~2000 pts
- **الدليل / proof:** `style:pm-stephanlivera-df17a2`

#### 3D-195 · خريطة حرارية من مكعبات ثلاثية الأبعاد · Isometric cube heatmap · 👁 شوهد في فيديو
- **ماذا / what:** Three.js InstancedMesh grid 24x16 of boxes in orthographic/isometric view; scale.y animates to data with staggered spring; colour by height (grey -> yellow -> red)
- **أرقام / params:** stagger by distance from hotspot 10 ms, overshoot 1.1
- **الدليل / proof:** `style:pm-sudeepsd-1a3485`

#### 3D-196 · كرة نقاط ثلاثية · 3D point sphere · 👁 شوهد في فيديو
- **ماذا / what:** fibonacci sphere points, rotate Y, perspective size
- **الدليل / proof:** `style:pm-sudo-kiran-49176d`

#### 3D-197 · أرضية شبكة منظورية نيون · Neon perspective grid stage · 👁 شوهد في فيديو
- **ماذا / what:** CSS 3D rotateX(70deg) grid lines fading to horizon on navy
- **أرقام / params:** line alpha 0.15
- **الدليل / proof:** `style:pm-sudo-kiran-4f8b59`

#### 3D-198 · جدار بطاقات مائل · Tilted card wall · 👁 شوهد في فيديو
- **ماذا / what:** grid of thumbnails rotated in 3D, dimmed, big headline overlay
- **أرقام / params:** rotateX 30 rotateZ -10, slow pan
- **الدليل / proof:** `style:pm-sudo-kiran-4f8b59`

#### 3D-199 · مستندات طافية · Floating 3D documents · 👁 شوهد في فيديو
- **ماذا / what:** CSS 3D planes drifting with depth blur
- **الدليل / proof:** `style:pm-sudo-kiran-b055de`

#### 3D-200 · تموّج أعمدة ثلاثية الأبعاد · Isometric voxel ripple · 👁 شوهد في فيديو
- **ماذا / what:** InstancedMesh boxes on a grid, height = A·max(0, sin(r·f − t·ω)) ; randomly colour tops orange/blue/white; isometric camera
- **أرقام / params:** grid 40×40, A 3 units, ω 4 rad/s, soft shadows
- **الدليل / proof:** `style:pm-tequilafunks-97f6c9`

#### 3D-201 · طارة سلكية تتحول لمجسم مع كلمات مدارية · Wireframe-to-shaded torus with orbit words · 👁 شوهد في فيديو
- **ماذا / what:** Generate torus mesh (~420 faces), rotate it, render first as wireframe then flat-shaded stripes with painter's algorithm; place words on a 3D ring around it, depth-scaled; add leader-line callout 'MES
- **كيف / how:** Generate torus mesh (~420 faces), rotate it, render first as wireframe then flat-shaded stripes with painter's algorithm; place words on a 3D ring around it, depth-scaled; add leader-line callout 'MESH_01 · TORUS'
- **أرقام / params:** rotation ~90 deg/s, 2-colour stripe shading
- **الدليل / proof:** `style:pm-teslachartz-c58b32`

#### 3D-202 · صخور عائمة إجرائية · Procedural floating rock spires · 👁 شوهد في فيديو
- **ماذا / what:** displaced cylinders/cones with noise and vertical striation shader, tapered bottoms, scattered at depth with fog
- **أرقام / params:** volumetric fog density 0.02
- **الدليل / proof:** `style:pm-theparuchh-6e08c3`

#### 3D-203 · حلقة سلكية ثلاثية · Wireframe torus · 👁 شوهد في فيديو
- **ماذا / what:** Line-mesh torus rotating with dashed orbit ellipse and accent dots
- **الدليل / proof:** `style:pm-tolgayhickiran-e90799`

#### 3D-204 · كرة نقاط · Dot sphere 3D · 👁 شوهد في فيديو
- **ماذا / what:** Fibonacci sphere, rotateY, size by z
- **أرقام / params:** 800 dots
- **الدليل / proof:** `style:pm-topi-003-9ca6b5`

#### 3D-205 · شريط بطاقات منحني · Curved 3D card carousel · 👁 شوهد في فيديو
- **ماذا / what:** cards placed on cylinder (rotateY step, translateZ r), rotate group, floor reflection
- **أرقام / params:** r~900px
- **الدليل / proof:** `style:pm-twoclipping-6dd14e`

#### 3D-206 · سطح موجي من الجسيمات · Particle sine-wave surface · 👁 شوهد في فيديو
- **ماذا / what:** project a grid of points z = sin(x*k+t)+cos(y*k2+t) with simple perspective; points coloured white with red/yellow accents
- **أرقام / params:** grid 60x30, perspective tilt 60°
- **الدليل / proof:** `style:pm-vanshwtfff-db0466`

#### 3D-207 · بطاقات عائمة حول العنوان · Floating cards around headline · 👁 شوهد في فيديو
- **ماذا / what:** 4-6 screenshot cards placed at screen edges with slight rotation and shadow, drifting slowly in opposite directions while headline sits centre
- **أرقام / params:** drift 20-40 px over 4 s, rotation ±6°
- **الدليل / proof:** `style:pm-viktoroddy-98c1d8`

#### 3D-208 · تحويل الشبكة إلى مجسمات · 2D→3D extrusion · 👁 شوهد في فيديو
- **ماذا / what:** Three.js extrude shapes on plane, camera tilts to iso
- **الدليل / proof:** `style:pm-web3wesley-7bb108`

#### 3D-209 · فقاعات ميتابول · Metaball blobs · 👁 شوهد في فيديو
- **ماذا / what:** SDF spheres smooth-union, orange-blue gradient shading
- **أرقام / params:** k=0.5
- **الدليل / proof:** `style:pm-zaqailo-212ad3`

#### 3D-210 · فقاعات زجاجية كاسرة · Refractive glass blobs · 👁 شوهد في فيديو
- **ماذا / what:** Three.js MeshPhysical transmission 1 over text plane
- **الدليل / proof:** `style:pm-zheke-38deff`

#### 3D-211 · نافذة واجهة مائلة بمنظور حقيقي · Perspective-tilted UI window with camera keys · 👁 شوهد في فيديو
- **ماذا / what:** wrapper perspective 1600px; window rotateX 12deg rotateY -18deg translateZ; interpolate camera keyframes with smooth easing; glowing gradient layer behind window for neon rim; internal UI stages anima
- **كيف / how:** wrapper perspective 1600px; window rotateX 12deg rotateY -18deg translateZ; interpolate camera keyframes with smooth easing; glowing gradient layer behind window for neon rim; internal UI stages animate progress bars sequentially
- **أرقام / params:** rotate 8-20deg, orbit over ~6 s
- **الدليل / proof:** `style:product`

#### 3D-212 · تحويلات ثلاثية الأبعاد بالـCSS · CSS 3D card transforms · 📄 موصوف
- **ماذا / what:** Perspective rotations for product reveals and card flips without WebGL.
- **كيف / how:** parent perspective 900px; child transform-style preserve-3d; back face rotateY(180deg); tl.to(card,{rotationY:360, rotationX:15, duration:1.2, ease:'sine.inOut'}); tilt effect rotateY(x*10deg) rotateX(-y*10deg).
- **أرقام / params:** perspective 900px; tilt 10deg
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/animation-patterns.md`

#### 3D-213 · S13 عمق هندسي 2.5D · S13 Dimensional geometry 2.5D · 📄 موصوف
- **ماذا / what:** Spaced layers, ordered shadows, consistent perspective; components separate and rearrange, limited rotation only when the asset allows. Explains structure visually; one photo has no back side - real 3D needs a model or more shots.
- **كيف / how:** CSS 3D (perspective, translateZ) layer stacks or three.js (CDN) for true geometry; KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg)
- **أرقام / params:** cost medium-high; MG-031 MG-039 MG-048 MG-074 MG-082 MG-087 MG-116
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### 3D-214 · MG-031 انفجار مكونات مرتب · MG-031 Ordered exploded view · 📄 موصوف
- **ماذا / what:** Product parts move apart vertically with short labels and then return.
- **كيف / how:** 0-1 s product, 1-3 s explode, 3-5 s labels, 5-7 s reassemble; independent layers with synced transforms and leader lines. Never invent internal parts or functions. Local: separated PNG layers in an HTML stack.
- **أرقام / params:** 7 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-product-ads.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### 3D-215 · MG-056 صورة ثابتة بعمق طبقات · MG-056 Still photo with layered depth · 📄 موصوف
- **ماذا / what:** Foreground, subject and background of an archive photo move at different rates during a slow push-in.
- **كيف / how:** 0-1 s hold, 1-6 s depth move, 6-8 s stop; cut and stack layers in 2.5D with a limited camera. Large moves reveal missing pixels - stay inside cut boundaries or inpaint. Local: CSS perspective + translateZ per layer in KOSIF.
- **أرقام / params:** 8 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### 3D-216 · قواعد عرض العوالم ثنائية الأبعاد المتعددة الطبقات · Layered 2D world presentation rules · 📄 موصوف
- **ماذا / what:** In layered 2D/2.5D scenes keep one pixel density and filtering, order depth (Y-sort) deliberately, use parallax and occluders on purpose, keep logical positions independent of decorative offsets; give surfaces distinct finishes (rough, satin, glossy, emissive) instead of one; keep post effects restr…
- **كيف / how:** HTML/canvas layers with per-layer parallax factor; image-rendering:pixelated for pixel art; KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg).
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4175-game-world-building/SKILL.md`

#### 3D-217 · فحوص محاذاة الكرة الأرضية · Globe and coordinate alignment checks · 📄 موصوف
- **ماذا / what:** When textures, markers and camera share a globe, mismatched longitude origins put cities in the wrong place.
- **كيف / how:** Record longitude origin and wrap policy, verify at least a few known places on the texture vs marker layer, use shortest-path rotation when the camera moves between far points (avoid spinning the long way), unwrap longitudes across the antimeridian before smoothing paths.
- **أرقام / params:** >=3 known-place spot checks
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/source-method-and-coordinate-ledger.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/assets/flight-path.ts`

#### 3D-218 · متى يكون البعد الثالث مبررا · When 3D is justified · 📄 موصوف
- **ماذا / what:** Depth only when z, terrain, volume, occlusion or a camera move reveals structure that 2D hides; otherwise flat beats 3D.
- **كيف / how:** Use 3D for point clouds, surfaces, terrain, trajectories, globe context; orthographic projection for chart-like 2.5D; perspective only when depth cues matter; every 3D shot needs static key frames that still prove the claim.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/when-3d-is-justified.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/SKILL.md`

#### 3D-219 · إضاءة سينمائية ثلاثية · Cinematic 3D lighting recipe · 📄 موصوف
- **ماذا / what:** One key light, one direction, defined Kelvin; primitives + seeded InstancedMesh crowds; Standard/Physical + PMREM env; custom shaders only for sky/water.
- **كيف / how:** Post: moderate Bloom, ACES, vignette, light grain; one camera move per shot as function of t.
- **أرقام / params:** <150k visible tris
- **الدليل / proof:** `100-superskills/skills/cinematic-3d-scene/SKILL.md`

#### 3D-220 · قاعدة الاختيار بين 3D الحقيقي و2.5D · Real 3D vs 2.5D decision rule · 📄 موصوف
- **ماذا / what:** Use true 3D only when the camera must travel around/through objects (turntables, fly-throughs, worlds); otherwise fake depth with layered planes.
- **كيف / how:** Decide in PLAN.md; 2.5D = DOM/Canvas layers at depth factors; 3D = Three.js seek scene or @remotion/three.
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:9` · `kosif-tool/playbooks/3d.md:86`

#### 3D-221 · بناء أيزومتري بموجة قطرية · Isometric build wave · 📄 موصوف
- **ماذا / what:** Tiles rise in a diagonal wave, buildings extrude, then small agents walk paths.
- **كيف / how:** Per-tile delay by (i+j).
- **أرقام / params:** 40 ms per tile; 300 ms per building extrude
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:44`

#### 3D-222 · منصة عمق 2.5D · 2.5D CSS depth rig · 📄 موصوف
- **ماذا / what:** perspective + translateZ per layer with pre-scale; small rotations.
- **كيف / how:** perspective:1200px; pre-scale (1200−z)/1200.
- **أرقام / params:** bg −400, mid −120, subject 0, occluder +200; rotateY ≤ 6°, rotateX ≤ 4°; 8° orbit 2000–3000 ms sine
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:36`

#### 3D-223 · بطاقة مدارية 2.5D · 2.5D orbit card · 📄 موصوف
- **ماذا / what:** Rig rotates −4°→+4° with foreground occluder passing; caption pill on subject plane.
- **أرقام / params:** 500–3000 ms easeInOutSine; pill spring 16/140; settle +2° push 1.04
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:86-93`

#### 3D-224 · أجسام حجمية بالأشعة · Raymarched volumetrics · 💡 فكرة
- **ماذا / what:** SDF raymarching for clouds, smoke and metaballs inside a full-screen shader.
- **كيف / how:** Fragment loop ~64-128 steps, accumulate density from FBM; keep loops bounded.
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md` · `kosif-atlas/skills/2199-lvtd-skills/8087-game-sdf-and-field-modeling/SKILL.md`

#### 3D-225 · وصف مشهد مجرة المراجعة ثلاثي الأبعاد · Three.js audit galaxy scene descriptor · 💡 فكرة
- **ماذا / what:** Declarative plan for a cinematic 3D scene: interactive perspective camera with mouse tracking, a central 'financial core' sphere, an orbital 'risk radar' network and evidence node cloud, with hover-reveal, click-inspect and evidence-path tracing.
- **كيف / how:** Only a JS config object exists; Claude would have to implement it (e.g. three.js PerspectiveCamera + SphereGeometry + instanced nodes + line paths) from scratch.
- **أرقام / params:** objects: sphere, orbital-network, nodes; camera perspective, mouseTracking true
- **الدليل / proof:** `kosif-audit-studio/cinema/threeAuditScene.js` · `kosif-audit-studio/docs/CINEMA_AUDIT_EDITION.md`

#### 3D-226 · دوران 15 درجة · Single 15° grid orbit · 💡 فكرة
- **ماذا / what:** One CSS-3D orbit of the grid plane during a kinetic burst.
- **كيف / how:** perspective + rotateY on stage.
- **أرقام / params:** 15°, once
- **الدليل / proof:** `style:pm-ajith-io-ea7f2d`

#### 3D-227 · ممر كلمات · Corridor of oversized words · 💡 فكرة
- **ماذا / what:** Camera dollies down a corridor built of huge words.
- **كيف / how:** CSS 3D / three.js text planes.
- **الدليل / proof:** `style:pm-itisrazak-3ad902`

#### 3D-228 · كاميرا مشي · First-person walk camera · 💡 فكرة
- **ماذا / what:** Walk with head bob, fixed FOV, no cuts.
- **كيف / how:** three.js camera.
- **أرقام / params:** 1.4 m/s; bob 2 cm @1.8 Hz; FOV 70°
- **الدليل / proof:** `style:pm-mandelduck-95fd08`

#### 3D-229 · كشف القطة · Hidden-object reveal with chime · 💡 فكرة
- **ماذا / what:** Hint (tail flick 2-4 s, glint 120 ms within 20 m), then pop with sparkle and Web Audio chime.
- **كيف / how:** scale 0.8→1.0 cubic-bezier(0.34,1.56,0.64,1).
- **أرقام / params:** 350 ms; 3-stroke sparkle
- **الدليل / proof:** `style:pm-mandelduck-95fd08`

#### 3D-230 · مدار وبارالاكس · Orbit + two-layer parallax · 💡 فكرة
- **ماذا / what:** parallax 0.6/1.0; 15° orbit; easeInOutCubic 1500-2500 ms
- **الدليل / proof:** `style:pm-xelandre-363f00`
