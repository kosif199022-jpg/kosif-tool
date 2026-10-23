# المستندات والكتابة — Documents & writing (`documents`)

> مكتبة بروتوكول USIP v5.5، مولّدة بـ `scripts/smart_capabilities.py library` من `data/powers/*.json` و`data/tools.json`؛ لا تُحرَّر يدويًا. الدليل: [A28 اختيار القدرات](../protocol/A28-capability-routing.md) · [الفهرس](INDEX.md) · [النواة](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

## الفهرس / contents

- [متى تستخدم هذه المجموعة / when](#متى-تستخدم-هذه-المجموعة--when)
- [الحالة بالأرقام / status](#الحالة-بالأرقام--status)
- [الأدوات القابلة للتشغيل / runnable tools](#الأدوات-القابلة-للتشغيل--runnable-tools)
- [العائلات / families](#العائلات--families)
- [كل القدرات / every power](#كل-القدرات--every-power)

## متى تستخدم هذه المجموعة / when

كلمات التوجيه: document pdf word excel office writing report مستند تقرير كتابة وورد

لا خط عمل مسجّل لهذه المجموعة؛ ركّبه من الأدوات أدناه.

العضوية في المجموعة تصنيف للتوجيه، لا دليل على أن القدرات تعمل معًا: اربطها بخط عمل مختبر فقط.

## الحالة بالأرقام / status

| الحالة | العدد | المعنى |
|---|---:|---|
| `proven` | 32 | ✅ proven: a proof exists in the catalog; still check its requirements here before calling it ready |
| `documented` | 99 | 📄 documented: a described method; needs building or wiring before it runs |
| `install` | 8 | 📦 install: needs a package, binary or model first |
| `key` | 4 | 🔑 key: needs an account, key or paid service (ask before any spend) |
| **المجموع** | **143** | |

## الأدوات القابلة للتشغيل / runnable tools

| الأداة | ما تفعله | ابدأ بـ | الدليل |
|---|---|---|---|
| `anchor-gate` | بوابة حفظ الحقائق عند إعادة الصياغة | `python3 scripts/anchor_gate.py --before proofs/general-writing/pairs/en_before.txt --after proofs/general-writing/pairs/en_after_drift.txt --text` | tested-here |
| `tell-scan` | فاحص العبارات الكتابية النمطية | `python3 scripts/tell_scan.py proofs/general-writing/samples/en_ai.txt` | tested-here |

الأوامر نسبية إلى مجلد المهارة (أو جذر المستودع لأدوات `tools/`)؛ `python3 scripts/hub.py tool <id>` يعطي كل الأوامر والمتطلبات والحدود.

## العائلات / families

| العائلة | القدرات | الفصل |
|---|---:|---|
| `atlas-craft` | 26 | [atlas-craft.md](../powers/atlas-craft.md) |
| `atlas-docs` | 55 | [atlas-docs.md](../powers/atlas-docs.md) |
| `documents-office` | 34 | [documents-office.md](../powers/documents-office.md) |
| `writing-humanizer` | 28 | [writing-humanizer.md](../powers/writing-humanizer.md) |

## كل القدرات / every power

مرتبة بالحالة ثم العائلة ثم المعرّف. `hub.py` و`skill_intelligence.py deep <ID>` يعطيان بطاقة القدرة كاملة بدليلها.

| المعرّف | الاسم | English | الحالة | المتطلبات |
|---|---|---|---|---|
| `DOC-01` | مستند Word عربي من اليمين | RTL Arabic DOCX with python-docx | proven | pip:office, fonts:arabic |
| `DOC-02` | جدول Excel عربي بمعادلات ورسم | Arabic XLSX with formulas and a native chart | proven | pip:office |
| `DOC-03` | إعادة حساب معادلات Excel بـ LibreOffice | Recalculate XLSX formulas headless | proven | chromium, libreoffice, pip:office |
| `DOC-04` | عرض PowerPoint عربي برسم أصلي | RTL Arabic PPTX with a native chart | proven | pip:office, fonts:arabic |
| `DOC-05` | PDF عربي من HTML وCSS | Arabic PDF from HTML/CSS (weasyprint) | proven | python3, fonts:arabic |
| `DOC-06` | PDF من المتصفح الخفي | HTML to PDF with headless Chromium | proven | node, chromium, fonts:arabic |
| `DOC-07` | PDF برمجي بـ reportlab | Programmatic PDF with reportlab (shape Arabic yourself) | proven | pip:office, fonts:arabic, pip:arabic-reshaper |
| `DOC-08` | مكتبات JavaScript للمستندات | JS document libraries (docx, pptxgenjs, exceljs, pdf-lib) | proven | node, pip:office |
| `DOC-09` | تحويل Office إلى PDF دفعة واحدة | Batch Office to PDF with LibreOffice | proven | chromium, libreoffice, pip:office |
| `DOC-10` | خطوط خاصة لـ LibreOffice دون تثبيت | Private fontconfig for LibreOffice and pango | proven | libreoffice, fonts:arabic |
| `DOC-11` | ملاءمة الورقة عند تحويل Excel | Fit-to-page before XLSX to PDF | proven | libreoffice, pip:office |
| `DOC-12` | Markdown ↔ Word بـ pandoc | Markdown <-> DOCX with pandoc (RTL) | proven | pandoc, pip:office |
| `DOC-13` | دمج وتدوير وتشفير PDF | Merge, rotate and encrypt PDFs (pypdf) | proven | pip:office |
| `DOC-14` | استخراج النص العربي من PDF بالطريقة الصحيحة | Extract Arabic from PDFs correctly | proven | pip:office |
| `DOC-15` | انتبه لربطة لا عند الاستخراج | Lam-alef ligature extraction artefact | proven | chromium, pip:office |
| `DOC-16` | تحويل أي مستند إلى Markdown | Any office file to Markdown (markitdown) | proven | pip:office |
| `DOC-17` | OCR لصفحات PDF الممسوحة | OCR for scanned PDF pages | proven | python3, tesseract |
| `DOC-18` | تصيير صفحات PDF للمراجعة البصرية | Render PDF pages to PNG for visual QA | proven | pip:pillow |
| `DOC-19` | pymupdf للنص والتصيير السريع | pymupdf fast text and render (AGPL) | proven | python3 |
| `DOC-22` | اتجاه النص المختلط في المستندات | Mixed-direction text hygiene | proven | pip:office |
| `DOC-23` | من يشكّل العربية بنفسه ومن يحتاج تشكيلًا يدويًا | Which engines need manual Arabic shaping | proven | chromium, libreoffice, pip:pillow, pip:matplotlib |
| `WRITE-02` | فحص علامات الكتابة الآلية في الإنجليزية | English tell scan (H1–H25 + X1) | proven | python3 |
| `WRITE-03` | فحص علامات الكتابة الآلية في الفصحى والمصرية | Arabic MSA and Egyptian tell scan (AR1–AR26) | proven | python3 |
| `WRITE-04` | سُلَّم الحكم بحسب قوة الدليل | Evidence-weighted verdict ladder | proven |  |
| `WRITE-05` | فحص Markdown دون لمس الكود والروابط والاقتباسات | Code-, URL- and quote-safe scanning | proven |  |
| `WRITE-07` | قفل الحقائق: بوابة المراسي | Fact lock: anchor gate | proven | python3 |
| `WRITE-08` | قفل الأسماء والعلامات التجارية | Names and brands lock | proven |  |
| `WRITE-09` | قفل الاقتباس المباشر | Direct-quote lock | proven | python3 |
| `WRITE-15` | تنظيف بقايا الأدوات والقوالب الفارغة | Tool-artifact and placeholder cleanup | proven | key:openai |
| `WRITE-18` | قاعدة الشرطة الطويلة | Dash rule on output | proven |  |
| `WRITE-20` | علامات الطباعة العربية | Arabic typography tells | proven |  |
| `WRITE-26` | مجموعة اختبارات انحدار للكتابة | Writing regression suite | proven | python3 |
| `ACRAFT-01` | مخطط أولي ومنظمات بصرية ملائمة | Low-fi wireframe and ADHD-friendly visual organizers | documented | npm:mermaid |
| `ACRAFT-02` | نظام ألوان يدعم الوصولية والوضع الداكن | Color system with accessibility and dark mode | documented |  |
| `ACRAFT-03` | اختبار تحمل الواجهة للمحتوى المتطرف | Content-stress and edge-case UI hardening | documented |  |
| `ACRAFT-04` | تخطيط جشتالت: الشبكة والمحاذاة والتجميع | Gestalt layout: grid, alignment, grouping | documented |  |
| `ACRAFT-05` | تدقيق التسلسل البصري والمسافات | Refactoring-UI hierarchy and spacing audit | documented |  |
| `ACRAFT-06` | تدقيق الضجيج البصري وإزالة الزخرفة | Signal-to-noise decoration audit | documented |  |
| `ACRAFT-07` | قواعد الخط والمقروئية للويب | Typography and legibility rules for web | documented |  |
| `ACRAFT-08` | بطاقة إخبارية مرسومة بأسلوب ثابت (موجّه صورة + SVG قابل للتعديل) | Fixed-style doodle card-news: image prompt plus editable SVG twin | documented | fonts:arabic |
| `ACRAFT-09` | صفحات ويبتون بشخصية ثابتة وألوان باستيل | Webtoon / essay-toon pages with a locked character sheet | documented |  |
| `ACRAFT-10` | قصة مصورة وثائقية: مقابلة أولاً وجملة شخصية تُنسخ حرفياً | Documentary story scenes: interview first, verbatim CHARACTER sentence | documented |  |
| `ACRAFT-11` | رسم توضيحي للكتب بقوالب تخطيط ثابتة ونص محدد حرفياً | Book and sketchbook-card illustration with fixed layout templates | documented |  |
| `ACRAFT-12` | مشهد قلم رصاص هادئ بلون واحد | Quiet pencil scene with a single colour accent | documented |  |
| `ACRAFT-13` | رسومات مدونة سفر: مصغّرة وخريطة مسار ومشهد | Travel-blog illustration kit: thumbnail, route sketch, scene | documented |  |
| `ACRAFT-14` | نظام بصري للكتاب: دليل فني ورسوم بالكود وحلقة رفض | Book visual system: art bible, code-rendered figures, art-director loop | documented | graphviz, pip:matplotlib, npm:mermaid |
| `ACRAFT-15` | تصميم الأيقونات بالتشابه والإغلاق البصري | Icon design by resemblance and Gestalt closure | documented |  |
| `ACRAFT-16` | نظام ألوان دلالي: درجات الحالة ودور واحد لكل لون | Semantic colour system: status ramps, one role per colour | documented |  |
| `ACRAFT-17` | مقاييس الوضوح والقراءة: التباين والتباعد وطول السطر | Legibility and readability numbers: contrast, spacing, measure | documented | npm:axe |
| `ACRAFT-18` | التدرج الطباعي بسلم مقاسات | Typographic hierarchy from a modular type scale | documented |  |
| `ACRAFT-19` | الأنماط الأصلية للعلامة والشخصية والتميمة | Brand archetypes for voice, mascot and character design | documented |  |
| `ACRAFT-20` | رسم أيقونة التطبيق بالكود | App icon drawn in code as flat layers | documented |  |
| `ACRAFT-21` | تصميم واجهة غير قالبي وملف DESIGN.md | Anti-template interface design and a DESIGN.md north star | documented |  |
| `ACRAFT-22` | التفاعلات الدقيقة: المحفّز والقواعد والاستجابة والحلقات | Microinteractions: trigger, rules, feedback, loops and modes | documented |  |
| `ACRAFT-23` | شرح بصري بصيغة واحدة مناسبة للسؤال | Visual explanation: one format chosen by the question | documented | npm:mermaid |
| `ACRAFT-24` | الإفصاح التدريجي للمعلومات والأدوات | Progressive disclosure of information and controls | documented |  |
| `ACRAFT-25` | حوكمة البرومبتات في الإنتاج: سجل وتقييمات وترقية وتراجع | Prompt governance: registry, evals, promotion and rollback | documented |  |
| `ACRAFT-26` | استخراج أسلوب كاتب إلى دليل أسلوب قابل للتطبيق | Extract a writing style into a reusable style guide | documented |  |
| `ADOCS-01` | كتابة AGENTS.md وCLAUDE.md جاهزة للوكلاء | Agent-ready AGENTS.md and CLAUDE.md authoring | documented |  |
| `ADOCS-02` | تدقيق CLAUDE.md وAGENTS.md وتخفيف السياق | Audit CLAUDE.md and AGENTS.md for context diet | documented | claude:tools |
| `ADOCS-03` | مزامنة ذاكرة التعليمات دون تضخم مع تحقق مستقل | Non-growth instruction-memory sync with independent verify | documented |  |
| `ADOCS-04` | إعداد تقرير TPAR للمقاولين في أستراليا | Australian TPAR contractor report prep | documented |  |
| `ADOCS-05` | تجميع حزمة الإقفال المالي الشهري للعميل | Month-end client financial pack assembly | documented | pip:office |
| `ADOCS-06` | توليد العقود والاتفاقيات | Contract and agreement generation | documented |  |
| `ADOCS-07` | مراجعة مخاطر العقود واتفاقيات السرية | Contract and NDA risk review with redline | documented | pip:office |
| `ADOCS-08` | مراجعة العقود بدليل بنود ومستويات مخاطر | Contract review with clause playbook and tiers | documented | pip:office |
| `ADOCS-09` | الرد على طلبات العروض والمشتريات العامة | RFP and public procurement response | documented |  |
| `ADOCS-10` | سجل المخاطر والحوكمة والامتثال | Risk register and compliance governance | documented |  |
| `ADOCS-11` | مخطط علاقات الكيانات من ملفات المخطط | Offline ER diagram from schema declarations | documented | npm:mermaid |
| `ADOCS-12` | مراجعة ما بعد الحادث بلا لوم | Blameless postmortem with timeline and action items | documented |  |
| `ADOCS-13` | حزمة تشخيص مُنقّحة وآمنة للدعم | Secret-safe redacted diagnostic bundle for support | documented |  |
| `ADOCS-14` | جاهزية الموقع لـ llms.txt وزواحف AI | llms.txt and AI-crawler readiness | documented |  |
| `ADOCS-15` | تصنيف MDR الأوروبي والملف الفني | EU MDR classification and technical file | documented |  |
| `ADOCS-16` | شجرة اختيار مسار FDA للأجهزة الطبية | FDA device pathway selection decision tree | documented |  |
| `ADOCS-17` | مخطط AWS بصيغة draw.io بأيقونات رسمية | AWS architecture draw.io with official icons | documented | npm:mermaid |
| `ADOCS-18` | اختيار محرك المخططات: PlantUML أو D2 أو Structurizr | Diagram-as-code engine choice: PlantUML, D2, Structurizr | documented | plantuml |
| `ADOCS-19` | مخطط معماري مبني على الريبو الفعلي | Evidence-grounded architecture diagram from repo | documented | docker, npm:mermaid |
| `ADOCS-20` | رسم Excalidraw يحمل حجة بصرية | Excalidraw diagram that argues visually | documented |  |
| `ADOCS-21` | رسم مخططات Mermaid والتحقق منها | Mermaid diagram render and validate loop | documented | npm:mermaid |
| `ADOCS-22` | تخطيط الرسوم العقدية وتصميم UML | Node-link layout and UML diagram design | documented |  |
| `ADOCS-23` | مخطط HTML مستقل بـ SVG مضمن | Self-contained HTML diagram with inline SVG | documented |  |
| `ADOCS-24` | خطة تنفيذ مرئية للمراجعة في المتصفح | Visual implementation plan reviewed in browser | documented | npm:mermaid |
| `ADOCS-25` | إنشاء ADR وRFC مع ترقيم وربط | ADR/RFC/PRD creation with ID linking | documented |  |
| `ADOCS-26` | تحديث التوثيق بالاعتماد على الكود | Code-grounded doc update and overhaul | documented | git, npm:mermaid |
| `ADOCS-27` | إعادة هيكلة التوثيق بإطار دياتاكسيس | Diataxis four-kind docs restructuring | documented |  |
| `ADOCS-28` | تدقيق انحراف التوثيق عن الكود | Docs drift audit against current code | documented | git |
| `ADOCS-29` | توثيق الدروس المستفادة من المشكلات المحلولة | Durable solved-problem learning notes | documented | claude:tools |
| `ADOCS-30` | ويكي مترابط تديره النماذج | LLM-maintained interlinked wiki | documented |  |
| `ADOCS-31` | البحث في توثيق المكتبات بالإصدار الصحيح | Look up version-correct library docs | documented |  |
| `ADOCS-32` | ضغط الماركداون دون فقدان المعنى | Lossless markdown compression with semantic-diff gate | documented |  |
| `ADOCS-33` | كتابة README والتحقق منه | README authoring and verification | documented |  |
| `ADOCS-34` | إزالة التعليقات الزائدة في الكود | Strip AI-slop and zero-info code comments | documented |  |
| `ADOCS-35` | كتابة سرد الألعاب المتفرع | Game narrative and branching writing | documented |  |
| `ADOCS-36` | اختيار رقم الإصدار وكتابة سجل التغييرات | Semver bump and changelog plan | documented | git |
| `ADOCS-37` | كتابة الرياضيات وشرحها المطوّل | Math notation and long-form exposition | documented |  |
| `ADOCS-38` | تقرير اختبار فهم بعد التغيير | Post-change comprehension quiz report | documented |  |
| `ADOCS-39` | هيكل منهج ذاتي مع سجل تقييم | Self-study curriculum scaffold with assessment log | documented | python3 |
| `ADOCS-40` | مقال تعليمي من جلسة عمل | Teaching-block article from a working session | documented |  |
| `ADOCS-41` | شرح بصري مبسط جداً بأسلوب طفل | Zero-knowledge visual ELI5 explainer | documented |  |
| `ADOCS-42` | الكتابة البسيطة: كلمات يومية وجمل كاملة | Plain writing: everyday words, complete sentences | documented |  |
| `ADOCS-43` | أنسنة النص بالكثافة لا بقائمة حذف | Humanize by density, with an over-correction guard | documented |  |
| `ADOCS-44` | تدقيق انحراف التوثيق عن الكود لكل بُعد | Per-dimension documentation drift audit | documented |  |
| `ADOCS-45` | الترجمة الإبداعية: متى نترجم ومتى نعيد الصياغة | Transcreation routing for marketing translation | documented |  |
| `ADOCS-46` | دمج بيانات JSON في قوالب Word وExcel وPowerPoint | JSON-to-document templating (DOCX/XLSX/PPTX/PDF) | documented | pip:office |
| `ADOCS-47` | تنقيح المستندات حقًا وإثبات ما سُلِّم ببصمات sha256 | True redaction and a sha256 delivery manifest | documented | tesseract |
| `ADOCS-48` | عروض تقديمية للمطورين بـ Slidev من Markdown | Developer slide decks in Markdown with Slidev | documented | chromium, latex, pip:office, npm:mermaid |
| `ADOCS-49` | كتابة README يجذب المطور في ثلاث ثوانٍ ويشغله في دقيقة | README that hooks in 3 seconds and runs in 60 | documented | npm:mermaid |
| `ADOCS-50` | تعليقات الكود الملائمة: معلومة لا يحملها الكود | Appropriate code comments: information the code cannot carry | documented |  |
| `ADOCS-51` | جولات CodeTour في الكود موجّهة لشخصية القارئ | Persona-targeted CodeTour walkthroughs with verified anchors | documented |  |
| `ADOCS-52` | تدقيق نصوص التعليمات الموجهة للنموذج: نواهٍ تلفت الانتباه وأمثلة تقيّد | LLM-facing prose audit: priming prohibitions and anchoring examples | documented |  |
| `ADOCS-53` | مخطط كتاب بمواصفة لكل فصل و'كتاب مرجعي' يحفظ الاتساق | Book outline with per-chapter specs and a series bible | documented |  |
| `ADOCS-54` | بناء ونشر كتاب: EPUB وPDF عبر Pandoc مع epubcheck وبيانات النشر | Book publishing build: EPUB/PDF via Pandoc, epubcheck and metadata | documented | pandoc |
| `ADOCS-55` | نشر مجموعة رقمية بعد بوابتي الحقوق والحساسية الثقافية | Publish a digital collection through rights and cultural-sensitivity gates | documented |  |
| `DOC-24` | مراجعة المستند قبل التسليم | Document delivery gate | documented |  |
| `WRITE-01` | سؤال واحد لكل جملة: هل تضيف جديدًا للقارئ؟ | One-question causal model for every sentence | documented |  |
| `WRITE-06` | إعادة الصياغة في أربع خطوات | Four-step rewrite: mark, draft, check, final | documented | python3 |
| `WRITE-10` | مطابقة صوت الكاتب من عينة | Voice matching from the writer's sample | documented |  |
| `WRITE-11` | الصوت حسب نوع النص بلا عينة | Genre voice without a sample | documented |  |
| `WRITE-12` | أوضاع الإخراج الثلاثة | Three output modes: pasted, file, embedded | documented |  |
| `WRITE-13` | الرد بالقرار أولًا | Reply-first rewrite (wrong-reader pattern) | documented |  |
| `WRITE-14` | تحرير Claude لردوده هو | Self-edit of Claude's own answers | documented | python3 |
| `WRITE-16` | متى لا تتدخل | When not to act | documented |  |
| `WRITE-17` | الحفاظ على تفاصيل الصوت البشري | Keep voice-carrying details | documented |  |
| `WRITE-19` | تبديل السجل: فصحى رسمية أو مبسطة أو مصرية | Register switch with facts locked | documented | python3, key:unspecified |
| `WRITE-21` | العادات البنيوية في النص العربي الآلي | Arabic paragraph-scale habits | documented |  |
| `WRITE-22` | نصوص الشاشة والتعليق الصوتي في الموشن | Captions and voiceover scripts in motion work | documented |  |
| `WRITE-23` | استثناءات المال والقانون والتدقيق | Finance, legal and audit exception | documented | python3 |
| `WRITE-24` | الأمانة: وضوح وصوت لا خداع | Honesty guard: clarity and voice, never authorship deception | documented |  |
| `WRITE-25` | لا اختراع: اسأل بدل أن تملأ الفراغ | No-invention rule | documented |  |
| `WRITE-27` | أسلوب اللغة الواضحة للتوثيق | Plain-language house style for docs | documented |  |
| `WRITE-28` | اختبارات التوجيه للتحسين اللغوي | Routing evals for the humanizer | documented |  |
| `DOC-20` | جداول PDF بالمواقع (LTR) | PDF tables with positions (pdfplumber) | install | pip:office |
| `DOC-21` | تحليل PDF بالتخطيط (ثقيل) | Layout-aware PDF parsing (docling, camelot, tabula) | install | pip:opencv, pip:torch, pip:docling |
| `DOC-29` | Docling: تحويل PDF وDOCX وPPTX إلى Markdown أو | Docling: Convert PDF/DOCX/PPTX to structured Markdown/JSON with tables kept | install | pip:office, pip:docling |
| `DOC-30` | Marker: تحويل ملفات PDF الأكاديمية أو الممسوحة إلى | Marker: Turn scanned or academic PDFs into Markdown with equations in LaTeX | install | latex, network, pip:marker |
| `DOC-31` | Slidev: كتابة عرض تقديمي بـMarkdown وتصديره PDF أو | Slidev: Author a Markdown deck and export PDF/PNG | install | chromium, npm:slidev |
| `DOC-32` | Marp CLI: تحويل Markdown إلى شرائح PDF أو PPTX | Marp CLI: Markdown to PDF/PPTX/HTML decks in one command | install | pip:office, npm:marp |
| `DOC-33` | Mermaid: رسم مخططات انسيابية وتسلسلية وجانت من نص | Mermaid: Render flowcharts, sequence and Gantt diagrams from text to SVG/PNG | install | npm:mermaid |
| `DOC-34` | PlantUML: توليد مخططات UML من نص | PlantUML: Generate UML class/sequence/component diagrams from text | install | plantuml |
| `DOC-25` | مهارات المستندات المدمجة في المضيف | Host document skills (docx/xlsx/pptx/pdf) | key | pip:office, key:unspecified |
| `DOC-26` | موصل المستندات الحية | Living-docs connector (Claude Docs) | key | key:unspecified |
| `DOC-27` | إنشاء الملفات في claude.ai | claude.ai file creation sandbox | key | pip:office, key:unspecified |
| `DOC-28` | ملفات Google عبر الموصل | Google Docs/Sheets/Slides via connector | key | key:unspecified |
