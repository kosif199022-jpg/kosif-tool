# `atlas-data` — البيانات والرسوم والمواقع (47 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/atlas-data.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/data.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`ADATA-01` خطوط معالجة آمنة التكرار وملء رجعي مضبوط](#adata-01--خطوط-معالجة-آمنة-التكرار-وملء-رجعي-مضبوط--idempotent-pipeline-steps-retries-and-safe-backfills)
- [`ADATA-02` استخراج الأنماط السيئة من سجلات جلسات الوكلاء](#adata-02--استخراج-الأنماط-السيئة-من-سجلات-جلسات-الوكلاء--mine-agent-session-logs-for-anti-patterns)
- [`ADATA-03` نشر استعلام محفوظ كنقطة API](#adata-03--نشر-استعلام-محفوظ-كنقطة-api--expose-saved-query-as-api-endpoint)
- [`ADATA-04` مطابقة الطلبات بين CRM وأدوات التحليل](#adata-04--مطابقة-الطلبات-بين-crm-وأدوات-التحليل--reconcile-leads-across-crm-and-analytics)
- [`ADATA-05` أدوات تحليل سوق الكريبتو وDeFi](#adata-05--أدوات-تحليل-سوق-الكريبتو-وdefi--crypto-market-and-defi-analytics-cli-suite)
- [`ADATA-06` ضرائب الكريبتو بطرق FIFO وLIFO وHIFO](#adata-06--ضرائب-الكريبتو-بطرق-fifo-وlifo-وhifo--crypto-tax-gains-with-fifo-lifo-hifo)
- [`ADATA-07` تحليل بيانات السلسلة والمحفظة وندرة NFT](#adata-07--تحليل-بيانات-السلسلة-والمحفظة-وندرة-nft--on-chain-data-portfolio-and-nft-rarity-analysis)
- [`ADATA-08` استقبال الفواتير والإيصالات وأرشفتها](#adata-08--استقبال-الفواتير-والإيصالات-وأرشفتها--invoice-and-receipt-intake-into-archive)
- [`ADATA-09` نمذجة مونت كارلو وسيناريوهات ماذا لو](#adata-09--نمذجة-مونت-كارلو-وسيناريوهات-ماذا-لو--monte-carlo-and-what-if-scenario-modeling)
- [`ADATA-10` تحليل النسب والانحرافات والتوقع المتجدد](#adata-10--تحليل-النسب-والانحرافات-والتوقع-المتجدد--ratio-analysis-variance-and-rolling-forecast)
- [`ADATA-11` مقاييس خط المبيعات وكفاءة الدخول للسوق](#adata-11--مقاييس-خط-المبيعات-وكفاءة-الدخول-للسوق--saas-pipeline-and-gtm-efficiency-metrics)
- [`ADATA-12` محاسبة الأعمال الصغيرة: رواتب وضرائب وتحصيل](#adata-12--محاسبة-الأعمال-الصغيرة-رواتب-وضرائب-وتحصيل--small-business-bookkeeping-payroll-tax-invoice-chase)
- [`ADATA-13` تحليل نتائج اختبار A/B مع حجم الأثر](#adata-13--تحليل-نتائج-اختبار-ab-مع-حجم-الأثر--ab-test-result-analysis-with-effect-sizes)
- [`ADATA-14` تخطيط حجم العينة وقوة اختبار A/B](#adata-14--تخطيط-حجم-العينة-وقوة-اختبار-ab--ab-test-sample-size-and-power-planning)
- [`ADATA-15` تخطيط القدرة الإحصائية وحجم العينة](#adata-15--تخطيط-القدرة-الإحصائية-وحجم-العينة--a-priori-power-and-sample-size-planning)
- [`ADATA-16` استكشاف البيانات الآمن المحدود](#adata-16--استكشاف-البيانات-الآمن-المحدود--bounded-safe-exploratory-data-profiling)
- [`ADATA-17` تشخيص الأفواج والاحتفاظ ومسار التحويل](#adata-17--تشخيص-الأفواج-والاحتفاظ-ومسار-التحويل--cohort-retention-and-funnel-diagnosis)
- [`ADATA-18` تدقيق جودة البيانات مع خطة إصلاح](#adata-18--تدقيق-جودة-البيانات-مع-خطة-إصلاح--dataset-quality-audit-with-scored-remediation-plan)
- [`ADATA-19` قراءة نتائج تجربة A/B بحكم قابل للدفاع](#adata-19--قراءة-نتائج-تجربة-ab-بحكم-قابل-للدفاع--defensible-ab-experiment-readout-and-verdict)
- [`ADATA-20` توقع الطلب مع بوابة الدقة](#adata-20--توقع-الطلب-مع-بوابة-الدقة--demand-forecast-with-accuracy-gate)
- [`ADATA-21` الإحصاء الوصفي وسرد التوزيعات](#adata-21--الإحصاء-الوصفي-وسرد-التوزيعات--descriptive-statistics-and-distribution-narrative)
- [`ADATA-22` استكشاف البيانات المنضبط قبل النمذجة](#adata-22--استكشاف-البيانات-المنضبط-قبل-النمذجة--disciplined-exploratory-data-analysis-pass)
- [`ADATA-23` التنبؤ بالمحركات ومراجعة نماذج الانحدار](#adata-23--التنبؤ-بالمحركات-ومراجعة-نماذج-الانحدار--driver-based-forecasts-and-regression-review)
- [`ADATA-24` سير عمل التحليل التجريبي بلغات بايثون وR وستاتا](#adata-24--سير-عمل-التحليل-التجريبي-بلغات-بايثون-وr-وستاتا--empirical-analysis-workflow-in-python-r-or-stata)
- [`ADATA-25` اختيار الاختبار الإحصائي وفحص الافتراضات](#adata-25--اختيار-الاختبار-الإحصائي-وفحص-الافتراضات--guided-test-selection-with-assumption-checks)
- [`ADATA-26` استرجاع ملفات CSV الفوضوية دون فقد صفوف](#adata-26--استرجاع-ملفات-csv-الفوضوية-دون-فقد-صفوف--recover-messy-csvtsv-without-losing-rows)
- [`ADATA-27` تمييز الإشارة عن الضجيج في مؤشرات اللوحات](#adata-27--تمييز-الإشارة-عن-الضجيج-في-مؤشرات-اللوحات--signal-vs-noise-annotation-for-dashboard-metrics)
- [`ADATA-28` بنية تجارب موثوقة مع فحص SRM](#adata-28--بنية-تجارب-موثوقة-مع-فحص-srm--trustworthy-experiment-plumbing-with-srm-check)
- [`ADATA-29` فهرس البيانات ووسم PII والنسب](#adata-29--فهرس-البيانات-ووسم-pii-والنسب--catalog-pii-tagging-and-lineage-setup)
- [`ADATA-30` حارس مخاطر Delta والبث](#adata-30--حارس-مخاطر-delta-والبث--delta-and-streaming-foot-gun-guard)
- [`ADATA-31` تشخيص فشل المزامنة وصحة المصادر](#adata-31--تشخيص-فشل-المزامنة-وصحة-المصادر--diagnose-failing-warehouse-syncs-and-source-health)
- [`ADATA-32` هيكلة مشروع dbt بطبقات وCI](#adata-32--هيكلة-مشروع-dbt-بطبقات-وci--layered-dbt-project-scaffold-with-ci)
- [`ADATA-33` تصميم ميدالية ومنهج الاستيعاب](#adata-33--تصميم-ميدالية-ومنهج-الاستيعاب--medallion-lakehouse-and-ingestion-method-choice)
- [`ADATA-34` عقد خط بيانات: الحبيبية والتكرار الآمن](#adata-34--عقد-خط-بيانات-الحبيبية-والتكرار-الآمن--pipeline-contract-grain-idempotency-checkpoints)
- [`ADATA-35` ضبط Spark بالأدلة أولاً](#adata-35--ضبط-spark-بالأدلة-أولاً--spark-and-databricks-evidence-first-tuning)
- [`ADATA-36` خطة اختبار لخطوط ETL وdbt](#adata-36--خطة-اختبار-لخطوط-etl-وdbt--test-plan-for-etl-and-dbt-pipelines)
- [`ADATA-37` ضبط نوع مزامنة المستودع والحقل التزايدي](#adata-37--ضبط-نوع-مزامنة-المستودع-والحقل-التزايدي--tune-warehouse-sync-type-and-incremental-field)
- [`ADATA-38` مراجعة مخطط واستعلامات ClickHouse](#adata-38--مراجعة-مخطط-واستعلامات-clickhouse--clickhouse-schema-and-query-rule-review)
- [`ADATA-39` استعلام DuckDB على ملفات محلية أو S3](#adata-39--استعلام-duckdb-على-ملفات-محلية-أو-s3--duckdb-attach-query-and-read-local-or-s3-data)
- [`ADATA-40` ضبط استعلامات SQL والفهارس بالأدلة](#adata-40--ضبط-استعلامات-sql-والفهارس-بالأدلة--evidence-first-sql-query-and-index-tuning)
- [`ADATA-41` إدارة Milvus وZilliz عبر الأوامر](#adata-41--إدارة-milvus-وzilliz-عبر-الأوامر--milvus-and-zilliz-admin-via-cli)
- [`ADATA-42` من اللغة الطبيعية إلى استعلام MongoDB](#adata-42--من-اللغة-الطبيعية-إلى-استعلام-mongodb--natural-language-to-mongodb-query-and-schema-design)
- [`ADATA-43` تشخيص استعلامات Postgres البطيئة بـ EXPLAIN](#adata-43--تشخيص-استعلامات-postgres-البطيئة-بـ-explain--postgres-slow-query-diagnosis-with-explain)
- [`ADATA-44` نمط الجداول الزمنية بوقت النظام](#adata-44--نمط-الجداول-الزمنية-بوقت-النظام--system-time-temporal-table-pattern)
- [`ADATA-45` سجل تدقيق للتغييرات في قاعدة البيانات](#adata-45--سجل-تدقيق-للتغييرات-في-قاعدة-البيانات--trigger-based-database-audit-trail)
- [`ADATA-46` تدقيق خط الاسترجاع على سبعة محاور](#adata-46--تدقيق-خط-الاسترجاع-على-سبعة-محاور--seven-axis-retrieval-pipeline-audit)
- [`ADATA-47` بوابة تسوية الحسابات قبل التقارير](#adata-47--بوابة-تسوية-الحسابات-قبل-التقارير--account-reconciliation-gate-before-reporting)

## البطاقات / cards

### `ADATA-01` — خطوط معالجة آمنة التكرار وملء رجعي مضبوط / Idempotent pipeline steps, retries and safe backfills

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0 / MIT (no copyleft seen among supporting ids); the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** جعل خطوط المعالجة متعددة الخطوات آمنة لإعادة التشغيل بإثبات التكرار الآمن وإضافة إعادة محاولة محدودة لكل خطوة وتنفيذ ملء رجعي مضبوط، باستخدام محرك سير عمل دائم بدل سلاسل مهام يدوية. — Make multi-step pipelines safe to re-run by proving idempotency, adding bounded per-step retries, and executing controlled backfills, using a durable workflow engine instead of hand-rolled job chains.

**متى:** A 'do A then B then C, retry each' job; ETL or order fulfillment; a backfill that may corrupt state; building or debugging a Falcon Fusion or Convex workflow.

**كيف:** 1) Prove idempotency first: deterministic partition keys and overwrite-by-partition writes so a re-run cannot duplicate. 2) Add bounded retries with exponential backoff and jitter per step. 3) On Convex use the workflow component so each step runs in order and retries independently; do not chain scheduler calls or build a custom jobs table. 4) Plan the backfill: partition strategy, catch-up configuration, concurrency caps, monitoring and rollback. 5) For Falcon Fusion style engines: discover actions through the live API, author workflow YAML, validate against the JSON schema, then trigger and tail execution status. Based on descriptions plus brief reads, not full procedures.

**المعاملات:** partition key; retry limits; concurrency cap; engine (Convex\|Airflow-style\|Falcon Fusion)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** idempotency · backfill · workflow · إعادة-المحاولة · durable

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2269-data-orchestration/8650-handle-backfills-and-retries`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1472-convex/3609-workflow`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1209-crowdstrike-falcon-fusion/2865-workflows`

#### 7. قدرات قريبة في العائلة

- `ADATA-02` استخراج الأنماط السيئة من سجلات جلسات الوكلاء / Mine agent session logs for anti-patterns (documented)
- `ADATA-03` نشر استعلام محفوظ كنقطة API / Expose saved query as API endpoint (documented)

### `ADATA-02` — استخراج الأنماط السيئة من سجلات جلسات الوكلاء / Mine agent session logs for anti-patterns

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يفهرس سجلات جلسات الوكلاء ويعلّم أخطاء الأدوات وحلقات إعادة المحاولة والاستدعاءات المكررة والنتائج الضخمة، ويستخرج حقائق محددة من JSONL ضخم دون تحميله في السياق. — Index agent session transcripts, flag tool errors, retry loops, duplicate calls and oversized results, and pull exact facts from huge JSONL without loading the raw data into context.

**متى:** User wants to review agent performance, find tool misuse, debug agent behavior, mine workflow patterns, or answer a numeric question about long transcripts or a fleet's traffic.

**كيف:** 1) Index sessions into a local store (sqlite or JSONL set). 2) Sweep for categories: tool errors, retry loops, duplicate calls, shell commands that a dedicated tool already covers, oversized results or sessions. 3) Record findings with session id and evidence in a findings store. 4) For specific numbers (tool timings, query counts, error summaries) delegate to an inspector that queries the files so raw data stays out of the main context. 5) Optionally keep an append-only JSONL traffic log so a fleet has one org-wide view. 6) Turn repeated findings into rules or skills.

**المعاملات:** transcript directory; finding categories; time window

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** transcript-analysis · kaizen · session-logs · تحليل الجلسات · observability

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/236-agent-transcripts/764-transcript-sweep`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1544-agentskill-kaizen/4237-transcript-analysis`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3264-agent-traffic-log/13775-agent-traffic-log`

#### 7. قدرات قريبة في العائلة

- `ADATA-01` خطوط معالجة آمنة التكرار وملء رجعي مضبوط / Idempotent pipeline steps, retries and safe backfills (documented)
- `ADATA-03` نشر استعلام محفوظ كنقطة API / Expose saved query as API endpoint (documented)
- `ADATA-04` مطابقة الطلبات بين CRM وأدوات التحليل / Reconcile leads across CRM and analytics (documented)

### `ADATA-03` — نشر استعلام محفوظ كنقطة API / Expose saved query as API endpoint

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** إنشاء وضبط نقطة PostHog بنوع الاستعلام والتخزين المؤقت والإصدارات. — Create and tune a PostHog endpoint: query kind, name, variables, freshness, materialisation, versions.

**متى:** Exposing HogQL/insight data to external callers.

**كيف:** 1) Confirm external caller and stable query. 2) URL-safe snake_case name, no version. 3) Choose HogQL vs insight. 4) Set data_freshness_seconds; materialise heavy queries without cohort breakdown. 5) Preview drafts, roll back versions. 6) Audit stale endpoints.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** posthog · endpoint · hogql · تحليلات

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2957-posthog/12289-creating-an-endpoint`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/see batch record 12372`

#### 7. قدرات قريبة في العائلة

- `ADATA-01` خطوط معالجة آمنة التكرار وملء رجعي مضبوط / Idempotent pipeline steps, retries and safe backfills (documented)
- `ADATA-02` استخراج الأنماط السيئة من سجلات جلسات الوكلاء / Mine agent session logs for anti-patterns (documented)
- `ADATA-04` مطابقة الطلبات بين CRM وأدوات التحليل / Reconcile leads across CRM and analytics (documented)
- `ADATA-05` أدوات تحليل سوق الكريبتو وDeFi / Crypto market and DeFi analytics CLI suite (documented)

### `ADATA-04` — مطابقة الطلبات بين CRM وأدوات التحليل / Reconcile leads across CRM and analytics

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يطابق سجلات الطلبات بين مصدرين بمفتاح الرابط الخارجي ويصنفها إلى مطابق ومختلف ومنفرد. — Reconcile lead records between two sources keyed on an external link and classify matches, diffs and one-sided rows.

**متى:** Comparing CRM leads with ad or call-tracking reports (amoCRM, Roistat, Yandex Direct).

**كيف:** 1) Require per-row fields: source, occurred_at, status, responsible, external_link. 2) Join on external_link. 3) Output three buckets: match, mismatch (field-level diff), only-in-second. 4) Read-only by default; any write needs separate explicit approval. 5) Use synthetic data for tests; never publish tokens, subdomains or contacts.

**المعاملات:** two exports, key field

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** reconciliation · crm · sheet-join · مطابقة · تحليل

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2655-yandex-direct-for-all/10092-amocrm-api-control`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2655-yandex-direct-for-all/10094-roistat-reports-api`

#### 7. قدرات قريبة في العائلة

- `ADATA-02` استخراج الأنماط السيئة من سجلات جلسات الوكلاء / Mine agent session logs for anti-patterns (documented)
- `ADATA-03` نشر استعلام محفوظ كنقطة API / Expose saved query as API endpoint (documented)
- `ADATA-05` أدوات تحليل سوق الكريبتو وDeFi / Crypto market and DeFi analytics CLI suite (documented)
- `ADATA-06` ضرائب الكريبتو بطرق FIFO وLIFO وHIFO / Crypto tax gains with FIFO LIFO HIFO (documented)

### `ADATA-05` — أدوات تحليل سوق الكريبتو وDeFi / Crypto market and DeFi analytics CLI suite

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تشغيل تحليلات الأرباح والسيولة والمعاملات المعلقة. — Run script-driven analysis: arbitrage, liquidity pools, yields, mempool, derivatives, sentiment.

**متى:** Researching spreads, pools, yields or gas.

**كيف:** 1) arb_finder.py scan/triangular/cross-chain with fees. 2) mempool_analyzer.py gas percentiles (10/50/75/90). 3) Compare APY, TVL, impermanent loss. 4) Use public APIs.

**المعاملات:** pair, chain

**التثبيت:** pip install httpx rich networkx

**الوسوم:** defi · arbitrage · تحليل

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1656-arbitrage-opportunity-finder/4661-finding-arbitrage-opportunities`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1672-mempool-analyzer/4677-analyzing-mempool`

#### 7. قدرات قريبة في العائلة

- `ADATA-03` نشر استعلام محفوظ كنقطة API / Expose saved query as API endpoint (documented)
- `ADATA-04` مطابقة الطلبات بين CRM وأدوات التحليل / Reconcile leads across CRM and analytics (documented)
- `ADATA-06` ضرائب الكريبتو بطرق FIFO وLIFO وHIFO / Crypto tax gains with FIFO LIFO HIFO (documented)
- `ADATA-07` تحليل بيانات السلسلة والمحفظة وندرة NFT / On-chain data, portfolio and NFT rarity analysis (documented)

### `ADATA-06` — ضرائب الكريبتو بطرق FIFO وLIFO وHIFO / Crypto tax gains with FIFO LIFO HIFO

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** حساب الأرباح الرأسمالية وإنتاج نموذج 8949. — Compute cost basis and capital gains from exchange CSVs and emit Form 8949.

**متى:** Tax reports for crypto.

**كيف:** 1) Export CSVs. 2) Run calculator with --year and --method. 3) --compare-methods. 4) --income-report for staking/airdrops. 5) Output CSV. Not tax advice.

**المعاملات:** year, method

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** tax · fifo · ضرائب

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1663-crypto-tax-calculator/4668-calculating-crypto-taxes`

#### 7. قدرات قريبة في العائلة

- `ADATA-04` مطابقة الطلبات بين CRM وأدوات التحليل / Reconcile leads across CRM and analytics (documented)
- `ADATA-05` أدوات تحليل سوق الكريبتو وDeFi / Crypto market and DeFi analytics CLI suite (documented)
- `ADATA-07` تحليل بيانات السلسلة والمحفظة وندرة NFT / On-chain data, portfolio and NFT rarity analysis (documented)
- `ADATA-08` استقبال الفواتير والإيصالات وأرشفتها / Invoice and receipt intake into archive (documented)

### `ADATA-07` — تحليل بيانات السلسلة والمحفظة وندرة NFT / On-chain data, portfolio and NFT rarity analysis

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** استكشاف المعاملات وتتبع الحيتان وترتيب ندرة NFT. — Explore blocks/transactions, whale flows, portfolios and rank NFT rarity.

**متى:** Investigating wallets or collections.

**كيف:** 1) Query blocks/txs. 2) Track whale flows. 3) Value portfolio and allocation. 4) Score rarity by trait frequency.

**المعاملات:** address, collection

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** onchain · nft · تحليل

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1674-on-chain-analytics/4679-analyzing-on-chain-data`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1673-nft-rarity-analyzer/4678-analyzing-nft-rarity`

#### 7. قدرات قريبة في العائلة

- `ADATA-05` أدوات تحليل سوق الكريبتو وDeFi / Crypto market and DeFi analytics CLI suite (documented)
- `ADATA-06` ضرائب الكريبتو بطرق FIFO وLIFO وHIFO / Crypto tax gains with FIFO LIFO HIFO (documented)
- `ADATA-08` استقبال الفواتير والإيصالات وأرشفتها / Invoice and receipt intake into archive (documented)
- `ADATA-09` نمذجة مونت كارلو وسيناريوهات ماذا لو / Monte Carlo and what-if scenario modeling (documented)

### `ADATA-08` — استقبال الفواتير والإيصالات وأرشفتها / Invoice and receipt intake into archive

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT/Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يستخرج حقول الفواتير بدرجة ثقة ويربط المستندات ويعيد تسميتها ويؤرشفها ويستعلم عنها. — Extract invoice fields with confidence, link documents by shared numbers, rename and file by period, then query.

**متى:** Folder of invoices/receipts/statements to organize for accounting.

**كيف:** 1) Read one doc first: fields (vendor, invoice_no, po, date, due, subtotal, tax, total, currency, iban) with high/medium/low confidence. 2) Cross-reference shared invoice/PO/IBAN numbers (check-digit verified). 3) Dry-run rename template {date}_{vendor}_{ref}. 4) Intake to YYYY/MM or FY/Q, OCR scans, keep originals. 5) Query by total>1000, due<date; export CSV. Caveat: no line items; low-confidence date is mtime.

**المعاملات:** date order, fiscal start

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** invoices · OCR · فواتير · accounting

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `tesseract` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1196-carrel-finance/2839-accounting-inbox`

#### 7. قدرات قريبة في العائلة

- `ADATA-06` ضرائب الكريبتو بطرق FIFO وLIFO وHIFO / Crypto tax gains with FIFO LIFO HIFO (documented)
- `ADATA-07` تحليل بيانات السلسلة والمحفظة وندرة NFT / On-chain data, portfolio and NFT rarity analysis (documented)
- `ADATA-09` نمذجة مونت كارلو وسيناريوهات ماذا لو / Monte Carlo and what-if scenario modeling (documented)
- `ADATA-10` تحليل النسب والانحرافات والتوقع المتجدد / Ratio analysis, variance and rolling forecast (documented)

### `ADATA-09` — نمذجة مونت كارلو وسيناريوهات ماذا لو / Monte Carlo and what-if scenario modeling

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحاكي سيناريوهات الميزانية بتوزيعات عائد ويعرض P10/P50/P90 واحتمال بلوغ الهدف. — Simulate budget or channel scenarios with sampled ROI distributions and report P10/P50/P90 and target probability.

**متى:** Comparing budget reallocations, cascading multi-variable what-ifs, risk-adjusted decisions.

**كيف:** 1) Define 2-4 scenarios with per-channel budget, ROI mean and std, saturation. 2) Run 10,000 iterations (50k for high stakes) sampling ROI with diminishing returns. 3) Report mean, P10, P50, P90, probability of target. 4) Rank by expected and risk-adjusted return; tornado sensitivity of top scenarios. 5) Check convergence; document assumptions.

**المعاملات:** scenarios, iterations, horizon months

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** monte-carlo · scenarios · محاكاة · budget

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1520-digital-marketing-pro/4117-simulate`

#### 7. قدرات قريبة في العائلة

- `ADATA-07` تحليل بيانات السلسلة والمحفظة وندرة NFT / On-chain data, portfolio and NFT rarity analysis (documented)
- `ADATA-08` استقبال الفواتير والإيصالات وأرشفتها / Invoice and receipt intake into archive (documented)
- `ADATA-10` تحليل النسب والانحرافات والتوقع المتجدد / Ratio analysis, variance and rolling forecast (documented)
- `ADATA-11` مقاييس خط المبيعات وكفاءة الدخول للسوق / SaaS pipeline and GTM efficiency metrics (documented)

### `ADATA-10` — تحليل النسب والانحرافات والتوقع المتجدد / Ratio analysis, variance and rolling forecast

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT/Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحسب نسب الربحية والسيولة والرفع والكفاءة وانحرافات الموازنة وتوقعات مبنية على المحركات. — Compute profitability, liquidity, leverage, efficiency and valuation ratios, favorable/unfavorable budget variances and driver-based forecasts.

**متى:** Statement analysis, monthly close review, budget vs actual, forecast refresh.

**كيف:** 1) Validate input completeness (nulls, implausible values) before ratios. 2) Run ratio calculator on JSON statements across 5 categories. 3) Decompose variances into drivers with waterfall narrative; mark favorable/unfavorable. 4) Rolling forecast with base/bull/bear. 5) Track accuracy targets about +/-5% revenue, +/-3% expenses. 6) Executive summary first.

**المعاملات:** statements JSON, materiality threshold

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ratios · variance · نسب مالية · forecast

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/189-finance-skills/560-financial-analyst`

#### 7. قدرات قريبة في العائلة

- `ADATA-08` استقبال الفواتير والإيصالات وأرشفتها / Invoice and receipt intake into archive (documented)
- `ADATA-09` نمذجة مونت كارلو وسيناريوهات ماذا لو / Monte Carlo and what-if scenario modeling (documented)
- `ADATA-11` مقاييس خط المبيعات وكفاءة الدخول للسوق / SaaS pipeline and GTM efficiency metrics (documented)
- `ADATA-12` محاسبة الأعمال الصغيرة: رواتب وضرائب وتحصيل / Small-business bookkeeping: payroll, tax, invoice chase (documented)

### `ADATA-11` — مقاييس خط المبيعات وكفاءة الدخول للسوق / SaaS pipeline and GTM efficiency metrics

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحلل تغطية خط المبيعات والسرعة وعمر الصفقات ودقة التوقع وكفاءة GTM. — Analyze pipeline coverage, velocity, deal aging, forecast accuracy and GTM efficiency from JSON deal data.

**متى:** Pipeline review, forecast accuracy audit, CRO reporting.

**كيف:** 1) Prepare JSON: quota, stages, average_cycle_days, deals. 2) Run pipeline analyzer (--format text\|json). 3) Healthy coverage 3-4x quota; velocity = opps x avg deal x win rate / cycle. 4) Flag deals over 2x stage cycle and >40% concentration. 5) Track forecast accuracy over periods; compute GTM efficiency.

**المعاملات:** quota, stages, deals

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pipeline · SaaS · مبيعات · GTM

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/136-business-growth-skills/386-revenue-operations`

#### 7. قدرات قريبة في العائلة

- `ADATA-09` نمذجة مونت كارلو وسيناريوهات ماذا لو / Monte Carlo and what-if scenario modeling (documented)
- `ADATA-10` تحليل النسب والانحرافات والتوقع المتجدد / Ratio analysis, variance and rolling forecast (documented)
- `ADATA-12` محاسبة الأعمال الصغيرة: رواتب وضرائب وتحصيل / Small-business bookkeeping: payroll, tax, invoice chase (documented)
- `ADATA-13` تحليل نتائج اختبار A/B مع حجم الأثر / A/B test result analysis with effect sizes (documented)

### `ADATA-12` — محاسبة الأعمال الصغيرة: رواتب وضرائب وتحصيل / Small-business bookkeeping: payroll, tax, invoice chase

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0 / MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ينفذ روتين نهاية الشهر للأعمال الصغيرة: تجهيز الرواتب وتذكير الفواتير وحزم الضرائب وجداول نهاية السنة. — Run month-end routines for small businesses: payroll prep, overdue invoice reminders, tax packs and AU year-end schedules.

**متى:** Owner wants cash snapshot, payroll or tax prep, reconciliation, or Australian Div 7A/FBT work.

**كيف:** 1) Pull ledger and timesheets from the accounting system. 2) Reconcile and close month. 3) Payroll: pre-run sanity checks, post-run reconciliation. 4) Draft invoice-chase emails by aging bucket. 5) Walk accounting profit to taxable income. 6) Build Div 7A loan schedule per shareholder loan. 7) Mark as prep for accountant, not tax advice.

**المعاملات:** jurisdiction, period, ledger source

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** payroll · tax prep · invoice · رواتب · ضرائب

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`

#### 7. قدرات قريبة في العائلة

- `ADATA-10` تحليل النسب والانحرافات والتوقع المتجدد / Ratio analysis, variance and rolling forecast (documented)
- `ADATA-11` مقاييس خط المبيعات وكفاءة الدخول للسوق / SaaS pipeline and GTM efficiency metrics (documented)
- `ADATA-13` تحليل نتائج اختبار A/B مع حجم الأثر / A/B test result analysis with effect sizes (documented)
- `ADATA-14` تخطيط حجم العينة وقوة اختبار A/B / A/B test sample size and power planning (documented)

### `ADATA-13` — تحليل نتائج اختبار A/B مع حجم الأثر / A/B test result analysis with effect sizes

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** اختر الاختبار الإحصائي المناسب واذكر القيمة p وفترة الثقة وحجم الأثر ثم قرار الإطلاق أو الانتظار. — Choose z/t/chi-square test, report p-value, CI and effect size, then give ship/hold/extend verdict.

**متى:** User shares experiment numbers and asks whether the result is significant.

**كيف:** 1) Confirm metric type, n and observed values. 2) Proportions->z-test, means->t-test, categories->chi-square. 3) Report p, CI, Cohen d/h or Cramer V. 4) Separate statistical from practical significance. 5) Flag peeking, multiple comparisons, SUTVA. 6) Answer Bottom line, What, Why, How to act.

**المعاملات:** control/treatment n and x or mean/std; alpha

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ab-test · significance · اختبار · إحصاء

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/184-statistical-analyst/553-statistical-analyst`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2996-revenuecat/12738-experiment-analysis`

#### 7. قدرات قريبة في العائلة

- `ADATA-11` مقاييس خط المبيعات وكفاءة الدخول للسوق / SaaS pipeline and GTM efficiency metrics (documented)
- `ADATA-12` محاسبة الأعمال الصغيرة: رواتب وضرائب وتحصيل / Small-business bookkeeping: payroll, tax, invoice chase (documented)
- `ADATA-14` تخطيط حجم العينة وقوة اختبار A/B / A/B test sample size and power planning (documented)
- `ADATA-15` تخطيط القدرة الإحصائية وحجم العينة / A priori power and sample-size planning (documented)

### `ADATA-14` — تخطيط حجم العينة وقوة اختبار A/B / A/B test sample size and power planning

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحسب حجم العينة المطلوب لكل مجموعة من ألفا والقوة وأصغر أثر مهم قبل الإطلاق. — Compute required n per group from alpha, power and a business-meaningful MDE before launch.

**متى:** Planning an experiment; asked how big a sample is needed or whether a null result is trustworthy.

**كيف:** 1) Fix the MDE first (smallest effect that changes the decision). 2) Default alpha 0.05, power 0.80. 3) Match calc to the test (two-proportion or two-sample t). 4) Solve n per group, report total and duration at given traffic. 5) If n is fixed, invert to power/MDE and warn when power<0.80. 6) Never compute post-hoc observed power. statsmodels TTestIndPower/NormalIndPower.

