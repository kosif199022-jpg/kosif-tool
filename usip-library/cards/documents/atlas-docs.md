# `atlas-docs` — المستندات والكتابة (45 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/atlas-docs.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/documents.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`ADOCS-01` كتابة AGENTS.md وCLAUDE.md جاهزة للوكلاء](#adocs-01--كتابة-agentsmd-وclaudemd-جاهزة-للوكلاء--agent-ready-agentsmd-and-claudemd-authoring)
- [`ADOCS-02` تدقيق CLAUDE.md وAGENTS.md وتخفيف السياق](#adocs-02--تدقيق-claudemd-وagentsmd-وتخفيف-السياق--audit-claudemd-and-agentsmd-for-context-diet)
- [`ADOCS-03` مزامنة ذاكرة التعليمات دون تضخم مع تحقق مستقل](#adocs-03--مزامنة-ذاكرة-التعليمات-دون-تضخم-مع-تحقق-مستقل--non-growth-instruction-memory-sync-with-independent-verify)
- [`ADOCS-04` إعداد تقرير TPAR للمقاولين في أستراليا](#adocs-04--إعداد-تقرير-tpar-للمقاولين-في-أستراليا--australian-tpar-contractor-report-prep)
- [`ADOCS-05` تجميع حزمة الإقفال المالي الشهري للعميل](#adocs-05--تجميع-حزمة-الإقفال-المالي-الشهري-للعميل--month-end-client-financial-pack-assembly)
- [`ADOCS-06` توليد العقود والاتفاقيات](#adocs-06--توليد-العقود-والاتفاقيات--contract-and-agreement-generation)
- [`ADOCS-07` مراجعة مخاطر العقود واتفاقيات السرية](#adocs-07--مراجعة-مخاطر-العقود-واتفاقيات-السرية--contract-and-nda-risk-review-with-redline)
- [`ADOCS-08` مراجعة العقود بدليل بنود ومستويات مخاطر](#adocs-08--مراجعة-العقود-بدليل-بنود-ومستويات-مخاطر--contract-review-with-clause-playbook-and-tiers)
- [`ADOCS-09` الرد على طلبات العروض والمشتريات العامة](#adocs-09--الرد-على-طلبات-العروض-والمشتريات-العامة--rfp-and-public-procurement-response)
- [`ADOCS-10` سجل المخاطر والحوكمة والامتثال](#adocs-10--سجل-المخاطر-والحوكمة-والامتثال--risk-register-and-compliance-governance)
- [`ADOCS-11` مخطط علاقات الكيانات من ملفات المخطط](#adocs-11--مخطط-علاقات-الكيانات-من-ملفات-المخطط--offline-er-diagram-from-schema-declarations)
- [`ADOCS-12` مراجعة ما بعد الحادث بلا لوم](#adocs-12--مراجعة-ما-بعد-الحادث-بلا-لوم--blameless-postmortem-with-timeline-and-action-items)
- [`ADOCS-13` حزمة تشخيص مُنقّحة وآمنة للدعم](#adocs-13--حزمة-تشخيص-مُنقّحة-وآمنة-للدعم--secret-safe-redacted-diagnostic-bundle-for-support)
- [`ADOCS-14` جاهزية الموقع لـ llms.txt وزواحف AI](#adocs-14--جاهزية-الموقع-لـ-llmstxt-وزواحف-ai--llmstxt-and-ai-crawler-readiness)
- [`ADOCS-15` تصنيف MDR الأوروبي والملف الفني](#adocs-15--تصنيف-mdr-الأوروبي-والملف-الفني--eu-mdr-classification-and-technical-file)
- [`ADOCS-16` شجرة اختيار مسار FDA للأجهزة الطبية](#adocs-16--شجرة-اختيار-مسار-fda-للأجهزة-الطبية--fda-device-pathway-selection-decision-tree)
- [`ADOCS-17` مخطط AWS بصيغة draw.io بأيقونات رسمية](#adocs-17--مخطط-aws-بصيغة-drawio-بأيقونات-رسمية--aws-architecture-drawio-with-official-icons)
- [`ADOCS-18` اختيار محرك المخططات: PlantUML أو D2 أو Structurizr](#adocs-18--اختيار-محرك-المخططات-plantuml-أو-d2-أو-structurizr--diagram-as-code-engine-choice-plantuml-d2-structurizr)
- [`ADOCS-19` مخطط معماري مبني على الريبو الفعلي](#adocs-19--مخطط-معماري-مبني-على-الريبو-الفعلي--evidence-grounded-architecture-diagram-from-repo)
- [`ADOCS-20` رسم Excalidraw يحمل حجة بصرية](#adocs-20--رسم-excalidraw-يحمل-حجة-بصرية--excalidraw-diagram-that-argues-visually)
- [`ADOCS-21` رسم مخططات Mermaid والتحقق منها](#adocs-21--رسم-مخططات-mermaid-والتحقق-منها--mermaid-diagram-render-and-validate-loop)
- [`ADOCS-22` تخطيط الرسوم العقدية وتصميم UML](#adocs-22--تخطيط-الرسوم-العقدية-وتصميم-uml--node-link-layout-and-uml-diagram-design)
- [`ADOCS-23` مخطط HTML مستقل بـ SVG مضمن](#adocs-23--مخطط-html-مستقل-بـ-svg-مضمن--self-contained-html-diagram-with-inline-svg)
- [`ADOCS-24` خطة تنفيذ مرئية للمراجعة في المتصفح](#adocs-24--خطة-تنفيذ-مرئية-للمراجعة-في-المتصفح--visual-implementation-plan-reviewed-in-browser)
- [`ADOCS-25` إنشاء ADR وRFC مع ترقيم وربط](#adocs-25--إنشاء-adr-وrfc-مع-ترقيم-وربط--adrrfcprd-creation-with-id-linking)
- [`ADOCS-26` تحديث التوثيق بالاعتماد على الكود](#adocs-26--تحديث-التوثيق-بالاعتماد-على-الكود--code-grounded-doc-update-and-overhaul)
- [`ADOCS-27` إعادة هيكلة التوثيق بإطار دياتاكسيس](#adocs-27--إعادة-هيكلة-التوثيق-بإطار-دياتاكسيس--diataxis-four-kind-docs-restructuring)
- [`ADOCS-28` تدقيق انحراف التوثيق عن الكود](#adocs-28--تدقيق-انحراف-التوثيق-عن-الكود--docs-drift-audit-against-current-code)
- [`ADOCS-29` توثيق الدروس المستفادة من المشكلات المحلولة](#adocs-29--توثيق-الدروس-المستفادة-من-المشكلات-المحلولة--durable-solved-problem-learning-notes)
- [`ADOCS-30` ويكي مترابط تديره النماذج](#adocs-30--ويكي-مترابط-تديره-النماذج--llm-maintained-interlinked-wiki)
- [`ADOCS-31` البحث في توثيق المكتبات بالإصدار الصحيح](#adocs-31--البحث-في-توثيق-المكتبات-بالإصدار-الصحيح--look-up-version-correct-library-docs)
- [`ADOCS-32` ضغط الماركداون دون فقدان المعنى](#adocs-32--ضغط-الماركداون-دون-فقدان-المعنى--lossless-markdown-compression-with-semantic-diff-gate)
- [`ADOCS-33` كتابة README والتحقق منه](#adocs-33--كتابة-readme-والتحقق-منه--readme-authoring-and-verification)
- [`ADOCS-34` إزالة التعليقات الزائدة في الكود](#adocs-34--إزالة-التعليقات-الزائدة-في-الكود--strip-ai-slop-and-zero-info-code-comments)
- [`ADOCS-35` كتابة سرد الألعاب المتفرع](#adocs-35--كتابة-سرد-الألعاب-المتفرع--game-narrative-and-branching-writing)
- [`ADOCS-36` اختيار رقم الإصدار وكتابة سجل التغييرات](#adocs-36--اختيار-رقم-الإصدار-وكتابة-سجل-التغييرات--semver-bump-and-changelog-plan)
- [`ADOCS-37` كتابة الرياضيات وشرحها المطوّل](#adocs-37--كتابة-الرياضيات-وشرحها-المطوّل--math-notation-and-long-form-exposition)
- [`ADOCS-38` تقرير اختبار فهم بعد التغيير](#adocs-38--تقرير-اختبار-فهم-بعد-التغيير--post-change-comprehension-quiz-report)
- [`ADOCS-39` هيكل منهج ذاتي مع سجل تقييم](#adocs-39--هيكل-منهج-ذاتي-مع-سجل-تقييم--self-study-curriculum-scaffold-with-assessment-log)
- [`ADOCS-40` مقال تعليمي من جلسة عمل](#adocs-40--مقال-تعليمي-من-جلسة-عمل--teaching-block-article-from-a-working-session)
- [`ADOCS-41` شرح بصري مبسط جداً بأسلوب طفل](#adocs-41--شرح-بصري-مبسط-جداً-بأسلوب-طفل--zero-knowledge-visual-eli5-explainer)
- [`ADOCS-42` الكتابة البسيطة: كلمات يومية وجمل كاملة](#adocs-42--الكتابة-البسيطة-كلمات-يومية-وجمل-كاملة--plain-writing-everyday-words-complete-sentences)
- [`ADOCS-43` أنسنة النص بالكثافة لا بقائمة حذف](#adocs-43--أنسنة-النص-بالكثافة-لا-بقائمة-حذف--humanize-by-density-with-an-over-correction-guard)
- [`ADOCS-44` تدقيق انحراف التوثيق عن الكود لكل بُعد](#adocs-44--تدقيق-انحراف-التوثيق-عن-الكود-لكل-بُعد--per-dimension-documentation-drift-audit)
- [`ADOCS-45` الترجمة الإبداعية: متى نترجم ومتى نعيد الصياغة](#adocs-45--الترجمة-الإبداعية-متى-نترجم-ومتى-نعيد-الصياغة--transcreation-routing-for-marketing-translation)

## البطاقات / cards

### `ADOCS-01` — كتابة AGENTS.md وCLAUDE.md جاهزة للوكلاء / Agent-ready AGENTS.md and CLAUDE.md authoring

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** كتابة ملفات توجيه الوكلاء بكثافة عالية وبنطاقات وأوامر وحدود ومراجعة الانحراف. — Write or refine high-density AGENTS.md/CLAUDE.md with scoped commands and boundaries, and audit for drift.

**متى:** Agents misuse repo commands; creating or maintaining project guidance files.

**كيف:** 1) Ask questionnaire first. 2) Size file to codebase. 3) Put exact commands and boundaries. 4) Add scoped AGENTS.md in areas with different rules. 5) Audit drift and let user decide each. 6) Cut anything not changing behavior.

**المعاملات:** repo

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** AGENTS.md · CLAUDE.md · توجيه

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `ADOCS-02` تدقيق CLAUDE.md وAGENTS.md وتخفيف السياق / Audit CLAUDE.md and AGENTS.md for context diet (documented)
- `ADOCS-03` مزامنة ذاكرة التعليمات دون تضخم مع تحقق مستقل / Non-growth instruction-memory sync with independent verify (documented)

### `ADOCS-02` — تدقيق CLAUDE.md وAGENTS.md وتخفيف السياق / Audit CLAUDE.md and AGENTS.md for context diet

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يدقق ملفات سياق الوكلاء في المستودع، وينقل المحتوى الدائم الثقيل إلى مهارات عند الطلب أو وثائق مرتبطة، ويزامن ملفات التعليمات بين الأدوات من مصدر واحد. — Audit repository agent-context files, move always-loaded bulk into on-demand skills or linked docs, and keep per-tool instruction files in sync from one source.

**متى:** CLAUDE.md feels bloated or ignored, an agent repeats the same project mistake, quality drops in long sessions, or the team wants one instruction source for several AI tools.

**كيف:** 1) Inventory CLAUDE.md, AGENTS.md, .cursor/rules, Copilot instructions and .claude/rules. 2) Classify each block: always-needed, task-specific (make it a skill), heavy reference (link a doc), or delegated work (subagent). 3) Cut long or ignored sections; keep short, testable rules about repeated mistakes. 4) Add pointers so every context file stays small and loads on demand. 5) Generate per-tool files from one config (AGENTS.md from a sources list) and verify they match. 6) Capture recurring corrections as new rules.

**المعاملات:** repo path; target tools (Claude, Cursor, Copilot); size budget

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** CLAUDE.md · AGENTS.md · context-budget · سياق الوكيل · prompt-hygiene

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3047-adlc-context/13100-agent-context-files`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2134-agent-patterns-plugin/7575-meta-context-diet`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2815-agent-sync/11429-agent-sync`

#### 7. قدرات قريبة في العائلة

- `ADOCS-01` كتابة AGENTS.md وCLAUDE.md جاهزة للوكلاء / Agent-ready AGENTS.md and CLAUDE.md authoring (documented)
- `ADOCS-03` مزامنة ذاكرة التعليمات دون تضخم مع تحقق مستقل / Non-growth instruction-memory sync with independent verify (documented)
- `ADOCS-04` إعداد تقرير TPAR للمقاولين في أستراليا / Australian TPAR contractor report prep (documented)

### `ADOCS-03` — مزامنة ذاكرة التعليمات دون تضخم مع تحقق مستقل / Non-growth instruction-memory sync with independent verify

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT (no copyleft seen among supporting ids); the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** توليد مهارة مزامنة ذاكرة محلية تقارن CLAUDE.md والقواعد وملفات الوكلاء بالشيفرة، فتصلح الحقائق القديمة أولاً ثم تزيل التكرار وتضغط دون أن يكبر أي ملف، مع وكلاء تحقق مستقلين. — Generate a project-local memory-sync skill that diffs CLAUDE.md, rules and agent files against the code, repairs stale facts first, then dedups and compresses so no file grows, with separate verifier agents re-checking every edit.

**متى:** CLAUDE.md or rules drifted from the code; too much always-loaded context; after a branch or commit range changed behavior; requests like 'sync memory', 'slim context', 'clean up agent config'.

**كيف:** 1) Resolve the mode (status\|install\|upgrade\|...\|purge) from the prompt; print a PLAN block; ask only if destructive. 2) Enumerate the memory surface by command; split into disjoint batches. 3) GATHER: read-only agents list change facts for the scope (session\|branch\|commit\|all). 4) SYNC: one bounded agent per batch, all spawned in one message; facts first, dedup second, compression third; every file ends at or below its line count. 5) VERIFY: a different read-only agent per edited batch re-checks each fact in code and that removed facts are gone. 6) HARD depth: audit rule path globs (TOO_BROAD/TOO_NARROW/DANGLING/MISSING) and purge what a model already knows. 7) Report in chat only.

**المعاملات:** scope (session\|branch\|commit <sha>\|recent:N\|all); depth (NORMAL\|HARD); reach (MEMORY\|REFS); free-text emphasis

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** memory-sync · CLAUDE.md · context-slim · مزامنة-الذاكرة · verify

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2096-brewdoc/7431-memory-sync-setup`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2098-brewtools/7442-context-slim`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/945-clean-up-agent-config/2230-clean-up-agent-config`

#### 7. قدرات قريبة في العائلة

- `ADOCS-01` كتابة AGENTS.md وCLAUDE.md جاهزة للوكلاء / Agent-ready AGENTS.md and CLAUDE.md authoring (documented)
- `ADOCS-02` تدقيق CLAUDE.md وAGENTS.md وتخفيف السياق / Audit CLAUDE.md and AGENTS.md for context diet (documented)
- `ADOCS-04` إعداد تقرير TPAR للمقاولين في أستراليا / Australian TPAR contractor report prep (documented)
- `ADOCS-05` تجميع حزمة الإقفال المالي الشهري للعميل / Month-end client financial pack assembly (documented)

### `ADOCS-04` — إعداد تقرير TPAR للمقاولين في أستراليا / Australian TPAR contractor report prep

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يعد تفصيل TPAR السنوي بتحديد المقاولين وفحص ABN وفصل ضريبة GST وتسجيل الأخطاء في ورقة عمل. — Prepare an annual TPAR breakdown: identify reportable contractors, validate ABNs, split GST and log errors in a working paper.

**متى:** Australian client in a reportable industry needs the contractor payments report.

**كيف:** 1) Pull a full year of supplier bills and direct payments. 2) Filter by reportable industries (construction, cleaning, courier, IT, road freight, security); mixed businesses apply the 10% of GST turnover test. 3) Validate ABN: 11 digits plus check digit. 4) Separate GST; report gross. 5) Aggregate per contractor (gross, GST, net, count, first/last date). 6) Error sweep: missing ABN, duplicates, employees in AP, materials-only. 7) Word working paper; deadline 28 August.

**المعاملات:** financial year, industry

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** tpar · abn · tax · ضرائب · أستراليا

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3585-xbert-tpar/14397-tpar`

#### 7. قدرات قريبة في العائلة

- `ADOCS-02` تدقيق CLAUDE.md وAGENTS.md وتخفيف السياق / Audit CLAUDE.md and AGENTS.md for context diet (documented)
- `ADOCS-03` مزامنة ذاكرة التعليمات دون تضخم مع تحقق مستقل / Non-growth instruction-memory sync with independent verify (documented)
- `ADOCS-05` تجميع حزمة الإقفال المالي الشهري للعميل / Month-end client financial pack assembly (documented)
- `ADOCS-06` توليد العقود والاتفاقيات / Contract and agreement generation (documented)

### `ADOCS-05` — تجميع حزمة الإقفال المالي الشهري للعميل / Month-end client financial pack assembly

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يجمع حزمة الإقفال الشهري من الأرباح والخسائر مقابل الميزانية وحركة الميزانية والتدفق النقدي ومؤشرات الأداء. — Assemble a month-end pack with P&L versus budget, balance sheet movement, cashflow and KPI commentary.

**متى:** Partner needs a client close packet or monthly management pack.

**كيف:** 1) Fetch figures only from the ledger tool, never estimate. 2) P&L vs budget with variance commentary. 3) Balance sheet movement walk. 4) Cashflow vs forecast. 5) Narrate material journals and outstanding queries inline. 6) KPI roll-up page. 7) Render to docx/xlsx payloads for review.

**المعاملات:** month, client

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** month-end · reporting · financials · إقفال · تقارير

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3562-xbert-close-packet/14374-close-packet`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3573-xbert-month-end-pack/14385-month-end-pack`

#### 7. قدرات قريبة في العائلة

- `ADOCS-03` مزامنة ذاكرة التعليمات دون تضخم مع تحقق مستقل / Non-growth instruction-memory sync with independent verify (documented)
- `ADOCS-04` إعداد تقرير TPAR للمقاولين في أستراليا / Australian TPAR contractor report prep (documented)
- `ADOCS-06` توليد العقود والاتفاقيات / Contract and agreement generation (documented)
- `ADOCS-07` مراجعة مخاطر العقود واتفاقيات السرية / Contract and NDA risk review with redline (documented)

### `ADOCS-06` — توليد العقود والاتفاقيات / Contract and agreement generation

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يصيغ اتفاقيات عدم إفصاح وعقود خدمة وشروط استخدام وعقود عمل مع شروحات مبسطة. — Draft NDAs, service agreements, terms of service and employment contracts with plain-English annotations.

**متى:** Need a first-draft agreement or ToS for a business.

**كيف:** 1) Ask relationship type, jurisdiction, parties, term. 2) Pick template among about 10 agreement types. 3) Fill clauses and annotate each in plain language (about 8th-grade level). 4) List missing protections checklist. 5) Mark counsel-review points.

**المعاملات:** type, jurisdiction

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** agreements · NDA · اتفاقيات · ToS

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `ADOCS-04` إعداد تقرير TPAR للمقاولين في أستراليا / Australian TPAR contractor report prep (documented)
- `ADOCS-05` تجميع حزمة الإقفال المالي الشهري للعميل / Month-end client financial pack assembly (documented)
- `ADOCS-07` مراجعة مخاطر العقود واتفاقيات السرية / Contract and NDA risk review with redline (documented)
- `ADOCS-08` مراجعة العقود بدليل بنود ومستويات مخاطر / Contract review with clause playbook and tiers (documented)

### `ADOCS-07` — مراجعة مخاطر العقود واتفاقيات السرية / Contract and NDA risk review with redline

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0 / MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يقرأ العقد كاملاً ويصنّفه ويقيّم بنوده في ثماني فئات مخاطر ويقترح تعديلات، ويصوغ اتفاقية سرية. — Read a contract fully, classify it, score clauses across eight risk categories and propose redlines; also draft an NDA.

**متى:** User uploads or pastes an NDA, MSA, lease or vendor agreement, or asks to draft an NDA.

**كيف:** 1) Use supplied file/paste first; read exhibits and schedules too. 2) Identify type and which party is the user. 3) Review 8 categories starting with payment terms (Net-30 normal, Net-60+ flag). 4) Tier findings by severity with plain-English reasons. 5) Write negotiation playbook and redline (DOCX). 6) Note not legal advice.

**المعاملات:** contract type, user party, jurisdiction

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** contract review · NDA · redline · عقود · مراجعة قانونية

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/335-small-business/1144-contract-review`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`

#### 7. قدرات قريبة في العائلة

- `ADOCS-05` تجميع حزمة الإقفال المالي الشهري للعميل / Month-end client financial pack assembly (documented)
- `ADOCS-06` توليد العقود والاتفاقيات / Contract and agreement generation (documented)
- `ADOCS-08` مراجعة العقود بدليل بنود ومستويات مخاطر / Contract review with clause playbook and tiers (documented)
- `ADOCS-09` الرد على طلبات العروض والمشتريات العامة / RFP and public procurement response (documented)

### `ADOCS-08` — مراجعة العقود بدليل بنود ومستويات مخاطر / Contract review with clause playbook and tiers

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT/Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يراجع العقد مقابل مواقف البنود المعيارية والبديلة والمرفوضة ويصنف الانحرافات ويستخرج الشروط. — Review a contract against standard/fallback/walk-away clause positions, flag material deviations by tier and extract key terms.

**متى:** Incoming contract, NDA triage, redlines, approval routing.

**كيف:** 1) Ingest file (PDF/DOCX/TXT) and classify type. 2) Compare against clause library (liability, indemnity, IP, term, confidentiality). 3) Tier each deviation: within fallback, beyond fallback, walk-away; route to approver. 4) Optionally run parallel lenses (risk, plain-English, missing protections, compliance) and aggregate a 0-100 safety score. 5) Extract parties, value, dates, cap, governing law, renewal into schema. 6) State not legal advice.

**المعاملات:** contract text, playbook

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** contracts · legal · عقود · redline · NDA

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2326-legal-ops-clm/8929-contract-review-and-redline`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1634-general-legal-assistant/4611-contract-review`

#### 7. قدرات قريبة في العائلة

- `ADOCS-06` توليد العقود والاتفاقيات / Contract and agreement generation (documented)
- `ADOCS-07` مراجعة مخاطر العقود واتفاقيات السرية / Contract and NDA risk review with redline (documented)
- `ADOCS-09` الرد على طلبات العروض والمشتريات العامة / RFP and public procurement response (documented)
- `ADOCS-10` سجل المخاطر والحوكمة والامتثال / Risk register and compliance governance (documented)

### `ADOCS-09` — الرد على طلبات العروض والمشتريات العامة / RFP and public procurement response

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يقرر المشاركة أو الاعتذار ويبني مصفوفة امتثال ويكتب رداً منظماً على طلب العرض. — Decide bid or no-bid, build a compliance matrix and write a scannable RFP/RFI response.

**متى:** Receiving an RFP/RFI/RFQ or government tender.

**كيف:** 1) Score bid/no-bid before effort. 2) Extract every requirement into a compliance matrix. 3) Draft answers mapped to requirements, scannable. 4) Add pricing and deal proposal. 5) Review gaps before submission.

**المعاملات:** tender, scoring criteria

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** RFP · bid · مناقصة · عروض · مشتريات

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2363-public-sector-govtech/9125-public-procurement-and-rfp`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`

#### 7. قدرات قريبة في العائلة

- `ADOCS-07` مراجعة مخاطر العقود واتفاقيات السرية / Contract and NDA risk review with redline (documented)
- `ADOCS-08` مراجعة العقود بدليل بنود ومستويات مخاطر / Contract review with clause playbook and tiers (documented)
- `ADOCS-10` سجل المخاطر والحوكمة والامتثال / Risk register and compliance governance (documented)
- `ADOCS-11` مخطط علاقات الكيانات من ملفات المخطط / Offline ER diagram from schema declarations (documented)

### `ADOCS-10` — سجل المخاطر والحوكمة والامتثال / Risk register and compliance governance

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | method paraphrased from Atlas skills under MIT/Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يبني سجل مخاطر باحتمال×أثر وسياسات حوكمة مرتبطة بضوابط ومسؤولين. — Build likelihood-times-impact risk registers and governance policies tied to controls and owners.

**متى:** Legal risk triage, ISO 42001, GRC, data access governance.

**كيف:** 1) List assets and threats. 2) Score likelihood x impact. 3) Select controls from risk. 4) Severity-by-likelihood escalation criteria. 5) Assign owners; evidence for audits.

**المعاملات:** framework

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** risk · GRC · امتثال · governance

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `ADOCS-08` مراجعة العقود بدليل بنود ومستويات مخاطر / Contract review with clause playbook and tiers (documented)
- `ADOCS-09` الرد على طلبات العروض والمشتريات العامة / RFP and public procurement response (documented)
- `ADOCS-11` مخطط علاقات الكيانات من ملفات المخطط / Offline ER diagram from schema declarations (documented)
- `ADOCS-12` مراجعة ما بعد الحادث بلا لوم / Blameless postmortem with timeline and action items (documented)

### `ADOCS-11` — مخطط علاقات الكيانات من ملفات المخطط / Offline ER diagram from schema declarations

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ارسم مخطط ERD من تعريفات المخطط المخزنة دون اتصال بقاعدة البيانات. — Draw a Mermaid or DBML ERD from Prisma models, EF mappings or SQL migrations without a DB connection, tracing every entity to a file.

**متى:** Need to document or understand data model from a repo.

**كيف:** 1) Resolve the output dir and dialect (mermaid default, dbml optional). 2) Collect declarations in precedence: Prisma, then EF fluent, then SQL migrations. 3) Emit entities, optional columns, and cardinalities only as recorded. 4) Render and cite source file per box. 5) Never invent a relation.

**المعاملات:** --scope, --include-columns, --dialect, --out

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** erd · schema · mermaid · مخطط · توثيق

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:mermaid` ← npm ls mermaid أو وجود node_modules/mermaid
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2415-architecture/9363-map-data`

#### 7. قدرات قريبة في العائلة

- `ADOCS-09` الرد على طلبات العروض والمشتريات العامة / RFP and public procurement response (documented)
- `ADOCS-10` سجل المخاطر والحوكمة والامتثال / Risk register and compliance governance (documented)
- `ADOCS-12` مراجعة ما بعد الحادث بلا لوم / Blameless postmortem with timeline and action items (documented)
- `ADOCS-13` حزمة تشخيص مُنقّحة وآمنة للدعم / Secret-safe redacted diagnostic bundle for support (documented)

### `ADOCS-12` — مراجعة ما بعد الحادث بلا لوم / Blameless postmortem with timeline and action items

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يكتب مراجعة بلا لوم بالجدول الزمني والسبب الجذري وبنود عمل متتبعة. — Writes a blameless postmortem: timeline, root cause, contributing factors and tracked actions.

**متى:** After SEV1/SEV2, outage over 15 min, data loss, or near-miss.

**كيف:** 1) Draft within 1-2 days, meeting days 3-5, finalize day 5-7. 2) Frame as what conditions allowed it. 3) Timeline, impact, root cause plus contributing factors. 4) Action items with owner and due date. 5) Review patterns quarterly.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** postmortem · RCA · مراجعة · حادث

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3101-incident-response/13273-postmortem-writing`

#### 7. قدرات قريبة في العائلة

- `ADOCS-10` سجل المخاطر والحوكمة والامتثال / Risk register and compliance governance (documented)
- `ADOCS-11` مخطط علاقات الكيانات من ملفات المخطط / Offline ER diagram from schema declarations (documented)
- `ADOCS-13` حزمة تشخيص مُنقّحة وآمنة للدعم / Secret-safe redacted diagnostic bundle for support (documented)
- `ADOCS-14` جاهزية الموقع لـ llms.txt وزواحف AI / llms.txt and AI-crawler readiness (documented)

### `ADOCS-13` — حزمة تشخيص مُنقّحة وآمنة للدعم / Secret-safe redacted diagnostic bundle for support

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** جمّع حزمة دعم دنيا قائمة على قائمة سماح مع تنقيح موثّق وبصمات ومسؤول حذف. — Assemble a minimal allowlist-based support bundle with verified redaction, hashes and a deletion owner.

**متى:** Escalating to vendor support or incident review with logs/config involved.

**كيف:** 1) Define incident window, service, audience, retention, custodian. 2) Write allowlist manifest and forbidden field classes first. 3) Collect versions, config key presence (not values), status/error class, request IDs, timing, retry history. 4) Synthetic repro with expected vs observed. 5) Run secret/URL/PII canary scan on all output; abort if any survives. 6) Hash bundle, log redactions and gaps, schedule deletion.

**المعاملات:** service, incident window, audience

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** debug-bundle · redaction · حزمة-تشخيص · support

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1819-adobe-pack/4896-adobe-debug-bundle`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1818-abridge-pack/4875-abridge-debug-bundle`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1835-claude-pack/5238-clade-debug-bundle`

#### 7. قدرات قريبة في العائلة

- `ADOCS-11` مخطط علاقات الكيانات من ملفات المخطط / Offline ER diagram from schema declarations (documented)
- `ADOCS-12` مراجعة ما بعد الحادث بلا لوم / Blameless postmortem with timeline and action items (documented)
- `ADOCS-14` جاهزية الموقع لـ llms.txt وزواحف AI / llms.txt and AI-crawler readiness (documented)
- `ADOCS-15` تصنيف MDR الأوروبي والملف الفني / EU MDR classification and technical file (documented)

### `ADOCS-14` — جاهزية الموقع لـ llms.txt وزواحف AI / llms.txt and AI-crawler readiness

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** جعل الموقع مقروءاً لنماذج اللغة عبر llms.txt ومسارات md وترويسات Link. — Make a site readable to LLMs with llms.txt, .md routes, Link headers, Content-Signal and crawler checks.

**متى:** Optimizing docs or blog for AI citation and agent fetching.

**كيف:** 1) Map host header control. 2) Allow GPTBot/ClaudeBot/PerplexityBot; add Content-Signal. 3) Curated /llms.txt. 4) Serve /path.md from same source, text/markdown. 5) Advertise via link tag and HTTP Link header. 6) Accept negotiation. 7) Measure AI citations with answer samples.

**المعاملات:** signal policy

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** llms-txt · geo · seo · ذكاء

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3174-llms-visibility/13503-llms-visibility`

#### 7. قدرات قريبة في العائلة

- `ADOCS-12` مراجعة ما بعد الحادث بلا لوم / Blameless postmortem with timeline and action items (documented)
- `ADOCS-13` حزمة تشخيص مُنقّحة وآمنة للدعم / Secret-safe redacted diagnostic bundle for support (documented)
- `ADOCS-15` تصنيف MDR الأوروبي والملف الفني / EU MDR classification and technical file (documented)
- `ADOCS-16` شجرة اختيار مسار FDA للأجهزة الطبية / FDA device pathway selection decision tree (documented)

### `ADOCS-15` — تصنيف MDR الأوروبي والملف الفني / EU MDR classification and technical file

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تصنيف الجهاز وفق قواعد MDR وتجهيز مخطط الملف الفني والتقييم السريري. — Classify a device under MDR 2017/745 Annex VIII rules and outline the technical documentation and clinical evaluation.

**متى:** User needs CE marking, MDR class, PSUR or post-market plan.

**كيف:** 1) Record duration, invasiveness, body-system contact, active/energy status. 2) Apply rules 1-22; software via MDCG 2019-11 algorithm. 3) Document rationale and confirm with Notified Body. 4) Map Annex II/III technical file sections. 5) Plan Annex XIV clinical evaluation and Art. 86 PSUR cadence.

**المعاملات:** device facts, software role

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** MDR · CE · medtech · تصنيف

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/214-ra-qm-skills/679-mdr-745-specialist`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/214-ra-qm-skills/684-ra-qm-skills`

#### 7. قدرات قريبة في العائلة

- `ADOCS-13` حزمة تشخيص مُنقّحة وآمنة للدعم / Secret-safe redacted diagnostic bundle for support (documented)
- `ADOCS-14` جاهزية الموقع لـ llms.txt وزواحف AI / llms.txt and AI-crawler readiness (documented)
- `ADOCS-16` شجرة اختيار مسار FDA للأجهزة الطبية / FDA device pathway selection decision tree (documented)
- `ADOCS-17` مخطط AWS بصيغة draw.io بأيقونات رسمية / AWS architecture draw.io with official icons (documented)

### `ADOCS-16` — شجرة اختيار مسار FDA للأجهزة الطبية / FDA device pathway selection decision tree

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** اختيار مسار 510(k) أو De Novo أو PMA حسب وجود جهاز مرجعي ودرجة الخطورة وتخطيط اجتماع ما قبل التقديم. — Choose 510(k) / De Novo / PMA from predicate availability and risk, then plan a Pre-Sub.

**متى:** Medical device team asks which FDA route, timeline or fee applies.

**كيف:** 1) Identify product code and class. 2) Search 510(k) database for predicates. 3) Branch: predicate+equivalent -> 510(k) (abbreviated/special/traditional by change type); novel low-moderate risk -> De Novo; Class III -> PMA. 4) Tabulate timeline and user fee, flag fee year. 5) Draft Q-Sub questions and schedule Pre-Sub. Output is a recommendation for regulatory review.

**المعاملات:** device description, intended use, candidate predicates

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** FDA · 510k · regulatory · هيئة الغذاء والدواء

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/214-ra-qm-skills/674-fda-consultant-specialist`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/214-ra-qm-skills/685-regulatory-affairs-head`

#### 7. قدرات قريبة في العائلة

- `ADOCS-14` جاهزية الموقع لـ llms.txt وزواحف AI / llms.txt and AI-crawler readiness (documented)
- `ADOCS-15` تصنيف MDR الأوروبي والملف الفني / EU MDR classification and technical file (documented)
- `ADOCS-17` مخطط AWS بصيغة draw.io بأيقونات رسمية / AWS architecture draw.io with official icons (documented)
- `ADOCS-18` اختيار محرك المخططات: PlantUML أو D2 أو Structurizr / Diagram-as-code engine choice: PlantUML, D2, Structurizr (documented)

### `ADOCS-17` — مخطط AWS بصيغة draw.io بأيقونات رسمية / AWS architecture draw.io with official icons

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0 / MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** توليد XML لمخطط AWS بأيقونات AWS4 الرسمية. — Generate validated draw.io XML for AWS architectures using AWS4 icons, optionally from IaC.

**متى:** User wants cloud infrastructure diagram or Azure resource map.

**كيف:** 1. Mode A scan CloudFormation/CDK/Terraform, or mode B ask 3-5 questions. 2. Confirm architecture. 3. Load XML, style and layout rules. 4. Add title, numbered step badges, legend for 7+ services. 5. Export .drawio, optional png/svg/pdf. Azure variant outputs Mermaid from resource groups.

**المعاملات:** sketch, legend, export format

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** aws · drawio · azure · سحابة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:mermaid` ← npm ls mermaid أو وجود node_modules/mermaid
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/373-deploy-on-aws/1376-aws-architecture-diagram`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2511-azure/9715-azure-resource-visualizer`

#### 7. قدرات قريبة في العائلة

- `ADOCS-15` تصنيف MDR الأوروبي والملف الفني / EU MDR classification and technical file (documented)
- `ADOCS-16` شجرة اختيار مسار FDA للأجهزة الطبية / FDA device pathway selection decision tree (documented)
- `ADOCS-18` اختيار محرك المخططات: PlantUML أو D2 أو Structurizr / Diagram-as-code engine choice: PlantUML, D2, Structurizr (documented)
- `ADOCS-19` مخطط معماري مبني على الريبو الفعلي / Evidence-grounded architecture diagram from repo (documented)

### `ADOCS-18` — اختيار محرك المخططات: PlantUML أو D2 أو Structurizr / Diagram-as-code engine choice: PlantUML, D2, Structurizr

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** اختيار أنسب محرك مخططات نصية وإنتاج أو فحص الشيفرة. — Select the best text-diagram engine for the request and produce or lint the source.

**متى:** User asks for UML, C4, Gantt, ERD or polished architecture diagram as code.

**كيف:** 1. Choose mode: create, reference or check. 2. Engine by rule: user-named or existing files first, then project convention. 3. C4 multi-view -> Structurizr; UML/Gantt/mindmap -> PlantUML; architecture/flowchart/ERD (sql_table) -> D2. 4. Consult the engine reference before writing syntax. 5. Render to validate; keep .puml/.d2/.dsl next to docs.

**المعاملات:** mode, engine

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** plantuml · d2 · C4 · uml

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `plantuml` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3135-diagram/13445-diagram`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2173-tools-plugin/7914-d2-diagrams`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2690-build-web-data-visualization/10334-uml-and-software-architecture-visualizat`

#### 7. قدرات قريبة في العائلة

- `ADOCS-16` شجرة اختيار مسار FDA للأجهزة الطبية / FDA device pathway selection decision tree (documented)
- `ADOCS-17` مخطط AWS بصيغة draw.io بأيقونات رسمية / AWS architecture draw.io with official icons (documented)
- `ADOCS-19` مخطط معماري مبني على الريبو الفعلي / Evidence-grounded architecture diagram from repo (documented)
- `ADOCS-20` رسم Excalidraw يحمل حجة بصرية / Excalidraw diagram that argues visually (documented)

### `ADOCS-19` — مخطط معماري مبني على الريبو الفعلي / Evidence-grounded architecture diagram from repo

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; one WTFPL; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** استخراج العقد والروابط من ملفات المشروع الفعلية ورسم المخطط. — Derive nodes and edges from manifests, compose, k8s, terraform and imports, then render a diagram.

**متى:** User asks to draw the real system, review a PR's structural change, or detect drift.

**كيف:** 1. Scan package manifests, docker-compose, k8s, terraform, import graph. 2. Build a node/edge graph, cite sources. 3. Choose single-SVG hero (<=8 nodes) or widescreen docs layout. 4. Fill HTML template with inline SVG; emit Mermaid copy. 5. Modes: generate, diff a PR, trace a stack into a sequence, watch via fingerprint.

**المعاملات:** mode (generate\|diff\|trace\|watch), target path

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** architecture · repo · معمارية · drift

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `docker` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:mermaid` ← npm ls mermaid أو وجود node_modules/mermaid
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1722-engineer-design-diagram/4729-engineer-design-diagram`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2179-architecture-suite/7964-ln-25-architecture-diagram-builder`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/x4919-visual-gen/x20317-architecture-diagram`

#### 7. قدرات قريبة في العائلة

- `ADOCS-17` مخطط AWS بصيغة draw.io بأيقونات رسمية / AWS architecture draw.io with official icons (documented)
- `ADOCS-18` اختيار محرك المخططات: PlantUML أو D2 أو Structurizr / Diagram-as-code engine choice: PlantUML, D2, Structurizr (documented)
- `ADOCS-20` رسم Excalidraw يحمل حجة بصرية / Excalidraw diagram that argues visually (documented)
- `ADOCS-21` رسم مخططات Mermaid والتحقق منها / Mermaid diagram render and validate loop (documented)

### `ADOCS-20` — رسم Excalidraw يحمل حجة بصرية / Excalidraw diagram that argues visually

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** إنشاء ملف Excalidraw بأشكال معبرة وحلقة تصيير وإصلاح. — Create .excalidraw JSON using shape-as-meaning patterns, palette file and a render-fix loop.

**متى:** User asks to visualize a workflow, plan or concept in Excalidraw.

**كيف:** 1. Assess simple vs technical depth. 2. Research real formats for technical ones. 3. Map concepts to visual patterns; apply isomorphism test. 4. Generate JSON section by section using a color palette file. 5. Render, view, fix until clean.

**المعاملات:** depth, palette

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** excalidraw · whiteboard · سبورة · workflow

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2790-work/11181-draw-excalidraw`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2966-pwdev-excalidraw/12488-excalidraw`

#### 7. قدرات قريبة في العائلة

- `ADOCS-18` اختيار محرك المخططات: PlantUML أو D2 أو Structurizr / Diagram-as-code engine choice: PlantUML, D2, Structurizr (documented)
- `ADOCS-19` مخطط معماري مبني على الريبو الفعلي / Evidence-grounded architecture diagram from repo (documented)
- `ADOCS-21` رسم مخططات Mermaid والتحقق منها / Mermaid diagram render and validate loop (documented)
- `ADOCS-22` تخطيط الرسوم العقدية وتصميم UML / Node-link layout and UML diagram design (documented)

### `ADOCS-21` — رسم مخططات Mermaid والتحقق منها / Mermaid diagram render and validate loop

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** كتابة Mermaid وتصييره عبر mmdc وإصلاح الأخطاء حتى ينجح. — Write Mermaid markup, render with mmdc to SVG/PNG/PDF and fix syntax errors until it compiles.

**متى:** User wants flowchart, sequence, ER, class, state, Gantt or gitGraph as an image or in Markdown.

**كيف:** 1. Pick diagram type matching the question. 2. Write .mmd source. 3. Run mmdc -i in.mmd -o out.svg (or png/pdf). 4. On parse error, fix syntax and rerun. 5. Embed the fenced mermaid block in GitHub Markdown and keep the source versioned.

**المعاملات:** type, output format, theme

**التثبيت:** npm i -g @mermaid-js/mermaid-cli

**الوسوم:** mermaid · diagram · مخطط · render

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:mermaid` ← npm ls mermaid أو وجود node_modules/mermaid
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1245-mermaid-cli/2925-mermaid-cli`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2173-tools-plugin/7922-mermaid-diagrams`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3206-literature-publication/13573-markdown-mermaid-writing`

#### 7. قدرات قريبة في العائلة

- `ADOCS-19` مخطط معماري مبني على الريبو الفعلي / Evidence-grounded architecture diagram from repo (documented)
- `ADOCS-20` رسم Excalidraw يحمل حجة بصرية / Excalidraw diagram that argues visually (documented)
- `ADOCS-22` تخطيط الرسوم العقدية وتصميم UML / Node-link layout and UML diagram design (documented)
- `ADOCS-23` مخطط HTML مستقل بـ SVG مضمن / Self-contained HTML diagram with inline SVG (documented)

### `ADOCS-22` — تخطيط الرسوم العقدية وتصميم UML / Node-link layout and UML diagram design

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** اختيار استراتيجية تخطيط لتقليل التقاطعات وفق UML. — Choose auto-layout strategies and notation to reduce crossings in node-link and UML diagrams.

**متى:** User asks how to lay out or critique a diagram.

**كيف:** 1. Classify graph (tree, DAG, general). 2. Pick layered, force or tree layout. 3. Minimize crossings, align ranks, group clusters. 4. Use correct UML notation per type. 5. Review readability.

**المعاملات:** graph type

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** layout · uml · تخطيط · graph

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2690-build-web-data-visualization/10326-node-link-and-diagram-layout`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2690-build-web-data-visualization/10334-uml-and-software-architecture-visualizat`

#### 7. قدرات قريبة في العائلة

- `ADOCS-20` رسم Excalidraw يحمل حجة بصرية / Excalidraw diagram that argues visually (documented)
- `ADOCS-21` رسم مخططات Mermaid والتحقق منها / Mermaid diagram render and validate loop (documented)
- `ADOCS-23` مخطط HTML مستقل بـ SVG مضمن / Self-contained HTML diagram with inline SVG (documented)
- `ADOCS-24` خطة تنفيذ مرئية للمراجعة في المتصفح / Visual implementation plan reviewed in browser (documented)

### `ADOCS-23` — مخطط HTML مستقل بـ SVG مضمن / Self-contained HTML diagram with inline SVG

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / BSD-3-Clause; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** رسم مخطط في ملف HTML واحد بـ SVG مع حد للتعقيد. — Draw a diagram as one HTML file with inline SVG, orthogonal connectors and a complexity budget.

**متى:** User needs a shareable explanatory figure or schematic.

**كيف:** 1. Fix the question the figure answers. 2. Cap node count (complexity budget). 3. Use semantic colors, orthogonal arrows, boundaries dashed, store paths solid and lookups dashed. 4. Inline SVG, no external deps. 5. Check labels, contrast and reading order.

**المعاملات:** node cap, theme

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** svg · html · figure · شكل

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/345-visuals/1242-html-diagram`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2657-figures/10113-svg-figure`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1095-akbun-draw-architecture/2428-akbun-draw-architecture`

#### 7. قدرات قريبة في العائلة

- `ADOCS-21` رسم مخططات Mermaid والتحقق منها / Mermaid diagram render and validate loop (documented)
- `ADOCS-22` تخطيط الرسوم العقدية وتصميم UML / Node-link layout and UML diagram design (documented)
- `ADOCS-24` خطة تنفيذ مرئية للمراجعة في المتصفح / Visual implementation plan reviewed in browser (documented)
- `ADOCS-25` إنشاء ADR وRFC مع ترقيم وربط / ADR/RFC/PRD creation with ID linking (documented)

### `ADOCS-24` — خطة تنفيذ مرئية للمراجعة في المتصفح / Visual implementation plan reviewed in browser

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** كتابة الخطة بصيغة ماركداون وعرضها محليا بمخططات وجمع الملاحظات. — Write a plan as markdown, lint, serve locally with diagrams and collect comments.

**متى:** User wants to review a plan visually before code.

**كيف:** 1. Research, then inventory components, schema, endpoints. 2. Write markdown with tldr, summary, mermaid architecture, key changes. 3. Lint and fix findings. 4. Self-review rendered page. 5. Serve via bundled node server, read comments, repeat. Write for a non-developer executive.

**المعاملات:** doc dir

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** plan · review · خطة · docs

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:mermaid` ← npm ls mermaid أو وجود node_modules/mermaid
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2865-visual-docs/11574-visual-plan`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2199-lvtd-skills/8203-visual-docs-diagrams`

#### 7. قدرات قريبة في العائلة

- `ADOCS-22` تخطيط الرسوم العقدية وتصميم UML / Node-link layout and UML diagram design (documented)
- `ADOCS-23` مخطط HTML مستقل بـ SVG مضمن / Self-contained HTML diagram with inline SVG (documented)
- `ADOCS-25` إنشاء ADR وRFC مع ترقيم وربط / ADR/RFC/PRD creation with ID linking (documented)
- `ADOCS-26` تحديث التوثيق بالاعتماد على الكود / Code-grounded doc update and overhaul (documented)

### `ADOCS-25` — إنشاء ADR وRFC مع ترقيم وربط / ADR/RFC/PRD creation with ID linking

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تسجيل القرارات كـADR أو RFC وترقيم المستندات وربطها بالمشكلات. — Record decisions as ADR or RFC, assign sequential PRD/ADR/PRP IDs and link documents bidirectionally to issues.

**متى:** We decided X; should we switch to Y; documents lack IDs

**كيف:** 1 Classify: settled decision -> ADR, open proposal -> RFC, accepted RFC -> resolve into ADR. 2 Fill context, decision, consequences, status. 3 Scan docs/prds, adrs, prps for missing IDs; assign next number; update manifest. 4 Use --dry-run first. 5 Link ids to GitHub issues; detect opportunities in conversation.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** adr · rfc · prd · قرارات معمارية

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/341-archcore/1209-document`

#### 7. قدرات قريبة في العائلة

- `ADOCS-23` مخطط HTML مستقل بـ SVG مضمن / Self-contained HTML diagram with inline SVG (documented)
- `ADOCS-24` خطة تنفيذ مرئية للمراجعة في المتصفح / Visual implementation plan reviewed in browser (documented)
- `ADOCS-26` تحديث التوثيق بالاعتماد على الكود / Code-grounded doc update and overhaul (documented)
- `ADOCS-27` إعادة هيكلة التوثيق بإطار دياتاكسيس / Diataxis four-kind docs restructuring (documented)

### `ADOCS-26` — تحديث التوثيق بالاعتماد على الكود / Code-grounded doc update and overhaul

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تحديث أو إعادة كتابة الوثائق لقارئ محدد مع التحقق من كل ادعاء بالكود وفحص الروابط والمخططات. — Update or rewrite docs for a named reader, verifying every claim against code and running link, diagram and prose checks.

**متى:** A code change made docs stale; README or guide rewrite; API docs generation

**كيف:** 1 Choose Update vs Overhaul mode; scope from git diff --name-only. 2 Write ownership map: one reader, one job per doc, one owner per fact. 3 Read code/tests/config; docs conform to code unless doc is declared contract. 4 Replace adjectives with measured facts; generate sample output from real code. 5 Render mermaid diagrams and inspect. 6 Run link check and prose lint once. 7 Report unverified claims.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** docs-update · source-grounded · توثيق · تحقق

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `git` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:mermaid` ← npm ls mermaid أو وجود node_modules/mermaid
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/113-dev-flow/288-documenting-code`

#### 7. قدرات قريبة في العائلة

- `ADOCS-24` خطة تنفيذ مرئية للمراجعة في المتصفح / Visual implementation plan reviewed in browser (documented)
- `ADOCS-25` إنشاء ADR وRFC مع ترقيم وربط / ADR/RFC/PRD creation with ID linking (documented)
- `ADOCS-27` إعادة هيكلة التوثيق بإطار دياتاكسيس / Diataxis four-kind docs restructuring (documented)
- `ADOCS-28` تدقيق انحراف التوثيق عن الكود / Docs drift audit against current code (documented)

### `ADOCS-27` — إعادة هيكلة التوثيق بإطار دياتاكسيس / Diataxis four-kind docs restructuring

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تصنيف كل صفحة إلى تعليمي أو دليل مهمة أو مرجع أو شرح وفصل الصفحات المختلطة لتتبع رحلة القارئ. — Classify each page as tutorial, how-to, reference or explanation and split mixed pages so the docs set follows reader journeys.

**متى:** Docs feel muddled; planning a docs set; auditing information architecture

**كيف:** 1 List audiences (newcomer, integrator, operator). 2 Tag every page with one of four kinds. 3 Split pages mixing kinds. 4 Organize navigation by reader task, not module tree. 5 Keep one fact owner and link elsewhere. 6 Optionally pick a docs-as-code site tool (Docusaurus, Mintlify, MkDocs, Starlight) by needs.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** diataxis · docs-architecture · توثيق · هيكلة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2395-technical-writing-docs/9273-diataxis-documentation`

#### 7. قدرات قريبة في العائلة

- `ADOCS-25` إنشاء ADR وRFC مع ترقيم وربط / ADR/RFC/PRD creation with ID linking (documented)
- `ADOCS-26` تحديث التوثيق بالاعتماد على الكود / Code-grounded doc update and overhaul (documented)
- `ADOCS-28` تدقيق انحراف التوثيق عن الكود / Docs drift audit against current code (documented)
- `ADOCS-29` توثيق الدروس المستفادة من المشكلات المحلولة / Durable solved-problem learning notes (documented)

### `ADOCS-28` — تدقيق انحراف التوثيق عن الكود / Docs drift audit against current code

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** استخراج الادعاءات القابلة للتحقق من الوثائق ومطابقتها بالكود وتقرير التناقضات دون تعديل. — Extract falsifiable claims from README, CLAUDE.md and docs, check each against the repo, and report contradictions, stale items and orphans without editing.

**متى:** After many commits; docs may be stale; before release; takeover of unknown repo

**كيف:** 1 Inventory doc files and their reader. 2 Extract claims (paths, counts, commands, badges, versions). 3 Verify each against code/config via grep and git log. 4 Report as audit: inventory, findings, recommendations; user dispositions before any edit. 5 Optionally stamp a .docs-sync file with the audited commit SHA so drift is counted from there.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** docs-audit · drift · تدقيق · توثيق

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `git` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1554-gates/4320-docs-consolidate`

#### 7. قدرات قريبة في العائلة

- `ADOCS-26` تحديث التوثيق بالاعتماد على الكود / Code-grounded doc update and overhaul (documented)
- `ADOCS-27` إعادة هيكلة التوثيق بإطار دياتاكسيس / Diataxis four-kind docs restructuring (documented)
- `ADOCS-29` توثيق الدروس المستفادة من المشكلات المحلولة / Durable solved-problem learning notes (documented)
- `ADOCS-30` ويكي مترابط تديره النماذج / LLM-maintained interlinked wiki (documented)

### `ADOCS-29` — توثيق الدروس المستفادة من المشكلات المحلولة / Durable solved-problem learning notes

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** كتابة درس واحد موثق لكل مشكلة محلولة عندما لا يظهر المنطق في الكود. — Write one validated learning per solved problem under a solutions folder, only when reasoning is not recoverable from code.

**متى:** After verifying a non-obvious fix; changelog/knowledge capture

**كيف:** 1 Apply counterfactual bar: would losing this cause recurrence or rediscovery; else write nothing. 2 One learning per run. 3 Resolve docs root from config. 4 Research subagents write scratch only. 5 Orchestrator writes solutions doc with frontmatter, validates claims. 6 Update existing learning rather than duplicate.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** knowledge · learnings · معرفة · تسجيل

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1391-compound-engineering/3284-ce-compound`

#### 7. قدرات قريبة في العائلة

- `ADOCS-27` إعادة هيكلة التوثيق بإطار دياتاكسيس / Diataxis four-kind docs restructuring (documented)
- `ADOCS-28` تدقيق انحراف التوثيق عن الكود / Docs drift audit against current code (documented)
- `ADOCS-30` ويكي مترابط تديره النماذج / LLM-maintained interlinked wiki (documented)
- `ADOCS-31` البحث في توثيق المكتبات بالإصدار الصحيح / Look up version-correct library docs (documented)

### `ADOCS-30` — ويكي مترابط تديره النماذج / LLM-maintained interlinked wiki

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تحويل المصادر إلى قاعدة معرفة ماركداون مترابطة. — Ingest sources into a persistent cross-referenced markdown knowledge base in the Karpathy pattern.

**متى:** Second brain; Obsidian vault; knowledge base

**كيف:** 1 Ingest source into raw folder. 2 Write summary notes with wikilinks. 3 Update index and log. 4 Lint for orphans and contradictions.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** wiki · knowledge-base · ويكي · معرفة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `ADOCS-28` تدقيق انحراف التوثيق عن الكود / Docs drift audit against current code (documented)
- `ADOCS-29` توثيق الدروس المستفادة من المشكلات المحلولة / Durable solved-problem learning notes (documented)
- `ADOCS-31` البحث في توثيق المكتبات بالإصدار الصحيح / Look up version-correct library docs (documented)
- `ADOCS-32` ضغط الماركداون دون فقدان المعنى / Lossless markdown compression with semantic-diff gate (documented)

### `ADOCS-31` — البحث في توثيق المكتبات بالإصدار الصحيح / Look up version-correct library docs

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** الإجابة عن أسئلة API من التوثيق الرسمي للإصدار المثبت. — Answer API questions from official docs for the installed version via llms.txt or doc MCP rather than memory.

**متى:** Using a library; training data may be stale

**كيف:** 1 Read dependency version from lockfile. 2 Fetch official docs or llms.txt. 3 Cite source URL. 4 Record gotchas in a rule file.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** docs-lookup · llms-txt · توثيق · مكتبات

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `ADOCS-29` توثيق الدروس المستفادة من المشكلات المحلولة / Durable solved-problem learning notes (documented)
- `ADOCS-30` ويكي مترابط تديره النماذج / LLM-maintained interlinked wiki (documented)
- `ADOCS-32` ضغط الماركداون دون فقدان المعنى / Lossless markdown compression with semantic-diff gate (documented)
- `ADOCS-33` كتابة README والتحقق منه / README authoring and verification (documented)

### `ADOCS-32` — ضغط الماركداون دون فقدان المعنى / Lossless markdown compression with semantic-diff gate

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** حذف الحشو والتحوط من الوثائق مع مراجعة فروق تعيد أي معنى مفقود. — Cut filler, hedging and articles from docs while a second-pass diff review reverts any lost directive, threshold or example.

**متى:** Instruction files too long; token cost; tighten docs

**كيف:** 1 Snapshot original to temp dir. 2 Compress mechanically (flavor-vs-content matrix: cut filler/hedge/pleasantry, keep directives, qualifiers, numbers, examples). 3 Spawn reviewer comparing original vs condensed, listing semantic loss, ambiguity, false positives with citations. 4 Revert any loss. 5 Keep snapshot only on request.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** compression · tokens · ضغط · ماركداون

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2434-docs-hygiene/9448-compress`

#### 7. قدرات قريبة في العائلة

- `ADOCS-30` ويكي مترابط تديره النماذج / LLM-maintained interlinked wiki (documented)
- `ADOCS-31` البحث في توثيق المكتبات بالإصدار الصحيح / Look up version-correct library docs (documented)
- `ADOCS-33` كتابة README والتحقق منه / README authoring and verification (documented)
- `ADOCS-34` إزالة التعليقات الزائدة في الكود / Strip AI-slop and zero-info code comments (documented)

### `ADOCS-33` — كتابة README والتحقق منه / README authoring and verification

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** توليد README بكشف التقنيات والبيانات ثم التحقق من كل ادعاء ومسار وشارة. — Generate a front-door README by detecting stack and metadata, then verify every claim, path, count and badge against the repo.

**متى:** New repo; README stale; open-source release

**كيف:** 1 Detect stack, layout, license, scripts. 2 Gather missing metadata (logo, badges, features). 3 Draft sections: tagline, badges, features, install, usage, tech stack. 4 Verify each command and path exists. 5 Re-check after changes.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** readme · badges · توثيق · ريدمي

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `ADOCS-31` البحث في توثيق المكتبات بالإصدار الصحيح / Look up version-correct library docs (documented)
- `ADOCS-32` ضغط الماركداون دون فقدان المعنى / Lossless markdown compression with semantic-diff gate (documented)
- `ADOCS-34` إزالة التعليقات الزائدة في الكود / Strip AI-slop and zero-info code comments (documented)
- `ADOCS-35` كتابة سرد الألعاب المتفرع / Game narrative and branching writing (documented)

### `ADOCS-34` — إزالة التعليقات الزائدة في الكود / Strip AI-slop and zero-info code comments

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** حذف التعليقات التي تكرر الكود أو تصف طبقة أخرى والإبقاء على أسباب القرار. — Delete comments that restate code, describe another layer or narrate unshipped plans, keeping only why-comments and tool directives.

**متى:** Reviewer calls comment useless; cleaning agent-written code; PR cleanup

**كيف:** 1 Apply three-clause test: true at this layer, not visible in code, not stated better nearby. 2 Flag wrong-layer (noun absent from signature/body), redundant, planning narration. 3 Dissolve what-comments into better names. 4 Keep license, lint directives, doctests, generated API docs. 5 Do not merely shorten or abstract.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** comments · cleanup · تعليقات · جودة الكود

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1221-comment-slop/2903-comment-slop`

#### 7. قدرات قريبة في العائلة

- `ADOCS-32` ضغط الماركداون دون فقدان المعنى / Lossless markdown compression with semantic-diff gate (documented)
- `ADOCS-33` كتابة README والتحقق منه / README authoring and verification (documented)
- `ADOCS-35` كتابة سرد الألعاب المتفرع / Game narrative and branching writing (documented)
- `ADOCS-36` اختيار رقم الإصدار وكتابة سجل التغييرات / Semver bump and changelog plan (documented)

### `ADOCS-35` — كتابة سرد الألعاب المتفرع / Game narrative and branching writing

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** بناء سرد متفرع ومهمات وحوار. — Craft branching structure, quests, dialogue and lore bible.

**متى:** Writing game story.

**كيف:** 1) Architecture of branches. 2) Quest design. 3) Dialogue. 4) Lore bible. 5) Avoid AI tells.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** narrative · quest · سرد · حوار

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1376-velith/3219-book-game`

#### 7. قدرات قريبة في العائلة

- `ADOCS-33` كتابة README والتحقق منه / README authoring and verification (documented)
- `ADOCS-34` إزالة التعليقات الزائدة في الكود / Strip AI-slop and zero-info code comments (documented)
- `ADOCS-36` اختيار رقم الإصدار وكتابة سجل التغييرات / Semver bump and changelog plan (documented)
- `ADOCS-37` كتابة الرياضيات وشرحها المطوّل / Math notation and long-form exposition (documented)

### `ADOCS-36` — اختيار رقم الإصدار وكتابة سجل التغييرات / Semver bump and changelog plan

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT/Apache; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تحديد رفع الإصدار من التغييرات وكتابة سجل تغييرات وقائمة تحقق. — Pick the semver bump from the change set and write a Keep-a-Changelog entry plus checklist.

**متى:** Is this major/minor/patch, cut release, write changelog.

**كيف:** 1) git log last tag..HEAD. 2) Incompatible API change=major, feature=minor, fixes=patch; 0.x may break. 3) Group Added/Changed/Deprecated/Removed/Fixed/Security, breaking first with migration link. 4) Bump manifests consistently. 5) Checklist: CI green on exact SHA.

**المعاملات:** force bump, dry-run, from tag

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** semver · changelog · إصدار

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `git` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2346-open-source-maintenance/9025-plan-a-release`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3152-shipwright-changelog/13481-shipwright-changelog`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/964-release/2248-release`

#### 7. قدرات قريبة في العائلة

- `ADOCS-34` إزالة التعليقات الزائدة في الكود / Strip AI-slop and zero-info code comments (documented)
- `ADOCS-35` كتابة سرد الألعاب المتفرع / Game narrative and branching writing (documented)
- `ADOCS-37` كتابة الرياضيات وشرحها المطوّل / Math notation and long-form exposition (documented)
- `ADOCS-38` تقرير اختبار فهم بعد التغيير / Post-change comprehension quiz report (documented)

### `ADOCS-37` — كتابة الرياضيات وشرحها المطوّل / Math notation and long-form exposition

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يكتب الرياضيات برموز يونيكود وبراهين مفصلة. — Write math with Unicode notation and detailed understanding-focused proofs.

**متى:** Response needs equations in plain text or a deep math explanation.

**كيف:** 1) Prefer Unicode math in chat text. 2) Long-form exposition with motivation before proof. 3) Detailed steps.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** math · unicode · رياضيات · كتابة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3259-claude-math/13770-math-unicode`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1244-long-form-math/2924-long-form-math`

#### 7. قدرات قريبة في العائلة

- `ADOCS-35` كتابة سرد الألعاب المتفرع / Game narrative and branching writing (documented)
- `ADOCS-36` اختيار رقم الإصدار وكتابة سجل التغييرات / Semver bump and changelog plan (documented)
- `ADOCS-38` تقرير اختبار فهم بعد التغيير / Post-change comprehension quiz report (documented)
- `ADOCS-39` هيكل منهج ذاتي مع سجل تقييم / Self-study curriculum scaffold with assessment log (documented)

### `ADOCS-38` — تقرير اختبار فهم بعد التغيير / Post-change comprehension quiz report

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ينتج تقرير HTML لتغيير منجز مع اختبار يتأكد من فهم الإنسان. — Produce an HTML report of a finished change with a quiz checking the human understood it.

**متى:** After finishing a change, user says quiz me or asks what was done.

**كيف:** 1) Summarize context, intuition and decisions. 2) Build a self-contained HTML with questions at the bottom. 3) Test whether the user can explain the change to a reviewer. 4) A failed quiz signals intent mismatch before merge. 5) Do not use it to verify the artifact itself.

