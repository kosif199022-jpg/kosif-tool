# التوقيت والإيقاع والتسهيل — Easing, timing & rhythm

> فصل مُجمَّع آليًا من 346 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **332 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 332 powers deduplicated by name from 346 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 28 · 🟢 جاهز 62 · 📦 بأمر تثبيت 77 · 👁 شوهد في فيديو 78 · 📄 موصوف 75 · 💡 فكرة 12

#### EASE-01 · مدة حسب المسافة · Distance-based duration (durFor) · ✅ مُثبت هنا
- **ماذا / what:** Move duration grows with travelled distance; camera moves clamped.
- **كيف / how:** MOTION.durFor(px, isCamera).
- **أرقام / params:** 0.35 s + 1.35 ms/px; camera clamp 0.6-2.4 s (600 px -> 1.16 s)
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:49` · `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### EASE-02 · تنعيم أثر المؤشر بأخذ عينات بالمسافة · Distance-sampled pointer trail easing · ✅ مُثبت هنا
- **ماذا / what:** Smooth a pointer or scripted finger by easing a 'head' toward the target each frame and laying trail points by distance travelled, not by time, so velocities are even and fast strokes do not tear.
- **كيف / how:** Per frame head += (target-head)*follow; push a point when distance > spacing; drop points older than life; convert to centered aspect-scaled coordinates. Plain JS, no deps.
- **أرقام / params:** follow 0.3/frame; spacing 0.01 field units; life 1.6s; 24 points
- **الدليل / proof:** `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail`

#### EASE-03 · رموز مدد الحركة · Motion duration tokens · ✅ مُثبت هنا
- **ماذا / what:** Four short duration steps used everywhere; a test bounds them to 120-420 ms.
- **كيف / how:** CSS vars --motion-instant/fast/medium/slow; reference them in transitions and keyframes.
- **أرقام / params:** instant 120ms; fast 160ms; medium 260ms; slow 420ms (at 30fps: 3.6/4.8/7.8/12.6 frames)
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:64` · `kosif-audit-pro/tests/motion-contract.test.mjs`

#### EASE-04 · منحنى التسهيل السينمائي · Cinematic ease curve · ✅ مُثبت هنا
- **ماذا / what:** Fast-out, long soft settle curve used for scene entries, sweeps and colour transitions.
- **كيف / how:** transition-timing-function: var(--ease-cinematic).
- **أرقام / params:** cubic-bezier(0.22, 0.8, 0.26, 1)
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:68`

#### EASE-05 · منحنى النابض المتجاوز · Spring overshoot ease curve · ✅ مُثبت هنا
- **ماذا / what:** Back-style overshoot (y2 > 1) for pops, indicator bars and icon swaps.
- **كيف / how:** transition/animation timing var(--ease-spring).
- **أرقام / params:** cubic-bezier(0.34, 1.35, 0.64, 1)
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:69`

#### EASE-06 · تتابع ظهور اللوحات · Staggered panel cascade · ✅ مُثبت هنا
- **ماذا / what:** Panels inside a scene enter in four delay groups so the eye reads title -> journey -> action -> metrics.
- **كيف / how:** keyframe kosif-scene-item on listed panel classes with animation-delay per group.
- **أرقام / params:** 420ms; 8px rise; delays 30 / 80 / 130 / 180 ms
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:600` · `kosif-audit-pro/app/globals.css:648`

#### EASE-07 · قاعدة التحريك بالتحويل والشفافية فقط · Transform/opacity-only motion rule · ✅ مُثبت هنا
- **ماذا / what:** Interactive surfaces must not use transition-all; animation is limited to transform and opacity (plus colour fades), and money values are never animated.
- **كيف / how:** Test asserts button/progress/tabs avoid transition-all and use explicit property lists.
- **الدليل / proof:** `kosif-audit-pro/tests/motion-contract.test.mjs` · `kosif-audit-pro/README.md`

#### EASE-08 · رموز الحركة: المنحنيات والمدد · Motion tokens (curves + durations) · ✅ مُثبت هنا
- **ماذا / what:** A small named set of easing curves and durations shared by every animated element: entering decelerates, leaving accelerates, feedback overshoots slightly.
- **كيف / how:** CSS custom properties in tokens.css; JS reads the same values.
- **أرقام / params:** --sk-ease cubic-bezier(.2,.8,.2,1); ease-out (expo-like) cubic-bezier(.16,1,.3,1); ease-in cubic-bezier(.55,0,1,.45); spring cubic-bezier(.34,1.56,.64,1); fast 160ms; panel 210ms; enter 420ms; stagger 45ms; feedback within 100ms
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/tokens.css:41` · `kosif-earth-ci-fork/docs/design/SQC-IDENTITY-ar.md`

#### EASE-09 · دخول متدرّج لكتل الشاشة · Staggered screen-enter choreography · ✅ مُثبت هنا
- **ماذا / what:** When a screen opens, its first ten blocks fade and rise in one after another; data-only re-renders do not replay it; vertical movement only so nothing scrolls sideways.
- **كيف / how:** SK.motion (ui/core/motion.js): on nav/render bus events set --sk-i index on each block, toggle #view.sk-enter, remove after 900ms; CSS @keyframes sk-view-in from opacity 0 translateY(10px); animation-delay calc(var(--sk-i)*var(--sk-motion-stagger)).
- **أرقام / params:** max 10 blocks; 420ms; 45ms stagger; ease-out (.16,1,.3,1); life 900ms
- **الدليل / proof:** `kosif-earth-ci-fork/ui/core/motion.js` · `kosif-earth-ci-fork/ui/ds/luxe.css:365` · `kosif-earth-ci-fork/tools/motion.test.mjs`

#### EASE-10 · مقسّم المشاهد التلقائي · Auto beat-count storyboard splitter · ✅ مُثبت هنا
- **ماذا / what:** Turns a brief into contiguous equal-length scenes whose count depends on total duration, with Arabic scene names and rotating visual types.
- **كيف / how:** makeStoryboard(): beats = 3 if d<=12 s, 5 if d<=35 s, else min(12, ceil(d/6)); start/end rounded to ms, last end = duration; names افتتاحية/الفكرة/التوضيح/التحول/النتيجة/الخاتمة; visual cycles kinetic-typography -> dynamic-infographic -> hand-drawn-shapes; sfx 'soft-whoosh'; fps 30.
- **أرقام / params:** 3/5/≤12 beats; ~6 s per beat for long films; fps 30
- **الدليل / proof:** `fastify-motion-bro/scripts/planner.mjs:14-24` · `fastify-motion-bro/tests/planner.test.mjs:5-6`

#### EASE-11 · خط زمني لمشهد 6 ثوانٍ · Six-second editorial scene timeline · ✅ مُثبت هنا
- **ماذا / what:** Every editorial scene is exactly 6 s: empty grid, kinetic spring entrance, floating hold, connected geometric exit.
- **كيف / how:** 0–0.5 s base (only grid + lines); 0.5–3.5 s entrance (spring, stagger 6–9 frames, word-by-word masked reveal); 3.5–4.7 s hold (sine float, 0.6° wobble, 4% push-in); 4.7–6.0 s exit (masked vertical text wipe, tracking expansion, easeOutCubic 1.3 s drop).
- **أرقام / params:** 0/0.5/3.5/4.7/6.0 s
- **الدليل / proof:** `fastify-motion-bro/scripts/viral-editorial.mjs:63-68` · `fastify-motion-bro/web/editorial.js:40` · `fastify-motion-bro/skills/viral-editorial/SKILL.md:11`

#### EASE-12 · تقدير المقاطع من سرعة الكلام · Word-pace clip estimator · ✅ مُثبت هنا
- **ماذا / what:** Derives total duration and clip count from word count when no timestamps are supplied.
- **كيف / how:** total = words / wps (fast 2.5, relaxed 1.8) or user duration; clips n=ceil(total/len) with len 8 or 10 s; words split evenly across clips.
- **أرقام / params:** fast 2.5 w/s; relaxed 1.8 w/s; ≤120 clips
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:89-100`

#### EASE-13 · خريطة كولاج 10 ثوانٍ · 10-second stop-motion collage beat map · ✅ مُثبت هنا
- **ماذا / what:** Five 2 s beats per clip with a new element every 1.5–2 s: two cutouts snap in; two more strike into new planes; string/sticker link; another torn detail; fresh element and hold.
- **كيف / how:** Prompt timeline from INVENTORY rotation (4 sets x 6 elements); neighbouring clips start with different pairs.
- **أرقام / params:** 0–2/2–4/4–6/6–8/8–10 s; 4–6 elements min
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/vox-history.mjs:14-19,50` · `fastify-motion-bro/tests/production-profiles.test.mjs:41-47`

#### EASE-14 · منحدرات السرعة · Speed ramps exact · ✅ مُثبت هنا
- **ماذا / what:** Speed ramps integrated exactly (log map), raised-cosine zoom, C1 continuity.
- **كيف / how:** python scripts/kmotion.py timeline clip speed ramp
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### EASE-15 · قالب العد التنازلي · Template: countdown · ✅ مُثبت هنا
- **ماذا / what:** Each second a number slams in, squashes, a ring runs down, camera shakes; then a double flash and the go word.
- **كيف / how:** python scripts/mtemplates.py new NAME --template countdown --set key=value ... [--seconds S --size WxH --fps F] -> projects/NAME/index.html (+ fonts, gsap, motion-kit); preview in a browser; render with motion.py render.
- **أرقام / params:** D = from + 1.6 s; from 5 (max 10), go 'انطلق', accent #FF6B6B, bg1 #1a1a2e, bg2 #0b0b14; number 26u scale 1.9->1 0.32 s; shake amp 5
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/motion/countdown.html` · `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:52`

#### EASE-16 · حركة الطبقة: ظهور ناعم · Layer entrance animation: Fade in/out (fade) · ✅ مُثبت هنا
- **ماذا / what:** Studio text/shape layer animation 'fade'.
- **كيف / how:** Inspector → الحركة = fade; overlay.animation='fade'; drawn in draw() with ease = 1 − (1 − clamp((t−start)/0.65))³ (easeOutCubic).
- **أرقام / params:** opacity follows the envelope only; envelope: fade-in over min(0.6 s, d/3), fade-out over min(0.4 s, d/3)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:75` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/model.mjs:12` · `100-superskills/skills/kosif-montage-motion/tests/studio/model.test.mjs`

#### EASE-17 · حركة الطبقة: صعود ناعم · Layer entrance animation: Soft rise (rise) · ✅ مُثبت هنا
- **ماذا / what:** Studio text/shape layer animation 'rise'.
- **كيف / how:** Inspector → الحركة = rise; overlay.animation='rise'; drawn in draw() with ease = 1 − (1 − clamp((t−start)/0.65))³ (easeOutCubic).
- **أرقام / params:** y offset (1−ease)·0.07·h, easing out over 0.65 s, plus the opacity envelope; envelope: fade-in over min(0.6 s, d/3), fade-out over min(0.4 s, d/3)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:75` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/model.mjs:12` · `100-superskills/skills/kosif-montage-motion/tests/studio/model.test.mjs`

#### EASE-18 · حركة الطبقة: تكبير ناعم · Layer entrance animation: Soft zoom (zoom) · ✅ مُثبت هنا
- **ماذا / what:** Studio text/shape layer animation 'zoom'.
- **كيف / how:** Inspector → الحركة = zoom; overlay.animation='zoom'; drawn in draw() with ease = 1 − (1 − clamp((t−start)/0.65))³ (easeOutCubic).
- **أرقام / params:** scale 0.65 + 0.35·ease (65% → 100%) over 0.65 s, plus the opacity envelope; envelope: fade-in over min(0.6 s, d/3), fade-out over min(0.4 s, d/3)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:75` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/model.mjs:12` · `100-superskills/skills/kosif-montage-motion/tests/studio/model.test.mjs`

#### EASE-19 · حركة الطبقة: ثابت · Layer entrance animation: Static (none) · ✅ مُثبت هنا
- **ماذا / what:** Studio text/shape layer animation 'none'.
- **كيف / how:** Inspector → الحركة = none; overlay.animation='none'; drawn in draw() with ease = 1 − (1 − clamp((t−start)/0.65))³ (easeOutCubic).
- **أرقام / params:** no envelope, full opacity for the layer's duration; envelope: fade-in over min(0.6 s, d/3), fade-out over min(0.4 s, d/3)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:75` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/model.mjs:12` · `100-superskills/skills/kosif-montage-motion/tests/studio/model.test.mjs`

#### EASE-20 · غلاف شفافية الطبقة · Overlay opacity envelope · ✅ مُثبت هنا
- **ماذا / what:** A trapezoid opacity curve for any timed layer: linear fade in, hold, linear fade out, scaled down for very short layers.
- **كيف / how:** animationProgress(o,t) = min(1, (t−start)/min(0.6, d/3), (end−t)/min(0.4, d/3)); 0 outside the window.
- **أرقام / params:** in 0.6 s, out 0.4 s, each ≤ d/3
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/model.mjs:12`

#### EASE-21 · رموز التسارع E · Easing tokens E (17 curves) · ✅ مُثبت هنا
- **ماذا / what:** A house set of cubic-bezier easing curves, one per motion role, usable as GSAP ease functions.
- **كيف / how:** MOTION.E.<name> inside any gsap tween ease; built by MOTION.bezier(x1,y1,x2,y2) (Newton solve, 8 iterations).
- **أرقام / params:** out(.16,1,.3,1) arrivals; outSoft(.22,1,.36,1); in(.7,0,.84,0); exit(.55,.055,.675,.19) exits into a cut; inOut(.87,0,.13,1) whips/morphs; smooth(.65,0,.35,1) fades 10-14f; ui(.4,0,.2,1); cam(.48,.1,0,.9) pushes, peak ~27%; glide(.47,.2,.15,1) 150-350px moves; rest(.45,0,.1,1); contact(.55,0,.9,.55)…
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:22` · `kosif-studio/tests/test_studio.py:637`

#### EASE-22 · أسماء التسارع القديمة · Legacy GSAP ease aliases · ✅ مُثبت هنا
- **ماذا / what:** Four named eases kept from kit v1/v2 that templates still use.
- **كيف / how:** MOTION.ease.slam/snap/drive/settle/linear passed to gsap.
- **أرقام / params:** slam=expo.out; snap=back.out(1.3); drive=power4.inOut; settle=power4.out; linear=none
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:12`

#### EASE-23 · تكبير لوغاريتمي · Log-space scale/zoom (logEase, lmix) · ✅ مُثبت هنا
- **ماذا / what:** Interpolates scale in log space so 1x->2x feels the same as 2x->4x.
- **كيف / how:** MOTION.lmix(a,b,t) for values; MOTION.logEase(a,b,fn) wraps an ease so a linear scale tween moves through log space.
- **أرقام / params:** lmix = exp(log a + (log b - log a)·t)
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:44`

#### EASE-24 · نوابض مطبَّعة · Normalised spring eases (SPRINGS) · ✅ مُثبت هنا
- **ماذا / what:** Damped-oscillator eases normalised to end at 1, for GSAP tweens.
- **كيف / how:** ease: MOTION.spring('snappy'|'default'|'heavy'|'playful') or {zeta, omega}.
- **أرقام / params:** snappy zeta .62 omega 20 (measured overshoot 8.4%); default .74/17 (3.2%); heavy 1.0/13 (0%); playful .45/18 (20.5%)
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:52`

#### EASE-25 · نوابض فيزيائية · Physical springs SPR (closed form) · ✅ مُثبت هنا
- **ماذا / what:** Seven damping/stiffness/mass presets solved in closed form, so any frame renders without simulating earlier frames.
- **كيف / how:** MOTION.springStep(t, MOTION.SPR.firm) (under/critical/over-damped branches, optional clamp).
- **أرقام / params:** snap d18 k260 m.7 (zeta .67, overshoot 6%, settle .35 s); pop 11/180/.6 (14%, .53 s); land 14.5/200/1 (15%, .65 s); micro 30/500/.6 (0.4%, .17 s); firm 24/140/1 (critical, .65 s); soft 26/120/1 (.94 s); heavy 30/90/1.4 (1.53 s) — measured here with node
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:65`

#### EASE-26 · مسار نابضي متعدد الأهداف · Retargetable spring track · ✅ مُثبت هنا
- **ماذا / what:** A value with several targets over time = first value plus one spring per change; continuous and seekable.
- **كيف / how:** MOTION.track(t, [[time,value],...], SPR.firm | 'default', settle=0.6).
- **أرقام / params:** keys are move START times; default settle 0.6 s
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:77`

#### EASE-27 · قواعد التسهيل · Easing conventions · ✅ مُثبت هنا
- **ماذا / what:** Linear only for drift, data fills and luminance; punches expo.out 0.12-0.18 s; drifts power2.inOut; later entrances use fromTo with immediateRender:false; no CSS transitions; finite repeats.
- **كيف / how:** lint warns + project timelines
- **أرقام / params:** data fill 'none'; exits ease E.exit 0.2-0.25 s
- **الدليل / proof:** `kosif-studio/motion/qa.py:65` · `kosif-studio/motion/projects/premium_edit/index.html:110`

#### EASE-28 · قاعدة الحتمية · Determinism rule · ✅ مُثبت هنا
- **ماذا / what:** Everything is a function of t: seeded RNG only, no wall clock, no timers, no THREE.Clock; frames can render in any order and in parallel.
- **كيف / how:** lint errors; tests assert no Math.random/new THREE.Clock in kits
- **الدليل / proof:** `kosif-studio/motion/qa.py:59` · `kosif-studio/tests/test_studio.py:585`

#### EASE-29 · لقطة السرعة U · U-speed shot · 🟢 جاهز
- **ماذا / what:** Element enters fast and decays, cruises slowly while read, then accelerates into the cut.
- **كيف / how:** MOTION.shot(tl, el, at, {enter, cruise, exit, cut, dir, dist, exitDist, fade}).
- **أرقام / params:** enter 0.45 s from 220 px (E.out); cruise 1.2 px/frame; exit 0.3 s E.exit over 1.4x dist
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:393` · `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:393` · `kosif-one/tools/kosif-studio/motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/SKILL.md:95`

#### EASE-30 · غلاف النبضة للضربات · Hit pulse envelope · 🟢 جاهز
- **ماذا / what:** One attack/exponential-decay envelope used for every punch, tick, kick-driven pulse and sound-synced hit.
- **كيف / how:** MOTION.hitPulse(t, attack, tau) with t in seconds, attack/tau in 60 fps frames; sine attack then exp(-(u-attack)/tau), zero after attack+6*tau.
- **أرقام / params:** default attack=2 f, tau=5 f; peak 2 f after its sound
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:47` · `kosif-one/tools/kosif-studio/motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`

#### EASE-31 · مسار نابضي متعدد الأهداف · Retargetable spring track / zoomTrack · 🟢 جاهز
- **ماذا / what:** A value with many keyed targets that springs to each new target continuously and stays seekable; zoomTrack does it in log space.
- **كيف / how:** MOTION.track(t, [[t0,v0],[t1,v1],...], preset, settle) sums one spring per change; zoomTrack(t, keys) for scale.
- **أرقام / params:** settle default 0.6 s with normalised presets; physical SPR objects accepted
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:77` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:88` · `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:77` · `kosif-one/tools/kosif-studio/motion/references/x-trend-2026.md`

#### EASE-32 · انضغاط عند الاصطدام · Contact squash · 🟢 جاهز
- **ماذا / what:** Element widens and flattens against the edge it hit, then recovers (cartoon squash).
- **كيف / how:** MOTION.squash(tl, el, at, {edge:'bottom'|'top'|'left'|'right', across, along, dur}).
- **أرقام / params:** scaleX 1.08 / scaleY 0.90 -> 1 in 0.13 s (8 f) E.outSoft
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:372` · `kosif-studio/motion/kit/motion-kit.js:372`

#### EASE-33 · دخول عناصر القائمة تباعاً · Stagger list arrival · 🟢 جاهز
- **ماذا / what:** Cards, bullets or icons arrive one by one with the same ease.
- **كيف / how:** MOTION.stagger(tl, els, at, {gap, dur, from, ease}).
- **أرقام / params:** gap 0.07 s, dur 0.55 s, from y 28 opacity 0 scale 0.96; stagger totals < 500 ms
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:557` · `kosif-studio/motion/kit/motion-kit.js:557`

#### EASE-34 · إعدادات النوابض الجاهزة · Spring presets and damping-ratio intuition · 🟢 جاهز
- **ماذا / what:** Physics springs (stiffness, damping, mass) give velocity-aware motion with natural overshoot; a handful of named presets covers most needs from gentle to stiff.
- **كيف / how:** Framer Motion transition={{type:'spring',stiffness,damping,mass}}; in a video renderer implement the damped oscillator per frame (Remotion spring() or own x''=-k(x-1)-c x'). Overshoot exists when c < 2*sqrt(k*m).
- **أرقام / params:** default 170/26; gentle 120/14; wobbly 180/12; stiff 210/20; slow 280/60; molasses 280/120 (mass 1); button tap 400/17; layout 500/30; 'premium' 300/30/1 with ~1.05 overshoot landing in 400-700ms; CSS fallback cubic-bezier(0.34,1.56,0.64,1) 500ms
- **الدليل / proof:** `kosif-atlas/skills/3529-ui-design/14308-interaction-design/references/animation-libraries.md` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`

