# `atlas-build` — البرمجة وبناء التطبيقات (52 بطاقة)

> مكتبة بروتوكول USIP v5.6 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/atlas-build.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/software.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`ABUILD-01` تنفيذ خارطة الطريق تلقائياً: مرحلة لكل طلب دمج](#abuild-01--تنفيذ-خارطة-الطريق-تلقائياً-مرحلة-لكل-طلب-دمج--autonomous-phase-per-pr-roadmap-execution-loop)
- [`ABUILD-02` مسجل قياس تشغيل بالملاحظة فقط](#abuild-02--مسجل-قياس-تشغيل-بالملاحظة-فقط--observation-only-run-telemetry-recorder)
- [`ABUILD-03` خط وكلاء بأدوار ومراحل وأقفال كتابة واستئناف](#abuild-03--خط-وكلاء-بأدوار-ومراحل-وأقفال-كتابة-واستئناف--role-squad-agent-pipeline-with-stages-locks-and-resume)
- [`ABUILD-04` تفكيك المواصفة إلى مهام صغيرة لوكلاء البرمجة](#abuild-04--تفكيك-المواصفة-إلى-مهام-صغيرة-لوكلاء-البرمجة--spec-to-task-decomposition-for-coding-agents)
- [`ABUILD-05` مسار توقيع وإصدار تطبيقات الجوال والمكتب](#abuild-05--مسار-توقيع-وإصدار-تطبيقات-الجوال-والمكتب--mobile-and-desktop-release-signing-pipeline)
- [`ABUILD-06` نموذج HTML تجريبي يجيب أسئلة مفتوحة](#abuild-06--نموذج-html-تجريبي-يجيب-أسئلة-مفتوحة--open-question-html-prototype-spike)
- [`ABUILD-07` تنسيق بناء تطبيق كامل على مراحل](#abuild-07--تنسيق-بناء-تطبيق-كامل-على-مراحل--phased-full-stack-app-build-orchestration)
- [`ABUILD-08` تقييم النموذج مقابل معايير القبول](#abuild-08--تقييم-النموذج-مقابل-معايير-القبول--prototype-evaluation-vs-acceptance-criteria)
- [`ABUILD-09` توليد PWA مع service worker](#abuild-09--توليد-pwa-مع-service-worker--pwa-manifest-and-service-worker-generation)
- [`ABUILD-10` هيكلة مشروع SaaS جاهز](#abuild-10--هيكلة-مشروع-saas-جاهز--saas-boilerplate-scaffold-spec)
- [`ABUILD-11` حالة الاشتراكات وواجهة إدارة الاشتراك](#abuild-11--حالة-الاشتراكات-وواجهة-إدارة-الاشتراك--subscription-store-state-and-paywall-ui)
- [`ABUILD-12` نموذج أولي مؤقت للإجابة عن سؤال](#abuild-12--نموذج-أولي-مؤقت-للإجابة-عن-سؤال--throwaway-prototype-to-answer-one-question)
- [`ABUILD-13` بناء موقع Wix هيدلس من وصفات SDK](#abuild-13--بناء-موقع-wix-هيدلس-من-وصفات-sdk--wix-headless-site-build-from-sdk-recipes)
- [`ABUILD-14` حلقة مراجع شجرة الوصولية لتحكم المتصفح](#abuild-14--حلقة-مراجع-شجرة-الوصولية-لتحكم-المتصفح--accessibility-tree-ref-loop-for-browser-agents)
- [`ABUILD-15` استنساخ موقع بأدلة المتصفح](#abuild-15--استنساخ-موقع-بأدلة-المتصفح--browser-evidence-website-clone-workflow)
- [`ABUILD-16` تصحيح الصفحات الحية عبر Chrome DevTools MCP](#abuild-16--تصحيح-الصفحات-الحية-عبر-chrome-devtools-mcp--chrome-devtools-mcp-debugging-of-live-pages)
- [`ABUILD-17` خط لقطات Playwright داخل حاوية](#abuild-17--خط-لقطات-playwright-داخل-حاوية--containerized-playwright-screenshot-pipeline)
- [`ABUILD-18` تشغيل متصفحات معزولة عبر بروتوكولاتها](#abuild-18--تشغيل-متصفحات-معزولة-عبر-بروتوكولاتها--isolated-headless-chromefirefoxsafari-drivers-over-native-protocols)
- [`ABUILD-19` جلسات Playwright مسماة بمخرجات على القرص](#abuild-19--جلسات-playwright-مسماة-بمخرجات-على-القرص--named-session-playwright-cli-with-disk-artifacts)
- [`ABUILD-20` كتابة اختبارات E2E مع فحص الوصولية والأداء](#abuild-20--كتابة-اختبارات-e2e-مع-فحص-الوصولية-والأداء--playwright-e2e-authoring-with-lint-a11y-and-cwv-scans)
- [`ABUILD-21` رفع ملف عبر Playwright MCP لحقل مخفي](#abuild-21--رفع-ملف-عبر-playwright-mcp-لحقل-مخفي--playwright-mcp-hidden-file-input-upload-workaround)
- [`ABUILD-22` إثبات السلوك المعروض بحكم نجح/فشل/معطل](#abuild-22--إثبات-السلوك-المعروض-بحكم-نجحفشلمعطل--rendered-behavior-proof-with-passfailblocked-verdict)
- [`ABUILD-23` فحص جودة الواجهة بثلاثة عروض](#abuild-23--فحص-جودة-الواجهة-بثلاثة-عروض--three-width-responsive-browser-qa-report)
- [`ABUILD-24` ضبط مجمع الاتصالات وموثوقية قاعدة البيانات](#abuild-24--ضبط-مجمع-الاتصالات-وموثوقية-قاعدة-البيانات--connection-pool-sizing-and-db-reliability-playbook)
- [`ABUILD-25` نص نسخ احتياطي لقاعدة البيانات مع الاحتفاظ والتشفير](#abuild-25--نص-نسخ-احتياطي-لقاعدة-البيانات-مع-الاحتفاظ-والتشفير--database-backup-script-with-retention-and-encryption)
- [`ABUILD-26` تطور مخططات الأحداث وKafka](#abuild-26--تطور-مخططات-الأحداث-وkafka--event-schema-evolution-and-kafka-platform-playbook)
- [`ABUILD-27` قواعد Postgres وRedis المُدارة على المنصات](#abuild-27--قواعد-postgres-وredis-المُدارة-على-المنصات--managed-postgres-and-redis-on-hosting-platforms)
- [`ABUILD-28` دليل الحوادث: احتواء وتشخيص واستعادة](#abuild-28--دليل-الحوادث-احتواء-وتشخيص-واستعادة--incident-runbook-contain-diagnose-recover)
- [`ABUILD-29` تصميم المراقبة: الإشارات الذهبية والتنبيهات](#abuild-29--تصميم-المراقبة-الإشارات-الذهبية-والتنبيهات--observability-design-golden-signals-and-alerts)
- [`ABUILD-30` استطلاع البنية وتدقيق التكلفة](#abuild-30--استطلاع-البنية-وتدقيق-التكلفة--infra-reconnaissance-and-cost-audit)
- [`ABUILD-31` تصميم مكوّن متاح افتراضيا](#abuild-31--تصميم-مكوّن-متاح-افتراضيا--accessible-by-default-component-pattern-design)
- [`ABUILD-32` إعداد هوية العلامة مع فحص التباين](#abuild-32--إعداد-هوية-العلامة-مع-فحص-التباين--brand-palette-onboarding-with-wcag-gate)
- [`ABUILD-33` حسابات الألوان وتخطيط CSS مع التباين](#abuild-33--حسابات-الألوان-وتخطيط-css-مع-التباين--color-and-css-layout-math-with-contrast)
- [`ABUILD-34` التصميم عبر قيود مكانية وطباعية صريحة](#abuild-34--التصميم-عبر-قيود-مكانية-وطباعية-صريحة--design-by-explicit-spatial-and-type-constraints)
- [`ABUILD-35` نقد التصميم وتسليم المطورين وتدقيق النظام](#abuild-35--نقد-التصميم-وتسليم-المطورين-وتدقيق-النظام--design-critique-handoff-and-system-audit)
- [`ABUILD-36` اشتقاق وترقية نظام التصميم](#abuild-36--اشتقاق-وترقية-نظام-التصميم--design-system-retrofit-and-derivation-workflow)
- [`ABUILD-37` رموز التصميم DTCG لكل المنصات](#abuild-37--رموز-التصميم-dtcg-لكل-المنصات--dtcg-design-tokens-multi-platform-export)
- [`ABUILD-38` تدقيق تصميم الواجهة بالأدلة](#abuild-38--تدقيق-تصميم-الواجهة-بالأدلة--evidence-backed-frontend-design-audit)
- [`ABUILD-39` استخراج بصمة التصميم من موقع حي](#abuild-39--استخراج-بصمة-التصميم-من-موقع-حي--extract-design-dna-from-live-website)
- [`ABUILD-40` من ملف Figma إلى رموز وأصول وكود](#abuild-40--من-ملف-figma-إلى-رموز-وأصول-وكود--figma-file-to-tokens-assets-and-code)
- [`ABUILD-41` قراءة Figma عبر MCP أو REST](#abuild-41--قراءة-figma-عبر-mcp-أو-rest--figma-read-via-mcp-or-rest-fallback)
- [`ABUILD-42` من Figma إلى كود مطابق](#abuild-42--من-figma-إلى-كود-مطابق--figma-to-pixel-exact-code-plan)
- [`ABUILD-43` تدقيق أداء الواجهة والاستجابة](#abuild-43--تدقيق-أداء-الواجهة-والاستجابة--frontend-performance-and-responsive-audit)
- [`ABUILD-44` اختبار الوصولية بلوحة المفاتيح مباشرة](#abuild-44--اختبار-الوصولية-بلوحة-المفاتيح-مباشرة--live-keyboard-accessibility-test-via-browser)
- [`ABUILD-45` صفحة هبوط فاخرة بحركة GSAP](#abuild-45--صفحة-هبوط-فاخرة-بحركة-gsap--premium-landing-page-with-gsap-scroll-motion)
- [`ABUILD-46` حلقة مقارنة لقطة الصفحة بالتصميم](#abuild-46--حلقة-مقارنة-لقطة-الصفحة-بالتصميم--screenshot-vs-design-pixel-diff-loop)
- [`ABUILD-47` حلقة مقارنة لقطة الشاشة بالمرجع](#abuild-47--حلقة-مقارنة-لقطة-الشاشة-بالمرجع--screenshot-vs-reference-pixel-diff-loop)
- [`ABUILD-48` معمارية رموز التصميم بثلاث طبقات](#abuild-48--معمارية-رموز-التصميم-بثلاث-طبقات--three-tier-design-token-architecture-with-theming)
- [`ABUILD-49` تدقيق إتاحة WCAG 2.2: فحص وإصلاح وتحقق](#abuild-49--تدقيق-إتاحة-wcag-22-فحص-وإصلاح-وتحقق--wcag-22-scan-fix-verify-accessibility-audit)
- [`ABUILD-50` إصدار نسخة: وسم ونشر وتحقق](#abuild-50--إصدار-نسخة-وسم-ونشر-وتحقق--cut-a-release-tag-github-release-verify)
- [`ABUILD-51` صياغة التذاكر وأوصاف PR بهيكل ماذا/لماذا/كيف](#abuild-51--صياغة-التذاكر-وأوصاف-pr-بهيكل-ماذالماذاكيف--whatwhyhow-ticket-and-pr-drafting)
- [`ABUILD-52` فرز أعطال الاتصال حسب مجال الخطأ دون تغيير الإعدادات](#abuild-52--فرز-أعطال-الاتصال-حسب-مجال-الخطأ-دون-تغيير-الإعدادات--fault-domain-connectivity-triage-without-touching-config)

## البطاقات / cards

### `ABUILD-01` — تنفيذ خارطة الطريق تلقائياً: مرحلة لكل طلب دمج / Autonomous phase-per-PR roadmap execution loop

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0 / MIT (no copyleft seen among supporting ids); the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** قيادة خارطة طريق معتمدة ذات مراحل حتى النهاية دون إشراف: وكيل منفذ معزول لكل مرحلة، وطلب دمج مشروط بنجاح CI والمراجع الآلي، ثم الدمج بعد مهلة وتحديث اللوحات وتسلسل المرحلة التالية. — Drive an approved phased roadmap to completion unattended with one isolated implementer subagent per phase, each PR gated on CI and the review bot, merged after a grace window, then dashboards updated and the next phase chained.

**متى:** An approved roadmap with per-phase task files exists; 'run autopilot'; overnight multi-phase build; any unattended loop that needs finite limits and stop conditions.

**كيف:** 1) Preflight in every mode: gh installed and authenticated, git base branch reachable on origin, roadmap with progress dashboard plus per-phase task files, a config doc present, declared external tools up; refuse rather than invent plans. 2) init mode writes the config from the roadmap, then STOPS for human review. 3) run: orchestrator spawns one isolated implementer per phase, opens a PR, waits for CI and review bot via background wake-ups, fixes findings, merges only when the full merge gate holds after a grace window, updates dashboards, chains the next phase. 4) Declare finite loop limits and termination conditions up front; stop on any unmet precondition.

**المعاملات:** mode (init\|run\|status); roadmap path; grace window; loop limits; retry-watchdog env for unattended sessions

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** autopilot · roadmap · pull-request · تنفيذ-ذاتي · loop

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `claude:tools` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/899-bymax-codex/2087-autopilot`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3407-clean-room/13957-clean-room-loop`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3111-constellation/13312-roundloop`

#### 7. قدرات قريبة في العائلة

- `ABUILD-02` مسجل قياس تشغيل بالملاحظة فقط / Observation-only run telemetry recorder (documented)
- `ABUILD-03` خط وكلاء بأدوار ومراحل وأقفال كتابة واستئناف / Role-squad agent pipeline with stages, locks and resume (documented)

### `ABUILD-02` — مسجل قياس تشغيل بالملاحظة فقط / Observation-only run telemetry recorder

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تسجيل التوقفات والأخطاء وأزمنة المراحل عبر مسجل موثق دون تشخيص. — Record halts, errors and stage timings through a validated recorder with observation-not-diagnosis rule.

**متى:** Long migration or pipeline runs.

**كيف:** 1) start dims json. 2) stage start/end with outcome. 3) record event (types not instances, max 400 chars, no secrets). 4) wait start/end for user halts. 5) finalize rollup.

**المعاملات:** project path

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** telemetry · observability · قياس

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3419-wix/14021-rp-telemetry`

#### 7. قدرات قريبة في العائلة

- `ABUILD-01` تنفيذ خارطة الطريق تلقائياً: مرحلة لكل طلب دمج / Autonomous phase-per-PR roadmap execution loop (documented)
- `ABUILD-03` خط وكلاء بأدوار ومراحل وأقفال كتابة واستئناف / Role-squad agent pipeline with stages, locks and resume (documented)
- `ABUILD-04` تفكيك المواصفة إلى مهام صغيرة لوكلاء البرمجة / Spec-to-task decomposition for coding agents (documented)

### `ABUILD-03` — خط وكلاء بأدوار ومراحل وأقفال كتابة واستئناف / Role-squad agent pipeline with stages, locks and resume

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يشغّل فريق وكلاء بأدوار (مطوّر ومراجع خصم ومختبر جودة) بخطة معماري عبر بوابات مراحل وأقفال كتابة واستئناف يبدأ بالتحقق، مع تنسيق بالرسائل وسجل مشترك. — Run an architect-planned team of role agents (developer, adversarial reviewer, QA) through staged gates with write locks and verify-first resume, coordinating via messages and a shared log.

**متى:** User wants an agent team on a repo's open issues, role-based specialist analysis (researcher, architect, PM), or to configure Claude Code agent teams with lead/teammates and messaging.

**كيف:** 1) An architect pass sorts outstanding issues into parallelizable groups. 2) Each issue gets a small squad: developer, adversarial reviewer, QA/SDET. 3) Define stages and gates; hold write locks so two roles never edit the same artifact. 4) Specialist deep-dive: researcher, architect and PM run in parallel and yield a prioritized next-build report. 5) Coordinate with SendMessage/TaskUpdate and ring a 'doorbell' instead of pasting payloads; log traffic as JSONL. 6) Show run status (stages, roles, locks, gates); resume an interrupted run verify-first.

**المعاملات:** repo and issue list; role set; stage gates; capacity

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** agent-teams · orchestration · role-based · فريق وكلاء · SendMessage

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3263-agent-team-orchestration/13774-agent-team-orchestration`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3605-ateam/14480-run`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2134-agent-patterns-plugin/7563-agent-teams`

#### 7. قدرات قريبة في العائلة

- `ABUILD-01` تنفيذ خارطة الطريق تلقائياً: مرحلة لكل طلب دمج / Autonomous phase-per-PR roadmap execution loop (documented)
- `ABUILD-02` مسجل قياس تشغيل بالملاحظة فقط / Observation-only run telemetry recorder (documented)
- `ABUILD-04` تفكيك المواصفة إلى مهام صغيرة لوكلاء البرمجة / Spec-to-task decomposition for coding agents (documented)
- `ABUILD-05` مسار توقيع وإصدار تطبيقات الجوال والمكتب / Mobile and desktop release signing pipeline (documented)

### `ABUILD-04` — تفكيك المواصفة إلى مهام صغيرة لوكلاء البرمجة / Spec-to-task decomposition for coding agents

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحوّل مواصفة أو خطة إلى مهام صغيرة قابلة للتحقق مع الاعتماديات وعلامات التوازي وفحوص الإنجاز ومستويات الاستقلالية وجدول تغطية معايير القبول. — Turn a spec or plan into small, verifiable agent tasks with dependencies, parallel markers, done-checks, autonomy levels and an acceptance-criteria coverage table.

**متى:** User has a spec/PRD/plan to hand to coding agents, wants work split for parallel sessions or worktrees, or an agent drifts and fails on tasks that are too large.

**كيف:** 1) Read spec and plan; list deliverables (endpoints, components, migrations, jobs, docs). 2) Order phases: setup -> contracts/tests -> core -> integration -> polish. 3) Size each task to one verifiable outcome, about 1-4 human hours or a diff reviewable in under 15 minutes, touching a small named file set; split any task needing 'and also'. 4) Write each as `T-07 [P] title` with Covers (FR/AC ids), Depends on, Files, Done when (a test or command), Autonomy level. 5) Mark [P] only for disjoint files with no unmerged dependency. 6) Name the critical path and tasks needing a human decision. 7) Emit tasks.md with a coverage table; drop tasks with no source requirement.

**المعاملات:** spec/plan path; autonomy policy; parallel-session limit

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** task-breakdown · spec-driven · INVEST · تفكيك المهام · tasks.md

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3050-adlc-intent/13136-task-decomposition`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2230-ai-coding-model-guidance/8467-coding-agent-task-scoping`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2139-blueprint-plugin/7620-blueprint-work-order`

#### 7. قدرات قريبة في العائلة

- `ABUILD-02` مسجل قياس تشغيل بالملاحظة فقط / Observation-only run telemetry recorder (documented)
- `ABUILD-03` خط وكلاء بأدوار ومراحل وأقفال كتابة واستئناف / Role-squad agent pipeline with stages, locks and resume (documented)
- `ABUILD-05` مسار توقيع وإصدار تطبيقات الجوال والمكتب / Mobile and desktop release signing pipeline (documented)
- `ABUILD-06` نموذج HTML تجريبي يجيب أسئلة مفتوحة / Open-question HTML prototype spike (documented)

### `ABUILD-05` — مسار توقيع وإصدار تطبيقات الجوال والمكتب / Mobile and desktop release signing pipeline

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يصمم التوقيع والتوثيق والطرح المرحلي والتحديث الآمن لتطبيقات الجوال والمكتب. — Design code signing, notarization, staged rollout and safe auto-update for mobile and desktop apps.

**متى:** Setting up CI releases or diagnosing signing failures.

**كيف:** 1) iOS: Fastlane match for certs, Android: keystore kept out of repo. 2) macOS: Developer ID, hardened runtime, notarytool then staple; Windows: Authenticode, EV cert. 3) Keys in CI secrets. 4) Updater verifies signature, uses channels, staged rollout, rollback, version floor. 5) Pick Electron vs Tauri by real needs.

**المعاملات:** platform

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** signing · release · notarization · توقيع التطبيقات

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `os:macos` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2279-desktop-app-engineering/8701-packaging-signing-and-updates`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2340-mobile-engineering/8992-app-store-release-pipeline`

#### 7. قدرات قريبة في العائلة

- `ABUILD-03` خط وكلاء بأدوار ومراحل وأقفال كتابة واستئناف / Role-squad agent pipeline with stages, locks and resume (documented)
- `ABUILD-04` تفكيك المواصفة إلى مهام صغيرة لوكلاء البرمجة / Spec-to-task decomposition for coding agents (documented)
- `ABUILD-06` نموذج HTML تجريبي يجيب أسئلة مفتوحة / Open-question HTML prototype spike (documented)
- `ABUILD-07` تنسيق بناء تطبيق كامل على مراحل / Phased full-stack app build orchestration (documented)

### `ABUILD-06` — نموذج HTML تجريبي يجيب أسئلة مفتوحة / Open-question HTML prototype spike

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يبني نموذج HTML واحداً تتحكم فيه الأسئلة المفتوحة مع تقرير نتائج. — Build one self-contained clickable HTML prototype whose controls are the open questions, with harvest table and spike report.

**متى:** Requirement needs validating or a technique is unproven before building.

**كيف:** 1) ANCHOR on a requirement id or technique with at least one named open question. 2) Open spike-report.md immediately and append as you go. 3) Harvest structure/tokens/payloads from source into harvest-table.md; only invent what the requirement adds and annotate it. 4) Keep reviewer shell visually distinct from app tokens. 5) Data fidelity: live > recorded > labeled stub.

**المعاملات:** anchor id, open questions

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** prototype · spike · html · نموذج أولي · تصميم

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3394-prototype-spike/13930-prototype-spike`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3394-prototype-spike/13930-prototype-spike`

#### 7. قدرات قريبة في العائلة

- `ABUILD-04` تفكيك المواصفة إلى مهام صغيرة لوكلاء البرمجة / Spec-to-task decomposition for coding agents (documented)
- `ABUILD-05` مسار توقيع وإصدار تطبيقات الجوال والمكتب / Mobile and desktop release signing pipeline (documented)
- `ABUILD-07` تنسيق بناء تطبيق كامل على مراحل / Phased full-stack app build orchestration (documented)
- `ABUILD-08` تقييم النموذج مقابل معايير القبول / Prototype evaluation vs acceptance criteria (documented)

### `ABUILD-07` — تنسيق بناء تطبيق كامل على مراحل / Phased full-stack app build orchestration

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ينسق المواصفة والنموذج والخلفية والواجهة عبر خطة عمل متتبعة وملفات تسليم. — Sequence spec, prototype, backend, agent and frontend work from a tracked work plan with handoff envelopes.

**متى:** Large app build needing staged delegation and resumable state.

**كيف:** 1) Resolve kit dir and require clean git tree. 2) Author spec then HTML prototype. 3) Analyze outputs to decide which backend/agent/frontend tracks are needed. 4) Track in a work-plan file with pointer json. 5) After each delegate, read its result envelope and check liveness. 6) Resume by reading the plan; one phase at a time (build skill).

**المعاملات:** app name or plan slug

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** orchestration · work-plan · بناء تطبيق · phases

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2104-app-orchestrator-kit/7475-orchestrate-app`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3431-metaskills/14075-create-app`

#### 7. قدرات قريبة في العائلة

- `ABUILD-05` مسار توقيع وإصدار تطبيقات الجوال والمكتب / Mobile and desktop release signing pipeline (documented)
- `ABUILD-06` نموذج HTML تجريبي يجيب أسئلة مفتوحة / Open-question HTML prototype spike (documented)
- `ABUILD-08` تقييم النموذج مقابل معايير القبول / Prototype evaluation vs acceptance criteria (documented)
- `ABUILD-09` توليد PWA مع service worker / PWA manifest and service worker generation (documented)

### `ABUILD-08` — تقييم النموذج مقابل معايير القبول / Prototype evaluation vs acceptance criteria

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يختبر النموذج بمعايير القبول وسيناريوهات مستخدمين ويصدر تقريراً مصوراً. — Run AC verdicts with fix loop then persona Playwright walkthroughs and emit an HTML evidence report.

**متى:** Validating a UX prototype before MR review or stakeholder share.

**كيف:** 1) Require ticket key and reachable URL or built dist (serve with sirv --single). 2) Phase A: check each acceptance criterion with source access, fix FAILs, log iterations. 3) Phase B: persona walkthroughs via Playwright with screenshots and think-aloud traces. 4) Write evaluation-report.html and csv. 5) Optionally publish to Pages/Vercel.

**المعاملات:** ticket key, URL, workspace

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** usability · playwright · evaluation · اختبار · تجربة المستخدم

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3010-uxd-prototype/12859-uxd-prototype-evaluate`

#### 7. قدرات قريبة في العائلة

- `ABUILD-06` نموذج HTML تجريبي يجيب أسئلة مفتوحة / Open-question HTML prototype spike (documented)
- `ABUILD-07` تنسيق بناء تطبيق كامل على مراحل / Phased full-stack app build orchestration (documented)
- `ABUILD-09` توليد PWA مع service worker / PWA manifest and service worker generation (documented)
- `ABUILD-10` هيكلة مشروع SaaS جاهز / SaaS boilerplate scaffold spec (documented)

### `ABUILD-09` — توليد PWA مع service worker / PWA manifest and service worker generation

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يولد PWA بملف manifest وعامل خدمة. — Generate a PWA with manifest, service worker caching and engine-gap awareness.

**متى:** Making web app installable or offline-capable.

**كيف:** 1) Write manifest with icons, display, start_url. 2) Register service worker with cache strategy per route. 3) Check engine gaps (iOS vs Chromium) in pwa-expert notes. 4) Test with Lighthouse.

**المعاملات:** app name, strategy

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pwa · service-worker · manifest · تطبيق ويب · عمل دون اتصال

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/723-pwa-builder/1752-pwa`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/723-pwa-builder/1752-pwa`

#### 7. قدرات قريبة في العائلة

- `ABUILD-07` تنسيق بناء تطبيق كامل على مراحل / Phased full-stack app build orchestration (documented)
- `ABUILD-08` تقييم النموذج مقابل معايير القبول / Prototype evaluation vs acceptance criteria (documented)
- `ABUILD-10` هيكلة مشروع SaaS جاهز / SaaS boilerplate scaffold spec (documented)
- `ABUILD-11` حالة الاشتراكات وواجهة إدارة الاشتراك / Subscription store state and paywall UI (documented)

### `ABUILD-10` — هيكلة مشروع SaaS جاهز / SaaS boilerplate scaffold spec

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يولّد هيكل SaaS كامل بمصادقة وفواتير ولوحة تحكم من وصف قصير. — Generate a Next.js App Router SaaS skeleton with auth, DB, Stripe billing, dashboard and marketing groups from a short brief.

**متى:** New SaaS or multi-tenant product kickoff.

**كيف:** 1) Collect brief: product, auth (nextauth/clerk/supabase), DB, payments, features. 2) Lay out route groups (auth), (dashboard), (marketing), api/webhooks/stripe, billing checkout/portal. 3) Add lib/auth, lib/db with Drizzle schema, plan cards, usage meter. 4) Wire Stripe webhooks with signature check. 5) Add tenant isolation per tenant-bill pattern.

**المعاملات:** auth, db, payments, features

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** saas · scaffold · nextjs · سااس · هيكل

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/198-product-skills/641-saas-scaffolder`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/198-product-skills/641-saas-scaffolder`

#### 7. قدرات قريبة في العائلة

- `ABUILD-08` تقييم النموذج مقابل معايير القبول / Prototype evaluation vs acceptance criteria (documented)
- `ABUILD-09` توليد PWA مع service worker / PWA manifest and service worker generation (documented)
- `ABUILD-11` حالة الاشتراكات وواجهة إدارة الاشتراك / Subscription store state and paywall UI (documented)
- `ABUILD-12` نموذج أولي مؤقت للإجابة عن سؤال / Throwaway prototype to answer one question (documented)

### `ABUILD-11` — حالة الاشتراكات وواجهة إدارة الاشتراك / Subscription store state and paywall UI

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يفحص حالة المنتجات ويضيف مركز العملاء للاشتراكات. — Inspect App Store/Play product state and add RevenueCat Customer Center to an app.

**متى:** Mobile subscription apps, pricing tiers, app valuation.

**كيف:** 1) Inspect product state across stores via the store-state skill. 2) Add Customer Center UI for self-service management. 3) Configure plans/usage pricing. 4) Estimate app value from recurring revenue multiples.

**المعاملات:** store, SDK

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** subscriptions · billing · revenuecat · اشتراكات · فوترة

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/723-pwa-builder/1752-pwa`

#### 7. قدرات قريبة في العائلة

- `ABUILD-09` توليد PWA مع service worker / PWA manifest and service worker generation (documented)
- `ABUILD-10` هيكلة مشروع SaaS جاهز / SaaS boilerplate scaffold spec (documented)
- `ABUILD-12` نموذج أولي مؤقت للإجابة عن سؤال / Throwaway prototype to answer one question (documented)
- `ABUILD-13` بناء موقع Wix هيدلس من وصفات SDK / Wix headless site build from SDK recipes (documented)

### `ABUILD-12` — نموذج أولي مؤقت للإجابة عن سؤال / Throwaway prototype to answer one question

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يبني نموذجا مؤقتا أو واجهة قابلة للنقر لحسم سؤال تصميم أو جدوى واحد ثم يحذفه أو يعتمده. — Build a disposable prototype or clickable mock to settle a single design or feasibility question, then discard or keep.

**متى:** Unclear how something should work or feel; requirements interview needs visuals.

**كيف:** 1) State the single question and a fixed budget. 2) Build minimum throwaway code in an isolated folder. 3) For requirements, render screens in a local dashboard while interviewing, pushing state each turn and draining user events first. 4) Record answer and decision, then keep or delete. 5) Fold results into SPEC.md.

**المعاملات:** question, time budget

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** prototype · spec · نموذج أولي · mockup

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1120-ambient-library/2627-grill-with-prototype`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1120-ambient-library/2601-chat-n-build`

#### 7. قدرات قريبة في العائلة

- `ABUILD-10` هيكلة مشروع SaaS جاهز / SaaS boilerplate scaffold spec (documented)
- `ABUILD-11` حالة الاشتراكات وواجهة إدارة الاشتراك / Subscription store state and paywall UI (documented)
- `ABUILD-13` بناء موقع Wix هيدلس من وصفات SDK / Wix headless site build from SDK recipes (documented)
- `ABUILD-14` حلقة مراجع شجرة الوصولية لتحكم المتصفح / Accessibility-tree ref loop for browser agents (documented)

### `ABUILD-13` — بناء موقع Wix هيدلس من وصفات SDK / Wix headless site build from SDK recipes

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يجمع موقع Wix هيدلس بربط وحدات SDK جاهزة بدل كتابتها. — Assemble a Wix Headless site by wiring shipped verified @wix/sdk modules and REST scaffolds rather than authoring integrations.

**متى:** Building headless storefront, bookings or CMS on Wix; migrating from Shopify or other platforms.

**كيف:** 1) Authenticate to obtain a Wix access token. 2) Use wix-docs to confirm endpoint, method and shape. 3) Wire shipped SDK modules for Stores/Bookings/CMS. 4) For vibe-coded front ends use dependency-free REST scaffolds. 5) For migrations route via replatform modules then quick catalog import adapter with final report.

**المعاملات:** business solutions needed

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** wix · headless · migration · ويكس · ترحيل

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/890-web/2012-heap-snapshot-leaks`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/890-web/2012-heap-snapshot-leaks`

#### 7. قدرات قريبة في العائلة

- `ABUILD-11` حالة الاشتراكات وواجهة إدارة الاشتراك / Subscription store state and paywall UI (documented)
- `ABUILD-12` نموذج أولي مؤقت للإجابة عن سؤال / Throwaway prototype to answer one question (documented)
- `ABUILD-14` حلقة مراجع شجرة الوصولية لتحكم المتصفح / Accessibility-tree ref loop for browser agents (documented)
- `ABUILD-15` استنساخ موقع بأدلة المتصفح / Browser-evidence website clone workflow (documented)

### `ABUILD-14` — حلقة مراجع شجرة الوصولية لتحكم المتصفح / Accessibility-tree ref loop for browser agents

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تشغيل متصفح حقيقي عبر لقطات شجرة وصولية مختصرة ومراجع عناصر، مع إعادة اللقطة بعد كل تغيير. — Drive a real browser by taking compact accessibility snapshots with element refs, acting on refs, and re-snapshotting after each DOM change.

**متى:** Task needs clicking/filling/scraping a live JS-rendered page cheaply in tokens.

**كيف:** 1) open URL (daemon starts Chrome). 2) snapshot interactive elements with bounded output. 3) click/fill by ref (@eN or eN), not CSS. 4) re-snapshot after any DOM change since refs move. 5) read text with a size cap. 6) screenshot only for visual or canvas checks. 7) close the session. Chain commands or batch to reuse the daemon.

**المعاملات:** url, output cap, session name

**التثبيت:** npm i -g agent-browser && agent-browser install

**الوسوم:** playwright · snapshot · متصفح · أتمتة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1395-agent-browser/3331-agent-browser`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2464-playwright/9552-playwright`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2923-playwright-cli/12134-playwright-cli`

#### 7. قدرات قريبة في العائلة

- `ABUILD-12` نموذج أولي مؤقت للإجابة عن سؤال / Throwaway prototype to answer one question (documented)
- `ABUILD-13` بناء موقع Wix هيدلس من وصفات SDK / Wix headless site build from SDK recipes (documented)
- `ABUILD-15` استنساخ موقع بأدلة المتصفح / Browser-evidence website clone workflow (documented)
- `ABUILD-16` تصحيح الصفحات الحية عبر Chrome DevTools MCP / Chrome DevTools MCP debugging of live pages (documented)

### `ABUILD-15` — استنساخ موقع بأدلة المتصفح / Browser-evidence website clone workflow

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** إعادة بناء صفحة رئيسية من بيان استخراج مجمد من المتصفح ثم سد الفجوات بمراجعة بصرية. — Rebuild a public home page as a headless frontend from a frozen browser-derived extraction manifest, then close gaps through visual review.

**متى:** Migrating or cloning a site while preserving SEO, assets, interactions.

**كيف:** 1) Resolve source URL, output dir, mode. 2) Capture with a real browser (never HTML-only), freeze extraction manifest and first-viewport evidence. 3) Build only from the frozen manifest. 4) Verify runnable dev/build scripts. 5) Visual compare and gap loop until accepted or done_with_gaps. Stage resources load on demand.

**المعاملات:** source url, mode

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** clone · migration · استنساخ · موقع

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3419-wix/14023-wix-headless-replatform`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3419-wix/14027-rp-source-evidence`

#### 7. قدرات قريبة في العائلة

- `ABUILD-13` بناء موقع Wix هيدلس من وصفات SDK / Wix headless site build from SDK recipes (documented)
- `ABUILD-14` حلقة مراجع شجرة الوصولية لتحكم المتصفح / Accessibility-tree ref loop for browser agents (documented)
- `ABUILD-16` تصحيح الصفحات الحية عبر Chrome DevTools MCP / Chrome DevTools MCP debugging of live pages (documented)
- `ABUILD-17` خط لقطات Playwright داخل حاوية / Containerized Playwright screenshot pipeline (documented)

### `ABUILD-16` — تصحيح الصفحات الحية عبر Chrome DevTools MCP / Chrome DevTools MCP debugging of live pages

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0 / MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** فحص الكونسول والشبكة وDOM للصفحة الحية عبر DevTools MCP أو منفذ CDP لإعادة إنتاج الأخطاء. — Inspect console, network, DOM and performance of a live page through Chrome DevTools MCP or a CDP port to reproduce browser bugs.

**متى:** UI bug that only reproduces in a browser; need console errors or failed requests.

**كيف:** 1) Connect via chrome-devtools MCP or a debugging port (9222; MCP proxy 9224). 2) Navigate, take snapshot, emulate viewport. 3) Read console and network for errors. 4) Reproduce flow with click/fill. 5) Screenshot before and after fix. 6) Fix, reload, re-verify. For a user's own Chrome, ask before attaching.

**المعاملات:** debug port, url

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** devtools · CDP · تصحيح · شبكة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3416-chrome-devtools/13989-chrome-devtools`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1219-chrome-cdp/2901-chrome-cdp`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2759-charly-selkies/10880-chrome-devtools-mcp`

#### 7. قدرات قريبة في العائلة

- `ABUILD-14` حلقة مراجع شجرة الوصولية لتحكم المتصفح / Accessibility-tree ref loop for browser agents (documented)
- `ABUILD-15` استنساخ موقع بأدلة المتصفح / Browser-evidence website clone workflow (documented)
- `ABUILD-17` خط لقطات Playwright داخل حاوية / Containerized Playwright screenshot pipeline (documented)
- `ABUILD-18` تشغيل متصفحات معزولة عبر بروتوكولاتها / Isolated headless Chrome/Firefox/Safari drivers over native protocols (documented)

### `ABUILD-17` — خط لقطات Playwright داخل حاوية / Containerized Playwright screenshot pipeline

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** توليد لقطات توثيق قابلة للتكرار داخل Docker بواسطة Playwright وتنظيف اللقطات الزائدة. — Generate reproducible README or doc screenshots in Docker with Playwright, then clean up stray screenshots.

**متى:** Need deterministic screenshots in CI or for custom-node packs.

**كيف:** 1) Build a Docker image with Playwright and fonts. 2) Mount the app, start it, wait on ready selector. 3) Run a script that captures each target at a fixed viewport. 4) Write to an output dir with a manifest. 5) Optionally compare to baselines for visual regression. 6) Move leftover session screenshots to trash only with approval.

