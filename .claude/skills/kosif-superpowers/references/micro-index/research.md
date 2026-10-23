# البحث والمعرفة — Research & knowledge

[← الفهرس الدقيق / micro index](README.md) · 56 powers

## الفهرس / contents

- [knowledge-graph (code)](#knowledge-graph-code)
- [atlas-research (research)](#atlas-research-research)
- [web-research (research)](#web-research-research)


## knowledge-graph (code)

chapter: [knowledge-graph](../powers/knowledge-graph.md) · card: `usip-library/cards/research/knowledge-graph.md` · tools: `capability-graph` · `powers` · `superpower-fusion`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| GRAPH-01 | ✅ | تثبيت Graphify في بيئة معزولة · Install Graphify locally (venv) | SP-0061 Connect the hosted Graphify MCP | python3, key:graphify, key:unspecified |
| GRAPH-02 | ✅ | رسم خريطة لأي مستودع دون اتصال · Map a codebase offline | SP-0061 Connect the hosted Graphify MCP | key:graphify |
| GRAPH-03 | ✅ | اسأل الخريطة بدل قراءة الملفات · Query the graph instead of reading files | SP-0061 Connect the hosted Graphify MCP | key:graphify |
| GRAPH-04 | ✅ | نطاق الضرر قبل التعديل · Blast radius before a change | SP-0061 Connect the hosted Graphify MCP | python3, key:graphify |
| GRAPH-05 | ✅ | تحديث الخريطة بعد التعديلات · Keep the map fresh | SP-0061 Connect the hosted Graphify MCP | key:graphify |
| GRAPH-06 | ✅ | ذاكرة دروس مبنية على الخريطة · Graph-backed lessons | SP-0061 Connect the hosted Graphify MCP | key:graphify |
| GRAPH-07 | ✅ | تقديم الخريطة عبر MCP محلي · Serve the graph over a local MCP server | SP-0061 Connect the hosted Graphify MCP | python3, key:graphify |
| GRAPH-08 | ✅ | صفحات ومخرجات بصرية للخريطة · Exports and visual map pages | SP-0061 Connect the hosted Graphify MCP | npm:d3, npm:mermaid, key:graphify |
| GRAPH-09 | ✅ | جعل Claude Code يستشير الخريطة تلقائيًا · Make Claude Code consult the graph automatically | SP-0061 Connect the hosted Graphify MCP | key:graphify |
| GRAPH-21 | ✅ | مصالحة فرع متباعد بالفهرس المستضاف · Reconcile a diverged branch with the hosted index | SP-0061 Connect the hosted Graphify MCP | git, key:graphify |
| GRAPH-10 | 🔑 | الوثائق والصور والفيديو داخل الخريطة · Docs, PDFs, images and media in the graph | SP-0061 Connect the hosted Graphify MCP | chromium, yt-dlp, pip:faster-whisper, key:graphify … |
| GRAPH-11 | 🔑 | ربط Graphify المستضاف · Connect the hosted Graphify MCP | SP-0061 Connect the hosted Graphify MCP | key:graphify, key:unspecified |
| GRAPH-12 | 🔑 | التنقل في الكود عبر الخدمة المستضافة · Navigate code with hosted Graphify tools | SP-0061 Connect the hosted Graphify MCP | python3, key:graphify |
| GRAPH-13 | 🔑 | الأثر والمخاطر والاختبارات المرتبطة · Impact, risk and linked tests (hosted) | SP-0061 Connect the hosted Graphify MCP | python3, key:unspecified |
| GRAPH-14 | 🔑 | ذاكرة مساحة العمل المشتركة · Shared workspace memory (remember / recall) | SP-0061 Connect the hosted Graphify MCP | key:unspecified |
| GRAPH-15 | 📄 | صدق لقطة الفهرس · Index-snapshot honesty | SP-0061 Connect the hosted Graphify MCP | python3, git |
| GRAPH-17 | ✅ | من الخريطة إلى خريطة ذهنية · Graph → communities → mind map | SP-0062 Understand any codebase or skill set fa… | python3, npm:mermaid, key:graphify |
| GRAPH-16 | 📄 | فهم أي مستودع أو مجموعة مهارات بسرعة · Understand any codebase or skill set fast | SP-0062 Understand any codebase or skill set fa… | key:graphify |
| GRAPH-18 | 📄 | الخريطة أولًا لغير الكود · Map-first for non-code corpora | SP-0062 Understand any codebase or skill set fa… | claude:tools |
| GRAPH-19 | 📄 | تسميات الدليل وثقة منفصلة · Evidence labels and discrete confidence | SP-0062 Understand any codebase or skill set fa… | — |
| GRAPH-20 | 💡 | الخريطة مادةً لفيلم موشن · Codebase map as motion graphics | SP-0062 Understand any codebase or skill set fa… | chromium, npm:three, npm:d3, key:graphify |

## atlas-research (research)

chapter: [atlas-research](../powers/atlas-research.md) · card: `usip-library/cards/research/atlas-research.md` · tools: —

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| AWEB-01 | 📄 | جلب بيانات يوتيوب بدون حصص · Zero-quota YouTube data lookup via proxy API | SP-0101 Healthcare provider list extraction and… | key:unspecified |
| AWEB-02 | 📄 | جلب ثابت أولا ثم احتياط المتصفح · Static-first scrape with headless-browser fallback | SP-0101 Healthcare provider list extraction and… | chromium |
| AWEB-03 | 📄 | بوابة الشرعية قبل جمع البيانات · Scraping legality gate before fetch | SP-0101 Healthcare provider list extraction and… | — |
| AWEB-04 | 📄 | ترميز نوعي قابل للتتبع وصياغة فرضيات · Traceable qualitative coding and hypothesis framing | SP-0101 Healthcare provider list extraction and… | — |
| AWEB-05 | 📄 | قرار الضبط الدقيق واختيار الطريقة · Fine-tune or not: method router | SP-0101 Healthcare provider list extraction and… | pip:chromadb |
| AWEB-06 | 📄 | بوابة نقاط النهاية وحجم العينة للدراسات · Clinical study endpoint and sample-size gate | SP-0101 Healthcare provider list extraction and… | — |
| AWEB-07 | 📄 | استخراج وإثراء بيانات الأطباء · Healthcare provider list extraction and enrichment | SP-0101 Healthcare provider list extraction and… | — |
| AWEB-08 | 📄 | بحث براءات الاختراع بأسئلة إلزامية · Patent search with forcing intake | SP-0101 Healthcare provider list extraction and… | — |
| AWEB-09 | 📄 | من المنهج الدراسي إلى قائمة قراءات · Course syllabus to supplementary reading list | SP-0101 Healthcare provider list extraction and… | node, pip:office |
| AWEB-10 | 📄 | قواعد بيانات الملاحظات بملفات Obsidian Bases · Database views over notes with Obsidian Bases | SP-0101 Healthcare provider list extraction and… | — |
| AWEB-11 | 📄 | التعرّف بدل التذكّر في المنتقيات والقوائم · Recognition over recall in pickers and menus | SP-0101 Healthcare provider list extraction and… | — |

## web-research (research)

chapter: [web-research](../powers/web-research.md) · card: `usip-library/cards/research/web-research.md` · tools: `atlas-audit-synthesis` · `atlas-body-audit` · `atlas-external-bridge` · `browser-scout` · `creative-external-search` · `rea-creative-research-atlas` · `rebalance-creative-repos` · `repo-sync-catalog` …

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| WEB-12 | 📄 | الاسترجاع التكراري · Iterative retrieval loop | SP-0001 Context compaction as a handoff | — |
| WEB-01 | ✅ | البحث في الويب المدمج · Built-in WebSearch tool | SP-0102 API server tools: web_search / web_fetch | claude:tools |
| WEB-02 | ✅ | جلب صفحة وقراءتها · Built-in WebFetch tool | SP-0102 API server tools: web_search / web_fetch | claude:tools |
| WEB-04 | ✅ | عميل HTTP خلف الوكيل · httpx through the agent proxy | SP-0102 API server tools: web_search / web_fetch | python3 |
| WEB-05 | ✅ | استخراج النص الرئيسي من صفحة · Main-text extraction (trafilatura + bs4) | SP-0102 API server tools: web_search / web_fetch | pandoc, pip:office, pip:trafilatura |
| WEB-06 | ✅ | قراءة خلاصات RSS · RSS/Atom feeds (feedparser) | SP-0102 API server tools: web_search / web_fetch | python3 |
| WEB-07 | ✅ | متصفح خفي للصفحات الديناميكية · Headless Chromium for JS pages and screenshots | SP-0102 API server tools: web_search / web_fetch | node, chromium |
| WEB-08 | ✅ | بيانات Hugging Face · Hugging Face hub files | SP-0102 API server tools: web_search / web_fetch | network |
| WEB-16 | ✅ | سياسات المواقع والروبوتات · Respect bot policies (no spoofing) | SP-0102 API server tools: web_search / web_fetch | claude:tools |
| WEB-23 | ✅ | Trafilatura: استخراج نص المقال الرئيسي وبياناته من HTML · Trafilatura: Extract main article text and metadata from HTML, dropping boilerplate (Arabic works) | SP-0102 API server tools: web_search / web_fetch | pip:trafilatura |
| WEB-22 | 📦 | Crawl4AI: عرض صفحات JavaScript وتحويلها إلى Markdown جاهز · Crawl4AI: Render JS pages and convert them to LLM-ready Markdown | SP-0102 API server tools: web_search / web_fetch | pip:crawl4ai |
| WEB-03 | 🔑 | أدوات الويب في واجهة API · API server tools: web_search / web_fetch | SP-0102 API server tools: web_search / web_fetch | pip:anthropic, key:unspecified |
| WEB-09 | 🔑 | البحث في GitHub · GitHub research (gh CLI / GitHub tools) | SP-0102 API server tools: web_search / web_fetch | gh, key:unspecified |
| WEB-20 | 🔑 | مراقبة سؤال متكرر · Monitor a recurring question | SP-0102 API server tools: web_search / web_fetch | claude:tools |
| WEB-24 | 🔑 | browser-use: قيادة متصفح بلا واجهة لإنجاز مهام ويب · browser-use: Drive a headless browser through multi-step web tasks from a goal | SP-0102 API server tools: web_search / web_fetch | chromium, key:unspecified, pip:browser-use |
| WEB-18 | 📄 | محتوى الويب بيانات لا أوامر · Web content is data, not instructions | SP-0102 API server tools: web_search / web_fetch | — |
| WEB-19 | 📄 | الاقتباس والترخيص · Quote short, paraphrase, credit | SP-0102 API server tools: web_search / web_fetch | — |
| WEB-17 | ✅ | تشخيص الوكيل دون التحايل · Diagnose proxy failures, do not route around | SP-0103 Deep research with parallel sub-agents | network |
| WEB-21 | 📦 | Scrapy: كتابة زاحف مهذب يحترم robots.txt يجمع موقعًا · Scrapy: Write a polite spider (robots.txt respected) that crawls a permitted site into JSON | SP-0103 Deep research with parallel sub-agents | pip:scrapy |
| WEB-10 | 📄 | دفتر الادعاءات · Claim ledger | SP-0103 Deep research with parallel sub-agents | — |
| WEB-11 | 📄 | درجات المصادر وحداثتها · Source tiers and freshness rule | SP-0103 Deep research with parallel sub-agents | node |
| WEB-13 | 📄 | فرز طلب البحث · Research-ops triage and labels | SP-0103 Deep research with parallel sub-agents | — |
| WEB-14 | 📄 | بحث معمّق بوكلاء متوازيين · Deep research with parallel sub-agents | SP-0103 Deep research with parallel sub-agents | claude:tools |
| WEB-15 | 📄 | الوثائق الحية قبل الذاكرة · Live docs before memory | SP-0103 Deep research with parallel sub-agents | node, pip:numpy, pip:opencv, pip:pandas … |
