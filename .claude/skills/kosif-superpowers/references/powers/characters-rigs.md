# الشخصيات والتحريك الهيكلي — Characters & rigs

> فصل مُجمَّع آليًا من 137 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **134 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 134 powers deduplicated by name from 137 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 10 · 🟢 جاهز 21 · 📦 بأمر تثبيت 31 · 🔑 مفتاح/خدمة 9 · 👁 شوهد في فيديو 35 · 📄 موصوف 23 · 💡 فكرة 5

#### CHAR-01 · مولد دورة المشي الإجرائي · Procedural walk cycle generator · ✅ مُثبت هنا
- **ماذا / what:** One draw(direction,pose) function parameterised by limb angles, step phase, body bob, arm swing and squash keeps every frame on-model.
- **كيف / how:** Python/Pillow or canvas JS; proportion presets chibi/standard/tall; mirror side view only if symmetric, shade after mirroring with light from top-left.
- **أرقام / params:** walk 4-8 frames; bob 1px; RPG Maker MZ walk 3 patterns 0-1-2-1
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9525-animate`

#### CHAR-02 · بايبل شخصية الرجل العصوي · Stickman Character Bible · ✅ مُثبت هنا
- **ماذا / what:** Fixed spec for an original 2D stick character pasted into every image prompt.
- **كيف / how:** BIBLE constant: charcoal-black 5 px brush strokes at 1080 px width, circular head = 1/4 of height, slim straight torso, single-line limbs each half a torso long, two dot eyes + one mouth stroke, tiny teal scarf at left of neck, palette black/teal + one muted warm accent.
- **أرقام / params:** stroke 5 px @1080 px; head 25% height; limb segment 0.5 torso
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/stickman.mjs:8` · `fastify-motion-bro/skills/stickman/SKILL.md:12`

#### CHAR-03 · قفل صورة الشخصية المرجعية · Stickman reference-image lock · ✅ مُثبت هنا
- **ماذا / what:** If the user has their own stick figure, prompts reference the attached image unchanged and the generator must accept image input; text-only tools are refused.
- **كيف / how:** image='yes' -> REF block; referenceTool 'text-only' throws.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/stickman.mjs:7,27` · `fastify-motion-bro/tests/production-profiles.test.mjs:17-23`

#### CHAR-04 · قفل شخصيتين أصليتين · Dual original character locks · ✅ مُثبت هنا
- **ماذا / what:** Two original family-friendly 3D designs: A a young woman (warm brown skin, curly dark shoulder hair with pale-blue ribbon, emerald jacket, cream boots); B a waist-high doll-like figure (porcelain face, lilac bob, coral/turquoise patchwork, amber buttons, teal boots).
- **كيف / how:** GIRL and DOLL constants pasted into all 10 image prompts.
- **أرقام / params:** B height = waist of A
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/character-romance.mjs:3-4` · `fastify-motion-bro/tests/production-profiles.test.mjs:24-28`

#### CHAR-05 · قفل الرياضي بلا وجه · Faceless sculpt-render athlete lock · ✅ مُثبت هنا
- **ماذا / what:** Identical style text for every fitness clip: faceless muscular sculpt-render body, black cap and shorts, dark gym, single overhead teal-blue rim light, black falloff, shallow DOF, premium fitness-app look; needs an attached reference image.
- **كيف / how:** STYLE constant embedded in all 5 prompts.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/fitness.mjs:15` · `fastify-motion-bro/skills/fitness/SKILL.md:13`

#### CHAR-06 · أرنب محشو مُجهز · Rigged plush bunny (SDF) · ✅ مُثبت هنا
- **ماذا / what:** A sculpted cute rabbit with pivots for head, ears, tail; eyes placed by ray hits; w-mouth; mint scarf.
- **كيف / how:** const b=K3S.bunny({fur, belly, pink, nose, scarf, cells, material}); animate b.parts.head/earL/earR/tail rotations.
- **أرقام / params:** fur #f2e4d8; belly #fbf3ea; pink #ff9fb8; nose #ff7c9c; blush #ff8fab; scarf #7fe7b4; ~0.33 m tall; tested 183,752 triangles, ~4.6 s mesh time
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:453` · `100-superskills/skills/kosif-montage-motion/tests/test_shape_kit.py:40`

#### CHAR-07 · هيكل قط متجهي مع دورة مشي · Vector cat rig with gait cycle · ✅ مُثبت هنا
- **ماذا / what:** An orange tabby walks, notices, crouches, jumps a puddle on a parabola, lands with a squash, walks on and looks back; four legs are separately articulated with quadratic knees and a swing/stance foot cycle.
- **كيف / how:** pose(t): walk x = 430+59t (gait 1.12 Hz) until 4.1 s; crouch 14 px; jump u∈[5.2,6.9] → x 671.9→1050, height 147·4u(1−u), body angle −14°→12°; land crouch 18·sin; walk 48 px/s at .98 Hz; limb(): stance 60% of cycle, swing lifts 21·sin(πv); tail 12 sin 2.2t + 3 sin 5t; head attention lift and 3/4 look-back after 9.7 s.
- **أرقام / params:** jump peak 147 px
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:59` · `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:67` · `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:77`

#### CHAR-08 · فراشة مرشدة ترفرف · Butterfly guide with wing flap · ✅ مُثبت هنا
- **ماذا / what:** A glowing butterfly leads the hero: wings flap by horizontal scale and it bobs on a sine path with a cyan halo.
- **كيف / how:** wing = |sin(2π·4.5t)|·.85 + .13 as scaleX; y = 348 − 20 sin 1.8t − 48 smooth((t−4.2)/1.8) + 55 smooth((t−7)/2); fill #86fff0 .87; halo r 28.
- **أرقام / params:** 4.5 Hz flap
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:107`