**المعاملات:** viewport, targets

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** screenshot · docker · لقطات · حاوية

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `docker` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2142-comfyui-plugin/7662-comfyui-screenshot-pipeline`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/861-visual-regression/1890-visual-reg`

#### 7. قدرات قريبة في العائلة

- `ABUILD-15` استنساخ موقع بأدلة المتصفح / Browser-evidence website clone workflow (documented)
- `ABUILD-16` تصحيح الصفحات الحية عبر Chrome DevTools MCP / Chrome DevTools MCP debugging of live pages (documented)
- `ABUILD-18` تشغيل متصفحات معزولة عبر بروتوكولاتها / Isolated headless Chrome/Firefox/Safari drivers over native protocols (documented)
- `ABUILD-19` جلسات Playwright مسماة بمخرجات على القرص / Named-session Playwright CLI with disk artifacts (documented)

### `ABUILD-18` — تشغيل متصفحات معزولة عبر بروتوكولاتها / Isolated headless Chrome/Firefox/Safari drivers over native protocols

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** فتح الصفحات في متصفح بلا واجهة بملف مؤقت وقراءتها والنقر وأخذ لقطات بأوامر قصيرة. — Open pages in throwaway-profile headless Chrome (CDP), Firefox (Marionette) or Safari (safaridriver) and read, click, eval and screenshot with one-line commands.

