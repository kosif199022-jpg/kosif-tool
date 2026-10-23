# `atlas-research` — البحث والمعرفة (9 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/atlas-research.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/research.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`AWEB-01` جلب بيانات يوتيوب بدون حصص](#aweb-01--جلب-بيانات-يوتيوب-بدون-حصص--zero-quota-youtube-data-lookup-via-proxy-api)
- [`AWEB-02` جلب ثابت أولا ثم احتياط المتصفح](#aweb-02--جلب-ثابت-أولا-ثم-احتياط-المتصفح--static-first-scrape-with-headless-browser-fallback)
- [`AWEB-03` بوابة الشرعية قبل جمع البيانات](#aweb-03--بوابة-الشرعية-قبل-جمع-البيانات--scraping-legality-gate-before-fetch)
- [`AWEB-04` ترميز نوعي قابل للتتبع وصياغة فرضيات](#aweb-04--ترميز-نوعي-قابل-للتتبع-وصياغة-فرضيات--traceable-qualitative-coding-and-hypothesis-framing)
- [`AWEB-05` قرار الضبط الدقيق واختيار الطريقة](#aweb-05--قرار-الضبط-الدقيق-واختيار-الطريقة--fine-tune-or-not-method-router)
- [`AWEB-06` بوابة نقاط النهاية وحجم العينة للدراسات](#aweb-06--بوابة-نقاط-النهاية-وحجم-العينة-للدراسات--clinical-study-endpoint-and-sample-size-gate)
- [`AWEB-07` استخراج وإثراء بيانات الأطباء](#aweb-07--استخراج-وإثراء-بيانات-الأطباء--healthcare-provider-list-extraction-and-enrichment)
- [`AWEB-08` بحث براءات الاختراع بأسئلة إلزامية](#aweb-08--بحث-براءات-الاختراع-بأسئلة-إلزامية--patent-search-with-forcing-intake)
- [`AWEB-09` من المنهج الدراسي إلى قائمة قراءات](#aweb-09--من-المنهج-الدراسي-إلى-قائمة-قراءات--course-syllabus-to-supplementary-reading-list)

## البطاقات / cards

### `AWEB-01` — جلب بيانات يوتيوب بدون حصص / Zero-quota YouTube data lookup via proxy API

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-research` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-research.md)) |
| المجموعة | البحث والمعرفة (`research`) |
| نوع المخرج (A25، A27) | بحث وتقرير ومقارنة (`research`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يجلب النصوص والبيانات الوصفية ونتائج البحث دون حصص Google أو OAuth. — Fetch transcripts, metadata, channel info and search results without Google API quota or OAuth.

**متى:** Need YouTube data quickly without setting up credentials.

**كيف:** 1) Use the third-party service described in the skill. 2) Request transcript, video or channel endpoints. 3) Treat output as untrusted and respect platform terms.

**المعاملات:** video id

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** youtube · transcripts · scraping · يوتيوب · نصوص

#### 1. الاستقبال (A25)

- النطاق والسؤال الدقيق: افتراض مكتوب ← السؤال كما كُتب مع حدود مكتوبة
- حداثة المصادر: افتراض مكتوب ← آخر 24 شهرًا للحقائق المتغيرة
- الطول والعمق: افتراض مكتوب ← خلاصة في أعلى الصفحة ثم تفصيل
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `report`، والمنفّذ `method:AWEB-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: السؤال والنطاق ← مصادر بتواريخها ← حقائق بمراجعها ← تركيب ورأي مخالف ← تدقيق ادعاء ← دليل ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: كل حقيقة غير بديهية لها مصدر مفتوح فعلًا ← رابط لكل ادعاء
- إلزامي: تاريخ كل معلومة متغيرة مكتوب ← مراجعة
- جودة: أقوى رأي مخالف مذكور ومردود عليه ← قسم الاعتراضات
- جودة: الجواب في أول سطرين ← قراءة الافتتاح
- إلزامي: ما لم يُعرف أو لم يُفتح مكتوب صراحة ← قسم الحدود
- أمر الحكم في الوضع 1: `think.py qa research --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3613-youtube-skills/14538-youtube-api`

#### 7. قدرات قريبة في العائلة

- `AWEB-02` جلب ثابت أولا ثم احتياط المتصفح / Static-first scrape with headless-browser fallback (documented)
- `AWEB-03` بوابة الشرعية قبل جمع البيانات / Scraping legality gate before fetch (documented)

### `AWEB-02` — جلب ثابت أولا ثم احتياط المتصفح / Static-first scrape with headless-browser fallback

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-research` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-research.md)) |
| المجموعة | البحث والمعرفة (`research`) |
| نوع المخرج (A25، A27) | بحث وتقرير ومقارنة (`research`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** جلب الصفحة ثابتا أولا ثم التصعيد لمتصفح بلا واجهة فقط عند صفحات JS أو الحماية. — Fetch statically first and escalate to headless Chrome only when the page is a JS shell or WAF-blocked.

**متى:** Static fetch returns empty or stub content; SPA, infinite scroll, interstitials.

**كيف:** 1) Try static fetch. 2) Check for near-empty body, noscript warnings, WAF vendor fingerprints. 3) Re-fetch with browser mode auto\|always\|never (always for known SPAs, never in hot loops or sandboxes). 4) Optionally attach external CDP endpoint. 5) Inspect content and warnings fields before trusting result. 6) Script clicks/scroll/wait before extraction when interaction is needed.

**المعاملات:** browser-mode, endpoint

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** scraping · SPA · جلب · ويب

#### 1. الاستقبال (A25)

- النطاق والسؤال الدقيق: افتراض مكتوب ← السؤال كما كُتب مع حدود مكتوبة
- حداثة المصادر: افتراض مكتوب ← آخر 24 شهرًا للحقائق المتغيرة
- الطول والعمق: افتراض مكتوب ← خلاصة في أعلى الصفحة ثم تفصيل
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `report`، والمنفّذ `method:AWEB-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: السؤال والنطاق ← مصادر بتواريخها ← حقائق بمراجعها ← تركيب ورأي مخالف ← تدقيق ادعاء ← دليل ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: كل حقيقة غير بديهية لها مصدر مفتوح فعلًا ← رابط لكل ادعاء
- إلزامي: تاريخ كل معلومة متغيرة مكتوب ← مراجعة
- جودة: أقوى رأي مخالف مذكور ومردود عليه ← قسم الاعتراضات
- جودة: الجواب في أول سطرين ← قراءة الافتتاح
- إلزامي: ما لم يُعرف أو لم يُفتح مكتوب صراحة ← قسم الحدود
- أمر الحكم في الوضع 1: `think.py qa research --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2101-crawlberg/7459-headless-fallback`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2101-crawlberg/7456-automating-the-browser`

#### 7. قدرات قريبة في العائلة

- `AWEB-01` جلب بيانات يوتيوب بدون حصص / Zero-quota YouTube data lookup via proxy API (documented)
- `AWEB-03` بوابة الشرعية قبل جمع البيانات / Scraping legality gate before fetch (documented)
- `AWEB-04` ترميز نوعي قابل للتتبع وصياغة فرضيات / Traceable qualitative coding and hypothesis framing (documented)

### `AWEB-03` — بوابة الشرعية قبل جمع البيانات / Scraping legality gate before fetch

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-research` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-research.md)) |
| المجموعة | البحث والمعرفة (`research`) |
| نوع المخرج (A25، A27) | بحث وتقرير ومقارنة (`research`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ينفذ قائمة فحص قانونية وأخلاقية (robots وشروط الاستخدام والمصادقة والمعدل والبيانات الشخصية) قبل كتابة أي كاشط. — Run a legal and ethical checklist (robots.txt, terms, auth, rate, PII) before writing any scraper.

**متى:** User asks to scrape or crawl a site.

**كيف:** 1) Check robots.txt. 2) Read ToS. 3) Public vs authenticated. 4) Set polite rate. 5) Flag PII and copyright. 6) Choose fetch strategy only after gate passes.

**المعاملات:** target site

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** scraping · robots · legal · جمع البيانات · أخلاقيات

#### 1. الاستقبال (A25)

- النطاق والسؤال الدقيق: افتراض مكتوب ← السؤال كما كُتب مع حدود مكتوبة
- حداثة المصادر: افتراض مكتوب ← آخر 24 شهرًا للحقائق المتغيرة
- الطول والعمق: افتراض مكتوب ← خلاصة في أعلى الصفحة ثم تفصيل
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `report`، والمنفّذ `method:AWEB-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: السؤال والنطاق ← مصادر بتواريخها ← حقائق بمراجعها ← تركيب ورأي مخالف ← تدقيق ادعاء ← دليل ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: كل حقيقة غير بديهية لها مصدر مفتوح فعلًا ← رابط لكل ادعاء
- إلزامي: تاريخ كل معلومة متغيرة مكتوب ← مراجعة
- جودة: أقوى رأي مخالف مذكور ومردود عليه ← قسم الاعتراضات
- جودة: الجواب في أول سطرين ← قراءة الافتتاح
- إلزامي: ما لم يُعرف أو لم يُفتح مكتوب صراحة ← قسم الحدود
- أمر الحكم في الوضع 1: `think.py qa research --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2407-web-scraping-data-extraction/9331-legal-ethical-and-fetch-strategy`

#### 7. قدرات قريبة في العائلة

- `AWEB-01` جلب بيانات يوتيوب بدون حصص / Zero-quota YouTube data lookup via proxy API (documented)
- `AWEB-02` جلب ثابت أولا ثم احتياط المتصفح / Static-first scrape with headless-browser fallback (documented)
- `AWEB-04` ترميز نوعي قابل للتتبع وصياغة فرضيات / Traceable qualitative coding and hypothesis framing (documented)
- `AWEB-05` قرار الضبط الدقيق واختيار الطريقة / Fine-tune or not: method router (documented)

### `AWEB-04` — ترميز نوعي قابل للتتبع وصياغة فرضيات / Traceable qualitative coding and hypothesis framing

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-research` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-research.md)) |
| المجموعة | البحث والمعرفة (`research`) |
| نوع المخرج (A25، A27) | بحث وتقرير ومقارنة (`research`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ابن دليل ترميز مع مقتطفات محفوظة وصغ فرضيات محدودة مع تفسيرات منافسة. — Build a codebook with preserved excerpts and formulate bounded hypotheses with rival explanations.

**متى:** Interviews, open-ended responses, research design.

**كيف:** 1) Draft codebook with definitions. 2) Code excerpts, keep source references. 3) Track inter-coder agreement. 4) Distinguish associational vs causal claims. 5) List rival explanations and discriminating predictions.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** qualitative · codebook · نوعي

