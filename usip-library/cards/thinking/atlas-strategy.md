# `atlas-strategy` — التفكير والتخطيط والاستراتيجية (72 بطاقة)

> مكتبة بروتوكول USIP v5.6 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/atlas-strategy.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/thinking.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`ASTRAT-01` تدقيق جدوى تعدد الوكلاء مقابل وكيل واحد](#astrat-01--تدقيق-جدوى-تعدد-الوكلاء-مقابل-وكيل-واحد--audit-multi-agent-topology-against-single-agent-baseline)
- [`ASTRAT-02` حلقة مستقلة لتصريف قائمة المهام](#astrat-02--حلقة-مستقلة-لتصريف-قائمة-المهام--autonomous-backlog-draining-loop-and-single-task-ralph-loop)
- [`ASTRAT-03` توجيه أسئلة المؤسس إلى أدوار المستشارين التنفيذيين](#astrat-03--توجيه-أسئلة-المؤسس-إلى-أدوار-المستشارين-التنفيذيين--route-founder-questions-to-c-suite-advisor-roles)
- [`ASTRAT-04` إرسال المهام على موجات مع بوابات تحقق](#astrat-04--إرسال-المهام-على-موجات-مع-بوابات-تحقق--sequential-wave-dispatch-with-verification-gates)
- [`ASTRAT-05` تقدير ميزانية الوكلاء قبل التشغيل](#astrat-05--تقدير-ميزانية-الوكلاء-قبل-التشغيل--size-agent-budget-before-running-a-workflow)
- [`ASTRAT-06` خريطة تذاكر قرارات للعمل الضخم](#astrat-06--خريطة-تذاكر-قرارات-للعمل-الضخم--wayfinder-decision-ticket-map-for-huge-work)
- [`ASTRAT-07` تأهيل العميل بمراحل وبوابات تحقق](#astrat-07--تأهيل-العميل-بمراحل-وبوابات-تحقق--client-onboarding-with-phase-gate-checks)
- [`ASTRAT-08` تقرير استخدام الطاقة وانحراف العمل قيد التنفيذ](#astrat-08--تقرير-استخدام-الطاقة-وانحراف-العمل-قيد-التنفيذ--practice-utilisation-and-wip-variance-report)
- [`ASTRAT-09` تخطيط دفعة الموردين الأسبوعية مع الاستثناءات](#astrat-09--تخطيط-دفعة-الموردين-الأسبوعية-مع-الاستثناءات--weekly-supplier-pay-run-planning-with-exclusions)
- [`ASTRAT-10` فحص كلمات ASO وتدقيق القائمة](#astrat-10--فحص-كلمات-aso-وتدقيق-القائمة--app-store-optimization-keyword-probe-and-lint)
- [`ASTRAT-11` رحلة من الفكرة إلى التطبيق بمتتبع](#astrat-11--رحلة-من-الفكرة-إلى-التطبيق-بمتتبع--idea-to-app-journey-with-docs-tracker)
- [`ASTRAT-12` مراجعة مخاطر ما قبل البناء](#astrat-12--مراجعة-مخاطر-ما-قبل-البناء--pre-build-risk-review-and-kill-test)
- [`ASTRAT-13` قرار تخزين البيانات على السلسلة أو خارجها](#astrat-13--قرار-تخزين-البيانات-على-السلسلة-أو-خارجها--on-chain-versus-off-chain-data-placement)
- [`ASTRAT-14` اختبار استراتيجية تداول بمقاييس المخاطر](#astrat-14--اختبار-استراتيجية-تداول-بمقاييس-المخاطر--backtest-trading-strategy-with-risk-metrics)
- [`ASTRAT-15` تقييم DCF متين مع فحوص تقاطعية](#astrat-15--تقييم-dcf-متين-مع-فحوص-تقاطعية--defensible-dcf-valuation-with-cross-checks)
- [`ASTRAT-16` سجل مخاطر مؤسسي مع التقييم](#astrat-16--سجل-مخاطر-مؤسسي-مع-التقييم--enterprise-risk-register-with-scoring)
- [`ASTRAT-17` بناء الأعمال ومراجعة طلب التمويل للمؤسسين](#astrat-17--بناء-الأعمال-ومراجعة-طلب-التمويل-للمؤسسين--founder-business-building-and-fundraising-review)
- [`ASTRAT-18` بروتوكول مداولات مجلس إدارة متعدد الأدوار](#astrat-18--بروتوكول-مداولات-مجلس-إدارة-متعدد-الأدوار--multi-role-board-deliberation-protocol)
- [`ASTRAT-19` تصميم استراتيجية التسعير والربحية](#astrat-19--تصميم-استراتيجية-التسعير-والربحية--pricing-and-monetization-strategy-design)
- [`ASTRAT-20` ميزانية البحث والتطوير والحرق وتوجيه الرسملة](#astrat-20--ميزانية-البحث-والتطوير-والحرق-وتوجيه-الرسملة--rd-program-budget-burn-and-capitalization-routing)
- [`ASTRAT-21` نموذج جدول الملكية وتخفيف الحصص](#astrat-21--نموذج-جدول-الملكية-وتخفيف-الحصص--startup-cap-table-and-dilution-model)
- [`ASTRAT-22` لوحات الاستراتيجية وSWOT وفحص الافتراضات](#astrat-22--لوحات-الاستراتيجية-وswot-وفحص-الافتراضات--strategy-canvases-swot-and-red-team)
- [`ASTRAT-23` توقع نقدي متدحرج 13 أسبوع](#astrat-23--توقع-نقدي-متدحرج-13-أسبوع--13-week-rolling-cash-forecast-with-variance-loop)
- [`ASTRAT-24` تقسيم العملاء والمستخدمين حسب القيمة](#astrat-24--تقسيم-العملاء-والمستخدمين-حسب-القيمة--customer-and-user-segmentation-by-value)
- [`ASTRAT-25` مواصفة تجربة مع بوابة قرار](#astrat-25--مواصفة-تجربة-مع-بوابة-قرار--experiment-design-spec-with-gono-go-gate)
- [`ASTRAT-26` تشخيص تسرب القمع والاحتفاظ](#astrat-26--تشخيص-تسرب-القمع-والاحتفاظ--funnel-and-retention-drop-off-diagnosis)
- [`ASTRAT-27` هيكلة المقاييس ووثائق التعريف](#astrat-27--هيكلة-المقاييس-ووثائق-التعريف--metrics-architecture-and-definition-docs)
- [`ASTRAT-28` تحليل الأسباب الجذرية والمخاطر](#astrat-28--تحليل-الأسباب-الجذرية-والمخاطر--root-cause-and-risk-analysis-fishbone-pfmea-lean)
- [`ASTRAT-29` دراسة الاستعداد للدفع وتغيير الأسعار](#astrat-29--دراسة-الاستعداد-للدفع-وتغيير-الأسعار--willingness-to-pay-and-price-change-planning)
- [`ASTRAT-30` قرار البث مقابل الدفعات](#astrat-30--قرار-البث-مقابل-الدفعات--streaming-versus-batch-decision)
- [`ASTRAT-31` اختيار قاعدة بيانات سحابية مناسبة](#astrat-31--اختيار-قاعدة-بيانات-سحابية-مناسبة--cloud-database-selection-and-managed-service-routing)
- [`ASTRAT-32` سلسلة خمسة لماذا مع تحقق](#astrat-32--سلسلة-خمسة-لماذا-مع-تحقق--5-why-root-cause-chain-with-validation)
- [`ASTRAT-33` دليل حادثة: فرز واحتواء واستعادة ومراجعة](#astrat-33--دليل-حادثة-فرز-واحتواء-واستعادة-ومراجعة--incident-runbook-triage-contain-recover-review)
- [`ASTRAT-34` فرز الحادث مقابل المشكلة وتحديد الخطورة](#astrat-34--فرز-الحادث-مقابل-المشكلة-وتحديد-الخطورة--incident-vs-problem-triage-and-severity)
- [`ASTRAT-35` تحليل السبب الجذري بخمسة لماذا وإيشيكاوا](#astrat-35--تحليل-السبب-الجذري-بخمسة-لماذا-وإيشيكاوا--root-cause-analysis-with-5-whys-and-fishbone)
- [`ASTRAT-36` إسناد تكلفة استخدام API وضوابط الإنفاق](#astrat-36--إسناد-تكلفة-استخدام-api-وضوابط-الإنفاق--api-usage-cost-attribution-and-spend-controls)
- [`ASTRAT-37` أدلة قرارات معمارية السحابة](#astrat-37--أدلة-قرارات-معمارية-السحابة--cloud-architecture-decision-playbooks)
- [`ASTRAT-38` حصاد هدر السحابة وترتيب تسرب التكلفة](#astrat-38--حصاد-هدر-السحابة-وترتيب-تسرب-التكلفة--cloud-waste-harvest-and-cost-leak-ranking)
- [`ASTRAT-39` تعريف SLI وSLO وميزانية الخطأ](#astrat-39--تعريف-sli-وslo-وميزانية-الخطأ--define-slis-slos-and-error-budgets)
- [`ASTRAT-40` تدقيق خفض التكلفة المبني على الاستخدام](#astrat-40--تدقيق-خفض-التكلفة-المبني-على-الاستخدام--usage-driven-cost-tuning-audit-for-saasapi-spend)
- [`ASTRAT-41` خطة اختبار اختراق للذكاء الاصطناعي ومعالجتها](#astrat-41--خطة-اختبار-اختراق-للذكاء-الاصطناعي-ومعالجتها--ai-red-team-plan-and-remediation)
- [`ASTRAT-42` سلم توجيه النماذج حسب التكلفة](#astrat-42--سلم-توجيه-النماذج-حسب-التكلفة--cost-per-task-model-routing-ladder)
- [`ASTRAT-43` جاهزية قانون الذكاء الأوروبي وفحص التحيز](#astrat-43--جاهزية-قانون-الذكاء-الأوروبي-وفحص-التحيز--eu-ai-act-readiness-and-bias-check)
- [`ASTRAT-44` تدقيق تكلفة LLM والتوجيه](#astrat-44--تدقيق-تكلفة-llm-والتوجيه--llm-cost-audit-and-routing)
- [`ASTRAT-45` مراجعة برنامج مكافحة غسل الأموال](#astrat-45--مراجعة-برنامج-مكافحة-غسل-الأموال--aml-program-review-against-fatfffiec)
- [`ASTRAT-46` تشخيص هامش الربح ومزيج الخدمات](#astrat-46--تشخيص-هامش-الربح-ومزيج-الخدمات--small-business-margin-and-mix-diagnostics)
- [`ASTRAT-47` مراجعة التصميم بالقواعد الإرشادية](#astrat-47--مراجعة-التصميم-بالقواعد-الإرشادية--design-review-heuristics-and-critique)
- [`ASTRAT-48` جولة موازنة اقتصاد اللعبة](#astrat-48--جولة-موازنة-اقتصاد-اللعبة--game-balance-and-economy-tuning-pass)
- [`ASTRAT-49` تصميم الآليات وتجربة اللاعب](#astrat-49--تصميم-الآليات-وتجربة-اللاعب--game-mechanics-and-player-experience-design)
- [`ASTRAT-50` تصنيف مؤشرات DORA الأربعة](#astrat-50--تصنيف-مؤشرات-dora-الأربعة--dora-four-keys-classification)
- [`ASTRAT-51` قراءة المؤشرات التشغيلية الصناعية](#astrat-51--قراءة-المؤشرات-التشغيلية-الصناعية--frequency-vs-severity-operating-metrics)
- [`ASTRAT-52` تفكيك المتطلبات لمهام قابلة للتنفيذ](#astrat-52--تفكيك-المتطلبات-لمهام-قابلة-للتنفيذ--task-breakdown-with-sizing-rules)
- [`ASTRAT-53` إصدار أمني منسق](#astrat-53--إصدار-أمني-منسق--coordinated-security-release)
- [`ASTRAT-54` بطاقات أنكي عبر AnkiConnect](#astrat-54--بطاقات-أنكي-عبر-ankiconnect--anki-flashcards-via-ankiconnect)
- [`ASTRAT-55` إعداد دورة Google Classroom والطلاب](#astrat-55--إعداد-دورة-google-classroom-والطلاب--google-classroom-course-setup-and-roster)
- [`ASTRAT-56` مدرب تعلم متعدد الجلسات بحالة محفوظة](#astrat-56--مدرب-تعلم-متعدد-الجلسات-بحالة-محفوظة--multi-session-learning-coach-with-persistent-state)
- [`ASTRAT-57` بروتوكول تدريس سقراطي سؤال واحد كل مرة](#astrat-57--بروتوكول-تدريس-سقراطي-سؤال-واحد-كل-مرة--socratic-one-question-at-a-time-tutoring-protocol)
- [`ASTRAT-58` الوظائف المطلوب إنجازها بأبعادها الثلاثة](#astrat-58--الوظائف-المطلوب-إنجازها-بأبعادها-الثلاثة--jobs-to-be-done-with-all-three-dimensions)
- [`ASTRAT-59` التموضع: السياق قبل الرسالة](#astrat-59--التموضع-السياق-قبل-الرسالة--positioning-as-context-obviously-awesome-canvas)
- [`ASTRAT-60` تحسين التحويل: اكتشف ولا تخمّن](#astrat-60--تحسين-التحويل-اكتشف-ولا-تخمّن--conversion-optimisation-discover-do-not-guess)
- [`ASTRAT-61` تحسين الظهور في البحث ومحركات الإجابة والذكاء التوليدي](#astrat-61--تحسين-الظهور-في-البحث-ومحركات-الإجابة-والذكاء-التوليدي--seo-answer-engine-and-generative-engine-visibility)
- [`ASTRAT-62` مراجعة تصميم بأسلوب الطرح حتى الجوهر](#astrat-62--مراجعة-تصميم-بأسلوب-الطرح-حتى-الجوهر--subtractive-design-review-from-the-customer-backwards)
- [`ASTRAT-63` مقابلة سؤال-بسؤال لاستخراج النية الحقيقية قبل البناء](#astrat-63--مقابلة-سؤال-بسؤال-لاستخراج-النية-الحقيقية-قبل-البناء--one-question-interview-to-extract-real-intent)
- [`ASTRAT-64` خطاب تقديم وظيفي مفصّل على الإعلان بلا عبارات آلية](#astrat-64--خطاب-تقديم-وظيفي-مفصّل-على-الإعلان-بلا-عبارات-آلية--tailored-cover-letter-without-ai-tells)
- [`ASTRAT-65` التفاوض بالتعاطف التكتيكي والأسئلة المعايَرة](#astrat-65--التفاوض-بالتعاطف-التكتيكي-والأسئلة-المعايَرة--negotiation-with-tactical-empathy-and-calibrated-questions)
- [`ASTRAT-66` تصميم الفرق للتدفق السريع: أربعة أنواع وثلاثة أنماط تفاعل](#astrat-66--تصميم-الفرق-للتدفق-السريع-أربعة-أنواع-وثلاثة-أنماط-تفاعل--team-topologies-four-team-types-three-interaction-modes)
- [`ASTRAT-67` تحقيق 8D ببوابات تحقق لكل مرحلة](#astrat-67--تحقيق-8d-ببوابات-تحقق-لكل-مرحلة--gated-8d-investigation-coach)
- [`ASTRAT-68` كتابة تقرير إجراء تصحيحي CAR/CAPA قابل للإغلاق](#astrat-68--كتابة-تقرير-إجراء-تصحيحي-carcapa-قابل-للإغلاق--closable-corrective-action-report-carcapa)
- [`ASTRAT-69` وصفة إعدادات LoRA وQLoRA للضبط الدقيق](#astrat-69--وصفة-إعدادات-lora-وqlora-للضبط-الدقيق--lora-and-qlora-fine-tuning-recipe)
- [`ASTRAT-70` سلّم أنظمة دعم العملاء من الخدمة الذاتية إلى مركز الاتصال](#astrat-70--سلّم-أنظمة-دعم-العملاء-من-الخدمة-الذاتية-إلى-مركز-الاتصال--customer-support-system-ladder-self-service-to-contact-center)
- [`ASTRAT-71` صياغة الردود للعمل أولًا لقارئ مشتت الانتباه](#astrat-71--صياغة-الردود-للعمل-أولًا-لقارئ-مشتت-الانتباه--action-first-response-shape-for-an-adhd-reader)
- [`ASTRAT-72` تقرير جلسة برمجة لصاحب قرار غير تقني](#astrat-72--تقرير-جلسة-برمجة-لصاحب-قرار-غير-تقني--session-report-for-a-non-technical-stakeholder)

## البطاقات / cards

### `ASTRAT-01` — تدقيق جدوى تعدد الوكلاء مقابل وكيل واحد / Audit multi-agent topology against single-agent baseline

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0 / MIT (no copyleft seen among supporting ids); the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** عدّ حدود السياق بين الوكلاء في سير عمل متعدد، وتسعير ما يضيع عند كل حد مقابل ما يكسبه، والتوصية بإلغاء أي حد يتفوق عليه وكيل واحد قادر. — Count the context boundaries in a multi-agent workflow, price what each one loses, compare with what it buys, and recommend collapsing any boundary that a single capable agent would beat.

**متى:** Before adding another agent or phase; a workflow is slow and nobody knows which part earns its time; agents keep agreeing; a handoff keeps losing information; post-mortem of a bad multi-agent result.

**كيف:** 1) List every point where context crosses between agents, including human to first agent and last agent to human; count crossings, not agents. 2) For each crossing note only the costs that apply: restating tokens and latency, handoff gaps, compression loss from free-text summaries, semantic drift, verification burden, governance waits. 3) Name what the boundary buys: real specialization, true wall-clock parallelism, cross-vendor diversity, or an adversarial reviewer whose disagreement is the product. 4) Compare with the single-expert baseline; the burden of proof is on the boundary; no gain term means collapse. 5) Label output prediction (described) or measurement (transcript).

**المعاملات:** workflow description or transcript; agent roster; what passes between agents

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** multi-agent · topology · coordination-cost · تدقيق-وكلاء · strategy

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2673-claude-octopus/10196-skill-agent-topology`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2875-codex-howto/11595-orchestrate-engineering`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3111-constellation/13314-roundtable`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-02` حلقة مستقلة لتصريف قائمة المهام / Autonomous backlog-draining loop and single-task ralph loop (documented)
- `ASTRAT-03` توجيه أسئلة المؤسس إلى أدوار المستشارين التنفيذيين / Route founder questions to C-suite advisor roles (documented)

### `ASTRAT-02` — حلقة مستقلة لتصريف قائمة المهام / Autonomous backlog-draining loop and single-task ralph loop

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تصريف قائمة العمل بحلقة ذاتية أو تنفيذ مهمة واحدة محددة حتى إيداع موثق. — Drain a work backlog on a self-paced loop, or execute exactly one assigned task to a queued commit.

**متى:** Backlog grinding or one explicit Kanban task.

**كيف:** 1) Each cycle triage intake, admit items through gates. 2) Work one item only; never edit tasks.md, push or deploy. 3) Log related follow-ups as new tasks instead of widening scope. 4) Validate before commit.

**المعاملات:** task id

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** loop · kanban · حلقة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2484-work-items/9646-work-loop`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3610-yylo/14516-ralph-loop`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-01` تدقيق جدوى تعدد الوكلاء مقابل وكيل واحد / Audit multi-agent topology against single-agent baseline (documented)
- `ASTRAT-03` توجيه أسئلة المؤسس إلى أدوار المستشارين التنفيذيين / Route founder questions to C-suite advisor roles (documented)
- `ASTRAT-04` إرسال المهام على موجات مع بوابات تحقق / Sequential wave dispatch with verification gates (documented)

### `ASTRAT-03` — توجيه أسئلة المؤسس إلى أدوار المستشارين التنفيذيين / Route founder questions to C-suite advisor roles

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT (no copyleft seen among supporting ids); the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** إجراء مقابلة واحدة مع المؤسس تُحفظ في ملف سياق شركة مشترك، ثم توجيه كل سؤال إلى أدوار المستشارين التنفيذيين المناسبة وعقد اجتماعات مجلس متعددة الأدوار بقواعد منع الحلقات وتلخيص قرار مُتتبَّع. — Interview the founder once into a shared company-context file, then route each question to the right executive advisor roles, run multi-role board meetings with loop-prevention rules, and synthesize a tracked decision.

**متى:** A founder or small-team lead needs CFO/CMO/COO/CISO-style perspectives; a complex decision needs several roles; company context looks stale; first-time advisor setup.

**كيف:** 1) Onboard: a seven-dimension interview writes ~/.claude/company-context.md; refresh quarterly. 2) At each session start load that file and flag it stale when older than 90 days. 3) A chief-of-staff layer routes the question to one or more advisor roles (CFO, CMO, CRO, CPO, COO, CHRO, CISO, GC, CDO, CAIO, CCO, VPE). 4) Complex decisions trigger a multi-role board meeting; roles may query each other only through the agent protocol (invocation syntax, loop prevention, isolation, response format). 5) Anonymize company data before any external API call. 6) Synthesize the outputs and log the decision.

**المعاملات:** question; roles to include; company-context path; staleness threshold (90 days)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** c-suite · advisor-routing · company-context · مستشارون-تنفيذيون · board

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/138-c-level-skills/417-chief-of-staff`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/138-c-level-skills/423-context-engine`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/138-c-level-skills/427-cs-onboard`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-01` تدقيق جدوى تعدد الوكلاء مقابل وكيل واحد / Audit multi-agent topology against single-agent baseline (documented)
- `ASTRAT-02` حلقة مستقلة لتصريف قائمة المهام / Autonomous backlog-draining loop and single-task ralph loop (documented)
- `ASTRAT-04` إرسال المهام على موجات مع بوابات تحقق / Sequential wave dispatch with verification gates (documented)
- `ASTRAT-05` تقدير ميزانية الوكلاء قبل التشغيل / Size agent budget before running a workflow (documented)

### `ASTRAT-04` — إرسال المهام على موجات مع بوابات تحقق / Sequential wave dispatch with verification gates

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** جدولة عمل الوكلاء المعتمد بعضه على بعض في موجات تفصل بينها بوابات تحقق. — Schedule dependent agent work as waves (research, foundation, extension) with gates between each.

**متى:** Multi-step work with cross-task dependencies.

**كيف:** 1) Wave 1 research writes artefacts to tmp/. 2) Wave 2 foundation: new types/APIs, gate on build+tests green. 3) Wave 3 extensions: call sites, tests, docs. 4) Lock-holding tools run alone in a wave. 5) Fan out widely inside a wave. 6) On gate failure fix before next wave. 7) Retry schema-constrained agents with backoff under rate limits.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** waves · dispatch · موجات

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2175-workflow-orchestration-plugin/7951-workflow-wave-dispatch`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/256-zirkel/861-zirkel-solve`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-02` حلقة مستقلة لتصريف قائمة المهام / Autonomous backlog-draining loop and single-task ralph loop (documented)
- `ASTRAT-03` توجيه أسئلة المؤسس إلى أدوار المستشارين التنفيذيين / Route founder questions to C-suite advisor roles (documented)
- `ASTRAT-05` تقدير ميزانية الوكلاء قبل التشغيل / Size agent budget before running a workflow (documented)
- `ASTRAT-06` خريطة تذاكر قرارات للعمل الضخم / Wayfinder decision-ticket map for huge work (documented)

### `ASTRAT-05` — تقدير ميزانية الوكلاء قبل التشغيل / Size agent budget before running a workflow

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تقدير عدد الوكلاء وتكلفتهم وتجميع العناصر بالمواضيع قبل إطلاق سير عمل كبير. — Estimate agent count and cost per item, group by theme, and design re-drives before launching a large workflow.

**متى:** About to launch a many-agent run.

**كيف:** 1) Count items and per-item agent multipliers. 2) Estimate cost per agent. 3) Group items by theme to cut agents. 4) Plan re-drive for failed items. 5) Compare to budget; cut scope if over.

**المعاملات:** item count, budget

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** budget · scale · ميزانية

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2175-workflow-orchestration-plugin/7949-workflow-scale-budget`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-03` توجيه أسئلة المؤسس إلى أدوار المستشارين التنفيذيين / Route founder questions to C-suite advisor roles (documented)
- `ASTRAT-04` إرسال المهام على موجات مع بوابات تحقق / Sequential wave dispatch with verification gates (documented)
- `ASTRAT-06` خريطة تذاكر قرارات للعمل الضخم / Wayfinder decision-ticket map for huge work (documented)
- `ASTRAT-07` تأهيل العميل بمراحل وبوابات تحقق / Client onboarding with phase gate checks (documented)

### `ASTRAT-06` — خريطة تذاكر قرارات للعمل الضخم / Wayfinder decision-ticket map for huge work

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** رسم العمل الكبير كخريطة بتذاكر قرارات فرعية بحجم جلسة واحدة وحلها تباعا. — Chart oversized work as a map issue with child decision tickets sized to one session and resolve them one by one.

**متى:** Work exceeds one agent session and the path to the goal is unclear.

**كيف:** 1) Name the destination. 2) Create map issue (labelled wayfinder:map) with Destination, Notes, Decisions so far, Not yet specified, Out of scope. 3) Child tickets with a Question, typed research/prototype/grilling/task, about 100K tokens each. 4) Claim by assigning first. 5) Use native blocking for the frontier. 6) Plan, do not execute; map only gists decisions and links.

**المعاملات:** issue tracker

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** planning · تخطيط · tickets

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2224-mattpocock-skills/8424-wayfinder`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-04` إرسال المهام على موجات مع بوابات تحقق / Sequential wave dispatch with verification gates (documented)
- `ASTRAT-05` تقدير ميزانية الوكلاء قبل التشغيل / Size agent budget before running a workflow (documented)
- `ASTRAT-07` تأهيل العميل بمراحل وبوابات تحقق / Client onboarding with phase gate checks (documented)
- `ASTRAT-08` تقرير استخدام الطاقة وانحراف العمل قيد التنفيذ / Practice utilisation and WIP variance report (documented)

### `ASTRAT-07` — تأهيل العميل بمراحل وبوابات تحقق / Client onboarding with phase gate checks

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يمرر العميل عبر مراحل الارتباط والربط والإعداد والتشغيل مع بوابة تحقق في كل مرحلة. — Run a client through engagement, connection, configuration and go-live phases with a gate check at each.

**متى:** Starting a new client or integration rollout.

**كيف:** 1) Define four phases. 2) Write exit criteria per phase. 3) Block progress until gate passes. 4) Record outcome and owner. 5) Summarise outstanding items at go-live.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** onboarding · checklist · gates · تأهيل · مراحل

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3560-xbert-client-onboard/14372-client-onboard`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3580-xbert-pulse/14392-client-pulse`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-05` تقدير ميزانية الوكلاء قبل التشغيل / Size agent budget before running a workflow (documented)
- `ASTRAT-06` خريطة تذاكر قرارات للعمل الضخم / Wayfinder decision-ticket map for huge work (documented)
- `ASTRAT-08` تقرير استخدام الطاقة وانحراف العمل قيد التنفيذ / Practice utilisation and WIP variance report (documented)
- `ASTRAT-09` تخطيط دفعة الموردين الأسبوعية مع الاستثناءات / Weekly supplier pay-run planning with exclusions (documented)

### `ASTRAT-08` — تقرير استخدام الطاقة وانحراف العمل قيد التنفيذ / Practice utilisation and WIP variance report

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يعد تقريرا عن نسبة الساعات القابلة للفوترة وانحراف العمل لكل مكتب وعميل مقابل حدود محددة مع إجراءات موصى بها. — Report billable percentage and WIP variance per practice and client against thresholds with recommended actions.

**متى:** Reviewing capacity, overruns or internal practice reports.

**كيف:** 1) Billable % = billable / tracked hours; WIP variance = (actual - planned) / planned. 2) Targets: billable 65-75% full-service, 70-85% bookkeeping; practice variance within 10%, client within 20%. 3) Flags: above +25% scope review, above +50% under-priced, below -25% over-planned. 4) Show both metrics together, note unsubmitted time, prefer 3-month trend. 5) Markdown report: practice level, top client variances table, actions, methodology. Read-only.

**المعاملات:** period, thresholds

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** utilisation · wip · kpi · تقرير · طاقة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3557-xbert-capacity/14369-capacity-reporting`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3580-xbert-pulse/14392-client-pulse`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-06` خريطة تذاكر قرارات للعمل الضخم / Wayfinder decision-ticket map for huge work (documented)
- `ASTRAT-07` تأهيل العميل بمراحل وبوابات تحقق / Client onboarding with phase gate checks (documented)
- `ASTRAT-09` تخطيط دفعة الموردين الأسبوعية مع الاستثناءات / Weekly supplier pay-run planning with exclusions (documented)
- `ASTRAT-10` فحص كلمات ASO وتدقيق القائمة / App Store Optimization keyword probe and lint (documented)

### `ASTRAT-09` — تخطيط دفعة الموردين الأسبوعية مع الاستثناءات / Weekly supplier pay-run planning with exclusions

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يخطط دفعة الموردين بإدراج الفواتير المستحقة المعتمدة وتوثيق كل استثناء وترتيب الأولويات وصياغة إشعار واحد لكل مورد. — Plan a pay run: include approved due bills, list every exclusion with a reason, score priorities and draft one remittance per supplier.

**متى:** Bookkeeper asks what to pay this week or to draft remittances.

**كيف:** 1) Include if awaiting payment, approved, due within 7 days or overdue, no hold or dispute, outstanding > 0. 2) Exclude with reason (held, disputed, unapproved, outside-window, zero); never drop silently. 3) Cashflow check: warn above 80% of bank balance, stop above 100% needing override. 4) Score: +10 discount window, +5 per week overdue, +5 critical supplier, -5 for 60+ day terms. 5) One remittance per supplier named client-remittance-supplier-date.pdf. 6) Never auto-pay or create the bank file.

**المعاملات:** pay window, thresholds

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** accounts-payable · remittance · cashflow · مدفوعات · موردين

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3575-xbert-payment-run/14387-payment-run`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3573-xbert-month-end-pack/14385-month-end-pack`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-07` تأهيل العميل بمراحل وبوابات تحقق / Client onboarding with phase gate checks (documented)
- `ASTRAT-08` تقرير استخدام الطاقة وانحراف العمل قيد التنفيذ / Practice utilisation and WIP variance report (documented)
- `ASTRAT-10` فحص كلمات ASO وتدقيق القائمة / App Store Optimization keyword probe and lint (documented)
- `ASTRAT-11` رحلة من الفكرة إلى التطبيق بمتتبع / Idea-to-app journey with docs tracker (documented)

### `ASTRAT-10` — فحص كلمات ASO وتدقيق القائمة / App Store Optimization keyword probe and lint

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يفحص الكلمات المفتاحية ويدقق بيانات المتجر من حيث الحدود والتغطية والحشو. — Probe keywords against live store data and lint per-locale listings for limits, coverage and stuffing.

**متى:** Optimizing an iOS or Play listing or localizing it.

**كيف:** 1) Write one markdown file per locale. 2) Probe candidates for intent (genre concentration), difficulty (median ratings of top 10) and density. 3) Assign terms to indexed surfaces: Apple name, subtitle, 100-char keyword field; Play title, short and full description. 4) Run linter for char limits, coverage gaps, duplicates, broken URLs; nonzero exit gates submission. 5) Validate volume in a paid tool.

**المعاملات:** locale, country, store

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** aso · app-store · تحسين المتجر · keywords

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2562-aso-craft/9929-aso-craft`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-08` تقرير استخدام الطاقة وانحراف العمل قيد التنفيذ / Practice utilisation and WIP variance report (documented)
- `ASTRAT-09` تخطيط دفعة الموردين الأسبوعية مع الاستثناءات / Weekly supplier pay-run planning with exclusions (documented)
- `ASTRAT-11` رحلة من الفكرة إلى التطبيق بمتتبع / Idea-to-app journey with docs tracker (documented)
- `ASTRAT-12` مراجعة مخاطر ما قبل البناء / Pre-build risk review and kill-test (documented)

### `ASTRAT-11` — رحلة من الفكرة إلى التطبيق بمتتبع / Idea-to-app journey with docs tracker

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يمر بالفكرة عبر مراحل ويسجل القرارات في متتبع بحالات واضحة. — Walk an app idea through phased skills while recording decisions in a docs tracker with statuses.

**متى:** Starting, growing or polishing an app end to end.

**كيف:** 1) Resume by reading tracker and artifacts. 2) Intake once. 3) Per phase announce decision and artifact; offer proceed/skip/defer. 4) Ask listed questions with recommendations and record key decisions. 5) Present draft for sign-off before writing docs files. 6) Update statuses pending/in-progress/awaiting-evidence/done.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** journey · tracker · رحلة التطبيق · docs

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3431-metaskills/14075-create-app`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-09` تخطيط دفعة الموردين الأسبوعية مع الاستثناءات / Weekly supplier pay-run planning with exclusions (documented)
- `ASTRAT-10` فحص كلمات ASO وتدقيق القائمة / App Store Optimization keyword probe and lint (documented)
- `ASTRAT-12` مراجعة مخاطر ما قبل البناء / Pre-build risk review and kill-test (documented)
- `ASTRAT-13` قرار تخزين البيانات على السلسلة أو خارجها / On-chain versus off-chain data placement (documented)

### `ASTRAT-12` — مراجعة مخاطر ما قبل البناء / Pre-build risk review and kill-test

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under mixed MIT/Apache; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يجري مراجعة استباقية لفكرة أو ميزة ويخرج بالحكم وأخطر افتراض وأرخص تحقق وما يؤجل. — Run a compact pre-mortem on an idea or feature and output verdict, riskiest assumption, cheapest validation and what to delay.

**متى:** User asks to build an MVP, SaaS, or major feature with unclear demand.

**كيف:** 1) Skip if narrow fix. 2) Score demand, positioning, monetization, retention, trust, distribution, adoption. 3) Output verdict low/medium/high with one sentence. 4) Name the single assumption most likely to break. 5) Give smallest evidence to find first and one next step. 6) List what not to build yet. Optionally challenge a wrong premise before coding (skeptic).

**المعاملات:** idea or feature brief

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pre-mortem · mvp · مراجعة المخاطر · validation

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3451-before-you-build/14154-before-you-build`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3431-metaskills/14075-create-app`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-10` فحص كلمات ASO وتدقيق القائمة / App Store Optimization keyword probe and lint (documented)
- `ASTRAT-11` رحلة من الفكرة إلى التطبيق بمتتبع / Idea-to-app journey with docs tracker (documented)
- `ASTRAT-13` قرار تخزين البيانات على السلسلة أو خارجها / On-chain versus off-chain data placement (documented)
- `ASTRAT-14` اختبار استراتيجية تداول بمقاييس المخاطر / Backtest trading strategy with risk metrics (documented)

### `ASTRAT-13` — قرار تخزين البيانات على السلسلة أو خارجها / On-chain versus off-chain data placement

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تحديد مكان تخزين البيانات حسب التكلفة والخصوصية. — Decide where data lives by cost and privacy, with hash pointers for integrity.

**متى:** Any data-placement question in a dApp.

**كيف:** 1) Classify data: consensus-critical vs ancillary. 2) Price storage as slots x gas x price. 3) Put media/history on IPFS/Arweave or an indexer with on-chain hash. 4) Confirm nothing sensitive is public forever.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** storage · ipfs · تخزين

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2247-blockchain-web3-engineering/8555-split-on-off-chain`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-11` رحلة من الفكرة إلى التطبيق بمتتبع / Idea-to-app journey with docs tracker (documented)
- `ASTRAT-12` مراجعة مخاطر ما قبل البناء / Pre-build risk review and kill-test (documented)
- `ASTRAT-14` اختبار استراتيجية تداول بمقاييس المخاطر / Backtest trading strategy with risk metrics (documented)
- `ASTRAT-15` تقييم DCF متين مع فحوص تقاطعية / Defensible DCF valuation with cross-checks (documented)

### `ASTRAT-14` — اختبار استراتيجية تداول بمقاييس المخاطر / Backtest trading strategy with risk metrics

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يختبر استراتيجية تداول على بيانات تاريخية دون انحياز استباقي ويقدّم مقاييس العائد والمخاطر. — Backtest a trading strategy on historical prices while avoiding look-ahead bias, then report Sharpe, Sortino, drawdown, VaR and CVaR.

**متى:** User wants to validate a trading idea, compare strategies, or compute portfolio risk (VaR/CVaR/drawdown).

**كيف:** 1) Fetch and cache OHLCV history. 2) Define signal with next-bar execution (no look-ahead), fees and slippage. 3) Run strategy over a fixed period with initial capital. 4) Compute Sharpe, Sortino, Calmar, max drawdown, historical VaR and CVaR. 5) Grid-search parameters only with out-of-sample split / walk-forward. 6) Export trade log, equity curve CSV and chart. 7) State assumptions: lookback, distribution, survivorship.

**المعاملات:** symbol, period, interval, capital, strategy params, confidence level

**التثبيت:** pip install pandas numpy matplotlib

**الوسوم:** backtest · VaR · trading · اختبار رجعي · مخاطر

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:numpy` ← python3 -c "import numpy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:pandas` ← python3 -c "import pandas" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:matplotlib` ← python3 -c "import matplotlib" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1678-trading-strategy-backtester/4683-backtesting-trading-strategies`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3511-quantitative-trading/14277-risk-metrics-calculation`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-12` مراجعة مخاطر ما قبل البناء / Pre-build risk review and kill-test (documented)
- `ASTRAT-13` قرار تخزين البيانات على السلسلة أو خارجها / On-chain versus off-chain data placement (documented)
- `ASTRAT-15` تقييم DCF متين مع فحوص تقاطعية / Defensible DCF valuation with cross-checks (documented)
- `ASTRAT-16` سجل مخاطر مؤسسي مع التقييم / Enterprise risk register with scoring (documented)

### `ASTRAT-15` — تقييم DCF متين مع فحوص تقاطعية / Defensible DCF valuation with cross-checks

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يبني تقييم تدفقات نقدية مخصومة بفترة توقع صريحة وقيمة نهائية بطريقتين وحساسيات. — Build a discounted-cash-flow valuation with explicit projection, both terminal-value methods, WACC build and sensitivities.

**متى:** Pre-investment, M&A diligence, 409A, impairment, board valuation discussion.

**كيف:** 1) Project 5-10 years until steady state (extend if margins/growth still moving). 2) Terminal value both ways: Gordon FCF(N+1)/(WACC-g) and exit EBITDA multiple; compare. 3) Smell test: TV over ~75% of EV means short horizon or high g. 4) Build WACC from comparable betas, risk-free, ERP, size premium. 5) Bridge EV to equity (net debt, minorities, options). 6) Sensitivity grid plus scenario weights; cross-check against trading/precedent multiples.

**المعاملات:** company financials, WACC inputs, g, exit multiple

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** valuation · DCF · تقييم · finance · M&A

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2294-finance/8782-dcf-valuation`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/189-finance-skills/560-financial-analyst`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-13` قرار تخزين البيانات على السلسلة أو خارجها / On-chain versus off-chain data placement (documented)
- `ASTRAT-14` اختبار استراتيجية تداول بمقاييس المخاطر / Backtest trading strategy with risk metrics (documented)
- `ASTRAT-16` سجل مخاطر مؤسسي مع التقييم / Enterprise risk register with scoring (documented)
- `ASTRAT-17` بناء الأعمال ومراجعة طلب التمويل للمؤسسين / Founder business building and fundraising review (documented)

### `ASTRAT-16` — سجل مخاطر مؤسسي مع التقييم / Enterprise risk register with scoring

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يبني سجل مخاطر جاهزاً للتدقيق بصياغة سبب-حدث-أثر وتصنيف وتقييم 5x5. — Build an audit-ready risk register using cause-event-consequence statements, a taxonomy and 5x5 inherent and residual scoring.

**متى:** Requests for risk assessment, risk register, vendor or supplier risk, operational risk.

**كيف:** 1) Name the framework (COSO ERM, ISO 31000). 2) Use 7-9 top-level categories, max 3 levels. 3) Write each risk as In [process] exposed to [event] caused by [driver] leading to [consequence]. 4) Score inherent likelihood x impact 5x5. 5) Map controls and three lines of defense, score residual. 6) Assign owner, mitigation, review date. 7) Add concentration view for single-source suppliers.

**المعاملات:** framework, appetite, categories

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** risk register · ERM · 5x5 · سجل المخاطر · امتثال

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2368-regulatory-compliance/9149-risk-register-build`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-14` اختبار استراتيجية تداول بمقاييس المخاطر / Backtest trading strategy with risk metrics (documented)
- `ASTRAT-15` تقييم DCF متين مع فحوص تقاطعية / Defensible DCF valuation with cross-checks (documented)
- `ASTRAT-17` بناء الأعمال ومراجعة طلب التمويل للمؤسسين / Founder business building and fundraising review (documented)
- `ASTRAT-18` بروتوكول مداولات مجلس إدارة متعدد الأدوار / Multi-role board deliberation protocol (documented)

### `ASTRAT-17` — بناء الأعمال ومراجعة طلب التمويل للمؤسسين / Founder business building and fundraising review

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ينقل الفكرة إلى تموضع مُتحقق وخطة سيولة ومراجعة طلب التمويل وقائمة قانونية للإطلاق. — Take an idea to validated positioning, runway plan, fundraising ask review and launch-legal checklist.

**متى:** Startup planning, runway, pitch review, company architecture.

**كيف:** 1) Diagnose founder fit and edge. 2) Backcast strategy from goals to commitments. 3) Runway and survival scenarios for bootstrapped finance. 4) Review ask and pitch before outreach. 5) List launch legal unknowns for counsel. 6) Optionally scaffold company as structured knowledge bundle.

**المعاملات:** stage, runway

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** startup · founder · ريادة · fundraising

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/139-arquiteto-de-empresa/441-arquiteto-de-empresa`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-15` تقييم DCF متين مع فحوص تقاطعية / Defensible DCF valuation with cross-checks (documented)
- `ASTRAT-16` سجل مخاطر مؤسسي مع التقييم / Enterprise risk register with scoring (documented)
- `ASTRAT-18` بروتوكول مداولات مجلس إدارة متعدد الأدوار / Multi-role board deliberation protocol (documented)
- `ASTRAT-19` تصميم استراتيجية التسعير والربحية / Pricing and monetization strategy design (documented)

### `ASTRAT-18` — بروتوكول مداولات مجلس إدارة متعدد الأدوار / Multi-role board deliberation protocol

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يدير مداولة تنفيذية بمساهمات معزولة ثم نقد وتركيب ومراجعة المؤسس وسجل قرارات. — Run an isolated-contribution C-suite deliberation with critic, synthesis, founder review and decision log.

**متى:** Major strategic decision, board prep, adversarial stress-test.

**كيف:** 1) Load company context and approved decisions only. 2) Chief of staff selects relevant roles by topic. 3) Each role writes max 5 points independently, no cross-reading. 4) Critic pass and synthesis keeping minority views. 5) Founder review. 6) Log approved memo to decisions store; optional multi-model cross-eval.

**المعاملات:** topic, roles

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** board · strategy · قرارات · C-suite

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/138-c-level-skills/409-board-meeting`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-16` سجل مخاطر مؤسسي مع التقييم / Enterprise risk register with scoring (documented)
- `ASTRAT-17` بناء الأعمال ومراجعة طلب التمويل للمؤسسين / Founder business building and fundraising review (documented)
- `ASTRAT-19` تصميم استراتيجية التسعير والربحية / Pricing and monetization strategy design (documented)
- `ASTRAT-20` ميزانية البحث والتطوير والحرق وتوجيه الرسملة / R&D program budget, burn and capitalization routing (documented)

### `ASTRAT-19` — تصميم استراتيجية التسعير والربحية / Pricing and monetization strategy design

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يصمم شرائح التسعير ومقاييس القيمة وخيارات الربحية مع تحليل المنافسين ونية الدفع وتجارب التحقق. — Design pricing tiers, value metrics and monetization options with competitive and willingness-to-pay analysis plus validation experiments.

**متى:** Setting prices, packaging tiers, usage billing, or revenue plans for a business.

**كيف:** 1) Choose pricing model (flat, tiered, usage, freemium). 2) Compare competitor prices and value metric. 3) Estimate willingness to pay. 4) Build 3 tiers; limit choices to cut decision load. 5) List 3-5 monetization options with risk and test. 6) For vertical cases use acuity, dynamic occupancy, tiered-fee blended rate.

**المعاملات:** segment, costs, competitors

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pricing · monetization · تسعير · شرائح · ربحية

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2883-pm-product-strategy/11658-pricing-strategy`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-17` بناء الأعمال ومراجعة طلب التمويل للمؤسسين / Founder business building and fundraising review (documented)
- `ASTRAT-18` بروتوكول مداولات مجلس إدارة متعدد الأدوار / Multi-role board deliberation protocol (documented)
- `ASTRAT-20` ميزانية البحث والتطوير والحرق وتوجيه الرسملة / R&D program budget, burn and capitalization routing (documented)
- `ASTRAT-21` نموذج جدول الملكية وتخفيف الحصص / Startup cap table and dilution model (documented)

### `ASTRAT-20` — ميزانية البحث والتطوير والحرق وتوجيه الرسملة / R&D program budget, burn and capitalization routing

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يعدّ ميزانية برنامج بحث وتطوير ويتتبع الحرق والمدرج مقابل المعالم ويوجّه التكاليف للرسملة أو المصروف. — Budget an R&D program with indirect-cost split, track burn and runway against milestones, and route costs to capitalize or expense review.

**متى:** Managing internal R&D money or asked about IAS 38 vs ASC 730.

**كيف:** 1) Fill work-package line items per period. 2) Apply F&A rate to eligible base (MTDC-style); roll up direct/F&A/loaded. 3) Compute average and trailing burn, runway months, flag below 6-month threshold and accelerating burn. 4) Score cost items against IAS 38 development criteria or flag ASC 730 expense. 5) Route to CAPITALIZE-CANDIDATE / EXPENSE / FINANCE-OWNER-REVIEW; never auto-decide. 6) Ship assumptions with every number.

**المعاملات:** profile, fa-rate, threshold-months, standard ifrs\|usgaap

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** R&D budget · burn rate · IAS 38 · ميزانية · رسملة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/217-research-ops-skills/693-research-finance`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-18` بروتوكول مداولات مجلس إدارة متعدد الأدوار / Multi-role board deliberation protocol (documented)
- `ASTRAT-19` تصميم استراتيجية التسعير والربحية / Pricing and monetization strategy design (documented)
- `ASTRAT-21` نموذج جدول الملكية وتخفيف الحصص / Startup cap table and dilution model (documented)
- `ASTRAT-22` لوحات الاستراتيجية وSWOT وفحص الافتراضات / Strategy canvases, SWOT and red-team (documented)

### `ASTRAT-21` — نموذج جدول الملكية وتخفيف الحصص / Startup cap table and dilution model

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يبني جدول ملكية مخفّفاً بالكامل عبر الجولات وSAFE ويكشف أثر مجمع الخيارات وتراكم SAFE على المؤسسين. — Model a fully diluted cap table through priced rounds and SAFEs, exposing option-pool shuffle and stacked SAFE dilution for founders.

**متى:** Founder asks what a round or SAFE does to ownership.

**كيف:** 1) Start from fully diluted table (founders, options, pool, prior SAFEs). 2) Identify instrument: priced round or SAFE (cap pre/post, discount, MFN). 3) Priced round: investor % = new money / post-money; put required pool top-up in pre-money first. 4) SAFE converts at better of cap price or discounted price. 5) Post-money SAFEs lock holder %, so each later SAFE dilutes founders. 6) Output post-round table with founder dilution delta. 7) Sanity check against typical 15-25% single-round dilution.

**المعاملات:** cap table, round size, pre/post valuation, pool %, SAFE terms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cap table · SAFE · fundraising · جدول الملكية · تمويل

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2386-startup-fundraising/9238-model-cap-table-and-dilution`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2386-startup-fundraising/9237-build-investor-pipeline`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-19` تصميم استراتيجية التسعير والربحية / Pricing and monetization strategy design (documented)
- `ASTRAT-20` ميزانية البحث والتطوير والحرق وتوجيه الرسملة / R&D program budget, burn and capitalization routing (documented)
- `ASTRAT-22` لوحات الاستراتيجية وSWOT وفحص الافتراضات / Strategy canvases, SWOT and red-team (documented)
- `ASTRAT-23` توقع نقدي متدحرج 13 أسبوع / 13-week rolling cash forecast with variance loop (documented)

### `ASTRAT-22` — لوحات الاستراتيجية وSWOT وفحص الافتراضات / Strategy canvases, SWOT and red-team

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ينتج لوحات نموذج العمل وSWOT وتحليل المحيط الأزرق ويختبر افتراضات الاستراتيجية الحرجة. — Produce business model or startup canvases, SWOT and blue-ocean analyses and red-team a strategy's load-bearing assumptions.

**متى:** Strategy framing, business model, lean experiment, or critique of a roadmap.

**كيف:** 1) Fill 9 Business Model Canvas blocks. 2) SWOT with actions per item. 3) Apply Rumelt kernel: diagnosis, guiding policy, coherent actions. 4) Blue ocean: eliminate-reduce-raise-create. 5) Red-team: list assumptions, attack the load-bearing ones. 6) Lean: define MVP, metric, pivot-or-persevere rule.

**المعاملات:** venture, market

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** SWOT · canvas · strategy · استراتيجية · تحليل

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `lean` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-20` ميزانية البحث والتطوير والحرق وتوجيه الرسملة / R&D program budget, burn and capitalization routing (documented)
- `ASTRAT-21` نموذج جدول الملكية وتخفيف الحصص / Startup cap table and dilution model (documented)
- `ASTRAT-23` توقع نقدي متدحرج 13 أسبوع / 13-week rolling cash forecast with variance loop (documented)
- `ASTRAT-24` تقسيم العملاء والمستخدمين حسب القيمة / Customer and user segmentation by value (documented)

### `ASTRAT-23` — توقع نقدي متدحرج 13 أسبوع / 13-week rolling cash forecast with variance loop

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ابن توقعا نقديا أسبوعيا مبنيا على المحركات وتتبع الانحراف وحجم الاحتياطي. — Build driver-based weekly cash receipts and disbursements, track variance, and size buffers against stress.

**متى:** Cash, liquidity or runway questions.

**كيف:** 1) Start from cash position per entity/currency. 2) Direct method for 13 weeks. 3) Receipts from AR aging/DSO; disbursements from AP runs, payroll, tax dates. 4) Weekly forecast vs actual variance by line, retune. 5) Size buffer to a stress case; prefer committed facilities. 6) State resize triggers.

**المعاملات:** ledger exports, DSO, payroll cadence

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cashflow · treasury · نقد

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2399-treasury-management/9289-build-cash-forecast-and-liquidity-plan`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3558-xbert-cashflow-13week/14370-cashflow-13week`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-21` نموذج جدول الملكية وتخفيف الحصص / Startup cap table and dilution model (documented)
- `ASTRAT-22` لوحات الاستراتيجية وSWOT وفحص الافتراضات / Strategy canvases, SWOT and red-team (documented)
- `ASTRAT-24` تقسيم العملاء والمستخدمين حسب القيمة / Customer and user segmentation by value (documented)
- `ASTRAT-25` مواصفة تجربة مع بوابة قرار / Experiment design spec with go/no-go gate (documented)

### `ASTRAT-24` — تقسيم العملاء والمستخدمين حسب القيمة / Customer and user segmentation by value

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** صنف العملاء حسب الإيراد والصحة وتكلفة الخدمة واشتق شخصيات من بيانات متعددة. — Tier customers by revenue, health and cost-to-serve and derive personas from mixed data.

**متى:** Segmentation, CS motion or client profitability tasks.

**كيف:** 1) Gather ARR/revenue, health, support, reviews. 2) Tier by value and expansion potential. 3) Net revenue minus cost-to-serve; find breakeven. 4) Assign motion per tier and capacity (households per advisor). 5) Flag over-capacity risk.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** segmentation · persona · تقسيم

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1567-tonone/4344-keep-segment`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2404-wealth-management-ria/9308-segment-client-profitability`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-22` لوحات الاستراتيجية وSWOT وفحص الافتراضات / Strategy canvases, SWOT and red-team (documented)
- `ASTRAT-23` توقع نقدي متدحرج 13 أسبوع / 13-week rolling cash forecast with variance loop (documented)
- `ASTRAT-25` مواصفة تجربة مع بوابة قرار / Experiment design spec with go/no-go gate (documented)
- `ASTRAT-26` تشخيص تسرب القمع والاحتفاظ / Funnel and retention drop-off diagnosis (documented)

### `ASTRAT-25` — مواصفة تجربة مع بوابة قرار / Experiment design spec with go/no-go gate

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** قرر هل الاختبار مناسب ثم اكتب الفرضية والمقياس الأساسي وحجم العينة وقاعدة القرار. — Decide whether an A/B test is appropriate then write hypothesis, single primary metric, MDE, sample size, runtime and decision rule.

**متى:** Planning a product or growth experiment.

**كيف:** 1) Gate: need ~500+ conversions/week, runtime <=6 weeks, tactical not strategic question; else prescribe qualitative research. 2) Hypothesis: if change then metric moves X because mechanism. 3) One primary metric fixed before start, plus guardrails. 4) Compute sample size from baseline, MDE, alpha, power. 5) Lock stopping rule and kill condition.

**المعاملات:** baseline rate, MDE, alpha, power, weekly traffic

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** experiment · hypothesis · MDE · تجربة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:hypothesis` ← python3 -c "import hypothesis" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1567-tonone/4458-lumen-abtest`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/198-product-skills/633-experiment-designer`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-23` توقع نقدي متدحرج 13 أسبوع / 13-week rolling cash forecast with variance loop (documented)
- `ASTRAT-24` تقسيم العملاء والمستخدمين حسب القيمة / Customer and user segmentation by value (documented)
- `ASTRAT-26` تشخيص تسرب القمع والاحتفاظ / Funnel and retention drop-off diagnosis (documented)
- `ASTRAT-27` هيكلة المقاييس ووثائق التعريف / Metrics architecture and definition docs (documented)

### `ASTRAT-26` — تشخيص تسرب القمع والاحتفاظ / Funnel and retention drop-off diagnosis

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** حدد نقطة التسرب الرئيسية واقترح تدخلا مستهدفا مع شرط الإيقاف. — Locate the primary drop-off in funnel or retention curve and produce a targeted intervention with kill condition.

**متى:** Low conversion, activation or churn questions.

**كيف:** 1) Define events and cohorts. 2) Step conversion and cohort retention curve. 3) Find largest drop and check segment splits. 4) Hypothesis with mechanism (behavior B=MAP). 5) One experiment with baseline, expected lift, kill condition.

**المعاملات:** events, cohort windows

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** funnel · retention · قمع

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1567-tonone/4459-lumen-funnel`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1567-tonone/4350-surge-retention`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-24` تقسيم العملاء والمستخدمين حسب القيمة / Customer and user segmentation by value (documented)
- `ASTRAT-25` مواصفة تجربة مع بوابة قرار / Experiment design spec with go/no-go gate (documented)
- `ASTRAT-27` هيكلة المقاييس ووثائق التعريف / Metrics architecture and definition docs (documented)
- `ASTRAT-28` تحليل الأسباب الجذرية والمخاطر / Root-cause and risk analysis (fishbone, PFMEA, lean) (documented)

### `ASTRAT-27` — هيكلة المقاييس ووثائق التعريف / Metrics architecture and definition docs

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** عرّف مقياس North Star وشجرة المقاييس والصيغ والمصادر وحدود الجيد والسيئ. — Define North Star, input metric tree, formulas, sources, segmentation and good/bad thresholds, plus analytics recon.

**متى:** Starting analytics, auditing tracking or writing a metrics spec.

**كيف:** 1) Recon existing tools/events/dashboards and freshness. 2) North Star + input tree. 3) Per metric: name, formula, source, SQL/event spec, segments, thresholds. 4) Stage-appropriate metric choice (Lean Analytics). 5) Weekly/monthly review with trend and actions.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** metrics · KPI · مقاييس

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `lean` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1567-tonone/4454-lens-metrics`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3433-product-strategy/14094-lean-analytics`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-25` مواصفة تجربة مع بوابة قرار / Experiment design spec with go/no-go gate (documented)
- `ASTRAT-26` تشخيص تسرب القمع والاحتفاظ / Funnel and retention drop-off diagnosis (documented)
- `ASTRAT-28` تحليل الأسباب الجذرية والمخاطر / Root-cause and risk analysis (fishbone, PFMEA, lean) (documented)
- `ASTRAT-29` دراسة الاستعداد للدفع وتغيير الأسعار / Willingness-to-pay and price change planning (documented)

### `ASTRAT-28` — تحليل الأسباب الجذرية والمخاطر / Root-cause and risk analysis (fishbone, PFMEA, lean)

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** اعصف الأسباب بمخطط عظم السمكة وقيّم PFMEA وحدد الهدر والاختناقات. — Brainstorm causes with 6M fishbone, score PFMEA action priority, and find lean wastes and bottlenecks.

**متى:** Quality defects, process improvement, risk review.

**كيف:** 1) Fishbone 6M to list causes before narrowing. 2) PFMEA 7 steps (AIAG-VDA 2019) with Action Priority. 3) Lean 8 wastes DOWNTIME, takt vs cycle time. 4) Identify constraint. 5) Assign actions and verify.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** rca · FMEA · جودة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `lean` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2989-quality-engineering-skills/12668-pfmea-process`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2357-process-improvement/9095-lean-waste-analysis`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-26` تشخيص تسرب القمع والاحتفاظ / Funnel and retention drop-off diagnosis (documented)
- `ASTRAT-27` هيكلة المقاييس ووثائق التعريف / Metrics architecture and definition docs (documented)
- `ASTRAT-29` دراسة الاستعداد للدفع وتغيير الأسعار / Willingness-to-pay and price change planning (documented)
- `ASTRAT-30` قرار البث مقابل الدفعات / Streaming versus batch decision (documented)

### `ASTRAT-29` — دراسة الاستعداد للدفع وتغيير الأسعار / Willingness-to-pay and price change planning

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** اختر منهج دراسة السعر ثم خطط لتغيير السعر مع حماية العملاء الحاليين. — Choose Van Westendorp, Gabor-Granger, conjoint or price A/B, and roll out price changes with grandfathering.

**متى:** Pricing research or price increase.

**كيف:** 1) Method by goal: PSM for ranges, Gabor-Granger for demand curve, conjoint for features, A/B for live. 2) Sample and screen. 3) Cohort-sequenced rollout, renewal timing, grandfathering. 4) Guardrails GRR/churn. 5) Comms plan.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pricing · WTP · تسعير

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2356-pricing-monetization/9092-willingness-to-pay-research`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2356-pricing-monetization/9089-price-change-rollout`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-27` هيكلة المقاييس ووثائق التعريف / Metrics architecture and definition docs (documented)
- `ASTRAT-28` تحليل الأسباب الجذرية والمخاطر / Root-cause and risk analysis (fishbone, PFMEA, lean) (documented)
- `ASTRAT-30` قرار البث مقابل الدفعات / Streaming versus batch decision (documented)
- `ASTRAT-31` اختيار قاعدة بيانات سحابية مناسبة / Cloud database selection and managed-service routing (documented)

### `ASTRAT-30` — قرار البث مقابل الدفعات / Streaming versus batch decision

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يختار البث أو الدفعات حسب الحاجة الفعلية للتأخير ويحدد دلالات التسليم. — Choose streaming or batch from the real latency need and set delivery semantics per hop.

**متى:** Someone proposes real-time without a latency requirement.

**كيف:** 1) Sub-minute reaction -> streaming; hourly/daily -> batch ELT. 2) If streaming: sources -> keyed topics -> processors -> sinks, name delivery semantic at each hop. 3) Platform: Kafka default, Pulsar multi-tenant, Kinesis on AWS. 4) Ingest through CDC/outbox, never dual-writes.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** streaming · batch · Kafka · بث

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2273-data-streaming-engineering/8678-streaming-vs-batch`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2207-majestic-data/8244-data-pipeline-design`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/438-change-data-capture/1467-cdc`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-28` تحليل الأسباب الجذرية والمخاطر / Root-cause and risk analysis (fishbone, PFMEA, lean) (documented)
- `ASTRAT-29` دراسة الاستعداد للدفع وتغيير الأسعار / Willingness-to-pay and price change planning (documented)
- `ASTRAT-31` اختيار قاعدة بيانات سحابية مناسبة / Cloud database selection and managed-service routing (documented)
- `ASTRAT-32` سلسلة خمسة لماذا مع تحقق / 5-Why root cause chain with validation (documented)

### `ASTRAT-31` — اختيار قاعدة بيانات سحابية مناسبة / Cloud database selection and managed-service routing

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** قارن واختر قاعدة البيانات المُدارة المناسبة مع الإعداد والممارسات. — Compare and route to the right managed database (Aurora, Neon, Cosmos, DynamoDB, Firestore) with setup and best practices.

**متى:** Which database should I use, getting started on a cloud DB.

**كيف:** 1) Capture workload: relational vs document vs key-value vs analytics, scale, latency. 2) Compare options in a table. 3) Pick partition keys (Cosmos, DynamoDB single-table). 4) Use branching/serverless where offered (Neon). 5) Lock down security rules and least-privilege users.

**المعاملات:** workload

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cloud · dynamodb · firestore · قاعدة بيانات

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `ASTRAT-29` دراسة الاستعداد للدفع وتغيير الأسعار / Willingness-to-pay and price change planning (documented)
- `ASTRAT-30` قرار البث مقابل الدفعات / Streaming versus batch decision (documented)
- `ASTRAT-32` سلسلة خمسة لماذا مع تحقق / 5-Why root cause chain with validation (documented)
- `ASTRAT-33` دليل حادثة: فرز واحتواء واستعادة ومراجعة / Incident runbook: triage, contain, recover, review (documented)

### `ASTRAT-32` — سلسلة خمسة لماذا مع تحقق / 5-Why root cause chain with validation

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** بناء سلسلة لماذا خطية مدعومة بأدلة والتحقق منها عكسياً قبل اتخاذ إجراء تصحيحي. — Build a linear evidence-backed Why chain, check it by reversal, and validate the systemic root cause before corrective action.

**متى:** quality or incident investigation, CAPA, 8D, recurring failures

**كيف:** 1) Define problem with measured value vs spec. 2) One cause path at a time; each Why needs objective evidence. 3) Reversal check (therefore-reading) for logic and circularity. 4) Stop at systemic cause, not 'human error'. 5) Validate by reproducibility and elimination tests. 6) Link to corrective action; run separate chains for multiple paths.

**المعاملات:** problem statement

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** rca · 5-why · quality · سبب جذري · جودة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2989-quality-engineering-skills/12659-5why-root-cause`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2989-quality-engineering-skills/12645-rca-facilitator`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-30` قرار البث مقابل الدفعات / Streaming versus batch decision (documented)
- `ASTRAT-31` اختيار قاعدة بيانات سحابية مناسبة / Cloud database selection and managed-service routing (documented)
- `ASTRAT-33` دليل حادثة: فرز واحتواء واستعادة ومراجعة / Incident runbook: triage, contain, recover, review (documented)
- `ASTRAT-34` فرز الحادث مقابل المشكلة وتحديد الخطورة / Incident vs problem triage and severity (documented)

### `ASTRAT-33` — دليل حادثة: فرز واحتواء واستعادة ومراجعة / Incident runbook: triage, contain, recover, review

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** شغّل مسار حادثة مرحليًا باحتواء قائم على الدليل واستعادة قابلة للعكس ومراجعة بلا لوم. — Run a staged incident workflow with evidence-led containment, reversible recovery and a blameless postmortem.

**متى:** Outage, auth/spend/data incident, or a failed launch needing review.

**كيف:** 1) Declare severity and owner; open timeline. 2) Triage with evidence, separate observed from conjecture. 3) Contain (feature flag, key rotation only if confirmed, pause jobs). 4) Recover reversibly and verify. 5) Communicate on a cadence. 6) Postmortem: timeline, root cause, contributing factors, action items with owners.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** incident · postmortem · حادثة · runbook

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1819-adobe-pack/4896-adobe-debug-bundle`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/319-engineering/960-incident-response`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3051-adlc-operate/13140-agent-incident-review`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-31` اختيار قاعدة بيانات سحابية مناسبة / Cloud database selection and managed-service routing (documented)
- `ASTRAT-32` سلسلة خمسة لماذا مع تحقق / 5-Why root cause chain with validation (documented)
- `ASTRAT-34` فرز الحادث مقابل المشكلة وتحديد الخطورة / Incident vs problem triage and severity (documented)
- `ASTRAT-35` تحليل السبب الجذري بخمسة لماذا وإيشيكاوا / Root cause analysis with 5 Whys and fishbone (documented)

