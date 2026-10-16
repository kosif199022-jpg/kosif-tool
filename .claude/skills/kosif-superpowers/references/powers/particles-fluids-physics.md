# الجسيمات والسوائل والفيزياء — Particles, fluids & physics

> فصل مُجمَّع آليًا من 264 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **255 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 255 powers deduplicated by name from 264 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 11 · 🟢 جاهز 33 · 📦 بأمر تثبيت 63 · 🔑 مفتاح/خدمة 2 · 👁 شوهد في فيديو 113 · 📄 موصوف 18 · 💡 فكرة 15

#### PART-01 · بحر عاكس · Reflective sea · ✅ مُثبت هنا
- **ماذا / what:** three.js Water plane with generated wave normals and sun reflection.
- **كيف / how:** K3.makeSea({size, res, color, distortion, waveSize, level}); per frame water.material.uniforms.time / sunDirection / sunColor.
- **أرقام / params:** size 30000; res 768; color #0e4a63; distortion 2.4; waveSize 3
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:245` · `100-superskills/skills/kosif-montage-motion/templates/scene3d/src/main.js:25` · `kosif-studio/motion/kit/three-kit.js:245`

#### PART-02 · سحب حجمية · Raymarched volumetric cloud slab · ✅ مُثبت هنا
- **ماذا / what:** A box of fbm-density clouds raymarched with self-shadowing and a powder term; cover and darkness animate.
- **كيف / how:** K3.makeCloudSlab({size, center}); userData.set(t, cover, dark, sunDir, camPos, sunCol, skyCol).
- **أرقام / params:** size [7000,520,4200] centre [0,1240,-900]; 36 view steps; 3 light steps x70; sky #9fb6cc; sun #fff2d9
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:273` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:273`

#### PART-03 · نفث النار بطبقات · Layered fire breath · ✅ مُثبت هنا
- **ماذا / what:** A fire jet made of three nested filled paths (outer red, mid orange, yellow core), a blurred white-hot core, 12 flame tongues along the stream and a radial splash where it hits.
- **كيف / how:** Quadratic-curve outlines outer/mid/core; extra blur20 copy under outer; loop i<12 placing small flame shapes along a line (980-600t, 380+340t); splash fan every 20 degrees from -80 to 80.
- **أرقام / params:** outer #dc2626 (+#f97316 blur20 .85), mid #f97316, core #fde68a, hot #fffbeb blur8 .8, tongues #fb923c .8
- **الدليل / proof:** `kosif-one/projects/duck-vs-dragon/duck_dragon.py:165-187` · `kosif-studio/scenes/dragon_girl.py:108` · `kosif-studio/scenes/dragon_girl.py:261` · `kosif-studio/scenes/whale_dragon.py:247`

#### PART-04 · حقل حراري يُلطَّخ بالإصبع · Thermal finger-trail shader field · ✅ مُثبت هنا
- **ماذا / what:** A heat-camera blob of domain-warped noise mapped through a seven-stop heat ramp; a pointer trail drags the field like wet paint and heals; a press sends a ripple ring.
- **كيف / how:** Single full-screen fragment shader (WebGL1), trail of points with velocity+age passed as uniforms; displacement = sum(velocity*smoothstep(radius)*age)*smudge. In video, feed a scripted Catmull-Rom path as the 'finger'. Reference HTML is self-contained except DialKit CDN panel.
- **أرقام / params:** fbm 5 octaves, warp-the-warp; ramp stops 0/.12/.30/.45/.60/.78/1; heat cap 0.75; smudge 9 (>14 tears); radius 0.17; 24 points; life 1.6s; melt 6s; flow 0.26; blob 0.37; ripple 0.18/bloom 0.55/0.9s; rim 0.6/halo 0.45; DPR cap 2 disc, 1.25 full-bleed
- **الدليل / proof:** `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail` · `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/references/thermal-finger-trail.html`

#### PART-05 · سحب لوني بأثر الإصبع · Velocity smear trail · ✅ مُثبت هنا
- **ماذا / what:** Field sampled from where a pointer came from, so colour is dragged like wet paint and heals.
- **كيف / how:** 24 trail points (pos+velocity+age, life 1.6s) as uniforms; disp+=vel*smoothstep(r,0,d)*age; uv+=disp*9. Head eases 30%/frame; new point every 0.01 field units. For video, script a fake path.
- **أرقام / params:** smudge 9 (>14 tears), radius 0.17
- **الدليل / proof:** `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/SKILL.md`

#### PART-06 · مؤثرات بكسل تتلاشى بدرجات اللوحة · Pixel VFX via palette-step fades · ✅ مُثبت هنا
- **ماذا / what:** Sparks, slashes, explosions and spells that grow, burst and fade by stepping down a bright-to-dark ramp, never alpha.
- **كيف / how:** Procedural draw(frame) in Pillow; hold the impact frame; frames fx0..fxN with fps or durations_ms.
- **أرقام / params:** ramp 4-6 colors; hold impact 2-3 frames
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9530-vfx`

#### PART-07 · جسيمات ثلج/جمر على المعالج الرسومي · GPU snow / ember particles · ✅ مُثبت هنا
- **ماذا / what:** Point-sprite particles that fall, sway and fade with depth, additively blended over the shards (snow for cobalt, warm embers for ledger).
- **كيف / how:** Vertex shader: y = mod(y - t*(.25+size*.15),16)-8; x += sin(t*.6+z*3.1+size*7)*.25; pointSize=(1.5+3.5*size)*dpr*clamp(10/d,.2,2.5); alpha clamp(1.2-d/22,.05,.8). Fragment: round sprite discard r>.25, smoothstep falloff. Blend ONE,ONE, depthMask false.
- **أرقام / params:** 160 particles phone / 360 desktop; field 24x16x(2..20)
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/crystal-world.js:65` · `kosif-earth-ci-fork/ui/art/crystal-world.js:149`

#### PART-08 · مطر بطبقات متوازية العمق · Layered parallax rain · ✅ مُثبت هنا
- **ماذا / what:** Two rain layers (far thin, near thick and fast) are slanted streaks with wrap-around that shift with the camera track for depth.
- **كيف / how:** far: 152 drops, speed 340–600 px/s, length 11–25 px, #86b7c9 .8 px α .13, parallax .03; near: 32 drops, 630 px/s, 37 px, #95d6df 1.3 px α .17, parallax .1; x drifts −95 px/s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:108`

#### PART-09 · تموجات وبقع رذاذ وانعكاسات مبللة · Puddle ripples, splashes and wet reflections · ✅ مُثبت هنا
- **ماذا / what:** A wet street: broken coloured horizontal reflection strokes, expanding elliptical ripples, splash droplets on landing paws and a flattened dark reflection of the hero.
- **كيف / how:** 85 jittered reflection lines (rose inside x 760–1110 else cyan, α .025–.125); 20 ripples rx 5→29, ry 1→5, period 1/0.65 s; 6 splash events × 11 droplets: x+vx·a, y + vy·a + 145a², life .63 s; hero reflection scale(1, −0.25) opacity .085.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:109` · `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:122`

#### PART-10 · جو الشرر والدخان والتعتيم · Embers, smoke and vignette atmosphere · ✅ مُثبت هنا
- **ماذا / what:** Atmospheric finish for a still: 110 seeded embers in four fire colours, 9 large blurred smoke ellipses and a radial edge darkening.
- **كيف / how:** Seeded random positions; circles r in {1.2,1.6,2.2,3,3.8}; smoke ellipses rx 120-260 ry 18-40 opacity .16 blur20; vignette radialGradient from .55 (transparent) to 1 (black .6).
- **أرقام / params:** embers #fde047 #fbbf24 #fb923c #f97316 op .55-1; vignette r=950
- **الدليل / proof:** `kosif-one/projects/duck-vs-dragon/duck_dragon.py:230-239`

#### PART-11 · انفجار جزيئات بعشوائية مزروعة · Seeded canvas particle burst · ✅ مُثبت هنا
- **ماذا / what:** 160 seeded particles explode from centre with outExpo distance, sine wobble, slight gravity and inOutCubic fade; positions are a pure function of t.
- **كيف / how:** rng(20261015); per particle angle, speed 420-1320 px, size 4-14, 70% #7ee8d2 / 30% #ffb86b; window 7.45-10.4 s
- **أرقام / params:** y stretch 1.4, gravity +120 px over life, wobble 12 px
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:118`

#### PART-12 · بخار ثنائي الأبعاد · 2D vapour / steam puffs · 🟢 جاهز
- **ماذا / what:** Rising, growing, fading SVG circles for steam, smoke or breath.
- **كيف / how:** MOTION.vapour(tl, svgGroup, {n, r, rise, height, drift, spread, color, at, dur, x0, x1, y0, seed}).
- **أرقام / params:** n 70; r 18 px; rise 2.6 s; height 320 px; drift 120 px; scale .5->1.4; color rgba(255,255,255,.55)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:283` · `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:283`

#### PART-13 · تموج قماش وأعلام · Cloth / flag wave · 🟢 جاهز
- **ماذا / what:** Travelling wave anchored at one edge for flags, banners and signs.
- **كيف / how:** K3.addWave(material, {amp, freq, wavelength, span, time}).
- **أرقام / params:** amp .08; freq 2.4; wavelength .9; span 1.0
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:977` · `kosif-studio/motion/kit/three-kit.js:977`

#### PART-14 · بخار ومطر بالجسيمات · GPU vapour and rain points · 🟢 جاهز
- **ماذا / what:** Seeded point sprites with uniforms uT/uOn for rising vapour and falling rain in 3D.
- **كيف / how:** makeVapour({n, region, y, seed}); makeRain({n, region, seed}).
- **أرقام / params:** vapour n 1400, rain n 9000
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:325` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:343` · `kosif-studio/motion/kit/three-kit.js:325`

#### PART-15 · شرر مرتبط بالضربات · Event sparks on the tape clock · 🟢 جاهز
- **ماذا / what:** Sparks thrown at events (kicks) that hang in the air when the track stops.
- **كيف / how:** makeSparks([{t,x,y,z}], {per, speed, seed}).
- **أرقام / params:** 60 sparks per event, speed 5
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:886` · `kosif-studio/motion/kit/three-kit.js:886`

#### PART-16 · طبقة إجرائية حتمية على الكانفس · Deterministic canvas procedural layer · 🟢 جاهز
- **ماذا / what:** Starfields, noise and particle textures drawn per frame from a hash of (index, frame) so every render is identical.
- **كيف / how:** Canvas 2D drawFrame(t) with integer hash instead of Math.random, driven by a GSAP proxy {time} or window.__kosif.seek(t).
- **أرقام / params:** e.g. 200 points, brightness = hash(i, floor(t*10))
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-atlas/skills/3198-remotion/13555-remotion-video-builder`

#### PART-17 · صندوق النويز · Noise toolbox (Perlin/Simplex/Curl/FBM) · 🟢 جاهز
- **ماذا / what:** Organic randomness: Perlin for blobs, Simplex for gradients, Curl for divergence-free fluid motion, FBM for clouds/terrain.
- **كيف / how:** glsl-noise functions pasted into shader; FBM 4-6 octaves; curl noise drives particle velocity.
- **أرقام / params:** FBM 5 octaves typical
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md` · `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/SKILL.md`

#### PART-18 · ضوضاء حتمية بدالة هاش · Deterministic hash noise in canvas · 🟢 جاهز
- **ماذا / what:** Integer hash per (index,time-bucket) gives reproducible flicker/particles so every render is identical.
- **كيف / how:** Canvas 2D drawFrame(t) driven by a GSAP proxy or Remotion frame; never Math.random at render time.
- **أرقام / params:** 200 particles, t*10 buckets
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### PART-19 · حقل جسيمات متناثرة · Golden-ratio drifting particle field · 🟢 جاهز
- **ماذا / what:** 26 soft teal dots spread by golden-ratio offsets that wobble and breathe in opacity over time.
- **كيف / how:** x=(w*(k*.618%1)+sin(phase+k)*15) mod w, y=(h*(k*.381%1)+cos(phase*.67+k)*20) mod h, radius 1.2+(k%3) px, fill rgba(159,236,226, .07..0.23).
- **أرقام / params:** 26 dots; drift ±15 px x, ±20 px y; alpha 0.07–0.23
- **الدليل / proof:** `fastify-motion-bro/web/motion.js:11`

#### PART-20 · مطر ثنائي الأبعاد · 2D rain particles · 🟢 جاهز
- **ماذا / what:** Seeded falling rain streaks (SVG lines or DOM divs) with container fade in/out.
- **كيف / how:** MOTION.rain(tl, container, {n, fall, len, angle, color, at, dur, seed, x0..y1}).
- **أرقام / params:** n 240; fall 0.55 s; len 46 px; angle -8 deg; width 1-2.6 px; color rgba(220,235,255,.75); fade in .6 s out .8 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:265`

#### PART-21 · نجوم متلألئة · Twinkle sparkle field · 🟢 جاهز
- **ماذا / what:** Small seeded dots that twinkle in a region (dust, stars, accents).
- **كيف / how:** MOTION.sparkle(tl, svgGroup, {n, x0, x1, y0, y1, color, at, seed}).
- **أرقام / params:** n 40; r 1-3.2 px; opacity .15<->1 over 0.6-1.8 s yoyo x40; sine.inOut
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:300`

#### PART-22 · ضباب جسيمي · GPU mist / vapour points · 🟢 جاهز
- **ماذا / what:** Rising, drifting additive point sprites for mist or steam over a region.
- **كيف / how:** K3.makeVapour({n, region, y, seed}); userData.set(t, on).
- **أرقام / params:** n 1400; life 6-10 s; rise 520-940 units; additive; alpha x0.16; size cap 170 px
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:325`

#### PART-23 · مطر ثلاثي الأبعاد · GPU rain streaks · 🟢 جاهز
- **ماذا / what:** Thousands of falling streak sprites with wind slant.
- **كيف / how:** K3.makeRain({n, region, top, seed}); userData.set(t, on).
- **أرقام / params:** n 9000; speed 900-1400 u/s; top 1500; slant 120; colour (0.85,0.92,1.0) alpha .55
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:343`

#### PART-24 · ماء ضحل · Shallow pond water shader · 🟢 جاهز
- **ماذا / what:** Sum-of-sines swell with analytic normals, expanding ripple rings, Fresnel sky/bank reflection, GGX sun glint, angle-dependent transparency and dappled light.
- **كيف / how:** const w=K3.makeShallowWater({width, depth, seg, ripples, amp, clarity, glint, skyTop, skyHorizon, bank, deep, shallow}); w.userData.ripple(x,z,t0,amp); w.userData.set(t, sun, sunCol).
- **أرقام / params:** 30x30 m, 256 seg; 6 swell waves amp .012; 24 ripple rings, life 3.5 s, front 0.34 m/s; deep #0d3b3a shallow #2f6f62; sky #6f9cc8/#f2d6b0; bank #26301c
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:506`

