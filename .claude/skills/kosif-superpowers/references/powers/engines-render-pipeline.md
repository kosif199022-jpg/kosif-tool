# المحركات وخط الرندر — Engines & render pipeline

> فصل مُجمَّع آليًا من 443 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **435 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 435 powers deduplicated by name from 443 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 54 · 🟢 جاهز 60 · 📦 بأمر تثبيت 209 · 🔑 مفتاح/خدمة 27 · 👁 شوهد في فيديو 8 · 📄 موصوف 82 · 💡 فكرة 1 · المجموع / total 441

**إضافات v2 — v2 additions:** ENG-X01 … ENG-X05 (5) — في آخر الفصل / at the end of this chapter.

#### ENG-01 · عقد تركيب HyperFrames · HyperFrames composition contract · ✅ مُثبت هنا
- **ماذا / what:** Every film is one index.html whose root div carries data-composition-id, data-width, data-height, data-duration and data-fps, with GSAP timelines registered in window.__timelines and the motion-kit shim so either engine can seek it.
- **كيف / how:** python motion.py new NAME; author a paused gsap.timeline, register window.__timelines['root']=tl, call MOTION.shim('root', seconds); everything must be a function of t.
- **أرقام / params:** root attrs data-composition-id/width/height/duration/fps; default 1920x1080, 8 s, 30 fps
- **الدليل / proof:** `kosif-studio/motion/motion.py:18` · `kosif-studio/motion/motion.py:126` · `kosif-studio/tests/test_studio.py:549` · `kosif-one/tools/kosif-studio/motion/references/hyperframes-authoring.md`

#### ENG-02 · عقد وحدة المشهد الحتمي · Deterministic scene module contract · ✅ مُثبت هنا
- **ماذا / what:** A scene is a JS module that sizes a canvas and exposes DURATION plus renderFrame(t); any renderer can photograph it frame by frame.
- **كيف / how:** window.DURATION; window.renderFrame(t) -> Promise; Playwright loop: for f in 0..N: await page.evaluate(t=>renderFrame(t), f/fps); screenshot canvas; then ffmpeg -framerate fps -i %05d.png -c:v libx264 -pix_fmt yuv420p. Works here with installed playwright + ffmpeg.
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9356-produce/SKILL.md` · `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md` · `kosif-atlas/skills/2460-pixel-art/9526-scene/SKILL.md`

#### ENG-03 · تجميع اللقطات بنوافذ إطارات · Shot assembly by frame windows · ✅ مُثبت هنا
- **ماذا / what:** Assemble an edit purely in ffmpeg: each shot trimmed by frame range, timestamps reset, audio windows trimmed identically, then concatenated and mixed with music.
- **كيف / how:** [k:v]trim=start_frame=S:end_frame=S+N,setpts=PTS-STARTPTS,format=yuv420p ; [k:a]atrim=..,asetpts=PTS-STARTPTS,aresample=48000,volume=XdB ; concat ; amix=inputs=2:duration=first:normalize=0 ; intermediate CRF 8 + PCM 24-bit, final libx264 high CRF 17 -g 60
- **أرقام / params:** SFX ≈ -8 dB under music cue
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/assembly-and-review.md` · `kosif-atlas/skills/1526-gamegen/4173-game-trailer/assets/marketing/render.py` · `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/gotchas.md`

#### ENG-04 · حمايات أداء WebGL · WebGL robustness guards · ✅ مُثبت هنا
- **ماذا / what:** Patterns that keep a decorative 3D layer from hurting the page: never block on shader link, remember slow devices, cap pixel ratio, pause when hidden, free the context.
- **كيف / how:** KHR_parallel_shader_compile COMPLETION_STATUS polling each frame, 12 s give-up; if LINK_STATUS read takes >1.5 s set localStorage sqc_world_slow; dpr cap 1 (phone) / 1.5; IntersectionObserver + visibilitychange pause; WEBGL_lose_context on destroy; returns null without WebGL; page paints first then canvas fades in 1.4-1.6s.
- **أرقام / params:** timeouts 12000ms / 1500ms; dpr 1 / 1.5
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/crystal-world.js:71` · `kosif-earth-ci-fork/ui/art/crystal-world.js:113` · `kosif-earth-ci-fork/tools/crystal_world.test.mjs`

#### ENG-05 · تشغيل الفيلم بشروط وتجاوز عامل الخدمة · Film-only-where-it-should gating + SW bypass · ✅ مُثبت هنا
- **ماذا / what:** Decorative clips play only on wide screens without reduced motion or data saving, poster stays as the still; the service worker never caches video or Range requests.
- **كيف / how:** door/dash <video preload=none data-src> swapped in by script; sw.js passes video and Range requests to network.
- **الدليل / proof:** `kosif-earth-ci-fork/tools/brand_art.test.mjs` · `kosif-earth-ci-fork/docs/design/HIGGSFIELD_VISUALS_ar.md` · `kosif-earth-ci-fork/unlock.html:170`

#### ENG-06 · مُجمّع ستوري بورد التحرير · Editorial storyboard compiler · ✅ مُثبت هنا
- **ماذا / what:** Builds a 30 s 9:16 storyboard with palette, exact_background_lines=2, approval flags, sound policy and 5 scenes each holding its motion prompt; preview-project copies it into project/.
- **كيف / how:** npm run viral -- compile (writes projects/viral-editorial/{storyboard,posters,motion-prompts}.json) or preview-project (also project/storyboard.json).
- **أرقام / params:** 5 x 6 s = 30 s; fps 30
- **الدليل / proof:** `fastify-motion-bro/scripts/viral-editorial.mjs:84-92` · `fastify-motion-bro/scripts/viral-cli.mjs:24-32`

#### ENG-07 · بديل ffprobe · ffprobe shim · ✅ مُثبت هنا
- **ماذا / what:** ffprobe stand-in built on ffmpeg, exact frame counts, durations to 1/100 s.
- **كيف / how:** scripts/ffprobe_shim.py installed to ~/kosif-motion/bin
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### ENG-08 · التايملاين JSON إلى فيلم · JSON timeline → film · ✅ مُثبت هنا
- **ماذا / what:** Declarative edit: clips in/out, speed (pitch-kept) or exact ramps, Ken Burns, grades, fit cover/contain/blur, images, colour cards, 57 xfade transitions + acrossfade, Pillow Arabic overlays/lower thirds with entrances, progress bar, karaoke, ducking, −14 LUFS; picture/sound two passes.
- **كيف / how:** python scripts/kmotion.py timeline edit.json --out film.mp4 --inspect [--dry-run]; timeline --example; transitions
- **أرقام / params:** 57 xfade; demo 1080x1920 7.67 s −14.6 LUFS
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### ENG-09 · فيلم بدون متصفح · workbench no-browser 2D film · ✅ مُثبت هنا
- **ماذا / what:** Task → plan → 2D film with Arabic titles via Pillow+FFmpeg.
- **كيف / how:** python scripts/kmotion.py workbench 'task' --aspect 9:16 --titles 'a|b' --out film.mp4
- **أرقام / params:** 9:16 6 s 180 frames verified
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### ENG-10 · جسر التصيير · Render shim (seek contract) · ✅ مُثبت هنا
- **ماذا / what:** Bridges GSAP timelines to frame-exact renderers: window.render(t)/__ready, window.seek(t), __timelines, CSS animations and <video data-start> clips seek to t.
- **كيف / how:** Register tl in window.__timelines['root'] then MOTION.shim('root', duration). Renderer calls render(t) and waits for __ready (two rAFs after videos sought).
- **أرقام / params:** video seek timeout 4 s; load timeout 15 s; waits for document.fonts.ready
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:466` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:578`

#### ENG-11 · سلسلة المعالجة السينمائية · Cinematic post stack (makePost) · ✅ مُثبت هنا
- **ماذا / what:** Render -> NaN guard -> bloom -> god rays -> bokeh DOF -> grade/CA/vignette -> film grain -> output, all uniforms animatable.
- **كيف / how:** const post=K3.makePost(renderer, scene, camera, W, H, {bloom, bloomThreshold, aperture, maxblur, vignette, ca, grain, clampMax}); post.sunOnScreen(sunDir).
- **أرقام / params:** bloom .22 radius .6 threshold .9; clamp 48; bokeh focus 900 aperture .00004 maxblur .0035; vignette .42; CA 1.2; grain .16
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:361`

#### ENG-12 · حزمة ثلاثية الأبعاد جاهزة · Pre-bundled 3D kit (window.K3) · ✅ مُثبت هنا
- **ماذا / what:** three.js r186 and all 69 three-kit exports as one classic script, so 3D scenes run from file:// with no npm.
- **كيف / how:** <script src='assets/three-kit.bundle.js'> -> window.K3 (also K3.POST classes for custom stacks). Rebuild with python motion.py kit-bundle (needs npm three@0.186.1 + esbuild).
- **أرقام / params:** 904,567 bytes; 69 exports; three REVISION 186 (verified under Node)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.bundle.js` · `100-superskills/skills/kosif-montage-motion/scripts/kit/k3-entry.js` · `100-superskills/skills/kosif-montage-motion/scripts/motion.py:232`

#### ENG-13 · فيلم SVG كدالة نقية بلا مكتبات · Pure-function SVG film (no libraries) · ✅ مُثبت هنا
- **ماذا / what:** A whole cinematic short is a JavaScript function sceneSVG(t) that returns a complete 1280×720 SVG string; no assets, fonts, packages or network.
- **كيف / how:** Write helpers rect/path/line/neon that emit SVG strings; precompute static layers (skyline, architecture, props) once; sceneSVG(t) composes parallax groups, character, rain, vignette and titles; index.html sets root.innerHTML=sceneSVG(t) inside window.render.
- **أرقام / params:** 1280×720, 24 fps, 12 s = 288 frames; deterministic rnd(i)=fract(sin(i·127.1+311.7)·43758.5453)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:124` · `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/index.html:20`

