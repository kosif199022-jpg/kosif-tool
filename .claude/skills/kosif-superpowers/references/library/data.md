# البيانات والرسوم والمواقع — Data & visual analytics (`data`)

> مكتبة بروتوكول USIP v5.5، مولّدة بـ `scripts/smart_capabilities.py library` من `data/powers/*.json` و`data/tools.json`؛ لا تُحرَّر يدويًا. الدليل: [A28 اختيار القدرات](../protocol/A28-capability-routing.md) · [الفهرس](INDEX.md) · [النواة](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

## الفهرس / contents

- [متى تستخدم هذه المجموعة / when](#متى-تستخدم-هذه-المجموعة--when)
- [الحالة بالأرقام / status](#الحالة-بالأرقام--status)
- [الأدوات القابلة للتشغيل / runnable tools](#الأدوات-القابلة-للتشغيل--runnable-tools)
- [العائلات / families](#العائلات--families)
- [كل القدرات / every power](#كل-القدرات--every-power)

## متى تستخدم هذه المجموعة / when

كلمات التوجيه: data chart dashboard graph excel map gis analytics بيانات إكسل رسوم مخطط خرائط

خط العمل المقترح (هدف تصميم، لم يُختبر كوحدة واحدة): الاستيراد والتنظيف → التحليل → الرسم والخرائط → التصدير

العضوية في المجموعة تصنيف للتوجيه، لا دليل على أن القدرات تعمل معًا: اربطها بخط عمل مختبر فقط.

## الحالة بالأرقام / status

| الحالة | العدد | المعنى |
|---|---:|---|
| `proven` | 49 | ✅ proven: a proof exists in the catalog; still check its requirements here before calling it ready |
| `ready` | 18 | 🟢 ready: runnable without setup according to the catalog |
| `documented` | 105 | 📄 documented: a described method; needs building or wiring before it runs |
| `seen` | 48 | 👁 seen: observed in a reference or demo, not executed here |
| `install` | 34 | 📦 install: needs a package, binary or model first |
| `key` | 7 | 🔑 key: needs an account, key or paid service (ask before any spend) |
| `idea` | 1 | 💡 idea: not built |
| **المجموع** | **262** | |

## الأدوات القابلة للتشغيل / runnable tools

| الأداة | ما تفعله | ابدأ بـ | الدليل |
|---|---|---|---|
| `repo-sync-catalog` | مزامنة الكتالوج مع PromptsMotion | `python3 tools/sync_catalog.py` | untested |
| `starter-remotion` | قالب فيلم Remotion | `python3 tools/kosif.py scaffold product ./my-film --starter remotion` | tested-elsewhere |

الأوامر نسبية إلى مجلد المهارة (أو جذر المستودع لأدوات `tools/`)؛ `python3 scripts/hub.py tool <id>` يعطي كل الأوامر والمتطلبات والحدود.

## العائلات / families

| العائلة | القدرات | الفصل |
|---|---:|---|
| `atlas-data` | 56 | [atlas-data.md](../powers/atlas-data.md) |
| `charts-data-infographic` | 105 | [charts-data-infographic.md](../powers/charts-data-infographic.md) |
| `data-analysis` | 39 | [data-analysis.md](../powers/data-analysis.md) |
| `maps-geo` | 62 | [maps-geo.md](../powers/maps-geo.md) |

## كل القدرات / every power

مرتبة بالحالة ثم العائلة ثم المعرّف. `hub.py` و`skill_intelligence.py deep <ID>` يعطيان بطاقة القدرة كاملة بدليلها.

| المعرّف | الاسم | English | الحالة | المتطلبات |
|---|---|---|---|---|
| `DATA-19` | العدّاد التصاعدي بأرقام ثابتة العرض | Tabular count-up counter | proven | node, chromium, fonts:arabic |
| `DATA-20` | قالب stat-counter: رقم مع حلقة | stat-counter template (count + drawn ring) | proven | python3, fonts:arabic |
| `DATA-29` | الرقم المنطوق يصبح حلقة ساعة | Spoken number → clock-ring motif | proven |  |
| `DATA-50` | خط يُرسم مع مساحة ونقاط تقفز | Line draw-on with area fade & dot pops | proven |  |
| `DATA-55` | الخطوط المصغرة | Sparklines & micro-charts | proven | python3 |
| `DATA-83` | مخطط بنفورد للرقم الأول | Benford first-digit chart | proven |  |
| `DATA-92` | لوحات ألوان الرسوم | Chart palettes (categorical, sequential, semantic) | proven | npm:react |
| `DATA-94` | لوحة التوأم الإنشائي | Structural-twin dashboard & utilisation ramp | proven | python3 |
| `DATA-95` | ملف إكسل برسوم أصلية | Excel workbook with native charts | proven | pip:office |
| `ANLY-01` | تحليل الجداول بـ pandas | pandas groupby / pivot analysis | proven | pip:pandas |
| `ANLY-02` | SQL مباشرة على ملفات CSV بـ DuckDB | DuckDB SQL straight on CSV/Parquet | proven | pip:duckdb |
| `ANLY-03` | تصدير Parquet وقراءته | Parquet export and read-back | proven | pip:duckdb |
| `ANLY-04` | polars للجداول الكبيرة | polars fast DataFrames (v2 API) | proven | pip:polars |
| `ANLY-05` | ملفات CSV عربية تفتح صحيحة في Excel | Arabic-safe CSV (utf-8-sig) | proven |  |
| `ANLY-06` | حل رياضي دقيق بـ sympy | Exact symbolic solving with sympy | proven | pip:sympy |
| `ANLY-07` | اختبارات إحصائية وانحدار بـ scipy | scipy.stats regression and tests | proven | pip:scipy |
| `ANLY-08` | نماذج إحصائية بـ statsmodels | statsmodels OLS and time-series models | proven | python3 |
| `ANLY-09` | محاكاة مونت كارلو للمخاطر | Seeded Monte Carlo risk check | proven | pip:numpy, npm:p5 |
| `ANLY-10` | رسم بياني بعناوين عربية في matplotlib | matplotlib charts with Arabic labels | proven | pip:matplotlib, fonts:arabic |
| `ANLY-11` | اكتشاف libraqm قبل تشكيل العربية | Detect libraqm before shaping Arabic | proven | pip:pillow, pip:matplotlib, pip:arabic-reshaper |
| `ANLY-12` | فحص ألوان الرسم آليًا | Validate chart colours with the dataviz checker | proven | node |
| `ANLY-13` | رسوم تفاعلية HTML بـ plotly | plotly interactive HTML charts | proven | pip:plotly |
| `ANLY-14` | مواصفات Vega-Lite بـ altair | altair / Vega-Lite chart specs | proven | python3 |
| `ANLY-15` | رسوم إحصائية بـ seaborn | seaborn statistical plots | proven | pip:matplotlib |
| `ANLY-16` | تعلم آلي كلاسيكي بـ scikit-learn | scikit-learn classic ML | proven | pip:sklearn |
| `ANLY-17` | تعزيز متدرّج XGBoost وLightGBM | Gradient boosting (XGBoost, LightGBM) | proven | python3 |
| `ANLY-18` | برمجة خطية لمزيج المنتجات | Linear programming with scipy/HiGHS | proven | pip:scipy, pip:sympy |
| `ANLY-19` | OR-Tools للجدولة والمسارات | OR-Tools (LP/MIP/CP-SAT/routing) | proven | pip:ortools, pip:pulp |
| `ANLY-20` | تغيّر واجهة PuLP 4.0 | PuLP 4.0 API change | proven | pip:ortools, pip:pulp |
| `ANLY-21` | تحسين محدّب بـ cvxpy | Convex optimisation with cvxpy | proven | python3 |
| `ANLY-22` | حل قيود منطقية بـ z3 | z3 SMT constraint solving | proven | pip:z3 |
| `ANLY-23` | خوارزميات الرسوم البيانية بـ networkx | Graph algorithms with networkx | proven | python3 |
| `ANLY-24` | تحليل مكاني بـ geopandas | Spatial analysis (geopandas/shapely/pyproj) | proven | fonts:arabic, pip:geopandas, pip:shapely |
| `ANLY-26` | احسب في الكود ثم جمّد ثم اروِ | Compute in code, reconcile, freeze, then narrate | proven | pip:pandas |
| `ANLY-27` | بوابات نظافة SQL | SQL hygiene gates | proven |  |
| `ANLY-28` | بيانات اختبار معلنة ومبذورة | Seeded, labelled synthetic data | proven | pip:numpy |
| `ANLY-30` | SymPy: حل المعادلات وتبسيطها واشتقاقها وتكاملها بدقة رمزية | SymPy: Solve, simplify, differentiate and integrate exactly; export LaTeX | proven | latex, pip:sympy |
| `ANLY-31` | Z3 SMT solver: صياغة القيود وخصائص البرامج كمسائل SMT وإثباتها | Z3 SMT solver: Encode constraints or program properties as SMT and prove them or get a counterexample | proven | pip:z3 |
| `ANLY-33` | DuckDB: تنفيذ SQL مباشرة على ملفات CSV وParquet | DuckDB: Run SQL directly over multi-GB CSV/Parquet/JSON files in-process | proven | pip:duckdb |
| `ANLY-34` | Polars: تنظيف وتجميع جداول كبيرة بإطارات بيانات كسولة | Polars: Clean and aggregate large tables with lazy, multi-threaded dataframes | proven | pip:polars |
| `ANLY-35` | scikit-learn: تدريب نماذج التصنيف والانحدار على بيانات جدولية | scikit-learn: Train, cross-validate and explain classifiers and regressors on tabular data | proven | pip:sklearn |
| `ANLY-36` | StatsForecast: بناء توقعات AutoARIMA وETS مع فترات ثقة | StatsForecast: Fit AutoARIMA/ETS forecasts with prediction intervals on many series | proven | pip:statsforecast |
| `ANLY-37` | GeoPandas: ربط البيانات الجغرافية وإعادة إسقاطها بإحداثيات مترية | GeoPandas: Join, buffer and reproject vector geodata in true metric CRSs and export GeoJSON | proven | fonts:arabic, pip:geopandas |
| `ANLY-38` | Biopython: قراءة FASTA وGenBank وترجمة التسلسلات ومحاذاتها | Biopython: Parse FASTA/GenBank, translate and align sequences | proven | pip:biopython |
| `ANLY-39` | RDKit: قراءة صيغ SMILES وحساب الواصفات الجزيئية ورسم | RDKit: Parse SMILES, compute molecular descriptors and draw molecules | proven | pip:rdkit |
| `MAP-29` | تجهيز ممر الكاميرا | Camera corridor path preparation | proven |  |
| `MAP-31` | توحيد أسماء الأماكن العربية | Arabic place-name normalisation | proven | node |
| `MAP-45` | خريطة المملكة التخطيطية بالمناطق | Schematic Saudi Arabia map — 13 regions, drill-down | proven | node |
| `MAP-57` | عناصر خرائط أرشيفية | Archival map-fragment collage props | proven | node |
| `DATA-105` | أيقونة مخطط أعمدة | Mini bar-chart hero icon | ready |  |
| `DATA-25` | تنسيق الأرقام المختصر والمحلي | Compact & locale number formatting | ready |  |
| `DATA-32` | أرقام KPI بتدرج أو نيون | Gradient-clipped & neon KPI numerals | ready |  |
| `DATA-36` | أعمدة أفقية مرتبة مع تمييز واحد | Ranked horizontal bars with one highlight | ready |  |
| `DATA-38` | أعمدة مجمّعة أو مكدّسة مع خط | Grouped / stacked columns + line | ready |  |
| `DATA-39` | مخطط الشلال (الجسر) | Waterfall / bridge chart | ready | key:unspecified |
| `DATA-43` | مقاييس وأشرطة تقدم بلون الحكم | Verdict-coloured meters & RTL-safe progress | ready |  |
| `DATA-51` | خط يرسمه رأس قلم يحمل العدّاد | Pen-tip counter line | ready |  |
| `DATA-54` | خط/مساحة مع مؤشر تقاطع | SKCharts line/area with crosshair | ready |  |
| `DATA-58` | طبقة التعليقات والإبراز | Annotation & highlight layer | ready |  |
| `DATA-67` | حلقة التقدم المخروطية | Conic-gradient progress ring | ready |  |
| `DATA-68` | دونات بخدعة المحيط 100 | Donut via r = 15.915 dasharray | ready |  |
| `DATA-80` | خريطة حرارية تقويمية | Calendar heatmap grid | ready |  |
| `DATA-81` | خريطة المخاطر 3×3 بأربع درجات | 3×3 risk heatmap with 4-step scale | ready |  |
| `DATA-82` | جدول حرارة الصفوف × الأعمدة | Matrix intensity table | ready |  |
| `MAP-30` | مرساة التسمية في أبعد نقطة داخلية | Label anchor at pole of inaccessibility | ready | node |
| `MAP-43` | شريط نهر يُرسم ويجري | River ribbon reveal & flow | ready | npm:three |
| `MAP-46` | تدرّج الخريطة الأزرق | Sequential blue map heat ramp | ready |  |
| `ADATA-01` | خطوط معالجة آمنة التكرار وملء رجعي مضبوط | Idempotent pipeline steps, retries and safe backfills | documented |  |
| `ADATA-02` | استخراج الأنماط السيئة من سجلات جلسات الوكلاء | Mine agent session logs for anti-patterns | documented |  |
| `ADATA-03` | نشر استعلام محفوظ كنقطة API | Expose saved query as API endpoint | documented |  |
| `ADATA-04` | مطابقة الطلبات بين CRM وأدوات التحليل | Reconcile leads across CRM and analytics | documented |  |
| `ADATA-05` | أدوات تحليل سوق الكريبتو وDeFi | Crypto market and DeFi analytics CLI suite | documented | python3 |
| `ADATA-06` | ضرائب الكريبتو بطرق FIFO وLIFO وHIFO | Crypto tax gains with FIFO LIFO HIFO | documented |  |
| `ADATA-07` | تحليل بيانات السلسلة والمحفظة وندرة NFT | On-chain data, portfolio and NFT rarity analysis | documented |  |
| `ADATA-08` | استقبال الفواتير والإيصالات وأرشفتها | Invoice and receipt intake into archive | documented | tesseract |
| `ADATA-09` | نمذجة مونت كارلو وسيناريوهات ماذا لو | Monte Carlo and what-if scenario modeling | documented |  |
| `ADATA-10` | تحليل النسب والانحرافات والتوقع المتجدد | Ratio analysis, variance and rolling forecast | documented |  |
| `ADATA-11` | مقاييس خط المبيعات وكفاءة الدخول للسوق | SaaS pipeline and GTM efficiency metrics | documented |  |
| `ADATA-12` | محاسبة الأعمال الصغيرة: رواتب وضرائب وتحصيل | Small-business bookkeeping: payroll, tax, invoice chase | documented |  |
| `ADATA-13` | تحليل نتائج اختبار A/B مع حجم الأثر | A/B test result analysis with effect sizes | documented |  |
| `ADATA-14` | تخطيط حجم العينة وقوة اختبار A/B | A/B test sample size and power planning | documented |  |
| `ADATA-15` | تخطيط القدرة الإحصائية وحجم العينة | A priori power and sample-size planning | documented |  |
| `ADATA-16` | استكشاف البيانات الآمن المحدود | Bounded safe exploratory data profiling | documented |  |
| `ADATA-17` | تشخيص الأفواج والاحتفاظ ومسار التحويل | Cohort, retention and funnel diagnosis | documented |  |
| `ADATA-18` | تدقيق جودة البيانات مع خطة إصلاح | Dataset quality audit with scored remediation plan | documented | python3 |
| `ADATA-19` | قراءة نتائج تجربة A/B بحكم قابل للدفاع | Defensible A/B experiment readout and verdict | documented |  |
| `ADATA-20` | توقع الطلب مع بوابة الدقة | Demand forecast with accuracy gate | documented |  |
| `ADATA-21` | الإحصاء الوصفي وسرد التوزيعات | Descriptive statistics and distribution narrative | documented | pip:pandas, npm:p5 |
| `ADATA-22` | استكشاف البيانات المنضبط قبل النمذجة | Disciplined exploratory data analysis pass | documented |  |
| `ADATA-23` | التنبؤ بالمحركات ومراجعة نماذج الانحدار | Driver-based forecasts and regression review | documented |  |
| `ADATA-24` | سير عمل التحليل التجريبي بلغات بايثون وR وستاتا | Empirical analysis workflow in Python, R or Stata | documented | pip:pandas |
| `ADATA-25` | اختيار الاختبار الإحصائي وفحص الافتراضات | Guided test selection with assumption checks | documented |  |
| `ADATA-26` | استرجاع ملفات CSV الفوضوية دون فقد صفوف | Recover messy CSV/TSV without losing rows | documented |  |
| `ADATA-27` | تمييز الإشارة عن الضجيج في مؤشرات اللوحات | Signal-vs-noise annotation for dashboard metrics | documented |  |
| `ADATA-28` | بنية تجارب موثوقة مع فحص SRM | Trustworthy experiment plumbing with SRM check | documented |  |
| `ADATA-29` | فهرس البيانات ووسم PII والنسب | Catalog, PII tagging and lineage setup | documented |  |
| `ADATA-30` | حارس مخاطر Delta والبث | Delta and streaming foot-gun guard | documented |  |
| `ADATA-31` | تشخيص فشل المزامنة وصحة المصادر | Diagnose failing warehouse syncs and source health | documented |  |
| `ADATA-32` | هيكلة مشروع dbt بطبقات وCI | Layered dbt project scaffold with CI | documented | python3 |
| `ADATA-33` | تصميم ميدالية ومنهج الاستيعاب | Medallion lakehouse and ingestion method choice | documented |  |
| `ADATA-34` | عقد خط بيانات: الحبيبية والتكرار الآمن | Pipeline contract: grain, idempotency, checkpoints | documented |  |
| `ADATA-35` | ضبط Spark بالأدلة أولاً | Spark and Databricks evidence-first tuning | documented | python3 |
| `ADATA-36` | خطة اختبار لخطوط ETL وdbt | Test plan for ETL and dbt pipelines | documented |  |
| `ADATA-37` | ضبط نوع مزامنة المستودع والحقل التزايدي | Tune warehouse sync type and incremental field | documented |  |
| `ADATA-38` | مراجعة مخطط واستعلامات ClickHouse | ClickHouse schema and query rule review | documented |  |
| `ADATA-39` | استعلام DuckDB على ملفات محلية أو S3 | DuckDB attach, query and read local or S3 data | documented | pip:duckdb |
| `ADATA-40` | ضبط استعلامات SQL والفهارس بالأدلة | Evidence-first SQL query and index tuning | documented |  |
| `ADATA-41` | إدارة Milvus وZilliz عبر الأوامر | Milvus and Zilliz admin via CLI | documented |  |
| `ADATA-42` | من اللغة الطبيعية إلى استعلام MongoDB | Natural-language to MongoDB query and schema design | documented |  |
| `ADATA-43` | تشخيص استعلامات Postgres البطيئة بـ EXPLAIN | Postgres slow-query diagnosis with EXPLAIN | documented |  |
| `ADATA-44` | نمط الجداول الزمنية بوقت النظام | System-time temporal table pattern | documented |  |
| `ADATA-45` | سجل تدقيق للتغييرات في قاعدة البيانات | Trigger-based database audit trail | documented |  |
| `ADATA-46` | تدقيق خط الاسترجاع على سبعة محاور | Seven-axis retrieval pipeline audit | documented | pip:chromadb |
| `ADATA-47` | بوابة تسوية الحسابات قبل التقارير | Account reconciliation gate before reporting | documented |  |
| `ADATA-48` | تجهيز بيانات الضبط الدقيق وبطاقة البيانات | Fine-tuning dataset curation and dataset card | documented |  |
| `ADATA-49` | كشف الشذوذ بخط أساس ومعايرة وتفسير لكل إنذار | Anomaly detection with baseline, calibration and explained flags | documented |  |
| `ADATA-50` | التشريح المسبق: تعريف النجاح والفشل قبل البدء | Pre-mortem: define success and failure before starting | documented |  |
| `ADATA-51` | ضبط العمليات إحصائيًا: اختيار مخطط التحكم وقدرة العملية | Statistical process control: chart choice and capability | documented |  |
| `ADATA-52` | استخراج أرقام موثوقة من لوحة معلومات تُرسم في المتصفح | Trustworthy numbers from a client-rendered dashboard | documented |  |
| `ADATA-53` | تنفيذ خطة تتبع الأحداث مع بوابة schema في CI وموافقة المستخدم من المصدر | Event instrumentation from a tracking plan with CI schema gate and consent at source | documented | chromium |
| `ADATA-54` | تقييم أنظمة التوصية: تقسيم زمني وخط أساس شعبية والحكم للـA/B | Recommender evaluation: temporal split, popularity baseline, A/B as verdict | documented |  |
| `ADATA-55` | تدقيق مصدر الأصفار في مقاييس متعددة المصادر قبل تصديقها | Zero-provenance audit for multi-source metrics before believing a 0 | documented |  |
| `ADATA-56` | اختيار منهج جودة البيانات: اختبارات للقواعد المعروفة ومراقبة للمجهول وعقود عند المنتِج | Choose a data-quality approach: tests, monitors and contracts, and where each runs | documented | python3, npm:three |
| `DATA-01` | اختيار المخطط حسب السؤال | Chart choice by analytical question | documented |  |
| `DATA-02` | المسار أم الميل | Line path vs slope net-change | documented |  |
| `DATA-03` | اختيار مخطط التوزيع | Distribution chart choice | documented |  |
| `DATA-04` | رسم واحد لخلاصة واحدة وقوس القصة | One insight per chart & data story arc | documented |  |
| `DATA-05` | صفر حقيقي ومقياس موحد | True-zero baseline & shared scale | documented |  |
| `DATA-06` | أمانة المقاييس: المساحة واللوغاريتم والتطبيع | Scale honesty: area, log, normalization | documented |  |
| `DATA-07` | أشكال ممنوعة أو خطرة | Forbidden and risky chart forms | documented |  |
| `DATA-08` | قواعد الرسم الدائري | Pie rules | documented |  |
| `DATA-09` | المفقود ليس صفرًا | Missing, zero and censored are different | documented |  |
| `DATA-10` | لا أرقام مخترعة: مصدر أو «توضيحي» | No invented figures: source line or 'illustrative' | documented |  |
| `DATA-100` | تخطيطات إنفوجرافيك العمليات | Process infographic layouts | documented |  |
| `DATA-103` | أدوات التحليل الخلفية | Analysis back-office skills | documented | python3 |
| `DATA-11` | التسمية المباشرة بدل وسيلة الإيضاح | Direct labels over legends | documented |  |
| `DATA-12` | الترتيب حسب القيمة ونسبة الأبعاد | Sort by value & aspect by task | documented |  |
| `DATA-13` | البيانات المتحركة لها وزن واستمرارية | Data-in-motion weight & continuity | documented |  |
| `DATA-14` | ربط البيانات بقنوات الحركة | Mapping data to motion channels | documented |  |
| `DATA-15` | قيمة واحدة تقود الشكل والرقم | One-scalar rule (no bar springs) | documented |  |
| `DATA-16` | اتجاه المحاور في العربية | RTL chart axis conventions | documented |  |
| `DATA-17` | أحجام نصوص الرسوم | Chart type sizes | documented |  |
| `DATA-18` | نبضة التمييز وهرمية التركيز | Highlight pulse & focus hierarchy | documented |  |
| `DATA-49` | المضاعفات الصغيرة | Small multiples | documented |  |
| `DATA-69` | مسح الدائرة بزاوية واحدة | Pie sweep (one eased angle) | documented |  |
| `DATA-79` | مقياس إلى شيء مألوف | Scale to a familiar object | documented |  |
| `DATA-85` | تشريح بطاقة المؤشر | KPI card anatomy | documented |  |
| `DATA-89` | مخططات مشاهد البيانات في HyperFrames | HyperFrames data blueprints & categories | documented | npm:hyperframes |
| `DATA-91` | ستايل البيانات المتحركة الداكن | Data-in-Motion dark style | documented |  |
| `DATA-93` | رموز بطاقات البيانات التقنية | Tech-doc data-card tokens | documented |  |
| `DATA-99` | مشاهد السرد بالتمرير كبيانات | Scrollytelling scenes as data | documented |  |
| `ANLY-29` | هيكل نموذج الجداول المالية | Spreadsheet model structure | documented | libreoffice |
| `MAP-01` | هل نحتاج خريطة أصلًا | Map or not | documented |  |
| `MAP-02` | الخريطة الأساسية حسب الغرض | Basemap substrate by purpose | documented |  |
| `MAP-03` | اختيار نوع الخريطة الموضوعية | Thematic map family choice | documented |  |
| `MAP-04` | اختيار الإسقاط | Projection choice | documented | npm:d3 |
| `MAP-05` | تطبيع خرائط التظليل | Choropleth normalization | documented |  |
| `MAP-06` | استراتيجيات تداخل النقاط | Point overlap strategies | documented |  |
| `MAP-07` | طبقات تتكبر مع الخريطة وأخرى ثابتة | Map-space vs screen-stable layers | documented |  |
| `MAP-08` | سجل الإحداثيات والمصادر | Coordinate & source ledger | documented | fonts:arabic |
| `MAP-09` | الخرائط الحساسة والبيانات الإنسانية | Sensitive maps & human data | documented |  |
| `MAP-10` | توقيعات حركة الخرائط وضوابطها | Map motion signatures & restraint rules | documented | npm:d3, npm:maplibre |
| `MAP-11` | محرك واحد لكل لقطة | One map engine per shot (chooser) | documented | npm:remotion, npm:d3, npm:maplibre |
| `MAP-12` | لوحة خريطة ثابتة للموقع | Static locator map plate | documented | chromium, npm:remotion |
| `MAP-23` | طبقات المزود أم GeoJSON مخصص | Provider vectors vs custom GeoJSON | documented |  |
| `MAP-24` | متى GeoJSON ومتى البلاطات المتجهة | GeoJSON vs vector-tile threshold | documented |  |
| `MAP-25` | خط PMTiles وGeoParquet | PMTiles & GeoParquet pipeline | documented | npm:maplibre, pip:duckdb |
| `MAP-26` | التحليل المكاني بـ DuckDB | DuckDB spatial analysis | documented | pip:duckdb |
| `MAP-27` | بيانات Overture Maps المفتوحة | Overture Maps open data | documented | key:unspecified |
| `MAP-28` | OSM عبر Overpass لخطوط الأنهار والطرق | OSM via Overpass for centerlines | documented |  |
| `MAP-37` | خط زمني بمحطات وخريطة رحلة | Milestone timeline & map route (MG-045/046) | documented | npm:d3 |
| `MAP-40` | خريطة وثائقية | Documentary map | documented | python3 |
| `DATA-101` | الخطوط الزمنية المتحركة | Animated timelines & Gantt traces | seen | key:unspecified |
| `DATA-104` | تقاطع فن والأشرطة الطيفية | Venn overlap & spectrum indicator | seen |  |
| `DATA-22` | العدّاد المتخلخل والوميض | Scramble / flicker counter | seen |  |
| `DATA-26` | عدّاد يتلوّن مع تصاعد المشكلة | Threshold-colour escalation counter | seen |  |
| `DATA-27` | عدّاد التكلفة التراكمي | Cost-stack accumulation counter | seen |  |
| `DATA-28` | عدّادات HUD والسنوات والمسافة | HUD, year & distance counters | seen |  |
| `DATA-30` | شطب القيمة واستبدالها | Strike-and-replace value | seen |  |
| `DATA-31` | حاسبة حيّة بشريط تمرير | Slider-driven live calculator | seen |  |
| `DATA-33` | عدّاد حي فوق اللقطات | Live stat over footage | seen |  |
| `DATA-34` | كومة أرقام الضرر | MMO damage-number stack | seen |  |
| `DATA-40` | شريط النسب المقسّم (كبسولة) | Proportional split bar (segmented pill) | seen |  |
| `DATA-41` | زووم لوغاريتمي داخل شريحة | Log-domain zoom into a slice | seen |  |
| `DATA-42` | أعمدة بفترات ثقة | Bars with interval whiskers | seen |  |
| `DATA-44` | أشرطة مقسّمة إلى خانات | Segmented / dotted meters | seen |  |
| `DATA-45` | سباق المقارنة والسرعة | Speed / latency comparison race | seen |  |
| `DATA-46` | لوحة احتمالات الكلمة التالية | Next-token probability panel | seen |  |
| `DATA-47` | ترتيب يتغير والقوائم المرتبة | Rank swap & ranked lists | seen |  |
| `DATA-57` | الشموع وشريط الأسعار | Candlesticks & price ticker | seen |  |
| `DATA-60` | رسم بياني بخط اليد | Hand-drawn axis plot | seen |  |
| `DATA-61` | مروحة مونت كارلو وعدم اليقين | Monte Carlo fan & uncertainty | seen |  |
| `DATA-62` | هيستوغرام نقاط يصير منحنى جرس | Dot histogram resolving to a bell curve | seen |  |
| `DATA-63` | رسم الدوال والمشتقة حيًّا | Live function & derivative tracer | seen | python3 |
| `DATA-64` | راكب على خط المخطط | Glyph riding the chart path | seen |  |
| `DATA-65` | حقل خطوط الجبال | Ridge-line wave field | seen |  |
| `DATA-66` | مبعثر الحد الفعّال | Scatter with frontier curve | seen |  |
| `DATA-70` | دونات متوهجة مع قائمة | Glowing donut with legend | seen |  |
| `DATA-72` | مقاييس HUD الدائرية | HUD radial gauges | seen |  |
| `DATA-73` | مقياس السائل والمنسوب | Liquid-fill & level gauges | seen |  |
| `DATA-75` | رادار المسح | Radar sweep with pings | seen |  |
| `DATA-76` | نصف دائرة البرلمان وحلقة النقاط | Parliament hemicycle & dot ring | seen |  |
| `DATA-77` | مخطط الوافل: 100 نقطة | Waffle — 100 dots with synced percent | seen |  |
| `DATA-78` | مصفوفة الوحدات: نقطة لكل عنصر | Unit dot matrix (one dot per item) | seen |  |
| `DATA-84` | جدول يتكشف صفًّا صفًّا | Progressive table & status pills | seen |  |
| `DATA-86` | ثلاثية بطاقات الأرقام والإثبات | Stat-tile trio & proof cards | seen |  |
| `DATA-87` | افتتاحية الرقم البطل | Hero-number opener card | seen |  |
| `DATA-90` | ستايل الإنفوجرافيك بأسلوب أبل | Keynote infographic style | seen | python3 |
| `MAP-34` | إسقاط خطوط الطول والعرض على SVG | Equirectangular lon/lat → SVG with latitude squash | seen |  |
| `MAP-35` | متتبع مسار بطول القوس مع توقف | Arc-length route follower with dwell | seen |  |
| `MAP-36` | كاميرا الخريطة المائلة 2.5D | Tilted 2.5D map camera | seen |  |
| `MAP-38` | رسم مسار بمحطات تنبثق | Route line with popping station dots | seen |  |
| `MAP-39` | مسار تقدم على جبل | Progress path up terrain with avatar | seen |  |
| `MAP-53` | رسم خريطة شوارع وإسقاط دبابيس | SVG street map draw + pin drop | seen |  |
| `MAP-54` | خريطة نقاط تجمعات المدن | Dot-cluster city map | seen |  |
| `MAP-55` | خريطة عالم نقطية بكبسولات صور | Dotted world map with avatar pills | seen |  |
| `MAP-56` | خريطة أعمدة ضوئية | Spike map | seen |  |
| `MAP-60` | كرة أرضية نقطية بإسقاط كروي | Orthographic dot / halftone globe | seen | npm:d3 |
| `MAP-61` | كرة أرضية بأقواس اتصال | Globe with great-circle arcs (wireframe / particle) | seen |  |
| `MAP-62` | كرة غبار مع تسميات | Dust point-cloud globe with leader labels | seen | npm:three |
| `DATA-102` | الشبكات والمحاور والأقواس | Networks, hubs & brackets | install | npm:hyperframes |
| `DATA-21` | عداد الأسطوانة (أودوميتر) | Odometer digit roll | install | npm:hyperframes |
| `DATA-23` | عدّاد يكبر مع قيمته ونبضة الهبوط | Count-up with growing scale & landing punch | install | npm:hyperframes |
| `DATA-24` | ظهور الرقم بضبابية ورفع | Number pop-in with blur & lift | install | npm:hyperframes |
| `DATA-35` | نمو الأعمدة المتدرج | Staggered bar growth | install | npm:gsap, npm:remotion |
| `DATA-37` | سباق الأعمدة | Bar-chart race | install | chromium, npm:hyperframes |
| `DATA-52` | منحنى ناعم في Remotion | Remotion smooth cubic line | install | npm:remotion |
| `DATA-53` | مؤشر قراءة متحرك على المخطط | Chart scrub readout (playhead) | install | npm:hyperframes |
| `DATA-56` | صعود ثم انهيار | Rise-then-crash line metaphor | install | npm:hyperframes |
| `DATA-59` | تحوّل المخططات | Chart morph (bars → donut / line / scatter) | install | node |
| `DATA-71` | حلقة قياس مع عدّاد متزامن | Arc gauge with synced counter | install | npm:hyperframes |
| `DATA-74` | تعبئة النجوم والتقييم | Star-rating fill | install | npm:hyperframes |
| `DATA-88` | سجل HyperFrames للبيانات | HyperFrames data registry (components & blocks) | install | npm:gsap, npm:hyperframes |
| `DATA-96` | مكتبات الرسوم كإطارات فيديو | Chart libraries as video frames | install | chromium, npm:d3 |
| `ANLY-25` | تنبؤ الأعمال بـ prophet | Business forecasting with prophet | install | python3 |
| `ANLY-32` | Lean 4: كتابة براهين رياضية صورية والتحقق منها آليًا | Lean 4: Write and machine-check formal proofs of theorems | install | network, lean |
| `MAP-13` | MapLibre حتمي بلا واجهة | Deterministic headless MapLibre | install | chromium, npm:remotion, npm:maplibre |
| `MAP-14` | لوحة خريطة مجمّدة ضد الارتعاش | Frozen oversized plate (anti-shimmer) | install | npm:maplibre |
| `MAP-15` | خريطة حقيقية مخبوزة مع طبقة متجهات حية | Baked real basemap MP4 + live SVG overlay | install | chromium, npm:maplibre |
| `MAP-20` | أنماط VersaTiles المجانية | VersaTiles self-hosted styles | install | npm:maplibre |
| `MAP-21` | خطوط SDF والتسميات العربية على خرائط GL | SDF glyphs & Arabic labels on GL maps | install | npm:maplibre |
| `MAP-22` | تنظيف الخريطة الأساسية | Basemap decluttering | install | npm:maplibre |
| `MAP-32` | رسم مسار الدائرة العظمى | Great-circle route draw-on | install | npm:d3 |
| `MAP-33` | رحلة على خريطة حبر قديمة | Parchment map journey | install | node, fonts:arabic |
| `MAP-41` | رحلة طيران نيويورك–باريس | NYC–Paris flight block | install | npm:hyperframes, fonts:arabic |
| `MAP-42` | أقواس ضوء ترسم بين المدن (3D) | 3D light arcs between cities | install | npm:three |
| `MAP-47` | خرائط تظليل بكشف متتابع | Choropleth staggered-reveal blocks | install | npm:gsap, npm:hyperframes, npm:d3 |
| `MAP-48` | خريطة الفقاعات | Proportional bubble map | install | npm:hyperframes |
| `MAP-49` | خريطة التدفق | Origin–destination flow map | install | npm:hyperframes |
| `MAP-50` | خريطة سداسية | Hex tile map | install | npm:hyperframes |
| `MAP-51` | زووم دولة مع دائرة حمراء | Country zoom with red scribble circle | install | npm:hyperframes |
| `MAP-52` | علامات وتسميات داخل الخريطة | Map-native circle & symbol markers | install | npm:maplibre |
| `MAP-58` | كوكب الأرض مع غلاف جوي | Procedural Earth with atmosphere | install | npm:three |
| `MAP-59` | خريطة الأضواء من المدار | Orbit-at-night lights map | install | npm:three, fonts:arabic |
| `DATA-97` | مشاهد بسمة للبيانات وقوالب أفلامها | Basma chart scenes & data-film templates | key | node, key:unspecified |
| `DATA-98` | إنفوجرافيك مولَّد مستند إلى بحث | Search-grounded infographic generation | key | key:unspecified |
| `MAP-16` | Mapbox: كرة وأبنية ثلاثية الأبعاد | Mapbox globe & 3D buildings | key | npm:maplibre, key:unspecified |
| `MAP-17` | MapTiler: التحريك فوق طبقات المزود | MapTiler provider-layer animation | key | key:unspecified |
| `MAP-18` | طيران فوق التضاريس بـ Cesium | Cesium terrain flyover | key | key:unspecified |
| `MAP-19` | صور خرائط ثابتة من AWS | Amazon Location static maps | key | npm:maplibre, key:unspecified |
| `MAP-44` | إضاءة الدول عند وصول النهر | River-triggered country reveal | key | npm:d3, key:unspecified |
| `DATA-48` | مخطط أعمدة دائري / شعاعي | Radial / clockwise bar chart | idea |  |