**المعاملات:** change scope

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** quiz · review · اختبار · فهم

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2437-education/9461-quiz-me`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2437-education/9463-teach`

#### 7. قدرات قريبة في العائلة

- `ADOCS-36` اختيار رقم الإصدار وكتابة سجل التغييرات / Semver bump and changelog plan (documented)
- `ADOCS-37` كتابة الرياضيات وشرحها المطوّل / Math notation and long-form exposition (documented)
- `ADOCS-39` هيكل منهج ذاتي مع سجل تقييم / Self-study curriculum scaffold with assessment log (documented)
- `ADOCS-40` مقال تعليمي من جلسة عمل / Teaching-block article from a working session (documented)

### `ADOCS-39` — هيكل منهج ذاتي مع سجل تقييم / Self-study curriculum scaffold with assessment log

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ينشئ منهجاً من وحدات مع سجل إجابات JSONL وتتبع تقدم. — Generate a modular curriculum with orientation, five-part modules, JSONL answer log and progress tracking.

**متى:** User asks for a curriculum, learning path, syllabus or study guide.

**كيف:** 1) Ask topic, goal, emphasis, level, output dir, module count (default 8-12). 2) Propose outline for approval: foundations, tools, application. 3) Scaffold with scripts/scaffold.py: README, 00-orientation, modules, final synthesis. 4) Log answers to responses.jsonl; recompute progress.md and misconceptions.md. 5) Write a synthesis prompt every 3 modules. 6) On return read MEMORY and progress.

