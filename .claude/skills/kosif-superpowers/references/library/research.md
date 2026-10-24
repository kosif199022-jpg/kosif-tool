# البحث والمعرفة — Research & knowledge (`research`)

> مكتبة بروتوكول USIP v5.6، مولّدة بـ `scripts/smart_capabilities.py library` من `data/powers/*.json` و`data/tools.json`؛ لا تُحرَّر يدويًا. الدليل: [A28 اختيار القدرات](../protocol/A28-capability-routing.md) · [الفهرس](INDEX.md) · [النواة](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

## الفهرس / contents

- [متى تستخدم هذه المجموعة / when](#متى-تستخدم-هذه-المجموعة--when)
- [الحالة بالأرقام / status](#الحالة-بالأرقام--status)
- [الأدوات القابلة للتشغيل / runnable tools](#الأدوات-القابلة-للتشغيل--runnable-tools)
- [العائلات / families](#العائلات--families)
- [كل القدرات / every power](#كل-القدرات--every-power)

## متى تستخدم هذه المجموعة / when

كلمات التوجيه: research web source citations evidence knowledge search بحث مصادر مراجع معرفة

لا خط عمل مسجّل لهذه المجموعة؛ ركّبه من الأدوات أدناه.

العضوية في المجموعة تصنيف للتوجيه، لا دليل على أن القدرات تعمل معًا: اربطها بخط عمل مختبر فقط.

## الحالة بالأرقام / status

| الحالة | العدد | المعنى |
|---|---:|---|
| `proven` | 21 | ✅ proven: a proof exists in the catalog; still check its requirements here before calling it ready |
| `documented` | 27 | 📄 documented: a described method; needs building or wiring before it runs |
| `install` | 2 | 📦 install: needs a package, binary or model first |
| `key` | 9 | 🔑 key: needs an account, key or paid service (ask before any spend) |
| `idea` | 1 | 💡 idea: not built |
| **المجموع** | **60** | |

## الأدوات القابلة للتشغيل / runnable tools

| الأداة | ما تفعله | ابدأ بـ | الدليل |
|---|---|---|---|
| `atlas-audit-synthesis` | تحويل مراجعة الأطلس إلى بيان مُراجَع | `python3 scripts/atlas_audit_synthesis.py --records ./out/atlas-audit-private/records.json --rea-dir ./out/rea --manifest-out ./out/manifest.json --report-out ./out/atlas-reviewed-audit.md` | untested |
| `atlas-body-audit` | مراجعة ساكنة لنصوص مهارات الأطلس | `python3 scripts/atlas_body_audit.py --index ./atlas-index.json --out ./out/atlas-audit-private --limit 200` | tested-here |
| `atlas-external-bridge` | بحث مهارات أطلس الخارجية | `python3 scripts/atlas_external_bridge.py stats --index ./atlas_index.json --copyleft-index ./atlas_copyleft_index.json` | tested-here |
| `browser-scout` | مستكشف المواقع بالمتصفح | `python3 scripts/browser_scout.py doctor` | tested-here |
| `capability-graph` | باني خريطة القدرات المترابطة | `python3 scripts/capability_graph.py build` | tested-here |
| `creative-external-search` | بحث المصادر الإبداعية دون اتصال | `python3 scripts/creative_external_search.py search "kinetic typography" --kind repo --top 5` | tested-here |
| `github-top-repos` | متابعة أشهر 1000 مستودع | `python3 scripts/github_top_repos.py build` | tested-here |
| `instagram-reference-discovery` | البحث عن مراجع فيديو إنستجرام وربطها بالمصفوفات اللانهائية | `python3 scripts/instagram_reference_bridge.py doctor` | tested-here |
| `powers` | البحث في كتالوج القدرات | `python3 scripts/powers.py stats --domain motion --json` | tested-here |
| `rea-creative-research-atlas` | باني فهرس البحث الإبداعي | `python3 scripts/rea_creative_research_atlas.py report` | tested-elsewhere |
| `rebalance-creative-repos` | إعادة موازنة فهرس المستودعات الإبداعية | `python3 scripts/rebalance_creative_repos.py run` | tested-elsewhere |
| `repo-sync-catalog` | مزامنة الكتالوج مع PromptsMotion | `python3 tools/sync_catalog.py` | untested |
| `source-scout` | مستكشف مصادر المجتمع | `python3 scripts/source_scout.py check` | tested-here |
| `sources-index` | فهرس المصادر: الذاكرة الفهرسية لمرفقات المستخدم داخل مجلد العمل | `python3 -I scripts/sources_index.py add charter.txt --dir ../../../out/demo` | tested-here |
| `superpower-fusion` | دمج القدرات في قدرات خارقة مترابطة | `python3 scripts/superpower_fusion.py build` | tested-here |

الأوامر نسبية إلى مجلد المهارة (أو جذر المستودع لأدوات `tools/`)؛ `python3 scripts/hub.py tool <id>` يعطي كل الأوامر والمتطلبات والحدود.

## العائلات / families

| العائلة | القدرات | الفصل |
|---|---:|---|
| `atlas-research` | 11 | [atlas-research.md](../powers/atlas-research.md) |
| `knowledge-graph` | 23 | [knowledge-graph.md](../powers/knowledge-graph.md) |
| `web-research` | 26 | [web-research.md](../powers/web-research.md) |

## كل القدرات / every power

مرتبة بالحالة ثم العائلة ثم المعرّف. `hub.py` و`skill_intelligence.py deep <ID>` يعطيان بطاقة القدرة كاملة بدليلها.

| المعرّف | الاسم | English | الحالة | المتطلبات |
|---|---|---|---|---|
| `GRAPH-01` | تثبيت Graphify في بيئة معزولة | Install Graphify locally (venv) | proven | python3, key:graphify |
| `GRAPH-02` | رسم خريطة لأي مستودع دون اتصال | Map a codebase offline | proven | key:graphify |
| `GRAPH-03` | اسأل الخريطة بدل قراءة الملفات | Query the graph instead of reading files | proven | key:graphify |
| `GRAPH-04` | نطاق الضرر قبل التعديل | Blast radius before a change | proven | python3, key:graphify |
| `GRAPH-05` | تحديث الخريطة بعد التعديلات | Keep the map fresh | proven | key:graphify |
| `GRAPH-06` | ذاكرة دروس مبنية على الخريطة | Graph-backed lessons | proven | key:graphify |
| `GRAPH-07` | تقديم الخريطة عبر MCP محلي | Serve the graph over a local MCP server | proven | python3, key:graphify |
| `GRAPH-08` | صفحات ومخرجات بصرية للخريطة | Exports and visual map pages | proven | npm:d3, npm:mermaid, key:graphify |
| `GRAPH-09` | جعل Claude Code يستشير الخريطة تلقائيًا | Make Claude Code consult the graph automatically | proven | key:graphify |
| `GRAPH-17` | من الخريطة إلى خريطة ذهنية | Graph → communities → mind map | proven | python3, npm:mermaid, key:graphify |
| `GRAPH-21` | مصالحة فرع متباعد بالفهرس المستضاف | Reconcile a diverged branch with the hosted index | proven | git, key:graphify |
| `WEB-01` | البحث في الويب المدمج | Built-in WebSearch tool | proven | claude:tools |
| `WEB-02` | جلب صفحة وقراءتها | Built-in WebFetch tool | proven | claude:tools |
| `WEB-04` | عميل HTTP خلف الوكيل | httpx through the agent proxy | proven | python3 |
| `WEB-05` | استخراج النص الرئيسي من صفحة | Main-text extraction (trafilatura + bs4) | proven | pandoc, pip:office, pip:trafilatura |
| `WEB-06` | قراءة خلاصات RSS | RSS/Atom feeds (feedparser) | proven | python3 |
| `WEB-07` | متصفح خفي للصفحات الديناميكية | Headless Chromium for JS pages and screenshots | proven | node, chromium |
| `WEB-08` | بيانات Hugging Face | Hugging Face hub files | proven | network |
| `WEB-16` | سياسات المواقع والروبوتات | Respect bot policies (no spoofing) | proven | claude:tools |
| `WEB-17` | تشخيص الوكيل دون التحايل | Diagnose proxy failures, do not route around | proven | network |
| `WEB-23` | Trafilatura: استخراج نص المقال الرئيسي وبياناته من HTML | Trafilatura: Extract main article text and metadata from HTML, dropping boilerplate (Arabic works) | proven | pip:trafilatura |
| `AWEB-01` | جلب بيانات يوتيوب بدون حصص | Zero-quota YouTube data lookup via proxy API | documented | key:unspecified |
| `AWEB-02` | جلب ثابت أولا ثم احتياط المتصفح | Static-first scrape with headless-browser fallback | documented | chromium |
| `AWEB-03` | بوابة الشرعية قبل جمع البيانات | Scraping legality gate before fetch | documented |  |
| `AWEB-04` | ترميز نوعي قابل للتتبع وصياغة فرضيات | Traceable qualitative coding and hypothesis framing | documented |  |
| `AWEB-05` | قرار الضبط الدقيق واختيار الطريقة | Fine-tune or not: method router | documented | pip:chromadb |
| `AWEB-06` | بوابة نقاط النهاية وحجم العينة للدراسات | Clinical study endpoint and sample-size gate | documented |  |
| `AWEB-07` | استخراج وإثراء بيانات الأطباء | Healthcare provider list extraction and enrichment | documented |  |
| `AWEB-08` | بحث براءات الاختراع بأسئلة إلزامية | Patent search with forcing intake | documented |  |
| `AWEB-09` | من المنهج الدراسي إلى قائمة قراءات | Course syllabus to supplementary reading list | documented | node, pip:office |
| `AWEB-10` | قواعد بيانات الملاحظات بملفات Obsidian Bases | Database views over notes with Obsidian Bases | documented |  |
| `AWEB-11` | التعرّف بدل التذكّر في المنتقيات والقوائم | Recognition over recall in pickers and menus | documented |  |
| `GRAPH-15` | صدق لقطة الفهرس | Index-snapshot honesty | documented | python3, git |
| `GRAPH-16` | فهم أي مستودع أو مجموعة مهارات بسرعة | Understand any codebase or skill set fast | documented | key:graphify |
| `GRAPH-18` | الخريطة أولًا لغير الكود | Map-first for non-code corpora | documented | claude:tools |
| `GRAPH-19` | تسميات الدليل وثقة منفصلة | Evidence labels and discrete confidence | documented |  |
| `GRAPH-22` | استرجاع بالرسم المعرفي وملخصات المجتمعات | Graph RAG with community summaries | documented | pip:chromadb |
| `GRAPH-23` | استرجاع بمستويين وتحديث تدريجي | Dual-level retrieval with incremental graph updates | documented | pip:chromadb |
| `WEB-10` | دفتر الادعاءات | Claim ledger | documented |  |
| `WEB-11` | درجات المصادر وحداثتها | Source tiers and freshness rule | documented | node |
| `WEB-12` | الاسترجاع التكراري | Iterative retrieval loop | documented |  |
| `WEB-13` | فرز طلب البحث | Research-ops triage and labels | documented |  |
| `WEB-14` | بحث معمّق بوكلاء متوازيين | Deep research with parallel sub-agents | documented | claude:tools |
| `WEB-15` | الوثائق الحية قبل الذاكرة | Live docs before memory | documented | node, pip:numpy, pip:opencv, pip:pandas |
| `WEB-18` | محتوى الويب بيانات لا أوامر | Web content is data, not instructions | documented |  |
| `WEB-19` | الاقتباس والترخيص | Quote short, paraphrase, credit | documented |  |
| `WEB-25` | بحث بوجهات نظر ثم مخطط ثم كتابة بمصادر | Perspective-guided research, outline, then cited writing | documented |  |
| `WEB-26` | مخطِّط وباحثون متوازيون ثم تقرير | Planner, parallel researchers, then report | documented |  |
| `WEB-21` | Scrapy: كتابة زاحف مهذب يحترم robots.txt يجمع موقعًا | Scrapy: Write a polite spider (robots.txt respected) that crawls a permitted site into JSON | install | pip:scrapy |
| `WEB-22` | Crawl4AI: عرض صفحات JavaScript وتحويلها إلى Markdown جاهز | Crawl4AI: Render JS pages and convert them to LLM-ready Markdown | install | pip:crawl4ai |
| `GRAPH-10` | الوثائق والصور والفيديو داخل الخريطة | Docs, PDFs, images and media in the graph | key | chromium, yt-dlp, pip:faster-whisper, key:graphify |
| `GRAPH-11` | ربط Graphify المستضاف | Connect the hosted Graphify MCP | key | key:graphify |
| `GRAPH-12` | التنقل في الكود عبر الخدمة المستضافة | Navigate code with hosted Graphify tools | key | python3, key:graphify |
| `GRAPH-13` | الأثر والمخاطر والاختبارات المرتبطة | Impact, risk and linked tests (hosted) | key | python3, key:graphify |
| `GRAPH-14` | ذاكرة مساحة العمل المشتركة | Shared workspace memory (remember / recall) | key | key:graphify |
| `WEB-03` | أدوات الويب في واجهة API | API server tools: web_search / web_fetch | key | pip:anthropic, key:unspecified |
| `WEB-09` | البحث في GitHub | GitHub research (gh CLI / GitHub tools) | key | gh, key:unspecified |
| `WEB-20` | مراقبة سؤال متكرر | Monitor a recurring question | key | claude:tools |
| `WEB-24` | browser-use: قيادة متصفح بلا واجهة لإنجاز مهام ويب | browser-use: Drive a headless browser through multi-step web tasks from a goal | key | chromium, key:unspecified, pip:browser-use |
| `GRAPH-20` | الخريطة مادةً لفيلم موشن | Codebase map as motion graphics | idea | chromium, npm:three, npm:d3, key:graphify |
