# A5 — الحالة والإيصالات والاستئناف / state, receipts and resume (USIP v5.3)

> **متى تقرأه / when to read:** حين يكون العمل طويلًا أو قابلًا للاستئناف أو متعدد الوكلاء، أو تحتاج رمز حالة تشغيلية أو تعافيًا، أو سجل تنفيذ وتسليم. · [العودة إلى النواة / back to the core](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

> **الحالة هنا / backing:** إجراء موثَّق: لا كود في هذا المستودع يكتب هذه السجلات أو يتحقق منها (next_safe_action وrollback_target وlast_verified_checkpoint)؛ أقرب سجل قابل للتشغيل وصفة FusionForge ([A4](A4-fusionforge-composition.md)) وملف `jobs/<id>/DECISIONS.md`.

نُقلت أقسام «المرحلة -1» هنا من `PROTOCOL.md` (v5.2) بنصها وبأرقامها؛ كل تعديل موسوم `(v5.3: …)`. معاني الخطط وكلمات الرد وسلالم الحالة المعتمدة في [مسرد النواة](../../PROTOCOL.md#المسرد--glossary)، وعند أي تعارض تغلب النواة. خريطة كل قسم قديم: [CHANGELOG](CHANGELOG.md).

## الفهرس / contents

- [-1.10.ب — الحالة التشغيلية والتعافي المقيّد](#-110ب--الحالة-التشغيلية-والتعافي-المقيّد)
- [-1.17 حقيبة الاستئناف والسجلات التنفيذية](#-117-حقيبة-الاستئناف-والسجلات-التنفيذية)
- [-1.28 تشغيل الوكلاء بعقود Typed وميزانية سياق](#-128-تشغيل-الوكلاء-بعقود-typed-وميزانية-سياق)
- [-1.29 Continuity OS — ذاكرة مشروع قابلة للاستئناف دون مراقبة خفية](#-129-continuity-os--ذاكرة-مشروع-قابلة-للاستئناف-دون-مراقبة-خفية)
- [-1.33 سجل التنفيذ والإيصالات والتسليم](#-133-سجل-التنفيذ-والإيصالات-والتسليم)
- [-1.46 عقد الحالة المشترك والإثبات القابل للاستئناف](#-146-عقد-الحالة-المشترك-والإثبات-القابل-للاستئناف)
- [خريطة الحقول المتكافئة (v5.3)](#خريطة-الحقول-المتكافئة-v53)

### -1.10.ب — الحالة التشغيلية والتعافي المقيّد

| رمز الحالة | المعنى | التصرف المسموح |
|---|---|---|
| `REGISTRY_VERSION_DRIFT` | معلومات Registry أو Fabric أو Eval لا تطابق الإصدار الفعلي | أوقف النشر؛ اقرأ الحزمة الحية وصحح توافق النسخ في تعديل محمي. |
| `DYNAMIC_MESH_SCHEMA_DRIFT` | مخطط Think/Atlas المستجد لا يطابق المعروف | ارجع للحزم التسع المحلية، ولا تخترع مهارات جديدة. |
| `HOST_SKILL_CATALOG_STALE` | المصدر محدث لكن فهرس المهارات داخل الجلسة قديم | حدّث الفهرس/أعد الاتصال إن أمكن؛ لا تنشر مكررًا باندفاع. |
| `REA_RUNTIME_NOT_EXPOSED` | دليل الهندسة العكسية موجود دون منفذ حقيقي | اقرأ الملفات المتاحة فقط، واذكر تعذر تشغيل REA/Ghidra. |
| `FULL_PRO_BLOCKED` | جميع مسارات Full Pro غير متاحة حاليًا | خطط/نفذ بالمسار المأذون المتاح، ووسم النتيجة NOT_FULL_PRO. |
| `REVIEWERS_FAILED` | لا توجد آثار مراجعة مستقلة صالحة | استخدم أدلة مباشرة وفحصًا حتميًا، ولا تدّع مجلسًا ناجحًا. |
| `HARD_FAIL` | مخالفة أمان أو ملكية أو رخصة أو حساب حتمي أو صلاحية | امنع النشر/الأثر الجانبي حتى الإصلاح والفحص مجددًا. |
| `POSTCONDITION_UNKNOWN` | انتهى اتصال الأداة ولم تثبت النتيجة | اقرأ الحالة الفعلية أولًا، خصوصًا قبل إعادة إرسال/دمج/دفع. |

**علاج الأخطاء:** صنّف الخطأ من دليل، حدّد أقل إصلاح قابل للتراجع ومأذون، أعد اختبار الخطوة الفاشلة فقط، واحتفظ بحالة الطلب ونجاحات المسارات الأخرى. لا تعطّل المصادقة أو الموافقات ولا تغيّر حدود الأمان لإجبار نجاح شكلي. راجع `OPERATIONAL_RUNBOOK.md` إن كان موجودًا فعلًا في الحزمة؛ لا تفترض امتلاك نسخة محدثة منه.

### -1.17 حقيبة الاستئناف والسجلات التنفيذية

احفظ لكل عمل معقد داخل نطاق مشروعه فقط: request_id وobjective وtenant/project scope وcurrent_stage وplan_version وchosen_packs وtool_state وowners وuser_approvals وfrozen_numeric_results وartifacts وchecks_passed/failed وopen_blockers وnext_action وrollback_target. لا تحفظ أي أسرار أو مفاتيح.

عند فشل أداة ذات أثر جانبي، اقرأ الحالة الفعلية قبل إعادة التنفيذ لمنع إرسال رسالة أو نشر أو دفع مرتين. لا تضِع العمل الصحيح للآخرين عند تعثر وكيل واحد. لكل مرحلة: **الوعد → الأثر الملموس → اختبار ما بعد التنفيذ → حالة مثبتة**. عند تغيير المتطلبات، أعد فحص الأجزاء المتأثرة دون إهدار النجاحات القديمة. تقرير التسليم يبدأ بما تحقق حقيقة ثم ما لم يثبت.

### -1.28 تشغيل الوكلاء بعقود Typed وميزانية سياق

لكل وكيل/أداة حدد: objective، input_schema، output_schema، allowed_tools، tenant_scope، artifact_paths، deadline، max_cost، owner، permissions، stop_condition، expected_postcondition، retryable، rollback. مخطط المخرجات يحتوي status وsummary وevidence وartifacts وnext_actions وverified، ومخرجات صريحة لحالتي unknown/error.

- قسّم السياق: قواعد ثابتة / مصادر تُسترجع عند الطلب / قرارات المستخدم / ملاحظات أدوات حديثة. لا تحمل كل فهرس Atlas في الذاكرة مرة واحدة.
- Parse → Schema Validate → Business Validate → Repair once → Fail closed؛ صحة JSON لا تثبت صحة القرار.
- وفّر cancellation قبل الأثر الجانبي التالي، وميز بين timeout وفشل عمل وفقد اتصال. لا تنفذ الطلب نفسه مرتين إذا كانت حالة الكتابة مجهولة.
- تنقل واجهات GUI وWindows إلى منفذ الجهاز المصرح به، وتظل طرق SEE إرشادية.
- إذا كان التوازي مفيداً فعلاً، افصل ملكية الملفات وأرقام الطلبات والمخاطر. عدد الوكلاء **ليس** معيار نجاح.

### -1.29 Continuity OS — ذاكرة مشروع قابلة للاستئناف دون مراقبة خفية

احفظ للمشروع الذي يأذن به المستخدم فقط: objective، plan_id، decision_log، user_approvals، inputs_hashes، immutable_artifacts، last_verified_checkpoint، open_failures، frozen_numeric_facts، next_safe_action، expected_receipt، tenant_id. امحُ المعلومات الحساسة من الملخصات المشتركة. الدروس عامة النطاق تمر عبر مراجعة وموافقة مستقلة؛ لا ترقِ سلوك شركة إلى قاعدة شركات أخرى.

الاستئناف: تحقّق من الحالة الراهنة أولاً؛ استعد أحدث checkpoint صالح؛ قارن ما تغيّر؛ عالج **delta** فقط. حافظ على عمل الوكلاء الناجحين؛ فشل خطوة لا يعني مسح الكل. سجّل أدلة فعالة لعزل crash / drift / stale catalog / absent runtime / permission failure / quota. تعلّم نمطاً قابلًا للنقل فقط إذا ظهر في مشروعين مستقلين مع اختبار نفي وموافقة، وليس من جلسة واحدة.

### -1.33 سجل التنفيذ والإيصالات والتسليم

اعتمد وثيقة تنفيذ مختصرة قابلة للتحويل إلى JSON ذات الحقول التالية (لا تحفظ أسراراً):

~~~json
{
  "request_id": "nonsecret-id",
  "mode": "fast|standard|deep|full_pro",
  "goal": "...",
  "plan_id": "A|B|C|D",
  "selected_methods": [],
  "dynamic_specialists": [],
  "required_outputs": [],
  "owner": "...",
  "authorization": "not_required|pending|granted",
  "status": "planned|blocked|running|produced|tested|verified|delivered",
  "evidence": [],
  "artifacts": [],
  "failed_gates": [],
  "retryable": false,
  "next_safe_action": "..."
}
~~~

(v5.3: هذه حالات مهمة أو عمل؛ حالات التسليم وسلّم المنفذ في [المسرد](../../PROTOCOL.md#المسرد--glossary).) الاستحقاق لا يتقدم إلا بإيصال حقيقي: planned ≠ executed، produced ≠ verified، verified ≠ delivered. اختبارات Markdown تثبت تكامل الوثيقة، لا تثبت جودة المجلس أو نجاح Fast/Full Pro أو سلامة تشغيل Blender. بعد أي نشر: اقرأ الملف المنشور مرة أخرى وتحقق من المحتوى والهاش واحتفظ بربط commit؛ لا تستخدم مؤشرات CI الخالية كنجاح.

### -1.46 عقد الحالة المشترك والإثبات القابل للاستئناف

استخدم سجلاً غير سري بهذه المفاتيح عند أي أثر حقيقي:
request_id | goal | tenant_id | plan_id | mode | full_pro_required | owner | executor_exposed | authorized | observed_health | selected_methods | expected_postconditions | artifacts | receipts | completed_gates | failure_code | idempotency_key | rollback | last_verified_checkpoint | next_safe_action

السلم الصحيح: candidate → selected → method_loaded → executor_exposed → configured/authorized → online/available → executed → verified. حالات التسليم: PLAN_ONLY، BLOCKED، EXECUTED_UNVERIFIED، PARTIALLY_VERIFIED، DONE_VERIFIED. لا تُعَد محاولة تنفيذ بعد timeout قبل فحص الأثر بالمفتاح الأصلي. عند فقد اتصال احتفظ بالخطوات الصحيحة واستأنف delta فقط. لا تسرب مصدر شركة إلى أخرى.

### خريطة الحقول المتكافئة (v5.3)

السجلات الأربعة أعلاه (-1.17 و-1.29 و-1.33 و-1.46) تصف السجل نفسه بأسماء مختلفة؛ هذه أسماؤها المتكافئة، والاسم الأول هو المعتمد:

| المعتمد | يقابله |
|---|---|
| `goal` | objective (-1.17، -1.29) |
| `request_id` | request_id (-1.17، -1.33، -1.46) |
| `tenant_id` | tenant/project scope (-1.17) |
| `plan_id` | plan_version (-1.17)؛ وفي FusionForge `plan_choice.plan` |
| `next_safe_action` | next_action (-1.17) |
| `rollback` | rollback_target (-1.17) |
| `frozen_numeric_facts` | frozen_numeric_results (-1.17) |
| `selected_methods` | chosen_packs (-1.17) |
| `last_verified_checkpoint` | checks_passed (-1.17) بآخر نقطة سليمة |
| `failure_code` | open_blockers / open_failures / failed_gates |
| `receipts` | evidence / expected_receipt |

حالات المهمة في -1.33 (planned … delivered) غير حالات التسليم وسلّم المنفذ وحالات الوصفة؛ الثلاثة في [المسرد](../../PROTOCOL.md#المسرد--glossary).
