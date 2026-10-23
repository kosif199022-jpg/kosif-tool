# الاختبارات والجودة والأمان — QA & security

[← الفهرس الدقيق / micro index](README.md) · 469 powers

## الفهرس / contents

- [api-testing (code)](#api-testing-code)
- [security-safety (code)](#security-safety-code)
- [verification-evals (mind)](#verification-evals-mind)
- [qa-verification (motion)](#qa-verification-motion)


## api-testing (code)

chapter: [api-testing](../powers/api-testing.md) · card: `usip-library/cards/quality/api-testing.md` · tools: —

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| API-01 | ✅ | مجموعة طلبات كملفات نصية في git · Author an API collection as git-tracked Bru files | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-02 | ✅ | تشغيل المجموعة كاختبارات قبول · Run a collection as automated acceptance tests | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-03 | ✅ | تأكيدات تعريفية على الاستجابة · Declarative response assertions | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-04 | ✅ | اختبارات Chai على الاستجابة · Chai-style tests on the response | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-05 | ✅ | تسلسل الطلبات بحفظ المتغيرات · Request chaining via saved variables | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-06 | ✅ | المصادقة: Bearer وBasic وOAuth2 · Auth: Bearer, Basic, OAuth 2.0 and more | SP-0042 Generate standalone HTML API docs | key:unspecified, npm:bruno |
| API-07 | ✅ | متغيرات على مستويات متعددة · Variables at every scope | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-08 | ✅ | الأسرار خارج الملفات · Secrets kept out of the files | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-09 | ✅ | سكربتات ما قبل وبعد الطلب · Pre-request and post-response scripts | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-10 | ✅ | تشغيل مدفوع بالبيانات من CSV/JSON · Data-driven runs from CSV/JSON | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-11 | ✅ | تقارير JSON وJUnit وHTML · JSON, JUnit and HTML reports | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-12 | ✅ | بوابة فشل لخط CI · CI failure gate | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-13 | ✅ | استيراد OpenAPI إلى مجموعة · Import OpenAPI into a collection | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-14 | ✅ | توليد توثيق HTML للـAPI · Generate standalone HTML API docs | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-15 | ✅ | تحويل Postman وInsomnia · Convert Postman and Insomnia collections | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-16 | 📦 | بروتوكولات متعددة · REST, GraphQL, gRPC, WebSocket, SOAP | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-17 | 📦 | استيراد WSDL · Import a WSDL (SOAP) definition | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-18 | 🔑 | خوادم محاكاة من مواصفة أو أمثلة · Mock servers from a spec or saved examples | SP-0042 Generate standalone HTML API docs | npm:bruno, key:unspecified |
| API-19 | 📄 | تعاون عبر git بلا سحابة · Git-native collaboration, no cloud | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-20 | 📄 | مكتبات مدمجة في السكربتات · Built-in libraries in scripts | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-21 | 📄 | إرسال طلب فرعي من سكربت · Send a sub-request from a script | SP-0042 Generate standalone HTML API docs | npm:bruno |
| API-22 | 📄 | صيغة OpenCollection وBru Lang · OpenCollection YAML and Bru Lang | SP-0042 Generate standalone HTML API docs | npm:bruno |

## security-safety (code)

chapter: [security-safety](../powers/security-safety.md) · card: `usip-library/cards/quality/security-safety.md` · tools: `agent-guard` · `atlas-audit-synthesis` · `atlas-body-audit` · `atlas-external-bridge` · `atlas-metadata-audit` · `capability-runtime-router` · `charter-ingest` · `check-skill` …

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| SEC-14 | ✅ | تشغيل أدوات غريبة في بيئة نظيفة · Run foreign tools in a scrubbed sandbox | SP-0068 Approval ladder and least escalation | python3, key:graphify |
| SEC-09 | 📦 | فحص الحزام بـAgentShield · Harness scan with AgentShield | SP-0068 Approval ladder and least escalation | node |
| SEC-17 | 📦 | Semgrep CE: تشغيل قواعد تحليل ثابت على مستودع وفرز · Semgrep CE: Run pattern-based SAST rules over a repo and triage findings | SP-0068 Approval ladder and least escalation | pip:semgrep |
| SEC-18 | 📦 | Gitleaks: كشف الأسرار المسرّبة في تاريخ git · Gitleaks: Detect committed secrets across git history | SP-0068 Approval ladder and least escalation | gitleaks |
| SEC-19 | 📦 | Trivy: فحص ملفات القفل والحاويات والبنية ككود بحثًا · Trivy: Scan lockfiles, containers and IaC for CVEs and misconfigurations | SP-0068 Approval ladder and least escalation | trivy |
| SEC-10 | 📄 | المهارات والإضافات سلسلة توريد · Skills, plugins and MCP servers are supply chain | SP-0068 Approval ladder and least escalation | — |
| SEC-11 | 📄 | لا تثق بإعدادات مستودع غريب · Do not trust a foreign repo's agent config | SP-0068 Approval ladder and least escalation | — |
| SEC-12 | 📄 | قواعد منع أساسية · Baseline deny rules | SP-0068 Approval ladder and least escalation | network |
| SEC-13 | 📄 | أقل قدر من الصلاحية · Least agency | SP-0068 Approval ladder and least escalation | — |
| SEC-15 | 📄 | حارس الأوامر المدمّرة · Destructive-command guard | SP-0068 Approval ladder and least escalation | — |
| SEC-16 | 📄 | حلقة الموافقة على الرسائل الصادرة · Outbound approval loop | SP-0068 Approval ladder and least escalation | — |
| SEC-20 | 📄 | سلّم الموافقة وأقل تصعيد · Approval ladder and least escalation | SP-0068 Approval ladder and least escalation | — |
| SEC-21 | 📄 | تقطيع الأوامر وقواعد بادئة مختبرة · Command segmentation and tested prefix rules | SP-0068 Approval ladder and least escalation | — |
| SEC-22 | 📄 | تصنيف مخاطر الحارس قبل الفعل · Guardian risk taxonomy before acting | SP-0068 Approval ladder and least escalation | — |
| SEC-23 | 📄 | صدق تدهور العزل · Honest sandbox degradation | SP-0068 Approval ladder and least escalation | python3 |
| SEC-01 | 📄 | المحتوى الخارجي بيانات لا أوامر · Untrusted content is data, not instructions | SP-0069 Secrets hygiene | — |
| SEC-02 | 📄 | فحص النص المخفي · Hidden-text and payload scan | SP-0069 Secrets hygiene | network |
| SEC-03 | 📄 | تغليف المدخلات غير الموثوقة للنموذج · Wrap untrusted input before a model reads it | SP-0069 Secrets hygiene | claude:tools |
| SEC-04 | 📄 | افصل القارئ عن المنفّذ · Split the reader from the actor | SP-0069 Secrets hygiene | — |
| SEC-05 | 📄 | نظافة الأسرار · Secrets hygiene | SP-0069 Secrets hygiene | key:unspecified |
| SEC-06 | 📄 | البحث عن الأسرار المسرّبة · Leaked-secret scanning | SP-0069 Secrets hygiene | git, mcp:github, gitleaks |
| SEC-07 | 📄 | عند تسرّب سر · When a secret leaks | SP-0069 Secrets hygiene | — |
| SEC-08 | 📄 | مراجعة أمان للتغييرات · Security review of a change | SP-0069 Secrets hygiene | node |

## verification-evals (mind)

chapter: [verification-evals](../powers/verification-evals.md) · card: `usip-library/cards/quality/verification-evals.md` · tools: `build-chapters` · `catalog-evidence-audit` · `check-skill` · `council` · `differential-exam` · `lesson-integrity` · `package-skill` · `prompt-lab` …

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| CHECK-02 | ✅ | بوابة ما بعد الرندر · Postcondition gate on the delivered file (ffprobe / verify_video.py / measured sync) | SP-0027 Verification loop (8 steps until done-c… | ffmpeg, pip:office |
| CHECK-03 | ✅ | انظر إلى المخرَج بعينك · Look at the output: contact sheets, frames, screenshots | SP-0027 Verification loop (8 steps until done-c… | ffmpeg, python3, chromium |
| CHECK-01 | 📄 | حلقة التحقق الثمانية · Verification loop (8 steps until done-criteria pass) | SP-0027 Verification loop (8 steps until done-c… | ffmpeg |
| CHECK-04 | 📄 | التقييم الذاتي بخمسة محاور · Five-axis self-evaluation (accuracy, completeness, clarity, actionability, concision) | SP-0027 Verification loop (8 steps until done-c… | — |
| CHECK-05 | 📄 | هاجم مخرَجك بنفسك · Red-team your own output (edge inputs + sceptical expert) | SP-0027 Verification loop (8 steps until done-c… | — |
| CHECK-06 | 📄 | حلقة تحقق الكود · Code verification loop: build → types → lint → tests → secrets → diff | SP-0027 Verification loop (8 steps until done-c… | node, python3, git, key:unspecified |
| CHECK-07 | 📄 | قاعدة التوقف · Stop rule: done means checks pass, or the budget ends with risks stated | SP-0027 Verification loop (8 steps until done-c… | — |
| CHECK-08 | 📄 | سُلَّم الأدلة للادعاءات · Evidence ladder for claims (badges are earned, leased and downgraded) | SP-0027 Verification loop (8 steps until done-c… | — |
| CHECK-09 | 📄 | الإيصال المنمَّط · Typed receipt after consequential actions | SP-0027 Verification loop (8 steps until done-c… | ffmpeg |
| CHECK-10 | 📄 | كلمات الحالة الصادقة · Honest status words (stage by stage) | SP-0027 Verification loop (8 steps until done-c… | — |
| CHECK-12 | 📄 | pass@k مقابل pass^k · pass@k vs pass^k (any success vs always success) | SP-0027 Verification loop (8 steps until done-c… | — |
| CHECK-15 | 📄 | طريقة سانتا: مراجعان معزولان · Santa method: two isolated reviewers, both must pass | SP-0027 Verification loop (8 steps until done-c… | claude:tools |
| CHECK-16 | 📄 | حلقة المولِّد والمقيِّم · Generator–evaluator loop (weighted rubric, threshold, iteration cap) | SP-0027 Verification loop (8 steps until done-c… | chromium |
| CHECK-17 | 📄 | المتحقق العدائي · Adversarial verifier that defaults to 'refuted' | SP-0027 Verification loop (8 steps until done-c… | — |
| CHECK-19 | 📄 | فحص تصميم الحلقة · Loop design check before automating anything | SP-0027 Verification loop (8 steps until done-c… | — |
| CHECK-32 | 📄 | خادم نموذج وهمي مسجِّل · Recording mock model server | SP-0027 Verification loop (8 steps until done-c… | python3 |
| CHECK-33 | 📄 | قائمة سطح الملاحظة · Observable-surface checklist | SP-0027 Verification loop (8 steps until done-c… | — |
| CHECK-34 | 📄 | المصحّح يعطي 100% على نفسه أولًا · Scorer must score 100% on itself first | SP-0027 Verification loop (8 steps until done-c… | python3 |
| CHECK-39 | 📄 | مراجعة حقائق تعيد الرقم المنشور · A fact-check pass that restores the published figure | SP-0027 Verification loop (8 steps until done-c… | python3 |
| CHECK-22 | ✅ | لقطة الفهرس والمدقِّق · Catalog snapshot: powers.py stats + repo validator | SP-0028 Self-evolution loop for this skill (evo… | python3 |
| CHECK-23 | ✅ | بوابة السجلات الحتمية · Deterministic record gate for the power catalog (mutation-tested) | SP-0028 Self-evolution loop for this skill (evo… | — |
| CHECK-21 | 📄 | مصفوفة اختبار التفعيل · Trigger eval matrix for a skill (+ with/without A/B) | SP-0028 Self-evolution loop for this skill (evo… | claude:tools |
| CHECK-24 | 📄 | حلقة التطوير الذاتي للمهارة · Self-evolution loop for this skill (evolve with evidence) | SP-0028 Self-evolution loop for this skill (evo… | python3 |
| CHECK-25 | 📄 | دروس بموافقة ونطاق مشروع · Consent-scoped lessons (growth log) | SP-0028 Self-evolution loop for this skill (evo… | — |
| CHECK-26 | 📄 | سجل القرارات المتكرر · Decision ledger for repeated rollouts | SP-0028 Self-evolution loop for this skill (evo… | — |
| CHECK-36 | 📄 | سجل قيم بمصدر واقتباس لكل رقم · One value registry: a source and the supporting sentence for every number | SP-0028 Self-evolution loop for this skill (evo… | python3 |
| CHECK-37 | 📄 | النص يشير إلى الرقم بمعرّفه ويفشل مغلقًا · Text refers to numbers by id and fails closed | SP-0028 Self-evolution loop for this skill (evo… | python3 |
| CHECK-38 | 📄 | ملف فجوات بدل اختراع رقم · An explicit gaps list instead of an invented number | SP-0028 Self-evolution loop for this skill (evo… | — |
| CHECK-40 | 📄 | دفتر حفظ: ابحث عن كل وحدة · A conservation ledger: account for every unit | SP-0028 Self-evolution loop for this skill (evo… | python3 |
| CHECK-11 | 📄 | التقييم أولًا · Eval-first: capability evals + regression evals | SP-0029 Eval-first: capability evals + regressi… | — |
| CHECK-13 | 📄 | بوابة الفشل القاطع · Hard-fail gate: one must-never-happen failure blocks release | SP-0029 Eval-first: capability evals + regressi… | — |
| CHECK-14 | 📄 | انضباط المحكِّم · Judge discipline: assertions first, one criterion per judgement, cited evidence | SP-0029 Eval-first: capability evals + regressi… | ffmpeg |
| CHECK-18 | 📄 | حلقة تحسين الأداء بالقياس · Benchmark-optimisation loop (one hypothesis per variant) | SP-0029 Eval-first: capability evals + regressi… | pip:hypothesis |
| CHECK-20 | 📄 | اختبار الطفرات للمدقِّق · Mutation-test your validator (seed defects, count catches) | SP-0029 Eval-first: capability evals + regressi… | — |
| CHECK-30 | 📄 | حَكَم مغلق الخيارات مرتين بترتيب معكوس · Closed-set judge asked twice with reversed options, a 'none' option and a declared fallback | SP-0029 Eval-first: capability evals + regressi… | — |
| CHECK-31 | 📄 | امتحان مختوم قبل العمل · Exam sealed before the work | SP-0029 Eval-first: capability evals + regressi… | python3 |
| CHECK-27 | 📄 | تصنيف الأعطال وأصغر إصلاح · Failure taxonomy → smallest repair | SP-0030 Failure taxonomy → smallest repair | key:unspecified |
| CHECK-28 | 📄 | سجل الحادثة · Incident record: expected vs actual vs evidence | SP-0030 Failure taxonomy → smallest repair | ffmpeg, pip:pillow |
| CHECK-29 | 📄 | قواعد الإصلاح الذاتي · Self-repair rules: retry once, narrower; never relax a safety gate | SP-0030 Failure taxonomy → smallest repair | — |
| CHECK-35 | 📄 | ملاحظات استرداد صادقة وخط أساس · Honest recovery notes and a measured baseline | SP-0030 Failure taxonomy → smallest repair | npm:rea |

## qa-verification (motion)

chapter: [qa-verification](../powers/qa-verification.md) · card: `usip-library/cards/quality/qa-verification.md` · tools: `anchor-gate` · `atlas-metadata-audit` · `blender-cycles-render` · `book-methods` · `catalog-evidence-audit` · `charter-ingest` · `cinematic-broll-render` · `creative-quality-gate` …

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| QA-137 | 📦 | نظافة البيانات المكانية · Spatial data hygiene | SP-0314 GeoJSON vs vector-tile threshold | — |
| QA-287 | 📄 | تحقق من واجهات البيانات · Trust-but-verify data APIs | SP-0314 GeoJSON vs vector-tile threshold | — |
| QA-01 | ✅ | بوابة التسليم · Delivery gate (inspect) | SP-0360 Delivery gate (inspect) | python3 |
| QA-03 | ✅ | بوابة فحص التسليم · verify_video delivery gate | SP-0360 Delivery gate (inspect) | ffmpeg, python3 |
| QA-04 | ✅ | فحص التسليم من الملف نفسه · Delivery QA from the decoded file | SP-0360 Delivery gate (inspect) | ffmpeg |
| QA-24 | ✅ | عبارة اعتماد التصدير النهائي · Typed final-render approval phrase | SP-0360 Delivery gate (inspect) | node, python3 |
| QA-46 | ✅ | بوابة فحص الجودة وإيصال الإنتاج · ffprobe delivery gate + receipt | SP-0360 Delivery gate (inspect) | ffmpeg |
| QA-51 | ✅ | بوابة الستوري بورد · Storyboard gate | SP-0360 Delivery gate (inspect) | python3 |
| QA-54 | ✅ | فحص الفيديو المولد · Post-generation video QA | SP-0360 Delivery gate (inspect) | — |
| QA-62 | ✅ | فحص الأصالة · Originality check | SP-0360 Delivery gate (inspect) | python3 |
| QA-65 | ✅ | تقرير الفحص بـ 16 بندًا · TEST_REPORT 16-check QA template | SP-0360 Delivery gate (inspect) | ffmpeg |
| QA-101 | 🟢 | فحص البيئة · Environment check | SP-0360 Delivery gate (inspect) | python3 |
| QA-106 | 🟢 | تقرير التصدير · Export report object | SP-0360 Delivery gate (inspect) | — |
| QA-116 | 🟢 | فحص مسبق لمهمة الوسائط · Media job preflight (proplan) | SP-0360 Delivery gate (inspect) | python3 |
| QA-80 | 🟢 | بوابة المعاينة قبل التصدير · Preview-before-final-render gate | SP-0360 Delivery gate (inspect) | python3 |
| QA-81 | 🟢 | إيصال الفحص الفني · ffprobe QA receipt | SP-0360 Delivery gate (inspect) | ffmpeg, python3 |
| QA-85 | 🟢 | كوسف: بوابة التسليم وقياسات الحركة · KOSIF: delivery inspect gate and motion measures | SP-0360 Delivery gate (inspect) | python3 |
| QA-87 | 🟢 | بوابة التسليم · inspect delivery gate | SP-0360 Delivery gate (inspect) | python3 |
| QA-144 | 📦 | بوابة التسليم · Delivery gate | SP-0360 Delivery gate (inspect) | — |
| QA-145 | 📦 | صفحة فحص الربط · Integration health check page | SP-0360 Delivery gate (inspect) | — |
| QA-173 | 📦 | بوابة قرار الترجمة · Caption decision gate (refuse bad clips) | SP-0360 Delivery gate (inspect) | ffmpeg, pip:faster-whisper |
| QA-178 | 📦 | بوابة الإطارات المفتاحية · Keyframe gate frames | SP-0360 Delivery gate (inspect) | python3 |
| QA-184 | 📦 | التصيير النهائي والبوابة · Final render + inspect gate | SP-0360 Delivery gate (inspect) | — |
| QA-193 | 📦 | بوابة الإطارات المفتاحية · Key frames gate | SP-0360 Delivery gate (inspect) | python3 |
| QA-206 | 📦 | بوابة الواقعية · Realism gate (judge.py) | SP-0360 Delivery gate (inspect) | python3 |
| QA-212 | 📦 | فحص التسليم · Delivery verification | SP-0360 Delivery gate (inspect) | python3 |
| QA-213 | 📦 | بوابة الفحص قبل الرندر · hyperframes check gate | SP-0360 Delivery gate (inspect) | npm:hyperframes, npm:axe |
| QA-223 | 🔑 | فحص الاستهلاك المتبقي · Usage and plan-window check | SP-0360 Delivery gate (inspect) | npm:hyperframes, key:unspecified |
| QA-237 | 📄 | فحص التسليم للفيديو · Delivery QA for web/social video | SP-0360 Delivery gate (inspect) | ffmpeg, python3 |
| QA-246 | 📄 | بوابة فحص الملف المسلّم · Delivered-file QA gate | SP-0360 Delivery gate (inspect) | ffmpeg |
| QA-294 | 📄 | ميثاق عدم الادعاء · No-false-claims honesty contract | SP-0360 Delivery gate (inspect) | pip:higgsfield |
| QA-295 | 📄 | قائمة مراجعة الرندر · Render review checklist | SP-0360 Delivery gate (inspect) | — |
| QA-296 | 📄 | فحص بوابات المحرر في CI · CI editorial gate check | SP-0360 Delivery gate (inspect) | ffmpeg, node, python3, chromium |
| QA-304 | 📄 | تقرير فحص التسليم لفيديو صوتي · Delivery QA report for a voice-driven render | SP-0360 Delivery gate (inspect) | — |
| QA-310 | 📄 | بوابة التسليم · Delivery gate (black, freeze, LUFS, peak, exposure) | SP-0360 Delivery gate (inspect) | python3 |
| QA-313 | 📄 | فحص البيئة · Environment doctor | SP-0360 Delivery gate (inspect) | ffmpeg, pip:faster-whisper |
| QA-315 | 📄 | بوابات جودة التسليم · Delivery quality gates (montage) | SP-0360 Delivery gate (inspect) | imagemagick |
| QA-322 | 📄 | بوابات تسليم المونتاج · Editor delivery gates | SP-0360 Delivery gate (inspect) | ffmpeg |
| QA-326 | 📄 | فحص ما قبل الرندر · Pre-render checklist (Resolve) | SP-0360 Delivery gate (inspect) | — |
| QA-330 | 📄 | بوابة الثماني ثوانٍ · Eight-second gate + weakest-beat gate | SP-0360 Delivery gate (inspect) | — |
| QA-345 | 📄 | بوابة التسليم · Delivery inspect gate | SP-0360 Delivery gate (inspect) | python3 |
| QA-349 | 📄 | معاينة قبل الرندر النهائي · Preview-before-render approval gate | SP-0360 Delivery gate (inspect) | — |
| QA-351 | 📄 | قائمة فحص الإعلان · Ad QA checklist | SP-0360 Delivery gate (inspect) | — |
| QA-360 | 📄 | قائمة فحص الرندر · Render QA checklist | SP-0360 Delivery gate (inspect) | — |
| QA-P01 | 📄 | إيصال تنفيذ مُتحقَّق منه: لا نجاح بلا دليل · Evidence receipt validator (no verified success without evidence) | SP-0360 Delivery gate (inspect) | ffmpeg, python3 |
| QA-09 | ✅ | عتبات التباين وتدقيق اللوحة · Contrast thresholds and palette audit | SP-0361 WCAG contrast floors | python3, npm:axe |
| QA-10 | ✅ | عقد تباين الألوان والمسافة الإدراكية · Palette contrast + perceptual-distance contract | SP-0361 WCAG contrast floors | npm:axe |
| QA-13 | ✅ | اختبار عقد التجاوب · Responsive layout contract test | SP-0361 WCAG contrast floors | node |
| QA-15 | ✅ | اختبار تثبيت الثيم · Theme lock test (dashboard/editorial) | SP-0361 WCAG contrast floors | node, fonts:arabic |
| QA-22 | ✅ | اختبار محرك ثلاثي الأبعاد دون متصفح · 3D engine unit test without a browser | SP-0361 WCAG contrast floors | chromium, npm:three |
| QA-25 | ✅ | حزمة الاختبارات · Unit test suite (24 tests) | SP-0361 WCAG contrast floors | node |
| QA-31 | ✅ | اختبار المشغل بمحاكاة DOM · Mocked-DOM player test harness | SP-0361 WCAG contrast floors | node |
| QA-47 | ✅ | اختبارات A/B · A/B test plan and read | SP-0361 WCAG contrast floors | python3 |
| QA-67 | ✅ | مجموعة الاختبارات · Test suite (node --test + unittest) | SP-0361 WCAG contrast floors | ffmpeg, node, python3 |
| QA-X03 | ✅ | الحجم الفعلي وأسوأ بكسل تباين · Effective text size and worst-pixel contrast by double render | SP-0361 WCAG contrast floors | pip:pillow, npm:axe |
| QA-X09 | ✅ | بطاقة نتائج اصطناعية بحقيقة أرضية لخط أنابيب المحاكاة · Synthetic ground-truth scorecard for the mimic pipeline | SP-0361 WCAG contrast floors | ffmpeg, chromium, pip:numpy, pip:pillow … |
| QA-102 | 🟢 | شارات حالة البيئة · Environment status pills | SP-0361 WCAG contrast floors | ffmpeg, pip:faster-whisper |
| QA-126 | 📦 | فحص التباين عبر الزمن · WCAG contrast audit over time | SP-0361 WCAG contrast floors | chromium, npm:hyperframes, npm:axe |
| QA-131 | 📦 | اختبار الإطارات الذهبية بأداة odiff · Golden-frame regression with odiff | SP-0361 WCAG contrast floors | ffmpeg, node, pip:numpy, pip:pillow |
| QA-149 | 📦 | أمر: فحص بصري · CLI: check | SP-0361 WCAG contrast floors | npm:hyperframes, npm:axe |
| QA-163 | 📦 | تقرير التباين من الإطارات · Contrast report from rendered frames | SP-0361 WCAG contrast floors | npm:axe |
| QA-165 | 📦 | الفحص في المتصفح: الأخطاء والتخطيط والحركة والتباين · Check (browser gate: runtime, layout, motion, WCAG contrast) | SP-0361 WCAG contrast floors | chromium, npm:hyperframes, npm:axe |
| QA-197 | 📦 | اختبار المحاكاة بفيديو اصطناعي · Synthetic regression harness for mimic | SP-0361 WCAG contrast floors | python3 |
| QA-199 | 📦 | اختبار المحاكاة الاصطناعي · Synthetic regression for mimic | SP-0361 WCAG contrast floors | python3 |
| QA-202 | 📦 | اللمسات الأخيرة حسب وضوح الفرق · Final-touch passes ordered by visibility (Delta E bands) | SP-0361 WCAG contrast floors | — |
| QA-242 | 📄 | فحص تباين النص فوق الصورة · Text-over-photo contrast check | SP-0361 WCAG contrast floors | pip:numpy, pip:pillow, npm:axe |
| QA-243 | 📄 | بوابات وضوح الإعلان الثابت · Static-ad legibility gates | SP-0361 WCAG contrast floors | npm:axe |
| QA-244 | 📄 | انضباط اختبار الإبداعات · Creative testing discipline | SP-0361 WCAG contrast floors | pip:hypothesis |
| QA-275 | 📄 | حدود التباين · WCAG contrast floors | SP-0361 WCAG contrast floors | python3, npm:axe |
| QA-288 | 📄 | فحص عمى الألوان والرمادي · Colorblind and grayscale check | SP-0361 WCAG contrast floors | — |
| QA-328 | 📄 | بوابة المقروئية · Readability gate | SP-0361 WCAG contrast floors | — |
| QA-332 | 📄 | 2). تدقيق وإصلاح الإتاحة · Accessibility (WCAG 2 | SP-0361 WCAG contrast floors | npm:axe |
| QA-337 | 📄 | اختبار الفهم بلا صوت · Silent-readability test | SP-0361 WCAG contrast floors | — |
| QA-338 | 📄 | نسختان A/B · A/B thumbnail single-variable | SP-0361 WCAG contrast floors | chromium |
| QA-X07 | 📄 | سلم حالات مهمة الوسائط · Media-job status ladder and preflight classes | SP-0361 WCAG contrast floors | ffmpeg, python3 |
| QA-371 | 💡 | منع النص فوق الوجه · Face-region text ban | SP-0361 WCAG contrast floors | — |
| QA-07 | ✅ | تدقيق القص على الإيقاع · Cut-to-beat audit | SP-0362 sheet contact review | — |
| QA-58 | ✅ | لوحات النقد · Critique contact sheets | SP-0362 sheet contact review | python3 |
| QA-X08 | ✅ | فحص المطابقة المرئي: الرندر مقابل إطارات المرجع · Fidelity check: composite the render against the reference frames | SP-0362 sheet contact review | node, chromium, pip:pillow, fonts:arabic |
| QA-109 | 🟢 | لوحة فحص 4×4 من الإطارات · Contact sheet 4x4 (every 15th frame) | SP-0362 sheet contact review | ffmpeg |
| QA-115 | 🟢 | أوراق المراجعة · Critique sheets: contact, phone, strip + review.md | SP-0362 sheet contact review | python3 |
| QA-119 | 🟢 | أوراق مراجعة المحاكاة · Review contact sheets (shots, transitions, texts, side by side) | SP-0362 sheet contact review | — |
| QA-88 | 🟢 | ورقة المراجعة · sheet contact review | SP-0362 sheet contact review | python3 |
| QA-98 | 🟢 | ورقة لقطات وفحص السرعة · Contact sheet + speed check | SP-0362 sheet contact review | — |
| QA-146 | 📦 | عرض المرجع والأصل والمنتج · Multi-monitor compare view | SP-0362 sheet contact review | — |
| QA-154 | 📦 | حلقة المراجعة: خطة ثم رسومات ثم بناء ثم معاينة · Review loop: plan -> sketch sheet -> build -> final look | SP-0362 sheet contact review | node |
| QA-167 | 📦 | لقطات ثابتة لورقة الاتصال · Snapshot contact sheets | SP-0362 sheet contact review | npm:hyperframes |
| QA-180 | 📦 | بناء المحاكاة وبوابة المقارنة · Mimic build + compare gate | SP-0362 sheet contact review | — |
| QA-183 | 📦 | مراجعة المستخدم · Review site markup | SP-0362 sheet contact review | — |
| QA-214 | 🔑 | صورة مفهوم أولاً ثم تنفيذ مطابق · Concept-image first, then faithful build | SP-0362 sheet contact review | key:unspecified |
| QA-220 | 🔑 | مراجعة الفريم الحالي · Single-frame director review | SP-0362 sheet contact review | key:unspecified |
| QA-227 | 🔑 | مقارنة ثلاثة نماذج · Three-model transition bake-off | SP-0362 sheet contact review | key:video-gen |
| QA-229 | 👁 | مقارنة إعادة بناء لقطة بلقطة · Shot-for-shot remake comparison | SP-0362 sheet contact review | ffmpeg |
| QA-231 | 📄 | حلقة النقد ثلاث جولات · Critique loop ≥3 rounds | SP-0362 sheet contact review | — |
| QA-234 | 📄 | ورقة لقطات للمراجعة · Contact sheet review | SP-0362 sheet contact review | ffmpeg |
| QA-238 | 📄 | مراجعة اللقطات الثابتة قبل الرندر · Stills-before-render review | SP-0362 sheet contact review | node, chromium |
| QA-248 | 📄 | مراجعة الثمبنيل بست نقاط · Six-check thumbnail review | SP-0362 sheet contact review | pip:pillow |
| QA-271 | 📄 | علامات مراجعة للأحكام الذوقية · Review markers for subjective calls | SP-0362 sheet contact review | — |
| QA-281 | 📄 | قائمة مراجعة التحريك · Animation review checklist (contact/passing) | SP-0362 sheet contact review | — |
| QA-297 | 📄 | مراجعة الإطار الأول والأوسط والأخير · First/middle/last frame review | SP-0362 sheet contact review | ffmpeg |
| QA-305 | 📄 | حلقة النقد الثمانية · 8-criterion critique loop | SP-0362 sheet contact review | — |
| QA-307 | 📄 | مراجعة بثلاث عدسات · Three-lens review receipt | SP-0362 sheet contact review | — |
| QA-311 | 📄 | لوحة النقد · Critique sheet (frames + phone view) | SP-0362 sheet contact review | python3 |
| QA-347 | 📄 | العدسات الجمالية الاثنتا عشرة · Twelve aesthetic lenses | SP-0362 sheet contact review | — |
| QA-P02 | 📄 | حلقة مراجعة الرندر المحدودة · Bounded iterative render review (½-second frames, 2–4 rounds) | SP-0362 sheet contact review | — |
| QA-11 | ✅ | عقد الحركة المخفضة · Reduced-motion contract | SP-0363 Motion quality checklist | — |
| QA-12 | ✅ | اختبار عقد الحركة · Motion contract test | SP-0363 Motion quality checklist | node |
| QA-16 | ✅ | محاكاة حركة المناطق من المرجع · Regional motion clone (4x4 block motion) | SP-0363 Motion quality checklist | — |
| QA-18 | ✅ | سياسة تقليل الحركة · Reduced-motion policy | SP-0363 Motion quality checklist | — |
| QA-122 | 🟢 | مقياس طاقة الحركة · Motion energy meter vs reference | SP-0363 Motion quality checklist | python3 |
| QA-71 | 🟢 | قياس طاقة الحركة · Motion energy measure | SP-0363 Motion quality checklist | python3 |
| QA-72 | 🟢 | كشف مكتبات الحركة ونموذج التفاعل · Motion-library and interaction-model detection | SP-0363 Motion quality checklist | npm:three, npm:gsap, npm:lottie, npm:animejs … |
| QA-82 | 🟢 | إثبات التغير الزمني بالبصمة · Temporal-change frame-hash proof | SP-0363 Motion quality checklist | ffmpeg |
| QA-128 | 📦 | خريطة الحركة لتدقيق الكوريغرافيا · Animation map (choreography audit) | SP-0363 Motion quality checklist | npm:gsap |
| QA-160 | 📦 | سكربت خريطة الحركة للتدقيق · Animation map audit script | SP-0363 Motion quality checklist | npm:gsap, npm:hyperframes |
| QA-161 | 📦 | أدوات تشخيص الحركة · Keyframe diagnostics CLI (keyframes / --shot / --ghost / strip) | SP-0363 Motion quality checklist | npm:three, npm:hyperframes |
| QA-166 | 📦 | تأكيدات الحركة الجانبية · Motion sidecar assertions (*.motion.json) | SP-0363 Motion quality checklist | — |
| QA-177 | 📦 | بوابة دقة حركة فيجما · Figma motion fidelity gate (motion-energy PSNR) | SP-0363 Motion quality checklist | npm:hyperframes |
| QA-194 | 📦 | قياس سرعة الحركة على الشاشة · On-screen speed gate (optical flow) | SP-0363 Motion quality checklist | python3 |
| QA-210 | 📦 | سرعة الحركة على الشاشة · On-screen speed by optical flow | SP-0363 Motion quality checklist | python3 |
| QA-239 | 📄 | بديل الحركة المخففة والإطار الثابت · Reduced-motion and static-frame fallback | SP-0363 Motion quality checklist | npm:gsap |
| QA-276 | 📄 | احترام تقليل الحركة · Reduced-motion respect | SP-0363 Motion quality checklist | — |
| QA-301 | 📄 | حدود السرعة · Speed limits | SP-0363 Motion quality checklist | — |
| QA-302 | 📄 | طاقة اختلاف الإطارات · Frame-difference energy | SP-0363 Motion quality checklist | — |
| QA-306 | 📄 | قائمة جودة الحركة · LottieFiles quality checklist | SP-0363 Motion quality checklist | npm:lottie |
| QA-331 | 📄 | اختبار التجميد · Freeze test for fake motion | SP-0363 Motion quality checklist | — |
| QA-341 | 📄 | حدّ نابض الأذن · Ear spring speed limit | SP-0363 Motion quality checklist | — |
| QA-342 | 📄 | قائمة جودة الحركة · Motion quality checklist | SP-0363 Motion quality checklist | npm:lottie |
| QA-34 | ✅ | توليد القوالب مع فحص · Template generation + lint gate | SP-0364 lint composition | — |
| QA-57 | ✅ | فحص الحتمية والذوق · Composition lint (determinism + contract + taste) | SP-0364 lint composition | python3 |
| QA-70 | 🟢 | فحص التركيب · Composition lint rules | SP-0364 lint composition | python3 |
| QA-89 | 🟢 | فحص التركيب · lint composition | SP-0364 lint composition | python3 |
| QA-148 | 📦 | أمر: فحص ثابت · CLI: lint | SP-0364 lint composition | npm:hyperframes |
| QA-157 | 📦 | أخطاء الفحص الأولى الشائعة · Lint first-pass gotchas | SP-0364 lint composition | — |
| QA-164 | 📦 | فحص البنية الثابت · Lint (static) gate | SP-0364 lint composition | npm:hyperframes |
| QA-176 | 📦 | أخطاء الترجمة المعروفة · Caption failure modes (learned) | SP-0364 lint composition | chromium |
| QA-189 | 📦 | تتبع أخطاء الشيدر بالعزل · Shader isolation debugging | SP-0364 lint composition | chromium |
| QA-209 | 📦 | لقطات مراجعة مفتاحية · Key-frame review grabs | SP-0364 lint composition | python3 |
| QA-300 | 📄 | فخاخ HyperFrames · HyperFrames traps | SP-0364 lint composition | npm:gsap, npm:hyperframes |
| QA-309 | 📄 | فحص الحتمية والذوق · Determinism and taste lint | SP-0364 lint composition | python3 |
| QA-316 | 📄 | قائمة منع أخطاء التوليد · Generator failure-prevention checklist | SP-0364 lint composition | — |
| QA-350 | 📄 | أخطاء الـ3D الشائعة · 3D anti-patterns | SP-0364 lint composition | — |
| QA-354 | 📄 | أخطاء تحريك الشخصيات · Character anti-patterns | SP-0364 lint composition | — |
| QA-355 | 📄 | أخطاء الرسوم البيانية · Chart anti-patterns | SP-0364 lint composition | — |
| QA-356 | 📄 | أخطاء مشاهد الكود · Code anti-patterns | SP-0364 lint composition | — |
| QA-357 | 📄 | أخطاء التايبوغرافي الحركي · Kinetic-type anti-patterns | SP-0364 lint composition | — |
| QA-359 | 📄 | أخطاء الجسيمات · Particle anti-patterns | SP-0364 lint composition | — |
| QA-361 | 📄 | أخطاء أفلام الهاتف · Phone anti-patterns | SP-0364 lint composition | — |
| QA-362 | 📄 | أخطاء أفلام الصور · Photo anti-patterns | SP-0364 lint composition | imagemagick |
| QA-363 | 📄 | أخطاء أفلام المنتج · Product UI anti-patterns | SP-0364 lint composition | — |
| QA-06 | ✅ | كشف تغير المشهد · Scene-change detection | SP-0365 Onset-sync verification | ffmpeg |
| QA-26 | ✅ | علم التحقق التاريخي · Historical fact-check flag | SP-0365 Onset-sync verification | — |
| QA-28 | ✅ | كشف الانتقالات: قطع وذوبان وغطس · Transition detection: cut, dissolve, dip | SP-0365 Onset-sync verification | — |
| QA-38 | ✅ | قواعد التحقق من manifest · Manifest validation rules | SP-0365 Onset-sync verification | — |
| QA-59 | ✅ | قاعدة الصدق في التوقيت · Truthful-timing rule | SP-0365 Onset-sync verification | — |
| QA-X04 | ✅ | فحص اتجاه الزوم عبر القطع · Zoom-direction check across cuts (log velocity) | SP-0365 Onset-sync verification | — |
| QA-68 | 🟢 | فحص إزاحة مزامنة الشفاه بالارتباط المتقاطع · Lip-sync offset check by cross-correlation | SP-0365 Onset-sync verification | — |
| QA-76 | 🟢 | ورقة إطارات الكلمات وبوابة تزامن الضربات · Word-frame sheet and hit-sync gate | SP-0365 Onset-sync verification | — |
| QA-134 | 📦 | التحقق من تزامن القطع مع الضربة · Onset-sync verification | SP-0365 Onset-sync verification | ffmpeg, pip:numpy, pip:librosa |
| QA-138 | 📦 | قياس مستوى الكلام والضوضاء · Speech level and noise-floor measurement | SP-0365 Onset-sync verification | — |
| QA-139 | 📦 | اكتشاف القطعات في الفيديو · Footage shot/cut detection (reference probe) | SP-0365 Onset-sync verification | — |
| QA-162 | 📦 | التحقق من الالتزام بالتصميم · Design adherence verification | SP-0365 Onset-sync verification | — |
| QA-191 | 📦 | فحص المطابقة بالإطارات والصوت · Mimic comparison QA (frames + audio correlation) | SP-0365 Onset-sync verification | — |
| QA-204 | 📦 | التحقق من المطابقة التامة · Exact-match verification badge | SP-0365 Onset-sync verification | — |
| QA-216 | 🔑 | التحقق من الكلمات المغناة بتحويل الكلام لنص · Sung-lyric verification by speech-to-text | SP-0365 Onset-sync verification | pip:faster-whisper, key:elevenlabs |
| QA-221 | 🔑 | مطابقة النص مع الكلام · Transcript verification against speech | SP-0365 Onset-sync verification | key:unspecified |
| QA-232 | 📄 | قياس إزاحة مزامنة الشفاه · GCC-PHAT lip-sync lag check | SP-0365 Onset-sync verification | — |
| QA-262 | 📄 | تحديث العناصر بعد إعادة القص · Recut propagation | SP-0365 Onset-sync verification | — |
| QA-286 | 📄 | التحقق من تصيير الخرائط · Map render verification | SP-0365 Onset-sync verification | — |
| QA-318 | 📄 | مستويات القدرة وقواعد الصدق · Capability tiers & truth rules | SP-0365 Onset-sync verification | — |
| QA-325 | 📄 | كشف اللقطات الرديئة · Bad-segment detection | SP-0365 Onset-sync verification | ffmpeg |
| QA-353 | 📄 | فحص التزامن في ثلاث لحظات · Three-point sync spot check | SP-0365 Onset-sync verification | — |
| QA-30 | ✅ | اختبارات حتمية لهندسة الفيلم · Deterministic geometry tests for a film function | SP-0366 Docker deterministic render | node |
| QA-52 | ✅ | دليل رندر demo2d · demo2d proof render | SP-0366 Docker deterministic render | — |
| QA-64 | ✅ | سطر التحقق بعد الرندر · Post-render ffprobe VERIFY line | SP-0366 Docker deterministic render | ffmpeg |
| QA-74 | 🟢 | إعدادات التقاط واجهة قابلة للتكرار · Reproducible UI capture settings | SP-0366 Docker deterministic render | chromium |
| QA-147 | 📦 | رندر تجريبي سريع · Smoke render mode | SP-0366 Docker deterministic render | python3 |
| QA-156 | 📦 | محظورات الحتمية · Determinism bans | SP-0366 Docker deterministic render | — |
| QA-175 | 📦 | بوابات فحص الترجمة · Caption render gates (timing / occlusion / overflow / hand-off) | SP-0366 Docker deterministic render | chromium, npm:gsap |
| QA-188 | 📦 | شريط تقدم حقيقي من FFmpeg · Live render progress from ffmpeg -progress | SP-0366 Docker deterministic render | ffmpeg |
| QA-215 | 🔑 | رندر مدفوع بسقف ميزانية · Budget-capped paid render | SP-0366 Docker deterministic render | key:unspecified |
| QA-222 | 🔑 | سد فراغات المونتاج قبل الريندر · Gap filling before render | SP-0366 Docker deterministic render | imagemagick, key:unspecified |
| QA-225 | 🔑 | رندر من دافنشي مع تحقق · Resolve render + verify | SP-0366 Docker deterministic render | ffmpeg, python3, key:unspecified |
| QA-263 | 📄 | جدول التحقق من الرندر النهائي · Final render verification table | SP-0366 Docker deterministic render | ffmpeg |
| QA-274 | 📄 | قائمة تحقق الريندر الأسود · Blender black-render checklist | SP-0366 Docker deterministic render | blender |
| QA-298 | 📄 | تصيير حتمي بدوكر · Docker deterministic render | SP-0366 Docker deterministic render | ffmpeg, chromium, docker, npm:hyperframes |
| QA-344 | 📄 | قائمة الفيديو القابل للتكرار · Reproducible video checklist | SP-0366 Docker deterministic render | python3 |
| QA-370 | 💡 | تشغيل قابل للتكرار · Reproducible seeded runs | SP-0366 Docker deterministic render | — |
| QA-43 | ✅ | مدقق برومبت الصور والفيديو · Image/video prompt linter | SP-0367 Settled poster frame pick | python3 |
| QA-44 | ✅ | عقد التنفيذ البصري · Visual execution contract (build/verify/repair/jev) | SP-0367 Settled poster frame pick | — |
| QA-53 | ✅ | فحص البرومبت · Image prompt lint | SP-0367 Settled poster frame pick | — |
| QA-56 | ✅ | تمييز الصورة الفوتوغرافية عن الرسم المسطح · Photo vs flat-art classifier | SP-0367 Settled poster frame pick | — |
| QA-108 | 🟢 | مقارنة صورتين لاستمرارية اللقطات · A/B image comparison for shot continuity | SP-0367 Settled poster frame pick | python3 |
| QA-112 | 🟢 | تحليل صورة مقاس · Measured image analysis | SP-0367 Settled poster frame pick | pip:numpy, pip:pillow |
| QA-77 | 🟢 | قراءة بيانات التوليد المضمنة · Embedded generation metadata readback | SP-0367 Settled poster frame pick | pip:pillow |
| QA-84 | 🟢 | تحديد موقع عنصر في صورة بشبكة مرقمة · Grid-index visual grounding (locate X in an image) | SP-0367 Settled poster frame pick | node |
| QA-93 | 🟢 | تثبيت الغلاف · poster bake | SP-0367 Settled poster frame pick | python3 |
| QA-205 | 📦 | كود الصورة كبيانات تُقرأ دون تنفيذ · Image code as pure data (read without executing) | SP-0367 Settled poster frame pick | — |
| QA-235 | 📄 | إطار مرجعي للمقارنة · Golden still regression | SP-0367 Settled poster frame pick | chromium, npm:remotion |
| QA-253 | 📄 | تراكب شفاف 50/50 لكشف الفروق الدقيقة · Onion-skin overlay for subtle visual diffs | SP-0367 Settled poster frame pick | ffmpeg, pip:pillow |
| QA-285 | 📄 | حالات ثابتة لاختبار الصور · Stable visual regression states | SP-0367 Settled poster frame pick | — |
| QA-339 | 📄 | قياسات الصورة · Image metrics by code | SP-0367 Settled poster frame pick | pip:numpy, pip:pillow |
| QA-365 | 📄 | اختيار إطار الغلاف · Settled poster frame pick | SP-0367 Settled poster frame pick | ffmpeg |
| QA-02 | ✅ | فحص الحلقة بلا درزة · Seamless loop check | SP-0368 Seamless loop check | python3 |
| QA-27 | ✅ | خصائص قابلة للتعديل وملف مشاهد داخل التركيب · Editable props + reel JSON inside the composition | SP-0368 Seamless loop check | — |
| QA-35 | ✅ | حلقة مراجعة مشهد بمشهد مع الكتابة للمصدر · Scene-by-scene review loop with write-back | SP-0368 Seamless loop check | — |
| QA-X02 | ✅ | مقياس الهواء الميت · Dead-air meter (block maximum) | SP-0368 Seamless loop check | chromium |
| QA-100 | 🟢 | مراجعة المشاهد · Review loop | SP-0368 Seamless loop check | — |
| QA-123 | 🟢 | فحص الملف · Probe media | SP-0368 Seamless loop check | python3 |
| QA-91 | 🟢 | فحص الحلقة · loopcheck | SP-0368 Seamless loop check | python3 |
| QA-207 | 📦 | حلقة المراجعة بالقياس · Measured review loop for painted scenes | SP-0368 Seamless loop check | python3 |
| QA-217 | 🔑 | دليل الأسلوب وحلقة التوليد والفحص · Theme bible + generate/QA loop for figure sets | SP-0368 Seamless loop check | tesseract, key:unspecified |
| QA-230 | 👁 | إغلاق حلقة بلا تقطيع · Seamless loop closure | SP-0368 Seamless loop check | — |
| QA-245 | 📄 | سلم تقييم مشاهد الخطاف · Hook scene scoring rubric | SP-0368 Seamless loop check | ffmpeg |
| QA-284 | 📄 | حلقة فحص: قياس ثم حكم · Measure-then-judge figure QA loop | SP-0368 Seamless loop check | — |
| QA-312 | 📄 | معلومات الملف · File probe | SP-0368 Seamless loop check | ffmpeg, python3 |
| QA-314 | 📄 | مخطط reel.json ومدققه · reel.json schema and checker | SP-0368 Seamless loop check | ffmpeg, node |
| QA-17 | ✅ | اختبارات CI · CI and regression tests | SP-0369 Built-in browser preview player | python3, npm:esbuild |
| QA-55 | ✅ | فحص أمان الكود قبل التشغيل · Code safety gate before running pasted code | SP-0369 Built-in browser preview player | python3 |
| QA-60 | ✅ | مجموعة اختبارات الموشن · Motion test suite | SP-0369 Built-in browser preview player | chromium, imagemagick, pip:opencv |
| QA-63 | ✅ | لوحة معاينة 8 إطارات · Contact-sheet preview (--preview) | SP-0369 Built-in browser preview player | ffmpeg, node, chromium |
| QA-103 | 🟢 | المراجعة: معاينة شبحية للعناصر المنقولة · Review: ghost preview of moved elements | SP-0369 Built-in browser preview player | — |
| QA-118 | 🟢 | فحص أمان الكود الملصوق · Pasted-code safety scan + sandbox | SP-0369 Built-in browser preview player | — |
| QA-121 | 🟢 | مشغل الكود الآمن · Sandboxed AI code runner | SP-0369 Built-in browser preview player | python3 |
| QA-124 | 🟢 | أدوات المعاينة الحية · Live preview controls (play/scrub/?t=) | SP-0369 Built-in browser preview player | — |
| QA-96 | 🟢 | مشغل المعاينة · Self-playing preview player | SP-0369 Built-in browser preview player | npm:hyperframes |
| QA-174 | 📦 | معاينة سريعة للإطارات المركبة · Fast composite preview frames (no render) | SP-0369 Built-in browser preview player | node |
| QA-182 | 📦 | معاينة وفحص القراءة · Preview + readability check | SP-0369 Built-in browser preview player | — |
| QA-192 | 📦 | مشغل معاينة داخل المتصفح · Built-in browser preview player | SP-0369 Built-in browser preview player | claude:browser |
| QA-201 | 📦 | مشغّل المعاينة · In-browser preview player | SP-0369 Built-in browser preview player | npm:hyperframes |
| QA-208 | 📦 | مجموعة اختبارات الاستوديو · KOSIF Studio regression suite | SP-0369 Built-in browser preview player | ffmpeg, python3 |
| QA-142 | 📦 | تقدير التكلفة وحد الصرف · Cost estimate and spending limit | SP-0370 Jev order-robust judge | key:video-gen |
| QA-195 | 📦 | حكم الواقعية للصور · Realism judge for still renders | SP-0370 Jev order-robust judge | python3 |
| QA-200 | 📦 | حكم الواقعية · Realism judge metric | SP-0370 Jev order-robust judge | python3 |
| QA-203 | 📦 | خطط رسم مقاسة يختار بينها حَكَم · Measured painting plans chosen by a judge | SP-0370 Jev order-robust judge | — |
| QA-218 | 🔑 | حكم Jev المغلق · Jev closed-set judge | SP-0370 Jev order-robust judge | key:unspecified |
| QA-224 | 🔑 | الحكم جيف · Jev order-robust judge | SP-0370 Jev order-robust judge | key:unspecified |
| QA-226 | 🔑 | حَكَم Jev المقاوم للترتيب · Jev order-robust judge client | SP-0370 Jev order-robust judge | key:unspecified |
| QA-333 | 📄 | فحص الادعاءات والأرقام والاقتباسات والاس · Fact-Checker & Verifier | SP-0370 Jev order-robust judge | — |
| QA-334 | 📄 | تقييم مخرجات الذكاء الاصطناعي بأرقام تصم · LLM Judge & Eval Lab | SP-0370 Jev order-robust judge | — |
| QA-335 | 📄 | تقييم أي ميزة ذكاء اصطناعي بأرقام · LLM Judge & Eval Suites | SP-0370 Jev order-robust judge | — |
| QA-336 | 📄 | اختبارات تثبت أن الكود يعمل · Complete Testing Suite | SP-0370 Jev order-robust judge | — |
| QA-340 | 📄 | تقييم بخمس معايير · 5x20 critique score | SP-0370 Jev order-robust judge | — |
| QA-364 | 📄 | تقييم حدة المؤثرات · SFX high-frequency risk scoring | SP-0370 Jev order-robust judge | — |
| QA-05 | ✅ | سياسة الإطارات الصادقة · Honest-frame capture policy | SP-0371 Frame QA: black/white/freeze/cut scan | ffmpeg, node, chromium |
| QA-40 | ✅ | صفحة المراجعة مشهدًا بمشهد · Scene-by-scene review page (KOSIF Review / Motion OS player) | SP-0371 Frame QA: black/white/freeze/cut scan | — |
| QA-50 | ✅ | فحص الإطارات الآلي · Frame QA: black/white/freeze/cut scan | SP-0371 Frame QA: black/white/freeze/cut scan | python3 |
| QA-X01 | ✅ | مسح الإطارات بعد الترميز · Frame-diff scan of the encoded file (OUTLIER · JUMP · FREEZE · DEAD AIR · TIMING) | SP-0371 Frame QA: black/white/freeze/cut scan | ffmpeg, pip:numpy |
| QA-110 | 🟢 | فاحص جودة الفيديو · Video QA inspector (black/freeze/loudness) | SP-0371 Frame QA: black/white/freeze/cut scan | ffmpeg, python3 |
| QA-95 | 🟢 | صفحة المراجعة · Review page (Motion OS) | SP-0371 Frame QA: black/white/freeze/cut scan | python3 |
| QA-135 | 📦 | التعامل مع فقد جهاز GPU · WebGPU device-loss handling | SP-0371 Frame QA: black/white/freeze/cut scan | chromium |
| QA-168 | 📦 | سطر تشخيص التصيير · Render diagnostics line (capture path) | SP-0371 Frame QA: black/white/freeze/cut scan | ffmpeg |
| QA-233 | 📄 | قواعد الأمانة في اللقطات · Honest capture rules | SP-0371 Frame QA: black/white/freeze/cut scan | — |
| QA-257 | 📄 | تحويل معدل إطارات متغير إلى ثابت · VFR to CFR fix for sync drift | SP-0371 Frame QA: black/white/freeze/cut scan | ffmpeg |
| QA-293 | 📄 | ميزانية أداء الطبقة الزخرفية · Decorative-layer perf budget | SP-0371 Frame QA: black/white/freeze/cut scan | — |
| QA-308 | 📄 | إطارات المراجعة · Review frames (eight-second gate) | SP-0371 Frame QA: black/white/freeze/cut scan | python3 |
| QA-08 | ✅ | إصلاح انزياح التوقيت عند الدمج · Concat drift fix: encode once | SP-0372 Loudness / true-peak verification | ffmpeg |
| QA-111 | 🟢 | تحليل صوتي مقاس · Measured audio analysis (BS.1770 loudness, true peak, BPM, spectrum) | SP-0372 Loudness / true-peak verification | ffmpeg, pip:matplotlib |
| QA-187 | 📦 | رسم الموجة والطيف · Waveform + spectrum plot | SP-0372 Loudness / true-peak verification | pip:matplotlib |
| QA-256 | 📄 | قياس الجهارة والذروة · Loudness / true-peak verification | SP-0372 Loudness / true-peak verification | ffmpeg |
| QA-267 | 📄 | صورة طيف وموجة للمراجعة · Spectrogram + waveform review image | SP-0372 Loudness / true-peak verification | ffmpeg |
| QA-268 | 📄 | ترتيب الميكس والفحص · Mix order & listening checks | SP-0372 Loudness / true-peak verification | ffmpeg |
| QA-269 | 📄 | تنبيه علو المؤثرات القصيرة · Short-SFX loudness caveat | SP-0372 Loudness / true-peak verification | — |
| QA-270 | 📄 | حفظ الصوت الأصلي بنسخة · Preserve original audio via duplicate | SP-0372 Loudness / true-peak verification | — |
| QA-292 | 📄 | قياس جهارة صوت المقدمة · Intro audio loudness (measured) | SP-0372 Loudness / true-peak verification | ffmpeg |
| QA-299 | 📄 | تشخيص صوت لا يمكن سماعه · Diagnose audio you cannot hear | SP-0372 Loudness / true-peak verification | ffmpeg |
| QA-37 | ✅ | مدقق الخطة · Plan validator | SP-0373 Arabic typography QA | — |
| QA-117 | 🟢 | فحص الملفات والدفعات والخطوط · Probe, batch and Arabic font scan | SP-0373 Arabic typography QA | python3 |
| QA-86 | 🟢 | فحص الملفات والخطوط · probe / fonts | SP-0373 Arabic typography QA | python3 |
| QA-94 | 🟢 | بوابة العربية · Arabic delivery gate | SP-0373 Arabic typography QA | python3 |
| QA-251 | 📄 | قائمة فحص قبل اعتماد الموشن · Pre-delivery motion QA checklist | SP-0373 Arabic typography QA | ffmpeg, python3 |
| QA-255 | 📄 | اختبار القوالب بمحتوى متطرف · Content-stress testing of templates | SP-0373 Arabic typography QA | chromium |
| QA-277 | 📄 | اختبار ثنائي الاتجاه · Bidi pseudo-locale stress test | SP-0373 Arabic typography QA | — |
| QA-279 | 📄 | فحص النقط عند حافة القناع · Mask-edge dot check | SP-0373 Arabic typography QA | — |
| QA-343 | 📄 | الدقة وإتاحة الوصول · Meaning, data truth and accessibility | SP-0373 Arabic typography QA | — |
| QA-352 | 📄 | فحص الطباعة العربية · Arabic typography QA | SP-0373 Arabic typography QA | — |
| QA-75 | 🟢 | التقاط إطارات مرجعية لمطابقة الأسلوب · Reference capture for style matching | SP-0374 Reference study | ffmpeg |
| QA-90 | 🟢 | دراسة مرجع · study reference | SP-0374 Reference study | python3 |
| QA-99 | 🟢 | دراسة فيلم مرجعي · Reference study | SP-0374 Reference study | — |
| QA-129 | 📦 | حزمة أسلوب بنطاقات إحصائية · Style pack with statistical bands | SP-0374 Reference study | — |
| QA-140 | 📦 | تحليل بصمة المرجع العميق · Style DNA deep reference study | SP-0374 Reference study | — |
| QA-185 | 📦 | تحليل الفيديو · Video analyze breakdown | SP-0374 Reference study | — |
| QA-186 | 📦 | مكتبة الأساليب · Batch style library | SP-0374 Reference study | — |
| QA-190 | 📦 | دراسة الفيديو المرجعي · Reference film study (boundaries, looks, text zones) | SP-0374 Reference study | — |
| QA-198 | 📦 | محلل الفيديو المرجعي · Reference video analyser | SP-0374 Reference study | python3 |
| QA-211 | 📦 | دراسة فيلم مرجعي · Reference film study | SP-0374 Reference study | python3 |
| QA-107 | 🟢 | قياس الحدة والضجيج · Sharpness and noise measurement | SP-0375 Fingerprint similarity score and auto-f… | — |
| QA-125 | 🟢 | فاحص أصالة النصوص · Brief originality n-gram checker | SP-0375 Fingerprint similarity score and auto-f… | python3 |
| QA-136 | 📦 | بوابات جودة الروتوسكوب · Rotoscope fidelity gates | SP-0375 Fingerprint similarity score and auto-f… | — |
| QA-141 | 📦 | درجة التشابه مع المرجع وتصليحها · Fingerprint similarity score and auto-fix | SP-0375 Fingerprint similarity score and auto-f… | — |
| QA-143 | 📦 | نصايح الكوتش بضغطة · Coach tips with one-tap fixes (no AI) | SP-0375 Fingerprint similarity score and auto-f… | — |
| QA-247 | 📄 | مقياس الالتصاق SUCCESs · SUCCESs stickiness score | SP-0375 Fingerprint similarity score and auto-f… | — |
| QA-266 | 📄 | قياس دقة التفريغ وضبط الصمت · ASR WER and endpointing discipline | SP-0375 Fingerprint similarity score and auto-f… | ffmpeg |
| QA-323 | 📄 | قياس بالـ Scopes عبر لقطات · Scope measurement via stills | SP-0375 Fingerprint similarity score and auto-f… | pip:pillow |
| QA-X06 | 📄 | لا قياسات مختلقة · Never fabricate measurements | SP-0375 Fingerprint similarity score and auto-f… | pip:librosa |
| QA-120 | 🟢 | فحص المصدر بـ ffprobe · ffprobe source inspection | SP-0376 Timeline inspection command | ffmpeg, python3 |
| QA-83 | 🟢 | تعليم المقاطع الخطرة نصياً · Text-risk clip flagging | SP-0376 Timeline inspection command | — |
| QA-127 | 📦 | فحص تجاوز النصوص على الخط الزمني · Layout inspect sweep | SP-0376 Timeline inspection command | chromium, npm:hyperframes |
| QA-132 | 📦 | سجل ألوان العلامات · Marker colour registry | SP-0376 Timeline inspection command | — |
| QA-150 | 📦 | أمر: لقطات · CLI: snapshot | SP-0376 Timeline inspection command | npm:hyperframes |
| QA-158 | 📦 | أمر فحص الخط الزمني · Timeline inspection command | SP-0376 Timeline inspection command | npm:hyperframes |
| QA-219 | 🔑 | ترتيب خطوات الإنتاج وسد الفراغات · Production step ordering + gap filling + auto review | SP-0376 Timeline inspection command | imagemagick, key:unspecified |
| QA-324 | 📄 | سجل العلامات الملوّنة · Resolve marker registry | SP-0376 Timeline inspection command | — |
| QA-367 | 📄 | فحص الوصلات · Seam QA pass | SP-0376 Timeline inspection command | — |
| QA-61 | ✅ | أفلام مرجعية مقاسة · Shipped-film benchmark (measured) | SP-0377 Transcript quality gate | — |
| QA-130 | 📦 | قالب تحليل فيديو مرجعي · Reference-video breakdown template | SP-0377 Transcript quality gate | ffmpeg, pip:faster-whisper |
| QA-133 | 📦 | مشاهدة فيديو مرجعي بالإطارات والتفريغ · Watch a reference video (frames + transcript) | SP-0377 Transcript quality gate | ffmpeg, yt-dlp, pip:faster-whisper |
| QA-171 | 📦 | معيار جودة المكونات والمساهمة · Component quality bar and contribution | SP-0377 Transcript quality gate | npm:hyperframes |
| QA-172 | 📦 | فحص جودة النص المفرغ وتنظيفه · Transcript quality check and cleaning | SP-0377 Transcript quality gate | — |
| QA-260 | 📄 | فحص جودة التفريغ · Transcript quality gate | SP-0377 Transcript quality gate | pip:faster-whisper |
| QA-265 | 📄 | فحص جودة التفريغ وإعادة المحاولة · Transcript quality gate + retry | SP-0377 Transcript quality gate | — |
| QA-320 | 📄 | حلقة النقد الذاتي · Critique loop rubric (8 criteria, >= 3 rounds) | SP-0377 Transcript quality gate | python3 |
| QA-346 | 📄 | معيار النقد بمراجعين · Two-reviewer critique rubric | SP-0377 Transcript quality gate | — |
| QA-42 | ✅ | مدقق مواصفة المشهد الصارم · Strict SceneSpec validator (25 fields) | SP-0378 Debug visibility toggles for heavy 3D s… | python3 |
| QA-45 | ✅ | تدقيق صفحات الويب · Static web/HTML audit | SP-0378 Debug visibility toggles for heavy 3D s… | python3, chromium |
| QA-151 | 📦 | أمر: إطارات مفتاحية · CLI: keyframes | SP-0378 Debug visibility toggles for heavy 3D s… | npm:hyperframes |
| QA-153 | 📦 | قواعد الأداء · Performance rules | SP-0378 Debug visibility toggles for heavy 3D s… | — |
| QA-179 | 📦 | مفاتيح إخفاء العناصر لتصحيح المشهد · Debug visibility toggles for heavy 3D scenes | SP-0378 Debug visibility toggles for heavy 3D s… | — |
| QA-236 | 📄 | إخفاء البيانات الحساسة في لقطات الواجهة · Privacy masking for UI footage | SP-0378 Debug visibility toggles for heavy 3D s… | ffmpeg |
| QA-273 | 📄 | ميزانية أداء الشيدر · Shader cost budget | SP-0378 Debug visibility toggles for heavy 3D s… | — |
| QA-321 | 📄 | تشخيص أعطال ffmpeg · ffmpeg troubleshooting table | SP-0378 Debug visibility toggles for heavy 3D s… | ffmpeg |
| QA-348 | 📄 | قائمة صيد العيوب · Failure hunt list | SP-0378 Debug visibility toggles for heavy 3D s… | — |
| QA-36 | ✅ | عميل التصيير البعيد وبوابات الأمان · Remote render client and bridge safety gates | SP-0379 Source hygiene rule (no burned-in text,… | — |
| QA-114 | 🟢 | لوحة معاينة المصادر · Source contact sheet for footage triage | SP-0379 Source hygiene rule (no burned-in text,… | ffmpeg, pip:pillow |
| QA-97 | 🟢 | وسوم الأمانة للمحاكاة التوضيحية · Honesty labels for illustrative simulations | SP-0379 Source hygiene rule (no burned-in text,… | — |
| QA-264 | 📄 | قاعدة المشاهدة مرتين · Watch twice rule | SP-0379 Source hygiene rule (no burned-in text,… | — |
| QA-303 | 📄 | قاعدة الصدق · Honesty rule | SP-0379 Source hygiene rule (no burned-in text,… | — |
| QA-319 | 📄 | قاعدة نظافة المصادر · Source hygiene rule (no burned-in text, logos, screen recordings) | SP-0379 Source hygiene rule (no burned-in text,… | — |
| QA-366 | 📄 | قاعدة الوصلة المتطابقة · Frame-identical seam rule | SP-0379 Source hygiene rule (no burned-in text,… | ffmpeg |
| QA-369 | 💡 | قاعدة العلامات التجارية · Trademark safety rule | SP-0379 Source hygiene rule (no burned-in text,… | — |
| QA-113 | 🟢 | مقارنة إطارين · A/B frame comparison | SP-0380 Compare variants and color grades | python3 |
| QA-152 | 📦 | أمر: مقارنة · CLI: compare / grade-compare | SP-0380 Compare variants and color grades | npm:hyperframes |
| QA-169 | 📦 | مقارنة النسخ ودرجات اللون · Compare variants and color grades | SP-0380 Compare variants and color grades | npm:hyperframes |
| QA-250 | 📄 | بحث تغليف نزيه · Honest packaging research | SP-0380 Compare variants and color grades | — |
| QA-254 | 📄 | ترتيب استبعاد النسخ المولدة · Elimination order for generated variants | SP-0380 Compare variants and color grades | pip:pillow |
| QA-261 | 📄 | قياس التلوين بالمقاييس · Scope-based grade measurement | SP-0380 Compare variants and color grades | ffmpeg, pip:numpy |
| QA-280 | 📄 | التحقق من اللوك بالمقاييس · Scope-target look verification | SP-0380 Compare variants and color grades | ffmpeg, pip:numpy |
| QA-14 | ✅ | فحص الأصول والصياغة الثابت · Static asset and syntax check | SP-0381 Brand art presence & weight tests | node |
| QA-19 | ✅ | اختبارات توحيد الهوية · Single-identity enforcement tests | SP-0381 Brand art presence & weight tests | node |
| QA-20 | ✅ | مقياس انحراف الهوية · Identity drift ratchet (identity_audit) | SP-0381 Brand art presence & weight tests | node |
| QA-21 | ✅ | اختبارات وجود أصول الهوية وخفتها · Brand art presence & weight tests | SP-0381 Brand art presence & weight tests | node |
| QA-78 | 🟢 | وثيقة الهوية المولدة من الرموز · Identity doc generated from tokens | SP-0381 Brand art presence & weight tests | python3 |
| QA-289 | 📄 | سجل المصدر والإفصاح عن الذكاء الاصطناعي · Provenance ledger and AI disclosure | SP-0381 Brand art presence & weight tests | — |
| QA-291 | 📄 | سجل مصدر الأصول · Asset provenance ledger | SP-0381 Brand art presence & weight tests | — |
| QA-33 | ✅ | قواعد نص المشاركة · Share-copy rules | SP-0382 Banned-font / default-colour gate | — |
| QA-159 | 📦 | انتقالات CSS محظورة · Banned CSS transitions | SP-0382 Banned-font / default-colour gate | — |
| QA-196 | 📦 | تحليل حدود اللقطات والمظهر · Shot boundary and look analysis | SP-0382 Banned-font / default-colour gate | — |
| QA-228 | 👁 | تعاقب حلقات تشغيل المعاينات في الشبكة · Staggered loop phases for live grids | SP-0382 Banned-font / default-colour gate | — |
| QA-327 | 📄 | بوابة الخطوط والألوان المحظورة · Banned-font / default-colour gate | SP-0382 Banned-font / default-colour gate | key:openai, fonts:arabic |
| QA-329 | 📄 | علامات التصميم الآلي · AI-design tells blacklist | SP-0382 Banned-font / default-colour gate | — |
| QA-X05 | 📄 | ناقد بعين العميل · Client-proxy critic instead of a generic creative director | SP-0382 Banned-font / default-colour gate | — |
| QA-32 | ✅ | بوابة قابلية قراءة النص · Readability gate for on-screen text | SP-0383 readable | — |
| QA-48 | ✅ | أفضل وقت نشر · Best time from own analytics | SP-0383 readable | python3 |
| QA-66 | ✅ | فحص المستودع والإحصاءات · kosif.py validate / stats | SP-0383 readable | python3 |
| QA-104 | 🟢 | المراجعة: ملاحظات مثبتة على الإطار · Review: pinned frame notes | SP-0383 readable | — |
| QA-92 | 🟢 | فحص المقروئية · readable | SP-0383 readable | python3 |
| QA-368 | 💡 | حد أدنى للقراءة · Readability hold & 400 ms floor | SP-0383 readable | — |
| QA-29 | ✅ | حلّال إنشائي بتحقق يدوي وبوابات ثقة · Structural solver with hand-calc and trust gates | SP-0384 Playwright visual sweeps (desktop + 390… | — |
| QA-39 | ✅ | حماية الواجهة المحلية من المواقع الأخرى · Cross-origin guard for the local API | SP-0384 Playwright visual sweeps (desktop + 390… | — |
| QA-69 | 🟢 | حارس القيم الشاذة · NaN/Inf guard pass | SP-0384 Playwright visual sweeps (desktop + 390… | — |
| QA-79 | 🟢 | مسح بصري بـ Playwright · Playwright visual sweeps (desktop + 390/320px phones) | SP-0384 Playwright visual sweeps (desktop + 390… | node, chromium |
| QA-290 | 📄 | منهج تدقيق الكثافة قبل وبعد · Before/after visual density audit method | SP-0384 Playwright visual sweeps (desktop + 390… | — |
| QA-317 | 📄 | أتمتة المتصفح ولقطات الفحص · Browser automation & screenshot QA (Playwright patterns) | SP-0384 Playwright visual sweeps (desktop + 390… | chromium |
| QA-23 | ✅ | مدقق ملخص المشروع · Brief validator | SP-0385 Pin and upgrade the project CLI | — |
| QA-41 | ✅ | منظف مشروع Studio · Studio project sanitiser | SP-0385 Pin and upgrade the project CLI | node |
| QA-105 | 🟢 | المراجعة: إعادة التحميل التلقائي والروابط العميقة · Review: auto-reload on new version and deep links | SP-0385 Pin and upgrade the project CLI | — |
| QA-155 | 📦 | تثبيت وترقية إصدار الأداة في المشروع · Pin and upgrade the project CLI | SP-0385 Pin and upgrade the project CLI | npm:hyperframes |
| QA-170 | 📦 | سجل المشروع والتراجع لكل دورة · Project history undo per agent turn | SP-0385 Pin and upgrade the project CLI | npm:hyperframes |
| QA-181 | 📦 | فخاخ المحاكاة · Mimic traps rules | SP-0386 No invented glyphs | ffmpeg |
| QA-240 | 📄 | لا تخترع الرقم الذي يصنع الخطاف · Never invent the hook statistic | SP-0386 No invented glyphs | — |
| QA-252 | 📄 | ضوابط الصدق لكل فئة موشن · Category truth guardrails | SP-0386 No invented glyphs | — |
| QA-259 | 📄 | حد أدنى لحجم الترجمة · Readable caption size floor | SP-0386 No invented glyphs | — |
| QA-278 | 📄 | لا تخترع رموزا · No invented glyphs | SP-0386 No invented glyphs | pip:fonttools |
| QA-241 | 📄 | ترجمة مدمجة وحدود الوميض · Burned captions and photosensitivity limits | SP-0387 Flash photosensitivity cap | — |
| QA-258 | 📄 | حد أمان الوميض · Flash-safety cap | SP-0387 Flash photosensitivity cap | — |
| QA-358 | 📄 | حد الوميض الآمن · Flash safety limit | SP-0387 Flash photosensitivity cap | — |
| QA-372 | 💡 | حد الوميض الآمن · Flash photosensitivity cap | SP-0387 Flash photosensitivity cap | — |
| QA-49 | ✅ | تجارب A/B · A/B plan and read | SP-0388 Signal-vs-noise annotation | python3 |
| QA-249 | 📄 | اختيار ذكي للإطارات لمشاهدة الفيديو · Smart frame selection for watching videos | SP-0388 Signal-vs-noise annotation | ffmpeg, pip:numpy |
| QA-283 | 📄 | تعليق الإشارة مقابل الضجيج · Signal-vs-noise annotation | SP-0388 Signal-vs-noise annotation | — |
| QA-U01 | ✅ | طبقة الرسوم وحدها من رندرين · Graphics-only layer from two aligned renders | SP-0389 Graphics-only layer from two aligned re… | — |
| QA-73 | 🟢 | مقارنة صور بدون اعتمادات · Dependency-free PNG visual diff | SP-0389 Graphics-only layer from two aligned re… | node, pip:numpy, pip:pillow |
| QA-282 | 📄 | فحص الشفافية والهالات · Real alpha and halo checks | SP-0389 Graphics-only layer from two aligned re… | pip:pillow |
| QA-272 | 📄 | فخ إعادة الإسناد في TSL · TSL reassignment pitfall | SP-0390 TSL reassignment pitfall | — |