**المعاملات:** baseline rate, MDE, alpha, power, daily traffic

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ab-test · power · sample-size · اختبار · عينة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2235-applied-statistics/8496-power-and-sample-size`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`

#### 7. قدرات قريبة في العائلة

- `ADATA-12` محاسبة الأعمال الصغيرة: رواتب وضرائب وتحصيل / Small-business bookkeeping: payroll, tax, invoice chase (documented)
- `ADATA-13` تحليل نتائج اختبار A/B مع حجم الأثر / A/B test result analysis with effect sizes (documented)
- `ADATA-15` تخطيط القدرة الإحصائية وحجم العينة / A priori power and sample-size planning (documented)
- `ADATA-16` استكشاف البيانات الآمن المحدود / Bounded safe exploratory data profiling (documented)

### `ADATA-15` — تخطيط القدرة الإحصائية وحجم العينة / A priori power and sample-size planning

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** احسب حجم العينة المطلوب أو أصغر أثر قابل للكشف بالصيغ المغلقة أو المحاكاة مع منحنيات القدرة. — Compute required n or minimum detectable effect by closed form or Monte Carlo simulation, with power curves.

**متى:** Grant, protocol or study needs a sample-size justification.

**كيف:** 1) Fix three of n, effect size, alpha, power. 2) Pick/convert effect size (d, f, OR). 3) Closed-form recipe for standard tests, handle unequal allocation. 4) Simulate generate-analyze-count for complex designs. 5) Plot power vs n and vs effect; report sensitivity to assumed effect.

