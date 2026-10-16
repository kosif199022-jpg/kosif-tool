# القصة والإخراج — Story & direction

> فصل مُجمَّع آليًا من 498 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **484 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 484 powers deduplicated by name from 498 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 34 · 🟢 جاهز 33 · 📦 بأمر تثبيت 66 · 🔑 مفتاح/خدمة 9 · 👁 شوهد في فيديو 78 · 📄 موصوف 254 · 💡 فكرة 10

#### STORY-01 · التخطيط المسبق · proplan preflight · ✅ مُثبت هنا
- **ماذا / what:** Deterministic read-only plan: intent mapping, bounded Atlas method picks, 5-beat frame-accurate storyboard; --require-full-pro exits 3.
- **كيف / how:** python scripts/kmotion.py proplan --task '…' --seconds 12 --fps 30 --aspect 9:16 --mode pro --out plan.json
- **أرقام / params:** max 2 packs (4 deep)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:240` · `100-superskills/skills/kosif-montage-motion/UPGRADE_REPORT.md` · `100-superskills/skills/kosif-montage-motion/scripts/proplan.py` · `kosif-studio/motion/proplan.py:18`

#### STORY-02 · تشريح خطاف الفلوج الصامت · Silent-vlog hook anatomy · ✅ مُثبت هنا
- **ماذا / what:** A speech-free hook in front of a finished vlog: cold open 5-7 s (1-3 cuts, first cut shows the thumbnail subject, title text within the first second), context 3-6 s (where/when), curiosity 8-12 s (3-5 cuts opening at least one loop), 'only in this video' 5-8 s, teaser 3-5 s; whole hook <=45 s.
- **كيف / how:** Cuts start at 1.5-4 s (no run of sub-1 s cuts in calm films); last intro cut matches motion/direction of the first main-body cut; hook scenes stay in the main body. Implement as a hook segment list rendered ahead of the main timeline (ffmpeg concat or composition prepend).
- **أرقام / params:** cold open 5-7 s; context 3-6; curiosity 8-12; unique 5-8; teaser 3-5; total <=45 s; cut 1.5-4 s
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/references/hook-principles.md`

#### STORY-03 · إنتاج الفيلم بعد اعتماد اللوحات · Boards-first film production gate · ✅ مُثبت هنا
- **ماذا / what:** Brief -> style guide, palette.json, character sheets, storyboard panels -> user approval -> shot list -> render -> review.
- **كيف / how:** Files: brief.md, boards/palette.json (ink, paper, tones), boards/storyboard.json panels {shot,panel,t,png,action,camera}, shots.json {fps,size,shots[t0,t1]}; refuse to render until approved.
- **أرقام / params:** t0 of shot1=0; each t1=next t0
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9356-produce`

#### STORY-04 · حالات المشهد: مفتوح/مقفل/فتح + وميض · Scene moods (open / locked / unlock) + pulse flash · ✅ مُثبت هنا
- **ماذا / what:** The 3D world tells the UI state: locked cools and slows it, unlocking flashes it brighter and faster; pulse() adds a decaying glow burst.
- **كيف / how:** MOODS tint/fog/glow/speed; per-frame lerp k=.04 toward target; pulse adds up to 3 and decays x0.92/frame.
- **أرقام / params:** open glow .6 speed 1; locked glow .25 speed .55; unlock glow 1.6 speed 1.6
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/crystal-world.js:96` · `kosif-earth-ci-fork/tools/crystal_world.test.mjs`

#### STORY-05 · كتل القفل للاستمرارية · Verbatim lock-block continuity · ✅ مُثبت هنا
- **ماذا / what:** Character, background, world, camera, lighting and style descriptions are frozen as exact text blocks pasted unchanged into every prompt, and the code asserts their presence.
- **كيف / how:** core.repeated(piece, prompts) / lockCheck(text, lock) + ensure() throw if a lock is missing; used by stickman, romance, fitness, vox, food, kinetic.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/core.mjs:6,12` · `fastify-motion-bro/scripts/profiles/stickman.mjs:40-41` · `fastify-motion-bro/docs/PRODUCTION-GATES.md:5`

#### STORY-06 · المخرج الفيروسي بخمس مراحل · Viral five-stage gated director · ✅ مُثبت هنا
- **ماذا / what:** Strict sequence: 5 titles -> 5-line spoken script -> 3 palettes -> 5 poster prompts -> 5 motion prompts, each stage waiting for the user's own reply.
- **كيف / how:** npm run viral -- start | reply 1..5 | reply NEXT | reply 1..3 | reply NEXT | reply NEXT | status | compile | preview-project | approve-render; session in projects/viral-editorial/session.json.
- **أرقام / params:** 5 stages; schema fmb.viral-editorial.v1; target 1080x1920 30 fps
- **الدليل / proof:** `fastify-motion-bro/scripts/viral-editorial.mjs:35-46` · `fastify-motion-bro/scripts/viral-cli.mjs:1-34` · `fastify-motion-bro/skills/viral-editorial/SKILL.md:7-13`

#### STORY-07 · قوالب المواضيع الفيروسية · Viral topic templates (5) · ✅ مُثبت هنا
- **ماذا / what:** Ready topics with hero icons and one-word type per line: Attention Trap; Why Saving Money Feels So Hard; Stop Learning Technology the Wrong Way; Real Reason Some Ideas Spread; Motivation Myth.
- **كيف / how:** TOPICS[i] -> lines, hero[], type[] feed posters, motion prompts and storyboard.
- **أرقام / params:** 5 topics x 5 lines
- **الدليل / proof:** `fastify-motion-bro/scripts/viral-editorial.mjs:10-31`

#### STORY-08 · أجسام استعارية عامة · Generic metaphor hero objects · ✅ مُثبت هنا
- **ماذا / what:** Rotating list of unbranded hero objects for kinetic beats: rocket, chess piece, hourglass, blank glass cube, magnifying glass, paper staircase, generic unbranded interface.
- **كيف / how:** metaphor[(i*5+j)%7] per beat, rendered in the theme's finish with 'no text on the object'.
- **أرقام / params:** 7 objects
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:103,110-111`

#### STORY-09 · ستة أقواس قصصية · Stickman six genre arcs · ✅ مُثبت هنا
- **ماذا / what:** Six premise + five-beat arcs: funny (commute misunderstanding), love (shy small gesture), heart-touching (unseen kindness), plot-twist (bad luck helps), dark comedy (shortcut backfires), surprise (reality flips).
- **كيف / how:** genre 1–6 -> arcs[genre-1]; beats map to setup/build/turn/peak/payoff.
- **أرقام / params:** 6 genres x 5 beats
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/stickman.mjs:9-17`

#### STORY-10 · قوس حب بخمسة مشاهد · Five-beat love arc with paired frames · ✅ مُثبت هنا
- **ماذا / what:** Meeting, Trust, Distance, Return, Promise around a paper crane motif; each beat yields a wide 35 mm establishing frame and an 85 mm emotional close-up plus one narration line.
- **كيف / how:** npm run profile -- start character-romance; answer '<emotion/setting or DEFAULT>'.
- **أرقام / params:** 5 scenes x 2 frames = 10 prompts; 35 mm + 85 mm; 9:16
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/character-romance.mjs:10-29` · `fastify-motion-bro/skills/character-romance/SKILL.md:12`

#### STORY-11 · خوارزمية ملاءمة عدد المقاطع · Clip-count fitting algorithm · ✅ مُثبت هنا
- **ماذا / what:** Maps N requested clips onto real preparation steps: merges adjacent steps when clips are few, adds new macro detail inserts (glossy texture, steam/condensation, plate rotation, final garnish) when many; last clip is always the tasting shot.
- **كيف / how:** pickStages(food, n): assembly=n-1; chunk or extend; never repeat identical action.
- **أرقام / params:** 1–200 clips
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/food-flow.mjs:62-80` · `fastify-motion-bro/tests/production-profiles.test.mjs:48-55`

#### STORY-12 · فيديو الإطلاق · Launch video /brag method · ✅ مُثبت هنا
- **ماذا / what:** Gather product material, 9-question rubric, storyboard, build, deliver with poster and share copy.
- **كيف / how:** python scripts/kmotion.py brag init DIR|URL --tone T --format landscape|vertical|square --duration 20; brag deliver OUT --film film.mp4
- **أرقام / params:** shape hook 2–3 s, reveal 2–4 s, 2–3 highlights, outro 2–4 s; 15–25 s (18–22 ideal); share copy ≤280 chars
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### STORY-13 · موجّه الطلبات وخطة اللقطات المؤقتة · Request router and timed shot plan · ✅ مُثبت هنا
- **ماذا / what:** An Arabic request is routed to an intent (footage_edit, 3d_motion, prompt…) with available commands and ≤4 skills, and a contiguous frame-exact shot plan with a text safe area; 'full pro' status needs verified receipts bound to the request digest.
- **كيف / how:** proplan.plan('مونتاج ريلز عربي مع ترجمة وصوت', mode='pro') → intent footage_edit, commands incl. reel, captions; plan('اعمل فيلم 3d', seconds 11, fps 30, aspect '9:16') → 5 shots, 0..330 frames contiguous, safe_area.text_top_pct 15.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_core.py:42` · `100-superskills/skills/kosif-montage-motion/tests/test_core.py:54`

#### STORY-14 · فيلم قصير صامت بمرشد وقفزة · Wordless cinematic short with a guide and a leap · ✅ مُثبت هنا
- **ماذا / what:** A 12 s silent story beat: hero follows a light (butterfly) through a hostile-but-beautiful world, anticipates an obstacle, leaps, lands, looks back at the audience; title fades early, tagline lands at the end.
- **كيف / how:** Beats: walk 0–4.1 s, notice/crouch 4.1–5.2, leap 5.2–6.9, land 6.9–7.35, walk 7.35–9.7, look back 9.7–12; end line 'FOLLOW THE LIGHT.' from 10.4 s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/README.txt:12` · `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:59`

#### STORY-15 · مخطط اللقطات الحتمي · Deterministic shot planner (kosif.proplan.v1) · ✅ مُثبت هنا
- **ماذا / what:** Turns a task sentence into a 5-beat shot plan (hook, setup, contrast, payoff, end card) with frame-exact cuts, a camera move per shot, audio intent and the commands to run; classifies intent and refuses structural-engineering simulation.
- **كيف / how:** POST /api/plan {task, seconds, fps, aspect, mode} or MCP motion_plan → wbcompat.make_plan(). Intent by regex: prompt (برومبت|prompt|veo|sora|kling), footage_edit (مونتاج|تعديل فيديو|video edit|caption|subtitle|ريل), 3d_motion (ثلاثي|3d|three.js|c4d), else 2d_motion.
- **أرقام / params:** cut ratios 0, .12, .36, .62, .84, 1 of total frames; audio_intent 'impact' on beats 1 and 4, else 'underscore'; seconds 2–600; fps 24/25/30/50/60; aspects 16:9, 9:16, 1:1, 4:5; mode standard|pro; commands footage→[montage,inspect,sheet], motion→[new,frames,render,inspect,sheet]
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:38` · `100-superskills/skills/kosif-montage-motion/tests/test_web.py:71`

#### STORY-16 · خطة محتوى · Content calendar (CSV / XLSX / MD / ICS) · ✅ مُثبت هنا
- **ماذا / what:** Spreads content pillars by weight across platforms and allowed days into a calendar file set that imports as reminders.
- **كيف / how:** python social.py calendar plan.json --out DIR.
- **أرقام / params:** default slots tiktok 21:00, reels 20:00, instagram 13:00, shorts 18:00, youtube 17:00, facebook 19:00, x 12:00, linkedin 09:00, threads 12:00 (heuristic)
- **الدليل / proof:** `kosif-one/tools/kosif-social/SKILL.md` · `kosif-one/tools/kosif-social/examples/plan.json` · `kosif-one/tools/kosif-social/scripts/social.py`

#### STORY-17 · موجه الطلب الواحد · One-request router (16 routes) · ✅ مُثبت هنا
- **ماذا / what:** Normalises an Arabic/English request, ranks routes by keyword evidence, detects add-ons and builds a Jev packet; Jev picks the route; explicit user words win.
- **كيف / how:** python kosif-one/scripts/plan.py --json 'request' | --route ROUTE | --json --main M --extra a,b | --combine M A B.
- **أرقام / params:** routes: reel_from_web, edit_my_footage, talking_reel, motion_2d, cinematic_3d, launch_video, sound_to_film, song_reel, analyze_reference, ai_video_prompts, image_graphics, pixel_redraw, audio_only, ui_web_motion, social_content, not_media (+ mimic_reel in catalog)
- **الدليل / proof:** `kosif-one/tools/kosif-one/SKILL.md` · `kosif-one/tools/kosif-one/scripts/plan.py:39`

#### STORY-18 · كشف الإضافات في الطلب · Request add-on detection · ✅ مُثبت هنا
- **ماذا / what:** Keyword detection of extras the user asked for.
- **كيف / how:** plan.py ADDONS.
- **أرقام / params:** captions, voice, music, vertical 9:16, wide 16:9, review page, poster, privacy face blur, grade, prompts, cloud (claude.ai), social_pack
- **الدليل / proof:** `kosif-one/tools/kosif-one/scripts/plan.py:169`

#### STORY-19 · دمج أكثر من مسار · Combined multi-route pipeline · ✅ مُثبت هنا
- **ماذا / what:** Merges up to 4 routes into one production-ordered pipeline (gather, design, build, finish, gate) with shared steps run once; one ratio, palette and font set across parts.
- **كيف / how:** plan.py --combine MAIN ADDED...; Jev noul p_yes >= 0.6 add, 0.4-0.6 only with a stated reason, < 0.4 drop.
- **أرقام / params:** max 4 routes
- **الدليل / proof:** `kosif-one/tools/kosif-one/SKILL.md`

#### STORY-20 · موجّه الطلب الواحد · KOSIF One request router · ✅ مُثبت هنا
- **ماذا / what:** Keyword planner ranks 16 routes (reel_from_web, edit_my_footage, talking_reel, motion_2d, cinematic_3d, launch_video, sound_to_film, song_reel, mimic_reel, analyze_reference, ai_video_prompts, image_graphics, pixel_redraw, audio_only, ui_web_motion, social_content, not_media) and detects add-ons, bu…
- **كيف / how:** python3 plan.py --json "request" | --route R | --main M --extra a,b | --combine M r1 r2 (max 4 routes)
- **أرقام / params:** ~0.1 s
- **الدليل / proof:** `100-superskills/skills/kosif-one/scripts/plan.py:37` · `100-superskills/skills/kosif-one/SKILL.md`

#### STORY-21 · الإضافات التلقائية · Add-on detection · ✅ مُثبت هنا
- **ماذا / what:** Detects captions, voice, music, vertical 9:16, wide 16:9, review, poster, privacy, grade, prompts, cloud, social_pack from Arabic/English keywords.
- **كيف / how:** plan.py ADDONS dict
- **الدليل / proof:** `100-superskills/skills/kosif-one/scripts/plan.py:169`

#### STORY-22 · خطة محتوى · Content calendar · ✅ مُثبت هنا
- **ماذا / what:** Weighted pillar round-robin across weeks/platforms, deterministic, exports CSV/XLSX/MD/ICS.
- **كيف / how:** python3 social.py calendar plan.json --out dir
- **الدليل / proof:** `100-superskills/skills/kosif-social/scripts/social.py:471`

#### STORY-23 · اكتشاف الذروة · Payoff detection · ✅ مُثبت هنا
- **ماذا / what:** Finds the climax line: after a repeated short line (كافح… كافح) the next full sentence resolves it; in songs the last return of the refrain; else the most stressed full sentence in the last 40 %.
- **كيف / how:** direct.plan / verse.plan
- **أرقام / params:** refrain = line heard ≥2×; payoff line size ×1.22, light sweep, flare; held +2.2 s
- **الدليل / proof:** `kosif-studio/motion/direct.py:116` · `kosif-studio/motion/verse.py:280` · `kosif-studio/tests/test_studio.py:910`

#### STORY-24 · لا معلومات مختلقة · Facts only from the cue (no invented labels) · ✅ مُثبت هنا
- **ماذا / what:** Scene headline is the number the cue said, else its longest word — never a demo value.
- **كيف / how:** audio2motion.head()
- **الدليل / proof:** `kosif-studio/motion/audio2motion.py:49` · `kosif-studio/tests/test_audio2motion.py:43`

#### STORY-25 · مولد البرومبت · Prompt generator · ✅ مُثبت هنا
- **ماذا / what:** Builds a Claude request for a style with aspect/fps/duration/source/brand/audio options.
- **كيف / how:** python3 tools/kosif.py prompt <id> --lang ar --aspect 9:16 --fps 30 --duration 15 --stack auto|remotion|canvas|svg|three.
- **الدليل / proof:** `kosif-tool/tools/kosif.py` · `kosif-tool/templates/claude_request.ar.txt`

#### STORY-26 · ورقة الملاحَظ مقابل المفترض · STYLE.md observed-vs-assumed sheet · ✅ مُثبت هنا
- **ماذا / what:** Style analysis template separating observed (with timestamp evidence) from assumed, plus design tokens for colour, type, line weights, easing, camera, Arabic rules and do-nots.
- **كيف / how:** kosif.py scaffold fills reference/deliverable fields
- **الدليل / proof:** `kosif-tool/templates/STYLE.md`

#### STORY-27 · جدول مشاهد موقّت · PLAN.md timed scene table · ✅ مُثبت هنا
- **ماذا / what:** Scene table with start/end, action, camera, transition, audio cue and assets; rules: no gaps, one clear motion per scene, last scene ends exactly at duration; word-timing table, transitions used, asset licence checklist, render plan.
- **كيف / how:** kosif.py scaffold
- **الدليل / proof:** `kosif-tool/templates/PLAN.md`

#### STORY-28 · قالب الطلب لـ Claude · Claude request template (ar/en) · ✅ مُثبت هنا
- **ماذا / what:** Bilingual request with 15 placeholders (repo,id,name,page,brief_line,playbooks,source,aspect,resolution,fps,duration,stack,lang,brand,audio,notes) and a 5-step workflow (STYLE/PLAN, real motion, RTL, audio master clock, preview then verify).
- **كيف / how:** kosif.py prompt <id> or web/generator.js buildRequest
- **الدليل / proof:** `kosif-tool/templates/claude_request.ar.txt` · `kosif-tool/templates/claude_request.en.txt` · `kosif-tool/templates/claude_request.README.md`

#### STORY-29 · مولد الطلب · kosif.py prompt (request generator) · ✅ مُثبت هنا
- **ماذا / what:** Fills the request template from a style record and options.
- **كيف / how:** python3 tools/kosif.py prompt <id> [--lang ar|en] [--aspect 9:16|16:9|1:1|4:5] [--fps 30] [--duration 15] [--source 'audio voice.mp3'|'video x.mp4'|'text s.md'|none|free] [--stack auto|remotion|canvas|svg|three] [--brand ..] [--audio keep|music|sfx|silent] [--content-lang ar|en|both] [--notes ..] [--out FILE]
- **أرقام / params:** defaults: aspect = record aspect_label or 9:16; duration = record duration_s or 15
- **الدليل / proof:** `kosif-tool/tools/kosif.py:425` · `kosif-tool/tools/kosif.py:452`

#### STORY-30 · المادة المصدرية: none · Source option: none · ✅ مُثبت هنا
- **ماذا / what:** Request phrase for source 'none': write an original narration and timed scene plan.
- **كيف / how:** --source "none <file>"
- **الدليل / proof:** `kosif-tool/tools/kosif.py:59`

#### STORY-31 · المادة المصدرية: audio · Source option: audio · ✅ مُثبت هنا
- **ماذا / what:** Request phrase for source 'audio': audio is master clock; transcribe and sync.
- **كيف / how:** --source "audio <file>"
- **الدليل / proof:** `kosif-tool/tools/kosif.py:59`

#### STORY-32 · المادة المصدرية: video · Source option: video · ✅ مُثبت هنا
- **ماذا / what:** Request phrase for source 'video': study cuts/motion/speech, preserve authorized material.
- **كيف / how:** --source "video <file>"
- **الدليل / proof:** `kosif-tool/tools/kosif.py:59`

#### STORY-33 · المادة المصدرية: text · Source option: text · ✅ مُثبت هنا
- **ماذا / what:** Request phrase for source 'text': script supplied.
- **كيف / how:** --source "text <file>"
- **الدليل / proof:** `kosif-tool/tools/kosif.py:59`

#### STORY-34 · مولد الطلب في الموقع · Website request generator (web/generator.js) · ✅ مُثبت هنا
- **ماذا / what:** ES module mirroring kosif.py prompt for the website: defaultsFor(), buildRequest(), cliCommand() that prints the equivalent CLI line.
- **كيف / how:** import {buildRequest,cliCommand} from 'web/generator.js'
- **الدليل / proof:** `kosif-tool/web/generator.js` · `kosif-tool/tests/test_generator.mjs`

#### STORY-35 · نبرة إطلاق default · Launch tone default · 🟢 جاهز
- **ماذا / what:** Launch-video tone 'default' fixing pacing, transition type and SFX density (from /brag, MIT).
- **كيف / how:** launch.py (kmotion brag init --tone default --format landscape|vertical|square --duration 20)
- **أرقام / params:** see TONES table
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/launch.py:29` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### STORY-36 · نبرة إطلاق polished · Launch tone polished · 🟢 جاهز
- **ماذا / what:** Launch-video tone 'polished' fixing pacing, transition type and SFX density (from /brag, MIT).
- **كيف / how:** launch.py (kmotion brag init --tone polished --format landscape|vertical|square --duration 20)
- **أرقام / params:** see TONES table
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/launch.py:29` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### STORY-37 · نبرة إطلاق yc-parody · Launch tone yc-parody · 🟢 جاهز
- **ماذا / what:** Launch-video tone 'yc-parody' fixing pacing, transition type and SFX density (from /brag, MIT).
- **كيف / how:** launch.py (kmotion brag init --tone yc-parody --format landscape|vertical|square --duration 20)
- **أرقام / params:** see TONES table
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/launch.py:29` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### STORY-38 · نبرة إطلاق chaotic · Launch tone chaotic · 🟢 جاهز
- **ماذا / what:** Launch-video tone 'chaotic' fixing pacing, transition type and SFX density (from /brag, MIT).
- **كيف / how:** launch.py (kmotion brag init --tone chaotic --format landscape|vertical|square --duration 20)
- **أرقام / params:** see TONES table
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/launch.py:29` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### STORY-39 · نبرة إطلاق deadpan · Launch tone deadpan · 🟢 جاهز
- **ماذا / what:** Launch-video tone 'deadpan' fixing pacing, transition type and SFX density (from /brag, MIT).
- **كيف / how:** launch.py (kmotion brag init --tone deadpan --format landscape|vertical|square --duration 20)
- **أرقام / params:** see TONES table
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/launch.py:29` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### STORY-40 · نبرة إطلاق cinematic · Launch tone cinematic · 🟢 جاهز
- **ماذا / what:** Launch-video tone 'cinematic' fixing pacing, transition type and SFX density (from /brag, MIT).
- **كيف / how:** launch.py (kmotion brag init --tone cinematic --format landscape|vertical|square --duration 20)
- **أرقام / params:** see TONES table
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/launch.py:29` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### STORY-41 · نبرة إطلاق app-store · Launch tone app-store · 🟢 جاهز
- **ماذا / what:** Launch-video tone 'app-store' fixing pacing, transition type and SFX density (from /brag, MIT).
- **كيف / how:** launch.py (kmotion brag init --tone app-store --format landscape|vertical|square --duration 20)
- **أرقام / params:** see TONES table
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/launch.py:29` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### STORY-42 · اعتماد اللوحات قبل التصيير · Boards-before-render production gate · 🟢 جاهز
- **ماذا / what:** Brief, style guide, palette, character sheets and storyboard panels are approved by the user before any shot list or render; a digest invalidates approval if boards change.
- **كيف / how:** brief.md -> boards/(style-guide, palette.json, models, storyboard.json) -> user approval -> shots.json {fps,size,shots:[{id,t0,t1,scene,audio}]} -> render -> review against pack.
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9356-produce/SKILL.md`

#### STORY-43 · بناء خطاف يوتيوب · YouTube hook builder (silent vlog) · 🟢 جاهز
- **ماذا / what:** Hook = cold open 5-7 s (1-3 cuts proving the title/thumbnail promise, text in first 1-2 s) + intro 20-30 s: context 3-6 s, curiosity 8-12 s (contrast, cut-before-completion, hidden destination; question without answer), uniqueness 5-8 s, teaser 3-5 s; total ≤45 s; cuts 1.5-4 s; score every scene 0-2…
- **كيف / how:** Build on a duplicated timeline; BGM track locked so music continues; hook audio on own track
- **أرقام / params:** cold 5-7 s; intro 20-30 s; ≤45 s
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/references/hook-principles.md`

#### STORY-44 · اختيار الستايل بالكلمات · Keyword style guesser (no AI) · 🟢 جاهز
- **ماذا / what:** Picks the closest film style from an Arabic request by keyword votes when no AI is reachable; the DNA study can also pick the closest style to a reference by colour distance.
- **كيف / how:** KIT.guess(text): regex vote per style (تقني/برمج -> plotter, قصة/حكاية -> doodle, درس/خطوات -> whiteboard, رياض/فيزي -> chalkboard ...); DNA closest style = bg distance*2 + accent distance*1.2 + aspect/shot-length penalties.
- **الدليل / proof:** `app/public/js/10_studio.js:928` · `app/public/js/10_studio.js:1380`

#### STORY-45 · برومت موشن جاهز لـ Claude Opus · Studio motion prompt builder (5 pillars) · 🟢 جاهز
- **ماذا / what:** Builds a copyable studio-grade prompt for an external Claude session: role, technical context (one HTML file, Canvas 2D, deterministic), duration/fps, second-by-second timeline from captions/scenes, palette/easing, banned list.
- **كيف / how:** buildMotionPrompt(): dims from aspect, 30 fps loop-safe, timeline in 5 chunks, cuts and BPM, entrance spring 0.42/16 rad/s or cubic ease-out 0.25-0.5 s, exits 0.2-0.3 s, stagger 0.06-0.12 s.
- **الدليل / proof:** `app/public/js/00_editor.js:1620`

#### STORY-46 · قصة المقدمة: من الفوضى إلى النظام · Intro story: chaos -> order, goal -> steps -> result · 🟢 جاهز
- **ماذا / what:** Calm-luxury opening where a data Earth turns chaos into order and the copy promises 'start with a goal, end with a verifiable result'; skippable, never replacing the real entry.
- **كيف / how:** Overlay copy: eyebrow 'عالم المحاسبة الذكي · CINEMATIC INTRO', line 'كل شركة عالم مستقل...', CTA 'ادخل KOSIF EARTH ←', skip 'تخطي المقدمة ←'.
- **الدليل / proof:** `kosif-earth-ci-fork/docs/design/KOSIF_EARTH_CINEMATIC_INTRO_20261009_ar.md` · `kosif-earth-ci-fork/unlock.html:158`

#### STORY-47 · استبيان الطرفية التفاعلي · Interactive terminal intake · 🟢 جاهز
- **ماذا / what:** A readline CLI that asks 7 prompts with bracketed defaults and writes project/brief.json, then auto-plans the storyboard.
- **كيف / how:** npm run intake -> scripts/cli.mjs: ask(title, topic, style, aspect, duration, language, voiceover) -> normalizeBrief -> write project/brief.json -> plan().
- **أرقام / params:** defaults: title 'Fastify Motion Bro', topic 'حكاية نجاح', style kinetic, aspect 9:16, 30 s, ar-EG, voiceover none
- **الدليل / proof:** `fastify-motion-bro/scripts/cli.mjs:9-19` · `fastify-motion-bro/package.json:7`

#### STORY-48 · توليد خطة وستايل المشروع · PLAN.md / STYLE.md bootstrap · 🟢 جاهز
- **ماذا / what:** Writes storyboard.json, a STYLE BIBLE stub and a PLAN.md checklist (one checkbox per scene plus preview/approval/QA boxes) from brief.json.
- **كيف / how:** npm run plan -> plan(): reads project/brief.json, writes project/storyboard.json, STYLE.md (language/aspect/style + RTL note), PLAN.md ('- [ ] scene | start–end | text | visual'). Agent must then rewrite creatively.
- **الدليل / proof:** `fastify-motion-bro/scripts/planner.mjs:25-35` · `fastify-motion-bro/project/PLAN.md` · `fastify-motion-bro/project/STYLE.md`

#### STORY-49 · قوس السرد بخمسة أسطر · Five-line explainer narration arc · 🟢 جاهز
- **ماذا / what:** 15–30 s spoken script in five lines: hook -> misconception -> hidden mechanism -> example/contrast -> memorable truth, second person, longest line ≤14 words.
- **كيف / how:** Write one sentence per 6 s scene; agent adapts the 5 sample topics to the user's subject.
- **أرقام / params:** 5 lines; ≤14 words; 30 s
- **الدليل / proof:** `fastify-motion-bro/skills/viral-editorial/SKILL.md:8` · `fastify-motion-bro/docs/VIRAL-EDITORIAL-DNA.md:9`

#### STORY-50 · أساليب البطاقات العشرة · Recut card styles (10) · 🟢 جاهز
- **ماذا / what:** academic (warm paper grid serif, #2557a7), editorial (cream + coral block + big italic quote, #ff3a2d), minimal (pure B/W huge type), spotlight (dark purple gradient glow, #a78bfa), geom (chartreuse #d4ff00 + hot pink + black), whiteboard (Caveat handwriting sketched borders, #ff6b35), audit (manila…
- **كيف / how:** Copy .card[data-card-id='ref-<key>'] from references/styles/<key>.html; combos: interview academic x stack, launch editorial x overlay, data audit x split, social xhs x overlay, tutorial terminal x split.
- **أرقام / params:** 10 styles
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/talking-head-recut/references/DESIGN_INDEX.md` · `kosif-one/vendor/hyperframes/skills/talking-head-recut/references/styles/whiteboard.html` · `kosif-one/vendor/hyperframes/skills/talking-head-recut/references/styles/swiss.html`

#### STORY-51 · من الكلمات إلى اللقطة · Words to shot (Veo vocabulary) · 🟢 جاهز
- **ماذا / what:** Parses phrases like 'low angle tracking shot' or 'slow push-in' into a camera.
- **كيف / how:** K3.shotFromWords(text, opts); 25-entry K3.SHOT_WORDS table; compound modifiers low/high/dutch/handheld.
- **أرقام / params:** phrases: dolly zoom, vertigo, whip, turntable, 360, orbit, arc shot, crane up/down, push, pull back, tracking, bird, top down, low/high angle, dutch, extreme close, close-up, establishing, wide, medium, handheld
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1092` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1097`

#### STORY-52 · قالب التكوين الأساسي · Base composition template (house rules) · 🟢 جاهز
- **ماذا / what:** Starter HyperFrames page with house rules: scene list first, one carrier object, entrances move position+scale+blur from >=0.35 stage width, 2-3 named camera moves, <=8 words on screen, four easings, no wall clock or Math.random.
- **كيف / how:** python motion.py new NAME --seconds S --size WxH --title T (flat template).
- **أرقام / params:** title 110 px weight 800; vignette .4; grain .06; sparkle 40
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/composition.html:23` · `100-superskills/skills/kosif-montage-motion/scripts/motion.py:163`

#### STORY-53 · مونتاج متحدث موجه · Directed talking edit · 🟢 جاهز
- **ماذا / what:** Auto edit of talking clip written to editable edit.js.
- **كيف / how:** direct.py CLIP --name N --size 1080x1920 --accent #E7B65A --fix 'a=b'
- **أرقام / params:** whisper large-v3
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/direct.py`

#### STORY-54 · فيديو إطلاق · Launch readability+brag deliver · 🟢 جاهز
- **ماذا / what:** Gather site material, banned clichés list, rubric, poster+gate delivery.
- **كيف / how:** kmotion brag init URL / deliver OUT --film F
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/launch.py:39`

#### STORY-55 · قوالب بداية Workbench · Workbench starter templates (kinetic, cinematic, montage) · 🟢 جاهز
- **ماذا / what:** Three starter briefs offered by /api/templates: Arabic kinetic letters and geometry, a cinematic 3D glass-product shot, and a rhythm montage that preserves the source footage.
- **كيف / how:** GET /api/templates or MCP motion_templates; feed the 'task' into /api/plan.
- **أرقام / params:** kinetic 'حروف وحركة' #a7e8d0 · cinematic 'لقطة سينمائية' #d3c0fa · montage 'مونتاج بإيقاع' #f5ce91
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:24` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:122`

#### STORY-56 · المراجعة: مؤلف رسالة الإرسال إلى Claude · Review: Send-to-Claude prompt composer · 🟢 جاهز
- **ماذا / what:** Turns every unsent edit and note into one structured prompt: exact edits (apply verbatim), notes with timecode/scene/position/element, motion requests, links to download, scene approval states, and the command sequence to apply, re-render, check and bump the version.
- **كيف / how:** prompt() builds sections '## Edits (apply exactly)', '## Notes', '## Links to download into assets/', '## Scenes', '## Do'; copy to clipboard (fallback select + Ctrl/Cmd+C); also POSTs the feedback (version, lang, text, over, notes, status, links) to /review/NAME/feedback (≤ 2 MB).
- **أرقام / params:** motion props (type 'motion') are routed to notes because only Claude can change motion
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:883` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:906` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:929`