#### CHAR-09 · أرنب قطيفة منحوت بأجزاء مفصلية · SDF plush bunny with rig parts · ✅ مُثبت هنا
- **ماذا / what:** A cute plush bunny generated procedurally with named rig parts (body, head, earL/earR, tail, eyes, mouth, scarf) and a stage disc; ears pivot from the skull.
- **كيف / how:** S.bunny({cells:136}) → {group, parts, stats:{triangles, head.cell_m}}; S.stageDisc({radius .24, color 0x9dffb4, shadow .5}); S.studioBackdrop({inner #22504a, mid #0d2627, outer #040b0c, cy .4}); test bunny(96 cells) > 50,000 triangles.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:29` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:46` · `100-superskills/skills/kosif-montage-motion/tests/test_shape_kit.py:40`

#### CHAR-10 · شخصية مرسومة في إحداثيات محلية · Posed character group in local coordinates · ✅ مُثبت هنا
- **ماذا / what:** The duck hero is drawn once around its own origin (body, wing, legs, beak, eye highlight, helmet, scarf) and then placed, rotated and scaled as one group, so it can be re-posed or animated as a unit.
- **كيف / how:** Collect parts into duck[] then wrap: <g transform='translate(560 392) rotate(-16) scale(1.3)'> with a blurred warm rim glow ellipse behind; loose feathers as small rotated groups.
- **أرقام / params:** translate(560,392) rotate(-16) scale(1.3); rim glow #fb923c rx80 ry54 op .55
- **الدليل / proof:** `kosif-one/projects/duck-vs-dragon/duck_dragon.py:189-228`

#### CHAR-11 · سمك كوي إجرائي · Procedural koi fish · 🟢 جاهز
- **ماذا / what:** Swimming koi with procedural body profile and skin patterns that bend as they swim.
- **كيف / how:** makeKoi({length, seed, kind}).
- **أرقام / params:** kinds kohaku, sanke, showa, ogon; length 0.62 m; 28 rings x 18 segments
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:629` · `kosif-studio/motion/kit/three-kit.js:629`

#### CHAR-12 · سرب طيور · Flock of birds · 🟢 جاهز
- **ماذا / what:** Instanced V-shaped birds that flap in a shader and follow a keyed path, visible between t0 and t1.
- **كيف / how:** K3.makeFlock({n, path:[[t,x,y,z],...], t0, t1, spread, size, color, seed}); mesh.userData.set(t).
- **أرقام / params:** n 18; spread 120; size 9; colour #1a1d22; flap sin(t*9)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:203`

#### CHAR-13 · سمك كوي · Koi fish · 🟢 جاهز
- **ماذا / what:** Procedural koi with lofted body, fins, seeded scale skin in four varieties and a swim bend that leans into turns.
- **كيف / how:** const k=K3.makeKoi({length, seed, kind, amp, caustics}); k.userData.set(t, path(t,out), speedHz).
- **أرقام / params:** kinds kohaku/sanke/showa/ogon; length .62 m; bend amp .11; swim 1.6 Hz; skin 256 px; clearcoat .6
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:613` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:629`

#### CHAR-14 · دوران 360 لورقة الشخصية · Turntable / 360 character sheet · 🟢 جاهز
- **ماذا / what:** Camera steps front, side, back, side with holds, like a character turnaround sheet.
- **كيف / how:** K3.shot('turntable', {subject, size, t0, t1}).
- **أرقام / params:** 4 quarter turns; holds for 70% of each quarter; frame 80% height
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1067`

#### CHAR-15 · عين لطيفة · Cute eye (SDF kit) · 🟢 جاهز
- **ماذا / what:** Glossy flattened eyeball, warm iris ring and two camera-facing catch-lights.
- **كيف / how:** K3S.eye({r, tall, color, iris}).
- **أرقام / params:** r .012 m; tall 1.12; iris #5a3a2c at 55% opacity; catchlights .3r and .14r
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:316`

#### CHAR-16 · عين برمش · Blinking layered eye · 🟢 جاهز
- **ماذا / what:** Sclera, emissive iris, pupil and clearcoat cornea, with a blink control.
- **كيف / how:** const e=K3.makeEye(r,{iris}); e.userData.blink(k 0..1).
- **أرقام / params:** sclera #f4f6f2; iris #8fe02a (emissive 12%); pupil #05070a; cornea opacity .22
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:56`

#### CHAR-17 · أرنب بمفاصل · Primitive rabbit character with joints · 🟢 جاهز
- **ماذا / what:** Plush rabbit from spheres/capsules with named pivots (head, earL/R, armL/R, footL/R, tail, eyes) and optional shell fur.
- **كيف / how:** K3.makeRabbit({color, inner, iris, fur, furLength, layers}); root.userData.joints.
- **أرقام / params:** white #f1f0ea; inner #f3b6c0; iris #3a7bd5; fur length .1, 8 layers
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:74`

#### CHAR-18 · أسد بمفاصل · Primitive lion character with joints · 🟢 جاهز
- **ماذا / what:** Plush lion with mane, legs, tail tuft and named joints; long fur on mane.
- **كيف / how:** K3.makeLion({color, mane, iris, fur, furLength, layers}).
- **أرقام / params:** body #e3b05a; mane #8a4a1c; iris #d9a21b; muzzle #f5e2b8; mane fur 2.6x length, gravity .5
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:101`

#### CHAR-19 · حياة الشخصية في السكون · Character idle life · 🟢 جاهز
- **ماذا / what:** Breathing scale, head sway, periodic blink, ear and tail motion as a pure function of t.
- **كيف / how:** K3.idle(root, t, {amount, phase}).
- **أرقام / params:** breath 1.2% at 2.2 rad/s; blink every 3.7 s lasting 0.3 s; ears .12 rad; tail .35 rad at 3.1 rad/s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:280`

#### CHAR-20 · نزهة قطة — أنيميشن شخصية SVG · Cat walk loop (نزهة قطة) — SVG character animation · 🟢 جاهز
- **ماذا / what:** An 8-second looping cartoon of an orange cat walking right-to-left across a soft garden, with leg cycle, body bob, tail sway, ear/eye detail and a blink, drawn as SVG strings from t.
- **كيف / how:** examples/cat.html: window.render(t) rebuilds the cat group; x = 680 − t·145 with a second copy 1160 px behind for a seamless loop; ?capture hides chrome for frame capture; rendered cat.mp4 and cat.gif shipped.
- **أرقام / params:** 960×540, 8 s; step frequency 1.5 Hz; bob cos(2p)·2 px; tail ±9° at half step rate; blink window 0.095 s every 4 s (offset 2.35 s); palette sky #e9efdf→#f8f3df, fur #efa849→#dc8736, face #f3b453→#e5953c; cat.mp4 960×540 24 fps 192 frames; cat.gif 640×360 12 fps
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cat.html` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cat.mp4` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cat.gif`

#### CHAR-21 · دورة مشي إجرائية للساق · Procedural walk-cycle leg · 🟢 جاهز
- **ماذا / what:** A leg drawn as a curved stroke whose foot swings with sin(phase) and lifts only on the forward half (max(0,cos)), with far legs darker; four legs offset by π give a natural gait.
- **كيف / how:** leg(x, phase, far): foot = x + 22·sin(phase), knee = x + 12·sin(phase), lift = max(0, cos(phase))·15; quadratic path, stroke width 23, round caps; paw stroke 15.
- **أرقام / params:** swing ±22 px, lift 15 px
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cat.html`

#### CHAR-22 · آلة حالات الوضعية · Keyframed pose state machine (walk, crouch, jump, land) · 🟢 جاهز
- **ماذا / what:** Character action as time segments: walk 0–4.1 s, anticipation crouch, a parabolic leap, landing squash, walk again, then a look-up hold; limbs re-pose per segment.
- **كيف / how:** pose(t): walk x=430+59t; crouch 14·smoothstep((t−4.65)/0.55); jump 5.2–6.9 s height 147·4u(1−u) with body angle −14°→+12°; land crouch 18·sin; walk 48 px/s; look = smoothstep((t−9.7)/0.7).
- **أرقام / params:** jump apex 147 px; flight 1.7 s; walk step 1.12 Hz then 0.98 Hz
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:59` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:67`

#### CHAR-23 · فراشة مرافقة ترفرف · Butterfly companion with wing flap · 🟢 جاهز
- **ماذا / what:** A small glowing butterfly that follows the hero and flaps by squashing its wing pair horizontally.
- **كيف / how:** butterfly(t,p): position offset from the hero with smoothstep drifts; wing scaleX = |sin(t·2π·4.5)|·0.85 + 0.13; body halo cyanHalo r 28; wing colour #86fff0.
- **أرقام / params:** flap 4.5 Hz
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:107`

#### CHAR-24 · انضغاط عند الاصطدام · Contact squash · 🟢 جاهز
- **ماذا / what:** On impact an element widens and flattens against the edge it hit, anchored at that edge, then recovers.
- **كيف / how:** MOTION.squash(tl, el, at, {edge, across, along, dur}).
- **أرقام / params:** scaleX 1.08, scaleY 0.90, dur 0.13 s (8 f), E.outSoft
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:372`

#### CHAR-25 · أرنب قطيفة بهيكل حركة · Rigged plush bunny + cute recipe · 🟢 جاهز
- **ماذا / what:** Reference cute character with named joints (body, head, earL, earR, tail, eyes, mouth, scarf) and a measured recipe for 'cute'.
- **كيف / how:** K3S.bunny(o); drive pivots with springs; recipe: head >= body, eyes low and wide, chubby cheeks, short limbs, pastel + one accent, neutral tone curve, breathing +-0.6%, blink, ear flop.
- **أرقام / params:** head width 0.16 vs torso 0.14; eyes at 45% head height spaced 0.4x head width; fur #f2e4d8; ear flop 1.5 Hz zeta 0.42 (2.2 Hz/0.28 broke the 80 px/f gate); bloom threshold >= 0.9
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/shape-kit.js:453` · `kosif-one/tools/kosif-studio/motion/references/shape-kit.md` · `kosif-one/tools/kosif-studio/motion/projects/bunny_twin/src/main.js`

#### CHAR-26 · أرنب وأسد إجرائيان · Procedural rabbit and lion characters · 🟢 جاهز
- **ماذا / what:** Lab-style characters with named joints, glossy eyes, plush/leather/metal materials.
- **كيف / how:** K3.makeRabbit(o), K3.makeLion(o), makeEye, leatherMaterial(0x15171a), metalMaterial(0xd8dde3).
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/lab-kit.js:74` · `kosif-one/tools/kosif-studio/motion/kit/lab-kit.js:101` · `kosif-one/tools/kosif-studio/motion/projects/lab_rabbit_lion/README.md`

#### CHAR-27 · بانِي جناح الخفاش · Bat-wing builder · 🟢 جاهز
- **ماذا / what:** Builds a dragon/bat wing from shoulder, elbow, wrist and finger tips: arm bones, finger bones, veins, a wrist claw and a membrane whose edge sags in scallops between tips.
- **كيف / how:** scenes/dragon_girl.wing(shoulder, elbow, wrist, tips, attach, sag=0.28) -> (membrane, bones, veins).
- **أرقام / params:** bones tube radii 8/6/4.5; fingers 3.4->0.7; scallop 12 samples
- **الدليل / proof:** `kosif-studio/scenes/dragon_girl.py:88`

#### CHAR-28 · أشواك الظهر وصفائح البطن · Creature detail helpers: spikes and belly plates · 🟢 جاهز
- **ماذا / what:** Adds dorsal spines along the top of a body tube and a lighter ribbed belly band, giving reptiles instant anatomy.
- **كيف / how:** scenes/dragon_girl.spikes(spine, radii, every, size) and belly_plates(spine, radii).
- **أرقام / params:** spike height (4+r*.45)*size; rib every 4th sample
- **الدليل / proof:** `kosif-studio/scenes/dragon_girl.py:46` · `kosif-studio/scenes/dragon_girl.py:68`

#### CHAR-29 · شكل الريشة · Feather leaf shape · 🟢 جاهز
- **ماذا / what:** A narrow bending leaf polygon from base to tip used feather by feather for a duck's spread wing.
- **كيف / how:** scenes/duck_dragon.leaf(base, tip, width, bend, n=10).
- **الدليل / proof:** `kosif-studio/scenes/duck_dragon.py:34` · `kosif-studio/scenes/duck_dragon.py:51`

#### CHAR-30 · بناء الشخصية في إطارها المحلي · Character built in its own local frame · 🟢 جاهز
- **ماذا / what:** Designs a body (whale profile, a figure around its feet) in a convenient local coordinate system, then rotates/scales it into the shot — easy re-posing.
- **كيف / how:** whale_dragon W(x,y)/WS(shape) rotate along HEAD->TAIL; dragon_girl xf() scales the girl 1.4x around her feet.
- **أرقام / params:** whale HEAD (700,290) -> TAIL (1200,760); girl K=1.4 around (380,619)
- **الدليل / proof:** `kosif-studio/scenes/whale_dragon.py:46` · `kosif-studio/scenes/dragon_girl.py:288`

#### CHAR-31 · هيكل SVG بنقاط دوران · SVG cut-out rig with pivots · 🟢 جاهز
- **ماذا / what:** Separate SVG groups per limb with explicit pivots; nested <g> rotate transforms.
- **كيف / how:** Remotion Arm: shoulder interpolate frames [0,6,14,24]→[0,8,-55,-48], elbow [2,10,18,26]→[0,5,-30,-24], Easing.inOut(sin); rotate(θ px py).
- **أرقام / params:** parts: head, torso, upper/lower arm, hand, upper/lower leg, foot; elbow 2-frame offset = follow-through
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:17` · `kosif-tool/playbooks/characters.md:54-71`

#### CHAR-32 · جسم جزيئي من الحركة · Particle body from mocap · 📦 بأمر تثبيت
- **ماذا / what:** Fixed-camera video → background difference → seeded points → particle body.
- **كيف / how:** three-kit.js (window.K3) in a --3d project; render --engine studio
- **أرقام / params:** motion.py mocap VIDEO --out body.json; makeParticleBody(json)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:106` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `kosif-studio/motion/kit/three-kit.js:938` · `kosif-studio/motion/references/x-trend-2026.md`

#### CHAR-33 · جسد من الجسيمات · Particle body from real motion (mocap) · 📦 بأمر تثبيت
- **ماذا / what:** A performer filmed on a fixed camera becomes glowing particles inside the silhouette, with tracer ghosts.
- **كيف / how:** python motion.py mocap VIDEO --out body.json (needs opencv); K3.makeParticleBody(json, {height, depth, ghosts, ghostStep, color, size}); userData.set(t, pulse).
- **أرقام / params:** 1200 points; ghosts 3 every 3 frames (alpha .35/k); height 4; colour #ffb36b; size 26
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:938` · `100-superskills/skills/kosif-montage-motion/scripts/qa.py:605` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:938` · `kosif-one/tools/kosif-studio/motion/qa.py`

#### CHAR-34 · شخصية ذكاء اصطناعي متحركة حسب الحالة · Stateful AI persona animation · 📦 بأمر تثبيت
- **ماذا / what:** A narrator/host orb with five conversational states - idle, listening, thinking, speaking, asleep - driven by app or audio state.
- **كيف / how:** Vercel ai-elements Persona (Rive WebGL2; `npx ai-elements add persona` - needs install); a local stand-in: SVG/CSS state classes switched by words.json speaking segments in KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg).
- **أرقام / params:** 5 states
- **تثبيت / install:** `npx ai-elements add persona` - needs install)`
- **الدليل / proof:** `kosif-atlas/skills/2722-vercel/10522-ai-elements/SKILL.md`

#### CHAR-35 · ثبات الشخصية والأسلوب بـ IP-Adapter · IP-Adapter character and style consistency · 📦 بأمر تثبيت
- **ماذا / what:** Condition the model on a reference image to keep a character or transfer a style across many generations.
- **كيف / how:** IPAdapterAdvanced weight 0.55-0.65 for characters (>0.75 copies pose, <0.4 drifts), FaceID 0.7-0.85; weight_type 'style transfer' or 'composition'; two-pass: make one canonical clean reference, then reuse it for all scenes; combine with ControlNet for pose.
- **أرقام / params:** weight 0.55-0.65; FaceID 0.7-0.85
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2819-comfyui/11445-comfyui-workflow-design`

