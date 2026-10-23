# الانتقالات والقطعات — Transitions & cuts

> فصل مُجمَّع آليًا من 475 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **460 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 460 powers deduplicated by name from 475 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 27 · 🟢 جاهز 58 · 📦 بأمر تثبيت 175 · 🔑 مفتاح/خدمة 1 · 👁 شوهد في فيديو 114 · 📄 موصوف 79 · 💡 فكرة 18 · المجموع / total 472

**إضافات v2 — v2 additions:** TRANS-X01 … TRANS-X12 (12) — في آخر الفصل / at the end of this chapter.

## الفهرس / contents
_الإدخالات مرتبة من الأقوى دليلًا؛ ابحث بالمعرّف أو استخدم_ `python3 scripts/powers.py family <family>` _— entries are ordered strongest evidence first; jump by ID or use the CLI._
- ✅ مُثبت هنا: TRANS-01 … TRANS-27 (27)
- 🟢 جاهز: TRANS-28 … TRANS-85 (58)
- 📦 بأمر تثبيت: TRANS-86 … TRANS-260 (175)
- 🔑 مفتاح/خدمة: TRANS-261 … TRANS-261 (1)
- 👁 شوهد في فيديو: TRANS-262 … TRANS-375 (114)
- 📄 موصوف: TRANS-376 … TRANS-442 (67)
- 💡 فكرة: TRANS-443 … TRANS-460 (18)
- 📄 موصوف: TRANS-X01 … TRANS-X12 (12)
- إضافات v2 — v2 additions
- إضافات v3 — v3 additions
- **من أكبر مستودعات GitHub — from the top GitHub repositories (2026-10-23)** — TRANS-G01 (1)

#### TRANS-01 · انتقال تطبيقات الموبايل: غمس للأسود · Phone-editor transition: dipblack · ✅ مُثبت هنا
- **ماذا / what:** Custom transition modelling what CapCut/InShot do: dip to black.
- **كيف / how:** mm_transitions.render('dipblack', A, B, P, **params) (custom kinds need OpenCV or SciPy here).
- **أرقام / params:** mid 0.5
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1` · `100-superskills/skills/kosif-mimic/scripts/mm_transitions.py:26`

#### TRANS-02 · انتقال تطبيقات الموبايل: غمس للأبيض · Phone-editor transition: dipwhite · ✅ مُثبت هنا
- **ماذا / what:** Custom transition modelling what CapCut/InShot do: dip to white.
- **كيف / how:** mm_transitions.render('dipwhite', A, B, P, **params) (custom kinds need OpenCV or SciPy here).
- **أرقام / params:** mid 0.5
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1` · `100-superskills/skills/kosif-mimic/scripts/mm_transitions.py:26`

#### TRANS-03 · انتقال تطبيقات الموبايل: فلاش أبيض · Phone-editor transition: flash · ✅ مُثبت هنا
- **ماذا / what:** Custom transition modelling what CapCut/InShot do: white flash cut (phone editors).
- **كيف / how:** mm_transitions.render('flash', A, B, P, **params) (custom kinds need OpenCV or SciPy here).
- **أرقام / params:** peak 0.5, width 0.25 or 0.5
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1` · `100-superskills/skills/kosif-mimic/scripts/mm_transitions.py:26`

#### TRANS-04 · إضافة خطاف في البداية مع استمرار الموسيقى · Prepend hook while music stays continuous · ✅ مُثبت هنا
- **ماذا / what:** When a hook is inserted at the head, picture, subtitles and location sound shift by the hook length while the music bed stays in place so it plays uninterrupted from frame 0; afterwards the first music clip is extended by the hook length so later music edits realign with scenes; hook audio lives on …
- **كيف / how:** Resolve version: duplicate timeline, lock BGM track (SetTrackLock), ripple-insert space, append nested hook segments with AppendToTimeline(startFrame,endFrame), drop markers. Local version: ffmpeg concat hook+main video, keep the original music file continuous from 0 with amix and adjust its trim; never alter the user's dialogue track.
- **أرقام / params:** hook <=45 s; chapters >=10 s apart
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/scripts/searchhook.py`

#### TRANS-05 · عتبات قص الصمت والحشو · Silence and filler cut thresholds · ✅ مُثبت هنا
- **ماذا / what:** Word gaps over 0.7 s are cut candidates; keep about 0.4 s breath at sentence ends; preserve 0.8-2 s intentional pauses after turning points, decisions, failures or realizations; remove filler-only segments; do not cut an in-sentence filler when neighbouring gaps are under 0.15 s (audible stutter).
- **كيف / how:** Detect with ffmpeg -af silencedetect=n=-35dB:d=0.7 and word timestamps; record preserved pauses with a reason; shrink picture by the same amount to keep sync.
- **أرقام / params:** gap >0.7 s; breath 0.4 s; keep 0.8-2 s pauses; filler guard 0.15 s; -35 dB
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2453-davinciresolve-cut-devtalk/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2460-davinciresolve-story-devtalk/SKILL.md`

#### TRANS-06 · مكتبة انتقالات xfade · xfade transition palette · ✅ مُثبت هنا
- **ماذا / what:** ffmpeg's xfade filter gives ~58 built-in transitions between two clips without any editor: fades, wipes, slides, circle/rect crops, pixelize, radial, slices, wind, cover/reveal, zoomin, squeeze.
- **كيف / how:** [0:v][1:v]xfade=transition=NAME:duration=D:offset=(len0-D)[v]; pair with acrossfade=d=D for audio. Names available locally: fade wipeleft/right/up/down slideleft/right/up/down circlecrop rectcrop distance fadeblack fadewhite radial smoothleft/right/up/down circleopen circleclose vertopen vertclose horzopen horzclose dissolve pixelize diagtl/tr/bl/br hlslice hrslice vuslice vdslice hblur fadegrays wipetl/tr/bl/br squeezeh squeezev zoomin fadefast fadeslow hlwind hrwind vuwind vdwind coverleft/rig…
- **أرقام / params:** dissolve 12-20 frames for time/place change; 0.4 s seam for loops
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/assets/marketing/render.py` · `kosif-atlas/skills/1096-akbun-editvideo/2454-davinciresolve-cut-travelflow/SKILL.md`

#### TRANS-07 · دخول المشهد عند تغيير الشاشة · Scene enter on view change · ✅ مُثبت هنا
- **ماذا / what:** Each view remounts inside a keyed stage that fades and rises with a hairline scale-up, then focus moves to the workspace without scrolling.
- **كيف / how:** React: <div key={view} className='view-stage'>; keyframe kosif-scene-enter; requestAnimationFrame(() => main.focus({preventScroll:true})).
- **أرقام / params:** 420ms ease-cinematic; translate3d(0,10px,0) scale(0.996) -> 0/1; opacity 0->1
- **الدليل / proof:** `kosif-audit-pro/components/kosif/app-shell.tsx:216` · `kosif-audit-pro/app/globals.css:595` · `kosif-audit-pro/app/globals.css:637`

#### TRANS-08 · مكتبة انتقالات الكينتك · Kinetic transition library (17) · ✅ مُثبت هنا
- **ماذا / what:** Named clip-to-clip handoffs, one per theme: soft blur-dissolve + grey arc; white flash; blur-dissolve + zoom-out; horizontal light-streak sweep; gold light leak; full-red panel; round iris wipe + zoom; leaf-shadow sweep; cobalt light sweep; glitch cut + whip-slide; sunburst stripe wipe; light-flare …
- **كيف / how:** Chosen theme's transition is written into the FINAL SECOND of each clip prompt and the join instructions.
- **أرقام / params:** 17 transitions
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:4-20,115,118`

#### TRANS-09 · تسليم بوضعية مطابقة · Matching exit-pose handoff · ✅ مُثبت هنا
- **ماذا / what:** Each clip ends in an identifiable pose/state that the next clip starts from, enabling invisible joins between AI clips.
- **كيف / how:** Written into stickman video prompts, food ('hold the state as the opening reference'), fitness (return to pose, action match cut).
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/stickman.mjs:36` · `fastify-motion-bro/scripts/profiles/food-flow.mjs:95` · `fastify-motion-bro/scripts/profiles/fitness.mjs:32`

#### TRANS-10 · انتقالات xfade في التايملاين · FFmpeg xfade transitions in the timeline · ✅ مُثبت هنا
- **ماذا / what:** JSON timelines use FFmpeg xfade transitions with Arabic labels; unknown names are rejected.
- **كيف / how:** timeline.transitions() includes fade, circleopen (not 'custom'); transition_ar('fadeblack') = 'عبر الأسود'; clip {transition:{type:'circleopen', dur:.4}} or 'slideup'; build graph contains xfade=transition=circleopen.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:47` · `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:64`

#### TRANS-11 · إظلام قصير بين القطعات · Micro dip between hard cuts · ✅ مُثبت هنا
- **ماذا / what:** Every segment fades from and to black for a few frames so the concatenated cuts breathe instead of popping.
- **كيف / how:** fade=t=in:st=0:d=0.17,fade=t=out:st=DUR-0.17:d=0.17 in each segment's filter chain before concat (no xfade needed, so concat can stream-copy).
- **أرقام / params:** 0.17 s in + 0.17 s out (about 4 frames at 24 fps)
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/tools/render_ghorba_preview.py:140`

#### TRANS-12 · تصنيف الانتقال بإعادة التركيب · Transition classification by re-synthesis · ✅ مُثبت هنا
- **ماذا / what:** Each detected transition is identified by re-rendering candidate kinds and fitting their progress curve to the real frames, then replayed with the same kind and curve.
- **كيف / how:** mm_analyze classify + mm_transitions.render(kind, A, B, P, **params) with PARAM_GRID search.
- **أرقام / params:** P: 1.0 = all A ... 0.0 = all B
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_analyze.py` · `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1`

#### TRANS-13 · تلاشي وذوبان · Fades and dissolves (xfade) · ✅ مُثبت هنا
- **ماذا / what:** FFmpeg xfade transitions ported formula-for-formula to numpy so a detected one replays exactly: crossfade, through black/white/grey, pixel dissolve.
- **كيف / how:** mm_transitions.render(kind, A, B, P) in Python, or ffmpeg -filter_complex xfade=transition=<kind>:duration=D:offset=O directly.
- **أرقام / params:** fade, fadeblack, fadewhite, fadegrays, fadefast, fadeslow, dissolve, distance
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1`

#### TRANS-14 · مسح · Wipes (xfade) · ✅ مُثبت هنا
- **ماذا / what:** FFmpeg xfade transitions ported formula-for-formula to numpy so a detected one replays exactly: hard-edge wipes incl. diagonal corners.
- **كيف / how:** mm_transitions.render(kind, A, B, P) in Python, or ffmpeg -filter_complex xfade=transition=<kind>:duration=D:offset=O directly.
- **أرقام / params:** wipeleft, wiperight, wipeup, wipedown, wipetl, wipetr, wipebl, wipebr
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1`

#### TRANS-15 · سحب · Slides (xfade) · ✅ مُثبت هنا
- **ماذا / what:** FFmpeg xfade transitions ported formula-for-formula to numpy so a detected one replays exactly: push the old shot out.
- **كيف / how:** mm_transitions.render(kind, A, B, P) in Python, or ffmpeg -filter_complex xfade=transition=<kind>:duration=D:offset=O directly.
- **أرقام / params:** slideleft, slideright, slideup, slidedown
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1`

#### TRANS-16 · مسح ناعم · Smooth wipes (xfade) · ✅ مُثبت هنا
- **ماذا / what:** FFmpeg xfade transitions ported formula-for-formula to numpy so a detected one replays exactly: soft-edged wipes.
- **كيف / how:** mm_transitions.render(kind, A, B, P) in Python, or ffmpeg -filter_complex xfade=transition=<kind>:duration=D:offset=O directly.
- **أرقام / params:** smoothleft, smoothright, smoothup, smoothdown
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1`

#### TRANS-17 · دوائر ومستطيلات · Circle and rect shapes (xfade) · ✅ مُثبت هنا
- **ماذا / what:** FFmpeg xfade transitions ported formula-for-formula to numpy so a detected one replays exactly: iris-style shape transitions and clock wipe.
- **كيف / how:** mm_transitions.render(kind, A, B, P) in Python, or ffmpeg -filter_complex xfade=transition=<kind>:duration=D:offset=O directly.
- **أرقام / params:** circleopen, circleclose, circlecrop, rectcrop, radial
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1`

#### TRANS-18 · أبواب تنفتح · Barn doors (xfade) · ✅ مُثبت هنا
- **ماذا / what:** FFmpeg xfade transitions ported formula-for-formula to numpy so a detected one replays exactly: split open/close.
- **كيف / how:** mm_transitions.render(kind, A, B, P) in Python, or ffmpeg -filter_complex xfade=transition=<kind>:duration=D:offset=O directly.
- **أرقام / params:** vertopen, vertclose, horzopen, horzclose
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1`

#### TRANS-19 · قطري · Diagonals (xfade) · ✅ مُثبت هنا
- **ماذا / what:** FFmpeg xfade transitions ported formula-for-formula to numpy so a detected one replays exactly: diagonal reveals.
- **كيف / how:** mm_transitions.render(kind, A, B, P) in Python, or ffmpeg -filter_complex xfade=transition=<kind>:duration=D:offset=O directly.
- **أرقام / params:** diagtl, diagtr, diagbl, diagbr
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1`

#### TRANS-20 · شرائح · Slices (xfade) · ✅ مُثبت هنا
- **ماذا / what:** FFmpeg xfade transitions ported formula-for-formula to numpy so a detected one replays exactly: venetian slice transitions.
- **كيف / how:** mm_transitions.render(kind, A, B, P) in Python, or ffmpeg -filter_complex xfade=transition=<kind>:duration=D:offset=O directly.
- **أرقام / params:** hlslice, hrslice, vuslice, vdslice
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1`

#### TRANS-21 · تغطية وكشف · Cover and reveal (xfade) · ✅ مُثبت هنا
- **ماذا / what:** FFmpeg xfade transitions ported formula-for-formula to numpy so a detected one replays exactly: new shot slides over / old shot slides off.
- **كيف / how:** mm_transitions.render(kind, A, B, P) in Python, or ffmpeg -filter_complex xfade=transition=<kind>:duration=D:offset=O directly.
- **أرقام / params:** coverleft, coverright, coverup, coverdown, revealleft, revealright, revealup, revealdown
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1`

#### TRANS-22 · ضغط وزووم وبكسلة · Squeeze, zoom, pixelize, blur (xfade) · ✅ مُثبت هنا
- **ماذا / what:** FFmpeg xfade transitions ported formula-for-formula to numpy so a detected one replays exactly: stylised xfade kinds.
- **كيف / how:** mm_transitions.render(kind, A, B, P) in Python, or ffmpeg -filter_complex xfade=transition=<kind>:duration=D:offset=O directly.
- **أرقام / params:** squeezeh, squeezev, zoomin, pixelize, hblur
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1`

#### TRANS-23 · مخطط المونتاج على الإيقاع · Beat-grid montage planner · ✅ مُثبت هنا
- **ماذا / what:** Places every cut on a detected beat with a rhythm of quick and breathing shots; breathing shots prefer downbeats; no flash frames; a short tail is folded into the last shot.
- **كيف / how:** montage.plan(beats, downbeats, seconds, beat) inside montage.py cut
- **أرقام / params:** pattern [hook, fast, fast, slow, fast, fast, fast, slow, fast, slow]; fast≈1.0 s, slow≈3.0 s, hook ≤1.4 s; downbeat search ±1 beat; min shot 0.35 s; fold tail <0.5 s
- **الدليل / proof:** `kosif-studio/motion/montage.py:81` · `kosif-studio/tests/test_studio.py:765`

#### TRANS-24 · اختيار أنشط مقطع · Most-active window shot picker · ✅ مُثبت هنا
- **ماذا / what:** For each slot, picks the window of the next clip (round robin) with the highest frame-difference energy that has not been used yet.
- **كيف / how:** montage.energy (6 fps, 160 px grey) + montage.pick
- **أرقام / params:** energy at 6 fps; fallback = least-overlap window
- **الدليل / proof:** `kosif-studio/motion/montage.py:105` · `kosif-studio/motion/montage.py:115` · `kosif-studio/tests/test_studio.py:765`

#### TRANS-25 · أمر مونتاج الإيقاع · Beat montage command · ✅ مُثبت هنا
- **ماذا / what:** Full music-driven edit: beats → plan → active windows → fill-crop + punches + grade → hard cuts → music (+voice ducked, +clips' own sound) → −14 LUFS → optional karaoke captions; writes a .montage.json log.
- **كيف / how:** python montage.py cut A.mp4 B.mp4 --music track.wav [--seconds 20 --ratio 9:16 --fps 30 --grade teal_orange --voice vo.wav --captions caps.json --keep-audio --style reels --no-punch] --out film.mp4
- **أرقام / params:** music fade-out 0.6 s; natural sound volume 0.35; AAC 256k 48 kHz; proof montage_demo 8 shots @120.97 bpm golden_hour
- **الدليل / proof:** `kosif-studio/motion/montage.py:148` · `kosif-studio/out/montage_demo.montage.json`

#### TRANS-26 · مونتاج يقوده الصوت · Voice-first montage · ✅ مُثبت هنا
- **ماذا / what:** For interviews, speeches and podcasts: cuts follow caption boundaries (semantic) or a varied cadence; no fake BPM; clips' own sound can sit under the voice.
- **كيف / how:** python montage.py voicecut CLIPS --voice vo.wav [--captions caps.json --grade clean_commercial --keep-audio] --out film.mp4
- **أرقام / params:** cut at caption starts 0.6 s from ends, merge cuts <1.8 s apart; long holds split with [3.2,4.0,3.6,5.0,3.0,4.4] s; max 6.5 s; min 0.45 s; natural sound 0.28; duck ratio 12 release 320
- **الدليل / proof:** `kosif-studio/motion/montage.py:218` · `kosif-studio/motion/montage.py:254` · `kosif-studio/motion/test_voice_montage.py:1`

#### TRANS-27 · زووم خاطف عند القطع · Camera punch-in on scene cuts · ✅ مُثبت هنا
- **ماذا / what:** Scene boundaries are marked by a quick 200 ms scale ramp (1.0->1.08/1.12) snapping back to 1.0, giving a punchy cut.
- **كيف / how:** camKeys pairs at t and t+0.2
- **أرقام / params:** scale 1.08-1.12, rot up to -1.5deg, 0.2 s
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:106`

#### TRANS-28 · قص الصمت · Silence jump-cut · 🟢 جاهز
- **ماذا / what:** Remove silences from talking clips.
- **كيف / how:** tools.py silence CLIP --threshold -35 --min 0.45 --pad 0.08
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/tools.py` · `kosif-one/tools/kosif-studio/motion/tools.py:113` · `kosif-one/tools/kosif-studio/motion/tools.py:121` · `kosif-studio/motion/tools.py:121`

#### TRANS-29 · قطع بسرعات متطابقة · Velocity-matched cut · 🟢 جاهز
- **ماذا / what:** Exit the outgoing beat with an accelerating move plus blur ramp and enter the next with a decelerating move from blur; the fastest moments meet at the cut so it reads as one camera move.
- **كيف / how:** GSAP: outgoing tween ends exactly at beat end with ease power2.in; incoming starts at 0 with power2.out. Same idea in CSS keyframes or Remotion interpolate.
- **أرقام / params:** exit y -150, blur 30px, 0.33s power2.in; enter y 150->0, blur 30->0, 1.0s power2.out
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/step-4-storyboard.md`

#### TRANS-30 · كشف دائري · Iris reveal / close · 🟢 جاهز
- **ماذا / what:** Reveals or hides an element through a growing circle from a point, radius in log space.
- **كيف / how:** MOTION.iris(tl, el, at, {x, y, r, r0, dur, close}); animates clip-path circle().
- **أرقام / params:** R 2300 px; r0 1 px; dur 0.4 s; open logEase E.out; close logEase E.in
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:334` · `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:334`

#### TRANS-31 · غمر لوني كامل · Colour flood seam · 🟢 جاهز
- **ماذا / what:** A full-frame accent colour floods from a point on its cue (one per film) and can fade out.
- **كيف / how:** MOTION.flood(tl, stage, at, {color, x, y, r, dur, out, outDur}).
- **أرقام / params:** color #e4342f, r 2400, dur 0.3 s, starts 1/60 s early
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:342` · `kosif-studio/motion/kit/motion-kit.js:342`

#### TRANS-32 · انتقالات السحب السريع والضبابي والزووم · Whip pan, blur-through and zoom-through transitions · 🟢 جاهز
- **ماذا / what:** Three CSS-level transition recipes for continuous-camera feeling between beats.
- **كيف / how:** Implement as paired exit/entry tweens on the two scene containers.
- **أرقام / params:** whip: exit x -400 blur 24px 0.3s power3.in -> entry x 400->0 0.3s power3.out; blur-through: exit blur 20px 0.3s -> entry 20->0 0.25s power3.out; zoom-through: exit scale 1->1.2 blur 20 0.2s power3.in -> entry scale 0.75->1 blur 20->0 0.5s expo.out
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/step-4-storyboard.md`

#### TRANS-33 · وصفات انتقالات العرض الأصلية · View Transitions recipes (fade, slide, scale, morph) · 🟢 جاهز
- **ماذا / what:** Browser-native snapshot transitions between UI states: cross-fade, directional slides for hierarchy, scale in/out, and shared-element morphs with a brief blur midway.
- **كيف / how:** document.startViewTransition or React <ViewTransition> with ::view-transition-old/new(.class) keyframes; type-keyed classes nav-forward/nav-back. Chromium in /opt/pw-browsers supports it.
- **أرقام / params:** exit 150ms, enter 210ms, move 400ms; slide offset 60px; scale 0.85<->1; morph blur 3px at 30%; toggle 100-200ms, route 150-250ms, suspense reveal 200-400ms, shared morph 300-500ms; sliding tab indicator 220ms
- **الدليل / proof:** `kosif-atlas/skills/1434-react-skills/3419-vercel-react-view-transitions` · `kosif-atlas/skills/1434-react-skills/3419-vercel-react-view-transitions/references/css-recipes.md` · `kosif-atlas/skills/1434-react-skills/3419-vercel-react-view-transitions/references/patterns.md`

#### TRANS-34 · تحوّل الحاوية المشتركة · Shared-element container morph · 🟢 جاهز
- **ماذا / what:** An element keeps its identity across states: a card grows into a modal, a pill expands into a panel, a highlight slides between tabs; content inside cross-fades while bounds animate.
- **كيف / how:** Framer Motion layout / layoutId, GSAP Flip, or View Transitions name; in a video, interpolate the bounding box between two measured rects with a spring and cross-fade contents (200ms).
- **أرقام / params:** container spring 300/30; content cross-fade 200ms; layout='position' to avoid squish; borderRadius as inline style
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion` · `kosif-atlas/skills/342-kernel/1223-frontend/motion/one-surface.md` · `kosif-atlas/skills/1434-react-skills/3419-vercel-react-view-transitions`

#### TRANS-35 · حركات الدخول الأصلية بـ starting-style · Native entry animations with @starting-style · 🟢 جاهز
- **ماذا / what:** CSS-only enter/exit for popovers, dialogs and newly displayed elements, including transitions on display; Tailwind v4 keeps keyframes inside @theme as --animate-* tokens (tailwindcss-animate is gone).
- **كيف / how:** [popover] transition opacity/transform/display allow-discrete with @starting-style initial state; @theme { --animate-fade-in: fade-in 0.2s ease-out; }
- **أرقام / params:** popover 0.2s, scale 0.95->1; dialog in 0.2s ease-out, out 0.15s ease-in; slide 0.3s
- **الدليل / proof:** `kosif-atlas/skills/3096-frontend-mobile-development/13267-tailwind-design-system` · `kosif-atlas/skills/3096-frontend-mobile-development/13267-tailwind-design-system/references/advanced-patterns.md` · `kosif-atlas/skills/1483-tailwind/3674-tailwind-best-practices`

#### TRANS-36 · كشف بالقص والقناع · Clip-path and SVG-mask reveals · 🟢 جاهز
- **ماذا / what:** Images and sections revealed by an animating clip-path or SVG mask rather than a fade, often triggered on scroll or beat.
- **كيف / how:** CSS clip-path inset()/circle() animated with the expo-out curve; for fullscreen reveals animate an SVG mask shape. Works in CSS/WAAPI.
- **أرقام / params:** 0.8s cubic-bezier(0.16,1,0.3,1)
- **الدليل / proof:** `kosif-atlas/skills/3529-ui-design/14308-interaction-design/references/scroll-animations.md` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion` · `kosif-atlas/skills/3438-ux-design/14124-top-design`

#### TRANS-37 · قص بدون فقد مضبوط على الإطار المفتاحي · Keyframe-snapped lossless trim · 🟢 جاهز
- **ماذا / what:** Stream-copy cuts only land cleanly on I/IDR frames; a cut on a P/B frame produces black/frozen first seconds. Probe packet flags to find the nearest keyframe before -c copy.
- **كيف / how:** ffprobe -select_streams v:0 -show_packets -show_entries packet=pts_time,flags -read_intervals T-5%+10 -of json in.mp4 ; pick packet with flag K ; ffmpeg -ss K -i in -to D -c copy -avoid_negative_ts make_zero out.mp4
- **أرقام / params:** search window ±5 s
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/756-losslesscut/SKILL.md`

#### TRANS-38 · انتقال تسرب ضوئي · Light-leak transition · 🟢 جاهز
- **ماذا / what:** Warm gradient overlays sweep across and peak while scenes swap.
- **كيف / how:** GSAP: warm overlay 0->0.4 (0.3s), leak layers x+300/+200 over 0.5-0.6s sine.inOut, swap at T+0.45, fade 0.4s power2.out.
- **أرقام / params:** total ~0.9s
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions/css-light.md`

#### TRANS-39 · احتراق تعريض زائد · Overexposure burn · 🟢 جاهز
- **ماذا / what:** Scene brightens to white flash then cuts.
- **كيف / how:** filter brightness 1.5->3 + scale 1.03->1.06 over 0.4s; white overlay to 1 at T+0.4; swap T+0.55; overlay out 0.35s.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions/css-light.md`

#### TRANS-40 · حرق فيلم · Film-burn transition · 🟢 جاهز
- **ماذا / what:** Three orange burn blobs slide across; swap under them.
- **كيف / how:** burn-a/b/c opacity 1 with x -300/-500/-200 over 0.4-0.5s; swap T+0.35; fade 0.3s staggered.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions/css-light.md`

#### TRANS-41 · احتراق الصفحة · Page-burn destruction · 🟢 جاهز
- **ماذا / what:** Noise-edged burning hole eats the frame; next scene fades from black at ~90%.
- **كيف / how:** Layered sin-hash noise on angle (amps 50/20/8); content reveal 0.8-1.2s power1.out staggered 0.5/0.7s.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions/css-destruction.md`

#### TRANS-42 · انتقال غليتش · RGB glitch transition · 🟢 جاهز
- **ماذا / what:** Tinted R/G/B copies jitter with large offsets for a few frames.
- **كيف / how:** Normal blend at 35% (not multiply); 6 jitter frames every 0.03s, ±30-60px.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions/css-distortion.md`

#### TRANS-43 · انتقال تفكك لوني · Chromatic-split transition · 🟢 جاهز
- **ماذا / what:** RGB layers spread ±80px, scene fades, converge onto new scene.
- **كيف / how:** GSAP 0.3s power2.in spread then reverse.
- **أرقام / params:** ±80px
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions/css-distortion.md`

#### TRANS-44 · تموج وشرائط VHS · Ripple / VHS strip transitions · 🟢 جاهز
- **ماذا / what:** Rapid ±30px oscillation with 0.97-1.03 scale and rising blur; or 20 clip-path strips of 54px shifting randomly.
- **كيف / how:** GSAP 0.04s steps; seeded offsets per strip.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions/css-distortion.md`

#### TRANS-45 · قلب بطاقة ثلاثي الأبعاد · CSS 3D card flip · 🟢 جاهز
- **ماذا / what:** 180° Y flip between scenes.
- **كيف / how:** perspective 1200px; preserve-3d; backface hidden; rotationY 0.6s power2.inOut.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions/css-3d.md`

#### TRANS-46 · انتقال بسرعة متطابقة · Velocity-matched blur transitions on text · 🟢 جاهز
- **ماذا / what:** Outgoing text accelerates out with blur, incoming decelerates in from blur, reading as one motion.
- **كيف / how:** Exit y:-150 blur 30px opacity0 0.33s power2.in; entry from y:150 blur 30px to 0 over 1.0s power2.out.
- **أرقام / params:** 0.33s / 1.0s; 30px
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### TRANS-47 · دخول الشاشة والإشعار · Legacy view-in and toast-in · 🟢 جاهز
- **ماذا / what:** Minimal 5px rise for whole views and a 10px slide-up for toasts.
- **كيف / how:** keyframes view-in (.24s ease-out) and toast-in (.22s forwards).
- **أرقام / params:** view 240ms translateY 5px; toast 220ms translateY 10px, opacity 0->1
- **الدليل / proof:** `kosif-audit-studio/styles.css:140` · `kosif-audit-studio/styles.css:532`

#### TRANS-48 · انتقال تبويبات مساحة العمل · Workspace tab switch (V5) · 🟢 جاهز
- **ماذا / what:** Quick partial-opacity rise when switching workspace tabs, skipped on overview.
- **كيف / how:** keyframe workspaceIn on .workspace-grid and .panel when body[data-workspace-view] != overview.
- **أرقام / params:** 180ms ease; opacity .55->1; translateY 4px
- **الدليل / proof:** `kosif-audit-studio/workspace-navigation.css`

