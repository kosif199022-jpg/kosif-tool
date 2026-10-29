# الوكلاء والتوجيه الذكي — Agents & routing (`agents`)

> مكتبة بروتوكول USIP v5.6، مولّدة بـ `scripts/smart_capabilities.py library` من `data/powers/*.json` و`data/tools.json`؛ لا تُحرَّر يدويًا. الدليل: [A28 اختيار القدرات](../protocol/A28-capability-routing.md) · [الفهرس](INDEX.md) · [النواة](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

## الفهرس / contents

- [متى تستخدم هذه المجموعة / when](#متى-تستخدم-هذه-المجموعة--when)
- [الحالة بالأرقام / status](#الحالة-بالأرقام--status)
- [الأدوات القابلة للتشغيل / runnable tools](#الأدوات-القابلة-للتشغيل--runnable-tools)
- [العائلات / families](#العائلات--families)
- [كل القدرات / every power](#كل-القدرات--every-power)

## متى تستخدم هذه المجموعة / when

كلمات التوجيه: agent orchestration tool routing discover automation وكلاء أدوات توجيه بحث

لا خط عمل مسجّل لهذه المجموعة؛ ركّبه من الأدوات أدناه.

العضوية في المجموعة تصنيف للتوجيه، لا دليل على أن القدرات تعمل معًا: اربطها بخط عمل مختبر فقط.

## الحالة بالأرقام / status

| الحالة | العدد | المعنى |
|---|---:|---|
| `proven` | 172 | ✅ proven: a proof exists in the catalog; still check its requirements here before calling it ready |
| `ready` | 21 | 🟢 ready: runnable without setup according to the catalog |
| `documented` | 65 | 📄 documented: a described method; needs building or wiring before it runs |
| `install` | 13 | 📦 install: needs a package, binary or model first |
| `key` | 2 | 🔑 key: needs an account, key or paid service (ask before any spend) |
| **المجموع** | **273** | |

## الأدوات القابلة للتشغيل / runnable tools

| الأداة | ما تفعله | ابدأ بـ | الدليل |
|---|---|---|---|
| `adobe-mcp-bridges` | ربط Claude ببرامج أدوبي (أفتر إفكتس وبريمير وفوتوشوب) | `python3 scripts/adobe_mcp.py list` | tested-here |
| `agent-guard` | حارس الوكيل: فحص الأوامر قبل تشغيلها وكشف الأسرار وخطة فروع متوازية | `python3 scripts/agent_guard.py rules` | tested-here |
| `ai-tool-discovery` | باحث القدرات ثنائي اللغة بلا اتصال | `python3 scripts/ai_tool_discovery.py "تحريك شخصيات فيديو" --top 8` | tested-here |
| `atlas-5000` | خريطة تغطية أطلس الـ5000 مهارة | `python3 scripts/atlas_5000.py stats --json` | tested-here |
| `atlas-ledger` | سجل الأطلس: حالة واحدة لكل مهارة | `python3 scripts/atlas_ledger.py stats --json` | tested-here |
| `boot` | إحاطة بدء الجلسة | `python3 scripts/boot.py` | tested-here |
| `build-chapters` | مولّد فصول العائلات | `python3 scripts/build_chapters.py` | untested |
| `business-workflows` | الذكاء الاصطناعي في الأعمال: 9 وظائف و64 خطة عمل بخطط تشغيل لClaude | `python3 scripts/business_workflows.py functions` | tested-here |
| `capability-atlas` | أطلس القدرات للبحث والتخطيط | `python3 scripts/capability_atlas.py stats --json` | tested-here |
| `capability-graph` | باني خريطة القدرات المترابطة | `python3 scripts/capability_graph.py build` | tested-here |
| `capability-runtime-router` | موجّه القدرات التنفيذية | `python3 scripts/capability_runtime_router.py --task "حلل فيديو مرجعي وأنتج مونتاج مشابه بأصولي" --limit 5 --json` | tested-here |
| `catalog-evidence-audit` | تدقيق أدلة الكتالوج | `python3 scripts/catalog_evidence_audit.py` | tested-elsewhere |
| `charter-ingest` | إدخال قائمة الميثاق: مجلس الخبراء 500 فهرسًا للاستشارة | `python3 scripts/charter_ingest.py roster.txt --out data/experts_500.json` | tested-here |
| `check-skill` | فحص سلامة المهارة | `python3 scripts/check_skill.py` | untested |
| `council` | مجلس البرو: خمسة متعارضين أو مجلس مناسب من 100 شخصية، ثلاث جولات وحكم بالدرجات | `python3 scripts/council.py plan "اعمل ريلز دعاء" --dir out/demo/council --options A,B,C` | tested-here |
| `fusionforge` | FusionForge v2 لوصفات الـWorkflow المركبة داخل المشروع | `python3 scripts/fusionforge.py propose "مونتاج ريلز بترجمة عربية" --project demo_project --from-brief out/20261021-reel/brief.json` | tested-here |
| `fusionforge-shared` | ذاكرة FusionForge المشتركة بوصفات مهارات معزولة | `python3 scripts/fusionforge_shared.py audit` | untested |
| `github-pulse` | نبض GitHub: أهم 1000 مستودع نشط في آخر 30 يومًا حسب المجال، والأفكار المنقولة منها | `python3 scripts/github_pulse.py top --domain design-ui -n 15` | tested-here |
| `github-top-repos` | متابعة أشهر 1000 مستودع | `python3 scripts/github_top_repos.py build` | tested-here |
| `hub` | بوابة KOSIF الموحّدة | `python3 scripts/hub.py find "اعمل فيديو موشن عربي متزامن مع صوتي"` | tested-here |
| `kosif-groups` | خريطة المجموعات مع القدرات الخارقة والسكربتات وخطط التثبيت | `python3 scripts/kosif_hubs.py` | tested-here |
| `kosif-mcp` | خادم MCP لكتالوج KOSIF | `python3 scripts/kosif_mcp.py` | tested-here |
| `kosif-remote-commander` | خادم KOSIF Remote Commander | `python3 scripts/kosif_remote_superpowers.py doctor` | tested-here |
| `local-first` | مدخل محلي بلا استنساخ | `python3 scripts/local_first.py doctor` | tested-here |
| `memory-ops` | عمليات الذاكرة | `python3 scripts/memory_ops.py propose --store memory.json --facts facts.json --out plan.json` | tested-here |
| `micro-index` | الفهرس الدقيق: سطر لكل قدرة وأداة وقدرة خارقة | `python3 scripts/micro_index.py build` | tested-here |
| `owned-repos` | خريطة مستودعات المالك وخريطة المهارات | `python3 scripts/owned_repos.py find "رسم شخصيات"` | tested-here |
| `photocraft-mcp` | PhotoCraft MCP: محرر صور مفتوح المصدر يتحكم فيه Claude | `python3 scripts/photocraft_mcp.py steps headless` | tested-here |
| `powers` | البحث في كتالوج القدرات | `python3 scripts/powers.py stats --domain motion --json` | tested-here |
| `probe-env` | فحص قدرات الجهاز | `python3 scripts/probe_env.py` | tested-elsewhere |
| `python-package-probe` | فاحص وجود حزم بايثون | `python3 scripts/python_package_probe.py pandas numpy httpx` | tested-here |
| `rea-bridge` | جسر أوامر REA | `python3 scripts/rea_bridge.py doctor` | tested-here |
| `rea-family-router` | موجّه عائلات REA | `python3 scripts/rea_family_router.py list` | tested-here |
| `rea-superpowers-map` | خريطة سوبر باور بمنهج REA | `python3 scripts/rea_superpowers_map.py build` | tested-here |
| `relabel-proofs` | إعادة تصنيف نطاق الأدلة | `python3 scripts/relabel_proofs.py` | untested |
| `repo-build` | مولّد ملفات أطلس الأساليب | `python3 tools/build.py` | untested |
| `requirements` | مخطط متطلبات القدرات | `python3 scripts/requirements.py present --json` | tested-here |
| `see-pro-cognitive-gate` | فاحص عقود التفكير والتوليف KOSIF SEE Pro | `python3 scripts/see_pro_cognitive_gate.py --self-test` | tested-here |
| `self-council` | مجلس المراجعة الذاتية: خمس شخصيات من Claude تنقد كل مهارة وميزة، مع سجل تغطية | `python3 scripts/self_council.py inventory --summary` | tested-here |
| `skill-intelligence` | محرك بروتوكول ذكاء المهارات الشامل | `python3 scripts/skill_intelligence.py brief "مونتاج ريلز على الإيقاع بترجمة عربية"` | tested-here |
| `skill-layout` | خريطة ترتيب المهارة | `python3 scripts/skill_layout.py build` | tested-here |
| `skill-loader` | خريطة التحميل الخفيف للمهارات | `python3 scripts/skill_loader.py build --check` | tested-here |
| `smart-capabilities` | فهرس ذكي للقدرات من أجل Claude | `python3 scripts/smart_capabilities.py groups` | tested-here |
| `superpower-fusion` | دمج القدرات في قدرات خارقة مترابطة | `python3 scripts/superpower_fusion.py build` | tested-here |
| `superpowers` | خريطة المستودعات الخارجية | `python3 scripts/superpowers.py list --capability voice --json` | tested-here |
| `superpowers-unified` | موجّه مهارات العمل ومثبّتها | `python3 scripts/superpowers_unified.py doctor` | tested-here |
| `superskills` | المهارات الخارقة: الـ114 مهارة الكاملة من مستودعك داخل سوبر باور | `python3 scripts/superskills.py find "نموذج مالي في إكسل"` | tested-here |
| `superskills-bridge` | جسر المهارات الخارقة: بحث للقراءة فقط في فهرس الـ114 مهارة | `python3 scripts/superskills_bridge.py doctor` | tested-here |
| `task-history` | سجل المهام: سجل لكل مهمة منجزة لإعادتها لاحقًا | `python3 scripts/task_history.py new --kind video` | tested-here |

الأوامر نسبية إلى مجلد المهارة (أو جذر المستودع لأدوات `tools/`)؛ `python3 scripts/hub.py tool <id>` يعطي كل الأوامر والمتطلبات والحدود.

## العائلات / families

| العائلة | القدرات | الفصل |
|---|---:|---|
| `agent-orchestration` | 55 | [agent-orchestration.md](../powers/agent-orchestration.md) |
| `runnable-tools` | 175 | [runnable-tools.md](../powers/runnable-tools.md) |
| `self-discovery` | 43 | [self-discovery.md](../powers/self-discovery.md) |

## كل القدرات / every power

مرتبة بالحالة ثم العائلة ثم المعرّف. `hub.py` و`skill_intelligence.py deep <ID>` يعطيان بطاقة القدرة كاملة بدليلها.

| المعرّف | الاسم | English | الحالة | المتطلبات |
|---|---|---|---|---|
| `AGENT-37` | Chroma: فهرسة المستندات في مخزن متجهات والإجابة عن | Chroma: Index documents into a vector store and answer semantic queries (RAG) | proven | pip:chromadb |
| `TOOL-01` | باحث القدرات ثنائي اللغة بلا اتصال | Offline bilingual capability finder | proven | python3 |
| `TOOL-02` | إحاطة بدء الجلسة | Session boot briefing | proven | python3 |
| `TOOL-03` | أطلس القدرات للبحث والتخطيط | Capability Atlas search and planner | proven | pip:pillow, pip:opencv |
| `TOOL-04` | موجّه القدرات التنفيذية | Capability runtime router | proven | python3 |
| `TOOL-05` | بوابة KOSIF الموحّدة | KOSIF hub (front door) | proven | python3 |
| `TOOL-06` | خادم MCP لكتالوج KOSIF | KOSIF catalog MCP server | proven | python3 |
| `TOOL-07` | مدخل محلي بلا استنساخ | Local-first no-clone entry | proven | python3 |
| `TOOL-08` | فاحص وجود حزم بايثون | Python package presence probe | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `TOOL-09` | موجّه مهارات العمل ومثبّتها | Process-skill router and installer | proven | python3, imagemagick |
| `TOOL-10` | مقدّر سعة الأنظمة | System Capacity Sizer | proven | python3 |
| `TOOL-100` | خريطة ترتيب المهارة | Skill Layout Map | proven | python3 |
| `TOOL-103` | فاحص سلامة أطلس الأنماط | Style atlas repository validator | proven | python3 |
| `TOOL-105` | منقّب قدرات الأطلس من البيانات الوصفية | Atlas metadata capability miner | proven | python3, blender, npm:rea, engine:ghidra |
| `TOOL-106` | خريطة تغطية أطلس الـ5000 مهارة | Atlas-5000 coverage map | proven | python3 |
| `TOOL-107` | سجل الأطلس: حالة واحدة لكل مهارة | Atlas ledger: one status for every Atlas skill | proven | python3, npm:rea |
| `TOOL-108` | خريطة سوبر باور بمنهج REA | Superpowers map, REA approach | proven | python3, npm:rea |
| `TOOL-11` | مختبر الابتكار الهندسي | Invention Lab Candidates | proven | pip:hypothesis |
| `TOOL-115` | الرسم الموحد: خطوط وأشكال وطبقات وتصدير | Unified Draw: freehand + geometry + layered export | proven | ffmpeg, pip:pillow |
| `TOOL-116` | فهرس ذكي للقدرات من أجل Claude | Smart capability index for Claude | proven | python3, npm:rea, engine:ghidra |
| `TOOL-117` | محرر الوسائط الموحد: صور ورسم وتحريك وفيديو | Unified Media: photo adjustments + drawn overlays + GIF/MP4 | proven | ffmpeg, imagemagick, pip:numpy, pip:pillow |
| `TOOL-118` | السينما الموحدة: مونتاج الفيديو مع الصوت وحركة الكاميرا | Unified Cinematic: sound-clocked animation and video | proven | ffmpeg, imagemagick, pip:numpy, pip:pillow |
| `TOOL-119` | دمج رندر Blender Cycles مع مونتاج KOSIF والصوت | Blender Cycles + KOSIF Cinematic compositor | proven | ffmpeg, blender, pip:pillow, npm:rea |
| `TOOL-12` | جسر الصوت إلى لوحة القصة | Audio-to-Storyboard Bridge | proven | python3 |
| `TOOL-120` | إنشاء مشهد إنقاذ قطة ثلاثي الأبعاد داخل Blender | Create an editable Blender 3D cat rescue demo | proven | python3, blender |
| `TOOL-121` | تطوير فرو القطة والملامح في Blender Cycles | Blender Cat Fur Upgrade: renderable hair geometry and character detail | proven | python3, blender |
| `TOOL-122` | محرر KOSIF Timeline: مونتاج متعدد المسارات مع تراجع وإعادة | KOSIF Timeline: genuine multitrack video, image and audio editor | proven | ffmpeg, pip:pillow |
| `TOOL-123` | تجربة مونتاج KOSIF Timeline تلقائية بملفات أصلية مولدة | KOSIF Timeline one-command synthetic media demo | proven | ffmpeg, pip:pillow |
| `TOOL-124` | محرك بروتوكول ذكاء المهارات الشامل | Universal Skill Intelligence Protocol engine | proven | python3 |
| `TOOL-125` | FusionForge v2 لوصفات الـWorkflow المركبة داخل المشروع | FusionForge v2 project-scoped composite workflow recipes | proven | python3 |
| `TOOL-127` | دمج القدرات في قدرات خارقة مترابطة | Superpower fusion (powers to connected superpowers) | proven | python3 |
| `TOOL-128` | الخريطة الذهنية المرحلية وتدقيق التكرار | Task-stage capability mind map and duplicate audit | proven | python3, npm:mermaid |
| `TOOL-129` | خريطة المجموعات مع القدرات الخارقة والسكربتات وخطط التثبيت | Group map with superpowers, scripts and install plans | proven | node, python3 |
| `TOOL-13` | مُصرِّف حركة SVG المتزامنة مع الصوت | Audio-timed SVG motion compiler | proven | ffmpeg, node, python3, chromium |
| `TOOL-130` | فريق مونتاج برو (صوت أو فيديو إلى مونتاج أو موشن) | Montage Pro task force (audio/video to montage or motion) | proven | ffmpeg, chromium, imagemagick, yt-dlp |
| `TOOL-131` | مصنع الريلز: صوت وتوقيت كلمات ولقطات مرخصة ← ريلز 9:16 مفحوص | Reel factory: voice + word timings + licensed shots → verified 9:16 reel | proven | ffmpeg, node, chromium, fonts:arabic |
| `TOOL-132` | دعاء يوم الأربعاء — محرك ريل دعاء موشن جرافيك 9:16 | Wednesday-morning dua reel (دعاء يوم الأربعاء) — 9:16 motion-graphics dua engine | proven | ffmpeg, node, chromium, yt-dlp |
| `TOOL-133` | ملتقط بث DASH وHLS للمونتاج | DASH/HLS stream grabber for editing | proven | ffmpeg, python3 |
| `TOOL-136` | أطلس مناهج كتب الرسم مع رسم بنائي بالطبقات | Drawing-book methods atlas with layered construction SVGs | proven | python3, tesseract |
| `TOOL-138` | تكامل مصمم وREA: فحص صور وتوليف مهارات آمن | Mosamem x REA source-safe image preflight and capability fusion | proven | python3, chromium, npm:rea |
| `TOOL-139` | إدخال قائمة الميثاق: مجلس الخبراء 500 فهرسًا للاستشارة | Charter roster ingest: the 500-expert council as a consultable index | proven | python3 |
| `TOOL-14` | محرك حركة SVG | SVG motion engine runtime | proven | ffmpeg, node, python3, chromium |
| `TOOL-140` | ذكاء الصور المحلي: إزالة الخلفية والملء الذكي بنموذج ONNX تختاره | Local image AI: remove background and smart fill with your own ONNX model | proven |  |
| `TOOL-141` | حزمة المطالبات: كل مطالبة في كتلة كود قابلة للنسخ مع فحص يحذّر فقط | Prompt pack: copyable prompts, one code block each, with a warn-only lint | proven | python3, key:video-gen |
| `TOOL-142` | فهرس المصادر: الذاكرة الفهرسية لمرفقات المستخدم داخل مجلد العمل | Sources index: per-work-dir index memory of the user's attachments | proven | pip:office |
| `TOOL-143` | خريطة مستودعات المالك وخريطة المهارات | Owned-repositories map and skill map | proven | python3 |
| `TOOL-144` | مدرب الرسم من فصول الكتب والتشخيص البصري المستقل | Book-chapter drawing coach and independent raster visual QA | proven | pip:pillow |
| `TOOL-145` | رياضيات القرار: نطاقات مونت كارلو ونقطة التعادل وترتيب ICE والقيمة الحالية ونقطة انقلاب القرار | Decision math: Monte Carlo ranges, break-even, ICE, NPV/IRR and flip thresholds | proven | python3, npm:p5 |
| `TOOL-146` | جسيمات قابلة للقفز: انفجار بصيغة مغلقة وفحص الميزانية وإطار SVG | Seekable particles: closed-form bursts, budget check and SVG frame | proven | python3, npm:three |
| `TOOL-147` | لوح الخرائط: إسقاط الإحداثيات إلى بكسلات وتصنيف الخرائط الملونة وسجل المصادر | Map plate: projection to pixels, choropleth classes and source ledger | proven | python3, fonts:arabic |
| `TOOL-148` | مصنع البرومبتات: برومبتات طبقية وفحص البرومبت وقائمة لقطات بإطارات دقيقة | Prompt forge: layered generator prompts, prompt lint and frame-exact shot lists | proven | python3 |
| `TOOL-149` | تخطيط المخططات: فحص الرسم البياني وتخطيط طبقي حتمي وSVG جاهز للعربية | Diagram layout: graph lint, deterministic layered layout and RTL-ready SVG | proven | python3 |
| `TOOL-15` | جسر توقيتات Motion Starter Kit | Motion Starter Kit timing bridge | proven | python3 |
| `TOOL-150` | إيقاع الواجهات: مسار مؤشر بتسهيل وعكس تخطيط للعربية وفحص الحلقة المتصلة | UI beat: eased cursor keyframes, RTL layout mirror and seamless-loop check | proven | python3 |
| `TOOL-151` | مختبر الإحصاء: اختبار A/B وحجم العينة ووصف عمود وأرباح الدفعات | Stats lab: A/B test, sample size, column statistics and FIFO/LIFO gains | proven | python3 |
| `TOOL-152` | تجهيز نص التعليق الصوتي: تقطيع آمن وتقدير المدة وSSML | TTS script prep: prosody-safe chunks, duration estimate and SSML | proven | python3 |
| `TOOL-153` | رموز الهوية: ألوان الشعار ورموز بثلاث طبقات ومصفوفة تباين WCAG | Brand tokens: SVG palette, 3-tier design tokens and WCAG contrast matrix | proven | python3, npm:axe |
| `TOOL-154` | حارس الوكيل: فحص الأوامر قبل تشغيلها وكشف الأسرار وخطة فروع متوازية | Agent guard: shell preflight, transcript secret scan and worktree plans | proven | python3, git |
| `TOOL-156` | البحث في كتالوج القدرات | Power catalog search | proven | python3, npm:mermaid |
| `TOOL-157` | نسخة مرسومة أو ملوّنة باليد لأي صورة أو مشهد متخيَّل: رصاص، فحم، حبر، ألوان خشبية، فرشاة زيت أو ألوان مائية | Hand-drawn or hand-painted version of any photo or imagined scene: pencil, charcoal, ink, coloured pencil, oil brush or watercolour | proven | chromium, blender, pip:numpy, pip:opencv |
| `TOOL-158` | مجلس خبراء الرسم: أحد عشر خبيرًا من بطاقات الكتب الـ48 يراجعون الصورة قبل إرسالها | Drawing council: eleven experts from the 48 method cards review an image before it is sent | proven | pip:pillow |
| `TOOL-159` | مختبر البرومبت | Prompt Lab | proven | python3 |
| `TOOL-16` | إنشاء فيلم سبورة مرسوم وتصييره | Doodle film runtime and renderer | proven | ffmpeg, node, python3, chromium |
| `TOOL-160` | متابعة أشهر 1000 مستودع | GitHub Top-1000 Tracker | proven | python3 |
| `TOOL-161` | الفهرس الدقيق: سطر لكل قدرة وأداة وقدرة خارقة | Micro index: one line per power, tool and superpower | proven | python3 |
| `TOOL-162` | خريطة المستودع | Repo Map | proven | python3 |
| `TOOL-163` | عمليات الذاكرة | Memory Ops | proven | python3 |
| `TOOL-164` | فيزياء الحركة | Motion Physics | proven | python3, npm:animejs, npm:react |
| `TOOL-165` | سطور الترجمة: من توقيت الكلمات إلى ترجمة مقروءة | Caption lines: word timings to readable SRT/VTT | proven | pip:faster-whisper, key:openai |
| `TOOL-166` | خط اللوك: تلوين واحد لـ ffmpeg وSVG وGLSL | Look pipeline: one colour grade for ffmpeg, SVG/CSS and GLSL | proven | ffmpeg, python3 |
| `TOOL-167` | فاحص أرقام الدروس والشروح | Lesson number integrity checker | proven | python3 |
| `TOOL-168` | التعديل السريع: قص فوري يعرف الإطارات المفتاحية، مغيّر صوت، تفتيح الفيديو المظلم، استخراج الصوت | Fast Edit: keyframe-aware instant cut, voice presets, low-light lift, audio extract | proven | ffmpeg, python3 |
| `TOOL-169` | محرك الخامات الملوّنة: ألوان خشبية وفرشاة زيت وألوان مائية لأي صورة | Colour media engine: coloured pencil, oil brush and watercolour painting of a photo | proven | chromium, pip:numpy, pip:opencv, pip:mediapipe |
| `TOOL-17` | مولّد مشاريع بداية لمحركات الحركة | Third-party motion engine scaffolder | proven | python3, npm:three, npm:gsap, npm:remotion |
| `TOOL-170` | سجل المهام: سجل لكل مهمة منجزة لإعادتها لاحقًا | Task history: record every finished task and repeat it later | proven | python3 |
| `TOOL-171` | محرك المصفوفات اللانهائية للأساليب السببية | KOSIF Infinite Matrices causal style engine | proven | ffmpeg, python3, chromium, npm:rea |
| `TOOL-172` | البحث عن مراجع فيديو إنستجرام وربطها بالمصفوفات اللانهائية | Instagram Reference Discovery → Infinite Matrices | proven | python3 |
| `TOOL-173` | البحث عن فيديوهات إنستجرام لمنتج وتحميلها | Instagram product video finder | proven | ffmpeg, python3, yt-dlp |
| `TOOL-174` | تشغيل المهام الطويلة في الخلفية وانتظارها بلا sleep | Background job runner and waiter (no sleep waits) | proven | ffmpeg, node, python3, chromium |
| `TOOL-175` | معمل السينما: كشف القطعات، حذف الصمت، تايملاين OTIO/EDL، ألوان LUT، تثبيت الكاميرا، تأطير ذكي بالطول، حركة كاميرا، مراجعة A/B | Cinema Lab: scene cuts, silence cut, OTIO/EDL timelines, LUT looks, stabilise, smart portrait reframe, camera moves, A/B review | proven | ffmpeg, pip:numpy, pip:opencv, npm:remotion |
| `TOOL-176` | تصدير للبرامج: افتح تايملاين KOSIF في دافنشي وفاينال كت وبريمير وبلندر وكاب كات | NLE Export: open a KOSIF timeline in DaVinci Resolve, Final Cut Pro, Premiere Pro, Blender or CapCut | proven | ffmpeg, python3, blender |
| `TOOL-18` | مكتبة رياضيات الحركة | Motion math toolkit | proven | node, python3 |
| `TOOL-19` | تصيير لقطات B-roll بحركة كاميرا | Cinematic B-roll Renderer | proven | ffmpeg, python3 |
| `TOOL-20` | مُخطِّط قطعات اللقطات الحقيقية | Footage-First Cut Planner | proven | python3 |
| `TOOL-21` | فاحص توقيت الفيديو المرجعي | Reference Video Timing Probe | proven | ffmpeg, python3 |
| `TOOL-22` | محرك إعادة بناء المونتاج المرجعي | Reference Edit Engine | proven | pip:higgsfield, npm:remotion, npm:react |
| `TOOL-23` | البصمة البصرية للفيديو المرجعي | Reference Visual Fingerprint | proven | ffmpeg, python3 |
| `TOOL-24` | جسر سير عمل الفيديو | Video Workflow Bridge | proven | python3 |
| `TOOL-25` | مستخرج إشارات التوقيت من الصوت | WAV audio cue mapper | proven | pip:faster-whisper |
| `TOOL-26` | فرضيات إيقاع الموسيقى | Music rhythm hypotheses | proven | python3 |
| `TOOL-27` | تحريك الشخصية بكامل الجسم | Full-body character animator | proven | ffmpeg, pip:pillow, pip:rdkit |
| `TOOL-28` | تحريك ذراع الشخصية بالحركية العكسية | Character IK arm animator | proven | ffmpeg, pip:pillow |
| `TOOL-29` | رسم الشخصيات والمشاهد بالكود | Code Drawing Master storyboards | proven | pip:faster-whisper |
| `TOOL-30` | الرسم الإبداعي بالطبقات | Creative Paint layered renderer | proven | ffmpeg, pip:pillow |
| `TOOL-31` | الرسم الذكي ومساعد الأشكال | Smart Draw shape assist | proven | pip:pillow |
| `TOOL-32` | فحص المشروع المحلي دون تشغيل | Local project static audit | proven | python3, npm:rea, engine:ghidra |
| `TOOL-34` | باني خريطة القدرات المترابطة | Capability Graph Builder | proven | node, python3, key:graphify |
| `TOOL-35` | بوابة جودة خطة المونتاج | Reference-edit structural quality gate | proven | python3, npm:remotion |
| `TOOL-36` | تدقيق واجهة بايثون في Blender | Blender Python API audit | proven | python3, blender |
| `TOOL-37` | جسر Blender الآمن | Safe headless Blender bridge | proven | python3, chromium, blender |
| `TOOL-38` | رندر Cycles إلى فيديو مُتحقَّق منه | Cycles scene to verified video | proven | ffmpeg, python3, blender |
| `TOOL-40` | رندر ثلاثي الأبعاد مستقل عن Blender | Native 3D renderer (no Blender) | proven | ffmpeg, blender, pip:pillow |
| `TOOL-41` | مُصدِّر GLB مستقل عن Blender | Native GLB exporter (no Blender) | proven | python3, blender, npm:three |
| `TOOL-42` | مختبر مطابقة الخطوط العربية | Arabic-aware font fidelity lab | proven | pip:pillow, fonts:arabic |
| `TOOL-43` | بحث مهارات أطلس الخارجية | Atlas external skill search | proven | python3, blender |
| `TOOL-44` | تدقيق بيانات أطلس الوصفية | Atlas metadata audit | proven | python3 |
| `TOOL-45` | مستكشف المواقع بالمتصفح | Browser scout site survey | proven | python3, chromium |
| `TOOL-46` | بحث المصادر الإبداعية دون اتصال | Creative sources offline search | proven | python3, npm:rea |
| `TOOL-47` | بوابة الوسائط المرخّصة | Licensed stock media gateway | proven | ffmpeg, python3, yt-dlp |
| `TOOL-50` | مستكشف مصادر المجتمع | Community source scout | proven | python3 |
| `TOOL-52` | موجّه عائلات REA | REA Family Router | proven | python3, npm:rea, engine:android, engine:binwalk |
| `TOOL-54` | فحص المستودعات وحزمها | Repository Capability Packer | proven | python3 |
| `TOOL-55` | خادم KOSIF Remote Commander | KOSIF Remote Commander MCP | proven | node, python3 |
| `TOOL-57` | تحزيم المهارة للرفع إلى claude.ai | Skill Packager for claude.ai | proven | python3 |
| `TOOL-61` | مكتبة KOSIF الشاملة للخطوط وأفكار التصميم من صادرات تيليجرام | KOSIF Telegram Typography Atlas — private-safe font knowledge and idea search | proven | fonts:arabic |
| `TOOL-62` | دراسة تطبيق ويب عام بـ REA (حقائق فقط) | Web app study (public frontend, REA, facts only) | proven | python3, chromium, npm:rea |
| `TOOL-63` | أطلس الأساليب الكامل (86 طريقة): بحث وتوليف وموجز إنتاج وهيكل مشروع شرح | Futurepedia AI Style Atlas — all 86 methods: search, fusion, storyboard-first briefs and engine scaffolds | proven | python3 |
| `TOOL-64` | رندر أفلام الشرح: ستوريبورد وفحص حتمية وMP4 حقيقي بصوت مُركّب | Atlas explainer renderer: storyboard, determinism check and real MP4 with synthesized score | proven | ffmpeg, python3, chromium |
| `TOOL-65` | الذكاء الاصطناعي في الأعمال: 9 وظائف و64 خطة عمل بخطط تشغيل لClaude | AI for business: 9 functions, 64 workflows, Claude-native gated runbooks | proven | python3, key:unspecified |
| `TOOL-66` | مناهج مستخلصة من الكتب: التفكير الجانبي والهندسة العملية والأدلة البايزية والشخصية وفحوص المحاسبة ووضوح البرومنت | Book-distilled methods: lateral ideas, pragmatic engineering, Bayesian evidence, personality, accounting checks, prompt clarity | proven | python3 |
| `TOOL-67` | مصحّح الامتحان الخفي التفاضلي | Differential hidden-exam scorer | proven | python3 |
| `TOOL-68` | مجلس البرو: خمسة متعارضين أو مجلس مناسب من 100 شخصية، ثلاث جولات وحكم بالدرجات | Pro Council: five opposing members or a task-fitted council from 100 personas, three rounds, a scored verdict | proven | python3 |
| `TOOL-69` | محرك التفكير وقوالبه | Thinking engine scaffolds | proven | python3 |
| `TOOL-70` | مكتبة الأساليب: 586 أسلوبًا بصريًا بالاسم (86 من أطلس Futurepedia + 500 أصلي) — بحث ووصف وبرومنت وعينة وكتالوج PDF مصوّر | Style library — 586 visual styles by name (86 Futurepedia-derived + 500 original): find, describe, prompt, swatch, illustrated PDF catalog | proven | python3, chromium |
| `TOOL-72` | مخطط متطلبات القدرات | Power requirements planner | proven | node, python3, key:unspecified |
| `TOOL-73` | أداة سطر أوامر لأطلس أنماط KOSIF | KOSIF style atlas CLI | proven | python3, npm:remotion |
| `TOOL-74` | بوابة حفظ الحقائق عند إعادة الصياغة | Rewrite Fact Anchor Gate | proven | python3 |
| `TOOL-75` | فاحص العبارات الكتابية النمطية | Writing Tell Scanner | proven | python3 |
| `TOOL-76` | فاحص عقود التفكير والتوليف KOSIF SEE Pro | SEE Pro Cognitive Fusion contract verifier | proven | python3, network |
| `TOOL-77` | محلّل نِسَب أبعاد الفيديو | Flexible aspect ratio resolver | proven | python3 |
| `TOOL-78` | محوّل HTML إلى فيديو MP4 | HTML to MP4 renderer | proven | ffmpeg, node, python3, chromium |
| `TOOL-79` | بوابة فحص تسليم الفيديو | Video delivery gate | proven | ffmpeg, python3 |
| `TOOL-80` | محلّل نسب العرض المرن | Flexible aspect ratio resolver | proven | python3 |
| `TOOL-81` | محوّل حتمي من HTML إلى فيديو MP4 | Deterministic HTML-to-MP4 renderer | proven | ffmpeg, python3, chromium, npm:gsap |
| `TOOL-82` | بوابة فحص تسليم الفيديو | Video delivery gate | proven | ffmpeg, python3 |
| `TOOL-85` | محرك محاكاة الفيديو المرجعي | KOSIF Mimic reference rebuilder | proven | ffmpeg, tesseract, pip:numpy, pip:pillow |
| `TOOL-86` | محوّل الترجمات إلى توقيت الكلمات | Subtitle to words.json converter | proven | pip:faster-whisper |
| `TOOL-88` | استوديو التطبيقات للصور والتصميم | App Studio photo & design CLI | proven | ffmpeg, chromium, pip:numpy, pip:pillow |
| `TOOL-89` | حزمة الرسم في استوديو التطبيقات | App Studio painting batch | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `TOOL-91` | مراجعة ساكنة لنصوص مهارات الأطلس | Atlas skill-body static audit | proven | python3 |
| `TOOL-92` | تحويل مراجعة الأطلس إلى بيان مُراجَع | Atlas audit to reviewed manifest | proven | python3, npm:rea |
| `TOOL-93` | جلب المرجع المسموح وقياسه | Permitted reference fetch and measure | proven | ffmpeg, python3 |
| `TOOL-95` | تحميل لقطات مجانية بلا مفتاح (Pexels وMixkit) | Keyless stock footage fetcher (Pexels, Mixkit) | proven | ffmpeg, python3, key:unspecified |
| `TOOL-96` | خريطة المستودعات الخارجية | External repository tool map | proven | ffmpeg, chromium, pip:faster-whisper |
| `TOOL-97` | فرز المثبّتات | Installer Triage | proven | python3, npm:rea, 7zip, innoextract |
| `TOOL-98` | جسر أوامر REA | REA CLI Bridge | proven | python3, npm:rea |
| `SELF-05` | اقرأ قائمة أدواتك | Read your own tool list | proven | pip:higgsfield, key:graphify |
| `SELF-06` | حمّل الأدوات المؤجلة بـToolSearch | Load deferred tools with ToolSearch | proven | claude:tools |
| `SELF-07` | جرد خوادم MCP وتكلفتها | MCP server inventory with cost flags | proven | pip:higgsfield, key:unspecified |
| `SELF-08` | اكتشف المهارات قبل العمل | Discover skills before acting | proven | claude:tools |
| `SELF-09` | الإضافات والمتجر | Plugins and marketplace check | proven |  |
| `SELF-10` | صفحات توثيق البيئة | Environment documentation pages | proven |  |
| `SELF-12` | بطاقة القدرات بسكربت واحد | One-command capability card | proven | python3, docker |
| `SELF-13` | فحص يدوي للآلة | Manual shell probe | proven | ffmpeg, python3, chromium, docker |
| `SELF-14` | لا GPU: خطط للمعالج | No GPU: plan for CPU | proven | ffmpeg, chromium, pip:faster-whisper, pip:torch |
| `SELF-15` | سُلَّم اختبار الشبكة | Network test ladder | proven | network |
| `SELF-17` | المفاتيح بالأسماء فقط | Credentials by name only | proven | pip:anthropic, key:unspecified |
| `SELF-18` | فحص مكتبات بايثون | Python import probe | proven | pip:numpy, pip:pillow, pip:opencv, pip:scipy |
| `SELF-19` | Node والمتصفح المدمج | Node globals and bundled browser | proven | chromium, npm:p5 |
| `SELF-20` | خطوط عربية قبل الرندر | Arabic font probe | proven | fonts:arabic |
| `SELF-21` | صلاحيات الجذر وapt | Root and apt check | proven |  |
| `SELF-22` | Docker: العميل ليس الخدمة | Docker: client is not daemon | proven | docker |
| `SELF-23` | وصول GitHub في جلسات السحابة | GitHub access in cloud sessions | proven | git, gh |
| `SELF-24` | اسأل السجل قبل أن تنفي | Registry lookup before saying no | proven | python3, npm:hyperframes, network |
| `SELF-25` | توافق إصدار بايثون | Python-version compatibility check | proven | pip:kokoro, network |
| `SELF-26` | ثبّت ثم تحقق (بايثون) | Install then verify (Python venv) | proven | pip:duckdb |
| `SELF-27` | ثبّت ثم تحقق (npm) | Install then verify (npm scratch dir) | proven | node, pip:office |
| `SELF-28` | النماذج الثقيلة ممكنة على المعالج | Heavy ML is possible on CPU | proven | pip:faster-whisper, pip:torch, gpu, network |
| `SELF-29` | بوابة الرخصة قبل التبني | License gate before adopting | proven | ffmpeg, blender, pip:piper, npm:remotion |
| `SELF-32` | التوثيق الحي لا الذاكرة | Live docs over memory | proven | node, claude:tools |
| `SELF-33` | واجهات الذاكرة قديمة | Training-data APIs are stale | proven | chromium, libreoffice, pip:numpy, pip:opencv |
| `SELF-36` | حدود جلسة Claude Code السحابية | Claude Code cloud session limits | proven | python3, docker, npm:p5 |
| `AGENT-50` | قرار الذاكرة: إضافة أو تحديث أو حذف أو لا شيء | Memory decision step: add, update, delete or no-op | ready | python3 |
| `TOOL-101` | مولّد ملفات أطلس الأساليب | Style Atlas Builder | ready | python3 |
| `TOOL-102` | فاحص أصالة الملفات الإبداعية | Brief originality checker | ready | python3 |
| `TOOL-104` | تدقيق نصوص مصادر الأطلس | Atlas source-text audit | ready | python3, blender, engine:ghidra |
| `TOOL-109` | منتقي مناهج الأطلس للقراءة فقط | Atlas read-only method selector | ready | python3, blender, engine:ghidra |
| `TOOL-110` | ملخص مراجعة الأطلس | Atlas review summary | ready | python3, blender, engine:ghidra |
| `TOOL-111` | مناهج الأطلس المراجَعة | Reviewed Atlas methods | ready | python3, blender, engine:ghidra |
| `TOOL-112` | موجّه مناهج الأطلس حسب المهمة | Atlas task method router | ready | python3, blender, engine:ghidra |
| `TOOL-113` | نقل مناهج الأطلس المثبتة | Atlas verified method transfer | ready | python3, blender, engine:ghidra |
| `TOOL-114` | مساعد فيديو الحركة في Blender | Blender motion video helper | ready | python3, blender, engine:ghidra |
| `TOOL-126` | ذاكرة FusionForge المشتركة بوصفات مهارات معزولة | FusionForge Shared Memory: reviewed cross-project skill structures | ready | python3 |
| `TOOL-134` | دراسة الرسم التدريجي والظل الأصلي | Staged drawing and original three-value visual studies | ready | python3 |
| `TOOL-135` | أكاديمية الرسم والدروس المبنية على مصادر | Source-aware drawing school and user-authorized book audits | ready | python3 |
| `TOOL-137` | منظور هندسي ومقاييس التباين اللوني | Original two-point perspective and numeric palette analysis | ready | python3, npm:axe |
| `TOOL-33` | تدقيق أدلة الكتالوج | Catalog Evidence Audit | ready | python3 |
| `TOOL-56` | فحص سلامة المهارة | Skill Health Check | ready | python3 |
| `TOOL-58` | إعادة تصنيف نطاق الأدلة | Proof Scope Relabeler | ready | python3 |
| `TOOL-59` | استيراد الملفات الإبداعية | Creative brief importer | ready | python3 |
| `TOOL-60` | مزامنة الكتالوج مع PromptsMotion | PromptsMotion catalog sync | ready | python3 |
| `TOOL-71` | فحص قدرات الجهاز | Machine capability probe | ready | node, python3, docker, gpu |
| `TOOL-99` | مولّد فصول العائلات | Family Chapter Generator | ready | python3 |
| `AGENT-01` | متى تفوّض ومتى تعمل بنفسك | Delegate or do it yourself | documented | claude:tools |
| `AGENT-02` | حزمة التنفيذ: موجز تفويض كامل | Execution packet (delegation brief) | documented | claude:tools |
| `AGENT-03` | الاسترجاع التكراري | Iterative retrieval loop | documented | claude:tools |
| `AGENT-04` | وكلاء مخصصون في Claude Code | Custom subagents (.claude/agents) | documented | git, claude:tools |
| `AGENT-05` | إيصال مكتوب لكل نتيجة | Typed receipts (exposure ≠ authorization ≠ execution ≠ verification) | documented | ffmpeg |
| `AGENT-06` | مصفوفة المسارات المتوازية | Parallel lane matrix | documented | git |
| `AGENT-07` | توزيع معزول الفشل | Failure-isolated fan-out | documented |  |
| `AGENT-08` | أشجار عمل للكتّاب المتوازيين | Worktrees for parallel writers | documented | git, claude:tools |
| `AGENT-09` | سير عمل ديناميكي يدير وكلاء كثيرين | Dynamic workflows (Workflow tool) | documented | claude:tools |
| `AGENT-10` | خط مراحل متتابع بمخرجات ملفات | Phase pipeline with file handoffs | documented |  |
| `AGENT-11` | مراجعة سانتا المزدوجة | Santa dual review | documented | claude:tools |
| `AGENT-12` | مجلس الأصوات الأربعة | Four-voice council for ambiguous decisions | documented | claude:tools |
| `AGENT-13` | حلقة المولّد والمقيّم | Generator–evaluator loop | documented | chromium |
| `AGENT-14` | محقق خصم يفترض الرفض | Adversarial verifier (fail closed) | documented | claude:tools |
| `AGENT-15` | لوحة أدوار متعددة | Role-split review panel | documented |  |
| `AGENT-16` | فحص تصميم الحلقة قبل الأتمتة | Loop design check | documented | claude:tools |
| `AGENT-18` | العمل الخلفي والمراقبة | Background jobs & monitoring | documented |  |
| `AGENT-19` | تشخيص الوكيل لنفسه | Agent introspection debugging | documented | pip:hypothesis |
| `AGENT-20` | الخطافات حواجز آلية | Hooks as automatic guardrails | documented |  |
| `AGENT-21` | بوابة التسليم وسجل التغطية | Delivery gate & coverage ledger | documented |  |
| `AGENT-22` | خوادم MCP: إضافة وتدقيق وميزانية | MCP servers: add, vet, budget | documented | claude:tools, key:unspecified |
| `AGENT-23` | سُلَّم اختيار السطح | Capability surface ladder | documented | ffmpeg, python3, key:unspecified |
| `AGENT-24` | الإضافات والأسواق | Plugins & marketplaces | documented |  |
| `AGENT-25` | تأليف مهارة | Author a skill | documented |  |
| `AGENT-26` | ابحث عن مهارة قبل أن تكتبها | Skill scout before creating | documented |  |
| `AGENT-27` | تطوير مهارة مقابل خط أساس | Evolve a skill against a baseline | documented | git |
| `AGENT-28` | تحميل ضيق للفصول | Narrow loading caps | documented |  |
| `AGENT-29` | اقتصاد السياق | Context economy | documented | claude:tools |
| `AGENT-30` | توجيه الجهد ومستوى النموذج | Effort and tier routing | documented | claude:tools |
| `AGENT-31` | ملف تسليم الجلسة | Session handoff file | documented |  |
| `AGENT-32` | تعلم بإذن وعلى مستوى المشروع | Consent-gated lessons | documented |  |
| `AGENT-33` | خريطة أسطح الذاكرة | Memory surfaces map | documented | key:graphify |
| `AGENT-35` | دليل ECC السريع: أي وكيل لأي مهمة | ECC roster quick map | documented |  |
| `AGENT-39` | طبقات التعليمات ونطاق AGENTS.md | Instruction layering and AGENTS.md scope | documented |  |
| `AGENT-40` | ضغط السياق بملخص تسليم | Context compaction as a handoff | documented |  |
| `AGENT-41` | وضع التخطيط غير المعدِّل | Non-mutating plan mode | documented |  |
| `AGENT-42` | انضباط قائمة الخطوات | Plan checklist discipline | documented |  |
| `AGENT-43` | الهدف المستمر وتدقيق الإكمال | Persistent goal and completion audit | documented |  |
| `AGENT-44` | المتابعة الاستباقية المحدودة | Bounded proactive follow-up | documented |  |
| `AGENT-45` | غلاف نتيجة الأداة وتيار الأحداث | Tool result envelope and typed event stream | documented | chromium |
| `AGENT-46` | ذاكرة على مرحلتين بعقود إيجار | Two-phase memory with leased jobs | documented |  |
| `AGENT-47` | رسم حالة بنقاط حفظ واستئناف | Checkpointed state graph with resume and approval interrupts | documented |  |
| `AGENT-48` | فريق بأدوار ومهام ومخرج متوقع | Role-goal crew with expected outputs | documented |  |
| `AGENT-49` | خط إنتاج بإجراءات قياسية ووثائق تسليم | SOP assembly line with document handoffs | documented |  |
| `AGENT-51` | ذاكرة بطبقات يحررها الوكيل | Tiered self-editing memory | documented |  |
| `AGENT-52` | التقاط ملاحظات الجلسة وحقنها في التالية | Session observation capture and injection | documented |  |
| `AGENT-53` | وكيل يتصرف بالكود | Code-as-action agent | documented | python3 |
| `AGENT-54` | حواجز تفعيل وتسليم لمتخصص | Tripwire guardrails and specialist handoffs | documented |  |
| `AGENT-55` | تيار أحداث قابل لإعادة التشغيل | Replayable event-stream agent | documented |  |
| `SELF-01` | اعرف قبل أن تقول لا | Registry before no | documented | node, python3, claude:tools |
| `SELF-02` | سُلَّم حقيقة القدرة | Capability-truth ladder | documented | ffmpeg, key:unspecified |
| `SELF-03` | الإثبات له تاريخ صلاحية | Proofs are dated leases | documented | tesseract |
| `SELF-04` | التنفيذ ليس تحققًا | Executed is not verified | documented | ffmpeg, chromium, libreoffice |
| `SELF-16` | آداب البروكسي | Proxy etiquette | documented |  |
| `SELF-30` | أعد الاستخدام قبل البناء | Reuse before build matrix | documented |  |
| `SELF-31` | مستكشف المهارات | Skill scout ladder | documented |  |
| `SELF-34` | تدقيق سطح مساحة العمل | Workspace surface audit | documented | key:unspecified |
| `SELF-35` | استنتج سطحك | Infer your surface | documented | python3 |
| `SELF-37` | صندوق تنفيذ الكود في API | API code-execution sandbox | documented | ffmpeg, pip:numpy, pip:pillow, pip:scipy |
| `SELF-38` | تنفيذ الكود في تطبيقات claude.ai | claude.ai code execution and files | documented | node, pip:office |
| `SELF-39` | مزايا تطبيق سطح المكتب | Desktop app extras | documented | os:macos, claude:browser, key:unspecified |
| `SELF-40` | أداة موجودة = قوة مفتوحة | Tool present → power unlocked map | documented | node, git |
| `SELF-41` | بطاقة القدرة والإيصال | Capability card and receipts | documented | ffmpeg |
| `SELF-42` | تصنيف الأعطال وأصغر إصلاح | Failure taxonomy with smallest fix | documented | key:unspecified |
| `SELF-43` | بوابة المدفوع والأثر الجانبي | Paid and side-effect gate | documented | ffmpeg, pip:piper |
| `AGENT-34` | تثبيت حزمة ECC | Install ECC (Everything Claude Code) | install | node |
| `AGENT-36` | llama.cpp: تشغيل نموذج مفتوح صغير دون اتصال للتصنيف | llama.cpp: Run a small quantised open model offline for batch classification or embeddings | install | pip:llama-cpp |
| `AGENT-38` | MCP reference servers: ربط خوادم MCP المرجعية (ملفات، git، جلب | MCP reference servers: Wire reference MCP servers (filesystem, git, fetch, memory) into an agent as tools | install | npm:mcp-servers |
| `TOOL-39` | منفّذ المشهد داخل Blender | Blender-side scene builder | install | python3, blender |
| `TOOL-48` | باني فهرس البحث الإبداعي | Creative research catalog builder | install | python3, gh, npm:rea |
| `TOOL-49` | إعادة موازنة فهرس المستودعات الإبداعية | Rebalance creative repo catalog | install | python3, gh, npm:rea |
| `TOOL-51` | استوديو التنزيل Cinema C للآيفون | Cinema C iPhone downloader studio | install | ffmpeg, python3, yt-dlp |
| `TOOL-53` | تحليل REA لمستودعات المالك دفعةً واحدة | REA Owned-Repo Batch | install | python3, git, npm:rea |
| `TOOL-83` | قالب فيلم HTML Canvas | HTML Canvas film starter | install | ffmpeg, node, python3, chromium |
| `TOOL-84` | قالب فيلم Remotion | Remotion film starter | install | ffmpeg, python3, npm:remotion, npm:react |
| `TOOL-87` | رندر سينمائي بـBlender Cycles | Blender Cycles cinematic renders | install | ffmpeg, blender |
| `TOOL-90` | أداة عرض النص بخطوط مرشّحة | Font candidate text renderer | install | node, python3, chromium, fonts:arabic |
| `TOOL-94` | تنزيل الفيديو من الروابط للمونتاج | Video link downloader for montage | install | ffmpeg, python3, imagemagick, yt-dlp |
| `AGENT-17` | مهام مجدولة وروتينات | Scheduled tasks & routines | key | claude:tools, key:unspecified |
| `SELF-11` | الموصلات والمفاتيح | Connectors and keys | key | claude:tools, key:unspecified |