**متى:** Cross-browser preview, no Playwright available, or must not touch the user's browser.

**كيف:** 1) open <url> (new throwaway profile; --headed only if watched; --size). 2) text/status for state. 3) click/type/press by CSS selector. 4) eval expression, wait expression with timeout. 5) screenshot --output [--full]. 6) With several instances pass --id. 7) close deletes the profile. Use herdr-browser inside Herdr for console/network.

**المعاملات:** url, size, id

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** CDP · firefox · safari · بروتوكول

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1449-browsers/3536-chrome`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1449-browsers/3537-firefox`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1449-browsers/3538-safari`

#### 7. قدرات قريبة في العائلة

- `ABUILD-16` تصحيح الصفحات الحية عبر Chrome DevTools MCP / Chrome DevTools MCP debugging of live pages (documented)
- `ABUILD-17` خط لقطات Playwright داخل حاوية / Containerized Playwright screenshot pipeline (documented)
- `ABUILD-19` جلسات Playwright مسماة بمخرجات على القرص / Named-session Playwright CLI with disk artifacts (documented)
- `ABUILD-20` كتابة اختبارات E2E مع فحص الوصولية والأداء / Playwright E2E authoring with lint, a11y and CWV scans (documented)

### `ABUILD-19` — جلسات Playwright مسماة بمخرجات على القرص / Named-session Playwright CLI with disk artifacts

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT AND Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تشغيل فحوص E2E في جلسات مسماة تكتب اللقطات والتتبع إلى القرص وتعيد المسارات فقط. — Run live E2E checks in named headless sessions that write snapshots, screenshots, traces and console logs to disk and return only paths.

**متى:** Smoke tests, evidence for a PR, auth-state reuse, network mocking.

**كيف:** 1) kill-all stale sessions. 2) open -s=<flow> <url>. 3) snapshot to YAML, read the file for refs. 4) click/fill by ref (fill --submit). 5) screenshot with a descriptive --filename. 6) console to summarize errors; use tracing/video and saved auth state when needed. 7) close; gitignore .playwright-cli/. Judge layout from the screenshot, not the YAML.

**المعاملات:** session name, filename

**التثبيت:** npm install -g @playwright/cli

**الوسوم:** playwright · e2e · جلسات · اختبار

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2464-playwright/9552-playwright`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2464-playwright/9553-playwright`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1251-playwright/2931-playwright`