#### TRANS-49 · تبديل لوحة التفاصيل · Detail panel swap · 🟢 جاهز
- **ماذا / what:** Content swap for a side detail: vertical variant rises 6px with tiny scale, horizontal variant slides 8px in from the inline side.
- **كيف / how:** Keyed element + .detail-panel-motion (kosif-detail-swap) or .standard-detail-motion (kosif-standard-swap).
- **أرقام / params:** 260ms ease-cinematic; 6px + scale .995 / translateX 8px
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:809` · `kosif-audit-pro/app/globals.css:2144`

#### TRANS-50 · توسيع الصف على الجوال · Mobile row expand · 🟢 جاهز
- **ماذا / what:** Expanded request details drop in from 5px above on phones.
- **كيف / how:** kosif-mobile-expand inside @media (max-width:768px).
- **أرقام / params:** 260ms ease-cinematic; translateY -5px -> 0
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:2912`

#### TRANS-51 · ارتفاع متحرك لعنصر details · Animated native <details> height · 🟢 جاهز
- **ماذا / what:** Pure-CSS accordion: the ::details-content pseudo animates block-size from 0 to auto (enabled by interpolate-size) while a +/- badge flips 180deg on a spring.
- **كيف / how:** html { interpolate-size: allow-keywords }; .x::details-content { block-size:0; transition: block-size, content-visibility allow-discrete, opacity }; [open] -> auto.
- **أرقام / params:** block-size 260ms ease-cinematic; opacity 160ms; badge 22px circle rotate(180deg) 260ms spring
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:159` · `kosif-audit-pro/app/globals.css:1875` · `kosif-audit-pro/app/globals.css:1897`

#### TRANS-52 · فيضان لوني · Colour flood wipe · 🟢 جاهز
- **ماذا / what:** A full-frame accent colour floods from a point (one per film), already opening on its cue.
- **كيف / how:** MOTION.flood(tl, stage, at, {color, x, y, r, dur, out, outDur, z}).
- **أرقام / params:** color #e4342f; r 2400; dur 0.3 s; starts 1 frame early; z 60; out fade 0.2 s E.smooth
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:342`

#### TRANS-53 · دوران ثلاثي الأبعاد · 3D card roll · 🟢 جاهز
- **ماذا / what:** Front-loaded rotationX flip into place with perspective on the parent.
- **كيف / how:** MOTION.roll(tl, el, at, {from, dur, origin, perspective}).
- **أرقام / params:** rotationX -90 -> 0 in 0.17 s (~10 f), E.out; origin 50% 100%; perspective 2200 px
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:362`

#### TRANS-54 · ضبابية السرعة · Directional speed blur · 🟢 جاهز
- **ماذا / what:** An SVG Gaussian blur on one axis that swells and fades over a fast move.
- **كيف / how:** MOTION.speedBlur(tl, el, at, dur, {px, axis, id}); creates filter #mk-sb-N.
- **أرقام / params:** px 12; rise 45% of dur E.in, fall 55% E.out
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:378`

#### TRANS-55 · تشويش رقمي · Digital glitch stutter (2D) · 🟢 جاهز
- **ماذا / what:** RGB-split drop shadows plus random horizontal slices, seeded, returning clean.
- **كيف / how:** MOTION.glitch(tl, el, at, {dur, amp, seed}).
- **أرقام / params:** dur 0.3 s (<=0.4); 30 steps/s; amp 10 px; shadows rgba(255,0,80,.7) and rgba(0,200,255,.7) +/-4 px; clip inset slices
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:548`

#### TRANS-56 · تشويش مرتبط بالتحليل · Analysis-keyed glitch pass (3D) · 🟢 جاهز
- **ماذا / what:** One deterministic post pass: chroma split, slice displacement on 24 bands, negative tear, cold silver freeze monochrome, tape warp.
- **كيف / how:** const g=K3.makeGlitchPass(); composer.addPass(g); g.userData.set({chroma, slice, negative, mono, warp, frame}).
- **أرقام / params:** 24 bands, 28% displaced up to 12%; chroma 1.2%; mono tint (0.78,0.88,1.0); negative x0.8
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:916`

#### TRANS-57 · قائمة لقطات بقطعات · Shot list sequencer (hard cuts) · 🟢 جاهز
- **ماذا / what:** A shot list becomes one camera function with hard cuts; each move starts at its cut.
- **كيف / how:** const cam=K3.sequence([{at:0, shot:'establishing'},{at:2.5, shot:'low angle tracking'}], {seconds}).
- **أرقام / params:** no crossfades; t0/t1 default to each entry's span
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1210`

#### TRANS-58 · انتقالات xfade · xfade transitions (57) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade + matching acrossfade; clamped to half clip.
- **كيف / how:** clips[].transition {type,dur 0.05-5}; kmotion transitions lists 57 (e.g. circleopen, slideup)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`

#### TRANS-59 · انتقالات xfade · FFmpeg xfade transition set (58) · 🟢 جاهز
- **ماذا / what:** 58 named FFmpeg xfade transitions with matching audio crossfades, filtered to those the local build supports.
- **كيف / how:** timeline spec clip 'transition':{'type':NAME,'dur':0.6}; list with timeline.py --transitions
- **أرقام / params:** fade, wipeleft, wiperight, wipeup, wipedown, slideleft, slideright, slideup, slidedown, circlecrop, rectcrop, distance, fadeblack, fadewhite, radial, smoothleft, smoothright, smoothup, smoothdown, circleopen, circleclose, vertopen, vertclose, horzopen, horzclose, dissolve, pixelize, diagtl, diagtr, …
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74`

#### TRANS-60 · محاكاة ريل · Mimic reference reel · 🟢 جاهز
- **ماذا / what:** Rebuild a reference reel shot-for-shot with new footage: frame-exact cuts, transitions, text zones, sound.
- **كيف / how:** kmotion mimic study REF --out DIR; then match/build (--strength 0.7, --snap HSV element)
- **أرقام / params:** boundary types: cut, dissolve, fadeblack, fadewhite, slide
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/mimic.py:49`

#### TRANS-61 · حلقة سلسة · Seamless loop · 🟢 جاهز
- **ماذا / what:** Tail dissolves into head.
- **كيف / how:** tools.py loop CLIP --seconds 30 --xfade 0.6
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/tools.py`

#### TRANS-62 · عائلة التلاشي · Cross-fade family (FFmpeg xfade) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade transitions of this family, offered by the studio's timeline tab and MCP with an Arabic family label; each comes with a matching audio cross-fade in the timeline renderer.
- **كيف / how:** In a timeline spec set clip.transition = "NAME" or {"type": "NAME", "dur": seconds}; GET /api/transitions or MCP kosif_transitions lists those the local FFmpeg build reports (parsed from `ffmpeg -h filter=xfade`).
- **أرقام / params:** names: fade, fadefast, fadeslow, dissolve (grainy), fadeblack (through black), fadewhite (through white), fadegrays (through grey)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:583`

#### TRANS-63 · عائلة المسح · Wipe family (FFmpeg xfade) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade transitions of this family, offered by the studio's timeline tab and MCP with an Arabic family label; each comes with a matching audio cross-fade in the timeline renderer.
- **كيف / how:** In a timeline spec set clip.transition = "NAME" or {"type": "NAME", "dur": seconds}; GET /api/transitions or MCP kosif_transitions lists those the local FFmpeg build reports (parsed from `ffmpeg -h filter=xfade`).
- **أرقام / params:** names: wipeleft, wiperight, wipeup, wipedown, wipetl, wipetr, wipebl, wipebr
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:583`

#### TRANS-64 · عائلة الانزلاق · Slide family (FFmpeg xfade) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade transitions of this family, offered by the studio's timeline tab and MCP with an Arabic family label; each comes with a matching audio cross-fade in the timeline renderer.
- **كيف / how:** In a timeline spec set clip.transition = "NAME" or {"type": "NAME", "dur": seconds}; GET /api/transitions or MCP kosif_transitions lists those the local FFmpeg build reports (parsed from `ffmpeg -h filter=xfade`).
- **أرقام / params:** names: slideleft, slideright, slideup, slidedown
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:583`

#### TRANS-65 · عائلة المسح الناعم · Smooth wipe family (FFmpeg xfade) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade transitions of this family, offered by the studio's timeline tab and MCP with an Arabic family label; each comes with a matching audio cross-fade in the timeline renderer.
- **كيف / how:** In a timeline spec set clip.transition = "NAME" or {"type": "NAME", "dur": seconds}; GET /api/transitions or MCP kosif_transitions lists those the local FFmpeg build reports (parsed from `ffmpeg -h filter=xfade`).
- **أرقام / params:** names: smoothleft, smoothright, smoothup, smoothdown
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:583`

#### TRANS-66 · كشف دائري ومستطيل وشعاعي · Circle / rect / radial reveals (FFmpeg xfade) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade transitions of this family, offered by the studio's timeline tab and MCP with an Arabic family label; each comes with a matching audio cross-fade in the timeline renderer.
- **كيف / how:** In a timeline spec set clip.transition = "NAME" or {"type": "NAME", "dur": seconds}; GET /api/transitions or MCP kosif_transitions lists those the local FFmpeg build reports (parsed from `ffmpeg -h filter=xfade`).
- **أرقام / params:** names: circlecrop, circleopen, circleclose, rectcrop, radial
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:583`

#### TRANS-67 · فتح وإغلاق رأسي وأفقي · Barn-door opens and closes (FFmpeg xfade) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade transitions of this family, offered by the studio's timeline tab and MCP with an Arabic family label; each comes with a matching audio cross-fade in the timeline renderer.
- **كيف / how:** In a timeline spec set clip.transition = "NAME" or {"type": "NAME", "dur": seconds}; GET /api/transitions or MCP kosif_transitions lists those the local FFmpeg build reports (parsed from `ffmpeg -h filter=xfade`).
- **أرقام / params:** names: vertopen, vertclose, horzopen, horzclose
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:583`

#### TRANS-68 · مسح قطري · Diagonal wipes (FFmpeg xfade) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade transitions of this family, offered by the studio's timeline tab and MCP with an Arabic family label; each comes with a matching audio cross-fade in the timeline renderer.
- **كيف / how:** In a timeline spec set clip.transition = "NAME" or {"type": "NAME", "dur": seconds}; GET /api/transitions or MCP kosif_transitions lists those the local FFmpeg build reports (parsed from `ffmpeg -h filter=xfade`).
- **أرقام / params:** names: diagtl, diagtr, diagbl, diagbr
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:583`

#### TRANS-69 · انتقالات الشرائح · Slice transitions (FFmpeg xfade) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade transitions of this family, offered by the studio's timeline tab and MCP with an Arabic family label; each comes with a matching audio cross-fade in the timeline renderer.
- **كيف / how:** In a timeline spec set clip.transition = "NAME" or {"type": "NAME", "dur": seconds}; GET /api/transitions or MCP kosif_transitions lists those the local FFmpeg build reports (parsed from `ffmpeg -h filter=xfade`).
- **أرقام / params:** names: hlslice, hrslice, vuslice, vdslice
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:583`

#### TRANS-70 · انتقالات الريح · Wind transitions (FFmpeg xfade) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade transitions of this family, offered by the studio's timeline tab and MCP with an Arabic family label; each comes with a matching audio cross-fade in the timeline renderer.
- **كيف / how:** In a timeline spec set clip.transition = "NAME" or {"type": "NAME", "dur": seconds}; GET /api/transitions or MCP kosif_transitions lists those the local FFmpeg build reports (parsed from `ffmpeg -h filter=xfade`).
- **أرقام / params:** names: hlwind, hrwind, vuwind, vdwind
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:583`

#### TRANS-71 · انتقالات التغطية · Cover transitions (FFmpeg xfade) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade transitions of this family, offered by the studio's timeline tab and MCP with an Arabic family label; each comes with a matching audio cross-fade in the timeline renderer.
- **كيف / how:** In a timeline spec set clip.transition = "NAME" or {"type": "NAME", "dur": seconds}; GET /api/transitions or MCP kosif_transitions lists those the local FFmpeg build reports (parsed from `ffmpeg -h filter=xfade`).
- **أرقام / params:** names: coverleft, coverright, coverup, coverdown
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:583`

#### TRANS-72 · انتقالات الكشف · Reveal transitions (FFmpeg xfade) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade transitions of this family, offered by the studio's timeline tab and MCP with an Arabic family label; each comes with a matching audio cross-fade in the timeline renderer.
- **كيف / how:** In a timeline spec set clip.transition = "NAME" or {"type": "NAME", "dur": seconds}; GET /api/transitions or MCP kosif_transitions lists those the local FFmpeg build reports (parsed from `ffmpeg -h filter=xfade`).
- **أرقام / params:** names: revealleft, revealright, revealup, revealdown
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:583`

#### TRANS-73 · انتقالات الضغط · Squeeze transitions (FFmpeg xfade) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade transitions of this family, offered by the studio's timeline tab and MCP with an Arabic family label; each comes with a matching audio cross-fade in the timeline renderer.
- **كيف / how:** In a timeline spec set clip.transition = "NAME" or {"type": "NAME", "dur": seconds}; GET /api/transitions or MCP kosif_transitions lists those the local FFmpeg build reports (parsed from `ffmpeg -h filter=xfade`).
- **أرقام / params:** names: squeezeh, squeezev
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:583`

#### TRANS-74 · انتقال الزووم للداخل · Zoom-in transition (FFmpeg xfade) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade transitions of this family, offered by the studio's timeline tab and MCP with an Arabic family label; each comes with a matching audio cross-fade in the timeline renderer.
- **كيف / how:** In a timeline spec set clip.transition = "NAME" or {"type": "NAME", "dur": seconds}; GET /api/transitions or MCP kosif_transitions lists those the local FFmpeg build reports (parsed from `ffmpeg -h filter=xfade`).
- **أرقام / params:** names: zoomin
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:583`

#### TRANS-75 · انتقال التبكسل · Pixelize transition (FFmpeg xfade) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade transitions of this family, offered by the studio's timeline tab and MCP with an Arabic family label; each comes with a matching audio cross-fade in the timeline renderer.
- **كيف / how:** In a timeline spec set clip.transition = "NAME" or {"type": "NAME", "dur": seconds}; GET /api/transitions or MCP kosif_transitions lists those the local FFmpeg build reports (parsed from `ffmpeg -h filter=xfade`).
- **أرقام / params:** names: pixelize
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:583`

#### TRANS-76 · انتقال الضبابية الأفقية · Horizontal blur transition (FFmpeg xfade) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade transitions of this family, offered by the studio's timeline tab and MCP with an Arabic family label; each comes with a matching audio cross-fade in the timeline renderer.
- **كيف / how:** In a timeline spec set clip.transition = "NAME" or {"type": "NAME", "dur": seconds}; GET /api/transitions or MCP kosif_transitions lists those the local FFmpeg build reports (parsed from `ffmpeg -h filter=xfade`).
- **أرقام / params:** names: hblur
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:583`

#### TRANS-77 · انتقال المسافة · Distance transition (FFmpeg xfade) · 🟢 جاهز
- **ماذا / what:** FFmpeg xfade transitions of this family, offered by the studio's timeline tab and MCP with an Arabic family label; each comes with a matching audio cross-fade in the timeline renderer.
- **كيف / how:** In a timeline spec set clip.transition = "NAME" or {"type": "NAME", "dur": seconds}; GET /api/transitions or MCP kosif_transitions lists those the local FFmpeg build reports (parsed from `ffmpeg -h filter=xfade`).
- **أرقام / params:** names: distance
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:67` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:74` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:583`

#### TRANS-78 · قلب ثلاثي الأبعاد · Front-loaded 3D roll flip · 🟢 جاهز
- **ماذا / what:** An element flips in on its X axis with 35% of the rotation on the first frame, done in about 10 frames.
- **كيف / how:** MOTION.roll(tl, el, at, {from, origin, dur, perspective}).
- **أرقام / params:** rotationX -90->0, dur 0.17 s, perspective 2200 px, origin 50% 100%
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:362`

#### TRANS-79 · مونتاج على الإيقاع · Beat-cut montage · 🟢 جاهز
- **ماذا / what:** Edits any footage to a music track: beat grid -> shot plan of quick/breathing shots landing on beats (big ones on downbeats) -> most active window of each clip -> fill-crop, punches, grade -> hard cuts -> ducked mix -> optional karaoke captions.
- **كيف / how:** python montage.py cut CLIP... --music track.wav [--seconds 20] [--ratio 9:16] [--grade teal_orange] [--voice vo.wav] [--captions caps.json] [--keep-audio] --out film.mp4 (or motion.py montage).
- **أرقام / params:** pattern hook(<=1.4 s), fast(~1 s), fast, slow(~3 s), fast, fast, fast, slow, fast, slow; never < 0.35 s; clip own audio at 0.35; end fade 0.6 s; writes .montage.json
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/montage.py:1` · `kosif-one/tools/kosif-studio/motion/montage.py:81`

#### TRANS-80 · زووم ضربة · Zoom punch that decays like a hit · 🟢 جاهز
- **ماذا / what:** On beats the picture jumps to +9% scale and decays with a 0.32 s time constant (rendered at 2x for half-pixel steps).
- **كيف / how:** montage._segment with punches; FFmpeg scale eval=frame expression 0.09*exp(-(t-p)/0.32).
- **أرقام / params:** +9%, tau 0.32 s
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/montage.py:136`

#### TRANS-81 · صانع الحلقة السلسة · Seamless loop maker · 🟢 جاهز
- **ماذا / what:** Makes a clip loop by dissolving its tail into its head.
- **كيف / how:** python tools.py loop CLIP --out loop.mp4 [--seconds 30] [--xfade 0.6].
- **أرقام / params:** xfade 0.6 s
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/tools.py:1`

#### TRANS-82 · انتقالات xfade مع تداخل الصوت · xfade transitions + acrossfade · 🟢 جاهز
- **ماذا / what:** Video crossfade-family transition with matching audio crossfade.
- **كيف / how:** [0:v][1:v]xfade=transition=TYPE:duration=d:offset=len1-d ; [0:a][1:a]acrossfade=d=d. Named types listed: fade, dissolve, wipeleft/right/up/down, slideleft/right/up/down, circleopen/close, pixelize, radial, fadeblack, fadewhite, zoomin, hblur.
- **أرقام / params:** d=0.5 s typical; offset = clip1 length - d
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md` · `100-superskills/skills/pro-video-editor-ffmpeg/scripts/edl_render.py:84`

#### TRANS-83 · قطع J وL · J-cut / L-cut · 🟢 جاهز
- **ماذا / what:** Audio of next clip leads its picture (J) or previous audio runs under new picture (L) to hide cuts.
- **كيف / how:** EDL field audio_lead (atrim starts earlier) for J; extend previous atrim and amix for L.
- **أرقام / params:** audio_lead 0.3 s in example
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md` · `100-superskills/skills/pro-video-editor-ffmpeg/templates/edl.example.json`

#### TRANS-84 · قطع حاد بلا تلاشي · Hard-cut concat (no crossfades) · 🟢 جاهز
- **ماذا / what:** Montage shots join with straight cuts through the concat demuxer; crossfades are avoided on purpose.
- **كيف / how:** ffmpeg -f concat -safe 0 -c copy
- **الدليل / proof:** `kosif-studio/motion/montage.py:174`

#### TRANS-85 · صانع الحلقة السلسة · Seamless loop builder · 🟢 جاهز
- **ماذا / what:** Dissolves the tail into the head so the clip loops without a seam, then repeats it to the requested length.
- **كيف / how:** python tools.py loop CLIP --out loop.mp4 [--seconds 30 --xfade 0.6]
- **أرقام / params:** xfade fade ≤ d/3 (default 0.6 s); acrossfade tri; stream_loop copy
- **الدليل / proof:** `kosif-studio/motion/tools.py:279`

#### TRANS-86 · كلمة الفصل كانتقال · Chapter keyword transition plane · 📦 بأمر تثبيت
- **ماذا / what:** At a cut the keyword fills the frame, then flies up and settles small as a chapter header.
- **كيف / how:** D.chapters [{text, t}] in edit.js.
- **أرقام / params:** 380·k px from x +140, scale 1.25, blur 18 in .2 s; fly to -23% H at scale .36 over .55 s; out at +1.2 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/templates/directed.html` · `100-superskills/skills/kosif-montage-motion/templates/directed.html:113`

#### TRANS-87 · خط الضوء الفاصل · Section rule of light · 📦 بأمر تثبيت
- **ماذا / what:** A thin gradient rule opening from centre marks each new section instead of a transition effect.
- **كيف / how:** Automatic per V.sections in verse.html.
- **أرقام / params:** 2 px, left/right 20%, scaleX 0 -> 1 in .7 s, fades at +1.1 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/templates/verse.html` · `100-superskills/skills/kosif-montage-motion/templates/verse.html:293`

#### TRANS-88 · انتقال تطبيقات الموبايل: تمويه متداخل · Phone-editor transition: blurcross · 📦 بأمر تثبيت
- **ماذا / what:** Custom transition modelling what CapCut/InShot do: blur crossfade.
- **كيف / how:** mm_transitions.render('blurcross', A, B, P, **params) (custom kinds need OpenCV or SciPy here).
- **أرقام / params:** blur 0.015 / 0.035 / 0.06
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1` · `100-superskills/skills/kosif-mimic/scripts/mm_transitions.py:26`

#### TRANS-89 · انتقال تطبيقات الموبايل: زووم + تمويه (CapCut Zoom) · Phone-editor transition: zoomblur · 📦 بأمر تثبيت
- **ماذا / what:** Custom transition modelling what CapCut/InShot do: zoom in with radial blur, CapCut style.
- **كيف / how:** mm_transitions.render('zoomblur', A, B, P, **params) (custom kinds need OpenCV or SciPy here).
- **أرقام / params:** zoom 0.2/0.4/0.7, blur 0-0.045, xmix 0.12
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1` · `100-superskills/skills/kosif-mimic/scripts/mm_transitions.py:26`

#### TRANS-90 · انتقال تطبيقات الموبايل: زووم للخارج + تمويه · Phone-editor transition: zoomblurout · 📦 بأمر تثبيت
- **ماذا / what:** Custom transition modelling what CapCut/InShot do: zoom out with blur.
- **كيف / how:** mm_transitions.render('zoomblurout', A, B, P, **params) (custom kinds need OpenCV or SciPy here).
- **أرقام / params:** zoom 0.2/0.35, blur 0/0.02, xmix 0.12
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1` · `100-superskills/skills/kosif-mimic/scripts/mm_transitions.py:26`

#### TRANS-91 · انتقال تطبيقات الموبايل: دوران · Phone-editor transition: spin · 📦 بأمر تثبيت
- **ماذا / what:** Custom transition modelling what CapCut/InShot do: rotating spin transition.
- **كيف / how:** mm_transitions.render('spin', A, B, P, **params) (custom kinds need OpenCV or SciPy here).
- **أرقام / params:** 90 or 180 deg
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1` · `100-superskills/skills/kosif-mimic/scripts/mm_transitions.py:26`

#### TRANS-92 · انتقالات الشيدر · Shader transitions (WebGL) · 📦 بأمر تثبيت
- **ماذا / what:** Per-pixel transitions (cross-warp morph, domain warp, whip pan, glitch, ridged burn, gravitational lens, swirl, ripple, SDF iris, thermal) composite both scene textures on a WebGL canvas.
- **كيف / how:** @hyperframes/shader-transitions package; scenes captured with html2canvas. Rules: no 'transparent' keyword in gradients (use target color at 0 alpha), no gradients on <4px elements, no var() during capture, gradient opacity >=0.15, explicit .scene background matching bgColor; don't mix CSS and shader transitions in one piece. Alternative here: hand-written GLSL noise-mask mix(colorA,colorB, clamp(noise+progress*2)).
- **أرقام / params:** gradient opacity >=0.15
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions.md` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### TRANS-93 · حساب مدة الانتقالات · TransitionSeries math · 📦 بأمر تثبيت
- **ماذا / what:** Transitions overlap scenes and shorten the total; overlays sit on the cut without changing duration.
- **كيف / how:** fade/slide({direction:'from-left'})/wipe/flip/clockWipe with linearTiming({durationInFrames:15}) or springTiming({config:{damping:200}}); total = sum(scenes) - sum(transitions) (60+60-15=105); overlay cannot be adjacent to another overlay or transition.
- **أرقام / params:** 15-25 frame transitions
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/transitions.md`

#### TRANS-94 · واجهة انتقالات العرض · View Transitions API · 📦 بأمر تثبيت
- **ماذا / what:** Browser-native snapshot morphs between DOM states (shared element, list reorder, enter/exit, route change).
- **كيف / how:** React <ViewTransition name enter exit share> triggered by startTransition; CSS ::view-transition-old/new; Chromium 125+, Firefox 144+, Safari 18.2+. Mostly for interactive web pieces, not frame-rendered video.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1434-react-skills/3419-vercel-react-view-transitions/SKILL.md` · `kosif-atlas/skills/3529-ui-design/14308-interaction-design/references/animation-libraries.md`

#### TRANS-95 · انتقال بقناع ضوضاء · Noise-mask scene transition (FBO) · 📦 بأمر تثبيت
- **ماذا / what:** Render two scenes to textures and mix them with a noise threshold that sweeps with progress for organic dissolves.
- **كيف / how:** noise = clamp(cnoise(vUv*2.5) + uProgress*2.0, 0, 1); color = mix(A,B,noise).
- **أرقام / params:** noise scale 2.5
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### TRANS-96 · متى نستخدم انتقال شيدر أو CSS أو قطع حاد · When to use shader vs CSS vs hard cut · 📦 بأمر تثبيت
- **ماذا / what:** Shader transitions for reveals, logo unveils and downbeat moments; CSS transitions for connective, continuous-camera beats; hard cuts for rapid lists, percussive beat edits and comic timing.
- **كيف / how:** Budget per 5-7 beat reel: 1-2 shader transitions (hero reveal + CTA), the rest CSS or cuts. Shader catalog is a HyperFrames package (needs install) or write own GLSL in a canvas.
- **أرقام / params:** cross-warp morph 0.5-0.8s power2.inOut; cinematic zoom 0.4-0.6s; gravitational lens 0.6-1.0s; glitch 0.3-0.5s; cut when 0.3-0.8s feels too slow
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/step-4-storyboard.md`

#### TRANS-97 · ذوبان ضوضائي بين مشهدين · Noise-dissolve between two rendered scenes · 📦 بأمر تثبيت
- **ماذا / what:** Render both scenes to offscreen targets and blend them with a noise threshold driven by a progress uniform, giving an organic burn/dissolve.
- **كيف / how:** Three.js/R3F two WebGLRenderTargets; fragment mixes A and B by clamp(noise(uv*2.5)+progress*2,0,1). Needs three (npm) and GPU; headless SwiftShader is slow but deterministic in frame-stepped render.
- **أرقام / params:** noise scale 2.5; progress multiplier 2.0
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`

#### TRANS-98 · انتقال المسح بطبقة غطاء · Overlay wipe page transition · 📦 بأمر تثبيت
- **ماذا / what:** A solid overlay scales up from the bottom to cover the old view, then scales away from the top revealing the new view whose elements rise in.
- **كيف / how:** GSAP timeline on .transition-overlay (scaleY 0->1 origin bottom, then 1->0 origin top) and stagger [data-reveal] items (Barba.js in web; plain timeline in video).
- **أرقام / params:** 0.6s expo.inOut each half; old content fades 0.3s at 0.3s; reveal y 60, stagger 0.1, 0.8s expo.out at 0.2s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md`

#### TRANS-99 · انتقال تحلل بالنويز بين مشهدين · Noise-dissolve scene transition · 📦 بأمر تثبيت
- **ماذا / what:** Render two scenes to textures and reveal B through an organic noise front.
- **كيف / how:** n=clamp(cnoise(uv*2.5)+progress*2,0,1); mix(A,B,n). Progress driven by timeline.
- **أرقام / params:** noise scale 2.5
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### TRANS-100 · كشف بمحاكاة سائل · Fluid-sim reveal / x-ray · 📦 بأمر تثبيت
- **ماذا / what:** A ping-pong fluid texture acts as a mask to reveal a second scene.
- **كيف / how:** Stable-fluids ping-pong FBO -> mask uniform -> mix(sceneA,sceneB,mask).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### TRANS-101 · الانتقالات الإحدى عشر · Cut transitions (11) · 📦 بأمر تثبيت
- **ماذا / what:** Eleven transitions applied at every zoom cut.
- **كيف / how:** draw(): flash (white alpha (1-L/0.35)^2*0.8), whip (x offset 18% W easing out over 0.2 s + blur 8 px), shake (0.5 s decaying 28 Hz shake 1.6% W, roll 0.0105 rad), zoomblur (+0.28 zoom, blur 7 px over 0.24 s), rgb (channel split 1.4% W over 0.26 s), glitch (7 sliced rows offset +-8% W + 0.6% split, 0.22 s), dip (to black 0.3 s + 0.16 s before cut), spin (0.14 rad roll + 0.16 zoom over 0.28 s), wipe (primary panel sweeps with 2% accent edge, 0.35 s each side), iris (primary circle closes then open…
- **أرقام / params:** flash|whip|shake|zoomblur|rgb|glitch|dip|spin|wipe|iris|none
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:250` · `app/public/js/00_editor.js:2337` · `app/index.html:316`