#### 1. الاستقبال (A25)

- النطاق والسؤال الدقيق: افتراض مكتوب ← السؤال كما كُتب مع حدود مكتوبة
- حداثة المصادر: افتراض مكتوب ← آخر 24 شهرًا للحقائق المتغيرة
- الطول والعمق: افتراض مكتوب ← خلاصة في أعلى الصفحة ثم تفصيل
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `report`، والمنفّذ `method:AWEB-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: السؤال والنطاق ← مصادر بتواريخها ← حقائق بمراجعها ← تركيب ورأي مخالف ← تدقيق ادعاء ← دليل ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: كل حقيقة غير بديهية لها مصدر مفتوح فعلًا ← رابط لكل ادعاء
- إلزامي: تاريخ كل معلومة متغيرة مكتوب ← مراجعة
- جودة: أقوى رأي مخالف مذكور ومردود عليه ← قسم الاعتراضات
- جودة: الجواب في أول سطرين ← قراءة الافتتاح
- إلزامي: ما لم يُعرف أو لم يُفتح مكتوب صراحة ← قسم الحدود
- أمر الحكم في الوضع 1: `think.py qa research --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3208-qualitative-research/13577-qualitative-analysis`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3209-research-design/13579-hypothesis-generation`

#### 7. قدرات قريبة في العائلة