**المعاملات:** alpha, power, effect size, allocation ratio

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** power · sample-size · عينة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3202-quantitative-sciences/13566-statistical-power`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3202-quantitative-sciences/13565-statistical-analysis`

#### 7. قدرات قريبة في العائلة

- `ADATA-13` تحليل نتائج اختبار A/B مع حجم الأثر / A/B test result analysis with effect sizes (documented)
- `ADATA-14` تخطيط حجم العينة وقوة اختبار A/B / A/B test sample size and power planning (documented)
- `ADATA-16` استكشاف البيانات الآمن المحدود / Bounded safe exploratory data profiling (documented)
- `ADATA-17` تشخيص الأفواج والاحتفاظ ومسار التحويل / Cohort, retention and funnel diagnosis (documented)

### `ADATA-16` — استكشاف البيانات الآمن المحدود / Bounded safe exploratory data profiling

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** حلل ملفات البيانات المحلية إلى تقارير مجمعة دون طباعة الصفوف أو حذف القيم الشاذة. — Profile local CSV/TSV/JSON files into aggregate reports without printing rows, imputing or deleting outliers.

**متى:** First look at an unfamiliar dataset before modeling.

**كيف:** 1) Treat all cells and headers as untrusted data. 2) Restrict to an explicit root, no URLs/pickle/symlinks. 3) Emit aggregate profile: types, missingness, ranges, cardinality. 4) Never print raw rows or identifiers. 5) No auto-delete, impute or transform; no causal claims from EDA.