#### PART-25 · تمايل النباتات · Wind sway for plants · 🟢 جاهز
- **ماذا / what:** Vertex-shader bend growing with height squared, phase per instance, with gusts.
- **كيف / how:** K3.addSway(material, {amp, freq, time}).
- **أرقام / params:** amp .06; freq 1.3 Hz; gust 0.6+0.4 sin
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:591`

#### PART-26 · بتلات تسقط على الماء · Sakura petals on water · 🟢 جاهز
- **ماذا / what:** Instanced petals fall with flutter, land on the water (each landing sends a ripple) and float.
- **كيف / how:** K3.makePetals({n, region, times:[t0,t1], level, floating, size, water, seed}); userData.set(t).
- **أرقام / params:** n 120; fall 2.4-4.6 s from 1.6-4 m; pink HSL h .96-.99 s .35-.65 l .84-.93; ripple amp .0016-.0024
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:685`

#### PART-27 · شرر على ساعة الشريط · Tape-clock sparks · 🟢 جاهز
- **ماذا / what:** Additive sparks thrown at sound events, moving on the tape clock so they hang in the air when the track stops.
- **كيف / how:** K3.makeSparks([{t,x,y,z}], {per, speed, gravity, drift, color, size}); userData.set(t, tapeFn).
- **أرقام / params:** per 60 per event; speed 5; gravity 6; life .5-1.6 s; colour #ffa040
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:886`

#### PART-28 · حقل جزيئات غبار منجرف · Drifting dust particle field (38 motes) · 🟢 جاهز
- **ماذا / what:** Small luminous dots drift sideways and bob vertically at staggered speeds and opacities; deterministic in t.
- **كيف / how:** for i<38: x = (i·137.3 + t·(5+i%3)) mod w, y = (sin(i·2.71 + t·0.18)·0.42 + 0.5)·h, radius 1+(i%3)·0.5, alpha 0.15+(i%5)·0.09, fill #d5fff0.
- **أرقام / params:** 38 particles; 5–7 px/s drift
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:69`

#### PART-29 · مطر بطبقتين · Two-layer parallax rain · 🟢 جاهز
- **ماذا / what:** Rain as thin slanted strokes in a far layer (many, short, slow) and a near layer (few, long, fast) with different parallax, drawn behind and in front of the action.
- **كيف / how:** rain(t, cam, near): far 152 drops, length 11–25 px, speed 340–600 px/s, width 0.8, opacity .13, colour #86b7c9; near 32 drops, length 37 px, 630 px/s, width 1.3, opacity .17, #95d6df; wrap 1450×850.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:108`

#### PART-30 · رذاذ البرك وحلقة التموج · Puddle splash bursts with ripple ring · 🟢 جاهز
- **ماذا / what:** At each foot impact, 11 droplets fly ballistically and fade while an expanding elliptical ripple ring spreads on the water.
- **كيف / how:** splash(t,p): events at 5.2, 6.9, 7.53, 8.02, 8.55, 9.1 s; droplet vx ±105, vy −45…−129, gravity 145 px/s², life 0.63 s, colour #91e2df; ring rx 4+75a, ry 1+12a.
- **أرقام / params:** 11 droplets per event; 0.63 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:122`

#### PART-31 · ضجيج تجزئة حتمي · Deterministic hash noise for procedural scenes · 🟢 جاهز
- **ماذا / what:** Replaces Math.random with a repeatable hash so every frame of a procedural scene renders identically on re-render.
- **كيف / how:** rnd(i) = fract(sin(i·127.1 + 311.7)·43758.5453123); index by element ids/time-independent seeds.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:9`

#### PART-32 · هالة شعاعية وجسيمات طافية · Radial aura + drifting particle canvas · 🟢 جاهز
- **ماذا / what:** A 2D canvas background with a soft amber/sky radial glow and dozens of small dots drifting upward and wrapping.
- **كيف / how:** kinetic_2d: ctx.createRadialGradient(W/2,H/2,50,W/2,H/2,W*0.7) stops amber .15 / sky .08 / transparent; 60 particles y = (y0 - t*40*speed) mod H, drawn at alpha 0.4. Seed the random generator (e.g. mulberry32) if two renders must match.
- **أرقام / params:** 60 particles, radius 2-6 px, speed factor 1-3 (40-120 px/s), colours #f59e0b / #38bdf8, alpha 0.4; aura radius 0.7*W
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/kinetic_2d.html:128` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/kinetic_2d.html:150`

#### PART-33 · مطر ثنائي الأبعاد · 2D seeded rain · 🟢 جاهز
- **ماذا / what:** Slanted rain streaks in SVG or HTML, each with seeded length/width/speed, fading in and out.
- **كيف / how:** MOTION.rain(tl, container, {n, x0..y1, fall, len, angle, color, at, dur, seed}).
- **أرقام / params:** n 240, fall 0.55 s, len 46 px (x0.6-1.4), width 1-2.6 px, angle -8 deg, color rgba(220,235,255,.75), fadeIn 0.6 s, fadeOut 0.8 s
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:265`

#### PART-34 · نجوم متلألئة · Twinkling sparkle field · 🟢 جاهز
- **ماذا / what:** Seeded dots twinkling (yoyo opacity) across a region: stars, dust, magic.
- **كيف / how:** MOTION.sparkle(tl, container, {n, x0..y1, color, at, seed}).
- **أرقام / params:** n 40, r 1-3.2 px, opacity 0.15<->1, 0.6-1.8 s, 40 repeats
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:300`

#### PART-35 · سرب طيور · Flapping bird flock · 🟢 جاهز
- **ماذا / what:** Instanced V-shaped birds flapping along a keyed path with seeded offsets, visible between t0 and t1.
- **كيف / how:** makeFlock({n, path:[[t,x,y,z]...], seed}); flock.userData.set(t).
- **أرقام / params:** n 18
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:203`

#### PART-36 · ماء ضحل شفاف بتموجات · Shallow see-through water with ripples · 🟢 جاهز
- **ماذا / what:** Sum-of-sines swell with analytic normals, ripple rings from petals/drops/fish, Fresnel sky reflection, GGX sun glint and depth-tinted transmission.
- **كيف / how:** makeShallowWater({width, depth, seg, ripples}); add rings at events.
- **أرقام / params:** 30x30 m, 256 segments, up to 24 rings
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:506`

#### PART-37 · تمايل الريح وتموج القماش · Wind sway and cloth wave shaders · 🟢 جاهز
- **ماذا / what:** Vertex shader patches: plants bend with height squared (sway); flags/banners ripple from an anchored edge (wave).
- **كيف / how:** addSway(material, {amp, freq}); addWave(material, {amp, freq, wavelength, span}).
- **أرقام / params:** sway amp 0.06, 1.3 Hz; wave amp 0.08, 2.4 Hz, wavelength 0.9
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:591` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:977`

#### PART-38 · بتلات ساكورا تتساقط وتطفو · Falling and floating sakura petals · 🟢 جاهز
- **ماذا / what:** Instanced petals fall with seeded flutter, land on water (ringing it) and drift/bob.
- **كيف / how:** makePetals({n, region, times, floating, level, seed}).
- **أرقام / params:** n 120, region [-4,4,-3,3], times [0,8]
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:685`

#### PART-39 · غيوم ودخان وبخار من عناقيد بيضاوية · Ellipse-cluster clouds, smoke and steam · 🟢 جاهز
- **ماذا / what:** Seeded clusters of ellipses tapered toward the ends read as clouds when blurred; offset copies in screen/add give moonlit tops and fire-lit bellies.
- **كيف / how:** scenes/dragon_girl.cloud(cx, cy, w, h, n, seed) + fill(blur 12-20) + translated fill(mode='screen'|'add').
- **أرقام / params:** ellipse widths w*.07-.16, heights h*.3-.6; blur 13-17
- **الدليل / proof:** `kosif-studio/scenes/dragon_girl.py:36` · `kosif-studio/scenes/dragon_girl.py:165` · `kosif-studio/scenes/whale_dragon.py:257`

#### PART-40 · حقل نجوم · Starfield with sky-weighted density · 🟢 جاهز
- **ماذا / what:** Seeded stars denser near the top, kept clear of the moon, with larger stars getting a soft blue halo.
- **كيف / how:** y = 480*rand^1.7; dots(...) '#e4e9ff' .9 add; halos r*3.5 '#7f93ff' .35 blur 2.5.
- **أرقام / params:** 280 stars, sizes .45/.55/.7/.9/1.25
- **الدليل / proof:** `kosif-studio/scenes/dragon_girl.py:144`

#### PART-41 · الشرر والجمر على مسار · Embers and sparks along a path · 🟢 جاهز
- **ماذا / what:** Sparks scattered with Gaussian noise along the fire's path and drifting upward, kept off the hero's face, with glowing larger embers.
- **كيف / how:** dots(emb) '#ffd27a' .9 add + halos x3 '#ff7a2a' .45 blur 2.4; order='sparkle'.
- **أرقام / params:** dragon_girl 320 + 120 ambient; whale 220; sigma 44/36 px, lift up to 100
- **الدليل / proof:** `kosif-studio/scenes/dragon_girl.py:408` · `kosif-studio/scenes/whale_dragon.py:282`

#### PART-42 · البخار عند تصادم النار والماء · Steam at a fire-water collision · 🟢 جاهز
- **ماذا / what:** Screen-mode cloud cluster with multiply noise, a warm add offset beneath, a hot core glow, curling flame tongues in six directions and warm spray dots.
- **كيف / how:** cloud(...) fill '#d6dde6' .45 blur 12 screen; noise .5 cell 20; translate +14 '#ff8a3a' .32 add; glow '#fff0c0' 26 .7; 6 tongues.
- **الدليل / proof:** `kosif-studio/scenes/whale_dragon.py:257`

#### PART-43 · مولد عشوائي مزروع · mulberry32 seeded rng helper · 🟢 جاهز
- **ماذا / what:** Small seeded PRNG for repeatable procedural layouts across renders.
- **كيف / how:** KOSIF.rng(seed)()
- **الدليل / proof:** `kosif-tool/starters/html-canvas/timeline.js:40`

#### PART-44 · انفجار مزروع البذرة · Seeded burst · 🟢 جاهز
- **ماذا / what:** Analytic burst computed from t: distance by easeOutExpo, gravity, alpha fade.
- **كيف / how:** Canvas drawBurst: KOSIF.rng(20261015), 160 parts {a, sp 400–1300, r 4–14}; d=outExpo(life)·sp; alpha 1−inOutCubic(life); y += life·120; r shrinks 60%.
- **أرقام / params:** speed 400–1300 px/s; gravity 60–150 px/s²; lifetime 0.7–1.0
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:25` · `kosif-tool/playbooks/particles.md:52-66` · `kosif-tool/starters/html-canvas/index.html:118`

#### PART-45 · أدوات الضوضاء في الشيدر · GLSL noise toolbox · 📦 بأمر تثبيت
- **ماذا / what:** Perlin/Simplex for organic fields, curl noise for divergence-free fluid particle motion, FBM for clouds/terrain, domain warping (warp the warp) for curling flow.
- **كيف / how:** glsl-noise functions in fragment shaders; blob = vertex displacement pnoise(position*1.5 + t*0.5); FBM 5 octaves; for video drive uniform time from frame/fps, not clock.elapsedTime.
- **أرقام / params:** FBM 5 octaves; freq 1.5; speed 0.5
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md` · `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/SKILL.md`

#### PART-46 · جسيمات على المعالج الرسومي · GPU particle systems (FBO) · 📦 بأمر تثبيت
- **ماذا / what:** Store particle positions in a float texture, update them in a simulation shader rendered to an offscreen target, and read that texture in the points shader for 100k+ particles.
- **كيف / how:** DataTexture RGBA per particle -> SimulationMaterial -> WebGLRenderTarget (useFBO) -> points uniform uPositions; glow points via distance(gl_PointCoord,0.5); basic BufferGeometry points for small counts. Seed positions deterministically for render.
- **أرقام / params:** 100k+ particles
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### PART-47 · جسيمات بالحوسبة على GPU · GPU compute particles (100k) · 📦 بأمر تثبيت
- **ماذا / what:** Simulate 100k particles with gravity/bounce on the GPU via storage buffers.
- **كيف / how:** TSL instancedArray(N,'vec3') for positions/velocities; Fn(...)().compute(N); renderer.compute(update) per frame; sprite/instanced mesh reads buffers.
- **أرقام / params:** N=100000, gravity -9.8, bounce 0.7, friction 0.98, hitStrength 5
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/examples/particle-system.js` · `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/compute-shaders.md`

#### PART-48 · نقاط مضيئة جمعية · Additive glowing point sprites · 📦 بأمر تثبيت
- **ماذا / what:** Soft round glowing particles from gl_PointCoord falloff.
- **كيف / how:** Fragment: s=pow(1-distance(gl_PointCoord,0.5),3); AdditiveBlending, depthWrite=false.
- **أرقام / params:** count 5000, spread ±2, falloff power 3
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### PART-49 · محاكاة جسيمات عبر FBO · FBO particle simulation · 📦 بأمر تثبيت
- **ماذا / what:** Store positions in a float texture and update in a simulation pass for 100k+ particles in WebGL.
- **كيف / how:** DataTexture RGBA Float; SimulationMaterial renders to useFBO target; render pass reads uPositions. Ping-pong two targets.
- **أرقام / params:** 100k+
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### PART-50 · سقوط فيزيائي · Rapier physics drops · 📦 بأمر تثبيت
- **ماذا / what:** Rigid-body voxels/logos falling and stacking with real physics.
- **كيف / how:** @react-three/rapier or rapier3d; for deterministic video, step fixed dt=1/fps per frame.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md` · `kosif-atlas/skills/2696-game-studio/10367-react-three-fiber-game/SKILL.md`

#### PART-51 · مجموعة دوال الضوضاء · Noise family toolkit · 📦 بأمر تثبيت
- **ماذا / what:** Perlin for organic blobs, Simplex for gradients, Curl for divergence-free fluid particle flow, FBM for clouds/terrain.
- **كيف / how:** GLSL (three.js/R3F) or JS simplex-noise; flow field = sample curl noise per particle per frame and integrate positions.
- **أرقام / params:** FBM 4-6 octaves
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`