- `AWEB-02` جلب ثابت أولا ثم احتياط المتصفح / Static-first scrape with headless-browser fallback (documented)
- `AWEB-03` بوابة الشرعية قبل جمع البيانات / Scraping legality gate before fetch (documented)
- `AWEB-05` قرار الضبط الدقيق واختيار الطريقة / Fine-tune or not: method router (documented)
- `AWEB-06` بوابة نقاط النهاية وحجم العينة للدراسات / Clinical study endpoint and sample-size gate (documented)

### `AWEB-05` — قرار الضبط الدقيق واختيار الطريقة / Fine-tune or not: method router

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-research` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-research.md)) |
| المجموعة | البحث والمعرفة (`research`) |
| نوع المخرج (A25، A27) | بحث وتقرير ومقارنة (`research`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تقرير هل نضبط النموذج وتوجيه إلى الطريقة المناسبة حسب البيانات وحجم النص. — Decide whether to fine-tune and route to SFT, DPO, GRPO or CPT by data type and text volume.

**متى:** Starting any fine-tuning effort or choosing RAG vs training.

**كيف:** 1) Volatile facts: RAG. 2) Unsettled behavior: prompting. 3) Domain text <10MB RAG; 10-500MB RAG+FT; 0.5-10GB CPT then SFT; >10GB CPT. 4) Demonstrations: SFT; preference pairs: DPO/ORPO/KTO; verifiable reward: GRPO/RLVR. 5) CPT LR about 10% of pretraining LR. 6) No eval harness: build it first. Then export merged/quantized.

**المعاملات:** domain text volume

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** finetuning · sft · dpo · ضبط

#### 1. الاستقبال (A25)

- النطاق والسؤال الدقيق: افتراض مكتوب ← السؤال كما كُتب مع حدود مكتوبة
- حداثة المصادر: افتراض مكتوب ← آخر 24 شهرًا للحقائق المتغيرة
- الطول والعمق: افتراض مكتوب ← خلاصة في أعلى الصفحة ثم تفصيل
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:chromadb` ← python3 -c "import chromadb" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `report`، والمنفّذ `method:AWEB-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: السؤال والنطاق ← مصادر بتواريخها ← حقائق بمراجعها ← تركيب ورأي مخالف ← تدقيق ادعاء ← دليل ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: كل حقيقة غير بديهية لها مصدر مفتوح فعلًا ← رابط لكل ادعاء
- إلزامي: تاريخ كل معلومة متغيرة مكتوب ← مراجعة
- جودة: أقوى رأي مخالف مذكور ومردود عليه ← قسم الاعتراضات
- جودة: الجواب في أول سطرين ← قراءة الافتتاح
- إلزامي: ما لم يُعرف أو لم يُفتح مكتوب صراحة ← قسم الحدود
- أمر الحكم في الوضع 1: `think.py qa research --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3104-llm-finetuning/13289-finetuning-method-selection`

#### 7. قدرات قريبة في العائلة

- `AWEB-03` بوابة الشرعية قبل جمع البيانات / Scraping legality gate before fetch (documented)
- `AWEB-04` ترميز نوعي قابل للتتبع وصياغة فرضيات / Traceable qualitative coding and hypothesis framing (documented)
- `AWEB-06` بوابة نقاط النهاية وحجم العينة للدراسات / Clinical study endpoint and sample-size gate (documented)
- `AWEB-07` استخراج وإثراء بيانات الأطباء / Healthcare provider list extraction and enrichment (documented)

### `AWEB-06` — بوابة نقاط النهاية وحجم العينة للدراسات / Clinical study endpoint and sample-size gate

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-research` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-research.md)) |
| المجموعة | البحث والمعرفة (`research`) |
| نوع المخرج (A25، A27) | بحث وتقرير ومقارنة (`research`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تقييم نقاط النهاية وتقدير حجم العينة وإصدار قرار جاهزية للدراسة. — Score endpoints, estimate two-arm sample size and score study feasibility into a go/no-go packet.

**متى:** Designing a prospective study before submission.

**كيف:** 1) Fill protocol synopsis template. 2) endpoint_selector: 5 weighted dimensions, classify primary/key-secondary/exploratory, flag surrogates. 3) sample_size_estimator for means (Cohen d), proportions, survival (Schoenfeld) with sourced effect size. 4) phase_gate_scorer 0-100 giving GO / GO-WITH-CONDITIONS / REDESIGN / NO-GO plus owners. 5) Route to biostatistician and medical monitor; output is advisory.