### `ASTRAT-34` — فرز الحادث مقابل المشكلة وتحديد الخطورة / Incident vs problem triage and severity

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | method paraphrased from Atlas skills under check per-plugin; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يفصل الحوادث عن المشاكل ويحدد الخطورة وأهداف SLO وميزانية الخطأ. — Separates restore-now incidents from remove-cause problems and sets severity, SLOs and error budgets.

**متى:** On alert or report needing classification.

**كيف:** 1) Ask: restore service now (incident) or remove cause (problem). 2) Assign severity by user impact. 3) Roles: commander, comms, ops. 4) Tie to SLI/SLO and error-budget policy. 5) Hand to postmortem.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** incident · SLO · فرز · خطورة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `ASTRAT-32` سلسلة خمسة لماذا مع تحقق / 5-Why root cause chain with validation (documented)
- `ASTRAT-33` دليل حادثة: فرز واحتواء واستعادة ومراجعة / Incident runbook: triage, contain, recover, review (documented)
- `ASTRAT-35` تحليل السبب الجذري بخمسة لماذا وإيشيكاوا / Root cause analysis with 5 Whys and fishbone (documented)
- `ASTRAT-36` إسناد تكلفة استخدام API وضوابط الإنفاق / API usage cost attribution and spend controls (documented)