#### EASE-35 · جدول سرعة الكتابة الآلية · Typewriter speed table · 🟢 جاهز
- **ماذا / what:** Characters-per-second presets for typed text and a hard-stepped blinking caret; also realistic per-key delay for scripted typing in UI recordings.
- **كيف / how:** GSAP TextPlugin {text:{value}, duration: len/cps, ease:'none'} or tl.call per char; caret opacity yoyo with ease 'steps(1)'; in recordings type at ~70ms per key.
- **أرقام / params:** 3-5 cps dramatic; 8-12 natural; 15-20 tech/code; 30+ bulk fill; scripted typing delay 70ms/char; caret block 11x22px
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10377-gsap/references/effects.md` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-atlas/skills/1511-homie/3903-video/references/RECORD.md`

#### EASE-36 · رموز الحركة مع بديل تقليل الحركة · Motion and duration tokens with reduced-motion swap · 🟢 جاهز
- **ماذا / what:** A token set for durations and easings plus a rule that reduced motion swaps to instant/linear; exposed to Tailwind theme.
- **كيف / how:** :root vars + @media (prefers-reduced-motion: reduce) override; Tailwind transitionDuration from vars.
- **أرقام / params:** instant 0ms; fast 100ms; normal 200ms; slow 300ms; slower 500ms; ease-in 0.4,0,1,1; ease-out 0,0,0.2,1
- **الدليل / proof:** `kosif-atlas/skills/1567-tonone/4430-form-tokens` · `kosif-atlas/skills/3438-ux-design/14124-top-design`

#### EASE-37 · انزلاق متناقص · Decaying slide distance · 🟢 جاهز
- **ماذا / what:** Entry offset shrinks per successive word so the line seems to settle like a camera.
- **كيف / how:** slides=[80,60,50,25,12]px applied per word index.
- **أرقام / params:** 80→12px
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### EASE-38 · قائمة لقطات على شبكة الإيقاع مع كلمات مضبوطة على البداية · Beat-grid shot list with onset-snapped words · 🟢 جاهز
- **ماذا / what:** Plan every generated shot on the song's bar lines and use per-word times to drive lyric type.
- **كيف / how:** grid.json holds tempo, beats, bar lines, sections and words; cuts land on bar lines (beats in fast sections); model word stamps ran 50-80 ms late so each word is snapped to the strongest vocal-band onset within −100 ms..+40 ms; characters on one side, words on the other.
- **أرقام / params:** snap window −100..+40 ms; stamps 50-80 ms late
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video` · `kosif-atlas/skills/1511-homie/3892-music`

#### EASE-39 · منحنى الاستوديو · Studio ease curve · 🟢 جاهز
- **ماذا / what:** Smooth expo-like ease used by KOSIF 4 scene and card entries.
- **كيف / how:** var(--ease-studio).
- **أرقام / params:** cubic-bezier(.2,.8,.2,1)
- **الدليل / proof:** `kosif-audit-studio/studio.css:2`

#### EASE-40 · دخول المشهد بتتابع حسب الترتيب · Studio scene-in with index stagger · 🟢 جاهز
- **ماذا / what:** Cards rise 12px and fade; delay is computed from a per-card CSS custom property set in JS.
- **كيف / how:** style='--card-order:i'; animation: scene-in .55s var(--ease-studio) both; animation-delay: calc(var(--card-order)*45ms).
- **أرقام / params:** view 0.48s; reference cards 0.55s @45ms/step; council seats 0.5s @40ms/step; metric cards 40/80/120ms; messages 0.35s
- **الدليل / proof:** `kosif-audit-studio/studio.css:114` · `kosif-audit-studio/studio.css:120` · `kosif-audit-studio/studio.js:133`

#### EASE-41 · زر تهدئة الحركة · User 'quiet motion' toggle · 🟢 جاهز
- **ماذا / what:** Besides the OS setting, a user button sets data-motion=quiet on the root (or a body class) that kills all animation/transition; the canvas waveform flattens too.
- **كيف / how:** studio.js renderMotion(): documentElement.dataset.motion = quiet|full; CSS :root[data-motion=quiet] * { animation:none; transition:none }; V5 uses localStorage key kosif:v5:motion-off -> body.dashboard-motion-off.
- **أرقام / params:** wave level fixed at .08 when quiet
- **الدليل / proof:** `kosif-audit-studio/studio.js:23` · `kosif-audit-studio/studio.css:140` · `kosif-audit-studio/dashboard-capabilities.css:15`

#### EASE-42 · توقيت القراءة للسطور العربية · Reading-speed timing for Arabic lines · 🟢 جاهز
- **ماذا / what:** Times script lines without audio from a words-per-second reading speed weighted by word length, with a minimum on-screen time per line.
- **كيف / how:** MK.speedTimings(lines,wps=2.2,gap=0.8,lead=0.5,tail=1.0): word dur=(1/wps)*clamp(len/5,0.6,1.6), end at 92%; line kept >= 0.3 s/word + 0.6 s; requested film length stretches pace (never below 1.2 wps) and gaps up to 2.2 s.
- **أرقام / params:** wps 2.2 (style 1.9-2.2); gap 0.8 s; lead 0.5 s; tail 1.0 s; min 0.3 s/word+0.6 s
- **الدليل / proof:** `app/public/js/10_studio.js:60` · `app/public/js/10_studio.js:999`

#### EASE-43 · دوال التسهيل والزنبرك · Core easing functions and damped spring · 🟢 جاهز
- **ماذا / what:** Basic easings and an analytic damped spring available to every template and to Claude-written code.
- **كيف / how:** easeOut = 1-(1-x)^3; easeInOut cubic; easeBack c1=1.70158; spring(x seconds, z=0.42, w=16 rad/s) = 1 - e^(-z w x)(cos wd x + z w/wd sin wd x).
- **أرقام / params:** spring damping 0.42, 16 rad/s
- **الدليل / proof:** `app/public/js/00_editor.js:8` · `app/public/js/00_editor.js:12`

#### EASE-44 · منحنيات بيزييه الاستوديو · Studio bezier curves (U.E) · 🟢 جاهز
- **ماذا / what:** Nine cubic-bezier easing curves solved by Newton iteration for motion tokens.
- **كيف / how:** bez(x1,y1,x2,y2) with 7 Newton steps; out(.16,1,.3,1), outSoft(.22,1,.36,1), in(.7,0,.84,0), exit(.55,.055,.675,.19), inOut(.87,0,.13,1), smooth(.65,0,.35,1), ui(.4,0,.2,1), cam(.48,.1,0,.9), whip(.6,0,.15,1).
- **الدليل / proof:** `app/public/js/00_editor.js:2309` · `app/public/js/00_editor.js:2311`

#### EASE-45 · زنبركات فيزيائية جاهزة · Physical spring presets (settle) · 🟢 جاهز
- **ماذا / what:** Mass-spring-damper presets with under/critical/over-damped solutions.
- **كيف / how:** SPR [c,k,m]: snap [18,260,.7], pop [11,180,.6], land [14.5,200,1], micro [30,500,.6], firm [24,140,1], soft [26,120,1], heavy [30,90,1.4]; u.settle(t,name); firm/soft/heavy never overshoot.
- **الدليل / proof:** `app/public/js/00_editor.js:2312`

#### EASE-46 · غلاف الضربة · Hit envelope · 🟢 جاهز
- **ماذا / what:** A punch envelope that peaks shortly after an event and decays, for impacts synced to sound.
- **كيف / how:** u.hit(t,attack=2/60,tau=5/60): sin rise during attack then exp(-(t-attack)/tau).
- **أرقام / params:** attack 33 ms; tau 83 ms
- **الدليل / proof:** `app/public/js/00_editor.js:2317`

#### EASE-47 · انتقال ناعم بين الثيمات · Smooth theme cross-fade · 🟢 جاهز
- **ماذا / what:** When the look changes, backgrounds, text, borders and shadows of the main frame cross-fade instead of snapping.
- **كيف / how:** html.sk-theme-trans adds transition on background-color/color/border-color/box-shadow.
- **أرقام / params:** 220ms cubic-bezier(.2,.8,.2,1)
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/tokens.css:99`

#### EASE-48 · دخول النوافذ والقوائم والتنبيهات · Dialog / menu / toast entrances · 🟢 جاهز
- **ماذا / what:** Dialogs settle with a slight spring overshoot (rise only, no scale so 44px targets stay full size), menus ease out, toasts slide up with a small scale-in.
- **كيف / how:** @keyframes sk-dialog-in {opacity 0, translateY(8px)} 300ms spring; .sk-menu 220ms ease-out; sk-toast-in {translateY(12px) scale(.96)} 340ms spring; dropdown ddin translateY(-4px) scale(.98) .2s; popover sk-pop translateY(-4px) .14s.
- **أرقام / params:** 300 / 220 / 340 / 200 / 140 ms
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/luxe.css:367` · `kosif-earth-ci-fork/ui/ds/components.css:225` · `kosif-earth-ci-fork/ui/ds/luxe.css:93`

#### EASE-49 · تفاعلات الضغط والمرور · Press & hover micro-interactions · 🟢 جاهز
- **ماذا / what:** Buttons dip on press; cards answer hover with a deeper shadow (no movement, so pinned lists do not jump); door gates lift 2px.
- **كيف / how:** .btn:active{transform:scale(.985)} transform 180ms ease-out; .card:hover box-shadow 220ms only under (hover:hover) and (pointer:fine); .gate:hover translateY(-2px) .18s.
- **أرقام / params:** scale .985; 180ms; 220ms; lift 2px
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/luxe.css:373` · `kosif-earth-ci-fork/ui/art/brand/earth-office-door.css`

#### EASE-50 · وميض الهيكل أثناء التحميل · Skeleton shimmer loader · 🟢 جاهز
- **ماذا / what:** Placeholder bars with a moving light band while content loads.
- **كيف / how:** background:linear-gradient(90deg,surface-2,surface-3,surface-2); background-size:200% 100%; @keyframes sks-sh{to{background-position:-200% 0}} 1.2s linear infinite; bars 14px tall radius 7px.
- **أرقام / params:** 1.2s linear infinite
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/shell.css:217`

#### EASE-51 · نبضات الحالة · Status pulses (alert dot, recording ring, typing dots) · 🟢 جاهز
- **ماذا / what:** Three tiny looping signals: a fading alert dot, an expanding glow ring on a recording mic, and three bouncing typing dots.
- **كيف / how:** pulse: opacity 1->.35->1 1.6s ease-in-out infinite; ska-pulse: box-shadow 0 0 0 6px color-mix(bad 25%) at 50%, 1s; ska-dot: opacity .25 translateY(-3px) at 50%, 1s, delays 0/.15s/.3s.
- **أرقام / params:** 1.6s; 1s; 150ms offsets
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/components.css:38` · `kosif-earth-ci-fork/ui/features/assistant.css:20`

#### EASE-52 · شريط تقدم متزامن مع الفيديو · Video-synced progress bar · 🟢 جاهز
- **ماذا / what:** A 3px bar fills linearly over exactly the clip duration while the intro plays and snaps full on completion.
- **كيف / how:** .earth-intro.is-playing .earth-intro__progress::before{animation:earthIntroProgress 5.06s linear forwards}; is-complete sets width 100%.
- **أرقام / params:** 3px; 5.06s linear; colour #e8bd76
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/brand/earth-intro-20261009.css:21`

#### EASE-53 · دوّار التحميل والدخول الهادئ · Spinner and calm enter · 🟢 جاهز
- **ماذا / what:** A ring spinner with one transparent side, and a very short calm fade for hero cards in the SQC light look.
- **كيف / how:** skdemo-spin: 34px ring border 4px, inline-end transparent, rotate 360deg .8s linear infinite; sqc-calm-enter opacity .65->1 translateY(4px) 180ms ease-out once.
- **أرقام / params:** .8s; 180ms
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/shell.css:535` · `kosif-earth-ci-fork/ui/ds/sqc.css:251`

#### EASE-54 · قاعدة حساب المدة · Duration arithmetic truth rule · 🟢 جاهز
- **ماذا / what:** Total duration must equal clips x clip length (5x6=30, 5x7=35, Nx10=10N); supplied timestamps override word-pace estimates; never promise 10 s with 6 s scenes.
- **كيف / how:** Compute totals in code (stickman seconds sum, vox n*10, food n*10, viral shots*6) and print them in output.
- **أرقام / params:** 5x6=30; 5x7=35; Nx10
- **الدليل / proof:** `fastify-motion-bro/docs/PRODUCTION-GATES.md:7` · `fastify-motion-bro/docs/VIRAL-EDITORIAL-DNA.md:26-27`

#### EASE-55 · تسهيل خروج تكعيبي · easeOutCubic · 🟢 جاهز
- **ماذا / what:** Standard cubic ease-out used for title slides, headline rise and hero exit.
- **كيف / how:** ease(t)=1-(1-clamp(t))^3.
- **الدليل / proof:** `fastify-motion-bro/web/motion.js:1` · `fastify-motion-bro/web/editorial.js:4`

#### EASE-56 · نابض مخمد بتجاوز 7٪ · Damped spring with 7% overshoot · 🟢 جاهز
- **ماذا / what:** Spring curve for hero entrances that overshoots slightly then settles.
- **كيف / how:** spring(t)=min(1.07, 1-exp(-7t)*cos(10t)); entrance enter=spring((local-.5)/3).
- **أرقام / params:** k=7 decay, 10 rad oscillation, cap 1.07, 3 s duration
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:11,40`

#### EASE-57 · رموز التسارع (16 منحنى) · Easing tokens E (16 cubic-bezier roles) · 🟢 جاهز
- **ماذا / what:** A house set of cubic-bezier easing curves, one curve per motion role (arrival, exit, whip, camera push, typewriter, iris, hop...).
- **كيف / how:** Browser page with gsap.min.js + motion-kit.js (window.MOTION); build a paused gsap.timeline, call pass MOTION.E.<token> as the GSAP ease (functions are accepted). Built by MOTION.bezier(x1,y1,x2,y2) with an 8-step Newton solve.
- **أرقام / params:** out(.16,1,.3,1) arrivals; outSoft(.22,1,.36,1); in(.7,0,.84,0) implosions; exit(.55,.055,.675,.19) into a cut (~x1.14/frame over last 10-24 f); inOut(.87,0,.13,1) whips/morphs; smooth(.65,0,.35,1) fades 10-14 f; ui(.4,0,.2,1); cam(.48,.1,0,.9) peak ~27%; glide(.47,.2,.15,1) 150-350 px moves; rest(.4…
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:22` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:15` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md:1`

#### EASE-58 · أربع تسارعات مسماة · Four named GSAP eases (slam/snap/drive/settle) · 🟢 جاهز
- **ماذا / what:** The minimal easing vocabulary the house rules allow for 2D compositions.
- **كيف / how:** MOTION.ease.slam / snap / drive / settle as GSAP ease strings; composition.html comment restricts films to these four.
- **أرقام / params:** slam=expo.out; snap=back.out(1.3); drive=power4.inOut; settle=power4.out; linear=none
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:12` · `100-superskills/skills/kosif-montage-motion/templates/composition.html:27`

#### EASE-59 · تسارع لوغاريتمي للزووم · Log-space ease for zooms (logEase / lmix) · 🟢 جاهز
- **ماذا / what:** Makes a scale or zoom tween feel constant-speed perceptually by interpolating in log space.
- **كيف / how:** MOTION.logEase(a,b,fn) returns an ease for a linear tween from a to b; MOTION.lmix(a,b,t) mixes values in log space. Used by push() and iris().
- **أرقام / params:** logEase(from,to,E.cam); 1 -> 2.4x push feels constant; cap ~5% scale change per frame
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:43` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:316`

#### EASE-60 · نبضة الضربة · hitPulse impact envelope · 🟢 جاهز
- **ماذا / what:** One attack/exponential-decay envelope used for punches, ticks, kicks and beat flashes.
- **كيف / how:** MOTION.hitPulse(t, attack, tau) with t in seconds, attack/tau in 60 fps frames: sine rise over attack then exp(-(u-attack)/tau), zero after attack+6 tau.
- **أرقام / params:** attack=2 f, tau=5 f (defaults); channels.kick uses attack 1 tau 5; onset 1/4; beat 1/6
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:47`

#### EASE-61 · مدة حسب المسافة · Distance-scaled duration (durFor) · 🟢 جاهز
- **ماذا / what:** Move duration grows with travel distance so long moves don't look rushed.
- **كيف / how:** MOTION.durFor(px, camera): 0.35 s + 1.35 ms per px; camera moves clamped.
- **أرقام / params:** 0.35 s + 0.00135 s/px; camera clamp 0.6-2.4 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:49`

#### EASE-62 · نوابض مطبّعة · Normalised spring eases (SPRINGS presets) · 🟢 جاهز
- **ماذا / what:** Damped-oscillator eases normalised to end at 1, usable as GSAP eases for pops and settles.
- **كيف / how:** MOTION.spring('snappy'|'default'|'heavy'|'playful') or spring({zeta,omega}) -> ease function.
- **أرقام / params:** snappy zeta .62 omega 20; default .74/17; heavy 1.0/13 (critically damped); playful .45/18
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:52` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:53`

#### EASE-63 · نوابض فيزيائية · Physical springs SPR + springStep · 🟢 جاهز
- **ماذا / what:** Closed-form damped spring step response (mass/stiffness/damping), seekable at any t, critically damped by default.
- **كيف / how:** MOTION.springStep(t, MOTION.SPR.<preset>) returns 0->1; handles under/critical/over-damped; cfg.clamp caps overshoot.
- **أرقام / params:** snap d18 k260 m.7; pop d11 k180 m.6; land d14.5 k200 m1; micro d30 k500 m.6; firm d24 k140 m1; soft d26 k120 m1; heavy d30 k90 m1.4
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:65` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:67`

#### EASE-64 · تتابع القائمة · List stagger · 🟢 جاهز
- **ماذا / what:** Cards, bullets or icons arrive one by one; returns end time for chaining.
- **كيف / how:** MOTION.stagger(tl, els, at, {gap, dur, from, ease}).
- **أرقام / params:** gap 0.07 s; dur 0.55 s; from {y:28, opacity:0, scale:.96}; E.out
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:557`

#### EASE-65 · دالة نابض مخمد للقفزات والارتخاء · Damped spring function for pops and flops · 🟢 جاهز
- **ماذا / what:** An analytic damped spring from 0 to 1 starting at t0 overshoots once and settles; used for joint pops, the ear flop at the break and the spring back after the repair.
- **كيف / how:** spring(t, t0, f=3.2 Hz, ζ=.32) = 1 − e^(−ζωx)(cos ω_d x + ζω/ω_d sin ω_d x), ω=2πf, ω_d = ω√(1−ζ²); pops f 4.2 ζ .38; flop f 1.5 ζ .42; recovery f 1.6 ζ .5.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:12` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:128` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:148`

#### EASE-66 · منحنيات السرعة · Speed ramps · 🟢 جاهز
- **ماذا / what:** Piecewise-linear speed keys inside a clip with exact integral time map.
- **كيف / how:** timeline clip 'ramp':[[0,1.0],[1.5,0.25],[3,1.0]]
- **أرقام / params:** speed 0.1–10; audio dropped under ramp, constant speed pitch-preserved
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:36` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:99`

#### EASE-67 · دوال التنعيم · Easing helpers: smoothstep, lerp, clamp, easeOutCubic · 🟢 جاهز
- **ماذا / what:** The small easing kit used across the studio pages for natural motion.
- **كيف / how:** smooth(v) = v²(3−2v) after clamp; lerp(a,b,t); easeOutCubic = 1 − (1−p)³ (review page, Studio overlays, manifest player).
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:6` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:431` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:75`

#### EASE-68 · شريط تقدّم زمني · Timeline progress bar · 🟢 جاهز
- **ماذا / what:** A bottom bar grows with normalized time so viewers feel the length of a reel.
- **كيف / how:** kinetic_2d render(t): width = (t/DURATION)*100%; absolute bottom bar, z-index 10.
- **أرقام / params:** height 12px, gradient 90deg #f59e0b->#ef4444
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/kinetic_2d.html:77` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/kinetic_2d.html:200`

