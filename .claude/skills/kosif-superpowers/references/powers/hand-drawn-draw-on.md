# الرسم اليدوي والرسم الحي — Hand-drawn & draw-on

> فصل مُجمَّع آليًا من 191 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **190 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 190 powers deduplicated by name from 191 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 2 · 🟢 جاهز 13 · 📦 بأمر تثبيت 78 · 🔑 مفتاح/خدمة 3 · 👁 شوهد في فيديو 57 · 📄 موصوف 29 · 💡 فكرة 8

#### DRAW-01 · رسم خط الرحلة من اليمين · Journey line draw-on (RTL) · ✅ مُثبت هنا
- **ماذا / what:** A 2px progress line grows from the right edge; its colour stops encode state (grey future, violet current, teal done).
- **كيف / how:** ::before line, transform-origin: right center; keyframe scaleX 0->1 with opacity .2->1.
- **أرقام / params:** 680ms ease-cinematic, delay 160ms; gradient to left: border 0-38%, primary 38-64%, teal 64-100%; inset 10%
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:981` · `kosif-audit-pro/app/globals.css:1082`

#### DRAW-02 · ترتيب ظهور الرسام: فرشاة، نمو، صعود، نزول، يمين، يسار، تناثر · Painter reveal orders (sweep/grow/rise/down/left/right/sparkle) · ✅ مُثبت هنا
- **ماذا / what:** Sorts the changed pixels of each step the way a painter lays them: horizontal boustrophedon brush bands, growth outward from an origin, figures rising from their feet, scattered sparkle for details.
- **كيف / how:** Step(order=..., origin=(x,y)); reveal_order(idx, W, step, scale, seed) returns a permutation; studio/film play it pixel by pixel.
- **أرقام / params:** sweep band height round(7*scale) px, back-and-forth rows, jitter 26*scale; grow: distance to origin + jitter 9*scale; rise/down/left/right jitter 7*scale; sparkle = random
- **الدليل / proof:** `kosif-studio/render.py:846` · `kosif-studio/tests/test_studio.py:93`

#### DRAW-03 · رسم المسار تدريجياً · SVG path draw-on · 🟢 جاهز
- **ماذا / what:** A stroke traces itself like a pen for arrows, connectors, diagrams, checkmarks and logo outlines.
- **كيف / how:** Set stroke-dasharray and stroke-dashoffset to path.getTotalLength(), then tween offset to 0 (GSAP or WAAPI).
- **أرقام / params:** 0.7s power2.out typical; success checkmark 300-500ms ease-out; round linecaps
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/feedback-patterns.md`

#### DRAW-04 · رسم الخط السفلي بتبديل نقطة الأصل · Underline draw and swap-origin hover · 🟢 جاهز
- **ماذا / what:** Underlines grow from one side and leave from the other by swapping transform-origin; or a background-size gradient draws a hairline.
- **كيف / how:** ::after scaleX 0->1 with origin right->left on hover; or background-size 0% 1px -> 100% 1px.
- **أرقام / params:** 0.4s ease-out-expo; 1px line
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md`

#### DRAW-05 · رسم فوق لقطات مولدة · Draw-over film on generated bases · 🟢 جاهز
- **ماذا / what:** Generated clips provide motion; a hand-built JavaScript drawing layer is the actual picture, with every frame a pure function of time rendered frame-exactly in a headless browser; both 16:9 and 9:16 modes come from the same film.
- **كيف / how:** Extract base frames with ffmpeg, draw stylised strokes/fills in canvas per frame using time t, render with Playwright, mux original audio; contact-sheet every cell before delivery.
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/SKILL.md` · `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md`

#### DRAW-06 · رسم الخط تدريجيا · Line draw-on reveal · 🟢 جاهز
- **ماذا / what:** A time-series or route line that draws itself from start to end, often with a glowing head and an end label popping in.
- **كيف / how:** SVG: set stroke-dasharray = path length and animate stroke-dashoffset from length to 0 driven by seek(t); or recompute a partial polyline by cumulative distance (same idea as slicing a route by km). Ease with a cubic-bezier (0.645,0.045,0.355,1) over the reveal window, then fade in the end marker and value label.
- **أرقام / params:** dash length = getTotalLength(); bezier 0.645,0.045,0.355,1
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-explainer-architecture.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/SKILL.md`

#### DRAW-07 · منظر الوادي عند الغسق (متجه) · Valley dusk vector landscape · 🟢 جاهز
- **ماذا / what:** Layered-dune lavender dusk scene with crescent moon, stars, a sheep flock on the horizon and palm silhouettes, recreated as vector from a Canva render.
- **كيف / how:** SVG with three dune paths (gradients d1/d2/d3), palms #4e46a8, flock ellipses; good as a parallax layer set (each dune a layer).
- **أرقام / params:** sky #8f8ae0 -> #c9c3f5 -> #f1e9fb; 1200x600, xMinYMax slice
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/valley-dusk.svg` · `kosif-earth-ci-fork/docs/rebuild/DESIGN_SYSTEM.md`

#### DRAW-08 · رسم الخط بالقلم · Pen draw-on stroke (drawPath) · 🟢 جاهز
- **ماذا / what:** Any SVG path is drawn on like a pen via dash offset, with an optional arrow/head that pops in at the end.
- **كيف / how:** MOTION.drawPath(tl, path, at, dur, {ease, opacity, head, headOrigin}); uses getTotalLength().
- **أرقام / params:** ease power4.inOut default; head scale 0->1 0.35 s spring snappy starting 0.1 s before the end
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:237`

#### DRAW-09 · رسومات خطية (سيارة وساعة ومقياس) · Line-art icon drawings (car, clock, rail) · 🟢 جاهز
- **ماذا / what:** Minimal ivory line drawings used as idea metaphors over footage: a car outline with two wheels and moving road dashes, a 24-tick clock with a rotating gold hand, a vertical measurement rail with a sliding marker.
- **كيف / how:** SVG path car body (stroke 2.6, round joins) + wheel circles r 19; road = 6 gold dashes sliding −70 px; clock ring r 150 with 24 ticks (every 6th longer and 3 px) and hand rotating 360° in 1 s; rail 460 px with 18 ticks (every 3rd longer).
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:58` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:198` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:222`

#### DRAW-10 · رسم يتكون · Studio vector renderer + draw-on · 🟢 جاهز
- **ماذا / what:** Program-of-steps vector picture on 1200x800 sheet revealed pixel by pixel (sweep/grow/rise/sparkle).
- **كيف / how:** film.py drawing SCENE --speed slow|normal|fast
- **أرقام / params:** speeds 5.0/1.8/0.55
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/render.py` · `100-superskills/skills/kosif-montage-motion/scripts/film.py:28`

#### DRAW-11 · رسم الخط بالقلم مع رأس سهم · Pen draw-on stroke with landing arrowhead · 🟢 جاهز
- **ماذا / what:** Any SVG path is drawn like a pen by animating its dash offset; an optional head (arrow, dot) pops in at the end with a spring.
- **كيف / how:** MOTION.drawPath(tl, pathEl, at, dur, {head, headOrigin, ease, opacity}).
- **أرقام / params:** dasharray=len; ease power4.inOut; head spring snappy 0.35 s at end-0.1 s
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:237`

#### DRAW-12 · نهر يرسم نفسه · River ribbon revealed along a curve · 🟢 جاهز
- **ماذا / what:** A flattened tube along a curve whose draw range grows so a river advances down its valley.
- **كيف / how:** makeRibbon(curve, {segments, radius, radial}); reveal with geometry.setDrawRange.
- **أرقام / params:** segments 220, radius 11, radial 10
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:255`

#### DRAW-13 · ترتيب الرسام في الكشف · Painter reveal orders · 🟢 جاهز
- **ماذا / what:** Each step's changed pixels are laid down like a painter: brush sweeps back and forth, grow from an origin, rise from the feet, fall, left/right, or sparkle last.
- **كيف / how:** Step(..., order='sweep'|'grow'|'rise'|'down'|'left'|'right'|'sparkle', origin=(x,y)); render.reveal_order().
- **أرقام / params:** sweep band 7*scale px; jitter 7-26*scale
- **الدليل / proof:** `kosif-one/tools/kosif-studio/render.py:846`

#### DRAW-14 · رسم الرابط مع رأس السهم · SVG edge draw-on with arrowhead · 🟢 جاهز
- **ماذا / what:** stroke-dashoffset from length to 0; arrowhead appears at end.
- **كيف / how:** Remotion Edge: strokeDasharray=len, strokeDashoffset=len*(1-p), markerEnd when p>0.95; html-canvas: pathLength='1', dashoffset = 1 - KOSIF.prog(t,t0,t1,Ease.inOutCubic).
- **أرقام / params:** 900–1200 px/s ease-in-out cubic; arrowhead in last 80 ms; stroke #9fb0cc 4 px
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:28` · `kosif-tool/playbooks/diagrams.md:58-67`

#### DRAW-15 · يد مثبتة على رأس القلم · Hand overlay pinned to pen tip · 🟢 جاهز
- **ماذا / what:** Hand image follows path point, lags 1 frame, rotates with stroke; removed during holds.
- **كيف / how:** path.getPointAtLength(p × getTotalLength()); Remotion DrawnPath with tip circle r 5.
- **أرقام / params:** lag 1 frame; rotation ±5°
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:27` · `kosif-tool/playbooks/hand-drawn.md:56-71`

#### DRAW-16 · محرك فرشاة الحبر · Ink brush engine rendering · 📦 بأمر تثبيت
- **ماذا / what:** Vector paths rendered through a deterministic capsule-dab brush with edge bias, gaussian softness, tone layers and paper grain to look hand-inked.
- **كيف / how:** ink.js capsule dabs of width 2*bias along contours; JS separable gaussian blur (Chromium canvas blur silently no-ops at very small sigma); tone layers at several gray levels for dry-brush; paperGrain opacity; scene modules expose window.renderFrame(t) and are rendered by Playwright into frames then ffmpeg.
- **أرقام / params:** source blur sigma ~0.85px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9357-rotoscope/SKILL.md` · `kosif-atlas/skills/2414-animation/9357-rotoscope/reference/method.md` · `kosif-atlas/skills/2414-animation/9357-rotoscope/scripts/roto.js`

#### DRAW-17 · تتبع ورسم وقياس لقطات مرجعية · Rotoscope trace-measure-fit loop · 📦 بأمر تثبيت
- **ماذا / what:** Decode a reference animation into distinct drawings, trace each to vector paths, re-render, and measure against source (XOR vs codec noise floor, SSIM) to learn a drawn style.
- **كيف / how:** Dedup drawings by large-gray-step pixel count not mean diff; threshold at midpoint of ink/paper gray modes; supersample 4x before findContours; approxPolyDP; unsharp mask before trace; overrides JSON per drawing range (bias, blur, sharp, levels, tint). Use for studying styles, never shipping traced third-party geometry.
- **أرقام / params:** S=4 supersample; XOR ~0.22%
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9357-rotoscope/reference/method.md` · `kosif-atlas/skills/2414-animation/9357-rotoscope/SKILL.md`

#### DRAW-18 · ترجمة كتابة يدوية متتابعة · Typewriter handwritten caption · 📦 بأمر تثبيت
- **ماذا / what:** Left-aligned handwritten-style sentence that reveals letter by letter after the full layout is fixed (so text never re-centres while typing), optional underline or hand-drawn circle accent.
- **كيف / how:** Fusion Text+ Write On End animated; reveal over 65% of clip by default (RevealDelay + RevealDuration ≤ 1); placement 8-12% inside frame edges on empty area; glyph 4-5% H; circle via shape WriteLength. In HTML: clip-path/char spans with GSAP stagger.
- **أرقام / params:** reveal 0.65 of clip
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2431-akbun-davinciresolve-caption-template/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2431-akbun-davinciresolve-caption-template/references/template-controls.md`

#### DRAW-19 · قياس أسلوب الرسم اليدوي · Hand-drawn style pack measurement · 📦 بأمر تثبيت
- **ماذا / what:** Turn a rotoscoped reference into numeric style bands (palette, edge softness, stroke width, roughness, boil, holds) and check new animation against them, without copying source geometry.
- **كيف / how:** Animation plugin: ffmpeg libx264 + Node + playwright-core Chromium + numpy/opencv; learn.py/controls.py (not run here)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9355-learn-style/SKILL.md` · `kosif-atlas/skills/2414-animation/9358-setup/SKILL.md`

#### DRAW-20 · تعليقات يدوية خشنة على النص · Rough-notation hand-drawn annotations · 📦 بأمر تثبيت
- **ماذا / what:** Sketchy highlight, circle, underline, strike, crossed-off, box and bracket marks drawn around words with a progress value.
- **كيف / how:** Remotion @remotion/rough-notation components <Highlight>/<Circle>/<Underline>/<Box>/<Bracket>; drive progress with interpolate(frame,[15,40],[0,1],clamp). Plain HTML alternative: rough-notation npm. Needs package install.
- **أرقام / params:** highlight rgba(255,236,79,0.62); draw window ~25 frames
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/text-highlights.md`