#### 7. قدرات قريبة في العائلة

- `ABUILD-17` خط لقطات Playwright داخل حاوية / Containerized Playwright screenshot pipeline (documented)
- `ABUILD-18` تشغيل متصفحات معزولة عبر بروتوكولاتها / Isolated headless Chrome/Firefox/Safari drivers over native protocols (documented)
- `ABUILD-20` كتابة اختبارات E2E مع فحص الوصولية والأداء / Playwright E2E authoring with lint, a11y and CWV scans (documented)
- `ABUILD-21` رفع ملف عبر Playwright MCP لحقل مخفي / Playwright MCP hidden file-input upload workaround (documented)

### `ABUILD-20` — كتابة اختبارات E2E مع فحص الوصولية والأداء / Playwright E2E authoring with lint, a11y and CWV scans

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** كتابة اختبارات Playwright بنمط Page Object ثم فحص الوصولية وCWV بمخرجات JSON. — Author Playwright E2E scripts with Page Objects, auth reuse and mocks, then run scripted axe a11y and Core Web Vitals scans with JSON output.

**متى:** Setting up or extending E2E suites with evidence and quality gates.

**كيف:** 1) Init runtime in the app (init_project script). 2) Classify page roles from a11y tree. 3) Record with codegen, then refactor into Page Objects with stored auth state and API mocks. 4) Lint scenario by AST; check app readiness. 5) run_a11y_scan (axe) with fail-on-violations exit 1. 6) check_cwv for LCP/CLS/TTFB with fail-on-poor. 7) Keep video/trace evidence; scripts print one JSON on stdout.

**المعاملات:** base url, thresholds

**التثبيت:** pip install playwright && playwright install chromium

**الوسوم:** E2E · a11y · اختبار · وصولية

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1329-playwright-kit/2981-playwright-kit-ops`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1329-playwright-kit/2979-playwright-authoring`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1369-boss/3164-qa-e2e-playwright`

#### 7. قدرات قريبة في العائلة

- `ABUILD-18` تشغيل متصفحات معزولة عبر بروتوكولاتها / Isolated headless Chrome/Firefox/Safari drivers over native protocols (documented)
- `ABUILD-19` جلسات Playwright مسماة بمخرجات على القرص / Named-session Playwright CLI with disk artifacts (documented)
- `ABUILD-21` رفع ملف عبر Playwright MCP لحقل مخفي / Playwright MCP hidden file-input upload workaround (documented)
- `ABUILD-22` إثبات السلوك المعروض بحكم نجح/فشل/معطل / Rendered-behavior proof with pass/fail/blocked verdict (documented)

### `ABUILD-21` — رفع ملف عبر Playwright MCP لحقل مخفي / Playwright MCP hidden file-input upload workaround

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** رفع ملف عندما يكون حقل الإدخال مخفيا وتفشل أداة الرفع. — Upload a file when the input is hidden and the MCP upload tool times out.

**متى:** MCP upload tool times out on a hidden input.

**كيف:** Locate the hidden input, expose it or target it directly, set files programmatically, then dispatch change events and verify the page shows the file.

**المعاملات:** file path

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** upload · MCP · رفع · playwright

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3342-playwright-mcp-upload-hidden-file-input/13856-playwright-mcp-upload-hidden-file-input`

#### 7. قدرات قريبة في العائلة

- `ABUILD-19` جلسات Playwright مسماة بمخرجات على القرص / Named-session Playwright CLI with disk artifacts (documented)
- `ABUILD-20` كتابة اختبارات E2E مع فحص الوصولية والأداء / Playwright E2E authoring with lint, a11y and CWV scans (documented)
- `ABUILD-22` إثبات السلوك المعروض بحكم نجح/فشل/معطل / Rendered-behavior proof with pass/fail/blocked verdict (documented)
- `ABUILD-23` فحص جودة الواجهة بثلاثة عروض / Three-width responsive browser QA report (documented)

### `ABUILD-22` — إثبات السلوك المعروض بحكم نجح/فشل/معطل / Rendered-behavior proof with pass/fail/blocked verdict

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** إثبات ادعاء واجهة في متصفح حقيقي بأرخص وسيلة متاحة والإبلاغ بنجاح أو فشل أو تعطل مع الأدلة. — Prove a UI claim in a real browser using the cheapest available runtime and report pass, fail or blocked with evidence.

