# الجودة والتحقق — QA & verification

> فصل مُجمَّع آليًا من 381 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **372 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 372 powers deduplicated by name from 381 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 67 · 🟢 جاهز 58 · 📦 بأمر تثبيت 88 · 🔑 مفتاح/خدمة 14 · 👁 شوهد في فيديو 3 · 📄 موصوف 137 · 💡 فكرة 5

#### QA-01 · بوابة التسليم · Delivery gate (inspect) · ✅ مُثبت هنا
- **ماذا / what:** Last check before delivery: H.264/yuv420p, black and frozen stretches, integrated LUFS and true peak, sampled exposure.
- **كيف / how:** python motion.py inspect FILM.mp4 [--lufs -14] [--allow 6.6-7.3].
- **أرقام / params:** blackdetect d=0.4 pix_th 0.03 (ends allowed); freezedetect -60 dB d=1.5; LUFS -14 +-1.5; true peak > -0.9 dBTP fails
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/qa.py:1` · `kosif-one/tools/kosif-studio/motion/motion.py:500` · `kosif-studio/motion/qa.py:173` · `kosif-studio/tests/test_studio.py:739`

#### QA-02 · فحص الحلقة بلا درزة · Seamless loop check · ✅ مُثبت هنا
- **ماذا / what:** Passes when the jump from last frame to first is no bigger than an ordinary step near the ends.
- **كيف / how:** python motion.py loopcheck FILM
- **أرقام / params:** seam ≤ max(0.4, 1.5 × median of 8 end steps), 320 px luma
- **الدليل / proof:** `kosif-studio/motion/qa.py:582` · `kosif-studio/tests/test_studio.py:739` · `kosif-one/tools/kosif-studio/motion/qa.py:1`

#### QA-03 · بوابة فحص التسليم · verify_video delivery gate · ✅ مُثبت هنا
- **ماذا / what:** ffprobe/ffmpeg checks: H.264, yuv420p, even dims, aspect, fps (±0.05), duration (±1 frame), frame count (±1), audio present, AAC, ≥44.1 kHz, EBU R128 integrated loudness vs target ±1.5 LU, true peak ≤ -1 dBFS, delivered audio = master ±50 ms; JSON report.
- **كيف / how:** python3 tools/verify_video.py film.mp4 --aspect 9:16 --fps 30 --duration 15 [--audio voice.mp3] [--lufs -14] [--no-audio] [--json r.json]
- **أرقام / params:** aspects 9:16,16:9,1:1,4:5,4:3,21:9; exit 1 on fail, 2 if ffmpeg missing
- **الدليل / proof:** `kosif-tool/tools/verify_video.py` · `kosif-tool/playbooks/audio-sync.md:86` · `kosif-tool/tests/test_tools_extra.py:44`

#### QA-04 · فحص التسليم من الملف نفسه · Delivery QA from the decoded file · ✅ مُثبت هنا
- **ماذا / what:** Verify the finished file itself: full decode errors, codec/pixel format, even dimensions, BT.709 tags, faststart, black/frozen/silent stretches, loudness and true peak, size cap.
- **كيف / how:** ffprobe streams; ffmpeg -v error -i f -f null -; blackdetect, freezedetect, silencedetect; ebur128/loudnorm measure; check moov before mdat. Targets: H.264 High yuv420p, BT.709, -14 LUFS, true peak < -1 dBTP (-1.5 used), faststart.
- **أرقام / params:** -14 LUFS; < -1 dBTP; yuv420p
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/references/DELIVERY.md` · `kosif-atlas/skills/1511-homie/3903-video/scripts/qa.mjs`

#### QA-05 · سياسة الإطارات الصادقة · Honest-frame capture policy · ✅ مُثبت هنا
- **ماذا / what:** Real captures keep only frames the page actually painted, laid onto a constant fps by holding the newest frame; never interpolate; report held frames, measured page fps and GPU renderer; warn under 20 fps or on software rendering.
- **كيف / how:** CDP screencast frames with presentation timestamps -> constant-fps sequence; or switch to deterministic virtual-time rendering (kosif-tool render_html.cjs (Playwright Chromium at /opt/pw-browsers + ffmpeg, both present)) for designed compositions.
- **أرقام / params:** warn pageFps < 20; wait ~3s after load for fonts/shaders; one 1080p game measured 8 fps vs 39 at 720p (--scale 0.67)
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/references/RECORD.md` · `kosif-atlas/skills/1511-homie/3903-video/references/DELIVERY.md`

#### QA-06 · كشف تغير المشهد · Scene-change detection · ✅ مُثبت هنا
- **ماذا / what:** Locate cuts in footage (for b-roll logging, thumbnails, or to check that cuts land on the beat grid).
- **كيف / how:** ffmpeg -i in -vf "select='gt(scene,0.3)',showinfo" -vsync vfr frames_%04d.png (pts_time in showinfo log) ; or the scdet filter (present locally). PySceneDetect is an install alternative.
- **أرقام / params:** scene threshold 0.3
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/assembly-and-review.md` · `kosif-atlas/skills/2451-knowledge/9503-video-digest/context/watch-pipeline.md`

#### QA-07 · تدقيق القص على الإيقاع · Cut-to-beat audit · ✅ مُثبت هنا
- **ماذا / what:** After assembly, compare detected scene changes to the intended bar/beat boundaries and render a contact sheet one frame a few frames after every half-bar labelled with bar and shot id.
- **كيف / how:** select='gt(scene,0.3)' timestamps vs planned boundaries; tile contact sheet; off-grid cut = either intended in-shot camera jump or wrong in-frame
- **أرقام / params:** sample 6 frames after each half-bar
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/assembly-and-review.md`

#### QA-08 · إصلاح انزياح التوقيت عند الدمج · Concat drift fix: encode once · ✅ مُثبت هنا
- **ماذا / what:** Joining mp3 pieces with -c copy keeps encoder padding (~50ms/join), so captions drift; decode and encode once.
- **كيف / how:** ffmpeg -f concat -i list.txt -c:a libmp3lame -write_xing 0 joined.mp3 (or join WAV/FLAC); then compare sum of durations vs joined.
- **أرقام / params:** 9.1s drift over 181 joins -> 0.06s
- **الدليل / proof:** `kosif-atlas/skills/3323-joined-audio-transcript-drift/13837-joined-audio-transcript-drift`

#### QA-09 · عتبات التباين وتدقيق اللوحة · Contrast thresholds and palette audit · ✅ مُثبت هنا
- **ماذا / what:** Measured contrast rules for text and graphic marks plus a grayscale distinguishability screen.
- **كيف / how:** WCAG relative luminance contrast: normal text >= 4.5:1, large text >= 3:1, meaningful graphics/state >= 3:1, enhanced text 7:1. Screen palettes by CIE L* differences between adjacent colors (heuristic delta 10). Easy to reimplement with stdlib Python (sRGB linearization) in our QA step.
- **أرقام / params:** 4.5 / 3 / 3 / 7; grayscale delta L* >= 10
- **الدليل / proof:** `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/scripts/palette_audit.py` · `kosif-atlas/skills/2690-build-web-data-visualization/10318-accessibility-and-inclusive-visualizatio/references/color-contrast-and-redundant-encoding.md` · `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/SKILL.md`

#### QA-10 · عقد تباين الألوان والمسافة الإدراكية · Palette contrast + perceptual-distance contract · ✅ مُثبت هنا
- **ماذا / what:** A node:test file parses hex tokens straight from the CSS and asserts WCAG 2.x contrast (4.5:1 for 10 text pairs, 3:1 for status colours on card and soft tints) plus CIE76 deltaE >= 25 between every pair of semantic hues, in both themes.
- **كيف / how:** Port the luminance/contrast/Lab functions to any palette file; fail the render if a caption colour pair drops below threshold. Run: node --test tests/palette.test.mjs.
- **أرقام / params:** Measured here: light fg/bg 15.47, primary-fg/primary 7.96, muted 5.31, teal/card 4.78, amber/card 4.45, coral/card 5.20; dark fg/bg 16.88, primary/card 5.54, teal/card 8.32, amber/card 9.51, coral/card 6.96; deltaE threshold 25
- **الدليل / proof:** `kosif-audit-pro/tests/palette.test.mjs`

#### QA-11 · عقد الحركة المخفضة · Reduced-motion contract · ✅ مُثبت هنا
- **ماذا / what:** Under prefers-reduced-motion all durations collapse to 0.01ms with one iteration and smooth scroll off; every decorated element is forced to its final visible state, but the progress bar transform is kept so data still reads.
- **كيف / how:** @media (prefers-reduced-motion: reduce) block listing animated classes with animation:none, opacity 1, transform none; test checks it does not blanket .view-stage *.
- **أرقام / params:** animation-duration 0.01ms; transition-duration 0.01ms; iteration 1
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:3177` · `kosif-audit-pro/tests/motion-contract.test.mjs`

#### QA-12 · اختبار عقد الحركة · Motion contract test · ✅ مُثبت هنا
- **ماذا / what:** Regex-based node:test checks over CSS/TSX: duration tokens exact, curves present, no transition-all, keyed view stage + focus, reduced-motion block, safe-area/dvh rules.
- **كيف / how:** node --test tests/motion-contract.test.mjs (reads files only; no build).
- **أرقام / params:** 5 tests; ran here with palette+responsive: 14/14 pass
- **الدليل / proof:** `kosif-audit-pro/tests/motion-contract.test.mjs`

#### QA-13 · اختبار عقد التجاوب · Responsive layout contract test · ✅ مُثبت هنا
- **ماذا / what:** Slices CSS by media query and asserts phone/tablet behaviours (bottom nav at 768px, 16px/12px padding, safe-area offsets, 100dvh).
- **كيف / how:** node --test tests/responsive.test.mjs.
- **أرقام / params:** breakpoints 768/480; offsets 72/68/80px + safe-area
- **الدليل / proof:** `kosif-audit-pro/tests/responsive.test.mjs`

#### QA-14 · فحص الأصول والصياغة الثابت · Static asset and syntax check · ✅ مُثبت هنا
- **ماذا / what:** Walks the repo, syntax-checks every JS module with node --check, validates local asset references, view IDs and the PWA cache list.
- **كيف / how:** cd kosif-audit-studio && node scripts/check-static.mjs.
- **أرقام / params:** ran here: 18 legacy views, 35 V5 IDs, 87 assets/imports, 140 JS modules, 23 stylesheets
- **الدليل / proof:** `kosif-audit-studio/scripts/check-static.mjs`

#### QA-15 · اختبار تثبيت الثيم · Theme lock test (dashboard/editorial) · ✅ مُثبت هنا
- **ماذا / what:** Asserts required hex tokens, Tajawal, hero gradient and shadow exist; checks cascade order, theme-color consistency and font weights linked.
- **كيف / how:** node --test tests/dashboard-theme.test.js.
- **أرقام / params:** 13 hex tokens locked
- **الدليل / proof:** `kosif-audit-studio/tests/dashboard-theme.test.js`