**المعاملات:** design, effect size, alpha, power

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** clinical · power · sample-size · تجارب سريرية

#### 1. الاستقبال (A25)

- النطاق والسؤال الدقيق: افتراض مكتوب ← السؤال كما كُتب مع حدود مكتوبة
- حداثة المصادر: افتراض مكتوب ← آخر 24 شهرًا للحقائق المتغيرة
- الطول والعمق: افتراض مكتوب ← خلاصة في أعلى الصفحة ثم تفصيل
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `report`، والمنفّذ `method:AWEB-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: السؤال والنطاق ← مصادر بتواريخها ← حقائق بمراجعها ← تركيب ورأي مخالف ← تدقيق ادعاء ← دليل ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: كل حقيقة غير بديهية لها مصدر مفتوح فعلًا ← رابط لكل ادعاء
- إلزامي: تاريخ كل معلومة متغيرة مكتوب ← مراجعة
- جودة: أقوى رأي مخالف مذكور ومردود عليه ← قسم الاعتراضات
- جودة: الجواب في أول سطرين ← قراءة الافتتاح
- إلزامي: ما لم يُعرف أو لم يُفتح مكتوب صراحة ← قسم الحدود
- أمر الحكم في الوضع 1: `think.py qa research --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/217-research-ops-skills/690-clinical-research`

#### 7. قدرات قريبة في العائلة

- `AWEB-04` ترميز نوعي قابل للتتبع وصياغة فرضيات / Traceable qualitative coding and hypothesis framing (documented)
- `AWEB-05` قرار الضبط الدقيق واختيار الطريقة / Fine-tune or not: method router (documented)
- `AWEB-07` استخراج وإثراء بيانات الأطباء / Healthcare provider list extraction and enrichment (documented)
- `AWEB-08` بحث براءات الاختراع بأسئلة إلزامية / Patent search with forcing intake (documented)

### `AWEB-07` — استخراج وإثراء بيانات الأطباء / Healthcare provider list extraction and enrichment

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-research` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-research.md)) |
| المجموعة | البحث والمعرفة (`research`) |
| نوع المخرج (A25، A27) | بحث وتقرير ومقارنة (`research`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** استخراج بيانات الممارسين وإكمال الحقول الناقصة. — Extract practitioners from practice sites and fill missing contact, credential and regulatory fields.

**متى:** Building or cleaning a provider list.

**كيف:** 1) Crawl practice page for names, credentials, specialties. 2) Enrich gaps via search. 3) Return structured table.

