# الوكلاء والتوجيه الذكي — Agents & routing (`agents`)

> مكتبة بروتوكول USIP v5.5، مولّدة بـ `scripts/smart_capabilities.py library` من `data/powers/*.json` و`data/tools.json`؛ لا تُحرَّر يدويًا. الدليل: [A28 اختيار القدرات](../protocol/A28-capability-routing.md) · [الفهرس](INDEX.md) · [النواة](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

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
| `proven` | 83 | ✅ proven: a proof exists in the catalog; still check its requirements here before calling it ready |
| `ready` | 5 | 🟢 ready: runnable without setup according to the catalog |
| `documented` | 49 | 📄 documented: a described method; needs building or wiring before it runs |
| `install` | 8 | 📦 install: needs a package, binary or model first |
| `key` | 2 | 🔑 key: needs an account, key or paid service (ask before any spend) |
| **المجموع** | **147** | |

## الأدوات القابلة للتشغيل / runnable tools

| الأداة | ما تفعله | ابدأ بـ | الدليل |
|---|---|---|---|
| `ai-tool-discovery` | باحث القدرات ثنائي اللغة بلا اتصال | `python3 scripts/ai_tool_discovery.py "تحريك شخصيات فيديو" --top 8` | tested-here |
| `atlas-5000` | خريطة تغطية أطلس الـ5000 مهارة | `python3 scripts/atlas_5000.py stats --json` | tested-here |
| `boot` | إحاطة بدء الجلسة | `python3 scripts/boot.py` | tested-here |
| `build-chapters` | مولّد فصول العائلات | `python3 scripts/build_chapters.py` | untested |
| `business-workflows` | الذكاء الاصطناعي في الأعمال: 9 وظائف و64 خطة عمل بخطط تشغيل لClaude | `python3 scripts/business_workflows.py functions` | tested-here |
| `capability-atlas` | أطلس القدرات للبحث والتخطيط | `python3 scripts/capability_atlas.py stats --json` | tested-here |
| `capability-graph` | باني خريطة القدرات المترابطة | `python3 scripts/capability_graph.py build` | tested-here |
| `capability-runtime-router` | موجّه القدرات التنفيذية | `python3 scripts/capability_runtime_router.py --task "حلل فيديو مرجعي وأنتج مونتاج مشابه بأصولي" --limit 5 --json` | tested-here |
| `catalog-evidence-audit` | تدقيق أدلة الكتالوج | `python3 scripts/catalog_evidence_audit.py` | tested-elsewhere |
| `charter-ingest` | إدخال قائمة الميثاق: مجلس الخبراء 500 فهرسًا للاستشارة | `python3 scripts/charter_ingest.py roster.txt --out data/experts_500.json` | tested-here |
| `check-skill` | فحص سلامة المهارة | `python3 scripts/check_skill.py` | untested |
| `council` | مجلس البرو: خمسة أعضاء متعارضين وثلاث جولات وحكم بالدرجات | `python3 scripts/council.py plan "اعمل ريلز دعاء" --dir out/demo/council --options A,B,C` | tested-here |
| `fusionforge` | FusionForge v2 لوصفات الـWorkflow المركبة داخل المشروع | `python3 scripts/fusionforge.py propose "مونتاج ريلز بترجمة عربية" --project demo_project --from-brief out/20261021-reel/brief.json` | tested-here |
| `fusionforge-shared` | ذاكرة FusionForge المشتركة بوصفات مهارات معزولة | `python3 scripts/fusionforge_shared.py audit` | untested |
| `hub` | بوابة KOSIF الموحّدة | `python3 scripts/hub.py find "اعمل فيديو موشن عربي متزامن مع صوتي"` | tested-here |
| `kosif-groups` | خريطة المجموعات مع القدرات الخارقة والسكربتات وخطط التثبيت | `python3 scripts/kosif_hubs.py` | tested-here |
| `kosif-mcp` | خادم MCP لكتالوج KOSIF | `python3 scripts/kosif_mcp.py` | tested-here |
| `kosif-remote-commander` | خادم KOSIF Remote Commander | `python3 scripts/kosif_remote_superpowers.py doctor` | tested-here |
| `local-first` | مدخل محلي بلا استنساخ | `python3 scripts/local_first.py doctor` | tested-here |
| `owned-repos` | خريطة مستودعات المالك وخريطة المهارات | `python3 scripts/owned_repos.py find "رسم شخصيات"` | tested-here |
| `powers` | البحث في كتالوج القدرات | `python3 scripts/powers.py stats --domain motion --json` | tested-here |
| `probe-env` | فحص قدرات الجهاز | `python3 scripts/probe_env.py` | tested-elsewhere |
| `python-package-probe` | فاحص وجود حزم بايثون | `python3 scripts/python_package_probe.py pandas numpy httpx` | tested-here |
| `rea-bridge` | جسر أوامر REA | `python3 scripts/rea_bridge.py doctor` | tested-here |
| `rea-family-router` | موجّه عائلات REA | `python3 scripts/rea_family_router.py list` | tested-here |
| `relabel-proofs` | إعادة تصنيف نطاق الأدلة | `python3 scripts/relabel_proofs.py` | untested |
| `repo-build` | مولّد ملفات أطلس الأساليب | `python3 tools/build.py` | untested |
| `requirements` | مخطط متطلبات القدرات | `python3 scripts/requirements.py present --json` | tested-here |
| `see-pro-cognitive-gate` | فاحص عقود التفكير والتوليف KOSIF SEE Pro | `python3 scripts/see_pro_cognitive_gate.py --self-test` | tested-here |
| `skill-intelligence` | محرك بروتوكول ذكاء المهارات الشامل | `python3 scripts/skill_intelligence.py brief "مونتاج ريلز على الإيقاع بترجمة عربية"` | tested-here |
| `skill-layout` | خريطة ترتيب المهارة | `python3 scripts/skill_layout.py build` | tested-here |
| `smart-capabilities` | فهرس ذكي للقدرات من أجل Claude | `python3 scripts/smart_capabilities.py groups` | tested-here |
| `superpower-fusion` | دمج القدرات في قدرات خارقة مترابطة | `python3 scripts/superpower_fusion.py build` | tested-here |
| `superpowers` | خريطة المستودعات الخارجية | `python3 scripts/superpowers.py list --capability voice --json` | tested-here |
| `superpowers-unified` | موجّه مهارات العمل ومثبّتها | `python3 scripts/superpowers_unified.py doctor` | tested-here |

الأوامر نسبية إلى مجلد المهارة (أو جذر المستودع لأدوات `tools/`)؛ `python3 scripts/hub.py tool <id>` يعطي كل الأوامر والمتطلبات والحدود.

## العائلات / families

| العائلة | القدرات | الفصل |
|---|---:|---|
| `agent-orchestration` | 38 | [agent-orchestration.md](../powers/agent-orchestration.md) |
| `runnable-tools` | 66 | [runnable-tools.md](../powers/runnable-tools.md) |
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
| `TOOL-11` | مختبر الابتكار الهندسي | Invention Lab Candidates | proven | pip:hypothesis |
| `TOOL-12` | جسر الصوت إلى لوحة القصة | Audio-to-Storyboard Bridge | proven | python3 |
| `TOOL-13` | مُصرِّف حركة SVG المتزامنة مع الصوت | Audio-timed SVG motion compiler | proven | ffmpeg, node, python3, chromium |
| `TOOL-14` | محرك حركة SVG | SVG motion engine runtime | proven | ffmpeg, node, python3, chromium |
| `TOOL-15` | جسر توقيتات Motion Starter Kit | Motion Starter Kit timing bridge | proven | python3 |
| `TOOL-16` | إنشاء فيلم سبورة مرسوم وتصييره | Doodle film runtime and renderer | proven | ffmpeg, node, python3, chromium |
| `TOOL-17` | مولّد مشاريع بداية لمحركات الحركة | Third-party motion engine scaffolder | proven | python3, npm:three, npm:gsap, npm:remotion |
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
| `TOOL-33` | تدقيق أدلة الكتالوج | Catalog Evidence Audit | ready | python3 |
| `TOOL-56` | فحص سلامة المهارة | Skill Health Check | ready | python3 |
| `TOOL-58` | إعادة تصنيف نطاق الأدلة | Proof Scope Relabeler | ready | python3 |
| `TOOL-59` | استيراد الملفات الإبداعية | Creative brief importer | ready | python3 |
| `TOOL-60` | مزامنة الكتالوج مع PromptsMotion | PromptsMotion catalog sync | ready | python3 |
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
| `AGENT-17` | مهام مجدولة وروتينات | Scheduled tasks & routines | key | claude:tools, key:unspecified |
| `SELF-11` | الموصلات والمفاتيح | Connectors and keys | key | claude:tools, key:unspecified |
