# الأشكال والتحوّل — Shapes & morphing

> فصل مُجمَّع آليًا من 204 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **197 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 197 powers deduplicated by name from 204 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 7 · 🟢 جاهز 24 · 📦 بأمر تثبيت 39 · 👁 شوهد في فيديو 102 · 📄 موصوف 14 · 💡 فكرة 11

#### SHAPE-01 · تموج ضغطة · Press ripple with heat bloom · ✅ مُثبت هنا
- **ماذا / what:** Expanding ring that shoves coordinates outward and adds heat.
- **كيف / how:** Ring radius grows over 0.9s; displacement 0.18, heat 0.55.
- **أرقام / params:** ripple 0.18, bloom 0.55, 0.9s
- **الدليل / proof:** `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/SKILL.md`

#### SHAPE-02 · توزيع حلزوني بالزاوية الذهبية · Golden-angle spiral placement · ✅ مُثبت هنا
- **ماذا / what:** Places N items evenly around a centre without geometry data (districts around their city) using a sunflower spiral.
- **كيف / how:** districtSpots(n,R): r = R*sqrt((i+.6)/n), a = i*2.39996 rad; dx=r*cos a, dy=r*sin a.
- **أرقام / params:** golden angle 2.39996 rad; R = min(58, 20+3n)
- **الدليل / proof:** `kosif-earth-ci-fork/app/src/engine/fusion/sales/sales-geo-engine.ts:83`

#### SHAPE-03 · خطان قطريان منجرفان · Exactly two drifting diagonal background lines · ✅ مُثبت هنا
- **ماذا / what:** Signature motif: two translucent curved diagonal lines behind everything that drift continuously and never stop; never three.
- **كيف / how:** for k in 0..1: ox=sin(phase*.20+k*2.3)*0.035w, oy=cos(phase*.16+k)*0.02h; quadratic curve from (-.2w+k*.63w, .93h) via (.30w+k*.41w, .43h) to (.65w+k*.5w, -.10h); stroke line colour 50% alpha, width 1.6*scale.
- **أرقام / params:** 2 lines; drift ±3.5% w, ±2% h
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:47-49` · `fastify-motion-bro/docs/VIRAL-EDITORIAL-DNA.md:18` · `fastify-motion-bro/tests/viral-editorial.test.mjs:8`

#### SHAPE-04 · دمج ناعم للأشكال · Smooth CSG (add / sub / and) · ✅ مُثبت هنا
- **ماذا / what:** Smooth union, subtraction and intersection with a blend radius k in metres; colours blend with the same weights.
- **كيف / how:** Pass {op:'add'|'sub'|'and', k, color} to any sculpt primitive.
- **أرقام / params:** k e.g. .012 m smooth union; sub with color tints the carved cavity (tested: tint red 1.0, plain side 0)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:104` · `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:123` · `100-superskills/skills/kosif-montage-motion/tests/test_shape_kit.py:31`

#### SHAPE-05 · نحت بدوال المسافة إلى مجسم مغلق · SDF sculpting to watertight mesh · ✅ مُثبت هنا
- **ماذا / what:** Characters and objects are sculpted from signed-distance primitives (sphere, box, smooth union, subtract with tint) and meshed with surface nets into closed, accurate geometry in the browser or Node.
- **كيف / how:** S.sculpt().sphere(c, r).sphere(c2, r2, {k}).box(c, size, round).sphere(c, r, {op:'sub', k, color}).mesh({cells}); coarse-to-fine evaluation skips empty space.
- **أرقام / params:** tests: sphere volume ±2%, area ±3%, radius error <1e-3, 0 open edges; evals <60% of full grid; smooth-union gap <−0.005
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/js/shape_kit_check.cjs:31` · `100-superskills/skills/kosif-montage-motion/tests/test_shape_kit.py:21` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:46`

#### SHAPE-06 · محلّل لغة مسارات SVG كاملة · Full SVG path language parser · ✅ مُثبت هنا
- **ماذا / what:** Parses M L H V C S Q T A Z (absolute and relative, smooth reflections, glued arc flags) into polygons, with arcs converted by the SVG centre-parameterisation.
- **كيف / how:** render.path('M ... Z', n=14) returns one polygon per subpath; _arc samples max(4, |dt|/2pi*64) points.
- **أرقام / params:** 14 samples per Bezier segment
- **الدليل / proof:** `kosif-studio/render.py:87` · `kosif-studio/render.py:192` · `kosif-studio/tests/test_studio.py:55`

#### SHAPE-07 · أشكال مركبة بثقوب · Even-odd compound shapes and holes · ✅ مُثبت هنا
- **ماذا / what:** Rings, letters with counters and logo cut-outs: subpaths bridged to one anchor so even-odd filling cancels the bridges, or explicit Hole polygons that erase.
- **كيف / how:** render.compound(polys); render.Hole([...]) drawn after the shape it cuts; to_python._bridge for Pillow programs.
- **الدليل / proof:** `kosif-studio/render.py:25` · `kosif-studio/render.py:229` · `kosif-studio/to_python.py:80`

#### SHAPE-08 · تحول شكل إلى شكل · SVG path morph · 🟢 جاهز
- **ماذا / what:** One SVG shape becomes another by resampling both paths to N points and interpolating; seek-safe.
- **كيف / how:** MOTION.morphPath(tl, pathEl, fromD, toD, at, {points, dur, ease, open}).
- **أرقام / params:** N=120 points, dur 0.66 s, ease E.inOut
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:255` · `kosif-studio/motion/kit/motion-kit.js:255`

#### SHAPE-09 · تحول أيقونة القائمة إلى إغلاق · Hamburger-to-close icon morph · 🟢 جاهز
- **ماذا / what:** Three bars become an X: top and bottom rotate opposite 45 degrees while the middle collapses.
- **كيف / how:** Framer Motion or CSS transitions on three spans.
- **أرقام / params:** rotate +-45deg; middle opacity 0 scaleX 0; 0.2s
- **الدليل / proof:** `kosif-atlas/skills/3529-ui-design/14308-interaction-design/references/microinteraction-patterns.md`

#### SHAPE-10 · حركة على مسار SVG · Motion along an SVG path · 🟢 جاهز
- **ماذا / what:** Move a dot, icon or cursor along an arbitrary curve, e.g. a slider following a growth curve or a plane on a route.
- **كيف / how:** GSAP MotionPathPlugin {motionPath:{path:'M ... C ...'}} or own sampler using SVGPathElement.getPointAtLength().
- **أرقام / params:** 1.5s power2.out typical
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### SHAPE-11 · أشكال طافية ومؤشر تمرير · Floating ambient shapes and scroll hint · 🟢 جاهز
- **ماذا / what:** Continuous decorative drift uses CSS keyframes with different periods so shapes never move in lockstep; a small bouncing chevron hints at more content.
- **كيف / how:** @keyframes with translate/rotate, ease-in-out infinite; chevron translateY bounce.
- **أرقام / params:** periods 10s/12s/16s; drift 12-30px, rotate 5-8deg; chevron 8px every 2s (16px+ anxious, 4px invisible)
- **الدليل / proof:** `kosif-atlas/skills/196-landing/621-landing/references/gsap_animation_patterns.md`

#### SHAPE-12 · نص على مسار · Text along SVG motion path · 🟢 جاهز
- **ماذا / what:** Move labels or words along a curve.
- **كيف / how:** GSAP MotionPathPlugin path 'M..C..'; or SVG <textPath> (Arabic shapes fine in textPath in Chromium).
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### SHAPE-13 · حلقات مدارية دوّارة · Orbiting arc cluster · 🟢 جاهز
- **ماذا / what:** Six 270-degree arcs orbit a centre point at varying distance, alternating teal and lime, with pulsing opacity and gentle whole-group sway.
- **كيف / how:** translate(w*.5,h*.34), rotate(sin(phase*.31)*.12); arc k: angle=phase*.5+k*PI/3, dist=w*(.15+.055 sin), radius w*(.04+.016 sin), sweep 1.5*PI, stroke #89d6ce/#d5f375, alpha .24+.25*sin^2, width max(2, .007w).
- **أرقام / params:** 6 arcs; sweep 270°; colours #89d6ce #d5f375
- **الدليل / proof:** `fastify-motion-bro/web/motion.js:13-14`

#### SHAPE-14 · نواة دائرية نابضة · Pulsing lime donut core · 🟢 جاهز
- **ماذا / what:** A breathing lime ring at the orbit centre made of a filled disc with a dark inner disc.
- **كيف / how:** r=w*(.12+.025*sin(phase*1.25)); fill #c9f96d at r, then #0a1724 at 0.58r.
- **أرقام / params:** radius 12%±2.5% of width; inner 58%
- **الدليل / proof:** `fastify-motion-bro/web/motion.js:15`

#### SHAPE-15 · خطوط موجية متحركة · Animated sine-wave strands · 🟢 جاهز
- **ماذا / what:** Three coloured sine waves cross the lower half and grow in amplitude as the scene progresses, standing in for 'hand-drawn infographic' lines.
- **كيف / how:** For line 0..2: y=h*(.55+.07*line)+sin(x/w*3PI+phase*2+line*1.9)*(10+12p), step 4 px, colours #d3f66a #6ad8d1 #e995ff, alpha .42, width max(2,.004w).
- **أرقام / params:** 3 waves; 1.5 cycles across width; amplitude 10→22 px
- **الدليل / proof:** `fastify-motion-bro/web/motion.js:16`

#### SHAPE-16 · بقعة عضوية في الزاوية · Soft organic corner blob · 🟢 جاهز
- **ماذا / what:** Large soft tinted ellipse bleeding off the top-right corner as part of the environment.
- **كيف / how:** ellipse centre (.93w,.14h), radii .35w x .13h, rotation PI/5, shape colour, alpha .65.
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:50-51`

#### SHAPE-17 · مكتبة 16 أيقونة متجهية · 16-icon vector hero library · 🟢 جاهز
- **ماذا / what:** Hand-coded Canvas path icons usable as hero objects: eye, brain, wallet, money, screen, hourglass, lightbulb, rocket, clock, cursor, chart, stairs, domino, book, people, chess, plus a default star-asterisk.
- **كيف / how:** icon(ctx, name, r, accent, ink) with round joins, stroke width .08r; select via scene.hero.
- **أرقام / params:** 16 named + default
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:12-34`

#### SHAPE-18 · حلقة مدار تجميلية · Orbit ring accent · 🟢 جاهز
- **ماذا / what:** Thin accent-coloured ellipse orbiting around the hero, slowly tilting.
- **كيف / how:** ellipse (.5w,.405h) radii .283w x .157h, rotation sin(phase*.1)*.12, stroke 2.5*scale accent.
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:67-68`