**المعاملات:** topic, goal, level, modules

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** curriculum · syllabus · منهج · خطة دراسة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2524-curriculum/9821-curriculum`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1120-ambient-library/2575-design-course`

#### 7. قدرات قريبة في العائلة

- `ADOCS-37` كتابة الرياضيات وشرحها المطوّل / Math notation and long-form exposition (documented)
- `ADOCS-38` تقرير اختبار فهم بعد التغيير / Post-change comprehension quiz report (documented)
- `ADOCS-40` مقال تعليمي من جلسة عمل / Teaching-block article from a working session (documented)
- `ADOCS-41` شرح بصري مبسط جداً بأسلوب طفل / Zero-knowledge visual ELI5 explainer (documented)

### `ADOCS-40` — مقال تعليمي من جلسة عمل / Teaching-block article from a working session

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحول جلسة عمل إلى مقال تعليمي يحتوي المطالبات والأخطاء والاستدلال. — Convert a session into a publishable walkthrough with real prompts, wrong turns and reasoning.

**متى:** User says write this up as a teaching block or debrief this session.

**كيف:** 1) Collect real prompts, outputs and dead ends. 2) Follow instructions.md and references/writing-style.md. 3) Add diagrams and rendered HTML. 4) Keep reflective, educational tone.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** writeup · session · مقال · توثيق

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1120-ambient-library/2677-teaching-block-synthesized`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1120-ambient-library/2588-teaching-block`

