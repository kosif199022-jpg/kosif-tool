# الموشن والمونتاج والسينما — Motion & video editing (`motion`)

> مكتبة بروتوكول USIP v5.5، مولّدة بـ `scripts/smart_capabilities.py library` من `data/powers/*.json` و`data/tools.json`؛ لا تُحرَّر يدويًا. الدليل: [A28 اختيار القدرات](../protocol/A28-capability-routing.md) · [الفهرس](INDEX.md) · [النواة](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

## الفهرس / contents

- [متى تستخدم هذه المجموعة / when](#متى-تستخدم-هذه-المجموعة--when)
- [الحالة بالأرقام / status](#الحالة-بالأرقام--status)
- [الأدوات القابلة للتشغيل / runnable tools](#الأدوات-القابلة-للتشغيل--runnable-tools)
- [العائلات / families](#العائلات--families)
- [كل القدرات / every power](#كل-القدرات--every-power)

## متى تستخدم هذه المجموعة / when

كلمات التوجيه: video film montage edit scene camera animation cut transition character motion فيديو مونتاج تحريك كاميرا مشهد انتقالات

خط العمل المقترح (هدف تصميم، لم يُختبر كوحدة واحدة): القصة والستوريبورد → التوقيت والكاميرا → التحريك والمونتاج → التصدير

العضوية في المجموعة تصنيف للتوجيه، لا دليل على أن القدرات تعمل معًا: اربطها بخط عمل مختبر فقط.

## الحالة بالأرقام / status

| الحالة | العدد | المعنى |
|---|---:|---|
| `proven` | 117 | ✅ proven: a proof exists in the catalog; still check its requirements here before calling it ready |
| `ready` | 180 | 🟢 ready: runnable without setup according to the catalog |
| `documented` | 269 | 📄 documented: a described method; needs building or wiring before it runs |
| `seen` | 292 | 👁 seen: observed in a reference or demo, not executed here |
| `install` | 314 | 📦 install: needs a package, binary or model first |
| `key` | 23 | 🔑 key: needs an account, key or paid service (ask before any spend) |
| `idea` | 33 | 💡 idea: not built |
| **المجموع** | **1,228** | |

## الأدوات القابلة للتشغيل / runnable tools

| الأداة | ما تفعله | ابدأ بـ | الدليل |
|---|---|---|---|
| `aspects` | محلّل نِسَب أبعاد الفيديو | `python3 -c "import sys; sys.path.insert(0,'scripts'); import aspects; print(aspects.resolve('2.35:1'))"` | tested-here |
| `atlas-render` | رندر أفلام الشرح: ستوريبورد وفحص حتمية وMP4 حقيقي بصوت مُركّب | `python3 scripts/atlas_render.py check` | tested-here |
| `blender-bridge` | جسر Blender الآمن | `python3 scripts/blender_bridge.py doctor` | tested-here |
| `blender-cinema` | رندر سينمائي بـBlender Cycles | `python3 scripts/blender_cinema.py doctor` | tested-elsewhere |
| `blender-cinematic-bridge` | دمج رندر Blender Cycles مع مونتاج KOSIF والصوت | `python3 scripts/blender_cinematic_bridge.py doctor` | tested-here |
| `character-fullbody` | تحريك الشخصية بكامل الجسم | `python3 scripts/character_fullbody.py doctor` | tested-here |
| `character-ik` | تحريك ذراع الشخصية بالحركية العكسية | `python3 scripts/character_ik.py doctor` | tested-here |
| `cinematic-broll-render` | تصيير لقطات B-roll بحركة كاميرا | `python3 scripts/cinematic_broll_render.py --edl ./edl.json --manifest ./clips.json --audio ./voice.wav --out ./out/master.mkv --width 1080 --height 1920` | tested-here |
| `cinematic-cut-planner` | مُخطِّط قطعات اللقطات الحقيقية | `python3 scripts/cinematic_cut_planner.py --words ./words.json --clips ./clips.json --duration 48.5 --fps 30 --out ./out/edl.json` | tested-here |
| `code-drawing-master` | رسم الشخصيات والمشاهد بالكود | `python3 scripts/code_drawing_master.py --cast human+cat --expression happy --location street --action walk --out ./story.json --html ./story.html` | tested-here |
| `creative-paint` | الرسم الإبداعي بالطبقات | `python3 scripts/creative_paint.py doctor` | tested-here |
| `creative-principles` | دراسة الرسم التدريجي والظل الأصلي | `python3 scripts/creative_principles.py construct --input original-shapes.json --out-prefix out/stage` | tested-elsewhere |
| `creative-quality-gate` | بوابة جودة خطة المونتاج | `python3 scripts/creative_quality_gate.py ./my-project/src/plan.json --out ./out/quality-audit.json` | tested-here |
| `creative-reasoning-bridge` | جسر الصوت إلى لوحة القصة | `python3 scripts/creative_reasoning_bridge.py ./cues.json --style auto --out ./out/scene.json --report ./out/decision.json` | tested-here |
| `drawing-academy` | أكاديمية الرسم والدروس المبنية على مصادر | `python3 scripts/drawing_academy.py index` | tested-elsewhere |
| `drawing-council` | مجلس خبراء الرسم: أحد عشر خبيرًا من بطاقات الكتب الـ48 يراجعون الصورة قبل إرسالها | `python3 scripts/drawing_council.py roster --markdown` | tested-here |
| `drawing-methods` | أطلس مناهج كتب الرسم مع رسم بنائي بالطبقات | `python3 scripts/drawing_methods.py find "ارسم وش شخصية بتضحك"` | tested-here |
| `drawing-visual-qa` | مدرب الرسم من فصول الكتب والتشخيص البصري المستقل | `python3 scripts/drawing_visual_qa.py curriculum "ارسم شخصية كرتونية بمنظور وإضاءة" --out out/lessons.json` | tested-here |
| `dua-wednesday` | دعاء يوم الأربعاء — محرك ريل دعاء موشن جرافيك 9:16 | `python3 scripts/dua_wednesday.py doctor` | tested-here |
| `fetch-reference` | جلب المرجع المسموح وقياسه | `python3 scripts/fetch_reference.py https://example.com/page --list --json` | tested-here |
| `fetch-video` | تنزيل الفيديو من الروابط للمونتاج | `python3 scripts/fetch_video.py --doctor` | tested-elsewhere |
| `kosif-timeline` | محرر KOSIF Timeline: مونتاج متعدد المسارات مع تراجع وإعادة | `python3 scripts/kosif_timeline.py doctor` | tested-here |
| `kosif-timeline-demo` | تجربة مونتاج KOSIF Timeline تلقائية بملفات أصلية مولدة | `python3 scripts/kosif_timeline_demo.py --dir ./fresh-kosif-timeline-demo` | tested-here |
| `media-sources` | بوابة الوسائط المرخّصة | `python3 scripts/media_sources.py list` | tested-here |
| `mimic` | محرك محاكاة الفيديو المرجعي | `python3 -c "import sys; sys.path.insert(0,'scripts/mimic'); import mm_analyze; mm_analyze.analyze('./in.mp4','./work')"` | tested-here |
| `montage-pro` | فريق مونتاج برو (صوت أو فيديو إلى مونتاج أو موشن) | `python3 scripts/montage_pro.py doctor` | tested-here |
| `motion-engine-js` | محرك حركة SVG | `python3 scripts/motion_director.py compile ./scene.json --out ./out/film.html` | tested-here |
| `motion-reference-probe` | فاحص توقيت الفيديو المرجعي | `python3 scripts/motion_reference_probe.py ./in.mp4` | tested-here |
| `motion-toolkit` | مكتبة رياضيات الحركة | `node --input-type=module -e "import {ease, timeCode} from './resources/motion-runtime/motion_toolkit.mjs'; console.log(ease(0.5,'cubic'), timeCode(2.5,30))"` | tested-here |
| `music-rhythm-engine` | فرضيات إيقاع الموسيقى | `python3 scripts/music_rhythm_engine.py ./out/cues.json --out ./out/rhythm.json` | tested-here |
| `native-glb` | مُصدِّر GLB مستقل عن Blender | `python3 scripts/native_glb.py --scene templates/blender-demo.json --output ./out/scene.glb` | tested-here |
| `perspective-color-lab` | منظور هندسي ومقاييس التباين اللوني | `python3 scripts/perspective_color_lab.py perspective --input scene.json --out out/scene.svg` | tested-elsewhere |
| `portrait-pipeline` | رسم يدوي المظهر بالرصاص أو الفحم أو الحبر لأي صورة أو مشهد متخيَّل، خطًا بخط | `python3 scripts/portrait_pipeline.py draw --photo photo.png --out out/portrait --models <dir with face_landmarker.task and selfie_multiclass.tflite>` | tested-here |
| `reel-factory` | مصنع الريلز: صوت وتوقيت كلمات ولقطات مرخصة ← ريلز 9:16 مفحوص | `python3 scripts/reel_factory.py plan --audio ./voice.m4a --audio-rights owned --words ./words.json --shots-manifest ./stock/manifest.json --shot-ids 17928486,8165467,20382699 --title "دعاء يوم الخميس" --handle @kosif` | tested-here |
| `reference-edit-engine` | محرك إعادة بناء المونتاج المرجعي | `python3 scripts/reference_edit_engine.py --probe ./cuts.json --out ./new-edit` | tested-here |
| `reference-visual-fingerprint` | البصمة البصرية للفيديو المرجعي | `python3 scripts/reference_visual_fingerprint.py ./in.mp4 --probe ./cuts.json --out ./reference-look.json` | tested-here |
| `render-html` | محوّل HTML إلى فيديو MP4 | `node resources/motion-runtime/render_html.cjs --in ./film.html --out ./out/film.mp4 --fps 30 --audio ./voice.wav` | tested-elsewhere |
| `repo-ashell-cinema` | استوديو التنزيل Cinema C للآيفون | `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh "https://www.youtube.com/watch?v=VIDEO_ID"` | tested-elsewhere |
| `repo-aspects` | محلّل نسب العرض المرن | `python3 -c "import sys; sys.path.insert(0,'tools'); from aspects import resolve; print(resolve('2.35:1'))"` | tested-here |
| `repo-build` | مولّد ملفات أطلس الأساليب | `python3 tools/build.py` | untested |
| `repo-import-briefs` | استيراد الملفات الإبداعية | `python3 tools/import_briefs.py ./briefs/` | untested |
| `repo-kosif` | أداة سطر أوامر لأطلس أنماط KOSIF | `python3 tools/kosif.py list --category charts --limit 10` | tested-here |
| `repo-render-html` | محوّل حتمي من HTML إلى فيديو MP4 | `node tools/render_html.cjs --in starters/html-canvas/index.html --out ./out/film.mp4 --fps 30 --audio ./voice.mp3` | tested-elsewhere |
| `repo-verify-video` | بوابة فحص تسليم الفيديو | `python3 tools/verify_video.py ./out/film.mp4 --aspect 9:16 --fps 30 --duration 12 --audio ./voice.mp3 --json ./out/report.json` | tested-here |
| `starter-html-canvas` | قالب فيلم HTML Canvas | `python3 tools/kosif.py scaffold kinetic-arabic ./my-film --starter html-canvas` | tested-elsewhere |
| `stock-fetch` | تحميل لقطات مجانية بلا مفتاح (Pexels وMixkit) | `python3 scripts/stock_fetch.py probe` | tested-here |
| `stream-grabber` | ملتقط بث DASH وHLS للمونتاج | `python3 scripts/stream_grabber.py find ./saved-page.html` | tested-here |
| `style-atlas-bridge` | أطلس الأساليب الكامل (86 طريقة): بحث وتوليف وموجز إنتاج وهيكل مشروع شرح | `python3 scripts/style_atlas_bridge.py families` | tested-here |
| `unified-cinematic` | السينما الموحدة: مونتاج الفيديو مع الصوت وحركة الكاميرا | `python3 scripts/unified_cinematic.py doctor` | tested-here |
| `verify-video` | بوابة فحص تسليم الفيديو | `python3 scripts/verify_video.py ./in.mp4 --aspect 9:16 --fps 30 --duration 15 --json ./out/report.json` | tested-here |
| `video-workflow-bridge` | جسر سير عمل الفيديو | `python3 scripts/video_workflow_bridge.py paper-edit templates/ik-wave-words.json --keep "1-3,5" --fps 30 --out ./out/paper-edit.json` | tested-here |

الأوامر نسبية إلى مجلد المهارة (أو جذر المستودع لأدوات `tools/`)؛ `python3 scripts/hub.py tool <id>` يعطي كل الأوامر والمتطلبات والحدود.

## العائلات / families

| العائلة | القدرات | الفصل |
|---|---:|---|
| `camera-composition-layout` | 425 | [camera-composition-layout.md](../powers/camera-composition-layout.md) |
| `characters-rigs` | 51 | [characters-rigs.md](../powers/characters-rigs.md) |
| `easing-timing-rhythm` | 102 | [easing-timing-rhythm.md](../powers/easing-timing-rhythm.md) |
| `formats-platforms` | 70 | [formats-platforms.md](../powers/formats-platforms.md) |
| `story-direction-ideas` | 95 | [story-direction-ideas.md](../powers/story-direction-ideas.md) |
| `transitions-cuts` | 474 | [transitions-cuts.md](../powers/transitions-cuts.md) |
| `video-download` | 11 | [video-download.md](../powers/video-download.md) |

## كل القدرات / every power

مرتبة بالحالة ثم العائلة ثم المعرّف. `hub.py` و`skill_intelligence.py deep <ID>` يعطيان بطاقة القدرة كاملة بدليلها.

| المعرّف | الاسم | English | الحالة | المتطلبات |
|---|---|---|---|---|
| `CAM-01` | مسار تكبير لوغاريتمي | Log-space zoom track | proven |  |
| `CAM-02` | هيكل مساحة عمل بثلاثة أعمدة | Three-column RTL workspace shell | proven |  |
| `CAM-03` | تخطيط بخصائص منطقية للاتجاه | RTL logical-property layout | proven |  |
| `CAM-04` | تخطيط حسب المقاس | Aspect-specific kinetic layout | proven |  |
| `CAM-05` | تدرج أحجام اللقطات | Stickman shot-size progression | proven | node |
| `CAM-06` | تغطية بعدستين 35/85 | Two-lens emotional coverage (35/85 mm) | proven |  |
| `CAM-07` | كاميرا طعام ثابتة 45° | Locked 45° food macro camera | proven |  |
| `CAM-08` | مفاتيح الكاميرا | Camera keys (smoothstep) | proven |  |
| `CAM-09` | بارالاكس متعدد الطبقات مع اقتراب | Multi-plane SVG parallax with push-in | proven |  |
| `CAM-10` | وضع النص بعيداً عن الوجه ضمن الحدود الآمنة | Safe-area and face-aware text placement | proven |  |
| `CAM-11` | مفردات حركة الكاميرا | Camera-move vocabulary + one-move rule | proven |  |
| `CAM-12` | ترتيب النص الآمن حول الوجه | Text-safe layout stack | proven |  |
| `CAM-13` | كاميرا ثنائية الأبعاد بمفاتيح | Keyframed 2D camera (cameraAt/applyCamera) | proven |  |
| `CHAR-05` | بايبلات شخصيات fastify | Fastify character bibles & reference locks | proven |  |
| `CHAR-11` | أطراف بـ IK بعظمتين | Two-bone IK limbs | proven |  |
| `CHAR-13` | وجوه بتبديل الأشكال | Swap-shape faces, mouths & expressions | proven |  |
| `CHAR-15` | الشخصية في إطارها المحلي | Character built in its own local frame | proven | pip:pillow |
| `CHAR-24` | دورة المشي بلا انزلاق | Walk cycle without foot sliding | proven |  |
| `CHAR-25` | ساق مشي إجرائية | Procedural walk-cycle leg | proven | chromium |
| `CHAR-26` | آلة حالات الوضعية | Keyframed pose state machine | proven |  |
| `CHAR-29` | لحظة رد الفعل والقفزة | Reaction & jump recipe | proven |  |
| `CHAR-35` | الشخصية العربية وفقاعة كلامها | RTL staging & Arabic speech bubble | proven | fonts:arabic |
| `CHAR-37` | حركة ثانوية بالنوابض والسلاسل | Spring & chain secondary motion | proven | python3 |
| `CHAR-38` | فراشة ويراعة مرافقة | Winged companions (butterfly, firefly) | proven |  |
| `CHAR-40` | الأرنب القطيفة المنحوت | SDF plush bunny (rigged) | proven |  |
| `EASE-01` | كل شيء دالة للزمن | Everything is a function of t | proven | python3, chromium, npm:three, npm:gsap |
| `EASE-02` | حساب الإطارات بنطاق نصف مفتوح | Half-open frame arithmetic | proven | ffmpeg, python3 |
| `EASE-04` | مقسّم المشاهد التلقائي | Auto beat-count storyboard splitter | proven |  |
| `EASE-05` | تقدير المدة من سرعة الكلام وخرائط المقاطع | Word-pace estimator & clip beat maps | proven |  |
| `EASE-09` | رموز التسارع حسب الدور (17 منحنى) | Role-based easing tokens MOTION.E | proven | npm:gsap |
| `EASE-11` | دوال تسهيل بلا مكتبات | Dependency-free easing set | proven | imagemagick, npm:remotion |
| `EASE-12` | رموز حركة CSS مختبرة | Tested CSS motion tokens | proven |  |
| `EASE-16` | زووم لوغاريتمي ثابت الإحساس | Log-space zoom (logEase, lmix, zoomTrack) | proven | npm:remotion |
| `EASE-22` | نوابض فيزيائية مغلقة الصيغة SPR | Physical springs SPR (closed form) | proven |  |
| `EASE-23` | نوابض مطبّعة كمنحنيات GSAP | Normalised spring eases | proven | npm:gsap |
| `EASE-24` | قيمة تتبع أهدافًا بنابض | Retargetable spring track | proven |  |
| `EASE-30` | القفزة النابضة للدخول | Spring pop entrance | proven | npm:gsap, npm:hyperframes |
| `EASE-34` | تتابع CSS بالترتيب | CSS index-stagger cascades | proven |  |
| `EASE-40` | مدة حسب المسافة | Distance-based duration durFor | proven |  |
| `EASE-48` | مفاتيح مأخوذة من دالة | Function-sampled keyframes | proven | npm:gsap |
| `EASE-51` | غلاف الضربة hitPulse | Hit pulse envelope | proven |  |
| `EASE-60` | حدود السرعة بالبكسل لكل إطار | Speed limits in px/frame | proven | python3 |
| `EASE-73` | قالب العد التنازلي | Countdown template | proven | python3, npm:gsap |
| `EASE-75` | منحدرات سرعة بتكامل دقيق | Exact speed ramps | proven | npm:remotion |
| `EASE-84` | التحويل والشفافية فقط | Transform/opacity-only contract | proven |  |
| `EASE-86` | حركات طبقات الاستوديو | Studio layer entrances & opacity envelope | proven | node |
| `EASE-X01` | نموذج شكل السرعة | Speed-shape model (r = speed ÷ mean speed) | proven |  |
| `EASE-X02` | إبرة السرعة على القطع | Needle ease: the speed peak lands on the cut | proven |  |
| `EASE-X03` | سرعة نسبية متطابقة عبر القطع | Match relative speed across a cut (rho) | proven |  |
| `EASE-X04` | تتابع متداخل بلا توقف | Relay overlap: start the next move at 0.45 | proven |  |
| `EASE-X05` | زوج منحنيين بميل متساوٍ عند القطع | Equal-slope curve pair across a cut | proven |  |
| `EASE-X09` | نابض بارتداد واحد ومفاتيح بمنحنى الوصول | One-overshoot spring and arriving-key ease tracks | proven | python3 |
| `FMT-02` | جدول المقاسات الموحد في أدواتك | Aspect presets across the owner tools | proven | python3 |
| `FMT-03` | الإطار السينمائي العريض والأشرطة | Cinematic 2.35/2.39:1 and letterbox bars | proven |  |
| `FMT-08` | المنطقة الآمنة في الإطار العمودي | 9:16 UI safe zone | proven |  |
| `FMT-13` | إعادة تأطير ذكية حول الوجوه | Smart reframe around faces | proven | pip:mediapipe, pip:ultralytics |
| `FMT-14` | الصورة الكاملة فوق نسختها الضبابية | Full frame over its blurred fill | proven | npm:hyperframes |
| `FMT-20` | ماستر H.264 آمن للويب | Web-safe H.264 master | proven | ffmpeg, python3 |
| `FMT-22` | فيديو بقناة شفافة | Alpha video: WebM VP9 & ProRes 4444 | proven | npm:remotion, npm:hyperframes |
| `FMT-24` | سلم جودات HLS | Multi-rendition HLS ladder | proven | ffmpeg |
| `FMT-31` | ملف مفحوص لكل منصة | Checked per-platform delivery (8 platforms) | proven | python3 |
| `FMT-32` | حزمة التسليم: كل النسب وغلاف وGIF | Delivery pack: all ratios + poster + GIF/WebP | proven | python3 |
| `FMT-33` | حزمة نشر مفحوصة لكل منصة | Post pack + linter per platform | proven | python3 |
| `FMT-34` | جدول حدود المنصات (2026-10) | Platform limits table (as of 2026-10) | proven | python3 |
| `FMT-42` | استوديو كامل كصفحة claude.ai واحدة | KOSIF Studio Cloud — one-page artifact | proven | python3, claude:tools |
| `FMT-44` | الغلاف كإطار أول | Poster picked and baked as frame 0 | proven | python3 |
| `FMT-59` | فصول يوتيوب من العلامات | YouTube chapters from markers | proven | ffmpeg |
| `FMT-62` | حلقة متصلة بلا قطع | Seamless loop (video + GIF) | proven | ffmpeg |
| `FMT-63` | قالب بطاقة الختام | End-card template | proven | python3, npm:gsap |
| `STORY-02` | موجّه الطلب الواحد (16 مسارًا) | One-request router (16 routes + add-ons) | proven | python3 |
| `STORY-03` | مخطط اللقطات الحتمي ProPlan | Deterministic shot planner (ProPlan) | proven | python3 |
| `STORY-04` | مولّد طلب Claude من الأسلوب | Style → Claude request generator | proven | python3, npm:remotion |
| `STORY-08` | STYLE.md وPLAN.md: المرصود والمفترض والجدول الموقوت | STYLE.md + PLAN.md: observed vs assumed + timed scene table | proven | node, python3 |
| `STORY-14` | كتل القفل الحرفية للاستمرارية | Verbatim lock-block continuity | proven |  |
| `STORY-21` | محرك الصراع وstory_lint | Conflict engine + story_lint (GMC+S) | proven | python3 |
| `STORY-45` | التعلم من المرجع دون نسخه | Learn from references without cloning | proven | python3 |
| `STORY-48` | كشف جملة الذروة | Payoff-line detection | proven |  |
| `STORY-59` | مونتاج مُخرَج لمقطع كلام | Directed edit of a talking clip | proven | pip:faster-whisper |
| `STORY-65` | ستة أقواس لأنواع الستيكمان | Stickman six genre arcs | proven |  |
| `STORY-66` | قوس الحب بخمس نبضات وإطارين | Five-beat love arc with paired frames | proven | node |
| `STORY-67` | ملاءمة عدد المقاطع لخطوات الطبخ | Clip-count fitting (food flow) | proven |  |
| `STORY-68` | مخرج الفيرال بخمس بوابات | Viral five-stage gated director | proven | node |
| `STORY-83` | أعمدة المحتوى والتقويم | Content pillars & publishing calendar | proven | pip:office |
| `TRANS-01` | انتقال تطبيقات الموبايل: غمس للأسود | Phone-editor transition: dipblack | proven | pip:opencv, pip:scipy |
| `TRANS-02` | انتقال تطبيقات الموبايل: غمس للأبيض | Phone-editor transition: dipwhite | proven | pip:opencv, pip:scipy |
| `TRANS-03` | انتقال تطبيقات الموبايل: فلاش أبيض | Phone-editor transition: flash | proven | pip:opencv, pip:scipy |
| `TRANS-04` | إضافة خطاف في البداية مع استمرار الموسيقى | Prepend hook while music stays continuous | proven | ffmpeg |
| `TRANS-05` | عتبات قص الصمت والحشو | Silence and filler cut thresholds | proven | ffmpeg |
| `TRANS-06` | مكتبة انتقالات xfade | xfade transition palette | proven | ffmpeg |
| `TRANS-07` | دخول المشهد عند تغيير الشاشة | Scene enter on view change | proven | npm:react |
| `TRANS-08` | مكتبة انتقالات الكينتك | Kinetic transition library (17) | proven |  |
| `TRANS-09` | تسليم بوضعية مطابقة | Matching exit-pose handoff | proven |  |
| `TRANS-10` | انتقالات xfade في التايملاين | FFmpeg xfade transitions in the timeline | proven | ffmpeg |
| `TRANS-11` | إظلام قصير بين القطعات | Micro dip between hard cuts | proven | ffmpeg |
| `TRANS-12` | تصنيف الانتقال بإعادة التركيب | Transition classification by re-synthesis | proven |  |
| `TRANS-13` | تلاشي وذوبان | Fades and dissolves (xfade) | proven | ffmpeg, pip:numpy |
| `TRANS-14` | مسح | Wipes (xfade) | proven | ffmpeg, pip:numpy |
| `TRANS-15` | سحب | Slides (xfade) | proven | ffmpeg, pip:numpy |
| `TRANS-16` | مسح ناعم | Smooth wipes (xfade) | proven | ffmpeg, pip:numpy |
| `TRANS-17` | دوائر ومستطيلات | Circle and rect shapes (xfade) | proven | ffmpeg, pip:numpy |
| `TRANS-18` | أبواب تنفتح | Barn doors (xfade) | proven | ffmpeg, pip:numpy |
| `TRANS-19` | قطري | Diagonals (xfade) | proven | ffmpeg, pip:numpy |
| `TRANS-20` | شرائح | Slices (xfade) | proven | ffmpeg, pip:numpy |
| `TRANS-21` | تغطية وكشف | Cover and reveal (xfade) | proven | ffmpeg, pip:numpy |
| `TRANS-22` | ضغط وزووم وبكسلة | Squeeze, zoom, pixelize, blur (xfade) | proven | ffmpeg, pip:numpy |
| `TRANS-23` | مخطط المونتاج على الإيقاع | Beat-grid montage planner | proven | python3, imagemagick |
| `TRANS-24` | اختيار أنشط مقطع | Most-active window shot picker | proven | imagemagick |
| `TRANS-25` | أمر مونتاج الإيقاع | Beat montage command | proven | python3, imagemagick |
| `TRANS-26` | مونتاج يقوده الصوت | Voice-first montage | proven | python3, imagemagick |
| `TRANS-27` | زووم خاطف عند القطع | Camera punch-in on scene cuts | proven |  |
| `TRANS-U01` | منحنى منزلق قبل/بعد: انزلاق ثم زحف ثم كشف | Before/after slider: glide → crawl → reveal | proven |  |
| `TRANS-X13` | تصنيف الانتقال بإعادة التركيب داخل المستودع | Transition classification by re-synthesis, shipped in-repo | proven | ffmpeg, chromium, pip:numpy, pip:pillow |
| `DL-01` | تحميل فيديو من أي رابط | Download video from any URL | proven | python3, yt-dlp |
| `DL-02` | قائمة روابط دفعة واحدة | Batch of links from a file | proven | python3, yt-dlp |
| `DL-03` | جودة محددة أو صوت فقط | Quality cap or audio-only | proven | yt-dlp |
| `DL-04` | نسخة آمنة للمونتاج | Edit-safe H.264/AAC copy | proven | ffmpeg, yt-dlp |
| `DL-07` | تحديث yt-dlp عند تغيّر الموقع | Update yt-dlp when a site breaks | proven | python3, yt-dlp |
| `CAM-14` | ثبات حي | Living hold (breathe) | ready |  |
| `CAM-15` | اختلاف المنظر | Layer parallax | ready |  |
| `CAM-16` | نقل البؤرة | Rack focus without animated blur | ready |  |
| `CAM-17` | اهتزاز الكاميرا | Camera shake / hit | ready |  |
| `CAM-18` | مسار كاميرا منحني | Centripetal Catmull-Rom camera path | ready |  |
| `CAM-19` | دوللي زووم | Dolly zoom (Vertigo) | ready |  |
| `CAM-20` | دوران الكاميرا مع توقفات | Orbit walk with stops | ready |  |
| `CAM-21` | كشف العناصر عند دخولها الإطار | Scroll reveal via IntersectionObserver | ready |  |
| `CAM-22` | حركة كين بيرنز على لقطات الموقع | Ken Burns on captured screenshots | ready | ffmpeg |
| `CAM-23` | تقريب الكاميرا عبر viewBox | SVG viewBox camera zoom (drill-down) | ready |  |
| `CAM-24` | كاميرا بارالاكس بالمؤشر واللمس والتمرير | Pointer / touch / scroll parallax camera | ready |  |
| `CAM-25` | أغطية تدرّج لقراءة النص فوق الفيديو | Legibility veils over footage | ready |  |
| `CAM-26` | تلاشي الصورة داخل البطاقة بالقناع | Masked art fade on cards | ready |  |
| `CAM-27` | كاميرا مقيدة بدفع بصري | Locked restrained camera | ready |  |
| `CAM-28` | تخطيط آمن للهاتف | Phone-safe vertical layout | ready |  |
| `CAM-29` | تخطيطات الفيديو والبطاقة الأربعة | Recut layouts: split / stack / pip / overlay | ready |  |
| `CAM-30` | إطارات الفيديو الزخرفية | Recut video frames: clean / hairline / polaroid | ready |  |
| `CAM-31` | حركة الكاميرا للمسرح | Stage camera move (camera) | ready |  |
| `CAM-32` | دفع الكاميرا | Log-space camera push (push) | ready |  |
| `CAM-33` | تحويل البؤرة | Rack focus by crossfade | ready |  |
| `CAM-34` | عمق الميدان | Bokeh depth of field | ready |  |
| `CAM-35` | لغة اللقطات | Shot language cameras (20 kinds) | ready |  |
| `CAM-36` | كاميرا محمولة | Handheld camera noise | ready |  |
| `CAM-37` | كاميرا تدور وتتوقف | Orbit walk camera with stops | ready |  |
| `CAM-38` | زووم كين بيرنز | Ken Burns zoom | ready |  |
| `CAM-39` | ملاءمة الإطار | Fit modes cover/contain/blur | ready |  |
| `CAM-40` | إعادة تأطير ذكية | Smart reframe | ready | python3 |
| `CAM-41` | مفردات حركة الكاميرا | Camera move vocabulary (2D and 3D) | ready |  |
| `CAM-42` | ملاءمة اللقطة: ملء أو احتواء | Clip fit: cover vs contain | ready |  |
| `CAM-43` | كاميرا بارالاكس متعددة الطبقات | Multi-plane parallax camera with slow push | ready |  |
| `CAM-44` | إطار سينمائي: أشرطة ونقش وبطاقات | Cinematic frame: letterbox bars, vignette and minimalist cards | ready |  |
| `CAM-45` | فحص التكوين | Composition check: saliency centroid, thirds, symmetry | ready |  |
| `CAM-46` | التعريض المكافئ | Equivalent exposure | ready | python3 |
| `CAM-47` | زاوية الغالق إلى سرعة الغالق | Shutter angle → shutter speed (motion blur) | ready | python3 |
| `CAM-48` | كاميرا المسرح الواحدة | Single 2D stage camera | ready |  |
| `CAM-49` | دفع الكاميرا للداخل | Log-space camera push | ready |  |
| `CAM-50` | تمويه السرعة الاتجاهي | Directional speed blur | ready |  |
| `CAM-51` | مفاتيح كاميرا ناعمة | Smooth camera keys (3D) | ready |  |
| `CAM-52` | مفردات اللقطات ككاميرات | Shot vocabulary as deterministic 3D cameras | ready | key:video-gen |
| `CAM-53` | تمويه البؤرة والحركة | Lens defocus and motion blur ops | ready |  |
| `CAM-54` | ترتيب طبقات الكاميرا | Camera stack order | ready |  |
| `CAM-55` | أشرطة السينما 16:9 | Cinema letterbox 16:9 | ready |  |
| `CAM-56` | العمق الجوي وضباب الوادي | Atmospheric depth veil and valley fog | ready |  |
| `CAM-57` | ضربة تكبير على النبضة | Zoom punch on downbeats | ready | imagemagick |
| `CAM-58` | إعادة التأطير الذكي | Smart reframe (face / motion / blur pad) | ready | python3 |
| `CHAR-10` | هيكل SVG بنقاط دوران | SVG cut-out rig with pivots | ready | python3, npm:remotion |
| `CHAR-16` | أدوات تفاصيل المخلوقات | Creature detail builders | ready |  |
| `CHAR-17` | الرجل العصوي الكوميدي | Stickman comic style | ready | python3 |
| `CHAR-36` | حياة الخمول | Idle life (breath, blink, glances) | ready |  |
| `CHAR-39` | سرب طيور | Flock of birds | ready |  |
| `CHAR-41` | عيون لامعة وعيون برمش | Glossy & blinking eyes | ready |  |
| `CHAR-42` | أرنب وأسد المختبر | Lab rabbit & lion characters | ready | python3 |
| `CHAR-43` | سمكة كوي إجرائية | Procedural koi | ready |  |
| `CHAR-44` | شخصيات من أشكال أولية | Primitive toon figures | ready |  |
| `CHAR-45` | دوران 360 لورقة الشخصية | Turntable character sheet | ready |  |
| `CHAR-46` | جسد من الجسيمات بحركة حقيقية | Particle body from real motion (mocap) | ready | pip:opencv |
| `CHAR-48` | لوحات الكوميكس | Comics panels | ready | python3 |
| `CHAR-49` | أنمي أكشن | Anime action | ready | python3 |
| `EASE-03` | المدة الكلية حساب صريح | Duration arithmetic truth | ready |  |
| `EASE-07` | توقيت السطور العربية بلا صوت | Arabic line timing without audio | ready |  |
| `EASE-10` | أربع تسارعات مسماة فقط | Four named eases slam/snap/drive/settle | ready |  |
| `EASE-14` | قاموس منحنيات GSAP حسب الإحساس | GSAP ease vocabulary by mood | ready | npm:gsap |
| `EASE-15` | اتجاه التسهيل معنى | Ease direction = meaning | ready | python3 |
| `EASE-19` | لقطة السرعة U | U-speed shot | ready | imagemagick |
| `EASE-25` | نابض بتردد وتخميد | Frequency–ζ analytic spring | ready |  |
| `EASE-33` | تتابع القائمة في مكتبة الحركة | Kit list stagger | ready |  |
| `EASE-41` | مشهد تحريري بست ثوانٍ | Six-second editorial scene timeline | ready |  |
| `EASE-47` | الخط الزمني الرئيسي المتوقف | Paused master timeline authoring | ready | npm:gsap, npm:hyperframes |
| `EASE-52` | انضغاط التلامس | Contact squash | ready |  |
| `EASE-53` | كلمة تقفز بالمط والضغط | Squash-and-stretch hop | ready |  |
| `EASE-58` | ظهور منبثق مع تمويه | Blur pop-in / pop-out | ready |  |
| `EASE-59` | اهتزاز الضحك والتمايل | Laughing wiggle & phase-offset sway | ready |  |
| `EASE-61` | تمويه السرعة الاتجاهي | Directional speed blur | ready |  |
| `EASE-63` | معايير الإيقاع من أفلام الإطلاق | Pacing medians of top launch films | ready | python3 |
| `EASE-67` | ساعة الإيقاع في التركيب | Beat clock in compositions | ready | python3, npm:hyperframes |
| `EASE-69` | أنماط توقيت القطع والمغناطيس | Cut timing modes & magnetic snapping | ready |  |
| `EASE-74` | شريط التقدم الزمني | Timeline progress bars | ready |  |
| `EASE-76` | حركة بطيئة بإطارات مولدة | Optical-flow slow motion & frame interpolation | ready | ffmpeg, gpu |
| `EASE-78` | حلقات التنفس والطفو | Sine idle loops & breathing | ready |  |
| `EASE-80` | حلقات الحالة الصغيرة | Status micro-loops | ready |  |
| `EASE-81` | سرعات الكتابة الآلية | Typewriter speed table | ready |  |
| `EASE-82` | زمن الرسم حسب حجم الخطوة | Drawing-time model | ready |  |
| `EASE-83` | تفاعلات الضغط والمرور والنوافذ | Press, hover & dialog entrances | ready |  |
| `EASE-85` | زر تهدئة الحركة وتقليلها | Quiet-motion toggle & reduced motion | ready |  |
| `FMT-01` | المقاس من الوجهة | Derive the canvas from the destination | ready | python3 |
| `FMT-11` | قواعد المقروئية على الهاتف | Phone legibility gate | ready | imagemagick |
| `FMT-15` | تحجيم مع حشو لأي إطار | Scale + pad / centre crop | ready |  |
| `FMT-16` | أوضاع ملاءمة اللقطة: cover / contain / blur | Clip fit modes cover · contain · blur | ready |  |
| `FMT-26` | أهداف العلوّ لكل وجهة | Loudness targets per destination | ready | ffmpeg |
| `FMT-30` | تسجيل المتصفح إلى MP4 وGIF بمرورين | Browser clip → MP4 + two-pass GIF | ready | ffmpeg, chromium |
| `FMT-45` | اختيار إطار الغلاف آليًا | Thumbnail candidate picking | ready | ffmpeg, pip:numpy |
| `FMT-46` | غلاف بعنوان عربي من الفيلم | Arabic-titled cover from a film frame | ready | chromium, pip:pillow |
| `FMT-50` | حزمة أصول الهوية الرقمية | Identity export set: favicon, PWA, OG | ready | chromium, pip:pillow |
| `FMT-51` | تصدير الرسوم PNG@2x وSVG | Chart export PNG@2x / SVG + data-table toggle | ready |  |
| `FMT-52` | تصدير SVG وأوضاع الاستوديو الرسام | Painter studio export modes (PNG · 4K · SVG · MP4) | ready | python3 |
| `FMT-53` | مخرجات الطباعة والمستندات | Print & document outputs | ready | fonts:arabic |
| `FMT-54` | المستند إلى عرض شرائح | Document → slideshow / interactive deck | ready | npm:hyperframes |
| `FMT-60` | بنية الكاروسيل وحدوده | Carousel structure & limits | ready | python3 |
| `FMT-68` | أمثلة بريفات جاهزة | Ready example briefs | ready | node |
| `STORY-01` | استقبال عربي بجولة واحدة | One-round Arabic intake with defaults | ready | node |
| `STORY-05` | بوابة اختيار الأسلوب قبل التخطيط | Style-choice gate: 3–5 directions, max 2 blended | ready | python3 |
| `STORY-23` | قوس القطعة القصيرة | Short-piece arc (hook → development → pressure → lift → payoff → end) | ready | imagemagick |
| `STORY-24` | وصفة فيلم الخمس ثوانٍ | Five-second film recipe | ready |  |
| `STORY-25` | هيكل الإعلان ووصفة إعلان التطبيق 15 ث | Ad beat skeleton & 15 s app-ad recipe | ready | npm:remotion |
| `STORY-37` | قائمة «المظهر المولَّد» الممنوعة | Generated-look blacklist (anti-slop) | ready | python3 |
| `STORY-42` | قواعد تصميم الحركة | Choreography rules (build · breathe · resolve, 1/3 rules) | ready |  |
| `STORY-47` | الشيء المحمول عبر الفيلم | Travelling device / hero-object thread | ready |  |
| `STORY-49` | من المعنى إلى الرمز | Concept-to-symbol motifs | ready |  |
| `STORY-60` | قوس الريل التحفيزي (FINAL_EDIT) | Motivational talking-reel arc (FINAL_EDIT) | ready |  |
| `STORY-61` | فيلم الإطلاق من الموقع أو الكود | Launch video from a site or codebase (/brag) | ready | python3 |
| `STORY-62` | بنية ريل العرض 15 ث | Showreel beat structure (120 BPM) | ready |  |
| `STORY-63` | فيلم المختبر SHAPE→RANK | Product-lab film (SHAPE → JOINT → LOAD → BREAK → SWAP → RANK) | ready |  |
| `STORY-64` | قصة بلا كلام: مرشد وقفزة | Wordless short: a guide and a leap | ready |  |
| `STORY-69` | أفلام الدعاء والجمعة | Dua & Friday reels | ready |  |
| `STORY-70` | مونتاج الغربة بمعنى الأغنية | Meaning-matched song montage (Ghorba) | ready | imagemagick |
| `STORY-71` | مستقبل مصر 2120: خطاف وقاعدة تراث | Egypt 2120: one-second concept + heritage rule | ready |  |
| `STORY-72` | شرح «تعريفان للنجاح» على لوحات مولدة | Two-definitions-of-success voice explainer | ready | npm:gsap |
| `STORY-76` | لوحات المشهد المرسوم وموجّه الرسم | Painted-scene showcases & drawing request router | ready | npm:three |
| `STORY-78` | توليد أفكار بعشوائية حقيقية | Lateral ideation with real randomness | ready |  |
| `TRANS-28` | قص الصمت | Silence jump-cut | ready | python3 |
| `TRANS-29` | قطع بسرعات متطابقة | Velocity-matched cut | ready | npm:gsap, npm:remotion |
| `TRANS-30` | كشف دائري | Iris reveal / close | ready |  |
| `TRANS-31` | غمر لوني كامل | Colour flood seam | ready |  |
| `TRANS-32` | انتقالات السحب السريع والضبابي والزووم | Whip pan, blur-through and zoom-through transitions | ready |  |
| `TRANS-33` | وصفات انتقالات العرض الأصلية | View Transitions recipes (fade, slide, scale, morph) | ready | chromium, npm:react |
| `TRANS-34` | تحوّل الحاوية المشتركة | Shared-element container morph | ready | npm:gsap, npm:animejs |
| `TRANS-35` | حركات الدخول الأصلية بـ starting-style | Native entry animations with @starting-style | ready | npm:react |
| `TRANS-36` | كشف بالقص والقناع | Clip-path and SVG-mask reveals | ready |  |
| `TRANS-37` | قص بدون فقد مضبوط على الإطار المفتاحي | Keyframe-snapped lossless trim | ready | ffmpeg |
| `TRANS-38` | انتقال تسرب ضوئي | Light-leak transition | ready | npm:gsap |
| `TRANS-39` | احتراق تعريض زائد | Overexposure burn | ready |  |
| `TRANS-40` | حرق فيلم | Film-burn transition | ready |  |
| `TRANS-41` | احتراق الصفحة | Page-burn destruction | ready |  |
| `TRANS-42` | انتقال غليتش | RGB glitch transition | ready |  |
| `TRANS-43` | انتقال تفكك لوني | Chromatic-split transition | ready | npm:gsap |
| `TRANS-44` | تموج وشرائط VHS | Ripple / VHS strip transitions | ready | npm:gsap |
| `TRANS-45` | قلب بطاقة ثلاثي الأبعاد | CSS 3D card flip | ready |  |
| `TRANS-46` | انتقال بسرعة متطابقة | Velocity-matched blur transitions on text | ready |  |
| `TRANS-47` | دخول الشاشة والإشعار | Legacy view-in and toast-in | ready |  |
| `TRANS-48` | انتقال تبويبات مساحة العمل | Workspace tab switch (V5) | ready |  |
| `TRANS-49` | تبديل لوحة التفاصيل | Detail panel swap | ready |  |
| `TRANS-50` | توسيع الصف على الجوال | Mobile row expand | ready |  |
| `TRANS-51` | ارتفاع متحرك لعنصر details | Animated native <details> height | ready |  |
| `TRANS-52` | فيضان لوني | Colour flood wipe | ready |  |
| `TRANS-53` | دوران ثلاثي الأبعاد | 3D card roll | ready |  |
| `TRANS-54` | ضبابية السرعة | Directional speed blur | ready |  |
| `TRANS-55` | تشويش رقمي | Digital glitch stutter (2D) | ready |  |
| `TRANS-56` | تشويش مرتبط بالتحليل | Analysis-keyed glitch pass (3D) | ready |  |
| `TRANS-57` | قائمة لقطات بقطعات | Shot list sequencer (hard cuts) | ready |  |
| `TRANS-58` | انتقالات xfade | xfade transitions (57) | ready | ffmpeg |
| `TRANS-59` | انتقالات xfade | FFmpeg xfade transition set (58) | ready | ffmpeg, python3 |
| `TRANS-60` | محاكاة ريل | Mimic reference reel | ready |  |
| `TRANS-61` | حلقة سلسة | Seamless loop | ready | ffmpeg, python3 |
| `TRANS-62` | عائلة التلاشي | Cross-fade family (FFmpeg xfade) | ready | ffmpeg |
| `TRANS-63` | عائلة المسح | Wipe family (FFmpeg xfade) | ready | ffmpeg |
| `TRANS-64` | عائلة الانزلاق | Slide family (FFmpeg xfade) | ready | ffmpeg |
| `TRANS-65` | عائلة المسح الناعم | Smooth wipe family (FFmpeg xfade) | ready | ffmpeg |
| `TRANS-66` | كشف دائري ومستطيل وشعاعي | Circle / rect / radial reveals (FFmpeg xfade) | ready | ffmpeg |
| `TRANS-67` | فتح وإغلاق رأسي وأفقي | Barn-door opens and closes (FFmpeg xfade) | ready | ffmpeg |
| `TRANS-68` | مسح قطري | Diagonal wipes (FFmpeg xfade) | ready | ffmpeg |
| `TRANS-69` | انتقالات الشرائح | Slice transitions (FFmpeg xfade) | ready | ffmpeg |
| `TRANS-70` | انتقالات الريح | Wind transitions (FFmpeg xfade) | ready | ffmpeg |
| `TRANS-71` | انتقالات التغطية | Cover transitions (FFmpeg xfade) | ready | ffmpeg |
| `TRANS-72` | انتقالات الكشف | Reveal transitions (FFmpeg xfade) | ready | ffmpeg |
| `TRANS-73` | انتقالات الضغط | Squeeze transitions (FFmpeg xfade) | ready | ffmpeg |
| `TRANS-74` | انتقال الزووم للداخل | Zoom-in transition (FFmpeg xfade) | ready | ffmpeg |
| `TRANS-75` | انتقال التبكسل | Pixelize transition (FFmpeg xfade) | ready | ffmpeg |
| `TRANS-76` | انتقال الضبابية الأفقية | Horizontal blur transition (FFmpeg xfade) | ready | ffmpeg |
| `TRANS-77` | انتقال المسافة | Distance transition (FFmpeg xfade) | ready | ffmpeg |
| `TRANS-78` | قلب ثلاثي الأبعاد | Front-loaded 3D roll flip | ready |  |
| `TRANS-79` | مونتاج على الإيقاع | Beat-cut montage | ready | python3, imagemagick |
| `TRANS-80` | زووم ضربة | Zoom punch that decays like a hit | ready | ffmpeg, imagemagick |
| `TRANS-81` | صانع الحلقة السلسة | Seamless loop maker | ready | ffmpeg, python3 |
| `TRANS-82` | انتقالات xfade مع تداخل الصوت | xfade transitions + acrossfade | ready | ffmpeg |
| `TRANS-83` | قطع J وL | J-cut / L-cut | ready |  |
| `TRANS-84` | قطع حاد بلا تلاشي | Hard-cut concat (no crossfades) | ready | ffmpeg, imagemagick |
| `TRANS-85` | صانع الحلقة السلسة | Seamless loop builder | ready | ffmpeg, python3 |
| `DL-05` | كوكيز للمحتوى الخاص | Cookies for private / age-gated posts | ready | yt-dlp |
| `DL-06` | محاكاة متصفح عند الحظر | Browser impersonation retry | ready | python3, yt-dlp |
| `DL-10` | من الرابط إلى المونتاج | Link → analyse → montage | ready | ffmpeg, imagemagick, yt-dlp, pip:faster-whisper |
| `CAM-340` | مونتاج شبكي للهوية | Brand grid montage | documented | imagemagick |
| `CAM-341` | التخطيط قبل التحريك | Layout-before-animation (hero frame first) | documented |  |
| `CAM-342` | قواعد تكوين الكادر للفيديو | Video-frame composition rules | documented |  |
| `CAM-343` | اختيار المنحنيات وسرعة ثابتة على المسار | Spline choice & arc-length speed | documented |  |
| `CAM-344` | مسرح ثابت 16:9 | Fixed 16:9 stage | documented |  |
| `CAM-345` | شبكة 8 بكسل وقاعدة الزوايا المتداخلة | Layered 8px grid and nested radius rule | documented |  |
| `CAM-346` | تكوين غير متماثل يتجاوز الإطار | Asymmetric bleed composition | documented |  |
| `CAM-347` | تقسيم مشهد العرض 15/65/20 | Demo scene zoning 15/65/20 | documented |  |
| `CAM-348` | إعدادات تصوير بدون إظهار الوجه | Face-free camera setups | documented |  |
| `CAM-349` | S01 مينيمال نظيف | S01 Minimal clean | documented |  |
| `CAM-350` | S06 سينمائي جوي | S06 Atmospheric cinematic | documented | ffmpeg, node, chromium |
| `CAM-351` | S09 تحريري حديث | S09 Modern editorial | documented | ffmpeg, node, chromium |
| `CAM-352` | MG-085 تكبير من الكل إلى الجزء | MG-085 Whole-to-part zoom with minimap | documented |  |
| `CAM-353` | وظيفة كل لقطة | Shot-purpose ladder | documented |  |
| `CAM-354` | معايرة الشكل والخلفية للطبقات فوق الفيديو | Figure-ground calibration for overlays | documented | ffmpeg |
| `CAM-355` | تدقيق الزخرفة ونسبة الإشارة للضجيج | Decoration audit (signal-to-noise) | documented |  |
| `CAM-356` | رندر عمودي أصلي بدلاً من القص | Native vertical render over crop | documented | npm:remotion, npm:hyperframes |
| `CAM-357` | صورة داخل صورة وجنباً إلى جنب | Picture-in-picture and side-by-side | documented |  |
| `CAM-358` | نص واحد في الإطار | One text-bearing object per frame | documented |  |
| `CAM-359` | هامش تمدد النص | Text expansion headroom | documented |  |
| `CAM-360` | التشابه الجشطالتي باللون | Gestalt similarity via colour | documented |  |
| `CAM-361` | التسلسل الهرمي باللون والدرجة | Hierarchy via colour and tone | documented |  |
| `CAM-362` | أنواع لقطات بدون وجه | Faceless shot types table | documented |  |
| `CAM-363` | قاعدة 3-30-300 لمستويات الانتباه | 3-30-300 attention tiers | documented |  |
| `CAM-364` | شبكة 8px والأقطار المتداخلة | Spacing grid & nested radii rule | documented |  |
| `CAM-365` | تكوين الفراغ لجهة النص العربي | RTL negative-space composition | documented | ffmpeg |
| `CAM-366` | معايير دفع الكاميرا | Camera push norms | documented |  |
| `CAM-367` | زووم نبضي | Dynamic zoom punch | documented |  |
| `CAM-368` | قيادة البطل والحركة المعاكسة | Hero-led choreography + counter-motion | documented |  |
| `CAM-369` | كاميرا بحاوية واحدة | Single-container camera | documented |  |
| `CAM-370` | تكوين: Rule of thirds | Composition: Rule of thirds | documented |  |
| `CAM-371` | تكوين: Golden ratio/spiral | Composition: Golden ratio/spiral | documented |  |
| `CAM-372` | تكوين: Centred symmetry | Composition: Centred symmetry | documented |  |
| `CAM-373` | تكوين: Leading lines | Composition: Leading lines | documented |  |
| `CAM-374` | تكوين: Negative space | Composition: Negative space | documented |  |
| `CAM-375` | تكوين: Frame-within-frame | Composition: Frame-within-frame | documented |  |
| `CAM-376` | تكوين: Low-angle hero / high-angle vulnerability | Composition: Low-angle hero / high-angle vulnerability | documented |  |
| `CAM-377` | تكوين: Depth stacking | Composition: Depth stacking | documented |  |
| `CAM-378` | العدسات | Lens list | documented |  |
| `CAM-379` | أحجام اللقطات والزوايا | Shot sizes + angles | documented |  |
| `CAM-380` | حركات الكاميرا | Camera motion vocabulary | documented |  |
| `CAM-381` | قائمة قواعد التكوين | Composition rule menu | documented |  |
| `CAM-382` | قائمة الاستمرارية | Continuity checklist (180-degree rule etc.) | documented |  |
| `CAM-383` | كتالوج العدسات | Lens catalog and focal-length meaning | documented |  |
| `CAM-384` | مفردات اللقطات والزوايا وحركة الكاميرا | Shot sizes, angles and camera-move vocabulary | documented |  |
| `CAM-385` | قواعد التكوين للفيديو | Video composition rules | documented |  |
| `CAM-386` | التخطيط قبل الحركة | Layout-before-motion (hero frame) | documented | npm:gsap |
| `CAM-387` | منع النمو في المكان | No grow-in-place hero entrance | documented |  |
| `CAM-388` | ميزانية الكاميرا | Named camera events budget | documented |  |
| `CAM-389` | تحكم كاميرا Kling | Kling camera control reference | documented | key:video-gen |
| `CAM-390` | قواعد الكاميرا ثنائية الأبعاد | 2D camera rules | documented |  |
| `CAM-391` | قواعد التكوين للوحات | Composition rules for painted stills | documented |  |
| `CAM-392` | مفردات حركة الكاميرا | Camera move vocabulary | documented |  |
| `CAM-393` | إعدادات العدسة وزاوية الرؤية | Lens / FOV presets | documented | npm:three |
| `CAM-394` | نسب البارالاكس للطبقات | 2.5D parallax depth ratios | documented |  |
| `CAM-395` | عمق ميدان مزيف | Fake depth of field | documented |  |
| `CAM-396` | حدود كاميرا الرسوم | Chart camera limits | documented |  |
| `CAM-397` | كاميرا فصول المخطط | Diagram camera chapters | documented |  |
| `CAM-398` | حجم الجهاز لكل نسبة | Device scale per aspect | documented |  |
| `CAM-399` | القص الآمن للجهاز | Device safe crops | documented |  |
| `CAM-400` | دفع الكاميرا والتقريب عند النقر | Device camera push and tap dolly | documented |  |
| `CAM-401` | كاميرا واحدة لكل تسلسل | One camera rig per sequence | documented |  |
| `CAM-402` | حدود تأطير البورتريه | Portrait framing limits | documented |  |
| `CAM-403` | أرقام تأطير الشاشة | Screen framing numbers | documented |  |
| `CAM-404` | كاميرا بتحويل مجموعة واحد | CameraRig single group transform | documented | npm:remotion |
| `CAM-405` | عقد تسليم الحركة | Motion handoff contract | documented |  |
| `CAM-406` | مسافات معتمدة | Spacing token set | documented |  |
| `CAM-U01` | تتبع الأرض بالهوموغرافيا ولوحات مثبتة في العالم | Ground homography chain and world-anchored billboards | documented |  |
| `CAM-X01` | الكاميرا داخل المشاهد فقط | Camera lives inside scenes, neutral in transition windows | documented |  |
| `CAM-X02` | حركات كاميرا لها دافع | Motivated camera moves table | documented |  |
| `CAM-X03` | فيلم علامة بكاميرا واحدة | Single-camera brand film | documented |  |
| `CHAR-01` | ورقة تصميم الشخصية واختبار الظل | Model sheet & silhouette test | documented |  |
| `CHAR-02` | وصفة اللطافة | Cute character recipe | documented |  |
| `CHAR-03` | أقفال الهوية النصية | Identity lock text (CHR/LOC sheets) | documented | python3 |
| `CHAR-04` | قفل الشخصية النفسي | Personality lock | documented |  |
| `CHAR-27` | مولد المشي للسبرايت | Procedural sprite walk generator | documented | pip:pillow |
| `CHAR-28` | الوضعيات المفتاحية أولًا | Pose-to-pose blocking | documented |  |
| `CHAR-30` | الإشارة والكشف | Point and reveal | documented | npm:react |
| `CHAR-31` | الحديث للكاميرا | Talk-to-camera behaviours | documented |  |
| `CHAR-34` | مبادئ التحريك للهياكل | Animation principles for rigs | documented |  |
| `CHAR-X01` | شخصيات حية ببصمات حركة | Alive characters: personality motion signatures | documented |  |
| `EASE-06` | زمن القراءة من النص الفعلي | Reading-hold formulas | documented |  |
| `EASE-13` | منحنيات الاستوديوهات ورموز ستايل الكتالوج | Agency curves & catalog style tokens | documented |  |
| `EASE-18` | انزلاق بطيء-سريع-بطيء | Nudge curve slow–fast–slow | documented |  |
| `EASE-20` | إعدادات توقيت الانتقال الستة | Transition timing presets | documented |  |
| `EASE-26` | جداول إعدادات النوابض | Spring preset tables | documented | npm:gsap, npm:animejs |
| `EASE-27` | منحنى النابض المحسوب مسبقًا | Baked spring ease (springEase) | documented | npm:gsap |
| `EASE-28` | ميزانية التجاوز | Overshoot budget | documented |  |
| `EASE-31` | سقوط ثم استقرار | Drop + spring settle | documented |  |
| `EASE-32` | ميزانيات التتابع | Stagger budgets | documented | npm:gsap |
| `EASE-35` | نوافذ افتتاحية المشهد | Hero opening choreography windows | documented | npm:gsap |
| `EASE-36` | التداخل ونسب الفصول الأربعة | Overlap & four-act proportions | documented |  |
| `EASE-37` | قواعد الثلث | The 1/3 rules | documented |  |
| `EASE-38` | بناء ثم تنفس ثم حسم | Build / breathe / resolve | documented |  |
| `EASE-39` | السرعة تعني الوزن | Speed = weight tiers | documented |  |
| `EASE-42` | سلالم مدد الواجهات | UI duration ladders | documented |  |
| `EASE-43` | جدول توقيت عرض المنتج | Product-demo interaction timing | documented |  |
| `EASE-44` | اكشف على امتداد اللقطة | Reveal across the shot (anti-slide) | documented |  |
| `EASE-45` | أبقِ كل عنصر حيًا | Keep every element alive | documented |  |
| `EASE-46` | سلّم الوضعيات بإطارات GSAP | Pose ladder & mechanism choice | documented |  |
| `EASE-49` | التمهيد والمتابعة | Anticipation & follow-through | documented |  |
| `EASE-64` | إيقاع المونتاج حسب النوع | Edit rhythm by genre | documented |  |
| `EASE-65` | البنية الدقيقة للفيديو القصير | Short-form micro-structure | documented |  |
| `EASE-66` | القص على الإيقاع 60/BPM | Beat-cut rule | documented |  |
| `EASE-68` | قائمة لقطات على شبكة الإيقاع | Beat-grid shot list with onset-snapped words | documented |  |
| `EASE-70` | قواعد الوقفات في قص المتكلم | Speech pause grammar | documented | ffmpeg, pip:faster-whisper |
| `EASE-88` | تنعيم أثر المؤشر بالمسافة | Distance-sampled pointer trail | documented |  |
| `EASE-89` | توقيتات الصور وضربات الميزات | Photo & feature-beat timings | documented | imagemagick |
| `EASE-X06` | جداول منحنيات بالاسم والنية | Named curves: AE ↔ CSS table and intent eases | documented |  |
| `EASE-X07` | أرقام نعومة قبلها العميل | Client-approved smoothness numbers | documented |  |
| `EASE-X08` | قراءات مسموحة وميزانية السكون | Listed reads and the still-time budget | documented |  |
| `EASE-X10` | بوسترة طبقة واحدة | Per-layer posterize (stepped time on one layer) | documented |  |
| `EASE-X11` | تصميم الضربة الرئيسية | Main-hit micro-choreography | documented |  |
| `FMT-04` | مسرح ثابت يُكبَّر ككتلة | Fixed stage scaled as one block | documented |  |
| `FMT-05` | خط متجاوب بين المقاسات | Fluid type tokens per aspect | documented |  |
| `FMT-06` | نسختان مقصودتان لمشاهد البيانات | Deliberate vertical vs horizontal data layouts | documented |  |
| `FMT-07` | أبعاد تناسب نماذج التوليد | Latent-friendly sizes and frame counts | documented | key:video-gen |
| `FMT-09` | جدول هوامش المنصات للصور | Social canvas + text-safe margin table | documented |  |
| `FMT-10` | منطقة الترجمة الآمنة | Caption safe area | documented |  |
| `FMT-12` | كثافة العرض: متحدث أم قراءة | Density mode: narrated vs read-first | documented |  |
| `FMT-17` | دفعة شورتس من مونتاج طويل | Batch vertical shorts from a long edit | documented | ffmpeg |
| `FMT-18` | إعادة التكوين لا القص الأعمى | Recompose per platform, never blind-crop | documented |  |
| `FMT-21` | ماستر يوتيوب 4K | YouTube 4K delivery spec | documented | ffmpeg, python3, npm:hyperframes |
| `FMT-25` | ترميز GPU بـ NVENC | NVENC GPU encode | documented | npm:hyperframes, gpu |
| `FMT-27` | صيغ الصوت للحلقات وتراخيص الموسيقى | Loop audio formats & music licence receipts | documented | ffmpeg, key:elevenlabs |
| `FMT-28` | مواصفات معاينة متجر التطبيقات | App-store preview video spec | documented | ffmpeg |
| `FMT-29` | تضمين الموشن في صفحات الويب | Web embedding of motion & media | documented |  |
| `FMT-35` | خلطة الوسوم والخطاف | Hashtag mix & hook rules | documented |  |
| `FMT-36` | خط إنتاج النسخ المترجمة | Localized versions pipeline | documented |  |
| `FMT-43` | حزم المساعدات الأخرى وغلاف JSON | Custom GPT / Claude Project packs & JSON envelope | documented |  |
| `FMT-47` | بريف الصورة المصغرة: 3 أفكار واختبار A/B | Thumbnail brief: 3 concepts + A/B | documented |  |
| `FMT-48` | كلمات الغلاف وتكامله مع العنوان | Thumbnail word limits & title pairing | documented |  |
| `FMT-49` | غلاف طباعي للروابط OG | Typography-first OG / cover image | documented | chromium |
| `FMT-55` | فيزياء خانات الإعلان | Ad-slot structure physics | documented |  |
| `FMT-56` | نسخ مختصرة ومطولة من نص واحد | Alternate cut-downs (60/30/15 s) | documented |  |
| `FMT-57` | تفتيت المحتوى الطويل | Content atomisation map | documented |  |
| `FMT-58` | مواصفات التريلر حسب المنصة | Trailer platform targets | documented |  |
| `FMT-61` | افتتاحيات وخواتيم سوشيال عربية (MG-061…070) | Arabic social openers & closers (MG-061…070) | documented |  |
| `FMT-69` | مهارات تسويق مساندة | Supporting marketing skills (store, newsletter, SEO) | documented |  |
| `FMT-X01` | ماستر بلا صوت وملاحظة صادقة عن الصوت | Masters with a no-sound copy and an honest audio note | documented |  |
| `STORY-06` | جدول الرد قبل البناء | Talk-before-build response table | documented |  |
| `STORY-07` | قائمة القوة الكاملة وفرصة الوسائط | Full-power checklist & media-opportunity pass | documented |  |
| `STORY-09` | عقد المشهد كبيانات | Scene contract as data (scene cards) | documented |  |
| `STORY-10` | اللوحات قبل الرندر | Boards-first production gate | documented |  |
| `STORY-11` | جدول النبضات بعمود «المعلومة الجديدة» | Timed beat sheet with a “new information” column | documented |  |
| `STORY-12` | نوتة الحركة | Motion score table | documented |  |
| `STORY-13` | حزمة المخرج السينمائي ومواصفة المشهد بسبع طبقات | Cinema deliverable package & 7-layer scene spec | documented |  |
| `STORY-16` | قانون الثانية الأولى | One-second hook law (0–1–3 s) | documented |  |
| `STORY-17` | مكتبة الخطافات المسماة | Named hook library | documented |  |
| `STORY-18` | خطاف الفلوج الصامت | Silent-vlog hook anatomy | documented | ffmpeg |
| `STORY-19` | الإطار الأول دليل لا تدرّج | Product-proof first frame | documented |  |
| `STORY-22` | منتقي الإطار السردي | Story framework chooser | documented |  |
| `STORY-26` | أقواس العروض والإطلاق | Demo & launch arcs with second budgets | documented |  |
| `STORY-27` | فيلم العلامة: من المشكلة إلى الكشف | Brand film arc: problem → reveal (6 beats) | documented | npm:hyperframes |
| `STORY-28` | هياكل الشرح | Explainer structures | documented |  |
| `STORY-29` | مقاييس أساليب المونتاج الطويل | Long-form edit style metrics (essay · diary · reflection) | documented |  |
| `STORY-30` | هيكل يوتيوب الطويل والاحتفاظ | Long-form YouTube skeleton & retention holds | documented |  |
| `STORY-31` | التريلر بالمازورات وقوس الطاقة | Trailer beat sheet in bars & energy arc | documented |  |
| `STORY-32` | قوس قصة البيانات | Data story arc & progressive layering | documented |  |
| `STORY-33` | أقواس العروض التقديمية كهياكل فيديو | Deck & pitch arcs as video skeletons | documented |  |
| `STORY-35` | منهج المخرج: أطروحة ونقش ونوتة | Motion-director method: thesis, motif, score | documented |  |
| `STORY-36` | جرأة في مكان واحد | Spend boldness in one place | documented |  |
| `STORY-38` | شخصية حركة واحدة لكل فيلم | One motion personality per film | documented | node, chromium |
| `STORY-39` | من الشعور إلى الأرقام | Feeling → motion vocabulary map | documented |  |
| `STORY-40` | الأساليب المسماة الثمانية | Eight named visual styles (Swiss Pulse …) | documented |  |
| `STORY-41` | أنظمة جمالية جاهزة ولا تخلطها | Aesthetic systems & presets — never mix | documented | npm:axe |
| `STORY-43` | إخراج النبضة بأفعال الطاقة | Beat direction with energy verbs | documented |  |
| `STORY-44` | عدسات النقد قبل الرندر | Creative review lenses & aesthetics council | documented |  |
| `STORY-46` | قواعد الصدق في الوعود | Honesty rules for claims | documented | tesseract |
| `STORY-73` | أشكال فيديو صانع المحتوى | Creator-video shapes & faceless VO | documented |  |
| `STORY-74` | قواعد مونتاج المدينة | City montage shot grammar | documented | imagemagick |
| `STORY-77` | كتاب العالم والكائنات الأصلية | Creature & world-bible kit | documented |  |
| `STORY-79` | استخراج القصص والنُّقَط من النص | Story-mine & transcript nuggets | documented |  |
| `STORY-80` | العناوين: التوتر الصادق وخمسة اختبارات | Titles: honest charge & five tests | documented |  |
| `STORY-81` | خريطة الدعوة للفعل | CTA placement map | documented |  |
| `STORY-82` | الغلاف يبدأ من النفس لا من الصورة | Psychology-first thumbnail brainstorm | documented | chromium |
| `STORY-84` | موجة الموشن 2026: أنماط الطلب والميزانيات | Motion-wave prompt patterns & effort budgets | documented |  |
| `STORY-P01` | عشرون وصفة أسلوب موشن بمحركاتها | 20 motion style recipes (S01–S20) with engine candidates | documented | ffmpeg, blender, npm:remotion, npm:d3 |
| `STORY-P02` | الإحاطة السينمائية بثماني خانات | Eight-slot cinematic brief (PRODUCT → … → OUTPUT) | documented | ffmpeg, blender, npm:three, npm:remotion |
| `STORY-P03` | قاموس تحويل وصف الهواة إلى أوامر حركة | Amateur → pro motion lexicon (adjective → code direction) | documented |  |
| `STORY-U01` | خط فيلم الأغنية الكرتوني | Cartoon music-video pipeline | documented | key:video-gen |
| `STORY-X01` | السيناريو أولًا وخريطة المحفزات | Scenario first: beat-grid shot table and trigger map | documented |  |
| `STORY-X02` | ذوق العميل: من الرفض إلى قاعدة | Client taste: from rejection to rule | documented |  |
| `STORY-X03` | انضباط التكرار والنسخ | Iteration and version discipline | documented |  |
| `STORY-X04` | تقديرات وقت واقعية | Realistic time estimates | documented |  |
| `STORY-X05` | استعارات بصرية من فيلم الأغنية | Visual metaphors from the owner's song film | documented | python3 |
| `STORY-X06` | اعرض ثلاث معاينات بدل الأسئلة | Show three previews instead of a questionnaire | documented |  |
| `TRANS-376` | انتقال بشكل مشترك | Shared-shape scene handover | documented |  |
| `TRANS-377` | قاعدة: الانتقال هو الخروج | Scene rules: transition is the exit | documented | npm:gsap |
| `TRANS-378` | اختيار الانتقال حسب الطاقة | Transition by energy table | documented |  |
| `TRANS-379` | معنى كل انتقال | Transition meaning map | documented |  |
| `TRANS-380` | إعدادات انتقال جاهزة | Transition presets | documented |  |
| `TRANS-381` | شدة ضبابية الانتقال | Blur crossfade intensity | documented | npm:gsap |
| `TRANS-382` | فتحة دائرية وقطع قطري | Clip-path iris & diagonal split | documented |  |
| `TRANS-383` | تشويش رقمي وانحراف لوني | Glitch / chromatic / VHS / ripple | documented |  |
| `TRANS-384` | ستائر وكتل متتابعة | Blinds / staggered blocks / grid dissolve | documented |  |
| `TRANS-385` | تبديل اللقطات عند حدود الجمل | B-roll swap at sentence boundaries | documented |  |
| `TRANS-386` | MG-001 انتقال داخل شكل مطابق | MG-001 Shape-matched zoom-through | documented | ffmpeg |
| `TRANS-387` | MG-002 ستارة من جسم عابر | MG-002 Foreground body wipe | documented | pip:rembg |
| `TRANS-388` | MG-003 نقلة باندفاع جانبي | MG-003 Whip push inside directional blur | documented | ffmpeg |
| `TRANS-389` | MG-005 حبر يفتح المشهد | MG-005 Ink-bloom luma-matte reveal | documented | ffmpeg |
| `TRANS-390` | MG-006 شرائح بسرعات متتابعة | MG-006 Staggered slat wipe | documented |  |
| `TRANS-391` | MG-008 انتقال بإيقاف الحركة | MG-008 Stop-motion shrink to sticker | documented | ffmpeg |
| `TRANS-392` | MG-009 موجة تشوه تعبر القطع | MG-009 Displacement wave across the cut | documented | ffmpeg |
| `TRANS-393` | MG-010 الانتقال عبر إطار مجمد وطي الورقة والباب | MG-010 Freeze-frame 2.5D hop (with page fold and door portal) | documented | ffmpeg |
| `TRANS-394` | قص الصمت حسب نوع المحتوى | Genre-aware silence trimming | documented | ffmpeg |
| `TRANS-395` | قص دقيق للإطار بإعادة الترميز | Frame-accurate trim by re-encode | documented | ffmpeg, npm:remotion |
| `TRANS-396` | دمج المقاطع بقائمة concat | Concat list join | documented | ffmpeg |
| `TRANS-397` | سياسة القص التلقائي حسب النوع | Genre-aware auto-trim policy | documented |  |
| `TRANS-398` | قطع J و L للأصوات | J-cut / L-cut ambience | documented | ffmpeg, npm:remotion |
| `TRANS-399` | عودة الموسيقى بذيل ورايزر | Music re-entry with tail & riser | documented |  |
| `TRANS-400` | الانتقال بين مقطوعتين | Song A to B transition | documented |  |
| `TRANS-401` | كشف تدريجي من البكسلة | Progressive depixelation reveal | documented |  |
| `TRANS-402` | قواعد الانتقالات في قاعدة المخرج | Director KB transition rules (12) | documented |  |
| `TRANS-403` | لا مزج متلاشي — القطع بمطابقة السرعة | No crossfades / velocity-matched cut | documented |  |
| `TRANS-404` | تسرب ضوئي عند القطع | Light-leak cut transition | documented |  |
| `TRANS-405` | تراكب لقطات B-roll بانتقال ذائب | B-roll overlay with crossfade | documented | ffmpeg |
| `TRANS-406` | قواعد الانتقالات | Transition grammar: no crossfades, velocity-matched cuts | documented |  |
| `TRANS-407` | قاعدة معنى الانتقال | Transition meaning rule | documented |  |
| `TRANS-408` | انتقالات push | CSS/GSAP push transitions | documented | npm:gsap |
| `TRANS-409` | انتقالات radial | CSS/GSAP radial transitions | documented | npm:gsap |
| `TRANS-410` | انتقالات 3D | CSS/GSAP 3D transitions | documented | npm:gsap |
| `TRANS-411` | انتقالات scale | CSS/GSAP scale transitions | documented | npm:gsap |
| `TRANS-412` | انتقالات dissolve | CSS/GSAP dissolve transitions | documented | npm:gsap |
| `TRANS-413` | انتقالات cover | CSS/GSAP cover transitions | documented | npm:gsap |
| `TRANS-414` | انتقالات light | CSS/GSAP light transitions | documented | npm:gsap |
| `TRANS-415` | انتقالات distortion | CSS/GSAP distortion transitions | documented | npm:gsap |
| `TRANS-416` | انتقالات mechanical | CSS/GSAP mechanical transitions | documented | npm:gsap |
| `TRANS-417` | انتقالات grid | CSS/GSAP grid transitions | documented | npm:gsap |
| `TRANS-418` | انتقالات other | CSS/GSAP other transitions | documented | npm:gsap |
| `TRANS-419` | قواعد الانتقالات الصلبة | Transition hard rules (HTML) | documented | npm:gsap |
| `TRANS-420` | انتقالات Remotion | Remotion TransitionSeries | documented | npm:remotion |
| `TRANS-421` | معاني الانتقالات | Transition semantics | documented |  |
| `TRANS-422` | سلسلة التحول بجسم حامل | Carrier-object transformation chain | documented |  |
| `TRANS-423` | قاعدة انتقالين | Two-transition rule | documented | ffmpeg |
| `TRANS-424` | قواعد الانتقالات | Transition grammar (no crossfades) | documented |  |
| `TRANS-425` | انتقال: قطع | Transition key: cut | documented |  |
| `TRANS-426` | انتقال: مسح | Transition key: wipe | documented |  |
| `TRANS-427` | انتقال: تحول | Transition key: morph | documented |  |
| `TRANS-428` | انتقال: كشف بالقناع | Transition key: mask-reveal | documented |  |
| `TRANS-429` | انتقال: زووم عابر | Transition key: zoom-through | documented |  |
| `TRANS-430` | انتقال: قطع مطابق | Transition key: match-cut | documented |  |
| `TRANS-431` | انتقال: ذوبان | Transition key: dissolve | documented |  |
| `TRANS-432` | مسح قبل وبعد | Before/after split wipe | documented |  |
| `TRANS-433` | من الرسم إلى الحقيقي | Sketch-to-real crossfade | documented |  |
| `TRANS-434` | القطع على الضربة | Cut-on-beat rule | documented |  |
| `TRANS-435` | شكل واحد بلا قطع | One shape never cut | documented |  |
| `TRANS-436` | كشف بقناع دائري | Boolean circle-mask reveal | documented |  |
| `TRANS-437` | سحب الشاشة واللوحة المنبثقة | Swipe / screen push and modal sheet | documented |  |
| `TRANS-438` | أقنعة الصور الديناميكية | Dynamic photo masks | documented |  |
| `TRANS-439` | تحويل الصورة إلى رسم | Photo-to-graphic trace | documented |  |
| `TRANS-440` | قطع وميضي | Flash cut | documented |  |
| `TRANS-441` | قطع بالتكبير | Zoom cut entrance | documented |  |
| `TRANS-442` | تلاشي مع تحجيم | Scale crossfade | documented |  |
| `TRANS-X01` | لكل انتقال سبب يُسمّى | Every transition needs a nameable cause | documented |  |
| `TRANS-X02` | زوم الإبرة على جسم مستمر | Needle zoom on a persistent object | documented |  |
| `TRANS-X03` | استمرار الطيران عبر الأشياء | Fly-through continuation rule | documented |  |
| `TRANS-X04` | حمل الجسم بإحداثيات الشاشة | Object carry contract in screen pixels | documented |  |
| `TRANS-X05` | اللطخة والسوط بطبقات وزوج التأرجح | Smear, layered-parallax whip and swing pair | documented |  |
| `TRANS-X06` | تحوّل الواجهة بالحجم لا بالمقياس | UI morph by size, not scale (button → CTA) | documented |  |
| `TRANS-X07` | فيضان اللون من نقطة الفعل | Colour flood from the action point | documented |  |
| `TRANS-X08` | انسكاب الأعمدة ومنحدر التعريض | Column pour and exposure-ramp reveals | documented |  |
| `TRANS-X09` | تسليم القزحية إلى شعار | Iris hand-off into a wordmark | documented |  |
| `TRANS-X10` | قطع الخلل بالأشرطة | Band glitch cut | documented |  |
| `TRANS-X11` | زوم لانهائي حول نقطة بؤرية | Focal-point infinite-zoom transition | documented |  |
| `TRANS-X12` | انتقالات دُفع ثمنها | Transition failures already paid for | documented |  |
| `DL-08` | حدود هذه الحاوية السحابية | Limits of this cloud container | documented | yt-dlp |
| `DL-09` | المصدر ثم الاستخدام: ترخيص وحقوق | Rights check before editing | documented | yt-dlp |
| `DL-11` | سجل سلسلة Cinema C للآيفون | Cinema C iPhone lineage ledger (V13 → V34) | documented | ffmpeg, yt-dlp |
| `CAM-195` | إطار HUD للريل | Showreel HUD frame | seen |  |
| `CAM-196` | إطار HUD | HUD frame overlay | seen |  |
| `CAM-197` | إطار HUD ثابت للشوريل | Persistent HUD reel frame | seen |  |
| `CAM-198` | إطار معلومات HUD | HUD frame chrome | seen |  |
| `CAM-199` | إطار معاينة بزوايا وتايمكود | Viewfinder HUD frame | seen |  |
| `CAM-200` | إطار HUD للريل | HUD showreel frame | seen |  |
| `CAM-201` | جولة كاميرا على عناصر الدرس | Lesson camera tour | seen |  |
| `CAM-202` | عالم متصل بكاميرا واحدة | One-take world strip camera | seen |  |
| `CAM-203` | غرفة بزاوية من مضلعات مسقطة | Oblique room from projected polygons | seen |  |
| `CAM-204` | كاميرا بمفاتيح في إحداثيات العالم مع تتبع | World-space camera keys + follow blend | seen |  |
| `CAM-205` | كاميرا تتبع مع زووم حسب المرحلة | Follow camera with leg-based zoom | seen |  |
| `CAM-206` | حقل شارات طافية فوضوية | Floating badge chaos field | seen |  |
| `CAM-207` | شريط خطوات مرقمة | Numbered step tab bar | seen |  |
| `CAM-208` | إطار HUD | HUD corner frame | seen |  |
| `CAM-209` | خاتمة بأشعة وحلقة شخصيات | Sunburst finale ring | seen |  |
| `CAM-210` | إطار HUD مرقم للشوريل | Numbered HUD reel frame | seen |  |
| `CAM-211` | تخطيط ميزة: نص يسار ونافذة يمين | Feature beat split layout | seen |  |
| `CAM-212` | تقريب بطيء داخل الواجهة | Ken-burns inside UI | seen |  |
| `CAM-213` | شريط تنقل سفلي | Bottom nav progress | seen |  |
| `CAM-214` | التحليق فوق حقل بطاقات متوهجة | Glowing card field fly-over | seen |  |
| `CAM-215` | طبقة HUD فيلمية | Film HUD overlay | seen |  |
| `CAM-216` | تخطيط نص وواجهة | Split text/UI layout | seen |  |
| `CAM-217` | دفع الكاميرا نحو الشخصية | Push-in camera dolly | seen |  |
| `CAM-218` | أقواس وإحداثيات | Geo HUD brackets | seen |  |
| `CAM-219` | رفع الكاميرا للقطة علوية ختامية | Crane to top-down hero end card | seen |  |
| `CAM-220` | عنوان صغير بمساحة فارغة واسعة | Negative-space headline | seen |  |
| `CAM-221` | كاميرا عالم واحد بمحاور تركيز وتكبير لوغاريتمي | World-layer camera (focus x, y, log-scale) | seen |  |
| `CAM-222` | خلفية جدار بطاقات مائل مع عمق ميدان | Tilted DOF card wall backdrop | seen |  |
| `CAM-223` | إحساس السرعة بمرور أعمدة السياج | Rail parallax for speed | seen |  |
| `CAM-224` | تجميع شبكة بينتو | Bento grid assembly | seen |  |
| `CAM-225` | شبكة بطاقات | Bento principle grid | seen |  |
| `CAM-226` | علامات قص زاوية للإطار | Corner crop marks frame | seen |  |
| `CAM-227` | مسرح مستدير فوق خلفية متدرجة | Rounded stage over atmospheric gradient | seen |  |
| `CAM-228` | اقتراب من الجهاز | Device push-in | seen |  |
| `CAM-229` | تسميات صغيرة بأسلوب الملصق | Poster HUD micro-labels | seen |  |
| `CAM-230` | عرض دوّار للنموذج | Turntable orbit showcase | seen |  |
| `CAM-231` | عنوان يسار وبطاقة واجهة يمين | Split headline + UI card | seen |  |
| `CAM-232` | تقريب على تفاصيل الواجهة | Macro zoom into UI | seen |  |
| `CAM-233` | بطاقات خلفية ضبابية | Depth-of-field cards | seen |  |
| `CAM-234` | نظام وسوم الفصول | Chapter tag system | seen |  |
| `CAM-235` | ترويسة تحريرية | Editorial header | seen |  |
| `CAM-236` | شبكة شاشات | Split-screen grid | seen |  |
| `CAM-237` | ترويسة فصل مرقّمة | Numbered chapter header | seen |  |
| `CAM-238` | بطاقة عنوان سوداء تتقلص | Black title card shrink-out | seen |  |
| `CAM-239` | حركة كاميرا بطيئة تكشف المعلم | Slow reveal dolly | seen |  |
| `CAM-240` | لوحة فارغة بسيطة | Negative-space minimal canvas | seen |  |
| `CAM-241` | بطاقات مبعثرة تستقر في صف منظم | Scatter-to-grid card settle | seen |  |
| `CAM-242` | عداد إطارات كجزء من التصميم | Frame-counter meta HUD | seen |  |
| `CAM-243` | عمق ميدان للواجهة | Depth-of-field UI | seen |  |
| `CAM-244` | بطاقات بنتو للميزات | Bento feature cards | seen |  |
| `CAM-245` | قالب بطاقة موحد لكل عنصر | Templated listicle card | seen | npm:react |
| `CAM-246` | شرطات تقدم المقاطع | Segment progress dashes | seen |  |
| `CAM-247` | إطار كاميرا تسجيل | Camcorder HUD frame | seen |  |
| `CAM-248` | واجهة كاميرا | Viewfinder HUD | seen |  |
| `CAM-249` | تقريب كولاج طبقي | Collage push-in parallax | seen |  |
| `CAM-250` | كاميرا مطاردة بتأخير | Chase camera with lag | seen |  |
| `CAM-251` | HUD يشرح التقنية | Self-annotating HUD | seen |  |
| `CAM-252` | مقارنة: ما كُتب مقابل البديل | Evidence pair: typed vs instead | seen |  |
| `CAM-253` | عدادات ركنية أحادية | Mono corner counters | seen |  |
| `CAM-254` | شريط زمني بنقاط مفاتيح | Editor timeline HUD | seen |  |
| `CAM-255` | دفع كاميرا على واجهة مائلة | Tilted UI push-in | seen |  |
| `CAM-256` | إطار HUD ورقي | Paper HUD frame | seen |  |
| `CAM-257` | لقطة ميزة بتقسيم تحريري | Editorial split feature beat | seen |  |
| `CAM-258` | إطار HUD لعبة ثابت | Persistent game HUD frame | seen |  |
| `CAM-259` | رقم فهرس مع اسم النموذج | Index + model lower-third | seen |  |
| `CAM-260` | منظر متحرك من نافذة بطبقات بارالاكس | Window parallax travel | seen |  |
| `CAM-261` | تكوين متناظر بأسلوب ويس أندرسون | Symmetrical Wes-Anderson frame | seen |  |
| `CAM-262` | مؤشر المشاهد | Scene index HUD | seen |  |
| `CAM-263` | كاميرا مطاردة مائلة | Chase camera with bank | seen |  |
| `CAM-264` | اقتراب للشاشة مع كتابة طرفية | Push-in terminal typewriter | seen |  |
| `CAM-265` | إطار HUD للشوريل | Showreel HUD overlay | seen |  |
| `CAM-266` | إطار بعلامات قص | Crop-mark frame | seen |  |
| `CAM-267` | عنوان فوق نافذة المنتج | Headline over product window | seen |  |
| `CAM-268` | عناصر زوايا ثابتة | Persistent corner chrome | seen |  |
| `CAM-269` | كاميرا افتراضية تتجول فوق لوحة واجهة كبيرة | Virtual camera over one big UI canvas | seen |  |
| `CAM-270` | تخطيط صفوف الآلات | Instrument tier diagram layout | seen |  |
| `CAM-271` | دخول وخروج من الشاشة | Push into screen bookend | seen |  |
| `CAM-272` | لوحات ثلاثية للأقسام | Triptych category panels | seen |  |
| `CAM-273` | عنوان جانبي عمودي | Vertical side label | seen |  |
| `CAM-274` | كشف اللوحة بالابتعاد | Canvas zoom-out reveal | seen |  |
| `CAM-275` | عناوين فصول وشريط زمني | Chapter HUD + timeline marker | seen |  |
| `CAM-276` | شريط تبويبات كأداة تنقل بين الفصول | Pill tab bar as chapter navigator | seen |  |
| `CAM-277` | زووم لا نهائي أُسّي | Exponential infinite zoom | seen |  |
| `CAM-278` | دوران ودفع الكاميرا | Orbit push-in | seen |  |
| `CAM-279` | خطوة مع تعليق | Step label + caption | seen |  |
| `CAM-280` | كاميرا افتراضية فوق سبورة كبيرة | Virtual camera over a big board | seen |  |
| `CAM-281` | تقريب الكاميرا على عنصر الواجهة | UI camera push-in | seen |  |
| `CAM-282` | إطار سويسري ثابت بعداد فصول ووقت | Swiss HUD frame with chapter counter | seen |  |
| `CAM-283` | عدسة مكبرة لكشف التفاصيل | Magnifier zoom-in proof | seen |  |
| `CAM-284` | تراكب عمق بخلفية مموهة | Background blur depth stack | seen |  |
| `CAM-285` | واجهة فصول | Chapter HUD | seen |  |
| `CAM-286` | خاتمة بأشرطة سينمائية تنغلق | Letterbox squeeze outro | seen |  |
| `CAM-287` | مزج كتابة رأسية وأفقية | Vertical + horizontal type pairing | seen |  |
| `CAM-288` | تسميات صغيرة في الزوايا | Corner meta labels | seen |  |
| `CAM-289` | شارة خطوة مرقمة | Numbered step chip | seen |  |
| `CAM-290` | طيران الكاميرا بين الفصول | Camera chapter fly-to | seen |  |
| `CAM-291` | إطار HUD بزوايا وعدّاد زمني | HUD corner frame with running timecode | seen |  |
| `CAM-292` | نفق لا نهائي | Infinite tunnel zoom | seen |  |
| `CAM-293` | إطار HUD بفصول مرقمة | Chaptered HUD frame | seen |  |
| `CAM-294` | كاميرا مطاردة تدور مع الطائرة | Chase camera with roll | seen |  |
| `CAM-295` | مقارنة أنت/أنا بتقسيم الشاشة | You/me split comparison | seen |  |
| `CAM-296` | إطار HUD سينمائي | Cinematic HUD chrome | seen |  |
| `CAM-297` | خط تقدم على حافة الشاشة السفلية | Bottom-edge progress line | seen |  |
| `CAM-298` | بيانات وصفية في زوايا الملصق | Poster metadata HUD | seen |  |
| `CAM-299` | بطاقة مقسومة فاتح/داكن للنتيجة | Split light/dark result card | seen |  |
| `CAM-300` | شريط فصول | Chapter progress bar | seen |  |
| `CAM-301` | جدار بطاقات | Card wall drift | seen |  |
| `CAM-302` | عنوان جانبي مع بطاقة واجهة طافية | Split headline + floating UI card | seen |  |
| `CAM-303` | اقتراب بطيء جدًا نحو الهدف | Ultra-slow approach dolly | seen |  |
| `CAM-304` | إطار HUD للفصول | Chapter HUD frame | seen |  |
| `CAM-305` | واجهة قراءات حية | Scope HUD with live readouts | seen |  |
| `CAM-306` | صور تطير لتكوين شبكة إلهام | Fly-in moodboard grid | seen |  |
| `CAM-307` | دفع كاميرا مستمر بلا ارتداد | Continuous push camera | seen |  |
| `CAM-308` | إطار سينمائي | Letterbox cinematic | seen |  |
| `CAM-309` | شبكة ملخص مرقمة | Recap grid with numbered badges | seen |  |
| `CAM-310` | إطار HUD سينمائي ثابت | Persistent cinematic HUD frame | seen |  |
| `CAM-311` | كلمات تسقط في خلايا شبكة | Paper grid drop-in | seen |  |
| `CAM-312` | ملصقات فصول HUD | Chapter HUD labels | seen |  |
| `CAM-313` | جدار بطاقات مائل متحرك | Tilted masonry card wall | seen |  |
| `CAM-314` | بطاقة فصل أسفل اليسار | Chapter text card bottom-left | seen |  |
| `CAM-315` | إطار عدسة كاميرا بفصول مرقمة | Viewfinder HUD chapters | seen |  |
| `CAM-316` | شريحة عنوان ضخم مع جسم ثلاثي الأبعاد | Editorial headline + 3D object slide | seen |  |
| `CAM-317` | تراجع لكشف الكولاج | Collage pull-back reveal | seen |  |
| `CAM-318` | مرور الكاميرا على أوراق مع ختم | Paperwork dolly + stamp | seen |  |
| `CAM-319` | خطوة مرقمة مع واجهة | Numbered step split | seen |  |
| `CAM-320` | سبورة بيضاء مؤطرة على جدار داكن | Framed whiteboard set | seen |  |
| `CAM-321` | إطار HUD إنتاجي | Production HUD frame | seen |  |
| `CAM-322` | عنوان مع دليل بصري | Headline + proof layout | seen |  |
| `CAM-323` | HUD تقني بتسميات FIG | FIG-caption technical HUD | seen |  |
| `CAM-324` | شخص صغير لإبراز الضخامة | Scale figure in frame | seen |  |
| `CAM-325` | شريط مراحل | Stage progress rail | seen |  |
| `CAM-326` | كولاج بطاقات متناثرة | Scattered card collage | seen |  |
| `CAM-327` | شبكة بطاقات صور متتابعة | Staggered photo card grid | seen |  |
| `CAM-328` | إطار HUD للريل | HUD reel chrome | seen |  |
| `CAM-329` | عناوين خطوات مرقمة | Numbered step headers | seen |  |
| `CAM-330` | مسطرة زمنية للفصول | Chapter ruler timeline | seen |  |
| `CAM-331` | جدار لقطات مائل ينزلق بسرعة | Tilted screenshot wall sweep | seen |  |
| `CAM-332` | بطاقات مكدسة مائلة | Stacked badge cards | seen |  |
| `CAM-333` | ملصقات منحنيات التسهيل | HUD ease labels | seen |  |
| `CAM-334` | دفع الكاميرا داخل نافذة التطبيق | Push into app window | seen |  |
| `CAM-335` | إطار ستارة | Stage curtain frame | seen |  |
| `CAM-336` | عبور الكاميرا بين كروت طائرة | Z-space card fly-through | seen |  |
| `CAM-337` | اهتزاز الكاميرا عند الارتطام | Impact camera shake | seen |  |
| `CAM-338` | تكوين خشبة مسرح جانبي | Stage-set side-view layout | seen |  |
| `CAM-339` | كاميرا واحدة لطبقتي SVG وHTML | Shared SVG+HTML camera transform | seen |  |
| `CHAR-12` | انحناء الجسم والمط حسب السرعة | Velocity-driven body bend & squash | seen |  |
| `CHAR-14` | شخصية قصاصات بمؤشر اتجاه | Cut-out rig with facing dial | seen |  |
| `CHAR-18` | تحريك رسمة واحدة بعظام | 2D mesh bone rig from one image | seen | npm:three, npm:p5 |
| `CHAR-19` | أشياء بوجوه وتمائم | Object-as-character faces & mascots | seen |  |
| `CHAR-20` | مسرح شخصية بديكور واحد | Single-set character stage | seen |  |
| `CHAR-21` | شخصيات ظلية مسطحة | Flat silhouette characters | seen |  |
| `CHAR-22` | تمائم البكسل والسبرايت | Pixel & sprite mascots | seen |  |
| `CHAR-23` | تحولات الشخصية | Character transformations & variants | seen |  |
| `CHAR-32` | ظهور التمائم وقفزاتها | Mascot pop-ins & hop arcs | seen |  |
| `CHAR-33` | لمسات تمثيل | Acting accents: celebrate, sleep, run | seen |  |
| `EASE-08` | معامل بطء واحد للدرس كله | Global slowness factor TS | seen |  |
| `EASE-21` | منحنى التسهيل على الشاشة | Easing curve shown on screen | seen |  |
| `EASE-50` | دخول بميل ثم استقرار | Tilt-in settle | seen |  |
| `EASE-55` | قفزة بقوس بين حاملين | Parabolic hops & piecewise paths | seen |  |
| `EASE-56` | ختم يُطبع بقوة | Stamp slam | seen |  |
| `EASE-57` | حلقة الأثر ووميض المفتاح | Impact ripple & key hit-flash | seen |  |
| `EASE-71` | انفجار القطع السريع | Rapid-fire cut bursts | seen | imagemagick |
| `EASE-72` | بناء بطيء ثم ضربة | Contrast pacing: slow burn, calm hold | seen |  |
| `EASE-79` | حلقة مغلقة بلا قطع | Seamless loop closure | seen |  |
| `EASE-87` | تبديل الحالات بانسيابية | State swaps: FLIP reflow & headline crossfade | seen |  |
| `FMT-66` | سؤال خطاف مع عدّاد حي | Hook question + live counter overlay | seen |  |
| `FMT-67` | إعلان مربع للخلاصة | Square feed promo | seen | python3 |
| `STORY-20` | افتتاحيات مرصودة: سؤال، سطران متعاكسان، إشعارات الألم | Observed openers: question, two-line reversal, pain notifications | seen |  |
| `STORY-34` | قصص الأطفال: كتاب مصور ويوم كامل | Kids stories: picture book & day-to-night arc | seen |  |
| `STORY-50` | أنظمة الفصول المرقّمة | Chapter label systems | seen |  |
| `STORY-51` | خواتيم الملخص | Recap endings (grid · collage · board · progress) | seen |  |
| `STORY-52` | الإطار المغلق والحلقة | Bookends & loop endings | seen |  |
| `STORY-53` | بطاقات الجملة والصمت | Statement cards, caption beats & silence | seen |  |
| `STORY-54` | تبدّل المزاج: ظلام/نور، نهار/ليل | Mood shifts: dark↔light acts, day/night interludes | seen |  |
| `STORY-55` | نبضات كوميدية وعاطفية | Comic & emotional beats | seen |  |
| `STORY-56` | نبضات الحجة | Argument beats (pain triptych · THE FIX bar · cost reframing · paper-form) | seen |  |
| `STORY-57` | جسر الوميض والسحب للخلف إلى ملصق | Flash bridge + poster pull-back reveal | seen |  |
| `STORY-58` | نبضات العالم والحالة | World beats: surreal props, overload, one-take, beacon | seen | npm:hyperframes |
| `TRANS-262` | بطاقة اقتباس فوق مشهد باهت | Quote card over hazed scene | seen |  |
| `TRANS-263` | انتقال بالعبور من فتحة | Zoom-through-hole transition | seen |  |
| `TRANS-264` | عبور السحاب كانتقال | Cloud fly-through transition | seen |  |
| `TRANS-265` | شريط فيلم ينزلق | Sliding film strip | seen |  |
| `TRANS-266` | كشف بدائرة قزحية | Circle iris reveal | seen |  |
| `TRANS-267` | مسح بثلاث شرائح لونية | Tri-band panel wipe | seen |  |
| `TRANS-268` | مسح دائري ناعم من النقطة | Soft circle iris wipe from focal point | seen |  |
| `TRANS-269` | إيقاع حقول لونية | Colour-field cut rhythm | seen |  |
| `TRANS-270` | كلمات فوق تكبير شديد للرسم | Macro zoom word beats | seen |  |
| `TRANS-271` | قطع كلمات المزايا السريع | Rapid feature word cuts | seen |  |
| `TRANS-272` | مسح نقطي دائري | Halftone ring wipe | seen |  |
| `TRANS-273` | مسح قطري بألواح ملوّنة | Diagonal panel wipe | seen |  |
| `TRANS-274` | لافتة الدور | Turn banner | seen |  |
| `TRANS-275` | مسح بخطوط قطرية | Diagonal stripe wipe | seen |  |
| `TRANS-276` | عد تنازلي بأسلوب شريط السينما | Film-leader countdown | seen |  |
| `TRANS-277` | اختراق بخطوط سرعة | Zoom-through speed lines | seen |  |
| `TRANS-278` | مسح شرائط قوس قزح | Rainbow stripe wipe | seen |  |
| `TRANS-279` | انتقال بالتلاشي إلى الخلفية | Fade-through-ground scene change | seen |  |
| `TRANS-280` | تقلص الشبكة إلى هاتف | Window grid to device | seen |  |
| `TRANS-281` | مفتاح أوضاع بمسح نقطي | Mode toggle with dither wipe | seen |  |
| `TRANS-282` | انقضاض تكبير داخل بطاقة حتى ملء الشاشة | Whip zoom into tile to full-bleed | seen |  |
| `TRANS-283` | قطع مطابق بالعودة إلى البطاقة | Match cut back into source tile | seen |  |
| `TRANS-284` | ومضات بطاقات العلامات | Rapid brand-card flashes | seen |  |
| `TRANS-285` | تتابع كلمات بقطع سريع | Cut-burst word sequence | seen |  |
| `TRANS-286` | مونتاج سريع لنطاق الأساليب | Style-range rapid montage | seen | imagemagick |
| `TRANS-287` | كشف الصورة من نقطة تتضخم | Dot-to-disc portrait reveal | seen |  |
| `TRANS-288` | مسح بنقاط الحبر الإلكتروني | E-ink dither wipe | seen |  |
| `TRANS-289` | توسيع العنصر المشترك (الغلاف) | Shared-element artwork expand | seen |  |
| `TRANS-290` | مسح درجي بكسلي | Pixel stair wipe | seen |  |
| `TRANS-291` | مسح ضوئي قبل/بعد | Light-bar before/after sweep | seen |  |
| `TRANS-292` | سهم النمو يطير إلى الشعار | Growth chart arrow fly-off to logo | seen |  |
| `TRANS-293` | قطع بانقلاب الفاتح والداكن | Light/dark inversion cuts | seen |  |
| `TRANS-294` | مسح بقرص يتمدد | Disc expand wipe | seen |  |
| `TRANS-295` | قلب فاتح داكن | Light/dark flip | seen |  |
| `TRANS-296` | انتقال بالتغبيش بين الفصول | Blur-dissolve chapter change | seen |  |
| `TRANS-297` | انتقال دائري من داخل الرقم | Digit iris transition | seen |  |
| `TRANS-298` | استعراض السمات بقطعات سريعة | Theme roll call cuts | seen |  |
| `TRANS-299` | بداية ونهاية بتلاشٍ من السواد وإليه | Fade-from/to-black bookends | seen |  |
| `TRANS-300` | مسح ورقي ممزق | Torn paper wipe | seen |  |
| `TRANS-301` | مسح لوني كامل كفاصل | Full-bleed colour wipe interstitial | seen |  |
| `TRANS-302` | غوص داخل شاشة متداخلة | Nested-screen dive (recursive zoom) | seen |  |
| `TRANS-303` | مسح ختامي كريمي | Cream end wipe | seen |  |
| `TRANS-304` | تذويب بكسلي | Pixel mosaic dissolve | seen |  |
| `TRANS-305` | تكرار نص متشوه | Glitch type tiling | seen |  |
| `TRANS-306` | انتقال مسح بالشرائط | Stripe wipe transition | seen |  |
| `TRANS-307` | ثمانية انتقالات في مازورة | Beat-locked transition bar | seen |  |
| `TRANS-308` | قطع بالكتل اللونية | Colour-block cut | seen |  |
| `TRANS-309` | مسح لوني صلب | Solid colour wipe | seen |  |
| `TRANS-310` | دوران سريع وتصغير لخريطة المستويات | World-map whip and zoom-out | seen |  |
| `TRANS-311` | مسح بشاشة منقسمة | Split-screen wipe | seen |  |
| `TRANS-312` | مرور عمود أمامي ضبابي | Foreground pole whoosh | seen |  |
| `TRANS-313` | انتقال بالنفق المظلم | Tunnel wipe scene change | seen |  |
| `TRANS-314` | مسح بأشرطة لونية | Colour stripe wipe | seen |  |
| `TRANS-315` | صورة تطير من المحادثة إلى المستند | Image flies into document slot | seen |  |
| `TRANS-316` | قواعد مشاهد مبنية على التلاشي | Fade-driven scene grammar | seen |  |
| `TRANS-317` | نهاية بالغوص في الشعار | Zoom-through logo ending | seen |  |
| `TRANS-318` | جليتش بانفصال القنوات وشرائح أفقية | RGB-split slice glitch | seen |  |
| `TRANS-319` | ومضة خاطفة تمهّد لما بعدها | Glitch flash-frame foreshadow | seen |  |
| `TRANS-320` | انتقال بقلب الثيم مع ضبابية | Theme-flip blur crossfade | seen |  |
| `TRANS-321` | قطع عبر بوابة الجسم | Portal object match-cut | seen |  |
| `TRANS-322` | دخول عنوان بسرعة مع ضبابية حركة | Whip-in headline with motion blur | seen |  |
| `TRANS-323` | خروج سوطي بضبابية حركة | Motion-blur whip exit | seen |  |
| `TRANS-324` | تتابع سحب سريع | Whip relay | seen |  |
| `TRANS-325` | تقلّص الصورة إلى بطاقة | Hero shrinks into card | seen |  |
| `TRANS-326` | خط أرض مستمر | Continuous ground line | seen |  |
| `TRANS-327` | تكبير عبر قناع دائري | Circle mask zoom-through | seen |  |
| `TRANS-328` | وميض سالب | Negative flash | seen |  |
| `TRANS-329` | تلاشي بين الخطوات | Dim-out step crossfade | seen |  |
| `TRANS-330` | ضربة كلمة بتشويش ألوان RGB | RGB split glitch slam | seen |  |
| `TRANS-331` | ومضة ضوء بيضاء بإضاءة بقعية | Spotlight bloom white-out | seen |  |
| `TRANS-332` | تقطيع وميضي | Strobe cut burst | seen |  |
| `TRANS-333` | انتقال لوح لوني للفصل | Chapter colour slam | seen |  |
| `TRANS-334` | انتقال جليتش بفصل الألوان | RGB-split glitch transition | seen |  |
| `TRANS-335` | انتقال بالبياض الشمسي | Sun whiteout bridge | seen |  |
| `TRANS-336` | إمالة سريعة مع وميض لوني | Whip-tilt with tint flash | seen |  |
| `TRANS-337` | صفحة تنزلق للأعلى بلطخة | Smear scroll-in page | seen |  |
| `TRANS-338` | بطاقات صادمة بانعكاس الألوان | Colour-inversion beat cards | seen |  |
| `TRANS-339` | انتقال بمسح دائري | Circle wipe scene change | seen |  |
| `TRANS-340` | كلمة تنشق بخط مائل | Slash-split word | seen |  |
| `TRANS-341` | انفجار كلمات سريع | Rapid word-cut burst | seen |  |
| `TRANS-342` | مسح بشبكة مربعات | Tile grid wipe | seen |  |
| `TRANS-343` | قطع متبادل بين الشيفرة والصورة | Code↔visual cut bursts | seen |  |
| `TRANS-344` | شريط مائل يدخل بقوة | Diagonal banner slam | seen |  |
| `TRANS-345` | ومضات صور سريعة بملء الشاشة | Rapid full-screen image flashes | seen |  |
| `TRANS-346` | انتقال بضبابية وتكبير | Blur-zoom dissolve | seen |  |
| `TRANS-347` | كشف واجهة المحرر بالتراجع | Editor pull-out reveal | seen |  |
| `TRANS-348` | كشف دائري من علامة تصويب | Iris reticle reveal | seen |  |
| `TRANS-349` | انتقال بقناع دائري | Iris circle transition | seen |  |
| `TRANS-350` | انتقال سحب بتمويه حركة | Motion-blur whip transition | seen |  |
| `TRANS-351` | مسح لوني دائري عملاق | Circular colour-field wipe | seen |  |
| `TRANS-352` | انتقال جليتش شرائحي | Slice glitch transition | seen |  |
| `TRANS-353` | مسح بدائرة متنامية | Circle grow wipe | seen |  |
| `TRANS-354` | خطوط تشويش ملونة للخاتمة | RGB glitch line end card | seen |  |
| `TRANS-355` | قطع بقلب الألوان | Colour-flip hard cuts | seen |  |
| `TRANS-356` | مونتاج كلمات على الإيقاع | Beat word-card montage | seen | imagemagick |
| `TRANS-357` | كروت تطير بضبابية حركة | Whip-out cards with motion blur | seen |  |
| `TRANS-358` | اهتزاز فصل ألوان | RGB split stutter | seen |  |
| `TRANS-359` | مسح السبورة بالممحاة بين الفصول | Eraser chapter wipe | seen |  |
| `TRANS-360` | مسح الشاشة بشرائط ملونة | Full-screen stripe wipe | seen |  |
| `TRANS-361` | انتقال دائرة لونية متوسعة | Iris circle colour wipe | seen |  |
| `TRANS-362` | مسح دائري يغمر الشاشة بلون | Circle wipe colour flood | seen |  |
| `TRANS-363` | دائرة تتمدد وتغمر الشاشة | Iris circle flood | seen |  |
| `TRANS-364` | مسح بشريط مائل إلى صورة | Diagonal band wipe to photo | seen |  |
| `TRANS-365` | تفكك بكسلي | Pixelation dissolve | seen |  |
| `TRANS-366` | مسح غلتش شرائحي | Glitch slice wipe | seen |  |
| `TRANS-367` | عبور زووم داخل الصورة | Zoom-through image portal | seen |  |
| `TRANS-368` | تبديل المحتوى بضبابية قصيرة | Blur content swap | seen |  |
| `TRANS-369` | كشف بعدسة دائرية | Circular lens reveal | seen |  |
| `TRANS-370` | كشف بطاقة ملونة | Colour card reveal | seen |  |
| `TRANS-371` | نقطة بطلة تربط المشاهد | Hero dot match-cut | seen |  |
| `TRANS-372` | عبور بتكبير لوني | Zoom-through colour wipe | seen |  |
| `TRANS-373` | مسح بأشرطة ألوان أساسية | Primary-colour stripe wipe | seen |  |
| `TRANS-374` | انتقال سوط ضبابي | Whip motion-blur transition | seen |  |
| `TRANS-375` | قطع حاد بين الظلام والنور | Hard dark/light section flip | seen |  |
| `CAM-100` | حركة كين بيرنز | Ken Burns pan on stills/footage | install | npm:gsap |
| `CAM-101` | إعادة التأطير بالقص | Crop / reframe with clip-path inset | install | npm:gsap |
| `CAM-102` | حركة ملء الشاشة بخلفيات مشتركة | Full-screen motion with shared backgrounds | install |  |
| `CAM-103` | تقريب إلى هدف غير مركزي | Coordinate target zoom | install | npm:gsap, npm:hyperframes |
| `CAM-104` | كاميرا تتبع مؤشر الكتابة | Camera tracks typing cursor | install | npm:gsap, npm:hyperframes |
| `CAM-105` | كاميرا متعددة المراحل مع انجراف | Multi-phase camera push/pull with drift | install | npm:gsap, npm:hyperframes |
| `CAM-106` | كاميرا افتراضية بتحريك العالم | Virtual camera via .world wrapper | install | npm:gsap, npm:hyperframes |
| `CAM-107` | عمق الميدان وسحب التركيز | Depth-of-field rack focus | install | npm:gsap, npm:hyperframes |
| `CAM-108` | انتشار من المركز إلى الخارج | Center-outward expansion | install | npm:gsap, npm:hyperframes |
| `CAM-109` | بطاقتان مائلتان متقابلتان | Split tilt cards | install | npm:gsap, npm:hyperframes |
| `CAM-110` | مخطط مشهد: محطات على لوحة كبيرة تتنقل بينها الكاميرا | Blueprint: Spatial pan stations | install | npm:hyperframes |
| `CAM-111` | مخطط مشهد: رحلة الكاميرا | Blueprint: Camera journey | install | npm:hyperframes |
| `CAM-112` | مخطط مشهد: كشف بالتبعيد عن مساحة العمل | Blueprint: Zoom-out workspace reveal | install | npm:hyperframes |
| `CAM-113` | مخطط مشهد: تجميع شبكة البطاقات | Blueprint: Grid card assemble | install | npm:hyperframes |
| `CAM-114` | مخطط مشهد: مقارنة منقسمة | Blueprint: Comparison split | install | npm:hyperframes |
| `CAM-115` | قواعد مقياس الفيديو | Video-scale composition rules | install |  |
| `CAM-116` | نمط صورة داخل صورة | Composition pattern: picture-in-picture | install |  |
| `CAM-117` | بطاقة عنوان وعرض شرائح | Composition pattern: title card fade / slideshow with section headers | install |  |
| `CAM-118` | المناطق الآمنة للبث | Broadcast safe zones | install | npm:hyperframes |
| `CAM-119` | حساب المناطق الآمنة من القناع | Safe zones from subject matte | install | node |
| `CAM-120` | أنواع المشاهد وقواعد تموضع الترجمة | Caption scene types and layout heuristics | install |  |
| `CAM-121` | تفاعلات اللوح: تعتيم وصدمة واهتزاز وحبيبات | Theme plate reactions (dim, punch, shake, grain) | install |  |
| `CAM-122` | مناطق البطاقات | Recut card zones | install |  |
| `CAM-123` | حركة إيقاعية: screen-shake | Beat motion primitive: screen-shake | install | npm:gsap |
| `CAM-124` | حركة إيقاعية: dolly-zoom | Beat motion primitive: dolly-zoom | install | npm:gsap |
| `CAM-125` | حركة إيقاعية: crash-zoom-in | Beat motion primitive: crash-zoom-in | install | npm:gsap |
| `CAM-126` | حركة إيقاعية: mosaic-pack | Beat motion primitive: mosaic-pack | install | npm:gsap |
| `CAM-127` | حركة إيقاعية: tile-mosaic | Beat motion primitive: tile-mosaic | install | npm:gsap |
| `CAM-128` | تكبير لوغاريتمي | Log-space zoom lmix/push/zoomTrack | install |  |
| `CAM-129` | اهتزاز الكاميرا | shake | install |  |
| `CAM-130` | البارالاكس | parallax | install |  |
| `CAM-131` | تنفس اللقطة الثابتة | breathe holds | install |  |
| `CAM-132` | مفردات اللقطات ككاميرات | Veo shot vocabulary as cameras | install | key:video-gen |
| `CAM-133` | مسار الكاميرا المستمر | cameraPath Catmull-Rom | install | npm:three |
| `CAM-134` | كاميرا الدوران مع التوقفات | orbitWalk camera | install |  |
| `CAM-135` | تظليل علوي لوضوح العنوان | Top shade for title legibility | install |  |
| `CAM-136` | كاميرا ثنائية الأبعاد متزامنة مع الكلام | Word-synced 2D camera on a footage plate | install |  |
| `CAM-137` | اهتزاز دقيق لأربعة إطارات | Seeded 4-frame micro shake | install | npm:gsap |
| `CAM-138` | دفع لوغاريتمي وثبات حي | Log-space push and living hold | install |  |
| `CAM-139` | مدار ثلاثي الأبعاد مع اقتراب واهتزاز | 3D orbit with push-in, break shake and pull-back | install |  |
| `CAM-140` | جولة كاميرا حول المشهد بتوقفات | Orbit walk with stops and holds | install |  |
| `CAM-141` | مفاتيح كاميرا هيرميت ووقت الرصاصة | Hermite camera keys with bullet time | install |  |
| `CAM-142` | مسارات كاميرا بمفاتيح | Keyed camera paths (cameraPath / cameraKeys) | install |  |
| `CAM-143` | دفع بطيء من مستوى الطريق | Road-level tripod push-in (Veo shot language) | install | key:video-gen |
| `CAM-144` | إسقاط نقطة ثلاثية على الشاشة لوسم | Project 3D point to screen for HUD callout | install |  |
| `CAM-145` | زووم كين بيرنز | Ken Burns raised-cosine zoom | install |  |
| `CAM-146` | كاميرا تقترب في قوس | Dolly-in arc camera (time-driven) | install |  |
| `CAM-147` | زووم نبضي لرفع الاحتفاظ | Retention zoom punches | install | ffmpeg |
| `CAM-148` | حركات كاميرا بالمسارات | Spline camera flights and eased dollies | install |  |
| `CAM-149` | طبقة قراءة وحجاب خارج المحراب | Readability glass and arch veil | install |  |
| `CAM-150` | تنفس الكاميرا ودفعات الإبراز | Camera breath and punctuating pushes (2D stage) | install |  |
| `CAM-151` | لقطات تدخل وهي تتحرك | Plates that arrive already moving (punch-in drift) | install | imagemagick |
| `CAM-152` | ضربة عاطفية مع اهتزاز | Emotional punch + camera shake | install |  |
| `CAM-153` | حركات الكاميرا على المسرح | Stage camera moves (camera, log push, breathe) | install |  |
| `CAM-154` | حركة كين برنز | Ken Burns move detection and replay | install |  |
| `CAM-155` | ملاءمة اللقطة وكن برنز | Shot fit modes + Ken Burns | install |  |
| `CAM-156` | عمق مجال | Scene op: defocus depth of field | install |  |
| `CAM-157` | تمويه حركة | Scene op: motion blur | install |  |
| `CAM-158` | تكوين الثمبنيل | Thumbnail composition rule | install | chromium |
| `CAM-159` | كاميرا المسرح | 2D stage camera move | install |  |
| `CAM-160` | دفع الكاميرا | Log-space push-in | install |  |
| `CAM-161` | اهتزاز الكاميرا | Camera shake (seeded) | install |  |
| `CAM-162` | مفاتيح الكاميرا | Smoothstep camera keys | install |  |
| `CAM-163` | مسار كاميرا مستمر | Continuous Catmull-Rom camera path | install |  |
| `CAM-164` | مفردات اللقطات | Shot vocabulary camera (20 kinds) | install | key:video-gen |
| `CAM-165` | اهتزاز يدوي | Seeded handheld sway | install |  |
| `CAM-166` | لقطة من الكلمات | Shot from words | install |  |
| `CAM-167` | خلفية الاستوديو | Studio backdrop gradient | install |  |
| `CAM-168` | استوديو كريمي | Cream studio sweep | install |  |
| `CAM-169` | ضبابية الحركة بالإطارات الفرعية والتعريض الطويل | Sub-frame shutter motion blur and lighten stacking | install | python3 |
| `CAM-170` | عمق المجال | Depth of field (defocus) | install |  |
| `CAM-171` | ضبابية حركة اتجاهية | Directional motion blur | install | pip:opencv |
| `CAM-172` | التشتت اللوني | Chromatic aberration | install |  |
| `CAM-173` | كاميرا رقمية موجهة على مقطع متكلم | Directed digital camera on a talking clip | install | npm:gsap |
| `CAM-174` | كاميرا تلقائية تتبع الموضوع | Auto camera from subject boxes | install | python3 |
| `CAM-175` | إبعاد النص عن الوجه | Type off the face over pictures | install |  |
| `CAM-176` | شرائط السينما | Letterbox open/close | install | npm:gsap |
| `CAM-177` | عدسة تدور حول المشهد | Orbit-walk lens with holds | install |  |
| `CAM-178` | جولة سينمائية | Style: Cinematic journey (higgsfield-journey) | install | pip:higgsfield |
| `CAM-179` | كاميرا Remotion بانجراف بطيء | CameraRig slow drift push/pan/rotate | install |  |
| `CAM-180` | مسار كاميرا منحني | Spline camera path | install | npm:three |
| `CAM-59` | طبقات عمق بتتبع المؤشر | Mouse-parallax depth layers | install | npm:gsap |
| `CAM-60` | بارالاكس مرتبط بالتمرير ومشاهد مثبتة | Scroll-scrubbed parallax and pinned acts | install | npm:gsap |
| `CAM-61` | رصّ البطاقات المثبتة أثناء التمرير | Sticky scroll-stack of cards | install | npm:gsap |
| `CAM-62` | قصة تمرير بصورة مثبتة | Sticky-graphic scroll story | install | npm:gsap |
| `CAM-63` | كشف بطاقات بميلان ثلاثي | Card batch reveal with 3D tilt-up | install | npm:gsap |
| `CAM-64` | عمق الميدان / بوكيه | Depth of field (TSL dof) | install | npm:three |
| `CAM-65` | معرض WebGL مدفوع بالزمن | Scroll/time-driven WebGL gallery | install | npm:three, npm:gsap |
| `CAM-66` | حالات كاميرا مسماة | Named camera states | install | npm:gsap |
| `CAM-67` | نص يتفادى العناصر | Obstacle-aware type layout | install | npm:matter |
| `CAM-68` | تصميم حركة الكاميرا مع المسار | Route camera choreography | install | npm:maplibre |
| `CAM-69` | أنماط الزووم | Zoom modes (punch, Ken Burns, drift, pulse) | install |  |
| `CAM-70` | حركات الكاميرا السينمائية | Cinematic camera moves (19) | install |  |
| `CAM-71` | قاعدة تغطية الدوران | Rotation coverage rule | install | python3 |
| `CAM-72` | تخطيط الكاميرا حسب المود | Mood-based camera planner | install |  |
| `CAM-73` | عرض الفيديو كامل بخلفية ضبابية | Fit vs cover framing with blurred fill | install |  |
| `CAM-74` | شرايط السينما | Cinema letterbox bars | install |  |
| `CAM-75` | نافذة صغيرة فوق الفيديو | Picture-in-picture inserts | install |  |
| `CAM-76` | نقل لغة كاميرا المرجع | Reference camera language transfer | install |  |
| `CAM-77` | اهتزاز الكاميرا | Camera Shake | install | chromium, npm:hyperframes |
| `CAM-78` | تكبير يتبع النقرات | Zoom Follow Cursor | install | chromium, npm:hyperframes |
| `CAM-79` | ثبات حي | Drift Hold | install | chromium, pip:faster-whisper, npm:hyperframes |
| `CAM-80` | نقل التركيز | Focus Rack | install | chromium, npm:hyperframes |
| `CAM-81` | بانوراما المحطات | Pan Stations | install | chromium, npm:hyperframes |
| `CAM-82` | الغوص في الجهاز | Parallax Device Dive | install | npm:hyperframes |
| `CAM-83` | تصغير بارالاكس | Parallax Unzoom | install | chromium, npm:hyperframes |
| `CAM-84` | تكبير بارالاكس | Parallax Zoom | install | chromium, npm:hyperframes |
| `CAM-85` | كشف بالتراجع | Pull Back Reveal | install | chromium, npm:hyperframes |
| `CAM-86` | دفع الكاميرا | Push In | install | chromium, npm:hyperframes |
| `CAM-87` | قصة التمرير | Scroll Camera Story | install | chromium, npm:hyperframes |
| `CAM-88` | تكبير على الواجهة | UI Focus Zoom | install | chromium, npm:hyperframes |
| `CAM-89` | حركات كاميرا يوتيوب | Camera Punch-In | install | chromium, npm:hyperframes |
| `CAM-90` | دوللي زووم (فيرتيغو) | Dolly Zoom (Vertigo Shot) | install | npm:gsap, npm:hyperframes |
| `CAM-91` | نقل البؤرة بالبوكيه | Rack Focus | install | npm:three, npm:gsap, npm:hyperframes |
| `CAM-92` | دوار دائري | Carousel circle (styles 1-5) | install | npm:gsap, npm:hyperframes |
| `CAM-93` | دوار كروي | Carousel orbit (styles 1-5) | install | npm:gsap, npm:hyperframes |
| `CAM-94` | دوار على مسار | Carousel path (styles 1-5) | install | npm:gsap, npm:hyperframes |
| `CAM-95` | عنوان مع دوار دائري | Carousel text-circle (styles 1-5) | install | npm:gsap, npm:hyperframes |
| `CAM-96` | دوار الرؤية | Carousel vision (styles 1-5) | install | npm:gsap, npm:hyperframes |
| `CAM-97` | الشبكة السويسرية | Example project: swiss-grid | install | npm:hyperframes |
| `CAM-98` | منطقة حجز الترجمة أسفل الإطار | Caption keep-out zone (bottom ~17%) | install |  |
| `CAM-99` | تقريب مفاجئ على اللقطة | Punch-in zoom on footage | install | npm:gsap |
| `CHAR-09` | شخصية ذكاء اصطناعي بالحالات | Stateful AI persona orb | install | node, chromium |
| `CHAR-47` | تمثيل الشخصيات بلوتي | Lottie character acting | install | npm:gsap, npm:hyperframes, npm:lottie |
| `EASE-17` | وصول مقدَّم الوزن | Front-loaded arrival (extended keyframe) | install | npm:hyperframes |
| `EASE-29` | نابض Remotion والتحجيم الإدراكي | Remotion spring & perceptual scale | install | npm:remotion |
| `EASE-54` | أشباح تبيّن التباعد | Onion-skin spacing ghosts & echo trail | install | npm:hyperframes |
| `EASE-62` | ضبابية الغالق الحقيقية | Shutter motion blur | install | npm:remotion, npm:hyperframes |
| `EASE-77` | الإيقاع المتقطع على اثنين وثلاثة | Stepped cadence: on twos & threes | install | npm:hyperframes |
| `EASE-90` | مكونات HyperFrames للتوقيت | HyperFrames timing components | install | npm:hyperframes |
| `EASE-91` | مكتبات توقيت إضافية | Extra timing libraries | install | chromium, npm:lottie, npm:animejs |
| `FMT-23` | HDR بعشرة بت | HDR 10-bit HEVC | install | ffmpeg, npm:hyperframes |
| `FMT-37` | رندر دفعي بالمتغيرات | Variable-driven batch render | install | python3, npm:hyperframes |
| `FMT-38` | HyperFrames: صيغ وجودات الرندر | HyperFrames render formats & quality tiers | install | ffmpeg, chromium, docker, npm:hyperframes |
| `FMT-39` | مشاركة ورفع بلا نشر تلقائي | Share sheet & upload shortcuts (never auto-post) | install | node |
| `FMT-64` | ختام تحميل التطبيق وشارات المتاجر | App end card & store badges | install | npm:hyperframes |
| `FMT-65` | بطاقات المنصات المتحركة | Animated platform cards (follow, post, comment, now-playing) | install | npm:gsap, npm:hyperframes, os:macos |
| `STORY-15` | ذاكرة الذوق والوصفات | Taste memory & recipe freeze | install | npm:hyperframes |
| `STORY-75` | معرض قوالب الأفلام (52) وقوالب البداية | Film template gallery (52) & starter briefs | install | node, imagemagick |
| `TRANS-100` | كشف بمحاكاة سائل | Fluid-sim reveal / x-ray | install |  |
| `TRANS-101` | الانتقالات الإحدى عشر | Cut transitions (11) | install |  |
| `TRANS-102` | الوضع الهادي بدون وميض | Calm mode (no flicker) rule | install |  |
| `TRANS-103` | انفصال الألوان والجليتش | RGB split and slice glitch technique | install |  |
| `TRANS-104` | تسليم المشاهد قطع أو تلاشي | Scene handover: hard cut vs fade | install |  |
| `TRANS-105` | انتقال شيدر: انفصال لوني | Shader transition: chromatic-split | install | npm:three, npm:hyperframes |
| `TRANS-106` | انتقال شيدر: زوم سينمائي | Shader transition: cinematic-zoom | install | npm:three, npm:hyperframes |
| `TRANS-107` | انتقال شيدر: تحول التوائي | Shader transition: cross-warp-morph | install | npm:three, npm:hyperframes |
| `TRANS-108` | انتقال شيدر: تشويه المجال | Shader transition: domain-warp | install | npm:three, npm:hyperframes |
| `TRANS-109` | انتقال شيدر: وميض أبيض | Shader transition: flash-through-white | install | npm:three, npm:hyperframes |
| `TRANS-110` | انتقال شيدر: غلتش | Shader transition: glitch | install | npm:three, npm:hyperframes |
| `TRANS-111` | انتقال شيدر: عدسة جاذبية | Shader transition: gravitational-lens | install | npm:three, npm:hyperframes |
| `TRANS-112` | انتقال شيدر: تسرب ضوء | Shader transition: light-leak | install | npm:three, npm:hyperframes |
| `TRANS-113` | انتقال شيدر: احتراق متعرج | Shader transition: ridged-burn | install | npm:three, npm:hyperframes |
| `TRANS-114` | انتقال شيدر: تموجات | Shader transition: ripple-waves | install | npm:three, npm:hyperframes |
| `TRANS-115` | انتقال شيدر: قزحية | Shader transition: sdf-iris | install | npm:three, npm:hyperframes |
| `TRANS-116` | انتقال شيدر: دوامة | Shader transition: swirl-vortex | install | npm:three, npm:hyperframes |
| `TRANS-117` | انتقال شيدر: تشوه حراري | Shader transition: thermal-distortion | install | npm:three, npm:hyperframes |
| `TRANS-118` | انتقال شيدر: سوط كاميرا | Shader transition: whip-pan | install | npm:three, npm:hyperframes |
| `TRANS-119` | مسح بانقسام الألوان | Chromatic Aberration Wipe | install | npm:hyperframes |
| `TRANS-120` | كشف الستارة المسرحية | Curtain Reveal | install | chromium, npm:hyperframes |
| `TRANS-121` | قطع على المنحنى | Cut the Curve | install | chromium, npm:hyperframes |
| `TRANS-122` | دفع اتجاهي | Directional Wipe | install | chromium, npm:hyperframes |
| `TRANS-123` | تلاشي عبر لون | Fade Through | install | chromium, npm:hyperframes |
| `TRANS-124` | انتقال البكسلة | Grid Pixelate Wipe | install | chromium, npm:hyperframes |
| `TRANS-125` | ذوبان الهافتون | Halftone Dissolve | install | chromium, npm:hyperframes |
| `TRANS-126` | كشف القزحية | Iris Reveal | install | chromium, npm:hyperframes |
| `TRANS-127` | قطع مطابق | Match Cut | install | chromium, npm:hyperframes |
| `TRANS-128` | تبادل بالتحول | Morph Swap | install | chromium, npm:hyperframes |
| `TRANS-129` | انزلاق الصفحة | Page Slide | install | chromium, npm:hyperframes |
| `TRANS-130` | الشريط المطاطي | Rubber Band Bumper | install | chromium, npm:hyperframes |
| `TRANS-131` | محور مشترك عمودي | Shared Axis Y | install | chromium, npm:hyperframes |
| `TRANS-132` | محور مشترك عمقي | Shared Axis Z | install | chromium, npm:hyperframes |
| `TRANS-133` | قطع مطابق للنص | Text Match Cut | install | chromium, npm:hyperframes |
| `TRANS-134` | قطع مطابق بالعنوان | Type Match Cut | install | chromium, npm:hyperframes |
| `TRANS-135` | قطع السوط | Whip Pan Cut | install | chromium, npm:hyperframes |
| `TRANS-136` | انتقال عبر التكبير | Zoom Through Transition | install | npm:hyperframes |
| `TRANS-137` | انتقال شيدر الانقسام الشعاعي | Chromatic Radial Split | install | npm:three, npm:gsap, npm:hyperframes |
| `TRANS-138` | انتقال الزووم السينمائي | Cinematic Zoom | install | npm:three, npm:gsap, npm:hyperframes |
| `TRANS-139` | انتقال الالتواء المتقاطع | Cross Warp Morph | install | npm:three, npm:gsap, npm:hyperframes |
| `TRANS-140` | انتقال التواء النطاق | Domain Warp Dissolve | install | npm:three, npm:gsap, npm:hyperframes |
| `TRANS-141` | انتقال الوميض الأبيض | Flash Through White | install | npm:three, npm:gsap, npm:hyperframes |
| `TRANS-142` | انتقال الغليتش | Glitch | install | npm:three, npm:gsap, npm:hyperframes |
| `TRANS-143` | انتقال العدسة الجاذبية | Gravitational Lens | install | npm:three, npm:gsap, npm:hyperframes |
| `TRANS-144` | انتقال تسرب الضوء | Light Leak | install | npm:three, npm:gsap, npm:hyperframes |
| `TRANS-145` | انتقال جدار الكلمات | Text Clone Wall Transition | install | npm:gsap, npm:hyperframes |
| `TRANS-146` | انتقال الحرق المتعرج | Ridged Burn | install | npm:three, npm:gsap, npm:hyperframes |
| `TRANS-147` | انتقال التموجات | Ripple Waves | install | npm:three, npm:gsap, npm:hyperframes |
| `TRANS-148` | انتقال قزحية SDF | SDF Iris | install | npm:three, npm:gsap, npm:hyperframes |
| `TRANS-149` | انتقال الدوامة | Swirl Vortex | install | npm:three, npm:gsap, npm:hyperframes |
| `TRANS-150` | انتقال السراب الحراري | Thermal Distortion | install | npm:three, npm:gsap, npm:hyperframes |
| `TRANS-151` | انتقالات ثلاثية الأبعاد | 3D Transitions | install | npm:gsap, npm:hyperframes |
| `TRANS-152` | انتقالات الضبابية | Blur Transitions | install | npm:gsap, npm:hyperframes |
| `TRANS-153` | انتقالات التغطية | Cover Transitions | install | npm:gsap, npm:hyperframes |
| `TRANS-154` | انتقالات التدمير | Destruction Transitions | install | npm:gsap, npm:hyperframes |
| `TRANS-155` | انتقالات الذوبان | Dissolve Transitions | install | npm:gsap, npm:hyperframes |
| `TRANS-156` | انتقالات التشويه | Distortion Transitions | install | npm:gsap, npm:hyperframes |
| `TRANS-157` | انتقالات الشبكة | Grid Transitions | install | npm:gsap, npm:hyperframes |
| `TRANS-158` | انتقالات الضوء | Light Transitions | install | npm:gsap, npm:hyperframes |
| `TRANS-159` | انتقالات ميكانيكية | Mechanical Transitions | install | npm:gsap, npm:hyperframes |
| `TRANS-160` | انتقالات متنوعة | Other Transitions | install | npm:gsap, npm:hyperframes |
| `TRANS-161` | انتقالات الدفع | Push Transitions | install | npm:gsap, npm:hyperframes |
| `TRANS-162` | انتقالات شعاعية | Radial Transitions | install | npm:gsap, npm:hyperframes |
| `TRANS-163` | انتقالات الحجم | Scale Transitions | install | npm:gsap, npm:hyperframes |
| `TRANS-164` | انتقال البوابة | Portal | install | chromium, npm:three, npm:gsap, npm:hyperframes |
| `TRANS-165` | تحطم الزجاج | Shatter | install | chromium, npm:three, npm:gsap, npm:hyperframes |
| `TRANS-166` | انتقال شيدر السوط | Whip Pan | install | npm:three, npm:gsap, npm:hyperframes |
| `TRANS-167` | نمط انتقال الشيدر من الصفحة | DOM-to-texture shader transition pattern | install | npm:three, npm:gsap |
| `TRANS-168` | المسح بالقناع وتقسيم الشاشة | Clip-path wipe and split-screen | install | npm:gsap |
| `TRANS-169` | مزج متقاطع للصورة والصوت | Crossfade with opposing volume envelopes | install |  |
| `TRANS-170` | تشويش انقسام الألوان والشرائح | Chromatic RGB-split / slice glitch | install | npm:gsap, npm:hyperframes |
| `TRANS-171` | تبديل بالتحجيم في نفس المركز | Scale swap morph | install | npm:gsap, npm:hyperframes |
| `TRANS-172` | تبديل السمة حول عنصر ثابت | Theme crossfade morph under fixed anchor | install | npm:gsap, npm:hyperframes |
| `TRANS-173` | انتقال CSS: دفع انزلاقي | CSS transition: Push slide | install | npm:gsap, npm:hyperframes |
| `TRANS-174` | انتقال CSS: دفع عمودي | CSS transition: Vertical push | install | npm:gsap, npm:hyperframes |
| `TRANS-175` | انتقال CSS: دفع مرن | CSS transition: Elastic push | install | npm:gsap, npm:hyperframes |
| `TRANS-176` | انتقال CSS: ضغط | CSS transition: Squeeze | install | npm:gsap, npm:hyperframes |
| `TRANS-177` | انتقال CSS: قزحية دائرية | CSS transition: Circle iris | install | npm:gsap, npm:hyperframes |
| `TRANS-178` | انتقال CSS: قزحية ماسية | CSS transition: Diamond iris | install | npm:gsap, npm:hyperframes |
| `TRANS-179` | انتقال CSS: انقسام قطري | CSS transition: Diagonal split | install | npm:gsap, npm:hyperframes |
| `TRANS-180` | انتقال CSS: قلب البطاقة ثلاثي الأبعاد | CSS transition: 3D card flip | install | npm:gsap, npm:hyperframes |
| `TRANS-181` | انتقال CSS: اختراق بالتقريب | CSS transition: Zoom through | install | npm:gsap, npm:hyperframes |
| `TRANS-182` | انتقال CSS: تبعيد | CSS transition: Zoom out | install | npm:gsap, npm:hyperframes |
| `TRANS-183` | انتقال CSS: تلاشي متقاطع | CSS transition: Crossfade | install | npm:gsap, npm:hyperframes |
| `TRANS-184` | انتقال CSS: تلاشي مع ضبابية | CSS transition: Blur crossfade | install | npm:gsap, npm:hyperframes |
| `TRANS-185` | انتقال CSS: سحب التركيز | CSS transition: Focus pull | install | npm:gsap, npm:hyperframes |
| `TRANS-186` | انتقال CSS: غمس لوني إلى الأسود | CSS transition: Color dip | install | npm:gsap, npm:hyperframes |
| `TRANS-187` | انتقال CSS: كتل لونية متتابعة | CSS transition: Staggered color blocks | install | npm:gsap, npm:hyperframes |
| `TRANS-188` | انتقال CSS: ستائر أفقية | CSS transition: Horizontal blinds | install | npm:gsap, npm:hyperframes |
| `TRANS-189` | انتقال CSS: ستائر عمودية | CSS transition: Vertical blinds | install | npm:gsap, npm:hyperframes |
| `TRANS-190` | انتقال CSS: تسرب ضوئي | CSS transition: Light leak | install | npm:gsap, npm:hyperframes |
| `TRANS-191` | انتقال CSS: حرق بالتعريض الزائد | CSS transition: Overexposure burn | install | npm:gsap, npm:hyperframes |
| `TRANS-192` | انتقال CSS: حرق الفيلم | CSS transition: Film burn | install | npm:gsap, npm:hyperframes |
| `TRANS-193` | انتقال CSS: تشويش رقمي | CSS transition: Glitch | install | npm:gsap, npm:hyperframes |
| `TRANS-194` | انتقال CSS: زيغ لوني | CSS transition: Chromatic aberration | install | npm:gsap, npm:hyperframes |
| `TRANS-195` | انتقال CSS: تموج | CSS transition: Ripple | install | npm:gsap, npm:hyperframes |
| `TRANS-196` | انتقال CSS: شريط VHS | CSS transition: VHS tape | install | npm:gsap, npm:hyperframes |
| `TRANS-197` | انتقال CSS: مصراع | CSS transition: Shutter | install | npm:gsap, npm:hyperframes |
| `TRANS-198` | انتقال CSS: مسح كعقرب الساعة | CSS transition: Clock wipe | install | npm:gsap, npm:hyperframes |
| `TRANS-199` | انتقال CSS: تحلل شبكي | CSS transition: Grid dissolve | install | npm:gsap, npm:hyperframes |
| `TRANS-200` | انتقال CSS: سقوط بالجاذبية | CSS transition: Gravity drop | install | npm:gsap, npm:hyperframes |
| `TRANS-201` | انتقال CSS: دائرة متحولة | CSS transition: Morph circle | install | npm:gsap, npm:hyperframes |
| `TRANS-202` | انتقال CSS: عبور بالضبابية | CSS transition: Blur through | install | npm:gsap, npm:hyperframes |
| `TRANS-203` | انتقال CSS: ضبابية اتجاهية | CSS transition: Directional blur | install | npm:gsap, npm:hyperframes |
| `TRANS-204` | انتقال CSS: احتراق الصفحة | CSS transition: Page burn | install | npm:gsap, npm:hyperframes |
| `TRANS-205` | انتقال شيدر WebGL: انقسام لوني | WebGL shader transition: chromatic-split | install | npm:three, npm:hyperframes |
| `TRANS-206` | انتقال شيدر WebGL: تقريب سينمائي | WebGL shader transition: cinematic-zoom | install | npm:three, npm:hyperframes |
| `TRANS-207` | انتقال شيدر WebGL: تحول بالتشويه المتقاطع | WebGL shader transition: cross-warp-morph | install | npm:three, npm:hyperframes |
| `TRANS-208` | انتقال شيدر WebGL: تشويه المجال | WebGL shader transition: domain-warp | install | npm:three, npm:hyperframes |
| `TRANS-209` | انتقال شيدر WebGL: وميض عبر الأبيض | WebGL shader transition: flash-through-white | install | npm:three, npm:hyperframes |
| `TRANS-210` | انتقال شيدر WebGL: عدسة جاذبية | WebGL shader transition: gravitational-lens | install | npm:three, npm:hyperframes |
| `TRANS-211` | انتقال شيدر WebGL: تسرب ضوئي | WebGL shader transition: light-leak | install | npm:three, npm:hyperframes |
| `TRANS-212` | انتقال شيدر WebGL: حرق متشقق | WebGL shader transition: ridged-burn | install | npm:three, npm:hyperframes |
| `TRANS-213` | انتقال شيدر WebGL: موجات متموجة | WebGL shader transition: ripple-waves | install | npm:three, npm:hyperframes |
| `TRANS-214` | انتقال شيدر WebGL: قزحية SDF | WebGL shader transition: sdf-iris | install | npm:three, npm:hyperframes |
| `TRANS-215` | انتقال شيدر WebGL: دوامة | WebGL shader transition: swirl-vortex | install | npm:three, npm:hyperframes |
| `TRANS-216` | انتقال شيدر WebGL: تشوه حراري | WebGL shader transition: thermal-distortion | install | npm:three, npm:hyperframes |
| `TRANS-217` | انتقال شيدر WebGL: حركة سوط سريعة | WebGL shader transition: whip-pan | install | npm:three, npm:hyperframes |
| `TRANS-218` | مطابقة الانتقال مع الطاقة والمزاج | Transition energy and mood mapping | install |  |
| `TRANS-219` | سجل الانتقالات والحقن الآلي | Transition registry and auto-injection | install | npm:gsap |
| `TRANS-220` | انتقالات بسرعات متطابقة | Velocity-matched transitions | install |  |
| `TRANS-221` | حركة إيقاعية: hypercut-whip | Beat motion primitive: hypercut-whip | install | npm:gsap |
| `TRANS-222` | حركة إيقاعية: mask-reveal | Beat motion primitive: mask-reveal | install | npm:gsap |
| `TRANS-223` | حركة إيقاعية: iris-open | Beat motion primitive: iris-open | install | npm:gsap |
| `TRANS-224` | حركة إيقاعية: blur-resolve | Beat motion primitive: blur-resolve | install | npm:gsap |
| `TRANS-225` | حركة إيقاعية: flash-cut | Beat motion primitive: flash-cut | install | npm:gsap |
| `TRANS-226` | حركة إيقاعية: hard-cut | Beat motion primitive: hard-cut | install | npm:gsap |
| `TRANS-227` | حركة إيقاعية: staggered-exit | Beat motion primitive: staggered-exit | install | npm:gsap |
| `TRANS-228` | قطوعات داخل اللقطة | Within-frame seam cuts (zoom-through, inverse zoom, cut-the-curve, waterfall) | install |  |
| `TRANS-229` | إعادة الاستهداف بالنابض | Spring retargeting track() | install |  |
| `TRANS-230` | تبديل البؤرة | rackFocus | install |  |
| `TRANS-231` | انتقال القزحية والفيضان | iris / flood seams | install |  |
| `TRANS-232` | انقلاب ثلاثي | roll 3D flip seam | install |  |
| `TRANS-233` | قلب قطبية المسرح | polarity stage flip | install |  |
| `TRANS-234` | دخول تدريجي بالتعريض | Exposure fade-in from black | install |  |
| `TRANS-235` | ومضة بيضاء | White flash accent | install |  |
| `TRANS-236` | فتح قزحي من نقطة إلى اللقطة | Iris open from a point onto footage | install |  |
| `TRANS-237` | الكلمة كسطح انتقال | Word as the transition plane | install |  |
| `TRANS-238` | لقطة إلى بطاقة إلى انهيار إلى شعار | Footage → card → implode → lockup | install | npm:gsap |
| `TRANS-239` | خاتمة بالغطس إلى الأسود | Dip to black / dip to ink ending | install |  |
| `TRANS-240` | شريطا السينما يفتحان ويغلقان | Cinematic letterbox open/close | install |  |
| `TRANS-241` | قطع حاد مع إعادة تأطير الكاميرا | Hard cut with camera reframe | install | npm:gsap |
| `TRANS-242` | ضربة القطع: تمويه شعاعي ووميض | Cut kick (radial blur on cuts) + white flash | install |  |
| `TRANS-243` | إيقاع الإظلام مع تداخل النص | Fade-through-black rhythm with overlapping text | install |  |
| `TRANS-244` | شاشة مقسومة للمقارنة | Split-screen comparison with whip-in halves | install |  |
| `TRANS-245` | إظلام الختام ووميض الانتقال | Dip to black end + white flash seams | install |  |
| `TRANS-246` | كشف دائري وفيضان لوني | Iris reveal and colour flood | install |  |
| `TRANS-247` | انتقال تطبيقات الموبايل: سوايب سريع | Phone-editor transition: whip (whipleft/whipright/whipup/whipdown) | install | pip:opencv, pip:scipy |
| `TRANS-248` | 54 انتقال xfade بالبايثون | 54 xfade transitions in Python | install | ffmpeg, python3 |
| `TRANS-249` | ويب يسار | Phone-editor transition: whipleft | install |  |
| `TRANS-250` | ويب يمين | Phone-editor transition: whipright | install |  |
| `TRANS-251` | ويب أعلى | Phone-editor transition: whipup | install |  |
| `TRANS-252` | ويب أسفل | Phone-editor transition: whipdown | install |  |
| `TRANS-253` | وميض | Flash frame | install |  |
| `TRANS-254` | انتقال القزحية | Iris wipe | install |  |
| `TRANS-255` | قلب ثلاثي الأبعاد | Front-loaded 3D roll | install |  |
| `TRANS-256` | تسلسل اللقطات | Shot list sequence with hard cuts | install |  |
| `TRANS-257` | انتقالات القزحية والبطاقة والانضغاط | Iris / card / implode transitions (showreel) | install | npm:gsap |
| `TRANS-258` | الكلمة المفتاحية كمستوى انتقال | Keyword as transition plane | install |  |
| `TRANS-259` | تلاشي حواف المشهد | sceneFade edge fades | install |  |
| `TRANS-260` | إطارات تحت المقاطع | Poster frames under clips with zoom | install |  |
| `TRANS-86` | كلمة الفصل كانتقال | Chapter keyword transition plane | install |  |
| `TRANS-87` | خط الضوء الفاصل | Section rule of light | install |  |
| `TRANS-88` | انتقال تطبيقات الموبايل: تمويه متداخل | Phone-editor transition: blurcross | install | pip:opencv, pip:scipy |
| `TRANS-89` | انتقال تطبيقات الموبايل: زووم + تمويه (CapCut Zoom) | Phone-editor transition: zoomblur | install | pip:opencv, pip:scipy |
| `TRANS-90` | انتقال تطبيقات الموبايل: زووم للخارج + تمويه | Phone-editor transition: zoomblurout | install | pip:opencv, pip:scipy |
| `TRANS-91` | انتقال تطبيقات الموبايل: دوران | Phone-editor transition: spin | install | pip:opencv, pip:scipy |
| `TRANS-92` | انتقالات الشيدر | Shader transitions (WebGL) | install | npm:three, npm:hyperframes |
| `TRANS-93` | حساب مدة الانتقالات | TransitionSeries math | install |  |
| `TRANS-94` | واجهة انتقالات العرض | View Transitions API | install | chromium, npm:react |
| `TRANS-95` | انتقال بقناع ضوضاء | Noise-mask scene transition (FBO) | install |  |
| `TRANS-96` | متى نستخدم انتقال شيدر أو CSS أو قطع حاد | When to use shader vs CSS vs hard cut | install | npm:hyperframes |
| `TRANS-97` | ذوبان ضوضائي بين مشهدين | Noise-dissolve between two rendered scenes | install | chromium, npm:three |
| `TRANS-98` | انتقال المسح بطبقة غطاء | Overlay wipe page transition | install | npm:gsap |
| `TRANS-99` | انتقال تحلل بالنويز بين مشهدين | Noise-dissolve scene transition | install |  |
| `CAM-181` | رياضيات كاميرا التحليق | Flyover camera math | key | key:unspecified |
| `CAM-182` | مفردات التكوين وترك فراغ للنص | Composition keywords that reserve space for type | key | key:unspecified |
| `CAM-183` | مفردات حركة الكاميرا لنماذج الفيديو | Camera-move vocabulary for video models | key | key:video-gen |
| `CAM-184` | التحكم البسيط بالكاميرا في كلينج | Kling simple camera control | key | key:video-gen |
| `CAM-185` | تأطير الإطار الأول لكل مقطع بدل حركة الكاميرا | First-frame framing per segment (not camera motion) | key | key:unspecified |
| `CAM-186` | تتبع الشخص في القص | Subject-follow reframing (bridge cv2) | key | pip:opencv, key:unspecified |
| `CAM-187` | حركة كاميرا: luxury product | Camera grammar: luxury product | key | key:unspecified |
| `CAM-188` | حركة كاميرا: real estate | Camera grammar: real estate | key | key:unspecified |
| `CAM-189` | حركة كاميرا: industrial | Camera grammar: industrial | key | key:unspecified |
| `CAM-190` | حركة كاميرا: travel | Camera grammar: travel | key | key:unspecified |
| `CAM-191` | حركة كاميرا: food/craft | Camera grammar: food/craft | key | key:unspecified |
| `CAM-192` | حركة كاميرا: miniature | Camera grammar: miniature | key | key:unspecified |
| `CAM-193` | انزلاق إيزومتري ثابت | Locked-iso glide | key | key:unspecified |
| `CAM-194` | معماريتا اللقطة المتصلة | Architecture A continuous take vs B dive+connector | key | key:unspecified |
| `CHAR-06` | ثبات الشخصية في التوليد بالمراجع | Reference-based consistency in generators | key | key:openai |
| `CHAR-07` | شريط حركة كامل من إطار واحد | Whole-strip sprite from one seed frame | key | key:unspecified |
| `CHAR-08` | الأفاتار الناطق | AI talking avatars | key | key:unspecified |
| `CHAR-50` | صفحات ويبتون بشخصيات حيوانية | Webtoon pages with Arabic overlay | key | key:unspecified |
| `FMT-19` | نسخ الصور متعددة المقاسات بخدمة Adobe | Multi-ratio still variations via Adobe | key | key:unspecified |
| `FMT-40` | إرسال الفيلم على واتساب | WhatsApp media delivery container | key | node, key:unspecified |
| `FMT-41` | روابط خاصة مستضافة وعمليات Cloudinary | Hosted private links & Cloudinary URL ops | key | ffmpeg, npm:hyperframes, claude:tools |
| `STORY-85` | وكلاء الإبداع الفرعيون وقرارات Jev | Creative sub-agents & Jev decisions | key | claude:tools |
| `TRANS-261` | لقطات بإطار أول وأخير (انتقال تحوّلي) | First-and-last-frame keyframe shots (AI morph transition) | key | key:video-gen |
| `CAM-407` | اهتزاز 2 بكسل | 2-px screen shake once | idea |  |
| `CAM-408` | دفع مع اهتزاز يدوي | Push + handheld drift camera | idea |  |
| `CAM-409` | شبكة ثابتة للمحاذاة | Persistent snap grid | idea |  |
| `CAM-410` | دفع بطيء للكاميرا | Gentle camera push/pan | idea |  |
| `CAM-411` | دولي في الكورس | Chorus dolly | idea |  |
| `CAM-412` | كاميرا تتبع متأخرة | Ball-tracking lag camera | idea |  |
| `CAM-413` | شريط سينمائي | 2.35:1 letterbox | idea |  |
| `CAM-414` | تقريب وذروة | Climax zoom and hit shake | idea |  |
| `CAM-415` | كاميرا 2.5D | 2.5D parallax UI camera | idea |  |
| `CAM-416` | زوم صادم لحظي | Single-frame punch-in | idea |  |
| `CAM-417` | زوم نفقي ثابت | Constant-rate tunnel zoom | idea |  |
| `CAM-418` | كاميرا ثابتة ودفعتان | Static cam with two push-ins | idea |  |
| `CAM-419` | عمق بالمقياس والظل | Locked cam, depth by scale+shadow | idea |  |
| `CAM-420` | بارالاكس طبقتين | Two-layer grid parallax | idea |  |
| `CAM-421` | لقطة واحدة | One-shot slow push | idea |  |
| `TRANS-443` | تقنيات السرد بالتمرير كحركات فيديو | Scrollytelling techniques as video moves | idea |  |
| `TRANS-444` | قلب صفحة | Paper-curl page flip | idea |  |
| `TRANS-445` | قطع على 120 نبضة | Hard cuts on 120 BPM | idea |  |
| `TRANS-446` | مسح دائري للثيم | Radial theme wipe | idea |  |
| `TRANS-447` | مزج 400 مللي | Vertical 400 ms dissolve only | idea |  |
| `TRANS-448` | قطع مطابق بالتكبير | Scale match-cut one-take | idea |  |
| `TRANS-449` | كشف بقناع | Masked axis-alternating reveals | idea |  |
| `TRANS-450` | حد المزج | Dissolve cap 150 ms | idea |  |
| `TRANS-451` | كشف قبل وبعد | Before/after wipe reveal | idea |  |
| `TRANS-452` | انخفاض مظلم | Dark-dip camera reset | idea |  |
| `TRANS-453` | قطع على كل ضربة | Beat-locked hard cuts | idea | npm:remotion |
| `TRANS-454` | انتقال بالتحول | Seed morph transitions | idea | npm:gsap |
| `TRANS-455` | تحريك سوطي | Whip-pan 180 ms | idea |  |
| `TRANS-456` | مزج بالتحريك | Stir gradient collapse blend | idea |  |
| `TRANS-457` | تحول الفصول | Element-reborn chapter morphs | idea |  |
| `TRANS-458` | انتقال بلا قطع | Morph/mask wipe/scale-through only | idea |  |
| `TRANS-459` | تحول الحاوية | Container morph loop | idea |  |
| `TRANS-460` | انزلاق مع تلاشي | Slide-up crossfade | idea |  |