### `ASTRAT-35` — تحليل السبب الجذري بخمسة لماذا وإيشيكاوا / Root cause analysis with 5 Whys and fishbone

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under check per-plugin; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يثبت السبب الجذري بخمسة لماذا وهيكل السمكة وباريتو مع التحقق بالبيانات. — Proves root cause using 5 Whys, 6M fishbone and Pareto, validated with data before any fix.

**متى:** Recurring defect or post-incident retrospective.

**كيف:** 1) State the problem with a number. 2) Fishbone across 6M (machine, method, material, measurement, people, environment). 3) 5 Whys on each plausible cause. 4) Pareto rank. 5) Proven only when mechanism, data correlation and pilot improvement all hold.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** RCA · fishbone · جذر · تحليل

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2357-process-improvement/9098-root-cause-analysis`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-33` دليل حادثة: فرز واحتواء واستعادة ومراجعة / Incident runbook: triage, contain, recover, review (documented)
- `ASTRAT-34` فرز الحادث مقابل المشكلة وتحديد الخطورة / Incident vs problem triage and severity (documented)
- `ASTRAT-36` إسناد تكلفة استخدام API وضوابط الإنفاق / API usage cost attribution and spend controls (documented)
- `ASTRAT-37` أدلة قرارات معمارية السحابة / Cloud architecture decision playbooks (documented)