#### 7. قدرات قريبة في العائلة

- `ADOCS-38` تقرير اختبار فهم بعد التغيير / Post-change comprehension quiz report (documented)
- `ADOCS-39` هيكل منهج ذاتي مع سجل تقييم / Self-study curriculum scaffold with assessment log (documented)
- `ADOCS-41` شرح بصري مبسط جداً بأسلوب طفل / Zero-knowledge visual ELI5 explainer (documented)
- `ADOCS-42` الكتابة البسيطة: كلمات يومية وجمل كاملة / Plain writing: everyday words, complete sentences (documented)

### `ADOCS-41` — شرح بصري مبسط جداً بأسلوب طفل / Zero-knowledge visual ELI5 explainer

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يشرح أي موضوع في صفحة HTML بصرية بنص قليل وفكرة واحدة لكل رسم. — Explain any topic as a minimal-text visual HTML with one idea per diagram.

**متى:** User types eli5, asks for dead-simple explanation of how something works.

**كيف:** 1) Assume zero prior knowledge. 2) One idea per diagram. 3) Minimal text and concrete analogies. 4) Render as self-contained HTML. 5) Works on a codebase or concept.

**المعاملات:** topic

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** eli5 · explainer · شرح · تبسيط

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2437-education/9459-eli5`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/257-eli5/864-eli5`