#### DRAW-21 · أسلوب الرسم الخشن بخطوط التظليل · Rough sketch rendering style (roughness/hachure) · 📦 بأمر تثبيت
- **ماذا / what:** Excalidraw/rough.js-style strokes with controllable wobble and hachure or cross-hatch fills.
- **كيف / how:** Excalidraw JSON elements carry roughness 0/1/2, fillStyle solid|hachure|cross-hatch, strokeStyle solid|dashed|dotted, seed for reproducible wobble. For video use rough.js on canvas/SVG with fixed seed per frame to avoid boiling, or re-seed every 2-3 frames for deliberate boil.
- **أرقام / params:** roughness 0-2; seed fixed; fontFamily 1 hand / 3 mono
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2790-work/11181-draw-excalidraw`

#### DRAW-22 · تحويل الحبر النقطي إلى متجهات · Raster-to-vector ink tracing · 📦 بأمر تثبيت
- **ماذا / what:** Trace two-tone ink drawings to polygon paths with holes so they can be re-rendered or animated as vectors.
- **كيف / how:** OpenCV findContours on 4x-supersampled image after unsharp mask, approxPolyDP; correct inward bias by a ring of capsule dabs at render. S=8 adds nothing over S=4.
- **أرقام / params:** supersample S=4; unsharp then blur sigma ~0.85px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9357-rotoscope`

#### DRAW-23 · محرك فرشاة حبر حتمي · Deterministic ink brush engine on canvas · 📦 بأمر تثبيت
- **ماذا / what:** Paths are rendered through capsule dabs, separable gaussian blur, optional paper grain and tone layers so the same input yields identical pixels.
- **كيف / how:** Canvas 2D in headless Chromium (Playwright) with an ink.js-style capsule() and paperGrain(); renderFrame(t) API for frame-accurate capture. Chromium ctx.filter blur is ignored below ~0.8px, so implement JS blur.
- **أرقام / params:** blur floor 0.8px; grain off for faithful copy
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9357-rotoscope`

#### DRAW-24 · كشف الحدود متعددة الأجزاء · Multi-segment border reveal · 📦 بأمر تثبيت
- **ماذا / what:** Draw a complete country border (many rings/islands) as one timed stroke by cumulative length, without inventing joins.
- **كيف / how:** Store each segment line, its length and cumulative start; for a reveal window [from,to] km slice every overlapping segment and emit a MultiLineString; skip slivers under 0.0008 km; never clip the border to the viewport (it may leave frame naturally).
- **أرقام / params:** sliver threshold 0.0008 km
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-explainer-architecture.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-geo-prep.md`

#### DRAW-25 · مخططات تجادل لا تعرض · Diagrams that argue (visual patterns) · 📦 بأمر تثبيت
- **ماذا / what:** Shape carries meaning: fan-out, convergence, tree, cycle, cloud, assembly line, side-by-side, gap, lines as structure.
- **كيف / how:** Isomorphism test: remove all text, the structure should still communicate. Timelines as a line with 10-20 px dots and free labels; trees as trunk+branch lines; assembly line chaos->process->order. Excalidraw JSON with roughness 0-2 gives a hand-drawn look and can be rendered to PNG then animated (draw-on of strokes).
- **أرقام / params:** roughness 0 smooth / 1 default / 2 rough; timeline dots 10-20 px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2790-work/11181-draw-excalidraw/SKILL.md` · `kosif-atlas/skills/2790-work/11181-draw-excalidraw/references/visual-patterns.md` · `kosif-atlas/skills/2790-work/11181-draw-excalidraw/references/json-schema.md`

#### DRAW-26 · رسم فوق اللقطات المولدة بشكل حتمي · Deterministic draw-over on generated bases · 📦 بأمر تثبيت
- **ماذا / what:** Generated clips provide motion; a hand-built JavaScript look redraws every frame as a pure function of time (two-ink print, halftone, line work, boiling lines) with kinetic lyric type.
- **كيف / how:** film.js renderAt(t) in headless Chrome, frame-exact capture then ffmpeg encode with the song; look.js default: two inks on paper, halftone dots, line work, line boil 12×/s, fixed paper tooth; shots.json fields at, dur, base, baseStart, focus (0..1), type big|quiet|none, side; 16:9 and 1080x1920 modes.
- **أرقام / params:** boil 12 fps; 1080x1920 vertical
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video`

#### DRAW-27 · خطوط حبر بضغط · Pressure ink strokes (draw-on) · 📦 بأمر تثبيت
- **ماذا / what:** Draws a polyline progressively by arc length with tapered ends and pressure variation, returning the pen head for a hand/spark.
- **كيف / how:** INK.stroke(c,pts,k,w,col,seed,{plain,alpha}): cumulative length; taper = min(1, .35+5u, .35+5(1-u)); pressure .74+.26 sin(0.9i+3.7seed); INK.strokes runs a list sequentially sharing progress by length; INK.at returns a point at fraction k.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:208` · `app/public/js/10_studio.js:210`

#### DRAW-28 · تظليل بخطوط مائلة · Hatching fill · 📦 بأمر تثبيت
- **ماذا / what:** Colours a closed shape with progressive diagonal hatching like a whiteboard marker.
- **كيف / how:** INK.hatch(c,outline,k,col,gap,w,alpha=0.5): clip to outline, draw diagonal lines up to k of span/gap.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:232`

#### DRAW-29 · مكتبة أيقونات مرسومة · Stroke motif icon library (16) · 📦 بأمر تثبيت
- **ماذا / what:** Sixteen icons built from strokes (with fill outlines for hatching) and an Arabic keyword matcher that picks one per line.
- **كيف / how:** MOT: sun, cloud, wave, drop, bulb, heart, star, check, chart, target, clock, mountain, phone, people, doc, arrow; MK.motifFor(text,i) matches regexes (شمس/سحاب/بحر/فكر/قلب/نمو/هدف/وقت/جبل...) else cycles 8 defaults.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:245` · `app/public/js/10_studio.js:262`

#### DRAW-30 · ستايل السبورة البيضاء · Whiteboard style · 📦 بأمر تثبيت
- **ماذا / what:** Lesson-style film: marker writing and motif doodles on a white board, step by step, synced to the voice.
- **كيف / how:** STY.whiteboard (board engine shared with chalkboard): 16:9, mood calm, 2.0 wps, font Marhey, palette bg #F4F4F1 ink #23272E accent #E0412E colours #1E63D6/#E0412E/#F28C12/#2E9B4F; sfx write=pen, line=click, end=shimmer; lines revealed right-to-left with the pen.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:342` · `app/public/js/10_studio.js:438`

#### DRAW-31 · ستايل السبورة والطباشير · Chalkboard style · 📦 بأمر تثبيت
- **ماذا / what:** Maths/science lesson in chalk on a green board.
- **كيف / how:** STY.chalkboard: 16:9, calm, 1.9 wps, font Aref Ruqaa, bg #264A3E ink #F3F1E7 accent #F6E07A colours #F6E07A/#F4A9BC/#9AD3F0/#A9E6A2; sfx write=chalk, line=tick, end=shimmer.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:471`

#### DRAW-32 · ستايل دودل حكاية · Doodle story style · 📦 بأمر تثبيت
- **ماذا / what:** An ink-drawn world in one take with a walking character and word-by-word speech with one glowing word; vertical.
- **كيف / how:** STY.doodle: 9:16, calm, 1.9 wps, font Tajawal; palette sky #AFDCF0->#EAF6F4, sand #F1D9AE, grass #BCDB92, water #6FB3C8, ink #3A2A1E, text #1E2B45, em #F07F2E, glow #FFD0A0, robe #F6F0E4, turban #2F4E86, skin #C98B5B; sfx pop/shimmer/swish/swell.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:854`

#### DRAW-33 · ستايل البلوتر · Plotter style · 📦 بأمر تثبيت
- **ماذا / what:** Tech explainer: a pen plotter traces a curve on dark grid paper with an orange spark, mono annotations, a timeline ruler and STEP counters while words light up with the voice.
- **كيف / how:** STY.plotter: 16:9, tech, 2.2 wps; fonts Readex Pro + IBM Plex Mono; bg #0B0B0C ink #F4F4F2 dim #3A3A3E accent #FF5A1F grid rgba(255,255,255,.055) at 6.2% m drifting 3 px/s; 180-point seeded curve; vignette 0.5 + grain 0.08; sfx blip/hit/whoosh/drop.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:292`

