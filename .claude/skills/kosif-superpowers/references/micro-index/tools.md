# الأدوات القابلة للتشغيل / Runnable tools

[← الفهرس الدقيق / micro index](README.md)

## الفهرس / contents

- [3d](#3d)
- [audio](#audio)
- [discover](#discover)
- [draw](#draw)
- [edit](#edit)
- [image](#image)
- [investigate](#investigate)
- [local-computer](#local-computer)
- [maintain](#maintain)
- [motion](#motion)
- [sources](#sources)
- [think](#think)

## 3d

| tool | ID | الأداة / tool | أمر أول / first command | tests |
|---|---|---|---|---|
| `blender-api-audit` | TOOL-36 | تدقيق واجهة بايثون في Blender · Blender Python API audit | `python3 scripts/blender_api_audit.py --help` | 1 |
| `blender-bridge` | TOOL-37 | جسر Blender الآمن · Safe headless Blender bridge | `python3 scripts/blender_bridge.py doctor` | 1 |
| `blender-cat-fur-upgrade` | TOOL-121 | تطوير فرو القطة والملامح في Blender Cycles · Blender Cat Fur Upgrade: renderable hair geometry and character detail | `blender --background --factory-startup --disable-autoexec --python-ex…` | 1 |
| `blender-cinema` | TOOL-87 | رندر سينمائي بـBlender Cycles · Blender Cycles cinematic renders | `python3 scripts/blender_cinema.py doctor` | 1 |
| `blender-cinematic-bridge` | TOOL-119 | دمج رندر Blender Cycles مع مونتاج KOSIF والصوت · Blender Cycles + KOSIF Cinematic compositor | `python3 scripts/blender_cinematic_bridge.py doctor` | 2 |
| `blender-cycles-render` | TOOL-38 | رندر Cycles إلى فيديو مُتحقَّق منه · Cycles scene to verified video | `python3 scripts/blender_cycles_render.py doctor` | 1 |
| `blender-motion-video` | TOOL-114 | مساعد فيديو الحركة في Blender · Blender motion video helper | `python3 scripts/blender_motion_video.py --help` | 0 |
| `blender-rescue-scene` | TOOL-120 | إنشاء مشهد إنقاذ قطة ثلاثي الأبعاد داخل Blender · Create an editable Blender 3D cat rescue demo | `blender --background --factory-startup --disable-autoexec --python-ex…` | 1 |
| `blender-worker` | TOOL-39 | منفّذ المشهد داخل Blender · Blender-side scene builder | `blender --background --factory-startup --disable-autoexec --python-ex…` | 1 |
| `native-3d` | TOOL-40 | رندر ثلاثي الأبعاد مستقل عن Blender · Native 3D renderer (no Blender) | `python3 scripts/native_3d.py doctor` | 3 |
| `native-glb` | TOOL-41 | مُصدِّر GLB مستقل عن Blender · Native GLB exporter (no Blender) | `python3 scripts/native_glb.py --scene templates/blender-demo.json --o…` | 1 |

## audio

| tool | ID | الأداة / tool | أمر أول / first command | tests |
|---|---|---|---|---|
| `audio-cue-mapper` | TOOL-25 | مستخرج إشارات التوقيت من الصوت · WAV audio cue mapper | `python3 scripts/audio_cue_mapper.py ./voice.wav --out ./out/cues.json` | 1 |
| `caption-lines` | TOOL-165 | سطور الترجمة: من توقيت الكلمات إلى ترجمة مقروءة · Caption lines: word timings to readable SRT/VTT | `python3 scripts/caption_lines.py group words.json -o captions.srt --r…` | 1 |
| `music-rhythm-engine` | TOOL-26 | فرضيات إيقاع الموسيقى · Music rhythm hypotheses | `python3 scripts/music_rhythm_engine.py ./out/cues.json --out ./out/rh…` | 1 |
| `repo-words-convert` | TOOL-86 | محوّل الترجمات إلى توقيت الكلمات · Subtitle to words.json converter | `python3 tools/words_convert.py ./captions.srt ./words.json` | 1 |
| `tts-script` | TOOL-152 | تجهيز نص التعليق الصوتي: تقطيع آمن وتقدير المدة وSSML · TTS script prep: prosody-safe chunks, duration estimate and SSML | `printf 'مرحبا بكم في KOSIF Studio. هذا اختبار، قصير جدا!\n\nفقرة ثاني…` | 1 |

## discover

| tool | ID | الأداة / tool | أمر أول / first command | tests |
|---|---|---|---|---|
| `ai-tool-discovery` | TOOL-01 | باحث القدرات ثنائي اللغة بلا اتصال · Offline bilingual capability finder | `python3 scripts/ai_tool_discovery.py "تحريك شخصيات فيديو" --top 8` | 1 |
| `atlas-5000` | TOOL-106 | خريطة تغطية أطلس الـ5000 مهارة · Atlas-5000 coverage map | `python3 scripts/atlas_5000.py stats --json` | 1 |
| `atlas-capability-miner` | TOOL-105 | منقّب قدرات الأطلس من البيانات الوصفية · Atlas metadata capability miner | `python3 scripts/atlas_capability_miner.py --help` | 1 |
| `atlas-ledger` | TOOL-107 | سجل الأطلس: حالة واحدة لكل مهارة · Atlas ledger: one status for every Atlas skill | `python3 scripts/atlas_ledger.py stats --json` | 1 |
| `atlas-task-method-router` | TOOL-112 | موجّه مناهج الأطلس حسب المهمة · Atlas task method router | `python3 scripts/atlas_task_method_router.py --help` | 0 |
| `boot` | TOOL-02 | إحاطة بدء الجلسة · Session boot briefing | `python3 scripts/boot.py` | 1 |
| `capability-atlas` | TOOL-03 | أطلس القدرات للبحث والتخطيط · Capability Atlas search and planner | `python3 scripts/capability_atlas.py stats --json` | 1 |
| `capability-graph` | TOOL-34 | باني خريطة القدرات المترابطة · Capability Graph Builder | `python3 scripts/capability_graph.py build` | 1 |
| `capability-runtime-router` | TOOL-04 | موجّه القدرات التنفيذية · Capability runtime router | `python3 scripts/capability_runtime_router.py --task "حلل فيديو مرجعي…` | 1 |
| `fusionforge` | TOOL-125 | FusionForge v2 لوصفات الـWorkflow المركبة داخل المشروع · FusionForge v2 project-scoped composite workflow recipes | `python3 scripts/fusionforge.py propose "مونتاج ريلز بترجمة عربية" --p…` | 2 |
| `fusionforge-shared` | TOOL-126 | ذاكرة FusionForge المشتركة بوصفات مهارات معزولة · FusionForge Shared Memory: reviewed cross-project skill structures | `python3 scripts/fusionforge_shared.py audit` | 1 |
| `hub` | TOOL-05 | بوابة KOSIF الموحّدة · KOSIF hub (front door) | `python3 scripts/hub.py find "اعمل فيديو موشن عربي متزامن مع صوتي"` | 1 |
| `kosif-groups` | TOOL-129 | خريطة المجموعات مع القدرات الخارقة والسكربتات وخطط التثبيت · Group map with superpowers, scripts and install plans | `python3 scripts/kosif_hubs.py` | 1 |
| `kosif-mcp` | TOOL-06 | خادم MCP لكتالوج KOSIF · KOSIF catalog MCP server | `python3 scripts/kosif_mcp.py` | 1 |
| `local-first` | TOOL-07 | مدخل محلي بلا استنساخ · Local-first no-clone entry | `python3 scripts/local_first.py doctor` | 1 |
| `micro-index` | TOOL-161 | الفهرس الدقيق: سطر لكل قدرة وأداة وقدرة خارقة · Micro index: one line per power, tool and superpower | `python3 scripts/micro_index.py build` | 1 |
| `owned-repos` | TOOL-143 | خريطة مستودعات المالك وخريطة المهارات · Owned-repositories map and skill map | `python3 scripts/owned_repos.py find "رسم شخصيات"` | 1 |
| `powers` | TOOL-156 | البحث في كتالوج القدرات · Power catalog search | `python3 scripts/powers.py stats --domain motion --json` | 3 |
| `probe-env` | TOOL-71 | فحص قدرات الجهاز · Machine capability probe | `python3 scripts/probe_env.py` | 0 |
| `python-package-probe` | TOOL-08 | فاحص وجود حزم بايثون · Python package presence probe | `python3 scripts/python_package_probe.py pandas numpy httpx` | 1 |
| `repo-kosif` | TOOL-73 | أداة سطر أوامر لأطلس أنماط KOSIF · KOSIF style atlas CLI | `python3 tools/kosif.py list --category charts --limit 10` | 2 |
| `requirements` | TOOL-72 | مخطط متطلبات القدرات · Power requirements planner | `python3 scripts/requirements.py present --json` | 1 |
| `skill-intelligence` | TOOL-124 | محرك بروتوكول ذكاء المهارات الشامل · Universal Skill Intelligence Protocol engine | `python3 scripts/skill_intelligence.py brief "مونتاج ريلز على الإيقاع…` | 3 |
| `skill-loader` | — | خريطة التحميل الخفيف للمهارات · Light skill loader map | `python3 scripts/skill_loader.py build --check` | 1 |
| `smart-capabilities` | TOOL-116 | فهرس ذكي للقدرات من أجل Claude · Smart capability index for Claude | `python3 scripts/smart_capabilities.py groups` | 1 |
| `superpower-fusion` | TOOL-127 | دمج القدرات في قدرات خارقة مترابطة · Superpower fusion (powers to connected superpowers) | `python3 scripts/superpower_fusion.py build` | 1 |
| `superpowers-unified` | TOOL-09 | موجّه مهارات العمل ومثبّتها · Process-skill router and installer | `python3 scripts/superpowers_unified.py doctor` | 1 |

## draw

| tool | ID | الأداة / tool | أمر أول / first command | tests |
|---|---|---|---|---|
| `brand-tokens` | TOOL-153 | رموز الهوية: ألوان الشعار ورموز بثلاث طبقات ومصفوفة تباين WCAG · Brand tokens: SVG palette, 3-tier design tokens and WCAG contrast matrix | `echo '<svg xmlns="http://www.w3.org/2000/svg"><rect fill="#1d4ed8"/><…` | 1 |
| `character-fullbody` | TOOL-27 | تحريك الشخصية بكامل الجسم · Full-body character animator | `python3 scripts/character_fullbody.py doctor` | 1 |
| `character-ik` | TOOL-28 | تحريك ذراع الشخصية بالحركية العكسية · Character IK arm animator | `python3 scripts/character_ik.py doctor` | 2 |
| `code-drawing-master` | TOOL-29 | رسم الشخصيات والمشاهد بالكود · Code Drawing Master storyboards | `python3 scripts/code_drawing_master.py --cast human+cat --expression…` | 1 |
| `color-media` | TOOL-169 | محرك الخامات الملوّنة: ألوان خشبية وفرشاة زيت وألوان مائية لأي صورة · Colour media engine: coloured pencil, oil brush and watercolour painting of a photo | `python3 scripts/color_media.py draw --photo in.png --out out/x --medi…` | 1 |
| `creative-paint` | TOOL-30 | الرسم الإبداعي بالطبقات · Creative Paint layered renderer | `python3 scripts/creative_paint.py doctor` | 3 |
| `creative-principles` | TOOL-134 | دراسة الرسم التدريجي والظل الأصلي · Staged drawing and original three-value visual studies | `python3 scripts/creative_principles.py construct --input original-sha…` | 1 |
| `diagram-layout` | TOOL-149 | تخطيط المخططات: فحص الرسم البياني وتخطيط طبقي حتمي وSVG جاهز للعربية · Diagram layout: graph lint, deterministic layered layout and RTL-ready SVG | `python3 scripts/diagram_layout.py lint /tmp/graph.json --max-label 24…` | 1 |
| `drawing-academy` | TOOL-135 | أكاديمية الرسم والدروس المبنية على مصادر · Source-aware drawing school and user-authorized book audits | `python3 scripts/drawing_academy.py index` | 1 |
| `drawing-council` | TOOL-158 | مجلس خبراء الرسم: أحد عشر خبيرًا من بطاقات الكتب الـ48 يراجعون الصورة قبل إرسالها · Drawing council: eleven experts from the 48 method cards review an image before it is sent | `python3 scripts/drawing_council.py roster --markdown` | 1 |
| `drawing-methods` | TOOL-136 | أطلس مناهج كتب الرسم مع رسم بنائي بالطبقات · Drawing-book methods atlas with layered construction SVGs | `python3 scripts/drawing_methods.py find "ارسم وش شخصية بتضحك"` | 1 |
| `drawing-visual-qa` | TOOL-144 | مدرب الرسم من فصول الكتب والتشخيص البصري المستقل · Book-chapter drawing coach and independent raster visual QA | `python3 scripts/drawing_visual_qa.py curriculum "ارسم شخصية كرتونية ب…` | 1 |
| `geo-plate` | TOOL-147 | لوح الخرائط: إسقاط الإحداثيات إلى بكسلات وتصنيف الخرائط الملونة وسجل المصادر · Map plate: projection to pixels, choropleth classes and source ledger | `python3 scripts/geo_plate.py project --proj equirect --size 2000x1000…` | 1 |
| `perspective-color-lab` | TOOL-137 | منظور هندسي ومقاييس التباين اللوني · Original two-point perspective and numeric palette analysis | `python3 scripts/perspective_color_lab.py perspective --input scene.js…` | 1 |
| `portrait-pipeline` | TOOL-157 | نسخة مرسومة أو ملوّنة باليد لأي صورة أو مشهد متخيَّل: رصاص، فحم، حبر، ألوان خشبية، فرشاة زيت أو ألوان مائية · Hand-drawn or hand-painted version of any photo or imagined scene: pencil, charcoal, ink, coloured pencil, oil brush or watercolour | `python3 scripts/portrait_pipeline.py draw --photo photo.png --out out…` | 1 |
| `smart-draw` | TOOL-31 | الرسم الذكي ومساعد الأشكال · Smart Draw shape assist | `python3 scripts/smart_draw.py doctor` | 1 |
| `unified-draw` | TOOL-115 | الرسم الموحد: خطوط وأشكال وطبقات وتصدير · Unified Draw: freehand + geometry + layered export | `python3 scripts/unified_draw.py doctor` | 2 |

## edit

| tool | ID | الأداة / tool | أمر أول / first command | tests |
|---|---|---|---|---|
| `cinema-lab` | TOOL-175 | معمل السينما: كشف القطعات، حذف الصمت، تايملاين OTIO/EDL، ألوان LUT، تثبيت الكاميرا، تأطير ذكي بالطول، حركة كاميرا، مراجعة A/B · Cinema Lab: scene cuts, silence cut, OTIO/EDL timelines, LUT looks, stabilise, smart portrait reframe, camera moves, A/B review | `python3 scripts/cinema_lab.py doctor` | 1 |
| `cinematic-broll-render` | TOOL-19 | تصيير لقطات B-roll بحركة كاميرا · Cinematic B-roll Renderer | `python3 scripts/cinematic_broll_render.py --edl ./edl.json --manifest…` | 1 |
| `cinematic-cut-planner` | TOOL-20 | مُخطِّط قطعات اللقطات الحقيقية · Footage-First Cut Planner | `python3 scripts/cinematic_cut_planner.py --words ./words.json --clips…` | 2 |
| `creative-quality-gate` | TOOL-35 | بوابة جودة خطة المونتاج · Reference-edit structural quality gate | `python3 scripts/creative_quality_gate.py ./my-project/src/plan.json -…` | 1 |
| `dua-wednesday` | TOOL-132 | دعاء يوم الأربعاء — محرك ريل دعاء موشن جرافيك 9:16 · Wednesday-morning dua reel (دعاء يوم الأربعاء) — 9:16 motion-graphics dua engine | `python3 scripts/dua_wednesday.py doctor` | 1 |
| `fast-edit` | TOOL-168 | التعديل السريع: قص فوري يعرف الإطارات المفتاحية، مغيّر صوت، تفتيح الفيديو المظلم، استخراج الصوت · Fast Edit: keyframe-aware instant cut, voice presets, low-light lift, audio extract | `python3 scripts/fast_edit.py doctor` | 1 |
| `kosif-timeline` | TOOL-122 | محرر KOSIF Timeline: مونتاج متعدد المسارات مع تراجع وإعادة · KOSIF Timeline: genuine multitrack video, image and audio editor | `python3 scripts/kosif_timeline.py doctor` | 1 |
| `kosif-timeline-demo` | TOOL-123 | تجربة مونتاج KOSIF Timeline تلقائية بملفات أصلية مولدة · KOSIF Timeline one-command synthetic media demo | `python3 scripts/kosif_timeline_demo.py --dir ./fresh-kosif-timeline-d…` | 1 |
| `look-pipeline` | TOOL-166 | خط اللوك: تلوين واحد لـ ffmpeg وSVG وGLSL · Look pipeline: one colour grade for ffmpeg, SVG/CSS and GLSL | `python3 scripts/look_pipeline.py presets` | 1 |
| `mimic` | TOOL-85 | محرك محاكاة الفيديو المرجعي · KOSIF Mimic reference rebuilder | `python3 -c "import sys; sys.path.insert(0,'scripts/mimic'); import mm…` | 1 |
| `montage-pro` | TOOL-130 | فريق مونتاج برو (صوت أو فيديو إلى مونتاج أو موشن) · Montage Pro task force (audio/video to montage or motion) | `python3 scripts/montage_pro.py doctor` | 1 |
| `motion-reference-probe` | TOOL-21 | فاحص توقيت الفيديو المرجعي · Reference Video Timing Probe | `python3 scripts/motion_reference_probe.py ./in.mp4` | 2 |
| `reel-factory` | TOOL-131 | مصنع الريلز: صوت وتوقيت كلمات ولقطات مرخصة ← ريلز 9:16 مفحوص · Reel factory: voice + word timings + licensed shots → verified 9:16 reel | `python3 scripts/reel_factory.py plan --audio ./voice.m4a --audio-righ…` | 1 |
| `reference-edit-engine` | TOOL-22 | محرك إعادة بناء المونتاج المرجعي · Reference Edit Engine | `python3 scripts/reference_edit_engine.py --probe ./cuts.json --out ./…` | 4 |
| `reference-visual-fingerprint` | TOOL-23 | البصمة البصرية للفيديو المرجعي · Reference Visual Fingerprint | `python3 scripts/reference_visual_fingerprint.py ./in.mp4 --probe ./cu…` | 2 |
| `script-storyboard` | — | من السيناريو إلى الستوري بورد والأنيماتك · Script-to-Storyboard Animatic | `python3 scripts/script_storyboard.py parse ./script.pdf --first-page…` | 1 |
| `video-workflow-bridge` | TOOL-24 | جسر سير عمل الفيديو · Video Workflow Bridge | `python3 scripts/video_workflow_bridge.py paper-edit templates/ik-wave…` | 1 |

## image

| tool | ID | الأداة / tool | أمر أول / first command | tests |
|---|---|---|---|---|
| `app-studio` | TOOL-88 | استوديو التطبيقات للصور والتصميم · App Studio photo & design CLI | `python3 scripts/app_studio.py --help` | 2 |
| `app-studio-paint` | TOOL-89 | حزمة الرسم في استوديو التطبيقات · App Studio painting batch | `python3 -c "import sys; sys.path.insert(0,'scripts'); import app_stud…` | 1 |
| `design-tells` | — | كاشف علامات التصميم المولّد: فحص حتمي لصفحات HTML/CSS · Design tells: deterministic audit of HTML/CSS for the look every AI-generated page shares | `python3 scripts/design_tells.py audit index.html` | 1 |
| `font-fidelity-lab` | TOOL-42 | مختبر مطابقة الخطوط العربية · Arabic-aware font fidelity lab | `python3 scripts/font_fidelity_lab.py inspect proofs/_shared/fonts/Ami…` | 1 |
| `image-local-ai` | TOOL-140 | ذكاء الصور المحلي: إزالة الخلفية والملء الذكي بنموذج ONNX تختاره · Local image AI: remove background and smart fill with your own ONNX model | `python3 scripts/image_local_ai.py models --json` | 1 |
| `mosamem-rea-fusion` | TOOL-138 | تكامل مصمم وREA: فحص صور وتوليف مهارات آمن · Mosamem x REA source-safe image preflight and capability fusion | `python3 scripts/mosamem_rea_fusion.py doctor` | 1 |
| `prompt-forge` | TOOL-148 | مصنع البرومبتات: برومبتات طبقية وفحص البرومبت وقائمة لقطات بإطارات دقيقة · Prompt forge: layered generator prompts, prompt lint and frame-exact shot lists | `python3 scripts/prompt_forge.py forge /tmp/spec.json --targets still-…` | 1 |
| `prompt-pack` | TOOL-141 | حزمة المطالبات: كل مطالبة في كتلة كود قابلة للنسخ مع فحص يحذّر فقط · Prompt pack: copyable prompts, one code block each, with a warn-only lint | `python3 scripts/prompt_pack.py build prompts.json --out out/demo/prom…` | 1 |
| `render-text` | TOOL-90 | أداة عرض النص بخطوط مرشّحة · Font candidate text renderer | `node scripts/render_text.cjs ./spec.json ./out/` | 0 |
| `style-library` | TOOL-70 | مكتبة الأساليب: 586 أسلوبًا بصريًا بالاسم (86 من أطلس Futurepedia + 500 أصلي) — بحث ووصف وبرومنت وعينة وكتالوج PDF مصوّر · Style library — 586 visual styles by name (86 Futurepedia-derived + 500 original): find, describe, prompt, swatch, illustrated PDF catalog | `python3 scripts/style_library.py groups` | 1 |
| `telegram-typography-atlas` | TOOL-61 | مكتبة KOSIF الشاملة للخطوط وأفكار التصميم من صادرات تيليجرام · KOSIF Telegram Typography Atlas — private-safe font knowledge and idea search | `python3 scripts/telegram_typography_atlas.py find --index data/telegr…` | 1 |
| `unified-media` | TOOL-117 | محرر الوسائط الموحد: صور ورسم وتحريك وفيديو · Unified Media: photo adjustments + drawn overlays + GIF/MP4 | `python3 scripts/unified_media.py doctor` | 1 |

## investigate

| tool | ID | الأداة / tool | أمر أول / first command | tests |
|---|---|---|---|---|
| `atlas-bulk-source-audit` | TOOL-104 | تدقيق نصوص مصادر الأطلس · Atlas source-text audit | `python3 scripts/atlas_bulk_source_audit.py --help` | 0 |
| `atlas-deep-fusion` | TOOL-109 | منتقي مناهج الأطلس للقراءة فقط · Atlas read-only method selector | `python3 scripts/atlas_deep_fusion.py --help` | 0 |
| `atlas-review-summary` | TOOL-110 | ملخص مراجعة الأطلس · Atlas review summary | `python3 scripts/atlas_review_summary.py --help` | 0 |
| `atlas-reviewed-methods-v3` | TOOL-111 | مناهج الأطلس المراجَعة · Reviewed Atlas methods | `python3 scripts/atlas_reviewed_methods_v3.py --help` | 0 |
| `atlas-transfer` | TOOL-113 | نقل مناهج الأطلس المثبتة · Atlas verified method transfer | `python3 scripts/atlas_transfer.py --help` | 0 |
| `differential-exam` | TOOL-67 | مصحّح الامتحان الخفي التفاضلي · Differential hidden-exam scorer | `python3 scripts/differential_exam.py seal ./exam --out ./exam-seal.js…` | 1 |
| `installer-triage` | TOOL-97 | فرز المثبّتات · Installer Triage | `python3 scripts/installer_triage.py scan ./setup.exe` | 1 |
| `local-project-audit` | TOOL-32 | فحص المشروع المحلي دون تشغيل · Local project static audit | `python3 scripts/local_project_audit.py ./my-project` | 1 |
| `rea-bridge` | TOOL-98 | جسر أوامر REA · REA CLI Bridge | `python3 scripts/rea_bridge.py doctor` | 1 |
| `rea-family-router` | TOOL-52 | موجّه عائلات REA · REA Family Router | `python3 scripts/rea_family_router.py list` | 1 |
| `rea-owned-repo-batch` | TOOL-53 | تحليل REA لمستودعات المالك دفعةً واحدة · REA Owned-Repo Batch | `python3 scripts/rea_owned_repo_batch.py --private-output "$HOME/kosif…` | 0 |
| `repo-map` | TOOL-162 | خريطة المستودع · Repo Map | `python3 scripts/repo_map.py map scripts --budget 3000 --focus prompt` | 1 |
| `repository-capability-packer` | TOOL-54 | فحص المستودعات وحزمها · Repository Capability Packer | `python3 scripts/repository_capability_packer.py inspect ./repo --out…` | 1 |
| `web-app-study` | TOOL-62 | دراسة تطبيق ويب عام بـ REA (حقائق فقط) · Web app study (public frontend, REA, facts only) | `python3 scripts/web_app_study.py doctor` | 1 |

## local-computer

| tool | ID | الأداة / tool | أمر أول / first command | tests |
|---|---|---|---|---|
| `kosif-remote-commander` | TOOL-55 | خادم KOSIF Remote Commander · KOSIF Remote Commander MCP | `python3 scripts/kosif_remote_superpowers.py doctor` | 1 |

## maintain

| tool | ID | الأداة / tool | أمر أول / first command | tests |
|---|---|---|---|---|
| `agent-guard` | TOOL-154 | حارس الوكيل: فحص الأوامر قبل تشغيلها وكشف الأسرار وخطة فروع متوازية · Agent guard: shell preflight, transcript secret scan and worktree plans | `python3 scripts/agent_guard.py rules` | 1 |
| `build-chapters` | TOOL-99 | مولّد فصول العائلات · Family Chapter Generator | `python3 scripts/build_chapters.py` | 0 |
| `catalog-evidence-audit` | TOOL-33 | تدقيق أدلة الكتالوج · Catalog Evidence Audit | `python3 scripts/catalog_evidence_audit.py` | 1 |
| `check-skill` | TOOL-56 | فحص سلامة المهارة · Skill Health Check | `python3 scripts/check_skill.py` | 0 |
| `package-skill` | TOOL-57 | تحزيم المهارة للرفع إلى claude.ai · Skill Packager for claude.ai | `python3 scripts/package_skill.py` | 1 |
| `rea-superpowers-map` | TOOL-108 | خريطة سوبر باور بمنهج REA · Superpowers map, REA approach | `python3 scripts/rea_superpowers_map.py build` | 1 |
| `relabel-proofs` | TOOL-58 | إعادة تصنيف نطاق الأدلة · Proof Scope Relabeler | `python3 scripts/relabel_proofs.py` | 0 |
| `repo-build` | TOOL-101 | مولّد ملفات أطلس الأساليب · Style Atlas Builder | `python3 tools/build.py` | 0 |
| `repo-check-originality` | TOOL-102 | فاحص أصالة الملفات الإبداعية · Brief originality checker | `python3 tools/check_originality.py --briefs ./briefs/ --texts ./sourc…` | 0 |
| `repo-import-briefs` | TOOL-59 | استيراد الملفات الإبداعية · Creative brief importer | `python3 tools/import_briefs.py ./briefs/` | 0 |
| `repo-sync-catalog` | TOOL-60 | مزامنة الكتالوج مع PromptsMotion · PromptsMotion catalog sync | `python3 tools/sync_catalog.py` | 0 |
| `repo-validate` | TOOL-103 | فاحص سلامة أطلس الأنماط · Style atlas repository validator | `python3 tools/validate.py` | 3 |
| `self-council` | — | مجلس المراجعة الذاتية: خمس شخصيات من Claude تنقد كل مهارة وميزة، مع سجل تغطية · Self-Council: five Claude-derived critics review every skill and feature, with a coverage ledger | `python3 scripts/self_council.py inventory --summary` | 1 |
| `skill-layout` | TOOL-100 | خريطة ترتيب المهارة · Skill Layout Map | `python3 scripts/skill_layout.py build` | 1 |

## motion

| tool | ID | الأداة / tool | أمر أول / first command | tests |
|---|---|---|---|---|
| `aspects` | TOOL-77 | محلّل نِسَب أبعاد الفيديو · Flexible aspect ratio resolver | `python3 -c "import sys; sys.path.insert(0,'scripts'); import aspects;…` | 1 |
| `atlas-render` | TOOL-64 | رندر أفلام الشرح: ستوريبورد وفحص حتمية وMP4 حقيقي بصوت مُركّب · Atlas explainer renderer: storyboard, determinism check and real MP4 with synthesized score | `python3 scripts/atlas_render.py check` | 1 |
| `creative-reasoning-bridge` | TOOL-12 | جسر الصوت إلى لوحة القصة · Audio-to-Storyboard Bridge | `python3 scripts/creative_reasoning_bridge.py ./cues.json --style auto…` | 1 |
| `export-profile` | — | معيار التصدير: إعدادات التسليم المعتمدة لكل فيديو · Export profile: the owner-approved delivery settings for every video | `python3 scripts/export_profile.py` | 1 |
| `infinite-matrices` | TOOL-171 | محرك المصفوفات اللانهائية للأساليب السببية · KOSIF Infinite Matrices causal style engine | `python3 .claude/skills/kosif-infinite-matrices/scripts/kmx.py doctor` | 2 |
| `motion-director` | TOOL-13 | مُصرِّف حركة SVG المتزامنة مع الصوت · Audio-timed SVG motion compiler | `python3 scripts/motion_director.py doctor` | 2 |
| `motion-engine-js` | TOOL-14 | محرك حركة SVG · SVG motion engine runtime | `python3 scripts/motion_director.py compile ./scene.json --out ./out/f…` | 3 |
| `motion-kit-bridge` | TOOL-15 | جسر توقيتات Motion Starter Kit · Motion Starter Kit timing bridge | `python3 scripts/motion_kit_bridge.py styles` | 1 |
| `motion-physics` | TOOL-164 | فيزياء الحركة · Motion Physics | `python3 scripts/motion_physics.py spring --from 0 --to 1 --stiffness…` | 1 |
| `motion-runtime` | TOOL-16 | إنشاء فيلم سبورة مرسوم وتصييره · Doodle film runtime and renderer | `python3 scripts/motion_runtime.py doctor` | 1 |
| `motion-stack` | TOOL-17 | مولّد مشاريع بداية لمحركات الحركة · Third-party motion engine scaffolder | `python3 scripts/motion_stack.py list` | 1 |
| `motion-toolkit` | TOOL-18 | مكتبة رياضيات الحركة · Motion math toolkit | `node --input-type=module -e "import {ease, timeCode} from './resource…` | 1 |
| `particles` | TOOL-146 | جسيمات قابلة للقفز: انفجار بصيغة مغلقة وفحص الميزانية وإطار SVG · Seekable particles: closed-form bursts, budget check and SVG frame | `python3 scripts/particles.py burst --seed 7 --count 40 --t 0.5 --visi…` | 1 |
| `render-html` | TOOL-78 | محوّل HTML إلى فيديو MP4 · HTML to MP4 renderer | `node resources/motion-runtime/render_html.cjs --in ./film.html --out…` | 0 |
| `repo-aspects` | TOOL-80 | محلّل نسب العرض المرن · Flexible aspect ratio resolver | `python3 -c "import sys; sys.path.insert(0,'tools'); from aspects impo…` | 1 |
| `repo-job-wait` | TOOL-174 | تشغيل المهام الطويلة في الخلفية وانتظارها بلا sleep · Background job runner and waiter (no sleep waits) | `python3 tools/job.py start --dir out/20261024-film/render -- node too…` | 1 |
| `repo-render-html` | TOOL-81 | محوّل حتمي من HTML إلى فيديو MP4 · Deterministic HTML-to-MP4 renderer | `node tools/render_html.cjs --in starters/html-canvas/index.html --out…` | 0 |
| `repo-verify-video` | TOOL-82 | بوابة فحص تسليم الفيديو · Video delivery gate | `python3 tools/verify_video.py ./out/film.mp4 --aspect 9:16 --fps 30 -…` | 2 |
| `starter-html-canvas` | TOOL-83 | قالب فيلم HTML Canvas · HTML Canvas film starter | `python3 tools/kosif.py scaffold kinetic-arabic ./my-film --starter ht…` | 0 |
| `starter-remotion` | TOOL-84 | قالب فيلم Remotion · Remotion film starter | `python3 tools/kosif.py scaffold product ./my-film --starter remotion` | 0 |
| `style-atlas-bridge` | TOOL-63 | أطلس الأساليب الكامل (86 طريقة): بحث وتوليف وموجز إنتاج وهيكل مشروع شرح · Futurepedia AI Style Atlas — all 86 methods: search, fusion, storyboard-first briefs and engine scaffolds | `python3 scripts/style_atlas_bridge.py families` | 1 |
| `ui-beat` | TOOL-150 | إيقاع الواجهات: مسار مؤشر بتسهيل وعكس تخطيط للعربية وفحص الحلقة المتصلة · UI beat: eased cursor keyframes, RTL layout mirror and seamless-loop check | `python3 scripts/ui_beat.py cursor --from 900,1700 --to 540,960 --dur…` | 1 |
| `unified-cinematic` | TOOL-118 | السينما الموحدة: مونتاج الفيديو مع الصوت وحركة الكاميرا · Unified Cinematic: sound-clocked animation and video | `python3 scripts/unified_cinematic.py doctor` | 1 |
| `verify-video` | TOOL-79 | بوابة فحص تسليم الفيديو · Video delivery gate | `python3 scripts/verify_video.py ./in.mp4 --aspect 9:16 --fps 30 --dur…` | 2 |
| `video-eyes` | — | عيون الفيديو: شريط إطارات، طبقات شفافة للحركة، خط طاقة الحركة وكشف التجميد، وارتفاع الصوت لكل ثانية · Video eyes: contact strip, onion skin, motion-energy timeline with frozen-stretch detection, and per-second loudness | `python3 scripts/video_eyes.py report film.mp4 --out out/job/eyes` | 1 |

## sources

| tool | ID | الأداة / tool | أمر أول / first command | tests |
|---|---|---|---|---|
| `atlas-audit-synthesis` | TOOL-92 | تحويل مراجعة الأطلس إلى بيان مُراجَع · Atlas audit to reviewed manifest | `python3 scripts/atlas_audit_synthesis.py --records ./out/atlas-audit-…` | 1 |
| `atlas-body-audit` | TOOL-91 | مراجعة ساكنة لنصوص مهارات الأطلس · Atlas skill-body static audit | `python3 scripts/atlas_body_audit.py --index ./atlas-index.json --out…` | 1 |
| `atlas-external-bridge` | TOOL-43 | بحث مهارات أطلس الخارجية · Atlas external skill search | `python3 scripts/atlas_external_bridge.py stats --index ./atlas_index.…` | 1 |
| `atlas-metadata-audit` | TOOL-44 | تدقيق بيانات أطلس الوصفية · Atlas metadata audit | `python3 scripts/atlas_metadata_audit.py --index ./atlas_index.json --…` | 1 |
| `browser-scout` | TOOL-45 | مستكشف المواقع بالمتصفح · Browser scout site survey | `python3 scripts/browser_scout.py doctor` | 1 |
| `creative-external-search` | TOOL-46 | بحث المصادر الإبداعية دون اتصال · Creative sources offline search | `python3 scripts/creative_external_search.py search "kinetic typograph…` | 1 |
| `fetch-reference` | TOOL-93 | جلب المرجع المسموح وقياسه · Permitted reference fetch and measure | `python3 scripts/fetch_reference.py https://example.com/page --list --…` | 2 |
| `fetch-video` | TOOL-94 | تنزيل الفيديو من الروابط للمونتاج · Video link downloader for montage | `python3 scripts/fetch_video.py --doctor` | 0 |
| `github-pulse` | — | نبض GitHub: أهم 1000 مستودع نشط في آخر 30 يومًا حسب المجال، والأفكار المنقولة منها · GitHub 30-day pulse: the 1,000 most important repositories active in the last 30 days, by domain, with the ideas taken | `python3 scripts/github_pulse.py top --domain design-ui -n 15` | 1 |
| `github-top-repos` | TOOL-160 | متابعة أشهر 1000 مستودع · GitHub Top-1000 Tracker | `python3 scripts/github_top_repos.py build` | 1 |
| `instagram-finder` | TOOL-173 | البحث عن فيديوهات إنستجرام لمنتج وتحميلها · Instagram product video finder | `python3 scripts/instagram_finder.py accounts` | 1 |
| `instagram-reference-discovery` | TOOL-172 | البحث عن مراجع فيديو إنستجرام وربطها بالمصفوفات اللانهائية · Instagram Reference Discovery → Infinite Matrices | `python3 scripts/instagram_reference_bridge.py doctor` | 1 |
| `media-sources` | TOOL-47 | بوابة الوسائط المرخّصة · Licensed stock media gateway | `python3 scripts/media_sources.py list` | 1 |
| `rea-creative-research-atlas` | TOOL-48 | باني فهرس البحث الإبداعي · Creative research catalog builder | `python3 scripts/rea_creative_research_atlas.py report` | 1 |
| `rebalance-creative-repos` | TOOL-49 | إعادة موازنة فهرس المستودعات الإبداعية · Rebalance creative repo catalog | `python3 scripts/rebalance_creative_repos.py run` | 0 |
| `repo-ashell-cinema` | TOOL-51 | استوديو التنزيل Cinema C للآيفون · Cinema C iPhone downloader studio | `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh "https://www.youtube.c…` | 0 |
| `source-scout` | TOOL-50 | مستكشف مصادر المجتمع · Community source scout | `python3 scripts/source_scout.py check` | 1 |
| `sources-index` | TOOL-142 | فهرس المصادر: الذاكرة الفهرسية لمرفقات المستخدم داخل مجلد العمل · Sources index: per-work-dir index memory of the user's attachments | `python3 -I scripts/sources_index.py add charter.txt --dir ../../../ou…` | 1 |
| `stock-fetch` | TOOL-95 | تحميل لقطات مجانية بلا مفتاح (Pexels وMixkit) · Keyless stock footage fetcher (Pexels, Mixkit) | `python3 scripts/stock_fetch.py probe` | 1 |
| `stream-grabber` | TOOL-133 | ملتقط بث DASH وHLS للمونتاج · DASH/HLS stream grabber for editing | `python3 scripts/stream_grabber.py find ./saved-page.html` | 1 |
| `superpowers` | TOOL-96 | خريطة المستودعات الخارجية · External repository tool map | `python3 scripts/superpowers.py list --capability voice --json` | 1 |

## think

| tool | ID | الأداة / tool | أمر أول / first command | tests |
|---|---|---|---|---|
| `anchor-gate` | TOOL-74 | بوابة حفظ الحقائق عند إعادة الصياغة · Rewrite Fact Anchor Gate | `python3 scripts/anchor_gate.py --before proofs/general-writing/pairs/…` | 1 |
| `architecture-sizer` | TOOL-10 | مقدّر سعة الأنظمة · System Capacity Sizer | `python3 scripts/architecture_sizer.py --daily-requests 86400 --peak-f…` | 1 |
| `book-methods` | TOOL-66 | مناهج مستخلصة من الكتب: التفكير الجانبي والهندسة العملية والأدلة البايزية والشخصية وفحوص المحاسبة ووضوح البرومنت · Book-distilled methods: lateral ideas, pragmatic engineering, Bayesian evidence, personality, accounting checks, prompt clarity | `python3 scripts/book_methods.py search "شخصية حوار"` | 1 |
| `business-workflows` | TOOL-65 | الذكاء الاصطناعي في الأعمال: 9 وظائف و64 خطة عمل بخطط تشغيل لClaude · AI for business: 9 functions, 64 workflows, Claude-native gated runbooks | `python3 scripts/business_workflows.py functions` | 1 |
| `capability-mindmap` | TOOL-128 | الخريطة الذهنية المرحلية وتدقيق التكرار · Task-stage capability mind map and duplicate audit | `python3 scripts/capability_mindmap.py build` | 1 |
| `charter-ingest` | TOOL-139 | إدخال قائمة الميثاق: مجلس الخبراء 500 فهرسًا للاستشارة · Charter roster ingest: the 500-expert council as a consultable index | `python3 scripts/charter_ingest.py roster.txt --out data/experts_500.j…` | 1 |
| `council` | TOOL-68 | مجلس البرو: خمسة متعارضين أو مجلس مناسب من 100 شخصية، ثلاث جولات وحكم بالدرجات · Pro Council: five opposing members or a task-fitted council from 100 personas, three rounds, a scored verdict | `python3 scripts/council.py plan "اعمل ريلز دعاء" --dir out/demo/counc…` | 2 |
| `decision-math` | TOOL-145 | رياضيات القرار: نطاقات مونت كارلو ونقطة التعادل وترتيب ICE والقيمة الحالية ونقطة انقلاب القرار · Decision math: Monte Carlo ranges, break-even, ICE, NPV/IRR and flip thresholds | `echo '{"inputs":{"price":{"dist":"triangular","low":8,"mode":10,"high…` | 1 |
| `invention-lab` | TOOL-11 | مختبر الابتكار الهندسي · Invention Lab Candidates | `python3 scripts/invention_lab.py methods` | 1 |
| `lesson-integrity` | TOOL-167 | فاحص أرقام الدروس والشروح · Lesson number integrity checker | `python3 scripts/lesson_integrity.py values --registry values.json` | 1 |
| `llm-council` | — | مجلس الخمسة الإلزامي: بوابة تحدد العمق، خمسة مستشارين متعارضين، مراجعة مجهولة، وحكم رئيس واحد · Mandatory five-member council: a gate sets the depth, five opposed advisors, anonymous peer review, one chairman verdict | `python3 scripts/llm_council.py gate --level L2 --from-brief out/<work…` | 1 |
| `memory-ops` | TOOL-163 | عمليات الذاكرة · Memory Ops | `python3 scripts/memory_ops.py propose --store memory.json --facts fac…` | 1 |
| `prompt-lab` | TOOL-159 | مختبر البرومبت · Prompt Lab | `python3 scripts/prompt_lab.py kinds` | 1 |
| `see-pro-cognitive-gate` | TOOL-76 | فاحص عقود التفكير والتوليف KOSIF SEE Pro · SEE Pro Cognitive Fusion contract verifier | `python3 scripts/see_pro_cognitive_gate.py --self-test` | 1 |
| `stats-lab` | TOOL-151 | مختبر الإحصاء: اختبار A/B وحجم العينة ووصف عمود وأرباح الدفعات · Stats lab: A/B test, sample size, column statistics and FIFO/LIFO gains | `python3 scripts/stats_lab.py abtest --a 1000,100 --b 1000,130` | 1 |
| `task-history` | TOOL-170 | سجل المهام: سجل لكل مهمة منجزة لإعادتها لاحقًا · Task history: record every finished task and repeat it later | `python3 scripts/task_history.py new --kind video` | 1 |
| `tell-scan` | TOOL-75 | فاحص العبارات الكتابية النمطية · Writing Tell Scanner | `python3 scripts/tell_scan.py proofs/general-writing/samples/en_ai.txt` | 1 |
| `think` | TOOL-69 | محرك التفكير وقوالبه · Thinking engine scaffolds | `python3 scripts/think.py ladder "design a 30-day plan for a course la…` | 5 |
| `thinking-books` | — | مكتبة كتب التفكير: 64 منهجًا من 40 كتابًا مشهورًا في طرق التفكير مربوطة بمراحل البروتوكول · Thinking-books library: 64 methods from 40 famous books on how to think, routed to USIP phases | `python3 scripts/thinking_books.py stack "عايز أطلق تطبيق جديد"` | 1 |