#### TRANS-102 · الوضع الهادي بدون وميض · Calm mode (no flicker) rule · 📦 بأمر تثبيت
- **ماذا / what:** Owner rule, on by default: no white flashes, dips to black, glitch/RGB bursts, shake or spin; energy must come from motion. Also appended to every Claude prompt.
- **كيف / how:** calmOn() reads localStorage basma.calm (default on); CALM_OFF {flash,dip,glitch,rgb,shake,spin,zoomblur} -> 'none'; punch zoom eases over 0.5 s instead of 0.18 s; NOFLICK text appended in claudeAPI; allowed transitions none/whip/wipe.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:187` · `app/public/js/00_editor.js:190` · `app/public/js/10_studio.js:2442`

#### TRANS-103 · انفصال الألوان والجليتش · RGB split and slice glitch technique · 📦 بأمر تثبيت
- **ماذا / what:** Channel-split by redrawing the frame through red and cyan multiplied buffers offset sideways, and slice glitch by shifting random horizontal bands.
- **كيف / how:** chroma(W,H,k): two offscreen canvases multiplied by #ff0000 / #00ffff, recomposed with 'lighter' at +-k px; glitchSlices: 7 bands, height 1.5-7.5% H, offset +-8% W*k, seed floor(t*30).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:226` · `app/public/js/00_editor.js:230`

#### TRANS-104 · تسليم المشاهد قطع أو تلاشي · Scene handover: hard cut vs fade · 📦 بأمر تثبيت
- **ماذا / what:** Adjacent full-screen scenes hand over with a hard cut; isolated scenes fade in 0.2 s and out 0.22 s.
- **كيف / how:** drawScenes(): inCut when another scene ends within 0.05 s of this start (or film start), outCut similarly; full layer paints a bg->primary 45% diagonal gradient.
- **أرقام / params:** fade in 0.2 s; out 0.22 s; adjacency 0.05 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:546`

#### TRANS-105 · انتقال شيدر: انفصال لوني · Shader transition: chromatic-split · 📦 بأمر تثبيت
- **ماذا / what:** WebGL fragment-shader transition between two scenes, captured from live DOM.
- **كيف / how:** @hyperframes/shader-transitions registry id 'chromatic-split'; page-side compositing ~6x faster for mp4/hls/gif.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts`

#### TRANS-106 · انتقال شيدر: زوم سينمائي · Shader transition: cinematic-zoom · 📦 بأمر تثبيت
- **ماذا / what:** WebGL fragment-shader transition between two scenes, captured from live DOM.
- **كيف / how:** @hyperframes/shader-transitions registry id 'cinematic-zoom'; page-side compositing ~6x faster for mp4/hls/gif.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts`

#### TRANS-107 · انتقال شيدر: تحول التوائي · Shader transition: cross-warp-morph · 📦 بأمر تثبيت
- **ماذا / what:** WebGL fragment-shader transition between two scenes, captured from live DOM.
- **كيف / how:** @hyperframes/shader-transitions registry id 'cross-warp-morph'; page-side compositing ~6x faster for mp4/hls/gif.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts`

#### TRANS-108 · انتقال شيدر: تشويه المجال · Shader transition: domain-warp · 📦 بأمر تثبيت
- **ماذا / what:** WebGL fragment-shader transition between two scenes, captured from live DOM.
- **كيف / how:** @hyperframes/shader-transitions registry id 'domain-warp'; page-side compositing ~6x faster for mp4/hls/gif.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts`

#### TRANS-109 · انتقال شيدر: وميض أبيض · Shader transition: flash-through-white · 📦 بأمر تثبيت
- **ماذا / what:** WebGL fragment-shader transition between two scenes, captured from live DOM.
- **كيف / how:** @hyperframes/shader-transitions registry id 'flash-through-white'; page-side compositing ~6x faster for mp4/hls/gif.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts`

#### TRANS-110 · انتقال شيدر: غلتش · Shader transition: glitch · 📦 بأمر تثبيت
- **ماذا / what:** WebGL fragment-shader transition between two scenes, captured from live DOM.
- **كيف / how:** @hyperframes/shader-transitions registry id 'glitch'; page-side compositing ~6x faster for mp4/hls/gif.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts`

#### TRANS-111 · انتقال شيدر: عدسة جاذبية · Shader transition: gravitational-lens · 📦 بأمر تثبيت
- **ماذا / what:** WebGL fragment-shader transition between two scenes, captured from live DOM.
- **كيف / how:** @hyperframes/shader-transitions registry id 'gravitational-lens'; page-side compositing ~6x faster for mp4/hls/gif.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts`

#### TRANS-112 · انتقال شيدر: تسرب ضوء · Shader transition: light-leak · 📦 بأمر تثبيت
- **ماذا / what:** WebGL fragment-shader transition between two scenes, captured from live DOM.
- **كيف / how:** @hyperframes/shader-transitions registry id 'light-leak'; page-side compositing ~6x faster for mp4/hls/gif.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts`

#### TRANS-113 · انتقال شيدر: احتراق متعرج · Shader transition: ridged-burn · 📦 بأمر تثبيت
- **ماذا / what:** WebGL fragment-shader transition between two scenes, captured from live DOM.
- **كيف / how:** @hyperframes/shader-transitions registry id 'ridged-burn'; page-side compositing ~6x faster for mp4/hls/gif.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts`

#### TRANS-114 · انتقال شيدر: تموجات · Shader transition: ripple-waves · 📦 بأمر تثبيت
- **ماذا / what:** WebGL fragment-shader transition between two scenes, captured from live DOM.
- **كيف / how:** @hyperframes/shader-transitions registry id 'ripple-waves'; page-side compositing ~6x faster for mp4/hls/gif.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts`

#### TRANS-115 · انتقال شيدر: قزحية · Shader transition: sdf-iris · 📦 بأمر تثبيت
- **ماذا / what:** WebGL fragment-shader transition between two scenes, captured from live DOM.
- **كيف / how:** @hyperframes/shader-transitions registry id 'sdf-iris'; page-side compositing ~6x faster for mp4/hls/gif.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts`

#### TRANS-116 · انتقال شيدر: دوامة · Shader transition: swirl-vortex · 📦 بأمر تثبيت
- **ماذا / what:** WebGL fragment-shader transition between two scenes, captured from live DOM.
- **كيف / how:** @hyperframes/shader-transitions registry id 'swirl-vortex'; page-side compositing ~6x faster for mp4/hls/gif.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts`

#### TRANS-117 · انتقال شيدر: تشوه حراري · Shader transition: thermal-distortion · 📦 بأمر تثبيت
- **ماذا / what:** WebGL fragment-shader transition between two scenes, captured from live DOM.
- **كيف / how:** @hyperframes/shader-transitions registry id 'thermal-distortion'; page-side compositing ~6x faster for mp4/hls/gif.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts`

#### TRANS-118 · انتقال شيدر: سوط كاميرا · Shader transition: whip-pan · 📦 بأمر تثبيت
- **ماذا / what:** WebGL fragment-shader transition between two scenes, captured from live DOM.
- **كيف / how:** @hyperframes/shader-transitions registry id 'whip-pan'; page-side compositing ~6x faster for mp4/hls/gif.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts`

#### TRANS-119 · مسح بانقسام الألوان · Chromatic Aberration Wipe · 📦 بأمر تثبيت
- **ماذا / what:** A fast slide wipe that splits RGB channels on its peak frames.
- **كيف / how:** Install with `npx hyperframes add chromatic-aberration-wipe` (copies to compositions/components/chromatic-aberration-wipe.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes rende…
- **أرقام / params:** direction left|right|up|down; aberration 1; vars: direction=left[left|right|up|down]; accent=blue[blue|green|violet]; aberration=1(0..2)
- **تثبيت / install:** `npx hyperframes add chromatic-aberration-wipe` (copies to compositions/components/chromatic-aberration-wipe`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/chromatic-aberration-wipe/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/chromatic-aberration-wipe/chromatic-aberration-wipe.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/chromatic-aberration-wipe.mdx`

#### TRANS-120 · كشف الستارة المسرحية · Curtain Reveal · 📦 بأمر تثبيت
- **ماذا / what:** Two pleated velvet curtains gather outward from centre under a fixed pelmet, optionally blooming a spotlight on the stage.
- **كيف / how:** Install with `npx hyperframes add curtain-reveal` (copies to compositions/components/curtain-reveal.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium …
- **أرقام / params:** tone red|burgundy|navy|forest; pelmet on|off; spotlight on|off; vars: tone=burgundy[red|burgundy|navy|forest]; pelmet=on[on|off]; spotlight=on[on|off]
- **تثبيت / install:** `npx hyperframes add curtain-reveal` (copies to compositions/components/curtain-reveal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/curtain-reveal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/curtain-reveal/curtain-reveal.html` · `kosif-one/vendor/hyperframes/registry/components/curtain-reveal/demo.html`