#### ENG-14 · مزامنة العدّة للمشاريع الخفيفة · Kit sync for lightweight example projects · ✅ مُثبت هنا
- **ماذا / what:** Example projects ship without library copies; one command copies motion-kit, GSAP, three-kit, shape-kit, lab-kit and only the kit fonts the page names.
- **كيف / how:** python scripts/kmotion.py sync projects/NAME → motion.sync_assets(d) copies kit files referenced by index.html and the woff2 files matched by assets/fonts/*.woff2.
- **أرقام / params:** fonts copied only if named; lab-kit/three-kit/shape-kit only if referenced
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:228` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:6`

#### ENG-15 · تقسيم الإطارات لتصيير متوازٍ · Shard plan for parallel rendering · ✅ مُثبت هنا
- **ماذا / what:** A project's frame range is split into contiguous shards with no gaps so several machines/pages can render in parallel.
- **كيف / how:** shard.plan(project_dir, n) → {frames, shards:[{i0,i1}]}; test asserts first i0=0, last i1=frames, each i1 == next i0 (run on night_boat with 7 shards).
- **أرقام / params:** 7 shards over night_boat (5 s × 30 fps)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_analyze.py:87`

#### ENG-16 · تطبيق الاستوديو المحلي وخادم MCP · Local studio web app + MCP server · ✅ مُثبت هنا
- **ماذا / what:** A local Starlette site exposes plan/validate/compile, a render job service with job tokens, recipe jobs, media, projects with path containment, timeline summaries and an MCP endpoint with motion and KOSIF tools; cross-origin writes are refused.
- **كيف / how:** kmotion web --port 8766; /api/plan (12 s × 30 fps → 360 frames), /api/validate, /api/compile (kosif.motion.manifest.v1 + project_html with window.render), /api/render/jobs (X-Job-Token), /api/recipes, /mcp tools motion_plan, motion_validate, motion_compile, motion_templates, kosif_run, kosif_job, kosif_project_write, kosif_timeline_check.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_web.py:71` · `100-superskills/skills/kosif-montage-motion/tests/test_web.py:205`

#### ENG-17 · تصدير MP4 من محرر المتصفح · Browser editor offline MP4 export (WebCodecs) · ✅ مُثبت هنا
- **ماذا / what:** The in-browser KOSIF Studio editor exports frame-accurate MP4 with WebCodecs and an MP4 muxer: exact frame plan, audio placement, codec fallback (AVC baseline → none; Opus for audio), keyframes every 2 s, cancel, loudness normalisation; plus a MediaRecorder WebM path with safe cancel.
- **كيف / how:** offline.mjs framePlan(8, 30) → 240 frames, timestampUs(30)=1e6; audioPlan(project); pickVideoCodec(VE, 1280, 720, 30) → 'avc1.42…'; encodeOffline({width, height, fps, frames, renderFrame, VideoEncoder, VideoFrame, Mp4Muxer}); model.mjs caps projects at 60 s, sanitises colours/enums/URLs.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/studio/offline.test.mjs:6` · `100-superskills/skills/kosif-montage-motion/tests/studio/model.test.mjs:5` · `100-superskills/skills/kosif-montage-motion/tests/studio/export.mock.test.mjs:1`

#### ENG-18 · استوديو KOSIF Motion Web المحلي · KOSIF Motion Web local studio server · ✅ مُثبت هنا
- **ماذا / what:** A loopback-only Starlette/uvicorn website that acts as the 'hands' of the montage engine: Arabic RTL tabs for media, recipes, projects, timeline, jobs, review, Workbench, Claude and environment; every file stays on the PC.
- **كيف / how:** python scripts/kmotion.py web --port 8766 (or python scripts/web/server.py --host 127.0.0.1 --port 8766 --workers 2 --open). Routes defined in create_app(); static UI at /, Studio at /studio/, examples at /examples/, project previews at /projects/NAME/index.html.
- **أرقام / params:** default host 127.0.0.1, port 8766, recipe workers 2, JSON body cap 4 MB, upload cap 4 GB per file, server VERSION 6.2 (health reports contract 5.3)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:1` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:49` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:963`

#### ENG-19 · كتالوج الوصفات كنماذج · Recipe catalogue as typed forms · ✅ مُثبت هنا
- **ماذا / what:** 32 kmotion commands grouped in 5 groups (auto montage, v6 timeline/scenes/privacy/templates, films from code, quick tools, QA) are described with typed fields so the browser builds forms, MCP validates arguments and the server builds a safe argv.
- **كيف / how:** recipes.GROUPS → catalogue(); build_args() puts options first, then '--', then positionals; unknown fields raise; field kinds file/files/save/dir/text/number/choice/bool/set; 'set' is shlex-split; values with NUL or newline refused. POST /api/jobs {recipe,args,note}.
- **أرقام / params:** groups: auto(reel,direct,verse,audio2motion,montage) · v6(timeline,studio-import,scenes,privacy,template) · films(new,frames,preview,render,lint) · tools(silence,aspect,grade,captions,transcribe,decaption,stabilize,trim,export,platforms,thumb,score) · qa(inspect,sheet,probe,doctor,transitions)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:19` · `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:107` · `100-superskills/skills/kosif-montage-motion/tests/test_web.py:115`

#### ENG-20 · مشغل المهام مع سجل حي · Background job runner with live SSE log · ✅ مُثبت هنا
- **ماذا / what:** Every recipe runs as its own `python kmotion.py CMD …` process in a queue with N workers; the log streams to the browser over Server-Sent Events, persists to disk and the produced files are auto-detected from the log.
- **كيف / how:** jobs.Runner(root, cwd, workers) → submit(); Job.run() streams stdout; GET /api/jobs/ID/log (SSE, 'event: end' carries the final job), /log.txt, POST /cancel; _collect_outputs() regex-matches printed paths (mp4/mov/webm/gif/webp/png/jpg/wav/mp3/json/srt/ass/html/md/txt) and keeps ≤ 20 existing files; history of 60 jobs reloaded from meta.json.
- **أرقام / params:** SSE poll 0.3 s; default workers 2; outputs ≤ 20; history 60; job id = YYYYmmdd-HHMMSS-hex6
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/jobs.py:1` · `100-superskills/skills/kosif-montage-motion/scripts/web/jobs.py:76` · `100-superskills/skills/kosif-montage-motion/scripts/web/jobs.py:101`

#### ENG-21 · تبويب المشاريع: تركيبات بمعاينة وتعديل مباشر · Projects tab: compositions with live preview and in-place editing · ✅ مُثبت هنا
- **ماذا / what:** Create a composition project (2D motion-kit, 3D three-kit, product lab, Canvas, motion template or compiled manifest), watch it self-play in an iframe, edit index.html / edit.json / verse.json / cues.json in a code box with automatic .bak, then run frames, draft, render or lint.
- **كيف / how:** POST /api/projects {name, kind:new|template|manifest, seconds, fps, size, title, three_d, canvas, lab, template, params}; GET/POST /api/projects/NAME/file {path, content} (text files ≤ 4 MB inside the project only); buttons map to recipes frames(--times 1,3,5), preview, render(--engine studio --blur 4 --workers 0), lint.
- **أرقام / params:** sizes 1080x1920 · 1920x1080 · 1080x1080 · 1080x1350; default seconds 8 (UI 6), fps 30; editable text extensions .html .htm .js .json .css .txt .md .svg .srt .ass .vtt .csv
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:402` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:444` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/app.js:134`

#### ENG-22 · مترجم الخطة إلى manifest وصفحة HTML · Plan → manifest + self-contained 2D HTML compiler · ✅ مُثبت هنا
- **ماذا / what:** Compiles a valid plan into a kosif.motion.manifest.v1 (scenes with title, subtitle, camera, accent) and, for 2D intent, a single HTML page whose window.render(t) draws the frame deterministically — the same contract the local renderer drives.
- **كيف / how:** POST /api/compile {plan} or MCP motion_compile → compile_plan() → project_html(manifest) embedding manifest-player.js; create a project from it with POST /api/projects {kind:'manifest'}.
- **أرقام / params:** page sets data-width/height/duration/fps, window.__duration, window.__ready; default scene titles: فكرة تبدأ · تفاصيل تتضح · من زاوية أخرى · لحظة الأثر · المشهد التالي; subtitles = first 85 chars of the task
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:122` · `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:135`

#### ENG-23 · مصيّر manifest على الخادم بـ Pillow · Pillow server-side manifest renderer with ffprobe verification · ✅ مُثبت هنا
- **ماذا / what:** Renders a silent 2D manifest frame by frame with Pillow, pipes raw RGB into FFmpeg H.264, then verifies the file with ffprobe (single h264 stream, exact size, exact frame count, duration within one frame).
- **كيف / how:** POST /api/render/jobs {manifest} → 202 {job_id, job_token}; poll GET /api/render/jobs/ID with X-Job-Token; GET …/video when succeeded (409 before). wbcompat.render_manifest(): ffmpeg -f rawvideo -pixel_format rgb24 -i pipe:0 -an -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -movflags +faststart.
- **أرقام / params:** frame look: vertical accent gradient (accent*.14 + 17*.86), grid #202a2d every unit/12, three breathing ellipses r=unit*(.17+k*.045)*(.7+.3*ease) drifting sin(t*.4)*unit*.025, accent dot r .026 unit, title unit*.066 #f2f4f3, subtitle unit*.03 #bbc7c9; progress 0→0.95 during frames
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:243` · `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:283` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:151`

#### ENG-24 · مهام التصيير برمز وصول · Capability-token render jobs · ✅ مُثبت هنا
- **ماذا / what:** Each manifest render job gets a random id and a separate 32-byte token; the token is compared in constant time and a wrong or missing token looks exactly like a missing job.
- **كيف / how:** RenderEngine.lookup() with hmac.compare_digest on the X-Job-Token header; DELETE cancels; failed or cancelled jobs delete their folder.
- **أرقام / params:** id token_urlsafe(18), token token_urlsafe(32); 404 wrong token, 409 not ready
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:151` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:167`

#### ENG-25 · تصدير بالتسجيل المباشر · Live recording export (MediaRecorder) · ✅ مُثبت هنا
- **ماذا / what:** Plays the project in real time and records the canvas plus mixed audio; the tab must stay visible.
- **كيف / how:** canvas.captureStream(24) + WebAudio MediaStreamDestination track; MediaRecorder(mimeType first supported of video/webm;codecs=vp8,opus · vp9,opus · webm · mp4; videoBitsPerSecond 5,000,000; audioBitsPerSecond 128,000), timeslice 250 ms; download .webm or .mp4.
- **أرقام / params:** 24 fps, 5 Mbps video, 128 kbps audio; aborted if the tab is hidden
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:92` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:108` · `100-superskills/skills/kosif-montage-motion/tests/studio/export.mock.test.mjs`

#### ENG-26 · تصدير MP4 دقيق بلا زمن حقيقي · Frame-accurate offline MP4 export (WebCodecs + mp4-muxer) · ✅ مُثبت هنا
- **ماذا / what:** Renders every frame after seeking media to the exact time, encodes H.264 with WebCodecs and muxes MP4 in memory; no dropped frames, no real time, no visible tab needed.
- **كيف / how:** encodeOffline({width,height,fps,frames,source:canvas,renderFrame,audioBuffer}); VideoEncoder latencyMode 'quality', keyframe every 2 s, encode queue ≤ 8; Mp4Muxer ArrayBufferTarget fastStart 'in-memory', firstTimestampBehavior 'offset'.
- **أرقام / params:** 30 fps (framePlan); bitrate = min(16 Mbps, w·h·fps·0.15); GOP fps·2 frames
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/offline.mjs:140` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:129` · `100-superskills/skills/kosif-montage-motion/tests/studio/offline.test.mjs`

#### ENG-27 · سلسلة احتياط ملف H.264 · H.264 profile fallback chain · ✅ مُثبت هنا
- **ماذا / what:** Picks the best H.264 profile the browser can encode at the size and rate: High, then Main, then Baseline, then a final Baseline 3.1.
- **كيف / how:** pickVideoCodec(): avc1.6400LL → avc1.4D40LL → avc1.42E0LL → avc1.42E01F where LL = 2A if w·h > 1280·720 or fps > 30 else 1F; isConfigSupported at 8 Mbps.
- **أرقام / params:** levels 1F (3.1) / 2A (4.2)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/offline.mjs:96`

#### ENG-28 · احتياط ترميز الصوت · AAC → Opus audio codec fallback · ✅ مُثبت هنا
- **ماذا / what:** Encodes the mix as AAC-LC when the browser can, otherwise Opus; with neither, the film is exported silent and the report says so.
- **كيف / how:** pickAudioCodec(): ['mp4a.40.2','aac'] then ['opus','opus'] at 192 kbps; AudioData f32-planar blocks of 4096 frames.
- **أرقام / params:** 192 kbps, stereo, 48 kHz
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/offline.mjs:108`

#### ENG-29 · تثبيت مواضع الوسائط عند التصدير · Robust media seeking for export · ✅ مُثبت هنا
- **ماذا / what:** Avoids lost or looping seeks: a newer seek waits while one is in flight, an already-reached target does not re-seek, and export waits for 'seeked' with an 8 s timeout.
- **كيف / how:** seekMedia/flushPendingSeek/stableSeek in media.mjs; tolerance 0.025 s.
- **أرقام / params:** timeout 8000 ms; tolerance 25 ms
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/media.mjs:1` · `100-superskills/skills/kosif-montage-motion/tests/studio/media.test.mjs`

#### ENG-30 · خادم MCP لكوسيف أومني · KOSIF Omni MCP server (65 tools) · ✅ مُثبت هنا
- **ماذا / what:** Standard-library MCP server exposing 65 deterministic tools over stdio and streamable HTTP, plus REST/OpenAPI for ChatGPT Actions, skill resources (kosif://skills/...), slash commands as MCP prompts and a browser console.
- **كيف / how:** python mcp-server/run.py (stdio) | --http --token T --workspace DIR [--corpus DIR] | --console | --list-tools | --print-openapi --profile chatgpt|full; tests: python -m unittest discover -s mcp-server/tests.
- **أرقام / params:** default port 8765; ChatGPT profile 29 read-only ops; version 11.11.0
- **الدليل / proof:** `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/__main__.py` · `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/registry.py` · `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/protocol.py:130`

#### ENG-31 · رسم SVG إجرائي ببايثون · Procedural SVG illustration from Python · ✅ مُثبت هنا
- **ماذا / what:** Builds a full illustration as a list of SVG strings with gradients, patterns and blur filters, deterministic from a seed, so the picture is editable code and scales to any resolution.
- **كيف / how:** out=[]; a=out.append; write <defs> (linearGradient/radialGradient/pattern/filter feGaussianBlur), then layers back-to-front; random.seed(7) for debris/embers; Path(argv[1]).write_text(...). Verified: re-running reproduces the committed SVG byte for byte.
- **أرقام / params:** W,H 1600x900; random.seed(7)
- **الدليل / proof:** `kosif-one/projects/duck-vs-dragon/duck_dragon.py:5-10` · `kosif-one/projects/duck-vs-dragon/duck_dragon.py:242-243` · `kosif-one/projects/duck-vs-dragon/duck_dragon.svg`

#### ENG-32 · طبقة تشغيل مزدوجة · Dual-engine shim (HyperFrames or studio renderer) · ✅ مُثبت هنا
- **ماذا / what:** One composition file renders under HyperFrames' runtime or KOSIF's own window.render(t) contract, and seeks <video data-start> footage frame-exactly.
- **كيف / how:** MOTION.shim(rootId, duration) after registering timelines (MOTION.register / window.__timelines); exposes window.render, window.seek, window.__ready.
- **أرقام / params:** video seek wait up to 4 s, load wait 15 s; waits for document.fonts.ready
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:466` · `kosif-one/tools/kosif-studio/motion/references/hyperframes-authoring.md`

#### ENG-33 · خريطة الخطوات إلى المهارات · Step-to-skill map · ✅ مُثبت هنا
- **ماذا / what:** Where each production step lives: kmotion commands, HyperFrames skills (embedded-captions 35 styles, registry ~400 effects, 24 text effects), 100 Super Skills playbooks, KOSIF Omni tools.
- **كيف / how:** plan.py STEP_SKILLS; references/catalog.md.
- **الدليل / proof:** `kosif-one/tools/kosif-one/scripts/plan.py:188` · `kosif-one/tools/kosif-one/references/catalog.md`

#### ENG-34 · عشوائية ببذرة · Seeded RNG (mulberry32) and hash · ✅ مُثبت هنا
- **ماذا / what:** Deterministic randomness so the same seed renders the same film; Math.random is banned (tests assert it).
- **كيف / how:** const r = MOTION.rng(seed); r(); MOTION.hash(i,j) for stateless per-cell noise.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:119` · `kosif-studio/tests/test_studio.py:570`

#### ENG-35 · أقنعة أشكال مُنعّمة بالعيّنات الفائقة · Antialiased supersampled shape masks · ✅ مُثبت هنا
- **ماذا / what:** Every shape is rasterised at ss x ss resolution with Pillow polygons (Hole polygons erase) and box-reduced, giving clean antialiased coverage at any output size.
- **كيف / how:** Ctx.mask(shape, box) draws polygons into an L image scaled by scale*ss, then Image.reduce(ss); fill() multiplies coverage with paint and blends.
- **أرقام / params:** ss=3 default; Hole polygons fill 0; bbox padded by 3*blur+2 px
- **الدليل / proof:** `kosif-studio/render.py:316` · `kosif-studio/render.py:333` · `kosif-studio/render.py:397`

#### ENG-36 · مستورد SVG · SVG importer (shapes, CSS, transforms, gradients, Arabic text) · ✅ مُثبت هنا
- **ماذا / what:** Turns any SVG (often written by an AI) into painting steps: rect (rounded), circle, ellipse, line, polyline, polygon, full path, text/tspan, g/svg/a/use/symbol, transforms incl. skew, inline style and <style> rules by tag/.class/#id, linear and radial gradients with see-through stops.
- **كيف / how:** svg_import.load_svg(text, max_steps=160) -> (title, steps); fits the viewBox into the sheet with 20 px margin; big elements (>45% of the view) sweep, others grow.
- **أرقام / params:** units % / em,rem x16 / pt x1.333; rgb()/rgba()/hsl()/hsla()/currentColor; ~95 CSS named colours; gradient href chain <= 8; not drawn: filter, mask, clipPath, pattern, image
- **الدليل / proof:** `kosif-studio/svg_import.py:1` · `kosif-studio/svg_import.py:178` · `kosif-studio/svg_import.py:393`

#### ENG-37 · مسارات إنشاء المشروع · Project scaffold routes (flat / 3D / canvas / lab) · ✅ مُثبت هنا
- **ماذا / what:** Four starter templates: a flat GSAP+DOM composition, a cinematic Three.js scene on the three-kit, a single-canvas page driven by window.seek(t), and a product-lab scene with plush 3D characters, HUD and an orbiting lens.
- **كيف / how:** python motion.py new NAME [--3d|--canvas|--lab] --seconds S --fps F --size WxH --title T; 3D without npm rewrites imports to window.K3 and copies three-kit.bundle.js + shape-kit.js.
- **أرقام / params:** --seconds 8 --fps 30 --size 1920x1080 defaults; names must match ^[\w\u0600-\u06FF][\w\u0600-\u06FF-]{0,63}$
- **الدليل / proof:** `kosif-studio/motion/motion.py:126` · `kosif-studio/motion/motion.py:466` · `kosif-studio/tests/test_studio.py:650`

#### ENG-38 · واجهة kmotion الموحدة بقائمة عربية · kmotion one-command hub with Arabic menu · ✅ مُثبت هنا
- **ماذا / what:** One entry point wrapping every tool in five groups (create, sound, edit, check, draw) with an interactive numbered Arabic menu that asks for each argument.
- **كيف / how:** python kmotion.py (menu) | kmotion.py help | kmotion.py COMMAND args
- **أرقام / params:** 47 commands incl. new, render, preview, score, ambience, voice, beats, channels, direct, verse, audio2motion, reel, montage, grade, captions, transcribe, decaption, footage, mocap, silence, aspect, trim, concat, loop, stabilize, export, thumb, probe, batch, fonts, lint, sheet, speed, study, measure,…
- **الدليل / proof:** `kosif-studio/motion/kmotion.py:30` · `kosif-studio/tests/test_studio.py:835`

#### ENG-39 · تجهيز مشروع · Project scaffold · ✅ مُثبت هنا
- **ماذا / what:** Creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter for any style id.
- **كيف / how:** python3 tools/kosif.py scaffold <id> <dir> --starter html-canvas|remotion|none.
- **الدليل / proof:** `kosif-tool/tools/kosif.py` · `kosif-tool/starters`

#### ENG-40 · خط الإنتاج الكامل من الطلب إلى التسليم · End-to-end KOSIF production pipeline · ✅ مُثبت هنا
- **ماذا / what:** Seven-step chain: pick a style id, generate the request, scaffold a project folder, fill STYLE/PLAN, animate in a starter, preview contact sheet, final render with untouched audio, gate with verify_video and TEST_REPORT.
- **كيف / how:** kosif.py search/show -> kosif.py prompt or scaffold <id> <dir> --starter html-canvas|remotion -> words_convert.py transcript -> words.js/public/words.json -> edit scenes -> render_html.cjs --preview -> user approval -> render_html.cjs --audio voice -> verify_video.py --aspect --fps --duration --audio -> fill TEST_REPORT.md
- **أرقام / params:** default deliverable 1080x1920, 30 fps, 15 s (scaffold) / 12 s (starters), H.264 yuv420p + AAC 192k
- **الدليل / proof:** `kosif-tool/tools/kosif.py:101` · `kosif-tool/templates/PLAN.md` · `kosif-tool/tools/render_html.md`

#### ENG-41 · محرك الرندر بوضع seek · render_html seek driver (window.__kosif contract) · ✅ مُثبت هنا
- **ماذا / what:** Deterministic HTML->MP4 where the page exposes window.__kosif={duration,fps?,seek(t)} and optional window.__kosifReady promise; the renderer calls seek(start+i/fps) per frame then screenshots via CDP Page.captureScreenshot.
- **كيف / how:** node tools/render_html.cjs --in film.html --out out.mp4 [--mode seek]; seek(t) may be sync or return a promise; duration defaults to window.__kosif.duration
- **أرقام / params:** frame t = start + i/fps; total = round(duration*fps)
- **الدليل / proof:** `kosif-tool/tools/render_html.cjs:283` · `kosif-tool/tools/render_html.cjs:274` · `kosif-tool/starters/html-canvas/index.html:230`

#### ENG-42 · وضع الزمن الافتراضي لأي صفحة متحركة · render_html virtual-time driver (any CSS/WAAPI/GSAP/rAF page) · ✅ مُثبت هنا
- **ماذا / what:** Renders unmodified animated pages by pausing Chromium's virtual clock and producing exactly one compositor frame per 1000/fps ms through HeadlessExperimental.beginFrame, so CSS animations, Web Animations, rAF timestamps, timers and Date.now are exact.
- **كيف / how:** auto-selected when no window.__kosif hook (browser relaunches with --enable-begin-frame-control etc.) or --mode virtual; needs --duration; cannot seek backwards
- **أرقام / params:** Date.now epoch fixed at 1767225600 (2026-01-01T00:00Z); beginFrame timeout 30000 ms; up to 3 retries if no damage
- **الدليل / proof:** `kosif-tool/tools/render_html.cjs:298` · `kosif-tool/tools/render_html.cjs:52` · `kosif-tool/tools/render_html.cjs:67`

#### ENG-43 · اكتشاف الوضع تلقائيًا · Auto mode detection and relaunch · ✅ مُثبت هنا
- **ماذا / what:** With no --mode the renderer loads the page, checks for window.__kosif.seek and otherwise closes and relaunches Chromium with BeginFrame control under the virtual driver.
- **كيف / how:** omit --mode; log line 'no window.__kosif hook found, switching to virtual mode'
- **الدليل / proof:** `kosif-tool/tools/render_html.cjs:483`

#### ENG-44 · رندر بلا شبكة · Offline render (--offline) · ✅ مُثبت هنا
- **ماذا / what:** Aborts every http(s) request so only local/system fonts and assets are used; output fully reproducible but web fonts (Google Cairo) fall back.
- **كيف / how:** --offline (context.route abort blockedbyclient)
- **الدليل / proof:** `kosif-tool/tools/render_html.cjs:230`

#### ENG-45 · تشفير H.264 مع دمج الصوت دون تعديل · H.264 encode with untouched audio mux · ✅ مُثبت هنا
- **ماذا / what:** PNG frames are encoded with libx264 yuv420p faststart; supplied audio is muxed as AAC 192k with apad + -shortest so the video length decides the end and the voice samples are never retimed; odd sizes are padded to even.
- **كيف / how:** --audio voice.mp3 [--crf 18] ; with --start the audio is also offset by -ss start
- **أرقام / params:** libx264 preset medium, crf 18, -pix_fmt yuv420p, -movflags +faststart, AAC 192k
- **الدليل / proof:** `kosif-tool/tools/render_html.cjs:356`

#### ENG-46 · رندر جزء من الفيلم · Partial render (--start/--duration) · ✅ مُثبت هنا
- **ماذا / what:** Renders only a time window of the film, e.g. the hardest scene, for quick review clips.
- **كيف / how:** --start 4 --duration 3
- **الدليل / proof:** `kosif-tool/tools/render_html.md`

#### ENG-47 · حفظ الإطارات PNG · Frame dump (--frames-dir/--keep-frames) · ✅ مُثبت هنا
- **ماذا / what:** Keeps per-frame PNGs (frame_%06d.png) for compositing elsewhere or debugging.
- **كيف / how:** --frames-dir out/frames or --keep-frames
- **الدليل / proof:** `kosif-tool/tools/render_html.cjs:170` · `kosif-tool/tools/render_html.cjs:456`

#### ENG-48 · إيجاد Playwright و Chromium · Playwright/Chromium resolution order · ✅ مُثبت هنا
- **ماذا / what:** render_html resolves Playwright from cwd, then /opt/node-tools/node_modules/playwright, then $KOSIF_PLAYWRIGHT; never run playwright install on the cloud machine.
- **كيف / how:** set KOSIF_PLAYWRIGHT if needed
- **الدليل / proof:** `kosif-tool/tools/render_html.cjs:138` · `kosif-tool/tools/render_html.md`

#### ENG-49 · محرك الخط الزمني الحتمي · html-canvas deterministic Timeline engine · ✅ مُثبت هنا
- **ماذا / what:** Dependency-free KOSIF.Timeline: scenes {id,t0,t1,el,draw(t,p,local)} are shown only inside their window, an always(t) hook runs every frame, play() loops via rAF; every frame is a pure function of t.
- **كيف / how:** new KOSIF.Timeline({duration,fps,scenes,always,onFrame}); tl.seek(t); window.__kosif={duration,fps,seek:t=>tl.seek(t)}
- **أرقام / params:** sample: 12 s, 30 fps, 4 scenes 0-3.4, 3.4-7.2, 7.2-10.4, 10.4-12 s
- **الدليل / proof:** `kosif-tool/starters/html-canvas/timeline.js:95` · `kosif-tool/starters/html-canvas/index.html:135`

#### ENG-50 · إنشاء مجلد مشروع · kosif.py scaffold (project folder) · ✅ مُثبت هنا
- **ماذا / what:** Creates STYLE.md, PLAN.md, TEST_REPORT.md (placeholders filled incl. frames=round(duration*fps)), words.json, REQUEST.md and a copy of the chosen starter without node_modules/out/media.
- **كيف / how:** python3 tools/kosif.py scaffold <id> <dir> [--starter html-canvas|remotion|none] [--force] [+prompt options]
- **الدليل / proof:** `kosif-tool/tools/kosif.py:540`

#### ENG-51 · خيار التقنية: auto · Stack option: auto · ✅ مُثبت هنا
- **ماذا / what:** Request phrase for stack 'auto': choose best: Remotion for editable sequences, Canvas/SVG for light vector, Three.js for spatial.
- **كيف / how:** --stack auto
- **الدليل / proof:** `kosif-tool/tools/kosif.py:43` · `kosif-tool/web/generator.js`

#### ENG-52 · خيار التقنية: canvas · Stack option: canvas · ✅ مُثبت هنا
- **ماذا / what:** Request phrase for stack 'canvas': starters/html-canvas + render_html.
- **كيف / how:** --stack canvas
- **الدليل / proof:** `kosif-tool/tools/kosif.py:43` · `kosif-tool/web/generator.js`

#### ENG-53 · خيار التقنية: svg · Stack option: svg · ✅ مُثبت هنا
- **ماذا / what:** Request phrase for stack 'svg': SVG + GSAP rendered in virtual-time mode.
- **كيف / how:** --stack svg
- **الدليل / proof:** `kosif-tool/tools/kosif.py:43` · `kosif-tool/web/generator.js`

#### ENG-54 · فحص البيئة ومسارات A/B/C · Environment route check A/B/C · 🟢 جاهز
- **ماذا / what:** Detect whether browser+FFmpeg (A), FFmpeg only (B) or neither (C) exist and pick deliverable accordingly.
- **كيف / how:** python scripts/env_check.py; route C delivers self-playing HTML + synthesized WAV + exact commands
- **أرقام / params:** Route A=browser+ffmpeg, B=ffmpeg, C=none
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:37` · `kosif-studio/motion/env_check.py:89`

#### ENG-55 · تشغيل دفعات · Batch jobs · 🟢 جاهز
- **ماذا / what:** Runs a list of kmotion jobs from jobs.json, several at a time, each in its own process, and writes a report.
- **كيف / how:** python tools.py batch jobs.json --parallel 2 → jobs.report.json
- **أرقام / params:** parallel 2; KOSIF_WORKERS=1 per job
- **الدليل / proof:** `kosif-studio/motion/tools.py:417` · `100-superskills/skills/kosif-montage-motion/SKILL.md:59`

#### ENG-56 · ضبابية حركة حقيقية · GPU sub-frame motion blur · 🟢 جاهز
- **ماذا / what:** Accumulates k sub-frames on the GPU per output frame across a shutter angle for real motion blur.
- **كيف / how:** const render=K3.makeFrameLoop(renderer, post, W, H, update); renderer sets window.__blur=k, __fps, __shutter.
- **أرقام / params:** shutter 0.5 (180 deg) default; half-float accumulation; grain fixed per output frame
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:423` · `100-superskills/skills/kosif-montage-motion/references/motion-craft.md` · `100-superskills/skills/kosif-montage-motion/references/render-farm.md` · `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### ENG-57 · انضباط صفحة الهبوط في ملف واحد · Landing-page single-file HTML discipline · 🟢 جاهز
- **ماذا / what:** One self-contained HTML file: inline CSS/JS, only fonts and the animation library from CDN, required sections, one h1, responsive breakpoints, gsap.set before any tween; validated by a regex structural checker.
- **كيف / how:** Same discipline makes HTML motion compositions portable to the renderer; checker html_validator.py is stdlib-only (review before running).
- **أرقام / params:** breakpoints 900px and 580px; hero H1 68-82px/800; H2 52-62px; body 17-19px; eyebrow 13px tracking 0.2em; card hover translateY(-6px) 0.3s
- **الدليل / proof:** `kosif-atlas/skills/196-landing/621-landing` · `kosif-atlas/skills/196-landing/621-landing/references/single_file_html_discipline.md` · `kosif-atlas/skills/196-landing/621-landing/scripts/html_validator.py`

#### ENG-58 · تحويل HTML إلى صورة PNG مع قص تلقائي · HTML-to-PNG still with auto-trim · 🟢 جاهز
- **ماذا / what:** Design cards, tables and figures as self-contained HTML with a solid body background and padding, render at 2x in headless Chromium, then crop to content by comparing against the background colour and re-pad evenly - crisp stills for lower thirds, end cards and data cards.
- **كيف / how:** Playwright page.screenshot (installed); then PIL: bg = pixel(2,2); mask = |img-bg| > thresh; crop bbox; pad margin x scale. Run render and trim as separate steps. The atlas render.sh hardcodes the macOS Chrome path, so reimplement with Playwright.
- **أرقام / params:** scale 2; margin 16 CSS px (32 device px)
- **الدليل / proof:** `kosif-atlas/skills/3186-create-figure/13532-create-figure/SKILL.md` · `kosif-atlas/skills/3186-create-figure/13532-create-figure/scripts/trim_pad.py` · `kosif-atlas/skills/3186-create-figure/13532-create-figure/scripts/render.sh`

#### ENG-59 · توليد FCPXML لفاينل كت · FCPXML generation · 🟢 جاهز
- **ماذا / what:** Hand an edit to Final Cut Pro (or Resolve/Premiere import) as FCPXML with rational frame times to avoid drift (e.g. 100/2400s per frame at 24 fps, 100/3000s at 30).
- **كيف / how:** Python ElementTree writing resources/format/asset + spine clips + markers; Compressor CLI for batch export on macOS
- **أرقام / params:** rational durations
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/755-final-cut-pro/SKILL.md`

#### ENG-60 · طبقات Lottie · Lottie text/logo layers · 🟢 جاهز
- **ماذا / what:** Play vector animations (logo stings, icons) inside compositions synced to timeline.
- **كيف / how:** lottie-web loadAnimation({renderer:'svg',autoplay:false}) and goToAndStop per frame; dotlottie-player 2.7.12 from jsdelivr.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### ENG-61 · نموذج مشهد محفوظ للـ Canvas · Canvas retained scene model · 🟢 جاهز
- **ماذا / what:** Canvas draws are immediate-mode, so state lives outside: records, scales, mark descriptors, cached Path2D; redraw deterministically per frame.
- **كيف / how:** Size backing store = CSS size x pixelRatio (clamp max 3); layers for static marks / active marks / overlay; HTML for text; redraw from state on every frame t (perfect for seek-based rendering).
- **أرقام / params:** max pixelRatio 3
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10319-canvas2d-data-visualization/references/rendering-architecture.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10319-canvas2d-data-visualization/references/performance-playbook.md`

#### ENG-62 · تصدير البصمة كملف وكود · Fingerprint export: JSON, style bible, runnable ffmpeg script · 🟢 جاهز
- **ماذا / what:** Exports the measured style as JSON, a readable Arabic style bible (Markdown) and a standalone Python script that rebuilds the edit on any footage with ffmpeg only.
- **كيف / how:** DNA.bundle/markdown/python; script args --clips --out --music --srt --mode style|clone --duration --aspect 9:16|16:9|1:1|4:5 (1080x1920...) --fps 30 --res 720|1080 --keep-audio --seed 7 --dry-run; per-shot ffmpeg scale/crop/rotate expressions for camera moves, eq/colorbalance grade, libx264 veryfast crf 18 yuv420p, aac 160k 48 kHz, concat demuxer, music mix (amix 0.3 with clip audio) aac 192k, SRT burn with force_style alignment from the measured band; pure-Python beat tracker (11025 Hz, hop 256…
- **أرقام / params:** crf 18; aac 160k/192k
- **الدليل / proof:** `app/public/js/10_studio.js:1451` · `app/public/js/10_studio.js:1462` · `app/public/js/10_studio.js:1506`

#### ENG-63 · محرك Canvas الأصلي القابل للتقديم · Native Canvas time-seekable renderer · 🟢 جاهز
- **ماذا / what:** drawFrame(canvas, story, t) paints a complete frame as a pure function of absolute time, so preview and export are deterministic.
- **كيف / how:** web/motion.js: find scene where start<=t<end, local progress p, phase=t*1.3; layer gradient, particles, orbit arcs, core ring, waves, Arabic title, footer, progress bar. Verified here: 6 sample times gave 6 distinct frames at 540x960 and 960x540 in headless Chromium.
- **أرقام / params:** phase speed 1.3 rad/s; canvas 540x960 / 960x540 / 720x720 preview
- **الدليل / proof:** `fastify-motion-bro/web/motion.js:4-23` · `fastify-motion-bro/docs/CANVAS-STUDIO.md:3`

#### ENG-64 · استوديو المعاينة في المتصفح · Browser preview studio · 🟢 جاهز
- **ماذا / what:** RTL Arabic web page with canvas, play/pause, 0–1000 seek slider, mm:ss readout and scene jump buttons; loops playback.
- **كيف / how:** npm run preview -> open http://127.0.0.1:4173; player.js fetches project/storyboard.json, sizes canvas by aspect, rAF tick with dt capped at 0.08 s.
- **أرقام / params:** canvas 540x960 (9:16), 960x540 (16:9), 720x720 (1:1); dt cap 80 ms
- **الدليل / proof:** `fastify-motion-bro/web/index.html:1` · `fastify-motion-bro/web/player.js:1-30` · `fastify-motion-bro/web/styles.css`

#### ENG-65 · اختيار المحرك حسب الملف · Renderer switch by storyboard.profile · 🟢 جاهز
- **ماذا / what:** The player routes to the editorial 2.5D renderer when storyboard.profile is 'viral-editorial-3d', otherwise to the native renderer, and exposes window.renderFrame / window.fmbReady for headless export.
- **كيف / how:** player.js draw(t): profile check -> drawEditorialFrame or drawFrame; window.renderFrame=draw; fmbReady=true after init.
- **الدليل / proof:** `fastify-motion-bro/web/player.js:6-13,23-25`

#### ENG-66 · خادم المعاينة المحلي · Local preview server · 🟢 جاهز
- **ماذا / what:** Minimal Node HTTP server bound to 127.0.0.1 that only serves web/, project/, assets/ and examples/ with no-store caching and path-traversal guard.
- **كيف / how:** node scripts/serve.mjs (PORT env, default 4173).
- **أرقام / params:** port 4173; whitelist web|project|assets|examples
- **الدليل / proof:** `fastify-motion-bro/scripts/serve.mjs:1-19`

#### ENG-67 · مخطط ستوري بورد JSON · Storyboard JSON schema · 🟢 جاهز
- **ماذا / what:** Machine-readable timeline consumed by preview and render: version, brief, duration_seconds, aspect, fps, scenes[{id,start,end,title,text,visual,motion,sfx}], optional profile/palette/approval/sound.
- **كيف / how:** Generate with npm run plan or npm run viral -- preview-project, then hand-edit scene text/timing.
- **أرقام / params:** fps 30; ids scene-01..; times in seconds (ms precision)
- **الدليل / proof:** `fastify-motion-bro/project/storyboard.json` · `fastify-motion-bro/scripts/planner.mjs:23` · `fastify-motion-bro/scripts/viral-editorial.mjs:84-92`

#### ENG-68 · محرك الكولاج التحريري 2.5D · Editorial 2.5D collage renderer · 🟢 جاهز
- **ماذا / what:** Second seekable Canvas renderer for the viral-editorial-3d profile: palette background, dot grid, two drifting lines, corner blob, ghost type, floating halftone hero card with icon, orbit + starburst, masked headline. Verified here: 6 distinct frames across 0.1–6.5 s.
- **كيف / how:** drawEditorialFrame(canvas, story, t) in web/editorial.js; scale=w/540; per-scene local time 0–6 s; phase=t*1.06.
- **أرقام / params:** scene 6 s; entrance from .5 s; exit from 4.7 s
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:35-86` · `fastify-motion-bro/docs/VIRAL-EDITORIAL-DNA.md:43`

#### ENG-69 · قانون الحركة القابلة للتقديم · Seek-safe deterministic motion law · 🟢 جاهز
- **ماذا / what:** Registry units derive every frame from timeline time alone (seeded hashes, closed-form noise, quantised boil, paused GSAP) so any frame renders identically in parallel capture.
- **كيف / how:** No CSS animations/requestAnimationFrame state; seed randomness; compute particles/shake/persistence as pure functions of t; register paused timelines on window.__timelines; data-timeline-locked on caption roots.
- **أرقام / params:** e.g. stop-motion floor(t*fps)/fps; phosphor exp(-age/tau); shake value-noise channels
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/camera-shake/camera-shake.html:594` · `kosif-one/vendor/hyperframes/registry/components/stop-motion-cadence/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/oscilloscope-trace/registry-item.json`

#### ENG-70 · كوسف: أداة kmotion الموحدة · KOSIF: kmotion one-command toolbox · 🟢 جاهز
- **ماذا / what:** Arabic-menu dispatcher over motion.py (new/frames/check/render/measure/lint/sheet/speed/beats/channels/inspect/montage/mocap), score.py, ambience.py, voice.py, reel.py, montage.py, decaption.py, transcribe.py; renders via HyperFrames CLI when installed else KOSIF Studio's own frame renderer.
- **كيف / how:** python3 scripts/kmotion.py [help]; python3 scripts/motion.py new NAME --seconds N --fps 30 --size 1920x1080 [--3d].
- **الدليل / proof:** `100-superskills/skills/hyperframes-animation-studio/scripts/kmotion.py` · `100-superskills/skills/hyperframes-animation-studio/scripts/motion.py`

#### ENG-71 · واجهة kmotion الموحدة · Single CLI entry kmotion · 🟢 جاهز
- **ماذا / what:** Every tool behind one CLI; no args shows numbered Arabic menu.
- **كيف / how:** python scripts/kmotion.py help
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:50` · `100-superskills/skills/kosif-montage-motion/README_AR.md`

#### ENG-72 · معاينة تشغيل ذاتي · Self-playing composition preview · 🟢 جاهز
- **ماذا / what:** Any composition opened in a browser plays itself with play/pause/scrub, audio in sync — route C deliverable.
- **كيف / how:** Open index.html
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:125`

#### ENG-73 · استيراد مشروع Studio · Studio import · 🟢 جاهز
- **ماذا / what:** Studio project JSON → timeline spec for full FFmpeg render.
- **كيف / how:** python scripts/kmotion.py studio-import P.kosif.json --out edit.json --media DIR [--render film.mp4]
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### ENG-74 · حزمة claude.ai · build_package claude.ai upload · 🟢 جاهز
- **ماذا / what:** Builds full zip or ≤200-file claude.ai upload, description ≤1024 chars.
- **كيف / how:** python scripts/build_package.py --claude-ai --out x.zip
- **أرقام / params:** 179 files 3.3 MB
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### ENG-75 · تحويل الدالة إلى مفاتيح · Function-to-keyframes sampler (sampled) · 🟢 جاهز
- **ماذا / what:** Turns any function of time into GSAP keyframes so code-driven motion stays seek-safe.
- **كيف / how:** MOTION.sampled(fn, t0, t1, fps) -> keyframes array of {duration:1/fps, ease:'none', ...fn(t)}; feed tl.to(el,{keyframes}).
- **أرقام / params:** 60 keyframes per second default
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:109`

#### ENG-76 · عشوائية ببذرة · Seeded randomness (mulberry32 + hash) · 🟢 جاهز
- **ماذا / what:** Deterministic random numbers so the same seed always gives the same film; no Math.random anywhere.
- **كيف / how:** MOTION.rng(seed)() and MOTION.hash(i,j); the 3D kit exports the same rng.
- **أرقام / params:** mulberry32 constant 0x6D2B79F5
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:119` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:123` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:24`

#### ENG-77 · مُصيّر WebGL مع منحنيات الإضاءة · WebGL renderer with tone curves · 🟢 جاهز
- **ماذا / what:** Deterministic three.js renderer: shadows on, pixel ratio 1, preserveDrawingBuffer, choice of tone mapping.
- **كيف / how:** K3.makeRenderer(canvas, W, H, {tone:'aces'|'agx'|'neutral', exposure}); lab-kit wraps it to honour window.__draftScale.
- **أرقام / params:** tone aces default (agx keeps highlight hue: fire/neon/sunsets; neutral for products); exposure 0.6; PCFShadowMap
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:76` · `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:291`

#### ENG-78 · معالجة خفيفة · Lite post stack · 🟢 جاهز
- **ماذا / what:** Bloom + grade/vignette/grain only, a fraction of makePost cost; same interface for makeFrameLoop; falls back to plain render.
- **كيف / how:** K3S.makeLitePost(renderer, scene, camera, W, H, {bloom, radius, threshold, vignette, grain}).
- **أرقام / params:** bloom .55 radius .5 threshold .82; vignette .38; grain .025
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:365`

#### ENG-79 · معالجة المختبر · Lab lightweight post · 🟢 جاهز
- **ماذا / what:** makePost tuned for fast software GL: bloom low, rays off, DOF opt-in.
- **كيف / how:** K3.labPost(renderer, scene, camera, W, H, {bloom, grain, vignette, dof}).
- **أرقام / params:** bloom .08 threshold .95; grain .05; vignette .18; CA .4; warm .25
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:272`

#### ENG-80 · مسودات سريعة ثلاثية · Draft-scale 3D renders · 🟢 جاهز
- **ماذا / what:** When film.py --draft sets window.__draftScale the GL buffer shrinks so 3D drafts render faster.
- **كيف / how:** Automatic once lab-kit.js wraps K3.makeRenderer.
- **أرقام / params:** pixel ratio = __draftScale
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:291`

#### ENG-81 · مسار الكانفس · Canvas route template (pure function of t) · 🟢 جاهز
- **ماذا / what:** One canvas, a SCENES list of draw(t) functions, window.seek(t) paints any frame exactly; includes closed-form spring, expo-out, exit ease, seeded rng and a BPM clock.
- **كيف / how:** python motion.py new NAME --canvas ...; edit SCENES; render with motion.py render --engine studio (per sub-frame for --blur).
- **أرقام / params:** spring k 170 d 26 (title uses 220/24); out = 1-2^(-10p); exit = p^2.8; BPM 120
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/canvas.html` · `100-superskills/skills/kosif-montage-motion/scripts/motion.py:198`

#### ENG-82 · فيلم بدون متصفح · Workbench Pillow film · 🟢 جاهز
- **ماذا / what:** 2D motion film drawn by Pillow, five-beat titles, cycled accents, works in cloud.
- **كيف / how:** workbench_cli.py 'task' --seconds 12 --aspect 9:16 --titles 'a|b|c' --accents '#E7B65A,#5BD1A5'
- **أرقام / params:** fps 24/25/30/50/60
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/workbench_cli.py`

#### ENG-83 · خط زمني JSON · Timeline JSON → FFmpeg · 🟢 جاهز
- **ماذا / what:** Declarative edit with Arabic text overlays, lower thirds, logos, progress bar, karaoke, music.
- **كيف / how:** timeline.py SPEC --out f.mp4 [--dry-run --inspect]; --example
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py`

#### ENG-84 · استيراد مشروع ستوديو · Studio project import · 🟢 جاهز
- **ماذا / what:** Browser editor JSON → timeline spec for offline render.
- **كيف / how:** studio_import.py project.json --out edit.json --render f.mp4
- **أرقام / params:** presets aurora #0b2a3a sunset #3a1a12 grid #101828
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/studio_import.py:29`

#### ENG-85 · كشف نوع المشروع تلقائيًا · Project kind auto-detection · 🟢 جاهز
- **ماذا / what:** Classifies an existing composition so the right renderer is used: 3D if it uses three-kit or window.K3, canvas if it exposes window.seek, manifest if built from the Workbench, else 2D; reads data-width/data-height for size and the duration from the page.
- **كيف / how:** server._project_info(): regex on index.html; motion.duration_of(); lists template.json/edit.json/verse.json/cues.json, the newest 6 MP4 outputs and up to 12 review frames.
- **أرقام / params:** kinds: 3d | canvas | manifest | 2d
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:402`

#### ENG-86 · تبويب Workbench · Workbench tab (plan → validate → manifest → preview → MP4 → project) · 🟢 جاهز
- **ماذا / what:** A five-button flow in the site: make a plan, validate it, compile the manifest, scrub a canvas preview, render a local MP4 and turn the manifest into an editable project.
- **كيف / how:** app.js wbPlan/wbValidate/wbCompile/wbRender/wbProject handlers; canvas preview with a 0.033 s slider; render polls every 700 ms with the job token and plays the video inline.
- **أرقام / params:** fps choices 24/25/30/50/60; aspects 16:9/9:16/1:1/4:5; default task 'مقدمة عربية أنيقة عن قوة الأفكار…' 12 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/index.html` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/app.js:210`

#### ENG-87 · عقد تصيير صفحات HTML · HTML composition render contract (window.render / __ready / ?capture) · 🟢 جاهز
- **ماذا / what:** Any composition page that exposes window.render(t), window.__duration and window.__ready (and a ?capture mode without UI) can be rendered frame-exactly by the engine; preview players use requestAnimationFrame only for playback.
- **كيف / how:** Pages set body data-composition-id, data-width, data-height, data-duration, data-fps; render(t) is pure in t; kmotion render drives it.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cat.html` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:148` · `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:122`

#### ENG-88 · ساعة المشهد الحتمية render(t) · Deterministic render(t) scene clock · 🟢 جاهز
- **ماذا / what:** Every HTML animation is written as a pure function of time so frame N always looks identical no matter how slowly it is captured; the page signals readiness with window.__ready.
- **كيف / how:** Author the page with window.render = function(t){...} that sets every transform/opacity/camera value from t only (no requestAnimationFrame, Date.now or unseeded Math.random), set window.__ready = true, then drive t = i/fps from the capturer.
- **أرقام / params:** t step = 1/fps (0.0333 s at 30 fps); frame 150 = t 5.00 s; ready wait 60 s
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/animation_craft.md` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/kinetic_2d.html:147` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:186`

#### ENG-89 · إنشاء مشروع أنيميشن 2D/3D · Animation project scaffold (2D/3D) · 🟢 جاهز
- **ماذا / what:** One command creates a ready-to-capture animation project folder from a 2D kinetic or 3D cinema template with title, size, duration and fps baked in.
- **كيف / how:** python scripts/ultra_animator.py new <name> --type 2d|3d --ratio 9:16|16:9|1:1|WxH --seconds 10 --fps 30 --title 'عنوان'; replaces {{TITLE}} {{WIDTH}} {{HEIGHT}} {{DURATION}} {{FPS}} in the template, writes index.html, project.json, STORYBOARD.md, ai_prompts.json, frames/, assets/ (copies three.min.js).
- **أرقام / params:** 9:16=1080x1920, 16:9=1920x1080, 1:1=1080x1080, custom 'WxH' (e.g. 3840x2160)
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/ultra_animator.py:29` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/projects/demo_2d/project.json` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/projects/demo_hero/project.json`

#### ENG-90 · تجميع الإطارات إلى فيديو MP4 · PNG sequence to H.264 MP4 encode · 🟢 جاهز
- **ماذا / what:** Encodes the captured frame sequence into a phone-compatible MP4, optionally muxing a soundtrack, and writes a contact sheet.
- **كيف / how:** python scripts/ultra_animator.py encode <project> --fps 30 --crf 17 [--audio file] [--out f.mp4]; ffmpeg -framerate fps -i frames/f_%04d.png [-i audio -c:a aac -b:a 256k -shortest | -an] -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p; default audio = assets/soundtrack.wav if present.
- **أرقام / params:** libx264 preset slow, CRF 17, yuv420p, AAC 256 kb/s, -shortest
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/ultra_animator.py:200`

#### ENG-91 · تحويل دالة زمنية إلى مفاتيح · Function-of-time to GSAP keyframes (sampled) · 🟢 جاهز
- **ماذا / what:** Samples any function of t at 60 Hz into GSAP keyframes so complex procedural motion remains seekable.
- **كيف / how:** MOTION.sampled(fn, t0, t1, fps=60) -> keyframes array for tl.to(el,{keyframes}).
- **أرقام / params:** 60 keyframes/s
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:109`

#### ENG-92 · عشوائية ببذرة ثابتة · Seeded randomness (mulberry32 rng + hash) · 🟢 جاهز
- **ماذا / what:** Every random choice comes from a seeded generator so a re-render is identical frame for frame.
- **كيف / how:** MOTION.rng(seed)() or MOTION.hash(i,j); Math.random is a lint error.
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:119` · `kosif-one/tools/kosif-studio/motion/qa.py:58`

#### ENG-93 · معاينة ذاتية بشريط تحكم · Self-playing browser preview with scrub bar · 🟢 جاهز
- **ماذا / what:** Opened in a normal browser, a composition plays in real time with audio/footage, scaled to the window, with play/pause, scrub and space-bar.
- **كيف / how:** Automatic from MOTION.shim when not under a renderer (navigator.webdriver, ?render, HyperFrames).
- **أرقام / params:** bar 48 px, play button #E7B65A
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:496`

#### ENG-94 · تمويه حركة حقيقي وتراكم الإضاءة · GPU sub-frame motion blur and lighten stacking · 🟢 جاهز
- **ماذا / what:** render(t) accumulates k sub-frames in a half-float target: averaged for true shutter blur, or max-blended ('lighten') for light trails / star trails / light painting.
- **كيف / how:** makeFrameLoop(renderer, post, W, H, update); motion.py render --blur K --shutter S --stack average|lighten sets window.__blur/__shutter/__stack.
- **أرقام / params:** shutter 0.5 frame (180 deg); --blur 4 ~ +30% render time; long exposure e.g. --blur 16 --shutter 30 --stack lighten
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:423` · `kosif-one/tools/kosif-studio/motion/references/book-lessons.md`

#### ENG-95 · قوالب مشاريع جاهزة · Project scaffolds: 2D, 3D, canvas, lab · 🟢 جاهز
- **ماذا / what:** Creates a ready composition project from a template: flat HyperFrames/GSAP, cinematic Three.js on three-kit, a single-canvas seek(t) page, or the product-lab look.
- **كيف / how:** python motion.py new NAME [--seconds 8] [--fps 30] [--size 1920x1080] [--title ...] [--3d|--canvas|--lab] (or kmotion new).
- **أرقام / params:** templates: composition.html, scene3d/, canvas.html, lab/, directed.html, verse.html
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/motion.py:1` · `kosif-one/tools/kosif-studio/motion/templates/composition.html` · `kosif-one/tools/kosif-studio/motion/templates/canvas.html`

#### ENG-96 · فحص قدرات الجهاز · Machine capability check and routes A/B/C · 🟢 جاهز
- **ماذا / what:** Reports Python libs, FFmpeg, a Chromium-family browser, Node, faster-whisper models, OS voices, GPU, and picks a route.
- **كيف / how:** python motion/env_check.py (JSON + Arabic summary); motion.py doctor.
- **أرقام / params:** Route A full studio (browser+FFmpeg); B footage only (FFmpeg); C preview only (HTML + WAV)
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/env_check.py`

#### ENG-97 · kmotion: قائمة عربية لكل الأدوات · kmotion: one Arabic menu for 48 commands · 🟢 جاهز
- **ماذا / what:** Single entry point grouping create, sound, edit, check and draw commands with an Arabic numbered menu.
- **كيف / how:** python motion/kmotion.py (menu) | help | COMMAND args.
- **أرقام / params:** 48 commands: new bundle kit-bundle frames check render preview sync doctor score ambience voice beats channels direct verse audio2motion reel montage grade captions transcribe decaption footage mocap silence aspect trim concat loop stabilize export thumb probe batch fonts lint sheet speed study meas…
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kmotion.py`

#### ENG-98 · استيراد SVG كخطوات رسم · SVG import as paint steps · 🟢 جاهز
- **ماذا / what:** Turns any AI-written SVG into paint steps (shapes, transforms, CSS, gradients, Arabic text) that render at any size.
- **كيف / how:** svg_import.load_svg(text) / paste in the studio code panel.
- **أرقام / params:** not drawn: filters, masks, clip paths, patterns, embedded images
- **الدليل / proof:** `kosif-one/tools/kosif-studio/svg_import.py`

#### ENG-99 · تشغيل كود الرسم من أي ذكاء اصطناعي · Run any AI drawing code in painter order · 🟢 جاهز
- **ماذا / what:** Runs SVG, KOSIF scenes, PIL (each draw command recorded in order), matplotlib or turtle code in its own process and emits paint jobs.
- **كيف / how:** python runner.py CODE_FILE OUT_DIR [--scale 1.0] [--export PNG].
- **أرقام / params:** 120 s limit in a scratch folder; consecutive PIL commands grouped (360 lines -> 18 strokes)
- **الدليل / proof:** `kosif-one/tools/kosif-studio/runner.py` · `kosif-one/tools/kosif-studio/README.md`

#### ENG-100 · EDL إلى أمر ffmpeg واحد · EDL JSON to single filter_complex · 🟢 جاهز
- **ماذا / what:** Declarative edit list (sources, clips in/out, speed, transition, audio_lead, music, loudnorm, LUT, captions) compiled into one ffmpeg command.
- **كيف / how:** python3 edl_render.py edl.json --out final.mp4 [--dry-run] [--ratios 9:16,1:1] [--copy]
- **أرقام / params:** fps 30, size [1080,1920] in example
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/scripts/edl_render.py` · `100-superskills/skills/pro-video-editor-ffmpeg/templates/edl.example.json`

#### ENG-101 · تجميع MP4 ولوحة تحقق · ffmpeg H.264 encode + contact sheet + GIF · 🟢 جاهز
- **ماذا / what:** Assembles PNG frames into H.264 yuv420p MP4, muxes optional audio, builds contact-sheet.png and optional GIF preview.
- **كيف / how:** python encode.py --frames frames --fps 30 --out x.mp4 --audio a.wav --crf 18 --sheet 12 --gif p.gif
- **أرقام / params:** crf 18; sheet 12 frames 4 cols; pattern f_%04d.png
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/scripts/encode.py`

#### ENG-102 · عشوائية مبذورة · Seeded PRNG (mulberry32) · 🟢 جاهز
- **ماذا / what:** Seeded random generator so particles/instancing are identical every render.
- **كيف / how:** rng(seed) mulberry32-style with 0x6D2B79F5; R=rng(7).
- **أرقام / params:** seed 7
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/templates/scene-2d.html:54`

#### ENG-103 · ذاكرة بصمة التصيير · Render fingerprint cache · 🟢 جاهز
- **ماذا / what:** Skips re-rendering when every text source (html/js/css/json/svg/txt by content) and binary asset (name+size+mtime) plus render parameters hash to the same SHA-1 as the stamp next to the film.
- **كيف / how:** render writes FILM.mp4.kosif.json {fingerprint, params}; --force overrides.
- **أرقام / params:** params hashed: engine, fps, size, scale, blur, shutter, stack, capture, preset, crf, quality, v=4
- **الدليل / proof:** `kosif-studio/motion/motion.py:278` · `kosif-studio/motion/motion.py:315`

#### ENG-104 · مجلد العمل القابل للكتابة · Writable home for projects (KOSIF_MOTION_HOME) · 🟢 جاهز
- **ماذا / what:** Projects and films go to KOSIF_MOTION_HOME if set, else next to the tool when writable, else the working directory, so the tool runs from a read-only skill folder.
- **كيف / how:** export KOSIF_MOTION_HOME=$PWD/work
- **الدليل / proof:** `kosif-studio/motion/motion.py:48` · `kosif-studio/motion/projects/lab_rabbit_lion/README.md`

#### ENG-105 · أعلام كروميوم للثبات · Deterministic Chromium flags · 🟢 جاهز
- **ماذا / what:** Rendering is made pixel-reproducible with fixed flags and context: no font hinting, no LCD text, sRGB colour profile, hidden scrollbars, locale ar, timezone UTC, light colour scheme.
- **كيف / how:** COMMON_FLAGS applied in openBrowser; reducedMotion no-preference
- **أرقام / params:** --font-render-hinting=none --disable-lcd-text --force-color-profile=srgb --hide-scrollbars --disable-partial-raster --disable-skia-runtime-opts --autoplay-policy=no-user-gesture-required
- **الدليل / proof:** `kosif-tool/tools/render_html.cjs:55` · `kosif-tool/tools/render_html.cjs:216`

#### ENG-106 · بذرة عشوائية ثابتة · Seeded Math.random in renderer (--seed) · 🟢 جاهز
- **ماذا / what:** Replaces Math.random inside the page with a mulberry32 PRNG before any page script runs, so random-driven animations reproduce.
- **كيف / how:** --seed <int>; injected with page.addInitScript
- **أرقام / params:** mulberry32 constant 0x6D2B79F5
- **الدليل / proof:** `kosif-tool/tools/render_html.cjs:243`

#### ENG-107 · بوابات الجاهزية قبل الرندر · Readiness gates (fonts + __kosifReady + settle) · 🟢 جاهز
- **ماذا / what:** Before capture the renderer waits for load, networkidle (max 8 s), document.fonts.ready (15 s) and window.__kosifReady, then an optional --settle delay.
- **كيف / how:** --timeout <ms> (default 60000) --settle <ms> (default 0)
- **الدليل / proof:** `kosif-tool/tools/render_html.cjs:261`

#### ENG-108 · قاعدة الحتمية · Determinism rule frame=f(t) · 🟢 جاهز
- **ماذا / what:** No Math.random/Date.now/accumulated state; seed PRNGs.
- **كيف / how:** KOSIF.rng(seed) (mulberry32-style), Remotion random(seed), render_html --seed.
- **أرقام / params:** budget < 50 ms/frame
- **الدليل / proof:** `kosif-tool/playbooks/code.md:24` · `kosif-tool/playbooks/code.md:29` · `kosif-tool/starters/html-canvas/timeline.js:41`

#### ENG-109 · وضع seek في render_html · render_html.cjs seek mode · 🟢 جاهز
- **ماذا / what:** Deterministic HTML/Canvas/SVG → MP4 via Playwright Chromium calling window.__kosif.seek(t) per frame.
- **كيف / how:** node tools/render_html.cjs --in film.html --out film.mp4 [--fps 30 --audio voice.mp3 --start --duration --width --height --crf 18 --scale --seed --offline]
- **أرقام / params:** defaults 1080×1920, 30 fps, CRF 18
- **الدليل / proof:** `kosif-tool/playbooks/render-pipeline.md:29` · `kosif-tool/tools/render_html.cjs`

#### ENG-110 · وضع الزمن الافتراضي · render_html virtual-time mode · 🟢 جاهز
- **ماذا / what:** Render pages using CSS/WAAPI/GSAP animations without a seek hook by advancing Chromium's virtual clock.
- **كيف / how:** --mode virtual; or pause document.getAnimations() and set currentTime=t·1000 inside seek.
- **الدليل / proof:** `kosif-tool/playbooks/render-pipeline.md:30` · `kosif-tool/playbooks/product-ui.md:203`

#### ENG-111 · عقد seek · Seek contract · 🟢 جاهز
- **ماذا / what:** Pages expose window.__kosif = {duration, fps, seek(t)} plus optional window.__kosifReady promise.
- **كيف / how:** See starters/html-canvas/index.html.
- **الدليل / proof:** `kosif-tool/playbooks/render-pipeline.md:77` · `kosif-tool/starters/html-canvas/index.html`

#### ENG-112 · فيديو قابل للبحث عبر Blob · Blob-URL seekable video · 🟢 جاهز
- **ماذا / what:** Fetch each clip as Blob to bypass hosts lacking byte-range so seeks work.
- **كيف / how:** fetch -> URL.createObjectURL -> video.src.
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md` · `kosif-one/vendor/scroll-world/skills/scroll-world/references/scrub-engine.js`

#### ENG-113 · محرك السحب بالتمرير · mountScrollWorld scrub engine · 🟢 جاهز
- **ماذا / what:** Vanilla JS engine building DOM/CSS, lerped scroll->time, section copy fades, particles, mobile clips, reduced motion.
- **كيف / how:** mountScrollWorld(container,{sections,connectors,diveScroll:1.3,connScroll:0.9,crossfade:0.12})
- **أرقام / params:** copy opacity smoothstep; scale 1.03+0.14*local
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/references/scrub-engine.js:66`

#### ENG-114 · حركات GSAP الأساسية · GSAP tween trio (to / from / fromTo / set) · 📦 بأمر تثبيت
- **ماذا / what:** Four primitives cover almost every property animation: go-to, come-from (entrances), explicit start+end, and instant set.
- **كيف / how:** Load gsap (pin version e.g. 3.14.x via npm or a local copy) in an HTML composition; gsap.from() for entrances so CSS holds the final layout; camelCase props; transform aliases x/y/scale/rotation/xPercent instead of raw transform strings; autoAlpha instead of opacity (hides at 0).
- **أرقام / params:** default duration 0.5s; default ease power1.out
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10377-gsap/SKILL.md`

#### ENG-115 · دوران موجه وقيم نسبية ومتغيرات CSS · GSAP directional rotation, relative values & CSS vars · 📦 بأمر تثبيت
- **ماذا / what:** Rotate along a chosen direction, add or multiply relative to current values, and animate CSS custom properties (e.g. hue, variable-font axes).
- **كيف / how:** rotation:'360_cw' / '-170_short' / '90_ccw'; x:'+=20', scale:'*=2'; gsap.to(el,{'--hue':180}); gsap.to('.wordmark',{'--wght':300,'--opsz':72}) with font-variation-settings bound to the vars.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10377-gsap/SKILL.md` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### ENG-116 · quickTo و matchMedia وتقليل الحركة · GSAP quickTo / matchMedia / reduced motion · 📦 بأمر تثبيت
- **ماذا / what:** quickTo builds a reusable setter for high-frequency targets (cursor followers); matchMedia runs setups only under conditions such as desktop width or prefers-reduced-motion.
- **كيف / how:** let xTo=gsap.quickTo('#dot','x',{duration:0.4,ease:'power3'}); gsap.matchMedia().add({isDesktop:'(min-width:800px)', reduceMotion:'(prefers-reduced-motion: reduce)'}, ctx=>{...duration: reduceMotion?0:2}). Mostly for interactive web pieces, not rendered video.
- **أرقام / params:** quickTo duration 0.4
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10377-gsap/SKILL.md`

#### ENG-117 · كائن وسيط يحرك الكانفس · GSAP proxy object driving Canvas · 📦 بأمر تثبيت
- **ماذا / what:** Tween a plain object's time value and redraw a canvas in onUpdate, so procedural canvas art becomes seekable on the GSAP timeline.
- **كيف / how:** var p={time:0}; tl.to(p,{time:5,duration:5,ease:'none',onUpdate:()=>drawFrame(p.time)},0); drawFrame uses a deterministic integer hash (no Math.random).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### ENG-118 · هايبر فريمز: HTML كمصدر للفيديو · HyperFrames: HTML as video source · 📦 بأمر تثبيت
- **ماذا / what:** An HTML file with data-* timing attributes plus a paused GSAP timeline registered on window.__timelines is captured frame-by-frame by headless Chrome into MP4/WebM.
- **كيف / how:** Root div with data-composition-id, data-width/height (1920x1080 or 1080x1920), data-duration; clips get id, data-start, data-duration, data-track-index (track index is not z-order); timelines created {paused:true} and registered synchronously; npx hyperframes init/lint/inspect/preview/render. Requires Node>=22 + FFmpeg + npm package download.
- **أرقام / params:** fps 24/30/60; quality draft|standard|high; workers 1-8
- **تثبيت / install:** `npx hyperframes init/lint/inspect/preview/render`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/SKILL.md` · `kosif-atlas/skills/2702-hyperframes/10379-hyperframes-cli/SKILL.md`

#### ENG-119 · تركيبات فرعية ومسارات · Sub-compositions and tracks · 📦 بأمر تثبيت
- **ماذا / what:** Split a long video into reusable composition files loaded into a root timeline; media and overlays live on numbered tracks.
- **كيف / how:** Sub-file wraps content in <template>; root loads <div data-composition-id data-composition-src='compositions/x.html' data-start data-duration data-track-index>; video always muted playsinline plus a separate <audio> element; animate a wrapper not the <video>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/SKILL.md`

#### ENG-120 · أوامر تصيير هايبر فريمز · HyperFrames CLI render matrix · 📦 بأمر تثبيت
- **ماذا / what:** One CLI handles scaffold, lint, inspect, preview (hot reload studio), render, transcribe and TTS.
- **كيف / how:** npx hyperframes render --fps 60 --quality high; --format webm for transparency; --docker for byte-identical output; --workers auto; templates: blank, warm-grain, play-mode, swiss-grid, vignelli, decision-tree, kinetic-type, product-promo, nyt-graph.
- **أرقام / params:** fps 30 default; 60 doubles render time
- **تثبيت / install:** `npx hyperframes render --fps 60 --quality high`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10379-hyperframes-cli/SKILL.md`

#### ENG-121 · تحريك ريموشن المعتمد على رقم الإطار · Remotion frame-driven animation · 📦 بأمر تثبيت
- **ماذا / what:** Every value is a pure function of useCurrentFrame(); CSS transitions/animations and Tailwind animate classes do not render.
- **كيف / how:** interpolate(frame,[0,0.3*fps],[0,1],{extrapolateLeft:'clamp', extrapolateRight:'clamp', easing:Easing.bezier(0.16,1,0.3,1)}); multi-keyframe arrays with n-1 easings; npx remotion studio/render/still. Needs npm install of remotion packages.
- **أرقام / params:** bezier(0.16,1,0.3,1)
- **تثبيت / install:** `npx remotion studio/render/still`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/SKILL.md` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/timing.md` · `kosif-atlas/skills/235-mas-video-lab/757-remotion/SKILL.md`

#### ENG-122 · التسلسل والسلاسل والتحميل المسبق · Sequence / Series / premount · 📦 بأمر تثبيت
- **ماذا / what:** Place components in time with from/durationInFrames, chain them with Series, and premount to avoid load flashes.
- **كيف / how:** <Sequence from={30} durationInFrames={60} layout='none' premountFor={1*fps}>; <Series><Series.Sequence durationInFrames={45}/>...</Series> with negative offset for overlaps; trimBefore shifts a child's internal clock.
- **أرقام / params:** premount 1s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/sequencing.md` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/SKILL.md`

#### ENG-123 · لوتي داخل الفيديو · Lottie inside timelines · 📦 بأمر تثبيت
- **ماذا / what:** Play After Effects/Bodymovin JSON animations inside a rendered composition, synced to frames.
- **كيف / how:** Remotion: @remotion/lottie <Lottie animationData/> with delayRender/continueRender while fetching JSON. HTML/GSAP: dotlottie-player or lottie.loadAnimation({autoplay:false}) and set frame from timeline; entrance scale 0.3->1 back.out(1.6) 0.35s.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/lottie.md` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### ENG-124 · كود قابل للتحرير في الاستوديو · Studio-editable markup · 📦 بأمر تثبيت
- **ماذا / what:** Write keyframes inline in style props with individual transform properties and named Interactive elements so the Studio can expose drag, resize and easing edits.
- **كيف / how:** <Interactive.Div name='Title' style={{scale: interpolate(...), translate: interpolate(frame,[0,100],['0px 0px','100px 100px']), rotate: ...}}>; inline fixed text; avoid transform strings unless skew/perspective needed; editable clips are separate JSX nodes, not .map().
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10434-remotion-interactivity/SKILL.md` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/SKILL.md` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/video-editing.md`

#### ENG-125 · معالجة لاحقة لعناصر HTML · HtmlInCanvas post-processing · 📦 بأمر تثبيت
- **ماذا / what:** Render DOM into a canvas to apply Canvas2D/WebGL effects to live HTML layers.
- **كيف / how:** <HtmlInCanvas width height onPaint> with ctx.drawElementImage; needs Chrome 149+ with canvas-draw-element flag; nested only in Chrome 152+; enable --gl=angle.
- **أرقام / params:** Chrome 149+
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/html-in-canvas.md`

#### ENG-126 · فريمر موشن · Framer Motion layout & spring · 📦 بأمر تثبيت
- **ماذا / what:** Declarative React animation: initial/animate/exit, gesture states, shared layoutId morphs, AnimatePresence, Reorder lists.
- **كيف / how:** <motion.div layoutId='tab' transition={{type:'spring', stiffness:500, damping:30}}/>; whileHover {scale:1.02,y:-4}; keyframe arrays scale [1,1.05,1]. Real-time (rAF) by default - for video use Remotion instead or drive via manual control; good for interactive artifacts.
- **أرقام / params:** 500/30; 400/17
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/3529-ui-design/14308-interaction-design/references/animation-libraries.md` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### ENG-127 · بطاقات جرافيك لعلامات المونتاج · GFX cards for NLE markers · 📦 بأمر تثبيت
- **ماذا / what:** For each GFX marker on an editor timeline, write one composition HTML matching timeline width/height/fps, render it, and drop it back on the marker.
- **كيف / how:** npx hyperframes render -c compositions/title-02.html -o renders/title-02.mp4 --fps 30; card kinds: chapter title, principle, tradeoff, opinion, before/after table.
- **تثبيت / install:** `npx hyperframes render -c compositions/title-02`
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2458-davinciresolve-gfx-hyperframes/SKILL.md`

#### ENG-128 · عقد طبقات خلفية الشيدر خلف الواجهة · Shader-backed product stage contract · 📦 بأمر تثبيت
- **ماذا / what:** Put GPU atmosphere on its own layer under crisp DOM UI; keep a static CSS background beneath as fallback; give the shader enough exposed area to register or drop it.
- **كيف / how:** .stage{isolation:isolate;overflow:hidden} .shader{position:absolute;inset:0;z-index:0;pointer-events:none} .ui{position:relative;z-index:1}; lazy import, pause offscreen, bounded pixel count.
- **أرقام / params:** Paper Shaders verified 0.0.81 Apache-2.0; DPR cap 2
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/references/shader-backed-ui.md`

#### ENG-129 · التمرير الناعم وتحذير الرندر · Smooth-scroll weight (Lenis) and its render caveat · 📦 بأمر تثبيت
- **ماذا / what:** Lenis gives scroll a weighted glide used on award sites; for frame-accurate video it must be replaced by a deterministic scroll tween.
- **كيف / how:** new Lenis({duration:1.2, easing:t=>Math.min(1,1.001-2**(-10*t))}); lenis.on('scroll', ScrollTrigger.update); gsap.ticker.add(t=>lenis.raf(t*1000)); lagSmoothing(0). For rendering, set scroll position from frame time.
- **أرقام / params:** duration 1.2; expo easing
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md` · `kosif-atlas/skills/100-ui-motion/210-scroll-blur-manifesto`

#### ENG-130 · فيديو إطلاق بمعاملات في ريموشن · Parameterized launch video in Remotion · 📦 بأمر تثبيت
- **ماذا / what:** Data-driven launch/demo films: one zod props schema, calculateMetadata for duration/size, Series for narrative and Sequence for overlays, footage modes none/placeholder/real, same logic for 16:9 and 9:16.
- **كيف / how:** npx create-video@latest (needs network install; kosif-tool has a remotion starter); pin all remotion packages to one exact version; premountFor on Sequences; random(seed) not Math.random.
- **أرقام / params:** fps 30; 1920x1080; overlays: stage badge, elapsed timer, escalation ladder, status, result badge, lower third
- **تثبيت / install:** `npx create-video@latest (needs network install`
- **الدليل / proof:** `kosif-atlas/skills/3198-remotion/13555-remotion-video-builder` · `kosif-atlas/skills/3198-remotion/13555-remotion-video-builder/references/millrace-launch-video.md`

#### ENG-131 · مخطط YAML لفيديو الشرح · Screencast guide YAML schema · 📦 بأمر تثبيت
- **ماذا / what:** Declarative guide: meta (language, voice, resolution), brand colors/logo, intro, steps of type slide (title-card, bullet-points, outro) or screencast (navigate, wait, highlight, click, fill, scroll, hover, screenshot_pause), outro CTA.
- **كيف / how:** Reuse the schema shape for our own Playwright + HTML renderer; the original runs in a Docker container (needs install).
- **أرقام / params:** resolution [1920,1080]; default voice en-US-AriaNeural
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2836-video-guide/11537-video-guide-creator/references/yaml-schema.md` · `kosif-atlas/skills/2836-video-guide/11537-video-guide-creator`

#### ENG-132 · كتالوج مكتبات المكونات المتحركة وتراخيصها · Animated component library catalog with licenses · 📦 بأمر تثبيت
- **ماذا / what:** Where to pull primitives (then restyle): React/Tailwind animated kits, shader/canvas/3D helpers and motion infrastructure, each with license notes.
- **كيف / how:** npm install per project (network); copy-paste kits are snippets not deps.
- **أرقام / params:** motion (ex-framer) MIT; anime.js v4 MIT; auto-animate MIT; lenis MIT; tailwindcss-animate MIT; GSAP custom no-charge (not OSI); open-props easings MIT; paper-shaders Apache-2.0; shadergradient MIT; tsparticles MIT; cobe 5KB globe MIT; r3f+drei MIT; vanta MIT (dated look); magicui MIT; motion-primiti…
- **تثبيت / install:** `npm install per project (network)`
- **الدليل / proof:** `kosif-atlas/skills/342-kernel/1223-frontend/reference/component-sources.md`

#### ENG-133 · تراكيب ريموشن قابلة للتهيئة · Parameterized Remotion compositions · 📦 بأمر تثبيت
- **ماذا / what:** Data-driven React video: one zod props schema per composition, calculateMetadata deriving duration/size from inputs, Series for narrative order and Sequence for overlays, premountFor on asset-heavy sequences, footage modes none/placeholder/real so the timeline renders without real footage.
- **كيف / how:** Scaffold with npx create-video@latest (blank), pin every remotion/@remotion package to the exact same version, default 30 fps 1920x1080, AbsoluteFill layering, staticFile for public assets, spring with high damping and clamped interpolate, random(seed) instead of Math.random; share logic across landscape and vertical outputs.
- **أرقام / params:** 30 fps; 1920x1080; exact version pins
- **تثبيت / install:** `npx create-video@latest (blank), pin every remotion/@remotion package to the exact same version, default 30 fps 1920x1080, AbsoluteFill layering, staticFile for public assets, spring with high damping and clamped interpolate, random(seed) instead of Math`
- **الدليل / proof:** `kosif-atlas/skills/3198-remotion/13555-remotion-video-builder/SKILL.md`

#### ENG-134 · أدوات تصميم النقرات في Slidev · Slidev click choreography toolkit · 📦 بأمر تثبيت
- **ماذا / what:** Markdown slides with click-stepped reveals (v-click, v-clicks with depth), hand-drawn emphasis marks (v-mark underline/circle/highlight/strike/box via Rough Notation), code morphs between blocks (Shiki magic-move with line highlights), v-motion initial/enter states, slide transitions (fade, slide-le…
- **كيف / how:** Needs npm install of @slidev/cli; record or export frames, then cut to narration; ideas transfer to the kosif HTML engine (rough marks via rough-notation, code morph via shiki-magic-move).
- **أرقام / params:** magicMoveDuration (ms); forward delay e.g. 500 ms
- **تثبيت / install:** `npm install of @slidev/cli`
- **الدليل / proof:** `kosif-atlas/skills/2938-slidev/12191-slidev/references/core-animations.md` · `kosif-atlas/skills/2938-slidev/12191-slidev/references/code-magic-move.md` · `kosif-atlas/skills/2938-slidev/12191-slidev/references/animation-rough-marker.md`

#### ENG-135 · الانضباط غير الهدام في التايملاين · Non-destructive timeline discipline · 📦 بأمر تثبيت
- **ماذا / what:** Never edit the source timeline or media: build a reference timeline A (chronological), duplicate to a working timeline B named <A>_edit_<YYYYMMDD_HHMM>, identify clips by filename + timeline TC (not index), test on one representative clip first, dry-run then apply, log every change in an edit-log ma…
- **كيف / how:** Resolve Python API: GetMediaPool, CreateEmptyTimeline/DuplicateTimeline, AppendToTimeline with startFrame/endFrame; scripts offer --dry-run/--reset
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2443-akbun-davinciresolve-timeline-chrono/SKILL.md`

#### ENG-136 · أنماط التايملاين في Remotion · Remotion editable timeline patterns · 📦 بأمر تثبيت
- **ماذا / what:** Two editable structures: independently positioned clips (each <Video> hardcoded from/durationInFrames/trimBefore, gaps/overlaps allowed) or ripple editing via <TransitionSeries> where transitions overlap scenes and shorten total length while overlays (light leak) do not.
- **كيف / how:** @remotion/media Video trimBefore/trimAfter (non-destructive), @remotion/transitions fade()/slide()/wipe() with linearTiming({durationInFrames:15}); needs npm install
- **أرقام / params:** transition 15 f
- **تثبيت / install:** `npm install transition 15 f`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/video-editing.md` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/transitions.md` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/ffmpeg.md`

#### ENG-137 · إعدادات رندر HyperFrames · HyperFrames render settings · 📦 بأمر تثبيت
- **ماذا / what:** HTML+GSAP compositions rendered to video; draft while iterating, standard for review, high for final; WebM keeps alpha for overlay graphics.
- **كيف / how:** npx hyperframes render -c comp.html -o out.mp4 --fps 24|30|60 --quality draft|standard|high --format mp4|webm --workers auto ; doctor checks Chrome/FFmpeg/Node
- **أرقام / params:** fps 30 default
- **تثبيت / install:** `npx hyperframes render -c comp`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10379-hyperframes-cli/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2458-davinciresolve-gfx-hyperframes/SKILL.md`

#### ENG-138 · ريندر WebGPU مع مواد TSL · WebGPU renderer + TSL node materials · 📦 بأمر تثبيت
- **ماذا / what:** Write GPU shaders as chained JavaScript nodes instead of GLSL strings, targeting WebGPU with WebGL2 fallback.
- **كيف / how:** Three.js 'three/webgpu' + 'three/tsl'; new WebGPURenderer(); await renderer.init(); MeshStandardNodeMaterial with colorNode/roughnessNode/positionNode; render headless via Puppeteer/Chromium frame capture to ffmpeg.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/SKILL.md` · `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/core-concepts.md`

#### ENG-139 · سلسلة ما بعد المعالجة في TSL · TSL RenderPipeline post stack · 📦 بأمر تثبيت
- **ماذا / what:** Compose post effects as a node graph: scene pass -> effect nodes -> outputNode.
- **كيف / how:** RenderPipeline(renderer) (renamed from PostProcessing in r183); pass(scene,camera).getTextureNode('output'); renderPipeline.render() instead of renderer.render().
- **أرقام / params:** r183 rename
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/post-processing.md`

#### ENG-140 · إطباق محيطي وانعكاسات وحدود · SSAO / SSR / Outline / FXAA / SMAA nodes · 📦 بأمر تثبيت
- **ماذا / what:** Built-in TSL screen-space passes for contact shadows, reflections, selection outlines and antialiasing.
- **كيف / how:** ao(depth,normal,camera) multiply; ssr(color,depth,normal,camera); outline(scene,camera,objs,{edgeStrength:3,edgeThickness:1}); fxaa()/smaa().
- **أرقام / params:** outline edgeStrength 3.0, thickness 1.0
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/post-processing.md`

#### ENG-141 · دوال WGSL مخصصة · WGSL custom functions in TSL · 📦 بأمر تثبيت
- **ماذا / what:** Inject raw WGSL code as callable nodes when TSL lacks a primitive.
- **كيف / how:** wgslFn() per docs/wgsl-integration.md.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/wgsl-integration.md`

#### ENG-142 · هيكل شيدر في React Three Fiber · R3F shaderMaterial scaffold · 📦 بأمر تثبيت
- **ماذا / what:** Plane mesh + custom vertex/fragment shader with memoized uniforms updated each frame.
- **كيف / how:** @react-three/fiber Canvas; <planeGeometry args={[2,2,32,32]}>; uniforms in useMemo; useFrame sets u_time=clock.elapsedTime. For video use deterministic time = frame/fps.
- **أرقام / params:** plane 32x32 segments
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### ENG-143 · ريندر بلندر بدون واجهة · Headless Blender Cycles render · 📦 بأمر تثبيت
- **ماذا / what:** Script a full scene (geometry, Principled material, camera, area light) and render stills or frame ranges.
- **كيف / how:** blender --background --python script.py; scene.render.engine='CYCLES'; samples 64 + denoise; 1920x1080; prefer bpy.data over bpy.ops; frame range: blender -b f.blend -o //frame_#### -F PNG -s 1 -e 120 -a.
- **أرقام / params:** Area light 400W; roughness 0.35; cam (4.5,-4.5,3.2) rot 65°/45°
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/228-mas-3d-games/705-blender/SKILL.md`

#### ENG-144 · خريطة اختيار المحرك · Engine selection map · 📦 بأمر تثبيت
- **ماذا / what:** Three.js for custom scenes; deck.gl for big geo layers/trips/arcs; CesiumJS for globes/terrain; PixiJS for 2D sprites/particles; regl/TWGL for minimal custom shaders; Babylon for full engine.
- **كيف / how:** Pick per scene type.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/SKILL.md`

#### ENG-145 · تقليص الخط · Font subsetting · 📦 بأمر تثبيت
- **ماذا / what:** Cut font files to used glyphs to speed browser renders.
- **كيف / how:** fonttools pyftsubset --unicodes or --text-file; keep Arabic presentation features (--layout-features='*').
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14126-web-typography/references/css-implementation.md` · `kosif-atlas/skills/564-font-optimizer/1593-font-opt/SKILL.md`

#### ENG-146 · تضمين لوتي · Lottie embedding · 📦 بأمر تثبيت
- **ماذا / what:** Play vector Lottie JSON animations deterministically inside a render.
- **كيف / how:** Remotion @remotion/lottie with delayRender/continueRender; in GSAP/HyperFrames scale-in back.out(1.6). Check each Lottie's license.
- **أرقام / params:** back.out(1.6), 0.35s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/lottie.md` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### ENG-147 · تصيير خرائط WebGL حتمي · Deterministic WebGL map rendering · 📦 بأمر تثبيت
- **ماذا / what:** Settings that make Mapbox/MapLibre/MapTiler frames reproducible when captured frame by frame.
- **كيف / how:** interactive:false, fadeDuration:0, attributionControl handled explicitly, canvasContextAttributes.preserveDrawingBuffer:true; hold the first frame until sources/layers are added and the map fires 'idle'; per frame: setData/setPaintProperty -> once('idle') -> triggerRepaint; do not call map.remove() in cleanup; drive everything from the frame number, never CSS transitions or timers; render with --gl=angle and concurrency 1 while validating.
- **أرقام / params:** --gl=angle; --concurrency=1; fadeDuration 0
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/TECHNIQUE.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maplibre/TECHNIQUE.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-explainer-architecture.md`

#### ENG-148 · خط مخططات بايثون الثابتة · Python static chart pipeline · 📦 بأمر تثبيت
- **ماذا / what:** matplotlib/seaborn (optionally SciencePlots) to produce chart frames or overlays, then ffmpeg to assemble.
- **كيف / how:** Object-oriented API, layout='constrained' (do not also call tight_layout), style context per figure, savefig PNG at exact pixel size (figsize*dpi) for frames or SVG with text kept as <text>; presentation preset: font 14, labels 16, titles 18, ticks 12, lines 2.5, markers 8, no top/right spines. Frame-by-frame animation by re-plotting per t is slow; prefer HTML/SVG for motion and Python for analysis/static plates.
- **أرقام / params:** presentation: 14/16/18/12 pt, lines 2.5; savefig dpi 300
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/SKILL.md` · `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/assets/presentation.mplstyle` · `kosif-atlas/skills/2657-figures/10111-plot-styling/SKILL.md`

#### ENG-149 · القواعد التصريحية للمخططات · Declarative grammars (Vega-Lite / Observable Plot) · 📦 بأمر تثبيت
- **ماذا / what:** Compact specs (data + marks + encodings + transforms) for standard charts; easy to validate and store.
- **كيف / how:** Use while the spec stays readable; leave for D3/Canvas when custom layout, choreographed motion or many marks are needed. For video: render each state to SVG and tween in our page, or export static plates; vl-convert/node needed for headless export.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10325-grammar-of-graphics-and-declarative-visu/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10325-grammar-of-graphics-and-declarative-visu/references/vega-lite-and-vega.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10325-grammar-of-graphics-and-declarative-visu/references/observable-plot.md`

#### ENG-150 · D3 كمحرك رياضيات وهندسة · D3 as math and geometry engine · 📦 بأمر تثبيت
- **ماذا / what:** Use D3 for scales, shapes, layouts, geo projections and annotation geometry; let our timeline own rendering and time.
- **كيف / how:** Modules: d3-array, d3-scale, d3-axis, d3-shape cover most charts; d3-force/d3-hierarchy/d3-geo only when the data needs them; stable keys in joins; separate parsing, scales, derived geometry, rendering, state. For deterministic video compute every frame from t (no d3.transition timers) or use transitions only under the virtual-time renderer.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/references/d3-module-map.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/references/d3-architecture-patterns.md`

#### ENG-151 · مكتبات المخططات الجاهزة · Product chart libraries · 📦 بأمر تثبيت
- **ماذا / what:** ECharts, Chart.js, Recharts, visx, Plotly when speed of integration beats custom semantics; ECharts GL and Plotly WebGL for large data.
- **كيف / how:** ECharts has built-in transitions and effectScatter ripples; Recharts for React; Plotly for interactive HTML (needs kaleido for static export). In video use them only with animation disabled and state set per frame, or with the virtual-time renderer.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10333-typescript-data-visualization-engineerin/references/library-selection-for-builders.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10322-data-visualization/references/default-stack-selection.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/SKILL.md`

#### ENG-152 · صيغة JSON لسير عمل ComfyUI · ComfyUI API-format workflow JSON · 📦 بأمر تثبيت
- **ماذا / what:** ComfyUI graphs are JSON maps of string node ids to {class_type, inputs}, where inputs are literals or [source_id, output_index] links.
- **كيف / how:** Discover nodes with GET /object_info/{class} and models with GET /models/{folder} before wiring; basic T2I: CheckpointLoaderSimple → CLIPTextEncode ×2 → EmptyLatentImage → KSampler → VAEDecode → SaveImage; GGUF: UnetLoaderGGUF + CLIPLoaderGGUF + VAELoader.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2819-comfyui/11445-comfyui-workflow-design` · `kosif-atlas/skills/2819-comfyui/11439-comfyui-api`

#### ENG-153 · التحكم في ComfyUI عبر REST وWebSocket · ComfyUI REST and WebSocket control · 📦 بأمر تثبيت
- **ماذا / what:** Queue, monitor and fetch ComfyUI jobs headlessly.
- **كيف / how:** POST /prompt {prompt, client_id} → prompt_id/node_errors; GET /history/{id} until status success; outputs via GET /view?filename&subfolder&type (preview 'webp;50'); ws://host/ws?clientId=uuid4 for progress; POST /upload/image; POST /free {unload_models, free_memory} on OOM; GET /system_stats, /queue; POST /interrupt.
- **أرقام / params:** default port 8188
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2819-comfyui/11439-comfyui-api` · `kosif-atlas/skills/2736-charly-comfyui/10712-comfyui`

#### ENG-154 · قوالب ComfyUI الفرعية ووضع التطبيق · Reusable ComfyUI subgraph blueprints and app mode · 📦 بأمر تثبيت
- **ماذا / what:** Package a stage (e.g. upscale + face fix) as a subgraph, publish it as a blueprint in the node library, or expose a simplified App Mode UI.
- **كيف / how:** Subgraphs need frontend ≥1.24.3, blueprints ≥1.27.7, App Mode ≥1.41.13; blueprint instances are snapshots — editing the master does not update placed copies.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2142-comfyui-plugin/7656-comfy-subgraphs-app-mode`

#### ENG-155 · مكساج الصوت أوفلاين · Offline audio mixdown · 📦 بأمر تثبيت
- **ماذا / what:** All tracks (main media, music, voice, SFX stems, montage segment audio) are mixed sample-accurately for the frame-accurate render.
- **كيف / how:** mixAudio(D): OfflineAudioContext(2 ch, 48 kHz), BufferSource per track with loop/in-point, gain automation; reports files whose audio could not be decoded.
- **أرقام / params:** 48000 Hz stereo
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:2234` · `app/public/js/10_studio.js:3891`

#### ENG-156 · بناء فيلم بستايل من المكتبة · Motion-kit film builder (11 styles) · 📦 بأمر تثبيت
- **ماذا / what:** Turns a timed script into a whole-timeline film drawn by one of 11 procedural styles, with its own SFX stem, a music bed and an optional aligned voice-over.
- **كيف / how:** KIT.build({style,script|lines,title,duration,voiceFile|voice,speed}): parse -> speedTimings (or align to voice) -> scene type 'motionkit' with params {style,lines,title,pal,fonts,seed} cached per signature -> KIT.sfxEvents stem -> SND.music bed; KIT.ORDER = lyric, plotter, doodle, whiteboard, chalkboard, stickman, isometric, fake3d, infographic, mapjourney, product; brand colours/fonts remap style roles (KIT.brandPal/brandFonts); reference DNA can recolour (KIT.palFromDNA).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:903` · `app/public/js/10_studio.js:999` · `app/public/js/10_studio.js:949`

#### ENG-157 · مركز الملفات وأدوارها · Input hub with file roles and document text · 📦 بأمر تثبيت
- **ماذا / what:** Drop anything (video, audio, photos, PDF, DOCX, text, SRT, fonts, zip, JSON, links); each file gets a guessed role the user can change; documents become script sources.
- **كيف / how:** HUB.ROLES: video main/clip/ref/bg; audio music/voice/sfx; image clip/logo/asset/layer/bg; pdf doc/brand; text doc/script/brand; captions; font; zip; json; link ref. Role guessed from file names (ref/مرجع, logo/شعار, voice/تعليق, music/أغنية). PDF via pdf.js 3.11.174 (<= 40 pages, refuses image-only PDFs with an OCR hint); DOCX via mammoth 1.6.0.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:2692` · `app/public/js/10_studio.js:2705` · `app/public/js/10_studio.js:2772`

#### ENG-158 · الريندر السريع · Fast realtime render (MediaRecorder) · 📦 بأمر تثبيت
- **ماذا / what:** Records the live canvas plus mixed audio in real time; MP4 when the browser supports it, otherwise WebM (named honestly).
- **كيف / how:** canvas.captureStream(30) + MediaStreamDestination audio; MIME priority video/mp4 avc1.42E01E+mp4a.40.2 -> video/mp4 -> webm vp9/opus -> vp8/opus -> webm; 8 Mbps video, 160 kbps audio; chunks every 250 ms; render takes real time.
- **أرقام / params:** 30 fps; 8 Mbps; 160 kbps
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:1725` · `app/public/js/00_editor.js:1733`

#### ENG-159 · ريندر دقيق إطار بإطار · Frame-accurate MP4 render (WebCodecs + mp4-muxer) · 📦 بأمر تثبيت
- **ماذا / what:** Draws and encodes every frame on its own with media elements parked at exact times, mixes audio offline and muxes H.264 + AAC into MP4.
- **كيف / how:** renderHQ (studio copy replaces editor copy): VideoEncoder H.264 avc1.640028 (<= 720p30) or avc1.64002A (1080p or 60 fps), fallback 60->30 fps / avc1.640029; bitrate 10 Mbps (<= 1 MP), 16 Mbps (> 1 MP), 20 Mbps (> 1 MP at 60 fps); keyframe every 2 s; encode queue <= 6; AudioEncoder mp4a.40.2 48 kHz stereo 160 kbps in 4800-sample chunks; Mp4Muxer 5.1.3 (cdn.jsdelivr) fastStart in-memory; falls back to the fast render when unsupported or audio missing; saved to 'My videos'.
- **أرقام / params:** 720p/1080p; 30/60 fps
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:2249` · `app/public/js/10_studio.js:1935` · `app/index.html:12`

#### ENG-160 · حفظ المشروع والتراجع · Project file, autosave and undo · 📦 بأمر تثبيت
- **ماذا / what:** Projects save as JSON (style, captions, overlays, SVG stickers, scenes with code, cuts, fix) without media; autosave every 6 s; undo up to 25 steps; handoff export includes cuts, beats, BPM and the motion prompt.
- **كيف / how:** projectData v4 / handoff v3; autosave < 1.5 MB to localStorage basma.autosave; loadProject marks external code scenes untrusted; Ctrl/Cmd+Z, Space play, arrows +-1 s (Shift +-5 s).
- **أرقام / params:** autosave 6 s; undo 25
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:2134` · `app/public/js/00_editor.js:2146` · `app/public/js/00_editor.js:2210`

#### ENG-161 · مكتبة فيديوهاتي · Local video library · 📦 بأمر تثبيت
- **ماذا / what:** Every finished render is kept in IndexedDB with title, size, cost and thumbnail (last 30) for replay and download.
- **كيف / how:** VLIB.add(blob) in 'basma-videos'; UI.videos dialog; WebM files keep .webm extension.
- **أرقام / params:** last 30
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:4575` · `app/public/js/10_studio.js:4584` · `app/public/js/10_studio.js:4605`

#### ENG-162 · جسر السيرفر الآمن · Server bridge with SSRF guard · 📦 بأمر تثبيت
- **ماذا / what:** Vite dev/preview middleware proxies Gemini and Anthropic with server-side keys and hosts helper routes; only public https hosts are allowed and every redirect hop is re-checked.
- **كيف / how:** routes /api/gemini/*, /api/anthropic/* (180 s, 300 s for long-running/streams), /api/basma-health, /api/gemini-status, /api/basma-echo, /api/basma-media, /api/basma-stock, /api/basma-templates (6 h cache), /api/basma-page, proxy /api/ping|media|search|file -> 127.0.0.1:8771; blockedHost covers localhost, 10/8, 192.168/16, 172.16/12, 169.254/16, 100.64/10, IPv6 literals, .local/.internal, numeric hosts; max 6 redirects; errors returned as 200 + x-basma-status.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/vite.config.ts:16` · `app/vite.config.ts:240`

#### ENG-163 · مسار Remotion · Remotion route (target) · 📦 بأمر تثبيت
- **ماذا / what:** React-based sequencing for long edits with Remotion Studio review, referencing motalim-ai/motion-starter-kit (MIT). Not wired in this repo.
- **كيف / how:** Only after installing Remotion and validating it; otherwise use Native Canvas.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `fastify-motion-bro/docs/ENGINE_ROUTER.md:3` · `fastify-motion-bro/docs/SOURCE_AUDIT.md:3`

#### ENG-164 · مسار HyperFrames · HyperFrames route (target) · 📦 بأمر تثبيت
- **ماذا / what:** HTML/CSS seekable compositions rendered to video (heygen-com/hyperframes, Apache-2.0); runtime not bundled; recent versions need Node >= 22.
- **كيف / how:** Install separately, check Node version, verify render before use.
- **أرقام / params:** Node >= 22
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `fastify-motion-bro/docs/ENGINE_ROUTER.md:4` · `fastify-motion-bro/docs/SOURCE_AUDIT.md:8`

#### ENG-165 · تصدير MP4 حتمي · Deterministic Playwright->FFmpeg MP4 export · 📦 بأمر تثبيت
- **ماذا / what:** Renders every frame by calling window.renderFrame(i/fps) in headless Chromium, grabs canvas PNG, and pipes it into FFmpeg as H.264.
- **كيف / how:** python scripts/render.py --smoke|--approved --height H --fps F --output path [--audio file]; Playwright launches chromium (--disable-gpu --no-sandbox), injects window.__FMB_STORYBOARD__, intercepts http://fmb.local/** to serve repo files offline, then ffmpeg -f image2pipe -vcodec png -framerate F -i pipe:0 -c:v libx264 -pix_fmt yuv420p -preset veryfast -crf 19 -movflags +faststart.
- **أرقام / params:** height even 144–3840; fps 1–60; CRF 19; preset veryfast; yuv420p; width=h*9/16|16/9|1
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `fastify-motion-bro/scripts/render.py:1-77` · `fastify-motion-bro/requirements-render.txt:1`

#### ENG-166 · خدمة الملفات دون خادم · Offline route-interception asset serving · 📦 بأمر تثبيت
- **ماذا / what:** During export no web server runs: Playwright fulfils requests to a fake host from local web/ and project/ only.
- **كيف / how:** page.route('http://fmb.local/**') -> resolve under ROOT, 403 outside web/ or project/, guess MIME.
- **أرقام / params:** allowed prefixes web/, project/
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `fastify-motion-bro/scripts/render.py:49-59` · `fastify-motion-bro/docs/CANVAS-STUDIO.md:5`

#### ENG-167 · صيغة التركيب HTML · HTML composition format · 📦 بأمر تثبيت
- **ماذا / what:** A video is a plain HTML file: a root element with data-composition-id plus width/height, and timed children carrying class=clip.
- **كيف / how:** Write index.html with root <div data-composition-id data-width=1920 data-height=1080>; children get data-start/data-duration/data-track-index; render with hyperframes render.
- **أرقام / params:** root 1920x1080 default; clips need class=clip
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/concepts/compositions.mdx`

#### ENG-168 · تراكيب فرعية متداخلة · Nested sub-compositions · 📦 بأمر تثبيت
- **ماذا / what:** Reusable scene files mounted inside the root with their own timeline window.
- **كيف / how:** <div data-composition-id=x data-composition-src=compositions/x.html data-start data-duration data-playback-start>; register window.__timelines['x'].
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/concepts/compositions.mdx`

#### ENG-169 · نموذج زمن حتمي بالبحث · Seek-driven deterministic time model · 📦 بأمر تثبيت
- **ماذا / what:** Every frame is computed as time=floor(frame)/fps and all animations are seeked, never played; fps/size/variables locked before frame 0.
- **كيف / how:** Keep GSAP timelines paused and registered; avoid Date/Math.random/rAF (lint non_deterministic_code, requestanimationframe_in_composition).
- **أرقام / params:** t=frame/fps
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/concepts/determinism.mdx` · `kosif-one/vendor/hyperframes/packages/lint/src/rules/core.ts`

#### ENG-170 · محولات الإطارات · Frame adapters (GSAP, CSS, Anime.js, Lottie, Three.js, WAAPI, TypeGPU) · 📦 بأمر تثبيت
- **ماذا / what:** Runtime seeks several animation libraries; custom hosts implement init/seekFrame/destroy.
- **كيف / how:** createGSAPFrameAdapter({fps:30,timeline}) from @hyperframes/core; adapter must support random/backward seeks.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/concepts/frame-adapters.mdx`

#### ENG-171 · أمر: إنشاء مشروع · CLI: init · 📦 بأمر تثبيت
- **ماذا / what:** Scaffold a project; --example, --resolution landscape|portrait|landscape-4k|portrait-4k|square|square-4k, --video/--audio (auto Whisper captions), --tailwind, --non-interactive, --skip-transcribe, --model, --language.
- **كيف / how:** npx hyperframes init ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** Scaffold a project; --example, --resolution landscape|portrait|landscape-4k|portrait-4k|square|square-4k, --video/--audio (auto Whisper captions), --tailwind, --non-interactive, --skip-transcribe, --model, --language.
- **تثبيت / install:** `npx hyperframes init`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### ENG-172 · أمر: تصيير · CLI: render · 📦 بأمر تثبيت
- **ماذا / what:** Render to mp4|webm|mov|gif|png-sequence|hls; --fps 1-240 or 30000/1001; --quality draft|looks(CRF16)|standard|high|delivery; --crf 0-51, --video-bitrate, --workers 1-24 (~256MB each), --gpu (NVENC/VideoToolbox/AMF/VAAPI/QSV), --docker, --hdr/--sdr, --resolution supersample, --gif-loop, --hls-segment…
- **كيف / how:** npx hyperframes render ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** Render to mp4|webm|mov|gif|png-sequence|hls; --fps 1-240 or 30000/1001; --quality draft|looks(CRF16)|standard|high|delivery; --crf 0-51, --video-bitrate, --workers 1-24 (~256MB each), --gpu (NVENC/VideoToolbox/AMF/VAAPI/QSV), --docker, --hdr/--sdr, --resolution supersample, --gif-loop, --hls-segment…
- **تثبيت / install:** `npx hyperframes render`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### ENG-173 · أمر: معاينة · CLI: preview · 📦 بأمر تثبيت
- **ماذا / what:** Studio preview server on port 3002; --background, --proxy transcodes HEVC/ProRes/AV1, --browser-gpu.
- **كيف / how:** npx hyperframes preview ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** Studio preview server on port 3002; --background, --proxy transcodes HEVC/ProRes/AV1, --browser-gpu.
- **تثبيت / install:** `npx hyperframes preview`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### ENG-174 · أمر: التقاط موقع · CLI: capture · 📦 بأمر تثبيت
- **ماذا / what:** Capture a website into assets/screenshots (max 21) with AI image captioning, --video download mode.
- **كيف / how:** npx hyperframes capture ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** Capture a website into assets/screenshots (max 21) with AI image captioning, --video download mode.
- **تثبيت / install:** `npx hyperframes capture`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### ENG-175 · أمر: الكتالوج والإضافة · CLI: catalog / add · 📦 بأمر تثبيت
- **ماذا / what:** List/search registry blocks & components (--type block|component, --tag, --query, --on-device) and paste one into a project.
- **كيف / how:** npx hyperframes catalog ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** List/search registry blocks & components (--type block|component, --tag, --query, --on-device) and paste one into a project.
- **تثبيت / install:** `npx hyperframes catalog`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### ENG-176 · أمر: عرض ونشر · CLI: present / play / publish · 📦 بأمر تثبيت
- **ماذا / what:** Present or play a composition; publish to hosted project (--public, --space).
- **كيف / how:** npx hyperframes present ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** Present or play a composition; publish to hosted project (--public, --space).
- **تثبيت / install:** `npx hyperframes present`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### ENG-177 · أمر: أدوات الصيانة · CLI: doctor / info / compositions / benchmark / clean / upgrade / browser · 📦 بأمر تثبيت
- **ماذا / what:** Environment diagnosis, project info, benchmarks, cache cleanup, Chrome management.
- **كيف / how:** npx hyperframes doctor ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** Environment diagnosis, project info, benchmarks, cache cleanup, Chrome management.
- **تثبيت / install:** `npx hyperframes doctor`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### ENG-178 · أمر: التصيير السحابي · CLI: cloud / lambda / cloudrun · 📦 بأمر تثبيت
- **ماذا / what:** Hosted render (cloud render/list/get/delete) and self-hosted AWS Lambda / GCP Cloud Run deployment commands.
- **كيف / how:** npx hyperframes cloud ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** Hosted render (cloud render/list/get/delete) and self-hosted AWS Lambda / GCP Cloud Run deployment commands.
- **تثبيت / install:** `npx hyperframes cloud`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### ENG-179 · أمر: استيراد التصميم · CLI: figma / events / claude-design · 📦 بأمر تثبيت
- **ماذا / what:** Figma import and Claude Design handoff commands.
- **كيف / how:** npx hyperframes figma ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** Figma import and Claude Design handoff commands.
- **تثبيت / install:** `npx hyperframes figma`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### ENG-180 · محرك التصيير المحلي · Render backends: local Chrome + FFmpeg · 📦 بأمر تثبيت
- **ماذا / what:** Producer drives headless Chrome (puppeteer) per worker, captures frames (BeginFrame/screenshot/fast draw-element), streams to FFmpeg.
- **كيف / how:** @hyperframes/producer createRenderJob/executeRenderJob; env HF_SEGMENTED_CAPTURE, HF_SEGMENT_FRAMES=3000, PRODUCER_ENABLE_STREAMING_ENCODE.
- **أرقام / params:** workers 1-24; low-memory at <=8GB
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/producer/src/index.ts` · `kosif-one/vendor/hyperframes/docs/packages/cli.mdx`

#### ENG-181 · استوديو التحرير · Studio editor + WebMCP · 📦 بأمر تثبيت
- **ماذا / what:** React/CodeMirror timeline editor; exposes ~12 WebMCP tools with commit stages refused/dispatched/saved/verified/failed.
- **كيف / how:** hyperframes preview; browser agent uses studio_inspect/studio_frame.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/webmcp.mdx` · `kosif-one/vendor/hyperframes/packages/studio/package.json`

#### ENG-182 · حزمة SDK للتحرير · SDK open/edit/serialize · 📦 بأمر تثبيت
- **ماذا / what:** Programmatic editing of compositions with persistence adapters.
- **كيف / how:** @hyperframes/sdk.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/sdk`

#### ENG-183 · عقد تركيب المكونات · Component mount contract · 📦 بأمر تثبيت
- **ماذا / what:** Every registry component is an elastic HTML template with one paused GSAP timeline keyed by its name; hosts mount it as a clip and pass only changed variables.
- **كيف / how:** <div class="clip" data-composition-src="compositions/components/<name>.html" data-start="2" data-duration="4" data-track-index="1" data-variable-values='{"text":"..."}'></div>; variables declared in data-composition-variables on <html>; cues = comma seconds from mount start; exit defaults to none (primitives hold last frame, frame root owns transitions); units fill the host box via container queries.
- **أرقام / params:** variable roles content|style|timing|layout; accent enum green|blue|violet; exit none|fade|up; IN/HOLD/OUT envelope, hold is elastic
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/CATALOG.md` · `kosif-one/vendor/hyperframes/registry/components/per-word-rise/per-word-rise.html`

#### ENG-184 · بحث دلالي في الكتالوج · Semantic catalog search · 📦 بأمر تثبيت
- **ماذا / what:** On-device vector search over all installable registry items so the right block/component can be found by intent words.
- **كيف / how:** `npx hyperframes catalog --query "<words>" --on-device` fetches local-vectors.json/.bin (384-dim bge-small-en-v1.5 quantised ONNX, rows embedded from title+description+tags in batches of 16); media-vectors index the bundled SFX manifest.
- **أرقام / params:** 384 dims; Float32 row-major; revision sha256 = registry.json catalogArtifact.revision 973eda0e...
- **تثبيت / install:** `npx hyperframes catalog --query "<words>" --on-device` fetches local-vectors`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/catalog-artifact/README.md` · `kosif-one/vendor/hyperframes/registry/catalog-artifact/local-vectors.json` · `kosif-one/vendor/hyperframes/registry/registry.json`

#### ENG-185 · واجهات HTML داخل الكانفس · HTML-in-Canvas live screens · 📦 بأمر تثبيت
- **ماذا / what:** Live HTML (phone/laptop UIs, panels) is drawn into a canvas texture each frame so WebGL/3D models (GLTF iPhone/MacBook) can show real, editable UI on their screens.
- **كيف / how:** <canvas layoutsubtree> wraps the HTML; script checks typeof ctx.drawElementImage === "function" and calls ctx.drawElementImage(el, 0, 0, w, h) then uploads to a Three.js texture; requires a Chromium build with the experimental HTML-in-Canvas API enabled.
- **أرقام / params:** phone 390x844, laptop 1440x900 screen buffers (ios26-liquid-glass)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/ios26-liquid-glass/ios26-liquid-glass.html:839` · `kosif-one/vendor/hyperframes/registry/blocks/ios26-liquid-glass/ios26-liquid-glass.html:1102` · `kosif-one/vendor/hyperframes/registry/blocks/vfx-portal/vfx-portal.html:460`

#### ENG-186 · نموذج التركيب: HTML يتحول إلى فيديو · HTML-to-video composition model · 📦 بأمر تثبيت
- **ماذا / what:** A video is one HTML file whose DOM carries timing in data-* attributes, animated by a seekable runtime; headless Chrome seeks every frame and FFmpeg encodes, so identical input gives identical frames.
- **كيف / how:** Write index.html with a root <div data-composition-id data-width data-height data-duration>, timed children with class="clip" + data-start/data-duration/data-track-index, one paused GSAP timeline on window.__timelines[id]; preview with `npx hyperframes preview`, render with `npx hyperframes render`.
- **أرقام / params:** Node.js >=22 + FFmpeg; canvases 1920x1080 / 1080x1920 / 1080x1080; GSAP 3.14.2 CDN in templates
- **تثبيت / install:** `npx hyperframes preview`, render with `npx hyperframes render``
- **الدليل / proof:** `kosif-one/vendor/hyperframes/README.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-core/SKILL.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/minimal-composition.md`

#### ENG-187 · حلقة الإنتاج كمخطط اعتمادات · Production loop as dependency graph · 📦 بأمر تثبيت
- **ماذا / what:** Stages: blocks & assets (install registry once before parallel work), audio (voice + word timings + BGM + SFX -> audio_meta.json, carve the bed under voice), frames, duration sync (real voice length wins), assembly, transitions, captions, verify (lint + check + snapshot contact sheet), deliver (fina…
- **كيف / how:** production-loop.md; fire every external generation concurrently/in background; batch visual checks into one contact sheet (images re-price context).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/production-loop.md`

#### ENG-188 · عمّال الإطارات المتوازيون · Parallel frame workers (subagent dispatch) · 📦 بأمر تثبيت
- **ماذا / what:** Each scene is authored by a sub-agent from a packet (frame block + inlined blueprint + rule recipes + frame.md) into compositions/frames/NN-*.html; orchestrator lints the assembled project and re-dispatches failures.
- **كيف / how:** subagent-dispatch.md concurrency cap -> batching; frame-worker-core.md contract: <template>-wrapped root, one paused timeline at window.__timelines[frame_id], ids prefixed with frame_id, self-check codes.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/subagent-dispatch.md` · `kosif-one/vendor/hyperframes/skills/hyperframes/references/frame-worker-core.md`

#### ENG-189 · محرر المعاينة Studio وتطبيق سطح المكتب · Studio preview editor + desktop app handoff · 📦 بأمر تثبيت
- **ماذا / what:** The Studio preview is a full browser editor (click to edit, drag/trim clips, export); the desktop app's assistant 'Framey' edits by chat and drawing on frames; after returning, `hyperframes catch-up` lists what changed.
- **كيف / how:** Open preview before delivery render (`npx hyperframes preview --background`); after render mention the desktop-app line; run `npx hyperframes catch-up [dir]` when the user returns.
- **تثبيت / install:** `npx hyperframes preview --background`)`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/SKILL.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-studio/SKILL.md`

#### ENG-190 · عقد جذر التركيب · Composition root contract · 📦 بأمر تثبيت
- **ماذا / what:** Root div sized width/height 100% with data-composition-id, data-width, data-height, data-duration (read once at compile time = render length), optional data-fps; standalone root sits in <body> without <template>.
- **كيف / how:** Write per minimal-composition.md; never hardcode 1920px on #root; length comes from root data-duration not timeline length.
- **أرقام / params:** data-fps optional; render length fixed at compile time
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/data-attributes.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/minimal-composition.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-core/SKILL.md`

#### ENG-191 · سمات المقاطع والمسارات · Clip attributes and tracks · 📦 بأمر تثبيت
- **ماذا / what:** class="clip" + data-start/data-duration mark timed elements; data-track-index is only a Studio lane (render ignores it, clips may overlap); img defaults 3 s; video/audio default to source length; data-media-start offsets source; data-volume 0..3.98 (+12 dB); data-has-audio keeps footage sound; data-…
- **كيف / how:** Author clips per data-attributes.md and tracks-and-clips.md; extend root duration when a clip ends past it (lint clip_ends_past_root_duration).
- **أرقام / params:** img default 3s; volume max 3.98 (+12 dB)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/data-attributes.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/tracks-and-clips.md`

#### ENG-192 · التركيبات الفرعية داخل template · Sub-compositions with <template> · 📦 بأمر تثبيت
- **ماذا / what:** Scenes live in separate files loaded via data-composition-src; the file is one <template> whose root carries data-composition-id; style/script must be inside the template (head is dropped); style root via #root never a class.
- **كيف / how:** Host: <div data-composition-id=x data-composition-src=compositions/x.html data-start data-duration>; per-instance data-variable-values JSON; host duration = visible window.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/sub-compositions.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/composition-patterns.md`

#### ENG-193 · متغيرات التركيب وربط البيانات · Composition variables and data binding · 📦 بأمر تثبيت
- **ماذا / what:** Declared variables (data-composition-variables JSON on <html>) let one template render many variants; data-var-text binds text, data-var-src binds media src; CLI --variables overrides.
- **كيف / how:** variables-and-media.md: declare array of {id,type,default}; per-instance data-variable-values; batch render via CSV (see CLI).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/variables-and-media.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/data-attributes.md`

#### ENG-194 · تركيبات بـ Tailwind v4 · Tailwind v4 compositions · 📦 بأمر تثبيت
- **ماذا / what:** `init --tailwind` projects use the Tailwind v4 browser runtime; dynamic class safety and a render-proof that frame 0 does not flash unstyled.
- **كيف / how:** tailwind.md: v4 runtime rules, composition pattern, guardrails, validate frame 0 in render.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/tailwind.md`

#### ENG-195 · قواعد التحويلات والأداء · GSAP transforms and performance rules · 📦 بأمر تثبيت
- **ماذا / what:** Use x/y/scale/rotation aliases, never width/height/top/left for motion; will-change sparingly; stagger beats N tweens; precompute layout constants instead of getBoundingClientRect at tween time.
- **كيف / how:** adapters/gsap-transforms-and-perf.md.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/gsap-transforms-and-perf.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/SKILL.md`

#### ENG-196 · محول Anime.js · Anime.js adapter · 📦 بأمر تثبيت
- **ماذا / what:** Lightweight Anime.js v4 timelines registered on window.__hfAnime for seeking.
- **كيف / how:** adapters/animejs.md loading v4, timeline pattern, determinism.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/animejs.md`

#### ENG-197 · محول إطارات CSS · CSS keyframes adapter · 📦 بأمر تثبيت
- **ماذا / what:** CSS @keyframes become seekable via animation-delay/play-state/fill-mode control; good for shimmer and repeated motifs.
- **كيف / how:** adapters/css-animations.md basic + stagger patterns.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/css-animations.md`

#### ENG-198 · محول واجهة الحركة في المتصفح · Web Animations API adapter · 📦 بأمر تثبيت
- **ماذا / what:** element.animate() animations seeked via currentTime without a GSAP dependency.
- **كيف / how:** adapters/waapi.md.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/waapi.md`

#### ENG-199 · حلقة التطوير بأداة سطر الأوامر · HyperFrames CLI dev loop · 📦 بأمر تثبيت
- **ماذا / what:** init -> catalog search -> author -> lint -> check -> snapshot -> preview --background -> render (after approval) -> verify with ffprobe -> feedback.
- **كيف / how:** npx hyperframes init <p>; npx hyperframes lint; npx hyperframes check; npx hyperframes preview --background; npx hyperframes render --quality looks --output out.mp4; test -s out.mp4; ffprobe -v error -show_format -show_streams out.mp4.
- **تثبيت / install:** `npx hyperframes init <p>`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/SKILL.md`

#### ENG-200 · إنشاء مشروع بالأمثلة والوسائط · Scaffold project (init) with examples and media · 📦 بأمر تثبيت
- **ماذا / what:** Creates a project (centered blank or example template) optionally with a video/audio file auto-transcribed by Whisper, Tailwind v4, resolution presets.
- **كيف / how:** npx hyperframes init my-video [--example warm-grain|play-mode|swiss-grid|vignelli|decision-tree|kinetic-type|product-promo|nyt-graph] [--resolution portrait] [--video clip.mp4] [--audio track.mp3] [--tailwind] [--skip-transcribe] [--model --language].
- **أرقام / params:** resolutions landscape 1920x1080, portrait 1080x1920, square 1080x1080, -4k variants
- **تثبيت / install:** `npx hyperframes init my-video [--example warm-grain|play-mode|swiss-grid|vignelli|decision-tree|kinetic-type|product-promo|nyt-graph] [--resolution portrait] [--video clip`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/init-and-scaffold.md` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/init.ts`

#### ENG-201 · الفحص البيئي وإدارة المتصفح · Doctor and browser management · 📦 بأمر تثبيت
- **ماذا / what:** Environment check (Node, FFmpeg, Chrome) and pinned Chrome download/path/clear.
- **كيف / how:** npx hyperframes doctor --json | jq -e '.ok'; npx hyperframes browser ensure|path|clear.
- **تثبيت / install:** `npx hyperframes doctor --json | jq -e '`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/doctor-browser.md` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/doctor.ts`

#### ENG-202 · بحث دلالي محلي في الكتالوج · Offline semantic catalog search · 📦 بأمر تثبيت
- **ماذا / what:** Search the registry by plain-English description of a beat; local word tier or optional on-device ONNX embedding tier; query in English even for non-English videos; report misses.
- **كيف / how:** npx hyperframes catalog --query 'reveal ...' [--json]; optional ~33 MB bge-small-en-v1.5 ONNX download cached in ~/.hyperframes/; npx hyperframes feedback --search-miss.
- **أرقام / params:** ~33 MB model
- **تثبيت / install:** `npx hyperframes catalog --query 'reveal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/SKILL.md` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/catalog.ts`

#### ENG-203 · أوامر مساعدة متنوعة · Info / upgrade / compositions / docs / benchmark / clean · 📦 بأمر تثبيت
- **ماذا / what:** Project metadata, version check, list compositions, docs, render benchmark, cache cleanup.
- **كيف / how:** npx hyperframes info --json; upgrade --check --json; compositions; docs; benchmark; clean --dry-run.
- **تثبيت / install:** `npx hyperframes info --json`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/upgrade-info-misc.md`

#### ENG-204 · تنظيم المسارات حسب النوع · Studio layout conventions (tracks by kind, one caption track) · 📦 بأمر تثبيت
- **ماذا / what:** Every scene is a sub-composition; one caption track; one element kind per track via data-track-kind video/graphics/captions/audio.
- **كيف / how:** hyperframes-studio SKILL §1-3.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-studio/SKILL.md`

#### ENG-205 · مكتبة الكتل والمكونات الجاهزة · Registry blocks and components (hyperframes add) · 📦 بأمر تثبيت
- **ماذا / what:** Installable catalog: blocks are standalone sub-compositions (charts, maps, device mockups, shaders, lower thirds, social cards, carousels), components are paste-in effect snippets; search before hand-building any named look.
- **كيف / how:** npx hyperframes add <name|tag> [--dir .] [--json] [--no-clipboard]; blocks -> compositions/<name>.html wired via data-composition-src; components -> compositions/components/<name>.html pasted into host.
- **أرقام / params:** registry.json: 170 blocks, 222 components, 8 examples (folders: 210 blocks, 236 components)
- **تثبيت / install:** `npx hyperframes add <name|tag> [--dir`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-registry/SKILL.md` · `kosif-one/vendor/hyperframes/registry/registry.json` · `kosif-one/vendor/hyperframes/skills/hyperframes-registry/references/wiring-blocks.md`

#### ENG-206 · التصيير ثم تركيب القناع · Render + matte overlay composite · 📦 بأمر تثبيت
- **ماذا / what:** hyperframes render of the caption layer then FFmpeg overlay of the subject matte to put embed words behind the speaker -> final.mp4.
- **كيف / how:** bash scripts/render-and-composite.sh <project>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/render-and-composite.sh`

#### ENG-207 · مجمّع الفهرس وحاقن الانتقالات · Index assembler and transition injector · 📦 بأمر تثبيت
- **ماذا / what:** Assembles frames as sub-compositions on tracks into index.html and injects/verifies registry transitions at boundaries.
- **كيف / how:** node assemble-index.mjs --storyboard STORYBOARD.md --hyperframes .; node transitions.mjs inject|verify.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/faceless-explainer/scripts/assemble-index.mjs` · `kosif-one/vendor/hyperframes/skills/faceless-explainer/scripts/transitions.mjs` · `kosif-one/vendor/hyperframes/skills/faceless-explainer/scripts/transitions.test.mjs`

#### ENG-208 · تحويل مشاريع Remotion · Remotion to HyperFrames port · 📦 بأمر تثبيت
- **ماذا / what:** One-way translation of a Remotion React composition: lint the source for blockers (useState, useEffect deps, async metadata, third-party React, Lambda config, custom hooks), plan, generate HTML, validate with render diff and frame strips, document gaps; refuse + interop when blocked.
- **كيف / how:** python lint_source.py <remotion-src> [--json]; API map: <Composition> -> root data-*; <Sequence from durationInFrames> -> sub-comp host data-start=F/fps; interpolate -> fromTo ease none; spring -> back.out(N); Easing.bezier -> CustomEase; scripts/render_diff.sh, frame_strip.sh; 4-tier test corpus.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/remotion-to-hyperframes/SKILL.md` · `kosif-one/vendor/hyperframes/skills/remotion-to-hyperframes/references/api-map.md` · `kosif-one/vendor/hyperframes/skills/remotion-to-hyperframes/scripts/lint_source.py`

#### ENG-209 · تجهيز بيئة claude.ai · Cloud sandbox setup · 📦 بأمر تثبيت
- **ماذا / what:** Make a writable home ~/kosif-motion, fetch ffmpeg via imageio-ffmpeg and an ffprobe shim so kmotion runs without a PC.
- **كيف / how:** python scripts/cloud_setup.py --install [--browser]; all calls via kmotion.py
- **أرقام / params:** uploads /mnt/user-data/uploads, outputs /mnt/user-data/outputs
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:16` · `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### ENG-210 · عقد تركيب HyperFrames · HyperFrames HTML composition contract · 📦 بأمر تثبيت
- **ماذا / what:** Root div with data-composition-id/width/height/start/duration/fps; clip class on timed elements; media need id; nested compositions via data-composition-src; variables via data-composition-variables.
- **كيف / how:** Write index.html per contract; npx hyperframes check/snapshot/render or kmotion studio engine
- **أرقام / params:** render -q draft|looks(CRF16)|delivery; --resolution 4k
- **تثبيت / install:** `npx hyperframes check/snapshot/render or kmotion studio engine render -q draft|looks(CRF16)|delivery`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### ENG-211 · مشروع موشن ثنائي الأبعاد · New flat 2D project (GSAP+motion-kit) · 📦 بأمر تثبيت
- **ماذا / what:** Scaffold an HTML+GSAP composition with the motion kit.
- **كيف / how:** python scripts/kmotion.py new NAME --seconds 10 [--fps --size --title]
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:84`

#### ENG-212 · مشروع كانفس · New canvas project · 📦 بأمر تثبيت
- **ماذا / what:** One page with window.seek(t) canvas drawing.
- **كيف / how:** python scripts/kmotion.py new NAME --canvas --seconds 10
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:86`

#### ENG-213 · معاينة مسودة · Draft preview render · 📦 بأمر تثبيت
- **ماذا / what:** Half-size 15 fps ultrafast draft ~10x faster than master, same composition.
- **كيف / how:** python scripts/kmotion.py preview projects/NAME (render --draft)
- **أرقام / params:** 0.5 scale, 15 fps; 6 s demo 11 s vs 34 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:53` · `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### ENG-214 · المصيّر المتوازي · Parallel studio renderer · 📦 بأمر تثبيت
- **ماذا / what:** Splits frames into contiguous chunks on N browser pages, each encodes H.264 segment, lossless concat.
- **كيف / how:** python scripts/kmotion.py render projects/NAME --engine studio --workers N --capture png|jpeg --preset --crf --force
- **أرقام / params:** auto ≥20 frames/page, ≤6 pages, cores/2 on software GL; KOSIF_WORKERS
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:289` · `100-superskills/skills/kosif-montage-motion/UPGRADE_REPORT.md`

#### ENG-215 · التقاط سريع عبر CDP · CDP optimizeForSpeed capture · 📦 بأمر تثبيت
- **ماذا / what:** Page.captureScreenshot with optimizeForSpeed; PNG piped undecoded to FFmpeg; GPU process off for DOM pages (2x).
- **كيف / how:** automatic in film.py/html_render; KOSIF_GPU=0|1 override
- **أرقام / params:** v3.4 96 s → v4 34 s (1 browser), 22 s (2)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### ENG-216 · كاش بصمة التصيير · Fingerprint render cache · 📦 بأمر تثبيت
- **ماذا / what:** Unchanged sources+params serve the prior master instantly.
- **كيف / how:** automatic; --force to redo
- **أرقام / params:** 96 s → 0.05 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### ENG-217 · تمويه الحركة · Motion blur render pass · 📦 بأمر تثبيت
- **ماذا / what:** Sub-frames centred on the frame averaged in float, quantised once; 3D accumulates on GPU (window.__nativeBlur).
- **كيف / how:** python scripts/kmotion.py render --blur 4
- **أرقام / params:** blur 2–16 subframes
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### ENG-218 · التصيير النهائي عالي الجودة · Quality-first final render · 📦 بأمر تثبيت
- **ماذا / what:** Lossless PNG capture, libx264 slow CRF 16, short side ≥1080, poster baked, gate run.
- **كيف / how:** python scripts/kmotion.py final PROJECT [--blur N]
- **أرقام / params:** 5 s 3D boat 1080p: draft 28 s, final 173 s with 4x blur
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:465`

#### ENG-219 · استوديو الويب المحلي · KOSIF Motion Web local studio · 📦 بأمر تثبيت
- **ماذا / what:** Starlette site on 127.0.0.1:8766 with media, recipes, projects, timeline, jobs, Workbench, Claude, env tabs; MCP /mcp with 14 studio tools; cross-origin guard.
- **كيف / how:** python scripts/kmotion.py web; claude mcp add --transport http kosif-web http://127.0.0.1:8766/mcp
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:349` · `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### ENG-220 · محرر المتصفح بتصدير دقيق · Browser Studio frame-accurate MP4 · 📦 بأمر تثبيت
- **ماذا / what:** Browser montage editor; offline export via WebCodecs H.264 + AAC, mp4-muxer, BS.1770-4 meter to −14 LUFS under −1.5 dBFS peak.
- **كيف / how:** /studio/ «تصدير MP4 دقيق»; build_studio_cloud.py for claude.ai artifact
- **أرقام / params:** caps 60 s / 24 scenes; hard cuts only
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:398` · `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### ENG-221 · عقد التركيب القابل للتقديم إطاراً بإطار · Seekable HTML composition contract · 📦 بأمر تثبيت
- **ماذا / what:** Every project is one HTML page whose #root declares size, fps and duration and whose paused GSAP timeline is registered globally so any frame can be rendered by time, in any order.
- **كيف / how:** Write <div id=root data-composition-id=root data-width data-height data-start=0 data-duration data-fps>; build gsap.timeline({paused:true}); assign window.__timelines['root']=tl; call MOTION.shim('root', seconds) which exposes window.render(t)/window.__kosifSeek; renderers (kmotion render --engine studio, HyperFrames) seek t and wait for window.__ready.
- **أرقام / params:** data-fps 24/30/60; tl.set({}, {}, 5) pins the end; double requestAnimationFrame before __ready=true
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:33` · `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:86` · `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:88`

#### ENG-222 · مشهد ثلاثي الأبعاد مع طبقة نصوص على ساعة واحدة · Three.js scene + DOM overlay on one clock · 📦 بأمر تثبيت
- **ماذا / what:** A WebGL canvas scene and HTML/CSS typography overlay share the same t: the overlay timeline is sought first, then the 3D frame is drawn, and the first frame waits for fonts and any async textures.
- **كيف / how:** src/main.js exports build(canvas,W,H) returning {render(t), ready:Promise}; index.html sets window.render=(t)=>{seek(t); three.render(t); 2×rAF → __ready}; Promise.all([document.fonts.ready, three.ready]) before frame 0.
- **أرقام / params:** canvas 1920×1080 or 1080×1920; ready waits for spectrogram image upload in sound_ground
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/index.html:41` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/index.html:48` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:43`

#### ENG-223 · تصدير إطارات SVG ثم ترميز MP4 · SVG frame export + ffmpeg encode · 📦 بأمر تثبيت
- **ماذا / what:** Node writes every frame as an SVG file, an external rasteriser (librsvg/Cairo) turns them into PNG and ffmpeg encodes H.264.
- **كيف / how:** node build.cjs → svg/0000.svg…0287.svg and a self-contained HTML player; rasterise; ffmpeg -framerate 24 -i frames/%04d.png -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart.
- **أرقام / params:** 288 frames, crf 18, yuv420p, faststart
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/build.cjs:3` · `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/README.txt:23`

#### ENG-224 · مسارات الصوت واللقطات معلنة داخل الصفحة · Audio and footage tracks declared in markup · 📦 بأمر تثبيت
- **ماذا / what:** Voice, music, ambience and real video plates are declared as <audio>/<video> elements with start, duration, volume, role and fade-out; the renderer mixes the audio and the shim seeks each video to composition time.
- **كيف / how:** <audio data-start data-duration data-volume data-role=voice|music data-fade-out>; <video data-start data-duration muted playsinline> (prepared all-intra with kmotion footage); shim hides a video outside its span and waits for 'seeked'.
- **أرقام / params:** premium_edit: voice 1.0 + music 0.5 fade 0.4 s; night_boat ambience 1.0 fade 0.6 s; showreel pond.mp4 from 7.9 s for 4.9 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:42` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:45` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:49`

#### ENG-225 · تجميع مشهد ES-module بـ esbuild · ES-module scene bundling with esbuild · 📦 بأمر تثبيت
- **ماذا / what:** Scenes that import three-kit.js as ES modules (and JSON/PNG data) are bundled into one classic assets/main.bundle.js so the page loads from file://.
- **كيف / how:** npm install three@0.186.1 esbuild in scripts/; kmotion bundle projects/NAME (entry src/main.js → assets/main.bundle.js); kmotion kit-bundle after editing three-kit.js.
- **أرقام / params:** three 0.186.1, iife, es2020
- **تثبيت / install:** `npm install three@0`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:4` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:7` · `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/index.html:8`

#### ENG-226 · ضبابية حركة بإطارات فرعية وتعريض طويل · Sub-frame motion blur and long-exposure stacking · 📦 بأمر تثبيت
- **ماذا / what:** The WebGL frame loop accumulates several sub-frames per output frame (average for motion blur, MAX/'lighten' for a long exposure), so moving lights draw trails and stars draw arcs.
- **كيف / how:** makeFrameLoop(renderer, post, W, H, update) sets window.__nativeBlur; render with kmotion render --blur N --shutter S --stack lighten; trailLength(v) stretches a light by speed·(shutter/fps)/k so dots overlap into a continuous streak.
- **أرقام / params:** blue_hour: --blur 16 --shutter 30 --stack lighten; star pole 0.011 rad/s ≈ 0.6°/s; cars 22–27 m/s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:6` · `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:119` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:423`

#### ENG-227 · تصيير متوازٍ بمقاطع تُدمج بلا إعادة ترميز · Parallel chunked browser render joined without re-encode · 📦 بأمر تثبيت
- **ماذا / what:** film.film_animate renders chunks of a page in several browser pages, encodes each as its own H.264 segment and concatenates them losslessly; frames must stay complete and in order.
- **كيف / how:** film.film_animate(page, out, fps=30, seconds=2, size, workers=2); film.auto_workers(frames) → 1 for 10 frames, ≤6 for 600.
- **أرقام / params:** test: 60 frames, luminance monotonic across the join
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_fast_render.py:29` · `100-superskills/skills/kosif-montage-motion/tests/test_fast_render.py:38`

#### ENG-228 · وصفة مشروع المختبر · Lab project recipe (new → score → frames → render → inspect) · 📦 بأمر تثبيت
- **ماذا / what:** A documented five-command loop for a 3D lab film: scaffold, synthesise the score with cues, pull review stills at chosen times, render with workers, inspect the MP4.
- **كيف / how:** kmotion new NAME --lab --seconds 20 --fps 24 --size 960x540 --title …; kmotion score out.wav --spec score.json --cues cues.json; kmotion frames projects/NAME --times 1,4.5,8,11,14.5,17,19.5; kmotion render … --engine studio --workers 2; kmotion inspect out.mp4.
- **أرقام / params:** ≈2 s/frame on software GL; ≈8 min with 2 workers (per SKILL.md)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/README.md:3`

#### ENG-229 · فيلم ثنائي الأبعاد بلا متصفح · Browser-free 2D workbench film · 📦 بأمر تثبيت
- **ماذا / what:** On a sandbox with no browser, a 2D motion film is made from a task through plan → manifest → Pillow frames → FFmpeg MP4.
- **كيف / how:** kmotion setup (writable home, ffmpeg via imageio-ffmpeg, ffprobe stand-in, examples incl. midnight_cat) then kmotion workbench 'TOPIC' --aspect 9:16 --seconds 2 --fps 24 --titles 'أ|ب|ج|د|هـ' --out wb.mp4 → 1080×1920, 48 frames.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_cloud.py:65`

#### ENG-230 · قواعد عقد التصيير · HyperFrames render-contract lints · 📦 بأمر تثبيت
- **ماذا / what:** No CSS transform on GSAP-tweened nodes, fromTo initial states, x/y/scale/rotation only, no visibility tween on .clip, audio needs id, clip-path masks, no will-change, no getBoundingClientRect at tween time, no Math.random/clock/network, repeat:-1 only under finite duration.
- **كيف / how:** motion.py lint
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### ENG-231 · إعداد السحابة · Cloud setup on claude.ai · 📦 بأمر تثبيت
- **ماذا / what:** Install deps on claude.ai sandbox; no browser routes there.
- **كيف / how:** python scripts/cloud_setup.py --install
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/operating-manual.md` · `100-superskills/skills/kosif-montage-motion/scripts/cloud_setup.py` · `100-superskills/skills/kosif-montage-motion/tests/test_cloud.py`

#### ENG-232 · مشروع موشن جديد · New motion project 2D/3D · 📦 بأمر تثبيت
- **ماذا / what:** Scaffold HTML composition with three-kit/motion-kit/shape-kit.
- **كيف / how:** kmotion new NAME [--3d] | template; kmotion frames
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/operating-manual.md` · `100-superskills/skills/kosif-montage-motion/scripts/motion.py`

#### ENG-233 · الاستوديو المحلي · Local KOSIF Motion Web studio · 📦 بأمر تثبيت
- **ماذا / what:** Local Arabic RTL site with media, recipes, projects, timeline, jobs SSE, workbench, Claude tab.
- **كيف / how:** python scripts/kmotion.py web --port 8766
- **أرقام / params:** 9 offline tests
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/web-studio.md` · `100-superskills/skills/kosif-montage-motion/tests/test_web.py`

#### ENG-234 · MCP الاستوديو · kosif-web MCP · 📦 بأمر تثبيت
- **ماذا / what:** Claude Code drives local site tools.
- **كيف / how:** claude mcp add --transport http kosif-web http://127.0.0.1:8766/mcp; kosif_project_write, kosif_run, kosif_job, kosif_render_manifest, kosif_timeline_check
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/web-studio.md`

#### ENG-235 · تصدير MP4 دقيق · KOSIF Studio exact MP4 export · 📦 بأمر تثبيت
- **ماذا / what:** Offline WebCodecs + mp4-muxer export in browser, -14 LUFS; studio import to timeline.
- **كيف / how:** /studio/; POST /api/studio/import; build_studio_cloud.py --out studio-cloud.html
- **أرقام / params:** mp4-muxer@5.2.1
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/web-studio.md` · `100-superskills/skills/kosif-montage-motion/scripts/studio_import.py`

#### ENG-236 · تقسيم التصيير · Shard render · 📦 بأمر تثبيت
- **ماذا / what:** Split frame ranges across machines and join losslessly with gate.
- **كيف / how:** scripts/shard.py plan | render --shard i --of N | join
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/render-farm.md` · `100-superskills/skills/kosif-montage-motion/scripts/shard.py` · `100-superskills/skills/kosif-montage-motion/tests/test_fast_render.py`

#### ENG-237 · مواصفة الخط الزمني · JSON timeline spec · 📦 بأمر تثبيت
- **ماذا / what:** One JSON = whole edit (clips, overlays, audio) rendered by FFmpeg.
- **كيف / how:** kmotion timeline SPEC.json --out film.mp4 [--dry-run] [--example]
- **أرقام / params:** ratios 9:16,16:9,1:1,4:5,4:3,21:9
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py` · `100-superskills/skills/kosif-montage-motion/tests/test_v6.py`

#### ENG-238 · محرك خارجي: Editly · External engine: Editly · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-239 · محرك خارجي: FFCreator · External engine: FFCreator · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-240 · محرك خارجي: fframes (MIT) · External engine: fframes (MIT) · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-241 · محرك خارجي: Manim Community (MIT) · External engine: Manim Community (MIT) · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-242 · محرك خارجي: Motion Canvas · External engine: Motion Canvas · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-243 · محرك خارجي: MoviePy · External engine: MoviePy · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-244 · محرك خارجي: Remotion · External engine: Remotion · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-245 · محرك خارجي: Rendervid · External engine: Rendervid · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-246 · محرك خارجي: Revideo · External engine: Revideo · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-247 · محرك خارجي: VideoFlow (Apache-2.0) · External engine: VideoFlow (Apache-2.0) · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-248 · محرك خارجي: VideoRenderingEngine · External engine: VideoRenderingEngine · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-249 · محرك خارجي: VidPy · External engine: VidPy · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-250 · محرك خارجي: WebMotion (MIT) · External engine: WebMotion (MIT) · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-251 · محرك خارجي: Diffusion Studio Core · External engine: Diffusion Studio Core · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-252 · محرك خارجي: Etro (GPL-3.0) · External engine: Etro (GPL-3.0) · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-253 · محرك خارجي: Movie Masher (MPL-2.0) · External engine: Movie Masher (MPL-2.0) · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-254 · محرك خارجي: Twick · External engine: Twick · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-255 · محرك خارجي: WebAV · External engine: WebAV · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-256 · محرك خارجي: Creatomate · External engine: Creatomate · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-257 · محرك خارجي: iLoveVideoEditor · External engine: iLoveVideoEditor · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-258 · محرك خارجي: JSON2Video · External engine: JSON2Video · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-259 · محرك خارجي: Shotstack · External engine: Shotstack · 📦 بأمر تثبيت
- **ماذا / what:** Direct code/timeline video tool from the 500-tool HyperFrames catalog (link only, not installed).
- **كيف / how:** external
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-260 · مكتبات الحركة داخل الصفحة · In-page motion/drawing library list · 📦 بأمر تثبيت
- **ماذا / what:** ~110 libraries usable inside a HyperFrames page: canvas (Konva, p5, Two.js, Rough.js...), SVG draw-on (Vivus, Lazy Line Painter, Walkway), tweening (GSAP, Anime.js, Motion, Popmotion), CSS packs (Animate.css...), charts (D3, ECharts, Chart.js, Vega...), shaders (Hydra, KodeLife), 3D (Three, Babylon,…
- **كيف / how:** load via CDN in page
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

#### ENG-261 · تكامل: Remotion Agent Skills · Integration: Remotion Agent Skills · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### ENG-262 · تكامل: HyperFrames skills plugin · Integration: HyperFrames skills plugin · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### ENG-263 · تكامل: PixiJS + skills · Integration: PixiJS + skills · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### ENG-264 · مشروع موشن HTML · HTML motion project · 📦 بأمر تثبيت
- **ماذا / what:** HyperFrames/GSAP compositions, 3D three-kit, canvas, lab routes; motion blur sub-frames, shutter, lighten stacking.
- **كيف / how:** motion.py new|frames|check|render --engine auto --blur 4 --shutter 0.5 --stack lighten --draft
- **أرقام / params:** draft = half size 15fps
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/motion.py`

#### ENG-265 · تصيير HTML · Headless HTML frame render · 📦 بأمر تثبيت
- **ماذا / what:** Edge/Chrome seeks window.render(t) and captures PNG.
- **كيف / how:** html_render.py page out --size 1920x1080 --t 2
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/html_render.py`

#### ENG-266 · تقسيم التصيير · Render sharding · 📦 بأمر تثبيت
- **ماذا / what:** Split frame ranges across machines and join losslessly.
- **كيف / how:** shard.py plan|render --shard i --of 6|join
- **أرقام / params:** libx264 slow CRF 16
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/shard.py`

#### ENG-267 · التقاط الإطارات عبر متصفح Edge وكارت الشاشة · Playwright Edge D3D11 frame capture · 📦 بأمر تثبيت
- **ماذا / what:** Headless browser opens the project page, calls render(t) for each frame time and screenshots the exact viewport to numbered PNGs.
- **كيف / how:** python scripts/ultra_animator.py capture <project> --fps 30 [--limit N]; uses playwright.sync_api chromium.launch(channel='msedge', headless=True) with GPU flags, viewport = project width x height, device_scale_factor 1, saves frames/f_%04d.png, logs page errors.
- **أرقام / params:** flags --ignore-gpu-blocklist --use-angle=d3d11 --enable-zero-copy; viewport 1080x1920 default; frames = round(duration*fps); progress every 30 frames
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/ultra_animator.py:141` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/animation_craft.md`

#### ENG-268 · عرض حتمي render(t) والتقاط الإطارات · Deterministic render(t) + frame capture (WebGL) · 📦 بأمر تثبيت
- **ماذا / what:** The page exposes window.render(t) that draws the frame at time t without reading the wall clock, and sets window.__ready after fonts load; a headless browser steps t and screenshots every frame so preview and video match exactly.
- **كيف / how:** In page: ?capture=1 disables the RAF loop and scaling; Playwright (Edge channel, --ignore-gpu-blocklist --use-angle=d3d11) viewport 1080x1920, wait_for_function('window.__ready===true'), loop page.evaluate('window.render(t)') + screenshot clip; --only 0.5,3.5 for QA stills; collect pageerror/console errors; then ffmpeg -framerate 30 -i f_%04d.png.
- **أرقام / params:** fps 30, dur 18, device_scale_factor 1, preserveDrawingBuffer true
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html:457-477` · `kosif-one/projects/egypt-2120-animation/index.html:479-486` · `kosif-one/projects/egypt-2120-animation/capture.py`

#### ENG-269 · خط زمني JSON إلى فيلم · JSON timeline -> film (fadeblack, overlays, voice) · 📦 بأمر تثبيت
- **ماذا / what:** A declarative edit: clips with in/out/speed/fit/mute/colour match/transition, image and text overlays with timing, fades and position expressions, and an audio block (voice, music, duck, LUFS), rendered to MP4 with parallel workers.
- **كيف / how:** timeline.json {size,fps,background,clips[{src,in,out,speed,fit:'cover',mute,match,transition:{type:'fadeblack',dur}}],overlays[{type:'text',font,size,color,stroke,shadow,anim,fade_in,fade_out,x:'0.5000*W-w/2',y:'0.4750*H-h/2',nowrap}|{type:'image',src}],audio{voice{src,start},keep_clip_audio:false,duck:'none',lufs}}; raw output records actual transitions and workers 4.
- **أرقام / params:** 1080x1920, 30 fps, 28.234 s raw; text 135 px; fade_in .45 first then .383; fade_out .383
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/mimic-jumuah/study/mimic.timeline.json` · `kosif-one/projects/mimic-jumuah/جمعة-محاكاة.raw.timeline.json`

#### ENG-270 · هيكل تركيب HyperFrames · HyperFrames composition skeleton · 📦 بأمر تثبيت
- **ماذا / what:** A single HTML file is a renderable composition: a root div with id/size/duration/fps data attributes, media elements with data-start/duration/volume, one paused GSAP timeline registered in window.__timelines, and M.shim to expose render(t)/__ready for KOSIF Studio's renderer.
- **كيف / how:** <div id=root data-composition-id=root data-width=1080 data-height=1920 data-start=0 data-duration=T data-fps=30>; <audio data-start data-duration data-volume data-role>; const tl=gsap.timeline({paused:true}); window.__timelines.root=tl; M.shim('root',T).
- **أرقام / params:** 1080x1920, 30 fps; durations 24.7 s / 47.0 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html:35-36` · `kosif-one/projects/thursday-dua-animation/source/index.html:228-230` · `kosif-one/projects/whatsapp-motion/projects/success/index.html:47-49`

#### ENG-271 · قالب SVG حتمي بدوال مساعدة · SVG render(t) template with seg/fadeWin/mix helpers · 📦 بأمر تثبيت
- **ماذا / what:** A small dependency-free animation core: one function sets every SVG attribute for time t using segment, eased segment, windowed fade and hex colour mix helpers; preview loops with click-to-pause, capture mode lets a recorder call render(t).
- **كيف / how:** seg(t,a,b)=clamp((t-a)/(b-a)); ease = easeInOutCubic; fadeWin(t,a,b,f=.25)=min(seg(t,a,a+f),1-seg(t,b-f,b)); mix(c1,c2,p) hex lerp; ?capture adds body.capture fixed 1920x1080; window.__ready after document.fonts.ready.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/index.html:93-102` · `kosif-one/projects/water-cycle-animation/index.html:200-211`

#### ENG-272 · التقاط إطارات SVG إلى فيديو · SVG frame capture to MP4 (Playwright + ffmpeg) · 📦 بأمر تثبيت
- **ماذا / what:** Screenshots the SVG stage frame by frame and encodes a high-quality H.264 file; checks that the web font actually loaded.
- **كيف / how:** Playwright Edge channel, viewport 1920x1080, wait for __ready, document.fonts.check('700 54px Cairo'), loop render(i/30) + locator('#stage').screenshot; ffmpeg -framerate 30 -i f_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow -movflags +faststart.
- **أرقام / params:** 300 frames, CRF 18, preset slow
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/capture.py`

#### ENG-273 · عشوائية بذرية · Seeded RNG and hash (mulberry32) · 📦 بأمر تثبيت
- **ماذا / what:** Same seed gives the same film: all scatter, particles and jitter come from a seeded generator or an integer hash, never Math.random.
- **كيف / how:** M.rng(seed) mulberry32; M.hash(i,j) integer hash -> [0,1).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:119-123` · `kosif-one/projects/egypt-2120-animation/index.html:65-66`

#### ENG-274 · جسر العرض ومزامنة الفيديو · Renderer shim + footage seeking · 📦 بأمر تثبيت
- **ماذا / what:** Bridges a GSAP composition to a frame-exact renderer: render(t) pauses every registered timeline and CSS animation at t, seeks any <video data-start> clip and flags __ready only after all seeks and two animation frames.
- **كيف / how:** M.shim(rootId,duration): window.render, window.seek, window.__kosifSeek, window.__duration; waits for fonts and video loadeddata (15 s timeout), seek timeout 4 s.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:465-492`

#### ENG-275 · تصيير إلى MP4 · Render to MP4 (HyperFrames CLI or studio engine) · 📦 بأمر تثبيت
- **ماذا / what:** Seeks the composition frame by frame in a headless browser and encodes with FFmpeg; muxes <audio> clips and normalises the mix.
- **كيف / how:** python motion.py render PROJECT [--engine auto|hyperframes|studio] [--workers 0] [--draft] [--blur K --shutter S --stack average|lighten] [--capture jpeg] [--preset --crf]; preview = render --draft.
- **أرقام / params:** default 1080p30 'looks' quality; workers up to 4; draft = half size, 15 fps, ultrafast, JPEG; mix -14 LUFS / -1 dBTP
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/motion.py:474` · `kosif-one/tools/kosif-studio/film.py`

#### ENG-276 · تجميع المشروع بـ esbuild · esbuild bundling of 3D projects · 📦 بأمر تثبيت
- **ماذا / what:** Bundles src/main.js with three-kit into one IIFE so file:// renders work; inlines GLB/HDR/PNG/WAV as data URLs and JSON.
- **كيف / how:** python motion.py bundle PROJECT [--entry src/main.js --out assets/main.bundle.js]; kit-bundle rebuilds three-kit.bundle.js.
- **أرقام / params:** es2020, minified; loaders .glb .gltf .hdr .png .jpg .jpeg .webp .wav .bin=dataurl
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/motion.py:194` · `kosif-one/tools/kosif-studio/motion/motion.py:217` · `kosif-one/tools/kosif-studio/motion/package.json`

#### ENG-277 · صورة إلى برنامج بايثون · Image -> standalone Pillow program · 📦 بأمر تثبيت
- **ماذا / what:** Writes a Python program (Pillow only) whose readable draw.polygon calls plus embedded original bytes reproduce the image exactly and self-check.
- **كيف / how:** python studio.py --image-code photo.jpg [--data-only]; to_python.image_to_python.
- **أرقام / params:** verified on a 900x900 ad: 3,394 polygons, 0 differing pixels
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/to_python.py` · `kosif-one/tools/kosif-studio/README.md`

#### ENG-278 · باني النسخة المقلّدة · Mimic remake builder · 📦 بأمر تثبيت
- **ماذا / what:** Per-shot ffmpeg prep (trim, speed, CFR, fit, LUT) then one Python compositing pass piped to a single H.264 encode copying original audio; keeps frame count, fps, size.
- **كيف / how:** mm_build.build('work', preview=True) then full
- **أرقام / params:** crf 17 preset medium
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-mimic/scripts/mm_build.py:232`

#### ENG-279 · عقد المشهد الحتمي render(t) · Deterministic render(t) scene contract · 📦 بأمر تثبيت
- **ماذا / what:** Every visual is a pure function of time; page exposes window.render(t) and window.__ready after fonts load, so preview equals frames.
- **كيف / how:** Write index.html from templates/scene-2d.html; no Date.now/performance.now/unseeded Math.random; capture.py calls render(t) per frame.
- **أرقام / params:** 30 fps default; first motion at 0.1-0.3 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/references/motion-rules.md` · `100-superskills/skills/claude-animation-studio/templates/scene-2d.html`

#### ENG-280 · تصوير الإطارات بـ Playwright · Playwright frame capture · 📦 بأمر تثبيت
- **ماذا / what:** Screenshots each frame of an HTML scene at true pixel size, optional selector and spot times.
- **كيف / how:** python capture.py --html index.html [--w --h --fps --dur --only 1,4,7 --selector #stage]
- **أرقام / params:** demo: 180 frames 1080x1920 in 64.7 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/scripts/capture.py` · `100-superskills/examples/demo2d/capture.json`

#### ENG-281 · مسار Remotion · Remotion equivalent path · 📦 بأمر تثبيت
- **ماذا / what:** Same principles in React: useCurrentFrame as only clock, interpolate with clamp, spring(), Sequence per scene, npx remotion render.
- **أرقام / params:** extrapolateRight clamp
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/references/motion-rules.md`

#### ENG-282 · عدة KOSIF Motion فوق HyperFrames · KOSIF Motion kit on HyperFrames (delta) · 📦 بأمر تثبيت
- **ماذا / what:** Owner layer over vendored HyperFrames: motion.py CLI (new/frames/check/render/measure/lint/sheet/speed/study/channels/mocap/inspect), motion-kit.js helpers, three-kit.js realism, ambience/score/voice/montage scripts.
- **كيف / how:** See SKILL.md steps 4-26; covered in detail by another scope.
- **أرقام / params:** -14 LUFS, peak <=-1
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/hyperframes-animation-studio/SKILL.md`

#### ENG-283 · أوامر ffmpeg · ffmpeg cut/concat/burn/reframe · 📦 بأمر تثبيت
- **ماذا / what:** Commands for trimming, joining, burning subs, aspect change, output verification; H.264 yuv420p delivery.
- **كيف / how:** ffmpeg-commands.sh
- **أرقام / params:** -c:v libx264 -pix_fmt yuv420p
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/video-editing-captions/SKILL.md:25`

#### ENG-284 · جسر المحرّكين · Dual-renderer shim + footage seek · 📦 بأمر تثبيت
- **ماذا / what:** Makes one HTML file render under HyperFrames (window.__timelines) and KOSIF Studio (window.render(t)/__ready/seek), and seeks <video data-start> clips exactly.
- **كيف / how:** Register tl on window.__timelines['root'] literally, then MOTION.shim('root', seconds); MOTION.register(id, tl) helper.
- **أرقام / params:** waits fonts + video loadeddata (15 s cap) + seeked (4 s cap), two rAFs before __ready
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:466` · `kosif-studio/motion/templates/composition.html`

#### ENG-285 · حلقة الإطار مع تمويه الحركة · GPU motion-blur / long-exposure frame loop · 📦 بأمر تثبيت
- **ماذا / what:** render(t) that accumulates k sub-frames on the GPU in half float: average = motion blur, MaxEquation = lighten stack (light trails, star arcs).
- **كيف / how:** const render = K3.makeFrameLoop(renderer, post, W, H, update); renderer sets window.__blur, __shutter, __fps, __stack ('lighten').
- **أرقام / params:** shutter .5 default; motion.py render --blur 4; long exposure --blur 16 --shutter 30 --stack lighten (1 s per frame at 30 fps)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:423` · `kosif-studio/motion/references/book-lessons.md` · `kosif-studio/tests/test_studio.py:793`

#### ENG-286 · حزمة three-kit الجاهزة · Prebuilt three-kit bundle (window.K3) · 📦 بأمر تثبيت
- **ماذا / what:** three.js r186 + the whole kit as one classic script on window.K3 (plus K3.POST post classes), loadable from file:// with no npm.
- **كيف / how:** <script src='assets/three-kit.bundle.js'> then shape-kit.js / lab-kit.js; rebuild with python kmotion.py kit-bundle (needs three@0.186.1 + esbuild).
- **أرقام / params:** bundle 904,567 bytes
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/k3-entry.js` · `kosif-studio/motion/kit/three-kit.bundle.js`

#### ENG-287 · مسودة منخفضة الدقة · Draft scale for fast 3D drafts · 📦 بأمر تثبيت
- **ماذا / what:** When the renderer sets window.__draftScale, GL buffers shrink so 3D drafts really render faster.
- **كيف / how:** film.py --draft sets __draftScale; lab-kit wraps K3.makeRenderer.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/lab-kit.js:291`

#### ENG-288 · قالب الكانفاس · Canvas route template · 📦 بأمر تثبيت
- **ماذا / what:** One HTML file, one canvas, a pure function of t: window.seek(t) paints any frame; includes closed-form spring, track, expo-out, exit ease, seeded rng, 120 BPM clock, scene list.
- **كيف / how:** python3 motion.py new NAME --canvas (fills {{W}} {{H}} {{SECONDS}} {{FPS}} {{TITLE}}); render with motion.py render --engine studio [--blur 4].
- **أرقام / params:** spring k 170 d 26; out = 1-2^-10p; exit p^2.8; bg #111312; title 700 150px Segoe UI rtl; accent bar #e4342f
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/templates/canvas.html` · `kosif-studio/tests/test_studio.py:650`

#### ENG-289 · قالب تركيب HyperFrames · HyperFrames GSAP composition template · 📦 بأمر تثبيت
- **ماذا / what:** Default composition: data-* contract on #root, #cam stage, SVG scene gradient, title word reveal, sparkle, vignette .4, grain .06, camera push 1.06.
- **كيف / how:** python3 motion.py new NAME; edit timeline; npx hyperframes check/render or motion.py render.
- **أرقام / params:** bg gradient #1b2a49 -> #0d1b2a; title 110 px/800 Segoe UI; house rules: one carrier object, entrances from ≥ .35 stage width, ≤ 8 words, 2-3 camera moves
- **تثبيت / install:** `npx hyperframes check/render or motion`
- **الدليل / proof:** `kosif-studio/motion/templates/composition.html` · `kosif-studio/tests/test_studio.py:549`

#### ENG-290 · أوامر HyperFrames · HyperFrames CLI pipeline · 📦 بأمر تثبيت
- **ماذا / what:** Lint/validate, snapshot key frames, render at quality presets or 4k DPR upscale, environment doctor.
- **كيف / how:** npx hyperframes check DIR; snapshot DIR; render DIR -o out.mp4 -q draft|looks|delivery -f 30; --resolution 4k; doctor.
- **أرقام / params:** looks = CRF 16; env HYPERFRAMES_SKIP_SKILLS=1, PRODUCER_LOW_MEMORY_MODE=1 (8 GB), PUPPETEER_EXECUTABLE_PATH; call node node_modules/hyperframes/bin directly on non-ASCII paths
- **تثبيت / install:** `npx hyperframes check DIR`
- **الدليل / proof:** `kosif-studio/motion/references/hyperframes-authoring.md`

#### ENG-291 · مكتبات الحركة داخل الصفحة · In-page animation library list · 📦 بأمر تثبيت
- **ماذا / what:** ~110 libraries that run inside a HyperFrames page: canvas (Konva, p5, Two.js, Pts, Rough.js), SVG draw-on (Vivus, Walkway, Lazy Line Painter), tweens (Anime.js, mo.js, Popmotion), text (SplitType, Typed.js, CountUp), charts (ECharts, D3, Vega-Lite, Chart.js), 3D (Babylon, OGL, R3F), shaders (Hydra, …
- **كيف / how:** Vendor locally (no CDN at render), keep seekable.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/references/tools-catalog.md`

#### ENG-292 · برنامج الصورة: خطوات وعمليات متجهة · KOSIF picture program (Step/ops vector renderer) · 📦 بأمر تثبيت
- **ماذا / what:** A picture is an ordered list of Step objects, each holding vector ops (fill, glow, rim, relief, camera ops) drawn on a float RGB canvas; re-rendering at any scale keeps it sharp.
- **كيف / how:** Write a scene file with TITLE, optional ROLLOFF and def build() -> [Step(label, [ops], order, origin, weight)]; all render.py names are injected without import. Render headless: python studio.py <scene> --render out.png --scale 3.2, or R.render_image(steps, scale, ss, rolloff).
- **أرقام / params:** sheet 1200x800 scene units; scale 1.0=1200x800, 3.2=3840x2560; supersample ss=3 (ss=2 when scale>2); default paper #000000 (studio paper #f3eee4)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/render.py:1` · `kosif-studio/render.py:811` · `kosif-studio/render.py:828`

#### ENG-293 · نافذة الرسم بيكسلاً ببيكسل · Pixel-by-pixel painting window (KOSIF Studio) · 📦 بأمر تثبيت
- **ماذا / what:** A Tkinter desktop app that streams paint jobs from a producer thread and lays changed pixels down in painter order with a moving brush cursor, step labels and pixel counts in Arabic.
- **كيف / how:** python studio.py [scene] [--speed slow|normal|fast|instant]; producers: produce() for scenes, produce_exact() for images, produce_code() for runner subprocess; queue maxsize 6.
- **أرقام / params:** window bg #16141c; paper #f3eee4; brush ring 14 px white + 10 px dark; status in Segoe UI 11
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/studio.py:276` · `kosif-studio/studio.py:182` · `kosif-studio/studio.py:203`

#### ENG-294 · لوحة بدقتها الأصلية مع عرض ملائم · Native-resolution canvas with viewer-style fit · 📦 بأمر تثبيت
- **ماذا / what:** Images and raster code are painted on a canvas exactly their own size; the view shrinks with area averaging and enlarges small pictures by whole numbers so pixels stay square.
- **كيف / how:** set_native(w,h) builds an index map; refresh_native uses cv2 INTER_AREA (<1x), INTER_NEAREST (>=2x) or INTER_CUBIC; >4 MP pictures use nearest view while drawing.
- **أرقام / params:** integer zoom when fit factor >= 2; 4,000,000 px threshold; transparent pixels show paper #f3eee4
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/studio.py:458` · `kosif-studio/studio.py:471` · `kosif-studio/runner.py:203`

#### ENG-295 · مشغّل كود أي ذكاء اصطناعي · Any-AI code runner (SVG / scene / PIL / matplotlib / turtle / HTML / image code) · 📦 بأمر تثبيت
- **ماذا / what:** Runs pasted picture code in its own process, detects its kind and turns the result into ordered paint jobs (npz + json) that the studio or film plays.
- **كيف / how:** python runner.py CODE_FILE OUT_DIR [--scale s] [--export PNG]; kind_of() -> image|html|svg|scene|python; writes job_####.npz/json, canvas.json, final.png, done.json or error.txt.
- **أرقام / params:** jobs written atomically (tmp + os.replace); scene ROLLOFF default 0.82; export at --scale 3.2 for 4K
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/runner.py:1` · `kosif-studio/runner.py:45` · `kosif-studio/runner.py:451`

#### ENG-296 · التقاط رسوم matplotlib وturtle · matplotlib and turtle capture · 📦 بأمر تثبيت
- **ماذا / what:** Code that plots with matplotlib is run on the Agg backend and its last figure saved; turtle drawings are captured from the screen after tracer(0,0); both are then painted in brush strokes.
- **كيف / how:** run_python(): plt.show patched to collect figures, savefig dpi 110 bbox tight; turtle mainloop/done/exitonclick no-oped, ImageGrab of the canvas.
- **أرقام / params:** dpi 110; turtle window appears briefly (documented limit)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/runner.py:359` · `kosif-studio/runner.py:425` · `kosif-studio/runner.py:439`

#### ENG-297 · صفحة HTML/Three.js إلى إطار حتمي · HTML / Three.js page to one deterministic frame · 📦 بأمر تثبيت
- **ماذا / what:** Renders a web page (WebGL, CSS, canvas) in headless Edge/Chrome after it signals readiness, optionally seeking a time; the frame is then painted pixel by pixel and can become Python code.
- **كيف / how:** python html_render.py page.html out.png [--size 1920x1080] [--t 2.5] [--scale 1]; Playwright path waits for window.__ready and calls window.render(t); fallback is the browser's --screenshot with --virtual-time-budget=30000 (no seek).
- **أرقام / params:** default 1920x1080; studio uses 1200x800; timeout 90 s; Windows GPU flags --use-angle=d3d11; elsewhere SwiftShader; measured 142 ms (GPU) vs 4335 ms (SwiftShader) per 1080p raymarch frame
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/html_render.py:1` · `kosif-studio/html_render.py:87` · `kosif-studio/html_render.py:21`

#### ENG-298 · تصيير صفحة قابلة للتقديم إلى فيديو · Seekable page animation renderer (render(t)/seek(t) -> MP4) · 📦 بأمر تثبيت
- **ماذا / what:** Renders time-driven HTML compositions frame by frame through headless Chromium and FFmpeg; scenes can also animate by defining build_t(t).
- **كيف / how:** python film.py animate page.html --out x.mp4 [--fps 30] [--seconds s] [--workers n] [--capture png|jpeg] [--preset] [--crf]; contract window.__ready, window.render(t) or window.seek(t), window.__duration.
- **أرقام / params:** default size 1280x720, fps 30, duration from __duration (fallback 4 s), page budget KOSIF_PAGE_TIMEOUT 600 s, 4 retries per frame
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/film.py:148` · `kosif-studio/film.py:239` · `kosif-studio/film.py:353`

#### ENG-299 · عمّال تصيير متوازون ودمج بلا فقد · Parallel browser render workers with lossless concat · 📦 بأمر تثبيت
- **ماذا / what:** Splits a timeline across several headless browsers (one process each), each encoding its own segment, then concatenates the MP4 segments without re-encoding.
- **كيف / how:** film.py _chunk subprocesses + ffmpeg -f concat -c copy; worker count from cores, frames and free memory; KOSIF_WORKERS overrides.
- **أرقام / params:** at most 6 workers, >= 20 frames per worker, 1 page per 2 cores on SwiftShader, memory budget 0.45 GB + 0.25 GB per megapixel with 2 GB headroom
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/film.py:186` · `kosif-studio/film.py:214` · `kosif-studio/film.py:343`

#### ENG-300 · التقاط سريع للإطارات عبر DevTools · Fast frame capture via DevTools · 📦 بأمر تثبيت
- **ماذا / what:** Grabs page pixels with CDP Page.captureScreenshot optimizeForSpeed (fast zlib PNG, or JPEG q95 for drafts) and pipes PNG bytes straight to FFmpeg when no blending is needed.
- **كيف / how:** _grabber(pg, capture) with fallback to Playwright screenshot; _decode uses cv2.imdecode; direct path uses ffmpeg image2pipe.
- **أرقام / params:** PNG lossless or JPEG quality 95 (about 2x faster)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/film.py:154` · `kosif-studio/film.py:167` · `kosif-studio/film.py:273`

#### ENG-301 · تحريك المشهد عبر build_t(t) · Scene animation through build_t(t) · 📦 بأمر تثبيت
- **ماذا / what:** A KOSIF scene becomes an animation by defining build_t(t) that returns steps for time t; each frame is a full re-render.
- **كيف / how:** film.py animate scene.py: imports the module, renders R.render_image(build_t(i/fps)) per frame into the Encoder.
- **أرقام / params:** DURATION default 4.0 s; 1200x800 frames
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/film.py:408`

#### ENG-302 · أوامر الاستوديو من سطر الأوامر · Studio command-line modes · 📦 بأمر تثبيت
- **ماذا / what:** Headless entry points for rendering scenes, tracing images, writing image programs and opening code or images in the window.
- **كيف / how:** python studio.py <scene> --render out.png --scale 3.2 | --trace IMG [--name --title] | --image-code IMG [--data-only] | --code FILE | --image IMG | --speed slow|normal|fast|instant
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/studio.py:1349`

#### ENG-303 · قائمة الأنيميشن في الاستوديو · Studio animation menu bridging to KOSIF Motion · 📦 بأمر تثبيت
- **ماذا / what:** The drawing window's Animation menu launches the motion pipeline: new 2D/3D project, key frame drawn in the studio, render with optional sub-frame blur, lint, critique sheet, optical-flow speed, beat grid, reference-film study, talking-clip auto reel, burned-caption removal and transcription.
- **كيف / how:** Calls motion/motion.py (new, bundle, frames, render --engine studio --blur, lint, sheet, speed, beats, study) and motion/kmotion.py (reel, decaption, transcribe) in threads or consoles.
- **أرقام / params:** blur 1..8 sub-frames (4 = cinematic); default new project 8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/studio.py:333` · `kosif-studio/studio.py:965` · `kosif-studio/studio.py:997`

#### ENG-304 · عقد الصفحة القابلة للتقديم · Seekable HTML page contract · 📦 بأمر تثبيت
- **ماذا / what:** Any page rendered by the studio sets window.__ready = true when a frame is fully drawn, exposes window.render(t) (or window.seek(t)) and window.__duration in seconds; no wall-clock animation.
- **كيف / how:** Implement in the page; html_render.render_html and film.film_animate wait on __ready after every seek.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/html_render.py:1` · `kosif-studio/film.py:148` · `kosif-studio/scenes/whale_dragon_3d.html:272`

#### ENG-305 · التصيير بمحركين · Dual-engine renderer (HyperFrames CLI or studio browser renderer) · 📦 بأمر تثبيت
- **ماذا / what:** Renders a composition to MP4 either through the HyperFrames node CLI or through KOSIF Studio's own Playwright frame renderer (film.film_animate), with the composition's <audio> clips mixed afterwards.
- **كيف / how:** python motion.py render PROJECT --engine auto|hyperframes|studio [--quality looks] [--fps N] [--out X.mp4]; auto picks HyperFrames when node_modules/hyperframes exists.
- **أرقام / params:** env HYPERFRAMES_SKIP_SKILLS=1, PRODUCER_LOW_MEMORY_MODE=1; studio defaults capture png, libx264 preset medium crf 18
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/motion.py:292` · `kosif-studio/motion/motion.py:64`

#### ENG-306 · مسودة معاينة سريعة · Draft preview cut · 📦 بأمر تثبيت
- **ماذا / what:** A review render at half the pixels and 15 fps, JPEG frame capture and ultrafast encoding, always through the studio engine.
- **كيف / how:** python motion.py preview PROJECT (= render --draft) → out/NAME.draft.mp4
- **أرقام / params:** scale 0.5, fps 15, preset ultrafast, crf 23, capture jpeg, blur 1
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/motion.py:304` · `kosif-studio/motion/motion.py:584`

#### ENG-307 · ضبابية الحركة والتعريض الطويل · Sub-frame motion blur and long exposure · 📦 بأمر تثبيت
- **ماذا / what:** Each output frame stacks N sub-frames over an exposure window; averaging gives cinematic motion blur, lightening gives star trails and light painting.
- **كيف / how:** python motion.py render P --engine studio --blur 8 --shutter 0.5 [--stack lighten]; blue_hour uses --blur 16 --shutter 30 --stack lighten for a 1 s exposure at 30 fps.
- **أرقام / params:** --blur 1..16 (sub-frames), --shutter 0.5 = 180°, 30 = 1 s at 30 fps; --stack average|lighten; speed check suggests up to 8 samples
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/motion.py:476` · `kosif-studio/motion/projects/blue_hour/src/main.js:1` · `kosif-studio/tests/test_studio.py:793`

#### ENG-308 · تصيير متوازٍ بعدة متصفحات · Parallel browser workers · 📦 بأمر تثبيت
- **ماذا / what:** Frames render in several headless browsers at once because every frame is a pure function of t.
- **كيف / how:** render --workers N (0 = one per core, capped at 4); batch jobs set KOSIF_WORKERS=1.
- **أرقام / params:** workers 0..4
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/motion.py:479` · `kosif-studio/motion/env_check.py:116`

#### ENG-309 · تجميع المشهد بـ esbuild · esbuild scene bundling · 📦 بأمر تثبيت
- **ماذا / what:** Turns an ES-module Three.js scene into one classic script that loads from file:// with assets inlined, so no dev server or CORS is needed.
- **كيف / how:** python motion.py bundle PROJECT [--entry src/main.js --out assets/main.bundle.js]; motion.py kit-bundle rebuilds kit/three-kit.bundle.js (window.K3).
- **أرقام / params:** --bundle --format=iife --minify --target=es2020; dataurl loaders .glb .gltf .hdr .png .jpg .jpeg .webp .wav .bin; json loader
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/motion.py:185` · `kosif-studio/motion/motion.py:204` · `kosif-studio/tests/test_studio.py:606`

#### ENG-310 · رندر HTML حتمي · HTML seek renderer · 📦 بأمر تثبيت
- **ماذا / what:** Renders an HTML/Canvas/SVG page exposing window.__kosif.seek(t) to MP4 frame-exactly.
- **كيف / how:** node tools/render_html.cjs --in film.html --out film.mp4 [--preview for 8-frame contact sheet]; Playwright + ffmpeg.
- **أرقام / params:** libx264 yuv420p crf 18 preset slow +faststart; AAC 48kHz 192k
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/tools/render_html.cjs` · `kosif-tool/tools/render_html.md` · `kosif-tool/playbooks/render-pipeline.md`

#### ENG-311 · قواعد الحتمية · Determinism rules · 📦 بأمر تثبيت
- **ماذا / what:** Frame is a pure function of time.
- **كيف / how:** Seeded RNG, no Math.random/Date.now, fonts ready via window.__kosifReady, no network at render.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/render-pipeline.md` · `kosif-tool/playbooks/code.md`

#### ENG-312 · تركيبة KosifFilm في Remotion · Remotion KosifFilm composition · 📦 بأمر تثبيت
- **ماذا / what:** Remotion v4 composition 1080x1920, 30 fps, 12 s with props title/words/accent/lang; three Sequences (title 34%, chart 40%, logo rest) inside a CameraRig plus a captions layer.
- **كيف / how:** cd starters/remotion && npm install && npm run preview|render|still|typecheck; npx remotion render KosifFilm out/film.mp4 --props=./props.example.json
- **أرقام / params:** remotion 4.0.535, react 19.3.1, jpeg frames, overwrite on
- **تثبيت / install:** `npm install && npm run preview|render|still|typecheck`
- **الدليل / proof:** `kosif-tool/starters/remotion/src/Root.tsx` · `kosif-tool/starters/remotion/src/Film.tsx:554` · `kosif-tool/starters/remotion/package.json`

#### ENG-313 · استخدام كروميوم المحلي مع Remotion · Local Chromium reuse for Remotion · 📦 بأمر تثبيت
- **ماذا / what:** remotion.config.ts picks KOSIF_BROWSER or newest Playwright chromium_headless_shell then chromium under $PLAYWRIGHT_BROWSERS_PATH or /opt/pw-browsers, avoiding downloads.
- **كيف / how:** Config.setBrowserExecutable(found); or --browser-executable=…
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/starters/remotion/remotion.config.ts`

#### ENG-314 · خيار التقنية: remotion · Stack option: remotion · 📦 بأمر تثبيت
- **ماذا / what:** Request phrase for stack 'remotion': starters/remotion.
- **كيف / how:** --stack remotion
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/tools/kosif.py:43` · `kosif-tool/web/generator.js`

#### ENG-315 · مشهد Three.js قابل للتقديم الحتمي · Deterministic Three.js seek scene · 📦 بأمر تثبيت
- **ماذا / what:** Three.js scene where every transform is computed from t inside seek(t) and rendered once per frame.
- **كيف / how:** WebGLRenderer({antialias:true, preserveDrawingBuffer:true}); no rAF loop; window.__kosif={duration,seek(t){...renderer.render()}}; render with render_html.cjs seek mode.
- **أرقام / params:** 1080×1920 canvas; sample 6 s 90° orbit radius 4, height 1.5, ease-in-out sine; box rotation 0.2 rad/s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:28` · `kosif-tool/playbooks/3d.md:52-68`

#### ENG-316 · تكامل Remotion مع Three · @remotion/three integration · 📦 بأمر تثبيت
- **ماذا / what:** Use ThreeCanvas in Remotion and drive transforms from useCurrentFrame().
- **كيف / how:** import {ThreeCanvas} from '@remotion/three'.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:70`

#### ENG-317 · مسار تسليم Remotion · Remotion delivery path · 📦 بأمر تثبيت
- **ماذا / what:** Still, then render with props, then gate.
- **كيف / how:** npx remotion still KosifFilm out/still.png --frame=60; npx remotion render KosifFilm out/film.mp4 --props=props.json
- **تثبيت / install:** `npx remotion still KosifFilm out/still`
- **الدليل / proof:** `kosif-tool/playbooks/render-pipeline.md:31` · `kosif-tool/playbooks/render-pipeline.md:55`

#### ENG-318 · موجز التكوين لـHyperframes · Composition brief handoff · 📦 بأمر تثبيت
- **ماذا / what:** Separate brief stating objective, verbatim copy, identity, scene summary, audio and which Hyperframes sub-skills to load.
- **كيف / how:** Write composition-brief.md; load hyperframes-core/animation/creative/keyframes/cli.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/step-3-compose.md`

#### ENG-319 · رندر مسودة ونهائي · Draft/high render quality · 📦 بأمر تثبيت
- **ماذا / what:** Render tiers for iteration vs delivery.
- **كيف / how:** npx hyperframes render --quality draft|high --output ../brag.mp4
- **تثبيت / install:** `npx hyperframes render --quality draft|high --output`
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/step-4-deliver.md`

#### ENG-320 · ربط التمرير بالزمن · Piecewise scroll->clip time mapping · 📦 بأمر تثبيت
- **ماذا / what:** Scroll mapped to continuous stop index w; active clip=floor(w); currentTime=(w-active)*duration clamped duration-0.05; seek only if diff>0.01.
- **كيف / how:** ScrollTrigger span onUpdate render().
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/mcp-higgsfield-landing/src/scripts/world.ts:79`

#### ENG-321 · تحميل حسب القرب · Proximity-priority clip loading · 📦 بأمر تثبيت
- **ماذا / what:** Load clips one at a time sorted by distance to scroll, ahead-first; whole blob; skip on reduced-motion/saveData; iOS play()/pause() prime.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/mcp-higgsfield-landing/src/scripts/world.ts:113` · `kosif-one/vendor/mcp-higgsfield-landing/README.md`

#### ENG-322 · تصيير موزع على لامبدا · AWS Lambda distributed render · 🔑 مفتاح/خدمة
- **ماذا / what:** One Lambda + Step Functions fans chunks to parallel workers, S3 holds plan and outputs.
- **كيف / how:** hyperframes lambda deploy; lambda render --concurrency=8 --memory=10240 --wait; lambda progress.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/deploy/aws-lambda.mdx` · `kosif-one/vendor/hyperframes/examples/aws-lambda/README.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/lambda.md` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/lambda.ts`

#### ENG-323 · التصيير السحابي · Remotion rendering at scale · 🔑 مفتاح/خدمة
- **ماذا / what:** Server-side rendering via Node renderer, render server template, or AWS Lambda for parallel renders.
- **كيف / how:** @remotion/renderer for SSR; @remotion/lambda (deploy function per Remotion version, redeploy site on source change, creds in env REMOTION_AWS_*); local: npx remotion render <id> out.mp4 --props='{...}' and still for golden frames.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10439-remotion-saas/rendering.md` · `kosif-atlas/skills/235-mas-video-lab/757-remotion/SKILL.md`

#### ENG-324 · أتمتة أفتر إفكتس · After Effects ExtendScript automation · 🔑 مفتاح/خدمة
- **ماذا / what:** Script AE to build comps, layers, expressions and render queue items for users who finish in Adobe.
- **كيف / how:** app.beginUndoGroup; proj.items.addComp(name,1920,1080,1.0,5.0,30); layers.addSolid/addText; property('Position').expression = 'ease(time,0,0.6,-200,420)'; renderQueue.items.add + outputModule.applyTemplate in try/catch; export .mogrt for Premiere.
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/751-adobe-after-effects/SKILL.md`

#### ENG-325 · مداخل البرمجة لبرامج المونتاج · NLE scripting entry points · 🔑 مفتاح/خدمة
- **ماذا / what:** Desktop NLE automation surfaces: After Effects ExtendScript (create comps with size/fps/duration, solids and text layers, expressions, controller null rigs, render queue output modules, .mogrt), Premiere Pro ExtendScript/UXP (sequence markers from lists, FCPXML/EDL/AAF interchange, AME presets), DaV…
- **كيف / how:** None of these apps is installed here; produce scripts or interchange files (FCPXML/EDL, marker CSV) for the user to run, and keep the local render path in HTML+ffmpeg.
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/751-adobe-after-effects/SKILL.md` · `kosif-atlas/skills/235-mas-video-lab/752-adobe-premiere-pro/SKILL.md` · `kosif-atlas/skills/235-mas-video-lab/753-davinci-resolve/SKILL.md`

#### ENG-326 · أتمتة بريمير وأفتر إفكتس بالسكربت · Premiere/AE scripting automation · 🔑 مفتاح/خدمة
- **ماذا / what:** Premiere: ExtendScript/UXP against app.project.activeSequence (guard null) for markers and sequence building; export via AME .epr presets; interchange FCPXML (keeps more effects) vs EDL (cuts only). After Effects: ExtendScript to create comps (e.g. addComp(name,1920,1080,1,5,30)), text/solid layers,…
- **كيف / how:** Requires the Adobe apps (paid, desktop) — not available here; generate JSX/XML files for the user to run
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/752-adobe-premiere-pro/SKILL.md` · `kosif-atlas/skills/235-mas-video-lab/751-adobe-after-effects/SKILL.md`

#### ENG-327 · تشغيل سكربتات DaVinci Resolve · Resolve scripting bootstrap · 🔑 مفتاح/خدمة
- **ماذا / what:** Connect Python to a running Resolve to import media, build timelines, set render jobs; external scripting is Studio-only with Preferences > System > General > External scripting = Local (free version: in-app console only).
- **كيف / how:** import DaVinciResolveScript as dvr; resolve=dvr.scriptapp('Resolve'); env RESOLVE_SCRIPT_API, RESOLVE_SCRIPT_LIB, PYTHONPATH += Modules; Linux module path /opt/resolve/Developer/Scripting/Modules; project.SetCurrentRenderFormatAndCodec('mp4','H264'), AddRenderJob
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/753-davinci-resolve/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow/SKILL.md`

#### ENG-328 · مزالق واجهة ريزولف البرمجية · Resolve API pitfalls · 🔑 مفتاح/خدمة
- **ماذا / what:** Observed in 21.1: no API to add/label grading nodes or move clips (order is set only when building a timeline); SetFades values reset to 0 after reopen; deleting with a stale item handle crashes Resolve (re-read GetItemListInTrack first); Text+ silently substitutes missing fonts; InsertFusionTitleIn…
- **كيف / how:** Plan edits as segment lists and rebuild timelines; verify fonts via fc-list before placing titles
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2465-davinciresolve-subtitle-travelnote/SKILL.md`

#### ENG-329 · محرر خارجي يقوده وكيل · Agent-driven external editor (Cassette) · 🔑 مفتاح/خدمة
- **ماذا / what:** MCP courier pattern: ingest media, pass the user's edit words verbatim to a remote editing agent, relay timeline deltas and versions, export only on explicit request; export QC returns duration, fps, resolution, black segments, mean/peak dBFS.
- **كيف / how:** cassette_ingest_media -> cassette_run_job(message verbatim) -> cassette_review_completion(decision, reason) ; requires Cassette account/back-end
- **الدليل / proof:** `kosif-atlas/skills/934-oh-my-cassette/2204-cassette-video-edit/SKILL.md`

#### ENG-330 · أنريل إنجن عبر MCP · Unreal Engine via MCP · 🔑 مفتاح/خدمة
- **ماذا / what:** Drive UE5 editor tools (assets, materials, Blueprints) through an MCP server for cinematic scenes.
- **كيف / how:** list_toolsets -> describe_toolset -> call_tool; save before/after bulk edits; wait for shader compile; stop PIE. Movie Render Queue for frames.
- **الدليل / proof:** `kosif-atlas/skills/1372-unreal-engine-skills-for-claude-code/3185-unreal-mcp/SKILL.md` · `kosif-atlas/skills/228-mas-3d-games/711-unreal-engine/SKILL.md`

#### ENG-331 · آليات تصيير سيزيوم دون واجهة · Cesium headless render mechanics · 🔑 مفتاح/خدمة
- **ماذا / what:** Cesium's globe draws nothing in a plain headless Playwright page; it works when driven frame-by-frame through Remotion with four settings.
- **كيف / how:** useDefaultRenderLoop=false; call viewer.render() (never scene.render()) per frame; contextOptions.webgl.preserveDrawingBuffer=true; gate init and each frame with delayRender (60-120 s) and settle until globe/tileset tilesLoaded is stable ~8 ticks (cap ~600); skyAtmosphere on; unrestricted MapTiler key; --gl=angle --concurrency=1 --timeout=180000.
- **أرقام / params:** settle 8 stable ticks, cap 600; delayRender 60000-120000 ms
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/references/3d-troubleshooting.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/references/3d-flyover-architecture.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/TECHNIQUE.md`

#### ENG-332 · توجيه المهام للموديلات · AI router: task-to-model and effort · 🔑 مفتاح/خدمة
- **ماذا / what:** Routes each job to Claude or Gemini by user preference, cost and availability, with per-task model, effort and token budgets; Gemini goes free-first through the app server with a hedged fallback chain.
- **كيف / how:** AIR.TASKS: code/film/imitate -> claude-opus-5-5 effort high (20000/14000/12000 tokens); plan/agent/script/vision/review/highlights -> claude-sonnet-5-5 medium; quick/post/captions -> claude-haiku-5-5 low; adaptive thinking for high/max; 400 -> retry without effort; 404 -> sonnet. Gemini: gfetch free route then user key; gemChain [chosen, gemini-3.6-flash, gemini-3.5-flash-lite] skipping sick models (3 min); hedge starts the next model if the first fails or is silent.
- **الدليل / proof:** `app/public/js/10_studio.js:2179` · `app/public/js/10_studio.js:2200` · `app/public/js/10_studio.js:2233`

#### ENG-333 · وكيل الأدوات بخطوات ظاهرة · Agent tool runner with live steps · 🔑 مفتاح/خدمة
- **ماذا / what:** The smart director plans 1-9 tool calls, shows each step live with engine and time, stops dependent steps when a critical one fails, and suggests follow-ups; a rule-based local plan runs when no AI answers.
- **كيف / how:** AGENT.plan -> {reply,title,steps,next}; tools: inputs, transcribe, verify_transcript, enhance_audio, reels, smart_captions, analyze_reference, imitate, montage, motion_film, launch_film, template, template_mix, stock, edit, camera, images, voice, music, brand, preset, review, compare, fill_gaps, export_fingerprint, post, jev_ideas, render, answer; render only if the user asked; critical tools inputs/montage/motion_film/launch_film/reels/imitate stop the chain on failure; film intent enforced.
- **الدليل / proof:** `app/public/js/10_studio.js:3180` · `app/public/js/10_studio.js:3206` · `app/public/js/10_studio.js:3229`

#### ENG-334 · تصيير على كلاود رن · GCP Cloud Run render · 🔑 مفتاح/خدمة
- **ماذا / what:** Cloud Run + Workflows + GCS chunked render.
- **كيف / how:** hyperframes cloudrun ...; examples/gcp-cloud-run.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/deploy/gcp-cloud-run.mdx` · `kosif-one/vendor/hyperframes/examples/gcp-cloud-run/README.md`

#### ENG-335 · تصيير كوبرنيتس · Kubernetes jobs render · 🔑 مفتاح/خدمة
- **ماذا / what:** Example Dockerfile and job manifests for batch rendering.
- **كيف / how:** examples/k8s-jobs.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/examples/k8s-jobs/README.md`

#### ENG-336 · التصيير السحابي · Cloud render (HeyGen-hosted) · 🔑 مفتاح/خدمة
- **ماذا / what:** Zero-infra render: zip, upload, render, download; OAuth or API key; 200 MB upload limit with .hyperframesignore.
- **كيف / how:** npx hyperframes auth login [--api-key]; npx hyperframes cloud render [--quality high --fps 60] [--dry-run --json].
- **أرقام / params:** 200 MB upload limit
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/cloud.md`

#### ENG-337 · التصيير على Cloud Run · Google Cloud Run render · 🔑 مفتاح/خدمة
- **ماذا / what:** Same lifecycle on GCP Cloud Run.
- **كيف / how:** npx hyperframes cloudrun deploy --project P --region us-central1; cloudrun render ... --wait; render-batch; progress; destroy.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/cloudrun.md` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/cloudrun.ts`

#### ENG-338 · تغليف الإضافة لعدة وكلاء · Multi-agent plugin packaging · 🔑 مفتاح/خدمة
- **ماذا / what:** Skills ship as a Claude Code plugin (marketplace heygen-com/hyperframes), Codex/Cursor/Gemini plugins and standalone skills via `npx skills add` or `npx hyperframes skills update` (core set; workflows install on demand).
- **كيف / how:** claude plugin marketplace add heygen-com/hyperframes; claude plugin install hyperframes@hyperframes; npx hyperframes skills update <workflow>.
- **أرقام / params:** 21 published skills
- **الدليل / proof:** `kosif-one/vendor/hyperframes/README.md` · `kosif-one/vendor/hyperframes/CLAUDE.md` · `kosif-one/vendor/hyperframes/skills-manifest.json`

#### ENG-339 · الجسر البعيد · Site bridge / render client (remote) · 🔑 مفتاح/خدمة
- **ماذا / what:** Consent-gated remote planning (KOSIF_SITE_TOKEN, --allow-remote) and remote 2D render client; fail closed.
- **كيف / how:** python scripts/kmotion.py bridge …; kmotion remote
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:327` · `100-superskills/skills/kosif-montage-motion/references/audit-v5.3-python.md`

#### ENG-340 · عميل التصيير الخارجي · External Python render client · 🔑 مفتاح/خدمة
- **ماذا / what:** Submits a 2d_motion plan to hosted Site for silent 2D MP4; fails closed.
- **كيف / how:** python scripts/render_client.py status | render --plan plan.json --out NEW.mp4 --allow-remote
- **أرقام / params:** 1-30 s; 24/25/30 fps; long edge <=1280; min 128; <=100 MiB; 3 jobs/h public
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/python-render.md` · `100-superskills/skills/kosif-montage-motion/scripts/render_client.py` · `100-superskills/skills/kosif-montage-motion/tests/test_render_client.py`

#### ENG-341 · جسر الموقع · Site bridge planner · 🔑 مفتاح/خدمة
- **ماذا / what:** health/templates/plan/validate/compile/project against hosted workbench.
- **كيف / how:** python scripts/site_bridge.py plan --task ... --seconds 12 --fps 30 --aspect 9:16 --mode pro --allow-remote
- **أرقام / params:** seconds 2-600; fps 24/25/30/50/60; aspects 9:16,16:9,1:1,4:5; 20 s timeout; 1 MiB
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/site-bridge.md` · `100-superskills/skills/kosif-montage-motion/scripts/site_bridge.py`

#### ENG-342 · تصيير على GitHub · GitHub Actions render · 🔑 مفتاح/خدمة
- **ماذا / what:** kosif-render workflow in kosif-render-lab; no GPU; billing issues.
- **كيف / how:** gh workflow run kosif-render.yml --repo kosif199022-jpg/kosif-render-lab -f project=night_boat -f shards=6 -f blur=4
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/render-farm.md`

#### ENG-343 · تكامل: Lottie Creator MCP · Integration: Lottie Creator MCP · 🔑 مفتاح/خدمة
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### ENG-344 · تكامل: LottieFiles platform MCP · Integration: LottieFiles platform MCP · 🔑 مفتاح/خدمة
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### ENG-345 · حزمة الأطلس لمهارات الفيديو والحركة · Atlas skill pack: video/motion pipeline skills · 🔑 مفتاح/خدمة
- **ماذا / what:** Pointers (skill ids) the video-producer agent reads from the Atlas for programmatic video work.
- **كيف / how:** kosif_atlas_read skill_id=<id> (third-party data, never run its scripts without review).
- **أرقام / params:** remotion 757, video 3531, remotion-maps 10435, ffmpeg 754, final-cut-pro 755 (FCPXML), remotion-captions 10431, remotion-markup 10436, transcoding-and-abr-ladder 9243
- **الدليل / proof:** `kosif-one/tools/kosif-omni/agents/kosif-video-producer.md` · `kosif-one/tools/kosif-omni/tools/swarm_skillpacks.json`

#### ENG-346 · خط DaVinci بالسكربت · Resolve scripting pipeline CLI · 🔑 مفتاح/خدمة
- **ماذا / what:** Drives DaVinci Resolve Studio via DaVinciResolveScript: doctor, clips by record date, duplicate timeline, named tracks, markers, render job, ffprobe verify.
- **كيف / how:** python3 resolve_pipeline.py {doctor|clips|duplicate|tracks|marker|render|verify} --timeline --frame --color Blue --format mp4 --codec H264
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/scripts/resolve_pipeline.py:83`

#### ENG-347 · خريطة محركات الفيديو بالكود · Code-video engine landscape (22 direct tools) · 🔑 مفتاح/خدمة
- **ماذا / what:** Reference list of code/timeline video tools with licences: Editly, FFCreator, fframes (MIT), Manim (MIT), Motion Canvas, MoviePy, Remotion, Rendervid, Revideo, VideoFlow (Apache-2.0), VideoRenderingEngine, VidPy, WebMotion (MIT), Diffusion Studio Core, Etro (GPL-3.0), Movie Masher (MPL-2.0), Twick, …
- **كيف / how:** Consult when the user's team uses another stack; KOSIF itself uses HyperFrames + GSAP + FFmpeg + Playwright + numpy.
- **أرقام / params:** source catalog: 500 tools (22 direct, 254 adjacent, 224 complementary), reviewed 2026-10-06
- **الدليل / proof:** `kosif-studio/motion/references/tools-catalog.md`

#### ENG-348 · مسودة ثم نهائي · Previz-then-final tiering · 🔑 مفتاح/خدمة
- **ماذا / what:** Render whole chain cheaply (480p/mini) then final legs at 1080p.
- **كيف / how:** Same endpoint with VRES.
- **أرقام / params:** 480p -> 1080p
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/references/prompts.md`

#### ENG-349 · ضبابية حركة بإطارات فرعية · Sub-frame motion blur · 👁 شوهد في فيديو
- **ماذا / what:** render 4 sub-frames per output frame by seeking t+k/(4·fps) and average with ffmpeg tmix (frames=4) for natural motion blur at 60 fps
- **أرقام / params:** tmix=frames=4
- **الدليل / proof:** `style:pm-twoclipping-5cba86` · `style:pm-xelandre-363f00`

#### ENG-350 · استخدام مكونات المنتج الحقيقية · Real component reuse · 👁 شوهد في فيديو
- **ماذا / what:** import product React components into Remotion scenes
- **الدليل / proof:** `style:pm-fractadev-149adc`

#### ENG-351 · كرة لامعة مرسومة بالأشعة مع ظل · Ray-traced glossy sphere with contact shadow · 👁 شوهد في فيديو
- **ماذا / what:** GLSL SDF/ray-sphere intersection, Blinn-Phong specular, soft shadow on ground plane computed analytically
- **أرقام / params:** albedo #111, spec power 64, shadow blur wide
- **الدليل / proof:** `style:pm-hbcoop-de365c`

#### ENG-352 · عرض حتمي بدالة الإطار · Deterministic seek(frame) rendering · 👁 شوهد في فيديو
- **ماذا / what:** Render each frame as a pure function of frame number using keyframe tables with interpolation, no timers or Math.random; capture with headless browser per frame and encode
- **أرقام / params:** Playwright screenshots, H.264 yuv420p
- **الدليل / proof:** `style:pm-notdwd-7de38a`

#### ENG-353 · مواصفة لقطات بأرقام الإطارات · Frame-addressed shot spec · 👁 شوهد في فيديو
- **ماذا / what:** write every keyframe as (frame, x, y, scale, blur, opacity) from a frame-counted reference; cuts placed a fixed 2 frames before beat k = offset + k*60/BPM
- **أرقام / params:** 29.97 fps spec, 59.94 master
- **الدليل / proof:** `style:pm-notdwd-c2037d`

#### ENG-354 · محاكاة حتمية كدالة في الزمن · Deterministic f(t) simulation · 👁 شوهد في فيديو
- **ماذا / what:** Precompute the event list with a seeded schedule; render(t) replays events <= t to derive state, so any frame can be screenshotted independently
- **أرقام / params:** canvas 1080x1080; 30fps; no RNG at render time
- **الدليل / proof:** `style:pm-parkerrex-1a54fe`

#### ENG-355 · خط إنتاج لفيلم طويل مع صوت وترجمة · Long-form render pipeline · 👁 شوهد في فيديو
- **ماذا / what:** Render frames offline, generate/mix audio, burn subtitles and mux with ffmpeg; keep only final file
- **أرقام / params:** 60 fps × 300 s = 18000 frames
- **الدليل / proof:** `style:pm-rebutonepress-810f78`

#### ENG-356 · قاعدة كل شيء مولّد بالكود · Code-only asset rule · 👁 شوهد في فيديو
- **ماذا / what:** no downloaded models/textures/audio: procedural geometry nodes, shader noise, synthesised audio, system fonts
- **أرقام / params:** document CONCEPT.md + STORYBOARD.md shots with timecodes
- **الدليل / proof:** `style:pm-theparuchh-6e08c3`

#### ENG-357 · اختيار أصغر محرك كافٍ · Smallest capable engine choice · 📄 موصوف
- **ماذا / what:** CSS/WAAPI, Motion, GSAP, SVG, Three/R3F, HyperFrames, Remotion selected by need.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-director.md` · `kosif-studio/motion/references/motion-director.md` · `kosif-studio/motion/references/tools-catalog.md`

#### ENG-358 · قواعد الحتمية للتصيير إطارًا بإطار · Seekable-timeline determinism rules · 📄 موصوف
- **ماذا / what:** Frame-captured HTML must give the same pixels for the same time: no wall clock, no unseeded random, no infinite repeats, no async timeline building, no media play() calls.
- **كيف / how:** Replace Math.random with a seeded PRNG (mulberry32); repeat: Math.ceil(duration/cycle)-1 instead of -1; never build timelines in setTimeout/await; use tl.set at a time instead of onComplete for state flips so rewind works; never animate visibility/display directly in GSAP.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/SKILL.md` · `kosif-atlas/skills/2702-hyperframes/10377-gsap/references/effects.md`

#### ENG-359 · ظهور بإطارات CSS · CSS/WAAPI keyframe reveals · 📄 موصوف
- **ماذا / what:** Pure CSS/Web Animations patterns: fade+slide up, scale-in, slide-from-side, blur-in, split-text char reveal.
- **كيف / how:** translateY 30px->0 0.6s out-expo; scale 0.9->1; translateX -50px; blur(10px)->0 0.8s; WAAPI el.animate(keyframes,{duration:300, easing:'cubic-bezier(0.16,1,0.3,1)', fill:'forwards'}). For frame-exact rendering, pause all animations and set currentTime per frame (document.getAnimations().forEach(a=>{a.pause(); a.currentTime=t})).
- **أرقام / params:** 30px/0.6s; blur 10px/0.8s
- **الدليل / proof:** `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/animation-patterns.md` · `kosif-atlas/skills/3529-ui-design/14308-interaction-design/references/animation-libraries.md`

#### ENG-360 · خط عرض توضيحي من HTML إلى فيديو · Single-prompt demo pipeline (HTML -> TTS -> ffmpeg) · 📄 موصوف
- **ماذا / what:** One HTML file per scene at 1920x1080, narration text per scene, a scenes.json manifest, then screenshot/render scenes, synthesize voice, and crossfade-concat with ffmpeg.
- **كيف / how:** Here: render scenes with kosif-tool render_html.cjs (Playwright Chromium at /opt/pw-browsers + ffmpeg, both present) (motion, not stills), voice from user audio or a TTS available; edge-tts is an online unofficial service (needs install+network).
- **أرقام / params:** scene transition crossfade 0.3-0.5s; auto duration = TTS + 1.5s; checklist: audio stream present, 1920x1080, no black frames, first 3s hook, end card URL+CTA
- **الدليل / proof:** `kosif-atlas/skills/166-demo-video/535-demo-video` · `kosif-atlas/skills/1644-framecraft/4629-demo-video`

#### ENG-361 · قواعد أداء الحركة في المتصفح · Web-motion performance rules for renders · 📄 موصوف
- **ماذا / what:** Animate transform and opacity; avoid layout properties; pre-blur instead of animating blur on many nodes; one engine per property; cap device pixel ratio; precompute ranges on resize; pause offscreen loops; remove will-change after use; no 'transition: all'.
- **كيف / how:** Even in frame-stepped rendering these keep frames cheap and avoid paint artifacts.
- **أرقام / params:** DPR cap 2 (1.25 for full-bleed shaders); Lighthouse 90+; LCP < 2.5s; CLS ~0
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali/references/implementation-and-performance.md` · `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md` · `kosif-atlas/skills/880-superloopy/1941-superloopy-frontend/references/motion.md`

#### ENG-362 · مواصفات تسليم يوتيوب 4K وفحص الجهارة · YouTube 4K delivery spec and loudness check · 📄 موصوف
- **ماذا / what:** Deliver at timeline frame rate with bitrates of H.264 45 Mbps / H.265 30 Mbps for <=30 fps and 68 / 45 Mbps for 60 fps; integrated loudness -14 LUFS +/-1 with true peak <= -1 dBTP; rendered duration within one frame of the timeline.
- **كيف / how:** Measure with ffmpeg -af ebur128=peak=true -f null -; check fps/size/duration with ffprobe; never copy example numbers into reports without measuring; normalize the full mix, not individual SFX.
- **أرقام / params:** 45/30 Mbps (<=30 fps); 68/45 Mbps (60 fps); -14 LUFS +/-1; TP <= -1 dBTP
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2450-davinciresolve-audio-delivery/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound/SKILL.md`

#### ENG-363 · اصطلاح المسارات والعلامات في المونتاج · Editing track and marker convention · 📄 موصوف
- **ماذا / what:** Fixed track layout for voice-led edits: V1 screen clips, V2 graphics, V3 text overlays, A1 voice, A2 location sound, A3 SFX, A4 music; named colour markers (CHAPTER per beat, GFX for card slots, HOOK for hook segments, review markers for audio/visual issues).
- **كيف / how:** Mirror this in the kosif timeline JSON (layers + markers) so captions, cards and sound passes can re-sync after any cut change; markers are re-placed when cuts change.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2460-davinciresolve-story-devtalk/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/SKILL.md`

#### ENG-364 · وصفة ترميز التريلر وحلقة الجيف · Trailer encode and GIF loop recipe · 📄 موصوف
- **ماذا / what:** Final masters as H.264 High, yuv420p, CRF 17, preset slow, 60 fps with GOP 60, AAC 192k 48 kHz, faststart, two-pass loudnorm; GIF loops cross-fade the last 0.4 s into the first 0.4 s and use palette generation.
- **كيف / how:** Intermediate at CRF 8 + PCM 24-bit; pass 1 loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json then apply measured values; GIF: xfade 0.4 s, palettegen=stats_mode=diff:max_colors=192 + paletteuse; if over 15 MB reduce width to 480, fps to 15, colors to 128, or shorten, in that order.
- **أرقام / params:** CRF 17; -g 60; AAC 192k; loudnorm I=-14 TP=-1.5 LRA=11; GIF 192 colors
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/assembly-and-review.md` · `kosif-atlas/skills/1526-gamegen/4173-game-trailer/SKILL.md`

#### ENG-365 · خط تحويل مشاهد HTML إلى فيديو · HTML scenes to MP4 pipeline · 📄 موصوف
- **ماذا / what:** Each scene is a 1920x1080 HTML file plus a narration text file; a scenes.json manifest lists order, durations and narration; a build script screenshots/records scenes, synthesizes narration, and concatenates with crossfades into one MP4 with an audio stream.
- **كيف / how:** Here: Playwright for frames (present), ffmpeg xfade/concat (present), TTS needs an install or the user's recorded audio; quality checks: audio stream exists, 1920x1080, no black frames between scenes, first 3 s grab attention, end card has URL and CTA.
- **أرقام / params:** 1920x1080; crossfade 0.3-0.5 s
- **الدليل / proof:** `kosif-atlas/skills/166-demo-video/535-demo-video/SKILL.md`

#### ENG-366 · نموذج التركيب بمحور زمني واحد · Single time-axis composition model · 📄 موصوف
- **ماذا / what:** Treat the whole film as one element tree rendered as a pure function of one authored time T: nothing mounts or unmounts at section boundaries, so any object can persist, travel and morph across the entire film; sections are named entries with durations and a one-sentence description; choreography ke…
- **كيف / how:** Implement in the kosif HTML engine: a global scenes array [{name,dur,desc}], cue lookup by name, animate({from,to,start,end,ease})(T) helpers, hard cuts as explicit Shot ranges; build the first 5-8 s, render, inspect a contact sheet, then continue.
- **أرقام / params:** gate after first 5-8 s
- **الدليل / proof:** `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`

#### ENG-367 · عرض تقديمي HTML بمسرح ثابت · Fixed-stage HTML deck · 📄 موصوف
- **ماذا / what:** A single-file deck authored on a fixed 1920x1080 stage scaled as a whole (letterbox, never reflow), slides switched by visibility/opacity not display, keyboard navigation, export to PDF; also a perfect base for slide-motion videos.
- **كيف / how:** Density modes: speaker-led (one idea, 1-3 bullets) vs reading-first (4-8 bullets or 4-6 cards); nothing below 24 px at stage size; split instead of shrinking; draft outline with seconds per slide vs the time budget; show three real title-slide previews (restrained, expressive, wildcard) instead of asking taste questions; verify every slide in a browser at 1280x720 and phone size.
- **أرقام / params:** 1920x1080; min 24 px; 1-3 vs 4-8 bullets
- **الدليل / proof:** `kosif-atlas/skills/345-visuals/1241-html-deck/SKILL.md` · `kosif-atlas/skills/345-visuals/1241-html-deck/references/deck-template.md`

#### ENG-368 · مصفوفة اختيار البرنامج المنفذ · Editor routing matrix · 📄 موصوف
- **ماذا / what:** Plan to the user's tool and its limits: After Effects for layered masks, text and compound motion (verify version before naming properties or writing JSX; never script over an existing project); DaVinci Resolve/Fusion separates edit, colour and node compositing (don't translate AE effect names into …
- **كيف / how:** If the user has no editor, Claude renders itself: KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg); ffmpeg for cuts/grades; Remotion only after npm install.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/quality-and-editors.md`

#### ENG-369 · تسلسل مراحل ما بعد الإنتاج · Post-production dependency chain · 📄 موصوف
- **ماذا / what:** Order finishing as editorial -> VFX -> colour -> sound -> conform -> deliver, with picture lock as the gate (grading before lock is rework); find the critical path that sets the delivery date; list deliverables (masters, formats, versions, captions, metadata), each traced to a finishing step with QC…
- **كيف / how:** For Claude's own pipeline: lock the timeline JSON, then apply grade/LUT and audio mix, then render master + platform variants and verify with kosif-tool verify_video.py / TEST_REPORT.md.
- **الدليل / proof:** `kosif-atlas/skills/2293-film-video-production/8775-sequence-the-post-pipeline/SKILL.md` · `kosif-atlas/skills/2293-film-video-production/8773-define-the-deliverables/SKILL.md` · `kosif-atlas/skills/2293-film-video-production/8774-schedule-the-shoot/SKILL.md`

#### ENG-370 · تغيير الحاوية بدون إعادة ترميز · Lossless remux / container swap · 📄 موصوف
- **ماذا / what:** Swap MKV/MOV to MP4 or repair a broken header instantly by copying streams instead of re-encoding.
- **كيف / how:** ffmpeg -i in.mkv -c copy -movflags +faststart out.mp4 ; for corrupted DTS add -fflags +genpts before -i and -avoid_negative_ts make_zero
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md` · `kosif-atlas/skills/235-mas-video-lab/756-losslesscut/SKILL.md`

#### ENG-371 · الترميز بالعتاد مع بديل برمجي · Hardware encoder fallback · 📄 موصوف
- **ماذا / what:** NVENC/QSV/VideoToolbox are fast but not always compiled in; check before use and fall back to libx264/libx265/SVT-AV1.
- **كيف / how:** ffmpeg -encoders | grep nvenc ; GPU: -hwaccel cuda -c:v h264_nvenc -preset p6/p7 -tune hq -rc vbr -cq 19-20 ; CPU fallback libx264 -crf 18. Container here has libx264, libx265, libsvtav1, libaom, libvpx (no GPU).
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md` · `kosif-atlas/skills/2387-streaming-media-engineering/9243-transcoding-and-abr-ladder/SKILL.md`

#### ENG-372 · مسارات مسماة بالأدوار · Named role tracks · 📄 موصوف
- **ماذا / what:** Reserve tracks by role so later stages never collide with the main edit: video OVERLAY, GFX, SUBTITLE, HOOK_TEXT (top); audio AMBIENCE, SFX, MUSIC, HOOK; dialogue VOICE on A1. Find tracks by name, re-running must not add duplicates.
- **كيف / how:** Resolve AddTrack + SetTrackName; same idea in Remotion/HyperFrames layer naming and ffmpeg filter labels
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2460-davinciresolve-story-devtalk/SKILL.md`

#### ENG-373 · ترتيب مراحل ما بعد الإنتاج · Post pipeline order · 📄 موصوف
- **ماذا / what:** Editorial -> VFX -> colour -> sound -> conform -> deliver, gated by picture lock; define deliverables (masters, versions, captions, metadata, QC) before finishing. In practice: cut -> colour -> privacy mosaic -> captions -> audio checks before render; any recut requires re-timing captions, cards, ch…
- **الدليل / proof:** `kosif-atlas/skills/2293-film-video-production/8775-sequence-the-post-pipeline/SKILL.md` · `kosif-atlas/skills/2293-film-video-production/8773-define-the-deliverables/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow/SKILL.md`

#### ENG-374 · وسائط بديلة للأداء · Proxy and performance workflow · 📄 موصوف
- **ماذا / what:** Long-GOP H.265/4K stutters in editors: generate proxies (ProRes Proxy / DNxHR LB / low-res H.264) and switch back for the final render.
- **كيف / how:** ffmpeg -c:v prores_ks -profile:v 0 or -c:v dnxhd -profile:v dnxhr_lb -vf scale=-2:540 ; Resolve 'Prefer Proxies'
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/753-davinci-resolve/SKILL.md` · `kosif-atlas/skills/235-mas-video-lab/755-final-cut-pro/SKILL.md`

#### ENG-375 · أخذ عينات حتمي للرندر · Deterministic sampling for render · 📄 موصوف
- **ماذا / what:** Audio reactivity must use pre-extracted data sampled per frame on the timeline — no Web Audio, Math.random or Date.now at render.
- **كيف / how:** for f<totalFrames: tl.call(draw(frames[f]),[],f/fps). Same in Remotion via useCurrentFrame index.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/audio-reactive.md`

#### ENG-376 · فخاخ ffmpeg الصوتية · ffmpeg audio traps · 📄 موصوف
- **ماذا / what:** Exit 0 isn't audio: amix divides by inputs (use normalize=0), adelay needs per-channel values, c=2 means channel mask, aevalsrc has no comparison operators, NaN silences sum.
- **كيف / how:** Always ffprobe duration/channels after render; adelay=500|500; gte(t,1); exp(-max(0,t-a)*k).
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3901-sound/references/TRAPS.md`

#### ENG-377 · اختيار معمارية الصوت اللحظي · Realtime audio architecture choice · 📄 موصوف
- **ماذا / what:** For live/browser audio: latency budget first; Web Audio AudioWorklet in browser; oversample nonlinearities 2-8x; no locks/allocs on audio thread.
- **كيف / how:** AudioWorklet; buffer 64-128 for live.
- **أرقام / params:** 64-128 samples
- **الدليل / proof:** `kosif-atlas/skills/2238-audio-dsp-engineering/8508-choose-audio-dsp-architecture` · `kosif-atlas/skills/996-write-realtime-audio-code/2280-write-realtime-audio-code`

#### ENG-378 · زمن حتمي للريندر · Deterministic time for offline render · 📄 موصوف
- **ماذا / what:** For video export, replace clock.elapsedTime with frame/fps and step physics with fixed dt so every frame re-renders identically.
- **كيف / how:** uniform uTime = frame/fps; capture canvas via Puppeteer/Playwright -> PNG sequence -> ffmpeg -c:v libx264 -pix_fmt yuv420p.
- **أرقام / params:** fps 30/60
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/SKILL.md` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### ENG-379 · تحميل الخطوط قبل الالتقاط · Web font loading for headless render · 📄 موصوف
- **ماذا / what:** Frame capture before fonts load gives fallback glyphs; block until fonts are ready.
- **كيف / how:** Self-host woff2 with font-display:block, preload critical files, await document.fonts.ready before first frame; never rely on Google Fonts @import at render time.
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14126-web-typography/references/css-implementation.md` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### ENG-380 · تحويلات ImageMagick · ImageMagick batch conversions · 📄 موصوف
- **ماذا / what:** Format conversion, resize, crop, thumbnails, contact sheets for sprite/illustration assets.
- **كيف / how:** convert (IM6 here) e.g. convert in.png -filter point -resize 800% out.png for crisp pixel upscale; montage for sheets.
- **أرقام / params:** -filter point for pixel art
- **الدليل / proof:** `kosif-atlas/skills/2173-tools-plugin/7919-imagemagick-conversion`

#### ENG-381 · سلم المصيّرات SVG ثم Canvas ثم WebGL · Renderer ladder SVG -> Canvas -> WebGL · 📄 موصوف
- **ماذا / what:** Pick the lightest renderer that handles the mark count and motion, measured not assumed.
- **كيف / how:** SVG/DOM: labels, exact values, moderate marks (crisp vector export). Canvas2D: dense flat marks, many sparklines, frequent redraws. WebGL (Three.js, PixiJS, regl, deck.gl, Sigma.js): 1e5-1e6+ marks, particles, blending, shaders, true 3D. Keep labels/axes in SVG/HTML even when marks are WebGL; one scene clock; typed arrays; rebuild buffers only on data change; clamp devicePixelRatio for heavy scenes.
- **أرقام / params:** WebGL when ~1e5-1e6+ marks
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/webgl-2d-animation-patterns.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/when-3d-is-justified.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10322-data-visualization/references/default-stack-selection.md`

#### ENG-382 · ساعة حركة مدفوعة بالإطار · Frame-driven animation clock · 📄 موصوف
- **ماذا / what:** All chart and map motion derives from the current frame/time, never wall-clock timers or CSS transitions, so renders are reproducible.
- **كيف / how:** Remotion: useCurrentFrame() + interpolate with clamp and easing; KOSIF HTML: seek(t) recomputes the whole scene; one scene clock per visualization; pause nothing because nothing runs on its own.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/TECHNIQUE.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/webgl-2d-animation-patterns.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-explainer-architecture.md`

#### ENG-383 · طبقات برمجية فوق اللقطات المولدة · Programmatic overlays over AI footage · 📄 موصوف
- **ماذا / what:** AI clips serve as B-roll; titles, UI, numbers, logos and captions are rendered programmatically (Remotion, Hyperframes, HTML) on top.
- **كيف / how:** Generate clean clips with 'No subtitles or on-screen text', then composite brand type, callouts and transitions in code; Hyperframes is Apache-2.0 HTML frames, Remotion needs a company license for commercial use by companies.
- **الدليل / proof:** `kosif-atlas/skills/1446-marketing-skills/3531-video` · `kosif-atlas/skills/2976-pwdev-social-media/12594-video-gen` · `kosif-atlas/skills/259-quickdesign/865-quickdesign`

#### ENG-384 · رفع دقة محلي صادق إلى 4K · Honest local upscale to 4K (Lanczos + unsharp) · 📄 موصوف
- **ماذا / what:** Delivers a sharper desktop copy of a 720p AI clip by local upscaling, explicitly labelled as not native 4K.
- **كيف / how:** ffmpeg -vf scale=3840:2160:flags=lanczos,unsharp=... (exact unsharp values not recorded) -> H.264; record provenance as upscale.
- **أرقام / params:** measured: 3840x2160, 24 fps, 5.056 s, ~8.5 Mbps video + AAC 129 kbps, 5.44 MB
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/brand/earth-intro-20261009-4k.mp4` · `kosif-earth-ci-fork/docs/design/KOSIF_EARTH_CINEMATIC_INTRO_20261009_ar.md`

#### ENG-385 · موجّه المحركات · Engine router · 📄 موصوف
- **ماذا / what:** Decision table choosing between Native Canvas (implemented), Remotion, HyperFrames, KOSIF Motion, Higgsfield and scroll-world/brag directions based on availability and goals.
- **كيف / how:** Read docs/ENGINE_ROUTER.md, verify the target tool is installed and usable, explain trade-offs before switching, fall back to Native Canvas and tell the user.
- **الدليل / proof:** `fastify-motion-bro/docs/ENGINE_ROUTER.md:1-12` · `fastify-motion-bro/AGENTS.md:11`

#### ENG-386 · مسار KOSIF Motion · KOSIF Motion route (target) · 📄 موصوف
- **ماذا / what:** Routing target for audio2motion, karaoke captions, structural shape kit, voice analysis and local montage living in the owner's kosif-one / kosif-studio repos.
- **كيف / how:** Discover tools in kosif-one and kosif-studio, run their alignment and read their report before claiming word sync.
- **الدليل / proof:** `fastify-motion-bro/docs/ENGINE_ROUTER.md:5` · `fastify-motion-bro/README.md:48` · `fastify-motion-bro/docs/SOURCE_AUDIT.md:9-10`

#### ENG-387 · إعادة الترميز بإطارات مفتاحية كثيفة · Dense-keyframe re-encode for seekable footage · 📄 موصوف
- **ماذا / what:** Sources with sparse GOP (>~1 s keyframe interval) freeze on seek under overlays; re-encode with keyframe interval = composition fps.
- **كيف / how:** ffmpeg -y -i in.mp4 -c:v libx264 -crf 18 -g 30 -keyint_min 30 ... (match 24/25/60 fps).
- **أرقام / params:** crf 18, -g = fps
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/talking-head-recut/SKILL.md`

#### ENG-388 · عقد الزمن الحتمي render(t) · Deterministic render(t) contract · 📄 موصوف
- **ماذا / what:** Each frame is a pure function of t; no requestAnimationFrame, Date.now or unseeded Math.random; use MOTION.rng(seed).
- **كيف / how:** window.render(t)+window.__ready, or paused GSAP timeline registered literally in window.__timelines['root']; MOTION.shim(root,seconds)
- **أرقام / params:** frame 150 at 5.00 s identical every render
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/animation_craft.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### ENG-389 · تقسيم التصيير على أجهزة · Render farm shard · 📄 موصوف
- **ماذا / what:** Split frame ranges across machines, join losslessly; GitHub Actions in private kosif-render-lab.
- **كيف / how:** scripts/shard.py; references/render-farm.md
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:468`

#### ENG-390 · تسريع العتاد عبر Edge · Edge D3D11 GPU flags · 📄 موصوف
- **ماذا / what:** Use Edge/Chrome with ANGLE D3D11 and ignore-gpu-blocklist to render shaders on real GPU; HTML_RENDER_SOFTWARE=1 forces SwiftShader.
- **كيف / how:** --use-angle=d3d11 --ignore-gpu-blocklist
- **أرقام / params:** claimed 30x vs software; 1.0–1.5 s per 1080p 3D frame on Iris Xe; CRF 17
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/animation_craft.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### ENG-391 · بديل ffprobe في البيئات المغلقة · Sandbox ffprobe stand-in · 📄 موصوف
- **ماذا / what:** Where ffprobe is missing, a Python stand-in answers the fields the kit reads (codec, size, frame rate, frames, sample rate, channels, duration, size) in JSON or CSV.
- **كيف / how:** python scripts/ffprobe_shim.py -v error -show_entries stream=…:format=… -of json FILE; parity test vs real ffprobe.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_cloud.py:31`

#### ENG-392 · فيديو حتمي قابل للقفز · Deterministic seekable video · 📄 موصوف
- **ماذا / what:** One seekable clock; seeded randomness; preload; sample first/peak/boundary/final frames, seek both ways.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-director.md` · `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### ENG-393 · جدول أزمنة التصيير · Render farm timing table · 📄 موصوف
- **ماذا / what:** Measured times on i7-1165G7 for 5 s 3D 1080p.
- **كيف / how:** preview 28 s; render --blur 1 --capture jpeg 87 s (SSIM 0.990); PNG 117 s; final --blur 4 173 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/render-farm.md`

#### ENG-394 · ترند: Program is the film: seek(t) route A · Trend: Program is the film: seek(t) route A · 📄 موصوف
- **ماذا / what:** Observed Opus motion wave technique (Sept-Oct 2026): index.html window.seek(t), Playwright per frame, FFmpeg.
- **أرقام / params:** index.html window.seek(t), Playwright per frame, FFmpeg
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### ENG-395 · ترند: Closed-form springs for UI morphs · Trend: Closed-form springs for UI morphs · 📄 موصوف
- **ماذا / what:** Observed Opus motion wave technique (Sept-Oct 2026): sum of springs per change.
- **أرقام / params:** sum of springs per change
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### ENG-396 · ترند: 4 sub-frame motion blur · Trend: 4 sub-frame motion blur · 📄 موصوف
- **ماذا / what:** Observed Opus motion wave technique (Sept-Oct 2026): --blur 4.
- **أرقام / params:** --blur 4
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### ENG-397 · ترند: One clock picture+sound · Trend: One clock picture+sound · 📄 موصوف
- **ماذا / what:** Observed Opus motion wave technique (Sept-Oct 2026): beat grid, hits on contact frames, -14 LUFS.
- **أرقام / params:** beat grid, hits on contact frames, -14 LUFS
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### ENG-398 · ترند: Self-critique on frames · Trend: Self-critique on frames · 📄 موصوف
- **ماذا / what:** Observed Opus motion wave technique (Sept-Oct 2026): contact sheets, phone-width, 6-8 criteria, >=3 rounds.
- **أرقام / params:** contact sheets, phone-width, 6-8 criteria, >=3 rounds
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### ENG-399 · ترند: Effort xhigh/max · Trend: Effort xhigh/max · 📄 موصوف
- **ماذا / what:** Observed Opus motion wave technique (Sept-Oct 2026): median 20 min short, 4 h celebrated, $10 median tokens.
- **أرقام / params:** median 20 min short, 4 h celebrated, $10 median tokens
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### ENG-400 · ترند: Generate-then-trace · Trend: Generate-then-trace · 📄 موصوف
- **ماذا / what:** Observed Opus motion wave technique (Sept-Oct 2026): video model base shots redrawn in JS.
- **أرقام / params:** video model base shots redrawn in JS
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### ENG-401 · ترند: Listen with math (@kloss_xyz) · Trend: Listen with math (@kloss_xyz) · 📄 موصوف
- **ماذا / what:** Observed Opus motion wave technique (Sept-Oct 2026): per-frame audio channels, tape clock, spectrogram magma ground, glitch pass; motion.py channels, loopcheck.
- **أرقام / params:** per-frame audio channels, tape clock, spectrogram magma ground, glitch pass; motion.py channels, loopcheck
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### ENG-402 · ترند: Measure real motion (@aicreataro) · Trend: Measure real motion (@aicreataro) · 📄 موصوف
- **ماذا / what:** Observed Opus motion wave technique (Sept-Oct 2026): motion.py mocap -> particle body, loadModel GLB.
- **أرقام / params:** motion.py mocap -> particle body, loadModel GLB
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### ENG-403 · ترند: Arabic kinetic type gap · Trend: Arabic kinetic type gap · 📄 موصوف
- **ماذا / what:** Observed Opus motion wave technique (Sept-Oct 2026): MOTION.revealWords masks, dir on text not html, karaoke per word.
- **أرقام / params:** MOTION.revealWords masks, dir on text not html, karaoke per word
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### ENG-404 · تايملاين JSON إلى فيلم · JSON timeline → film renderer · 📄 موصوف
- **ماذا / what:** Renders a timeline spec into a finished film with cuts, transitions, speed changes, Arabic text overlays and ducked music, then runs the delivery gate.
- **كيف / how:** From the studio: recipe 'timeline' (form in the الوصفات tab, POST /api/jobs {recipe:'timeline', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py timeline …`.
- **أرقام / params:** spec (file); --out out/film.mp4; --workers 0 (auto); --inspect 1
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:39`

#### ENG-405 · مشروع أنيميشن جديد · New animation project (2D / 3D / lab) · 📄 موصوف
- **ماذا / what:** Scaffolds a deterministic HTML composition project in 2D, 3D or the product lab.
- **كيف / how:** From the studio: recipe 'new' (form in the الوصفات tab, POST /api/jobs {recipe:'new', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py new …`.
- **أرقام / params:** name film1; --seconds 8; --size 1080x1920|1920x1080|1080x1080|1080x1350; --title; --3d; --lab
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:57`

#### ENG-406 · مسودة سريعة · Fast draft render · 📄 موصوف
- **ماذا / what:** Renders a quick draft at half size and 15 fps for timing checks.
- **كيف / how:** From the studio: recipe 'preview' (form in the الوصفات tab, POST /api/jobs {recipe:'preview', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py preview …`.
- **أرقام / params:** project (dir); half size; 15 fps
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:62`

#### ENG-407 · تصيير الفيلم بمتصفحات متوازية · Parallel browser film render · 📄 موصوف
- **ماذا / what:** Renders an HTML composition through parallel headless browsers with optional motion blur and a render cache.
- **كيف / how:** From the studio: recipe 'render' (form in the الوصفات tab, POST /api/jobs {recipe:'render', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py render …`.
- **أرقام / params:** project; --engine studio|auto (default studio); --blur 4 (motion-blur samples); --workers 0 (auto); --out; --force
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:63`

#### ENG-408 · المراجعة: وضع التركيبة الحية · Review: live composition mode · 📄 موصوف
- **ماذا / what:** Instead of the MP4, a reel can load the real composition bundle so size/position edits render for real; a thin adapter makes the player look like a <video> element.
- **كيف / how:** reel.json 'live': 'bundle.js' → window.MotionOSLive(el) providing ref.current with seekTo(frame), getCurrentFrame(), isPlaying(), play(), pause(), setRate(), setBoxes(); liveVideo() wraps it.
- **أرقام / params:** frame = round(t × fps)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:508` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:986`

#### ENG-409 · المراجعة: تصدير MP4 بالتعديلات · Review: export MP4 with edits baked in · 📄 موصوف
- **ماذا / what:** The Export button re-renders the film with the user's edits applied and saves a new MP4 without overwriting the original; progress is read from the job log.
- **كيف / how:** POST /review/NAME/export {over, boxes} → job `kmotion review export NAME --props review/export-props.json`; GET polls {state, pct, line, out}; shown only when reel.export.cmd exists.
- **أرقام / params:** poll every 1 s; pct from the last 'n/N' in the log, capped at 99 until done
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:922` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:929`

#### ENG-410 · مواصفة خط زمني للمونتاج · Montage timeline spec (JSON) · 📄 موصوف
- **ماذا / what:** A declarative edit description: format, loudness target, grade preset, music with ducking, A-roll with zoom punches, B-roll overlay with crossfade, and word-split captions.
- **كيف / how:** templates/montage_spec.json documents the intended schema; no script in the repo consumes it yet, so Claude must translate it into ffmpeg filtergraphs (or a Remotion/HTML timeline) by hand.
- **أرقام / params:** 1080x1920, 30 fps, 15 s, -14 LUFS, music 112 BPM at -12 dB duck -18 dB; zoom punches {2.6 s x1.12 1.2 s},{6.0 x1.10 1.0},{9.5 x1.15 1.5}; B-roll 6.0-9.5 s crossfade 0.3 s
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/montage_spec.json`

#### ENG-411 · خريطة أدوات الفيديو · Video-tool landscape (500 tools / 33 integrations) · 📄 موصوف
- **ماذا / what:** Distilled catalogue of code-to-video frameworks (Remotion, Motion Canvas, Manim, MoviePy, Editly, Revideo, WebMotion...) and integrations (Blender, Spline, Rive, Meshy, Tripo, Lottie, Figma, Canva, Theatre.js, Babylon, PixiJS, Paper Shaders) with when to choose which.
- **كيف / how:** Read references/tools-catalog.md and tools-catalog-2.md when the house engine is not enough.
- **أرقام / params:** 22 direct, 254 adjacent, 224 complementary
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/references/tools-catalog.md` · `kosif-one/tools/kosif-studio/motion/references/tools-catalog-2.md`

#### ENG-412 · إعدادات التصدير · Export presets · 📄 موصوف
- **ماذا / what:** Encoder presets: web H.264, HEVC small, NVENC, HLS, image seq, GIF.
- **كيف / how:** Web libx264 crf 18-23 slow yuv420p +faststart aac 192k; libx265 crf 24 -tag:v hvc1; h264_nvenc preset p6 cq 20; HLS -g 60 -keyint_min 60 -sc_threshold 0 -hls_time 4; -framerate 30 -i f_%04d.png; GIF fps=12,scale=360:-1 palettegen/paletteuse.
- **أرقام / params:** see how
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### ENG-413 · خط زمني أصلي ونسخة عمل · Protected A / working B timelines · 📄 موصوف
- **ماذا / what:** Timeline A ordered by Date Recorded never touched; B = dated duplicate with 4 video + 4 audio named tracks (OVERLAY, GFX, SUBTITLE, AMBIENCE, SFX, MUSIC).
- **كيف / how:** Timeline.DuplicateTimeline(name) (v19+); idempotent track naming.
- **أرقام / params:** 4V+4A
- **الدليل / proof:** `100-superskills/skills/davinci-resolve-pipeline/SKILL.md` · `100-superskills/skills/davinci-resolve-pipeline/references/color-grading-order.md`

#### ENG-414 · عقد HyperFrames · HyperFrames composition contract (motion) · 📄 موصوف
- **ماذا / what:** data-composition-id root, one paused GSAP timeline in window.__timelines['root'], MOTION.shim; kit revealWords/hideWords, drawPath with head, rain/vapour/sparkle seeded, camera, flash, grain, vignette; banned dir=rtl on html, audio without id, fonts without @font-face, Math.random, setTimeout, marke…
- **كيف / how:** motion.py new/frames/check/render/measure (motion/ dir not present here)
- **أرقام / params:** 8-second gate
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md`

#### ENG-415 · سكربتات Python/Bash/PowerShell وأدوات CL · Automation Scripts & CLI Tools · 📄 موصوف
- **ماذا / what:** Owner-built skill "Automation Scripts & CLI Tools" (own words): workflow guidance for automation scripts & cli tools; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill automation-scripts-cli (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/automation-scripts-cli/SKILL.md`

#### ENG-416 · تشغيل المتصفح برمجياً للاختبار والجمع وا · Browser Automation (Playwright) · 📄 موصوف
- **ماذا / what:** Stable selectors, proper waits, saved sessions, screenshots -> headless capture of HTML animations frame-by-frame (used by the repo capture path, Edge headless).
- **كيف / how:** Load skill browser-automation-playwright (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/browser-automation-playwright/SKILL.md`

#### ENG-417 · حاوية ونشر مستمر لأي مشروع · Docker & CI/CD · 📄 موصوف
- **ماذا / what:** Owner-built skill "Docker & CI/CD" (own words): workflow guidance for docker & ci/cd; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill docker-ci-devops (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/docker-ci-devops/SKILL.md`

#### ENG-418 · ألعاب متصفح كاملة · Web Game Development · 📄 موصوف
- **ماذا / what:** Browser games with Canvas/Phaser/Three.js: game loop, state, input, simple physics, sound, localStorage save, touch -> same loop drives procedural animation frames for capture.
- **كيف / how:** Load skill game-dev-web (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/game-dev-web/SKILL.md`

#### ENG-419 · تسريع المواقع والتطبيقات والاستعلامات با · Performance Optimization · 📄 موصوف
- **ماذا / what:** Owner-built skill "Performance Optimization" (own words): workflow guidance for performance optimization; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill performance-optimization (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/performance-optimization/SKILL.md`

#### ENG-420 · كود Python إنتاجي · Python Pro · 📄 موصوف
- **ماذا / what:** Owner-built skill "Python Pro" (own words): workflow guidance for python pro; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill python-pro (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/python-pro/SKILL.md`

#### ENG-421 · كود TypeScript صارم لـ Node وBun وDeno · TypeScript & Node Pro · 📄 موصوف
- **ماذا / what:** Owner-built skill "TypeScript & Node Pro" (own words): workflow guidance for typescript & node pro; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill typescript-node-pro (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/typescript-node-pro/SKILL.md`

#### ENG-422 · ترميز NVENC · NVENC encode flags (vendored) · 📄 موصوف
- **ماذا / what:** Hardware encode recipe and loudnorm/subtitle filtergraphs.
- **أرقام / params:** -hwaccel cuda -c:v h264_nvenc -preset p7 -tune hq -rc vbr -cq 19
- **الدليل / proof:** `100-superskills/skills/video-editing-captions/references/sources.md:118`

#### ENG-423 · قواعد قابلية القفز · Seekability rules · 📄 موصوف
- **ماذا / what:** Only seekable animation sources; no wall clock or unseeded randomness; fromTo pitfalls.
- **كيف / how:** Use GSAP tweens, CSS animations (seeked via getAnimations), Lottie, Three.js adapters; MOTION.rng; drawPath uses set + immediateRender:false.
- **أرقام / params:** banned: setTimeout, requestAnimationFrame state, Math.random, network at render, getBoundingClientRect at tween time, will-change on camera-scaled nodes, tweening visibility/display on .clip, width/height/top/left tweens; repeat:-1 only under a finite duration
- **الدليل / proof:** `kosif-studio/motion/references/hyperframes-authoring.md` · `kosif-studio/motion/references/motion-craft.md`

#### ENG-424 · سياسة تشغيل المتصفح: GPU أو برمجي · GPU vs software WebGL launch policy · 📄 موصوف
- **ماذا / what:** Picks Chromium flags per page: real GPU through ANGLE/D3D11 on Windows, SwiftShader elsewhere, and --disable-gpu for pages that never touch WebGL (about 2x faster capture).
- **كيف / how:** page_flags(page) greps the HTML for webgl/three/K3/main.bundle/babylon/pixi; env HTML_RENDER_SOFTWARE=1, KOSIF_GPU=0/1, KOSIF_BROWSER; browser_path searches Edge/Chrome/Chromium and Playwright caches incl. /opt/pw-browsers.
- **أرقام / params:** flags --headless=new --hide-scrollbars --ignore-gpu-blocklist --autoplay-policy=no-user-gesture-required --allow-file-access-from-files
- **الدليل / proof:** `kosif-studio/html_render.py:26` · `kosif-studio/html_render.py:35` · `kosif-studio/html_render.py:55`

#### ENG-425 · تكبير دقة الإخراج · Supersampled output (--scale) · 📄 موصوف
- **ماذا / what:** Device scale factor multiplies output pixels (width*scale x height*scale), e.g. 2x for crisp downscales.
- **كيف / how:** --scale 2
- **أرقام / params:** default 1; min 0.1
- **الدليل / proof:** `kosif-tool/tools/render_html.cjs:99`

#### ENG-426 · خيار التقنية: three · Stack option: three · 📄 موصوف
- **ماذا / what:** Request phrase for stack 'three': Three.js real 3D scene with moving camera.
- **كيف / how:** --stack three
- **الدليل / proof:** `kosif-tool/tools/kosif.py:43` · `kosif-tool/web/generator.js`

#### ENG-427 · المعاينة قبل الرندر · Preview-before-render gate · 📄 موصوف
- **ماذا / what:** User approves a contact sheet and short motion clip before full render.
- **كيف / how:** render_html --preview (8 labelled frames); half-res 2–4 s clip.
- **أرقام / params:** 8 frames; clip 2–4 s at half resolution (540×960)
- **الدليل / proof:** `kosif-tool/playbooks/render-pipeline.md:9` · `kosif-tool/playbooks/render-pipeline.md:17-19`

#### ENG-428 · لا تسجيل شاشة للتسليم · No screen recording for delivery · 📄 موصوف
- **ماذا / what:** Screen capture drops frames and is not reproducible.
- **الدليل / proof:** `kosif-tool/playbooks/render-pipeline.md:34`

#### ENG-429 · قواعد الرندر الحتمي · Render determinism checklist · 📄 موصوف
- **ماذا / what:** frame=f(t), seeded randomness, fonts loaded before frame 0 (window.__kosifReady), no network assets at render, fixed viewport/DPR.
- **الدليل / proof:** `kosif-tool/playbooks/render-pipeline.md:36` · `kosif-tool/playbooks/render-pipeline.md:83`

#### ENG-430 · مسارات المتصفح في الجهاز السحابي · Cloud machine browser paths · 📄 موصوف
- **ماذا / what:** Use preinstalled Playwright and Chromium; never run playwright install; Remotion uses headless_shell.
- **كيف / how:** /opt/node-tools/node_modules/playwright; /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell
- **الدليل / proof:** `kosif-tool/playbooks/render-pipeline.md:38`

#### ENG-431 · التسليم القياسي بست خطوات · Standard 6-step delivery · 📄 موصوف
- **ماذا / what:** preview PNG → motion check clip → approval → final render with audio → verify_video gate → TEST_REPORT.
- **كيف / how:** Commands in render-pipeline recipe A.
- **أرقام / params:** check clip --start 4 --duration 3 --width 540 --height 960
- **الدليل / proof:** `kosif-tool/playbooks/render-pipeline.md:44-53`

#### ENG-432 · ترميز يدوي من الإطارات · Manual ffmpeg encode from frames · 📄 موصوف
- **ماذا / what:** Encode PNG frames + voice to MP4.
- **كيف / how:** ffmpeg -framerate 30 -i frames/frame_%06d.png -i voice.mp3 -c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow -movflags +faststart -c:a aac -b:a 192k -shortest out/film.mp4
- **الدليل / proof:** `kosif-tool/playbooks/render-pipeline.md:71-75`

#### ENG-433 · وضع brag-slim · brag-slim single-file mode · 📄 موصوف
- **ماذا / what:** Model builds whole video with local tools from a project or URL; no bundled assets.
- **كيف / how:** Follow slim.md; work/ subfolder for intermediates.
- **أرقام / params:** 1920x1080 / 1080x1920 / 1080x1080, 30fps, ~20s
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/slim.md` · `kosif-one/vendor/brag/skills/brag-slim/SKILL.md`

#### ENG-434 · ترميز مناسب للسحب · Scrub-friendly encode · 📄 موصوف
- **ماذا / what:** Native res, crf 20, GOP 8, unsharp, no audio, faststart; mobile 720w GOP 4 crf 23.
- **كيف / how:** ffmpeg -an -vf unsharp=5:5:0.8:5:5:0.0 -c:v libx264 -preset slow -crf 20 -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart
- **أرقام / params:** ~8 MB per 8 s vs 25 MB all-intra
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/references/pipeline.md:126` · `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md:523`

#### ENG-435 · عرض حتمي إطار بإطار · Deterministic render(t) capture · 💡 فكرة
- **ماذا / what:** Pure function of time captured by headless browser, ffmpeg mux.
- **كيف / how:** Puppeteer/Playwright frame stepping; seeded random; no rAF/CSS transitions.
- **الدليل / proof:** `style:pm-xelandre-363f00`

## إضافات من Cinematic Director PRO v5

_مستخلصة من حزمة المالك KOSIF Claude Cinematic Director PRO v5 (انظر [cinematic-director-pro.md](../cinematic-director-pro.md)). مسارات الدليل `owner-upload:` تشير إلى ملفات داخل أرشيف المالك، لا إلى هذا المستودع._

#### ENG-P01 · مخطط المشهد المصغّر CineGraph: JSON إلى MP4 بأنبوب مباشر · CineGraph mini scene graph: JSON → Pillow frames → ffmpeg rawvideo pipe · ✅ مُثبت هنا / proven here
- **ماذا / what:** مواصفة JSON صغيرة (عرض، ارتفاع، fps، مدة، خلفية، عناصر) تتحول إلى فيديو H.264 بحساب كل إطار من الزمن المطلق، وتُضخ البكسلات إلى ffmpeg عبر stdin بلا ملفات PNG وسيطة. / A small JSON spec becomes H.264 by computing every frame from absolute time and streaming RGB24 bytes into ffmpeg stdin — no intermediate PNGs.
- **كيف / how:** Element types text/line/box/ring/bars; easings linear, ease_out_cubic, spring_pop (1−e^(−7t)·cos 12t). Each element animates over the first third of its life: progress = ease(min(1, 3·(t−start)/duration)); text scales from 0.5× and rises 35 px; ring draws an arc −90°→+270°; bars grow in a stagger (progress·n − k). Arabic text gets direction="rtl" through Pillow RAQM. The validator rejects odd sizes, >3840 px, fps outside 1–60, >10,800 frames, >100 elements, text >300 chars and non-normalised x/y. ffmpeg: -f rawvideo -pix_fmt rgb24 -i - -c:v libx264 -preset veryfast -crf 23 -pix_fmt yuv420p +faststart; optional --audio muxes AAC 160k with -shortest. Re-ran here: 480×854, 24 fps, 4.000 s in 1.7 s wall time. Honest limits seen on the decoded frame at 2.5 s: the BARS block grows up into the second title (layout bug in the sample spec) and only DejaVu is found here (no Noto Sans Arabic), yet the words joined correctly. Full-frame renderer only — no alpha overlay over footage. **أرقام / params:** 480×854 · 24 fps · 4 s · crf 23 · bounds 96–3840 px, ≤10,800 frames, ≤100 elements
- **الرخصة / license:** owner package (own work)
- **الدليل / proof:** `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/tools/kosif_scene_graph.py` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/templates/example_scene.json` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/examples/CineGraph_Arabic_Intro.mp4` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/references/CINEGRAPH_CINECLAUDE_REVIEW.md`

## إضافات v2 — v2 additions

_قدرات أُضيفت في الإصدار الثاني من حزم المالك (higgsfield-motion-saas وhiggsfield-motion-claude ومهارة المونتاج التحريرية وفيلم الأغنية وKOSIF SEE) ومن مهارات ECC (رخصة MIT)، مكتوبة بكلماتنا. ✅ هنا = شُغّلت في جلسة 2026-10-16 وسجلها في [external-skills.md](../external-skills.md)؛ مسارات `owner-upload:` تشير إلى أرشيفات المالك لا إلى هذا المستودع. — v2 additions from the owner's packages and ECC skills (MIT), in our own words; ✅ = run in this session, log in external-skills.md; `owner-upload:` paths point into the owner's archives, not this repo._

#### ENG-X01 · ضبابية حركة تكيفية · Adaptive motion-blur sample count (180° shutter) · 📄 موصوف / documented only
- **ماذا / what:** عدد الإطارات الفرعية لكل إطار يتحدد بمقدار الحركة فيه، والإطارات الفرعية لا تعبر قطعًا حادًا أبدًا. — The number of sub-frames per frame follows how much moves in it, and sub-frames never straddle a hard cut.
- **متى أستخدمها / when:** رندر نهائي لفيلم فيه سوط أو زوم سريع — a final render of a film with whips or fast zooms.
- **كيف / how:** 180° shutter centred: sub-frame k of N at t = (n + 0.5·((k+0.5)/N − 0.5))/fps (N = 4 → offsets −0.1875, −0.0625, +0.0625, +0.1875 frame). Adaptive: luma difference between t−½ and t+½ frame at ¼ resolution; n = 1 if diff < 0.5, else clamp(3 + 1.6·diff, 5, 14), rounded up; ≥ 6 for rolling objects. Clamp sub-frames at hard cuts (the film publishes its hard-cut times); quantise discrete events. Four fixed sub-frames look cheap; masters with 8 sub-frames and shutter 0.5 cost about 20 s of render per film second. Extends ENG-349. **أرقام / params:** n = 1 | clamp(3 + 1.6·diff, 5, 14); ≥ 6 rolling; no straddled cuts.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/code-engine.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/code-engine.md`

#### ENG-X02 · عمال رندر متداخلون وبوابة استمرار · Interleaved render workers and a continuity gate · 📄 موصوف / documented only
- **ماذا / what:** وزّع الإطارات على العمال بالتناوب لا بكتل متصلة، وارفض الترميز إن نقص إطار واحد. — Deal frames to workers round-robin rather than in contiguous chunks, and refuse to encode if a single frame is missing.
- **متى أستخدمها / when:** رندر فيلم طويل أو ثقيل على عدة عمليات متصفح — rendering a long or heavy film on several browser processes.
- **كيف / how:** Worker i renders frames i, i+N, i+2N… (--from i/fps --every N) so heavy scenes are shared evenly: 3:09 versus 5:18 for contiguous chunks on the same film. Before encoding, check the frame sequence is complete (no gaps) and stop otherwise. Bitrate 24–30 Mbps for 1080p30 (15 s ≈ 45–57 MB). Serialize heavy renders and kill only your own browser processes. **أرقام / params:** interleave by N; 24–30 Mbps @1080p30.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/code-engine.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/scripts/code/render_film.sh` · `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/code-engine.md`

#### ENG-X03 · أخطاء رندر دُفع ثمنها · Render bugs already paid for · 📄 موصوف / documented only
- **ماذا / what:** قائمة أعطال حقيقية في التقاط المتصفح والرندر بالبايثون مع علاجها، تُفحص قبل أي رندر كبير. — Real failures in browser capture and Python rendering with their fixes, to check before any big render.
- **متى أستخدمها / when:** قبل رندر متوازٍ أو نهائي — before a parallel or final render.
- **كيف / how:** One DevTools port per parallel capture (shared ports mixed scenes); document.fonts.ready resolves before unused faces load → force-load every face (7–20 px layout drift otherwise); measuring a display:none element returns 0; browser profiles fill the disk (ENOSPC) → clean temp profiles; ProcessPool code needs an `if __name__ == '__main__'` guard; relative output paths silently lose the MP4; file:// taints canvas → `--allow-file-access-from-files`; a grain tile in a pooled canvas is cleared on reuse; SDF squash without rescaling distance becomes a blob; clip-path: inset() cuts glyph tops → negative insets −20…−60 %; Pillow floodfill on an array-backed image is a no-op → .copy() first; set globalAlpha by multiplying, not assigning. For offline determinism vendor fonts and libraries instead of loading them from a CDN. **أرقام / params:** negative clip insets −20…−60 %; one port per worker.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/code-engine.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/code-engine.md` · `owner-upload:KOSIF_SEE_Humanizer_Optimize_Graphify_v1.7.5/skills/kosif-media-motion/SKILL.md`

#### ENG-X04 · خط رندر فيلم الأغنية · Song-film render pipeline (seek → JPEG → ffmpeg, song untouched) · 📄 موصوف / documented only
- **ماذا / what:** فيلم أغنية كامل من ملف canvas واحد: المتصفح يقفز إلى كل زمن، يصدّر صورة، وffmpeg يرمّز، ثم تُدمج الأغنية دون تعديل. — A full song film from one canvas file: the browser seeks each time, exports an image, ffmpeg encodes, and the song is muxed unchanged.
- **متى أستخدمها / when:** فيلم كلمات أو موسيقى مرسوم بالكامل بالكود — a lyric or music film drawn entirely in code.
- **كيف / how:** Playwright evaluates seek(t); canvas.toDataURL('image/jpeg', 0.9) for each frame (wait for window.FILM_READY); pipe MJPEG into `ffmpeg -c:v libx264 -crf 16 -pix_fmt yuv420p`; N worker chunks joined with the concat demuxer (-c copy); mux the song with `-c:a aac -b:a 256k -ar 48000 -shortest -movflags +faststart`. Test frames first (`render.py frames 3,10.5`) and a 4-column contact sheet. Lesson: contiguous chunks are unbalanced, interleave instead (ENG-X02). The owner's film: 1080×1920, 30 fps, 56.92 s, 8 scenes. **أرقام / params:** JPEG q 0.9 → crf 16; AAC 256k 48 kHz.
- **الرخصة / license:** owner (song audio and lyrics are third-party; not included)
- **المصدر / source:** `owner-upload:film_project/film/render.py`
- **الدليل / proof:** `owner-upload:film_project/film/render.py` · `owner-upload:film_project/film/sheet.py` · `owner-upload:film_project/film/README_AR.md`

#### ENG-X05 · قائمة قواعد Remotion · Remotion rule checklist · 📦 بأمر تثبيت / one install
- **ماذا / what:** خريطة مختصرة لما يجب معرفته قبل بناء فيديو بـRemotion: من التركيب والتوقيت إلى الترجمات والانتقالات والقياس. — A short map of what to know before building a Remotion video: from compositions and timing to captions, transitions and measurement.
- **متى أستخدمها / when:** حين يكون Remotion هو المحرك المختار — when Remotion is the chosen engine.
- **كيف / how:** Rule topics: compositions, sequencing, timing (spring/easing), animations, text animations, transitions, trimming, videos, audio, assets, fonts, gifs, lottie, charts, 3D via React Three Fiber, tailwind, measuring text (fit and overflow), calculate-metadata, media helpers (can-decode, extract frames, audio/video duration and dimensions), display captions (pages with word highlight), import SRT, transcribe captions. Check Remotion's licence: some companies need a paid licence.
- **تثبيت / install:** `npx create-video@latest`
- **الرخصة / license:** MIT (ECC, (c) 2026 Affaan Mustafa); Remotion has its own licence
- **المصدر / source:** `https://github.com/affaan-m/ECC/tree/main/skills/remotion-video-creation/SKILL.md`
- **الدليل / proof:** `https://github.com/affaan-m/ECC/tree/main/skills/remotion-video-creation/SKILL.md`