**المعاملات:** list

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** providers · scraping · enrich · أطباء

#### 1. الاستقبال (A25)

- النطاق والسؤال الدقيق: افتراض مكتوب ← السؤال كما كُتب مع حدود مكتوبة
- حداثة المصادر: افتراض مكتوب ← آخر 24 شهرًا للحقائق المتغيرة
- الطول والعمق: افتراض مكتوب ← خلاصة في أعلى الصفحة ثم تفصيل
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `report`، والمنفّذ `method:AWEB-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: السؤال والنطاق ← مصادر بتواريخها ← حقائق بمراجعها ← تركيب ورأي مخالف ← تدقيق ادعاء ← دليل ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: كل حقيقة غير بديهية لها مصدر مفتوح فعلًا ← رابط لكل ادعاء
- إلزامي: تاريخ كل معلومة متغيرة مكتوب ← مراجعة
- جودة: أقوى رأي مخالف مذكور ومردود عليه ← قسم الاعتراضات
- جودة: الجواب في أول سطرين ← قراءة الافتتاح
- إلزامي: ما لم يُعرف أو لم يُفتح مكتوب صراحة ← قسم الحدود
- أمر الحكم في الوضع 1: `think.py qa research --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2666-nimble/10153-healthcare-providers-enrich`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2666-nimble/10154-healthcare-providers-extract`

#### 7. قدرات قريبة في العائلة

- `AWEB-05` قرار الضبط الدقيق واختيار الطريقة / Fine-tune or not: method router (documented)
- `AWEB-06` بوابة نقاط النهاية وحجم العينة للدراسات / Clinical study endpoint and sample-size gate (documented)
- `AWEB-08` بحث براءات الاختراع بأسئلة إلزامية / Patent search with forcing intake (documented)
- `AWEB-09` من المنهج الدراسي إلى قائمة قراءات / Course syllabus to supplementary reading list (documented)