#### CHAR-36 · ستايل الشخصية العصوية · Stickman comic style · 📦 بأمر تثبيت
- **ماذا / what:** A flexible stick figure, cards that drop and stack, and a comic beat for tips with a twist.
- **كيف / how:** STY.stickman: 16:9, bright, 2.1 wps, Readex Pro; bg #FBF9F4 ink #1F2328 accent #F2C94C floor #EFEAE0, colours #EB5757/#F2C94C/#5B8DEF/#9B51E0/#27AE60; sfx pop/hit/tick/shimmer; question lines end with ؟.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:504`

#### CHAR-37 · شخصية لوتي تمشي · Lottie Character Walk · 📦 بأمر تثبيت
- **ماذا / what:** Jointed flat mascot walks in on planted feet, stops and points at a card; body acting from a Lottie JSON, stage in GSAP.
- **كيف / how:** Install with `npx hyperframes add lottie-character-walk` (copies the full composition to compositions/lottie-character-walk.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: lottie-web player, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** assets/mascot.json; 7.5 s; vars: title=Meet your guide; body=Walks in on planted feet, then points the way.; Google Fonts: Inter; 1920x1080; duration 7.5 s
- **تثبيت / install:** `npx hyperframes add lottie-character-walk` (copies the full composition to compositions/lottie-character-walk`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/lottie-character-walk/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/lottie-character-walk/lottie-character-walk.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/lottie-character-walk.mdx`

#### CHAR-38 · محول لوتي · Lottie / dotLottie adapter · 📦 بأمر تثبيت
- **ماذا / what:** After Effects exports play seekably via lottie-web or dotLottie registered on window.__hfLottie; multiple animations against composition time.
- **كيف / how:** adapters/lottie.md patterns; read beat times from file markers (tm frames / fr).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/lottie.md`

#### CHAR-39 · تحريك الشخصيات بلوتي · Lottie character acting (walk cycle, gestures) · 📦 بأمر تثبيت
- **ماذا / what:** Put the character's acting (walk, stop, point, idle) in one Lottie; GSAP owns cards, captions, camera timed to the Lottie's markers; in-place cycles moved with GSAP x matched to stride; license the character.
- **كيف / how:** 1 s walk cycle loop:true; offset actions inside the file (no per-animation start offset); registry block lottie-character-walk.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/lottie.md`

#### CHAR-40 · أرنب كيوت بهيكل · Rigged cute bunny() · 📦 بأمر تثبيت
- **ماذا / what:** Ready rigged bunny (head, ears...).
- **كيف / how:** shape-kit.js / lab-kit.js in a 3D project; read references/shape-kit.md
- **أرقام / params:** K3S.bunny()
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:101` · `100-superskills/skills/kosif-montage-motion/SKILL.md:113` · `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### CHAR-41 · أرنب وأسد بمفاصل · makeRabbit / makeLion rigs · 📦 بأمر تثبيت
- **ماذا / what:** Procedural rabbit and lion with named joints userData.joints; idle breath/blink/ear/tail.
- **كيف / how:** shape-kit.js / lab-kit.js in a 3D project; read references/shape-kit.md
- **أرقام / params:** makeRabbit, makeLion, idle
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:101` · `100-superskills/skills/kosif-montage-motion/SKILL.md:113` · `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### CHAR-42 · حياة الخمول: تنفس ورمش ونظرات · Idle life: breathing, blinks, glances · 📦 بأمر تثبيت
- **ماذا / what:** Characters never freeze: a small breathing scale, head sway on several sines, scheduled blinks and a look toward camera at its stop.
- **كيف / how:** bunny breath .006·sin(2π·0.9t); head (.05 sin1.7t, .12 sin(1.1t+.5), .05 sin1.3t); blinks smooth windows 1.18–1.34 s and 4.62–4.76 s eye scaleY 1−.85·bl; cat blinks at 2.44–2.56, 9.9–10.06, 11.3–11.45 s; lab idle(rabbit, t, {amount 1, phase 0}), head turns 0.25 rad at its stop.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:118` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:133` · `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:77`

#### CHAR-43 · شخصيتا أرنب وأسد قطيفة · Plush rabbit and lion characters (lab kit) · 📦 بأمر تثبيت
- **ماذا / what:** Two plush animals with joints (head, eyes, ears, tail) on a cream studio sweep, with a callout HUD naming parts and a part swap (rabbit tail recoloured and scaled into a lion tuft).
- **كيف / how:** K3.makeRabbit({color, inner, iris, layers 7, furLength .09}); makeLion({color, mane, iris, layers 8, furLength .07}); studio(scene); labPost(renderer,…,{bloom:0}); swap: tail colour lerp to 0x8a4a1c, scale 1+.45·sw over 16.4–17.2 s.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/src/main.js:12` · `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/src/main.js:44`

#### CHAR-44 · صياد بسيط من كبسولات · Low-poly fisherman silhouette · 📦 بأمر تثبيت
- **ماذا / what:** A seated figure seen from behind built from capsules and spheres, with cap and rod whose line drops into the water: enough to read as a person in silhouette.
- **كيف / how:** torso Capsule(.2,.42) rotated −.18; head sphere .13 + cap half-sphere 0xcfc6b2; legs capsules; rod cylinder .008→.02 oriented by quaternion from base to tip; Line to water.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:96`

#### CHAR-45 · عيون لامعة · Glossy eyes + tubes · 📦 بأمر تثبيت
- **ماذا / what:** Glossy eyes with two catch-lights, mouth/stitch tubes.
- **كيف / how:** K3S.eye({r}), glossMaterial, tube(points,r,colour)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/shape-kit.md`

#### CHAR-46 · شخصية الأرنب · Bunny reference character · 📦 بأمر تثبيت
- **ماذا / what:** Rigged body/head/ears/tail/eyes/mouth/scarf.
- **كيف / how:** K3S.bunny(o); example projects/bunny_twin 5 s 1080x1920
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/shape-kit.md`

#### CHAR-47 · حركة ثانوية بالنوابض · Spring rig secondary motion · 📦 بأمر تثبيت
- **ماذا / what:** Pivot groups driven by spring(t,t0,freq,damping) under speed gate.
- **أرقام / params:** ear 1.5 Hz ζ0.42 ok; 2.2 Hz ζ0.28 fails 80 px/frame at 1080x1920
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/shape-kit.md`

#### CHAR-48 · دوال مشاهد جاهزة · Ready scene helpers (dragon set) · 📦 بأمر تثبيت
- **ماذا / what:** Importable cloud, ridge (mountains), wing (bat wing), flame, tongue, spikes, belly_plates; sample scenes dragon_girl, duck_dragon, whale_dragon, whale_dragon_3d.html.
- **كيف / how:** from scenes.dragon_girl import ...
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/scripts/scenes/dragon_girl.py` · `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md`

#### CHAR-49 · دوران ورقة الشخصية · Turntable character sheet · 📦 بأمر تثبيت
- **ماذا / what:** Front -> side -> back -> side holds, the 360° continuity sheet rendered before animating a character.
- **كيف / how:** K3.shot('turntable', {subject, size, t0, t1}).
- **أرقام / params:** 4 holds, each turns in the last 30% of its quarter
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:1066` · `kosif-studio/motion/references/book-lessons.md`

#### CHAR-50 · عين لامعة لطيفة · Glossy cute eye · 📦 بأمر تثبيت
- **ماذا / what:** Clearcoat dark eyeball with a warm iris ring and two catch-lights facing the camera.
- **كيف / how:** K3S.eye({r, tall, color, iris}); K3S.glossMaterial(color, {roughness, env}).
- **أرقام / params:** r .012, tall 1.12, depth .78; iris #5a3a2c opacity .55; catch-lights r .3 and .14 upper-outer; gloss roughness .08, clearcoat 1, ior 1.5, env 1.6
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/shape-kit.js:311`

#### CHAR-51 · أنابيب للخطوط · Tube strokes (mouth, stitches) · 📦 بأمر تثبيت
- **ماذا / what:** Catmull-Rom tube for mouths, stitches, whiskers.
- **كيف / how:** K3S.tube(points, r, colour, {segments}).
- **أرقام / params:** 32 segments, 8 radial; mouth r 1.1 mm
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/shape-kit.js:329`

#### CHAR-52 · أرنب محشو مجهز · Rigged plush bunny · 📦 بأمر تثبيت
- **ماذا / what:** Reference cute character: body, head on neck pivot, ears on root pivots, tail, glossy eyes placed by raycast, 'w' mouth, mint scarf.
- **كيف / how:** const b = K3S.bunny({fur, belly, pink, nose, scarf, cells, material}); animate b.parts.head/earL/earR/tail.
- **أرقام / params:** fur #f2e4d8, belly #fbf3ea, pink #ff9fb8, nose #ff7c9c, blush #ff8fab, scarf #7fe7b4, mouth #6b3540; ~0.33 m tall; cells 132; neck pivot [0,.152,.004]
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/shape-kit.js:453` · `kosif-studio/motion/references/shape-kit.md`

#### CHAR-53 · عين بطبقات ورمش · Layered eye with blink · 📦 بأمر تثبيت
- **ماذا / what:** Sclera, emissive iris, pupil and clearcoat cornea; blink by squashing y.
- **كيف / how:** K3.makeEye(r, {iris}); eye.userData.blink(k).
- **أرقام / params:** sclera #f4f6f2, iris #8fe02a default, pupil #05070a, cornea opacity .22; blink scale 1-.92k
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/lab-kit.js:56`

#### CHAR-54 · أرنب إجرائي · Procedural plush rabbit · 📦 بأمر تثبيت
- **ماذا / what:** Primitive-built rabbit with named joints (head, ears, arms, feet, tail, eyes) and optional shell fur.
- **كيف / how:** K3.makeRabbit({color, inner, iris, fur, furLength, layers}); root.userData.joints.
- **أرقام / params:** colour #f1f0ea, inner #f3b6c0, iris #3a7bd5, fur length .1, 8 layers
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/lab-kit.js:74`

#### CHAR-55 · أسد إجرائي · Procedural plush lion · 📦 بأمر تثبيت
- **ماذا / what:** Primitive-built lion with mane, muzzle, four legs, tail tuft and named joints; long fur on mane.
- **كيف / how:** K3.makeLion({color, mane, iris, fur, furLength, layers}).
- **أرقام / params:** colour #e3b05a, mane #8a4a1c, iris #d9a21b, muzzle #f5e2b8, fur .08 (mane ×2.6, gravity .5)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/lab-kit.js:101`

#### CHAR-56 · حياة الخمول · Idle life cycle · 📦 بأمر تثبيت
- **ماذا / what:** Breath, head drift, periodic blink, ear and tail motion for any lab character.
- **كيف / how:** K3.idle(root, t, {amount, phase}).
- **أرقام / params:** breath ±1.2% at 2.2 rad/s; blink every 3.7 s lasting .3 s; ears ±.12 rad at 2.6; tail ±.35 at 3.1
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/lab-kit.js:280`

#### CHAR-57 · مختبر الأرنب والأسد · Plush rabbit and lion lab · 📦 بأمر تثبيت
- **ماذا / what:** Two plush fur characters on a cream studio sweep; one lens circles them and the HUD names six beats SHAPE → JOINT → LOAD → BREAK → SWAP → RANK.
- **كيف / how:** motion.py new NAME --lab; lab-kit makeRabbit/makeLion/schematic/orbitWalk/studio/hud/labPost/idle
- **أرقام / params:** 960×540 24 fps 20 s; rabbit #F2F0EA inner #F1B7C3 iris #3A7BD5 7 fur layers 0.09; lion #E6B35B mane #8A4A1C iris #D9A21B 8 layers 0.07
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/lab_rabbit_lion/src/main.js:1` · `kosif-studio/motion/projects/lab_rabbit_lion/README.md`

#### CHAR-58 · لوحات كوميكس · Style: Comics panels (comics-panels) · 📦 بأمر تثبيت
- **ماذا / what:** Story told in comic-book panels with gutters, speech balloons and camera moving panel to panel.
- **كيف / how:** Canvas/SVG panel grid; each panel a scene with pose-to-pose rig; camera rig pans between panels; balloons pop with spring; ink outlines. Scaffold: python3 tools/kosif.py scaffold comics-panels <dir>.
- **أرقام / params:** key poses every 8-16 frames; anticipation 4-8 frames
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:comics-panels` · `kosif-tool/playbooks/characters.md`

#### CHAR-59 · أنمي أكشن · Style: Anime action (anime-action) · 📦 بأمر تثبيت
- **ماذا / what:** Dynamic anime-inspired action: speed lines, impact frames, smears.
- **كيف / how:** 2D rig + smear frames, speed-line overlays, camera shake; anticipation 4-8 frames, overshoot 5-10%. Original designs only. Scaffold: python3 tools/kosif.py scaffold anime-action <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:anime-action` · `kosif-tool/playbooks/characters.md`

#### CHAR-60 · تحريك هيكلي · Style: Character rig (character-rig) · 📦 بأمر تثبيت
- **ماذا / what:** Skeletal 2D/SVG character with pivots, walk cycles and lip-flap.
- **كيف / how:** SVG groups with transform-origin pivots; walk 12 frames/step at 24fps; 5-7 mouth shapes; moving hold 1-2%. Scaffold: python3 tools/kosif.py scaffold character-rig <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:character-rig` · `kosif-tool/playbooks/characters.md`

#### CHAR-61 · شخصيات عصوية · Style: Stickman (stickman) · 📦 بأمر تثبيت
- **ماذا / what:** Flexible stick-figure character comedy.
- **كيف / how:** SVG line rig with pivots, arcs, squash; on twos optional. Scaffold: python3 tools/kosif.py scaffold stickman <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:stickman` · `kosif-tool/playbooks/characters.md`

#### CHAR-62 · شخصيات · Category: Characters · 📦 بأمر تثبيت
- **ماذا / what:** Capability family 'characters' (47 catalog entries) with a dedicated bilingual playbook of timings and recipes.
- **كيف / how:** Read playbooks/characters.md (visual grammar, motion mechanics, scene recipes, QA); build in starters/html-canvas or starters/remotion; filter catalog with python3 tools/kosif.py list --category characters.
- **أرقام / params:** keys every 8-16 frames; anticipation 4-8f; follow-through 2-4f; walk 12f/step; 5-7 mouth shapes
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/characters.md` · `kosif-tool/catalog/categories.json` · `kosif-tool/catalog/meta.json`

#### CHAR-63 · صفحات ويبتون بأسلوب تشيبي · Pastel chibi webtoon pages · 🔑 مفتاح/خدمة
- **ماذا / what:** Fixed animal character descriptions repeated verbatim in every prompt for identity consistency, white background, editable text overlay SVG for dialogue.
- **كيف / how:** Image model (external) for art; SVG text overlay for correct (Arabic) lettering.
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2423-akbun-draw-webtoon-b`

#### CHAR-64 · جملة الشخصية المكررة حرفيًا لضمان الثبات · Character sentence reused verbatim across a series · 🔑 مفتاح/خدمة
- **ماذا / what:** Image models keep no memory between calls, so a recurring character must be defined once in one sentence and pasted unchanged into every scene prompt.
- **كيف / how:** Write CHARACTER: <body shape, colours, face, clothing> once; copy it byte-for-byte into each prompt; keep background tone and 3-5 colour palette identical; vary only the SCENE line.
- **أرقام / params:** palette 3-5 colours per scene
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2421-akbun-draw-storytellingimage` · `kosif-atlas/skills/2976-pwdev-social-media/12595-visual-consistency`

#### CHAR-65 · ثبات الشخصية بمراجع متعددة في جيميناي · Multi-reference character consistency in Gemini · 🔑 مفتاح/خدمة
- **ماذا / what:** Feed several reference images of each character, name them, and keep 2-3 identifiers in every follow-up prompt.
- **كيف / how:** Provide 4-5 references per character from different angles; label 'Character A: the red-haired knight'; in multi-turn chat say 'the same character' and repeat hair/clothing/face identifiers.
- **أرقام / params:** 4-5 refs per character (max 5 per request in generate-image skill)
- **الدليل / proof:** `kosif-atlas/skills/881-codex-seo/1954-seo-image-gen` · `kosif-atlas/skills/2173-tools-plugin/7917-generate-image`

#### CHAR-66 · تعديل الصورة المرجعية بدل توليدها · Edit the supplied avatar instead of regenerating it · 🔑 مفتاح/خدمة
- **ماذا / what:** When the user's person/avatar image exists and the setting does not change, edit that image; composing a new scene makes a different person.
- **كيف / how:** Use 'Edit @Image1: ...' phrasing, keep face/hair/lighting unchanged; audit references (product, avatar, scene) and ask for a missing avatar before generating.
- **الدليل / proof:** `kosif-atlas/skills/259-quickdesign/865-quickdesign`

#### CHAR-67 · الأفاتار الناطق بالذكاء الاصطناعي · AI talking avatars (HeyGen, Synthesia) · 🔑 مفتاح/خدمة
- **ماذا / what:** Script-driven presenter videos with lip-sync without filming; HeyGen offers an MCP server, many avatars and languages and personal digital twins.
- **كيف / how:** HeyGen MCP or API: send script, avatar, language; custom twin from a 2-5 min recording; Synthesia for full-body corporate presenters. Composite the avatar layer under coded motion graphics.
- **أرقام / params:** 230+ avatars; 140+ languages; twin from 2-5 min video
- **الدليل / proof:** `kosif-atlas/skills/1446-marketing-skills/3531-video`

#### CHAR-68 · أوراق الشخصيات والمواقع كمراسي توليد · Character and set sheets as generation anchors · 🔑 مفتاح/خدمة
- **ماذا / what:** One image call per sheet gives references for every later clip: characters in front, three-quarter and profile on a plain ground with one telling prop; sets empty and lit to the style.
- **كيف / how:** Generate, check against STYLE.md, redo off-style sheets and keyframes before animating (an image costs cents, a clip dollars).
- **أرقام / params:** front / 3/4 / profile
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video` · `kosif-atlas/skills/1511-homie/3889-art`

#### CHAR-69 · شريط حركة كامل من إطار مرجعي واحد · Whole-strip sprite animation from one seed frame · 🔑 مفتاح/خدمة
- **ماذا / what:** Generate a mascot's whole animation strip in one edit request around an approved frame, because frame-by-frame generation drifts.
- **كيف / how:** Place the seed on a transparent 1024 canvas with 4 slots of 256; prompt invariants (same character, facing, palette, silhouette, outfit, transparent background, exact frame count, no scenery); normalise to fixed frames (e.g. 64 px) with one shared scale and bottom-centre anchor; optionally lock frame 1 to the seed; review a preview sheet.
- **أرقام / params:** canvas 1024; slot 256; 4 frames; 64 px frames
- **الدليل / proof:** `kosif-atlas/skills/2696-game-studio/10368-sprite-pipeline`

#### CHAR-70 · شخصية هندسية بتحكي · Geometric mascot direction (characters category) · 🔑 مفتاح/خدمة
- **ماذا / what:** Prompt direction for Claude-coded mascots: circle body, dot eyes, squash and stretch, anticipation, blinking, reacting to on-screen text.
- **كيف / how:** FILM_CATS 'characters' guide + template 'character' (hop in, point at 3 cards, react, wave).
- **الدليل / proof:** `app/public/js/00_editor.js:2007` · `app/public/js/00_editor.js:1777`

#### CHAR-71 · مقدم أفاتار · Avatar presenter · 🔑 مفتاح/خدمة
- **ماذا / what:** Combine a presenter clip (e.g. HeyGen avatar) with editable scenes.
- **كيف / how:** Keep clip as project media.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/avatar-presenter.mdx`

#### CHAR-72 · شخصية قصاصات بمفاصل · Cut-out character rig with facing dial · 👁 شوهد في فيديو
- **ماذا / what:** separate head, near/far arm, legs, body; rotate around pivots; one face value -1..1 shifts facial features and swaps near/far arm; walk phase derived from distance travelled so feet do not slide
- **أرقام / params:** arm swing +-20 deg, head bob 2-3 px, step length ~40 px
- **الدليل / proof:** `style:doodle`

#### CHAR-73 · تبديل الشخصية بنفخة دخان · Class/character swap gag · 👁 شوهد في فيديو
- **ماذا / what:** Same position, swap sprite (wizard -> knight -> rogue) via a pixel smoke puff each new spell
- **أرقام / params:** puff 6-8 frames
- **الدليل / proof:** `style:pm-0xevinho-3777d8`

#### CHAR-74 · ظهور من خلف الأفق · Pop-up from behind horizon · 👁 شوهد في فيديو
- **ماذا / what:** Characters start masked below the hill line and rise with back-out overshoot, then idle bob ±3 px; stagger left to right
- **أرقام / params:** rise 350 ms easeOutBack(1.6), stagger 150-250 ms
- **الدليل / proof:** `style:pm-abderrahmen-g-9e8ed0`

#### CHAR-75 · تحول وتركيب الأجزاء · Transform & dock · 👁 شوهد في فيديو
- **ماذا / what:** parts tween rotation/position into slots, camera shake on contact
- **أرقام / params:** shake 6 px 150 ms
- **الدليل / proof:** `style:pm-allforbigfire-86ff3c`

#### CHAR-76 · تميمة فقاعة كلام · Speech-bubble mascot · 👁 شوهد في فيديو
- **ماذا / what:** glossy white blob with tail, kawaii eyes, blush, blink and squash
- **أرقام / params:** bounce 1.1/0.9
- **الدليل / proof:** `style:pm-anas0ra-e57aea`

#### CHAR-77 · تحويل جسم إلى شخصية بعيون · Object-as-character face rig · 👁 شوهد في فيديو
- **ماذا / what:** Add two glossy black spheres (metalness 0.6, roughness 0.15) slightly protruding from face plus capsule brows; animate brow y/rotation and eye scaleY for blink (100 ms)
- **أرقام / params:** eye radius ~8% tile width; blink every 2-4 s
- **الدليل / proof:** `style:pm-anilraok-eff262`

#### CHAR-78 · تميمة مرافقة للعلامة · Brand mascot companion · 👁 شوهد في فيديو
- **ماذا / what:** simple spiky SVG blob with 2 eyes; idle wobble (rotate +/-4 deg, scale 0.97-1.03), hops between corners, reacts to scenes
- **أرقام / params:** size ~8-15% frame, wobble 1.2 s loop
- **الدليل / proof:** `style:pm-anthonyriera-9b1b2a`

#### CHAR-79 · تحريك دراجة بدواسات متزامنة · Pedalling bicycle rig · 👁 شوهد في فيديو
- **ماذا / what:** crank angle θ(t)=ω t; pedals at θ and θ+π; legs solved with 2-bone IK from hip to pedal; wheels rotate at gear ratio × ω
- **أرقام / params:** ω ~ 2π×1 Hz; gear ratio ~2.5; wheel radius 0.33 m
- **الدليل / proof:** `style:pm-axtonliu-0b861d`

#### CHAR-80 · حركة احتفال للشخصية · Character celebration pose · 👁 شوهد في فيديو
- **ماذا / what:** blend from riding pose to wings-spread pose over ~0.8 s with overshoot, hold, return
- **أرقام / params:** wing span rotation ~70°, ease back.out
- **الدليل / proof:** `style:pm-axtonliu-0b861d`

#### CHAR-81 · حروف نوم طافية · Floating Z sleep glyphs · 👁 شوهد في فيديو
- **ماذا / what:** Z glyphs rise, scale up and fade sequentially
- **أرقام / params:** stagger 250 ms
- **الدليل / proof:** `style:pm-cansincengiz-me-cf68dd`

#### CHAR-82 · هيكل شخصية وضعية لوضعية · Pose-to-pose stick rig · 👁 شوهد في فيديو
- **ماذا / what:** joint angles per pose, interpolate with easeInOut 400 ms, hold 1 s
- **الدليل / proof:** `style:pm-chrisjdimarco-f068db`

#### CHAR-83 · أشياء بعيون · Googly-eye objects · 👁 شوهد في فيديو
- **ماذا / what:** add eyes to everyday props
- **الدليل / proof:** `style:pm-davidshulmanfl-371638`

#### CHAR-84 · شخصية عصوية · Doodle stick figure · 👁 شوهد في فيديو
- **ماذا / what:** SVG stroke figures, pose swap every 0.5 s with boil
- **الدليل / proof:** `style:pm-devius-maximus-beab45`

#### CHAR-85 · روبوت بوجه شاشة معبّر · Screen-face robot emotions · 👁 شوهد في فيديو
- **ماذا / what:** eyes/mouth as glyph shapes on display, swap per emotion
- **الدليل / proof:** `style:pm-faroukzy-9ff23e`

#### CHAR-86 · عداء بتمويه حركة يقفز حواجز · Motion-blurred runner figure · 👁 شوهد في فيديو
- **ماذا / what:** Simple limb rig (stick/flat figure) run cycle along a baseline with hurdles; add directional motion blur and a figure caption
- **أرقام / params:** cycle 8 frames, jump arc 400 ms
- **الدليل / proof:** `style:pm-fionntobin-97b7af`

#### CHAR-87 · كرة شخصية بوجه وإكسسوار · Mascot ball with face and prop · 👁 شوهد في فيديو
- **ماذا / what:** Egg-scaled sphere with emissive orange material, two eye decals, a cone/disc hat with a point light as headlamp; squash on landing
- **أرقام / params:** scale (1,1.25,1), squash y 0.75 for 80 ms
- **الدليل / proof:** `style:pm-gorden-sun-041f56`

#### CHAR-88 · كرة بالانضغاط والتمدد · Squash & stretch ball · 👁 شوهد في فيديو
- **ماذا / what:** scaleY/scaleX inverse pair driven by velocity (stretch along motion) and impact (squash 1.3x/0.7 for ~80 ms)
- **أرقام / params:** preserve area: sx*sy=1
- **الدليل / proof:** `style:pm-himanshutwtxs-5f4b43`

#### CHAR-89 · مسرح شخصية بديكور واحد ثابت · Single-set character stage · 👁 شوهد في فيديو
- **ماذا / what:** Build one illustrated room as SVG layers (background wall, window, props, desk front) with the character layer between desk back and desk front so arms/body tuck behind
- **أرقام / params:** layers ~6, character pivot at desk line
- **الدليل / proof:** `style:pm-jake11moran-a269c4`

#### CHAR-90 · تبديل تعابير الوجه · Expression swap rig · 👁 شوهد في فيديو
- **ماذا / what:** Box body with eye/mouth sprite variants (dots, ^ ^ joy, angry brows, hearts, wink+tongue) swapped on beats; add sweat-drop and sparkle overlays
- **أرقام / params:** 8 expression states, swap in 1 frame, small bounce 6px
- **الدليل / proof:** `style:pm-jake11moran-a269c4`

#### CHAR-91 · شخصية ظلية مسطحة · Flat silhouette character staging · 👁 شوهد في فيديو
- **ماذا / what:** single dark fill character (cap, long coat) with 2-3 jointed limbs, side profile; readable only by outline against lit backgrounds
- **أرقام / params:** fill ~#0d0c0b, no internal detail
- **الدليل / proof:** `style:pm-kamstudiolabs-0b0824`

#### CHAR-92 · شخصية يراعة متوهجة · Glowing firefly character · 👁 شوهد في فيديو
- **ماذا / what:** oval body, big eyes, wing flap 8 Hz, radial gradient glow on tail
- **الدليل / proof:** `style:pm-kamstudiolabs-c9bb28`

#### CHAR-93 · قفزة شخصية على قوس · Mascot hop arc · 👁 شوهد في فيديو
- **ماذا / what:** Silhouette sprite follows dotted parabola, dots drawn trailing behind, lands with squash
- **أرقام / params:** arc ~1 s
- **الدليل / proof:** `style:pm-kangaroohere-b10f8d`

#### CHAR-94 · كشف الشخصية البطل · Mascot hero reveal · 👁 شوهد في فيديو
- **ماذا / what:** 3D render PNG fades/scales in with glow
- **الدليل / proof:** `style:pm-kentcdodds-6fa8cf`

#### CHAR-95 · تميمة بكسل تمشي · Walking pixel mascot · 👁 شوهد في فيديو
- **ماذا / what:** 8-bit sprite of horizontal bricks with two eyes and four legs; 2-frame leg swap + 2 px bob, slides along with the camera
- **أرقام / params:** ~6 fps cycle, colour #d17c55
- **الدليل / proof:** `style:pm-lemomo-ai-0d9cff`

#### CHAR-96 · شخصية تكبر · Same character aging · 👁 شوهد في فيديو
- **ماذا / what:** swap rig variant per stage keeping colours
- **الدليل / proof:** `style:pm-loicrambo-ad6830`

#### CHAR-97 · شخصية خطية متوهجة · Glowing stickman logo · 👁 شوهد في فيديو
- **ماذا / what:** stroke figure in lime with blur glow, walk cycle
- **الدليل / proof:** `style:pm-marklaunches-3b9492`

#### CHAR-98 · تميمة على دائرة ملونة · Mascot on colour disc · 👁 شوهد في فيديو
- **ماذا / what:** cut-out character PNG pops in (scale 0.8 -> 1.05 -> 1) while a pastel circle grows behind it; add a name pill 'Name: role' under it
- **أرقام / params:** pop 300 ms, disc 400 ms
- **الدليل / proof:** `style:pm-paulo-kombucha-96431c`

#### CHAR-99 · شخصيات كرتونية من أشكال أولية · Primitive toon characters · 👁 شوهد في فيديو
- **ماذا / what:** spheres/capsules, big eyes, toon material, hierarchical joints
- **الدليل / proof:** `style:pm-ryzoft-4f85bd`

#### CHAR-100 · تحريك رسمة واحدة بعظام · 2D mesh bone rig from one image · 👁 شوهد في فيديو
- **ماذا / what:** split illustration into parts, mesh deform with ~16 bones, sine-based dance cycles
- **أرقام / params:** bpm 150
- **الدليل / proof:** `style:pm-topi-003-b0e12c`

#### CHAR-101 · صورة رمزية مسطحة · Flat avatar bust · 👁 شوهد في فيديو
- **ماذا / what:** circle head + shoulders + tie, accessories (hat, glasses)
- **الدليل / proof:** `style:pm-triglyceee-bd5b08`

#### CHAR-102 · ظل يجري · Silhouette sprite run · 👁 شوهد في فيديو
- **ماذا / what:** looping galloping silhouette over speed lines
- **الدليل / proof:** `style:pm-utopyaszx-1b2f94`

#### CHAR-103 · أطراف بـ IK بعظمتين وانثناء ناعم · Two-bone IK limbs with smooth bend · 👁 شوهد في فيديو
- **ماذا / what:** pose = hip position, torso tilt, head tilt, facing + world targets for hands/feet; solve elbow/knee with 2-bone IK, bend direction from facing (elbow back, knee forward); draw limb as quadratic curve 
- **كيف / how:** pose = hip position, torso tilt, head tilt, facing + world targets for hands/feet; solve elbow/knee with 2-bone IK, bend direction from facing (elbow back, knee forward); draw limb as quadratic curve with control = 2J - (S+E)/2 so it passes through the joint
- **أرقام / params:** stroke ~3 px, round caps
- **الدليل / proof:** `style:stickman`

#### CHAR-104 · انحناء الجسم وتمدده حسب السرعة · Velocity-driven body bend + squash/stretch · 👁 شوهد في فيديو
- **ماذا / what:** torso is a quadratic bezier tube hip->neck drawn twice (wide black then thinner white on top); bend amount from d(tilt)/dt between frames; stretch/squash from vertical hip velocity plus landing impuls
- **كيف / how:** torso is a quadratic bezier tube hip->neck drawn twice (wide black then thinner white on top); bend amount from d(tilt)/dt between frames; stretch/squash from vertical hip velocity plus landing impulses; head lags slightly
- **أرقام / params:** tube width ~38 px, squash 0.85-1.15
- **الدليل / proof:** `style:stickman`

#### CHAR-105 · وجه معبر بتبديل العينين والفم · Swappable expressive face · 👁 شوهد في فيديو
- **ماذا / what:** eyes as dots with periodic blink (scaleY to 0.1 for 80 ms), brows as short strokes with angle per emotion, mouth path per emotion (smile, flat, O + sweat drop, grit, content)
- **أرقام / params:** blink every 2.5-4 s
- **الدليل / proof:** `style:stickman`

#### CHAR-106 · قطرة بوجه تدور على مسار منقط · Character droplet on dotted loop · 👁 شوهد في فيديو
- **ماذا / what:** dotted closed path around the cycle; droplet with face sampled along it by getPointAtLength over ~3 s, slight bob
- **أرقام / params:** dash 2/6, droplet 20 px
- **الدليل / proof:** `style:whiteboard`

#### CHAR-107 · مبادئ تحريك الشخصيات · Animation principles for character clips · 📄 موصوف
- **ماذا / what:** Locomotion needs contact/passing/extreme poses with planted feet; actions need readable anticipation, contact and recovery; hold impact frames; keep volumes constant.
- **كيف / how:** Define clip names, durations, loop, event markers (contact, hit window, footsteps); check body bob and limb separation; player-facing attacks avoid long anticipation; verify encoded frame count/fps/duration.
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4162-game-animation/SKILL.md` · `kosif-atlas/skills/2460-pixel-art/9525-animate/SKILL.md`

#### CHAR-108 · مواصفة الشخصية الثابتة (دستور التميمة) · Canonical character spec (mascot bible) · 📄 موصوف
- **ماذا / what:** Keep one canonical spec per recurring character, separate from style skills: silhouette, fixed features (e.g. dot eyes, small curved mouth, tiny fins), proportions (features inside the front third), outline weight and colour, default palette (#FFFFFF belly, #D9D9D9 back, #F0F0F0 cheek, #1A1A1A outli…
- **كيف / how:** Store JSON/MD in the project; build an SVG rig with grouped parts and pivots so every video reuses the same character; expressions as swappable eye/mouth shapes.
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2427-akbun-mascot-whale/SKILL.md`

#### CHAR-109 · حزمة مراجع زوايا الشخصية · Turnaround reference package · 📄 موصوف
- **ماذا / what:** Before animating a character, lock consistent views: front, side, rear (other side if asymmetric), three-quarter and the in-video camera view, on one ground line and scale; add face/material details, expressions and key poses; reconcile differences between views and prefer separate readable images o…
- **كيف / how:** Draw in SVG or generate with a fixed seed (external model); fixed-camera Blender blockout renders as reference need a Blender install.
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4166-game-concept-art/SKILL.md`

#### CHAR-110 · أقفال الاستمرارية · Continuity locks CHR/LOC · 📄 موصوف
- **ماذا / what:** 360° character (CHR-001) and location (LOC-001) sheets with verbatim lock text in every prompt; turntable shot as 3D sheet.
- **كيف / how:** Write lock paragraphs; shot('turntable')
- **أرقام / params:** views front/¾/profile/back; 5 expressions
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/continuity-protocols.md` · `100-superskills/skills/kosif-montage-motion/references/book-lessons.md`

#### CHAR-111 · وصفة الكيوت · Cute recipe · 📄 موصوف
- **ماذا / what:** Head>=body, low wide eyes, cheeks, tiny nose, soft blends, short limbs, pastel+one accent, toy lighting, alive acting.
- **أرقام / params:** head 0.16 vs torso 0.14; eyes at ~45% head height, spacing 0.4x; blends 10-30 mm; fur #f2e4d8; breathing ±0.6%
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/shape-kit.md`

#### CHAR-112 · صحائف مرجعية 360° للشخصيات والأماكن · CHR-/LOC- 360-degree reference sheets · 📄 موصوف
- **ماذا / what:** Locks a recurring character or location once (views, expressions, wardrobe, layout) and reuses its lock paragraph verbatim in every later prompt to stop identity drift.
- **كيف / how:** Character CHR-001: name, age, build, skin/hair/eyes, marks; views front, 3/4 left, profile, back, full-body contrapposto; expressions neutral, joy, anger, fear, determination; wardrobe fabrics; one lock paragraph. Location LOC-001: era, scale, left/right/centre landmarks, HDRI-style 360 description, time-of-day variants. Prefer reference images when the platform supports them. identity_reference.py checks 5 views (front, left, right, back, three_quarter).
- **أرقام / params:** 5 views; 5 expressions
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/continuity-protocols.md` · `kosif-one/tools/kosif-omni/skills/kosif-think-pro/scripts/identity_reference.py`

#### CHAR-113 · قفل الشخصية النفسي · Personality lock for characters · 📄 موصوف
- **ماذا / what:** Translates a fictional character's personality facets into posture, gaze and styling cues so acting stays consistent across shots.
- **كيف / how:** Pick 4-6 Big-Five facets; map to cues (assertive: squared shoulders, direct gaze, centre frame; anxious: guarded arms, glance off-camera, tense jaw; ordered: pressed clothes, symmetrical workspace...); add 3 if-then behaviour signatures and the driving need (autonomy/competence/relatedness). Fictional characters only.
- **أرقام / params:** 4-6 facets; 3 if-then rules
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/character-psychology.md`

#### CHAR-114 · قالب قفل الشخصية · Character Lock template · 📄 موصوف
- **ماذا / what:** One-line identity spec reused verbatim across prompts.
- **كيف / how:** NAME · age · skin tone · face shape · eyes · brows · nose · lips · hair · build/height · signature outfit · accessories · distinctive marks · MUST NOT CHANGE: ...
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/prompt-library.md`

#### CHAR-115 · ريغ شخصية SVG · SVG character rig with pivots · 📄 موصوف
- **ماذا / what:** Character from circles/rects in <g> groups pivoting at shoulder, hip, neck.
- **كيف / how:** Build character.svg + rig.js; transform-origin per joint.
- **أرقام / params:** 3 expressions on sheet
- **الدليل / proof:** `100-superskills/skills/character-animation-2d/SKILL.md`

#### CHAR-116 · دورات مشي وسكون وكلام · Phase-driven walk/idle/talk cycles · 📄 موصوف
- **ماذا / what:** Cycles are functions of phase giving limb angles and body height.
- **كيف / how:** walk(phase), idle(phase), talk(phase); distinct contact and passing poses.
- **الدليل / proof:** `100-superskills/skills/character-animation-2d/SKILL.md`

#### CHAR-117 · مبادئ التحريك · 12-principles subset for rigs · 📄 موصوف
- **ماذا / what:** Anticipation, squash on landing, follow-through for hair/cloth, arcs; constant volumes.
- **الدليل / proof:** `100-superskills/skills/character-animation-2d/SKILL.md`

#### CHAR-118 · ورقة شخصية 360 · 360 character sheet + 4-angle location sheet · 📄 موصوف
- **ماذا / what:** Front/side/back/expressions sheet per character and a 4-angle sheet per location for continuity.
- **كيف / how:** prompt each view with same locks
- **أرقام / params:** 4 views + expressions
- **الدليل / proof:** `100-superskills/skills/cinema-director-7layers/SKILL.md:22`

#### CHAR-119 · وصفة الشخصية اللطيفة · Cute character recipe · 📄 موصوف
- **ماذا / what:** Proportion and look rules that made the bunny read as cute.
- **كيف / how:** Apply when sculpting any mascot with K3S.
- **أرقام / params:** head width ≥ body (.16 vs .14); eyes at ~45% head height, spacing .4×head width, tall 1.12, 2 catch-lights; cheeks k≈.02; nose ≤ 1/8 head width; blend 10-30 mm; short limbs, big feet; pastel + one accent; warm key front-left-top, mint+pink rims, tone 'neutral', bloom threshold ≥ .9; breathing ±0.6%,…
- **الدليل / proof:** `kosif-studio/motion/references/shape-kit.md`

#### CHAR-120 · ورقة تصميم الشخصية · Character model sheet · 📄 موصوف
- **ماذا / what:** Write proportions, palette, line weight and views in STYLE.md before animating; original designs only.
- **أرقام / params:** 3–5 colours; front/side/three-quarter views
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:15` · `kosif-tool/playbooks/characters.md:9`

#### CHAR-121 · اختبار الظل الأسود · Silhouette test · 📄 موصوف
- **ماذا / what:** Every key pose must read as a solid black shape.
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:16`

#### CHAR-122 · وجوه بتبديل الأشكال · Swap-shape faces and mouth set · 📄 موصوف
- **ماذا / what:** Eyes and mouth are swapped shapes, not distorted paths; closed mouth on M/B/P.
- **كيف / how:** Mouth index from phoneme/word timing.
- **أرقام / params:** 5–7 mouth shapes; switch within 1 frame
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:18` · `kosif-tool/playbooks/characters.md:30`

#### CHAR-123 · الوضعيات المفتاحية أولًا · Pose-to-pose blocking · 📄 موصوف
- **ماذا / what:** Block keys then breakdowns.
- **أرقام / params:** keys every 8–16 frames at 24–30 fps
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:24`

#### CHAR-124 · دورة المشي · Walk cycle · 📄 موصوف
- **ماذا / what:** Contact-down-passing-up cycle with body bob; walk in place with background parallax at stride speed.
- **أرقام / params:** 24 frames per two steps at 24 fps (12/step); bob 3–5% height; bg speed = stride / 0.5 s
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:27` · `kosif-tool/playbooks/characters.md:46`

#### CHAR-125 · ثبات متحرك (تنفس) · Moving hold / breathing · 📄 موصوف
- **ماذا / what:** Character never freezes during holds.
- **كيف / how:** Sine scale on torso.
- **أرقام / params:** 1–2% scale over 2 s
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:28`

#### CHAR-126 · وصفة لحظة رد الفعل · Reaction beat recipe · 📄 موصوف
- **ماذا / what:** Sink, jump, land with squash, hair follow-through, breathing hold.
- **أرقام / params:** 0–200 ms sink 4% ease-in sine; 200–450 jump ease-out cubic; 450–700 land squash 8% spring 12/200; 450–800 follow-through; 800–2000 hold
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:36-44`

#### CHAR-127 · الحديث للكاميرا · Talk-to-camera behaviours · 📄 موصوف
- **ماذا / what:** Head tilts on stress, periodic blinks, mouth from phoneme timing.
- **أرقام / params:** tilt ±3°; blink every 2.5–4 s, 3-frame blink
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:48`

#### CHAR-128 · الإشارة والكشف · Point and reveal · 📄 موصوف
- **ماذا / what:** Arm extends on arc; target pops after finger stops.
- **أرقام / params:** arm 350 ms; target pops +80 ms
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:50`

#### CHAR-129 · دخول الشخصية من اليمين · RTL character staging · 📄 موصوف
- **ماذا / what:** In Arabic films characters enter from right, look left; speech bubbles hold whole phrases RTL.
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:75`

#### CHAR-130 · شخصية ساحر بكسل · Pixel wizard character loop · 💡 فكرة
- **ماذا / what:** Reusable pixel wizard with walk, staff-raise (6 stepped frames), 2-frame hat overshoot and rotating rune circle at 8 fps.
- **كيف / how:** Sprite sheets in Canvas/Remotion.
- **أرقام / params:** 10 s, 16:9
- **الدليل / proof:** `style:pm-0xevinho-3777d8`

#### CHAR-131 · قفزة بضغط ومط · Squash/stretch hop with anticipation · 💡 فكرة
- **ماذا / what:** Character hops with crouch anticipation and overshoot landing.
- **كيف / how:** Scale keyframes + cubic-bezier landing.
- **أرقام / params:** squash 0.85 / stretch 1.15; 120 ms crouch; land cubic-bezier(0.34,1.56,0.64,1) 450 ms
- **الدليل / proof:** `style:pm-abderrahmen-g-9e8ed0`

#### CHAR-132 · شخصيات متقطعة وواجهة ناعمة · Stepped characters, smooth UI · 💡 فكرة
- **ماذا / what:** Characters on twos, UI smooth; never mixed on one element.
- **كيف / how:** CSS steps(12) per second.
- **أرقام / params:** 2-frame holds
- **الدليل / proof:** `style:pm-jake11moran-a269c4`

#### CHAR-133 · شخصية ظلية · Silhouette 2-3 joint rig · 💡 فكرة
- **ماذا / what:** Flat silhouettes with few joints, walk 12 frames/step at 24 fps cadence.
- **أرقام / params:** 12 frames/step
- **الدليل / proof:** `style:pm-kamstudiolabs-0b0824`

#### CHAR-134 · تميمة مطاطية · Squash-stretch mascot · 💡 فكرة
- **ماذا / what:** Rubbery mascot with squash on landing, stretch at take-off, limb overlap.
- **كيف / how:** Back-out easing + scale keys.
- **أرقام / params:** cubic-bezier(0.34,1.56,0.64,1); squash 80%, stretch 115%; limbs 60 ms overlap
- **الدليل / proof:** `style:pm-paulo-kombucha-96431c`