**متى:** User asks to verify, screenshot or record a flow without wanting permanent tests.

**كيف:** 1) Pick runtime: session browser tools, project runner, bundled Playwright scripts, else report blocked. 2) Reuse a running dev server; ask if several. 3) Use role/label/text/testid locators, wait on observable state, never fixed sleeps. 4) screenshot-url/sequence scripts emit a JSON manifest (viewport, console errors, failed network, status>=400). 5) Write temp scripts under /tmp/playwright-*. 6) After two failed attempts, save evidence and stop.

**المعاملات:** url, ready selector, out path

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** verification · screenshot · دليل · واجهة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/112-browser/286-browser-automation`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/238-browser/775-browser`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2111-frontend-dev-kit/7511-browser-debug`

#### 7. قدرات قريبة في العائلة

- `ABUILD-20` كتابة اختبارات E2E مع فحص الوصولية والأداء / Playwright E2E authoring with lint, a11y and CWV scans (documented)
- `ABUILD-21` رفع ملف عبر Playwright MCP لحقل مخفي / Playwright MCP hidden file-input upload workaround (documented)
- `ABUILD-23` فحص جودة الواجهة بثلاثة عروض / Three-width responsive browser QA report (documented)
- `ABUILD-24` ضبط مجمع الاتصالات وموثوقية قاعدة البيانات / Connection pool sizing and DB reliability playbook (documented)

### `ABUILD-23` — فحص جودة الواجهة بثلاثة عروض / Three-width responsive browser QA report

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** فحص الصفحات المتغيرة عند 375 و768 و1280 بكسل وإخراج جدول بالمشاكل. — Check changed pages at 375, 768 and 1280 px in a real browser and tabulate layout, console and network findings.

**متى:** After a frontend change, before merge, or when asked to check how a page looks.

**كيف:** 1) Map changed files to routes (or take the given URL). 2) curl -sI; start dev server if nothing answers. 3) Open a NEW tab; resize or emulate 375x812x2 mobile, 768, 1280. 4) Screenshot and read each; look for overflow, clipping, overlap, tiny tap targets, uncollapsed nav, broken images. 5) Check console and failed requests; ignore third-party analytics. 6) Exercise any new interaction once. 7) Output page-by-width table; fix only if asked; close tabs.

**المعاملات:** url/path, optional fix

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** responsive · QA · تجاوب · فحص

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `network` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3166-browser-qa/13495-browser-qa`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3165-browser-compat/13494-browser-compat`

#### 7. قدرات قريبة في العائلة

- `ABUILD-21` رفع ملف عبر Playwright MCP لحقل مخفي / Playwright MCP hidden file-input upload workaround (documented)
- `ABUILD-22` إثبات السلوك المعروض بحكم نجح/فشل/معطل / Rendered-behavior proof with pass/fail/blocked verdict (documented)
- `ABUILD-24` ضبط مجمع الاتصالات وموثوقية قاعدة البيانات / Connection pool sizing and DB reliability playbook (documented)
- `ABUILD-25` نص نسخ احتياطي لقاعدة البيانات مع الاحتفاظ والتشفير / Database backup script with retention and encryption (documented)

### `ABUILD-24` — ضبط مجمع الاتصالات وموثوقية قاعدة البيانات / Connection pool sizing and DB reliability playbook

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** حدد حجم مجمع الاتصالات وعزل المعاملات وتشخيص حوادث قاعدة البيانات. — Size pools (PgBouncer or app-level), choose isolation, triage live DB incidents and design HA from RPO/RTO.

**متى:** Too many connections, deadlocks, failover design, outage.

**كيف:** 1) Size pool from cores and max_connections, avoid per-instance over-allocation. 2) Serverless: pooled endpoint or Prisma limit. 3) Pick isolation deliberately; detect deadlocks. 4) Triage: classify latency vs errors vs saturation, mitigate, then root cause. 5) Choose replica type and failover from RPO/RTO.

**المعاملات:** RPO, RTO, load

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pool · ha · incident · اتصالات

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `ABUILD-22` إثبات السلوك المعروض بحكم نجح/فشل/معطل / Rendered-behavior proof with pass/fail/blocked verdict (documented)
- `ABUILD-23` فحص جودة الواجهة بثلاثة عروض / Three-width responsive browser QA report (documented)
- `ABUILD-25` نص نسخ احتياطي لقاعدة البيانات مع الاحتفاظ والتشفير / Database backup script with retention and encryption (documented)
- `ABUILD-26` تطور مخططات الأحداث وKafka / Event schema evolution and Kafka platform playbook (documented)

### `ABUILD-25` — نص نسخ احتياطي لقاعدة البيانات مع الاحتفاظ والتشفير / Database backup script with retention and encryption

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** ولّد نصوص نسخ احتياطي مجدولة مع ضغط وتشفير وسياسة احتفاظ وخطوات استعادة. — Generate scheduled backup scripts for Postgres, MySQL, MongoDB, SQLite with compression, GPG encryption, retention and restore steps.

**متى:** Disaster recovery, cron backups, restore drills.

**كيف:** 1) set -euo pipefail script with timestamped file. 2) pg_dump --format=custom --compress=9 / mysqldump / mongodump / sqlite .backup. 3) Optional gpg --symmetric AES256 with key file, delete plaintext. 4) Cron schedule plus retention prune by age. 5) Write and test a restore procedure; verify checksum. 6) Litestream for continuous SQLite.

**المعاملات:** engine, schedule, retention days

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** backup · restore · نسخ احتياطي · استعادة

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1686-database-backup-automator/4690-automating-database-backups`

#### 7. قدرات قريبة في العائلة

- `ABUILD-23` فحص جودة الواجهة بثلاثة عروض / Three-width responsive browser QA report (documented)
- `ABUILD-24` ضبط مجمع الاتصالات وموثوقية قاعدة البيانات / Connection pool sizing and DB reliability playbook (documented)
- `ABUILD-26` تطور مخططات الأحداث وKafka / Event schema evolution and Kafka platform playbook (documented)
- `ABUILD-27` قواعد Postgres وRedis المُدارة على المنصات / Managed Postgres and Redis on hosting platforms (documented)

### `ABUILD-26` — تطور مخططات الأحداث وKafka / Event schema evolution and Kafka platform playbook

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** طوّر مخططات الأحداث بأمان باستخدام أنماط التوافق وشغّل Kafka بموثوقية. — Evolve Avro/Protobuf/JSON schemas safely with registry compatibility modes and run Kafka reliably.

**متى:** Changing event contracts, Kafka partitioning, streaming ingest.

**كيف:** 1) Choose compatibility mode (backward/forward/full). 2) Add optional fields with defaults, never reuse field numbers. 3) Register and test with consumers first. 4) Partition for needed ordering (order is per-partition). 5) Dedup and batch ingestion into sinks.

**المعاملات:** format, mode

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** kafka · avro · schema · أحداث

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `ABUILD-24` ضبط مجمع الاتصالات وموثوقية قاعدة البيانات / Connection pool sizing and DB reliability playbook (documented)
- `ABUILD-25` نص نسخ احتياطي لقاعدة البيانات مع الاحتفاظ والتشفير / Database backup script with retention and encryption (documented)
- `ABUILD-27` قواعد Postgres وRedis المُدارة على المنصات / Managed Postgres and Redis on hosting platforms (documented)
- `ABUILD-28` دليل الحوادث: احتواء وتشخيص واستعادة / Incident runbook: contain, diagnose, recover (documented)

### `ABUILD-27` — قواعد Postgres وRedis المُدارة على المنصات / Managed Postgres and Redis on hosting platforms

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يجهز تخزين Render وVercel وSealos بسلاسل اتصال صحيحة. — Provision Render, Vercel and Sealos storage with correct connection strings.

**متى:** deploying with managed DB/KV/blob

**كيف:** 1) Choose store: Postgres, Key Value, Blob, Edge Config. 2) Internal vs external connection string. 3) Respect creation constraints and autoscaling. 4) Use Marketplace Neon/Upstash on Vercel. 5) Set env secrets.

**المعاملات:** platform

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** render · vercel · استضافة

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/889-render/2010-render-postgres`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2722-vercel/10571-vercel-storage`

#### 7. قدرات قريبة في العائلة

- `ABUILD-25` نص نسخ احتياطي لقاعدة البيانات مع الاحتفاظ والتشفير / Database backup script with retention and encryption (documented)
- `ABUILD-26` تطور مخططات الأحداث وKafka / Event schema evolution and Kafka platform playbook (documented)
- `ABUILD-28` دليل الحوادث: احتواء وتشخيص واستعادة / Incident runbook: contain, diagnose, recover (documented)
- `ABUILD-29` تصميم المراقبة: الإشارات الذهبية والتنبيهات / Observability design: golden signals and alerts (documented)

### `ABUILD-28` — دليل الحوادث: احتواء وتشخيص واستعادة / Incident runbook: contain, diagnose, recover

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** إدارة حادث إنتاجي عبر الفرز والاحتواء والسبب الجذري والإصلاح مع التراجع والمطابقة. — Run a production incident through triage, containment, root cause, fix with rollback, and reconciliation.

**متى:** outage, webhook or sync failure, degraded integration

**كيف:** 1) Triage severity and blast radius. 2) Contain (pause jobs, fallback). 3) Gather logs/metrics bundle. 4) Identify root cause and propose fix with rollback. 5) Reconcile missed data/webhooks. 6) Post-incident review.

**المعاملات:** service

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** incident · runbook · recovery · حوادث · استعادة

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1897-ramp-pack/6601-ramp-incident-runbook`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/4524-tonone/4524-vigil-incident`

#### 7. قدرات قريبة في العائلة

- `ABUILD-26` تطور مخططات الأحداث وKafka / Event schema evolution and Kafka platform playbook (documented)
- `ABUILD-27` قواعد Postgres وRedis المُدارة على المنصات / Managed Postgres and Redis on hosting platforms (documented)
- `ABUILD-29` تصميم المراقبة: الإشارات الذهبية والتنبيهات / Observability design: golden signals and alerts (documented)
- `ABUILD-30` استطلاع البنية وتدقيق التكلفة / Infra reconnaissance and cost audit (documented)

### `ABUILD-29` — تصميم المراقبة: الإشارات الذهبية والتنبيهات / Observability design: golden signals and alerts

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** اختيار مقاييس RED وUSE والإشارات الذهبية وكتابة PromQL وتنبيهات قابلة للتنفيذ. — Choose RED/USE/golden-signal metrics, write PromQL, and define actionable alerts with for-duration, severity and runbook links.

**متى:** set up monitoring, dashboards, SLOs, instrument a service, incident readiness

**كيف:** 1) RED at the edge, USE for infra. 2) PromQL: 5xx ratio via rate over 5m, p95 via histogram_quantile. 3) rate window at least 4x scrape interval. 4) Every alert has for: (no flapping), severity, runbook link and an action. 5) Add OpenTelemetry traces, structured logs, SLO/error budget.

**المعاملات:** stack

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** observability · prometheus · slo · مراقبة · تنبيهات

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2965-pwdev-devops/12477-observability`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/4525-tonone/4525-vigil-instrument`

#### 7. قدرات قريبة في العائلة

- `ABUILD-27` قواعد Postgres وRedis المُدارة على المنصات / Managed Postgres and Redis on hosting platforms (documented)
- `ABUILD-28` دليل الحوادث: احتواء وتشخيص واستعادة / Incident runbook: contain, diagnose, recover (documented)
- `ABUILD-30` استطلاع البنية وتدقيق التكلفة / Infra reconnaissance and cost audit (documented)
- `ABUILD-31` تصميم مكوّن متاح افتراضيا / Accessible-by-default component pattern design (documented)

