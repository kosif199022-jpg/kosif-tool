# الملمس والخامات — Texture & material

> فصل مُجمَّع آليًا من 163 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **158 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 158 powers deduplicated by name from 163 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 8 · 🟢 جاهز 32 · 📦 بأمر تثبيت 55 · 👁 شوهد في فيديو 46 · 📄 موصوف 14 · 💡 فكرة 3

#### TEX-01 · قفل خلفية ورقية · Paper sketch background lock · ✅ مُثبت هنا
- **ماذا / what:** Flat hand-drawn paper/whiteboard background with sketched props and no photoreal depth, matching the 2D figure.
- **كيف / how:** BACKGROUNDS.paper block repeated in all 5 prompts.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/stickman.mjs:4`

#### TEX-02 · قفل أسلوب الأرشيف · Archival scrapbook style lock · ✅ مُثبت هنا
- **ماذا / what:** Vintage mixed-media documentary look: sepia newspaper, film grain, scan lines, halftone, warped corners, torn photo cutouts with white borders, label stickers, brass tacks, red thread, generic ARCHIVE stamps, projector flicker and dust/scratch overlays; fast stop-motion entrances.
- **كيف / how:** STYLE constant in every vox clip prompt.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/vox-history.mjs:11` · `fastify-motion-bro/skills/vox-history/SKILL.md:12`

#### TEX-03 · بقع لونية على المجسم · Colour paint stamps on SDF · ✅ مُثبت هنا
- **ماذا / what:** Soft spherical/ellipsoidal colour stamps (blush, belly patch) with no geometry.
- **كيف / how:** S.paint(c, r, colour, {soft, radii, amount, rot}).
- **أرقام / params:** soft default r*0.5; amount 1
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:98`

#### TEX-04 · ستايل البطة ضد التنين · Duck vs Dragon epic still (style) · ✅ مُثبت هنا
- **ماذا / what:** A 16:9 heroic fantasy still: a white duck in a gold helmet and red scarf charging a giant green dragon breathing fire over a broken stone bridge above lava, storm sky with lightning, embers and smoke, heavy vignette.
- **كيف / how:** Pure-Python SVG generator (no deps), seeded random, every element as path/gradient/filter strings; convert SVG to PNG/video frames with a browser or rsvg if needed.
- **أرقام / params:** 1600x900, seed 7, ~173 paths, 113 circles, 10 linear + 4 radial gradients, 3 blur filters
- **الدليل / proof:** `kosif-one/projects/duck-vs-dragon/duck_dragon.py` · `kosif-one/projects/duck-vs-dragon/duck_dragon.svg`

#### TEX-05 · نسيج الحراشف · Scale texture pattern · ✅ مُثبت هنا
- **ماذا / what:** Reptile scales as a tiling SVG pattern of arcs overlaid on the gradient-filled body.
- **كيف / how:** <pattern id=scales width=22 height=16 patternUnits=userSpaceOnUse> with arc paths; fill the body path twice: gradient then url(#scales).
- **أرقام / params:** tile 22x16, stroke #052e16 1.6 op .55 + #4ade80 1 op .25
- **الدليل / proof:** `kosif-one/projects/duck-vs-dragon/duck_dragon.py:57-60` · `kosif-one/projects/duck-vs-dragon/duck_dragon.py:98-99`

#### TEX-06 · نسيج الضوضاء الكسرية · Fractal value-noise texture · ✅ مُثبت هنا
- **ماذا / what:** Seeded multi-octave value noise inside a shape that the eye reads as material: skin, rock, water streaks, fur, fog.
- **كيف / how:** noise(shape, amount, cell, seed, mode='multiply'|'normal'|'add'|'screen', colour, octaves=4, stretch=(sx,sy)).
- **أرقام / params:** presets from the guide: skin cell 10-14 multiply; water stretch (6,1); cloud cell 60 + blur; rock cell 26 + cold rim; sky 160 multiply .35
- **الدليل / proof:** `kosif-studio/render.py:480` · `kosif-studio/render.py:496` · `kosif-studio/references/drawing-guide.md:62`

#### TEX-07 · نقش الحراشف والقرميد · Scales / tiles pattern · ✅ مُثبت هنا
- **ماذا / what:** Staggered overlapping arcs clipped to a shape: reptile scales, fish skin, roof tiles.
- **كيف / how:** scales(shape, size=14, colour, alpha=.35, width=1, stagger=True); put over shade() or relief().
- **أرقام / params:** row step size*.55; dragon hide size 8 alpha .22 width .8
- **الدليل / proof:** `kosif-studio/render.py:539` · `kosif-studio/scenes/whale_dragon.py:164`

#### TEX-08 · حبيبات الفيلم · Film grain · ✅ مُثبت هنا
- **ماذا / what:** Seeded Gaussian luminance grain over the whole frame.
- **كيف / how:** grain(amount, seed).
- **أرقام / params:** typical .012-.02 (whale .018, duck .02, ad .012)
- **الدليل / proof:** `kosif-studio/render.py:791`

#### TEX-09 · فرو بالطبقات · Shell fur · 🟢 جاهز
- **ماذا / what:** Layered shell copies pushed along normals with dot alpha maps; roots darker, gravity on outer shells.
- **كيف / how:** Load lab-kit.js after the bundle; K3.makeFur(mesh, {layers, length, repeat, color, rootShade, gravity, density, seed}).
- **أرقام / params:** layers 10 (8-12 at 540p, 16 at 1080p); length .12; repeat 14; rootShade .72; gravity .35; alphaTest .1->.78; default colour #a7ff2a
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:28` · `kosif-one/tools/kosif-studio/motion/kit/lab-kit.js:28` · `kosif-studio/motion/kit/lab-kit.js:28`

#### TEX-10 · ضجيج إجرائي · Seeded CPU noise (perlin / fbm / ridged) · 🟢 جاهز
- **ماذا / what:** Deterministic 2D Perlin, fractal Brownian motion and ridged noise for terrain, textures and placement.
- **كيف / how:** Load assets/three-kit.bundle.js (window.K3, three.js r186) or import from three-kit.js; K3.perlin(x,y), K3.fbm(x,y,oct,lac,gain), K3.ridged(x,y,oct); helpers smooth/ramp/clamp01/lerp.
- **أرقام / params:** perm seed 1337; fbm oct 5 lac 2.0 gain 0.5; ridged lac 2.1 gain .5
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:24` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:29` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:34` · `kosif-studio/motion/kit/three-kit.js:24`

#### TEX-11 · سطح زجاجي مركب · Composed glass surface · 🟢 جاهز
- **ماذا / what:** Frosted panels as a layered material: backdrop blur, faint white fill, gradient top-lit border, diffuse ambient shadow; only on dark backgrounds.
- **كيف / how:** CSS backdrop-filter + border-image gradient + large soft box-shadow. Rendered fine in Chromium headless.
- **أرقام / params:** blur 28px standard / 40px spotlight; fill rgba(255,255,255,0.05); border 0.12->0.02 gradient; shadow 0 24px 80px rgba(0,0,0,0.25)
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`

#### TEX-12 · خلفيات تدرج شبكي وشبكة خطوط · Layered mesh-gradient and grid backgrounds · 🟢 جاهز
- **ماذا / what:** Atmospheric backgrounds from stacked radial gradients, a faint 1px grid, or inline SVG noise; or GPU mesh gradients behind crisp UI.
- **كيف / how:** CSS: two ellipse radial-gradients at 20%/80% and 80%/20% over a base; grid via two linear-gradients; GPU option @paper-design/shaders-react MeshGradient (Apache-2.0, npm) behind a z-index:1 UI layer with pointer-events none and a static CSS fallback.
- **أرقام / params:** radials alpha 0.3/0.2 ending 50%; grid rgba(255,255,255,0.03) 1px, 50px cells; mesh colors e.g. #00F0FF/#7000FF/#000 drifting slowly
- **الدليل / proof:** `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/animation-patterns.md` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion` · `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/references/shader-backed-ui.md`

#### TEX-13 · حبيبات فيلم وانحراف لوني على الحواف · Film grain and edge chromatic aberration · 🟢 جاهز
- **ماذا / what:** Monochrome animated grain removes digital banding; a tiny RGB split only near frame edges imitates a lens.
- **كيف / how:** Grain: per-frame noise canvas or SVG feTurbulence overlay with seed = frame; aberration as a post pass offsetting R/B by distance from centre.
- **أرقام / params:** grain opacity 0.02 (never > 0.03); RGB shift 0.002 at edges only
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`

#### TEX-14 · فحص قابلية التكرار للخامات المولدة · Tileable texture check for AI textures · 🟢 جاهز
- **ماذا / what:** Models are bad at seamless tiling, so generated textures must be measured and fixed before use as backgrounds.
- **كيف / how:** Compute seam differences and preview 2×2; a seam score over 2 shows as grid lines — mirror-blend edges or tile manually; fit backdrops to drawn size (e.g. width 1024, ≤250 KB), JPEG/WebP for pictures, PNG only for alpha sprites.
- **أرقام / params:** seam >2 visible; 1024 px; ≤250 KB
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3889-art`

#### TEX-15 · أسطح زجاجية ضبابية · Glassmorphism surfaces · 🟢 جاهز
- **ماذا / what:** Translucent sticky bars, dialogs and panels with background blur over colour washes.
- **كيف / how:** background: color-mix(in srgb, var(--card) 92-96%, transparent) + backdrop-filter: blur(12-20px); dialog ::backdrop blur 3-7px.
- **أرقام / params:** topbars blur 12/16/18/20px; studio dialog radius 22px shadow 0 30px 100px #15111a45; cinema panel rgba(15,23,42,.78) blur 18px
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:308` · `kosif-audit-studio/studio.css:117` · `kosif-audit-studio/cinema/cinemaTheme.css`