#### DRAW-34 · رسم المسارات SVG · SVG draw-on safety · 📦 بأمر تثبيت
- **ماذا / what:** Stroke draw-on must measure path after d is set and not fight CSS dasharray.
- **كيف / how:** Lint svg_measure_before_path_d, svg_drawon_css_dasharray_conflict; registry hw-* and svg-stroke-trace components.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/lint/src/rules/gsap.ts`

#### DRAW-35 · قلم التعليق · Annotate Cursor · 📦 بأمر تثبيت
- **ماذا / what:** A marker pen glides in and hand-draws a loop, underline or arrow around a region with ink exactly under the nib, then lifts away.
- **كيف / how:** Install with `npx hyperframes add cursor-annotate` (copies to compositions/components/cursor-annotate.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **أرقام / params:** shape circle|underline|arrow; color #f43f5e; target_x/y/w/h %; vars: shape=circle[circle|underline|arrow]; color=#f43f5e; target_x=40(0..95); target_y=38(0..95); target_w=20(2..90); target_h=16(2..90)
- **تثبيت / install:** `npx hyperframes add cursor-annotate` (copies to compositions/components/cursor-annotate`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/cursor-annotate/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/cursor-annotate/cursor-annotate.html` · `kosif-one/vendor/hyperframes/registry/components/cursor-annotate/demo.html`

#### DRAW-36 · سهم مرسوم باليد · Hand-Drawn Arrow · 📦 بأمر تثبيت
- **ماذا / what:** Wobbly draw-on arrow in straight/gentle/swoop poses with plain/soft/sharp/spray stroke textures and a stretch pulse when the head arrives; boils on screen.
- **كيف / how:** Install with `npx hyperframes add hw-arrow` (copies to compositions/components/hw-arrow.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame captur…
- **أرقام / params:** stroke matrix plain|soft|sharp|spray; Caveat 700 bundled
- **تثبيت / install:** `npx hyperframes add hw-arrow` (copies to compositions/components/hw-arrow`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/hw-arrow/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/hw-arrow/hw-arrow.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/hw-arrow.mdx`

#### DRAW-37 · غليان الرسم اليدوي · Hand-Drawn Boil · 📦 بأمر تثبيت
- **ماذا / what:** Seek-safe helper library: hand-drawn jitter that re-poses every N frames from quantised time through a seeded hash, wobbly ellipse generator, boil control off/calm/lively, curvature-adaptive pen ease, stroke matrix.
- **كيف / how:** Install with `npx hyperframes add hw-boil` (copies to compositions/components/hw-boil.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame capture …
- **أرقام / params:** boil off|calm|lively; spray = index-seeded dots
- **تثبيت / install:** `npx hyperframes add hw-boil` (copies to compositions/components/hw-boil`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/hw-boil/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/hw-boil/hw-boil.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/hw-boil.mdx`

#### DRAW-38 · صندوق بعنوان يدوي · Hand-Drawn Box Label · 📦 بأمر تثبيت
- **ماذا / what:** Wobbly rounded rectangle draws on (or drops in with volume-preserving squash and spring) with a handwritten label.
- **كيف / how:** Install with `npx hyperframes add hw-box-label` (copies to compositions/components/hw-box-label.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fram…
- **تثبيت / install:** `npx hyperframes add hw-box-label` (copies to compositions/components/hw-box-label`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/hw-box-label/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/hw-box-label/hw-box-label.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/hw-box-label.mdx`

#### DRAW-39 · دائرة تعليق يدوية · Scribble Callout Circle · 📦 بأمر تثبيت
- **ماذا / what:** Wobbly ellipse drawn around a target, optional scribble fill and curved connector; handwritten label pops in with momentum and shapes squash on contact.
- **كيف / how:** Install with `npx hyperframes add hw-callout-circle` (copies to compositions/components/hw-callout-circle.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chr…
- **تثبيت / install:** `npx hyperframes add hw-callout-circle` (copies to compositions/components/hw-callout-circle`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/hw-callout-circle/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/hw-callout-circle/hw-callout-circle.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/hw-callout-circle.mdx`

#### DRAW-40 · خط سفلي يدوي · Squiggle Marks · 📦 بأمر تثبيت
- **ماذا / what:** Hand-drawn squiggle underline, double-pass strikethrough and bracket marks that draw on.
- **كيف / how:** Install with `npx hyperframes add hw-underline` (copies to compositions/components/hw-underline.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fram…
- **تثبيت / install:** `npx hyperframes add hw-underline` (copies to compositions/components/hw-underline`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/hw-underline/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/hw-underline/hw-underline.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/hw-underline.mdx`

#### DRAW-41 · بطاقة قائمة بالماركر · Marker Checklist Card · 📦 بأمر تثبيت
- **ماذا / what:** Paper card with marker headline, underline and a drawn ellipse on one word, then three checklist rows whose ticks draw on (typewriter labels, marker values).
- **كيف / how:** Install with `npx hyperframes add marker-checklist-card` (copies to compositions/components/marker-checklist-card.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (head…
- **أرقام / params:** Permanent Marker 400 + Courier Prime 700 bundled; vars: top=THE POWER; mid=OF; circled=ONE; rest=FILE; l1=WRITE; v1=HTML; l2=RENDER; v2=IN 4K; l3=SHIP; v3=TODAY
- **تثبيت / install:** `npx hyperframes add marker-checklist-card` (copies to compositions/components/marker-checklist-card`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/marker-checklist-card/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/marker-checklist-card/marker-checklist-card.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/marker-checklist-card.mdx`

#### DRAW-42 · إبراز بالماركر · Marker Highlight · 📦 بأمر تثبيت
- **ماذا / what:** Display text settles, then one hand-drawn marker stroke (highlight/circle/underline/scribble) draws over the emphasis word on cue.
- **كيف / how:** Install with `npx hyperframes add marker-highlight` (copies to compositions/components/marker-highlight.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chrom…
- **أرقام / params:** draw_at 0.9 s; vars: text=Ship it with confidence; emphasis_word=confidence; style=highlight[highlight|circle|underline|scribble]; draw_at=0.9(0..None); accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add marker-highlight` (copies to compositions/components/marker-highlight`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/marker-highlight/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/marker-highlight/marker-highlight.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/marker-highlight.mdx`

#### DRAW-43 · نص مخيط · Stitched Text Draw · 📦 بأمر تثبيت
- **ماذا / what:** Single-stroke display alphabet drawn as thread stitches: dash patterns, angle jitter, needle-hole dots, leading needle and thread-tail overshoot.
- **كيف / how:** Install with `npx hyperframes add stitched-text-draw` (copies to compositions/components/stitched-text-draw.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless C…
- **أرقام / params:** stitch fine|coarse; vars: text=STITCH; stitch=fine[fine|coarse]; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add stitched-text-draw` (copies to compositions/components/stitched-text-draw`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/stitched-text-draw/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/stitched-text-draw/stitched-text-draw.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/stitched-text-draw.mdx`

#### DRAW-44 · رسم خط محمل · SVG Line Draw Loader · 📦 بأمر تثبيت
- **ماذا / what:** Anime.js-style path-drawing loader as a seekable GSAP stroke timeline.
- **كيف / how:** Install with `npx hyperframes add svg-line-draw-loader` (copies to compositions/components/svg-line-draw-loader.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headle…
- **تثبيت / install:** `npx hyperframes add svg-line-draw-loader` (copies to compositions/components/svg-line-draw-loader`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/svg-line-draw-loader/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/svg-line-draw-loader/svg-line-draw-loader.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/svg-line-draw-loader.mdx`

#### DRAW-45 · تتبع الخط · SVG Stroke Trace · 📦 بأمر تثبيت
- **ماذا / what:** Authored SVG path draws from its measured length, holds with drift and optionally fills if closed.
- **كيف / how:** Install with `npx hyperframes add svg-stroke-trace` (copies to compositions/components/svg-stroke-trace.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chrom…
- **أرقام / params:** stroke_width 12; path d; vars: path=M 92 328 C 178 142 292 138 366 276 C 430 396 500 414 558 262 C 622 94 724 112 786 274 C 836 406 894 376 930 194; stroke_width=12(2..32); accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add svg-stroke-trace` (copies to compositions/components/svg-stroke-trace`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/svg-stroke-trace/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/svg-stroke-trace/svg-stroke-trace.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/svg-stroke-trace.mdx`

#### DRAW-46 · تعليق بأسلوب فوكس · Vox Annotate · 📦 بأمر تثبيت
- **ماذا / what:** Keyword in a held sentence gets a marker stroke while a thin connector draws to a mono callout label in one beat.
- **كيف / how:** Install with `npx hyperframes add vox-annotate` (copies to compositions/components/vox-annotate.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fram…
- **أرقام / params:** style highlight|circle|underline|scribble; draw_at 0.9 s; vars: text=Ship the story, not the spec; keyword=story; note=the annotate beat; style=highlight[highlight|circle|underline|scribble]; draw_at=0.9(0..None); accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add vox-annotate` (copies to compositions/components/vox-annotate`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/vox-annotate/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/vox-annotate/vox-annotate.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/vox-annotate.mdx`

#### DRAW-47 · رسم السبورة · Whiteboard Ink · 📦 بأمر تثبيت
- **ماذا / what:** Whiteboard sketch draws one measured stroke at a time with a pen nib on the tip; presets or own multi-stroke SVG; data-ink=accent stroke uses accent.
- **كيف / how:** Install with `npx hyperframes add whiteboard-ink` (copies to compositions/components/whiteboard-ink.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium …
- **أرقام / params:** sketch bulb|flow|rocket; pen show|hide; vars: sketch=bulb[bulb|flow|rocket]; caption=Draw the idea; pen=show[show|hide]; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add whiteboard-ink` (copies to compositions/components/whiteboard-ink`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/whiteboard-ink/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/whiteboard-ink/whiteboard-ink.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/whiteboard-ink.mdx`

#### DRAW-48 · دائرة مؤشرة · Pointer Circle + Countdown · 📦 بأمر تثبيت
- **ماذا / what:** Draw-on ellipse around a target plus a countdown chip pulsing each tick.
- **كيف / how:** Install with `npx hyperframes add yt-circle-pointer` (copies to compositions/components/yt-circle-pointer.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chr…
- **تثبيت / install:** `npx hyperframes add yt-circle-pointer` (copies to compositions/components/yt-circle-pointer`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/yt-circle-pointer/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/yt-circle-pointer/yt-circle-pointer.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/yt-circle-pointer.mdx`

#### DRAW-49 · إطار مرسوم باليد · Sketched Frame · 📦 بأمر تثبيت
- **ماذا / what:** Media inside a hand-drawn border with corner doodles and handwritten caption; tilts and boils.
- **كيف / how:** Install with `npx hyperframes add hw-frame` (copies the full composition to compositions/hw-frame.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Caveat 700; 1920x1080; duration 8 s
- **تثبيت / install:** `npx hyperframes add hw-frame` (copies the full composition to compositions/hw-frame`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/hw-frame/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/hw-frame/hw-frame.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/hw-frame.mdx`

#### DRAW-50 · كتابة على مسار · Text Along a Path · 📦 بأمر تثبيت
- **ماذا / what:** Handwriting flows along any SVG path with per-character reveal.
- **كيف / how:** Install with `npx hyperframes add hw-path-text` (copies the full composition to compositions/hw-path-text.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Caveat 700; 1920x1080; duration 6 s
- **تثبيت / install:** `npx hyperframes add hw-path-text` (copies the full composition to compositions/hw-path-text`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/hw-path-text/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/hw-path-text/hw-path-text.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/hw-path-text.mdx`

#### DRAW-51 · خط أنابيب يدوي · Hand-Drawn Flowchart · 📦 بأمر تثبيت
- **ماذا / what:** Wobbly boxes with handwritten labels joined by curved connectors, drawing on in sequence from a node list.
- **كيف / how:** Install with `npx hyperframes add hw-pipeline` (copies the full composition to compositions/hw-pipeline.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Caveat 700; 7 s; 1920x1080; duration 7 s
- **تثبيت / install:** `npx hyperframes add hw-pipeline` (copies the full composition to compositions/hw-pipeline`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/hw-pipeline/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/hw-pipeline/hw-pipeline.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/hw-pipeline.mdx`

#### DRAW-52 · انتقال الشخبطة · Scribble Transition · 📦 بأمر تثبيت
- **ماذا / what:** Overlay transition: scribble bands accumulate to cover the frame, host cuts underneath, scribble clears.
- **كيف / how:** Install with `npx hyperframes add hw-scribble-transition` (copies the full composition to compositions/hw-scribble-transition.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 2.2 s; 1920x1080; duration 2.2 s
- **تثبيت / install:** `npx hyperframes add hw-scribble-transition` (copies the full composition to compositions/hw-scribble-transition`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/hw-scribble-transition/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/hw-scribble-transition/hw-scribble-transition.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/hw-scribble-transition.mdx`

#### DRAW-53 · فقاعة كلام يدوية · Speech Bubble · 📦 بأمر تثبيت
- **ماذا / what:** Hand-drawn speech bubble with positionable tail: outline draws, paper fill fades, text types per character; boils.
- **كيف / how:** Install with `npx hyperframes add hw-text-cloud` (copies the full composition to compositions/hw-text-cloud.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Caveat 700; 1920x1080; duration 6 s
- **تثبيت / install:** `npx hyperframes add hw-text-cloud` (copies the full composition to compositions/hw-text-cloud`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/hw-text-cloud/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/hw-text-cloud/hw-text-cloud.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/hw-text-cloud.mdx`

#### DRAW-54 · عنوان بخط اليد · Handwritten Title · 📦 بأمر تثبيت
- **ماذا / what:** Handwritten display text with scalar-driven word highlight sweep and seeded squiggle underline sized to the text; boils.
- **كيف / how:** Install with `npx hyperframes add hw-title` (copies the full composition to compositions/hw-title.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Caveat 700; 1920x1080; duration 6 s
- **تثبيت / install:** `npx hyperframes add hw-title` (copies the full composition to compositions/hw-title`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/hw-title/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/hw-title/hw-title.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/hw-title.mdx`

#### DRAW-55 · كتابة العنوان بالقلم · Handwritten Write-On Title · 📦 بأمر تثبيت
- **ماذا / what:** True glyph write-on: filled Caveat letters revealed by baked per-glyph centreline strokes in real stroke order with curvature-adaptive pen speed and pen lifts.
- **كيف / how:** Install with `npx hyperframes add hw-write-title` (copies the full composition to compositions/hw-write-title.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Caveat 700; 1920x1080; duration 6 s
- **تثبيت / install:** `npx hyperframes add hw-write-title` (copies the full composition to compositions/hw-write-title`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/hw-write-title/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/hw-write-title/hw-write-title.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/hw-write-title.mdx`

#### DRAW-56 · رسم المسار ذاتيا · SVG path self-draw · 📦 بأمر تثبيت
- **ماذا / what:** Outline draws stroke by stroke via stroke-dasharray/dashoffset measured with getTotalLength at setup; rings rotate -90deg to start at 12 o'clock.
- **كيف / how:** Read hyperframes-animation/rules/svg-path-draw.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** each segment starts at ~70-80% of previous segment's duration; ease power2.out
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/svg-path-draw.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### DRAW-57 · أنماط قلم التحديد · Marker highlight drawing modes · 📦 بأمر تثبيت
- **ماذا / what:** Pure CSS + GSAP marker emphasis: highlight (yellow sweep), circle (hand-drawn ellipse), burst (radiating lines), scribble, sketchout (rough rectangle).
- **كيف / how:** Read hyperframes-animation/rules/css-marker-patterns.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** highlight bar inset 0 -6px, radius 3 px, scaleX 0->1 0.5 s power2.out at 0.6 s; multi-line stagger 0.3 s; ellipse border-radius 50% + slight rotation
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/css-marker-patterns.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### DRAW-58 · مكونات الرسم اليدوي · Registry hand-drawn components and blocks · 📦 بأمر تثبيت
- **ماذا / what:** hw-arrow, hw-boil, hw-box-label, hw-callout-circle, hw-underline components; hw-frame, hw-path-text, hw-pipeline, hw-scribble-transition, hw-text-cloud, hw-title, hw-write-title blocks; plus whiteboard-ink, marker-highlight, outline-draw, stitched-text-draw.
- **كيف / how:** npx hyperframes add hw-*.
- **تثبيت / install:** `npx hyperframes add hw-*`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components` · `kosif-one/vendor/hyperframes/registry/blocks`

#### DRAW-59 · خطوط هيرشي أحادية الخط للكتابة اليدوية · Hershey single-stroke fonts for handwriting draw-on · 📦 بأمر تثبيت
- **ماذا / what:** HersheyScript1 and HersheyScriptMed SVG stroke fonts used to WRITE apex words stroke by stroke (neonsign, aurora, chalkboard, graffiti, brush, spectrum).
- **كيف / how:** python scripts/gen-stroke-path.py builds stroke paths; theme fonts.strokeFont = 'HersheyScript1.svg'.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/assets/strokefonts/HersheyScript1.svg` · `kosif-one/vendor/hyperframes/skills/embedded-captions/assets/strokefonts/HersheyScriptMed.svg` · `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/gen-stroke-path.py`

#### DRAW-60 · دائرة إبراز على أصل حقيقي · Circle highlight on real asset sample · 📦 بأمر تثبيت
- **ماذا / what:** Reference sample of a drawn circle highlight around a located object in an image (asset-fusion).
- **كيف / how:** Open samples/asset-fusion/_ref-circle-highlight.html.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/motion-graphics/samples/asset-fusion/_ref-circle-highlight.html`

#### DRAW-61 · رسم المسار · drawPath pen stroke · 📦 بأمر تثبيت
- **ماذا / what:** SVG stroke draw-on with optional arrowhead landing on arrival; flowDash for moving current.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** drawPath(...,{head}); flowDash
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### DRAW-62 · رسم الخط تدريجياً برأس قلم · Stroke draw-on with pen head · 📦 بأمر تثبيت
- **ماذا / what:** Any SVG stroke draws itself via dash offset; an optional dot pops at the leading end like a pen tip.
- **كيف / how:** M.drawPath(tl, path, at, dur, {head:dot, ease, opacity}) → strokeDashoffset len→0; head scale 0→1 with spring('snappy') at at+dur−0.1; used for the gold ring (0.9 s E.out), clock ring (1.0 s), dream path (0.9 s), car body (0.75 s), wheels (0.4 s), spring curve (1.15 s), end ring (0.62 s).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:67` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:204` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:98`

#### DRAW-63 · ظهور العلامات بالتتابع · Staggered tick reveal · 📦 بأمر تثبيت
- **ماذا / what:** Clock ticks or scale marks appear one after another right after their ring draws, adding a mechanical rhythm.
- **كيف / how:** tl.to(tickEls, {opacity:.9, duration:.08, stagger:.035, ease:'none'}, 1.95) for 24 ticks; scale rail ticks static at .7 with slide-in x −24→0.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:205`

#### DRAW-64 · شريط مسح سلكي فوق المجسم · Wireframe scan band over a sculpt · 📦 بأمر تثبيت
- **ماذا / what:** A glowing wireframe band sweeps up the character's mesh with a bright leading edge and a shrinking ground ring, reading as 'digitising the object'.
- **كيف / how:** ShaderMaterial wireframe on the same geometry: band = smoothstep(.09,0, scan−y)·step(y, scan+.004); edge = smoothstep(.012,0,|y−scan|); colour mix (.62,1,.72)→(.95,1,.8); scanY lerp(−.02,.4) over .78 s; ring 0xd0ff6a scale 1.15→0.6.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:59` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:137`

#### DRAW-65 · تشكّل من مخطط سلكي إلى مجسم قطيفة · Schematic wireframe → plush formation · 📦 بأمر تثبيت
- **ماذا / what:** Characters form from a technical schematic into finished plush over the opening seconds; parts can explode apart and joint markers glow while the lens visits them.
- **كيف / how:** schematic(obj).set(form, camera) with form = 1 − ease(ramp(t, .4, 2.8)); .explode(.35·pulse(3.2, 6.2)); .joints(pulse(3.0, 9.0)).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/src/main.js:19` · `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/src/main.js:53`

#### DRAW-66 · رسم يدوي Rough.js · Rough.js hand-drawn · 📦 بأمر تثبيت
- **ماذا / what:** Sketchy SVG/Canvas shapes.
- **كيف / how:** in-page lib
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### DRAW-67 · رسم المسار تدريجياً · SVG draw-on (Vivus/Lazy Line/Walkway) · 📦 بأمر تثبيت
- **ماذا / what:** Path stroke reveal libs.
- **كيف / how:** in-page lib; or GSAP stroke-dashoffset
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### DRAW-68 · رسم متجهي بالقلم في برنامج الرسام · Vector drawing by pen in Windows Paint (SVG/shapes) · 📦 بأمر تثبيت
- **ماذا / what:** Claude draws SVG paths or primitive shapes stroke by stroke into Paint (or any canvas window) with its own synthetic pen, fitted into a target box, optionally hatch-filled.
- **كيف / how:** kosif_mouse_act window=Paint actions=[{do:'draw', target:'canvas', viewbox:[0,0,100,100], svg:'M50 30 C35 18 ...'} or shapes:[{type:circle|ellipse|arc|rect|line|polyline|polygon|path, fill:true}], expect:{changed:true}]; for solid areas outline then bucket-fill (1 tap per area).
- **أرقام / params:** fit margin 0.08; hatch gap default 2 px (whole-pixel rows); closed shapes run on 30% past start to seal bucket fills; arcs sampled every 6 deg (>= 12 points)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/desktop.py:1032` · `kosif-one/tools/kosif-omni/skills/kosif-mouse/SKILL.md` · `kosif-one/tools/kosif-omni/mcp-server/tests/test_desktop.py:259`

#### DRAW-69 · إعادة رسم صورة بكسل ببكسل في الرسام · Pixel-exact image redraw in Paint (KOSIF Replicate) · 📦 بأمر تثبيت
- **ماذا / what:** Redraws an image by hand in Windows Paint with Pencil 1 px and the colour dialog, then verifies every pixel and repairs until identical — a provable 'hand-made' recreation (or a fast 64-colour approximation).
- **كيف / how:** kosif_paint_copy image=<png> window=Paint [zoom 4] [colors 64] [budget_s 3600]; resumable; CLI python -m kosif_mcp.replicate --save new.png compares RGB and alpha; --erase-transparent.
- **أرقام / params:** limit 200,000 px; ~0.6-0.68 s per colour; taps ~1,030 px/s; 85x98 logo 2,650 colours = 100% (8,330/8,330 px) in ~25 min; 64 colours ~1.3 min mean dE 2.4; two-coat recipe for hues Paint cannot hold (20% opacity)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/replicate.py:1` · `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/replicate.py:1003` · `kosif-one/tools/kosif-omni/mcp-server/tests/test_replicate.py`

#### DRAW-70 · رسم المحراب بقلم ذهبي · Gold pen draw-on of a mihrab arch · 📦 بأمر تثبيت
- **ماذا / what:** The pointed arch (and an inner parallel arch, two date rules) draws itself like a gold pen at the start, then thickens on the final 'آمين'.
- **كيف / how:** SVG path with stroke url(#gold) linearGradient #fff0b3/#e8b04a/#fff0b3, width 7 round caps; M.drawPath(tl,path,0,1.7,{ease:E.out}); inner arch #f3c766 op .55 width 3 at 0.25 s; on 22.95 s stroke-width 7 -> 9.
- **أرقام / params:** arch d='M150,1760 L150,1010 C150,770 370,610 540,520 C710,610 930,770 930,1010 L930,1760'
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html:74-77` · `kosif-one/projects/thursday-dua-animation/source/index.html:188-194` · `kosif-one/projects/thursday-dua-animation/source/index.html:220`

#### DRAW-71 · نهر يمتلئ ثم يجري · River fill then flow (pathLength dash) · 📦 بأمر تثبيت
- **ماذا / what:** A river first fills from the mountain to the sea, then light dashes run along it to show flow.
- **كيف / how:** Same path three times: dry bed #CDE7F7 20 px; water #2B8CE6 pathLength=1 dasharray '1 1' dashoffset 1 -> 0 (7.3-8.7 s); flow #A9DBFF 6 px dasharray '0.04 0.07' dashoffset -0.35t, opacity in at 8.4 s.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/index.html:63-66` · `kosif-one/projects/water-cycle-animation/index.html:176-179`

#### DRAW-72 · رسم المسار بالقلم وتدفق الشرطات · SVG pen draw-on and flowing dashes · 📦 بأمر تثبيت
- **ماذا / what:** Any stroke draws itself like a pen (optionally popping an arrowhead at the end), or carries marching dashes to show flow.
- **كيف / how:** M.drawPath(tl,path,at,dur,{ease:power4.inOut,opacity,head}) using getTotalLength dasharray/dashoffset; M.flowDash(tl,path,at,dur,{pattern:'28 22',cycles:6}).
- **أرقام / params:** head pops 0.1 s before end with snappy spring 0.35 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:236-253`

#### DRAW-73 · فيلم رسم الصورة بيكسل ببيكسل · Drawing film: picture forming pixel by pixel · 📦 بأمر تثبيت
- **ماذا / what:** Records any scene, code file or image being painted in painter order as an MP4.
- **كيف / how:** python film.py drawing <scene|code|image> --out x.mp4 [--fps 30 --speed normal]; python film.py animate page.html|scene.py --out x.mp4 [--seconds 6].
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/film.py:1`

#### DRAW-74 · استوديو الرسم بيكسل ببيكسل · Pixel-by-pixel drawing studio · 📦 بأمر تثبيت
- **ماذا / what:** Desktop app that paints any picture in painter order, replaying PIL/SVG/matplotlib/turtle code step by step.
- **كيف / how:** python3 studio.py --code drawing.py | --image photo.jpg | --image-code; headless runner.py CODE OUT -> job_*.npz, done.json
- **أرقام / params:** canvas 1200x800, export 3840x2560
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/scripts/studio.py` · `100-superskills/skills/pixel-studio-painter/SKILL.md`

#### DRAW-75 · إعادة رسم مطابقة · Exact redraw (zero-pixel diff) · 📦 بأمر تثبيت
- **ماذا / what:** Three stages (blocks, refine, fine touches) ending with assert of 0 mismatched pixels incl. alpha; photos test 4 plans (6/10/16/24 block colours) in ~3 s, Jev picks twice in swapped order.
- **كيف / how:** exact.py; jev_client.py
- **أرقام / params:** 6/10/16/24 colours
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/scripts/exact.py` · `100-superskills/skills/pixel-studio-painter/scripts/jev_client.py`

#### DRAW-76 · صورة إلى كود بايثون · Image to standalone Pillow program · 📦 بأمر تثبيت
- **ماذا / what:** Writes a Pillow-only program drawing polygons then completing pixels from embedded original and self-verifying; --data-only form.
- **كيف / how:** python3 to_python.py / studio.py --image-code
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/scripts/to_python.py`

#### DRAW-77 · استيراد SVG · SVG import to draw steps · 📦 بأمر تثبيت
- **ماذا / what:** Every SVG element becomes a drawing step in order.
- **كيف / how:** svg_import.py
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/scripts/svg_import.py`

#### DRAW-78 · ترتيب ظهور الخطوات · Scene op: Step reveal orders · 📦 بأمر تثبيت
- **ماذا / what:** KOSIF Studio scene operation: Step.
- **كيف / how:** Step(name,ops,order sweep|grow|rise|down|left|right|sparkle,origin,weight)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md` · `100-superskills/skills/pixel-studio-painter/scripts/render.py`

#### DRAW-79 · فيلم الرسم · Drawing film / animate to MP4 · 📦 بأمر تثبيت
- **ماذا / what:** Video of the picture forming pixel by pixel, or animate render(t)/build_t(t) scenes, frames piped to ffmpeg.
- **كيف / how:** python3 film.py drawing|animate SRC --out x.mp4 --fps 30 --speed normal --seconds N
- **أرقام / params:** 30 fps, hold 1.5 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/scripts/film.py:229`

#### DRAW-80 · رسم المسار بالقلم · Pen draw-on stroke with arrowhead · 📦 بأمر تثبيت
- **ماذا / what:** Draws any SVG path like a pen via stroke-dashoffset; optional arrowhead lands with a spring just before the stroke ends.
- **كيف / how:** MOTION.drawPath(tl, path, at, dur, {ease, head, headOrigin, opacity}).
- **أرقام / params:** default ease power4.inOut; head scale 0->1 in .35 s spring snappy at at+dur-0.1
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:237` · `kosif-studio/motion/references/hyperframes-authoring.md`

#### DRAW-81 · أيقونات المعنى · Meaning icons drawn on (12) · 📦 بأمر تثبيت
- **ماذا / what:** Stroke-only 200×200 icons chosen by the meaning of a line and drawn with drawPath, breathing on the beat; numbers count up instead.
- **كيف / how:** line.motif.kind in sun|moon|heart|clock|money|trophy|road|question|check|home|rain|light, or kind 'count' with value.
- **أرقام / params:** stroke 5, round caps, accent colour; draw .7 s stagger .06; breathe 1+.06·beat+.04·rms
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/templates/verse.html`

#### DRAW-82 · مسجّل أوامر PIL بترتيب الكود · PIL drawing-command recorder (draw in the code's own order) · 📦 بأمر تثبيت
- **ماذا / what:** Monkey-patches ImageDraw so every rectangle/ellipse/polygon/line/arc/text call is snapshotted; consecutive calls of one kind are grouped into strokes, so the picture forms in the order the code drew it.
- **كيف / how:** Recorder.install() wraps ImageDraw methods, Image.paste/alpha_composite and save/show; commit() stores PNG snapshots; labels are Arabic call names with counts.
- **أرقام / params:** RUN = 20 commands per stroke (360 sky lines -> 18 strokes); stream thinned when > 300 snapshots; final job 'اللمسات الأخيرة'
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/runner.py:247` · `kosif-studio/runner.py:359` · `kosif-studio/runner.py:39`

#### DRAW-83 · فيلم الرسم: تشكّل الصورة كفيديو · Drawing film: the picture forming as MP4 · 📦 بأمر تثبيت
- **ماذا / what:** Records any scene, code file or image being painted pixel by pixel into an H.264 video, holding the finished frame at the end — a painting timelapse.
- **كيف / how:** python film.py drawing <scene|code file|image> --out out/x.mp4 [--fps 30] [--speed normal]; images are first wrapped as image code; native canvases are fitted into a 1280x720 frame on #1b1b1b.
- **أرقام / params:** fps 30; hold 1.5 s; libx264 preset medium crf 18 yuv420p, GOP 2*fps, +faststart; scene sheet 1200x800
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/film.py:59` · `kosif-studio/film.py:100` · `kosif-studio/studio.py:891`

#### DRAW-84 · الرسم المطابق تماماً: كتل ثم تدقيق ثم لمسات · Exact-match painting (block-in, refine, final touches) · 📦 بأمر تثبيت
- **ماذا / what:** Repaints any image from a blank transparent sheet in painter stages and ends identical to the original in every RGBA value: flat colour blocks first, then tonal refinement for photos, then exact correction of every remaining pixel.
- **كيف / how:** exact.plan(rgba, block_k, fine_k) yields jobs (label, order, origin, weight, idx, cols); block-in uses the logo's own palette or Lab k-means on a bilateral-filtered copy (+median 5); refine splits changed pixels into luminance tertiles (shadows, mid-tones, lights); asserts array_equal at the end.
- **أرقام / params:** block-in jobs grow, weight 0.9; refine sparkle weight 0.7 with change threshold sum|diff|>12; bilateral 9/40/9; k-means cap 60000 samples, 40 iters
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/exact.py:1` · `kosif-studio/exact.py:66` · `kosif-studio/exact.py:151`

#### DRAW-85 · رسوم خطية صغيرة فوق الفيديو · Line micro-graphics over footage · 📦 بأمر تثبيت
- **ماذا / what:** Thin ivory line drawings that illustrate each spoken example for ~1.2 s: a 24-hour clock with ticks and sweeping hand, a dream path rising with glow, a measurement rail with sliding marker, a one-line car with road streak, a draining time bar, a closing ring.
- **كيف / how:** inline SVG + M.drawPath / GSAP rotation
- **أرقام / params:** stroke 2-3 px #F5F0E6 with #E7B65A accents; ring r 150 at (205,640)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/premium_edit/index.html:56` · `kosif-studio/out/FINAL_EDIT/EDIT_NOTES.txt`

#### DRAW-86 · وايتبورد سينمائي · Style: Whiteboard cinematic (whiteboard-cinematic) · 📦 بأمر تثبيت
- **ماذا / what:** Whiteboard explainer upgraded with camera dolly, depth and dramatic framing between drawings.
- **كيف / how:** Draw-on strokes 800-1400 px/s with hand overlay pinned to path tip; camera pushes/pans to clean board space after 1.5-2s hold. Scaffold: python3 tools/kosif.py scaffold whiteboard-cinematic <dir>.
- **أرقام / params:** pen 4/8px; texture 5-10%
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:whiteboard-cinematic` · `kosif-tool/playbooks/hand-drawn.md`

#### DRAW-87 · إطار بإطار · Style: Frame by frame (frame-by-frame) · 📦 بأمر تثبيت
- **ماذا / what:** Traditional per-frame drawn animation feel on twos.
- **كيف / how:** Swap drawings every 2 frames (12 dps); boil with 3 stroke variants every 2-3 frames. Scaffold: python3 tools/kosif.py scaffold frame-by-frame <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:frame-by-frame` · `kosif-tool/playbooks/hand-drawn.md`

#### DRAW-88 · سبورة طباشير · Style: Chalkboard (chalkboard) · 📦 بأمر تثبيت
- **ماذا / what:** Chalk drawing on green/black board, inverted ink.
- **كيف / how:** Draw-on 800-1400 px/s, chalk texture strokes, board texture 5-10%. Scaffold: python3 tools/kosif.py scaffold chalkboard <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:chalkboard` · `kosif-tool/playbooks/hand-drawn.md`

#### DRAW-89 · سبورة بيضاء · Style: Whiteboard (whiteboard) · 📦 بأمر تثبيت
- **ماذا / what:** Marker drawing on whiteboard step by step with hand.
- **كيف / how:** Hand overlay lags 1 frame, rotates +-5 deg; hold 1.5-2s; pan to clean space. Scaffold: python3 tools/kosif.py scaffold whiteboard <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:whiteboard` · `kosif-tool/playbooks/hand-drawn.md`

#### DRAW-90 · قصص الدودل · Style: Doodle stories (doodle) · 📦 بأمر تثبيت
- **ماذا / what:** Ink doodle characters in one connected world, boiling lines.
- **كيف / how:** Boil: 3 stroke variants every 2-3 frames; continuous camera through world. Scaffold: python3 tools/kosif.py scaffold doodle <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:doodle` · `kosif-tool/playbooks/hand-drawn.md`

#### DRAW-91 · قلم البلوتر · Style: Plotter pen (plotter) · 📦 بأمر تثبيت
- **ماذا / what:** Mechanical pen-plotter drawing at constant speed.
- **كيف / how:** Constant pen speed, no easing; optional pen-up travel lines at 10% opacity. Scaffold: python3 tools/kosif.py scaffold plotter <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:plotter` · `kosif-tool/playbooks/hand-drawn.md`

#### DRAW-92 · رسم يدوي · Category: Hand-drawn · 📦 بأمر تثبيت
- **ماذا / what:** Capability family 'hand-drawn' (11 catalog entries) with a dedicated bilingual playbook of timings and recipes.
- **كيف / how:** Read playbooks/hand-drawn.md (visual grammar, motion mechanics, scene recipes, QA); build in starters/html-canvas or starters/remotion; filter catalog with python3 tools/kosif.py list --category hand-drawn.
- **أرقام / params:** pen 800-1400px/s; lift 60-120ms; hatching 2000px/s; boil every 2-3 frames; texture 5-10%
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md` · `kosif-tool/catalog/categories.json` · `kosif-tool/catalog/meta.json`

#### DRAW-93 · رسم الحلقات بالتمرير · SVG ring draw-on with scroll · 📦 بأمر تثبيت
- **ماذا / what:** Sand spiral grooves draw centre-out via strokeDashoffset 1->0 scrubbed.
- **كيف / how:** gsap.set dasharray 1; to offset 0 ease none scrub 1 start top 85% end center 40%.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/mcp-higgsfield-landing/src/scripts/motion.ts:64`

#### DRAW-94 · برومبت إطار ستوري بورد بالرصاص · Pencil storyboard frame prompt · 🔑 مفتاح/خدمة
- **ماذا / what:** A reusable prompt for 16:9 gray pencil storyboard frames: no colour except thin red lines for camera axis and eye line, camera drawn as a box on a tripod with a direction arrow, dashed frame rectangle, handwritten dimension notes.
- **كيف / how:** Fill slots (props, camera position, person view, action, frame cut line); output per shot as PNG via an image model or render the same look procedurally (SVG strokes with jitter) here.
- **أرقام / params:** 16:9; gray pencil + red axis lines
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2448-akbun-vlog-shotsketch/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2449-akbun-vlog-storyboard/SKILL.md`

#### DRAW-95 · أسلوب رسم الماركر على السبورة · Whiteboard marker-doodle illustration style · 🔑 مفتاح/خدمة
- **ماذا / what:** A graphic-recording look: warm cream paper, bold slightly wobbly navy ink outlines, loose marker hatching that overshoots the lines, a few bright colours, faceless white crowd figures, red/orange emphasis arrows.
- **كيف / how:** Use the fixed English template (style lines unchanged, only CHARACTER/SCENE/LABEL slots filled) to generate one illustration per narration beat; then in Remotion/GSAP reveal the plate with a draw-on mask or wipe to fake the hand drawing.
- **أرقام / params:** 3-5 colours; 1-2 short labels max; 2-5 scenes per story
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2421-akbun-draw-storytellingimage`

#### DRAW-96 · أسلوب القلم الرصاص الهادئ بلون واحد · Quiet pencil one-accent style · 🔑 مفتاح/خدمة
- **ماذا / what:** Grayscale graphite scene on cream paper with two thirds of the frame empty and exactly one small object filled in a single accent colour.
- **كيف / how:** Prompt: cream #F4ECDC, landscape 4:3, subjects small on a thin ground line, graphite #4A4A4A-#9A9A9A, hatching only, ONE object flat teal #2E7D8C. In motion, animate only the coloured object or let it be the transition anchor.
- **أرقام / params:** #F4ECDC; #4A4A4A-#9A9A9A; accent #2E7D8C; 4:3
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2419-akbun-draw-quiet-pencil`

#### DRAW-97 · دائرة يدوية لتأكيد الخطأ · Hand-drawn circle emphasis · 👁 شوهد في فيديو
- **ماذا / what:** irregular double-loop ellipse path drawn with stroke-dashoffset around the duplicate items, plus radiating burst ticks around a label
- **أرقام / params:** draw 500 ms, stroke 3 px black
- **الدليل / proof:** `style:pm-0xnfrith-5be616` · `style:pm-tak3sh8-be5012`

#### DRAW-98 · طباشيرة بلا يد تتبع رأس الخط · Hand-less chalk tip follower · 👁 شوهد في فيديو
- **ماذا / what:** place a rotated rounded-rect chalk sprite at the current stroke tip; tint it to the stroke colour; between strokes lift it (scale 1->1.08, shadow offset 2->10 px) and move along an eased path
- **أرقام / params:** chalk 60x12 px, lift 250 ms
- **الدليل / proof:** `style:chalkboard`

#### DRAW-99 · خط طباشير بضغط متغير وهالة · Pressure chalk stroke with halo · 👁 شوهد في فيديو
- **ماذا / what:** sample points along path, getStroke(points.slice(0, n*progress)) from perfect-freehand; draw twice: wider halo at ~0.12 opacity then the stroke
- **أرقام / params:** size 6-8, thinning 0.5, halo x2.2
- **الدليل / proof:** `style:chalkboard`

#### DRAW-100 · تقسيم المسارات المتعددة قبل الرسم الحر · Split multi-M paths for freehand · 👁 شوهد في فيديو
- **ماذا / what:** split a path with several M commands (e.g. grid lines) into separate strokes; distribute overall progress across them proportional to their length so freehand never bridges them with a scribble
- **أرقام / params:** length-weighted progress
- **الدليل / proof:** `style:chalkboard`

#### DRAW-101 · خط حبر متغيّر السُّمك · Variable-width ink outline · 👁 شوهد في فيديو
- **ماذا / what:** sample each SVG path to points, assign pressure via sin over arc length, run perfect-freehand getStroke and fill with ink colour; cache static shapes
- **أرقام / params:** size 3-6 px at 720w, thinning 0.5, ink #2f2820
- **الدليل / proof:** `style:doodle`

#### DRAW-102 · بناء الجسم: خط ثم تعبئة ثم سُمك · Stroke-to-fill-to-extrude build · 👁 شوهد في فيديو
- **ماذا / what:** outline dash draw-on, then face opacity 0->1, then extrusion depth 0->full, starting from a sparkle
- **أرقام / params:** 0.6 s / 0.3 s / 0.5 s
- **الدليل / proof:** `style:fake3d`

#### DRAW-103 · خطوط ماء موازية للساحل · Triple coastline water lines · 👁 شوهد في فيديو
- **ماذا / what:** stroke the sea boundary 3 times with decreasing widths, alternating ink then sea colour on top, all clipped inside the sea polygon -> three parallel ripples
- **أرقام / params:** widths ~18/12/6 px, ink #5d5140, sea #bfcdbe
- **الدليل / proof:** `style:map-journey`

#### DRAW-104 · رسم خط حبر برعشة يد · Hand-jitter ink stroke draw-on · 👁 شوهد في فيديو
- **ماذا / what:** smooth polygon with Catmull-Rom, add fixed seeded jitter (~0.5-1 px), animate strokeDashoffset via pathLength=1 over ~2 s
- **أرقام / params:** seeded noise, ease-in-out
- **الدليل / proof:** `style:map-journey`

#### DRAW-105 · قلم بشرارة يرسم المنحنى · Spark pen plotter draw-on · 👁 شوهد في فيديو
- **ماذا / what:** animate stroke-dashoffset of an SVG path and place a glowing orange dot plus 4-6 tiny particle sparks at getPointAtLength(progress); thin bone-white line with faint glow behind
- **أرقام / params:** line 1.5 px, spark core 6 px #f27525, glow blur 10 px, 1-2 s per stroke, easeInOutCubic
- **الدليل / proof:** `style:plotter`

#### DRAW-106 · نقطة تجرّ خطاً يرسم رمزاً · Dot-led line draw into a glyph · 👁 شوهد في فيديو
- **ماذا / what:** SVG path for a looping '?' with stroke-dashoffset animated while the dot rides the path tip (getPointAtLength)
- **أرقام / params:** stroke 3 px white, ~0.8 s ease-in-out
- **الدليل / proof:** `style:pm-1littlecoder-9fef89`

#### DRAW-107 · حديقة تنمو · Growing garden · 👁 شوهد في فيديو
- **ماذا / what:** Flowers scale-Y from their root point (transform-origin bottom) with staggered delays, then insects fly on Lissajous/sine paths with wing flap (scaleX oscillation)
- **أرقام / params:** grow 500-700 ms easeOut, stagger 80 ms, flap 8 Hz
- **الدليل / proof:** `style:pm-abderrahmen-g-9e8ed0`

#### DRAW-108 · رسم الأنبوب · Pipe draw-on · 👁 شوهد في فيديو
- **ماذا / what:** thick rounded stroke with light gradient, dashoffset 600 ms, dimension tick lines
- **الدليل / proof:** `style:pm-adamdesgns-478d6d`

#### DRAW-109 · كشف رسم السبورة · Whiteboard reveal · 👁 شوهد في فيديو
- **ماذا / what:** mask-reveal sketch illustration parts per sentence
- **الدليل / proof:** `style:pm-ajith-io-c52e09`

#### DRAW-110 · كتابة يدوية · Handwritten slogan write-on · 👁 شوهد في فيديو
- **ماذا / what:** script font revealed by mask with arrow drawn
- **الدليل / proof:** `style:pm-ajith-io-ea7f2d`

#### DRAW-111 · رسم الشعار بالخط · Monogram stroke draw-on · 👁 شوهد في فيديو
- **ماذا / what:** SVG stroke-dashoffset 1→0
- **أرقام / params:** 1 s inOut
- **الدليل / proof:** `style:pm-andginja-333d32`

#### DRAW-112 · رسم هندسي يُخطّ · Geometric line draw-on · 👁 شوهد في فيديو
- **ماذا / what:** SVG stroke-dashoffset on plan/temple outlines, stagger cells 40 ms
- **أرقام / params:** 1.5 s per drawing
- **الدليل / proof:** `style:pm-buildfastwithai-53234e`

#### DRAW-113 · شروح بخط اليد مع أسهم مرسومة · Handwritten annotations with arrows · 👁 شوهد في فيديو
- **ماذا / what:** handwritten font notes typed on, curved SVG arrow drawn with stroke-dashoffset pointing to subject; red for wrong, blue for right
- **أرقام / params:** arrow draw 300 ms; note 25 ms/char; blue #2f7bf5, red #ef3b55
- **الدليل / proof:** `style:pm-chatgptastra-0d95c7`

#### DRAW-114 · كتابة عنوان بخط يدوي · Script headline write-on · 👁 شوهد في فيديو
- **ماذا / what:** Script font text revealed by left-to-right mask wipe with gold gradient fill and soft shadow
- **أرقام / params:** 800 ms linear-ish, gradient #f5c542->#d8a664
- **الدليل / proof:** `style:pm-deebeeeff-50fcd0`

#### DRAW-115 · خيوط تعليق · Hang strings · 👁 شوهد في فيديو
- **ماذا / what:** Thin vertical lines draw down then word drops on spring
- **أرقام / params:** 1px gold
- **الدليل / proof:** `style:pm-gdgtify-287ddf`

#### DRAW-116 · رسم خط نيون برأس متوهج · Neon line draw with glowing head · 👁 شوهد في فيديو
- **ماذا / what:** stroke-dashoffset reveal of a smooth curve in lime; a grey offset ghost copy trails; a glowing dot rides the leading end with value label
- **أرقام / params:** stroke 4 px #d4ff3a, glow 12 px, draw 1 s
- **الدليل / proof:** `style:pm-ghinaiya-nirmal-5d8fec`

#### DRAW-117 · خط حبر مهتز يدوي · Hand-inked stroke wobble · 👁 شوهد في فيديو
- **ماذا / what:** offset stroke points with small noise (±0.6 px) and slight width variation to mimic ink on paper
- **أرقام / params:** stroke 4-6 px #1a1a18
- **الدليل / proof:** `style:pm-hbcoop-de365c`

#### DRAW-118 · رسم خطي استعاري · Line-art metaphor illustration · 👁 شوهد في فيديو
- **ماذا / what:** simple outline drawing (copier/printer) that outputs copies sliding out, a red blot spreading to show an error copied everywhere, with an italic red serif aside
- **أرقام / params:** stroke 2 px charcoal, pages slide 600 ms
- **الدليل / proof:** `style:pm-henkvaness-0e06af`

#### DRAW-119 · طبقة تعليقات بخط اليد · Handwritten annotation layer · 👁 شوهد في فيديو
- **ماذا / what:** script font text revealed per letter (~30 ms) plus SVG arrow paths drawn with stroke-dashoffset; blue for correct, red for wrong; strikethrough line drawn over wrong statement
- **أرقام / params:** Kalam/Caveat 600, arrow draw 250 ms
- **الدليل / proof:** `style:pm-himanshutwtxs-5f4b43`

#### DRAW-120 · خط يمتد إلى العنوان · Underline sweep to heading · 👁 شوهد في فيديو
- **ماذا / what:** red line scaleX 0→1 easeOut 500ms then heading unblurs
- **الدليل / proof:** `style:pm-ho-ba-f3f0e9`

#### DRAW-121 · كتابة يدوية بقلم ماركر ترسم نفسها · Marker handwriting draw-on · 👁 شوهد في فيديو
- **ماذا / what:** Handwriting font converted to paths (or single-line font), animate stroke-dashoffset per glyph; curved arrow drawn first then label
- **أرقام / params:** ~40 ms per glyph, arrow 300 ms, colours in accent ink
- **الدليل / proof:** `style:pm-ik-builds-b8bdcf`

#### DRAW-122 · رابط محاط بدائرة يدوية · Hand-circled CTA · 👁 شوهد في فيديو
- **ماذا / what:** Draw a wobbly ellipse around the URL with stroke-dashoffset after the tagline lands
- **أرقام / params:** ellipse 400 ms, accent rust colour, stroke 2 px
- **الدليل / proof:** `style:pm-ik-builds-b8bdcf`

#### DRAW-123 · تحويل النص إلى رسم يدوي · Text-to-doodle diagram · 👁 شوهد في فيديو
- **ماذا / what:** SVG paths with stroke-dashoffset draw-on, handwritten labels fade in after each path
- **أرقام / params:** each path 400-800ms, stagger 150ms
- **الدليل / proof:** `style:pm-itisrazak-3ad902`

#### DRAW-124 · شريط خطوط فنية · Line-art ribbon · 👁 شوهد في فيديو
- **ماذا / what:** parametric curves drawn as many thin strokes on yellow
- **أرقام / params:** stroke 1px
- **الدليل / proof:** `style:pm-itsuki-dev-10942d`

#### DRAW-125 · رسم مسطح بحدود حبر · Ink-outline flat illustration · 👁 شوهد في فيديو
- **ماذا / what:** Flat fills with 3-4px dark ink strokes slightly uneven, muted warm palette, subtle paper grain overlay
- **أرقام / params:** stroke #2a2a2a, grain 6% opacity
- **الدليل / proof:** `style:pm-jake11moran-a269c4`

#### DRAW-126 · شرارة ترسم المحيط · Outline spark trace · 👁 شوهد في فيديو
- **ماذا / what:** bright dot travels along SVG path with stroke-dashoffset trailing
- **أرقام / params:** 1.5 s ease-in-out
- **الدليل / proof:** `style:pm-jazzen-chen-4542ae`

#### DRAW-127 · رسم أيقونة خطية · Line icon draw-on · 👁 شوهد في فيديو
- **ماذا / what:** SVG stroke-dashoffset draw of circuit/chart/target icons
- **أرقام / params:** ~600 ms
- **الدليل / proof:** `style:pm-kangaroohere-b10f8d`

#### DRAW-128 · قلم ماركر يكتب بخط اليد · Marker-pen handwriting reveal · 👁 شوهد في فيديو
- **ماذا / what:** SVG paths of handwritten letters revealed with stroke-dashoffset in writing order; a marker image follows getPointAtLength of the active path, tilted ~30°
- **أرقام / params:** ~120 ms per letter, stroke 3 px #1f1d19
- **الدليل / proof:** `style:pm-lemomo-ai-0d9cff`

#### DRAW-129 · ملاحظة بخط اليد داخل إطار · Boxed handwritten callout · 👁 شوهد في فيديو
- **ماذا / what:** rough rounded rectangle path (jittered) draws first in accent orange, then handwritten words appear inside
- **أرقام / params:** box 400 ms + text 600 ms, #d17c55
- **الدليل / proof:** `style:pm-lemomo-ai-0d9cff`

#### DRAW-130 · رسم خط الحبر · Ink stroke draw-on · 👁 شوهد في فيديو
- **ماذا / what:** SVG path dashoffset 1->0 with ease-in-out
- **أرقام / params:** ~800 ms
- **الدليل / proof:** `style:pm-lexnlin-038035`

#### DRAW-131 · خط تحتي يرسم · Underline draw accent · 👁 شوهد في فيديو
- **ماذا / what:** stroke path under word dashoffset
- **أرقام / params:** 0.4 s
- **الدليل / proof:** `style:pm-m1n9-k7-ff9ab9`

#### DRAW-132 · خط نبض يتحول لشعار · Heartbeat stroke to logo · 👁 شوهد في فيديو
- **ماذا / what:** SVG path of flat line with one ECG spike; animate stroke-dashoffset 1 -> 0 over ~1 s with ease-in-out, add duplicate path with blur 8-12 px for glow; later reuse the spike as the logo glyph in an app-
- **كيف / how:** SVG path of flat line with one ECG spike; animate stroke-dashoffset 1 -> 0 over ~1 s with ease-in-out, add duplicate path with blur 8-12 px for glow; later reuse the spike as the logo glyph in an app-icon tile
- **أرقام / params:** stroke 3 px #cfe0ff, glow #4f8fe6 at 60%
- **الدليل / proof:** `style:pm-marouanegazouzi-6071d5`

#### DRAW-133 · تحويل خط اليد إلى نص · Handwriting-to-transcript demo · 👁 شوهد في فيديو
- **ماذا / what:** lined sticky note with script font revealed line by line (mask left->right), then arrow and typed transcript card below
- **أرقام / params:** line reveal 500 ms each
- **الدليل / proof:** `style:pm-mehul4795-4a7007`

#### DRAW-134 · شريط مخطط يرسم · Striped ribbon draw-on · 👁 شوهد في فيديو
- **ماذا / what:** 3 parallel offset strokes red/white/blue with dashoffset animation
- **أرقام / params:** 1.5 s
- **الدليل / proof:** `style:pm-mrtanviir-132457`

#### DRAW-135 · ارتعاش خط الرصاص بـ12 إطاراً · Graphite line boil at 12 fps · 👁 شوهد في فيديو
- **ماذا / what:** Render every stroke with per-frame random offset seeded by floor(t*12); hold frames on twos; grey #3a3c3c 2px rough strokes
- **أرقام / params:** jitter ±1.2px, roughness 1.5, fps 12
- **الدليل / proof:** `style:pm-nikolajankovic-ce4ff4`

#### DRAW-136 · خط نبض قلب بحلقات · ECG pulse with ring markers · 👁 شوهد في فيديو
- **ماذا / what:** Orange heartbeat polyline draws left->right with glow; at each beat a white dot appears with an expanding faint ring and warm halo
- **أرقام / params:** stroke 2px #e8603a; ring 0->60px 800ms
- **الدليل / proof:** `style:pm-nolkeeg-bf062e`

#### DRAW-137 · خط يُرسم تحت السؤال · Underline draw under question · 👁 شوهد في فيديو
- **ماذا / what:** after headline lands, a thick black rule draws left-to-right under the last line
- **أرقام / params:** 4 px, 400 ms ease-out
- **الدليل / proof:** `style:pm-palashbagchi11-0a4b6b`

#### DRAW-138 · شطب بخربشة ثم إعادة كتابة · Scribble strike-through rewrite · 👁 شوهد في فيديو
- **ماذا / what:** draw a looping magenta scribble path over the old words via stroke-dashoffset, fade old words to 50%, then slide the new line up below
- **أرقام / params:** scribble 300 ms, new line 250 ms easeOutBack
- **الدليل / proof:** `style:pm-paulo-kombucha-96431c`

#### DRAW-139 · مسار متموج · Squiggle path see→act · 👁 شوهد في فيديو
- **ماذا / what:** SVG path dashoffset between two nodes
- **الدليل / proof:** `style:pm-reflex-cloud-72ffe5`

#### DRAW-140 · رسم خط الشعاع لصورة ظلية · Beam draw-on silhouette · 👁 شوهد في فيديو
- **ماذا / what:** SVG path of logo shape; stroke-dashoffset from length to 0 over ~2 s with bright dot at path head (getPointAtLength), plus slight jitter
- **أرقام / params:** head dot radius 4px with glow 20px
- **الدليل / proof:** `style:pm-rneayan-ea6129`

#### DRAW-141 · حدود مرسومة باليد · Hand-drawn wobble outline · 👁 شوهد في فيديو
- **ماذا / what:** jittered SVG paths, 2-3px dark stroke, flat pastel fill
- **الدليل / proof:** `style:pm-ror-fly-9950f1`

#### DRAW-142 · علامات الإثارة: سهم ودائرة حمراء · Clickbait marks: red arrow and circle · 👁 شوهد في فيديو
- **ماذا / what:** Curved red 3D arrow pointing at face and red ring drawn around head via stroke-dashoffset; yellow Impact text with black stroke 'NO WAY?!'
- **أرقام / params:** circle draw 300 ms, arrow slide 250 ms
- **الدليل / proof:** `style:pm-sab8a-364a5a`

#### DRAW-143 · قوس متوهج يُرسم في الختام · Glowing draw-on closing arc · 👁 شوهد في فيديو
- **ماذا / what:** SVG path (smile arc) stroke-dashoffset 100%->0 with drop-shadow glow, title blurred behind, countdown hits 00:00
- **أرقام / params:** stroke 3px #ff4a20, glow 8px
- **الدليل / proof:** `style:pm-samaote-5e2fc2`

#### DRAW-144 · خط حلزوني يرسم نفسه · Loop line draw-on · 👁 شوهد في فيديو
- **ماذا / what:** SVG path with loops, dashoffset 1→0 over 1.2s
- **الدليل / proof:** `style:pm-samuel-spitz-974923`

#### DRAW-145 · إناء بخط يد مرتعش · Wobbly hand-drawn container · 👁 شوهد في فيديو
- **ماذا / what:** SVG path with small per-vertex noise (1-2 px) and a slightly uneven 3 px dark-brown stroke; inner wall highlight stripe at 20% white
- **أرقام / params:** optionally re-jitter every 3-4 frames for boil
- **الدليل / proof:** `style:pm-sarut0bisasuke-cefa43`

#### DRAW-146 · أقواس تحريك دائرية · Stir orbit arcs · 👁 شوهد في فيديو
- **ماذا / what:** two thin elliptical arcs around the glass drawn/rotated to suggest stirring while a straw sits diagonally in the glass
- **أرقام / params:** arc rotation ~1 turn/s, stroke 2 px
- **الدليل / proof:** `style:pm-sarut0bisasuke-cefa43`

#### DRAW-147 · منحنى فكرة يُرسم · Thought curve draw-on · 👁 شوهد في فيديو
- **ماذا / what:** SVG path with loop, dashoffset animate, endpoint dot
- **أرقام / params:** 600 ms
- **الدليل / proof:** `style:pm-souravbhar871-61f424`

#### DRAW-148 · رسم بالماركر يتبع رأس الخط · Marker-follows-stroke draw-on · 👁 شوهد في فيديو
- **ماذا / what:** animate stroke-dashoffset of each SVG path; place a marker sprite at getPointAtLength(progress) rotated ~-40°, swap its cap colour with the ink colour
- **أرقام / params:** speed ~400-600 px/s; text paths ~0.6-1.5 s per line
- **الدليل / proof:** `style:pm-tak3sh8-be5012`

#### DRAW-149 · رسم شبكة سلكية · Wireframe mesh draw · 👁 شوهد في فيديو
- **ماذا / what:** edges stroke-dashoffset staggered
- **أرقام / params:** ~1.5 s total
- **الدليل / proof:** `style:pm-tdinh-me-815acb`

#### DRAW-150 · خط تحت الكلمة يُرسم · Underline swoosh draw-on · 👁 شوهد في فيديو
- **ماذا / what:** hand-drawn curved SVG stroke under the accent word, stroke-dashoffset animates to 0
- **أرقام / params:** stroke 4px brand blue, 300 ms
- **الدليل / proof:** `style:pm-thismacapital-dfba20`

#### DRAW-151 · شريط مخطط مرسوم · Striped ribbon stroke · 👁 شوهد في فيديو
- **ماذا / what:** 3 stacked strokes red/white/blue draw along curve
- **أرقام / params:** width 30px
- **الدليل / proof:** `style:pm-umangratani-57f86a`

#### DRAW-152 · خط ماركر حر يُرسم بالتدريج · Progress-revealed freehand marker stroke · 👁 شوهد في فيديو
- **ماذا / what:** sample path with getPointAtLength (clamp to L - 1e-4 to avoid null), pass points up to eased progress into getStroke(simulatePressure) and fill the outline polygon in marker colour
- **أرقام / params:** size 8-10, thinning 0.6, easeInOut per stroke
- **الدليل / proof:** `style:whiteboard`

#### DRAW-153 · ماركر بلا يد يتبع رأس الخط · Hand-less marker tip follower · 👁 شوهد في فيديو
- **ماذا / what:** marker sprite (body + coloured cap + 'MARKER' label) positioned/rotated at the stroke tip; recolour cap to the active stroke; lift between strokes with growing shadow
- **أرقام / params:** angle ~-35deg, lift 200 ms
- **الدليل / proof:** `style:whiteboard`

#### DRAW-154 · تمييز النص بقلم التحديد · Marker highlight modes · 📄 موصوف
- **ماذا / what:** Five deterministic emphasis styles on words: highlight sweep, hand circle, burst lines, scribble underline, sketch-out strike.
- **كيف / how:** Highlight: absolute span inset -6px, scaleX 0->1 0.5s power2.out; circle: 3px border ellipse back.out(1.7) 0.6s; burst: 12 lines at 30deg steps with lengths 40-80px, stagger 0.03; scribble: wavy SVG path stroke 3px round caps drawn with dashoffset. Remotion alt: @remotion/rough-notation <Highlight/Circle/Underline/StrikeThrough/CrossedOff/Box/Bracket progress=...>.
- **أرقام / params:** burst 12 lines 40-80px; stagger 0.03s
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/css-patterns.md` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/text-highlights.md`

#### DRAW-155 · رسم المسار تدريجيًا · SVG stroke draw-on · 📄 موصوف
- **ماذا / what:** A path traces itself like a pen stroke by animating dash offset from full length to zero.
- **كيف / how:** len = path.getTotalLength(); set strokeDasharray=len, strokeDashoffset=len; tl.to(path,{strokeDashoffset:0, duration:0.7, ease:'power2.out'}); stroke-linecap round; works for arrows, connectors, logos, underlines.
- **أرقام / params:** 0.7s power2.out
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/css-patterns.md`

#### DRAW-156 · أسلوب رسومات السبورة البيضاء · Whiteboard-doodle illustration style · 📄 موصوف
- **ماذا / what:** Marker-doodle look for story illustrations: warm cream paper (not pure white), bold slightly wobbly navy/black outlines, loose hatched marker fills that overshoot the lines, 3-5 bright primaries per scene, one exaggerated protagonist, uncoloured faceless white mini-silhouettes for crowds, oversized …
- **كيف / how:** For generation, reuse a fixed CHARACTER sentence verbatim across all scene prompts (models have no memory); split stories into 2-5 scenes (intro -> problem -> solution). Procedurally reproducible here with SVG jittered strokes + hatch patterns and draw-on stroke-dashoffset animation.
- **أرقام / params:** 3-5 colours; 2-5 scenes
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2421-akbun-draw-storytellingimage/SKILL.md`

#### DRAW-157 · S14 خطوط مرسومة · S14 Drawn linework · 📄 موصوف
- **ماذا / what:** Simple lines, marks and signs, white space; path drawing, emphasis circles, line turning into shape. Focused explanation with light assets; paths need tuning and Arabic letter joins must never break.
- **كيف / how:** SVG stroke-dasharray/dashoffset draw-on with slight jitter for a hand feel; text revealed by masks, not re-drawn; KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg)
- **أرقام / params:** cost low-medium; MG-015 MG-021 MG-035 MG-054 MG-081 MG-086 MG-090 MG-120
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### DRAW-158 · MG-015 نص يكتب بقناع فرشاة · MG-015 Brush-mask write-on (right to left) · 📄 موصوف
- **ماذا / what:** A brush stroke reveals a finished phrase from right to left - a warm handwritten opening.
- **كيف / how:** 0-0.5 s stroke starts, 0.5-2.5 s reveal, 2.5-4 s read. Animate a thick SVG stroke (dashoffset) used as a mask over correctly typeset text; this is a reveal, not generating Arabic glyphs from arbitrary paths.
- **أرقام / params:** 4 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### DRAW-159 · MG-074 خط أفق يبني مدينة · MG-074 Skyline line becomes the city · 📄 موصوف
- **ماذا / what:** One line draws symbolic buildings and then dissolves into city footage aligned on the horizon.
- **كيف / how:** 0-1 line, 1-4 draw, 4-7 match dissolve to footage; trim-path drawing then a dissolve matched to the horizon; draw generic or licensed landmarks only.
- **أرقام / params:** 7 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-cinematic-titles.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### DRAW-160 · MG-105/107 خربشة توضيحية ومسح قلم تمييز · MG-105/107 Doodle annotations and highlighter swipe · 📄 موصوف
- **ماذا / what:** Arrow, circle and underline are drawn on top of the referenced object (MG-105); a semi-transparent marker band runs under a short sentence and leaves colour (MG-107).
- **كيف / how:** MG-105: 0-1 shot, 1-4 marks, 4-6 read; stroke/trim-path drawing with tracking if needed; each mark explains one point and never covers the subject. MG-107: 0-1 text, 1-2 highlight, 2-4 read; start the swipe from the RIGHT for Arabic and check contrast. Local: jittered hand-drawn SVG paths, multiply-blended highlight rect.
- **أرقام / params:** 6 s / 4 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-collage-textures.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### DRAW-161 · مشهد قلم رصاص هادئ · Quiet pencil scene · 📄 موصوف
- **ماذا / what:** Calm illustration grammar: warm cream paper, the top two-thirds left empty, 1-3 small grey pencil subjects on a low ground line, a figure seen from behind, and exactly one desaturated teal prop where the meaning lands; the subject changes, the style never does.
- **كيف / how:** Either an image-model prompt (external) or SVG with pencil texture (feTurbulence + feDisplacementMap) and slow draw-on in KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg); suits reflective narration B-roll and end cards.
- **أرقام / params:** 1-3 subjects; 1 teal accent; top 2/3 empty
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2419-akbun-draw-quiet-pencil/SKILL.md`

#### DRAW-162 · حزمة أسلوب من مقطع مرجعي · Style pack from reference clip · 📄 موصوف
- **ماذا / what:** Turn a traced reference animation into a statistics-only style pack (palette ink/paper/tone ramp, knobs, p10/p50/p90 bands) and check new scenes against it — never store source frames.
- **كيف / how:** animation plugin learn.py (unreviewed; reimplement): measure edge roughness, solidity, palette; store style.json bands.
- **أرقام / params:** p10/p50/p90
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9355-learn-style`

#### DRAW-163 · رسم المسار ذاتيًا · SVG path draw-on (stroke-dashoffset) · 📄 موصوف
- **ماذا / what:** A stroke appears to be traced by a pen by animating its dash offset from full length to zero.
- **كيف / how:** Inline SVG in HTML/GSAP or Remotion: set stroke-dasharray=stroke-dashoffset=path.getTotalLength(), tween offset to 0; fill none, round caps. Fill can fade in after the stroke completes.
- **أرقام / params:** duration 0.5-0.9s, ease power2.out, stroke-linecap round
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### DRAW-164 · ارتعاش الخط المتعمد · Line boil (deliberate redraw jitter) · 📄 موصوف
- **ماذا / what:** Hand-drawn animation vibes come from lines that re-wobble on 2s or 3s; the animation plugin measures boil as a style statistic.
- **كيف / how:** Re-seed rough/noise displacement every 2 frames (on twos at 24fps) or 3; keep amplitude 0.5-1.5px at 1080p. Measured per style pack in learn-style.
- **أرقام / params:** update every 2-3 frames; amp 0.5-1.5px
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9355-learn-style` · `kosif-atlas/skills/2414-animation/9357-rotoscope`

#### DRAW-165 · خريطة مسار مرسومة باليد · Hand-drawn route sketch map · 📄 موصوف
- **ماذا / what:** A crayon-textured flat illustration of a trip route: numbered stops on cream paper, colored route lines, no invented roads.
- **كيف / how:** Palette: paper #FBF6E9, confirmed path #B9AEA6, routes #8CC63F / #8E6BB0 / #F2A03D, greenery #DDE8B5 #7FB241 #3F6B2A, water #A9CDE8, ink #2B2B2B, panel #F7F1DC; 3:4 frame; numbers only as text; if no direction info, flow stops top-to-bottom. Can be an image-generation prompt or drawn in SVG with a rough stroke filter and animated draw-on.
- **أرقام / params:** aspect 3:4; 3 route colors
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2422-akbun-draw-travel-blog/SKILL.md` · `kosif-atlas/skills/2790-work/11181-draw-excalidraw/references/visual-patterns.md`

#### DRAW-166 · إعادة رسم مخرجات Canva متجهياً · Canva render -> hand vector recreation · 📄 موصوف
- **ماذا / what:** When a generated raster cannot be downloaded or must stay sharp at any size, recreate it as a compact SVG (sky 2.6 KB, ram emblem, valley dusk, ornament) and score it against the render.
- **كيف / how:** Generate in Canva (media ids recorded), then hand-author SVG with gradients/filters; Jev scored Canva render 3.84/4 vs vector 3.79/4 for the emblem.
- **الدليل / proof:** `kosif-earth-ci-fork/docs/design/KOSIF-LUXE.md` · `kosif-earth-ci-fork/docs/rebuild/DESIGN_SYSTEM.md`

#### DRAW-167 · أسلوب الرسم اليدوي · Hand-drawn / whiteboard style (requested, not built) · 📄 موصوف
- **ماذا / what:** Doodle, whiteboard, chalkboard and plotter styles are offered and a 'hand-drawn-shapes' scene type is planned, but no stroke draw-on renderer exists; roadmap v0.5 promises real stroke animation.
- **كيف / how:** Today: write bespoke SVG/Canvas stroke-dashoffset scenes or route to another engine.
- **الدليل / proof:** `fastify-motion-bro/README.md:52-56` · `fastify-motion-bro/scripts/planner.mjs:21` · `fastify-motion-bro/docs/ROADMAP.md:6`

#### DRAW-168 · أيقونات حسب المعنى · Meaning-matched line icons (12) · 📄 موصوف
- **ماذا / what:** Stroke-only symbols drawn on above a line when its meaning matches, breathing on the beat; numbers count up instead.
- **كيف / how:** verse.py sets line.motif {kind, t, end, value}; verse.html ICONS + drawPath per stroke (0.7 s, 0.06 s stagger).
- **أرقام / params:** icons: sun, moon, heart, clock, money, trophy, road, question, check, home, rain, light; 200x200 box, stroke 5, accent; count motif 150 px
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/verse.html:258`

#### DRAW-169 · قالب موشن: كشف الشعار بالرسم · Motion template: Logo reveal (pen draw-on) (logo-reveal) · 📄 موصوف
- **ماذا / what:** Arabic-first, deterministic motion template 'logo-reveal' that becomes an editable project with its parameters kept in template.json.
- **كيف / how:** Projects tab → 'قالب موشن…' or recipe template (new NAME --template logo-reveal --set key="value" … --size 1080x1920 --seconds N), or MCP kosif_project_create {kind:'template', template:'logo-reveal', params}; GET /api/templates lists params with defaults.
- **أرقام / params:** logo SVG path drawn by pen, then filled, then name and tagline; 6 s; name KOSIF, tagline 'حركة لها معنى', default hexagon path in viewBox 120×136, accent #E7B65A, bg #0f1a2b → #06101c
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:14` · `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:48` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:127`

#### DRAW-170 · قالب موشن: نقاط بعلامات صح مرسومة · Motion template: Bullet list with drawn ticks (bullet-list) · 📄 موصوف
- **ماذا / what:** Arabic-first, deterministic motion template 'bullet-list' that becomes an editable project with its parameters kept in template.json.
- **كيف / how:** Projects tab → 'قالب موشن…' or recipe template (new NAME --template bullet-list --set key="value" … --size 1080x1920 --seconds N), or MCP kosif_project_create {kind:'template', template:'bullet-list', params}; GET /api/templates lists params with defaults.
- **أرقام / params:** title then up to 6 items appearing with a drawn check each; 8 s; title 'ثلاث خطوات', items 'خطّط|نفّذ|راجع', accent #5BD1A5, bg #10233a → #071321
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:14` · `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:58` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:127`

#### DRAW-171 · محوّل مسارات SVG إلى نقاط · SVG path sampler (M/L/H/V/C/Q/T/Z) · 📄 موصوف
- **ماذا / what:** Pure-Python sampling of SVG path data (absolute/relative, cubic and quadratic curves) into polylines — reusable for draw-on/stroke animations.
- **كيف / how:** desktop._svg_paths(d) -> list of point lists; desktop._shape_paths(shapes); desktop._fit_tf(paths, box, margin, viewbox) to scale into a frame. Lift the functions into a render(t) draw-on by revealing points up to t.
- **أرقام / params:** curves sampled (not chords); closed paths return to start
- **الدليل / proof:** `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/desktop.py:1032` · `kosif-one/tools/kosif-omni/mcp-server/tests/test_desktop.py:259`

#### DRAW-172 · الخط الذي يرسم نفسه · Self-drawing Line Art · 📄 موصوف
- **ماذا / what:** stroke-dashoffset easeInOut with staggered durations, then fill fades in.
- **كيف / how:** Copy style sheet section into DESIGN.md, then build via claude-animation-studio render(t).
- **أرقام / params:** stroke #111 or #F4F7FF; Changa 600; never draw all paths at once
- **الدليل / proof:** `100-superskills/skills/trend-animation-styles/references/styles.md`

#### DRAW-173 · سماكات الخطوط المرسومة · Stroke weight tokens · 📄 موصوف
- **ماذا / what:** Primary path 6 px round/round, secondary 3 px, grid 1.5 px butt/miter at 1080 width.
- **كيف / how:** STYLE.md §4.3
- **الدليل / proof:** `kosif-tool/templates/STYLE.md`

#### DRAW-174 · عائلة سماكات القلم · Pen weight family and ink · 📄 موصوف
- **ماذا / what:** One pen weight family, one ink + one highlight; chalkboard inverts.
- **أرقام / params:** e.g. 4 and 8 px
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:15`

#### DRAW-175 · عدم الكمال المقصود · Deliberate stroke imperfection · 📄 موصوف
- **ماذا / what:** Slight wobble, round caps, corner overshoot; objects from few strokes.
- **أرقام / params:** 1–2 px wobble; 5–30 strokes per object
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:16-17`

#### DRAW-176 · ترتيب الرسم البشري · Human draw order · 📄 موصوف
- **ماذا / what:** Outline, details, fill/hatching; RTL for Arabic writing.
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:24`

#### DRAW-177 · سرعة القلم والرفع · Pen speed and lifts · 📄 موصوف
- **ماذا / what:** Constant-ish pen speed with per-stroke easing and pauses between strokes; fills after.
- **أرقام / params:** 800–1400 px/s; lift 60–120 ms; hatching 2000 px/s or 300 ms wipe
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:25-26`

#### DRAW-178 · ارتعاش الخط (boil) · Line boil · 📄 موصوف
- **ماذا / what:** Swap slightly different stroke versions on twos.
- **أرقام / params:** 3 versions every 2–3 frames
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:28`

#### DRAW-179 · إيقاع السبورة وتحريكها · Whiteboard rhythm and pan · 📄 موصوف
- **ماذا / what:** Draw while narrating, hold at sentence end, slide to fresh board space.
- **أرقام / params:** hold 1.5–2 s; pan 1 board-width in 800 ms ease-in-out
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:29` · `kosif-tool/playbooks/hand-drawn.md:46`

#### DRAW-180 · جمالية البلوتر · Plotter aesthetic · 📄 موصوف
- **ماذا / what:** Constant pen speed, no easing, optional visible pen-up travel.
- **أرقام / params:** pen-up lines at 10%
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:30`

#### DRAW-181 · وصفة ارسم وسمِّ · Draw-and-label recipe · 📄 موصوف
- **ماذا / what:** Outline, details, highlight fill, handwritten label, hold with hand exit.
- **أرقام / params:** 0–900 outline; 900–1300 details; 1300–1600 fill; 1600–2300 label; 2300–4000 hold
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:36-44`

#### DRAW-182 · معادلة طباشير مع غبار · Chalkboard formula with dust puffs · 📄 موصوف
- **ماذا / what:** Chalk strokes with dusty texture; small dust puff on each completed term.
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:50`

#### DRAW-183 · شرح سبورة من التعليق الصوتي · Whiteboard explainer from narration · 💡 فكرة
- **ماذا / what:** Each narration sentence triggers its Excalidraw-style element drawing on, with a camera pan to the next region.
- **كيف / how:** Build scene as SVG with rough strokes; per element draw-on start = sentence onset; camera via viewBox tween.
- **أرقام / params:** pan 0.6-0.8s
- **الدليل / proof:** `kosif-atlas/skills/2790-work/11181-draw-excalidraw` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/text-highlights.md`

#### DRAW-184 · قص الرسومات من الورق · Sketch cut-out lift with alpha mask · 💡 فكرة
- **ماذا / what:** Scanned drawings are lifted off a photographed sketchbook page via alpha masks and animated as cut-outs.
- **كيف / how:** PNG alpha cut-outs; only translate, rotate ±12°, uniform scale; never recolour or trace.
- **أرقام / params:** rotate max ±12°
- **الدليل / proof:** `style:pm-abderrahmen-g-9e8ed0`

#### DRAW-185 · ارتعاش الخطوط اليدوي · Line boil at 8 fps · 💡 فكرة
- **ماذا / what:** Hand-drawn outline wobble by cycling scan variants or jitter, held on threes.
- **كيف / how:** Cycle 2-3 variants or 2 px jitter, hold 3 frames at 24 fps.
- **أرقام / params:** 8 fps, 2 px
- **الدليل / proof:** `style:pm-abderrahmen-g-9e8ed0`

#### DRAW-186 · تظليل بالقلم · Highlighter sweep · 💡 فكرة
- **ماذا / what:** Highlighter sweep isolates key sentences.
- **كيف / how:** Rect scaleX behind text.
- **الدليل / proof:** `style:pm-itisrazak-3ad902`

#### DRAW-187 · حبوب بأيقونات مرسومة · Icon stroke draw-on pills · 💡 فكرة
- **ماذا / what:** Benefit pills slide in; icons stroke-draw.
- **كيف / how:** dashoffset.
- **أرقام / params:** 350 ms; 120 ms stagger
- **الدليل / proof:** `style:pm-l3d1c-0e35a3`

#### DRAW-188 · يدان خطيتان تطلقان · Line-art hand release metaphor · 💡 فكرة
- **ماذا / what:** Outlined hands release an object that keeps moving alone.
- **أرقام / params:** 900 ms cubic-bezier(0.33,1,0.68,1); 120 ms hold then linear
- **الدليل / proof:** `style:pm-robvjourney-ce3e1a`

#### DRAW-189 · سبورة بسرعة قلم ثابتة · Constant pen-speed whiteboard · 💡 فكرة
- **ماذا / what:** Strokes revealed linearly at pen speed, synced to narration.
- **كيف / how:** SVG dashoffset; duration=length/speed.
- **أرقام / params:** 500-700 px/s; lead <=150 ms
- **الدليل / proof:** `style:pm-tak3sh8-be5012`

#### DRAW-190 · مسح بالممحاة · Eraser-shape wipe · 💡 فكرة
- **ماذا / what:** 400 ms wipe following eraser shape
- **الدليل / proof:** `style:pm-tak3sh8-be5012`

## إضافات من Cinematic Director PRO v5

_مستخلصة من حزمة المالك KOSIF Claude Cinematic Director PRO v5 (انظر [cinematic-director-pro.md](../cinematic-director-pro.md)). مسارات الدليل `owner-upload:` تشير إلى ملفات داخل أرشيف المالك، لا إلى هذا المستودع._

#### DRAW-P01 · قصة الخط الواحد المستمر حتى الشعار · Continuous-line logo story (one stroke → three beats → wordmark loop) · ✅ مُثبت هنا / proven here
- **ماذا / what:** خط واحد لا ينقطع يمر بثلاث محطات مرقّمة ثم يلتف حول الشعار، مع صوت مولّد بالكود. / One unbroken line travels through three numbered beats and closes into a loop around the wordmark, with code-synthesised sound.
- **كيف / how:** 13 waypoints interpolated 18 steps each; drawn length = smoothstep(t/4.1); beat dots grow with smoothstep((t−(0.9+0.85k))/0.55) and their labels (01 CAPTURE, 02 CONNECT, 03 RESURFACE) appear at the same instants; from 4.25 s an ellipse (rx 100, ry 42) draws over 1.1 s around the wordmark. Editorial palette: paper (246,241,230), ink (31,36,34), one accent (213,70,48), 6 px stroke, pen-tip dot. Audio generated in NumPy (see BEAT-P01). Re-ran here: 6.000 s, 360×640, 24 fps, H.264 + AAC 96k. **أرقام / params:** 360×640 · 24 fps · 6 s · draw 4.1 s · beats at 0.9/1.75/2.6 s · loop 4.25–5.35 s
- **الرخصة / license:** owner package (own work)
- **الدليل / proof:** `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/tools/render_continuous_line.py` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/examples/Continuous_Line_Logo_Story.mp4` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/integrations/kosif-see/INTEGRATION_REPORT.json`