### `ABUILD-30` — استطلاع البنية وتدقيق التكلفة / Infra reconnaissance and cost audit

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يجرد الموارد ويرسم خط CI/CD ويعد خطة تحسين التكلفة. — Inventory cloud resources, map pipelines and risks, and produce a costed optimization plan.

**متى:** inherit infra, audit spend

**كيف:** 1) Inventory resources and connections. 2) Flag risks. 3) Map triggers, build, test, deploy. 4) Rank cost levers. 5) Estimate savings.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** infra · cost · audit · تكلفة

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/*/4416-forge-recon`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/*/4412-forge-cost`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/*/4497-relay-recon`

#### 7. قدرات قريبة في العائلة

- `ABUILD-28` دليل الحوادث: احتواء وتشخيص واستعادة / Incident runbook: contain, diagnose, recover (documented)
- `ABUILD-29` تصميم المراقبة: الإشارات الذهبية والتنبيهات / Observability design: golden signals and alerts (documented)
- `ABUILD-31` تصميم مكوّن متاح افتراضيا / Accessible-by-default component pattern design (documented)
- `ABUILD-32` إعداد هوية العلامة مع فحص التباين / Brand palette onboarding with WCAG gate (documented)

### `ABUILD-31` — تصميم مكوّن متاح افتراضيا / Accessible-by-default component pattern design

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تصميم مكونات بعناصر دلالية أولا وARIA عند الحاجة فقط مع إدارة لوحة المفاتيح والتركيز. — Design components with semantic HTML first, ARIA only where needed, keyboard and focus management.

**متى:** Building dialogs, menus, tabs, forms or reviewing ARIA misuse.

**كيف:** 1) Pick native element before ARIA. 2) Define roles, name and state. 3) Specify keyboard map and focus trap/return. 4) Check visible focus and 2.5.8 target size. 5) Write tests (axe/pa11y, keyboard walk-through).

**المعاملات:** component type

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** aria · keyboard · focus · لوحة المفاتيح

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:pa11y` ← npm ls pa11y أو وجود node_modules/pa11y
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/8453`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/7559`

#### 7. قدرات قريبة في العائلة

- `ABUILD-29` تصميم المراقبة: الإشارات الذهبية والتنبيهات / Observability design: golden signals and alerts (documented)
- `ABUILD-30` استطلاع البنية وتدقيق التكلفة / Infra reconnaissance and cost audit (documented)
- `ABUILD-32` إعداد هوية العلامة مع فحص التباين / Brand palette onboarding with WCAG gate (documented)
- `ABUILD-33` حسابات الألوان وتخطيط CSS مع التباين / Color and CSS layout math with contrast (documented)

### `ABUILD-32` — إعداد هوية العلامة مع فحص التباين / Brand palette onboarding with WCAG gate

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** التقط ألوان وخطوط العلامة مرة واحدة واشتق لوحة من 12 رمزاً وارفض ما يفشل بتباين AA. — Capture brand colors and fonts once, derive a 12-token palette, and refuse values failing WCAG AA contrast.

**متى:** Converting markdown or reports to branded HTML, or setting a brand default.

**كيف:** 1. Ask ~10 questions: output dir, primary/accent HEX, heading/body Google fonts, style (editorial/technical/minimal/playful), code theme, TOC mode. 2. Validate body-text and link contrast >= 4.5:1; reject the save otherwise. 3. Derive 12 CSS custom properties from HSL. 4. Merge config project > global > defaults. 5. Every converter must read the config and visibly change output.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** brand · contrast · palette · هوية

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:axe` ← npm ls axe أو وجود node_modules/axe
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/191-markdown-html-skills/564-design-system`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/191-markdown-html-skills/565-markdown-html-orchestrator`

#### 7. قدرات قريبة في العائلة

- `ABUILD-30` استطلاع البنية وتدقيق التكلفة / Infra reconnaissance and cost audit (documented)
- `ABUILD-31` تصميم مكوّن متاح افتراضيا / Accessible-by-default component pattern design (documented)
- `ABUILD-33` حسابات الألوان وتخطيط CSS مع التباين / Color and CSS layout math with contrast (documented)
- `ABUILD-34` التصميم عبر قيود مكانية وطباعية صريحة / Design by explicit spatial and type constraints (documented)

### `ABUILD-33` — حسابات الألوان وتخطيط CSS مع التباين / Color and CSS layout math with contrast

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** اشتقاق ألوان آمنة للتباين وإحداثيات الشبكة وأحجام clamp مرنة بصيغ صريحة. — Derive OKLCH/contrast-safe palettes, grid coordinates and fluid clamp() sizes with explicit formulas.

**متى:** Tuning palettes, fluid type, responsive breakpoints or grid placement.

**كيف:** 1) Convert colors to OKLCH/LAB, compute luminance contrast (4.5:1 text, 3:1 large/UI). 2) Fluid size: clamp(min, preferred vw+rem, max). 3) Grid line math with negative indexes and spans. 4) Verify at viewport extremes.

**المعاملات:** palette, viewport range

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** css · oklch · contrast · تباين

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2199-lvtd-skills/8013-color-math-accessibility`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/8145`

#### 7. قدرات قريبة في العائلة

- `ABUILD-31` تصميم مكوّن متاح افتراضيا / Accessible-by-default component pattern design (documented)
- `ABUILD-32` إعداد هوية العلامة مع فحص التباين / Brand palette onboarding with WCAG gate (documented)
- `ABUILD-34` التصميم عبر قيود مكانية وطباعية صريحة / Design by explicit spatial and type constraints (documented)
- `ABUILD-35` نقد التصميم وتسليم المطورين وتدقيق النظام / Design critique, handoff and system audit (documented)

### `ABUILD-34` — التصميم عبر قيود مكانية وطباعية صريحة / Design by explicit spatial and type constraints

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تثبيت الشبكة والزوايا والحشو والخطوط واللون المميز على قيم قليلة لتجنب الشكل العام الممل. — Lock the grid, radii, padding, fonts and accent to a few legal values so generated UI avoids generic look.

**متى:** Building or restyling any UI where output looks generic.

**كيف:** 1) Use project tokens if present. 2) 8px grid, 24px outer padding/radius, 4px half-step only when 8 overflows. 3) Concentric radii: inner = outer - inset (24/8/16). 4) Max 2 families, 2-3 weights and sizes per component; mono only for machine text. 5) One accent per view. 6) Build one component at a time, give feedback as constraints.

**المعاملات:** grid, radius

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ui · constraints · typography · طباعة

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/96-design-constraints/205-design-constraints`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2905`

#### 7. قدرات قريبة في العائلة

- `ABUILD-32` إعداد هوية العلامة مع فحص التباين / Brand palette onboarding with WCAG gate (documented)
- `ABUILD-33` حسابات الألوان وتخطيط CSS مع التباين / Color and CSS layout math with contrast (documented)
- `ABUILD-35` نقد التصميم وتسليم المطورين وتدقيق النظام / Design critique, handoff and system audit (documented)
- `ABUILD-36` اشتقاق وترقية نظام التصميم / Design-system retrofit and derivation workflow (documented)

### `ABUILD-35` — نقد التصميم وتسليم المطورين وتدقيق النظام / Design critique, handoff and system audit

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0 / MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** نقد منظم للتصميم وإعداد مواصفات التسليم وتدقيق اتساق نظام التصميم. — Run structured design critique, produce developer handoff specs and audit design system consistency.

**متى:** Reviewing mockups, preparing handoff, or checking hardcoded values.

**كيف:** 1) Critique: usability, hierarchy, consistency with prioritized findings. 2) Handoff: spacing, tokens, states, responsive, edge cases. 3) System audit: naming inconsistencies, hardcoded values, missing states. 4) Component spec: variants, sizes, states. 5) Offer 2-3 variants with tradeoffs.

**المعاملات:** design source

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** critique · handoff · design-system · نقد

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/949`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/950`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3174`

#### 7. قدرات قريبة في العائلة

- `ABUILD-33` حسابات الألوان وتخطيط CSS مع التباين / Color and CSS layout math with contrast (documented)
- `ABUILD-34` التصميم عبر قيود مكانية وطباعية صريحة / Design by explicit spatial and type constraints (documented)
- `ABUILD-36` اشتقاق وترقية نظام التصميم / Design-system retrofit and derivation workflow (documented)
- `ABUILD-37` رموز التصميم DTCG لكل المنصات / DTCG design tokens multi-platform export (documented)

### `ABUILD-36` — اشتقاق وترقية نظام التصميم / Design-system retrofit and derivation workflow

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** اشتق نظام تصميم وانقل CSS الحالي إلى تصنيفه دون تغيير بصري. — Derive a design system, lift ad-hoc CSS into its taxonomy, and render to targets without visual change.

**متى:** Design direction open or existing CSS needs systematizing.

**كيف:** 1. Survey current token/tooling state. 2. If direction is open, spread divergent idioms; if settled, echo variations. 3. Retrofit existing CSS into the taxonomy with zero visual change. 4. Emit to targets via committed formatters. 5. Report status of artefacts.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** design-system · retrofit · taxonomy · نظام

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/matrize/846-matrize-retrofit`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/matrize/843-matrize-emit`

#### 7. قدرات قريبة في العائلة

- `ABUILD-34` التصميم عبر قيود مكانية وطباعية صريحة / Design by explicit spatial and type constraints (documented)
- `ABUILD-35` نقد التصميم وتسليم المطورين وتدقيق النظام / Design critique, handoff and system audit (documented)
- `ABUILD-37` رموز التصميم DTCG لكل المنصات / DTCG design tokens multi-platform export (documented)
- `ABUILD-38` تدقيق تصميم الواجهة بالأدلة / Evidence-backed frontend design audit (documented)

### `ABUILD-37` — رموز التصميم DTCG لكل المنصات / DTCG design tokens multi-platform export

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under Apache-2.0 / MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** اكتب مصدر رموز DTCG واحد وصدّره إلى Tailwind وCSS وSwiftUI وCompose وWinUI. — Author one W3C DTCG token JSON and export it to Tailwind, CSS variables, SwiftUI, Compose and WinUI.

**متى:** User asks for design tokens, a theme system, or one token source for web and native.

**كيف:** 1. Write tokens with $value/$type/$description (color, dimension, fontFamily, duration, shadow, typography). 2. Layer primitive, semantic, component tokens, aliasing via {color.brand.primary}. 3. Translate with a script, never by hand (Tailwind v4 @theme, :root vars, Compose ColorScheme, WinUI ResourceDictionary). 4. Audit for circular refs, raw-vs-semantic naming, single-platform drift. 5. Skip tokens for bespoke art-directed pages.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** design-tokens · DTCG · theming · رموز التصميم

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1394-stark/3327-design-tokens`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3529-ui-design/14307-design-system-patterns`

#### 7. قدرات قريبة في العائلة

- `ABUILD-35` نقد التصميم وتسليم المطورين وتدقيق النظام / Design critique, handoff and system audit (documented)
- `ABUILD-36` اشتقاق وترقية نظام التصميم / Design-system retrofit and derivation workflow (documented)
- `ABUILD-38` تدقيق تصميم الواجهة بالأدلة / Evidence-backed frontend design audit (documented)
- `ABUILD-39` استخراج بصمة التصميم من موقع حي / Extract Design DNA from live website (documented)

### `ABUILD-38` — تدقيق تصميم الواجهة بالأدلة / Evidence-backed frontend design audit

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** نفّذ تدقيقاً حتمياً لمصدر الواجهة وأبلغ بنتائج مرتبطة بالملفات. — Run a deterministic source audit of React/Tailwind UI and report file-anchored findings by user impact.

**متى:** Reviewing or changing a React, Next.js, Tailwind or shadcn interface.

**كيف:** 1. Read repo instructions and pick the route/component. 2. Run a static diagnose over the repo with JSON output and no write. 3. Group findings by user impact (a11y, hierarchy, tokens, states, responsive). 4. Verify each fix against the cited file and local tokens. 5. Re-run; report before/after score, omissions, remaining risk as a priority/evidence/change table.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** audit · UI · frontend · تدقيق

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:react` ← npm ls react أو وجود node_modules/react
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3029-memoire/12946-audit-frontend-design`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3029-memoire/12950-remember-design-system`