### `ASTRAT-36` — إسناد تكلفة استخدام API وضوابط الإنفاق / API usage cost attribution and spend controls

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يقيس استهلاك API والاعتمادات لكل نقطة ويضيف ميزانيات وضوابط بدل أسعار ثابتة. — Measures API/credit/plan usage per endpoint or tenant from live account data and adds budgets and traffic controls instead of hard-coded prices.

**متى:** Asked to reduce spend on an LLM/SaaS API, find waste, or add budget alerts.

**كيف:** 1) Pull current plan/rates from the live account, never freeze prices. 2) Attribute usage by product, endpoint, method, tenant. 3) Find failed calls, duplicate polling, repeated lookups, deep pagination. 4) Add caching, dedupe, admission budgets, model-tier policy. 5) Alert on thresholds; report savings without quality loss.

**المعاملات:** vendor, period

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cost · finops · تكلفة · ميزانية

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1885-mistral-pack/6329-mistral-cost-tuning`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1895-procore-pack/6553-procore-cost-tuning`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1896-quicknode-pack/6577-quicknode-cost-tuning`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-34` فرز الحادث مقابل المشكلة وتحديد الخطورة / Incident vs problem triage and severity (documented)
- `ASTRAT-35` تحليل السبب الجذري بخمسة لماذا وإيشيكاوا / Root cause analysis with 5 Whys and fishbone (documented)
- `ASTRAT-37` أدلة قرارات معمارية السحابة / Cloud architecture decision playbooks (documented)
- `ASTRAT-38` حصاد هدر السحابة وترتيب تسرب التكلفة / Cloud waste harvest and cost leak ranking (documented)