#### TEX-16 · طبقة حبيبات نقطية · Dot-grain overlay texture · 🟢 جاهز
- **ماذا / what:** A subtle dot lattice over the dark hero gives a printed/film-grain feel without images.
- **كيف / how:** ::after inset 0, background-image radial-gradient(#ffffff16 .6px, transparent .6px), background-size 6px 6px, opacity .25, pointer-events none.
- **أرقام / params:** dot .6px; grid 6px; opacity 0.25
- **الدليل / proof:** `kosif-audit-studio/studio.css:58`

#### TEX-17 · غلاف زجاجي فوق خلفية ثلاثية الأبعاد · Glass shell over a live 3D background · 🟢 جاهز
- **ماذا / what:** UI card floats as frosted glass above the full-screen WebGL world; glass is used only over dark/animated backdrops.
- **كيف / how:** .world fixed inset 0, opacity 0 -> 1 over 1.6s; .shell background rgba(255,253,249,.96) + backdrop-filter blur(14px); visual panel gradient 180deg rgba(29,24,20,.12)->.58 with saffron wash 160deg rgba(217,83,14,.26).
- **أرقام / params:** blur 14px; alpha .96 (.94 phone); fade 1.6s
- **الدليل / proof:** `kosif-earth-ci-fork/unlock.html:75` · `kosif-earth-ci-fork/docs/design/SQC-IDENTITY-ar.md`

#### TEX-18 · وصفات الزجاج للقوائم والتنبيهات · Glassmorphism recipes (menus, toasts, top bar) · 🟢 جاهز
- **ماذا / what:** Translucent surfaces with saturation-boosted background blur for dropdowns, tooltips, toasts and a sticky top bar.
- **كيف / how:** backdrop-filter:saturate(180%) blur(24px) (dropdown, radius 24px); blur(20px) tooltip; saturate(180%) blur(22px) toast; top bar color-mix(surface 92%) + saturate(1.4) blur(10px); modal scrim rgba(0,0,0,.32) blur(6px).
- **أرقام / params:** blur 6/10/20/22/24px; saturate 140-180%
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/components.css:196` · `kosif-earth-ci-fork/ui/ds/components.css:224` · `kosif-earth-ci-fork/ui/ds/components.css:282`

#### TEX-19 · ظلال الارتفاع الناعمة المتعددة · Layered soft elevation shadows · 🟢 جاهز
- **ماذا / what:** Three-level shadow tokens built from a hairline contact shadow plus a large negative-spread ambient shadow tinted with the brand dark.
- **كيف / how:** --sk-shadow-1/2/3 per look.
- **أرقام / params:** cobalt: 0 1px 2px rgba(11,16,48,.05),0 12px 32px -24px rgba(11,16,48,.36) / 0 18px 40px -22px rgba(11,16,48,.32) / 0 32px 80px -28px rgba(11,16,48,.48); ledger uses rgba(29,24,20,.05/.30/.26/.40)
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/tokens.css:184` · `kosif-earth-ci-fork/docs/design/SQC-IDENTITY-ar.md`

#### TEX-20 · سحب SVG إجرائية · Procedural SVG clouds (feTurbulence) · 🟢 جاهز
- **ماذا / what:** Soft cumulus built from plain ellipses distorted by fractal noise and blurred, over a vertical sky gradient and radial sun glow - a 2.6 KB vector replacement for a raster sky.
- **كيف / how:** filter: feTurbulence type=fractalNoise baseFrequency .011 numOctaves 5 seed 11 -> feDisplacementMap scale 70 (R/G) -> feGaussianBlur 5; far layer .009/4 octaves/scale 55/blur 12; sky gradient #f1e3bf .3 #d4b06a .62 #f2732d 1 #1d1814; sun radial cx .62 cy .18.
- **أرقام / params:** viewBox 800x600; preserveAspectRatio xMidYMid slice
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/kosif-sky.svg` · `kosif-earth-ci-fork/docs/design/KOSIF-LUXE.md`

#### TEX-21 · شبكة نقطية دقيقة · Fine dot-dash modular grid · 🟢 جاهز
- **ماذا / what:** Low-contrast stationary grid of tiny dashes giving an editorial paper feel without diagonals.
- **كيف / how:** vertical dashes every 0.10w from 0.07w, step 0.051h, length 2*scale; horizontal dashes same; stroke grid colour at 55% alpha, width max(.5, .7*scale).
- **أرقام / params:** spacing 10% width x 5.1% height
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:43-46`

#### TEX-22 · نقاط هافتون على القصاصة · Halftone dot texture on cutout · 🟢 جاهز
- **ماذا / what:** Clipped halftone dots on the hero card to imitate print/cutout texture.
- **كيف / how:** clip to card rect; dots every 10*scale px where (floor(x/10s)+floor(y/10s))%4==0, radius 1.7*scale, text colour at 8% alpha.
- **أرقام / params:** 10 px cell; r 1.7 px; 8% alpha
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:63-66`

#### TEX-23 · حشو الحروف بخامات (66 قناعا) · Texture-mask letter fills (66 PBR masks) · 🟢 جاهز
- **ماذا / what:** 66 luminance texture masks (masonry, stone, ground/road, metal, wood, fabric, grass, snow, lava...) derived from ambientCG PBR color maps that cut texture through letterforms.
- **كيف / how:** Use held-text-strobe-burst assets or `npx hyperframes add texture-mask-text`.
- **أرقام / params:** 66 PNG masks
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/templates/held-text-strobe-burst/assets/texture-mask-text/masks/lava.png` · `kosif-one/vendor/hyperframes/registry/components/texture-mask-text/registry-item.json`

#### TEX-24 · حبيبات الفيلم · Film grain overlay (2D) · 🟢 جاهز
- **ماذا / what:** SVG fractal-noise grain that jumps in steps (seekable CSS animation) blended over the frame.
- **كيف / how:** MOTION.grain(stage, {opacity, blend, freq, seed, z}).
- **أرقام / params:** feTurbulence fractalNoise baseFrequency 0.9, 2 octaves, desaturated; opacity .09; mix-blend soft-light; 0.6 s steps(1) 6-position jump
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:440`

#### TEX-25 · خامات مولدة · Procedural textures (noiseCanvas / normalFromHeight / spriteTex) · 🟢 جاهز
- **ماذا / what:** Generates canvas textures, normal maps from height functions and soft/ring/streak particle sprites with no downloads.
- **كيف / how:** K3.noiseCanvas(N, (x,y)=>[r,g,b,a]); K3.normalFromHeight(N, h, strength); K3.spriteTex('soft'|'ring'|'streak').
- **أرقام / params:** sprites 128 px; repeat wrapping
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:41` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:48` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:57`

#### TEX-26 · حبيبات فيلم ثلاثي · Film grain pass (3D) · 🟢 جاهز
- **ماذا / what:** three.js FilmPass grain, time-seeded per output frame.
- **كيف / how:** post.film; makeFrameLoop writes film.uniforms.time = t.
- **أرقام / params:** intensity .16 (lab .05)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:402`

#### TEX-27 · حصى · Pebbles / river stones · 🟢 جاهز
- **ماذا / what:** Instanced water-worn stones from noise-deformed icosahedra, clumped into drifts, speckled texture and caustics.
- **كيف / how:** K3.makePebbles({n, region, accept, height, size, flat, clump, seed}).
- **أرقام / params:** n 2400; size .06 m; flat .5; 4 colour families by HSL
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:724`

#### TEX-28 · خامة قطيفة محشوة · Plush / felt velvet material · 🟢 جاهز
- **ماذا / what:** Vertex-coloured physical material with sheen, a fuzz rim in the fabric's own colour and object-space fibre noise (no UVs).
- **كيف / how:** K3S.plushMaterial({fuzz, fibre, fibreScale, sheen, sheenRoughness, sheenColor, fuzzTint, roughness}).
- **أرقام / params:** roughness .82; sheen 1.0; sheenRoughness .42; sheenColor #fff4f6; fuzz .38; fibre .22; fibreScale 520/m
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:286`

#### TEX-29 · خامة لامعة · Glossy clearcoat material · 🟢 جاهز
- **ماذا / what:** Dark glossy clearcoat for eyes and noses.
- **كيف / how:** K3S.glossMaterial(color, {roughness, env}).
- **أرقام / params:** #15100f; roughness .08; clearcoat 1, clearcoatRoughness .04; ior 1.5; envMapIntensity 1.6
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:311`

#### TEX-30 · خامات المختبر · Lab material set (plush/gloss/leather/metal) · 🟢 جاهز
- **ماذا / what:** Quick standard materials for product-lab scenes.
- **كيف / how:** K3.plushMaterial(c), K3.glossMaterial(c,{roughness}), K3.leatherMaterial(c), K3.metalMaterial(c).
- **أرقام / params:** plush roughness .95; gloss clearcoat 1 roughness .08; leather #15171a r .55 m .05; metal #d8dde3 r .25 m .95
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:49`

#### TEX-31 · شبكة خطوط قطرية منجرفة · Drifting diagonal line grid backdrop · 🟢 جاهز
- **ماذا / what:** A faint grid of slanted lines plus horizontals that sways gently, giving motion to an empty background.
- **كيف / how:** globalAlpha 0.13, spacing min(w,h)/12; slanted lines from (x + sin(t·0.15)·25, 0) to (x+0.15w, h); horizontals every spacing.
- **أرقام / params:** alpha 0.13; sway ±25 px at 0.15 rad/s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:66`

#### TEX-32 · انعكاسات الشارع المبتل · Wet street reflections · 🟢 جاهز
- **ماذا / what:** A wet road made of broad coloured light pools, perspective paving joints and many short broken horizontal glints, plus a dark rippled mirror copy of the hero.
- **كيف / how:** ground(): street gradient #17343f → #030b16, joints radiating, 85 broken reflection lines; hero reflection = cat drawn with scale(1, −0.25) at opacity 0.085.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:109` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:124`

#### TEX-33 · أفق مدينة ليلي إجرائي · Procedural night skyline with lit windows · 🟢 جاهز
- **ماذا / what:** Background city blocks of random heights with randomly lit windows in two tones, generated once from a deterministic hash.
- **كيف / how:** skyline(): 30 towers, height 105–340, width 62–108, windows 3.5×6 lit if rnd > .43 (#4b99a2 or #9c976e, opacity .15–.55); architecture(): 12 mid buildings 200 px wide with 23×28 windows lit if rnd > .37.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:31` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:33`

#### TEX-34 · شارة زجاجية ضبابية · Glassmorphism badge · 🟢 جاهز
- **ماذا / what:** Frosted-glass pill label over a 3D scene.
- **كيف / how:** CSS: background rgba(255,255,255,.08); backdrop-filter blur(12px); border 1px rgba(255,255,255,.15); border-radius 9999px; color #38bdf8; box-shadow 0 8px 32px rgba(56,189,248,.2).
- **أرقام / params:** padding 12x28px, 24px/600, letter-spacing 1px, blur 12px
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:34`

#### TEX-35 · حبيبات فيلم · Seekable film grain overlay · 🟢 جاهز
- **ماذا / what:** Fractal-noise grain as an SVG overlay that jumps in steps (seekable CSS), soft-light blended.
- **كيف / how:** MOTION.grain(stage, {opacity, blend, freq, seed}).
- **أرقام / params:** opacity 0.09, soft-light, baseFrequency 0.9, 2 octaves, 0.6 s steps(1)
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:440`

#### TEX-36 · حصى وقصب · Pebbles and reed blades · 🟢 جاهز
- **ماذا / what:** Instanced water-worn pebbles (deformed icosahedra, caustics included) and tapered grass/reed blades with sway.
- **كيف / how:** makePebbles({n, region, accept, seed}); makeBlades({n, region, tall, width, seed}).
- **أرقام / params:** pebbles n 2400; blades n 1500, tall 0.9 m
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:724` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:746`

#### TEX-37 · ضوضاء ونسيج مولد · Seeded noise and generated textures · 🟢 جاهز
- **ماذا / what:** CPU Perlin/FBM/ridged noise, canvas textures, normal maps from height and soft/ring/streak sprites: no downloaded textures.
- **كيف / how:** perlin, fbm(x,y,oct,lac,gain), ridged, noiseCanvas(N, fn), normalFromHeight(N, hfn, strength), spriteTex('soft'|'ring'|'streak').
- **أرقام / params:** fbm 5 octaves lacunarity 2 gain 0.5; ridged lacunarity 2.1
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:24` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:41`

#### TEX-38 · خامات القماش واللمعان والعيون · Plush, gloss, eye and tube materials · 🟢 جاهز
- **ماذا / what:** Felt plush material with velvet sheen and fibre noise, glossy material, eyes with two catch-lights, tubes for mouths/stitches.
- **كيف / how:** K3S.plushMaterial(), K3S.glossMaterial(color), K3S.eye({r, tall}), K3S.tube(points, r, colour).
- **أرقام / params:** eye tall 1.12, two catch-lights upper-outer
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/shape-kit.js:286` · `kosif-one/tools/kosif-studio/motion/kit/shape-kit.js:311` · `kosif-one/tools/kosif-studio/motion/kit/shape-kit.js:316`

#### TEX-39 · نسيج ضوضاء كسرية · Fractal noise texture · 🟢 جاهز
- **ماذا / what:** Multiplies fractal value noise into a shape for skin, rock, water or cloud texture.
- **كيف / how:** noise(shape, amount=0.25, cell=24, seed, mode='multiply').
- **أرقام / params:** 4 octaves
- **الدليل / proof:** `kosif-one/tools/kosif-studio/render.py:496`

#### TEX-40 · نقش الحراشف · Scale pattern · 🟢 جاهز
- **ماذا / what:** Draws overlapping scales over a shape (dragons, fish).
- **كيف / how:** scales(shape, size=14, colour, alpha=0.35, width=1.0).
- **الدليل / proof:** `kosif-one/tools/kosif-studio/render.py:539`

#### TEX-41 · نص بقناع خامة · Texture-mask text · 📦 بأمر تثبيت
- **ماذا / what:** Text filled with a texture (e.g. texture-lava) via mask; lint enforces base class and mask asset.
- **كيف / how:** class texture-text + texture-<name>; rules texture_class_unknown, texture_text_missing_mask.
- **تثبيت / install:** `npx hyperframes add texture-mask-text` (copies to compositions/components/texture-mask-text`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/lint/src/rules/textures.ts` · `kosif-one/vendor/hyperframes/registry/components/texture-mask-text/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/texture-mask-text/texture-mask-text.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/texture-mask-text.mdx`

#### TEX-42 · خامة القطيفة · Plush felt material · 📦 بأمر تثبيت
- **ماذا / what:** Velvet sheen, fuzz rim, object-space fibre noise without UVs.
- **كيف / how:** K3S.plushMaterial()
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/shape-kit.md` · `kosif-studio/motion/kit/shape-kit.js:286`

#### TEX-43 · حبيبات الفيلم · Film grain node · 📦 بأمر تثبيت
- **ماذا / what:** Animated noise overlay to kill banding and add filmic texture.
- **كيف / how:** film(color,{intensity,grayscale}) TSL node, or custom hash(uv+time) overlay in GLSL.
- **أرقام / params:** TSL intensity 0.5 default demo; editorial rule: ~2% opacity, never above 3%
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/post-processing.md` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### TEX-44 · زجاج بانكسار وتشتت لوني · Refraction + chromatic dispersion glass · 📦 بأمر تثبيت
- **ماذا / what:** Glass/crystal objects that bend and split the background into rainbow fringes.
- **كيف / how:** FBO of background; refract(eye,normal,1/IOR); per-channel IOR sampling loop; backside pass first for internal dispersion. drei MeshTransmissionMaterial as shortcut.
- **أرقام / params:** IOR 1.31 base; separate IOR per R/G/B
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### TEX-45 · طبقات درجات لمظهر الفرشاة الجافة · Tone layers for dry-brush look · 📦 بأمر تثبيت
- **ماذا / what:** Trace the same drawing at several gray levels and fill each with its median color to capture dry-brush streaks and soft edge ramps.
- **كيف / how:** Multi-threshold contour tracing; fill bottom-up in even-odd; 6 levels gives marginal gain for 1.4x points.
- **أرقام / params:** levels 3-6
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9357-rotoscope`

#### TEX-46 · حبيبات الفيلم · Film grain overlay · 📦 بأمر تثبيت
- **ماذا / what:** Animated film grain from a pre-made noise tile, re-offset every frame.
- **كيف / how:** 192x192 random grey tile -> createPattern; overlay blend at alpha=grain; translated by random 0-192 px each frame (MK.grain uses a deterministic offset at 24 fps for renders).
- **أرقام / params:** grain 0-0.3 (AutoEdit 0-0.7)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:75` · `app/public/js/00_editor.js:288` · `app/public/js/10_studio.js:265`

#### TEX-47 · خلفيات النقشات المتحركة · Animated pattern backgrounds (6) · 📦 بأمر تثبيت
- **ماذا / what:** Six animated procedural backgrounds plus moving gradient and solid colour, all beat-aware.
- **كيف / how:** drawPattern(): aurora (4 screen-blended radial blobs on Lissajous paths, radius 0.5 max(W,H)+beat), grid (spacing 9% m drifting 0.35 sp/s + accent radial), dots (7% grid, size wave sin(d*14-2.2t)), waves (6 layered sine bands amplitude 3.5% H), stars (140 twinkling points + primary horizon glow), rays (14 rotating wedges at 0.08 rad/s); default gradient rotates 0.25 rad/s through bg->primary.
- **أرقام / params:** aurora|grid|dots|waves|stars|rays|gradient|solid
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:2418` · `app/public/js/00_editor.js:2443` · `app/index.html:49`

#### TEX-48 · حقل الحبيبات · Grain Field · 📦 بأمر تثبيت
- **ماذا / what:** Visible accent-tinted dot field drifting over a soft luminance gradient in a seamless loop.
- **كيف / how:** Install with `npx hyperframes add grain-field` (copies to compositions/components/grain-field.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame …
- **أرقام / params:** density fine|coarse; vars: density=fine[fine|coarse]; accent=green[green|blue|violet]
- **تثبيت / install:** `npx hyperframes add grain-field` (copies to compositions/components/grain-field`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/grain-field/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/grain-field/grain-field.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/grain-field.mdx`

#### TEX-49 · حبيبات الفيلم · Grain Overlay · 📦 بأمر تثبيت
- **ماذا / what:** Animated film-grain texture overlay for analogue warmth.
- **كيف / how:** Install with `npx hyperframes add grain-overlay` (copies to compositions/components/grain-overlay.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fr…
- **أرقام / params:** CSS keyframes
- **تثبيت / install:** `npx hyperframes add grain-overlay` (copies to compositions/components/grain-overlay`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/grain-overlay/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/grain-overlay/grain-overlay.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/grain-overlay.mdx`

#### TEX-50 · نزف الحبر · Ink Bleed Reveal · 📦 بأمر تثبيت
- **ماذا / what:** Liquid ink blooms through paper using a gooey blur+threshold filter, merges, then contracts while a crisp slotted mark resolves, with static paper grain.
- **كيف / how:** Install with `npx hyperframes add ink-bleed-reveal` (copies to compositions/components/ink-bleed-reveal.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chrom…
- **أرقام / params:** blobs 5; vars: blobs=5(4..6); accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add ink-bleed-reveal` (copies to compositions/components/ink-bleed-reveal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/ink-bleed-reveal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/ink-bleed-reveal/ink-bleed-reveal.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/ink-bleed-reveal.mdx`

#### TEX-51 · كولاج الورق · Paper Collage Reveal · 📦 بأمر تثبيت
- **ماذا / what:** Torn paper scraps with their own textures and tilts flutter away in a staggered scatter revealing content.
- **كيف / how:** Install with `npx hyperframes add paper-collage-reveal` (copies to compositions/components/paper-collage-reveal.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headle…
- **أرقام / params:** panels 6; tone cream|kraft|mixed; spread outward|scatter; vars: panels=6(4..8); tone=mixed[cream|kraft|mixed]; spread=outward[outward|scatter]
- **تثبيت / install:** `npx hyperframes add paper-collage-reveal` (copies to compositions/components/paper-collage-reveal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/paper-collage-reveal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/paper-collage-reveal/paper-collage-reveal.html` · `kosif-one/vendor/hyperframes/registry/components/paper-collage-reveal/demo.html`

#### TEX-52 · كشف بقناع الكلمة · SVG Mask Reveal · 📦 بأمر تثبيت
- **ماذا / what:** Soft token-coloured sweep reveals media only through an editable SVG wordmark mask.
- **كيف / how:** Install with `npx hyperframes add svg-mask-reveal` (copies to compositions/components/svg-mask-reveal.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **أرقام / params:** featherPx 24; revealProgress 100; vars: text=REVEAL; revealProgress=100(0..100); featherPx=24(0..120)
- **تثبيت / install:** `npx hyperframes add svg-mask-reveal` (copies to compositions/components/svg-mask-reveal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/svg-mask-reveal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/svg-mask-reveal/svg-mask-reveal.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/svg-mask-reveal.mdx`

#### TEX-53 · تمزيق الورق · Torn Paper Rip · 📦 بأمر تثبيت
- **ماذا / what:** Fibrous tear runs across the frame showing white paper core on the edge; sheet lifts away on a soft shadow revealing the next scene.
- **كيف / how:** Install with `npx hyperframes add torn-paper-rip` (copies to compositions/components/torn-paper-rip.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium …
- **أرقام / params:** direction left-to-right|right-to-left; tone cream|kraft|white; roughness 55; vars: direction=left-to-right[left-to-right|right-to-left]; tone=cream[cream|kraft|white]; roughness=55(20..90)
- **تثبيت / install:** `npx hyperframes add torn-paper-rip` (copies to compositions/components/torn-paper-rip`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/torn-paper-rip/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/torn-paper-rip/torn-paper-rip.html` · `kosif-one/vendor/hyperframes/registry/components/torn-paper-rip/demo.html`

#### TEX-54 · كرة كروم · Chrome Orb · 📦 بأمر تثبيت
- **ماذا / what:** Mirror-chrome sphere reflecting a bright studio light. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add chrome-orb` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="Chrome" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="Chrome"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add chrome-orb` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/chrome-orb/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/chrome-orb/chrome-orb.html` · `kosif-one/vendor/hyperframes/registry/blocks/chrome-orb/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### TEX-55 · ضوضاء كسورية · Fractal Noise · 📦 بأمر تثبيت
- **ماذا / what:** Soft grey fractal noise drifting like slow clouds. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add fractal-noise` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="FractalNoise" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="FractalNoise"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add fractal-noise` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/fractal-noise/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/fractal-noise/fractal-noise.html` · `kosif-one/vendor/hyperframes/registry/blocks/fractal-noise/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### TEX-56 · كرة الصقيع · Frost · 📦 بأمر تثبيت
- **ماذا / what:** Blue orb with frost creeping in from its edge. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add frost` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="Frost" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="Frost"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add frost` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/frost/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/frost/frost.html` · `kosif-one/vendor/hyperframes/registry/blocks/frost/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### TEX-57 · ضوضاء غابور · Gabor Noise · 📦 بأمر تثبيت
- **ماذا / what:** Streaky grey noise drifting like a moving fingerprint. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add gabor-noise` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="GaborNoise" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="GaborNoise"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add gabor-noise` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/gabor-noise/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/gabor-noise/gabor-noise.html` · `kosif-one/vendor/hyperframes/registry/blocks/gabor-noise/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### TEX-58 · رقاقة قزحية · Holographic · 📦 بأمر تثبيت
- **ماذا / what:** Iridescent foil orb with shifting rainbow sheen. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add holographic` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="Holographic" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="Holographic"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add holographic` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/holographic/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/holographic/holographic.html` · `kosif-one/vendor/hyperframes/registry/blocks/holographic/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### TEX-59 · معدن سائل · Liquid Metal · 📦 بأمر تثبيت
- **ماذا / what:** Chrome sphere rippling like molten metal. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add liquid-metal` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="LiquidMetal" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="LiquidMetal"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add liquid-metal` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/liquid-metal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/liquid-metal/liquid-metal.html` · `kosif-one/vendor/hyperframes/registry/blocks/liquid-metal/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### TEX-60 · رخام · Marble · 📦 بأمر تثبيت
- **ماذا / what:** Dark veins winding through white marble, slowly shifting. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add marble` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="Marble" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="Marble"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add marble` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/marble/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/marble/marble.html` · `kosif-one/vendor/hyperframes/registry/blocks/marble/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### TEX-61 · زجاج بركاني · Obsidian · 📦 بأمر تثبيت
- **ماذا / what:** Dark glass orb catching pink and cyan iridescence. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add obsidian` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="Obsidian" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="Obsidian"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add obsidian` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/obsidian/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/obsidian/obsidian.html` · `kosif-one/vendor/hyperframes/registry/blocks/obsidian/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### TEX-62 · بلاستيك لامع · Plastic · 📦 بأمر تثبيت
- **ماذا / what:** Glossy white plastic orb with soft studio reflections. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add plastic` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="Plastic" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="Plastic"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add plastic` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/plastic/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/plastic/plastic.html` · `kosif-one/vendor/hyperframes/registry/blocks/plastic/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### TEX-63 · غشاء رقيق · Thin Film · 📦 بأمر تثبيت
- **ماذا / what:** Orb rim shimmering with soap-bubble iridescence. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add thin-film` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="ThinFilm" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="ThinFilm"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add thin-film` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/thin-film/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/thin-film/thin-film.html` · `kosif-one/vendor/hyperframes/registry/blocks/thin-film/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### TEX-64 · كرة ماء · Water · 📦 بأمر تثبيت
- **ماذا / what:** Sphere of wind-rippled water reflecting blue sky. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add water` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="Water" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="Water"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add water` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/water/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/water/water.html` · `kosif-one/vendor/hyperframes/registry/blocks/water/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### TEX-65 · ضوضاء وورلي · Worley Noise · 📦 بأمر تثبيت
- **ماذا / what:** Drifting cells bright at centres and dark at edges. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add worley-noise` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="WorleyNoise" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="WorleyNoise"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add worley-noise` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/worley-noise/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/worley-noise/worley-noise.html` · `kosif-one/vendor/hyperframes/registry/blocks/worley-noise/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### TEX-66 · دفء الحبيبات · Example project: warm-grain · 📦 بأمر تثبيت
- **ماذا / what:** Cream #f5f0e0 aesthetic with grain texture, Outfit font (10 s). [Local copy lacks its sub-compositions: compositions/captions.html, compositions/graphics.html, compositions/intro.html.]
- **كيف / how:** Starter project: `npx hyperframes init --example warm-grain` style scaffold (index.html mounts sub-compositions via data-composition-src); reuse its palette/type as a style reference.
- **أرقام / params:** 1920x1080; 10 s
- **تثبيت / install:** `npx hyperframes init --example warm-grain` style scaffold (index`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/examples/warm-grain/registry-item.json` · `kosif-one/vendor/hyperframes/registry/examples/warm-grain/index.html`

#### TEX-67 · كتل المؤثرات والخلفيات · Registry shader/VFX background blocks · 📦 بأمر تثبيت
- **ماذا / what:** Procedural/look blocks: aurora, blob, chrome-orb, cosmic-orb, flowing-gradient, fractal-noise, gabor-noise, godrays, goo, halftone-field, hologram, holographic, ios26-liquid-glass, lens-flare, light-leak, liquid-metal, marble, mesh-gradient, nebula, obsidian, plasma, plastic, prism, snow, spiral-gal…
- **كيف / how:** npx hyperframes add <block>.
- **تثبيت / install:** `npx hyperframes add <block>`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks`

#### TEX-68 · مؤثرات الشيدر على الصورة والفيديو · Shader media effects (18 keys) · 📦 بأمر تثبيت
- **ماذا / what:** Realtime effects on footage: blur, pixelate, chromaBleed, tapeDamage, filmArtifacts, halftone, twoInkPrint, ascii, dither (Bayer), bloom, monoScreen, scanlines, chromaticAberration, crtCurvature, digitalGlitch, engraving, crosshatch, kuwahara (painterly); details grain + vignette.
- **كيف / how:** Set effects.<key> 0..1 in data-color-grading via media-treatment; never recreate with CSS overlays.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/core/src/colorGrading.ts` · `kosif-one/vendor/hyperframes/skills/media-use/references/media-treatments.md`

#### TEX-69 · انعكاس الكروم · Chrome CubeCamera reflection · 📦 بأمر تثبيت
- **ماذا / what:** Chrome hero reflects real scene via CubeCamera.
- **كيف / how:** three-kit.js (window.K3) in a --3d project; render --engine studio
- **أرقام / params:** 256², half float; hide hero while rendering
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:106` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### TEX-70 · خامة القطيفة والعين اللامعة · plushMaterial and glossy eye · 📦 بأمر تثبيت
- **ماذا / what:** Felt sheen + fuzz material; glossy eye(), tube(), stageDisc.
- **كيف / how:** shape-kit.js / lab-kit.js in a 3D project; read references/shape-kit.md
- **أرقام / params:** K3S.plushMaterial, eye, tube, stageDisc
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:101` · `100-superskills/skills/kosif-montage-motion/SKILL.md:113` · `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### TEX-71 · الفرو والعين · makeFur shell fur & makeEye · 📦 بأمر تثبيت
- **ماذا / what:** Shell fur; eye with sclera/iris/pupil/cornea.
- **كيف / how:** shape-kit.js / lab-kit.js in a 3D project; read references/shape-kit.md
- **أرقام / params:** makeFur, makeEye
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:101` · `100-superskills/skills/kosif-montage-motion/SKILL.md:113` · `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### TEX-72 · خامة بدن خشبي مدهون إجرائياً · Procedural painted wooden hull texture · 📦 بأمر تثبيت
- **ماذا / what:** A traditional boat's paint bands, plank seams, wood grain and chipped paint are generated on a canvas, no image files.
- **كيف / how:** Canvas 1024×256: bands [0–.30 #4a1f17, .30–.78 #1d5f78, .78–.84 #e9e2cf, .84–.92 #b5432c, .92–1 #c89a52]; dark seam line every 9 px; per-pixel n = fbm(x/60,y/5)·0.10 + noise·0.05 − 0.12 where fbm(x/9,y/140)<−0.35 (chips); CanvasTexture sRGB anisotropy 8, roughness 0.62.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:25`

#### TEX-73 · خامة قمر إجرائية · Procedural moon texture · 📦 بأمر تثبيت
- **ماذا / what:** A believable full moon from math: limb darkening, darker maria from noise, small craters, soft alpha edge, bright enough to bloom.
- **كيف / how:** 512² canvas: limb = (1−r²)^0.22; maria = smooth(0.05,0.35,fbm(2.2u,2.2v,5))·0.32; crater = max(0,fbm(14u,14v,3))·0.12; rgb (255,250,236)·l; disc 2.1° wide at 9000 units; halo sprite ×7 opacity .28.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:115` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:156`

#### TEX-74 · حبيبات فيلم وتعتيم أطراف SVG · SVG film grain and vignette overlays · 📦 بأمر تثبيت
- **ماذا / what:** A static, seeded fractal-noise grain in soft-light blend and a radial vignette give 2D motion pieces a filmic finish.
- **كيف / how:** M.vignette(root, {strength:.45}) → radial-gradient transparent 55% → rgba(0,0,0,.45); M.grain(root, {opacity:.05, seed:7}) → SVG feTurbulence fractalNoise baseFrequency .9, 2 octaves, desaturated, soft-light.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:60` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:440` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:457`

#### TEX-75 · شفافية الأشعة السينية للمجسم · Plush X-ray during analysis · 📦 بأمر تثبيت
- **ماذا / what:** The soft plush character turns semi-transparent while its internal structure is analysed, then returns opaque.
- **كيف / how:** Collect all materials, set transparent; opacity = base·(1 − 0.66·xr), depthWrite only when > 0.98; xr = smooth(joint−.05, joint+.3) · (1 − smooth(rank+.05, rank+.42)).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:53` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:144`

#### TEX-76 · طبقات فرو للشخصيات القطيفة · Fur shells for plush characters · 📦 بأمر تثبيت
- **ماذا / what:** Plush animals get layered fur shells (roots dark, tips light, gravity on shells); colour of every shell can be recoloured live.
- **كيف / how:** makeRabbit({layers:7, furLength:.09}); makeLion({layers:8, furLength:.07}); mane described as 10 shells 0.18 m; recolour shells m.material.color.lerp(target).multiplyScalar(0.55+0.45·(i+1)/n).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/src/main.js:14` · `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/src/main.js:67`

#### TEX-77 · قاع بركة مع انكسارات ضوئية · Pond bed terrain with caustics · 📦 بأمر تثبيت
- **ماذا / what:** A pond bowl terrain coloured by depth and slope (silt, sand, mud, moss) with animated light caustics on the bed, pebbles and fish, absorbing red with depth.
- **كيف / how:** makeTerrain({height, colour, size 44, seg 320, albedoRepeat 10, normalRepeat 22, normalScale .8, texSize 512}); addCaustics(material, {time, level 0, strength 3.2, scale 5.5, absorb [1.35,.42,1.0], sun}); makePebbles n 2600 size .038 + rim 170 size .24.
- **أرقام / params:** colours silt #4a4532 sand #857a5c mud #2e2a20 moss #3d5a26 #5f7a33
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:9` · `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:39`

#### TEX-78 · كرة كروم تعكس المشهد حياً · Chrome orb with live cube reflection · 📦 بأمر تثبيت
- **ماذا / what:** A mirror sphere floats over the playhead and reflects the actual canyon via a cube camera updated each frame.
- **كيف / how:** WebGLCubeRenderTarget(256, HalfFloat, mipmaps); CubeCamera(0.05, 600); MeshStandardMaterial metalness 1, roughness .06, envMap cube; per frame hide orb → cubeCam.update → show.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:51` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:126`

#### TEX-79 · أسفلت مبلل وطلاء عاكس · Wet asphalt road and retro-reflective paint · 📦 بأمر تثبيت
- **ماذا / what:** Night road realism: slightly wet low-roughness asphalt that glints with lamps, centre dashes and solid edge lines that glow faintly.
- **كيف / how:** Road ribbon from CatmullRom (800 segments, 8 m wide) MeshStandard 0x15161a roughness .32; paint 0xe8e4da emissive 0x6a6658 ×0.6; 340 instanced dashes 0.16×3 m every 12 m; edge lines 0.14 m at ±(4−0.35) m.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:64` · `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:80`

#### TEX-80 · وصفات خامات PBR · PBR material recipes (Three.js) · 📦 بأمر تثبيت
- **ماذا / what:** Quick material settings for realistic 3D surfaces.
- **كيف / how:** MeshStandardMaterial/MeshPhysicalMaterial; shiny metal metalness 0.8 roughness 0.2; self-lit parts via emissive + emissiveIntensity.
- **أرقام / params:** metalness 0.8-0.85, roughness 0.15-0.2, emissiveIntensity 0.8
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/animation_craft.md` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:132`

#### TEX-81 · حبيبات الفيلم والتعتيم · Film grain and vignette overlays · 📦 بأمر تثبيت
- **ماذا / what:** Finishing layers: SVG fractal-noise grain that jumps in steps (seek-safe CSS) in soft-light, and a radial vignette.
- **كيف / how:** M.grain(stage,{opacity:.09,blend:'soft-light',freq:'0.9',seed}) feTurbulence 2 octaves desaturated, keyframes mk-grain-jump 0.6 s steps(1); M.vignette(stage,{inner:55,strength:.42}).
- **أرقام / params:** used: thursday grain .07 vignette .45; whatsapp grain .07 vignette .5 inner 50
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:439-463` · `kosif-one/projects/thursday-dua-animation/source/index.html:107-108` · `kosif-one/projects/whatsapp-motion/projects/success/index.html:116-117`

#### TEX-82 · إضاءة بارزة بخريطة ارتفاع · Relief lighting (height field) · 📦 بأمر تثبيت
- **ماذا / what:** Lights a shape as a height field with subsurface scattering, bumps, roughness, Fresnel and specular.
- **كيف / how:** relief(shape, lights=[...], base, ambient=0.22, bulge=0.6, plateau=0.5, ...).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/render.py:618` · `kosif-one/tools/kosif-studio/scenes/whale_dragon.py`

#### TEX-83 · محاكاة اللوك · Look replication: vignette/grain/letterbox/fades · 📦 بأمر تثبيت
- **ماذا / what:** Solves vignette strength from corner ratio, grain sigma compensated for H.264 crf loss, letterbox and fades.
- **كيف / how:** mm_build.solve_vignette, grain_gain(crf)
- **أرقام / params:** crf 17 default
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-mimic/scripts/mm_build.py:130`

#### TEX-84 · نسيج ضوضاء · Scene op: noise texture · 📦 بأمر تثبيت
- **ماذا / what:** KOSIF Studio scene operation: noise.
- **كيف / how:** noise(shape,amount,cell,seed,mode,colour,octaves,stretch); skin cell 10-14 multiply, water stretch (6,1), cloud cell 60 + blur, rock cell 26 + cold rim
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md` · `100-superskills/skills/pixel-studio-painter/scripts/render.py`

#### TEX-85 · حراشف · Scene op: scales pattern · 📦 بأمر تثبيت
- **ماذا / what:** KOSIF Studio scene operation: scales.
- **كيف / how:** scales(shape,size 14,colour,alpha .35,width 1)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md` · `100-superskills/skills/pixel-studio-painter/scripts/render.py`

#### TEX-86 · حبيبات الفيلم · Seekable film grain (CSS/SVG) · 📦 بأمر تثبيت
- **ماذا / what:** Fractal-noise SVG overlay that jumps between 6 offsets in stepped CSS animation, so it is seekable.
- **كيف / how:** MOTION.grain(stage, {opacity, blend, freq, seed, z}).
- **أرقام / params:** opacity .09, soft-light, feTurbulence baseFrequency .9, 2 octaves, desaturated, 0.6 s steps(1) loop
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:440`

#### TEX-87 · خامات مولّدة · Generated textures (no downloads) · 📦 بأمر تثبيت
- **ماذا / what:** Canvas textures from functions, normal maps from height functions, and sprite textures.
- **كيف / how:** K3.noiseCanvas(N, fn), K3.normalFromHeight(N, hfn, strength), K3.spriteTex('soft'|'ring'|'streak').
- **أرقام / params:** sprite 128 px; ring warm stop rgba(255,220,180,.35)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:41`

#### TEX-88 · حصى · Water-worn pebbles · 📦 بأمر تثبيت
- **ماذا / what:** Instanced deformed icosahedra in colour families, clumped in drifts, with caustics.
- **كيف / how:** K3.makePebbles({n, region, accept, size, flat, clump, seed}).
- **أرقام / params:** n 2400, size .06 (×0.4-2.8), flatten .5
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:724`

#### TEX-89 · طلاء بلا هندسة · Paint stamps (colour only) · 📦 بأمر تثبيت
- **ماذا / what:** Colour stamps on the surface without geometry: blush, belly patch, paw pads.
- **كيف / how:** S.paint(c, r, colour, {soft, radii, amount}).
- **أرقام / params:** e.g. blush r .015 soft .009 amount .8
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/shape-kit.js:98`

#### TEX-90 · خامات المختبر · Lab material set · 📦 بأمر تثبيت
- **ماذا / what:** Quick materials: plush, gloss, leather, metal.
- **كيف / how:** K3.plushMaterial(c), K3.glossMaterial(c,{roughness}), K3.leatherMaterial(c), K3.metalMaterial(c).
- **أرقام / params:** plush rough .95; gloss rough .08 clearcoat 1; leather #15171a rough .55 metal .05; metal #d8dde3 rough .25 metal .95
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/lab-kit.js:49`

#### TEX-91 · سطح ماء يلمع · Water surface with light glints · 📦 بأمر تثبيت
- **ماذا / what:** Waves as a stretched noise height field; colour mixes deep water and sky by how much each facet faces up; every light leaves a trail of specular glints.
- **كيف / how:** water(area, lights, deep, sky, cell, stretch, height, seed, shininess, spec, octaves).
- **أرقام / params:** defaults deep #0a1118, sky #2a3a4c, cell 18, stretch 6, height 6, shininess 60, spec 1.2; storm sea #060a0f/#28323f cell 20 stretch 7 height 7 shininess 70
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/render.py:652` · `kosif-studio/scenes/whale_dragon.py:115`

#### TEX-92 · ستوب موشن · Style: Stop motion (stop-motion) · 📦 بأمر تثبيت
- **ماذا / what:** Choppy physical-object animation feel with tiny jitter.
- **كيف / how:** Animate on twos, seeded 1-2px position/rotation jitter per held frame, photo textures and contact shadows. Scaffold: python3 tools/kosif.py scaffold stop-motion <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:stop-motion` · `kosif-tool/playbooks/characters.md`

#### TEX-93 · قصاصات ورقية · Style: Cutout paper (cutout-paper) · 📦 بأمر تثبيت
- **ماذا / what:** Paper cut-out layers with torn edges and drop shadows.
- **كيف / how:** SVG shapes with paper texture 5-10%, soft drop shadow, hinge-pivot rigs, on twos. Scaffold: python3 tools/kosif.py scaffold cutout-paper <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:cutout-paper` · `kosif-tool/playbooks/hand-drawn.md`

#### TEX-94 · صلصال متحرك · Style: Claymation (claymation) · 📦 بأمر تثبيت
- **ماذا / what:** Clay-like soft characters with matte material and squash/stretch.
- **كيف / how:** Three.js matte roughness 0.6-0.9 or 2D with soft shading; squash scaleY 0.7/scaleX 1.3 80ms. Scaffold: python3 tools/kosif.py scaffold claymation <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:claymation` · `kosif-tool/playbooks/characters.md`

#### TEX-95 · إزالة الخلفية بلون الزاوية · Corner-colour background knockout · 📦 بأمر تثبيت
- **ماذا / what:** Float scenes by flood-removing bg matched to averaged corner colour within RGB tolerance.
- **كيف / how:** python3 knockout.py with PIL; TOL env.
- **أرقام / params:** TOL=34 Euclidean RGB
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/references/knockout.py:25`

#### TEX-96 · ملمس حبيبات الطباشير · Chalk grain overlay · 👁 شوهد في فيديو
- **ماذا / what:** static full-board SVG layer: feTurbulence (fractalNoise) -> feColorMatrix mapping to board-coloured specks over the drawings; do not use feDisplacementMap on strokes
- **أرقام / params:** baseFrequency ~0.9, opacity ~0.35
- **الدليل / proof:** `style:chalkboard`

#### TEX-97 · تعبئة طباشيرية للثياب · Chalky robe scribble fill · 👁 شوهد في فيديو
- **ماذا / what:** overlay short diagonal hatch strokes in a slightly lighter tint inside the robe shape, clipped to the silhouette
- **أرقام / params:** hatch spacing 6-8 px, opacity 0.3
- **الدليل / proof:** `style:doodle`

#### TEX-98 · كرة لامعة بانعكاسات · Glossy sphere material · 👁 شوهد في فيديو
- **ماذا / what:** stack radial gradients: body, rotating soft reflections inside, top-left specular, rim light; outer soft glow
- **أرقام / params:** #5b9bff->#1239a0, rim #c9f4ff
- **الدليل / proof:** `style:infographic`

#### TEX-99 · ورق قديم بحواف محروقة ونقاط رمل · Parchment vignette and sand stipple · 👁 شوهد في فيديو
- **ماذا / what:** radial gradient #ead9b5 centre -> #c9aa72 edges; random dots inside desert rectangles, rejecting points inside seas via point-in-polygon; faint fold lines
- **أرقام / params:** dot r 0.6-1px, opacity 0.3
- **الدليل / proof:** `style:map-journey`

#### TEX-100 · أرضية ورق مربعات داكن · Graph-paper grid ground · 👁 شوهد في فيديو
- **ماذا / what:** draw a 1 px grid in #1a1a1a over #090909, plus film grain overlay and soft vignette
- **أرقام / params:** cell 40-48 px at 1280w, grain opacity 0.06
- **الدليل / proof:** `style:plotter`

#### TEX-101 · سماء متدرجة بالتنقيط مع نجوم · Dithered sky gradient + stars · 👁 شوهد في فيديو
- **ماذا / what:** Bayer-dither between 3-4 indigo/purple bands; 1-2 px stars twinkle on random stepped intervals
- **أرقام / params:** 4x4 Bayer matrix, twinkle 4 fps
- **الدليل / proof:** `style:pm-0xevinho-3777d8`

#### TEX-102 · رسمة ممسوحة كملصق مقصوص · Scanned drawing as sticker cut-out · 👁 شوهد في فيديو
- **ماذا / what:** Mask hand-drawn scans to alpha, add 6-10 px white outline (dilate) plus soft 4 px drop shadow so each character reads as a paper sticker over a textured ground
- **أرقام / params:** outline #ffffff 90%, shadow rgba(0,0,0,.2) offset 2 px
- **الدليل / proof:** `style:pm-abderrahmen-g-9e8ed0`

#### TEX-103 · خلفية ورق ألوان مائية · Watercolour paper ground · 👁 شوهد في فيديو
- **ماذا / what:** Full-frame cream paper texture (embossed noise/normal map look) multiplied over every scene; watercolour wash hill drawn as wobbly ink arc with green wash fill
- **أرقام / params:** paper #f3e8cf, hill wash #c6c7a4 with darker blotches
- **الدليل / proof:** `style:pm-abderrahmen-g-9e8ed0`

#### TEX-104 · أرضية بلاط · Tile floor pattern · 👁 شوهد في فيديو
- **ماذا / what:** repeating pixel tile bg
- **أرقام / params:** 32px
- **الدليل / proof:** `style:pm-aisongman-71ffac`

#### TEX-105 · أرض ورقية · Paper doodle ground · 👁 شوهد في فيديو
- **ماذا / what:** cloudy paper texture, hand-drawn baseline
- **الدليل / proof:** `style:pm-ajith-io-ea7f2d`

#### TEX-106 · تعبئة نقطية أحادية البت · 1-bit dither pattern fill · 👁 شوهد في فيديو
- **ماذا / what:** Bayer/checker dither of orange on black filling a region or full frame; animate threshold to sweep
- **أرقام / params:** cell 8px, threshold sweep 600 ms
- **الدليل / proof:** `style:pm-anthonyriera-9b1b2a`

#### TEX-107 · تظليل كرة بالهافتون · Halftone sphere shading · 👁 شوهد في فيديو
- **ماذا / what:** Grid of dots whose radius = lambert(normal·light) for a virtual sphere; light direction animates
- **أرقام / params:** grid 14px, rmax 6px, color #f04a2a
- **الدليل / proof:** `style:pm-ayushunleashed-ece3e3`

#### TEX-108 · غيوم مرسومة بخطوط انسيابية · Painterly streak clouds · 👁 شوهد في فيديو
- **ماذا / what:** Domain-warped fbm noise thresholded into soft streaks, coloured by sky gradient + rim tint toward the sun, drifting slowly
- **أرقام / params:** fbm 4-5 octaves, warp 0.3, drift 0.01 uv/s
- **الدليل / proof:** `style:pm-demitiyageekzen-7770ad`

#### TEX-109 · خلفية أشرطة ضوء منقطة · Halftone light-band backdrop · 👁 شوهد في فيديو
- **ماذا / what:** Diagonal soft gradient bands at corners filled with halftone dots and pixel circuit pattern, masked by radial fade toward centre; slow drift
- **أرقام / params:** band angle ~-35°, dot pitch 6-8 px, opacity 0.3-0.5
- **الدليل / proof:** `style:pm-elliot-garreffa-f334bc`

#### TEX-110 · مشهد أطفال بخامة ورق وكرايون · Paper-craft kids scene · 👁 شوهد في فيديو
- **ماذا / what:** crayon-textured shapes (sun, clouds, rainbow, hills), fuzzy puppet with big eyes, speech balloon with two-colour bubbly text
- **أرقام / params:** texture fill + 3px dark outline
- **الدليل / proof:** `style:pm-emollick-8661a8`

#### TEX-111 · نقاط تتحول إلى هافتون متداخل · Raster dot morph with halftone moiré · 👁 شوهد في فيديو
- **ماذا / what:** Grid of dots whose radius is driven by a radial wave field; overlay a second screen at different angle to produce overprint moiré
- **أرقام / params:** 16 px screen, angles 15° and 45°, ripple speed 1 ring/0.5 s
- **الدليل / proof:** `style:pm-fionntobin-97b7af`

#### TEX-112 · أرضية حمم بعروق مضيئة · Veined lava floor shader · 👁 شوهد في فيديو
- **ماذا / what:** Plane with fragment shader: abs(fbm) ridged noise thresholded to thin orange veins over purple-maroon base, slow time scroll
- **أرقام / params:** ridge width 0.03, colors #f0a040 on #4a2040, scroll 0.05/s
- **الدليل / proof:** `style:pm-gorden-sun-041f56`

#### TEX-113 · حبيبات وتعتيم أطراف · Grain and vignette finish · 👁 شوهد في فيديو
- **ماذا / what:** Overlay animated film grain (per-frame noise, 4-6% opacity) and a strong radial vignette on light/red scenes so flat colour reads as printed
- **أرقام / params:** vignette edge -35% luminance
- **الدليل / proof:** `style:pm-grace-sunnyy-29bc61`

#### TEX-114 · درجة ورق تحريري دافئ · Editorial paper grade · 👁 شوهد في فيديو
- **ماذا / what:** cream #efecdd base + 3% noise + radial vignette; ink near-black, single red accent
- **أرقام / params:** noise 3%, vignette 10%
- **الدليل / proof:** `style:pm-hbcoop-de365c`

#### TEX-115 · خلفية نسيج بيانات خافت · Faint data-texture background · 👁 شوهد في فيديو
- **ماذا / what:** fill dark background with a grid of tiny mono text items (emails) at 6-10% opacity slowly scrolling, under a radial violet glow
- **أرقام / params:** mono 9 px, opacity 0.08, scroll 10 px/s
- **الدليل / proof:** `style:pm-kmasiff-cc72cb`

#### TEX-116 · قصاصة جريدة بحافة بيضاء · Newspaper cutout sticker · 👁 شوهد في فيديو
- **ماذا / what:** B&W halftone/engraved object, 4-8 px white stroke border, soft drop shadow 30% opacity offset down
- **أرقام / params:** stroke white 6px, shadow blur 12px
- **الدليل / proof:** `style:pm-koldo2k-5cff87`

#### TEX-117 · صور النقش · Engraving imagery · 👁 شوهد في فيديو
- **ماذا / what:** greyscale etching cutouts on white
- **أرقام / params:** desat 100%
- **الدليل / proof:** `style:pm-lexnlin-038035`

#### TEX-118 · جدار بيانات خافت · Data wall texture · 👁 شوهد في فيديو
- **ماذا / what:** columns of mono text at 10% alpha scrolling slowly
- **أرقام / params:** speed 10 px/s
- **الدليل / proof:** `style:pm-madebyjmayala-b9204d`

#### TEX-119 · حبيبات فيلم مع زوايا HUD · Film grain + HUD corners · 👁 شوهد في فيديو
- **ماذا / what:** Animated noise overlay at low opacity plus corner brackets with micro mono labels and a progress meter
- **أرقام / params:** grain opacity 6-10%, refreshed every frame
- **الدليل / proof:** `style:pm-madhav-xo-f97f20`

#### TEX-120 · سماء بضربات فرشاة · Brush-stroke sky shader · 👁 شوهد في فيديو
- **ماذا / what:** flow-field oriented stroke sprites/shader scrolling along swirl paths
- **أرقام / params:** slow loop
- **الدليل / proof:** `style:pm-mandelduck-95fd08`

#### TEX-121 · تلوين سينمائي بحبيبات وخدوش · Vintage film grade · 👁 شوهد في فيديو
- **ماذا / what:** Post pass: warm/violet split-tone, animated grain, sparse dust specks and vertical scratches, slight vignette and bloom
- **أرقام / params:** grain 0.08, dust 20/frame, bloom threshold 0.8
- **الدليل / proof:** `style:pm-nft-chen-5f8bb0`

#### TEX-122 · عنوان محبب متوهج · Grain-glow title card · 👁 شوهد في فيديو
- **ماذا / what:** Heavy sans title filled with noise texture, soft outer glow, subtitle in italic serif; fade in from a single star point
- **أرقام / params:** noise opacity 0.5; glow 20px
- **الدليل / proof:** `style:pm-nolkeeg-bf062e`

#### TEX-123 · أشكال وحروف من زجاج متجمد · Frosted glass shapes and glass letters · 👁 شوهد في فيديو
- **ماذا / what:** Render a blurred (20-40 px), lightened (+20% white) copy of the backdrop clipped to the shape or text path; add a bright 1px top rim; text letters can be cut by the card edge
- **أرقام / params:** blur 30 px, white overlay 0.25, rim rgba(255,255,255,.7)
- **الدليل / proof:** `style:pm-notdwd-7de38a`

#### TEX-124 · مربع زجاجي مُثلج للكتابة · Frosted glass prompt box · 👁 شوهد في فيديو
- **ماذا / what:** backdrop-filter blur(24px) saturate(1.4), white 35% fill, bright 1px top rim, radius 60; springs open from the menu icon with ~2% width overshoot
- **أرقام / params:** 726x228 @1080 stage
- **الدليل / proof:** `style:pm-notdwd-c2037d`

#### TEX-125 · بقع نقطية · Halftone corner blobs · 👁 شوهد في فيديو
- **ماذا / what:** radial halftone dot pattern in magenta/blue at corners, slow drift
- **الدليل / proof:** `style:pm-polydao-7a572b`

#### TEX-126 · حروف مملوءة بسائل رخامي · Fluid-shader filled letters · 👁 شوهد في فيديو
- **ماذا / what:** render domain-warped noise (fbm) shader in blue/magenta/red; use text as mask; then scale the mask up until fluid fills frame and overlay outline text
- **أرقام / params:** fbm 4 octaves, warp 2x, colours #2f4bff #e8503c #ff7ad9
- **الدليل / proof:** `style:pm-prasenx-8d9323`

#### TEX-127 · صورة هالفتون · Halftone macro image · 👁 شوهد في فيديو
- **ماذا / what:** dot screen shader over greyscale photo
- **الدليل / proof:** `style:pm-reflex-cloud-72ffe5`

#### TEX-128 · حلقة نقاط هافتون · Halftone dot ring · 👁 شوهد في فيديو
- **ماذا / what:** dot grid with radius by distance field
- **الدليل / proof:** `style:pm-rendesr-86be44`

#### TEX-129 · تعبئة حبيبات ريزو · Riso grain fill · 👁 شوهد في فيديو
- **ماذا / what:** SVG feTurbulence threshold mask on flat shapes
- **أرقام / params:** freq 0.9, 2-3 inks
- **الدليل / proof:** `style:pm-rneayan-474bcf`

#### TEX-130 · شبكة قياس خلفية · Graticule grid background · 👁 شوهد في فيديو
- **ماذا / what:** 10x8 grid lines #0f2a1a at 1px plus minor ticks; radial vignette
- **أرقام / params:** opacity 0.35
- **الدليل / proof:** `style:pm-rneayan-ea6129`

#### TEX-131 · خلفية سوداء دافئة بحبيبات وتعتيم أطراف · Warm-black film grain + vignette · 👁 شوهد في فيديو
- **ماذا / what:** base #0a0907, animated noise overlay 3-5% opacity, radial vignette to black
- **أرقام / params:** noise regenerate each frame; vignette 60% at corners
- **الدليل / proof:** `style:pm-robj3d3-b18fad`

#### TEX-132 · عنصر تحكم من زجاج سائل · Liquid glass control · 👁 شوهد في فيديو
- **ماذا / what:** Capture backdrop, blur ~14 px for body; in a 12 px edge band draw a slightly blurred copy magnified 1.06x (refraction); add milky white fill, top sheen gradient, 1px bright rim and soft lift shadow; p
- **كيف / how:** Capture backdrop, blur ~14 px for body; in a 12 px edge band draw a slightly blurred copy magnified 1.06x (refraction); add milky white fill, top sheen gradient, 1px bright rim and soft lift shadow; put a pastel aura behind so glass reads on white
- **أرقام / params:** body blur 14 px, edge band 12 px, magnify 1.06
- **الدليل / proof:** `style:pm-rossaxbt-3085b7`

#### TEX-133 · سماء سديمية · Nebula skybox · 👁 شوهد في فيديو
- **ماذا / what:** fbm noise shader purple/magenta + star points
- **الدليل / proof:** `style:pm-ryzoft-4f85bd`

#### TEX-134 · حبيبات وتظليل أطراف · Grain + vignette finish · 👁 شوهد في فيديو
- **ماذا / what:** Overlay animated noise at low opacity and radial vignette on every scene
- **أرقام / params:** grain 4%, vignette 30%
- **الدليل / proof:** `style:pm-sahildesigner23-ee3155`

#### TEX-135 · جدار نص كثيف · Dense text wall · 👁 شوهد في فيديو
- **ماذا / what:** rows of small text scrolling opposite directions behind headline
- **أرقام / params:** speed 40-80px/s
- **الدليل / proof:** `style:pm-souravbhar871-61f424`

#### TEX-136 · تدرج داكن مع حبيبات · Grain + vignette dark grade · 👁 شوهد في فيديو
- **ماذا / what:** Heavy animated film grain and vignette over all dark scenes for a gritty premium look
- **أرقام / params:** grain 8-10%, vignette 40%
- **الدليل / proof:** `style:pm-spearwtf-3c1fd1`

#### TEX-137 · خلفية أشعة وهافتون · Sunburst + halftone background · 👁 شوهد في فيديو
- **ماذا / what:** conic gradient rays rotating slowly + dot overlay
- **الدليل / proof:** `style:pm-topi-003-b0e12c`

#### TEX-138 · تموج هافتون · Halftone ripple · 👁 شوهد في فيديو
- **ماذا / what:** dot grid radius = f(distance to centre, t)
- **الدليل / proof:** `style:pm-ultimaxbt-bbebf5`

#### TEX-139 · كورة زجاجية لامعة · Glass orb material · 👁 شوهد في فيديو
- **ماذا / what:** circle with radial-gradient (light top-left to deep violet), white elliptical specular blur at top, small orange inner blur hotspot, outer purple glow + faint concentric halo rings
- **أرقام / params:** #a88bff->#6c3bff, highlight opacity 0.6
- **الدليل / proof:** `style:product`

#### TEX-140 · تهشير بالماركر داخل حدود الشكل · Clipped marker hatching · 👁 شوهد في فيديو
- **ماذا / what:** diagonal zigzag path covering the shape's bbox drawn with strokeDasharray progress, clipped by clipPath of the shape, opacity ~0.55
- **أرقام / params:** spacing 10-12 px, angle 60deg
- **الدليل / proof:** `style:whiteboard`

#### TEX-141 · آثار مسح على السبورة البيضاء · Eraser-smudge board texture · 👁 شوهد في فيديو
- **ماذا / what:** a few very light grey rounded strokes with large blur at random positions over #f6f6f4, plus subtle inner border shadow
- **أرقام / params:** opacity 0.05-0.1, blur 8-12 px
- **الدليل / proof:** `style:whiteboard`

#### TEX-142 · سطح زجاجي · Glass surface material · 📄 موصوف
- **ماذا / what:** Layered frosted-glass panel: backdrop blur, faint white fill, gradient top-lit border, wide ambient shadow; dark backgrounds only.
- **كيف / how:** backdrop-filter: blur(28px) (40px for modal/spotlight); background rgba(255,255,255,0.05); border 1px rgba(255,255,255,0.08) with 180deg gradient 0.12->0.02; box-shadow 0 24px 80px rgba(0,0,0,0.25).
- **أرقام / params:** blur 28/40px; fill 0.05
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### TEX-143 · خلفيات تدرج شبكي · Mesh gradient & grid backgrounds · 📄 موصوف
- **ماذا / what:** Atmospheric backgrounds from stacked radial gradients, inline SVG noise and faint 1px grid lines.
- **كيف / how:** radial-gradient(ellipse at 20% 80%, rgba(r,g,b,0.3) 0%, transparent 50%) x2 over base; grid lines rgba(255,255,255,0.03) 1px every 50px; animate gradient centers slowly; film grain monochrome noise at ~2% opacity to fight banding.
- **أرقام / params:** grid 50px @3%; grain 2%
- **الدليل / proof:** `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/animation-patterns.md` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### TEX-144 · S04 كولاج ورقي · S04 Paper collage · 📄 موصوف
- **ماذا / what:** Cut-outs, tape, paper, tactile edges; layers hop lightly, tear and page-flip. Personal and playful and buildable from photos, but needs cutting and layer organisation; too many textures crowd the frame.
- **كيف / how:** PNG cut-outs with paper textures (licensed/procedural feTurbulence), small rotations, drop shadows; render via KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg)
- **أرقام / params:** cost medium; MG-004 MG-076 MG-101 MG-102 MG-103 MG-110
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### TEX-145 · MG-101/102 قصاصات تبني مشهداً وشريط لاصق · MG-101/102 Cut-out board and tape pin · 📄 موصوف
- **ماذا / what:** Cut photos enter at small angles and compose a board around a title (MG-101); a photo lands and a little strip of tape passes over its corner to pin it (MG-102).
- **كيف / how:** MG-101: 0-1 background, 1-4 cut-outs, 4-7 read; independent layers with few rotation/scale keys; don't copy a specific commercial template. MG-102: 0-1 photo, 1-2 tape, 2-4 hold; reveal mask on the tape, keep its shadow light because tape sits close to paper.
- **أرقام / params:** 7 s / 4 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-collage-textures.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### TEX-146 · MG-103 تمزيق بين طبقتين · MG-103 Paper tear reveal · 📄 موصوف
- **ماذا / what:** A ragged tear opens from the middle uncovering the image beneath.
- **كيف / how:** 0-0.7 slit, 0.7-2.5 tear, 2.5-4 read; irregular mask path with two paper edges and shadow - never a perfectly smooth edge for a hand tear. Local: jittered SVG polygon edges animated apart with a paper texture.
- **أرقام / params:** 4 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-collage-textures.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### TEX-147 · لمسات تشطيب سينمائية · Film finishing touches · 📄 موصوف
- **ماذا / what:** Add organic texture after grading: grain, vignette, slight halation/bloom, letterbox bars, gentle light leaks on transitions.
- **كيف / how:** noise=alls=8:allf=t+u ; vignette=PI/5 ; bloom: split,gblur=sigma=20,blend=all_mode=screen:all_opacity=0.25 ; letterbox 2.39:1 via drawbox or pad ; Remotion @remotion/effects lightLeak overlay on TransitionSeries.Overlay
- **أرقام / params:** grain 6-10; vignette π/5
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/transitions.md`

#### TEX-148 · النقص المقصود · Intentional imperfection (wabi-sabi) · 📄 موصوف
- **ماذا / what:** Warmth from subtle asymmetry, varied line weight, paper/watercolor texture, irregular spacing; less in functional/data parts.
- **كيف / how:** Add slight rotation +-1-2deg, stroke width variance, paper texture overlay; keep data labels clean.
- **أرقام / params:** rotation +-1-2deg
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3743-wabi-sabi-imperfection`

#### TEX-149 · حبيبات فيلم · Film grain overlay 2% · 📄 موصوف
- **ماذا / what:** Monochrome per-frame noise at very low opacity to kill banding and add texture.
- **كيف / how:** Shader or canvas noise layer; ffmpeg noise=alls=8:allf=t alternative.
- **أرقام / params:** opacity 0.02
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`

#### TEX-150 · الهالفتون · Halftone and CMYK halftone · 📄 موصوف
- **ماذا / what:** Dots sized by luma; CMYK version uses four rotated grids C15 M75 Y0 K45 with subtractive blend; gooey version via smooth-min.
- **كيف / how:** GLSL or Python/numpy offline; 3x3 neighbor sampling to avoid clipping; fwidth antialias.
- **أرقام / params:** angles 15/75/0/45
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`

#### TEX-151 · أساليب رسم تشمل الزخرفة الإسلامية والخط العربي · Illustration mediums incl. Islamic geometry & Arabic calligraphy · 📄 موصوف
- **ماذا / what:** Medium keywords for non-photo looks, including culturally Arabic ones.
- **كيف / how:** Pick one medium per style lock.
- **أرقام / params:** Pixar-style 3D, claymation, Ghibli-inspired watercolour, anime key visual, oil impasto, ink wash, isometric 3D, flat vector, low-poly, paper cut, blueprint, double exposure, tilt-shift miniature, Islamic geometric ornament, Arabic calligraphy composition
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/prompt-library.md`

#### TEX-152 · الورق المقصوص · Paper Cut-out style · 📄 موصوف
- **ماذا / what:** Cream paper with muted paper colours and hard paper drop shadow; 3-depth parallax and gentle sway.
- **كيف / how:** Copy style sheet section into DESIGN.md, then build via claude-animation-studio render(t).
- **أرقام / params:** #F6EBD9, #D96B4A, #5B8C5A, #3B6EA8; drop-shadow(0 8px 0 rgba(0,0,0,.18)); parallax 1/0.6/0.3; sway +-2deg; Amiri 700/Lateef + Tajawal 500
- **الدليل / proof:** `100-superskills/skills/trend-animation-styles/references/styles.md`

#### TEX-153 · وصفات المواد · Material recipe sheet (flame, spray, steam, fur, atmosphere) · 📄 موصوف
- **ماذا / what:** Written recipes: flames as add-layers red to white with glow; airborne water as dots+blur with a warm add layer near fire; steam as a screen cloud with warm add inside; feathers/fur as thin parallel tubes plus strokes; distance as a blue screen veil.
- **كيف / how:** Follow references/drawing-guide.md section 3 when writing a build().
- **أرقام / params:** atmosphere: fill(rect, colour, .2, blur=30, mode='screen'); far edges blur 1-3
- **الدليل / proof:** `kosif-studio/references/drawing-guide.md:62`

#### TEX-154 · عائلة مواد مطفية · Matte material family · 📄 موصوف
- **ماذا / what:** Keep one material family; matte for clay and low-poly, gloss reserved for hero products.
- **كيف / how:** MeshStandardMaterial roughness in matte range.
- **أرقام / params:** roughness 0.6–0.9; sample color 0x7ee8d2 roughness 0.7
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:16` · `kosif-tool/playbooks/3d.md:59`

#### TEX-155 · خامة ورق ثابتة · Static paper/board texture · 📄 موصوف
- **ماذا / what:** Paper or board texture overlay, static unless style asks for boil.
- **أرقام / params:** 5–10% opacity
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:18`

#### TEX-156 · ارتعاش محدد البذرة · Seeded held-frame jitter · 💡 فكرة
- **ماذا / what:** Deterministic per-hold jitter so set breathes like stop-motion.
- **كيف / how:** seeded noise per held index.
- **أرقام / params:** ±1.5 px, ±0.6°
- **الدليل / proof:** `style:pm-davidshulmanfl-371638`

#### TEX-157 · ملمس بصمات · Fingerprint clay texture · 💡 فكرة
- **ماذا / what:** Fingerprint overlay plus baked top-left key light on saturated primaries.
- **كيف / how:** Overlay PNG, multiply.
- **أرقام / params:** 12% opacity
- **الدليل / proof:** `style:pm-davidshulmanfl-371638`

#### TEX-158 · شيدر ضربات فرشاة · Stroke-based painterly shader · 💡 فكرة
- **ماذا / what:** Three stroke sizes jittering so surfaces look hand-painted.
- **كيف / how:** WebGL/three.js stroke shader.
- **أرقام / params:** 3 sizes; 1-2 px jitter @6 Hz
- **الدليل / proof:** `style:pm-mandelduck-95fd08`