#### PART-52 · طبقات التدفق في deck.gl · deck.gl flow layers · 📦 بأمر تثبيت
- **ماذا / what:** GPU layers for animated movement on maps: timestamped trips, origin-destination arcs, paths, hex aggregation.
- **كيف / how:** TripsLayer with currentTime driven by the frame for fading trails; ArcLayer for OD links (state whether geodesic or schematic); PathLayer/LineLayer static; HexagonLayer/GridLayer for density; overlay on MapLibre/Mapbox/Google. Width/color carry volume; trails carry direction/recency.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/deckgl-d3-geo-stack-selection.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/particle-effects-and-flow.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/webgl-2d-animation-patterns.md`

#### PART-53 · أنظمة الجزيئات الخمسة · Particle systems (5) · 📦 بأمر تثبيت
- **ماذا / what:** Deterministic particle overlays that are a pure function of time.
- **كيف / how:** drawParticles(): dust (54 white dots rising 1.8%/s, twinkle alpha 0.18-0.48), bokeh (16 screen-blended discs 3-10% m in primary/accent, alpha 0.08-0.15), sparks (54 accent dots rising 12%/s in 'lighter'), snow (54 white falling 6%/s), confetti (46 rotating flips in accent/primary/text/#ff6b5e falling 16%/s); positions from rnd(i) = frac(sin(i*127.1+311.7)*43758.5453).
- **أرقام / params:** dust|bokeh|sparks|confetti|snow
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:234`