### `ASTRAT-37` — أدلة قرارات معمارية السحابة / Cloud architecture decision playbooks

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يختار الحوسبة والحسابات والتخزين وخيارات التكلفة بحسب شكل الحمل. — Chooses compute, accounts, storage and cost levers from workload shape.

**متى:** Landing zone, compute selection, rightsizing.

**كيف:** 1) Characterize workload. 2) Pick Lambda/Fargate/EC2 or Azure equivalent. 3) Separate accounts by blast radius. 4) Tag costs, budgets, anomaly detection. 5) Scope IAM to resource ARNs.

**المعاملات:** workload

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** aws · azure · architecture · معمارية

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2244-aws-cloud/8528-aws-compute-selection`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2243-azure-cloud/8535-compute-host-selection`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-35` تحليل السبب الجذري بخمسة لماذا وإيشيكاوا / Root cause analysis with 5 Whys and fishbone (documented)
- `ASTRAT-36` إسناد تكلفة استخدام API وضوابط الإنفاق / API usage cost attribution and spend controls (documented)
- `ASTRAT-38` حصاد هدر السحابة وترتيب تسرب التكلفة / Cloud waste harvest and cost leak ranking (documented)
- `ASTRAT-39` تعريف SLI وSLO وميزانية الخطأ / Define SLIs, SLOs and error budgets (documented)

### `ASTRAT-38` — حصاد هدر السحابة وترتيب تسرب التكلفة / Cloud waste harvest and cost leak ranking

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** جرد الموارد الخاملة والمهملة وترتيب الوفورات بالدولار. — Inventory idle, orphaned and oversized resources and rank savings in dollars before discounts.

**متى:** Cost spike or bill review on any cloud or SaaS platform.

**كيف:** 1) Inventory idle instances, orphaned volumes/IPs, oversized, zombie envs. 2) Rank pure-savings by dollars. 3) Harvest before commitments. 4) Confirm no rare-job dependency. 5) For Databricks use system.billing.usage joined to list_prices; label modeled amounts separately. 6) Add unit economics per customer/transaction.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** finops · cost · waste · توفير

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2295-finops-cloud-cost/8801-harvest-waste`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1844-databricks-pack/5461-databricks-cost-leak-hunter`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-36` إسناد تكلفة استخدام API وضوابط الإنفاق / API usage cost attribution and spend controls (documented)
- `ASTRAT-37` أدلة قرارات معمارية السحابة / Cloud architecture decision playbooks (documented)
- `ASTRAT-39` تعريف SLI وSLO وميزانية الخطأ / Define SLIs, SLOs and error budgets (documented)
- `ASTRAT-40` تدقيق خفض التكلفة المبني على الاستخدام / Usage-driven cost tuning audit for SaaS/API spend (documented)

### `ASTRAT-39` — تعريف SLI وSLO وميزانية الخطأ / Define SLIs, SLOs and error budgets

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يعرف المؤشرات والأهداف وتنبيهات الاستهلاك ويربطها باتفاقيات الخدمة. — Define indicators, targets and burn-rate alerts per service and map to customer-facing SLAs.

**متى:** reliability targets, error budget

**كيف:** 1) Pick SLIs: availability, latency percentile, error rate. 2) Set SLO e.g. 99.9% over 30 days. 3) Budget = 1 - SLO. 4) Burn-rate alerts. 5) SLA looser than SLO.

**المعاملات:** service

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** slo · sre · monitoring · موثوقية

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1788-sla-sli-tracker/4808-tracking-service-reliability`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/*/4809-*`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-37` أدلة قرارات معمارية السحابة / Cloud architecture decision playbooks (documented)
- `ASTRAT-38` حصاد هدر السحابة وترتيب تسرب التكلفة / Cloud waste harvest and cost leak ranking (documented)
- `ASTRAT-40` تدقيق خفض التكلفة المبني على الاستخدام / Usage-driven cost tuning audit for SaaS/API spend (documented)
- `ASTRAT-41` خطة اختبار اختراق للذكاء الاصطناعي ومعالجتها / AI red-team plan and remediation (documented)

### `ASTRAT-40` — تدقيق خفض التكلفة المبني على الاستخدام / Usage-driven cost tuning audit for SaaS/API spend

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ينسب الاستخدام للأحمال ويقترح ضوابط تكلفة قابلة للقياس والتراجع دون أسعار مختلقة. — Attributes API/SaaS usage to workloads and proposes measurable, reversible cost controls without invented prices.

**متى:** Bills rising, request or credit overuse, retry storms, caching decisions.

**كيف:** 1) Pull real usage evidence (invoices, dashboards, logs). 2) Attribute volume per workload/retry/cache miss. 3) Rank drivers by share. 4) Propose controls: caching, batching, memory tuning, budgets, alerts. 5) Define baseline and success metric; make each change reversible. Never hard-code plan prices.

**المعاملات:** vendor, usage export

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cost · finops · تكلفة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1821-algolia-pack/4940-algolia-cost-tuning`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1823-apify-pack/5012-apify-cost-tuning`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-38` حصاد هدر السحابة وترتيب تسرب التكلفة / Cloud waste harvest and cost leak ranking (documented)
- `ASTRAT-39` تعريف SLI وSLO وميزانية الخطأ / Define SLIs, SLOs and error budgets (documented)
- `ASTRAT-41` خطة اختبار اختراق للذكاء الاصطناعي ومعالجتها / AI red-team plan and remediation (documented)
- `ASTRAT-42` سلم توجيه النماذج حسب التكلفة / Cost-per-task model routing ladder (documented)

### `ASTRAT-41` — خطة اختبار اختراق للذكاء الاصطناعي ومعالجتها / AI red-team plan and remediation

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT/Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** نمذجة تهديدات نظام ذكاء اصطناعي وترتيب مخاطر OWASP LLM ثم معالجة متعددة الطبقات. — Threat-model an AI system, prioritise OWASP LLM risks, then drive layered remediation.

**متى:** Launching an LLM feature with tools or RAG; triaging jailbreak findings.

**كيف:** 1) Characterise system: inputs, tools, data reach. 2) Threat-model assets x attackers x abuse cases. 3) Split safety from security. 4) Walk taxonomy: indirect injection, excessive agency, disclosure, prompt leak. 5) Rank P0-P2 by likelihood x impact. 6) Rules of engagement, kill-switch. 7) Remediate with input/output guards and least privilege.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** red-team · owasp-llm · security · اختبار-اختراق · أمان

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2232-ai-red-teaming/8480-design-ai-redteam-plan`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2232-ai-red-teaming/8481-harden-and-remediate-ai-system`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1823-anthropic-pack/4999-anth-policy-guardrails`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-39` تعريف SLI وSLO وميزانية الخطأ / Define SLIs, SLOs and error budgets (documented)
- `ASTRAT-40` تدقيق خفض التكلفة المبني على الاستخدام / Usage-driven cost tuning audit for SaaS/API spend (documented)
- `ASTRAT-42` سلم توجيه النماذج حسب التكلفة / Cost-per-task model routing ladder (documented)
- `ASTRAT-43` جاهزية قانون الذكاء الأوروبي وفحص التحيز / EU AI Act readiness and bias check (documented)

### `ASTRAT-42` — سلم توجيه النماذج حسب التكلفة / Cost-per-task model routing ladder

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT/Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** توجيه الطلبات لأرخص نموذج كافٍ بمصنف فرز وتصعيد عند عدم اليقين. — Route requests to the cheapest adequate model via a triage classifier with escalation.

**متى:** Spend is high, Opus-for-everything policy, or mixed latency needs.

**كيف:** 1) Define simple/medium/complex tiers per domain. 2) Cheap-model triage call returning only a tier label; cache by request hash. 3) Handlers per tier; escalate on uncertainty signals. 4) Track cost-per-resolved-task, not per call. 5) Compare vendors with a task-shape cost table and set budget alerts.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** routing · cost · model-selection · توجيه · نماذج

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2254-claude-app-engineering/8583-llm-routing-ladder`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3051-adlc-operate/13142-ai-cost-management`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2230-ai-coding-model-guidance/8472-multi-tool-model-comparison`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-40` تدقيق خفض التكلفة المبني على الاستخدام / Usage-driven cost tuning audit for SaaS/API spend (documented)
- `ASTRAT-41` خطة اختبار اختراق للذكاء الاصطناعي ومعالجتها / AI red-team plan and remediation (documented)
- `ASTRAT-43` جاهزية قانون الذكاء الأوروبي وفحص التحيز / EU AI Act readiness and bias check (documented)
- `ASTRAT-44` تدقيق تكلفة LLM والتوجيه / LLM cost audit and routing (documented)

### `ASTRAT-43` — جاهزية قانون الذكاء الأوروبي وفحص التحيز / EU AI Act readiness and bias check

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT/Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تصنيف نظام ذكاء اصطناعي حسب فئة مخاطر القانون الأوروبي والتحقق من العدالة. — Classify an AI system by EU AI Act risk tier and validate fairness metrics.

**متى:** Compliance review before launching an AI feature.