#### TRANS-121 · قطع على المنحنى · Cut the Curve · 📦 بأمر تثبيت
- **ماذا / what:** Velocity-matched hard cut: outgoing subject accelerates (power4.in), swaps at peak speed, incoming continues same direction (power4.out).
- **كيف / how:** Install with `npx hyperframes add cut-the-curve` (copies to compositions/components/cut-the-curve.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fr…
- **أرقام / params:** cutFraction 0.33; blurPx 12; subject cursor|card|scene; vars: subject=cursor[cursor|card|scene]; direction=left[left|right|up|down]; cutFraction=0.33(0..1); blurPx=12(0..40); exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add cut-the-curve` (copies to compositions/components/cut-the-curve`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/cut-the-curve/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/cut-the-curve/cut-the-curve.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/cut-the-curve.mdx`

#### TRANS-122 · دفع اتجاهي · Directional Wipe · 📦 بأمر تثبيت
- **ماذا / what:** One panel slides over another as a directional scene push.
- **كيف / how:** Install with `npx hyperframes add directional-wipe` (copies to compositions/components/directional-wipe.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chrom…
- **أرقام / params:** palette slate|teal|ember; corner square|rounded|soft; vars: palette=slate[slate|teal|ember]; corner=rounded[square|rounded|soft]
- **تثبيت / install:** `npx hyperframes add directional-wipe` (copies to compositions/components/directional-wipe`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/directional-wipe/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/directional-wipe/directional-wipe.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/directional-wipe.mdx`

#### TRANS-123 · تلاشي عبر لون · Fade Through · 📦 بأمر تثبيت
- **ماذا / what:** Calm transition: layer A fades into a wash colour then layer B fades up.
- **كيف / how:** Install with `npx hyperframes add fade-through` (copies to compositions/components/fade-through.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fram…
- **أرقام / params:** wash paper|white|ink|accent; shape flat|bloom; strength 1; vars: wash=paper[paper|white|ink|accent]; strength=1(0.1..1); shape=flat[flat|bloom]
- **تثبيت / install:** `npx hyperframes add fade-through` (copies to compositions/components/fade-through`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/fade-through/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/fade-through/fade-through.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/fade-through.mdx`

#### TRANS-124 · انتقال البكسلة · Grid Pixelate Wipe · 📦 بأمر تثبيت
- **ماذا / what:** Screen dissolves into a grid of squares fading out with staggered timing.
- **كيف / how:** Install with `npx hyperframes add grid-pixelate-wipe` (copies to compositions/components/grid-pixelate-wipe.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless C…
- **تثبيت / install:** `npx hyperframes add grid-pixelate-wipe` (copies to compositions/components/grid-pixelate-wipe`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/grid-pixelate-wipe/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/grid-pixelate-wipe/grid-pixelate-wipe.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/grid-pixelate-wipe.mdx`

#### TRANS-125 · ذوبان الهافتون · Halftone Dissolve · 📦 بأمر تثبيت
- **ماذا / what:** Accent ink dots pop onto a grid smallest-first, each becoming a window onto scene B until B replaces A.
- **كيف / how:** Install with `npx hyperframes add halftone-dissolve` (copies to compositions/components/halftone-dissolve.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chr…
- **أرقام / params:** dot_size small|medium|large; direction ltr|center|noise; dissolve_at 1.1 s; vars: dot_size=medium[small|medium|large]; direction=ltr[ltr|center|noise]; dissolve_at=1.1(0.2..10); accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add halftone-dissolve` (copies to compositions/components/halftone-dissolve`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/halftone-dissolve/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/halftone-dissolve/halftone-dissolve.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/halftone-dissolve.mdx`

#### TRANS-126 · كشف القزحية · Iris Reveal · 📦 بأمر تثبيت
- **ماذا / what:** Circle clip-path opens from a set origin revealing B over A; classic register desaturates A so B lands in full colour, thin accent rim.
- **كيف / how:** Install with `npx hyperframes add iris-reveal` (copies to compositions/components/iris-reveal.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame …
- **أرقام / params:** iris_x/y 50 %; open_at 0.35 s; register color|plain; vars: iris_x=50(0..100); iris_y=50(0..100); open_at=0.35(0..8); register=color[color|plain]; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add iris-reveal` (copies to compositions/components/iris-reveal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/iris-reveal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/iris-reveal/iris-reveal.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/iris-reveal.mdx`

#### TRANS-127 · قطع مطابق · Match Cut · 📦 بأمر تثبيت
- **ماذا / what:** A circle accelerates into a single-frame scene swap that matches the incoming circle exactly, then continues to a smaller rest pose.
- **كيف / how:** Install with `npx hyperframes add match-cut` (copies to compositions/components/match-cut.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame capt…
- **أرقام / params:** vars: accent=green[green|blue|violet]; label_a=Start; label_b=Done
- **تثبيت / install:** `npx hyperframes add match-cut` (copies to compositions/components/match-cut`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/match-cut/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/match-cut/match-cut.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/match-cut.mdx`

#### TRANS-128 · تبادل بالتحول · Morph Swap · 📦 بأمر تثبيت
- **ماذا / what:** Two slotted siblings share one centre; A condenses (shrink-fade) or reshapes (scaleX/scaleY) into B.
- **كيف / how:** Install with `npx hyperframes add morph-swap` (copies to compositions/components/morph-swap.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame ca…
- **أرقام / params:** swap_at 1.4 s (0.1-8); register condense|reshape; vars: swap_at=1.4(0.1..8); register=condense[condense|reshape]; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add morph-swap` (copies to compositions/components/morph-swap`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/morph-swap/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/morph-swap/morph-swap.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/morph-swap.mdx`

#### TRANS-129 · انزلاق الصفحة · Page Slide · 📦 بأمر تثبيت
- **ماذا / what:** Outgoing and incoming page panels slide (transitions.dev-inspired).
- **كيف / how:** Install with `npx hyperframes add page-slide` (copies to compositions/components/page-slide.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame ca…
- **أرقام / params:** corner square|soft|round; vars: label_a=Dashboard; label_b=Analytics; accent=green[green|blue|violet]; corner=round[square|soft|round]
- **تثبيت / install:** `npx hyperframes add page-slide` (copies to compositions/components/page-slide`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/page-slide/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/page-slide/page-slide.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/page-slide.mdx`

#### TRANS-130 · الشريط المطاطي · Rubber Band Bumper · 📦 بأمر تثبيت
- **ماذا / what:** Outgoing panel strains against rising resistance, holds at tension, then snaps past an edge with overshoot as the next settles.
- **كيف / how:** Install with `npx hyperframes add rubber-band-bumper` (copies to compositions/components/rubber-band-bumper.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless C…
- **أرقام / params:** direction up|left; vars: direction=up[up|left]; accent=green[green|blue|violet]
- **تثبيت / install:** `npx hyperframes add rubber-band-bumper` (copies to compositions/components/rubber-band-bumper`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/rubber-band-bumper/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/rubber-band-bumper/rubber-band-bumper.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/rubber-band-bumper.mdx`

#### TRANS-131 · محور مشترك عمودي · Shared Axis Y · 📦 بأمر تثبيت
- **ماذا / what:** Per-word vertical shared-axis swap for sharp editorial changes.
- **كيف / how:** Install with `npx hyperframes add shared-axis-y` (copies to compositions/components/shared-axis-y.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fr…
- **أرقام / params:** direction up|down; vars: direction=up[up|down]; distance=standard[close|standard|far]; tone=ink[ink|paper|accent]
- **تثبيت / install:** `npx hyperframes add shared-axis-y` (copies to compositions/components/shared-axis-y`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/shared-axis-y/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/shared-axis-y/shared-axis-y.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/shared-axis-y.mdx`

#### TRANS-132 · محور مشترك عمقي · Shared Axis Z · 📦 بأمر تثبيت
- **ماذا / what:** Scale-based shared-axis transition for depth/focus shifts.
- **كيف / how:** Install with `npx hyperframes add shared-axis-z` (copies to compositions/components/shared-axis-z.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fr…
- **أرقام / params:** direction in|out; depth shallow|standard|deep; vars: direction=in[in|out]; depth=standard[shallow|standard|deep]; tone=ink[ink|paper|accent]
- **تثبيت / install:** `npx hyperframes add shared-axis-z` (copies to compositions/components/shared-axis-z`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/shared-axis-z/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/shared-axis-z/shared-axis-z.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/shared-axis-z.mdx`

#### TRANS-133 · قطع مطابق للنص · Text Match Cut · 📦 بأمر تثبيت
- **ماذا / what:** One line becomes another mid-move: both ride one 85 % easy-ease curve and hard-swap at speed peak as scale, tracking or slide.
- **كيف / how:** Install with `npx hyperframes add text-match-cut` (copies to compositions/components/text-match-cut.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium …
- **أرقام / params:** mode scale-down|scale-up|tracking-in|slide-left|slide-right|slide-up|slide-down; background navy|transparent; vars: text_a=Basic Interface Behavior; text_b=Thoughtful Experience Design; mode=scale-down[scale-down|scale-up|tracking-in|slide-left|slide-right|slide-up|slide-down]; sweep=on[on|off]; bac…
- **تثبيت / install:** `npx hyperframes add text-match-cut` (copies to compositions/components/text-match-cut`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/text-match-cut/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/text-match-cut/text-match-cut.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/text-match-cut.mdx`

#### TRANS-134 · قطع مطابق بالعنوان · Type Match Cut · 📦 بأمر تثبيت
- **ماذا / what:** Headline splits vertically around an incoming panel that grows from the gap; words exit opposite edges.
- **كيف / how:** Install with `npx hyperframes add type-match-cut` (copies to compositions/components/type-match-cut.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium …
- **أرقام / params:** vars: text=Meet the new editor; accent=green[green|blue|violet]
- **تثبيت / install:** `npx hyperframes add type-match-cut` (copies to compositions/components/type-match-cut`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/type-match-cut/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/type-match-cut/type-match-cut.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/type-match-cut.mdx`

#### TRANS-135 · قطع السوط · Whip Pan Cut · 📦 بأمر تثبيت
- **ماذا / what:** Full-frame whip pan: A whips off with capped directional blur, B enters at matched velocity on a speed-ramp with decelerating catch.
- **كيف / how:** Install with `npx hyperframes add whip-pan-cut` (copies to compositions/components/whip-pan-cut.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fram…
- **أرقام / params:** direction left|right; whip_at 0.25 s; vars: direction=left[left|right]; whip_at=0.25(0..8); accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add whip-pan-cut` (copies to compositions/components/whip-pan-cut`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/whip-pan-cut/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/whip-pan-cut/whip-pan-cut.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/whip-pan-cut.mdx`

#### TRANS-136 · انتقال عبر التكبير · Zoom Through Transition · 📦 بأمر تثبيت
- **ماذا / what:** Zooms through a focal card into the next scene.
- **كيف / how:** Install with `npx hyperframes add zoom-through-transition` (copies to compositions/components/zoom-through-transition.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (…
- **أرقام / params:** depth close|standard|far; vars: from-label=Before; to-label=Zoom Through Transition; depth=standard[close|standard|far]; accent=blue[blue|green|violet]
- **تثبيت / install:** `npx hyperframes add zoom-through-transition` (copies to compositions/components/zoom-through-transition`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/zoom-through-transition/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/zoom-through-transition/zoom-through-transition.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/zoom-through-transition.mdx`

#### TRANS-137 · انتقال شيدر الانقسام الشعاعي · Chromatic Radial Split · 📦 بأمر تثبيت
- **ماذا / what:** WebGL transition: radial chromatic-aberration split between scene A and B.
- **كيف / how:** Install with `npx hyperframes add chromatic-radial-split` (copies the full composition to compositions/chromatic-radial-split.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Google Fonts: Bebas Neue, JetBrains Mono, Lato, Space Mono; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add chromatic-radial-split` (copies the full composition to compositions/chromatic-radial-split`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/chromatic-radial-split/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/chromatic-radial-split/chromatic-radial-split.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/chromatic-radial-split.mdx`

#### TRANS-138 · انتقال الزووم السينمائي · Cinematic Zoom · 📦 بأمر تثبيت
- **ماذا / what:** WebGL transition with dramatic zoom blur.
- **كيف / how:** Install with `npx hyperframes add cinematic-zoom` (copies the full composition to compositions/cinematic-zoom.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Google Fonts: Bebas Neue, JetBrains Mono, Lato, Space Mono; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add cinematic-zoom` (copies the full composition to compositions/cinematic-zoom`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/cinematic-zoom/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/cinematic-zoom/cinematic-zoom.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/cinematic-zoom.mdx`

#### TRANS-139 · انتقال الالتواء المتقاطع · Cross Warp Morph · 📦 بأمر تثبيت
- **ماذا / what:** WebGL transition with cross-warped morph.
- **كيف / how:** Install with `npx hyperframes add cross-warp-morph` (copies the full composition to compositions/cross-warp-morph.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Google Fonts: Bebas Neue, JetBrains Mono, Lato, Space Mono; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add cross-warp-morph` (copies the full composition to compositions/cross-warp-morph`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/cross-warp-morph/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/cross-warp-morph/cross-warp-morph.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/cross-warp-morph.mdx`

#### TRANS-140 · انتقال التواء النطاق · Domain Warp Dissolve · 📦 بأمر تثبيت
- **ماذا / what:** WebGL transition using fractal-noise domain warping.
- **كيف / how:** Install with `npx hyperframes add domain-warp-dissolve` (copies the full composition to compositions/domain-warp-dissolve.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Google Fonts: Bebas Neue, JetBrains Mono, Lato, Space Mono; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add domain-warp-dissolve` (copies the full composition to compositions/domain-warp-dissolve`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/domain-warp-dissolve/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/domain-warp-dissolve/domain-warp-dissolve.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/domain-warp-dissolve.mdx`

#### TRANS-141 · انتقال الوميض الأبيض · Flash Through White · 📦 بأمر تثبيت
- **ماذا / what:** WebGL crossfade through a white flash.
- **كيف / how:** Install with `npx hyperframes add flash-through-white` (copies the full composition to compositions/flash-through-white.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Google Fonts: Bebas Neue, JetBrains Mono, Lato, Space Mono; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add flash-through-white` (copies the full composition to compositions/flash-through-white`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/flash-through-white/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/flash-through-white/flash-through-white.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/flash-through-white.mdx`

#### TRANS-142 · انتقال الغليتش · Glitch · 📦 بأمر تثبيت
- **ماذا / what:** WebGL glitch transition: line displacement, block offsets, RGB shift, scanlines, colour quantisation, mixed by progress.
- **كيف / how:** Install with `npx hyperframes add glitch` (copies the full composition to compositions/glitch.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** progress window 1-3 s quadInOut; 60 scan rows; 12x8 blocks; shift 0.035; Google Fonts: Bebas Neue, JetBrains Mono, Lato, Space Mono; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add glitch` (copies the full composition to compositions/glitch`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/glitch/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/glitch/glitch.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/glitch.mdx`

#### TRANS-143 · انتقال العدسة الجاذبية · Gravitational Lens · 📦 بأمر تثبيت
- **ماذا / what:** WebGL transition with gravitational lensing distortion.
- **كيف / how:** Install with `npx hyperframes add gravitational-lens` (copies the full composition to compositions/gravitational-lens.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Google Fonts: Bebas Neue, JetBrains Mono, Lato, Space Mono; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add gravitational-lens` (copies the full composition to compositions/gravitational-lens`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/gravitational-lens/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/gravitational-lens/gravitational-lens.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/gravitational-lens.mdx`

#### TRANS-144 · انتقال تسرب الضوء · Light Leak · 📦 بأمر تثبيت
- **ماذا / what:** WebGL transition with a cinematic light-leak overlay.
- **كيف / how:** Install with `npx hyperframes add light-leak` (copies the full composition to compositions/light-leak.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Google Fonts: Bebas Neue, JetBrains Mono, Lato, Space Mono; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add light-leak` (copies the full composition to compositions/light-leak`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/light-leak/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/light-leak/light-leak.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/light-leak.mdx`

#### TRANS-145 · انتقال جدار الكلمات · Text Clone Wall Transition · 📦 بأمر تثبيت
- **ماذا / what:** Overlay transition: tiled word wall covers frame, inverts by difference blend, clears; hard-cut underneath while covered.
- **كيف / how:** Install with `npx hyperframes add mk-clone-wall-transition` (copies the full composition to compositions/mk-clone-wall-transition.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 2.4 s; 1920x1080; duration 2.4 s
- **تثبيت / install:** `npx hyperframes add mk-clone-wall-transition` (copies the full composition to compositions/mk-clone-wall-transition`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/mk-clone-wall-transition/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/mk-clone-wall-transition/mk-clone-wall-transition.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/mk-clone-wall-transition.mdx`

#### TRANS-146 · انتقال الحرق المتعرج · Ridged Burn · 📦 بأمر تثبيت
- **ماذا / what:** WebGL transition with ridged-turbulence burn.
- **كيف / how:** Install with `npx hyperframes add ridged-burn` (copies the full composition to compositions/ridged-burn.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Google Fonts: Bebas Neue, JetBrains Mono, Lato, Space Mono; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add ridged-burn` (copies the full composition to compositions/ridged-burn`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/ridged-burn/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/ridged-burn/ridged-burn.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/ridged-burn.mdx`

#### TRANS-147 · انتقال التموجات · Ripple Waves · 📦 بأمر تثبيت
- **ماذا / what:** WebGL transition with concentric ripple distortion.
- **كيف / how:** Install with `npx hyperframes add ripple-waves` (copies the full composition to compositions/ripple-waves.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Google Fonts: Bebas Neue, JetBrains Mono, Lato, Space Mono; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add ripple-waves` (copies the full composition to compositions/ripple-waves`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/ripple-waves/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/ripple-waves/ripple-waves.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/ripple-waves.mdx`

#### TRANS-148 · انتقال قزحية SDF · SDF Iris · 📦 بأمر تثبيت
- **ماذا / what:** WebGL iris reveal built on a signed distance field.
- **كيف / how:** Install with `npx hyperframes add sdf-iris` (copies the full composition to compositions/sdf-iris.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Google Fonts: Bebas Neue, JetBrains Mono, Lato, Space Mono; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add sdf-iris` (copies the full composition to compositions/sdf-iris`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/sdf-iris/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/sdf-iris/sdf-iris.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/sdf-iris.mdx`

#### TRANS-149 · انتقال الدوامة · Swirl Vortex · 📦 بأمر تثبيت
- **ماذا / what:** WebGL transition with swirling vortex distortion.
- **كيف / how:** Install with `npx hyperframes add swirl-vortex` (copies the full composition to compositions/swirl-vortex.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Google Fonts: Bebas Neue, JetBrains Mono, Lato, Space Mono; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add swirl-vortex` (copies the full composition to compositions/swirl-vortex`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/swirl-vortex/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/swirl-vortex/swirl-vortex.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/swirl-vortex.mdx`

#### TRANS-150 · انتقال السراب الحراري · Thermal Distortion · 📦 بأمر تثبيت
- **ماذا / what:** WebGL transition with heat-haze distortion.
- **كيف / how:** Install with `npx hyperframes add thermal-distortion` (copies the full composition to compositions/thermal-distortion.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Google Fonts: Bebas Neue, JetBrains Mono, Lato, Space Mono; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add thermal-distortion` (copies the full composition to compositions/thermal-distortion`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/thermal-distortion/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/thermal-distortion/thermal-distortion.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/thermal-distortion.mdx`

#### TRANS-151 · انتقالات ثلاثية الأبعاد · 3D Transitions · 📦 بأمر تثبيت
- **ماذا / what:** Showcase of a 3D perspective card-flip transition (rotationY 0->180, power2.inOut 0.6 s).
- **كيف / how:** Install with `npx hyperframes add transitions-3d` (copies the full composition to compositions/transitions-3d.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** named: 3D Card Flip; 11 s; 1920x1080; duration 11 s
- **تثبيت / install:** `npx hyperframes add transitions-3d` (copies the full composition to compositions/transitions-3d`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/transitions-3d/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/transitions-3d/transitions-3d.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/transitions-3d.mdx`

#### TRANS-152 · انتقالات الضبابية · Blur Transitions · 📦 بأمر تثبيت
- **ماذا / what:** Showcase of blur transitions.
- **كيف / how:** Install with `npx hyperframes add transitions-blur` (copies the full composition to compositions/transitions-blur.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** named: Blur Through (blur 15px, scale 1.05, 0.4 s power2), Directional Blur (blur 12px, skewX 8, x 200, power3), Calm Blur Through (blur 30px, scale 1.08, 0.5 s); 20 s; 1920x1080; duration 20 s
- **تثبيت / install:** `npx hyperframes add transitions-blur` (copies the full composition to compositions/transitions-blur`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/transitions-blur/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/transitions-blur/transitions-blur.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/transitions-blur.mdx`

#### TRANS-153 · انتقالات التغطية · Cover Transitions · 📦 بأمر تثبيت
- **ماذا / what:** Showcase of cover/uncover transitions.
- **كيف / how:** Install with `npx hyperframes add transitions-cover` (copies the full composition to compositions/transitions-cover.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** named: Staggered Blocks, Horizontal Blinds, Vertical Blinds (power3.inOut); 21 s; 1920x1080; duration 21 s
- **تثبيت / install:** `npx hyperframes add transitions-cover` (copies the full composition to compositions/transitions-cover`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/transitions-cover/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/transitions-cover/transitions-cover.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/transitions-cover.mdx`

#### TRANS-154 · انتقالات التدمير · Destruction Transitions · 📦 بأمر تثبيت
- **ماذا / what:** Showcase of break-apart transitions.
- **كيف / how:** Install with `npx hyperframes add transitions-destruction` (copies the full composition to compositions/transitions-destruction.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** named: Page Burn (2 s build, 3 s burn, 3 s settle); 14 s; 1920x1080; duration 14 s
- **تثبيت / install:** `npx hyperframes add transitions-destruction` (copies the full composition to compositions/transitions-destruction`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/transitions-destruction/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/transitions-destruction/transitions-destruction.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/transitions-destruction.mdx`

#### TRANS-155 · انتقالات الذوبان · Dissolve Transitions · 📦 بأمر تثبيت
- **ماذا / what:** Showcase of dissolve and fade transitions.
- **كيف / how:** Install with `npx hyperframes add transitions-dissolve` (copies the full composition to compositions/transitions-dissolve.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** named: Crossfade, Blur Crossfade, Focus Pull, Color Dip; 24 s; 1920x1080; duration 24 s
- **تثبيت / install:** `npx hyperframes add transitions-dissolve` (copies the full composition to compositions/transitions-dissolve`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/transitions-dissolve/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/transitions-dissolve/transitions-dissolve.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/transitions-dissolve.mdx`

#### TRANS-156 · انتقالات التشويه · Distortion Transitions · 📦 بأمر تثبيت
- **ماذا / what:** Showcase of warp/distortion transitions.
- **كيف / how:** Install with `npx hyperframes add transitions-distortion` (copies the full composition to compositions/transitions-distortion.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** named: Glitch, Chromatic Aberration, Ripple; 21 s; 1920x1080; duration 21 s
- **تثبيت / install:** `npx hyperframes add transitions-distortion` (copies the full composition to compositions/transitions-distortion`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/transitions-distortion/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/transitions-distortion/transitions-distortion.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/transitions-distortion.mdx`

#### TRANS-157 · انتقالات الشبكة · Grid Transitions · 📦 بأمر تثبيت
- **ماذا / what:** Showcase of grid tile transitions (cells timed by distance from centre).
- **كيف / how:** Install with `npx hyperframes add transitions-grid` (copies the full composition to compositions/transitions-grid.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** named: Grid Dissolve; 11 s; 1920x1080; duration 11 s
- **تثبيت / install:** `npx hyperframes add transitions-grid` (copies the full composition to compositions/transitions-grid`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/transitions-grid/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/transitions-grid/transitions-grid.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/transitions-grid.mdx`

#### TRANS-158 · انتقالات الضوء · Light Transitions · 📦 بأمر تثبيت
- **ماذا / what:** Showcase of light-based transitions.
- **كيف / how:** Install with `npx hyperframes add transitions-light` (copies the full composition to compositions/transitions-light.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** named: Light Leak, Overexposure Burn, Film Burn; 21 s; 1920x1080; duration 21 s
- **تثبيت / install:** `npx hyperframes add transitions-light` (copies the full composition to compositions/transitions-light`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/transitions-light/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/transitions-light/transitions-light.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/transitions-light.mdx`

#### TRANS-159 · انتقالات ميكانيكية · Mechanical Transitions · 📦 بأمر تثبيت
- **ماذا / what:** Showcase of mechanical transitions.
- **كيف / how:** Install with `npx hyperframes add transitions-mechanical` (copies the full composition to compositions/transitions-mechanical.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** named: Shutter, Clock Wipe; 15 s; 1920x1080; duration 15 s
- **تثبيت / install:** `npx hyperframes add transitions-mechanical` (copies the full composition to compositions/transitions-mechanical`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/transitions-mechanical/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/transitions-mechanical/transitions-mechanical.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/transitions-mechanical.mdx`

#### TRANS-160 · انتقالات متنوعة · Other Transitions · 📦 بأمر تثبيت
- **ماذا / what:** Showcase of misc creative transitions.
- **كيف / how:** Install with `npx hyperframes add transitions-other` (copies the full composition to compositions/transitions-other.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** named: Flash Cut, Gravity Drop, Morph Circle; 20 s; 1920x1080; duration 20 s
- **تثبيت / install:** `npx hyperframes add transitions-other` (copies the full composition to compositions/transitions-other`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/transitions-other/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/transitions-other/transitions-other.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/transitions-other.mdx`

#### TRANS-161 · انتقالات الدفع · Push Transitions · 📦 بأمر تثبيت
- **ماذا / what:** Showcase of push/slide transitions.
- **كيف / how:** Install with `npx hyperframes add transitions-push` (copies the full composition to compositions/transitions-push.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** named: Push Slide, Vertical Push, Elastic Push, Squeeze (power3.inOut 0.4-0.5 s); 24 s; 1920x1080; duration 24 s
- **تثبيت / install:** `npx hyperframes add transitions-push` (copies the full composition to compositions/transitions-push`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/transitions-push/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/transitions-push/transitions-push.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/transitions-push.mdx`

#### TRANS-162 · انتقالات شعاعية · Radial Transitions · 📦 بأمر تثبيت
- **ماذا / what:** Showcase of radial wipes.
- **كيف / how:** Install with `npx hyperframes add transitions-radial` (copies the full composition to compositions/transitions-radial.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** named: Circle Iris, Diamond Iris, Diagonal Split; 20 s; 1920x1080; duration 20 s
- **تثبيت / install:** `npx hyperframes add transitions-radial` (copies the full composition to compositions/transitions-radial`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/transitions-radial/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/transitions-radial/transitions-radial.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/transitions-radial.mdx`

#### TRANS-163 · انتقالات الحجم · Scale Transitions · 📦 بأمر تثبيت
- **ماذا / what:** Showcase of scale/zoom transitions.
- **كيف / how:** Install with `npx hyperframes add transitions-scale` (copies the full composition to compositions/transitions-scale.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** named: Zoom Through, Zoom Out; 15 s; 1920x1080; duration 15 s
- **تثبيت / install:** `npx hyperframes add transitions-scale` (copies the full composition to compositions/transitions-scale`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/transitions-scale/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/transitions-scale/transitions-scale.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/transitions-scale.mdx`

#### TRANS-164 · انتقال البوابة · Portal · 📦 بأمر تثبيت
- **ماذا / what:** HTML portal transition between a light-mode and a dark-mode panel.
- **كيف / how:** Install with `npx hyperframes add vfx-portal` (copies the full composition to compositions/vfx-portal.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.147.0 (CDN), HTML-in-Canvas (canvas layoutsubtree + ctx.drawElementImage, experimental Chromium API), WebGL fragment shader, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Three 0.147; 10 s; Google Fonts: Inter; 1920x1080; duration 10 s
- **تثبيت / install:** `npx hyperframes add vfx-portal` (copies the full composition to compositions/vfx-portal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/vfx-portal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/vfx-portal/vfx-portal.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/vfx-portal.mdx`

#### TRANS-165 · تحطم الزجاج · Shatter · 📦 بأمر تثبيت
- **ماذا / what:** HTML glass-shatter transition from panel A to panel B.
- **كيف / how:** Install with `npx hyperframes add vfx-shatter` (copies the full composition to compositions/vfx-shatter.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.147.0 (CDN), HTML-in-Canvas (canvas layoutsubtree + ctx.drawElementImage, experimental Chromium API), WebGL fragment shader, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Three 0.147; 12 s; Google Fonts: Inter; 1920x1080; duration 12 s
- **تثبيت / install:** `npx hyperframes add vfx-shatter` (copies the full composition to compositions/vfx-shatter`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/vfx-shatter/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/vfx-shatter/vfx-shatter.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/vfx-shatter.mdx`

#### TRANS-166 · انتقال شيدر السوط · Whip Pan · 📦 بأمر تثبيت
- **ماذا / what:** WebGL transition simulating a fast camera whip pan.
- **كيف / how:** Install with `npx hyperframes add whip-pan` (copies the full composition to compositions/whip-pan.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Google Fonts: Bebas Neue, JetBrains Mono, Lato, Space Mono; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add whip-pan` (copies the full composition to compositions/whip-pan`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/whip-pan/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/whip-pan/whip-pan.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/whip-pan.mdx`

#### TRANS-167 · نمط انتقال الشيدر من الصفحة · DOM-to-texture shader transition pattern · 📦 بأمر تثبيت
- **ماذا / what:** Shader transition blocks rasterise scene A and scene B DOM into canvas textures once, then a WebGL fragment shader mixes u_from/u_to by u_progress inside a GSAP-driven onUpdate.
- **كيف / how:** captureScene() paints each scene element (background, text) to a 2D canvas -> gl texture; full-screen quad; uniforms u_from,u_to,u_progress,u_resolution; progress window t=1..3 s with quadratic in-out; 14 named shaders (chromatic-radial-split, cinematic-zoom, cross-warp-morph, domain-warp-dissolve, flash-through-white, glitch, gravitational-lens, light-leak, ridged-burn, ripple-waves, sdf-iris, swirl-vortex, thermal-distortion, whip-pan); a packaged version lives in packages/shader-transitions.
- **أرقام / params:** 4 s blocks; glitch: 60 scan rows, 12x8 blocks, channel shift 0.035, 8-256 colour levels
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/glitch/glitch.html:270` · `kosif-one/vendor/hyperframes/registry/blocks/glitch/glitch.html:331` · `kosif-one/vendor/hyperframes/packages/shader-transitions`

#### TRANS-168 · المسح بالقناع وتقسيم الشاشة · Clip-path wipe and split-screen · 📦 بأمر تثبيت
- **ماذا / what:** A polygon clip-path tween reveals the next clip over an overlapping 0.5 s handoff; same tool builds split-screens.
- **كيف / how:** tl.fromTo('#next .inner',{clipPath:'polygon(0 0,0 0,0 100%,0 100%)'},{clipPath:'polygon(0 0,100% 0,100% 100%,0 100%)',duration:0.5},2).
- **أرقام / params:** 0.5 s overlap
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/creator-editing-recipes.md`

#### TRANS-169 · مزج متقاطع للصورة والصوت · Crossfade with opposing volume envelopes · 📦 بأمر تثبيت
- **ماذا / what:** Two video clips on distinct tracks overlap 0.5 s with opposing opacity tweens on their wrappers and opposing volume lanes in each video's data-automation.
- **كيف / how:** volume lane points a:{0:1,2.5:1,3:0} b:{0:0,0.5:1}; opacity tweens 0.5 s at 2.5 s.
- **أرقام / params:** 0.5 s overlap
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/creator-editing-recipes.md`

#### TRANS-170 · تشويش انقسام الألوان والشرائح · Chromatic RGB-split / slice glitch · 📦 بأمر تثبيت
- **ماذا / what:** Offset color copies jitter on a hash of quantized timeline time, or horizontal slice bands displace and converge under a stepped ease; brief violence then clean clamped rest; entrance stretch, emphasis burst, slice-reveal forms.
- **كيف / how:** Read hyperframes-animation/rules/chromatic-glitch.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** glitch ease power3.in; slice resolve steps(SLICE_STEPS); stretch entrance scaleX 1.3-1.8 -> 1 power4.out
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/chromatic-glitch.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### TRANS-171 · تبديل بالتحجيم في نفس المركز · Scale swap morph · 📦 بأمر تثبيت
- **ماذا / what:** Two elements at the same center: exit shrinks and fades (power2.in), entrance pops with back.out overshoot.
- **كيف / how:** Read hyperframes-animation/rules/scale-swap-transition.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** incoming back.out(2); shared transform-origin 50% 50%; sub-reveal power3.out
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/scale-swap-transition.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### TRANS-172 · تبديل السمة حول عنصر ثابت · Theme crossfade morph under fixed anchor · 📦 بأمر تثبيت
- **ماذا / what:** Whole theme (background, type, radii, icons, logos) re-skins through N pre-styled layers via opacity crossfades while one anchor never moves.
- **كيف / how:** Read hyperframes-animation/rules/theme-crossfade-morph.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** MORPH_DUR ~0.3 s power2.inOut
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/theme-crossfade-morph.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### TRANS-173 · انتقال CSS: دفع انزلاقي · CSS transition: Push slide · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Push slide' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-push.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** old x -> -1920, new 1920 -> 0, 0.5 s power3.inOut
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-push.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-174 · انتقال CSS: دفع عمودي · CSS transition: Vertical push · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Vertical push' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-push.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** y -1080/1080, 0.5 s power3.inOut
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-push.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-175 · انتقال CSS: دفع مرن · CSS transition: Elastic push · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Elastic push' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-push.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** new overshoots to x 30 (0.4 s power4.out) then -15 then 0 (sine)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-push.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-176 · انتقال CSS: ضغط · CSS transition: Squeeze · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Squeeze' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-push.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** old scaleX 0 origin left, new scaleX 0->1 origin right, 0.4 s power3.inOut
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-push.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-177 · انتقال CSS: قزحية دائرية · CSS transition: Circle iris · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Circle iris' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-radial.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** clipPath circle(0% -> 75% at 50% 50%), 0.5 s power2.out
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-radial.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-178 · انتقال CSS: قزحية ماسية · CSS transition: Diamond iris · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Diamond iris' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-radial.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** polygon center -> (50% -20%,120% 50%,50% 120%,-20% 50%), 0.5 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-radial.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-179 · انتقال CSS: انقسام قطري · CSS transition: Diagonal split · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Diagonal split' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-radial.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** old shrinks to corner triangle polygon, 0.5 s power3.inOut, old zIndex 10
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-radial.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-180 · انتقال CSS: قلب البطاقة ثلاثي الأبعاد · CSS transition: 3D card flip · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff '3D card flip' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-3d.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** rotationY 180, 0.6 s power2.inOut, perspective 1200 px, backface hidden
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-3d.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-181 · انتقال CSS: اختراق بالتقريب · CSS transition: Zoom through · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Zoom through' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-scale.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** old scale 2.5 + blur 8px power3.in; new 0.5->1 power3.out at +0.15, 0.4 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-scale.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-182 · انتقال CSS: تبعيد · CSS transition: Zoom out · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Zoom out' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-scale.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** old scale 0.3 opacity 0, 0.4 s power3.in, old on top
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-scale.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-183 · انتقال CSS: تلاشي متقاطع · CSS transition: Crossfade · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Crossfade' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-dissolve.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** opacity 0.5 s power2.inOut
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-dissolve.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-184 · انتقال CSS: تلاشي مع ضبابية · CSS transition: Blur crossfade · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Blur crossfade' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-dissolve.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** medium blur 10px scale 1.03/0.97 0.5 s; calm 25px hold at abstract color
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-dissolve.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-185 · انتقال CSS: سحب التركيز · CSS transition: Focus pull · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Focus pull' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-dissolve.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** old blur 15px 0.5 s; calm 30px 0.8 s with hold
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-dissolve.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-186 · انتقال CSS: غمس لوني إلى الأسود · CSS transition: Color dip · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Color dip' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-dissolve.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** dip to solid (black) between scenes; outro 0.6-1.0 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-dissolve.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-187 · انتقال CSS: كتل لونية متتابعة · CSS transition: Staggered color blocks · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Staggered color blocks' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-cover.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** 2 full-frame blocks x -1920->0->1920, 0.25 s power3.inOut, 0.06 s offset; 5-block dense at 0.04 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-cover.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-188 · انتقال CSS: ستائر أفقية · CSS transition: Horizontal blinds · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Horizontal blinds' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-cover.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** 6 strips x 180 px at 0.03 s or 12 x 90 px at 0.018 s; strip 0.2 s power3.inOut
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-cover.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-189 · انتقال CSS: ستائر عمودية · CSS transition: Vertical blinds · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Vertical blinds' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-cover.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** count by energy: calm 4h/6v, medium 6-8h/8v, high 12-16h/16v
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-cover.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-190 · انتقال CSS: تسرب ضوئي · CSS transition: Light leak · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Light leak' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-light.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** warm tint to 0.4->0.6, 2-3 radial leaks (>=2400 px) drift x 200-300, swap at +0.45 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-light.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-191 · انتقال CSS: حرق بالتعريض الزائد · CSS transition: Overexposure burn · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Overexposure burn' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-light.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** brightness 1.5 -> 3 with scale 1.03->1.06, white overlay to 1, swap at +0.55 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-light.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-192 · انتقال CSS: حرق الفيلم · CSS transition: Film burn · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Film burn' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-light.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** amber/orange/red radial overlays bleed from an edge, staggered 0.05 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-light.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-193 · انتقال CSS: تشويش رقمي · CSS transition: Glitch · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Glitch' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-distortion.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** RGB overlays normal blend 35% opacity, 6 jitter frames at 0.03 s with +/-30-60 px, swap at +0.2 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-distortion.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-194 · انتقال CSS: زيغ لوني · CSS transition: Chromatic aberration · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Chromatic aberration' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-distortion.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** RGB copies spread +/-80 px over 0.3 s power2.in then converge
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-distortion.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-195 · انتقال CSS: تموج · CSS transition: Ripple · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Ripple' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-distortion.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** x +/-30 px oscillations 0.04 s, scale 0.97-1.03, rising blur, swap at peak
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-distortion.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-196 · انتقال CSS: شريط VHS · CSS transition: VHS tape · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'VHS tape' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-distortion.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** clone scene into 20 strips x 54 px (2020 px wide at left -50), seeded per-strip offsets, red+blue copies
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-distortion.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-197 · انتقال CSS: مصراع · CSS transition: Shutter · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Shutter' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-mechanical.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** top/bottom halves close 0.25 s power3.in, swap, reopen to +/-540 px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-mechanical.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-198 · انتقال CSS: مسح كعقرب الساعة · CSS transition: Clock wipe · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Clock wipe' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-mechanical.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** 9-point polygon stepped through 4 quadrants, 0.1 s per quadrant, ease none
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-mechanical.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-199 · انتقال CSS: تحلل شبكي · CSS transition: Grid dissolve · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Grid dissolve' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-grid.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** 12 cells (4x3 of 480x270) or 120 cells (12x10 of 160x108, opacity 0.75); ripple from center; 5 palette colors
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-grid.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-200 · انتقال CSS: سقوط بالجاذبية · CSS transition: Gravity drop · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Gravity drop' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-other.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** old y 1200 rotation 4, 0.5 s power3.in, old zIndex 10
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-other.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-201 · انتقال CSS: دائرة متحولة · CSS transition: Morph circle · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Morph circle' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-other.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** circle in new bg color scale 0 -> 30, 0.5 s power3.in, swap at +0.4
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-other.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-202 · انتقال CSS: عبور بالضبابية · CSS transition: Blur through · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Blur through' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-blur.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** calm blur 30px scale 1.08 hold then 0.7 s resolve; medium 15px 0.4 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-blur.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-203 · انتقال CSS: ضبابية اتجاهية · CSS transition: Directional blur · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Directional blur' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-blur.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** medium blur 12px skewX -8 x -200 0.4 s; calm 20px skewX 4 x 100 0.6 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-blur.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-204 · انتقال CSS: احتراق الصفحة · CSS transition: Page burn · 📦 بأمر تثبيت
- **ماذا / what:** Scene-to-scene handoff 'Page burn' between an outgoing and incoming scene container driven by GSAP.
- **كيف / how:** Read hyperframes-animation/transitions/css-destruction.md; old/new scene-inner selectors at transition time T: position new -> animate old -> swap -> animate new -> clean overlays.
- **أرقام / params:** radial fire front from a corner with 3-octave sin-hash noise (x50, x20, x8 px), evenodd SVG clip, canvas char fringe; new scene fades from black at 90%
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/css-destruction.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### TRANS-205 · انتقال شيدر WebGL: انقسام لوني · WebGL shader transition: chromatic-split · 📦 بأمر تثبيت
- **ماذا / what:** Per-pixel GPU transition 'chromatic-split' compositing both scene textures from @hyperframes/shader-transitions.
- **كيف / how:** Use the package's transitions array, e.g. {time: 4.0, shader: 'chromatic-split', duration: 0.7}; scenes follow shader-compatible CSS rules; roots go transparent on the layered-composite path.
- **أرقام / params:** typical duration 0.6-0.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/overview.md`

#### TRANS-206 · انتقال شيدر WebGL: تقريب سينمائي · WebGL shader transition: cinematic-zoom · 📦 بأمر تثبيت
- **ماذا / what:** Per-pixel GPU transition 'cinematic-zoom' compositing both scene textures from @hyperframes/shader-transitions.
- **كيف / how:** Use the package's transitions array, e.g. {time: 4.0, shader: 'cinematic-zoom', duration: 0.7}; scenes follow shader-compatible CSS rules; roots go transparent on the layered-composite path.
- **أرقام / params:** typical duration 0.6-0.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/overview.md`

#### TRANS-207 · انتقال شيدر WebGL: تحول بالتشويه المتقاطع · WebGL shader transition: cross-warp-morph · 📦 بأمر تثبيت
- **ماذا / what:** Per-pixel GPU transition 'cross-warp-morph' compositing both scene textures from @hyperframes/shader-transitions.
- **كيف / how:** Use the package's transitions array, e.g. {time: 4.0, shader: 'cross-warp-morph', duration: 0.7}; scenes follow shader-compatible CSS rules; roots go transparent on the layered-composite path.
- **أرقام / params:** typical duration 0.6-0.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/overview.md`

#### TRANS-208 · انتقال شيدر WebGL: تشويه المجال · WebGL shader transition: domain-warp · 📦 بأمر تثبيت
- **ماذا / what:** Per-pixel GPU transition 'domain-warp' compositing both scene textures from @hyperframes/shader-transitions.
- **كيف / how:** Use the package's transitions array, e.g. {time: 4.0, shader: 'domain-warp', duration: 0.7}; scenes follow shader-compatible CSS rules; roots go transparent on the layered-composite path.
- **أرقام / params:** typical duration 0.6-0.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/overview.md`

#### TRANS-209 · انتقال شيدر WebGL: وميض عبر الأبيض · WebGL shader transition: flash-through-white · 📦 بأمر تثبيت
- **ماذا / what:** Per-pixel GPU transition 'flash-through-white' compositing both scene textures from @hyperframes/shader-transitions.
- **كيف / how:** Use the package's transitions array, e.g. {time: 4.0, shader: 'flash-through-white', duration: 0.7}; scenes follow shader-compatible CSS rules; roots go transparent on the layered-composite path.
- **أرقام / params:** typical duration 0.6-0.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/overview.md`

#### TRANS-210 · انتقال شيدر WebGL: عدسة جاذبية · WebGL shader transition: gravitational-lens · 📦 بأمر تثبيت
- **ماذا / what:** Per-pixel GPU transition 'gravitational-lens' compositing both scene textures from @hyperframes/shader-transitions.
- **كيف / how:** Use the package's transitions array, e.g. {time: 4.0, shader: 'gravitational-lens', duration: 0.7}; scenes follow shader-compatible CSS rules; roots go transparent on the layered-composite path.
- **أرقام / params:** typical duration 0.6-0.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/overview.md`

#### TRANS-211 · انتقال شيدر WebGL: تسرب ضوئي · WebGL shader transition: light-leak · 📦 بأمر تثبيت
- **ماذا / what:** Per-pixel GPU transition 'light-leak' compositing both scene textures from @hyperframes/shader-transitions.
- **كيف / how:** Use the package's transitions array, e.g. {time: 4.0, shader: 'light-leak', duration: 0.7}; scenes follow shader-compatible CSS rules; roots go transparent on the layered-composite path.
- **أرقام / params:** typical duration 0.6-0.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/overview.md`

#### TRANS-212 · انتقال شيدر WebGL: حرق متشقق · WebGL shader transition: ridged-burn · 📦 بأمر تثبيت
- **ماذا / what:** Per-pixel GPU transition 'ridged-burn' compositing both scene textures from @hyperframes/shader-transitions.
- **كيف / how:** Use the package's transitions array, e.g. {time: 4.0, shader: 'ridged-burn', duration: 0.7}; scenes follow shader-compatible CSS rules; roots go transparent on the layered-composite path.
- **أرقام / params:** typical duration 0.6-0.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/overview.md`

#### TRANS-213 · انتقال شيدر WebGL: موجات متموجة · WebGL shader transition: ripple-waves · 📦 بأمر تثبيت
- **ماذا / what:** Per-pixel GPU transition 'ripple-waves' compositing both scene textures from @hyperframes/shader-transitions.
- **كيف / how:** Use the package's transitions array, e.g. {time: 4.0, shader: 'ripple-waves', duration: 0.7}; scenes follow shader-compatible CSS rules; roots go transparent on the layered-composite path.
- **أرقام / params:** typical duration 0.6-0.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/overview.md`

#### TRANS-214 · انتقال شيدر WebGL: قزحية SDF · WebGL shader transition: sdf-iris · 📦 بأمر تثبيت
- **ماذا / what:** Per-pixel GPU transition 'sdf-iris' compositing both scene textures from @hyperframes/shader-transitions.
- **كيف / how:** Use the package's transitions array, e.g. {time: 4.0, shader: 'sdf-iris', duration: 0.7}; scenes follow shader-compatible CSS rules; roots go transparent on the layered-composite path.
- **أرقام / params:** typical duration 0.6-0.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/overview.md`

#### TRANS-215 · انتقال شيدر WebGL: دوامة · WebGL shader transition: swirl-vortex · 📦 بأمر تثبيت
- **ماذا / what:** Per-pixel GPU transition 'swirl-vortex' compositing both scene textures from @hyperframes/shader-transitions.
- **كيف / how:** Use the package's transitions array, e.g. {time: 4.0, shader: 'swirl-vortex', duration: 0.7}; scenes follow shader-compatible CSS rules; roots go transparent on the layered-composite path.
- **أرقام / params:** typical duration 0.6-0.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/overview.md`

#### TRANS-216 · انتقال شيدر WebGL: تشوه حراري · WebGL shader transition: thermal-distortion · 📦 بأمر تثبيت
- **ماذا / what:** Per-pixel GPU transition 'thermal-distortion' compositing both scene textures from @hyperframes/shader-transitions.
- **كيف / how:** Use the package's transitions array, e.g. {time: 4.0, shader: 'thermal-distortion', duration: 0.7}; scenes follow shader-compatible CSS rules; roots go transparent on the layered-composite path.
- **أرقام / params:** typical duration 0.6-0.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/overview.md`

#### TRANS-217 · انتقال شيدر WebGL: حركة سوط سريعة · WebGL shader transition: whip-pan · 📦 بأمر تثبيت
- **ماذا / what:** Per-pixel GPU transition 'whip-pan' compositing both scene textures from @hyperframes/shader-transitions.
- **كيف / how:** Use the package's transitions array, e.g. {time: 4.0, shader: 'whip-pan', duration: 0.7}; scenes follow shader-compatible CSS rules; roots go transparent on the layered-composite path.
- **أرقام / params:** typical duration 0.6-0.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/shader-transitions/src/shaders/registry.ts` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/overview.md`

#### TRANS-218 · مطابقة الانتقال مع الطاقة والمزاج · Transition energy and mood mapping · 📦 بأمر تثبيت
- **ماذا / what:** Pick one primary transition for 60-70% of cuts plus 1-2 accents, chosen by energy (calm/medium/high) and mood (warm, cold, editorial, tech, tense, playful, dramatic, premium, retro) and narrative position (opening 0.4-0.6 s, related 0.3 s, outro 0.6-1.0 s).
- **كيف / how:** transitions/overview.md tables: calm 0.5-0.8 s sine/power1; medium 0.3-0.5 s power2/3; high 0.15-0.3 s power4/expo; blur by energy calm 20-30 px / medium 8-15 px / high 3-6 px.
- **أرقام / params:** primary 60-70%; 2-3 types per video
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/overview.md`

#### TRANS-219 · سجل الانتقالات والحقن الآلي · Transition registry and auto-injection · 📦 بأمر تثبيت
- **ماذا / what:** Five tier-B between-scene types (crossfade 0.5 s, blur-crossfade 0.6 s, push-slide 0.5 s LEFT/RIGHT/UP/DOWN, zoom-through 0.4 s, squeeze 0.4 s) with GSAP templates the harness stamps; defaults zoom-through for high energy and blur-crossfade otherwise; max 2.0 s; tier-A shared-element morph exempt.
- **كيف / how:** Planner writes '**Transition:** push-slide LEFT' per scene; transitions.mjs injects code with __OLD__/__NEW__/__T__/__DUR__/__DX__ placeholders.
- **أرقام / params:** max_duration_s 2.0
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/TRANSITION-REGISTRY.md` · `kosif-one/vendor/hyperframes/skills/faceless-explainer/scripts/transitions.mjs` · `kosif-one/vendor/hyperframes/skills/faceless-explainer/scripts/lib/transitions.json`

#### TRANS-220 · انتقالات بسرعات متطابقة · Velocity-matched transitions · 📦 بأمر تثبيت
- **ماذا / what:** Exit one beat accelerating with blur and enter the next at the matched velocity so motion reads continuous across a cut.
- **كيف / how:** techniques.md §10 (exit y -150 power in + blur; entry from matching offset out).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/techniques.md`

#### TRANS-221 · حركة إيقاعية: hypercut-whip · Beat motion primitive: hypercut-whip · 📦 بأمر تثبيت
- **ماذا / what:** Fast whip-pan hard cut between frames, anchored to music events (beat / hard_stop).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/hypercut-whip/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: beat / hard_stop; best span 0.18-0.45 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/hypercut-whip/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### TRANS-222 · حركة إيقاعية: mask-reveal · Beat motion primitive: mask-reveal · 📦 بأمر تثبيت
- **ماذا / what:** Clip-path mask wipe reveal, anchored to music events (section_start / downbeat).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/mask-reveal/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: section_start / downbeat; best span 0.5-1.2 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/mask-reveal/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### TRANS-223 · حركة إيقاعية: iris-open · Beat motion primitive: iris-open · 📦 بأمر تثبيت
- **ماذا / what:** Circular iris-open reveal, anchored to music events (section_start / reveal).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/iris-open/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: section_start / reveal; best span 0.6-1.2 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/iris-open/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### TRANS-224 · حركة إيقاعية: blur-resolve · Beat motion primitive: blur-resolve · 📦 بأمر تثبيت
- **ماذا / what:** Blur-in to crisp then blur-out on the cut, anchored to music events (stop / final hold).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/blur-resolve/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: stop / final hold; best span 0.7-2.0 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/blur-resolve/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### TRANS-225 · حركة إيقاعية: flash-cut · Beat motion primitive: flash-cut · 📦 بأمر تثبيت
- **ماذا / what:** Full-frame flash masking a state change, anchored to music events (drop / crash).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/flash-cut/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: drop / crash; best span 0-0.6 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/flash-cut/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### TRANS-226 · حركة إيقاعية: hard-cut · Beat motion primitive: hard-cut · 📦 بأمر تثبيت
- **ماذا / what:** Sample-accurate color-block + word cut, anchored to music events (beat / hard_stop).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/hard-cut/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: beat / hard_stop; best span 0 ms in; 0.3-2 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/hard-cut/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### TRANS-227 · حركة إيقاعية: staggered-exit · Beat motion primitive: staggered-exit · 📦 بأمر تثبيت
- **ماذا / what:** Ordered cascade-out clearing the frame, anchored to music events (phrase / transition).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/staggered-exit/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: phrase / transition; best span 0.4-1.2 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/staggered-exit/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### TRANS-228 · قطوعات داخل اللقطة · Within-frame seam cuts (zoom-through, inverse zoom, cut-the-curve, waterfall) · 📦 بأمر تثبيت
- **ماذا / what:** Worker-built seams: zoom-through forward (Z toward viewer, hard cut at blur peak, opacity 0.15 at cut), inverse zoom (arrival), cut-the-curve between scenes (same path same direction x 0 -> -230 then +230 -> 0 with mirrored eases), waterfall cut (per-word cut-the-curve).
- **كيف / how:** references/cut-catalog.md; peak blur 10 px for text, 18-20 px for full-frame surfaces; never two texts visible during a zoom-through.
- **أرقام / params:** 230 px travel; blur 10/20 px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/faceless-explainer/references/cut-catalog.md` · `kosif-one/vendor/hyperframes/skills/pr-to-video/references/cut-catalog.md`

#### TRANS-229 · إعادة الاستهداف بالنابض · Spring retargeting track() · 📦 بأمر تثبيت
- **ماذا / what:** Multi-target value = first value + one spring per change, still pure in t.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** MOTION.track(t,keys,SPR.firm)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### TRANS-230 · تبديل البؤرة · rackFocus · 📦 بأمر تثبيت
- **ماذا / what:** Cross-fade to a constant-blur copy; never animate a large blur.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** rackFocus
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### TRANS-231 · انتقال القزحية والفيضان · iris / flood seams · 📦 بأمر تثبيت
- **ماذا / what:** Radius-in-log-space circular reveal or colour flood.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** iris, flood
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### TRANS-232 · انقلاب ثلاثي · roll 3D flip seam · 📦 بأمر تثبيت
- **ماذا / what:** Front-loaded flip: 35% in first frame, done in 10 f.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** roll
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### TRANS-233 · قلب قطبية المسرح · polarity stage flip · 📦 بأمر تثبيت
- **ماذا / what:** Stage light/dark flips only at act boundaries riding a move.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** polarity
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### TRANS-234 · دخول تدريجي بالتعريض · Exposure fade-in from black · 📦 بأمر تثبيت
- **ماذا / what:** Instead of a black overlay, the 3D film opens by ramping tone-mapping exposure from about 12 % to full over the first second.
- **كيف / how:** renderer.toneMappingExposure = 0.95·(0.12 + 0.88·smooth(0, 1.1, t)); sound_ground fades out by ×(1−0.45·smooth(9.4,10,t)).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:247` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:132`

#### TRANS-235 · ومضة بيضاء · White flash accent · 📦 بأمر تثبيت
- **ماذا / what:** A white overlay spikes for one or two frames and settles, masking a hard change (brand flood).
- **كيف / how:** M.flash(tl, el, at, {peak:.6, dur:.3}) → 0→peak in 0.06 s, then 0 over dur power4.out; optional 'again' double flash.
- **أرقام / params:** peak 0.6, 0.3 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:83` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:325`

#### TRANS-236 · فتح قزحي من نقطة إلى اللقطة · Iris open from a point onto footage · 📦 بأمر تثبيت
- **ماذا / what:** A circular clip opens from the travelling dot to reveal full-bleed footage on the drop beat.
- **كيف / how:** M.iris(tl, '#card', b(15.8), {x:960, y:540, r0:22, r:1150, dur:.42}) – circle() clip-path animated in log space (E.iris family); dot hidden 0.05 s later; M.breathe card creep .012.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:110` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:334`

#### TRANS-237 · الكلمة كسطح انتقال · Word as the transition plane · 📦 بأمر تثبيت
- **ماذا / what:** A giant word fills the frame at the moment of a cut so the cut happens behind it, then the word flies up and shrinks into the sky of the new shot.
- **كيف / how:** 'كافح' 400 px: fromTo {x 140, scale 1.25, blur 18} → {0, 1, 0} 0.2 s expo.out at 13.12; cam set scale 1.42 at 13.30 then expo.out to 1.10; word to y −440, scale .36 in .55 s power3.inOut; bounce .40/.36 on the repeated word; exit y −470.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:260` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:133`

#### TRANS-238 · لقطة إلى بطاقة إلى انهيار إلى شعار · Footage → card → implode → lockup · 📦 بأمر تثبيت
- **ماذا / what:** One container is never cut: full-bleed footage shrinks into a rounded card beside metrics, then implodes into the dot, a beat of silence, and the lockup builds around it.
- **كيف / how:** tl.to(card, {x:−360, scale:.56, borderRadius:44px, .66 s E.inOut}); metrics x 40→0 staggered .12; implode {x:0, scale:.02, radius 600px, .38 s E.in}; lockup at b(26).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:120` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:127`

#### TRANS-239 · خاتمة بالغطس إلى الأسود · Dip to black / dip to ink ending · 📦 بأمر تثبيت
- **ماذا / what:** Films end deliberately on a dip rather than a hard stop.
- **كيف / how:** premium_edit: #dim opacity → 1 over 0.32 s power2.in at 20.06 s of 20.566; lab: #dip #0f1512 → 1 over 0.6 s linear at S−0.6; bunny: #fade → 0.85 over last 0.14 s.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:147` · `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/index.html:38` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:125`

#### TRANS-240 · شريطا السينما يفتحان ويغلقان · Cinematic letterbox open/close · 📦 بأمر تثبيت
- **ماذا / what:** Black bars at top and bottom frame the title and open as the film starts, or snap open on the first kick, and close on the end card.
- **كيف / how:** #letterbox-top/bottom height 70→0 over 2.2 s power4.inOut at min(2.4, 0.15·S); water_cycle closes 0→70 over 1.6 s at 15.4; sound_ground 120→0 in 0.55 s expo.out at 2.0 (first kick); night_boat fixed 64 px.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/index.html:33` · `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/index.html:49` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/index.html:37`

#### TRANS-241 · قطع حاد مع إعادة تأطير الكاميرا · Hard cut with camera reframe · 📦 بأمر تثبيت
- **ماذا / what:** At a story turn the virtual camera jumps to a new crop and origin and settles fast, so one plate feels like a new shot.
- **كيف / how:** tl.set(cam, {scale:1.42, x:0, y:0, transformOrigin:'585px 690px'}, 13.30).to(cam, {scale:1.10, .6 s, expo.out}, 13.30).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:133`

#### TRANS-242 · ضربة القطع: تمويه شعاعي ووميض · Cut kick (radial blur on cuts) + white flash · 📦 بأمر تثبيت
- **ماذا / what:** Every hard cut gets a 12-tap radial zoom blur that peaks on the cut and a soft radial white flash, hiding the jump and adding punch.
- **كيف / how:** ShaderPass sampling tDiffuse at c+d*(1-amt*i/11*.12) for i<12, centre (.5,.48); amt=clamp(1-|t-cut|/.16); DOM #flash radial-gradient(#fff, rgba(255,240,210,.85) 35%, transparent 75%) opacity=clamp(1-d/.1)*.55.
- **أرقام / params:** window ±0.16 s blur, ±0.10 s flash, peak .55
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html:430-434` · `kosif-one/projects/egypt-2120-animation/index.html:464-465` · `kosif-one/projects/egypt-2120-animation/index.html:475`

#### TRANS-243 · إيقاع الإظلام مع تداخل النص · Fade-through-black rhythm with overlapping text · 📦 بأمر تثبيت
- **ماذا / what:** Every shot ends in a ~0.77 s dip to black; the next line of text starts at the start of the dip, so words cross the black and the cut never feels empty.
- **كيف / how:** transitions[{after_clip,type:'fadeblack',dur,at}] at 2.3, 4.834, 8.734, 10.434, 11.934, 15.167, 18.734, 20.567, 22.601, 25.701 s; each texts[i].start = previous boundary.
- **أرقام / params:** durations 0.70-0.80 s (mostly 0.767 = 23 frames)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/mimic-jumuah/جمعة-محاكاة.raw.timeline.json` · `kosif-one/projects/mimic-jumuah/study/mimic.json`

#### TRANS-244 · شاشة مقسومة للمقارنة · Split-screen comparison with whip-in halves · 📦 بأمر تثبيت
- **ماذا / what:** Two mindsets side by side: the right half (money) and left half (joy) whip in from their edges, a gold seam grows down the middle, and each half dims while the other is named.
- **كيف / how:** Halves width 50% with 200%-wide images offset ±50%; xPercent 100 -> 0 and -100 -> 0 in 0.45 s E.whip (60 ms apart); seam 2 px linear-gradient(#0000,#f5c97a,#0000) scaleY 0 -> 1 in 0.5 s; tint rgba(0,0,0,.6) toggles at 39.95/40.82 s.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html:18-24` · `kosif-one/projects/whatsapp-motion/projects/success/index.html:267-277`

#### TRANS-245 · إظلام الختام ووميض الانتقال · Dip to black end + white flash seams · 📦 بأمر تثبيت
- **ماذا / what:** Act changes are sealed by a short warm-white flash; the film ends with a 0.6 s fade to black after the viewer question.
- **كيف / how:** M.flash(tl,#flash,24.5,{peak:.9,dur:.45}) and (42.32,{peak:.55,dur:.4}) with #fff6e0; #black opacity 0 -> 1 in 0.6 s E.smooth at 46.3 s.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html:42-43` · `kosif-one/projects/whatsapp-motion/projects/success/index.html:152-154` · `kosif-one/projects/whatsapp-motion/projects/success/index.html:285`

#### TRANS-246 · كشف دائري وفيضان لوني · Iris reveal and colour flood · 📦 بأمر تثبيت
- **ماذا / what:** A circle wipe in log space from any point (open or close), and a one-time full-frame colour flood transition built on it.
- **كيف / how:** M.iris(tl,el,at,{x,y,r:2300,r0:1,dur:.4,close}) clip-path circle with logEase; M.flood(tl,stage,at,{color:'#e4342f',x,y,dur:.3,out}).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:332-350`

#### TRANS-247 · انتقال تطبيقات الموبايل: سوايب سريع · Phone-editor transition: whip (whipleft/whipright/whipup/whipdown) · 📦 بأمر تثبيت
- **ماذا / what:** Custom transition modelling what CapCut/InShot do: whip pan with directional motion blur.
- **كيف / how:** mm_transitions.render('whip', A, B, P, **params) (custom kinds need OpenCV or SciPy here).
- **أرقام / params:** blur 0.08
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_transitions.py:1`

#### TRANS-248 · 54 انتقال xfade بالبايثون · 54 xfade transitions in Python · 📦 بأمر تثبيت
- **ماذا / what:** Python port of FFmpeg vf_xfade formulas so detected transitions replay identically: fade, wipeleft, wiperight, wipeup, wipedown, slideleft, slideright, slideup, slidedown, circlecrop, rectcrop, distance, fadeblack, fadewhite, radial, smoothleft, smoothright, smoothup, smoothdown, circleopen, circlec…
- **كيف / how:** mm_transitions.render(kind,A,B,P) with P=1 all A..0 all B
- **أرقام / params:** 54 kinds
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-mimic/scripts/mm_transitions.py:19`

#### TRANS-249 · ويب يسار · Phone-editor transition: whipleft · 📦 بأمر تثبيت
- **ماذا / what:** Custom model of CapCut/InShot-style 'whipleft' transition, replayable with a measured progress curve.
- **كيف / how:** mm_transitions.render('whipleft',A,B,P)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-mimic/scripts/mm_transitions.py:26`

#### TRANS-250 · ويب يمين · Phone-editor transition: whipright · 📦 بأمر تثبيت
- **ماذا / what:** Custom model of CapCut/InShot-style 'whipright' transition, replayable with a measured progress curve.
- **كيف / how:** mm_transitions.render('whipright',A,B,P)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-mimic/scripts/mm_transitions.py:26`

#### TRANS-251 · ويب أعلى · Phone-editor transition: whipup · 📦 بأمر تثبيت
- **ماذا / what:** Custom model of CapCut/InShot-style 'whipup' transition, replayable with a measured progress curve.
- **كيف / how:** mm_transitions.render('whipup',A,B,P)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-mimic/scripts/mm_transitions.py:26`

#### TRANS-252 · ويب أسفل · Phone-editor transition: whipdown · 📦 بأمر تثبيت
- **ماذا / what:** Custom model of CapCut/InShot-style 'whipdown' transition, replayable with a measured progress curve.
- **كيف / how:** mm_transitions.render('whipdown',A,B,P)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-mimic/scripts/mm_transitions.py:26`

#### TRANS-253 · وميض · Flash frame · 📦 بأمر تثبيت
- **ماذا / what:** A white (or any) overlay flash with optional double flicker.
- **كيف / how:** MOTION.flash(tl, overlayEl, at, {peak, dur, again}).
- **أرقام / params:** peak .85 in .06 s, decay .35 s power4.out; again: .5 peak at +.16 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:325`

#### TRANS-254 · انتقال القزحية · Iris wipe · 📦 بأمر تثبيت
- **ماذا / what:** Reveals or hides an element through a growing/shrinking circle from a point, radius in log space.
- **كيف / how:** MOTION.iris(tl, el, at, {x, y, r, r0, dur, close}).
- **أرقام / params:** R 2300 px, r0 1 px, dur .4 s, E.out (open) / E.in (close)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:334`

#### TRANS-255 · قلب ثلاثي الأبعاد · Front-loaded 3D roll · 📦 بأمر تثبيت
- **ماذا / what:** A rotationX flip that does ~35% in the first frame and finishes in ~10 frames.
- **كيف / how:** MOTION.roll(tl, el, at, {from, dur, origin, perspective}).
- **أرقام / params:** from -90°, dur .17 s, E.out, origin 50% 100%, parent perspective 2200 px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:362`

#### TRANS-256 · تسلسل اللقطات · Shot list sequence with hard cuts · 📦 بأمر تثبيت
- **ماذا / what:** A list [{at, shot}] becomes one camera function with hard cuts and moves starting at each cut.
- **كيف / how:** const seq = K3.sequence([{at:0, shot:'establishing'}, {at:2.5, shot:'low angle tracking'}], {seconds}); K3.applyShot(cam, seq(t)).
- **أرقام / params:** no crossfades
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:1210`

#### TRANS-257 · انتقالات القزحية والبطاقة والانضغاط · Iris / card / implode transitions (showreel) · 📦 بأمر تثبيت
- **ماذا / what:** One-container transitions instead of cuts: an iris opens from a dot onto real footage, the footage shrinks into a rounded card beside facts, then everything implodes back into the dot.
- **كيف / how:** motion-kit M.iris(tl, el, t, {x,y,r0,r,dur}); gsap scale/borderRadius on #card
- **أرقام / params:** iris r0 22 → r 1150 in 0.42 s; card x −360 scale 0.56 radius 44 px over 0.66 s; implode scale 0.02 radius 600 px in 0.38 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/showreel/index.html:110` · `kosif-studio/motion/projects/showreel/index.html:120` · `kosif-studio/motion/projects/showreel/index.html:127`

#### TRANS-258 · الكلمة المفتاحية كمستوى انتقال · Keyword as transition plane · 📦 بأمر تثبيت
- **ماذا / what:** In a directed talking-head edit, the strongest content word nearest a shot cut becomes a full-frame typographic plane that carries the cut (e.g. 'كافح' at 400 px).
- **كيف / how:** direct.plan → chapters [{t, text}]; template draws the plane; premium_edit shows it by hand
- **أرقام / params:** candidate words −0.8/+0.2 s around the cut; score = stress − 2.5·|Δt|; keys within −1.2/+0.6 s removed
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/direct.py:185` · `kosif-studio/motion/projects/premium_edit/index.html:1`

#### TRANS-259 · تلاشي حواف المشهد · sceneFade edge fades · 📦 بأمر تثبيت
- **ماذا / what:** Every scene fades in and out over 10 frames with easeOutCubic.
- **كيف / how:** sceneFade(frame,length,edge=10)
- **أرقام / params:** 10 frames (333 ms at 30 fps)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/starters/remotion/src/Film.tsx:64`

#### TRANS-260 · إطارات تحت المقاطع · Poster frames under clips with zoom · 📦 بأمر تثبيت
- **ماذا / what:** First frames from MP4 sit under video, fade in second half of previous leg and scale 1+0.06*progress so swap is invisible.
- **أرقام / params:** scale 1.06
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/mcp-higgsfield-landing/src/scripts/world.ts:90`

#### TRANS-261 · لقطات بإطار أول وأخير (انتقال تحوّلي) · First-and-last-frame keyframe shots (AI morph transition) · 🔑 مفتاح/خدمة
- **ماذا / what:** Give the video model a start image and an end image and let it invent the motion between them; ideal for scene-to-scene morph transitions or time-lapses.
- **كيف / how:** Kling image2video with image + image_tail; Together frame_images with frame 'first' and 'last' on Veo 2.0, Kling 2.1 Pro, Seedance, PixVerse, Vidu. Generate both stills with the same model/style first; keep 5 s; cut the clip in as the transition.
- **أرقام / params:** 5 s typical; Kling image_tail excludes camera_control/masks
- **الدليل / proof:** `kosif-atlas/skills/1874-klingai-pack/6075-klingai-image-to-video` · `kosif-atlas/skills/3214-togetherai-skills/13597-together-video`

#### TRANS-262 · بطاقة اقتباس فوق مشهد باهت · Quote card over hazed scene · 👁 شوهد في فيديو
- **ماذا / what:** fade a white veil over the world to ~70%, scale in a rounded white card with ink border, reveal quote text, then reverse (text first, then card)
- **أرقام / params:** veil 400 ms, card 350 ms, radius 24 px
- **الدليل / proof:** `style:doodle`

#### TRANS-263 · انتقال بالعبور من فتحة · Zoom-through-hole transition · 👁 شوهد في فيديو
- **ماذا / what:** exponential scale around hole centre (s = e^(k t)); next scene rendered full frame and clip-path: circle(holeRadius*s) until it exceeds the diagonal
- **أرقام / params:** ~1 s, k so 1->40x
- **الدليل / proof:** `style:fake3d`

#### TRANS-264 · عبور السحاب كانتقال · Cloud fly-through transition · 👁 شوهد في فيديو
- **ماذا / what:** large blurred white cloud sprites scale up and pass the camera while the map zooms, masking a big camera change
- **أرقام / params:** blur 20-40px, ~1 s
- **الدليل / proof:** `style:map-journey`

#### TRANS-265 · شريط فيلم ينزلق · Sliding film strip · 👁 شوهد في فيديو
- **ماذا / what:** row of frame cards with sprocket holes translating horizontally at constant speed, each showing a slightly later state of the animation
- **أرقام / params:** ~200 px/s, 4-5 visible frames
- **الدليل / proof:** `style:plotter`

#### TRANS-266 · كشف بدائرة قزحية · Circle iris reveal · 👁 شوهد في فيديو
- **ماذا / what:** clip-path circle grows from centre (with a thin ring ahead of it) revealing the next solid-colour scene
- **أرقام / params:** radius 0 -> 120% diagonal, 400-500 ms easeInOutCubic
- **الدليل / proof:** `style:pm-0xfemyn-e114d3`

#### TRANS-267 · مسح بثلاث شرائح لونية · Tri-band panel wipe · 👁 شوهد في فيديو
- **ماذا / what:** Three full-height bands (brand orange, black, cream) slide across in sequence, the last one becomes the new ground
- **أرقام / params:** band offset 80-100 ms, 500 ms easeInOutQuart
- **الدليل / proof:** `style:pm-0xfemyn-e114d3`

#### TRANS-268 · مسح دائري ناعم من النقطة · Soft circle iris wipe from focal point · 👁 شوهد في فيديو
- **ماذا / what:** clip-path circle (or radial mask) centred on the dot, radius 0→hypot(w,h) with feathered edge
- **أرقام / params:** 300 ms, expo.in-out, feather 20 px
- **الدليل / proof:** `style:pm-1littlecoder-9fef89`

#### TRANS-269 · إيقاع حقول لونية · Colour-field cut rhythm · 👁 شوهد في فيديو
- **ماذا / what:** full-bleed palette swap each beat 120 bpm
- **الدليل / proof:** `style:pm-3xtihor-0f6911`

#### TRANS-270 · كلمات فوق تكبير شديد للرسم · Macro zoom word beats · 👁 شوهد في فيديو
- **ماذا / what:** Cut rapidly between extreme close-ups of the drawings (scale 6-10x, paper texture visible) clipped by a large circle edge, on flat saturated colour fields, with one word of a sentence per cut
- **أرقام / params:** cut every 0.5-1 s, word fade 100 ms, slow push during shot
- **الدليل / proof:** `style:pm-abderrahmen-g-9e8ed0`

#### TRANS-271 · قطع كلمات المزايا السريع · Rapid feature word cuts · 👁 شوهد في فيديو
- **ماذا / what:** each feature word full-frame 0.25 s, alternate black/yellow fields
- **الدليل / proof:** `style:pm-adamdesgns-478d6d`

#### TRANS-272 · مسح نقطي دائري · Halftone ring wipe · 👁 شوهد في فيديو
- **ماذا / what:** dot grid with radial scale gradient opening a window
- **الدليل / proof:** `style:pm-adamdesgns-478d6d`

#### TRANS-273 · مسح قطري بألواح ملوّنة · Diagonal panel wipe · 👁 شوهد في فيديو
- **ماذا / what:** 2-3 skewed rectangles in light-to-deep blue sweep across the frame with 60 ms offsets, revealing the next scene behind
- **أرقام / params:** skewX -25deg, 400 ms easeInOutQuart
- **الدليل / proof:** `style:pm-agonaliu-466a8f`

#### TRANS-274 · لافتة الدور · Turn banner · 👁 شوهد في فيديو
- **ماذا / what:** full-width strip slides across with label
- **أرقام / params:** 400 ms
- **الدليل / proof:** `style:pm-aisongman-71ffac`

#### TRANS-275 · مسح بخطوط قطرية · Diagonal stripe wipe · 👁 شوهد في فيديو
- **ماذا / what:** 3-4 violet tint bands slide across 400 ms
- **الدليل / proof:** `style:pm-aistocksavvy-3fb9f5`

#### TRANS-276 · عد تنازلي بأسلوب شريط السينما · Film-leader countdown · 👁 شوهد في فيديو
- **ماذا / what:** double circle, crosshair lines, grey wedge sweeping 360° per second, big numeral swapping each sweep; end on white flash
- **أرقام / params:** 1 s per number; flash 2-3 frames
- **الدليل / proof:** `style:pm-ajith-io-4c248f`

#### TRANS-277 · اختراق بخطوط سرعة · Zoom-through speed lines · 👁 شوهد في فيديو
- **ماذا / what:** scale object up while radial pencil lines converge, white-out
- **أرقام / params:** 800ms ease-in
- **الدليل / proof:** `style:pm-ajith-io-ea7f2d`

#### TRANS-278 · مسح شرائط قوس قزح · Rainbow stripe wipe · 👁 شوهد في فيديو
- **ماذا / what:** 6 stripes slide in staggered with dashed edges
- **أرقام / params:** stagger 60ms
- **الدليل / proof:** `style:pm-ajith-io-ea7f2d`

#### TRANS-279 · انتقال بالتلاشي إلى الخلفية · Fade-through-ground scene change · 👁 شوهد في فيديو
- **ماذا / what:** Fade all scene elements to 0 (~500 ms) leaving the flat ground, short hold, then build next scene
- **أرقام / params:** out 500 ms, gap 200-400 ms
- **الدليل / proof:** `style:pm-alex-prompter-1ea044`

#### TRANS-280 · تقلص الشبكة إلى هاتف · Window grid to device · 👁 شوهد في فيديو
- **ماذا / what:** FLIP animate grid windows to single phone screen
- **أرقام / params:** 800 ms
- **الدليل / proof:** `style:pm-amol909s-27533e`

#### TRANS-281 · مفتاح أوضاع بمسح نقطي · Mode toggle with dither wipe · 👁 شوهد في فيديو
- **ماذا / what:** segmented control: active segment orange; switching animates a dithered wipe between segments
- **أرقام / params:** 300 ms
- **الدليل / proof:** `style:pm-anthonyriera-9b1b2a`

#### TRANS-282 · انقضاض تكبير داخل بطاقة حتى ملء الشاشة · Whip zoom into tile to full-bleed · 👁 شوهد في فيديو
- **ماذا / what:** zoom camera into a grid tile with zoom/motion blur; interpolate tile corner radius to 0 as it reaches full frame so the hand-off to the full-res video is seamless; start the full-res clip with a match
- **كيف / how:** zoom camera into a grid tile with zoom/motion blur; interpolate tile corner radius to 0 as it reaches full frame so the hand-off to the full-res video is seamless; start the full-res clip with a matching offset
- **أرقام / params:** ~500 ms, radius 12->0 px, blur peak 20 px
- **الدليل / proof:** `style:pm-antonio-kodheli-490109`

#### TRANS-283 · قطع مطابق بالعودة إلى البطاقة · Match cut back into source tile · 👁 شوهد في فيديو
- **ماذا / what:** reverse the whip: scale the playing full-bleed video down into its tile position in the grid while the grid fades into view around it
- **أرقام / params:** ~600 ms ease-in-out
- **الدليل / proof:** `style:pm-antonio-kodheli-490109`

#### TRANS-284 · ومضات بطاقات العلامات · Rapid brand-card flashes · 👁 شوهد في فيديو
- **ماذا / what:** hard cut through 5-6 full-frame cards at a fixed 250 ms grid (8 beats at 120 BPM)
- **أرقام / params:** cut interval 0.25 s
- **الدليل / proof:** `style:pm-arjunsh1607-93005d`

#### TRANS-285 · تتابع كلمات بقطع سريع · Cut-burst word sequence · 👁 شوهد في فيديو
- **ماذا / what:** 4-6 giant words, each 0.25 s, alternating dark/orange fields
- **الدليل / proof:** `style:pm-astrodevil-3f2054`

#### TRANS-286 · مونتاج سريع لنطاق الأساليب · Style-range rapid montage · 👁 شوهد في فيديو
- **ماذا / what:** Hard-cut through 4 full-bleed style cards (Swiss grid / halftone / op-art / glitch), each 0.25-0.5 s, labelled 'STYLE 0N — NAME'
- **أرقام / params:** cuts on 8th notes at 130 BPM (~230 ms)
- **الدليل / proof:** `style:pm-ayushunleashed-ece3e3`

#### TRANS-287 · كشف الصورة من نقطة تتضخم · Dot-to-disc portrait reveal · 👁 شوهد في فيديو
- **ماذا / what:** Accent dot scales up to a large disc, then the disc becomes a circular mask revealing the photo with an accent ring
- **أرقام / params:** scale 1->30 in 400 ms easeInOut, ring 8 px
- **الدليل / proof:** `style:pm-blushpetal795-0c85c2`

#### TRANS-288 · مسح بنقاط الحبر الإلكتروني · E-ink dither wipe · 👁 شوهد في فيديو
- **ماذا / what:** Ordered/Bayer dither mask sweeping left->right; pixels inside the front band flicker between old and new text before settling
- **أرقام / params:** band width ~15% frame, sweep 350-450 ms, pixel size 4-6 px
- **الدليل / proof:** `style:pm-bogdandragomir-35e024`

#### TRANS-289 · توسيع العنصر المشترك (الغلاف) · Shared-element artwork expand · 👁 شوهد في فيديو
- **ماذا / what:** FLIP the same artwork from list thumbnail rect to centred hero rect, then slide left as details reveal on the right
- **أرقام / params:** 500-700 ms easeOutQuart
- **الدليل / proof:** `style:pm-brainextends-e19ac3`

#### TRANS-290 · مسح درجي بكسلي · Pixel stair wipe · 👁 شوهد في فيديو
- **ماذا / what:** stepped column mask advances across frame
- **أرقام / params:** 0.5 s
- **الدليل / proof:** `style:pm-buildfastwithai-53234e`

#### TRANS-291 · مسح ضوئي قبل/بعد · Light-bar before/after sweep · 👁 شوهد في فيديو
- **ماذا / what:** Bright vertical glowing bar travels across a card; left of the bar shows the improved 'after' state, right still shows the grey blurred 'before' with red X issues
- **أرقام / params:** sweep 600-800 ms, bar 8 px with 40 px glow
- **الدليل / proof:** `style:pm-ceowinkz-7c776b`

#### TRANS-292 · سهم النمو يطير إلى الشعار · Growth chart arrow fly-off to logo · 👁 شوهد في فيديو
- **ماذا / what:** Line chart with monthly ticks draws with node dots and gradient area; an arrowhead rides the line tip, then detaches and flies to become the arrow of the brand logo in the end card
- **أرقام / params:** chart 1.2 s, arrow fly 400 ms
- **الدليل / proof:** `style:pm-ceowinkz-7c776b`

#### TRANS-293 · قطع بانقلاب الفاتح والداكن · Light/dark inversion cuts · 👁 شوهد في فيديو
- **ماذا / what:** alternate chapters between paper-light and charcoal grounds with hard cuts to create rhythm
- **أرقام / params:** 4-5 inversions in 15 s
- **الدليل / proof:** `style:pm-chatgptastra-0d95c7`

#### TRANS-294 · مسح بقرص يتمدد · Disc expand wipe · 👁 شوهد في فيديو
- **ماذا / what:** circle scale from point to cover screen 400 ms
- **الدليل / proof:** `style:pm-codestackr-c071bf`

#### TRANS-295 · قلب فاتح داكن · Light/dark flip · 👁 شوهد في فيديو
- **ماذا / what:** invert ground on beat
- **الدليل / proof:** `style:pm-davidmarcus-a28a60`

#### TRANS-296 · انتقال بالتغبيش بين الفصول · Blur-dissolve chapter change · 👁 شوهد في فيديو
- **ماذا / what:** outgoing elements animate filter blur 0→12 px + opacity 1→0 while incoming go blur 12→0, ~400 ms overlap
- **أرقام / params:** ease-out cubic
- **الدليل / proof:** `style:pm-ddryo-loos-300829`

#### TRANS-297 · انتقال دائري من داخل الرقم · Digit iris transition · 👁 شوهد في فيديو
- **ماذا / what:** A disc in the next scene's colour grows from the counter of a digit (the '0') until it covers the frame, revealing the new background
- **أرقام / params:** radius 0->diag, 400 ms easeIn, ring stroke accent
- **الدليل / proof:** `style:pm-deebeeeff-50fcd0`

#### TRANS-298 · استعراض السمات بقطعات سريعة · Theme roll call cuts · 👁 شوهد في فيديو
- **ماذا / what:** hard cut each beat to the same game view in a different skin with label 'COURT 0N / 06 · TYPE' and a giant city name bottom-left
- **أرقام / params:** 1 s per skin, 4-6 skins
- **الدليل / proof:** `style:pm-deifosv-04e4d3`

#### TRANS-299 · بداية ونهاية بتلاشٍ من السواد وإليه · Fade-from/to-black bookends · 👁 شوهد في فيديو
- **ماذا / what:** Open and close a contemplative piece with ~1 s black fades instead of logo cards
- **أرقام / params:** 1 s linear opacity
- **الدليل / proof:** `style:pm-demitiyageekzen-7770ad`

#### TRANS-300 · مسح ورقي ممزق · Torn paper wipe · 👁 شوهد في فيديو
- **ماذا / what:** jagged-edge polygon sweeping diagonally 500 ms
- **الدليل / proof:** `style:pm-devius-maximus-beab45`

#### TRANS-301 · مسح لوني كامل كفاصل · Full-bleed colour wipe interstitial · 👁 شوهد في فيديو
- **ماذا / what:** Brand-blue panel slides over the scene, hosts a two-line statement, then wipes off to the next chapter
- **أرقام / params:** in 450 ms, hold ~2.5 s, out 450 ms; colour #0b58d4
- **الدليل / proof:** `style:pm-elliot-garreffa-f334bc`

#### TRANS-302 · غوص داخل شاشة متداخلة · Nested-screen dive (recursive zoom) · 👁 شوهد في فيديو
- **ماذا / what:** each scene renders the next scene live inside a screen rect; animate scale so the inner rect fills the frame, then swap; reverse for return
- **أرقام / params:** ~0.8-1.2 s per dive, ease-in-out
- **الدليل / proof:** `style:pm-emollick-8661a8`

#### TRANS-303 · مسح ختامي كريمي · Cream end wipe · 👁 شوهد في فيديو
- **ماذا / what:** Full rect slides in from side
- **أرقام / params:** 500 ms
- **الدليل / proof:** `style:pm-gdgtify-287ddf`

#### TRANS-304 · تذويب بكسلي · Pixel mosaic dissolve · 👁 شوهد في فيديو
- **ماذا / what:** sample frame into blocks of growing size or randomly replace blocks with flat palette tiles; ease block size 2->32px
- **أرقام / params:** 400-700 ms
- **الدليل / proof:** `style:pm-gizakdag-b8c59e`

#### TRANS-305 · تكرار نص متشوه · Glitch type tiling · 👁 شوهد في فيديو
- **ماذا / what:** repeat word rows with RGB offset, shift
- **الدليل / proof:** `style:pm-gizakdag-cf4ae6`

#### TRANS-306 · انتقال مسح بالشرائط · Stripe wipe transition · 👁 شوهد في فيديو
- **ماذا / what:** stacked full-width coloured bands translate down across frame in sequence 60 ms apart, revealing next scene
- **أرقام / params:** total 400 ms, easeInOutQuart
- **الدليل / proof:** `style:pm-gonzalomacagno-2de1a9`

#### TRANS-307 · ثمانية انتقالات في مازورة · Beat-locked transition bar · 👁 شوهد في فيديو
- **ماذا / what:** At 128 BPM fire one transition per eighth note (~234 ms) for a full bar: iris circle grow, alternating inset block wipe, spin +270 deg inside a diamond mask, etc.; each carries a one-word title naming
- **كيف / how:** At 128 BPM fire one transition per eighth note (~234 ms) for a full bar: iris circle grow, alternating inset block wipe, spin +270 deg inside a diamond mask, etc.; each carries a one-word title naming itself and a mono caption 'T05 SPIN · rotate +270° · diamond mask'
- **أرقام / params:** 8 transitions x 234 ms
- **الدليل / proof:** `style:pm-grace-sunnyy-29bc61`

#### TRANS-308 · قطع بالكتل اللونية · Colour-block cut · 👁 شوهد في فيديو
- **ماذا / what:** each cut swaps full background among 3-4 flat colours
- **أرقام / params:** on beat
- **الدليل / proof:** `style:pm-hanifproduktif-54bdee`

#### TRANS-309 · مسح لوني صلب · Solid colour wipe · 👁 شوهد في فيديو
- **ماذا / what:** full rectangle slides in from top 350ms then reveals next scene
- **الدليل / proof:** `style:pm-hqmank-7c61f1`

#### TRANS-310 · دوران سريع وتصغير لخريطة المستويات · World-map whip and zoom-out · 👁 شوهد في فيديو
- **ماذا / what:** Pan the camera horizontally fast with directional blur, then scale out to reveal all previous scenes as glowing thumbnails in a grid
- **أرقام / params:** whip 300ms blur 30px; zoom-out 600ms
- **الدليل / proof:** `style:pm-ibrahimwasim240-809370`

#### TRANS-311 · مسح بشاشة منقسمة · Split-screen wipe · 👁 شوهد في فيديو
- **ماذا / what:** vertical accent line divides two images
- **الدليل / proof:** `style:pm-imthatcarlos-e04bfe`

#### TRANS-312 · مرور عمود أمامي ضبابي · Foreground pole whoosh · 👁 شوهد في فيديو
- **ماذا / what:** Every 2-3 s a tall semi-transparent dark vertical bar sweeps across the window very fast with horizontal blur to sell speed
- **أرقام / params:** width 40 px, cross in 250 ms, blur 20 px, opacity 0.4
- **الدليل / proof:** `style:pm-itsolelehmann-e47532`

#### TRANS-313 · انتقال بالنفق المظلم · Tunnel wipe scene change · 👁 شوهد في فيديو
- **ماذا / what:** A tunnel portal wall then darkness scrolls in from the right, covers the window for ~0.5 s while the season state is swapped behind it, then the new scene scrolls in
- **أرقام / params:** ~1.5 s total, mid dark hold 0.3-0.5 s
- **الدليل / proof:** `style:pm-itsolelehmann-e47532`

#### TRANS-314 · مسح بأشرطة لونية · Colour stripe wipe · 👁 شوهد في فيديو
- **ماذا / what:** 8 vertical stripes drop from top (or rise) with staggered timing, colours cycling orange/cream/blue, covering the frame and revealing the next chapter
- **أرقام / params:** stagger 40-60 ms, each 250 ms expo-out
- **الدليل / proof:** `style:pm-jasonzhou1993-8595e0`

#### TRANS-315 · صورة تطير من المحادثة إلى المستند · Image flies into document slot · 👁 شوهد في فيديو
- **ماذا / what:** Duplicate the generated image, animate its bounding box from chat thumbnail to the email hero slot (FLIP), then flash a 4-point sparkle
- **أرقام / params:** 700 ms easeInOutQuart; sparkle scale 0 -> 1 -> 0 over 500 ms
- **الدليل / proof:** `style:pm-justincooperman-e7bbc4`

#### TRANS-316 · قواعد مشاهد مبنية على التلاشي · Fade-driven scene grammar · 👁 شوهد في فيديو
- **ماذا / what:** use dips to black (1-2 s) to mark time jumps and location changes instead of cuts; reveal each scene by its own light source
- **أرقام / params:** ease in-out sine
- **الدليل / proof:** `style:pm-kamstudiolabs-0b0824`

#### TRANS-317 · نهاية بالغوص في الشعار · Zoom-through logo ending · 👁 شوهد في فيديو
- **ماذا / what:** Camera pushes into the logo tile until it fills the frame, then resolve to a clean name card with role line and URL pill that the cursor clicks
- **أرقام / params:** push 800 ms, card fade 400 ms
- **الدليل / proof:** `style:pm-kikelopezdesign-7cc9e8`

#### TRANS-318 · جليتش بانفصال القنوات وشرائح أفقية · RGB-split slice glitch · 👁 شوهد في فيديو
- **ماذا / what:** Draw text in R, G, B offsets ±6-12 px plus random horizontal band displacements and duplicate ghost letters for 2-6 frames between scenes
- **أرقام / params:** bands 4-8, offset up to 40px, duration 100-200 ms
- **الدليل / proof:** `style:pm-kloss-xyz-15182a`

#### TRANS-319 · ومضة خاطفة تمهّد لما بعدها · Glitch flash-frame foreshadow · 👁 شوهد في فيديو
- **ماذا / what:** insert 1-3 frames of the next chapter (pixel-font word on grey) between collapse and title cut to create a subliminal jolt
- **أرقام / params:** 33-100 ms
- **الدليل / proof:** `style:pm-kloss-xyz-b9b3f6`

#### TRANS-320 · انتقال بقلب الثيم مع ضبابية · Theme-flip blur crossfade · 👁 شوهد في فيديو
- **ماذا / what:** outgoing scene blurs 0->12 px and fades while incoming scene starts at 12 px blur and sharpens; alternate dark and light scenes to create rhythm
- **أرقام / params:** ~400 ms
- **الدليل / proof:** `style:pm-kmasiff-cc72cb`

#### TRANS-321 · قطع عبر بوابة الجسم · Portal object match-cut · 👁 شوهد في فيديو
- **ماذا / what:** render next scene inside a circular mask (watch glass/lens); when mask diameter exceeds frame diagonal swap to the full next scene
- **أرقام / params:** circular mask, swap at mask>=1.05*diagonal
- **الدليل / proof:** `style:pm-koldo2k-5cff87`

#### TRANS-322 · دخول عنوان بسرعة مع ضبابية حركة · Whip-in headline with motion blur · 👁 شوهد في فيديو
- **ماذا / what:** headline enters from off-frame horizontally in ~200 ms with directional blur that resolves to sharp; previous card exits same direction
- **أرقام / params:** blur 20->0 px horizontal, ease-out expo
- **الدليل / proof:** `style:pm-kyonax-on-tech-aabc1d`

#### TRANS-323 · خروج سوطي بضبابية حركة · Motion-blur whip exit · 👁 شوهد في فيديو
- **ماذا / what:** Wordmark slides quickly sideways with directional blur proportional to velocity
- **أرقام / params:** blur 30 px horizontal, 250 ms
- **الدليل / proof:** `style:pm-leonkohli-6dc01b`

#### TRANS-324 · تتابع سحب سريع · Whip relay · 👁 شوهد في فيديو
- **ماذا / what:** fast horizontal motion-blur slide between samples
- **أرقام / params:** ~300 ms
- **الدليل / proof:** `style:pm-lexnlin-6161a6`

#### TRANS-325 · تقلّص الصورة إلى بطاقة · Hero shrinks into card · 👁 شوهد في فيديو
- **ماذا / what:** Animate a full-frame image to a rounded-corner card (radius 0 -> 24 px, scale 1 -> 0.85) to reveal the UI or gallery around it
- **أرقام / params:** 500-700 ms easeInOut
- **الدليل / proof:** `style:pm-listudio-820c7b`

#### TRANS-326 · خط أرض مستمر · Continuous ground line · 👁 شوهد في فيديو
- **ماذا / what:** single line persists across scenes as anchor
- **الدليل / proof:** `style:pm-loicrambo-ad6830`

#### TRANS-327 · تكبير عبر قناع دائري · Circle mask zoom-through · 👁 شوهد في فيديو
- **ماذا / what:** scale circle mask from device into full frame
- **الدليل / proof:** `style:pm-macrohou-33959d`

#### TRANS-328 · وميض سالب · Negative flash · 👁 شوهد في فيديو
- **ماذا / what:** invert to white ground with dark text for 1-2 frames on a hit
- **أرقام / params:** 2 frames
- **الدليل / proof:** `style:pm-majin-appsheet-2d3c1a`

#### TRANS-329 · تلاشي بين الخطوات · Dim-out step crossfade · 👁 شوهد في فيديو
- **ماذا / what:** Finished card and caption drop to ~30% opacity and fade while the next step's chip and card fade in; no cuts
- **أرقام / params:** 500-700 ms
- **الدليل / proof:** `style:pm-majorbaguette-fb11d7`

#### TRANS-330 · ضربة كلمة بتشويش ألوان RGB · RGB split glitch slam · 👁 شوهد في فيديو
- **ماذا / what:** render word three times in red/blue/white with offsets ±6 px and random horizontal slice displacement, decay to 0 over 200 ms; scale 1.2→1
- **أرقام / params:** mix-blend screen, 2-3 slices
- **الدليل / proof:** `style:pm-maxalexweber-67688b`

#### TRANS-331 · ومضة ضوء بيضاء بإضاءة بقعية · Spotlight bloom white-out · 👁 شوهد في فيديو
- **ماذا / what:** flash to a white field shaped like a soft spotlight with dark vignette corners, then cut; used to reset between sections
- **أرقام / params:** 2-6 frames, vignette 40%
- **الدليل / proof:** `style:pm-micheleharmonic-77628e`

#### TRANS-332 · تقطيع وميضي · Strobe cut burst · 👁 شوهد في فيديو
- **ماذا / what:** 5+ cuts within 0.5 s before finale
- **الدليل / proof:** `style:pm-monokern-ade5b6`

#### TRANS-333 · انتقال لوح لوني للفصل · Chapter colour slam · 👁 شوهد في فيديو
- **ماذا / what:** Full-bleed flat colour panel scales/slides in over 150-250 ms to open each chapter; next chapter uses a new brand colour
- **أرقام / params:** easeOutExpo, 4-5 rotating colours
- **الدليل / proof:** `style:pm-motiondsgnr-9dcfa6`

#### TRANS-334 · انتقال جليتش بفصل الألوان · RGB-split glitch transition · 👁 شوهد في فيديو
- **ماذا / what:** offset R/G/B channels and slice horizontal bands with random x shifts for 3-6 frames
- **أرقام / params:** offset 6-12 px
- **الدليل / proof:** `style:pm-ndhabarde11-f155b4`

#### TRANS-335 · انتقال بالبياض الشمسي · Sun whiteout bridge · 👁 شوهد في فيديو
- **ماذا / what:** Push into a bloomed sun until the frame clips to warm white, hold 0.5 s, then cut to black scene
- **أرقام / params:** exposure ramp 1.5s
- **الدليل / proof:** `style:pm-nolkeeg-bf062e`

#### TRANS-336 · إمالة سريعة مع وميض لوني · Whip-tilt with tint flash · 👁 شوهد في فيديو
- **ماذا / what:** Accelerate the whole scene upward to ~25 px/frame with vertical blur while tinting toward light blue; cut; new page arrives low and smeared and decays into place
- **أرقام / params:** flash #e2f4fe fading in 6 frames
- **الدليل / proof:** `style:pm-notdwd-7de38a`

#### TRANS-337 · صفحة تنزلق للأعلى بلطخة · Smear scroll-in page · 👁 شوهد في فيديو
- **ماذا / what:** page starts ~400 px low with 24px blur, offsets decay geometrically (×0.75/frame) to 0 and blur to ~1.5 px; one key phrase set in black 600 among grey body
- **أرقام / params:** settle ~20 frames
- **الدليل / proof:** `style:pm-notdwd-c2037d`

#### TRANS-338 · بطاقات صادمة بانعكاس الألوان · Colour-inversion beat cards · 👁 شوهد في فيديو
- **ماذا / what:** hard cut to a full black frame with white bold claim for the hook and the manifesto, then hard cut back to white page
- **أرقام / params:** hold 2-2.5 s, words rise per word
- **الدليل / proof:** `style:pm-palashbagchi11-0a4b6b`

#### TRANS-339 · انتقال بمسح دائري · Circle wipe scene change · 👁 شوهد في فيديو
- **ماذا / what:** brand-coloured circle/ring expands from off-frame to cover and reveal the next scene
- **أرقام / params:** ~400 ms easeInOutQuart
- **الدليل / proof:** `style:pm-paulo-kombucha-96431c`

#### TRANS-340 · كلمة تنشق بخط مائل · Slash-split word · 👁 شوهد في فيديو
- **ماذا / what:** thin line draws diagonally across frame; word clipped into two polygons along the line, halves offset a few px in opposite directions
- **أرقام / params:** line 2px white, 120 ms draw
- **الدليل / proof:** `style:pm-prasenx-8d9323`

#### TRANS-341 · انفجار كلمات سريع · Rapid word-cut burst · 👁 شوهد في فيديو
- **ماذا / what:** each tool word 250 ms on new colour field
- **الدليل / proof:** `style:pm-quickdesignio-dd93d0`

#### TRANS-342 · مسح بشبكة مربعات · Tile grid wipe · 👁 شوهد في فيديو
- **ماذا / what:** rounded squares scale 0→1 stagger diagonal 15 ms
- **الدليل / proof:** `style:pm-quickdesignio-dd93d0`

#### TRANS-343 · قطع متبادل بين الشيفرة والصورة · Code↔visual cut bursts · 👁 شوهد في فيديو
- **ماذا / what:** Alternate cuts every 0.6-1 s at drop
- **الدليل / proof:** `style:pm-rames-jusso-589f80`

#### TRANS-344 · شريط مائل يدخل بقوة · Diagonal banner slam · 👁 شوهد في فيديو
- **ماذا / what:** rotated -15deg band slides across with text
- **أرقام / params:** 400 ms
- **الدليل / proof:** `style:pm-rneayan-474bcf`

#### TRANS-345 · ومضات صور سريعة بملء الشاشة · Rapid full-screen image flashes · 👁 شوهد في فيديو
- **ماذا / what:** Cut full-bleed images on every 16th note leading into a music drop, with a click SFX per change; caption typed over in white
- **أرقام / params:** ~115 ms per image, 6-10 images
- **الدليل / proof:** `style:pm-rossaxbt-3085b7`

#### TRANS-346 · انتقال بضبابية وتكبير · Blur-zoom dissolve · 👁 شوهد في فيديو
- **ماذا / what:** outgoing scene scales 1 -> 1.04 and blurs 0 -> 12 px while fading; incoming scene does the reverse
- **أرقام / params:** 500-700 ms total
- **الدليل / proof:** `style:pm-sachaarbonel-8f14f4`

#### TRANS-347 · كشف واجهة المحرر بالتراجع · Editor pull-out reveal · 👁 شوهد في فيديو
- **ماذا / what:** Scale the current scene down into a preview window inside a mock NLE: layer list, spring graph, waveform track and clip chips with playhead
- **أرقام / params:** scale 1->0.6 in 600 ms, UI fades in staggered 40 ms
- **الدليل / proof:** `style:pm-sahildesigner23-ee3155`

#### TRANS-348 · كشف دائري من علامة تصويب · Iris reticle reveal · 👁 شوهد في فيديو
- **ماذا / what:** Small reticle circle with centre dot expands into a soft-edged bright disc that fills the frame
- **أرقام / params:** radius 20 px -> 120% frame, feather 40 px, 500 ms
- **الدليل / proof:** `style:pm-sahildesigner23-ee3155`

#### TRANS-349 · انتقال بقناع دائري · Iris circle transition · 👁 شوهد في فيديو
- **ماذا / what:** clip-path circle shrinks/expands from content to dark ground, with a dotted ring outside
- **أرقام / params:** ~400 ms ease-in-out
- **الدليل / proof:** `style:pm-samaote-5e2fc2`

#### TRANS-350 · انتقال سحب بتمويه حركة · Motion-blur whip transition · 👁 شوهد في فيديو
- **ماذا / what:** Translate the whole scene group ~60% width in 200 ms with expo ease and apply horizontal blur proportional to velocity (CSS filter blur 0->20px->0 or multi-sample); next scene enters from the opposite
- **كيف / how:** Translate the whole scene group ~60% width in 200 ms with expo ease and apply horizontal blur proportional to velocity (CSS filter blur 0->20px->0 or multi-sample); next scene enters from the opposite side
- **أرقام / params:** 200-250 ms, blur max 20 px, ease expo.inOut
- **الدليل / proof:** `style:pm-samuel-yostt-891f87`

#### TRANS-351 · مسح لوني دائري عملاق · Circular colour-field wipe · 👁 شوهد في فيديو
- **ماذا / what:** Huge circles of flat colour sweep across the frame in sequence to change the ground colour
- **أرقام / params:** 300-400ms; 2-3 layered colours
- **الدليل / proof:** `style:pm-shinskinakamoto-20190b`

#### TRANS-352 · انتقال جليتش شرائحي · Slice glitch transition · 👁 شوهد في فيديو
- **ماذا / what:** offset horizontal strips randomly by +/-40 px, split RGB channels, flash 3-5 frames, then cut to next scene
- **أرقام / params:** 0.3-0.5 s, 6-12 strips
- **الدليل / proof:** `style:pm-shneural-2abdfa`

#### TRANS-353 · مسح بدائرة متنامية · Circle grow wipe · 👁 شوهد في فيديو
- **ماذا / what:** dot scales to fill frame revealing next colour
- **أرقام / params:** 350 ms expo-in
- **الدليل / proof:** `style:pm-souravbhar871-61f424`

#### TRANS-354 · خطوط تشويش ملونة للخاتمة · RGB glitch line end card · 👁 شوهد في فيديو
- **ماذا / what:** Thin horizontal coloured lines streak across the frame randomly behind the wordmark; brief chromatic offset on text
- **أرقام / params:** lines 1-2 px, life 200 ms, RGB offset 2 px
- **الدليل / proof:** `style:pm-spearwtf-3c1fd1`

#### TRANS-355 · قطع بقلب الألوان · Colour-flip hard cuts · 👁 شوهد في فيديو
- **ماذا / what:** alternate full-field bg colours per scene on beat
- **أرقام / params:** black/red/blue/cream
- **الدليل / proof:** `style:pm-stephanlivera-df17a2`

#### TRANS-356 · مونتاج كلمات على الإيقاع · Beat word-card montage · 👁 شوهد في فيديو
- **ماذا / what:** single word per card, hard cut every 250 ms, colour-tinted word
- **الدليل / proof:** `style:pm-steventey-0d20e4`

#### TRANS-357 · كروت تطير بضبابية حركة · Whip-out cards with motion blur · 👁 شوهد في فيديو
- **ماذا / what:** translate and rotate cards off-frame in 250 ms with directional blur proportional to velocity (CSS filter blur or sampled frames)
- **أرقام / params:** rotateZ 8-12 deg, blur up to 12 px
- **الدليل / proof:** `style:pm-sudeepsd-1a3485`

#### TRANS-358 · اهتزاز فصل ألوان · RGB split stutter · 👁 شوهد في فيديو
- **ماذا / what:** offset R/B copies ±8px, cuts every ~120ms
- **الدليل / proof:** `style:pm-sudo-kiran-49176d`

#### TRANS-359 · مسح السبورة بالممحاة بين الفصول · Eraser chapter wipe · 👁 شوهد في فيديو
- **ماذا / what:** eraser sprite sweeps zig-zag across the board while a reveal mask clears the drawing layer behind it
- **أرقام / params:** ~0.8-1.2 s, then 0.5 s blank before next title
- **الدليل / proof:** `style:pm-tak3sh8-be5012`

#### TRANS-360 · مسح الشاشة بشرائط ملونة · Full-screen stripe wipe · 👁 شوهد في فيديو
- **ماذا / what:** 8-9 horizontal bars in palette colours scaleX 0→1 from alternating sides with 30 ms stagger, then exit
- **أرقام / params:** each bar 350 ms expo.inOut
- **الدليل / proof:** `style:pm-tequilafunks-97f6c9`

#### TRANS-361 · انتقال دائرة لونية متوسعة · Iris circle colour wipe · 👁 شوهد في فيديو
- **ماذا / what:** A solid circle in the next scene's ground colour scales from a point to cover the frame, soft-edged, with faint inner rings
- **أرقام / params:** 400-500 ms easeInOut
- **الدليل / proof:** `style:pm-teslachartz-c58b32`

#### TRANS-362 · مسح دائري يغمر الشاشة بلون · Circle wipe colour flood · 👁 شوهد في فيديو
- **ماذا / what:** Clip-path circle grows from centre (r 0 -> 120% diagonal) in accent colour over ~400 ms easeInOut, carrying a blurred badge
- **أرقام / params:** clip-path: circle(); 400ms
- **الدليل / proof:** `style:pm-thilina-a-891c09`

#### TRANS-363 · دائرة تتمدد وتغمر الشاشة · Iris circle flood · 👁 شوهد في فيديو
- **ماذا / what:** brand-colour circle scales from an icon until it covers the frame diagonal, becoming the next background
- **أرقام / params:** 350-450 ms ease-in
- **الدليل / proof:** `style:pm-thismacapital-dfba20`

#### TRANS-364 · مسح بشريط مائل إلى صورة · Diagonal band wipe to photo · 👁 شوهد في فيديو
- **ماذا / what:** skewed brand-colour band sweeps across revealing full-bleed photo; giant white title masks up from bottom-left
- **أرقام / params:** skew 20 deg, 400 ms
- **الدليل / proof:** `style:pm-thismacapital-dfba20`

#### TRANS-365 · تفكك بكسلي · Pixelation dissolve · 👁 شوهد في فيديو
- **ماذا / what:** Downsample frame into growing blocks then cut
- **أرقام / params:** block 4→64 px
- **الدليل / proof:** `style:pm-tolgayhickiran-e90799`

#### TRANS-366 · مسح غلتش شرائحي · Glitch slice wipe · 👁 شوهد في فيديو
- **ماذا / what:** Horizontal bands offset x randomly, colour blocks
- **أرقام / params:** 300 ms
- **الدليل / proof:** `style:pm-topi-003-9ca6b5`

#### TRANS-367 · عبور زووم داخل الصورة · Zoom-through image portal · 👁 شوهد في فيديو
- **ماذا / what:** scale card until it fills frame, swap to full-bleed photo
- **أرقام / params:** scale 1→6
- **الدليل / proof:** `style:pm-twoclipping-221cab`

#### TRANS-368 · تبديل المحتوى بضبابية قصيرة · Blur content swap · 👁 شوهد في فيديو
- **ماذا / what:** outgoing content blur 0->6px & opacity 1->0 over 120 ms; incoming starts 60 ms later with blur 6->0 & opacity 0->1
- **أرقام / params:** total ~200 ms
- **الدليل / proof:** `style:pm-twoclipping-5cba86`

#### TRANS-369 · كشف بعدسة دائرية · Circular lens reveal · 👁 شوهد في فيديو
- **ماذا / what:** clip-path circle growing with blurred rim exposing new layer
- **أرقام / params:** ~600 ms
- **الدليل / proof:** `style:pm-twoclipping-6dd14e`

#### TRANS-370 · كشف بطاقة ملونة · Colour card reveal · 👁 شوهد في فيديو
- **ماذا / what:** lime rectangle scales then content card zooms
- **الدليل / proof:** `style:pm-ultimaxbt-2ddf1e`

#### TRANS-371 · نقطة بطلة تربط المشاهد · Hero dot match-cut · 👁 شوهد في فيديو
- **ماذا / what:** keep a single dot at same screen pos across cuts while bg changes
- **الدليل / proof:** `style:pm-ultimaxbt-bbebf5`

#### TRANS-372 · عبور بتكبير لوني · Zoom-through colour wipe · 👁 شوهد في فيديو
- **ماذا / what:** scale circle/bar to fill frame 400 ms
- **الدليل / proof:** `style:pm-utopyaszx-1b2f94`

#### TRANS-373 · مسح بأشرطة ألوان أساسية · Primary-colour stripe wipe · 👁 شوهد في فيديو
- **ماذا / what:** vertical bars of red/blue/yellow/black slide horizontally at different speeds with motion blur, revealing next card
- **أرقام / params:** 8-12 bars, 300-500 ms, stagger 30 ms
- **الدليل / proof:** `style:pm-vanshwtfff-db0466`

#### TRANS-374 · انتقال سوط ضبابي · Whip motion-blur transition · 👁 شوهد في فيديو
- **ماذا / what:** horizontal blur slide 300 ms
- **الدليل / proof:** `style:pm-visheshbaghell-3aba37`

#### TRANS-375 · قطع حاد بين الظلام والنور · Hard dark/light section flip · 👁 شوهد في فيديو
- **ماذا / what:** cut instantly from #06050a scene to #f8f7ff scene on a beat, with a reverse-suck SFX leading into it
- **أرقام / params:** cut on frame, SFX peak aligned
- **الدليل / proof:** `style:product`

#### TRANS-376 · انتقال بشكل مشترك · Shared-shape scene handover · 📄 موصوف
- **ماذا / what:** Last frame of a scene equals next scene's first; a dot grows into a pill then a card; no cut, no crossfade.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md` · `kosif-studio/motion/references/motion-craft.md`

#### TRANS-377 · قاعدة: الانتقال هو الخروج · Scene rules: transition is the exit · 📄 موصوف
- **ماذا / what:** In multi-scene pieces every element enters with an animation, no element exits before the transition, and only the final scene fades out.
- **كيف / how:** Every scene: one entrance tween per element (vary at least 3 eases per scene, offset first motion 0.1-0.3s); no gsap.to(...opacity:0) before the cut; transition takes the full outgoing frame.
- **أرقام / params:** first offset 0.1-0.3s; >=3 eases per scene
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/SKILL.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions.md`

#### TRANS-378 · اختيار الانتقال حسب الطاقة · Transition by energy table · 📄 موصوف
- **ماذا / what:** Choose one primary transition (60-70% of cuts) plus 1-2 accents according to the piece's energy.
- **كيف / how:** Calm: blur crossfade/focus pull 0.5-0.8s sine.inOut; medium: push slide/staggered blocks 0.3-0.5s power2-3; high: zoom-through/overexposure 0.15-0.3s power4/expo. Opening = most distinctive 0.4-0.6s; related points 0.3s; climax boldest; outro slowest 0.6-1.0s.
- **أرقام / params:** calm 0.5-0.8s; medium 0.3-0.5s; high 0.15-0.3s
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions.md`

#### TRANS-379 · معنى كل انتقال · Transition meaning map · 📄 موصوف
- **ماذا / what:** A cut type communicates a relation: crossfade continues, hard cut wakes up, slow dissolve drifts, push = next point, staggered blocks = new section.
- **كيف / how:** Use hard cuts deliberately for register shifts; don't crossfade everything; mood map: warm->light leak/blur; clinical->squeeze/blinds/grid; editorial->push/diagonal split; tech->grid dissolve/glitch; tense->VHS/chromatic; playful->elastic push/iris; cinematic->zoom through/dip to black.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/motion-principles.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions.md`

#### TRANS-380 · إعدادات انتقال جاهزة · Transition presets · 📄 موصوف
- **ماذا / what:** Six named duration/ease presets for scene changes.
- **كيف / how:** snappy 0.2s power4.inOut; smooth 0.4s power2.inOut; gentle 0.6s sine.inOut; dramatic 0.5s power3.in->out; instant 0.15s expo.inOut; luxe 0.7s power1.inOut.
- **أرقام / params:** 0.15-0.7s
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions.md`

#### TRANS-381 · شدة ضبابية الانتقال · Blur crossfade intensity · 📄 موصوف
- **ماذا / what:** Blur-through dissolve whose blur radius, duration and hold scale with energy.
- **كيف / how:** Calm 20-30px over 0.8-1.2s hold 0.3-0.5s; medium 8-15px 0.4-0.6s hold 0.1-0.2s; high 3-6px 0.2-0.3s no hold. CSS filter:blur on scene containers via GSAP.
- **أرقام / params:** 20-30 / 8-15 / 3-6 px
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions.md`

#### TRANS-382 · فتحة دائرية وقطع قطري · Clip-path iris & diagonal split · 📄 موصوف
- **ماذا / what:** Reveal the next scene through a growing circle/diamond mask or slice the outgoing scene away diagonally.
- **كيف / how:** fromTo clipPath 'circle(0% at 50% 50%)' -> 'circle(75% at 50% 50%)' 0.5s power2.out; diamond polygon(50% -20%,120% 50%,50% 120%,-20% 50%); diagonal split: outgoing scene zIndex 10 with polygon tween 0.5s power3.inOut. Clock wipe = 9-point polygon stepped through 4 quadrant tweens.
- **أرقام / params:** iris 0.5s; circle to 75%
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions/css-radial.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions/catalog.md`

#### TRANS-383 · تشويش رقمي وانحراف لوني · Glitch / chromatic / VHS / ripple · 📄 موصوف
- **ماذا / what:** Digital breakdown cuts built from RGB-split overlays, jitter frames and sliced strips.
- **كيف / how:** Glitch: 6 jitter frames at 0.03s, offsets +-30-60px, RGB overlays normal blend 35% opacity (not multiply). Chromatic: R/B copies spread +-80px over 0.3s then converge. Ripple: +-30px oscillation, scale 0.97-1.03, rising blur, swap at peak. VHS: 20 cloned strips 54px tall, 2020px wide at left:-50px, seeded offsets.
- **أرقام / params:** jitter 0.03s x6; +-80px; 20 strips x 54px
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions/css-distortion.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions/catalog.md`

#### TRANS-384 · ستائر وكتل متتابعة · Blinds / staggered blocks / grid dissolve · 📄 موصوف
- **ماذا / what:** Cover the frame with full-size panels or slats that sweep in a stagger, then reveal the next scene.
- **كيف / how:** Blinds count by energy: calm 4 horizontal/6 vertical, medium 6-8h/8v, high 12-16h/16v; staggered blocks are full 1920x1080 panels; grid dissolve cycles 5 palette colors per cell. Avoid visible regular geometric repetition patterns.
- **أرقام / params:** 4/6-8/12-16 slats
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions/catalog.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions.md`

#### TRANS-385 · تبديل اللقطات عند حدود الجمل · B-roll swap at sentence boundaries · 📄 موصوف
- **ماذا / what:** When one screen has been held past the style's maximum, switch to another B-roll or screen capture at a sentence boundary where a noun or action is spoken, while the voice continues uninterrupted.
- **كيف / how:** Max same-screen run: 8 s (essay), 6 s (reflection), 40 s (project); keep longer holds only for reading code/documents or intended lingering, with a logged reason; if no replacement exists, mark for review instead of padding.
- **أرقام / params:** 8 s / 6 s / 40 s by style
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2453-davinciresolve-cut-devtalk/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2461-davinciresolve-style-essay/SKILL.md`

#### TRANS-386 · MG-001 انتقال داخل شكل مطابق · MG-001 Shape-matched zoom-through · 📄 موصوف
- **ماذا / what:** Two shots sharing a round element (cup rim -> camera lens) are joined by scaling into the circle of shot A and emerging from the matching circle of shot B.
- **كيف / how:** Match circle centre and diameter first. 0-0.6 s hold, 0.6-1.2 s scale up with a circular mask (CSS clip-path:circle()) and light blur, cut at peak, 1.2-2 s ease out of shot B. Match light direction or the cut shows. Short air-push SFX. Local: HTML <video> layers in KOSIF or ffmpeg crop/scale expressions.
- **أرقام / params:** 2 s: 0-0.6 / 0.6-1.2 / 1.2-2.0
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-transitions.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### TRANS-387 · MG-002 ستارة من جسم عابر · MG-002 Foreground body wipe · 📄 موصوف
- **ماذا / what:** A person or object close to the lens crosses frame and hides the cut; the new location is revealed behind its trailing edge.
- **كيف / how:** 0-0.5 s approach, 0.5-1 s full occlusion, 1-1.5 s reveal. Animated mask follows the body edge with shot B underneath; hair and motion-blur edges need manual cleanup (tracking alone is not enough). Local: keyframed SVG mask path, or a segmentation matte (SAM/rembg - needs install).
- **أرقام / params:** 1.5 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-transitions.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### TRANS-388 · MG-003 نقلة باندفاع جانبي · MG-003 Whip push inside directional blur · 📄 موصوف
- **ماذا / what:** Shot slides sideways and the cut is hidden at the moment of maximum motion blur, in the same direction on both sides.
- **كيف / how:** 0-0.25 s accelerate, cut inside 0.25-0.45 s, settle to 0.8 s. Local ffmpeg: animated crop/overlay x with ease expression plus dblur (directional blur, present in this ffmpeg 6.1) ramped up/down, or xfade=slideleft + gblur; one whoosh.
- **أرقام / params:** 0.8 s; cut window 0.25-0.45 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-transitions.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### TRANS-389 · MG-005 حبر يفتح المشهد · MG-005 Ink-bloom luma-matte reveal · 📄 موصوف
- **ماذا / what:** An ink drop spreads across the screen until the next shot fills it.
- **كيف / how:** 0-0.4 s drop, 0.4-1.3 s spread, 1.3-1.8 s fill. Use an ink clip (or a procedural growing noise blob on canvas) as luma matte; push contrast so the matte reaches pure white - holes otherwise remain. ffmpeg: maskedmerge with the matte stream after eq/curves.
- **أرقام / params:** 1.8 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-transitions.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### TRANS-390 · MG-006 شرائح بسرعات متتابعة · MG-006 Staggered slat wipe · 📄 موصوف
- **ماذا / what:** Five vertical strips each pull the new image in with a short delay, then fuse.
- **كيف / how:** 0-0.2 s prep, 0.2-0.9 s slats, 0.9-1.2 s merge; each strip delayed 2-3 frames. Pre-align the image inside every strip (background-position offsets). Local: 5 divs with translateY + animation-delay = i x 2-3 frames.
- **أرقام / params:** 1.2 s; 5 slats; 2-3 frame stagger
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-transitions.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### TRANS-391 · MG-008 انتقال بإيقاف الحركة · MG-008 Stop-motion shrink to sticker · 📄 موصوف
- **ماذا / what:** Frame freezes and shrinks in four jumps into a sticker sitting over the next scene - a handmade cut for ads.
- **كيف / how:** 0-0.4 s freeze, 0.4-1.2 s four hold-key jumps, 1.2-1.6 s settle with a simple shadow; no motion blur (it ruins the stop-motion read). Local: WAAPI with steps(4) easing or stepped keyframes; ffmpeg freeze via tpad.
- **أرقام / params:** 1.6 s; 4 steps
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-transitions.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### TRANS-392 · MG-009 موجة تشوه تعبر القطع · MG-009 Displacement wave across the cut · 📄 موصوف
- **ماذا / what:** A ripple starts in the centre and rolls over the cut point; fits water or heat scenes.
- **كيف / how:** 0-0.4 s start, 0.4-0.9 s peak distortion and cut, 0.9-1.5 s fade. Keep strength limited so faces and package text don't break. Local: SVG feTurbulence + feDisplacementMap with animated scale 0->N->0, or ffmpeg displace with generated sine maps.
- **أرقام / params:** 1.5 s; peak 0.4-0.9
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-transitions.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### TRANS-393 · MG-010 الانتقال عبر إطار مجمد وطي الورقة والباب · MG-010 Freeze-frame 2.5D hop (with page fold and door portal) · 📄 موصوف
- **ماذا / what:** The shot freezes into a hanging print; a camera travels to another print that comes alive (time jump). Same 2.5D family: MG-004 a paper corner folds over to reveal the next clip (two fake-3D panels with shadows), MG-007 a door plane is tracked and the next location corner-pinned into the opening.
- **كيف / how:** MG-010: 0-1 s freeze, 1-2.5 s camera move, 2.5-4 s play; the frozen frame must equal the first frame of the moving clip. MG-004: 0-0.7 lift corner, 0.7-1.4 fold passes, 1.4-2 flatten (approximation, not cloth sim). MG-007: 0-1 approach, 1-2 reveal opening, 2-3 enter; perspective and occlusion matter more than glow. Local: CSS 3D cards with ffmpeg-extracted stills.
- **أرقام / params:** 4 s / 2 s / 3 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-transitions.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### TRANS-394 · قص الصمت حسب نوع المحتوى · Genre-aware silence trimming · 📄 موصوف
- **ماذا / what:** Decide how hard to cut pauses by content type: ambient/relaxing keeps silences of 15 s+ and cuts under 20%; action trims pauses of 500 ms+ and may cut up to 40%; speech-driven cuts only at semantic boundaries; visual-first keeps wordless scenes and cuts only true silence; mixed narrative cuts only w…
- **كيف / how:** Local reimplementation: ffmpeg silencedetect=noise=-30dB:d=0.5 + scdet / select='gt(scene,0.3)' motion profile + sentence ends from words.json -> EDL -> ffmpeg concat; keep an old->new time map for captions. (The hosted VidSeeds feature is paid.)
- **أرقام / params:** ambient: >=15 s tolerance, <20% cut; action: >=0.5 s pauses, <=40% cut
- **الدليل / proof:** `kosif-atlas/skills/932-vidseeds/2178-vidseeds/skills/vidseeds-local-video/SKILL.md`

#### TRANS-395 · قص دقيق للإطار بإعادة الترميز · Frame-accurate trim by re-encode · 📄 موصوف
- **ماذا / what:** When the cut must be frame-exact (or for any standalone deliverable) re-encode from the in-point rather than stream-copy, otherwise the head freezes until the next keyframe. Smart-cut (re-encode only the boundary GOP) is the middle ground.
- **كيف / how:** ffmpeg -ss 00:00:05 -i in.mp4 -to 00:00:10 -c:v libx264 -crf 18 -c:a aac out.mp4 (Remotion exposes the same ffmpeg via npx remotion ffmpeg)
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/ffmpeg.md` · `kosif-atlas/skills/235-mas-video-lab/756-losslesscut/SKILL.md`

#### TRANS-396 · دمج المقاطع بقائمة concat · Concat list join · 📄 موصوف
- **ماذا / what:** Join many segments in order from a text list; stream copy when codecs match, re-encode once when they do not or when timing must add up exactly.
- **كيف / how:** segments.txt with lines file 'a.mp4' ; ffmpeg -f concat -safe 0 -i segments.txt -c copy -movflags +faststart merged.mp4 ; or filter_complex concat=n=N:v=1:a=1 for mixed sources
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/756-losslesscut/SKILL.md` · `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/assembly-and-review.md`

#### TRANS-397 · سياسة القص التلقائي حسب النوع · Genre-aware auto-trim policy · 📄 موصوف
- **ماذا / what:** Trim aggressiveness depends on genre: ambient/relax tolerates 15 s+ silence and cuts <20%; action trims pauses ≥500 ms up to 40% cut ratio; speech-driven cuts at semantic boundaries; visual-first keeps silent scenes and cuts only true silence; tutorial trims precisely and never speeds through instru…
- **كيف / how:** Classify via silencedetect + frame-diff motion + transcript; then apply thresholds
- **أرقام / params:** see what
- **الدليل / proof:** `kosif-atlas/skills/932-vidseeds/2181-vidseeds-local-video/SKILL.md`

#### TRANS-398 · قطع J و L للأصوات · J-cut / L-cut ambience · 📄 موصوف
- **ماذا / what:** Bring next scene's ambience in early (J) or let the previous tail linger (L) to bridge cuts.
- **كيف / how:** Offset audio vs video edit points by 6-24 frames in ffmpeg/Remotion Sequence.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound`

#### TRANS-399 · عودة الموسيقى بذيل ورايزر · Music re-entry with tail & riser · 📄 موصوف
- **ماذا / what:** Preserve reverb tail when music stops; land reverse swells/risers on the next downbeat or scene.
- **كيف / how:** Reverse a copy of the hit (areverse) and end at target; never overwrite originals.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound`

#### TRANS-400 · الانتقال بين مقطوعتين · Song A to B transition · 📄 موصوف
- **ماذا / what:** Switch at phrase ends/emotion change; crossfade if key/BPM compatible, else short tail -> ambience/silence -> new song.
- **كيف / how:** acrossfade; check key/tempo compatibility.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound`

#### TRANS-401 · كشف تدريجي من البكسلة · Progressive depixelation reveal · 📄 موصوف
- **ماذا / what:** Reveal an image by halving pixel size in power-of-two steps.
- **كيف / how:** Shader/canvas: level = 2^k pixel size stepping to 1 over 0.6-1s.
- **أرقام / params:** sizes 64->1
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`

#### TRANS-402 · قواعد الانتقالات في قاعدة المخرج · Director KB transition rules (12) · 📄 موصوف
- **ماذا / what:** When-to-use guidance for hard cut, J/L cut, match cut, whip, zoom-through, flash (disabled), shake, dissolve, fade-to-black, jump cut, glitch and AI morph.
- **كيف / how:** DIRECTOR_KB.transitions: hard cut default 90%+; J/L audio lead/trail 0.3-1.5 s; whip 0.15-0.3 s blur; zoom-through 1.5-2x; shake 0.15-0.3 s ~2%; dissolve 0.5-1.5 s; fade black 0.5-1.5 s; glitch 2-6 frames.
- **الدليل / proof:** `app/public/js/10_studio.js:8`

#### TRANS-403 · لا مزج متلاشي — القطع بمطابقة السرعة · No crossfades / velocity-matched cut · 📄 موصوف
- **ماذا / what:** Half of changes are hard cuts on grid; rest via camera, morph, match cut, flood, 1–2 f blends; 6–8 transition types ≤2 uses each + one signature move at open/middle/close.
- **كيف / how:** Apply as defaults while authoring; verify with kmotion measure/speed/sheet
- **أرقام / params:** accelerate out, cut at peak speed, next shot moving same direction
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`

#### TRANS-404 · تسرب ضوئي عند القطع · Light-leak cut transition · 📄 موصوف
- **ماذا / what:** A warm light leak drifts across each section cut (alternating direction) instead of a flat flash.
- **كيف / how:** verse.html with footage plate and FX3D; otherwise #flash #FFF6E4 0.42 -> 0 in 0.5 s.
- **أرقام / params:** radial rgba(255,176,80,.75)->rgba(255,120,40,.25)->0; opacity .85 in .28 s from xPercent -45 scale 1.2, out .7 s; screen blend
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/verse.html:40` · `100-superskills/skills/kosif-montage-motion/templates/verse.html:186`

#### TRANS-405 · تراكب لقطات B-roll بانتقال ذائب · B-roll overlay with crossfade · 📄 موصوف
- **ماذا / what:** Cover silence or abstract explanation with supporting footage or a 3D insert dissolved in over the A-roll.
- **كيف / how:** Documented only (montage_spec layer 1, crossfade_0.3s); smart_montage accepts broll_clips but never uses them. Implement with ffmpeg overlay=enable='between(t,6,9.5)' + fade=t=in:st=6:d=0.3:alpha=1 or xfade=transition=fade:duration=0.3.
- **أرقام / params:** crossfade 0.3 s
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/montage_spec.json` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/montage_grammar.md` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/smart_montage.py:156`

#### TRANS-406 · قواعد الانتقالات · Transition grammar: no crossfades, velocity-matched cuts · 📄 موصوف
- **ماذا / what:** About half of beat changes are hard cuts on the grid; the rest ride camera moves, morphs, match cuts, floods or 1-2 f blends; 6-8 transition types per film each <= 2 uses plus one signature move at open, middle and close.
- **كيف / how:** Plan transitions in the beat sheet; kit seams iris/flood/rackFocus/roll/morphPath/polarity.
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/references/craft-numbers.md` · `kosif-one/tools/kosif-studio/motion/references/motion-craft.md`

#### TRANS-407 · قاعدة معنى الانتقال · Transition meaning rule · 📄 موصوف
- **ماذا / what:** Each transition carries meaning; max two transition types per film.
- **كيف / how:** Hard cut = change/wake up; fade = continuation; slow dissolve = drift; wipe/push = spatial move; zoom-through = enter; burn/light leak = memory/time.
- **أرقام / params:** max 2 types
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md` · `100-superskills/skills/davinci-resolve-pipeline/references/transitions-catalog.md`

#### TRANS-408 · انتقالات push · CSS/GSAP push transitions · 📄 موصوف
- **ماذا / what:** HTML/GSAP transition family 'push': push slide, vertical push, elastic push, squeeze.
- **كيف / how:** Scene containers after the first start opacity:0; GSAP timeline reveals; outgoing above incoming (z-index) for drop/scale-out/diagonal split.
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/transitions-catalog.md`

#### TRANS-409 · انتقالات radial · CSS/GSAP radial transitions · 📄 موصوف
- **ماذا / what:** HTML/GSAP transition family 'radial': circle iris, diamond iris, diagonal split.
- **كيف / how:** Scene containers after the first start opacity:0; GSAP timeline reveals; outgoing above incoming (z-index) for drop/scale-out/diagonal split.
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/transitions-catalog.md`

#### TRANS-410 · انتقالات 3D · CSS/GSAP 3D transitions · 📄 موصوف
- **ماذا / what:** HTML/GSAP transition family '3D': card flip.
- **كيف / how:** Scene containers after the first start opacity:0; GSAP timeline reveals; outgoing above incoming (z-index) for drop/scale-out/diagonal split.
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/transitions-catalog.md`

#### TRANS-411 · انتقالات scale · CSS/GSAP scale transitions · 📄 موصوف
- **ماذا / what:** HTML/GSAP transition family 'scale': zoom through, zoom out.
- **كيف / how:** Scene containers after the first start opacity:0; GSAP timeline reveals; outgoing above incoming (z-index) for drop/scale-out/diagonal split.
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/transitions-catalog.md`

#### TRANS-412 · انتقالات dissolve · CSS/GSAP dissolve transitions · 📄 موصوف
- **ماذا / what:** HTML/GSAP transition family 'dissolve': crossfade, blur crossfade, focus pull, color dip.
- **كيف / how:** Scene containers after the first start opacity:0; GSAP timeline reveals; outgoing above incoming (z-index) for drop/scale-out/diagonal split.
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/transitions-catalog.md`

#### TRANS-413 · انتقالات cover · CSS/GSAP cover transitions · 📄 موصوف
- **ماذا / what:** HTML/GSAP transition family 'cover': staggered blocks, horizontal blinds, vertical blinds.
- **كيف / how:** Scene containers after the first start opacity:0; GSAP timeline reveals; outgoing above incoming (z-index) for drop/scale-out/diagonal split.
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/transitions-catalog.md`

#### TRANS-414 · انتقالات light · CSS/GSAP light transitions · 📄 موصوف
- **ماذا / what:** HTML/GSAP transition family 'light': light leak, overexposure burn, film burn.
- **كيف / how:** Scene containers after the first start opacity:0; GSAP timeline reveals; outgoing above incoming (z-index) for drop/scale-out/diagonal split.
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/transitions-catalog.md`

#### TRANS-415 · انتقالات distortion · CSS/GSAP distortion transitions · 📄 موصوف
- **ماذا / what:** HTML/GSAP transition family 'distortion': glitch, chromatic aberration, ripple, VHS.
- **كيف / how:** Scene containers after the first start opacity:0; GSAP timeline reveals; outgoing above incoming (z-index) for drop/scale-out/diagonal split.
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/transitions-catalog.md`

#### TRANS-416 · انتقالات mechanical · CSS/GSAP mechanical transitions · 📄 موصوف
- **ماذا / what:** HTML/GSAP transition family 'mechanical': shutter, clock wipe.
- **كيف / how:** Scene containers after the first start opacity:0; GSAP timeline reveals; outgoing above incoming (z-index) for drop/scale-out/diagonal split.
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/transitions-catalog.md`

#### TRANS-417 · انتقالات grid · CSS/GSAP grid transitions · 📄 موصوف
- **ماذا / what:** HTML/GSAP transition family 'grid': grid dissolve.
- **كيف / how:** Scene containers after the first start opacity:0; GSAP timeline reveals; outgoing above incoming (z-index) for drop/scale-out/diagonal split.
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/transitions-catalog.md`

#### TRANS-418 · انتقالات other · CSS/GSAP other transitions · 📄 موصوف
- **ماذا / what:** HTML/GSAP transition family 'other': gravity drop, morph circle, blur through, page burn.
- **كيف / how:** Scene containers after the first start opacity:0; GSAP timeline reveals; outgoing above incoming (z-index) for drop/scale-out/diagonal split.
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/transitions-catalog.md`

#### TRANS-419 · قواعد الانتقالات الصلبة · Transition hard rules (HTML) · 📄 موصوف
- **ماذا / what:** Full-frame block overlays; RGB glitch at 35% normal blend not multiply; light leak >=2400px with no visible shape; VHS clones real scene + red/blue copies, seeded noise; page burn hides via tl.set and clipPath:none on return; clock wipe = 9-point polygon, 4 tweens; blinds by energy (calm 4H/6V, mid …
- **كيف / how:** GSAP
- **أرقام / params:** 35%, 2400px, blind counts
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/transitions-catalog.md`

#### TRANS-420 · انتقالات Remotion · Remotion TransitionSeries · 📄 موصوف
- **ماذا / what:** Remotion transitions shorten total duration (60+60-15=105); overlays don't.
- **كيف / how:** <TransitionSeries> with presentation fade()/slide(direction)/wipe()/flip()/clockWipe(), linearTiming({durationInFrames:15}) or springTiming({config:{damping:200}})
- **أرقام / params:** 15 frames, damping 200
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/transitions-catalog.md`

#### TRANS-421 · معاني الانتقالات · Transition semantics · 📄 موصوف
- **ماذا / what:** Crossfade = continues, hard cut = wake up, slow dissolve = drift; don't dissolve everything.
- **كيف / how:** Choose transition by narrative intent.
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/references/motion-rules.md`

#### TRANS-422 · سلسلة التحول بجسم حامل · Carrier-object transformation chain · 📄 موصوف
- **ماذا / what:** One object inherits through every scene; incoming scene visible while outgoing still 25-50%; no fade-to-empty.
- **كيف / how:** Plan in scenes.json.
- **أرقام / params:** overlap 25-50%
- **الدليل / proof:** `100-superskills/skills/motion-director-pro/SKILL.md`

#### TRANS-423 · قاعدة انتقالين · Two-transition rule · 📄 موصوف
- **ماذا / what:** Hard cut for change, fade/dissolve for continuity; no more than 2 transition types.
- **كيف / how:** ffmpeg xfade/concat
- **الدليل / proof:** `100-superskills/skills/video-editing-captions/SKILL.md:22`

#### TRANS-424 · قواعد الانتقالات · Transition grammar (no crossfades) · 📄 موصوف
- **ماذا / what:** How beat changes are carried in top films.
- **كيف / how:** Mostly hard cuts on the grid; seams from the kit (iris, flood, rackFocus, roll, morphPath, polarity).
- **أرقام / params:** ~50% hard cuts; 6-8 transition types per film, each ≤ 2 uses, one signature move at open/middle/close; velocity-matched cut (accelerate out, cut at peak speed, next shot moving the same direction); blends only 1-2 f
- **الدليل / proof:** `kosif-studio/motion/references/craft-numbers.md`

#### TRANS-425 · انتقال: قطع · Transition key: cut · 📄 موصوف
- **ماذا / what:** Named transition in the PLAN vocabulary (cut); implemented per film in the starter scene code.
- **كيف / how:** declare in PLAN.md transitions table with duration (ms) and curve, then code in scene draw()
- **الدليل / proof:** `kosif-tool/templates/PLAN.md`

#### TRANS-426 · انتقال: مسح · Transition key: wipe · 📄 موصوف
- **ماذا / what:** Named transition in the PLAN vocabulary (wipe); implemented per film in the starter scene code.
- **كيف / how:** declare in PLAN.md transitions table with duration (ms) and curve, then code in scene draw()
- **الدليل / proof:** `kosif-tool/templates/PLAN.md`

#### TRANS-427 · انتقال: تحول · Transition key: morph · 📄 موصوف
- **ماذا / what:** Named transition in the PLAN vocabulary (morph); implemented per film in the starter scene code.
- **كيف / how:** declare in PLAN.md transitions table with duration (ms) and curve, then code in scene draw()
- **الدليل / proof:** `kosif-tool/templates/PLAN.md`

#### TRANS-428 · انتقال: كشف بالقناع · Transition key: mask-reveal · 📄 موصوف
- **ماذا / what:** Named transition in the PLAN vocabulary (mask-reveal); implemented per film in the starter scene code.
- **كيف / how:** declare in PLAN.md transitions table with duration (ms) and curve, then code in scene draw()
- **الدليل / proof:** `kosif-tool/templates/PLAN.md`

#### TRANS-429 · انتقال: زووم عابر · Transition key: zoom-through · 📄 موصوف
- **ماذا / what:** Named transition in the PLAN vocabulary (zoom-through); implemented per film in the starter scene code.
- **كيف / how:** declare in PLAN.md transitions table with duration (ms) and curve, then code in scene draw()
- **الدليل / proof:** `kosif-tool/templates/PLAN.md`

#### TRANS-430 · انتقال: قطع مطابق · Transition key: match-cut · 📄 موصوف
- **ماذا / what:** Named transition in the PLAN vocabulary (match-cut); implemented per film in the starter scene code.
- **كيف / how:** declare in PLAN.md transitions table with duration (ms) and curve, then code in scene draw()
- **الدليل / proof:** `kosif-tool/templates/PLAN.md`

#### TRANS-431 · انتقال: ذوبان · Transition key: dissolve · 📄 موصوف
- **ماذا / what:** Named transition in the PLAN vocabulary (dissolve); implemented per film in the starter scene code.
- **كيف / how:** declare in PLAN.md transitions table with duration (ms) and curve, then code in scene draw()
- **الدليل / proof:** `kosif-tool/templates/PLAN.md`

#### TRANS-432 · مسح قبل وبعد · Before/after split wipe · 📄 موصوف
- **ماذا / what:** Split-screen wipe from before to after with a saved-hours counter.
- **كيف / how:** clip-path wipe.
- **أرقام / params:** 600 ms wipe
- **الدليل / proof:** `kosif-tool/playbooks/ads.md:50`

#### TRANS-433 · من الرسم إلى الحقيقي · Sketch-to-real crossfade · 📄 موصوف
- **ماذا / what:** Pencil sketch of UI crossfades into real screenshot at same geometry.
- **أرقام / params:** 400 ms crossfade
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:48`

#### TRANS-434 · القطع على الضربة · Cut-on-beat rule · 📄 موصوف
- **ماذا / what:** Cut on beat or one frame before; never 2+ frames late.
- **أرقام / params:** −1 frame
- **الدليل / proof:** `kosif-tool/playbooks/music.md:25`

#### TRANS-435 · شكل واحد بلا قطع · One shape never cut · 📄 موصوف
- **ماذا / what:** Hero shape survives every transition changing role (button→card→screen) through morph and scale.
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:28`

#### TRANS-436 · كشف بقناع دائري · Boolean circle-mask reveal · 📄 موصوف
- **ماذا / what:** Circle mask grows from hero shape revealing next scene.
- **أرقام / params:** 700 ms ease-in-out
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:45`

#### TRANS-437 · سحب الشاشة واللوحة المنبثقة · Swipe / screen push and modal sheet · 📄 موصوف
- **ماذا / what:** Incoming screen travels full width from inline-end; outgoing parallax and dim.
- **أرقام / params:** 420–520 ms cubic-bezier(0.2,0.8,0.2,1); outgoing 30% + dim 60%; sheet 380 ms up / 300 ms down cubic-bezier(0.4,0,0.2,1)
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:37`

#### TRANS-438 · أقنعة الصور الديناميكية · Dynamic photo masks · 📄 موصوف
- **ماذا / what:** Feathered wipes with mask leading the photo; shape masks grow with counter-scaling content.
- **كيف / how:** clip-path or ctx.clip with feathered gradient.
- **أرقام / params:** 500–700 ms cubic-bezier(0.65,0,0.35,1); feather 1–2% width; lead 60–90 ms; circle r 0→full 450 ms, inner 1.15→1.00; cut-out pop spring 14/120 from 0.92 ~600 ms
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:38` · `kosif-tool/playbooks/photos.md:187`

#### TRANS-439 · تحويل الصورة إلى رسم · Photo-to-graphic trace · 📄 موصوف
- **ماذا / what:** Outline traces subject, photo fades, vector fill arrives.
- **كيف / how:** stroke-dashoffset.
- **أرقام / params:** trace 900 ms easeInOutCubic; photo fade 300 ms from 700 ms; fill +150 ms
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:42` · `kosif-tool/playbooks/photos.md:77-84`

#### TRANS-440 · قطع وميضي · Flash cut · 📄 موصوف
- **ماذا / what:** Brief white/black frame between scenes for chaotic tone.
- **كيف / how:** Insert 1-2 frame solid between scenes.
- **أرقام / params:** 1-2 frames
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/tones.md`

#### TRANS-441 · قطع بالتكبير · Zoom cut entrance · 📄 موصوف
- **ماذا / what:** Scene enters at scale 1.2 settling to 1.0.
- **كيف / how:** Scale tween on scene enter.
- **أرقام / params:** scale 1.2->1.0
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/tones.md`

#### TRANS-442 · تلاشي مع تحجيم · Scale crossfade · 📄 موصوف
- **ماذا / what:** Crossfade while incoming scene grows 0.95->1.0 (cinematic).
- **كيف / how:** Opacity + scale tween.
- **أرقام / params:** 0.95->1.0; 0.6-1.0s
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/tones.md`

#### TRANS-443 · تقنيات السرد بالتمرير كحركات فيديو · Scrollytelling techniques as video moves · 💡 فكرة
- **ماذا / what:** The scroll-story vocabulary maps directly onto video transitions between chart states.
- **كيف / how:** Graphic sequence -> crossfade/cut between key frames; animated transition -> interpolate chart state; pan and zoom -> camera over a large map or image; moviescroller -> scrubbed frame sequence; parallax depth -> foreground/background layers at different speeds (only when depth clarifies scale); sticky overlay -> text cards over a full-frame visual without covering the evidence.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali/references/story-patterns-and-scene-contracts.md`

#### TRANS-444 · قلب صفحة · Paper-curl page flip · 💡 فكرة
- **ماذا / what:** Page turn using a paper-curl mask with rustle.
- **كيف / how:** Animated mask/clip path curl.
- **الدليل / proof:** `style:pm-abderrahmen-g-9e8ed0`

#### TRANS-445 · قطع على 120 نبضة · Hard cuts on 120 BPM · 💡 فكرة
- **ماذا / what:** Cuts land exactly on beats, optional 2-frame hold, no flash frames.
- **كيف / how:** beat=500 ms; cut frames=round(n*0.5*fps).
- **أرقام / params:** 120 BPM
- **الدليل / proof:** `style:pm-ajith-io-ea7f2d`

#### TRANS-446 · مسح دائري للثيم · Radial theme wipe · 💡 فكرة
- **ماذا / what:** Theme reskin radiates from a centre point per beat.
- **كيف / how:** clip-path circle grow.
- **أرقام / params:** 280 ms
- **الدليل / proof:** `style:pm-deifosv-04e4d3`

#### TRANS-447 · مزج 400 مللي · Vertical 400 ms dissolve only · 💡 فكرة
- **ماذا / what:** Only cross-dissolves; device stays in central third of 720x1280.
- **أرقام / params:** 400 ms; push ≤8%; rot ≤12°
- **الدليل / proof:** `style:pm-gautam-mer1-2ae354`

#### TRANS-448 · قطع مطابق بالتكبير · Scale match-cut one-take · 💡 فكرة
- **ماذا / what:** Continuous camera; element fills frame and becomes next background.
- **كيف / how:** Scale element to cover frame then swap scene.
- **أرقام / params:** rotation ≤12°; no cuts
- **الدليل / proof:** `style:pm-itisrazak-3ad902`

#### TRANS-449 · كشف بقناع · Masked axis-alternating reveals · 💡 فكرة
- **ماذا / what:** Claims slide in on alternating axes through masks.
- **كيف / how:** overflow:hidden masks.
- **الدليل / proof:** `style:pm-jasonzhou1993-8595e0`

#### TRANS-450 · حد المزج · Dissolve cap 150 ms · 💡 فكرة
- **ماذا / what:** Hard/match cuts on beat; any dissolve ≤150 ms; accent ≤10% frame, swaps per chapter.
- **أرقام / params:** 150 ms
- **الدليل / proof:** `style:pm-jasonzhou1993-8595e0`

#### TRANS-451 · كشف قبل وبعد · Before/after wipe reveal · 💡 فكرة
- **ماذا / what:** Vertical wipe line reveals AI twin; preset swaps with scale pop.
- **كيف / how:** clip-path inset.
- **أرقام / params:** 900 ms; hold 600 ms; swap 500 ms; 3% pop
- **الدليل / proof:** `style:pm-l3d1c-0e35a3`

#### TRANS-452 · انخفاض مظلم · Dark-dip camera reset · 💡 فكرة
- **ماذا / what:** Dolly then 200 ms dark dip resets camera.
- **أرقام / params:** 1.0→1.04; 200 ms
- **الدليل / proof:** `style:pm-listudio-820c7b`

#### TRANS-453 · قطع على كل ضربة · Beat-locked hard cuts · 💡 فكرة
- **ماذا / what:** Cut on every beat in drops, every second beat elsewhere.
- **كيف / how:** Remotion: compute beat frames from BPM, place cuts on them.
- **أرقام / params:** 150 BPM = 400 ms/beat; max shot 1.2 s
- **الدليل / proof:** `style:pm-micheleharmonic-77628e`

#### TRANS-454 · انتقال بالتحول · Seed morph transitions · 💡 فكرة
- **ماذا / what:** Last element of a scene reshapes into the next scene's first.
- **كيف / how:** Shared-element morph (flubber/GSAP MorphSVG).
- **أرقام / params:** no hard cuts
- **الدليل / proof:** `style:pm-quickdesignio-dd93d0`

#### TRANS-455 · تحريك سوطي · Whip-pan 180 ms · 💡 فكرة
- **ماذا / what:** Fast whip with directional blur and arrival hold.
- **أرقام / params:** 180 ms; 8 px directional blur; 2-frame hold
- **الدليل / proof:** `style:pm-reflex-cloud-72ffe5`

#### TRANS-456 · مزج بالتحريك · Stir gradient collapse blend · 💡 فكرة
- **ماذا / what:** Stacked colour layers blend via vertical gradient collapsing to flat.
- **أرقام / params:** bottles 400 ms ease-out, tilt 300 ms; 5% push
- **الدليل / proof:** `style:pm-ror-fly-9950f1`

#### TRANS-457 · تحول الفصول · Element-reborn chapter morphs · 💡 فكرة
- **ماذا / what:** Baseline->rail, letters->bars, outline->blob.
- **أرقام / params:** master cubic-bezier(0.16,1,0.3,1) 600-800 ms; zoom 1.0-1.35x
- **الدليل / proof:** `style:pm-samuel-spitz-974923`

#### TRANS-458 · انتقال بلا قطع · Morph/mask wipe/scale-through only · 💡 فكرة
- **ماذا / what:** push 3-6%, orbit <=8°
- **الدليل / proof:** `style:pm-stephanlivera-df17a2`

#### TRANS-459 · تحول الحاوية · Container morph loop · 💡 فكرة
- **ماذا / what:** link->card->dashboard->link.
- **أرقام / params:** push 6%
- **الدليل / proof:** `style:pm-steventey-0d20e4`

#### TRANS-460 · انزلاق مع تلاشي · Slide-up crossfade · 💡 فكرة
- **ماذا / what:** 20 px up, 400 ms
- **الدليل / proof:** `style:pm-techyoutbe-945b56`

## إضافات v2 — v2 additions

_قدرات أُضيفت في الإصدار الثاني من حزم المالك (higgsfield-motion-saas وhiggsfield-motion-claude ومهارة المونتاج التحريرية وفيلم الأغنية وKOSIF SEE) ومن مهارات ECC (رخصة MIT)، مكتوبة بكلماتنا. ✅ هنا = شُغّلت في جلسة 2026-10-16 وسجلها في [external-skills.md](../external-skills.md)؛ مسارات `owner-upload:` تشير إلى أرشيفات المالك لا إلى هذا المستودع. — v2 additions from the owner's packages and ECC skills (MIT), in our own words; ✅ = run in this session, log in external-skills.md; `owner-upload:` paths point into the owner's archives, not this repo._

#### TRANS-X01 · لكل انتقال سبب يُسمّى · Every transition needs a nameable cause · 📄 موصوف / documented only
- **ماذا / what:** الانتقال الذي لا سبب له يبدو عشوائيًا؛ اربطه بنقرة أو ضغطة مفتاح أو جسم يقترب من العدسة أو لون يفيض من زر، واستبدل التلاشي بتغيير حالة. — A transition without a cause reads as random: tie it to a click, a key press, an object at the lens or a colour flooding from a button, and replace fades with state changes.
- **متى أستخدمها / when:** تخطيط أي فيلم إطلاق أو ريل سريع — planning any launch film or fast reel.
- **كيف / how:** Hard cuts with the speed peak on the cut feel energetic; object transitions without a cut feel premium. Cut on the music grid (0.5 s multiples at 120 BPM) and shorten shots toward the climax (e.g. 0.85 s then 0.65 s). State changes instead of opacity: tile flip 0.42 s, push-swap, a hard font swap per beat with a 6 % pulse, clip-path wipe, panels sliding out from under. Nothing important appears or disappears by opacity alone: it is carried, grown, pushed, wiped or morphed. **أرقام / params:** cuts on 0.5 s grid @120 BPM; tile flip 0.42 s; font swap pulse 6 %.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md` · `owner-upload:motion-saas_skill/higgsfield-motion-saas/SKILL.md`

#### TRANS-X02 · زوم الإبرة على جسم مستمر · Needle zoom on a persistent object · 📄 موصوف / documented only
- **ماذا / what:** جسم واحد يبقى بينما تُقطع الخلفيات تحته ثلاث مرات في الثانية؛ الإبرة تمر عبر القطع دون أن تُرى. — One object persists while the backgrounds hard-cut beneath it three times a second; the needle carries it through the cut unseen.
- **متى أستخدمها / when:** شعار أو منتج يبقى في المركز عبر عدة لقطات — a logo or product staying centre-frame across several shots.
- **كيف / how:** needle(t, cut, 1, 1.12): keys at cut − 0.2 s and cut + 0.2 s − 1 frame, cubic-bezier(.95,0,.05,1); backgrounds hard-cut about 3×/s and never scale. Move the pivot first (one film moved the pivot to the centre of the letter O over 1.92–2.22 s before an x⁵ zoom at 2.05–2.5 s). Parallax: layers behind zoom at scale^0.6, layers in front at scale^1.35. Needles beyond ×9 need 16–24 motion-blur sub-frames. **أرقام / params:** ×1 → 1.12 over ±0.2 s; parallax s^0.6 / s^1.35; ×9+ → 16–24 sub-frames.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`

#### TRANS-X03 · استمرار الطيران عبر الأشياء · Fly-through continuation rule · 📄 موصوف / documented only
- **ماذا / what:** إذا طارت الكاميرا داخل شيء فاللقطة التالية تبدأ أصغر وتتباطأ نحو الداخل؛ لا تبدأ كبيرة ثم تنكمش. — If the camera flies into something, the next shot starts smaller and decelerates inward; never start it large and shrink.
- **متى أستخدمها / when:** انتقال «داخل الشاشة» أو داخل حرف أو زر — a dive into a screen, a letter or a button.
- **كيف / how:** Example that shipped: A ×1.04 → ×12 with an x⁵ curve over 0.45 s; B ×0.26 → ×1 with out() over 0.9 s plus 4 % drift. A rejected version started B at ×5.2 and shrank. Exception: when the cut frame is a solid colour (A ×1 → ×12 expoIn 0.48 s until colour fills the frame) B may start at ×5.2 → ×1. Lockup dive: ×1 → ×3.4 in(2) 0.35 s, fade only in the last 0.17 s, thin chrome fades first; incoming letters ×1.9 → ×1 out(3) with 15–20 ms stagger. Size match: a dive with into-bezier (.5,0,.85,.625) 0.58 s where the tile width at the cut equals the next prompt-bar width. Check the cut with QA-X04. **أرقام / params:** A ×1.04→×12 x⁵ 0.45 s · B ×0.26→×1 0.9 s + 4 % drift.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`

#### TRANS-X04 · حمل الجسم بإحداثيات الشاشة · Object carry contract in screen pixels · 📄 موصوف / documented only
- **ماذا / what:** لنقل عنصر من مشهد إلى آخر يرسم المشهد القادم نسخة مطابقة في المستطيل نفسه على الشاشة ويخفي الأصل تحتها، فلا يرى المشاهد أي قفزة. — To carry an element between scenes, the incoming scene draws an identical copy at the same on-screen rect and hides the original under it, so nothing jumps.
- **متى أستخدمها / when:** بطاقة أو صورة أو زر ينتقل بين مشهدين بكاميرتين مختلفتين — a card, image or button travelling between scenes with different cameras.
- **كيف / how:** Agree on screen pixels: screen = 960 + s·(local − 960) with a neutral camera; the outgoing scene reports the element's screen rect, the incoming one draws its copy there. Lift ×1.05–1.12 with a growing shadow over 0.1 s, travel on smooth(), set down. Grow-from-a-point variant: results start at the Generate button centre at ×0.06, fly on arcs, bank −6…+5° → 0, opacity front-loaded over 0.06 s, centre item first, sides +0.06 / +0.12 s. **أرقام / params:** lift ×1.05–1.12 + shadow 0.1 s; grow from ×0.06; side stagger 0.06/0.12 s.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`

#### TRANS-X05 · اللطخة والسوط بطبقات وزوج التأرجح · Smear, layered-parallax whip and swing pair · 📄 موصوف / documented only
- **ماذا / what:** سوط تتحرك فيه كل طبقة بعامل سفر مختلف فيبدو كتصوير حقيقي، ولطخة تبقى معتمة وهي تعبر حافة الإطار. — A whip where every layer travels by its own factor so it reads as a real camera, and a smear that stays opaque while crossing the frame edge.
- **متى أستخدمها / when:** انتقال سريع بين بطاقات أو شاشات أو مشاهد واجهة — a fast move between cards, screens or UI scenes.
- **كيف / how:** Smear ≈ 1150 px with in(2) (≈ 9000 px/s at the end), opaque across the edge, fade only in the last 0.12 s. Whip: wind-up +12 px over 0.14 s, then in(3) to −1500 px in 0.3–0.55 s; travel factors dots 0.5, glow 0.7, type 1.0–1.05, UI 1.1, cursors 1.2 (lead 20 ms); x-blur ≤ 10–18 px. Swing pair: out expoIn 0.36 s / 300 px with 20–24° tilt, in expoOut 0.7 s / 600 px. Mirrored whip: −700 px in(2) 0.45 s / +700 px out(2) 0.45 s (equal speed, EASE-X05). Known failure: 0.14 s whips with 46 px blur and 5–6 empty frames read 'too sharp' → fixed with 620 px over 0.34 s. **أرقام / params:** whip 0.3–0.55 s, factors .5/.7/1/1.1/1.2; blur ≤ 10–18 px; swing 0.36 s ↔ 0.7 s.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`

#### TRANS-X06 · تحوّل الواجهة بالحجم لا بالمقياس · UI morph by size, not scale (button → CTA) · 📄 موصوف / documented only
- **ماذا / what:** عند تحويل زر إلى شريط أو بطاقة غيّر العرض والارتفاع الحقيقيين لا scale، ودع اللون يسبق الحجم. — When a button becomes a bar or card, change real width/height, not scale, and let colour lead size.
- **متى أستخدمها / when:** عرض منتج يتحول فيه عنصر صغير إلى شاشة أو نداء إجراء — a product demo where a small element becomes a screen or CTA.
- **كيف / how:** Morph 1 +18 % size, morph 2 −18 %; in 3D the incoming camera distance D = w·PERSP / w_screen so the copy matches on screen. Worked case: a 47×23 px button rotated 4.3° grows in log size over 0.55 s into an 800×164 pill; colour leads size; the label rolls vertically. Tile → full-frame colour match cut with in(2) 0.45 s. **أرقام / params:** ±18 % size; button→pill 0.55 s log size; tile→frame in(2) 0.45 s.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`

#### TRANS-X07 · فيضان اللون من نقطة الفعل · Colour flood from the action point · 📄 موصوف / documented only
- **ماذا / what:** خلفية جديدة تتدفق من نقطة النقر كبقعة حية متموجة الحواف لا كدائرة صلبة. — A new background floods out from the click point as a living, wobbling blob, not a hard circle.
- **متى أستخدمها / when:** تغيير خلفية مشهد بعد نقرة أو ضغطة زر — changing a scene's background after a click or button press.
- **كيف / how:** Base disc plus 4 radial blobs (r 820–1050 px) drifting on Lissajous paths ±140/±90 px, union of 3 wobbling circles, 420 px feather; radius R = smooth(p)·(distance to the farthest corner + 504 px); an iridescent fringe ring on the edge. **أرقام / params:** 4 blobs r 820–1050; feather 420 px; R = smooth(p)·(corner + 504).
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`

#### TRANS-X08 · انسكاب الأعمدة ومنحدر التعريض · Column pour and exposure-ramp reveals · 📄 موصوف / documented only
- **ماذا / what:** طريقتان لتبديل الخلفية بلا تلاشٍ: أعمدة تنسكب من المركز، أو صورة تُضاء تدريجيًا من العتمة بدل لوحة نصية. — Two fade-free background changes: columns pouring from the centre, or a picture brought up from darkness instead of a text plate.
- **متى أستخدمها / when:** تبديل خلفيات بإيقاع أو كشف صورة منتج — rhythmic background swaps or a product reveal.
- **كيف / how:** Pour: 48 px columns, centre-first stagger 0.02 + hash·0.24 + |i − n/2|/n·0.14, each column 0.34 s, a 6-glyph head. Exposure ramp: brightness(.42) saturate(.9) → 1 over 0.75 s replaces text plates and fades. Plate cuts: hard-cut background plates 3×/s with +6 % drift. Infinite band: overscan +360 px each side (2640 px wide at 1920), no camera swing in that scene, all transitions happen inside the band. **أرقام / params:** columns 48 px × 0.34 s; ramp 0.75 s; overscan +360 px.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`

#### TRANS-X09 · تسليم القزحية إلى شعار · Iris hand-off into a wordmark · 📄 موصوف / documented only
- **ماذا / what:** دائرة تنغلق على جسم دوار ثم يصبح الجسم نفسه حرفًا في الشعار. — A circle closes onto a spinning object and the object itself becomes a letter of the wordmark.
- **متى أستخدمها / when:** نهاية فيلم تصل إلى الشعار — a film ending that lands on the logo.
- **كيف / how:** A vinyl record spins with rotation = distance / radius · 57.3° (rolls without slipping); the clip circle shrinks from 1150 px to the record radius × 0.96; the record becomes the 'o'. Finish fading any masked text before the iris starts. **أرقام / params:** rotation = d/r·57.3°; clip 1150 px → r·0.96.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`

#### TRANS-X10 · قطع الخلل بالأشرطة · Band glitch cut · 📄 موصوف / documented only
- **ماذا / what:** خلل قصير متماثل حول القطع: أشرطة أفقية تنزاح وانحراف لوني يزداد ثم يزول. — A short symmetric glitch around the cut: horizontal bands shift and chromatic aberration swells and clears.
- **متى أستخدمها / when:** 3–4 قطعات فقط في فيلم تقني أو ريل — only 3–4 cuts in a tech film or reel.
- **كيف / how:** Triangular envelope g over ±0.07 s; 34 bands; a band shifts when hash > 1 − 0.55·g, by up to ±0.035 of the width, wrapped with fract(); chromatic aberration × (1 + 5g). More than 3–4 per film becomes noise. **أرقام / params:** ±0.07 s; 34 bands; shift ≤ 0.035·W; CA ×(1+5g).
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`

#### TRANS-X11 · زوم لانهائي حول نقطة بؤرية · Focal-point infinite-zoom transition · 📄 موصوف / documented only
- **ماذا / what:** كل مشهد يحدد نقطة ضوء يخرج منها؛ نغوص فيها فيولد المشهد التالي داخل ذلك الضوء. — Each scene names the point of light it leaves through; we dive into it and the next scene is born inside that light.
- **متى أستخدمها / when:** فيلم أغنية أو قصة متصلة بلا قطع ظاهر — a song film or a continuous story without visible cuts.
- **كيف / how:** Each scene function returns its outgoing focus point. Over ±0.42 s scene A is zoomed K^pe (K = 9) about the focus point while the point drifts to centre; a 35 % ghost copy at ×1.08 adds a streak; scene B is masked destination-in by a radial gradient whose radius grows 170 → 1450 px and is drawn at zA/K so it lives inside the focal light; a warm glow follows sin(πp). Good focus targets: a lit window, a point of light, a thread, an ink dot, the evening star. **أرقام / params:** K = 9; half-width 0.42 s; mask radius 170 → 1450 px; ghost 35 % ×1.08.
- **الرخصة / license:** owner (song audio and lyrics are third-party; not included)
- **المصدر / source:** `owner-upload:film_project/film/film.js`
- **الدليل / proof:** `owner-upload:film_project/film/film.js` · `owner-upload:film_project/film/README_AR.md`

#### TRANS-X12 · انتقالات دُفع ثمنها · Transition failures already paid for · 📄 موصوف / documented only
- **ماذا / what:** قائمة أخطاء رفضها العميل فعلًا، كي لا تُكرر. — Failures a real client already rejected, so they are not repeated.
- **متى أستخدمها / when:** مراجعة أي انتقال قبل الرندر النهائي — reviewing any transition before the final render.
- **كيف / how:** Starting the shot after a fly-through larger and shrinking (×5.2 → ×1 after ×12 in) reads backwards; 0.14 s whips with 46 px blur and 5–6 empty frames read too sharp (use ~620 px over 0.34 s); chromatic aberration 0.012·r is far too much (0.0032·r is enough); 4 fixed motion-blur sub-frames look cheap (use adaptive counts, ENG-X01); animated grain on a UI film defeats the dead-air meter and doubles bitrate; opacity-only appearances read as slides; tilting flat UI into 3D to fake depth reads cheap.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md` · `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/client-taste.md`

## إضافات v3 — v3 additions (2026-10-18)

_قدرات أُثبتت في هذه الجلسة: خط أنابيب المحاكاة المدمج في `scripts/mimic/`. — Proven in this session: the in-repo mimic pipeline._

#### TRANS-X13 · تصنيف الانتقال بإعادة التركيب داخل المستودع · Transition classification by re-synthesis, shipped in-repo · ✅ مُثبت هنا / proven here
- **ماذا / what:** لا تخمّن الانتقال من شكل منحنى الفرق؛ ارسم كل نوع مرشح (54 من xfade في FFmpeg + 11 من محررات الهاتف) من الإطارين النقيين قبل وبعد عند 25 قيمة تقدّم، واختر مسارًا رتيبًا بالبرمجة الديناميكية؛ الناتج نوع ومعاملات ومدى ومنحنى تقدّم مقاس يُعاد تشغيله حرفيًا في البناء. — Instead of guessing from the difference curve, render every candidate kind (54 FFmpeg xfade + 11 phone-editor kinds) from the pure frames before and after at 25 progress values and pick a monotone dynamic-programming path; the output is kind, params, exact span and a measured progress curve replayed verbatim in the build.
- **متى أستخدمها / when:** rebuilding a reference edit exactly; identifying what CapCut/InShot/xfade transition a reference used
- **كيف / how:** `mm_analyze.analyze(ref, work)` → `spec.json: transitions[{type, params, ts, te, progress, confidence, alternatives}]`; replay with `mm_transitions.render(kind, A, B, p, **params)`. The xfade port is LGPL-2.1-or-later (notice at the top of `mm_transitions.py`); custom kinds need OpenCV or SciPy. **أرقام / params:** score = colour error + gradient error + small complexity prior; 25 progress samples; span grown/trimmed with the same model
- **الرخصة / license:** LGPL-2.1-or-later (xfade port) / owner (custom kinds)
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/scripts/mimic/mm_transitions.py` · `kosif-tool/.claude/skills/kosif-superpowers/scripts/mimic/mm_analyze.py` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/mimic-synthetic/README.md`

## إضافات مرفقات 2026-10-23 — 2026-10-23 upload additions

_من مراجعة مرفقات المالك: [owner-uploads-review-20261023.md](../owner-uploads-review-20261023.md). — From the owner-upload review._


#### TRANS-U01 · منحنى منزلق قبل/بعد: انزلاق ثم زحف ثم كشف · Before/after slider: glide → crawl → reveal · ✅ مُثبت هنا / proven here
- **ماذا / what:** p = 0.46·easeOut((t−t0)/0.8) + 0.10·smoothstep((t−t0−0.5)/2.05) + 0.44·easeInOut((t−t0−2.3)/0.95): ينزلق سريعًا إلى المنتصف، يزحف ببطء دون توقف ~1.5–2 ث للمقارنة، ثم يتسارع إلى كشف كامل. — Fast glide to the middle, a slow never-stopping crawl for comparison, then an accelerating full reveal.
- **متى أستخدمها / when:** مقارنة قبل/بعد في فيديو / a before/after comparison
- **كيف / how:** img[:, :x] = graphics[:, :x] مع x = W·p؛ فاصل أبيض 1–2 px بتوهج ومقبض زجاجي ≈52×128 وبطاقتا تسمية تتلاشيان مع تقلص جانبهما. **أرقام / params:** crawl 0.47→0.55 between 0.9 and 2.2 s (measured)
- **الرخصة / license:** Claude AI Motion Graphics (Tao Prompts) — ideas and numbers only, code not copied
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/owner-uploads-20261023/proof_uploads.py` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/owner-uploads-20261023/receipt.json` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/owner-uploads-20261023/sheet.jpg`

## من أكبر مستودعات GitHub — from the top GitHub repositories (2026-10-23)

_قدرات من أشهر مستودعات GitHub ذات الترخيص المفتوح (MIT)، مكتوبة بكلماتنا لا منسوخة، وسجل كل مستودع في [github-top-1000.md](../github-top-1000.md). 🟢 = الكود هنا في `scripts/motion_physics.py` واختباره `evals/test_motion_physics.py`. — Powers from the most-starred open-licence (MIT) GitHub repositories, restated in our own words; per-repo record in github-top-1000.md; 🟢 = code here in scripts/motion_physics.py with its test._

#### TRANS-G01 · انتقال سحري بين حالتين · Auto-animate between two states (magic move) · 📄 موصوف / documented only
- **ماذا / what:** طابق العناصر بين حالتين بمعرّف ثابت، وحرّك الموضع والحجم واللون للمتطابق، وأظهر أو أخفِ غير المتطابق، فيبدو الانتقال حركة واحدة. — Match elements between two states by a stable id, tween position, size and colour of matches, and fade the rest, so the change reads as one move.
- **متى أستخدمها / when:** شرائح أو شاشات تطبيق أو لوحات بيانات تتغير / slides, app screens or dashboards that change
- **كيف / how:** Give each persistent element a data-id in both states; measure both layouts; tween matched boxes (FLIP: first, last, invert, play) with one easing; unmatched: fade 150-250 ms; text that changes content cross-fades in place. Keep durations 0.4-0.8 s; more than ~12 moving matches turns into noise. **أرقام / params:** 0.4-0.8 s; unmatched fade 150-250 ms.
- **الرخصة / license:** MIT
- **المصدر / source:** https://github.com/hakimel/reveal.js (MIT; auto-animate) — restated in our own words