#### EASE-69 · رموز التسارع حسب الدور · Role-based easing tokens (MOTION.E) · 🟢 جاهز
- **ماذا / what:** A family of 17 cubic-bezier eases, one per motion role (arrival, exit, camera, whip, UI, typewriter...), so every move in a film shares one consistent feel.
- **كيف / how:** In a HyperFrames/GSAP composition load assets/motion-kit.js and pass MOTION.E.<role> as the GSAP ease; bezier() solves x->t with 8 Newton steps so GSAP accepts the function.
- **أرقام / params:** out(.16,1,.3,1) arrivals; outSoft(.22,1,.36,1); in(.7,0,.84,0); exit(.55,.055,.675,.19) ~x1.14/frame over last 10-24 f; inOut(.87,0,.13,1) whips/morphs; smooth(.65,0,.35,1) fades 10-14 f; ui(.4,0,.2,1); cam(.48,.1,0,.9) peak ~27%; glide(.47,.2,.15,1) 150-350 px; rest(.45,0,.1,1); contact(.55,0,.9,.5…
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:22` · `kosif-one/tools/kosif-studio/motion/references/craft-numbers.md`

#### EASE-70 · تسارعات مسماة: صدمة/خطفة/دفع/استقرار · Legacy named eases slam/snap/drive/settle · 🟢 جاهز
- **ماذا / what:** Four short named GSAP eases from kit v1 used by the word reveals and pen strokes.
- **كيف / how:** MOTION.ease.slam etc. passed as GSAP ease strings.
- **أرقام / params:** slam=expo.out, snap=back.out(1.3), drive=power4.inOut, settle=power4.out, linear=none
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:12`

#### EASE-71 · زووم لوغاريتمي ثابت الإحساس · Log-space zoom ease (logEase / lmix) · 🟢 جاهز
- **ماذا / what:** Makes scale and zoom changes feel constant (1x->2x feels like 2x->4x) by interpolating in log space.
- **كيف / how:** MOTION.logEase(a,b,fn) wraps any ease for a linear tween of scale; MOTION.lmix(a,b,t) for direct values; zoomTrack for multi-target zooms.
- **أرقام / params:** push 1->2.4x feels constant; peak about 5% scale per frame
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:43` · `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:88`

#### EASE-72 · مدة تتناسب مع المسافة · Distance-proportional duration · 🟢 جاهز
- **ماذا / what:** Duration of a move grows with distance travelled; camera moves are clamped.
- **كيف / how:** MOTION.durFor(px, camera) = 0.35 s + 1.35 ms per px; camera clamped to 0.6-2.4 s; slowest move >= 3x fastest.
- **أرقام / params:** 0.35 + 0.00135*px s; camera 0.6-2.4 s
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:49` · `kosif-one/tools/kosif-studio/motion/references/craft-numbers.md`

#### EASE-73 · زنبركات جاهزة كمنحنيات · Normalised spring eases (snappy/default/heavy/playful) · 🟢 جاهز
- **ماذا / what:** Damped-oscillator eases normalised to end at 1, usable directly as GSAP eases for springy arrivals.
- **كيف / how:** MOTION.spring('snappy'|'default'|'heavy'|'playful') returns an ease function.
- **أرقام / params:** snappy zeta .62 omega 20 (~3% overshoot); default .74/17 (~1%); heavy 1.0/13 (0%); playful .45/18 (visible)
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:52` · `kosif-one/tools/kosif-studio/motion/references/motion-craft.md`

#### EASE-74 · زنبركات فيزيائية بكتلة وصلابة · Physical spring presets SPR + springStep · 🟢 جاهز
- **ماذا / what:** Closed-form damped spring step responses (under/critical/over-damped), seekable at any t, critically damped by default.
- **كيف / how:** MOTION.springStep(t, MOTION.SPR.<name>) or MOTION.track(t, keys, SPR.firm); clamp option removes overshoot.
- **أرقام / params:** snap d18 k260 m0.7; pop d11 k180 m0.6; land d14.5 k200 m1; micro d30 k500 m0.6; firm d24 k140 m1; soft d26 k120 m1; heavy d30 k90 m1.4; max two overshooting springs per film
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:65` · `kosif-one/tools/kosif-studio/motion/references/craft-numbers.md`

#### EASE-75 · تغيير السرعة · Speed change · 🟢 جاهز
- **ماذا / what:** Speed up/slow clips with pitch-safe audio.
- **كيف / how:** setpts=0.5*PTS + atempo=2.0 (atempo range 0.5-2, chain for more); EDL clip.speed.
- **أرقام / params:** speed 1.5 in example
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md` · `100-superskills/skills/pro-video-editor-ffmpeg/templates/edl.example.json`

#### EASE-76 · نابض بصيغة مغلقة · Closed-form spring easing · 🟢 جاهز
- **ماذا / what:** Deterministic damped spring evaluated analytically, overshoots ~1.05 then settles.
- **كيف / how:** spring(x) in scene-2d.html using omega=sqrt(stiffness), zeta=damping/(2*omega).
- **أرقام / params:** stiffness 300, damping 30, mass 1
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/templates/scene-2d.html:49` · `100-superskills/skills/claude-animation-studio/references/motion-rules.md`

#### EASE-77 · دوال التوقيت seg/lerp · seg/lerp/ease helper set · 🟢 جاهز
- **ماذا / what:** Local progress seg(t,a,b) clamped 0..1 with lerp, easeIn/easeOut/easeInOut, breathe, glow helpers.
- **كيف / how:** Use seg to map beat window then shape with ease or spring.
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/templates/scene-2d.html`

#### EASE-78 · مفاتيح مأخوذة من دالة · Function-sampled keyframes · 🟢 جاهز
- **ماذا / what:** Turns any f(t) into GSAP keyframes so code-driven motion stays seek-safe.
- **كيف / how:** tl.to(el, {keyframes: MOTION.sampled(fn, t0, t1, 60)}).
- **أرقام / params:** 60 samples/s default
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:109`

#### EASE-79 · حركة النابض المخمد · Damped spring motion · 🟢 جاهز
- **ماذا / what:** Overshoot-and-settle curve for squash, pops and floppy ears as a pure function of time.
- **كيف / how:** spring(t, t0, f, z) = 1 − e^(−zωx)(cos ω_d x + (zω/ω_d) sin ω_d x)
- **أرقام / params:** f 3.2 Hz, ζ 0.32 (one overshoot)
- **الدليل / proof:** `kosif-studio/motion/projects/bunny_twin/src/main.js:9`

#### EASE-80 · تسهيل خطي · Easing linear (html-canvas) · 🟢 جاهز
- **ماذا / what:** Ease.linear maps 0..1 to 0..1 for entrances/exits in the canvas starter.
- **كيف / how:** KOSIF.Ease.linear(x) or prog(t,t0,t1,Ease.linear)
- **أرقام / params:** formula x; used for —
- **الدليل / proof:** `kosif-tool/starters/html-canvas/timeline.js:12`

#### EASE-81 · تسهيل خروج تكعيبي · Easing outCubic (html-canvas) · 🟢 جاهز
- **ماذا / what:** Ease.outCubic maps 0..1 to 0..1 for entrances/exits in the canvas starter.
- **كيف / how:** KOSIF.Ease.outCubic(x) or prog(t,t0,t1,Ease.outCubic)
- **أرقام / params:** formula 1-(1-x)^3; used for default for prog()
- **الدليل / proof:** `kosif-tool/starters/html-canvas/timeline.js:12`

#### EASE-82 · تسهيل دخول وخروج تكعيبي · Easing inOutCubic (html-canvas) · 🟢 جاهز
- **ماذا / what:** Ease.inOutCubic maps 0..1 to 0..1 for entrances/exits in the canvas starter.
- **كيف / how:** KOSIF.Ease.inOutCubic(x) or prog(t,t0,t1,Ease.inOutCubic)
- **أرقام / params:** formula 4x^3 / 1-(-2x+2)^3/2; used for camera default, draw-on
- **الدليل / proof:** `kosif-tool/starters/html-canvas/timeline.js:12`

#### EASE-83 · تسهيل خروج أسي · Easing outExpo (html-canvas) · 🟢 جاهز
- **ماذا / what:** Ease.outExpo maps 0..1 to 0..1 for entrances/exits in the canvas starter.
- **كيف / how:** KOSIF.Ease.outExpo(x) or prog(t,t0,t1,Ease.outExpo)
- **أرقام / params:** formula 1-2^(-10x); used for ring burst, particles
- **الدليل / proof:** `kosif-tool/starters/html-canvas/timeline.js:12`

#### EASE-84 · تسهيل خروج خماسي · Easing outQuint (html-canvas) · 🟢 جاهز
- **ماذا / what:** Ease.outQuint maps 0..1 to 0..1 for entrances/exits in the canvas starter.
- **كيف / how:** KOSIF.Ease.outQuint(x) or prog(t,t0,t1,Ease.outQuint)
- **أرقام / params:** formula 1-(1-x)^5; used for counter
- **الدليل / proof:** `kosif-tool/starters/html-canvas/timeline.js:12`

#### EASE-85 · تسهيل ارتداد للخارج · Easing outBack (html-canvas) · 🟢 جاهز
- **ماذا / what:** Ease.outBack maps 0..1 to 0..1 for entrances/exits in the canvas starter.
- **كيف / how:** KOSIF.Ease.outBack(x) or prog(t,t0,t1,Ease.outBack)
- **أرقام / params:** formula s=1.70158; used for dots pop, caption pop
- **الدليل / proof:** `kosif-tool/starters/html-canvas/timeline.js:12`

#### EASE-86 · تسهيل سحب للخلف قبل الخروج · Easing inBack (html-canvas) · 🟢 جاهز
- **ماذا / what:** Ease.inBack maps 0..1 to 0..1 for entrances/exits in the canvas starter.
- **كيف / how:** KOSIF.Ease.inBack(x) or prog(t,t0,t1,Ease.inBack)
- **أرقام / params:** formula s=1.70158; used for exits
- **الدليل / proof:** `kosif-tool/starters/html-canvas/timeline.js:12`

#### EASE-87 · تسهيل نابضي مخمّد · Damped spring easing (stiffness/damping) · 🟢 جاهز
- **ماذا / what:** Analytic damped-spring curve with under/critically damped branches; gives overshoot pops without a physics loop.
- **كيف / how:** Ease.spring(x, stiffness, damping) inside prog()
- **أرقام / params:** defaults 170/18; title 170/16, burst 150/14, card 160/17
- **الدليل / proof:** `kosif-tool/starters/html-canvas/timeline.js:20` · `kosif-tool/starters/html-canvas/index.html:149`

#### EASE-88 · دوال التقدم والنافذة · prog / window01 / lerp timing helpers · 🟢 جاهز
- **ماذا / what:** prog(t,t0,t1,ease) gives eased progress inside a time window; window01 combines entrance and exit windows in one value; lerp/clamp01 interpolate.
- **كيف / how:** window01(t,t0,t1,tin=0.4,tout=0.4,easeIn=outCubic,easeOut=inOutCubic)
- **الدليل / proof:** `kosif-tool/starters/html-canvas/timeline.js:29`

#### EASE-89 · أدوات الخط الزمني KOSIF · KOSIF timeline helpers (Ease/prog/window01/rng/cameraAt) · 🟢 جاهز
- **ماذا / what:** Shared easing set and helpers used by all canvas snippets in playbooks.
- **كيف / how:** KOSIF.Ease {linear,outCubic,inOutCubic,outExpo,outQuint,outBack,inBack,spring(x,k,d)}, prog, window01, lerp, rng, cameraAt, applyCamera, activeWord, phrases, Timeline.
- **أرقام / params:** spring defaults k170 d18; outBack s 1.70158
- **الدليل / proof:** `kosif-tool/starters/html-canvas/timeline.js:12-131`

#### EASE-90 · منحنى الحركة السائلة · Fluid easing cubic-bezier(0.32,0.72,0,1) · 🟢 جاهز
- **ماذا / what:** Mass/spring-like easing for all transitions, 700 ms+.
- **كيف / how:** transition duration-700 ease-[cubic-bezier(0.32,0.72,0,1)]
- **أرقام / params:** 700-1000 ms
- **الدليل / proof:** `kosif-one/vendor/ai-design-skills/skills/landing-page-design/SKILL.md:270` · `kosif-one/vendor/mcp-higgsfield-landing/src/styles/global.css:13`

#### EASE-91 · نوابض الحركة · Spring presets · 📦 بأمر تثبيت
- **ماذا / what:** Closed-form springs as GSAP eases.
- **كيف / how:** MOTION.spring('snappy'|'default'|'heavy'|'playful')
- **أرقام / params:** overshoot ~3% / 1% / 0 / visible; settle ~0.5 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js` · `kosif-atlas/skills/3529-ui-design/14308-interaction-design/references/animation-libraries.md` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### EASE-92 · تمويه السرعة الاتجاهي · Directional speed blur · 📦 بأمر تثبيت
- **ماذا / what:** Fast moves get a motion-blur whose strength rises and falls over the move along one axis.
- **كيف / how:** M.speedBlur(tl,el,at,dur,{px:12,axis:'x'|'y'}) via an SVG feGaussianBlur stdDeviation 'px 0' bell (45% in E.in, 55% out E.out).
- **أرقام / params:** 12 px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:377-391` · `kosif-studio/motion/kit/motion-kit.js:378`

#### EASE-93 · معامل موضع الخط الزمني في GSAP · GSAP timeline position parameter · 📦 بأمر تثبيت
- **ماذا / what:** Place each tween on a master timeline by absolute time, relative offset or alignment to the previous tween, instead of chaining delays.
- **كيف / how:** const tl = gsap.timeline({paused:true, defaults:{duration:0.5, ease:'power2.out'}}); tl.to(a,{x:100},0); tl.to(b,{y:50},'<'); tl.to(c,{opacity:0},'<0.2'); '+=0.5' after end, '-=0.2' overlap, labels via tl.addLabel('intro', 0) and 'intro+=0.3'. Nest child timelines with master.add(child, t).
- **أرقام / params:** '<' same start; '>' after end; '<0.2' 0.2s after previous start
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10377-gsap/SKILL.md`

#### EASE-94 · التتابع المتدرج stagger · GSAP stagger object · 📦 بأمر تثبيت
- **ماذا / what:** One tween animates a list of elements with an offset between each, from start, end, center, edges or a seeded order.
- **كيف / how:** gsap.from('.word',{y:40, autoAlpha:0, stagger:{each:0.08, from:'center'}}) or {amount:0.3} to fit the whole cascade in 0.3s. Function-based values (i)=>i*50 give per-item offsets. Keep a total stagger under ~0.5s regardless of item count.
- **أرقام / params:** each 0.03-0.12s; amount 0.3s; total cascade <500ms
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10377-gsap/SKILL.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/motion-principles.md`

#### EASE-95 · مفردات منحنيات GSAP · GSAP ease vocabulary · 📦 بأمر تثبيت
- **ماذا / what:** Named ease families (power1-4, expo, circ, sine, back, elastic, bounce, steps) each with .in/.out/.inOut; the ease is the emotional adverb of the move.
- **كيف / how:** Map mood to ease: expo.out confident, sine.inOut dreamy, back.out(1.7) playful overshoot, elastic.out(1,0.3) springy, steps(1) discrete blink, 'none' for scrubbed/linear progress. Use .out for entering, .in for leaving, .inOut for moving between positions.
- **أرقام / params:** back.out(1.7); elastic.out(1,0.3); elastic.out(1,0.5)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10377-gsap/SKILL.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/motion-principles.md`

#### EASE-96 · نابض ريموشن والتحجيم الإدراكي · Easing.spring and perceptual scale · 📦 بأمر تثبيت
- **ماذا / what:** Spring easing inside interpolate gives organic pushes; scale animations need a perceptual mapping because linear scale looks slower as it grows.
- **كيف / how:** easing: Easing.spring({damping:200}) for no-bounce push; output:'perceptual-scale' on scale interpolations; posterize:3 samples every 3rd frame for a stepped, low-frame-rate look.
- **أرقام / params:** damping 200; posterize 3
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/timing.md` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/SKILL.md`

#### EASE-97 · قاموس منحنيات GSAP حسب الغرض · GSAP ease vocabulary by intent · 📦 بأمر تثبيت
- **ماذا / what:** Which named GSAP eases fit which job: strong deceleration for hero arrivals, gentler for scroll reveals, back for playful pop, elastic for magnetic snap-back, stepped for blinking cursors, none for scrubbed scroll.
- **كيف / how:** gsap.timeline({defaults:{ease:'power3.out'}}); reveals power2.out; premium expo.out; playful back.out(1.4)/back.out(1.6); magnetic release elastic.out(1,0.5); cursor blink ease 'steps(1)'; scroll-linked ease 'none'. Needs gsap (npm or CDN).
- **أرقام / params:** power3.out entrance; power2.out reveal; expo.out premium; back.out(1.4); elastic.out(1,0.5) 0.5-0.6s; steps(1)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/196-landing/621-landing/references/gsap_animation_patterns.md` · `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### EASE-98 · توزيع زمني لافتتاحية الصفحة/المشهد · Hero page-load choreography windows · 📦 بأمر تثبيت
- **ماذا / what:** A strict order for an opening: structure first, headline words staggered, subtitle, navigation cascade, then supporting elements; everything overlaps so the whole entrance lands in about 1.5 s.
- **كيف / how:** GSAP timeline with negative position offsets ('-=0.3', '-=0.5'); set initial states with gsap.set() before the timeline to avoid a flash of final layout.
- **أرقام / params:** structure 0-200ms; title words 200-600ms; subtitle 400-800ms; nav 600-900ms; support 800-1200ms; eyebrow 0.6s, h1 0.8s (-=0.3), subtitle 0.6s (-=0.5), CTA 0.5s (-=0.3), hint 0.4s (-=0.2); start y:30 opacity:0
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14124-top-design` · `kosif-atlas/skills/196-landing/621-landing/references/gsap_animation_patterns.md`

#### EASE-99 · توليد الإطارات البينية · Frame interpolation (RIFE / FILM) · 📦 بأمر تثبيت
- **ماذا / what:** Double apparent smoothness of low-fps generated clips.
- **كيف / how:** RIFE VFI multiplier 2, fast_mode, ensemble (FILM VFI for large motion) then re-encode at doubled fps; local fallback without GPU: ffmpeg minterpolate (lower quality).
- **أرقام / params:** multiplier 2; 8→16 fps
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2819-comfyui/11445-comfyui-workflow-design`

#### EASE-100 · توقيت القطع · Cut timing sync modes · 📦 بأمر تثبيت
- **ماذا / what:** Zoom cuts land on a fixed interval, beats, an editor's beat pattern, sentence starts, AI-chosen times, or the footage's own camera cuts.
- **كيف / how:** cutList(): interval (every 0.6-8 s), beat (beats >= max(0.45, 0.8*every) apart), pattern (planCuts), speech (voiced starts after >= 0.3 s pause, >= max(0.8, every/2) apart), ai (S.cuts), shots (bridge-measured shot boundaries); cached by signature.
- **أرقام / params:** interval|beat|pattern|speech|ai|shots
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:166` · `app/index.html:316`

#### EASE-101 · المغناطيس في التايملاين · Timeline magnetic snapping · 📦 بأمر تثبيت
- **ماذا / what:** Scrubbing snaps to caption edges, scene edges, cuts, shot cuts and beats within 7 px.
- **كيف / how:** snapTime(t,w): threshold 7 px converted to seconds; candidate points from S.caps, S.scenes, cutList(), S.shotCuts, S.beats.
- **أرقام / params:** 7 px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:573`

#### EASE-102 · توقيت نسبي للمقاطع · Relative clip start expressions · 📦 بأمر تثبيت
- **ماذا / what:** data-start may reference another clip id with an offset so scenes chain without manual seconds.
- **كيف / how:** data-start="intro + 0.5" or "intro - 0.5" (overlap).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/concepts/data-attributes.mdx`

#### EASE-103 · تحريك GSAP بخط زمني متوقف · GSAP paused-timeline authoring · 📦 بأمر تثبيت
- **ماذا / what:** Motion authored as a paused gsap.timeline registered under the composition id; transforms/opacity only.
- **كيف / how:** const tl=gsap.timeline({paused:true}); window.__timelines[id]=tl; avoid top/left/width tweens; load fonts before measuring.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/gsap-animation.mdx`

#### EASE-104 · مسار قوسي · Arc Motion Path · 📦 بأمر تثبيت
- **ماذا / what:** A callout travels along a curved arc using the GSAP MotionPath plugin with auto-rotation to the tangent.
- **كيف / how:** Install with `npx hyperframes add arc-motion-path` (copies to compositions/components/arc-motion-path.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **أرقام / params:** GSAP MotionPathPlugin autoRotate
- **تثبيت / install:** `npx hyperframes add arc-motion-path` (copies to compositions/components/arc-motion-path`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/arc-motion-path/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/arc-motion-path/arc-motion-path.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/arc-motion-path.mdx`

#### EASE-105 · عمود توقيت الضربات · Beat Timeline · 📦 بأمر تثبيت
- **ماذا / what:** A paused master timeline pins N titled rows to evenly spaced named labels; each enters on its label and the group exits together.
- **كيف / how:** Install with `npx hyperframes add beat-timeline` (copies to compositions/components/beat-timeline.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fr…
- **أرقام / params:** beatCount 4; interval 0.6 s; vars: beatCount=4(2..6); interval=0.6(0.2..2); labels=One,Two,Three,Four
- **تثبيت / install:** `npx hyperframes add beat-timeline` (copies to compositions/components/beat-timeline`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/beat-timeline/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/beat-timeline/beat-timeline.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/beat-timeline.mdx`

#### EASE-106 · أثر الصدى · Echo Trail · 📦 بأمر تثبيت
- **ماذا / what:** Moving element drawn with N ghost copies sampled at t - i*delta with stepped opacity that collapse into the element at rest (onion skin).
- **كيف / how:** Install with `npx hyperframes add echo-trail` (copies to compositions/components/echo-trail.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame ca…
- **أرقام / params:** echoes 4; delta 0.09 s; path sweep|rise|arc; vars: echoes=4; delta=0.09; path=sweep[sweep|rise|arc]; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add echo-trail` (copies to compositions/components/echo-trail`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/echo-trail/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/echo-trail/echo-trail.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/echo-trail.mdx`

#### EASE-107 · وصول ممتد · Extended Keyframe · 📦 بأمر تثبيت
- **ماذا / what:** An arrival curve that covers most of the move in the first fifth of the duration and creeps the remainder to the final frame, exiting along the same vector with shutter blur; also exposed as a bare ease.
- **كيف / how:** Install with `npx hyperframes add extended-keyframe` (copies to compositions/components/extended-keyframe.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chr…
- **أرقام / params:** ~80 % of travel in first 20 % of time
- **تثبيت / install:** `npx hyperframes add extended-keyframe` (copies to compositions/components/extended-keyframe`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/extended-keyframe/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/extended-keyframe/extended-keyframe.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/extended-keyframe.mdx`

#### EASE-108 · رصة إطارات مفتاحية · Keyframe Scrub Stack · 📦 بأمر تثبيت
- **ماذا / what:** Stack of cards keyed with offset timing and a choice of easing presets.
- **كيف / how:** Install with `npx hyperframes add keyframe-scrub-stack` (copies to compositions/components/keyframe-scrub-stack.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headle…
- **تثبيت / install:** `npx hyperframes add keyframe-scrub-stack` (copies to compositions/components/keyframe-scrub-stack`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/keyframe-scrub-stack/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/keyframe-scrub-stack/keyframe-scrub-stack.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/keyframe-scrub-stack.mdx`

#### EASE-109 · ضبابية الحركة · Motion Blur · 📦 بأمر تثبيت
- **ماذا / what:** AE-style shutter motion blur: samples the GSAP timeline at sub-frame times across the shutter window and averages equal-weight copies along the real trajectory (translate, scale, rotate, 3D, skew).
- **كيف / how:** Install with `npx hyperframes add motion-blur` (copies to compositions/components/motion-blur.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame …
- **أرقام / params:** shutterAngle 720; shutterPhase -360; samplesPerFrame 16; window [t-1/fps, t+1/fps]
- **تثبيت / install:** `npx hyperframes add motion-blur` (copies to compositions/components/motion-blur`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/motion-blur/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/motion-blur/motion-blur.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/motion-blur.mdx`

#### EASE-110 · مسافر على مسار · Offset Path Traveler · 📦 بأمر تثبيت
- **ماذا / what:** Slotted element follows an authored SVG path with tangent rotation and curved entry/exit.
- **كيف / how:** Install with `npx hyperframes add offset-path-traveler` (copies to compositions/components/offset-path-traveler.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headle…
- **أرقام / params:** path SVG d string; vars: path=M -90 390 C 150 490 190 70 430 185 C 650 300 720 105 850 145 C 970 180 1030 85 1090 35; traveler_label=Live preview; accent=green[green|blue|violet]
- **تثبيت / install:** `npx hyperframes add offset-path-traveler` (copies to compositions/components/offset-path-traveler`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/offset-path-traveler/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/offset-path-traveler/offset-path-traveler.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/offset-path-traveler.mdx`

#### EASE-111 · صدمة الغالق · Shutter Slam · 📦 بأمر تثبيت
- **ماذا / what:** One word thrown through six single-property beats (two translate slams, scale punch, full turn on each axis) under integrated shutter blur on easing measured from an AE export.
- **كيف / how:** Install with `npx hyperframes add shutter-slam` (copies to compositions/components/shutter-slam.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fram…
- **تثبيت / install:** `npx hyperframes add shutter-slam` (copies to compositions/components/shutter-slam`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/shutter-slam/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/shutter-slam/shutter-slam.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/shutter-slam.mdx`

#### EASE-112 · المسح الشقي · Slit Scan Reveal · 📦 بأمر تثبيت
- **ماذا / what:** Each row (or column) samples the subject at a different time offset, smearing arrival through time until offsets collapse to zero.
- **كيف / how:** Install with `npx hyperframes add slit-scan-reveal` (copies to compositions/components/slit-scan-reveal.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chrom…
- **أرقام / params:** axis rows|cols; spread 0.45; resolve_at 2.2 s; vars: axis=rows[rows|cols]; spread=0.45; resolve_at=2.2; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add slit-scan-reveal` (copies to compositions/components/slit-scan-reveal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/slit-scan-reveal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/slit-scan-reveal/slit-scan-reveal.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/slit-scan-reveal.mdx`

#### EASE-113 · قفزة نابضية · Spring Pop · 📦 بأمر تثبيت
- **ماذا / what:** Badge pops from near-rest scale, overshoots once and settles.
- **كيف / how:** Install with `npx hyperframes add spring-pop` (copies to compositions/components/spring-pop.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame ca…
- **أرقام / params:** fromScale 0.9; overshoot 1.7; vars: overshoot=1.7(1.1..2); fromScale=0.9(0.8..0.97); text=New
- **تثبيت / install:** `npx hyperframes add spring-pop` (copies to compositions/components/spring-pop`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/spring-pop/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/spring-pop/spring-pop.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/spring-pop.mdx`

#### EASE-114 · تتابع الشبكة · Stagger Cascade · 📦 بأمر تثبيت
- **ماذا / what:** Grid of tiles fades/travels into place with an even per-item stagger.
- **كيف / how:** Install with `npx hyperframes add stagger-cascade` (copies to compositions/components/stagger-cascade.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **أرقام / params:** itemCount 6; stagger 60 ms; vars: itemCount=6(3..12); stagger=60(20..150); direction=up[up|down|left|right]
- **تثبيت / install:** `npx hyperframes add stagger-cascade` (copies to compositions/components/stagger-cascade`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/stagger-cascade/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/stagger-cascade/stagger-cascade.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/stagger-cascade.mdx`

#### EASE-115 · شبكة متتابعة · Stagger Lattice · 📦 بأمر تثبيت
- **ماذا / what:** Staggered grid reveal in the spirit of Anime.js v4 stagger utilities, rebuilt in GSAP.
- **كيف / how:** Install with `npx hyperframes add stagger-lattice` (copies to compositions/components/stagger-lattice.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **تثبيت / install:** `npx hyperframes add stagger-lattice` (copies to compositions/components/stagger-lattice`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/stagger-lattice/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/stagger-lattice/stagger-lattice.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/stagger-lattice.mdx`

#### EASE-116 · إيقاع الستوب موشن · Stop Motion Cadence · 📦 بأمر تثبيت
- **ماذا / what:** Stepped-time law: one driver quantises time to floor(t*fps)/fps and feeds all motion; paper-cut shapes throw/land with squash, 2-frame boil, sparkles living 2-3 frames.
- **كيف / how:** Install with `npx hyperframes add stop-motion-cadence` (copies to compositions/components/stop-motion-cadence.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless…
- **أرقام / params:** fps 8|10|12; boil on|off; vars: fps=10[8|10|12]; boil=on[on|off]; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add stop-motion-cadence` (copies to compositions/components/stop-motion-cadence`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/stop-motion-cadence/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/stop-motion-cadence/stop-motion-cadence.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/stop-motion-cadence.mdx`

#### EASE-117 · رمي وتثبيت · Velocity Throw Snap · 📦 بأمر تثبيت
- **ماذا / what:** Five-shot rail whips past on a fast decaying curve, overshoots and snaps the hero shot to centre.
- **كيف / how:** Install with `npx hyperframes add velocity-throw-snap` (copies to compositions/components/velocity-throw-snap.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless…
- **أرقام / params:** hero_index 2; vars: hero_index=2(0..4); accent=green[green|blue|violet]; card_label_prefix=Shot
- **تثبيت / install:** `npx hyperframes add velocity-throw-snap` (copies to compositions/components/velocity-throw-snap`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/velocity-throw-snap/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/velocity-throw-snap/velocity-throw-snap.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/velocity-throw-snap.mdx`

#### EASE-118 · وضع اللعب · Example project: play-mode · 📦 بأمر تثبيت
- **ماذا / what:** Playful elastic-motion example with intro, stats and captions sub-compositions (Nunito, #0057FF, 10 s). [Local copy lacks its sub-compositions: compositions/captions.html, compositions/intro.html, compositions/stats.html.]
- **كيف / how:** Starter project: `npx hyperframes init --example play-mode` style scaffold (index.html mounts sub-compositions via data-composition-src); reuse its palette/type as a style reference.
- **أرقام / params:** 1920x1080; 10 s
- **تثبيت / install:** `npx hyperframes init --example play-mode` style scaffold (index`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/examples/play-mode/registry-item.json` · `kosif-one/vendor/hyperframes/registry/examples/play-mode/index.html`

#### EASE-119 · الكشف على امتداد اللقطة لا دفعة واحدة · Reveal across the whole shot (anti-slide rule) · 📦 بأمر تثبيت
- **ماذا / what:** Front-loading all content in the first ~25% then holding reads as a PowerPoint slide; pieces must reveal as the voiceover reaches them, especially in the back half of the shot.
- **كيف / how:** Map every Scene line to a timeline phase cued on the voiceover word; on silent frames cue on the beat.
- **أرقام / params:** avoid >~25% front-load
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/frame-worker-core.md`

#### EASE-120 · توقيت تلقائي حسب طول المحتوى · Content-length driven sequencing · 📦 بأمر تثبيت
- **ماذا / what:** A script array is reduced once into absolute [{start,end}] windows where each item's time = base + chars x secPerChar + hold, so longer content gets more screen time.
- **كيف / how:** Read hyperframes-animation/rules/dynamic-content-sequencing.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** duration = BASE_DURATION + body.length x SEC_PER_CHAR + hold; reserve min-height 160 px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/dynamic-content-sequencing.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### EASE-121 · تنفس وحركة خمول جيبية · Sine idle loop / breathing · 📦 بأمر تثبيت
- **ماذا / what:** Continuous breathing via sine.inOut yoyo with finite repeats, or an onUpdate phase driver for compound transforms; settle amplitude to zero in last ~20% for idles >6 s.
- **كيف / how:** Read hyperframes-animation/rules/sine-wave-loop.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** SCALE_AMP 0.008-0.015 default (0.02-0.04 isolated/kinetic)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/sine-wave-loop.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### EASE-122 · دخول بالقفز النابض · Spring pop entrance · 📦 بأمر تثبيت
- **ماذا / what:** The canonical arrival: scale 0 -> 1 (+ small y rise) with smooth long-tail settle; overshoot only for playful register; group stagger capped.
- **كيف / how:** Read hyperframes-animation/rules/spring-pop-entrance.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** fromTo {scale:0,opacity:0}->{scale:1,opacity:1,ease:'power3.out'}; group items x stagger <= 0.5 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/spring-pop-entrance.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### EASE-123 · انزلاق بطيء سريع بطيء · Nudge curve slow-fast-slow slide · 📦 بأمر تثبيت
- **ماذا / what:** Three chained tweens reposition a group: power3.in ramp, linear burst, power4.out tail.
- **كيف / how:** Read hyperframes-animation/rules/nudge-curve.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** distance 10/65/25 %; time ~20/18/62 %; tail >= 3x ramp-in
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/nudge-curve.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### EASE-124 · إعدادات توقيت الانتقال · Transition timing presets · 📦 بأمر تثبيت
- **ماذا / what:** Six named presets: snappy 0.2 s power4.inOut; smooth 0.4 s power2.inOut; gentle 0.6 s sine.inOut; dramatic 0.5 s power3.in->out; instant 0.15 s expo.inOut; luxe 0.7 s power1.inOut.
- **كيف / how:** Reference the preset name when planning transitions.
- **أرقام / params:** snappy/smooth/gentle/dramatic/instant/luxe
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/overview.md`

#### EASE-125 · مفردات التسارع والإعداد الافتراضي · Easing vocabulary and house default · 📦 بأمر تثبيت
- **ماذا / what:** power3.out is the house entrance ease; sine.inOut for calm/loops; expo.inOut for snappy hero transitions; none for camera/mechanical; steps(N) for typing/counters; back/elastic/bounce only for explicitly playful register (back N<=2); use ~3 easing characters per film.
- **كيف / how:** Timeline defaults {duration:0.6, ease:'power3.out'}; .out entrances, .in exits, .inOut symmetric.
- **أرقام / params:** default 0.6 s power3.out
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/gsap-easing-and-stagger.md`

#### EASE-126 · منحنى النابض المحسوب مسبقا · Baked spring ease (springEase) · 📦 بأمر تثبيت
- **ماذا / what:** Closed-form damped-spring position curve as a seek-safe GSAP ease; returns both duration (settle time within 0.1%) and ease.
- **كيف / how:** springEase({response, dampingFraction}); zeta 1.0 = no overshoot (house), 0.80-0.85 ~1-1.5% (iOS feel), 0.60-0.70 ~5-10% playful, <0.55 forbidden; response 0.25-0.35 -> 0.37-0.51 s, 0.35-0.5 -> 0.51-0.74 s, 0.5-0.7 -> 0.74-1.03 s; overshoot only on transforms not opacity.
- **أرقام / params:** EPS 0.001; N 4800 scan steps
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/gsap-easing-and-stagger.md`

#### EASE-127 · التتابع والقيم المحسوبة · Stagger and function-based values · 📦 بأمر تثبيت
- **ماذا / what:** GSAP stagger objects (each/amount/from) and index-based function values; a group arrival reads as one beat when items x stagger <= ~0.5 s.
- **كيف / how:** adapters/gsap-easing-and-stagger.md § Stagger / Function-Based Values.
- **أرقام / params:** items x stagger <= 0.5 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/gsap-easing-and-stagger.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### EASE-128 · علامات وتداخل الخط الزمني · GSAP timeline labels and nesting · 📦 بأمر تثبيت
- **ماذا / what:** Position parameter, labels and nested timelines; in sub-compositions prefer fromTo over from; play controls only for debug.
- **كيف / how:** adapters/gsap-timeline-and-labels.md; scene timelines added to the root must not be paused.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/gsap-timeline-and-labels.md`

#### EASE-129 · عقد الوضعيات المفتاحية · Keyframe pose contract · 📦 بأمر تثبيت
- **ماذا / what:** Keyframes are a pose contract: name the moving subject, the poses that prove the motion including the final state, keyframe visible channels, preserve object identity, crossfade only for replacement, final frame is part of the animation, never reset to rest or end on black unless asked.
- **كيف / how:** hyperframes-keyframes SKILL § Contract + Procedure (identify subject/states -> smallest mechanism -> author seek-safe -> verify with check, keyframes, --shot, snapshots).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/SKILL.md`

#### EASE-130 · سلم الوضعيات بإطارات GSAP · GSAP array/percentage keyframes (pose ladder) · 📦 بأمر تثبيت
- **ماذا / what:** Multi-stop motion on one subject via GSAP keyframes arrays (per-step duration/ease), percentage keyframes, property arrays, ease none on parent with per-stop eases, or easeEach.
- **كيف / how:** tl.to('.subject',{keyframes:[{x:0,duration:0.2},{x:120,duration:0.4,ease:'power2.out'},{x:100,duration:0.2,ease:'power2.inOut'}],ease:'none'}); labels for semantic states; immediateRender:false on later from/fromTo.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/SKILL.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/references/keyframe-patterns.md`

#### EASE-131 · اختيار آلية الحركة المناسبة · Mechanism choice table for motion · 📦 بأمر تثبيت
- **ماذا / what:** Map the need to the smallest mechanism: same subject changes box -> FLIP/shared element; route -> path travel; trace -> stroke draw; shape change -> shape interpolation (MorphSVG); visible reveal boundary -> clip/mask/shader uniform; ordered many -> stagger; moving text -> line/word/char/band subdiv…
- **كيف / how:** keyframes SKILL § Mechanism Choice; prefer DrawSVGPlugin then dasharray; MorphSVGPlugin for morphs.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/SKILL.md`

#### EASE-132 · مبادئ التوقيت: التمهيد والمتابعة والثبات · Motion timing doctrine (anticipation, follow-through, holds) · 📦 بأمر تثبيت
- **ماذا / what:** Anticipation only when it clarifies cause; follow-through sells energy; overshoot only for elastic subjects; constant path travel uses ease none; discrete UI states sharp ease-out; final lockups hold longer; avoid big clip-path changes while the same surface scales.
- **كيف / how:** keyframes SKILL § Timing.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/SKILL.md`

#### EASE-133 · بناء ثم تنفس ثم حسم · Build / breathe / resolve scene structure · 📦 بأمر تثبيت
- **ماذا / what:** Every scene: build 0-30% staggered entries, breathe 30-70% with ONE ambient motion, resolve 70-100% decisive exit (exits faster than entrances); speed communicates weight (0.15-0.3 urgent, 0.3-0.5 professional, 0.5-0.8 luxury, 0.8-2.0 cinematic).
- **كيف / how:** references/motion-principles.md.
- **أرقام / params:** 0-30/30-70/70-100 %
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/motion-principles.md`

#### EASE-134 · أنواع حركة البطاقات الثلاث عشرة · Recut card animation kinds (data-anim, 13) · 📦 بأمر تثبيت
- **ماذا / what:** Closed declarative list compiled into the master timeline: fade-in, fade-out, slide-in (from, distance), kinetic-chars (pop|fade, stagger), typewriter, count-up (from, to, format .0f/.1f/.2f/,d), draw-path, grow-y (target-h), grow-x (target-w), scale-pop, blur-in, mask-reveal (direction), morph-to (…
- **كيف / how:** data-anim + data-anim-at (seconds relative to card start, quantized to 1/fps).
- **أرقام / params:** 13 kinds
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/talking-head-recut/SKILL.md`

#### EASE-135 · انضباط مدد المجموعات · Group duration discipline for music frames · 📦 بأمر تثبيت
- **ماذا / what:** Best span is the active treatment span; frames over ~6 s usually need 2+ groups; roll templates are one-roll tools; split at the next downbeat when a template would run long.
- **كيف / how:** references/template-catalog.md § Group duration discipline.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/template-catalog.md`

#### EASE-136 · عقيدة لغة الحركة · Motion language doctrine (narrative workflows) · 📦 بأمر تثبيت
- **ماذا / what:** Smooth beats bouncy (power3 default); sequential reveal in the back ~50% timed to the voiceover; no lazy breathing and no bad pan/push ('no motion over bad motion'); internal seams are velocity-matched cuts; move vocabulary for kinetic type, typewriter, count-up, decode, camera, layout, surface/UI, …
- **كيف / how:** references/motion-language.md Parts 1-3.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/faceless-explainer/references/motion-language.md`

#### EASE-137 · عائلات التسهيل · Ease families E.out/exit/inOut/whip/cam/rest · 📦 بأمر تثبيت
- **ماذا / what:** Three curve families by role: expo-out arrivals, ease-in exits into cuts, steep in-out or momentum for camera; linear only for drift/data/light.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** out: velocity x0.92/frame settle 18–55 f; exit x1.14/frame over 10–24 f
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### EASE-138 · النوابض الفيزيائية · Critically damped springs SPR · 📦 بأمر تثبيت
- **ماذا / what:** Springs firm/soft/heavy default; snap/pop/land only for surface landings, max 2 per film; overshoot 0 or 1–4%.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** SPR.firm|soft|heavy|snap|pop|land
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### EASE-139 · الانضغاط عند التلامس · Squash on contact · 📦 بأمر تثبيت
- **ماذا / what:** Contact squash and shape settling before position.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** 8%/10% over 8 f; shape settles 6 f before position
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### EASE-140 · التتابع · stagger · 📦 بأمر تثبيت
- **ماذا / what:** List items arriving one by one.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** MOTION.stagger
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### EASE-141 · منحنيات حركة حسب الدور · Role-based easing tokens · 📦 بأمر تثبيت
- **ماذا / what:** Each kind of move gets its own curve: arrivals, exits, whips, camera pushes, UI nudges, impacts, typewriters, irises; five_sec states 'four easings, no wall clock'.
- **كيف / how:** M.ease {slam expo.out, snap back.out(1.3), drive power4.inOut, settle power4.out}; M.E cubic-beziers: out (.16,1,.3,1), outSoft (.22,1,.36,1), in (.7,0,.84,0), exit (.55,.055,.675,.19), inOut (.87,0,.13,1), smooth (.65,0,.35,1), ui (.4,0,.2,1), cam (.48,.1,0,.9), glide (.47,.2,.15,1), rest (.45,0,.1,1), contact (.55,0,.9,.55), whip (.6,0,.15,1), dolly (.35,0,.65,1), type (.5,1,.89,1), iris (.4,0,.7,.92), shutter (.2,.7,.2,1), hop (.35,0,.7,.85).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:31` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:69` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:12`

#### EASE-142 · مط وضغط مع حفظ الحجم · Volume-preserving squash and stretch · 📦 بأمر تثبيت
- **ماذا / what:** Impacts and loads squash objects while keeping volume, plus landing squash on a dropped dot and a character hop with landing wobble.
- **كيف / how:** orb: sq = 1 − .16·kick, stretch = 1/√sq; M.squash(tl, dot, .42, {edge:'bottom', across:.22, along:.26, dur:.18}); bunny: scale (1+.5sq−.4land, 1−sq+breath+land), hop sin(π·u)·.026 over .42 s, land = e^(−7x)·sin(30x)·.05.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:106` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:70` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:118`

#### EASE-143 · مفاتيح مأخوذة بالعينات لركوب مسار · Seek-safe sampled keyframes for path riding · 📦 بأمر تثبيت
- **ماذا / what:** Following an SVG path is baked into dense keyframes so scrubbing to any time gives the right position (no onUpdate callbacks).
- **كيف / how:** tl.to(dot, {keyframes: M.sampled(t → path.getPointAtLength(L·E.out((t−b9)/1.15)), b9, b9+1.15, 60)}, b9) → 60 fps sub-keys with ease 'none'.
- **أرقام / params:** 60 samples/s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:102` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:109`

#### EASE-144 · تتبع متعدد الأهداف · MOTION.track multi-target · 📦 بأمر تثبيت
- **ماذا / what:** Value with several targets as sum of one spring per change, pure function of t.
- **كيف / how:** MOTION.track(t,[[time,value],...],preset)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md` · `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### EASE-145 · تغيير السرعة · Speed ramp exact integral · 📦 بأمر تثبيت
- **ماذا / what:** Speed keys linear, time map integrated; optional minterpolate.
- **كيف / how:** clips[].ramp [[t,speed],...]; speed 0.1-10 atempo; interpolate:true
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`

#### EASE-146 · تكامل: LottieFiles motion-design skill · Integration: LottieFiles motion-design skill · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### EASE-147 · تكامل: GSAP · Integration: GSAP · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### EASE-148 · تكامل: Motion + AI Kit · Integration: Motion + AI Kit · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### EASE-149 · تكامل: Theatre.js · Integration: Theatre.js · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### EASE-150 · نابض مغلق الصيغة للنصوص · Closed-form overlay spring (k300 c30) · 📦 بأمر تثبيت
- **ماذا / what:** Seek-safe spring for DOM overlays: an analytic damped-oscillator step response, so any frame can be rendered out of order.
- **كيف / how:** spring(x)=1-e^(-zwx)(cos(wd x)+(zw/wd) sin(wd x)), w=sqrt(300), z=30/(2w); overlays use opacity=clamp(spring(t-t0)*1.4)*(1-out) and translateY((1-s)*70) scale(.92+.08s); plus easeInOutCubic and easeOutCubic.
- **أرقام / params:** stiffness 300, damping 30, mass 1 (zeta ~0.87, slight overshoot)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html:58-64` · `kosif-one/projects/egypt-2120-animation/index.html:469-476`

#### EASE-151 · ظهور منبثق مع تمويه · Blur pop-in / pop-out keyword · 📦 بأمر تثبيت
- **ماذا / what:** Keywords and chips pop in from small and blurred with a slight overshoot, and leave by growing and blurring out.
- **كيف / how:** in: scale .4, opacity 0, blur 16 px -> 1, 1, 0 in 0.55 s back.out(1.3); out: scale 1.12, opacity 0, blur 10 px in 0.25 s E.in.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html:209-213`

#### EASE-152 · كلمة تقفز بالضغط والمط · Squash-and-stretch jumping word · 📦 بأمر تثبيت
- **ماذا / what:** The word 'بيتنطط' (he jumps around) jumps three times with stretch on take-off and squash on landing.
- **كيف / how:** Three hops 0.42 s apart: y 0 -> -90 scaleY 1.08 in 0.2 s E.out; y 0 scaleY .86 in 0.18 s E.contact; scaleY 1 in 0.12 s.
- **أرقام / params:** hop height 90 px; squash .86; stretch 1.08
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html:243-250`

#### EASE-153 · اهتزاز الضحك · Laughing wiggle · 📦 بأمر تثبيت
- **ماذا / what:** A word wobbles left-right quickly to read as laughter.
- **كيف / how:** rotation -4 -> 4 degrees, 0.12 s yoyo, repeat 7, sine.inOut.
- **أرقام / params:** ±4 degrees, 0.12 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html:252`

#### EASE-154 · رموز التسهيل في مكتبة الحركة · Motion Kit easing tokens (E) · 📦 بأمر تثبيت
- **ماذا / what:** A house set of cubic-bezier curves, one family per role, usable directly as GSAP eases.
- **كيف / how:** M.E.<name> built by bezier(x1,y1,x2,y2) (Newton solve 8 iterations); named GSAP eases M.ease: slam expo.out, snap back.out(1.3), drive power4.inOut, settle power4.out.
- **أرقام / params:** out (.16,1,.3,1); outSoft (.22,1,.36,1); in (.7,0,.84,0); exit (.55,.055,.675,.19); inOut (.87,0,.13,1); smooth (.65,0,.35,1); ui (.4,0,.2,1); cam (.48,.1,0,.9); glide (.47,.2,.15,1); rest (.45,0,.1,1); contact (.55,0,.9,.55); whip (.6,0,.15,1); dolly (.35,0,.65,1); type (.5,1,.89,1); iris (.4,0,.7,…
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:12-41` · `kosif-one/projects/thursday-dua-animation/source/assets/motion-kit.js`

#### EASE-155 · إعدادات النوابض · Spring presets (normalised + physical) · 📦 بأمر تثبيت
- **ماذا / what:** Two spring families: normalised oscillator eases for GSAP and physical damped springs (closed form, seekable, retargetable via track()).
- **كيف / how:** M.spring('snappy'|'default'|'heavy'|'playful') as ease; M.springStep(t,M.SPR.x); M.track(t,[[t0,v0],[t1,v1]...],preset) sums one spring per target change; M.zoomTrack works in log space.
- **أرقام / params:** SPRINGS snappy z.62 w20, default z.74 w17, heavy z1 w13, playful z.45 w18; SPR snap d18 k260 m.7, pop d11 k180 m.6, land d14.5 k200 m1, micro d30 k500 m.6, firm d24 k140 m1, soft d26 k120 m1, heavy d30 k90 m1.4
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:51-88`

#### EASE-156 · غلاف النبضة ومدة حسب المسافة · hitPulse envelope and distance-based durations · 📦 بأمر تثبيت
- **ماذا / what:** One envelope for every punch/tick (sine attack, exponential decay, counted in 60 fps frames) and a rule that move duration grows with distance.
- **كيف / how:** hitPulse(t,attack=2,tau=5); durFor(px,camera)=0.35 s + 1.35 ms/px, camera clamped 0.6-2.4 s.
- **أرقام / params:** attack 2 f, tau 5 f @60 fps; 0.35 s + 0.00135 s/px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:46-49`

#### EASE-157 · مفاتيح حركة من دالة زمنية · Seek-safe sampled keyframes from code · 📦 بأمر تثبيت
- **ماذا / what:** Any function of time becomes GSAP keyframes sampled at 60 per second, so procedural motion survives paused seeking.
- **كيف / how:** M.sampled(fn,t0,t1,fps=60) -> [{duration:1/60,ease:'none',...fn(t)}]; used by moveCursor.
- **أرقام / params:** 60 samples per second
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:108-109`

#### EASE-158 · دحرجة ثلاثية وقلب الألوان وضغط الاصطدام · 3D roll, polarity flip, contact squash · 📦 بأمر تثبيت
- **ماذا / what:** Three punctuation moves: a front-loaded 3D roll-in from -90 degrees, an ink/paper colour flip at act boundaries, and a squash against the edge an object hits.
- **كيف / how:** M.roll(tl,el,at,{from:-90,dur:.17,perspective:2200}); M.polarity(tl,stage,at,bg,fg) 0.1 s; M.squash(tl,el,at,{edge,across:.08,along:.10,dur:.13}).
- **أرقام / params:** roll 10 frames; squash 8 frames +8%/-10%
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:361-376`

#### EASE-159 · لقطة السرعة U · U-speed shot (enter fast, cruise, exit into cut) · 📦 بأمر تثبيت
- **ماذا / what:** An element enters fast and decays, keeps drifting slowly while it is read, then accelerates out right into the cut.
- **كيف / how:** M.shot(tl,el,at,{enter:.45,exit:.3,cut,dir:'x',dist:220,cruise:1.2}) enter E.out, cruise linear, exit E.exit by dist*1.4.
- **أرقام / params:** cruise 1.2 px/frame
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:392-401`

#### EASE-160 · سرعات الرسم · Painting speed presets · 📦 بأمر تثبيت
- **ماذا / what:** Studio drawing speed for the pixel-by-pixel playback.
- **كيف / how:** studio.SPEEDS.
- **أرقام / params:** بطيء 5.0, عادي 1.8, سريع 0.55, فوري 0
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/studio.py:46`

#### EASE-161 · منحنى تقدّم الانتقال المقاس · Measured transition progress curves · 📦 بأمر تثبيت
- **ماذا / what:** Transition easing extracted from the reference by re-synthesis and replayed frame-exactly.
- **كيف / how:** mm_analyze classifies; mm_build replays curve
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-mimic/scripts/mm_build.py:1`

#### EASE-162 · زمن الرسم وسرعاته · Drawing-time model and speed presets · 📦 بأمر تثبيت
- **ماذا / what:** Each step's drawing duration scales with the square root of its changed-pixel share times its weight, so small details are quick and the sky is slow; four named speeds.
- **كيف / how:** tick(): dur = SPEEDS[speed] * step.weight * sqrt(n/area); pixels revealed linearly in time; UI timer 12 ms; film uses the same formula per frame.
- **أرقام / params:** بطيء 5.0 s, عادي 1.8 s, سريع 0.55 s, فوري 0 (seconds per full-sheet step); film speeds slow 5.0 / normal 1.8 / fast 0.55
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/studio.py:46` · `kosif-studio/studio.py:535` · `kosif-studio/film.py:28`

#### EASE-163 · ساعة الإيقاع في التركيب · Beat clock in compositions · 📦 بأمر تثبيت
- **ماذا / what:** Animations are placed by beat number from a BPM so picture and score share one clock.
- **كيف / how:** const B = M.beats(120), b = B.at; tl.to(x, {...}, b(4))
- **أرقام / params:** 120 BPM → beat n at n×0.5 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/showreel/index.html:61`

#### EASE-164 · تقسيم المشاهد حسب المدة · Duration-proportional scene layout · 📦 بأمر تثبيت
- **ماذا / what:** Scene lengths are derived from total frames (34% / 40% / remainder) so the film rescales when duration follows the audio.
- **كيف / how:** sceneLayout(total)
- **أرقام / params:** s1=round(.34T), s2=round(.40T)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/starters/remotion/src/Film.tsx:58`

#### EASE-165 · دوال تسهيل Remotion · Dependency-free easing set (Remotion) · 📦 بأمر تثبيت
- **ماذا / what:** linear, easeOutCubic, easeInOutCubic, easeOutExpo, easeInOutSine, easeOutBack (c=1.70158), progress(frame,start,length,ease), staggerStart(i,step,offset).
- **كيف / how:** import from ./easing; pass to interpolate({easing})
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/starters/remotion/src/easing.ts`

#### EASE-166 · ظهور مع تمويه · Blur fade-up reveal · 📦 بأمر تثبيت
- **ماذا / what:** Elements enter translateY 4rem + blur 12px + opacity 0 -> rest over 1000 ms with stagger var(--d).
- **كيف / how:** IntersectionObserver rootMargin -10% adds .is-in.
- **أرقام / params:** 800-1000 ms
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/ai-design-skills/skills/landing-page-design/SKILL.md` · `kosif-one/vendor/mcp-higgsfield-landing/src/styles/global.css:181` · `kosif-one/vendor/mcp-higgsfield-landing/src/scripts/motion.ts:25`

#### EASE-167 · تمرير ناعم GSAP وLenis · GSAP+Lenis smooth scroll sync · 📦 بأمر تثبيت
- **ماذا / what:** Lenis autoRaf off driven by gsap.ticker, lagSmoothing(0), lenis.on scroll -> ScrollTrigger.update.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/mcp-higgsfield-landing/src/scripts/motion.ts:18`

#### EASE-168 · كرة بانضغاط وتمدد · Squash and stretch ball · 👁 شوهد في فيديو
- **ماذا / what:** scaleY = 1 - k·impact, scaleX = 1 + k·impact on contact; stretch along velocity in flight; preserve area
- **أرقام / params:** squash 0.65/1.35 for ~3 frames; stretch 1.2 at max speed
- **الدليل / proof:** `style:pm-chatgptastra-0d95c7` · `style:pm-eyishazyer-af035b` · `style:pm-zheke-38deff`

#### EASE-169 · نسخ شبحية لإظهار تباعد الحركة · Onion-skin spacing ghosts · 👁 شوهد في فيديو
- **ماذا / what:** sample object position at fixed frame intervals and draw outline copies at low opacity, so spacing reveals the easing
- **أرقام / params:** every 2-3 frames, 8-12 ghosts, 1 px outline 40% opacity
- **الدليل / proof:** `style:pm-chatgptastra-0d95c7` · `style:pm-himanshutwtxs-5f4b43`

#### EASE-170 · لوحة مقارنة منحنيات التسارع · Easing comparison board · 👁 شوهد في فيديو
- **ماذا / what:** Rows: index, easing name, small curve glyph, track A→B; a coloured ball per row runs the same distance in the same duration with linear/easeInOut/expoOut/backOut/elastic/bounce
- **أرقام / params:** duration 0.94 s, rows 6, ball r 14px
- **الدليل / proof:** `style:pm-roundtablespace-d3a1be` · `style:pm-stephanlivera-df17a2`

#### EASE-171 · معامل بطء واحد للتوقيت · Global slowness factor TS · 👁 شوهد في فيديو
- **ماذا / what:** express all timings as step units multiplied by one TS constant so the whole lesson can be slowed/sped uniformly, while continuous motions run on real time
- **أرقام / params:** TS ~1.0-1.4
- **الدليل / proof:** `style:chalkboard`

#### EASE-172 · كرت يقفز لكل جملة · Sentence prop pop-in · 👁 شوهد في فيديو
- **ماذا / what:** for every sentence spawn one visual prop (sign, question bubble, heart card) with spring scale 0 -> 1.08 -> 1 and slight rotation
- **أرقام / params:** 300-400 ms, damping ~12
- **الدليل / proof:** `style:doodle`

#### EASE-173 · مسار عربية بمراحل وقفزة تخفي الدوران · Piecewise vehicle timeline with hop-masked turns · 👁 شوهد في فيديو
- **ماذا / what:** position(t) as segments (wait, reverse, exit, stop at light, continue); when heading flips, add 120 ms hop + squash to hide the sprite swap
- **أرقام / params:** squash scaleY 0.9, hop 6 px
- **الدليل / proof:** `style:isometric`

#### EASE-174 · قفزة الكرتونة بقوس بين حاملين · Parabolic object hop between carriers · 👁 شوهد في فيديو
- **ماذا / what:** lerp xy between start/end, z = h*4t(1-t); when landed, parent the box to the carrier so it inherits motion
- **أرقام / params:** h ~1.5 units, 400 ms
- **الدليل / proof:** `style:isometric`

#### EASE-175 · ختم حالة يُطبع على البطاقة · Stamp badge (DOWN / REJECTED / EXPIRED) · 👁 شوهد في فيديو
- **ماذا / what:** black rounded badge with white text scales from 1.4→1 with rotation -8° and slight shake; underlying card switches to hatched grey
- **أرقام / params:** 250 ms back.out, shake 2 frames
- **الدليل / proof:** `style:pm-0xnfrith-5be616`

#### EASE-176 · كرة التوقيت · Bouncing ball timing · 👁 شوهد في فيديو
- **ماذا / what:** y with gravity ease, squash 1.2x on impact
- **الدليل / proof:** `style:pm-3xtihor-0f6911`

#### EASE-177 · تبديل العناوين بتلاشٍ متقاطع · Headline crossfade swap · 👁 شوهد في فيديو
- **ماذا / what:** Outgoing headline moves y -12px and fades, incoming from +12px; overlap 200 ms
- **أرقام / params:** 500ms easeInOut
- **الدليل / proof:** `style:pm-ai-baymax-0ef9dd`

#### EASE-178 · قفز متتابع إلى الخانات · Staggered hop-into-grid · 👁 شوهد في فيديو
- **ماذا / what:** each tile follows parabolic arc to cell centre with rotation settling; stagger 180 ms; easeOutBack on landing with tiny bounce
- **أرقام / params:** arc height 0.6 tile, duration 450 ms
- **الدليل / proof:** `style:pm-anilraok-eff262`

#### EASE-179 · كرة مرتدة مع أشباح · Bouncing ball with onion skin · 👁 شوهد في فيديو
- **ماذا / what:** ball on axis, squash 0.8 at contact, ghost copies at frame steps
- **أرقام / params:** bounce 600ms
- **الدليل / proof:** `style:pm-blue-clarity-ef56d0`

#### EASE-180 · شريط تقدم سفلي · Global progress bar · 👁 شوهد في فيديو
- **ماذا / what:** Thin accent bar along bottom edge grows linearly with total time
- **أرقام / params:** 3 px, 0->100% over duration
- **الدليل / proof:** `style:pm-blushpetal795-0c85c2`

#### EASE-181 · طفو المنتج · Floating product idle · 👁 شوهد في فيديو
- **ماذا / what:** Sine bob y ±6 px with soft shadow scaling inversely
- **أرقام / params:** period 2.5 s
- **الدليل / proof:** `style:pm-cansincengiz-me-cf68dd`

#### EASE-182 · ختم يُطبع بقوة · Paid stamp slam · 👁 شوهد في فيديو
- **ماذا / what:** Outlined green stamp label scales from 1.6 to 1 with slight rotation (-8 deg) and a 2-frame overshoot/shake, landing on the corner of a card
- **أرقام / params:** 180 ms, easeOutBack
- **الدليل / proof:** `style:pm-ceowinkz-7c776b`

#### EASE-183 · شريط تقدم الفصول · Chapter progress bar · 👁 شوهد في فيديو
- **ماذا / what:** thin green line at bottom fills per chapter + label top-left
- **الدليل / proof:** `style:pm-charlesmendez-73b6e4`

#### EASE-184 · عرض منحنى التسهيل · Easing curve demo · 👁 شوهد في فيديو
- **ماذا / what:** draw cubic-bezier with handles, pills sliding with that ease
- **الدليل / proof:** `style:pm-codestackr-c071bf`

#### EASE-185 · ارتداد مع انضغاط · Squash bounce · 👁 شوهد في فيديو
- **ماذا / what:** Ball falls with gravity, squash on contact, ellipse shadow ring expands
- **الدليل / proof:** `style:pm-crazyalphaaa-bc7e75`

#### EASE-186 · إيقاع لقطات متساوٍ · Even shot cadence · 👁 شوهد في فيديو
- **ماذا / what:** cut every 7.5 s = musical phrase
- **الدليل / proof:** `style:pm-davidshulmanfl-371638`

#### EASE-187 · انزلاق مفتاح التبديل · Toggle knob slide · 👁 شوهد في فيديو
- **ماذا / what:** translateX knob + bg color swap
- **أرقام / params:** 250 ms spring
- **الدليل / proof:** `style:pm-demonugc-4c5753`

#### EASE-188 · جملة مقسومة ذهاباً وإياباً · Split-sentence round trip · 👁 شوهد في فيديو
- **ماذا / what:** write the script so the first half of each sentence is said on the way down and the second half on the way back up
- **أرقام / params:** mirror structure
- **الدليل / proof:** `style:pm-emollick-8661a8`

#### EASE-189 · ضبابية حركة للأزرار · Button motion smear · 👁 شوهد في فيديو
- **ماذا / what:** duplicate element echoes at low opacity along velocity during fast moves
- **أرقام / params:** 3-4 echoes
- **الدليل / proof:** `style:pm-en-ra-81c6dd`

#### EASE-190 · شبكة إيقاع · Rhythm grid stagger · 👁 شوهد في فيديو
- **ماذا / what:** squares flip/scale on beat, stagger by distance
- **الدليل / proof:** `style:pm-eyishazyer-af035b`

#### EASE-191 · سقوط كلمة بميل ثم استقرار · Tilt-settle word drop · 👁 شوهد في فيديو
- **ماذا / what:** Enter with rotate 4° and y-30, spring to 0
- **أرقام / params:** 400 ms
- **الدليل / proof:** `style:pm-gdgtify-287ddf`

#### EASE-192 · نقاط مرقمة تظهر تباعًا · Sequential numbered bullets · 👁 شوهد في فيديو
- **ماذا / what:** rows fade-up 12 px with a numbered square badge in accent colour; space them to narration (~2 s)
- **أرقام / params:** fade 300 ms, stagger to voice
- **الدليل / proof:** `style:pm-gigabit-million-16b3a0`

#### EASE-193 · تدرج الحروف على قوس · Per-letter arc stagger · 👁 شوهد في فيديو
- **ماذا / what:** letters offset y/rotate along sine
- **أرقام / params:** stagger 40ms
- **الدليل / proof:** `style:pm-hanifproduktif-54bdee`

#### EASE-194 · تلطيخ ضبابي · Motion blur smear · 👁 شوهد في فيديو
- **ماذا / what:** duplicate offset copies with opacity falloff
- **الدليل / proof:** `style:pm-hanifproduktif-54bdee`

#### EASE-195 · خط تقدم سفلي · Bottom progress line · 👁 شوهد في فيديو
- **ماذا / what:** 2px accent line width = t/duration
- **الدليل / proof:** `style:pm-hqmank-7c61f1`

#### EASE-196 · إيقاع هادئ بتوقفات طويلة · Calm hold pacing · 👁 شوهد في فيديو
- **ماذا / what:** Each beat: ~400-600 ms of motion followed by 3-5 s hold to let the viewer read
- **أرقام / params:** beat length ~5 s, motion 10-15%
- **الدليل / proof:** `style:pm-iammxfschr-d68f90`

#### EASE-197 · كرة قافزة بأثر شفاف لمسارها · Onion-skin bouncing ball · 👁 شوهد في فيديو
- **ماذا / what:** Simulate ball with gravity and restitution, squash on contact (scaleX 1.2, scaleY 0.8), and leave outline ghost circles every N frames along the arc with dotted path
- **أرقام / params:** restitution 0.6, ghost every 3 frames, ghost stroke 1 px 40% opacity
- **الدليل / proof:** `style:pm-ik-builds-b8bdcf`

#### EASE-198 · حلقة مغلقة بلا قطع · Seamless loop closure · 👁 شوهد في فيديو
- **ماذا / what:** Make the season parameter cyclic and end the timeline at the same scroll phase/state as frame 0 so the video loops endlessly
- **أرقام / params:** period = duration
- **الدليل / proof:** `style:pm-itsolelehmann-e47532`

#### EASE-199 · منحنى التسارع الظاهر · Visible easing curve · 👁 شوهد في فيديو
- **ماذا / what:** small plot of easing fn with moving dot synced to shape
- **أرقام / params:** outElastic 0.48s
- **الدليل / proof:** `style:pm-itsuki-dev-10942d`

#### EASE-200 · دخول خاطف بضبابية حركة · Motion-blur whip entrance · 👁 شوهد في فيديو
- **ماذا / what:** translate the word ~40% of frame width in 4-6 frames with a directional blur proportional to velocity (or stack 6-8 offset copies at decreasing opacity), then hard stop
- **أرقام / params:** 150-250 ms, easeOutExpo, blur 30-60 px
- **الدليل / proof:** `style:pm-jhylee95-e1152f`

#### EASE-201 · حلقات حركة محيطية للحياة · Ambient loops for life (pendulum, rocking) · 👁 شوهد في فيديو
- **ماذا / what:** sine rotation of pendulum (±18°, 1 s) and rocking chair (±4°, 2 s) so static interiors feel alive
- **أرقام / params:** ease sine, phase offsets
- **الدليل / proof:** `style:pm-kamstudiolabs-0b0824`

#### EASE-202 · وميض المفتاح عند الضرب · Hit-flash key response · 👁 شوهد في فيديو
- **ماذا / what:** On impact, key brightens to full accent, dips down and springs back with damped oscillation, glow decays exponentially
- **أرقام / params:** dip 4 px, spring k=300 d=18, glow decay 300 ms
- **الدليل / proof:** `style:pm-kamstudiolabs-447565`

#### EASE-203 · دائرة أثر الاصطدام · Impact ripple marker · 👁 شوهد في فيديو
- **ماذا / what:** on each collision spawn an outline circle at contact point, radius 6->22px, alpha 0.8->0 over ~250 ms ease-out
- **أرقام / params:** 1px stroke, ring colour
- **الدليل / proof:** `style:pm-kantamk-61f410`

#### EASE-204 · فقاعة تعليق منبثقة · Comment bubble pop · 👁 شوهد في فيديو
- **ماذا / what:** Avatar dot + card with author, 'just now' and one-line story pops beside a frame with scale 0.9 -> 1 and fade, holds ~1.5 s
- **أرقام / params:** 200 ms easeOutBack
- **الدليل / proof:** `style:pm-kikelopezdesign-7cc9e8`

#### EASE-205 · مونتاج بطاقات خاطفة · Rapid flash-card montage · 👁 شوهد في فيديو
- **ماذا / what:** Sequence of full-bleed cards (one word each) hard-cut every ~250 ms with an NN/48 counter to create a chaos climax
- **أرقام / params:** 8th-note cuts, alternating coral/black grounds
- **الدليل / proof:** `style:pm-kloss-xyz-15182a`

#### EASE-206 · بناء بطيء ثم ضربة · Slow-burn then slam pacing · 👁 شوهد في فيديو
- **ماذا / what:** keep 6-7 s of near-still frame with tiny light changes, then a sudden collapse + cut to a full-weight title for contrast
- **أرقام / params:** energy <0.01 then spike
- **الدليل / proof:** `style:pm-kloss-xyz-b9b3f6`

#### EASE-207 · تحريك على اثنين · On-twos cutout animation · 👁 شوهد في فيديو
- **ماذا / what:** update cutout transforms at 15 fps while camera runs at 30 fps for a hand-made stop-motion feel
- **أرقام / params:** hold each pose 2 frames
- **الدليل / proof:** `style:pm-koldo2k-5cff87`

#### EASE-208 · لكمة نص بضبابية حركة · Motion-blur type punch · 👁 شوهد في فيديو
- **ماذا / what:** Short word enters fast from side with directional blur 40px->0 and slight scale overshoot on a contrasting full-colour ground
- **أرقام / params:** 250ms
- **الدليل / proof:** `style:pm-leadnotifi-e83f94`

#### EASE-209 · كرة ترتد بضغط وتمدد مع آثار شبحية · Squash-and-stretch bounce with onion skin · 👁 شوهد في فيديو
- **ماذا / what:** Ball follows parabolic arcs, scaleY 0.6/scaleX 1.4 at impact, stretch on fall; draw 6-8 fading ghost copies and a dotted path, with labelled callouts and a frame ruler/playhead
- **أرقام / params:** ghost opacity 0.1-0.4, impact squash 80 ms
- **الدليل / proof:** `style:pm-levabashidze-2d713a`

#### EASE-210 · دوران النجمة بضبابية · Spinning starburst blur · 👁 شوهد في فيديو
- **ماذا / what:** rotate fast with motion blur then settle to logo
- **أرقام / params:** ~600 ms
- **الدليل / proof:** `style:pm-lexnlin-038035`

#### EASE-211 · مونتاج ثلاثيات بالتصنيف · Category triptych montage · 👁 شوهد في فيديو
- **ماذا / what:** Split frame into 3 vertical photos; hard-cut the set every 0.5 s with one centred italic-serif word naming the category (Portraits., Yours.)
- **أرقام / params:** cut 500 ms, word 120 px serif italic
- **الدليل / proof:** `style:pm-listudio-820c7b`

#### EASE-212 · مخطط تسهيل مصغر · Easing graph inset · 👁 شوهد في فيديو
- **ماذا / what:** small HUD plot of easing with moving dot
- **الدليل / proof:** `style:pm-m1n9-k7-ff9ab9`

#### EASE-213 · بطاقات عناوين متلاحقة سريعة · Rapid-fire title cards · 👁 شوهد في فيديو
- **ماذا / what:** sequence of full-frame single-word cards, each held 3-10 frames, hard cuts on music hits; accelerate toward the reveal
- **أرقام / params:** 20+ cuts in 6 s at 30 fps
- **الدليل / proof:** `style:pm-majin-appsheet-2d3c1a`

#### EASE-214 · مؤقت تنازلي · Countdown pressure timer · 👁 شوهد في فيديو
- **ماذا / what:** mm:ss.cc decreasing fast to 00:00.00 then 'FINAL'
- **الدليل / proof:** `style:pm-marklaunches-3b9492`

#### EASE-215 · إبراز تدريجي لقائمة · Checklist progressive highlight · 👁 شوهد في فيديو
- **ماذا / what:** Vertical list of 4 serif words all dimmed 40%; on each beat one word goes to full white and gets an accent underline that wipes in from left; previous ones stay lit
- **أرقام / params:** beat interval ~250-300 ms
- **الدليل / proof:** `style:pm-marouanegazouzi-6071d5`

#### EASE-216 · إعادة ترتيب التخطيط بانسيابية · Layout reflow morph · 👁 شوهد في فيديو
- **ماذا / what:** FLIP animate boxes from old to new positions/sizes; collapse detail list into one chip row
- **أرقام / params:** 600 ms cubic-bezier(.65,0,.35,1)
- **الدليل / proof:** `style:pm-moguzbulbul-6311b6`

#### EASE-217 · قطع على الإيقاع · Beat-grid scene cuts · 👁 شوهد في فيديو
- **ماذا / what:** cut every 4 beats at 120 BPM = 2 s, or 3.75 beats
- **أرقام / params:** bpm=120
- **الدليل / proof:** `style:pm-mrtanviir-132457`

#### EASE-218 · كلمة واحدة لكل نبضة · One-word-per-beat serif cuts · 👁 شوهد في فيديو
- **ماذا / what:** hard cut italic serif words with ground colour flips each beat
- **أرقام / params:** 250-500 ms
- **الدليل / proof:** `style:pm-ndhabarde11-f155b4`

#### EASE-219 · تسهيل أُسّي بحيث لا تبدأ أي لقطة ساكنة · Always-moving exponential ease-out · 👁 شوهد في فيديو
- **ماذا / what:** Each property moves a fixed fraction of remaining distance per frame (x += (target-x)*k) so shots enter already in motion; exits accelerate (ease-in) into the cut
- **أرقام / params:** k = 0.12-0.19 per frame at 30 fps
- **الدليل / proof:** `style:pm-notdwd-7de38a`

#### EASE-220 · دخول بتباطؤ أسّي · Exponential ease-out entrances · 👁 شوهد في فيديو
- **ماذا / what:** per frame: pos += (target - pos) * k, k 0.12-0.19; shots start mid-move, never on a still
- **أرقام / params:** k≈0.15
- **الدليل / proof:** `style:pm-notdwd-c2037d`

#### EASE-221 · ضبابية اتجاهية حسب السرعة · Speed-matched directional blur · 👁 شوهد في فيديو
- **ماذا / what:** blur radius = |velocity| * c along the movement axis (SVG feGaussianBlur stdDeviation x/y or canvas filter)
- **أرقام / params:** c ≈ 0.25 px per px/frame, cap 24px
- **الدليل / proof:** `style:pm-notdwd-c2037d`

#### EASE-222 · افتتاحية منحنى التسارع · Easing-curve editor intro · 👁 شوهد في فيديو
- **ماذا / what:** draw cubic-bezier S-curve with handles and endpoints on dark grid; red glowing dot travels along curve in sync with a playhead on a ruler; label shows the bezier values
- **أرقام / params:** ~1.2 s, stroke 2px off-white, dot #e8503c with 12px glow
- **الدليل / proof:** `style:pm-prasenx-8d9323`

#### EASE-223 · قطع فصول على الإيقاع · Beat-locked chapter cuts · 👁 شوهد في فيديو
- **ماذا / what:** ~1.25–2 s per section, hard cut with palette inversion
- **الدليل / proof:** `style:pm-raphaelaubryy-4b137e`

#### EASE-224 · كرة مرتدة مع مخطط التباعد · Bouncing ball with spacing chart · 👁 شوهد في فيديو
- **ماذا / what:** parabolic arcs with ghost trail on timeline ticks
- **الدليل / proof:** `style:pm-rendesr-86be44`

#### EASE-225 · شارة خطوة دوّارة · Rotating step badge · 👁 شوهد في فيديو
- **ماذا / what:** small Lissajous/ellipse in corner rotating continuously; label 'STEP n/10' increments per beat
- **أرقام / params:** rotation 90°/s
- **الدليل / proof:** `style:pm-rneayan-ea6129`

#### EASE-226 · دخول الأداة بميل · Prop tilt-in · 👁 شوهد في فيديو
- **ماذا / what:** bottle rotates from -60deg at corner, holds, exits
- **الدليل / proof:** `style:pm-ror-fly-9950f1`

#### EASE-227 · ساعة تتقدم بسرعة · Time-lapse clock counter · 👁 شوهد في فيديو
- **ماذا / what:** large serif clock digits incremented per frame to show time passing, with job rows completing at matching timestamps
- **أرقام / params:** 52 minutes in ~3 s
- **الدليل / proof:** `style:pm-sachaarbonel-8f14f4`

#### EASE-228 · سقوط مكعبات الثلج · Ice drop and settle · 👁 شوهد في فيديو
- **ماذا / what:** rounded-square cubes fall from above frame into the glass with gravity ease and a tiny settle bounce, staggered
- **أرقام / params:** ~450 ms fall easeInQuad + 120 ms settle, stagger ~300 ms
- **الدليل / proof:** `style:pm-sarut0bisasuke-cefa43`

#### EASE-229 · بطاقات كلمة واحدة متتابعة · One-word punch cards · 👁 شوهد في فيديو
- **ماذا / what:** Split a slogan into single words on black, each cut on the beat with slight scale-in
- **أرقام / params:** ~1.6 s per word, scale 1.05->1
- **الدليل / proof:** `style:pm-spearwtf-3c1fd1`

#### EASE-230 · عرض منحنى التسهيل · Easing curve visualiser · 👁 شوهد في فيديو
- **ماذا / what:** draw bezier with handles, glowing dot follows
- **أرقام / params:** cubic-bezier(.83,0,.17,1)
- **الدليل / proof:** `style:pm-sudiyasa-f48ac9`

#### EASE-231 · عرض منحنى التسهيل كأداة محرر · Easing graph editor demo · 👁 شوهد في فيديو
- **ماذا / what:** draw grid + cubic-bezier curve with handle lines and points; label 'cubic-bezier(x1,y1,x2,y2)'; a dot moves along curve while a ball moves with that easing
- **أرقام / params:** curve stroke 3 px #e25f2f; 1.2 s
- **الدليل / proof:** `style:pm-tequilafunks-97f6c9`

#### EASE-232 · مونتاج سريع على كل ثُمن · Rapid-fire 8th-note montage · 👁 شوهد في فيديو
- **ماذا / what:** At 120 BPM cut every 250 ms between bold single-word type gags: repeated word rows alternating outline/fill scrolling opposite ways, extruded 3D word with stacked offset layers, word split across colo
- **كيف / how:** At 120 BPM cut every 250 ms between bold single-word type gags: repeated word rows alternating outline/fill scrolling opposite ways, extruded 3D word with stacked offset layers, word split across colour bars with glitch
- **أرقام / params:** 6-7 cuts x 250 ms
- **الدليل / proof:** `style:pm-teslachartz-c58b32`

#### EASE-233 · قائمة تنزلق بتتابع مع ضبابية حركة · Stagger slide-in list with motion blur · 👁 شوهد في فيديو
- **ماذا / what:** Rows enter from x=+100% one after another, 80 ms stagger, blur 10px->0 and opacity 0->1, ease-out back
- **أرقام / params:** stagger 80ms; 350ms each
- **الدليل / proof:** `style:pm-thilina-a-891c09`

#### EASE-234 · انفجار قطع سريع · Strobe cut burst · 👁 شوهد في فيديو
- **ماذا / what:** Cut every 250 ms for 2 s at climax
- **أرقام / params:** 8 cuts
- **الدليل / proof:** `style:pm-topi-003-9ca6b5`

#### EASE-235 · عد تنازلي · Countdown intro · 👁 شوهد في فيديو
- **ماذا / what:** numbers 6..1 on beats with silhouettes
- **الدليل / proof:** `style:pm-topi-003-b0e12c`

#### EASE-236 · نابض محسوب كدالة زمن صرفة · Closed-form spring as pure function of time · 👁 شوهد في فيديو
- **ماذا / what:** x(t)=target + sum over retargets of Δ_i * step_response(t - t_i); step_response(τ)=1 - e^(-ζωτ)(cos(ωdτ)+ζω/ωd sin(ωdτ)); deterministic seek(t), no CSS transitions
- **أرقام / params:** ω≈2π·2.2, ζ≈0.75
- **الدليل / proof:** `style:pm-twoclipping-5cba86`

#### EASE-237 · تأرجح شكل · Pendulum shape swing · 👁 شوهد في فيديو
- **ماذا / what:** rotate about pin with damped sine
- **الدليل / proof:** `style:pm-ultimaxbt-2ddf1e`

#### EASE-238 · منحنى النابض · Spring overshoot graph · 👁 شوهد في فيديو
- **ماذا / what:** plot damped spring x(t); dot rides the curve; label peak %
- **أرقام / params:** stiffness 180, damping 12
- **الدليل / proof:** `style:pm-ultimaxbt-bbebf5`

#### EASE-239 · صف عينات منحنيات التسهيل · Easing-curve specimen row · 👁 شوهد في فيديو
- **ماذا / what:** draw six mini graphs (linear, ease-in-out, expo-out, back-out, elastic, bounce) with italic labels; a red dot rides each curve in sync while an object above moves with that ease
- **أرقام / params:** graph 60x40 px, stroke 1.5 px white, 1 s loop
- **الدليل / proof:** `style:pm-vanshwtfff-db0466`

#### EASE-240 · قفزة بضغط وتمدد مع أشباح الحركة · Squash-and-stretch hop with onion skin · 👁 شوهد في فيديو
- **ماذا / what:** shape jumps along a parabola; scaleY 0.6/scaleX 1.4 on landing, stretch 1.3 in air; draw dotted arc trail and semi-transparent ghost copies at past positions; impact rays + ground ripple
- **أرقام / params:** hop 600 ms, 5 ghosts alpha 0.15, rays 8 x 30 px
- **الدليل / proof:** `style:pm-vanshwtfff-db0466`

#### EASE-241 · إيقاع لقطة لكل ميزة · One-beat-per-claim rhythm · 👁 شوهد في فيديو
- **ماذا / what:** Deliver each value proposition as a 1-1.2 s beat: headline + single object, swap on beat
- **أرقام / params:** ~1.15 s per beat for a 14 s film
- **الدليل / proof:** `style:pm-wozu-co-242285`

#### EASE-242 · وضعيات مفتاحية مع حركات مضافة بالكود · Pose keys with procedural overlays · 👁 شوهد في فيديو
- **ماذا / what:** interpolate pose keyframes with Easing.inOut(cubic); add procedural layers: breathing sine, phone thumb scroll, buried leg kicks, 2-step walk cycle
- **أرقام / params:** breath 0.3 Hz amplitude 2 px
- **الدليل / proof:** `style:stickman`

#### EASE-243 · بطاقة تطير لليد وتنقلب ثم تُرمى بأثر · Fly-to-hand, flip, throw with ghost trail · 👁 شوهد في فيديو
- **ماذا / what:** card lerps to hand; scaleX 1->-1 flip swaps to green check face at the midpoint; parabolic throw to box with 2-3 fading ghost copies of previous positions; box squash on impact; counter +1
- **أرقام / params:** flip 250 ms, throw 500 ms, ghost opacity 0.3/0.15
- **الدليل / proof:** `style:stickman`

#### EASE-244 · الرسمة تعيش بعد اكتمالها · Living drawing loops after reveal · 👁 شوهد في فيديو
- **ماذا / what:** once drawn, run continuous real-time loops independent of the slowness factor: sun rotation, rain translateY modulo, vapour rise, dash-offset flow on rivers
- **أرقام / params:** rain 1.2 s period, sun 10 deg/s
- **الدليل / proof:** `style:whiteboard`

#### EASE-245 · توقيتات بخطوات ومعامل بطء واحد · Global step timing with TS factor · 👁 شوهد في فيديو
- **ماذا / what:** all reveal timings in step units multiplied by a single TS constant so the whole piece can be slowed by one number
- **أرقام / params:** TS ~1
- **الدليل / proof:** `style:whiteboard`

#### EASE-246 · السرعة تعني الوزن · Speed as weight table · 📄 موصوف
- **ماذا / what:** Duration tells the viewer how heavy and important a move is.
- **كيف / how:** Fast 0.15-0.3s urgency; medium 0.3-0.5s most content; slow 0.5-0.8s gravity/luxury; very slow 0.8-2.0s cinematic. Never same ease on >2 tweens per scene; never same entrance direction for everything.
- **أرقام / params:** 0.15-0.3 / 0.3-0.5 / 0.5-0.8 / 0.8-2.0 s
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/motion-principles.md`

#### EASE-247 · منحنيات جاهزة بمعايير الاستوديوهات · Agency easing token set · 📄 موصوف
- **ماذا / what:** A reusable set of cubic-bezier tokens for CSS/WAAPI/Remotion.
- **كيف / how:** out-expo (0.16,1,0.3,1); out-quart (0.25,1,0.5,1); out-quint (0.22,1,0.36,1); out-circ (0,0.55,0.45,1); in-expo (0.7,0,0.84,0); in-quart (0.5,0,0.75,0); inOut-quint (0.83,0,0.17,1); inOut-expo (0.87,0,0.13,1); out-back (0.34,1.56,0.64,1); elastic-ish (0.68,-0.6,0.32,1.6); strong UI out (0.23,1,0.32,1); drawer (0.32,0.72,0,1).
- **أرقام / params:** durations 150/300/500/800/1200ms
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md` · `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/motion-and-interaction.md`

#### EASE-248 · سلم المدد · Duration ladder (100/300/500) · 📄 موصوف
- **ماذا / what:** Feedback is fastest, state changes medium, layout changes slower, entrances slowest; exits about 75% of entrances.
- **كيف / how:** 100-150ms feedback, 200-300ms state, 300-500ms layout, 500-800ms entrances; exit = 0.75x enter; ease-in only for exits. Video uses the longer end of each band.
- **أرقام / params:** exit 0.75x
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/motion-and-interaction.md`

#### EASE-249 · سلّم مدد الحركة حسب المسافة · UI duration ladder scaled by distance · 📄 موصوف
- **ماذا / what:** A small fixed set of durations keyed to how big the change is: tiny feedback is near-instant, panels and modals take longer, choreographed sequences longest. Travel distance also scales the time.
- **كيف / how:** Define CSS custom properties (--dur-fast/normal/slow/slower) and pick by category; in GSAP/WAAPI use the same values. Rendered deterministically with kosif-tool render_html.cjs (Playwright Chromium at /opt/pw-browsers + ffmpeg, both present) in virtual-time mode.
- **أرقام / params:** hover/press 100-150ms; toggles/dropdowns 200-300ms; modals/page 300-500ms; choreography 500ms+; 8-16px move 100-150ms, 50-100px 150-250ms, full-screen 250-350ms; most UI ~200ms (<100 imperceptible, >400 sluggish)
- **الدليل / proof:** `kosif-atlas/skills/3529-ui-design/14308-interaction-design` · `kosif-atlas/skills/3438-ux-design/14122-refactoring-ui` · `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/feedback-patterns.md`

#### EASE-250 · مجموعة منحنيات التسارع الاحترافية · Agency custom easing token set · 📄 موصوف
- **ماذا / what:** Named cubic-bezier curves used by award-level studios instead of browser defaults: expo/quart/quint/circ outs for arrivals, expo/quart ins for exits, symmetric quint/expo in-outs for loops, plus back and elastic overshoots.
- **كيف / how:** Paste as :root variables; mirror in GSAP via CustomEase.create('smooth','0.16,1,0.3,1'). Works in CSS/WAAPI with no install; GSAP CustomEase needs gsap package.
- **أرقام / params:** out-expo 0.16,1,0.3,1; out-quart 0.25,1,0.5,1; out-quint 0.22,1,0.36,1; out-circ 0,0.55,0.45,1; in-expo 0.7,0,0.84,0; in-quart 0.5,0,0.75,0; in-out-quint 0.83,0,0.17,1; in-out-expo 0.87,0,0.13,1; out-back 0.34,1.56,0.64,1; out-elastic 0.68,-0.6,0.32,1.6; durations 150/300/500/800/1200ms
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md` · `kosif-atlas/skills/3529-ui-design/14308-interaction-design` · `kosif-atlas/skills/166-demo-video/535-demo-video/references/scene-design-system.md`

#### EASE-251 · قاعدة اتجاه التسارع للدخول والخروج · Enter/exit/state easing direction rule · 📄 موصوف
- **ماذا / what:** Arrivals decelerate, departures accelerate, things that stay but change use symmetric easing; exits are shorter than entrances so the new state appears to win.
- **كيف / how:** ease-out (or power*.out) on entering layers, ease-in on leaving layers, ease-in-out for in-place moves; give exit ~150ms and enter ~210ms with the enter delayed by the exit.
- **أرقام / params:** exit 150ms ease-in, enter 210ms ease-out (delayed 150ms), move 400ms ease-in-out; panels slide in ease-out 200-400ms, out ease-in
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/feedback-patterns.md` · `kosif-atlas/skills/1434-react-skills/3419-vercel-react-view-transitions/references/css-recipes.md` · `kosif-atlas/skills/1567-tonone/4430-form-tokens`

#### EASE-252 · قواعد التتابع بين العناصر · Stagger spacing rules · 📄 موصوف
- **ماذا / what:** Stagger intervals that read as one gesture rather than a queue: very small per character, larger per word and per card; past ~0.2 s per item viewers feel they are waiting.
- **كيف / how:** gsap stagger or CSS animation-delay calc(var(--i)*step); Framer staggerChildren.
- **أرقام / params:** chars 0.02-0.03s; words 0.05s; nav items 0.05s; lines/cards 0.1s; feature cards 0.11s; max ~0.2s; per-element entrance 0.5-0.8s with 0.2-0.4s gaps and 1-2s hold after last
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md` · `kosif-atlas/skills/196-landing/621-landing/references/gsap_animation_patterns.md` · `kosif-atlas/skills/166-demo-video/535-demo-video/references/scene-design-system.md`

#### EASE-253 · حركة واجهات المؤسسات المنضبطة · Restrained enterprise UI motion · 📄 موصوف
- **ماذا / what:** For dashboards/admin/SaaS scenes: short micro-interactions, quick transitions, no bounce.
- **كيف / how:** Use quart-out easing for everything.
- **أرقام / params:** 150ms micro; 200-250ms transitions; cubic-bezier(0.25,1,0.5,1); no spring
- **الدليل / proof:** `kosif-atlas/skills/2963-pwdev-code/12442-skill-frontend-design`

#### EASE-254 · غلاف الإيقاع للمونتير · Editor pacing envelope · 📄 موصوف
- **ماذا / what:** Pacing changes across a long video: tightest in the first 3 minutes, a little looser after the cold open, real-time for demos, tight again in the last 2 minutes.
- **كيف / how:** Cut word-searches out of talking head; hold verdict/insight lines 1-2 s before cutting; allow 5-10% more breathing after the cold open; never stay on B-roll/slides more than 30-45 s without returning to the presenter; B-roll supports, it never patches a weak moment.
- **أرقام / params:** first 3 min tightest; +5-10% breathing; verdict hold 1-2 s; max off-presenter 30-45 s
- **الدليل / proof:** `kosif-atlas/skills/3067-youtube/13224-creator-editor-brief/SKILL.md` · `kosif-atlas/skills/3067-youtube/13229-creator-visual-director/SKILL.md`

#### EASE-255 · البنية الدقيقة للفيديو العمودي · Vertical micro-structure · 📄 موصوف
- **ماذا / what:** Vertical clips follow a compressed arc: 0-1 s hook that works muted and without context, 1-3 s development, then delivery, CTA inside the safe area; for generated/assembled clips: 0-3 s hook, 3-10 s problem/promise, 10-25 s proof, 25 s+ close; under ~30 s retains best on Reels/Shorts.
- **كيف / how:** Lay these as markers in the timeline template; each story card in a sequence must survive alone because viewers enter mid-sequence.
- **أرقام / params:** 0-1/1-3/3+ s; or 0-3/3-10/10-25/25+ s; target <=30 s
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12592-story-reels/SKILL.md` · `kosif-atlas/skills/2976-pwdev-social-media/12594-video-gen/SKILL.md`

#### EASE-256 · قالب الفيديو القصير 60 ثانية · 60-second short template · 📄 موصوف
- **ماذا / what:** 0-3 s pattern-interrupt hook, 3-15 s problem or promise, 15-50 s the value, 50-60 s CTA; one idea per video; hook in the first frame before any title card; captions always on.
- **كيف / how:** Use as the default grid for talking-head reels; map words.json segments into these windows and flag overflow.
- **أرقام / params:** 0-3 / 3-15 / 15-50 / 50-60 s
- **الدليل / proof:** `kosif-atlas/skills/192-marketing-skills/617-video-content-strategist/SKILL.md`

#### EASE-257 · أربع منحنيات حركة مسماة · Four named motion helpers · 📄 موصوف
- **ماذا / what:** Restrict a film to three or four easing roles: slam = easeOutExpo (arrivals and impacts), snap = easeOutBack with overshoot capped near 6% (chips landing), drive = easeInOutQuart (travel, light, drift), settle = easeOutQuart (final resolve); back/elastic overshoot never touches a logo or official br…
- **كيف / how:** Define them once in the composition config and forbid ad-hoc cubic-beziers elsewhere; the same film uses a non-black ground colour so light has somewhere to fall off.
- **أرقام / params:** overshoot <=6%
- **الدليل / proof:** `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`

#### EASE-258 · خريطة الحركة إلى الإحساس في الشرائح · Motion-to-feeling map for slides · 📄 موصوف
- **ماذا / what:** Choose motion by feeling: dramatic = slow fades 1-1.5 s and scale 0.9->1 with parallax; techy = neon glow, text scramble, grid reveals; playful = spring easing and gentle float; corporate = fast subtle 200-300 ms; calm = very slow fades; editorial = staggered text reveals with image-text interplay. …
- **كيف / how:** Default reveal: opacity 0 + translateY(30px) -> 0 over 0.6 s with ease-out-expo cubic-bezier(0.16,1,0.3,1), children staggered 0.1 s; variants scale 0.9, translateX(-50px), blur(10px) over 0.8 s; depth via layered radial gradients and a 50 px grid at 3% white; grain as inline SVG noise; animate only transform/opacity; honour reduced motion.
- **أرقام / params:** 0.6 s; stagger 0.1 s; 30 px; scale 0.9; blur 10 px; grid 50 px @3%
- **الدليل / proof:** `kosif-atlas/skills/345-visuals/1241-html-deck/references/animations.md`

#### EASE-259 · حساب الإطارات والتايم كود بنطاق نصف مفتوح · Half-open frame and timecode arithmetic · 📄 موصوف
- **ماذا / what:** Treat every scene as [start, end); frame = round(seconds x fps). 0-3 s at 30 fps covers frames 0-89 and the cut lands on 90; a 12 s piece ends at frame 360 with 359 the last frame shown. Overlapping transitions are counted once, not added to both scenes. For 29.97/23.976 do not invent drop-frame tim…
- **كيف / how:** Python helper while planning; after render check ffprobe nb_frames == round(duration x fps) (kosif-tool verify_video.py / TEST_REPORT).
- **أرقام / params:** frame=round(s*fps); 0-3 s@30 -> 0-89; 12 s@30 -> 360 frames (0-359)
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/workflow.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/examples.md`

#### EASE-260 · S12 رياضي سريع · S12 Sports energy · 📄 موصوف
- **ماذا / what:** High contrast, directional lines, big numbers; cuts on the beat, limited thrusts, freeze frames. High energy and readable motion; needs fitting footage and licensed music; avoid fast flashing.
- **كيف / how:** Beat markers from the audio file, ffmpeg freeze (tpad/loop) + overlays, speed lines in SVG; KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg)
- **أرقام / params:** cost medium-high; MG-003 MG-091..MG-095 MG-097..MG-100
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### EASE-261 · MG-097 عد تنازلي قبل الانطلاق · MG-097 3-2-1 countdown · 📄 موصوف
- **ماذا / what:** Numbers 3, 2, 1 appear steadily and the frame opens on 'go'.
- **كيف / how:** 0-1 / 1-2 / 2-3 s numbers with hold keys, 3-4 s expanding mask; tie it to a real moment or state it is a visual opener. Regular ticks and a start hit.
- **أرقام / params:** 4 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-music-sports.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### EASE-262 · MG-118/119/120 تمايل بفروق طور وبندول وإطار متحرك · MG-118/119/120 Phase-offset sway, pendulum and border tracer · 📄 موصوف
- **ماذا / what:** Edge branches sway around a title with different delays (MG-118); a product tilts like a pendulum with a coupled shadow (MG-119); a short segment travels around a rectangle border (MG-120).
- **كيف / how:** MG-118: 0-4 tilt, 4-8 return; pivots at branch bases, never all in phase. MG-119: 0-1.5 / 1.5-4.5 / 4.5-6 s sinusoidal limited rotation, shadow scale tied to tilt; 2D sway cannot show unseen sides. MG-120: one 6 s lap, trim-path offset with constant arc length, inside safe area, text static.
- **أرقام / params:** 8 s / 6 s / 6 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-loops-backgrounds.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### EASE-263 · جدول الإشارات الزمنية للمونتاج · Edit cue sheet (run-of-show style) · 📄 موصوف
- **ماذا / what:** A timed table with one row per segment: clock time, duration, segment, explicit cues (graphic in/out, SFX, music dip, caption style) and an owner; durations must add up exactly to the total, buffers are planned, and no cue is left implicit; keep contingencies beside it.
- **كيف / how:** Generate CSV/HTML from the timeline JSON; Python assert sum(durations) == total.
- **الدليل / proof:** `kosif-atlas/skills/2290-event-management/8759-build-run-of-show/SKILL.md`

#### EASE-264 · مواصفة الحركة فقط حين تكون الحركة هوية · Motion spec only when motion is the brand · 📄 موصوف
- **ماذا / what:** Write a dedicated motion spec (easing curves, duration scale, triggers, purpose: feedback, continuity, expression) only for expressive brands or projects already using framer-motion, GSAP or Lottie; utility work just honours prefers-reduced-motion. Mood clusters for naming a direction: premium (Arch…
- **كيف / how:** Store duration/easing tokens in the kosif-tool style STYLE.json.
- **الدليل / proof:** `kosif-atlas/skills/1530-webcraft/4189-design-guide-authoring/SKILL.md`

#### EASE-265 · قواعد الوقفات في قص المتكلم · Speech pause grammar for talking-head cuts · 📄 موصوف
- **ماذا / what:** Treat word gaps >0.7 s as cut candidates, keep ~0.4 s breath at sentence ends, keep 0.8-2 s of deliberate silence after a turning point, decision, failure or realisation, never cut a filler when neighbouring word gap <0.15 s (the splice becomes audible), keep only the last take of a retake group.
- **كيف / how:** From word-timestamp transcript (whisper word_timestamps) build a segment list, then re-assemble with startFrame/endFrame (Resolve AppendToTimeline) or ffmpeg trim+concat; V1 picture trimmed by the same length as A1 speech.
- **أرقام / params:** gap>0.7 cut; breath 0.4; keep pause 0.8-2.0; min splice gap 0.15
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2453-davinciresolve-cut-devtalk/SKILL.md`

#### EASE-266 · قاعدة توقيت الترجمة · Caption timing rule · 📄 موصوف
- **ماذا / what:** On-screen time = max(chars × 0.15 s, 2 s), capped at 6 s; start 0.5 s after a cut and end 0.3 s before the next; shots under 2.8 s either share the caption with the next same-place shot or get none; 8-frame fade in/out.
- **كيف / how:** Compute from cut list; place via ASS events or Text+/HTML
- **أرقام / params:** 0.15 s/char; 2-6 s; +0.5/-0.3 s; 8 f fade
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2465-davinciresolve-subtitle-travelnote/SKILL.md`

#### EASE-267 · إيقاع المونتاج حسب النوع · Edit rhythm presets by genre · 📄 موصوف
- **ماذا / what:** Measured rhythm targets: explainer/essay ASL 3.3 s (2.5-4), 20 cuts in first 60 s (15-25), same picture ≤8 s, cards 30-50%; build/project vlog ASL 8 s (5-12), 3 cuts first minute, same screen ≤40 s, dissolve 12 f only around timelapses; reflection ASL 3.8 s (3-5), 20 cuts, same picture ≤6 s, voice 6…
- **كيف / how:** Compute ASL and first-minute cut count from the cut list; adjust by swapping b-roll at noun/action sentence boundaries, never delete meaningful pauses to hit numbers
- **أرقام / params:** ASL 3.3 / 8 / 3.8 s
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2461-davinciresolve-style-essay/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2462-davinciresolve-style-project/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2463-davinciresolve-style-reflection/SKILL.md`

#### EASE-268 · تسريع وتبطيء متدرج · Speed ramp and slow motion · 📄 موصوف
- **ماذا / what:** Change clip speed (constant, or ramped by splitting into segments with different setpts), optionally synthesising in-between frames for smooth slow motion.
- **كيف / how:** video setpts=PTS/F (F>1 faster); audio atempo=F (0.5-2 per instance, chain for more) or rubberband=tempo=F (pitch-preserving, present locally); smooth slow-mo: minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:vsbmc=1; ramp = trim pieces at 1.0 -> 0.5 -> 1.0 and concat (or Remotion playbackRate per Sequence)
- **أرقام / params:** atempo 0.5-2.0
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md` · `kosif-atlas/skills/1526-gamegen/4173-game-trailer/SKILL.md`

#### EASE-269 · حركة نابضية · Spring motion defaults · 📄 موصوف
- **ماذا / what:** Primary motion uses springs with slight overshoot, settling in 400-700ms.
- **كيف / how:** Framer Motion spring stiffness 300 damping 30 mass 1; GSAP elastic.out(1,0.5) ~0.6s; CSS cubic-bezier(0.34,1.56,0.64,1).
- **أرقام / params:** overshoot 1.05x
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### EASE-270 · مزامنة المؤثر مع لحظة الاصطدام · Sync VFX to contact frame · 📄 موصوف
- **ماذا / what:** Align bursts to the real impact/apex frame, not clip start; test on varied backgrounds and honor flash limits.
- **كيف / how:** Use event markers/word timestamps.
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4164-game-audio-vfx/SKILL.md`

#### EASE-271 · زمن القراءة من النص · Reading-time from real text · 📄 موصوف
- **ماذا / what:** Hold each text long enough to read, computed from the actual words.
- **كيف / how:** hold ≥ max(1.2s, words/3 s) approx (≈180 wpm); verify on target size.
- **أرقام / params:** ~3 words/s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-typography/SKILL.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/quality-and-editors.md`

#### EASE-272 · التحريك على الاثنين والثلاثة · Hold mix on 1s/2s/3s · 📄 موصوف
- **ماذا / what:** Drawn animation alternates holds of 1, 2 or 3 frames per drawing; the mix is a measurable fingerprint of a style.
- **كيف / how:** When animating hand-drawn layers, step time with Math.floor(frame/2)*2 for twos; keep camera moves on ones for smoothness.
- **أرقام / params:** on twos at 24fps = 12 drawings/s
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9355-learn-style` · `kosif-atlas/skills/2414-animation/9357-rotoscope`

#### EASE-273 · حركة نابضية · Spring physics motion · 📄 موصوف
- **ماذا / what:** Springs with slight overshoot feel alive.
- **كيف / how:** Framer Motion stiffness 300 damping 30 mass 1; GSAP elastic.out(1,0.5); CSS fallback cubic-bezier(0.34,1.56,0.64,1); Remotion spring().
- **أرقام / params:** overshoot 1.05; settle 400-700ms
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`

#### EASE-274 · سمِّ فعل الحركة · Name the animation verb · 📄 موصوف
- **ماذا / what:** Every chart motion must be one named verb (reveal, flow, accumulate, compare, transition, pulse, highlight, decay, orbit, slice, scrub) tied to data or story state.
- **كيف / how:** Write the verb per scene before coding; first frame already readable; animate between meaningful states only; one scene clock; final frame or key frames must still prove the claim without motion (also serves as thumbnail and reduced-motion fallback).
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/webgl-2d-animation-patterns.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10335-visualization-strategy-and-critique/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/SKILL.md`

#### EASE-275 · إبقاء عناصر الأرقام حية · Keep every stat element alive · 📄 موصوف
- **ماذا / what:** No element sits frozen mid-scene: stats count, images drift, persistent items float subtly.
- **كيف / how:** Stat/number: counter from 0; screenshot: slow zoom 1->1.03 or pan; logos: shimmer sweep or gentle scale pulse; any persistent element: float y +/-4-6 px sine in-out yoyo; with music, bass pulses a logo 3-4%.
- **أرقام / params:** zoom 1.00->1.03; float +/-4-6 px; bass pulse 3-4%
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/step-6-build.md`

#### EASE-276 · أرقام حرفة الحركة · Motion craft numbers for coded scenes · 📄 موصوف
- **ماذا / what:** Measured craft rules baked into the code contract Claude follows.
- **كيف / how:** Something moves within 0.1 s; arrivals U.E.out 0.3-0.9 s; exits U.E.exit 0.17-0.4 s; zero overshoot default (max two true landings); travel time 0.35 s + 1.35 ms/px; secondary starts at 55-75% of leader; stagger 0.06-0.12 s; read text <= 3 px/frame; 3-4 words/card ~0.4 s/word, >= 0.5 s/card; words arrive from 40% opacity with small rise; holds creep ~4% scale/s; one accent colour ~5% of pixels; banned: crossfades, glow on type, glassmorphism, multi-hue gradients, purpose-less particles, floaty d…
- **الدليل / proof:** `app/public/js/00_editor.js:1568`

#### EASE-277 · قواعد إيقاع الفيلم · Film pacing rules · 📄 موصوف
- **ماذا / what:** Pacing targets for storyboarded films.
- **كيف / how:** genFilm prompt: first word readable by 0.4 s, premise by 2 s; picture change ~every 0.7 s; median shot ~1.5 s (1.1-2.8); one designed 1.0-1.6 s hold; lull near 65%; last energy peak near 82%; end card ~9% (assemble 1 s, hold 0.8 s); 3-4 words per card; scene lengths in whole beats when BPM known.
- **الدليل / proof:** `app/public/js/00_editor.js:2024`

#### EASE-278 · معايير الإيقاع · Pacing medians · 📄 موصوف
- **ماذا / what:** Measured medians of top motion films used as defaults.
- **كيف / how:** Apply as defaults while authoring; verify with kmotion measure/speed/sheet
- **أرقام / params:** median shot 1.46 s (1.1–2.8); change every ~0.7 s; first change 0.10 s; first word 0.4 s; premise by 2 s; one hold 1.0–1.6 s; last peak at 82%; lull at ~65%; end card 2.2 s (assemble 1.0–1.3, hold 0.6–1.3)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`

#### EASE-279 · تداخل الحركات · Overlap of secondary moves · 📄 موصوف
- **ماذا / what:** Secondary move starts at 55–75% of the lead so both settle within 2 f.
- **كيف / how:** Apply as defaults while authoring; verify with kmotion measure/speed/sheet
- **أرقام / params:** 55–75%
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`

#### EASE-280 · تنويع أطوال اللقطات · Shot length variety · 📄 موصوف
- **ماذا / what:** Alternate fast shots with breathing shots to avoid rhythmic monotony.
- **أرقام / params:** fast 0.5-1.5 s; breathing 2.5-4.0 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/montage_grammar.md`

#### EASE-281 · قواعد اتجاه التسارع · Easing direction rules · 📄 موصوف
- **ماذا / what:** Never linear on spatial moves; entrances ease-out, exits ease-in, on-screen ease-in-out, ambient sine; exit ~65-75% of entrance.
- **أرقام / params:** exit 65-75%
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### EASE-282 · جدول المدد · Duration table by element · 📄 موصوف
- **ماذا / what:** LottieFiles timing by element size; scale with distance.
- **أرقام / params:** micro 80-120 ms; button 120-180; icon 150-250; card 200-350; modal 300-400; page 400-600; reveal 600-1200; ambient 2-20 s; full screen 1.8-2x
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### EASE-283 · ميزانية التجاوز · Overshoot budget · 📄 موصوف
- **ماذا / what:** How much overshoot per intent.
- **أرقام / params:** premium 0%; feedback 2-5%; success 5-10%; celebration 15-25%
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### EASE-284 · ميزانية التتابع · Stagger budget · 📄 موصوف
- **ماذا / what:** Stagger totals under 500 ms, same easing family.
- **أرقام / params:** micro 20-40 ms; standard 50-100; dramatic 100-200; total <500 ms
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### EASE-285 · قواعد الثلث · 1/3 rules · 📄 موصوف
- **ماذا / what:** No travel >1/3 frame without intermediate key; at most 1/3 of elements move at once; new event every 2-4 s; no hold >1.5 beats.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### EASE-286 · الفصول الأربعة للحركة · Four-act motion · 📄 موصوف
- **ماذا / what:** Anticipation, action, reaction, resolution proportions.
- **أرقام / params:** 10-20% / 30-50% / 10-20% / 20-30% + 100-200 ms breathing
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### EASE-287 · قاعدة القص على الإيقاع · Beat-cut timing rule (60/BPM) · 📄 موصوف
- **ماذا / what:** Place major visual changes on downbeats, small accents on off-beats, and alternate fast and breathing shot lengths.
- **كيف / how:** beat = 60/BPM s; scene change/B-roll/impact on downbeat; punch-zoom, quick camera, caption keyword on off-beat; mix 0.5-1.5 s shots with 2.5-4.0 s shots.
- **أرقام / params:** 120 BPM = 0.500 s; 100 BPM = 0.600 s; 85 BPM = 0.705 s
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/montage_grammar.md` · `kosif-one/tools/kosif-omni/skills/kosif-video/SKILL.md`

#### EASE-288 · أنماط التمهيد الحركي الأربعة · Easing profile taxonomy (Snap/Drive/Heavy Spring/Elastic) · 📄 موصوف
- **ماذا / what:** Four named motion characters for choosing easing by meaning.
- **كيف / how:** Snap = fast in, soft settle (text, key cards); Drive = gradual acceleration then strong launch (vehicles, big transforms); Heavy Spring = slow massive oscillation (luxury, weight); Elastic/Playful = bouncy overshoot (stickers, icons). kinetic_2d ships a spring() helper (exp(-10t) * sin) but the template actually uses cubic ease-out.
- **أرقام / params:** spring helper: a*2^(-10t)*sin((t*d)*2PI/(0.4d)) + c
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/animation_craft.md` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/kinetic_2d.html:137`

#### EASE-289 · معايير الإيقاع من أفلام الإطلاق · Pacing norms from top launch films · 📄 موصوف
- **ماذا / what:** Measured medians to aim for: shot length, picture-change rate, first change, first readable word, holds, energy peak, end card.
- **كيف / how:** Use as defaults when planning beats; check with motion.py measure/study.
- **أرقام / params:** median shot 1.46 s (1.1-2.8); change every ~0.7 s; first change 0.10 s; first word 0.4 s, premise by ~2 s; one hold 1.0-1.6 s; last energy peak at 82%, lull 1-4 s at ~65%, calm outro 8-20%; end card 2.2 s (assemble 1.0-1.3, hold 0.6-1.3)
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/references/craft-numbers.md`

#### EASE-290 · حدود السرعة وقواعد الوزن · Speed limits and weight rules · 📄 موصوف
- **ماذا / what:** Motion budget: overlap secondary moves, settle shape before position, limit speeds, rarely overshoot.
- **كيف / how:** Apply while choreographing; verify with motion.py speed.
- **أرقام / params:** zero overshoot norm (or 1-4%); secondary starts at 55-75% of lead; shape settles 6 f before position; text <= 3 px/f; > 12-20 px/f needs blur; nothing > 80 px/f
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/references/craft-numbers.md`

#### EASE-291 · مدد العناصر وحدود الارتداد · Element duration and overshoot budgets · 📄 موصوف
- **ماذا / what:** Durations by element type, stagger totals and overshoot budgets by context.
- **كيف / how:** Apply when timing UI and explainer elements.
- **أرقام / params:** micro 80-120 ms, button 120-180, icon 150-250, card 200-350, modal 300-400, page 400-600, dramatic 600-1200, ambient 2-20 s; distance scaling up to 1.8-2x full screen; overshoot premium 0%, feedback 2-5%, success 5-10%, celebration 15-25%; stagger totals < 500 ms (micro 20-40, standard 50-100, drama…
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/references/motion-craft.md`

#### EASE-292 · حركة بطيئة باستيفاء · Optical-flow slow motion · 📄 موصوف
- **ماذا / what:** Smooth 0.5x slowmo by synthesising frames.
- **كيف / how:** minterpolate=fps=60:mi_mode=mci,setpts=2.0*PTS
- **أرقام / params:** 60 fps, mci
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### EASE-293 · طبقات السرعة حسب الإحساس · Speed tiers by mood · 📄 موصوف
- **ماذا / what:** Duration communicates energy; slowest move should be ~3x fastest.
- **كيف / how:** Pick per element: fast energy, medium pro, slow luxury, very slow cinematic.
- **أرقام / params:** 0.15-0.3 / 0.3-0.5 / 0.5-0.8 / 0.8-2 s; ratio 3x
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/references/motion-rules.md`

#### EASE-294 · اتجاه التمهيد معنى · Ease direction = meaning · 📄 موصوف
- **ماذا / what:** .out for entrances, .in for exits, .inOut between positions; entrance longer than exit; max two tweens sharing one ease.
- **كيف / how:** Card enters 0.4 s, exits 0.25 s.
- **أرقام / params:** 0.4 in / 0.25 out
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/references/motion-rules.md`

#### EASE-295 · أربعة تمهيدات · Four-ease vocabulary slam/snap/drive/settle · 📄 موصوف
- **ماذا / what:** Only four eases: slam easeOutExpo for impacts, snap easeOutBack <=6% overshoot for landing, drive easeInOutQuart travel/light, settle easeOutQuart resolution; no elastic/back on official logo.
- **أرقام / params:** overshoot <=6%
- **الدليل / proof:** `100-superskills/skills/motion-director-pro/SKILL.md`

#### EASE-296 · أرقام الإيقاع · Pacing numbers of top motion films · 📄 موصوف
- **ماذا / what:** Median measurements at 60 fps from shipped films (via the MIT cinetic skill and others).
- **كيف / how:** Plan shot lengths and holds; verify with motion.py measure / study.
- **أرقام / params:** median shot 1.46 s (1.1-2.8); picture change every ~.7 s (dense .33); first visible change .10 s; first readable word .4 s, premise by 2 s; one designed hold 1.0-1.6 s; last energy peak at 82%, lull 1-4 s at ~65%, outro 8-20%; end card 2.2 s (assemble 1.0-1.3, hold .6-1.3); frame diff median 1.4 p90…
- **الدليل / proof:** `kosif-studio/motion/references/craft-numbers.md`

#### EASE-297 · قواعد سرعة الحركة · Motion speed and curve-role rules · 📄 موصوف
- **ماذا / what:** One curve family per role, near-zero overshoot, speed limits that decide when to blur or redesign.
- **كيف / how:** Use E.out arrivals, E.exit into cuts, E.inOut/E.whip/E.cam repositioning; check px/f with motion.py speed.
- **أرقام / params:** arrivals settle 18-55 f; exits 10-24 f; >half of top films 0% overshoot, rest 1-4%; ≤2 snap/pop/land springs per film; slowest move ≥ 3× fastest; secondary starts at 55-75% of lead; text being read ≤ 3 px/f; > 12-20 px/f needs blur; > 80 px/f redesign; shape settles 6 f before position; squash 8%/10…
- **الدليل / proof:** `kosif-studio/motion/references/craft-numbers.md`

#### EASE-298 · جدول مدد العناصر · Element duration table · 📄 موصوف
- **ماذا / what:** Durations by element type, overshoot budget and stagger totals (LottieFiles motion-design, MIT).
- **كيف / how:** Pick durations from the table; scale by distance.
- **أرقام / params:** micro 80-120 ms, button 120-180, icon 150-250, card 200-350, modal 300-400, page 400-600, dramatic reveal 600-1200, ambient 2-20 s; full screen 1.8-2× of 100 px; overshoot premium 0%, feedback 2-5%, success 5-10%, celebration 15-25%; stagger total < 500 ms (micro 20-40, standard 50-100, dramatic 100…
- **الدليل / proof:** `kosif-studio/motion/references/motion-craft.md`

#### EASE-299 · أرقام الحرفة · Craft-number norms · 📄 موصوف
- **ماذا / what:** Measured launch-film norms used by QA: motion energy median ≈1.4 and p90 ≈6.0, something new every 2-4 s, ≤2 uses of any transition, idea felt by 1 s, ≤12 px/frame without blur.
- **كيف / how:** qa.study / measure / speed
- **الدليل / proof:** `kosif-studio/motion/qa.py:11` · `kosif-studio/motion/qa.py:407`

#### EASE-300 · منحنى دخول · Easing token: Entrance · 📄 موصوف
- **ماذا / what:** Documented default curve and duration range for entrance motions.
- **كيف / how:** use as CSS transition/WAAPI easing or GSAP CustomEase
- **أرقام / params:** cubic-bezier(0.22, 1, 0.36, 1); 250-600 ms
- **الدليل / proof:** `kosif-tool/templates/STYLE.md`

#### EASE-301 · منحنى خروج · Easing token: Exit · 📄 موصوف
- **ماذا / what:** Documented default curve and duration range for exit motions.
- **كيف / how:** use as CSS transition/WAAPI easing or GSAP CustomEase
- **أرقام / params:** cubic-bezier(0.55, 0, 1, 0.45); 200-400 ms
- **الدليل / proof:** `kosif-tool/templates/STYLE.md`

#### EASE-302 · منحنى تأكيد بارتداد · Easing token: Accent overshoot · 📄 موصوف
- **ماذا / what:** Documented default curve and duration range for accent overshoot motions.
- **كيف / how:** use as CSS transition/WAAPI easing or GSAP CustomEase
- **أرقام / params:** cubic-bezier(0.34, 1.56, 0.64, 1); 120-300 ms
- **الدليل / proof:** `kosif-tool/templates/STYLE.md`

#### EASE-303 · منحنى انتقال · Easing token: Transition · 📄 موصوف
- **ماذا / what:** Documented default curve and duration range for transition motions.
- **كيف / how:** use as CSS transition/WAAPI easing or GSAP CustomEase
- **أرقام / params:** cubic-bezier(0.65, 0, 0.35, 1); 300-800 ms
- **الدليل / proof:** `kosif-tool/templates/STYLE.md`

#### EASE-304 · منحنى رسم مسار · Easing token: Path draw · 📄 موصوف
- **ماذا / what:** Documented default curve and duration range for path draw motions.
- **كيف / how:** use as CSS transition/WAAPI easing or GSAP CustomEase
- **أرقام / params:** linear -> ease-out, sequential; 400-1200 ms
- **الدليل / proof:** `kosif-tool/templates/STYLE.md`

#### EASE-305 · سقوط واستقرار بنابض · Drop + spring settle entrance (3D) · 📄 موصوف
- **ماذا / what:** Objects land with an ease-in drop then a spring settle, or rise from below the floor.
- **كيف / how:** Position y from ease-in quad then damped spring.
- **أرقام / params:** drop 0.4 s ease-in; spring damping 12
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:26`

#### EASE-306 · توقيت ضربة الميزة · Feature beat timing · 📄 موصوف
- **ماذا / what:** Feature beats enter fast, hold until read, exit quicker, cut on music.
- **أرقام / params:** enter 300–450 ms ease-out quint; exit 200 ms
- **الدليل / proof:** `kosif-tool/playbooks/ads.md:26`

#### EASE-307 · هبوط بطاقة السعر · Price card landing · 📄 موصوف
- **ماذا / what:** Price counts up only if it is a saving; otherwise lands with a spring; max 2 lines, CTA verb first.
- **كيف / how:** spring config.
- **أرقام / params:** spring damping 14 stiffness 180; CTA readable ≥ 2 s
- **الدليل / proof:** `kosif-tool/playbooks/ads.md:19` · `kosif-tool/playbooks/ads.md:28`

#### EASE-308 · الاستباق والمتابعة · Anticipation and follow-through · 📄 موصوف
- **ماذا / what:** Counter-move before action; secondary parts lag and overshoot.
- **أرقام / params:** anticipation 4–8 frames; follow-through lag 2–4 frames, overshoot 5–10%
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:25`

#### EASE-309 · ظهور الحبوب والتسميات · Pills/labels pop and exits · 📄 موصوف
- **ماذا / what:** Label pills spring in; exits short ease-in.
- **أرقام / params:** spring {damping 14, stiffness 120, mass 1}; exit 200–300 ms ease-in cubic
- **الدليل / proof:** `kosif-tool/playbooks/charts.md:43`

#### EASE-310 · ظهور العقدة · Node pop · 📄 موصوف
- **ماذا / what:** Scale spring pop with quick fade.
- **أرقام / params:** scale 0.85→1 spring {damping 14, stiffness 160} ~300 ms; opacity 150 ms
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:27`

#### EASE-311 · منحنى دخول الكلمة · Word entrance curve · 📄 موصوف
- **ماذا / what:** Rise and fade in per word.
- **أرقام / params:** 300–450 ms; translateY 40–70 px; cubic-bezier(0.22,1,0.36,1); opacity in first 60%
- **الدليل / proof:** `kosif-tool/playbooks/kinetic-type.md:26`

#### EASE-312 · تدرج الكلمات · Word stagger · 📄 موصوف
- **ماذا / what:** Fixed stagger without audio, word start − 60 ms with audio.
- **أرقام / params:** 70–120 ms; −60 ms anticipation
- **الدليل / proof:** `kosif-tool/playbooks/kinetic-type.md:27`

#### EASE-313 · نبضة التأكيد · Emphasis pop · 📄 موصوف
- **ماذا / what:** Scale pop or weight crossfade on emphasis word, landing on stressed syllable.
- **أرقام / params:** 1→1.12→1 over 280 ms spring {damping 12, stiffness 180}; or 500→900 weight with 150 ms crossfade
- **الدليل / proof:** `kosif-tool/playbooks/kinetic-type.md:28` · `kosif-tool/playbooks/kinetic-type.md:85`

#### EASE-314 · الخروج أقصر من الدخول · Exit shorter than entrance · 📄 موصوف
- **ماذا / what:** Exits are quicker and move opposite to entrance.
- **أرقام / params:** 200–300 ms ease-in cubic; 30 px
- **الدليل / proof:** `kosif-tool/playbooks/kinetic-type.md:30`

#### EASE-315 · معادلة مدة القراءة · Reading hold formula · 📄 موصوف
- **ماذا / what:** Minimum readable hold after last word lands.
- **أرقام / params:** hold ≥ 0.3 s + 0.06 s × characters
- **الدليل / proof:** `kosif-tool/playbooks/kinetic-type.md:31`

#### EASE-316 · استباق الحركة السريعة · Pre-move anticipation · 📄 موصوف
- **ماذا / what:** Move opposite to travel before fast move.
- **أرقام / params:** 8–12% for 120–180 ms
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:26`

#### EASE-317 · حركة سريعة على قوس · Fast arc travel · 📄 موصوف
- **ماذا / what:** Fast moves on arcs.
- **أرقام / params:** 250–400 ms ease-in-out quint
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:27`

#### EASE-318 · دخول وخروج وتدرج الصور · Photo entrance/exit/stagger/holds · 📄 موصوف
- **ماذا / what:** Standard photo timings.
- **أرقام / params:** in 400 ms opacity + scale 1.04→1 cubic-bezier(0.22,1,0.36,1); out 250–300 ms cubic-bezier(0.55,0,1,0.45); next starts 2 frames early; stagger 80–120 ms (60 for ≥6); ≤ 6 photos; holds 2.5–5 s narration, 1.2–2 s montage, ≥ 8 frames
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:40`

#### EASE-319 · جدول توقيتات تفاعل الواجهة · UI interaction timing table · 📄 موصوف
- **ماذا / what:** Reference durations and curves for 17 UI events.
- **أرقام / params:** cursor 380–700 ms/200–900 px cubic-bezier(0.2,0.8,0.2,1) arc 2–4% settle 80–120; hover 120–160; press 80 down/140 up spring k300 d20, button 0.96 cursor 0.88; ripple 320–400 0→48 px; modal backdrop 200 panel 280–320 spring k170 d18 scale 0.96 y12; close 160–200; dropdown 180–220 expo-out; toggle 180…
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:31-50`

#### EASE-320 · وقفة القراءة وتسلسل السرعة ونابض واحد · Dwell, speed hierarchy, one overshoot · 📄 موصوف
- **ماذا / what:** Reading dwell after states; chrome slowest, pointer fastest; one bouncy spring per scene; floors/ceilings.
- **أرقام / params:** dwell 1.2–2.0 s (reels 0.8 s); overshoot only damping < 16 once; nothing < 80 ms; nothing frozen > 1.2 s
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:54-58`

#### EASE-321 · معدلات إطارات متدرجة · Tiered stepped frame rates · 💡 فكرة
- **ماذا / what:** Different sprite loops run at fixed low fps with no tweening.
- **كيف / how:** Remotion: sprite index = floor(frame*fps_target/30) % n.
- **أرقام / params:** idle 4 fps, walk 8 fps (4-frame cycle), spell 12 fps
- **الدليل / proof:** `style:pm-0xevinho-3777d8`

#### EASE-322 · حركة حاسمة بلا ارتداد · Decisive no-overshoot easing · 💡 فكرة
- **ماذا / what:** Short moves with expo-like out curve and no bounce.
- **كيف / how:** CSS/Remotion bezier.
- **أرقام / params:** 300-450 ms cubic-bezier(0.22,1,0.36,1)
- **الدليل / proof:** `style:pm-ajith-io-ea7f2d`

#### EASE-323 · دخول بنوابض · Spring entrances 170-200 · 💡 فكرة
- **ماذا / what:** Every primary entrance uses a spring rather than tween.
- **كيف / how:** Remotion spring().
- **أرقام / params:** stiffness 170-200, damping 12-16, mass 1
- **الدليل / proof:** `style:pm-aschapmann-131210`

#### EASE-324 · سقوط الأيقونة بارتداد · Icon bounce drop · 💡 فكرة
- **ماذا / what:** App icon drops with back-out bounce; other entrances smooth.
- **كيف / how:** cubic-bezier.
- **أرقام / params:** icon cubic-bezier(0.34,1.56,0.64,1) 600 ms; others (0.2,0.8,0.2,1) 500 ms
- **الدليل / proof:** `style:pm-cansincengiz-me-cf68dd`

#### EASE-325 · حزمة دخول وخروج · Entrance/stagger/exit kit · 💡 فكرة
- **ماذا / what:** Expo-out entrances, short list stagger, fade+drift exits; single push across piece.
- **كيف / how:** CSS.
- **أرقام / params:** enter (0.16,1,0.3,1) 700 ms; stagger 50 ms; exit 300 ms +20 px; push 1.0→1.06/15 s
- **الدليل / proof:** `style:pm-danilowm-d3720d`

#### EASE-326 · حركة إيقاف على اثنين وثلاثة · Stop-motion on twos/threes · 💡 فكرة
- **ماذا / what:** Puppets update only on held frames with linear steps.
- **كيف / how:** Math.floor(frame/2) or /3 at 24 fps.
- **أرقام / params:** 24 fps; holds 2/3
- **الدليل / proof:** `style:pm-davidshulmanfl-371638`

#### EASE-327 · حركات كبيرة بطيئة · Slow-large-move rule · 💡 فكرة
- **ماذا / what:** Large moves never faster than 900 ms, one easing.
- **كيف / how:** cubic-bezier(0.16,1,0.3,1).
- **أرقام / params:** 900-1400 ms
- **الدليل / proof:** `style:pm-gautam-mer1-2ae354`

#### EASE-328 · نابض الواجهة · UI spring settle · 💡 فكرة
- **ماذا / what:** Panels spring in, bounce at most once.
- **كيف / how:** spring stiffness 170 damping 22 mass 1.
- **أرقام / params:** settle ≤700 ms
- **الدليل / proof:** `style:pm-melvynx-6cde6c`

#### EASE-329 · نبض جيبي · Sinusoidal pulse 2 Hz · 💡 فكرة
- **ماذا / what:** Scale pulse sine with safe frequency.
- **كيف / how:** scale=1+0.06*sin(2π·2t).
- **أرقام / params:** 2 Hz; 6% amp; nothing >3 Hz
- **الدليل / proof:** `style:pm-monokern-ade5b6`

#### EASE-330 · شبكة 120 وخروج أسرع · 120 BPM grid, fast exits · 💡 فكرة
- **ماذا / what:** Entries overshoot slowly, exits snap faster.
- **كيف / how:** Quantize events to 250/500 ms.
- **أرقام / params:** in cubic-bezier(0.22,1,0.36,1) 450 ms; out cubic-bezier(0.64,0,0.78,0) 220 ms
- **الدليل / proof:** `style:pm-mrtanviir-132457`

#### EASE-331 · نابض أساسي · Spring 180/18 primary · 💡 فكرة
- **ماذا / what:** stiffness 180 damping 18 mass 1; UI cubic-bezier(0.2,0.8,0.2,1) 450 ms
- **أرقام / params:** max hold 900 ms
- **الدليل / proof:** `style:pm-stephanlivera-df17a2`

#### EASE-332 · رسم منحنى التسهيل · On-screen easing curve demo · 💡 فكرة
- **ماذا / what:** Draw the easing graph while applying it.
- **أرقام / params:** exits 40% shorter; spring 180/14 overshoot cap 12%; label >=600 ms
- **الدليل / proof:** `style:pm-tolgayhickiran-e90799`