#### 7. قدرات قريبة في العائلة

- `ADOCS-39` هيكل منهج ذاتي مع سجل تقييم / Self-study curriculum scaffold with assessment log (documented)
- `ADOCS-40` مقال تعليمي من جلسة عمل / Teaching-block article from a working session (documented)
- `ADOCS-42` الكتابة البسيطة: كلمات يومية وجمل كاملة / Plain writing: everyday words, complete sentences (documented)
- `ADOCS-43` أنسنة النص بالكثافة لا بقائمة حذف / Humanize by density, with an over-correction guard (documented)

### `ADOCS-42` — الكتابة البسيطة: كلمات يومية وجمل كاملة / Plain writing: everyday words, complete sentences

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يكتب نصاً يُفهم من القراءة الأولى: كلمات شائعة، بلا مصطلحات مخترعة، بلا تفخيم فارغ، مع مثال قبل وبعد لكل قاعدة. — Writes text readable in one pass: common words, no invented jargon, no empty emphasis, with a before/after for each rule.

**متى:** اكتب ببساطة، نص واضح، بدون حشو / plain language, simple writing, remove fluff

**كيف:** 1) Prefer the common word; avoid words AI tools overuse (delve, tapestry, landscape, robust, leverage). 2) No jargon or invented shorthand; if a term is not in a standard dictionary, explain it. 3) Drop empty emphasis (really, pivotal, renowned, a testament to) and state the fact instead. 4) Complete sentences, one idea each, short paragraphs. 5) Revise by reading once as a newcomer and fixing every place you had to reread.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** writing · كتابة · plain · بسيط · clarity · وضوح

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2868-plain-writing/11578-plain-writing`

#### 7. قدرات قريبة في العائلة

- `ADOCS-40` مقال تعليمي من جلسة عمل / Teaching-block article from a working session (documented)
- `ADOCS-41` شرح بصري مبسط جداً بأسلوب طفل / Zero-knowledge visual ELI5 explainer (documented)
- `ADOCS-43` أنسنة النص بالكثافة لا بقائمة حذف / Humanize by density, with an over-correction guard (documented)
- `ADOCS-44` تدقيق انحراف التوثيق عن الكود لكل بُعد / Per-dimension documentation drift audit (documented)

### `ADOCS-43` — أنسنة النص بالكثافة لا بقائمة حذف / Humanize by density, with an over-correction guard

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يزيل علامات النص الآلي التي يلاحظها القراء (المفردات والبنية) بقياس كثافتها، دون وعد بتجاوز كاشفات الذكاء الاصطناعي. — Removes the AI tells readers notice (vocabulary, structure) by scoring their density, without promising to beat AI detectors.

**متى:** النص يبدو آلياً، أنسنة تغريدة / sounds like AI, humanize tweet, AI tells

**كيف:** 1) Readers mostly cite vocabulary and sentence structure as tells; target those. 2) Score suspect words by density per length instead of deleting a fixed list. 3) Cap em dashes rather than banning them; treat forced rhythm (triplets, staccato fragments) as a tell, not a fix. 4) Add an over-correction guard: do not strip natural phrasing or facts while removing tells. 5) Be honest that rewrites do not make text pass trained detectors; on short texts their scores are noise.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** humanizer · أنسنة · AI tells · writing · تغريدة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3035-x-skills/13066-x-humanizer`

