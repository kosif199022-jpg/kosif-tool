# الكاميرا والتكوين — Camera & composition

> فصل مُجمَّع آليًا من 446 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **421 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 421 powers deduplicated by name from 446 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 13 · 🟢 جاهز 45 · 📦 بأمر تثبيت 122 · 🔑 مفتاح/خدمة 14 · 👁 شوهد في فيديو 145 · 📄 موصوف 70 · 💡 فكرة 15 · المجموع / total 424

**إضافات v2 — v2 additions:** CAM-X01 … CAM-X03 (3) — في آخر الفصل / at the end of this chapter.

#### CAM-01 · مسار تكبير لوغاريتمي · Log-space zoom track · ✅ مُثبت هنا
- **ماذا / what:** Spring track on log(scale) for camera zooms with several targets.
- **كيف / how:** MOTION.zoomTrack(t, [[t,scale],...], preset).
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:88` · `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### CAM-02 · هيكل مساحة عمل بثلاثة أعمدة · Three-column RTL workspace shell · ✅ مُثبت هنا
- **ماذا / what:** Sticky 72px glass top bar, left/right rails and a central stage that collapse progressively; at 768px it becomes a 4-tab bottom nav with safe-area padding.
- **كيف / how:** grid-template-columns 196px | 1fr | 300px; breakpoints 1550/1280/1024/768/480; 100dvh with @supports fallback.
- **أرقام / params:** topbar 72px (64px mobile) blur 12px; rails 184-196px & 300px; bottom nav min-height calc(68px + env(safe-area-inset-bottom)); padding 24/16/12px
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:308` · `kosif-audit-pro/app/globals.css:2617` · `kosif-audit-pro/tests/responsive.test.mjs`

#### CAM-03 · تخطيط بخصائص منطقية للاتجاه · RTL logical-property layout · ✅ مُثبت هنا
- **ماذا / what:** All spacing/positioning uses inline/block logical properties so the same CSS mirrors correctly for Arabic.
- **كيف / how:** inset-inline-*, inset-block-*, padding-inline, margin-block, border-inline-start; html lang=ar dir=rtl.
- **الدليل / proof:** `kosif-audit-pro/app/globals.css` · `kosif-audit-pro/app/layout.tsx`

#### CAM-04 · تخطيط حسب المقاس · Aspect-specific kinetic layout · ✅ مُثبت هنا
- **ماذا / what:** Layout rules baked into the style line: 9:16 lockups upper middle with 10% safe margins and object off-centre lower third; 16:9 text left third, objects right; 1:1 centred type above object; 40–50% negative space; top-centre wordmark strip.
- **كيف / how:** makePrompts style string switch on c.ratio.
- **أرقام / params:** margins 10%; negative space 40–50%
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:101`

#### CAM-05 · تدرج أحجام اللقطات · Stickman shot-size progression · ✅ مُثبت هنا
- **ماذا / what:** Five-clip camera plan that escalates with the story arc: wide establishing, medium eye-level, over-the-shoulder three-quarter, slightly low angle, close-up on posture with room for the reveal.
- **كيف / how:** shots[] in stickman.mjs mapped to clips 1–5; video prompt camera 'steady with subtle horizontal follow', final clip 'very slow push-in'; 9:16 with a defined floor line.
- **أرقام / params:** 5 shot sizes; push-in on clip 5
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/stickman.mjs:31,36-37`

#### CAM-06 · تغطية بعدستين 35/85 · Two-lens emotional coverage (35/85 mm) · ✅ مُثبت هنا
- **ماذا / what:** Each story beat is covered twice: a wide 35 mm establishing frame with layered depth and an intimate 85 mm close-up on hands, posture and eyes.
- **كيف / how:** character-romance image prompt j=0 -> 35 mm wide, j=1 -> 85 mm close-up, both 9:16.
- **أرقام / params:** 35 mm wide; 85 mm close-up
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/character-romance.mjs:18`

#### CAM-07 · كاميرا طعام ثابتة 45° · Locked 45° food macro camera · ✅ مُثبت هنا
- **ماذا / what:** Fixed tripod three-quarter medium food close-up at 45 degrees with a 50 mm look and shallow depth of field, allowing only tiny motivated macro pushes.
- **كيف / how:** camera constant in food-flow prompts; identical in every clip.
- **أرقام / params:** 45°; 50 mm; shallow DOF
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/food-flow.mjs:32`

#### CAM-08 · مفاتيح الكاميرا · Camera keys (smoothstep) · ✅ مُثبت هنا
- **ماذا / what:** Camera position + look target keyed in time with smoothstep between keys (still between events).
- **كيف / how:** const camAt=K3.cameraKeys([[t,x,y,z,lx,ly,lz],...]); const [p,l]=camAt(t); camera.position.copy(p); camera.lookAt(l).
- **أرقام / params:** keys: [t, camX, camY, camZ, lookX, lookY, lookZ]
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:414`

#### CAM-09 · بارالاكس متعدد الطبقات مع اقتراب · Multi-plane SVG parallax with push-in · ✅ مُثبت هنا
- **ماذا / what:** A 2.5D camera track: each layer translates by its own factor of one camera value while a slow zoom centred low in frame pushes in; a black foreground alley edge moves fastest.
- **كيف / how:** cam = lerp(0, 630, smooth(t/12)); zoom = 1 + .10·smooth(t/12) around (640,500); moon ×.035, far skyline ×.19, mid buildings ×.68, street & hero ×1.0, foreground ×1.38; letterbox bars 36 px.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:124`

#### CAM-10 · وضع النص بعيداً عن الوجه ضمن الحدود الآمنة · Safe-area and face-aware text placement · ✅ مُثبت هنا
- **ماذا / what:** Automatic edit plans keep keywords below the detected face box and captions inside the 9:16 safe area.
- **كيف / how:** direct.plan(segs, shots[{box, cx, cy}], stress, 1080, 1920, dur): every key with t in the face shot has y > (box.y+box.h)·1920; captions y ≤ 0.80·1920; proplan safe_area text_top_pct 15.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_directors.py:30` · `100-superskills/skills/kosif-montage-motion/tests/test_core.py:54`

#### CAM-11 · مفردات حركة الكاميرا · Camera-move vocabulary + one-move rule · ✅ مُثبت هنا
- **ماذا / what:** Recognised moves: push-in, pull-out, dolly, tracking, orbit, arc, crane, handheld, whip pan, pan, tilt, rack focus, dolly-zoom, drone, flyover, static, locked-off, POV, zoom; lint rejects more than one per shot.
- **كيف / how:** video_prompt_forge lint multi_camera
- **أرقام / params:** 1 move per shot
- **الدليل / proof:** `100-superskills/skills/video-prompt-director/scripts/video_prompt_forge.py:24` · `100-superskills/skills/video-prompt-director/scripts/video_prompt_forge.py:40`

#### CAM-12 · ترتيب النص الآمن حول الوجه · Text-safe layout stack · ✅ مُثبت هنا
- **ماذا / what:** Vertical stack from face down: keyword under the chin, caption under the keyword; motifs on the free side; text never over eyes or mouth.
- **كيف / how:** direct.plan layout
- **أرقام / params:** keyY = clip(face bottom + 1.5 % H, 0.50 H, 0.66 H); capY = clip(keyY + 13.5 % H, 0.64 H, 0.80 H); motif x 0.20 W or 0.80 W opposite the face
- **الدليل / proof:** `kosif-studio/motion/direct.py:108` · `kosif-studio/tests/test_studio.py:910`

#### CAM-13 · كاميرا ثنائية الأبعاد بمفاتيح · Keyframed 2D camera (cameraAt/applyCamera) · ✅ مُثبت هنا
- **ماذا / what:** Camera keys {t,x,y,scale,rot} are eased (inOutCubic) and applied to a #world wrapper as pan, then scale/rotate around stage centre; captions stay outside so they remain pinned.
- **كيف / how:** applyCamera(world, cameraAt(camKeys,t), 1080, 1920)
- **أرقام / params:** sample punches: 1.0->1.08 at 3.4 s, y -40 & 1.04 at 7.2 s, 1.12 & rot -1.5deg at 10.4 s, settle 1.02 at 12 s
- **الدليل / proof:** `kosif-tool/starters/html-canvas/timeline.js:52` · `kosif-tool/starters/html-canvas/index.html:106`

#### CAM-14 · ثبات حي · Living hold (breathe) · 🟢 جاهز
- **ماذا / what:** Keeps a hold alive with a slow scale creep and optional drift so frames never freeze.
- **كيف / how:** MOTION.breathe(tl, cam, at, dur, {creep, drift}).
- **أرقام / params:** creep 0.04 scale/s default (templates use .012-.02); drift px per frame x60
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:321` · `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:321` · `kosif-studio/motion/kit/motion-kit.js:321`

#### CAM-15 · اختلاف المنظر · Layer parallax · 🟢 جاهز
- **ماذا / what:** Multiple layers drift by depth factor (far moves less) for 2.5D depth.
- **كيف / how:** MOTION.parallax(tl, [{el, depth}], at, dur, {dx, dy, scale, ease}).
- **أرقام / params:** offset = dx*depth, scale 1+scale*depth; ease none
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:543` · `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:543` · `kosif-one/tools/kosif-studio/motion/references/motion-craft.md` · `kosif-studio/motion/kit/motion-kit.js:543`

#### CAM-16 · نقل البؤرة · Rack focus without animated blur · 🟢 جاهز
- **ماذا / what:** Fakes a focus pull by cross-fading a sharp element and a constant-blur twin (animating large blur steps visibly).
- **كيف / how:** MOTION.rackFocus(tl, el, at, {blur, dur, to:'sharp'|'blur'}).
- **أرقام / params:** blur 18 px, dur 0.3 s, E.smooth
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:352` · `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:351-360` · `kosif-studio/motion/kit/motion-kit.js:352`

#### CAM-17 · اهتزاز الكاميرا · Camera shake / hit · 🟢 جاهز
- **ماذا / what:** Decaying seeded jitter in x, y and rotation for impacts.
- **كيف / how:** MOTION.shake(tl, el, at, {amp, dur, hz, rot, seed}).
- **أرقام / params:** amp 14 px (y x0.7); dur 0.5 s; 28 Hz; rot 0.6 deg; decay (1-i/n)^1.8; settle 0.12 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:535` · `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:535`

#### CAM-18 · مسار كاميرا منحني · Centripetal Catmull-Rom camera path · 🟢 جاهز
- **ماذا / what:** Camera and target follow centripetal Catmull-Rom curves so moves never stop dead between keys.
- **كيف / how:** const path=K3.cameraPath(keys); [pos, look]=path(t).
- **أرقام / params:** ease mix: 35% smoothstep + 65% linear
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:789` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:789` · `kosif-one/tools/kosif-studio/motion/references/craft-numbers.md`

#### CAM-19 · دوللي زووم · Dolly zoom (Vertigo) · 🟢 جاهز
- **ماذا / what:** Dolly in while widening fov so the subject keeps its size and the background stretches.
- **كيف / how:** K3.shot('dolly_zoom', {from, to, fov}).
- **أرقام / params:** to defaults 0.45x the start distance; fov recomputed each frame
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1070` · `kosif-studio/motion/kit/three-kit.js:1072`

#### CAM-20 · دوران الكاميرا مع توقفات · Orbit walk with stops · 🟢 جاهز
- **ماذا / what:** A lens that walks the circle around the hero object and holds at parts with micro drift.
- **كيف / how:** K3.orbitWalk(camera, [{t, angle, dist, height, look, hold}], {drift}).
- **أرقام / params:** drift 0.012
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/lab-kit.js:172` · `kosif-studio/motion/kit/lab-kit.js:172`

#### CAM-21 · كشف العناصر عند دخولها الإطار · Scroll reveal via IntersectionObserver · 🟢 جاهز
- **ماذا / what:** Elements rise into place when they enter view, children staggered; lightweight class toggling instead of scroll handlers.
- **كيف / how:** IntersectionObserver(rootMargin '0px 0px -100px 0px', threshold 0.1) adds .is-visible; CSS transitions. In video, trigger by timeline time instead.
- **أرقام / params:** y 60->0, 0.8s ease-out-expo; children y 40, 0.6s, delays 0.1/0.2/0.3s
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md` · `kosif-atlas/skills/3529-ui-design/14308-interaction-design/references/scroll-animations.md`

#### CAM-22 · حركة كين بيرنز على لقطات الموقع · Ken Burns on captured screenshots · 🟢 جاهز
- **ماذا / what:** Static captures always move: slow push or pan across a screenshot, often under a tinted overlay, so no still sits dead on screen.
- **كيف / how:** CSS transform scale/translate over beat duration with linear or sine ease; or ffmpeg zoompan.
- **أرقام / params:** zoom 1 -> 1.04 over the beat; 70% overlay for background photos
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/step-4-storyboard.md` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/step-6-build.md`

#### CAM-23 · تقريب الكاميرا عبر viewBox · SVG viewBox camera zoom (drill-down) · 🟢 جاهز
- **ماذا / what:** Animates an SVG map's viewBox from the current frame to a fitted target so the 'camera' flies into a region or city.
- **كيف / how:** animateTo(target): requestAnimationFrame loop, k=(now-t0)/520, eased e=1-(1-k)^3, vb_i = from_i + (target_i-from_i)*e; target box = bbox of points + pad 90 (region) / 70 (city), aspect-fitted to 1000:820.
- **أرقام / params:** 520ms; ease-out cubic; pad 90/70
- **الدليل / proof:** `kosif-earth-ci-fork/ui/features/sales-map.js:86` · `kosif-earth-ci-fork/ui/features/sales-map.js:40`

#### CAM-24 · كاميرا بارالاكس بالمؤشر واللمس والتمرير · Pointer / touch / scroll parallax camera · 🟢 جاهز
- **ماذا / what:** Camera drifts on slow sines and follows the pointer with lag; scrolling dollies it forward and tilts the look-at.
- **كيف / how:** eye=(px*1.6+sin(t*.11)*.6, .4+py+cos(t*.09)*.4, 6.5-scroll*4); lookAt (px*.4, py*.3-scroll*1.5, -8); pointer lerp .06; scroll normalised over min(page,900px).
- **أرقام / params:** lerp .06; dolly 4 units
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/crystal-world.js:179` · `kosif-earth-ci-fork/ui/art/crystal-world.js:209`

#### CAM-25 · أغطية تدرّج لقراءة النص فوق الفيديو · Legibility veils over footage · 🟢 جاهز
- **ماذا / what:** Two stacked gradients darken the text side and the bottom of a full-bleed video so Arabic copy stays readable; phones switch to a mostly-bottom veil and re-centre the subject.
- **كيف / how:** desktop: linear-gradient(90deg,rgba(4,9,17,.78),rgba(4,9,17,.18) 58%,rgba(4,9,17,.24)), linear-gradient(0deg,rgba(4,9,17,.85),transparent 57%); phone (<=700px): 0deg .92 -> .2 at 76% and object-position 83% center.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/brand/earth-intro-20261009.css:6` · `kosif-earth-ci-fork/ui/art/brand/earth-intro-20261009.css:27`

#### CAM-26 · تلاشي الصورة داخل البطاقة بالقناع · Masked art fade on cards · 🟢 جاهز
- **ماذا / what:** Sector/gate cards carry a picture on the far side that fades into the card with a gradient mask, toned to the brand.
- **كيف / how:** .gate.has-art::after width 30% background var(--art) cover; mask-image linear-gradient(to right, ink 35%, transparent); filter grayscale sepia; EARTH door: width 25% opacity .58 saturate(.86) contrast(.92).
- **الدليل / proof:** `kosif-earth-ci-fork/unlock.html:127` · `kosif-earth-ci-fork/ui/art/brand/earth-office-door.css`

#### CAM-27 · كاميرا مقيدة بدفع بصري · Locked restrained camera · 🟢 جاهز
- **ماذا / what:** Editorial camera: locked lens with a slow 4% optical push and slight Z drift, no shake.
- **كيف / how:** State in motion prompt; in Canvas approximate with depth scale breathing.
- **أرقام / params:** push 4%; no shake
- **الدليل / proof:** `fastify-motion-bro/scripts/viral-editorial.mjs:68` · `fastify-motion-bro/docs/VIRAL-EDITORIAL-DNA.md:23`

#### CAM-28 · تخطيط آمن للهاتف · Phone-safe vertical layout · 🟢 جاهز
- **ماذا / what:** 1080x1920 centre composition with 10% side margins and clean negative space.
- **كيف / how:** Place hero at ~40% height, headline ~73%, footer ~91%; maxWidth 84% of width.
- **أرقام / params:** 1080x1920; margins 10%
- **الدليل / proof:** `fastify-motion-bro/docs/VIRAL-EDITORIAL-DNA.md:17` · `fastify-motion-bro/web/editorial.js:56,77`

#### CAM-29 · تخطيطات الفيديو والبطاقة الأربعة · Recut layouts: split / stack / pip / overlay · 🟢 جاهز
- **ماذا / what:** Four video+card canvas recipes with exact #video-wrap targets: split (landscape video 960x1080 at left 960; portrait bottom half 1080x960), stack (top 52%: 1892x548 at 14,14; portrait top 44% 1080x844), pip (400x300 at 1480,760; portrait 360x203 at 690,28 + .framed), overlay (full bleed + glass card…
- **كيف / how:** references/layouts/<key>.html give videoBounds + cardBounds; tween #video-wrap per card window.
- **أرقام / params:** see what
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/talking-head-recut/references/layouts/split.html` · `kosif-one/vendor/hyperframes/skills/talking-head-recut/references/layouts/pip.html` · `kosif-one/vendor/hyperframes/skills/talking-head-recut/references/DESIGN_INDEX.md`

#### CAM-30 · إطارات الفيديو الزخرفية · Recut video frames: clean / hairline / polaroid · 🟢 جاهز
- **ماذا / what:** Decorative chrome around the video: clean (none, default), hairline (double stroke + four viewfinder corner ticks), polaroid (white photo frame + Caveat label + blue washi tape).
- **كيف / how:** Add references/frames/<key>.html as sibling of #video-wrap; skip hairline/polaroid over overlay layout.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/talking-head-recut/references/frames/hairline.html` · `kosif-one/vendor/hyperframes/skills/talking-head-recut/references/frames/polaroid.html`

#### CAM-31 · حركة الكاميرا للمسرح · Stage camera move (camera) · 🟢 جاهز
- **ماذا / what:** Moves the whole stage as one camera (x, y, scale, rotation); house rule: count the moves, stay still between.
- **كيف / how:** Wrap content in #cam; MOTION.camera(tl, cam, at, {x, y, scale, rotation, dur, ease, origin}).
- **أرقام / params:** dur 1.4 s; ease E.cam(.48,.1,0,.9)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:311`

#### CAM-32 · دفع الكاميرا · Log-space camera push (push) · 🟢 جاهز
- **ماذا / what:** A push-in or pull-out whose zoom speed feels constant.
- **كيف / how:** MOTION.push(tl, cam, at, from, to, dur, {ease, origin}); dur defaults from durFor.
- **أرقام / params:** typical 1.0 -> 1.04..1.08 over the hold; peak ~5% scale/frame
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:316`

#### CAM-33 · تحويل البؤرة · Rack focus by crossfade · 🟢 جاهز
- **ماذا / what:** Simulates focus pulls by crossfading the sharp element with a constant-blur twin (avoids stepping animated blur).
- **كيف / how:** MOTION.rackFocus(tl, el, at, {blur, dur, to:'sharp'|'blur'}).
- **أرقام / params:** blur 18 px; dur 0.3 s; ease E.smooth
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:352`

#### CAM-34 · عمق الميدان · Bokeh depth of field · 🟢 جاهز
- **ماذا / what:** BokehPass DOF with focus distance driven per frame (or by applyShot).
- **كيف / how:** post.bokeh.uniforms.focus.value = distance; aperture/maxblur options.
- **أرقام / params:** focus 900; aperture 0.00004; maxblur 0.0035
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:387` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1089`

#### CAM-35 · لغة اللقطات · Shot language cameras (20 kinds) · 🟢 جاهز
- **ماذا / what:** Deterministic cameras for named shot types with framing computed from subject size and fov.
- **كيف / how:** const cam=K3.shot(kind,{subject, size, t0, t1, fov, azimuth, distance, degrees, roll, velocity, handheld, low, high, dutch}); K3.applyShot(camera, cam(t), post).
- **أرقام / params:** kinds: establishing(6% frame height) wide(25%) medium(55%) closeup(160%) extreme_closeup(400%) low_angle high_angle birds_eye dutch(12 deg) tracking(1.2 m/s) crane_up crane_down push_in pull_back orbit(360) arc(60) handheld dolly_zoom whip_pan(90) turntable; fov 35; azimuth -20
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1038` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1086`

#### CAM-36 · كاميرا محمولة · Handheld camera noise · 🟢 جاهز
- **ماذا / what:** Three octaves of smooth seeded noise around a ~1.3 Hz sway plus slight roll.
- **كيف / how:** K3.shot(kind, {handheld:true, shake}) or kind 'handheld'.
- **أرقام / params:** amplitude 0.012 x distance x shake; frequencies 1.3/1.1/0.9 Hz with 2.17x and 4.9x harmonics
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1047`

#### CAM-37 · كاميرا تدور وتتوقف · Orbit walk camera with stops · 🟢 جاهز
- **ماذا / what:** A lens walking around the subject on the shorter arc, holding at stops with micro drift, fov per stop.
- **كيف / how:** const walk=K3.orbitWalk(camera,[{t, angle, dist, height, look:[x,y,z]|Object3D, fov, hold}], {drift, fov}); walk(t); walk.lookPoint for DOF.
- **أرقام / params:** drift .012; fov 32 default; smoothstep between stops
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:172`

#### CAM-38 · زووم كين بيرنز · Ken Burns zoom · 🟢 جاهز
- **ماذا / what:** Slow zoom on clip/still.
- **كيف / how:** timeline clip 'zoom':{'from':1.0,'to':1.08}
- **أرقام / params:** 1.0→1.08
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:899`

#### CAM-39 · ملاءمة الإطار · Fit modes cover/contain/blur · 🟢 جاهز
- **ماذا / what:** Fit footage to frame by crop, letterbox pad, or blurred-fill background.
- **كيف / how:** timeline 'fit'; blur = gblur sigma 40 + brightness -0.12 sat .85
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:316`

#### CAM-40 · إعادة تأطير ذكية · Smart reframe · 🟢 جاهز
- **ماذا / what:** Face-aware crop / centre crop / blurred pad to target ratio.
- **كيف / how:** tools.py aspect CLIP --to 9:16 --mode smart
- **أرقام / params:** ratios 9:16,16:9,1:1,4:5,4:3,21:9
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/tools.py:44`

#### CAM-41 · مفردات حركة الكاميرا · Camera move vocabulary (2D and 3D) · 🟢 جاهز
- **ماذا / what:** Ten named camera moves the planner and manifest accept: five for 2D motion and five for 3D shots.
- **كيف / how:** Set scene.camera / shot.camera_move to one of the names; validate_manifest() rejects anything else.
- **أرقام / params:** 2D: fast_reveal, slow_push, match_cut, focus_lift, still_hold · 3D: dolly_in, orbit, side_track, push_in, locked
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:29` · `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:59`

#### CAM-42 · ملاءمة اللقطة: ملء أو احتواء · Clip fit: cover vs contain · 🟢 جاهز
- **ماذا / what:** Media clips either fill the frame with edge cropping or show the whole picture letterboxed on the project background colour.
- **كيف / how:** fitImage(): scale = max(w/iw, h/ih) for cover or min(...) for contain; centred drawImage.
- **أرقام / params:** default cover; background default #07111e
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:72`

#### CAM-43 · كاميرا بارالاكس متعددة الطبقات · Multi-plane parallax camera with slow push · 🟢 جاهز
- **ماذا / what:** Depth from layers moving at different rates under one camera track, plus a gentle zoom: far sky slowest, mid buildings, ground, then fast foreground alley edges.
- **كيف / how:** cam = lerp(0, 630, smoothstep(t/12)); zoom 1 → 1.10 (smoothstep) about (640,500); translate far ×0.19, moon ×0.035, mid ×0.68, ground ×1.0, foreground ×1.38.
- **أرقام / params:** track 630 px over 12 s; zoom +10%
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:124`

#### CAM-44 · إطار سينمائي: أشرطة ونقش وبطاقات · Cinematic frame: letterbox bars, vignette and minimalist cards · 🟢 جاهز
- **ماذا / what:** Black top and bottom bars, a horizontal edge vignette, a tiny tracked-out brand line and a light-weight widely spaced title for a filmic look.
- **كيف / how:** 36 px bars #020711 top and bottom; vignette linearGradient #020611 .8 → 0 (17%) … 0 (80%) → .75; labels 9–10 px letter-spacing 3; title 43 px weight 300 spacing 10 with an accent rule #ed9f64.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:124`