#### 7. قدرات قريبة في العائلة

- `ABUILD-36` اشتقاق وترقية نظام التصميم / Design-system retrofit and derivation workflow (documented)
- `ABUILD-37` رموز التصميم DTCG لكل المنصات / DTCG design tokens multi-platform export (documented)
- `ABUILD-39` استخراج بصمة التصميم من موقع حي / Extract Design DNA from live website (documented)
- `ABUILD-40` من ملف Figma إلى رموز وأصول وكود / Figma file to tokens, assets and code (documented)

### `ABUILD-39` — استخراج بصمة التصميم من موقع حي / Extract Design DNA from live website

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** استخراج الأنماط المحسوبة من موقع حي إلى ملف تصميم منظم JSON مع استنساخ اختياري. — Pull exact computed styles from a live site into a structured design profile JSON and optionally clone it.

**متى:** Asked to replicate, analyze or reverse a site's visual style.

**كيف:** 1) Open URL in browser tool, inject JS reading getComputedStyle for colors, fonts, spacing, radii, shadows, motion. 2) Scan code for canvas/WebGL/shader effects. 3) Judge mood and layout by eye. 4) Write DNA JSON (150+ field schema), --dna-only stops here. 5) Optionally generate code and compare screenshots.

**المعاملات:** urls, mode

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** design-dna · clone · scraping · استنساخ

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3594-design-clone/14410-design-clone`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2673-claude-octopus/10214-skill-extract`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2042`

#### 7. قدرات قريبة في العائلة

- `ABUILD-37` رموز التصميم DTCG لكل المنصات / DTCG design tokens multi-platform export (documented)
- `ABUILD-38` تدقيق تصميم الواجهة بالأدلة / Evidence-backed frontend design audit (documented)
- `ABUILD-40` من ملف Figma إلى رموز وأصول وكود / Figma file to tokens, assets and code (documented)
- `ABUILD-41` قراءة Figma عبر MCP أو REST / Figma read via MCP or REST fallback (documented)

### `ABUILD-40` — من ملف Figma إلى رموز وأصول وكود / Figma file to tokens, assets and code

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** استخدام واجهة Figma لاستخراج الرموز وتصدير الأصول ثم تنفيذ مكونات من رابط Figma. — Use the Figma REST API to extract tokens and export assets, then implement components from a Figma URL.

**متى:** Given a Figma URL or asked to sync tokens in CI.

**كيف:** 1) Auth with scoped token. 2) GET file, walk styles for colors/type/spacing. 3) Export images by node id (svg/png) with batching. 4) Respect rate limits with exponential backoff and caching. 5) Map to tokens and components. 6) Optionally CI sync job.

**المعاملات:** file key

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** figma · tokens · export · فيجما

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3252`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/5606`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/5625`

#### 7. قدرات قريبة في العائلة

- `ABUILD-38` تدقيق تصميم الواجهة بالأدلة / Evidence-backed frontend design audit (documented)
- `ABUILD-39` استخراج بصمة التصميم من موقع حي / Extract Design DNA from live website (documented)
- `ABUILD-41` قراءة Figma عبر MCP أو REST / Figma read via MCP or REST fallback (documented)
- `ABUILD-42` من Figma إلى كود مطابق / Figma to pixel-exact code plan (documented)

### `ABUILD-41` — قراءة Figma عبر MCP أو REST / Figma read via MCP or REST fallback

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** جلب لقطات وبنية ومتغيرات من رابط Figma عبر MCP ثم REST. — Pull screenshots, structure and variables from a Figma URL using MCP first then REST with a token.

**متى:** User supplies Figma link; need tokens or frames for implementation.

**كيف:** 1) Parse file key and node-id (convert - to :). 2) Try Figma MCP get_metadata; authenticate if needed. 3) Else require FIGMA_PAT (file_content:read) and stop if missing. 4) Discover pages/frames. 5) Export frames and variables for downstream skills.

**المعاملات:** figma url

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** figma · mcp · استيراد تصميم · tokens

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3009-uxd-design/12857-uxd-figma-read`

#### 7. قدرات قريبة في العائلة

- `ABUILD-39` استخراج بصمة التصميم من موقع حي / Extract Design DNA from live website (documented)
- `ABUILD-40` من ملف Figma إلى رموز وأصول وكود / Figma file to tokens, assets and code (documented)
- `ABUILD-42` من Figma إلى كود مطابق / Figma to pixel-exact code plan (documented)
- `ABUILD-43` تدقيق أداء الواجهة والاستجابة / Frontend performance and responsive audit (documented)

### `ABUILD-42` — من Figma إلى كود مطابق / Figma to pixel-exact code plan

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** استخرج عقد Figma إلى خطة مقاسة ثم ابنِ وقارن وأصلح. — Extract Figma nodes into a measured plan, build against it, then diff and fix deviations.

**متى:** Implementing or syncing a design from Figma.

**كيف:** 1. Read selected nodes via Figma MCP and write measurements into a plan. 2. Build each node against the embedded specs using project components. 3. Compare the implemented screen with the source and fix deviations. 4. Diff Figma versions to produce a code-update checklist. 5. Map colors/spacing to tokens.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** figma · design-to-code · tokens · فيجما

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/quiver/14453-design`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2998-patternfly/12791-pf-figma-diff`

#### 7. قدرات قريبة في العائلة

- `ABUILD-40` من ملف Figma إلى رموز وأصول وكود / Figma file to tokens, assets and code (documented)
- `ABUILD-41` قراءة Figma عبر MCP أو REST / Figma read via MCP or REST fallback (documented)
- `ABUILD-43` تدقيق أداء الواجهة والاستجابة / Frontend performance and responsive audit (documented)
- `ABUILD-44` اختبار الوصولية بلوحة المفاتيح مباشرة / Live keyboard accessibility test via browser (documented)

### `ABUILD-43` — تدقيق أداء الواجهة والاستجابة / Frontend performance and responsive audit

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** شخّص مشاكل LCP وCLS وINP والاستجابة من المصدر والعرض. — Diagnose LCP, CLS, INP regressions and responsive issues from source and rendered output.

**متى:** Page feels slow, layout shifts, or breakpoints break.

**كيف:** 1. Check LCP image priority, font loading, layout reservations for CLS, long handlers for INP. 2. Audit CSS for fixed widths and missing breakpoints. 3. Render at several viewports and compare. 4. Prefer container queries and fluid type. 5. Report fixes with evidence.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** performance · responsive · CWV · أداء

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/majestic-frontend/8280-frontend-performance`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3529-ui-design/14312-responsive-design`

#### 7. قدرات قريبة في العائلة

- `ABUILD-41` قراءة Figma عبر MCP أو REST / Figma read via MCP or REST fallback (documented)
- `ABUILD-42` من Figma إلى كود مطابق / Figma to pixel-exact code plan (documented)
- `ABUILD-44` اختبار الوصولية بلوحة المفاتيح مباشرة / Live keyboard accessibility test via browser (documented)
- `ABUILD-45` صفحة هبوط فاخرة بحركة GSAP / Premium landing page with GSAP scroll motion (documented)

### `ABUILD-44` — اختبار الوصولية بلوحة المفاتيح مباشرة / Live keyboard accessibility test via browser

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** شغّل الواجهة عبر المتصفح لفحص ترتيب Tab ومصائد التركيز وسلوك المفاتيح. — Drive a running UI with browser automation to check tab order, focus traps and component key behavior.

**متى:** Validating keyboard navigation of an app or component demo.

**كيف:** 1. Open the URL at 1440x900 and screenshot a baseline. 2. Read the accessibility tree; list interactive elements and overlay triggers. 3. Walk ordered criteria: tab order, skip link, focus visible, modal trapping, menu arrows, Escape. 4. Apply component-specific key maps. 5. Report violations with fixes; note manual testing is still needed.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** a11y · keyboard · WCAG · وصولية

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:axe` ← npm ls axe أو وجود node_modules/axe
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2998-patternfly/12754-pf-a11y-keyboard`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2998-patternfly/12753-pf-a11y-audit`

#### 7. قدرات قريبة في العائلة

- `ABUILD-42` من Figma إلى كود مطابق / Figma to pixel-exact code plan (documented)
- `ABUILD-43` تدقيق أداء الواجهة والاستجابة / Frontend performance and responsive audit (documented)
- `ABUILD-45` صفحة هبوط فاخرة بحركة GSAP / Premium landing page with GSAP scroll motion (documented)
- `ABUILD-46` حلقة مقارنة لقطة الصفحة بالتصميم / Screenshot-vs-design pixel diff loop (documented)

### `ABUILD-45` — صفحة هبوط فاخرة بحركة GSAP / Premium landing page with GSAP scroll motion

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** بناء صفحة هبوط بهوية العلامة مع CSS ثلاثي الأبعاد وحركة GSAP بعد مقابلة العلامة. — Build a brand-first single-page landing with 3D CSS and GSAP scroll effects after a brand interview.

**متى:** Requests for marketing or landing pages.

**كيف:** 1) Interview: colors, typography, shape language, audience. 2) Choose art direction from product context. 3) Generate single HTML with GSAP ScrollTrigger and 3D CSS. 4) Audit six conversion dimensions (above-fold, trust, form). 5) Deploy optional.