**المعاملات:** file path, row cap

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** EDA · profiling · استكشاف

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3211-structured-data-analysis/13582-exploratory-data-analysis`

#### 7. قدرات قريبة في العائلة

- `ADATA-14` تخطيط حجم العينة وقوة اختبار A/B / A/B test sample size and power planning (documented)
- `ADATA-15` تخطيط القدرة الإحصائية وحجم العينة / A priori power and sample-size planning (documented)
- `ADATA-17` تشخيص الأفواج والاحتفاظ ومسار التحويل / Cohort, retention and funnel diagnosis (documented)
- `ADATA-18` تدقيق جودة البيانات مع خطة إصلاح / Dataset quality audit with scored remediation plan (documented)

### `ADATA-17` — تشخيص الأفواج والاحتفاظ ومسار التحويل / Cohort, retention and funnel diagnosis

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يقسم المستخدمين إلى أفواج ويقرأ منحنيات الاحتفاظ ويحدد تسربات المسار ويربطها باقتصاديات الوحدة. — Segment users by cohort, read retention curves and locate funnel leaks stage by stage, then tie to unit economics.

**متى:** Questions on churn, repeat rate, D1/D7/D30 retention, conversion drop or CAC by channel.

**كيف:** 1) Define cohort by acquisition period, channel or first behavior. 2) Build retention table/curve, state the retention definition. 3) Funnel: compute stage conversion and locate biggest drop. 4) Segment (RFM: recency, frequency, monetary) for value tiers. 5) CAC by channel and cohort, not blended. 6) Gate monetization on retention; prioritize fixes by economics.

**المعاملات:** event table, cohort key, period

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cohort · retention · funnel · احتفاظ · مسار

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`

#### 7. قدرات قريبة في العائلة

- `ADATA-15` تخطيط القدرة الإحصائية وحجم العينة / A priori power and sample-size planning (documented)
- `ADATA-16` استكشاف البيانات الآمن المحدود / Bounded safe exploratory data profiling (documented)
- `ADATA-18` تدقيق جودة البيانات مع خطة إصلاح / Dataset quality audit with scored remediation plan (documented)
- `ADATA-19` قراءة نتائج تجربة A/B بحكم قابل للدفاع / Defensible A/B experiment readout and verdict (documented)

### `ADATA-18` — تدقيق جودة البيانات مع خطة إصلاح / Dataset quality audit with scored remediation plan

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يوصف مجموعة بيانات ويصنف القيم المفقودة والشاذة ويمنح درجة جودة ويرتب الإصلاحات. — Profile a dataset, classify missingness and outliers, score quality 0-100 and prioritize fixes.

**متى:** Asked to check data quality, hunt nulls/outliers/duplicates, or set up monitoring thresholds.

**كيف:** 1) Profile: shape, dtypes, null %, cardinality, constants, mixed types (data_profiler.py --file x.csv, --format json). 2) Missingness pattern MCAR/MAR/MNAR with imputation advice per column. 3) Outliers by IQR and z-score. 4) Cross-column: duplicates, referential integrity, logical constraints. 5) Data Quality Score 0-100 and ranked remediation. 6) Monitoring: 5-8 critical columns with null/outlier/domain thresholds. Also uniqueness/not-null/referential/freshness tests (Great Expectations, dbt).

**المعاملات:** file, columns, thresholds

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** data-quality · missing · outliers · جودة · تدقيق

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/164-data-quality-auditor/533-data-quality-auditor`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3081-data-engineering/13248-data-quality-frameworks`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`

#### 7. قدرات قريبة في العائلة

- `ADATA-16` استكشاف البيانات الآمن المحدود / Bounded safe exploratory data profiling (documented)
- `ADATA-17` تشخيص الأفواج والاحتفاظ ومسار التحويل / Cohort, retention and funnel diagnosis (documented)
- `ADATA-19` قراءة نتائج تجربة A/B بحكم قابل للدفاع / Defensible A/B experiment readout and verdict (documented)
- `ADATA-20` توقع الطلب مع بوابة الدقة / Demand forecast with accuracy gate (documented)

### `ADATA-19` — قراءة نتائج تجربة A/B بحكم قابل للدفاع / Defensible A/B experiment readout and verdict

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحلل تجربة منتهية مقابل خطتها ويصدر حكم إطلاق أو رفض أو غير حاسم مع حجم الأثر وفاصل الثقة. — Analyze a finished experiment against its plan and issue a ship / don't ship / inconclusive verdict with effect size and CI.

**متى:** A test finished and someone asks whether the winner is real or can ship.

**كيف:** 1) Recover pre-registered metric, test and stopping rule; flag post-hoc choices. 2) Check early stopping/peeking. 3) Run primary test; headline is effect size plus 95% CI, not p. 4) Check guardrails (latency, churn, revenue). 5) Holm/Bonferroni (confirmatory) or Benjamini-Hochberg (exploratory) across metrics/segments. 6) Simpson's paradox check by subgroup. 7) Fill template: Primary / Decision-relevant / Guardrails / Multiplicity / Pitfall screen / Verdict.

**المعاملات:** experiment data, plan, metrics, guardrails

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ab-test · verdict · multiplicity · تجربة · نتائج

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2235-applied-statistics/8495-experiment-analysis`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`

#### 7. قدرات قريبة في العائلة

- `ADATA-17` تشخيص الأفواج والاحتفاظ ومسار التحويل / Cohort, retention and funnel diagnosis (documented)
- `ADATA-18` تدقيق جودة البيانات مع خطة إصلاح / Dataset quality audit with scored remediation plan (documented)
- `ADATA-20` توقع الطلب مع بوابة الدقة / Demand forecast with accuracy gate (documented)
- `ADATA-21` الإحصاء الوصفي وسرد التوزيعات / Descriptive statistics and distribution narrative (documented)

### `ADATA-20` — توقع الطلب مع بوابة الدقة / Demand forecast with accuracy gate

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** نظف السجل واختر نموذج التمهيد أو كروستون وتحقق من MAPE والانحياز قبل الاعتماد. — Clean history, pick smoothing/Croston model by demand pattern, and require MAPE/bias/tracking signal before use.

**متى:** Forecasting SKU demand, sales or any time series.

**كيف:** 1) Use unconstrained demand; flag outliers. 2) Need >=12 periods for seasonal, >=6 otherwise. 3) SES / Holt / Holt-Winters; Croston or TSB if CV>0.5 intermittent. 4) Holdout last 3-6 periods. 5) MAPE, bias (\|bias\|<=5%), tracking signal (\|TS\|>4 out of control). 6) Documented overrides overlay.

**المعاملات:** horizon, holdout, season length

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** forecast · MAPE · توقع

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2389-supply-chain-planning/9247-demand-forecasting`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1603-time-series-forecaster/4574-forecasting-time-series-data`

#### 7. قدرات قريبة في العائلة

- `ADATA-18` تدقيق جودة البيانات مع خطة إصلاح / Dataset quality audit with scored remediation plan (documented)
- `ADATA-19` قراءة نتائج تجربة A/B بحكم قابل للدفاع / Defensible A/B experiment readout and verdict (documented)
- `ADATA-21` الإحصاء الوصفي وسرد التوزيعات / Descriptive statistics and distribution narrative (documented)
- `ADATA-22` استكشاف البيانات المنضبط قبل النمذجة / Disciplined exploratory data analysis pass (documented)

### `ADATA-21` — الإحصاء الوصفي وسرد التوزيعات / Descriptive statistics and distribution narrative

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يختار مقاييس المركز والتشتت المناسبة ويصف التوزيعات بالمئينات والقيم الشاذة وتنعيم الاتجاه. — Choose the right center/spread measures and describe distributions with percentiles, outliers and trend smoothing.

**متى:** Summarizing a numeric column, asked about outliers, correlations or trends in a dataset.

**كيف:** 1) Skewed data: report median and mean together; gap shows skew. 2) Spread: SD if normal, IQR if skewed, CV across scales. 3) Report p1,p5,p25,p50,p75,p90,p95,p99. 4) Describe shape, center, spread, outliers, bounds. 5) Trends: rolling 7d/28d means via pandas. 6) Outliers by IQR or z-score; hedge statistical claims.

**المعاملات:** column, grouping, window

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** descriptive · percentiles · outliers · إحصاء · توزيع

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pandas` ← python3 -c "import pandas" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `npm:p5` ← npm ls p5 أو وجود node_modules/p5
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/317-data/945-statistical-analysis`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`

