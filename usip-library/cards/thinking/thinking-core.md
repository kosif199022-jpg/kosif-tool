# `thinking-core` — التفكير والتخطيط والاستراتيجية (46 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/thinking-core.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/thinking.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`THINK-01` حلقة التفكير السباعية](#think-01--حلقة-التفكير-السباعية--thinking-loop-frame--recall--explore--decide--build--verify--report)
- [`THINK-02` تأطير الطلب ومعيار الإنجاز](#think-02--تأطير-الطلب-ومعيار-الإنجاز--frame-the-request-contract--done-criteria)
- [`THINK-03` جرد القدرات قبل الحل](#think-03--جرد-القدرات-قبل-الحل--60-second-capability-inventory-recall-powers-before-solving)
- [`THINK-04` استدعاء القوى من الفهرس](#think-04--استدعاء-القوى-من-الفهرس--recall-powers-from-the-catalog-powerspy-suggest--search--show)
- [`THINK-05` الاستكشاف من الواسع إلى الضيق](#think-05--الاستكشاف-من-الواسع-إلى-الضيق--explore-broad-then-narrow-in-parallel)
- [`THINK-06` القرار بمصفوفة تقييم وتشريح مسبق](#think-06--القرار-بمصفوفة-تقييم-وتشريح-مسبق--decide-small-rubric--pre-mortem--first-slice)
- [`THINK-07` البناء بشريحة رفيعة وتجارب صغيرة](#think-07--البناء-بشريحة-رفيعة-وتجارب-صغيرة--build-a-thin-end-to-end-slice-probe-dont-guess)
- [`THINK-08` وقفة فحص بعد كل نتيجة أداة](#think-08--وقفة-فحص-بعد-كل-نتيجة-أداة--pause-and-check-after-every-tool-result)
- [`THINK-09` التقرير: النتيجة أولًا وبلغة المستخدم](#think-09--التقرير-النتيجة-أولًا-وبلغة-المستخدم--report-outcome-first-evidence-badges-users-language)
- [`THINK-10` قائمة المرحلة صفر (12 وحدة)](#think-10--قائمة-المرحلة-صفر-12-وحدة--stage-0-checklist-12-modules)
- [`THINK-11` العدسات ونقاط الانقلاب](#think-11--العدسات-ونقاط-الانقلاب--lenses-and-pivots-multi-perspective--decision-sensitivity)
- [`THINK-12` حالة الحقائق وسجل الادعاءات](#think-12--حالة-الحقائق-وسجل-الادعاءات--fact-status-tags--claim-ledger)
- [`THINK-13` عدم اليقين المعايَر](#think-13--عدم-اليقين-المعايَر--calibrated-uncertainty-ranges-and-scenarios)
- [`THINK-14` قوالب التفكيك حسب المجال](#think-14--قوالب-التفكيك-حسب-المجال--decomposition-templates-product-system-causal-quantitative-adr)
- [`THINK-15` العمق بقدر المخاطر](#think-15--العمق-بقدر-المخاطر--scale-effort-to-stakes-effort-table)
- [`THINK-16` دفعة الإبداع بعد الخطة الآمنة](#think-16--دفعة-الإبداع-بعد-الخطة-الآمنة--creative-push-one-bolder-move-after-the-safe-plan)
- [`THINK-17` قفل الأرقام: احسب بالكود ثم جمّد](#think-17--قفل-الأرقام-احسب-بالكود-ثم-جمّد--numeric-lock-compute-in-code-freeze-then-narrate)
- [`THINK-18` سجل التغطية قبل الإرسال](#think-18--سجل-التغطية-قبل-الإرسال--coverage-ledger-every-explicit-ask-pass-or-declared-fail)
- [`THINK-19` اعرف قبل أن تقول «لا»](#think-19--اعرف-قبل-أن-تقول-لا--know-before-you-say-no-map--probe--install--alternative)
- [`THINK-20` سُلَّم حقيقة القدرة](#think-20--سُلَّم-حقيقة-القدرة--capability-truth-ladder-exposure--authorization--execution--verification)
- [`THINK-21` سُلَّم اختيار السطح](#think-21--سُلَّم-اختيار-السطح--surface-selection-rule--skill--mcp--local-cli--api)
- [`THINK-22` ابحث قبل أن تبني](#think-22--ابحث-قبل-أن-تبني--search-first-adopt--extend--compose--build)
- [`THINK-23` تحميل محدود للفصول](#think-23--تحميل-محدود-للفصول--bounded-loading-2-chapters-4-deep--gap-test)
- [`THINK-24` التوثيق الحي قبل الذاكرة](#think-24--التوثيق-الحي-قبل-الذاكرة--live-docs-over-memory-for-libraries-and-apis)
- [`THINK-25` اسأل أم افترض؟](#think-25--اسأل-أم-افترض--ask-or-assume-proceed-on-cheap-guesses-ask-only-at-costly-forks)
- [`THINK-26` معايير قبول قابلة للملاحظة](#think-26--معايير-قبول-قابلة-للملاحظة--observable-acceptance-criteria-37-acs)
- [`THINK-27` تفويض الوكلاء الفرعيين والتوازي](#think-27--تفويض-الوكلاء-الفرعيين-والتوازي--subagent-brief-parallel-fan-out-and-completion-contract)
- [`THINK-28` مجلس الأصوات الأربعة](#think-28--مجلس-الأصوات-الأربعة--council-of-four-voices-anti-anchoring-decision)
- [`THINK-29` ثلاثة خيارات وخيار «لا شيء»](#think-29--ثلاثة-خيارات-وخيار-لا-شيء--three-real-options--do-nothing--kill-criteria)
- [`THINK-30` حقائق قبل أول تعديل](#think-30--حقائق-قبل-أول-تعديل--fact-forcing--change-impact-before-editing)
- [`THINK-31` الاسترجاع المتكرر](#think-31--الاسترجاع-المتكرر--iterative-retrieval-dispatch--evaluate--refine-3-cycles)
- [`THINK-32` بروتوكول فكّ التعثّر](#think-32--بروتوكول-فكّ-التعثّر--unstick-protocol-introspect-when-looping-or-failing)
- [`THINK-33` اقتصاد السياق](#think-33--اقتصاد-السياق--context-economy-just-in-time-loading-compaction-at-phase-boundaries)
- [`THINK-34` مسح الأنماط المضادة](#think-34--مسح-الأنماط-المضادة--anti-pattern-sweep-before-sending)
- [`THINK-35` سلّم مستويات التفكير L0–L6](#think-35--سلّم-مستويات-التفكير-l0l6--cognition-ladder-l0l6)
- [`THINK-36` العقد التلقائي للمهمة](#think-36--العقد-التلقائي-للمهمة--auto-framed-task-contract)
- [`THINK-37` مصفوفة قرار بفحص الحساسية](#think-37--مصفوفة-قرار-بفحص-الحساسية--decision-matrix-with-sensitivity)
- [`THINK-38` تقدير فيرمي بمونت كارلو](#think-38--تقدير-فيرمي-بمونت-كارلو--monte-carlo-fermi-estimate)
- [`THINK-39` ناقد المسودة الآلي](#think-39--ناقد-المسودة-الآلي--automatic-draft-critic)
- [`THINK-40` اختيار النماذج الذهنية للمشكلة](#think-40--اختيار-النماذج-الذهنية-للمشكلة--mental-model-selection-for-a-problem)
- [`THINK-41` اكتشاف المشكلة الحقيقية](#think-41--اكتشاف-المشكلة-الحقيقية--problem-finding-three-statements)
- [`THINK-42` إعادة التأطير مرتين](#think-42--إعادة-التأطير-مرتين--reframe-twice-before-solving)
- [`THINK-43` محاكاة الخبير](#think-43--محاكاة-الخبير--expert-simulation)
- [`THINK-44` نموذج القارئ البشري](#think-44--نموذج-القارئ-البشري--reader-model-theory-of-mind)
- [`THINK-45` المراقبة الذاتية عند الحدود](#think-45--المراقبة-الذاتية-عند-الحدود--metacognition-checkpoint)
- [`THINK-46` عادات العبقرية العشر](#think-46--عادات-العبقرية-العشر--ten-genius-habits-as-procedures)

## البطاقات / cards

### `THINK-01` — حلقة التفكير السباعية / Thinking Loop: frame → recall → explore → decide → build → verify → report

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حلقة عمل من سبع خطوات لكل طلب غير تافه، يتناسب عمقها مع حجم المهمة. — A seven-step working loop for every non-trivial request, scaled to the size of the task.

**متى:** Every new request, and again whenever the request changes. A trivial ask gets a one-pass version that still verifies.

**كيف:** 1 FRAME: goal sentence + done-criteria (THINK-02). 2 RECALL powers: inventory + catalog search (THINK-03, THINK-04). 3 EXPLORE: read ground truth, broad then narrow, ≥3 options (THINK-05). 4 DECIDE: small rubric + pre-mortem, pick the first thin slice (THINK-06). 5 BUILD: thin end-to-end slice, probe instead of guessing, pause after each tool result (THINK-07, THINK-08). 6 VERIFY: tools first, then eyes, then a rubric (CHECK-01). 7 REPORT: outcome first, evidence badges, user's language (THINK-09). Size it: trivial = one pass; medium = full loop once; large = loop + plan file on disk + subagents; research = broad-then-narrow fan-out.

**المعاملات:** trivial ≤5 tool calls · medium 5–20 · comparison 2–4 subagents · broad 5–10+ subagents only when value justifies ≈15× tokens

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** thinking loop · workflow · plan · method · think better · reasoning · حلقة التفكير · تفكير · فكر · منهج · خطة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-02` تأطير الطلب ومعيار الإنجاز / Frame the request: contract + done-criteria (documented)
- `THINK-03` جرد القدرات قبل الحل / 60-second capability inventory (recall powers before solving) (documented)

### `THINK-02` — تأطير الطلب ومعيار الإنجاز / Frame the request: contract + done-criteria

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أعد صياغة الهدف في جملة واحدة بلغة المستخدم، وحدد المُسلَّم والجمهور ومتى يقول المستخدم «تمام، هذا هو». — Restate the goal in one sentence in the user's language and name the deliverable, the audience and the moment the user would say 'yes, that's it'.

**متى:** Start of every request; again when the user changes direction or adds files.

**كيف:** Write six lines: (1) goal, one sentence, in the user's language/dialect; (2) deliverable + format + where it goes (file path, artifact, doc, MP4); (3) audience; (4) done-criteria as observable checks; (5) hard constraints (format, length/duration, fps, language/RTL, budget, licence, deadline) and soft preferences; (6) size class trivial / medium / large / research. State assumptions instead of inventing requirements; ask only when a missing choice changes the outcome (THINK-25).

**المعاملات:** 6 lines · done-criteria must be checkable

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** frame · contract · requirements · done criteria · scope · تأطير · معيار الإنجاز · متطلبات · نطاق

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-01` حلقة التفكير السباعية / Thinking Loop: frame → recall → explore → decide → build → verify → report (documented)
- `THINK-03` جرد القدرات قبل الحل / 60-second capability inventory (recall powers before solving) (documented)
- `THINK-04` استدعاء القوى من الفهرس / Recall powers from the catalog (powers.py suggest / search / show) (proven)

### `THINK-03` — جرد القدرات قبل الحل / 60-second capability inventory (recall powers before solving)

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** قبل اختيار الطريقة اجرد أدواتك وبيئتك والمكتبات القابلة للتثبيت والمفاتيح والمهارات، ولا تفترض. — Before choosing an approach, inventory tools, environment, installable libraries, keys and skills; probe, never assume.

**متى:** Any non-trivial request; any moment you are about to say 'I can't' or reach for the familiar route out of habit.

**كيف:** 1 Tools: loaded tools, deferred tool names (load with ToolSearch 'select:<name>' or keywords), every mcp__<server>__ prefix, skills list, subagent/parallel ability. 2 Environment: `command -v python3 node ffmpeg gh`, `python3 -c 'import X'`; machine facts live in the environment snapshot (re-run scripts/probe_env.py). 3 Installable: which library turns this into a solved problem? (pip/uv/npm/apt into a venv or scratch dir). 4 Keys/services 🔑: name the exact key or connector; ask once, only if blocking. 5 Prior art: `python3 scripts/powers.py suggest "<brief>"` (THINK-04), repo templates. 6 Pick a tier per sub-problem ✅ > 🟢 > 📦 > 🔑 > 💡 and say which you rely on. 7 Write a 3–8 line 'powers I will use' note (internal, or shown on big tasks).

**المعاملات:** ≈60 s · 7 steps · 3–8 line note

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** capability inventory · recall powers · tools · probe · deferred tools · جرد القدرات · قدراتي · أدوات · فحص البيئة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-01` حلقة التفكير السباعية / Thinking Loop: frame → recall → explore → decide → build → verify → report (documented)
- `THINK-02` تأطير الطلب ومعيار الإنجاز / Frame the request: contract + done-criteria (documented)
- `THINK-04` استدعاء القوى من الفهرس / Recall powers from the catalog (powers.py suggest / search / show) (proven)
- `THINK-05` الاستكشاف من الواسع إلى الضيق / Explore broad-then-narrow, in parallel (documented)

### `THINK-04` — استدعاء القوى من الفهرس / Recall powers from the catalog (powers.py suggest / search / show)

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | owner |

**ما هي:** ابحث في فهرس القوى بوصف الطلب بالعربية أو الإنجليزية قبل أن تخترع حلًا من الصفر. — Search the power catalog with the brief, in Arabic or English, before inventing a solution from scratch.

**متى:** Right after framing; whenever a sub-problem appears ('how do I do X here?'); before saying a capability is missing.

**كيف:** `python3 scripts/powers.py suggest "<brief>"` → ranked powers + reference styles. `python3 scripts/powers.py search <words> --status proven ready` keeps only ✅/🟢. `show <ID>` prints how/params/proof. `family <name>` browses one family (new mind families too, e.g. `family thinking-core`). Open at most two chapters (THINK-23). Hits are recall hints, not routes: read the record's proof before claiming the power.

**المعاملات:** --limit 25 default · --status filter · results rank stronger evidence first

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** catalog · search · suggest · recall · powers.py · فهرس · بحث · استدعاء · قوى

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `session-2026-10-16:skill-audit.md#2`
- `kosif-tool/.claude/skills/kosif-superpowers/scripts/powers.py`

#### 7. قدرات قريبة في العائلة

- `THINK-02` تأطير الطلب ومعيار الإنجاز / Frame the request: contract + done-criteria (documented)
- `THINK-03` جرد القدرات قبل الحل / 60-second capability inventory (recall powers before solving) (documented)
- `THINK-05` الاستكشاف من الواسع إلى الضيق / Explore broad-then-narrow, in parallel (documented)
- `THINK-06` القرار بمصفوفة تقييم وتشريح مسبق / Decide: small rubric + pre-mortem + first slice (documented)

### `THINK-05` — الاستكشاف من الواسع إلى الضيق / Explore broad-then-narrow, in parallel

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اقرأ الحقيقة الأرضية قبل الكتابة: ابحث بعبارات قصيرة واسعة ثم ضيّق، وأطلق القراءات المستقلة معًا. — Read ground truth before writing: short broad queries first, then narrow; fire independent reads together.

**متى:** Medium or larger tasks, an unfamiliar codebase or domain, or any 'best / most creative' request.

**كيف:** Read the files, data, source media and docs first. Batch independent Read/Grep/Bash probes in one message. Generate at least three genuinely different approaches (IDEA-01). Fermi-check feasibility: time, tokens, file sizes, render time, cost (IDEA-05). With three or more independent threads, delegate with full briefs (THINK-27).

**المعاملات:** ≥3 options · one parallel batch per round · broad → narrow

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** explore · research · parallel · ground truth · استكشاف · بحث · قراءة · توازي

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-03` جرد القدرات قبل الحل / 60-second capability inventory (recall powers before solving) (documented)
- `THINK-04` استدعاء القوى من الفهرس / Recall powers from the catalog (powers.py suggest / search / show) (proven)
- `THINK-06` القرار بمصفوفة تقييم وتشريح مسبق / Decide: small rubric + pre-mortem + first slice (documented)
- `THINK-07` البناء بشريحة رفيعة وتجارب صغيرة / Build a thin end-to-end slice; probe, don't guess (documented)

### `THINK-06` — القرار بمصفوفة تقييم وتشريح مسبق / Decide: small rubric + pre-mortem + first slice

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قيّم الخيارات على خمسة معايير من 1 إلى 5، ثم تخيّل أن العمل فشل واكتب أسبابه الثلاثة وعالجها، ثم اختر أصغر شريحة كاملة. — Score options 1–5 on five criteria, imagine the work failed and mitigate its top three causes, then pick the smallest end-to-end slice.

**متى:** Whenever two or more options exist.

**كيف:** Rubric (1–5 each): fit to done-criteria · risk · effort · wow/novelty · reversibility. Pre-mortem: 'it is tomorrow and this failed — why?' → top three causes → mitigations go into the plan (IDEA-04). For large tasks write the plan to a file (it survives compaction). Choose the first thin slice that proves the riskiest assumption.

**المعاملات:** 5 criteria × 1–5 · top-3 failure causes

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** decide · rubric · premortem · tradeoff · قرار · مصفوفة · تشريح مسبق · مفاضلة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-04` استدعاء القوى من الفهرس / Recall powers from the catalog (powers.py suggest / search / show) (proven)
- `THINK-05` الاستكشاف من الواسع إلى الضيق / Explore broad-then-narrow, in parallel (documented)
- `THINK-07` البناء بشريحة رفيعة وتجارب صغيرة / Build a thin end-to-end slice; probe, don't guess (documented)
- `THINK-08` وقفة فحص بعد كل نتيجة أداة / Pause-and-check after every tool result (documented)

### `THINK-07` — البناء بشريحة رفيعة وتجارب صغيرة / Build a thin end-to-end slice; probe, don't guess

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أظهر نسخة تعمل من طرف إلى طرف مبكرًا، وعند الشك شغّل تجربة صغيرة بدل الاستنتاج. — Get a thin end-to-end version working early; when unsure, run a one-minute probe instead of reasoning about it.

**متى:** A plan is chosen.

**كيف:** One scene rendered, one endpoint answering, one chart drawn before any polish. Unsure whether a font shapes Arabic, a library exists or a flag is real? Run it (`--help`, an import, a one-frame render). Use code for maths, data and file ops; use renderers for visuals. Work on copies; the user's assets (for example their audio) stay untouched. Keep a progress note on long tasks.

**المعاملات:** probe ≈1 min · 1 working slice before polish · iterate 2–3× against a visual target

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** build · thin slice · prototype · probe · بناء · نموذج أولي · تجربة صغيرة · شريحة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-05` الاستكشاف من الواسع إلى الضيق / Explore broad-then-narrow, in parallel (documented)
- `THINK-06` القرار بمصفوفة تقييم وتشريح مسبق / Decide: small rubric + pre-mortem + first slice (documented)
- `THINK-08` وقفة فحص بعد كل نتيجة أداة / Pause-and-check after every tool result (documented)
- `THINK-09` التقرير: النتيجة أولًا وبلغة المستخدم / Report: outcome first, evidence badges, user's language (documented)

### `THINK-08` — وقفة فحص بعد كل نتيجة أداة / Pause-and-check after every tool result

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بين خطوات الأدوات توقف وراجع: القواعد المنطبقة، والمعلومات الناقصة، والامتثال، ومعقولية النتيجة. — Between tool steps, stop and check the applicable rules, missing information, compliance and the sanity of the result.

**متى:** Analysing tool output, policy-heavy work, long sequential decisions where errors compound. Not needed for a single call or simple parallel calls.

**كيف:** Before the next action: (1) list the rules and constraints that apply now; (2) is required information missing? (3) does the planned action comply? (4) did the last result do what I expected — if not, backtrack instead of pushing on. Extended or interleaved thinking does this job; a dedicated 'think' tool is no longer the point, the checklist is.

**المعاملات:** τ-bench airline pass^1 0.570 with checklist prompt vs 0.370 baseline (article text; its table shows 0.584 vs 0.332); k=5 consistency 0.100 → 0.340; SWE-bench ≈ +1.6%

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** think · checklist · tool results · interleaved thinking · وقفة · فحص · تفكير متخلل · قائمة تحقق

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-06` القرار بمصفوفة تقييم وتشريح مسبق / Decide: small rubric + pre-mortem + first slice (documented)
- `THINK-07` البناء بشريحة رفيعة وتجارب صغيرة / Build a thin end-to-end slice; probe, don't guess (documented)
- `THINK-09` التقرير: النتيجة أولًا وبلغة المستخدم / Report: outcome first, evidence badges, user's language (documented)
- `THINK-10` قائمة المرحلة صفر (12 وحدة) / Stage-0 checklist (12 modules) (documented)

### `THINK-09` — التقرير: النتيجة أولًا وبلغة المستخدم / Report: outcome first, evidence badges, user's language

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** ابدأ بالنتيجة والرابط، ثم ما تحققت منه بدليله، ثم ما لم يُنجز أو غير المؤكد، ثم الخيارات التالية، وبلهجة المستخدم. — Lead with the outcome and the link, then what was verified with evidence, then what is undone or uncertain, then next options, all in the user's language.

**متى:** End of every task and at milestones of long ones.

**كيف:** Mirror language and register (Egyptian Arabic in → Egyptian or plain Arabic out unless told otherwise). Four blocks: outcome + path/link · verified (with what command or look) · not done / unverified / risks · next options. Separate 'done and checked' from 'done, unchecked' from 'suggested'. Badge claims (✅ ran · 📄 documented · 💡 untested). Use honest stage words (CHECK-10). Keep it short; offer depth on request.

**المعاملات:** 4 blocks · no claim without evidence

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** report · summary · honesty · user language · تقرير · خلاصة · لغة المستخدم · صدق

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-07` البناء بشريحة رفيعة وتجارب صغيرة / Build a thin end-to-end slice; probe, don't guess (documented)
- `THINK-08` وقفة فحص بعد كل نتيجة أداة / Pause-and-check after every tool result (documented)
- `THINK-10` قائمة المرحلة صفر (12 وحدة) / Stage-0 checklist (12 modules) (documented)
- `THINK-11` العدسات ونقاط الانقلاب / Lenses and pivots (multi-perspective + decision sensitivity) (documented)

### `THINK-10` — قائمة المرحلة صفر (12 وحدة) / Stage-0 checklist (12 modules)

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** فحص ذهني سريع ومحلي قبل اختيار المسار، يتوسع فقط في الوحدات التي تنطبق. — A fast, local mental pass before choosing a route, expanding only the modules that apply.

**متى:** Every non-trivial request, before tools. Fast mode: one line per module; deep mode: alternatives + verification plan + acceptance criteria.

**كيف:** 1 Contract (THINK-02) · 2 Capability recall (THINK-03) · 3 Lenses: 2–4 viewpoints (THINK-11) · 4 Pivots: the assumption that flips the plan · 5 Pre-mortem (IDEA-04) · 6 Fact status: given / known / needs fresh check / inferred / unknown (THINK-12) · 7 Uncertainty as ranges (THINK-13) · 8 Acceptance tests first (THINK-26) · 9 Numbers go to code (THINK-17) · 10 Decompose by domain only when triggered (THINK-14) · 11 Depth by stakes (THINK-15) · 12 Creative push (THINK-16). Running the checklist is thinking, not evidence of having done anything.

**المعاملات:** 12 modules · fast / deep profiles

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** stage-0 · cognitive core · checklist · metacognition · المرحلة صفر · النواة المعرفية · قائمة فحص · تفكير

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-08` وقفة فحص بعد كل نتيجة أداة / Pause-and-check after every tool result (documented)
- `THINK-09` التقرير: النتيجة أولًا وبلغة المستخدم / Report: outcome first, evidence badges, user's language (documented)
- `THINK-11` العدسات ونقاط الانقلاب / Lenses and pivots (multi-perspective + decision sensitivity) (documented)
- `THINK-12` حالة الحقائق وسجل الادعاءات / Fact-status tags + claim ledger (documented)

### `THINK-11` — العدسات ونقاط الانقلاب / Lenses and pivots (multi-perspective + decision sensitivity)

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** اختر من 2 إلى 4 وجهات نظر قد تغيّر الإجابة، وحدد الافتراض الذي لو ثبت خطؤه لانقلبت الخطة. — Pick 2–4 viewpoints that could change the answer and name the assumption that flips the plan if it is wrong.

**متى:** Recommendations, design choices, anything with several stakeholders.

**كيف:** Lenses, for example: viewer, editor, engineer, lawyer, accountant, the user's own customer. For each ask 'what would they object to?'. Pivots: list the assumptions, mark the 1–3 whose failure changes the choice, compute any threshold in code (THINK-17) and state them in the report. Spend subagents on lenses only when the stakes justify the cost (THINK-28 for a full council).

**المعاملات:** 2–4 lenses · 1–3 pivots

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** lenses · perspectives · sensitivity · assumptions · عدسات · وجهات نظر · افتراضات · حساسية القرار

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-09` التقرير: النتيجة أولًا وبلغة المستخدم / Report: outcome first, evidence badges, user's language (documented)
- `THINK-10` قائمة المرحلة صفر (12 وحدة) / Stage-0 checklist (12 modules) (documented)
- `THINK-12` حالة الحقائق وسجل الادعاءات / Fact-status tags + claim ledger (documented)
- `THINK-13` عدم اليقين المعايَر / Calibrated uncertainty: ranges and scenarios (documented)

### `THINK-12` — حالة الحقائق وسجل الادعاءات / Fact-status tags + claim ledger

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** صنّف كل ادعاء: معطى أو معروف أو يحتاج فحصًا حديثًا أو استنتاج أو مجهول، واحتفظ بسجل فيه مصدر وتاريخ لكل ادعاء. — Tag each claim as given, known, needs a fresh check, inferred or unknown, and keep a ledger with a source and date per claim.

**متى:** Factual answers, research, comparisons, anything about versions, prices, laws, products or current events.

**كيف:** List the claims → status supported / contradicted / unverifiable + source + date. Hunt for evidence against each claim, not only for it. Write the answer from the ledger, marking fact vs inference vs unchecked; show conflicts instead of averaging them away. Changing facts need a fresh source: memory or confidence is not current evidence. Labels for the reader: sourced · user-supplied · inference · recommendation.

**المعاملات:** ledger columns: claim \| status \| source \| date

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** claim ledger · fact check · evidence · freshness · سجل الادعاءات · تحقق من الحقائق · مصادر · أدلة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-10` قائمة المرحلة صفر (12 وحدة) / Stage-0 checklist (12 modules) (documented)
- `THINK-11` العدسات ونقاط الانقلاب / Lenses and pivots (multi-perspective + decision sensitivity) (documented)
- `THINK-13` عدم اليقين المعايَر / Calibrated uncertainty: ranges and scenarios (documented)
- `THINK-14` قوالب التفكيك حسب المجال / Decomposition templates: product, system, causal, quantitative, ADR (documented)

### `THINK-13` — عدم اليقين المعايَر / Calibrated uncertainty: ranges and scenarios

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** عبّر عن المجهول بمدى وسيناريوهات لا بنبرة واثقة؛ فالثقة ليست برهانًا. — Express unknowns as ranges and scenarios, not a confident tone; confidence is not proof.

**متى:** Forecasts, estimates, timelines, costs, 'will this work?' questions.

**كيف:** Give low / base / high with the driver of each. Name what new fact would move the estimate. Mark 'measured' vs 'estimated' explicitly ('render ≈9 min, estimated, not measured'). Never turn self-confidence into a score: a 1–10 confidence is not evidence and never replaces a check.

**المعاملات:** 3-point range + named driver

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** uncertainty · forecast · estimate · calibration · عدم اليقين · تقدير · توقع · سيناريوهات

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-11` العدسات ونقاط الانقلاب / Lenses and pivots (multi-perspective + decision sensitivity) (documented)
- `THINK-12` حالة الحقائق وسجل الادعاءات / Fact-status tags + claim ledger (documented)
- `THINK-14` قوالب التفكيك حسب المجال / Decomposition templates: product, system, causal, quantitative, ADR (documented)
- `THINK-15` العمق بقدر المخاطر / Scale effort to stakes (effort table) (documented)

### `THINK-14` — قوالب التفكيك حسب المجال / Decomposition templates: product, system, causal, quantitative, ADR

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** قوالب جاهزة لتفكيك المشكلة حسب نوعها: منتج، نظام، سببية، أرقام، وقرار معماري. — Ready templates to break a problem down by kind: product, system, causal, numbers and architecture decisions.

**متى:** Only when the request is of that kind (do not apply all of them by default).

**كيف:** Product: goals → users → requirements → metrics → risks → rollout (+ kill criteria). System: entities → interfaces → dependencies → states → failure boundaries. Causal: inputs → mechanism → outputs → feedback loops; test alternative explanations; correlation ≠ causation. Quantitative: inputs, formulas, constraints, scenarios, units, reconciliation (numbers via THINK-17). ADR: context, drivers, options, trade-offs, failure modes, decision, consequences, review/kill criteria.

**المعاملات:** 5 templates

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** decomposition · prd · architecture · causal · adr · تفكيك · متطلبات المنتج · معمارية · سببية

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-12` حالة الحقائق وسجل الادعاءات / Fact-status tags + claim ledger (documented)
- `THINK-13` عدم اليقين المعايَر / Calibrated uncertainty: ranges and scenarios (documented)
- `THINK-15` العمق بقدر المخاطر / Scale effort to stakes (effort table) (documented)
- `THINK-16` دفعة الإبداع بعد الخطة الآمنة / Creative push: one bolder move after the safe plan (documented)

### `THINK-15` — العمق بقدر المخاطر / Scale effort to stakes (effort table)

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** اجعل عدد الخطوات والوكلاء متناسبًا مع قيمة المهمة ومخاطرها، لا مع حماسك. — Match the number of steps and agents to the task's value and risk, not to enthusiasm.

**متى:** While framing (size class) and whenever the scope grows.

**كيف:** Trivial: 0 subagents, ≤5 calls, still verify. Medium: 0–1 subagent, 5–20 calls. Comparison: 2–4 subagents × 10–15 calls each. Broad research or a big build: 5–10+ subagents, only when value justifies ≈15× the tokens of chat (single agents ≈4×). Invoking a skill does not force the heaviest mode. Ceremony grows with blast radius: security or public-API work is at least 'standard'.

**المعاملات:** multi-agent beat single-agent by 90.2% on Anthropic's internal research eval; token use explained ≈80% of BrowseComp variance (internal results — do not generalise)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** effort · scaling · subagents · budget · جهد · ميزانية · وكلاء فرعيون · حجم المهمة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-13` عدم اليقين المعايَر / Calibrated uncertainty: ranges and scenarios (documented)
- `THINK-14` قوالب التفكيك حسب المجال / Decomposition templates: product, system, causal, quantitative, ADR (documented)
- `THINK-16` دفعة الإبداع بعد الخطة الآمنة / Creative push: one bolder move after the safe plan (documented)
- `THINK-17` قفل الأرقام: احسب بالكود ثم جمّد / Numeric lock: compute in code, freeze, then narrate (documented)

### `THINK-16` — دفعة الإبداع بعد الخطة الآمنة / Creative push: one bolder move after the safe plan

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بعد أن تكتمل الخطة الآمنة اسأل مرة واحدة: ما الذي يجعل هذا مدهشًا أو أفضل بقدرة لم يطلبها المستخدم؟ — Once the safe plan exists, ask once: what would make this surprising or better using a capability the user did not think to ask for?

**متى:** Creative or design asks, 'make it great', and any deliverable a human will look at.

**كيف:** Pick one operator — capability cross-over (IDEA-17), exaggerate (IDEA-11) or analogy (IDEA-08) — and produce one bold variant. Offer it beside the safe plan as a safe + bold pair; never let it delay the thin slice or replace an explicit request.

**المعاملات:** 1 question · 1 bold variant

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** creative push · ambition · wow · bold option · دفعة إبداع · طموح · فكرة جريئة · إبهار

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-14` قوالب التفكيك حسب المجال / Decomposition templates: product, system, causal, quantitative, ADR (documented)
- `THINK-15` العمق بقدر المخاطر / Scale effort to stakes (effort table) (documented)
- `THINK-17` قفل الأرقام: احسب بالكود ثم جمّد / Numeric lock: compute in code, freeze, then narrate (documented)
- `THINK-18` سجل التغطية قبل الإرسال / Coverage ledger: every explicit ask PASS or declared FAIL (documented)

### `THINK-17` — قفل الأرقام: احسب بالكود ثم جمّد / Numeric lock: compute in code, freeze, then narrate

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** كل رقم دقيق يأتي من تشغيل كود، ثم يُجمَّد ويُقتبس ولا يُعاد حسابه نثرًا. — Every exact number comes from running code; it is then frozen and quoted, never recomputed in prose.

**متى:** Exact arithmetic, optimisation, allocation, scheduling, reconciliation, thresholds, unit conversion, money, tax, frame counts and durations.

**كيف:** Write the inputs explicitly → compute with python / duckdb / a spreadsheet engine → check constraints, ties and slack → print the result → freeze it. Later reasoning may interpret the number but never silently recompute it; if prose disagrees, the code wins until the code is shown wrong. Reconcile totals two independent ways and report differences instead of plugging them. Examples: VAT on 1000 → state the rate assumption, compute in code; frames = round(duration × fps) computed, not guessed.

**المعاملات:** 2 independent reconciliations · zero prose arithmetic in final answers

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** numeric lock · deterministic · arithmetic · reconcile · قفل الأرقام · حساب بالكود · مطابقة · أرقام دقيقة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:duckdb` ← python3 -c "import duckdb" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-15` العمق بقدر المخاطر / Scale effort to stakes (effort table) (documented)
- `THINK-16` دفعة الإبداع بعد الخطة الآمنة / Creative push: one bolder move after the safe plan (documented)
- `THINK-18` سجل التغطية قبل الإرسال / Coverage ledger: every explicit ask PASS or declared FAIL (documented)
- `THINK-19` اعرف قبل أن تقول «لا» / Know before you say no: map → probe → install → alternative (documented)

### `THINK-18` — سجل التغطية قبل الإرسال / Coverage ledger: every explicit ask PASS or declared FAIL

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** قبل الإرسال اقرأ رسالة المستخدم من جديد، وضع على كل طلب صريح علامة «نجح» أو «فشل» من محتوى المُسلَّم الفعلي. — Before sending, re-read the user's message and mark every explicit ask PASS or FAIL from the actual deliverable.

**متى:** Before every final answer; especially multi-part asks, file deliverables and long tasks.

**كيف:** List each explicit ask: format, length, language, sections, files, counts, tone, deadline. Open the artefact and check it (count rows, open the file, ffprobe the video) — not memory. Fix each FAIL or declare it in the report. In multi-reviewer work: if zero reviewers returned valid output, report REVIEWERS_FAILED and answer from verified evidence only.

**المعاملات:** 1 row per ask · PASS/FAIL from the artefact

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** coverage · requirements · checklist · missed asks · سجل التغطية · تغطية الطلبات · مراجعة الطلب · نقص

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-16` دفعة الإبداع بعد الخطة الآمنة / Creative push: one bolder move after the safe plan (documented)
- `THINK-17` قفل الأرقام: احسب بالكود ثم جمّد / Numeric lock: compute in code, freeze, then narrate (documented)
- `THINK-19` اعرف قبل أن تقول «لا» / Know before you say no: map → probe → install → alternative (documented)
- `THINK-20` سُلَّم حقيقة القدرة / Capability-truth ladder: exposure ≠ authorization ≠ execution ≠ verification (documented)

### `THINK-19` — اعرف قبل أن تقول «لا» / Know before you say no: map → probe → install → alternative

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** قبل أن تقول «مستحيل» راجع خريطة القدرات وشغّل الفحص؛ فكثير مما تظنه ناقصًا على بُعد أمر تثبيت. — Before saying 'impossible', check the capability map and run the probe; much of what seems missing is one install away.

**متى:** Whenever you are about to decline, downgrade the deliverable, or answer 'I don't have that tool'.

**كيف:** 1 Look it up: `python3 scripts/powers.py search <words>` and the SELF family. 2 Probe: `command -v X`, `python3 -c 'import X'`, ToolSearch for deferred tools/connectors. 3 Absent but installable: install into a venv or scratch dir (`uv venv && uv pip install X`, `npm i X` in scratch, `apt-get install` where allowed), run its smallest example, then call it present. 4 Needs a key or paid service: name the exact key/connector and offer the best keyless alternative. 5 Only then say 'not possible here', with the reason and the next step.

**المعاملات:** 5 steps · installs go to an isolated env

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** capability · can't · install · probe · alternative · مستحيل · تثبيت · بديل · قدرة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-17` قفل الأرقام: احسب بالكود ثم جمّد / Numeric lock: compute in code, freeze, then narrate (documented)
- `THINK-18` سجل التغطية قبل الإرسال / Coverage ledger: every explicit ask PASS or declared FAIL (documented)
- `THINK-20` سُلَّم حقيقة القدرة / Capability-truth ladder: exposure ≠ authorization ≠ execution ≠ verification (documented)
- `THINK-21` سُلَّم اختيار السطح / Surface selection: rule → skill → MCP → local CLI → API (documented)

### `THINK-20` — سُلَّم حقيقة القدرة / Capability-truth ladder: exposure ≠ authorization ≠ execution ≠ verification

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** وجود الأداة ليس إذنًا، والإذن ليس تنفيذًا، والتنفيذ ليس تحققًا؛ أبلغ دائمًا عن أدنى حالة صحيحة. — Having a tool is not permission, permission is not action, action is not proof; always report the lowest true state.

**متى:** Every capability claim, every status line, every 'done'.

**كيف:** States: IDEA 💡 → DOCUMENTED 📄 → INSTALLABLE 📦 → NEEDS-KEY 🔑 → PRESENT (🟢 when code exists) → EXECUTED → VERIFIED ✅ → PROVEN-BEFORE (a dated lease; re-probe in a new container) · BLOCKED (reason + next step). Rules: a success message is transport evidence, not verification; a demo asset is not an engine; a plan is not a render; choosing a method is not executing it; a prompt cannot create a tool or a permission. Missing runtime → say 'plan only, not executed' and offer the install.

**المعاملات:** 8 states + BLOCKED

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** capability truth · honesty · badges · verification · حقيقة القدرة · شارات · تحقق · تنفيذ

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-18` سجل التغطية قبل الإرسال / Coverage ledger: every explicit ask PASS or declared FAIL (documented)
- `THINK-19` اعرف قبل أن تقول «لا» / Know before you say no: map → probe → install → alternative (documented)
- `THINK-21` سُلَّم اختيار السطح / Surface selection: rule → skill → MCP → local CLI → API (documented)
- `THINK-22` ابحث قبل أن تبني / Search first: Adopt / Extend / Compose / Build (documented)

### `THINK-21` — سُلَّم اختيار السطح / Surface selection: rule → skill → MCP → local CLI → API

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** اختر المكان الصحيح لكل قدرة: قاعدة دائمة، أو فصل مهارة، أو موصل، أو سكربت محلي، أو واجهة برمجية بإذن. — Put each capability on the right surface: always-on rule, skill chapter, connector, local script, or an approved API call.

**متى:** Designing a workflow, adding a capability to the skill, or choosing how to do a repeated task.

**كيف:** Always-true invariant → one line in CLAUDE.md / SKILL.md. Occasional procedure → a skill chapter loaded on demand. Repeated stateful integration → an MCP server/connector, only after confirming it is connected. Deterministic transformation → a local script/CLI verified here (ffmpeg, python). Narrow authenticated or paid operation → a direct API call with explicit approval, a budget and a key supplied through a proper channel. No new runtime surface for fashion; a CLI wrapped by a skill often costs fewer tokens than an MCP wrapper.

**المعاملات:** 5 rungs

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** surface · mcp · skill · cli · api · سطح · موصل · سكربت · اختيار الأداة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-19` اعرف قبل أن تقول «لا» / Know before you say no: map → probe → install → alternative (documented)
- `THINK-20` سُلَّم حقيقة القدرة / Capability-truth ladder: exposure ≠ authorization ≠ execution ≠ verification (documented)
- `THINK-22` ابحث قبل أن تبني / Search first: Adopt / Extend / Compose / Build (documented)
- `THINK-23` تحميل محدود للفصول / Bounded loading: ≤2 chapters (≤4 deep) + gap test (documented)

### `THINK-22` — ابحث قبل أن تبني / Search first: Adopt / Extend / Compose / Build

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** قبل كتابة أداة أو مهارة ابحث عمّا هو موجود في المستودع والمهارات والحزم وGitHub، ثم قرر: اعتمد، أو وسّع، أو ركّب، أو ابنِ. — Before writing a tool or skill, search the repo, skills, package indexes and GitHub, then adopt, extend, compose or build.

**متى:** Before hand-coding an effect, a parser, a converter, a skill or an integration.

**كيف:** Step 0: check which search channels work (rg, pip, npm, `gh auth status`, skills list, ToolSearch) and say which were skipped. Search order: this repo → installed skills / deferred tools → package indexes (`pip index versions X`, `npm view X version`) → GitHub (`gh search repos <kw> --sort stars --limit 10`) → web. Score function fit, maintenance, community, docs, licence, dependencies. Decide: exact, maintained, MIT/Apache match → Adopt; partial → Extend with a thin wrapper; several weak → Compose 2–3; none → Build, informed by the research. Read README and LICENSE of the top 1–3; never auto-run third-party installers or hooks.

**المعاملات:** shortlist 5–12 · read top 1–3 · 4 decisions

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** search first · reuse · libraries · adopt · ابحث أولًا · إعادة استخدام · مكتبات · لا تعد اختراع العجلة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-20` سُلَّم حقيقة القدرة / Capability-truth ladder: exposure ≠ authorization ≠ execution ≠ verification (documented)
- `THINK-21` سُلَّم اختيار السطح / Surface selection: rule → skill → MCP → local CLI → API (documented)
- `THINK-23` تحميل محدود للفصول / Bounded loading: ≤2 chapters (≤4 deep) + gap test (documented)
- `THINK-24` التوثيق الحي قبل الذاكرة / Live docs over memory for libraries and APIs (documented)

### `THINK-23` — تحميل محدود للفصول / Bounded loading: ≤2 chapters (≤4 deep) + gap test

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** افتح فصلين على الأكثر لطلب عادي وأربعة لإنتاج كبير، ولا تفتح فصلًا إضافيًا إلا بعد تسمية المتطلب الناقص. — Open at most two chapters for an ordinary request and four for a big production; open another only after naming the uncovered requirement.

**متى:** Whenever the catalog or references are large (they are: some chapters exceed 2,000 lines).

**كيف:** Gap test: before opening another chapter, write the specific requirement the open ones do not cover. On collision, prefer the chapter matching the requested artefact (a 9:16 reel → formats + captions, not 3D). A second chapter must add a distinct dimension, not paraphrase the first. Keywords are recall hints, not routes. Read by section (grep the heading, `sed -n` the range) instead of whole files.

**المعاملات:** 2 / 4 chapters · one extra at a time

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** progressive disclosure · context · chapters · gap test · تحميل محدود · فصول · سياق · اختبار الفجوة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-21` سُلَّم اختيار السطح / Surface selection: rule → skill → MCP → local CLI → API (documented)
- `THINK-22` ابحث قبل أن تبني / Search first: Adopt / Extend / Compose / Build (documented)
- `THINK-24` التوثيق الحي قبل الذاكرة / Live docs over memory for libraries and APIs (documented)
- `THINK-25` اسأل أم افترض؟ / Ask or assume: proceed on cheap guesses, ask only at costly forks (documented)

### `THINK-24` — التوثيق الحي قبل الذاكرة / Live docs over memory for libraries and APIs

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** لأي سؤال عن مكتبة أو واجهة برمجية فضّل التوثيق الحالي على ذاكرة التدريب، واذكر الإصدار. — For any library or API question, prefer current docs over training memory and cite the version.

**متى:** Writing code against a library, CLI flags, model or product lineups, prices, limits.

**كيف:** Docs connector (e.g. Context7) if present: resolve the library id, then query; ≤3 calls per question. Otherwise: WebFetch the official docs or their /llms.txt, `pip show X`, `npm view X version`, `X --help`, `python3 -c 'import X; help(X.f)'`. Cite the version used. Redact secrets from queries. If you could not check, say the answer comes from memory and may be stale.

**المعاملات:** ≤3 doc calls per question

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** docs · documentation · version · api · توثيق · إصدار · مكتبة · ذاكرة قديمة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-22` ابحث قبل أن تبني / Search first: Adopt / Extend / Compose / Build (documented)
- `THINK-23` تحميل محدود للفصول / Bounded loading: ≤2 chapters (≤4 deep) + gap test (documented)
- `THINK-25` اسأل أم افترض؟ / Ask or assume: proceed on cheap guesses, ask only at costly forks (documented)
- `THINK-26` معايير قبول قابلة للملاحظة / Observable acceptance criteria (3–7 ACs) (documented)

### `THINK-25` — اسأل أم افترض؟ / Ask or assume: proceed on cheap guesses, ask only at costly forks

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** إن كان الخطأ رخيص الإصلاح فاختر أعقل تفسير وصرّح بافتراضك وتابع؛ واسأل فقط عند مفترق مكلف أو لا رجعة فيه. — If a wrong guess is cheap to fix, pick the most reasonable reading, state it and proceed; ask only at a costly or irreversible fork.

**متى:** Any ambiguity in a request.

**كيف:** Look first: inspect the repo, docs and files before asking anything you could find. Proceed with a stated assumption when a wrong guess is cheap; show a draft instead of a questionnaire. Ask 1–3 questions, batched, once, only for: material security exposure, data loss, irreversible migration, API breakage, meaningful cost or credits, destructive or public actions. Always confirm deleting, publishing, pushing and paid generation.

**المعاملات:** ≤1–3 questions, batched · 6 blocking reasons

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ambiguity · clarifying questions · assumptions · over-asking · غموض · أسئلة توضيحية · افتراض · إفراط في السؤال

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-23` تحميل محدود للفصول / Bounded loading: ≤2 chapters (≤4 deep) + gap test (documented)
- `THINK-24` التوثيق الحي قبل الذاكرة / Live docs over memory for libraries and APIs (documented)
- `THINK-26` معايير قبول قابلة للملاحظة / Observable acceptance criteria (3–7 ACs) (documented)
- `THINK-27` تفويض الوكلاء الفرعيين والتوازي / Subagent brief, parallel fan-out and completion contract (documented)

### `THINK-26` — معايير قبول قابلة للملاحظة / Observable acceptance criteria (3–7 ACs)

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** حوّل الطلب الغامض إلى 3–7 معايير قبول يمكن رؤيتها أو قياسها قبل البناء. — Turn a vague ask into 3–7 acceptance criteria that can be observed or measured before building.

**متى:** Medium+ tasks, anything with a reviewer, any loop or automation.

**كيف:** Quick capture: goal, in/out of scope, assumptions, 3–7 ACs, blockers. Each AC: scenario · action · expected result · must-not · verification method · priority. Replace vague words ('fast', 'nice', 'clean') with numbers or observable states. The ACs become the checks in CHECK-01. If an AC turns impossible, mark it [revised] and re-present only the change. Tests are evidence, not truth.

**المعاملات:** 3–7 ACs · 6 fields each

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** acceptance criteria · requirements · definition of done · معايير القبول · متطلبات · تعريف الإنجاز

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-24` التوثيق الحي قبل الذاكرة / Live docs over memory for libraries and APIs (documented)
- `THINK-25` اسأل أم افترض؟ / Ask or assume: proceed on cheap guesses, ask only at costly forks (documented)
- `THINK-27` تفويض الوكلاء الفرعيين والتوازي / Subagent brief, parallel fan-out and completion contract (documented)
- `THINK-28` مجلس الأصوات الأربعة / Council of four voices (anti-anchoring decision) (documented)

### `THINK-27` — تفويض الوكلاء الفرعيين والتوازي / Subagent brief, parallel fan-out and completion contract

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** فوّض المسارات المستقلة بموجز كامل، وأطلقها معًا، واجمع نتائجها بنفسك، واعزل فشل أي منها. — Delegate independent lanes with a full brief, launch them together, collect the results yourself and isolate any failure.

**متى:** Three or more independent threads, wide research, multi-file builds, parallel renders.

**كيف:** Brief = objective + why it matters + exact output format/path + tools and sources allowed + boundaries (what not to do, what others cover) + budget + how success is judged. Launch independent lanes in one message (3–5 at once); batch independent tool calls. Lane matrix: lane \| parallel? \| write surface \| risk \| verification — one writer per file; never parallelise destructive commands or migrations. Completion contract: you own collection; never finish with 'waiting for agents'. Failure isolation: keep good peers, retry a failed lane once with a narrower brief, then report it failed. Ask subagents for 1–2k-token summaries.

**المعاملات:** 3–5 lanes at once · retry once · 1–2k-token returns

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** subagents · delegation · parallel · fan-out · orchestration · وكلاء فرعيون · تفويض · توازي · تنسيق

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-25` اسأل أم افترض؟ / Ask or assume: proceed on cheap guesses, ask only at costly forks (documented)
- `THINK-26` معايير قبول قابلة للملاحظة / Observable acceptance criteria (3–7 ACs) (documented)
- `THINK-28` مجلس الأصوات الأربعة / Council of four voices (anti-anchoring decision) (documented)
- `THINK-29` ثلاثة خيارات وخيار «لا شيء» / Three real options + do-nothing + kill criteria (documented)

### `THINK-28` — مجلس الأصوات الأربعة / Council of four voices (anti-anchoring decision)

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** لقرار غامض متعدد المسارات: اكتب رأيك أولًا، ثم استشر ثلاثة وكلاء جدد بلا تاريخ المحادثة، ثم اجمع مع إظهار الخلاف. — For an ambiguous multi-path decision: write your view first, consult three fresh agents without the conversation history, then synthesise showing dissent.

**متى:** Ambiguous decisions with little guidance (style direction, architecture, strategy). Not for facts or code review.

**كيف:** Reduce to one question (what is decided, constraints, success). Write your own position + 3 reasons + main risk before reading anyone else. Launch 3 fresh subagents in parallel with only the question and compact context: Skeptic (challenge the premise, simplify), Pragmatist (speed, user impact), Critic (failure modes). You hold the Architect voice (correctness, long-term). Synthesise: decision first, then the strongest dissent and what would change the decision.

**المعاملات:** 4 voices · 3 fresh subagents · own view written first

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** council · decision · debate · anchoring · مجلس · قرار · آراء · تحيز الإرساء

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-26` معايير قبول قابلة للملاحظة / Observable acceptance criteria (3–7 ACs) (documented)
- `THINK-27` تفويض الوكلاء الفرعيين والتوازي / Subagent brief, parallel fan-out and completion contract (documented)
- `THINK-29` ثلاثة خيارات وخيار «لا شيء» / Three real options + do-nothing + kill criteria (documented)
- `THINK-30` حقائق قبل أول تعديل / Fact-forcing + change impact before editing (documented)

### `THINK-29` — ثلاثة خيارات وخيار «لا شيء» / Three real options + do-nothing + kill criteria

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** لا توصية بلا بدائل: ثلاثة خيارات حقيقية منها «لا تغيّر شيئًا»، مع افتراضات الانقلاب وشروط الإيقاف. — No recommendation without alternatives: three real options including 'change nothing', with flip-assumptions and kill criteria.

**متى:** Strategy, product, architecture, purchases, any 'what should I do?'.

**كيف:** Frame the decision, users, outcome and horizon. Write ≥3 genuinely different options, one of which is to change nothing, and judge it properly. Mark the assumptions that flip the choice and compute thresholds in code. Check second-order effects, reversibility and dependencies. Pre-mortem the favourite (IDEA-04). Recommend in stages, each with a measure and a stop/review condition. Rank quickly with ICE = impact × confidence ÷ effort (1–5 each).

**المعاملات:** ≥3 options + do-nothing · ICE 1–5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** options · strategy · decision · kill criteria · ice · خيارات · استراتيجية · قرار · شروط الإيقاف

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-27` تفويض الوكلاء الفرعيين والتوازي / Subagent brief, parallel fan-out and completion contract (documented)
- `THINK-28` مجلس الأصوات الأربعة / Council of four voices (anti-anchoring decision) (documented)
- `THINK-30` حقائق قبل أول تعديل / Fact-forcing + change impact before editing (documented)
- `THINK-31` الاسترجاع المتكرر / Iterative retrieval: dispatch → evaluate → refine, ≤3 cycles (documented)

### `THINK-30` — حقائق قبل أول تعديل / Fact-forcing + change impact before editing

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** قبل تعديل ملف اجمع الحقائق: من يستورده، وما الدوال المتأثرة، وشكل البيانات، ونص طلب المستخدم حرفيًا. — Before editing a file gather the facts: who imports it, which functions change, the data shapes, and the user's instruction quoted verbatim.

**متى:** First edit of any file in an unfamiliar area; any change to shared code, formats or schemas.

**كيف:** Edit facts: importers/callers (`rg -n <symbol>`), public functions affected, field names and formats of data touched, the instruction quoted. New file facts: who will call it, proof that nothing existing does the same. Impact order: code (entry points, callers, generated files) → data (schemas, caches) → interfaces (APIs, file formats, CLIs) → the tests that prove success → docs → release/rollback. Evidence only from real imports, grep and tests — never from directory names; mark unknowns 'unverified'. After: did the diff exceed scope? leftover temp code?

**المعاملات:** 4 facts per edit · 6-step impact order

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** change impact · blast radius · gateguard · investigate · أثر التعديل · حقائق · قبل التعديل · نطاق

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-28` مجلس الأصوات الأربعة / Council of four voices (anti-anchoring decision) (documented)
- `THINK-29` ثلاثة خيارات وخيار «لا شيء» / Three real options + do-nothing + kill criteria (documented)
- `THINK-31` الاسترجاع المتكرر / Iterative retrieval: dispatch → evaluate → refine, ≤3 cycles (documented)
- `THINK-32` بروتوكول فكّ التعثّر / Unstick protocol: introspect when looping or failing (documented)

### `THINK-31` — الاسترجاع المتكرر / Iterative retrieval: dispatch → evaluate → refine, ≤3 cycles

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** ابحث بحثًا واسعًا، وقيّم صلة كل نتيجة، ثم أعد البحث بمفردات المشروع نفسه، ولا تتجاوز ثلاث دورات. — Search broadly, score each hit's relevance, re-search with the project's own vocabulary, and stop within three cycles.

**متى:** Finding the right files or sources in a large codebase or corpus; briefing a subagent with context.

**كيف:** Cycle 1: broad globs + keywords. Score hits: 0.8–1 direct · 0.5–0.7 related · 0.2–0.4 tangential · <0.2 drop; note what context is missing. Refine with terms learnt in cycle 1 and target the gaps. Stop after ≤3 cycles or when ≥3 files score ≥0.7 with no critical gap. When orchestrating, question each subagent return and send it back once if it is thin.

**المعاملات:** ≤3 cycles · stop at ≥3 hits ≥0.7

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** retrieval · search · codebase · relevance · استرجاع · بحث · صلة · مفردات المشروع

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-29` ثلاثة خيارات وخيار «لا شيء» / Three real options + do-nothing + kill criteria (documented)
- `THINK-30` حقائق قبل أول تعديل / Fact-forcing + change impact before editing (documented)
- `THINK-32` بروتوكول فكّ التعثّر / Unstick protocol: introspect when looping or failing (documented)
- `THINK-33` اقتصاد السياق / Context economy: just-in-time loading, compaction at phase boundaries (documented)

### `THINK-32` — بروتوكول فكّ التعثّر / Unstick protocol: introspect when looping or failing

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** عندما تدور في حلقة أو تتكرر المحاولات بلا تقدم: التقط الحالة، وطابق النمط، واسترجع بخطوة صغيرة قابلة للتراجع. — When looping or retrying without progress: capture the state, match the pattern, recover with one small reversible step.

**متى:** Same command repeated, retries without progress, context bloat, file/env mismatch, three failed attempts.

**كيف:** Capture: goal, exact error, last good step, last failed command, repeated pattern, environment assumptions (cwd, branch, services). Match: repeated command → no-exit loop; duplicated plans / huge logs → degraded reasoning, trim context; ECONNREFUSED / timeout → wrong port or service down; 429 → retry storm; file missing after write → wrong cwd/branch; tests still failing → wrong hypothesis, isolate one test. Recover: stop retrying, restate the hypothesis, re-observe the real state, narrow to one command/file/test, switch from speculation to observation, escalate if risky. Never claim a self-repair you did not perform (CHECK-29).

**المعاملات:** trigger after 3 failed attempts · 6 known patterns

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** stuck · loop · debugging · introspection · تعثر · حلقة مفرغة · تصحيح · مراجعة ذاتية

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:hypothesis` ← python3 -c "import hypothesis" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-30` حقائق قبل أول تعديل / Fact-forcing + change impact before editing (documented)
- `THINK-31` الاسترجاع المتكرر / Iterative retrieval: dispatch → evaluate → refine, ≤3 cycles (documented)
- `THINK-33` اقتصاد السياق / Context economy: just-in-time loading, compaction at phase boundaries (documented)
- `THINK-34` مسح الأنماط المضادة / Anti-pattern sweep before sending (documented)

### `THINK-33` — اقتصاد السياق / Context economy: just-in-time loading, compaction at phase boundaries

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** السياق ميزانية محدودة: حمّل ما تحتاجه عند الحاجة، واحفظ الخطة على القرص، ولخّص عند حدود المراحل. — Context is a finite budget: load what you need when you need it, keep the plan on disk, and compact at phase boundaries.

**متى:** Long tasks, large files or logs, many tools enabled, multi-phase work.

**كيف:** Use grep / head / `sed -n` ranges instead of dumping files or logs; load by path just in time. Keep a plan or notes file on disk and a todo list — they survive compaction; reasoning and file contents do not. Compact or clear at phase boundaries (research → plan, plan → build, after a failed approach), not mid-implementation. Subagents return summaries. Live context usage cannot be inferred from files: use the host's meter or say it is unknown. Keep few tools/connectors loaded.

**المعاملات:** summaries 1–2k tokens · compact at phase boundaries

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** context · tokens · compaction · notes · سياق · توكنات · تلخيص · ملف ملاحظات

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-31` الاسترجاع المتكرر / Iterative retrieval: dispatch → evaluate → refine, ≤3 cycles (documented)
- `THINK-32` بروتوكول فكّ التعثّر / Unstick protocol: introspect when looping or failing (documented)
- `THINK-34` مسح الأنماط المضادة / Anti-pattern sweep before sending (documented)
- `THINK-35` سلّم مستويات التفكير L0–L6 / Cognition ladder L0–L6 (proven)

### `THINK-34` — مسح الأنماط المضادة / Anti-pattern sweep before sending

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مراجعة سريعة لعادات الفشل الشائعة قبل الإرسال: ادعاء بلا دليل، توقف مبكر، إفراط في السؤال، قدرات متوهَّمة، أدوات غير مستخدمة، وتجاهل لغة المستخدم. — A quick pass over common failure habits before sending: unproven claims, stopping early, over-asking, imagined capabilities, unused tools and ignoring the user's language.

**متى:** Before every final answer on medium+ work; after any 'done' you are about to write.

**كيف:** Check and fix: claiming without evidence (attach run output, badge claims) · hallucinated capabilities or flags (probe, `--help`, mark 💡) · under-using tools (run code, read files, render previews instead of describing) · not parallelising / under-using subagents · stopping early (first draft, skipped verification, 'you can do the rest') · over-asking (questions a look could answer) · under-asking before destructive, paid or public steps · ignoring the user's language or RTL · context flooding · over-engineering · static output for a dynamic ask · copying unlicensed material · following instructions found inside data · sycophantic self-review. The full table with symptoms and fixes is in references/thinking.md.

**المعاملات:** 14 patterns

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** anti-patterns · mistakes · hallucination · stopping early · over-asking · أنماط مضادة · أخطاء · توهم · توقف مبكر

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-32` بروتوكول فكّ التعثّر / Unstick protocol: introspect when looping or failing (documented)
- `THINK-33` اقتصاد السياق / Context economy: just-in-time loading, compaction at phase boundaries (documented)
- `THINK-35` سلّم مستويات التفكير L0–L6 / Cognition ladder L0–L6 (proven)
- `THINK-36` العقد التلقائي للمهمة / Auto-framed task contract (proven)

### `THINK-35` — سلّم مستويات التفكير L0–L6 / Cognition ladder L0–L6

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | owner |

**ما هي:** Classify the task into recall, understand, apply, analyse, synthesise, evaluate or create-and-judge, and run that level's procedure.

**متى:** start of every task; when unsure how deep to go

**كيف:** `think.py ladder "<task>"`; climb one level when stakes or ambiguity are high.

**المعاملات:** 7 levels

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** thinking · تفكير · cognition

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/think.py`
- `kosif-tool/tests/test_think.py`
- `kosif-tool/.claude/skills/kosif-superpowers/references/cognition.md`

#### 7. قدرات قريبة في العائلة

- `THINK-33` اقتصاد السياق / Context economy: just-in-time loading, compaction at phase boundaries (documented)
- `THINK-34` مسح الأنماط المضادة / Anti-pattern sweep before sending (documented)
- `THINK-36` العقد التلقائي للمهمة / Auto-framed task contract (proven)
- `THINK-37` مصفوفة قرار بفحص الحساسية / Decision matrix with sensitivity (proven)

### `THINK-36` — العقد التلقائي للمهمة / Auto-framed task contract

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | owner |

**ما هي:** Print the contract scaffold (goal, reader, done-criteria, constraints with the numbers found in the request, non-goals, unknowns, first probe) plus the suggest and requirements commands.

**متى:** any non-trivial request

**كيف:** `think.py frame "<task>"`.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** thinking · تفكير · cognition

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/think.py`
- `kosif-tool/tests/test_think.py`
- `kosif-tool/.claude/skills/kosif-superpowers/references/cognition.md`

#### 7. قدرات قريبة في العائلة

- `THINK-34` مسح الأنماط المضادة / Anti-pattern sweep before sending (documented)
- `THINK-35` سلّم مستويات التفكير L0–L6 / Cognition ladder L0–L6 (proven)
- `THINK-37` مصفوفة قرار بفحص الحساسية / Decision matrix with sensitivity (proven)
- `THINK-38` تقدير فيرمي بمونت كارلو / Monte-Carlo Fermi estimate (proven)

### `THINK-37` — مصفوفة قرار بفحص الحساسية / Decision matrix with sensitivity

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | owner |

**ما هي:** Weighted totals in code and every ±1 weight change that flips the winner; a flip means the choice is really about weights.

**متى:** choosing tools, vendors, designs

**كيف:** `think.py decide decision.json` → totals, winner, margin, robust, flips.

**المعاملات:** weights integers; scores 1–5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** thinking · تفكير · cognition

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/think.py`
- `kosif-tool/tests/test_think.py`
- `kosif-tool/.claude/skills/kosif-superpowers/references/cognition.md`

#### 7. قدرات قريبة في العائلة

- `THINK-35` سلّم مستويات التفكير L0–L6 / Cognition ladder L0–L6 (proven)
- `THINK-36` العقد التلقائي للمهمة / Auto-framed task contract (proven)
- `THINK-38` تقدير فيرمي بمونت كارلو / Monte-Carlo Fermi estimate (proven)
- `THINK-39` ناقد المسودة الآلي / Automatic draft critic (proven)

### `THINK-38` — تقدير فيرمي بمونت كارلو / Monte-Carlo Fermi estimate

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | owner |

**ما هي:** Factor tree with ranges sampled log-uniformly; report p10/p50/p90 instead of one number.

**متى:** sizing, budgets, reach estimates

**كيف:** `think.py fermi "a*b" --range a=lo:hi b=lo:hi`.

**المعاملات:** 20 000 samples, seeded

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** thinking · تفكير · cognition

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/think.py`
- `kosif-tool/tests/test_think.py`
- `kosif-tool/.claude/skills/kosif-superpowers/references/cognition.md`

#### 7. قدرات قريبة في العائلة

- `THINK-36` العقد التلقائي للمهمة / Auto-framed task contract (proven)
- `THINK-37` مصفوفة قرار بفحص الحساسية / Decision matrix with sensitivity (proven)
- `THINK-39` ناقد المسودة الآلي / Automatic draft critic (proven)
- `THINK-40` اختيار النماذج الذهنية للمشكلة / Mental-model selection for a problem (proven)

### `THINK-39` — ناقد المسودة الآلي / Automatic draft critic

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | owner |

**ما هي:** Flag intensifiers, unverified claims, absolutes, vague lists, AI-tell vocabulary and unproven completion words in a draft.

**متى:** before sending any long answer or document

**كيف:** `think.py critic draft.md`.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** thinking · تفكير · cognition

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/think.py`
- `kosif-tool/tests/test_think.py`
- `kosif-tool/.claude/skills/kosif-superpowers/references/cognition.md`

#### 7. قدرات قريبة في العائلة

- `THINK-37` مصفوفة قرار بفحص الحساسية / Decision matrix with sensitivity (proven)
- `THINK-38` تقدير فيرمي بمونت كارلو / Monte-Carlo Fermi estimate (proven)
- `THINK-40` اختيار النماذج الذهنية للمشكلة / Mental-model selection for a problem (proven)
- `THINK-41` اكتشاف المشكلة الحقيقية / Problem finding: three statements (documented)

### `THINK-40` — اختيار النماذج الذهنية للمشكلة / Mental-model selection for a problem

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | owner |

**ما هي:** Rank 63 mental models by Arabic/English triggers (with Arabic prefix stripping) and print each one's question, steps, output and pitfall.

**متى:** analysis, strategy, decisions, diagnosis

**كيف:** `think.py models "<problem>" -n 5`.

**المعاملات:** 63 models

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** thinking · تفكير · cognition

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/think.py`
- `kosif-tool/tests/test_think.py`
- `kosif-tool/.claude/skills/kosif-superpowers/references/cognition.md`

#### 7. قدرات قريبة في العائلة

- `THINK-38` تقدير فيرمي بمونت كارلو / Monte-Carlo Fermi estimate (proven)
- `THINK-39` ناقد المسودة الآلي / Automatic draft critic (proven)
- `THINK-41` اكتشاف المشكلة الحقيقية / Problem finding: three statements (documented)
- `THINK-42` إعادة التأطير مرتين / Reframe twice before solving (documented)

### `THINK-41` — اكتشاف المشكلة الحقيقية / Problem finding: three statements

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** Write the problem three ways (user's words, root cause, opportunity) and solve the one with most leverage.

**متى:** vague or symptom-level requests

**كيف:** cognition.md §3.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** thinking · تفكير · cognition

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-39` ناقد المسودة الآلي / Automatic draft critic (proven)
- `THINK-40` اختيار النماذج الذهنية للمشكلة / Mental-model selection for a problem (proven)
- `THINK-42` إعادة التأطير مرتين / Reframe twice before solving (documented)
- `THINK-43` محاكاة الخبير / Expert simulation (documented)

### `THINK-42` — إعادة التأطير مرتين / Reframe twice before solving

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** Ask what if the constraint is the feature, what if the audience changes, what would make the problem unnecessary.

**متى:** stuck or generic results

**كيف:** cognition.md §3.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** thinking · تفكير · cognition

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-40` اختيار النماذج الذهنية للمشكلة / Mental-model selection for a problem (proven)
- `THINK-41` اكتشاف المشكلة الحقيقية / Problem finding: three statements (documented)
- `THINK-43` محاكاة الخبير / Expert simulation (documented)
- `THINK-44` نموذج القارئ البشري / Reader model (theory of mind) (documented)

### `THINK-43` — محاكاة الخبير / Expert simulation

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** Ask what the best practitioner in this field would do now, list their first three checks, and compare with your plan.

**متى:** domains outside daily practice

**كيف:** cognition.md §8 q5; pair with circle of competence (MODEL-05).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** thinking · تفكير · cognition

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-41` اكتشاف المشكلة الحقيقية / Problem finding: three statements (documented)
- `THINK-42` إعادة التأطير مرتين / Reframe twice before solving (documented)
- `THINK-44` نموذج القارئ البشري / Reader model (theory of mind) (documented)
- `THINK-45` المراقبة الذاتية عند الحدود / Metacognition checkpoint (documented)

### `THINK-44` — نموذج القارئ البشري / Reader model (theory of mind)

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** Describe the reader in two lines (knows, wants, fears, next action) and edit the answer for them.

**متى:** every answer a person will act on

**كيف:** MODEL-38 + cognition.md §7.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** thinking · تفكير · cognition

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-42` إعادة التأطير مرتين / Reframe twice before solving (documented)
- `THINK-43` محاكاة الخبير / Expert simulation (documented)
- `THINK-45` المراقبة الذاتية عند الحدود / Metacognition checkpoint (documented)
- `THINK-46` عادات العبقرية العشر / Ten genius habits as procedures (documented)

### `THINK-45` — المراقبة الذاتية عند الحدود / Metacognition checkpoint

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** Six questions at each phase boundary or after two failed attempts: right problem, breaking assumption, looping, calibration, expert view, missed power.

**متى:** phase boundaries; repeated failure

**كيف:** cognition.md §8.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** thinking · تفكير · cognition

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-43` محاكاة الخبير / Expert simulation (documented)
- `THINK-44` نموذج القارئ البشري / Reader model (theory of mind) (documented)
- `THINK-46` عادات العبقرية العشر / Ten genius habits as procedures (documented)

### `THINK-46` — عادات العبقرية العشر / Ten genius habits as procedures

| الحقل | القيمة |
|---|---|
| العائلة | `thinking-core` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/thinking-core.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | owner |

**ما هي:** Problem finding, reframing, quantity first, distant analogy, combinatorial play, simplicity after mastery, taste, obsessive verification, long horizon, honesty — each with a check.

**متى:** creative or high-stakes work

**كيف:** cognition.md §3 table.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** thinking · تفكير · cognition

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:THINK-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `invention-lab` · `think`.
- مراحل النوع: الهدف بمؤشره ← ثلاثة خيارات مختلفة ← تقييم وحساسية ← تشريح مسبق ← بوابات مكتوبة ← خطوة أولى قابلة للتراجع.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: لكل هدف مؤشر وعتبة وتاريخ ← جدول المؤشرات
- إلزامي: ثلاثة خيارات مختلفة المنهج مع توصية ← جدول المقارنة
- جودة: تشريح مسبق بأهم أسباب الفشل والوقاية ← think.py plan
- جودة: بوابات go/pivot/kill مكتوبة قبل النتائج ← think.py gate
- إلزامي: خطوة أولى صغيرة قابلة للتراجع هذا الأسبوع ← مراجعة
- أمر الحكم في الوضع 1: `think.py qa plan --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `THINK-44` نموذج القارئ البشري / Reader model (theory of mind) (documented)
- `THINK-45` المراقبة الذاتية عند الحدود / Metacognition checkpoint (documented)