#### SHAPE-19 · نجمة رباعية دوارة · Rotating four-spoke starburst · 🟢 جاهز
- **ماذا / what:** Small accent starburst near top right that spins continuously.
- **كيف / how:** translate(.82w,.273h), rotate(phase*.21), 4 spokes from 10 to 24 scale-px.
- **أرقام / params:** 4 spokes; 0.21 rad per phase unit
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:67-70`

#### SHAPE-20 · تحويل الأشكال · SVG path morph (morphPath) · 🟢 جاهز
- **ماذا / what:** Morphs one SVG path into another by resampling both to N points and interpolating; no plugin needed.
- **كيف / how:** MOTION.morphPath(tl, pathEl, fromD, toD, at, {points, dur, ease, open}).
- **أرقام / params:** N=120 points; dur 0.66 s; ease E.inOut; closes with Z unless open
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:255`

#### SHAPE-21 · أنبوب عبر نقاط · Tube along points · 🟢 جاهز
- **ماذا / what:** Catmull-Rom TubeGeometry for mouths, whiskers, cables.
- **كيف / how:** K3S.tube(points, r, color, {segments}).
- **أرقام / params:** 32 segments; 8 radial; roughness .6
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:329`

#### SHAPE-22 · حلقات إهليلجية دوّارة · Rotating orbital ellipse rings · 🟢 جاهز
- **ماذا / what:** Three concentric tilted ellipse outlines that rotate slowly around the glow centre for an orbital, 'study' feel.
- **كيف / how:** ctx.rotate(t·0.1); ellipse radii r·(0.66+i·0.18) by r·(0.2+i·0.11), tilt 0.3+i·0.65 rad; line width 0.002·min(w,h).
- **أرقام / params:** 3 rings; 0.1 rad/s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:68`

#### SHAPE-23 · طبقات الأشكال: دائرة وشريط · Shape layers: circle and rounded bar · 🟢 جاهز
- **ماذا / what:** Animated accent shapes over scenes: a filled circle, or a rounded rectangle bar used as an underline/accent.
- **كيف / how:** overlay.type='shape', shape 'circle' (arc radius size/2) or 'rectangle' (roundRect width size, height 0.24·size, radius max(2, 0.06·size)).
- **أرقام / params:** default size 16%, colour #52dbc6 (initial bar #55dbc4 at y 72%)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:76` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:158`

#### SHAPE-24 · نحت أشكال ناعمة بالحقول المسافية · SDF sculpting of soft 3D shapes · 🟢 جاهز
- **ماذا / what:** Characters and props as a list of soft primitives blended with smooth union/subtraction/intersection, meshed into a watertight geometry with vertex colours; no modelling package.
- **كيف / how:** K3S.sculpt().ellipsoid(c,r,{k,color,op,rot}).sphere().capsule(a,b,r1,r2).box(c,h,round).torus(c,R,r).paint(c,r,colour,{soft}); geo = S.mesh({cells:120}).
- **أرقام / params:** ops add/sub/and; k blend radius in metres (10-30 mm for plush); 136-cell body ~1.5 s, bunny 274k triangles ~4 s
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/shape-kit.js:1` · `kosif-one/tools/kosif-studio/motion/references/shape-kit.md`

#### SHAPE-25 · لغة المشهد بالخطوات · Scene language (Step programs) · 🟢 جاهز
- **ماذا / what:** A picture is an ordered program of Steps made of vector shapes, gradients, light and particles, re-rendered at any size on a 1200x800 sheet.
- **كيف / how:** def build(): return [Step(name, [ops...], order, origin=...)] ; shapes rect, ellipse(cx,cy,rx,ry,rot), poly, path('M..C..A..Z'), compound/Hole, tube(spine, radii), dots, stroke(polys,width), catmull, translate, union.
- **أرقام / params:** sheet 1200x800; supersampling ss=3; render(steps, scale)
- **الدليل / proof:** `kosif-one/tools/kosif-studio/render.py:1` · `kosif-one/tools/kosif-studio/render.py:259` · `kosif-one/tools/kosif-studio/references/drawing-guide.md`

#### SHAPE-26 · منحنيات كاتمول-روم الناعمة · Catmull-Rom smooth curves · 🟢 جاهز
- **ماذا / what:** Turns a few control points into a smooth curve through them, open or closed; the base for tubes, whale profiles and organic outlines.
- **كيف / how:** render.catmull(points, n=10, closed=False).
- **أرقام / params:** n samples per segment (default 10)
- **الدليل / proof:** `kosif-studio/render.py:57`

#### SHAPE-27 · أنبوب بنصف قطر متغير · Variable-radius tube (limbs, tails, horns, flames, hair) · 🟢 جاهز
- **ماذا / what:** Builds an organic stroke along a smooth spine with a radius at each spine point, as a union of quads and discs so tight bends never punch holes.
- **كيف / how:** render.tube(spine, radii, n=8); radii interpolated along catmull samples.
- **أرقام / params:** discs every n//2 samples where r>0.6
- **الدليل / proof:** `kosif-studio/render.py:286` · `kosif-studio/scenes/dragon_girl.py:229`

#### SHAPE-28 · خطوط بسُمك ونهايات دائرية · Round-joined stroke outlines · 🟢 جاهز
- **ماذا / what:** Converts polylines into filled outlines of a given width with round caps/joins (quads plus discs) — used for rain, pleats, mouth lines and SVG strokes.
- **كيف / how:** render.stroke(polys, width, closed=False).
- **أرقام / params:** discs n=12 below r 3 else 24
- **الدليل / proof:** `kosif-studio/render.py:241`

#### SHAPE-29 · عدة الأشكال الأساسية · Basic shape kit (rect, ellipse with rotation, poly, dots, translate, union) · 🟢 جاهز
- **ماذا / what:** Minimal vector primitives in scene units that return polygon lists and compose by union.
- **كيف / how:** rect(x,y,w,h); ellipse(cx,cy,rx,ry,rot,n=48); poly(pts); dots([(x,y,r)]); translate(shape,dx,dy); union(*shapes).
- **أرقام / params:** ellipse 48 segments; dots 10/20 segments
- **الدليل / proof:** `kosif-studio/render.py:259` · `kosif-studio/render.py:267` · `kosif-studio/render.py:278`

#### SHAPE-30 · سلاسل جبال بالإزاحة العشوائية · Midpoint-displacement mountain ridges · 🟢 جاهز
- **ماذا / what:** Generates layered mountain silhouettes by recursive midpoint displacement with optional carved peaks, filled down to the sheet bottom.
- **كيف / how:** scenes/dragon_girl.ridge(seed, base, amp, rough=0.55, peaks=[(x, height, width)]); importable by other scenes.
- **أرقام / params:** 7 subdivision rounds; amplitude x rough per round
- **الدليل / proof:** `kosif-studio/scenes/dragon_girl.py:20` · `kosif-studio/scenes/dragon_girl.py:174`

#### SHAPE-31 · الانضغاط والتمدد بحفظ المساحة · Area-preserving squash & stretch · 🟢 جاهز
- **ماذا / what:** Impact squash then spring recovery.
- **كيف / how:** Canvas ctx.scale(1+s·0.3, 1−s·0.3) around contact; s from KOSIF.window01(t,hit,hit+0.08,0.02,0.06).
- **أرقام / params:** scaleY 0.7/scaleX 1.3 for 80 ms; spring {damping 10, stiffness 220}
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:25` · `kosif-tool/playbooks/shapes.md:66`

#### SHAPE-32 · زخرفة ثمانية · Eight-point rosette interlude · 📦 بأمر تثبيت
- **ماذا / what:** Two squares at 0/45° + circle (a khatam-like rosette) drawn on during instrumental interludes, rotating 9°/s and breathing on the beat.
- **كيف / how:** V.interludes [{t, end}].
- **أرقام / params:** R 150·k, stroke 2.2·k, draw 1.1 s stagger .12
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/templates/verse.html` · `kosif-studio/motion/templates/verse.html:216` · `kosif-studio/motion/verse.py:258` · `100-superskills/skills/kosif-montage-motion/templates/verse.html:298`

#### SHAPE-33 · الحركة على مسار · GSAP MotionPathPlugin · 📦 بأمر تثبيت
- **ماذا / what:** Move an element along an SVG path with auto-rotation to the path tangent (planes, arrows, comets).
- **كيف / how:** gsap.registerPlugin(MotionPathPlugin); tl.to(el,{motionPath:{path:'#route', align:'#route', autoRotate:true}, duration:2, ease:'power1.inOut'}). Pair with a stroke-dashoffset draw of the same path.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### SHAPE-34 · كتلة عضوية متموجة · Noise-displaced blob · 📦 بأمر تثبيت
- **ماذا / what:** Sphere vertices pushed along normals by animated noise for a living blob.
- **كيف / how:** Vertex shader: disp=pnoise(position*1.5+time*0.5); newPos=position+normal*disp*intensity.
- **أرقام / params:** freq 1.5, speed 0.5
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### SHAPE-35 · كتلة مموجة بالضوضاء · Vertex noise blob · 📦 بأمر تثبيت
- **ماذا / what:** Sphere displaced along normals by time-driven Perlin noise for a living blob.
- **كيف / how:** three.js ShaderMaterial; displacement = pnoise(position*1.5 + t*0.5)*intensity.
- **أرقام / params:** freq 1.5, speed 0.5
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`

#### SHAPE-36 · انفجار الأشكال · Shapes burst emphasis scene · 📦 بأمر تثبيت
- **ماذا / what:** A 0.6-1 s burst of 14 radial lines and an expanding ring for emphasis.
- **كيف / how:** TEMPLATES.shapes: lines from r0=m(0.1+0.25k) to r1=m(0.16+0.42k)*jitter, alternating accent/primary, ring radius 0.42m*k, fades over the second half.
- **أرقام / params:** 14 lines
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:518`

#### SHAPE-37 · عناصر إيموجي ونص وملصقات · Emoji, text and sticker pop-ups · 📦 بأمر تثبيت
- **ماذا / what:** Timed overlays that spring in with a slight wobble: emoji, accent text pills, or image/SVG stickers.
- **كيف / how:** drawOverlays(): spring(z .4, w 17) scale, rotate sin(3l)*0.03, 0.2 s fade-out; positions top 30%, center 47%, bottom 64%, corner (78%,16%); emoji 17% m; text Lalezar 6.5% m on accent pill; stickers 46% m (26% in corner) with white card or SVG shadow.
- **أرقام / params:** pos top|center|bottom|corner
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:412`