#### 7. قدرات قريبة في العائلة

- `ADATA-19` قراءة نتائج تجربة A/B بحكم قابل للدفاع / Defensible A/B experiment readout and verdict (documented)
- `ADATA-20` توقع الطلب مع بوابة الدقة / Demand forecast with accuracy gate (documented)
- `ADATA-22` استكشاف البيانات المنضبط قبل النمذجة / Disciplined exploratory data analysis pass (documented)
- `ADATA-23` التنبؤ بالمحركات ومراجعة نماذج الانحدار / Driver-based forecasts and regression review (documented)

### `ADATA-22` — استكشاف البيانات المنضبط قبل النمذجة / Disciplined exploratory data analysis pass

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يوصف البيانات ويوثق قرارات التنظيف ويكشف التسرب ويحول الأنماط إلى فرضيات قبل النمذجة. — Profile data, document cleaning decisions, flag leakage and turn patterns into hypotheses before modeling.

**متى:** Starting analysis on a new dataset or before any model is trained.

**كيف:** 1) Verify target definition and availability at prediction time. 2) Profile shape, dtypes, missingness (and why), cardinality, duplicates, per-column distributions. 3) Record each cleaning choice and rationale. 4) Read plots adversarially (bimodality, Simpson reversal). 5) List leakage candidates (post-outcome columns, target-derived, ID-encoded). 6) Frame findings as hypotheses with uncertainty; do not p-hack. 7) Emit EDA report.

**المعاملات:** dataset, target

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** eda · leakage · profiling · استكشاف · بيانات

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2272-data-science-research/8669-eda-workflow`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`

#### 7. قدرات قريبة في العائلة

- `ADATA-20` توقع الطلب مع بوابة الدقة / Demand forecast with accuracy gate (documented)
- `ADATA-21` الإحصاء الوصفي وسرد التوزيعات / Descriptive statistics and distribution narrative (documented)
- `ADATA-23` التنبؤ بالمحركات ومراجعة نماذج الانحدار / Driver-based forecasts and regression review (documented)
- `ADATA-24` سير عمل التحليل التجريبي بلغات بايثون وR وستاتا / Empirical analysis workflow in Python, R or Stata (documented)

### `ADATA-23` — التنبؤ بالمحركات ومراجعة نماذج الانحدار / Driver-based forecasts and regression review

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يبني تنبؤات قائمة على المحركات أو السلاسل الزمنية ويراجع نماذج الانحدار والتنبؤ. — Build driver-based or time-series forecasts and review regression/forecast models for defensibility.

**متى:** Quarterly bookings/ARR/cash forecasts, spend anomaly thresholds, or checking an OLS/forecast model.

**كيف:** 1) Pick model family (OLS, GLM, time-series) from outcome type. 2) Driver-based: explicit drivers with owners, rolling refresh. 3) 13-week cash: receipts by source, disbursements, direct method. 4) Backtest on holdout, report error and intervals. 5) Check assumptions: residuals, multicollinearity, seasonality. 6) Set anomaly thresholds from forecast band.

**المعاملات:** history, horizon, drivers

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** forecast · regression · backtest · تنبؤ · انحدار

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`

#### 7. قدرات قريبة في العائلة

- `ADATA-21` الإحصاء الوصفي وسرد التوزيعات / Descriptive statistics and distribution narrative (documented)
- `ADATA-22` استكشاف البيانات المنضبط قبل النمذجة / Disciplined exploratory data analysis pass (documented)
- `ADATA-24` سير عمل التحليل التجريبي بلغات بايثون وR وستاتا / Empirical analysis workflow in Python, R or Stata (documented)
- `ADATA-25` اختيار الاختبار الإحصائي وفحص الافتراضات / Guided test selection with assumption checks (documented)

### `ADATA-24` — سير عمل التحليل التجريبي بلغات بايثون وR وستاتا / Empirical analysis workflow in Python, R or Stata

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ينفذ سير عمل قياسيا كاملا مع تسجيل مسبق وجداول ورسوم جاهزة للنشر. — Run a classical end-to-end econometric workflow with preregistration and publication-grade tables and figures.

**متى:** Economics-style empirical project needing regressions, tables, or a preregistered design.

**كيف:** 1) Preregister hypotheses, outcomes, specification. 2) Clean and document data in chosen stack (pandas/statsmodels, tidyverse/fixest, Stata). 3) Descriptive table then main regressions with robust/clustered errors. 4) Robustness checks. 5) Regression tables and figures to journal style. 6) Reproducible script top to bottom.

**المعاملات:** language, data, spec

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** econometrics · regression · tables · اقتصاد قياسي · جداول

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pandas` ← python3 -c "import pandas" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`

#### 7. قدرات قريبة في العائلة

- `ADATA-22` استكشاف البيانات المنضبط قبل النمذجة / Disciplined exploratory data analysis pass (documented)
- `ADATA-23` التنبؤ بالمحركات ومراجعة نماذج الانحدار / Driver-based forecasts and regression review (documented)
- `ADATA-25` اختيار الاختبار الإحصائي وفحص الافتراضات / Guided test selection with assumption checks (documented)
- `ADATA-26` استرجاع ملفات CSV الفوضوية دون فقد صفوف / Recover messy CSV/TSV without losing rows (documented)

### `ADATA-25` — اختيار الاختبار الإحصائي وفحص الافتراضات / Guided test selection with assumption checks

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** اختر الاختبار من نوع البيانات وافحص الافتراضات واذكر أحجام الأثر وبدائل بايزية. — Pick a statistical test from data type, check assumptions, report effect sizes and Bayesian alternatives.

**متى:** Researcher asks which test to use or how to report results.

**كيف:** 1) Classify outcome and design (paired, groups, repeated). 2) Check normality, variance, independence. 3) Select parametric or non-parametric. 4) Report effect size and CI not just p. 5) Offer Bayesian estimate; correct for multiple tests.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** stats · assumptions · اختبار

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3202-quantitative-sciences/13565-statistical-analysis`

#### 7. قدرات قريبة في العائلة

- `ADATA-23` التنبؤ بالمحركات ومراجعة نماذج الانحدار / Driver-based forecasts and regression review (documented)
- `ADATA-24` سير عمل التحليل التجريبي بلغات بايثون وR وستاتا / Empirical analysis workflow in Python, R or Stata (documented)
- `ADATA-26` استرجاع ملفات CSV الفوضوية دون فقد صفوف / Recover messy CSV/TSV without losing rows (documented)
- `ADATA-27` تمييز الإشارة عن الضجيج في مؤشرات اللوحات / Signal-vs-noise annotation for dashboard metrics (documented)

### `ADATA-26` — استرجاع ملفات CSV الفوضوية دون فقد صفوف / Recover messy CSV/TSV without losing rows

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يقرأ ملفات محددة الفواصل غير موثوقة بشكل قابل للتكرار مع فحص البايتات واكتشاف اللهجة وحجر الصفوف التالفة. — Parse unreliable delimited files reproducibly with byte inspection, dialect detection and a quarantine of bad rows.

**متى:** CSV with unknown encoding, ragged rows, locale numbers, repeated headers or schema drift.

**كيف:** 1) Copy file, record checksum; inspect BOM, line endings, null bytes, encoding candidates (strict UTF-8 first). 2) Detect dialect by sampling several regions; use a real CSV parser, never regex split. 3) Map source to normalized headers. 4) Parse with expected column count; quarantine failures with line number, raw text, error, field count. 5) Normalize dates/numbers/booleans as hypotheses. 6) Count every dropped or repaired row.

**المعاملات:** file, expected schema

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** csv · encoding · quarantine · ملفات · تنظيف

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2207-majestic-data/8243-csv-wrangling`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`

#### 7. قدرات قريبة في العائلة

- `ADATA-24` سير عمل التحليل التجريبي بلغات بايثون وR وستاتا / Empirical analysis workflow in Python, R or Stata (documented)
- `ADATA-25` اختيار الاختبار الإحصائي وفحص الافتراضات / Guided test selection with assumption checks (documented)
- `ADATA-27` تمييز الإشارة عن الضجيج في مؤشرات اللوحات / Signal-vs-noise annotation for dashboard metrics (documented)
- `ADATA-28` بنية تجارب موثوقة مع فحص SRM / Trustworthy experiment plumbing with SRM check (documented)

### `ADATA-27` — تمييز الإشارة عن الضجيج في مؤشرات اللوحات / Signal-vs-noise annotation for dashboard metrics

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يرفق فواصل ثقة أو علامة بيانات غير كافية بتغيرات المؤشرات حتى لا تدعي اللوحات ضجيجا. — Attach confidence intervals or insufficient-data flags to KPI movements so dashboards do not assert noise.

**متى:** A KPI tile shows a period-over-period change or trend and someone asks if it is real.