#### 7. قدرات قريبة في العائلة

- `ADOCS-41` شرح بصري مبسط جداً بأسلوب طفل / Zero-knowledge visual ELI5 explainer (documented)
- `ADOCS-42` الكتابة البسيطة: كلمات يومية وجمل كاملة / Plain writing: everyday words, complete sentences (documented)
- `ADOCS-44` تدقيق انحراف التوثيق عن الكود لكل بُعد / Per-dimension documentation drift audit (documented)
- `ADOCS-45` الترجمة الإبداعية: متى نترجم ومتى نعيد الصياغة / Transcreation routing for marketing translation (documented)

### `ADOCS-44` — تدقيق انحراف التوثيق عن الكود لكل بُعد / Per-dimension documentation drift audit

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يقارن التوثيق بالكود الفعلي بُعداً بُعداً (الأوامر، الإعدادات، الواجهات…) ويخطط الإصلاح قبل التنفيذ. — Compares documentation with the actual code dimension by dimension (commands, config, APIs...) and plans fixes before executing them.

**متى:** التوثيق قديم، راجع ملفات README، تحديث الوثائق / outdated docs, docs drift, update README

**كيف:** 1) Inventory every doc. 2) For each dimension (install, commands, config keys, public API, architecture) check the claim against the code and record drift. 3) Plan: merge duplicates, surgical edits for outdated sections, link or archive orphans, fix broken references, add missing sections. 4) Ask before executing the plan. 5) After editing, verify no content was lost and links resolve.