**كيف:** 1) Ask forcing questions on use case. 2) Classify prohibited/high-risk/limited. 3) List Article obligations. 4) Compute fairness metrics across groups. 5) Document gaps and owners.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** compliance · eu-ai-act · fairness · امتثال · عدالة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/148-compliance-os/483-ai-act-readiness`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/215-compliance-team-eu-ai-act/688-eu-ai-act-specialist`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1569-ai-ethics-validator/4540-validating-ai-ethics-and-fairness`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-41` خطة اختبار اختراق للذكاء الاصطناعي ومعالجتها / AI red-team plan and remediation (documented)
- `ASTRAT-42` سلم توجيه النماذج حسب التكلفة / Cost-per-task model routing ladder (documented)
- `ASTRAT-44` تدقيق تكلفة LLM والتوجيه / LLM cost audit and routing (documented)
- `ASTRAT-45` مراجعة برنامج مكافحة غسل الأموال / AML program review against FATF/FFIEC (documented)

### `ASTRAT-44` — تدقيق تكلفة LLM والتوجيه / LLM cost audit and routing

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** خفض تكلفة LLM عبر تسجيل التكلفة وتوزيع النماذج على طبقات والتخزين المؤقت وضغط الرموز. — Cut LLM spend 40-80% by logging per-request cost, tiering models, caching and compressing tokens.

**متى:** Costs are high, an AI feature is launching, or model choice is open.

**كيف:** 1) Classify mode: audit, optimize, or design. 2) Log model, in/out tokens, latency, feature, cost per request. 3) Find top endpoints by feature x model x tokens. 4) Route simple/medium/complex tasks to small/mid/large tiers. 5) Add prompt caching and compression. 6) Monitor continuously; logging comes before optimization.

**المعاملات:** target cut; quality floor

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cost · routing · caching · تكلفة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/176-llm-cost-optimizer/545-llm-cost-optimizer`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-42` سلم توجيه النماذج حسب التكلفة / Cost-per-task model routing ladder (documented)
- `ASTRAT-43` جاهزية قانون الذكاء الأوروبي وفحص التحيز / EU AI Act readiness and bias check (documented)
- `ASTRAT-45` مراجعة برنامج مكافحة غسل الأموال / AML program review against FATF/FFIEC (documented)
- `ASTRAT-46` تشخيص هامش الربح ومزيج الخدمات / Small-business margin and mix diagnostics (documented)

### `ASTRAT-45` — مراجعة برنامج مكافحة غسل الأموال / AML program review against FATF/FFIEC

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** مراجعة برنامج AML عبر الركائز الخمس بمستويات التصميم والتنفيذ والفعالية. — Review an AML program across five pillars at design, implementation and effectiveness levels.

**متى:** Audit of AML/KYC controls or regulator readiness.

**كيف:** 1) Check five pillars: AML officer, policies/controls, training, independent testing, CDD/beneficial ownership. 2) For each pillar assess design, implementation, effectiveness separately. 3) List findings by frequency with primary-source citations. 4) Structured report with remediation.

**المعاملات:** pillar docs, jurisdiction

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** AML · KYC · audit · غسل الأموال

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2368-regulatory-compliance/9142-aml-program-review`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-43` جاهزية قانون الذكاء الأوروبي وفحص التحيز / EU AI Act readiness and bias check (documented)
- `ASTRAT-44` تدقيق تكلفة LLM والتوجيه / LLM cost audit and routing (documented)
- `ASTRAT-46` تشخيص هامش الربح ومزيج الخدمات / Small-business margin and mix diagnostics (documented)
- `ASTRAT-47` مراجعة التصميم بالقواعد الإرشادية / Design review heuristics and critique (documented)

### `ASTRAT-46` — تشخيص هامش الربح ومزيج الخدمات / Small-business margin and mix diagnostics

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** قراءة الهامش لكل ساعة وسلة المبيعات وسعة التشغيل لأنشطة خدمية. — Read margin per provider-hour, basket, attach and capacity for retail, spa, funeral, pharmacy operations.

**متى:** Owner asks to lift profit in a regulated local business.

**كيف:** 1) Compute revenue and margin per service or room hour. 2) Tilt mix to high contribution. 3) Model device payback on realistic volume. 4) Find gating stage in case pipeline and size staffing. 5) Route clinical judgment to professionals.

**المعاملات:** sales by category

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** margin · operations · spa · هامش

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2333-med-spa-aesthetics/8957-service-mix-injectables-devices-memberships`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2378-salon-spa-operations/9203-retail-attach-and-service-mix`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-44` تدقيق تكلفة LLM والتوجيه / LLM cost audit and routing (documented)
- `ASTRAT-45` مراجعة برنامج مكافحة غسل الأموال / AML program review against FATF/FFIEC (documented)
- `ASTRAT-47` مراجعة التصميم بالقواعد الإرشادية / Design review heuristics and critique (documented)
- `ASTRAT-48` جولة موازنة اقتصاد اللعبة / Game balance and economy tuning pass (documented)

### `ASTRAT-47` — مراجعة التصميم بالقواعد الإرشادية / Design review heuristics and critique

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** إجراء تقييم إرشادي ونقد منظم للتصميم مع نتائج مرتبة الأولوية. — Run a structured heuristic evaluation and design critique with prioritized findings.

**متى:** Design review, UX evaluation, handoff readiness, iOS HIG compliance.

**كيف:** 1) State goals and audience. 2) Walk Nielsen-style heuristics per screen. 3) Log issues with severity and evidence. 4) Check platform guidelines (iOS HIG). 5) Give prioritized fixes and handoff notes.

**المعاملات:** design files or screenshots

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** heuristics · critique · نقد التصميم · ux

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3011-uxd-research/12863-uxd-evaluate-design-heuristics`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1529-uxdesign/4182-design-critique`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-45` مراجعة برنامج مكافحة غسل الأموال / AML program review against FATF/FFIEC (documented)
- `ASTRAT-46` تشخيص هامش الربح ومزيج الخدمات / Small-business margin and mix diagnostics (documented)
- `ASTRAT-48` جولة موازنة اقتصاد اللعبة / Game balance and economy tuning pass (documented)
- `ASTRAT-49` تصميم الآليات وتجربة اللاعب / Game mechanics and player experience design (documented)

### `ASTRAT-48` — جولة موازنة اقتصاد اللعبة / Game balance and economy tuning pass

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تحديد التجربة المقصودة ورسم الاقتصاد وحساب القيمة المتوقعة وجدول ضبط. — Define intended experience, map sources and sinks, compute expected value and output a tuning table with safe ranges.

**متى:** Tuning difficulty, loot, rewards, progression.

**كيف:** 1) State target feel. 2) Map currencies, sources, sinks, gates. 3) Hunt dominant strategies and runaway feedback. 4) Run expected_value.py --outcome value:prob. 5) Output Balance Intent, Economy Map, Tuning Table, Risk Review, Validation Plan. 6) Confirm with playtest.

**المعاملات:** outcomes

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** balance · economy · موازنة · اقتصاد

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2199-lvtd-skills/8078-game-balance-economy`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-46` تشخيص هامش الربح ومزيج الخدمات / Small-business margin and mix diagnostics (documented)
- `ASTRAT-47` مراجعة التصميم بالقواعد الإرشادية / Design review heuristics and critique (documented)
- `ASTRAT-49` تصميم الآليات وتجربة اللاعب / Game mechanics and player experience design (documented)
- `ASTRAT-50` تصنيف مؤشرات DORA الأربعة / DORA four keys classification (documented)

### `ASTRAT-49` — تصميم الآليات وتجربة اللاعب / Game mechanics and player experience design

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تصميم حلقات اللعب والقواعد ونماذج دافعية اللاعب. — Design core loops, rules and player motivation models with interest curves.

**متى:** Starting or repairing a game design.

**كيف:** 1) Define target player, motivations, flow. 2) Specify goal, actions, state, chance, secrets. 3) Check emergent dynamics. 4) Plot interest curve. 5) Plan small slice.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** design · mechanics · تصميم · لاعب

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2199-lvtd-skills/8082-game-mechanics-design`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2199-lvtd-skills/8139-player-experience-modeling`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-47` مراجعة التصميم بالقواعد الإرشادية / Design review heuristics and critique (documented)
- `ASTRAT-48` جولة موازنة اقتصاد اللعبة / Game balance and economy tuning pass (documented)
- `ASTRAT-50` تصنيف مؤشرات DORA الأربعة / DORA four keys classification (documented)
- `ASTRAT-51` قراءة المؤشرات التشغيلية الصناعية / Frequency vs severity operating metrics (documented)

### `ASTRAT-50` — تصنيف مؤشرات DORA الأربعة / DORA four keys classification

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحسب مؤشرات DORA ويصنفها مع نافذة وخط أساس. — Compute deploy frequency, lead time, change-failure rate and MTTR, classify to bands with windows and baselines.

**متى:** Developer-experience or delivery performance measurement.

**كيف:** 1) Pull four keys over a fixed window. 2) Classify elite/high/medium/low via a calc script. 3) Attach window and prior baseline or do not ship. 4) Name the weakest key as binding constraint, paired with survey signal.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** dora · metrics · مقاييس · devex

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2353-platform-engineering-idp/9055-classify-dora`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-48` جولة موازنة اقتصاد اللعبة / Game balance and economy tuning pass (documented)
- `ASTRAT-49` تصميم الآليات وتجربة اللاعب / Game mechanics and player experience design (documented)
- `ASTRAT-51` قراءة المؤشرات التشغيلية الصناعية / Frequency vs severity operating metrics (documented)
- `ASTRAT-52` تفكيك المتطلبات لمهام قابلة للتنفيذ / Task breakdown with sizing rules (documented)

### `ASTRAT-51` — قراءة المؤشرات التشغيلية الصناعية / Frequency vs severity operating metrics

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** قراءات مؤشرات مجالية مع خط أساس. — Domain-specific metric reads (utilization, LTV:CAC, absorption, DORA, NDCG) with baselines.

**متى:** Business-metric diagnosis questions.

**كيف:** 1) Name the metric and formula. 2) Use a fixed window plus baseline. 3) Segment, never blended. 4) Compare to threshold (e.g. LTV:CAC 3:1, collection 98%). 5) Name the binding lever.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** metrics · kpi · مؤشرات · analysis

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `ASTRAT-49` تصميم الآليات وتجربة اللاعب / Game mechanics and player experience design (documented)
- `ASTRAT-50` تصنيف مؤشرات DORA الأربعة / DORA four keys classification (documented)
- `ASTRAT-52` تفكيك المتطلبات لمهام قابلة للتنفيذ / Task breakdown with sizing rules (documented)
- `ASTRAT-53` إصدار أمني منسق / Coordinated security release (documented)

### `ASTRAT-52` — تفكيك المتطلبات لمهام قابلة للتنفيذ / Task breakdown with sizing rules

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يفكك المتطلبات إلى مهام صغيرة مع تبعيات ومخاطر. — Split requirements into SMART tasks capped at two days, with serial/parallel/blocking dependencies and risk handling.

**متى:** Planning work, estimating effort, assessing project risk.

**كيف:** 1) Break via WBS to SMART tasks. 2) Size: small 2-4h, medium 1-2d, large 3-5d; split anything over 2 days. 3) Mark dependencies serial/parallel/blocking and do blockers first. 4) List risks with mitigation. 5) Detect tech stack from config files first.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** wbs · planning · تخطيط · estimation

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1369-boss/3168-scrum-master-task-breakdown`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-50` تصنيف مؤشرات DORA الأربعة / DORA four keys classification (documented)
- `ASTRAT-51` قراءة المؤشرات التشغيلية الصناعية / Frequency vs severity operating metrics (documented)
- `ASTRAT-53` إصدار أمني منسق / Coordinated security release (documented)
- `ASTRAT-54` بطاقات أنكي عبر AnkiConnect / Anki flashcards via AnkiConnect (documented)

### `ASTRAT-53` — إصدار أمني منسق / Coordinated security release

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تنفيذ إصدار ترقيع أمني بشكل خاص مع إفصاح منسق. — Run a private-fix coordinated disclosure release for a reported vulnerability.

**متى:** Private vulnerability report, GHSA, CVE.

**كيف:** 1) Private advisory/branch, no public traces. 2) Fix and test privately. 3) Request CVE via GHSA. 4) Backport to supported lines. 5) Release patch and publish advisory same time. 6) Notify downstream.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** security · advisory · ثغرة

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2346-open-source-maintenance/9023-coordinate-a-security-release`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2346-open-source-maintenance/9025-plan-a-release`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-51` قراءة المؤشرات التشغيلية الصناعية / Frequency vs severity operating metrics (documented)
- `ASTRAT-52` تفكيك المتطلبات لمهام قابلة للتنفيذ / Task breakdown with sizing rules (documented)
- `ASTRAT-54` بطاقات أنكي عبر AnkiConnect / Anki flashcards via AnkiConnect (documented)
- `ASTRAT-55` إعداد دورة Google Classroom والطلاب / Google Classroom course setup and roster (documented)

### `ASTRAT-54` — بطاقات أنكي عبر AnkiConnect / Anki flashcards via AnkiConnect

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ينشئ ويدير مجموعات وبطاقات أنكي عبر واجهة AnkiConnect المحلية. — Create and manage Anki decks and cards through the local AnkiConnect HTTP API.

**متى:** User wants flashcards, spaced repetition decks or Anki card changes.

**كيف:** 1) Anki must be running with AnkiConnect (add-on 2055492159). 2) Check: curl -s localhost:8765 -X POST -d '{"action":"requestPermission","version":6}' expects granted. 3) Create decks and add notes with JSON actions. 4) Keep one atomic fact per card. 5) On macOS disable App Nap.

**المعاملات:** deck, note model

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** anki · flashcards · spaced repetition · بطاقات

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `os:macos` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `network` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1217-anki-flashcards/2899-anki-flashcards`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1390-core-learning/3276-learn-core`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-52` تفكيك المتطلبات لمهام قابلة للتنفيذ / Task breakdown with sizing rules (documented)
- `ASTRAT-53` إصدار أمني منسق / Coordinated security release (documented)
- `ASTRAT-55` إعداد دورة Google Classroom والطلاب / Google Classroom course setup and roster (documented)
- `ASTRAT-56` مدرب تعلم متعدد الجلسات بحالة محفوظة / Multi-session learning coach with persistent state (documented)

### `ASTRAT-55` — إعداد دورة Google Classroom والطلاب / Google Classroom course setup and roster

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ينشئ الفصول ويدعو الطلاب ويدير الواجبات عبر أداة gws. — Create classes, invite students and manage coursework through the gws CLI.

**متى:** User manages classes or coursework in Google Classroom.

**كيف:** 1) Use gws classroom commands. 2) Create the course. 3) Invite students. 4) Manage coursework.

**المعاملات:** course name

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** classroom · LMS · فصل · طلاب

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2907-google-workspace/11852-recipe-create-classroom-course`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2907-google-workspace/11797-gws-classroom`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-53` إصدار أمني منسق / Coordinated security release (documented)
- `ASTRAT-54` بطاقات أنكي عبر AnkiConnect / Anki flashcards via AnkiConnect (documented)
- `ASTRAT-56` مدرب تعلم متعدد الجلسات بحالة محفوظة / Multi-session learning coach with persistent state (documented)
- `ASTRAT-57` بروتوكول تدريس سقراطي سؤال واحد كل مرة / Socratic one-question-at-a-time tutoring protocol (documented)

### `ASTRAT-56` — مدرب تعلم متعدد الجلسات بحالة محفوظة / Multi-session learning coach with persistent state

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يدرّب المتعلم عبر جلسات متعددة بملفات هدف ومسرد وسجل تعلم تراكمي. — Coach a learner over several sessions using a mission file, glossary, concept slices and an append-only learning log.