#### CAM-45 · فحص التكوين · Composition check: saliency centroid, thirds, symmetry · 🟢 جاهز
- **ماذا / what:** Finds the visual centre of strong edges and reports whether it sits on a rule-of-thirds point, centred or off-grid, plus mirror symmetry and the nearest standard aspect ratio.
- **كيف / how:** Gradient magnitude above max(p99, 0.3·max) as saliency; distance to the four thirds points; symmetry = 1 − mean|I − mirror(I)|/255; nearest_ratio() over 12 ratios.
- **أرقام / params:** thirds if distance < 0.08, centred if < 0.08 from centre; ratios 1:1, 4:5, 3:4, 2:3, 9:16, 5:4, 4:3, 3:2, 16:9, 1.85:1, 2:1, 2.39:1
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:24` · `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:114` · `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:120`

#### CAM-46 · التعريض المكافئ · Equivalent exposure · 🟢 جاهز
- **ماذا / what:** Deterministic photo/cinema light maths op 'equivalent' for planning believable lighting in shots, prompts and 3D scenes.
- **كيف / how:** echo JSON | python3 scripts/omni/light_calc.py (one op or a list) — {op:'equivalent', aperture, shutter, iso, new_aperture, new_iso} → matching shutter + handheld warning
- **أرقام / params:** f/2.8 1/125 → f/1.4 = 1/500 s; warns slower than 1/60 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/light_calc.py:52`

#### CAM-47 · زاوية الغالق إلى سرعة الغالق · Shutter angle → shutter speed (motion blur) · 🟢 جاهز
- **ماذا / what:** Deterministic photo/cinema light maths op 'shutter_angle' for planning believable lighting in shots, prompts and 3D scenes.
- **كيف / how:** echo JSON | python3 scripts/omni/light_calc.py (one op or a list) — {op:'shutter_angle', fps, angle} → angle/360/fps
- **أرقام / params:** 24 fps 180° → 1/48 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/light_calc.py:84`

#### CAM-48 · كاميرا المسرح الواحدة · Single 2D stage camera · 🟢 جاهز
- **ماذا / what:** The whole stage moves as one camera (x, y, scale, rotation); count the moves and keep still in between.
- **كيف / how:** MOTION.camera(tl, stage, at, {x, y, scale, rotation, dur, ease, origin}).
- **أرقام / params:** dur 1.4 s, ease E.cam
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:311` · `kosif-one/tools/kosif-studio/motion/references/motion-craft.md`

#### CAM-49 · دفع الكاميرا للداخل · Log-space camera push · 🟢 جاهز
- **ماذا / what:** A push-in whose scale changes in log space so it feels constant.
- **كيف / how:** MOTION.push(tl, stage, at, from, to, dur, {ease, origin}); default duration from durFor.
- **أرقام / params:** pushes 1.5-3.1x over 30-70 f; peak ~5% scale/frame
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:316` · `kosif-one/tools/kosif-studio/motion/references/craft-numbers.md`

#### CAM-50 · تمويه السرعة الاتجاهي · Directional speed blur · 🟢 جاهز
- **ماذا / what:** An SVG Gaussian blur along one axis that swells and clears over a fast move.
- **كيف / how:** MOTION.speedBlur(tl, el, at, dur, {px, axis}).
- **أرقام / params:** 12 px peak at 45% of the move (E.in up, E.out down)
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:378`

#### CAM-51 · مفاتيح كاميرا ناعمة · Smooth camera keys (3D) · 🟢 جاهز
- **ماذا / what:** Camera position and look target interpolated with smoothstep between keys, still between events.
- **كيف / how:** const cam = cameraKeys([[t,x,y,z,lx,ly,lz],...]); [pos, look] = cam(t).
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:414`

#### CAM-52 · مفردات اللقطات ككاميرات · Shot vocabulary as deterministic 3D cameras · 🟢 جاهز
- **ماذا / what:** Director/Veo shot words become camera functions: framing by subject size and fov, moves, dolly zoom with constant subject size, seeded handheld.
- **كيف / how:** shot(kind, {subject, size, t0, t1, fov, azimuth, degrees, ...}); shotFromWords('low angle tracking shot'); sequence([{at, shot}]) hard cuts; applyShot(camera, s, post) sets DOF focus.
- **أرقام / params:** kinds: establishing(0.06 frame), wide(0.25), medium(0.55), closeup(1.6), extreme_closeup(4.0), low_angle, high_angle, birds_eye, dutch(12 deg), tracking, crane_up, crane_down, push_in, pull_back, orbit(360), arc(60), handheld(~1.3 Hz 3 octaves), dolly_zoom(to 0.45 d), whip_pan(90), turntable
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:1038` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:1092` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:1210`

#### CAM-53 · تمويه البؤرة والحركة · Lens defocus and motion blur ops · 🟢 جاهز
- **ماذا / what:** Depth-of-field blur on the whole canvas or a shape, and directional motion blur on a shape.
- **كيف / how:** defocus(radius, shape=None, soft=30); motion_blur(shape, length, angle=90, mix=1).
- **الدليل / proof:** `kosif-one/tools/kosif-studio/render.py:692` · `kosif-one/tools/kosif-studio/render.py:707`

#### CAM-54 · ترتيب طبقات الكاميرا · Camera stack order · 🟢 جاهز
- **ماذا / what:** Make a painting look photographed by applying, in order: defocus on background, motion blur on rain, bloom and flare from the strongest light, light chroma, filmic, vignette, grain.
- **كيف / how:** Last steps of build(): [defocus..] mid-scene, then Step('الكاميرا', [bloom, flare, chroma, filmic, vignette, grain]) and ROLLOFF = 1.0.
- **أرقام / params:** AI recipe: defocus(2); motion_blur(shape,6,104); bloom(.72,26,.5); flare((x,y),'#ffb070',110,380,.45); chroma(1.4); filmic(1.0,1.08,1.02); vignette(.55); grain(.018)
- **الدليل / proof:** `kosif-studio/references/drawing-guide.md:62` · `kosif-studio/studio.py:55` · `kosif-studio/scenes/whale_dragon.py:287`

#### CAM-55 · أشرطة السينما 16:9 · Cinema letterbox 16:9 · 🟢 جاهز
- **ماذا / what:** Black bars top and bottom turn the 1200x800 sheet into a 1200x676 cinematic frame.
- **كيف / how:** Final Step with fill(rect(0,0,1200,TOP),'#000000') and fill(rect(0,BOTTOM,1200,800-BOTTOM),'#000000').
- **أرقام / params:** TOP 62, BOTTOM 738
- **الدليل / proof:** `kosif-studio/scenes/whale_dragon.py:294` · `kosif-studio/scenes/duck_dragon.py:17`

#### CAM-56 · العمق الجوي وضباب الوادي · Atmospheric depth veil and valley fog · 🟢 جاهز
- **ماذا / what:** Distant layers are lowered in contrast and pushed blue by translucent blurred screen bands; valley fog sits between mountain layers.
- **كيف / how:** fill(rect(...), colour, .2-.3, blur=26-34, mode='screen') between depth layers.
- **أرقام / params:** dragon fog #a86484 .26 blur 26 and #5c3550 .30 blur 30; whale horizon #54637a .2 blur 34
- **الدليل / proof:** `kosif-studio/scenes/dragon_girl.py:195` · `kosif-studio/scenes/whale_dragon.py:93` · `kosif-studio/references/drawing-guide.md:62`

#### CAM-57 · ضربة تكبير على النبضة · Zoom punch on downbeats · 🟢 جاهز
- **ماذا / what:** A hit-like zoom: the shot jumps to +9 % scale on a downbeat and decays exponentially; rendered at 2× so the zoom moves in half-pixel steps.
- **كيف / how:** montage._segment with punches; disable with --no-punch
- **أرقام / params:** 0.09·exp(−(t−p)/0.32)·[t≥p]; render 2W×2H then lanczos down; crf 17
- **الدليل / proof:** `kosif-studio/motion/montage.py:136`

#### CAM-58 · إعادة التأطير الذكي · Smart reframe (face / motion / blur pad) · 🟢 جاهز
- **ماذا / what:** Converts aspect ratio by cropping around detected faces (weighted by face size), else around the centroid of motion energy; or fits the whole frame over a blurred darker copy.
- **كيف / how:** python tools.py aspect CLIP --to 9:16 --mode smart|crop|blur --out v.mp4 [--size WxH]
- **أرقام / params:** Haar frontal face scale 1.15 minNeighbors 5 minSize 28 on 24 samples at 480 px; motion centroid 160 px; blur bg gblur σ 40, brightness −0.12, saturation 0.85
- **الدليل / proof:** `kosif-studio/motion/tools.py:158` · `kosif-studio/motion/tools.py:186` · `kosif-studio/motion/tools.py:219`

#### CAM-59 · طبقات عمق بتتبع المؤشر · Mouse-parallax depth layers · 📦 بأمر تثبيت
- **ماذا / what:** Three layers drift by different multipliers of a normalized pointer position with a lagging tween, creating a looking-through-a-window depth.
- **كيف / how:** Normalize pointer to -1..1; gsap.to(layer,{x:x*k,y:y*k2,duration:0.8}). For video, replace pointer with a scripted path or slow Lissajous so it renders deterministically.
- **أرقام / params:** back 45/22px; mid 22/11px; content 8/5px; lag 0.8s (0.3 too reactive, 1.2+ laggy); disable when (hover: none)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/196-landing/621-landing/references/gsap_animation_patterns.md`

#### CAM-60 · بارالاكس مرتبط بالتمرير ومشاهد مثبتة · Scroll-scrubbed parallax and pinned acts · 📦 بأمر تثبيت
- **ماذا / what:** Background moves slower than foreground while scrolling; a section pins while its internal timeline plays, then releases; horizontal galleries translate while the page scrolls vertically.
- **كيف / how:** GSAP ScrollTrigger: bg yPercent -30 with scrub:true from 'top bottom' to 'bottom top'; pin section with end '+=200%' scrub 1; horizontal track xPercent -100*(n-1) pinned. For video renders, tween window.scrollTo deterministically per frame instead of real scrolling.
- **أرقام / params:** yPercent -30; pin end +=200%; scrub 1; horizontal end = track width
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md` · `kosif-atlas/skills/3529-ui-design/14308-interaction-design/references/scroll-animations.md` · `kosif-atlas/skills/880-superloopy/1941-superloopy-frontend/references/motion.md`

#### CAM-61 · رصّ البطاقات المثبتة أثناء التمرير · Sticky scroll-stack of cards · 📦 بأمر تثبيت
- **ماذا / what:** Each card pins at the top while the next slides over it; the covered card shrinks and dims, producing a deck being stacked.
- **كيف / how:** ScrollTrigger pin each card except the last (pinSpacing false) and scrub scale/opacity as the next card travels from bottom to top; gate inside gsap.matchMedia for wide screens and motion allowed.
- **أرقام / params:** covered card scale 0.92, opacity 0.55; cards min-height 70dvh; breakpoint example 1024px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/880-superloopy/1941-superloopy-frontend/references/motion.md`

#### CAM-62 · قصة تمرير بصورة مثبتة · Sticky-graphic scroll story · 📦 بأمر تثبيت
- **ماذا / what:** A pinned visual on one side swaps or interpolates frames as text steps scroll past on the other side.
- **كيف / how:** ScrollTrigger per step start 'top 58%' end 'bottom 42%' calling show(index); pin visual from 'top top+=96'; frames autoAlpha with slight scale. Default CSS shows all steps stacked (fallback).
- **أرقام / params:** frame scale 0.985->1; step trigger top 58% / bottom 42%; pin offset 96px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/examples/motion/scroll-story.ts` · `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali`

#### CAM-63 · كشف بطاقات بميلان ثلاثي · Card batch reveal with 3D tilt-up · 📦 بأمر تثبيت
- **ماذا / what:** Feature cards flip up slightly in 3D as they arrive in sequence.
- **كيف / how:** gsap.set cards {opacity:0,y:55,rotateX:18}; ScrollTrigger.batch start 'top 80%' -> to {opacity:1,y:0,rotateX:0}.
- **أرقام / params:** rotateX 18deg (8 invisible, 30+ gimmicky); stagger 0.11; 0.8s power2.out
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/196-landing/621-landing/references/gsap_animation_patterns.md`

#### CAM-64 · عمق الميدان / بوكيه · Depth of field (TSL dof) · 📦 بأمر تثبيت
- **ماذا / what:** Focus pull and bokeh blur from view depth.
- **كيف / how:** dof(colorNode, viewZNode, focusDistance, focalLength, bokehScale); animate focusDistance for rack focus.
- **أرقام / params:** e.g. 5.0, 25.0, 1.0; API reimplemented in r181 (old options object broken)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/post-processing.md`

#### CAM-65 · معرض WebGL مدفوع بالزمن · Scroll/time-driven WebGL gallery · 📦 بأمر تثبيت
- **ماذا / what:** Image planes in 3D with velocity-reactive shader distortion; in video, drive by timeline progress instead of scroll.
- **كيف / how:** GSAP timeline progress -> uniform uVelocity bending planes.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### CAM-66 · حالات كاميرا مسماة · Named camera states · 📦 بأمر تثبيت
- **ماذا / what:** Define first/final frames and named camera states; interpolate shortest path between them.
- **كيف / how:** Store {position,target,fov} keyframes; GSAP tween camera + controls.target; slerp for globes.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/SKILL.md`

#### CAM-67 · نص يتفادى العناصر · Obstacle-aware type layout · 📦 بأمر تثبيت
- **ماذا / what:** Kinetic letters treat copy blocks/buttons as obstacles and flow around them.
- **كيف / how:** Static Matter.js bodies for overlay rectangles; letters collide around them.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/100-ui-motion/209-kinetic-inflated-hero/SKILL.md`

#### CAM-68 · تصميم حركة الكاميرا مع المسار · Route camera choreography · 📦 بأمر تثبيت
- **ماذا / what:** Camera follows the drawing head and breathes out in the middle of a long route, then dives back in at the destination.
- **كيف / how:** Keep route progress and camera progress separate. Mapbox: jumpTo({center: point along route, zoom, bearing, pitch}) with keyframes zoom 7 -> 2.4 -> 8, bearing -20 -> 35, pitch 25 -> 55 -> 55 -> 30, all on bezier(0.645,0.045,0.355,1). MapLibre: calculateCameraOptionsFromTo(cameraLngLat, altitude, targetLngLat) with a separate camera route; altitude 180 km -> 2,200 km -> 180 km and latitude offset 1.1 -> 8 -> 1.1 deg at timeline points 0, .28, .74, 1.
- **أرقام / params:** zoom 7/2.4/8; bearing -20..35; pitch 25/55/55/30; altitude 180000/2200000/180000 m
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/TECHNIQUE.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maplibre/TECHNIQUE.md`

#### CAM-69 · أنماط الزووم · Zoom modes (punch, Ken Burns, drift, pulse) · 📦 بأمر تثبيت
- **ماذا / what:** Per-shot zoom behaviours applied to footage between cuts.
- **كيف / how:** zoomState(): punch alternates 1 and 1+amount each cut (ease-out 0.18 s, 0.5 s in calm mode); kenburns linear 1->1+amount over the shot; drift scale 1+0.7a with lateral travel +-0.3a W alternating direction; pulse 1+a*exp(-t/0.32) after each cut; none.
- **أرقام / params:** amount 0-0.3; every 0.6-8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:191` · `app/index.html:316`

#### CAM-70 · حركات الكاميرا السينمائية · Cinematic camera moves (19) · 📦 بأمر تثبيت
- **ماذا / what:** Nineteen parametric virtual camera moves on footage: base moves per shot multiplied by short accents plus handheld noise.
- **كيف / how:** CAM.MOVES {z:[from,to], x/y travel as share of zoom room, r degrees, blur px@1080, shake, ease, snap}: push_in z1->1.15 sine; pull_out 1.2->1; slow_zoom 1->1.06 linear; punch_in 1->1.18 cubic snap 0.16 s shake .05; whip_pan z1.12 x 1->-1 expo blur 10; pan z1.15 x .8->-.8; tilt y .8->-.8; truck z1.2 x -.9->.9 linear; dolly_zoom 1->1.3 quad blur 0->1.5; orbit 1.12->1.18 x +-.5 r -3->3; crane_up 1.2->1.05 y .7->-.6 cubic; handheld 1.06 shake .3; locked_off; rack_focus 1->1.03 blur 8->0; dutch_tilt …
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:1087` · `app/public/js/10_studio.js:1114`

#### CAM-71 · قاعدة تغطية الدوران · Rotation coverage rule · 📦 بأمر تثبيت
- **ماذا / what:** When the camera rolls, zoom is raised enough that no black corners appear.
- **كيف / how:** CAM.at: need = |cos r| + q*|sin r|*0.56 with q = long/short side; z = max(z, need). Same formula in the Python fingerprint camera_chain.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:1129` · `app/public/js/10_studio.js:1726`

#### CAM-72 · تخطيط الكاميرا حسب المود · Mood-based camera planner · 📦 بأمر تثبيت
- **ماذا / what:** Plans a camera move per shot from the cuts, the mood and the loudest spoken words.
- **كيف / how:** CAM.plan({mood}): pools talk/music/hype/cinematic/photo/screen (long shots >1.6 s vs short); first shot push_in (photo: ken_burns) + punch accent 0.55; last shot pull_out; music/hype punch every 2nd cut; cinematic rack_focus on 35% of long shots; loud peaks get punch_in (max ~1 per 4 s, >= 2.5 s apart, not within 0.35 s of a cut); score>9 in music/hype -> crash_zoom at most once per 12 s; never the same move twice in a row.
- **أرقام / params:** moods: talk|music|hype|cinematic|photo|screen
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:1144` · `app/public/js/10_studio.js:1152`

#### CAM-73 · عرض الفيديو كامل بخلفية ضبابية · Fit vs cover framing with blurred fill · 📦 بأمر تثبيت
- **ماذا / what:** Footage whose aspect differs can fill the frame (crop) or sit whole over a blurred, darkened copy of itself.
- **كيف / how:** frame 'fit': background copy blur 4.5% W, brightness .88, saturate .85, scale 1.14; foreground contain-fit times zoom; coach suggests fit when cover crops > 40%.
- **أرقام / params:** cover|fit
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:275` · `app/public/js/00_editor.js:2769`

#### CAM-74 · شرايط السينما · Cinema letterbox bars · 📦 بأمر تثبيت
- **ماذا / what:** Black bars top and bottom for a widescreen look.
- **كيف / how:** fx.letterbox: bar height 10.5% H in landscape, 7% in portrait; captions move up to 72% H.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:294`

#### CAM-75 · نافذة صغيرة فوق الفيديو · Picture-in-picture inserts · 📦 بأمر تثبيت
- **ماذا / what:** Video or image tracks can play as a rounded window in the top corner that springs in.
- **كيف / how:** drawPips(): width 42% short side, aspect clamped 0.56-1.4, x = W-w-5% m, y = 9% H, spring(l) scale-in, accent 5 px frame, shadow 3% m, 0.2 s fade out.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:305`

#### CAM-76 · نقل لغة كاميرا المرجع · Reference camera language transfer · 📦 بأمر تثبيت
- **ماذا / what:** Maps the reference's measured camera moves onto the product's own cuts in the same order, plus punch accents at the reference's accent rate.
- **كيف / how:** DNA.cameraFor(dna,cuts,D): cycles reference moves per shot; accents every 1/rate s (min 1.5 s gap); if < 3 measured moves, plans by mood and keeps the dominant move.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:1402`

#### CAM-77 · اهتزاز الكاميرا · Camera Shake · 📦 بأمر تثبيت
- **ماذا / what:** Closed-form, seek-safe camera shake for any wrapper using value-noise channels over three octaves with per-lens projection (28/50/85 mm).
- **كيف / how:** Install with `npx hyperframes add camera-shake` (copies to compositions/components/camera-shake.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fram…
- **أرقام / params:** 9 profiles: handheld-normal-mild|handheld-normal-strong|handheld-normal-extreme|handheld-wideangle-mild|handheld-wideangle-strong|handheld-tele-mild|handheld-tele-strong|rig-6d-shake|rig-6d-wobble; mild octave rot amps 7/5 deg @0.15/0.1 Hz, 4/2 @0.8/0.75, 1/0.8 @1.2/1.5; intensity 0-3, frequency 0.1…
- **تثبيت / install:** `npx hyperframes add camera-shake` (copies to compositions/components/camera-shake`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/camera-shake/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/camera-shake/camera-shake.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/camera-shake.mdx`

#### CAM-78 · تكبير يتبع النقرات · Zoom Follow Cursor · 📦 بأمر تثبيت
- **ماذا / what:** Screen-recording auto-zoom: camera pushes toward each upcoming click, follows the cursor on a spring, marks clicks with press+ring, and eases back out.
- **كيف / how:** Install with `npx hyperframes add cursor-zoom-follow` (copies to compositions/components/cursor-zoom-follow.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless C…
- **أرقام / params:** zoom 1.8; three click points in %; vars: image=; zoom=1.8(1.2..2.6); click1_x=68.5(0..100); click1_y=7.5(0..100); click2_x=50(0..100); click2_y=48.5(0..100); click3_x=90.5(0..100); click3_y=7.5(0..100); accent=#0a84ff
- **تثبيت / install:** `npx hyperframes add cursor-zoom-follow` (copies to compositions/components/cursor-zoom-follow`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/cursor-zoom-follow/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/cursor-zoom-follow/cursor-zoom-follow.html` · `kosif-one/vendor/hyperframes/registry/components/cursor-zoom-follow/demo.html`

#### CAM-79 · ثبات حي · Drift Hold · 📦 بأمر تثبيت
- **ماذا / what:** Centred card stays subtly alive with loop-exact rotation, scale breathing and a slow light sweep.
- **كيف / how:** Install with `npx hyperframes add drift-hold` (copies to compositions/components/drift-hold.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame ca…
- **أرقام / params:** intensity whisper|standard; vars: text=Always alive; intensity=standard[whisper|standard]
- **تثبيت / install:** `npx hyperframes add drift-hold` (copies to compositions/components/drift-hold`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/drift-hold/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/drift-hold/drift-hold.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/drift-hold.mdx`

#### CAM-80 · نقل التركيز · Focus Rack · 📦 بأمر تثبيت
- **ماذا / what:** Focus moves once between two cards at different apparent depths using synced blur, dimming, scale and parallax.
- **كيف / how:** Install with `npx hyperframes add focus-rack` (copies to compositions/components/focus-rack.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame ca…
- **أرقام / params:** labels Draft/Published; vars: label_a=Draft; label_b=Published; accent=blue[green|blue|violet]
- **تثبيت / install:** `npx hyperframes add focus-rack` (copies to compositions/components/focus-rack`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/focus-rack/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/focus-rack/focus-rack.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/focus-rack.mdx`

#### CAM-81 · بانوراما المحطات · Pan Stations · 📦 بأمر تثبيت
- **ماذا / what:** Lateral camera move across a row of labelled stations with a steady dwell at each stop; centring logic is unit-tested.
- **كيف / how:** Install with `npx hyperframes add pan-stations` (copies to compositions/components/pan-stations.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fram…
- **أرقام / params:** stationCount 4; dwell 0.6 s; widths in cqw; vars: stationCount=4(3..6); labels=Capture,Edit,Render,Share; dwell=0.6(0.2..2)
- **تثبيت / install:** `npx hyperframes add pan-stations` (copies to compositions/components/pan-stations`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/pan-stations/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/pan-stations/pan-stations.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/pan-stations.mdx`

#### CAM-82 · الغوص في الجهاز · Parallax Device Dive · 📦 بأمر تثبيت
- **ماذا / what:** Phone rises, camera pushes through its screen and layered app UI expands to fill frame.
- **كيف / how:** Install with `npx hyperframes add parallax-device-dive` (copies to compositions/components/parallax-device-dive.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headle…
- **أرقام / params:** vars: accent=blue[green|blue|violet]; app_title=Dashboard
- **تثبيت / install:** `npx hyperframes add parallax-device-dive` (copies to compositions/components/parallax-device-dive`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/parallax-device-dive/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/parallax-device-dive/parallax-device-dive.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/parallax-device-dive.mdx`

#### CAM-83 · تصغير بارالاكس · Parallax Unzoom · 📦 بأمر تثبيت
- **ماذا / what:** Focus card shrinks from full frame while siblings parallax in to form a grid.
- **كيف / how:** Install with `npx hyperframes add parallax-unzoom` (copies to compositions/components/parallax-unzoom.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **تثبيت / install:** `npx hyperframes add parallax-unzoom` (copies to compositions/components/parallax-unzoom`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/parallax-unzoom/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/parallax-unzoom/parallax-unzoom.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/parallax-unzoom.mdx`

#### CAM-84 · تكبير بارالاكس · Parallax Zoom · 📦 بأمر تثبيت
- **ماذا / what:** Centre card scales to fill frame while siblings parallax outward.
- **كيف / how:** Install with `npx hyperframes add parallax-zoom` (copies to compositions/components/parallax-zoom.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fr…
- **تثبيت / install:** `npx hyperframes add parallax-zoom` (copies to compositions/components/parallax-zoom`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/parallax-zoom/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/parallax-zoom/parallax-zoom.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/parallax-zoom.mdx`

#### CAM-85 · كشف بالتراجع · Pull Back Reveal · 📦 بأمر تثبيت
- **ماذا / what:** Tight detail (e.g. +312%) holds, then one decelerating pull-back reveals the headline and context cards.
- **كيف / how:** Install with `npx hyperframes add pull-back-reveal` (copies to compositions/components/pull-back-reveal.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chrom…
- **أرقام / params:** vars: detail_text=+312%; headline=Growth compounds; accent=green[green|blue|violet]
- **تثبيت / install:** `npx hyperframes add pull-back-reveal` (copies to compositions/components/pull-back-reveal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/pull-back-reveal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/pull-back-reveal/pull-back-reveal.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/pull-back-reveal.mdx`