**كيف:** 1) Classify claim: point comparison, trend or group comparison. 2) Get denominators; no n means 'insufficient data'. 3) Rates: Wilson CI; means: t or bootstrap CI on the difference; rare counts: Poisson CI. 4) If CI spans zero, annotate 'within normal variation'. 5) Trends: fitted slope with CI or control-chart band, never two points. 6) Output the widget annotation plus one-line caveat.

**المعاملات:** metric, period values, n

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** dashboard · confidence-interval · kpi · مؤشرات · ضجيج

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2235-applied-statistics/8498-statistical-qa-of-metrics`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/317-data/945-statistical-analysis`

#### 7. قدرات قريبة في العائلة

- `ADATA-25` اختيار الاختبار الإحصائي وفحص الافتراضات / Guided test selection with assumption checks (documented)
- `ADATA-26` استرجاع ملفات CSV الفوضوية دون فقد صفوف / Recover messy CSV/TSV without losing rows (documented)
- `ADATA-28` بنية تجارب موثوقة مع فحص SRM / Trustworthy experiment plumbing with SRM check (documented)
- `ADATA-29` فهرس البيانات ووسم PII والنسب / Catalog, PII tagging and lineage setup (documented)

### `ADATA-28` — بنية تجارب موثوقة مع فحص SRM / Trustworthy experiment plumbing with SRM check

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يهيئ توزيعا ثابتا وتسجيل التعرض وبوابة عدم تطابق النسب قبل قراءة أي نتيجة. — Set up sticky assignment, exposure logging and a sample-ratio-mismatch gate before reading any result.

**متى:** Building or auditing an experimentation pipeline; suspicious or strange experiment results.

**كيف:** 1) Hash-based deterministic sticky assignment per unit. 2) Log exposure (who saw the variant), not just assignment. 3) Chi-square SRM test of observed vs intended split; failure invalidates the result. 4) Pre-register primary metric, MDE, duration, guardrails. 5) Forbid peeking-to-stop and HARKing. 6) Hand clean exposure/metric data to the statistics step.

**المعاملات:** intended split, unit of randomization

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** srm · assignment · exposure · تجارب · تسجيل

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2291-experimentation-growth-engineering/8764-ab-test-plumbing`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`

#### 7. قدرات قريبة في العائلة

- `ADATA-26` استرجاع ملفات CSV الفوضوية دون فقد صفوف / Recover messy CSV/TSV without losing rows (documented)
- `ADATA-27` تمييز الإشارة عن الضجيج في مؤشرات اللوحات / Signal-vs-noise annotation for dashboard metrics (documented)
- `ADATA-29` فهرس البيانات ووسم PII والنسب / Catalog, PII tagging and lineage setup (documented)
- `ADATA-30` حارس مخاطر Delta والبث / Delta and streaming foot-gun guard (documented)

### `ADATA-29` — فهرس البيانات ووسم PII والنسب / Catalog, PII tagging and lineage setup

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يبني فهرس بيانات مع وسم الأعمدة الحساسة والنسب وتنقية العينات. — Build a maintained data catalog with sensitive-column tagging and lineage, and scrub samples.

**متى:** Governance request or sharing example data from a dbt output.

**كيف:** 1) Automated PII discovery and column-level tags. 2) Capture lineage from runs. 3) Certify canonical metrics and trusted tables. 4) For sample data, use non-production profile and scrub classified columns.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** catalog · lineage · PII · حوكمة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2268-data-governance-privacy/8644-catalog-and-lineage`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1371-dataproduct-builder-dbt/3180-dataproduct-exampledata`

#### 7. قدرات قريبة في العائلة

- `ADATA-27` تمييز الإشارة عن الضجيج في مؤشرات اللوحات / Signal-vs-noise annotation for dashboard metrics (documented)
- `ADATA-28` بنية تجارب موثوقة مع فحص SRM / Trustworthy experiment plumbing with SRM check (documented)
- `ADATA-30` حارس مخاطر Delta والبث / Delta and streaming foot-gun guard (documented)
- `ADATA-31` تشخيص فشل المزامنة وصحة المصادر / Diagnose failing warehouse syncs and source health (documented)

### `ADATA-30` — حارس مخاطر Delta والبث / Delta and streaming foot-gun guard

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يمنع العمليات المدمرة على جداول البث ويعالج أعطال التزامن ونقاط التحقق. — Prevent destructive Delta operations on streamed tables and recover from concurrency or checkpoint failures.

**متى:** ConcurrentAppend errors, stream breaks after VACUUM, Auto Loader stops on new column, DLT full refresh.

**كيف:** 1) Check active streaming consumers before DROP, CREATE OR REPLACE or VACUUM. 2) Narrow MERGE predicates to clustering keys. 3) Keep VACUUM retention beyond checkpoint and time-travel needs. 4) Auto Loader: plan for schema evolution. 5) Confirm source replayability before DLT full refresh. 6) Hook fails open if consumers cannot be verified.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** delta · streaming · hook · حماية

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1844-databricks-pack/5462-databricks-streaming-guardian`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1844-databricks-pack/5460-databricks-cluster-forensics`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2276-databricks-lakehouse-engineering/8688-design-medallion-lakehouse`

#### 7. قدرات قريبة في العائلة

- `ADATA-28` بنية تجارب موثوقة مع فحص SRM / Trustworthy experiment plumbing with SRM check (documented)
- `ADATA-29` فهرس البيانات ووسم PII والنسب / Catalog, PII tagging and lineage setup (documented)
- `ADATA-31` تشخيص فشل المزامنة وصحة المصادر / Diagnose failing warehouse syncs and source health (documented)
- `ADATA-32` هيكلة مشروع dbt بطبقات وCI / Layered dbt project scaffold with CI (documented)

### `ADATA-31` — تشخيص فشل المزامنة وصحة المصادر / Diagnose failing warehouse syncs and source health

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يفحص كل المصادر ويجد المزامنات المعطلة ويوصي بإجراء الإصلاح المناسب. — Audit all warehouse sources, find broken syncs and recommend the matching recovery action.

**متى:** A synced table is stale, missing or erroring.

**كيف:** 1) List all sources and schemas with status. 2) Classify errors: credentials, schema drift, wrong incremental field, rate limit. 3) Map each class to a recovery (reconnect, tune config, reload, resync). 4) Report degraded sources ranked by staleness. 5) Verify after the fix.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** diagnosis · warehouse · health · تشخيص

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2957-posthog/12303-diagnosing-failed-warehouse-syncs`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2957-posthog/12265-auditing-warehouse-source-health`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2957-posthog/12413-tuning-incremental-sync-config`

#### 7. قدرات قريبة في العائلة

- `ADATA-29` فهرس البيانات ووسم PII والنسب / Catalog, PII tagging and lineage setup (documented)
- `ADATA-30` حارس مخاطر Delta والبث / Delta and streaming foot-gun guard (documented)
- `ADATA-32` هيكلة مشروع dbt بطبقات وCI / Layered dbt project scaffold with CI (documented)
- `ADATA-33` تصميم ميدالية ومنهج الاستيعاب / Medallion lakehouse and ingestion method choice (documented)

### `ADATA-32` — هيكلة مشروع dbt بطبقات وCI / Layered dbt project scaffold with CI

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يبني مشروع dbt بطبقات واضحة واختبارات وتوثيق وسير CI عند كل طلب دمج. — Scaffold a dbt project with sources, staging, intermediate and marts layers, tests, docs and a PR build workflow.

**متى:** Greenfield warehouse, or an ungoverned dbt project with no tests or marts reading raw.

**كيف:** 1) Layout: models/staging (one model per source table, cast/rename only), intermediate (private int_*), marts (fct_/dim_ BI contract), seeds, snapshots, macros. 2) Rules: staging uses source(); marts use ref() only; BI never reads int_*. 3) Add source freshness, generic tests (unique, not_null, relationships) plus singular tests. 4) Doc blocks for every model. 5) Separate build role and query role. 6) CI runs dbt build on PR; keep profiles.yml out of git, ship profiles.yml.example.

**المعاملات:** warehouse target, source systems, env promotion (dev/prod)

**التثبيت:** pip install dbt-core

**الوسوم:** dbt · scaffold · نمذجة · CI

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2270-data-platform/8659-dbt-project-scaffolding`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2233-analytics-engineering/8485-dbt-modeling`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2207-majestic-data/8249-dbt-development`

#### 7. قدرات قريبة في العائلة

- `ADATA-30` حارس مخاطر Delta والبث / Delta and streaming foot-gun guard (documented)
- `ADATA-31` تشخيص فشل المزامنة وصحة المصادر / Diagnose failing warehouse syncs and source health (documented)
- `ADATA-33` تصميم ميدالية ومنهج الاستيعاب / Medallion lakehouse and ingestion method choice (documented)
- `ADATA-34` عقد خط بيانات: الحبيبية والتكرار الآمن / Pipeline contract: grain, idempotency, checkpoints (documented)

### `ADATA-33` — تصميم ميدالية ومنهج الاستيعاب / Medallion lakehouse and ingestion method choice

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT/Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يختار طبقات برونز وفضي وذهبي وطريقة الاستيعاب انطلاقاً من أهداف الاستعلام والحداثة. — Pick bronze/silver/gold layering and the ingestion method backward from query and freshness SLOs.

**متى:** Designing a lakehouse or choosing among mirroring, copy job, pipelines and dataflows.

**كيف:** 1) State queries and freshness SLO. 2) Decide what earns each layer. 3) Match method to source: mirroring, copy job, pipeline, dataflow, JDBC import. 4) Prefer managed Iceberg or Delta tables with compaction. 5) Document trade-offs and cost.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** lakehouse · medallion · ingestion · بحيرة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2276-databricks-lakehouse-engineering/8688-design-medallion-lakehouse`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2337-microsoft-fabric/8978-fabric-ingestion-method-selection`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/366-aws-data-analytics/1348-ingesting-into-data-lake`

#### 7. قدرات قريبة في العائلة

- `ADATA-31` تشخيص فشل المزامنة وصحة المصادر / Diagnose failing warehouse syncs and source health (documented)
- `ADATA-32` هيكلة مشروع dbt بطبقات وCI / Layered dbt project scaffold with CI (documented)
- `ADATA-34` عقد خط بيانات: الحبيبية والتكرار الآمن / Pipeline contract: grain, idempotency, checkpoints (documented)
- `ADATA-35` ضبط Spark بالأدلة أولاً / Spark and Databricks evidence-first tuning (documented)

### `ADATA-34` — عقد خط بيانات: الحبيبية والتكرار الآمن / Pipeline contract: grain, idempotency, checkpoints

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يكتب عقد الخط ويختار استراتيجية التحميل قبل تنفيذ أي ETL أو ELT أو CDC. — Write a pipeline contract and pick a load strategy before implementing any ETL/ELT/CDC job.