**متى:** User says teach me, study session, onboard me to a topic or codebase.

**كيف:** 1) Write MISSION.md (goal, success criteria, constraints). 2) Create per-concept folders with lesson, reference.md and exercise.md. 3) Progress through Knowledge-Skills-Wisdom stages. 4) Add glossary terms only after the learner shows understanding. 5) Append numbered ADR-style learning records. 6) On resume, read state first. Topic mode uses external sources; codebase mode uses repo docs.

**المعاملات:** topic\|codebase, workspace root

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** tutoring · teach · تعليم · تدريس

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2437-education/9463-teach`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1390-core-learning/3276-learn-core`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-54` بطاقات أنكي عبر AnkiConnect / Anki flashcards via AnkiConnect (documented)
- `ASTRAT-55` إعداد دورة Google Classroom والطلاب / Google Classroom course setup and roster (documented)
- `ASTRAT-57` بروتوكول تدريس سقراطي سؤال واحد كل مرة / Socratic one-question-at-a-time tutoring protocol (documented)
- `ASTRAT-58` الوظائف المطلوب إنجازها بأبعادها الثلاثة / Jobs to Be Done with all three dimensions (documented)

### `ASTRAT-57` — بروتوكول تدريس سقراطي سؤال واحد كل مرة / Socratic one-question-at-a-time tutoring protocol

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يدير حلقة تدريس بسؤال واحد وتلميحات عند الخطأ ويحكم بالإتقان عبر التطبيق المستقل. — Run a tutor loop with one pending question, hints on errors and mastery judged by independent application.

**متى:** Learner wants to master a skill or concept, not just receive an explanation.

**كيف:** 1) State a mode contract each session. 2) Give brief concept plus one question, then stop and wait. 3) On a wrong answer give a minimal hint only, then retry. 4) Follow with a new-conditions question and ask for reasoning. 5) Record untested, hinted, independent, transfer, delayed-recheck. 6) Never simulate the learner's answers. Modes: Socratic, reverse-teach (Feynman), drill, project review, spaced quiz.

**المعاملات:** mode, time budget

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** socratic · tutor · سقراطي · تعلم

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1390-core-learning/3276-learn-core`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1097-akbun-learning/2467-akbun-algorithm-tutor`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-55` إعداد دورة Google Classroom والطلاب / Google Classroom course setup and roster (documented)
- `ASTRAT-56` مدرب تعلم متعدد الجلسات بحالة محفوظة / Multi-session learning coach with persistent state (documented)
- `ASTRAT-58` الوظائف المطلوب إنجازها بأبعادها الثلاثة / Jobs to Be Done with all three dimensions (documented)
- `ASTRAT-59` التموضع: السياق قبل الرسالة / Positioning as context (Obviously Awesome canvas) (documented)

### `ASTRAT-58` — الوظائف المطلوب إنجازها بأبعادها الثلاثة / Jobs to Be Done with all three dimensions

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يفهم سبب «توظيف» العميل للمنتج: التقدم الذي يريده في ظرف معين، وظيفياً وعاطفياً واجتماعياً. — Understands why a customer 'hires' a product: the progress wanted in a circumstance, functional, emotional and social.

**متى:** لماذا يشتري العميل، احتياج العميل، JTBD / why customers buy, jobs to be done, customer needs

**كيف:** 1) Define the job as progress in specific circumstances, not a goal or a solution; demographics do not define it. 2) Capture all three dimensions: functional (what to get done), emotional (how to feel), social (how to be seen). 3) Map hiring and firing: what they used before and why they switched. 4) Interview about past behaviour, not opinions about your idea (Mom Test). 5) Score seven diagnostic rows plus depth points.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** JTBD · customer · عميل · product · منتج · needs

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3433-product-strategy/14093-jobs-to-be-done`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-56` مدرب تعلم متعدد الجلسات بحالة محفوظة / Multi-session learning coach with persistent state (documented)
- `ASTRAT-57` بروتوكول تدريس سقراطي سؤال واحد كل مرة / Socratic one-question-at-a-time tutoring protocol (documented)
- `ASTRAT-59` التموضع: السياق قبل الرسالة / Positioning as context (Obviously Awesome canvas) (documented)
- `ASTRAT-60` تحسين التحويل: اكتشف ولا تخمّن / Conversion optimisation: discover, do not guess (documented)

### `ASTRAT-59` — التموضع: السياق قبل الرسالة / Positioning as context (Obviously Awesome canvas)

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحدد الفئة والبدائل والصفات الفريدة والقيمة والعميل الأنسب قبل كتابة أي رسالة تسويقية. — Defines category, alternatives, unique attributes, value and best-fit customer before writing any marketing message.

**متى:** تموضع المنتج، كيف نميز منتجنا، المنافسين / product positioning, differentiation, competitors

**كيف:** 1) List the real competitive alternatives customers would use instead (including spreadsheets or doing nothing). 2) Extract attributes only you have. 3) Translate attributes into value with proof. 4) Identify who cares most about that value. 5) Choose the market category that makes the value obvious. 6) Only then write messaging. 7) Score 0-10: 7-8 when all components are defined and the team agrees.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** positioning · تموضع · marketing · تسويق · competitors

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-59` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3435-strategy-growth/14106-obviously-awesome`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-57` بروتوكول تدريس سقراطي سؤال واحد كل مرة / Socratic one-question-at-a-time tutoring protocol (documented)
- `ASTRAT-58` الوظائف المطلوب إنجازها بأبعادها الثلاثة / Jobs to Be Done with all three dimensions (documented)
- `ASTRAT-60` تحسين التحويل: اكتشف ولا تخمّن / Conversion optimisation: discover, do not guess (documented)
- `ASTRAT-61` تحسين الظهور في البحث ومحركات الإجابة والذكاء التوليدي / SEO, answer-engine and generative-engine visibility (documented)

### `ASTRAT-60` — تحسين التحويل: اكتشف ولا تخمّن / Conversion optimisation: discover, do not guess

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يبحث عن أسباب عدم تحويل الزوار (من هم، ما الذي يعيقهم، ما اعتراضاتهم) قبل أي اختبار A/B. — Researches why visitors do not convert (who they are, what blocks them, what objections stop them) before any A/B test.

**متى:** الصفحة لا تبيع، تحسين التحويل، صفحة هبوط / landing page not converting, CRO, A/B test

**كيف:** 1) Define the success metric tied to business KPIs first. 2) Map the funnel to find high-traffic underperforming paths and missing stages. 3) Research visitors on three axes: who they are, UX blockers, objections (surveys, recordings, analytics). 4) Turn findings into hypotheses, prioritise, and test one change at a time with enough traffic. 5) Scale wins across pages; record losses too.

**المعاملات:** metric

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** CRO · conversion · تحويل · landing page · A/B

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-60` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3430-marketing-cro/14069-cro-methodology`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-58` الوظائف المطلوب إنجازها بأبعادها الثلاثة / Jobs to Be Done with all three dimensions (documented)
- `ASTRAT-59` التموضع: السياق قبل الرسالة / Positioning as context (Obviously Awesome canvas) (documented)
- `ASTRAT-61` تحسين الظهور في البحث ومحركات الإجابة والذكاء التوليدي / SEO, answer-engine and generative-engine visibility (documented)
- `ASTRAT-62` مراجعة تصميم بأسلوب الطرح حتى الجوهر / Subtractive design review from the customer backwards (documented)

### `ASTRAT-61` — تحسين الظهور في البحث ومحركات الإجابة والذكاء التوليدي / SEO, answer-engine and generative-engine visibility

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحسّن ظهور المحتوى في محركات البحث وفي إجابات المساعدات الذكية، مستنداً إلى أبحاث حديثة لا إلى الموروث. — Improves visibility in search engines and AI assistant answers, grounded in current research rather than folklore.

**متى:** سيو، الظهور في جوجل، الظهور في إجابات الذكاء الاصطناعي / SEO, AEO, GEO, AI search visibility

**كيف:** 1) Pull current research first; treat vendor-blog insights as lower trust than the durable model and weigh each on provenance. 2) Write answer-first sections that state the fact in the first sentence, with clear headings matching real questions. 3) Use structured data and clean entities so engines can cite you. 4) Earn mentions on sources assistants already cite. 5) Measure with search console data and citation checks, not guesses.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** SEO · سيو · AEO · GEO · search · بحث

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-61` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/99-seo-aeo-geo/208-seo-aeo-geo`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-59` التموضع: السياق قبل الرسالة / Positioning as context (Obviously Awesome canvas) (documented)
- `ASTRAT-60` تحسين التحويل: اكتشف ولا تخمّن / Conversion optimisation: discover, do not guess (documented)
- `ASTRAT-62` مراجعة تصميم بأسلوب الطرح حتى الجوهر / Subtractive design review from the customer backwards (documented)
- `ASTRAT-63` مقابلة سؤال-بسؤال لاستخراج النية الحقيقية قبل البناء / One-question interview to extract real intent (documented)

### `ASTRAT-62` — مراجعة تصميم بأسلوب الطرح حتى الجوهر / Subtractive design review from the customer backwards

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يراجع المنتج من تجربة العميل إلى التقنية، ويحذف حتى يصبح الحذف التالي كاسراً للمنتج. — Reviews a product from the customer experience back to the technology, subtracting until one more removal would break it.

**متى:** راجع تصميم منتجي، بسّط المنتج / design review, simplify product, product critique

**كيف:** 1) Start from what the customer sees, feels and does, then work back to the technology. 2) Remove elements until removing one more breaks the product; prefer one good default over a setting. 3) Count steps to value and cut them. 4) If it needs explaining, redesign it. 5) Score seven diagnostic rows: 7/7 = 10, 6/7 = 9, 5/7 = 7, 4/7 = 6.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** design review · مراجعة تصميم · simplicity · بساطة · product

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-62` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3438-ux-design/14123-steve-jobs-design-review`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-60` تحسين التحويل: اكتشف ولا تخمّن / Conversion optimisation: discover, do not guess (documented)
- `ASTRAT-61` تحسين الظهور في البحث ومحركات الإجابة والذكاء التوليدي / SEO, answer-engine and generative-engine visibility (documented)
- `ASTRAT-63` مقابلة سؤال-بسؤال لاستخراج النية الحقيقية قبل البناء / One-question interview to extract real intent (documented)
- `ASTRAT-64` خطاب تقديم وظيفي مفصّل على الإعلان بلا عبارات آلية / Tailored cover letter without AI tells (documented)

### `ASTRAT-63` — مقابلة سؤال-بسؤال لاستخراج النية الحقيقية قبل البناء / One-question interview to extract real intent

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يكشف ما يريده المستخدم فعلًا لا ما يظن أنه ينبغي أن يريده، بسؤال واحد في كل مرة مع تخمين مرفق حتى ثقة ~95%. — Surfaces what the user actually wants rather than what they think they should want, one question at a time with an attached guess, until ~95% confidence.

**متى:** طلب ناقص (من؟ لماذا الآن؟ ما النجاح؟)، أو 'اسألني'، قبل أي خطة أو كود / an underspecified ask, 'interview me', before any plan or code

**كيف:** 1) Write a one-sentence hypothesis with an honest confidence number and what is missing. 2) Ask one focused question, each with your GUESS and its reasoning; wait for the reaction. 3) Watch for 'should want' answers (buzzwords, 'the standard way') and ask: if you did not have to justify it, what would you want? 4) Restate as Outcome, User, Why now, Success, Constraint, Out of scope. 5) Accept only an explicit yes; 'whatever you think' means re-ask as two concrete options. 6) Stop when you can predict the reactions to the next three questions; if several rounds still fail, say something foundational is missing. Never run it in non-interactive contexts.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** requirements · intent · interview · استيضاح · متطلبات · clarifying questions

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-63` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3225-interview-me/13638-interview-me`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-61` تحسين الظهور في البحث ومحركات الإجابة والذكاء التوليدي / SEO, answer-engine and generative-engine visibility (documented)
- `ASTRAT-62` مراجعة تصميم بأسلوب الطرح حتى الجوهر / Subtractive design review from the customer backwards (documented)
- `ASTRAT-64` خطاب تقديم وظيفي مفصّل على الإعلان بلا عبارات آلية / Tailored cover letter without AI tells (documented)
- `ASTRAT-65` التفاوض بالتعاطف التكتيكي والأسئلة المعايَرة / Negotiation with tactical empathy and calibrated questions (documented)

### `ASTRAT-64` — خطاب تقديم وظيفي مفصّل على الإعلان بلا عبارات آلية / Tailored cover letter without AI tells

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يكتب خطاب تقديم من السيرة الذاتية مطابقًا لإعلان الوظيفة وثقافة الشركة، بنثر مباشر وادعاءات قابلة للتتبع. — Writes a cover letter from the CV matched to the job posting and company culture, in direct prose with traceable claims.

**متى:** التقديم على وظيفة، خطاب تقديم، رسالة لينكدإن قصيرة / applying for a job, cover letter, short LinkedIn note

**كيف:** 1) Intake: get the CV and the full job description in one message; extract text from PDF/LaTeX if given. 2) Read the company's tone, values page and repeated keywords. 3) Map must-haves and nice-to-haves to 2-3 strongest matching outcomes with numbers; bridge gaps honestly, never invent. 4) Standard: 4 paragraphs, 250-380 words, open with the strongest result (not 'I am excited'), one concrete company-specific paragraph, short close. LinkedIn: 100-150 plain words. 5) Ban stock phrases, triads of adjectives, 'not only X but also Y', uniform sentence length. 6) Grammar and authenticity pass, then save as YYYY-MM-DD-company-role.md for the user to review before sending.

**المعاملات:** channel: standard\|linkedin

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cover letter · job application · خطاب تقديم · وظيفة · سيرة ذاتية · career

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `latex` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-64` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3410-career-tools/13964-cover-letter-builder`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-62` مراجعة تصميم بأسلوب الطرح حتى الجوهر / Subtractive design review from the customer backwards (documented)
- `ASTRAT-63` مقابلة سؤال-بسؤال لاستخراج النية الحقيقية قبل البناء / One-question interview to extract real intent (documented)
- `ASTRAT-65` التفاوض بالتعاطف التكتيكي والأسئلة المعايَرة / Negotiation with tactical empathy and calibrated questions (documented)
- `ASTRAT-66` تصميم الفرق للتدفق السريع: أربعة أنواع وثلاثة أنماط تفاعل / Team Topologies: four team types, three interaction modes (documented)

### `ASTRAT-65` — التفاوض بالتعاطف التكتيكي والأسئلة المعايَرة / Negotiation with tactical empathy and calibrated questions

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يجهّز تفاوضًا (راتب، عقد، سعر) بالإصغاء والتسمية والأسئلة المفتوحة وتدقيق الاتهامات والبديل الأفضل، بلا تقسيم للفرق. — Prepares a salary, contract or price negotiation with listening, labelling, open questions, an accusation audit and a BATNA, never splitting the difference.

**متى:** طلب زيادة، تفاوض مع مورّد، عميل يرفض السعر، محادثة صعبة / asking for a raise, vendor terms, a client who will not budge

**كيف:** 1) Before: write your BATNA, target and walk-away; list every negative thing they may think of you (accusation audit) and say it first. 2) Mirror their last 1-3 key words as a question, then stay silent. 3) Label emotions with 'It seems like...' rather than 'I think you...'. 4) Push back with 'How'/'What' questions ('How am I supposed to do that?'), not 'Why'. 5) Summarise their position with its emotions until they say 'That's right'. 6) On money: offers rising 65%, 85%, 95%, 100% of target with a precise final number and a non-monetary extra; no concession without something in return; hunt for unknown facts that change the deal.