#### QA-16 · محاكاة حركة المناطق من المرجع · Regional motion clone (4x4 block motion) · ✅ مُثبت هنا
- **ماذا / what:** Measures where and how parts of a reference move over time (16 regions), compensating for camera motion, then rebuilds animated inserts on the user's project and scores motion similarity.
- **كيف / how:** BasmaMotionCore.extract(frames{t,gray 96x96},{duration,cuts}): per region 15x15 patch block matching +-6 px (step 2), texture >= 6, confidence threshold 0.12; global camera = median of >= 7 strong cells; activity = speed/7 + change term; 10 time bins; shots split at cuts (min 0.13 s), top 5 regions; planShots keeps chronological order (max 36, sampled evenly); compare = 0.4 profile + 0.25 energy + 0.35 active regions, capped at 20 for static vs animated; runtime samples 2/s (12-72 frames, <= 180…
- **أرقام / params:** grid 4x4; frame 96 px; block radius 6 px
- **الدليل / proof:** `app/public/motion-clone-core.js` · `app/public/motion-clone-runtime.js` · `app/tests/motion-clone.test.mjs`

#### QA-17 · اختبارات CI · CI and regression tests · ✅ مُثبت هنا
- **ماذا / what:** GitHub Actions run the source smoke check, Python media-helper tests, motion-clone tests, TypeScript check and a Vite build.
- **كيف / how:** ci.yml (Node 22): npm install, npm run check:project, python3 -m unittest discover -s tests, node --test tests/motion-clone.test.mjs, tsc --noEmit, vite build, upload dist (7 days). Ran here: motion-clone 7/7 pass, media helper 3/3 pass, check-project 8 FAIL (stale after JS split).
- **الدليل / proof:** `app/.github/workflows/ci.yml` · `app/tests/motion-clone.test.mjs` · `app/tests/test_media_cli.py`

#### QA-18 · سياسة تقليل الحركة · Reduced-motion policy · ✅ مُثبت هنا
- **ماذا / what:** Every animation is decoration: prefers-reduced-motion zeroes all duration tokens, disables keyframes, renders the 3D world as one still frame and skips the cinematic intro.
- **كيف / how:** @media (prefers-reduced-motion:reduce){--sk-t:0ms;--sk-motion-enter:0ms;--sk-motion-stagger:0ms}; matchMedia checks in motion.js, crystal-world.js, earth-intro js.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/tokens.css:96` · `kosif-earth-ci-fork/ui/art/crystal-world.js:13` · `kosif-earth-ci-fork/ui/art/brand/earth-intro-20261009.js`

#### QA-19 · اختبارات توحيد الهوية · Single-identity enforcement tests · ✅ مُثبت هنا
- **ماذا / what:** Tests lock the brand: no cobalt hex in marks/icons/manifest/door styles, theme-color #1d1814, crystal world colours only via uniforms, door tokens equal ledger tokens, cobalt kept as a selectable look.
- **كيف / how:** node --test tools/identity_unity.test.mjs tools/door_tokens.test.mjs (5/5 and 2/2 pass here).
- **أرقام / params:** COBALT regex #2340c4|#0b1030|#19c3d9|#2a46d6|#070a1e|#9beef7|#b6f3fa
- **الدليل / proof:** `kosif-earth-ci-fork/tools/identity_unity.test.mjs` · `kosif-earth-ci-fork/tools/door_tokens.test.mjs`

#### QA-20 · مقياس انحراف الهوية · Identity drift ratchet (identity_audit) · ✅ مُثبت هنا
- **ماذا / what:** Measures how far stylesheets/modules drift from the identity and fails CI if any metric worsens.
- **كيف / how:** node tools/identity_audit.mjs [--json|--write-baseline]; counts hard-coded colours, off-4px-grid spacing, literal radii, colours inside JS, !important, heavy weights, weight variants, focus variants; lists families.
- **أرقام / params:** baseline 2026-10-09: colours 438, offGrid 1104, radiusLiterals 415, inlineColours 64, important 99, heavyWeights 55, weightVariants 7, focusVariants 16
- **الدليل / proof:** `kosif-earth-ci-fork/tools/identity_audit.mjs` · `kosif-earth-ci-fork/tools/fixtures/identity-baseline.json`

#### QA-21 · اختبارات وجود أصول الهوية وخفتها · Brand art presence & weight tests · ✅ مُثبت هنا
- **ماذا / what:** Every sector has its picture, every named brand file exists and stays light, door film gating is correct, and the EARTH intro has adaptive 4K + mobile fallback.
- **كيف / how:** node --test tools/brand_art.test.mjs (5/5 pass here).
- **الدليل / proof:** `kosif-earth-ci-fork/tools/brand_art.test.mjs`

#### QA-22 · اختبار محرك ثلاثي الأبعاد دون متصفح · 3D engine unit test without a browser · ✅ مُثبت هنا
- **ماذا / what:** Loads the WebGL engine in a Node vm sandbox with stubbed window to assert API shape, graceful null without WebGL, closed shard geometry with unit normals and determinism.
- **كيف / how:** node --test tools/crystal_world.test.mjs (4/4 pass here); node --test tools/motion.test.mjs (4/4 pass).
- **أرقام / params:** 72 vertices/shard asserted; |n|=1 +-1e-5
- **الدليل / proof:** `kosif-earth-ci-fork/tools/crystal_world.test.mjs` · `kosif-earth-ci-fork/tools/motion.test.mjs`

#### QA-23 · مدقق ملخص المشروع · Brief validator · ✅ مُثبت هنا
- **ماذا / what:** Normalises a brief over defaults and rejects invalid duration, aspect or empty fields before any planning.
- **كيف / how:** normalizeBrief(): merge defaultBrief, Number(duration) must be finite 3..600 s, aspect in {9:16,16:9,1:1}, title/topic/style/language non-empty strings.
- **أرقام / params:** duration 3–600 s; aspects 9:16|16:9|1:1
- **الدليل / proof:** `fastify-motion-bro/scripts/planner.mjs:5-13` · `fastify-motion-bro/tests/planner.test.mjs:2-4`

#### QA-24 · عبارة اعتماد التصدير النهائي · Typed final-render approval phrase · ✅ مُثبت هنا
- **ماذا / what:** For the Viral Editorial profile, MP4 export with --approved is refused unless all five stages are done and the user typed APPROVE FINAL RENDER, recorded as approval.final_render=true.
- **كيف / how:** npm run viral -- approve-render (readline prompt) -> approveFinalRender() -> compileStoryboard writes approval.final_render; render.py checks story.profile=='viral-editorial-3d' and errors otherwise.
- **أرقام / params:** phrase: APPROVE FINAL RENDER
- **الدليل / proof:** `fastify-motion-bro/scripts/viral-editorial.mjs:47-51` · `fastify-motion-bro/scripts/viral-cli.mjs:14-22` · `fastify-motion-bro/scripts/render.py:24-25`

#### QA-25 · حزمة الاختبارات · Unit test suite (24 tests) · ✅ مُثبت هنا
- **ماذا / what:** node --test covering planner, all seven profiles, CLI persistence/clean plate and the viral gate logic; 24/24 passed here in under 1 s.
- **كيف / how:** npm test
- **أرقام / params:** 24 tests; ~0.9 s
- **الدليل / proof:** `fastify-motion-bro/tests/planner.test.mjs` · `fastify-motion-bro/tests/production-profiles.test.mjs` · `fastify-motion-bro/tests/production-cli.test.mjs`

#### QA-26 · علم التحقق التاريخي · Historical fact-check flag · ✅ مُثبت هنا
- **ماذا / what:** History narration lines are placeholders; output carries needsFactCheck=true and requires real sources and authenticated images before publishing; single clips are revised in place.
- **كيف / how:** Artifacts include needsFactCheck; output footer warns.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/vox-history.mjs:53-55` · `fastify-motion-bro/docs/PRODUCTION-GATES.md:13`

#### QA-27 · خصائص قابلة للتعديل وملف مشاهد داخل التركيب · Editable props + reel JSON inside the composition · ✅ مُثبت هنا
- **ماذا / what:** A kosif-props JSON block holds editable copy (title, subtitle, titleAt) and a kosif-reel JSON block describes scenes, elements, boxes (percent), bindings and AI shot layers so a review page can edit the film and write back.
- **كيف / how:** <script type=application/json id=kosif-props>{title, subtitle, titleAt}</script>; <script id=kosif-reel>{ai:{locks,environment,time,lighting,fps}, scenes:[{id,name,t:[a,b],els:[{id,label,t,box:[x,y,w,h],props:{text:{type,bind}}}],ai:{subject,action,shot,angle,lens,camera_move,atmosphere,palette,sound}}]}</script>; colours editable in :root vars; kmotion review init/apply/bump.
- **أرقام / params:** boxes in % of frame; boxBind/timeBind keys; :root --lantern #ff9a3c
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/index.html:33` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/index.html:34` · `100-superskills/skills/kosif-montage-motion/tests/test_review.py:85`

#### QA-28 · كشف الانتقالات: قطع وذوبان وغطس · Transition detection: cut, dissolve, dip · ✅ مُثبت هنا
- **ماذا / what:** Boundaries in a film are found frame-exactly and typed as cut, dissolve or fade-to-black; exposure ramps inside a shot are not mistaken for cuts; shots cover the whole film.
- **كيف / how:** mimic.boundaries(frames, fps) → {boundaries:[{type, frame, start, dur}], flashes}; mimic.shots_from(boundaries, dur); planned_boundaries(timeline report).
- **أرقام / params:** cut at frame 60 exact; dissolve ±2 frames, 16-frame length; dip start ±3, length ±4
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_mimic.py:47` · `100-superskills/skills/kosif-montage-motion/tests/test_mimic.py:76`

#### QA-29 · حلّال إنشائي بتحقق يدوي وبوابات ثقة · Structural solver with hand-calc and trust gates · ✅ مُثبت هنا
- **ماذا / what:** The truss solver is checked against hand calculations (2D triangle, 3D tripod), equilibrium, mechanisms, NaN/geometry rejection, swap that cannot hide the next bottleneck, and a self-contained dashboard.
- **كيف / how:** structural_twin.analyse(model, scale) → reactions, members {axial_n, stress, utilization, failure_load_multiplier, mode}, ranked_failure_modes; report(model, id, changes, fracture_scale); tests: A.y = C.y = 6000 N, AB = BC = −12000/√2 N, AC = 6000 N.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_structural_twin.py:21` · `100-superskills/skills/kosif-montage-motion/tests/test_space_truss.py:23` · `100-superskills/skills/kosif-montage-motion/examples/illustrative-truss-report.json`

#### QA-30 · اختبارات حتمية لهندسة الفيلم · Deterministic geometry tests for a film function · ✅ مُثبت هنا
- **ماذا / what:** A film written as a pure function is unit-tested like code: every frame string is valid, contains no NaN/undefined/Infinity, has the right size, is identical on re-render, changes over time, and story beats (jump height, landing, travel, clamping) hold.
- **كيف / how:** node test.cjs: for i 0..288 sceneSVG(i/24) startsWith '<svg', no /NaN|undefined|Infinity/, width=1280; sceneSVG(3.5)==sceneSVG(3.5); sceneSVG(2)!=sceneSVG(4); pose(6).jump>80; pose(8).jump==0; pose(8).x>pose(3).x; pose(12).x==pose(13).x.
- **أرقام / params:** 289 samples; ran here: PASS
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/test.cjs:1`

#### QA-31 · اختبار المشغل بمحاكاة DOM · Mocked-DOM player test harness · ✅ مُثبت هنا
- **ماذا / what:** The standalone HTML player is executed in a Node vm with a fake document and rAF to test init, reduced motion, seek, deterministic frame, play/pause, restart, auto-stop and bounds without a browser.
- **كيف / how:** node player-test.cjs: extract <script> blocks with regex, vm.runInContext; elements map; callback(1000), callback(1042) to advance 42 ms; render(−20) clamps to 0, render(40) to 12.
- **أرقام / params:** ran here: PASS
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/player-test.cjs:1`

#### QA-32 · بوابة قابلية قراءة النص · Readability gate for on-screen text · ✅ مُثبت هنا
- **ماذا / what:** Each text overlay is checked against its on-screen time for its length; too-short items are flagged and the hook is checked.
- **كيف / how:** launch.readable(edit.json) → {items, too_short:[{what:'overlay 1'}], hook:{ok}}; e.g. a 14-word line shown 1.1 s fails, a 2-word line 1.7 s passes.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_launch.py:54`

#### QA-33 · قواعد نص المشاركة · Share-copy rules · ✅ مُثبت هنا
- **ماذا / what:** Launch/share text is linted: banned clichés (e.g. 'Excited to share…'), too many short sentences, empty copy are flagged; a short concrete Arabic line passes.
- **كيف / how:** launch.check_copy(text) → [] or issues containing 'banned' / 'sentences'.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_launch.py:48`

#### QA-34 · توليد القوالب مع فحص · Template generation + lint gate · ✅ مُثبت هنا
- **ماذا / what:** Every motion template generates a project whose HTML has no leftover {{placeholders}}, escapes HTML in titles, registers window.__timelines, ships motion-kit and template.json, and passes the project lint with zero errors.
- **كيف / how:** mtemplates.create(name, template, {title, items 'أ|ب|ج', quote, from}, None, 30, '540x960'); qa.lint(dir); templates: bullet-list, countdown, end-card, logo-reveal, lower-third, quote-card, stat-counter, title-card.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:154`

#### QA-35 · حلقة مراجعة مشهد بمشهد مع الكتابة للمصدر · Scene-by-scene review loop with write-back · ✅ مُثبت هنا
- **ماذا / what:** A film or timeline becomes a reel the user reviews in a browser page; edits to copy, times, boxes and colours are applied back into the source, motion requests and pinned notes are left for Claude, approved scenes are locked, versions bump.
- **كيف / how:** kmotion review init SPEC|PROJECT --video FILM --name N → reel.json; review apply N --feedback fb.json → {applied, left_for_claude:{edits, notes}, approved_do_not_touch}; review bump N; web: /review/N/, /review/N/feedback (same-origin only), MCP tool kosif_review_apply.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_review.py:59` · `100-superskills/skills/kosif-montage-motion/tests/test_web.py:45`

#### QA-36 · عميل التصيير البعيد وبوابات الأمان · Remote render client and bridge safety gates · ✅ مُثبت هنا
- **ماذا / what:** Remote 2D rendering and the public Workbench bridge only run with explicit consent: pinned origin, no redirects, bounded request/response sizes, refusing tokens in payloads, never echoing credentials, no overwrite races, project folders created without execution.
- **كيف / how:** render_client (status/render --plan --allow-remote), site_bridge (health/templates/plan/validate/compile/project, POST needs approval); 13 + 31 offline tests.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_render_client.py:12` · `100-superskills/skills/kosif-montage-motion/tests/bridge/test_site_bridge.py:19`

#### QA-37 · مدقق الخطة · Plan validator · ✅ مُثبت هنا
- **ماذا / what:** Checks a proplan for schema, intent, fps/aspect, whole frames and gapless shot coverage (1–100 shots), with Arabic error messages and a rights/fonts/audio review warning.
- **كيف / how:** POST /api/validate {plan} or MCP motion_validate → wbcompat.validate_plan().
- **أرقام / params:** shots 1–100; each start_frame == previous end; beat/camera_move strings ≤ 150 chars
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:80`

#### QA-38 · قواعد التحقق من manifest · Manifest validation rules · ✅ مُثبت هنا
- **ماذا / what:** Strict model for a renderable manifest: only known keys, even pixel sizes, allowed fps, whole frames, gapless scenes covering the whole duration, safe ids and #rrggbb accents.
- **كيف / how:** wbcompat.validate_manifest(); used by /api/render/jobs, project kind 'manifest' and MCP kosif_render_manifest.
- **أرقام / params:** width/height even 128–1920; fps 24/25/30/50/60; duration 1–600 s; scenes 1–200; id [A-Za-z0-9_-]{1,64}; title ≤ 120, subtitle ≤ 300 chars; local limit max_bytes 2 GB (hosted demo: 1–30 s, ≤ 1280 px, 24/25/30 fps, 50 scenes)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:31` · `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:154`

#### QA-39 · حماية الواجهة المحلية من المواقع الأخرى · Cross-origin guard for the local API · ✅ مُثبت هنا
- **ماذا / what:** State-changing requests to /api/*, /review/* and /mcp are refused with 403 when a browser reports they came from another website, while curl, scripts and MCP clients without an Origin header still work; API answers are no-store and nosniff.
- **كيف / how:** _foreign_origin(scope) checks Sec-Fetch-Site (cross-site|same-site) and Origin host ∉ {127.0.0.1, localhost, [::1]}; _Headers ASGI middleware.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:1012` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:1029` · `100-superskills/skills/kosif-montage-motion/tests/test_web.py:224`

#### QA-40 · صفحة المراجعة مشهدًا بمشهد · Scene-by-scene review page (KOSIF Review / Motion OS player) · ✅ مُثبت هنا
- **ماذا / what:** After a render, the film opens in a review player where the user edits text, colours, fonts, logo, music, timing, size and position, pins notes on the frame, marks scenes approved, and sends one prompt back to Claude.
- **كيف / how:** kmotion review init PROJECT|SPEC.json|VIDEO [--video film.mp4] (or MCP kosif_review_init / POST /api/reviews) writes reel.json and serves /review/NAME/; Claude reads kosif_review_feedback and runs kosif_review_apply, then `kmotion review bump NAME --video NEW.mp4`.
- **أرقام / params:** scene status review | changes (Fix) | approved; tabs Scene, Script, Style, Media, Notes; light and dark themes; prefers-reduced-motion respected
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:1` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:694` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:697`

#### QA-41 · منظف مشروع Studio · Studio project sanitiser · ✅ مُثبت هنا
- **ماذا / what:** Every project change or opened file is normalised: version 1 only, ids de-duplicated, numbers clamped, colours #rrggbb, enums whitelisted, clips capped against media duration and the 60-second total.
- **كيف / how:** sanitizeProject(raw) in model.mjs, called inside every transaction.
- **أرقام / params:** aspect 16:9|9:16|1:1; clip type image|video|demo; fit contain|cover; preset aurora|sunset|grid; overlay text|shape, shape circle|rectangle, animation none|fade|rise|zoom
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/model.mjs:13` · `100-superskills/skills/kosif-montage-motion/tests/studio/model.test.mjs`

#### QA-42 · مدقق مواصفة المشهد الصارم · Strict SceneSpec validator (25 fields) · ✅ مُثبت هنا
- **ماذا / what:** Rejects any scene missing identity, anatomy, physics, camera, lens, lighting key/fill/rim, grade, materials, weather, VFX, composition or negatives.
- **كيف / how:** MCP kosif_scene_spec_check scene={...} (wraps kosif-secure-executor/scripts/scene_spec.py validate_scene).
- **أرقام / params:** fields: subjects, character_identity, anatomy, action, contact_physics, world, location, architecture, camera, lens, camera_angle, depth_of_field, lighting{key,fill,rim}, color_temperature, color_grade, materials, weather, atmosphere, VFX, composition, story_focus, negative_constraints, aspect_ratio
- **الدليل / proof:** `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/tools_scripts.py:239` · `kosif-one/tools/kosif-omni/skills/kosif-secure-executor/scripts/scene_spec.py` · `kosif-one/tools/kosif-omni/mcp-server/tests/test_server.py:269`

#### QA-43 · مدقق برومبت الصور والفيديو · Image/video prompt linter · ✅ مُثبت هنا
- **ماذا / what:** Scores a prompt against the KOSIF formula, enforces required/forbidden terms and verbatim locks, flags contradictions and Arabic inside generation text.
- **كيف / how:** kosif_image_prompt_lint {prompt, mode image|video, contract{required,forbidden}, locks{}} or stdin to scripts/prompt_lint.py; exit 0 PASS / 1 REVISE / 3 BLOCK.
- **أرقام / params:** weights subject 20, lighting 14, environment 14, camera 10, style 10, lens 8, color 8, quality 8, aspect 8; video adds camera_move/duration/motion/pacing 8 each; <25 words short, >220 long; score < 60 -> REVISE; conflicts photoreal vs cartoon/anime, B&W vs vibrant, daylight vs night, high-key vs low…
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-image-studio/scripts/prompt_lint.py` · `kosif-one/tools/kosif-omni/mcp-server/tests/test_server.py:226`

#### QA-44 · عقد التنفيذ البصري · Visual execution contract (build/verify/repair/jev) · ✅ مُثبت هنا
- **ماذا / what:** Freezes what must stay true in a generated image, checks observed evidence against it, and allows exactly one targeted repair.
- **كيف / how:** kosif_visual_contract command=build|verify|repair|jev payload={...}; locks order subject, action, composition, camera, lighting, weather, environment, style; attention budget max 3; evidence must come from host-vision / vision-tool / human-review / state-observation bound to the same request_id.
- **أرقام / params:** thresholds anatomy 0.70, composition 0.65, lighting 0.65, physics 0.65, attention 0.70; one repair max
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-image-studio/scripts/visual_contract.py:20` · `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/visual-execution-contract.md` · `kosif-one/tools/kosif-omni/skills/kosif-think-pro/scripts/visual_reliability_self_test.py`

#### QA-45 · تدقيق صفحات الويب · Static web/HTML audit · ✅ مُثبت هنا
- **ماذا / what:** Deterministic audit of an HTML page or folder: document, accessibility incl. contrast in both themes, responsive, performance, token use, security.
- **كيف / how:** python3 scripts/web_audit.py PAGE|DIR or MCP kosif_web_audit path=|html=; exit 0 PASS / 1 REVISE / 3 BLOCK; then render-check with Playwright at 360x800 and 1280x800 light/dark.
- **أرقام / params:** BLOCK on zoom disabled, missing viewport/lang, text contrast fail, secret
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-web-design/scripts/web_audit.py` · `kosif-one/tools/kosif-omni/mcp-server/tests/test_server.py:312`

#### QA-46 · بوابة فحص الجودة وإيصال الإنتاج · ffprobe delivery gate + receipt · ✅ مُثبت هنا
- **ماذا / what:** Refuses to call a render finished unless duration, size, codecs and both streams are right; then writes a receipt with sha256, scenes, sources, licence status and QA stills.
- **كيف / how:** ffprobe -show_entries format=duration,size:stream=codec_type,codec_name,width,height -of json; assert |dur-48|<0.55 (or 47.8..48.3), width/height exact, video+audio present; render to a .tmp.mp4 and os.replace only after QA; grab QA frames at 4/16/28/43 s; write production_receipt.json and an auto-generated Arabic reuse guide .md.
- **أرقام / params:** tolerance ±0.55 s (v1) or 47.8-48.3 s (v2); 4 QA stills
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:86-93` · `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:94-133` · `kosif-one/projects/KOSIF_Motion_Ghorba/tools/render_ghorba_preview.py:163-189`

#### QA-47 · اختبارات A/B · A/B test plan and read · ✅ مُثبت هنا
- **ماذا / what:** Sample size per variant and a results reader with rates, lift, 95% CI, z and p for hooks, covers or titles.
- **كيف / how:** python social.py abplan ab.json --out DIR; python social.py abread ab_results.csv --need N.
- **أرقام / params:** 95% CI
- **الدليل / proof:** `kosif-one/tools/kosif-social/SKILL.md` · `kosif-one/tools/kosif-social/examples/ab.json`

#### QA-48 · أفضل وقت نشر · Best time from own analytics · ✅ مُثبت هنا
- **ماذا / what:** Median per weekday x 3-hour block (>=2 posts per cell) vs overall median; <8 posts keeps defaults.
- **كيف / how:** python3 social.py besttime export.csv --metric views --block 3
- **الدليل / proof:** `100-superskills/skills/kosif-social/scripts/social.py:583`

#### QA-49 · تجارب A/B · A/B plan and read · ✅ مُثبت هنا
- **ماذا / what:** Sample size per variant (alpha 0.05, power 0.8) and results with lift, 95% CI, z and p.
- **كيف / how:** social.py abplan ab.json; social.py abread results.csv --need N
- **أرقام / params:** alpha .05 power .8
- **الدليل / proof:** `100-superskills/skills/kosif-social/scripts/social.py:633`

#### QA-50 · فحص الإطارات الآلي · Frame QA: black/white/freeze/cut scan · ✅ مُثبت هنا
- **ماذا / what:** Downsamples frames to 320px grey, flags near-black (mean<6), near-white (>249), freezes (diff<0.05 for >=1.5 s) and excess hard cuts (diff>60).
- **كيف / how:** python qa.py --frames frames --fps 30 --out qa.json --freeze 1.5 -> PASS/REVISE
- **أرقام / params:** thresholds 6/249/0.05/60
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/scripts/qa.py`

#### QA-51 · بوابة الستوري بورد · Storyboard gate · ✅ مُثبت هنا
- **ماذا / what:** Validates scenes.json/storyboard.json: scene count, verb descriptions, carrier object every scene, <=8 words/frame, hero coverage, object test, camera budget; returns PASS/REVISE.
- **كيف / how:** python storyboard_gate.py --scenes s.json --storyboard b.json --anchor NAME
- **أرقام / params:** <=8 words
- **الدليل / proof:** `100-superskills/skills/motion-director-pro/scripts/storyboard_gate.py` · `100-superskills/skills/motion-director-pro/templates/scenes.example.json`

#### QA-52 · دليل رندر demo2d · demo2d proof render · ✅ مُثبت هنا
- **ماذا / what:** A rendered 6 s 1080x1920 30 fps demo with mp4, GIF, contact sheet and PASS qa.json.
- **كيف / how:** run.md commands.
- **أرقام / params:** 180 frames, mean_motion 0.21
- **الدليل / proof:** `100-superskills/examples/demo2d/qa.json` · `100-superskills/examples/demo2d/run.md`

#### QA-53 · فحص البرومبت · Image prompt lint · ✅ مُثبت هنا
- **ماذا / what:** Flags missing required fields, >2 light sources, two lenses, living-artist names (BLOCK), real-person prompts (BLOCK), unsupported aspect, no negatives, Arabic text warning.
- **كيف / how:** Run forge; exit 3=BLOCK, 1=REVISE, 0=PASS
- **أرقام / params:** living-artist regex: greg rutkowski, artgerm, loish, wlop, beeple, james jean, ross tran, ilya kuvshinov, sakimichan
- **الدليل / proof:** `100-superskills/skills/image-prompt-forge/scripts/image_prompt_forge.py:30` · `100-superskills/skills/image-prompt-forge/scripts/image_prompt_forge.py:38`

#### QA-54 · فحص الفيديو المولد · Post-generation video QA · ✅ مُثبت هنا
- **ماذا / what:** Check identity drift, hands/faces, physics, stray text, wardrobe/light continuity; regenerate only failed shot.
- **كيف / how:** Checklist appended by forge
- **الدليل / proof:** `100-superskills/skills/video-prompt-director/SKILL.md:25`

#### QA-55 · فحص أمان الكود قبل التشغيل · Code safety gate before running pasted code · ✅ مُثبت هنا
- **ماذا / what:** Scans pasted Python for commands beyond drawing (file deletion, process launch, network, ctypes/winreg, eval/exec, file writes, pip/sys.exit) and asks the user; runs in a scratch folder with a time limit. SVG is treated as data.
- **كيف / how:** risky(code) matches the RISKY regex list; _launch_code shows an Arabic yes/no warning; produce_code kills the process after CODE_TIMEOUT; runner chdirs to a temp dir.
- **أرقام / params:** CODE_TIMEOUT = 120 s; 8 risk categories
- **الدليل / proof:** `kosif-studio/studio.py:49` · `kosif-studio/studio.py:167` · `kosif-studio/studio.py:1139`

#### QA-56 · تمييز الصورة الفوتوغرافية عن الرسم المسطح · Photo vs flat-art classifier · ✅ مُثبت هنا
- **ماذا / what:** Decides whether an image is a photo/painting or a logo/flat art by counting distinct colours at a fixed size.
- **كيف / how:** vectorize.looks_like_photo(rgba): resize to 200x200, quantise /8, count unique colours.
- **أرقام / params:** > 1200 distinct bins = photo
- **الدليل / proof:** `kosif-studio/vectorize.py:158` · `kosif-studio/tests/test_studio.py:149`

#### QA-57 · فحص الحتمية والذوق · Composition lint (determinism + contract + taste) · ✅ مُثبت هنا
- **ماذا / what:** Static scan of index.html, src/*.js and project scripts for render-breaking and generated-looking patterns.
- **كيف / how:** python motion.py lint PROJECT (exit 1 on errors)
- **أرقام / params:** errors: Math.random, Date.now/performance.now/new Date(), setTimeout/setInterval, dir=rtl on <html>, <audio> without id, no data-composition-id, no timeline/seek; warns: will-change on filter/transform, CSS transition, repeat:-1, backdrop-filter, large/coloured text-shadow, linear ease on moves, >3 …
- **الدليل / proof:** `kosif-studio/motion/qa.py:58` · `kosif-studio/motion/qa.py:75` · `kosif-studio/tests/test_studio.py:684`

#### QA-58 · لوحات النقد · Critique contact sheets · ✅ مُثبت هنا
- **ماذا / what:** Builds a 2 fps contact sheet, a 1 fps phone-width sheet, a 12-frame strip around a moment, the first frame and a review.md template.
- **كيف / how:** python motion.py sheet FILM.mp4 [--at 4.2] [--out DIR]
- **أرقام / params:** contact fps=2 320 px 6 cols padding 4 #111111; phone fps=1 360 px 5 cols; strip 12x1 from at-0.1 s
- **الدليل / proof:** `kosif-studio/motion/qa.py:106` · `kosif-studio/tests/test_studio.py:699`

#### QA-59 · قاعدة الصدق في التوقيت · Truthful-timing rule · ✅ مُثبت هنا
- **ماذا / what:** Timing that was not measured is labelled: verse marks 'estimated', audio2motion writes timing_quality 'estimated_from_text_length_NOT_ASR' and refuses to invent a transcript; transcribe.load_transcript only accepts timed words.
- **كيف / how:** Check verse.json 'timing' and the plan JSON timing_quality before claiming sync.
- **الدليل / proof:** `kosif-studio/motion/verse.py:475` · `kosif-studio/motion/audio2motion.py:262` · `kosif-studio/motion/transcribe.py:89`

#### QA-60 · مجموعة اختبارات الموشن · Motion test suite · ✅ مُثبت هنا
- **ماذا / what:** Unit tests for scaffold, ambience, bundling, canvas route, score+beats, lint, sheet+speed, channels tape-stop, loopcheck+inspect, montage, long exposure, book lessons, kmotion, decaption, transcript writers, direct plan, verse; plus Voice2Motion, site bridge, open footage and voice plan tests.
- **كيف / how:** python3 tests/test_audio2motion.py (7 pass here); test_studio.py needs cv2/playwright for some cases
- **أرقام / params:** test_studio Motion class 22 tests; test_audio2motion 7(+1 unreachable); bridge 21; open_footage 2; voice_montage 3
- **الدليل / proof:** `kosif-studio/tests/test_studio.py:546` · `kosif-studio/tests/test_audio2motion.py:1` · `kosif-studio/tests/bridge/test_site_bridge.py:1`

#### QA-61 · أفلام مرجعية مقاسة · Shipped-film benchmark (measured) · ✅ مُثبت هنا
- **ماذا / what:** Rendered films in out/ that serve as proof and regression references; measured here with qa.inspect and motion energy.
- **كيف / how:** qa.inspect + motion energy at 15 fps 320 px
- **أرقام / params:** blue_hour 8 s 1080p30 −15.1 LUFS TP −0.9; koi_pond 10 s −13.9/−1.6 still 0 %; showreel 15 s 1080p60 −13.7/−2.8 still 54 %; montage_demo 10.07 s 1080x1920 −14.0/−1.4; sound_ground 10 s −13.2/−2.4 mean energy 11.96; water_cycle 17 s −19.8 LUFS (FAIL); water_cycle_3d 17 s TP −0.5 (FAIL); FINAL_EDIT 20.…
- **الدليل / proof:** `kosif-studio/out/blue_hour.mp4` · `kosif-studio/out/koi_pond.mp4` · `kosif-studio/out/kosif_motion_showreel.mp4`

#### QA-62 · فحص الأصالة · Originality check · ✅ مُثبت هنا
- **ماذا / what:** Checks that generated text does not copy third-party prompts.
- **كيف / how:** python3 tools/check_originality.py.
- **الدليل / proof:** `kosif-tool/tools/check_originality.py`

#### QA-63 · لوحة معاينة 8 إطارات · Contact-sheet preview (--preview) · ✅ مُثبت هنا
- **ماذا / what:** Renders 8 evenly spaced frames, labels each with time and frame index via ffmpeg drawtext, and tiles them 4x2 into one PNG for approval before the full render.
- **كيف / how:** node tools/render_html.cjs --in film.html --out out/preview.png --preview  (writes out/preview_preview.png)
- **أرقام / params:** tiles scaled to fit 480x540, tile=4x2 padding 8 margin 12 bg 0x101418, label fontsize h/36 box black@0.55
- **الدليل / proof:** `kosif-tool/tools/render_html.cjs:414` · `kosif-tool/tools/render_html.cjs:515`

#### QA-64 · سطر التحقق بعد الرندر · Post-render ffprobe VERIFY line · ✅ مُثبت هنا
- **ماذا / what:** After encoding, render_html probes the file and fails with exit code 3 if fps, frame count (±1), duration (±1 frame+2 ms), size or audio presence disagree with the request.
- **كيف / how:** automatic; prints 'VERIFY OK|FAIL duration=… fps=… frames=… size=… audio=…'
- **أرقام / params:** exit codes 0 ok, 1 usage, 2 render, 3 verify
- **الدليل / proof:** `kosif-tool/tools/render_html.cjs:399` · `kosif-tool/tools/render_html.cjs:580`

#### QA-65 · تقرير الفحص بـ 16 بندًا · TEST_REPORT 16-check QA template · ✅ مُثبت هنا
- **ماذا / what:** Measured-values report: duration, fps, frames, resolution, audio track, untouched voice, loudness, phone legibility, RTL shaping, key-word sync, motion in every scene, safe margins, contrast, first/last frame, assets licensing, preview approval; with ffprobe/ffmpeg commands incl. 4x4 contact sheet a…
- **كيف / how:** scaffold fills {duration},{fps},{frames},{resolution}; any FAIL blocks delivery
- **الدليل / proof:** `kosif-tool/templates/TEST_REPORT.md`

#### QA-66 · فحص المستودع والإحصاءات · kosif.py validate / stats · ✅ مُثبت هنا
- **ماذا / what:** validate passes through to tools/validate.py; stats counts by origin/type/category/aspect, top creators, brief and playbook coverage.
- **كيف / how:** python3 tools/kosif.py validate [--quiet|--json]; stats [--top 10] [--json]
- **أرقام / params:** stats now: 288 styles, 243 PromptsMotion + 45 KOSIF, 44 briefs, 14/14 playbooks
- **الدليل / proof:** `kosif-tool/tools/kosif.py:606` · `kosif-tool/tools/kosif.py:614`

#### QA-67 · مجموعة الاختبارات · Test suite (node --test + unittest) · ✅ مُثبت هنا
- **ماذا / what:** npm test runs 5 node tests (generator, markdown) and 55 Python tests (catalog, CLI, templates, validate, words_convert, verify_video on a synthetic ffmpeg clip); all passed here in ~10 s.
- **كيف / how:** npm test
- **الدليل / proof:** `kosif-tool/tests/test_cli.py` · `kosif-tool/tests/test_tools_extra.py` · `kosif-tool/package.json`

#### QA-68 · فحص إزاحة مزامنة الشفاه بالارتباط المتقاطع · Lip-sync offset check by cross-correlation · 🟢 جاهز
- **ماذا / what:** Measure whether a generated clip actually used the audio reference by cross-correlating its soundtrack with the reference slice.
- **كيف / how:** Decode both to 16 kHz mono, GCC-PHAT cross-correlation; sharp peak near 0 ms = lips locked; clear peak elsewhere = shift the clip start (baseStart) by that lag; no clear peak = regenerate; at 120 BPM one beat = 500 ms so require the peak to dominate the next one. Then eyeball mouths at sung words (open on vowels, closed on m/b/p).
- **أرقام / params:** 16 kHz; example shift 475 ms
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video` · `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md`

#### QA-69 · حارس القيم الشاذة · NaN/Inf guard pass · 🟢 جاهز
- **ماذا / what:** Zeroes NaN/Inf pixels and clamps HDR before bloom so bad pixels don't bloom into black rectangles.
- **كيف / how:** First pass in K3.makePost (post.guard).
- **أرقام / params:** clampMax 48
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:364` · `kosif-studio/motion/kit/three-kit.js:364` · `kosif-studio/motion/references/hyperframes-authoring.md`

#### QA-70 · فحص التركيب · Composition lint rules · 🟢 جاهز
- **ماذا / what:** Determinism/taste lint: no Math.random, Date.now, timers, dir=rtl on html, CSS transitions, glow text-shadow, linear eases, infinite repeat, backdrop-filter.
- **كيف / how:** qa.lint(project) / motion.py check
- **أرقام / params:** 12 rules
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/qa.py:62` · `kosif-one/tools/kosif-studio/motion/qa.py:58`

#### QA-71 · قياس طاقة الحركة · Motion energy measure · 🟢 جاهز
- **ماذا / what:** Reports near-still share, mean and peak frame difference of a film.
- **كيف / how:** python motion.py measure FILM.mp4 [--fps 15].
- **أرقام / params:** norm: median diff 1.4, p90 6.0 (320 px luma); calm premium 0.35-0.5
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/motion.py:486` · `kosif-one/tools/kosif-studio/motion/references/craft-numbers.md` · `kosif-studio/motion/motion.py:423`

#### QA-72 · كشف مكتبات الحركة ونموذج التفاعل · Motion-library and interaction-model detection · 🟢 جاهز
- **ماذا / what:** Detect whether a reference site uses GSAP, Lottie, anime.js, Lenis/Locomotive, Three/Pixi/WebGL canvas, SVG SMIL, custom cursors, backdrop filters, blend modes, clip paths; classify each section as static, click-, scroll- or time-driven by scrolling slowly before clicking.
- **كيف / how:** In-page script checking window globals, script src, computed styles; scroll sweep with screenshots at scroll 0 and past thresholds and diff.
- **أرقام / params:** rule: scroll before you click
- **الدليل / proof:** `kosif-atlas/skills/3594-design-clone/14410-design-clone`

#### QA-73 · مقارنة صور بدون اعتمادات · Dependency-free PNG visual diff · 🟢 جاهز
- **ماذا / what:** Compare a rendered frame against its reference: per-pixel diff ratio, similarity score, alpha flag and an 8x8 grid of ranked hotspots showing where it deviates; evidence for review, not a verdict.
- **كيف / how:** node visual-diff.mjs ref.png actual.png --json --tolerance N (node:zlib only; review before running) or reimplement with Pillow/numpy.
- **أرقام / params:** grid 8x8; max 25M pixels; 8-bit non-interlaced PNG
- **الدليل / proof:** `kosif-atlas/skills/880-superloopy/1941-superloopy-frontend/scripts/visual-diff.mjs`

#### QA-74 · إعدادات التقاط واجهة قابلة للتكرار · Reproducible UI capture settings · 🟢 جاهز
- **ماذا / what:** Capture before/after or current-state UI with identical route, viewport, scale, theme, locale, timezone, data and interaction state; wait for observable readiness (content visible + fonts loaded) rather than sleeps; drive hover/focus/menus explicitly; keep the same crop for pairs; inspect every fram…
- **كيف / how:** Playwright test.use({viewport:{width:1280,height:820}, deviceScaleFactor:2, colorScheme:'light', locale}) -> await page.evaluate(() => document.fonts.ready) -> page.screenshot.
- **أرقام / params:** default 1280x820 @2x
- **الدليل / proof:** `kosif-atlas/skills/1530-webcraft/4196-ui-screenshots/SKILL.md`

#### QA-75 · التقاط إطارات مرجعية لمطابقة الأسلوب · Reference capture for style matching · 🟢 جاهز
- **ماذا / what:** To copy a look (not content) from a reference, grab frames at 0.5-1 s steps across appear/hold/emphasis/exit and measure glyph height, margins, alignment, colours, reveal order and read time; never ship the reference's people, words or memes.
- **كيف / how:** ffmpeg -ss T -i ref -frames:v 1 -q:v 2 f_T.png in a temp dir; open each frame
- **أرقام / params:** 0.5-1 s step
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2430-akbun-davinciresolve-article-overlay/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2431-akbun-davinciresolve-caption-template/SKILL.md`

#### QA-76 · ورقة إطارات الكلمات وبوابة تزامن الضربات · Word-frame sheet and hit-sync gate · 🟢 جاهز
- **ماذا / what:** Before delivery every sung word and every musical hit is checked on the actual rendered frames.
- **كيف / how:** Extract one frame at each word onset into a labelled contact sheet (8 columns, 220 px cells) and compare sound onset vs picture change at hit times — pass within one frame; contact sheet every 1 s for the whole film and every 0.5 s for hook/chorus.
- **أرقام / params:** tolerance 1 frame; sheets every 1 s / 0.5 s
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video`

#### QA-77 · قراءة بيانات التوليد المضمنة · Embedded generation metadata readback · 🟢 جاهز
- **ماذا / what:** ComfyUI outputs embed the exact prompt and workflow, so a still or clip can be reproduced or audited.
- **كيف / how:** PNG tEXt keys 'prompt'/'workflow' (PIL Image.info); animated PNG iTXt; WebP EXIF 0x0110 'prompt:' and 0x010F 'workflow:'; MP4/WebM container keys (kijai wrapper: one double-encoded 'comment'); .latent safetensors header.
- **الدليل / proof:** `kosif-atlas/skills/2142-comfyui-plugin/7653-comfy-metadata`

#### QA-78 · وثيقة الهوية المولدة من الرموز · Identity doc generated from tokens · 🟢 جاهز
- **ماذا / what:** Regenerates the identity reference so every hex in the doc is the one rendered.
- **كيف / how:** python3 tools/identity_doc.py [root] parses tokens.css selector blocks (later blocks win) and writes docs/design/SQC-IDENTITY-ar.md.
- **الدليل / proof:** `kosif-earth-ci-fork/tools/identity_doc.py` · `kosif-earth-ci-fork/docs/design/SQC-IDENTITY-ar.md`

#### QA-79 · مسح بصري بـ Playwright · Playwright visual sweeps (desktop + 390/320px phones) · 🟢 جاهز
- **ماذا / what:** Browser sweeps that open every registered screen on laptop and phone, screenshot it and fail on page errors, broken values (undefined/NaN/[object Object]), horizontal overflow, clipped controls or empty views; a clutter audit measures chrome vs content.
- **كيف / how:** node tools/page_review.mjs URL [out]; node tools/phone_layout.mjs; node tools/ui_smoke.mjs URL; node tools/clutter_audit.mjs URL [out]; all need a served build.
- **أرقام / params:** phone 390x844 and 320px; laptop viewport
- **الدليل / proof:** `kosif-earth-ci-fork/tools/page_review.mjs` · `kosif-earth-ci-fork/tools/phone_layout.mjs` · `kosif-earth-ci-fork/tools/ui_smoke.mjs`

#### QA-80 · بوابة المعاينة قبل التصدير · Preview-before-final-render gate · 🟢 جاهز
- **ماذا / what:** No final render, publishing, paid API call or third-party upload until the user explicitly approves the preview; local smoke renders are allowed.
- **كيف / how:** render.py forces exactly one of --smoke / --approved; agent only passes --approved after the user says e.g. 'ارندر' / 'اعتمد'.
- **أرقام / params:** --smoke default 2 s capped at 12 s
- **الدليل / proof:** `fastify-motion-bro/AGENTS.md:15` · `fastify-motion-bro/scripts/render.py:17` · `fastify-motion-bro/README.md:32`

#### QA-81 · إيصال الفحص الفني · ffprobe QA receipt · 🟢 جاهز
- **ماذا / what:** Probes the MP4 and writes output/qa_report.json; passes only if a video stream exists, codec is h264, width/height are even and duration > 0, and it explicitly records manual review NOT_DONE and word alignment NOT_VERIFIED.
- **كيف / how:** python scripts/qa.py output/final.mp4 (exit 1 on failure).
- **أرقام / params:** checks: h264, even dims, duration>0; fields duration, video, bytes
- **الدليل / proof:** `fastify-motion-bro/scripts/qa.py:1-18`

#### QA-82 · إثبات التغير الزمني بالبصمة · Temporal-change frame-hash proof · 🟢 جاهز
- **ماذا / what:** Proves a render is real motion by extracting frames at several timestamps and requiring all SHA-256 hashes to differ.
- **كيف / how:** CI: ffmpeg -ss t -frames:v 1 at 0.8, 3.8, 5.4, 6.5 s of a 7 s 360p 6 fps editorial smoke; assert 4 unique hashes.
- **أرقام / params:** t = 0.8/3.8/5.4/6.5 s; 4 unique
- **الدليل / proof:** `fastify-motion-bro/.github/workflows/ci.yml:55-67`

#### QA-83 · تعليم المقاطع الخطرة نصياً · Text-risk clip flagging · 🟢 جاهز
- **ماذا / what:** Flags clips whose words exceed 10 Latin letters or contain digits/hyphens because AI video may misspell them.
- **كيف / how:** risks.push(i+1) if token letters>10 or /\d|-/; listed in FLOW TIPS.
- **أرقام / params:** >10 letters, digits, hyphens
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:114,118`

#### QA-84 · تحديد موقع عنصر في صورة بشبكة مرقمة · Grid-index visual grounding (locate X in an image) · 🟢 جاهز
- **ماذا / what:** Find a target's box in an image without a detector API: overlay numbered 1-9 vertical/horizontal strips, the model picks strips, region crop + upscale, refine; optional Gemini auto path; returns normalized box and center.
- **كيف / how:** node grounding/locate.mjs overlay <img> --out DIR -> read gv.png/gh.png -> node locate.mjs region <img> --vids 4,5 --hids 6,7 --out DIR; or `locate.mjs auto <img> '<target>'` with GEMINI_API_KEY.
- **أرقام / params:** strip picking ~3-4% center error vs 16-24% direct regression
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/motion-graphics/grounding/locate.mjs` · `kosif-one/vendor/hyperframes/skills/motion-graphics/grounding/PROTOCOL.md`

#### QA-85 · كوسف: بوابة التسليم وقياسات الحركة · KOSIF: delivery inspect gate and motion measures · 🟢 جاهز
- **ماذا / what:** Post-render checks absent from vendor CLI: yuv420p/H.264, real black frames, unintended freezes, LUFS within +/-1.5 of -14 and true peak <= -1 dB; motion energy still share/peak/mean; speed caps (text <= 3 px/frame, nothing > ~80 px/frame); contact sheet + 360 px phone test + review.md critique roun…
- **كيف / how:** python3 scripts/motion.py inspect out/NAME.mp4 [--allow 6.6-7.3]; motion.py measure; motion.py speed; motion.py sheet.
- **أرقام / params:** -14 LUFS, TP <= -1 dB
- **الدليل / proof:** `100-superskills/skills/hyperframes-animation-studio/scripts/qa.py` · `100-superskills/skills/hyperframes-animation-studio/scripts/motion.py` · `100-superskills/skills/hyperframes-animation-studio/references/craft-numbers.md`

#### QA-86 · فحص الملفات والخطوط · probe / fonts · 🟢 جاهز
- **ماذا / what:** Streams/duration; list Arabic fonts available.
- **كيف / how:** python scripts/kmotion.py probe FILE; fonts
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### QA-87 · بوابة التسليم · inspect delivery gate · 🟢 جاهز
- **ماذا / what:** yuv420p H.264 even size, no unintended black/frozen, −14±1.5 LUFS, TP ≤ −1, blown/crushed checks.
- **كيف / how:** python scripts/kmotion.py inspect FILM [--allow a-b]
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:207` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### QA-88 · ورقة المراجعة · sheet contact review · 🟢 جاهز
- **ماذا / what:** Contact 2 fps, phone 360 px, first frame, strip, review.md P0/P1/P2 with 12 aesthetic lenses.
- **كيف / how:** python scripts/kmotion.py sheet FILM
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:207` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### QA-89 · فحص التركيب · lint composition · 🟢 جاهز
- **ماذا / what:** Determinism, contract, taste checks.
- **كيف / how:** python scripts/kmotion.py lint PROJECT
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:207` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### QA-90 · دراسة مرجع · study reference · 🟢 جاهز
- **ماذا / what:** Cuts, shot lengths, first change, energy, palette → style_guide.md.
- **كيف / how:** python scripts/kmotion.py study REF.mp4
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:207` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### QA-91 · فحص الحلقة · loopcheck · 🟢 جاهز
- **ماذا / what:** Prove a loop seam.
- **كيف / how:** python scripts/kmotion.py loopcheck FILM
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:207` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### QA-92 · فحص المقروئية · readable · 🟢 جاهز
- **ماذا / what:** Every line settled ≥ max(0.8 s, 0.3 s×words); hook ≤2 s.
- **كيف / how:** python scripts/kmotion.py readable reel.json|verse.json|edit.json
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:207` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### QA-93 · تثبيت الغلاف · poster bake · 🟢 جاهز
- **ماذا / what:** Strongest settled frame baked as frame 0, frame count/duration/sound unchanged.
- **كيف / how:** python scripts/kmotion.py poster FILM [--at T] --bake
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:207` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### QA-94 · بوابة العربية · Arabic delivery gate · 🟢 جاهز
- **ماذا / what:** Spelling, joined letters, RTL, order (ASS Encoding -1), descender dots, max 2 lines, 9:16 text between ~15% and ~80% height, off right UI, never over eyes/mouth.
- **كيف / how:** python scripts/kmotion.py manual + frames
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:207` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### QA-95 · صفحة المراجعة · Review page (Motion OS) · 🟢 جاهز
- **ماذا / what:** reel.json scenes/elements served at /review/NAME/; user edits saved; apply writes bound edits; bump versions.
- **كيف / how:** python scripts/kmotion.py review init|feedback|apply|bump
- **أرقام / params:** MIT Motion OS commit 6dbf5da
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:207` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### QA-96 · مشغل المعاينة · Self-playing preview player · 🟢 جاهز
- **ماذا / what:** Opening a composition in a normal browser plays it in real time with audio, scaled to the window, with play/pause, scrub bar and Space key; hidden from renderers.
- **كيف / how:** Automatic from MOTION.shim when not navigator.webdriver, not ?render, not HyperFrames.
- **أرقام / params:** bar 48 px #14161a; button #E7B65A; clock follows playing media element
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:496`

#### QA-97 · وسوم الأمانة للمحاكاة التوضيحية · Honesty labels for illustrative simulations · 🟢 جاهز
- **ماذا / what:** Simulated numbers are labelled on screen and in data as illustrative, chosen values, not measurements, with a scope warning that it is not for safety decisions; break paths are called hypothetical.
- **كيف / how:** HUD #note 'ILLUSTRATIVE 3D SPACE-TRUSS PROXY · CHOSEN VALUES · NOT A MEASURED TOY'; report.json source_note + scope_warning; break.warning 'no buckling, fracture, fatigue or dynamic redistribution'; dashboard 'Analysis boundary' notice.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:71` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/twin/report.json` · `100-superskills/skills/kosif-montage-motion/examples/structural-twin-demo.html:6`

#### QA-98 · ورقة لقطات وفحص السرعة · Contact sheet + speed check · 🟢 جاهز
- **ماذا / what:** 2 fps contact sheet, phone-width test, optical-flow px/frame speed.
- **كيف / how:** qa.sheet / qa.speed
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/qa.py:1`

#### QA-99 · دراسة فيلم مرجعي · Reference study · 🟢 جاهز
- **ماذا / what:** Measure cuts, shot lengths, energy, palette of a reference into a style guide.
- **كيف / how:** qa.study(reference)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/qa.py:1`

#### QA-100 · مراجعة المشاهد · Review loop · 🟢 جاهز
- **ماذا / what:** reel.json review page; feedback applied to source, re-render.
- **كيف / how:** kmotion review init|apply|export|feedback
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/review.py`

#### QA-101 · فحص البيئة · Environment check · 🟢 جاهز
- **ماذا / what:** Reports route A/B/C and available capabilities.
- **كيف / how:** python3 env_check.py
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/env_check.py`

#### QA-102 · شارات حالة البيئة · Environment status pills · 🟢 جاهز
- **ماذا / what:** The site header shows which route (A/B/C) the PC supports, FFmpeg, a browser, Whisper, CPU cores, the face detector and the number of xfade transitions; the env tab shows the full JSON.
- **كيف / how:** GET /api/env (env_check.check() cached 120 s) and MCP kosif_env; recipe doctor.
- **أرقام / params:** cache TTL 120 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:257` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/app.js:27`

#### QA-103 · المراجعة: معاينة شبحية للعناصر المنقولة · Review: ghost preview of moved elements · 🟢 جاهز
- **ماذا / what:** When an element is moved or resized on a rendered video, the old spot is blurred and that patch of the live video is redrawn at the new spot, so the change is visible before re-rendering.
- **كيف / how:** drawGhosts(): per edited box a .was div at the original box and a canvas that drawImage()s the source patch of <video> into the new box at devicePixelRatio; live projects get setBoxes() instead.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:573`

#### QA-104 · المراجعة: ملاحظات مثبتة على الإطار · Review: pinned frame notes · 🟢 جاهز
- **ماذا / what:** Note mode (N) or Alt-click pins a numbered note to an exact time and x/y spot (and the element under it); notes sort by time, move a scene to 'changes', and appear as markers on the timeline.
- **كيف / how:** renderPop()/popLayer handlers; note = {id, t (2 decimals), x, y (1 decimal), el, text}; Ctrl/Cmd+Enter adds, Esc cancels.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:637`

#### QA-105 · المراجعة: إعادة التحميل التلقائي والروابط العميقة · Review: auto-reload on new version and deep links · 🟢 جاهز
- **ماذا / what:** The page polls reel.json and reloads itself when Claude bumps the version; a URL hash can jump to a time and select an element.
- **كيف / how:** setInterval fetch('reel.json', no-store) every 3000 ms; #t=12.5&el=ID; per-project edits in localStorage key 'motionos:<id>', with already-sent edits cleared on a new version.
- **أرقام / params:** poll 3 s; video starts at 0.7 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:986` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:441`

#### QA-106 · تقرير التصدير · Export report object · 🟢 جاهز
- **ماذا / what:** After an offline export the page records what was produced so a script or Claude can verify it: codec, audio codec, frames, fps, size, bytes, seconds taken, skipped audio files and loudness before/after/gain/limitedByPeak.
- **كيف / how:** globalThis.__kosifLastExport; status line in Arabic with MP4 size, fps, frames, MB, seconds, LUFS.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:146`

#### QA-107 · قياس الحدة والضجيج · Sharpness and noise measurement · 🟢 جاهز
- **ماذا / what:** Rates focus with Laplacian variance (global and the mean of the 3 most detailed tiles of an 8×8 grid, so a sharp subject on bokeh still counts) and noise with Immerkaer's fast sigma estimate.
- **كيف / how:** sharpness(gray, grid=8), noise_sigma(gray).
- **أرقام / params:** blurry < 60 ≤ soft < 150 ≤ sharp; clean < 2.5 ≤ moderate < 6 ≤ noisy
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:78` · `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:89`

#### QA-108 · مقارنة صورتين لاستمرارية اللقطات · A/B image comparison for shot continuity · 🟢 جاهز
- **ماذا / what:** Compares two images metric by metric (brightness, contrast, clipping, CCT, saturation, colourfulness, sharpness, noise, symmetry) and says which is sharper and cleaner — e.g. last frame of one generated chunk vs first frame of the next.
- **كيف / how:** python3 scripts/omni/image_analyze.py A.jpg B.jpg --compare.
- **أرقام / params:** 10 metrics with deltas
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:227`

#### QA-109 · لوحة فحص 4×4 من الإطارات · Contact sheet 4x4 (every 15th frame) · 🟢 جاهز
- **ماذا / what:** Builds one PNG grid of sampled frames so a reviewer (or Claude's vision) can check a whole video at a glance before delivery.
- **كيف / how:** ffmpeg -i video -vf "select='not(mod(n\,15))',scale=270:480,tile=4x4" -frames:v 1 contact-sheet.png (run automatically by ultra_animator encode and qa_inspector).
- **أرقام / params:** 1 of every 15 frames, tiles 270x480, grid 4x4 = 16 samples (covers 8 s at 30 fps)
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/ultra_animator.py:239` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/qa_inspector.py:128`

#### QA-110 · فاحص جودة الفيديو · Video QA inspector (black/freeze/loudness) · 🟢 جاهز
- **ماذا / what:** Probes a finished MP4 for black spans, frozen frames, loudness and size, writes a contact sheet and returns PASS/WARN/FAIL JSON.
- **كيف / how:** python scripts/qa_inspector.py out.mp4 [--json] [--out report.json]; ffprobe streams; blackdetect=d=0.5:pic_th=0.98 (FAIL if a span > 1.0 s); freezedetect=n=-60dB:d=1.5 (WARN); ebur128 (WARN if > -10 or < -24 LUFS). BUG: runs ffmpeg with -v error so the ebur128 summary never prints — lufs_integrated is always null and the loudness gate silently passes; also needs ebur128=peak=true for true peak.
- **أرقام / params:** black d 0.5 s / pic_th 0.98 / fail > 1.0 s; freeze -60 dB / 1.5 s; loudness window -24..-10 LUFS; aspect label from w/h
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/qa_inspector.py:21` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/qa_inspector.py:73` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/SKILL.md`

#### QA-111 · تحليل صوتي مقاس · Measured audio analysis (BS.1770 loudness, true peak, BPM, spectrum) · 🟢 جاهز
- **ماذا / what:** Reports loudness, peaks, clipping, silence, stereo health, tonal balance and tempo of any audio file, with Arabic fix suggestions — the check for a voice-over or a finished mix.
- **كيف / how:** python3 scripts/audio_analyze.py FILE --summary [--target streaming|podcast|broadcast|club] [--plot out.png] (MCP kosif_audio_analyze); WAV natively, other formats via ffmpeg; plot needs matplotlib.
- **أرقام / params:** K-weighting + 400 ms blocks/100 ms hop, gates -70 / -10; true peak 4x Kaiser-windowed sinc (12 taps/phase); clip >= 0.999; silence < -50 dB for >= 0.5 s; bands sub 20-60, bass 60-250, low-mid 250-500, mid 500-2k, presence 2-6k, air 6-20k; tempo spectral-flux autocorr 60-200 then folded into 70-180 B…
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-audio/scripts/audio_analyze.py:87` · `kosif-one/tools/kosif-omni/skills/kosif-audio/scripts/audio_analyze.py:195` · `kosif-one/tools/kosif-omni/skills/kosif-audio/SKILL.md`

#### QA-112 · تحليل صورة مقاس · Measured image analysis · 🟢 جاهز
- **ماذا / what:** Measures exposure, tonal key, colour temperature, cast, saturation, palette, sharpness, noise, light side and composition of a frame — for checking renders, grading references and reverse-engineering looks.
- **كيف / how:** python3 scripts/image_analyze.py IMG [--summary] or MCP kosif_image_analyze path= [compare_with=]; Pillow + numpy; downsizes to 1600 px.
- **أرقام / params:** clip >= 250, crushed <= 5; zones <85 / 85-170 / >=170; exposure over if mean > 185 or clip > 5%; McCamy CCT; cast +/-12; Laplacian var blurry < 60, soft < 150; noise sigma clean < 2.5, noisy >= 6; light side +/-8 luma; thirds distance < 0.08; ran OK here
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-vision/scripts/image_analyze.py:120` · `kosif-one/tools/kosif-omni/skills/kosif-vision/SKILL.md`

#### QA-113 · مقارنة إطارين · A/B frame comparison · 🟢 جاهز
- **ماذا / what:** Compares two images metric by metric — used to check continuity between stitched clips or before/after grades.
- **كيف / how:** image_analyze.py A B --compare (MCP compare_with); 10 metrics with deltas + sharper/cleaner verdict.
- **أرقام / params:** metrics: mean luma, contrast std, clipped %, crushed %, CCT, saturation, colourfulness, sharpness, noise, symmetry
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-vision/scripts/image_analyze.py:227`

#### QA-114 · لوحة معاينة المصادر · Source contact sheet for footage triage · 🟢 جاهز
- **ماذا / what:** One JPEG showing two frames (early and middle) of every candidate clip so burned-in text, logos or wrong style can be spotted before editing.
- **كيف / how:** ffprobe duration; ffmpeg -ss at=min(1.5,0.2d) and min(0.63d,d-0.2) -frames:v 1 -vf scale=240:420:force_original_aspect_ratio=increase,crop=240:420; paste into a Pillow canvas (7 cols x 2 rows, 240x450 cells, bg (14,18,26)) with file name labels. v2 variant: 32 clips in 8x4 grid of 192x342 cells at t=2 s.
- **أرقام / params:** cells 240x450 or 192x342; JPEG quality 80-82
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/tools/qa_contact.py` · `kosif-one/projects/ghorba-motion-v2/make_contact.py`

#### QA-115 · أوراق المراجعة · Critique sheets: contact, phone, strip + review.md · 🟢 جاهز
- **ماذا / what:** Builds a 2 fps contact sheet, a 360 px phone-width test, a 12-frame strip around a moment, the first frame, and a review rubric.
- **كيف / how:** python motion.py sheet FILM.mp4 [--at 4.2] [--out DIR]; read the PNGs and fix the three worst issues, >= 3 rounds.
- **أرقام / params:** contact 320 px tiles at 2 fps; phone 360 px at 1 fps 5 columns; strip 12x1 at 320 px
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/qa.py:1` · `kosif-one/tools/kosif-studio/motion/references/craft-numbers.md`

#### QA-116 · فحص مسبق لمهمة الوسائط · Media job preflight (proplan) · 🟢 جاهز
- **ماذا / what:** Deterministic read-only preflight that states what a media job can truthfully claim (NOT_FULL_PRO without runtime receipts).
- **كيف / how:** python motion/proplan.py ...
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/proplan.py`

#### QA-117 · فحص الملفات والدفعات والخطوط · Probe, batch and Arabic font scan · 🟢 جاهز
- **ماذا / what:** Probe streams/duration/fps/loudness, run several kmotion jobs in parallel, list Arabic-capable fonts on the machine.
- **كيف / how:** python tools.py probe FILE | batch jobs.json [--parallel 2] | fonts.
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/tools.py:1`

#### QA-118 · فحص أمان الكود الملصوق · Pasted-code safety scan + sandbox · 🟢 جاهز
- **ماذا / what:** Scans pasted code for file deletion, process launch, network or low-level access and asks first; runs in a separate process with a 120 s limit in a scratch folder; SVG is data and never checked.
- **كيف / how:** studio.risky(code) over RISKY patterns.
- **أرقام / params:** 120 s timeout
- **الدليل / proof:** `kosif-one/tools/kosif-studio/studio.py:49` · `kosif-one/tools/kosif-studio/studio.py:167`

#### QA-119 · أوراق مراجعة المحاكاة · Review contact sheets (shots, transitions, texts, side by side) · 🟢 جاهز
- **ماذا / what:** Sheets Claude and the user look at to fill texts, describe shots and compare remake vs reference.
- **كيف / how:** mm_sheets.all_sheets / side_by_side.
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_sheets.py`

#### QA-120 · فحص المصدر بـ ffprobe · ffprobe source inspection · 🟢 جاهز
- **ماذا / what:** Reads codec, resolution, CFR/VFR, duration, audio and keyframe positions of every source before editing.
- **كيف / how:** python3 probe.py files... [--keyframes] [--json out]; underlying ffprobe -show_format -show_streams and -show_packets packet=pts_time,flags (K=keyframe).
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/scripts/probe.py:53` · `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### QA-121 · مشغل الكود الآمن · Sandboxed AI code runner · 🟢 جاهز
- **ماذا / what:** Runs pasted picture code in a separate process, 120 s timeout, temp dir, risky() scan for delete/network/subprocess/ctypes needing consent.
- **كيف / how:** runner.py
- **أرقام / params:** 120 s
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/scripts/runner.py` · `100-superskills/skills/pixel-studio-painter/SKILL.md`

#### QA-122 · مقياس طاقة الحركة · Motion energy meter vs reference · 🟢 جاهز
- **ماذا / what:** Measures per-frame motion energy of an mp4 or frame dir: mean, peak, share above threshold, near-still share, longest freeze, luma/saturation; compares to a reference.
- **كيف / how:** python motion_energy.py build.mp4 --ref ref.mp4 --fps 15 --out motion-report.json
- **أرقام / params:** 15 fps sampling
- **الدليل / proof:** `100-superskills/skills/motion-director-pro/scripts/motion_energy.py:95`

#### QA-123 · فحص الملف · Probe media · 🟢 جاهز
- **ماذا / what:** Streams, duration, size, fps, audio rate/channels as JSON.
- **كيف / how:** python tools.py probe FILE
- **الدليل / proof:** `kosif-studio/motion/tools.py:54`

#### QA-124 · أدوات المعاينة الحية · Live preview controls (play/scrub/?t=) · 🟢 جاهز
- **ماذا / what:** Play/pause button, range scrubber, space-bar toggle, ?t=3.2 to jump, ?autoplay=1; controls hide automatically when navigator.webdriver (renderer).
- **كيف / how:** open index.html in a browser
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:219` · `kosif-tool/starters/html-canvas/index.html:232`

#### QA-125 · فاحص أصالة النصوص · Brief originality n-gram checker · 🟢 جاهز
- **ماذا / what:** Flags BRIEF texts that share a run of ≥N words (default 6) with the creator's source description, enforcing original writing.
- **كيف / how:** python3 tools/check_originality.py --briefs <dir> --texts <dir> [--ngram 6]
- **الدليل / proof:** `kosif-tool/tools/check_originality.py`

#### QA-126 · فحص التباين عبر الزمن · WCAG contrast audit over time · 📦 بأمر تثبيت
- **ماذا / what:** Sample background pixels behind every text element at several timestamps and compute contrast ratios.
- **كيف / how:** hyperframes validate (5 timestamps); fix by brightening/darkening within the palette family. Can be re-implemented here: Playwright screenshots at t values + per-element bbox luminance math.
- **أرقام / params:** 4.5:1 normal; 3:1 large (24px+ or 19px+ bold)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/SKILL.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/scripts/contrast-report.mjs`

#### QA-127 · فحص تجاوز النصوص على الخط الزمني · Layout inspect sweep · 📦 بأمر تثبيت
- **ماذا / what:** Seek through the timeline in headless Chrome and report text spilling out of containers, clipped text and off-canvas elements, with timestamps.
- **كيف / how:** npx hyperframes inspect --json --samples 15 or --at 1.5,4,7.25; mark intentional overflow with data-layout-allow-overflow, ignore decoratives with data-layout-ignore.
- **أرقام / params:** samples 15
- **تثبيت / install:** `npx hyperframes inspect --json --samples 15 or --at 1`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/SKILL.md` · `kosif-atlas/skills/2702-hyperframes/10379-hyperframes-cli/SKILL.md`

#### QA-128 · خريطة الحركة لتدقيق الكوريغرافيا · Animation map (choreography audit) · 📦 بأمر تثبيت
- **ماذا / what:** Produce per-tween summaries, an ASCII Gantt of all tweens, measured stagger intervals, dead zones and flags (offscreen, collision, invisible, too fast, too slow).
- **كيف / how:** animation-map.mjs <dir> --out ...; flags: paced-fast <0.2s, paced-slow >2s, dead zone >1s without motion. Idea re-implementable with a GSAP timeline walker (tl.getChildren()).
- **أرقام / params:** fast <0.2s; slow >2s; dead zone >1s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/SKILL.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/scripts/animation-map.mjs`

#### QA-129 · حزمة أسلوب بنطاقات إحصائية · Style pack with statistical bands · 📦 بأمر تثبيت
- **ماذا / what:** Measure a drawn style into knob values and p10/p50/p90 bands (edge roughness, stroke widths, solid black, boil rate, holds) and check whether a new film stays inside them.
- **كيف / how:** style.json: palette (ink, paper, tone ramp), seven knobs, stats, timing, bands, check; validate with controls that must fail (blur/noise/near-miss filters) and positives that pass; new scene >= 1/3 source length authored with own geometry.
- **أرقام / params:** p10/p50/p90
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9355-learn-style/SKILL.md`

#### QA-130 · قالب تحليل فيديو مرجعي · Reference-video breakdown template · 📦 بأمر تثبيت
- **ماذا / what:** To learn from a reference reel or post: sample frames across the timeline (all slides for carousels), get a verbatim timestamped transcript and the caption, then write header, TL;DR, full transcript, on-screen text and visuals timeline, verbatim caption, beat-by-beat structure (hook -> points -> CTA…
- **كيف / how:** Here with a user-supplied local file: ffmpeg frame sampling + reading frames with vision + transcript from provided words.json or whisper (needs install). Never claim to have watched what could not be opened.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1083-social-vision/2399-analyze-social/SKILL.md`

#### QA-131 · اختبار الإطارات الذهبية بأداة odiff · Golden-frame regression with odiff · 📦 بأمر تثبيت
- **ماذا / what:** Pixel-compare rendered frames against approved goldens with exit-code verdicts: 0 match, 22 pixel differences, 21 size/layout change (with --fail-on-layout); suppress antialias noise on text, ignore dynamic rectangles (timestamps), write a magenta diff image.
- **كيف / how:** npm i -g odiff-bin (needs install). odiff golden.png frame.png diff.png --aa -t 0.05 --fail-on-layout --parsable-stdout -i x1:y1-x2:y2. Grab frames with ffmpeg -ss t -frames:v 1. Fallback that runs here: numpy abs-diff + PIL.
- **أرقام / params:** threshold default 0.1 (strict 0.02-0.05); diff colour #cd2cc9
- **تثبيت / install:** `npm i -g odiff-bin (needs install)`
- **الدليل / proof:** `kosif-atlas/skills/2172-testing-plugin/7896-odiff-image-diffing/SKILL.md`

#### QA-132 · سجل ألوان العلامات · Marker colour registry · 📦 بأمر تثبيت
- **ماذا / what:** Use a fixed marker vocabulary so review is machine-readable: chapter, cut-done, cut-review, privacy, exposure/WB checks, audio review, hook, GFX; Resolve allows one marker per frame and only 16 colours (Blue Cyan Green Yellow Red Pink Purple Fuchsia Rose Lavender Sky Mint Lemon Sand Cocoa Cream); of…
- **كيف / how:** Timeline.AddMarker / TimelineItem.AddMarker(frameId = absolute - GetStartFrame())
- **أرقام / params:** 16 colours
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound/SKILL.md`

#### QA-133 · مشاهدة فيديو مرجعي بالإطارات والتفريغ · Watch a reference video (frames + transcript) · 📦 بأمر تثبيت
- **ماذا / what:** Understand a social/local video by sampling frames across the timeline (scene-detect + perceptual-hash dedupe + stratified interval + transcript-anchored frames, no hard cap), reading them with vision, plus a full timestamped transcript and caption; every frame keeps a measured, estimated (±half int…
- **كيف / how:** yt-dlp/gallery-dl acquire (install), ffmpeg frames, faster-whisper; contact sheets for triage; output: header, TL;DR, verbatim transcript, on-screen text timeline, beat structure hook->CTA
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1083-social-vision/2399-analyze-social/SKILL.md` · `kosif-atlas/skills/2451-knowledge/9503-video-digest/context/watch-pipeline.md`

#### QA-134 · التحقق من تزامن القطع مع الضربة · Onset-sync verification · 📦 بأمر تثبيت
- **ماذا / what:** Every cut must change the picture within one frame of the sound onset.
- **كيف / how:** Compute onsets (librosa.onset or energy-flux numpy) and scene-change times (ffmpeg select='gt(scene,0.3)'), assert |diff|<=1/fps.
- **أرقام / params:** <=1 frame
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video`

#### QA-135 · التعامل مع فقد جهاز GPU · WebGPU device-loss handling · 📦 بأمر تثبيت
- **ماذا / what:** Headless renders can lose the GPU device; detect and rebuild instead of producing black frames.
- **كيف / how:** renderer device.lost promise -> recreate renderer/resources; check limits/features before using big buffers.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/device-loss.md` · `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/limits-and-features.md`

#### QA-136 · بوابات جودة الروتوسكوب · Rotoscope fidelity gates · 📦 بأمر تثبيت
- **ماذا / what:** Replica acceptance per drawing measured, not eyeballed.
- **كيف / how:** Compare render vs source: XOR <= 1.2x codec floor, SSIM >= 0.980, edge-band SSIM >= 0.980; review worst crops.
- **أرقام / params:** SSIM>=0.98
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9357-rotoscope`

#### QA-137 · نظافة البيانات المكانية · Spatial data hygiene · 📦 بأمر تثبيت
- **ماذا / what:** Invalid or mis-projected geometry produces blank maps, points in the ocean and crashing area/union operations.
- **كيف / how:** Validate (ST_IsValid / ST_MakeValid), ensure SRID is set (not 0), reproject to WGS84 (EPSG:4326) for GeoJSON, handle empty geometries, check adjacent polygons for gaps/overlaps; if features land in the wrong place the data is probably not lon/lat WGS84.
- **أرقام / params:** EPSG:4326 for GeoJSON; EPSG:3857 for web tiles
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2307-geospatial-engineering/8858-spatial-data-quality/SKILL.md` · `kosif-atlas/skills/1650-portaljs/4640-portaljs-add-map/SKILL.md`

#### QA-138 · قياس مستوى الكلام والضوضاء · Speech level and noise-floor measurement · 📦 بأمر تثبيت
- **ماذا / what:** Measures speech level, noise floor, peak and SNR to decide gain, low-cut and compression.
- **كيف / how:** AUD.measure: 50 ms RMS frames; noise = 15th percentile; speech = 70th percentile of frames > noise+8 dB; gain = clamp(-20 - speech, -12, 26); lowcut 120 Hz when SNR < 14 dB; comp = 0.45 or clamp((peak-speech)/30, 0.35, 0.8).
- **أرقام / params:** frames 50 ms
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:3848`

#### QA-139 · اكتشاف القطعات في الفيديو · Footage shot/cut detection (reference probe) · 📦 بأمر تثبيت
- **ماذا / what:** Counts hard cuts, average shot length, motion and still share of any reference video locally.
- **كيف / how:** analyzeRef(): samples every 0.25 s (16-72), 40x40 luma frames; mean absolute diff; threshold = max(18, min(8*median, mean+1.8*sd)); returns cuts, avgShot, cutsPer10, still share (<0.5 diff), up to 8 JPEG key frames (512 px, q 0.8) for the model.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:1299`

#### QA-140 · تحليل بصمة المرجع العميق · Style DNA deep reference study · 📦 بأمر تثبيت
- **ماذا / what:** A local study of a reference: frame-accurate cuts (hard cuts, whips, dissolves, white flashes, dips), per-shot camera moves from a motion field, palette and grade, caption band/size/colour/rate, per-second energy and beat alignment of cuts.
- **كيف / how:** DNA.analyze: sample fps 8/6/4/2/1 by length (12-420 samples), 48x48 luma grid; every presented frame gets a 64-bin histogram; chi-square distance at two scales (frame-to-frame and ~0.25 s), threshold max(0.28, 7*p60); flash = brightness spike that returns; motionEst() searches scale +-0.02 and shift for global motion -> push/pull/pan/still/shake; textBands() finds dense horizontal-edge rows (>9% of row) for caption band; onBeat share of cuts.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:1178` · `app/public/js/10_studio.js:1192` · `app/public/js/10_studio.js:1203`

#### QA-141 · درجة التشابه مع المرجع وتصليحها · Fingerprint similarity score and auto-fix · 📦 بأمر تثبيت
- **ماذا / what:** Renders the product through the same measurements and scores it against the reference, then closes the biggest gap.
- **كيف / how:** DNA.measureProduct samples clamp(2.5*D,12,90) frames; DNA.compare weights rhythm 0.30 (log shot-length ratio), light 0.15, contrast 0.15, colour 0.15, camera 0.25 (zoom share); DNA.fix re-grades, retimes cuts (MON.retime) or replans camera.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:1412` · `app/public/js/10_studio.js:1426` · `app/public/js/10_studio.js:1439`

#### QA-142 · تقدير التكلفة وحد الصرف · Cost estimate and spending limit · 📦 بأمر تثبيت
- **ماذا / what:** Estimates a plan's cost before running it and tracks actual cost per key; asks before plans above the limit.
- **كيف / how:** COST.DEF USD per 1M tokens in/out: opus/fable 5/25, sonnet 3/15, haiku 1/5, gemini-4-argon 2.5/15, 3.1-pro 2/12, 3.8-flash 0.5/3, 3.6-flash 0.3/2.5, flash-lite 0.1/0.4, transcribe 0.5/2, tts 0.5/10, image $0.039 each, Veo $0.15/s, Lyria $0.06; typical tokens per tool (code 7000/6000 ...); default limit $0.50.
- **أرقام / params:** limit $0.50 default
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:3959` · `app/public/js/10_studio.js:3968` · `app/public/js/10_studio.js:3994`

#### QA-143 · نصايح الكوتش بضغطة · Coach tips with one-tap fixes (no AI) · 📦 بأمر تثبيت
- **ماذا / what:** Local checks every 1.5 s suggest the next step and fix problems with one tap.
- **كيف / how:** coachTips(): no captions -> transcribe/sync; music but cuts off-beat -> pattern; cuts mid-sentence -> speech sync; dead sync mode; overlays clashing with caption row; title vs captions in first 3 s; no hook in first 0.45 s -> make title from first starred/number line; lines > 8 words -> split; caption size < 6; no stroke on video; loud undocked music; crop > 40% -> fit; leftover demo text; plain gradient on audio -> pattern; broken code scenes; then render / post.
- **أرقام / params:** max 4 tips; refresh 1.5 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:2751`

#### QA-144 · بوابة التسليم · Delivery gate · 📦 بأمر تثبيت
- **ماذا / what:** A pre-publish checklist with pass/warn/fail lines and a verdict.
- **كيف / how:** deliveryGate(): duration < 3 s fail, > 90 s on 9:16 warn; captions present; size >= 6; lines <= 8 words; >= 0.18 s per word reading speed; bottom elements vs caption on 9:16; code scene errors; items after the end; pending stickers; main peak >= 0.99 clipping / < 0.25 quiet; music ducking; beat sync without beats; dark text without stroke; shortest shot < 0.35 s = flicker fail; median shot > 2.8 s warn (top films 1.1-2.8 s); first motion after 0.45 s warn; < 0.25 s per word warn (readable 0.4); …
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:2110`

#### QA-145 · صفحة فحص الربط · Integration health check page · 📦 بأمر تثبيت
- **ماذا / what:** A safe status page checks configuration and then makes read-only requests to test reachability/auth of Gemini and Claude; the agent can also run a timed diagnosis of every route.
- **كيف / how:** /integration-status.html + /api/basma-health (never returns credentials); AIR.diagnose: server, streaming test (5 chunks 0.7 s apart), one-word answer per model (45 s timeout), a realistic 4 KB JSON script job.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/integration-status.html` · `app/vite.config.ts:63` · `app/public/js/10_studio.js:2389`

#### QA-146 · عرض المرجع والأصل والمنتج · Multi-monitor compare view · 📦 بأمر تثبيت
- **ماذا / what:** Product, original and reference monitors can be shown one at a time or side by side, with the reference video playing in sync.
- **كيف / how:** viewTabs product/orig/ref/all; drawOrig contain-fit at half resolution.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:843` · `app/index.html:184`

#### QA-147 · رندر تجريبي سريع · Smoke render mode · 📦 بأمر تثبيت
- **ماذا / what:** Short low-res test render to prove the pipeline before approval.
- **كيف / how:** python scripts/render.py --smoke --seconds 2 --height 360 --fps 10 --output output/smoke.mp4; duration=min(storyboard, seconds or 2, 12).
- **أرقام / params:** default 2 s, cap 12 s, 360p, 10 fps
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `fastify-motion-bro/scripts/render.py:27` · `fastify-motion-bro/docs/CANVAS-STUDIO.md:4`

#### QA-148 · أمر: فحص ثابت · CLI: lint · 📦 بأمر تثبيت
- **ماذا / what:** Static linter (~150 rule codes) over composition HTML/CSS/JS.
- **كيف / how:** npx hyperframes lint ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** Static linter (~150 rule codes) over composition HTML/CSS/JS.
- **تثبيت / install:** `npx hyperframes lint`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### QA-149 · أمر: فحص بصري · CLI: check · 📦 بأمر تثبيت
- **ماذا / what:** Browser audit at 9 midpoint samples (+--at-transitions): overflow tolerance 2px, WCAG contrast, --caption-zone band gate, --frame-check, --snapshots crops.
- **كيف / how:** npx hyperframes check ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** Browser audit at 9 midpoint samples (+--at-transitions): overflow tolerance 2px, WCAG contrast, --caption-zone band gate, --frame-check, --snapshots crops.
- **تثبيت / install:** `npx hyperframes check`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### QA-150 · أمر: لقطات · CLI: snapshot · 📦 بأمر تثبيت
- **ماذا / what:** PNG frames at --at times or --frames 5; --zoom selector crop at scale 3; --against reference video side-by-side.
- **كيف / how:** npx hyperframes snapshot ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** PNG frames at --at times or --frames 5; --zoom selector crop at scale 3; --against reference video side-by-side.
- **تثبيت / install:** `npx hyperframes snapshot`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### QA-151 · أمر: إطارات مفتاحية · CLI: keyframes · 📦 بأمر تثبيت
- **ماذا / what:** Inspect tween keyframes over time.
- **كيف / how:** npx hyperframes keyframes ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** Inspect tween keyframes over time.
- **تثبيت / install:** `npx hyperframes keyframes`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### QA-152 · أمر: مقارنة · CLI: compare / grade-compare · 📦 بأمر تثبيت
- **ماذا / what:** Compare renders; grade-compare tiles up to 16 grades 4 per row into grade-compare.png.
- **كيف / how:** npx hyperframes compare ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** Compare renders; grade-compare tiles up to 16 grades 4 per row into grade-compare.png.
- **تثبيت / install:** `npx hyperframes compare`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### QA-153 · قواعد الأداء · Performance rules · 📦 بأمر تثبيت
- **ماذا / what:** Fewer big backdrop-filter/blur layers; draft quality for review only.
- **كيف / how:** Lint composition_heavy_overlay_count_high; render -q draft.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/performance.mdx`

#### QA-154 · حلقة المراجعة: خطة ثم رسومات ثم بناء ثم معاينة · Review loop: plan -> sketch sheet -> build -> final look · 📦 بأمر تثبيت
- **ماذا / what:** Fidelity is earned pass by pass: frame table proposal in chat, static styled sketches as cells of storyboard.html, building that dresses (never redraws) confirmed layouts, then Studio preview before render; autonomous mode keeps exactly one question before render.
- **كيف / how:** review-loop.md §1-4; STORYBOARD.md frame statuses outline -> built -> animated; after approval offer `recipe.mjs freeze --name <name>`.
- **أرقام / params:** statuses: outline/built/animated
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/review-loop.md` · `kosif-one/vendor/hyperframes/skills/hyperframes/references/storyboard-format.md`

#### QA-155 · تثبيت وترقية إصدار الأداة في المشروع · Pin and upgrade the project CLI · 📦 بأمر تثبيت
- **ماذا / what:** Projects pin hyperframes@<version>; before render-affecting commands probe and, if behind, upgrade then verify with check; name old/new version in the summary, revert on failure.
- **كيف / how:** `npx hyperframes@latest upgrade --project . --check` then `npx hyperframes@latest upgrade --project .` then `npx hyperframes check`.
- **تثبيت / install:** `npx hyperframes@latest upgrade --project`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/SKILL.md`

#### QA-156 · محظورات الحتمية · Determinism bans · 📦 بأمر تثبيت
- **ماذا / what:** Every frame must be a pure function of time: no Date.now/performance.now, no unseeded Math.random (use seeded PRNG), no render-time network, no hover/scroll/input, repeat:-1 only under finite root duration, no tl.play() for render motion.
- **كيف / how:** determinism-rules.md; lint rules gsap_infinite_repeat, gsap_timeline_registered_before_async_build.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/determinism-rules.md`

#### QA-157 · أخطاء الفحص الأولى الشائعة · Lint first-pass gotchas · 📦 بأمر تثبيت
- **ماذا / what:** Known lint errors: gsap_css_transform_conflict, media_crossorigin_breaks_preview, video_nested_in_timed_element, media_missing_id (silent render), gsap_animates_clip_element, font_family_without_font_face, standalone_composition_wrapped_in_template, subcomposition_root_styled_by_class.
- **كيف / how:** Use fromTo instead of CSS initial transforms; no crossorigin on media; id on every <audio>; @font-face to local files; clear lint errors before trusting check's layout/contrast numbers (they report 0 samples otherwise).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/SKILL.md`

#### QA-158 · أمر فحص الخط الزمني · Timeline inspection command · 📦 بأمر تثبيت
- **ماذا / what:** Lists every track and clip (starts, ends, what plays) of a project.
- **كيف / how:** `npx hyperframes timeline [--json]`.
- **تثبيت / install:** `npx hyperframes timeline [--json]``
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/tracks-and-clips.md` · `kosif-one/vendor/hyperframes/skills/hyperframes/SKILL.md`

#### QA-159 · انتقالات CSS محظورة · Banned CSS transitions · 📦 بأمر تثبيت
- **ماذا / what:** Do not use star iris (polygon interpolation broken), tilt-shift, lens flare (visible shape), hinge/door; glitch overlays must not use multiply blend; light leaks >2400 px.
- **كيف / how:** transitions/catalog.md hard rules.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/catalog.md`

#### QA-160 · سكربت خريطة الحركة للتدقيق · Animation map audit script · 📦 بأمر تثبيت
- **ماذا / what:** Enumerates every GSAP tween on window.__timelines, samples bounding boxes, flags dead zones, stagger inconsistency and lifecycle problems into animation-map.json.
- **كيف / how:** node <skill>/scripts/animation-map.mjs <comp-dir> --out <comp-dir>/.hyperframes/anim-map.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/scripts/animation-map.mjs` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/scripts/animation-map.test.mjs` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/scripts/animation-map-sampling.test.mjs`

#### QA-161 · أدوات تشخيص الحركة · Keyframe diagnostics CLI (keyframes / --shot / --ghost / strip) · 📦 بأمر تثبيت
- **ماذا / what:** Surfaces targets, explicit stops, paths, traces and composed motion; --shot renders onion-skin ghosts of a selector; --layout strip shows in-place motion; --ghost covers canvas/WebGL; snapshot --at proves final lockups.
- **كيف / how:** `npx hyperframes keyframes . [--json] [--runtime all] [--selector S --shot f.png --samples n] [--layout strip --from t0 --to t1] [--ghost --angle a]`; read flat/keyframes/motionPath/trace labels; even ghost spacing = constant speed.
- **تثبيت / install:** `npx hyperframes keyframes`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/SKILL.md` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/keyframes.ts`

#### QA-162 · التحقق من الالتزام بالتصميم · Design adherence verification · 📦 بأمر تثبيت
- **ماذا / what:** Post-authoring check of colors, type, corners, spacing and depth against the spec.
- **كيف / how:** references/design-adherence.md.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/design-adherence.md`

#### QA-163 · تقرير التباين من الإطارات · Contrast report from rendered frames · 📦 بأمر تثبيت
- **ماذا / what:** Inspects WCAG contrast warnings in rendered frames.
- **كيف / how:** node <skill>/scripts/contrast-report.mjs.
- **أرقام / params:** WCAG AA
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/scripts/contrast-report.mjs` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/contrast-fg.test.ts`

#### QA-164 · فحص البنية الثابت · Lint (static) gate · 📦 بأمر تثبيت
- **ماذا / what:** Static HTML structure check with named rule ids.
- **كيف / how:** npx hyperframes lint [dir] [--verbose] [--json].
- **تثبيت / install:** `npx hyperframes lint [dir] [--verbose] [--json]`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/lint-validate-inspect.md` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/lint.ts`

#### QA-165 · الفحص في المتصفح: الأخطاء والتخطيط والحركة والتباين · Check (browser gate: runtime, layout, motion, WCAG contrast) · 📦 بأمر تثبيت
- **ماذا / what:** One headless browser session and seek pass auditing runtime errors, failed requests, layout overflow, *.motion.json motion assertions and WCAG AA contrast; persistent findings gate the exit code.
- **كيف / how:** npx hyperframes check [--json] [--snapshots] [--samples 15] [--at 1.5,4,7.25] [--at-transitions] [--tolerance 4] [--no-contrast] [--strict].
- **أرقام / params:** default samples 9; overflow tolerance 2 px; timeouts 3000/10000 ms
- **تثبيت / install:** `npx hyperframes check [--json] [--snapshots] [--samples 15] [--at 1`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/lint-validate-inspect.md` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/check.ts`

#### QA-166 · تأكيدات الحركة الجانبية · Motion sidecar assertions (*.motion.json) · 📦 بأمر تثبيت
- **ماذا / what:** State motion intent next to a composition (entrances firing under seek, stagger order, in-frame, liveness) so `check` verifies it automatically; closest automated proxy for watching the MP4.
- **كيف / how:** Drop <name>.motion.json beside the html; check discovers it.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/lint-validate-inspect.md`

#### QA-167 · لقطات ثابتة لورقة الاتصال · Snapshot contact sheets · 📦 بأمر تثبيت
- **ماذا / what:** Render still frames at chosen timestamps to inspect mounts, text and final lockups.
- **كيف / how:** npx hyperframes snapshot --at t1,t2,t3.
- **تثبيت / install:** `npx hyperframes snapshot --at t1,t2,t3`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/SKILL.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/lint-validate-inspect.md`

#### QA-168 · سطر تشخيص التصيير · Render diagnostics line (capture path) · 📦 بأمر تثبيت
- **ماذا / what:** After render read the second summary line: beginframe vs screenshot capture, GPU mode, stage timings (compile/setup/capture/encode); screenshot + software GPU on Linux is the slow path.
- **كيف / how:** Inspect stdout after render; ffprobe duration/streams.
- **أرقام / params:** e.g. 'beginframe capture - software gpu - compile 0.7s ...'
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/SKILL.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-core/SKILL.md`

#### QA-169 · مقارنة النسخ ودرجات اللون · Compare variants and color grades · 📦 بأمر تثبيت
- **ماذا / what:** Side-by-side comparison of projects/variants and of color grades.
- **كيف / how:** npx hyperframes compare <a> <b> ...; npx hyperframes grade-compare ...
- **تثبيت / install:** `npx hyperframes compare <a> <b>`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/compare-and-batch.md` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/grade-compare.ts`

#### QA-170 · سجل المشروع والتراجع لكل دورة · Project history undo per agent turn · 📦 بأمر تثبيت
- **ماذا / what:** Every write is an undoable entry; agents bracket turns and undo their newest turn without touching the person's edits.
- **كيف / how:** npx hyperframes history begin --who <name> --label '...'; history --since mine; history undo --who <name>; history end.
- **أرقام / params:** turn auto-ends after 10 min idle
- **تثبيت / install:** `npx hyperframes history begin --who <name> --label '`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/SKILL.md` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/history.ts`

#### QA-171 · معيار جودة المكونات والمساهمة · Component quality bar and contribution · 📦 بأمر تثبيت
- **ماذا / what:** Rules for authoring a new block/component upstream: demo HTML pattern, placeholder material, quality bar, templates, discovery metadata.
- **كيف / how:** hyperframes-registry/references/component-quality-bar.md, contributing.md, templates.md, placeholder-material.md.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-registry/references/component-quality-bar.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-registry/references/contributing.md`

#### QA-172 · فحص جودة النص المفرغ وتنظيفه · Transcript quality check and cleaning · 📦 بأمر تثبيت
- **ماذا / what:** Mandatory transcript QC (hallucinations, missing words, timestamps), automatic retry with bigger model, cleaning, importing external API transcripts (SRT/VTT/JSON).
- **كيف / how:** audio/references/captions/transcript-handling.md.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/audio/references/captions/transcript-handling.md`

#### QA-173 · بوابة قرار الترجمة · Caption decision gate (refuse bad clips) · 📦 بأمر تثبيت
- **ماذا / what:** Refuse or split: multiple speakers or hard cuts, no human subject, <3 s or no speech (Whisper hallucinates 'Thank you.'), burned-in captions (check 1 fps contact sheet), garbage transcript (retry WHISPER_MODEL=medium once), busy handheld motion.
- **كيف / how:** ffprobe; ffmpeg frames at 20/50/80%; ffmpeg -i in.mp4 -vf 'fps=1,scale=160:-1,tile=10x5' sheet.png.
- **أرقام / params:** probe at 20/50/80%
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/SKILL.md`

#### QA-174 · معاينة سريعة للإطارات المركبة · Fast composite preview frames (no render) · 📦 بأمر تثبيت
- **ماذا / what:** Approximate final composite frames in ~2 s/frame without rendering, for visual QA before paying for a render.
- **كيف / how:** node scripts/preview-frames.cjs <project> [t1 t2 ...].
- **أرقام / params:** ~2 s/frame
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/preview-frames.cjs` · `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/preview-frames.test.mjs`

#### QA-175 · بوابات فحص الترجمة · Caption render gates (timing / occlusion / overflow / hand-off) · 📦 بأمر تثبيت
- **ماذا / what:** Gates before final: check-timing, check-occlusion (Chromium DOM rects vs matte alpha per word/cap), check-overflow (frame edge), check-rail-climax (rail-to-climax hand-off); measure-layout seeks the GSAP timeline and measures bboxes.
- **كيف / how:** node scripts/check-timing.cjs <p> [--strict]; check-occlusion.cjs <p> [--word-fail F --cap-fail F]; check-overflow.cjs; check-rail-climax.cjs; measure-layout.cjs.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/check-timing.cjs` · `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/check-occlusion.cjs` · `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/check-overflow.cjs`

#### QA-176 · أخطاء الترجمة المعروفة · Caption failure modes (learned) · 📦 بأمر تثبيت
- **ماذا / what:** CoreML corrupts face alpha; aspect/channel-stride garbage alpha; flex-stacked captions push into gesture zone; letterSpacing animation reflow jumps; double fade pop; overlay blend vanishes in dark, screen washes on bright; fps mismatch between bg and matte; WebM alpha flaky in Chromium; centered cro…
- **كيف / how:** references/failure-modes.md + anti-patterns.md.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/references/failure-modes.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/references/anti-patterns.md`

#### QA-177 · بوابة دقة حركة فيجما · Figma motion fidelity gate (motion-energy PSNR) · 📦 بأمر تثبيت
- **ماذا / what:** Compares the HyperFrames render against Figma's export_video using frame-difference deltas so static font/raster divergence cancels and only trajectories, timing and easing are scored.
- **كيف / how:** node figma/scripts/verify-motion.mjs --reference figma-export.mp4 --render out.mp4 [--crop WxH+X+Y] [--interval 0.2] [--min-motion-psnr 15].
- **أرقام / params:** threshold 15 dB; faithful min 20.3 / mean 27.7 dB vs diverging min 5.0 / mean 23.1 dB
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/figma/scripts/verify-motion.mjs`

#### QA-178 · بوابة الإطارات المفتاحية · Keyframe gate frames · 📦 بأمر تثبيت
- **ماذا / what:** Render selected stills before any video render (the 8-second gate).
- **كيف / how:** python scripts/kmotion.py frames projects/NAME --times 1,4,7
- **أرقام / params:** retries stalled grabs
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:88` · `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### QA-179 · مفاتيح إخفاء العناصر لتصحيح المشهد · Debug visibility toggles for heavy 3D scenes · 📦 بأمر تثبيت
- **ماذا / what:** A window.__dbg object hides water, pads, petals, grass, reeds, pebbles, rim, ground, koi or the whole post stack, isolating performance or artefact problems.
- **كيف / how:** Set window.__dbg={nowater:1, nopost:1, nokoi:1,…} before build(); render bypasses makeFrameLoop when nopost; webglcontextlost/restored listeners log loudly.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:118` · `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/index.html:35`

#### QA-180 · بناء المحاكاة وبوابة المقارنة · Mimic build + compare gate · 📦 بأمر تثبيت
- **ماذا / what:** Builds mimic.timeline.json -> film, then compares duration, boundaries, audio correlation.
- **كيف / how:** mimic build PROJECT/study --out FINAL.mp4 -> compare.json, compare.jpg
- **أرقام / params:** duration ±2 frames; boundaries ±2 frames same type; audio corr >=0.95, lag <=40 ms
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/mimic.md`

#### QA-181 · فخاخ المحاكاة · Mimic traps rules · 📦 بأمر تثبيت
- **ماذا / what:** Known pitfalls: truncated downloads, text fades mistaken for dissolves (ignore_mask), exposure fades as suspects, dark dip thresholds, 720p upscale.
- **كيف / how:** ffmpeg -v error -xerror -i CLIP -f null - ; dip needs bright side >=30 and near-black <16; settb=1/90000 after concat
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/mimic.md`

#### QA-182 · معاينة وفحص القراءة · Preview + readability check · 📦 بأمر تثبيت
- **ماذا / what:** Draft preview and readability (~0.3 s/word, hook in 2 s).
- **كيف / how:** kmotion preview PROJECT; kmotion readable FILE; kmotion sheet
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/operating-manual.md`

#### QA-183 · مراجعة المستخدم · Review site markup · 📦 بأمر تثبيت
- **ماذا / what:** User marks up film on local review page.
- **كيف / how:** kmotion review init; http://127.0.0.1:8766/review/NAME/; feedback; apply
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/operating-manual.md` · `100-superskills/skills/kosif-montage-motion/scripts/review.py` · `100-superskills/skills/kosif-montage-motion/tests/test_review.py`

#### QA-184 · التصيير النهائي والبوابة · Final render + inspect gate · 📦 بأمر تثبيت
- **ماذا / what:** Lossless capture CRF 16, poster frame 0; inspect H.264 yuv420p, -14±1.5 LUFS, TP<=-1, no black/frozen.
- **كيف / how:** kmotion final PROJECT [--blur 4]; kmotion inspect FILM; kmotion poster FILM --bake
- **أرقام / params:** CRF 16
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/operating-manual.md` · `100-superskills/skills/kosif-montage-motion/scripts/qa.py`

#### QA-185 · تحليل الفيديو · Video analyze breakdown · 📦 بأمر تثبيت
- **ماذا / what:** Specs, beats<=3 s, palette hex, motion energy, pan, entries, LUFS, BPM, onsets, stills.
- **كيف / how:** kmotion analyze VIDEO --out NAME.breakdown [--transcribe]
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/video-breakdown.md` · `100-superskills/skills/kosif-montage-motion/scripts/analyze.py` · `100-superskills/skills/kosif-montage-motion/tests/test_analyze.py`

#### QA-186 · مكتبة الأساليب · Batch style library · 📦 بأمر تثبيت
- **ماذا / what:** Measure many references to library.json/csv for house style.
- **كيف / how:** kmotion analyze --batch FOLDER --out style-library
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/video-breakdown.md`

#### QA-187 · رسم الموجة والطيف · Waveform + spectrum plot · 📦 بأمر تثبيت
- **ماذا / what:** Saves a PNG with the waveform and a log-frequency spectrum of the file.
- **كيف / how:** audio_analyze.py FILE --plot out.png (matplotlib Agg).
- **أرقام / params:** 10×6 in, 120 dpi
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/audio_analyze.py:270`

#### QA-188 · شريط تقدم حقيقي من FFmpeg · Live render progress from ffmpeg -progress · 📦 بأمر تثبيت
- **ماذا / what:** Shows honest percent progress of a render by parsing ffmpeg's machine-readable progress stream and writing an atomic status JSON that a small window polls.
- **كيف / how:** Run ffmpeg with -progress pipe:1 -nostats, read stdout lines out_time=HH:MM:SS.xx, convert to seconds, map into a stage share (start..end %) of the whole job; write status via tmp file + os.replace; a Tkinter window polls every 550-650 ms, shows stage text in Arabic, percent and a bar, turns green on done / red on error and enables 'open video'; heartbeat file proves the window is alive.
- **أرقام / params:** v1 window 760x385 bg #0d1525 bar #d5aa62 title #e0b778 (Segoe UI 18 bold, Dubai 22 bold); v2 560x215 ttk 'clam' trough #273248 bar #76e4d6 thickness 16, bg #10182a; poll 550/650 ms
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:31-33` · `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:64-81` · `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:172-212`

#### QA-189 · تتبع أخطاء الشيدر بالعزل · Shader isolation debugging · 📦 بأمر تثبيت
- **ماذا / what:** Find which object or material causes an artifact by rendering the same frame with one material type (or one ShaderMaterial) hidden at a time and comparing screenshots; also list meshes with distance to camera.
- **كيف / how:** Playwright: window.__S.S5.update(15); traverse scene, toggle o.visible by material.type or by index among ShaderMaterials, window.render(15), screenshot qa/s5_hide_*.png.
- **أرقام / params:** t = 15.0 s test frame
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/dbg.py` · `kosif-one/projects/egypt-2120-animation/dbg2.py`

#### QA-190 · دراسة الفيديو المرجعي · Reference film study (boundaries, looks, text zones) · 📦 بأمر تثبيت
- **ماذا / what:** Measures a reference reel automatically: cut/transition boundaries with type and confidence, per-shot look statistics, text bounding boxes and colour, text appear/disappear events, global fades and audio loudness.
- **كيف / how:** kosif-mimic study writes mimic.json: boundaries[{frame,start,dur,type,conf}], shots[{start,end,look{mean,std,contrast,sat,motion,hist512},text_zone{bbox,color}}], text_events, audio lufs, then a todo list for the human/agent.
- **أرقام / params:** 10 boundaries all fadeblack conf .9; shot contrast 50-86, saturation .17-.55, motion 1.9-7.0; audio AAC 44.1 kHz -12.75 LUFS
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/mimic-jumuah/study/mimic.json`

#### QA-191 · فحص المطابقة بالإطارات والصوت · Mimic comparison QA (frames + audio correlation) · 📦 بأمر تثبيت
- **ماذا / what:** Proves a rebuilt film matches its reference: every boundary found within 2 frames with the same transition type, no extra cuts, duration within 2 frames and identical audio by cross-correlation; a comparison sheet is saved.
- **كيف / how:** mimic compare -> compare.json checks {duration_within_2_frames, every_boundary_found, boundaries_within_2_frames, transition_types_match, no_extra_boundaries, audio_same} and pass.
- **أرقام / params:** mean offset 0.3 frames; audio corr .9937, lag -3 ms; duration offset 2 frames; pass true
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/mimic-jumuah/study/compare.json`

#### QA-192 · مشغل معاينة داخل المتصفح · Built-in browser preview player · 📦 بأمر تثبيت
- **ماذا / what:** Opening a composition in a normal browser shows a fitted preview with play/pause, scrub bar, time readout and space-bar toggle, synced to its audio/video; hidden from renderers.
- **كيف / how:** player(rootId,duration) (whatsapp copy of the kit): skipped when navigator.webdriver, window.__hf or ?render; clock follows a playing media element else wall clock; 48 px bar #14161a, button #E7B65A.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:493-533`

#### QA-193 · بوابة الإطارات المفتاحية · Key frames gate · 📦 بأمر تثبيت
- **ماذا / what:** Renders a handful of key frames to look at before any full render.
- **كيف / how:** python motion.py frames PROJECT --times 0.5,2,4,6,8 (builds the page once and seeks each time).
- **أرقام / params:** default times 0.5,2,4,6,8
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/motion.py:472`

#### QA-194 · قياس سرعة الحركة على الشاشة · On-screen speed gate (optical flow) · 📦 بأمر تثبيت
- **ماذا / what:** Measures px/frame by optical flow and says whether a move is clean, needs motion blur, or must be redesigned.
- **كيف / how:** python motion.py speed FILM.mp4.
- **أرقام / params:** peak <= 12 px/f clean; <= 80 blur it (--blur up to 8); > 80 redesign (cut, match cut, mask wipe); text being read <= 3 px/f
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/qa.py:283` · `kosif-one/tools/kosif-studio/motion/references/craft-numbers.md`

#### QA-195 · حكم الواقعية للصور · Realism judge for still renders · 📦 بأمر تثبيت
- **ماذا / what:** Measures flat fills, one-pixel edges, distinct colours and tonal range against calibrated thresholds, then lets Jev pick the verbal verdict.
- **كيف / how:** python judge.py out/x.png [--prompt ...] [--no-jev].
- **أرقام / params:** flat_share: photos 0.11-0.23, shaded scenes < 0.02, flat cartoon 0.76; target distinct colours > 1200, flat < 12%
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/judge.py` · `kosif-one/tools/kosif-studio/references/drawing-guide.md`

#### QA-196 · تحليل حدود اللقطات والمظهر · Shot boundary and look analysis · 📦 بأمر تثبيت
- **ماذا / what:** Per-frame features detect shot boundaries, per-shot look/motion/keyframes, and a global look (vignette, grain, letterbox, fades).
- **كيف / how:** mm_analyze.detect_boundaries / shot_measures / global_look.
- **أرقام / params:** letterbox = rows near-black in mean and max image; vignette = corner/centre ratio per frame
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_analyze.py`

#### QA-197 · اختبار المحاكاة بفيديو اصطناعي · Synthetic regression harness for mimic · 📦 بأمر تثبيت
- **ماذا / what:** Builds a synthetic reference with known truth (transitions, texts) and scores the analyser's detections.
- **كيف / how:** python tests/make_reference.py ...; python tests/run_synthetic.py REF_DIR WORK_DIR.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/tests/run_synthetic.py` · `kosif-one/tools/kosif-mimic/tests/make_reference.py`

#### QA-198 · محلل الفيديو المرجعي · Reference video analyser · 📦 بأمر تثبيت
- **ماذا / what:** Per-frame features -> shot boundaries -> transition kind + progress curve by re-synthesis -> per-shot look/motion -> global look (vignette, grain, letterbox, fades) -> review sheets; original audio copied untouched.
- **كيف / how:** python -c "import mm_analyze;mm_analyze.analyze('REF.mp4','work')" -> spec.json, analysis.md, sheets/
- **أرقام / params:** analysis 96 px short side; 360 px for motion
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-mimic/scripts/mm_analyze.py:1` · `100-superskills/skills/kosif-mimic/SKILL.md`

#### QA-199 · اختبار المحاكاة الاصطناعي · Synthetic regression for mimic · 📦 بأمر تثبيت
- **ماذا / what:** Generates a synthetic reference with truth.json and scores analysis + font ranking.
- **كيف / how:** python3 tests/make_reference.py; tests/run_synthetic.py REF_DIR WORK_DIR [--build]
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-mimic/tests/run_synthetic.py`

#### QA-200 · حكم الواقعية · Realism judge metric · 📦 بأمر تثبيت
- **ماذا / what:** Measures flat-area %, hard-edge %, distinct colours, value range to classify painted-realistic vs flat cartoon; optional Jev verdict.
- **كيف / how:** python3 judge.py x.png --prompt ... [--no-jev]
- **أرقام / params:** guide: colours>1200, flat<12%, edges<35%, range>150
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/scripts/judge.py` · `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md`

#### QA-201 · مشغّل المعاينة · In-browser preview player · 📦 بأمر تثبيت
- **ماذا / what:** When opened in a normal browser (not under a renderer) the composition plays with audio, scales to window, play/pause + scrub bar + space key.
- **كيف / how:** Automatic via MOTION.shim; skipped when navigator.webdriver, ?render or HyperFrames.
- **أرقام / params:** bar 48 px #14161a, button #E7B65A, media-element clock
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:496`

#### QA-202 · اللمسات الأخيرة حسب وضوح الفرق · Final-touch passes ordered by visibility (Delta E bands) · 📦 بأمر تثبيت
- **ماذا / what:** Remaining differences are painted most-visible first, with time proportional to visibility, using CIE76 Delta E plus an alpha term.
- **كيف / how:** exact.delta_e(); bands: dE>=12 'visible details' sweep weight 1.2; 4..12 'light corrections' sparkle 0.4; <4 'invisible differences' sparkle 0.12.
- **أرقام / params:** Delta E = |Lab1-Lab2| + |alpha1-alpha2|/2.55
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/exact.py:59` · `kosif-studio/exact.py:193` · `kosif-studio/tests/test_studio.py:271`

#### QA-203 · خطط رسم مقاسة يختار بينها حَكَم · Measured painting plans chosen by a judge · 📦 بأمر تثبيت
- **ماذا / what:** For photos, four block-in/refine plans are measured on a 240 px copy (first-impression dE, refined dE, % pixels visibly off, step count) and the Jev service is asked twice with options reversed; a deterministic rule decides offline.
- **كيف / how:** exact.candidates() + exact.choose_plan(); rule = min(visibly_off_pct + 0.4*steps); KOSIF_JEV_URL=off forces the rule; logos skip (keep own colours).
- **أرقام / params:** PLANS A=(6,32) B=(10,64) C=(16,96) D=(24,128) colours/tones; default B; visible = dE>10; ~3 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/exact.py:22` · `kosif-studio/exact.py:95` · `kosif-studio/exact.py:124`

#### QA-204 · التحقق من المطابقة التامة · Exact-match verification badge · 📦 بأمر تثبيت
- **ماذا / what:** After drawing an image the canvas is compared with the original pixel by pixel; the window shows a success line with the pixel count or the number of differing pixels, and saves <name>_exact.png.
- **كيف / how:** exact.mismatches(canvas, rgba) counts pixels differing in any of R,G,B,A; Studio.finish writes out/<name>_exact.png.
- **أرقام / params:** 0 differing pixels required
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/exact.py:208` · `kosif-studio/studio.py:612` · `kosif-studio/out/Untitled_exact.png`

#### QA-205 · كود الصورة كبيانات تُقرأ دون تنفيذ · Image code as pure data (read without executing) · 📦 بأمر تثبيت
- **ماذا / what:** A data-only image program (TITLE/SIZE/IMAGE_B64) is read with ast.literal_eval so nothing in the file ever runs, then painted exactly.
- **كيف / how:** studio.image_code(path,title) or --image-code IMG --data-only; runner.read_image_code + run_image_code.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/studio.py:126` · `kosif-studio/runner.py:116` · `kosif-studio/runner.py:177`

#### QA-206 · بوابة الواقعية · Realism gate (judge.py) · 📦 بأمر تثبيت
- **ماذا / what:** Measures a render after removing letterbox bars and pure black/white areas: smooth-gradient share, perfectly flat share, hard one-pixel edge share, distinct colours and tonal range; returns PASS or REVISE with reasons, then optionally asks Jev which description fits the numbers.
- **كيف / how:** python judge.py image.png [--prompt "..."] [--no-jev].
- **أرقام / params:** thresholds: smooth_share >= .12, flat_share <= .30, hard_edge_share <= .55, distinct_colours >= 900 (/8 bins at 200x200), tonal_range >= 150 (p2..p98); calibration: photos flat .11-.23 hard .46-.51; shaded scenes flat < .02 hard .18-.34; flat cartoon flat .76 hard .64
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/judge.py:1` · `kosif-studio/judge.py:33` · `kosif-studio/judge.py:36`

#### QA-207 · حلقة المراجعة بالقياس · Measured review loop for painted scenes · 📦 بأمر تثبيت
- **ماذا / what:** Write quality locks, build back-to-front, render a still, measure with judge.py, inspect 1:1 crops of face/action/main material, fix and repeat 2-4 rounds, then report what worked in numbers.
- **كيف / how:** python studio.py <scene> --render x.png --scale 1 -> python judge.py x.png --prompt ... -> crop review -> revise.
- **أرقام / params:** 2-4 rounds
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/references/drawing-guide.md:82`

#### QA-208 · مجموعة اختبارات الاستوديو · KOSIF Studio regression suite · 📦 بأمر تثبيت
- **ماذا / what:** Unit tests covering renderer holes/even-odd/arcs/gradients/Arabic text, realism and camera ops, reveal orders, SVG import, vectorising, exact redraw, image-to-Python, judge, Jev fallback, HTML frames, drawing films, the runner, edit packages, local edits, AI bridge with a fake CLI, plus motion pipel…
- **كيف / how:** python -m unittest discover -s tests (from kosif-studio).
- **أرقام / params:** 58 tests in tests/test_studio.py (README says 42); browser/ffmpeg tests skip when missing
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/tests/test_studio.py:1`

#### QA-209 · لقطات مراجعة مفتاحية · Key-frame review grabs · 📦 بأمر تثبيت
- **ماذا / what:** Opens the composition once in the studio browser and saves PNG stills at chosen times, retrying stalled grabs and reporting page errors and console warnings.
- **كيف / how:** python motion.py frames PROJECT --times 0.5,2,4,6,8 [--out DIR]
- **أرقام / params:** default times 0.5,2,4,6,8; 4 attempts with 1.5 s × n back-off; timeout 300 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/motion.py:226`

#### QA-210 · سرعة الحركة على الشاشة · On-screen speed by optical flow · 📦 بأمر تثبيت
- **ماذا / what:** Farneback optical flow forward and backward; only consistent pixels count; frame speed is the 99.5th percentile in px/frame at native size, with a verdict.
- **كيف / how:** python motion.py speed FILM.mp4
- **أرقام / params:** ≤12 px/f clean; 12-80 px/f → render --blur min(8, ceil(peak·240/360/3)); >80 px/f redesign as beat cut/match cut/mask wipe; Farneback 0.5,3,15,3,5,1.2
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/qa.py:254` · `kosif-studio/tests/test_studio.py:699`

#### QA-211 · دراسة فيلم مرجعي · Reference film study · 📦 بأمر تثبيت
- **ماذا / what:** Measures a reference's grammar (never its content): cuts, shot lengths, first change, motion energy, palette by area, contact sheet, and writes style_guide.md with fill-in prompts for type, transitions, camera, texture.
- **كيف / how:** python motion.py study REFERENCE.mp4 [--out DIR] → study.json + style_guide.md
- **أرقام / params:** cut threshold max(18, 8×median diff); still <0.5; k-means k=6 on 160 px frames at 1 fps (60k px, seed 7)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/qa.py:357`

#### QA-212 · فحص التسليم · Delivery verification · 📦 بأمر تثبيت
- **ماذا / what:** Checks duration, fps, frame count, audio stream and loudness of the output.
- **كيف / how:** python3 tools/verify_video.py film.mp4 --lufs -14; fill templates/TEST_REPORT.md.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/tools/verify_video.py` · `kosif-tool/templates/TEST_REPORT.md`

#### QA-213 · بوابة الفحص قبل الرندر · hyperframes check gate · 📦 بأمر تثبيت
- **ماذا / what:** Single pre-render gate incl. WCAG contrast (errors) and layout overflow.
- **كيف / how:** npx hyperframes check; fix; optional snapshot.
- **أرقام / params:** --no-contrast skips all
- **تثبيت / install:** `npx hyperframes check`
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/step-4-deliver.md`

#### QA-214 · صورة مفهوم أولاً ثم تنفيذ مطابق · Concept-image first, then faithful build · 🔑 مفتاح/خدمة
- **ماذا / what:** Generate or sketch a concept frame per section/beat, lock it as the spec (colors exact, no added overlays), extract a token system from it, build, then compare concept vs render side by side until they match.
- **كيف / how:** Image generation is an external service (not available here); substitute with an approved storyboard still. Compare with a pixel diff (8x8 hotspot grid) plus human review.
- **أرقام / params:** 1 concept per major section; fidelity bar 10/10
- **الدليل / proof:** `kosif-atlas/skills/1420-frontend-design-skills/3377-openai-frontend-design` · `kosif-atlas/skills/880-superloopy/1941-superloopy-frontend/scripts/visual-diff.mjs`

#### QA-215 · رندر مدفوع بسقف ميزانية · Budget-capped paid render · 🔑 مفتاح/خدمة
- **ماذا / what:** Quote cost, get user go-ahead and cap, dry-run free validation, then one paid render; never raise the cap yourself.
- **كيف / how:** quote -> budget --cap -> render --dry-run -> render --yes.
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3892-music`

#### QA-216 · التحقق من الكلمات المغناة بتحويل الكلام لنص · Sung-lyric verification by speech-to-text · 🔑 مفتاح/خدمة
- **ماذا / what:** Check that every planned line was actually sung by transcribing the render and matching lines in order.
- **كيف / how:** ElevenLabs Scribe (or whisper) on the render; a line passes at 75% of its words; on a miss simplify the line (key word on a strong beat, fewer syllables) and re-render only with user approval; show what was actually sung.
- **أرقام / params:** pass threshold 75% words
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3892-music`

#### QA-217 · دليل الأسلوب وحلقة التوليد والفحص · Theme bible + generate/QA loop for figure sets · 🔑 مفتاح/خدمة
- **ماذا / what:** A shared theme file (palette, typography, style and negative tokens, text limits, model settings) drives every generated panel, and each candidate is QA'd before the next change.
- **كيف / how:** Generate N candidates in parallel, QA (OCR of expected strings, palette compliance, geometry/fonts, visual rubric) in one pass, apply one targeted change, stop at 'ship' or after 3 iterations; 1-3 minutes per image.
- **أرقام / params:** ≤3 iterations
- **الدليل / proof:** `kosif-atlas/skills/2657-figures/10108-ai-full-figure` · `kosif-atlas/skills/2657-figures/10115-transparent-icons`

#### QA-218 · حكم Jev المغلق · Jev closed-set judge · 🔑 مفتاح/خدمة
- **ماذا / what:** Chooses among fixed options (choice, yes/no, score) with order bias removed: asked twice with options reversed; thousands of options pre-ranked by multilingual embeddings in heats of 12.
- **كيف / how:** JEV.ask; letters A-L; Gemini embeddings cached on device, word-overlap fallback; tool jev_ideas ('thousands of ideas + Jev'). Judges only, never acts.
- **أرقام / params:** heats of 12
- **الدليل / proof:** `app/public/js/10_studio.js:4920` · `app/public/js/10_studio.js:4941` · `app/public/js/10_studio.js:5085`

#### QA-219 · ترتيب خطوات الإنتاج وسد الفراغات · Production step ordering + gap filling + auto review · 🔑 مفتاح/خدمة
- **ماذا / what:** Steps always run in a working order; montages get free stock clips when none were uploaded, empty frames get a matching photo before review/render, and Claude reviews new productions automatically.
- **كيف / how:** Q.RANK: inputs 0, stock/analyze_reference 1, transcribe/enhance_audio 2, montage/motion_film/launch_film/template/reels/imitate 3, preset 4, edit/images 5, voice/music 6, camera/smart_captions 7, brand/compare 8, fill_gaps 8.5, review/post/export_fingerprint 9, render/answer 10.
- **الدليل / proof:** `app/public/js/10_studio.js:4618` · `app/public/js/10_studio.js:4631` · `app/public/js/10_studio.js:4668`

#### QA-220 · مراجعة الفريم الحالي · Single-frame director review · 🔑 مفتاح/خدمة
- **ماذا / what:** Claude looks at the current frame and fixes only what is wrong: caption legibility and contrast, faces covered, TikTok/Reels safe zones (bottom 18%, right side), colour harmony, clutter.
- **كيف / how:** btnReview: canvas JPEG q0.82 sent as image to director().
- **الدليل / proof:** `app/public/js/00_editor.js:1491`

#### QA-221 · مطابقة النص مع الكلام · Transcript verification against speech · 🔑 مفتاح/خدمة
- **ماذا / what:** Checks the film's written words against what is actually said before building on them.
- **كيف / how:** AGENT.TOOLS.verify_transcript (needs media).
- **الدليل / proof:** `app/public/js/10_studio.js:3600`

#### QA-222 · سد فراغات المونتاج قبل الريندر · Gap filling before render · 🔑 مفتاح/خدمة
- **ماذا / what:** After a montage or film plan, any empty stretch of the timeline gets a matching photo before review and export.
- **كيف / how:** AGENT.TOOLS.fill_gaps (rank 8.5, auto-appended when a plan builds a montage/launch film).
- **الدليل / proof:** `app/public/js/10_studio.js:4668`

#### QA-223 · فحص الاستهلاك المتبقي · Usage and plan-window check · 🔑 مفتاح/خدمة
- **ماذا / what:** At creation start and milestones the agent reads remaining hosted allowance and reset times; unknown means say unknown.
- **كيف / how:** `npx hyperframes usage --json` at start, after drafting, before rendering.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/SKILL.md`

#### QA-224 · الحكم جيف · Jev order-robust judge · 🔑 مفتاح/خدمة
- **ماذا / what:** Asks the live Jev service to choose between options twice with reversed order and averages; falls back to a deterministic rule offline.
- **كيف / how:** jev_client.choose(...); KOSIF_JEV_URL=off disables.
- **الدليل / proof:** `kosif-one/tools/kosif-studio/jev_client.py`

#### QA-225 · رندر من دافنشي مع تحقق · Resolve render + verify · 🔑 مفتاح/خدمة
- **ماذا / what:** SetCurrentRenderFormatAndCodec, SetRenderSettings, AddRenderJob, StartRendering, GetRenderJobStatus then ffprobe match of size/fps/duration (±1 frame).
- **كيف / how:** resolve_pipeline.py render/verify
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/color-grading-order.md` · `100-superskills/skills/davinci-resolve-pipeline/scripts/resolve_pipeline.py`

#### QA-226 · حَكَم Jev المقاوم للترتيب · Jev order-robust judge client · 🔑 مفتاح/خدمة
- **ماذا / what:** Asks the owner's Jev service to choose between options twice in parallel with the option order reversed, averages the probabilities and flags whether both orders agreed; returns None offline so callers fall back to a rule.
- **كيف / how:** jev_client.choose(question, state, options, timeout=20); KOSIF_JEV_URL overrides or 'off' disables.
- **أرقام / params:** 2 calls; probabilities averaged; stable flag
- **الدليل / proof:** `kosif-studio/jev_client.py:1` · `kosif-studio/jev_client.py:24`

#### QA-227 · مقارنة ثلاثة نماذج · Three-model transition bake-off · 🔑 مفتاح/خدمة
- **ماذا / what:** Test one transition on Kling 3.0, MiniMax H3, Seedance 2.0 before committing.
- **أرقام / params:** ~64 credits
- **الدليل / proof:** `kosif-one/vendor/mcp-higgsfield-landing/PROMPTS.md:100`

#### QA-228 · تعاقب حلقات تشغيل المعاينات في الشبكة · Staggered loop phases for live grids · 👁 شوهد في فيديو
- **ماذا / what:** for grid of video previews, detect internal cuts (scene detection), loop only cut-free windows with a short dissolve at the seam, offset each tile's phase so neighbours never change on the same frame
- **أرقام / params:** 12-frame dissolve seam
- **الدليل / proof:** `style:pm-antonio-kodheli-490109`

#### QA-229 · مقارنة إعادة بناء لقطة بلقطة · Shot-for-shot remake comparison · 👁 شوهد في فيديو
- **ماذا / what:** render remake at same fps/frame count as the reference, then ffmpeg hstack both with labels on a dark frame to prove timing parity
- **أرقام / params:** hstack, pad 10px, labels 16px bold white
- **الدليل / proof:** `style:pm-notdwd-c2037d`

#### QA-230 · إغلاق حلقة بلا تقطيع · Seamless loop closure · 👁 شوهد في فيديو
- **ماذا / what:** ensure final frame equals first frame including cursor position/velocity; verify by diffing frame 0 and last
- **أرقام / params:** pixel diff < 1%
- **الدليل / proof:** `style:pm-twoclipping-5cba86`

#### QA-231 · حلقة النقد ثلاث جولات · Critique loop ≥3 rounds · 📄 موصوف
- **ماذا / what:** Contact sheet 2 fps, phone 360 px, first frame, strip around fast moment, review.md rubric (hook, phone readability, motion, variety, composition, truth, sound sync, identity); fix 3 worst per round.
- **كيف / how:** Apply as defaults while authoring; verify with kmotion measure/speed/sheet
- **أرقام / params:** kmotion sheet FILM
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `kosif-studio/motion/references/craft-numbers.md` · `kosif-studio/motion/references/motion-craft.md` · `kosif-studio/motion/references/hyperframes-authoring.md`

#### QA-232 · قياس إزاحة مزامنة الشفاه · GCC-PHAT lip-sync lag check · 📄 موصوف
- **ماذا / what:** Cross-correlate a generated clip's soundtrack with the reference slice to find the offset; a sharp peak near 0 means lips follow the song.
- **كيف / how:** GCC-PHAT on both signals; no clear peak -> regenerate; clear off-zero peak -> shift baseStart; at 120 BPM a beat is 500ms so confirm peak dominance.
- **أرقام / params:** 120 BPM = 500ms beat
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md`

#### QA-233 · قواعد الأمانة في اللقطات · Honest capture rules · 📄 موصوف
- **ماذا / what:** Never pass generated footage as real capture, no frame interpolation inventing motion, rebuild constant frame rate from real timestamps, mask private info and decode every QR before publishing.
- **كيف / how:** Capture waits ~3s after load; count held frames; recapture rather than minterpolate.
- **أرقام / params:** wait 3s
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/references/DELIVERY.md` · `kosif-atlas/skills/1511-homie/3903-video/SKILL.md`

#### QA-234 · ورقة لقطات للمراجعة · Contact sheet review · 📄 موصوف
- **ماذا / what:** Tile frames every N seconds of the render into one image to review the whole film at a glance, then denser sheets at hook/chorus.
- **كيف / how:** ffmpeg -i film.mp4 -vf "fps=1,scale=480:-1,tile=6x5" sheet.png (every 1s; 0.5s for key sections); plus one frame per sung word onset.
- **أرقام / params:** every 1s / 0.5s
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md` · `kosif-atlas/skills/1511-homie/3903-video/SKILL.md`

#### QA-235 · إطار مرجعي للمقارنة · Golden still regression · 📄 موصوف
- **ماذا / what:** Render and commit a still of a key frame to diff against after changes.
- **كيف / how:** npx remotion still <id> out.png --frame N or Playwright screenshot at t; compare with pixel diff/SSIM.
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/757-remotion/SKILL.md`

#### QA-236 · إخفاء البيانات الحساسة في لقطات الواجهة · Privacy masking for UI footage · 📄 موصوف
- **ماذا / what:** Before publishing UI footage, mask addresses, ports, local URLs, location text, keys, private messages and QR codes; decode every QR in the final; re-cut stills from the masked master.
- **كيف / how:** ffmpeg boxblur/drawbox on tracked regions or mask in the HTML port; use disposable test data during capture.
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/references/DELIVERY.md` · `kosif-atlas/skills/101-video-skills/215-feature-video`

#### QA-237 · فحص التسليم للفيديو · Delivery QA for web/social video · 📄 موصوف
- **ماذا / what:** Check the delivered file, not the command: every frame decodes, H.264 yuv420p, even dimensions, BT.709 tags, faststart, no black/frozen/silent stretches, loudness and true peak, size cap; then watch a contact sheet once end to end.
- **كيف / how:** ffprobe/ffmpeg filters (blackdetect, freezedetect, silencedetect, ebur128) + kosif verify_video.py; contact sheet via ffmpeg tile.
- **أرقام / params:** -14 LUFS integrated; true peak < -1 dBTP; site cap 25 MiB; 30 fps
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/references/DELIVERY.md` · `kosif-atlas/skills/1511-homie/3903-video/scripts/qa.mjs` · `kosif-atlas/skills/166-demo-video/535-demo-video`

#### QA-238 · مراجعة اللقطات الثابتة قبل الرندر · Stills-before-render review · 📄 موصوف
- **ماذا / what:** Before a full export render stills at the first frame, every action, every transition midpoint and the last frame; check readability at phone size and that every scene works as a still.
- **كيف / how:** node tools/render_html.cjs --preview (8-frame sheet) or --start/--duration slices; then full render.
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/217-silent-product-demo` · `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali` · `kosif-atlas/skills/101-video-skills/219-ui-component-clip`

#### QA-239 · بديل الحركة المخففة والإطار الثابت · Reduced-motion and static-frame fallback · 📄 موصوف
- **ماذا / what:** Every animated scene needs a meaningful static state: reduced motion swaps travel/parallax for direct state changes, freezes shaders at a good frame, and keeps all information available.
- **كيف / how:** @media (prefers-reduced-motion: reduce) overrides; gsap.matchMedia conditions; in video, the static frame doubles as thumbnail/poster.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali` · `kosif-atlas/skills/3438-ux-design/14124-top-design` · `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail`

#### QA-240 · لا تخترع الرقم الذي يصنع الخطاف · Never invent the hook statistic · 📄 موصوف
- **ماذا / what:** A data hook is only as good as its source: precise numbers read as researched, round ones as invented; a missing source is left as a visible placeholder rather than fabricated, and data cards always show source and date.
- **كيف / how:** Use a [FILL: source] placeholder in scripts and block render when unresolved; data cards get a third hierarchy level with source/date at ~24 px.
- **الدليل / proof:** `kosif-atlas/skills/2964-pwdev-copy/12448-copy-hooks/SKILL.md` · `kosif-atlas/skills/2976-pwdev-social-media/12589-post-visual/SKILL.md` · `kosif-atlas/skills/2964-pwdev-copy/12454-copy-video/SKILL.md`

#### QA-241 · ترجمة مدمجة وحدود الوميض · Burned captions and photosensitivity limits · 📄 موصوف
- **ماذا / what:** Vertical videos need burned-in captions (most watch muted; required for deaf viewers), on-screen text at least 32 px with high contrast and enough reading time, and no flashing faster than 3 Hz.
- **كيف / how:** Check caption placement inside the safe area; run a luminance-flash check on rendered frames (count large luminance swings per second) and cap overlay flash peaks (one trailer template uses peak 0.35).
- **أرقام / params:** min text 32 px @1080w; flash <3 Hz; flash peak ~0.35
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12592-story-reels/SKILL.md` · `kosif-atlas/skills/2976-pwdev-social-media/12594-video-gen/SKILL.md` · `kosif-atlas/skills/1526-gamegen/4173-game-trailer/SKILL.md`

#### QA-242 · فحص تباين النص فوق الصورة · Text-over-photo contrast check · 📄 موصوف
- **ماذا / what:** Never trust raw contrast of text on photos: add a solid overlay, gradient or box and measure contrast against the brightest region under the text, not the image average.
- **كيف / how:** Compute WCAG contrast with PIL/numpy on the bounding box of each text layer using the max-luminance pixel percentile; require 4.5:1 (3:1 for >=18 pt large text).
- **أرقام / params:** WCAG AA 4.5:1; large text 3:1
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12589-post-visual/SKILL.md` · `kosif-atlas/skills/1567-tonone/4428-form-social/SKILL.md`

#### QA-243 · بوابات وضوح الإعلان الثابت · Static-ad legibility gates · 📄 موصوف
- **ماذا / what:** Paid statics pass a 3-second comprehension test, a 150 px preview legibility test, WCAG AA contrast, and keep text at or below ~20% of the canvas area (logo excluded); one message per asset.
- **كيف / how:** Sum text bounding-box areas / canvas area in the renderer; downscale render to 150 px wide and inspect; split into two assets if two messages are needed.
- **أرقام / params:** text area <=20%; preview 150 px; 3 s test
- **الدليل / proof:** `kosif-atlas/skills/1567-tonone/4428-form-social/SKILL.md`

#### QA-244 · انضباط اختبار الإبداعات · Creative testing discipline · 📄 موصوف
- **ماذا / what:** Test one creative variable at a time (video hook = first 3 s, length, format, offer framing, social proof type...), keep a 10-20% holdout control, require 90% confidence for directional and 95% for major decisions, observe at least 7 days, and name assets platform_audience_variable_variant_date.
- **كيف / how:** Prioritize variables on an impact x effort 2x2; produce hook variants as alternative first scenes of one composition; log a test card per experiment (hypothesis, variants, metrics, significance, learning).
- **أرقام / params:** holdout 10-20%; 90/95% confidence; >=7 days
- **الدليل / proof:** `kosif-atlas/skills/1520-digital-marketing-pro/4019-creative-testing-framework/SKILL.md` · `kosif-atlas/skills/192-marketing-skills/570-ad-creative/SKILL.md`

#### QA-245 · سلم تقييم مشاهد الخطاف · Hook scene scoring rubric · 📄 موصوف
- **ماذا / what:** Score candidate scenes 0-2 on six criteria (12 max): matches the title/thumbnail promise, understandable muted from one still, single focus with empty space for text, visible motion or light change, sparks curiosity (contrast, cut-before-the-end, surprise), representative of the best footage.
- **كيف / how:** Extract mid-clip stills (and 2-s interval stills for motion) with ffmpeg, view them, fill a score table; ties go to the brighter scene; scenes with identifiable bystander faces are excluded unless masked; scoring is a selection aid, not a view prediction.
- **أرقام / params:** 6 criteria x 0-2 = 12; motion via 2 s stills
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/SKILL.md`

#### QA-246 · بوابة فحص الملف المسلّم · Delivered-file QA gate · 📄 موصوف
- **ماذا / what:** Before publishing: every frame decodes, phone-safe encoding, faststart, no black or frozen stretches, loudness and true peak in range, file size under the destination limit (25 MiB in one site), plus a contact sheet where every cell is actually looked at.
- **كيف / how:** ffmpeg -v error -i f -f null - (decode), blackdetect and freezedetect filters, ebur128, ffprobe for moov position/pix_fmt; tile contact sheets with ffmpeg; never call a video good on numbers alone.
- **أرقام / params:** size cap example 25 MiB
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/SKILL.md` · `kosif-atlas/skills/1511-homie/3903-video/references/DELIVERY.md` · `kosif-atlas/skills/1526-gamegen/4173-game-trailer/SKILL.md`

#### QA-247 · مقياس الالتصاق SUCCESs · SUCCESs stickiness score · 📄 موصوف
- **ماذا / what:** Score a message on six traits (Simple, Unexpected, Concrete, Credible, Emotional, Stories) 1-10 each; 50-60 extremely sticky, 35-49 strong, 20-34 forgettable, under 20 will not stick; fix the lowest traits first.
- **كيف / how:** Curiosity tools: question, prediction, mystery (delay the resolution), challenge; convert abstractions to concrete numbers and sensory details ('saves 40%' -> '16 hours a month'); use before/after framing. Apply to the core line of every explainer before animating.
- **أرقام / params:** 6 traits x 1-10; bands 50/35/20
- **الدليل / proof:** `kosif-atlas/skills/3434-sales-influence/14100-made-to-stick/SKILL.md`

#### QA-248 · مراجعة الثمبنيل بست نقاط · Six-check thumbnail review · 📄 موصوف
- **ماذا / what:** Review covers for clicks with reasons: (1) TV 50% test - the top half alone must convey the topic because TV home rows show only the top (apply if TV share >=10% or unknown); (2) works without the title by creating a question or emotion; (3) built from 10-15 references across 5 sources by extracting…
- **كيف / how:** Mask the lower half of the rendered PNG with PIL for the 50% test; deliver a verdict table (good/needs work/problem) with evidence, fix and reason.
- **أرقام / params:** TV share >=10%; 10-15 refs; 5 sources; 5+ text variants
- **الدليل / proof:** `kosif-atlas/skills/1101-akbun-writing/2486-akbun-thumbnail-review/SKILL.md`

#### QA-249 · اختيار ذكي للإطارات لمشاهدة الفيديو · Smart frame selection for watching videos · 📄 موصوف
- **ماذا / what:** Combine scene-change detection, perceptual-hash de-duplication, stratified interval sampling, frames anchored to transcript cues, and denser sampling in transcript windows; batch frames into contact sheets; every frame records whether its time is measured, estimated (interval index, +/- half interva…
- **كيف / how:** ffmpeg select='gt(scene,...)',showinfo for timed scene frames, fps=1/N for intervals, imagehash-like dHash in numpy for dedupe, tile filter for sheets.
- **أرقام / params:** estimated error = interval/2
- **الدليل / proof:** `kosif-atlas/skills/2451-knowledge/9503-video-digest/context/watch-pipeline.md` · `kosif-atlas/skills/2451-knowledge/9503-video-digest/SKILL.md`

#### QA-250 · بحث تغليف نزيه · Honest packaging research · 📄 موصوف
- **ماذا / what:** Compare competitor packaging against each channel's own baseline for similar format and age, flag normalized outliers, separate repeated patterns from one-off anomalies, never compare raw views across unlike channels, and remember impressions, CTR, average view duration and retention are creator-onl…
- **كيف / how:** Label every baseline as an estimate with its window; never copy titles or thumbnails; every promise must be substantiable.
- **الدليل / proof:** `kosif-atlas/skills/2211-majestic-marketing/8297-youtube-packaging/SKILL.md` · `kosif-atlas/skills/2211-majestic-marketing/8297-youtube-packaging/references/data-currentness.md`

#### QA-251 · قائمة فحص قبل اعتماد الموشن · Pre-delivery motion QA checklist · 📄 موصوف
- **ماذا / what:** Before sign-off: Arabic letters stay joined with dots and diacritics visible and the reading order correct; reading time measured on the real text at the target size; each scene has an asset or a 'missing' tag with fallback; no full product spin promised from a single still; data, prices, before/aft…
- **كيف / how:** ffprobe for duration/size/streams; ffmpeg -ss t -frames:v 1 frame grabs viewed with Read; ffmpeg ebur128 for loudness; kosif-tool verify_video.py and templates/TEST_REPORT.md.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/quality-and-editors.md`

#### QA-252 · ضوابط الصدق لكل فئة موشن · Category truth guardrails · 📄 موصوف
- **ماذا / what:** Per-category rules: data pieces need source, unit and period, fair scales and no invented final counter value; product ads separate confirmed features from proposed copy and never infer available colours, discounts or before/after results; social clips carry one message, one opener and one CTA, take…
- **كيف / how:** Insert as acceptance items in the delivery plan; verify numbers against supplied sources before animating them.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-data-infographics.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-product-ads.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-social-clips.md`

#### QA-253 · تراكب شفاف 50/50 لكشف الفروق الدقيقة · Onion-skin overlay for subtle visual diffs · 📄 موصوف
- **ماذا / what:** Blend before and after 50/50 at identical pixel geometry to expose small spacing, alignment or typography changes; it's supplemental evidence kept beside the originals; never stretch or shift one image to align. Works for comparing render v1 vs v2 frames of a motion piece.
- **كيف / how:** PIL Image.blend(a, b, 0.5) (runs here) or ffmpeg blend=all_mode=average; same crop coordinates for close-ups.
- **أرقام / params:** 50% / 50%
- **الدليل / proof:** `kosif-atlas/skills/1530-webcraft/4196-ui-screenshots/SKILL.md`

#### QA-254 · ترتيب استبعاد النسخ المولدة · Elimination order for generated variants · 📄 موصوف
- **ماذا / what:** Judge candidates in order and stop at the first failure: concept fit -> clean space for text -> brand palette -> generation defects (hands, faces, garbled text, mechanical repetition, impossible shadows/reflections/scale) -> set consistency -> technical quality -> taste last. Inspect at full size, l…
- **كيف / how:** Contact sheet + 100% crops via PIL; manifest log.
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12578-asset-curation/SKILL.md`

#### QA-255 · اختبار القوالب بمحتوى متطرف · Content-stress testing of templates · 📄 موصوف
- **ماذا / what:** Test lower thirds, cards and counters with worst-case content: names from 1 to 60+ characters, currencies up to 13 visible characters, counts in billions (abbreviate like 12.4M), German ~30% longer text, Arabic RTL and mixed bidi, emoji and combining marks, missing or wrong-aspect images, empty stat…
- **كيف / how:** Feed a stress JSON into KOSIF scene templates and render contact sheets with Playwright to catch overflow.
- **أرقام / params:** names 1-60+ chars; currency <=13 chars; +30% length
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3847-factor-of-safety-content-stress/SKILL.md`

#### QA-256 · قياس الجهارة والذروة · Loudness / true-peak verification · 📄 موصوف
- **ماذا / what:** Confirm the final file meets the loudness spec instead of trusting the mixer.
- **كيف / how:** ffmpeg -i final.mp4 -af ebur128=peak=true -f null - 2>&1 | tail -12 ; read I (LUFS) and True peak (dBTP)
- **أرقام / params:** pass: I within 1 LU of target, TP ≤ -1 dBTP
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2450-davinciresolve-audio-delivery/SKILL.md` · `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/assembly-and-review.md`

#### QA-257 · تحويل معدل إطارات متغير إلى ثابت · VFR to CFR fix for sync drift · 📄 موصوف
- **ماذا / what:** Phone and screen recordings are often variable frame rate; A/V drifts in editors and filters. Force constant frame rate and resample audio with async.
- **كيف / how:** -vf fps=30 (or -fps_mode cfr -r 30) ; -af aresample=async=1 ; inspect with ffprobe r_frame_rate vs avg_frame_rate
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md`

#### QA-258 · حد أمان الوميض · Flash-safety cap · 📄 موصوف
- **ماذا / what:** Full-screen flashes are capped to avoid photosensitive risk: keep flashes under ~0.35 opacity with soft fades, and never flicker above 3 Hz.
- **كيف / how:** overlay flash peak 0.35 with 12-frame fade; check frame-luma deltas over time
- **أرقام / params:** peak 0.35, 12 f fade, <3 Hz
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/gotchas.md` · `kosif-atlas/skills/2976-pwdev-social-media/12592-story-reels/SKILL.md`

#### QA-259 · حد أدنى لحجم الترجمة · Readable caption size floor · 📄 موصوف
- **ماذا / what:** Measure real glyph height on a still rather than trusting font size numbers. Dialogue/comments ≥5% of frame height (108 px at 4K), keywords/beat titles ≥6% (130 px), numbered/opening titles ≥8% (173 px). Never shrink to fit; shorten or split to 2 lines.
- **كيف / how:** Render one representative caption still, measure glyph box; inside 90% x 90% safe area
- **أرقام / params:** 5% / 6% / 8% of H
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2464-davinciresolve-subtitle-devtalk/SKILL.md`

#### QA-260 · فحص جودة التفريغ · Transcript quality gate · 📄 موصوف
- **ماذا / what:** Read every transcript before using it: music-note tokens, garbled words, looping repeated lines over music, inserted ads; Whisper has no speaker labels; keep verbatim, do not invent.
- **كيف / how:** scan JSON for ♪/�, repeated consecutive lines, implausible words; fix proper nouns against source
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transcript-guide.md` · `kosif-atlas/skills/886-intel/1994-transcribe/SKILL.md`

#### QA-261 · قياس التلوين بالمقاييس · Scope-based grade measurement · 📄 موصوف
- **ماذا / what:** Judge grades numerically on the same frame/output: P10/P50/P95 luma, % pixels ≥99 IRE (bright ≠ clipped; check RGB parade separately), ROI-based chroma radius; exclude letterbox/titles; log 'estimated' when read by eye.
- **كيف / how:** Export graded still -> numpy; or ffmpeg signalstats (YMIN/YLOW/YAVG/YHIGH/YMAX, SATAVG) per frame
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow/references/look-scopes.md`

#### QA-262 · تحديث العناصر بعد إعادة القص · Recut propagation · 📄 موصوف
- **ماذا / what:** When cuts change, pass a change list (file | old start TC | new start TC | frame delta) to captions, graphics and sound; timeline markers do not follow clips, so remove/re-place them; re-run auto-subtitles and transcript diff.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2453-davinciresolve-cut-devtalk/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2465-davinciresolve-subtitle-travelnote/SKILL.md`

#### QA-263 · جدول التحقق من الرندر النهائي · Final render verification table · 📄 موصوف
- **ماذا / what:** Before calling a render done: resolution, fps, frame count (duration×fps within 1 frame), one AAC 48 kHz stereo stream, LUFS/TP, playback of head/middle/tail for missing media or unintended black/silence, source timeline unchanged vs preflight record.
- **كيف / how:** ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels -show_entries format=duration -of json ; blackdetect=d=0.5:pix_th=0.1 ; silencedetect ; ebur128
- **أرقام / params:** ±1 frame
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2450-davinciresolve-audio-delivery/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2466-davinciresolve-youtube-shorts/SKILL.md` · `kosif-atlas/skills/934-oh-my-cassette/2204-cassette-video-edit/SKILL.md`

#### QA-264 · قاعدة المشاهدة مرتين · Watch twice rule · 📄 موصوف
- **ماذا / what:** Numbers cannot judge excitement or readability at phone size: watch every cut once with sound and once muted, at phone scale, before delivery; send contact sheets and the report to the user.
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/assembly-and-review.md` · `kosif-atlas/skills/101-video-skills/214-creator-video/SKILL.md`

#### QA-265 · فحص جودة التفريغ وإعادة المحاولة · Transcript quality gate + retry · 📄 موصوف
- **ماذا / what:** Reject transcripts with music tokens, nonsense or ultra-short word spans; retry with a bigger model, then ask for lyrics/script.
- **كيف / how:** Count ♪ tokens; fail if >20%; flag words with end-start<0.05s; retry medium/large.
- **أرقام / params:** threshold 20%, span <0.05s
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transcript-guide.md`

#### QA-266 · قياس دقة التفريغ وضبط الصمت · ASR WER and endpointing discipline · 📄 موصوف
- **ماذا / what:** Measure word error rate on real representative audio (accents, noise), and tune VAD silence thresholds rather than one fixed value.
- **كيف / how:** jiwer WER on 3-5 sample clips; silence detection via ffmpeg silencedetect.
- **الدليل / proof:** `kosif-atlas/skills/2261-conversational-ai-voice-engineering/8616-speech-recognition-and-synthesis`

#### QA-267 · صورة طيف وموجة للمراجعة · Spectrogram + waveform review image · 📄 موصوف
- **ماذا / what:** Claude can't listen, so render a spectrogram over waveform PNG and look for clicks, aliasing, tails and section structure.
- **كيف / how:** ffmpeg -lavfi showspectrumpic=s=1600x600 and showwavespic; check no energy >16kHz aliasing lines, tails decay to black.
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3901-sound` · `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural/references/mixing-and-loops.md`

#### QA-268 · ترتيب الميكس والفحص · Mix order & listening checks · 📄 موصوف
- **ماذا / what:** Decide hero sound, then clip gain -> EQ -> dynamics; compare without music, without SFX, full mix; check masking, clicks, phase, mono.
- **كيف / how:** ffmpeg volume/equalizer/acompressor; -ac 1 mono check.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound`

#### QA-269 · تنبيه علو المؤثرات القصيرة · Short-SFX loudness caveat · 📄 موصوف
- **ماذا / what:** Integrated LUFS needs 400ms blocks; sub-400ms effects read -70 LUFS — level them by peak/loudest 50ms.
- **أرقام / params:** 400ms
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3901-sound/references/TRAPS.md` · `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural`

#### QA-270 · حفظ الصوت الأصلي بنسخة · Preserve original audio via duplicate · 📄 موصوف
- **ماذا / what:** Duplicate the timeline/file before any audio edit; never overwrite originals; reverse/reverb as derived files.
- **كيف / how:** Work on copies; log source ids.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound` · `kosif-atlas/skills/1096-akbun-editvideo/2450-davinciresolve-audio-delivery`

#### QA-271 · علامات مراجعة للأحكام الذوقية · Review markers for subjective calls · 📄 موصوف
- **ماذا / what:** Leave AUDIO_REVIEW markers with TC, intent, alternative and status; report numbers, ask the user to listen; never claim it 'sounds great'.
- **كيف / how:** Markers/JSON notes.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound` · `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural`

#### QA-272 · فخ إعادة الإسناد في TSL · TSL reassignment pitfall · 📄 موصوف
- **ماذا / what:** Inside If() blocks, reassigning a JS variable is invisible to TSL; use .assign(), property setters or select().
- **كيف / how:** Use node.x.assign(v), buffer.element(i).assign(v), or select(cond,a,b).
- **الدليل / proof:** `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/compute-shaders.md`

#### QA-273 · ميزانية أداء الشيدر · Shader cost budget · 📄 موصوف
- **ماذا / what:** Noise-heavy shaders: cap DPR 2 for objects, ~1.25 full-bleed; pause offscreen; constant loop bounds in GLSL ES 1.0.
- **كيف / how:** For offline render quality, DPR can be raised since realtime is not required.
- **أرقام / params:** ~30 noise evals/pixel
- **الدليل / proof:** `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/SKILL.md` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### QA-274 · قائمة تحقق الريندر الأسود · Blender black-render checklist · 📄 موصوف
- **ماذا / what:** Black Cycles output usually means missing camera, lights or broken material links; assert before render.
- **كيف / how:** assert scene.camera; add Sun/Area; check node links; --factory-startup for CI.
- **الدليل / proof:** `kosif-atlas/skills/228-mas-3d-games/705-blender/SKILL.md`

#### QA-275 · حدود التباين · WCAG contrast floors · 📄 موصوف
- **ماذا / what:** Text contrast minimums double as safe floors for video text.
- **كيف / how:** 4.5:1 normal, 3:1 large/graphics, 7:1 AAA; compute relative luminance in Python before render; #767676 on white ≈4.5:1, #999 ≈2.8:1.
- **أرقام / params:** 4.5/3/7
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3825-legibility-contrast-and-spacing/SKILL.md`

#### QA-276 · احترام تقليل الحركة · Reduced-motion respect · 📄 موصوف
- **ماذا / what:** Keep text legible at rest; avoid rapid repeated flashing.
- **كيف / how:** Final frame of every text beat must be static and readable; no >3 flashes/sec.
- **أرقام / params:** ≤3 flashes/s
- **الدليل / proof:** `kosif-atlas/skills/100-ui-motion/209-kinetic-inflated-hero/SKILL.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/quality-and-editors.md`

#### QA-277 · اختبار ثنائي الاتجاه · Bidi pseudo-locale stress test · 📄 موصوف
- **ماذا / what:** Wrap strings in RLI…PDF or reverse order to flush out direction bugs before final render.
- **كيف / how:** Render a test frame with pseudo strings; also 140% and 200% expansion variants to test box overflow.
- **أرقام / params:** 140%/200%
- **الدليل / proof:** `kosif-atlas/skills/2329-localization-i18n-engineering/8942-localization-qa-and-pseudo-loc/SKILL.md`

#### QA-278 · لا تخترع رموزا · No invented glyphs · 📄 موصوف
- **ماذا / what:** If a glyph is not in the chosen font, use a fallback notation rather than an approximate lookalike.
- **كيف / how:** Check cmap with fonttools before using special symbols (sub/superscripts, math).
- **الدليل / proof:** `kosif-atlas/skills/3259-claude-math/13770-math-unicode/SKILL.md`

#### QA-279 · فحص النقط عند حافة القناع · Mask-edge dot check · 📄 موصوف
- **ماذا / what:** Masks and clipping can cut Arabic dots and harakat that sit above/below the line box.
- **كيف / how:** Pad mask by ≥0.35em vertically for Arabic; inspect frames at reveal midpoints.
- **أرقام / params:** 0.35em
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### QA-280 · التحقق من اللوك بالمقاييس · Scope-target look verification · 📄 موصوف
- **ماذا / what:** Verify a grade by measuring luma percentiles and vectorscope cluster radius on the final SDR output, excluding letterbox/subtitles, and compare +1/+2 stop variants on a real display.
- **كيف / how:** FFmpeg signalstats / Python numpy on extracted frames: Y' P10/P50/P95, % >99 IRE, chroma radius per hue cluster.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow` · `kosif-atlas/skills/1096-akbun-editvideo/2434-akbun-davinciresolve-exposure`

#### QA-281 · قائمة مراجعة التحريك · Animation review checklist (contact/passing) · 📄 موصوف
- **ماذا / what:** Check distinct contact and passing poses, consistent bob, limbs separated from torso, constant volumes, held impact frames, short anticipation on player attacks.
- **كيف / how:** Render all frames side by side in a preview sheet and inspect; GIF first frame alone is misleading.
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9525-animate`

#### QA-282 · فحص الشفافية والهالات · Real alpha and halo checks · 📄 موصوف
- **ماذا / what:** Verify true transparency (a baked checkerboard is not alpha) and look for edge halos on both light and dark backgrounds.
- **كيف / how:** Pillow: check alpha channel range, composite over #000 and #fff and inspect edges; keep untrimmed frames or trim offsets to avoid jitter.
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4171-game-sprites` · `kosif-atlas/skills/2657-figures/10115-transparent-icons`

#### QA-283 · تعليق الإشارة مقابل الضجيج · Signal-vs-noise annotation · 📄 موصوف
- **ماذا / what:** Do not let an animated stat claim a change that sampling noise can explain; attach an interval or say 'not yet distinguishable'.
- **كيف / how:** Get the denominator first; rates -> Wilson interval, means -> t or bootstrap CI on the difference, counts -> Poisson CI. If the 95% CI of a change spans zero, the on-screen line is 'within normal variation'. Never call two points a trend; use a fitted slope with a band.
- **أرقام / params:** 95% CI; alpha 0.05
- **الدليل / proof:** `kosif-atlas/skills/2235-applied-statistics/8498-statistical-qa-of-metrics/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10330-statistical-and-uncertainty-visualizatio/references/uncertainty-encodings.md`

#### QA-284 · حلقة فحص: قياس ثم حكم · Measure-then-judge figure QA loop · 📄 موصوف
- **ماذا / what:** Scripts measure everything with ground truth (fonts, palette, overlaps, text present, resolution); a fresh-context vision review scores only aesthetics.
- **كيف / how:** Pass the reviewer the frame/figure, target format, palette and the exact strings that must appear. Vision rubric 1-5: clarity, hierarchy, alignment, palette coherence, format fit. Verdict: ship (no programmatic issues and all >=4), revise (fixable issues or any 3), block (any 1-2 or unreadable text). One targeted change per iteration, stop at ship or after 3 iterations.
- **أرقام / params:** 5 dims x 1-5; ship >=4; max 3 iterations
- **الدليل / proof:** `kosif-atlas/skills/2657-figures/10110-figure-qa/SKILL.md` · `kosif-atlas/skills/2657-figures/10110-figure-qa/references/figure-qa-procedure.md` · `kosif-atlas/skills/2657-figures/10110-figure-qa/references/iterate-loop.md`

#### QA-285 · حالات ثابتة لاختبار الصور · Stable visual regression states · 📄 موصوف
- **ماذا / what:** Screenshot tests compare intentional states, with fonts, viewport, timezone, locale and motion frozen.
- **كيف / how:** Capture the smallest useful region at named key times; wait for fonts and async labels; mask volatile regions; pair each image diff with a semantic assertion (e.g. label text present); review baseline updates instead of auto-accepting. Applies to frame checks of chart scenes.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10331-testing-data-visualizations/references/visual-regression-and-image-testing.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10331-testing-data-visualizations/SKILL.md`

#### QA-286 · التحقق من تصيير الخرائط · Map render verification · 📄 موصوف
- **ماذا / what:** Map motion must be judged on a rendered MP4, not a live preview.
- **كيف / how:** Render a middle-frame still first (framing, bank, labels), then a short MP4; inspect terrain/satellite detail during camera moves for shimmer (switch to fixed plate if any), check soft tiles (plate underspecified or scale > 1), check each aspect ratio, check attribution visible.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/references/render-stability.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/references/3d-flyover-architecture.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/TECHNIQUE.md`

#### QA-287 · تحقق من واجهات البيانات · Trust-but-verify data APIs · 📄 موصوف
- **ماذا / what:** Some public data APIs return HTTP 200 with empty or silently wrong aggregates; never trust a plausible number from a guessed query.
- **كيف / how:** Use only queries verified live; check row counts and totals against a second source; record the query and date in the scene's source line. Example trap: Data USA cubes that return zero rows or aggregate over undrilled dimensions.
- **الدليل / proof:** `kosif-atlas/skills/2622-city-report/9999-city-report/references/api-gotchas.md` · `kosif-atlas/skills/2622-city-report/9999-city-report/SKILL.md`

#### QA-288 · فحص عمى الألوان والرمادي · Colorblind and grayscale check · 📄 موصوف
- **ماذا / what:** Charts must survive color-vision deficiency and grayscale: color is never the only cue.
- **كيف / how:** Add direct labels, markers, dash styles or ordering; simulate deficiencies and a grayscale pass on key frames; avoid hue-only red/green pairs; keep the accent distinguishable by lightness too.
- **الدليل / proof:** `kosif-atlas/skills/317-data/942-data-visualization/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10318-accessibility-and-inclusive-visualizatio/references/color-contrast-and-redundant-encoding.md` · `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/SKILL.md`

#### QA-289 · سجل المصدر والإفصاح عن الذكاء الاصطناعي · Provenance ledger and AI disclosure · 📄 موصوف
- **ماذا / what:** Record prompt, model, provider, license, indemnity, C2PA status and date for every generated asset because C2PA manifests are often stripped; add visible disclosure for EU audiences.
- **كيف / how:** Append one JSON line per asset; state that a paid plan is a license, not copyright ownership (purely AI images lack US copyright; substantial human modification helps); EU AI Act Art.50 disclosure enforceable from 2 Aug 2026; route legal claims to counsel.
- **الدليل / proof:** `kosif-atlas/skills/2306-generative-web-media/8853-license-and-provenance-ledger` · `kosif-atlas/skills/2248-brand-identity-studio/8558-brand-legal-and-licensing` · `kosif-atlas/skills/259-quickdesign/865-quickdesign`

#### QA-290 · منهج تدقيق الكثافة قبل وبعد · Before/after visual density audit method · 📄 موصوف
- **ماذا / what:** Documented method for a style-only patch: measure font sizes, line length, chrome height and visible tabs before/after, and prove no capability changed by counting tables/rows/fields/buttons on every tab plus overflow checks at 390px.
- **كيف / how:** Run in a real browser; record per-tab counts (e.g. 1/330/3/8) and compare; check horizontal overflow and console errors.
- **أرقام / params:** chrome 226 -> 188px; visible tabs 7/13 -> 13/13; mobile 390px no overflow
- **الدليل / proof:** `kosif-audit-pro/patch/README.md`

#### QA-291 · سجل مصدر الأصول · Asset provenance ledger · 📄 موصوف
- **ماذا / what:** Every generated or processed asset is logged with source model, approval, resolution, size, use and honesty notes (e.g. 'local upscale, not native 4K'), private inputs never committed, paid retries guarded.
- **كيف / how:** Markdown table per asset in docs/design/*; flag file to block automatic paid re-tries; worklog entry.
- **الدليل / proof:** `kosif-earth-ci-fork/docs/design/KOSIF_EARTH_CINEMATIC_INTRO_20261009_ar.md` · `kosif-earth-ci-fork/docs/design/HIGGSFIELD_VISUALS_ar.md` · `kosif-earth-ci-fork/AGENT_WORKLOG.md:1045`

#### QA-292 · قياس جهارة صوت المقدمة · Intro audio loudness (measured) · 📄 موصوف
- **ماذا / what:** Measured the intro soundtrack: quiet, low-range bed well below a -14 LUFS social target; sample rate 32 kHz rather than 48 kHz.
- **كيف / how:** ffmpeg -af loudnorm=print_format=summary on earth-intro-20261009.mp4.
- **أرقام / params:** integrated -24.5 LUFS; true peak -7.5 dBTP; LRA 2.8 LU; AAC-LC 32 kHz stereo
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/brand/earth-intro-20261009.mp4`

#### QA-293 · ميزانية أداء الطبقة الزخرفية · Decorative-layer perf budget · 📄 موصوف
- **ماذا / what:** Acceptance for the 3D background: at least 20 fps on a laptop, canvas size equals viewport, one still frame under reduced motion.
- **كيف / how:** Browser checks recorded in the rebuild doc.
- **أرقام / params:** >=20 fps
- **الدليل / proof:** `kosif-earth-ci-fork/docs/rebuild/COMPANY_FIRST_REBUILD_ar.md:41`

#### QA-294 · ميثاق عدم الادعاء · No-false-claims honesty contract · 📄 موصوف
- **ماذا / what:** Forbids claiming premium models, 4K, sync, lip-sync, Higgsfield connectivity, inspected media or paid services without evidence; QA metrics and manual checks are reported separately.
- **كيف / how:** Agent states which engines are routing targets vs implemented, marks manual_visual_review NOT_DONE until actually watched, and lists missing deps/licences on delivery.
- **الدليل / proof:** `fastify-motion-bro/AGENTS.md:18-22` · `fastify-motion-bro/docs/PRODUCTION-GATES.md:8-14` · `fastify-motion-bro/docs/ROADMAP.md:9`

#### QA-295 · قائمة مراجعة الرندر · Render review checklist · 📄 موصوف
- **ماذا / what:** Ten-point pre-delivery list: signed script, device safe margins, real animation tied to words, captions validated, colours/Arabic diacritics, preview viewed, first/middle/last frames, codec/size/fps/duration/audio/loudness, licensing, deliverables.
- **كيف / how:** Walk the list after render; mark each item with evidence.
- **أرقام / params:** 10 items; aspects 9:16/16:9/1:1
- **الدليل / proof:** `fastify-motion-bro/docs/REVIEW_CHECKLIST.md:1-11`

#### QA-296 · فحص بوابات المحرر في CI · CI editorial gate check · 📄 موصوف
- **ماذا / what:** CI runs all five viral stages with a fixture, compiles, and asserts 30 s, 5 scenes, 9:16, exactly 2 background lines and final_render still false before a smoke render + qa.py.
- **كيف / how:** GitHub Actions job editorial-smoke (Node 22, Python 3.12, apt ffmpeg, playwright chromium).
- **أرقام / params:** duration 30; scenes 5; lines 2
- **الدليل / proof:** `fastify-motion-bro/.github/workflows/ci.yml:14-54`

#### QA-297 · مراجعة الإطار الأول والأوسط والأخير · First/middle/last frame review · 📄 موصوف
- **ماذا / what:** After render, inspect opening, middle and closing frames and listen for sync, transitions, Arabic correctness and artefacts; do not overstate metrics.
- **كيف / how:** Extract stills with ffmpeg -ss, view them, record findings separately from ffprobe metrics.
- **الدليل / proof:** `fastify-motion-bro/AGENTS.md:17` · `fastify-motion-bro/docs/REVIEW_CHECKLIST.md:8`

#### QA-298 · تصيير حتمي بدوكر · Docker deterministic render · 📄 موصوف
- **ماذا / what:** Pins Chromium, fonts and FFmpeg for bit-stable output.
- **كيف / how:** hyperframes render --docker.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/concepts/determinism.mdx`

#### QA-299 · تشخيص صوت لا يمكن سماعه · Diagnose audio you cannot hear · 📄 موصوف
- **ماذا / what:** Compare against something inside the same file (clean original, pauses/noise floor, speech tilt, file vs itself over time), never a different voice; ffmpeg recipes for integrated loudness (ebur128), proportional band energy, noise floor, level over time, pitch.
- **كيف / how:** references/diagnosis.md; gain_db = target_lufs - measured_lufs; formants +/-10 dB, fundamentals 85-255 Hz, sentences decline 5-6 dB.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-audio/references/diagnosis.md`

#### QA-300 · فخاخ HyperFrames · HyperFrames traps · 📄 موصوف
- **ماذا / what:** Known lint failures: dir=rtl on <html> renders blank; audio without id silent; unknown font family fails; GSAP fromTo renders from-state immediately; marker-end arrowheads show early.
- **كيف / how:** Use direction:rtl;unicode-bidi:isolate on text elements; @font-face local(); drawPath with set+immediateRender:false; separate head shapes
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `100-superskills/skills/kosif-montage-motion/SKILL.md:123`

#### QA-301 · حدود السرعة · Speed limits · 📄 موصوف
- **ماذا / what:** Text being read ≤3 px/f; >12–20 px/f needs blur; nothing >80 px/f.
- **كيف / how:** Apply as defaults while authoring; verify with kmotion measure/speed/sheet
- **أرقام / params:** kmotion speed FILM (optical flow px/f)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`

#### QA-302 · طاقة اختلاف الإطارات · Frame-difference energy · 📄 موصوف
- **ماذا / what:** Luma frame difference at 320 px as pacing metric.
- **كيف / how:** Apply as defaults while authoring; verify with kmotion measure/speed/sheet
- **أرقام / params:** median 1.4, p90 6.0; calm premium median 0.35–0.5, spikes ≥2.4; kmotion measure / study REF.mp4
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`

#### QA-303 · قاعدة الصدق · Honesty rule · 📄 موصوف
- **ماذا / what:** Report measured vs not; credit footage; never fabricate/replace a real face; never claim un-run renders.
- **كيف / how:** policy
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:207` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### QA-304 · تقرير فحص التسليم لفيديو صوتي · Delivery QA report for a voice-driven render · 📄 موصوف
- **ماذا / what:** A finished render is checked and reported: input vs output duration, codec, resolution, fps, frame count, audio codec/sample rate, correlation between delivered and source voice, sampled brightness levels and frame differences, plus honest notes about timing method and review depth.
- **كيف / how:** qa_report.json {result PASS, input_duration_s 28.84, rendered 28.84, video h264 720x1280 30/1 865 frames, audio aac 24000 Hz, voice_signal_correlation 0.99997, sample_brightness_levels[8], sample_differences[7], notes[]}.
- **أرقام / params:** voice correlation ≥ 0.9999 means audio untouched
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/examples/voice2motion/qa_report.json`

#### QA-305 · حلقة النقد الثمانية · 8-criterion critique loop · 📄 موصوف
- **ماذا / what:** Score Hook, Readability, Motion, Variety, Composition, Truth, Sound sync, Brand 1-10; fix worst 3; >=3 rounds; end with What I'd still change.
- **كيف / how:** kmotion sheet + review.md
- **أرقام / params:** readable at 360 px wide; nothing <28 px; 8+ target
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md` · `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### QA-306 · قائمة جودة الحركة · LottieFiles quality checklist · 📄 موصوف
- **ماذا / what:** Elements >40 px, natural arcs, follow-through, <20 animated elements, transform+opacity, reduced-motion variant.
- **أرقام / params:** follow-through 50-150 ms; <20 elements
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### QA-307 · مراجعة بثلاث عدسات · Three-lens review receipt · 📄 موصوف
- **ماذا / what:** Design/Motion/Engineering review and receipt of rendered/tested/untested.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-director.md`

#### QA-308 · إطارات المراجعة · Review frames (eight-second gate) · 📄 موصوف
- **ماذا / what:** Exports still frames at chosen times so the composition can be judged before rendering.
- **كيف / how:** From the studio: recipe 'frames' (form in the الوصفات tab, POST /api/jobs {recipe:'frames', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py frames …`.
- **أرقام / params:** project (dir); --times 1,4,7 (the project panel uses 1,3,5)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:60`

#### QA-309 · فحص الحتمية والذوق · Determinism and taste lint · 📄 موصوف
- **ماذا / what:** Checks a composition for non-deterministic code and taste issues before rendering.
- **كيف / how:** From the studio: recipe 'lint' (form in the الوصفات tab, POST /api/jobs {recipe:'lint', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py lint …`.
- **أرقام / params:** project (dir)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:66`

#### QA-310 · بوابة التسليم · Delivery gate (black, freeze, LUFS, peak, exposure) · 📄 موصوف
- **ماذا / what:** Checks a finished film for black frames, freezes, loudness, peaks and exposure before delivery.
- **كيف / how:** From the studio: recipe 'inspect' (form in the الوصفات tab, POST /api/jobs {recipe:'inspect', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py inspect …`.
- **أرقام / params:** film
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:96`

#### QA-311 · لوحة النقد · Critique sheet (frames + phone view) · 📄 موصوف
- **ماذا / what:** Builds a contact sheet of frames and a phone-size view for critique.
- **كيف / how:** From the studio: recipe 'sheet' (form in the الوصفات tab, POST /api/jobs {recipe:'sheet', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py sheet …`.
- **أرقام / params:** film
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:97`

#### QA-312 · معلومات الملف · File probe · 📄 موصوف
- **ماذا / what:** Prints media file information (ffprobe).
- **كيف / how:** From the studio: recipe 'probe' (form in the الوصفات tab, POST /api/jobs {recipe:'probe', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py probe …`.
- **أرقام / params:** file
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:98`

#### QA-313 · فحص البيئة · Environment doctor · 📄 موصوف
- **ماذا / what:** Reports what this PC can run (FFmpeg, browser, Whisper, fonts, face detector).
- **كيف / how:** From the studio: recipe 'doctor' (form in the الوصفات tab, POST /api/jobs {recipe:'doctor', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py doctor …`.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:99`

#### QA-314 · مخطط reel.json ومدققه · reel.json schema and checker · 📄 موصوف
- **ماذا / what:** Validates a review reel before the player opens it: required fields, gapless scenes, unique ids without dots, boxes inside the frame, brand colour references, prop types, list rows and choices, Arabic copy without lang, and the video's size/fps/duration via ffprobe.
- **كيف / how:** node scripts/web/static/review/check.mjs <project-dir> [--json] | --selftest (not executed here: third-party file).
- **أرقام / params:** prop types text, longtext, number, color, media, list, choice, motion; tolerance 0.06 s (~2 frames at 30 fps); duration mismatch > 0.25 s = error; fps mismatch > 0.05 = warning; audio defaults {music:null,bpm:null,drop:0,musicVol:0.6,sfxVol:0.8}
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/check.mjs:1` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/check.mjs:10`

#### QA-315 · بوابات جودة التسليم · Delivery quality gates (montage) · 📄 موصوف
- **ماذا / what:** Four gates before any video ships.
- **كيف / how:** 1) look at contact-sheet.png for black/glitch frames; 2) ebur128 measured -14 +/- 1.5 LUFS; 3) caption contrast >= 4.5:1 and Arabic text inside the safe area; 4) H.264 + yuv420p.
- **أرقام / params:** -14 +/- 1.5 LUFS; 4.5:1; yuv420p
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/SKILL.md`

#### QA-316 · قائمة منع أخطاء التوليد · Generator failure-prevention checklist · 📄 موصوف
- **ماذا / what:** What to check in every generated frame.
- **كيف / how:** anatomy, duplicated limbs, impossible contact, inconsistent light, bad scale, garbled text, melted props, contradictory camera cues; also hands, teeth, earrings asymmetry, repeated textures, reflections.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-visual-aesthetics-council/SKILL.md` · `kosif-one/tools/kosif-omni/skills/kosif-vision/SKILL.md`

#### QA-317 · أتمتة المتصفح ولقطات الفحص · Browser automation & screenshot QA (Playwright patterns) · 📄 موصوف
- **ماذا / what:** Element index script with stable FNV-1a ids, role/name locators, postcondition waits and full-page screenshots — for rendering and checking HTML animations or UI demos.
- **كيف / how:** page.evaluate(element-index JS) -> act on [data-kosif-action=ID]; expect(...).to_be_visible(timeout=10000); page.screenshot(full_page=True); downloads via expect_download; gate steps with kosif_action_gate.
- **أرقام / params:** viewport 1280x800; 250 elements max; anti-loop: 3 same-target picks
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-computer-use/references/computer-playbook.md` · `kosif-one/tools/kosif-omni/skills/kosif-computer-use/SKILL.md`

#### QA-318 · مستويات القدرة وقواعد الصدق · Capability tiers & truth rules · 📄 موصوف
- **ماذا / what:** Labels how much was actually verified: T0 playbook only (unverified), T1 local scripts, T2 MCP tools, T3 live backend; capability != exposure != execution != goal; receipts at the end.
- **كيف / how:** State tier and receipt: family, mode, what ran, evidence, verification, limits, next step.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-omni/references/host-adapters.md` · `kosif-one/tools/kosif-omni/skills/kosif-omni/SKILL.md` · `kosif-one/tools/kosif-omni/skills/kosif-omni/references/live-verification.md`

#### QA-319 · قاعدة نظافة المصادر · Source hygiene rule (no burned-in text, logos, screen recordings) · 📄 موصوف
- **ماذا / what:** Reject found clips that carry burned-in English text, logos, screen recordings or a drawing style that breaks realism; record URL, creator and rights for every clip; never claim publication rights from a download.
- **كيف / how:** Contact-sheet review + manifest 'rights: unverified' field + receipt 'source_licensing' note.
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/MONTAGE_REUSE_RUNBOOK_AR.md` · `kosif-one/projects/KOSIF_Motion_Ghorba/pinterest_kmotion/fetch-credits.json`

#### QA-320 · حلقة النقد الذاتي · Critique loop rubric (8 criteria, >= 3 rounds) · 📄 موصوف
- **ماذا / what:** Score hook, readability, motion quality, variety, composition, truth, sound sync and brand 1-10 on rendered frames; fix the three worst with timestamps; end with 'What I'd still change'.
- **كيف / how:** Apply after motion.py sheet; documented in motion-craft.md and craft-numbers.md.
- **أرقام / params:** hook in first 2 s; words readable at 360 px; nothing < 28 px; something new every 2-4 s
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/references/motion-craft.md` · `kosif-one/tools/kosif-studio/motion/references/craft-numbers.md`

#### QA-321 · تشخيص أعطال ffmpeg · ffmpeg troubleshooting table · 📄 موصوف
- **ماذا / what:** Fixes for VFR drift, non-monotonous DTS, washed iOS colour, invalid NAL, frozen start.
- **كيف / how:** fps=30 or -vsync cfr -r 30 + aresample=async=1; -fflags +genpts; -color_primaries/trc/colorspace bt709; remux -c copy; align to I-frame.
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### QA-322 · بوابات تسليم المونتاج · Editor delivery gates · 📄 موصوف
- **ماذا / what:** Duration within 1 frame of EDL, measured loudness, peak <=-1 dBTP, CFR output, no -c copy off keyframe, contact sheet, black-frame check.
- **كيف / how:** ffprobe on output + blackdetect + contact-sheet.png
- **أرقام / params:** ±1 frame
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/SKILL.md`

#### QA-323 · قياس بالـ Scopes عبر لقطات · Scope measurement via stills · 📄 موصوف
- **ماذا / what:** Without API scopes: set timecode to clip middle, export still, compute luminance/channel histograms with Pillow; WB channel diff <=20/255 on true neutral.
- **كيف / how:** Timeline.SetCurrentTimecode + Project.ExportCurrentFrameAsStill + Pillow
- **أرقام / params:** <=20/255
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/color-grading-order.md`

#### QA-324 · سجل العلامات الملوّنة · Resolve marker registry · 📄 موصوف
- **ماذا / what:** Fixed marker colours: Blue CHAPTER (first at frame 0), Purple/Pink PRIVACY, Red CUT_DONE, Yellow CUT_REVIEW, Lemon EXPOSURE_CHECK, Sky WB_CHECK, Sand AUDIO_REVIEW, Cyan GFX; offsets +0..+6 avoid collisions; only Resolve's 16 colours.
- **كيف / how:** Timeline.AddMarker(frame,color,name,note,dur)
- **أرقام / params:** 16 colours
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/color-grading-order.md`

#### QA-325 · كشف اللقطات الرديئة · Bad-segment detection · 📄 موصوف
- **ماذا / what:** Dark, shaky, out-of-focus parts found from extracted frames by Laplacian variance and flagged CUT_REVIEW before deletion.
- **كيف / how:** ffmpeg frame extract + Laplacian variance
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/SKILL.md`

#### QA-326 · فحص ما قبل الرندر · Pre-render checklist (Resolve) · 📄 موصوف
- **ماذا / what:** Resolution/fps match timeline, no offline media/black frames, peak <=-1 dBTP, scene diffs <=6 dB, no exposure/colour jumps, faces blurred, subs in safe area.
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/references/color-grading-order.md`

#### QA-327 · بوابة الخطوط والألوان المحظورة · Banned-font / default-colour gate · 📄 موصوف
- **ماذا / what:** Flags AI-default design: banned Latin fonts and over-used Arabic fonts, default greys/blues.
- **كيف / how:** Reject Inter, Roboto, Open Sans, Lato, Poppins, Outfit, Sora, Syne, Playfair, Cinzel; Arabic flagged list Cairo, Tajawal, Changa, Amiri, Readex Pro, IBM Plex Sans Arabic; no #333/#3b82f6.
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/references/motion-rules.md` · `100-superskills/skills/claude-animation-studio/SKILL.md`

#### QA-328 · بوابة المقروئية · Readability gate · 📄 موصوف
- **ماذا / what:** Text >=40px at 1080p, contrast 4.5:1, read time less than on-screen time (3 s on screen read in 2).
- **كيف / how:** Check contact sheet.
- **أرقام / params:** 40px; 4.5:1
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/SKILL.md`

#### QA-329 · علامات التصميم الآلي · AI-design tells blacklist · 📄 موصوف
- **ماذا / what:** List of generic AI looks to remove: gradient text, left accent bar on cards, cyan on black, purple-blue gradient, pure black/white, identical card grids, all-centred single weight.
- **كيف / how:** Review contact sheet against list.
- **الدليل / proof:** `100-superskills/skills/trend-animation-styles/references/styles.md`

#### QA-330 · بوابة الثماني ثوانٍ · Eight-second gate + weakest-beat gate · 📄 موصوف
- **ماذا / what:** Build 5-8 s, contact sheet to requester, ask worst seconds, rebuild; then same for middle.
- **أرقام / params:** 5-8 s
- **الدليل / proof:** `100-superskills/skills/motion-director-pro/SKILL.md`

#### QA-331 · اختبار التجميد · Freeze test for fake motion · 📄 موصوف
- **ماذا / what:** Motion that survives freezing all gradients is real; drifting gradients fake low stillness numbers.
- **الدليل / proof:** `100-superskills/skills/motion-director-pro/references/motion-floor.md`

#### QA-332 · 2). تدقيق وإصلاح الإتاحة · Accessibility (WCAG 2 · 📄 موصوف
- **ماذا / what:** WCAG 2.2: 4.5:1 contrast, 200% zoom, pausable motion, meaningful alt text, RTL checks -> apply as caption/text contrast and motion-safety gate.
- **كيف / how:** Load skill accessibility-wcag (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/accessibility-wcag/SKILL.md`

#### QA-333 · فحص الادعاءات والأرقام والاقتباسات والاس · Fact-Checker & Verifier · 📄 موصوف
- **ماذا / what:** Owner-built skill "Fact-Checker & Verifier" (own words): workflow guidance for fact-checker & verifier; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill fact-checker-verifier (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/fact-checker-verifier/SKILL.md`

#### QA-334 · تقييم مخرجات الذكاء الاصطناعي بأرقام تصم · LLM Judge & Eval Lab · 📄 موصوف
- **ماذا / what:** Owner-built skill "LLM Judge & Eval Lab" (own words): workflow guidance for llm judge & eval lab; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill llm-judge-eval-lab (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/llm-judge-eval-lab/SKILL.md`

#### QA-335 · تقييم أي ميزة ذكاء اصطناعي بأرقام · LLM Judge & Eval Suites · 📄 موصوف
- **ماذا / what:** Owner-built skill "LLM Judge & Eval Suites" (own words): workflow guidance for llm judge & eval suites; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill llm-judge-evals (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/llm-judge-evals/SKILL.md`

#### QA-336 · اختبارات تثبت أن الكود يعمل · Complete Testing Suite · 📄 موصوف
- **ماذا / what:** Owner-built skill "Complete Testing Suite" (own words): workflow guidance for complete testing suite; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill testing-suite-complete (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/testing-suite-complete/SKILL.md`

#### QA-337 · اختبار الفهم بلا صوت · Silent-readability test · 📄 موصوف
- **ماذا / what:** Storyboard must be understandable muted; each shot adds new info.
- **كيف / how:** review
- **الدليل / proof:** `100-superskills/skills/storyboard-shotlist/SKILL.md:25`

#### QA-338 · نسختان A/B · A/B thumbnail single-variable · 📄 موصوف
- **ماذا / what:** Two versions differing in exactly one element; 10% downscale legibility test.
- **كيف / how:** Playwright
- **الدليل / proof:** `100-superskills/skills/thumbnail-social-graphics/SKILL.md:24`

#### QA-339 · قياسات الصورة · Image metrics by code · 📄 موصوف
- **ماذا / what:** Histogram, sharpness, exposure ratio, dominant colour.
- **كيف / how:** PIL/numpy
- **الدليل / proof:** `100-superskills/skills/image-critique-reverse-prompt/SKILL.md:21`

#### QA-340 · تقييم بخمس معايير · 5x20 critique score · 📄 موصوف
- **ماذا / what:** Declared criteria each scored /20; composition (thirds, leading lines, space, balance) and gen defects (limbs, text, reflections, repetition).
- **كيف / how:** score.json
- **الدليل / proof:** `100-superskills/skills/image-critique-reverse-prompt/SKILL.md:22`

#### QA-341 · حدّ نابض الأذن · Ear spring speed limit · 📄 موصوف
- **ماذا / what:** Spring parameters for secondary motion chosen to stay under the speed gate.
- **كيف / how:** spring(t, t0, freq, damping) on ear pivots.
- **أرقام / params:** 1.5 Hz / zeta .42 stays under 80 px/frame at 1080×1920; 2.2 Hz / zeta .28 failed
- **الدليل / proof:** `kosif-studio/motion/references/shape-kit.md`

#### QA-342 · قائمة جودة الحركة · Motion quality checklist · 📄 موصوف
- **ماذا / what:** Abridged LottieFiles checklist.
- **كيف / how:** Run before final render.
- **أرقام / params:** elements > 40 px; < 20 animated per viewport; follow-through 50-150 ms on children; primary/secondary/ambient layers; natural arcs; not opacity-only for key changes; transform+opacity primary; reduced-motion alternative for interactive
- **الدليل / proof:** `kosif-studio/motion/references/motion-craft.md`

#### QA-343 · الدقة وإتاحة الوصول · Meaning, data truth and accessibility · 📄 موصوف
- **ماذا / what:** Keep real values/units/provenance; never animate fabricated intermediate amounts; label demo data; Arabic shaping and bidi numbers; reduced motion keeps information.
- **كيف / how:** Logical CSS properties; keyboard/touch alternatives.
- **الدليل / proof:** `kosif-studio/motion/references/motion-director.md`

#### QA-344 · قائمة الفيديو القابل للتكرار · Reproducible video checklist · 📄 موصوف
- **ماذا / what:** Confirm size/fps/duration/audio; one seekable clock; seed randomness; load fonts/media before capture; sample first, peak, boundary and final frames, seek backward and forward; verify the encoded file.
- **كيف / how:** motion.py frames / inspect; report rendered/tested/untested honestly.
- **الدليل / proof:** `kosif-studio/motion/references/motion-director.md`

#### QA-345 · بوابة التسليم · Delivery inspect gate · 📄 موصوف
- **ماذا / what:** Fail-closed check of the encoded file.
- **كيف / how:** motion.py inspect FILM [--allow 6.6-7.3].
- **أرقام / params:** H.264 yuv420p even size; truly black and frozen stretches (end hold = warning); integrated LUFS and true peak; blown highlights/crushed blacks on sampled frames
- **الدليل / proof:** `kosif-studio/motion/references/hyperframes-authoring.md` · `kosif-studio/motion/references/KOSIF_SEE_INTEGRATION.md`

#### QA-346 · معيار النقد بمراجعين · Two-reviewer critique rubric · 📄 موصوف
- **ماذا / what:** Two reviewers score alone, then merge; findings are ranked P0 (breaks film), P1 (reads generated), P2 (taste); the fixer only changes what a reviewer can point to on a frame; at least 3 rounds until no P0/P1.
- **كيف / how:** Fill review.md written by qa.sheet; score 8 criteria 1-10 with timestamps.
- **أرقام / params:** criteria: hook by 1 s; readability at 360 px; motion quality; variety every 2-4 s and ≤2 uses per transition; one hero per frame; truth; sound sync on contact frames, −14 LUFS; identity
- **الدليل / proof:** `kosif-studio/motion/qa.py:133`

#### QA-347 · العدسات الجمالية الاثنتا عشرة · Twelve aesthetic lenses · 📄 موصوف
- **ماذا / what:** A council checklist judged on frames: world & depth, character silhouette, action/contact, camera, light, colour, VFX, atmosphere, materials, production design, composition, beauty.
- **كيف / how:** Write one line per lens in review.md.
- **الدليل / proof:** `kosif-studio/motion/qa.py:152`

#### QA-348 · قائمة صيد العيوب · Failure hunt list · 📄 موصوف
- **ماذا / what:** Concrete defects to look for: overlapping text during swaps, sliding instead of easing, corner labels/frame borders, centred title on gradient, blurry scaled text, dead beats, loop-seam stutter, device blinking out, inconsistent light, bad scale, impossible contact, blown/crushed exposure.
- **كيف / how:** Scan contact.png and phone.png against the list.
- **الدليل / proof:** `kosif-studio/motion/qa.py:159`

#### QA-349 · معاينة قبل الرندر النهائي · Preview-before-render approval gate · 📄 موصوف
- **ماذا / what:** Contact sheet (9-12 frames) + 3-5 s clip of the hardest scene approved by the user before the final render.
- **كيف / how:** render_html --preview; --start/--duration
- **الدليل / proof:** `kosif-tool/templates/PLAN.md`

#### QA-350 · أخطاء الـ3D الشائعة · 3D anti-patterns · 📄 موصوف
- **ماذا / what:** Reject chrome-everything, aimless spinning logos, motion-sick whips, default grey light, random lens flares, 3D where flat explains better.
- **كيف / how:** Preview review checklist.
- **أرقام / params:** hero frame hold ≥ 1.5 s; no z-fighting/clipping
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:86-99`

#### QA-351 · قائمة فحص الإعلان · Ad QA checklist · 📄 موصوف
- **ماذا / what:** 10-point ad gate: first-frame motion, one message per beat, one CTA ≥2 s, brand tokens, product ≥40%, platform aspect, works muted, prices isolated, logo ≥1 s, truthful claims.
- **الدليل / proof:** `kosif-tool/playbooks/ads.md:89-98` · `kosif-tool/playbooks/ads.md:102`

#### QA-352 · فحص الطباعة العربية · Arabic typography QA · 📄 موصوف
- **ماذا / what:** 10 checks: no split words, no letter-spacing, fonts loaded, captions ≥56 px on 9:16, bidi isolated, one digit system, diacritics unclipped, entrances from right, Arabic punctuation, phone-size screenshot.
- **الدليل / proof:** `kosif-tool/playbooks/arabic-typography.md:85-94` · `kosif-tool/playbooks/arabic-typography.md:98`

#### QA-353 · فحص التزامن في ثلاث لحظات · Three-point sync spot check · 📄 موصوف
- **ماذا / what:** Watch with sound at three timestamps per scene after automated checks.
- **أرقام / params:** 3 points per scene
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:86` · `kosif-tool/playbooks/kinetic-type.md:85`

#### QA-354 · أخطاء تحريك الشخصيات · Character anti-patterns · 📄 موصوف
- **ماذا / what:** Avoid puppet whole-body rotation, rubber limbs, identical timing, sliding feet, famous-character imitation.
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:87-100`

#### QA-355 · أخطاء الرسوم البيانية · Chart anti-patterns · 📄 موصوف
- **ماذا / what:** Bouncing bars, everything-at-once soup, slot-machine counters, neon/gradients/3D on data, invented data, truncated axes, cross-dataset morphs, idle wobble, simultaneous chart+caption, camera shake, mirrored time axes, mixed digits.
- **الدليل / proof:** `kosif-tool/playbooks/charts.md:229-241` · `kosif-tool/playbooks/charts.md:214-223`

#### QA-356 · أخطاء مشاهد الكود · Code anti-patterns · 📄 موصوف
- **ماذا / what:** No Matrix rain, hacker clichés, tiny code, typing 60-line files, render-varying jitter; same frame twice = identical pixels.
- **الدليل / proof:** `kosif-tool/playbooks/code.md:85-98`

#### QA-357 · أخطاء التايبوغرافي الحركي · Kinetic-type anti-patterns · 📄 موصوف
- **ماذا / what:** No typewriter everywhere, letter flying, glow/chromatic aberration on body, bounce-every-word, diagonal slides, random fonts, too-short holds.
- **الدليل / proof:** `kosif-tool/playbooks/kinetic-type.md:91-104`

#### QA-358 · حد الوميض الآمن · Flash safety limit · 📄 موصوف
- **ماذا / what:** Avoid strobe; keep flashes below 3 per second.
- **أرقام / params:** < 3 flashes/s
- **الدليل / proof:** `kosif-tool/playbooks/music.md:93`

#### QA-359 · أخطاء الجسيمات · Particle anti-patterns · 📄 موصوف
- **ماذا / what:** No endless glowing dust, bloom on everything, Math.random per frame, particles over captions, rainbow colours.
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:84-97`

#### QA-360 · قائمة فحص الرندر · Render QA checklist · 📄 موصوف
- **ماذا / what:** Preview approved, identical re-render, fonts loaded, duration/fps/frames match, yuv420p even dims, AAC untouched audio, loudness, intentional first/last frames, editable sources delivered, TEST_REPORT filled; never claim unrun checks.
- **الدليل / proof:** `kosif-tool/playbooks/render-pipeline.md:95-108`

#### QA-361 · أخطاء أفلام الهاتف · Phone anti-patterns · 📄 موصوف
- **ماذا / what:** Floating phone, perpetual bob, bending glass, mismatched radii, blurry screenshot, ghost taps, looping glare, rainbow chrome, mirrored hardware, linear scrolling, wall-clock motion.
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:211-237`

#### QA-362 · أخطاء أفلام الصور · Photo anti-patterns · 📄 موصوف
- **ماذا / what:** Screensaver push-ins, 1 s crossfades, stretched edges, opposing layers, haloed cut-outs, glossy 3D photo cards, per-layer HDR, face over-push, black boxes, literal stock, mirrored text, undisclosed AI, audio-reactive scaling.
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:217-245`

#### QA-363 · أخطاء أفلام المنتج · Product UI anti-patterns · 📄 موصوف
- **ماذا / what:** Teleporting cursor, zero latency, bounce everywhere, glass-and-glow, lorem UI, uniform 300 ms, infinite stagger, blur-in text, 3D wobble, mismatched density, fake scroll, sound on everything.
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:243-257`

#### QA-364 · تقييم حدة المؤثرات · SFX high-frequency risk scoring · 📄 موصوف
- **ماذا / what:** Classify SFX by spectral centroid, brightBurden, highActiveDuration, envelope, transient sharpness to avoid fatiguing sounds.
- **كيف / how:** Use JSON fields to filter.
- **أرقام / params:** risk low/medium/high
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/assets/sfx/sfx-analysis.md`

#### QA-365 · اختيار إطار الغلاف · Settled poster frame pick · 📄 موصوف
- **ماذا / what:** Pick the strongest beat at a settled moment, not mid-transition.
- **كيف / how:** ffmpeg -ss T -i brag.mp4 -frames:v 1 -q:v 2 brag.jpg
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/step-4-deliver.md`

#### QA-366 · قاعدة الوصلة المتطابقة · Frame-identical seam rule · 📄 موصوف
- **ماذا / what:** Next clip starts from the previous clip's actual last frame to avoid pop.
- **كيف / how:** Extract last frame with ffmpeg -sseof -0.15, pass as --start-image.
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md` · `kosif-one/vendor/scroll-world/skills/scroll-world/references/pipeline.md:95`

#### QA-367 · فحص الوصلات · Seam QA pass · 📄 موصوف
- **ماذا / what:** Step 8 eyeballs each seam and each leg's last frame before chaining.
- **كيف / how:** Extract frames, compare.
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md:613`

#### QA-368 · حد أدنى للقراءة · Readability hold & 400 ms floor · 💡 فكرة
- **ماذا / what:** Scenes hold ≥1.8 s with settled title; anything visible <400 ms gets extended after frame inspection.
- **كيف / how:** Frame-by-frame QA pass.
- **أرقام / params:** 1.8 s min hold; 400 ms min visibility
- **الدليل / proof:** `style:pm-aschapmann-131210`

#### QA-369 · قاعدة العلامات التجارية · Trademark safety rule · 💡 فكرة
- **ماذا / what:** Never use third-party logos/trade dress; label unverified claims as placeholders.
- **كيف / how:** Review checklist.
- **الدليل / proof:** `style:pm-ceowinkz-7c776b`

#### QA-370 · تشغيل قابل للتكرار · Reproducible seeded runs · 💡 فكرة
- **ماذا / what:** No unseeded randomness; every run reproducible frame for frame.
- **كيف / how:** Seeded PRNG.
- **الدليل / proof:** `style:pm-kantamk-61f410`

#### QA-371 · منع النص فوق الوجه · Face-region text ban · 💡 فكرة
- **ماذا / what:** No text over selfie face, no blur on result, photos untinted.
- **كيف / how:** Face detect box check.
- **الدليل / proof:** `style:pm-l3d1c-0e35a3`

#### QA-372 · حد الوميض الآمن · Flash photosensitivity cap · 💡 فكرة
- **ماذا / what:** White/accent flash frames limited.
- **كيف / how:** Count flashes per second in timeline.
- **أرقام / params:** <=2 consecutive frames; <=3 flashes/s
- **الدليل / proof:** `style:pm-micheleharmonic-77628e`

## إضافات من Cinematic Director PRO v5

_مستخلصة من حزمة المالك KOSIF Claude Cinematic Director PRO v5 (انظر [cinematic-director-pro.md](../cinematic-director-pro.md)). مسارات الدليل `owner-upload:` تشير إلى ملفات داخل أرشيف المالك، لا إلى هذا المستودع._

#### QA-P01 · إيصال تنفيذ مُتحقَّق منه: لا نجاح بلا دليل · Evidence receipt validator (no verified success without evidence) · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل خطوة مهمة تُرجع إيصالًا بثمانية حقول، والفاحص يرفض أي «تم» بلا دليل. / Every consequential step returns an 8-field receipt; the gate rejects any verified success that carries no evidence.
- **كيف / how:** Receipt = {status: success|warning|error, summary, owner, evidence:[{type,ref}], artifacts:[], next_actions:[], retryable: bool, verified: bool}. Rules: all keys present; owner non-empty; evidence/artifacts/next_actions are arrays; booleans are real booleans; verified=true requires status=success AND non-empty evidence (else UNVERIFIED_SUCCESS_CLAIM); error can never be verified. CLI: python3 integrations/kosif-see/ecc_contract_gate.py validate-receipt r.json → exit 0 / 2. Ran here: a receipt with verified=true and evidence [] returned UNVERIFIED_SUCCESS_CLAIM, exit 2. Pair with QA-46 (ffprobe delivery receipt): put the ffprobe JSON and frame-sheet path into evidence. Idea adapted from ECC (MIT). **أرقام / params:** 8 required keys · exit 0 pass / 2 fail
- **الرخصة / license:** owner package; method adapted from affaan-m/ECC (MIT), no ECC code
- **الدليل / proof:** `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/integrations/kosif-see/ecc_contract_gate.py` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/tests/test_ecc_upgrade.py` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/integrations/kosif-see/ECC_DISTILLED_CORE.md`

#### QA-P02 · حلقة مراجعة الرندر المحدودة · Bounded iterative render review (½-second frames, 2–4 rounds) · 📄 موصوف / documented only
- **ماذا / what:** راجع الإطارات على فواصل ثابتة، أصلح، أعد الرندر — بعدد جولات محدود وشرط توقف واضح لا دوران بلا نهاية. / Review frames at fixed intervals, fix, re-render — a bounded number of rounds with a clear stop rule.
- **كيف / how:** Sample a frame every 0.5 s (every 0.25 s for short idents/logos); check motion, legibility, text clipping, sync and audio; fix the worst defect first; re-render. Plan 2–4 rounds by job size and stop as soon as the acceptance list passes or the time/budget cap is hit. Keep CODE_WRITTEN ≠ VIDEO_RENDERED ≠ QA_PASS as three separate states in the report. **أرقام / params:** frame step 0.5 s (0.25 s idents) · 2–4 rounds · three states
- **الرخصة / license:** owner package (own work)
- **الدليل / proof:** `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/references/GOOGLE_DOC_DISTILLATION.md` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/.claude/skills/kosif-cinematic-director/SKILL.md`