#### STORY-57 · منتصف الليل — فيلم قصير 2.5D · MIDNIGHT — 12 s 2.5D neon-rain short · 🟢 جاهز
- **ماذا / what:** A hand-authored vector short: an orange tabby walks through a rainy neon city at night, crouches, leaps a puddle with splashes, lands, walks on and looks up at a butterfly; title and end cards; no external assets.
- **كيف / how:** examples/cinematic-cat.html: CinematicCat.sceneSVG(t) returns the full SVG per frame; window.render(t) contract and ?capture mode; rendered midnight-cat.mp4 shipped; engine port in projects/midnight_cat.
- **أرقام / params:** 1280×720, 12 s, 24 fps (midnight-cat.mp4: 288 frames); title 'MIDNIGHT' (font-size 43, weight 300, letter-spacing 10) fades out 2.2–3.2 s; end card 'FOLLOW THE LIGHT.' fades in from 10.4 s over 0.7 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:124` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/midnight-cat.mp4`

#### STORY-58 · فحص القصة: هدف ودافع وصراع ورهان · Story lint: GMC+S per beat with agency check · 🟢 جاهز
- **ماذا / what:** Lints a script/reel/ad beat list: every beat needs Goal, Motivation, Conflict and Stakes, a protagonist choice (agency), escalating stakes ending at the highest, ≈20% introspection, an inner-conflict beat, no early relationship resolution, and a climax stating both the outer clash and the inner shif…
- **كيف / how:** echo '{central_conflict, protagonist, beats:[{goal,motivation,conflict,stakes,stakes_level,choice,mode,level,relationship_resolved,stage}], climax:{outer,inner}, plot}' | python3 scripts/omni/story_lint.py (exit 1 when issues).
- **أرقام / params:** score = 100 − 12·issues − 4·warnings; ≥ 3 beats; introspection > 30% warns; relationship resolved before 60% of beats warns; verified on a 3-beat sample → score 100
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/story_lint.py:32` · `100-superskills/skills/kosif-montage-motion/scripts/omni/story_lint.py:57` · `100-superskills/skills/kosif-montage-motion/scripts/omni/story_lint.py:66`

#### STORY-59 · أنواع الصراع المركزي الستة · Six central conflict types · 🟢 جاهز
- **ماذا / what:** The story's central conflict must be one of six forms.
- **كيف / how:** story_lint central_conflict field.
- **أرقام / params:** character vs character · vs society · vs nature · vs technology · vs supernatural · vs self
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/story_lint.py:28`

#### STORY-60 · الحبكات السبع الأساسية · Booker's seven basic plots with Overcoming-the-Monster stages · 🟢 جاهز
- **ماذا / what:** Plot shapes to choose for an ad/reel story; for Overcoming the Monster, beats can be tagged with its six stages and missing stages are flagged.
- **كيف / how:** story_lint plot field + beat 'stage'.
- **أرقام / params:** overcoming the monster (threat and call → preparation/weapon or fatal flaw → initial success → first confrontation and frustration → nightmare stage → escape, victory, reward), rags to riches, the quest, voyage and return, comedy, tragedy, rebirth
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/story_lint.py:24`

#### STORY-61 · ستوريبورد تلقائي من 3 لقطات · Auto 3-shot storyboard (30/40/30) · 🟢 جاهز
- **ماذا / what:** Scaffold writes a shot table splitting the duration into hook, hero and payoff with a camera move per shot.
- **كيف / how:** Generated by ultra_animator new into STORYBOARD.md; edit times/actions then mirror them in render(t).
- **أرقام / params:** Shot 1 0-30% wide establishing + slow dolly-in (hook, title reveal, particle glow); Shot 2 30-70% medium hero + orbit 45 deg (lighting shift); Shot 3 70-100% close-up payoff + crane up/push (climax, CTA, particle burst)
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/ultra_animator.py:104` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/projects/demo_2d/STORYBOARD.md` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/projects/demo_hero/STORYBOARD.md`

#### STORY-62 · مدقق القصة GMC+S · Story lint (GMC+S conflict engine) · 🟢 جاهز
- **ماذا / what:** Checks every beat has goal, motivation, conflict and stakes, the hero drives choices, stakes escalate, introspection stays near 20%, and the climax resolves outer through inner conflict.
- **كيف / how:** kosif_story_lint or stdin to scripts/story_lint.py {central_conflict, protagonist, beats[{goal,motivation,conflict,stakes,stakes_level,choice,mode,level,stage}], climax{outer,inner}, plot}; exit 0 ok / 1 issues.
- **أرقام / params:** score = 100 - 12*issues - 4*warnings; >= 3 beats; introspection warn > 30%; relationship resolved before 60% warns
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-video/scripts/story_lint.py:32` · `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/tools_scripts.py:170`

#### STORY-63 · الحبكات السبع · Booker's seven plots + Overcoming-the-Monster stages · 🟢 جاهز
- **ماذا / what:** Plot archetypes for story ideas, with stage list for one of them checked by story_lint.
- **كيف / how:** Choose a plot; mark beats with 'stage' for story_lint.
- **أرقام / params:** Overcoming the Monster, Rags to Riches, The Quest, Voyage and Return, Comedy, Tragedy, Rebirth; Monster stages: threat & call, preparation, initial success, first confrontation & frustration, nightmare stage, escape/victory/reward
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-video/references/story-conflict.md` · `kosif-one/tools/kosif-omni/skills/kosif-video/scripts/story_lint.py:24`

#### STORY-64 · توليد أفكار بمحفز عشوائي حقيقي · Lateral ideation with real randomness · 🟢 جاهز
- **ماذا / what:** Gives genuinely random stimulus words and provocation prompts so brainstorming escapes predictable LLM ideas.
- **كيف / how:** kosif_ideate {problem, concepts[], n<=30, seed} -> definition checklist, n stimuli with contiguity/similarity/contrast prompts, concept challenges, provocation operators, stage-2 filter.
- **أرقام / params:** n 1-30, reproducible seed
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-think-pro/scripts/ideate.py` · `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/tools_scripts.py:63`

#### STORY-65 · رموز حسب المعنى · Concept-to-symbol motifs · 🟢 جاهز
- **ماذا / what:** A keyword's meaning picks a symbol drawn beside the line; spoken numbers become a counter; symbols are rationed so they never become wallpaper.
- **كيف / how:** verse.concept_of + plan motifs
- **أرقام / params:** 12 concepts: sun, moon, heart, clock, money, trophy, road, question, check, home, rain, light (Arabic roots + English prefixes, prefixes و ف ب ل ال stripped); never same symbol twice in a row, ≥2.5 s apart; numbers always shown (t−0.25 s)
- **الدليل / proof:** `kosif-studio/motion/verse.py:173` · `kosif-studio/motion/verse.py:190` · `kosif-studio/motion/verse.py:322`

#### STORY-66 · قوالب لوحة القصة · Storyboard beat templates (ProPlan) · 🟢 جاهز
- **ماذا / what:** Frame-exact beat lists with camera moves per intent.
- **كيف / how:** proplan.plan → timeline.shots
- **أرقام / params:** 2D: hook/setup/contrast/payoff/end_card at 0/12/36/62/84 % with fast_reveal/slow_push/match_cut/focus_lift/still_hold; 3D: dolly_in/orbit/side_track/push_in/locked; structural: shape/joint/load/break/swap/rank at 0/12/29/47/64/82 % with orbit_schematic/joint_closeup/force_vector_overlay/failure_path…
- **الدليل / proof:** `kosif-studio/motion/proplan.py:84`

#### STORY-67 · تكتيكات الفئات في build.py · Category tactics injection (build.py TACTICS) · 🟢 جاهز
- **ماذا / what:** build.py holds a 14-entry TACTICS dict (product-ui, phone, charts, diagrams, kinetic-type, shapes, particles, characters, photos, music, code, hand-drawn, 3d, ads) whose one-line directives are written into each style's generated SKILL.md alongside links to its category playbooks.
- **كيف / how:** python3 tools/build.py regenerates styles/<id>/SKILL.md; fallback tactic when no category matches.
- **أرقام / params:** 14 categories
- **الدليل / proof:** `kosif-tool/tools/build.py:24-39` · `kosif-tool/tools/build.py:67` · `kosif-tool/catalog/categories.json`

#### STORY-68 · إخراج آلي لفيديو كلام · Directed edit of a talking clip · 📦 بأمر تثبيت
- **ماذا / what:** Builds an editable edit.js: subject-aware camera pushes, one stressed keyword per sentence in large type with a punch and sound accent, numbers as clock rings, keyword as the transition plane at cuts, a payoff with a light sweep and a deliberate dip to black.
- **كيف / how:** python direct.py CLIP.mp4 --name NAME [--size 1080x1920] [--accent #E7B65A] [--render]; then kmotion render projects/NAME --engine studio.
- **أرقام / params:** stress = loudness x length; accent #E7B65A; paper #F5F0E6
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/direct.py` · `kosif-one/tools/kosif-studio/motion/templates/directed.html` · `kosif-one/tools/kosif-studio/motion/projects/premium_edit/index.html` · `kosif-studio/motion/direct.py:231`

#### STORY-69 · مونتاج بصوت دون ظهور الوجه · Faceless voice-over editing · 📦 بأمر تثبيت
- **ماذا / what:** Speaker's face never appears: V1 carries screen recordings and face-free b-roll, voice on A1, cards on V2, captions on V3; verify by sampling frames each second through a face detector.
- **كيف / how:** Face detection on 1 fps frames; replace flagged segments
- **أرقام / params:** 1 fps check
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2460-davinciresolve-story-devtalk/SKILL.md`

#### STORY-70 · حزمة أسلوب من إحصاءات مقاسة · Style pack from measured statistics · 📦 بأمر تثبيت
- **ماذا / what:** Learn a drawn style as numbers (edge straightness, roughness, solid black share, boil, hold mix) with p10/p50/p90 bands, then check new films against them.
- **كيف / how:** learn.py-style analysis: measure traces, set bands from held-out shot splits, prove with negative controls (blur, noise, stripes, contour warp). Never store source geometry.
- **أرقام / params:** p10/p50/p90 bands
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9355-learn-style`

#### STORY-71 · تحويل البصمة لإعدادات · DNA to editor style (no AI) · 📦 بأمر تثبيت
- **ماذا / what:** Turns a measured fingerprint into captions, zoom rhythm, transition, grade and fx settings without a model.
- **كيف / how:** DNA.toStyle: caption position from text band, size = text height*62 (5-14), word mode chunk 1 if > 2.4 changes/s; zoom every = median shot (0.6-8 s), sync beat when > 45% cuts on beat; transition = dominant (flash/dip/whip); grade contrast 0.92+0.9c, saturate 0.75+1.1s; vignette 0.5 for dark refs; grain for bw/warm.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:1385`

#### STORY-72 · تصنيف نوع المحتوى وإعدادات ذكية · Content-type classifier with smart defaults · 📦 بأمر تثبيت
- **ماذا / what:** Locally classifies the upload as talk, song, screen recording, already-edited, silent, podcast audio or music audio and applies fitting defaults once.
- **كيف / how:** classifyContent(): music = silence < 6% and beat conf >= 1.35; screen = >= 55% still frames and < 1 cut/10 s; edited = >= 2.5 cuts/10 s; silent = speech cover < 10% or peak < 0.02. TYPE_DEFAULTS e.g. talk = punch 0.1 sync speech, word chunk 3 pop; music = pulse 0.09 pattern, react, whip, line rise; screen = fit, kenburns 6 s 0.04, clean look vignette 0.1, size 6 box; aud_music = circle viz.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:2789` · `app/public/js/00_editor.js:2803`

#### STORY-73 · ذاكرة ذوق المستخدم · Taste memory from exports · 📦 بأمر تثبيت
- **ماذا / what:** Remembers caption animation, highlight, look and transition of the last 12 exported videos and tells the AI the user's habits when a choice repeats.
- **كيف / how:** tasteKeep on export; tasteTop: a value counts when >= 2 times and >= 60% of keeps; appended to stateBrief as an Arabic line.
- **أرقام / params:** last 12 exports; >= 60%
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:2839` · `app/public/js/00_editor.js:2841`

#### STORY-74 · أوضاع الاستوديو · Studio modes · 📦 بأمر تثبيت
- **ماذا / what:** One Start button with modes: auto, auto montage, reels from long video, product launch film, imitate a video, motion film, captions and camera; helper toggles for Gemini images/voice/transcription, audio enhancement, music, SFX, camera, brand and captions.
- **كيف / how:** UI.MODES and UI.TOOLS (defaults: gstt, aud, music, sfx, camera, captions on; gimg, gvoice, brand off); 60_unify merges everything into one page with collapsible pro tools.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:2896` · `app/public/js/10_studio.js:2907` · `app/public/js/60_unify.js:1`