#### SHAPE-38 · شبكة متحركة · Dynamic Grid · 📦 بأمر تثبيت
- **ماذا / what:** CSS-variable-driven animated grid background for SaaS/code/data scenes.
- **كيف / how:** Install with `npx hyperframes add dynamic-grid` (copies to compositions/components/dynamic-grid.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fram…
- **أرقام / params:** density fine|standard|coarse; weight hairline|standard|bold; vars: density=standard[fine|standard|coarse]; weight=hairline[hairline|standard|bold]; tone=neutral[neutral|green|blue|violet]
- **تثبيت / install:** `npx hyperframes add dynamic-grid` (copies to compositions/components/dynamic-grid`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/dynamic-grid/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/dynamic-grid/dynamic-grid.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/dynamic-grid.mdx`

#### SHAPE-39 · تحول متعدد الأوجه · Facet Morph · 📦 بأمر تثبيت
- **ماذا / what:** A 36-triangle low-poly mass morphs between three silhouettes (blob, mark, badge) with per-facet flat shading lit from the upper left.
- **كيف / how:** Install with `npx hyperframes add facet-morph` (copies to compositions/components/facet-morph.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame …
- **أرقام / params:** forms "blob,mark,badge"; hold_last true; vars: forms=blob,mark,badge; hold_last=True; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add facet-morph` (copies to compositions/components/facet-morph`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/facet-morph/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/facet-morph/facet-morph.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/facet-morph.mdx`

#### SHAPE-40 · فاصل · Separator · 📦 بأمر تثبيت
- **ماذا / what:** 1-pixel structural separator (horizontal/vertical) with seek-safe progress reveal.
- **كيف / how:** Install with `npx hyperframes add separator` (copies to compositions/components/separator.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame capt…
- **أرقام / params:** thickness hairline|medium|bold; vars: orientation=horizontal[horizontal|vertical]; thickness=hairline[hairline|medium|bold]; tone=neutral[neutral|accent|warning]
- **تثبيت / install:** `npx hyperframes add separator` (copies to compositions/components/separator`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/separator/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/separator/separator.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/separator.mdx`

#### SHAPE-41 · الكتلة الناعمة · Soft Blob Touch · 📦 بأمر تثبيت
- **ماذا / what:** Grainy soft blob idles; a touch dot arrives, blob bulges toward it and recovers on a velocity-preserving spring.
- **كيف / how:** Install with `npx hyperframes add soft-blob-touch` (copies to compositions/components/soft-blob-touch.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **أرقام / params:** touch_x 66; touch_y 38; touch_at 1.6 s; grain fine|coarse; vars: touch_x=66(8..92); touch_y=38(8..92); touch_at=1.6(0.9..10); grain=fine[fine|coarse]; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add soft-blob-touch` (copies to compositions/components/soft-blob-touch`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/soft-blob-touch/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/soft-blob-touch/soft-blob-touch.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/soft-blob-touch.mdx`

#### SHAPE-42 · الانقسام اللزج · Gooey Split · 📦 بأمر تثبيت
- **ماذا / what:** Dot splits into a three-dot menu through a metaball neck, spins to a swirl mark under directional shutter blur, then re-merges.
- **كيف / how:** Install with `npx hyperframes add gooey-split` (copies the full composition to compositions/gooey-split.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 4.7 s; SVG blur+threshold goo; 1920x1080; duration 4.7 s
- **تثبيت / install:** `npx hyperframes add gooey-split` (copies the full composition to compositions/gooey-split`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/gooey-split/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/gooey-split/gooey-split.html`

#### SHAPE-43 · حلقات متموجة · Ripples · 📦 بأمر تثبيت
- **ماذا / what:** White concentric rings rippling outward on black. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add ripples` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="Ripples" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="Ripples"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add ripples` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/ripples/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/ripples/ripples.html` · `kosif-one/vendor/hyperframes/registry/blocks/ripples/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### SHAPE-44 · حلزون · Spiral · 📦 بأمر تثبيت
- **ماذا / what:** Bold black-and-white spiral turning (op-art). A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add spiral` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="Spiral" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="Spiral"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add spiral` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/spiral/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/spiral/spiral.html` · `kosif-one/vendor/hyperframes/registry/blocks/spiral/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### SHAPE-45 · خطوط قطرية · Stripes · 📦 بأمر تثبيت
- **ماذا / what:** Bold black-and-white diagonal stripes sliding. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add stripes` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="Stripes" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="Stripes"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add stripes` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/stripes/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/stripes/stripes.html` · `kosif-one/vendor/hyperframes/registry/blocks/stripes/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### SHAPE-46 · خلايا فورونوي · Voronoi · 📦 بأمر تثبيت
- **ماذا / what:** Magenta cells with glowing blue centres reshaping. A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add voronoi` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="Voronoi" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="Voronoi"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add voronoi` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/voronoi/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/voronoi/voronoi.html` · `kosif-one/vendor/hyperframes/registry/blocks/voronoi/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### SHAPE-47 · أيقونات SVG حية · Living SVG icons · 📦 بأمر تثبيت
- **ماذا / what:** Animate inner SVG parts (clock hands, fan blades, pulsing dots, dash-flow lines) using the SVG transform attribute rotate(deg cx cy) for exact centers.
- **كيف / how:** Read hyperframes-animation/rules/svg-icon-enrichment.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** ease none for linear rotation; setAttribute('transform', 'rotate(d cx cy)')
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/svg-icon-enrichment.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### SHAPE-48 · تحول البطاقة كمرساة انتقال · Card morph anchor handoff · 📦 بأمر تثبيت
- **ماذا / what:** A container morphs apparent size (uniform scale), corner radius, background and shadow between two shots then fades to reveal the real target.
- **كيف / how:** Read hyperframes-animation/rules/card-morph-anchor.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** MORPH_DUR power2.inOut; fades power1.in/out by fraction
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/card-morph-anchor.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### SHAPE-49 · حركة على مسار منحني · MotionPath along SVG curve · 📦 بأمر تثبيت
- **ماذا / what:** Animate an element along an arbitrary SVG path with GSAP MotionPathPlugin.
- **كيف / how:** gsap.registerPlugin(MotionPathPlugin); tl.to('.dot',{motionPath:{path:'M 12 300 C ...'},duration:1.5,ease:'power2.out'}).
- **أرقام / params:** 1.5 s power2.out
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/techniques.md`

#### SHAPE-50 · انتقال العنصر المشترك (FLIP) · FLIP / shared element continuity · 📦 بأمر تثبيت
- **ماذا / what:** Keep one element alive as it changes box or hierarchy between states, so identity is continuous rather than crossfaded.
- **كيف / how:** Use one continuous transform tween or FLIP between source/final boxes; split x/y/scale into eased keyframes only for deliberate beats.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/SKILL.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/references/keyframe-patterns.md`

#### SHAPE-51 · تحويل شكل SVG إلى آخر · SVG shape morph · 📦 بأمر تثبيت
- **ماذا / what:** Interpolate one SVG shape into another; convert primitives to paths and split complex silhouettes.
- **كيف / how:** MorphSVGPlugin preferred; verify with `hyperframes keyframes --shot`.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/SKILL.md`

#### SHAPE-52 · حركة إيقاعية: liquid-morph · Beat motion primitive: liquid-morph · 📦 بأمر تثبيت
- **ماذا / what:** Liquid blob morph, anchored to music events (phrase / transition).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/liquid-morph/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: phrase / transition; best span 1.0-2.5 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/liquid-morph/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### SHAPE-53 · تحول الشكل · morphPath · 📦 بأمر تثبيت
- **ماذا / what:** One shape becomes the next as a seam.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** morphPath
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### SHAPE-54 · تحول شكل: نقطة إلى زر إلى شريط تقدم · Shape morph chain: dot → button → progress bar · 📦 بأمر تثبيت
- **ماذا / what:** One red dot is the visual through-line: it falls, becomes a pill button that is clicked, flattens into a progress bar, rides a spring curve, becomes a full stop.
- **كيف / how:** pill set at scaleX 44/400, scaleY .44 then → 1,1 in 0.42 s E.inOut at beat 4; after press: scaleX 2.0, scaleY .24 in 0.34 s, swap to #bar; #fill width 0→800 linear 1.1 s; counter 0→900.
- **أرقام / params:** 120 BPM beat grid
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:66` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:78` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:89`

#### SHAPE-55 · حلقة تتحول إلى قزحية تغمر الإطار · Ring → iris → colour flood · 📦 بأمر تثبيت
- **ماذا / what:** A drawn ring shrinks and thickens into an iris point, then a circular clip opens from that point to flood the frame with the brand colour.
- **كيف / how:** tl.to(ring, {scale:.14, strokeWidth:60, 0.45 s, E.in}, 3.65); M.iris(tl, brand, 4.05, {x:540, y:930, r0:60, r:2300, dur:.5}) (log-space ease) + M.flash peak .6.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:80` · `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:82` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:334`

#### SHAPE-56 · بناء الزخرفة الثمانية · Islamic eight-point rosette builder · 📦 بأمر تثبيت
- **ماذا / what:** Generates a geometric rosette from code (two rotated squares forming an eight-point star, a 16-vertex star, a circle and a small inner star), draws each part in sequence and slowly rotates the whole.
- **كيف / how:** sq(78,0), sq(78,PI/4), star8(120,92), circle r48, star8(30,14); M.drawPath each at 0.4+i*0.18 s for 1.3 s opacity .85; rosette rotates 0 -> 45 degrees over the film; stroke #f6d27a width 3 -> 5 on آمين.
- **أرقام / params:** centre (540,760)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html:119-122` · `kosif-one/projects/thursday-dua-animation/source/index.html:195-196`

#### SHAPE-57 · فوانيس تتأرجح بتوهج · Swaying lanterns with breathing glow · 📦 بأمر تثبيت
- **ماذا / what:** Two hanging lanterns built from SVG primitives that swing like pendulums and pulse their glow independently.
- **كيف / how:** Group per lantern: chain line, radial glow circle r120, cap, body hexagon fill #ffcf72 .92 stroke #c48a2c, ribs #b07a22, tip; rotation ±3.5 degrees yoyo 2.2/2.5 s repeat 11 (svgOrigin 0 0); glow opacity .7 -> 1 yoyo .96 s.
- **أرقام / params:** x 200 / 880, chain 300 / 360
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html:124-134` · `kosif-one/projects/thursday-dua-animation/source/index.html:164-167`

#### SHAPE-58 · صورة ظلية لمسجد بنوافذ مضيئة · Mosque silhouette with flickering windows · 📦 بأمر تثبيت
- **ماذا / what:** A dome, two minarets and ground band as flat silhouette paths, with small arched windows that flicker softly.
- **كيف / how:** Paths in #1d0f2c, ground #140920; 8 arched window paths #ffc768 with opacity .55 -> 1 yoyo 0.9-1.7 s repeat 30 at random offsets.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html:62-71` · `kosif-one/projects/thursday-dua-animation/source/index.html:136-139`

#### SHAPE-59 · حلقة ترسم ونبض قلب · Ring draw + heartbeat ripples · 📦 بأمر تثبيت
- **ماذا / what:** A gold ring draws around the sun on 'live every moment', and on two beats a second ring expands and fades like a heartbeat.
- **كيف / how:** circle r150 stroke #f5c97a 5 px drawPath 1.1 s; ring2 opacity .9 scale 1 -> 1.9, opacity 0 in 0.9 s E.out at 36.14 and 38.94 s (transform-origin 540px 1030px).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html:69-70` · `kosif-one/projects/whatsapp-motion/projects/success/index.html:259-264`

#### SHAPE-60 · غيمة من دوائر تكبر وتعتم · Circle-cluster cloud that grows, drifts and darkens · 📦 بأمر تثبيت
- **ماذا / what:** Clouds made of five circles and a rounded base grow over the sea, drift over the mountain and darken before rain, then lighten.
- **كيف / how:** cloud(): circles (0,0,62) (-75,18,46) (78,18,50) (-32,-34,52) (38,-40,58) + rect 248x58 rx29; scale .2 -> 1 (3.8-5.0 s), drift 4.9-6.2 s; colour mix #FFFFFF -> #A6B9CC and base #DCE8F2 -> #8FA3B8 for dark 6.0-6.5 s, back after 8.3 s.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/index.html:109-115` · `kosif-one/projects/water-cycle-animation/index.html:159-168`

#### SHAPE-61 · تحويل الأشكال بإعادة العينة · SVG path morph by resampling · 📦 بأمر تثبيت
- **ماذا / what:** Morphs one SVG path into another of any structure by sampling both to the same number of points and interpolating.
- **كيف / how:** M.morphPath(tl,pathEl,fromD,toD,at,{points:120,dur:.66,ease:E.inOut,open}).
- **أرقام / params:** 120 points, 0.66 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:254-262`

#### SHAPE-62 · نجمة ثمانية في الفواصل · Interlude eight-point rosette · 📦 بأمر تثبيت
- **ماذا / what:** During long pauses an eight-point rosette is drawn and breathes on the beat, then withdraws.
- **كيف / how:** verse.html interlude block (pause >= 4.5 s).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/templates/verse.html:216`

#### SHAPE-63 · لغة أشكال المشهد · KOSIF scene language shapes · 📦 بأمر تثبيت
- **ماذا / what:** rect, ellipse(rot), poly, full SVG path (arcs/beziers), compound even-odd holes, tube(spine,radii) for limbs/tails/flames, dots for sparks, stroke, translate, catmull spline, union; paints hex/hexa, lin() and rad() gradients.
- **كيف / how:** scenes/<name>.py build() returning Step lists; render.py
- **أرقام / params:** canvas 1200x800
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md` · `100-superskills/skills/pixel-studio-painter/scripts/render.py:87`

#### SHAPE-64 · نحت بحقول المسافة · SDF sculpt primitives · 📦 بأمر تثبيت
- **ماذا / what:** Characters and props as a chain of soft signed-distance primitives (sphere, ellipsoid, round-cone capsule, rounded box, torus) with per-item rotation and colour.
- **كيف / how:** K3S.sculpt().color(hex).sphere(c,r,o).ellipsoid(c,[rx,ry,rz],o).capsule(a,b,r1,r2,o).box(c,[hx,hy,hz],round,o).torus(c,R,r,o); o = {k, op, color, rot:[rx,ry,rz]}.
- **أرقام / params:** units metres; blend radius k typically 10-30 mm
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/shape-kit.js:44` · `kosif-studio/motion/references/shape-kit.md`

#### SHAPE-65 · دمج ونحت ناعم · Smooth union / carve / intersect · 📦 بأمر تثبيت
- **ماذا / what:** Polynomial smooth min/max blends make primitives read as one stuffed, stitched object; colour blends follow the same weights.
- **كيف / how:** o.op = 'add' (default) | 'sub' | 'and' with o.k blend radius.
- **أرقام / params:** h = clamp(.5 ± .5·(d2-d1)/k); d = mix - k·h·(1-h)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/shape-kit.js:100`

#### SHAPE-66 · استعلام الحقل · Field queries for placement · 📦 بأمر تثبيت
- **ماذا / what:** Query distance/colour, project points onto the surface and raycast it, e.g. to seat eyes where a ray from the front meets the face.
- **كيف / how:** S.dist(x,y,z), S.colorAt(...), S.project(p), S.hit(from, dir) -> {point, normal}.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/shape-kit.js:104` · `kosif-studio/motion/references/shape-kit.md`

#### SHAPE-67 · تحول دائرة إلى مربع · Circle-to-square path morph · 📦 بأمر تثبيت
- **ماذا / what:** One shape morphs into another without a cut.
- **كيف / how:** M.morphPath(tl, el, fromD, toD, t, {dur})
- **أرقام / params:** 0.6 s at 4.95 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/kit_v3_demo/index.html:1`

#### SHAPE-68 · أشكال سائلة · Style: Liquid morph (liquid-morph) · 📦 بأمر تثبيت
- **ماذا / what:** Blobby fluid shapes merging and splitting.
- **كيف / how:** SVG path morph with equal point count (64-128) or metaball/gooey filter (blur+threshold); noise-driven vertices. Scaffold: python3 tools/kosif.py scaffold liquid-morph <dir>.
- **أرقام / params:** morph 500-800ms
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:liquid-morph` · `kosif-tool/playbooks/shapes.md`

#### SHAPE-69 · أشكال · Category: Shapes · 📦 بأمر تثبيت
- **ماذا / what:** Capability family 'shapes' (30 catalog entries) with a dedicated bilingual playbook of timings and recipes.
- **كيف / how:** Read playbooks/shapes.md (visual grammar, motion mechanics, scene recipes, QA); build in starters/html-canvas or starters/remotion; filter catalog with python3 tools/kosif.py list --category shapes.
- **أرقام / params:** 24px unit; radii 0/8/24/50%; strokes 2/4/8; morph 500-800ms 64-128pts; squash 0.7/1.3 80ms
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md` · `kosif-tool/catalog/categories.json` · `kosif-tool/catalog/meta.json`

#### SHAPE-70 · تحوّل المسارات بإعادة العينات · Path morph with resampling · 📦 بأمر تثبيت
- **ماذا / what:** Morph only equal-point, same-winding paths; resample first.
- **كيف / how:** flubber or precomputed points; Remotion Morph lerps [x,y] arrays with Easing.inOut(cubic).
- **أرقام / params:** 500–800 ms cubic-bezier(0.65,0,0.35,1); 64–128 points
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:24` · `kosif-tool/playbooks/shapes.md:53-64`

#### SHAPE-71 · زهرة نقاط ذهبية · Phyllotaxis dot flower · 👁 شوهد في فيديو
- **ماذا / what:** n points r=c*sqrt(i), angle=i*137.5deg, rotate
- **أرقام / params:** n~400
- **الدليل / proof:** `style:pm-ajith-io-b5626e` · `style:pm-mrtanviir-132457` · `style:pm-umangratani-57f86a`

#### SHAPE-72 · انفجار خطوط شعاعي · Radial line burst · 👁 شوهد في فيديو
- **ماذا / what:** 12 lines from centre, length eased outExpo, staggered 20ms
- **أرقام / params:** 400 ms
- **الدليل / proof:** `style:pm-stephanlivera-df17a2` · `style:pm-sudo-kiran-49176d`

#### SHAPE-73 · شبكة أشكال باوهاوس · Bauhaus tile grid · 👁 شوهد في فيديو
- **ماذا / what:** grid cells with circles/quarters/triangles in 4 colours, rotate 90° stagger
- **أرقام / params:** back.inOut(1.7), 40 ms
- **الدليل / proof:** `style:pm-web3wesley-7bb108` · `style:pm-zaqailo-212ad3`

#### SHAPE-74 · جدول ماء بشرطات متحركة · Flowing channel dashes · 👁 شوهد في فيديو
- **ماذا / what:** draw a thick blue polyline channel with ink outline and translate white dash segments along its path via strokeDashoffset
- **أرقام / params:** dash 20/60 px, speed ~40 px/s
- **الدليل / proof:** `style:doodle`

#### SHAPE-75 · فتحة في الجسم بجدران تلقائية · Hole with auto walls (even-odd) · 👁 شوهد في فيديو
- **ماذا / what:** inner circle in the same path with reverse winding so extrusion layers show the hole's inner walls automatically
- **أرقام / params:** fill-rule nonzero, reversed subpath
- **الدليل / proof:** `style:fake3d`

#### SHAPE-76 · تحول نقاط عشوائية إلى شبكة · Scatter-to-grid dot morph · 👁 شوهد في فيديو
- **ماذا / what:** each of N dots starts at random point inside source shape and lerps to its grid cell with delay = (row+col)*k (diagonal stagger) and spring easing
- **أرقام / params:** 10x10, k ~25 ms, total ~1 s
- **الدليل / proof:** `style:infographic`

#### SHAPE-77 · شريط ينثني فيصير حلقة · Bar bends into ring · 👁 شوهد في فيديو
- **ماذا / what:** draw as arc of constant length L = bar length; radius r goes from very large to L/(2pi) with log interpolation; centre shifts so the arc stays anchored; then split ring with cumulative strokeDashoffse
- **كيف / how:** draw as arc of constant length L = bar length; radius r goes from very large to L/(2pi) with log interpolation; centre shifts so the arc stays anchored; then split ring with cumulative strokeDashoffset
- **أرقام / params:** ~1 s, stroke width = bar height
- **الدليل / proof:** `style:infographic`

#### SHAPE-78 · صندوق أيزومتريك بثلاث درجات · Three-tone iso box · 👁 شوهد في فيديو
- **ماذا / what:** three polygons (top lightest, left mid, right darkest) of one hue plus a thin translucent white top edge stroke and soft ground shadow
- **أرقام / params:** lightness steps ~+12/0/-12%
- **الدليل / proof:** `style:isometric`

#### SHAPE-79 · ملصقات زخرفية وشرائط تحذير · Decorative stickers and hazard tape · 👁 شوهد في فيديو
- **ماذا / what:** starburst polygons and diagonal striped tapes in corners with slow wobble rotation; colours rotate per scene
- **أرقام / params:** rotate ±6° over 2 s yoyo
- **الدليل / proof:** `style:pm-0xnfrith-5be616`

#### SHAPE-80 · موجة تحول الشبكة · Grid morph wave · 👁 شوهد في فيديو
- **ماذا / what:** border-radius 0→50% with delay = distance*30 ms
- **الدليل / proof:** `style:pm-3xtihor-0f6911`

#### SHAPE-81 · رسم يدوي إلى نظيف · Sketch-to-clean morph · 👁 شوهد في فيديو
- **ماذا / what:** jittered polyline interpolates to smoothed path 500 ms, button 'clean up'
- **الدليل / proof:** `style:pm-adamdesgns-478d6d`

#### SHAPE-82 · أنبوب مخطط · Striped tube path · 👁 شوهد في فيديو
- **ماذا / what:** stroke same path 3x with decreasing width red/white/blue, animate dash offset
- **الدليل / proof:** `style:pm-ajith-io-b5626e`

#### SHAPE-83 · كبسولات وسوم تطفو حول العنوان · Floating tag pills around headline · 👁 شوهد في فيديو
- **ماذا / what:** 6 white rounded pills with blue text at scattered positions avoiding the centre, each rotated randomly ±6 deg, staggered pop-in 120 ms, then idle bobbing sin(t) 4 px
- **أرقام / params:** radius 999px, 1px #c4d8e5 border, bob period 3-4 s
- **الدليل / proof:** `style:pm-alex-prompter-1ea044`

#### SHAPE-84 · خلفية أشعة بطولية · Sunburst hero background · 👁 شوهد في فيديو
- **ماذا / what:** alternating wedges rotating slowly
- **الدليل / proof:** `style:pm-allforbigfire-86ff3c`

#### SHAPE-85 · بحر خطوط مع شخصية رمزية · Line-art sea with mascot · 👁 شوهد في فيديو
- **ماذا / what:** 4-6 horizontal SVG sine paths with slow phase drift and parallax speeds; small flat mascot bobs (rotate ±4 deg) and translates across
- **أرقام / params:** wave amplitude 4-10 px, period 6 s, bob 1.5 s
- **الدليل / proof:** `style:pm-aschapmann-131210`

#### SHAPE-86 · بناء نقطة ثم خط ثم مستوى · Point-line-plane build · 👁 شوهد في فيديو
- **ماذا / what:** Start from a crosshair point with coordinate label, stretch to a ruler line with ticks, extrude/skew into a rotated plane carrying text
- **أرقام / params:** each stage ~1.2 s, easeInOutExpo, skew -25°
- **الدليل / proof:** `style:pm-ayushunleashed-ece3e3`

#### SHAPE-87 · تحويل أشكال بدوال قطبية · Polar-function shape morph · 👁 شوهد في فيديو
- **ماذا / what:** Draw r(θ)=a+b·cos(kθ)^p as filled path, interpolate a,b,k,p between named forms (squircle, burst); show ghost outlines and live formula label on polar grid
- **أرقام / params:** k 4→8, 120 samples, easeInOutCubic 600 ms
- **الدليل / proof:** `style:pm-ayushunleashed-ece3e3`

#### SHAPE-88 · تحويل مسار · 200-vertex path morph · 👁 شوهد في فيديو
- **ماذا / what:** resample both shapes to 200 points and lerp
- **أرقام / params:** 700ms
- **الدليل / proof:** `style:pm-blue-clarity-ef56d0`

#### SHAPE-89 · تفريد أوراق مكدسة · Card fan-out stack · 👁 شوهد في فيديو
- **ماذا / what:** Duplicate the card N times behind, offset each by x+18 px and rotate +2..+6 deg with stagger, numbered tabs on edges
- **أرقام / params:** 6 cards, stagger 70 ms, 400 ms easeOutBack(1.2)
- **الدليل / proof:** `style:pm-bogdandragomir-35e024`

#### SHAPE-90 · بناء كسيري متكرر · Recursive fractal build · 👁 شوهد في فيديو
- **ماذا / what:** Sierpinski levels appear one depth at a time
- **أرقام / params:** 4-6 levels, 200 ms each
- **الدليل / proof:** `style:pm-buildfastwithai-53234e`

#### SHAPE-91 · زخرفة حلقية حول شبكة نقاط · Kolam loop around dot grid · 👁 شوهد في فيديو
- **ماذا / what:** single closed path weaving around n×m dots, drawn with a leading glowing dot
- **أرقام / params:** 7×5 dots
- **الدليل / proof:** `style:pm-buildfastwithai-53234e`

#### SHAPE-92 · حلقة صدمة أرضية · Ground shockwave ring · 👁 شوهد في فيديو
- **ماذا / what:** ellipse stroke radius 0→300 px over 500 ms, alpha fade, flattened y 0.25
- **الدليل / proof:** `style:pm-chrisjdimarco-f068db`

#### SHAPE-93 · تموج شبكة نقاط · Dot grid ripple · 👁 شوهد في فيديو
- **ماذا / what:** grid of diamonds rotating/scaling by distance wave, colour shift to orange
- **الدليل / proof:** `style:pm-codestackr-c071bf`

#### SHAPE-94 · شبكة مربعات متموجة · Tile grid wave · 👁 شوهد في فيديو
- **ماذا / what:** Grid of squares, rotate/scale each by sin(dist-from-centre − t), random accent tiles
- **أرقام / params:** period ~1 s
- **الدليل / proof:** `style:pm-crazyalphaaa-bc7e75`

#### SHAPE-95 · نقطة تتفتح إلى واجهة · Dot-to-interface bloom · 👁 شوهد في فيديو
- **ماذا / what:** glowing 8px dot, scale to rectangle frame 1.2s expo, content fades in
- **الدليل / proof:** `style:pm-dale-vaz-cc612a`

#### SHAPE-96 · حلزون ذهبي فوق مربعات فيبوناتشي · Golden spiral over Fibonacci tiles · 👁 شوهد في فيديو
- **ماذا / what:** nest rectangles in lavender tints, label each (s40..s70), then draw an SVG quarter-arc chain with stroke-dashoffset 1.5-2 s ease-in-out
- **أرقام / params:** stroke 1.5 px dark, fills #c8b8f0 → #e6dcf8
- **الدليل / proof:** `style:pm-ddryo-loos-300829`

#### SHAPE-97 · خلفية أشعة شمسية دوارة · Rotating sunburst ground · 👁 شوهد في فيديو
- **ماذا / what:** Draw 24-32 alternating wedge rays from centre in two close tones, rotate slowly, add radial vignette
- **أرقام / params:** rotation 6-10°/s, tone delta ~8% lightness
- **الدليل / proof:** `style:pm-deebeeeff-50fcd0`

#### SHAPE-98 · شريط تظليل مائل يمسح خلف النص · Slanted highlighter bar wipe · 👁 شوهد في فيديو
- **ماذا / what:** skewed rectangle scales X from 0 to 1 from the left behind a text line, slightly larger than the text box
- **أرقام / params:** skewX -8°, 180-250 ms easeOutCubic
- **الدليل / proof:** `style:pm-deifosv-04e4d3`

#### SHAPE-99 · تحوّل البطاقات إلى حبوب أفقية · Card-to-pill morph · 👁 شوهد في فيديو
- **ماذا / what:** Interpolate width/height/border-radius of portrait cards into wide pills while label moves beside icon; a white disc sweeps across as a connective transition
- **أرقام / params:** ~600 ms easeInOutQuint; radius 16 px -> 999 px
- **الدليل / proof:** `style:pm-elliot-garreffa-f334bc`

#### SHAPE-100 · مروحة عينات الألوان · Swatch fan · 👁 شوهد في فيديو
- **ماذا / what:** stack of rounded rects rotated around pivot, stagger 80 ms
- **الدليل / proof:** `style:pm-ercankeskinx-ec2568`

#### SHAPE-101 · جدار أيقونات مائل · Tilted icon wall · 👁 شوهد في فيديو
- **ماذا / what:** grid of rounded-square tiles with line icons, rotated ~-12 deg, drifting diagonally; one tile highlighted brighter
- **أرقام / params:** tile 90px, radius 18px, opacity 0.25-0.4, drift 20 px/s
- **الدليل / proof:** `style:pm-gabrielbuzziv-4ff0c6`

#### SHAPE-102 · خط حبل يتدلى بالوزن · Sagging rope baseline · 👁 شوهد في فيديو
- **ماذا / what:** Quadratic curve whose control y increases when a word hangs; spring settle
- **أرقام / params:** sag 30-60px
- **الدليل / proof:** `style:pm-gdgtify-287ddf`

#### SHAPE-103 · تحول شكل مع مقابض التصميم · Shape morph with design handles · 👁 شوهد في فيديو
- **ماذا / what:** interpolate path squircle -> wavy flower (n-petal sine radius); overlay bounding box, bezier handle dots and a lime dimension tag; concentric gradient rings behind
- **أرقام / params:** r = R(1 + 0.12 sin(8θ+t)), 600 ms morph
- **الدليل / proof:** `style:pm-ghinaiya-nirmal-5d8fec`

#### SHAPE-104 · هيكل يتجمع من قطعه · Skeleton assemble along path · 👁 شوهد في فيديو
- **ماذا / what:** bone pieces start scattered, travel along a dotted arc and snap into a skeleton silhouette with slight overshoot
- **أرقام / params:** stagger 40 ms, 1.2 s total
- **الدليل / proof:** `style:pm-gigabit-million-16b3a0`

#### SHAPE-105 · أشرطة متلوية في الخلفية · Background ribbon loops · 👁 شوهد في فيديو
- **ماذا / what:** 2-3 SVG cubic paths stroke-width ~6% frame, linear gradient strokes, round caps; animate control points slowly and dashoffset to draw; lower opacity to 0.35 when text on top
- **أرقام / params:** gradients blue->violet, pink->orange
- **الدليل / proof:** `style:pm-gonzalomacagno-2de1a9`

#### SHAPE-106 · نص في شكل متحول · Text in morphing blob · 👁 شوهد في فيديو
- **ماذا / what:** square path morphs to blob with outline over halftone dots
- **أرقام / params:** 600ms
- **الدليل / proof:** `style:pm-hanifproduktif-54bdee`

#### SHAPE-107 · شريط قوس قزح متموج · Ribbon sine wave · 👁 شوهد في فيديو
- **ماذا / what:** Stacked colour bands y=sin(x*k+t)
- **أرقام / params:** 7 bands
- **الدليل / proof:** `style:pm-hoyoyoda-3a5c08`

#### SHAPE-108 · قطار مقابل يمر سريعًا · Passing oncoming train · 👁 شوهد في فيديو
- **ماذا / what:** Long cream/red carriage strip with window blocks slides across at high speed with motion blur, occluding the landscape; rain streaks on glass as diagonal lines
- **أرقام / params:** ~1.5 s, blur 30 px
- **الدليل / proof:** `style:pm-itsolelehmann-e47532`

#### SHAPE-109 · تحول المضلعات · Polygon morph · 👁 شوهد في فيديو
- **ماذا / what:** interpolate vertex arrays triangle->hexagon
- **أرقام / params:** outElastic
- **الدليل / proof:** `style:pm-itsuki-dev-10942d`

#### SHAPE-110 · موجة في شبكة أشكال · Shape grid wave · 👁 شوهد في فيديو
- **ماذا / what:** Grid of rounded squares; a diagonal wave front rotates each cell 45-90 deg and morphs square->circle (border-radius) while switching fill/outline
- **أرقام / params:** cell 30 px, gap 40 px, delay = (x+y)*25 ms
- **الدليل / proof:** `style:pm-jasonzhou1993-8595e0`

#### SHAPE-111 · تحول الجزيرة الديناميكية · Island morph · 👁 شوهد في فيديو
- **ماذا / what:** animate width/height/radius of one container between states with spring
- **أرقام / params:** stiffness 200 damping 22
- **الدليل / proof:** `style:pm-jazzen-chen-4542ae`

#### SHAPE-112 · حقل أشكال متحولة · Pattern morph field · 👁 شوهد في فيديو
- **ماذا / what:** grid glyphs cross→blob→triangle by column phase
- **الدليل / proof:** `style:pm-johnsavage-ai-b091c0`

#### SHAPE-113 · غرفة مصباح بزجاج معيّني وعدسة فرينل · Diamond-pane lamp room & Fresnel flare · 👁 شوهد في فيديو
- **ماذا / what:** lattice of diagonal lines over a glowing cylinder; lens as concentric ellipses; ignition = 0->1 brightness over ~400 ms with bloom spike
- **أرقام / params:** lattice 40px cells, glow blur 30-60px
- **الدليل / proof:** `style:pm-kamstudiolabs-0b0824`

#### SHAPE-114 · حلقات متحدة المركز بفجوات دوّارة · Rotating gapped concentric rings · 👁 شوهد في فيديو
- **ماذا / what:** draw N arcs from gapStart+gap to gapStart+2π; gapStart_i += ω_i·dt with alternating sign; spacing equal
- **أرقام / params:** N=12, stroke 6-8px, spacing ~14px, ω 0.3-1.2 rad/s
- **الدليل / proof:** `style:pm-kantamk-61f410`

#### SHAPE-115 · تحوّل شكل داخل صندوق أداة تصميم · Design-tool gizmo morph · 👁 شوهد في فيديو
- **ماذا / what:** Morph an SVG path between shapes (circle, scallop, star) while a thin bounding box with square handles rotates around it; show live readout 'ROT 340.9°' and shape label in mono
- **أرقام / params:** morph 600ms; box stroke 1px #aaa
- **الدليل / proof:** `style:pm-leadnotifi-e83f94`

#### SHAPE-116 · شبكة بلاطات باوهاوس · Bauhaus tile flip grid · 👁 شوهد في فيديو
- **ماذا / what:** N×M grid; each cell draws one of {quarter circle, triangle, bar, circle} in 4-colour palette and swaps glyph on staggered rotation
- **أرقام / params:** 8x5 cells, stagger diagonal 30 ms, swap every 250 ms
- **الدليل / proof:** `style:pm-leonkohli-6dc01b`

#### SHAPE-117 · أقواس متحدة المركز تدور وتنهار · Concentric arc spin collapse · 👁 شوهد في فيديو
- **ماذا / what:** Several partial arcs at decreasing radii rotate at different speeds and scale to the centre dot
- **أرقام / params:** 6 rings, speeds 90-360°/s, collapse 500 ms easeIn
- **الدليل / proof:** `style:pm-leonkohli-6dc01b`

#### SHAPE-118 · مروحة صور خلف البطاقة · Fan-out photo stack · 👁 شوهد في فيديو
- **ماذا / what:** Several images behind a hero card rotate outward around a common pivot to form a fan
- **أرقام / params:** 5-8 images, ±12-25°, 500 ms easeOutBack
- **الدليل / proof:** `style:pm-lester-tyy-f897f7`

#### SHAPE-119 · تحول شكل فائق الإهليجية مع حلقات صدى · Superellipse shape morph with echo rings · 👁 شوهد في فيديو
- **ماذا / what:** Morph through |x|^n+|y|^n=1 with animated n (2 -> 4.2), surrounded by offset contour rings that lag behind, then to 3D cube and star
- **أرقام / params:** n tween 400 ms, 5-7 rings at 12 px offsets, ring lag 60 ms each
- **الدليل / proof:** `style:pm-levabashidze-2d713a`

#### SHAPE-120 · نقش بلاطات تروشيه · Truchet tile pattern · 👁 شوهد في فيديو
- **ماذا / what:** Tile grid with quarter-circle arcs randomly rotated; animate rotations in a diagonal wave and recolour a subset in accent
- **أرقام / params:** tile 60 px, stroke 14 px, wave delay 20 ms per tile
- **الدليل / proof:** `style:pm-levabashidze-2d713a`

#### SHAPE-121 · خط نبض القلب · ECG heartbeat line · 👁 شوهد في فيديو
- **ماذا / what:** polyline spike traveling along horizon; flatline at end
- **الدليل / proof:** `style:pm-loicrambo-ad6830`

#### SHAPE-122 · تحول أشكال باوهاوس · Bauhaus shape morph · 👁 شوهد في فيديو
- **ماذا / what:** red square → yellow pentagon → triangle with point interpolation
- **أرقام / params:** 400ms
- **الدليل / proof:** `style:pm-lukasersil-0ed38e`

#### SHAPE-123 · شبكة مربعات تدور كموجة · Wave-rotating square grid · 👁 شوهد في فيديو
- **ماذا / what:** rotate each square by f(distance - t) 
- **أرقام / params:** phase 0.1/cell
- **الدليل / proof:** `style:pm-m1n9-k7-ff9ab9`

#### SHAPE-124 · أشعة شمسية دائرية · Radial sunburst rays · 👁 شوهد في فيديو
- **ماذا / what:** conic-gradient repeating wedges in dark crimson on black, slow rotation behind title
- **أرقام / params:** 24-36 rays, 3-6 deg/s
- **الدليل / proof:** `style:pm-majin-appsheet-2d3c1a`

#### SHAPE-125 · حلقة اكتشاف · Discovery ring burst · 👁 شوهد في فيديو
- **ماذا / what:** radial yellow dashes burst outward around found object
- **أرقام / params:** 500ms
- **الدليل / proof:** `style:pm-mandelduck-95fd08`

#### SHAPE-126 · تحويل أيقونة من نقاط · Dot-matrix icon morph · 👁 شوهد في فيديو
- **ماذا / what:** sample target shape into N dots, tween each dot position with stagger
- **أرقام / params:** ~400 dots, 0.8 s, ease inOutCubic
- **الدليل / proof:** `style:pm-manuelogomigo-f33ca9`

#### SHAPE-127 · منحنيات ليساجو · Lissajous neon curves · 👁 شوهد في فيديو
- **ماذا / what:** (sin 3t, sin 2t, sin 5t) stroke with glow
- **الدليل / proof:** `style:pm-math-files-39c9d0`

#### SHAPE-128 · كسيرية جوليا · Julia fractal shader · 👁 شوهد في فيديو
- **ماذا / what:** GLSL iterate z^2+c, palette purple-orange
- **الدليل / proof:** `style:pm-math-files-39c9d0`

#### SHAPE-129 · تحوّل الشعار إلى بؤبؤ عين · Logo-to-iris morph · 👁 شوهد في فيديو
- **ماذا / what:** keep the logo ring of 8 rounded pentagons, scale it into an iris disc with radial ray gradient and add an almond eye outline with lash ticks around it
- **أرقام / params:** ~600 ms, iris blur glow 30-40 px, colour #5cc8ff
- **الدليل / proof:** `style:pm-micheleharmonic-77628e`

#### SHAPE-130 · حلقة نقاط تتسع مع خطوط شعاعية · Expanding dot ring with radial lines · 👁 شوهد في فيديو
- **ماذا / what:** duplicate logo dots around a larger circle (8 -> 24), thin violet lines radiate from behind towards the frame edges
- **أرقام / params:** ring radius 40% width, lines 1.5 px #8a6cff
- **الدليل / proof:** `style:pm-micheleharmonic-77628e`

#### SHAPE-131 · انفتاح العين · Eye opening · 👁 شوهد في فيديو
- **ماذا / what:** almond path height 0→full with iris scale, concentric outlines
- **أرقام / params:** 800ms ease-out
- **الدليل / proof:** `style:pm-monokern-ade5b6`

#### SHAPE-132 · كاليدوسكوب · Kaleidoscope shader · 👁 شوهد في فيديو
- **ماذا / what:** polar fold n=6-12 of rotating texture
- **الدليل / proof:** `style:pm-monokern-ade5b6`

#### SHAPE-133 · تحول شكل مع أثر ضبابي · Shape morph with blur trail · 👁 شوهد في فيديو
- **ماذا / what:** Interpolate star polygon points (flubber-style) while rotating, with motion-blur echo; dotted orbit circle and orbiting accent dots
- **أرقام / params:** morph 600 ms easeInOutCubic, 3 orbit dots
- **الدليل / proof:** `style:pm-motiondsgnr-9dcfa6`

#### SHAPE-134 · خطوط موجية توليدية · Ridge-line generative waves · 👁 شوهد في فيديو
- **ماذا / what:** Stack of 40-60 horizontal polylines displaced by noise near centre (Joy Division look), with coloured bars sliding across
- **أرقام / params:** noise amplitude ramp 0->60 px, gradient red->blue by row
- **الدليل / proof:** `style:pm-motiondsgnr-9dcfa6`

#### SHAPE-135 · شبكة نقاط موجية · Dot-grid wave · 👁 شوهد في فيديو
- **ماذا / what:** grid dots coloured where sin(x*k - t) > threshold
- **أرقام / params:** grid 30x20
- **الدليل / proof:** `style:pm-mrtanviir-132457`

#### SHAPE-136 · شبكة أشكال تتحول بتأخير المسافة · Distance-delayed shape grid morph · 👁 شوهد في فيديو
- **ماذا / what:** 6x10 grid; each cell morphs circle->4-point star with ease(t-0.3*d) where d is distance from origin
- **أرقام / params:** 60 shapes, 600 ms each
- **الدليل / proof:** `style:pm-ndhabarde11-f155b4`

#### SHAPE-137 · إطار مطاطي يتعرّج تحت الضغط · Rubber frame strain · 👁 شوهد في فيديو
- **ماذا / what:** draw the border as an SVG path with ~40 points; displace points outward with noise/sine where the content touches, amplitude rising as the word grows
- **أرقام / params:** amp 0→12 px, freq 3-4 waves per edge
- **الدليل / proof:** `style:pm-pankajkumar-dev-0bee87`

#### SHAPE-138 · رقصة أشكال باوهاوس الأساسية · Bauhaus primitive choreography · 👁 شوهد في فيديو
- **ماذا / what:** circle, square, triangle, bar enter on diagonals with back.out overshoot and small rotation, layered on primary colour fields
- **أرقام / params:** red #d6341f, yellow #e9c634, blue #2135bc, stagger 120 ms
- **الدليل / proof:** `style:pm-pankajkumar-dev-0bee87`

#### SHAPE-139 · بطاقة شفافة تعبر قطرياً · Translucent diagonal promo card sweep · 👁 شوهد في فيديو
- **ماذا / what:** large pink frosted card rotated ~-12° with big text slides diagonally across the frame on top of the scene, partially out of frame
- **أرقام / params:** ~700 ms, opacity 0.7, backdrop blur 8 px
- **الدليل / proof:** `style:pm-paulo-kombucha-96431c`

#### SHAPE-140 · أثر نقطي للرمي · Dotted throw trail · 👁 شوهد في فيديو
- **ماذا / what:** bezier arc, dots every 8 px fading
- **الدليل / proof:** `style:pm-pluginplay-3d4006`

#### SHAPE-141 · شبكة بلاطات باوهاوس تتبدل · Bauhaus tile state-flip grid · 👁 شوهد في فيديو
- **ماذا / what:** 16x9 grid; each cell picks from circle, ring, half/quarter circle, triangle with palette of 5 colours; cells rotate/flip to new state with stagger by distance from centre
- **أرقام / params:** stagger 15-25 ms, flip 200 ms
- **الدليل / proof:** `style:pm-prasenx-8d9323`

#### SHAPE-142 · كرات لزجة تندمج · Metaball goo · 👁 شوهد في فيديو
- **ماذا / what:** SVG feGaussianBlur 10 + feColorMatrix alpha 18 -7 on circles
- **الدليل / proof:** `style:pm-raphaelaubryy-4b137e`

#### SHAPE-143 · موجات تردد · Frequency wave stack · 👁 شوهد في فيديو
- **ماذا / what:** 3 offset sine paths, increase frequency over time
- **الدليل / proof:** `style:pm-reflex-cloud-72ffe5`

#### SHAPE-144 · تشابك ليساجو · Lissajous complexity tangle · 👁 شوهد في فيديو
- **ماذا / what:** x=A sin(a t+δ), y=B sin(b t); draw 20 copies with slowly drifting δ and ratios 3:2, 5:4; additive low alpha
- **أرقام / params:** δ drift 0.2 rad/s
- **الدليل / proof:** `style:pm-rneayan-ea6129`

#### SHAPE-145 · تحويل أشكال بنابض · Spring shape morph · 👁 شوهد في فيديو
- **ماذا / what:** Interpolate resampled polygon points circle→square→5-point star with spring easing; add ring of small stars rotating around
- **أرقام / params:** 200 pts, stiffness 180, damping 14
- **الدليل / proof:** `style:pm-roundtablespace-d3a1be`

#### SHAPE-146 · نمط ترَشيه مع موجة تلوين · Truchet wave recolour · 👁 شوهد في فيديو
- **ماذا / what:** Grid of quarter-arc Truchet tiles; a radial wave front rotates tiles 90° and tints them red with falloff
- **أرقام / params:** tile 80px, stroke 18px, wave speed 600px/s
- **الدليل / proof:** `style:pm-roundtablespace-d3a1be`

#### SHAPE-147 · بوابة دوامية · Swirl portal · 👁 شوهد في فيديو
- **ماذا / what:** ring torus glow + polar-twisted noise disc shader
- **الدليل / proof:** `style:pm-ryzoft-4f85bd`

#### SHAPE-148 · مربعات متداخلة · Nested rotating squares · 👁 شوهد في فيديو
- **ماذا / what:** 8 squares rotate delay 50 ms each
- **الدليل / proof:** `style:pm-safarkhanshuvo-ffd52d`

#### SHAPE-149 · شاشة مقسومة واستعارة الكسوف · Split-screen eclipse metaphor · 👁 شوهد في فيديو
- **ماذا / what:** half cream / half black; outline circle on light side, filled red dot on dark side slide toward each other and overlap into an eclipse
- **أرقام / params:** ~1.5 s ease-in-out
- **الدليل / proof:** `style:pm-samaote-5e2fc2`

#### SHAPE-150 · شبكة بلاطات باوهاوس · Bauhaus modular tile grid · 👁 شوهد في فيديو
- **ماذا / what:** 6x3 cells of circle/half/quarter shapes; each 200ms swaps shape and colour from 3-colour set
- **الدليل / proof:** `style:pm-samuel-spitz-974923`

#### SHAPE-151 · مدار حول جسم · Orbit ellipse accent · 👁 شوهد في فيديو
- **ماذا / what:** thin red ellipse stroke rotating around object, tilted 20°
- **الدليل / proof:** `style:pm-samuel-spitz-974923`

#### SHAPE-152 · انفجار أشعة ملونة · Radial ray burst · 👁 شوهد في فيديو
- **ماذا / what:** N line segments at random angles shoot outward from a ring with varied length and colour from palette, ease-out; outer arc rotates
- **أرقام / params:** 40-60 rays; 600ms expoOut
- **الدليل / proof:** `style:pm-shinskinakamoto-20190b`

#### SHAPE-153 · تحول مربع إلى دائرة مع أقمار · Square-to-circle morph with satellites · 👁 شوهد في فيديو
- **ماذا / what:** Animate border-radius 0->50% with rotation while three small dots orbit on a thin ring; background polka grid pulses
- **أرقام / params:** morph 500ms; orbit 1 rev/s
- **الدليل / proof:** `style:pm-shinskinakamoto-20190b`

#### SHAPE-154 · حقل أشكال عائمة · Blob background field · 👁 شوهد في فيديو
- **ماذا / what:** large rounded rects/circles drifting with blur
- **أرقام / params:** 5-8 shapes
- **الدليل / proof:** `style:pm-slvdev-64c45a`

#### SHAPE-155 · بلاطات تروشيه المتموجة · Truchet wave tiles · 👁 شوهد في فيديو
- **ماذا / what:** grid of quarter-arc tiles; rotate 90deg with delay = column*40ms; tint wavefront red
- **أرقام / params:** tile 80px, stroke 14px
- **الدليل / proof:** `style:pm-stephanlivera-df17a2`

#### SHAPE-156 · نجمة تنفجر مع توابع · Star pop with orbiters · 👁 شوهد في فيديو
- **ماذا / what:** star scale outBack, small stars placed on circle and rotating
- **الدليل / proof:** `style:pm-stephanlivera-df17a2`

#### SHAPE-157 · موجة شبكة نقاط · Distance-delay dot wave · 👁 شوهد في فيديو
- **ماذا / what:** grid of squircles; scale = sin(t - dist*k); colour by ring
- **الدليل / proof:** `style:pm-sudo-kiran-49176d`

#### SHAPE-158 · كتلة متدرجة خلف نص · Gradient blob behind knockout text · 👁 شوهد في فيديو
- **ماذا / what:** SVG blob noise morph, lime→blue gradient, text multiply
- **الدليل / proof:** `style:pm-sudo-kiran-49176d`

#### SHAPE-159 · ملء بشظايا · Shard fly-in fill · 👁 شوهد في فيديو
- **ماذا / what:** each triangle starts off-screen rotated, eases into slot
- **أرقام / params:** 600 ms ease-out
- **الدليل / proof:** `style:pm-tdinh-me-815acb`

#### SHAPE-160 · موجة بلاطات أرباع الدوائر · Quarter-circle tile wave · 👁 شوهد في فيديو
- **ماذا / what:** grid of square cells each holding a quarter circle in one of 3-4 colours; rotate each cell 90° with delay = distance from centre × k
- **أرقام / params:** cell 80-100 px; k 30 ms/cell; rotation 300 ms back.out
- **الدليل / proof:** `style:pm-tequilafunks-97f6c9`

#### SHAPE-161 · انفجار خطوط شعاعي افتتاحي · Radial line burst opener · 👁 شوهد في فيديو
- **ماذا / what:** Single horizontal line + faint circle on black; then 36-48 rays scale out from centre with varying lengths and widths, sparks drift; cut on beat
- **أرقام / params:** burst 400 ms easeOutExpo
- **الدليل / proof:** `style:pm-teslachartz-c58b32`

#### SHAPE-162 · تموج شعاعي في شبكة أشكال · Shape grid radial ripple · 👁 شوهد في فيديو
- **ماذا / what:** 9x5 grid of cells with crosshair corners; each cell shows one primitive (square, plus, triangle, ring) in red/blue/black; a ripple from the centre cell swaps each cell's shape/colour with scale pop, d
- **كيف / how:** 9x5 grid of cells with crosshair corners; each cell shows one primitive (square, plus, triangle, ring) in red/blue/black; a ripple from the centre cell swaps each cell's shape/colour with scale pop, delay = distance * k
- **أرقام / params:** k ~40 ms per cell, pop 200 ms
- **الدليل / proof:** `style:pm-teslachartz-c58b32`

#### SHAPE-163 · كومة بطاقات تتكاثر · Card stack fan counter · 👁 شوهد في فيديو
- **ماذا / what:** duplicate card with rotate/offset per item and 'n items' label
- **الدليل / proof:** `style:pm-thayto-dev-44b911`

#### SHAPE-164 · قناع القضمة · Bite mask · 👁 شوهد في فيديو
- **ماذا / what:** Remove a scalloped circle-union shape from an object edge (logo cookie, phone tab bar) to show 'eaten'; animate mask radius 0->r with a few crumb particles
- **أرقام / params:** 3 overlapping circles; 200ms; 4-6 crumbs
- **الدليل / proof:** `style:pm-thilina-a-891c09`

#### SHAPE-165 · مسار دائري بطائرة ورقية · Orbit path with paper plane · 👁 شوهد في فيديو
- **ماذا / what:** dashed ellipse around headline; small plane icon follows the path (motion path)
- **أرقام / params:** dash 2/6, 1.5 s per loop
- **الدليل / proof:** `style:pm-thismacapital-dfba20`

#### SHAPE-166 · تحوّل شكل مع صدى ملون · Shape morph with echo · 👁 شوهد في فيديو
- **ماذا / what:** Interpolate path points circle→star (flubber), draw two lagged coloured stroke copies
- **أرقام / params:** ~800 ms
- **الدليل / proof:** `style:pm-tolgayhickiran-e90799`

#### SHAPE-167 · تحول الزر إلى نافذة · Button-to-window morph · 👁 شوهد في فيديو
- **ماذا / what:** animate width/height/border-radius of pill to 60% square card, image fades in inside
- **أرقام / params:** ~800 ms easeInOut
- **الدليل / proof:** `style:pm-twoclipping-221cab`

#### SHAPE-168 · مؤشر مطاطي بحافتين · Two-edge stretchy indicator · 👁 شوهد في فيديو
- **ماذا / what:** left and right edges of tab indicator/toggle knob follow separate springs (leading edge stiffer) so the shape stretches in travel and settles
- **أرقام / params:** stiffness ratio ~1.6:1
- **الدليل / proof:** `style:pm-twoclipping-5cba86`

#### SHAPE-169 · تمطيط الدائرة إلى كبسولة · Circle to pill stretch · 👁 شوهد في فيديو
- **ماذا / what:** animate width with fixed radius; squash on settle
- **الدليل / proof:** `style:pm-ultimaxbt-bbebf5`

#### SHAPE-170 · نقطة تتحول إلى نظام · Dot→system morph · 👁 شوهد في فيديو
- **ماذا / what:** Start with single accent dot on empty frame, scale rings out from it and scatter satellite dots with stagger 50 ms
- **أرقام / params:** ~1 s
- **الدليل / proof:** `style:pm-xelandre-363f00`

#### SHAPE-171 · نفق مربعات حلزوني · Spiral square tunnel · 👁 شوهد في فيديو
- **ماذا / what:** nested squares scale 0.9 rotate 8° each, alternating colours, rotate loop
- **الدليل / proof:** `style:pm-zheke-38deff`

#### SHAPE-172 · تغيير لون الكلمة داخل الكورة فقط · Clip-path colour flip over a moving lens · 👁 شوهد في فيديو
- **ماذا / what:** render word row twice: dark copy, and white copy clipped with clip-path: circle(r at orbX orbY); translate row horizontally so each word passes the orb
- **أرقام / params:** orb r ~70px, row speed ~1 word/0.8 s
- **الدليل / proof:** `style:product`

#### SHAPE-173 · اختيار المنحنيات وسرعة ثابتة على المسار · Spline choice and constant-speed paths · 📄 موصوف
- **ماذا / what:** Pick curve families for cursor paths, camera rails and object routes: Catmull-Rom to pass through waypoints, Hermite with known tangents, Bezier for handle authoring; target C1 continuity and use an arc-length table so speed is constant.
- **كيف / how:** Plain JS/Python: sample curve, build cumulative length table, map distance->t; separate authoring points from baked samples.
- **أرقام / params:** C0 position, C1 tangent, C2 curvature; never one high-degree polynomial through many points
- **الدليل / proof:** `kosif-atlas/skills/2199-lvtd-skills/8088-game-smooth-curves-and-motion`

#### SHAPE-174 · S07 مرح هندسي · S07 Playful geometric · 📄 موصوف
- **ماذا / what:** Limited bold palette, circles, cards and icons; small bounces, shape swaps, varied rhythm. Lively from simple assets; can be wrong for serious topics and over-bouncing distracts.
- **كيف / how:** SVG primitives, overshoot easings, staggered entrances; KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg)
- **أرقام / params:** cost low-medium; MG-008 MG-029 MG-061 MG-081 MG-083 MG-108 MG-115
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### SHAPE-175 · MG-112/115 حلقات دوران بنسب صحيحة · MG-112/115 Integer-ratio rotation loops · 📄 موصوف
- **ماذا / what:** Dots orbit a centre away from the text (MG-112); two arcs rotate at related speeds around one centre (MG-115).
- **كيف / how:** MG-112: exactly one turn in 6 s, linear, evenly spaced angles. MG-115: arc A one turn and arc B two turns per 6 s around a shared centre - integer turn ratios guarantee no jump; never export the first frame twice at the seam.
- **أرقام / params:** 6 s; ratio 1:2
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-loops-backgrounds.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### SHAPE-176 · MG-116/117 بلاطات تنقلب وشريط صور لا ينتهي · MG-116/117 Tile flips and endless strip · 📄 موصوف
- **ماذا / what:** A tile grid flips row by row to a second colour and back (MG-116); a row of images scrolls with its end meeting its start (MG-117).
- **كيف / how:** MG-116: 0-4 flip, 4-8 return; scaleX or 2.5D rotate with row delay, few flips, no harsh flashing contrast. MG-117: move exactly one repeat-unit width (including gaps) in 10 s using two identical copies and linear motion - miscounted gaps cause a jump.
- **أرقام / params:** 8 s / 10 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-loops-backgrounds.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### SHAPE-177 · نمذجة حقول المسافة · SDF field modeling · 📄 موصوف
- **ماذا / what:** Compose primitive signed distance fields with transforms and booleans for shapes, morphs and raymarching.
- **كيف / how:** Inverse-transform the point; union=min, intersect=max, smooth-min for blends; debug via slices/isolines.
- **الدليل / proof:** `kosif-atlas/skills/2199-lvtd-skills/8087-game-sdf-and-field-modeling/SKILL.md` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### SHAPE-178 · أيقونة بأقل الخطوط · Minimal icon via closure · 📄 موصوف
- **ماذا / what:** Imply forms with gaps, aligned terminations and negative space; test legibility at 8-12px.
- **كيف / how:** SVG strokes with small breaks; draw-on works especially well because perception completes the form early.
- **أرقام / params:** test at 8-12px
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3812-closure-implied-shapes` · `kosif-atlas/skills/1503-universal-design-principles/3760-iconic-representation`

#### SHAPE-179 · فلتر اللزوجة · SVG goo filter · 📄 موصوف
- **ماذا / what:** Blobs merge like liquid: blur then sharpen alpha with a color matrix.
- **كيف / how:** feGaussianBlur stdDeviation ~10 + feColorMatrix alpha row '0 0 0 18 -7'.
- **أرقام / params:** std 10; 18 -7
- **الدليل / proof:** `kosif-atlas/skills/100-ui-motion/209-kinetic-inflated-hero` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`

#### SHAPE-180 · أشكال بدوال المسافة · Signed distance field shapes · 📄 موصوف
- **ماذا / what:** Represent shapes as distance functions for smooth unions, morphs, outlines and glows.
- **كيف / how:** GLSL or numpy: circle length(p)-r, box, smooth-min union k; morph by mixing two SDFs; glow = exp(-d*k).
- **أرقام / params:** smin k 0.1-0.3
- **الدليل / proof:** `kosif-atlas/skills/2199-lvtd-skills/8087-game-sdf-and-field-modeling` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`

#### SHAPE-181 · شبكة أيقونات 24px · 24px/2px icon grid · 📄 موصوف
- **ماذا / what:** Unified 24px grid, 2px stroke, round caps, square viewBox, no text, <4KB file.
- **كيف / how:** primitive SVG with seeded randomness
- **أرقام / params:** test at 16/24/48/192 px
- **الدليل / proof:** `100-superskills/skills/svg-illustration-icons/SKILL.md:21`

#### SHAPE-182 · نظام الوحدة والشبكة · Base-unit grid system · 📄 موصوف
- **ماذا / what:** All sizes multiples of a base unit on a column grid; final frames exactly on grid.
- **أرقام / params:** unit 24 px; 8 or 12 columns
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:15` · `kosif-tool/playbooks/shapes.md:29`

#### SHAPE-183 · سلالم الأشكال والأقطار · Primitive and radius/stroke scales · 📄 موصوف
- **ماذا / what:** Max three primitives, two colours + background, radius and stroke scales, ≥30% negative space.
- **أرقام / params:** radii 0/8/24/50%; strokes 2/4/8; negative space ≥ 30%
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:16-18`

#### SHAPE-184 · رقصة الشبكة · Grid choreography wave · 📄 موصوف
- **ماذا / what:** 4×4 grid rotates 90° in diagonal wave.
- **أرقام / params:** 40 ms offset per cell; 400 ms each
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:47`

#### SHAPE-185 · التحول عبر حالات الواجهة · Morph through UI states · 📄 موصوف
- **ماذا / what:** Button→toggle→card→full screen.
- **أرقام / params:** 600 ms per step; 900 ms holds
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:49`

#### SHAPE-186 · معادلة الزوايا المتداخلة · Nested radius formula · 📄 موصوف
- **ماذا / what:** inner radius = outer - gap when gap<32 px and result>2.
- **أرقام / params:** 16px outer, 8px gap -> 8px
- **الدليل / proof:** `kosif-one/vendor/ai-design-skills/skills/landing-page-design/SKILL.md:225`

#### SHAPE-187 · نقرة وتحول لعلامة صح · Tap ripple + circle-to-check morph · 💡 فكرة
- **ماذا / what:** Tap ripple triggers success; circle morphs into checkmark.
- **كيف / how:** SVG path morph (flubber-like) + ripple circle scale/fade.
- **الدليل / proof:** `style:pm-cansincengiz-me-cf68dd`

#### SHAPE-188 · تجمع إلى شعار · Converge to monogram tile · 💡 فكرة
- **ماذا / what:** Lanes/bars/line converge into a square tile that rotates 90° into monogram.
- **كيف / how:** Transform interpolation.
- **أرقام / params:** 90°
- **الدليل / proof:** `style:pm-danilowm-d3720d`

#### SHAPE-189 · تجمع الصلصال · Metaball clay assembly · 💡 فكرة
- **ماذا / what:** Blobs roll in and merge via metaball threshold.
- **كيف / how:** Canvas field sum + threshold (or SVG goo filter).
- **أرقام / params:** 6 blobs
- **الدليل / proof:** `style:pm-davidshulmanfl-371638`

#### SHAPE-190 · انكماش لنقطة · Converge-to-dot outro · 💡 فكرة
- **ماذا / what:** All elements collapse to a dot which expands to logo.
- **أرقام / params:** hold final 2 s
- **الدليل / proof:** `style:pm-itisrazak-3ad902`

#### SHAPE-191 · نقطة لخط لكلمة · Dot-line-word cold open · 💡 فكرة
- **ماذا / what:** A dot stretches to a line then snaps into a word letter by letter with drum hit per letter.
- **الدليل / proof:** `style:pm-jasonzhou1993-8595e0`

#### SHAPE-192 · نفق الخطوط · Outline tunnel speed ramp · 💡 فكرة
- **ماذا / what:** Mark multiplies into tunnel of outlines with ticking counter.
- **كيف / how:** Repeated scaled outlines.
- **الدليل / proof:** `style:pm-jasonzhou1993-8595e0`

#### SHAPE-193 · كل شيء من المركز · Centre-origin geometry · 💡 فكرة
- **ماذا / what:** All transforms around frame centre; elements enter from centre only.
- **كيف / how:** transform-origin 960px 540px.
- **أرقام / params:** (960,540)
- **الدليل / proof:** `style:pm-marouanegazouzi-6071d5`

#### SHAPE-194 · ظرف يتحول لشارة · Envelope to badge morph · 💡 فكرة
- **ماذا / what:** Sent envelope streaks off and becomes a notification badge.
- **الدليل / proof:** `style:pm-melvynx-6cde6c`

#### SHAPE-195 · تماثل كاليدوسكوبي · Kaleidoscope wedge symmetry · 💡 فكرة
- **ماذا / what:** 6/8-fold symmetry mirrored from one wedge in shader.
- **كيف / how:** Fragment shader polar fold; wedge rotates.
- **أرقام / params:** 6 or 8 folds; wedge 10°/s
- **الدليل / proof:** `style:pm-monokern-ade5b6`

#### SHAPE-196 · التصاق مغناطيسي · Magnet snap spring · 💡 فكرة
- **ماذا / what:** Primitives snap into place with one overshoot.
- **كيف / how:** Remotion spring.
- **أرقام / params:** stiffness 220 damping 14; UI cubic-bezier(0.16,1,0.3,1) 400-600 ms
- **الدليل / proof:** `style:pm-quickdesignio-dd93d0`

#### SHAPE-197 · تموج شبكة نقاط · Dot-grid spring ripple · 💡 فكرة
- **ماذا / what:** Wave front through dot grid with spring overshoot.
- **أرقام / params:** stiffness 220 damping 12; 900 px/s
- **الدليل / proof:** `style:pm-reflex-cloud-72ffe5`