#### CAM-86 · دفع الكاميرا · Push In · 📦 بأمر تثبيت
- **ماذا / what:** One slow continuous camera push on a centred headline with gentle fade.
- **كيف / how:** Install with `npx hyperframes add push-in` (copies to compositions/components/push-in.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame capture …
- **أرقام / params:** intensity subtle|standard|bold; vars: text=Focus; intensity=standard[subtle|standard|bold]
- **تثبيت / install:** `npx hyperframes add push-in` (copies to compositions/components/push-in`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/push-in/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/push-in/push-in.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/push-in.mdx`

#### CAM-87 · قصة التمرير · Scroll Camera Story · 📦 بأمر تثبيت
- **ماذا / what:** Forced-scroll cinematic pass through a tall scene of slotted sections with depth-layer parallax, decelerating into the last section.
- **كيف / how:** Install with `npx hyperframes add scroll-camera-story` (copies to compositions/components/scroll-camera-story.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless…
- **أرقام / params:** sections 3; travel 220; vars: sections=3(2..4); travel=220(100..400); cues=; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add scroll-camera-story` (copies to compositions/components/scroll-camera-story`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/scroll-camera-story/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/scroll-camera-story/scroll-camera-story.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/scroll-camera-story.mdx`

#### CAM-88 · تكبير على الواجهة · UI Focus Zoom · 📦 بأمر تثبيت
- **ماذا / what:** App surface settles, then camera zooms/pans to an anchor on cue and holds, optional soft halo.
- **كيف / how:** Install with `npx hyperframes add ui-focus-zoom` (copies to compositions/components/ui-focus-zoom.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fr…
- **أرقام / params:** anchor 64,36 %; zoom 1.6; zoom_at 1.4 s; vars: anchor_x=64(0..100); anchor_y=36(0..100); zoom=1.6(1..3); zoom_at=1.4(0..30); halo=show[show|hide]; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add ui-focus-zoom` (copies to compositions/components/ui-focus-zoom`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/ui-focus-zoom/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/ui-focus-zoom/ui-focus-zoom.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/ui-focus-zoom.mdx`

#### CAM-89 · حركات كاميرا يوتيوب · Camera Punch-In · 📦 بأمر تثبيت
- **ماذا / what:** Helpers for zoom, slide and 3D tilt-pan on any wrapper (video/include/card) with cubic defaults and edge-defocus pulse overlay.
- **كيف / how:** Install with `npx hyperframes add yt-camera-move` (copies to compositions/components/yt-camera-move.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium …
- **تثبيت / install:** `npx hyperframes add yt-camera-move` (copies to compositions/components/yt-camera-move`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/yt-camera-move/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/yt-camera-move/yt-camera-move.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/yt-camera-move.mdx`

#### CAM-90 · دوللي زووم (فيرتيغو) · Dolly Zoom (Vertigo Shot) · 📦 بأمر تثبيت
- **ماذا / what:** Dolly zoom: camera tracks while field of view solves d*tan(FOV/2)=const each frame so the subject keeps size while the background stretches or collapses; needs layered depth.
- **كيف / how:** Install with `npx hyperframes add camera-dolly-zoom` (copies the full composition to compositions/camera-dolly-zoom.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** direction out|in; strength 2; subjectDistance 1400; easing none|sine.inOut|power1.inOut|power2.inOut|power3.inOut; vars: direction=out[out|in]; strength=2(1.1..4); subjectDistance=1400(600..3000); easing=power2.inOut[none|sine.inOut|power1.inOut|power2.inOut|power3.inOut]; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add camera-dolly-zoom` (copies the full composition to compositions/camera-dolly-zoom`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/camera-dolly-zoom/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/camera-dolly-zoom/camera-dolly-zoom.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/camera-dolly-zoom.mdx`

#### CAM-91 · نقل البؤرة بالبوكيه · Rack Focus · 📦 بأمر تثبيت
- **ماذا / what:** WebGL focus pull with real aperture bokeh: polygon discs that clip to cat-eye toward the corners as the focal plane travels near to far.
- **كيف / how:** Install with `npx hyperframes add rack-focus` (copies the full composition to compositions/rack-focus.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGL fragment shader, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** nearfocus 1.2; farfocus 80; focallength 85; aperture 1.8; blades 6; catseye 0.62; pullstart 1.2; pullduration 3.2; power2.inOut; vars: nearfocus=1.2(0.2..100); farfocus=80(0.3..400); focallength=85(12..300); aperture=1.8(0.95..22); blades=6(3..14); catseye=0.62(0..1); pullstart=1.2(0..30); pulldurat…
- **تثبيت / install:** `npx hyperframes add rack-focus` (copies the full composition to compositions/rack-focus`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/rack-focus/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/rack-focus/rack-focus.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/rack-focus.mdx`

#### CAM-92 · دوار دائري · Carousel circle (styles 1-5) · 📦 بأمر تثبيت
- **ماذا / what:** Image cards ride a circle with size graded by depth angle, sweeping in fast-slow-fast swings; 12 image slots. Five style variants (1-5).
- **كيف / how:** Install `npx hyperframes add carousel-circle-<1..5>`; replace image1..imageN variables with your own image paths (the shipped sample photos are absent locally); 1920x1080, ~6 s; GSAP-driven 3D transforms.
- **أرقام / params:** carousel-circle-1: 12 slots; carousel-circle-2: 12 slots; carousel-circle-3: 12 slots; carousel-circle-4: 12 slots; carousel-circle-5: 12 slots; duration 6 s
- **تثبيت / install:** `npx hyperframes add carousel-circle-<1`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/carousel-circle-1/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/carousel-circle-2/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/carousel-circle-3/registry-item.json`

#### CAM-93 · دوار كروي · Carousel orbit (styles 1-5) · 📦 بأمر تثبيت
- **ماذا / what:** Image cards on a spinning 3D Fibonacci sphere, billboarded to camera and sized by distance; 24 slots. Five style variants (1-5).
- **كيف / how:** Install `npx hyperframes add carousel-orbit-<1..5>`; replace image1..imageN variables with your own image paths (the shipped sample photos are absent locally); 1920x1080, ~6 s; GSAP-driven 3D transforms.
- **أرقام / params:** carousel-orbit-1: 24 slots; carousel-orbit-2: 24 slots; carousel-orbit-3: 24 slots; carousel-orbit-4: 24 slots; carousel-orbit-5: 24 slots; duration 6 s
- **تثبيت / install:** `npx hyperframes add carousel-orbit-<1`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/carousel-orbit-1/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/carousel-orbit-2/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/carousel-orbit-3/registry-item.json`

#### CAM-94 · دوار على مسار · Carousel path (styles 1-5) · 📦 بأمر تثبيت
- **ماذا / what:** Image cards ride an open bezier path (arc, V, diagonal, wave, S-curve) with depth scaling and tangent rotation; 12-24 slots. Five style variants (1-5).
- **كيف / how:** Install `npx hyperframes add carousel-path-<1..5>`; replace image1..imageN variables with your own image paths (the shipped sample photos are absent locally); 1920x1080, ~6 s; GSAP-driven 3D transforms.
- **أرقام / params:** carousel-path-1: 24 slots; carousel-path-2: 12 slots; carousel-path-3: 12 slots; carousel-path-4: 24 slots; carousel-path-5: 24 slots; duration 6 s
- **تثبيت / install:** `npx hyperframes add carousel-path-<1`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/carousel-path-1/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/carousel-path-2/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/carousel-path-3/registry-item.json`

#### CAM-95 · عنوان مع دوار دائري · Carousel text-circle (styles 1-5) · 📦 بأمر تثبيت
- **ماذا / what:** Headline mask-reveals per word while a circle carousel converges from off-frame, threads the line, collapses to centre and hard-cuts to a second line at 1.4x. Five style variants (1-5).
- **كيف / how:** Install `npx hyperframes add carousel-text-circle-<1..5>`; replace image1..imageN variables with your own image paths (the shipped sample photos are absent locally); 1920x1080, ~6 s; GSAP-driven 3D transforms.
- **أرقام / params:** carousel-text-circle-1: 12 slots; carousel-text-circle-2: 12 slots; carousel-text-circle-3: 12 slots; carousel-text-circle-4: 12 slots; carousel-text-circle-5: 12 slots; duration 5 s
- **تثبيت / install:** `npx hyperframes add carousel-text-circle-<1`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/carousel-text-circle-1/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/carousel-text-circle-2/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/carousel-text-circle-3/registry-item.json`

#### CAM-96 · دوار الرؤية · Carousel vision (styles 1-5) · 📦 بأمر تثبيت
- **ماذا / what:** Ring of large image cards tilted into a row under a 3D camera, each turning toward centre; 12 slots. Five style variants (1-5).
- **كيف / how:** Install `npx hyperframes add carousel-vision-<1..5>`; replace image1..imageN variables with your own image paths (the shipped sample photos are absent locally); 1920x1080, ~6 s; GSAP-driven 3D transforms.
- **أرقام / params:** carousel-vision-1: 12 slots; carousel-vision-2: 12 slots; carousel-vision-3: 12 slots; carousel-vision-4: 12 slots; carousel-vision-5: 12 slots; duration 6 s
- **تثبيت / install:** `npx hyperframes add carousel-vision-<1`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/carousel-vision-1/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/carousel-vision-2/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/carousel-vision-3/registry-item.json`

#### CAM-97 · الشبكة السويسرية · Example project: swiss-grid · 📦 بأمر تثبيت
- **ماذا / what:** Structured Swiss-grid layout example in Helvetica on #f2f2f2 (10 s). [Local copy lacks its sub-compositions: compositions/captions.html, compositions/graphics.html, compositions/intro.html.]
- **كيف / how:** Starter project: `npx hyperframes init --example swiss-grid` style scaffold (index.html mounts sub-compositions via data-composition-src); reuse its palette/type as a style reference.
- **أرقام / params:** 1920x1080; 10 s
- **تثبيت / install:** `npx hyperframes init --example swiss-grid` style scaffold (index`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/examples/swiss-grid/registry-item.json` · `kosif-one/vendor/hyperframes/registry/examples/swiss-grid/index.html`

#### CAM-98 · منطقة حجز الترجمة أسفل الإطار · Caption keep-out zone (bottom ~17%) · 📦 بأمر تثبيت
- **ماذا / what:** All frame content stays in the top ~83% of the canvas because a karaoke caption pill owns the bottom ~17%, even when captions are disabled.
- **كيف / how:** Compute cutoff y <= 0.83 x height (<=900 px on 1080 tall, <=1600 px on 1920 tall); anchor the portrait hero at 0.2-0.35 x height; landscape centers near 0.42 x height.
- **أرقام / params:** 0.83 x H; 900px@1080; 1600px@1920
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/frame-worker-core.md`

#### CAM-99 · تقريب مفاجئ على اللقطة · Punch-in zoom on footage · 📦 بأمر تثبيت
- **ماذا / what:** Zoom/punch animates the inner wrapper of a clip, never the timed clip element.
- **كيف / how:** tl.to('#clip .inner',{scale:1.35,xPercent:-8,duration:0.18},1).
- **أرقام / params:** scale 1.35, 0.18 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/creator-editing-recipes.md`

#### CAM-100 · حركة كين بيرنز · Ken Burns pan on stills/footage · 📦 بأمر تثبيت
- **ماذا / what:** Slow scale + translate drift across an image or clip.
- **كيف / how:** tl.fromTo('#clip .inner',{scale:1.05,xPercent:0},{scale:1.2,xPercent:-12,duration:4,ease:'none'},0).
- **أرقام / params:** scale 1.05->1.2, xPercent 0->-12, 4 s linear
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/creator-editing-recipes.md`

#### CAM-101 · إعادة التأطير بالقص · Crop / reframe with clip-path inset · 📦 بأمر تثبيت
- **ماذا / what:** Reframe a clip by tweening clipPath inset and offset on the inner wrapper.
- **كيف / how:** tl.to('#clip .inner',{clipPath:'inset(8% 12% 6% 10%)',xPercent:-4,duration:1},2).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/creator-editing-recipes.md`

#### CAM-102 · حركة ملء الشاشة بخلفيات مشتركة · Full-screen motion with shared backgrounds · 📦 بأمر تثبيت
- **ماذا / what:** Pattern for full-frame motion where a persistent background layer spans scenes while foreground scenes swap.
- **كيف / how:** full-screen-motion.md pattern + rules; on shader/HDR layered-composite path put fills on a full-bleed child, not the root.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/full-screen-motion.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-core/SKILL.md`

#### CAM-103 · تقريب إلى هدف غير مركزي · Coordinate target zoom · 📦 بأمر تثبيت
- **ماذا / what:** Zoom onto a non-centered element: outer wrapper scales around 50% 50%, inner wrapper counter-translates (T = -offset).
- **كيف / how:** Read hyperframes-animation/rules/coordinate-target-zoom.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** await document.fonts.ready before measuring; keep target <= ~88% of canvas at peak
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/coordinate-target-zoom.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### CAM-104 · كاميرا تتبع مؤشر الكتابة · Camera tracks typing cursor · 📦 بأمر تثبيت
- **ماذا / what:** Two-phase virtual camera: static framing, then the world translates to keep a moving typing caret locked in view.
- **كيف / how:** Read hyperframes-animation/rules/camera-cursor-tracking.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** track ease power2.inOut; blink ease steps(1) yoyo; VIEWPORT_PAD_LEFT 0-~10% must match CSS padding
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/camera-cursor-tracking.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### CAM-105 · كاميرا متعددة المراحل مع انجراف · Multi-phase camera push/pull with drift · 📦 بأمر تثبيت
- **ماذا / what:** Sequential zoom phases (pull-back / focus / push) plus continuous micro-drift spanning the composition; patterns like bookend pull.
- **كيف / how:** Read hyperframes-animation/rules/multi-phase-camera.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** off-center transform-origin creates phase drift; drift tween ease none over TOTAL_DURATION
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/multi-phase-camera.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### CAM-106 · كاميرا افتراضية بتحريك العالم · Virtual camera via .world wrapper · 📦 بأمر تثبيت
- **ماذا / what:** Simulate zoom/pan/focus-lock by transforming one .world wrapper with translate(x,y) scale(S); counter-translate T = -offset x S.
- **كيف / how:** Read hyperframes-animation/rules/viewport-change.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** <5% scale imperceptible; 10-15% comfortable; >30% dramatic; product feel 1.05-1.15x over 2-3 s; ease power3.inOut
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/viewport-change.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### CAM-107 · عمق الميدان وسحب التركيز · Depth-of-field rack focus · 📦 بأمر تثبيت
- **ماذا / what:** Blur (and slight dim) off-focus layers through a --dof variable while the focal element stays sharp: single pull, two-plane rack, or blur-the-cluster while pushing in.
- **كيف / how:** Read hyperframes-animation/rules/depth-of-field-blur.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** filter: blur(var(--dof)); FOCUS_DUR window
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/depth-of-field-blur.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### CAM-108 · انتشار من المركز إلى الخارج · Center-outward expansion · 📦 بأمر تثبيت
- **ماذا / what:** Elements start clustered at center and expand to CSS-authored target positions in lockstep with one driver (x = targetX x progress).
- **كيف / how:** Read hyperframes-animation/rules/center-outward-expansion.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** xPercent/yPercent -50 bakes centering; data-target-x/y per element
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/center-outward-expansion.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### CAM-109 · بطاقتان مائلتان متقابلتان · Split tilt cards · 📦 بأمر تثبيت
- **ماذا / what:** Two cards side by side with opposing rotateY tilts, sliding in from their sides, floating in phase opposition.
- **كيف / how:** Read hyperframes-animation/rules/split-tilt-cards.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** SCENE_PERSPECTIVE 1000-2400 px; entry power3.out; float sine.inOut yoyo; PI phase offset
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/split-tilt-cards.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### CAM-110 · مخطط مشهد: محطات على لوحة كبيرة تتنقل بينها الكاميرا · Blueprint: Spatial pan stations · 📦 بأمر تثبيت
- **ماذا / what:** Labeled stations on one oversized canvas traversed by one virtual camera with lateral/diagonal pans, landing on the last.
- **كيف / how:** Pick from hyperframes-animation/blueprints-index.md by role, then read hyperframes-animation/blueprints/spatial-pan-stations.md for the multi-phase recipe; cite blueprint id per beat in the storyboard.
- **أرقام / params:** duration 7-10 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/spatial-pan-stations.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`

#### CAM-111 · مخطط مشهد: رحلة الكاميرا · Blueprint: Camera journey · 📦 بأمر تثبيت
- **ماذا / what:** A multi-leg motivated camera journey across one world: action roundtrip (dive, click fires, swoop to consequence) or cursorless cinematic 3D flight with motion blur and DoF.
- **كيف / how:** Pick from hyperframes-animation/blueprints-index.md by role, then read hyperframes-animation/blueprints/camera-journey.md for the multi-phase recipe; cite blueprint id per beat in the storyboard.
- **أرقام / params:** duration 5.6-11.1 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/camera-journey.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`

#### CAM-112 · مخطط مشهد: كشف بالتبعيد عن مساحة العمل · Blueprint: Zoom-out workspace reveal · 📦 بأمر تثبيت
- **ماذا / what:** Open tight on a detail, micro-action in close-up, then one continuous decelerating zoom-out reveals the whole workspace.
- **كيف / how:** Pick from hyperframes-animation/blueprints-index.md by role, then read hyperframes-animation/blueprints/zoom-out-workspace-reveal.md for the multi-phase recipe; cite blueprint id per beat in the storyboard.
- **أرقام / params:** duration 6.8-11 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/zoom-out-workspace-reveal.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`

#### CAM-113 · مخطط مشهد: تجميع شبكة البطاقات · Blueprint: Grid card assemble · 📦 بأمر تثبيت
- **ماذا / what:** N tiles/cards/logos self-assemble in a staggered cascade into a grid or list, optional zoom-out reveal.
- **كيف / how:** Pick from hyperframes-animation/blueprints-index.md by role, then read hyperframes-animation/blueprints/grid-card-assemble.md for the multi-phase recipe; cite blueprint id per beat in the storyboard.
- **أرقام / params:** duration 3.0-10.5 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/grid-card-assemble.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`

#### CAM-114 · مخطط مشهد: مقارنة منقسمة · Blueprint: Comparison split · 📦 بأمر تثبيت
- **ماذا / what:** Two equal items enter from opposite wings with mirrored 3D book-open tilts, then inner-edge pill badges spring-pop.
- **كيف / how:** Pick from hyperframes-animation/blueprints-index.md by role, then read hyperframes-animation/blueprints/comparison-split.md for the multi-phase recipe; cite blueprint id per beat in the storyboard.
- **أرقام / params:** duration 4-6 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/comparison-split.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`

#### CAM-115 · قواعد مقياس الفيديو · Video-scale composition rules · 📦 بأمر تثبيت
- **ماذا / what:** Web sizes vanish on video: headlines 64-120 px, body 28-42 px, labels 18-24 px, decorative opacity 12-25%, borders 2-4 px, padding 60-140 px; 6-10 visual roles for produced marketing frames; no full-screen linear gradients on dark (H.264 banding).
- **كيف / how:** references/video-composition.md tables; plan background/midground/foreground roles.
- **أرقام / params:** headline 64-120px; body 28-42px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/video-composition.md`

#### CAM-116 · نمط صورة داخل صورة · Composition pattern: picture-in-picture · 📦 بأمر تثبيت
- **ماذا / what:** Video inside a framed window over a designed background.
- **كيف / how:** references/composition-patterns.md § Picture-in-Picture.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/composition-patterns.md`

#### CAM-117 · بطاقة عنوان وعرض شرائح · Composition pattern: title card fade / slideshow with section headers · 📦 بأمر تثبيت
- **ماذا / what:** Simple title card with fade and a slide show with section headers + top-level composition example.
- **كيف / how:** references/composition-patterns.md.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/composition-patterns.md`

#### CAM-118 · المناطق الآمنة للبث · Broadcast safe zones · 📦 بأمر تثبيت
- **ماذا / what:** Action-safe 90% of frame (5% inset each edge); title-safe 80% (10% inset).
- **كيف / how:** hyperframes-studio SKILL §4.
- **أرقام / params:** action 5% / title 10% inset
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-studio/SKILL.md`

#### CAM-119 · حساب المناطق الآمنة من القناع · Safe zones from subject matte · 📦 بأمر تثبيت
- **ماذا / what:** Precomputes where captions can go (global + per-sentence windows) plus scene palette, optics and lighting from the matte.
- **كيف / how:** node scripts/safe-zones.cjs <project> -> safe-zones.json; read before authoring.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/safe-zones.cjs`

#### CAM-120 · أنواع المشاهد وقواعد تموضع الترجمة · Caption scene types and layout heuristics · 📦 بأمر تثبيت
- **ماذا / what:** wall-embed (text printed on a flat real surface, four conditions), corner-column-crown (clean region beside subject), portrait-header (subject fills center, top banner); pick the bigger clean zone, honor gaze 'looking room', avoid baked graphics.
- **كيف / how:** references/scene-types.md + layout-heuristics.md (sample 3 frames, find clean zone, choose side, place crown, validate).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/references/scene-types.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/references/layout-heuristics.md`

#### CAM-121 · تفاعلات اللوح: تعتيم وصدمة واهتزاز وحبيبات · Theme plate reactions (dim, punch, shake, grain) · 📦 بأمر تثبيت
- **ماذا / what:** Register-gated reaction beats applied to the footage after the matte composite so subject + text + plate move as one: charge-dim, punch zoom, screen shake, grain.
- **كيف / how:** theme.json plate {dim, charge, punch, punchDecay, punchOffset, shakeAmpX/Y, shakeHz, pushIn, grain, scrim}.
- **أرقام / params:** e.g. stomp punch 0.05, shake 8x5 px at 12 Hz; anchor dim 0.16 pushIn 0.012 grain 5
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/stomp.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/anchor.json` · `kosif-one/vendor/hyperframes/skills/embedded-captions/themes/README.md`

#### CAM-122 · مناطق البطاقات · Recut card zones · 📦 بأمر تثبيت
- **ماذا / what:** Five zones: fullscreen, whiteboard-area (40 px inset landscape / bottom 45% portrait), lower-third (bottom 30%), side-panel (right 42% / bottom 40% portrait), video-overlay (transparent card root).
- **كيف / how:** Declare card.zone in storyboard.json; resolve to pixels in the card-host style.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/talking-head-recut/SKILL.md`

#### CAM-123 · حركة إيقاعية: screen-shake · Beat motion primitive: screen-shake · 📦 بأمر تثبيت
- **ماذا / what:** Camera/screen shake jitter, anchored to music events (drop / crash / kick).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/screen-shake/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: drop / crash / kick; best span 0.1-0.5 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/screen-shake/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### CAM-124 · حركة إيقاعية: dolly-zoom · Beat motion primitive: dolly-zoom · 📦 بأمر تثبيت
- **ماذا / what:** Vertigo dolly zoom (scale vs perspective), anchored to music events (phrase / build).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/dolly-zoom/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: phrase / build; best span 1.2-2.5 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/dolly-zoom/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### CAM-125 · حركة إيقاعية: crash-zoom-in · Beat motion primitive: crash-zoom-in · 📦 بأمر تثبيت
- **ماذا / what:** Violent crash zoom-in, anchored to music events (drop / surge).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/crash-zoom-in/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: drop / surge; best span 0.2-0.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/crash-zoom-in/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### CAM-126 · حركة إيقاعية: mosaic-pack · Beat motion primitive: mosaic-pack · 📦 بأمر تثبيت
- **ماذا / what:** Scattered tiles fly in and pack into a grid, anchored to music events (beat / build).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/mosaic-pack/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: beat / build; best span 1.5-3.5 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/mosaic-pack/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### CAM-127 · حركة إيقاعية: tile-mosaic · Beat motion primitive: tile-mosaic · 📦 بأمر تثبيت
- **ماذا / what:** Diagonal tile sweep assembling a poster, anchored to music events (build / reveal).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/tile-mosaic/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: build / reveal; best span 1.5-3.5 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/tile-mosaic/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### CAM-128 · تكبير لوغاريتمي · Log-space zoom lmix/push/zoomTrack · 📦 بأمر تثبيت
- **ماذا / what:** Scale and zoom interpolated in log space.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** MOTION.lmix, MOTION.push, zoomTrack
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### CAM-129 · اهتزاز الكاميرا · shake · 📦 بأمر تثبيت
- **ماذا / what:** Decaying seeded camera hit.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** MOTION.shake
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### CAM-130 · البارالاكس · parallax · 📦 بأمر تثبيت
- **ماذا / what:** Layers moving by depth.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** MOTION.parallax
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### CAM-131 · تنفس اللقطة الثابتة · breathe holds · 📦 بأمر تثبيت
- **ماذا / what:** Holds stay alive with creep or drift; no handheld shake.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** creep ~4%/s or drift 0.3–2.5 px/f; MOTION.breathe
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### CAM-132 · مفردات اللقطات ككاميرات · Veo shot vocabulary as cameras · 📦 بأمر تثبيت
- **ماذا / what:** shot(kind) for establishing, wide, medium, closeup, extreme_closeup, low/high angle, birds_eye, dutch, tracking, crane_up/down, push_in, pull_back, orbit, arc, handheld(seeded), dolly_zoom, whip_pan, turntable; shotFromWords; sequence with hard cuts.
- **كيف / how:** three-kit.js (window.K3) in a --3d project; render --engine studio
- **أرقام / params:** dolly_zoom fov=2·atan(h/2d); handheld 3-octave seeded sway
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:106` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### CAM-133 · مسار الكاميرا المستمر · cameraPath Catmull-Rom · 📦 بأمر تثبيت
- **ماذا / what:** One continuous camera through keys without stops.
- **كيف / how:** three-kit.js (window.K3) in a --3d project; render --engine studio
- **أرقام / params:** centripetal Catmull-Rom
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:106` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### CAM-134 · كاميرا الدوران مع التوقفات · orbitWalk camera · 📦 بأمر تثبيت
- **ماذا / what:** Walks around target holding at each stop.
- **كيف / how:** shape-kit.js / lab-kit.js in a 3D project; read references/shape-kit.md
- **أرقام / params:** orbitWalk(camera,stops)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:101` · `100-superskills/skills/kosif-montage-motion/SKILL.md:113` · `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### CAM-135 · تظليل علوي لوضوح العنوان · Top shade for title legibility · 📦 بأمر تثبيت
- **ماذا / what:** A gradient shade over the top half fades in under the title and out after, so text never fights a bright sky.
- **كيف / how:** #shade linear-gradient(180deg, rgba(5,10,18,.55) 0% → .25 55% → 0 100%) height 48%; opacity 0→1 at 0.3 s (0.8 s), back to 0 before the action; koi end title uses radial #endshade ellipse 46%×30%.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/index.html:29` · `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/index.html:29`

#### CAM-136 · كاميرا ثنائية الأبعاد متزامنة مع الكلام · Word-synced 2D camera on a footage plate · 📦 بأمر تثبيت
- **ماذا / what:** One move per idea on a talking-head plate: slow eased pushes and lateral drifts between lines, quick expo punches on stressed words, with the transform origin on the subject's face.
- **كيف / how:** #cam transform-origin 705px 700px, start scale 1.10; to 1.035 (0.55 s expo.out) on hook release; 1.07 (1.7 s power2.inOut); x ±10–18 drifts; punches 1.12/1.16/1.19 in 0.12–0.14 s expo.out on محدش يقدر … إطلاقاً; build 1.22 power2.in then 1.30/1.35 punches; final 1.38 over 2 s.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:120`

#### CAM-137 · اهتزاز دقيق لأربعة إطارات · Seeded 4-frame micro shake · 📦 بأمر تثبيت
- **ماذا / what:** A tiny deterministic shake on the hardest word sells impact without randomness between renders.
- **كيف / how:** tl.set(cam, {x, y}) at 10.90 + d for [(0,6,−4), (1/30,−5,3), (2/30,3,−2), (3/30,0,0)] plus #dim .22 flash.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:141`

#### CAM-138 · دفع لوغاريتمي وثبات حي · Log-space push and living hold · 📦 بأمر تثبيت
- **ماذا / what:** Zooms ease in log space so the perceived speed is even; holds never freeze but creep slowly.
- **كيف / how:** M.push(tl, stage, at, from, to, dur, {ease:E.dolly}) → logEase; five_sec 1.0→1.09 over 2.4 s plus ring rotation 8° linear; M.breathe(tl, card, at, 2.6, {creep:.012}); showreel end push 1→1.045 over 2.6 s.
- **أرقام / params:** breathe default creep 4%/s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:74` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:118` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:316`

#### CAM-139 · مدار ثلاثي الأبعاد مع اقتراب واهتزاز · 3D orbit with push-in, break shake and pull-back · 📦 بأمر تثبيت
- **ماذا / what:** Around a small character the camera slowly orbits, pushes in on the weak part for the break, shakes with exponential decay at the snap, and pulls back for the ranking.
- **كيف / how:** ang = lerp(.42, −.3, easeInOut(t/5)) + .06·sin(.9t); push = smooth(load, brk+.1)·(1−smooth(swap+.3, rank+.4)); dist 1.95→1.8 (+.14 end pull); shake = exp(−9(t−T_BREAK))·.006 at sin(93t), cos(71t); fov 30.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:106`

#### CAM-140 · جولة كاميرا حول المشهد بتوقفات · Orbit walk with stops and holds · 📦 بأمر تثبيت
- **ماذا / what:** One lens walks the whole circle around two characters, stopping at parts (head, eye extreme close-up, mane, far side, tail) with holds, then returns to the wide.
- **كيف / how:** orbitWalk(camera, [{t, angle°, dist, height, look:[x,y,z]|joint, fov, hold}]): 0 s 28°/6.4 m/30°; 3 s −35°/2.3 m head hold 1.2; 6.5 s −5°/1.0 m eye fov 26; 9.5 s lion head; 13 s 175°/4.2 m; 16 s 300°/1.6 m tail; 18 s 388°/6.0 m.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/src/main.js:21`

#### CAM-141 · مفاتيح كاميرا هيرميت ووقت الرصاصة · Hermite camera keys with bullet time · 📦 بأمر تثبيت
- **ماذا / what:** A continuous take keyed on the music's bars with velocity-continuous Hermite interpolation; during a tape stop the world freezes while the camera keeps orbiting, then whips home; kicks add fov punches, shake and alternating roll.
- **كيف / how:** KEYS [t, angle, dist, height, lookX, lookY] ×14; tangents (k2−k0)/(t2−t0)·h; camera.fov = 36 + 3.5·kick − 2.5·smooth(STOP, FREEZE)·(1−smooth(START, HOME)); shake .05·kick seeded per frame; rotateZ(.026·kick·±1) after 7.9 s.
- **أرقام / params:** STOP 6.0, FREEZE 6.75, START 7.2, HOME 7.85
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:73` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:118`

#### CAM-142 · مسارات كاميرا بمفاتيح · Keyed camera paths (cameraPath / cameraKeys) · 📦 بأمر تثبيت
- **ماذا / what:** A list of [t, camera xyz, look-at xyz] keys yields one smooth move with no stops (koi) or slow moves with stillness between (water cycle), with fov changes for the storm.
- **كيف / how:** cameraPath([[0, 4.5,.42,2.3, −2.6,−.12,−1.6], [3.4,…], [6.6,…], [10,…]]); cameraKeys 7 keys over 17 s; fov 38 − 4·smooth(9.5,12.8) + 4·smooth(12.8,15.2); focus = |p−l|·0.9.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:93` · `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:51` · `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:91`

#### CAM-143 · دفع بطيء من مستوى الطريق · Road-level tripod push-in (Veo shot language) · 📦 بأمر تثبيت
- **ماذا / what:** Shot words like 'slow push-in, low angle, road-level' or 'orbit 10°' are translated into explicit camera math so AI-video vocabulary and code agree.
- **كيف / how:** blue_hour camAt(t): position (6.4−1.0e, 1.5+0.2e, 16−7e), look (−8, 26, −420), e = smooth(0,8,t), fov 32; night_boat: angle 132°−12°·e, radius 19−5.5r, height 1.55+.35e, fov 30.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:127` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:221`

#### CAM-144 · إسقاط نقطة ثلاثية على الشاشة لوسم · Project 3D point to screen for HUD callout · 📦 بأمر تثبيت
- **ماذا / what:** A 2D callout (leader line + label box) follows a 3D member exactly by projecting its midpoint with this frame's camera.
- **كيف / how:** camera.updateMatrixWorld(true); proj.copy(mid).project(camera); sx = (x·.5+.5)·W, sy = (−y·.5+.5)·H; tag translate(sx, sy); leader 150 px at −45°, box Mono 22 px; colour by state (broken #ff907a, fixed #9dffb4, ≥72% #ffe083).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:184` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:115`

#### CAM-145 · زووم كين بيرنز · Ken Burns raised-cosine zoom · 📦 بأمر تثبيت
- **ماذا / what:** Push eased by raised cosine rendered at 2x.
- **كيف / how:** clips[].zoom {from,to} 1-3
- **أرقام / params:** e.g. 1.0->1.08
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`

#### CAM-146 · كاميرا تقترب في قوس · Dolly-in arc camera (time-driven) · 📦 بأمر تثبيت
- **ماذا / what:** Camera circles a quarter turn while pushing in and gently rising and falling, always looking at the subject.
- **كيف / how:** cinematic_3d render(t): n=t/DUR; angle = n*PI*0.5 + 0.3; dist = 9.5 - 2.2n; x = sin(angle)*dist; z = cos(angle)*dist; y = sin(n*PI)*1.5 + 0.5; camera.lookAt(0,0,0); PerspectiveCamera FOV 45.
- **أرقام / params:** FOV 45 deg, distance 9.5 -> 7.3, orbit 90 deg over the clip, height bob 1.5
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:104` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:189`

#### CAM-147 · زووم نبضي لرفع الاحتفاظ · Retention zoom punches · 📦 بأمر تثبيت
- **ماذا / what:** Talking-head footage alternates between normal framing and a slight punch-in every few seconds to reset attention.
- **كيف / how:** Design rule 1.0x <-> 1.10-1.15x every 2.5-4 s on speech. smart_montage auto applies ffmpeg zoompan z=1.10 for 1.2 s on every 4th beat — but its expression uses 't' which zoompan does not define; replace with 'it' (in_time) or use crop+scale with enable='between(t,..)'.
- **أرقام / params:** scale 1.10-1.15, hold 1.0-1.5 s, every 2.5-4 s; code: every 4th beat, 1.2 s, output forced to 1080x1920@30
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/montage_grammar.md` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/smart_montage.py:188` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/montage_spec.json`

#### CAM-148 · حركات كاميرا بالمسارات · Spline camera flights and eased dollies · 📦 بأمر تثبيت
- **ماذا / what:** Each shot has one readable camera move: orbit dive with roll, slow push and crane at Giza, a drone track that follows the maglev, a CatmullRom flythrough rising to the tower, a low glide over water to the lighthouse, a pull back to orbit.
- **كيف / how:** cam.position = lerp(from,to,ease(seg(t,a,b))) or CatmullRomCurve3(points).getPoint(u); cam.lookAt(...); cam.rotation.z += lerp(roll0,roll1,u).
- **أرقام / params:** FOV 40-52; roll .25 -> 0 (dive), .12 -> -.08 (flythrough); Giza push from (158,7,-44) to (122,14,-26)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html:192-201` · `kosif-one/projects/egypt-2120-animation/index.html:253` · `kosif-one/projects/egypt-2120-animation/index.html:322-323`

#### CAM-149 · طبقة قراءة وحجاب خارج المحراب · Readability glass and arch veil · 📦 بأمر تثبيت
- **ماذا / what:** Keeps busy art behind text readable: a soft elliptical dark radial behind the text card and an even-odd veil that darkens everything outside the arch so the eye stays inside.
- **كيف / how:** #glass 860x500 border-radius 50% radial rgba(25,8,40,.55) -> .32 at 45% -> 0 at 72%; SVG path fill-rule evenodd (full frame minus arch) #12062a op .38 -> .22.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html:29-30` · `kosif-one/projects/thursday-dua-animation/source/index.html:59-60`

#### CAM-150 · تنفس الكاميرا ودفعات الإبراز · Camera breath and punctuating pushes (2D stage) · 📦 بأمر تثبيت
- **ماذا / what:** A 2D 'camera' div scales almost imperceptibly through the film, then pushes on the key line and again on the final amen.
- **كيف / how:** #cam transform-origin 50% 52%: scale 1 -> 1.035 over 10.9 s linear; 1.075 y -18 in 1.6 s E.cam at 10.99; 1.06 y 0 over 9.5 s; 1.09 y -10 in 1.7 s at 22.95.
- **أرقام / params:** max scale 1.09
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html:222-226`

#### CAM-151 · لقطات تدخل وهي تتحرك · Plates that arrive already moving (punch-in drift) · 📦 بأمر تثبيت
- **ماذا / what:** Still images feel like footage: every plate is cut in hard while already scaling and slides on a dolly curve until the next cut.
- **كيف / how:** plate(id,t0,t1,{from,to,x0,x1,y0,y1}): visibility on/off at cut times, img scale from -> to over the whole hold with E.dolly; plates inset -4% to allow movement.
- **أرقام / params:** examples 1.0 -> 1.22 (+40 px y), 1.18 -> 1.02, 1.05 -> 1.25, 1.25 -> 1.06, 1.02 -> 1.3, 1.35 -> 1.0
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html:121-135`

#### CAM-152 · ضربة عاطفية مع اهتزاز · Emotional punch + camera shake · 📦 بأمر تثبيت
- **ماذا / what:** On the emotional word ('تعيس جداً') the whole stage punches in and shakes for a quarter second, then settles.
- **كيف / how:** cam scale 1 -> 1.09 in 0.25 s E.out, back to 1.0 over 0.9 s E.rest; x ±8 px yoyo 0.05 s repeat 7; reset at +0.46 s.
- **أرقام / params:** punch 9%, shake 8 px, 8 half-cycles
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html:140-143`

#### CAM-153 · حركات الكاميرا على المسرح · Stage camera moves (camera, log push, breathe) · 📦 بأمر تثبيت
- **ماذا / what:** Treat the whole stage as one camera: named moves with the camera ease, pushes in log space so zoom speed feels constant, and slow 'breathing' holds.
- **كيف / how:** M.camera(tl,stage,at,{x,y,scale,rotation,dur:1.4,ease:E.cam}); M.push(tl,stage,at,from,to,dur) with logEase (peak ~5% scale per frame); M.breathe(tl,stage,at,dur,{creep:.04,drift}).
- **أرقام / params:** creep 4%/s; drift 0.3-2.5 px/frame
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:310-324`

#### CAM-154 · حركة كين برنز · Ken Burns move detection and replay · 📦 بأمر تثبيت
- **ماذا / what:** Guesses the slow pan/zoom applied to each reference shot and applies the same to replacement footage.
- **كيف / how:** mm_analyze._kenburns_guess; mm_build applies per frame.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_analyze.py` · `kosif-one/tools/kosif-mimic/scripts/mm_build.py`

#### CAM-155 · ملاءمة اللقطة وكن برنز · Shot fit modes + Ken Burns · 📦 بأمر تثبيت
- **ماذا / what:** cover / contain / contain on blurred darkened cover, plus Ken Burns from measured per-shot motion; exact frame count per shot.
- **كيف / how:** mm_build fit param; kenburns=True
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-mimic/scripts/mm_build.py:31`

#### CAM-156 · عمق مجال · Scene op: defocus depth of field · 📦 بأمر تثبيت
- **ماذا / what:** KOSIF Studio scene operation: defocus.
- **كيف / how:** defocus(radius) after background, before hero
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md` · `100-superskills/skills/pixel-studio-painter/scripts/render.py`

#### CAM-157 · تمويه حركة · Scene op: motion blur · 📦 بأمر تثبيت
- **ماذا / what:** KOSIF Studio scene operation: motion_blur.
- **كيف / how:** motion_blur(shape,length,angle) for rain/spray
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md` · `100-superskills/skills/pixel-studio-painter/scripts/render.py`

#### CAM-158 · تكوين الثمبنيل · Thumbnail composition rule · 📦 بأمر تثبيت
- **ماذا / what:** Hero element fills 40% of frame, text in safe zone, optional arrow/circle pointer; 3-word message.
- **كيف / how:** HTML/CSS + Playwright screenshot
- **أرقام / params:** 1280x720, 1080x1080, 1080x1920; readable at 160px width; max 3 main colours
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/thumbnail-social-graphics/SKILL.md:21`

#### CAM-159 · كاميرا المسرح · 2D stage camera move · 📦 بأمر تثبيت
- **ماذا / what:** The whole stage moves as one object (x, y, scale, rotation) for a virtual camera.
- **كيف / how:** MOTION.camera(tl, stageEl, at, {x, y, scale, rotation, dur, ease, origin}).
- **أرقام / params:** dur 1.4 s, ease E.cam
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:311`

#### CAM-160 · دفع الكاميرا · Log-space push-in · 📦 بأمر تثبيت
- **ماذا / what:** Camera push whose scale grows at a constant perceived rate.
- **كيف / how:** MOTION.push(tl, stage, at, from, to, dur, {ease, origin}); duration defaults to durFor(|Δ|·600, camera).
- **أرقام / params:** rule: peak ~5% scale/frame; pushes 1.5-3.1× over 30-70 f
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:316` · `kosif-studio/motion/references/craft-numbers.md`

#### CAM-161 · اهتزاز الكاميرا · Camera shake (seeded) · 📦 بأمر تثبيت
- **ماذا / what:** Decaying seeded jitter in x, y and a little rotation for hits.
- **كيف / how:** MOTION.shake(tl, el, at, {amp, dur, hz, rot, seed}).
- **أرقام / params:** amp 14 px, .5 s, 28 Hz steps, rot .6°, decay (1-i/n)^1.8, settle .12 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:535`

#### CAM-162 · مفاتيح الكاميرا · Smoothstep camera keys · 📦 بأمر تثبيت
- **ماذا / what:** Camera position/look-at keys with smoothstep between them (still between events).
- **كيف / how:** const camAt = K3.cameraKeys([[t,cx,cy,cz,lx,ly,lz],...]); const [p,l] = camAt(t).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:414`

#### CAM-163 · مسار كاميرا مستمر · Continuous Catmull-Rom camera path · 📦 بأمر تثبيت
- **ماذا / what:** One continuous camera through keys (centripetal Catmull-Rom for position and target) that never stops dead.
- **كيف / how:** const path = K3.cameraPath([[t,x,y,z,lx,ly,lz],...]); const [pos, look] = path(t).
- **أرقام / params:** time ease = 0.35·smoothstep + 0.65·linear
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:789`

#### CAM-164 · مفردات اللقطات · Shot vocabulary camera (20 kinds) · 📦 بأمر تثبيت
- **ماذا / what:** Director/Veo shot words as deterministic 3D cameras returning pos/look/fov/roll/focus per t.
- **كيف / how:** const cam = K3.shot(kind, {subject, size, t0, t1, fov, azimuth, distance, degrees, velocity, seed}); K3.applyShot(camera, cam(t), post).
- **أرقام / params:** kinds: establishing .06 frame height, wide .25, medium .55, closeup 1.6, extreme_closeup 4.0, low_angle, high_angle, birds_eye, dutch (12°), tracking (1.2 m/s), crane_up, crane_down, push_in (1.8->1.0 d), pull_back, orbit (360°), arc (60°), handheld, dolly_zoom, whip_pan (90°), turntable; fov 35, az…
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:1038` · `kosif-studio/motion/references/book-lessons.md`

#### CAM-165 · اهتزاز يدوي · Seeded handheld sway · 📦 بأمر تثبيت
- **ماذا / what:** Three octaves of smooth sine noise around a ~1.3 Hz sway, not random jitter.
- **كيف / how:** K3.shot(kind, {handheld:true, shake, seed}) or shotFromWords('handheld ...').
- **أرقام / params:** base 1.3/1.1/0.9 Hz, octaves ×2.17 and ×4.9, amp .012·distance
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:1049`

#### CAM-166 · لقطة من الكلمات · Shot from words · 📦 بأمر تثبيت
- **ماذا / what:** Parses a phrase ('low angle tracking shot', 'slow push-in', 'vertigo') into a camera, combining modifiers.
- **كيف / how:** K3.shotFromWords(text, opts); K3.SHOT_WORDS (25 phrase->kind pairs).
- **أرقام / params:** phrases: dolly zoom, vertigo, whip, turntable, 360, orbit, arc shot, crane up/down, push, pull back, tracking, bird, top down, low/high angle, dutch, extreme close, close-up, establishing, wide, medium, handheld
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:1092`

#### CAM-167 · خلفية الاستوديو · Studio backdrop gradient · 📦 بأمر تثبيت
- **ماذا / what:** Radial gradient canvas texture as a scene background.
- **كيف / how:** scene.background = K3S.studioBackdrop({inner, mid, outer, cy}).
- **أرقام / params:** inner #1e4a44, mid #0c2224, outer #050c0d, centre y .42
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/shape-kit.js:336`

#### CAM-168 · استوديو كريمي · Cream studio sweep · 📦 بأمر تثبيت
- **ماذا / what:** Product-lab set: cream sweep sphere, contact shadow floor, faint grid, key/fill/rim + hemisphere.
- **كيف / how:** K3.studio(scene, {bg, grid}).
- **أرقام / params:** bg #f1efe8; shadow .22; grid 16 m/32 #c9d8c2 .35; key 2.6 @ (3,6,4); fill #dfe8ff .9; rim 1.4; hemi .9
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/lab-kit.js:194`

#### CAM-169 · ضبابية الحركة بالإطارات الفرعية والتعريض الطويل · Sub-frame shutter motion blur and lighten stacking · 📦 بأمر تثبيت
- **ماذا / what:** Averages k sub-frames centred on each frame time (a real shutter) or keeps each pixel's brightest sample for long-exposure light trails and star trails.
- **كيف / how:** film_animate(blur=k, shutter=frames, stack='average'|'lighten'); pages that set window.__nativeBlur accumulate on the GPU instead; exposed on the CLI via motion.py render --blur/--shutter/--stack (film.py's own CLI lacks --blur).
- **أرقام / params:** shutter 0.5 frame = 180 degrees; shutter 30 at 30 fps = 1 s exposure; samples at t + s/fps*((j+.5)/k - .5); averaged in float, quantised once
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/film.py:273` · `kosif-studio/film.py:353` · `kosif-studio/tests/test_studio.py:793`

#### CAM-170 · عمق المجال · Depth of field (defocus) · 📦 بأمر تثبيت
- **ماذا / what:** Everything painted so far goes out of focus (optionally inside a soft-edged shape); call after background steps and before the subject.
- **كيف / how:** defocus(radius, shape=None, soft=30).
- **أرقام / params:** whale background 2.2, far wing 1.2; AI recipe 2
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/render.py:692` · `kosif-studio/scenes/whale_dragon.py:128`

#### CAM-171 · ضبابية حركة اتجاهية · Directional motion blur · 📦 بأمر تثبيت
- **ماذا / what:** Streaks what is inside a shape along an angle — rain, spray, wing beats.
- **كيف / how:** motion_blur(shape, length, angle=90, mix=1) with a line kernel via cv2.filter2D.
- **أرقام / params:** rain 6 px at 104 deg mix .35; spray 7 px at 112 deg mix .7
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/render.py:707` · `kosif-studio/scenes/whale_dragon.py:269`

#### CAM-172 · التشتت اللوني · Chromatic aberration · 📦 بأمر تثبيت
- **ماذا / what:** Red and blue channels scale apart toward the frame edges like a real lens.
- **كيف / how:** chroma(amount).
- **أرقام / params:** default 1.5; whale 1.1; AI recipe 1.4
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/render.py:756`

#### CAM-173 · كاميرا رقمية موجهة على مقطع متكلم · Directed digital camera on a talking clip · 📦 بأمر تثبيت
- **ماذا / what:** One eased move per idea on a static plate: a hook release, slow pushes, lateral drifts, sharp punches on stressed words, a seeded 4-frame micro-shake, and a scale pull-back reveal at the shot change.
- **كيف / how:** GSAP on a #cam wrapper with transformOrigin on the subject
- **أرقام / params:** start 1.10 → 1.035 expo.out 0.55 s; pushes 1.07-1.095 power2.inOut 1.7-2.2 s; punches 1.12/1.16/1.19 in 0.12-0.18 s expo.out; shake (6,−4),(−5,3),(3,−2),(0,0) per frame; reveal 1.42 → 1.10 in 0.6 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/premium_edit/index.html:1`

#### CAM-174 · كاميرا تلقائية تتبع الموضوع · Auto camera from subject boxes · 📦 بأمر تثبيت
- **ماذا / what:** direct.py finds the subject per shot (largest skin region in the upper 78 %, else moving region) and pushes the camera on it, starting wider when the subject is small.
- **كيف / how:** direct.subject_box + shots[{from,to,cx,cy}]
- **أرقام / params:** skin YCrCb Cr 133-178 Cb 80-130 Y>60, area >1.2 %; push 1.03→1.09, small subject (<20 % H) 1.12→1.22; keyword punch 0.035, payoff punch 0.05
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/direct.py:49` · `kosif-studio/motion/direct.py:271`

#### CAM-175 · إبعاد النص عن الوجه · Type off the face over pictures · 📦 بأمر تثبيت
- **ماذا / what:** For verse films with photos, finds the head region after fill-crop and moves the line to the lower or upper third when the face occupies the middle band.
- **كيف / how:** verse.text_band(image, W, H)
- **أرقام / params:** skin ≥0.4 % of frame; head height ≤22 % H; returns 0.70 H or 0.26 H
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/verse.py:350`

#### CAM-176 · شرائط السينما · Letterbox open/close · 📦 بأمر تثبيت
- **ماذا / what:** Cinematic bars that open from the title and close on the end.
- **كيف / how:** GSAP height tween on #letterbox-top/bottom
- **أرقام / params:** 70 px → 0 over 2.2 s, ease drive, starts at min(2.4, 0.15·S)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/blue_hour/index.html:1` · `kosif-studio/motion/projects/water_cycle_3d/index.html:48`

#### CAM-177 · عدسة تدور حول المشهد · Orbit-walk lens with holds · 📦 بأمر تثبيت
- **ماذا / what:** A single lens walks the full circle around the subjects and stops at parts (head, eye, mane) with holds, as a lab/HUD documentary move.
- **كيف / how:** lab-kit orbitWalk(camera, [{t, angle, dist, height, look, fov, hold}])
- **أرقام / params:** e.g. t0 angle 28 dist 6.4 h 2.1 fov 30; t3 −35/2.3/1.75 hold 1.2; t6.5 eye extreme close dist 1.0 fov 26
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/lab_rabbit_lion/src/main.js:1`

#### CAM-178 · جولة سينمائية · Style: Cinematic journey (higgsfield-journey) · 📦 بأمر تثبيت
- **ماذا / what:** Continuous fly-through camera journey across scenes (Higgsfield-style).
- **كيف / how:** 3D/2.5D world with single continuous spline camera; no cuts; transitions via camera travel. Scaffold: python3 tools/kosif.py scaffold higgsfield-journey <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:higgsfield-journey` · `kosif-tool/playbooks/3d.md`

#### CAM-179 · كاميرا Remotion بانجراف بطيء · CameraRig slow drift push/pan/rotate · 📦 بأمر تثبيت
- **ماذا / what:** One group transform drifts across the film: scale 1.08->1.0->1.04->1.1, x 0->-36, y 26->-18->0 at scene boundaries, rotate -0.8->0.8 deg, eased inOutCubic.
- **كيف / how:** interpolate(frame, [0,s1,s1+s2,T], …, {easing: easeInOutCubic, clamp})
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/starters/remotion/src/Film.tsx:102`

#### CAM-180 · مسار كاميرا منحني · Spline camera path · 📦 بأمر تثبيت
- **ماذا / what:** Camera moves along a CatmullRom spline with sine in-out, never linear starts/stops.
- **كيف / how:** THREE.CatmullRomCurve3 sampled at eased p(t) inside seek(t).
- **أرقام / params:** duration 2–5 s; dolly 0.3–1.2 units/s; orbit 10–25°/s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:24-25`

#### CAM-181 · رياضيات كاميرا التحليق · Flyover camera math · 🔑 مفتاح/خدمة
- **ماذا / what:** Smooth cinematic path: rounded curve, constant ground speed, look-ahead heading, constant pitch, bank into turns.
- **كيف / how:** Chaikin corner-cutting 3 passes (4 softer, 2 tighter); walk by arc length; heading = bearing to a point LOOK_AHEAD km further; pitch constant (Cesium pitch = -(90 - pitchFromNadir)); roll = clamp(dHeading*gain, +/-max) measured between aim and 2x look-ahead. Speed = travel km / seconds; slow cameras also render faster (tiles stay cached).
- **أرقام / params:** travel 13 km / 24 s = 0.54 km/s; look-ahead 1.5 km; pitch-from-nadir 76 deg (-14); bank gain 0.6, max 0.13 rad; altitude 4600->4300 m; vertical exaggeration 1.1; path km >= travel + 2*look-ahead
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/references/3d-flyover-architecture.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/assets/flight-path.ts`

#### CAM-182 · مفردات التكوين وترك فراغ للنص · Composition keywords that reserve space for type · 🔑 مفتاح/خدمة
- **ماذا / what:** Ask the generator for rule-of-thirds, centered, wide panoramic, overhead or negative-space framing so later motion typography has a clean area.
- **كيف / how:** Add phrases like 'subject on the right third, generous empty space on the left for text overlay' or 'no text, space for logo on left third'; verify the empty zone before animating type into it.
- **أرقام / params:** LinkedIn banner example 1584x396 with left-third space
- **الدليل / proof:** `kosif-atlas/skills/1446-marketing-skills/3504-image` · `kosif-atlas/skills/881-codex-seo/1954-seo-image-gen`

#### CAM-183 · مفردات حركة الكاميرا لنماذج الفيديو · Camera-move vocabulary for video models · 🔑 مفتاح/خدمة
- **ماذا / what:** Terms video generators understand: static, pan, tilt, dolly in/out, orbit, tracking, crane/aerial, handheld, zoom (lens) vs dolly (body), slow push.
- **كيف / how:** Pick one move per clip and phrase it plainly ('camera slowly pushes in'); Kling and Runway follow explicit verbs well, Seedance R2V tends to ignore or randomise camera verbs, so describe a first-frame framing there instead.
- **الدليل / proof:** `kosif-atlas/skills/1446-marketing-skills/3531-video` · `kosif-atlas/skills/259-quickdesign/865-quickdesign` · `kosif-atlas/skills/2976-pwdev-social-media/12594-video-gen`

#### CAM-184 · التحكم البسيط بالكاميرا في كلينج · Kling simple camera control · 🔑 مفتاح/خدمة
- **ماذا / what:** Numeric single-axis camera moves for T2V/I2V on v1.6+.
- **كيف / how:** camera_control {type:'simple', config:{horizontal, vertical, zoom, roll, pan, tilt}} each -10..10 with exactly ONE non-zero: horizontal 5 = slow pan right, zoom 7 = dramatic push, vertical 8 = tilt-up reveal, tilt 5 = dolly forward, zoom -5 = slow pull-out on a photo.
- **أرقام / params:** range -10..10; one non-zero axis
- **الدليل / proof:** `kosif-atlas/skills/1874-klingai-pack/6067-klingai-camera-control`

#### CAM-185 · تأطير الإطار الأول لكل مقطع بدل حركة الكاميرا · First-frame framing per segment (not camera motion) · 🔑 مفتاح/خدمة
- **ماذا / what:** In multi-segment generated ads what defines the cut is where each segment starts, so prompts describe the opening framing, and UGC keeps the same framing unless asked.
- **كيف / how:** Default: all segments 'medium shot chest-up, eye level'; cinematic progression only on request (wide → medium close-up → face close-up); use character action lines ('turns toward camera') instead of lens moves.
- **الدليل / proof:** `kosif-atlas/skills/259-quickdesign/865-quickdesign`

#### CAM-186 · تتبع الشخص في القص · Subject-follow reframing (bridge cv2) · 🔑 مفتاح/خدمة
- **ماذا / what:** With the local bridge's /api/watch (cv2, no models), the cover crop follows the subject sideways per shot without jitter.
- **كيف / how:** watchMain posts {threshold:10,min:0.5,subject:true}; smoothSubject: samples every 0.4 s, confidence>0.3, two-way exponential smoothing weight 0.3*conf (~1.3 s), still shots (<0.08 travel) use the median, sub-second weak shots not reframed; subjectPan clamps to picture edges.
- **الدليل / proof:** `app/public/js/00_editor.js:2854` · `app/public/js/00_editor.js:2871` · `app/public/js/00_editor.js:2899`

#### CAM-187 · حركة كاميرا: luxury product · Camera grammar: luxury product · 🔑 مفتاح/خدمة
- **ماذا / what:** Concept-matched mid-leg camera move.
- **كيف / how:** Add to leg prompt from move library.
- **أرقام / params:** slow half-orbit around hero object
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md` · `kosif-one/vendor/scroll-world/skills/scroll-world/references/prompts.md`

#### CAM-188 · حركة كاميرا: real estate · Camera grammar: real estate · 🔑 مفتاح/خدمة
- **ماذا / what:** Concept-matched mid-leg camera move.
- **كيف / how:** Add to leg prompt from move library.
- **أرقام / params:** steadicam glide through doorways, crane-up in atria
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md` · `kosif-one/vendor/scroll-world/skills/scroll-world/references/prompts.md`

#### CAM-189 · حركة كاميرا: industrial · Camera grammar: industrial · 🔑 مفتاح/خدمة
- **ماذا / what:** Concept-matched mid-leg camera move.
- **كيف / how:** Add to leg prompt from move library.
- **أرقام / params:** low lateral track with foreground parallax
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md` · `kosif-one/vendor/scroll-world/skills/scroll-world/references/prompts.md`

#### CAM-190 · حركة كاميرا: travel · Camera grammar: travel · 🔑 مفتاح/خدمة
- **ماذا / what:** Concept-matched mid-leg camera move.
- **كيف / how:** Add to leg prompt from move library.
- **أرقام / params:** drone rise-and-reveal then descending swoop
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md` · `kosif-one/vendor/scroll-world/skills/scroll-world/references/prompts.md`

#### CAM-191 · حركة كاميرا: food/craft · Camera grammar: food/craft · 🔑 مفتاح/خدمة
- **ماذا / what:** Concept-matched mid-leg camera move.
- **كيف / how:** Add to leg prompt from move library.
- **أرقام / params:** push in to craft moment, ease back
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md` · `kosif-one/vendor/scroll-world/skills/scroll-world/references/prompts.md`

#### CAM-192 · حركة كاميرا: miniature · Camera grammar: miniature · 🔑 مفتاح/خدمة
- **ماذا / what:** Concept-matched mid-leg camera move.
- **كيف / how:** Add to leg prompt from move library.
- **أرقام / params:** dives + aerial hops
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md` · `kosif-one/vendor/scroll-world/skills/scroll-world/references/prompts.md`

#### CAM-193 · انزلاق إيزومتري ثابت · Locked-iso glide · 🔑 مفتاح/خدمة
- **ماذا / what:** Fixed high isometric angle, only straight level travel; calmest, cheapest rerolls.
- **كيف / how:** Locked-iso clause in every leg prompt; reroll if view rotates.
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md` · `kosif-one/vendor/scroll-world/skills/scroll-world/references/prompts.md`

#### CAM-194 · معماريتا اللقطة المتصلة · Architecture A continuous take vs B dive+connector · 🔑 مفتاح/خدمة
- **ماذا / what:** A: one forward flight for grounded worlds; B: dive into each diorama then aerial connector.
- **كيف / how:** Choose at intake CAMERA.
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md`

#### CAM-195 · إطار HUD للريل · Showreel HUD frame · 👁 شوهد في فيديو
- **ماذا / what:** Overlay layer on top of every scene: 4 L-shaped corner brackets (~40 px arms, 1.5 px white 60%), top-left title/subtitle/REC dot, top-right running timecode HH:MM:SS:FF + spec line, bottom-left scene 
- **كيف / how:** Overlay layer on top of every scene: 4 L-shaped corner brackets (~40 px arms, 1.5 px white 60%), top-left title/subtitle/REC dot, top-right running timecode HH:MM:SS:FF + spec line, bottom-left scene label with segmented progress, bottom-right URL with thin progress bar and 'SAMPLE DATA' boxed tag; mid-edge tick marks
- **أرقام / params:** mono 12-14 px, letter-spacing 0.12em, update label at each scene start
- **الدليل / proof:** `style:pm-marouanegazouzi-6071d5` · `style:pm-motiondsgnr-9dcfa6` · `style:pm-shneural-2abdfa` · `style:pm-tequilafunks-97f6c9`

#### CAM-196 · إطار HUD · HUD frame overlay · 👁 شوهد في فيديو
- **ماذا / what:** corner brackets, mono timecode TC and frame counter F 0263/0900
- **الدليل / proof:** `style:pm-codestackr-c071bf` · `style:pm-mrtanviir-132457` · `style:pm-sudo-kiran-49176d` · `style:pm-topi-003-9ca6b5`

#### CAM-197 · إطار HUD ثابت للشوريل · Persistent HUD reel frame · 👁 شوهد في فيديو
- **ماذا / what:** Overlay layer with corner brackets, mono labels, live timecode TC hh:mm:ss:ff, chapter 'NN/07 NAME', and 4 beat squares filling per beat
- **أرقام / params:** brackets 24px, mono 13px, margin 4% safe
- **الدليل / proof:** `style:pm-ayushunleashed-ece3e3` · `style:pm-kyonax-on-tech-aabc1d` · `style:pm-sudeepsd-1a3485`

#### CAM-198 · إطار معلومات HUD · HUD frame chrome · 👁 شوهد في فيديو
- **ماذا / what:** corner tick marks, timecode, bottom progress line
- **أرقام / params:** 1 px, 40% opacity
- **الدليل / proof:** `style:pm-manuelogomigo-f33ca9` · `style:pm-misbahsy-80eaec` · `style:pm-stephanlivera-df17a2`

#### CAM-199 · إطار معاينة بزوايا وتايمكود · Viewfinder HUD frame · 👁 شوهد في فيديو
- **ماذا / what:** corner L-brackets at 3% inset; mono labels in all four corners; running timecode TC hh:mm:ss:ff from frame number; bottom progress line width = t/duration
- **أرقام / params:** mono 11 px, tracking +10%, blue square bullet #0645e2
- **الدليل / proof:** `style:pm-arjunsh1607-93005d` · `style:pm-sahildesigner23-ee3155`

#### CAM-200 · إطار HUD للريل · HUD showreel frame · 👁 شوهد في فيديو
- **ماذا / what:** Corner brackets, mono chapter label 'NN NAME', timecode, progress bar persistent over all scenes
- **أرقام / params:** mono 10–12 px
- **الدليل / proof:** `style:pm-crazyalphaaa-bc7e75` · `style:pm-zaqailo-212ad3`

#### CAM-201 · جولة كاميرا على عناصر الدرس · Lesson camera tour · 👁 شوهد في فيديو
- **ماذا / what:** key camera (x, y, zoom) to each element as it is drawn, ease-in-out between, final pull-out revealing the full board composition
- **أرقام / params:** zoom 1.0-2.2, moves ~1 s
- **الدليل / proof:** `style:chalkboard`

#### CAM-202 · عالم متصل بكاميرا واحدة · One-take world strip camera · 👁 شوهد في فيديو
- **ماذا / what:** build one long world strip; zones blend by ground colour and prop density; animate camera x/y/zoom keyframes with inOut cubic, moving only in sentence pauses
- **أرقام / params:** wide 0.85-0.95, medium 1.15-1.3, close 1.5-1.6; moves 0.8-1.5 s
- **الدليل / proof:** `style:doodle`

#### CAM-203 · غرفة بزاوية من مضلعات مسقطة · Oblique room from projected polygons · 👁 شوهد في فيديو
- **ماذا / what:** fixed yaw/pitch camera, wall/floor/frame as 3D polygons projected point by point; draw door before wall-with-opening to occlude swing; key inside lock clipped in its own coordinates
- **أرقام / params:** yaw ~20deg, pitch ~10deg
- **الدليل / proof:** `style:fake3d`

#### CAM-204 · كاميرا بمفاتيح في إحداثيات العالم مع تتبع · World-space camera keys + follow blend · 👁 شوهد في فيديو
- **ماذا / what:** keyframes [t, x, y, z, zoom] interpolated with easeInOut; follow weight w(t) blends target to the van position; project target to centre the viewport
- **أرقام / params:** glide ~1.5-2 s between zones
- **الدليل / proof:** `style:isometric`

#### CAM-205 · كاميرا تتبع مع زووم حسب المرحلة · Follow camera with leg-based zoom · 👁 شوهد في فيديو
- **ماذا / what:** camera centre = lerp(head, point slightly ahead on route); zoom = base - k*sin(pi*legProgress) so it widens mid-leg and tightens on arrival
- **أرقام / params:** zoom range ~1.0-1.8
- **الدليل / proof:** `style:map-journey`

#### CAM-206 · حقل شارات طافية فوضوية · Floating badge chaos field · 👁 شوهد في فيديو
- **ماذا / what:** 40-60 mono pill badges with coloured status dot, random rotateZ ±8 deg and translateZ, spawned progressively and drifting slowly; density increases with counter
- **أرقام / params:** spawn every 60-100 ms, drift 10-20 px/s, depth blur on far layer
- **الدليل / proof:** `style:pm-0xfemyn-e114d3`

#### CAM-207 · شريط خطوات مرقمة · Numbered step tab bar · 👁 شوهد في فيديو
- **ماذا / what:** Mono pill tabs '01 Read · 02 Tap · 03 Listen · 04 Speak'; active one inverts (dark fill, light text) as the section changes
- **أرقام / params:** invert 200 ms
- **الدليل / proof:** `style:pm-1stnoel-c20a89`

#### CAM-208 · إطار HUD · HUD corner frame · 👁 شوهد في فيديو
- **ماذا / what:** corner brackets + mono timecode 9 px
- **الدليل / proof:** `style:pm-3xtihor-0f6911`

#### CAM-209 · خاتمة بأشعة وحلقة شخصيات · Sunburst finale ring · 👁 شوهد في فيديو
- **ماذا / what:** Pastel alternating rays from centre rotating slowly; every character sticker arranged on an ellipse around a centred two-line handwritten title; small stars twinkle
- **أرقام / params:** 16-24 rays, rotation 4°/s
- **الدليل / proof:** `style:pm-abderrahmen-g-9e8ed0`

#### CAM-210 · إطار HUD مرقم للشوريل · Numbered HUD reel frame · 👁 شوهد في فيديو
- **ماذا / what:** corner brackets, top-left project label, top-right '0N / 06 - SECTION', bottom timecode, resolution tag and a progress line
- **أرقام / params:** mono 11 px uppercase, 40 px margins
- **الدليل / proof:** `style:pm-agonaliu-466a8f`

#### CAM-211 · تخطيط ميزة: نص يسار ونافذة يمين · Feature beat split layout · 👁 شوهد في فيديو
- **ماذا / what:** Left column: numbered pill + feature name, 2-line headline, grey body, 3 tag chips; right: browser window at 60% width with large soft shadow
- **أرقام / params:** left 35% / right 60%; margins 6%
- **الدليل / proof:** `style:pm-ai-baymax-0ef9dd`

#### CAM-212 · تقريب بطيء داخل الواجهة · Ken-burns inside UI · 👁 شوهد في فيديو
- **ماذا / what:** Scale the screenshot inside the window 1.0->1.25 and pan to the region being explained
- **أرقام / params:** 3-4s easeInOut
- **الدليل / proof:** `style:pm-ai-baymax-0ef9dd`

#### CAM-213 · شريط تنقل سفلي · Bottom nav progress · 👁 شوهد في فيديو
- **ماذا / what:** section names highlighted per chapter
- **الدليل / proof:** `style:pm-aistocksavvy-3fb9f5`

#### CAM-214 · التحليق فوق حقل بطاقات متوهجة · Glowing card field fly-over · 👁 شوهد في فيديو
- **ماذا / what:** hundreds of small thumbnail planes on a curved ground with warm glow; camera dolly forward and tilt; bold statement overlaid centre
- **أرقام / params:** 300-600 cards, DOF blur, 4-5 s
- **الدليل / proof:** `style:pm-ajith-io-4c248f`

#### CAM-215 · طبقة HUD فيلمية · Film HUD overlay · 👁 شوهد في فيديو
- **ماذا / what:** corner crop marks, BPM/bar counter, timecode
- **الدليل / proof:** `style:pm-ajith-io-b5626e`

#### CAM-216 · تخطيط نص وواجهة · Split text/UI layout · 👁 شوهد في فيديو
- **ماذا / what:** left 40% headline, right card with shadow
- **الدليل / proof:** `style:pm-ajith-io-c52e09`

#### CAM-217 · دفع الكاميرا نحو الشخصية · Push-in camera dolly · 👁 شوهد في فيديو
- **ماذا / what:** dolly from wide to mascot close-up with DOF
- **أرقام / params:** 3 s ease-in-out
- **الدليل / proof:** `style:pm-anas0ra-e57aea`

#### CAM-218 · أقواس وإحداثيات · Geo HUD brackets · 👁 شوهد في فيديو
- **ماذا / what:** corner brackets + coordinates + section labels
- **الدليل / proof:** `style:pm-andginja-333d32`

#### CAM-219 · رفع الكاميرا للقطة علوية ختامية · Crane to top-down hero end card · 👁 شوهد في فيديو
- **ماذا / what:** lerp camera from low 3/4 to overhead over 2 s easeInOutCubic; overlay HTML tagline and logo with fade 500 ms
- **أرقام / params:** final FOV 35
- **الدليل / proof:** `style:pm-anilraok-eff262`

#### CAM-220 · عنوان صغير بمساحة فارغة واسعة · Negative-space headline · 👁 شوهد في فيديو
- **ماذا / what:** short 1-2 line headline centred, ~6% height, accent word/icon in brand colour, everything else black
- **أرقام / params:** accent #f03c0a
- **الدليل / proof:** `style:pm-anthonyriera-9b1b2a`

#### CAM-221 · كاميرا عالم واحد بمحاور تركيز وتكبير لوغاريتمي · World-layer camera (focus x, y, log-scale) · 👁 شوهد في فيديو
- **ماذا / what:** lay out the whole UI once in world coordinates; animate a camera with focusX, focusY and log(scale) keyframes, interpolate in log space so zooms feel uniform; never animate two camera moves at once
- **أرقام / params:** ease-in-out cubic 0.6-1.2 s per move, zoom range 1x-6x
- **الدليل / proof:** `style:pm-antonio-kodheli-490109`

#### CAM-222 · خلفية جدار بطاقات مائل مع عمق ميدان · Tilted DOF card wall backdrop · 👁 شوهد في فيديو
- **ماذا / what:** Grid of real-looking content cards on a plane rotated (rotateX 20 deg, rotateZ -10 deg), blurred 4-8 px and darkened, drifting slowly behind a sharp headline
- **أرقام / params:** drift 15 px/s, blur 6 px, opacity 50%
- **الدليل / proof:** `style:pm-aschapmann-131210`

#### CAM-223 · إحساس السرعة بمرور أعمدة السياج · Rail parallax for speed · 👁 شوهد في فيديو
- **ماذا / what:** repeat railing posts along pier; track camera at rider speed so foreground posts sweep past faster than background
- **أرقام / params:** post spacing 2 m; rider speed 4 m/s
- **الدليل / proof:** `style:pm-axtonliu-0b861d`

#### CAM-224 · تجميع شبكة بينتو · Bento grid assembly · 👁 شوهد في فيديو
- **ماذا / what:** Feature tiles of varied sizes/colours spring into a 4x3 grid, each tile a mini feature label
- **أرقام / params:** spring stiffness 180 damping 14, stagger 80 ms
- **الدليل / proof:** `style:pm-bizibeast-10f264`

#### CAM-225 · شبكة بطاقات · Bento principle grid · 👁 شوهد في فيديو
- **ماذا / what:** 3x3 colour cards each looping a mini demo
- **أرقام / params:** stagger 60ms
- **الدليل / proof:** `style:pm-blue-clarity-ef56d0`

#### CAM-226 · علامات قص زاوية للإطار · Corner crop marks frame · 👁 شوهد في فيديو
- **ماذا / what:** Four thin L-shaped ticks framing the UI panel like print registration marks
- **أرقام / params:** 1 px lines, 16 px arms, 30% opacity
- **الدليل / proof:** `style:pm-bogdandragomir-35e024`

#### CAM-227 · مسرح مستدير فوق خلفية متدرجة · Rounded stage over atmospheric gradient · 👁 شوهد في فيديو
- **ماذا / what:** Full-frame brand-colour gradient (bright top-left → dark bottom), centred near-black rounded rectangle ~80%x75% slightly below centre with soft shadow; all action inside the stage
- **أرقام / params:** radius 48px, shadow 0 30px 80px rgba(0,0,0,.6)
- **الدليل / proof:** `style:pm-brainextends-e19ac3`

#### CAM-228 · اقتراب من الجهاز · Device push-in · 👁 شوهد في فيديو
- **ماذا / what:** scale phone 1->1.8 around badge, hold, return
- **أرقام / params:** 1 s easeInOut
- **الدليل / proof:** `style:pm-bthreeagency-b9b8d9`

#### CAM-229 · تسميات صغيرة بأسلوب الملصق · Poster HUD micro-labels · 👁 شوهد في فيديو
- **ماذا / what:** mono 10px plate number, chapter code, colour-key dots at left edge
- **الدليل / proof:** `style:pm-buildfastwithai-53234e`

#### CAM-230 · عرض دوّار للنموذج · Turntable orbit showcase · 👁 شوهد في فيديو
- **ماذا / what:** camera orbits 30-60°/s around model on textured ground with soft shadow
- **الدليل / proof:** `style:pm-buildfastwithai-ed9447`

#### CAM-231 · عنوان يسار وبطاقة واجهة يمين · Split headline + UI card · 👁 شوهد في فيديو
- **ماذا / what:** 40/60 split, headline 2 lines with green key word
- **أرقام / params:** margins 6%
- **الدليل / proof:** `style:pm-charlesmendez-73b6e4`

#### CAM-232 · تقريب على تفاصيل الواجهة · Macro zoom into UI · 👁 شوهد في فيديو
- **ماذا / what:** scale 1→3 on a region over 2s ease-in-out with slight blur
- **الدليل / proof:** `style:pm-dale-vaz-cc612a`

#### CAM-233 · بطاقات خلفية ضبابية · Depth-of-field cards · 👁 شوهد في فيديو
- **ماذا / what:** Back cards opacity .3 blur 4px
- **الدليل / proof:** `style:pm-daniel-haida-8691d4`

#### CAM-234 · نظام وسوم الفصول · Chapter tag system · 👁 شوهد في فيديو
- **ماذا / what:** Mono 'NN/06 SECTION' bottom-left + progress line, spec text bottom-right
- **الدليل / proof:** `style:pm-danilowm-d3720d`

#### CAM-235 · ترويسة تحريرية · Editorial header · 👁 شوهد في فيديو
- **ماذا / what:** brand left, tagline right, section label over rule
- **الدليل / proof:** `style:pm-davidmarcus-a28a60`

#### CAM-236 · شبكة شاشات · Split-screen grid · 👁 شوهد في فيديو
- **ماذا / what:** 3x3 grid of clips on coloured panels
- **الدليل / proof:** `style:pm-davidshulmanfl-371638`

#### CAM-237 · ترويسة فصل مرقّمة · Numbered chapter header · 👁 شوهد في فيديو
- **ماذا / what:** top-left at 5% margin: tiny grey mono index ('04') + bold 700 sans title; fade/blur in 300 ms at chapter start, blur out at end
- **أرقام / params:** index 1.5% h, title 4% h, colour #111113 on #f2f2f2
- **الدليل / proof:** `style:pm-ddryo-loos-300829`

#### CAM-238 · بطاقة عنوان سوداء تتقلص · Black title card shrink-out · 👁 شوهد في فيديو
- **ماذا / what:** full-frame black card with centred white title; scale to 0.9 with rounded corners revealing grey surround, then cross to next UI content
- **أرقام / params:** ~600 ms, ease-in-out, motion blur on text
- **الدليل / proof:** `style:pm-ddryo-loos-300829`

#### CAM-239 · حركة كاميرا بطيئة تكشف المعلم · Slow reveal dolly · 👁 شوهد في فيديو
- **ماذا / what:** Continuous lateral truck with parallax (far skyline slower, near tree line faster) bringing the landmark from frame edge to centre
- **أرقام / params:** ~3 s move easeInOutSine; parallax ratio 0.3/0.6/1.0
- **الدليل / proof:** `style:pm-demitiyageekzen-7770ad`

#### CAM-240 · لوحة فارغة بسيطة · Negative-space minimal canvas · 👁 شوهد في فيديو
- **ماذا / what:** one element on flat warm grey, soft shadow 0 8px 24px rgba(0,0,0,.08)
- **الدليل / proof:** `style:pm-demonugc-4c5753`

#### CAM-241 · بطاقات مبعثرة تستقر في صف منظم · Scatter-to-grid card settle · 👁 شوهد في فيديو
- **ماذا / what:** Start cards at random positions with ±8-12° rotation; spring them to an aligned row while a search pill appears above and branches connect to each
- **أرقام / params:** spring stiffness ~120 damping ~16; 80 ms stagger
- **الدليل / proof:** `style:pm-elliot-garreffa-f334bc`

#### CAM-242 · عداد إطارات كجزء من التصميم · Frame-counter meta HUD · 👁 شوهد في فيديو
- **ماذا / what:** Show 'frame / total' and 'chapter / total' counters in corners, ticking every frame, to celebrate the code-rendered nature
- **أرقام / params:** mono 11 px, total 900 frames at 60 fps
- **الدليل / proof:** `style:pm-fionntobin-97b7af`

#### CAM-243 · عمق ميدان للواجهة · Depth-of-field UI · 👁 شوهد في فيديو
- **ماذا / what:** blur inactive UI, sharpen focus region
- **أرقام / params:** blur 6px
- **الدليل / proof:** `style:pm-fractadev-149adc`

#### CAM-244 · بطاقات بنتو للميزات · Bento feature cards · 👁 شوهد في فيديو
- **ماذا / what:** White rounded cards on light grey, each with title and mini demo, staggered rise
- **أرقام / params:** gap 16 px
- **الدليل / proof:** `style:pm-gautam-mer1-2ae354`

#### CAM-245 · قالب بطاقة موحد لكل عنصر · Templated listicle card · 👁 شوهد في فيديو
- **ماذا / what:** one React/HTML component fed by data rows (title, tagline, bullets, stats, accent colour, illustration); left text column + right framed visual; reuse for every item
- **أرقام / params:** segment 8 s, 6 items, 55/40 split
- **الدليل / proof:** `style:pm-gigabit-million-16b3a0`

#### CAM-246 · شرطات تقدم المقاطع · Segment progress dashes · 👁 شوهد في فيديو
- **ماذا / what:** N short dashes in the header; past ones grey, current one fills with accent colour as the segment plays
- **أرقام / params:** 6 dashes 28x3 px
- **الدليل / proof:** `style:pm-gigabit-million-16b3a0`

#### CAM-247 · إطار كاميرا تسجيل · Camcorder HUD frame · 👁 شوهد في فيديو
- **ماذا / what:** corner brackets, mono labels top (title/reel, TC hh:mm:ss:ff) and bottom (counter, red REC dot blinking 1 Hz)
- **أرقام / params:** inset 5%, 70% opacity
- **الدليل / proof:** `style:pm-gizakdag-b8c59e`

#### CAM-248 · واجهة كاميرا · Viewfinder HUD · 👁 شوهد في فيديو
- **ماذا / what:** corner marks, TC counter, REC dot
- **الدليل / proof:** `style:pm-gizakdag-cf4ae6`

#### CAM-249 · تقريب كولاج طبقي · Collage push-in parallax · 👁 شوهد في فيديو
- **ماذا / what:** layered PNGs scale at different rates
- **الدليل / proof:** `style:pm-gizakdag-cf4ae6`

#### CAM-250 · كاميرا مطاردة بتأخير · Chase camera with lag · 👁 شوهد في فيديو
- **ماذا / what:** camera.position lerps toward ball + offset(2,3,5) each frame, lookAt smoothed target
- **أرقام / params:** lerp 0.06/frame, offset rotates slowly
- **الدليل / proof:** `style:pm-gorden-sun-041f56`

#### CAM-251 · HUD يشرح التقنية · Self-annotating HUD · 👁 شوهد في فيديو
- **ماذا / what:** Top line shows a mono code comment describing the current technique (e.g. '// per-letter rise + rotate · stagger 22ms · circ.out') and right side 'NN / SECTION'; bottom shows scene id, BPM, bar number
- **كيف / how:** Top line shows a mono code comment describing the current technique (e.g. '// per-letter rise + rotate · stagger 22ms · circ.out') and right side 'NN / SECTION'; bottom shows scene id, BPM, bar number with 4 beat diamonds that fill per beat, and a full-width timeline whose diamond keyframes turn red as playback passes
- **أرقام / params:** mono 12 px, letter-spacing .1em, red #e93e24 progress
- **الدليل / proof:** `style:pm-grace-sunnyy-29bc61`

#### CAM-252 · مقارنة: ما كُتب مقابل البديل · Evidence pair: typed vs instead · 👁 شوهد في فيديو
- **ماذا / what:** two columns, each with a kicker dot (red 'what people typed', green 'type this instead'), prompt card above and reply card below; paraphrased replies use a dashed border, verbatim replies a solid one
- **أرقام / params:** column gap ~4% width
- **الدليل / proof:** `style:pm-henkvaness-0e06af`

#### CAM-253 · عدادات ركنية أحادية · Mono corner counters · 👁 شوهد في فيديو
- **ماذا / what:** 04/10 index top-right, labels uppercase mono
- **الدليل / proof:** `style:pm-heyiammallik-e72d17`

#### CAM-254 · شريط زمني بنقاط مفاتيح · Editor timeline HUD · 👁 شوهد في فيديو
- **ماذا / what:** bottom bar with diamond keyframes, playhead moving with real time, handwritten section label at playhead; timecode top-right in HH:MM:SS:FF
- **أرقام / params:** 1px line, 6 diamonds
- **الدليل / proof:** `style:pm-himanshutwtxs-5f4b43`

#### CAM-255 · دفع كاميرا على واجهة مائلة · Tilted UI push-in · 👁 شوهد في فيديو
- **ماذا / what:** rotateX ~10deg, translateZ push 3s
- **الدليل / proof:** `style:pm-ho-ba-f3f0e9`

#### CAM-256 · إطار HUD ورقي · Paper HUD frame · 👁 شوهد في فيديو
- **ماذا / what:** corner brackets + tiny mono timecode labels on cream ground
- **الدليل / proof:** `style:pm-hqmank-7c61f1`

#### CAM-257 · لقطة ميزة بتقسيم تحريري · Editorial split feature beat · 👁 شوهد في فيديو
- **ماذا / what:** Left: headline + one-line subline; right: dark UI card with large soft shadow sliding in
- **أرقام / params:** text column 35%, card 50%, margins 6%
- **الدليل / proof:** `style:pm-iammxfschr-d68f90`

#### CAM-258 · إطار HUD لعبة ثابت · Persistent game HUD frame · 👁 شوهد في فيديو
- **ماذا / what:** Top bar with player name, zero-padded score counter, hearts and level; bottom bar with section label, countdown TIME and a thin progress bar that grows across the full duration
- **أرقام / params:** score pad 7 digits; timer 0.1s steps; bar 4px lime
- **الدليل / proof:** `style:pm-ibrahimwasim240-809370`

#### CAM-259 · رقم فهرس مع اسم النموذج · Index + model lower-third · 👁 شوهد في فيديو
- **ماذا / what:** thin violet rule under the hero word, pixel-mono index number (01-04) in violet and the model identifier in typewriter mono beside it
- **أرقام / params:** slide in 250 ms, index 2x label size
- **الدليل / proof:** `style:pm-influencer-seo-ce8c33`

#### CAM-260 · منظر متحرك من نافذة بطبقات بارالاكس · Window parallax travel · 👁 شوهد في فيديو
- **ماذا / what:** Clip a landscape to a window rect; draw 4-5 tiled layers (sky, mountains, hills+buildings, trees, foreground fence/poles) scrolling horizontally at increasing speeds; wrap tiles seamlessly
- **أرقام / params:** speeds 10/30/80/200/600 px/s at 1080p
- **الدليل / proof:** `style:pm-itsolelehmann-e47532`

#### CAM-261 · تكوين متناظر بأسلوب ويس أندرسون · Symmetrical Wes-Anderson frame · 👁 شوهد في فيديو
- **ماذا / what:** Centre every element on the vertical axis, mirror props left/right, pastel pink + deep purple + gold, flat frontal perspective, ornamental medallion at top centre
- **أرقام / params:** palette rose #c8909a, purple #402151, gold #d4a645
- **الدليل / proof:** `style:pm-itsolelehmann-e47532`

#### CAM-262 · مؤشر المشاهد · Scene index HUD · 👁 شوهد في فيديو
- **ماذا / what:** '03/08 KINETIC TYPE' label + progress segment
- **أرقام / params:** mono 10px
- **الدليل / proof:** `style:pm-itsuki-dev-10942d`

#### CAM-263 · كاميرا مطاردة مائلة · Chase camera with bank · 👁 شوهد في فيديو
- **ماذا / what:** lerp camera behind target, roll proportional to lateral velocity
- **أرقام / params:** lerp 0.1, roll max 25deg
- **الدليل / proof:** `style:pm-ivanfioravanti-bd9261`

#### CAM-264 · اقتراب للشاشة مع كتابة طرفية · Push-in terminal typewriter · 👁 شوهد في فيديو
- **ماذا / what:** Scale the whole scene ~2.5x toward monitor, type a green mono line with block cursor, then pull back
- **أرقام / params:** push 700 ms easeInOut, 40 ms/char
- **الدليل / proof:** `style:pm-jake11moran-a269c4`

#### CAM-265 · إطار HUD للشوريل · Showreel HUD overlay · 👁 شوهد في فيديو
- **ماذا / what:** Persistent overlay: 4 corner brackets (20 px arms), mono title top-left, timecode top-right, chapter label bottom-left, 'frame / total' with thin progress line bottom-right, all ~12 px mono at 60% opa
- **كيف / how:** Persistent overlay: 4 corner brackets (20 px arms), mono title top-left, timecode top-right, chapter label bottom-left, 'frame / total' with thin progress line bottom-right, all ~12 px mono at 60% opacity
- **أرقام / params:** margin 32 px, update every frame
- **الدليل / proof:** `style:pm-jasonzhou1993-8595e0`

#### CAM-266 · إطار بعلامات قص · Crop-mark frame · 👁 شوهد في فيديو
- **ماذا / what:** Four L corners + brand tag + footer date
- **أرقام / params:** safe 40px
- **الدليل / proof:** `style:pm-jesscaroline7-1ff7cb`

#### CAM-267 · عنوان فوق نافذة المنتج · Headline over product window · 👁 شوهد في فيديو
- **ماذا / what:** short lowercase line at top centre ('as a demo.', 'or a video.') with a browser/app window sliding up below it and a cursor performing one action
- **أرقام / params:** window slide 400 ms easeOutQuint
- **الدليل / proof:** `style:pm-jhylee95-e1152f`

#### CAM-268 · عناصر زوايا ثابتة · Persistent corner chrome · 👁 شوهد في فيديو
- **ماذا / what:** tracked uppercase section kicker top-left, contextual line icon top-right, brand logo bubble bottom-left kept across every cut to unify rapid scenes
- **أرقام / params:** kicker ~1.5% height, logo 7% height
- **الدليل / proof:** `style:pm-jhylee95-e1152f`

#### CAM-269 · كاميرا افتراضية تتجول فوق لوحة واجهة كبيرة · Virtual camera over one big UI canvas · 👁 شوهد في فيديو
- **ماذا / what:** Lay out the full product UI on a large canvas and animate a transform (translate/scale) to frame each step instead of cutting
- **أرقام / params:** moves 1-1.5 s easeInOutCubic; zoom 1.0-1.8
- **الدليل / proof:** `style:pm-justincooperman-e7bbc4`

#### CAM-270 · تخطيط صفوف الآلات · Instrument tier diagram layout · 👁 شوهد في فيديو
- **ماذا / what:** Horizontal rails at 25/55/90% height, each a row of labelled bars with note names below; colour-code each instrument family
- **أرقام / params:** bar width ∝ 1/pitch, mono 9 px labels
- **الدليل / proof:** `style:pm-kamstudiolabs-447565`

#### CAM-271 · دخول وخروج من الشاشة · Push into screen bookend · 👁 شوهد في فيديو
- **ماذا / what:** scale camera from room to monitor content and back
- **الدليل / proof:** `style:pm-kamstudiolabs-c9bb28`

#### CAM-272 · لوحات ثلاثية للأقسام · Triptych category panels · 👁 شوهد في فيديو
- **ماذا / what:** 3 equal vertical colour panels slide up staggered 120 ms, each with icon + serif label
- **أرقام / params:** blue/black/yellow
- **الدليل / proof:** `style:pm-kangaroohere-b10f8d`

#### CAM-273 · عنوان جانبي عمودي · Vertical side label · 👁 شوهد في فيديو
- **ماذا / what:** Rotated 90° uppercase word on left edge in accent blue framing a card
- **الدليل / proof:** `style:pm-kangaroohere-b10f8d`

#### CAM-274 · كشف اللوحة بالابتعاد · Canvas zoom-out reveal · 👁 شوهد في فيديو
- **ماذا / what:** Start tight on a single tile (logo) and scale the canvas container from ~4x to ~0.5x with motion blur so the whole body of work appears at once
- **أرقام / params:** 1.2-1.5 s easeInOut, blur proportional to speed
- **الدليل / proof:** `style:pm-kikelopezdesign-7cc9e8`

#### CAM-275 · عناوين فصول وشريط زمني · Chapter HUD + timeline marker · 👁 شوهد في فيديو
- **ماذا / what:** '05 / ELIZA' top-left, tick ruler top-right with orange marker
- **الدليل / proof:** `style:pm-kloss-xyz-fe0c31`

#### CAM-276 · شريط تبويبات كأداة تنقل بين الفصول · Pill tab bar as chapter navigator · 👁 شوهد في فيديو
- **ماذا / what:** persistent top pill nav; a dark active pill slides to next tab, scene content (headline left, window right) swaps with blur crossfade
- **أرقام / params:** slide 300 ms ease-in-out
- **الدليل / proof:** `style:pm-kmasiff-cc72cb`

#### CAM-277 · زووم لا نهائي أُسّي · Exponential infinite zoom · 👁 شوهد في فيديو
- **ماذا / what:** scale = base^(t/T); zoom toward a fixed anchor; each segment duration proportional to log(zoom ratio) so perceived speed is constant
- **أرقام / params:** zoom ratio per world ~8-20x, ~3-5 s per world
- **الدليل / proof:** `style:pm-koldo2k-5cff87`

#### CAM-278 · دوران ودفع الكاميرا · Orbit push-in · 👁 شوهد في فيديو
- **ماذا / what:** OrbitControls tween target and distance
- **أرقام / params:** 4 s ease
- **الدليل / proof:** `style:pm-konstantinsaifo-96fc89`

#### CAM-279 · خطوة مع تعليق · Step label + caption · 👁 شوهد في فيديو
- **ماذا / what:** mono '01 · UPLOAD' + bold caption under UI
- **الدليل / proof:** `style:pm-l3d1c-0e35a3`

#### CAM-280 · كاميرا افتراضية فوق سبورة كبيرة · Virtual camera over a big board · 👁 شوهد في فيديو
- **ماذا / what:** lay all steps on one large canvas (~4x frame); animate a camera transform (translate/scale) between step regions; finish with a pull-back to show the whole map
- **أرقام / params:** pan 0.8-1.2 s ease-in-out, final scale ~0.3
- **الدليل / proof:** `style:pm-lemomo-ai-0d9cff`

#### CAM-281 · تقريب الكاميرا على عنصر الواجهة · UI camera push-in · 👁 شوهد في فيديو
- **ماذا / what:** Scale and translate the whole UI layer so a target element (button) fills a corner, then return
- **أرقام / params:** scale 1->2.5, 800 ms easeInOutCubic
- **الدليل / proof:** `style:pm-lester-tyy-f897f7`

#### CAM-282 · إطار سويسري ثابت بعداد فصول ووقت · Swiss HUD frame with chapter counter · 👁 شوهد في فيديو
- **ماذا / what:** Corner crop marks, mono labels in four corners (name/role, project/year, chapter 'NN — NAME', running timecode) and a segmented progress bar at bottom centre
- **أرقام / params:** inset 3%, mono 11 px uppercase, segments = chapter count
- **الدليل / proof:** `style:pm-levabashidze-2d713a`

#### CAM-283 · عدسة مكبرة لكشف التفاصيل · Magnifier zoom-in proof · 👁 شوهد في فيديو
- **ماذا / what:** draw a circle + handle; inside, render the function rescaled around a focus point by factor k so curvature vanishes; caption 'magnification ×100'
- **أرقام / params:** circle r ~35% H; k = 1→100 animated; compare smooth vs corner (|x|)
- **الدليل / proof:** `style:pm-linearuncle-5d2bae`

#### CAM-284 · تراكب عمق بخلفية مموهة · Background blur depth stack · 👁 شوهد في فيديو
- **ماذا / what:** When focusing on a detail panel, keep the previous scene (gallery) behind it blurred 12-20 px and dimmed 50%, panel slides in from the right with shadow
- **أرقام / params:** blur 16 px, dim 0.5
- **الدليل / proof:** `style:pm-listudio-820c7b`

#### CAM-285 · واجهة فصول · Chapter HUD · 👁 شوهد في فيديو
- **ماذا / what:** corner brackets, chapter index, timecode, bpm in mono
- **الدليل / proof:** `style:pm-lukasersil-0ed38e`

#### CAM-286 · خاتمة بأشرطة سينمائية تنغلق · Letterbox squeeze outro · 👁 شوهد في فيديو
- **ماذا / what:** Black bars animate from top and bottom until only a thin strip of the name card remains, then cut to black
- **أرقام / params:** ~500 ms easeInCubic
- **الدليل / proof:** `style:pm-madhav-xo-f97f20`

#### CAM-287 · مزج كتابة رأسية وأفقية · Vertical + horizontal type pairing · 👁 شوهد في فيديو
- **ماذا / what:** large glyph horizontal plus a vertical stack of smaller glyphs, separated by thin 1-2 px L-shaped rule lines
- **أرقام / params:** rule 1.5px #f4f4eb at 60%
- **الدليل / proof:** `style:pm-majin-appsheet-2d3c1a`

#### CAM-288 · تسميات صغيرة في الزوايا · Corner meta labels · 👁 شوهد في فيديو
- **ماذا / what:** tiny wide-tracked condensed caps labels top-left (with red underline) and bottom-right (year/version)
- **أرقام / params:** tracking .3em, size ~2%
- **الدليل / proof:** `style:pm-majin-appsheet-2d3c1a`

#### CAM-289 · شارة خطوة مرقمة · Numbered step chip · 👁 شوهد في فيديو
- **ماذا / what:** Top-centre label: small accent-filled square with two-digit number in dark mono + uppercase tracked mono step name; swap on each step
- **أرقام / params:** chip 28 px, label letter-spacing .15em
- **الدليل / proof:** `style:pm-majorbaguette-fb11d7`

#### CAM-290 · طيران الكاميرا بين الفصول · Camera chapter fly-to · 👁 شوهد في فيديو
- **ماذا / what:** lerp camera pos/target over 3 s easeInOutCubic
- **الدليل / proof:** `style:pm-mdaman010-e7226a`

#### CAM-291 · إطار HUD بزوايا وعدّاد زمني · HUD corner frame with running timecode · 👁 شوهد في فيديو
- **ماذا / what:** four small mono labels pinned to safe-area corners (URL, network, slogan, live timecode mm:ss.cs) that persist across cuts and stay readable on both black and white
- **أرقام / params:** ~1.5% height, 60-70% opacity grey
- **الدليل / proof:** `style:pm-micheleharmonic-77628e`

#### CAM-292 · نفق لا نهائي · Infinite tunnel zoom · 👁 شوهد في فيديو
- **ماذا / what:** repeating rings of instances scaled exponentially, wrap-around
- **الدليل / proof:** `style:pm-monokern-ade5b6`

#### CAM-293 · إطار HUD بفصول مرقمة · Chaptered HUD frame · 👁 شوهد في فيديو
- **ماذا / what:** corner brackets, 0N/07 chapter label, timecode, ruler progress
- **أرقام / params:** mono 24 px at 1080w
- **الدليل / proof:** `style:pm-ndhabarde11-f155b4`

#### CAM-294 · كاميرا مطاردة تدور مع الطائرة · Chase camera with roll · 👁 شوهد في فيديو
- **ماذا / what:** Camera target = plane position + offset behind/above in plane space, smoothed with a critically damped spring; inherit a fraction of plane roll so the horizon tilts
- **أرقام / params:** offset (0, 2, -8), spring 4 Hz, roll inherit 0.6-1.0
- **الدليل / proof:** `style:pm-nft-chen-5f8bb0`

#### CAM-295 · مقارنة أنت/أنا بتقسيم الشاشة · You/me split comparison · 👁 شوهد في فيديو
- **ماذا / what:** Dashed vertical divider, labels at top, one icon per side (key = ownership, pencil = action) and a red caveat line with crash arrow
- **أرقام / params:** divider dash 8/6
- **الدليل / proof:** `style:pm-nikolajankovic-ce4ff4`

#### CAM-296 · إطار HUD سينمائي · Cinematic HUD chrome · 👁 شوهد في فيديو
- **ماذا / what:** Corner crop brackets, top labels and timecode, bottom elapsed bar with tick marks and moving playhead; everything ~40% opacity tiny mono
- **أرقام / params:** margins 4%; ticks every 0.1s
- **الدليل / proof:** `style:pm-nolkeeg-bf062e`

#### CAM-297 · خط تقدم على حافة الشاشة السفلية · Bottom-edge progress line · 👁 شوهد في فيديو
- **ماذا / what:** 2 px black line at the very bottom edge grows linearly from left over the whole duration, signalling story progress
- **أرقام / params:** width = t/duration * 100%
- **الدليل / proof:** `style:pm-palashbagchi11-0a4b6b`

#### CAM-298 · بيانات وصفية في زوايا الملصق · Poster metadata HUD · 👁 شوهد في فيديو
- **ماذا / what:** four corner mono labels (title, chapter 'NN / NAME', grid spec, running timecode) that update per act
- **أرقام / params:** mono 10-12 px uppercase, tracking +8%
- **الدليل / proof:** `style:pm-pankajkumar-dev-0bee87`

#### CAM-299 · بطاقة مقسومة فاتح/داكن للنتيجة · Split light/dark result card · 👁 شوهد في فيديو
- **ماذا / what:** rounded card with controls on a light half and the result number in brand orange on a black half; a mascot overlaps the corner
- **أرقام / params:** radius 16 px, shadow 0 20 40 rgba(0,0,0,.1)
- **الدليل / proof:** `style:pm-paulo-kombucha-96431c`

#### CAM-300 · شريط فصول · Chapter progress bar · 👁 شوهد في فيديو
- **ماذا / what:** top '04 / 07 TITLE' strip
- **الدليل / proof:** `style:pm-polydao-7a572b`

#### CAM-301 · جدار بطاقات · Card wall drift · 👁 شوهد في فيديو
- **ماذا / what:** 4x3 cards slight rotation drift
- **الدليل / proof:** `style:pm-quickdesignio-dd93d0`

#### CAM-302 · عنوان جانبي مع بطاقة واجهة طافية · Split headline + floating UI card · 👁 شوهد في فيديو
- **ماذا / what:** Left column: mono kicker with dot, 2-line bold headline (line 2 in brand colour); right column: white rounded card with large soft shadow; keep layout fixed and swap content per feature
- **أرقام / params:** card radius 16px, shadow 0 20px 60px rgba(30,40,80,.12), split 40/60
- **الدليل / proof:** `style:pm-ratheejaisal-1f4538`

#### CAM-303 · اقتراب بطيء جدًا نحو الهدف · Ultra-slow approach dolly · 👁 شوهد في فيديو
- **ماذا / what:** Exponential ease of camera distance over minutes so object size grows steadily; slight inclination change for reveal
- **أرقام / params:** distance 200 r_s -> 6 r_s over ~120 s, log-space interpolation
- **الدليل / proof:** `style:pm-rebutonepress-810f78`

#### CAM-304 · إطار HUD للفصول · Chapter HUD frame · 👁 شوهد في فيديو
- **ماذا / what:** corner brackets, chapter n/8, mono label, progress line bottom
- **الدليل / proof:** `style:pm-rendesr-86be44`

#### CAM-305 · واجهة قراءات حية · Scope HUD with live readouts · 👁 شوهد في فيديو
- **ماذا / what:** four corner labels in small uppercase sans; bottom-left 'CH1 2.0V/div 110BPM T+ss.ss' updated per frame; top-right chapter word swaps per section
- **أرقام / params:** font 11-13px at 720p, 70% opacity
- **الدليل / proof:** `style:pm-rneayan-ea6129`

#### CAM-306 · صور تطير لتكوين شبكة إلهام · Fly-in moodboard grid · 👁 شوهد في فيديو
- **ماذا / what:** 9 images start off-frame with random rotation/scale and ease into a 3x3 grid with small gaps, staggered
- **أرقام / params:** stagger 50 ms, 600 ms expo-out, start rot ±25 deg
- **الدليل / proof:** `style:pm-rossaxbt-3085b7`

#### CAM-307 · دفع كاميرا مستمر بلا ارتداد · Continuous push camera · 👁 شوهد في فيديو
- **ماذا / what:** Each scene scales 1.00->1.04; next scene starts at the previous end scale so zoom never snaps; all appearances use >=0.3 s eased fades
- **أرقام / params:** scale +0.04 per scene
- **الدليل / proof:** `style:pm-rossaxbt-3085b7`

#### CAM-308 · إطار سينمائي · Letterbox cinematic · 👁 شوهد في فيديو
- **ماذا / what:** black bars to 2.39:1, shot list with varied lens
- **الدليل / proof:** `style:pm-ryzoft-4f85bd`

#### CAM-309 · شبكة ملخص مرقمة · Recap grid with numbered badges · 👁 شوهد في فيديو
- **ماذا / what:** Blur last footage frame as backdrop, left: big CTA question in white + lime, right: 3x3 grid of segment stills each with white border and numbered lime circle, staggered pop
- **أرقام / params:** stagger 60 ms, card tilt 0-2 deg
- **الدليل / proof:** `style:pm-sab8a-364a5a`

#### CAM-310 · إطار HUD سينمائي ثابت · Persistent cinematic HUD frame · 👁 شوهد في فيديو
- **ماذا / what:** corner brackets 24px inset; mono uppercase labels: title/artist top-left, countdown top-right, 'BAR n / N' + dash progress bottom-left, 'NN — CHAPTER' bottom-right; all at ~60% opacity cream
- **أرقام / params:** font mono 11-13px @1080p, tracking 0.15em, inset 40px
- **الدليل / proof:** `style:pm-samaote-5e2fc2`

#### CAM-311 · كلمات تسقط في خلايا شبكة · Paper grid drop-in · 👁 شوهد في فيديو
- **ماذا / what:** cream grainy paper, black 2px grid lines draw on, each word snaps into a cell on its onset, key word coloured red, red dot pops (scale 0->1.1->1)
- **أرقام / params:** 3x3 grid; red #e0482a
- **الدليل / proof:** `style:pm-samaote-5e2fc2`

#### CAM-312 · ملصقات فصول HUD · Chapter HUD labels · 👁 شوهد في فيديو
- **ماذا / what:** 01 Geometry / 02 Depth corner labels + timecode
- **الدليل / proof:** `style:pm-samuel-spitz-974923`

#### CAM-313 · جدار بطاقات مائل متحرك · Tilted masonry card wall · 👁 شوهد في فيديو
- **ماذا / what:** Grid of rounded video thumbnails rotated ~20 deg occupying right half, translated diagonally continuously to suggest infinite content; text on left
- **أرقام / params:** rotate 20deg, speed ~80 px/s, radius 18 px
- **الدليل / proof:** `style:pm-samuel-yostt-891f87`

#### CAM-314 · بطاقة فصل أسفل اليسار · Chapter text card bottom-left · 👁 شوهد في فيديو
- **ماذا / what:** colored rule + 'n of 11' + condensed headline + 3-line body, crossfade on chapter
- **الدليل / proof:** `style:pm-sayan-shanky-f850d8`

#### CAM-315 · إطار عدسة كاميرا بفصول مرقمة · Viewfinder HUD chapters · 👁 شوهد في فيديو
- **ماذا / what:** Corner brackets, reel ID, running timecode and 'NN / 08 CHAPTER' label with progress dots updated on each section
- **أرقام / params:** mono 11px; 40% opacity; margin 3%
- **الدليل / proof:** `style:pm-shinskinakamoto-20190b`

#### CAM-316 · شريحة عنوان ضخم مع جسم ثلاثي الأبعاد · Editorial headline + 3D object slide · 👁 شوهد في فيديو
- **ماذا / what:** left headline in heavy caps (second line lime), mono subline, rotating chrome/lime blob on right, pagination top-right
- **أرقام / params:** headline ~12% frame height per line
- **الدليل / proof:** `style:pm-shneural-2abdfa`

#### CAM-317 · تراجع لكشف الكولاج · Collage pull-back reveal · 👁 شوهد في فيديو
- **ماذا / what:** zoom out to show all previous scenes as tiled cards dimmed
- **أرقام / params:** scale 1→0.3
- **الدليل / proof:** `style:pm-slvdev-64c45a`

#### CAM-318 · مرور الكاميرا على أوراق مع ختم · Paperwork dolly + stamp · 👁 شوهد في فيديو
- **ماذا / what:** Camera tracks over a column of form sheets under a spotlight; a red stamp slams onto one
- **أرقام / params:** dolly 2 s, stamp scale 1.4->1 in 120 ms
- **الدليل / proof:** `style:pm-spearwtf-3c1fd1`

#### CAM-319 · خطوة مرقمة مع واجهة · Numbered step split · 👁 شوهد في فيديو
- **ماذا / what:** big gradient numeral 01 + 2-line title left, UI window right sliding in
- **أرقام / params:** window slides x+60 ->0 500 ms
- **الدليل / proof:** `style:pm-sudo-kiran-4f8b59`

#### CAM-320 · سبورة بيضاء مؤطرة على جدار داكن · Framed whiteboard set · 👁 شوهد في فيديو
- **ماذا / what:** off-white rounded rect with faint smudge noise, 8 px light-grey frame, tray bar under it with drop shadow, dark slate wall with radial vignette; subtitles live on the wall below
- **أرقام / params:** board ~85% width, wall #2f3a3e
- **الدليل / proof:** `style:pm-tak3sh8-be5012`

#### CAM-321 · إطار HUD إنتاجي · Production HUD frame · 👁 شوهد في فيديو
- **ماذا / what:** Corner brackets, bottom-left spec string (ID, BPM, resolution, fps), bottom-right elapsed time + beat counter, left vertical ruler ticks
- **أرقام / params:** mono 11px olive
- **الدليل / proof:** `style:pm-techhalla-7acbc2`

#### CAM-322 · عنوان مع دليل بصري · Headline + proof layout · 👁 شوهد في فيديو
- **ماذا / what:** headline top-left 64px, visual proof fills lower 70%
- **الدليل / proof:** `style:pm-techyoutbe-945b56`

#### CAM-323 · HUD تقني بتسميات FIG · FIG-caption technical HUD · 👁 شوهد في فيديو
- **ماذا / what:** Corner ticks; top-left reel title; top-right 'NN/06 — CHAPTER'; per-scene caption 'FIG.0n — NAME' with a short line of technical specs (e.g. '9x5 grid · radial ripple · eases'); bottom: timecode, cent
- **كيف / how:** Corner ticks; top-left reel title; top-right 'NN/06 — CHAPTER'; per-scene caption 'FIG.0n — NAME' with a short line of technical specs (e.g. '9x5 grid · radial ripple · eases'); bottom: timecode, centre progress bar, 'WxH · 60P · 120 BPM' with 4 beat squares
- **أرقام / params:** mono 11 px, colour adapts to scene ground
- **الدليل / proof:** `style:pm-teslachartz-c58b32`

#### CAM-324 · شخص صغير لإبراز الضخامة · Scale figure in frame · 👁 شوهد في فيديو
- **ماذا / what:** place a tiny red-cloaked character centre-low facing a huge emissive object; only saturated colour in frame
- **أرقام / params:** figure ~5% frame height
- **الدليل / proof:** `style:pm-theparuchh-6e08c3`

#### CAM-325 · شريط مراحل · Stage progress rail · 👁 شوهد في فيديو
- **ماذا / what:** 4 colored dots on line with labels, active fills
- **الدليل / proof:** `style:pm-theviableedge-9065be`

#### CAM-326 · كولاج بطاقات متناثرة · Scattered card collage · 👁 شوهد في فيديو
- **ماذا / what:** rotated small cards drift slightly
- **الدليل / proof:** `style:pm-theviableedge-9065be`

#### CAM-327 · شبكة بطاقات صور متتابعة · Staggered photo card grid · 👁 شوهد في فيديو
- **ماذا / what:** 3 rounded photo cards on dark navy rise 40 px + fade with 100 ms stagger, labels bottom-left
- **أرقام / params:** radius 12px, gap 2%
- **الدليل / proof:** `style:pm-thismacapital-dfba20`

#### CAM-328 · إطار HUD للريل · HUD reel chrome · 👁 شوهد في فيديو
- **ماذا / what:** Scene code, ruler scrubber with moving marker, spec text 1920x1080/30fps, corner brackets
- **الدليل / proof:** `style:pm-tolgayhickiran-e90799`

#### CAM-329 · عناوين خطوات مرقمة · Numbered step headers · 👁 شوهد في فيديو
- **ماذا / what:** italic serif 01/02/03 + bold label top-left
- **الدليل / proof:** `style:pm-utopyaszx-1b2f94`

#### CAM-330 · مسطرة زمنية للفصول · Chapter ruler timeline · 👁 شوهد في فيديو
- **ماذا / what:** bottom ruler with ticks and diamond chapter markers; a red playhead moves with the video; label shows current frame + chapter name in serif italic
- **أرقام / params:** y = 95% height, ticks every 10 frames
- **الدليل / proof:** `style:pm-vanshwtfff-db0466`

#### CAM-331 · جدار لقطات مائل ينزلق بسرعة · Tilted screenshot wall sweep · 👁 شوهد في فيديو
- **ماذا / what:** grid of rounded screenshots inside a container rotated ~-15° with rotateX tilt; translate diagonally with motion blur; scale down to reveal
- **أرقام / params:** rotate -15°, gap 24 px, radius 12 px, sweep 3-4 s
- **الدليل / proof:** `style:pm-viktoroddy-98c1d8`

#### CAM-332 · بطاقات مكدسة مائلة · Stacked badge cards · 👁 شوهد في فيديو
- **ماذا / what:** 2 cards with ±5° rotation, overlap, spring in
- **الدليل / proof:** `style:pm-wani-shola-16ca7a`

#### CAM-333 · ملصقات منحنيات التسهيل · HUD ease labels · 👁 شوهد في فيديو
- **ماذا / what:** show easing name + timecode in corners
- **الدليل / proof:** `style:pm-web3wesley-7bb108`

#### CAM-334 · دفع الكاميرا داخل نافذة التطبيق · Push into app window · 👁 شوهد في فيديو
- **ماذا / what:** Show a full desktop window, then scale+translate the group to crop on the area of interest while headline stays pinned
- **أرقام / params:** scale 1 -> 2.2 over ~1 s easeInOutCubic
- **الدليل / proof:** `style:pm-wozu-co-242285`

#### CAM-335 · إطار ستارة · Stage curtain frame · 👁 شوهد في فيديو
- **ماذا / what:** red curtain sides + valance overlay
- **الدليل / proof:** `style:pm-x4b47x-9cc84f`

#### CAM-336 · عبور الكاميرا بين كروت طائرة · Z-space card fly-through · 👁 شوهد في فيديو
- **ماذا / what:** each card has fixed translateZ and xy; global cameraZ added to all; opacity fades as card z approaches camera; trigger whoosh at computed pass time (inverse of easing)
- **أرقام / params:** 8-10 cards, z spread 2000px, 3 s dolly
- **الدليل / proof:** `style:product`

#### CAM-337 · اهتزاز الكاميرا عند الارتطام · Impact camera shake · 👁 شوهد في فيديو
- **ماذا / what:** add noise2D(seed, t*freq) offsets to camera x/y with an exponentially decaying amplitude after each impact
- **أرقام / params:** amp 12 px, decay 250 ms, freq 25
- **الدليل / proof:** `style:stickman`

#### CAM-338 · تكوين خشبة مسرح جانبي · Stage-set side-view layout · 👁 شوهد في فيديو
- **ماذا / what:** single floor line, props spaced left-to-right as story stations (cause -> problem -> solution box), wall props for context, title top-centre
- **أرقام / params:** floor at 78% height
- **الدليل / proof:** `style:stickman`

#### CAM-339 · كاميرا واحدة لطبقتي SVG وHTML · Shared SVG+HTML camera transform · 👁 شوهد في فيديو
- **ماذا / what:** keyframes (x, y, zoom) with Easing.inOut(cubic) applied as one CSS transform to both the SVG drawing layer and the HTML text layer so they stay locked
- **أرقام / params:** zoom 1-2
- **الدليل / proof:** `style:whiteboard`

#### CAM-340 · مونتاج شبكي للهوية · Brand grid montage · 📄 موصوف
- **ماذا / what:** A multi-cell moving grid that mixes real UI moments with the brand's mark, palette and type so the product's range reads as one world.
- **كيف / how:** 2x2 grid for wide/square, vertical stack for 9:16, designed separately per ratio; each cell animates on its own clock but cuts are staggered so there is one dominant place to look; avoid simultaneous flashes, repeated footage, or several dark cells landing together; check every cell for blank frames at opening, each cut and closing.
- **أرقام / params:** 2x2 (16:9/1:1); vertical stack (9:16)
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/213-brand-grid-video/SKILL.md`

#### CAM-341 · التخطيط قبل التحريك · Layout-before-animation (hero frame first) · 📄 موصوف
- **ماذا / what:** Build the static layout of each scene's fullest moment first, then animate entrances with from() and exits with to(), so overlaps are caught before motion hides them.
- **كيف / how:** Scene container: width/height 100%, padding, flex column, gap, box-sizing border-box; absolute positioning only for decoratives; no <br> in running text (use max-width); then tl.from for entrances.
- **أرقام / params:** padding e.g. 120px 160px; gap 24px
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/SKILL.md`

#### CAM-342 · قواعد تكوين الكادر للفيديو · Video-frame composition rules · 📄 موصوف
- **ماذا / what:** Video frames are not web pages: fill the frame, keep three layers, give two focal points, anchor to edges, use split zones and structural rules.
- **كيف / how:** Hero text 60-80% of frame width; layers = background treatment + foreground + accents; radial glows/ghost type/hairlines instead of empty #000; structural lines scaleX from 0.
- **أرقام / params:** hero 60-80% width; >=3 layers; >=2 focal points
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/motion-principles.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/house-style.md`

#### CAM-343 · اختيار المنحنيات وسرعة ثابتة على المسار · Spline choice & arc-length speed · 📄 موصوف
- **ماذا / what:** Camera rails and object paths need the right curve family and arc-length reparameterization to move at constant world speed.
- **كيف / how:** Catmull-Rom to pass through waypoints, cubic Hermite when tangents known, Bezier when handles are the authoring tool; target C1 for smooth direction, C2 for smooth curvature; build cumulative-distance lookup table, map distance->t; never move a camera at constant t.
- **الدليل / proof:** `kosif-atlas/skills/2199-lvtd-skills/8088-game-smooth-curves-and-motion/SKILL.md`

#### CAM-344 · مسرح ثابت 16:9 · Fixed 16:9 stage · 📄 موصوف
- **ماذا / what:** Author at 1920x1080 and scale the whole stage to the viewport (letterbox allowed, never reflow); switch slides with visibility/opacity not display.
- **كيف / how:** viewport wrapper + transform scale(min(vw/1920, vh/1080)); nothing below 24px at stage size; split content instead of shrinking.
- **أرقام / params:** 1920x1080; min 24px
- **الدليل / proof:** `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/SKILL.md` · `kosif-atlas/skills/345-visuals/1241-html-deck/SKILL.md`

#### CAM-345 · شبكة 8 بكسل وقاعدة الزوايا المتداخلة · Layered 8px grid and nested radius rule · 📄 موصوف
- **ماذا / what:** Spacing from an 8px scale; inner radius equals outer radius minus inset; per-component type budget of at most three sizes and three weights; two families per piece.
- **كيف / how:** Apply as tokens in the HTML stage (1920x1080). Inspect computed styles before rendering.
- **أرقام / params:** spacing 8,16,24,32,40,48,64,80,96; outer 24 + inset 8 -> inner 16; outer 24 + inset 24 -> square; editorial hero 12/16/64px at 400/500/600; mobile display ~40px
- **الدليل / proof:** `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/references/layered-grid.md`

#### CAM-346 · تكوين غير متماثل يتجاوز الإطار · Asymmetric bleed composition · 📄 موصوف
- **ماذا / what:** Offset titles and let imagery bleed past containers; alternate dense and sparse beats so scale shifts create rhythm.
- **كيف / how:** e.g. margin-left 8.33% with margin-right -5vw on media; alternate full-bleed immersion beats with contained reading beats.
- **أرقام / params:** offset 8.33% (1/12 column); bleed -5vw
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14124-top-design`

#### CAM-347 · تقسيم مشهد العرض 15/65/20 · Demo scene zoning 15/65/20 · 📄 موصوف
- **ماذا / what:** A dependable layout for 1920x1080 demo scenes: title band top, hero media middle, footer/CTA bottom; one focal point per scene.
- **كيف / how:** HTML scene with three blocks; screenshots get 12px radius and shadow on a dark glow background.
- **أرقام / params:** title top 15%; hero 65%; footer 20%; title 48-72px/800; subtitle 24-32px/400; bullets 18-22px/600 pills
- **الدليل / proof:** `kosif-atlas/skills/166-demo-video/535-demo-video/references/scene-design-system.md`

#### CAM-348 · إعدادات تصوير بدون إظهار الوجه · Face-free camera setups · 📄 موصوف
- **ماذا / what:** Five repeatable framings for faceless creators: top-down (60-80 cm above desk), over-shoulder (1 m behind, shoulder +10 cm, tilted 15 deg down), below-chest frontal (1 m, chest height), object/space (30-50 cm at object height, no person), side hands (50 cm beside desk, desk +20 cm).
- **كيف / how:** Use in shot lists; check a 10 s test recording for faces reflected in monitors or windows; every shot states its story role.
- **أرقام / params:** 60-80 cm; 1 m/+10 cm/15 deg; 30-50 cm; 50 cm/+20 cm
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2448-akbun-vlog-shotsketch/SKILL.md`

#### CAM-349 · S01 مينيمال نظيف · S01 Minimal clean · 📄 موصوف
- **ماذا / what:** Wide negative space, one focal element, a single accent colour; gentle positional entrances, straight cuts and clear holds for reading. Cheap and clear; may feel too calm for a loud ad.
- **كيف / how:** One accent token in the KOSIF scene CSS, eased entrances, hard scene switches, holds sized to reading time.
- **أرقام / params:** cost low; e.g. MG-012 MG-016 MG-023 MG-044 MG-070 MG-120
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### CAM-350 · S06 سينمائي جوي · S06 Atmospheric cinematic · 📄 موصوف
- **ماذا / what:** Depth and layers, directed light, balanced frame; slow scene-driven moves and gradual reveals. Builds mood and anticipation; slower to deliver a direct offer and needs suitable plates.
- **كيف / how:** Layered plates with parallax depth, fog/light layers in screen blend, slow push; KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg)
- **أرقام / params:** cost medium-high; MG-007 MG-030 MG-056 MG-071 MG-072 MG-073 MG-079 MG-080
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### CAM-351 · S09 تحريري حديث · S09 Modern editorial · 📄 موصوف
- **ماذا / what:** Typographic grid, clear headlines, orderly photo composition; line reveals, measured cuts, moves between columns. Clear reading order and mature tone; depends on text formatting and long text needs more time.
- **كيف / how:** CSS grid columns, overflow-hidden line reveals, serif/sans pairing (Arabic: Naskh-style body + display headline); KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg)
- **أرقام / params:** cost low-medium; MG-012 MG-016 MG-020 MG-067 MG-068 MG-076 MG-089 MG-110
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### CAM-352 · MG-085 تكبير من الكل إلى الجزء · MG-085 Whole-to-part zoom with minimap · 📄 موصوف
- **ماذا / what:** The frame pushes into a specific part while a small locator map keeps the viewer oriented.
- **كيف / how:** 0-2 whole, 2-4 approach, 4-7 detail, 7-9 return; nested precomps/scale with a small position box (scaled clone with a rectangle indicator).
- **أرقام / params:** 9 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-explainers.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### CAM-353 · وظيفة كل لقطة · Shot-purpose ladder · 📄 موصوف
- **ماذا / what:** Every shot must do a job: wide shots establish space and situation, medium shots show action, close shots show decisions and details; a camera move needs a start, end, direction, speed and a reason; B-roll should add context, action or emotion rather than literally repeating the words; get varied co…
- **كيف / how:** Tag each storyboard row with shot size and purpose; drop rows without a purpose.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2446-akbun-vlog-prepared-devtalk/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2447-akbun-vlog-shootplan/SKILL.md`

#### CAM-354 · معايرة الشكل والخلفية للطبقات فوق الفيديو · Figure-ground calibration for overlays · 📄 موصوف
- **ماذا / what:** Push overlays forward and footage back with calibrated cues: scrim 10-20% for soft separation, 40-60% for modal-like focus, 70%+ for full focus; dim inactive content to 50-70% opacity while keeping it legible; shadow blur 2-4 px for slight lift, 8-12 px for floating; background blur is the strongest…
- **كيف / how:** CSS rgba scrims, backdrop-filter/blur and box-shadow in KOSIF scenes; ffmpeg boxblur/eq on the plate.
- **أرقام / params:** scrim 10-20/40-60/70%+; opacity 50-70%; shadow 2-4/8-12 px
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3816-figure-ground-cues/SKILL.md` · `kosif-atlas/skills/1503-universal-design-principles/3818-figure-ground-relationship/SKILL.md`

#### CAM-355 · تدقيق الزخرفة ونسبة الإشارة للضجيج · Decoration audit (signal-to-noise) · 📄 موصوف
- **ماذا / what:** For every border, tint, shadow, gradient, icon and repeated logo ask whether removing it loses information; keep separators that disambiguate, state colours, semantic colours and real elevation; decorative heading icons and repeated brand marks go (one mark per screen, plus an end card).
- **كيف / how:** Review pass on storyboard frames before animating.
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3838-snr-decoration-removal/SKILL.md`

#### CAM-356 · رندر عمودي أصلي بدلاً من القص · Native vertical render over crop · 📄 موصوف
- **ماذا / what:** For motion-graphics or game footage, render the 9:16 version natively (re-layout, zoom canvas) instead of cropping the 16:9, which halves resolution and loses the subject in motion.
- **كيف / how:** In HyperFrames/Remotion: separate composition 1080x1920 with its own layout; in game engines zoom canvas ~1.78x and expand aspect.
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/assembly-and-review.md` · `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/gotchas.md` · `kosif-atlas/skills/101-video-skills/213-brand-grid-video/SKILL.md`

#### CAM-357 · صورة داخل صورة وجنباً إلى جنب · Picture-in-picture and side-by-side · 📄 موصوف
- **ماذا / what:** Overlay a presenter/webcam over a screen capture, or stitch clips side by side / stacked for comparisons.
- **كيف / how:** overlay=W-w-40:H-h-40 with scaled+rounded (geq alpha or pre-made mask) PiP; hstack/vstack/xstack for comparisons; watermark overlay with format=rgba,colorchannelmixer=aa=0.6
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md`

#### CAM-358 · نص واحد في الإطار · One text-bearing object per frame · 📄 موصوف
- **ماذا / what:** Only one object carries copy at any moment, on a real surface rather than floating.
- **كيف / how:** Storyboard check: count text layers per frame ≤1 (excluding captions).
- **أرقام / params:** ≤1
- **الدليل / proof:** `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`

#### CAM-359 · هامش تمدد النص · Text expansion headroom · 📄 موصوف
- **ماذا / what:** Translated text can be 30-50% longer; layouts must not clip.
- **كيف / how:** Text boxes sized to 150% of source length; auto-fit font size with min floor.
- **أرقام / params:** 30-50%
- **الدليل / proof:** `kosif-atlas/skills/2329-localization-i18n-engineering/8940-i18n-foundations-and-icu/SKILL.md`

#### CAM-360 · التشابه الجشطالتي باللون · Gestalt similarity via colour · 📄 موصوف
- **ماذا / what:** Elements sharing hue read as a group; preattentive pop-out works only when colour is sparse.
- **كيف / how:** Colour only the one element the narration is about; keep others neutral.
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3813-color` · `kosif-atlas/skills/1503-universal-design-principles/3819-gestalt-similarity`

#### CAM-361 · التسلسل الهرمي باللون والدرجة · Hierarchy via colour and tone · 📄 موصوف
- **ماذا / what:** Use value (lightness) contrast before hue for hierarchy; signal-to-noise: emphasise little.
- **كيف / how:** Squint test on a frame; reduce competing accents.
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3821-hierarchy-color-and-tone` · `kosif-atlas/skills/1503-universal-design-principles/3840-snr-emphasis-economy`

#### CAM-362 · أنواع لقطات بدون وجه · Faceless shot types table · 📄 موصوف
- **ماذا / what:** Top-down 60-80cm above desk; over-shoulder 1m behind at shoulder+10cm tilted 15deg; chest-down 1m; object 30-50cm; side-hand 50cm at desk+20cm.
- **كيف / how:** Use as composition presets for B-roll briefs or for virtual cameras in 3D/2D scenes.
- **أرقام / params:** see distances
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2448-akbun-vlog-shotsketch`

#### CAM-363 · قاعدة 3-30-300 لمستويات الانتباه · 3-30-300 attention tiers · 📄 موصوف
- **ماذا / what:** Layout tiers by viewing time: 3 s overview, 30 s filtering/breakdown, 300 s detail. In video this becomes headline shot, breakdown shot, optional detail.
- **كيف / how:** Place the 3-second answer in the first reading position (top-left for Latin, top-right for Arabic RTL), group 3-5 breakdown visuals in the middle, push detail tables to the end or cut them. Lay out on an 8-px grid; Power BI default canvas 1664x936.
- **أرقام / params:** 3 s / 30 s / 300 s; 3-5 breakdowns; 8 px grid; 1664x936
- **الدليل / proof:** `kosif-atlas/skills/2354-power-platform/9080-report-visualization-design/SKILL.md` · `kosif-atlas/skills/3455-business-analytics/14162-kpi-dashboard-design/SKILL.md`

#### CAM-364 · شبكة 8px والأقطار المتداخلة · Spacing grid & nested radii rule · 📄 موصوف
- **ماذا / what:** 8px spacing grid (half-step 4 only when needed); inner radius = outer radius minus padding; no borders at rest, full-target hover; touch targets >= 44px; one focus ring.
- **كيف / how:** Tokens --sk-1..7; outer 18px -> 8px padding -> inner 10px; card 12px; pill 999px; focus 3px solid offset 2px.
- **أرقام / params:** 4/8/12/16/24/32/48 px; radii 10/12/18/999
- **الدليل / proof:** `kosif-earth-ci-fork/docs/design/SQC-IDENTITY-ar.md` · `kosif-earth-ci-fork/ui/ds/tokens.css:28`

#### CAM-365 · تكوين الفراغ لجهة النص العربي · RTL negative-space composition · 📄 موصوف
- **ماذا / what:** Generated hero art and clips are mirrored so subjects sit on the far (left) side and the right side stays empty for Arabic headlines; on phones the subject is re-centred via object-position.
- **كيف / how:** hflip in ffmpeg / mirror before export; prompt 'leave space for title'; object-position 83% center on narrow screens.
- **الدليل / proof:** `kosif-earth-ci-fork/docs/design/HIGGSFIELD_VISUALS_ar.md` · `kosif-earth-ci-fork/ui/art/brand/earth-intro-20261009.css:25`

#### CAM-366 · معايير دفع الكاميرا · Camera push norms · 📄 موصوف
- **ماذا / what:** Pushes and close-ups numbers.
- **كيف / how:** Apply as defaults while authoring; verify with kmotion measure/speed/sheet
- **أرقام / params:** push 1.5–3.1x over 30–70 f, peak ~5%/frame; 2–5x close-up per interaction
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`

#### CAM-367 · زووم نبضي · Dynamic zoom punch · 📄 موصوف
- **ماذا / what:** Alternate 1.0x and 1.10-1.15x framing during talking heads.
- **كيف / how:** timeline clip zoom or punch on off-beat
- **أرقام / params:** every 2.5-4 s; 1.10-1.15x
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/montage_grammar.md`

#### CAM-368 · قيادة البطل والحركة المعاكسة · Hero-led choreography + counter-motion · 📄 موصوف
- **ماذا / what:** Hero leads; one origin per group; counter-motion 20-30%; parallax speeds.
- **أرقام / params:** counter 20-30%; fg 1x, mid 0.5x, bg 0.2x
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### CAM-369 · كاميرا بحاوية واحدة · Single-container camera · 📄 موصوف
- **ماذا / what:** One transform on one container, one move at a time, still between events.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### CAM-370 · تكوين: Rule of thirds · Composition: Rule of thirds · 📄 موصوف
- **ماذا / what:** Composition rule for prompts/shots.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/seven-layer-anatomy.md`

#### CAM-371 · تكوين: Golden ratio/spiral · Composition: Golden ratio/spiral · 📄 موصوف
- **ماذا / what:** Composition rule for prompts/shots.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/seven-layer-anatomy.md`

#### CAM-372 · تكوين: Centred symmetry · Composition: Centred symmetry · 📄 موصوف
- **ماذا / what:** Composition rule for prompts/shots.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/seven-layer-anatomy.md`

#### CAM-373 · تكوين: Leading lines · Composition: Leading lines · 📄 موصوف
- **ماذا / what:** Composition rule for prompts/shots.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/seven-layer-anatomy.md`

#### CAM-374 · تكوين: Negative space · Composition: Negative space · 📄 موصوف
- **ماذا / what:** Composition rule for prompts/shots.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/seven-layer-anatomy.md`

#### CAM-375 · تكوين: Frame-within-frame · Composition: Frame-within-frame · 📄 موصوف
- **ماذا / what:** Composition rule for prompts/shots.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/seven-layer-anatomy.md`

#### CAM-376 · تكوين: Low-angle hero / high-angle vulnerability · Composition: Low-angle hero / high-angle vulnerability · 📄 موصوف
- **ماذا / what:** Composition rule for prompts/shots.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/seven-layer-anatomy.md`

#### CAM-377 · تكوين: Depth stacking · Composition: Depth stacking · 📄 موصوف
- **ماذا / what:** Composition rule for prompts/shots.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/seven-layer-anatomy.md`

#### CAM-378 · العدسات · Lens list · 📄 موصوف
- **ماذا / what:** 14mm to 200mm + anamorphic 40mm.
- **أرقام / params:** 14, 24 f/1.4, 35 f/1.4, 50 f/1.2, 85 f/1.4, 100 macro, 135 f/2, 200 f/2.8
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/visual-catalog.md`

#### CAM-379 · أحجام اللقطات والزوايا · Shot sizes + angles · 📄 موصوف
- **ماذا / what:** ECU..insert; eye/low/high/drone/Dutch/worm/bird/POV.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/visual-catalog.md`

#### CAM-380 · حركات الكاميرا · Camera motion vocabulary · 📄 موصوف
- **ماذا / what:** static, pan, tilt, dolly, truck, pedestal, zoom, orbit, handheld, Steadicam, prose motion for models.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/visual-catalog.md`

#### CAM-381 · قائمة قواعد التكوين · Composition rule menu · 📄 موصوف
- **ماذا / what:** Named composition systems to pick per shot.
- **كيف / how:** Choose one: rule of thirds, golden ratio/spiral, centred symmetry (Wes Anderson), leading lines, negative space, frame within frame, low-angle hero / high-angle vulnerability, depth stacking (foreground/mid/background).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/seven-layer-anatomy.md`

#### CAM-382 · قائمة الاستمرارية · Continuity checklist (180-degree rule etc.) · 📄 موصوف
- **ماذا / what:** Pass to run before delivering any multi-shot sequence.
- **كيف / how:** Same lock text; same light direction and Kelvin; wardrobe damage persists; same time of day; props in the same hand; screen direction (180-degree rule); same aspect and frame rate.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/continuity-protocols.md`

#### CAM-383 · كتالوج العدسات · Lens catalog and focal-length meaning · 📄 موصوف
- **ماذا / what:** Focal lengths with their storytelling effect.
- **كيف / how:** Wide = more environment and distortion; long = compression and isolation.
- **أرقام / params:** 14mm; 24mm f/1.4; 35mm f/1.4; 50mm f/1.2; 85mm f/1.4; 100mm macro; 135mm f/2; 200mm f/2.8; anamorphic 40mm (oval bokeh, horizontal flare); 300mm+ wildlife
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/visual-catalog.md` · `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/prompt-library.md`

#### CAM-384 · مفردات اللقطات والزوايا وحركة الكاميرا · Shot sizes, angles and camera-move vocabulary · 📄 موصوف
- **ماذا / what:** Complete vocabulary for describing framing and motion, each move tagged with its emotional use.
- **كيف / how:** Pick size + angle + move per shot in the shot list.
- **أرقام / params:** Sizes ECU, CU, MCU, MS, full, wide, extreme wide, POV, OTS, two-shot, insert. Angles eye level, low (hero), high (vulnerable), drone top-down, Dutch (unease), worm's-eye, bird's-eye. Moves static/locked-off, pan, tilt, dolly in/out, truck, pedestal, zoom, orbit/arc (hero), crane up/down (scale), han…
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/visual-catalog.md` · `kosif-one/tools/kosif-omni/skills/kosif-video/SKILL.md` · `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/prompt-library.md`

#### CAM-385 · قواعد التكوين للفيديو · Video composition rules · 📄 موصوف
- **ماذا / what:** Two focal points, title 60-80% of width, three layers (living bg, content, accents), anchor to edges, never pure black empty bg.
- **كيف / how:** Apply in DESIGN.md before motion.
- **أرقام / params:** title 60-80% width; text 40px+ at 1080p; tracking -0.03em; weights 300 vs 900
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/references/motion-rules.md`

#### CAM-386 · التخطيط قبل الحركة · Layout-before-motion (hero frame) · 📄 موصوف
- **ماذا / what:** Place every element at its clearest moment as static CSS, then animate from/to it.
- **كيف / how:** Build hero frame per scene, then gsap.from entrance and .to exit.
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/references/motion-rules.md`

#### CAM-387 · منع النمو في المكان · No grow-in-place hero entrance · 📄 موصوف
- **ماذا / what:** Hero entrances combine position, rotation, blur and scale and start >=0.35 stage width away; distances as fractions of width.
- **أرقام / params:** 0.35 W
- **الدليل / proof:** `100-superskills/skills/motion-director-pro/references/motion-floor.md`

#### CAM-388 · ميزانية الكاميرا · Named camera events budget · 📄 موصوف
- **ماذا / what:** 2-3 named timed camera moves; hold between; no constant drift/orbit; budget 60% object transforms, 20% surface/light, 20% camera; fill every camera lock with acting object.
- **أرقام / params:** 60/20/20
- **الدليل / proof:** `100-superskills/skills/motion-director-pro/SKILL.md` · `100-superskills/skills/motion-director-pro/references/motion-floor.md`

#### CAM-389 · تحكم كاميرا Kling · Kling camera control reference · 📄 موصوف
- **ماذا / what:** Vendored atlas skill excerpt for Kling camera control parameters.
- **كيف / how:** read references/sources.md
- **الدليل / proof:** `100-superskills/skills/cinema-director-7layers/references/sources.md`

#### CAM-390 · قواعد الكاميرا ثنائية الأبعاد · 2D camera rules · 📄 موصوف
- **ماذا / what:** Virtual camera behaviour in 2D/2.5D films.
- **كيف / how:** MOTION.breathe/push/camera; one transform on one container.
- **أرقام / params:** no handheld shake in 2D; holds creep ~4%/s or drift .3-2.5 px/f; pushes 1.5-3.1× over 30-70 f, peak ~5%/frame; every interaction gets a 2-5× close-up; one move at a time; still between events; 3D: one continuous camera, DOF on look target, one tilted object per act
- **الدليل / proof:** `kosif-studio/motion/references/craft-numbers.md` · `kosif-studio/motion/references/motion-craft.md`

#### CAM-391 · قواعد التكوين للوحات · Composition rules for painted stills · 📄 موصوف
- **ماذا / what:** One strong diagonal between hero and antagonist, scale contrast, calm empty space around the action, far = softer and bluer, near = sharp, no black outlines unless cartoon is intended.
- **كيف / how:** Plan the scene back-to-front (sky, clouds, far, mid, hero, effects, atmosphere) then check.
- **أرقام / params:** far edges blur 1-3
- **الدليل / proof:** `kosif-studio/references/drawing-guide.md:62` · `kosif-studio/references/drawing-guide.md:82`

#### CAM-392 · مفردات حركة الكاميرا · Camera move vocabulary · 📄 موصوف
- **ماذا / what:** PLAN keys: static, push-in, pull-back, pan, tilt, orbit, rack-focus; STYLE defaults: opening push-in 100->108% ease-out, pans ≤20% of frame, closing pull-back 105->100%.
- **كيف / how:** PLAN.md scene table Camera column
- **الدليل / proof:** `kosif-tool/templates/PLAN.md` · `kosif-tool/templates/STYLE.md`

#### CAM-393 · إعدادات العدسة وزاوية الرؤية · Lens / FOV presets · 📄 موصوف
- **ماذا / what:** Natural shots vs product close-ups mapped to Three.js field of view.
- **كيف / how:** PerspectiveCamera(fov,...)
- **أرقام / params:** 35–50 mm ≈ fov 40–55°; 85 mm ≈ fov 24° for product close-up; sample fov 45, near 0.1, far 100
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:18` · `kosif-tool/playbooks/3d.md:58`

#### CAM-394 · نسب البارالاكس للطبقات · 2.5D parallax depth ratios · 📄 موصوف
- **ماذا / what:** Layer speed inversely proportional to depth for planar parallax.
- **كيف / how:** offset_layer = camera_offset × factor.
- **أرقام / params:** foreground 1.0, mid 0.5, background 0.15
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:27`

#### CAM-395 · عمق ميدان مزيف · Fake depth of field · 📄 موصوف
- **ماذا / what:** Avoid expensive DOF by blurring a background layer in 2.5D.
- **كيف / how:** CSS/Canvas filter blur on background plate.
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:29`

#### CAM-396 · حدود كاميرا الرسوم · Chart camera limits · 📄 موصوف
- **ماذا / what:** Gentle camera on tabular info.
- **أرقام / params:** push ≤ 4% per scene (~0.5%/s); pan ≤ 40 px/s; rotation ±0.5°; no shake
- **الدليل / proof:** `kosif-tool/playbooks/charts.md:42`

#### CAM-397 · كاميرا فصول المخطط · Diagram camera chapters · 📄 موصوف
- **ماذا / what:** Pan between chapters; zoom limits; hold after moves.
- **أرقام / params:** 700–1000 ms cubic-bezier(0.65,0,0.35,1); zoom 1.0→1.4, max 1.8; hold 1.5 s
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:30`

#### CAM-398 · حجم الجهاز لكل نسبة · Device scale per aspect · 📄 موصوف
- **ماذا / what:** Device frame share by aspect ratio.
- **أرقام / params:** 9:16 55–70% height; 16:9 75–85% on a third line; 1:1 70%
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:25`

#### CAM-399 · القص الآمن للجهاز · Device safe crops · 📄 موصوف
- **ماذا / what:** Text margins; never crop through island/camera/home indicator; keep one vertical edge in push-ins.
- **أرقام / params:** 5% sides; 12% top/bottom; bleed bottom only if lower 20% of screen non-essential
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:27`

#### CAM-400 · دفع الكاميرا والتقريب عند النقر · Device camera push and tap dolly · 📄 موصوف
- **ماذا / what:** Slow push during holds; dolly toward tapped element.
- **أرقام / params:** push 1.00→1.06 over 3–4 s sine; dolly 1.00→1.12 in 600 ms, back over 900 ms
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:40`

#### CAM-401 · كاميرا واحدة لكل تسلسل · One camera rig per sequence · 📄 موصوف
- **ماذا / what:** All photos in a scene share one rig transform so cuts feel like one operator.
- **أرقام / params:** rotate ≤ 1°
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:17`

#### CAM-402 · حدود تأطير البورتريه · Portrait framing limits · 📄 موصوف
- **ماذا / what:** Eyes in top third; limited push into faces; 9:16 subject on vertical third.
- **أرقام / params:** face push ≤ 1.08×; pan ≤ 6% width; push ≤ 12%
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:24-25`

#### CAM-403 · أرقام تأطير الشاشة · Screen framing numbers · 📄 موصوف
- **ماذا / what:** Device-free screen width share, arrival rotation; vertical travel on 9:16; callouts outside screen.
- **أرقام / params:** 16:9 72–84% width; ≤ 6° rotation on arrival only
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:21`

#### CAM-404 · كاميرا بتحويل مجموعة واحد · CameraRig single group transform · 📄 موصوف
- **ماذا / what:** One transform drives push/pan/focus per scene; build at 2× for zooms >1.4×.
- **كيف / how:** starters/remotion CameraRig or one ctx.setTransform; render --scale 2.
- **أرقام / params:** zoom > 1.4× → 2×
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:22`

#### CAM-405 · عقد تسليم الحركة · Motion handoff contract · 📄 موصوف
- **ماذا / what:** Every leg ends ~1 s in slow forward drift and next begins continuing it; reversals only inside a leg.
- **كيف / how:** Verbatim clauses in leg prompts.
- **أرقام / params:** final ~1 s
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md`

#### CAM-406 · مسافات معتمدة · Spacing token set · 📄 موصوف
- **ماذا / what:** Only 0,2,4,8,12,16,24,32,40,48,64,80,96 px; buttons 8x12 px.
- **الدليل / proof:** `kosif-one/vendor/ai-design-skills/skills/landing-page-design/SKILL.md:199`

#### CAM-407 · اهتزاز 2 بكسل · 2-px screen shake once · 💡 فكرة
- **ماذا / what:** Single impact shake as integer offset.
- **كيف / how:** Translate stage by ±2 px for 3 frames.
- **أرقام / params:** 2 px, 3 frames, once
- **الدليل / proof:** `style:pm-0xevinho-3777d8`

#### CAM-408 · دفع مع اهتزاز يدوي · Push + handheld drift camera · 💡 فكرة
- **ماذا / what:** Slow push per beat plus sinusoidal drift; straight cuts on sound hits.
- **كيف / how:** scale 1.0→1.05 per beat; offset 4*sin(2π·0.5·t).
- **أرقام / params:** ±4 px @0.5 Hz
- **الدليل / proof:** `style:pm-abderrahmen-g-9e8ed0`

#### CAM-409 · شبكة ثابتة للمحاذاة · Persistent snap grid · 💡 فكرة
- **ماذا / what:** Visible grid in every shot; elements rest on grid cells.
- **كيف / how:** Background grid layer; snap rest positions.
- **أرقام / params:** 24 px cells @1080p, 8% opacity
- **الدليل / proof:** `style:pm-ajith-io-ea7f2d`

#### CAM-410 · دفع بطيء للكاميرا · Gentle camera push/pan · 💡 فكرة
- **ماذا / what:** Continuous slow pushes or small pans, no whip/rotation.
- **كيف / how:** Stage transform.
- **أرقام / params:** 3-5% scale/scene or <80 px pan
- **الدليل / proof:** `style:pm-aschapmann-131210`

#### CAM-411 · دولي في الكورس · Chorus dolly · 💡 فكرة
- **ماذا / what:** Only the camera eases: one dolly-in per chorus.
- **كيف / how:** eased scale.
- **أرقام / params:** 6% per chorus
- **الدليل / proof:** `style:pm-davidshulmanfl-371638`

#### CAM-412 · كاميرا تتبع متأخرة · Ball-tracking lag camera · 💡 فكرة
- **ماذا / what:** Camera follows subject with lag and overshoot then recentres.
- **كيف / how:** Lagged follow + bezier recentre.
- **أرقام / params:** 120 ms lag; 15% overshoot; (0.2,0.9,0.3,1)
- **الدليل / proof:** `style:pm-deifosv-04e4d3`

#### CAM-413 · شريط سينمائي · 2.35:1 letterbox · 💡 فكرة
- **ماذا / what:** Cinematic letterbox inside 16:9; dolly only.
- **كيف / how:** Black bars.
- **أرقام / params:** ≤2%/s scale, ease-in-out sine
- **الدليل / proof:** `style:pm-kamstudiolabs-0b0824`

#### CAM-414 · تقريب وذروة · Climax zoom and hit shake · 💡 فكرة
- **ماذا / what:** Zoom when 3 rings remain, decaying shake per hit.
- **أرقام / params:** 1.0→1.25 over 3 s; 2 px shake 100 ms
- **الدليل / proof:** `style:pm-kantamk-61f410`

#### CAM-415 · كاميرا 2.5D · 2.5D parallax UI camera · 💡 فكرة
- **ماذا / what:** Pans and one push; flat UI rotates ≤8° in 3D.
- **أرقام / params:** push 1.0→1.08; ≤8°; UI sizes 14/16/24/40 px
- **الدليل / proof:** `style:pm-melvynx-6cde6c`

#### CAM-416 · زوم صادم لحظي · Single-frame punch-in · 💡 فكرة
- **ماذا / what:** Scale jumps in one frame then relaxes.
- **كيف / how:** Set scale 1.15 at hit frame, interpolate back easeOutExpo.
- **أرقام / params:** 1.00->1.15 in 1 frame; relax 350 ms easeOutExpo
- **الدليل / proof:** `style:pm-micheleharmonic-77628e`

#### CAM-417 · زوم نفقي ثابت · Constant-rate tunnel zoom · 💡 فكرة
- **ماذا / what:** Inward zoom toward pupil at exponential constant rate.
- **كيف / how:** scale=2^(t/2.5); ease only start/end.
- **أرقام / params:** doubles every 2.5 s; 600 ms ease-in-out ends
- **الدليل / proof:** `style:pm-monokern-ade5b6`

#### CAM-418 · كاميرا ثابتة ودفعتان · Static cam with two push-ins · 💡 فكرة
- **ماذا / what:** Only two small push-ins.
- **أرقام / params:** 4% push, 2 s each
- **الدليل / proof:** `style:pm-mrtanviir-132457`

#### CAM-419 · عمق بالمقياس والظل · Locked cam, depth by scale+shadow · 💡 فكرة
- **ماذا / what:** scale 0.92->1.00 plus 24 px drop shadow.
- **الدليل / proof:** `style:pm-ratheejaisal-1f4538`

#### CAM-420 · بارالاكس طبقتين · Two-layer grid parallax · 💡 فكرة
- **ماذا / what:** background grid at 0.5 speed; grid scale 0.92->1
- **أرقام / params:** accent <=25%
- **الدليل / proof:** `style:pm-robvjourney-ce3e1a`

#### CAM-421 · لقطة واحدة · One-shot slow push · 💡 فكرة
- **ماذا / what:** scale 1.00->1.06 over 30 s
- **الدليل / proof:** `style:pm-sarut0bisasuke-cefa43`

## إضافات v2 — v2 additions

_قدرات أُضيفت في الإصدار الثاني من حزم المالك (higgsfield-motion-saas وhiggsfield-motion-claude ومهارة المونتاج التحريرية وفيلم الأغنية وKOSIF SEE) ومن مهارات ECC (رخصة MIT)، مكتوبة بكلماتنا. ✅ هنا = شُغّلت في جلسة 2026-10-16 وسجلها في [external-skills.md](../external-skills.md)؛ مسارات `owner-upload:` تشير إلى أرشيفات المالك لا إلى هذا المستودع. — v2 additions from the owner's packages and ECC skills (MIT), in our own words; ✅ = run in this session, log in external-skills.md; `owner-upload:` paths point into the owner's archives, not this repo._

#### CAM-X01 · الكاميرا داخل المشاهد فقط · Camera lives inside scenes, neutral in transition windows · 📄 موصوف / documented only
- **ماذا / what:** حركة الكاميرا تحدث داخل المشهد وتعود محايدة في نافذة الانتقال، وتُبنى مفاتيحها كفروق مجمّعة. — Camera moves happen inside scenes and return to neutral in transition windows; their keys are stacked deltas.
- **متى أستخدمها / when:** أي فيلم ثنائي ونصف الأبعاد أو واجهات بكاميرا افتراضية — any 2.5D or UI film with a virtual camera.
- **كيف / how:** Orbits ry ≤ 2.5°, rx ≤ 1.6°; pushes ×1.02–1.09; key the camera as summed deltas on stacked nulls; counter-transform HUD chrome so it stays flat; open on a tilted pose {s 1.12, rx 14, ry −11, rz −1.5} and settle frontal over 1.4 s with bezier(.3,.3,.15,1). Depth of field on DOM layers: blur = min(18, k·|1 − D/depth|) with k 6–10; camera-move blur via feGaussianBlur = half-frame travel × 0.32, max 44 px. **أرقام / params:** orbit ≤ 2.5°/1.6°; push ×1.02–1.09; DOF blur ≤ 18 px; move blur ≤ 44 px.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`

#### CAM-X02 · حركات كاميرا لها دافع · Motivated camera moves table · 📄 موصوف / documented only
- **ماذا / what:** كل حركة كاميرا تتبع حدثًا: مؤشر كتابة، تصدير، انفجار نتائج. — Every camera move follows an event: a typing caret, an export, a burst of results.
- **متى أستخدمها / when:** عرض منتج تتحرك فيه الكاميرا داخل واجهة واحدة — a product demo where the camera travels inside one UI.
- **كيف / how:** Follow the caret: +290 px with rx 11°; crane back: distance +1450 with rx 20°; pull out on export: D × 1.62; on a burst of results: D × 2.5. Always counter-transform the HUD; never move the camera at peak velocity while text is animating. **أرقام / params:** follow +290 px rx 11°; crane +1450 rx 20°; export ×1.62; burst ×2.5.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md` · `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`

#### CAM-X03 · فيلم علامة بكاميرا واحدة · Single-camera brand film · 📄 موصوف / documented only
- **ماذا / what:** فيلم علامة يُروى بحركة كاميرا مهيمنة واحدة وينتهي بدفع بطيء نحو العلامة لا يتراجع أبدًا. — A brand film told with one dominant camera verb that ends on a slow push toward the brand and never retreats.
- **متى أستخدمها / when:** فيلم علامة قصير بلا قطع كثيرة — a short brand film with few cuts.
- **كيف / how:** One dominant verb (push, orbit or travel); every push ≥ 1.14× (smaller reads static); no peak camera velocity while text animates; end on a slow push toward the brand; a one-to-many carousel uses about 13 cards ~28° apart turning ~200°. Depth comes from a motivated camera over flat designed layouts, not from tilting UI into 3D. **أرقام / params:** push ≥ 1.14×; carousel 13 cards × 28°, ~200° turn.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`
- **الدليل / proof:** `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`