#### STORY-75 · الإحاطة بالضغط · Overwhelm Surround · 📦 بأمر تثبيت
- **ماذا / what:** Tasks, tabs, pings and bubbles accelerate inward around a calm centre subject to visualise overload.
- **كيف / how:** Install with `npx hyperframes add overwhelm-surround` (copies to compositions/components/overwhelm-surround.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless C…
- **أرقام / params:** count 16; centerLabel You; vars: count=16(8..24); centerLabel=You; intensity=1(0.5..2)
- **تثبيت / install:** `npx hyperframes add overwhelm-surround` (copies to compositions/components/overwhelm-surround`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/overwhelm-surround/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/overwhelm-surround/overwhelm-surround.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/overwhelm-surround.mdx`

#### STORY-76 · تمرير لا نهائي · Scroll Feed · 📦 بأمر تثبيت
- **ماذا / what:** Column of skeleton posts scrolls upward fast with motion trails (doomscroll problem beat).
- **كيف / how:** Install with `npx hyperframes add scroll-feed` (copies to compositions/components/scroll-feed.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame …
- **أرقام / params:** speed doom|frantic; card_count 6; vars: speed=doom[doom|frantic]; card_count=6(4..10); cues=; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add scroll-feed` (copies to compositions/components/scroll-feed`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/scroll-feed/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/scroll-feed/scroll-feed.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/scroll-feed.mdx`

#### STORY-77 · مقدمة صانع محتوى · Blue Sweater Intro Video · 📦 بأمر تثبيت
- **ماذا / what:** Warm 12 s AI-creator intro that resolves into an X follow card for a named real creator handle (avatar + sfx mix declared). [Local copy lacks 1 declared file(s), e.g. assets/sfx/integrated-melodic-tech-mix.wav.]
- **كيف / how:** Install with `npx hyperframes add blue-sweater-intro-video` (copies the full composition to compositions/blue-sweater-intro-video.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 1920x1080; duration 12 s
- **تثبيت / install:** `npx hyperframes add blue-sweater-intro-video` (copies the full composition to compositions/blue-sweater-intro-video`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/blue-sweater-intro-video/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/blue-sweater-intro-video/blue-sweater-intro-video.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/blue-sweater-intro-video.mdx`

#### STORY-78 · موجّه الطلبات إلى عشرة مسارات إنتاج · Router: route a 'make a video' request to one of 10 workflows · 📦 بأمر تثبيت
- **ماذا / what:** A priority table decides the deliverable: Remotion port > slideshow > embedded captions > talking-head overlays > music-driven > short motion graphic > PR explainer > product/site promo > faceless explainer > general-video fallback.
- **كيف / how:** Read /hyperframes SKILL §1 state table (resume BRIEF.md / STORYBOARD.md / hyperframes.json first), then §2 priority table; read only the matched routes/<workflow>.md contract; install with `npx hyperframes skills update <workflow>`.
- **أرقام / params:** 10 routes; narrative workflows up to ~3 min, sweet spot 30-90 s; motion-graphics typically <10 s
- **تثبيت / install:** `npx hyperframes skills update <workflow>``
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/SKILL.md` · `kosif-one/vendor/hyperframes/skills/hyperframes/references/routes/general-video.md` · `kosif-one/vendor/hyperframes/skills/hyperframes/references/routes/motion-graphics.md`

#### STORY-79 · استئناف المشروع من حالته · Project-state resume rules · 📦 بأمر تثبيت
- **ماذا / what:** Before asking anything, the agent inspects existing project files: a BRIEF.md means execute its workflow silently; STORYBOARD.md/hyperframes.json means resume; a specific edit means just edit; `hyperframes timeline --json` lists tracks/clips instead of reading every file.
- **كيف / how:** Apply the first matching row of the state table in /hyperframes SKILL §1; use `npx hyperframes timeline --json` to inspect timelines; bracket edits with project history.
- **تثبيت / install:** `npx hyperframes timeline --json` to inspect timelines`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/SKILL.md`

#### STORY-80 · مقابلة النية بثماني خطوات تنتهي بملف BRIEF.md · Intent interview (8 steps) ending in BRIEF.md · 📦 بأمر تثبيت
- **ماذا / what:** A one-conversation intake: memory/recipes first, triage formed vs unformed, pick route, pitch round if unformed, must-have questions with a recommended default and a receipt, two orthogonal run-shape questions, one capability offer, then an integration check and a confirmed summary written to BRIEF.…
- **كيف / how:** Follow intent-interview.md steps 1-8; read prefs via `node <media-use>/scripts/prefs.mjs get --hyperframes <root> --json` and recipes via `recipe.mjs list`; write BRIEF.md frontmatter (workflow, flow, storyboard, message, destination, aspect, language, audience, length, angle).
- **أرقام / params:** flow = automation|companion; storyboard = yes|no; mode derived: companion->collaborative, automation+yes->collaborative, automation+no->autonomous
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/intent-interview.md` · `kosif-one/vendor/hyperframes/skills/hyperframes/references/brief-contract.md` · `kosif-one/vendor/hyperframes/skills/hyperframes/references/brief-format.md`

#### STORY-81 · جولة العروض: خمسة مفاهيم متباينة · Pitch round: five divergent concepts · 📦 بأمر تثبيت
- **ماذا / what:** For an unformed request the agent samples five genuinely different concepts (at least two from the unusual tail of ideas), presents all before recommending one; each pitch names the capability it rides.
- **كيف / how:** pitch-round.md: internal sampling gate always; present round; user may pick, mix or redirect; autonomous runs keep the gate internally and pick.
- **أرقام / params:** 5 pitches, >=2 tail concepts
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/pitch-round.md`

#### STORY-82 · خريطة القرارات للمستخدم المبتدئ · Decision map for novice users · 📦 بأمر تثبيت
- **ماذا / what:** When a user says they know nothing about video, offer only 2-3 decision surfaces (where it plays, how long, how it should feel), each with 2-4 plain options and a marked default.
- **كيف / how:** pitch-round.md § decision map; every unanswered surface becomes a stated default.
- **أرقام / params:** 2-3 surfaces x 2-4 options
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/pitch-round.md`

#### STORY-83 · قائمة القدرات بلغة المستخدم · Capability menu as pitch vocabulary · 📦 بأمر تثبيت
- **ماذا / what:** A single table maps each capability (design spec, website capture, beat analysis, blueprints, media, generative video, transcription, transcript-cut, overlays, real maps, Figma, registry blocks, transitions, user media, publish) to a plain-language line and an entry command.
- **كيف / how:** capability-menu.md: recommend at most 1-2 rows traced to the brief, one labeled challenger with a named cost; borrow other workflows' scripts by absolute path after `skills update <workflow>`.
- **أرقام / params:** 15 capability rows
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/capability-menu.md`

#### STORY-84 · استعارة عدسات الأنواع · Genre lenses borrowing · 📦 بأمر تثبيت
- **ماذا / what:** Freeform pieces borrow the taste docs (story-design, visual-design, motion-language, cut-catalog) of the workflow they resemble: product promo, topic explainer, or code walkthrough; never their machinery.
- **كيف / how:** Read <workflow>/references/*.md of product-launch-video, faceless-explainer (neutral default), or pr-to-video (+code-vocabulary.md).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/capability-menu.md`

#### STORY-85 · صيغة لوحة القصة STORYBOARD.md · STORYBOARD.md format · 📦 بأمر تثبيت
- **ماذا / what:** Markdown with global frontmatter (format, duration, message, arc, audience, mode) and per-frame sections (status, src, duration, transition_in, scene, voiceover, poster, extra keys) parsed into a manifest.
- **كيف / how:** Write per storyboard-format.md; arc example 'Hook -> Problem -> Solution -> Proof -> CTA'.
- **أرقام / params:** format 1920x1080; duration e.g. 22s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/storyboard-format.md`

#### STORY-86 · حفظ الوصفة وتذكر التفضيلات · Recipe freeze and preference memory · 📦 بأمر تثبيت
- **ماذا / what:** An approved run is frozen as a named recipe (design spec, storyboard skeleton with content blanked, brief skeleton, confirmed values); preferences (preset, voice, caption identity) promote to recommended defaults next time.
- **كيف / how:** `node <media-use>/scripts/recipe.mjs freeze --name <name>`; `recipe.mjs list`; `prefs.mjs get --hyperframes <root> --json`.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/review-loop.md` · `kosif-one/vendor/hyperframes/skills/media-use/scripts/recipe.mjs` · `kosif-one/vendor/hyperframes/skills/media-use/scripts/prefs.mjs`

#### STORY-87 · مخطط مشهد: الإغراق والإحاطة · Blueprint: Overwhelm surround · 📦 بأمر تثبيت
- **ماذا / what:** Surfaces accumulate, density icons scatter, the center morphs into the viewer's avatar, elements close in from all sides; clutter-shove-to-question variant.
- **كيف / how:** Pick from hyperframes-animation/blueprints-index.md by role, then read hyperframes-animation/blueprints/overwhelm-surround.md for the multi-phase recipe; cite blueprint id per beat in the storyboard.
- **أرقام / params:** duration 6-9 s (~10 s variant)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/overwhelm-surround.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`

#### STORY-88 · الأسلوب الافتراضي وقائمة العادات الكسولة · House style and lazy-default checklist · 📦 بأمر تثبيت
- **ماذا / what:** Interpret the prompt into a concept; question AI design tells (gradient text, left accent stripes, cyan/purple neon, pure #000/#fff, identical card grids, everything centered, banned fonts); one bg + one fg + one accent declared before HTML; 2-5 ambient decoratives per scene.
- **كيف / how:** references/house-style.md; decoratives: radial glows, ghost text 3-8% (video 12-25%), hairlines, grain, grids, thematic motifs, all slowly breathing.
- **أرقام / params:** motion 0.3-0.6 s; headlines 700-900 / body 300-400; 60px+ / 20px+
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/house-style.md`

#### STORY-89 · الأساليب البصرية الثمانية المسماة · Named visual styles (8 designer-inspired) · 📦 بأمر تثبيت
- **ماذا / what:** Swiss Pulse (clinical; SaaS/data; Cinematic Zoom or SDF Iris), Velvet Standard (premium; Cross-Warp Morph), Deconstructed (raw industrial; Glitch/Whip Pan), Maximalist Type (loud launches; Ridged Burn), Data Drift (AI futuristic; Gravitational Lens/Domain Warp), Soft Signal (warm wellness; Thermal D…
- **كيف / how:** references/visual-styles.md sections 1-8 + mood->style table + custom style recipe.
- **أرقام / params:** 8 styles
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/visual-styles.md`

#### STORY-90 · إخراج كل لقطة (الإيقاع) · Beat direction per scene · 📦 بأمر تثبيت
- **ماذا / what:** Each beat gets concept, mood direction, animation choreography, transition, >=2 depth layers (BG/MG/FG) and SFX cues; rhythm is declared up front (e.g. fast-fast-SLOW-fast-SHADER-hold) and derived from story and brand.
- **كيف / how:** references/beat-direction.md; one strong feature may beat three in 15 s.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/beat-direction.md`

#### STORY-91 · عمود القصة: القيمة قبل الدليل · Story spine: value-first doctrine · 📦 بأمر تثبيت
- **ماذا / what:** Hook speaks the viewer's language; reverse iceberg puts value before evidence; storyboard is a proposal ('This video tells [audience] that [message]'); visuals point back to the source.
- **كيف / how:** references/story-spine.md.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/story-spine.md`

#### STORY-92 · توسيع الطلب المفتوح · Prompt expansion for open-ended asks · 📦 بأمر تثبيت
- **ماذا / what:** A structured expansion step always runs on open prompts to generate real content and a concept before design.
- **كيف / how:** references/prompt-expansion.md.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/prompt-expansion.md`

#### STORY-93 · وصفة لوحة القصة وصفحة المراجعة · Storyboard recipe and storyboard.html sheet · 📦 بأمر تثبيت
- **ماذا / what:** Open with decisions, write the beat list, draw storyboard.html cells (static styled sketches at the key moment), one review round.
- **كيف / how:** references/storyboard-recipe.md.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/storyboard-recipe.md`

#### STORY-94 · جدول الاستجابة قبل البناء · Studio talk-before-build response table · 📦 بأمر تثبيت
- **ماذا / what:** Named change -> make it; felt note -> find the measurable cause, change it and explain; question -> answer only; 'hold' -> change nothing; idea -> propose and add to plan; new film -> plan it; approval -> build.
- **كيف / how:** hyperframes-studio SKILL § 0.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-studio/SKILL.md`

#### STORY-95 · قواعد الاستمرارية لأفلام المنتجات · Product film continuity rules · 📦 بأمر تثبيت
- **ماذا / what:** Ask for real screen recordings; one world continues across beats; cursors/scrolled content must stay consistent across cuts; close on the command or address with the logo landing in still-moving footage; state runtime at every version.
- **كيف / how:** hyperframes-studio SKILL §5.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-studio/SKILL.md`

#### STORY-96 · مسح فرص تحسين الوسائط · Media opportunity pass · 📦 بأمر تثبيت
- **ماذا / what:** One grounded scan per project, one consolidated ask: script without voice -> TTS; emoji-as-icon -> real icons; placeholder image -> better image/upscale; silent cuts -> transition SFX; >10 s without music -> BGM; bad exposure -> corrective grade; flat photos -> one treatment; static reveal -> seek-s…
- **كيف / how:** media-use SKILL § Be proactive; user approves all/some/none.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/SKILL.md`

#### STORY-97 · ذاكرة التفضيلات والوصفات · Preferences and recipe memory store · 📦 بأمر تثبيت
- **ماذا / what:** Per-project .media store with promotion rules turning confirmed choices (preset, voice, caption identity) into next-run defaults.
- **كيف / how:** scripts/prefs.mjs, scripts/recipe.mjs, lib/prefs-store.mjs, lib/recipe-store.mjs.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/references/memory.md` · `kosif-one/vendor/hyperframes/skills/media-use/scripts/lib/prefs-store.mjs` · `kosif-one/vendor/hyperframes/skills/media-use/scripts/lib/recipe-store.mjs`

#### STORY-98 · كتالوج اتجاهات الإخراج للترجمة · Caption direction catalog (10 film references) · 📦 بأمر تثبيت
- **ماذا / what:** documentary-dignified (Morris/Frontline), cinematic-noir (Kyle Cooper Se7en), tech-keynote-confident (Apple), lyrical-poem-on-wall, high-energy-vlog, chapter-card (Wes Anderson), investigative-typewriter, k-pop-lyric, broadcast-dignified (BBC/NYT), conference-lower-third-killer.
- **كيف / how:** references/direction-catalog.md + classification matrix (tone x shot x platform).
- **أرقام / params:** 10 directions
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/references/direction-catalog.md`

#### STORY-99 · مسار الموشن جرافيك القصير · Motion-graphics workflow (asset-first, autonomous) · 📦 بأمر تثبيت
- **ماذا / what:** Short unnarrated design-led graphic (<10 s, up to ~30 s): init -> director subagent plans (search? category, asset_needs) -> media-use resolve -> director designs shot-plan.json -> builder composes reuse-first -> lint/check/snapshots -> preview approval -> render MP4 or transparent overlay.
- **كيف / how:** Follow motion-graphics/SKILL.md; agents/director.md, agents/builder.md, agents/finalize.md; schema references/shot-plan-ir.md; never init in workspace root.
- **أرقام / params:** <10 s typical
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/motion-graphics/SKILL.md` · `kosif-one/vendor/hyperframes/skills/motion-graphics/references/shot-plan-ir.md` · `kosif-one/vendor/hyperframes/skills/motion-graphics/agents/director.md`

#### STORY-100 · بنى فيديو الشرح الأربع · Explainer structures (4) · 📦 بأمر تثبيت
- **ماذا / what:** concept-explainer (name concept -> mechanism layer by layer -> implication), how-to-process (3-6 steps on one visual stage), listicle (hook -> N co-equal items -> wrap), story-explainer (setup -> tension -> turn -> resolution -> lesson); register matched to frame.md mood.
- **كيف / how:** faceless-explainer/references/story-design.md § Step 3 method; type enum hook/pain_point/product_intro/feature_showcase/benefit_highlight/social_proof/branding/cta.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/faceless-explainer/references/story-design.md`

#### STORY-101 · استراتيجيات الخطاف الافتتاحي · Hook strategies · 📦 بأمر تثبيت
- **ماذا / what:** Shocking statistic, rhetorical question, counterintuitive claim, pain validation, visceral metaphor (explainers); for PRs also concept announcement, before/after teaser, stakes/consequence.
- **كيف / how:** Pick one per video in the first 3-5 s (story-design.md § Hook strategy).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/faceless-explainer/references/story-design.md` · `kosif-one/vendor/hyperframes/skills/pr-to-video/references/story-design.md`

#### STORY-102 · أقواس سرد الإطلاق الخمسة · Launch narrative arcs (5) · 📦 بأمر تثبيت
- **ماذا / what:** PAS (hook -> pain -> agitation -> solution tease -> product -> proof -> CTA), Future Pacing (imagine -> name -> remove pain -> mechanism -> outcome -> CTA), Demo Loop (question -> intro -> demo 1 -> demo 2 -> trust -> CTA), BAB (before -> after tease -> bridge -> steps -> wow -> CTA), Feature-Benefi…
- **كيف / how:** product-launch-video/references/story-design.md arc table.
- **أرقام / params:** 5 arcs
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/product-launch-video/references/story-design.md`

#### STORY-103 · الفيديو العام ووضع المرافقة · General-video fallback and companion mode · 📦 بأمر تثبيت
- **ماذا / what:** Fallback for any other build (title card, brand/sizzle reel, montage, static loop, footage remix, freeform, any length) and companion co-creation: arrive as the director with the ceiling treatment, offer capability-menu rows as triggers, record accepted capabilities in BRIEF.md; inline builds beat s…
- **كيف / how:** general-video/SKILL.md §3-7; frame-packets.mjs for dispatch at scale.
- **أرقام / params:** 5 short scenes inline ~9 min (measured claim)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/general-video/SKILL.md` · `kosif-one/vendor/hyperframes/skills/general-video/scripts/frame-packets.test.mjs`

#### STORY-104 · المونتاج الموجّه التلقائي · direct auto-directed talking edit · 📦 بأمر تثبيت
- **ماذا / what:** Plans a directed edit of a talking clip: subject push, face→keyword→caption stack, end-focus keyword per sentence, number→clock ring, cut word as transition plane, payoff by rhetoric then dip to black.
- **كيف / how:** python scripts/kmotion.py direct CLIP.mp4 --name NAME --credit 'insta: handle' [--fix 'a=b;c=d']
- **أرقام / params:** payoff fallback: most stressed sentence in last 40%
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### STORY-105 · محاكاة ريل · mimic reel rebuild · 📦 بأمر تثبيت
- **ماذا / what:** Rebuild someone's reel shot for shot with new Pinterest footage: study, fill, fetch pool, match, build; compare.json gate.
- **كيف / how:** python scripts/kmotion.py mimic (see references/mimic.md)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### STORY-106 · توقيت سردي على مراحل · Stage-band narrative timing · 📦 بأمر تثبيت
- **ماذا / what:** A short film is cut into named stage bands that drive chips, captions, camera and effects together: SHAPE → JOINT → LOAD → BREAK → SWAP → RANK.
- **كيف / how:** B = {joint .85, load 1.65, brk 2.55, swap 3.35, rank 4.15, end 5.0}; T_BREAK 2.66; stage = findIndex(t ≥ stage_i); load ramps easeInOut to 3.0× then back to 1.0×; lab uses 0/3/9.5/13/16/18 s over 20 s.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:8` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:78` · `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/src/main.js:40`

#### STORY-107 · وصفة فيلم الخمس ثوانٍ · Five-second film recipe (3 beats, ≤8 words) · 📦 بأمر تثبيت
- **ماذا / what:** A complete 5 s brand sting: one idea, a drawn carrier, at most 8 words, one slow push, an iris flood to the brand.
- **كيف / how:** beat 1 0–1.2 s: ring draws (0.9 s) + halo + lines rise; beat 2 1.2–3.6 s: push 1→1.09 and slow ring rotation; beat 3 3.6–5 s: words leave, ring → iris, gold flood + flash, brand words reveal; 1080×1920 30 fps.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:31` · `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:65`

#### STORY-108 · بنية ريلز تحفيزي صوتي · Motivational voice reel arc · 📦 بأمر تثبيت
- **ماذا / what:** A 20 s spoken motivational reel structured as hook (frozen dim frame, word slams) → claim with one motif per idea → pressure (punches, shake, hard stop) → lift (warmth returns, YOU in accent) → word-transition to a wide shot → build (rays, push) → payoff (light sweep on the action word) → closing mo…
- **كيف / how:** Time map: 0 hook, 1.56 clock, 3.28 dream, 5.22 weight, 7.24 car, 9.5 pressure, 11.3 lift, 13.14 word transition, 14.62 time drain, 16.02 build, 17.26 payoff, 18.42 close, 20.06 dip.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:188` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:287`

#### STORY-109 · شوريل بأداة واحدة تعبر كل اللقطات · One-device showreel (a dot through every shot) · 📦 بأمر تثبيت
- **ماذا / what:** A product showreel where one red dot is the continuous device: it lands, becomes a button, a bar, rides a spring curve, becomes a caret's period, opens an iris onto footage, the footage becomes a card, everything implodes into it and it becomes the logo's full stop.
- **كيف / how:** All on a 120 BPM grid over 15 s at 60 fps; Arabic claims 'كل إطار برنامج', 'نابض، لا منحنى', 'الإطار دالة في الزمن', 'واقعية تُكتب بالكود'.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:66`

#### STORY-110 · فيلم دروس الكتب · Book-lesson film (painting and photography rules as code) · 📦 بأمر تثبيت
- **ماذا / what:** A shot is designed to demonstrate named lessons: Gurney's aerial perspective, colour corona, warm/cool shadow rule and night vision, a night-photography 1 s tripod exposure, Veo shot language, complementary colour theory.
- **كيف / how:** Annotate the scene file header with the lessons; implement each with its kit primitive (aerialPerspective, bloom radius, skyBounce, makeLookPass night, --stack lighten, harmony).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:1`

#### STORY-111 · تكامل: Motion Director skill · Integration: Motion Director skill · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### STORY-112 · تكامل: KOSIF Motion Director original · Integration: KOSIF Motion Director original · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### STORY-113 · ستايل مونتاج الغربة السينمائي · Ghorba cinematic Pinterest montage (style) · 📦 بأمر تثبيت
- **ماذا / what:** A 48 s vertical nostalgic montage about living abroad: 7 found vertical clips (plane window, airport, night drive, rain on glass, walking in rain, family/memory, sunrise from plane) under the original song, muted desaturated grade, centred Arabic title + subtitle in the lower third, small KOSIF MOTI…
- **كيف / how:** FFmpeg pipeline: per-shot scale/crop to 9:16, eq grade, burned ASS titles, concat demuxer, mux the untouched song with AAC; QA with ffprobe; see the individual Ghorba atoms.
- **أرقام / params:** 540x960 or 720x1280, 24 fps, 48.0 s, 7 shots 5.0-9.6 s, contrast 1.06-1.08, saturation 0.86-0.95
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:19` · `kosif-one/projects/KOSIF_Motion_Ghorba/tools/render_ghorba_preview.py:23` · `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_MOTION_GUIDE_REUSE_AR.md`

#### STORY-114 · دليل إعادة المونتاج ١٨ خطوة · Montage reuse runbook (18 steps) · 📦 بأمر تثبيت
- **ماذا / what:** A repeatable checklist for turning any song or video into a vertical meaning-matched montage: inspect, transcribe with review, pitch 2-3 scene ideas, source new footage, triage, beat/meaning shot list, Arabic motion type in safe zones, live progress, QA, honest report.
- **كيف / how:** Follow MONTAGE_REUSE_RUNBOOK_AR.md; commands: kmotion.py fetch --list URL, kmotion.py fetch URL --only video --max 1, kmotion.py montage cut ... --ratio 9:16 --grade blue_hour, kmotion.py songreel analyze track.mp3 --seconds 45; fallback yt-dlp -f 'b[ext=mp4]/b'.
- **أرقام / params:** advice: 20-35 clean vertical shots for a full song; exports 9:16 and 16:9 on request
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/MONTAGE_REUSE_RUNBOOK_AR.md` · `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_MOTION_GUIDE_REUSE_AR.md`

#### STORY-115 · الأهرامات بنسبها الحقيقية · Heritage-accurate pyramids rule · 📦 بأمر تثبيت
- **ماذا / what:** Real monuments are kept untouched and proportional: Khufu, Khafre, Menkaure at 1:5 scale in their real diagonal plus queens' pyramids; futurism is added around them, never on them.
- **كيف / how:** ConeGeometry(base/sqrt2, h, 4) rotated 45 degrees, flatShading stone #E3BC86; sizes (46,29.2), (43,27.2), (20.6,13), queens (9,5.6).
- **أرقام / params:** scale 1:5; SW diagonal offsets (0,0), (-64,52), (-112,118)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html:218-221` · `kosif-one/projects/egypt-2120-animation/README.md`

#### STORY-116 · بنية الخطاف للفيديو القصير · Short-video hook structure (concept in 1 s, one fact per shot, one CTA) · 📦 بأمر تثبيت
- **ماذا / what:** Open on the concept within a second with a question, let each shot add one new fact with a numbered chip (01-04), end with one line call and a disclaimer.
- **كيف / how:** Hook 0-2.6 s ('مصر ٢١٢٠' + 'كيف سنعيش بعد مئة عام؟'), chips '٠١ · الجيزة'..., end card 'المستقبل يُبنى اليوم' + 'تصوّر فني تخيّلي'.
- **أرقام / params:** 18 s total; captions start 0.25 s after each cut and leave 0.3 s before the next
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html:448-453` · `kosif-one/projects/egypt-2120-animation/README.md`

#### STORY-117 · ستايل ريل دعاء الجمعة · Friday dua aesthetic reel (style) · 📦 بأمر تثبيت
- **ماذا / what:** A 28.2 s vertical Friday supplication reel: cozy aesthetic B-roll (incense smoke, Quran with candles and tasbih, flowers in vases, roses, coffee), one Diwani-script line per shot in cream with a black stroke centred at 47.5% height, and a fade through black at every boundary (~every 2.5 s) over the …
- **كيف / how:** Rebuilt with the kosif-mimic workflow (study -> fonts -> layer -> queries -> fetch -> match -> build -> compare).
- **أرقام / params:** 1080x1920, 30 fps, 11 shots, 10 fadeblack transitions 0.70-0.80 s, text 135 px #fdfbf3 stroke 7 #000000
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/mimic-jumuah/study/mimic.json` · `kosif-one/projects/mimic-jumuah/study/mimic.timeline.json` · `kosif-one/projects/mimic-jumuah/جمعة-محاكاة.raw.timeline.json`

#### STORY-118 · ستايل دعاء الخميس من الليل للفجر · Thursday dua night-to-dawn mihrab (style) · 📦 بأمر تثبيت
- **ماذا / what:** A 24.7 s vertical supplication animation: a gold pen draws a mihrab arch and an eight-point rosette, a mosque silhouette with lit windows, two swaying lanterns, falling rose petals and gold dust, while the sky turns from deep night to golden morning and the sun rises as the story object; each line o…
- **كيف / how:** GSAP 3.15 timeline + KOSIF Motion Kit v3 inside a HyperFrames composition (1080x1920, 30 fps) with the voice track; downbeats from a channels JSON.
- **أرقام / params:** AmiriB 84/104/130 px lines #fff6e2/#ffd77a/#ffe39a, Aldhabi 170 px day name #ffe7a8, sky #0b1033 -> #34509a/#f2a079/#ffd890
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html`

#### STORY-119 · الشمس كعنصر حامل للقصة · Sun as the story carrier object · 📦 بأمر تثبيت
- **ماذا / what:** One visual object embodies the text: the sun climbs slowly through the film and, on the line 'اللهم لا تغرب شمس هذا اليوم', lifts with a heavy spring into the rosette with a flash, scale pop and ray brighten.
- **كيف / how:** sunMove y 120 -> -300 over 10.9 s (E.cam), then -940 in 1.9 s with M.spring('heavy') at 10.99 s, then creep to -975; sun scale 1 -> 1.18 (0.5 s) -> 1; rays opacity .95 -> .6; M.flash peak .55 dur .9.
- **أرقام / params:** key line at 10.99 s = downbeat 10.987
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html:51-56` · `kosif-one/projects/thursday-dua-animation/source/index.html:153-161` · `kosif-one/projects/thursday-dua-animation/source/index.html:211-215`

#### STORY-120 · ستايل تعريفين للنجاح · Two definitions of success explainer (style) · 📦 بأمر تثبيت
- **ماذا / what:** A 47 s vertical talking-voice explainer cut on AI-generated cinematic plates: a question with a giant outlined question mark, a hall of 1,000 people, a cold-blue money world that drains to grey on 'unhappy', a warm golden joy world, a split screen of the two mindsets, and a payoff counter to 600 def…
- **كيف / how:** GSAP + Motion Kit v3 composition with three text levels, synthesised score at 90 BPM D minor (vol .42) under the voice and designed SFX cues.
- **أرقام / params:** 1080x1920, 30 fps, 47 s; base #05070b; gold #f5c97a, cold #7fd0ff, alarm #ff6b6b/#ff5a5a, cream #e9dcc4
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html`

#### STORY-121 · دراسة فيلم مرجعي · Reference film study -> style guide · 📦 بأمر تثبيت
- **ماذا / what:** Measures a reference's cuts, shot lengths, first change, motion energy, stillness and palette and writes style_guide.md: borrow the grammar, never the content.
- **كيف / how:** python motion.py study REFERENCE.mp4 --out DIR.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/qa.py:1` · `kosif-one/tools/kosif-studio/motion/references/x-trend-2026.md`

#### STORY-122 · من فيديو كلام إلى ريل جاهز · Talking clip -> finished vertical reel · 📦 بأمر تثبيت
- **ماذا / what:** One command: transcribe + erase burned captions in parallel, restore and reframe, voice chain, music only if none, karaoke captions, -14 LUFS, delivery gate.
- **كيف / how:** python reel.py CLIP.mp4 --out FINAL.mp4 [--size 1080x1920] [--model large-v3] [--music auto|none|score.wav] [--style reels|cinema|punchy] [--credit ...].
- **أرقام / params:** auto underscore: 90 BPM D minor pad+bass; writes FINAL.srt + FINAL.reel.json
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/reel.py:1`

#### STORY-123 · محاكاة فيديو مرجعي بلقطات جديدة · Reference remake pipeline (mimic) · 📦 بأمر تثبيت
- **ماذا / what:** Remakes an uploaded reference with new footage while copying the original audio untouched, the same texts/fonts/positions/colours/shadows, the measured text animations, the transitions with their timing, and the colour mood.
- **كيف / how:** mm_analyze.analyze('REF.mp4','work') -> spec.json + sheets; fill exact texts; mm_fonts.match; assign shots[i].replacement {path, in, fit, focus}; mm_build.build('work', preview=True) then full.
- **أرقام / params:** keeps exact frame count, fps, size; one H.264 encode copying the reference audio stream
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/SKILL.md` · `kosif-one/tools/kosif-mimic/scripts/mm_analyze.py` · `kosif-one/tools/kosif-mimic/scripts/mm_build.py`

#### STORY-124 · قالب مختبر المنتج · Product-lab 3D template (KOSIF LAB 01) · 📦 بأمر تثبيت
- **ماذا / what:** 20 s rabbit × lion lab film: plush pair forms from wireframe, one lens walks the circle stopping at ear/eye/mane/tail, HUD stages SHAPE→JOINT→LOAD→BREAK→SWAP→RANK, ears flop, tail swaps to a lion tuft, deliberate dip to ink.
- **كيف / how:** python3 motion.py new NAME --lab (assumed) -> templates/lab/index.html + main.js on three-kit.bundle + lab-kit.
- **أرقام / params:** tone neutral exposure 1.0; fov 30; stops at 0/3/6.5/9.5/13/16/18 s; callout bilingual labels; dip #0f1512 .6 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/templates/lab/index.html` · `kosif-studio/motion/templates/lab/main.js`

#### STORY-125 · مشهد: فتاة تقاتل تنيناً تحت القمر · Showcase: girl vs dragon under the moon · 📦 بأمر تثبيت
- **ماذا / what:** A 17-step fantasy painting program: gradient night sky, 280 stars, moon, cloud layers, two mountain ridges with a castle, fog, a winged dragon breathing fire onto a shield, a girl with cape and glowing sword, embers and a final grade.
- **كيف / how:** python studio.py dragon_girl (or --render ... --scale 3.2).
- **أرقام / params:** sky stops #05071a #11133a #2e1a48 #5c2440 #8c3a2e #1a0c10; lights moon (cool), fire (warm), sword (cyan)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/scenes/dragon_girl.py:1` · `kosif-studio/scenes/dragon_girl.py:129` · `kosif-studio/out/dragon_girl_1200x800.png`

#### STORY-126 · مشهد: الحوت والتنين في العاصفة · Showcase: whale breaching vs dragon in a storm · 📦 بأمر تثبيت
- **ماذا / what:** The realism showcase: storm sky with noise, relief-lit clouds, lightning, a water() sea with foam, a relief-shaded dragon with scales, a humpback built in its own frame (pleats, tubercles, pectoral fin) with SSS skin, fire meeting spray in steam, rain, embers and a full camera stack; passes judge.py…
- **كيف / how:** python studio.py whale_dragon; tested by test_the_whale_scene_passes_the_gate.
- **أرقام / params:** letterbox 62/738; LIGHTS cold/warm/ambient; ROLLOFF 1.0
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/scenes/whale_dragon.py:1` · `kosif-studio/out/whale_dragon_1200x800.png` · `kosif-studio/out/whale_dragon_3840x2560.png`

#### STORY-127 · مشهد: بطة شجاعة أمام تنين عملاق · Showcase: brave duck charging a giant dragon · 📦 بأمر تثبيت
- **ماذا / what:** Low-angle storm scene: moon behind clouds, lightning, volcanic glow, wet rocks with dual rims, a giant dragon with fire frozen a beat before impact, a white duck with feather-by-feather spread wing, splashing feet, rain far/near, embers, grade and letterbox.
- **كيف / how:** python studio.py duck_dragon.
- **أرقام / params:** grade #0a1426/#ffe2c4; duck rims #ffa04a, #ff6a2a, #bcd2f5
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/scenes/duck_dragon.py:1` · `kosif-studio/out/duck_dragon_1200x800.png`

#### STORY-128 · العنصر المتنقل (نقطة حمراء) · Travelling device (one red dot) · 📦 بأمر تثبيت
- **ماذا / what:** One object carried through every shot of a showreel — it lands, pulses on beats, becomes a button, rides a drawn spring curve, becomes a caret's period, opens the iris and ends as the lockup's full stop.
- **كيف / how:** M.sampled path ride (60 samples), M.beats(120) clock, squash on landing
- **أرقام / params:** dot #E4342F on #0F1211; pulses 1.25/1.2 scale (0.06 s out, 0.22 s settle); 15 s 1080p60
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/showreel/index.html:66` · `kosif-studio/out/kosif_motion_showreel.mp4`

#### STORY-129 · قوس المونتاج التحفيزي · Talking-head arc template (FINAL_EDIT) · 📦 بأمر تثبيت
- **ماذا / what:** A proven arc for a motivational talking clip: hook micro-freeze → realisation graphic → dream warmth → micro-graphic examples (~1.2 s each) → pressure punches → lift in accent colour → giant word as transition into the wide → time drains → light from above → payoff alone with sweep → closing motif →…
- **كيف / how:** Hand-directed composition on motion-kit; see EDIT_NOTES
- **أرقام / params:** 20.57 s 1080×1920 30 fps; −14.4 LUFS; TP −2.7 dBTP
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/out/FINAL_EDIT/EDIT_NOTES.txt` · `kosif-studio/motion/projects/premium_edit/index.html:1`

#### STORY-130 · بنية الشوريل · Showreel beat structure · 📦 بأمر تثبيت
- **ماذا / what:** 15 s product showreel on a 120 BPM grid: hook claim, button press, progress counter, pen-drawn spring curve, typed law, iris drop to real footage, card with facts, implode, lockup.
- **كيف / how:** projects/showreel + score.json + cues.json
- **أرقام / params:** 1920×1080 60 fps; beats b4, b6, b9, b12, b15.8, b21, b24.6, b26
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/showreel/index.html:66` · `kosif-studio/out/kosif_motion_showreel.mp4`

#### STORY-131 · توجيه الخطة · STYLE.md / PLAN.md direction · 📦 بأمر تثبيت
- **ماذا / what:** Every scene gets an audio interval, visual action, camera, transition and sound cue; observed vs assumed tokens recorded.
- **كيف / how:** Fill templates/STYLE.md and templates/PLAN.md before coding; preview contact sheet before final render.
- **أرقام / params:** entrances 250-600ms, accents 120-300ms, transitions 300-800ms
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/templates/PLAN.md` · `kosif-tool/templates/STYLE.md` · `kosif-tool/AGENTS.md`

#### STORY-132 · وصفة إعلان تطبيق 15 ثانية · 15-second app ad recipe · 📦 بأمر تثبيت
- **ماذا / what:** Seven-beat app ad timed to frames.
- **كيف / how:** Remotion Sequences at 30 fps: 0/45/120/195/270/345/405 frames, durations 45/75/75/75/75/60/45.
- **أرقام / params:** hook 0–1.5 s ease-out quint; tap 1.5–4 s spring 14/160; chart 4–6.5 s; notification 6.5–9; rating 4.8 counts 9–11.5 ease-out cubic; CTA 11.5–13.5 spring 14/180; logo 13.5–15
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/ads.md:36-70`

#### STORY-133 · فيديو إطلاق من كود الموقع · Website-to-launch-video workflow · 📦 بأمر تثبيت
- **ماذا / what:** Turns a project's code (index.html, CSS, README, routes) into a 15-25 s launch video without screenshots or live URL.
- **كيف / how:** Inspect -> brag-plan.md -> composition-brief.md -> Hyperframes composition -> check/render -> poster -> share copy.
- **أرقام / params:** duration auto 15-25s; landscape default
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/SKILL.md` · `kosif-one/vendor/brag/skills/brag/references/step-1-inspect.md`

#### STORY-134 · منهج موجز الصورة المصغرة · Thumbnail creative brief method · 🔑 مفتاح/خدمة
- **ماذا / what:** Produce three thumbnail concepts, pick one, and generate only the background with AI while the real face photo and text are composited.
- **كيف / how:** Each concept: layout, exact expression direction, ≤4 words with position, one accent colour on 1-2 elements over a dark ground, brand elements; tests: 'I want ___', readable in <1 s at mobile size, curiosity gap, audience-specific, works without the face; AI prompt describes environment only.
- **أرقام / params:** ≤4 words; 1 accent colour
- **الدليل / proof:** `kosif-atlas/skills/3067-youtube/13228-creator-thumbnail-agent` · `kosif-atlas/skills/932-vidseeds/2185-vidseeds-thumbnails`

#### STORY-135 · قواعد كتابة السكريبت لكل ستايل · Style script-writing rules per style · 🔑 مفتاح/خدمة
- **ماذا / what:** Each film style has a script contract (line count, words per line, one starred word, number/colon conventions) used when Claude writes the script.
- **كيف / how:** KIT.HINTS: plotter 4-7 lines of 2-5 words; doodle 4-8 sentences of 5-9 words with «dialogue»; whiteboard 4-6 steps of 3-7 words; chalkboard formulas allowed; stickman 4-7 lines 2-6 words with a twist; isometric 'Stage: ...' 3-6 stages; fake3d 3-5 poetic lines; infographic 3-6 lines with one figure each, never invented; mapjourney 'Place: what happened'; product 4-7 lines of 1-4 words, first a huge verb, last the name; lyric real song words. KIT.writeScript sizes to duration*wps*0.8 words.
- **الدليل / proof:** `app/public/js/10_studio.js:913` · `app/public/js/10_studio.js:983`

#### STORY-136 · معرض قوالب الأفلام · Built-in film template gallery (52) · 🔑 مفتاح/خدمة
- **ماذا / what:** 52 original brief templates in 7 Arabic genres with slots for subject {s}, line {l} and figure {x}; filling never invents numbers.
- **كيف / how:** TPL (00_editor.js): showreels (reel-designer 15 s, reel-type 12, reel-principles 15, reel-system 12, self-intro 10, studio-reel 15, particle-sphere 10, poster-alive 8, logo-sting 5); launch (app-launch 15, saas-promo 15, feature-teaser 10, pricing 12, milestone 8, dev-tool 12, release 10, dashboard-reveal 12, service-3 12); explain (concept 20, what-is 18, timeline 20, how-to 15, compare 12, math 18, recipe 15, code-explain 15, myth-fact 10); data (data-story, bar-race, report-card 12, price-mov…
- **الدليل / proof:** `app/public/js/00_editor.js:1777` · `app/public/js/00_editor.js:1838`

#### STORY-137 · المخرج بالكلام · KOSIF One director chat (JSON patch) · 🔑 مفتاح/خدمة
- **ماذا / what:** Natural-language Arabic edits become a JSON patch on the project (style, overlays, scenes, captions, cuts) plus optional routing to films, generated assets, post pack or shot prompts; asks one clarifying question with tappable answers only when a request is genuinely ambiguous.
- **كيف / how:** director(q,images): stateBrief (style JSON, overlays, scenes, transcript, taste line) + SCHEMA + DIRECTOR_EXTRA; routes talking_reel, edit_my_footage, mimic_reel, sound_to_film, song_reel, launch_video, ui_web_motion, analyze_reference, ai_video_prompts, image_graphics, audio_only, social_content; ASK_NOTE produces {ask:{q,options[2-4]}}; last 6 turns as memory; undo stack 25.
- **الدليل / proof:** `app/public/js/00_editor.js:1351` · `app/public/js/00_editor.js:1472` · `app/public/js/00_editor.js:2062`

#### STORY-138 · المخرج الآلي مع مراجعة ذاتية · One-click autopilot edit with self-critique · 🔑 مفتاح/خدمة
- **ماذا / what:** Does the complete edit in one pass (style, rhythm, starred captions, hook title, 3-6 overlays, up to 3 data scenes, nothing in the bottom 18%), then looks at a contact sheet of the result and fixes the three worst problems.
- **كيف / how:** autoPilot(): askJSON with up to 2 content frames; zoom.sync = pattern (music), speech (talk) or interval; then btnCritique: 6-frame contact sheet (3 columns, 264 px tiles, timestamps) scored on hook, readability, motion, variety, safe zones, brief, sound sync, identity; returns patch + up to 3 sceneFixes for code scenes.
- **أرقام / params:** contact sheet 6 frames
- **الدليل / proof:** `app/public/js/00_editor.js:1878` · `app/public/js/00_editor.js:2382` · `app/public/js/00_editor.js:2394`

#### STORY-139 · ترتيب اللقطات من كونتاكت شيت · Clip footage AI ordering from contact sheet · 🔑 مفتاح/خدمة
- **ماذا / what:** The AI sees a numbered contact sheet of all clips and decides story order (strongest image first, satisfying last), hook title, on-screen lines, pace and grade.
- **كيف / how:** MON.sheet: up to 4 columns of 192 px cells with amber number badges, JPEG 0.8; prompt in MON.run.
- **الدليل / proof:** `app/public/js/10_studio.js:2097` · `app/public/js/10_studio.js:2122`

#### STORY-140 · من ملف PDF لفيلم موشن · PDF/document to motion film · 🔑 مفتاح/خدمة
- **ماذا / what:** A text PDF, DOCX or text file becomes the source of the film script (summarised faithfully, no invented facts); image-only PDFs are rejected with an OCR hint.
- **كيف / how:** HUB.sourceText collects doc/script items; KIT.writeScript receives source (<= 9000 chars) with 'never invent facts or numbers'.
- **الدليل / proof:** `app/public/js/10_studio.js:2787` · `app/public/js/10_studio.js:983`

#### STORY-141 · قرارات التصميم بتقييم Jev · Design decisions scored by Jev · 🔑 مفتاح/خدمة
- **ماذا / what:** Design options (font, tab bar, emblem direction, brand assets vs templates) were chosen with the owner's Jev decision engine giving a probability per option, and recorded in docs.
- **كيف / how:** jev_choice -> e.g. IBM Plex Sans Arabic p=0.99, hybrid bottom bar p=0.75, ram emblem 0.97; jev_score ideas 0-4 with confidence.
- **الدليل / proof:** `kosif-earth-ci-fork/docs/design/KOSIF-LUXE.md` · `kosif-earth-ci-fork/docs/rebuild/DESIGN_SYSTEM.md`

#### STORY-142 · عتبات دمج المسارات · Jev combo acceptance thresholds · 🔑 مفتاح/خدمة
- **ماذا / what:** Extra route kept if p_yes>=0.6 stable, 0.4-0.6 only with a concrete unseen reason, <0.4 dropped; explicit user request always wins; one ratio/palette/font set across combined parts.
- **كيف / how:** kosif_jev_decide mode noul, stability on
- **أرقام / params:** 0.6/0.4
- **الدليل / proof:** `100-superskills/skills/kosif-one/SKILL.md`

#### STORY-143 · ومضة ثم رجوع يكشف أن المشهد بوستر · Flash bridge + poster pull-back reveal · 👁 شوهد في فيديو
- **ماذا / what:** push into light until full frame, flash to the light colour, start next scene zoomed on the same point inside a small <svg viewBox> poster of the same scene, then ease back to reveal wall + headline
- **أرقام / params:** flash ~200 ms, pull-back ~2 s easeOutCubic
- **الدليل / proof:** `style:fake3d`

#### STORY-144 · فاصل ورق الاستمارات · Paper-form interlude contrast · 👁 شوهد في فيديو
- **ماذا / what:** cut from the dark world to an off-white bureaucratic form (black header bar, numbered fields, flowchart) to represent the old way; strike it with a red marker line
- **أرقام / params:** hard cut, red line draw 400 ms
- **الدليل / proof:** `style:plotter`

#### STORY-145 · ختام بكلمة REKT ساخرة · REKT meme stamp ending · 👁 شوهد في فيديو
- **ماذا / what:** Escalate damage, then invert the joke: huge negative dollar value, red flood, giant pixel word stamp, charred target
- **أرقام / params:** stamp scale 1.4->1 in 3 frames, hold 2 s
- **الدليل / proof:** `style:pm-0xevinho-3777d8`

#### STORY-146 · بنية المشكلة ثم الحل البديهي ثم الحل الحقيقي · Problem → obvious fix → real fix story · 👁 شوهد في فيديو
- **ماذا / what:** chapter pills: THE FAILURE, THE OBVIOUS FIX (show its flaw), THE IDEA, STEP 1, STEP 2, failure test, EDGE CASE, TRADE-OFF
- **أرقام / params:** ~8-10 scenes, 5-6 s each
- **الدليل / proof:** `style:pm-0xnfrith-5be616`

#### STORY-147 · نقطة بطلة ثابتة عبر المشاهد · Persistent dot protagonist · 👁 شوهد في فيديو
- **ماذا / what:** one accent dot survives every cut and is reused as i-dot, full stop and decimal; animate its position continuously between scenes so it reads as a match-cut anchor
- **أرقام / params:** diameter ~2.5% h, colour #f2643a, squash 0.7/1.3 on landings
- **الدليل / proof:** `style:pm-1littlecoder-9fef89`

#### STORY-148 · قوس الحكاية من الصباح لليل · Day-to-night storybook arc · 👁 شوهد في فيديو
- **ماذا / what:** Structure the film as a day: morning greeting, play, nature scenes, sunset wash with typewriter line, night village with glowing windows and goodnight line, finale gathering of all characters
- **أرقام / params:** ~6 acts over 60-80 s
- **الدليل / proof:** `style:pm-abderrahmen-g-9e8ed0`

#### STORY-149 · إعلان مستخرج من كود المنتج · Promo from codebase · 👁 شوهد في فيديو
- **ماذا / what:** Read the product repo, list features, reuse real components/screens and copy; structure: hook question -> logo -> N features -> social proof -> CTA
- **أرقام / params:** ~60s; 6 features x ~4.6s
- **الدليل / proof:** `style:pm-ai-baymax-0ef9dd`

#### STORY-150 · بنية فصول قائمة على استعارة · Metaphor-chapter structure · 👁 شوهد في فيديو
- **ماذا / what:** frame the product story as a scientific metaphor (fission → fusion): chapter 1 breaks the source apart, chapter 2 fuses outputs; numbered chapter cards between
- **أرقام / params:** 2 chapters, each 15-18 s, climax at ~60% of runtime
- **الدليل / proof:** `style:pm-ajith-io-4c248f`

#### STORY-151 · قواعد لقطات الأنمي · Anime shot grammar · 👁 شوهد في فيديو
- **ماذا / what:** intro each unit → launch → transform → close-ups → pose
- **الدليل / proof:** `style:pm-allforbigfire-86ff3c`

#### STORY-152 · قلب الحجر كتعبير عاطفي · Emotional beat via flip · 👁 شوهد في فيديو
- **ماذا / what:** character hides by rotating 180° to blank back face, then returns; story arc: outsider letter finds its word
- **أرقام / params:** flip 600 ms easeInOut
- **الدليل / proof:** `style:pm-anilraok-eff262`

#### STORY-153 · هيكل إعلان بقصة · Product-promo story structure · 👁 شوهد في فيديو
- **ماذا / what:** characters solve a mini puzzle linked to the app, payoff line, then app logo + URL; brand only at end
- **أرقام / params:** ~40 s, 8-10 shots
- **الدليل / proof:** `style:pm-anilraok-eff262`

#### STORY-154 · ثلاثية بطاقات الألم · Three-pain card triptych · 👁 شوهد في فيديو
- **ماذا / what:** Three columns each with icon chip, short title, mini UI example proving the pain, and a one-line caption; built left to right
- **أرقام / params:** stagger 300 ms, card radius 12 px
- **الدليل / proof:** `style:pm-aschapmann-131210`

#### STORY-155 · قائمة لقطات سينمائية برمجيًا · Cinematic shot list in code · 👁 شوهد في فيديو
- **ماذا / what:** define 6 camera presets (wide, track, macro, ECU, low front, high rear) each ~6 s with hard cuts; camera parented to rider for tracking shots
- **أرقام / params:** focal lengths 24/50/85/100 mm equivalent; cut every 4-8 s
- **الدليل / proof:** `style:pm-axtonliu-0b861d`

#### STORY-156 · إيقاع فصول طويل للشرح · Long-form chaptered pacing · 👁 شوهد في فيديو
- **ماذا / what:** structure a 2-3 min explainer as ~12 chapters of ~12 s, each: establish camera move -> headline -> one concrete visual proof -> data panel; hard cut between chapters; bookend with the hero title card
- **أرقام / params:** 12 x 12 s, hold 3-5 s for reading
- **الدليل / proof:** `style:pm-blueoctopusai-dd17bd`

#### STORY-157 · تسمية الأقسام · Section label taxonomy · 👁 شوهد في فيديو
- **ماذا / what:** chapter number + caps label + italic subtitle bottom-left
- **الدليل / proof:** `style:pm-codestackr-c071bf`

#### STORY-158 · وسم فصل مرقّم أعلى العنوان · Numbered chapter tag · 👁 شوهد في فيديو
- **ماذا / what:** Small mono label '• 0N / VERB THE NOUN' above each headline to structure a promo into steps
- **أرقام / params:** accent dot, mono uppercase, 1.2% frame height
- **الدليل / proof:** `style:pm-elliot-garreffa-f334bc`

#### STORY-159 · القفز بين الأنماط البصرية · Genre-hop style switching · 👁 شوهد في فيديو
- **ماذا / what:** keep one message, re-skin each beat in a distinct visual genre (palette, font, texture, framing) to keep attention
- **أرقام / params:** 6-8 s per genre
- **الدليل / proof:** `style:pm-emollick-8661a8`

#### STORY-160 · نكتة الصفحة الخام · Unstyled base-case gag · 👁 شوهد في فيديو
- **ماذا / what:** at the climax show a browser-default HTML page (Times, white) and hold still to make the concept land
- **أرقام / params:** hold ~3-5 s
- **الدليل / proof:** `style:pm-emollick-8661a8`

#### STORY-161 · خطوة واحدة لكل بطاقة · One-card-per-step storyboard · 👁 شوهد في فيديو
- **ماذا / what:** tell a product flow as sequential single cards with one action each, ending in logo
- **أرقام / params:** ~1.3 s per step
- **الدليل / proof:** `style:pm-en-ra-81c6dd`

#### STORY-162 · نظام عناوين فصول · Chapter label system · 👁 شوهد في فيديو
- **ماذا / what:** '[0N] WORD' heavy caps top-left per scene
- **الدليل / proof:** `style:pm-eyishazyer-af035b`

#### STORY-163 · ذروة القلب المضيء · Glow core sacrifice beat · 👁 شوهد في فيديو
- **ماذا / what:** build to climax by transferring a glow from character to object
- **الدليل / proof:** `style:pm-faroukzy-9ff23e`

#### STORY-164 · افتتاح من الفضاء · Space-to-earth opener · 👁 شوهد في فيديو
- **ماذا / what:** starfield + planet with tracked title, then cut to world
- **الدليل / proof:** `style:pm-faroukzy-9ff23e`

#### STORY-165 · جدول ملخص في النهاية · Summary grid recap · 👁 شوهد في فيديو
- **ماذا / what:** close with a 2-column grid of all items (index in accent colour, title, one-line hook, rating) and a recommendation bar
- **أرقام / params:** row stagger 120 ms
- **الدليل / proof:** `style:pm-gigabit-million-16b3a0`

#### STORY-166 · من نقطة واحدة إلى سرب أفكار · One dot to thought swarm · 👁 شوهد في فيديو
- **ماذا / what:** start with a lone dot + typewriter caption, then ripple rings and spawn words in increasing number to visualise escalation
- **أرقام / params:** word count doubling every 0.5 s
- **الدليل / proof:** `style:pm-gizakdag-b8c59e`

#### STORY-167 · نافذة ختام هادئة · Calm porthole ending · 👁 شوهد في فيديو
- **ماذا / what:** circle mask with slow loop, italic word, title
- **الدليل / proof:** `style:pm-gizakdag-cf4ae6`

#### STORY-168 · هيكل إعلان ثلاثي في 10 ثوانٍ · Three-beat 10 s ad structure · 👁 شوهد في فيديو
- **ماذا / what:** 0-1.6 s title, 1.6-4.8 day 1, 4.8-7.4 day 2, 7.4-10 title + info + CTA
- **أرقام / params:** each beat: banner -> headliner -> tiers -> hold 0.8 s
- **الدليل / proof:** `style:pm-gonzalomacagno-2de1a9`

#### STORY-169 · فقاعة كلام فكاهية · Comic speech bubble gag · 👁 شوهد في فيديو
- **ماذا / what:** HTML/CSS2D overlay bubble anchored to projected character position, pop scale 0→1.1→1 with back-out easing, hold 1.5 s
- **أرقام / params:** white fill, 2px black stroke, radius 10px, tail triangle
- **الدليل / proof:** `style:pm-gorden-sun-041f56`

#### STORY-170 · سلسلة تحوّل من نقطة إلى عالم · Evolution chain morph · 👁 شوهد في فيديو
- **ماذا / what:** each scene's object is born from the previous (point→line→circle→sphere→lens→ball→flock→world→full stop) with no cuts
- **أرقام / params:** ~2.5-3 s per step
- **الدليل / proof:** `style:pm-hbcoop-de365c`

#### STORY-171 · الكوميديا بالذوق السيئ · Deliberate bad-taste comedy · 👁 شوهد في فيديو
- **ماذا / what:** escalate clichés with self-aware captions; end with rejection gag
- **الدليل / proof:** `style:pm-henkpoley-3d3407`

#### STORY-172 · شريط الحل مع إحصاء التكرار · THE FIX bar with frequency stat · 👁 شوهد في فيديو
- **ماذا / what:** full-width cream card at the bottom: green pill 'THE FIX', one-sentence rule in serif, divider, '≈1 in N questions' with tiny caption at right
- **أرقام / params:** slide-up 400 ms easeOutCubic
- **الدليل / proof:** `style:pm-henkvaness-0e06af`

#### STORY-173 · بطاقات ميزات مرقمة · Eyebrow numbered feature cards · 👁 شوهد في فيديو
- **ماذا / what:** '0N — LABEL' mono small caps above two-line title
- **الدليل / proof:** `style:pm-ho-ba-f3f0e9`

#### STORY-174 · تحويل السيرة إلى لعبة · Life as a game metaphor · 👁 شوهد في فيديو
- **ماذا / what:** Map each skill to a 'level', progress to score, finale to 'level up' and the end card to 'Player 1' — gives a structure and a reason for every counter
- **أرقام / params:** 5 levels + level up + map + end
- **الدليل / proof:** `style:pm-ibrahimwasim240-809370`

#### STORY-175 · عنصر بطل يربط كل المشاهد · Hero object as continuity thread · 👁 شوهد في فيديو
- **ماذا / what:** One simple object (ball) persists through every scene, carrying the story and finally becoming part of the logo
- **أرقام / params:** keep position continuity across cuts
- **الدليل / proof:** `style:pm-ik-builds-b8bdcf`

#### STORY-176 · رسالة تصل كطائرة ورقية · Paper airplane message delivery · 👁 شوهد في فيديو
- **ماذا / what:** Paper plane flies a bezier path in from the window/left, lands in the character's hand, unfolds (scaleX 0→1 with crease lines) into a note with handwritten request
- **أرقام / params:** flight 800 ms, unfold 300 ms
- **الدليل / proof:** `style:pm-jake11moran-a269c4`

#### STORY-177 · مكافآت تتراكم على الشخصية · Accumulating reward props · 👁 شوهد في فيديو
- **ماذا / what:** Each compliment adds a persistent prop (sash with curved text, butterfly clips) so the character visibly gathers praise over the story
- **أرقام / params:** text on path, prop drop-in 400 ms back-out
- **الدليل / proof:** `style:pm-jake11moran-a269c4`

#### STORY-178 · افتتاح بسؤال يلامس الحاجة · Question hook opener · 👁 شوهد في فيديو
- **ماذا / what:** Open on a centred two-line question with one key word coloured, hold ~2 s, then move into the product
- **أرقام / params:** accent green on key word
- **الدليل / proof:** `style:pm-justincooperman-e7bbc4`

#### STORY-179 · لحظة صمت في ظلام تام · Silence-in-darkness dramatic beat · 👁 شوهد في فيديو
- **ماذا / what:** drop frame to near-black with one tiny warm ember for 2-3 s to create tension before the climax reveal
- **أرقام / params:** mean luminance <3%
- **الدليل / proof:** `style:pm-kamstudiolabs-0b0824`

#### STORY-180 · لقطة واحدة متواصلة · Single-take continuous scene · 👁 شوهد في فيديو
- **ماذا / what:** No cuts; narrative carried by music sections and HUD state; density of launches rises toward climax
- **أرقام / params:** sections THEME/GROOVE/.../FALL
- **الدليل / proof:** `style:pm-kamstudiolabs-447565`

#### STORY-181 · مؤشر عملاق خصم · Giant cursor antagonist · 👁 شوهد في فيديو
- **ماذا / what:** oversized OS pointer that lunges with ease-in
- **الدليل / proof:** `style:pm-kamstudiolabs-c9bb28`

#### STORY-182 · بطاقة ختام صنع بالكود · Made-with-code end card · 👁 شوهد في فيديو
- **ماذا / what:** hard cut to dark card with three short bold lines and a muted small credits row
- **أرقام / params:** ~3-5 s hold
- **الدليل / proof:** `style:pm-kantamk-61f410`

#### STORY-183 · سرد بضمير المتكلم للأداة · First-person POV narrative · 👁 شوهد في فيديو
- **ماذا / what:** Structure: greeting → rules/identity → typical requests → stats jokes → noise/overload → what I know → calm reflection → thanks; each beat one card
- **أرقام / params:** ~45 cards over 150 s
- **الدليل / proof:** `style:pm-kloss-xyz-15182a`

#### STORY-184 · جملة جذب من سطرين: متضادان · Grown vs built two-line hook · 👁 شوهد في فيديو
- **ماذا / what:** line 1 neutral colour states a universal fact; line 2 in accent colour reverses it; second line enters ~1 s later
- **أرقام / params:** same size, accent colour on line 2 only
- **الدليل / proof:** `style:pm-kloss-xyz-b9b3f6`

#### STORY-185 · أغراض طافية سريالية · Surreal floating props · 👁 شوهد في فيديو
- **ماذا / what:** scatter unrelated vintage objects floating in sky with slow drift/rotation to build a dream-collage world
- **أرقام / params:** drift 10-30 px/s, rotation 2-8 deg/s
- **الدليل / proof:** `style:pm-koldo2k-5cff87`

#### STORY-186 · حلقة تبدأ وتنتهي بفيلم نموذجي · Loop bookend with sample film · 👁 شوهد في فيديو
- **ماذا / what:** open on rapid previews of outputs, explain the process, end by returning to the same film so the video loops seamlessly
- **أرقام / params:** intro cuts ~0.5 s
- **الدليل / proof:** `style:pm-lemomo-ai-0d9cff`

#### STORY-187 · خيط العنصر البطل · Hero object thread · 👁 شوهد في فيديو
- **ماذا / what:** One coloured ball persists across every scene (bounce -> sun -> i-dot -> cube roller -> gauge marker -> logo dot) to stitch unrelated vignettes
- **أرقام / params:** single accent #ff5a1f, same screen position at each cut for match
- **الدليل / proof:** `style:pm-leonkohli-6dc01b`

#### STORY-188 · بطاقة عبارة سوداء · Black statement title card · 👁 شوهد في فيديو
- **ماذا / what:** Hard cut to black with one short bold sentence to change chapter (e.g. scope expansion), then cut back to UI
- **أرقام / params:** hold 1.5-2 s, white 800 weight
- **الدليل / proof:** `style:pm-lester-tyy-f897f7`

#### STORY-189 · شاشة تصدير وهمية تلخص الفصول · Fake render-progress recap · 👁 شوهد في فيديو
- **ماذا / what:** Blue screen with spinner + filename, giant rolling percent counter and a filmstrip of previous chapters filling left-to-right as a recap before the logo
- **أرقام / params:** counter 0 -> 99 over ~1.5 s, digit motion blur
- **الدليل / proof:** `style:pm-levabashidze-2d713a`

#### STORY-190 · نقطة لونية رابطة · Accent dot motif · 👁 شوهد في فيديو
- **ماذا / what:** single coral dot persists across cuts as match element
- **أرقام / params:** r~3% width
- **الدليل / proof:** `style:pm-lexnlin-038035`

#### STORY-191 · تقسيم الدرس بعناوين وتلاشٍ · Section title + fade chaptering · 👁 شوهد في فيديو
- **ماذا / what:** each concept is a scene: yellow numbered title top-left, content, FadeOut all, short empty beat, next scene
- **أرقام / params:** fade 0.5-1 s; 12-14 sections for a 7-min lesson
- **الدليل / proof:** `style:pm-linearuncle-5d2bae`

#### STORY-192 · خاتمة بأسئلة للتفكير · Reflective question ending · 👁 شوهد في فيديو
- **ماذا / what:** end card with centred heading '想一想' and numbered open questions, narrated one by one
- **أرقام / params:** 2-3 questions, each held ~8-10 s
- **الدليل / proof:** `style:pm-linearuncle-5d2bae`

#### STORY-193 · إيقاع هادئ صامت · Calm silent pacing · 👁 شوهد في فيديو
- **ماذا / what:** Question opener -> 3 numbered steps (~8 s each) -> logo; every step self-explains with on-screen caption so it works muted on social feeds
- **أرقام / params:** 30 s total, no audio
- **الدليل / proof:** `style:pm-majorbaguette-fb11d7`

#### STORY-194 · جمل سردية متقطعة · Narrative caption beats · 👁 شوهد في فيديو
- **ماذا / what:** single short line on black, fade 400 ms, hold 2 s
- **الدليل / proof:** `style:pm-marklaunches-3b9492`

#### STORY-195 · ختام هادئ بالشعار والشعار النصي · Calm logo lock-up outro · 👁 شوهد في فيديو
- **ماذا / what:** after the frenzy, hold a black frame with centred wordmark, 3-line tracked uppercase tagline and handles at the bottom
- **أرقام / params:** 3-4 s hold, fade 400 ms
- **الدليل / proof:** `style:pm-micheleharmonic-77628e`

#### STORY-196 · شارة رقم الفصل · Numbered chapter chip · 👁 شوهد في فيديو
- **ماذا / what:** small black circle with white number + uppercase chapter name; structure explainer as 01..06 principles
- **أرقام / params:** circle 14px
- **الدليل / proof:** `style:pm-moguzbulbul-6311b6`

#### STORY-197 · شبكة تجميع لقطات سابقة · Collage recap grid · 👁 شوهد في فيديو
- **ماذا / what:** Reuse earlier scene renders as tilted thumbnails flying into a 3x3 grid before the logo
- **أرقام / params:** stagger 50 ms, rotate ±4 deg, 500 ms easeOutBack
- **الدليل / proof:** `style:pm-motiondsgnr-9dcfa6`

#### STORY-198 · أيقونات ليل ونهار للمزاج · Night/day mood icons · 👁 شوهد في فيديو
- **ماذا / what:** Swap moon+stars+bed+Zzz for sun+coffee steam to signal time passing without text
- **أرقام / params:** yellow #efd77a fills only on celestial icons
- **الدليل / proof:** `style:pm-nikolajankovic-ce4ff4`

#### STORY-199 · تأطير القصة بوحدة زمن واحدة · Per-unit time framing · 👁 شوهد في فيديو
- **ماذا / what:** Structure the whole film around 'in one second' facts; each chapter resets an 'elapsed 0->1.000 s' bar so the viewer feels slowed time
- **أرقام / params:** 5 chapters; numbered 01-05 with mono labels
- **الدليل / proof:** `style:pm-nolkeeg-bf062e`

#### STORY-200 · قوس: انضباط ثم هروب ثم فوضى ثم عودة · Control-escape-chaos-control arc · 👁 شوهد في فيديو
- **ماذا / what:** structure acts by named states printed in the HUD; bookend start and end with the same calm frame
- **أرقام / params:** 5 acts over 30 s
- **الدليل / proof:** `style:pm-pankajkumar-dev-0bee87`

#### STORY-201 · تعليقات المراحل · Phase captions · 👁 شوهد في فيديو
- **ماذا / what:** Divide the simulation into 3 scenarios (steady, burst, recovery) and swap a one-line lowercase caption per phase; final takeaway in accent colour
- **أرقام / params:** 3 phases + takeaway
- **الدليل / proof:** `style:pm-parkerrex-1a54fe`

#### STORY-202 · تكرار متصاعد · Looping beat-escalation · 👁 شوهد في فيديو
- **ماذا / what:** same action per year with shorter period each loop
- **الدليل / proof:** `style:pm-pluginplay-3d4006`

#### STORY-203 · منارة وامضة تتباطأ لإظهار تمدد الزمن · Pulsing beacon time-dilation cue · 👁 شوهد في فيديو
- **ماذا / what:** A point light blinking at a fixed proper interval whose observed interval grows (and redshifts) as it nears the horizon — visualizes an abstract concept
- **أرقام / params:** interval 1 s × 1/sqrt(1-r_s/r)
- **الدليل / proof:** `style:pm-rebutonepress-810f78`

#### STORY-204 · العنوان في البداية والنهاية فوق الموضوع · Title bookend over subject · 👁 شوهد في فيديو
- **ماذا / what:** Open and close with the same widely-tracked title + subtitle, the ending version over the darkened final image
- **أرقام / params:** letter-spacing 0.3em, fade 1.5 s
- **الدليل / proof:** `style:pm-rebutonepress-810f78`

#### STORY-205 · لحظة السؤال قبل الكشف · Question-mark twist beat · 👁 شوهد في فيديو
- **ماذا / what:** state an assumption (X = known thing), break it (scramble + strike), replace with '?', then reveal brand promise 'never just one' + 'Soon.'
- **أرقام / params:** assumption 1.5 s, break 1.5 s, ? hold 1 s
- **الدليل / proof:** `style:pm-robj3d3-b18fad`

#### STORY-206 · فاصل ليلي لتغيير المزاج · Day/night mood interlude · 👁 شوهد في فيديو
- **ماذا / what:** insert one dark indigo scene in a light film to express 'while you sleep', then return to light
- **أرقام / params:** crossfade 600 ms
- **الدليل / proof:** `style:pm-sachaarbonel-8f14f4`

#### STORY-207 · توقيع ختامي برذاذ حبر · Handwritten sign-off with ink splatter · 👁 شوهد في فيديو
- **ماذا / what:** clear all instructional text and leave the finished object plus a short handwritten closing phrase and 5-8 random ink dots near it
- **أرقام / params:** phrase write-on ~800 ms
- **الدليل / proof:** `style:pm-sarut0bisasuke-cefa43`

#### STORY-208 · بنية الريل بالفصول · Chapter showreel structure · 👁 شوهد في فيديو
- **ماذا / what:** Name each chapter by a skill (ignition, kinetic type, shape language, particle systems, dimension, interface, generative) and give each ~1.5 s with its own technique, close on logo
- **أرقام / params:** 8 x 1.6s + 2s end
- **الدليل / proof:** `style:pm-shinskinakamoto-20190b`

#### STORY-209 · دوّامة فئات سريعة · Rapid 'a ___' category carousel · 👁 شوهد في فيديو
- **ماذا / what:** same sentence slot swapped per scene with new bg colour
- **أرقام / params:** 1.5 s each
- **الدليل / proof:** `style:pm-slvdev-64c45a`

#### STORY-210 · افتتاحية ساخرة · Ironic cold open · 👁 شوهد في فيديو
- **ماذا / what:** Start with a sterile white 'compliance' UI element, then hard-cut to loud cinematic visuals to set satirical tone
- **أرقام / params:** hold 2.3 s, cursor hover
- **الدليل / proof:** `style:pm-spearwtf-3c1fd1`

#### STORY-211 · انتقال من داكن لفاتح · Dark-to-light act change · 👁 شوهد في فيديو
- **ماذا / what:** switch theme mid video to mark problem→solution
- **الدليل / proof:** `style:pm-sudo-kiran-b055de`

#### STORY-212 · لوحة خلاصة مرقّمة ملوّنة · Colour-coded recap board · 👁 شوهد في فيديو
- **ماذا / what:** final chapter writes a numbered list of 5 one-line takeaways, each in its chapter colour, plus a boxed footnote
- **أرقام / params:** one line per narration sentence
- **الدليل / proof:** `style:pm-tak3sh8-be5012`

#### STORY-213 · بنية سؤال ثم بحث ثم جواب · Question → scan → answer structure · 👁 شوهد في فيديو
- **ماذا / what:** ask in text, show a search/scan with suspense, lock with a flash, reveal the answer big, back it with data, restate the answer in the native language
- **أرقام / params:** 30 s: 4 s ask, 9 s scan, 6 s reveal, 6 s data, 5 s answer
- **الدليل / proof:** `style:pm-tankazunori0914-0fc886`

#### STORY-214 · رسائل مقفلة بترتيب ثابت · Locked message beats · 👁 شوهد في فيديو
- **ماذا / what:** Write the ad as 5-6 short shouty lines in a fixed order (hook, thesis, twist, proof, command, handle), one per 4 s phrase
- **أرقام / params:** <=4 words per line
- **الدليل / proof:** `style:pm-techhalla-7acbc2`

#### STORY-215 · إعادة صياغة التكلفة يومياً · Cost-per-day reframing · 👁 شوهد في فيديو
- **ماذا / what:** dark slide: big loss number vs tiny daily price
- **الدليل / proof:** `style:pm-thayto-dev-44b911`

#### STORY-216 · منحنى طاقة المقطع الدعائي · Trailer energy arc · 👁 شوهد في فيديو
- **ماذا / what:** quiet wide shots -> build with day-night shift -> fast cut climax on beat -> silence -> title card
- **أرقام / params:** 0-8 / 8-20 / 20-32 / 32-38 s
- **الدليل / proof:** `style:pm-theparuchh-6e08c3`

#### STORY-217 · ريل بطاقات ميزات بإيقاع ثابت · Feature-card reel grid · 👁 شوهد في فيديو
- **ماذا / what:** One feature per scene, fixed rhythm ~2.5 s each: badge -> 2-line headline -> live mini-demo -> hold; alternate light/dark background per scene
- **أرقام / params:** scene=2.5s; 8-10 scenes in 25s; end card 3s
- **الدليل / proof:** `style:pm-thilina-a-891c09`

#### STORY-218 · بطاقة افتتاح وختام · Bookend CV card · 👁 شوهد في فيديو
- **ماذا / what:** open and close on same card, final with added icons
- **الدليل / proof:** `style:pm-web3wesley-7bb108`

#### STORY-219 · عنقود إشعارات تعرض المشكلة · Problem-notification cluster · 👁 شوهد في فيديو
- **ماذا / what:** Open with 3 tilted OS-style notification banners voicing the pain point, then fly the product icon into the middle as the answer
- **أرقام / params:** banner radius 18 px, shadow 0 12px 30px rgba(0,0,0,.08), tilt ±4°, stagger 300 ms
- **الدليل / proof:** `style:pm-wozu-co-242285`

#### STORY-220 · تجميع الظل · Silhouette assembly · 👁 شوهد في فيديو
- **ماذا / what:** shapes slide in black on gradient
- **الدليل / proof:** `style:pm-x4b47x-9cc84f`

#### STORY-221 · عقد المشهد كبيانات · Scene contract as data · 📄 موصوف
- **ماذا / what:** Describe every scene as structured data before binding to any library: id, viewer text, takeaway, data layers, media, annotations, camera/transform, trigger or time range, motion verb, reduced-motion fallback, static frame.
- **كيف / how:** Store scenes in JSON; render engine reads ranges by named id; the same JSON drives stills QA (static frame per scene).
- **أرقام / params:** motion verbs: reveal, compare, accumulate, transform, move, zoom, pan, highlight, play
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali/references/story-patterns-and-scene-contracts.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali/SKILL.md`

#### STORY-222 · تقسيم التريلر بالمازورات · Trailer beat sheet in bars · 📄 موصوف
- **ماذا / what:** A 35-45 s progress trailer: cold open 1-2 bars (most striking moment already in motion, ending on a downbeat hit with flash/hit-stop, no logo first), optional half-time studio sting 1-2 bars, drop/hook 6-8 bars (one shot per bar, one-word kinetic captions on downbeats, half-bar cuts in the last bar)…
- **كيف / how:** Write the beat sheet in bars before music or rendering and get approval; captions 1-3 words, at most one per bar, centred in safe zones, nothing that must be read in under one beat.
- **أرقام / params:** cold 1-2 bars; drop 6-8; tour 3-4; climax 4-6; end 2-3 (hold >=1.5)
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/concept-and-music.md` · `kosif-atlas/skills/1526-gamegen/4173-game-trailer/SKILL.md`

#### STORY-223 · جدول نوتة الحركة · Motion score table · 📄 موصوف
- **ماذا / what:** Per beat: subject, start, end, duration/delay, ease, trigger, fallback, interruption.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-director.md` · `kosif-studio/motion/references/motion-director.md`

#### STORY-224 · أنماط ممنوعة تبدو مولدة · Banned generated-looking defaults · 📄 موصوف
- **ماذا / what:** Looks that read as template/AI: centred title on gradient, everything fading in, blur-in text, crossfades, dark scene with green/purple glow, particle bursts and flares for their own sake, frame borders and corner labels, invented logos, synthesised beeps, long holds.
- **كيف / how:** Avoid unless the brand owns them; motion.py lint warns on some.
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/references/motion-craft.md` · `kosif-one/tools/kosif-studio/motion/references/x-trend-2026.md` · `kosif-studio/motion/references/motion-craft.md` · `kosif-studio/motion/references/craft-numbers.md`

#### STORY-225 · بناء ثم تنفس ثم حسم · Build / breathe / resolve scene arc · 📄 موصوف
- **ماذا / what:** Each scene has three phases: staggered build, a calm hold with one ambient motion, then a decisive end; exits are faster than entrances.
- **كيف / how:** Build 0-30% of scene, breathe 30-70% with ONE ambient motion (drift, breathe, slow pan), resolve 70-100%; enter ~0.4s vs exit ~0.25s; slowest scene ~3x slower than fastest.
- **أرقام / params:** 0-30/30-70/70-100%; enter 0.4s exit 0.25s
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/motion-principles.md`

#### STORY-226 · علامات التصميم الآلي المبتذل · AI-design tells to question · 📄 موصوف
- **ماذا / what:** A list of defaults that make output look machine-made, to be used only deliberately.
- **كيف / how:** Question: gradient text, left accent stripes, cyan-on-dark / purple-blue gradients, pure #000/#fff (tint toward accent), identical card grids, everything centered, overused display fonts (Syne named), Inter/Roboto defaults.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/house-style.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/typography.md` · `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/SKILL.md`

#### STORY-227 · ظهور مربوط بالتمرير · Scroll-scrubbed reveals · 📄 موصوف
- **ماذا / what:** ScrollTrigger/Lenis scrub patterns translate directly into time-scrubbed video beats.
- **كيف / how:** trigger start 'top 65%', end 'bottom 30%', scrub 1; two text layers (sharp + statically pre-blurred 6-10px ghost) crossfaded by opacity instead of animating blur per word; in video replace scroll progress with timeline progress.
- **أرقام / params:** ghost blur 6-10px; scrub 1
- **الدليل / proof:** `kosif-atlas/skills/100-ui-motion/210-scroll-blur-manifesto/SKILL.md` · `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md`

#### STORY-228 · هياكل قصصية للإعلانات القصيرة · Story structures for short promos · 📄 موصوف
- **ماذا / what:** Timed beat templates for demo/promo videos with one focus per scene.
- **كيف / how:** Classic 30-60s: hook 3s, problem 5s, magic moment 5s, proof 15s, social proof 4s, invite 4s; problem-solution 20-40s: before 6, after 6, how 10, CTA 4; teaser 15s: hook 2, demo 8, logo 3, tagline 2. Narration: one idea per scene, lead with the verb, contrast numbers.
- **الدليل / proof:** `kosif-atlas/skills/166-demo-video/535-demo-video/SKILL.md`

#### STORY-229 · بصمات حركية لأساليب مسماة · Named motion style signatures · 📄 موصوف
- **ماذا / what:** Eight design-tradition presets each with palette, type and an ease signature (e.g. Swiss Pulse = expo.out/power4.out snap, Velvet Standard = sine.inOut/power1 glide, Maximalist Type = ridged burn).
- **كيف / how:** Swiss Pulse: #1a1a1a + one accent #0066FF or #FFB300, grid-locked, counters; Velvet Standard: navy #1a237e or gold #c9a84c, ALL CAPS tracking 0.15em+, long holds; others: Deconstructed, Data Drift, Soft Signal, Folk Frequency, Shadow Cut.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/visual-styles.md`

#### STORY-230 · حزمة تسليم لمولد خارجي · Claude Design kit handoff · 📄 موصوف
- **ماذا / what:** When the film is built by another engine/agent, ship a folder: PROMPT.md in the engine's language, START-HERE upload order, ATTACH/ with the runtime and isolated transparent parts (>=1600px long edge), reference frames whose filenames carry the instruction, and a KIT manifest.
- **كيف / how:** Name missing assets explicitly instead of inventing substitutes; optional local build + contact sheet for verification.
- **أرقام / params:** >=1600px parts
- **الدليل / proof:** `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`

#### STORY-231 · شخصية حركة: حقل المؤشر · Motion personality: cursor-field · 📄 موصوف
- **ماذا / what:** Nothing moves until the viewer/pointer does; fields ripple and elements lean toward the pointer, then settle slowly. No autoplay, no scroll entrances.
- **كيف / how:** Pick exactly one personality per film/page from the brief, then derive every animation from its allowed moves and bans. Implement with CSS/WAAPI/GSAP/Canvas in an HTML composition and render with kosif-tool render_html.cjs (Playwright Chromium at /opt/pw-browsers + ffmpeg, both present).
- **أرقام / params:** instant response, long settle; magnetic pull; ripple grids; click sparks only as punctuation
- **الدليل / proof:** `kosif-atlas/skills/342-kernel/1223-frontend/motion/cursor-field.md` · `kosif-atlas/skills/342-kernel/1223-frontend`

#### STORY-232 · شخصية حركة: الجولة الكبرى · Motion personality: grand-tour · 📄 موصوف
- **ماذا / what:** The page is a film in acts: pinned scenes, one continuous background world evolving, scroll-scrubbed scale/position, chapter wipes; at most ~6 acts.
- **كيف / how:** Pick exactly one personality per film/page from the brief, then derive every animation from its allowed moves and bans. Implement with CSS/WAAPI/GSAP/Canvas in an HTML composition and render with kosif-tool render_html.cjs (Playwright Chromium at /opt/pw-browsers + ffmpeg, both present).
- **أرقام / params:** 2-3 depth layers max; one long held beat for the product; fast beats for energy
- **الدليل / proof:** `kosif-atlas/skills/342-kernel/1223-frontend/motion/grand-tour.md` · `kosif-atlas/skills/342-kernel/1223-frontend`

#### STORY-233 · شخصية حركة: الآلة المسكونة · Motion personality: haunted-machine · 📄 موصوف
- **ماذا / what:** Old hardware straining: decode/glitch text, scanline/dither/halftone reveals, split-flap signs, LED matrices, radar sweeps; motion is quantized on a tick, no smooth easing, no glass.
- **كيف / how:** Pick exactly one personality per film/page from the brief, then derive every animation from its allowed moves and bans. Implement with CSS/WAAPI/GSAP/Canvas in an HTML composition and render with kosif-tool render_html.cjs (Playwright Chromium at /opt/pw-browsers + ffmpeg, both present).
- **أرقام / params:** stepped timing at fixed or irregular ticks; glitch never on functional feedback
- **الدليل / proof:** `kosif-atlas/skills/342-kernel/1223-frontend/motion/haunted-machine.md` · `kosif-atlas/skills/342-kernel/1223-frontend`

#### STORY-234 · شخصية حركة: حبس الأنفاس · Motion personality: held-breath · 📄 موصوف
- **ماذا / what:** Restraint as luxury: one almost imperceptible drift, instant cuts between states, at most one event per view, never two moving things at once, no springs.
- **كيف / how:** Pick exactly one personality per film/page from the brief, then derive every animation from its allowed moves and bans. Implement with CSS/WAAPI/GSAP/Canvas in an HTML composition and render with kosif-tool render_html.cjs (Playwright Chromium at /opt/pw-browsers + ffmpeg, both present).
- **أرقام / params:** timing either instant or glacial; ambient changes over minutes
- **الدليل / proof:** `kosif-atlas/skills/342-kernel/1223-frontend/motion/held-breath.md` · `kosif-atlas/skills/342-kernel/1223-frontend`

#### STORY-235 · شخصية حركة: الطباعة الحركية · Motion personality: kinetic-type · 📄 موصوف
- **ماذا / what:** Only letterforms move: variable-font axes bend to the pointer, scroll-velocity skew, per-glyph mask reveals, split-flap/decode swaps, odometer digits; body text never animates.
- **كيف / how:** Pick exactly one personality per film/page from the brief, then derive every animation from its allowed moves and bans. Implement with CSS/WAAPI/GSAP/Canvas in an HTML composition and render with kosif-tool render_html.cjs (Playwright Chromium at /opt/pw-browsers + ffmpeg, both present).
- **أرقام / params:** one text behaviour per view; no particles/background shaders
- **الدليل / proof:** `kosif-atlas/skills/342-kernel/1223-frontend/motion/kinetic-type.md` · `kosif-atlas/skills/342-kernel/1223-frontend`

#### STORY-236 · شخصية حركة: المادة السائلة · Motion personality: liquid-material · 📄 موصوف
- **ماذا / what:** One viscous substance (liquid, metal) that deforms around input and heals slowly, refraction passing over content, moving specular light on type.
- **كيف / how:** Pick exactly one personality per film/page from the brief, then derive every animation from its allowed moves and bans. Implement with CSS/WAAPI/GSAP/Canvas in an HTML composition and render with kosif-tool render_html.cjs (Playwright Chromium at /opt/pw-browsers + ffmpeg, both present).
- **أرقام / params:** slow continuous; recovery slower than disturbance; one substance per page
- **الدليل / proof:** `kosif-atlas/skills/342-kernel/1223-frontend/motion/liquid-material.md` · `kosif-atlas/skills/342-kernel/1223-frontend`

#### STORY-237 · شخصية حركة: السطح الواحد · Motion personality: one-surface · 📄 موصوف
- **ماذا / what:** The interface is one surface changing shape: shared-element container morphs, islands expanding into panels, one sliding highlight, digit-by-digit numbers; no entrance choreography.
- **كيف / how:** Pick exactly one personality per film/page from the brief, then derive every animation from its allowed moves and bans. Implement with CSS/WAAPI/GSAP/Canvas in an HTML composition and render with kosif-tool render_html.cjs (Playwright Chromium at /opt/pw-browsers + ffmpeg, both present).
- **أرقام / params:** smooth easing, no bounce; one morph owns the beat
- **الدليل / proof:** `kosif-atlas/skills/342-kernel/1223-frontend/motion/one-surface.md` · `kosif-atlas/skills/342-kernel/1223-frontend`

#### STORY-238 · شخصية حركة: الوزن الحقيقي · Motion personality: real-weight · 📄 موصوف
- **ماذا / what:** Everything has mass: sticker-peel reveals, thrown card decks, swinging hung elements, elastic controls, gooey merges; objects arrive by moving, never by fading.
- **كيف / how:** Pick exactly one personality per film/page from the brief, then derive every animation from its allowed moves and bans. Implement with CSS/WAAPI/GSAP/Canvas in an HTML composition and render with kosif-tool render_html.cjs (Playwright Chromium at /opt/pw-browsers + ffmpeg, both present).
- **أرقام / params:** visible overshoot, 1-2 bounces, fast settle; one gravity for the whole piece
- **الدليل / proof:** `kosif-atlas/skills/342-kernel/1223-frontend/motion/real-weight.md` · `kosif-atlas/skills/342-kernel/1223-frontend`

#### STORY-239 · تسع هويات حسية بصرية · Nine sensory aesthetic variants · 📄 موصوف
- **ماذا / what:** Mood families described by sight/feel/sound with a direction and a danger note: abyss (glow from darkness), arctic (extreme white, one dark disruptor), ember (ash with rare warm focal points), patina (texture and wear), signal (dense mono data), spatial (receding grids, z-depth), substrate (stacked …
- **كيف / how:** Choose one variant as the look bible for a video; convert its direction into palette, texture and light rules before designing scenes.
- **أرقام / params:** abyss: never pure black, light emitted by elements; arctic: blue-grey shadows; ember: warmth used sparingly; void: spacing and type only
- **الدليل / proof:** `kosif-atlas/skills/342-kernel/1223-frontend/variants/abyss.md` · `kosif-atlas/skills/342-kernel/1223-frontend/variants/ember.md` · `kosif-atlas/skills/342-kernel/1223-frontend/variants/void.md`

#### STORY-240 · ست عائلات اتجاه بصري للويب · Six web direction families · 📄 موصوف
- **ماذا / what:** Established directions to commit to (never blend into a sampler): editorial, brutalist, glow-grain, industrial-mono, active-bento, type-as-hero; each defines composition grammar, type contrast, palette ratio, material, motif and one tasteful risk.
- **كيف / how:** Write a decision brief (job, focal path, type plan, palette ratio, motif, motion level, restraints) before building any scene.
- **أرقام / params:** one direction per piece; one tasteful risk
- **الدليل / proof:** `kosif-atlas/skills/1394-stark/3329-web-design`

#### STORY-241 · ربط المؤثر بالإحساس · Effect-to-feeling mapping · 📄 موصوف
- **ماذا / what:** Which motion vocabulary produces which emotional register: cinematic, techy, playful, corporate, calm, editorial.
- **كيف / how:** Use as a lookup when a user names a feeling in Arabic (فخم، تقني، مرح، رسمي، هادئ، صحفي) and translate into durations and effects.
- **أرقام / params:** dramatic: 1-1.5s fades, scale 0.9->1, spotlight; techy: neon glow, scramble text, grid reveals, particles; playful: spring bounce, bobbing; corporate: 200-300ms subtle; calm: very slow fades, serif; editorial: staggered text, pull quotes
- **الدليل / proof:** `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/animation-patterns.md`

#### STORY-242 · قائمة الأنماط المستهلكة الممنوعة · Generic-AI-look blacklist · 📄 موصوف
- **ماذا / what:** Recognisable defaults that make output look machine-made unless the brief asks for them: centered headline with purple glow and three equal cards, Inter/Roboto display, indigo #6366f1, warm cream with clay accent, near-black with acid green, tracked caps eyebrows everywhere, middle-dot meta strings,…
- **كيف / how:** Run a self-check pass on every storyboard frame; if a choice would appear for any similar brief, replace it with one specific to the subject.
- **أرقام / params:** cream ~#F4F1EA + clay ~#D97757 flagged as a tell; uppercase eyebrow count <= ceil(sections/3); zigzag image/text rows capped at 2 consecutive
- **الدليل / proof:** `kosif-atlas/skills/1420-frontend-design-skills/3376-anthropic-frontend-design` · `kosif-atlas/skills/342-kernel/1223-frontend/reference/component-sources.md` · `kosif-atlas/skills/880-superloopy/1941-superloopy-frontend/references/anti-slop.md`

#### STORY-243 · الجرأة في عنصر واحد · Spend boldness in one place · 📄 موصوف
- **ماذا / what:** Pick one memorable element (one orchestrated reveal, one signature interaction) and keep everything around it quiet; scattered effects read as template.
- **كيف / how:** In the storyboard mark one 'signature beat' per film; other beats use utility motion only.
- **أرقام / params:** 1 signature moment per piece; 1-2 signature moments per product
- **الدليل / proof:** `kosif-atlas/skills/1420-frontend-design-skills/3376-anthropic-frontend-design` · `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/signature-moments.md` · `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director`

#### STORY-244 · طابع الحركة حسب نوع المنتج · Motion character by product archetype · 📄 موصوف
- **ماذا / what:** Motion style follows what the audience must believe: product-led SaaS crisp state changes; developer tools instrument-like terminal/data progressions; fintech calm without overshoot; commerce tactile material response; research explanatory layering; experimental one signature behaviour plus quiet ut…
- **كيف / how:** Classify the client (from the audio/script) into an archetype first, then choose evidence (product-in-action, code, outcomes, photography, diagrams) and motion character.
- **أرقام / params:** state feedback 120-250ms tuned to distance
- **الدليل / proof:** `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/references/motion.md` · `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director`

#### STORY-245 · مفردات السرد بالتمرير · Scrollytelling technique vocabulary · 📄 موصوف
- **ماذا / what:** Named narrative mechanics: graphic sequence, animated transition, pan-and-zoom, moviescroller (scroll scrubs video/frames), show-and-play, parallax depth layer, sticky side-by-side, sticky overlay, stacked mobile fallback.
- **كيف / how:** Choose the lightest implementation: CSS sticky -> IntersectionObserver/Scrollama -> CSS ScrollTimeline/ViewTimeline -> Motion useScroll -> GSAP ScrollTrigger -> D3/Canvas/WebGL/video. Each maps directly to a video edit device.
- **أرقام / params:** every scene must work as a still; each step adds evidence
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali` · `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali/references/story-patterns-and-scene-contracts.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali/references/implementation-and-performance.md`

#### STORY-246 · خط إنتاج من الموقع إلى فيديو · Website-to-video 7-step pipeline · 📄 موصوف
- **ماذا / what:** Capture a site, write a short brand cheat sheet, write narration, write a beat storyboard, generate VO and word timestamps, build compositions with self-review, validate and preview before any MP4 render.
- **كيف / how:** Gate each step by an artifact (DESIGN.md, SCRIPT.md, STORYBOARD.md, narration + transcript.json). Here: capture with local Playwright, compose in HTML/GSAP, render with kosif-tool render_html.cjs (Playwright Chromium at /opt/pw-browsers + ffmpeg, both present); HyperFrames CLI itself needs npm install.
- **أرقام / params:** social ad 10-15s/3-4 beats; product demo 30-60s/5-8; feature 15-30s/3-5; brand reel 20-45s/4-6; launch teaser 10-20s/2-4; 1920x1080, 1080x1920, 1080x1080
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/step-1-capture.md` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/step-4-storyboard.md`

#### STORY-247 · قواعد تدقيق الأصول · Asset audit rules for website films · 📄 موصوف
- **ماذا / what:** Use the client's real visuals generously and deliberately: assign every captured asset to a beat or skip it with a reason.
- **كيف / how:** Print an asset table (asset, type, beat, role) before writing beats.
- **أرقام / params:** >= 50% of product screenshots/hero images used; logo in first and last beat; site's signature visual must appear; <= 2 consecutive text-only beats; opening beat has a visual
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/step-4-storyboard.md`

#### STORY-248 · قالب توجيه المشهد بأفعال الطاقة · Beat direction template with energy verbs · 📄 موصوف
- **ماذا / what:** Each beat is written as an experience: concept, VO cue, cinematic description with at least five elements across FG/MG/BG, mood references, named assets, choreography where every element gets a verb, transition, depth layers, SFX cues.
- **كيف / how:** Energy verbs: high SLAMS/CRASHES/PUNCHES/STAMPS/SHATTERS; medium CASCADE/SLIDES/DROPS/FILLS/DRAWS; low types on/FLOATS/morphs/COUNTS UP/fades in.
- **أرقام / params:** 8-10 visual elements per beat; 2-3 techniques per beat; >= 2 depth layers; slow push e.g. scale 1->1.04 per beat
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/step-4-storyboard.md`

#### STORY-249 · تركيبات التقنيات حسب طاقة الفيديو · Technique combos by video energy · 📄 موصوف
- **ماذا / what:** Preset combinations: high-impact launches, cinematic tours, technical dev tools, premium/luxury, data-driven.
- **كيف / how:** Pick the row matching the brief and use 2-3 of its techniques per beat.
- **أرقام / params:** high impact: per-word type + velocity transitions + counters; cinematic: path drawing + video compositing + CSS 3D; technical: typing + canvas procedural + motion path; premium: variable font + Lottie + slow transitions; data: canvas + counters + path drawing
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### STORY-250 · هياكل قصة العرض بالثواني · Demo story structures with second budgets · 📄 موصوف
- **ماذا / what:** Three proven arcs for product films with per-section seconds; vary durations to avoid slideshow pacing.
- **كيف / how:** Map voice segments to these slots; one idea per scene; problem scenes chaotic/red, solution scenes spacious/green.
- **أرقام / params:** Classic 30-60s: hook 3, problem 5, magic moment 5, proof 15, social proof 4, invite 4; Problem-solution 20-40s: before 6, after 6, how 10, CTA 4; Teaser 15s: hook 2, demo 8, logo 3, tagline 2
- **الدليل / proof:** `kosif-atlas/skills/166-demo-video/535-demo-video`

#### STORY-251 · أطر كتابة الصفحات كهيكل للفيديو · Landing copy frameworks as video skeletons · 📄 موصوف
- **ماذا / what:** PAS (problem, agitate, solution), AIDA (attention, interest, desire, action) and BAB (before, after, bridge) give a promo its spine; alternate proof modes down the timeline: demonstration, metric, customer, mechanism, action.
- **كيف / how:** Write the headline per framework, then assign each step a beat.
- **الدليل / proof:** `kosif-atlas/skills/198-product-skills/634-landing-page-generator` · `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director`

#### STORY-252 · إيقاع ظهور المتحدث وأنواع اللقطات · Talking-head cadence and shot taxonomy · 📄 موصوف
- **ماذا / what:** For creator videos return to the face within 30-45 s of any B-roll stretch; label each scene as talking head, screen recording, B-roll, 3D animation, graphic or split screen with a duration estimate.
- **كيف / how:** Write a visual production brief scene by scene from the script's B-roll cues.
- **أرقام / params:** max 30-45s away from face
- **الدليل / proof:** `kosif-atlas/skills/3067-youtube/13229-creator-visual-director`

#### STORY-253 · إثبات المنتج من اللقطة الأولى · Product-proof first frame · 📄 موصوف
- **ماذا / what:** The opening must show the product, object, evidence or thesis, not a generic gradient; product scenes need an input, a user action and a visible consequence; fictional data is labelled and metrics are never invented.
- **كيف / how:** Check frame 0 of every film against this rule.
- **الدليل / proof:** `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director` · `kosif-atlas/skills/880-superloopy/1941-superloopy-frontend/references/anti-slop.md` · `kosif-atlas/skills/1420-frontend-design-skills/3377-openai-frontend-design`

#### STORY-254 · إشارات التوقع في الثواني الأولى · Expectation cues in the first seconds · 📄 موصوف
- **ماذا / what:** Typography quality, consistent timing, confident loading states and copy tone in the first seconds create a halo that colours the whole impression; inconsistent timing reads as cobbled together.
- **كيف / how:** Lock one timing/easing system for the whole film and show a deliberate loading/arrival moment early.
- **أرقام / params:** an 800ms blank before results reads as broken; add skeleton
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3791-expectation-effect-design-cues`

#### STORY-255 · قاعدة خطّاف الثانية الأولى للفيديو القصير · One-second hook rule for short-form · 📄 موصوف
- **ماذا / what:** The first second of a reel must be understandable on its own: show a meaningful action or result, and let picture, spoken line and on-screen title support one idea without repeating the same words.
- **كيف / how:** Pick exactly one primary hook type (result-first, visible test, specific problem, surprising action, direct question). Frame 0 already shows the subject; on-screen text only when it adds clarity. Validate by watching the first 1 s muted and with sound.
- **أرقام / params:** hook window 0-1 s (vertical template), 0-3 s (general); one primary hook
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/218-social-video-hooks/SKILL.md` · `kosif-atlas/skills/2976-pwdev-social-media/12592-story-reels/SKILL.md`

#### STORY-256 · جدول نبضات زمني بعمود المعلومة الجديدة · Timed beat sheet with 'new information' column · 📄 موصوف
- **ماذا / what:** A short video is planned as rows of Time | exact spoken words | camera/screen action | what new information the viewer gains; a beat that adds nothing new is cut.
- **كيف / how:** Write the table before any animation. Change framing or introduce new evidence as soon as the current image has made its point. Put proof before long explanation; end with one CTA that follows from what was shown. Convert rows directly into timeline cues (words.json timings when audio exists).
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/218-social-video-hooks/SKILL.md` · `kosif-atlas/skills/101-video-skills/214-creator-video/SKILL.md`

#### STORY-257 · أربعة قوالب لفيديو صانع المحتوى · Four creator-video shapes · 📄 موصوف
- **ماذا / what:** Talking-head or founder videos fall into four shapes: The Test (same task two ways, measured), The Real Task (doing useful work), The Day (recurring problem in context), The Guided Screen (presenter beside a legible screen).
- **كيف / how:** Choose the shape the available footage can actually prove; never stage results. Turn the beat sheet into a shot list stating what can be filmed now vs missing. Record each spoken beat twice (precise + natural take); lens near eye level; leave caption/UI safe space.
- **أرقام / params:** 2 takes per beat
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/214-creator-video/SKILL.md`

#### STORY-258 · قوس الفيلم الإعلاني من المشكلة إلى الكشف · Brand film arc: problem to reveal · 📄 موصوف
- **ماذا / what:** A narrative brand film earns the product reveal through six beats: problem, escalation, turn, reveal, proof, landing - one claim per beat, a visual metaphor carrying the problem, the real product as proof.
- **كيف / how:** Storyboard major frames and transitions; use a limited set of recurring shapes and one motivated transition from 'problem world' to 'product world'; never redraw the logo from memory; rough cut for story clarity before polish; must still read muted.
- **أرقام / params:** 6 beats; 1 claim per beat
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/212-brand-film/SKILL.md`

#### STORY-259 · هيكل سكريبت يوتيوب الطويل · Long-form YouTube script skeleton · 📄 موصوف
- **ماذا / what:** Hook in the first 3 s (spoken, no B-roll, lead with the destination not the journey) -> cold open 30-90 s with stakes and an explicit 'by the end you will...' promise -> labeled segments with chapter and B-roll cues -> at least one live demonstration moment -> soft CTA about 2 min before the end -> …
- **كيف / how:** Write full spoken sentences (no bullets) with tags [CHAPTER: name ~m:s], [B-ROLL: ...], [IMPROVISE: ...]; infer length from research depth; these tags become timeline markers and motion-graphics cue lists.
- **أرقام / params:** ~150 wpm: 15 min ~2250 words, 20 min ~3000, 30 min ~4500, 45 min ~6750
- **الدليل / proof:** `kosif-atlas/skills/3067-youtube/13226-creator-script-agent/SKILL.md`

#### STORY-260 · خط إنتاج من ست مراحل لصانع المحتوى · Six-stage creator production pipeline · 📄 موصوف
- **ماذا / what:** Research brief -> script -> SEO/metadata -> visual director brief -> editor brief -> thumbnail brief; each stage consumes the previous stage's markdown so the final package is self-contained for an editor or AI tool.
- **كيف / how:** Emit each stage as a markdown file; mark missing upstream inputs as [MISSING: ...] instead of inventing; the visual brief lists scenes (shot type, description, duration), B-roll/graphics/demo lists, music and grade direction; the editor brief turns that into chapter-level cut instructions.
- **أرقام / params:** 6 stages; research brief: 5-10 signal sources from >=5-8 searches, a named core tension/hook angle, default 20 min target
- **الدليل / proof:** `kosif-atlas/skills/3067-youtube/13225-creator-research-agent/SKILL.md` · `kosif-atlas/skills/3067-youtube/13229-creator-visual-director/SKILL.md` · `kosif-atlas/skills/3067-youtube/13224-creator-editor-brief/SKILL.md`

#### STORY-261 · قائمة حزمة الجرافيك على الشاشة · On-screen graphics package list · 📄 موصوف
- **ماذا / what:** Every on-screen text graphic is listed with type, text, timestamp and style before editing: lower thirds, chapter titles, call-out boxes, stats overlays, and branded keyword call-outs when certain phrases are spoken.
- **كيف / how:** Produce a table Graphic | Text | ~timestamp | style notes from the script; drive the motion layer from it (one component per graphic type) and trigger keyword call-outs from words.json matches.
- **الدليل / proof:** `kosif-atlas/skills/3067-youtube/13229-creator-visual-director/SKILL.md` · `kosif-atlas/skills/3067-youtube/13224-creator-editor-brief/SKILL.md`

#### STORY-262 · علامات لحظات الهوية · Brand-moment flags · 📄 موصوف
- **ماذا / what:** Mark the few moments where the presenter embodies the channel identity (return with the find, reveal of what was built, verdict) so the editor holds on the face and lets energy land.
- **كيف / how:** Add a flag block per moment with timestamp, moment type, presenter action and editor note; in motion graphics, give these moments a signature treatment (color push, longer hold, sting).
- **الدليل / proof:** `kosif-atlas/skills/3067-youtube/13229-creator-visual-director/SKILL.md`

#### STORY-263 · وسم نية الاكتشاف: بحث أم تصفح · Discovery-intent tag (search vs browse) · 📄 موصوف
- **ماذا / what:** Every organic video declares how it will be found: Search (typed queries, ranks over months), Browse (home/suggested feeds, lives on CTR and early retention) or Both; no discovery logic means it is not a video idea yet.
- **كيف / how:** Search videos front-load the answer to the query and use real query phrasing in title; browse videos spend more on the opening and the thumbnail pattern-break.
- **الدليل / proof:** `kosif-atlas/skills/1520-digital-marketing-pro/4133-video-script/SKILL.md` · `kosif-atlas/skills/1520-digital-marketing-pro/4132-video-packaging/SKILL.md`

#### STORY-264 · اختبارات العنوان الخمسة · Five title tests · 📄 موصوف
- **ماذا / what:** Screen titles with five checks: completes 'I want ___', instant clarity, positive energy, uses the audience's native vocabulary, memorable enough to repeat aloud; prefer destination-led over journey-led phrasing.
- **كيف / how:** Score each candidate pass/fail per test in a table; also apply them to thumbnail text (readable in <1 s at mobile size, works without the face).
- **أرقام / params:** 5 tests
- **الدليل / proof:** `kosif-atlas/skills/3067-youtube/13227-creator-seo-agent/SKILL.md` · `kosif-atlas/skills/3067-youtube/13228-creator-thumbnail-agent/SKILL.md`

#### STORY-265 · عائلات استراتيجية العنوان · Title strategy families · 📄 موصوف
- **ماذا / what:** Four title strategies: direct benefit ('How to X to Y'), curiosity gap (honest intrigue), authority/definitive ('complete guide'), trending/urgency (update videos); evergreen favours searchable keywords, trending favours curiosity.
- **كيف / how:** Generate 5-10 titles across strategies with keywords, character count and strategy label; research the top 5-10 competing titles for patterns and unused angles first.
- **أرقام / params:** 5-10 titles; <60 chars
- **الدليل / proof:** `kosif-atlas/skills/1817-youtube-strategy/4868-yt-packaging/SKILL.md`

#### STORY-266 · ثلاثة خطافات بديلة لكل سكريبت · Three-hook variants per script · 📄 موصوف
- **ماذا / what:** Every script ships three distinct opening hooks for the first 3 s, each using a different technique (bold claim, question, visual shock, pattern interrupt, relatable pain, curiosity gap) with a reason it fits the audience.
- **كيف / how:** Render the three openings as alternative first scenes of the same composition (props switch) so they can be A/B tested without re-editing the body.
- **أرقام / params:** 3 hooks x 3 s
- **الدليل / proof:** `kosif-atlas/skills/1520-digital-marketing-pro/4133-video-script/SKILL.md` · `kosif-atlas/skills/192-marketing-skills/617-video-content-strategist/SKILL.md`

#### STORY-267 · نقاط تسرّب المشاهدين وعلاجها · Retention risk points and holds · 📄 موصوف
- **ماذا / what:** Long-form scripts name 2-3 likely drop points (setup stretch, mid-video sag, pre-CTA fade) and place a specific hold at each: a re-hook, an open loop paid off later, or a pattern interrupt; every body section must deliver its own payoff, never only set up the next.
- **كيف / how:** Annotate the script/timeline with RISK markers and the chosen hold; in motion graphics a pattern interrupt can be a scene-style switch, a camera jolt, or a kinetic stat card.
- **أرقام / params:** 2-3 risk points
- **الدليل / proof:** `kosif-atlas/skills/1520-digital-marketing-pro/4133-video-script/SKILL.md`

#### STORY-268 · خريطة توزيع الدعوة لاتخاذ إجراء · CTA placement map · 📄 موصوف
- **ماذا / what:** Short videos place one CTA at the natural climax; long videos use a soft mid-roll CTA plus a strong end CTA, across verbal, on-screen overlay, end card and pinned comment.
- **كيف / how:** Mark CTA cues on the timeline with their rationale; build the end card as a reusable component held long enough to read.
- **أرقام / params:** short: 1 CTA; long: soft mid + strong end; end CTA within final 60 s
- **الدليل / proof:** `kosif-atlas/skills/1520-digital-marketing-pro/4133-video-script/SKILL.md` · `kosif-atlas/skills/192-marketing-skills/617-video-content-strategist/SKILL.md`

#### STORY-269 · مكتبة أنماط الخطاف المسماة · Named hook pattern library · 📄 موصوف
- **ماذا / what:** Nine named opening patterns: contrarian, question, narrative cold-open, data point, list preview, strong claim, empathy, before/after, confession; each has conditions under which it works.
- **كيف / how:** Generate 5-7 variants in different patterns (never 5 of the same), label each with its pattern, recommend one; for video the hook lives in the first 1-3 s both spoken and on screen; prefer verbatim audience language as raw material.
- **أرقام / params:** 5-7 variants; video hook 1-3 s
- **الدليل / proof:** `kosif-atlas/skills/2964-pwdev-copy/12448-copy-hooks/SKILL.md` · `kosif-atlas/skills/192-marketing-skills/611-social-content/SKILL.md`

#### STORY-270 · الصورة يجب أن تحمل حجة · Visual must carry an argument · 📄 موصوف
- **ماذا / what:** Test any concept by removing the image: if nothing is lost, the visual only decorates. Choose a mechanism: dominant typography, before/after contrast, product demonstration, visualized data, human face, or (sparingly) metaphor.
- **كيف / how:** Write one sentence of what the piece must make the viewer understand or feel in 2 s; define what repeats across the campaign (grid, band, logo position, treatment) vs what varies; avoid illustrating the copy literally (arrow up for 'growth').
- **أرقام / params:** 2 s comprehension
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12583-creative-concept/SKILL.md`

#### STORY-271 · قالب بطاقة المشهد في الستوري بورد · Scene card storyboard schema · 📄 موصوف
- **ماذا / what:** Each scene is a card: number + duration, visual, base image file, camera movement (static/pan/dolly/orbital), on-screen text + position inside safe area, caption transcript, motion prompt.
- **كيف / how:** Store cards as JSON next to the composition; the renderer reads durations and texts from it so storyboard and film never drift.
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12594-video-gen/SKILL.md` · `kosif-atlas/skills/2414-animation/9356-produce/SKILL.md`

#### STORY-272 · بنية الفيديو الطويل حسب الاحتفاظ · Long-form video architecture by retention · 📄 موصوف
- **ماذا / what:** Hook 0-30 s, context 30-90 s (who it is for, what they will learn), body ~90% of runtime structured Problem -> Solution -> Example -> Result per point, CTA in the final 60 s; chapters for videos over ~6-8 minutes.
- **كيف / how:** Put the primary keyword in the title's first 60 chars, the first 2 description sentences, and say it in the first 30 s; chapter markers come from the beat list.
- **أرقام / params:** hook 0-30 s; context 30-90 s; CTA last 60 s; chapters >6-8 min
- **الدليل / proof:** `kosif-atlas/skills/192-marketing-skills/617-video-content-strategist/SKILL.md`

#### STORY-273 · تصنيف زوايا استخراج القصص · Story-mine angle taxonomy · 📄 موصوف
- **ماذا / what:** A lived story usually hides several pieces: the lesson, the contrarian take, the framework, the proof (number/before-after), and the relatable moment; return only the angles that genuinely hold.
- **كيف / how:** Draft openings lead with the surprise, number or reversal, never chronology ('It started when...'); never improve facts; anonymise client details by default.
- **أرقام / params:** 5 angle types; return 3-5
- **الدليل / proof:** `kosif-atlas/skills/1520-digital-marketing-pro/4122-story-mine/SKILL.md`

#### STORY-274 · مؤشرات بحثية لصياغة العناوين · Headline evidence priors · 📄 موصوف
- **ماذا / what:** Large headline experiments suggest numbers, concreteness and stories about individuals raise clicks; each extra negative word associated with ~2.3% higher CTR (not a license for fear); informativeness is inverted-U; word features predicted A/B winners only ~55% of the time, so generate materially di…
- **كيف / how:** Use as weak priors; build a fact sheet first and keep every claim traceable; vary what leads (actor, verb, number, consequence, deadline, image).
- **أرقام / params:** ~2.3% CTR per negative word; ~55% predictability; Upworthy 32,487 tests (2013-2015)
- **الدليل / proof:** `kosif-atlas/skills/2218-majestic-writing/8393-headline-generator/references/evidence.md` · `kosif-atlas/skills/2218-majestic-writing/8393-headline-generator/SKILL.md`

#### STORY-275 · إيجاد شحنة التوتر في العنوان · Finding the headline charge · 📄 موصوف
- **ماذا / what:** Strong titles express a true tension: expected vs actual, promise vs cost, belief vs measured finding, small cause vs big consequence, deadline vs affected group, old state vs verified change, or two concrete ideas that gain meaning together.
- **كيف / how:** State 2-4 charges in plain words before styling; generate 10-20 raw candidates, keep 3-5 per format with the supporting fact noted; cut words until cutting removes truth.
- **أرقام / params:** 10-20 raw, 3-5 keepers
- **الدليل / proof:** `kosif-atlas/skills/2218-majestic-writing/8393-headline-generator/SKILL.md`

#### STORY-276 · أنواع مرشحي الخطاف · Hook candidate types · 📄 موصوف
- **ماذا / what:** Offer 3-5 hooks of different types: result-first (climax first, then how we got here), contrast (ordinary start vs peak; day vs night), interruption (cut right before an action completes), list (one shot of each of three places, the last revealed at the end), reason (the why of the trip). Only open …
- **كيف / how:** If no material creates curiosity, propose a cold open only rather than faking tension. Present a candidate table with source in/out, length, on-screen text, score, the loop it opens and its closing timestamp.
- **أرقام / params:** 3-5 candidates; each with closing TC
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/references/hook-principles.md`

#### STORY-277 · مبادئ الخطاف من أبحاث صناع المحتوى · Hook principles from creator research · 📄 موصوف
- **ماذا / what:** The hook's single job is to help the viewer decide to keep watching: the subject is clear in 1-2 s, the first 5-7 s confirm the click (show the thumbnail's subject; showing beats saying because autoplay previews are muted), minimal context up front, intro <=45 s, curiosity from contrast/contradictio…
- **كيف / how:** Use plain words a 10-11 year old reads instantly, active voice, one reading only, viewer-centred benefits, no answer in the curiosity line.
- **أرقام / params:** subject by 1-2 s; confirm in 5-7 s; intro <=45 s
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/references/hook-principles.md`

#### STORY-278 · مقاييس أسلوب المقال المرئي · Essay edit style metrics · 📄 موصوف
- **ماذا / what:** Argument-led faceless explainer: hook 0:15 (question + personal line), why-it-matters 0:30, 3-5 principles at 0:35-0:45 each, my take 0:40, data 0:45, misconceptions 0:30, conclusion 0:20, next action 0:15.
- **كيف / how:** Average shot 3.3 s (2.5-4.0), first-minute cuts 20 (15-25), max same screen 8 s, cards/source material 40% (30-50%: principle cards 15%, source docs 10%, tables 10%, logos/reactions 5%); cuts only, no dissolves; card transitions act as beat transitions; no full dialogue subtitles.
- **أرقام / params:** ASL 3.3 s; 20 cuts first min; cards 40%; 5-7 min
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2461-davinciresolve-style-essay/SKILL.md`

#### STORY-279 · مقاييس أسلوب يوميات المشروع · Project-diary edit style metrics · 📄 موصوف
- **ماذا / what:** Build/diary videos show goal -> attempt -> obstacle -> choice -> result: cold open 0:20, context 0:45, starting point 0:40, attempts 1:00, decisions 1:10, turning point 0:40, before/after 0:50, reflection 0:35, next episode 0:15.
- **كيف / how:** Average shot 8 s (5-12), first-minute cuts 3 (2-6), max same screen 40 s, B-roll 30% (20-40%), timelapse only for visible change (10-20 s), 12-frame dissolves only around timelapses; never hide what got stuck.
- **أرقام / params:** ASL 8 s; 3 cuts first min; dissolve 12 frames
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2462-davinciresolve-style-project/SKILL.md`

#### STORY-280 · مقاييس أسلوب التأمل الشخصي · Reflection edit style metrics · 📄 موصوف
- **ماذا / what:** Opinion/reflection videos: cold open 0:25 (question + teaser of 2-3 strongest lines from later beats), situation 0:45, trigger event 1:00, thought 1 1:15, counter-view 1:00, most honest thought 1:15, conclusion 0:40, next action 0:15.
- **كيف / how:** Average shot 3.8 s (3-5), 15 cuts/min (12-20), first minute 20 cuts, max same screen 6 s, voice present 70% (60-80%) of runtime, 12-20 frame dissolves only at beat changes; dialogue subtitles bottom-centre, 8% margin, 5.5% glyph height, ~18 chars/line.
- **أرقام / params:** ASL 3.8 s; 15 cuts/min; voice 70%; subtitles 5.5% height
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2463-davinciresolve-style-reflection/SKILL.md`

#### STORY-281 · قوالب قصة ديمو المنتج · Product demo story templates · 📄 موصوف
- **ماذا / what:** Classic 30-60 s: hook 3 s -> problem 5 s -> magic moment 5 s -> proof 15 s -> social proof 4 s -> invite 4 s. Problem-solution 20-40 s: before 6 s -> after 6 s -> how 10 s -> CTA 4 s. Teaser 15 s: hook 2 s -> demo 8 s -> logo 3 s -> tagline 2 s.
- **كيف / how:** Vary durations (hooks short, proof long) to avoid slideshow pacing; one focus per scene: title=product name, problem=pain (red, chaotic), solution=result (green, spacious), feature=highlighted region, end=URL/CTA.
- **أرقام / params:** see what
- **الدليل / proof:** `kosif-atlas/skills/166-demo-video/535-demo-video/SKILL.md`

#### STORY-282 · لكل مرجع مهمة واحدة · One job per reference · 📄 موصوف
- **ماذا / what:** Assign each reference a single job (motion/transformation, camera and easing, or brand identity) with an explicit do-not-copy list, and state 'do not average the references' so styles do not blend into mush.
- **كيف / how:** When studying several finished films, keep only what is constant across at least three (how scenes are declared, how entrances hit, how the last 3 s are built); anything unique to one film is its costume.
- **الدليل / proof:** `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`

#### STORY-283 · بوابة الإنتاج: اللوحات أولًا · Boards-first animation production gate · 📄 موصوف
- **ماذا / what:** A film is not rendered until boards are approved: brief, style guide, palette (ink, paper, tone levels), character/element sheets rendered from scene modules, a storyboard of panels {shot, panel, t, png, action, camera, caption}; only then a shots list {fps, size, shots [{id, t0, t1, scene, pack}]} …
- **كيف / how:** Scene modules expose renderFrame(t) and renderDrawing(k); an approval digest invalidates when boards change; audio is muxed afterwards with ffmpeg.
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9356-produce/SKILL.md`

#### STORY-284 · أقواس السرد للعروض وعناوين الادعاء · Deck narrative arcs and claim headlines · 📄 موصوف
- **ماذا / what:** Arc by deck type: investor (problem, solution, market, product, traction, team, ask), sales (problem, solution, proof, offer, next step), conference (hook ~30 s, context, insight, evidence, takeaway), internal SCQA (situation, complication, question, answer, evidence, next steps). Each slide headlin…
- **كيف / how:** Lock the narrative before any visual work; spec each slide: claim headline, visual treatment, supporting content, layout notes, brand notes. Works equally as a script skeleton for explainer motion videos.
- **الدليل / proof:** `kosif-atlas/skills/1567-tonone/4422-form-deck/SKILL.md` · `kosif-atlas/skills/2280-developer-relations/8704-conference-talk-and-cfp/SKILL.md` · `kosif-atlas/skills/1498-thermal-fluid-research-workflow/3719-research-slide-design/SKILL.md`

#### STORY-285 · اختيار إطار القصة المناسب · Story framework chooser · 📄 موصوف
- **ماذا / what:** Pick an arc by job: hero's journey compressed to 8 stages (ordinary world, call, hesitation, mentor, threshold, trials, reward, return) for brand stories and case studies; PAS for short ads; Before-After-Bridge for feature announcements; StoryBrand 7 parts for messaging; three-act for demos; Pixar c…
- **كيف / how:** Make the viewer the hero and the product the mentor; never skip the trials (friction makes the triumph credible); run a 3-second 'who is the protagonist?' check.
- **أرقام / params:** hero's journey 8 stages; StoryBrand 7
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3732-archetypes-storytelling-arcs/SKILL.md` · `kosif-atlas/skills/1503-universal-design-principles/3732-archetypes-storytelling-arcs/references/narrative-frameworks.md`

#### STORY-286 · قالب و-لكن-لذلك وقوس التحول للشرح · ABT and transformation arc for explainers · 📄 موصوف
- **ماذا / what:** And-But-Therefore gives clarity-driven explainers a minimal tension structure; a transformation arc creates a 'how did you know?' recognition moment for pain-led content; case-study pattern offers proof without pressure.
- **كيف / how:** Choose by goal: recognition -> transformation arc; clarity -> ABT; proof -> case study. For live talks: webinar = arc then ABT; workshop = ABT then application.
- **الدليل / proof:** `kosif-atlas/skills/1164-leaderize-storytelling-framework/2746-leaderize-storytelling-framework/instructions.md`

#### STORY-287 · نتائج المشهد: نعم-لكن ولا-و · Try/fail scene outcomes · 📄 موصوف
- **ماذا / what:** Each scene's goal resolves as yes, no, yes-but or no-and; runs of clean 'yes' drain tension, so prefer the complicating outcomes; pair scenes with sequels (reaction, dilemma, decision).
- **كيف / how:** Tag beats in a narrative motion piece with their outcome and check that the middle does not resolve too easily.
- **أرقام / params:** 4 outcomes
- **الدليل / proof:** `kosif-atlas/skills/1213-story-skills/2883-scene-craft/SKILL.md` · `kosif-atlas/skills/1213-story-skills/2877-plot-structure/SKILL.md`

#### STORY-288 · عصف ذهني للثمبنيل يبدأ بالنفس · Psychology-first thumbnail brainstorm · 📄 موصوف
- **ماذا / what:** Start from what the viewer should wonder and feel, not what to show: 2-3 questions, 1-2 emotions (curiosity, unease, trust, vulnerability, surprise), a one-phrase problem as hero, elements that produce each, then 2-3 directions with a note of what lands in the top half.
- **كيف / how:** Turn each direction into an HTML/CSS thumbnail layout and render variants with Playwright at 1280x720.
- **أرقام / params:** 2-3 questions; 1-2 emotions; 2-3 directions
- **الدليل / proof:** `kosif-atlas/skills/1101-akbun-writing/2486-akbun-thumbnail-review/SKILL.md`

#### STORY-289 · استخراج الجواهر من التفريغ · Transcript nugget extraction · 📄 موصوف
- **ماذا / what:** Turn a raw talk/podcast transcript into content: extract 15-25 nuggets using three filters (what surprised, what challenged an assumption, what you would repeat over coffee), each with a provisional headline and signal score, select 2-4, write a creative brief (angle, assumption to disturb, structur…
- **كيف / how:** Use the same nuggets to choose short-clip windows from the user's audio and to title animated quote cards.
- **أرقام / params:** 15-25 nuggets; pick 2-4
- **الدليل / proof:** `kosif-atlas/skills/1181-transcript-to-content-pipeline/2789-transcript-to-content-pipeline/instructions.md`

#### STORY-290 · تصنيف صيغ الافتتاح الفيروسية · Viral opener formula classification · 📄 موصوف
- **ماذا / what:** Classify an opener into named shapes: flat contrarian one-liner, odd-precision number, build-in-public confession, quote reframe, mini-list, relatable cold open, listicle promise, story starting at the tension, surprising result with mechanism withheld, 'how I' teardown, third-person case-study flex…
- **كيف / how:** Use to turn a studied reference into a reusable hook template for the opening card of a reel.
- **أرقام / params:** 11 formulas
- **الدليل / proof:** `kosif-atlas/skills/3035-x-skills/13065-x-hook-extractor/SKILL.md` · `kosif-atlas/skills/3035-x-skills/13065-x-hook-extractor/references/classification-rules.md`

#### STORY-291 · مزيج محاور المحتوى ووتيرة النشر · Content pillar mix and cadence · 📄 موصوف
- **ماذا / what:** Example pillar mix: industry insights 30%, behind-the-scenes 25%, educational 25%, personal 15%, promotional 5% (promotion above ~20% reduces reach); 3-5 pillars each tied to a metric (reach, trust, conversion); a cadence the creator can hold for a year beats daily-then-quit.
- **كيف / how:** Plan series of motion templates per pillar so production cost per post drops.
- **أرقام / params:** 30/25/25/15/5 %
- **الدليل / proof:** `kosif-atlas/skills/192-marketing-skills/611-social-content/SKILL.md` · `kosif-atlas/skills/2264-creator-economy-operations/8628-plan-content-and-audience-growth/SKILL.md`

#### STORY-292 · هيكل الديمو: النتيجة أولًا · Do-it-first demo structure · 📄 موصوف
- **ماذا / what:** Open on the compelling 'after' result, then peel back only the layers the audience asks for; map each beat to a pain and its impact and cut beats with no pain; pre-script honesty boundaries ('on the roadmap', 'we don't do that - here's the workaround').
- **كيف / how:** Apply to product explainers: first scene shows the end state, subsequent scenes rewind to how.
- **الدليل / proof:** `kosif-atlas/skills/2375-sales-engineering/9185-demo-design/SKILL.md`

#### STORY-293 · هياكل الفيديو التعليمي حسب النوع · Tutorial video structures by type · 📄 موصوف
- **ماذا / what:** Feature tutorial 15-30 min: hook 30-60 s, context 1-2 min, core 10-20 min, advanced 2-3 min, CTA 1-2 min. Update video 10-20 min: hook 30 s, overview 1-2, walkthrough 8-15, impact 1-2, CTA 1. Use-case 15-30 min: hook with outcome, problem, solution overview, live build, results with metrics, CTA. Fu…
- **كيف / how:** Each section lists talking points, what is on screen, demo steps with expected outcome and a backup plan, and a running time total; reach the first 'wow' as fast as possible.
- **أرقام / params:** see what
- **الدليل / proof:** `kosif-atlas/skills/1817-youtube-strategy/4867-yt-outline/SKILL.md` · `kosif-atlas/skills/1817-youtube-strategy/4865-yt-brief/SKILL.md`

#### STORY-294 · توليد الأفكار وتصنيفها · Idea generation and tiering · 📄 موصوف
- **ماذا / what:** Generate 15-20 raw ideas through gap analysis, trend riding, format innovation and audience questions; label each with working title, tier (growth vs supporting), type, one-line angle and timeliness; aim for 60-70% growth-tier ideas; filter for audience fit, demonstrability and asset giveaway potent…
- **كيف / how:** Brief per chosen idea: angle (specific and defensible), audience, 5-8 key points, value proposition, CTA asset, prerequisites, demo needs, length, urgency.
- **أرقام / params:** 15-20 ideas; 60-70% tier 1; 5-8 key points
- **الدليل / proof:** `kosif-atlas/skills/1817-youtube-strategy/4866-yt-ideation/SKILL.md` · `kosif-atlas/skills/1817-youtube-strategy/4865-yt-brief/SKILL.md`

#### STORY-295 · بوابة اختيار الاستايل قبل التخطيط · Style-choice gate before planning · 📄 موصوف
- **ماذا / what:** Before any storyboard, keyframe values or code, offer 3-5 clearly different visual directions from a fixed 14-style menu; each option gets a one-line picture of the result, why it fits, its asset/effort trade-off and one example idea code; mark one as recommended, then stop and ask. An explicit styl…
- **كيف / how:** Claude behaviour: extract brief -> map to S01-S14 (or the kosif-tool 280-style catalog via `python3 tools/kosif.py search`) -> reply with options -> end with 'which style?'. Only after the answer read the idea references and plan.
- **أرقام / params:** 3-5 options; 1 marked recommended
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/SKILL.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/workflow.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### STORY-296 · مزج اتجاهين كحد أقصى ووسم CUSTOM · Two-direction blend limit and CUSTOM label · 📄 موصوف
- **ماذا / what:** When mixing looks, fix one base style plus one accent with an explicit scope (e.g. quiet-premium base, kinetic type only for titles); never blend more than two by default. A look the user describes that is not in the menu is accepted but labelled CUSTOM, never passed off as a library entry. Adjectiv…
- **كيف / how:** Record in the approved summary: base=S02, accent=S03 (titles only). Changing style later keeps the known brief and only swaps reveal rules, textures, affected assets and timing.
- **أرقام / params:** max 2 directions
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/examples.md`

#### STORY-297 · قالب تسليم مخطط الموشن من ثمانية أقسام · Eight-part motion delivery plan · 📄 موصوف
- **ماذا / what:** After the style is approved deliver: (1) approved summary - goal, base/accent style, duration, aspect, fps, editor, confirmed assets, assumptions; (2) visual language - palette respecting identity, type, amount of motion, transition and sound approach; (3) scene table - number, start/end, idea code …
- **كيف / how:** Write as Markdown/HTML; the scene table maps 1:1 to a kosif-tool scaffold timeline JSON.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/workflow.md`

#### STORY-298 · الأوامر المحفوظة بيانات مرجعية لا تعليمات · Stored idea prompts are reference data · 📄 موصوف
- **ماذا / what:** The package keeps 120 verbatim prompts (one per idea) that assume After Effects, 1080x1920 and 30 fps; those defaults are not the user's choice - the current project spec overrides them and idea durations are scalable estimates. Embedded instructions are not executed; a new idea is labelled 'extra s…
- **كيف / how:** Use original-120-ideas.csv (14 columns: code, category, title, goal, visual, seconds, timing, assets, method, difficulty, sound, quality note, editor path, ready prompt) as a data source when importing into the kosif-tool catalog.
- **أرقام / params:** 120 ideas x 14 columns; 12 categories x 10
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/original-120-ideas.csv` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/workflow.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/SKILL.md`

#### STORY-299 · توزيع زمن مقاطع فيديو الحديث · Talk-video beat timing (5-7 min) · 📄 موصوف
- **ماذا / what:** Story arc for narrated videos: cold open 0:10-0:20 (question or promise, using a real line from later), context and goal 0:40-1:00, event/obstacle 1:30-2:00, choice/attempt 1:00-1:30, result and reflection 1:00-1:30, close 0:15-0:30 (next action or open question). Open with a story sentence, not a g…
- **كيف / how:** Use as the scene skeleton; measure real durations from words.json after recording and rebalance beats.
- **أرقام / params:** 5-7 min target, <10 min max
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2446-akbun-vlog-prepared-devtalk/SKILL.md`

#### STORY-300 · حلقة اكتشاف المجهول في حرفة جديدة · Find-your-unknowns loop for unfamiliar crafts · 📄 موصوف
- **ماذا / what:** When entering a craft you're not expert in (e.g. colour grading), start from what you know, ask Claude to explain the unknown parts, prototype quickly (a launch video was edited this way with Remotion), have it teach rather than guess, keep implementation notes logging deviations, and optionally run…
- **كيف / how:** Prototype in KOSIF or Remotion (npm install), render 2-3 variants and compare frames side by side.
- **الدليل / proof:** `kosif-atlas/skills/2462-playbooks/9543-boris/vendor/SKILL.md`

#### STORY-301 · إعادة توظيف مصدر واحد لقنوات متعددة · Repurpose one source into channel derivatives · 📄 موصوف
- **ماذا / what:** Inventory the source's thesis, evidence, examples and quotes; mark which stand alone; map each to a channel, format and action; rewrite natively while preserving claim scope and attribution; publish in sequence; every derivative must trace back to the source and add context rather than duplicate.
- **كيف / how:** From a long video transcript -> list of 15-60 s clip candidates with timestamps -> ffmpeg cut + reframe + captions.
- **الدليل / proof:** `kosif-atlas/skills/2211-majestic-marketing/8287-content-repurposing/SKILL.md`

#### STORY-302 · عدسات المراجعة الإبداعية · Creative review lenses · 📄 موصوف
- **ماذا / what:** Two critique passes before render: subtract until each frame states one intent and can be explained in one sentence (seven diagnostic rows mapped to a 10-point score), and choose the motion register from the surface: Persuade (ads/landing - earn attention), Operate (tools - scanability), Read (docs/…
- **كيف / how:** Checklist step in the delivery plan.
- **أرقام / params:** 7/7 -> 10, 6/7 -> 9, 5/7 -> 7
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14123-steve-jobs-design-review/SKILL.md` · `kosif-atlas/skills/1709-uizze/4716-anti-ui-slop/SKILL.md`

#### STORY-303 · بنية الفيديو القصير · Short-form structure 0-1-3 s · 📄 موصوف
- **ماذا / what:** Vertical clips: hook in 0-1 s that works muted and without context, develop 1-3 s, deliver after 3 s, CTA inside safe zone; every story card must stand alone because viewers enter mid-sequence. Burned-in captions are mandatory.
- **كيف / how:** Plan beat table (time/say/show/new info); captions in safe zone not footer
- **أرقام / params:** hook ≤1 s
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12592-story-reels/SKILL.md` · `kosif-atlas/skills/101-video-skills/218-social-video-hooks/SKILL.md`

#### STORY-304 · ترجمة مذكرات السفر · Travel-note caption tone · 📄 موصوف
- **ماذا / what:** Short factual captions that give place, time and mood ('9 AM, market alley') instead of describing what is visible; commas only, no full stops/exclamations; chapter title bottom-left 0.5 s after scene start for 3 s, no captions while it shows.
- **كيف / how:** Text+ Size 0.12 (1.5x default 0.08), chapter 0.16, line spacing 1.2, bottom margin 8% (≈173 px at 4K), ≤2 lines, ≈18 chars/line start
- **أرقام / params:** size 0.12/0.16; margin 8%
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2465-davinciresolve-subtitle-travelnote/SKILL.md`

#### STORY-305 · هيكل فيديو الشرح · Explainer beat structure (5-7 min) · 📄 موصوف
- **ماذا / what:** Hook (question + personal line) 0:15 -> why this matters 0:30 -> 3-5 principles at 0:35-0:45 each -> my take 0:40 -> evidence/before-after 0:45 -> 2-3 misconceptions 0:30 -> conclusion 0:20 -> next action 0:15; hook within first 10 s; ≥3 chapters 10 s apart.
- **كيف / how:** Beat sheet confirmed by user, then assemble segments per beat with CHAPTER/GFX markers
- **أرقام / params:** 5-7 min
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2461-davinciresolve-style-essay/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2460-davinciresolve-story-devtalk/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2451-davinciresolve-beats-devtalk/SKILL.md`

#### STORY-306 · التجميع حسب النص المفرغ · Transcript-first beat assembly · 📄 موصوف
- **ماذا / what:** Transcribe all clips into an inventory (file, camera, face flag, length, sentence count, one-line gist), propose a beat sheet grounded only in what was actually said, get user approval, then lay segments in beat order; never invent lines the speaker did not say.
- **كيف / how:** whisper word timestamps -> inventory table -> segment list -> timeline build (Resolve CreateTimelineFromClips or ffmpeg concat / Remotion Sequences)
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2451-davinciresolve-beats-devtalk/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2460-davinciresolve-story-devtalk/SKILL.md`

#### STORY-307 · لغة مونتاج المدينة · City montage shot grammar · 📄 موصوف
- **ماذا / what:** Open on establishing street/traffic/signage/light; alternate wide place shots, mid architecture/street, and details (food, signs, transit, nature); chain motion direction across cuts (train passes, camera moves, water/leaves); use the beat as a guide but don't cut on every beat; mix short and breath…
- **كيف / how:** Plan shot list with wide/medium/detail tags and motion vectors; cut to downbeats from a beat map
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2433-akbun-davinciresolve-cut-new-york/SKILL.md`

#### STORY-308 · مبادئ الخطاف · Hook principles · 📄 موصوف
- **ماذا / what:** The hook only helps the viewer decide to keep watching: topic clear within 1-2 s, it confirms the title/thumbnail promise (showing beats saying because autoplay previews are muted), plain active language at a 5th-6th grade reading level, aimed at one viewer type and their existing want, never promis…
- **كيف / how:** Write title/thumbnail first, then hook
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/references/hook-principles.md` · `kosif-atlas/skills/101-video-skills/218-social-video-hooks/SKILL.md`

#### STORY-309 · أنواع الخطافات · Hook archetypes · 📄 موصوف
- **ماذا / what:** Five openers: result-first, visible test/comparison, specific relatable problem, surprising action, direct question; pick one primary, add a second cue only for clarity; write a beat table (time/say/show/new info) and put proof before explanation.
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/218-social-video-hooks/SKILL.md` · `kosif-atlas/skills/101-video-skills/214-creator-video/SKILL.md`

#### STORY-310 · أشكال فيديو صانع المحتوى · Creator-video shapes · 📄 موصوف
- **ماذا / what:** Four proof-driven formats: the test (same task two ways, measure), the real task, the day (recurring problem in context), guided screen (presenter beside legible capture); record each beat twice (precise + natural take); watch final once muted and once with sound.
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/214-creator-video/SKILL.md`

#### STORY-311 · الصوت يحرك المحتوى لا يُرسم · Content-not-medium audio rule · 📄 موصوف
- **ماذا / what:** Avoid cliche equalizer bars, spectrum, note clip-art, strobes; let audio drive the narrative visual's behaviour.
- **كيف / how:** Design visual from story; use bands only as intensity.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/audio-reactive.md`

#### STORY-312 · ورقة الإيقاع القصصي من التفريغ · Beat sheet from transcript · 📄 موصوف
- **ماذا / what:** Build a material inventory from transcripts then a beat sheet (one message per beat, mapped to chapters).
- **كيف / how:** whisper -> segments; classify voice vs b-roll clips (speech > 50% of clip); user approves sheet.
- **أرقام / params:** speech>50% = voice clip
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2451-davinciresolve-beats-devtalk`

#### STORY-313 · أشكال المقطوعات حسب السياق · Song forms per context · 📄 موصوف
- **ماذا / what:** Loop 60-120s with intro once; boss 45-90s; title 40-80s hook in 8 bars; ambient 30-90s; jingle 2-6s 1-3 bars; change something audible every 8 bars.
- **كيف / how:** Section markers in score.
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural/references/music-composition.md`

#### STORY-314 · الخطاف في أول 10 ثوان · Hook in first 10 seconds · 📄 موصوف
- **ماذا / what:** Themes/songs put the hook in the first ~10s; 1-2 sung lines per bar max; verses show, chorus tells.
- **كيف / how:** Arrangement rule for music briefs.
- **أرقام / params:** 10s
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3892-music` · `kosif-atlas/skills/2475-songwriting/9606-song-form`

#### STORY-315 · ممنوعات بصرية · Visual anti-patterns · 📄 موصوف
- **ماذا / what:** Grain >3% opacity, uniform chromatic aberration, glass on light bg, bold weights on glass, springs without overshoot read cheap.
- **كيف / how:** Checklist during review.
- **أرقام / params:** grain ≤3%
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### STORY-316 · اختيار 3D عند الحاجة فقط · Choose WebGL only when 3D earns it · 📄 موصوف
- **ماذا / what:** Use 3D for spatial, volumetric, trajectory or huge-mark data; prefer 2D when labels/exact values dominate.
- **كيف / how:** Decision checklist before building.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/when-3d-is-justified.md`

#### STORY-317 · وصفة حسب المزاج · Style-recipe by mood · 📄 موصوف
- **ماذا / what:** Choose typography techniques by video mood.
- **كيف / how:** High impact: per-word type+velocity transitions+counters; Premium: variable-font anim+Lottie+slow transitions; Technical: typing+canvas+motion path.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### STORY-318 · اقترح 3-5 استايلات · Offer 3-5 style options before planning · 📄 موصوف
- **ماذا / what:** Before building, propose distinct directions with trade-offs and let the user choose.
- **كيف / how:** Present S-codes with reason/trade-off, ask once in Arabic, then plan.
- **أرقام / params:** 3-5
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-typography/SKILL.md`

#### STORY-319 · الأسلوب البسيط التحريري · Minimalist / Editorial look · 📄 موصوف
- **ماذا / what:** Document-flat surfaces, hairline borders, huge whitespace, colour as scarce spot pastels, off-black serif headlines, no shadows or gradients.
- **كيف / how:** Canvas #FFFFFF or bone #F7F6F3; border #EAEAEA; text #111111/#2F3437, secondary #787774; pastel pairs FDEBEC/9F2F2D, E1F3FE/1F6C9F, EDF3EC/346538, FBF3DB/956400. Motion: translateY 12px+fade over 600ms cubic-bezier(0.16,1,0.3,1).
- **أرقام / params:** radius ≤12px, line-height 1.6
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/aesthetic-systems.md`

#### STORY-320 · البروتالي / الطباعة السويسرية الصناعية · Brutalist / Swiss industrial print · 📄 موصوف
- **ماذا / what:** Swiss grid + industrial manual: 90° corners, visible compartments, one hazard red, mechanical motion.
- **كيف / how:** Paper #F4F4F0 or #EAE8E3, ink #050505-#111111, only accent aviation red #E61919/#FF2A2A; huge neo-grotesk headers clamp(4rem,10vw,15rem); 1-2px rules; no radius, no gradients, no soft shadows.
- **أرقام / params:** radius 0
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/aesthetic-systems.md`

#### STORY-321 · شاشة CRT تكتيكية · Tactical telemetry / CRT dark · 📄 موصوف
- **ماذا / what:** Dark sibling of brutalist: phosphor text on near-black, scanlines, terminal green on one element only.
- **كيف / how:** bg #0A0A0A/#121212 (never #000), fg #EAEAEA, red #E61919, green #4AF626 once; scanlines repeating-linear-gradient 2px transparent / 2px rgba(0,0,0,0.1).
- **أرقام / params:** scanline period 4px
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/aesthetic-systems.md`

#### STORY-322 · الأسلوب الناعم الزجاجي · Soft / Ethereal glass · 📄 موصوف
- **ماذا / what:** Haptic depth: OLED black with glowing purple/emerald radial mesh orbs, vantablack cards with heavy backdrop blur and 10% white hairlines; spring blur-up motion.
- **كيف / how:** bg #050505; cards backdrop-blur ~40px, border white/10; entry translateY 64px + blur(md) + opacity 0 -> rest over ~800ms cubic-bezier(0.32,0.72,0,1).
- **أرقام / params:** 700-800ms
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/aesthetic-systems.md`

#### STORY-323 · الفخامة التحريرية · Editorial luxury · 📄 موصوف
- **ماذا / what:** Warm cream, sage and espresso with high-contrast variable serif heads and faint film grain.
- **كيف / how:** bg #FDFBF7; grain overlay opacity 0.03; serif display (Fraunces/Instrument Serif/Editorial New class).
- **أرقام / params:** grain 3%
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/aesthetic-systems.md`

#### STORY-324 · البنيوية الناعمة · Soft structuralism · 📄 موصوف
- **ماذا / what:** Silver-grey or white, massive bold grotesk, extremely soft diffused ambient shadows; double-bezel nested squircle cards.
- **كيف / how:** Outer shell black/5 + ring black/5 + 6-8px padding + radius 2rem; inner core own bg with inset highlight.
- **أرقام / params:** radius 32px
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/aesthetic-systems.md`

#### STORY-325 · الفخامة المنضبطة · High-end calibrated restraint (Stitch) · 📄 موصوف
- **ماذا / what:** Warm-neutral zinc palette, one accent under 80% saturation, whisper borders, weight-driven hierarchy, spring motion only.
- **كيف / how:** Canvas #F9FAFB, surface #FFFFFF, ink #18181B, steel #71717A, slate #94A3B8, border rgba(226,232,240,0.5), shadow rgba(0,0,0,0.05); accent ONE of emerald #10B981, blue #3B82F6, rose #E11D48, amber #F59E0B. Spring stiffness 100 damping 20, stagger index*100ms; cards radius 2.5rem shadow 0 20px 40px -15px.
- **أرقام / params:** spring 100/20
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/aesthetic-systems.md`

#### STORY-326 · استراتيجيات جرعة لون العلامة · Brand colour dosage strategies · 📄 موصوف
- **ماذا / what:** Name the commitment level: Restrained (tinted neutrals + accent ≤10%), Committed (one saturated colour 30-60%), Full palette (3-4 named roles), Drenched (surface IS the colour).
- **كيف / how:** Pick one strategy per film and stick to it across scenes; name a reference.
- **أرقام / params:** ≤10% / 30-60% / 100%
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/aesthetic-systems.md`

#### STORY-327 · أنماط لوحة الهوية · Identity-board palette modes · 📄 موصوف
- **ماذا / what:** Eight ready moods for 3×3 identity boards: Dark Developer (near-black, mono, cyan/blue/coral/lime), Dark Operator (black/dark-red/amber), Dark Nature (deep green+lime), Dark Security (black/navy, red/blue alerts), Light Editorial (ivory, serif, blue/red/gold), Luxury (ivory/stone/espresso, emboss, g…
- **كيف / how:** Use as a moodboard picker; repeat one accent across all panels.
- **أرقام / params:** 3×3
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/aesthetic-systems.md`

#### STORY-328 · مولدات فكرة الشعار · Logo concept operators · 📄 موصوف
- **ماذا / what:** Build a mark from one (max two) of: Monogram+Meaning, Product Action, Metaphor Fusion, Negative Space, Construction Geometry.
- **كيف / how:** Pick operator, sketch on grid, test at 32px.
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/aesthetic-systems.md`

#### STORY-329 · لا تخلط بين الأنظمة الجمالية · Never mix aesthetic systems · 📄 موصوف
- **ماذا / what:** Each surface speaks one language: glass orbs on hairline bento, or scanlines under whisper shadows, cancel each other.
- **كيف / how:** Lock one system per film/sequence; contradictory rules (Inter allowed only in brutalist; shadows banned in brutalist, required in soft).
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/aesthetic-systems.md`

#### STORY-330 · تحديد الفاتح/الداكن من المشهد · Scene-first light/dark decision · 📄 موصوف
- **ماذا / what:** Dark vs light is never default: write one sentence about who watches, where, under what light and mood, and let it decide.
- **كيف / how:** Add to creative brief before palette.
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/aesthetic-systems.md`

#### STORY-331 · باليت الزجاجية · Glassmorphism preset · 📄 موصوف
- **ماذا / what:** Frosted translucent layers, subtle blur, luminous borders.
- **كيف / how:** Seed tokens: primary #1856FF, secondary #3A344E, success #07CA6B, warning #E89558, danger #EA2143, surface #FFFFFF, text #141414; fonts Plus Jakarta Sans / JetBrains Mono. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/glassmorphism/DESIGN.md`

#### STORY-332 · باليت النيوبروتالية · Neobrutalism preset · 📄 موصوف
- **ماذا / what:** Bold borders, vivid accents, raw high-contrast layout on warm surface.
- **كيف / how:** Seed tokens: primary #FDC800, secondary #432DD7, surface #FBFBF9, text #1C293C; scale 13/15/17/21/27/35; fonts Inter. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/neobrutalism/DESIGN.md`

#### STORY-333 · باليت النيومورفيزم · Neumorphism preset · 📄 موصوف
- **ماذا / what:** Extruded soft UI with paired inner/outer shadows on a monochrome surface.
- **كيف / how:** Seed tokens: primary #006666, secondary #F1F2F5, surface #E7E5E4, text #1E2938; fonts Space Mono. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/neumorphism/DESIGN.md`

#### STORY-334 · باليت النيون · Neon preset · 📄 موصوف
- **ماذا / what:** Electric glow, high-contrast pairings.
- **كيف / how:** Seed tokens: primary #BBF351, secondary #00BCFF; fonts Roboto / STIX Two Text. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/neon/DESIGN.md`

#### STORY-335 · باليت فينتج التسعينات · Vintage 90s OS preset · 📄 موصوف
- **ماذا / what:** Retro desktop nostalgia, grain, skeuomorphic touches.
- **كيف / how:** Seed tokens: primary #008080 teal, secondary/surface #C0C0C0, text #000000; fonts Silkscreen. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/vintage/DESIGN.md`

#### STORY-336 · باليت الأركيد · Pac-arcade preset · 📄 موصوف
- **ماذا / what:** Pixel fonts, dotted borders, black stage.
- **كيف / how:** Seed tokens: primary #2A3FE5, secondary #F4B9B0, surface #000000; fonts Press Start 2P. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/pacman/DESIGN.md`

#### STORY-337 · باليت التدرجات · Gradient-rich preset · 📄 موصوف
- **ماذا / what:** Smooth colour transitions, playful vivid surfaces.
- **كيف / how:** Seed tokens: primary #990FFA, secondary #E60076; fonts Montserrat / Space Grotesk. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/gradient/DESIGN.md`

#### STORY-338 · باليت الفخامة الداكنة · Luxury mono-dark preset · 📄 موصوف
- **ماذا / what:** Black stage, white type, monochrome premium.
- **كيف / how:** Seed tokens: surface #000000, primary/text #FAFAFA; fonts Oswald. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/luxury/DESIGN.md`

#### STORY-339 · باليت الدرامي · Dramatic preset · 📄 موصوف
- **ماذا / what:** Theatrical high-contrast immersive layouts.
- **كيف / how:** Seed tokens: primary #8B5CF6, secondary #F43F5E, surface #09090B, text #FAFAFA; fonts Outfit. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/dramatic/DESIGN.md`

#### STORY-340 · باليت الحيوي · Energetic preset · 📄 موصوف
- **ماذا / what:** Thick borders, geometric shapes, warm high-contrast.
- **كيف / how:** Seed tokens: primary #EA580B, secondary #F59E0B, surface #FDBA74; fonts Limelight. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/energetic/DESIGN.md`

#### STORY-341 · باليت البروتالية الخرسانية · Brutalism (concrete) preset · 📄 موصوف
- **ماذا / what:** Raw anti-design inspired by concrete architecture.
- **كيف / how:** Seed tokens: primary #DD614C, secondary #DAA144; fonts Darker Grotesque. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/brutalism/DESIGN.md`

#### STORY-342 · باليت المونو الماتريكس · Mono / matrix preset · 📄 موصوف
- **ماذا / what:** Monospace, matrix-like compact density.
- **كيف / how:** Seed tokens: primary #37F712, secondary #00A6F4, surface #E7E5E4; fonts Space Mono. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/mono/DESIGN.md`

#### STORY-343 · باليت البينتو · Bento preset · 📄 موصوف
- **ماذا / what:** Modular card grid, soft spacing.
- **كيف / how:** Seed tokens: primary #FAD4C0, secondary #80A1C1, surface #FFF5E6; fonts Inter. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/bento/DESIGN.md`

#### STORY-344 · باليت الدودل · Doodle preset · 📄 موصوف
- **ماذا / what:** Hand-drawn sketchy imperfect lines.
- **كيف / how:** Seed tokens: primary #49B6E5, secondary #263D5B; fonts Delius Swash Caps. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/doodle/DESIGN.md`

#### STORY-345 · باليت المطبوعات · Publication preset · 📄 موصوف
- **ماذا / what:** Print-inspired editorial for reports.
- **كيف / how:** Seed tokens: primary #A855F7, secondary/text #0A1829; fonts Nunito / Oswald. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/publication/DESIGN.md`

#### STORY-346 · باليت الفانتازيا · Fantasy game preset · 📄 موصوف
- **ماذا / what:** Game-inspired bold premium visuals.
- **كيف / how:** Seed tokens: primary #0250CC, secondary #FDC800; fonts New Rocker. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/fantasy/DESIGN.md`

#### STORY-347 · باليت السكيومورفيزم · Skeuomorphism preset · 📄 موصوف
- **ماذا / what:** Real-world textures and 3D physical metaphors.
- **كيف / how:** Seed tokens: primary #FA3C00, secondary #F08321; fonts Germania One / Roboto. Treat as a starting preset and run WCAG checks.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/skeumorphism/DESIGN.md`

#### STORY-348 · موجه علم نفس الجماليات · Aesthetic psychology router · 📄 موصوف
- **ماذا / what:** Pick emotional levers for brand films: aesthetic-usability effect, archetypes, exposure effect, wabi-sabi, baby-face bias for mascots, uncanny valley warnings, biophilia, prospect-refuge.
- **كيف / how:** Use as a checklist in the creative brief.
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3729-aesthetics-router`

#### STORY-349 · النماذج الأصلية للعلامة · Brand archetypes for voice and look · 📄 موصوف
- **ماذا / what:** Map a brand to an archetype (hero, sage, jester...) to align colour, type, music and VO tone.
- **كيف / how:** Pick archetype in brief, derive palette temperature and motion energy from it.
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3731-archetypes-brand-voice` · `kosif-atlas/skills/1503-universal-design-principles/3730-archetypes`

#### STORY-350 · المخطط يجادل لا يعرض · Diagrams must argue (isomorphism test) · 📄 موصوف
- **ماذا / what:** With text removed, the structure itself should communicate the idea; good diagrams teach concrete specifics.
- **كيف / how:** Pick a visual pattern matching meaning before drawing; include real examples for technical topics.
- **الدليل / proof:** `kosif-atlas/skills/2790-work/11181-draw-excalidraw`

#### STORY-351 · أسلوب رسم الكتب أحادي الرمادي · Monogray book illustration style · 📄 موصوف
- **ماذا / what:** Dark-gray ink hand lines + flat grays + one orange accent on off-white paper, in five fixed layouts (icon strip, zoom-in, dialogue, flow, poster card).
- **كيف / how:** SVG for editable layout + image-model prompt for fills; keep labels 2-6 chars, captions ~15 chars to reduce model text errors.
- **أرقام / params:** 1 accent color
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2415-akbun-draw-book-illustration`

#### STORY-352 · بطاقة كراسة الرسم · Spiral sketchbook concept card · 📄 موصوف
- **ماذا / what:** Pencil sketchbook page with handwritten number, uppercase title, underline, 2-4 checkmarks and a framed pencil illustration of the concept.
- **كيف / how:** Build as SVG/HTML layout with hand font and pencil-texture filter, or prompt an image model; animate the checkmarks drawing on.
- **أرقام / params:** 2-4 checklist items
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2420-akbun-draw-sketchbook-card`

#### STORY-353 · إطار ستوري بورد بالقلم · Pencil storyboard frame spec · 📄 موصوف
- **ماذا / what:** 16:9 gray pencil sketch, only thin red lines for camera axis/eye line, dashed rectangle for frame, dimension notes below.
- **كيف / how:** Draw in SVG (rough strokes) or prompt image model; per-beat table: length, voice, screen type (B-ROLL/SCREEN/GRAPHIC IDEA), story role.
- **أرقام / params:** 16:9
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2448-akbun-vlog-shotsketch` · `kosif-atlas/skills/1096-akbun-editvideo/2449-akbun-vlog-storyboard`

#### STORY-354 · جدول الإيقاع واللقطة · Beat-to-shot story table · 📄 موصوف
- **ماذا / what:** Each beat has one story function; table lists narration, screen recording vs B-roll split, graphic idea, keyword captions and privacy check.
- **كيف / how:** Markdown table per cut, e.g. 0:40 = 25s screen + 15s B-roll.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2449-akbun-vlog-storyboard`

#### STORY-355 · حلقة الاسكتش والتعرف · Iterative sketch-recognize loop · 📄 موصوف
- **ماذا / what:** When the user cannot describe a look, present several concrete variant sketches and let them mark what fits until one is recognized.
- **كيف / how:** Produce 2-4 quick variants (stills or 3s loops), keep retained parents, revise only from marked versions.
- **أرقام / params:** 2-4 variants/round
- **الدليل / proof:** `kosif-atlas/skills/1995-hypotyposis/7163-sketch`

#### STORY-356 · عنوان الاستنتاج بدل عنوان الموضوع · Insight-first claim title · 📄 موصوف
- **ماذا / what:** Every chart scene carries a headline that states the finding (a number plus its impact) instead of naming the topic.
- **كيف / how:** Write the title as [specific number] + [impact] + [context], e.g. 'Exports up 23% after the new port' rather than 'Exports by month'. Subtitle holds date range, unit, filters and source. Write it before sketching the chart; if it cannot be written the scene is not ready. In Arabic voice-over videos, time the title reveal to the spoken number in words.json.
- **أرقام / params:** title + subtitle (unit, date, source)
- **الدليل / proof:** `kosif-atlas/skills/3455-business-analytics/14161-data-storytelling/references/details.md` · `kosif-atlas/skills/317-data/942-data-visualization/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10335-visualization-strategy-and-critique/SKILL.md`

#### STORY-357 · أسلوب النبض السويسري للبيانات · Swiss Pulse data style · 📄 موصوف
- **ماذا / what:** Clinical metrics look: black/white plus one electric accent, grid-locked, huge numbers that count up, hard cuts.
- **كيف / how:** Palette #1a1a1a, white, one accent #0066FF or #FFB300; Inter/Helvetica bold headlines; numbers 80-120 px; 12-column grid; easing expo.out/power4.out; transitions hard cut or geometric (zoom, iris).
- **أرقام / params:** #1a1a1a, #0066FF|#FFB300; 12 cols; 80-120 px numbers
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/visual-styles.md`

#### STORY-358 · أسلوب انجراف البيانات · Data Drift immersive style · 📄 موصوف
- **ماذا / what:** Futuristic data aesthetic where particles coalesce into numbers and light traces data paths.
- **كيف / how:** Deep black #0a0a0a, purple #7c3aed, cyan #06b6d4; thin light sans; extreme micro-to-macro scale shifts; sine.inOut/power2.out easing; warp-style transitions. Use particles as carriers that settle into the final readable figure.
- **أرقام / params:** #0a0a0a / #7c3aed / #06b6d4
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/visual-styles.md`

#### STORY-359 · قوس القصة البيانية · Data story arc · 📄 موصوف
- **ماذا / what:** Narrative skeleton for a data explainer video: hook, context, rising evidence, key insight, resolution, call to action.
- **كيف / how:** Open on the surprising number, set the baseline, add 2-3 evidence beats (rule of three), land the single insight, end on the recommendation. Lead with the 'so what', curate ruthlessly, method after context.
- **أرقام / params:** 3 evidence beats
- **الدليل / proof:** `kosif-atlas/skills/3455-business-analytics/14161-data-storytelling/SKILL.md` · `kosif-atlas/skills/3455-business-analytics/14161-data-storytelling/references/details.md`

#### STORY-360 · الكشف التدريجي بالطبقات · Progressive reveal layering · 📄 موصوف
- **ماذا / what:** Start with one simple chart and add one layer per beat (growth rate, segment split, share, opportunity zone).
- **كيف / how:** Keep the same axes and position across beats so viewers track change; each beat adds exactly one new encoding or annotation and its VO sentence; dim previous layers to 30-40% opacity rather than removing them.
- **أرقام / params:** 1 new layer per beat
- **الدليل / proof:** `kosif-atlas/skills/3455-business-analytics/14161-data-storytelling/references/details.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali/references/story-patterns-and-scene-contracts.md`

#### STORY-361 · لوحة المقارنة قبل وبعد · Before/after contrast panel · 📄 موصوف
- **ماذا / what:** Two side-by-side states with the same metrics so the change is read instantly.
- **كيف / how:** Split screen or slide-over wipe; identical row order and units on both sides; animate the 'after' values counting from the 'before' values; emphasize the delta with the accent color only.
- **الدليل / proof:** `kosif-atlas/skills/3455-business-analytics/14161-data-storytelling/references/details.md` · `kosif-atlas/skills/2790-work/11181-draw-excalidraw/references/visual-patterns.md`

#### STORY-362 · كل مشهد يضيف دليلا · Every scene must add evidence · 📄 موصوف
- **ماذا / what:** A beat that only adds drama (zoom, particles, parallax) without a new fact is cut or simplified.
- **كيف / how:** Check each beat for one evidence-bearing change: new data layer, annotation shift, map reveal, meaningful camera move. Test: pause on any frame; the claim should still be readable.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali/references/story-patterns-and-scene-contracts.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10335-visualization-strategy-and-critique/SKILL.md`

#### STORY-363 · استنتج ثم اسأل من سؤال إلى ثلاثة · Infer then ask 1-3 questions · 📄 موصوف
- **ماذا / what:** Start from what the request implies, propose substrate/chart, and ask only the few questions that change the design.
- **كيف / how:** Infer purpose from domain words; recommend; list assumptions; ask 1-3 focused either/or questions (e.g. 'route context with roads, or terrain and rivers?'). Matches the owner's one-short-Arabic-message intake rule.
- **أرقام / params:** 1-3 questions
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/adaptive-basemaps-and-layer-stacks.md` · `kosif-atlas/skills/2957-posthog/12277-choosing-trend-or-slope-view/SKILL.md`

#### STORY-364 · تحويل المرجع لا نسخه · Reference transformation, not cloning · 📄 موصوف
- **ماذا / what:** When the user shows a famous infographic or data video, extract the principle and redesign for this data.
- **كيف / how:** Write what was learned (pacing, layering, label strategy), then build a composition that would not be mistaken for the reference: different palette, type, layout and cadence. Same license caution as for footage.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10335-visualization-strategy-and-critique/SKILL.md`

#### STORY-365 · اختبار القرار لكل مخطط · Decision test for every chart · 📄 موصوف
- **ماذا / what:** Each chart included must answer a question the viewer needs; otherwise cut it.
- **كيف / how:** Ask 'does this answer a decision or claim in the script?' for each visual; list the question next to each scene in the storyboard; decorative charts are removed.
- **الدليل / proof:** `kosif-atlas/skills/1567-tonone/4452-lens-chart/SKILL.md` · `kosif-atlas/skills/2354-power-platform/9080-report-visualization-design/SKILL.md`

#### STORY-366 · قوس ثلاثي (افتتاح، كشف، إغلاق) · Three-beat arc for multi-segment generated spots · 📄 موصوف
- **ماذا / what:** Plan open, reveal and close before writing segment prompts so cuts carry a through-line.
- **كيف / how:** Choose one arc (gaze arc, prop interaction, product entering frame) and make each segment's action advance it; when an action contradicts the reference image, make a state-matched reference first (image edit) because the reference wins.
- **أرقام / params:** 3 segments
- **الدليل / proof:** `kosif-atlas/skills/259-quickdesign/865-quickdesign`

#### STORY-367 · ورقة الأسلوب قبل التوليد · One-page style sheet before any generation · 📄 موصوف
- **ماذا / what:** Fix the look in writing first: one real aesthetic risk, a hex palette with meanings, 2-3 typefaces each with a job, and a list of what never appears.
- **كيف / how:** Write STYLE.md; never-appears list includes real people, logos, brands, copyrighted characters and text inside generated images; keep prompts in a prompts/ folder per video.
- **أرقام / params:** 2-3 typefaces
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video`

#### STORY-368 · اكتب البرومبت مما في الإطار لا من العنوان · Draw the prompt from the frame, not the title · 📄 موصوف
- **ماذا / what:** Generated covers/plates must depict what the video really contains; describe palette, time of day, action and shapes seen.
- **كيف / how:** Inspect real frames first, write prompts from them, and use a real frame as image reference.
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3889-art`

#### STORY-369 · بنية الفيديو القصير · Short-form structure for generated video · 📄 موصوف
- **ماذا / what:** 0-3 s hook that works muted, 3-10 s problem or promise, 10-25 s proof/demo, then close with CTA; ≤30 s holds retention best.
- **كيف / how:** Burn captions (most social video is watched muted), keep text inside platform safe areas, no flashing above 3 Hz, offer a static alternative when motion carries key information.
- **أرقام / params:** hook 0-3 s; ≤30 s; flash ≤3 Hz
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12594-video-gen` · `kosif-atlas/skills/1446-marketing-skills/3531-video`

#### STORY-370 · بطاقة الستوري بورد للمشاهد المولدة · Storyboard card for generated scenes · 📄 موصوف
- **ماذا / what:** A per-scene card that pairs the visual, its base image, camera movement, on-screen text with safe position, caption and motion prompt.
- **كيف / how:** Fill one card per scene; mark scenes 'SPECIFIED, NOT GENERATED' when no key exists so nothing is presented as rendered.
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12594-video-gen`

#### STORY-371 · قاعدة معرفة المخرج · Director knowledge base: shots, composition, lenses, lighting · 📄 موصوف
- **ماذا / what:** Embedded cinematography knowledge used in prompts: 10 shot sizes, 11 composition rules (incl. 9:16 safe zone), 10 lenses, 13 lighting setups, 16 editing rules, 6-step story arc, 12 director principles.
- **كيف / how:** DIRECTOR_KB JSON at the top of 10_studio.js; DIRECTOR_BRIEF() injects it into agent planning. Examples: lighting three_point key:fill 2:1-4:1, rembrandt 3:1 ~3200K, golden_hour sun <15 deg ~3500K, blue_hour 7500-9000K; lenses 14/24/35/50/85/100 macro/135/200 mm, anamorphic 2.39:1, tilt-shift.
- **الدليل / proof:** `app/public/js/10_studio.js:8`

#### STORY-372 · رموز القطاعات المجسّمة · Sector symbol set (object metaphors) · 📄 موصوف
- **ماذا / what:** Twelve object metaphors for business sectors rendered as metal+crystal sculptures: health = crescent on crystal base with a pulse line (crescent, not cross), education = open book turning to crystal + grad cap, manufacturing = three meshed gears, bakery = loaf + wheat, agriculture = ram on crystal, …
- **كيف / how:** Prompt per sector with the shared grammar; deliver 720x480 WebP; currently recoloured ice/teal on disk.
- **أرقام / params:** 10 sectors + audit 1200x800 + cover 900x1206 + gate-tools (copy of manufacturing)
- **الدليل / proof:** `kosif-earth-ci-fork/docs/design/HIGGSFIELD_VISUALS_ar.md` · `kosif-earth-ci-fork/ui/art/brand/sector-health.webp` · `kosif-earth-ci-fork/ui/art/brand/audit.webp`

#### STORY-373 · مقابلة عربية بجولة واحدة · One-round Arabic intake · 📄 موصوف
- **ماذا / what:** Before planning, ask the user a single short Arabic message containing only the still-missing independent questions, each with a suggested default, then wait.
- **كيف / how:** Read AGENTS.md + docs/QUESTIONS.md, diff against what the user already gave (audio, references, timing, style), send one message, never re-ask known facts; unanswered non-blocking items take the agent's stated default.
- **أرقام / params:** 1 message; 7 candidate questions; defaults offered; skip allowed
- **الدليل / proof:** `fastify-motion-bro/AGENTS.md:7` · `fastify-motion-bro/docs/QUESTIONS.md:1-10` · `fastify-motion-bro/skills/fastify-motion-bro/SKILL.md:8`

#### STORY-374 · قالب الأسئلة السبعة · Seven-question brief template · 📄 موصوف
- **ماذا / what:** A fixed Arabic checklist of seven brief questions: message/audience/script, production type, duration+platform, language/dialect, supplied assets, realism/rhythm/likes-dislikes, preview-vs-final.
- **كيف / how:** Copy questions from docs/QUESTIONS.md, drop answered ones, attach defaults (9:16 TikTok/Reels, dialect choice fusha/Egyptian/Saudi/English).
- **أرقام / params:** types: Hand-drawn/Doodle/Kinetic typography/Infographic/2D/3D/Ad/Reference-imitation; aspects 9:16 default, 16:9, custom
- **الدليل / proof:** `fastify-motion-bro/docs/QUESTIONS.md:3-9`

#### STORY-375 · خط الإنتاج الكامل · End-to-end production workflow · 📄 موصوف
- **ماذا / what:** Fixed order: intake -> reference/media analysis -> one round of questions -> brief -> style bible -> timed script/storyboard -> tool verification -> scene build -> browser preview -> revisions -> explicit approval -> local render -> ffprobe + human review -> MP4 + editable assets.
- **كيف / how:** Follow docs/WORKFLOW.md and AGENTS.md steps 1–9; deliver MP4, editable project, brief, storyboard and QA receipt with honest notes.
- **أرقام / params:** 9 numbered agent steps
- **الدليل / proof:** `fastify-motion-bro/docs/WORKFLOW.md:2` · `fastify-motion-bro/AGENTS.md:5-17`

#### STORY-376 · قاعدة لا للشرائح الثابتة · Anti-slideshow motion rule · 📄 موصوف
- **ماذا / what:** Every meaningful shot must carry continuous time-driven motion; still images with fades must not be called motion graphics.
- **كيف / how:** Implement scenes as functions of time t (Canvas/SVG/WebGL/GSAP/Remotion); verify with frame-hash differences across a scene.
- **الدليل / proof:** `fastify-motion-bro/AGENTS.md:13` · `fastify-motion-bro/docs/WORKFLOW.md:14` · `fastify-motion-bro/README.md:83`

#### STORY-377 · قائمة الأساليب الأحد عشر · Named style menu (11 looks) · 📄 موصوف
- **ماذا / what:** Style vocabulary offered to users: cinematic, kinetic, doodle, whiteboard, chalkboard, plotter, stickman, isometric, 3d, infographic, brag.
- **كيف / how:** Stored as brief.style; planner only echoes it into STYLE.md and the Native Canvas renderer draws the same look for all, so each style needs bespoke scene code.
- **أرقام / params:** 11 style ids
- **الدليل / proof:** `fastify-motion-bro/README.md:52-56` · `fastify-motion-bro/scripts/cli.mjs:11`

#### STORY-378 · اختيار نمط الإنتاج · Profile mode chooser · 📄 موصوف
- **ماذا / what:** A bare 'start' with no selected mode must ask which of nine modes to run (stickman, character-romance, fitness, car-exploded, vox-history, food-flow, kinetic-flow, viral-editorial-3d, generic native) and never launch several.
- **كيف / how:** Agent asks, then loads only skills/<mode>/SKILL.md; CLI: npm run profile -- list.
- **أرقام / params:** 9 modes
- **الدليل / proof:** `fastify-motion-bro/AGENTS.md:27-31` · `fastify-motion-bro/docs/PROFILE_CATALOG.md:5-17` · `fastify-motion-bro/docs/PRODUCTION-GATES.md:3`

#### STORY-379 · حدود تقليد المرجع · Reference imitation boundary · 📄 موصوف
- **ماذا / what:** Learn general style, shot language and rhythm from references; never copy scripts, logos, characters, footage or people.
- **كيف / how:** Inspect real frames when accessible; if not, say so and ask for screenshots/notes (kinetic mode S needs 5–8 screenshots).
- **أرقام / params:** 5–8 reference screenshots
- **الدليل / proof:** `fastify-motion-bro/AGENTS.md:8` · `fastify-motion-bro/docs/PROFILE_CATALOG.md:21` · `fastify-motion-bro/skills/kinetic-flow/SKILL.md:12`

#### STORY-380 · رف المكونات الأساسية · Hero primitive shelf (use_when/avoid_when) · 📄 موصوف
- **ماذا / what:** A curated shelf of ~21 hero primitives with use_when, avoid_when and pairs_with guidance distilled from QA, to be checked before building anything bespoke.
- **كيف / how:** Read registry/components/CATALOG.md; match the scene mechanic to a primitive; treat avoid_when lines as hard steers (e.g. scramble-reveal not for calm premium voice; whip-pan-cut not for quiet enterprise; count-up needs chart context).
- **أرقام / params:** groups: Text effects, Product demo, Proof and stats, Call to action, Feature tour, Transitions, Problem setup
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/CATALOG.md`

#### STORY-381 · قاعدة ضد الزخرفة · Anti-decoration taste rule · 📄 موصوف
- **ماذا / what:** No glow on type, glassmorphism, multi-hue gradients, particles or lens flares standing in for ideas unless brand owns them; lint warns.
- **كيف / how:** Apply as defaults while authoring; verify with kmotion measure/speed/sheet
- **أرقام / params:** kmotion lint
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`

#### STORY-382 · قوس القصة القصيرة · Story arc for short pieces · 📄 موصوف
- **ماذا / what:** hook (frame 0 composed and moving) → development → pressure → lift → payoff → deliberate end; 2–3 directions, 4–7 beats, one carried device.
- **كيف / how:** Apply as defaults while authoring; verify with kmotion measure/speed/sheet
- **أرقام / params:** 4–7 beats
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`

#### STORY-383 · فيلم الخمس ثواني · 5-second film recipe · 📄 موصوف
- **ماذا / what:** Default quick deliverable: one idea, ≤3 beats, one carrier, one camera move, ≤8 words.
- **كيف / how:** Apply as defaults while authoring; verify with kmotion measure/speed/sheet
- **أرقام / params:** entrance 0–1.2 s, hold 1.2–3.8 s, payoff 3.8–5 s; 1080x1920 30fps
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/SKILL.md:338`

#### STORY-384 · قصة الست مراحل · Six-beat SHAPE→RANK storyboard · 📄 موصوف
- **ماذا / what:** Educational film beats SHAPE, JOINT, LOAD, BREAK, SWAP, RANK with measured callouts; animation illustrates, not proof.
- **كيف / how:** proplan --task '...' --seconds 18; lab kit
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/STRUCTURAL_TWIN.md`

#### STORY-385 · مونتاج احترافي يدوي · Directed premium edit by hand · 📄 موصوف
- **ماذا / what:** Transcribe+OCR cross-check, decaption, restore Lanczos 1080x1920, plate, composition with push 100→108%, punches, 3 text levels, micro-graphics ≤1.5 s, payoff alone, hold→dip to black; 2 reviewers P0/P1/P2.
- **كيف / how:** python scripts/kmotion.py example scripts/projects/premium_edit/index.html
- **أرقام / params:** push 100→108%
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### STORY-386 · خطّاف الثانيتين · 2-second hook · 📄 موصوف
- **ماذا / what:** Motion within first 3 frames, provocative question or result, bold high-contrast text.
- **أرقام / params:** <=4-5 words; motion in first 3 frames
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/montage_grammar.md` · `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### STORY-387 · الأشكال المحظورة · Banned generic looks · 📄 موصوف
- **ماذا / what:** Avoid centred title on gradient, fade-ins everywhere, blur-in text, crossfades, dark+green/purple glow, generic particles/flares, borders/corner labels, invented logos, synth beeps, long holds.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md` · `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### STORY-388 · اتجاهات بصرية بديلة · Two-three directions with metaphor · 📄 موصوف
- **ماذا / what:** For open briefs sketch 2-3 truly different directions (metaphor, composition, signature behaviour, trade-off) and recommend one.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-director.md`

#### STORY-389 · القواعد البصرية · Visual grammar: thesis/motif/composition/material/movement · 📄 موصوف
- **ماذا / what:** Commit to one thesis sentence, signature motif, composition, material, movement.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-director.md`

#### STORY-390 · قراءة الطلب · Request intake · 📄 موصوف
- **ماذا / what:** Identify deliverable, duration, shape 9:16/16:9/1:1, language, brand, sound, deadline; ask one question max.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/operating-manual.md`

#### STORY-391 · الهدف والدافع والصراع · GMC+S beat · 📄 موصوف
- **ماذا / what:** Goal, Motivation, Conflict, Stakes per beat; linted.
- **كيف / how:** scripts/story_lint.py
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/story-conflict.md`

#### STORY-392 · أنواع الصراع · Central conflict types · 📄 موصوف
- **ماذا / what:** Pick one: vs character/society/nature/technology/supernatural/self.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/story-conflict.md`

#### STORY-393 · أدوات التصعيد · Escalation levers · 📄 موصوف
- **ماذا / what:** Uncertain outcome, withhold need, personal stakes, no-win choice, no safe haven, team shake-up, clock.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/story-conflict.md`

#### STORY-394 · معادلة القصة القصيرة · Short-form story formula · 📄 موصوف
- **ماذا / what:** Conflict hook in 2 s -> one escalation -> choice -> payoff/CTA; product as tool of choice.
- **أرقام / params:** 15-60 s; ~80% action/20% reflection
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/story-conflict.md`

#### STORY-395 · الحبكات السبع · Seven basic plots · 📄 موصوف
- **ماذا / what:** Booker's seven plots incl. Overcoming the Monster stages.
- **كيف / how:** beats tagged with stage for story_lint
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/story-conflict.md`

#### STORY-396 · حقول التفريغ · brief.json per-beat fields · 📄 موصوف
- **ماذا / what:** time, composition, camera, subjects, text, typography, icons_ui, lighting_texture, motion, transition_out, audio + style_line, typography_lock, sound_line, final_frame.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/video-breakdown.md`

#### STORY-397 · ترند: One-liner showreel prompt · Trend: One-liner showreel prompt · 📄 موصوف
- **ماذا / what:** Observed Opus motion wave technique (Sept-Oct 2026): genre-named; brief contagion risk.
- **أرقام / params:** genre-named; brief contagion risk
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### STORY-398 · ترند: Point at a brand URL · Trend: Point at a brand URL · 📄 موصوف
- **ماذا / what:** Observed Opus motion wave technique (Sept-Oct 2026): real screenshots/logo/colours/fonts, music.
- **أرقام / params:** real screenshots/logo/colours/fonts, music
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### STORY-399 · ترند: Name a look + reference · Trend: Name a look + reference · 📄 موصوف
- **ماذا / what:** Observed Opus motion wave technique (Sept-Oct 2026): frame every 0.5 s, style_guide.md, shot list; motion.py study.
- **أرقام / params:** frame every 0.5 s, style_guide.md, shot list; motion.py study
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### STORY-400 · ترند: XML spec prompt · Trend: XML spec prompt · 📄 موصوف
- **ماذا / what:** Observed Opus motion wave technique (Sept-Oct 2026): inputs/direction/structure 120 BPM/build/gotchas/start.
- **أرقام / params:** inputs/direction/structure 120 BPM/build/gotchas/start
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### STORY-401 · ترند: Director's brief long form · Trend: Director's brief long form · 📄 موصوف
- **ماذا / what:** Observed Opus motion wave technique (Sept-Oct 2026): 9.5k-19k chars, payoff every 3-5 s, gates plan->stills->animatic->pass->polish->audio->render.
- **أرقام / params:** 9.5k-19k chars, payoff every 3-5 s, gates plan->stills->animatic->pass->polish->audio->render
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### STORY-402 · إحصاءات الترند · Trend view stats · 📄 موصوف
- **ماذا / what:** 3,984 posts, 203M views; 3D 487 posts 52.0M; seek(t) 70/34.9M; UI 217/16.3M; Arabic 11/0.13M.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### STORY-403 · قواعد Claude عند كتابة التركيبات · Studio-brain composition rules for Claude · 📄 موصوف
- **ماذا / what:** The system prompt the studio gives Claude: compositions are deterministic motion-kit HTML (timeline registered as window.__timelines['root']; no Math.random, Date or setTimeout), never invent media, durations in seconds, correct Arabic, at most 8 words on screen, motion with an arc (entry → developm…
- **كيف / how:** claude_bridge.SYSTEM prepended to every package.
- **أرقام / params:** ≤ 8 on-screen words; arc entry→development→climax
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/claude_bridge.py:129`

#### STORY-404 · قاعدة الخطّاف في أول ثانيتين · 2-second hook rule · 📄 موصوف
- **ماذا / what:** Short-form openers must move in the first frames and pose a question or result immediately.
- **كيف / how:** Frames 1-3 contain motion (zoom-in, hand move, falling object, light shift); open with a question or shocking result; bold high-contrast text.
- **أرقام / params:** motion within first 3 frames; on-screen hook text <= 4-5 words; hook <= 2 s
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/montage_grammar.md` · `kosif-one/tools/kosif-omni/skills/kosif-video/references/story-conflict.md`

#### STORY-405 · حزمة المخرج السينمائية · Cinema deliverable package · 📄 موصوف
- **ماذا / what:** Standard output of a cinematic brief: everything a production needs in one package.
- **كيف / how:** Title, logline, platform plan -> reference sheets (CHR/LOC + lock text) -> shot list (# size angle lens motion duration purpose) -> per-shot positive/negative/params/audio direction -> lighting plan (setup, ratio, Kelvin) + grade -> continuity checklist -> risks -> next 2-3 steps. English prompts, Arabic explanations. Slash command /kosif-omni:cinema.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/SKILL.md` · `kosif-one/tools/kosif-omni/commands/cinema.md`

#### STORY-406 · عدة تصميم الكائنات وعوالم القصص · Creature and world-bible design kit · 📄 موصوف
- **ماذا / what:** Templates for original creature systems and world bibles (no trademarked characters).
- **كيف / how:** 19 element types; rarity weights; 8 biomes; creature card (name, type, rarity, biome, silhouette + 3 features, palette, signature move + VFX, evolution trigger, weakness, lore hook, 7-layer prompt + CHR code); world bible (premise, map zones, factions, magic/tech limits, economy, conflicts, 5 LOC + 5 CHR).
- **أرقام / params:** rarity Common 60 / Uncommon 25 / Rare 10 / Epic 4 / Legendary 0.9 / Mythical 0.1 %; biomes Forest, Cave, Ocean, Mountain, Urban, Desert, Tundra, Wetland
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/creative-worlds.md`

#### STORY-407 · خط إنتاج المخرج للفيديو · Video director pipeline · 📄 موصوف
- **ماذا / what:** End-to-end plan from story to export for reels, ads and AI video.
- **كيف / how:** Story (GMC+S + story_lint) -> frame (platform, duration, goal, hook 1-2 s, CTA) -> locks -> beat sheet hook/setup/escalation/payoff/CTA with timecodes -> shot list table (# time type lens move action lighting audio text transition) -> per-shot English prompts -> keyframe first -> edit plan (cuts on 60/BPM, VO, SFX, subs, grade) -> QA (identity drift, hands, physics, text, continuity) -> regenerate only failed shots.
- **أرقام / params:** per-shot clips 5-10 s
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-video/SKILL.md`

#### STORY-408 · قواعد محرك الصراع · Conflict engine rules · 📄 موصوف
- **ماذا / what:** Rules for building tension in scripts and ads.
- **كيف / how:** One central conflict (vs character/society/nature/technology/supernatural/self); four levels (central, story, scene, inner); escalation levers (fake wins, withheld needs, personal stakes, no-win choice, no safe haven, team shake-up, tighter clock); every conflict ends in a protagonist choice; ~80% action / 20% reflection; conflict anatomy for generation.
- **أرقام / params:** 80/20 action/introspection
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-video/references/story-conflict.md`

#### STORY-409 · بنية قصة الريلز القصيرة · Short-form reel story structure · 📄 موصوف
- **ماذا / what:** 15-60 s narrative shape that sells without a deus ex machina.
- **كيف / how:** Conflict in the first 2 s -> one escalation -> protagonist choice -> payoff/CTA; the product is the tool of the hero's choice. /reel = 15-30 s vertical ad with 3 hook variants; /ad = 30 s spot with VO script.
- **أرقام / params:** 15-60 s; hook <= 2 s; 3 hook variants
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-video/references/story-conflict.md` · `kosif-one/tools/kosif-omni/skills/kosif-video/SKILL.md`

#### STORY-410 · بنية الخطاف الفيروسي وتفكيكه · Viral hook architecture & deconstruction · 📄 موصوف
- **ماذا / what:** Recipe for hooks and a template for reverse-engineering a viral video.
- **كيف / how:** Hook: pattern interrupt <= 0.5 s, curiosity gap, one emotion, micro-story, organic CTA. Deconstruct: hook, pacing map, visual psychology, audio, emotional arc, reproduction blueprint.
- **أرقام / params:** pattern interrupt <= 0.5 s
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/references/books-drive-ledger.md`

#### STORY-411 · مجلس الجماليات البصرية · Visual aesthetics council (12 lenses) · 📄 موصوف
- **ماذا / what:** Twelve named art-direction lenses used to challenge a scene before generation.
- **كيف / how:** Run each lens over the scene spec: VA01 Spatial Worldbuilder, VA02 Character Designer, VA03 Action Choreographer, VA04 Cinematographer, VA05 Lighting Artist, VA06 Colorist, VA07 VFX Designer, VA08 Atmosphere & Weather, VA09 Materials & Texture, VA10 Production Designer, VA11 Composition Director, VA12 Beauty Critic (Full Pro quota: 100 ideas + 100 questions each — not executable locally).
- **أرقام / params:** 12 lenses
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-visual-aesthetics-council/SKILL.md`

#### STORY-412 · وكلاء السرب الإبداعيون · Creative swarm agents (Claude Code sub-agents) · 📄 موصوف
- **ماذا / what:** Ready sub-agent personas with tool allowlists: Cinema Director (E37), Video Producer (E27, frame-by-frame QA, HTML/Three.js -> Playwright -> ffmpeg), Lighting Designer, Audio Engineer (E39), Voice Director, Visual Critic, Image Prompt Engineer, Storyteller (E38).
- **كيف / how:** Launch via Agent tool as kosif-omni:<agent>; each delegates to inner-team roles (prompt engineer, camera-move expert, duration/rhythm expert, frame-consistency, edit director, Arabic captions engineer).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/agents/kosif-video-producer.md` · `kosif-one/tools/kosif-omni/agents/kosif-cinema-director.md` · `kosif-one/tools/kosif-omni/agents/kosif-storyteller.md`

#### STORY-413 · قوس مشاعر الغربة · Exile emotional arc shot list · 📄 موصوف
- **ماذا / what:** A seven-beat emotional order for songs about distance: departure (plane window) -> goodbye (airport) -> foreign streets (night drive) -> memory (rain on glass) -> loneliness (walking in rain) -> family voices -> hope (sunrise from plane), each with a 1-2 word Arabic hero and a short line.
- **كيف / how:** Use as SHOTS list (file, seconds, hero, line) driving per-shot ASS titles.
- **أرقام / params:** 6.8/5.2/7.0/5.0/7.6/6.8/9.6 s
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:19-27`

#### STORY-414 · ملفا التصميم والستوري بورد · DESIGN.md + STORYBOARD.md pre-production pair · 📄 موصوف
- **ماذا / what:** Before any code: a design sheet (style prompt, colour roles with hex, typography, motion rules, what not to do) and a beat-sheet storyboard table (time, beat, on-screen text, motion, optional voice-over line).
- **كيف / how:** Copy the two-file structure; keep one main motion per beat; suggested VO lines sized to ~9 s of calm delivery for any Arabic TTS.
- **أرقام / params:** rules: text >= 40 px at 1080p, one line per label, contrast >= 4.5:1, easeInOutCubic, 0.25 s cross-fades, no flashing
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/DESIGN.md` · `kosif-one/projects/water-cycle-animation/STORYBOARD.md`

#### STORY-415 · وصفة اللوحة السينمائية · Cinematic painted scene recipe · 📄 موصوف
- **ماذا / what:** Value before colour (range > 150/255), three lights (cool key, warm key, dim ambient) with rim from each, aerial depth, then grade/vignette/grain; measure with judge.py.
- **كيف / how:** Follow references/drawing-guide.md section 3; examples dragon_girl, duck_dragon, whale_dragon.
- **أرقام / params:** 12 glow + 12 rim ops in dragon_girl
- **الدليل / proof:** `kosif-one/tools/kosif-studio/references/drawing-guide.md` · `kosif-one/tools/kosif-studio/scenes/dragon_girl.py` · `kosif-one/tools/kosif-studio/scenes/whale_dragon.py`

#### STORY-416 · قواعد تصميم الحركة · Choreography rules (1/3 rules, four acts) · 📄 موصوف
- **ماذا / what:** Lead with the hero; one origin per group; counter-motion; depth through speed; no move over a third of the frame without a key; at most a third of elements move at once; anticipation-action-reaction-resolution.
- **كيف / how:** Apply in motion scores.
- **أرقام / params:** counter-motion 20-30%; depth 1x/0.5x/0.2x; acts 10-20% / 30-50% / 10-20% / 20-30%; something new every 2-4 s
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/references/motion-craft.md`

#### STORY-417 · منهج مخرج الحركة · Motion director method (thesis, motif, motion score) · 📄 موصوف
- **ماذا / what:** Size the assignment, propose 2-3 directions, commit to a thesis and signature motif, write a per-beat motion score (start/end state, duration, ease, trigger, fallback, interruption), choose the smallest capable engine, review in design/motion/engineering lenses.
- **كيف / how:** Follow references/motion-director.md before building.
- **أرقام / params:** examples: Arabic finance 'ledger finding its structure'; product 'aperture discovers the object' (700 ms mask)
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/references/motion-director.md`

#### STORY-418 · خمسة أنماط برومبت ناجحة · Five proven prompt patterns for motion · 📄 موصوف
- **ماذا / what:** From the Opus 5.5 X wave: one-liner showreel, point at a brand URL, name a look + reference, XML spec (inputs/direction/structure/build/gotchas/start), long director's brief with gates.
- **كيف / how:** Offer the matching pattern when a user starts a motion project.
- **أرقام / params:** corpus 3,984 posts; 120 BPM state list; brief 9.5k-19k chars
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/references/x-trend-2026.md`

#### STORY-419 · دليل كتابة البوست العربي · Arabic post copy guide · 📄 موصوف
- **ماذا / what:** Per-platform copy rules: hook in line one matching the video's first 2 s, one CTA, hashtag mix, dialect consistency, honesty.
- **كيف / how:** Read references/copy-guide.md.
- **أرقام / params:** Instagram tag mix 1 general + 2 niche + 1 place + 1 brand; X <= 200 comfortable; LinkedIn first ~210 chars
- **الدليل / proof:** `kosif-one/tools/kosif-social/references/copy-guide.md`

#### STORY-420 · قائمة القدرة الكاملة · Full-power checklist for video requests · 📄 موصوف
- **ماذا / what:** Walk material, understanding, picture, sound, finish and ideas before building: 2-3 directions, hook in first 2 s, one carried device, payoff, deliberate end, poster, credits, post pack.
- **كيف / how:** kosif-one SKILL.md section 2c and the 'full power' sentence in references/catalog.md.
- **أرقام / params:** deliver >= 1080p
- **الدليل / proof:** `kosif-one/tools/kosif-one/SKILL.md` · `kosif-one/tools/kosif-one/references/catalog.md`

#### STORY-421 · بنية القصة بالإيقاعات · Story beat structure · 📄 موصوف
- **ماذا / what:** Central conflict (want/why/obstacle/stakes), hero want+need+flaw, timed beats: opening, inciting, escalation, point of no return, climax, resolution; conflict in first 10%; hero decides climax.
- **كيف / how:** Playbook outputs story.md, beats.md, characters.md
- **أرقام / params:** first 10%
- **الدليل / proof:** `100-superskills/skills/storytelling-scripts/SKILL.md`

#### STORY-422 · بنية الاحتفاظ ليوتيوب · YouTube retention structure · 📄 موصوف
- **ماذا / what:** Promise in 15 s, re-hook every 2 min, no long intro; titles <60 chars curiosity+clarity; 2 thumbnail variants; 20 ideas in search/follow/trend formats; review metrics every 2 weeks.
- **كيف / how:** Playbook
- **أرقام / params:** 15 s, 2 min, 60 chars
- **الدليل / proof:** `100-superskills/skills/youtube-channel-strategy/SKILL.md`

#### STORY-423 · صيغ الكتابة الإعلانية · Arabic copy formulas · 📄 موصوف
- **ماذا / what:** PAS for problems, AIDA for journeys, 4U for headlines; 10 headlines -> pick 3; one CTA; dialects Egyptian/Gulf/Levantine/Maghrebi; Arabic punctuation, no space before comma.
- **كيف / how:** Playbook
- **الدليل / proof:** `100-superskills/skills/arabic-copywriting/SKILL.md`

#### STORY-424 · قائمة القوة الكاملة · Full-power checklist · 📄 موصوف
- **ماذا / what:** Every video checked for material (Pinterest, links), understanding (transcribe, beats, sections), picture (beat cut, per-section grades, kinetic Arabic, 3D, Voice2Motion, face-aware 9:16, privacy), sound (audiolab split, SFX on cuts, -14 LUFS), finish (poster, credits, platform files, post pack), id…
- **كيف / how:** Follow SKILL 2c; kmotion commands referenced live in kosif-montage-motion (not in scope)
- **أرقام / params:** hook <=2 s
- **الدليل / proof:** `100-superskills/skills/kosif-one/SKILL.md` · `100-superskills/skills/kosif-one/references/catalog.md`

#### STORY-425 · وصفة الواقعية المرسومة · Painted-realism recipe · 📄 موصوف
- **ماذا / what:** Value before colour (range >150/255); three lights (cool key, warm key, dim ambient) with rim from each; relief on every big body; flames as add layers red->white + glow; aerial depth via screen fill blur 30 at 0.2; far edges blur 1-3; one strong diagonal; saturation only in fire and eyes; camera or…
- **كيف / how:** Scene ops in order
- **أرقام / params:** value range >150
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md`

#### STORY-426 · بناء/تنفس/حسم · Build/Breathe/Resolve scene structure · 📄 موصوف
- **ماذا / what:** Each scene: elements enter by importance in first 30%, one ambient motion in middle 40%, decisive exit last 30%.
- **كيف / how:** Total stagger <500 ms regardless of count; exit faster.
- **أرقام / params:** 30/40/30 %; stagger <500 ms
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/SKILL.md` · `100-superskills/skills/claude-animation-studio/references/motion-rules.md`

#### STORY-427 · اختبار الجسم · Object test per beat · 📄 موصوف
- **ماذا / what:** Three lines per beat: on-screen phrase, a weighted body doing a named verb, the surface; a word is not a body.
- **الدليل / proof:** `100-superskills/skills/motion-director-pro/references/motion-floor.md`

#### STORY-428 · قالب موجز الفيلم · Film brief folder template · 📄 موصوف
- **ماذا / what:** Deliver a folder: PROMPT.md, START-HERE.md, ATTACH/, frames/, KIT.md with one-law rule (every on-screen body is a kit file), reference roles, exclusion ceiling.
- **الدليل / proof:** `100-superskills/skills/motion-director-pro/references/film-brief-template.md`

#### STORY-429 · منهج تعلّم متكيّف لأي موضوع · Curriculum & Course Builder · 📄 موصوف
- **ماذا / what:** Owner-built skill "Curriculum & Course Builder" (own words): workflow guidance for curriculum & course builder; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill curriculum-course-builder (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/curriculum-course-builder/SKILL.md`

#### STORY-430 · قرار بآراء مستقلة · Genius Council Decisions · 📄 موصوف
- **ماذا / what:** Owner-built skill "Genius Council Decisions" (own words): workflow guidance for genius council decisions; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill genius-council-decision (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/genius-council-decision/SKILL.md`

#### STORY-431 · توليد أفكار بكمية ثم جودة · 100-Ideas Generator · 📄 موصوف
- **ماذا / what:** 100 ideas across 10 deliberate directions (reverse, combine, constrain, exaggerate, swap audience...) then filtered -> concept generation for video hooks.
- **كيف / how:** Load skill ideation-100-ideas (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/ideation-100-ideas/SKILL.md`

#### STORY-432 · صورة سوق قابلة للقرار · Market & Competitor Research · 📄 موصوف
- **ماذا / what:** Owner-built skill "Market & Competitor Research" (own words): workflow guidance for market & competitor research; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill market-competitor-research (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/market-competitor-research/SKILL.md`

#### STORY-433 · عرض من 10 إلى 12 شريحة بترتيب مثبت · Investor Pitch Deck · 📄 موصوف
- **ماذا / what:** 10-12 slide fixed order (problem, solution, market, product, traction, model, competition, team, numbers, ask) -> sequence for a 60-90 s pitch video.
- **كيف / how:** Load skill pitch-deck-investor (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/pitch-deck-investor/SKILL.md`

#### STORY-434 · عروض تقديمية احترافية · PowerPoint Decks · 📄 موصوف
- **ماذا / what:** Story structure problem->vision->how->proof->ask, one idea per slide, grid + brand colours -> reusable as scene/beat structure of an explainer video.
- **كيف / how:** Load skill powerpoint-decks (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/powerpoint-decks/SKILL.md`

#### STORY-435 · هجوم منظّم على أي خطة أو تصميم أو نص قبل · Red Team & Pre-mortem · 📄 موصوف
- **ماذا / what:** Owner-built skill "Red Team & Pre-mortem" (own words): workflow guidance for red team & pre-mortem; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill red-team-premortem (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/red-team-premortem/SKILL.md`

#### STORY-436 · بحث متعدد المصادر على أي موضوع · Deep Research with Citations · 📄 موصوف
- **ماذا / what:** Owner-built skill "Deep Research with Citations" (own words): workflow guidance for deep research with citations; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill research-deep-citations (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/research-deep-citations/SKILL.md`

#### STORY-437 · طبقة الهوية · 7-layer scene: Identity · 📄 موصوف
- **ماذا / what:** Layer 1 of the cinema-director scene spec written before any prompt.
- **كيف / how:** fill scene-spec.json per layer, convert via image/video forges
- **الدليل / proof:** `100-superskills/skills/cinema-director-7layers/SKILL.md:12`

#### STORY-438 · طبقة العالم · 7-layer scene: World · 📄 موصوف
- **ماذا / what:** Layer 2 of the cinema-director scene spec written before any prompt.
- **كيف / how:** fill scene-spec.json per layer, convert via image/video forges
- **الدليل / proof:** `100-superskills/skills/cinema-director-7layers/SKILL.md:12`

#### STORY-439 · طبقة الفعل والفيزياء · 7-layer scene: Action & physics · 📄 موصوف
- **ماذا / what:** Layer 3 of the cinema-director scene spec written before any prompt.
- **كيف / how:** fill scene-spec.json per layer, convert via image/video forges
- **الدليل / proof:** `100-superskills/skills/cinema-director-7layers/SKILL.md:12`

#### STORY-440 · طبقة الكاميرا والعدسة · 7-layer scene: Camera & lens · 📄 موصوف
- **ماذا / what:** Layer 4 of the cinema-director scene spec written before any prompt.
- **كيف / how:** fill scene-spec.json per layer, convert via image/video forges
- **الدليل / proof:** `100-superskills/skills/cinema-director-7layers/SKILL.md:12`

#### STORY-441 · طبقة الإضاءة · 7-layer scene: Lighting · 📄 موصوف
- **ماذا / what:** Layer 5 of the cinema-director scene spec written before any prompt.
- **كيف / how:** fill scene-spec.json per layer, convert via image/video forges
- **الدليل / proof:** `100-superskills/skills/cinema-director-7layers/SKILL.md:12`

#### STORY-442 · طبقة المواد والجو · 7-layer scene: Materials & atmosphere · 📄 موصوف
- **ماذا / what:** Layer 6 of the cinema-director scene spec written before any prompt.
- **كيف / how:** fill scene-spec.json per layer, convert via image/video forges
- **الدليل / proof:** `100-superskills/skills/cinema-director-7layers/SKILL.md:12`

#### STORY-443 · طبقة اللون والقصة · 7-layer scene: Colour & story · 📄 موصوف
- **ماذا / what:** Layer 7 of the cinema-director scene spec written before any prompt.
- **كيف / how:** fill scene-spec.json per layer, convert via image/video forges
- **الدليل / proof:** `100-superskills/skills/cinema-director-7layers/SKILL.md:12`

#### STORY-444 · قواعد الاستمرارية · Continuity rules · 📄 موصوف
- **ماذا / what:** Fixed light direction per scene, fixed wardrobe/props, lens must match stated distance.
- **كيف / how:** manual review
- **الدليل / proof:** `100-superskills/skills/cinema-director-7layers/SKILL.md:29`

#### STORY-445 · تقسيم 5 إيقاعات · 5-beat storyboard timing · 📄 موصوف
- **ماذا / what:** Five beats with cumulative times summing to total; 1-2 shots per beat.
- **كيف / how:** storyboard.md table
- **أرقام / params:** reels: no more than one shot per 2.5 s; hook within 1.5 s; one CTA
- **الدليل / proof:** `100-superskills/skills/storyboard-shotlist/SKILL.md:21`

#### STORY-446 · أعمدة قائمة اللقطات · Shot-list table columns · 📄 موصوف
- **ماذا / what:** # · time · shot type · lens · move · action · lighting · sound · text · transition.
- **كيف / how:** markdown table
- **أرقام / params:** 10 columns
- **الدليل / proof:** `100-superskills/skills/storyboard-shotlist/SKILL.md:23`

#### STORY-447 · بنية كتاب الأطفال · Picture-book story structure · 📄 موصوف
- **ماذا / what:** Problem, three attempts, resolution, implicit lesson; cliffhanger at end of each right page.
- **كيف / how:** script.md
- **أرقام / params:** 12-32 pages; max 25 words per page for kids
- **الدليل / proof:** `100-superskills/skills/comics-picture-books/SKILL.md:21`

#### STORY-448 · بنية إعلان 30 ثانية · 30s ad structure · 📄 موصوف
- **ماذا / what:** 0-3 hook, 3-10 problem, 10-22 solution+proof, 22-30 CTA; one provable promise.
- **كيف / how:** ad-script.md
- **أرقام / params:** VO max 70 words
- **الدليل / proof:** `100-superskills/skills/ad-creative-30s/SKILL.md:23`

#### STORY-449 · 3 أنواع خطافات · Three hook types · 📄 موصوف
- **ماذا / what:** Question, visual shock, result — for first 2 s.
- **كيف / how:** hooks.md
- **أرقام / params:** 2 s
- **الدليل / proof:** `100-superskills/skills/ad-creative-30s/SKILL.md:22`

#### STORY-450 · صيغة أفكار الريلز · Reels idea formula hook+promise+conversion · 📄 موصوف
- **ماذا / what:** 3 content pillars, 10 ideas, script: 1 s hook, 3 value points, soft CTA.
- **كيف / how:** ideas.md/script.md
- **أرقام / params:** max 150 words per 45 s; motion+text in first second
- **الدليل / proof:** `100-superskills/skills/reels-shorts-factory/SKILL.md:21`

#### STORY-451 · قواعد التصميم الحركي · Choreography rules · 📄 موصوف
- **ماذا / what:** Hero leads, counter-motion, depth by speed, the 1/3 rules, four acts.
- **كيف / how:** Apply when writing the motion score.
- **أرقام / params:** counter-motion 20-30%; depth speeds 1× / .5× / .2×; no move over 1/3 of frame without an intermediate key; with 3+ elements ≤ 1/3 move at once; something new every 2-4 s; acts anticipation 10-20% / action 30-50% / reaction 10-20% / resolution 20-30% with 100-200 ms breathing
- **الدليل / proof:** `kosif-studio/motion/references/motion-craft.md`

#### STORY-452 · القواعد البصرية أولاً · Visual grammar first (thesis, motif) · 📄 موصوف
- **ماذا / what:** Propose 2-3 genuinely different directions, each with a subject metaphor, composition, signature behaviour and trade-off; commit to thesis, signature motif, composition, material, movement.
- **كيف / how:** Answer in the user's language; strong still frame first, then animate to reveal relationships.
- **الدليل / proof:** `kosif-studio/motion/references/motion-director.md`

#### STORY-453 · دفتر يجد بنيته · Ledger-finding-structure motif (finance) · 📄 موصوف
- **ماذا / what:** Arabic finance motion: warm paper, charcoal Arabic type, restrained blue rules; a selected account's rule grows inline-start, detail panel follows.
- **كيف / how:** CSS/GSAP; retarget on interruption; reduced motion = immediate update.
- **أرقام / params:** rule grows 280 ms decelerating; panel +80 ms delay, 12 px translate settling 360 ms
- **الدليل / proof:** `kosif-studio/motion/references/motion-director.md`

#### STORY-454 · خمسة أنماط برومبت · Five prompt patterns that worked (X wave) · 📄 موصوف
- **ماذا / what:** One-liner showreel; point at a brand URL with real assets and music; name a look + reference (frame every .5 s -> style_guide.md); XML spec (<inputs> <direction> <structure> on 120 BPM <build> <gotchas> <start>); long director's brief (9.5k-19k chars) with gates.
- **كيف / how:** Offer as intake templates; study references with motion.py study REF.mp4.
- **أرقام / params:** showreel ~15 s; payoff every 3-5 s in long briefs
- **الدليل / proof:** `kosif-studio/motion/references/x-trend-2026.md`

#### STORY-455 · ميزانيات الجهد · Effort budgets from the X wave · 📄 موصوف
- **ماذا / what:** Expectation setting for one-shot and celebrated pieces.
- **كيف / how:** Tell the user realistic time/cost.
- **أرقام / params:** median 20 min (p90 57) for a short clip from one prompt; median 4 h for celebrated pieces; median $10 tokens (p90 $200); 7 h / 163 calls for a 45 s watercolour short; 12 h for a 142 s music video
- **الدليل / proof:** `kosif-studio/motion/references/x-trend-2026.md`

#### STORY-456 · موجّه الطلبات إلى المسار المناسب · Request router: which code for which ask · 📄 موصوف
- **ماذا / what:** Maps the user's ask to a pipeline: 'draw this image as is / give me its code' -> to_python; cinematic painting from a prompt -> KOSIF scene + judge; realistic 3D/reflections -> Three.js page; film of the drawing or animation -> film.py; flat logo to enlarge -> SVG/vectorize; ready AI code -> runner.
- **كيف / how:** Read references/drawing-guide.md sections 0-1 before choosing.
- **الدليل / proof:** `kosif-studio/references/drawing-guide.md:6` · `kosif-studio/references/drawing-guide.md:17`

#### STORY-457 · كتابة البرومبت كأقفال جودة · Quality-locks prompt writing · 📄 موصوف
- **ماذا / what:** Write the brief as a list of must-show elements, light sources and prohibitions (e.g. 'no cartoon look, no text'), then build the scene step by step from back to front.
- **كيف / how:** See the PROMPT block at the top of whale_dragon.py and guide section 4.
- **الدليل / proof:** `kosif-studio/references/drawing-guide.md:82` · `kosif-studio/scenes/whale_dragon.py:1`

#### STORY-458 · قواعد الصدق في الادعاءات · Honesty rules for drawing claims · 📄 موصوف
- **ماذا / what:** 'Realistic' here means a realistically lit digital painting, not a photograph; code from a description never matches a photo; exact match only comes from image code or exact mode; never claim what you did not see in 1:1 crops.
- **كيف / how:** State these limits to the user up front.
- **الدليل / proof:** `kosif-studio/references/drawing-guide.md:93` · `kosif-studio/README.md`

#### STORY-459 · بنية الإعلان القصير · Ad beat structure · 📄 موصوف
- **ماذا / what:** Commercial film skeleton: hook, promise, feature beats, proof, CTA, logo.
- **كيف / how:** Remotion <Sequence> per beat or scenes[] with t0/t1 in html-canvas.
- **أرقام / params:** hook 0–1.5 s; problem/promise 1.5–4 s; 2–4 features × 2–3 s; proof; CTA 2–3 s; logo 1–1.5 s
- **الدليل / proof:** `kosif-tool/playbooks/ads.md:15-19`

#### STORY-460 · قاعدة جذب الإطار الأول · First-frame hook rule · 📄 موصوف
- **ماذا / what:** Something moves on frame 1; major change before 1.5 s; never open on the logo.
- **أرقام / params:** change ≤ 1.5 s
- **الدليل / proof:** `kosif-tool/playbooks/ads.md:25` · `kosif-tool/playbooks/ads.md:102`

#### STORY-461 · وصفة إعلان منتج متجر · Store product ad recipe · 📄 موصوف
- **ماذا / what:** Product drops on coloured plinth, turns 30°, three benefit tags pop, price lands, CTA.
- **أرقام / params:** turn 30°; 3 tags
- **الدليل / proof:** `kosif-tool/playbooks/ads.md:48`

#### STORY-462 · استبيان الفحص التسعة · 9-question inspection rubric · 📄 موصوف
- **ماذا / what:** Nine fixed questions (what is app, funniest claim, visual hook, UI to show, shortest video, tone, audio feel, user flow...) answered before planning.
- **كيف / how:** Read files in priority order, write answers before Step 2.
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/step-1-inspect.md`

#### STORY-463 · إيقاع الدخول-الفعل-النتيجة · Entry-action-result user-flow beats · 📄 موصوف
- **ماذا / what:** Centerpiece scenes show the product in use in 2-3 beats rather than marketing sections.
- **كيف / how:** Scan routes/components/stores for the happy path; storyboard it.
- **أرقام / params:** 2-3 beats
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/step-1-inspect.md` · `kosif-one/vendor/brag/skills/brag/references/step-2-plan.md`

#### STORY-464 · قالب خطة الفيديو · Brag plan template · 📄 موصوف
- **ماذا / what:** One-page plan: app, angle, hook 2-3 s, key moments, outro, tone, format, visual identity, share copy, audio direction, per-scene storyboard with audio intent.
- **كيف / how:** Write <out>/brag-plan.md from template.
- **أرقام / params:** hook first 2-3s
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/step-2-plan.md`

#### STORY-465 · نبرة: default · Tone preset: default · 📄 موصوف
- **ماذا / what:** Brag tone preset changing copy voice, type personality, pacing and transitions.
- **كيف / how:** Pick via --tone or map freeform direction to nearest preset.
- **أرقام / params:** 3-5 s scenes, 4-5 scenes, crossfade or clean slide
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/tones.md`

#### STORY-466 · نبرة: polished · Tone preset: polished · 📄 موصوف
- **ماذا / what:** Brag tone preset changing copy voice, type personality, pacing and transitions.
- **كيف / how:** Pick via --tone or map freeform direction to nearest preset.
- **أرقام / params:** 3-4 scenes of 4-6 s, slow crossfade 0.6-0.8 s, light weight wide tracking
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/tones.md`

#### STORY-467 · نبرة: yc-parody · Tone preset: yc-parody · 📄 موصوف
- **ماذا / what:** Brag tone preset changing copy voice, type personality, pacing and transitions.
- **كيف / how:** Pick via --tone or map freeform direction to nearest preset.
- **أرقام / params:** deadpan serious claims, hard cut or 0.2 s crossfade, mono for data
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/tones.md`

#### STORY-468 · نبرة: chaotic · Tone preset: chaotic · 📄 موصوف
- **ماذا / what:** Brag tone preset changing copy voice, type personality, pacing and transitions.
- **كيف / how:** Pick via --tone or map freeform direction to nearest preset.
- **أرقام / params:** 6-8 scenes, <=4 s each some <2 s, ALL CAPS heavy, hard/flash cut, zoom cut scale 1.2->1.0
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/tones.md`

#### STORY-469 · نبرة: deadpan · Tone preset: deadpan · 📄 موصوف
- **ماذا / what:** Brag tone preset changing copy voice, type personality, pacing and transitions.
- **كيف / how:** Pick via --tone or map freeform direction to nearest preset.
- **أرقام / params:** 3-4 scenes 4-7 s holds, very slow crossfade 0.8-1.0 s
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/tones.md`

#### STORY-470 · نبرة: cinematic · Tone preset: cinematic · 📄 موصوف
- **ماذا / what:** Brag tone preset changing copy voice, type personality, pacing and transitions.
- **كيف / how:** Pick via --tone or map freeform direction to nearest preset.
- **أرقام / params:** 4-5 scenes 3-5 s, dramatic wipe or crossfade with scale 0.95->1.0
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/tones.md`

#### STORY-471 · نبرة: app-store · Tone preset: app-store · 📄 موصوف
- **ماذا / what:** Brag tone preset changing copy voice, type personality, pacing and transitions.
- **كيف / how:** Pick via --tone or map freeform direction to nearest preset.
- **أرقام / params:** 4-6 scenes, clean slide/wipe 0.35-0.45 s
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/tones.md`

#### STORY-472 · عرض واحد جمهور واحد فعل واحد · One offer one audience one action · 📄 موصوف
- **ماذا / what:** Landing page principle; single primary CTA above fold.
- **كيف / how:** Intake A1 then structure A2.
- **الدليل / proof:** `kosif-one/vendor/ai-design-skills/skills/landing-page-design/SKILL.md`

#### STORY-473 · ترتيب مخرجات الصفحة · Landing output order · 📄 موصوف
- **ماذا / what:** Outline, hero copy, benefits 3-5, how-it-works 3 steps, FAQ 6-12, SEO/AEO, layout A-D.
- **الدليل / proof:** `kosif-one/vendor/ai-design-skills/skills/landing-page-design/SKILL.md`

#### STORY-474 · تجميع مقاطع جاهزة · Pre-generated assets into scroll-world · 📄 موصوف
- **ماذا / what:** Prompting scroll-world to skip generation and only encode/wire existing clips; stills must be real video frames.
- **الدليل / proof:** `kosif-one/vendor/mcp-higgsfield-landing/PROMPTS.md:204`

#### STORY-475 · قائمة مشاهد مركز القيادة السينمائي · Cinema command-center scene list · 💡 فكرة
- **ماذا / what:** Named scenes and effects for an audit 'cinema edition': command center (3D financial network, data particles, cinematic transitions), evidence galaxy, AI risk radar 3D, council room, benchmark engine.
- **كيف / how:** Config objects only; use as a shot list for an explainer film about auditing.
- **أرقام / params:** modules 5; panels 4; flow Data -> Risk -> Materiality -> Procedures -> Evidence -> Findings -> Opinion
- **الدليل / proof:** `kosif-audit-studio/cinema/auditCinemaConfig.js` · `kosif-audit-studio/cinema/cinemaCommandCenter.js` · `kosif-audit-studio/docs/CINEMA_AUDIT_EDITION.md`

#### STORY-476 · اتجاه دفتر الحسابات · Ledger direction example · 💡 فكرة
- **ماذا / what:** Arabic finance: rule grows inline-start, panel follows.
- **أرقام / params:** 280 ms rule; +80 ms delay; 12 px translate over 360 ms
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-director.md`

#### STORY-477 · الإصلاح الذي يفسد · Well-meant fix makes worse · 💡 فكرة
- **ماذا / what:** Escalation pattern from Cursed Child case study for series/reels.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/story-conflict.md`

#### STORY-478 · ستايل ريل تسويقي نظيف (مرجع فقط) · Clean marketing reel reference (style, not built) · 💡 فكرة
- **ماذا / what:** Only a target is recorded: a smooth, clean marketing reel (25.6 s) chosen as the look to imitate; no composition was built in this folder.
- **كيف / how:** Pair with the mimic workflow (study -> match -> build) once the reference file is available locally.
- **أرقام / params:** 25.567 s
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_TikTok_Reference/source_probe.txt`

#### STORY-479 · قصة مشكلة ثم حل · Problem→fix→outcome SaaS arc · 💡 فكرة
- **ماذا / what:** 30 s 5-beat explainer: why, pain (tangled UI fragments), fix (snap into real UI), outcomes, logo.
- **كيف / how:** Remotion scenes 6/6/7/6/5 s.
- **الدليل / proof:** `style:pm-aschapmann-131210`

#### STORY-480 · حد أقصى للقطة · Max shot length 2.5 s · 💡 فكرة
- **ماذا / what:** Fast promo: no shot over 2.5 s; one 1.10 push 200 ms in/500 ms out.
- **أرقام / params:** 2.5 s
- **الدليل / proof:** `style:pm-influencer-seo-ce8c33`

#### STORY-481 · حد ثلاث مجموعات · Three moving groups cap · 💡 فكرة
- **ماذا / what:** Max three independently moving groups at any frame.
- **أرقام / params:** 3 groups
- **الدليل / proof:** `style:pm-itisrazak-3ad902`

#### STORY-482 · نهاية بمؤشر · Loop-friendly blinking cursor end · 💡 فكرة
- **ماذا / what:** Outro leaves only a blinking cursor for a seamless loop; secrets never shown.
- **الدليل / proof:** `style:pm-jake11moran-a269c4`

#### STORY-483 · تاريخ الذكاء الاصطناعي · AI history timeline idea · 💡 فكرة
- **ماذا / what:** 45 s timeline 1950→today with winters desaturated.
- **الدليل / proof:** `style:pm-kloss-xyz-fe0c31`

#### STORY-484 · الخروج من اللوحة · Step-out-of-painting outro · 💡 فكرة
- **ماذا / what:** 3D scene flattens back into framed canvas on a wall.
- **الدليل / proof:** `style:pm-mandelduck-95fd08`