**متى:** Designing a new batch or incremental load, or a replay/backfill requirement.

**كيف:** 1) Capture inputs: source/target grain, natural and dedup keys, volume, cadence, late-arriving and delete behaviour, backfill needs. 2) Contract: cursor, write behaviour, delete handling, validation boundary, publication condition, owner. 3) Strategy table: small stable -> full refresh with atomic swap; ordered cursor -> incremental with overlap + upsert; change log -> CDC; immutable events -> append+dedup; no change signal -> snapshot diff. 4) Never advance the checkpoint before durable publish and validation. 5) Add bad-record path and run metadata.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ETL · idempotency · CDC · تصميم

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2207-majestic-data/8244-data-pipeline-design`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/438-change-data-capture/1467-cdc`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2270-data-platform/8651-airbyte-cdk-authoring`

#### 7. قدرات قريبة في العائلة

- `ADATA-32` هيكلة مشروع dbt بطبقات وCI / Layered dbt project scaffold with CI (documented)
- `ADATA-33` تصميم ميدالية ومنهج الاستيعاب / Medallion lakehouse and ingestion method choice (documented)
- `ADATA-35` ضبط Spark بالأدلة أولاً / Spark and Databricks evidence-first tuning (documented)
- `ADATA-36` خطة اختبار لخطوط ETL وdbt / Test plan for ETL and dbt pipelines (documented)

### `ADATA-35` — ضبط Spark بالأدلة أولاً / Spark and Databricks evidence-first tuning

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يشخص مهام Spark البطيئة من الواجهة وخطة الاستعلام ثم يطبق الإصلاح المناسب. — Diagnose slow or spilling Spark jobs from Spark UI and query plan, then apply the matching fix and cost cut.

**متى:** A job is slow, spills, OOMs or the DBU bill is high.

**كيف:** 1) Read stage timeline, task-time skew, shuffle spill, GC, plan. 2) Map: one task far longer -> AQE skew join or salting; small dim -> broadcast; tiny files -> OPTIMIZE; driver OOM -> no collect(). 3) Prefer AQE and built-ins over conf knobs; replace Python UDFs. 4) Re-run and confirm the metric moved. 5) Cost: auto-terminate, jobs compute, spot workers, right-size warehouses.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** spark · databricks · performance · أداء

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2276-databricks-lakehouse-engineering/8689-tune-spark-and-costs`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2765-oracle-ai-data-platform-workbench-engine/11006-aidp-spark-optimization`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1844-databricks-pack/5460-databricks-cluster-forensics`

#### 7. قدرات قريبة في العائلة

- `ADATA-33` تصميم ميدالية ومنهج الاستيعاب / Medallion lakehouse and ingestion method choice (documented)
- `ADATA-34` عقد خط بيانات: الحبيبية والتكرار الآمن / Pipeline contract: grain, idempotency, checkpoints (documented)
- `ADATA-36` خطة اختبار لخطوط ETL وdbt / Test plan for ETL and dbt pipelines (documented)
- `ADATA-37` ضبط نوع مزامنة المستودع والحقل التزايدي / Tune warehouse sync type and incremental field (documented)

### `ADATA-36` — خطة اختبار لخطوط ETL وdbt / Test plan for ETL and dbt pipelines

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يصمم بيانات اختبار وفحوصاً للتحويلات والعقود وإعادة التشغيل والمطابقة. — Design fixtures and tests for transforms, contracts, incrementality, replay and reconciliation.

**متى:** Verifying a pipeline or dbt model change before merge.

**كيف:** 1) Tiny deterministic fixtures covering duplicates, nulls, late rows, deletes. 2) Contract tests on schema and keys. 3) Run the incremental model twice and on a replay; results must be identical. 4) Reconcile source vs target counts and sums. 5) Failure-path tests for bad records and partial failure. 6) Run in a non-production profile.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** testing · dbt · fixtures · اختبار

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2207-majestic-data/8245-data-pipeline-testing`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2207-majestic-data/8249-dbt-development`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3081-data-engineering/13249-dbt-transformation-patterns`

#### 7. قدرات قريبة في العائلة

- `ADATA-34` عقد خط بيانات: الحبيبية والتكرار الآمن / Pipeline contract: grain, idempotency, checkpoints (documented)
- `ADATA-35` ضبط Spark بالأدلة أولاً / Spark and Databricks evidence-first tuning (documented)
- `ADATA-37` ضبط نوع مزامنة المستودع والحقل التزايدي / Tune warehouse sync type and incremental field (documented)
- `ADATA-38` مراجعة مخطط واستعلامات ClickHouse / ClickHouse schema and query rule review (documented)

### `ADATA-37` — ضبط نوع مزامنة المستودع والحقل التزايدي / Tune warehouse sync type and incremental field

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يغير نوع مزامنة جدول المستودع بين كامل وتزايدي وCDC بأمان. — Change a warehouse table sync between full refresh, incremental, append, CDC or webhook safely.

**متى:** A sync is too slow, too frequent, or its incremental column or primary key is wrong.

**كيف:** 1) Read current config first; do not tune a running schema. 2) Refresh candidate incremental fields from the source. 3) Patch sync_type, incremental_field (matching real type), primary_key_columns (required for CDC), cdc_table_mode, sync_frequency. 4) Run CDC prerequisite check for Postgres. 5) Trigger reload; use resync only when old data is invalid. 6) Confirm last_synced_at advanced.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** sync · incremental · CDC · مزامنة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2957-posthog/12413-tuning-incremental-sync-config`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2957-posthog/12303-diagnosing-failed-warehouse-syncs`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2957-posthog/12265-auditing-warehouse-source-health`

#### 7. قدرات قريبة في العائلة

- `ADATA-35` ضبط Spark بالأدلة أولاً / Spark and Databricks evidence-first tuning (documented)
- `ADATA-36` خطة اختبار لخطوط ETL وdbt / Test plan for ETL and dbt pipelines (documented)
- `ADATA-38` مراجعة مخطط واستعلامات ClickHouse / ClickHouse schema and query rule review (documented)
- `ADATA-39` استعلام DuckDB على ملفات محلية أو S3 / DuckDB attach, query and read local or S3 data (documented)

### `ADATA-38` — مراجعة مخطط واستعلامات ClickHouse / ClickHouse schema and query rule review

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0 / MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** راجع مخططات واستعلامات ClickHouse وفق قواعد محددة مع استكشاف آمن. — Review ClickHouse schemas/queries against a rule set (ORDER BY, partitioning, inserts) and run safe agent discovery.

**متى:** CREATE TABLE review, slow analytical query, ingest design.

**كيف:** 1) Connect via MCP or CLI. 2) Discover databases, tables, columns, sort keys, skip indexes, sample rows, EXPLAIN. 3) Check rules per category (schema, query, insert, agent) and cite rule names. 4) Always LIMIT and set timeouts; narrow filters on memory errors. 5) Design MergeTree ORDER BY, TTL, batch inserts; monitor with system tables.

**المعاملات:** ddl or query

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** clickhouse · olap · مراجعة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1118-clickhouse/2556-clickhouse-best-practices`

#### 7. قدرات قريبة في العائلة

- `ADATA-36` خطة اختبار لخطوط ETL وdbt / Test plan for ETL and dbt pipelines (documented)
- `ADATA-37` ضبط نوع مزامنة المستودع والحقل التزايدي / Tune warehouse sync type and incremental field (documented)
- `ADATA-39` استعلام DuckDB على ملفات محلية أو S3 / DuckDB attach, query and read local or S3 data (documented)
- `ADATA-40` ضبط استعلامات SQL والفهارس بالأدلة / Evidence-first SQL query and index tuning (documented)

### `ADATA-39` — استعلام DuckDB على ملفات محلية أو S3 / DuckDB attach, query and read local or S3 data

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** اربط ملف DuckDB واستكشف المخطط واستعلم عن ملفات CSV وParquet وS3 بـ SQL. — Attach a DuckDB file, explore schema, persist a state.sql, and query CSV/Parquet/JSON/SQLite or S3 files with SQL.

**متى:** Ad-hoc analytics on files without a server.

**كيف:** 1) Resolve absolute path, check file exists. 2) command -v duckdb; validate with PRAGMA version. 3) List duckdb_tables(), columns, row counts. 4) Write state.sql and reuse via duckdb -init state.sql -c query. 5) read_csv/read_parquet/httpfs for files and S3/R2/GCS; spatial extension for geo. 6) chDB for ClickHouse-flavoured local SQL.

**المعاملات:** db path, SQL

**التثبيت:** pip install duckdb

**الوسوم:** duckdb · parquet · sql · استعلام

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:duckdb` ← python3 -c "import duckdb" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1366-duckdb-skills/3103-attach-db`

#### 7. قدرات قريبة في العائلة

- `ADATA-37` ضبط نوع مزامنة المستودع والحقل التزايدي / Tune warehouse sync type and incremental field (documented)
- `ADATA-38` مراجعة مخطط واستعلامات ClickHouse / ClickHouse schema and query rule review (documented)
- `ADATA-40` ضبط استعلامات SQL والفهارس بالأدلة / Evidence-first SQL query and index tuning (documented)
- `ADATA-41` إدارة Milvus وZilliz عبر الأوامر / Milvus and Zilliz admin via CLI (documented)

### `ADATA-40` — ضبط استعلامات SQL والفهارس بالأدلة / Evidence-first SQL query and index tuning

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** اقرأ خطة التنفيذ واختر نوع الفهرس المناسب وأعد كتابة الاستعلام لتحسين الأداء بقياس فعلي. — Read EXPLAIN ANALYZE output, pick the right index type and rewrite the query to be sargable, yielding a measured speedup.

**متى:** Slow query, slow endpoint, N+1 suspicion, index design question.

**كيف:** 1) Capture EXPLAIN (ANALYZE, BUFFERS); note seq scans, bad row estimates, costly sorts. 2) Map predicate to index: equality/range B-tree, subset partial, multi-column composite by selectivity, INCLUDE covering, jsonb/text GIN. 3) Rewrite: no function on indexed column, no SELECT *, batch instead of loop, join/IN for N+1. 4) Refresh stats (ANALYZE/autovacuum) before adding more indexes. 5) Re-run plan and compare.

**المعاملات:** query text, plan output, dialect

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** sql · explain · index · فهارس · أداء

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2274-database-engineering/8681-query-and-index-tuning`

