# `code-engineering` — البرمجة وبناء التطبيقات (26 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/code-engineering.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/software.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`CODE-01` ابحث قبل أن تبني](#code-01--ابحث-قبل-أن-تبني--search-first-adopt-extend-compose-build)
- [`CODE-02` الوثائق الحية قبل الذاكرة](#code-02--الوثائق-الحية-قبل-الذاكرة--live-docs-over-memory)
- [`CODE-03` إثبات حزمة في بيئة معزولة](#code-03--إثبات-حزمة-في-بيئة-معزولة--prove-a-package-in-an-isolated-venv)
- [`CODE-04` دليل التعرّف على مستودع](#code-04--دليل-التعرّف-على-مستودع--codebase-onboarding-guide)
- [`CODE-05` قائمة أثر التغيير](#code-05--قائمة-أثر-التغيير--change-impact-checklist)
- [`CODE-06` حقائق قبل أول تعديل](#code-06--حقائق-قبل-أول-تعديل--fact-forcing-before-the-first-edit)
- [`CODE-07` اتبع أسلوب المستودع القائم](#code-07--اتبع-أسلوب-المستودع-القائم--inherit-the-repos-style)
- [`CODE-08` التطوير بالاختبار أولًا](#code-08--التطوير-بالاختبار-أولًا--test-driven-development)
- [`CODE-09` حلقة التحقق بست مراحل](#code-09--حلقة-التحقق-بست-مراحل--six-phase-verification-loop)
- [`CODE-10` نقاط تفتيش وخط أساس للانحدار](#code-10--نقاط-تفتيش-وخط-أساس-للانحدار--checkpoints-regression-baselines-and-passk)
- [`CODE-11` حلقة التشخيص من الجذر](#code-11--حلقة-التشخيص-من-الجذر--root-cause-debugging-loop)
- [`CODE-12` إصلاح البناء بأقل فرق](#code-12--إصلاح-البناء-بأقل-فرق--minimal-diff-build-fixing)
- [`CODE-13` صيد الأعطال الصامتة](#code-13--صيد-الأعطال-الصامتة--silent-failure-and-click-path-hunt)
- [`CODE-14` حلقة تحسين أداء مقاسة](#code-14--حلقة-تحسين-أداء-مقاسة--measured-optimization-loop)
- [`CODE-15` معالجة أخطاء متينة](#code-15--معالجة-أخطاء-متينة--resilient-error-handling)
- [`CODE-16` قائمة مراجعة الكود](#code-16--قائمة-مراجعة-الكود--code-review-checklist)
- [`CODE-17` مراجعة طلب دمج بفريق وكلاء](#code-17--مراجعة-طلب-دمج-بفريق-وكلاء--pr-review-fan-out)
- [`CODE-18` إعادة هيكلة آمنة](#code-18--إعادة-هيكلة-آمنة--safe-refactoring)
- [`CODE-19` سجل قرار معماري](#code-19--سجل-قرار-معماري--architecture-decision-record)
- [`CODE-20` الحتمي أولًا والنموذج للذيل](#code-20--الحتمي-أولًا-والنموذج-للذيل--deterministic-first-model-for-the-tail)
- [`CODE-21` ذاكرة مؤقتة ببصمة المحتوى](#code-21--ذاكرة-مؤقتة-ببصمة-المحتوى--content-hash-cache)
- [`CODE-22` نظافة الإيداع وكلمات الحالة](#code-22--نظافة-الإيداع-وكلمات-الحالة--commit-hygiene--status-words)
- [`CODE-23` Hypothesis: اختبارات قائمة على الخصائص تولّد مدخلات فاشلة](#code-23--hypothesis-اختبارات-قائمة-على-الخصائص-تولّد-مدخلات-فاشلة--hypothesis-property-based-tests-that-generate-and-shrink-failing-inputs)
- [`CODE-24` Pandera: تعريف عقود بيانات لإطارات pandas وPolars وفرضها](#code-24--pandera-تعريف-عقود-بيانات-لإطارات-pandas-وpolars-وفرضها--pandera-declare-and-enforce-schemas-on-pandaspolars-dataframes-data-contracts)
- [`CODE-25` خريطة مستودع مرتبة بالأهمية](#code-25--خريطة-مستودع-مرتبة-بالأهمية--ranked-repository-map)
- [`CODE-26` تعديلات بكتل بحث واستبدال](#code-26--تعديلات-بكتل-بحث-واستبدال--searchreplace-edit-blocks)

## البطاقات / cards

### `CODE-01` — ابحث قبل أن تبني / Search-first: adopt, extend, compose, build

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** قبل كتابة كود جديد ابحث عن حزمة أو أداة أو مهارة أو مستودع يحلّ المشكلة، ثم قرّر: تبنَّ، أو وسّع، أو ركّب، أو ابنِ. — Before writing new code, look for a package, tool, skill or repo that already solves it, then adopt, extend, compose or build.

**متى:** any new feature, effect, parser, integration or utility

**كيف:** Step 0 — check which search channels work and say which you skipped: `rg --files`, `python3 -m pip --version`, `npm --version`, `gh auth status`, the MCP/deferred tool list, `ls ~/.claude/skills .claude/skills`. Then search in order: this repo → package registries (`pip index versions X`, `npm view X version`) → MCP servers and skills → GitHub (`gh search repos <kw> --sort stars`) → web. Score candidates on fit, maintenance, community, docs, licence, dependencies. Decide: exact maintained MIT/Apache match → Adopt; partial → Extend with a thin wrapper; several weak matches → Compose 2–3 small packages; none → Build, informed by what you read.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** search first · reuse · library · build vs buy · ابحث أولا · إعادة استخدام · مكتبة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-02` الوثائق الحية قبل الذاكرة / Live docs over memory (documented)
- `CODE-03` إثبات حزمة في بيئة معزولة / Prove a package in an isolated venv (proven)

### `CODE-02` — الوثائق الحية قبل الذاكرة / Live docs over memory

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** لأي سؤال عن مكتبة أو API اعتمد على الوثائق الحالية لا على ما تتذكره، واذكر النسخة. — For any library or API question, read the current docs instead of recalling them, and cite the version.

**متى:** library usage, API parameters, CLI flags, version-sensitive behaviour

**كيف:** With the Context7 MCP (🔑 if connected): resolve-library-id with the full question → pick by exact name, reputation and the user's version → query-docs; at most 3 calls per question. Without it: WebFetch the official docs (many sites serve /llms.txt), `pip show X`, `npm view X version`, `<tool> --help`, read the installed source. Cite the version you read. Redact secrets from queries. If still unsure, say so.

**المعاملات:** ≤3 doc calls per question

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** documentation · api docs · context7 · llms.txt · version · توثيق · نسخة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-01` ابحث قبل أن تبني / Search-first: adopt, extend, compose, build (documented)
- `CODE-03` إثبات حزمة في بيئة معزولة / Prove a package in an isolated venv (proven)
- `CODE-04` دليل التعرّف على مستودع / Codebase onboarding guide (documented)

### `CODE-03` — إثبات حزمة في بيئة معزولة / Prove a package in an isolated venv

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لا تَعِد بمكتبة قبل أن تثبّتها في بيئة افتراضية وتشغّل أصغر مثال لها وترى ناتجه. — Never promise a library before installing it in a venv and running its smallest example.

**متى:** a power or plan depends on a package that is not yet present

**كيف:** 1) `python3 -m venv $SCRATCH/venvs/<name>` (or `uv venv`); 2) `$V/bin/pip install -q "<pkg>==<exact version>"` — pin it; 3) run the smallest real command with a scrubbed environment (`env -i PATH=$V/bin:/usr/bin:/bin HOME=$V/home`) so it cannot read keys or call paid backends; 4) record the command, exit code, timing and output path; 5) only then call it present/verified. Example in this skill: graphifyy 0.9.91 + [mcp] installed in 15.8 s and mapped 13 files in 1.49 s.

**المعاملات:** pin exact versions; scrubbed env

**التثبيت:** python3 -m venv V && V/bin/pip install "<pkg>==<ver>"

**الوسوم:** venv · pip install · proof · sandbox · بيئة افتراضية · تثبيت · إثبات

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-graphify/README.md`

#### 7. قدرات قريبة في العائلة

- `CODE-01` ابحث قبل أن تبني / Search-first: adopt, extend, compose, build (documented)
- `CODE-02` الوثائق الحية قبل الذاكرة / Live docs over memory (documented)
- `CODE-04` دليل التعرّف على مستودع / Codebase onboarding guide (documented)
- `CODE-05` قائمة أثر التغيير / Change-impact checklist (documented)

### `CODE-04` — دليل التعرّف على مستودع / Codebase onboarding guide

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** حوّل مستودعًا مجهولًا إلى خريطة: طبقات، ونقاط دخول، واختبارات، وأوامر بناء، ومسودة CLAUDE.md. — Turn an unfamiliar repo into a map: layers, entry points, tests, build commands and a starter CLAUDE.md.

**متى:** first contact with a repo; before planning a change in unknown code

**كيف:** Read in this order: README / CLAUDE.md / AGENTS.md → manifests (package.json, pyproject, go.mod) and lockfiles → entry points (main, CLI, routes) → test layout and how to run it → CI config → `git log --oneline -20` and `git log --stat -5` for what changes often. Then map the code (GRAPH-16: build a graph, read god nodes and communities). Output: a one-page onboarding note (purpose, layers, entry points, commands, conventions, risky areas) and, with consent, a starter CLAUDE.md.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** onboarding · repo map · architecture · تعرف على المستودع · خريطة الكود

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `git` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-02` الوثائق الحية قبل الذاكرة / Live docs over memory (documented)
- `CODE-03` إثبات حزمة في بيئة معزولة / Prove a package in an isolated venv (proven)
- `CODE-05` قائمة أثر التغيير / Change-impact checklist (documented)
- `CODE-06` حقائق قبل أول تعديل / Fact-forcing before the first edit (documented)

### `CODE-05` — قائمة أثر التغيير / Change-impact checklist

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** قبل أي تعديل اعرف ما سينكسر: الكود والبيانات والواجهات والاختبارات والتوثيق والإصدار، بدليل من الاستيرادات الحقيقية لا من أسماء المجلدات. — Before a change, list what can break across code, data, interfaces, tests, docs and release, with evidence from real imports, not folder names.

**متى:** edits to shared code, schemas, file formats, CLIs or public APIs

**كيف:** Answer in order: Code (entry points, callers, consumers, generated artifacts); Data (schemas, caches, serialization); Interfaces (APIs, file formats, CLIs and who uses them); Tests (which ones prove success); Docs; Release (order, compatibility window, rollback, irreversible effects). Evidence only from real imports, routes, `git grep -n`, graph `affected` (GRAPH-04) and tests; mark unknowns 'unverified'. After the change: did it solve the original issue, did the diff exceed scope, does the evidence cover the criteria (not just 'the command ran'), are docs synced, is temporary code gone.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** change impact · blast radius · dependencies · أثر التغيير · نطاق الضرر

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-03` إثبات حزمة في بيئة معزولة / Prove a package in an isolated venv (proven)
- `CODE-04` دليل التعرّف على مستودع / Codebase onboarding guide (documented)
- `CODE-06` حقائق قبل أول تعديل / Fact-forcing before the first edit (documented)
- `CODE-07` اتبع أسلوب المستودع القائم / Inherit the repo's style (documented)

### `CODE-06` — حقائق قبل أول تعديل / Fact-forcing before the first edit

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** قبل أن تعدّل ملفًا اكتب حقائق ملموسة: من يستورده، وأي دوال عامة تتأثر، وشكل البيانات، ونص طلب المستخدم حرفيًا. — Before editing a file, state concrete facts: who imports it, which public functions change, the data shape, and the user's request verbatim.

**متى:** the first Edit/Write of any file in a session; destructive shell commands

**كيف:** Edit: list importers (`git grep -n "from x import\\|require('x')"` or GRAPH-04), affected public functions, field names/structure/date format of any data file (use synthetic values), and quote the instruction. New file: who will call it, proof that no existing file already does the job, its schema. Destructive command (rm, forced checkout, find -exec): what exactly is removed and how to undo. 'Are you sure?' always answers yes; concrete facts force real investigation. Can be enforced by a PreToolUse hook (GateGuard).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** gateguard · investigate first · importers · edit safety · تحقق قبل التعديل · حقائق

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-04` دليل التعرّف على مستودع / Codebase onboarding guide (documented)
- `CODE-05` قائمة أثر التغيير / Change-impact checklist (documented)
- `CODE-07` اتبع أسلوب المستودع القائم / Inherit the repo's style (documented)
- `CODE-08` التطوير بالاختبار أولًا / Test-driven development (documented)

### `CODE-07` — اتبع أسلوب المستودع القائم / Inherit the repo's style

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** اكتب الكود الجديد بأسلوب المستودع الموجود: افحص أعرافه، واحسم التعارضات واحدًا واحدًا، وطابق نمط التكاملات القائمة. — Write new code in the repo's existing style: scan its conventions, resolve conflicts one at a time, mirror existing integrations.

**متى:** adding a module, endpoint or integration to an established codebase

**كيف:** Sample 3–5 sibling files: naming, error handling, logging, tests, file layout, imports, comments, language of messages (this repo: bilingual Arabic/English help texts). Where files disagree, pick one rule per conflict and say why. When adding an integration, copy the closest existing one's structure exactly (config keys, error type, test style). Optionally record the rules in a short style file.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** conventions · style · consistency · أسلوب · اتساق

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-05` قائمة أثر التغيير / Change-impact checklist (documented)
- `CODE-06` حقائق قبل أول تعديل / Fact-forcing before the first edit (documented)
- `CODE-08` التطوير بالاختبار أولًا / Test-driven development (documented)
- `CODE-09` حلقة التحقق بست مراحل / Six-phase verification loop (documented)

### `CODE-08` — التطوير بالاختبار أولًا / Test-driven development

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** اكتب اختبارًا يفشل أولًا، ثم أقل كود يجعله ينجح، ثم حسّن البنية والاختبارات خضراء. — Write a failing test first, then the least code to pass it, then refactor while green.

**متى:** new behaviour, bug fixes, refactors

**كيف:** RED: a test that states the behaviour and fails for the right reason. GREEN: the smallest change that passes. REFACTOR: improve structure with tests green. Bugs: reproduce as a failing regression test first, fix to green, keep the test. Changed requirements: update the tests to the new spec first, then the code. Coverage target ~80% where meaningful (ECC default) — coverage is evidence, not truth; never delete or weaken a test to go green.

**المعاملات:** coverage ≈80% target

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** tdd · unit tests · regression test · red green refactor · اختبار أولا · اختبارات

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-06` حقائق قبل أول تعديل / Fact-forcing before the first edit (documented)
- `CODE-07` اتبع أسلوب المستودع القائم / Inherit the repo's style (documented)
- `CODE-09` حلقة التحقق بست مراحل / Six-phase verification loop (documented)
- `CODE-10` نقاط تفتيش وخط أساس للانحدار / Checkpoints, regression baselines and pass^k (documented)

### `CODE-09` — حلقة التحقق بست مراحل / Six-phase verification loop

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** قبل القول «جاهز»: بناء، ثم أنواع، ثم فحص أسلوب، ثم اختبارات، ثم بحث عن أسرار، ثم مراجعة الفرق. — Before saying 'ready': build, types, lint, tests, secret scan, diff review.

**متى:** before a commit, PR, delivery, or after a major change (or every ~15 minutes of edits)

**كيف:** `set -o pipefail`. 1) build — stop if it fails; 2) types (`tsc --noEmit`, `pyright`/`mypy`); 3) lint (`ruff check`, `npm run lint`); pipe long output through `sed -n '1,30p'` rather than `head` so success is not killed by SIGPIPE; 4) tests with coverage; 5) secret and debug grep (`sk-`, `api_key`, `console.log`, `debugger`); 6) `git diff --stat` and read the diff. Report: Build / Types / Lint / Tests / Security / Diff, then READY or NOT READY with the issues. For video work the same loop is build → preview → ffprobe duration/fps/audio → sampled frames → diff.

**المعاملات:** 6 phases; rerun ≈ every 15 min of edits

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** verification loop · lint · typecheck · ready check · تحقق · جاهزية

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `git` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-07` اتبع أسلوب المستودع القائم / Inherit the repo's style (documented)
- `CODE-08` التطوير بالاختبار أولًا / Test-driven development (documented)
- `CODE-10` نقاط تفتيش وخط أساس للانحدار / Checkpoints, regression baselines and pass^k (documented)
- `CODE-11` حلقة التشخيص من الجذر / Root-cause debugging loop (documented)

### `CODE-10` — نقاط تفتيش وخط أساس للانحدار / Checkpoints, regression baselines and pass^k

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** ثبّت نقطة معروفة السلامة قبل التغيير، وقِس الانحدار مقابلها، واستخدم pass^k حين يهم الثبات. — Pin a known-good point before changing things, measure regressions against it, and use pass^k when consistency matters.

**متى:** risky multi-step changes; flaky or AI-written code; anything that must work every time

**كيف:** Checkpoint: verify clean state → commit or stash → log `date \| name \| sha` (e.g. .claude/checkpoints.log). Regression eval: baseline SHA, X/Y checks passed, compare after the change. Capability eval: checklist of new behaviours. Graders: code (test, grep, build = PASS/FAIL), model (1–5 rubric), human (risk LOW/MED/HIGH). pass@k = at least one of k runs succeeds (70% → 91% at k=3); pass^k = all k succeed (70% → 34% at k=3) — use pass^k for critical paths and regressions (target 100%). Keep a REGRESSION.md of each module's consumers and its acceptance command.

**المعاملات:** pass@3 >90% for capability; pass^3 = 100% for critical paths

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** checkpoint · regression · pass@k · eval · نقطة تفتيش · انحدار

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-08` التطوير بالاختبار أولًا / Test-driven development (documented)
- `CODE-09` حلقة التحقق بست مراحل / Six-phase verification loop (documented)
- `CODE-11` حلقة التشخيص من الجذر / Root-cause debugging loop (documented)
- `CODE-12` إصلاح البناء بأقل فرق / Minimal-diff build fixing (documented)

### `CODE-11` — حلقة التشخيص من الجذر / Root-cause debugging loop

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** أعد إنتاج الخطأ في أصغر حالة، وغيّر شيئًا واحدًا في كل تجربة، وأصلح السبب لا العَرَض، وأضف اختبارًا كان سيمسكه: الفرق في الكود ليس إصلاحًا. — Reproduce in the smallest case, change one thing per experiment, fix the cause not the symptom, add the test that would have caught it: a diff is not a fix.

**متى:** bugs, errors, flaky behaviour, wrong output

**كيف:** 1) Reproduce with the smallest reliable case; capture environment and the exact failure. 2) Diff working vs broken; one hypothesis per experiment. 3) Fix the root cause with the smallest reversible change. 4) Add a regression test that fails before and passes after. 5) Review correctness and edge cases before style. 6) Verify the requested postcondition (observe the behaviour). Never retry blindly after an uncertain, half-applied risky change: inspect the actual state first.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** debug · root cause · bug · reproduce · تشخيص · سبب جذري · خلل

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:hypothesis` ← python3 -c "import hypothesis" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-09` حلقة التحقق بست مراحل / Six-phase verification loop (documented)
- `CODE-10` نقاط تفتيش وخط أساس للانحدار / Checkpoints, regression baselines and pass^k (documented)
- `CODE-12` إصلاح البناء بأقل فرق / Minimal-diff build fixing (documented)
- `CODE-13` صيد الأعطال الصامتة / Silent-failure and click-path hunt (documented)

### `CODE-12` — إصلاح البناء بأقل فرق / Minimal-diff build fixing

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** أصلح أخطاء البناء والأنواع بأصغر تغيير ممكن وصنفًا صنفًا، وأصلح الكود لا إعدادات الفاحص. — Fix build and type errors with the smallest change, one error class at a time; fix the code, not the linter config.

**متى:** red CI, compile/type errors, dependency resolution failures

**كيف:** Detect the build system; run it; group errors by class; fix the first root error (later ones often cascade); rebuild after each group. Do not touch architecture, rename things or 'improve' unrelated code. Never weaken linter/formatter/tsconfig rules to get green (ECC blocks such edits with a config-protection hook). Record what each fix was for.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** build error · type error · ci · minimal diff · خطأ بناء · إصلاح

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-10` نقاط تفتيش وخط أساس للانحدار / Checkpoints, regression baselines and pass^k (documented)
- `CODE-11` حلقة التشخيص من الجذر / Root-cause debugging loop (documented)
- `CODE-13` صيد الأعطال الصامتة / Silent-failure and click-path hunt (documented)
- `CODE-14` حلقة تحسين أداء مقاسة / Measured optimization loop (documented)

### `CODE-13` — صيد الأعطال الصامتة / Silent-failure and click-path hunt

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** ابحث عن الأخطاء المبتلعة والبدائل الخاطئة، وتتبّع كل زر خطوة خطوة لترى إن كانت خطوة لاحقة تلغي سابقتها. — Hunt swallowed errors and bad fallbacks, and trace each action step by step to see if a later step undoes an earlier one.

**متى:** 'it does nothing', state resets unexpectedly, errors vanish, UI shows the wrong mode

**كيف:** Silent failures: grep for empty catch/except, `except Exception: pass`, defaults that hide errors, missing error propagation, ignored return codes. Click-path: for each interactive action, list its handler's calls in order and, for each call, the state it reads/writes/resets; build a map `action → {sets, resets}`; check whether a later call resets what an earlier one set, whether the final state matches the label, and async races. The same idea applies to animation timelines: a later tween can silently override an earlier property.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** silent failure · error handling · state bug · click path · عطل صامت · حالة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-11` حلقة التشخيص من الجذر / Root-cause debugging loop (documented)
- `CODE-12` إصلاح البناء بأقل فرق / Minimal-diff build fixing (documented)
- `CODE-14` حلقة تحسين أداء مقاسة / Measured optimization loop (documented)
- `CODE-15` معالجة أخطاء متينة / Resilient error handling (documented)

### `CODE-14` — حلقة تحسين أداء مقاسة / Measured optimization loop

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** لا تحسّن الأداء قبل تحديد العملية والمقياس وخط الأساس والميزانية، وجرّب فرضية واحدة في كل نسخة، وقل «أفضل نسخة آمنة مقاسة» لا «الأمثل». — Optimize only after fixing the operation, metric, baseline and budget; one hypothesis per variant; report 'best measured safe variant', never 'optimal'.

**متى:** slow renders, builds, queries, scripts

**كيف:** Prerequisites: operation, correctness gate, metric (wall time, p95, rows/s, cost/run, memory), baseline, budget (max variants, time, spend). Loop: measure baseline → find the bottleneck from evidence → variants that each test ONE hypothesis → same input shape → reject incorrect, unsafe or irreproducible ones → promote the fastest safe one → codify it in a script/config → rerun baseline vs winner. Keep a table: variant \| hypothesis \| command \| time \| correct? \| notes. Stop when within noise, correctness fails or budget is spent.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** performance · benchmark · optimization · profiling · أداء · تحسين · قياس

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-12` إصلاح البناء بأقل فرق / Minimal-diff build fixing (documented)
- `CODE-13` صيد الأعطال الصامتة / Silent-failure and click-path hunt (documented)
- `CODE-15` معالجة أخطاء متينة / Resilient error handling (documented)
- `CODE-16` قائمة مراجعة الكود / Code review checklist (documented)

### `CODE-15` — معالجة أخطاء متينة / Resilient error handling

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** صمّم الأخطاء: أنواع واضحة، وإعادة محاولة بتراجع وعشوائية للأخطاء العابرة فقط، وقاطع دائرة، وعمليات قابلة للتكرار بأمان. — Design errors on purpose: typed errors, retries with backoff and jitter only for transient faults, a circuit breaker, idempotent operations.

**متى:** network calls, external APIs, file processing, long pipelines

**كيف:** Typed error classes carrying cause and context; user-facing messages that leak nothing sensitive. Retry only transient errors (timeouts, 429, 5xx) with exponential backoff + jitter and a cap; never retry validation or auth errors. Circuit breaker after N consecutive failures. Make writes idempotent (keys, temp file + rename). Log once at the boundary. No blind retry of a half-applied operation: check state first.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** errors · retry · backoff · circuit breaker · idempotent · أخطاء · إعادة محاولة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-13` صيد الأعطال الصامتة / Silent-failure and click-path hunt (documented)
- `CODE-14` حلقة تحسين أداء مقاسة / Measured optimization loop (documented)
- `CODE-16` قائمة مراجعة الكود / Code review checklist (documented)
- `CODE-17` مراجعة طلب دمج بفريق وكلاء / PR review fan-out (key)

### `CODE-16` — قائمة مراجعة الكود / Code review checklist

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** راجع الصحة والحالات الحدّية قبل الأسلوب، ورتّب النتائج حسب الخطورة مع دليل لكل نتيجة. — Review correctness and edge cases before style; rank findings by severity with evidence for each.

**متى:** after writing or changing code; before merge; the user asks for a review

**كيف:** Order: logic and edge cases → error handling → security (inputs, authz, injection, secrets) → performance → tests (do they test behaviour?) → readability. Each finding: file:line, severity CRITICAL/HIGH/MEDIUM/LOW, evidence, suggested fix; group by file. Built-in skills in Claude Code: /code-review (effort low…max; --comment posts inline PR comments; --fix applies findings) and /simplify for reuse/simplification. Report what you did not review.

**المعاملات:** 4 severity levels

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** code review · review checklist · severity · مراجعة الكود · خطورة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-14` حلقة تحسين أداء مقاسة / Measured optimization loop (documented)
- `CODE-15` معالجة أخطاء متينة / Resilient error handling (documented)
- `CODE-17` مراجعة طلب دمج بفريق وكلاء / PR review fan-out (key)
- `CODE-18` إعادة هيكلة آمنة / Safe refactoring (documented)

### `CODE-17` — مراجعة طلب دمج بفريق وكلاء / PR review fan-out

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** وزّع مراجعة طلب الدمج على مراجعين متخصصين بالتوازي، ثم أزل التكرار وتحقق، ثم انشر تعليقات مرتبطة بالأسطر. — Fan a PR review out to specialist reviewers in parallel, dedupe and verify, then post line-level comments.

**متى:** a GitHub PR number or URL; the user asks for a thorough review

**كيف:** Fetch the diff (`gh pr diff <n>` or the GitHub MCP pull_request_read). In one message run: code-reviewer, comment-analyzer (comment rot), pr-test-analyzer (behavioural coverage), silent-failure-hunter, type-design-analyzer. Merge, dedupe, verify each serious finding (AGENT-14). Post with the GitHub MCP review flow: create a pending review → add_comment_to_pending_review per finding → submit. Needs the GitHub connector or `gh auth`.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pull request · github · review fan-out · طلب دمج · مراجعة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `gh` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `mcp:github` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-15` معالجة أخطاء متينة / Resilient error handling (documented)
- `CODE-16` قائمة مراجعة الكود / Code review checklist (documented)
- `CODE-18` إعادة هيكلة آمنة / Safe refactoring (documented)
- `CODE-19` سجل قرار معماري / Architecture decision record (documented)

### `CODE-18` — إعادة هيكلة آمنة / Safe refactoring

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** لا تعِد الهيكلة إلا والاختبارات خضراء، وغيّر البنية دون السلوك، وتحقق بعد كل خطوة حذف. — Refactor only with green tests, change structure not behaviour, and verify after each removal.

**متى:** cleanup, dead code, duplication, simplifying recently changed code

**كيف:** 1) Confirm tests are green (add characterization tests if coverage is thin). 2) Small behaviour-preserving steps, each followed by tests. 3) Dead code: find candidates with tools (knip, ts-prune, vulture, `graphify affected` showing no dependents), remove one group at a time, rebuild and test after each. 4) Focus on recently modified code unless asked for more. 5) Commit per step so rollback is trivial.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** refactor · dead code · cleanup · simplify · إعادة هيكلة · تنظيف

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:graphify` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-16` قائمة مراجعة الكود / Code review checklist (documented)
- `CODE-17` مراجعة طلب دمج بفريق وكلاء / PR review fan-out (key)
- `CODE-19` سجل قرار معماري / Architecture decision record (documented)
- `CODE-20` الحتمي أولًا والنموذج للذيل / Deterministic first, model for the tail (documented)

### `CODE-19` — سجل قرار معماري / Architecture decision record

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** وثّق كل قرار معماري: السياق والدوافع والخيارات والمفاضلات وأنماط الفشل والقرار والعواقب ومتى يُراجع. — Record each architecture decision: context, drivers, options, trade-offs, failure modes, decision, consequences, review trigger.

**متى:** choosing a framework, storage, protocol, structure; reversing an earlier decision

**كيف:** File docs/adr/NNNN-<slug>.md (numbered, never edited after acceptance; supersede instead). Fields: context; decision drivers; options considered; trade-offs; failure modes; decision; consequences; kill/review criteria. Claims about the architecture must come from the code and live constraints, not imagined topology. Keep a CONTEXT.md glossary for domain terms separate from ADRs.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** adr · architecture · decision record · قرار معماري · توثيق

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-17` مراجعة طلب دمج بفريق وكلاء / PR review fan-out (key)
- `CODE-18` إعادة هيكلة آمنة / Safe refactoring (documented)
- `CODE-20` الحتمي أولًا والنموذج للذيل / Deterministic first, model for the tail (documented)
- `CODE-21` ذاكرة مؤقتة ببصمة المحتوى / Content-hash cache (documented)

### `CODE-20` — الحتمي أولًا والنموذج للذيل / Deterministic first, model for the tail

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** حين يتبع معظم المدخلات نمطًا: عالجها بالتعابير النمطية أو محلل حتمي، وأرسل الحالات منخفضة الثقة فقط إلى النموذج. — When most inputs follow a pattern, parse them deterministically and send only low-confidence leftovers to a model.

**متى:** structured text extraction, log parsing, subtitle/timing files, catalog cleanup

**كيف:** Pipeline: regex/parser → cleaner → confidence score per item. Confidence ≥0.95 → output directly; below → a model validates or fixes that item only. Typical regex coverage 95–98% of items. Exact numbers (sums, timings, allocations) are computed by code and then frozen; prose arithmetic is never final.

**المعاملات:** use when >90% of inputs follow a pattern; confidence cut 0.95

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** regex · parser · deterministic · cost · llm fallback · حتمي · تحليل نصوص

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-18` إعادة هيكلة آمنة / Safe refactoring (documented)
- `CODE-19` سجل قرار معماري / Architecture decision record (documented)
- `CODE-21` ذاكرة مؤقتة ببصمة المحتوى / Content-hash cache (documented)
- `CODE-22` نظافة الإيداع وكلمات الحالة / Commit hygiene & status words (documented)

### `CODE-21` — ذاكرة مؤقتة ببصمة المحتوى / Content-hash cache

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** اجعل مفتاح الذاكرة المؤقتة بصمة SHA-256 للمحتوى ونسخة الإعدادات، فتُعاد المعالجة تلقائيًا عند التغيير فقط. — Key caches by a SHA-256 of the content plus the config/prompt version, so work reruns only when something changed.

**متى:** expensive per-file processing: renders, transcriptions, extractions, thumbnails

**كيف:** key = sha256(file bytes + tool version + prompt/config version); store results by key; write the manifest only after a successful run (a crash must not corrupt the next diff); refuse to overwrite a larger output with a much smaller one without --force (shrink guard). Example: skip re-rendering unchanged scenes; graphify uses this for its AST and semantic caches.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cache · sha256 · incremental · content hash · ذاكرة مؤقتة · بصمة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:graphify` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-19` سجل قرار معماري / Architecture decision record (documented)
- `CODE-20` الحتمي أولًا والنموذج للذيل / Deterministic first, model for the tail (documented)
- `CODE-22` نظافة الإيداع وكلمات الحالة / Commit hygiene & status words (documented)
- `CODE-23` Hypothesis: اختبارات قائمة على الخصائص تولّد مدخلات فاشلة / Hypothesis: Property-based tests that generate and shrink failing inputs (proven)

### `CODE-22` — نظافة الإيداع وكلمات الحالة / Commit hygiene & status words

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** أودِع تغييرات صغيرة برسائل تطابق تاريخ المستودع، وافحص الفرق المرحلي قبل الإيداع، واستخدم كلمات حالة دقيقة. — Commit small changes with messages matching the repo's history, review the staged diff first, and report with exact status words.

**متى:** before any commit or push; when reporting progress

**كيف:** Read `git log --oneline -15` to match the message style (Conventional Commits if the repo uses them). Review `git diff --staged`: no secrets, no debug prints, no stray files. Commit only when the user asked; never force-push or rewrite shared history without explicit approval; branch first if on the default branch. Report with: inspected · changed locally · verified locally · committed · pushed · blocked.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** git · commit · conventional commits · status · إيداع · حالة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `git` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-20` الحتمي أولًا والنموذج للذيل / Deterministic first, model for the tail (documented)
- `CODE-21` ذاكرة مؤقتة ببصمة المحتوى / Content-hash cache (documented)
- `CODE-23` Hypothesis: اختبارات قائمة على الخصائص تولّد مدخلات فاشلة / Hypothesis: Property-based tests that generate and shrink failing inputs (proven)
- `CODE-24` Pandera: تعريف عقود بيانات لإطارات pandas وPolars وفرضها / Pandera: Declare and enforce schemas on pandas/Polars dataframes (data contracts) (proven)

### `CODE-23` — Hypothesis: اختبارات قائمة على الخصائص تولّد مدخلات فاشلة / Hypothesis: Property-based tests that generate and shrink failing inputs

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | MPL-2.0 |

**ما هي:** اختبارات قائمة على الخصائص تولّد مدخلات فاشلة وتختزلها. — Property-based tests that generate and shrink failing inputs. (Hypothesis, ★9.1k, MPL-2.0).

**متى:** testing tasks the user has the right to run

**كيف:** `pip install hypothesis`. Verified here 2026-10-18: falsified 'short or small' list property and shrank the input (hypothesis 6.170.1). Licence note: weak copyleft.

**التثبيت:** pip install hypothesis

**الوسوم:** Testing · Hypothesis · toolbelt · توسعة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:hypothesis` ← python3 -c "import hypothesis" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/toolbelt-smoke/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/toolbelt-smoke/smoke.py`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/toolbelt-smoke/results.json`

#### 7. قدرات قريبة في العائلة

- `CODE-21` ذاكرة مؤقتة ببصمة المحتوى / Content-hash cache (documented)
- `CODE-22` نظافة الإيداع وكلمات الحالة / Commit hygiene & status words (documented)
- `CODE-24` Pandera: تعريف عقود بيانات لإطارات pandas وPolars وفرضها / Pandera: Declare and enforce schemas on pandas/Polars dataframes (data contracts) (proven)
- `CODE-25` خريطة مستودع مرتبة بالأهمية / Ranked repository map (ready)

### `CODE-24` — Pandera: تعريف عقود بيانات لإطارات pandas وPolars وفرضها / Pandera: Declare and enforce schemas on pandas/Polars dataframes (data contracts)

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | MIT |

**ما هي:** تعريف عقود بيانات لإطارات pandas وPolars وفرضها. — Declare and enforce schemas on pandas/Polars dataframes (data contracts). (Pandera, ★4.5k, MIT).

**متى:** data contracts tasks the user has the right to run

**كيف:** `pip install pandera`. Verified here 2026-10-18: fps column contract: 29 rejected, 30/60 accepted (pandera 0.34.1). Licence note: permissive.

**التثبيت:** pip install pandera

**الوسوم:** Data contracts · Pandera · toolbelt · توسعة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pandas` ← python3 -c "import pandas" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:polars` ← python3 -c "import polars" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:pandera` ← python3 -c "import pandera" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/toolbelt-smoke/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/toolbelt-smoke/smoke.py`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/toolbelt-smoke/results.json`

#### 7. قدرات قريبة في العائلة

- `CODE-22` نظافة الإيداع وكلمات الحالة / Commit hygiene & status words (documented)
- `CODE-23` Hypothesis: اختبارات قائمة على الخصائص تولّد مدخلات فاشلة / Hypothesis: Property-based tests that generate and shrink failing inputs (proven)
- `CODE-25` خريطة مستودع مرتبة بالأهمية / Ranked repository map (ready)
- `CODE-26` تعديلات بكتل بحث واستبدال / Search/replace edit blocks (documented)

### `CODE-25` — خريطة مستودع مرتبة بالأهمية / Ranked repository map

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `repo` |
| الرخصة | Apache-2.0 |

**ما هي:** أهم الملفات والتعريفات في مستودع ضمن ميزانية صغيرة، مرتبة بمن يشير إليها أكثر. — The most important files and definitions of a repository within a small budget, ranked by how much the rest of the code refers to them.

**متى:** قبل تعديل مستودع غريب أو تكليف وكيل بكود / before editing an unfamiliar repo or briefing a coding agent

**كيف:** `python3 scripts/repo_map.py map <dir> --budget 6000 [--focus <file-or-word> …] [--json]` parses Python with ast and JS/TS, Go and Rust by line patterns, builds a reference graph (who mentions whose definitions, damped for generic names), ranks files with PageRank (pulled toward --focus), and prints each top file with its definition lines. `python3 scripts/repo_map.py defs <dir> <name>` shows where a name is defined and who mentions it. Read-only: it never imports or runs the target, so it is safe on untrusted checkouts. Paste the map into a code brief (PROMPT-37, kind code).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** repo map · aider · pagerank · code navigation · symbols · خريطة المستودع · فهم الكود · تعريفات

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/repo_map.py`
- `kosif-tool/.claude/skills/kosif-superpowers/evals/test_repo_map.py`

#### 7. قدرات قريبة في العائلة

- `CODE-23` Hypothesis: اختبارات قائمة على الخصائص تولّد مدخلات فاشلة / Hypothesis: Property-based tests that generate and shrink failing inputs (proven)
- `CODE-24` Pandera: تعريف عقود بيانات لإطارات pandas وPolars وفرضها / Pandera: Declare and enforce schemas on pandas/Polars dataframes (data contracts) (proven)
- `CODE-26` تعديلات بكتل بحث واستبدال / Search/replace edit blocks (documented)

### `CODE-26` — تعديلات بكتل بحث واستبدال / Search/replace edit blocks

| الحقل | القيمة |
|---|---|
| العائلة | `code-engineering` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/code-engineering.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | Apache-2.0 |

**ما هي:** عبّر عن كل تعديل كنص أصلي حرفي ونص بديل، واشترط أن يطابق الأصلي موضعًا واحدًا، وافشل بصوت عالٍ إن لم يوجد، ثم شغّل الفحص بعد كل تعديل. — Express each edit as an exact original block and its replacement, require the original to match exactly once, fail loudly when it does not, and run checks after every edit.

**متى:** تعديل كود بنموذج أو وكيل / editing code through a model or agent

**كيف:** Block: file path, SEARCH (copied verbatim, enough lines to be unique), REPLACE. Reject when SEARCH matches 0 or >1 times and show the nearest lines instead of guessing. Never rewrite a whole file for a small change. After applying: lint/tests; on failure feed the exact error back once (PROMPT-33). Commit each logical change with a message that says why.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** aider · edit format · search replace · diff · code editing · تعديل الكود · بحث واستبدال

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:CODE-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `repo-map`.
- مراحل النوع: قراءة الكود والاختبارات ← إعادة إنتاج أو اختبار جديد ← أصغر تغيير ← الاختبارات ← مراجعة الفرق ← فرع وPR.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: الاختبارات الموجودة تمر قبل التعديل وبعده ← أمر الاختبار
- إلزامي: اختبار لكل سلوك جديد أو خطأ مُصلح ← الاختبار الجديد يفشل قبل الإصلاح
- إلزامي: لا أسرار ولا مسارات جلسة في الشيفرة ← بحث أنماط الأسرار
- جودة: يطابق أسلوب الكود المحيط وتسمياته ← مراجعة الفرق
- جودة: طريقة تشغيل مكتوبة ومجرَّبة ← تشغيل الأمر المكتوب
- جودة: الفرق أصغر ما يحقق الطلب بلا إعادة كتابة غير مطلوبة ← git diff --stat
- جودة: المدخل الخاطئ يعطي خطأ واضحًا لا انهيارًا صامتًا ← تشغيل بمدخل خاطئ
- أمر الحكم في الوضع 1: `think.py qa code --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `CODE-24` Pandera: تعريف عقود بيانات لإطارات pandas وPolars وفرضها / Pandera: Declare and enforce schemas on pandas/Polars dataframes (data contracts) (proven)
- `CODE-25` خريطة مستودع مرتبة بالأهمية / Ranked repository map (ready)