### `AWEB-08` — بحث براءات الاختراع بأسئلة إلزامية / Patent search with forcing intake

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-research` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-research.md)) |
| المجموعة | البحث والمعرفة (`research`) |
| نوع المخرج (A25، A27) | بحث وتقرير ومقارنة (`research`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** فرض اختيار هدف واحد للبحث والولايات القضائية قبل بدء البحث. — Force a single search purpose and jurisdictions before running prior-art, FTO, landscape, diligence or invalidity searches.

**متى:** Patent novelty, freedom-to-operate or competitor landscape request.

**كيف:** 1) Q1 precise invention description; reject vague answers once. 2) Q2 pick one of five sub-use-cases. 3) Q3 jurisdictions (US/EP/CN/JP/KR/PCT) for FTO, landscape, diligence. 4) Extract concepts and keywords. 5) Search per path strategy, report with caveats and no legal advice.

**المعاملات:** invention, purpose, jurisdictions

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** patent · prior-art · FTO · براءات

#### 1. الاستقبال (A25)

- النطاق والسؤال الدقيق: افتراض مكتوب ← السؤال كما كُتب مع حدود مكتوبة
- حداثة المصادر: افتراض مكتوب ← آخر 24 شهرًا للحقائق المتغيرة
- الطول والعمق: افتراض مكتوب ← خلاصة في أعلى الصفحة ثم تفصيل
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `report`، والمنفّذ `method:AWEB-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: السؤال والنطاق ← مصادر بتواريخها ← حقائق بمراجعها ← تركيب ورأي مخالف ← تدقيق ادعاء ← دليل ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: كل حقيقة غير بديهية لها مصدر مفتوح فعلًا ← رابط لكل ادعاء
- إلزامي: تاريخ كل معلومة متغيرة مكتوب ← مراجعة
- جودة: أقوى رأي مخالف مذكور ومردود عليه ← قسم الاعتراضات
- جودة: الجواب في أول سطرين ← قراءة الافتتاح
- إلزامي: ما لم يُعرف أو لم يُفتح مكتوب صراحة ← قسم الحدود
- أمر الحكم في الوضع 1: `think.py qa research --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/224-patent/701-patent`

#### 7. قدرات قريبة في العائلة

- `AWEB-06` بوابة نقاط النهاية وحجم العينة للدراسات / Clinical study endpoint and sample-size gate (documented)
- `AWEB-07` استخراج وإثراء بيانات الأطباء / Healthcare provider list extraction and enrichment (documented)
- `AWEB-09` من المنهج الدراسي إلى قائمة قراءات / Course syllabus to supplementary reading list (documented)

### `AWEB-09` — من المنهج الدراسي إلى قائمة قراءات / Course syllabus to supplementary reading list

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-research` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-research.md)) |
| المجموعة | البحث والمعرفة (`research`) |
| نوع المخرج (A25، A27) | بحث وتقرير ومقارنة (`research`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يبني قائمة قراءات docx بأحدث الأوراق لكل قسم من المنهج. — Build a docx reading list of recent papers per syllabus section via academic search.

**متى:** Instructor or student supplies a syllabus.

**كيف:** 1) Intake: syllabus format and course level. 2) Split syllabus into sections. 3) Query Consensus MCP per section for recent peer-reviewed papers. 4) Assemble with scripts/generate_reading_list.js (node docx). 5) Deliver .docx.

**المعاملات:** syllabus file

**التثبيت:** npm i docx

**الوسوم:** syllabus · reading list · docx · قراءات

#### 1. الاستقبال (A25)

- النطاق والسؤال الدقيق: افتراض مكتوب ← السؤال كما كُتب مع حدود مكتوبة
- حداثة المصادر: افتراض مكتوب ← آخر 24 شهرًا للحقائق المتغيرة
- الطول والعمق: افتراض مكتوب ← خلاصة في أعلى الصفحة ثم تفصيل
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `report`، والمنفّذ `method:AWEB-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: السؤال والنطاق ← مصادر بتواريخها ← حقائق بمراجعها ← تركيب ورأي مخالف ← تدقيق ادعاء ← دليل ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: كل حقيقة غير بديهية لها مصدر مفتوح فعلًا ← رابط لكل ادعاء
- إلزامي: تاريخ كل معلومة متغيرة مكتوب ← مراجعة
- جودة: أقوى رأي مخالف مذكور ومردود عليه ← قسم الاعتراضات
- جودة: الجواب في أول سطرين ← قراءة الافتتاح
- إلزامي: ما لم يُعرف أو لم يُفتح مكتوب صراحة ← قسم الحدود
- أمر الحكم في الوضع 1: `think.py qa research --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/227-syllabus/704-syllabus`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2451-knowledge/9499-course-digest`

#### 7. قدرات قريبة في العائلة

- `AWEB-07` استخراج وإثراء بيانات الأطباء / Healthcare provider list extraction and enrichment (documented)
- `AWEB-08` بحث براءات الاختراع بأسئلة إلزامية / Patent search with forcing intake (documented)