**المعاملات:** target, BATNA

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** negotiation · salary · تفاوض · راتب · عقد · BATNA

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-65` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3433-product-strategy/14097-negotiation`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-63` مقابلة سؤال-بسؤال لاستخراج النية الحقيقية قبل البناء / One-question interview to extract real intent (documented)
- `ASTRAT-64` خطاب تقديم وظيفي مفصّل على الإعلان بلا عبارات آلية / Tailored cover letter without AI tells (documented)
- `ASTRAT-66` تصميم الفرق للتدفق السريع: أربعة أنواع وثلاثة أنماط تفاعل / Team Topologies: four team types, three interaction modes (documented)
- `ASTRAT-67` تحقيق 8D ببوابات تحقق لكل مرحلة / Gated 8D investigation coach (documented)

### `ASTRAT-66` — تصميم الفرق للتدفق السريع: أربعة أنواع وثلاثة أنماط تفاعل / Team Topologies: four team types, three interaction modes

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ينظّم فرق الهندسة حسب قانون كونواي والحمل الذهني: فرق مسار، منصة، تمكين، أنظمة معقدة، مع نمط تفاعل معلن لكل زوج. — Organises engineering teams by Conway's law and cognitive load into stream-aligned, platform, enabling and complicated-subsystem teams with a declared interaction mode per pair.

**متى:** إعادة هيكلة فريق، من يملك هذه الخدمة، تقسيم مونوليث، فريق منصة داخلي / reorg, service ownership, splitting a monolith, internal platform

**كيف:** 1) Decide the target architecture, then shape teams so it becomes the natural outcome (inverse Conway). 2) Assign every team one of four types; stream-aligned is the default, the others exist only to remove its load. 3) For each interacting pair declare collaboration (time-boxed discovery), X-as-a-Service or facilitating, and evolve it deliberately. 4) Count domains per team: at most one complicated or two-three simple; split software, not people, when it exceeds a team. 5) Split along fracture planes, business domain first; avoid technology-layer splits. 6) Publish a team API (owners, docs, on-call, request path) and score the design 0-10 with the gaps to 10.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** team topologies · Conway · org design · تنظيم الفرق · هيكلة · platform team

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-66` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3436-systems-architecture/14113-team-topologies`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-64` خطاب تقديم وظيفي مفصّل على الإعلان بلا عبارات آلية / Tailored cover letter without AI tells (documented)
- `ASTRAT-65` التفاوض بالتعاطف التكتيكي والأسئلة المعايَرة / Negotiation with tactical empathy and calibrated questions (documented)
- `ASTRAT-67` تحقيق 8D ببوابات تحقق لكل مرحلة / Gated 8D investigation coach (documented)
- `ASTRAT-68` كتابة تقرير إجراء تصحيحي CAR/CAPA قابل للإغلاق / Closable corrective action report (CAR/CAPA) (documented)

### `ASTRAT-67` — تحقيق 8D ببوابات تحقق لكل مرحلة / Gated 8D investigation coach

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يدير تحقيق جودة 8D من D0 إلى D8 ولا ينتقل لمرحلة قبل أن تجتاز السابقة معاييرها، ويرفض الاحتواء والأسباب الجذرية الضعيفة. — Runs an 8D quality investigation from D0 to D8 and advances only when each discipline passes its criteria, rejecting weak containment and root causes.

**متى:** عيب وصل للعميل، شكوى جودة، مراجعة تقرير 8D قبل إرساله / a defect escape, customer complaint, reviewing an 8D before submission

**كيف:** 1) D0: safety assessment and customer notification before anything else. 2) D1 cross-functional team with a named champion; D2 problem with measured value vs spec, part/revision and 'X of Y = Z%', no cause speculation. 3) D3 containment must physically stop bad product, be in the past tense, dated and verified ('be more careful' is not containment). 4) D4 two validated 5-Why chains: why it occurred and why it escaped; 'human error' is a prompt to ask why the system allowed it. 5) D5 one action per root cause, D6 before/after data on a volume of at least about 3/baseline-rate units. 6) D7 update PFMEA, control plan, work instructions and check similar parts; D8 sign-off and a one-paragraph summary.

**المعاملات:** customer CSR deadlines

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** 8D · quality · root cause · جودة · سبب جذري · CAPA · 5 why

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:d3` ← npm ls d3 أو وجود node_modules/d3
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-67` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2989-quality-engineering-skills/12639-8d-coach`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-65` التفاوض بالتعاطف التكتيكي والأسئلة المعايَرة / Negotiation with tactical empathy and calibrated questions (documented)
- `ASTRAT-66` تصميم الفرق للتدفق السريع: أربعة أنواع وثلاثة أنماط تفاعل / Team Topologies: four team types, three interaction modes (documented)
- `ASTRAT-68` كتابة تقرير إجراء تصحيحي CAR/CAPA قابل للإغلاق / Closable corrective action report (CAR/CAPA) (documented)
- `ASTRAT-69` وصفة إعدادات LoRA وQLoRA للضبط الدقيق / LoRA and QLoRA fine-tuning recipe (documented)

### `ASTRAT-68` — كتابة تقرير إجراء تصحيحي CAR/CAPA قابل للإغلاق / Closable corrective action report (CAR/CAPA)

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يكتب تقرير إجراء تصحيحي بسببين جذريين مثبتين، وإجراء لكل سبب، ودليل تنفيذ، وتحقق من الفعالية بحجم عينة مبرر. — Writes a corrective action report with two validated root causes, one action per cause, implementation evidence and effectiveness verification on a justified sample.

**متى:** الرد على عدم مطابقة أو ملاحظة تدقيق أو شكوى عميل / responding to an NCR, audit finding or customer complaint

**كيف:** 1) Header with traceable number, named owner and named closure authority; problem summary copied exactly from the NCR. 2) Root cause of occurrence and of escape, each as a documented Why chain, validated by reproduction, data correlation, physical evidence or record review (team opinion is not validation). 3) A corrective action table mapping each action to its root cause with owner and date. 4) Implementation evidence = revised documents with revision numbers and approval dates. 5) Verification of effectiveness: method, metric, volume and target defined before collecting data (e.g. zero defects in 60 units for a 5% baseline at 95% confidence). 6) Horizontal deployment, lessons learned, and a closure checklist; 'retrain operators' alone is never enough.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** CAPA · CAR · NCR · ISO 9001 · إجراء تصحيحي · تدقيق

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-68` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2989-quality-engineering-skills/12651-car-corrective-action`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-66` تصميم الفرق للتدفق السريع: أربعة أنواع وثلاثة أنماط تفاعل / Team Topologies: four team types, three interaction modes (documented)
- `ASTRAT-67` تحقيق 8D ببوابات تحقق لكل مرحلة / Gated 8D investigation coach (documented)
- `ASTRAT-69` وصفة إعدادات LoRA وQLoRA للضبط الدقيق / LoRA and QLoRA fine-tuning recipe (documented)
- `ASTRAT-70` سلّم أنظمة دعم العملاء من الخدمة الذاتية إلى مركز الاتصال / Customer-support system ladder: self-service to contact center (documented)

### `ASTRAT-69` — وصفة إعدادات LoRA وQLoRA للضبط الدقيق / LoRA and QLoRA fine-tuning recipe

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يضبط مُكيّف LoRA/QLoRA بالإعدادات المستقرة: كل الطبقات الخطية، alpha = 2×rank، معدل تعلم أعلى بعشر مرات، ورتبة حسب المهمة. — Configures a LoRA/QLoRA adapter with the settled recipe: all linear modules, alpha = 2 × rank, ~10× the full-FT learning rate, rank by task.

**متى:** كتابة أو مراجعة إعدادات تدريب LoRA، الاختيار بين LoRA وQLoRA والضبط الكامل / writing or reviewing a LoRA config, choosing LoRA vs QLoRA vs full fine-tune

**كيف:** 1) Target all linear modules (q,k,v,o and the MLP gate/up/down, which matter most); never drop modules to save memory. 2) Rank: 1-32 for RL adapters, 16-32 default, up to ~256 only for SFT at scale; raise it only if held-out eval underfits. 3) lora_alpha = 2 × r; LR about 10× the full fine-tune LR (QLoRA starts at 2e-4); effective batch under 32. 4) LoRA by default, QLoRA only when bf16 does not fit, full fine-tuning only for dense knowledge injection. 5) Use bf16 where supported (check torch.cuda.is_bf16_supported()), fix the seed, dropout 0 with fused kernels. 6) Treat loss spikes, plateaus or memorisation first as config deviations from this recipe before debugging the loop.

**المعاملات:** rank, model size

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** LoRA · QLoRA · fine-tuning · ضبط دقيق · PEFT · hyperparameters

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:torch` ← python3 -c "import torch" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `gpu` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-69` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3104-llm-finetuning/13291-lora-qlora-recipes`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-67` تحقيق 8D ببوابات تحقق لكل مرحلة / Gated 8D investigation coach (documented)
- `ASTRAT-68` كتابة تقرير إجراء تصحيحي CAR/CAPA قابل للإغلاق / Closable corrective action report (CAR/CAPA) (documented)
- `ASTRAT-70` سلّم أنظمة دعم العملاء من الخدمة الذاتية إلى مركز الاتصال / Customer-support system ladder: self-service to contact center (documented)
- `ASTRAT-71` صياغة الردود للعمل أولًا لقارئ مشتت الانتباه / Action-first response shape for an ADHD reader (documented)

### `ASTRAT-70` — سلّم أنظمة دعم العملاء من الخدمة الذاتية إلى مركز الاتصال / Customer-support system ladder: self-service to contact center

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يؤهل احتياج نظام دعم العملاء بستة أسئلة (الاتجاه، القنوات، الحجم، الأتمتة، أدوات الموظف، التحويلات) ثم يختار درجة السلّم المناسبة. — Qualifies a support-system need with six questions (direction, channels, volume, automation, agent tooling, transfers) and picks the matching rung of the ladder.

**متى:** بناء مركز اتصال، رد آلي IVR، توجيه مكالمات، دعم متعدد القنوات / building a call center, IVR, call routing, omnichannel support

**كيف:** 1) Detect the request level: discovery (whole system), validation (a named pattern) or build (one concrete piece). 2) Ask: inbound/outbound, channel mix, daily volume (<50, 50-500, 500+), self-service depth, agent desktop/CRM, cold vs warm transfer and coaching. 3) Rungs: scripted menu, AI self-service with a human fallback, skills-based routing with queues and conferences, then analytics and real-time assistance. 4) Make every multi-party call a conference (warm transfer, hold, coaching); record dual-channel for QA and pause recording during card entry. 5) Check consent and calling-hours rules, card-data handling, health-data and GDPR recording consent before launch. 6) Make webhooks idempotent and receive-queue-acknowledge fast under load. (Source examples use Twilio; the ladder is vendor-neutral.)

**المعاملات:** volume, channels

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** customer support · contact center · IVR · دعم العملاء · مركز اتصال · routing

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-70` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2721-twilio-developer-kit/10479-twilio-customer-support-architect`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-68` كتابة تقرير إجراء تصحيحي CAR/CAPA قابل للإغلاق / Closable corrective action report (CAR/CAPA) (documented)
- `ASTRAT-69` وصفة إعدادات LoRA وQLoRA للضبط الدقيق / LoRA and QLoRA fine-tuning recipe (documented)
- `ASTRAT-71` صياغة الردود للعمل أولًا لقارئ مشتت الانتباه / Action-first response shape for an ADHD reader (documented)
- `ASTRAT-72` تقرير جلسة برمجة لصاحب قرار غير تقني / Session report for a non-technical stakeholder (documented)

### `ASTRAT-71` — صياغة الردود للعمل أولًا لقارئ مشتت الانتباه / Action-first response shape for an ADHD reader

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يشكّل كل رد ليبدأ بالخطوة التالية القابلة للتنفيذ، بخطوات مرقمة وحالة معادة وقوائم لا تتجاوز خمسة وتقديرات زمنية ملموسة. — Shapes every reply to open with the next doable action, with numbered steps, restated state, lists capped at five and concrete time estimates.

**متى:** 'ادخل في الموضوع'، 'بدون مقدمات'، قارئ مصاب بتشتت الانتباه، تعليمات خطوة بخطوة / 'cut the preamble', ADHD-friendly, step-by-step help

**كيف:** 1) First line is an action (a command, a path, a snippet), not context. 2) Multi-step work is a numbered list, one bounded action per item. 3) Restate state each turn as 'step 3 of 5 done: X. Next: Y' (not a running recap). 4) Estimates in real units; show the finished, working result concretely; state errors flat with cause and fix. 5) Cap lists at five, split into now/later; park tangents as a separate offer; end with one action doable in under two minutes; no preamble, recap or closing pleasantry. 6) Override for 'explain in full', for destructive actions (confirm first) and after three 'still broken' turns (stop and question the assumption).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ADHD · concise · action-first · مختصر · تنسيق الرد · accessibility

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-71` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2411-adhd/9350-shape`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-69` وصفة إعدادات LoRA وQLoRA للضبط الدقيق / LoRA and QLoRA fine-tuning recipe (documented)
- `ASTRAT-70` سلّم أنظمة دعم العملاء من الخدمة الذاتية إلى مركز الاتصال / Customer-support system ladder: self-service to contact center (documented)
- `ASTRAT-72` تقرير جلسة برمجة لصاحب قرار غير تقني / Session report for a non-technical stakeholder (documented)

### `ASTRAT-72` — تقرير جلسة برمجة لصاحب قرار غير تقني / Session report for a non-technical stakeholder

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-strategy` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-strategy.md)) |
| المجموعة | التفكير والتخطيط والاستراتيجية (`thinking`) |
| نوع المخرج (A25، A27) | خطة واستراتيجية وقرار (`plan`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحول جلسة عمل إلى تقرير يتخذ عليه مدير المنتج قرارًا: الدليل قبل التفسير، كل مصطلح معرَّف عند أول ظهور، والتحقق والافتراض وغير المختبر في سلال صريحة. — Turns a work session into a report a product owner can act on: evidence before interpretation, each term defined at first use, and verified/assumed/untested stated in explicit buckets.

**متى:** 'اكتب ملخص اليوم لمدير المنتج'، شرح ما بُني لغير المبرمجين / 'write today up for my PM', explaining a session to a non-developer

**كيف:** 1) Use the conversation as the main source, then corroborate with git log/diff/status; state how far each change got: edited, committed, pushed/merged, or live and observed. 2) Sections, omitting empty ones: one-line summary (the gap between plan and reality is the headline), why we started here, what we found or built (verbatim artifact first), why it happened (name the part that behaved correctly too), how we solved it and why this way (the rejected alternative and what the fix deliberately does not cover), numbers with denominators, verified/assumed/untested, next steps and what I need from you. 3) Attach analogies, never substitute them for the real term. 4) Keep identifiers verbatim in the reader's language. 5) No blame on people or models; describe the missing information. 6) 600-1,200 words for one thread.

**المعاملات:** scope hint

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** status report · stakeholder · PM · تقرير · ملخص الجلسة · non-technical

#### 1. الاستقبال (A25)

- الهدف القابل للقياس: سؤال بإجابة مقترحة ← هدف مقترح بعتبة رقمية يُعرض للتعديل
- الأفق الزمني: افتراض مكتوب ← 90 يومًا
- الموارد والميزانية: افتراض مكتوب ← شخص واحد بلا صرف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `git` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `plan`، والمنفّذ `method:ASTRAT-72` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `decision-math`.
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

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1074-dev-report/2383-dev-report`

#### 7. قدرات قريبة في العائلة

- `ASTRAT-70` سلّم أنظمة دعم العملاء من الخدمة الذاتية إلى مركز الاتصال / Customer-support system ladder: self-service to contact center (documented)
- `ASTRAT-71` صياغة الردود للعمل أولًا لقارئ مشتت الانتباه / Action-first response shape for an ADHD reader (documented)