#### PART-54 · قصاصات الاحتفال · Confetti · 📦 بأمر تثبيت
- **ماذا / what:** Seeded, deterministic confetti burst with gravity.
- **كيف / how:** Install with `npx hyperframes add confetti` (copies to compositions/components/confetti.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame captur…
- **تثبيت / install:** `npx hyperframes add confetti` (copies to compositions/components/confetti`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/confetti/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/confetti/confetti.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/confetti.mdx`

#### PART-55 · كشف صورة بالجزيئات · Particle Image Reveal · 📦 بأمر تثبيت
- **ماذا / what:** Seeded particle field converges while a slotted image reveals beneath, trails thinning until clean.
- **كيف / how:** Install with `npx hyperframes add particle-image-reveal` (copies to compositions/components/particle-image-reveal.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (head…
- **أرقام / params:** density low|med|high; direction ltr|center; vars: density=med[low|med|high]; direction=ltr[ltr|center]; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add particle-image-reveal` (copies to compositions/components/particle-image-reveal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/particle-image-reveal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/particle-image-reveal/particle-image-reveal.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/particle-image-reveal.mdx`

#### PART-56 · نص من الجزيئات · Particle Text Dissolve · 📦 بأمر تثبيت
- **ماذا / what:** Text assembles from (or dissolves into) seeded particles whose targets are sampled once from the rendered text bitmap; one onUpdate painter, no per-particle tweens.
- **كيف / how:** Install with `npx hyperframes add particle-text-dissolve` (copies to compositions/components/particle-text-dissolve.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (he…
- **أرقام / params:** direction in|out; vars: text=Dissolve; direction=in[in|out]; density=med[low|med|high]; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add particle-text-dissolve` (copies to compositions/components/particle-text-dissolve`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/particle-text-dissolve/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/particle-text-dissolve/particle-text-dissolve.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/particle-text-dissolve.mdx`

#### PART-57 · تأرجح البندول · Pendulum Swing · 📦 بأمر تثبيت
- **ماذا / what:** Content hanging from a pivot swings into rest with gravity-damped oscillation.
- **كيف / how:** Install with `npx hyperframes add pendulum-swing` (copies to compositions/components/pendulum-swing.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium …
- **أرقام / params:** pivot top-center|top-left|top-right; amplitude gentle|standard|wide; vars: pivot=top-center[top-center|top-left|top-right]; amplitude=standard[gentle|standard|wide]; direction=right[right|left]; tone=ink[ink|paper|accent]
- **تثبيت / install:** `npx hyperframes add pendulum-swing` (copies to compositions/components/pendulum-swing`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/pendulum-swing/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/pendulum-swing/pendulum-swing.html` · `kosif-one/vendor/hyperframes/registry/components/pendulum-swing/demo.html`

#### PART-58 · خروج فيزيائي · Physical Exit · 📦 بأمر تثبيت
- **ماذا / what:** Card leaves with physical momentum (toss, drop, slide) keeping acceleration and rotation, no fade.
- **كيف / how:** Install with `npx hyperframes add physical-exit` (copies to compositions/components/physical-exit.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fr…
- **أرقام / params:** mode toss|drop|slide; vars: mode=toss[toss|drop|slide]; text=Later; accent=green[green|blue|violet]
- **تثبيت / install:** `npx hyperframes add physical-exit` (copies to compositions/components/physical-exit`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/physical-exit/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/physical-exit/physical-exit.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/physical-exit.mdx`

#### PART-59 · خلط الرصة · Spring Stack Shuffle · 📦 بأمر تثبيت
- **ماذا / what:** Stack of 3-5 slotted cards reshuffles on cues: back card arcs over and lands in front with mass; mid-flight cues redirect with velocity preserved.
- **كيف / how:** Install with `npx hyperframes add spring-stack-shuffle` (copies to compositions/components/spring-stack-shuffle.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headle…
- **أرقام / params:** cues "0.9, 1.7, 1.95"; vars: cards=4(3..5); cues=0.9, 1.7, 1.95; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add spring-stack-shuffle` (copies to compositions/components/spring-stack-shuffle`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/spring-stack-shuffle/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/spring-stack-shuffle/spring-stack-shuffle.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/spring-stack-shuffle.mdx`

#### PART-60 · تساقط الثلج · Snow · 📦 بأمر تثبيت
- **ماذا / what:** Seek-safe falling snow overlay; per-flake size/speed/opacity correlated for depth, radial mask keeps centre clear.
- **كيف / how:** Install with `npx hyperframes add snow` (copies the full composition to compositions/snow.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** density sparse|dense; speed calm|gust; 6 s; vars: density=sparse[sparse|dense]; speed=calm[calm|gust]; 1920x1080; duration 6 s
- **تثبيت / install:** `npx hyperframes add snow` (copies the full composition to compositions/snow`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/snow/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/snow/snow.html` · `kosif-one/vendor/hyperframes/registry/blocks/snow/demo.html`

#### PART-61 · المجرة الحلزونية · Spiral Galaxy · 📦 بأمر تثبيت
- **ماذا / what:** Spiral galaxy with differential rotation (inner stars faster) using 20,000 additive GPU sprites solved directly from time.
- **كيف / how:** Install with `npx hyperframes add spiral-galaxy` (copies the full composition to compositions/spiral-galaxy.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.147.0 (CDN), WebGL fragment shader, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** stars 20000; arms 3; rate 0.25; glow 1.9; core #ffa575; rim #311599; Three 0.147; vars: stars=20000(2000..40000); arms=3(2..8); rate=0.25(0..1.5); glow=1.9(0.2..4); size=10(2..40); core=#ffa575; rim=#311599; 1920x1080; duration 10 s
- **تثبيت / install:** `npx hyperframes add spiral-galaxy` (copies the full composition to compositions/spiral-galaxy`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/spiral-galaxy/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/spiral-galaxy/spiral-galaxy.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/spiral-galaxy.mdx`

#### PART-62 · حقل النجوم · Starfield · 📦 بأمر تثبيت
- **ماذا / what:** Seek-safe night sky: three size tiers twinkle and drift in two parallax layers, radial mask keeps centre clear.
- **كيف / how:** Install with `npx hyperframes add starfield` (copies the full composition to compositions/starfield.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** density sparse|dense; tone warm|cool|white; speed slow|fast; vars: density=sparse[sparse|dense]; tone=warm[warm|cool|white]; speed=slow[slow|fast]; 1920x1080; duration 6 s
- **تثبيت / install:** `npx hyperframes add starfield` (copies the full composition to compositions/starfield`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/starfield/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/starfield/starfield.html` · `kosif-one/vendor/hyperframes/registry/blocks/starfield/demo.html`

#### PART-63 · خلفية سائلة · Liquid Background · 📦 بأمر تثبيت
- **ماذا / what:** Liquid simulation by vertex displacement on a subdivided plane with HTML floating above the rippling surface.
- **كيف / how:** Install with `npx hyperframes add vfx-liquid-background` (copies the full composition to compositions/vfx-liquid-background.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.147.0 (CDN), HTML-in-Canvas (canvas layoutsubtree + ctx.drawElementImage, experimental Chromium API), WebGL fragment shader, Canvas 2D painter, inline SVG,…
- **أرقام / params:** 12 s; Google Fonts: Inter; 1920x1080; duration 12 s
- **تثبيت / install:** `npx hyperframes add vfx-liquid-background` (copies the full composition to compositions/vfx-liquid-background`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/vfx-liquid-background/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/vfx-liquid-background/vfx-liquid-background.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/vfx-liquid-background.mdx`

#### PART-64 · كرة لزجة · Goo · 📦 بأمر تثبيت
- **ماذا / what:** Glossy green liquid ball whose surface bulges and ripples. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add goo` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="Goo" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="Goo"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add goo` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/goo/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/goo/goo.html` · `kosif-one/vendor/hyperframes/registry/blocks/goo/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### PART-65 · سديم · Nebula · 📦 بأمر تثبيت
- **ماذا / what:** Pink and blue gas swirling inside a small sphere. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add nebula` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="Nebula" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="Nebula"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add nebula` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/nebula/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/nebula/nebula.html` · `kosif-one/vendor/hyperframes/registry/blocks/nebula/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### PART-66 · إزاحة تصادمية فيزيائية · Reactive displacement collision · 📦 بأمر تثبيت
- **ماذا / what:** An entering element's tween drives the exiting element's displacement (three concurrent tweens), victim finishing before the intruder for hit-then-settle; optional damped wobble.
- **كيف / how:** Read hyperframes-animation/rules/reactive-displacement.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** victim durations 40-50% of intruder; intruder back.out(BOUNCE)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/reactive-displacement.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### PART-67 · انفجار جسيمات وقصاصات حتمي · Deterministic particle / confetti burst · 📦 بأمر تثبيت
- **ماذا / what:** Confetti pop with gravity drift, dot burst behind text, glyph dissolve to particles; fixed pool, index-seeded launch values, one ease-none driver computing ballistic positions as pure function of T.
- **كيف / how:** Read hyperframes-animation/rules/particle-burst.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** <= ~40 particles; gravity G in closed form; chip border-radius 2 px (50% for dots)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/particle-burst.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### PART-68 · حركة إيقاعية: gooey-metaball · Beat motion primitive: gooey-metaball · 📦 بأمر تثبيت
- **ماذا / what:** Gooey metaball merge field, anchored to music events (build / drop).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/gooey-metaball/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: build / drop; best span 1.5-3.0 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/gooey-metaball/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### PART-69 · حركة إيقاعية: particle-burst · Beat motion primitive: particle-burst · 📦 بأمر تثبيت
- **ماذا / what:** Particle explosion burst, anchored to music events (drop / crash).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/particle-burst/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: drop / crash; best span 0.2-1.2 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/particle-burst/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### PART-70 · حركة إيقاعية: radial-burst-lines · Beat motion primitive: radial-burst-lines · 📦 بأمر تثبيت
- **ماذا / what:** Radial speed-lines burst, anchored to music events (drop / surge).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/radial-burst-lines/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: drop / surge; best span 0.2-0.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/radial-burst-lines/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### PART-71 · حركة إيقاعية: bg-flow-field · Beat motion primitive: bg-flow-field · 📦 بأمر تثبيت
- **ماذا / what:** Generative curl-noise background bed, anchored to music events (energy / whole span bed).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/bg-flow-field/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: energy / whole span bed; best span 4-12 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/bg-flow-field/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### PART-72 · أدوات الكيت القديم · Legacy kit eases and FX · 📦 بأمر تثبيت
- **ماذا / what:** ease slam/snap/drive/settle, rain, vapour, sparkle, camera, flash, stepped grain, vignette.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** MOTION.ease.*, rain, vapour, sparkle, flash, grain, vignette
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### PART-73 · الماء الضحل والكاوستكس · Shallow water + caustics · 📦 بأمر تثبيت
- **ماذا / what:** Sum-of-sines swell, ripple rings, Fresnel, GGX glint, transmission; procedural caustics on sunlight with depth absorption.
- **كيف / how:** three-kit.js (window.K3) in a --3d project; render --engine studio
- **أرقام / params:** caustic scale ≈5.5 (5–15 cm cells); makeShallowWater, addCaustics
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:106` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### PART-74 · حقل لمعان متلألئ ببذرة · Seeded twinkling sparkle field · 📦 بأمر تثبيت
- **ماذا / what:** Small SVG dots twinkle (yoyo opacity) across a region at random phases; reproducible by seed.
- **كيف / how:** M.sparkle(tl, group, {at:0, n:48, seed:5, x0:0, x1:1080, y0:200, y1:1700, color:'#ffe9b8'}) → circles r 1–3.2, opacity .15↔1, 0.6–1.8 s sine.inOut, repeat 40.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:66` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:300`

#### PART-75 · ذرات غبار تطفو فوق اللقطة · Drifting dust motes over footage · 📦 بأمر تثبيت
- **ماذا / what:** Warm seeded dust particles rise and fade during the 'dream' and 'lift' moments, screen-blended over the plate.
- **كيف / how:** 34 divs, size 4–13 px, radial rgba(255,232,190,.95)→0, screen; drift 60–200 px; opacity .35–.85 over 1 s then rise and fade over 1.6 s; delays 0–0.6 s; M.rng(31).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:157`

#### PART-76 · شرر الكسر وحلقة الوميض · Snap sparks and flash ring · 📦 بأمر تثبيت
- **ماذا / what:** When a member breaks, deterministic sparks fly ballistically from its midpoint and a camera-facing torus ring expands; the same ring returns in green for the repair.
- **كيف / how:** 26 Points, soft sprite, additive, colour 0xffb08a, size .0075; pos = mid + v·k − (0, 0.9k²); opacity 1−ts/0.6; ring Torus(1, .06) scale .004+.04·easeOut(ts/0.4), colour 0xff907a → 0x9dffb4 on swap.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:93` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:170`

#### PART-77 · شرر على كل ضربة وجمر يتبع ساعة الشريط · Kick-triggered sparks and embers on the tape clock · 📦 بأمر تثبيت
- **ماذا / what:** Every kick drum throws a burst of sparks from the lava river; 2400 slow embers drift in the air; both freeze mid-air when the tape stops.
- **كيف / how:** makeSparks(kicks.map(t→{t,x:0,y:.1,z:0}), {per 90, speed 6.5, gravity 7, drift 15 m/s, size 4.5, seed 11}); sparks.userData.set(t, tape); embers wrap along 120 m, colour 0xff9a5a, size .09 additive.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:56` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:61`

#### PART-78 · قفزة سمكة: حلقات ورذاذ · Fish jump: rings and spray · 📦 بأمر تثبيت
- **ماذا / what:** A fish breaks a moonlit surface: 60 spray points arc under gravity and two additive rings expand and decay, the second 0.35 s later.
- **كيف / how:** rings opacity .9·exp(−0.9u), scale 0.6+3.4u; spray v ∈ (±.8, 1.4–3.4, ±.8), y = .05 + vy·u − 4.9u², u ≤ 0.7 s, opacity .8·(1−ft/.7); at 2.8 s, 6.5 m off the bow; paired with a splash SFX.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:205` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:238`

#### PART-79 · حقول نجوم: أقواس دوّارة وتلألؤ · Star fields: rotating arcs and twinkling scintillation · 📦 بأمر تثبيت
- **ماذا / what:** Two star recipes: a sphere of stars rotating about the pole (exaggerated so a long exposure draws arcs) and a seeded sky where each star twinkles at its own rate, more near the horizon, washed out near the moon.
- **كيف / how:** blue_hour: 1600 points r 8000, brightness pow(rand,3), size 2+3.5b, pole rotation (−.45,0,.25), y-rot 0.011·t; night_boat: 2600 points r 10000, tw = .75+.25·sin(t(3+.2f)+f)·(1−y), moonWash smoothstep(.995,.93, d·moon), size 1.4+2.2b.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:44` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:164`

#### PART-80 · مسارات ضوء السيارات · Light trails from moving cars · 📦 بأمر تثبيت
- **ماذا / what:** Tail lights going away and headlights coming in become continuous streaks during a long-exposure render by stretching each light along its motion.
- **كيف / how:** 18 cars, 22–27 m/s, wrap 1560 m; tail 0xff1e1e×6, head 0xfff1d8×6 spheres r .16; scale.z = 1 + trailLength(v)/(2·0.16)·1.2 and offset forward so the streak never sits inside the body.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:107`

#### PART-81 · حياة طبيعية: أسماك كوي وبتلات وزنابق وقصب · Nature life: koi, petals, lily pads, reeds and grass · 📦 بأمر تثبيت
- **ماذا / what:** A living pond: seven koi bend as they swim looping Lissajous paths at different depths, 170 petals fall and float (landing rings on water), 34 lily pads bob, 2200 reeds and 6000 grass blades sway in wind.
- **كيف / how:** makeKoi({seed, length .62–.92, amp .10–.14, caustics}); path x = cx + ax·sin(dir·w·t+ph), z = cz + az·sin(2·dir·w·t+ph2), depth −.22…−.52; makePetals({n 170, floating .45, water, size 1.5}); makeBlades({n 2200, tall .95, amp .07, freq 1.2}) and ({n 6000, tall .22, amp .25, freq 1.7}); pads notched CircleGeometry(.2, 28, .25, 2π−.25), bob .004.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:50` · `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:66` · `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:78`

#### PART-82 · أنظمة الطقس: بخار وسحب ومطر وطيور · Weather systems: vapour, cloud slab, rain, flocks · 📦 بأمر تثبيت
- **ماذا / what:** An explainer drives evaporation vapour, a volumetric cloud slab whose cover and colour follow the story, rain, a flowing river reveal and two bird flocks crossing near the focus plane.
- **كيف / how:** makeVapour({region}) set(t, ramp(2.6,3.6)·(1−ramp(6.2,7.2))); makeCloudSlab set(t, cover, overcast, sun, camPos, light, shadow 0x9fb6cc→0x56616d); makeRain set(t, ramp(9.5,10.3)·(1−ramp(12.6,13.4))); makeRibbon river reveal(ramp(12.6,14.4)); makeFlock({n 16, t0 2.9, t1 4.8, size 16, spread 220, path}); forest on slopes ≤ .42, 28–430 m.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:34` · `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:83`

#### PART-83 · حركة من فيديو · Mocap from video to particles · 📦 بأمر تثبيت
- **ماذا / what:** Median background, difference, morphology, seeded points -> JSON -> particle body.
- **كيف / how:** motion.py mocap; makeParticleBody
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### PART-84 · تكامل: algorithmic-art skill · Integration: algorithmic-art skill · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### PART-85 · حقل جسيمات مضيئة ثلاثي الأبعاد · Additive point-sprite star field · 📦 بأمر تثبيت
- **ماذا / what:** Hundreds of glowing points scattered in a volume and slowly rotating, adding depth and sparkle around the hero.
- **كيف / how:** cinematic_3d: BufferGeometry with 400 random positions in a 20x25x20 box; PointsMaterial{color #38bdf8, size 0.08, opacity .75, AdditiveBlending}; particles.rotation.y = 0.08*t.
- **أرقام / params:** 400 points, size 0.08, opacity 0.75, rotation 0.08 rad/s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:165` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:211`

#### PART-86 · شيدر ماء بالموج واللمعان · Stylised water shader (waves, fresnel, sparkle) · 📦 بأمر تثبيت
- **ماذا / what:** Moving water with three summed sine waves, analytic normals, fresnel sky reflection, a hot sun specular, hashed glints and exponential-squared fog.
- **كيف / how:** Vertex: a=sin(x*.045+1.1t)*.7+sin(z*.06+.8t)*.6+sin((x+z)*.13+1.9t)*.25 scaled by amp; fragment: fres=pow(1-N.V,4), spec=pow(R.L,400)*14+pow(R.L,24)*.5, sparkle step(.9965, hash(floor(xz*1.6)+floor(9t))), fog 1-exp(-(d*fogDen)^2).
- **أرقام / params:** Nile: deep #0A3A66 sky #7FB2E0 amp .12; sea: deep #051833 sky #5E70A8 amp 1 sparkle .8
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html:100-120` · `kosif-one/projects/egypt-2120-animation/index.html:278-280` · `kosif-one/projects/egypt-2120-animation/index.html:380-382`

#### PART-87 · آثار ضوئية من تاريخ الحركة · Light trails from time-sampled history · 📦 بأمر تثبيت
- **ماذا / what:** Moving lights leave fading streaks: each mover is drawn K times at slightly earlier times with shrinking size and alpha.
- **كيف / how:** For k in 0..K-1 sample position at t-k*dt, size = head ? 3.4-4.2 : 2.2-2.6*(1-k/K), alpha = head ? 1 : .55-.7*(1-k/K); used for 36 drones x16 samples (dt .045), 9 sky lanes x30 taxis x14 (dt .03), maglev trail 70 samples along the curve.
- **أرقام / params:** drones 36x16, lanes 9x30x14 colours #55E6FF #FF5AD9 #FFD27A #FFFFFF, maglev trail #7FE9FF
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html:246-258` · `kosif-one/projects/egypt-2120-animation/index.html:356-367` · `kosif-one/projects/egypt-2120-animation/index.html:312`

#### PART-88 · بتلات ورد تتساقط كدالة للزمن · Seeded falling petals as a pure function of time · 📦 بأمر تثبيت
- **ماذا / what:** Rose petals fall, drift, sway and spin forever but every frame is computed from t alone, so seeking is exact.
- **كيف / how:** 22 petals from M.rng(11): x, scale .7-1.5, fall period 7-12 s, phase; y=-60+u*2050 with u=(t/dur+ph)%1; x+=drift*u (±170) + sin(1.3t+9ph)*sway (20-50); rotate spin*u (±300-700); driven by a proxy tween {t:0->T} with onUpdate.
- **أرقام / params:** colours #e8436a / #f27b93 op .9
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html:170-184`

#### PART-89 · موج بحر متحرك · Animated sea wave path · 📦 بأمر تثبيت
- **ماذا / what:** A flat-style sea surface rebuilt every frame from a sine wave, with a foam stroke along the crest.
- **كيف / how:** for x in -20..1000 step 20: y=790+9 sin(x/180*2PI+2.2t); fill path with gradient #2B86E0 -> #1559A8; foam stroke #CFE9FF 5 px op .8.
- **أرقام / params:** amplitude 9 px, wavelength 180 px, speed 2.2 rad/s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/index.html:147-150`

#### PART-90 · خيوط بخار صاعدة · Rising vapour wisps · 📦 بأمر تثبيت
- **ماذا / what:** Evaporation drawn as wavy lines that rise from the sea, sway and fade in/out over their life.
- **كيف / how:** 14 wisps (7 x positions, 2 waves 1.05 s apart, start 1.6+0.17i), life 1.7 s; 9-point polyline with x+14 sin(y/60+5t+x); y0=770-420p; opacity sin(PI p)*.9; stroke #7FBFFF 8 px round.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/index.html:107` · `kosif-one/projects/water-cycle-animation/index.html:152-157`

#### PART-91 · خطوط مطر · Seeded rain streaks · 📦 بأمر تثبيت
- **ماذا / what:** Rain as short slanted lines falling in a loop below the cloud base, faded in and out by stage.
- **كيف / how:** 38 drops from LCG seed 7 (x 1240-1660), y=340+((950t+off)%470), line 28 px long slanted 6 px, stroke #3D8BFF 6 px; opacity fadeWin(t,6.3,8.3,.3). Motion Kit also has M.rain (240 drops, angle -8 degrees, fall .55 s).
- **أرقام / params:** fall speed 950 px/s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/index.html:117-118` · `kosif-one/projects/water-cycle-animation/index.html:171-174` · `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:265-282`

#### PART-92 · جسيمات المكتبة: مطر وبخار ولمعان · Kit particles: rain, vapour, sparkle · 📦 بأمر تثبيت
- **ماذا / what:** Three seeded particle generators that work in SVG or HTML containers: slanted rain streaks, rising puffs of vapour and twinkling dots.
- **كيف / how:** M.rain(tl,c,{n:240,fall:.55,len:46,angle:-8,at,dur}); M.vapour(tl,c,{n:70,r:18,rise:2.6,height:320,drift:120}); M.sparkle(tl,c,{n:40,x0,x1,y0,y1,color,at}) opacity .15 <-> 1 over 0.6-1.8 s yoyo.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:264-308`

#### PART-93 · سطح ماء مرسوم · Painted water surface · 📦 بأمر تثبيت
- **ماذا / what:** Stretched-noise water with sky reflection and light glints in an area.
- **كيف / how:** water(area, lights, deep='#0a1118', sky='#2a3a4c', cell=18, stretch=6).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/render.py:652`

#### PART-94 · سطح ماء · Scene op: water surface · 📦 بأمر تثبيت
- **ماذا / what:** KOSIF Studio scene operation: water.
- **كيف / how:** water(area,lights,deep #0a1118,sky #2a3a4c,cell 18,stretch 6,height,...)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md` · `100-superskills/skills/pixel-studio-painter/scripts/render.py`

#### PART-95 · مطر · SVG/DOM rain · 📦 بأمر تثبيت
- **ماذا / what:** Seeded rain streaks (SVG lines or divs) falling on repeat with fade in/out.
- **كيف / how:** MOTION.rain(tl, container, {n, fall, len, angle, color, at, dur, seed, x0..y1}).
- **أرقام / params:** n 240, fall .55 s, length 46 px (×0.6-1.4), angle -8°, width 1-2.6 px, colour rgba(220,235,255,.75), fadeIn .6 fadeOut .8
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:265`

#### PART-96 · بخار · SVG vapour puffs · 📦 بأمر تثبيت
- **ماذا / what:** Rising, growing, fading circles for steam/evaporation explainers.
- **كيف / how:** MOTION.vapour(tl, svgGroup, {n, r, rise, height, drift, spread, at, dur, x0, x1, y0}).
- **أرقام / params:** n 70, radius 18 px (×0.6-1.7), rise 2.6 s, height 320 px, drift 120 px, scale .5->1.4, sine.out
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:283`

#### PART-97 · تلألؤ · Sparkle field · 📦 بأمر تثبيت
- **ماذا / what:** Seeded twinkling dots.
- **كيف / how:** MOTION.sparkle(tl, svgGroup, {n, x0..y1, at, color, seed}).
- **أرقام / params:** n 40, r 1-3.2 px, opacity .15<->1 over .6-1.8 s, yoyo 40 repeats
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:300`

#### PART-98 · سرب طيور · Bird flock · 📦 بأمر تثبيت
- **ماذا / what:** Instanced flapping V-birds following a keyed path with seeded offsets, visible in a time window.
- **كيف / how:** K3.makeFlock({n, path:[[t,x,y,z]...], t0, t1, spread, size, color}); mesh.userData.set(t).
- **أرقام / params:** n 18, spread 120, size 9, flap sin(9t), colour #1a1d22
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:203`

#### PART-99 · سحب مرسومة بالأشعة · Raymarched cloud slab · 📦 بأمر تثبيت
- **ماذا / what:** Volumetric cloud layer inside a box: 36 march steps, 3 light taps, powder term, coverage and darkness controls.
- **كيف / how:** K3.makeCloudSlab({size, center}); clouds.userData.set(t, cover, dark, sun, camPos, sunCol, skyCol).
- **أرقام / params:** size [7000,520,4200], centre [0,1240,-900], sky #9fb6cc, sun #fff2d9
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:273`

#### PART-100 · ماء ضحل شفاف · Shallow see-through water · 📦 بأمر تثبيت
- **ماذا / what:** Sum-of-sines swell with analytic normals, ripple rings, Fresnel reflection that mirrors dark banks near the horizon, GGX sun glint and depth-tinted transmission.
- **كيف / how:** K3.makeShallowWater({width, depth, seg, ripples, skyTop, skyHorizon, bank, bankHeight, deep, shallow, amp, glint, clarity}).
- **أرقام / params:** 30×30 m, 256 seg, 24 ripple rings, sky top #6f9cc8, horizon #f2d6b0, bank #26301c h .12, deep #0d3b3a, shallow #2f6f62, amp .012, clarity .62
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:506` · `kosif-studio/tests/test_studio.py:637`

#### PART-101 · تمايل الرياح · Wind sway shader · 📦 بأمر تثبيت
- **ماذا / what:** Vertex bend ∝ height² with per-instance phase for reeds, grass, leaves.
- **كيف / how:** K3.addSway(material, {amp, freq, time}).
- **أرقام / params:** amp .06, freq 1.3 Hz
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:591`

#### PART-102 · بتلات متساقطة · Falling petals that ring the water · 📦 بأمر تثبيت
- **ماذا / what:** Sakura petals fall with seeded flutter, land, ring the water and drift.
- **كيف / how:** K3.makePetals({n, region, times:[ta,tb], level, size, seed}).
- **أرقام / params:** n 120, region [-4,4,-3,3], times [0,8], size 1.4
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:685`

#### PART-103 · خطوط المطر · Rain streaks with exposure smear · 📦 بأمر تثبيت
- **ماذا / what:** Slanted stroke lines in two depth layers (thin far, thick near), a warm layer lit by fire, then directional motion blur.
- **كيف / how:** rain(seed, n, x0, x1, y0, y1, length, width, slant=-0.25) -> stroke(); fill colours #a8bbd4/.15, #cddcef/.2, fire-lit #ffb066 add.
- **أرقام / params:** 520 + 150 + 160 streaks; lengths 24/60/36; duck uses 950 far drops
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/scenes/whale_dragon.py:55` · `kosif-studio/scenes/whale_dragon.py:269` · `kosif-studio/scenes/duck_dragon.py:24`

#### PART-104 · الرذاذ والزبد وانهمار الماء · Spray, foam and water sheeting · 📦 بأمر تثبيت
- **ماذا / what:** Breaching-water effects: Gaussian spray dots in white and warm add, foam lines along wave crests, water sheets as screen strokes running off a body, then motion blur.
- **كيف / how:** spray(seed, cx, cy, n, sx, sy, up, sizes) and foam(seed, y, amp, n) helpers + dots/stroke fills + motion_blur.
- **أرقام / params:** spray 460 dots sigma 160x70; foam 5 crest rows at y 496-712
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/scenes/whale_dragon.py:65` · `kosif-studio/scenes/whale_dragon.py:70` · `kosif-studio/scenes/whale_dragon.py:233`

#### PART-105 · التقاط الحركة إلى جسيمات · Mocap: performer silhouette → particles · 📦 بأمر تثبيت
- **ماذا / what:** From a fixed-camera video, subtracts a median background, cleans the silhouette and samples a stable set of particle positions per frame for a three-kit particle body.
- **كيف / how:** python motion.py mocap VIDEO --out body.json [--fps 30 --points 1200 --from 0 --dur D]
- **أرقام / params:** 480 px; threshold 28; Gaussian 5×5; open/close ellipse 5×5 (close ×2); components ≥1 % of largest; 30× seeded candidates (seed 7); coords 0-1000, −1 unused
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/qa.py:598`

#### PART-106 · غبار متطاير فوق الفيديو · Seeded dust particles over footage · 📦 بأمر تثبيت
- **ماذا / what:** Seeded dust specks drifting upward through warm passages of a talking-head edit.
- **كيف / how:** DOM particles created from M.rng and animated on the timeline
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/premium_edit/index.html:157`

#### PART-107 · جسيمات · Category: Particles · 📦 بأمر تثبيت
- **ماذا / what:** Capability family 'particles' (20 catalog entries) with a dedicated bilingual playbook of timings and recipes.
- **كيف / how:** Read playbooks/particles.md (visual grammar, motion mechanics, scene recipes, QA); build in starters/html-canvas or starters/remotion; filter catalog with python3 tools/kosif.py list --category particles.
- **أرقام / params:** sizes 4/8/14px; 150-600 Canvas, 20000 WebGL; burst 400-1300px/s gravity 60-150px/s2; flow-field noise scale 0.0025
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/particles.md` · `kosif-tool/catalog/categories.json` · `kosif-tool/catalog/meta.json`

#### PART-108 · جسيمات منحنية في هوديني · Houdini VEX curl-flow particles · 🔑 مفتاح/خدمة
- **ماذا / what:** Advect points by noise velocity, orient to velocity, shrink near end of life.
- **كيف / how:** VEX wrangle: @v=lerp(@v,noise*speed,blend); @orient=quaternion(maketransform(normalize(@v),up)); @pscale=base*(1-smooth(0.7,1,@age/@life)). Run via hython.
- **أرقام / params:** shrink from 70% of life
- **الدليل / proof:** `kosif-atlas/skills/228-mas-3d-games/708-houdini/SKILL.md`

#### PART-109 · محاكاة هوديني · Houdini FLIP/Pyro/Vellum/RBD + Karma · 🔑 مفتاح/خدمة
- **ماذا / what:** Pro fluid, smoke, cloth and rigid-body solvers; USD/MaterialX rendering with Karma XPU and cryptomatte AOVs.
- **كيف / how:** Commercial license; hython headless baking. Not available here.
- **الدليل / proof:** `kosif-atlas/skills/228-mas-3d-games/708-houdini/SKILL.md`

#### PART-110 · حلقة جزيئات · Particle torus · 👁 شوهد في فيديو
- **ماذا / what:** points on torus projected with perspective, rotate, size by depth
- **الدليل / proof:** `style:pm-codestackr-c071bf` · `style:pm-roundtablespace-d3a1be`

#### PART-111 · كرة جسيمات · Particle sphere · 👁 شوهد في فيديو
- **ماذا / what:** Fibonacci-sphere points projected and rotated, coloured dots
- **أرقام / params:** ~600 points
- **الدليل / proof:** `style:pm-crazyalphaaa-bc7e75` · `style:pm-zaqailo-212ad3`

#### PART-112 · تراب طباشير يتساقط · Falling chalk dust particles · 👁 شوهد في فيديو
- **ماذا / what:** for the last ~14 frames the chalk was drawing, spawn a dot at that tip; it falls with gravity and fades over 0.5 s; deterministic random(seed)
- **أرقام / params:** r 0.8-1.5 px, g ~400 px/s^2
- **الدليل / proof:** `style:chalkboard`

#### PART-113 · مطر من الغيمة مع حلقات ارتطام · Rain with splash rings · 👁 شوهد في فيديو
- **ماذا / what:** short blue dashes fall from the cloud footprint with random x and speed; on ground y spawn small ellipse rings that expand and fade
- **أرقام / params:** 40-60 streaks, fall 600-900 ms, ring 300 ms
- **الدليل / proof:** `style:doodle`

#### PART-114 · انفجار قصاصات عند الوصول · Confetti burst on arrival · 👁 شوهد في فيديو
- **ماذا / what:** 20-40 small rotated rectangles in stage colours with random velocity, gravity and spin, fading after ~1 s
- **أرقام / params:** g ~900 px/s^2
- **الدليل / proof:** `style:isometric`

#### PART-115 · أوتار تهتز عند الاصطدام · Vibrating strings impact · 👁 شوهد في فيديو
- **ماذا / what:** 5 horizontal quadratic curves; on impact set control-point offset to amplitude A and decay with damped sine A·e^(-6t)·sin(30t)
- **أرقام / params:** A ≈ 4% h, 400 ms
- **الدليل / proof:** `style:pm-1littlecoder-9fef89`

#### PART-116 · دوامة جسيمات · Particle vortex · 👁 شوهد في فيديو
- **ماذا / what:** 3k points on spiral, angle+=k/r
- **الدليل / proof:** `style:pm-3xtihor-0f6911`

#### PART-117 · أشعة تحت الماء وتمايل · Underwater rays and bobbing · 👁 شوهد في فيديو
- **ماذا / what:** Vertical blue gradient with semi-transparent diagonal light shafts; jellyfish bob with sine y and tentacle sway, bubbles rise and wobble, fish cross horizontally
- **أرقام / params:** bob amplitude 10 px at 0.4 Hz, bubbles 20-40 px/s
- **الدليل / proof:** `style:pm-abderrahmen-g-9e8ed0`

#### PART-118 · تفكك النص إلى شرارات جمرية · Text disintegrates into embers · 👁 شوهد في فيديو
- **ماذا / what:** sample text pixels into points; each point gets delayed release (left→right noise threshold), curl-noise velocity, colour from white to orange, additive blending
- **أرقام / params:** 20-60k points; release sweep 1.2 s; life 2 s
- **الدليل / proof:** `style:pm-ajith-io-4c248f`

#### PART-119 · موجة شبكة نقاط · Dot grid wave · 👁 شوهد في فيديو
- **ماذا / what:** grid of dots, colour flips along sine wave front
- **أرقام / params:** spacing 40px
- **الدليل / proof:** `style:pm-ajith-io-b5626e`

#### PART-120 · سرب حروف · Letter flock · 👁 شوهد في فيديو
- **ماذا / what:** boids with glyph sprites over gradient sky
- **الدليل / proof:** `style:pm-ajith-io-ea7f2d`

#### PART-121 · انفجار قصاصات احتفالي · Confetti celebration burst · 👁 شوهد في فيديو
- **ماذا / what:** 300 thin planes with random colour from palette, initial upward velocity, gravity 9.8, drag 0.98, random angular velocity
- **أرقام / params:** lifetime 2.5 s
- **الدليل / proof:** `style:pm-anilraok-eff262`

#### PART-122 · خطوط فضاء · Hyperspace streaks · 👁 شوهد في فيديو
- **ماذا / what:** radial lines length∝speed
- **الدليل / proof:** `style:pm-apoorvjain25-d24184`

#### PART-123 · حياة محيطة: نوارس وفوانيس · Ambient life: gulls and lamps · 👁 شوهد في فيديو
- **ماذا / what:** few bird sprites/meshes with flap cycle on slow paths; emissive lantern heads on posts
- **أرقام / params:** 3-5 gulls, flap 3 Hz
- **الدليل / proof:** `style:pm-axtonliu-0b861d`

#### PART-124 · كرة جسيمات فيبوناتشي · Fibonacci particle sphere · 👁 شوهد في فيديو
- **ماذا / what:** Place N points with golden-angle spiral on unit sphere, rotate in y, project with perspective, sort by depth, size/alpha by z, a few red accent points, plus elliptical orbit line
- **أرقام / params:** N=1200, FOV 42°, rot 167°/s guess
- **الدليل / proof:** `style:pm-ayushunleashed-ece3e3`

#### PART-125 · مربعات شفافة عائمة كقصاصات · Confetti rounded squares · 👁 شوهد في فيديو
- **ماذا / what:** Spawn 20-30 translucent rounded squares of brand colours drifting upward with slow rotation and parallax depth by size
- **أرقام / params:** opacity 0.4-0.7, speed 20-60 px/s, rotation 10-30°/s
- **الدليل / proof:** `style:pm-bizibeast-10f264`

#### PART-126 · خطوط تتجمع · Line particles regroup · 👁 شوهد في فيديو
- **ماذا / what:** line segments explode then attract to rectangle targets
- **أرقام / params:** 1s
- **الدليل / proof:** `style:pm-blue-clarity-ef56d0`

#### PART-127 · تحول الجسيمات إلى شبكة ثم واجهة · Particles-to-grid-to-UI resolve · 👁 شوهد في فيديو
- **ماذا / what:** Each sphere tweens to a snapped grid cell (stagger by distance), grid dots then fade while UI layers fade up in their place
- **أرقام / params:** grid pitch ~24 px, tween 600 ms easeInOutCubic, stagger 0-300 ms
- **الدليل / proof:** `style:pm-bogdandragomir-35e024`

#### PART-128 · أيقونة تتكوّن من سحابة نقاط · Icon coalescing from point cloud · 👁 شوهد في فيديو
- **ماذا / what:** Sample points along icon SVG path, start them scattered in a teardrop cloud and spring to target positions
- **أرقام / params:** 300-600 points, spring stiffness 120, damping 18, ~600 ms
- **الدليل / proof:** `style:pm-bogdandragomir-35e024`

#### PART-129 · انفجار فتح إنجاز · Achievement unlock burst · 👁 شوهد في فيديو
- **ماذا / what:** spawn 80 gold star particles radial, gravity 0.05, fade 2 s
- **أرقام / params:** colors #e3b75a/#fff
- **الدليل / proof:** `style:pm-bthreeagency-b9b8d9`

#### PART-130 · جسيمات غبار للعمق · Dust particle depth field · 👁 شوهد في فيديو
- **ماذا / what:** 40-80 small soft dots of varied blur and opacity drifting slowly upward over a radial navy gradient to add depth behind flat UI
- **أرقام / params:** size 2-6 px, speed 5-15 px/s
- **الدليل / proof:** `style:pm-ceowinkz-7c776b`

#### PART-131 · شبكة نقاط تتأثر بجسم متحرك · Dot-grid field displacement · 👁 شوهد في فيديو
- **ماذا / what:** grid of dots; each dot offset away from a moving attractor and tinted red/blue by distance; chain of balls follows leader with lag (follow-through)
- **أرقام / params:** grid 28 px, radius 160 px, chain 15 balls lag 2 frames
- **الدليل / proof:** `style:pm-chatgptastra-0d95c7`

#### PART-132 · باعث لهب · Canvas fire emitter · 👁 شوهد في فيديو
- **ماذا / what:** spawn 30-60 particles/frame rising with noise, colour ramp white→yellow→red→transparent, lighter blend
- **الدليل / proof:** `style:pm-chrisjdimarco-f068db`

#### PART-133 · بلوب سائل · Metaball blob · 👁 شوهد في فيديو
- **ماذا / what:** SVG gooey filter or metaballs with inner lighter circles, offset blue shadow
- **أرقام / params:** blur 12 + threshold
- **الدليل / proof:** `style:pm-crazyalphaaa-bc7e75`

#### PART-134 · فاصل كوكبة النجوم · Constellation interlude · 👁 شوهد في فيديو
- **ماذا / what:** random star points, lines connect nearby, purple radial haze
- **الدليل / proof:** `style:pm-dale-vaz-cc612a`

#### PART-135 · مطر قصاصات الورق · Confetti rain · 👁 شوهد في فيديو
- **ماذا / what:** Small rectangles in brand + festive colours spawned above, fall with gravity, sway (sin) and 3D flip (scaleY cos)
- **أرقام / params:** 150 pcs, fall 150-300 px/s, sway 20 px
- **الدليل / proof:** `style:pm-deebeeeff-50fcd0`

#### PART-136 · ماء متموج عاكس بتظليل إجرائي · Procedural reflective water · 👁 شوهد في فيديو
- **ماذا / what:** Fragment shader: mirror the sky above horizon, distort with scrolling layered sine/noise normals, add specular streaks under bright sources
- **أرقام / params:** 2-3 noise octaves, scroll 0.02-0.05 uv/s, reflection darken 20%
- **الدليل / proof:** `style:pm-demitiyageekzen-7770ad`

#### PART-137 · فوانيس عائمة مضيئة على الماء · Floating lantern particles · 👁 شوهد في فيديو
- **ماذا / what:** Small emissive lotus sprites placed in perspective on the water plane, drifting slowly with flicker and a short vertical reflection streak each
- **أرقام / params:** 8-15 lanterns, flicker 0.85-1.0 at 3-6 Hz, drift 5-10 px/s
- **الدليل / proof:** `style:pm-demitiyageekzen-7770ad`

#### PART-138 · انفجار قصاصات · Confetti burst · 👁 شوهد في فيديو
- **ماذا / what:** 40 particles gravity + spin from button
- **الدليل / proof:** `style:pm-devius-maximus-beab45`

#### PART-139 · طبقات أمواج متوازية · Parallax wave layers · 👁 شوهد في فيديو
- **ماذا / what:** 3-5 sine wave bands with offset phase & speeds
- **أرقام / params:** amp 10-30px
- **الدليل / proof:** `style:pm-faroukzy-9ff23e`

#### PART-140 · نظام مطر · Rain streak system · 👁 شوهد في فيديو
- **ماذا / what:** slanted short lines falling fast with alpha
- **أرقام / params:** ~400 drops
- **الدليل / proof:** `style:pm-faroukzy-9ff23e`

#### PART-141 · شبكة نقاط تتحرك فيها موجة · Travelling wave dot grid · 👁 شوهد في فيديو
- **ماذا / what:** grid of small grey dots; cells near a moving sine band scale up into pink squares, falloff by distance
- **أرقام / params:** grid 24 px, band width 120 px, speed 400 px/s
- **الدليل / proof:** `style:pm-ghinaiya-nirmal-5d8fec`

#### PART-142 · بقع سائلة متداخلة · Metaball fluid blobs · 👁 شوهد في فيديو
- **ماذا / what:** several circles blurred + threshold (gooey filter) moving on noise paths, merging; overlaid italic word
- **أرقام / params:** SVG feGaussianBlur 12 + feColorMatrix alpha 20 -8
- **الدليل / proof:** `style:pm-ghinaiya-nirmal-5d8fec`

#### PART-143 · شظايا كريستال طافية · Floating crystal shards · 👁 شوهد في فيديو
- **ماذا / what:** Instanced flat star/shard meshes in neon emissive colours drifting and spinning in the foreground for depth
- **أرقام / params:** count ~40, rot 0.5 rad/s, depth-of-field feel by size
- **الدليل / proof:** `style:pm-gorden-sun-041f56`

#### PART-144 · جسيمات تكوّن كلمة · Particles assemble a word · 👁 شوهد في فيديو
- **ماذا / what:** Sample points from rasterised text; start particles from a dot-matrix shape, drift them with curl noise, then spring them to their target text points; mix red and white particles
- **أرقام / params:** ~4800 particles, spring k ~0.08, damping 0.85
- **الدليل / proof:** `style:pm-grace-sunnyy-29bc61`

#### PART-145 · نقاط مسار الارتداد · Bounce trajectory dots · 👁 شوهد في فيديو
- **ماذا / what:** simulate y'' = -g with restitution e on contact; stamp a red dot every N frames to leave a dotted parabola trail; annotate 'e = 0.75'
- **أرقام / params:** e 0.75, dot 4 px #c9452c, every 2 frames
- **الدليل / proof:** `style:pm-hbcoop-de365c`

#### PART-146 · سرب جسيمات منقّطة · Boids stipple flock · 👁 شوهد في فيديو
- **ماذا / what:** 8,192 points with separation/alignment/cohesion (GPU or instanced), drawn as 1-2 px dark dots, projected soft shadow below
- **أرقام / params:** n 8192, point 1.5 px
- **الدليل / proof:** `style:pm-hbcoop-de365c`

#### PART-147 · حقل نقاط يتشوه بالحركة · Dot-matrix displacement field · 👁 شوهد في فيديو
- **ماذا / what:** grid of dots; each dot offset by falloff from a moving attractor; trail of large blue dots with lagging follow-through and red secondary particles
- **أرقام / params:** grid 24px, falloff radius 200px
- **الدليل / proof:** `style:pm-himanshutwtxs-5f4b43`

#### PART-148 · وميض نجوم · Star twinkle · 👁 شوهد في فيديو
- **ماذا / what:** Random phase sine on alpha, cross sparkles
- **أرقام / params:** 60 stars
- **الدليل / proof:** `style:pm-hoyoyoda-3a5c08`

#### PART-149 · جسيمات بكسل تتجمع نصاً · Pixel particles assemble text · 👁 شوهد في فيديو
- **ماذا / what:** Sample text pixels on an offscreen canvas, spawn square particles at random positions, tween each to its target with easeOutExpo and random delay 0-600 ms
- **أرقام / params:** particle 6px; 1.2-1.5s
- **الدليل / proof:** `style:pm-ibrahimwasim240-809370`

#### PART-150 · شفط دوامي للعناصر · Vortex suck-in · 👁 شوهد في فيديو
- **ماذا / what:** Cards spiral toward the hero object while scaling down; radial scribble lines around the object convey force
- **أرقام / params:** 300-500 ms easeInCubic, rotation 90-180 deg
- **الدليل / proof:** `style:pm-ik-builds-b8bdcf`

#### PART-151 · سرب جسيمات متدفق · Flow-field streak swarm · 👁 شوهد في فيديو
- **ماذا / what:** ~10k particles, curl noise velocity, draw short lines with alpha trail 0.1
- **أرقام / params:** additive blend
- **الدليل / proof:** `style:pm-ismailfahmi-557268`

#### PART-152 · تحول الجسيمات إلى شكل · Particle target morph · 👁 شوهد في فيديو
- **ماذا / what:** lerp each particle to target point sets (clusters, histogram bins) over 1.2s easeInOut
- **الدليل / proof:** `style:pm-ismailfahmi-557268`

#### PART-153 · جزيئات موسمية: بتلات وأوراق وثلج · Seasonal particles · 👁 شوهد في فيديو
- **ماذا / what:** Emitters drifting diagonally with the wind direction of travel: blossoms (pink ellipses, spin), leaves (orange quads, tumbling), snow (white dots, slow fall, sine sway)
- **أرقام / params:** 60-150 particles, vx -100..-300 px/s, sway amp 10 px
- **الدليل / proof:** `style:pm-itsolelehmann-e47532`

#### PART-154 · بخار قهوة يتصاعد · Coffee steam curls · 👁 شوهد في فيديو
- **ماذا / what:** 3 thin translucent white bezier strokes rising from the cup, each offset by noise over time and fading out at the top
- **أرقام / params:** rise 40 px/s, opacity 0.4->0, loop 3 s
- **الدليل / proof:** `style:pm-itsolelehmann-e47532`

#### PART-155 · عادم جسيمات مكعبة · Cube particle exhaust · 👁 شوهد في فيديو
- **ماذا / what:** spawn small emissive cubes behind engine, random velocity, scale/alpha fade
- **أرقام / params:** life ~1s, 40/s
- **الدليل / proof:** `style:pm-ivanfioravanti-bd9261`

#### PART-156 · جزيئات تتجمع لتكوين كلمة · Particles to text · 👁 شوهد في فيديو
- **ماذا / what:** Sample points from text rendered to offscreen canvas; spawn particles at a burst origin and lerp each to its target with ease-out plus noise; colour by gradient
- **أرقام / params:** 2-4k particles, 800 ms travel, size 2 px
- **الدليل / proof:** `style:pm-jasonzhou1993-8595e0`

#### PART-157 · شرائط خطوط موجية · Line-ribbon waves · 👁 شوهد في فيديو
- **ماذا / what:** Draw 100-200 thin sine curves whose phase/amplitude are offset per line and driven by noise over time, stroked with an orange->magenta->blue gradient at low alpha
- **أرقام / params:** lineWidth 0.6, alpha 0.3, 3-4 bands
- **الدليل / proof:** `style:pm-jasonzhou1993-8595e0`

#### PART-158 · شعار بكسلي من جسيمات · Particle-to-pixel logo · 👁 شوهد في فيديو
- **ماذا / what:** random particles ease to grid cells of logo bitmap
- **أرقام / params:** ~600 px cells, 1.5 s
- **الدليل / proof:** `style:pm-jayscambler-3f8889`

#### PART-159 · مطر وضباب جوي · Rain and fog atmosphere · 👁 شوهد في فيديو
- **ماذا / what:** 300-500 thin streaks falling at ~10-15° with slight speed variance; 2-3 blurred horizontal fog bands drifting slowly at different speeds
- **أرقام / params:** streak alpha 0.25-0.4, length 12-24px
- **الدليل / proof:** `style:pm-kamstudiolabs-0b0824`

#### PART-160 · شرارات الاصطدام · Impact spark lines · 👁 شوهد في فيديو
- **ماذا / what:** Emit 4-6 short radial line particles at impact point that fly out and fade
- **أرقام / params:** life 200 ms, speed 200 px/s
- **الدليل / proof:** `style:pm-kamstudiolabs-447565`

#### PART-161 · ارتداد كرة داخل حلقة دائرية · Ball-in-ring circular reflection physics · 👁 شوهد في فيديو
- **ماذا / what:** fixed timestep; when |p-c| >= R - r, reflect velocity about normal n=(p-c)/|p-c|: v = v - 2(v·n)n; keep speed constant (restitution 1); check gap: if atan2 angle within rotating gap window, let ball p
- **كيف / how:** fixed timestep; when |p-c| >= R - r, reflect velocity about normal n=(p-c)/|p-c|: v = v - 2(v·n)n; keep speed constant (restitution 1); check gap: if atan2 angle within rotating gap window, let ball pass and remove ring
- **أرقام / params:** substeps 4/frame, speed ~600 px/s @720w, gap ~30-40 deg
- **الدليل / proof:** `style:pm-kantamk-61f410`

#### PART-162 · ذيل حركة مدبّب · Tapered motion trail · 👁 شوهد في فيديو
- **ماذا / what:** store last bounce point and recent positions; draw line segments with width and alpha decreasing toward the tail
- **أرقام / params:** trail ~0.3 s, width 6->0px
- **الدليل / proof:** `style:pm-kantamk-61f410`

#### PART-163 · تفتت الحلقة إلى نقاط · Ring-burst particle dissolve · 👁 شوهد في فيديو
- **ماذا / what:** on escape, sample ~60 points along the ring, give radial outward velocity 40-120 px/s with slight random tangent, glowing dots fade over ~2 s
- **أرقام / params:** dot radius 1.5-3px, seeded RNG
- **الدليل / proof:** `style:pm-kantamk-61f410`

#### PART-164 · كرة نقاط تتجمع ثم تنهار · Point-cloud sphere gather/collapse · 👁 شوهد في فيديو
- **ماذا / what:** ~400 points on a Fibonacci sphere, project with slow Y rotation; scale radius 0->R (ease-out 1.5 s) to form, R->0 (ease-in 0.6 s) to collapse into origin dot
- **أرقام / params:** point alpha 0.25, size 1-1.5px, R ~25% height
- **الدليل / proof:** `style:pm-kloss-xyz-b9b3f6`

#### PART-165 · كلمة من الضوضاء · Noise-to-word denoise · 👁 شوهد في فيديو
- **ماذا / what:** particles lerp from random to text-sampled positions over steps
- **الدليل / proof:** `style:pm-kloss-xyz-fe0c31`

#### PART-166 · مجرة جزيئات · Particle galaxy outro · 👁 شوهد في فيديو
- **ماذا / what:** log spiral points rotating with depth fade
- **الدليل / proof:** `style:pm-kloss-xyz-fe0c31`

#### PART-167 · شيدر لهب العادم · Exhaust plume shader · 👁 شوهد في فيديو
- **ماذا / what:** additive cone with noise and shock-diamond bright bands
- **أرقام / params:** violet->white core
- **الدليل / proof:** `style:pm-konstantinsaifo-96fc89`

#### PART-168 · قطرات لزجة تتصل وتنفصل · Metaball gooey flow · 👁 شوهد في فيديو
- **ماذا / what:** Circles moving along paths with SVG filter feGaussianBlur(stdDev 10) + feColorMatrix alpha 20 -8 so they merge like liquid; add small white specular dot
- **أرقام / params:** blur 10; alpha matrix 0 0 0 20 -8
- **الدليل / proof:** `style:pm-leadnotifi-e83f94`

#### PART-169 · شبكة نقاط تموج بموجة · Rippling dot-matrix field · 👁 شوهد في فيديو
- **ماذا / what:** Grid of small squares; scale and colour each by a travelling sine/radial wave so a lime band sweeps across
- **أرقام / params:** grid 24px; wave speed 400px/s
- **الدليل / proof:** `style:pm-leadnotifi-e83f94`

#### PART-170 · نفق جسيمات بخطوط سرعة · Particle streak tunnel · 👁 شوهد في فيديو
- **ماذا / what:** Thousands of particles on a cylinder moving toward camera rendered as short lines (velocity streaks), dark hole in centre
- **أرقام / params:** 3000 pts, warm multicolour, additive blend, 1 s
- **الدليل / proof:** `style:pm-leonkohli-6dc01b`

#### PART-171 · تكدس ملصقات أسفل الشاشة · Poster pile spill · 👁 شوهد في فيديو
- **ماذا / what:** Dozens of image cards drop from above with random rotation and pile along the bottom edge (pre-baked rigid body or eased random rest positions)
- **أرقام / params:** 40-60 cards, rot ±30°, stagger 30 ms
- **الدليل / proof:** `style:pm-lester-tyy-f897f7`

#### PART-172 · تكدس رقائق بفيزياء · Physics chip pile · 👁 شوهد في فيديو
- **ماذا / what:** chips drop with gravity and settle with bounce
- **الدليل / proof:** `style:pm-lexnlin-6161a6`

#### PART-173 · سائل ملون · Fluid sim backdrop · 👁 شوهد في فيديو
- **ماذا / what:** GPU stable fluids with dye injection; outlined text overlay
- **الدليل / proof:** `style:pm-lukasersil-0ed38e`

#### PART-174 · انفجار جزيئات · Particle burst tunnel · 👁 شوهد في فيديو
- **ماذا / what:** thousands of points radially accelerating with motion streaks
- **أرقام / params:** 1s
- **الدليل / proof:** `style:pm-lukasersil-0ed38e`

#### PART-175 · نص من جسيمات · Particle-filled text · 👁 شوهد في فيديو
- **ماذا / what:** sample text pixels, place many dots, jitter
- **الدليل / proof:** `style:pm-m1n9-k7-ff9ab9`

#### PART-176 · حقل موجة جسيمات · 3D particle wave field · 👁 شوهد في فيديو
- **ماذا / what:** grid of points with sin displacement, perspective
- **الدليل / proof:** `style:pm-m1n9-k7-ff9ab9`

#### PART-177 · انفجار جزيئات المنتج · Product particle explosion · 👁 شوهد في فيديو
- **ماذا / what:** 3D-ish pills scattered with blur by depth, outward drift
- **الدليل / proof:** `style:pm-macrohou-33959d`

#### PART-178 · لولب يتحول إلى خيوط · Helix to strands · 👁 شوهد في فيديو
- **ماذا / what:** sinusoidal double helix whose points become bezier strands to target bar
- **أرقام / params:** 1.5 s
- **الدليل / proof:** `style:pm-madebyjmayala-b9204d`

#### PART-179 · أيقونة مبنية من جسيمات · Particle-built icon · 👁 شوهد في فيديو
- **ماذا / what:** Sample points from an SVG icon (padlock/logo) and spring scattered particles into it, additive blending + bloom, glowing focal point (keyhole)
- **أرقام / params:** 3000-6000 points, size 1-2 px, bloom strength 1.5, spring 600 ms
- **الدليل / proof:** `style:pm-madhav-xo-f97f20`

#### PART-180 · نمو عباد الشمس · Phyllotaxis growth · 👁 شوهد في فيديو
- **ماذا / what:** n*137.508deg, r=c*sqrt(n), grow n over time
- **الدليل / proof:** `style:pm-math-files-39c9d0`

#### PART-181 · حقل نجوم بقفزة فضائية · Hyperspace starfield warp · 👁 شوهد في فيديو
- **ماذا / what:** N≈600 points with z depth; project x/z, y/z; draw line from previous to current projected position; speed ramps up on drops
- **أرقام / params:** speed 2→30 units/frame, stroke 1 px #9db4ff alpha 0.6
- **الدليل / proof:** `style:pm-maxalexweber-67688b`

#### PART-182 · كرة جسيمات بحلقات مدارية · Particle sphere with orbit rings · 👁 شوهد في فيديو
- **ماذا / what:** Fibonacci-sphere points projected in 3D, gradient colour by height, two tilted thin ellipses; burst into velocity streaks
- **أرقام / params:** 2000 points, rotation 0.4 rad/s, streak length 10-30 px
- **الدليل / proof:** `style:pm-motiondsgnr-9dcfa6`

#### PART-183 · سائل ميتابول خلف النص · Metaball liquid behind text · 👁 شوهد في فيديو
- **ماذا / what:** Blurred blob field with threshold (or SVG goo filter), dark inner holes, moves behind bold headline; text keeps a gradient fill
- **أرقام / params:** gaussian blur 20 px + alpha threshold, 4-6 blobs
- **الدليل / proof:** `style:pm-motiondsgnr-9dcfa6`

#### PART-184 · جزيئات تتجمع في كلمة · Particle text assembly · 👁 شوهد في فيديو
- **ماذا / what:** sample text pixels as targets; particles advect by curl noise then lerp to targets
- **أرقام / params:** 6000 particles, 1.5 s
- **الدليل / proof:** `style:pm-ndhabarde11-f155b4`

#### PART-185 · خطوط رصاص متوهجة · Tracer streaks · 👁 شوهد في فيديو
- **ماذا / what:** Short additive-blended line segments fired in bursts of 6-10 along a direction, moving very fast and fading; warm white core
- **أرقام / params:** speed ~3000 u/s, life 0.3 s, colour #fff2d0
- **الدليل / proof:** `style:pm-nft-chen-5f8bb0`

#### PART-186 · ذيول بخار من أطراف الأجنحة · Wingtip contrail ribbons · 👁 شوهد في فيديو
- **ماذا / what:** Record last N wingtip positions each frame and draw a flat ribbon mesh with alpha fading toward the tail
- **أرقام / params:** N = 60, width 0.3 u, alpha 0.8->0
- **الدليل / proof:** `style:pm-nft-chen-5f8bb0`

#### PART-187 · نجوم ممتدة كالانتقال الفضائي · Warp star streaks · 👁 شوهد في فيديو
- **ماذا / what:** Stars stretched into lines along radial vectors to imply camera travel between scenes
- **أرقام / params:** streak length 50-200px; 0.8s
- **الدليل / proof:** `style:pm-nolkeeg-bf062e`

#### PART-188 · انفجار بكسلي · Pixel explosion · 👁 شوهد في فيديو
- **ماذا / what:** circles orange/grey expand+fade 600 ms
- **الدليل / proof:** `style:pm-pluginplay-3d4006`

#### PART-189 · تجمع جسيمات إلى نص · Particle-to-text assembly · 👁 شوهد في فيديو
- **ماذا / what:** sample text pixels to ~3k points, lerp from random with ease-out 800ms
- **الدليل / proof:** `style:pm-raphaelaubryy-4b137e`

#### PART-190 · كشف بحقل خطوط متدفق · Flow-field line reveal · 👁 شوهد في فيديو
- **ماذا / what:** grid of short strokes oriented by noise; text mask colors lines
- **أرقام / params:** noise scale 0.003
- **الدليل / proof:** `style:pm-rendesr-86be44`

#### PART-191 · حزمة موجات ضوضائية متعددة · Multi-trace noisy waveform band · 👁 شوهد في فيديو
- **ماذا / what:** N=15 polylines across width; y = base + sum of 3 sines with per-trace phase + simplex noise(t*2, x*0.01)*amp; alpha 0.25 each, additive
- **أرقام / params:** amp 20-60px, 200 points per trace, update every frame
- **الدليل / proof:** `style:pm-rneayan-ea6129`

#### PART-192 · انفجار جزيئات بشكل الشعار ثم تجمعها · Iconic particle burst to logo · 👁 شوهد في فيديو
- **ماذا / what:** spawn 80-150 tiny X glyph particles with random velocity, mix of white and red, then lerp to centre target with ease-in; crossfade into large X
- **أرقام / params:** scatter 0.6 s, converge 0.8 s, motion blur
- **الدليل / proof:** `style:pm-robj3d3-b18fad`

#### PART-193 · تفكك النص لجسيمات · Text→particle burst · 👁 شوهد في فيديو
- **ماذا / what:** Sample text pixels into particles, apply outward velocity + noise drift
- **أرقام / params:** ~800 ms
- **الدليل / proof:** `style:pm-robvjourney-ce3e1a`

#### PART-194 · سكب وارتفاع السائل · Liquid fill with pour stream · 👁 شوهد في فيديو
- **ماذا / what:** bezier stream from bottle neck; clip-rect rising per oz; colour blend
- **أرقام / params:** ~2.5 s per pour
- **الدليل / proof:** `style:pm-ror-fly-9950f1`

#### PART-195 · انفجار سحابة صور · Image burst cloud · 👁 شوهد في فيديو
- **ماذا / what:** ~120 rounded image cards spawn at centre and fly radially outward with varied depth (scale 0.4-1.2), slight rotation and soft shadows, slowing to a drifting cloud around a caption pill
- **أرقام / params:** burst 700 ms expo-out, then drift 10 px/s
- **الدليل / proof:** `style:pm-rossaxbt-3085b7`

#### PART-196 · تجميع النص بالجسيمات · Particles assemble text · 👁 شوهد في فيديو
- **ماذا / what:** sample text pixels, lerp from random
- **الدليل / proof:** `style:pm-safarkhanshuvo-ffd52d`

#### PART-197 · كرات سائلة معدنية · Chrome metaball fluid · 👁 شوهد في فيديو
- **ماذا / what:** Raymarched SDF smooth-union of 3-5 spheres orbiting, env-map chrome material on flat accent bg
- **أرقام / params:** smooth k=0.4, orbit 0.5 Hz
- **الدليل / proof:** `style:pm-sahildesigner23-ee3155`

#### PART-198 · زجاجة تميل وتسكب · Tilt-and-pour bottle · 👁 شوهد في فيديو
- **ماذا / what:** bottle group translates in from top-right, rotates about its neck to ~-45°, a 4-6 px stream path grows from neck to surface then retracts before the bottle exits
- **أرقام / params:** enter 500 ms easeOutBack, hold during pour, exit 400 ms
- **الدليل / proof:** `style:pm-sarut0bisasuke-cefa43`

#### PART-199 · سُحب قشدة تنتشر · Diffusing cream clouds · 👁 شوهد في فيديو
- **ماذا / what:** spawn 6-10 light blobs at the pour point, blur 12-20 px, drift downward and sideways with noise, clip to the liquid shape, then fade into a pale top layer
- **أرقام / params:** duration ~3 s, opacity 0.8 -> 0.4
- **الدليل / proof:** `style:pm-sarut0bisasuke-cefa43`

#### PART-200 · جزيئات تدفق على مسار · Flow particles along path · 👁 شوهد في فيديو
- **ماذا / what:** instanced dashes moving along CatmullRom curve, speed 0.2 u/s, colour per flow type
- **الدليل / proof:** `style:pm-sayan-shanky-f850d8`

#### PART-201 · خطوط حرارة صاعدة · Heat streaks · 👁 شوهد في فيديو
- **ماذا / what:** red vertical line sprites rising and fading above object
- **الدليل / proof:** `style:pm-sayan-shanky-f850d8`

#### PART-202 · جسيمات تبني كلمة · Particles assemble word · 👁 شوهد في فيديو
- **ماذا / what:** Explode coloured particles from centre, then tween each to a sampled pixel of the target word; caption counts particles
- **أرقام / params:** 2000 particles; 1s
- **الدليل / proof:** `style:pm-shinskinakamoto-20190b`

#### PART-203 · مجرة جزيئات حلزونية · Particle spiral galaxy · 👁 شوهد في فيديو
- **ماذا / what:** thousands of points on logarithmic spiral arms coloured by arm, rotating with differential speed
- **أرقام / params:** ~5k pts, 2 arms red/white-blue
- **الدليل / proof:** `style:pm-shneural-2abdfa`

#### PART-204 · انفجار شرطات شعاعي · Radial dash burst · 👁 شوهد في فيديو
- **ماذا / what:** spawn 80-150 short line segments at the centre with random angles; move outward with decelerating speed, rotate along velocity, fade out; 3-colour mix
- **أرقام / params:** white 70 %, yellow 20 %, red 10 %; life 600-900 ms
- **الدليل / proof:** `style:pm-sudeepsd-1a3485`

#### PART-205 · مدار حلزوني لنقاط · Spiral orbit of N dots · 👁 شوهد في فيديو
- **ماذا / what:** dots on log-spiral arms rotating
- **الدليل / proof:** `style:pm-sudiyasa-f48ac9`

#### PART-206 · كرة لغات بفقاعات · Multilingual chips globe · 👁 شوهد في فيديو
- **ماذا / what:** Fibonacci dot sphere rotating slowly; chips pop at projected points
- **أرقام / params:** ~600 dots
- **الدليل / proof:** `style:pm-sudo-kiran-6609ed`

#### PART-207 · قصاصات احتفال على الختام · Confetti end card · 👁 شوهد في فيديو
- **ماذا / what:** 40 small rects with gravity + spin around logo + CTA button
- **الدليل / proof:** `style:pm-sudo-kiran-6609ed`

#### PART-208 · تحول سحابة جزيئات من حلقة إلى كرة · Particle torus-to-sphere morph · 👁 شوهد في فيديو
- **ماذا / what:** N points with two target positions (torus surface, sphere surface); lerp with easing and add short streak lines oriented along velocity; colour ramp orange→blue
- **أرقام / params:** N 5-10k, morph 1.5 s, slow y rotation
- **الدليل / proof:** `style:pm-tequilafunks-97f6c9`

#### PART-209 · تحطم إلى مربعات بانحراف لوني · Shatter to squares with RGB split · 👁 شوهد في فيديو
- **ماذا / what:** Replace mesh faces with square particles carrying their colours, fling them outward on a spiral with rotation, apply chromatic aberration (offset R/B channels 4-8 px) and motion blur
- **أرقام / params:** 300-600 particles, 600 ms
- **الدليل / proof:** `style:pm-teslachartz-c58b32`

#### PART-210 · كرات سائلة مع خطوط كنتور · Metaballs with iso-contours · 👁 شوهد في فيديو
- **ماذا / what:** Sum of 7 radial fields; fill threshold region lime, draw several iso-lines (marching squares) as thin black contours; balls drift and merge; heavy blue word on top
- **أرقام / params:** 7 balls, 4-6 contour levels
- **الدليل / proof:** `style:pm-teslachartz-c58b32`

#### PART-211 · شرر متصاعد · Rising ember particles · 👁 شوهد في فيديو
- **ماذا / what:** particle system of tiny emissive points, upward velocity 0.3-1 m/s, turbulence noise, random lifetime 2-4 s, motion blur streaks
- **أرقام / params:** 500-2000 particles
- **الدليل / proof:** `style:pm-theparuchh-6e08c3`

#### PART-212 · برطمان يمتلئ مع عدّاد · Jar fill with counter · 👁 شوهد في فيديو
- **ماذا / what:** Items drop from above lid with gravity + small bounce and random rotation ±15°, stacking in rows; a text counter increments per item
- **أرقام / params:** gravity ~2500 px/s2; restitution 0.3; 1 item / 120 ms
- **الدليل / proof:** `style:pm-thilina-a-891c09`

#### PART-213 · مجرة جسيمات حلزونية · Spiral galaxy particles · 👁 شوهد في فيديو
- **ماذا / what:** Particles on log-spiral arms, angular velocity ∝ 1/r, multicoloured streak trails
- **أرقام / params:** ~3000 pts
- **الدليل / proof:** `style:pm-tolgayhickiran-e90799`

#### PART-214 · جسيمات تتجمع لكلمة · Particles to wordmark · 👁 شوهد في فيديو
- **ماذا / what:** Sample text pixels as targets; vortex then lerp to targets
- **أرقام / params:** 3000 pts, 1.5 s
- **الدليل / proof:** `style:pm-topi-003-9ca6b5`

#### PART-215 · شبكة نقاط موجية · Wave dot grid · 👁 شوهد في فيديو
- **ماذا / what:** grid dots coloured where sin(x+t) > threshold
- **أرقام / params:** spacing 24px
- **الدليل / proof:** `style:pm-umangratani-57f86a`

#### PART-216 · سجادة شرطات تتبع حقل تدفق · Flow-field dash carpet · 👁 شوهد في فيديو
- **ماذا / what:** grid of short line segments coloured red/black/blue on yellow; each rotates to angle = noise(x,y,t)*2π
- **أرقام / params:** grid 40 px, segment 24x5 px, noise scale 0.004
- **الدليل / proof:** `style:pm-vanshwtfff-db0466`

#### PART-217 · بطاقة نهاية بنثار لامع · Confetti spark end card · 👁 شوهد في فيديو
- **ماذا / what:** burst of small multicolour dots/squares around logo with gravity and fade
- **أرقام / params:** 60-120 particles, life 1.5-2 s
- **الدليل / proof:** `style:pm-viktoroddy-98c1d8`

#### PART-218 · كرة ترتد بالجاذبية · Gravity bounce ball · 👁 شوهد في فيديو
- **ماذا / what:** parabolic y with damping
- **الدليل / proof:** `style:pm-web3wesley-7bb108`

#### PART-219 · جسيمات تشكل نصاً · Particle hair to text · 👁 شوهد في فيديو
- **ماذا / what:** short line particles swirl radially then align to text mask
- **الدليل / proof:** `style:pm-web3wesley-7bb108`

#### PART-220 · أيقونات تسقط في وعاء · Icons dropping into a container · 👁 شوهد في فيديو
- **ماذا / what:** Rounded icon tiles fall with gravity and rotate into an illustrated bowl, slight bounce, label inside bowl
- **أرقام / params:** fall 500 ms easeInQuad + bounce 15%, random rotation ±15°
- **الدليل / proof:** `style:pm-wozu-co-242285`

#### PART-221 · انفجار شظايا · Shard burst · 👁 شوهد في فيديو
- **ماذا / what:** triangles explode radially from glowing core with spin
- **أرقام / params:** 600 ms easeOutExpo
- **الدليل / proof:** `style:pm-zaqailo-212ad3`

#### PART-222 · بطاقات تسقط وتتكدس ثم ينهار البرج · Falling stack with bounce and collapse · 👁 شوهد في فيديو
- **ماذا / what:** each card a function of time with phases: drop with bounce (easeOutBounce), shared tower sway (sine growing amplitude), topple rotation about base, settle on pile
- **أرقام / params:** drop ~300 ms, stagger 400 ms, sway up to 6 deg
- **الدليل / proof:** `style:stickman`

#### PART-223 · S11 عضوي سائل · S11 Organic flowing · 📄 موصوف
- **ماذا / what:** Curves, soft gradients, leaves or ink; slow breathing, flowing, organic reveals. Calm and flexible for backgrounds; heavy warping damages logos and text and health claims must be substantiated.
- **كيف / how:** SVG blobs with animated path morph/feTurbulence, blurred gradient blobs on canvas; KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg)
- **أرقام / params:** cost medium; MG-005 MG-015 MG-030 MG-081 MG-111 MG-113 MG-114 MG-118
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### PART-224 · MG-111/113/114 خلفيات هادئة متكررة · MG-111/113/114 Ambient background loops · 📄 موصوف
- **ماذا / what:** Two blurred colour blobs drift apart and back (MG-111); three wavy lines shift periodically behind a podcast title (MG-113); a few light specks drift with varied depth (MG-114).
- **كيف / how:** MG-111: 0-4 apart, 4-8 back; test gradients for banding after compression. MG-113: one full 8 s wave cycle, low contrast under long text. MG-114: 10 s drift with staggered fade at edges - every speck's cycle must divide the loop length for a true seamless loop. Canvas with t mod period; tiny dither noise against banding.
- **أرقام / params:** 8 s / 8 s / 10 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-loops-backgrounds.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### PART-225 · المؤثر البصري على لحظة التلامس · Visual impact synced to contact frame · 📄 موصوف
- **ماذا / what:** Particle bursts and hit SFX land on the actual contact/apex frame, not clip start; honour reduced-motion and flashing limits.
- **كيف / how:** Event markers -> trigger both audio and particles.
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4164-game-audio-vfx`

#### PART-226 · خبز المحاكاة قبل الريندر · Bake sims before frame renders · 📄 موصوف
- **ماذا / what:** Stateful simulations must be baked so independent frames match; Blender sims do not transfer through GLB.
- **كيف / how:** Bake in Blender, render sequences or export sprite sheets; runtime particles in engine.
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4164-game-audio-vfx/SKILL.md`

#### PART-227 · ماذا يمثل الجسيم الواحد · What does one particle mean · 📄 موصوف
- **ماذا / what:** Particles in data videos must be entity, sample, carrier (direction only) or focus cue; pure texture is not allowed in analytical scenes.
- **كيف / how:** State the unit on screen or in VO; cap counts; sample instead of drawing every edge; pair with static width/labels for quantity; provide a final static frame. Avoid for aggregated or uncertain human harm.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/particle-effects-and-flow.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/deckgl-d3-geo-stack-selection.md`

#### PART-228 · تدفق الجسيمات على المسارات والروابط · Particle flow along routes and edges · 📄 موصوف
- **ماذا / what:** Dots travelling along routes, pipes or network edges to show direction and activity, with fading trails.
- **كيف / how:** Precompute paths (polyline/arc/spline/geodesic); each particle has offset phase and speed; position = pointAt((t*speed+phase) % 1); trail = last k positions with decaying opacity; emission sampled, not one per entity unless real; never all edges at once (filter to focus neighborhood); Three.js Points/instanced quads or PixiJS ParticleContainer for many sprites; Canvas2D for a few hundred.
- **أرقام / params:** trail k 8-20 samples; additive blend clamped
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/particle-effects-and-flow.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/SKILL.md`

#### PART-229 · ذرات صاعدة وحلقات الإيقاع · Rising motes + kick rings · 📄 موصوف
- **ماذا / what:** 72 light motes rise and twinkle, lifted by onsets; each kick sends an expanding ring for 1.3 s.
- **كيف / how:** verse.html draw(t) with SOUND.kicks; additive 'lighter' compositing.
- **أرقام / params:** motes r 2-9 px, speed .006-.026/s; ring radius (0.16 + 0.42 dt) min(W,H), alpha .22 (1-dt/1.3)^2
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/verse.html:153` · `100-superskills/skills/kosif-montage-motion/templates/verse.html:161`

#### PART-230 · مفردات المؤثرات البيئية · Environmental VFX vocabulary · 📄 موصوف
- **ماذا / what:** Effect families to specify (or build procedurally) around a subject.
- **كيف / how:** Name the effect, its direction and its interaction with light/subject (rain streak direction, splash response, smoke/fire interaction).
- **أرقام / params:** fire, smoke, rain, fog, sparks, debris, dust, energy, splashes, trails, motion blur, wind, haze, cloud layers
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-visual-aesthetics-council/SKILL.md` · `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/visual-execution-contract.md`

#### PART-231 · حقل ضوضاء تحليلي · Analytic noise field · 📄 موصوف
- **ماذا / what:** Deterministic noise from summed prime-frequency sines or seeded simplex, scrolled through time.
- **أرقام / params:** 3–4 sines; 0.1–0.3 units/s
- **الدليل / proof:** `kosif-tool/playbooks/code.md:28`

#### PART-232 · خلفية خطوط تدفق توليدية · Generative flow-line backdrop · 📄 موصوف
- **ماذا / what:** Seeded flow lines behind titles.
- **أرقام / params:** 15% opacity; 0.2 units/s
- **الدليل / proof:** `kosif-tool/playbooks/code.md:47`

#### PART-233 · الجسيمات ذات المعنى · Particle meaning rule · 📄 موصوف
- **ماذا / what:** Particles must show quantity→structure, energy, flow or dissolution; remove decorative dust.
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:9`

#### PART-234 · ميزانية الجسيمات · Particle size/colour/count budget · 📄 موصوف
- **ماذا / what:** Limited sizes and colours; count budget by renderer; behind type; uneven density.
- **أرقام / params:** sizes 4/8/14 px; ≤ 2 colours; 150–600 on Canvas 2D; ≤ 20 000 WebGL points
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:15-18`

#### PART-235 · حقل تدفق · Flow field particles · 📄 موصوف
- **ماذا / what:** Particles follow angle from analytic noise.
- **أرقام / params:** angle = noise(x·0.0025, y·0.0025, t·0.2)·2π; speed 40–120 px/s
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:26`

#### PART-236 · تجمع في شكل أو نص · Gather into shape / text · 📄 موصوف
- **ماذا / what:** Sample target points from shape or offscreen-rendered text, ease each particle to target with per-particle delay.
- **أرقام / params:** 900–1400 ms in-out cubic; delay 0–300 ms
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:27`

#### PART-237 · جذب بالتربيع العكسي · Inverse-square attraction · 📄 موصوف
- **ماذا / what:** Attraction to hero element, clamped, procedural only.
- **أرقام / params:** force ∝ 1/d²
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:28`

#### PART-238 · وصفة انفجار الكشف · Reveal burst recipe · 📄 موصوف
- **ماذا / what:** Hero word scales in, seeded particles burst, ring expands and fades.
- **أرقام / params:** word 0–250 ms spring 14/150; 160 particles 50–3000 ms; ring 100–1100 ms outExpo
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:38-40`

#### PART-239 · تفكك النص · Text dissolve · 📄 موصوف
- **ماذا / what:** Replace word pixels with particles that drift up and fade; Arabic sampled from whole shaped word, readable ≥1 s first.
- **أرقام / params:** drift 200 px; 1.5 s; hold ≥ 1 s
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:44` · `kosif-tool/playbooks/particles.md:72`

#### PART-240 · تيار بيانات على مسار · Data stream along path · 📄 موصوف
- **ماذا / what:** Particles travel along an SVG path with offsets.
- **أرقام / params:** 600 ms per traversal
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:46`

#### PART-241 · شبكات تتموج حول المؤشر · Cursor-field ripple grids · 💡 فكرة
- **ماذا / what:** Dots or grid lines displaced outward around a pointer and relaxing slowly behind it; proximity sharpens near content and softens far content.
- **كيف / how:** Canvas 2D grid with per-point spring back toward rest, force from pointer distance; deterministic when the pointer is scripted.
- **أرقام / params:** near-zero response latency, generous settle
- **الدليل / proof:** `kosif-atlas/skills/342-kernel/1223-frontend/motion/cursor-field.md`

#### PART-242 · جماليات توليدية مُبذّرة · Seeded generative aesthetics · 💡 فكرة
- **ماذا / what:** Seeded deterministic generative art idea from algorithmic-art.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### PART-243 · جسيمات بكسل تنكمش · Shrink-to-die pixel particles · 💡 فكرة
- **ماذا / what:** Spark burst particles that die by losing 1 px per frame instead of alpha fade.
- **كيف / how:** Canvas particle array, size-- each frame.
- **أرقام / params:** 24 particles, 3-5 frame life
- **الدليل / proof:** `style:pm-0xevinho-3777d8`

#### PART-244 · كرة فيزيائية · Physics ball arc with restitution · 💡 فكرة
- **ماذا / what:** Gravity parabola with bounce energy loss and squash/stretch.
- **كيف / how:** Per-frame integration.
- **أرقام / params:** restitution 85%; squash 20% impact; stretch 10%; on screen ≥80%
- **الدليل / proof:** `style:pm-deifosv-04e4d3`

#### PART-245 · تفتت النص لشبكة صور · Text shatter to image grid · 💡 فكرة
- **ماذا / what:** Typed brand name shatters into GPU particles reassembling into a grid of images.
- **كيف / how:** Instanced WebGL (three.js InstancedMesh); random delay ≤150 ms.
- **أرقام / params:** 400-800 particles; 600 ms; 6x4 grid
- **الدليل / proof:** `style:pm-influencer-seo-ce8c33`

#### PART-246 · مطر مائل · Angled rain particles · 💡 فكرة
- **ماذا / what:** Wind-angled rain streaks.
- **كيف / how:** Particle system.
- **أرقام / params:** 300-500 drops; 1.2 s fall; 15°
- **الدليل / proof:** `style:pm-kamstudiolabs-0b0824`

#### PART-247 · أمواج متوازية · Sine-path parallax waves · 💡 فكرة
- **ماذا / what:** Three layered sine wave paths at parallax ratios.
- **كيف / how:** SVG paths.
- **أرقام / params:** 1 : 0.6 : 0.3
- **الدليل / proof:** `style:pm-kamstudiolabs-0b0824`

#### PART-248 · محاكاة الحلقات · Ring escape physics sim · 💡 فكرة
- **ماذا / what:** Ball ricochets within 12 rotating gapped rings; deterministic sim.
- **كيف / how:** Fixed sub-step physics.
- **أرقام / params:** 120 Hz sub-step @60 fps; restitution 1.0; gravity ≤200 px/s²; ring speed 0.3+0.08i rad/s alternating; gap 28°
- **الدليل / proof:** `style:pm-kantamk-61f410`

#### PART-249 · تشظي الحلقة · Ring shard burst · 💡 فكرة
- **ماذا / what:** Ring splits into arc shards flying out.
- **كيف / how:** ease-out quad.
- **أرقام / params:** 24 shards; 400-600 px/s; 500 ms fade
- **الدليل / proof:** `style:pm-kantamk-61f410`

#### PART-250 · نص يتحول لمخطط · Prompt to particles to chart · 💡 فكرة
- **ماذا / what:** Prompt dissolves into particles reforming as charts.
- **كيف / how:** Particle targets from chart geometry.
- **أرقام / params:** morph 700 ms
- **الدليل / proof:** `style:pm-listudio-820c7b`

#### PART-251 · سماء دوامية · Curl-noise swirling sky · 💡 فكرة
- **ماذا / what:** Sky flows with curl noise and global rotation, never pauses.
- **كيف / how:** Curl noise flow field.
- **أرقام / params:** ~0.15 rad/s
- **الدليل / proof:** `style:pm-mandelduck-95fd08`

#### PART-252 · خطوط سرعة شعاعية · Radial speed lines · 💡 فكرة
- **ماذا / what:** Strokes from frame edge to centre regenerated per hit.
- **كيف / how:** Canvas: random radial strokes, lifetime 3-5 frames.
- **أرقام / params:** 80-140 lines; 3-5 frames life
- **الدليل / proof:** `style:pm-micheleharmonic-77628e`

#### PART-253 · رمية قوسية بأثر · Parabolic toss with trail · 💡 فكرة
- **ماذا / what:** Token thrown on parabola with fading sample trail.
- **كيف / how:** Sample positions; draw 12 ghost copies.
- **أرقام / params:** 900 ms; 12 samples; trail fade 200 ms
- **الدليل / proof:** `style:pm-paulo-kombucha-96431c`

#### PART-254 · منسوب سائل متموج · Pour level with sine wobble · 💡 فكرة
- **ماذا / what:** Liquid level eases to exact amount with damped surface wobble.
- **كيف / how:** Canvas/SVG; cubic-bezier(0.33,0,0.2,1).
- **أرقام / params:** wobble 2-4 px @1.5 Hz; damp 600 ms; pour 2.5-3 s
- **الدليل / proof:** `style:pm-ror-fly-9950f1`

#### PART-255 · سقوط مكعبات الثلج · Ice-cube bounce drop · 💡 فكرة
- **ماذا / what:** easeOutBounce 700 ms; bounce 12 px; 180 ms stagger
- **أرقام / params:** fill easeOutCubic 1400-1800 ms; ripple 2-3 px
- **الدليل / proof:** `style:pm-sarut0bisasuke-cefa43`