**المعاملات:** dimensions

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** documentation · توثيق · README · drift · docs

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/60-codebase-mapper/95-docs-maintain-workflow`

#### 7. قدرات قريبة في العائلة

- `ADOCS-42` الكتابة البسيطة: كلمات يومية وجمل كاملة / Plain writing: everyday words, complete sentences (documented)
- `ADOCS-43` أنسنة النص بالكثافة لا بقائمة حذف / Humanize by density, with an over-correction guard (documented)
- `ADOCS-45` الترجمة الإبداعية: متى نترجم ومتى نعيد الصياغة / Transcreation routing for marketing translation (documented)

### `ADOCS-45` — الترجمة الإبداعية: متى نترجم ومتى نعيد الصياغة / Transcreation routing for marketing translation

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-docs` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-docs.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يفرز في النص ما يحتاج ترجمة حرفية وما يحتاج إعادة إبداع (تعابير، تلاعب لفظي، فكاهة)، مع قائمة كلمات لا تُترجم. — Sorts what needs literal translation from what needs transcreation (idioms, wordplay, humour), with a do-not-translate list.

**متى:** ترجمة تسويقية، ترجمة إعلان، تعريب / marketing translation, transcreation, localize ad copy

**كيف:** 1) Inputs: content, target languages (codes or names), optional source language, formality, do-not-translate terms. 2) Flag idioms, wordplay, humour, cultural references and emotional hooks for transcreation instead of literal translation. 3) Keep brand and product names in the source language. 4) Route each language pair to the tool that handles it best and record why. 5) Quality-check meaning, tone and length; numbers, names and dates must survive (see KOSIF anchor_gate).

**المعاملات:** formality, DNT list

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** translation · ترجمة · localization · تعريب · transcreation

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:ADOCS-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1520-digital-marketing-pro/4128-translate-content`

#### 7. قدرات قريبة في العائلة

- `ADOCS-43` أنسنة النص بالكثافة لا بقائمة حذف / Humanize by density, with an over-correction guard (documented)
- `ADOCS-44` تدقيق انحراف التوثيق عن الكود لكل بُعد / Per-dimension documentation drift audit (documented)