#### 7. قدرات قريبة في العائلة

- `ADATA-38` مراجعة مخطط واستعلامات ClickHouse / ClickHouse schema and query rule review (documented)
- `ADATA-39` استعلام DuckDB على ملفات محلية أو S3 / DuckDB attach, query and read local or S3 data (documented)
- `ADATA-41` إدارة Milvus وZilliz عبر الأوامر / Milvus and Zilliz admin via CLI (documented)
- `ADATA-42` من اللغة الطبيعية إلى استعلام MongoDB / Natural-language to MongoDB query and schema design (documented)

### `ADATA-41` — إدارة Milvus وZilliz عبر الأوامر / Milvus and Zilliz admin via CLI

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يدير قواعد المتجهات والفهارس والمستخدمين والأدوار. — Manage vector databases, indexes, users, roles and projects.

**متى:** vector DB admin

**كيف:** 1) Create/list/drop databases. 2) Create indexes on collections. 3) Manage users, roles, privileges. 4) Cloud ACL and projects. Confirm drops.

**المعاملات:** cluster

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** milvus · vector · متجهات

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3616-zilliz/14557-index`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3616-zilliz/14567-user-role`

#### 7. قدرات قريبة في العائلة

- `ADATA-39` استعلام DuckDB على ملفات محلية أو S3 / DuckDB attach, query and read local or S3 data (documented)
- `ADATA-40` ضبط استعلامات SQL والفهارس بالأدلة / Evidence-first SQL query and index tuning (documented)
- `ADATA-42` من اللغة الطبيعية إلى استعلام MongoDB / Natural-language to MongoDB query and schema design (documented)
- `ADATA-43` تشخيص استعلامات Postgres البطيئة بـ EXPLAIN / Postgres slow-query diagnosis with EXPLAIN (documented)

### `ADATA-42` — من اللغة الطبيعية إلى استعلام MongoDB / Natural-language to MongoDB query and schema design

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** اجلب الفهارس والمخطط وعينات ثم ولّد استعلام find أو aggregation للقراءة فقط. — Fetch indexes, schema and samples, validate fields, then emit a read-only find or aggregation pipeline; advise schema patterns.

**متى:** MongoDB query writing, optimization, modeling.

**كيف:** 1) list DBs/collections. 2) collection-indexes, collection-schema (sampleSize 50), find limit 4. 3) Validate every field name. 4) Prefer find; use aggregation only for grouping or multi-stage. 5) Check query uses an index; apply embed-vs-reference schema patterns; tune connection pools/timeouts.

**المعاملات:** db, collection, request

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** mongodb · nosql · aggregation · استعلام

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2540-mongodb/9854-mongodb-natural-language-querying`

#### 7. قدرات قريبة في العائلة

- `ADATA-40` ضبط استعلامات SQL والفهارس بالأدلة / Evidence-first SQL query and index tuning (documented)
- `ADATA-41` إدارة Milvus وZilliz عبر الأوامر / Milvus and Zilliz admin via CLI (documented)
- `ADATA-43` تشخيص استعلامات Postgres البطيئة بـ EXPLAIN / Postgres slow-query diagnosis with EXPLAIN (documented)
- `ADATA-44` نمط الجداول الزمنية بوقت النظام / System-time temporal table pattern (documented)

### `ADATA-43` — تشخيص استعلامات Postgres البطيئة بـ EXPLAIN / Postgres slow-query diagnosis with EXPLAIN

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0 / MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحدد الاستعلامات الأبطأ ويقرأ الخطة الفعلية ويربط الأعراض بالحلول. — Find top time-consuming queries, read the real plan, and map plan symptoms to fixes.

**متى:** slow query, seq scan, missing index, vacuum bloat, lock/deadlock

**كيف:** 1) Rank pg_stat_statements by total_exec_time. 2) EXPLAIN (ANALYZE, BUFFERS) the culprit. 3) Compare estimated vs actual rows; large gap means ANALYZE the table. 4) Seq Scan on big table or Nested Loop: add index; Sort to disk: raise work_mem; heavy Filter: partial index. 5) Build with CREATE INDEX CONCURRENTLY; list idx_scan=0 indexes only after a full usage cycle. 6) Check n_dead_tup and autovacuum; VACUUM FULL last resort.

**المعاملات:** connection string, query text

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** postgres · explain · بطء الاستعلام · indexing

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2965-pwdev-devops/12480-postgres-dba`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2939-supabase/12194-supabase-postgres-best-practices`

#### 7. قدرات قريبة في العائلة

- `ADATA-41` إدارة Milvus وZilliz عبر الأوامر / Milvus and Zilliz admin via CLI (documented)
- `ADATA-42` من اللغة الطبيعية إلى استعلام MongoDB / Natural-language to MongoDB query and schema design (documented)
- `ADATA-44` نمط الجداول الزمنية بوقت النظام / System-time temporal table pattern (documented)
- `ADATA-45` سجل تدقيق للتغييرات في قاعدة البيانات / Trigger-based database audit trail (documented)

### `ADATA-44` — نمط الجداول الزمنية بوقت النظام / System-time temporal table pattern

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يؤرشف الصفوف بإضافة فقط مع system_from وsystem_to وقيمة مستقبلية. — Version rows append-only with system_from/system_to and a far-future sentinel.

**متى:** audit history, rollback, sync/merge

**كيف:** 1) Columns system_from, system_to NOT NULL, sentinel 9999-12-31 23:59:59. 2) PK (id, system_to); index (id, system_from). 3) Update = phase out old row, insert new with contiguous timestamps. 4) Skip when incoming equals current. 5) Rollback by phasing in prior version. 6) SQLite: recreate table to change PK.

**المعاملات:** table

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** temporal · versioning · سجل تاريخي

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2559-temporal-data/9928-temporal-data`

#### 7. قدرات قريبة في العائلة

- `ADATA-42` من اللغة الطبيعية إلى استعلام MongoDB / Natural-language to MongoDB query and schema design (documented)
- `ADATA-43` تشخيص استعلامات Postgres البطيئة بـ EXPLAIN / Postgres slow-query diagnosis with EXPLAIN (documented)
- `ADATA-45` سجل تدقيق للتغييرات في قاعدة البيانات / Trigger-based database audit trail (documented)
- `ADATA-46` تدقيق خط الاسترجاع على سبعة محاور / Seven-axis retrieval pipeline audit (documented)

### `ADATA-45` — سجل تدقيق للتغييرات في قاعدة البيانات / Trigger-based database audit trail

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** أنشئ جدول تدقيق ومشغلات تسجل القيم القديمة والجديدة والمستخدم والوقت. — Create an audit_log table plus triggers capturing old/new JSONB values, actor and timestamp for compliance.

**متى:** GDPR/HIPAA/SOX change tracking.

**كيف:** 1) Choose tables (PII, financial, access control) and operations. 2) Create audit_log(table_name, record_id, action, old_values JSONB, new_values JSONB, changed_by, changed_at, client_ip). 3) Generic trigger function per table. 4) Alternatives: app-level, CDC, native logs. 5) Plan 10-30 percent yearly storage, separate tablespace, retention/archival.

**المعاملات:** tables, ops, retention

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** audit · trigger · compliance · تدقيق

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1685-database-audit-logger/4689-implementing-database-audit-logging`

#### 7. قدرات قريبة في العائلة

- `ADATA-43` تشخيص استعلامات Postgres البطيئة بـ EXPLAIN / Postgres slow-query diagnosis with EXPLAIN (documented)
- `ADATA-44` نمط الجداول الزمنية بوقت النظام / System-time temporal table pattern (documented)
- `ADATA-46` تدقيق خط الاسترجاع على سبعة محاور / Seven-axis retrieval pipeline audit (documented)
- `ADATA-47` بوابة تسوية الحسابات قبل التقارير / Account reconciliation gate before reporting (documented)

### `ADATA-46` — تدقيق خط الاسترجاع على سبعة محاور / Seven-axis retrieval pipeline audit

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تدقيق خط RAG رقمياً عبر مجموعة التقييم والتقطيع وهندسة التضمين واسترجاع ANN والدمج وإعادة الترتيب. — Audit a RAG or vector index numerically across eval set, chunking, embedding geometry, ANN recall, fusion and reranking.

**متى:** Retrieval returns wrong or missing context, or before launching a RAG system.

**كيف:** 1) Check a labeled query set exists (else bootstrap; that is finding #1). 2) Chunking: size sweep, truncation beyond embedding context, dedup. 3) Geometry: anisotropy, effective rank, hubness, normalization. 4) ANN recall vs brute force, with production filters, tune ef/nprobe. 5) Composition: add sparse leg for exact-match corpora. 6) Fusion: use RRF, not raw score sums. 7) Reranker: check first-stage headroom and eval-gate lift. Rank findings with unretrievable docs first.

**المعاملات:** embedding model; index params; labeled queries

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** rag-audit · recall · vector-index · تدقيق

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:chromadb` ← python3 -c "import chromadb" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2530-retrieval-review/9827-retrieval-review`

#### 7. قدرات قريبة في العائلة

- `ADATA-44` نمط الجداول الزمنية بوقت النظام / System-time temporal table pattern (documented)
- `ADATA-45` سجل تدقيق للتغييرات في قاعدة البيانات / Trigger-based database audit trail (documented)
- `ADATA-47` بوابة تسوية الحسابات قبل التقارير / Account reconciliation gate before reporting (documented)

### `ADATA-47` — بوابة تسوية الحسابات قبل التقارير / Account reconciliation gate before reporting

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-data` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-data.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT/Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** مطابقة كل حساب بمصدر مستقل وتسوية البنود قبل إصدار القوائم. — Tie each bank and balance-sheet account to an independent source and clear reconciling items before statements ship.

**متى:** Bank rec, GL-to-subledger, intercompany rec or month-end close.

**كيف:** 1) List accounts needing tie-out. 2) Match each to statement or subledger and investigate variances. 3) Classify reconciling items (outstanding checks, deposits in transit, timing). 4) Block reporting until reconciled; output a status.

**المعاملات:** GL balances, statements

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** reconciliation · accounting · close · تسوية

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:ADATA-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2228-accounting-bookkeeping/8461-reconcile-accounts`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/321-finance/975-reconciliation`

#### 7. قدرات قريبة في العائلة

- `ADATA-45` سجل تدقيق للتغييرات في قاعدة البيانات / Trigger-based database audit trail (documented)
- `ADATA-46` تدقيق خط الاسترجاع على سبعة محاور / Seven-axis retrieval pipeline audit (documented)

