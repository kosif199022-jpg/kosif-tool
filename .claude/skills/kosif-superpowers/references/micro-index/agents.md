# الوكلاء والتوجيه الذكي — Agents & routing

[← الفهرس الدقيق / micro index](README.md) · 267 powers

## الفهرس / contents

- [runnable-tools (build)](#runnable-tools-build)
- [agent-orchestration (mind)](#agent-orchestration-mind)
- [self-discovery (mind)](#self-discovery-mind)


## runnable-tools (build)

chapter: [runnable-tools](../powers/runnable-tools.md) · card: `usip-library/cards/agents/runnable-tools.md` · tools: —

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| TOOL-01 | ✅ | باحث القدرات ثنائي اللغة بلا اتصال · Offline bilingual capability finder → `ai-tool-discovery` | SP-0133 Atlas metadata capability miner | python3 |
| TOOL-02 | ✅ | إحاطة بدء الجلسة · Session boot briefing → `boot` | SP-0133 Atlas metadata capability miner | python3 |
| TOOL-03 | ✅ | أطلس القدرات للبحث والتخطيط · Capability Atlas search and planner → `capability-atlas` | SP-0133 Atlas metadata capability miner | pip:pillow, pip:opencv |
| TOOL-04 | ✅ | موجّه القدرات التنفيذية · Capability runtime router → `capability-runtime-router` | SP-0133 Atlas metadata capability miner | python3 |
| TOOL-05 | ✅ | بوابة KOSIF الموحّدة · KOSIF hub (front door) → `hub` | SP-0133 Atlas metadata capability miner | python3 |
| TOOL-06 | ✅ | خادم MCP لكتالوج KOSIF · KOSIF catalog MCP server → `kosif-mcp` | SP-0133 Atlas metadata capability miner | python3 |
| TOOL-07 | ✅ | مدخل محلي بلا استنساخ · Local-first no-clone entry → `local-first` | SP-0133 Atlas metadata capability miner | python3 |
| TOOL-08 | ✅ | فاحص وجود حزم بايثون · Python package presence probe → `python-package-probe` | SP-0133 Atlas metadata capability miner | chromium, pip:numpy, pip:pillow, pip:opencv … |
| TOOL-105 | ✅ | منقّب قدرات الأطلس من البيانات الوصفية · Atlas metadata capability miner → `atlas-capability-miner` | SP-0133 Atlas metadata capability miner | python3, blender, npm:rea, engine:ghidra |
| TOOL-106 | ✅ | خريطة تغطية أطلس الـ5000 مهارة · Atlas-5000 coverage map → `atlas-5000` | SP-0133 Atlas metadata capability miner | python3 |
| TOOL-107 | ✅ | سجل الأطلس: حالة واحدة لكل مهارة · Atlas ledger: one status for every Atlas skill → `atlas-ledger` | SP-0133 Atlas metadata capability miner | python3, npm:rea |
| TOOL-116 | ✅ | فهرس ذكي للقدرات من أجل Claude · Smart capability index for Claude → `smart-capabilities` | SP-0133 Atlas metadata capability miner | python3, npm:rea, engine:ghidra |
| TOOL-125 | ✅ | FusionForge v2 لوصفات الـWorkflow المركبة داخل المشروع · FusionForge v2 project-scoped composite workflow recipes → `fusionforge` | SP-0133 Atlas metadata capability miner | python3 |
| TOOL-127 | ✅ | دمج القدرات في قدرات خارقة مترابطة · Superpower fusion (powers to connected superpowers) → `superpower-fusion` | SP-0133 Atlas metadata capability miner | python3 |
| TOOL-129 | ✅ | خريطة المجموعات مع القدرات الخارقة والسكربتات وخطط التثبيت · Group map with superpowers, scripts and install plans → `kosif-groups` | SP-0133 Atlas metadata capability miner | node, python3 |
| TOOL-161 | ✅ | الفهرس الدقيق: سطر لكل قدرة وأداة وقدرة خارقة · Micro index: one line per power, tool and superpower → `micro-index` | SP-0133 Atlas metadata capability miner | python3 |
| TOOL-34 | ✅ | باني خريطة القدرات المترابطة · Capability Graph Builder → `capability-graph` | SP-0133 Atlas metadata capability miner | node, python3, key:graphify |
| TOOL-43 | ✅ | بحث مهارات أطلس الخارجية · Atlas external skill search → `atlas-external-bridge` | SP-0133 Atlas metadata capability miner | python3, blender |
| TOOL-44 | ✅ | تدقيق بيانات أطلس الوصفية · Atlas metadata audit → `atlas-metadata-audit` | SP-0133 Atlas metadata capability miner | python3 |
| TOOL-54 | ✅ | فحص المستودعات وحزمها · Repository Capability Packer → `repository-capability-packer` | SP-0133 Atlas metadata capability miner | python3 |
| TOOL-63 | ✅ | أطلس الأساليب الكامل (86 طريقة): بحث وتوليف وموجز إنتاج وهيكل مشروع شرح · Futurepedia AI Style Atlas — all 86 methods: search, fusion, storyboard-first briefs and engine scaffolds → `style-atlas-bridge` | SP-0133 Atlas metadata capability miner | python3 |
| TOOL-72 | ✅ | مخطط متطلبات القدرات · Power requirements planner → `requirements` | SP-0133 Atlas metadata capability miner | node, python3, key:unspecified |
| TOOL-73 | ✅ | أداة سطر أوامر لأطلس أنماط KOSIF · KOSIF style atlas CLI → `repo-kosif` | SP-0133 Atlas metadata capability miner | python3, npm:remotion |
| TOOL-91 | ✅ | مراجعة ساكنة لنصوص مهارات الأطلس · Atlas skill-body static audit → `atlas-body-audit` | SP-0133 Atlas metadata capability miner | python3 |
| TOOL-101 | 🟢 | مولّد ملفات أطلس الأساليب · Style Atlas Builder → `repo-build` | SP-0133 Atlas metadata capability miner | python3 |
| TOOL-104 | 🟢 | تدقيق نصوص مصادر الأطلس · Atlas source-text audit → `atlas-bulk-source-audit` | SP-0133 Atlas metadata capability miner | python3, blender, engine:ghidra |
| TOOL-109 | 🟢 | منتقي مناهج الأطلس للقراءة فقط · Atlas read-only method selector → `atlas-deep-fusion` | SP-0133 Atlas metadata capability miner | python3, blender, engine:ghidra |
| TOOL-110 | 🟢 | ملخص مراجعة الأطلس · Atlas review summary → `atlas-review-summary` | SP-0133 Atlas metadata capability miner | python3, blender, engine:ghidra |
| TOOL-111 | 🟢 | مناهج الأطلس المراجَعة · Reviewed Atlas methods → `atlas-reviewed-methods-v3` | SP-0133 Atlas metadata capability miner | python3, blender, engine:ghidra |
| TOOL-112 | 🟢 | موجّه مناهج الأطلس حسب المهمة · Atlas task method router → `atlas-task-method-router` | SP-0133 Atlas metadata capability miner | python3, blender, engine:ghidra |
| TOOL-113 | 🟢 | نقل مناهج الأطلس المثبتة · Atlas verified method transfer → `atlas-transfer` | SP-0133 Atlas metadata capability miner | python3, blender, engine:ghidra |
| TOOL-71 | 🟢 | فحص قدرات الجهاز · Machine capability probe → `probe-env` | SP-0133 Atlas metadata capability miner | node, python3, docker, gpu |
| TOOL-92 | 🟢 | تحويل مراجعة الأطلس إلى بيان مُراجَع · Atlas audit to reviewed manifest → `atlas-audit-synthesis` | SP-0133 Atlas metadata capability miner | python3, npm:rea |
| TOOL-122 | ✅ | محرر KOSIF Timeline: مونتاج متعدد المسارات مع تراجع وإعادة · KOSIF Timeline: genuine multitrack video, image and audio editor → `kosif-timeline` | SP-0134 Reference Edit Engine | ffmpeg, pip:pillow |
| TOOL-123 | ✅ | تجربة مونتاج KOSIF Timeline تلقائية بملفات أصلية مولدة · KOSIF Timeline one-command synthetic media demo → `kosif-timeline-demo` | SP-0134 Reference Edit Engine | ffmpeg, pip:pillow |
| TOOL-130 | ✅ | فريق مونتاج برو (صوت أو فيديو إلى مونتاج أو موشن) · Montage Pro task force (audio/video to montage or motion) → `montage-pro` | SP-0134 Reference Edit Engine | ffmpeg, chromium, imagemagick, yt-dlp … |
| TOOL-131 | ✅ | مصنع الريلز: صوت وتوقيت كلمات ولقطات مرخصة ← ريلز 9:16 مفحوص · Reel factory: voice + word timings + licensed shots → verified 9:16 reel → `reel-factory` | SP-0134 Reference Edit Engine | ffmpeg, node, chromium, fonts:arabic |
| TOOL-132 | ✅ | دعاء يوم الأربعاء — محرك ريل دعاء موشن جرافيك 9:16 · Wednesday-morning dua reel (دعاء يوم الأربعاء) — 9:16 motion-graphics dua engine → `dua-wednesday` | SP-0134 Reference Edit Engine | ffmpeg, node, chromium, yt-dlp … |
| TOOL-166 | ✅ | خط اللوك: تلوين واحد لـ ffmpeg وSVG وGLSL · Look pipeline: one colour grade for ffmpeg, SVG/CSS and GLSL → `look-pipeline` | SP-0134 Reference Edit Engine | ffmpeg, python3 |
| TOOL-168 | ✅ | التعديل السريع: قص فوري يعرف الإطارات المفتاحية، مغيّر صوت، تفتيح الفيديو المظلم، استخراج الصوت · Fast Edit: keyframe-aware instant cut, voice presets, low-light lift, audio extract → `fast-edit` | SP-0134 Reference Edit Engine | ffmpeg, python3 |
| TOOL-19 | ✅ | تصيير لقطات B-roll بحركة كاميرا · Cinematic B-roll Renderer → `cinematic-broll-render` | SP-0134 Reference Edit Engine | ffmpeg, python3 |
| TOOL-20 | ✅ | مُخطِّط قطعات اللقطات الحقيقية · Footage-First Cut Planner → `cinematic-cut-planner` | SP-0134 Reference Edit Engine | python3 |
| TOOL-21 | ✅ | فاحص توقيت الفيديو المرجعي · Reference Video Timing Probe → `motion-reference-probe` | SP-0134 Reference Edit Engine | ffmpeg, python3 |
| TOOL-22 | ✅ | محرك إعادة بناء المونتاج المرجعي · Reference Edit Engine → `reference-edit-engine` | SP-0134 Reference Edit Engine | pip:higgsfield, npm:remotion, npm:react |
| TOOL-23 | ✅ | البصمة البصرية للفيديو المرجعي · Reference Visual Fingerprint → `reference-visual-fingerprint` | SP-0134 Reference Edit Engine | ffmpeg, python3 |
| TOOL-24 | ✅ | جسر سير عمل الفيديو · Video Workflow Bridge → `video-workflow-bridge` | SP-0134 Reference Edit Engine | python3 |
| TOOL-35 | ✅ | بوابة جودة خطة المونتاج · Reference-edit structural quality gate → `creative-quality-gate` | SP-0134 Reference Edit Engine | python3, npm:remotion |
| TOOL-47 | ✅ | بوابة الوسائط المرخّصة · Licensed stock media gateway → `media-sources` | SP-0134 Reference Edit Engine | ffmpeg, python3, yt-dlp |
| TOOL-85 | ✅ | محرك محاكاة الفيديو المرجعي · KOSIF Mimic reference rebuilder → `mimic` | SP-0134 Reference Edit Engine | ffmpeg, tesseract, pip:numpy, pip:pillow … |
| TOOL-95 | ✅ | تحميل لقطات مجانية بلا مفتاح (Pexels وMixkit) · Keyless stock footage fetcher (Pexels, Mixkit) → `stock-fetch` | SP-0134 Reference Edit Engine | ffmpeg, python3, key:unspecified |
| TOOL-13 | ✅ | مُصرِّف حركة SVG المتزامنة مع الصوت · Audio-timed SVG motion compiler → `motion-director` | SP-0135 Audio-timed SVG motion compiler | ffmpeg, node, python3, chromium |
| TOOL-14 | ✅ | محرك حركة SVG · SVG motion engine runtime → `motion-engine-js` | SP-0135 Audio-timed SVG motion compiler | ffmpeg, node, python3, chromium |
| TOOL-146 | ✅ | جسيمات قابلة للقفز: انفجار بصيغة مغلقة وفحص الميزانية وإطار SVG · Seekable particles: closed-form bursts, budget check and SVG frame → `particles` | SP-0135 Audio-timed SVG motion compiler | python3, npm:three |
| TOOL-150 | ✅ | إيقاع الواجهات: مسار مؤشر بتسهيل وعكس تخطيط للعربية وفحص الحلقة المتصلة · UI beat: eased cursor keyframes, RTL layout mirror and seamless-loop check → `ui-beat` | SP-0135 Audio-timed SVG motion compiler | python3 |
| TOOL-16 | ✅ | إنشاء فيلم سبورة مرسوم وتصييره · Doodle film runtime and renderer → `motion-runtime` | SP-0135 Audio-timed SVG motion compiler | ffmpeg, node, python3, chromium |
| TOOL-164 | ✅ | فيزياء الحركة · Motion Physics → `motion-physics` | SP-0135 Audio-timed SVG motion compiler | python3, npm:animejs, npm:react |
| TOOL-17 | ✅ | مولّد مشاريع بداية لمحركات الحركة · Third-party motion engine scaffolder → `motion-stack` | SP-0135 Audio-timed SVG motion compiler | python3, npm:three, npm:gsap, npm:remotion … |
| TOOL-18 | ✅ | مكتبة رياضيات الحركة · Motion math toolkit → `motion-toolkit` | SP-0135 Audio-timed SVG motion compiler | node, python3 |
| TOOL-64 | ✅ | رندر أفلام الشرح: ستوريبورد وفحص حتمية وMP4 حقيقي بصوت مُركّب · Atlas explainer renderer: storyboard, determinism check and real MP4 with synthesized score → `atlas-render` | SP-0135 Audio-timed SVG motion compiler | ffmpeg, python3, chromium |
| TOOL-77 | ✅ | محلّل نِسَب أبعاد الفيديو · Flexible aspect ratio resolver → `aspects` | SP-0135 Audio-timed SVG motion compiler | python3 |
| TOOL-79 | ✅ | بوابة فحص تسليم الفيديو · Video delivery gate → `verify-video` | SP-0135 Audio-timed SVG motion compiler | ffmpeg, python3 |
| TOOL-80 | ✅ | محلّل نسب العرض المرن · Flexible aspect ratio resolver → `repo-aspects` | SP-0135 Audio-timed SVG motion compiler | python3 |
| TOOL-82 | ✅ | بوابة فحص تسليم الفيديو · Video delivery gate → `repo-verify-video` | SP-0135 Audio-timed SVG motion compiler | ffmpeg, python3 |
| TOOL-78 | 📦 | محوّل HTML إلى فيديو MP4 · HTML to MP4 renderer → `render-html` | SP-0135 Audio-timed SVG motion compiler | ffmpeg, node, python3, chromium |
| TOOL-81 | 📦 | محوّل حتمي من HTML إلى فيديو MP4 · Deterministic HTML-to-MP4 renderer → `repo-render-html` | SP-0135 Audio-timed SVG motion compiler | ffmpeg, python3, chromium, npm:gsap |
| TOOL-83 | 📦 | قالب فيلم HTML Canvas · HTML Canvas film starter → `starter-html-canvas` | SP-0135 Audio-timed SVG motion compiler | ffmpeg, node, python3, chromium |
| TOOL-84 | 📦 | قالب فيلم Remotion · Remotion film starter → `starter-remotion` | SP-0135 Audio-timed SVG motion compiler | ffmpeg, python3, npm:remotion, npm:react |
| TOOL-115 | ✅ | الرسم الموحد: خطوط وأشكال وطبقات وتصدير · Unified Draw: freehand + geometry + layered export → `unified-draw` | SP-0136 Source-aware drawing school and user-au… | ffmpeg, pip:pillow |
| TOOL-117 | ✅ | محرر الوسائط الموحد: صور ورسم وتحريك وفيديو · Unified Media: photo adjustments + drawn overlays + GIF/MP4 → `unified-media` | SP-0136 Source-aware drawing school and user-au… | ffmpeg, imagemagick, pip:numpy, pip:pillow … |
| TOOL-136 | ✅ | أطلس مناهج كتب الرسم مع رسم بنائي بالطبقات · Drawing-book methods atlas with layered construction SVGs → `drawing-methods` | SP-0136 Source-aware drawing school and user-au… | python3, tesseract |
| TOOL-144 | ✅ | مدرب الرسم من فصول الكتب والتشخيص البصري المستقل · Book-chapter drawing coach and independent raster visual QA → `drawing-visual-qa` | SP-0136 Source-aware drawing school and user-au… | pip:pillow |
| TOOL-149 | ✅ | تخطيط المخططات: فحص الرسم البياني وتخطيط طبقي حتمي وSVG جاهز للعربية · Diagram layout: graph lint, deterministic layered layout and RTL-ready SVG → `diagram-layout` | SP-0136 Source-aware drawing school and user-au… | python3 |
| TOOL-153 | ✅ | رموز الهوية: ألوان الشعار ورموز بثلاث طبقات ومصفوفة تباين WCAG · Brand tokens: SVG palette, 3-tier design tokens and WCAG contrast matrix → `brand-tokens` | SP-0136 Source-aware drawing school and user-au… | python3, npm:axe |
| TOOL-157 | ✅ | نسخة مرسومة أو ملوّنة باليد لأي صورة أو مشهد متخيَّل: رصاص، فحم، حبر، ألوان خشبية، فرشاة زيت أو ألوان مائية · Hand-drawn or hand-painted version of any photo or imagined scene: pencil, charcoal, ink, coloured pencil, oil brush or watercolour → `portrait-pipeline` | SP-0136 Source-aware drawing school and user-au… | chromium, blender, pip:numpy, pip:opencv … |
| TOOL-169 | ✅ | محرك الخامات الملوّنة: ألوان خشبية وفرشاة زيت وألوان مائية لأي صورة · Colour media engine: coloured pencil, oil brush and watercolour painting of a photo → `color-media` | SP-0136 Source-aware drawing school and user-au… | chromium, pip:numpy, pip:opencv, pip:mediapipe |
| TOOL-27 | ✅ | تحريك الشخصية بكامل الجسم · Full-body character animator → `character-fullbody` | SP-0136 Source-aware drawing school and user-au… | ffmpeg, pip:pillow, pip:rdkit |
| TOOL-29 | ✅ | رسم الشخصيات والمشاهد بالكود · Code Drawing Master storyboards → `code-drawing-master` | SP-0136 Source-aware drawing school and user-au… | pip:faster-whisper |
| TOOL-30 | ✅ | الرسم الإبداعي بالطبقات · Creative Paint layered renderer → `creative-paint` | SP-0136 Source-aware drawing school and user-au… | ffmpeg, pip:pillow |
| TOOL-31 | ✅ | الرسم الذكي ومساعد الأشكال · Smart Draw shape assist → `smart-draw` | SP-0136 Source-aware drawing school and user-au… | pip:pillow |
| TOOL-89 | ✅ | حزمة الرسم في استوديو التطبيقات · App Studio painting batch → `app-studio-paint` | SP-0136 Source-aware drawing school and user-au… | chromium, pip:numpy, pip:pillow, pip:opencv |
| TOOL-134 | 🟢 | دراسة الرسم التدريجي والظل الأصلي · Staged drawing and original three-value visual studies → `creative-principles` | SP-0136 Source-aware drawing school and user-au… | python3 |
| TOOL-135 | 🟢 | أكاديمية الرسم والدروس المبنية على مصادر · Source-aware drawing school and user-authorized book audits → `drawing-academy` | SP-0136 Source-aware drawing school and user-au… | python3 |
| TOOL-137 | 🟢 | منظور هندسي ومقاييس التباين اللوني · Original two-point perspective and numeric palette analysis → `perspective-color-lab` | SP-0136 Source-aware drawing school and user-au… | python3, npm:axe |
| TOOL-100 | ✅ | خريطة ترتيب المهارة · Skill Layout Map → `skill-layout` | SP-0137 Skill Layout Map | python3 |
| TOOL-108 | ✅ | خريطة سوبر باور بمنهج REA · Superpowers map, REA approach → `rea-superpowers-map` | SP-0137 Skill Layout Map | python3, npm:rea |
| TOOL-128 | ✅ | الخريطة الذهنية المرحلية وتدقيق التكرار · Task-stage capability mind map and duplicate audit → `capability-mindmap` | SP-0137 Skill Layout Map | python3, npm:mermaid |
| TOOL-143 | ✅ | خريطة مستودعات المالك وخريطة المهارات · Owned-repositories map and skill map → `owned-repos` | SP-0137 Skill Layout Map | python3 |
| TOOL-147 | ✅ | لوح الخرائط: إسقاط الإحداثيات إلى بكسلات وتصنيف الخرائط الملونة وسجل المصادر · Map plate: projection to pixels, choropleth classes and source ledger → `geo-plate` | SP-0137 Skill Layout Map | python3, fonts:arabic |
| TOOL-162 | ✅ | خريطة المستودع · Repo Map → `repo-map` | SP-0137 Skill Layout Map | python3 |
| TOOL-55 | ✅ | خادم KOSIF Remote Commander · KOSIF Remote Commander MCP → `kosif-remote-commander` | SP-0137 Skill Layout Map | node, python3 |
| TOOL-57 | ✅ | تحزيم المهارة للرفع إلى claude.ai · Skill Packager for claude.ai → `package-skill` | SP-0137 Skill Layout Map | python3 |
| TOOL-96 | ✅ | خريطة المستودعات الخارجية · External repository tool map → `superpowers` | SP-0137 Skill Layout Map | ffmpeg, chromium, pip:faster-whisper |
| TOOL-102 | 🟢 | فاحص أصالة الملفات الإبداعية · Brief originality checker → `repo-check-originality` | SP-0137 Skill Layout Map | python3 |
| TOOL-126 | 🟢 | ذاكرة FusionForge المشتركة بوصفات مهارات معزولة · FusionForge Shared Memory: reviewed cross-project skill structures → `fusionforge-shared` | SP-0137 Skill Layout Map | python3 |
| TOOL-56 | 🟢 | فحص سلامة المهارة · Skill Health Check → `check-skill` | SP-0137 Skill Layout Map | python3 |
| TOOL-103 | ✅ | فاحص سلامة أطلس الأنماط · Style atlas repository validator → `repo-validate` | SP-0138 Catalog Evidence Audit | python3 |
| TOOL-124 | ✅ | محرك بروتوكول ذكاء المهارات الشامل · Universal Skill Intelligence Protocol engine → `skill-intelligence` | SP-0138 Catalog Evidence Audit | python3 |
| TOOL-156 | ✅ | البحث في كتالوج القدرات · Power catalog search → `powers` | SP-0138 Catalog Evidence Audit | python3, npm:mermaid |
| TOOL-70 | ✅ | مكتبة الأساليب: 586 أسلوبًا بصريًا بالاسم (86 من أطلس Futurepedia + 500 أصلي) — بحث ووصف وبرومنت وعينة وكتالوج PDF مصوّر · Style library — 586 visual styles by name (86 Futurepedia-derived + 500 original): find, describe, prompt, swatch, illustrated PDF catalog → `style-library` | SP-0138 Catalog Evidence Audit | python3, chromium |
| TOOL-33 | 🟢 | تدقيق أدلة الكتالوج · Catalog Evidence Audit → `catalog-evidence-audit` | SP-0138 Catalog Evidence Audit | python3 |
| TOOL-58 | 🟢 | إعادة تصنيف نطاق الأدلة · Proof Scope Relabeler → `relabel-proofs` | SP-0138 Catalog Evidence Audit | python3 |
| TOOL-59 | 🟢 | استيراد الملفات الإبداعية · Creative brief importer → `repo-import-briefs` | SP-0138 Catalog Evidence Audit | python3 |
| TOOL-60 | 🟢 | مزامنة الكتالوج مع PromptsMotion · PromptsMotion catalog sync → `repo-sync-catalog` | SP-0138 Catalog Evidence Audit | python3 |
| TOOL-99 | 🟢 | مولّد فصول العائلات · Family Chapter Generator → `build-chapters` | SP-0138 Catalog Evidence Audit | python3 |
| TOOL-48 | 📦 | باني فهرس البحث الإبداعي · Creative research catalog builder → `rea-creative-research-atlas` | SP-0138 Catalog Evidence Audit | python3, gh, npm:rea |
| TOOL-49 | 📦 | إعادة موازنة فهرس المستودعات الإبداعية · Rebalance creative repo catalog → `rebalance-creative-repos` | SP-0138 Catalog Evidence Audit | python3, gh, npm:rea |
| TOOL-119 | ✅ | دمج رندر Blender Cycles مع مونتاج KOSIF والصوت · Blender Cycles + KOSIF Cinematic compositor → `blender-cinematic-bridge` | SP-0139 Safe headless Blender bridge | ffmpeg, blender, pip:pillow, npm:rea … |
| TOOL-120 | ✅ | إنشاء مشهد إنقاذ قطة ثلاثي الأبعاد داخل Blender · Create an editable Blender 3D cat rescue demo → `blender-rescue-scene` | SP-0139 Safe headless Blender bridge | python3, blender |
| TOOL-121 | ✅ | تطوير فرو القطة والملامح في Blender Cycles · Blender Cat Fur Upgrade: renderable hair geometry and character detail → `blender-cat-fur-upgrade` | SP-0139 Safe headless Blender bridge | python3, blender |
| TOOL-36 | ✅ | تدقيق واجهة بايثون في Blender · Blender Python API audit → `blender-api-audit` | SP-0139 Safe headless Blender bridge | python3, blender |
| TOOL-37 | ✅ | جسر Blender الآمن · Safe headless Blender bridge → `blender-bridge` | SP-0139 Safe headless Blender bridge | python3, chromium, blender |
| TOOL-38 | ✅ | رندر Cycles إلى فيديو مُتحقَّق منه · Cycles scene to verified video → `blender-cycles-render` | SP-0139 Safe headless Blender bridge | ffmpeg, python3, blender |
| TOOL-40 | ✅ | رندر ثلاثي الأبعاد مستقل عن Blender · Native 3D renderer (no Blender) → `native-3d` | SP-0139 Safe headless Blender bridge | ffmpeg, blender, pip:pillow |
| TOOL-41 | ✅ | مُصدِّر GLB مستقل عن Blender · Native GLB exporter (no Blender) → `native-glb` | SP-0139 Safe headless Blender bridge | python3, blender, npm:three |
| TOOL-114 | 🟢 | مساعد فيديو الحركة في Blender · Blender motion video helper → `blender-motion-video` | SP-0139 Safe headless Blender bridge | python3, blender, engine:ghidra |
| TOOL-39 | 📦 | منفّذ المشهد داخل Blender · Blender-side scene builder → `blender-worker` | SP-0139 Safe headless Blender bridge | python3, blender |
| TOOL-87 | 📦 | رندر سينمائي بـBlender Cycles · Blender Cycles cinematic renders → `blender-cinema` | SP-0139 Safe headless Blender bridge | ffmpeg, blender |
| TOOL-10 | ✅ | مقدّر سعة الأنظمة · System Capacity Sizer → `architecture-sizer` | SP-0140 Prompt Lab | python3 |
| TOOL-145 | ✅ | رياضيات القرار: نطاقات مونت كارلو ونقطة التعادل وترتيب ICE والقيمة الحالية ونقطة انقلاب القرار · Decision math: Monte Carlo ranges, break-even, ICE, NPV/IRR and flip thresholds → `decision-math` | SP-0140 Prompt Lab | python3, npm:p5 |
| TOOL-148 | ✅ | مصنع البرومبتات: برومبتات طبقية وفحص البرومبت وقائمة لقطات بإطارات دقيقة · Prompt forge: layered generator prompts, prompt lint and frame-exact shot lists → `prompt-forge` | SP-0140 Prompt Lab | python3 |
| TOOL-159 | ✅ | مختبر البرومبت · Prompt Lab → `prompt-lab` | SP-0140 Prompt Lab | python3 |
| TOOL-163 | ✅ | عمليات الذاكرة · Memory Ops → `memory-ops` | SP-0140 Prompt Lab | python3 |
| TOOL-167 | ✅ | فاحص أرقام الدروس والشروح · Lesson number integrity checker → `lesson-integrity` | SP-0140 Prompt Lab | python3 |
| TOOL-170 | ✅ | سجل المهام: سجل لكل مهمة منجزة لإعادتها لاحقًا · Task history: record every finished task and repeat it later → `task-history` | SP-0140 Prompt Lab | python3 |
| TOOL-65 | ✅ | الذكاء الاصطناعي في الأعمال: 9 وظائف و64 خطة عمل بخطط تشغيل لClaude · AI for business: 9 functions, 64 workflows, Claude-native gated runbooks → `business-workflows` | SP-0140 Prompt Lab | python3, key:unspecified |
| TOOL-69 | ✅ | محرك التفكير وقوالبه · Thinking engine scaffolds → `think` | SP-0140 Prompt Lab | python3 |
| TOOL-74 | ✅ | بوابة حفظ الحقائق عند إعادة الصياغة · Rewrite Fact Anchor Gate → `anchor-gate` | SP-0140 Prompt Lab | python3 |
| TOOL-118 | ✅ | السينما الموحدة: مونتاج الفيديو مع الصوت وحركة الكاميرا · Unified Cinematic: sound-clocked animation and video → `unified-cinematic` | SP-0141 Subtitle to words.json converter | ffmpeg, imagemagick, pip:numpy, pip:pillow … |
| TOOL-12 | ✅ | جسر الصوت إلى لوحة القصة · Audio-to-Storyboard Bridge → `creative-reasoning-bridge` | SP-0141 Subtitle to words.json converter | python3 |
| TOOL-15 | ✅ | جسر توقيتات Motion Starter Kit · Motion Starter Kit timing bridge → `motion-kit-bridge` | SP-0141 Subtitle to words.json converter | python3 |
| TOOL-152 | ✅ | تجهيز نص التعليق الصوتي: تقطيع آمن وتقدير المدة وSSML · TTS script prep: prosody-safe chunks, duration estimate and SSML → `tts-script` | SP-0141 Subtitle to words.json converter | python3 |
| TOOL-165 | ✅ | سطور الترجمة: من توقيت الكلمات إلى ترجمة مقروءة · Caption lines: word timings to readable SRT/VTT → `caption-lines` | SP-0141 Subtitle to words.json converter | pip:faster-whisper, key:openai |
| TOOL-25 | ✅ | مستخرج إشارات التوقيت من الصوت · WAV audio cue mapper → `audio-cue-mapper` | SP-0141 Subtitle to words.json converter | pip:faster-whisper |
| TOOL-26 | ✅ | فرضيات إيقاع الموسيقى · Music rhythm hypotheses → `music-rhythm-engine` | SP-0141 Subtitle to words.json converter | python3 |
| TOOL-28 | ✅ | تحريك ذراع الشخصية بالحركية العكسية · Character IK arm animator → `character-ik` | SP-0141 Subtitle to words.json converter | ffmpeg, pip:pillow |
| TOOL-86 | ✅ | محوّل الترجمات إلى توقيت الكلمات · Subtitle to words.json converter → `repo-words-convert` | SP-0141 Subtitle to words.json converter | pip:faster-whisper |
| TOOL-138 | ✅ | تكامل مصمم وREA: فحص صور وتوليف مهارات آمن · Mosamem x REA source-safe image preflight and capability fusion → `mosamem-rea-fusion` | SP-0142 REA CLI Bridge | python3, chromium, npm:rea |
| TOOL-154 | ✅ | حارس الوكيل: فحص الأوامر قبل تشغيلها وكشف الأسرار وخطة فروع متوازية · Agent guard: shell preflight, transcript secret scan and worktree plans → `agent-guard` | SP-0142 REA CLI Bridge | python3, git |
| TOOL-160 | ✅ | متابعة أشهر 1000 مستودع · GitHub Top-1000 Tracker → `github-top-repos` | SP-0142 REA CLI Bridge | python3 |
| TOOL-32 | ✅ | فحص المشروع المحلي دون تشغيل · Local project static audit → `local-project-audit` | SP-0142 REA CLI Bridge | python3, npm:rea, engine:ghidra |
| TOOL-45 | ✅ | مستكشف المواقع بالمتصفح · Browser scout site survey → `browser-scout` | SP-0142 REA CLI Bridge | python3, chromium |
| TOOL-52 | ✅ | موجّه عائلات REA · REA Family Router → `rea-family-router` | SP-0142 REA CLI Bridge | python3, npm:rea, engine:android, engine:binwalk … |
| TOOL-62 | ✅ | دراسة تطبيق ويب عام بـ REA (حقائق فقط) · Web app study (public frontend, REA, facts only) → `web-app-study` | SP-0142 REA CLI Bridge | python3, chromium, npm:rea |
| TOOL-98 | ✅ | جسر أوامر REA · REA CLI Bridge → `rea-bridge` | SP-0142 REA CLI Bridge | python3, npm:rea |
| TOOL-53 | 📦 | تحليل REA لمستودعات المالك دفعةً واحدة · REA Owned-Repo Batch → `rea-owned-repo-batch` | SP-0142 REA CLI Bridge | python3, git, npm:rea |
| TOOL-11 | ✅ | مختبر الابتكار الهندسي · Invention Lab Candidates → `invention-lab` | SP-0143 Arabic-aware font fidelity lab | pip:hypothesis |
| TOOL-140 | ✅ | ذكاء الصور المحلي: إزالة الخلفية والملء الذكي بنموذج ONNX تختاره · Local image AI: remove background and smart fill with your own ONNX model → `image-local-ai` | SP-0143 Arabic-aware font fidelity lab | — |
| TOOL-141 | ✅ | حزمة المطالبات: كل مطالبة في كتلة كود قابلة للنسخ مع فحص يحذّر فقط · Prompt pack: copyable prompts, one code block each, with a warn-only lint → `prompt-pack` | SP-0143 Arabic-aware font fidelity lab | python3, key:video-gen |
| TOOL-151 | ✅ | مختبر الإحصاء: اختبار A/B وحجم العينة ووصف عمود وأرباح الدفعات · Stats lab: A/B test, sample size, column statistics and FIFO/LIFO gains → `stats-lab` | SP-0143 Arabic-aware font fidelity lab | python3 |
| TOOL-42 | ✅ | مختبر مطابقة الخطوط العربية · Arabic-aware font fidelity lab → `font-fidelity-lab` | SP-0143 Arabic-aware font fidelity lab | pip:pillow, fonts:arabic |
| TOOL-61 | ✅ | مكتبة KOSIF الشاملة للخطوط وأفكار التصميم من صادرات تيليجرام · KOSIF Telegram Typography Atlas — private-safe font knowledge and idea search → `telegram-typography-atlas` | SP-0143 Arabic-aware font fidelity lab | fonts:arabic |
| TOOL-88 | ✅ | استوديو التطبيقات للصور والتصميم · App Studio photo & design CLI → `app-studio` | SP-0143 Arabic-aware font fidelity lab | ffmpeg, chromium, pip:numpy, pip:pillow … |
| TOOL-90 | 📦 | أداة عرض النص بخطوط مرشّحة · Font candidate text renderer → `render-text` | SP-0143 Arabic-aware font fidelity lab | node, python3, chromium, fonts:arabic |
| TOOL-133 | ✅ | ملتقط بث DASH وHLS للمونتاج · DASH/HLS stream grabber for editing → `stream-grabber` | SP-0144 Video link downloader for montage | ffmpeg, python3 |
| TOOL-142 | ✅ | فهرس المصادر: الذاكرة الفهرسية لمرفقات المستخدم داخل مجلد العمل · Sources index: per-work-dir index memory of the user's attachments → `sources-index` | SP-0144 Video link downloader for montage | pip:office |
| TOOL-46 | ✅ | بحث المصادر الإبداعية دون اتصال · Creative sources offline search → `creative-external-search` | SP-0144 Video link downloader for montage | python3, npm:rea |
| TOOL-50 | ✅ | مستكشف مصادر المجتمع · Community source scout → `source-scout` | SP-0144 Video link downloader for montage | python3 |
| TOOL-93 | ✅ | جلب المرجع المسموح وقياسه · Permitted reference fetch and measure → `fetch-reference` | SP-0144 Video link downloader for montage | ffmpeg, python3 |
| TOOL-51 | 📦 | استوديو التنزيل Cinema C للآيفون · Cinema C iPhone downloader studio → `repo-ashell-cinema` | SP-0144 Video link downloader for montage | ffmpeg, python3, yt-dlp |
| TOOL-94 | 📦 | تنزيل الفيديو من الروابط للمونتاج · Video link downloader for montage → `fetch-video` | SP-0144 Video link downloader for montage | ffmpeg, python3, imagemagick, yt-dlp |
| TOOL-139 | ✅ | إدخال قائمة الميثاق: مجلس الخبراء 500 فهرسًا للاستشارة · Charter roster ingest: the 500-expert council as a consultable index → `charter-ingest` | SP-0145 Pro Council: five opposing members or a… | python3 |
| TOOL-158 | ✅ | مجلس خبراء الرسم: أحد عشر خبيرًا من بطاقات الكتب الـ48 يراجعون الصورة قبل إرسالها · Drawing council: eleven experts from the 48 method cards review an image before it is sent → `drawing-council` | SP-0145 Pro Council: five opposing members or a… | pip:pillow |
| TOOL-66 | ✅ | مناهج مستخلصة من الكتب: التفكير الجانبي والهندسة العملية والأدلة البايزية والشخصية وفحوص المحاسبة ووضوح البرومنت · Book-distilled methods: lateral ideas, pragmatic engineering, Bayesian evidence, personality, accounting checks, prompt clarity → `book-methods` | SP-0145 Pro Council: five opposing members or a… | python3 |
| TOOL-68 | ✅ | مجلس البرو: خمسة متعارضين أو مجلس مناسب من 100 شخصية، ثلاث جولات وحكم بالدرجات · Pro Council: five opposing members or a task-fitted council from 100 personas, three rounds, a scored verdict → `council` | SP-0145 Pro Council: five opposing members or a… | python3 |
| TOOL-75 | ✅ | فاحص العبارات الكتابية النمطية · Writing Tell Scanner → `tell-scan` | SP-0145 Pro Council: five opposing members or a… | python3 |
| TOOL-76 | ✅ | فاحص عقود التفكير والتوليف KOSIF SEE Pro · SEE Pro Cognitive Fusion contract verifier → `see-pro-cognitive-gate` | SP-0145 Pro Council: five opposing members or a… | python3, network |
| TOOL-09 | ✅ | موجّه مهارات العمل ومثبّتها · Process-skill router and installer → `superpowers-unified` | SP-0146 Installer Triage | python3, imagemagick |
| TOOL-67 | ✅ | مصحّح الامتحان الخفي التفاضلي · Differential hidden-exam scorer → `differential-exam` | SP-0146 Installer Triage | python3 |
| TOOL-97 | ✅ | فرز المثبّتات · Installer Triage → `installer-triage` | SP-0146 Installer Triage | python3, npm:rea, 7zip, innoextract |

## agent-orchestration (mind)

chapter: [agent-orchestration](../powers/agent-orchestration.md) · card: `usip-library/cards/agents/agent-orchestration.md` · tools: `agent-guard` · `business-workflows` · `charter-ingest` · `council` · `fusionforge` · `hub` · `kosif-mcp` · `kosif-remote-commander` …

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| AGENT-37 | ✅ | Chroma: فهرسة المستندات في مخزن متجهات والإجابة عن · Chroma: Index documents into a vector store and answer semantic queries (RAG) | SP-0001 Session checkpoint and handoff via a .c… | pip:chromadb |
| AGENT-50 | 🟢 | قرار الذاكرة: إضافة أو تحديث أو حذف أو لا شيء · Memory decision step: add, update, delete or no-op | SP-0001 Session checkpoint and handoff via a .c… | python3 |
| AGENT-36 | 📦 | llama.cpp: تشغيل نموذج مفتوح صغير دون اتصال للتصنيف · llama.cpp: Run a small quantised open model offline for batch classification or embeddings | SP-0001 Session checkpoint and handoff via a .c… | pip:llama-cpp |
| AGENT-20 | 📄 | الخطافات حواجز آلية · Hooks as automatic guardrails | SP-0001 Session checkpoint and handoff via a .c… | — |
| AGENT-21 | 📄 | بوابة التسليم وسجل التغطية · Delivery gate & coverage ledger | SP-0001 Session checkpoint and handoff via a .c… | — |
| AGENT-22 | 📄 | خوادم MCP: إضافة وتدقيق وميزانية · MCP servers: add, vet, budget | SP-0001 Session checkpoint and handoff via a .c… | claude:tools, key:unspecified |
| AGENT-23 | 📄 | سُلَّم اختيار السطح · Capability surface ladder | SP-0001 Session checkpoint and handoff via a .c… | ffmpeg, python3, key:unspecified |
| AGENT-24 | 📄 | الإضافات والأسواق · Plugins & marketplaces | SP-0001 Session checkpoint and handoff via a .c… | — |
| AGENT-29 | 📄 | اقتصاد السياق · Context economy | SP-0001 Session checkpoint and handoff via a .c… | claude:tools |
| AGENT-30 | 📄 | توجيه الجهد ومستوى النموذج · Effort and tier routing | SP-0001 Session checkpoint and handoff via a .c… | claude:tools |
| AGENT-31 | 📄 | ملف تسليم الجلسة · Session handoff file | SP-0001 Session checkpoint and handoff via a .c… | — |
| AGENT-33 | 📄 | خريطة أسطح الذاكرة · Memory surfaces map | SP-0001 Session checkpoint and handoff via a .c… | key:graphify |
| AGENT-39 | 📄 | طبقات التعليمات ونطاق AGENTS.md · Instruction layering and AGENTS.md scope | SP-0001 Session checkpoint and handoff via a .c… | — |
| AGENT-40 | 📄 | ضغط السياق بملخص تسليم · Context compaction as a handoff | SP-0001 Session checkpoint and handoff via a .c… | — |
| AGENT-41 | 📄 | وضع التخطيط غير المعدِّل · Non-mutating plan mode | SP-0001 Session checkpoint and handoff via a .c… | — |
| AGENT-42 | 📄 | انضباط قائمة الخطوات · Plan checklist discipline | SP-0001 Session checkpoint and handoff via a .c… | — |
| AGENT-43 | 📄 | الهدف المستمر وتدقيق الإكمال · Persistent goal and completion audit | SP-0001 Session checkpoint and handoff via a .c… | — |
| AGENT-44 | 📄 | المتابعة الاستباقية المحدودة · Bounded proactive follow-up | SP-0001 Session checkpoint and handoff via a .c… | — |
| AGENT-46 | 📄 | ذاكرة على مرحلتين بعقود إيجار · Two-phase memory with leased jobs | SP-0001 Session checkpoint and handoff via a .c… | — |
| AGENT-47 | 📄 | رسم حالة بنقاط حفظ واستئناف · Checkpointed state graph with resume and approval interrupts | SP-0001 Session checkpoint and handoff via a .c… | — |
| AGENT-49 | 📄 | خط إنتاج بإجراءات قياسية ووثائق تسليم · SOP assembly line with document handoffs | SP-0001 Session checkpoint and handoff via a .c… | — |
| AGENT-51 | 📄 | ذاكرة بطبقات يحررها الوكيل · Tiered self-editing memory | SP-0001 Session checkpoint and handoff via a .c… | — |
| AGENT-52 | 📄 | التقاط ملاحظات الجلسة وحقنها في التالية · Session observation capture and injection | SP-0001 Session checkpoint and handoff via a .c… | — |
| AGENT-54 | 📄 | حواجز تفعيل وتسليم لمتخصص · Tripwire guardrails and specialist handoffs | SP-0001 Session checkpoint and handoff via a .c… | — |
| AGENT-01 | 📄 | متى تفوّض ومتى تعمل بنفسك · Delegate or do it yourself | SP-0002 Delegate-or-inline decision for subagen… | claude:tools |
| AGENT-02 | 📄 | حزمة التنفيذ: موجز تفويض كامل · Execution packet (delegation brief) | SP-0002 Delegate-or-inline decision for subagen… | claude:tools |
| AGENT-04 | 📄 | وكلاء مخصصون في Claude Code · Custom subagents (.claude/agents) | SP-0002 Delegate-or-inline decision for subagen… | git, claude:tools |
| AGENT-05 | 📄 | إيصال مكتوب لكل نتيجة · Typed receipts (exposure ≠ authorization ≠ execution ≠ verification) | SP-0002 Delegate-or-inline decision for subagen… | ffmpeg |
| AGENT-45 | 📄 | غلاف نتيجة الأداة وتيار الأحداث · Tool result envelope and typed event stream | SP-0002 Delegate-or-inline decision for subagen… | chromium |
| AGENT-53 | 📄 | وكيل يتصرف بالكود · Code-as-action agent | SP-0002 Delegate-or-inline decision for subagen… | python3 |
| AGENT-55 | 📄 | تيار أحداث قابل لإعادة التشغيل · Replayable event-stream agent | SP-0002 Delegate-or-inline decision for subagen… | — |
| AGENT-11 | 📄 | مراجعة سانتا المزدوجة · Santa dual review | SP-0003 Author a skill | claude:tools |
| AGENT-12 | 📄 | مجلس الأصوات الأربعة · Four-voice council for ambiguous decisions | SP-0003 Author a skill | claude:tools |
| AGENT-13 | 📄 | حلقة المولّد والمقيّم · Generator–evaluator loop | SP-0003 Author a skill | chromium |
| AGENT-14 | 📄 | محقق خصم يفترض الرفض · Adversarial verifier (fail closed) | SP-0003 Author a skill | claude:tools |
| AGENT-15 | 📄 | لوحة أدوار متعددة · Role-split review panel | SP-0003 Author a skill | — |
| AGENT-25 | 📄 | تأليف مهارة · Author a skill | SP-0003 Author a skill | — |
| AGENT-26 | 📄 | ابحث عن مهارة قبل أن تكتبها · Skill scout before creating | SP-0003 Author a skill | — |
| AGENT-27 | 📄 | تطوير مهارة مقابل خط أساس · Evolve a skill against a baseline | SP-0003 Author a skill | git |
| AGENT-28 | 📄 | تحميل ضيق للفصول · Narrow loading caps | SP-0003 Author a skill | — |
| AGENT-34 | 📦 | تثبيت حزمة ECC · Install ECC (Everything Claude Code) | SP-0004 Agent introspection debugging | node |
| AGENT-17 | 🔑 | مهام مجدولة وروتينات · Scheduled tasks & routines | SP-0004 Agent introspection debugging | claude:tools, key:unspecified |
| AGENT-16 | 📄 | فحص تصميم الحلقة قبل الأتمتة · Loop design check | SP-0004 Agent introspection debugging | claude:tools |
| AGENT-18 | 📄 | العمل الخلفي والمراقبة · Background jobs & monitoring | SP-0004 Agent introspection debugging | — |
| AGENT-19 | 📄 | تشخيص الوكيل لنفسه · Agent introspection debugging | SP-0004 Agent introspection debugging | pip:hypothesis |
| AGENT-32 | 📄 | تعلم بإذن وعلى مستوى المشروع · Consent-gated lessons | SP-0004 Agent introspection debugging | — |
| AGENT-35 | 📄 | دليل ECC السريع: أي وكيل لأي مهمة · ECC roster quick map | SP-0004 Agent introspection debugging | — |
| AGENT-48 | 📄 | فريق بأدوار ومهام ومخرج متوقع · Role-goal crew with expected outputs | SP-0004 Agent introspection debugging | — |
| AGENT-38 | 📦 | MCP reference servers: ربط خوادم MCP المرجعية (ملفات، git، جلب · MCP reference servers: Wire reference MCP servers (filesystem, git, fetch, memory) into an agent as tools | SP-0005 Worktrees for parallel writers | npm:mcp-servers |
| AGENT-06 | 📄 | مصفوفة المسارات المتوازية · Parallel lane matrix | SP-0005 Worktrees for parallel writers | git |
| AGENT-07 | 📄 | توزيع معزول الفشل · Failure-isolated fan-out | SP-0005 Worktrees for parallel writers | — |
| AGENT-08 | 📄 | أشجار عمل للكتّاب المتوازيين · Worktrees for parallel writers | SP-0005 Worktrees for parallel writers | git, claude:tools |
| AGENT-09 | 📄 | سير عمل ديناميكي يدير وكلاء كثيرين · Dynamic workflows (Workflow tool) | SP-0005 Worktrees for parallel writers | claude:tools |
| AGENT-10 | 📄 | خط مراحل متتابع بمخرجات ملفات · Phase pipeline with file handoffs | SP-0005 Worktrees for parallel writers | — |
| AGENT-03 | 📄 | الاسترجاع التكراري · Iterative retrieval loop | SP-0109 Deep research with parallel sub-agents | claude:tools |

## self-discovery (mind)

chapter: [self-discovery](../powers/self-discovery.md) · card: `usip-library/cards/agents/self-discovery.md` · tools: `ai-tool-discovery` · `atlas-5000` · `atlas-ledger` · `boot` · `build-chapters` · `capability-atlas` · `capability-graph` · `capability-runtime-router` …

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| SELF-24 | ✅ | اسأل السجل قبل أن تنفي · Registry lookup before saying no | SP-0019 Registry before no | python3, npm:hyperframes, network |
| SELF-25 | ✅ | توافق إصدار بايثون · Python-version compatibility check | SP-0019 Registry before no | pip:kokoro, network |
| SELF-26 | ✅ | ثبّت ثم تحقق (بايثون) · Install then verify (Python venv) | SP-0019 Registry before no | pip:duckdb |
| SELF-27 | ✅ | ثبّت ثم تحقق (npm) · Install then verify (npm scratch dir) | SP-0019 Registry before no | node, pip:office |
| SELF-28 | ✅ | النماذج الثقيلة ممكنة على المعالج · Heavy ML is possible on CPU | SP-0019 Registry before no | pip:faster-whisper, pip:torch, gpu, network |
| SELF-29 | ✅ | بوابة الرخصة قبل التبني · License gate before adopting | SP-0019 Registry before no | ffmpeg, blender, pip:piper, npm:remotion … |
| SELF-32 | ✅ | التوثيق الحي لا الذاكرة · Live docs over memory | SP-0019 Registry before no | node, claude:tools |
| SELF-33 | ✅ | واجهات الذاكرة قديمة · Training-data APIs are stale | SP-0019 Registry before no | chromium, libreoffice, pip:numpy, pip:opencv … |
| SELF-36 | ✅ | حدود جلسة Claude Code السحابية · Claude Code cloud session limits | SP-0019 Registry before no | python3, docker, npm:p5 |
| SELF-01 | 📄 | اعرف قبل أن تقول لا · Registry before no | SP-0019 Registry before no | node, python3, claude:tools |
| SELF-02 | 📄 | سُلَّم حقيقة القدرة · Capability-truth ladder | SP-0019 Registry before no | ffmpeg, key:unspecified |
| SELF-03 | 📄 | الإثبات له تاريخ صلاحية · Proofs are dated leases | SP-0019 Registry before no | tesseract |
| SELF-04 | 📄 | التنفيذ ليس تحققًا · Executed is not verified | SP-0019 Registry before no | ffmpeg, chromium, libreoffice |
| SELF-30 | 📄 | أعد الاستخدام قبل البناء · Reuse before build matrix | SP-0019 Registry before no | — |
| SELF-34 | 📄 | تدقيق سطح مساحة العمل · Workspace surface audit | SP-0019 Registry before no | key:unspecified |
| SELF-35 | 📄 | استنتج سطحك · Infer your surface | SP-0019 Registry before no | python3 |
| SELF-38 | 📄 | تنفيذ الكود في تطبيقات claude.ai · claude.ai code execution and files | SP-0019 Registry before no | node, pip:office |
| SELF-39 | 📄 | مزايا تطبيق سطح المكتب · Desktop app extras | SP-0019 Registry before no | os:macos, claude:browser, key:unspecified |
| SELF-40 | 📄 | أداة موجودة = قوة مفتوحة · Tool present → power unlocked map | SP-0019 Registry before no | node, git |
| SELF-10 | ✅ | صفحات توثيق البيئة · Environment documentation pages | SP-0020 One-command capability card | — |
| SELF-12 | ✅ | بطاقة القدرات بسكربت واحد · One-command capability card | SP-0020 One-command capability card | python3, docker |
| SELF-13 | ✅ | فحص يدوي للآلة · Manual shell probe | SP-0020 One-command capability card | ffmpeg, python3, chromium, docker … |
| SELF-14 | ✅ | لا GPU: خطط للمعالج · No GPU: plan for CPU | SP-0020 One-command capability card | ffmpeg, chromium, pip:faster-whisper, pip:torch … |
| SELF-15 | ✅ | سُلَّم اختبار الشبكة · Network test ladder | SP-0020 One-command capability card | network |
| SELF-17 | ✅ | المفاتيح بالأسماء فقط · Credentials by name only | SP-0020 One-command capability card | pip:anthropic, key:unspecified |
| SELF-18 | ✅ | فحص مكتبات بايثون · Python import probe | SP-0020 One-command capability card | pip:numpy, pip:pillow, pip:opencv, pip:scipy … |
| SELF-19 | ✅ | Node والمتصفح المدمج · Node globals and bundled browser | SP-0020 One-command capability card | chromium, npm:p5 |
| SELF-20 | ✅ | خطوط عربية قبل الرندر · Arabic font probe | SP-0020 One-command capability card | fonts:arabic |
| SELF-21 | ✅ | صلاحيات الجذر وapt · Root and apt check | SP-0020 One-command capability card | — |
| SELF-22 | ✅ | Docker: العميل ليس الخدمة · Docker: client is not daemon | SP-0020 One-command capability card | docker |
| SELF-23 | ✅ | وصول GitHub في جلسات السحابة · GitHub access in cloud sessions | SP-0020 One-command capability card | git, gh |
| SELF-16 | 📄 | آداب البروكسي · Proxy etiquette | SP-0020 One-command capability card | — |
| SELF-31 | 📄 | مستكشف المهارات · Skill scout ladder | SP-0020 One-command capability card | — |
| SELF-37 | 📄 | صندوق تنفيذ الكود في API · API code-execution sandbox | SP-0020 One-command capability card | ffmpeg, pip:numpy, pip:pillow, pip:scipy … |
| SELF-05 | ✅ | اقرأ قائمة أدواتك · Read your own tool list | SP-0021 Read your own tool list | pip:higgsfield, key:graphify |
| SELF-06 | ✅ | حمّل الأدوات المؤجلة بـToolSearch · Load deferred tools with ToolSearch | SP-0021 Read your own tool list | claude:tools |
| SELF-07 | ✅ | جرد خوادم MCP وتكلفتها · MCP server inventory with cost flags | SP-0021 Read your own tool list | pip:higgsfield, key:unspecified |
| SELF-08 | ✅ | اكتشف المهارات قبل العمل · Discover skills before acting | SP-0021 Read your own tool list | claude:tools |
| SELF-09 | ✅ | الإضافات والمتجر · Plugins and marketplace check | SP-0021 Read your own tool list | — |
| SELF-11 | 🔑 | الموصلات والمفاتيح · Connectors and keys | SP-0021 Read your own tool list | claude:tools, key:unspecified |
| SELF-41 | 📄 | بطاقة القدرة والإيصال · Capability card and receipts | SP-0022 Capability card and receipts | ffmpeg |
| SELF-42 | 📄 | تصنيف الأعطال وأصغر إصلاح · Failure taxonomy with smallest fix | SP-0022 Capability card and receipts | key:unspecified |
| SELF-43 | 📄 | بوابة المدفوع والأثر الجانبي · Paid and side-effect gate | SP-0022 Capability card and receipts | ffmpeg, pip:piper |