**المعاملات:** brand brief

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** landing · gsap · marketing · هبوط

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/196-landing/621-landing`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/14160`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/4059`

#### 7. قدرات قريبة في العائلة

- `ABUILD-43` تدقيق أداء الواجهة والاستجابة / Frontend performance and responsive audit (documented)
- `ABUILD-44` اختبار الوصولية بلوحة المفاتيح مباشرة / Live keyboard accessibility test via browser (documented)
- `ABUILD-46` حلقة مقارنة لقطة الصفحة بالتصميم / Screenshot-vs-design pixel diff loop (documented)
- `ABUILD-47` حلقة مقارنة لقطة الشاشة بالمرجع / Screenshot-vs-reference pixel diff loop (documented)

### `ABUILD-46` — حلقة مقارنة لقطة الصفحة بالتصميم / Screenshot-vs-design pixel diff loop

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** مقارنة صفحة منفذة بالتصميم المرجعي وربط الفروق بعناصر مسماة. — Compare a built page to a reference, attributing colour and position diffs to named elements.

**متى:** Matching a page to a mockup, figuring out why a build differs.

**كيف:** 1) Screenshot actual page; save desired.png. 2) Optionally dump DOM bboxes scaled by DPR to elements.json. 3) Run bundled check_design.py with tolerances (deltaE 3, px 2, region 0.5%). 4) Read diff.json: kind color/position per element. 5) Fix, recapture, stop at pass true.

**المعاملات:** actual.png, desired.png

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** visual-diff · screenshot · مقارنة بصرية · qa

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/890-web/2011-check-web-design`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1530-webcraft/4196-ui-screenshots`

#### 7. قدرات قريبة في العائلة

- `ABUILD-44` اختبار الوصولية بلوحة المفاتيح مباشرة / Live keyboard accessibility test via browser (documented)
- `ABUILD-45` صفحة هبوط فاخرة بحركة GSAP / Premium landing page with GSAP scroll motion (documented)
- `ABUILD-47` حلقة مقارنة لقطة الشاشة بالمرجع / Screenshot-vs-reference pixel diff loop (documented)
- `ABUILD-48` معمارية رموز التصميم بثلاث طبقات / Three-tier design token architecture with theming (documented)

### `ABUILD-47` — حلقة مقارنة لقطة الشاشة بالمرجع / Screenshot-vs-reference pixel diff loop

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** قارن الشاشة المبنية بصورة التصميم واحسب فرق اللون الإدراكي لكل عنصر. — Compare a built screen to a design image, mask chrome, and report perceptual delta per element.

**متى:** Matching a screen to a design reference or debugging a mismatch.

**كيف:** 1. Capture actual screenshot beside the desired one. 2. Optionally export element bboxes (scaled by device scale x2/x3) as JSON. 3. Diff with tolerances (deltaE CIE76 ~3, px ~2, region area 0.5%). 4. Mask status bar (~141px) and home indicator (~102px) at x3. 5. Read diff.json pass flag and heatmap PNG; iterate until pass.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** visual-diff · iOS · Figma · مقارنة

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/887-mobile/1996-check-mobile-design`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2370-report-regeneration/9165-report-fidelity-harness`

#### 7. قدرات قريبة في العائلة

- `ABUILD-45` صفحة هبوط فاخرة بحركة GSAP / Premium landing page with GSAP scroll motion (documented)
- `ABUILD-46` حلقة مقارنة لقطة الصفحة بالتصميم / Screenshot-vs-design pixel diff loop (documented)
- `ABUILD-48` معمارية رموز التصميم بثلاث طبقات / Three-tier design token architecture with theming (documented)
- `ABUILD-49` تدقيق إتاحة WCAG 2.2: فحص وإصلاح وتحقق / WCAG 2.2 scan-fix-verify accessibility audit (documented)

### `ABUILD-48` — معمارية رموز التصميم بثلاث طبقات / Three-tier design token architecture with theming

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** هيكلة رموز التصميم أولية ودلالية ومكوّنية مع الثيمات كتبديل قيم دلالية وتصديرها لكل منصة. — Structure tokens as primitive, semantic and component tiers with themes as semantic value swaps, emitted per platform.

**متى:** Setting up tokens, dark mode or multi-brand.

**كيف:** 1) One source of truth in W3C DTCG JSON ($value/$type). 2) Primitives: raw palette, never used by products. 3) Semantic tokens name roles (color.bg.surface) referencing primitives. 4) Component tokens only when independent tuning is needed. 5) Themes = semantic maps under [data-brand][data-theme]. 6) Style Dictionary to CSS vars plus typed TS map, build fails on bad names.

**المعاملات:** brands, modes

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** tokens · theming · dark-mode · ثيمات

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2278-design-systems-engineering/8697-design-token-architecture`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/13267`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/7560`

#### 7. قدرات قريبة في العائلة

- `ABUILD-46` حلقة مقارنة لقطة الصفحة بالتصميم / Screenshot-vs-design pixel diff loop (documented)
- `ABUILD-47` حلقة مقارنة لقطة الشاشة بالمرجع / Screenshot-vs-reference pixel diff loop (documented)
- `ABUILD-49` تدقيق إتاحة WCAG 2.2: فحص وإصلاح وتحقق / WCAG 2.2 scan-fix-verify accessibility audit (documented)
- `ABUILD-50` إصدار نسخة: وسم ونشر وتحقق / Cut a release: tag, GitHub release, verify (documented)

### `ABUILD-49` — تدقيق إتاحة WCAG 2.2: فحص وإصلاح وتحقق / WCAG 2.2 scan-fix-verify accessibility audit

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT / Apache-2.0; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** فحص كود الواجهة لمخالفات WCAG 2.2 وترتيبها بالخطورة وتقديم إصلاحات قبل/بعد ثم إعادة التحقق. — Scan a front-end codebase for WCAG 2.2 A/AA violations, rank by severity, emit before/after fixes and re-verify against a baseline.

**متى:** Asked to audit, fix or gate accessibility in React/Vue/Angular/HTML code.

**كيف:** 1) Detect framework. 2) Scan for criteria (alt 1.1.1, keyboard 2.1.1, labels, contrast 1.4.3). 3) Classify Critical (fix before release) / Major (this sprint) / Minor (2 sprints). 4) Emit framework-specific before/after diffs. 5) Re-run against saved baseline JSON to catch regressions. 6) Output stakeholder report and CI-friendly result.

**المعاملات:** scope dir, severity threshold, framework

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** a11y · wcag · audit · إتاحة

#### 1. الاستقبال (A25)

- اللغة والإطار: افتراض مكتوب ← لغة المستودع الموجود، وإلا Python أو HTML/JS بلا اعتماديات
- أين يعمل: افتراض مكتوب ← المتصفح أو سطر الأوامر حسب المخرج
- مستودع أو ملفات موجودة: سؤال بإجابة مقترحة ← مشروع جديد مستقل
- متى يكون ناجحًا: افتراض مكتوب ← الاختبارات الموجودة تمر + اختبار لكل سلوك جديد
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:axe` ← npm ls axe أو وجود node_modules/axe
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/149-a11y-audit/492-a11y-audit`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/13231`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/948`

#### 7. قدرات قريبة في العائلة

- `ABUILD-47` حلقة مقارنة لقطة الشاشة بالمرجع / Screenshot-vs-reference pixel diff loop (documented)
- `ABUILD-48` معمارية رموز التصميم بثلاث طبقات / Three-tier design token architecture with theming (documented)
- `ABUILD-50` إصدار نسخة: وسم ونشر وتحقق / Cut a release: tag, GitHub release, verify (documented)
- `ABUILD-51` صياغة التذاكر وأوصاف PR بهيكل ماذا/لماذا/كيف / What/Why/How ticket and PR drafting (documented)

### `ABUILD-50` — إصدار نسخة: وسم ونشر وتحقق / Cut a release: tag, GitHub release, verify

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT/Apache; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** تنفيذ بوابات الإصدار ثم الوسم والنشر والتحقق من وجود الوسم. — Run release gates, tag, push and publish a GitHub release then prove the tag exists.

**متى:** Cut/ship a release, publish version.

**كيف:** 1) Preflight git status, branch, existing tags. 2) Validate/review gates. 3) Bump, commit release files. 4) git tag vX locally, push tag. 5) gh release create with notes. 6) Verify with git ls-remote --tags. Support --dry-run.

**المعاملات:** version, dry-run

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** release · tag · نشر

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/?/10012-release`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/?/1238-ship`
- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/?/9678-releasing`

#### 7. قدرات قريبة في العائلة

- `ABUILD-48` معمارية رموز التصميم بثلاث طبقات / Three-tier design token architecture with theming (documented)
- `ABUILD-49` تدقيق إتاحة WCAG 2.2: فحص وإصلاح وتحقق / WCAG 2.2 scan-fix-verify accessibility audit (documented)
- `ABUILD-51` صياغة التذاكر وأوصاف PR بهيكل ماذا/لماذا/كيف / What/Why/How ticket and PR drafting (documented)
- `ABUILD-52` فرز أعطال الاتصال حسب مجال الخطأ دون تغيير الإعدادات / Fault-domain connectivity triage without touching config (documented)

### `ABUILD-51` — صياغة التذاكر وأوصاف PR بهيكل ماذا/لماذا/كيف / What/Why/How ticket and PR drafting

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يكتب جسم تذكرة أو بلاغ خطأ أو وصف PR بثلاثة أقسام ثابتة ولغة محايدة إيجابية بلا وعود. — Writes an issue, bug report or PR body in three fixed sections with neutral, affirmative wording and no unbacked claims.

**متى:** كتابة issue أو وصف PR أو مهمة إعادة هيكلة / drafting an issue, bug report, PR description or migration task

**كيف:** 1) What: 1-3 sentences on the subject, with links to related issues and official docs. 2) Why: the problem or opportunity and its background, linked to the discussion. 3) How: one concrete action per bullet, in order, ending in verifiable acceptance criteria. 4) Say what to do rather than what to avoid; state facts without superlatives, percentages or time estimates. 5) Before posting check every link resolves and the Markdown renders; read the repo's PR template first.

**المعاملات:** type: feature\|bug\|refactor

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ticket · issue · PR description · تذكرة · وصف طلب الدمج · What/Why/How

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2143-communication-plugin/7664-ticket-drafting-guidelines`

#### 7. قدرات قريبة في العائلة

- `ABUILD-49` تدقيق إتاحة WCAG 2.2: فحص وإصلاح وتحقق / WCAG 2.2 scan-fix-verify accessibility audit (documented)
- `ABUILD-50` إصدار نسخة: وسم ونشر وتحقق / Cut a release: tag, GitHub release, verify (documented)
- `ABUILD-52` فرز أعطال الاتصال حسب مجال الخطأ دون تغيير الإعدادات / Fault-domain connectivity triage without touching config (documented)

### `ABUILD-52` — فرز أعطال الاتصال حسب مجال الخطأ دون تغيير الإعدادات / Fault-domain connectivity triage without touching config

| الحقل | القيمة |
|---|---|
| العائلة | `atlas-build` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/atlas-build.md)) |
| المجموعة | البرمجة وبناء التطبيقات (`software`) |
| نوع المخرج (A25، A27) | كود وتطبيقات ومواقع (`code`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | method paraphrased from Atlas skills under MIT; the skills keep their own licenses — see each folder's SOURCE.md |

**ما هي:** يحدد مكان عطل الشبكة (الشبكة المحلية، DNS، المسار، الخدمة نفسها) بأقل الأدلة وبأوامر قراءة فقط. — Localises a live connectivity failure to LAN, DNS, upstream path or the remote service with bounded, read-only probes.

**متى:** API أو خادم MCP ينقطع، DNS متقلب، فقدان حزم / an API or MCP server times out, DNS is flaky, calls drop packets

**كيف:** 1) Record the exact affected host/URL, start time, continuous or intermittent, and whether other sites work. 2) Compare a 5-packet ping to a known local target with one to the destination (never invent a gateway). 3) Separate resolver configuration (scutil --dns / resolvectl) from query behaviour (dig +time=2 +tries=1). 4) Bounded traceroute -n -q 1 -m 20 only if path visibility reduces doubt; a silent hop is not a broken hop. 5) Time the real endpoint with curl -w dns/connect/tls/ttfb/total and timeouts. 6) Label each line Observed / Inferred / Unknown and return one fault domain with low/medium/high confidence plus the single next safest check; no restarts, DNS flushes or firewall edits during diagnosis.

**المعاملات:** host, symptom window

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** network · DNS · latency · شبكة · انقطاع · MCP timeout · triage

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

- عقدة منمّطة: المدخل `spec` ← المخرج `code`، والمنفّذ `method:ABUILD-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
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

#### 6. الأدلة

- `https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3494-incident-response/14217-connectivity-triage`

#### 7. قدرات قريبة في العائلة

- `ABUILD-50` إصدار نسخة: وسم ونشر وتحقق / Cut a release: tag, GitHub release, verify (documented)
- `ABUILD-51` صياغة التذاكر وأوصاف PR بهيكل ماذا/لماذا/كيف / What/Why/How ticket and PR drafting (documented)

